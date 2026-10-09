#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_carmlspine_drr.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""DRRs of the three real L6 CBCTs (C-ArmLSpine case42 / case121 / case136), rendered under the Surgio
pose pool and styled through every fitted device card, into their OWN root so they can be held out entirely.

WHY A SEPARATE ROOT. These CBCTs are PAIRED with real intraoperative frames: they are the real-data check
of the rare-class program and must never enter training. Everything lands under
/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr/ in the level-bank layout (img/ uint8 .npy,
ann/ .json), and every ann carries held_out: true besides the identity fields.

GEOMETRY. Each case is rendered under its own registered Surgio poses (AP and LAT from the devcorpus pose
pool, which poses_surgio built from the consensus registrations) plus a synthetic AP->lateral arc about the
AP anchor (pose_arc.arc_pose, the same construction the devcorpus arc pools use), at the Surgio detector's
own K / pitch, down 2 (0.30 mm rendered pitch, 1024 px). The volume is NOT translated: the registered pose
maps this exact CBCT in its native world frame, which is the whole point of the pairing.

TRUNCATION IS RECORDED, NOT REJECTED. A CBCT is a small cylinder, so almost every ray leaves the volume
through tissue the scan does not contain; the devcorpus rejection rule (trunc > 0.25) would reject every
frame here. trunc_frac goes in the ann instead, so a consumer can see what it is looking at.

