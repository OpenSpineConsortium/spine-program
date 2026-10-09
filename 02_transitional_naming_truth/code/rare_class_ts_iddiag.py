#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_ts_iddiag.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Diagnose the scrambled level names in the rare-class TS renders.

The previews show boxes tiling consecutive vertebral bodies whose NAMES are non-monotonic
(T12 above L2 above L1 above T10). load_case pairs name<->mask by id, so the only way that
happens is if the mask ids themselves sit at scrambled S-I positions. For every staged mask
(ts_stage/TS_*/TS_*_msk.nii.gz) and its SOURCE (~/bench_ts/spineps/native/*_seg-vert_msk.nii.gz),
print each id's centroid along the world S-I axis (from the affine, no reorientation assumptions),
sorted superior->inferior, with the VerSe name the renderer would assign.
"""
import json, sys, glob, os
import numpy as np
import nibabel as nib

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "SAC", 28: "T13"}

def si_order(path):
    img = nib.load(path)
    arr = np.asanyarray(img.dataobj).astype(np.int16)
    A = img.affine
    out = []
    for lid in [int(x) for x in np.unique(arr) if x]:
        idx = np.argwhere(arr == lid)
        c = idx.mean(axis=0)
        world = A[:3, :3] @ c + A[:3, 3]
        out.append((float(world[2]), lid, VERSE.get(lid, f"id{lid}"), int(len(idx))))
    out.sort(key=lambda t: -t[0])   # superior (larger S in RAS-world z) first
    return out

def main():
    report = {}
    for stage in sorted(glob.glob(os.path.expanduser("~/") + "../../rs/rs_grp_oschome/go2432/data/rare_class/ts_stage/TS_*/")):
        pass
    stages = sorted(glob.glob("/rs/rs_grp_oschome/go2432/data/rare_class/ts_stage/TS_*"))
    for d in stages:
        cid = os.path.basename(d)
        mp = os.path.join(d, f"{cid}_msk.nii.gz")
        if not os.path.exists(mp):
            continue
        rows = si_order(mp)
        names = [n for _, _, n, _ in rows]
        ids = [i for _, i, _, _ in rows]
        mono = all(ids[k] < ids[k+1] for k in range(len(ids)-1) if ids[k] != 26 and ids[k+1] != 26)
        print(f"{cid} staged  monotonic={mono}")
        for z, lid, n, px in rows:
            print(f"   z={z:8.1f}  id={lid:2d}  {n:4s}  vox={px}")
        report[cid] = {"staged_ids_sup_to_inf": ids, "names": names, "monotonic": mono}
    # one source mask for comparison
    src = os.path.expanduser("~/bench_ts/spineps/native/TS_s0224_seg-vert_msk.nii.gz")
    if os.path.exists(src):
        rows = si_order(src)
        print("SOURCE TS_s0224:")
        for z, lid, n, px in rows:
            print(f"   z={z:8.1f}  id={lid:2d}  {n:4s}  vox={px}")
        report["SOURCE_TS_s0224"] = {"ids_sup_to_inf": [r[1] for r in rows]}
    out = "/rs/rs_grp_oschome/go2432/data/rare_class/ts_iddiag.json"
    json.dump(report, open(out, "w"), indent=1)
    print("wrote", out)

if __name__ == "__main__":
    main()
