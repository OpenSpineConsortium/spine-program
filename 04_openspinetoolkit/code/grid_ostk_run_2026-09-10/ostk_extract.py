# spine-program/04_openspinetoolkit: copied 2026-10-08 (read on the grid 2026-10-09 00:12 UTC with `cat`, read-only).
# Source: grid HOME /wsu/home/go/go24/go2432/ostk_run/ostk_extract.py, dated 2026-09-10 03:41; in no repository. Hash of the file as read: sha256 809f823492048917e809893f9e02e50e16a2b74474c9281a816fea2e1feac3be.
# The 2026-09-10 shard run of ostk per-level morphometry; see 04_openspinetoolkit/STATUS.md G.4 and results/grid_run_2026-09-10/README.md.
"""Per-level morphometry for the whole corpus, computed by ostk.

One row per (case, level). Every dimension is a landmark reading in the vertebra's own
frame, so nothing here depends on how the patient lay in the scanner. Sharded by case
index; the shards are concatenated afterwards.

    python ostk_extract.py <labels_dir> <out.csv> <shard> <n_shards>
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import nibabel as nib

from ostk.morphometry import level_morphometry

LEVELS = {19: "T12", 20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6"}
FIELDS = ["case", "level", "VBHa", "VBHp", "EPWu", "EPWl", "EPDu", "EPDl",
          "SCW", "SCD", "PDW_l", "PDW_r", "PDW", "plate_rms_mm"]


def main():
    lab_dir, out_p = Path(sys.argv[1]), Path(sys.argv[2])
    shard = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    n_shards = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    files = sorted(lab_dir.glob("*_label.nii.gz"))[shard::n_shards]
    print(f"shard {shard}/{n_shards}: {len(files)} case(s)", flush=True)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    n_rows = n_drop = 0
    with out_p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for i, f in enumerate(files, 1):
            case = f.name.split("_")[0]
            try:
                img = nib.as_closest_canonical(nib.load(str(f)))
                lab = np.asanyarray(img.dataobj)
                aff = img.affine
            except Exception as exc:
                print(f"  {case}: load failed: {type(exc).__name__}: {exc}", flush=True)
                continue
            present = set(np.unique(lab).tolist())
            for vid, name in LEVELS.items():
                if vid not in present:
                    continue
                try:
                    r = level_morphometry(lab, aff, vid)
                except Exception as exc:
                    print(f"  {case} {name}: {type(exc).__name__}: {exc}", flush=True)
                    n_drop += 1
                    continue
                if r is None:
                    n_drop += 1
                    continue
                row = {k: "" for k in FIELDS}
                row["case"], row["level"] = case, name
                for k, v in r.items():
                    if k in row:
                        row[k] = v
                w.writerow(row)
                n_rows += 1
            if i % 20 == 0:
                fh.flush()
                print(f"  {i}/{len(files)}  rows={n_rows} dropped={n_drop}", flush=True)

    print(f"\nshard {shard}: {n_rows} rows, {n_drop} levels dropped -> {out_p}")


if __name__ == "__main__":
    main()
