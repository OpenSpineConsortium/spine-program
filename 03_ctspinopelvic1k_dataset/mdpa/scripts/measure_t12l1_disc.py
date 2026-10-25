"""The T12/L1 disc space, measured from the labels, as an independent transition point.

    python measure_t12l1_disc.py --labels <dir of *_label.nii.gz> [--jobs 6]

WHY THIS EXISTS. The release ships disc heights for L1L2 down to L5S1 (`degenerative.csv`,
`level_atlas.csv`) and nothing at T12/L1, so the thoracolumbar junction had no measured
ground truth and the labelled name was standing in for one. The disc is simply the gap
between the inferior surface of T12 (id 19) and the superior surface of L1 (id 20), and the
label volumes carry both, so it can be measured rather than assumed.

WHAT MAKES IT WORTH MEASURING. Disc height is NOT one of the classifier's features, which
are end-plate width, anterior and posterior body height, canal width and transverse-process
span, each over the case's own median, plus ratios between them. So the T12/L1 disc is an
independent check on where the junction sits, not a restatement of the thing being checked.

THE METHOD IS extract_degenerative.py's, NOT A NEW ONE, and the trap it records is the
reason: vertebral end-plates are CONCAVE, so the lowest voxel of the upper body anywhere in
a wide column is its rim projecting down into the space. Measuring rim to rim read 4 to 6 mm
against a published lumbar 8 to 12. The height is therefore taken PER COLUMN through the
overlap of the two bodies, and the median of those columns is what a radiologist reads off a
mid-sagittal slice. Volumes are canonicalised for ANALYSIS only; nothing is written back.

THE SAME CODE COMPUTES L1L2, WHICH THE RELEASE ALREADY HOLDS. That is the check: if this
file's L1L2 does not reproduce degenerative.csv's, the T12L1 column is measuring something
else and must not be used. The agreement is printed at the end.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import nibabel as nib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_degenerative import MIN_VOX, body_of

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "morphometrics"
PAIRS = [(19, 20, "T12L1"), (20, 21, "L1L2")]     # L1L2 is the control, not a result


def disc_height(bu, bl, sp):
    """Gap between two bodies in mm, per column through their overlap, then the median."""
    iu, il = np.argwhere(bu), np.argwhere(bl)
    if len(iu) < 40 or len(il) < 40:
        return None

    def _mid(a, b):
        # the middle of the OVERLAP, not of the union: where one body is offset from the
        # other, the union's median lands where only one of them is and samples nothing
        lo, hi = max(a.min(), b.min()), min(a.max(), b.max())
        return 0.5 * (lo + hi) if hi >= lo else float(np.median(np.concatenate([a, b])))

    cx, cy = _mid(iu[:, 0], il[:, 0]), _mid(iu[:, 1], il[:, 1])
    rx, ry = max(2, int(round(8.0 / sp[0]))), max(2, int(round(8.0 / sp[1])))
    sel_u = iu[(np.abs(iu[:, 0] - cx) <= rx) & (np.abs(iu[:, 1] - cy) <= ry)]
    sel_l = il[(np.abs(il[:, 0] - cx) <= rx) & (np.abs(il[:, 1] - cy) <= ry)]
    if len(sel_u) < 40 or len(sel_l) < 40:
        return None
    cols = {}
    for xx, yy, zz in sel_u:
        k = (xx, yy)
        c0 = cols.setdefault(k, [None, None])[0]
        cols[k][0] = zz if c0 is None else min(c0, zz)
    for xx, yy, zz in sel_l:
        k = (xx, yy)
        if k not in cols:
            continue
        c1 = cols[k][1]
        cols[k][1] = zz if c1 is None else max(c1, zz)
    gaps = [a - b for a, b in cols.values() if a is not None and b is not None]
    if len(gaps) < 15:
        return None
    gap_vox = float(np.median(gaps))
    if not (-2 < gap_vox < 60):
        return None
    return round(max(0.0, gap_vox * sp[2]), 1)


def one(path):
    stem = Path(path).name.replace("_label.nii.gz", "")
    r = {"case": stem}
    try:
        li = nib.as_closest_canonical(nib.load(path))     # ANALYSE in RAS; never written
        lab = np.asanyarray(li.dataobj)
        sp = np.asarray(li.header.get_zooms()[:3], float)
    except Exception as exc:                                        # noqa: BLE001
        return {"case": stem, "error": type(exc).__name__}
    bodies = {}
    for vid in (19, 20, 21):
        m = lab == vid
        if m.sum() >= MIN_VOX:
            b = body_of(m)
            if b is not None:
                bodies[vid] = b
    for up, lo, name in PAIRS:
        bu, bl = bodies.get(up), bodies.get(lo)
        if bu is None or bl is None:
            continue
        h = disc_height(bu, bl, sp)
        if h is not None:
            r["disc_%s_mm" % name] = h
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True, help="directory of *_label.nii.gz")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--out", default=str(DATA / "t12l1_disc.csv"))
    a = ap.parse_args()

    files = sorted(str(p) for p in Path(a.labels).glob("*_label.nii.gz"))
    print("%d label volumes, %d workers" % (len(files), a.jobs))
    rows = []
    with Pool(a.jobs) as pool:
        for i, r in enumerate(pool.imap_unordered(one, files, chunksize=4), 1):
            rows.append(r)
            if i % 100 == 0:
                print("  %d/%d" % (i, len(files)), flush=True)
    rows.sort(key=lambda d: d["case"])
    cols = ["case", "disc_T12L1_mm", "disc_L1L2_mm", "error"]
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote %s" % a.out)

    for key in ("disc_T12L1_mm", "disc_L1L2_mm"):
        v = np.array([r[key] for r in rows if isinstance(r.get(key), float)], float)
        if len(v):
            print("  %-14s n=%3d  median %.1f  IQR %.1f-%.1f mm"
                  % (key, len(v), np.median(v), np.percentile(v, 25), np.percentile(v, 75)))

    # THE CHECK: reproduce the release's own L1L2 with this code.
    ref = {}
    p = DATA / "degenerative.csv"
    if p.exists():
        for r in csv.DictReader(open(p)):
            try:
                ref[r["case"]] = float(r["disc_height_L1L2_mm"])
            except (TypeError, ValueError, KeyError):
                pass
    pairs = [(r["disc_L1L2_mm"], ref[r["case"]]) for r in rows
             if isinstance(r.get("disc_L1L2_mm"), float) and r["case"] in ref]
    if pairs:
        d = np.array([a_ - b for a_, b in pairs], float)
        print("\n  L1L2 against degenerative.csv on %d records:" % len(pairs))
        print("    identical %.1f%%   median difference %+.2f mm   max |difference| %.1f mm"
              % (100.0 * np.mean(d == 0), np.median(d), np.abs(d).max()))
        if np.abs(d).max() > 0.11:
            print("    WARNING: this is not the same measurement; do not use the T12L1 column")
    else:
        print("\n  no overlap with degenerative.csv: the L1L2 check did not run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
