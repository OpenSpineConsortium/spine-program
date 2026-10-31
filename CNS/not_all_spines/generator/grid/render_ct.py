"""The CT in each vertebra's frame at three heights through the body, the window ct_canal reads, with
the seed and the 150 and 200 HU contours: why the canal is or is not found. One PNG a study."""
import sys
import numpy as np
import nibabel as nib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scanimport import volume as V
from morphometry import measure as M
sys.path.insert(0, ".")
import cal

path, scheme, ctpath, out = sys.argv[1:5]
levels = sys.argv[5].split(",")
vol, grid, names, problems, _ = V.read_labels(path, scheme)
keep = {}
M.measure_volume(vol, grid, names, "x", pelvis=False, keep=keep)
img = nib.load(ctpath)
ct = np.asarray(img.dataobj, dtype=np.float32)
inv = np.linalg.inv(img.affine)
verts = keep["verts"]
levels = [l for l in levels if l in verts]
fig, axes = plt.subplots(len(levels), 3, figsize=(10, 3.3 * len(levels)), squeeze=False)
for r, lv in enumerate(levels):
    v = verts[lv]
    B = v.body_pts
    zb = (B[:, 2].min(), B[:, 2].max())
    xs = np.arange(v.midline - 22, v.midline + 22, cal.STEP)
    ys = np.arange(v.wall - 32, v.wall + 4, cal.STEP)
    for c, share in enumerate((0.3, 0.5, 0.7)):
        z = zb[0] + share * (zb[1] - zb[0])
        plane = cal.ct_plane(ct, inv, v.frame, z, xs, ys)
        ax = axes[r, c]
        ax.imshow(plane.T, origin="lower", extent=(xs[0], xs[-1], ys[0], ys[-1]), cmap="gray", vmin=-200, vmax=1000)
        ax.contour(xs, ys, plane.T, levels=[150, 200], colors=["y", "r"], linewidths=0.6)
        ax.plot([v.midline], [v.wall - 5], "c+")
        ax.axhline(v.wall, c="c", lw=0.4)
        ax.set_title("%s z %.0f%%" % (lv, 100 * share), fontsize=7)
        ax.tick_params(labelsize=6)
fig.tight_layout()
fig.savefig(out, dpi=80)
