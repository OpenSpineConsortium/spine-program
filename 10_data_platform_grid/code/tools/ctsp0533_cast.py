# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ctsp0533_cast.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Make a rebuilt CTSpinoPelvic1K CT the same KIND of file as the other 801.

fetch_from_tcia.py writes float32 because that is what scipy's resampler returns. Whether the
released volumes are float32 or int16 is a property of the release, not of the rebuild, so it
is read off the neighbouring released CTs rather than assumed. Integer targets are rounded,
not truncated. The affine is copied through untouched -- nothing here reorients a volume.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import nibabel as nib


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ct", required=True)
    ap.add_argument("--neighbours", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    dts = []
    for n in a.neighbours:
        p = Path(n)
        if p.exists():
            try:
                dts.append(np.dtype(nib.load(str(p)).get_data_dtype()))
            except Exception:                                           # noqa: BLE001
                pass
    if not dts:
        print("  no readable neighbour; leaving the rebuild as it is")
        return 3
    want = dts[0]
    if len({str(d) for d in dts}) > 1:
        print(f"  neighbours disagree on dtype {sorted({str(d) for d in dts})}; using {want}")

    img = nib.load(a.ct)
    have = np.dtype(img.get_data_dtype())
    print(f"  rebuilt dtype {have}, released neighbours {want}")
    if have == want:
        print("  already the released dtype; nothing to do")
        return 0

    data = np.asanyarray(img.dataobj)
    if np.issubdtype(want, np.integer):
        info = np.iinfo(want)
        data = np.clip(np.rint(np.asarray(data, dtype=np.float32)), info.min, info.max)
    out = nib.Nifti1Image(np.asarray(data, dtype=want), img.affine, img.header)
    out.set_data_dtype(want)
    out.header.set_slope_inter(None, None)
    nib.save(out, a.out)
    print(f"  wrote {a.out} as {want}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
