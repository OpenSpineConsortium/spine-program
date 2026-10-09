# spine-program/04_openspinetoolkit: copied 2026-10-08 (read on the grid 2026-10-09 00:12 UTC with `cat`, read-only).
# Source: grid HOME /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/pdw_why.py, dated 2026-09-10 16:00; in no repository. Hash of the file as read: sha256 0153b3cac21413459531d119fff528399abc2650a82ca47867a11897feb26619.
# The 2026-09-10 shard run of ostk per-level morphometry; see 04_openspinetoolkit/STATUS.md G.4 and results/grid_run_2026-09-10/README.md.
"""Where does ostk.morphometry.pedicle_widths bail on released volumes?"""
import sys
from pathlib import Path
import numpy as np, nibabel as nib
sys.path.insert(0, "/wsu/home/go/go24/go2432/ostk_run/OpenSpineToolkit")
from ostk.labels import labels_for
from ostk.vertebral_body import body_mask, canal_mask
from ostk import morphometry as M

lab_dir = Path(sys.argv[1])
for cs in sys.argv[2].split(","):
    f = lab_dir / f"{cs}_label.nii.gz"
    if not f.exists():
        continue
    img = nib.as_closest_canonical(nib.load(str(f)))
    lab = np.asanyarray(img.dataobj); aff = img.affine
    L = labels_for(lab)
    for lv in ("L1", "L5"):
        vert = lab == L[lv]
        if vert.sum() < 500:
            print(f"{cs} {lv}: no vertebra"); continue
        body = body_mask(vert, aff)
        canal = canal_mask(np.asarray(vert, bool), aff)
        sp = np.abs(np.asarray(aff, float)[:3, :3]).sum(axis=0)
        vfill = M._fill(np.asarray(vert, bool))
        idx = np.argwhere(vfill)
        lo = np.maximum(idx.min(0) - 6, 0)
        hi = np.minimum(idx.max(0) + 7, np.array(vfill.shape))
        V = M._resample_sdf(vfill, sp, (lo, hi), 0.35)
        C = M._resample_sdf(canal, sp, (lo, hi), 0.35) if canal is not None else None
        B = M._resample_sdf(M._fill(np.asarray(body, bool)), sp, (lo, hi), 0.35) if body is not None else None
        out = M.pedicle_widths(vert, body, aff)
        print(f"{cs} {lv}: body={'ok' if body is not None else 'NONE'} "
              f"canal={'ok' if canal is not None else 'NONE'} "
              f"V={'ok' if V is not None else 'NONE'} C={'ok' if C is not None else 'NONE'} "
              f"B={'ok' if B is not None else 'NONE'} "
              f"C.any={bool(C.any()) if C is not None else '-'} -> {out}")
