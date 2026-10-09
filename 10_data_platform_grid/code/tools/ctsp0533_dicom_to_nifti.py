# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ctsp0533_dicom_to_nifti.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""DICOM series -> NIfTI with pydicom, as a fallback for dcm2niix.

The grid's compute nodes are glibc 2.17; the dcm2niix binaries published on GitHub need 2.29
and die with a link error that the caller can mistake for "the series is bad". conda-forge's
build is the first choice because the release used dcm2niix; this exists for when that route
is unavailable too.

Being a different converter is not a licence to be a different volume. Only the geometry
matters here, because the next step resamples onto the released label's grid and the check
that decides everything is how much of the label lands on bone:

  * slices sorted along the slice normal, not by InstanceNumber
  * the affine built exactly as nibabel's DICOM note specifies -- column 0 is the ROW
    direction (ImageOrientationPatient[3:6] x PixelSpacing[0]), column 1 the COLUMN
    direction, column 2 the measured first-to-last step divided by (n-1)
  * LPS -> RAS by negating the first two rows, which is the only reorientation in this file
  * RescaleSlope / RescaleIntercept applied, so the values are HU

It refuses a series with mixed geometry rather than silently averaging it away.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import nibabel as nib
import pydicom


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dicom-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tol", type=float, default=0.05,
                    help="mm of slice-spacing variation tolerated across the series")
    a = ap.parse_args()

    files = sorted(Path(a.dicom_dir).rglob("*.dcm"))
    if not files:
        print(f"  no DICOM under {a.dicom_dir}")
        return 2
    print(f"  {len(files)} DICOM files")

    # an NBIA zip carries a LICENSE beside the images; whatever is not a readable image slice is
    # counted and skipped rather than allowed to stop the conversion
    slices, skipped = [], []
    for f in files:
        try:
            d = pydicom.dcmread(str(f), stop_before_pixels=False)
        except Exception as e:                                          # noqa: BLE001
            skipped.append((f.name, type(e).__name__))
            continue
        if not hasattr(d, "ImagePositionPatient") or "PixelData" not in d:
            skipped.append((f.name, "no image data"))
            continue
        slices.append(d)
    if skipped:
        print(f"  skipped {len(skipped)} non-image file(s): {skipped[:5]}")
    if len(slices) < 2:
        print(f"  only {len(slices)} usable slices")
        return 2
    print(f"  {len(slices)} image slices")

    iop = np.asarray(slices[0].ImageOrientationPatient, dtype=float)
    rows_dir, cols_dir = iop[3:6], iop[0:3]          # increasing row index, increasing column index
    normal = np.cross(cols_dir, rows_dir)
    for d in slices:
        if not np.allclose(np.asarray(d.ImageOrientationPatient, dtype=float), iop, atol=1e-4):
            print("  series mixes orientations -- refusing")
            return 3

    slices.sort(key=lambda d: float(np.dot(np.asarray(d.ImagePositionPatient, dtype=float), normal)))
    pos = np.asarray([np.asarray(d.ImagePositionPatient, dtype=float) for d in slices])
    steps = np.linalg.norm(np.diff(pos, axis=0), axis=1)
    print(f"  slice step: median {np.median(steps):.4f} mm, min {steps.min():.4f}, max {steps.max():.4f}")
    if steps.max() - steps.min() > a.tol:
        print(f"  slice spacing varies by more than {a.tol} mm -- refusing; this is not a single "
              f"uniformly sampled reconstruction")
        return 4

    shapes = {(int(d.Rows), int(d.Columns)) for d in slices}
    if len(shapes) != 1:
        print(f"  slices disagree on in-plane size {shapes} -- refusing")
        return 3
    nr, nc = shapes.pop()

    vol = np.empty((nr, nc, len(slices)), dtype=np.float32)
    for k, d in enumerate(slices):
        arr = d.pixel_array.astype(np.float32)
        vol[:, :, k] = arr * float(getattr(d, "RescaleSlope", 1.0)) + float(getattr(d, "RescaleIntercept", 0.0))

    dr, dc = (float(x) for x in slices[0].PixelSpacing)     # [between rows, between columns]
    step = (pos[-1] - pos[0]) / (len(slices) - 1)
    aff = np.eye(4)
    aff[:3, 0] = rows_dir * dr
    aff[:3, 1] = cols_dir * dc
    aff[:3, 2] = step
    aff[:3, 3] = pos[0]
    aff[:2, :] *= -1.0                                      # LPS -> RAS

    img = nib.Nifti1Image(vol, aff)
    img.header.set_xyzt_units("mm")
    nib.save(img, a.out)
    print(f"  wrote {a.out}: shape {vol.shape}, axcodes {''.join(nib.aff2axcodes(aff))}, "
          f"HU range [{vol.min():.0f}, {vol.max():.0f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
