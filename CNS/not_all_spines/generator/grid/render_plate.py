"""The top end-plate slab the engine reads EPWu from, in the vertebra's frame, for chosen levels:
the slab's points (x, y) coloured by height above the plate plane, the plain extent and the
depth-profile run at 0.5 marked. One PNG a study."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scanimport import volume as V
from scanimport import geometry as G
from morphometry import measure as M
from morphometry import anatomy as A
sys.path.insert(0, ".")
import cal

path, scheme, out = sys.argv[1:4]
levels = sys.argv[4].split(",")
vol, grid, names, problems, _ = V.read_labels(path, scheme)
keep = {}
M.measure_volume(vol, grid, names, "x", pelvis=False, keep=keep)
verts = keep["verts"]
levels = [l for l in levels if l in verts]
fig, axes = plt.subplots(2, len(levels), figsize=(3.2 * len(levels), 6.4), squeeze=False)
for c, lv in enumerate(levels):
    v = verts[lv]
    B = A.square_to_wall(v, v.body_pts)
    wall = v.wall_y0
    top, bot, fx, fy, fz = cal.slabs_of(G, B, wall, v.grid, v.frame)
    for r, slab in enumerate((top, bot)):
        ax = axes[r, c]
        ax.scatter(B[:, 0], B[:, 1], s=1, c="0.85")
        sc = ax.scatter(slab[:, 0], slab[:, 1], s=4, c=slab[:, 2] - slab[:, 2].min(), cmap="viridis")
        ext = G.extent(slab[:, 0], fx)
        pw = cal.profile_width(slab, wall, v.pixel, 0.5)
        ax.axhline(wall, c="k", lw=0.5)
        ax.set_title("%s %s ext %.1f prof50 %.1f" % (lv, "top" if r == 0 else "bottom", ext, pw), fontsize=7)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=6)
fig.tight_layout()
fig.savefig(out, dpi=90)
