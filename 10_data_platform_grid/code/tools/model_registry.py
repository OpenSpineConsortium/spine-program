# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/model_registry.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""The model registry: every trained weight file is stored once, immutably, under its own content hash, tracked
in MLflow, and pushed off the cluster. No script ever addresses a model by a mutable path again.

Why this exists: on 2026-09-15 a chain ran `ln -sf model.pt model.pt`, which replaces the file with a link to
itself, and a 2.5-hour model was gone two minutes after it was written. A registry makes that impossible: the
store is content-addressed (the name IS the hash, so nothing can be overwritten), files are made read-only, and
each registration is mirrored to a private Hugging Face repo so a lost cluster directory is a restore, not a
retrain.

    store        ~/model_registry/<sha256[:16]>/<file>       read-only, one directory per artifact
    ledger       ~/model_registry/registry.jsonl             one line per registration (name, sha, metrics, git, source)
    aliases      ~/model_registry/aliases/<name>             symlink -> the store entry, moved atomically; `latest` per name
    tracking     MLflow, SQLite store at ~/mlflow/mlflow.db (mlflow ui --backend-store-uri sqlite:///$HOME/mlflow/mlflow.db)
                 logged from the login node by `sync` when the registering env has no MLflow (compute jobs)
    mirror       hf://gregoryschwingmdphd/level-id-weights/registry/<name>/<sha>.<ext>   (private repo)
    lineage      ~/model_registry/lineage.jsonl              one line per (sha, what it was initialised from, which train
                 and val/selection lists it read); written by register(parents=..., train_list=..., val_list=...)
                 and by tools/checkpoint_lineage.py for weights that were never copied into the store

    python tools/model_registry.py register PATH --name allspine_v2_rung1 --stage level_model --metrics result.json --bank ~/allspine_v2_fov96_ctx
    python tools/model_registry.py resolve allspine_v2_rung1            # -> store path of the newest registration
    python tools/model_registry.py link  allspine_v2_rung1 /some/dir/model_rung_1_aug2.pt   # a safe alias, never ln -sf onto a file
    python tools/model_registry.py backfill                              # register every existing weight file the pipeline uses
    python tools/model_registry.py restore <sha>                         # pull a store entry back from the mirror
    python tools/model_registry.py list
    python tools/model_registry.py lineage <sha prefix | name>             # what a model was initialised from and saw

Training scripts call `register()` right after they save; chains call `resolve()` / `link()` instead of guessing
file names. The mirror push needs the personal HF token at ~/.cache/huggingface/token and is skipped, with a note in
the ledger, when it is absent or offline; `sync` pushes whatever is not yet mirrored.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

STORE = Path(os.environ.get("MODEL_REGISTRY", "~/model_registry")).expanduser()
LEDGER = STORE / "registry.jsonl"
LINEAGE = STORE / "lineage.jsonl"   # kept apart from the ledger: resolve() reads the ledger's last row per name
ALIASES = STORE / "aliases"
MLFLOW_DIR = Path(os.environ.get("MLFLOW_DIR", "~/mlflow")).expanduser()
MIRROR_REPO = os.environ.get("MODEL_MIRROR_REPO", "gregoryschwingmdphd/level-id-weights")
TOKEN_FILE = Path("~/.cache/huggingface/token").expanduser()


def sha256_of(p: Path, chunk=1 << 22) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def git_commit(repo=None) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo or Path(__file__).resolve().parent.parent), "rev-parse", "--short", "HEAD"],
                                       stderr=subprocess.DEVNULL, timeout=10).decode().strip()
    except Exception:  # noqa: BLE001
        return ""


def read_ledger():
    if not LEDGER.exists():
        return []
    out = []
    for l in open(LEDGER, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except Exception:  # noqa: BLE001
            pass
    return out


def _mirror_push(entry: dict) -> str:
    """copy the store file to the private HF repo; returns the remote path or '' when it could not."""
    if not TOKEN_FILE.exists() or os.environ.get("HF_HUB_OFFLINE") == "1":
        return ""
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=TOKEN_FILE.read_text().strip())
        remote = f"registry/{entry['name']}/{entry['sha'][:16]}{Path(entry['file']).suffix}"
        api.upload_file(path_or_fileobj=entry["store_path"], path_in_repo=remote, repo_id=MIRROR_REPO, repo_type="model",
                        commit_message=f"registry: {entry['name']} {entry['sha'][:16]}")
        return remote
    except Exception as e:  # noqa: BLE001
        print("mirror push failed:", type(e).__name__, file=sys.stderr)
        return ""


