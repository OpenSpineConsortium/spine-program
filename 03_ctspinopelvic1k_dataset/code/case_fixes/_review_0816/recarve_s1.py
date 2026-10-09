# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _review_0816/recarve_s1.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""recarve_s1.py -- S1/S2 as a FLAT plane in the SACRUM'S OWN FRAME.

Three things are being distinguished here and it is worth keeping them apart:

  LEVEL   -- where along the bone the split sits.
  TILT    -- the plane's orientation. It SHOULD follow the sacral/pelvic axis, because S1's
             superior endplate is the landmark for sacral slope and pelvic incidence. A
             world-axial cut is wrong: it ignores pelvic tilt entirely.
  FLATNESS-- whether the boundary is a plane at all. The shipped carve takes S1 as
             (GT sacrum) INTERSECT (TotalSegmentator vertebrae_S1), so the boundary is the
             edge of a network's blob -- close to right, but irregular, and unstable between
             runs (190,451 voxels one run, 103,467 on an identical earlier one).

So: normal = the sacrum's own principal axis (the cranio-caudal one, chosen as the component
most aligned with superior-inferior, never assumed to be a voxel axis), and the cut is a true
plane through a chosen level. Tilt preserved, irregularity gone.

The sacrum and S1 are recombined before splitting, so the bone's OUTER boundary stays exactly
the radiologist's; only which side of one plane each voxel lies on changes.

NOTHING IS REORIENTED: written on its own grid with its own affine.

    python recarve_s1.py --label 0816_label_v4.nii.gz --out 0816_label_v5.nii.gz
    python recarve_s1.py ... --shift 4          # move the plane 4 mm cranially along the axis
"""
from __future__ import annotations

import argparse

import nibabel as nib
import numpy as np
from scipy import ndimage

S1_ID, SACRUM_ID = 29, 26


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shift", type=float, default=0.0,
                    help="mm to move the plane ALONG the sacral axis; + = cranial (smaller S1)")
    ap.add_argument("--keep_lateral_tilt", action="store_true",
                    help="do NOT zero the plane's left-right component. Off by default: the "
                         "sacrum is asymmetric, so its principal axis leans sideways by ~10 "
                         "deg, but the S1/S2 junction is symmetric about the midline and a "
                         "coronal obliquity there is an artefact of the bone's shape, not "
                         "anatomy.")
    a = ap.parse_args()

    li = nib.load(a.label)
    lab = np.asanyarray(li.dataobj).astype(np.uint8)
    aff = li.affine

    s1 = lab == S1_ID
    sac = lab == SACRUM_ID
    whole = s1 | sac
    print(f"  sacrum+S1 together : {int(whole.sum()):,} voxels")
    print(f"  S1 before          : {int(s1.sum()):,}")

    idx = np.argwhere(whole)
    ras = (aff @ np.c_[idx, np.ones(len(idx))].T).T[:, :3]
    centre = ras.mean(0)

    # the sacrum's own axes; take the one most aligned with superior-inferior as
    # cranio-caudal -- the bone is nearly as wide as it is tall, so PC1 is not
    # reliably the long axis and must not be assumed.
    _, sv, vt = np.linalg.svd(ras - centre, full_matrices=False)
    k = int(np.argmax(np.abs(vt[:, 2])))
    axis = vt[k]
    if axis[2] < 0:
        axis = -axis
    if not a.keep_lateral_tilt:
        lat = np.degrees(np.arcsin(abs(axis[0])))
        axis = np.array([0.0, axis[1], axis[2]])
        axis /= np.linalg.norm(axis)
        print(f"  lateral tilt       : {lat:.1f} deg removed (sagittal-plane normal)")
    print(f"  sacral axes (var)  : {np.round(sv / sv.sum(), 3)}   using component {k}")
    print(f"  cut plane normal   : R={axis[0]:+.3f} A={axis[1]:+.3f} S={axis[2]:+.3f}")
    print(f"    -> lateral tilt {np.degrees(np.arcsin(abs(axis[0]))):.1f} deg, "
          f"ant-post tilt {np.degrees(np.arcsin(abs(axis[1]))):.1f} deg")

    # level: the existing interface centroid, projected onto that axis
    inter = s1 & ndimage.binary_dilation(sac, iterations=1)
    ii = np.argwhere(inter)
    ir = (aff @ np.c_[ii, np.ones(len(ii))].T).T[:, :3]
    cut = float((ir - centre) @ axis) if False else float(((ir - centre) @ axis).mean())
    cut += a.shift
    print(f"  cut at             : {cut:+.1f} mm along the axis from the bone centroid"
          f"{'  (shifted ' + format(a.shift, '+.1f') + ' mm)' if a.shift else ''}")

    proj = (ras - centre) @ axis
    out = lab.copy()
    out[tuple(idx[proj >= cut].T)] = S1_ID
    out[tuple(idx[proj < cut].T)] = SACRUM_ID

    n_after = int((out == S1_ID).sum())
    print(f"  S1 after           : {n_after:,}  ({n_after - int(s1.sum()):+,})")
    print(f"  sacrum after       : {int((out == SACRUM_ID).sum()):,}")
    print(f"  bone total kept    : "
          f"{int(((out == S1_ID) | (out == SACRUM_ID)).sum()) == int(whole.sum())}")

    img = nib.Nifti1Image(out, aff, li.header)
    img.set_data_dtype(np.uint8)
    nib.save(img, a.out)
    print(f"  wrote {a.out}")

    # verify the new boundary is planar and carries the intended tilt
    ns1, nsac = out == S1_ID, out == SACRUM_ID
    ni = np.argwhere(ns1 & ndimage.binary_dilation(nsac, iterations=1))
    nr = (aff @ np.c_[ni, np.ones(len(ni))].T).T[:, :3]
    _, ns, nvt = np.linalg.svd(nr - nr.mean(0), full_matrices=False)
    n = nvt[2]
    n = -n if n[2] < 0 else n
    print(f"  achieved normal    : R={n[0]:+.3f} A={n[1]:+.3f} S={n[2]:+.3f}")
    print(f"  planarity (3rd sv) : {ns[2] / ns.sum():.4f}   (0 = perfectly flat)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
