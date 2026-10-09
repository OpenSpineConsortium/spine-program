#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_label_census.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""What ids a SPINEPS instance mask actually carries, over a sample of cases.

WHY. The body masks built from the cases the retry ladder rescued on a resampled grid came out with ids in the
100s (102-128) alongside the ordinary VerSe ids, and every one of those came back "thin" -- under the
200-voxel body floor. Two readings fit: SPINEPS writes those ids on every case and they are discs, in which
case nothing about the rescue is unusual; or the resample introduced them, in which case a rescued mask is not
the same object as a native one and cannot be shipped beside it. The reading is not argued for here, it is
counted: the same census over masks SPINEPS produced natively months ago and over the rescued ones.

It matters downstream because `tools/body_masks.py` keys a level by its instance id and
`make_drr_dataset.body_boxes` bridges schemes BY NAME -- an id with no VerSe name gets no body box at all.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", required=True, nargs="+")
    ap.add_argument("--sample", type=int, default=40, help="cases per directory (0 = all)")
    ap.add_argument("--only", nargs="*", default=None, help="case names to force in")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    import nibabel as nib
    import numpy as np

    rng = random.Random(a.seed)
    report = {}
    for d in a.dirs:
        files = sorted(glob.glob(os.path.join(os.path.expanduser(d), "*_seg-vert_msk.nii.gz")))
        names = [os.path.basename(f)[: -len("_seg-vert_msk.nii.gz")] for f in files]
        keep = set(a.only or [])
        pool = [f for f, n in zip(files, names) if n not in keep]
        chosen = [f for f, n in zip(files, names) if n in keep]
        if a.sample and len(pool) > a.sample:
            pool = rng.sample(pool, a.sample)
        chosen += pool
        rows, with_high, without_high = [], 0, 0
        idhist: Counter = Counter()
        for f in sorted(chosen):
            case = os.path.basename(f)[: -len("_seg-vert_msk.nii.gz")]
            arr = np.asanyarray(nib.load(f).dataobj)
            vals, cnts = np.unique(arr[arr > 0], return_counts=True)
            ids = {int(v): int(c) for v, c in zip(vals, cnts)}
            high = {k: v for k, v in ids.items() if k >= 100}
            low = {k: v for k, v in ids.items() if k < 100}
            rows.append({"case": case, "n_ids": len(ids), "n_below_100": len(low), "n_at_or_above_100": len(high),
                         "ids": sorted(ids), "voxels_below_100": int(sum(low.values())),
                         "voxels_at_or_above_100": int(sum(high.values())),
                         "rescued_on_a_resampled_grid": os.path.exists(
                             os.path.join(os.path.dirname(f), f"{case}_retry.json"))})
            with_high += bool(high)
            without_high += not high
            idhist.update(ids)
        report[d] = {"n_cases_examined": len(rows), "cases_with_ids_>=100": with_high,
                     "cases_without": without_high,
                     "id_frequency": {str(k): v for k, v in sorted(idhist.items())},
                     "cases": rows}
        print(f"{d}: {len(rows)} cases, {with_high} carry ids >= 100, {without_high} do not", flush=True)
    Path(a.out).write_text(json.dumps(report, indent=1))
    tot_hi = sum(v["cases_with_ids_>=100"] for v in report.values())
    tot = sum(v["n_cases_examined"] for v in report.values())
    print(f"SPINEPS_LABEL_CENSUS_DONE examined={tot} with_high_ids={tot_hi} -> {a.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
