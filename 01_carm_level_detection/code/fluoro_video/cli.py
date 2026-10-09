# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/cli.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Command line.

    python -m tools.fluoro_video.cli inventory  [--config C] --work W
    python -m tools.fluoro_video.cli run        [--config C] --work W --out O (--index N | --video-id ID)
    python -m tools.fluoro_video.cli report     [--config C] --work W --out O
    python -m tools.fluoro_video.cli determinism [--config C] --work W --out D --videos ID,ID,ID
    python -m tools.fluoro_video.cli synth      --out D        (the synthetic test videos)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

from . import inventory as INV
from . import pipeline as PL
from . import report as RP
from .common import (PKG_DIR, dump_json, load_config, load_json, load_overrides, strip_volatile)


def _log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def _repo_root():
    return PKG_DIR.parent.parent


def cmd_inventory(a):
    cfg, sha, _ = load_config(a.config)
    ents = INV.build(cfg, _repo_root())
    dump_json(dict(config_sha256=sha, entries=ents), Path(a.work) / "inventory.json")
    inc = [e for e in ents if e.get("include")]
    _log(f"inventory: {len(ents)} files, {len(inc)} videos -> {Path(a.work) / 'inventory.json'}")
    for e in ents:
        _log(f"  {'+' if e.get('include') else '-'} {e['relpath']}: {e['rule']}")
    # fetch source texts once, here (network), so every run reads the cache
    from . import sourcetext as ST
    for e in inc:
        try:
            st, info = ST.for_video(e, Path(a.work) / "source_text", allow_fetch=cfg["speed"]["allow_fetch"])
            _log(f"  source text {e['video_id']}: {len(st)} statements ({info.get('status', '')})")
        except Exception as ex:
            _log(f"  source text {e['video_id']}: failed {ex}")
    return 0


def _entries(work):
    inv = load_json(Path(work) / "inventory.json")
    return [e for e in inv["entries"] if e.get("include")], inv


def cmd_run(a):
    cfg, sha, _ = load_config(a.config)
    ov, ovsha, _ = load_overrides(a.overrides)
    ents, _ = _entries(a.work)
    ents.sort(key=lambda e: e["video_id"])
    if a.video_id:
        sel = [e for e in ents if e["video_id"] == a.video_id]
    else:
        sel = [ents[a.index]] if a.index is not None and a.index < len(ents) else []
    if not sel:
        raise SystemExit("run: no such video")
    rc = 0
    for e in sel:
        if a.skip_done:
            vm = Path(a.out) / e["video_id"] / "video_manifest.json"
            if vm.exists():
                m = load_json(vm)
                from .common import code_identity
                if (m.get("input", {}).get("sha256") == e.get("sha256") and m.get("config_sha256") == sha
                        and m.get("overrides_sha256") == ovsha
                        and m.get("code", {}).get("identity") == code_identity()["identity"]):
                    _log(f"skip {e['video_id']}: done with the same input, config, overrides and code")
                    continue
        try:
            PL.run_video(e, cfg, sha, ov, ovsha, a.out, a.work, log=_log)
        except Exception:
            rc = 1
            tb = traceback.format_exc()
            _log(f"FAILED {e['video_id']}\n{tb}")
            (Path(a.out) / "_failures").mkdir(parents=True, exist_ok=True)
            (Path(a.out) / "_failures" / f"{e['video_id']}.txt").write_text(tb, encoding="utf-8")
    return rc


def cmd_report(a):
    cfg, sha, _ = load_config(a.config)
    ov, ovsha, _ = load_overrides(a.overrides)
    _, inv = _entries(a.work)
    fails = []
    fd = Path(a.out) / "_failures"
    if fd.exists():
        fails = [f"{p.stem}: {p.read_text(encoding='utf-8').strip().splitlines()[-1]}" for p in sorted(fd.glob("*.txt"))]
    man = RP.build(a.out, cfg, sha, ovsha, inv["entries"], fails)
    _log(f"report: {len(man['videos'])} videos, {len(man['clips'])} clips -> {Path(a.out) / 'REPORT.md'}")
    return 0


def cmd_export(a):
    n = RP.export_small(a.out, a.dest)
    _log(f"export: {n} QC images -> {a.dest}")
    return 0


