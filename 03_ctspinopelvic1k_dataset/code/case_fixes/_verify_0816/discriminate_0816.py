# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/discriminate_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""discriminate_0816.py -- metal, or very dense calcium?

Two things separate them and neither is the HU threshold alone:

  Saturation. Surgical alloy drives the reconstruction to its ceiling over a solid core.
  Atherosclerotic calcium is dense but finite; it peaks in the high hundreds to ~1500 HU and
  only clips in flecks.

  Cross-section. An artery calcifies in its WALL, so a slice across it is a ring around a
  patent lumen. A screw or a plate is solid through the middle.

So this prints the HU distribution per component and, for the two large ones, walks along the
principal axis reporting whether each cross-section is filled or hollow.
"""
from __future__ import annotations

import nibabel as nib
import numpy as np
from scipy import ndimage

METAL_HU, GROUP_GAP_MM, MIN_VOX = 2200.0, 6.0, 20

ci = nib.load("0816_ct.nii.gz")
li = nib.load("0816_label.nii.gz")
ct = np.asanyarray(ci.dataobj).astype(np.float32)
lab = np.asanyarray(li.dataobj).astype(np.int16)
sp = np.array(ci.header.get_zooms()[:3], float)

hot = ct >= METAL_HU
it = max(1, int(round(GROUP_GAP_MM / float(min(sp)))))
grouped, n = ndimage.label(ndimage.binary_dilation(hot, iterations=it))
cc = grouped * hot

comps = []
for i in range(1, n + 1):
    m = cc == i
    if int(m.sum()) >= MIN_VOX:
        comps.append((int(m.sum()), i))
comps.sort(reverse=True)

print(f"{'comp':>5} {'vox':>6} {'mean':>7} {'p50':>7} {'p90':>7} {'max':>7} "
      f"{'>=3000':>7} {'>=3071':>7}")
for v, i in comps:
    m = cc == i
    vals = ct[m]
    print(f"{i:>5} {v:>6} {vals.mean():>7.0f} {np.percentile(vals,50):>7.0f} "
          f"{np.percentile(vals,90):>7.0f} {vals.max():>7.0f} "
          f"{int((vals>=3000).sum()):>7} {int((vals>=3071).sum()):>7}")

# --- hollow or solid, for the two biggest -------------------------------------------
print("\ncross-sections along each component's long axis")
print("(fill = metal voxels / voxels inside the section's convex hull)\n")
for v, i in comps[:2]:
    m = cc == i
    idx = np.argwhere(m)
    lo, hi = idx.min(0), idx.max(0)
    # long axis is superior-inferior for both: that is voxel axis 1 (I)
    ext = hi - lo
    ax = int(np.argmax(ext * sp))
    print(f"--- component {i}: {v} vox, slicing along voxel axis {ax} "
          f"(extent {ext[ax]*sp[ax]:.0f} mm) ---")
    fills, lumens = [], 0
    for s in range(lo[ax], hi[ax] + 1):
        sl = [slice(None)] * 3
        sl[ax] = s
        plane = m[tuple(sl)]
        k = int(plane.sum())
        if k < 8:
            continue
        filled = ndimage.binary_fill_holes(plane)
        hull = int(filled.sum())
        fill = k / max(hull, 1)
        fills.append(fill)
        if hull - k >= 6:      # a real enclosed lumen, not one stray hole
            lumens += 1
    if fills:
        print(f"    sections examined : {len(fills)}")
        print(f"    fill fraction     : median {np.median(fills):.2f}  "
              f"min {min(fills):.2f}  max {max(fills):.2f}")
        print(f"    sections with an enclosed lumen: {lumens}/{len(fills)}")
    print()

# --- what does the neighbourhood look like: bone, fat, vessel? -----------------------
print("mean HU in a 4 mm shell around each big component (context tissue)")
for v, i in comps[:2]:
    m = cc == i
    sh = ndimage.binary_dilation(m, iterations=6) & ~m
    sv = ct[sh]
    print(f"  comp {i}: shell mean {sv.mean():7.0f} HU | "
          f"<0 HU (fat/air) {100*np.mean(sv<0):5.1f}% | "
          f"0-150 (soft tissue) {100*np.mean((sv>=0)&(sv<150)):5.1f}% | "
          f">150 (bone/calc) {100*np.mean(sv>=150):5.1f}%")
