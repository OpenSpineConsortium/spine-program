# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _verify_0816/fragments_0816.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""fragments_0816.py -- discrete objects, or one connected device?

This decides two different questions at once.

Clinically: a chain of small separate radiodense objects strung along a vessel is surgical
clips; one continuous piece spanning levels is an implant.

For the detector: if these are clips, then grouping at 6 mm manufactured a 61 mm "construct"
out of unrelated objects, and the fix that recovers this case is also a way to invent
implants that are not there. Either way the answer has to come from the fragment geometry,
not from the grouped blob.

Reports each un-grouped fragment in RAS mm, its size, its side, its nearest neighbour, and
which vertebral level it sits beside.
"""
from __future__ import annotations

import nibabel as nib
import numpy as np
from scipy import ndimage

METAL_HU, MIN_FRAG = 2200.0, 8
BODIES = {18: "T11", 19: "T12", 20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5"}

ci = nib.load("0816_ct.nii.gz")
li = nib.load("0816_label.nii.gz")
ct = np.asanyarray(ci.dataobj).astype(np.float32)
lab = np.asanyarray(li.dataobj).astype(np.int16)
aff, sp = ci.affine, np.array(ci.header.get_zooms()[:3], float)
vox = float(np.prod(sp))


def ras(idx):
    return (aff @ np.c_[idx, np.ones(len(idx))].T).T[:, :3]


# level midplanes, to say which level a fragment lies beside
lev = {}
for lid, nm in BODIES.items():
    m = lab == lid
    if m.sum() > 500:
        lev[nm] = ras(np.argwhere(m)).mean(0)

hot = ct >= METAL_HU
cc, n = ndimage.label(hot)
frags = []
for i in range(1, n + 1):
    m = cc == i
    v = int(m.sum())
    if v < MIN_FRAG:
        continue
    idx = np.argwhere(m)
    r = ras(idx)
    c = r.mean(0)
    ext = r.max(0) - r.min(0)
    vals = ct[m]
    # nearest labelled level
    best = min(lev, key=lambda k: np.linalg.norm(c - lev[k])) if lev else "?"
    rel = c - lev[best] if lev else np.zeros(3)
    frags.append({"vox": v, "mm3": v * vox, "c": c, "ext": ext, "best": best, "rel": rel,
                  "sat": float((vals >= 3071).mean())})

frags.sort(key=lambda f: -f["c"][2])   # superior -> inferior

print(f"{len(frags)} fragments >= {MIN_FRAG} voxels at {METAL_HU:.0f} HU\n")
print(f"{'mm3':>7} {'side':>5} {'level':>6} {'A-off':>7} {'R-off':>7} "
      f"{'size R x A x S (mm)':>22} {'sat%':>5}")
for f in frags:
    side = "L" if f["c"][0] < 0 else "R"
    e = f["ext"]
    print(f"{f['mm3']:>7.1f} {side:>5} {f['best']:>6} {f['rel'][1]:>+7.1f} "
          f"{f['rel'][0]:>+7.1f} {e[0]:>6.1f} x{e[1]:>6.1f} x{e[2]:>6.1f}   "
          f"{100*f['sat']:>4.0f}")

# nearest-neighbour spacing: clips sit apart, a device is continuous
print("\nnearest-neighbour centroid distance per fragment (mm):")
C = np.array([f["c"] for f in frags])
for i, f in enumerate(frags):
    d = np.linalg.norm(C - C[i], axis=1)
    d[i] = 1e9
    j = int(np.argmin(d))
    print(f"   {f['mm3']:>6.1f} mm3 at {f['best']:>4}  ->  {d[j]:6.1f} mm to a "
          f"{frags[j]['mm3']:.1f} mm3 fragment")

# gap between the actual metal surfaces of the two biggest, not their centres
if len(frags) >= 2:
    print("\nsurface-to-surface gaps among the six largest fragments (mm):")
    big = sorted(frags, key=lambda f: -f["mm3"])[:6]
    pts = []
    for f in big:
        pass
    for a in range(len(big)):
        for b in range(a + 1, len(big)):
            d = np.linalg.norm(big[a]["c"] - big[b]["c"])
            # subtract half-extents along the connecting direction, a rough surface gap
            u = (big[b]["c"] - big[a]["c"]) / max(d, 1e-9)
            ra = float(np.abs(big[a]["ext"] / 2 @ np.abs(u)))
            rb = float(np.abs(big[b]["ext"] / 2 @ np.abs(u)))
            print(f"   {big[a]['mm3']:>6.1f} <-> {big[b]['mm3']:>6.1f} : "
                  f"centres {d:6.1f}, approx surface gap {max(d - ra - rb, 0):6.1f}")
