#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/verification_pages.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Human truth-verification worklist for the real-frame G3 TEST persons (SchwingNet/LEVELCHECK_MODEL.md section 4).

WHY. Every COBRA test person's subtype and lumbar names come from SPINEPS+VERIDAH on the deformed planning CT, and
the C-ArmLSpine truth comes from two labellers on a lumbar-only CBCT. Section 4 requires a human to confirm or
correct the subtype and the lumbar names of every such person, written to a frozen truth file whose SHA-256 is
recorded, BEFORE unblinding. This tool builds the worklist and one page per person; it never fills the truth in.

WHAT A PAGE SHOWS (one JPEG per person, pages/<order>_<corpus>_<case>.jpg):
  a  coronal MIP of the spine slab (the CT between the posterior and anterior faces of the vertebra masks, +-15 mm)
     with every vertebral body labelled BY POSITION -- P1 is the first body above the sacrum, P2 the next, ... --
     never by a name. Ribs: TotalSegmentator rib masks in green, bone TotalSegmentator did not label in orange;
     each rib's medial end carries the position it attaches to ('>P7'), found by tracing bone to the vertebra.
  b  the same coronal field as a full-thickness MIP (rib count), c sagittal MIP +-10 mm, d lumbosacral sagittal
     thin slab (the L5/S1 or L6/S1 joint: a disc or a fusion), e/f the real frames the analysis will score
     (AP-most and lateral-most of the person's exported frames), g the text: the proposed subtype and its reason,
     the field-of-view facts, and per position the TWO automatic labellings (VERIDAH's ctd name bound to that
     body by position; TotalSegmentator's class covering that body) with the ribs attached.
  Where the sacrum is not in the field the bodies are labelled V1.. from the top and the page says the count
  cannot be anchored. A position label is a geometric fact; the names beside it are model outputs.

ORDER (worklist.csv `order`): tier 1 = transitional calls with a real frame, the known-problem calls first
  (L6 called with no L1 in the field; T13 calls naming only L1-L4; calls resting on a VERIDAH T12 skip; the three
  C-ArmLSpine L6 patients whose two labellers agree on no lumbar level); tier 2 = ordinary test persons with a
  real frame; tier 3 = test persons with no exported real frame (not in the primary analysis; verify last).

TRUTH FILE. truth_to_fill.csv has one row per person and blank reader columns. `freeze` validates a filled copy,
derives the lumbar names from (lowest rib-bearing body, number of lumbar bodies) and writes truth_frozen.csv with
its SHA-256. The tool never writes a subtype or a name into the reader columns.

Volumes are canonicalised to RAS for ANALYSIS only; nothing is written back as a volume. Every input is read from
the frozen v1 snapshot or from stores other workflows wrote; nothing outside <out> is written.

    python tools/verification_pages.py build   [--out DIR]                       (grid: worklist + blank csv)
    python tools/verification_pages.py render  [--shard i --n-shards n] [--cases A158,case42] [--force]
    python tools/verification_pages.py index   [--out DIR]                       (index.html + summary)
    python tools/verification_pages.py freeze  --csv FILLED.csv [--out DIR]      (validate + sha256)
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import time
import traceback
from collections import Counter, OrderedDict
from pathlib import Path

import numpy as np

RS = Path("/rs/rs_grp_oschome/go2432")
D = RS / "data"
F6 = D / "fig6"
FROZEN = F6 / "frozen_v1"
SETS = F6 / "sets_v2"
OUT_DEFAULT = F6 / "verification"
COBRA_CASES = D / "cobra2026/cases"
COBRA_NII = [D / "cobra2026/lstv/nifti", D / "cobra2026/varian/nifti"]
COBRA_TS = D / "anomaly_harvest/cobra/ts"                       # TotalSegmentator total (--ml) on ct_def's grid
CLASS_MAP = D / "anomaly_harvest/cobra/class_map.json"
CARM_NII = D / "carmlspine/nifti"
CARM_SPINEPS = [D / "carmlspine/spineps", D / "carmlspine/spineps_retry134"]
CARM_TS = D / "or_ready/auto_reference/ts/carmlspine"          # TotalSegmentator total (--ml) on the CBCT grid
CARM_LEVELS = D / "carmlspine/levels.json"

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "sacrum", 27: "coccyx", 28: "T13"}
ORDER = list(range(1, 20)) + [28] + list(range(20, 26)) + [26]
RANK = {lab: k for k, lab in enumerate(ORDER)}
SUBTYPES = ("ordinary", "L6", "T13", "sacralised_L5", "four_lumbar", "both_L6_T13", "cannot_verify")
READER_COLS = ["subtype_confirmed", "subtype_corrected", "lowest_rib_bearing_body", "n_lumbar_bodies",
               "sacrum_in_field", "lowest_rib_in_field", "lumbar_names_top_to_bottom", "reader_initials",
               "read_date", "notes"]
ID_COLS = ["order", "tier", "person", "corpus", "case", "proposed_subtype", "proposed_by", "flags",
           "has_real_frame", "page"]
PROBLEM_ORDER = ["carm_L6_contested", "L6_no_L1", "T12_skip", "T13_only_L1_L4", "four_lumbar_candidate"]

# TotalSegmentator v2 `total` ids used here (read from class_map.json at run time; these are the names)
TS_VERT_NAMES = ["sacrum", "vertebrae_S1"] + [f"vertebrae_L{i}" for i in range(5, 0, -1)] + \
                [f"vertebrae_T{i}" for i in range(12, 0, -1)] + [f"vertebrae_C{i}" for i in range(7, 0, -1)]
TS_MUSCLE_NAMES = ["autochthon_left", "autochthon_right", "iliopsoas_left", "iliopsoas_right",
                   "gluteus_maximus_left", "gluteus_maximus_right"]


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jload(p):
    return json.load(open(p))


# ---------------------------------------------------------------------------------------------------- worklist
def frame_angle(meta_path: Path):
    """lat_from_ap_deg of an exported frame (0 = AP, 90 = lateral), or None."""
    try:
        m = jload(meta_path)
    except Exception:
        return None
    v = m.get("view")
    if isinstance(v, dict) and "lat_from_ap_deg" in v:
        return float(v["lat_from_ap_deg"])
    if isinstance(v, str):
        return {"AP": 0.0, "LAT": 90.0, "LAT2": 90.0}.get(v.upper())
    vc = m.get("view_class")
    if isinstance(vc, str):
        return {"AP": 0.0, "LAT": 90.0}.get(vc.upper())
    return None


def pick_frames(set_name: str, person: str, frames: dict):
    """The AP-most and the lateral-most exported frame of a person, as (stem, gate, angle, image path)."""
    cands = []
    for gate in ("open", "blinded"):
        for stem in frames.get(gate, []):
            img = SETS / set_name / gate / "images" / f"{stem}.png"
            meta = SETS / set_name / gate / "meta" / f"{stem}.json"
            cands.append(dict(stem=stem, gate=gate, angle=frame_angle(meta), image=str(img)))
    if not cands:
        return []
    known = [c for c in cands if c["angle"] is not None]
    if not known:
        return [cands[0]] + ([cands[len(cands) // 2]] if len(cands) > 1 else [])
    ap = min(known, key=lambda c: abs(c["angle"]))
    lat = min(known, key=lambda c: abs(abs(c["angle"]) - 90.0))
    return [ap] if lat["stem"] == ap["stem"] else [ap, lat]


def cobra_flags(screen: dict) -> list:
    """The known problems of a COBRA screen call, computed from the frozen screen json itself."""
    fl = []
    st = screen.get("subtype")
    levels = screen.get("levels_present") or []
    lumbar = [n for n in levels if n.startswith("L")]
    labs = screen.get("ctd_check", {}).get("labels", []) or []
    if st == "L6" and "L1" not in levels:
        fl.append("L6_no_L1")
    if st == "T13" and lumbar == ["L1", "L2", "L3", "L4"]:
        fl.append("T13_only_L1_L4")
    if labs and 19 not in labs and 20 in labs and any(8 <= l <= 18 for l in labs):
        fl.append("T12_skip")
    if st == "four_lumbar" or "four_lumbar CANDIDATE" in (screen.get("reason") or ""):
        fl.append("four_lumbar_candidate")
    return fl


def cmd_build(a) -> int:
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    strat = jload(FROZEN / "stratify.json")
    split = jload(FROZEN / "split_final.json")
    strata = jload(FROZEN / "strata.json")["strata"]
    t2 = jload(SETS / "T2/persons.json")
    t3 = jload(SETS / "T3/persons.json")
    carm_levels = jload(CARM_LEVELS).get("cases", {}) if CARM_LEVELS.exists() else {}
    rows = []
    # COBRA: every test person of the frozen split
    for key, rec in sorted(strat["cobra"].items()):
        if rec.get("side") != "test":
            continue
        case = key.split(":")[1]
        sp = FROZEN / "cobra_lstv" / f"{case}.json"
        screen = jload(sp) if sp.exists() else {}
        status = rec.get("status")
        subtype = screen.get("subtype", rec.get("call", "unreadable"))
        reason = screen.get("reason", rec.get("reason", ""))
        flags = cobra_flags(screen)
        transitional = status in ("transitional_call", "reread_candidate")
        pers = t2.get(key, {})
        frames = pick_frames("T2", key, pers.get("frames", {}))
        withheld = pers.get("withheld") or {}
        if not isinstance(withheld, dict):
            withheld = {"withheld": str(withheld)}
        rows.append(dict(person=key, corpus="cobra", case=case, set="T2", status=status, subtype=subtype,
                         proposed_by="SPINEPS+VERIDAH screen of the deformed planning CT (tools/cobra_lstv_screen.py)",
                         reason=reason, flags=flags, transitional=transitional, frames=frames,
                         withheld=withheld, stratum=strata.get(key, {}).get("stratum", "ordinary"),
                         levels_present=screen.get("levels_present") or [],
                         screen_json=str(sp), screen_sha256=sha256(sp) if sp.exists() else None))
    # C-ArmLSpine: every test person of the frozen split
    for key, side in sorted(split["side_of_person"].items()):
        if not key.startswith("carmlspine:") or side != "test":
            continue
        case = key.split(":")[1]
        prec = strat["people"].get(key)
        lv = carm_levels.get(case, {})
        pairs = [(v.get("ts"), v.get("spineps")) for v in lv.get("vertebrae", [])]
        if prec:
            subtype, reason = prec.get("subtype"), ("stratify.json: " + prec.get("truth", ""))
            flags = ["carm_L6_contested"]
            reason = ("VERIDAH names the mobile bodies L2-L6, TotalSegmentator names the same bodies L1-L5 "
                      "(carmlspine/levels.json: no lumbar level agreed); neither saw the ribs")
            transitional = True
        else:
            subtype, flags, transitional = "ordinary", [], False
            reason = "no transitional call by either labeller; G3 ordinary hash rule"
        pers = t3.get(key, {})
        frames = pick_frames("T3", key, pers.get("frames", {}))
        wh = pers.get("withheld") or {}
        if not isinstance(wh, dict):
            wh = {"withheld": str(wh)}
        rows.append(dict(person=key, corpus="carmlspine", case=case, set="T3", status="cbct_two_labellers",
                         subtype=subtype, proposed_by="stratify.json (VERIDAH L6 call on the CBCT)" if prec else
                         "no call (two labellers agree on the ordinary names, carmlspine/levels.json)",
                         reason=reason, flags=flags, transitional=transitional, frames=frames,
                         withheld=wh, stratum=strata.get(key, {}).get("stratum", "ordinary"),
                         levels_present=[f"{t}/{s}" for t, s in pairs], screen_json=None, screen_sha256=None))
    # order: tier, then the problems, then case
    def prio(r):
        has = 1 if r["frames"] else 0
        tier = (1 if r["transitional"] else 2) if has else 3
        pk = min([PROBLEM_ORDER.index(f) for f in r["flags"] if f in PROBLEM_ORDER] or [len(PROBLEM_ORDER)])
        sub = 0 if r["transitional"] else 1
        return (tier, sub, pk, r["corpus"], r["case"])
    rows.sort(key=prio)
    for i, r in enumerate(rows, 1):
        r["order"] = i
        r["tier"] = prio(r)[0]
        r["page"] = f"pages/{i:03d}_{r['corpus']}_{r['case']}.jpg"
    json.dump(rows, open(out / "worklist.json", "w"), indent=1)
    with open(out / "worklist.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ID_COLS + ["status", "stratum", "reason", "levels_present", "frames", "withheld"])
        for r in rows:
            w.writerow([r["order"], r["tier"], r["person"], r["corpus"], r["case"], r["subtype"], r["proposed_by"],
                        "+".join(r["flags"]), "yes" if r["frames"] else "no", r["page"], r["status"], r["stratum"],
                        r["reason"], " ".join(r["levels_present"]), " ".join(fr["stem"] for fr in r["frames"]),
                        ";".join(f"{k}={v}" for k, v in (r["withheld"] or {}).items())])
    with open(out / "truth_to_fill.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ID_COLS + READER_COLS)
        for r in rows:
            w.writerow([r["order"], r["tier"], r["person"], r["corpus"], r["case"], r["subtype"], r["proposed_by"],
                        "+".join(r["flags"]), "yes" if r["frames"] else "no", r["page"]] + [""] * len(READER_COLS))
    # the record correction (stratify.json is frozen and owned by another workflow: it is NOT edited here)
    corr = {"_about": "Correction to results/rare_class/stratify.json (frozen in fig6/frozen_v1, sha256 recorded in "
                      "SHA256SUMS.json; owned by tools/make_split.py). The frozen file is not edited: this record "
                      "states what is wrong in it and what the truth file must carry instead.",
            "written": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "corrections": []}
    for key in ("carmlspine:case42", "carmlspine:case121", "carmlspine:case136"):
        prec = strat["people"].get(key, {})
        corr["corrections"].append({
            "person": key, "field": "verified", "recorded": prec.get("verified"), "correct": False,
            "recorded_truth": prec.get("truth"),
            "why": "carmlspine/levels.json (tools/dual_seg_compare.py): TotalSegmentator names the five mobile bodies "
                   "L1-L5 and VERIDAH names them L2-L6; no lumbar level is agreed (only the sacrum). The L6 rests on "
                   "VERIDAH alone, called on a lumbar-only CBCT with no rib in view. results/spineps_ids/VERIFY.md "
                   "item 1a: FAIL as transitional truth. LEVELCHECK_MODEL.md s4 already excludes these three from "
                   "the primary analysis; their subtype is 'unverified' until a human reads this worklist page.",
            "worklist_page": next(r["page"] for r in rows if r["person"] == key)})
    json.dump(corr, open(out / "stratify_corrections.json", "w"), indent=1)
    n = Counter((r["tier"], r["corpus"]) for r in rows)
    build = {"written": corr["written"], "tool": "tools/verification_pages.py build",
             "inputs": {str(p): sha256(p) for p in [FROZEN / "stratify.json", FROZEN / "split_final.json",
                                                    FROZEN / "strata.json", SETS / "T2/persons.json",
                                                    SETS / "T3/persons.json"]},
             "carm_levels": str(CARM_LEVELS), "persons": len(rows),
             "per_tier_corpus": {f"tier{t}|{c}": k for (t, c), k in sorted(n.items())},
             "flags": dict(Counter(f for r in rows for f in r["flags"]))}
    json.dump(build, open(out / "BUILD.json", "w"), indent=1)
    log(f"worklist: {len(rows)} persons; {build['per_tier_corpus']}; flags {build['flags']}")
    return 0


# ---------------------------------------------------------------------------------------------------- volumes
def mha_to_nib(p: Path):
    import nibabel as nib
    import SimpleITK as sitk
    im = sitk.ReadImage(str(p))
    arr = sitk.GetArrayFromImage(im).transpose(2, 1, 0)             # (x, y, z) in the image's own index order
    sp = np.asarray(im.GetSpacing()); org = np.asarray(im.GetOrigin())
    dc = np.asarray(im.GetDirection()).reshape(3, 3)
    A = np.eye(4); A[:3, :3] = dc * sp[None, :]; A[:3, 3] = org        # LPS world
    A[:2] *= -1                                                        # -> RAS
    return nib.Nifti1Image(np.ascontiguousarray(arr), A)


def on_grid(img, ref):
    import nibabel as nib
    from nibabel.processing import resample_from_to
    c = nib.as_closest_canonical(img)
    if c.shape == ref.shape and np.allclose(c.affine, ref.affine, atol=1e-3):
        return np.asanyarray(c.dataobj)
    return np.asanyarray(resample_from_to(img, (ref.shape, ref.affine), order=0).dataobj)


def world_of(A, ijk):
    ijk = np.atleast_2d(np.asarray(ijk, float))
    return ijk @ A[:3, :3].T + A[:3, 3]


def poi_world(ctd_path):
    d = jload(ctd_path)
    meta, pts = d[0], d[-1]
    rot = np.asarray(meta["rotation"], float); zoom = np.asarray(meta["zoom"], float)
    origin = np.asarray(meta["origin"], float)
    out = {}
    for k, v in pts.items():
        c = v.get("50") or next(iter(v.values()))
        out[int(k)] = rot @ (np.asarray(c, float) * zoom) + origin     # RAS mm (the screen's own convention)
    return out


def lookup(arr, Ainv, w, rad=3):
    ix = np.round((Ainv @ np.r_[w, 1.0])[:3]).astype(int)
    if (ix < 0).any() or (ix >= np.array(arr.shape)).any():
        return 0
    v = int(arr[tuple(ix)])
    if v:
        return v
    lo = np.clip(ix - rad, 0, None); hi = np.minimum(ix + rad + 1, arr.shape)
    win = arr[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    u, n = np.unique(win[win > 0], return_counts=True)
    return int(u[np.argmax(n)]) if len(u) else 0


def objects(lab, A, min_vox=1):
    from scipy import ndimage
    out = {}
    sl = ndimage.find_objects(lab.astype(np.int32))
    for i, s in enumerate(sl):
        if s is None:
            continue
        l = i + 1
        sub = lab[s] == l
        n = int(sub.sum())
        if n < min_vox:
            continue
        idx = np.argwhere(sub) + np.array([x.start for x in s])
        w = world_of(A, idx)
        out[l] = dict(vox=n, centroid=w.mean(0), zmin=float(w[:, 2].min()), zmax=float(w[:, 2].max()),
                      xyz=w, idx=idx)
    return out


def bone_path_attach(rib_idx, hu, sarr, tsr, rc, axis_xy_at, Ac, sac_ids, thr=150.0, max_it=30):
    """Grow from the medial 15 mm of a rib through bone (HU >= thr, not another TS rib, not a vertebra) until the
    front touches a SPINEPS instance; the first instance touched is the one the rib reaches through bone
    (tools/ts12_verify_ids.py). Returns (instance, steps, how)."""
    from scipy import ndimage
    from scipy.spatial import cKDTree
    w = world_of(Ac, rib_idx)
    axx, axy = axis_xy_at(w[:, 2])
    rh = np.hypot(w[:, 0] - axx, w[:, 1] - axy)
    seed_idx = rib_idx[rh <= rh.min() + 15.0]
    lo = np.maximum(seed_idx.min(0) - 40, 0); hi = np.minimum(seed_idx.max(0) + 41, hu.shape)
    sl = tuple(slice(int(a), int(b)) for a, b in zip(lo, hi))
    H = hu[sl]; S = sarr[sl]; T = tsr[sl]; O = (T > 0) & (T != rc)
    seed = np.zeros(H.shape, bool)
    q = seed_idx - lo
    seed[q[:, 0], q[:, 1], q[:, 2]] = True
    vert = (S > 0) & ~np.isin(S, list(sac_ids))
    allowed = (H >= thr) & ~O & (S == 0)
    st = np.ones((3, 3, 3), bool)
    front = seed.copy(); visited = seed.copy()
    it = 0
    for it in range(max_it):
        ring = ndimage.binary_dilation(front, structure=st)
        touch = ring & vert
        if touch.any():
            v, n = np.unique(S[touch], return_counts=True)
            return int(v[np.argmax(n)]), it, "bone"
        front = ring & allowed & ~visited
        if not front.any():
            break
        visited |= front
    reach = np.argwhere(visited)
    inst_pts = np.argwhere(vert)
    if len(inst_pts) == 0:
        return None, it, "none"
    t = cKDTree(inst_pts)
    d, j = t.query(reach[:: max(1, len(reach) // 3000)], k=1)
    k = int(np.argmin(d))
    ip = inst_pts[j[k]]
    return int(S[tuple(ip)]), it, f"nearest-after-stall({d[k] * float(np.abs(Ac[0, 0])):.1f}mm)"


# ---------------------------------------------------------------------------------------------------- one person
def find_inputs(row):
    """CT (or CBCT), SPINEPS instance mask + ctd, TotalSegmentator multilabel -- all existing files, read only."""
    corpus, case = row["corpus"], row["case"]
    inp = {}
    if corpus == "cobra":
        ct = next((d / f"{case}_ct.nii.gz" for d in COBRA_NII if (d / f"{case}_ct.nii.gz").exists()), None)
        if ct is None:
            seg_ct = D / "cobra2026/seg" / case / "ct_def.nii.gz"
            ct = seg_ct if seg_ct.exists() else COBRA_CASES / case / "ct_def.mha"
        inp["ct"] = str(ct)
        inp["ct_kind"] = "planning CT deformably registered to the CBCT (ct_def)"
        screen = jload(row["screen_json"]) if row.get("screen_json") and Path(row["screen_json"]).exists() else {}
        mask, ctd = screen.get("mask"), screen.get("ctd")
        if not mask:
            for d in (D / "cobra2026/lstv/seg", D / "spineps/cobra_varian"):
                if (d / f"{case}_seg-vert_msk.nii.gz").exists():
                    mask = str(d / f"{case}_seg-vert_msk.nii.gz"); ctd = str(d / f"{case}_ctd.json"); break
        inp["mask"], inp["ctd"] = mask, ctd
        ts = COBRA_TS / f"{case}.nii.gz"
        inp["ts"] = str(ts) if ts.exists() else None
        inp["hu_scale"] = "HU"
    else:
        inp["ct"] = str(CARM_NII / f"{case}_cbct.nii.gz")
        inp["ct_kind"] = "intraoperative CBCT (lumbar field, values rescaled to HU-like by TS muscle/vertebra medians)"
        mask = ctd = None
        for d in CARM_SPINEPS:
            for nm in (f"{case}_seg-vert_msk_veridah.nii.gz", f"{case}_seg-vert_msk.nii.gz"):
                if (d / nm).exists() and (d / f"{case}_ctd.json").exists():
                    mask, ctd = str(d / nm), str(d / f"{case}_ctd.json"); break
            if mask:
                break
        inp["mask"], inp["ctd"] = mask, ctd
        ts = CARM_TS / f"{case}.nii.gz"
        inp["ts"] = str(ts) if ts.exists() else None
        inp["hu_scale"] = "anchored"
    return inp


def load_ct(p: str):
    import nibabel as nib
    return mha_to_nib(Path(p)) if p.endswith(".mha") else nib.load(p)


def analyse(row, inp):
    """Everything the page draws, from the volumes: positions, the two labellings, ribs, field facts."""
    import nibabel as nib
    from scipy import ndimage
    from scipy.spatial import cKDTree
    R = {"inputs": inp}
    ct = load_ct(inp["ct"])
    ctc = nib.as_closest_canonical(ct)
    Ac = ctc.affine; Ainv = np.linalg.inv(Ac)
    hu = np.asanyarray(ctc.dataobj).astype(np.float32)
    zooms = np.abs(np.diag(Ac[:3, :3]))
    voxml = float(np.prod(zooms)) / 1000.0
    R["ct_shape"] = list(hu.shape); R["ct_zooms_mm"] = [round(float(z), 3) for z in zooms]
    zc = world_of(Ac, [[0, 0, 0], [0, 0, hu.shape[2] - 1]])[:, 2]
    R["ct_z_range_mm"] = [round(float(zc.min()), 1), round(float(zc.max()), 1)]
    # TotalSegmentator multilabel on the same grid
    cmap = {int(k): v for k, v in jload(CLASS_MAP).items()}
    name2id = {v: k for k, v in cmap.items()}
    tsml = on_grid(nib.load(inp["ts"]), ctc).astype(np.int16) if inp.get("ts") else np.zeros(hu.shape, np.int16)
    rib_ids = {name2id[f"rib_{s}_{k}"]: (s, k) for s in ("left", "right") for k in range(1, 13)
               if f"rib_{s}_{k}" in name2id}
    tsr = np.zeros(hu.shape, np.int16)
    for cid, (s, k) in rib_ids.items():
        tsr[tsml == cid] = (100 if s == "left" else 200) + k
    vert_ids = {name2id[n]: n.replace("vertebrae_", "") for n in TS_VERT_NAMES if n in name2id}
    # CBCT values -> HU-like, anchored on the TS labels of this volume (rib_count_reader.py's rule)
    if inp["hu_scale"] == "anchored" and inp.get("ts"):
        vmask = np.isin(tsml, [i for i, n in vert_ids.items() if n not in ("sacrum", "S1")])
        mids = [name2id[n] for n in TS_MUSCLE_NAMES if n in name2id]
        mmask = np.isin(tsml, mids)
        if vmask.sum() > 1000 and mmask.sum() > 1000:
            mv, mm = float(np.median(hu[vmask])), float(np.median(hu[mmask]))
            if mv - mm > 1e-3:
                hu = 40.0 + (hu - mm) * (210.0 / (mv - mm))
                R["hu_anchor"] = dict(vertebra_median_raw=round(mv, 1), muscle_median_raw=round(mm, 1))
    # SPINEPS instances (ids < 100; discs / end plates >= 100 dropped) and the ctd names bound BY POSITION
    simg = nib.load(inp["mask"])
    sarr = on_grid(simg, ctc).astype(np.int16)
    sarr[(sarr >= 100) | (sarr == 80)] = 0
    sobj = objects(sarr, Ac, min_vox=max(20, int(1.0 / voxml)))
    pts = poi_world(inp["ctd"]) if inp.get("ctd") and Path(inp["ctd"]).exists() else {}
    bound = {}                                                            # instance -> [ctd labels]
    for lab, w in pts.items():
        v = lookup(sarr, Ainv, w)
        if v:
            bound.setdefault(v, []).append(lab)
    # the sacrum: SPINEPS 26 when it is a real object, else TotalSegmentator sacrum + S1
    sac_mask = None; sac_src = None
    if 26 in sobj and sobj[26]["vox"] * voxml >= 3.0:
        sac_mask = sarr == 26; sac_src = "SPINEPS id 26"
    elif inp.get("ts"):
        ids = [i for i, n in vert_ids.items() if n in ("sacrum", "S1")]
        m = np.isin(tsml, ids)
        if m.sum() * voxml >= 3.0:
            sac_mask = m; sac_src = "TotalSegmentator sacrum+S1 (SPINEPS has no sacrum object)"
    sac = None
    if sac_mask is not None:
        idx = np.argwhere(sac_mask); w = world_of(Ac, idx)
        sac = dict(centroid=w.mean(0), zmin=float(w[:, 2].min()), zmax=float(w[:, 2].max()), vox=int(len(idx)),
                   cut_bottom=bool(idx[:, 2].min() <= 0), src=sac_src,
                   zmax_mid=float(np.percentile(w[np.abs(w[:, 0] - np.median(w[:, 0])) < 12, 2], 99.5))
                   if (np.abs(w[:, 0] - np.median(w[:, 0])) < 12).sum() > 50 else float(w[:, 2].max()))
    R["sacrum"] = None if sac is None else {k: (round(float(v), 1) if isinstance(v, (float, np.floating)) else v)
                                            for k, v in sac.items() if k != "centroid"}
    inst_all = [l for l in sobj if l not in (26, 27) and sobj[l]["vox"] * voxml >= 3.0]
    dropped = []
    if sac is not None:
        keep = []
        for l in inst_all:
            if sobj[l]["centroid"][2] < sac["centroid"][2]:
                dropped.append((int(l), "centroid below the sacrum centroid: sacral fragment"))
            else:
                keep.append(l)
        inst_all = keep
    inst = sorted(inst_all, key=lambda l: -sobj[l]["centroid"][2])       # top -> bottom
    n = len(inst)
    pos = {l: (f"P{n - i}" if sac is not None else f"V{i + 1}") for i, l in enumerate(inst)}
    R["position_scheme"] = ("P = presacral index counting UP from the sacrum (P1 = first body above the sacrum)"
                            if sac is not None else "V = index from the TOP of the field (no sacrum in the field)")
    R["dropped_instances"] = dropped
    # TS class covering each instance
    ts_of = {}
    for l in inst:
        vals, cnt = np.unique(tsml[sarr == l], return_counts=True)
        best, bf = None, 0.0
        for v, c in zip(vals, cnt):
            if int(v) in vert_ids and c / sobj[l]["vox"] > bf:
                best, bf = vert_ids[int(v)], c / sobj[l]["vox"]
        ts_of[l] = (best, round(float(bf), 2))
    # body centres (anterior half) -> the column axis
    bc = np.array([sobj[l]["xyz"][sobj[l]["xyz"][:, 1] >= np.median(sobj[l]["xyz"][:, 1])].mean(0) for l in inst]) \
        if inst else np.zeros((0, 3))
    if len(bc) >= 2:
        zo = np.argsort(bc[:, 2])

        def axis_xy_at(z):
            return np.interp(z, bc[zo, 2], bc[zo, 0]), np.interp(z, bc[zo, 2], bc[zo, 1])
    elif len(bc) == 1:
        def axis_xy_at(z):
            z = np.asarray(z, float); return np.full(z.shape, bc[0, 0]), np.full(z.shape, bc[0, 1])
    else:
        def axis_xy_at(z):
            z = np.asarray(z, float); return np.zeros(z.shape), np.zeros(z.shape)
    # ribs: TS rib masks, then bone TS did not label
    sac_ids = {26}
    ribs = []
    robj = objects(tsr, Ac, min_vox=max(30, int(0.3 / voxml)))
    if inst:
        spts = np.concatenate([sobj[l]["xyz"] for l in inst]); sown = np.concatenate([np.full(sobj[l]["vox"], l) for l in inst])
        stree = cKDTree(spts)
    for rc in sorted(robj):
        xyz = robj[rc]["xyz"]
        if not inst:
            break
        bp, bsteps, bhow = bone_path_attach(robj[rc]["idx"], hu, sarr, tsr, rc, axis_xy_at, Ac, sac_ids)
        d, j = stree.query(xyz, k=1)
        m = np.argsort(d)[:100]
        v, cnt = np.unique(sown[j[m]], return_counts=True)
        near = int(v[np.argmax(cnt)])
        att = bp if (bhow == "bone" and bp in inst) else near
        med = xyz[m].mean(0)
        chord = float(np.max(np.linalg.norm(xyz - med, axis=1)))
        ribs.append(dict(kind="TS", ts_rib=f"rib_{'left' if rc < 200 else 'right'}_{rc % 100}",
                         side="L" if rc < 200 else "R", vox=robj[rc]["vox"], ml=round(robj[rc]["vox"] * voxml, 1),
                         medial_gap_mm=round(float(np.median(d[m])), 1), medial_xyz=[round(float(x), 1) for x in med],
                         chord_mm=round(chord, 1), attach=int(att) if att in inst else None,
                         attach_pos=pos.get(att), rule="bone_path" if (bhow == "bone" and bp in inst) else "medial_end",
                         far=bool(np.median(d[m]) > 25.0)))
    # bone in no TS label except the ribs and not in a SPINEPS instance -- CT only: on a CBCT the rescaled values
    # are not HU and scatter artefact beside the spine passes a 200 threshold (case42 smoke: soft tissue 'ribs')
    R["ct_only_rib_search"] = bool(inp.get("ts") and inst and inp["hu_scale"] == "HU")
    if R["ct_only_rib_search"]:
        nonrib = (tsml > 0) & (tsr == 0)
        cand = (hu >= 200) & ~ndimage.binary_dilation(nonrib, iterations=1) & ~ndimage.binary_dilation(sarr > 0, iterations=1)
        del nonrib
        lab_c, ncomp = ndimage.label(cand, structure=np.ones((3, 3, 3)))
        del cand
        sizes = np.bincount(lab_c.ravel())
        objs_c = ndimage.find_objects(lab_c)
        zlow = min(sobj[l]["zmin"] for l in inst)
        for k in np.nonzero(sizes >= max(30, int(0.25 / voxml)))[0]:
            if k == 0:
                continue
            s_k = objs_c[k - 1]
            idx = np.argwhere(lab_c[s_k] == k) + np.array([x.start for x in s_k])
            w = world_of(Ac, idx)
            axx, axy = axis_xy_at(w[:, 2])
            rh = np.hypot(w[:, 0] - axx, w[:, 1] - axy)
            if rh.min() > 45.0 or rh.max() - rh.min() < 15.0 or w[:, 2].max() < zlow:
                continue
            tsfrac = float((tsr[tuple(idx.T)] > 0).mean())
            if tsfrac > 0.5:
                continue
            bp, steps, how = bone_path_attach(idx, hu, sarr, tsr, -1, axis_xy_at, Ac, sac_ids)
            if how != "bone" or bp not in inst:
                continue
            reach = float(rh.max() - rh.min())
            side = "R" if np.median(w[:, 0] - axx) > 0 else "L"
            kmed = int(np.argmin(rh))
            ribs.append(dict(kind="CT", ts_rib=None, side=side, vox=int(len(idx)), ml=round(len(idx) * voxml, 1),
                             medial_gap_mm=round(float(rh.min()), 1), medial_xyz=[round(float(x), 1) for x in w[kmed]],
                             chord_mm=round(reach, 1), attach=int(bp), attach_pos=pos.get(bp), rule="bone_path",
                             far=False, idx_box=[int(x.start) for x in s_k] + [int(x.stop) for x in s_k], comp=int(k)))
        # keep the label array for drawing the CT-only components
        keep_comps = {r["comp"] for r in ribs if r["kind"] == "CT"}
        ctr = np.isin(lab_c, list(keep_comps)) if keep_comps else np.zeros(hu.shape, bool)
        del lab_c
    else:
        ctr = np.zeros(hu.shape, bool)
    # a rib whose medial end lies at the field top is cut: its head may belong to a body above the field, and the
    # trace then lands on the transverse process of the first body in the field (C-ArmLSpine case101: both 12th
    # ribs were attached to L1). Such a rib never anchors the automatic count.
    ztop = float(zc.max())
    for r in ribs:
        r["cut_top"] = bool(r["medial_xyz"][2] >= ztop - 12.0)
    # per position: names and ribs
    positions = []
    top_cut = bottom_cut = False
    for i, l in enumerate(inst):
        o = sobj[l]
        idx = o["idx"]
        cut_top = bool(idx[:, 2].max() >= hu.shape[2] - 1)
        cut_bot = bool(idx[:, 2].min() <= 0)
        top_cut |= cut_top and i == 0
        labs = sorted(bound.get(l, []), key=lambda x: RANK.get(x, 99))
        rl = [r for r in ribs if r["attach"] == l and not r["far"]]
        positions.append(dict(pos=pos[l], instance_id=int(l), ml=round(o["vox"] * voxml, 1),
                              z_mm=round(float(o["centroid"][2]), 1),
                              veridah=[VERSE.get(x, str(x)) for x in labs],
                              ts=ts_of[l][0], ts_frac=ts_of[l][1],
                              ribs=[dict(side=r["side"], kind=r["kind"], chord_mm=r["chord_mm"], rule=r["rule"],
                                         cut_top=r["cut_top"]) for r in rl],
                              cut=("top" if cut_top else "bottom" if cut_bot else None)))
    R["positions"] = positions
    R["ribs"] = [{k: v for k, v in r.items() if k not in ("idx_box",)} for r in ribs]
    long_ribs = [r for r in ribs if not r["far"] and not r["cut_top"] and r["attach"] in inst and r["chord_mm"] >= 38.0]
    R["ribs_cut_by_field_top"] = sum(1 for r in ribs if not r["far"] and r["cut_top"])
    rib_pos = sorted({r["attach_pos"] for r in long_ribs}, key=lambda p: int(p[1:]))
    R["rib_bearing_positions"] = rib_pos
    if sac is not None and rib_pos:
        lowest = min(int(p[1:]) for p in rib_pos)
        R["lowest_rib_bearing_pos_auto"] = f"P{lowest}"
        R["n_rib_free_above_sacrum_auto"] = lowest - 1
    else:
        R["lowest_rib_bearing_pos_auto"] = None
        R["n_rib_free_above_sacrum_auto"] = None
    R["field"] = dict(sacrum_in_field=sac is not None, sacrum_source=sac_src,
                      sacrum_cut_by_bottom=bool(sac["cut_bottom"]) if sac else None,
                      sacrum_mm_in_field=round(sac["zmax"] - sac["zmin"], 1) if sac else None,
                      top_body_cut_by_field=top_cut, n_bodies=len(inst),
                      any_rib_in_field=bool(long_ribs), n_ts_ribs=sum(1 for r in ribs if r["kind"] == "TS" and not r["far"]),
                      n_ct_only_ribs=sum(1 for r in ribs if r["kind"] == "CT"))
    ctx = dict(ctc=ctc, hu=hu, sarr=sarr, sobj=sobj, inst=inst, pos=pos, sac_mask=sac_mask, sac=sac, tsr=tsr,
               ctr=ctr, ribs=ribs, ts_of=ts_of, bound=bound, axis_xy_at=axis_xy_at)
    return R, ctx


def render(row, R, ctx, out_path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from PIL import Image
    ctc, hu, sarr, sobj, inst, pos = ctx["ctc"], ctx["hu"], ctx["sarr"], ctx["sobj"], ctx["inst"], ctx["pos"]
    sac_mask, sac, tsr, ctr, ribs = ctx["sac_mask"], ctx["sac"], ctx["tsr"], ctx["ctr"], ctx["ribs"]
    A = ctc.affine
    sx, sy, sz = np.diag(A[:3, :3]); ox, oy, oz = A[:3, 3]
    X = ox + sx * np.arange(hu.shape[0]); Y = oy + sy * np.arange(hu.shape[1]); Z = oz + sz * np.arange(hu.shape[2])
    allidx = np.concatenate([sobj[l]["idx"] for l in inst] + ([np.argwhere(sac_mask)] if sac_mask is not None else [])) \
        if (inst or sac_mask is not None) else np.array([[hu.shape[0] // 2, hu.shape[1] // 2, hu.shape[2] // 2]])
    xc = int(round(np.median(allidx[:, 0]))); yc = int(round(np.median(allidx[:, 1])))
    y0 = max(int(allidx[:, 1].min() - 15 / sy), 0); y1 = min(int(allidx[:, 1].max() + 15 / sy) + 1, hu.shape[1])
    xs_c = slice(max(xc - int(175 / sx), 0), min(xc + int(175 / sx) + 1, hu.shape[0]))
    ys_s = slice(max(yc - int(110 / sy), 0), min(yc + int(120 / sy) + 1, hu.shape[1]))
    C_POS, C_VER, C_TS, C_RIB, C_CT, C_SAC = "#ffd400", "#ff4fd8", "#4fd2ff", "#39e639", "#ff9d1c", "#ffffff"
    flags = row.get("flags", [])

    def outlines_cor(ax, zs):
        for l in inst:
            pr = (sarr[xs_c, y0:y1, zs] == l).any(axis=1)
            if pr.any():
                ax.contour(X[xs_c], Z[zs], pr.T.astype(float), levels=[0.5], colors=[C_POS], linewidths=0.6)
        if sac_mask is not None:
            pr = sac_mask[xs_c, y0:y1, zs].any(axis=1)
            if pr.any():
                ax.contour(X[xs_c], Z[zs], pr.T.astype(float), levels=[0.5], colors=[C_SAC], linewidths=0.6, linestyles="dashed")
        rp = (tsr[xs_c, :, zs] > 0).any(axis=1)
        if rp.any():
            ax.contour(X[xs_c], Z[zs], rp.T.astype(float), levels=[0.5], colors=[C_RIB], linewidths=0.6)
        cp = ctr[xs_c, :, zs].any(axis=1)
        if cp.any():
            ax.contour(X[xs_c], Z[zs], cp.T.astype(float), levels=[0.5], colors=[C_CT], linewidths=0.6)

    def labels_cor(ax, names=True):
        for l in inst:
            c = sobj[l]["centroid"]
            ax.text(c[0] + 62, c[2], pos[l], color=C_POS, fontsize=10, fontweight="bold", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none", alpha=0.55))
            if names:
                labs = sorted(ctx["bound"].get(l, []), key=lambda q: RANK.get(q, 99))
                v = "/".join(VERSE.get(x, str(x)) for x in labs) or "-"
                t = ctx["ts_of"][l][0] or "-"
                ax.text(c[0] - 60, c[2] + 4, v, color=C_VER, fontsize=7.5, ha="center", va="center", fontweight="bold")
                ax.text(c[0] - 60, c[2] - 6, t, color=C_TS, fontsize=7.5, ha="center", va="center")
        if sac is not None:
            ax.text(sac["centroid"][0] + 62, min(sac["centroid"][2], sac["zmax"] - 30), "S", color=C_SAC, fontsize=10,
                    fontweight="bold", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none", alpha=0.55))
        for r in ribs:
            if r["attach"] is None or r["far"]:
                continue
            mx, my, mz = r["medial_xyz"]
            col = C_RIB if r["kind"] == "TS" else C_CT
            ax.plot([mx], [mz], "o", ms=3.5, color=col)
            dx = 30 if r["side"] == "R" else -30
            ax.text(mx + dx, mz, f">{r['attach_pos']}" + ("?" if r.get("cut_top") else "")
                    + ("" if r["chord_mm"] >= 38 else f" ({r['chord_mm']:.0f}mm)"),
                    color=col, fontsize=6.5, ha="center", va="center", fontweight="bold")

    def coronal(ax, slab, title):
        zs = slice(0, hu.shape[2])
        cor = hu[xs_c, y0:y1, :].max(axis=1) if slab else hu[xs_c, :, :].max(axis=1)
        ax.imshow(np.clip(cor.T, -150, 1100), cmap="gray", origin="lower", aspect="equal",
                  extent=[X[xs_c][0] - sx / 2, X[xs_c][-1] + sx / 2, Z[0] - sz / 2, Z[-1] + sz / 2])
        outlines_cor(ax, zs)
        labels_cor(ax, names=slab)
        ax.invert_xaxis()
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("patient's RIGHT on the left of the image; x mm", fontsize=7)
        ax.tick_params(labelsize=6)

    def sagittal(ax, xc_i, half_mm, zr, title, ywin=None, labels=True):
        xs = slice(max(xc_i - int(half_mm / sx), 0), min(xc_i + int(half_mm / sx) + 1, hu.shape[0]))
        zs = slice(max(int((zr[0] - oz) / sz) - 1, 0), min(int((zr[1] - oz) / sz) + 2, hu.shape[2]))
        sag = hu[xs, ys_s, zs].max(axis=0)
        ax.imshow(np.clip(sag.T, -150, 1300), cmap="gray", origin="lower", aspect="equal",
                  extent=[Y[ys_s][0] - sy / 2, Y[ys_s][-1] + sy / 2, Z[zs][0] - sz / 2, Z[zs][-1] + sz / 2])
        for l in inst:
            pr = (sarr[xs, ys_s, zs] == l).any(axis=0)
            if pr.any():
                ax.contour(Y[ys_s], Z[zs], pr.T.astype(float), levels=[0.5], colors=[C_POS], linewidths=0.6)
            if labels and zr[0] - 10 <= sobj[l]["centroid"][2] <= zr[1] + 10:
                c = sobj[l]["centroid"]
                ax.text(c[1] + 52, c[2], pos[l], color=C_POS, fontsize=9, fontweight="bold", ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none", alpha=0.55))
        if sac_mask is not None:
            pr = sac_mask[xs, ys_s, zs].any(axis=0)
            if pr.any():
                ax.contour(Y[ys_s], Z[zs], pr.T.astype(float), levels=[0.5], colors=[C_SAC], linewidths=0.6, linestyles="dashed")
            if labels:
                ax.text(sac["centroid"][1] + 52, max(zr[0] + 12, min(sac["centroid"][2], sac["zmax"] - 30)), "S", color=C_SAC,
                        fontsize=9, fontweight="bold", ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.15", fc="black", ec="none", alpha=0.55))
        ax.axhline(Z[0], color="red", lw=0.8, ls="--")
        ax.axhline(Z[-1], color="red", lw=0.8, ls="--")
        ax.invert_xaxis()
        if ywin:
            ax.set_xlim(*ywin)
        ax.set_ylim(*zr)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("ANTERIOR on the left; y mm | red dashed = field edge", fontsize=7)
        ax.tick_params(labelsize=6)

    fig = plt.figure(figsize=(24, 13.5))
    gs = GridSpec(2, 4, figure=fig, width_ratios=[1.35, 1.0, 1.05, 1.3], height_ratios=[1, 1], wspace=0.12, hspace=0.18,
                  left=0.03, right=0.99, top=0.95, bottom=0.04)
    ax_a = fig.add_subplot(gs[0, 0]); ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[0, 1]); ax_d = fig.add_subplot(gs[1, 1])
    ax_e = fig.add_subplot(gs[0, 2]); ax_f = fig.add_subplot(gs[1, 2])
    ax_g = fig.add_subplot(gs[:, 3])
    coronal(ax_a, True, "a  coronal MIP, spine slab +-15 mm: bodies by POSITION (yellow), rib attachments (>P)")
    coronal(ax_b, False, "b  coronal MIP, full thickness (count the ribs)")
    zall = (float(Z[0]) - 5, float(Z[-1]) + 5)
    sagittal(ax_c, xc, 10, zall, "c  sagittal MIP +-10 mm")
    if inst:
        lo = inst[-1]
        xl = int(round(np.median(sobj[lo]["idx"][:, 0])))
        ztop = sobj[inst[-3]]["zmax"] + 5 if len(inst) >= 3 else zall[1]
        zbot = max(zall[0], (sac["zmin"] if sac else sobj[lo]["zmin"]) - 10)
        ycl = sobj[lo]["centroid"][1]
        sagittal(ax_d, xl, 3, (zbot, ztop), "d  lumbosacral sagittal +-3 mm: disc or fusion below P1?",
                 ywin=(ycl + 95, ycl - 75))
    else:
        ax_d.axis("off"); ax_d.set_title("d  no vertebra instance found", fontsize=9)
    # frames
    frs = row.get("frames", [])
    for ax, k, lab in ((ax_e, 0, "e"), (ax_f, 1, "f")):
        ax.axis("off")
        if k < len(frs) and Path(frs[k]["image"]).exists():
            im = np.asarray(Image.open(frs[k]["image"]).convert("L"))
            ax.imshow(im, cmap="gray", aspect="equal")
            ang = frs[k]["angle"]
            ax.set_title(f"{lab}  real frame {frs[k]['stem']}" + (f"  ({ang:.0f} deg from AP)" if ang is not None else ""), fontsize=9)
        elif k == 0:
            ax.set_title(f"{lab}  no exported real frame (not in the primary analysis)", fontsize=9, color="red")
        else:
            ax.set_title(f"{lab}  (no second frame)", fontsize=9)
    # text
    ax_g.axis("off")
    L = []

    def add(t, c="black", w="normal", s=8.6):
        L.append((t, c, w, s))
    add(f"{row['person']}   order {row['order']:03d}   tier {row['tier']}   set {row['set']}", "black", "bold", 11)
    add(f"volume: {R['inputs']['ct_kind']}", "black", "normal", 7.5)
    add("colours on a-d: yellow = SPINEPS body outline + POSITION label; white dashed = sacrum; magenta = VERIDAH "
        "name; cyan = TotalSegmentator name; green = TS rib; orange = bone TS did not label; dot = a rib's medial end",
        "#444444", "normal", 7)
    add("")
    add(f"PROPOSED SUBTYPE: {row['subtype']}", "#8b0000" if row["transitional"] else "#1a5e1a", "bold", 11)
    add(f"by: {row['proposed_by']}", "black", "normal", 7.5)
    for line in wrap(f"reason: {row['reason']}", 78):
        add(line, "black", "normal", 7.5)
    if flags:
        add("KNOWN PROBLEMS WITH THIS CALL:", "red", "bold", 9)
        for f_ in flags:
            for line in wrap("  - " + FLAG_TEXT.get(f_, f_), 78):
                add(line, "red", "normal", 8)
    add("")
    F = R["field"]
    add("FIELD OF VIEW (measured on the volume)", "black", "bold", 9)
    add(f"  sacrum in field: {'yes' if F['sacrum_in_field'] else 'NO'}"
        + (f" ({F['sacrum_source']}; {F['sacrum_mm_in_field']} mm{'; CUT by the field bottom' if F['sacrum_cut_by_bottom'] else ''})" if F["sacrum_in_field"] else ""),
        "black" if F["sacrum_in_field"] else "red")
    add(f"  bodies in field: {F['n_bodies']}" + ("; the top body is CUT by the field" if F["top_body_cut_by_field"] else ""))
    add(f"  ribs attached in field: {F['n_ts_ribs']} TS ribs, {F['n_ct_only_ribs']} CT-only components"
        + ("" if R.get("ct_only_rib_search") else " (CT-only search not run: CBCT values are not HU)")
        + f"; rib-bearing positions (rib >= 38 mm): {', '.join(R['rib_bearing_positions']) or 'none'}")
    if R["lowest_rib_bearing_pos_auto"]:
        add(f"  automatic: lowest rib-bearing body {R['lowest_rib_bearing_pos_auto']} -> "
            f"{R['n_rib_free_above_sacrum_auto']} rib-free bodies above the sacrum (CHECK it on panels a/b)", "#333333")
    else:
        add("  automatic: the last rib-bearing body is NOT in the field (or no sacrum): the count cannot be anchored "
            "from this volume", "red")
    add("")
    add("POSITIONS, top to bottom -- the two automatic labellings (neither is truth)", "black", "bold", 9)
    add("  pos   VERIDAH(ctd)  TotalSeg      ribs attached (side, length)      size", "#444444", "normal", 7.5)
    for p in R["positions"]:
        rib_s = ", ".join(("%s%s %.0fmm%s%s" % (r["side"], "" if r["kind"] == "TS" else "*", r["chord_mm"],
                                                "" if r["chord_mm"] >= 38 else " stump",
                                                " CUT?" if r.get("cut_top") else "")) for r in p["ribs"]) or "-"
        ver_s = "/".join(p["veridah"]) or "-"
        ts_s = ("%s %.2f" % (p["ts"], p["ts_frac"])) if p["ts"] else "-"
        cut_s = (" CUT " + p["cut"]) if p["cut"] else ""
        add("  %-5s %-13s %-13s %-33s %.0f ml%s" % (p["pos"], ver_s, ts_s, rib_s, p["ml"], cut_s), "black", "normal", 7.5)
    if sac is not None:
        add(f"  S     sacrum ({sac['src']})", "black", "normal", 7.5)
    add("  * = bone TotalSegmentator did not label as a rib (a 13th rib, a lumbar rib, or a fragment); CUT? = the rib's "
        "medial end is at the field top, its head may belong to a body above the field: not counted", "#444444", "normal", 7)
    if row["corpus"] == "carmlspine" and row.get("levels_present"):
        add(f"  carmlspine/levels.json TS/VERIDAH pairs: {' '.join(row['levels_present'])}", "#444444", "normal", 7)
    add("")
    add("WHAT TO WRITE IN truth_to_fill.csv (this row)", "black", "bold", 9)
    for line in ("subtype_confirmed: Y if the proposed subtype is right, N if not",
                 "subtype_corrected: ordinary | L6 | T13 | sacralised_L5 | four_lumbar | both_L6_T13 | cannot_verify",
                 "lowest_rib_bearing_body: its P-label (P7 ...), or 'not_in_field'",
                 "n_lumbar_bodies: rib-free bodies between that body and the sacrum (blank if it cannot be counted)",
                 "sacrum_in_field / lowest_rib_in_field: Y or N;  reader_initials, read_date (YYYY-MM-DD), notes"):
        add("  " + line, "black", "normal", 7.5)
    add("")
    add("CONVENTION (docs/STUDENT_FLUORO_CORRECTION_GUIDE.md): L6 = six rib-free mobile bodies between the last", "#333333", "normal", 7)
    add("rib-bearing body and the sacrum; T13 = thirteen rib-bearing bodies (needs T1 in the field); sacralised_L5 =", "#333333", "normal", 7)
    add("the last presacral body fused to the sacrum, no disc (panel d); four_lumbar = four rib-free bodies and a", "#333333", "normal", 7)
    add("free S1 with a disc. No ribs or no sacrum in the field -> cannot_verify, never 'probably'.", "#333333", "normal", 7)
    y = 0.995
    for t, c, w, s in L:
        width = max(40, int(86 * 7.5 / s))                    # the column holds ~86 monospace characters at 7.5 pt
        for line in (wrap(t, width) if len(t) > width else [t]):
            ax_g.text(0.0, y, line, color=c, fontweight=w, fontsize=s, family="monospace", va="top", ha="left",
                      transform=ax_g.transAxes)
            y -= 0.0168 * (s / 8.6) + 0.002
    fig.suptitle(f"Truth verification -- {row['person']} -- proposed {row['subtype']} -- for a HUMAN reader; nothing on "
                 f"this page is truth", fontsize=11, y=0.995)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=100, pil_kwargs={"quality": 88, "optimize": True})
    plt.close(fig)


FLAG_TEXT = {
    "L6_no_L1": "L6 was called with NO L1 in the field: the count behind the call cannot be made from this volume "
                "(the screen types the same field 'unreadable' when no 25 is named).",
    "T13_only_L1_L4": "T13 was called with only L1-L4 named above the sacrum: 13 + 4 = 17 thoracolumbar bodies, the "
                      "ordinary count -- a naming shift at the thoracolumbar junction, not an extra vertebra.",
    "T12_skip": "VERIDAH skipped T12 (its names above L1 are one level off): the thoracic names on this page carry "
                "that skip.",
    "four_lumbar_candidate": "four lumbar bodies named between a thoracic vertebra and the sacrum: is the fourth "
                             "free of the sacrum (panel d), and is the body above it rib-bearing?",
    "carm_L6_contested": "the two CBCT labellers disagree on EVERY lumbar name (TotalSegmentator L1-L5, VERIDAH "
                         "L2-L6); neither saw a rib; stratify.json's 'verified: true' is wrong (stratify_corrections.json).",
}


def wrap(t, n):
    out, cur = [], ""
    for w in t.split():
        if len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out or [""]


def cmd_render(a) -> int:
    out = Path(a.out)
    rows = jload(out / "worklist.json")
    if a.cases:
        want = {c for c in a.cases.replace("+", ",").replace(" ", ",").split(",") if c}   # sbatch --export splits on ','
        rows = [r for r in rows if r["case"] in want or r["person"] in want]
    rows = [r for i, r in enumerate(rows) if i % a.n_shards == a.shard]
    log(f"render shard {a.shard}/{a.n_shards}: {len(rows)} persons")
    n_ok = n_fail = n_skip = 0
    for r in rows:
        page = out / r["page"]
        aj = out / "auto" / f"{r['corpus']}_{r['case']}.json"
        if page.exists() and aj.exists() and not a.force:
            n_skip += 1; continue
        t0 = time.time()
        try:
            inp = find_inputs(r)
            if not inp.get("mask") or not Path(inp["mask"]).exists():
                raise FileNotFoundError(f"no SPINEPS instance mask for {r['person']}")
            R, ctx = analyse(r, inp)
            render(r, R, ctx, page)
            R.update(person=r["person"], order=r["order"], tier=r["tier"], proposed_subtype=r["subtype"],
                     flags=r["flags"], frames=r["frames"], page=r["page"], seconds=round(time.time() - t0, 1))
            aj.parent.mkdir(parents=True, exist_ok=True)
            json.dump(R, open(aj, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
            log(f"{r['order']:03d} {r['person']}: ok ({R['seconds']}s) positions={[p['pos'] for p in R['positions']]} "
                f"ribs={R['rib_bearing_positions']} lowest_auto={R['lowest_rib_bearing_pos_auto']}")
            n_ok += 1
        except Exception as e:  # noqa: BLE001 -- the failure is recorded per person and the run goes on
            n_fail += 1
            (out / "auto").mkdir(parents=True, exist_ok=True)
            json.dump({"person": r["person"], "order": r["order"], "error": repr(e)[:800],
                       "trace": traceback.format_exc()[-3000:]}, open(out / "auto" / f"FAILED_{r['corpus']}_{r['case']}.json", "w"), indent=1)
            log(f"{r['order']:03d} {r['person']}: FAILED {repr(e)[:300]}")
    log(f"shard {a.shard}: ok {n_ok}, failed {n_fail}, skipped {n_skip}")
    return 0


def cmd_index(a) -> int:
    out = Path(a.out)
    rows = jload(out / "worklist.json")
    done = failed = 0
    parts = ["<html><head><meta charset='utf-8'><title>Truth verification worklist</title>",
             "<style>body{font-family:sans-serif;font-size:13px} table{border-collapse:collapse} td,th{border:1px solid #ccc;padding:3px 6px} "
             ".t1{background:#ffe9e9} .t2{background:#eef7ee} .t3{background:#f3f3f3}</style></head><body>",
             "<h2>Human truth verification -- real-frame G3 test persons (LEVELCHECK_MODEL.md s4)</h2>",
             "<p>Open each page, then fill the row in <b>truth_to_fill.csv</b>. Tier 1 = transitional calls (problems first), "
             "tier 2 = ordinary, tier 3 = no exported real frame (verify last). Nothing on a page is truth.</p>",
             "<table><tr><th>order</th><th>tier</th><th>person</th><th>proposed subtype</th><th>flags</th><th>real frame</th><th>page</th><th>auto</th></tr>"]
    for r in rows:
        page = out / r["page"]
        ok = page.exists()
        done += ok
        fj = out / "auto" / f"FAILED_{r['corpus']}_{r['case']}.json"
        failed += fj.exists() and not ok
        link = ('<a href="%s">page</a>' % r["page"]) if ok else ("FAILED" if fj.exists() else "pending")
        parts.append("<tr class='t%d'><td>%03d</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
                     "<td><a href='auto/%s_%s.json'>json</a></td></tr>"
                     % (r["tier"], r["order"], r["tier"], r["person"], r["subtype"], "+".join(r["flags"]),
                        "yes" if r["frames"] else "no", link, r["corpus"], r["case"]))
    parts.append("</table></body></html>")
    (out / "index.html").write_text("\n".join(parts), encoding="utf-8")
    summ = {"persons": len(rows), "pages": done, "failed": failed, "written": time.strftime("%Y-%m-%dT%H:%M:%S")}
    json.dump(summ, open(out / "RENDER_STATUS.json", "w"), indent=1)
    log(f"index: {summ}")
    return 0


def cmd_freeze(a) -> int:
    """Validate a HUMAN-filled copy of truth_to_fill.csv and write the frozen truth with its SHA-256."""
    out = Path(a.out)
    src = Path(a.csv)
    rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
    problems, frozen = [], []
    for r in rows:
        o = r.get("order", "?")
        conf = (r.get("subtype_confirmed") or "").strip().upper()
        corr = (r.get("subtype_corrected") or "").strip()
        lrb = (r.get("lowest_rib_bearing_body") or "").strip()
        nl = (r.get("n_lumbar_bodies") or "").strip()
        ini = (r.get("reader_initials") or "").strip()
        tier = int(r.get("tier") or 3)
        filled = bool(conf or corr or lrb or nl or ini)
        if not filled:
            if tier < 3:
                problems.append(f"row {o} {r.get('person')}: tier {tier} not read")
            continue
        if conf not in ("Y", "N"):
            problems.append(f"row {o}: subtype_confirmed must be Y or N (got '{conf}')")
        final = r.get("proposed_subtype") if conf == "Y" and not corr else corr
        if final not in SUBTYPES:
            problems.append(f"row {o}: subtype '{final}' not in {SUBTYPES}")
        if not ini:
            problems.append(f"row {o}: reader_initials empty")
        names = ""
        if nl:
            try:
                k = int(nl)
                names = ",".join(f"L{i}" for i in range(1, k + 1))
            except ValueError:
                problems.append(f"row {o}: n_lumbar_bodies must be an integer")
        if lrb and not (lrb.startswith("P") or lrb == "not_in_field"):
            problems.append(f"row {o}: lowest_rib_bearing_body must be a P-label or not_in_field")
        frozen.append({**{k: r.get(k, "") for k in ID_COLS}, "subtype_final": final,
                       "lowest_rib_bearing_body": lrb, "n_lumbar_bodies": nl,
                       "lumbar_names_derived": names, "lumbar_names_reader": r.get("lumbar_names_top_to_bottom", ""),
                       "sacrum_in_field": r.get("sacrum_in_field", ""), "lowest_rib_in_field": r.get("lowest_rib_in_field", ""),
                       "reader_initials": ini, "read_date": r.get("read_date", ""), "notes": r.get("notes", "")})
    if problems and not a.allow_incomplete:
        for p in problems[:60]:
            print("PROBLEM:", p)
        print(f"{len(problems)} problems; nothing frozen (use --allow-incomplete to freeze the rows that are complete)")
        return 1
    fp = out / "truth_frozen.csv"
    with open(fp, "w", newline="") as f:
        w = csv.DictWriter(f, list(frozen[0]) if frozen else ID_COLS)
        w.writeheader(); w.writerows(frozen)
    h = sha256(fp)
    (out / "truth_frozen.sha256").write_text(f"{h}  truth_frozen.csv\n")
    json.dump({"frozen_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "source_csv": str(src), "source_sha256": sha256(src),
               "truth_frozen_sha256": h, "rows": len(frozen), "problems": problems,
               "readers": sorted({r["reader_initials"] for r in frozen})}, open(out / "truth_frozen.json", "w"), indent=1)
    print(f"frozen {len(frozen)} rows -> {fp}  sha256 {h}  ({len(problems)} problems recorded)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "render", "index", "freeze"])
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--cases", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--csv", default="")
    ap.add_argument("--allow-incomplete", action="store_true")
    a = ap.parse_args()
    return {"build": cmd_build, "render": cmd_render, "index": cmd_index, "freeze": cmd_freeze}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
