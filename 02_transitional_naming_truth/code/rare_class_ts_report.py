#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_ts_report.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Census of the rare-class TotalSegmentator render root: frames per case, per level class, per subtype.

Verifies the contract of the render step: every one of the 12 SPINEPS+VERIDAH-called cases present with
>= 60 frames, every ann carrying case / scheme / source_case / patient_id / truth / subtype, and every
case keyed by tools/patient_keys.py (run here over this one root -- the dry run the task requires).
Writes <dst>/render_report.json and prints the same.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED = ["TS_s0224", "TS_s0616", "TS_s0790", "TS_s1088", "TS_s1089", "TS_s1123",
            "TS_s1124", "TS_s1171", "TS_s1178", "TS_s1304", "TS_s1350", "TS_s1380"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dst", required=True)
    ap.add_argument("--min-frames", type=int, default=60)
    a = ap.parse_args()
    dst = Path(a.dst).expanduser()
    per_case, per_class, per_subtype, missing_fields = {}, {}, {}, []
    views = {}
    for f in sorted((dst / "ann").glob("*.json")):
        ann = json.load(open(f))
        sc = ann.get("source_case") or "?"
        per_case[sc] = per_case.get(sc, 0) + 1
        st = ann.get("subtype") or "?"
        per_subtype[st] = per_subtype.get(st, 0) + 1
        v = "_lat_" in f.stem and "lat" or "ap"
        views[(sc, v)] = views.get((sc, v), 0) + 1
        for lv in ann.get("levels", {}).values():
            per_class[lv["name"]] = per_class.get(lv["name"], 0) + 1
        for k in ("case", "scheme", "source_case", "patient_id", "truth", "subtype", "subtype_source"):
            if not ann.get(k):
                missing_fields.append(f"{f.stem}:{k}")
        if not (dst / "img" / f"{f.stem}.npy").exists():
            missing_fields.append(f"{f.stem}:IMG_MISSING")
    not_rendered = [c for c in EXPECTED if per_case.get(c, 0) == 0]
    short = {c: n for c, n in per_case.items() if n < a.min_frames}
    # patient_keys dry run over this root alone
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import patient_keys as PK
    cross = PK.d813_crosswalk("~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs")
    vmap = PK.verse_subjects("~/VerSeFusion/data/manifest/manifest.csv")
    keys, unmatched = {}, []
    for f in sorted((dst / "ann").glob("*.json")):
        k = PK.key_for(f.stem, json.load(open(f)), cross, vmap)
        if k is None:
            unmatched.append(f.stem)
        else:
            keys[f.stem] = f"{k[0]}:{k[1]}"
    order = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + ["T13"] + [f"L{i}" for i in range(1, 7)]
    rep = {
        "root": str(dst),
        "n_frames": sum(per_case.values()),
        "frames_per_case": dict(sorted(per_case.items())),
        "frames_per_view": {f"{c}:{v}": n for (c, v), n in sorted(views.items())},
        "frames_per_class": {k: per_class[k] for k in sorted(per_class, key=lambda n: order.index(n) if n in order else 99)},
        "frames_per_subtype": per_subtype,
        "cases_not_rendered": not_rendered,
        "cases_below_min": short,
        "anns_missing_fields": missing_fields[:50],
        "patient_keys": {"n_keyed": len(keys), "n_people": len(set(keys.values())),
                         "people": sorted(set(keys.values())), "unmatched": unmatched[:20],
                         "n_unmatched": len(unmatched)},
    }
    json.dump(rep, open(dst / "render_report.json", "w"), indent=1)
    print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
