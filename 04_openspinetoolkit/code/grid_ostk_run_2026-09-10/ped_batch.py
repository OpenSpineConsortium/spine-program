# spine-program/04_openspinetoolkit: copied 2026-10-08 (read on the grid 2026-10-09 00:12 UTC with `cat`, read-only).
# Source: grid HOME /wsu/home/go/go24/go2432/ostk_run/ped_batch.py, dated 2026-09-10 06:02; in no repository. Hash of the file as read: sha256 6d3544a2647ca9a2c91a960def9f7f09b6e0da0a31e49c5d50e4b67892c4aab2.
# The 2026-09-10 shard run of ostk per-level morphometry; see 04_openspinetoolkit/STATUS.md G.4 and results/grid_run_2026-09-10/README.md.
"""PDW over many cases, against three independent published series."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, nibabel as nib
sys.path.insert(0, str(Path(__file__).resolve().parent / "OpenSpineToolkit"))
from ostk.vertebral_body import body_mask, canal_mask
from pedicle_dev import isthmus_width

LV = {20:"L1",21:"L2",22:"L3",23:"L4",24:"L5"}
REF = {
 "Panjabi 1992 (n=12, cadaver)":  {"L1":8.6,"L2":8.2,"L3":10.2,"L4":14.1,"L5":18.6},
 "Zindrick 1987 (cadaver)":       {"L1":8.7,"L2":8.9,"L3":10.3,"L4":12.9,"L5":18.0},
 "Yu 2015 (n=503, cadaver)":      {"L1":8.5,"L2":8.6,"L3":10.4,"L4":13.1,"L5":18.0},
 "Arockiaraj 2025 (n=300, CT)":   {"L1":5.8,"L2":6.3,"L3":8.1,"L4":9.8,"L5":13.6},
}

def main():
    lab_dir = Path(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv)>2 else 60
    acc = {}
    files = sorted(lab_dir.glob("*_label.nii.gz"))[:n]
    for i,f in enumerate(files,1):
        try:
            img = nib.as_closest_canonical(nib.load(str(f)))
            lab = np.asanyarray(img.dataobj); sp = np.asarray(img.header.get_zooms()[:3],float)
            for vid,name in LV.items():
                v = lab==vid
                if v.sum()<500: continue
                b = body_mask(v, img.affine)
                if b is None: continue
                w,_,_ = isthmus_width(v, b, sp, canal_mask(v, img.affine))
                for side in ("l","r"):
                    if side in w: acc.setdefault(name,[]).append(w[side])
        except Exception as exc:
            print(f"  {f.name}: {type(exc).__name__}: {exc}", flush=True)
        if i%10==0: print(f"  {i}/{len(files)}", flush=True)
    print(f"\n{'level':6s} {'n':>5s} {'median':>8s} {'p25':>7s} {'p75':>7s}  " +
          "  ".join(f"{k.split()[0]:>9s}" for k in REF))
    for name in LV.values():
        v = acc.get(name, [])
        if len(v)<10: continue
        a = np.array(v)
        cells = "  ".join(f"{REF[k][name]:9.1f}" for k in REF)
        print(f"{name:6s} {len(a):5d} {np.median(a):8.1f} {np.percentile(a,25):7.1f} "
              f"{np.percentile(a,75):7.1f}  {cells}")
    print("\ncolumns after p75 are published means for the same level.")

if __name__ == "__main__":
    main()