def compare_runs(d1, d2):
    """Identical clip digests and manifests (volatile keys removed) between two output roots."""
    d1, d2 = Path(d1), Path(d2)
    diffs = []
    v1 = sorted(p.relative_to(d1).as_posix() for p in d1.rglob("video_manifest.json"))
    v2 = sorted(p.relative_to(d2).as_posix() for p in d2.rglob("video_manifest.json"))
    if v1 != v2:
        diffs.append(f"manifest sets differ: {v1} vs {v2}")
    for rel in v1:
        if rel not in v2:
            continue
        a = strip_volatile(load_json(d1 / rel))
        b = strip_volatile(load_json(d2 / rel))
        if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
            diffs.append(f"{rel}: differs " + _first_diff(a, b))
    c1 = sorted(p.relative_to(d1).as_posix() for p in d1.rglob("clip.json"))
    c2 = sorted(p.relative_to(d2).as_posix() for p in d2.rglob("clip.json"))
    if c1 != c2:
        diffs.append(f"clip sets differ ({len(c1)} vs {len(c2)})")
    n_same = 0
    for rel in c1:
        if rel not in c2:
            continue
        a, b = load_json(d1 / rel), load_json(d2 / rel)
        if a["digest"] != b["digest"]:
            diffs.append(f"{rel}: digest {a['digest']} vs {b['digest']}")
        elif json.dumps(strip_volatile(a), sort_keys=True) != json.dumps(strip_volatile(b), sort_keys=True):
            diffs.append(f"{rel}: clip.json differs " + _first_diff(strip_volatile(a), strip_volatile(b)))
        else:
            n_same += 1
    return diffs, dict(manifests=len(v1), clips=len(c1), clips_identical=n_same)


def _first_diff(a, b, path=""):
    if type(a) != type(b):
        return f"at {path}: {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"at {path}/{k}: key missing"
            if json.dumps(a[k], sort_keys=True) != json.dumps(b[k], sort_keys=True):
                return _first_diff(a[k], b[k], f"{path}/{k}")
    if isinstance(a, list):
        if len(a) != len(b):
            return f"at {path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True):
                return _first_diff(x, y, f"{path}[{i}]")
    return f"at {path}: {str(a)[:80]} vs {str(b)[:80]}"


def cmd_determinism(a):
    cfg, sha, _ = load_config(a.config)
    ov, ovsha, _ = load_overrides(a.overrides)
    ents, _ = _entries(a.work)
    if a.videos.startswith("auto:"):
        # the N shortest included videos, taking sources in turn (youtube, pmc, commons, ...) so the check spans
        # containers and codecs; ties broken by video_id
        n = int(a.videos.split(":")[1])
        by_src = {}
        for e in sorted(ents, key=lambda e: (e.get("duration_s") or 1e9, e["video_id"])):
            if (e.get("duration_s") or 0) < 20.0:     # long enough to hold a panel segment, cut or cadence
                continue
            by_src.setdefault(e["source"], []).append(e)
        sel = []
        while len(sel) < n and any(by_src.values()):
            for src in sorted(by_src):
                if by_src[src] and len(sel) < n:
                    sel.append(by_src[src].pop(0))
        want = [e["video_id"] for e in sel]
    else:
        want = [v.strip() for v in a.videos.split(",") if v.strip()]
        sel = [e for e in ents if e["video_id"] in want]
    if len(sel) < 3:
        raise SystemExit(f"determinism: need >= 3 videos, found {len(sel)} of {want}")
    out = Path(a.out)
    for run in ("run1", "run2"):
        for e in sel:
            PL.run_video(e, cfg, sha, ov, ovsha, out / run, Path(a.work) / f"det_{run}", log=_log,
                         text_cache=Path(a.work) / "source_text")
    diffs, stats = compare_runs(out / "run1", out / "run2")
    res = dict(videos=want, **stats, identical=not diffs, differences=diffs,
               excluded_keys="run_timestamp, wall_time_s, host (and other VOLATILE_KEYS in common.py)")
    dump_json(res, out / "determinism.json")
    _log(f"determinism: {'IDENTICAL' if not diffs else 'DIFFERENT'} {stats}")
    for d in diffs[:20]:
        _log(f"  {d}")
    return 0 if not diffs else 1


def cmd_synth(a):
    from . import synth
    synth.make_all(Path(a.out))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Programmatic fluoroscopy panel extraction from composite videos")
    ap.add_argument("cmd", choices=["inventory", "run", "report", "determinism", "synth", "export"])
    ap.add_argument("--config", default=None)
    ap.add_argument("--overrides", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--index", type=int, default=None)
    ap.add_argument("--video-id", default=None)
    ap.add_argument("--videos", default="")
    ap.add_argument("--dest", default=None, help="export: folder for REPORT.md, manifests and downsized QC images")
    ap.add_argument("--skip-done", action="store_true",
                    help="run: skip a video whose manifest has the same input sha256, config, overrides and code")
    a = ap.parse_args(argv)
    return dict(inventory=cmd_inventory, run=cmd_run, report=cmd_report, determinism=cmd_determinism,
                synth=cmd_synth, export=cmd_export)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
