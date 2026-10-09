#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_relabel_from_poi.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Give a harvested SPINEPS vertebra mask its VERIDAH names back, from the centroid file SPINEPS wrote beside it.

WHY. benchmark/run_spineps_cases.py harvests "the last file whose name holds seg-vert" from SPINEPS's derivatives
tree. On the 2026-09-21 real-X-ray runs that file carried INSTANCE ids 1..N, while the <case>_ctd.json beside it
carried the labelled centroids in VerSe ids (L2-L5 = 21-24, sacrum 26 ...). tools/dual_seg_compare.py then read
instance ids as C1..C7 and reported every vertebra as a disagreement. The names exist; they were only detached.

HOW. The POI json's last element maps VerSe label -> {subregion: [x, y, z]} in VOXEL coordinates of the SOURCE
volume; its header gives that grid's RAS affine (origin, rotation, zoom). The harvested mask is on SPINEPS's own
cropped, resampled grid (its affine is right -- overlap with TotalSegmentator is Dice ~0.9 -- but its shape is not
the source's), so each centroid goes voxel -> RAS mm -> mask voxel. The instance at that voxel -- or, if the
centroid falls between voxels, the instance holding the most voxels within 3 voxels -- takes the label. A mapping
is accepted only if it is one-to-one and every instance's own centroid lies within 40 mm of its label's centroid (over 15 mm is flagged: a vertebra the CT cuts);
otherwise the case is reported and left unrelabelled. Every label's centroid is also written in LPS mm (the ITK /
SimpleITK world of the source NIfTI), because the sacrum (26) often has a centroid and no instance in this mask.

    python tools/spineps_relabel_from_poi.py --dir <spineps out> [--cases a,b,c]
    -> <case>_seg-vert_msk_veridah.nii.gz and relabel.json in the same directory
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def poi_labels(p):
    J = json.load(open(p))
    hdr, pts = J[0], J[-1]
    out = {}
    for lab, sub in pts.items():
        c = sub.get("50") or next(iter(sub.values()))
        out[int(lab)] = np.array(c, np.float64)
    return hdr, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--cases", default="")
    a = ap.parse_args()
    import nibabel as nib
    d = Path(a.dir)
    cases = a.cases.split(",") if a.cases else sorted(p.name[: -len("_seg-vert_msk.nii.gz")] for p in d.glob("*_seg-vert_msk.nii.gz"))
    report = {}
    for c in cases:
        vp = d / f"{c}_seg-vert_msk.nii.gz"; cp = d / f"{c}_ctd.json"
        img = nib.load(str(vp)); m = np.asarray(img.dataobj).astype(np.int32)
        hdr, P = poi_labels(cp)
        ids = [int(x) for x in np.unique(m) if x > 0]
        rec = dict(mask_ids=ids, poi_labels=sorted(P), poi_shape=hdr.get("shape"), mask_shape=list(m.shape))
        rot = np.array(hdr["rotation"], np.float64); zoom = np.array(hdr["zoom"], np.float64)
        A = np.eye(4); A[:3, :3] = rot * zoom[None, :]; A[:3, 3] = np.array(hdr["origin"], np.float64)
        Minv = np.linalg.inv(img.affine)
        world = {lab: (A @ np.r_[xyz, 1.0])[:3] for lab, xyz in P.items()}                 # RAS mm
        rec["poi_world_lps"] = {str(l): [round(float(-w[0]), 2), round(float(-w[1]), 2), round(float(w[2]), 2)] for l, w in world.items()}
        if set(ids) == set(P):
            rec["mapping"] = {str(i): [i] for i in ids}; rec["passthrough"] = True; rec["ok"] = True
            nib.save(nib.Nifti1Image(m.astype(np.int16), img.affine, img.header), str(d / f"{c}_seg-vert_msk_veridah.nii.gz"))
            report[c] = rec; print(c, "already VerSe ids", ids, flush=True); continue
        cen = {i: (img.affine @ np.r_[np.array(np.nonzero(m == i)).mean(1), 1.0])[:3] for i in ids}   # RAS mm
        mapping = {}; dist = {}
        for lab, w in world.items():
            xyz = (Minv @ np.r_[w, 1.0])[:3]
            ix = np.round(xyz).astype(int)
            if (ix < 0).any() or (ix >= np.array(m.shape)).any():
                continue
            inst = int(m[tuple(ix)])
            if inst == 0:
                lo = np.clip(ix - 3, 0, None); hi = np.minimum(ix + 4, m.shape)
                win = m[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
                v, n = np.unique(win[win > 0], return_counts=True)
                inst = int(v[np.argmax(n)]) if len(v) else 0
            if inst:
                mapping.setdefault(inst, []).append(lab)
                dist[lab] = float(np.linalg.norm(cen[inst] - w))
        ok = all(len(v) == 1 for v in mapping.values()) and all(x < 40 for x in dist.values())
        rec["far_over_15mm"] = [l for l, x in dist.items() if x >= 15]   # a CT-cut vertebra: body centroid vs its fragment
        rec.update(mapping={str(k): v for k, v in mapping.items()}, centroid_dist_mm={str(k): round(v, 2) for k, v in dist.items()},
                   unmatched_instances=[i for i in ids if i not in mapping], unmatched_labels=[l for l in P if l not in dist], ok=ok)
        if ok:
            out = np.zeros_like(m, np.int16)
            for inst, labs in mapping.items():
                out[m == inst] = labs[0]
            nib.save(nib.Nifti1Image(out, img.affine, img.header), str(d / f"{c}_seg-vert_msk_veridah.nii.gz"))
        report[c] = rec
        print(c, json.dumps(rec), flush=True)
    json.dump(report, open(d / "relabel.json", "w"), indent=1)
    print("wrote", d / "relabel.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
