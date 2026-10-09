# spine-program copy 2026-10-08: from CTSpinoPelvic1K poster/render_0068_panels.py (untracked in that repository at head 7ddfe38),
# one laptop-path line replaced (marked 'spine-program edit'); the inputs it reads (case CTs and label revisions
# as .nii.gz) are imaging data and are not in this folder. Recorded in MANIFEST_LOCAL.md.
"""render_0068_panels.py -- the vertebra half of the poster's before/after.

0068 is the known body-mixing case. In v5 a single L1 label covered TWO vertebral bodies, so
every level beneath it was named one too high, and L3's mask had 19% of the bone sitting in a
stray blob of another class. class_mixing_qc says both out loud:

    X L1 covers TWO vertebral bodies (a duplicated / transitional level -- possible L6)
    X L3 is split into pieces (largest 80% of the bone) -> one bone must be ONE class

In v6 the column is renumbered L1-L6 against the twelfth rib, T10-T12 are added where the
scan images them, and all three spine checks pass. The check even predicted the answer:
"add L6 if there is a 6th lumbar" -- and v6 has one.

Sagittal, because a renumber is a story about the STACK: the same bones, differently named.
"""
from __future__ import annotations

import json
from pathlib import Path

import imageio.v2 as iio
import nibabel as nib
import numpy as np
from scipy import ndimage

SCHEME = Path("itksnap_v6_labels.txt")  # spine-program edit: was a laptop path; the descriptor is on the grid at /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt (listed 2026-10-08); copy it beside this script
# a para-sagittal slab through the bodies; the column sits at x 203-338
X0, X1 = 238, 306
Y0, Y1 = 88, 240          # anterior-posterior span of the bodies
Z0, Z1 = 300, 566          # L3 up through the T12 that v6 adds
UP = 4.0
HILITE = {20, 21, 22}     # L1 (two bodies in v5), L2, L3 (mixed in v5)


def load_colours():
    col = {}
    for line in SCHEME.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        if len(p) >= 4:
            col[int(p[0])] = (int(p[1]) / 255, int(p[2]) / 255, int(p[3]) / 255)
    return col


COL = load_colours()
ci = nib.as_closest_canonical(nib.load("0068_ct.nii.gz"))
ct = np.asanyarray(ci.dataobj).astype(np.float32)
sx, sy, sz = (float(v) for v in ci.header.get_zooms()[:3])
labs = {r: np.asanyarray(nib.as_closest_canonical(
    nib.load(f"0068_label_{r}.nii.gz")).dataobj).astype(np.int16) for r in ("v5", "v6")}
print("shape", ct.shape, "zooms", (round(sx, 3), round(sy, 3), round(sz, 3)))

Path("panels").mkdir(exist_ok=True)
MARKS = {}


def panel(rev, out_png):
    lab = labs[rev]
    sub_ct = ct[X0:X1, Y0:Y1, Z0:Z1]
    sub_lb = lab[X0:X1, Y0:Y1, Z0:Z1]

    mip = sub_ct.max(axis=0)                       # (y, z) -- sagittal
    rgb = np.stack([np.clip((mip - 170) / 1300, 0, 1)] * 3, axis=-1)

    for i in sorted(int(v) for v in np.unique(sub_lb) if v):
        m = (sub_lb == i).any(axis=0)
        if not m.any():
            continue
        c = COL.get(i, (1, 1, 1))
        a = 0.88 if i in HILITE else 0.40
        for k in range(3):
            rgb[..., k][m] = (1 - a) * rgb[..., k][m] + a * c[k]

    # (y, z) -> display rows = z (superior up), cols = y (anterior to the LEFT)
    img = np.transpose(rgb, (1, 0, 2))[::-1, ::-1]
    img = ndimage.zoom(img, (sz / sy * UP, UP, 1.0), order=3)
    img = np.clip(img, 0, 1)
    iio.imwrite(out_png, (img * 255).astype(np.uint8))

    marks = {}
    for i in HILITE:
        m = (sub_lb == i).any(axis=0)
        if not m.any():
            continue
        proj = np.transpose(m)[::-1, ::-1]
        proj = ndimage.zoom(proj.astype(float), (sz / sy * UP, UP), order=0) > 0.5
        ys, xs = np.nonzero(proj)
        marks[str(i)] = {"cx": float(xs.mean()), "cy": float(ys.mean()),
                         "x0": int(xs.min()), "x1": int(xs.max()),
                         "y0": int(ys.min()), "y1": int(ys.max())}
    MARKS[rev] = marks
    h, w = img.shape[:2]
    print(f"wrote {out_png}  {w}x{h}px  aspect {w/h:.2f}")


panel("v5", "panels/0068_v5.png")
panel("v6", "panels/0068_v6.png")
Path("panels/markers_0068.json").write_text(json.dumps(MARKS, indent=1))
print(json.dumps(MARKS, indent=1)[:400])
