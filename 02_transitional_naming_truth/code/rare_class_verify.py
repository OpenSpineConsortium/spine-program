#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_verify.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Verify the rare-class VerSe render root: counts per case / subtype / vertebra class, and the misses.

Reads every ann under --root, checks each of the 56 expected cases reached the frame floor (>= 60
distinct frames), tallies frames per vertebra class (a frame counts for a class when that vertebra's
silhouette survived projection into it) and per subtype, and dry-runs tools/patient_keys.py over the
root so an unkeyable ann fails HERE, not in the split.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--subtypes", required=True)
    ap.add_argument("--floor", type=int, default=60)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(os.path.expanduser(a.root))
    subs = json.load(open(os.path.expanduser(a.subtypes)))
    subs = {k: v for k, v in subs.items() if not k.startswith("_")}   # _about / _n of the maximize jsons
    anns = sorted((root / "ann").glob("*.json"))
    per_case, per_class, per_sub, per_view = Counter(), Counter(), Counter(), Counter()
    styled, raw = Counter(), Counter()
    cls_by_sub = defaultdict(Counter)
    bad = []
    for p in anns:
        try:
            d = json.load(open(p))
        except Exception as e:  # noqa: BLE001
            bad.append(f"{p.name}: unreadable ({e})")
            continue
        case = d.get("source_case")
        if case not in subs:
            bad.append(f"{p.name}: source_case {case} not in the subtype table")
            continue
        img = root / "img" / (p.stem + ".npy")
        if not img.exists():
            bad.append(f"{p.name}: no img npy")
            continue
        per_case[case] += 1
        per_sub[d.get("subtype", "?")] += 1
        per_view[d.get("view", "?")] += 1
        (styled if d.get("styled") else raw)[case] += 1
        for rec in d.get("levels", {}).values():
            per_class[rec["name"]] += 1
            cls_by_sub[d.get("subtype", "?")][rec["name"]] += 1
    missing = sorted(set(subs) - set(per_case))
    below = {c: n for c, n in sorted(per_case.items()) if n < a.floor}

    # patient_keys dry run over this root alone
    pk_out = root / "patient_keys_dryrun.json"
    r = subprocess.run([sys.executable, str(Path(__file__).parent / "patient_keys.py"),
                        "--drr", str(root), "--out", str(pk_out)],
                       capture_output=True, text=True)
    pk = json.load(open(pk_out)) if pk_out.exists() else {}
    rep = dict(
        root=str(root), anns=len(anns),
        cases=len(per_case), frames_total=sum(per_case.values()),
        frames_raw=sum(raw.values()), frames_styled=sum(styled.values()),
        per_subtype=dict(per_sub), per_view=dict(per_view),
        frames_per_class=dict(sorted(per_class.items())),
        frames_per_class_by_subtype={k: dict(sorted(v.items())) for k, v in cls_by_sub.items()},
        frames_per_case=dict(sorted(per_case.items())),
        below_floor=below, floor=a.floor, missing_cases=missing, bad=bad,
        patient_keys=dict(n_cases=len(pk.get("keys", {})), n_people=pk.get("n_people"),
                          unmatched=pk.get("unmatched", ["patient_keys.py did not run"]),
                          by_scheme=pk.get("by_scheme"), stderr_tail=r.stderr[-400:] if r.stderr else ""),
    )
    json.dump(rep, open(os.path.expanduser(a.out), "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("cases", "frames_total", "frames_raw", "frames_styled",
                                          "per_subtype", "missing_cases", "below_floor", "bad")}, indent=1))
    print("frames_per_class:", json.dumps(rep["frames_per_class"]))
    print("patient_keys:", json.dumps(rep["patient_keys"]["n_cases"]), "keyed,",
          len(rep["patient_keys"]["unmatched"]), "unmatched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
