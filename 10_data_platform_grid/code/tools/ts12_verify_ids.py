#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ts12_verify_ids.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Adversarial check of the TS12 subtype finding (2026-09-23): are the bench_ts SPINEPS seg-vert ids really
scrambled, is the ctd-based relabel right, and does a count that uses NO VERIDAH output agree with the ctd subtype?

Per case (one TotalSegmentator subject):
  A. native seg-vert mask: per-id centroid (world mm), voxels, components; is id order S-I monotonic?
  B. POI-in-mask: each ctd POI (label -> corpus point "50", voxel coords of the ctd grid) is taken to world mm and
     looked up IN the mask -- the instance that physically contains the POI. This does not use z rank at all, so it
     checks tools/rare_class_ts_fixids.py (z-rank alignment) independently: (i) native id at each POI vs the
     fixids pair (old_id -> new name); (ii) the staged, relabelled mask must read the POI's own label at the POI.
  C. independent count, NO VERIDAH output: SPINEPS INSTANCES as objects in S-I order from the top (their relabelled
     names are reported beside them, never used to count) and the TotalSegmentator GT objects of the same CT (names
     reported; a TS object holding two SPINEPS instances is a TS merge -- TS has only 24 presacral names, so a 25th
     vertebra shows up as a merge or as a free "S1"). Every TS rib label is one object, attached by its MEDIAL END
     (100 voxels nearest the spine) to the nearest instance with no distance cap: the TS rib masks stop 10-20 mm
     short of the costovertebral joint (first-pass renders), so a contact rule silently drops ribs.
        cervical = instances above the highest rib-bearing one; thoracic = highest..lowest rib-bearing span;
        lumbar-type = instances below the lowest rib-bearing one (is the lowest free? HU profile + rendered slice)
     A CT field of view that ends in the upper sacrum is flagged: there S1 free-vs-fused cannot be read.
  E. ribs counted from the CT itself: bone (HU >= 200) in no TotalSegmentator label except the ribs and not touching
     a SPINEPS instance; components beside the spine are attached through bone to the instance they reach. This
     sees a rib TS did not label (TS has 12 rib names per side, so a 13th rib cannot be in its GT under its own name).
  D. renders (coronal MIP over the spine slab + mid-sagittal slab) with the relabelled names on the patient's right
     and the TS names on the left, TS ribs outlined with their medial-end attachment -- whole spine, a
     thoracolumbar-to-sacrum zoom, a full-resolution lumbosacral sagittal (<case>_ls.png), and axial MIPs over
     each decisive vertebra's body (_axial.png) and transverse-process level (_axial_tp.png).

    python tools/ts12_verify_ids.py --subject s1089 --out <dir>
