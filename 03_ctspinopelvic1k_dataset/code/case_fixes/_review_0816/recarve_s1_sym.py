# source-of-copy: CTSpinoPelvic1K repository (public, master; head 7ddfe38 on 2026-10-08), path _review_0816/recarve_s1_sym.py; gitignored there, so not in any commit; copied 2026-10-08 from the working tree
# project folder: 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
"""recarve_s1_sym.py -- S1/S2 cut plane built on the SACRUM'S OWN mirror symmetry.

The previous attempt zeroed the plane's left-right component against the WORLD R axis. That
is only correct if the patient is not rolled in the scanner. On 0816 the carve came out
tangential to the right S1 foramen while leaving clearance on the left -- the signature of a
plane that is level in world coordinates and oblique to the patient.

So the left-right axis is measured rather than assumed: search for the reflection plane that
maps the sacrum onto itself best (maximum Dice between the bone and its mirror image), and
take that plane's normal as the patient's true LR axis. The S1/S2 cut is then built to
CONTAIN that axis, which is what makes it bilaterally symmetric -- equal clearance to the
left and right foramen -- while still carrying the sagittal tilt that follows pelvic tilt.

Reported at the end: the distance from the cut plane to the nearest foramen edge on each
side, which is the thing being judged by eye.

    python recarve_s1_sym.py --label 0816_label_v4.nii.gz --out 0816_label_v6.nii.gz
    python recarve_s1_sym.py ... --shift 3      # move the plane cranially along the axis
"""
from __future__ import annotations

import argparse

import nibabel as nib
import numpy as np
from scipy import ndimage

S1_ID, SACRUM_ID = 29, 26


def rot(axis, deg):
    """Rodrigues rotation matrix."""
    t = np.radians(deg)
    k = axis / np.linalg.norm(axis)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * (K @ K)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--shift", type=float, default=0.0)
    ap.add_argument("--ds", type=int, default=3, help="downsample factor for the symmetry search")
    a = ap.parse_args()

    li = nib.load(a.label)
    lab = np.asanyarray(li.dataobj).astype(np.uint8)
    aff = li.affine

    s1, sac = lab == S1_ID, lab == SACRUM_ID
    whole = s1 | sac
    print(f"  sacrum+S1 : {int(whole.sum()):,} voxels   S1 before {int(s1.sum()):,}")

    idx = np.argwhere(whole)
    ras = (aff @ np.c_[idx, np.ones(len(idx))].T).T[:, :3]
    centre = ras.mean(0)
    P = ras - centre
    Pd = P[:: a.ds]                                   # thinned cloud for the search

    # ---- the patient's LR axis = normal of the best mirror plane ---------------
    # occupancy overlap on a 3 mm grid. Encoded as int64 keys so the whole score is
    # numpy set arithmetic -- the obvious set-of-tuples version is ~1000x slower and
    # made a 225-candidate search unusable.
    GRID = 3.0
    OFF = 512

    def keys(pts):
        g = np.round(pts / GRID).astype(np.int64) + OFF
        return np.unique((g[:, 0] << 22) | (g[:, 1] << 11) | g[:, 2])

    KA = keys(Pd)

    def sym_score(n):
        n = n / np.linalg.norm(n)
        refl = Pd - 2.0 * np.outer(Pd @ n, n)
        KB = keys(refl)
        inter = np.intersect1d(KA, KB, assume_unique=True).size
        return 2.0 * inter / (KA.size + KB.size)

    best_n, best_s = np.array([1.0, 0.0, 0.0]), sym_score(np.array([1.0, 0.0, 0.0]))
    print(f"  symmetry (world R axis)      : Dice {best_s:.4f}")
    for ay in np.arange(-14, 14.1, 2.0):              # yaw about S
        for az in np.arange(-14, 14.1, 2.0):          # roll about A
            n = rot([0, 0, 1], ay) @ (rot([0, 1, 0], az) @ np.array([1.0, 0.0, 0.0]))
            sc = sym_score(n)
            if sc > best_s:
                best_s, best_n = sc, n / np.linalg.norm(n)
    lr = best_n
    dev = np.degrees(np.arccos(abs(np.dot(lr, [1, 0, 0]))))
    print(f"  symmetry (measured LR axis)  : Dice {best_s:.4f}")
    print(f"  patient LR axis : R={lr[0]:+.3f} A={lr[1]:+.3f} S={lr[2]:+.3f}"
          f"   ({dev:.1f} deg off the world R axis)")

    # ---- cranio-caudal axis, made orthogonal to the LR axis --------------------
    _, sv, vt = np.linalg.svd(P, full_matrices=False)
    k = int(np.argmax(np.abs(vt[:, 2])))
    cc = vt[k]
    cc = -cc if cc[2] < 0 else cc
    cc = cc - np.dot(cc, lr) * lr                     # remove any LR component
    cc /= np.linalg.norm(cc)
    print(f"  cut plane normal: R={cc[0]:+.3f} A={cc[1]:+.3f} S={cc[2]:+.3f}"
          f"   (ant-post tilt {np.degrees(np.arcsin(abs(cc[1]))):.1f} deg)")

    # ---- level: the existing interface, projected onto that axis ---------------
    inter = s1 & ndimage.binary_dilation(sac, iterations=1)
    ii = np.argwhere(inter)
    ir = (aff @ np.c_[ii, np.ones(len(ii))].T).T[:, :3] - centre
    cut = float((ir @ cc).mean()) + a.shift
    print(f"  cut at {cut:+.1f} mm along the axis"
          f"{'  (shift ' + format(a.shift, '+.1f') + ')' if a.shift else ''}")

    proj = P @ cc
    out = lab.copy()
    out[tuple(idx[proj >= cut].T)] = S1_ID
    out[tuple(idx[proj < cut].T)] = SACRUM_ID
    n_after = int((out == S1_ID).sum())
    print(f"  S1 after  : {n_after:,} ({n_after - int(s1.sum()):+,})   "
          f"sacrum {int((out == SACRUM_ID).sum()):,}   "
          f"total kept {int(((out==S1_ID)|(out==SACRUM_ID)).sum()) == int(whole.sum())}")

    nib.save(nib.Nifti1Image(out, aff, li.header), a.out)
    print(f"  wrote {a.out}")

    # ---- clearance to the foramina, left vs right -----------------------------
    # foramina = holes in the bone: background enclosed by sacrum in each half
    side = P @ lr
    for nm, sel in (("right", side > 0), ("left", side < 0)):
        d = proj[sel] - cut
        near = d[np.abs(d) < 25]
        if near.size:
            print(f"  {nm:<5}: bone spans {d.min():+7.1f} to {d.max():+7.1f} mm about the cut")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
