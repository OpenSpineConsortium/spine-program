# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/look_native_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""look_native_0816.py -- the greyscale itself, no threshold, no overlay.

The earlier read came off a >=2200 HU mask, which shows only what saturates. If a plate spans
the anterior bodies at a lower attenuation -- or if the dense foci are screw heads on
something less opaque -- that mask cannot show it and neither could I. So this renders the
native image through the L3/L4 anterior region: a sagittal sweep left to right across the
front of the column, and axial slices through the disc, on two windows.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np

ci = nib.as_closest_canonical(nib.load("0816_ct.nii.gz"))
ct = np.asanyarray(ci.dataobj).astype(np.float32)
out = Path("renders")
out.mkdir(exist_ok=True)

# L3 z245-306, L4 z210-270 -> the L3/L4 disc sits near z~242
# anterior half of the bodies is y ~ 215-270; column spans x ~ 187-300
ZS = [228, 234, 240, 244, 248]
XS = [200, 211, 225, 240, 255, 269, 282]
Y0, Y1 = 200, 285          # anterior half of the bodies and just in front
Z0, Z1 = 195, 290          # L4 through L3
X0, X1 = 180, 305

def panel(ax, img, title, vmin, vmax):
    ax.imshow(img.T, cmap="gray", vmin=vmin, vmax=vmax, origin="lower", aspect="auto")
    ax.set_title(title, fontsize=7)
    ax.axis("off")

# --- sagittal sweep, bone window --------------------------------------------------
fig, axes = plt.subplots(2, len(XS), figsize=(3.0 * len(XS), 8))
for k, x in enumerate(XS):
    sag = ct[x, Y0:Y1, Z0:Z1]
    panel(axes[0, k], sag, f"sag x={x}  bone (300-1800)", 300, 1800)
    panel(axes[1, k], sag, f"sag x={x}  wide (-150-2500)", -150, 2500)
fig.suptitle("0816 sagittal sweep across the anterior L3/L4 region (anterior = up)", fontsize=10)
fig.tight_layout()
fig.savefig(out / "native_sag_sweep.png", dpi=115, bbox_inches="tight")
plt.close(fig)
print("wrote native_sag_sweep.png")

# --- axial series through the disc -------------------------------------------------
fig, axes = plt.subplots(2, len(ZS), figsize=(3.0 * len(ZS), 8))
for k, z in enumerate(ZS):
    ax_img = ct[X0:X1, Y0:Y1, z]
    panel(axes[0, k], ax_img, f"axial z={z}  bone", 300, 1800)
    panel(axes[1, k], ax_img, f"axial z={z}  wide", -150, 2500)
fig.suptitle("0816 axial through L3/L4 (anterior = up, right = image right)", fontsize=10)
fig.tight_layout()
fig.savefig(out / "native_ax_series.png", dpi=115, bbox_inches="tight")
plt.close(fig)
print("wrote native_ax_series.png")

# --- coronal sweep through the anterior bodies -------------------------------------
YS = [230, 242, 252, 260, 268]
fig, axes = plt.subplots(2, len(YS), figsize=(3.0 * len(YS), 8))
for k, y in enumerate(YS):
    cor = ct[X0:X1, y, Z0:Z1]
    panel(axes[0, k], cor, f"cor y={y}  bone", 300, 1800)
    panel(axes[1, k], cor, f"cor y={y}  wide", -150, 2500)
fig.suptitle("0816 coronal sweep, posterior->anterior through the bodies", fontsize=10)
fig.tight_layout()
fig.savefig(out / "native_cor_sweep.png", dpi=115, bbox_inches="tight")
print("wrote native_cor_sweep.png")