def try_register(path, name, **kw):
    """register() that cannot take a training run down: every failure is a line on stderr, never an exception.
    Trainers call this right after torch.save; the mirror push is left to the login node (`sync`) because compute
    nodes have no route out, so pass push=False from a job."""
    try:
        return register(path, name, **kw)
    except Exception as e:  # noqa: BLE001
        print(f"    registry: could not register {path} as {name}: {type(e).__name__}: {e}", file=sys.stderr)
        return None


def _mlflow_log(entry: dict):
    try:
        import mlflow
    except ImportError:
        return None
    try:
        # SQLite store by default (the file store is deprecated in MLflow 3); MLFLOW_TRACKING_URI overrides
        MLFLOW_DIR.mkdir(parents=True, exist_ok=True)
        mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI") or f"sqlite:///{MLFLOW_DIR / 'mlflow.db'}")
        exp_name = entry.get("stage") or "models"
        if mlflow.get_experiment_by_name(exp_name) is None:   # artifacts under ~/mlflow, not ./mlruns in whatever cwd
            mlflow.create_experiment(exp_name, artifact_location=str(MLFLOW_DIR / "artifacts" / exp_name))
        mlflow.set_experiment(exp_name)
        with mlflow.start_run(run_name=f"{entry['name']}@{entry['sha'][:8]}") as run:
            mlflow.set_tags({"name": entry["name"], "sha256": entry["sha"], "git": entry.get("git", ""), "bank": entry.get("bank", ""),
                             "source_path": entry.get("source_path", ""), "mirror": entry.get("mirror", ""), "store_path": entry["store_path"]})
            for k, v in (entry.get("metrics") or {}).items():
                if isinstance(v, (int, float)):
                    mlflow.log_metric(k, float(v))
            mlflow.log_params({k: str(v)[:250] for k, v in (entry.get("params") or {}).items()})
            # the weights themselves stay in the store and the mirror (both immutable); the run carries a pointer.
            # Written to tmpfs: MLflow copies xattrs when it stages an artifact and NFS refuses to set them.
            import tempfile
            tdir = Path("/dev/shm") if Path("/dev/shm").is_dir() else Path(tempfile.gettempdir())
            with tempfile.TemporaryDirectory(dir=tdir) as td:
                pj = Path(td) / "registration.json"
                pj.write_text(json.dumps({k: v for k, v in entry.items() if k != "mlflow_run"}, indent=1), encoding="utf-8")
                mlflow.log_artifact(str(pj))
            return run.info.run_id
    except Exception as e:  # noqa: BLE001
        print("mlflow logging failed:", type(e).__name__, str(e)[:200], file=sys.stderr)
        return None


def register(path, name, stage="model", metrics=None, params=None, bank=None, note="", push=True,
             parents=None, train_list=None, val_list=None):
    """copy `path` into the immutable store, ledger it, log it, mirror it; returns the ledger entry.

    `parents` is what the weights were INITIALISED from (a path, a registry sha, or a declared public root such
    as "public:torchvision/resnet18/IMAGENET1K_V1"); `train_list` and `val_list` name what the run fitted on and
    what it SELECTED the checkpoint on ("<bank>/rung_1.npz#train", a data.yaml, a list file). A model registered
    without them says nothing about what it saw, which is how a checkpoint-selection subject was scored as
    held out on 2026-09-23 (SchwingNet/results/arc/ARC_CHECK.md item 4)."""
    src = Path(path).expanduser().resolve()
    if not src.is_file():
        raise FileNotFoundError(src)
    sha = sha256_of(src)
    d = STORE / sha[:16]; d.mkdir(parents=True, exist_ok=True)
    dst = d / src.name
    if not dst.exists():
        shutil.copy2(src, dst); os.chmod(dst, 0o444)
    elif sha256_of(dst) != sha:
        raise RuntimeError(f"store collision at {d}: different content for the same prefix")
    if isinstance(metrics, (str, Path)):
        try:
            mj = json.load(open(Path(metrics).expanduser()))
            metrics = {k: v for k, v in mj.items() if isinstance(v, (int, float))}
        except Exception:  # noqa: BLE001
            metrics = {}
    entry = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "name": name, "stage": stage, "file": src.name, "sha": sha, "bytes": src.stat().st_size,
             "store_path": str(dst), "source_path": str(src), "bank": str(bank or ""), "git": git_commit(), "metrics": metrics or {},
             "params": params or {}, "note": note, "mirror": "",
             "parents": _as_list(parents), "train_list": _as_list(train_list), "val_list": _as_list(val_list)}
    if push:
        entry["mirror"] = _mirror_push(entry)
    entry["mlflow_run"] = _mlflow_log(entry)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    if entry["parents"] or entry["train_list"] or entry["val_list"]:
        record_lineage(sha, str(src), parents=entry["parents"], train_list=entry["train_list"],
                       val_list=entry["val_list"], source="register", name=name)
    ALIASES.mkdir(exist_ok=True)
    _set_alias(name, dst)
    print(f"registered {name} {sha[:16]} ({entry['bytes'] // 1_000_000} MB) -> {dst}" + (f"; mirrored to {entry['mirror']}" if entry["mirror"] else "; NOT mirrored"))
    return entry


