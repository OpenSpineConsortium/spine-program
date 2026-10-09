# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/test_grouping_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""Does grouping the fragments recover 0816, and at what gap?

Same thresholds as detect_metal.py, changing one thing: connected components are taken on a
DILATED copy of the hot mask, so pieces of one construct that the 2200 HU cut separated are
scored together. Volume is still counted on the undilated voxels.

Work is done inside each group's bounding box; dilating a 512x408x512 array seventeen times
per component is what made the honest version too slow to iterate on.
"""
from __future__ import annotations

from collections import Counter

import nibabel as nib
import numpy as np
from scipy import ndimage

METAL_HU, STREAK_HU, AIR_HU = 2200.0, -250.0, -800.0
MIN_VOX, CLIP_VOX = 20, 60
BONE_REACH_MM, IMPLANT_MM3 = 12.0, 300.0

li = nib.load("0816_label.nii.gz")
ci = nib.load("0816_ct.nii.gz")
lab = np.asanyarray(li.dataobj).astype(np.int16)
ct = np.asanyarray(ci.dataobj).astype(np.float32)
sp = np.array(li.header.get_zooms()[:3], float)
vox = float(np.prod(sp))
hot = ct >= METAL_HU


def crop(mask, pad):
    """Bounding box of mask, padded, clipped to the volume."""
    idx = np.argwhere(mask)
    lo = np.maximum(idx.min(0) - pad, 0)
    hi = np.minimum(idx.max(0) + pad + 1, mask.shape)
    return tuple(slice(a, b) for a, b in zip(lo, hi))


def score(group_mask):
    """(voxels, mm3, streak fraction, host label) for one construct."""
    reach = max(1, int(round(BONE_REACH_MM / float(min(sp)))))
    sl = crop(group_mask, reach + 4)
    m = group_mask[sl]
    ctc, labc = ct[sl], lab[sl]

    v = int(m.sum())
    sh = ndimage.binary_dilation(m, iterations=3) & ~m
    sv = ctc[sh]
    dark = float(np.mean((sv < STREAK_HU) & (sv > AIR_HU))) if sv.size else 0.0

    near = labc[ndimage.binary_dilation(m, iterations=reach)]
    near = near[(near > 0) & (near != 255)]
    host = int(Counter(near.tolist()).most_common(1)[0][0]) if near.size else 0
    return v, v * vox, dark, host


print(f"spacing {sp.round(3)}  vox {vox:.4f} mm3  hot voxels {int(hot.sum())}")
print(f"{'gap':>5} {'groups':>7} {'IMPLANT?':>9}   largest group (vox, mm3, dark, host)")
for gap_mm in (0, 2, 3, 4, 6):
    if gap_mm == 0:
        cc, n = ndimage.label(hot)
    else:
        it = max(1, int(round(gap_mm / float(min(sp)))))
        cc, n = ndimage.label(ndimage.binary_dilation(hot, iterations=it))
        cc = cc * hot  # keep only true metal voxels, grouped

    rows = []
    for i in range(1, n + 1):
        g = cc == i
        if int(g.sum()) < MIN_VOX:
            continue
        v, mm3, dark, host = score(g)
        ok = dark >= 0.15 and v >= CLIP_VOX and host > 0 and mm3 >= IMPLANT_MM3
        rows.append((v, round(mm3, 1), round(dark, 3), host, ok))
    rows.sort(reverse=True)
    hit = any(r[4] for r in rows)
    print(f"{gap_mm:>4}mm {len(rows):>7} {str(hit):>9}   {rows[0] if rows else '-'}")