LABELS. The SPINEPS+VERIDAH instance mask (VerSe ids, L6 = 25 -- the id CONFIRMED in the subtype table and
in levels.json's spineps_labels) names the vertebrae; TotalSegmentator cannot say L6 by construction, which
is exactly why its names disagree on these three cases (levels.json: 'VERIDAH calls L6'). Boxes follow the
ONE box convention (Greg 2026-09-23): the vertebral BODY (instance x corpus sub-region 49/50), projected;
the whole-vertebra box is kept beside it as box_whole. The sacrum uses its whole mask. SPINEPS sits on its
own cropped, resampled grid, so masks are projected as WORLD points (carmlspine_labels.world_points), never
by index against the CBCT grid.

    python tools/rare_class_carmlspine_drr.py --case case42
    python tools/rare_class_carmlspine_drr.py --summary
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import zlib
from pathlib import Path

import numpy as np


def stable_seed(*parts):
    """A deterministic seed: str hash() is salted per process and must never seed a corpus."""
    return zlib.crc32("|".join(str(p) for p in parts).encode()) % (2 ** 31)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import device_style as DS  # noqa: E402
import pose_arc as PA  # noqa: E402
from carmlspine_labels import VERSE, project, rot_pts, upright_turns, world_points  # noqa: E402

D = "/rs/rs_grp_oschome/go2432/data/carmlspine"
ROOT = "/rs/rs_grp_oschome/go2432/data/rare_class/carmlspine_cbct_drr"
POOL = "/rs/rs_grp_oschome/go2432/data/devcorpus/poses/surgio_b51_dr.json"
SUBTYPES = str(Path(__file__).resolve().parents[1] / "SchwingNet" / "results" / "rare_class" / "transitional_subtypes.json")
CASES = ["case42", "case121", "case136"]
CARDS = ["surgio_b51_dr", "cios_fusion", "elekta_xvi", "bv_pulsera", "pixium_4600", "varian_halcyon"]
DOWN = 2                       # Surgio geometry family: 0.15 mm detector pitch -> 0.30 mm rendered (GEOM_DOWN)
DRAWS = 2
ARC_LATS = [-88.0, -67.5, -45.0, -22.5, 0.0, 22.5, 45.0, 67.5, 88.0]   # +/-90 exactly is the lat/roll gimbal of angles_of and fails arc_pose's read-back; the REAL registered lateral covers the true lateral
MIN_INSIDE = 0.50              # the carmlspine_labels box rule: >= 50 % of points in frame, both sides >= 8 px
MIN_SIDE = 8.0


def subtype_of(case):
    d = json.load(open(SUBTYPES))
    for r in d["rows"]:
        if r.get("source") == "carmlspine_real" and r.get("case") == case:
            return r["subtype"], r.get("truth_source", "")
    raise SystemExit(f"{case}: no carmlspine_real row in {SUBTYPES}")


def load_cbct_lps(path):
    """The CBCT as an axis-aligned LPS volume (z, y, x), origin (x, y, z) mm, spacing (x, y, z) mm.

    The direction matrix is required to be a signed permutation (checked, not assumed): raycast wants an
    axis-aligned grid, and silently feeding it an oblique volume would move every bone by a finite,
    plausible-looking amount. A genuinely oblique CBCT fails loudly here and is reported un-rendered.
    """
    import SimpleITK as sitk
    im = sitk.ReadImage(path)
    a = sitk.GetArrayFromImage(im).astype(np.float32)                     # (z, y, x) index order
    Dm = np.array(im.GetDirection()).reshape(3, 3)
    sp = np.array(im.GetSpacing(), float)                                  # per index axis (x, y, z)
    org = np.array(im.GetOrigin(), float)
    P = np.round(Dm)
    if np.abs(Dm - P).max() > 1e-3 or np.abs(np.abs(P).sum(0) - 1).max() > 0 or np.abs(np.abs(P).sum(1) - 1).max() > 0:
        raise RuntimeError(f"direction is not a signed permutation: {Dm.tolist()}")
    ax = a.transpose(2, 1, 0)                                              # (x, y, z) index order
    world_axis = [int(np.argmax(np.abs(P[:, k]))) for k in range(3)]       # index axis k -> world axis
    sign = [float(P[world_axis[k], k]) for k in range(3)]
    n = ax.shape
    org_w = np.empty(3); sp_w = np.empty(3); src = [None] * 3
    for k in range(3):
        w = world_axis[k]
        src[w] = k
        sp_w[w] = sp[k]
        org_w[w] = org[w] if sign[k] > 0 else org[w] - (n[k] - 1) * sp[k]
    ax = ax.transpose(src)                                                 # index order = world (x, y, z)
    for w in range(3):
        if sign[src[w]] < 0:
            ax = np.flip(ax, axis=w)
    vol = np.ascontiguousarray(ax.transpose(2, 1, 0))                      # (z, y, x) for raycast
    # read-back check: voxel (0,0,0) and (-1,-1,-1) of the reoriented grid must be corners of the original
    lo, hi = org_w, org_w + (np.array(vol.shape[::-1]) - 1) * sp_w
    c0 = org + Dm @ (np.zeros(3) * sp)
    c1 = org + Dm @ ((np.array([a.shape[2], a.shape[1], a.shape[0]]) - 1) * sp)
    for c in (c0, c1):
        if not (np.all(c >= lo - 0.01) and np.all(c <= hi + 0.01)):
            raise RuntimeError(f"reorientation read-back failed: corner {c} outside [{lo}, {hi}]")
    return vol, org_w, sp_w


def strip_table(vol):
    from scipy.ndimage import binary_opening, label
    body = binary_opening(vol > -300.0, iterations=2)
    lab, n = label(body)
    if n > 1:
        sizes = np.bincount(lab.ravel()); sizes[0] = 0; body = lab == int(sizes.argmax())
    return np.where(body, vol, -1000.0).astype(np.float32)


def case_poses(case, rng):
    pool = json.load(open(POOL))["poses"]
    mine = {p["view"]: p for p in pool if p.get("case") == case and p.get("view") in ("AP", "LAT")}
    if "AP" not in mine or "LAT" not in mine:
        raise SystemExit(f"{case}: pool {POOL} has views {sorted(mine)} -- need AP and LAT")
    poses = [("AP", mine["AP"]), ("LAT", mine["LAT"])]
    for lat in ARC_LATS:
        p = PA.arc_pose(mine["AP"], lat, tilt_deg=rng.uniform(-10, 10), roll_deg=rng.uniform(-8, 8),
                        jitter_mm=(rng.uniform(-10, 10), rng.uniform(-10, 10), rng.uniform(-10, 10)),
                        tag=f"{case}/arc{int(round(lat)):+04d}")
        poses.append((f"arc{int(round(lat)):+04d}", p))
    return poses


def structures(case, rng):
    """[(name, verse_id, body_pts|None, whole_pts, touch, n_body, n_whole, box_source)] from the SPINEPS masks."""
    import SimpleITK as sitk
    sp_vert = f"{D}/spineps/{case}_seg-vert_msk_veridah.nii.gz"
    sp_spine = f"{D}/spineps/{case}_seg-spine_msk.nii.gz"
    vi = sitk.GetArrayFromImage(sitk.ReadImage(sp_vert))
    si = sitk.GetArrayFromImage(sitk.ReadImage(sp_spine)) if os.path.exists(sp_spine) else None
    corpus = np.isin(si, [49, 50]) if si is not None and si.shape == vi.shape else None
    ids = sorted(int(v) for v in np.unique(vi) if v > 0 and int(v) in VERSE)
    print(f"{case}: veridah ids {ids} -> {[VERSE[i] for i in ids]}"
          + ("" if corpus is None else f"; corpus voxels {int(corpus.sum())}"), flush=True)
    out = []
    for vid in ids:
        whole, touch, n_w = world_points(sp_vert, select=lambda m, v=vid: m == v, rng=rng)
        if whole is None or n_w < 500:
            continue
        body, n_b, src = None, 0, "whole_vertebra"
        if VERSE[vid] != "sacrum" and corpus is not None:
            body, _, n_b = world_points(sp_vert, select=lambda m, v=vid: (m == v) & corpus, rng=rng, max_pts=8000)
            if body is not None and n_b > 200:
                src = "spineps_corpus"
            else:
                body, n_b = None, 0
        if VERSE[vid] == "sacrum":
            src = "whole_sacrum"
        out.append(dict(name=VERSE[vid], id=vid, body=body, whole=whole, touch=bool(touch),
                        n_body=int(n_b), n_whole=int(n_w), box_source=src))
    return out


def box_of(uv, S):
    inside = (uv[:, 0] >= 0) & (uv[:, 0] < S) & (uv[:, 1] >= 0) & (uv[:, 1] < S)
    vis = float(inside.mean()) if len(uv) else 0.0
    if inside.sum() < 20 or vis < MIN_INSIDE:
        return None, vis
    q = uv[inside]
    x0, y0 = np.percentile(q, 2, axis=0); x1, y1 = np.percentile(q, 98, axis=0)
    x0, y0 = max(0.0, x0), max(0.0, y0); x1, y1 = min(S - 1.0, x1), min(S - 1.0, y1)
    if x1 - x0 < MIN_SIDE or y1 - y0 < MIN_SIDE:
        return None, vis
    return [float(x0), float(y0), float(x1), float(y1)], vis


def qc_png(img, levels, path):
    from PIL import Image, ImageDraw
    im = Image.fromarray(img).convert("RGB"); dr = ImageDraw.Draw(im)
    for name, e in levels.items():
        if e.get("box_whole") and e["box_whole"] != e["box"]:
            dr.rectangle(e["box_whole"], outline=(200, 60, 60), width=1)
        if e.get("box"):
            dr.rectangle(e["box"], outline=(60, 220, 60), width=2)
            dr.text((e["box"][0] + 3, max(0, e["box"][1] - 14)), name, fill=(60, 220, 60))
    im.save(path)


def render_case(case):
    import deepfluoro_render as DR
    subtype, subtype_source = subtype_of(case)
    for sub in ("img", "ann", "qc"):
        Path(ROOT, sub).mkdir(parents=True, exist_ok=True)
    rng = np.random.RandomState(stable_seed(case, "pts"))
    arc_rng = np.random.RandomState(stable_seed(case, "arc"))

    vol, org, sp = load_cbct_lps(f"{D}/nifti/{case}_cbct.nii.gz")
    vol = strip_table(vol)
    print(f"{case}: CBCT {vol.shape} at {sp.tolist()} mm, origin {org.tolist()}", flush=True)
    structs = structures(case, rng)
    if not any(s["name"] == "L6" for s in structs):
        print(f"{case}: WARNING -- no L6 (id 25) in the veridah mask; rendering what is there", flush=True)
    centre = np.mean([s["whole"].mean(0) for s in structs], 0)

    poses = case_poses(case, arc_rng)
    RP = DS.rp_tables()
    devs = {c: DS.load_device(c) for c in CARDS}
    made, per_pose = 0, {}
    for ptag, pose in poses:
        K = np.array(pose["K"]); ext = np.array(pose["ext"]); T = np.array(pose["T"])
        M = ext @ np.linalg.inv(T)
        d = dict(K=K, ext=ext, T=T, nr=pose["nr"], nc=pose["nc"], vol=vol, org=org, sp=sp)
        try:
            trans, water, bone, hit, trunc = DR.raycast(d, down=DOWN)
        except Exception as e:  # noqa: BLE001
            print(f"{case} {ptag}: raycast failed: {e}", flush=True); per_pose[ptag] = "raycast_failed"; continue
        if not hit.any():
            print(f"{case} {ptag}: no ray hit the volume", flush=True); per_pose[ptag] = "no_hit"; continue
        S = water.shape[0]
        R3, t3 = M[:3, :3], M[:3, 3]
        k, _up = upright_turns(K, R3, t3, centre)
        water, bone = np.rot90(water, k).copy(), np.rot90(bone, k).copy()
        hit, trunc = np.rot90(hit, k).copy(), np.rot90(trunc, k).copy()
        trunc_frac = float(trunc[hit].mean())
        levels = {}
        for s in structs:
            uv_w = rot_pts(project(K, R3, t3, s["whole"]) / DOWN, k, S)
            bw, vis_w = box_of(uv_w, S)
            if s["body"] is not None:
                uv_b = rot_pts(project(K, R3, t3, s["body"]) / DOWN, k, S)
                bb, vis_b = box_of(uv_b, S)
            else:
                bb, vis_b = bw, vis_w
            if bb is None and bw is None:
                continue
            box = bb if bb is not None else bw
            src = s["box_source"] if bb is not None else "whole_vertebra"
            clipped = bool(s["touch"] or min(vis_b if bb is not None else vis_w, vis_w) < 0.95
                           or min(box[0], box[1]) <= 0.5 or max(box[2], box[3]) >= S - 1.5)
            levels[s["name"]] = dict(id=s["id"], name=s["name"], box=[int(round(v)) for v in box],
                                     box_whole=[int(round(v)) for v in bw] if bw is not None else None,
                                     box_source=src, px=int(s["n_body"] if bb is not None and src == "spineps_corpus" else s["n_whole"]),
                                     vis=round(float(vis_b if bb is not None else vis_w), 3), clipped=clipped)
        if not levels:
            print(f"{case} {ptag}: no structure projected into frame", flush=True); per_pose[ptag] = "no_levels"; continue
        yy, xx = np.mgrid[0:S, 0:S]
        disc = ((yy - S / 2) ** 2 + (xx - S / 2) ** 2 <= (0.06 * S) ** 2) & hit
        thick = float(np.median(water[disc])) if disc.any() else float("nan")
        pitch = float(pose["px_mm"]) * DOWN
        an = PA.angles_of(pose)
        n_pose = 0
        for card in CARDS:
            srng = np.random.default_rng(stable_seed(case, ptag, card))
            for j in range(DRAWS):
                t = DS.sample_terms(devs[card], 1, srng, cond={"thickness_cm": thick} if np.isfinite(thick) else None,
                                    mode="typicality")[0]
                t["rot180"] = False          # head-up is set by the upright turn and must stay deterministic
                img, _field = DS.style(water, bone, hit, devs[card], t, srng, pitch, RP=RP)
                stem = f"carmlspine_{case}_{ptag}_{card}_{j}"
                np.save(Path(ROOT, "img", f"{stem}.npy"), img.astype(np.uint8))
                ann = dict(case=stem, source_case=case, patient_id=f"carmlspine_{case}", scheme="carmlspine",
                           subtype=subtype, subtype_source=subtype_source, held_out=True,
                           shape=list(img.shape), axcodes="film", mm_per_px_detector=pitch,
                           pose=dict(tag=pose["tag"], view=ptag, arc=bool(pose.get("arc", False)),
                                     lat_deg=round(an["lat_deg"], 2), tilt_deg=round(an["tilt_deg"], 2),
                                     roll_deg=round(an["roll_deg"], 2), rot90_k=int(k), rot180=False),
                           card=card, draw=j, sample_mode="typicality", trunc_frac=round(trunc_frac, 4),
                           levels=levels,
                           renderer="rare_class_carmlspine_drr v1 (deepfluoro_render.raycast down 2, SPINEPS+VERIDAH "
                                    "boxes as world points, body convention, device_style typicality)")
                json.dump(ann, open(Path(ROOT, "ann", f"{stem}.json"), "w"), indent=1)
                if j == 0 and (ptag in ("AP", "LAT") or (card == "surgio_b51_dr" and ptag in ("arc-045", "arc+045"))):
                    qc_png(img, levels, Path(ROOT, "qc", f"{stem}.png"))
                made += 1; n_pose += 1
        per_pose[ptag] = n_pose
        print(f"{case} {ptag}: lat {an['lat_deg']:+.1f} tilt {an['tilt_deg']:+.1f} k={k} trunc {trunc_frac:.2f} "
              f"levels {sorted(levels)} -> {n_pose} frames", flush=True)
    info = dict(case=case, subtype=subtype, frames=made, poses=per_pose, cards=CARDS, draws=DRAWS,
                levels_present=[s["name"] for s in structs])
    json.dump(info, open(Path(ROOT, f"RENDER_INFO_{case}.json"), "w"), indent=1)
    print(f"{case}: {made} frames", flush=True)
    return 0


def summary():
    import collections
    import subprocess
    anns = sorted(glob.glob(f"{ROOT}/ann/*.json"))
    per_class, per_subtype, per_card, per_case, per_view = (collections.Counter() for _ in range(5))
    l6_two_body = 0
    for p in anns:
        a = json.load(open(p))
        per_subtype[a["subtype"]] += 1; per_card[a["card"]] += 1; per_case[a["source_case"]] += 1
        per_view[a["pose"]["view"]] += 1
        for name in a["levels"]:
            per_class[name] += 1
    out = dict(frames=len(anns), imgs=len(glob.glob(f"{ROOT}/img/*.npy")),
               frames_per_class=dict(per_class), frames_per_subtype=dict(per_subtype),
               frames_per_card=dict(per_card), frames_per_case=dict(per_case), frames_per_view=dict(per_view))
    json.dump(out, open(f"{ROOT}/summary.json", "w"), indent=1)
    print(json.dumps(out, indent=1), flush=True)
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("patient_keys.py")),
                        "--drr", ROOT, "--out", f"{ROOT}/patient_keys_dryrun.json"], capture_output=True, text=True)
    print("patient_keys dry-run rc", r.returncode, "\n", r.stdout[-2000:], r.stderr[-1000:], flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    if a.summary:
        return summary()
    if not a.case:
        raise SystemExit("--case or --summary")
    return render_case(a.case)


if __name__ == "__main__":
    sys.exit(main())