def _set_alias(name, target: Path):
    """aliases/<name> -> store file; written to a temp name and renamed, so a half-written link never exists and
    a target is never replaced by a link to itself."""
    ALIASES.mkdir(parents=True, exist_ok=True)
    tmp = ALIASES / f".{name}.tmp"
    if tmp.exists() or tmp.is_symlink():
        tmp.unlink()
    os.symlink(str(target), str(tmp)); os.replace(str(tmp), str(ALIASES / name))


def _as_list(x):
    if x is None or x == "":
        return []
    return [str(v) for v in x] if isinstance(x, (list, tuple, set)) else [str(x)]


def record_lineage(sha, path, parents=None, train_list=None, val_list=None, source="", **extra):
    """append one lineage row for weights with content hash `sha` at `path`. Nothing is copied into the store, so
    this is safe for every checkpoint a result scored, registered or not. `extra` carries what the writer knows
    beyond the three lists (key counts, the touched.json it came from, what could not be resolved). An empty
    `parents` means NOTHING WAS RECORDED, not 'trained from scratch': a from-scratch or public-root start is
    written as such ('scratch', 'public:...') by whoever knows it."""
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "sha": sha, "path": str(path),
           "registered": any(r.get("sha") == sha for r in read_ledger()),
           "parents": _as_list(parents), "train_list": _as_list(train_list), "val_list": _as_list(val_list),
           "source": source, **extra}
    LINEAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(LINEAGE, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def lineage_of(key):
    """every lineage row whose sha starts with `key`, or whose registration is named `key` (newest last)."""
    shas = {r["sha"] for r in read_ledger() if r.get("name") == key}
    if not LINEAGE.exists():
        return []
    out = []
    for l in open(LINEAGE, encoding="utf-8"):
        try:
            r = json.loads(l)
        except Exception:  # noqa: BLE001
            continue
        if str(r.get("sha", "")).startswith(key) or r.get("sha") in shas:
            out.append(r)
    return out


def resolve(name, sha_prefix=None) -> Path:
    rows = [r for r in read_ledger() if r["name"] == name and (not sha_prefix or r["sha"].startswith(sha_prefix))]
    if not rows:
        raise SystemExit(f"no registration named {name!r}" + (f" with sha {sha_prefix}" if sha_prefix else ""))
    p = Path(rows[-1]["store_path"])
    if not p.exists():
        raise SystemExit(f"store entry missing for {name}: {p}; run `model_registry.py restore {rows[-1]['sha'][:16]}`")
    return p


def link(name, dest, sha_prefix=None):
    """a symlink at `dest` to the registered file. Refuses to touch a real file at `dest`; replaces only links."""
    target = resolve(name, sha_prefix); dest = Path(dest).expanduser()
    if dest.exists() and not dest.is_symlink():
        raise SystemExit(f"refusing to replace a real file with a link: {dest} (register it first if it matters)")
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f".{dest.name}.tmp"
    if tmp.exists() or tmp.is_symlink():
        tmp.unlink()
    os.symlink(str(target), str(tmp)); os.replace(str(tmp), str(dest))
    print(f"{dest} -> {target}")


def restore(sha_prefix):
    rows = [r for r in read_ledger() if r["sha"].startswith(sha_prefix)]
    if not rows:
        raise SystemExit("unknown sha")
    r = rows[-1]; dst = Path(r["store_path"])
    if dst.exists() and sha256_of(dst) == r["sha"]:
        print("already present:", dst); return dst
    if not r.get("mirror"):
        raise SystemExit("this registration was never mirrored; nothing to restore from")
    from huggingface_hub import hf_hub_download
    got = hf_hub_download(MIRROR_REPO, r["mirror"], repo_type="model", token=TOKEN_FILE.read_text().strip())
    dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(got, dst); os.chmod(dst, 0o444)
    if sha256_of(dst) != r["sha"]:
        raise SystemExit("restored file does not match its recorded hash")
    print("restored", dst); return dst


MLFLOW_RUNS = STORE / "mlflow_runs.jsonl"   # sha -> MLflow run id, for registrations logged after the fact


def sync():
    """login-node follow-through for what a compute node could not do: push every unmirrored entry to the HF
    mirror, and log every entry without an MLflow run (trainers register in envs without MLflow) to the tracking
    store. Idempotent; safe to run after every chain step."""
    rows = read_ledger(); done = 0
    seen = set()
    for r in rows:
        if r.get("mirror") or r["sha"] in seen:
            continue
        seen.add(r["sha"])
        m = _mirror_push(r)
        if m:
            r["mirror"] = m; done += 1
            with open(LEDGER, "a", encoding="utf-8") as f:
                f.write(json.dumps({**r, "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "note": "mirror sync"}) + "\n")
    print(f"mirrored {done} entries")
    logged = set()
    if MLFLOW_RUNS.exists():
        logged = {json.loads(l)["sha"] for l in open(MLFLOW_RUNS, encoding="utf-8") if l.strip()}
    logged |= {r["sha"] for r in rows if r.get("mlflow_run")}
    n = 0
    for r in rows:
        if r["sha"] in logged or not Path(r["store_path"]).exists():
            continue
        run = _mlflow_log(r)
        if run:
            logged.add(r["sha"]); n += 1
            with open(MLFLOW_RUNS, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sha": r["sha"], "name": r["name"], "mlflow_run": run, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
    print(f"logged {n} entries to MLflow")


def listing():
    rows = read_ledger(); last = {}
    for r in rows:
        last[r["name"]] = r
    for n, r in sorted(last.items()):
        m = ", ".join(f"{k} {v:.3f}" if isinstance(v, float) else f"{k} {v}" for k, v in list((r.get("metrics") or {}).items())[:4])
        print(f"{n:34s} {r['sha'][:12]}  {r['bytes'] // 1_000_000:5d} MB  {r['ts'][:16]}  {'mirrored' if r.get('mirror') else 'local only'}  {m}")


BACKFILL = [
    # name, path, stage, metrics json (optional), bank
    ("films_all2_rung1_aug2", "~/films_all2_fov96_ctx/runs/model_rung_1_aug2.pt", "level_model", "~/films_all2_fov96_ctx/runs/result_rung_1_aug2.json", "~/films_all2_fov96_ctx"),
    ("films_all2_rung1", "~/films_all2_fov96_ctx/runs/model_rung_1.pt", "level_model", "~/films_all2_fov96_ctx/runs/result_rung_1.json", "~/films_all2_fov96_ctx"),
    ("films_all2_rung2_aug2", "~/films_all2_fov96_ctx/runs/model_rung_2_aug2.pt", "level_model", "~/films_all2_fov96_ctx/runs/result_rung_2_aug2.json", "~/films_all2_fov96_ctx"),
    ("films_all2_rung2", "~/films_all2_fov96_ctx/runs/model_rung_2.pt", "level_model", "~/films_all2_fov96_ctx/runs/result_rung_2.json", "~/films_all2_fov96_ctx"),
    ("allspine_v1_rung1_aug2", "~/allspine_fov96_ctx/runs/model_rung_1_aug2_aug2.pt", "level_model", "~/allspine_fov96_ctx/runs/result_rung_1_aug2_aug2.json", "~/allspine_fov96_ctx"),
    ("allspine_v2_rung1_aug2", "~/allspine_v2_fov96_ctx/runs/model_rung_1_aug2.pt", "level_model", "~/allspine_v2_fov96_ctx/runs/result_rung_1_aug2.json", "~/allspine_v2_fov96_ctx"),
    ("recurrent_head_films_all2_r1", "~/FluoroCap/recurrent_head_films_all2_fov96_ctx_d081b4ab_r1.pt", "recurrent_head", None, "~/films_all2_fov96_ctx"),
    ("detector_v5z_final", "~/FluoroCap/detect_v5z_final_best.pt", "detector", None, ""),
    ("detector_v5z_epoch25", "~/FluoroCap/detect_v5z_epoch25_best.pt", "detector", None, ""),
    ("detector_v6f", "~/FluoroCap/detect_v6f_best.pt", "detector", None, ""),
    ("anchor_detector_v1", "~/FluoroCap/anchor_det_v1.pt", "anchor_detector", None, "~/anchor_drr"),
    ("anchor_detector_v2", "~/FluoroCap/anchor_det_v2.pt", "anchor_detector", None, "~/anchor_drr"),
    ("orientation_net", "~/FluoroCap/orientation_net.pt", "orientation", None, ""),
    ("hardware_detector_v1", "~/FluoroCap/hardware_det_v1.pt", "hardware_detector", None, ""),
    ("hardware_detector_v2", "~/FluoroCap/hardware_det_v2.pt", "hardware_detector", None, ""),
    ("panel_classifier", "~/FluoroCap/panel_classifier.pt", "panel_classifier", None, ""),
    ("fluorogen_lora_v1", "~/fluorogen/lora_v1/pytorch_lora_weights.safetensors", "generator_lora", None, "~/fluorogen/dataset_v1"),
    ("cut_drr2fluoro_G", "~/cut_v1/G_last.pt", "translator", None, "~/physics_drr"),
]


def backfill():
    n = 0
    for name, p, stage, metrics, bank in BACKFILL:
        pp = Path(p).expanduser()
        if not pp.is_file():
            continue
        try:
            register(pp, name, stage=stage, metrics=(Path(metrics).expanduser() if metrics and Path(metrics).expanduser().exists() else None), bank=bank, note="backfill"); n += 1
        except Exception as e:  # noqa: BLE001
            print("skip", name, type(e).__name__, e, file=sys.stderr)
    print(f"backfilled {n} models")


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register"); r.add_argument("path"); r.add_argument("--name", required=True); r.add_argument("--stage", default="model")
    r.add_argument("--metrics", default=None, help="json file of numbers"); r.add_argument("--bank", default=None); r.add_argument("--note", default="")
    r.add_argument("--no-push", action="store_true")
    r.add_argument("--parent", action="append", default=None, help="what the weights were initialised from (repeatable)")
    r.add_argument("--train-list", action="append", default=None); r.add_argument("--val-list", action="append", default=None)
    ln = sub.add_parser("lineage"); ln.add_argument("key", help="sha prefix or registration name")
    s = sub.add_parser("resolve"); s.add_argument("name"); s.add_argument("--sha", default=None)
    lk = sub.add_parser("link"); lk.add_argument("name"); lk.add_argument("dest"); lk.add_argument("--sha", default=None)
    rs = sub.add_parser("restore"); rs.add_argument("sha")
    sub.add_parser("backfill"); sub.add_parser("sync"); sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "register":
        register(a.path, a.name, a.stage, a.metrics, bank=a.bank, note=a.note, push=not a.no_push,
                 parents=a.parent, train_list=a.train_list, val_list=a.val_list)
    elif a.cmd == "lineage":
        rows = lineage_of(a.key)
        if not rows:
            print(f"no lineage recorded for {a.key!r} -- that is NOT a statement that it saw nothing")
            return 1
        for r in rows:
            print(json.dumps(r, indent=1))
    elif a.cmd == "resolve":
        print(resolve(a.name, a.sha))
    elif a.cmd == "link":
        link(a.name, a.dest, a.sha)
    elif a.cmd == "restore":
        restore(a.sha)
    elif a.cmd == "backfill":
        backfill()
    elif a.cmd == "sync":
        sync()
    elif a.cmd == "list":
        listing()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
