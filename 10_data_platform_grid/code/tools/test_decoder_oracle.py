# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_decoder_oracle.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Can the counting decoder recover the levels from PERFECT four-class input?

THIS RUNS BEFORE ANY TRAINING, and if it fails the training is pointless. The baseline is
a segmenter plus a decoder, and a poor score could come from either. Feeding the decoder
ground truth collapsed to four classes removes the segmenter entirely: whatever it gets
wrong here is the counting rule and the instance split, not the network.

It also sets the baseline's CEILING. The trained network cannot beat its own decoder on
perfect input, so this number is the most the counting approach can possibly score on this
cohort -- which is exactly the quantity the paper needs, and it can be measured today.

READ THE BREAKDOWN, NOT THE HEADLINE. Overall per-level accuracy is dominated by ordinary
five-lumbar anatomy and will look high whatever happens at the junction. The rows that carry
the argument are the L6 cases and the lumbar-rib cases.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import nibabel as nib
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enumerate_decoder import decode, summarize  # noqa: E402
from make_quaternary_dataset import build_lut  # noqa: E402

NAMES = {1: "T10", 2: "T11", 3: "T12", 4: "T13", 5: "L1", 6: "L2", 7: "L3",
         8: "L4", 9: "L5", 10: "L6", 11: "sacrum"}
LUMBAR = (5, 6, 7, 8, 9, 10)
IGNORE = 44


def si_axis_of(affine: np.ndarray):
    """Which array axis runs supero-inferior, and whether the index grows cranially."""
    codes = nib.aff2axcodes(affine)
    for i, c in enumerate(codes):
        if c in ("S", "I"):
            return i, c == "S"
    return 2, True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--lstv-json", default=None, help="lstv_cases.json, to pick rare cases")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--cases", default=None, help="comma separated case ids to force in")
    a = ap.parse_args()

    root = Path(a.labels)
    files = sorted(root.glob("*.nii.gz"))
    forced = set((a.cases or "").split(",")) - {""}
    # THE RARE CASES ARE THE EXPERIMENT. case_to_subtype carries the phenotype per case;
    # 'lumb' is lumbarization, which is where an L6 lives, and the sacralizations are the
    # mirror failure. An average dominated by 'normal' would tell us nothing we do not
    # already expect.
    rare: set[str] = set()
    subtype_of: dict[str, str] = {}
    if a.lstv_json and Path(a.lstv_json).exists():
        j = json.load(open(a.lstv_json))
        subtype_of = j.get("case_to_subtype", {}) or {}
        rare = {c for c, s in subtype_of.items()
                if s in ("lumb", "sacralization", "semisacralization", "ambiguous")}
        from collections import Counter as _C
        print("  subtype inventory:", dict(_C(subtype_of.values())))
    # rare cases first: an average over ordinary anatomy hides exactly what matters
    def rank(p: Path):
        stem = p.name.split(".")[0]
        return (0 if any(r in stem for r in forced) else
                1 if any(r in stem for r in rare) else 2, p.name)
    files = sorted(files, key=rank)[: a.limit]
    print(f"{len(files)} cases  ({len(rare)} rare ids known)\n")

    lut = build_lut()
    per_case, conf = [], Counter()
    n_anchor_fail = 0
    for p in files:
        img = nib.load(str(p))
        gt = np.asanyarray(img.dataobj).astype(np.int32)
        quad = lut[np.clip(gt, 0, len(lut) - 1)]
        ax, up = si_axis_of(img.affine)
        d = decode(quad, spacing=img.header.get_zooms()[:3], si_axis=ax,
                   si_increases_cranially=up)
        if not d.anchor_ok:
            n_anchor_fail += 1
            print(f"  {p.name[:28]:<30} ANCHOR FAIL  {d.note}")
            continue

        valid = (gt != IGNORE) & (gt > 0) & (gt <= 11)
        both = valid & (d.labels > 0)
        if not both.any():
            continue
        agree = float((d.labels[both] == gt[both]).mean())
        per_case.append((p.name, agree, d))
        for g, q in zip(gt[both][::97], d.labels[both][::97]):   # sparse sample for the matrix
            if g != q:
                conf[(int(g), int(q))] += 1
        gt_l6 = bool((gt == 10).sum() > 200)
        stem = p.name.split(".")[0]
        sub = subtype_of.get(stem, "?")
        flag = "  <-- L6 IN GT" if gt_l6 else ""
        print(f"  {stem[:22]:<24} {sub:<18} agree {agree:6.1%}   {summarize(d)}{flag}")
        if gt_l6:
            got_l6 = int((d.labels == 10).sum())
            print(f"      L6: gt {int((gt==10).sum()):,} vox, decoder assigned {got_l6:,}"
                  f"  -> {'FOUND' if got_l6 > 200 else 'MISSED'}")

    if not per_case:
        print("\nnothing decoded", file=sys.stderr)
        return 1
    acc = np.array([c[1] for c in per_case])
    print(f"\n  cases decoded        : {len(per_case)}   anchor failures: {n_anchor_fail}")
    print(f"  voxel agreement      : median {np.median(acc):.1%}  mean {acc.mean():.1%}")
    print(f"  cases above 90%      : {int((acc > 0.9).sum())} of {len(acc)}")
    print(f"  cases below 50%      : {int((acc < 0.5).sum())} of {len(acc)}")
    if conf:
        print("\n  most common confusions (gt -> decoded), sampled:")
        for (g, q), n in conf.most_common(10):
            print(f"    {NAMES.get(g,g):<7} -> {NAMES.get(q,q):<7} {n:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
