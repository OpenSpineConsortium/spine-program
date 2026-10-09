# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/audit_case_shifts.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Are the wide-context errors scattered, or do they come in whole-case blocks?

The rendered errors said blocks: gl279 contributes T3, T4, T5, T6, T7, T10, T11, T12, L3, L4,
L5 and L6, every one predicted a level cranial; verse015 contributes T12 through L5, every one
predicted a level caudal. That is not a model unsure about a vertebra -- it is a model that
has counted the column and applied the usual convention to a spine that does not follow it.
Which is the thesis of the whole project, showing up in 2-D.

This makes it a number: for a rung's validation errors, how many come from cases carrying
three or more errors with one dominant sign, and do those cases have an atypical count
(a T13 or an L6 in the raw VerSe label, or four lumbar labels)?

    python tools/audit_case_shifts.py --ctx ~/merged_ctx --rung full --verse ~/VerSeFusion/data/unified
"""
from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

LEVELS = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)]
          + ["T13"] + [f"L{i}" for i in range(1, 7)] + ["sacrum"])


def verse_count_flags(case: str, root: Path):
    """From the raw VerSe mask ids: has T13 (28), has L6 (25), number of lumbar labels."""
    hits = glob.glob(str(root / f"scan-{case}" / "*_msk.nii.gz"))
    if not hits:
        return None
    import nibabel as nib
    ids = set(int(v) for v in np.unique(np.asanyarray(nib.load(hits[0]).dataobj)) if v)
    return {"T13": 28 in ids, "L6": 25 in ids, "n_lumbar": len(ids & {20, 21, 22, 23, 24, 25}),
            "n_thoracic": len(ids & set(range(8, 20)))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ctx", required=True)
    ap.add_argument("--rung", required=True)
    ap.add_argument("--tag", default="")
    ap.add_argument("--verse", default=None, help="VerSeFusion unified root, to check raw counts")
    a = ap.parse_args()

    ctx = Path(a.ctx)
    res = json.load(open(ctx / "runs" / f"result_rung_{a.rung}{a.tag}.json"))
    z = np.load(ctx / f"rung_{a.rung}.npz", allow_pickle=True)
    va = np.flatnonzero(z["split"] == "val")
    case = z["case"][va]
    pred, truth = np.array(res["pred"]), np.array(res["truth"])
    off = pred - truth

    per_case = defaultdict(list)
    n_case = Counter(case.tolist())
    for c, o in zip(case, off):
        if o != 0:
            per_case[c].append(int(o))
    n_err = int((off != 0).sum())
    blocks = {c: v for c, v in per_case.items() if len(v) >= 3}
    coherent = {c: v for c, v in blocks.items()
                if abs(sum(np.sign(v))) >= 0.8 * len(v)}
    in_blocks = sum(len(v) for v in blocks.values())
    in_coherent = sum(len(v) for v in coherent.values())
    print(f"rung {a.rung}: {n_err} errors over {len(per_case)} cases "
          f"(of {len(n_case)} validation cases)")
    print(f"  errors in cases with >=3 errors        : {in_blocks} ({100*in_blocks/max(1,n_err):.0f}%) "
          f"in {len(blocks)} cases")
    print(f"  ... of which one-signed (whole-case shift): {in_coherent} ({100*in_coherent/max(1,n_err):.0f}%) "
          f"in {len(coherent)} cases")
    print("\n  case            errors/levels  dominant offset   raw-label flags")
    flagged = 0
    for c, v in sorted(coherent.items(), key=lambda kv: -len(kv[1]))[:20]:
        dom = Counter(v).most_common(1)[0][0]
        flags = ""
        if a.verse and not c.startswith("CTSP"):
            f = verse_count_flags(c, Path(a.verse))
            if f:
                atyp = f["T13"] or f["L6"] or f["n_lumbar"] == 4
                flagged += int(atyp)
                flags = (f"T13={int(f['T13'])} L6={int(f['L6'])} lumbar={f['n_lumbar']} "
                         f"thoracic={f['n_thoracic']}{'  <- atypical count' if atyp else ''}")
        print(f"  {c:<15} {len(v):>3}/{n_case[c]:<3}      {dom:+d}            {flags}")
    if a.verse:
        print(f"\n  whole-case-shift cases with an atypical count in the raw label: {flagged} of "
              f"{sum(1 for c in coherent if not c.startswith('CTSP'))} VerSe cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