Outputs <dir>/TS_<s>_verify.json, _full.png, _zoom.png, _ls.png.
Volumes are canonicalised to RAS for ANALYSIS only; nothing is written back.
"""
import argparse, json, os, sys
import numpy as np
import nibabel as nib
from nibabel.processing import resample_from_to
from scipy import ndimage
from scipy.spatial import cKDTree

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "SAC", 28: "T13"}
TS_VERT = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + [f"L{i}" for i in range(1, 6)]
TS_CODE = {n: i + 1 for i, n in enumerate(TS_VERT)}          # C1=1 .. L5=24 (names kept for REPORTING only)
TS_CODE["S1"] = 50
TS_CODE["sacrum"] = 26
TS_NAME = {v: k for k, v in TS_CODE.items()}

def world_of(aff, ijk):
    ijk = np.atleast_2d(np.asarray(ijk, float))
    return ijk @ aff[:3, :3].T + aff[:3, 3]


def on_grid(img, ref):
    """img resampled (nearest) onto the canonical reference grid; exact reorientation when grids coincide."""
    c = nib.as_closest_canonical(img)
    if c.shape == ref.shape and np.allclose(c.affine, ref.affine, atol=1e-3):
        return np.asanyarray(c.dataobj)
    return np.asanyarray(resample_from_to(img, (ref.shape, ref.affine), order=0).dataobj)


def poi_world(ctd_path):
    d = json.load(open(ctd_path))
    meta, pts = d[0], d[-1]
    A = np.eye(4)
    A[:3, :3] = np.asarray(meta["rotation"], float) * np.asarray(meta["zoom"], float)[None, :]
    A[:3, 3] = np.asarray(meta["origin"], float)
    out = {}
    for k, v in pts.items():
        c = v.get("50") or next(iter(v.values()))
        out[int(k)] = (A @ np.r_[np.asarray(c, float), 1.0])[:3]
    return out, meta


def lookup(arr, aff, w, rad=3):
    """instance at world point w (majority within +-rad voxels if the point itself is background)."""
    ix = np.round(np.linalg.inv(aff) @ np.r_[w, 1.0])[:3].astype(int)
    if (ix < 0).any() or (ix >= np.array(arr.shape)).any():
        return None, "outside"
    v = int(arr[tuple(ix)])
    if v:
        return v, "at"
    lo = np.clip(ix - rad, 0, None); hi = np.minimum(ix + rad + 1, arr.shape)
    win = arr[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    u, n = np.unique(win[win > 0], return_counts=True)
    return (int(u[np.argmax(n)]), "near") if len(u) else (0, "none")


def objects(lab, aff, min_vox=1):
    """per-label voxel coords (world), centroid, extent, components."""
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
        w = world_of(aff, idx)
        cc, ncc = ndimage.label(sub, structure=np.ones((3, 3, 3)))
        sizes = np.bincount(cc.ravel())[1:] if ncc else np.array([])
        out[l] = dict(vox=n, centroid=w.mean(0), zmin=float(w[:, 2].min()), zmax=float(w[:, 2].max()),
                      xyz=w, idx=idx, n_comp=int((sizes >= max(50, 0.05 * n)).sum()),
                      comp_sizes=sorted((int(x) for x in sizes), reverse=True)[:4])
    return out


def bone_path_attach(rib_idx, hu, sarr, tsr, rc, axis_xy_at, Ac, thr=150.0, max_it=30):
    """Grow from the medial 15 mm of a TS rib mask through bone (HU >= thr, not another TS rib, not a vertebra)
    until the growing front touches a SPINEPS instance; the first instance touched is the one the rib reaches
    through bone. TS rib masks stop short of the costovertebral joint, so the nearest-voxel rule is biased by a
    level for the steep lower ribs; the bone path follows the rib itself. Returns (instance, steps, how)."""
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
    allowed = (H >= thr) & ~O & (S == 0)
    st = np.ones((3, 3, 3), bool)
    front = seed.copy(); visited = seed.copy()
    for it in range(max_it):
        ring = ndimage.binary_dilation(front, structure=st)
        touch = ring & (S > 0) & (S != 26)
        if touch.any():
            v, n = np.unique(S[touch], return_counts=True)
            return int(v[np.argmax(n)]), it, "bone"
        front = ring & allowed & ~visited
        if not front.any():
            break
        visited |= front
    # stalled (joint space wider than a voxel, or osteopenic head): nearest instance to everything reached
    reach = np.argwhere(visited)
    inst_pts = np.argwhere((S > 0) & (S != 26))
    if len(inst_pts) == 0:
        return None, it, "none"
    t = cKDTree(inst_pts)
    d, j = t.query(reach[:: max(1, len(reach) // 3000)], k=1)
    k = int(np.argmin(d))
    ip = inst_pts[j[k]]
    return int(S[tuple(ip)]), it, f"nearest-after-stall({d[k] * float(np.abs(Ac[0, 0])):.1f}mm)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ts_root", default=os.path.expanduser("~/data/TotalSegmentator"))
    ap.add_argument("--native", default=os.path.expanduser("~/bench_ts/spineps/native"))
    ap.add_argument("--stage", default="/rs/rs_grp_oschome/go2432/data/rare_class/ts_stage")
    ap.add_argument("--no_render", action="store_true")
    a = ap.parse_args()
    s = a.subject
    cid = f"TS_{s}"
    os.makedirs(a.out, exist_ok=True)
    R = {"case": cid}

    # ---------------- A. native mask ----------------
    nimg = nib.load(f"{a.native}/{cid}_seg-vert_msk.nii.gz")
    narr = np.asanyarray(nimg.dataobj).astype(np.int16)
    R["native_axcodes"] = "".join(nib.aff2axcodes(nimg.affine))
    nobj = objects(narr, nimg.affine)
    order = sorted(nobj, key=lambda l: -nobj[l]["centroid"][2])
    R["native_ids_top_down"] = [dict(id=l, z=round(float(nobj[l]["centroid"][2]), 1), vox=nobj[l]["vox"],
                                     n_comp=nobj[l]["n_comp"]) for l in order]
    seq = [l for l in order if l not in (26, 28)]
    disc = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq)) if seq[i] > seq[j])
    npair = len(seq) * (len(seq) - 1) // 2
    R["native_monotonic"] = disc == 0
    R["native_discordant_pair_frac"] = round(disc / max(npair, 1), 3)

    # ---------------- B. POI-in-mask ----------------
    P, meta = poi_world(f"{a.native}/{cid}_ctd.json")
    fixp = f"{a.stage}/{cid}/subtype_fix.json"
    fix = json.load(open(fixp)) if os.path.exists(fixp) else None
    fix_old_of = {p["new_id"]: p["old_id"] for p in fix["pairs"]} if fix else {}
    simg = nib.load(f"{a.stage}/{cid}/{cid}_msk.nii.gz")
    sarr = np.asanyarray(simg.dataobj).astype(np.int16)
    rows = []
    for L in sorted(P, key=lambda k: -P[k][2]):
        w = P[L]
        nid, nhow = lookup(narr, nimg.affine, w)
        sid, show = lookup(sarr, simg.affine, w)
        # LPS alternative, to show which world convention the POI file uses
        wl = np.array([-w[0], -w[1], w[2]])
        nid_lps, _ = lookup(narr, nimg.affine, wl)
        rows.append(dict(poi=VERSE.get(L, L), poi_id=L, z=round(float(w[2]), 1),
                         native_id=nid, native_how=nhow, native_id_if_lps=nid_lps,
                         native_id_equals_label=(nid == L),
                         fix_old_id=fix_old_of.get(L), fix_agrees=(fix_old_of.get(L) == nid) if L in fix_old_of else None,
                         staged_label=sid, staged_how=show, staged_ok=(sid == L)))
    R["poi_rows"] = rows
    R["poi_in_native_hits"] = sum(1 for r in rows if r["native_id"] not in (None, 0))
    R["poi_in_native_hits_if_lps"] = sum(1 for r in rows if r["native_id_if_lps"] not in (None, 0))
    R["native_id_equals_poi_label"] = sum(1 for r in rows if r["native_id_equals_label"])
    R["n_poi"] = len(rows)
    R["fix_pairs_confirmed_by_poi_lookup"] = sum(1 for r in rows if r["fix_agrees"])
    R["fix_pairs_contradicted_by_poi_lookup"] = [r["poi"] for r in rows if r["fix_agrees"] is False]
    R["staged_label_at_poi_ok"] = sum(1 for r in rows if r["staged_ok"])
    R["staged_label_at_poi_bad"] = [(r["poi"], r["staged_label"]) for r in rows if not r["staged_ok"]]
    # one native id taking two POIs would be a merged instance
    taken = {}
    for r in rows:
        if r["native_id"]:
            taken.setdefault(r["native_id"], []).append(r["poi"])
    R["native_ids_holding_two_pois"] = {str(k): v for k, v in taken.items() if len(v) > 1}
    if fix:
        R["fix_report"] = dict(subtype=fix["subtype"], c1_added=fix.get("c1_added"),
                               sacrum_poi_dropped=fix.get("sacrum_poi_dropped"),
                               max_dz_vertebra=max(p["dz_mm"] for p in fix["pairs"] if p["new_id"] != 26),
                               dz_sacrum=[p["dz_mm"] for p in fix["pairs"] if p["new_id"] == 26],
                               sacrum_instance_vox=[p["vox"] for p in fix["pairs"] if p["new_id"] == 26])
    # margin of the z-rank match: for each fixids pair, |dz| to its own POI vs to the nearest OTHER POI
    if fix:
        pz = {k: v[2] for k, v in P.items()}
        marg = []
        for p in fix["pairs"]:
            zi = nobj[p["old_id"]]["centroid"][2]
            own = abs(zi - pz[p["new_id"]])
            other = min(abs(zi - z) for k, z in pz.items() if k != p["new_id"])
            marg.append(dict(name=p["name"], own=round(own, 1), nearest_other=round(other, 1)))
        R["zrank_margin"] = marg
        R["zrank_pairs_nearer_another_poi"] = [m["name"] for m in marg if m["nearest_other"] < m["own"]]

    # ---------------- C. independent count (no VERIDAH output) ----------------
    # Objects only: SPINEPS INSTANCES (the instance model's bodies, taken in S-I order from the top; the VERIDAH names
    # the staged mask carries are reported beside them, never used to count) and TotalSegmentator GT objects (names
    # reported; a TS object that holds two SPINEPS instances is a TS merge -- TS has only 24 presacral names).
    # Ribs: every TS rib label is one object; it is attached by its MEDIAL END (the 100 rib voxels nearest the
    # spine) to the nearest vertebra object, no distance cap -- the TS rib masks stop 10-20 mm short of the
    # costovertebral joint (seen in the first-pass renders), so a contact rule drops ribs.
    ct = nib.load(f"{a.ts_root}/{s}/ct.nii.gz")
    ctc = nib.as_closest_canonical(ct)
    Ac = ctc.affine
    R["ct_shape"] = list(ctc.shape); R["ct_zooms"] = [round(float(z), 3) for z in ctc.header.get_zooms()[:3]]
    zc = world_of(Ac, [[0, 0, 0], [0, 0, ctc.shape[2] - 1]])[:, 2]
    R["ct_z_range_mm"] = [round(float(zc.min()), 1), round(float(zc.max()), 1)]
    seg = f"{a.ts_root}/{s}/segmentations"
    tsv = np.zeros(ctc.shape, np.int16)
    for n, code in TS_CODE.items():
        p = f"{seg}/{'sacrum' if n == 'sacrum' else 'vertebrae_' + n}.nii.gz"
        if os.path.exists(p):
            tsv[on_grid(nib.load(p), ctc) > 0] = code
    tsr = np.zeros(ctc.shape, np.int16)
    for side, sc in (("left", 100), ("right", 200)):
        for k in range(1, 13):
            p = f"{seg}/rib_{side}_{k}.nii.gz"
            if os.path.exists(p):
                tsr[on_grid(nib.load(p), ctc) > 0] = sc + k
    sarr_c = on_grid(simg, ctc).astype(np.int16)

    tobj = objects(tsv, Ac, min_vox=200)
    sobj = objects(sarr_c, Ac, min_vox=50)
    robj = objects(tsr, Ac, min_vox=100)
    inst = sorted([c for c in sobj if c != 26], key=lambda c: -sobj[c]["centroid"][2])       # SPINEPS, top-down
    tcodes = sorted([c for c in tobj if c != 26], key=lambda c: -tobj[c]["centroid"][2])     # TS, top-down
    R["ts_C1_present"] = 1 in tobj
    R["ts_sacrum_present"] = 26 in tobj
    zmin_ct = float(zc.min())
    R["fov_bottom_cuts_sacrum"] = bool(26 in tobj and tobj[26]["zmin"] - zmin_ct < 4.0)
    R["fov_bottom_cuts_lowest_instance"] = bool(sobj[inst[-1]]["zmin"] - zmin_ct < 4.0)

    # TS object <-> SPINEPS instance overlap (merges / splits)
    hold = {}
    for c in list(tcodes) + ([26] if 26 in tobj else []):
        vals, cnt = np.unique(sarr_c[tsv == c], return_counts=True)
        hold[c] = [(int(v), round(float(n) / sobj[int(v)]["vox"], 2)) for v, n in zip(vals, cnt)
                   if v and int(v) in sobj and n / sobj[int(v)]["vox"] >= 0.3]
    R["ts_objects"] = [dict(ts_name=TS_NAME[c], z=round(float(tobj[c]["centroid"][2]), 1), vox=tobj[c]["vox"],
                            n_comp=tobj[c]["n_comp"],
                            holds_spineps=[f"{VERSE.get(v, v)}({f})" for v, f in hold.get(c, [])])
                       for c in tcodes + ([26] if 26 in tobj else [])]
    R["ts_merges"] = [f"TS {TS_NAME[c]} holds {[VERSE.get(v, v) for v, _ in hold[c]]}" for c in tcodes if len(hold.get(c, [])) > 1]
    R["ts_names_out_of_order"] = [TS_NAME[c] for i, c in enumerate(tcodes) if i and c < tcodes[i - 1] and c != 50]

    # ribs -> vertebra objects by medial end
    spts = np.concatenate([sobj[c]["xyz"] for c in inst]); sown = np.concatenate([np.full(sobj[c]["vox"], c) for c in inst])
    tpts = np.concatenate([tobj[c]["xyz"] for c in tcodes]); town = np.concatenate([np.full(tobj[c]["vox"], c) for c in tcodes])
    stree, ttree = cKDTree(spts), cKDTree(tpts)
    bc = np.array([sobj[c]["xyz"][sobj[c]["xyz"][:, 1] >= np.median(sobj[c]["xyz"][:, 1])].mean(0) for c in inst])
    zo = np.argsort(bc[:, 2])

    def axis_xy_at(z):
        return np.interp(z, bc[zo, 2], bc[zo, 0]), np.interp(z, bc[zo, 2], bc[zo, 1])

    hu = np.asanyarray(ctc.dataobj).astype(np.float32)
    ribs = []
    for rc in sorted(robj):
        xyz = robj[rc]["xyz"]
        bp, bsteps, bhow = bone_path_attach(robj[rc]["idx"], hu, sarr_c, tsr, rc, axis_xy_at, Ac)
        d, j = stree.query(xyz, k=1)
        m = np.argsort(d)[:100]
        v, n = np.unique(sown[j[m]], return_counts=True)
        best = int(v[np.argmax(n)])
        d2, j2 = ttree.query(xyz[m], k=1)
        v2, n2 = np.unique(town[j2], return_counts=True)
        tbest = int(v2[np.argmax(n2)])
        ribs.append(dict(ts_rib=f"rib_{'left' if rc < 200 else 'right'}_{rc % 100}", side="left" if rc < 200 else "right",
                         vox=robj[rc]["vox"], medial_gap_mm=round(float(np.median(d[m])), 1),
                         medial_xyz=[round(float(x), 1) for x in xyz[m].mean(0)],
                         instance_index=inst.index(best) + 1, instance_veridah_name=VERSE.get(best, best),
                         votes={VERSE.get(int(a_), a_): int(b_) for a_, b_ in zip(v, n)},
                         ts_object=TS_NAME[tbest],
                         bone_path_instance_index=(inst.index(bp) + 1) if bp in inst else None,
                         bone_path_veridah_name=VERSE.get(bp, bp) if bp else None, bone_path_steps=bsteps, bone_path_how=bhow))
    R["ribs"] = ribs
    ok = [r for r in ribs if r["medial_gap_mm"] <= 25.0]
    R["ribs_far_from_spine"] = [(r["ts_rib"], r["medial_gap_mm"]) for r in ribs if r["medial_gap_mm"] > 25.0]
    R["rib_objects_per_side"] = {sd: sum(1 for r in ok if r["side"] == sd) for sd in ("left", "right")}
    for r in ribs:
        r["attach_index"] = r["bone_path_instance_index"] if (r["bone_path_how"] == "bone" and r["bone_path_instance_index"]) else r["instance_index"]
        r["attach_rule"] = "bone_path" if r["attach_index"] == r["bone_path_instance_index"] and r["bone_path_how"] == "bone" else "medial_end"
    R["rib_rules_disagree"] = [(r["ts_rib"], r["instance_veridah_name"], r["bone_path_veridah_name"], r["bone_path_how"])
                               for r in ribs if r["bone_path_instance_index"] != r["instance_index"]]
    if ok:
        h = min(r["attach_index"] for r in ok); l = max(r["attach_index"] for r in ok)
        R["rib_bearing_instance_indices"] = sorted({r["attach_index"] for r in ok})
        R["count_cervical"] = h - 1
        R["count_thoracic_span"] = l - h + 1
        below = inst[l:]                                     # instances strictly below the lowest rib-bearing one
        R["instances_below_lowest_rib"] = [VERSE.get(c, c) for c in below]
        R["count_lumbar_type"] = len(below)
        R["count_presacral"] = len(inst)
        R["lowest_rib_on_instance"] = dict(index=l, veridah_name=VERSE.get(inst[l - 1], inst[l - 1]),
                                           ribs=[(r["ts_rib"], r["attach_rule"]) for r in ok if r["attach_index"] == l],
                                           ts_object=sorted({r["ts_object"] for r in ok if r["attach_index"] == l}))
        R["highest_rib_on_instance"] = dict(index=h, veridah_name=VERSE.get(inst[h - 1], inst[h - 1]),
                                            ribs=[(r["ts_rib"], r["attach_rule"]) for r in ok if r["attach_index"] == h])
        # which TS object the lowest SPINEPS instance lives in (TS calls a 25th presacral vertebra "S1")
        lo = inst[-1]
        vals, cnt = np.unique(tsv[sarr_c == lo], return_counts=True)
        R["lowest_instance_in_ts"] = {TS_NAME.get(int(v_), str(v_)): round(float(c_) / sobj[lo]["vox"], 2) for v_, c_ in zip(vals, cnt) if v_}

    # HU profile across the joint below each of the lowest two instances: body centroid (anterior half) to the
    # body below (next instance, else TS S1 if it is not the same bone, else TS sacrum); a disc is a dip between
    # two end-plate peaks. Reported for the reader; the verdict is taken from the rendered slice.
    Ainv = np.linalg.inv(Ac)

    def body(xyz):
        return xyz[xyz[:, 1] >= np.median(xyz[:, 1])].mean(0)

    def profile(p0, p1, r=5.0, step=0.5):
        v = p1 - p0; L = float(np.linalg.norm(v)); u = v / L
        e = np.cross(u, [1.0, 0, 0]); e = e if np.linalg.norm(e) > 1e-3 else np.cross(u, [0, 1.0, 0]); e /= np.linalg.norm(e)
        f = np.cross(u, e)
        offs = [(0.0, 0.0)] + [(rr * np.cos(t), rr * np.sin(t)) for rr in (r / 2, r) for t in np.linspace(0, 2 * np.pi, 8, endpoint=False)]
        ts_ = np.arange(0, L + step, step)
        pts_ = np.array([[p0 + t * u + ox * e + oy * f for ox, oy in offs] for t in ts_])      # (T, K, 3)
        ijk = (pts_.reshape(-1, 3) @ Ainv[:3, :3].T + Ainv[:3, 3]).T
        vals_ = ndimage.map_coordinates(hu, ijk, order=1, mode="nearest").reshape(len(ts_), len(offs)).mean(1)
        return ts_, vals_

    joints = []
    cand = inst[-2:]
    for c in cand:
        i = inst.index(c)
        p0 = body(sobj[c]["xyz"])
        if i + 1 < len(inst):
            p1, what = body(sobj[inst[i + 1]]["xyz"]), VERSE.get(inst[i + 1], inst[i + 1])
        else:
            ts_here = R.get("lowest_instance_in_ts", {})
            if 50 in tobj and ts_here.get("S1", 0) < 0.5:
                p1, what = body(tobj[50]["xyz"]), "TS S1"
            elif 26 in tobj:
                sac = tobj[26]["xyz"]
                top = sac[sac[:, 2] >= np.percentile(sac[:, 2], 75)]
                p1, what = body(top), "TS sacrum (upper quarter)"
            else:
                continue
        t_, pr = profile(p0, p1)
        mid = (t_ > 0.2 * t_[-1]) & (t_ < 0.8 * t_[-1])
        k = int(np.argmin(np.where(mid, pr, np.inf)))
        pk_up = float(pr[:k + 1].max()) if k > 0 else float(pr[0])
        pk_dn = float(pr[k:].max())
        joints.append(dict(upper=VERSE.get(c, c), lower=what, length_mm=round(float(t_[-1]), 1),
                           min_hu_mid=round(float(pr[k]), 0), at_mm=round(float(t_[k]), 1),
                           peak_above=round(pk_up, 0), peak_below=round(pk_dn, 0),
                           dip_contrast=round(min(pk_up, pk_dn) - float(pr[k]), 0),
                           profile_hu=[int(x) for x in pr[:: 2]]))
    R["lowest_joints"] = joints

    # ---------------- E. ribs counted from the CT itself ----------------
    # Bone (HU >= 200) that is in NO TotalSegmentator label except the ribs (so organs, vessels with contrast,
    # scapulae, clavicles, sternum, costal cartilage, pelvis are gone) and not in or touching a SPINEPS instance.
    # What is left beside the spine is ribs -- whether or not TS labelled them. Each component whose medial end lies
    # within 40 mm of the spinal axis is attached through bone to the instance it reaches (bone_path_attach).
    nonrib = np.zeros(ctc.shape, bool)
    for f in sorted(os.listdir(seg)):
        if f.endswith(".nii.gz") and not f.startswith("rib_"):
            nonrib |= on_grid(nib.load(f"{seg}/{f}"), ctc) > 0
    cand = (hu >= 200) & ~ndimage.binary_dilation(nonrib, iterations=1) & ~ndimage.binary_dilation(sarr_c > 0, iterations=1)
    del nonrib
    lab_c, ncomp = ndimage.label(cand, structure=np.ones((3, 3, 3)))
    del cand
    comps = []
    sizes = np.bincount(lab_c.ravel())
    for k in np.nonzero(sizes >= 60)[0]:
        if k == 0:
            continue
        comps.append(int(k))
    objs_c = ndimage.find_objects(lab_c)
    ct_ribs = []
    for k in comps:
        s_k = objs_c[k - 1]
        idx = np.argwhere(lab_c[s_k] == k) + np.array([x.start for x in s_k])
        w = world_of(Ac, idx)
        axx, axy = axis_xy_at(w[:, 2])
        rh = np.hypot(w[:, 0] - axx, w[:, 1] - axy)
        if rh.min() > 45.0 or rh.max() - rh.min() < 15.0:
            continue
        if w[:, 2].max() < sobj[inst[-1]]["zmin"]:
            continue                                       # below the spine: pelvis leftovers
        side = "right" if np.median(w[:, 0] - axx) > 0 else "left"
        # one component can hold two ribs if they touch (callus, calcified cartilage): count medial ends
        bp, steps, how = bone_path_attach(idx, hu, sarr_c, tsr, -1, axis_xy_at, Ac)
        tsfrac = float((tsr[tuple(idx.T)] > 0).mean())
        ct_ribs.append(dict(side=side, vox=int(len(idx)), medial_mm=round(float(rh.min()), 1), reach_mm=round(float(rh.max()), 1),
                            z_medial=round(float(w[np.argmin(rh), 2]), 1),
                            instance_index=(inst.index(bp) + 1) if bp in inst else None,
                            veridah_name=VERSE.get(bp, bp) if bp else None, how=how, ts_rib_fraction=round(tsfrac, 2)))
    del lab_c
    ct_ribs.sort(key=lambda r: (r["side"], -r["z_medial"]))
    R["ct_rib_components"] = ct_ribs
    long_ = [r for r in ct_ribs if r["reach_mm"] - r["medial_mm"] >= 40.0 and r["how"] == "bone"]
    R["ct_ribs_per_instance"] = {}
    for r in long_:
        key = f"#{r['instance_index']} {r['veridah_name']}"
        R["ct_ribs_per_instance"].setdefault(key, []).append(r["side"][0].upper())
    R["ct_rib_instances"] = sorted({r["instance_index"] for r in long_ if r["instance_index"]})
    R["ct_ribs_short_or_unattached"] = [r for r in ct_ribs if r not in long_]

    # ctd subtype vs the object count
    labs = set(P)
    R["ctd_subtype"] = "L6" if 25 in labs else ("T13" if 28 in labs else "none")
    R["ctd_counts"] = dict(thoracic=sum(1 for l in labs if 8 <= l <= 19) + (1 if 28 in labs else 0),
                           lumbar=sum(1 for l in labs if 20 <= l <= 25))
    cv, th, lu = R.get("count_cervical"), R.get("count_thoracic_span"), R.get("count_lumbar_type")
    ind = {(7, 12, 5): "none", (7, 13, 5): "T13", (7, 12, 6): "L6"}.get((cv, th, lu), f"C{cv}/T{th}/L{lu}")
    R["independent_subtype_if_lowest_instance_free"] = ind
    R["independent_counts"] = dict(cervical=cv, thoracic_span=th, lumbar_type=lu, presacral=R.get("count_presacral"))
    json.dump(R, open(f"{a.out}/{cid}_verify.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print(f"TS12V {cid} ctd={R['ctd_subtype']} {R['ctd_counts']} objects={R['independent_counts']} -> {ind} "
          f"lowest_rib={R.get('lowest_rib_on_instance')} highest_rib={R.get('highest_rib_on_instance')} "
          f"ribs/side={R['rib_objects_per_side']} far={R['ribs_far_from_spine']} rules_disagree={R['rib_rules_disagree']} ts_merges={R['ts_merges']} "
          f"lowest_inst_in_ts={R.get('lowest_instance_in_ts')} fov_cut_sac={R['fov_bottom_cuts_sacrum']} "
          f"CT_RIBS instances={R['ct_rib_instances']} per_instance={R['ct_ribs_per_instance']} "
          f"fov_cut_lowest={R['fov_bottom_cuts_lowest_instance']} joints={[(j['upper'], j['lower'], j['min_hu_mid'], j['dip_contrast']) for j in joints]} "
          f"| native_monotonic={R['native_monotonic']} poi->native_equal={R['native_id_equals_poi_label']}/{R['n_poi']} "
          f"fix_confirmed={R['fix_pairs_confirmed_by_poi_lookup']} contradicted={R['fix_pairs_contradicted_by_poi_lookup']} "
          f"staged_ok={R['staged_label_at_poi_ok']}/{R['n_poi']} bad={R['staged_label_at_poi_bad']}", flush=True)
    if not a.no_render:
        render(R, cid, ctc, hu, sarr_c, tsv, tsr, tobj, sobj, inst, a.out)
    return 0


def render(R, cid, ctc, hu, sarr, tsv, tsr, tobj, sobj, inst, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    A = ctc.affine
    sx, sy, sz = np.diag(A[:3, :3]); ox, oy, oz = A[:3, 3]
    X = ox + sx * np.arange(hu.shape[0]); Y = oy + sy * np.arange(hu.shape[1]); Z = oz + sz * np.arange(hu.shape[2])
    allv = np.argwhere(tsv > 0)
    y0, y1 = allv[:, 1].min(), allv[:, 1].max() + 1
    cols = ["#ffd400", "#ff4fd8"]
    order = inst + ([26] if 26 in sobj else [])

    def zsl(zr):
        return slice(max(int((zr[0] - oz) / sz) - 2, 0), min(int((zr[1] - oz) / sz) + 3, hu.shape[2]))

    def outlines(ax, lab, proj_axis, sl3, hh, zz, names, zr, dx):
        for i, c in enumerate(order):
            if not (zr[0] - 40 <= sobj[c]["centroid"][2] <= zr[1] + 40):
                continue
            pr = (lab[sl3] == c).any(axis=proj_axis)
            if pr.any():
                ax.contour(hh, zz, pr.T.astype(float), levels=[0.5], colors=[cols[i % 2]], linewidths=0.7)
            if names:
                cxyz = sobj[c]["centroid"]
                hpos = cxyz[0] if proj_axis == 1 else cxyz[1]
                ax.text(hpos + dx, cxyz[2], VERSE.get(c, str(c)), color=cols[i % 2], fontsize=7, ha="center",
                        va="center", fontweight="bold")

    def coronal(ax, zr, title, marks):
        zs = zsl(zr)
        cor = hu[:, y0:y1, zs].max(axis=1)
        ax.imshow(np.clip(cor.T, -150, 1100), cmap="gray", origin="lower", aspect="equal",
                  extent=[X[0] - sx / 2, X[-1] + sx / 2, Z[zs][0] - sz / 2, Z[zs][-1] + sz / 2])
        outlines(ax, sarr, 1, (slice(None), slice(y0, y1), zs), X, Z[zs], True, zr, 55)
        rp = (tsr[:, y0:y1, zs] > 0).any(axis=1)
        if rp.any():
            ax.contour(X, Z[zs], rp.T.astype(float), levels=[0.5], colors=["#39e639"], linewidths=0.6)
        for c in [c for c in tobj if c != 26]:
            cxyz = tobj[c]["centroid"]
            if zr[0] <= cxyz[2] <= zr[1]:
                ax.text(cxyz[0] - 55, cxyz[2], TS_NAME[c], color="#4fd2ff", fontsize=7, ha="center", va="center")
        if marks:
            for r in R.get("ribs", []):
                mx, my, mz = r["medial_xyz"]
                if zr[0] <= mz <= zr[1]:
                    ax.plot([mx], [mz], "o", ms=3, color="#39e639")
                    nm = VERSE.get(inst[r["attach_index"] - 1], "?")
                    ax.text(mx + (14 if r["side"] == "right" else -14), mz - 4, f"{r['ts_rib'].split('_')[-1]}>{nm}{'' if r['attach_rule'] == 'bone_path' else '*'}",
                            color="#9cff9c", fontsize=5.5, ha="center", va="top")
        ax.invert_xaxis()
        ax.set_ylim(*zr)
        ax.set_title(title, fontsize=8)
        ax.set_xlabel("R <- x (mm) -> L | yellow/magenta: SPINEPS instances with relabelled (VERIDAH) names; cyan: TS names; "
                      "green: TS ribs, dot = medial end, 'k>NAME' = instance it attaches to", fontsize=5.5)
        ax.tick_params(labelsize=6)

    def sagittal(ax, zr, xc_i, half_mm, title, fov=True):
        xs = slice(max(xc_i - int(half_mm / sx), 0), xc_i + int(half_mm / sx) + 1)
        zs = zsl(zr)
        sag = hu[xs, :, zs].max(axis=0)
        ax.imshow(np.clip(sag.T, -150, 1300), cmap="gray", origin="lower", aspect="equal",
                  extent=[Y[0] - sy / 2, Y[-1] + sy / 2, Z[zs][0] - sz / 2, Z[zs][-1] + sz / 2])
        outlines(ax, sarr, 0, (xs, slice(None), zs), Y, Z[zs], True, zr, 45)
        for c, colr in ((50, "#4fd2ff"), (26, "#4fd2ff")):
            if c in tobj:
                pr = (tsv[xs, :, zs] == c).any(axis=0)
                if pr.any():
                    ax.contour(Y, Z[zs], pr.T.astype(float), levels=[0.5], colors=[colr], linewidths=0.6, linestyles="dashed")
        if fov:
            ax.axhline(Z[0], color="red", lw=0.8, ls="--")
        ax.invert_xaxis()
        ax.set_ylim(*zr)
        ax.set_title(title, fontsize=8)
        ax.set_xlabel("A <- y (mm) -> P | cyan dashed: TS S1 / TS sacrum; red dashed: CT field-of-view bottom", fontsize=5.5)
        ax.tick_params(labelsize=6)

    lum = inst[-6:]
    xc_i = int(round(np.median(np.concatenate([sobj[c]["idx"][:, 0] for c in lum]))))
    zall = (min(sobj[c]["zmin"] for c in sobj) - 15, max(sobj[c]["zmax"] for c in sobj) + 15)
    t = f"{cid} ctd={R['ctd_subtype']} objects={R['independent_counts']}"
    fig, axs = plt.subplots(1, 2, figsize=(10, 14), gridspec_kw=dict(width_ratios=[1.6, 1]))
    coronal(axs[0], zall, t, marks=False)
    sagittal(axs[1], zall, xc_i, 12, "sagittal slab +-12 mm")
    fig.tight_layout(); fig.savefig(f"{out}/{cid}_full.png", dpi=130); plt.close(fig)

    lr = R.get("lowest_rib_on_instance", {}).get("index", len(inst) - 5)
    top = sobj[inst[max(lr - 4, 0)]]["zmax"] + 10
    zr = (min(zall[0], float(Z[0]) - 5), top)
    fig, axs = plt.subplots(1, 2, figsize=(12, 10), gridspec_kw=dict(width_ratios=[1.6, 1]))
    coronal(axs[0], zr, f"{t}\nlowest rib on instance #{lr} ({R.get('lowest_rib_on_instance', {}).get('veridah_name')})", marks=True)
    sagittal(axs[1], zr, xc_i, 12, "sagittal slab +-12 mm")
    fig.tight_layout(); fig.savefig(f"{out}/{cid}_zoom.png", dpi=150); plt.close(fig)

    # lumbosacral: thin slab, full resolution, from two instances above the lowest to the FOV bottom
    lo = inst[-1]
    xl = int(round(np.median(sobj[lo]["idx"][:, 0])))
    ztop = sobj[inst[-3]]["zmax"] + 5 if len(inst) >= 3 else zall[1]
    zr = (max(float(Z[0]) - 5, sobj[lo]["zmin"] - 90), ztop)
    fig, axs = plt.subplots(1, 2, figsize=(12, 7))
    sagittal(axs[0], zr, xl, 3, f"{cid} lumbosacral sagittal +-3 mm at the lowest instance")
    sagittal(axs[1], zr, xl, 15, "same, +-15 mm slab")
    for ax in axs:
        yc = sobj[lo]["centroid"][1]
        ax.set_xlim(yc + 110, yc - 90)
    js = "; ".join(f"{j['upper']}->{j['lower']}: min {j['min_hu_mid']} HU, dip {j['dip_contrast']}" for j in R.get("lowest_joints", []))
    fig.suptitle(js, fontsize=7)
    fig.tight_layout(); fig.savefig(f"{out}/{cid}_ls.png", dpi=160); plt.close(fig)
    # axial slab MIPs: a rib is a separate bone meeting the vertebra at a joint; a transverse process is part of it
    lr = R.get("lowest_rib_on_instance", {}).get("index", len(inst) - 5)
    hr = R.get("highest_rib_on_instance", {}).get("index", 8)
    picks = [i for i in (hr - 1, hr, hr + 1, lr - 1, lr, lr + 1, lr + 2) if 1 <= i <= len(inst)]
    fig, axs = plt.subplots(2, 4, figsize=(16, 8.5))
    axs = axs.ravel()
    for ax, i in zip(axs, picks):
        c = inst[i - 1]
        o = sobj[c]
        bodyv = o["idx"][o["xyz"][:, 1] >= np.median(o["xyz"][:, 1])]
        z0, z1 = int(bodyv[:, 2].min()), int(bodyv[:, 2].max()) + 1
        xc = int(round(np.median(o["idx"][:, 0]))); yc = int(round(np.median(o["idx"][:, 1])))
        xs = slice(max(xc - int(110 / sx), 0), min(xc + int(110 / sx), hu.shape[0]))
        ys = slice(max(yc - int(70 / sy), 0), min(yc + int(90 / sy), hu.shape[1]))
        mip = hu[xs, ys, z0:z1].max(axis=2)
        ax.imshow(np.clip(mip.T, -150, 1100), cmap="gray", origin="lower", aspect="equal",
                  extent=[X[xs][0], X[xs][-1], Y[ys][0], Y[ys][-1]])
        pr = (sarr[xs, ys, z0:z1] == c).any(axis=2)
        ax.contour(X[xs], Y[ys], pr.T.astype(float), levels=[0.5], colors=["#ffd400"], linewidths=0.7)
        rp = (tsr[xs, ys, z0:z1] > 0).any(axis=2)
        if rp.any():
            ax.contour(X[xs], Y[ys], rp.T.astype(float), levels=[0.5], colors=["#39e639"], linewidths=0.6)
        ax.invert_xaxis()
        att = [r["ts_rib"].replace("rib_", "") for r in R.get("ribs", []) if r.get("attach_index") == i]
        ax.set_title(f"#{i} {VERSE.get(c, c)}  (body z {Z[z0]:.0f}..{Z[z1 - 1]:.0f})  TS ribs counted here: {att or 'none'}", fontsize=7)
        ax.tick_params(labelsize=5)
    for ax in axs[len(picks):]:
        ax.axis("off")
    fig.suptitle(f"{cid} axial slab MIP over each body (R on the left, anterior up); yellow = that SPINEPS instance, green = TS ribs", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{out}/{cid}_axial.png", dpi=140); plt.close(fig)

    # TP level: the z-range of the instance's own LATERAL parts (|x - xc| > 18 mm: pedicles, transverse processes),
    # which is where a rib meets it; thin and magnified
    fig, axs = plt.subplots(2, 4, figsize=(16, 8.5))
    axs = axs.ravel()
    for ax, i in zip(axs, picks):
        c = inst[i - 1]
        o = sobj[c]
        xcw = np.median(o["xyz"][:, 0])
        lat = o["idx"][np.abs(o["xyz"][:, 0] - xcw) > 18.0]
        if len(lat) < 20:
            lat = o["idx"]
        z0, z1 = int(np.percentile(lat[:, 2], 10)), int(np.percentile(lat[:, 2], 90)) + 1
        xc = int(round(np.median(o["idx"][:, 0]))); yc = int(round(np.median(o["idx"][:, 1])))
        xs = slice(max(xc - int(85 / sx), 0), min(xc + int(85 / sx), hu.shape[0]))
        ys = slice(max(yc - int(45 / sy), 0), min(yc + int(55 / sy), hu.shape[1]))
        mip = hu[xs, ys, z0:z1].max(axis=2)
        ax.imshow(np.clip(mip.T, -150, 1300), cmap="gray", origin="lower", aspect="equal",
                  extent=[X[xs][0], X[xs][-1], Y[ys][0], Y[ys][-1]], interpolation="nearest")
        for cc_, colr in ((c, "#ffd400"),):
            pr = (sarr[xs, ys, z0:z1] == cc_).any(axis=2)
            ax.contour(X[xs], Y[ys], pr.T.astype(float), levels=[0.5], colors=[colr], linewidths=0.8)
        oth = ((sarr[xs, ys, z0:z1] > 0) & (sarr[xs, ys, z0:z1] != c)).any(axis=2)
        if oth.any():
            ax.contour(X[xs], Y[ys], oth.T.astype(float), levels=[0.5], colors=["#ff4fd8"], linewidths=0.5, linestyles="dotted")
        rp = (tsr[xs, ys, z0:z1] > 0).any(axis=2)
        if rp.any():
            ax.contour(X[xs], Y[ys], rp.T.astype(float), levels=[0.5], colors=["#39e639"], linewidths=0.6)
        ax.invert_xaxis()
        cr = R.get("ct_ribs_per_instance", {}).get(f"#{i} {VERSE.get(c, c)}", [])
        ax.set_title(f"#{i} {VERSE.get(c, c)} TP level z {Z[z0]:.0f}..{Z[z1 - 1]:.0f} | CT ribs reaching it: {cr or 'none'}", fontsize=7)
        ax.tick_params(labelsize=5)
    for ax in axs[len(picks):]:
        ax.axis("off")
    fig.suptitle(f"{cid} axial MIP at each vertebra's transverse-process level (R left, anterior up): yellow = the instance, "
                 f"magenta dotted = other instances, green = TS ribs", fontsize=8)
    fig.tight_layout(); fig.savefig(f"{out}/{cid}_axial_tp.png", dpi=150); plt.close(fig)
    print(f"TS12V_RENDER {cid} full/zoom/ls/axial written", flush=True)


if __name__ == "__main__":
    sys.exit(main())
