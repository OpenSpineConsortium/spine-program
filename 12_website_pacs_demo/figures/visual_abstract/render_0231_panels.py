# spine-program copy 2026-10-08: from CTSpinoPelvic1K poster/render_0231_panels.py (untracked in that repository at head 7ddfe38),
# one laptop-path line replaced (marked 'spine-program edit'); the inputs it reads (case CTs and label revisions
# as .nii.gz) are imaging data and are not in this folder. Recorded in MANIFEST_LOCAL.md.
"""render_0231_panels.py -- the before/after rasters for the poster's middle column.

0231 is the case worth showing: the pseudolabeller split one rib bone across rib_left_8 and
rib_left_9, and called a rib on a LUMBAR vertebra rib_7. The blocking gate caught the first;
the student's correction fixed both, and the second turned into the finding -- ids 74/75,
rib_left_lumbar and rib_right_lumbar, the rib-side signature of transitional anatomy.

TWO THINGS THAT MUST NOT BE GOT WRONG, because both silently distort anatomy:

  The voxels are ANISOTROPIC -- 0.545 mm in plane, 0.8 mm through it. A coronal projection
  drawn one array-element to one pixel is stretched by 47% vertically. The projection is
  resampled to isotropic here, so a rib's angle on the poster is the rib's angle.

  Nothing downstream may rescale these anisotropically. They are written as plain rasters at
  their true proportion, and the poster script CROPS to fit a frame rather than squashing.
"""
from __future__ import annotations

from pathlib import Path

import imageio.v2 as iio
import json
import nibabel as nib
import numpy as np
from scipy import ndimage

SCHEME = Path("itksnap_v6_labels.txt")  # spine-program edit: was a laptop path; the descriptor is on the grid at /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/itksnap_v6_labels.txt (listed 2026-10-08); copy it beside this script
# frame: the lumbar ribs (x 162-377, z 338-402) plus the vertebrae below them
X0, X1 = 138, 402
Z0, Z1 = 268, 422
# the ribs sit anteriorly; project only that slab so the posterior elements do not
# paint over them
Y0, Y1 = 70, 190


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
ci = nib.as_closest_canonical(nib.load("0231_ct.nii.gz"))
ct = np.asanyarray(ci.dataobj).astype(np.float32)
sx, sy, sz = (float(v) for v in ci.header.get_zooms()[:3])
labs = {r: np.asanyarray(nib.as_closest_canonical(
    nib.load(f"0231_label_{r}.nii.gz")).dataobj).astype(np.int16) for r in ("v4", "v6")}
print("shape", ct.shape, "zooms", (round(sx, 3), round(sy, 3), round(sz, 3)))

Path("panels").mkdir(exist_ok=True)


MARKS = {}


def panel(rev, out_png):
    lab = labs[rev]
    sub_ct = ct[X0:X1, Y0:Y1, Z0:Z1]
    sub_lb = lab[X0:X1, Y0:Y1, Z0:Z1]

    mip = sub_ct.max(axis=1)                       # (x, z)
    rgb = np.stack([np.clip((mip - 180) / 1350, 0, 1)] * 3, axis=-1)

    for i in sorted(int(v) for v in np.unique(sub_lb) if v):
        m = (sub_lb == i).any(axis=1)
        if not m.any():
            continue
        c = COL.get(i, (1, 1, 1))
        a = 0.92 if i in (74, 75, 45, 57) else 0.38   # the ribs in question, loud
        for k in range(3):
            rgb[..., k][m] = (1 - a) * rgb[..., k][m] + a * c[k]

    # (x, z) -> display (row = z, col = x), then make pixels square in millimetres
    img = np.transpose(rgb, (1, 0, 2))[::-1]
    zoom_rows = sz / sx                              # 0.8 / 0.545 = 1.47
    # one resample does both jobs: square the pixels, and carry the 264-sample-wide
    # data up to a size a 48-inch poster can print without visible voxel steps.
    up = 5.0
    img = ndimage.zoom(img, (zoom_rows * up, up, 1.0), order=3)
    img = np.clip(img, 0, 1)

    # centroid of each rib-of-interest, in the FINAL raster's pixel frame
    marks = {}
    for i in (74, 75, 45, 57):
        m = (sub_lb == i).any(axis=1)
        if not m.any():
            continue
        proj = np.transpose(m)[::-1]                       # match the display transform
        proj = ndimage.zoom(proj.astype(float), (zoom_rows * up, up), order=0) > 0.5
        ys, xs = np.nonzero(proj)
        marks[str(i)] = {"cx": float(xs.mean()), "cy": float(ys.mean()),
                         "x0": int(xs.min()), "x1": int(xs.max()),
                         "y0": int(ys.min()), "y1": int(ys.max())}
    MARKS[rev] = marks

    iio.imwrite(out_png, (img * 255).astype(np.uint8))
    h, w = img.shape[:2]
    print(f"wrote {out_png}  {w}x{h}px  = {w*sx/up:.0f} x {h*sx/up:.0f} mm  aspect {w/h:.2f}")


panel("v4", "panels/0231_v4.png")
panel("v6", "panels/0231_v6.png")
Path("panels/markers.json").write_text(json.dumps(MARKS, indent=1))
print("markers:", json.dumps(MARKS, indent=1)[:600])
