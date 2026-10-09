# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/analyse_0816_hardware.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""analyse_0816_hardware.py -- what device is this, measured rather than eyeballed.

Reports every metal component in anatomical (RAS) millimetres, not voxels: where it sits
relative to each vertebral body centroid, which way it points, how long and how thick it is.
A screw is a long thin rod pointing INTO a body; a plate is a flat slab lying ON the front
or side of one. Those are separable by shape and position, so the measurement can name the
construct instead of the reader guessing from a slice.

The volume is PIR, so anterior is -axis0, superior is -axis1, left is -axis2. Everything
below goes through the affine rather than assuming any of that.
"""
from __future__ import annotations

from collections import Counter

import nibabel as nib
import numpy as np
from scipy import ndimage

METAL_HU = 2200.0
GROUP_GAP_MM = 6.0
MIN_VOX = 20
BODIES = {22: "L3", 23: "L4", 24: "L5", 21: "L2", 20: "L1", 19: "T12", 18: "T11"}

ci = nib.load("0816_ct.nii.gz")
li = nib.load("0816_label.nii.gz")
ct = np.asanyarray(ci.dataobj).astype(np.float32)
lab = np.asanyarray(li.dataobj).astype(np.int16)
aff = ci.affine
sp = np.array(ci.header.get_zooms()[:3], float)


def to_ras(vox_idx: np.ndarray) -> np.ndarray:
    """(N,3) voxel indices -> (N,3) RAS millimetres."""
    h = np.c_[vox_idx, np.ones(len(vox_idx))]
    return (aff @ h.T).T[:, :3]


def describe(mask):
    """Volume, RAS centroid, principal direction, length and thickness of a component."""
    idx = np.argwhere(mask)
    ras = to_ras(idx)
    c = ras.mean(0)
    x = ras - c
    # principal axis = first right singular vector
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    axis = vt[0]
    proj = x @ axis
    length = float(proj.max() - proj.min())
    # thickness: spread perpendicular to the principal axis, as a full width
    perp = x - np.outer(proj, axis)
    r = np.linalg.norm(perp, axis=1)
    thick = float(2 * np.percentile(r, 90))
    # flatness: is the perpendicular spread itself one-sided (a slab) or round (a rod)?
    sv = s / max(s.sum(), 1e-9)
    return {
        "vox": int(mask.sum()),
        "mm3": float(mask.sum() * np.prod(sp)),
        "centroid_ras": c,
        "axis": axis,
        "length_mm": length,
        "thick_mm": thick,
        "sv": sv,
    }


# vertebral body centroids, in RAS
body_c = {}
for lid, name in BODIES.items():
    m = lab == lid
    if m.sum() > 500:
        body_c[name] = to_ras(np.argwhere(m)).mean(0)

print("vertebral body centroids (RAS mm):")
for k, v in body_c.items():
    print(f"   {k:>4}  R={v[0]:8.1f}  A={v[1]:8.1f}  S={v[2]:8.1f}")

hot = ct >= METAL_HU
gap_it = max(1, int(round(GROUP_GAP_MM / float(min(sp)))))
grouped, n = ndimage.label(ndimage.binary_dilation(hot, iterations=gap_it))
cc = grouped * hot

print(f"\n{int(hot.sum())} metal voxels, {n} construct group(s) at {GROUP_GAP_MM:g} mm\n")

rows = []
for i in range(1, n + 1):
    m = cc == i
    if int(m.sum()) < MIN_VOX:
        continue
    d = describe(m)

    # nearest vertebral body, and where this sits relative to it
    best, bd = None, 1e9
    for name, bc in body_c.items():
        dist = float(np.linalg.norm(d["centroid_ras"] - bc))
        if dist < bd:
            best, bd = name, dist
    rel = d["centroid_ras"] - body_c[best]

    # is it inside a body label, and which
    inside = Counter(lab[m].tolist())
    inside_named = {BODIES.get(k, str(k)): v for k, v in inside.most_common(4)}

    ax = d["axis"]
    rows.append((d, best, bd, rel, inside_named, ax))

rows.sort(key=lambda r: -r[0]["mm3"])
for d, best, bd, rel, inside_named, ax in rows:
    print(f"--- component {d['mm3']:7.1f} mm3 ({d['vox']} vox) ---")
    print(f"    nearest body      : {best}  (centre {bd:.1f} mm away)")
    print(f"    offset from {best:>3}   : R{rel[0]:+7.1f}  A{rel[1]:+7.1f}  S{rel[2]:+7.1f}  mm")
    print(f"    length x thickness: {d['length_mm']:6.1f} x {d['thick_mm']:5.1f} mm"
          f"   (aspect {d['length_mm'] / max(d['thick_mm'], 1e-6):.1f})")
    print(f"    principal axis    : R{ax[0]:+.2f} A{ax[1]:+.2f} S{ax[2]:+.2f}")
    print(f"    singular values   : {np.round(d['sv'], 3)}")
    print(f"    voxels lie in     : {inside_named}")
    print()
