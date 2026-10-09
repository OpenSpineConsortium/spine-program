#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_ts_fixids.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Repair the scrambled instance ids in a staged bench_ts SPINEPS seg-vert mask from its ctd POI file.

Found 2026-09-23: the ~/bench_ts/spineps/native/*_seg-vert_msk.nii.gz files carry vertebra INSTANCES at
correct spatial positions (the boxes sit on bodies) but under ids that are spatially scrambled -- id 25
can sit anywhere in the column, so "id 25 present" never meant L6. The VERIDAH naming that is actually
ordered and trustworthy is the ctd POI json (label -> corpus point "50" on the SPINEPS RAS grid), which
names C2..L5/L6 (+26 sacrum, +28 T13); C1 is never named there. Per the ctd, of the 12 "L6" cases only
s1089 and s1178 are L6; s0616, s1088, s1123 are T13; the other 7 are normal spines.

Method: instances sorted by world S-I centroid; POIs sorted the same; if there is exactly one extra
instance and it sits above the C2 POI it is C1; then 1:1 rank alignment, each pair within a z tolerance
(25 mm, 45 mm for the sacrum, whose POI is not a centroid). Output ids are VerSe (C1=1..L6=25, sacrum=26,
T13=28), spatially monotonic by construction; anything else fails loudly rather than render a wrong label.

SUPERSEDED for whole trees by tools/spineps_ids.py relabel (position binding AND this z-rank, refusing unless they
agree; checked 280/280 against this tool's output on the 12). Kept for the staged rcts2 masks on the CT grid. Since
2026-09-23 it writes no sacrum (the raw mask has none; see the SACRUM note in main) and its output must pass the
shared id guard (tools/spineps_ids.check_ids, zero ctd disagreements) or nothing is written.
"""
import argparse, json, os, sys
import numpy as np
import nibabel as nib

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "SAC", 28: "T13"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", required=True, help="staged mask on the CT grid (relabelled in place)")
    ap.add_argument("--ctd", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--report", required=True, help="subtype_fix.json out")
    a = ap.parse_args()

    d = json.load(open(a.ctd))
    meta = d[0]
    pois = d[-1]
    zoom = np.asarray(meta["zoom"], float)
    origin = np.asarray(meta["origin"], float)
    rot = np.asarray(meta["rotation"], float)
    assert meta["direction"] == ["R", "A", "S"], f"ctd direction {meta['direction']}"
    poi_world = {}
    for k, v in pois.items():
        c = np.asarray(v["50"], float)
        poi_world[int(k)] = rot @ (c * zoom) + origin

    img = nib.load(a.staged)
    arr = np.asanyarray(img.dataobj).astype(np.int16)
    A = img.affine
    inst = []
    for lid in (int(x) for x in np.unique(arr) if x):
        idx = np.argwhere(arr == lid)
        w = A[:3, :3] @ idx.mean(axis=0) + A[:3, 3]
        inst.append((float(w[2]), lid, int(len(idx))))
    inst.sort(key=lambda t: -t[0])                       # superior first
    plist = sorted(poi_world.items(), key=lambda kv: -kv[1][2])

    mapping = {}
    extra_c1 = None
    sacrum_poi_dropped = False
    # VERIDAH's ctd never names C1; the mask may or may not carry a sacrum instance. So: if the topmost
    # instance sits clearly above the topmost POI (C2), it is C1; and if the counts then leave exactly one
    # POI over and that POI is the sacrum, the mask simply has no sacrum instance (seen in the four
    # cases whose 1:1 alignment drifted by one vertebral height: C1<->C2, C2<->C3, ... failing mid-thorax).
    inst_rest = inst
    top_z = inst[0][0]
    c2_z = poi_world.get(2, [None, None, -1e9])[2]
    if top_z > c2_z + 8.0:
        extra_c1 = inst[0]
        mapping[inst[0][1]] = 1
        inst_rest = inst[1:]
    if len(inst_rest) == len(plist) - 1 and plist[-1][0] == 26:
        plist = plist[:-1]
        sacrum_poi_dropped = True
    if len(inst_rest) != len(plist):
        raise SystemExit(f"{a.case}: {len(inst_rest)} instances vs {len(plist)} POIs after C1/sacrum handling -- no safe alignment")

    pairs = []
    for (zi, lid, vox), (plab, pw) in zip(inst_rest, plist):
        tol = 45.0 if plab == 26 else 25.0
        dz = abs(zi - pw[2])
        assert dz <= tol, f"{a.case}: instance id {lid} z={zi:.1f} vs POI {VERSE.get(plab,plab)} z={pw[2]:.1f} (|dz|={dz:.1f} > {tol})"
        mapping[lid] = plab
        pairs.append({"old_id": lid, "new_id": plab, "name": VERSE.get(plab, str(plab)), "z_mm": round(zi, 1), "dz_mm": round(dz, 1), "vox": vox})

    # THE SACRUM (2026-09-23, SchwingNet/results/spineps_ids/TS12_VERIFY.md, IMPACT.md): the raw bench_ts instance
    # masks hold NO sacrum. The instance this rank match paired with the ctd S point was a 380-684-voxel fragment
    # (s0790, s1124, s1350) or an S1-sized piece 24-29 mm above the point (s0224, s1304, s1380), and a render drew
    # the "sacrum" box on it. The staged mask has no semantic sacrum to confirm one, so 26 is no longer written
    # (the same rule as tools/spineps_ids.relabel_by_ctd); the instance is dropped and reported.
    sacrum_dropped = [p for p in pairs if p["new_id"] == 26]
    for p in sacrum_dropped:
        mapping[p["old_id"]] = 0
        p["new_id"], p["name"] = 0, "dropped (not the sacrum: no semantic sacrum in a raw mask)"

    # relabel through a lookup so no in-place collisions
    lut = np.zeros(int(arr.max()) + 1, np.int16)
    for old, new in mapping.items():
        lut[old] = new
    out = lut[arr]
    # the result must read as VerSe names against the ctd (tools/spineps_ids.py, the shared guard): zero disagreements
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from spineps_ids import check_ids
    chk = check_ids((out, A), {k: v for k, v in poi_world.items() if k != 26})
    if chk["verdict"] != "verse_ok" or chk["ctd_disagree"]:
        raise SystemExit(f"{a.case}: relabelled mask fails the id guard: {chk['verdict']} {chk['reasons']}")
    nib.save(nib.Nifti1Image(out, img.affine, img.header), a.staged)

    labels = sorted(v for v in mapping.values() if v)
    subtype = "L6" if 25 in labels else ("T13" if 28 in labels else "none")
    rep = {
        "case": a.case,
        "subtype": subtype,
        "subtype_source": "VERIDAH ctd naming (seg-vert instance ids were spatially scrambled; repaired by ctd centroid rank-match 2026-09-23)",
        "subtype_confidence": "SPINEPS+VERIDAH pseudo-truth (ctd), not a radiologist read",
        "labels": [VERSE.get(l, str(l)) for l in labels],
        "c1_added": bool(extra_c1),
        "sacrum_poi_dropped": sacrum_poi_dropped,
        "sacrum_instance_dropped": [dict(old_id=p["old_id"], vox=p["vox"], dz_mm=p["dz_mm"]) for p in sacrum_dropped],
        "id_guard": {k: chk.get(k) for k in ("verdict", "ctd_agree", "ctd_disagree")},
        "pairs": pairs,
    }
    json.dump(rep, open(a.report, "w"), indent=1)
    print(f"RCTSFIX {a.case} subtype={subtype} labels={rep['labels']}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
