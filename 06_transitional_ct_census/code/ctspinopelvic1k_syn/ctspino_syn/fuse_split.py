# copied into spine-program/06_transitional_ct_census on 2026-10-08 from CTSpinoPelvic1K-Syn (local git, no remote) ctspino_syn/fuse_split.py; commit 7098eb1 of 2026-06-11; this folder is the only copy. The banned word, where it occurred, is rewritten as origin.
"""
fuse_split.py — reproducibly re-partition a FUSED two-label region (e.g. an L6
fused to the sacrum, Castellvi III) into its two structures.

The L6<->sacrum boundary in fused bone is genuinely ambiguous, so hand-drawn
boundaries come out staggered and inconsistent. This computes a *deterministic*
boundary so every fused case is split the same way — and it is exactly the
instance-separation step the synth engine needs (separating a fused L6 from the
sacrum == separating fused instances).

Method (default, 'watershed' — the standard "split touching objects"):
  1. bone = (label==a) | (label==b)            the fused mass to partition
  2. seeds: the confident CORE of each structure (the part of each label that is
     >margin_mm from the other label — i.e. away from the fusion), or an
     explicit seed map (--seeds).
  3. D = distance transform of `bone`           high in body centres, low at the
                                                 bridge/neck
  4. watershed(-D, markers=seeds, mask=bone)    every bone voxel -> a or b,
     cutting at the constriction (the disc-level neck) and labelling sides by the
     seeds. Non-bone voxels keep their original label.

Fallback 'nearest' (scipy-only, no scikit-image): assign each bone voxel to the
nearest seed core by Euclidean distance — the *equidistant* boundary, i.e. the
symmetry plane between the two cores (the "use symmetry to draw it" idea, done
deterministically).

Voxel spacing is honoured, so the geometry is anisotropy-correct.

CLI:
  python -m ctspino_syn.fuse_split --label in.nii.gz --out clean.nii.gz --a 6 --b 7
  # then load clean.nii.gz in ITK-SNAP to inspect/accept the new boundary
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, Tuple

import numpy as np


def _has_skimage() -> bool:
    try:
        import skimage.segmentation  # noqa: F401
        return True
    except ImportError:
        return False


def _auto_cores(arr: np.ndarray, a: int, b: int, spacing, margin_mm: float):
    """Confident core of each label = the part of it that is >margin_mm from the
    other label (i.e. away from the fusion). Shrinks the margin if a core would
    be empty, falling back to the single most-interior voxel."""
    from scipy.ndimage import distance_transform_edt
    a_mask, b_mask = (arr == a), (arr == b)
    d_to_b = distance_transform_edt(~b_mask, sampling=spacing)
    d_to_a = distance_transform_edt(~a_mask, sampling=spacing)
    m = margin_mm
    while m > 0.5:
        core_a = a_mask & (d_to_b > m)
        core_b = b_mask & (d_to_a > m)
        if core_a.any() and core_b.any():
            return core_a, core_b, m
        m *= 0.5
    core_a = np.zeros_like(a_mask)
    core_b = np.zeros_like(b_mask)
    if a_mask.any():
        da = distance_transform_edt(a_mask, sampling=spacing)
        core_a[np.unravel_index(int(np.argmax(da)), da.shape)] = True
    if b_mask.any():
        db = distance_transform_edt(b_mask, sampling=spacing)
        core_b[np.unravel_index(int(np.argmax(db)), db.shape)] = True
    return core_a, core_b, m


def split_fused(arr: np.ndarray, a: int, b: int, spacing=(1.0, 1.0, 1.0),
                margin_mm: float = 5.0, method: str = "auto",
                core_a: Optional[np.ndarray] = None,
                core_b: Optional[np.ndarray] = None) -> Tuple[np.ndarray, dict]:
    """Return (new_label_array, stats). Only voxels in (arr==a)|(arr==b) are
    re-assigned; everything else is untouched."""
    from scipy.ndimage import distance_transform_edt
    arr = arr.astype(np.int32)
    bone = (arr == a) | (arr == b)
    if not bone.any():
        return arr.copy(), {"reassigned_a_to_b": 0, "reassigned_b_to_a": 0,
                            "method": "none", "note": "no a/b voxels"}

    if core_a is None or core_b is None:
        core_a, core_b, used_margin = _auto_cores(arr, a, b, spacing, margin_mm)
    else:
        used_margin = float("nan")

    if method == "auto":
        method = "watershed" if _has_skimage() else "nearest"

    if method == "watershed":
        from skimage.segmentation import watershed
        D = distance_transform_edt(bone, sampling=spacing)
        markers = np.zeros(arr.shape, np.int32)
        markers[core_a] = 1
        markers[core_b] = 2
        ws = watershed(-D, markers, mask=bone)
        assign_a = bone & (ws == 1)
        assign_b = bone & (ws == 2)
        # any bone voxel the watershed left at 0 (unreachable) -> nearest core
        leftover = bone & ~(assign_a | assign_b)
        if leftover.any():
            da = distance_transform_edt(~core_a, sampling=spacing)
            db = distance_transform_edt(~core_b, sampling=spacing)
            assign_a |= leftover & (da <= db)
            assign_b |= leftover & (da > db)
    elif method == "nearest":
        da = distance_transform_edt(~core_a, sampling=spacing)
        db = distance_transform_edt(~core_b, sampling=spacing)
        assign_a = bone & (da <= db)
        assign_b = bone & (da > db)
    else:
        raise ValueError(f"unknown method {method!r} (auto|watershed|nearest)")

    new = arr.copy()
    new[assign_a] = a
    new[assign_b] = b
    stats = {
        "method": method,
        "margin_mm": used_margin,
        "n_bone": int(bone.sum()),
        "reassigned_a_to_b": int(((arr == a) & assign_b).sum()),
        "reassigned_b_to_a": int(((arr == b) & assign_a).sum()),
    }
    return new, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True, type=Path, help="input label NIfTI")
    ap.add_argument("--out", required=True, type=Path, help="output label NIfTI")
    ap.add_argument("--a", type=int, default=6, help="first label (default 6 = L6)")
    ap.add_argument("--b", type=int, default=7, help="second label (default 7 = sacrum)")
    ap.add_argument("--seeds", type=Path, default=None,
                    help="optional seed NIfTI: voxels valued a/b override the "
                         "auto cores (paint a couple scribbles in ITK-SNAP)")
    ap.add_argument("--margin_mm", type=float, default=5.0,
                    help="auto-core distance from the other label (mm)")
    ap.add_argument("--method", choices=["auto", "watershed", "nearest"],
                    default="auto")
    args = ap.parse_args()

    import nibabel as nib
    img = nib.load(str(args.label))
    arr = np.asarray(img.dataobj)
    spacing = tuple(float(z) for z in img.header.get_zooms()[:3])

    core_a = core_b = None
    if args.seeds:
        seed = np.asarray(nib.load(str(args.seeds)).dataobj)
        core_a = (seed == args.a)
        core_b = (seed == args.b)
        if not core_a.any() or not core_b.any():
            raise SystemExit(f"--seeds must contain voxels valued {args.a} AND "
                             f"{args.b}")

    new, stats = split_fused(arr, args.a, args.b, spacing=spacing,
                             margin_mm=args.margin_mm, method=args.method,
                             core_a=core_a, core_b=core_b)

    out = nib.Nifti1Image(new.astype(np.uint8), img.affine, img.header)
    out.set_data_dtype(np.uint8)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    nib.save(out, str(args.out))

    print(f"method={stats['method']}  margin_mm={stats.get('margin_mm')}")
    print(f"fused bone voxels: {stats['n_bone']}")
    print(f"reassigned {args.a}->{args.b}: {stats['reassigned_a_to_b']}   "
          f"{args.b}->{args.a}: {stats['reassigned_b_to_a']}")
    print(f"wrote {args.out}  (load over the CT in ITK-SNAP to inspect)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
