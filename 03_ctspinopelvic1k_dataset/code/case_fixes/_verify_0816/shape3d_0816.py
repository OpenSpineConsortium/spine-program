# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/shape3d_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""shape3d_0816.py -- render each metal object in 3D, to millimetre scale.

Slices keep hiding the answer because every one of these objects is a few millimetres across
and the plane never contains the whole of it. Shape is the discriminator: a ligature clip is
a short bent bar, a U or a V a few mm on a side; a pedicle or vertebral body screw is a
straight shank 25-50 mm long with a head; a plate is a flat slab with holes.

So each object is drawn on its own, at true scale, from three directions, with an explicit
millimetre box around it. Lower threshold than the census (1200 HU rather than 2200) so a
less opaque connecting element cannot hide -- if a plate joins these, it appears here.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from scipy import ndimage

LOW_HU = 1200.0        # deliberately well below the census threshold
ci = nib.as_closest_canonical(nib.load("0816_ct.nii.gz"))
li = nib.as_closest_canonical(nib.load("0816_label.nii.gz"))
ct = np.asanyarray(ci.dataobj).astype(np.float32)
lab = np.asanyarray(li.dataobj).astype(np.int16)
sp = np.array(ci.header.get_zooms()[:3], float)
out = Path("renders")
out.mkdir(exist_ok=True)

# restrict to the lumbar region so ribs and bowel do not clutter the picture
zs = np.argwhere((lab >= 22) & (lab <= 24))[:, 2]
z0, z1 = zs.min() - 15, zs.max() + 15
sub = ct[:, :, z0:z1]
sublab = lab[:, :, z0:z1]

hot = sub >= LOW_HU
# bone is also above 1200, so exclude anything the segmentation calls bone;
# what remains above 1200 and outside bone is either metal or dense calcium
hot_nonbone = hot & (sublab == 0) | (hot & (sublab == 255))
cc, n = ndimage.label(hot_nonbone)
sizes = sorted(((int((cc == i).sum()), i) for i in range(1, n + 1)), reverse=True)
sizes = [s for s in sizes if s[0] >= 25][:6]
print("objects (>=1200 HU, outside bone labels):", sizes)

fig = plt.figure(figsize=(16, 11))
for k, (v, i) in enumerate(sizes):
    m = cc == i
    idx = np.argwhere(m)
    pts = idx * sp                        # to millimetres
    pts = pts - pts.mean(0)
    hu = sub[m]
    for j, (elev, azim, nm) in enumerate([(0, 0, "from the front"),
                                          (0, 90, "from the side"),
                                          (90, 0, "from above")]):
        ax = fig.add_subplot(len(sizes), 3, k * 3 + j + 1, projection="3d")
        ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=hu, cmap="inferno",
                   s=14, vmin=1200, vmax=3071, depthshade=False)
        r = float(np.abs(pts).max()) + 1
        ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(f"obj {i}: {v} vox, {np.ptp(pts,0).round(1)} mm\n{nm}", fontsize=7)
        ax.tick_params(labelsize=5)
fig.suptitle(f"0816 -- every dense object outside bone, >= {LOW_HU:.0f} HU, true mm scale",
             fontsize=11)
fig.tight_layout()
fig.savefig(out / "shape3d.png", dpi=105, bbox_inches="tight")
print("wrote", out / "shape3d.png")
