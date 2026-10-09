# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/render_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""render_0816.py -- look at the thing, in the three planes a radiologist would use.

Reorients to RAS for DISPLAY ONLY (nothing is written back), then renders axial, coronal and
sagittal slices through each large metal component: once on a bone window so the construct's
shape reads, and once with the metal outlined so its extent against the vertebra is obvious.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from scipy import ndimage

METAL_HU, GAP_MM, MIN_VOX = 2200.0, 6.0, 20

ci = nib.as_closest_canonical(nib.load("0816_ct.nii.gz"))   # display only
li = nib.as_closest_canonical(nib.load("0816_label.nii.gz"))
ct = np.asanyarray(ci.dataobj).astype(np.float32)
lab = np.asanyarray(li.dataobj).astype(np.int16)
sp = np.array(ci.header.get_zooms()[:3], float)
print("display axcodes:", nib.aff2axcodes(ci.affine), "zooms", sp.round(3))

hot = ct >= METAL_HU
it = max(1, int(round(GAP_MM / float(min(sp)))))
grouped, n = ndimage.label(ndimage.binary_dilation(hot, iterations=it))
cc = grouped * hot
sizes = [(int((cc == i).sum()), i) for i in range(1, n + 1)]
sizes = sorted([s for s in sizes if s[0] >= MIN_VOX], reverse=True)
print("components:", sizes)


def show(ax, img, mask, title, vmin=-150, vmax=1500):
    ax.imshow(img.T, cmap="gray", vmin=vmin, vmax=vmax, origin="lower", aspect="auto")
    if mask is not None and mask.any():
        ov = np.zeros((*mask.shape, 4))
        ov[mask.astype(bool)] = [1, 0, 0, 0.55]
        ax.imshow(np.transpose(ov, (1, 0, 2)), origin="lower", aspect="auto")
    ax.set_title(title, fontsize=8)
    ax.axis("off")


out = Path("renders")
out.mkdir(exist_ok=True)

for rank, (v, i) in enumerate(sizes[:2], 1):
    m = cc == i
    idx = np.argwhere(m)
    c = idx.mean(0).round().astype(int)
    lo, hi = idx.min(0), idx.max(0)
    print(f"comp {i}: {v} vox, centre voxel {c}, bbox {lo}-{hi}")

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    # axial (fix z), coronal (fix y), sagittal (fix x) in RAS display space
    show(axes[0, 0], ct[:, :, c[2]], None, f"axial z={c[2]} (bone window)")
    show(axes[1, 0], ct[:, :, c[2]], m[:, :, c[2]], "axial + metal")
    show(axes[0, 1], ct[:, c[1], :], None, f"coronal y={c[1]}")
    show(axes[1, 1], ct[:, c[1], :], m[:, c[1], :], "coronal + metal")
    show(axes[0, 2], ct[c[0], :, :], None, f"sagittal x={c[0]}")
    show(axes[1, 2], ct[c[0], :, :], m[c[0], :, :], "sagittal + metal")
    fig.suptitle(f"0816 component {i}: {v} voxels", fontsize=10)
    fig.tight_layout()
    p = out / f"comp{rank}_{i}.png"
    fig.savefig(p, dpi=110, bbox_inches="tight")
    plt.close(fig)
    print("  wrote", p)

# one wide view: coronal and sagittal maximum-intensity projection of all metal
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
allm = cc > 0
for k, (axis, name) in enumerate([(0, "sagittal MIP"), (1, "coronal MIP"), (2, "axial MIP")]):
    mip = ct.max(axis=axis)
    mm = allm.max(axis=axis)
    show(axes[k], mip, mm, f"{name} (all metal)", vmin=100, vmax=2000)
fig.suptitle("0816 -- every metal voxel, projected", fontsize=11)
fig.tight_layout()
fig.savefig(out / "mip_all.png", dpi=110, bbox_inches="tight")
print("  wrote", out / "mip_all.png")
