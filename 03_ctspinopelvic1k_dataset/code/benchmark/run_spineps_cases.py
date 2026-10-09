#!/usr/bin/env python3
# source-of-copy: spinesurg-ct-nnunet repository (private), branch L6_Class, path benchmark/run_spineps_cases.py; working tree, uncommitted edit on 2026-10-08 (differs from 097933a)
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""benchmark/run_spineps_cases.py — SPINEPS (CT models) with VERIDAH labeling over a shard of
the benchmark case table. Runs in the `spineps` conda env (benchmark/install_envs.sh) with
SPINEPS_SEGMENTOR_MODELS pointing at the unpacked CT models (benchmark/fetch_weights.sh).

Each case is staged alone as <work>/<case>/<case>_ct.nii.gz (spineps writes a derivatives
tree next to its input and names outputs from the input name), `spineps sample` runs on it,
and the vertebra INSTANCE mask (VerSe ids; L6 = 25, T13 = 28 when VERIDAH says so) is
harvested to <out_dir>/<case>_seg-vert_msk.nii.gz with the semantic mask and the centroid
json beside it. Resumable.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import time
from pathlib import Path


def _rank(p: Path):
    """Lower is better. SPINEPS also writes RAW masks (output_raw_*/...seg-vert-raw_msk: instance ids 1..N on its
    cropped grid, no VERIDAH names). Taking "the last file that matches" picked those on the 2026-09-21 real-X-ray
    runs, and every level came out C1..C7. Prefer a non-raw file under derivatives/, then the shortest path."""
    low = [x.lower() for x in p.parts]
    raw = "raw" in p.name.lower() or any("raw" in x for x in low[-4:-1])
    return (raw, "derivatives" not in low and not any(x.startswith("derivatives") for x in low), len(str(p)))


def harvest(stage: Path, case: str, out_dir: Path) -> dict:
    cand = {"vert": [], "spine": [], "ctd": []}
    for p in stage.rglob("*"):
        if not p.is_file():
            continue
        n = p.name
        if n.endswith(".nii.gz") and "seg-vert" in n:
            cand["vert"].append(p)
        elif n.endswith(".nii.gz") and "seg-spine" in n:
            cand["spine"].append(p)
        elif n.endswith(".json") and ("ctd" in n or "poi" in n):
            cand["ctd"].append(p)
    found = {k: sorted(v, key=_rank)[0] for k, v in cand.items() if v}
    # 2026-09-23 (SchwingNet/results/spineps_ids/IMPACT.md): _rank only PREFERS the named derivative; when SPINEPS left
    # nothing but the raw instance mask, sorted(...)[0] still returned it and the case was harvested with ids 1..N
    # under the name "<case>_seg-vert_msk". That is the defect behind 2,437 raw masks. A raw-only candidate is now
    # refused: the case fails, visibly, and nothing is copied under the seg-vert name.
    if "vert" in found and _rank(found["vert"])[0]:
        json.dump({"refused": "only a RAW instance mask (ids 1..N, no VERIDAH names) was produced",
                   "candidates": {k: [str(x) for x in v] for k, v in cand.items()}},
                  open(out_dir / f"{case}_harvest.json", "w"), indent=1)
        raise RuntimeError(f"{case}: only a raw seg-vert mask ({found['vert']}); refused -- its ids are not names")
    dst = {"vert": out_dir / f"{case}_seg-vert_msk.nii.gz",
           "spine": out_dir / f"{case}_seg-spine_msk.nii.gz",
           "ctd": out_dir / f"{case}_ctd.json"}
    for k, p in found.items():
        shutil.copy2(p, dst[k])
    # which file each output came from, and what else was there: a wrong pick is visible without the work tree
    rec = {k: dict(chosen=str(found[k]), candidates=[str(x) for x in cand[k]]) for k in found}
    # the naming test (tools/spineps_ids.py): recorded, never raised here -- a VERIDAH derivative whose own names
    # are out of order is still VERIDAH's output, and every reader that names by id runs the guard itself
    if "vert" in found:
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
            from spineps_ids import check_ids
            chk = check_ids(str(dst["vert"]), str(dst["ctd"]) if "ctd" in found else None)
            rec["naming"] = {k: chk.get(k) for k in ("verdict", "ctd_agree", "ctd_disagree", "reasons")}
        except Exception as e:  # noqa: BLE001  (the record is informational; a failure to test is written down)
            rec["naming"] = {"verdict": "not_tested", "error": repr(e)[:300]}
    json.dump(rec, open(out_dir / f"{case}_harvest.json", "w"), indent=1)
    return {k: str(dst[k]) for k in found}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True, type=Path)
    ap.add_argument("--out_dir", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n_shards", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model_semantic", default="ct")
    ap.add_argument("--model_instance", default="CT_instance")
    ap.add_argument("--model_labeling", default="ct_labeling")
    ap.add_argument("--extra", default="", help="extra flags passed straight to spineps sample")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()

    a.out_dir.mkdir(parents=True, exist_ok=True); a.work.mkdir(parents=True, exist_ok=True)
    with open(a.cases) as fh:
        rows = [r for i, r in enumerate(csv.DictReader(fh)) if i % a.n_shards == a.shard]
    if a.limit:
        rows = rows[: a.limit]
    print(f"shard {a.shard}/{a.n_shards}: {len(rows)} cases", flush=True)
    log = open(a.out_dir / f"timing_shard{a.shard}.jsonl", "a")
    n_done = n_skip = n_fail = 0
    for r in rows:
        case = r["case"]
        if (a.out_dir / f"{case}_seg-vert_msk.nii.gz").exists():
            n_skip += 1; continue
        stage = a.work / case
        shutil.rmtree(stage, ignore_errors=True); stage.mkdir(parents=True)
        staged = stage / f"{case}_ct.nii.gz"
        os.symlink(r["ct"], staged)
        cmd = ["spineps", "sample", "-i", str(staged),
               "--model-semantic", a.model_semantic, "--model-instance", a.model_instance,
               "--model-labeling", a.model_labeling,
               "--ignore-inference-compatibility", "--no-n4"] + (a.extra.split() if a.extra else [])
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout)
            if proc.returncode != 0:
                raise RuntimeError(f"spineps exited {proc.returncode}: {proc.stderr[-600:]}")
            got = harvest(stage, case, a.out_dir)
            if "vert" not in got:
                raise RuntimeError("no seg-vert mask produced; stage tree: " +
                                   ", ".join(p.name for p in stage.rglob("*") if p.is_file())[:500])
            n_done += 1
            rec = {"case": case, "seconds": round(time.time() - t0, 1), "ok": True, "files": got}
            shutil.rmtree(stage, ignore_errors=True)
        except Exception as e:  # noqa: BLE001
            n_fail += 1
            rec = {"case": case, "seconds": round(time.time() - t0, 1), "ok": False, "error": repr(e)[:800]}
        log.write(json.dumps(rec) + "\n"); log.flush()
        print(rec, flush=True)
    print(f"done {n_done}, skipped {n_skip}, failed {n_fail}", flush=True)
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
