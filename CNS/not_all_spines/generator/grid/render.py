"""Axial cuts of cervical and other vertebrae in the vertebra's frame: bone, body, canal and the holes
clip_to_foramina sees, at four heights through the body. One PNG a study.

    python render.py <mask> <scheme> <out.png> [levels]
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from scanimport import volume as V
from scanimport import geometry as G
from morphometry import measure as M
from morphometry import anatomy as A

path, scheme, out = sys.argv[1:4]
levels = sys.argv[4].split(",") if len(sys.argv) > 4 else ["C3", "C4", "C5", "C6", "C7", "L5"]
vol, grid, names, problems, _ = V.read_labels(path, scheme)
keep = {}
M.measure_volume(vol, grid, names, "x", pelvis=False, keep=keep)
verts = keep["verts"]
levels = [l for l in levels if l in verts]
fig, axes = plt.subplots(len(levels), 4, figsize=(12, 3 * len(levels)), squeeze=False)
for r, lv in enumerate(levels):
    v = verts[lv]
    loc = A.square_to_wall(v, v.loc)
    body = v.body
    zb = (loc[body, 2].min(), loc[body, 2].max())
    for c, share in enumerate((0.2, 0.4, 0.6, 0.8)):
        z = zb[0] + share * (zb[1] - zb[0])
        sel = np.abs(loc[:, 2] - z) <= 0.5 * v.fz
        ax = axes[r, c]
        xy = loc[sel, :2]
        if len(xy) < 5:
            continue
        g, origin = G.raster(xy, v.pixel)
        h = G.holes(g)
        lab, n = ndimage.label(h)
        ax.scatter(xy[:, 0], xy[:, 1], s=2, c=np.where(body[sel], "tab:blue", "0.6"))
        for k in range(1, n + 1):
            ij = np.argwhere(lab == k)
            pts = origin + (ij + 0.5) * v.pixel
            ax.scatter(pts[:, 0], pts[:, 1], s=2, c="tab:red")
        ax.axhline(v.wall_y0, lw=0.5, c="k")
        ax.set_title("%s z %.0f%% pix %.2f fz %.2f %s" % (lv, 100 * share, v.pixel, v.fz,
                     "fallback" if "body_foramina" in v.flags else "foramina"), fontsize=7)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=6)
fig.tight_layout()
fig.savefig(out, dpi=80)
