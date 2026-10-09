#!/usr/bin/env python
"""A synthetic flexion-extension CINE with exact truth: one whole-spine VerSe CT, its spine moved segment by segment
through a smooth flexion-extension arc by PolyPose's polyrigid warp, every frame ray-cast at ONE fixed C-arm lateral
pose with frozen noise, and every frame's truth projected through the same rigid transforms that moved it
(docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md section 4, with the source changed as below).

SOURCE (Greg, 2026-09-26): not CTSpinoPelvic1K. A whole-spine VerSe CT -- verse823 by default (C1-L5 labelled, no
sacrum label, 0.72 x 0.72 x 0.70 mm, VerSe20 training split; alternates verse809, verse108), read from
~/VerSeFusion/data/unified (never ~/vf_813, which drops C1-T9). NOTHING HERE IS HELD OUT: every VerSe CT is inside the
v9 training renders, so level_prototype must run with --not-held-out "demo on a VerSe CT; VerSe renders are in v9
training", and frames.json, every truth meta and the README say so.

LABEL MAP. VerSe ids are VerSe-native (C1-C7 = 1-7, T1-T12 = 8-19, L1-L6 = 20-25, sacrum 26, T13 28), and
ostk.labels.labels_for(volume) does NOT return that map for a VerSe mask: it decides by pelvis voxel mass, and ids 9-12
-- T2-T5 here -- are the legacy scheme's hips and femurs, so verse823 is detected "v4" and "L1" resolves to id 1, which
is C1 (measured 2026-09-26). No fixed map is imported instead: labels_for(volume) is called and recorded, then every map
ostk knows (labels_for(scheme=s)) is held against the anatomy -- the vertebrae it names must lie in cranio-caudal order
in world z, and no sizeable id may go unnamed. The detected map is kept when it passes; otherwise the ONE map that
passes is used and the override recorded; none or two passing is a refusal.

REGIONS (--region). lumbar: T10-T11 .. L4-L5 move (the plan's "T10-T11 through L5-S1", less L5-S1), L5 is the fixed
base. There is no sacrum label, so the chain hinges on L5 and L5-S1 does not move -- the one departure from the plan's
segments, forced by the source. cervical: C1-C2 .. C7-T1 move, T1 is fixed; the skull is unlabelled, so it is not a
rigid body -- it follows the blended field, which near the craniocervical junction is dominated by C1 (and C2).
whole: both plus the thoracic segments, L5 fixed. Vertebrae cranial of the top moving segment ride with it; vertebrae
caudal of the base stay. Ignore regions cover the unlabelled sacrum below L5 and the unlabelled skull above C1.

MOTION. N frames (60 = 4 s at 15 fps), a_k = -sin(2 pi k / N): frame 0 neutral, N/4 the largest flexion, N/2 neutral
again, 3N/4 the largest extension. segs[s].flex_ext_deg = frac * m * (a_k * ext_s if a_k > 0 else a_k * flex_s),
lateral bending and axial rotation 0; positive = extension (build_transforms' convention: a rotation about world +x,
RAS, through the midpoint of the two vertebral centroids, composed from the fixed base upward). The caps are
SchwingNet/results/polypose/rom_cine.json, whose lumbar/thoracolumbar rows are verbatim copies of sampling_spec.json
rom_deg (a copy that drifts is refused). A region with any PENDING row is refused: no number is invented. The plan
said verify_equivalence runs on frame 30 "the largest flexion"; a_30 = 0 is neutral, so it runs on argmin a_k (15).

STAGES, all under one sequence directory <seq> (default /rs/.../polypose/cine/<case>_<region>_fe_f<frac*100>):
  plan    frames.json (per-frame segments and rigid transforms, the label-map record, the re-keyed body mask, the
          end-plate corners, the crop, the render settings), README.md, sources/.   CPU, fluorogen env.
  warp    volumes/f###_{ct,label,body_msk}.nii.gz on the source grid (cropped along S-I, never reoriented) via
          polypose_warp.warp_volumes; verify_equivalence on the verify frame; the geometric invariants
          (label_rigidity, jacobian_positive, field_matches_transforms, label_set_preserved, and base_fixed --
          pelvis_fixed's identity test with a single-vertebra voxel rule, see base_fixed) -> checks/f###.json, which
          records the frame_key of the plan the volumes were warped for: a frame is skipped only when that key is
          the current plan's, and render / gt / check refuse volumes warped for another.  GPU, the PolyPose container.
  render  images/<stem>.png (device-styled, one exposure drawn from frame 0, frozen noise, rot180 off, fixed field)
          and images_logor/<stem>.png (unstyled -log attenuation -> carmlspine_labels.window_or), one lateral pose
          (pose_arc.arc_pose of the pool's anchor) and one isocentre, both fixed from frame 0 (render_state.json).
  gt      meta/<stem>.json in the cine truth schema: body boxes from the warped body mask (min/max and 2-98 %,
          `inside`), each cross-checked against source body voxels moved by the frame's transform (IoU), the 3-D
          end-plate corners (ostk.vertebral_body.endplate_corners_body, rms- and body-screened) moved and projected,
          the silhouette quad, ignore regions, K, M, pitch and the isocentre. A level clipped by the frame border
          is box-only: corners null unless all four project onto the image, silhouette null when any of its voxels
          projects off it.                                                            CPU, fluorogen env.
  check   qc/contact_sheet.png (frames 0, N/4, N/2, 3N/4 with the truth drawn) and qc/check.json; exits non-zero on
          any failed invariant, cross-check or missing frame. LOOK AT THE SHEET BEFORE SCORING ANYTHING.

    python tools/polypose/cine_render.py self-test
    python tools/polypose/cine_render.py rom-check --region lumbar
    python tools/polypose/cine_render.py plan --region lumbar --case verse823 --frac 0.5
    sbatch ... slurm/polypose_cine.sh      (bash slurm/polypose_cine.sh submit --region lumbar --case verse823)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import polypose_manifest as PM  # noqa: E402  (LEVEL_ORDER, VERTEBRA_RE, sha256_file; stdlib only)

SCHEMA = "polypose_cine/1"
TRUTH_SCHEMA = "cine_truth/1"
ROM_DEFAULT = ROOT / "SchwingNet/results/polypose/rom_cine.json"
SPEC_DEFAULT = ROOT / "SchwingNet/results/polypose/sampling_spec.json"
OUT_ROOT = "/rs/rs_grp_oschome/go2432/data/polypose/cine"
VERSE_UNIFIED = "~/VerSeFusion/data/unified"
BODIES = "/rs/rs_grp_oschome/go2432/data/spineps/bodies"
POOL_DEFAULT = "/rs/rs_grp_oschome/go2432/data/devcorpus/poses/surgio_b51_dr.json"
NOT_HELD_OUT = "demo on a VerSe CT; VerSe renders are in v9 training"
LR = (1.0, 0.0, 0.0)                 # world left-right (RAS +x), passed to ostk explicitly
MIN_VERTEBRA_VOXELS = 200            # = polypose_invariants.MIN_VERTEBRA_VOXELS (asserted in self-test)
CORNER_ORDER = "anatomical:AS,AI,PI,PS"   # Bournemouth's order: anterior-superior, anterior-inferior, posterior-inf, posterior-sup
SIL_ORDER = "geometric:canonical_slots"  # spine-detector/src/manifest.py: 0 sup small-x, 1 sup large-x, 2 inf large-x, 3 inf small-x
PENDING = "pending"

REGIONS = {
    "lumbar": dict(top="T10", base="L5", iso="L3",
                   note="no sacrum label on this source: the chain hinges on L5, which is held fixed; L5-S1 does not "
                        "move (the plan's T10-T11 .. L5-S1 less its last segment), and the unlabelled sacrum below L5 "
                        "is carried by the blended field (ignore region)"),
    "cervical": dict(top="C1", base="T1", iso="C5",
                     note="T1 is held fixed. The skull is unlabelled: it is not a rigid body but follows the blended "
                          "field, dominated near the craniocervical junction by C1 (and C2), so the occiput bends with "
                          "the motion instead of riding C1 rigidly (ignore region above C1)"),
    "whole": dict(top="C1", base="L5", iso="T7",
                  note="every segment C1-C2 .. L4-L5 moves with L5 fixed; both the lumbar and the cervical limitations "
                       "apply; the isocentre sits on a mid-thoracic body"),
}
ORDINARY = [n for n in PM.LEVEL_ORDER if PM.VERTEBRA_RE.match(n) and n not in ("T13", "L6")]     # C1 .. L5


class Refused(Exception):
    """This source or region cannot be planned, and no setting will change that: exit 3, nothing written."""


# ============================================================================================ small helpers
def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _x(p):
    return os.path.expanduser(str(p))


def _dump(path, obj):
    """Atomic JSON write (a preempted requeue job never leaves half a file)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(obj, indent=1, default=_jsonable))
    os.replace(tmp, path)


def _jsonable(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, np.ndarray):
        return v.tolist()
    return str(v)


def _save_nifti(arr, affine, header, dtype, path):
    import nibabel as nib
    h = header.copy()
    h.set_data_dtype(dtype)
    path = Path(path)
    tmp = path.with_name(path.name.replace(".nii.gz", f".tmp{os.getpid()}.nii.gz"))
    nib.save(nib.Nifti1Image(np.asarray(arr).astype(dtype), np.asarray(affine, float), header=h), str(tmp))
    os.replace(tmp, path)


def _sha256_lf(path) -> str:
    """sha256 of a text file with CRLF normalised to LF: the committed blob's hash on any checkout (`git show
    <commit>:<path> | sha256sum`), where a Windows working tree with core.autocrlf=true hashes the same commit
    differently."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _ftag(frac):
    return f"f{int(round(float(frac) * 100)):03d}"


def seq_name(case, region, frac):
    return f"{case}_{region}_fe_{_ftag(frac)}"


def stem_for(case, region, frac, k, view="lat"):
    """cine_<region>_f<frac>_<case>_<view>_p<frame>: keys to verse:<case> through patient_keys' verse_any rule (the
    person is the last (gl|verse)<digits> token, then _lat|_ap and _p<k>). A bare f###.png keys to nobody."""
    return f"cine_{region}_{_ftag(frac)}_{case}_{view}_p{int(k):03d}"


def phase(k, n):
    return -math.sin(2.0 * math.pi * k / n)


def _load_plan(seq):
    p = Path(seq) / "frames.json"
    if not p.exists():
        raise SystemExit(f"no {p}: run `plan` first")
    return json.loads(p.read_text())


# ============================================================================================ ROM table
def load_rom(path=ROM_DEFAULT, spec_path=SPEC_DEFAULT) -> dict:
    """rom_cine.json flattened to {segment: row}; REFUSES (ValueError) when a row it says it copied from
    sampling_spec.json rom_deg no longer equals the spec's row, so the cine and the sampler cannot silently diverge."""
    p = Path(path)
    d = json.loads(p.read_text(encoding="utf-8"))
    rows = {}
    for block in d["rom_deg"].values():
        for seg, row in block.items():
            if seg in rows:
                raise ValueError(f"{p}: segment {seg} appears twice")
            rows[seg] = row
    cf = d.get("copied_from") or {}
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))["rom_deg"]
    drift = [s for s in cf.get("rows", []) if rows.get(s) != spec.get(s)]
    if drift:
        raise ValueError(f"{p}: rows {drift} no longer equal {spec_path} rom_deg -- the copy has drifted; re-copy them "
                         "(never edit the copy by hand)")
    # the rows above are the refusal; the file hash is a record only (the spec may change in rows not copied here).
    # Compared with CRLF normalised to LF: copied_from.sha256 is the committed blob's, which a Windows checkout with
    # core.autocrlf=true does not reproduce byte for byte.
    spec_lf = _sha256_lf(spec_path)
    return dict(rows=rows, path=str(p), sha256=PM.sha256_file(str(p)), copied_from=cf,
                spec_sha256=PM.sha256_file(str(spec_path)), spec_sha256_lf=spec_lf,
                spec_is_copied_version=bool(cf.get("sha256")) and spec_lf == cf.get("sha256"),
                citations=d.get("citations", {}))


def row_status(row):
    """None when a row is usable, else why not. Usable = numeric, finite, non-negative flex and ext, not pending."""
    if not isinstance(row, dict):
        return "no row"
    st = row.get("status")
    if st is not None and str(st).strip().lower().startswith(PENDING):
        return str(st)
    for k in ("flex", "ext"):
        v = row.get(k)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(float(v)) or float(v) < 0:
            return f"no numeric {k}"
    return None


def require_rows(rom, segments) -> dict:
    """{segment: row} for every segment, or Refused naming each unusable one. Never a default, never a neighbour's."""
    bad = {s: row_status(rom["rows"].get(s)) for s in segments}
    bad = {s: w for s, w in bad.items() if w}
    if bad:
        raise Refused("ROM rows unusable for this region -- " + "; ".join(f"{s}: {w}" for s, w in bad.items())
                      + f". Fill them in {rom['path']} from a verified extraction first; nothing is invented here.")
    return {s: rom["rows"][s] for s in segments}


def region_segments(chain, region) -> list:
    r = REGIONS[region]
    for n in (r["top"], r["base"]):
        if n not in chain:
            raise Refused(f"region {region} needs {n}, which this source does not label (chain {chain[0]}..{chain[-1]})")
    i0, i1 = chain.index(r["top"]), chain.index(r["base"])
    if i0 >= i1:
        raise Refused(f"region {region}: {r['top']} is not cranial of {r['base']}")
    return [f"{chain[i]}-{chain[i + 1]}" for i in range(i0, i1)]


def frame_segments(a, caps, frac, mult) -> dict:
    out = {}
    for s, c in caps.items():
        fe = float(frac) * float(mult) * (a * float(c["ext"]) if a > 0 else a * float(c["flex"]))
        out[s] = dict(flex_ext_deg=round(fe + 0.0, 6), lat_bend_deg=0.0, axial_rot_deg=0.0)
    return out


# ============================================================================================ labels
def label_stats(lab) -> dict:
    """{id: (voxel count, voxel-index centroid)} in one slice-wise pass (no full-size coordinate arrays)."""
    lab = np.asarray(lab)
    n = int(lab.max()) + 1
    cnt = np.zeros(n)
    acc = np.zeros((3, n))
    X, Y = np.meshgrid(np.arange(lab.shape[0], dtype=float), np.arange(lab.shape[1], dtype=float), indexing="ij")
    xr, yr = X.ravel(), Y.ravel()
    for k in range(lab.shape[2]):
        f = lab[:, :, k].ravel()
        if not f.any():
            continue
        c = np.bincount(f, minlength=n)
        cnt += c
        acc[0] += np.bincount(f, weights=xr, minlength=n)
        acc[1] += np.bincount(f, weights=yr, minlength=n)
        acc[2] += c * k
    return {i: (int(cnt[i]), acc[:, i] / cnt[i]) for i in range(1, n) if cnt[i] > 0}


def _world(affine, vox):
    A = np.asarray(affine, float)
    return A[:3, :3] @ np.asarray(vox, float) + A[:3, 3]


def _order_test(M, stats, affine) -> dict:
    """Does map M name this volume's vertebrae in cranio-caudal order (world +z superior, RAS) with no sizeable id
    left unnamed? The legacy and the VerSe-native maps disagree grossly on a spine, so this separates them."""
    inv = {v: k for k, v in M.items()}
    named = {inv[i]: _world(affine, c)[2] for i, (n, c) in stats.items()
             if i in inv and PM.VERTEBRA_RE.match(inv[i]) and n >= MIN_VERTEBRA_VOXELS}
    order = [n for n in PM.LEVEL_ORDER if n in named]
    inversions = [f"{a}({named[a]:.0f}) not above {b}({named[b]:.0f})" for a, b in zip(order, order[1:])
                  if not named[a] > named[b]]
    unnamed = sorted(i for i, (n, _) in stats.items() if i not in inv and n >= MIN_VERTEBRA_VOXELS)
    ok = len(order) >= 3 and not inversions and not unnamed
    return dict(ok=bool(ok), vertebrae=order, inversions=inversions[:6], n_inversions=len(inversions), unnamed_ids=unnamed)


def resolve_label_map(lab, affine, stats) -> tuple:
    """(LMAP, record). ostk decides the scheme; the anatomy confirms it or overrides it; nothing is guessed."""
    from ostk.labels import SCHEMES, SchemeError, detect_scheme, labels_for
    counts = {i: n for i, (n, _) in stats.items()}
    rec = dict(rule="ostk.labels.labels_for(volume), confirmed by cranio-caudal order of the vertebrae each ostk map "
                    "names; the detected map is kept when it passes, else the one map that passes")
    try:
        det = detect_scheme(lab, counts=counts)
        det_map = labels_for(lab, counts=counts)
        rec.update(detected=det, labels_for_volume={k: det_map.get(k) for k in ("C1", "T1", "L1", "L5", "sacrum", "left_hip")})
    except SchemeError as e:
        det = None
        rec.update(detected=None, detect_error=str(e))
    tests = {s: _order_test(labels_for(scheme=s), stats, affine) for s in SCHEMES}
    rec["order_tests"] = tests
    if det is not None and tests[det]["ok"]:
        chosen, how = det, "detected map confirmed by the anatomy"
    else:
        passing = [s for s, t in tests.items() if t["ok"]]
        if len(passing) != 1:
            raise Refused(f"no single ostk label map fits this volume's anatomy (detected {det}; passing {passing}): "
                          + json.dumps({s: t['inversions'][:2] + t['unnamed_ids'][:4] for s, t in tests.items()}))
        chosen = passing[0]
        how = (f"labels_for(volume) detected {det!r}, whose names are out of cranio-caudal order here "
               f"({tests[det]['n_inversions'] if det in tests else 'n/a'} inversions); labels_for(scheme={chosen!r}) is "
               "the only ostk map in order, and is used")
    rec.update(chosen=chosen, how=how)
    LMAP = {k: int(v) for k, v in labels_for(scheme=chosen).items()}
    return LMAP, rec


# ============================================================================================ transforms
def chain_transforms(cent, chain, base, segments) -> tuple:
    """{vertebra: 4x4 source -> output world motion (FILE world mm, RAS)} and the hinges. polypose_sample
    .build_transforms' construction with a generic fixed base instead of the S1 slab: every vertebra from the base down
    stays; walking up, each vertebra takes the one below composed with its segment's single rotation vector
    (flex_ext, lat_bend, axial_rot) about world +x, +y, +z through the midpoint of the two centroids."""
    from scipy.spatial.transform import Rotation
    b = chain.index(base)
    T = {n: np.eye(4) for n in chain[b:]}
    hinges = {}
    for i in range(b - 1, -1, -1):
        up, lo = chain[i], chain[i + 1]
        seg = f"{up}-{lo}"
        d = segments.get(seg, {})
        centre = 0.5 * (np.asarray(cent[up], float) + np.asarray(cent[lo], float))
        rv = np.radians([float(d.get("flex_ext_deg", 0.0)), float(d.get("lat_bend_deg", 0.0)), float(d.get("axial_rot_deg", 0.0))])
        S = np.eye(4)
        if np.any(rv != 0.0):
            R = Rotation.from_rotvec(rv).as_matrix()
            S[:3, :3] = R
            S[:3, 3] = centre - R @ centre
        T[up] = T[lo] @ S
        hinges[seg] = np.round(centre, 3).tolist()
    return T, hinges


def body_groups(chain, region, LMAP, present_ids, debris_owner) -> list:
    """The rigid bodies, fixed by the region's STRUCTURE (not by which transforms happen to be equal in a frame):
    vertebrae cranial of the top moving segment ride with its upper vertebra as one body; each vertebra between top
    and base is its own; the base and everything caudal (and a sacrum or coccyx label, if any) is the fixed body.
    Debris joins its owner. Any other id has no motion rule and is refused."""
    r = REGIONS[region]
    it, ib = chain.index(r["top"]), chain.index(r["base"])
    inv = {v: k for k, v in LMAP.items()}
    groups = []
    ride = chain[:it + 1]
    groups.append(dict(name="+".join([r["top"]] + (["above"] if len(ride) > 1 else [])), members=ride, fixed=False))
    for n in chain[it + 1:ib]:
        groups.append(dict(name=n, members=[n], fixed=False))
    fixed_names = chain[ib:] + [n for n in ("sacrum", "coccyx") if LMAP.get(n) in present_ids]
    groups.append(dict(name=f"{r['base']}(fixed)" if len(fixed_names) == 1 else f"{r['base']}+below(fixed)",
                       members=fixed_names, fixed=True))
    of = {n: g for g in groups for n in g["members"]}
    for g in groups:
        g["ids"] = sorted(LMAP[n] for n in g["members"] if LMAP[n] in present_ids)
    for i, owner in sorted(debris_owner.items()):
        of[owner]["ids"] = sorted(set(of[owner]["ids"]) | {int(i)})
    covered = sorted(i for g in groups for i in g["ids"])
    stray = sorted(set(present_ids) - set(covered))
    if stray:
        raise Refused(f"label ids {[(i, inv.get(i, 'unnamed')) for i in stray]} have no motion rule (hardware, ribs or an "
                      "unknown structure): refused rather than guessed")
    if len(covered) != len(set(covered)):
        raise RuntimeError("bodies overlap")
    return groups


# ============================================================================================ geometry helpers
def centred_affine(affine, shape):
    """PolyPose's centred frame (polypose_warp.centred_affine: file affine minus torchio's get_center(), the image
    centre (shape - 1) / 2 in world mm) for an array on `affine`. Checked against polypose_warp.centred_affine on the
    full source before a crop uses it."""
    A = np.asarray(affine, float)
    c = A[:3, :3] @ ((np.asarray(shape, float) - 1.0) / 2.0) + A[:3, 3]
    T = np.eye(4)
    T[:3, 3] = -c
    return T @ A


def _bbox_crop(mask, affine, pad=4):
    idx = [np.nonzero(np.asarray(mask).any(axis=tuple(d for d in range(3) if d != ax)))[0] for ax in range(3)]
    if any(len(i) == 0 for i in idx):
        return None, None
    lo = [max(0, int(i.min()) - pad) for i in idx]
    hi = [min(mask.shape[k], int(idx[k].max()) + 1 + pad) for k in range(3)]
    A = np.asarray(affine, float).copy()
    A[:3, 3] = A[:3, :3] @ np.asarray(lo, float) + A[:3, 3]
    return tuple(slice(l, h) for l, h in zip(lo, hi)), A


def _points_world(mask, affine, step=1):
    idx = np.array(np.nonzero(np.asarray(mask)[::step, ::step, ::step]), float) * step
    A = np.asarray(affine, float)
    return (A[:3, :3] @ idx + A[:3, 3:4]).T


def _mask_points_lps(mask, org, sp, step=1):
    """spine_project.project_mask's own voxel -> LPS mapping for a (z, y, x) array."""
    zz, yy, xx = np.nonzero(np.asarray(mask)[::step, ::step, ::step])
    return np.c_[xx * step * sp[0] + org[0], yy * step * sp[1] + org[1], zz * step * sp[2] + org[2]]


def _project(P, M, K, down):
    """spine_project.project_mask's internals: uv = K (M p) / z / down, in the downsampled detector's (col, row)."""
    P = np.asarray(P, float).reshape(-1, 3)
    Pc = (np.asarray(M, float) @ np.c_[P, np.ones(len(P))].T).T[:, :3]
    uvw = (np.asarray(K, float) @ Pc.T).T
    return uvw[:, :2] / uvw[:, 2:3] / down


def _inside(uv, nr, nc, down):
    return (uv[:, 0] >= 0) & (uv[:, 0] < nc / down) & (uv[:, 1] >= 0) & (uv[:, 1] < nr / down)


def ras_to_lps(P):
    return np.asarray(P, float) * np.array([-1.0, -1.0, 1.0])


def _move(T, P):
    P = np.asarray(P, float).reshape(-1, 3)
    return (np.asarray(T, float) @ np.c_[P, np.ones(len(P))].T).T[:, :3]


def _box(uv):
    return [float(uv[:, 0].min()), float(uv[:, 1].min()), float(uv[:, 0].max()), float(uv[:, 1].max())]


def _box_pct(uv, lo=2.0, hi=98.0):
    return [float(np.percentile(uv[:, 0], lo)), float(np.percentile(uv[:, 1], lo)),
            float(np.percentile(uv[:, 0], hi)), float(np.percentile(uv[:, 1], hi))]


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return float(inter / u) if u > 0 else 0.0


def canonical_slots(pts):
    """A copy of spine-detector/src/manifest.py::canonical_slots (y down): 0 superior smaller x, 1 superior larger x,
    2 inferior larger x, 3 inferior smaller x. Geometric, not anatomical."""
    p = np.asarray(pts, dtype=float).reshape(4, 2)
    top = p[np.argsort(p[:, 1])[:2]]
    bot = p[np.argsort(p[:, 1])[2:]]
    s0, s1 = top[np.argsort(top[:, 0])]
    s3, s2 = bot[np.argsort(bot[:, 0])]
    return np.array([s0, s1, s2, s3], dtype=float)


def min_area_rect(pts):
    """The minimum-area enclosing rectangle of 2-D points (rotating calipers over the convex hull's edges), as 4
    corners in order around the rectangle, or None for fewer than 3 non-collinear points."""
    from scipy.spatial import ConvexHull, QhullError
    P = np.asarray(pts, float)
    if len(P) < 3:
        return None
    try:
        h = P[ConvexHull(P).vertices]
    except (QhullError, ValueError):
        return None
    best = None
    for i in range(len(h)):
        e = h[(i + 1) % len(h)] - h[i]
        L = float(np.hypot(e[0], e[1]))
        if L < 1e-9:
            continue
        u = e / L
        v = np.array([-u[1], u[0]])
        pu, pv = h @ u, h @ v
        area = float(np.ptp(pu) * np.ptp(pv))
        if best is None or area < best[0]:
            best = (area, u, v, pu.min(), pu.max(), pv.min(), pv.max())
    if best is None:
        return None
    _, u, v, a0, a1, b0, b1 = best
    return np.array([a0 * u + b0 * v, a1 * u + b0 * v, a1 * u + b1 * v, a0 * u + b1 * v])


# ============================================================================================ plan
def _default_paths(a):
    base = Path(_x(VERSE_UNIFIED)) / f"scan-{a.case}"
    ct = a.ct or str(base / f"scan-{a.case}_ct.nii.gz")
    lab = a.label or str(base / f"scan-{a.case}_msk.nii.gz")
    body = a.body or f"{BODIES}/VERSE_{a.case}_body_msk.nii.gz"
    return _x(ct), _x(lab), _x(body)


def body_on_label_grid(bimg, shape, affine):
    """The SPINEPS body mask on the LABEL's grid: unchanged when the grids agree, else nearest neighbour through world
    mm (the SPINEPS masks sit on SPINEPS's own 0.8 mm PIR grid). Resampled into the CT's grid, never the reverse."""
    from scipy import ndimage as ndi
    B = np.asarray(bimg.dataobj).astype(np.int16)
    if B.shape == tuple(shape) and np.allclose(bimg.affine, affine, atol=1e-3):
        return B, "same grid as the label"
    M = np.linalg.inv(np.asarray(bimg.affine, float)) @ np.asarray(affine, float)
    out = ndi.affine_transform(B, M[:3, :3], offset=M[:3, 3], output_shape=tuple(shape), order=0, mode="constant", cval=0)
    return out.astype(np.int16), (f"resampled from {B.shape} on its own grid onto the label grid {tuple(shape)}, "
                                  "nearest neighbour through world mm")


def plate_corners(lab, affine, LMAP, names, body_rk, body_source, rms_max, dmax):
    """3-D end-plate corners per level (ostk.vertebral_body.endplate_corners_body on the whole-vertebra VerSe mask,
    axes passed explicitly), each plate SCREENED twice: its own rms (ostk.morphometry.level_morphometry's gate) and an
    OUTSIDE check -- each corner must lie within `dmax` mm of the SPINEPS body, an independent isolation of the same
    body. The canal-closing regression (ostk 1b7005c) throws corners 10-17 mm; the rms does not see it. Measured on
    verse823 (local ostk cb43197, 2026-09-26): every plate rms <= 1.15 mm, while the posterior-inferior corner of T10,
    T11, L2 and L3 sat 14.0-20.9 mm from the SPINEPS body; every other corner sat 0.6-4.6 mm from it (two body
    segmentations on different grids, and Frobin's wall extension). The 6 mm default sits between the two. Validity is
    kept per corner as well as per plate, so a level with one bad corner still carries its other three."""
    from scipy.spatial import cKDTree
    from ostk import vertebral_body as VB
    from ostk.geometry import WORLD_SUPERIOR
    out = {}
    for n in names:
        i = LMAP[n]
        rec = dict(level=n, sup_axis=[float(v) for v in WORLD_SUPERIOR], lr=list(LR), body_source=body_source.get(n))
        if n == "C1":
            out[n] = dict(rec, ok=False, why="C1 has no vertebral body")
            continue
        sl, A_sub = _bbox_crop(lab == i, affine, pad=4)
        if sl is None:
            out[n] = dict(rec, ok=False, why="empty label")
            continue
        sub = lab[sl] == i
        body_iso = VB.body_mask(sub, A_sub, sup_axis=WORLD_SUPERIOR, lr=LR)
        bp = _points_world(body_rk[sl] == i, A_sub)
        kd = cKDTree(bp) if len(bp) else None
        rec["independent_body_check"] = body_source.get(n) == "spineps"
        for which in ("superior", "inferior"):
            if n == "C2" and which == "superior":
                rec[which] = dict(ok=False, why="the dens: C2 has no superior end plate")
                continue
            r = VB.endplate_corners_body(sub, A_sub, which, sup_axis=WORLD_SUPERIOR, lr=LR, body=body_iso) \
                if body_iso is not None else None
            if r is None:
                rec[which] = dict(ok=False, why="ostk fitted no plate")
                continue
            ant, post, rms, npts = np.asarray(r[0], float), np.asarray(r[1], float), float(r[2]), int(r[3])
            d = kd.query(np.stack([ant, post]))[0] if kd is not None else np.array([np.inf, np.inf])
            why = []
            rms_ok = rms <= rms_max
            if not rms_ok:
                why.append(f"plate rms {rms:.2f} > {rms_max} mm")
            for tag, dd in (("anterior", d[0]), ("posterior", d[1])):
                if float(dd) > dmax:
                    why.append(f"{tag} corner {float(dd):.1f} mm from the SPINEPS body (> {dmax} mm)")
            rec[which] = dict(anterior=ant.round(3).tolist(), posterior=post.round(3).tolist(), rms_mm=round(rms, 3),
                              n_on_plate=npts, d_ant_body_mm=round(float(d[0]), 2), d_post_body_mm=round(float(d[1]), 2),
                              anterior_ok=bool(rms_ok and d[0] <= dmax), posterior_ok=bool(rms_ok and d[1] <= dmax),
                              ok=not why, why="; ".join(why))
        rec["ok"] = bool(rec.get("superior", {}).get("ok") and rec.get("inferior", {}).get("ok"))
        out[n] = rec
    return out


def _box_corners_world(lo, hi):
    return np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])], float)


def ignore_regions(lab, affine, LMAP, chain, present_ids) -> list:
    """Unlabelled bone beside the chain that a detector may box: the sacrum below L5 (when no sacrum label) and the
    skull above C1. A 3-D box on the neighbouring vertebra's extent, moved with that vertebra, projected per frame;
    a prediction inside it is neither a true nor a false positive."""
    out = []
    if "L5" in chain and LMAP.get("sacrum") not in present_ids:
        P = _points_world(lab == LMAP["L5"], affine, step=2)
        lo, hi = P.min(0), P.max(0)
        out.append(dict(gt_id="sacrum_unlabelled", cls=1, anchor="L5",
                        corners_world=_box_corners_world([lo[0] - 15, lo[1] - 20, lo[2] - 70],
                                                         [hi[0] + 15, hi[1] + 20, lo[2] + 5]).round(2).tolist(),
                        rule="L5 extent +-15 mm (L-R), +-20 mm (A-P), from 70 mm below its lowest voxel to 5 mm above"))
    if "C1" in chain:
        P = _points_world(lab == LMAP["C1"], affine, step=2)
        lo, hi = P.min(0), P.max(0)
        out.append(dict(gt_id="skull_unlabelled", cls=0, anchor="C1",
                        corners_world=_box_corners_world([lo[0] - 30, lo[1] - 30, hi[2] - 5],
                                                         [hi[0] + 30, hi[1] + 30, hi[2] + 60]).round(2).tolist(),
                        rule="C1 extent +-30 mm, from 5 mm below its highest voxel to 60 mm above; moved with C1"))
    return out


def cmd_rom_check(a) -> int:
    try:
        rom = load_rom(a.rom, a.spec)
        caps = require_rows(rom, region_segments(ORDINARY, a.region))
    except Refused as e:
        print(f"REFUSED region {a.region}: {e}")
        return 3
    print(f"ROM OK for region {a.region}: " + ", ".join(f"{s} flex {c['flex']} ext {c['ext']} ({c.get('source')})"
                                                      for s, c in caps.items()))
    return 0


def cmd_plan(a) -> int:
    t0 = time.time()
    import nibabel as nib
    import polypose_invariants as INV
    import polypose_sample as PS
    INV.find_ostk()
    from ostk import vertebral_body as VB
    from ostk.geometry import WORLD_SUPERIOR
    assert INV.MIN_VERTEBRA_VOXELS == MIN_VERTEBRA_VOXELS
    ct_p, lab_p, body_p = _default_paths(a)
    seq = Path(_x(a.seq_dir)) if a.seq_dir else Path(OUT_ROOT) / seq_name(a.case, a.region, a.frac)
    try:
        # 1. the region's ROM rows, on the ordinary chain, before a volume is read
        rom = load_rom(a.rom, a.spec)
        require_rows(rom, region_segments(ORDINARY, a.region))
        # 2. the source on one grid
        li = nib.load(lab_p)
        affine = np.asarray(li.affine, float)
        ct_rec = None
        if os.path.exists(ct_p):
            ci = nib.load(ct_p)
            if tuple(ci.shape) != tuple(li.shape) or not np.allclose(ci.affine, affine, atol=1e-3):
                raise Refused(f"CT grid {ci.shape} differs from the label's {li.shape}")
            ct_rec = dict(path=ct_p, sha256=PM.sha256_file(ct_p), shape=list(ci.shape), dtype=str(ci.get_data_dtype()))
        elif not a.dry_run:
            raise Refused(f"no CT at {ct_p}")
        lab = np.asarray(li.dataobj).astype(np.int16)
        stats = label_stats(lab)
        LMAP, lab_rec = resolve_label_map(lab, affine, stats)
        inv = {v: k for k, v in LMAP.items()}
        present = sorted(stats)
        cent = {inv[i]: _world(affine, c) for i, (n, c) in stats.items() if i in inv}
        vcount = {inv[i]: n for i, (n, _) in stats.items() if i in inv and PM.VERTEBRA_RE.match(inv[i])}
        debris = sorted(n for n, c in vcount.items() if c < MIN_VERTEBRA_VOXELS)
        chain = [n for n in PM.LEVEL_ORDER if n in vcount and n not in debris and n != "S1"]
        want = [n for n in ORDINARY if chain and ORDINARY.index(chain[0]) <= ORDINARY.index(n) <= ORDINARY.index(chain[-1])] \
            if all(n in ORDINARY for n in chain) else None
        if want is None or chain != want:
            raise Refused(f"the labelled chain {chain} is not a contiguous ordinary chain (a T13 or L6 has no ROM rows here, "
                          "and a gap has no segment)")
        segs = region_segments(chain, a.region)
        caps = require_rows(rom, segs)
        r = REGIONS[a.region]
        iso = a.iso or r["iso"]
        if iso not in chain:
            raise Refused(f"isocentre level {iso} not labelled")
        debris_owner = {LMAP[n]: min(chain, key=lambda c: float(np.linalg.norm(cent[c] - cent[n]))) for n in debris}
        groups = body_groups(chain, a.region, LMAP, set(present), debris_owner)
    except Refused as e:
        print(f"REFUSED {a.case} region {a.region}: {e}")
        return 3

    # 3. the motion: every frame's segments and every body's rigid transform
    n_frames = int(a.frames)
    frames, hinges = [], None
    for k in range(n_frames):
        ak = phase(k, n_frames)
        sg = frame_segments(ak, caps, a.frac, a.multiplier)
        Tn, hinges = chain_transforms(cent, chain, r["base"], sg)
        gT = {}
        for g in groups:
            mats = [Tn[m] for m in g["members"] if m in Tn] or [np.eye(4)]
            if any(not np.array_equal(mats[0], M) for M in mats[1:]):
                raise RuntimeError(f"body {g['name']} is not rigid in frame {k}")
            gT[g["name"]] = np.round(mats[0], 10).tolist()
        frames.append(dict(frame=k, stem=stem_for(a.case, a.region, a.frac, k), phase=round(ak, 9), segments=sg,
                           total_flex_ext_deg=round(sum(v["flex_ext_deg"] for v in sg.values()), 6), group_T=gT))
    verify_frame = int(np.argmin([f["phase"] for f in frames]))

    # 4. the body mask: SPINEPS bodies on the label grid, re-keyed to the VerSe names by overlap, ostk where missing
    seq.mkdir(parents=True, exist_ok=True)
    (seq / "sources").mkdir(exist_ok=True)
    guard = None
    try:
        import spineps_ids as SI
        rep = SI.check_ids(body_p, "auto", kind="body")
        guard = dict(verdict=rep.get("verdict"), reasons=rep.get("reasons"))
    except Exception as e:  # noqa: BLE001  (information only: the names below come from the overlap, not the ids)
        guard = dict(verdict=None, error=repr(e)[:300])
    bimg = nib.load(body_p)
    body_on, grid_note = body_on_label_grid(bimg, lab.shape, affine)
    body_rk, rk_table = PS.rekey_body_mask(body_on, lab, LMAP)
    body_rk = body_rk.astype(np.int16)
    iso_z = cent[iso][2]
    near = [n for n in chain if abs(cent[n][2] - iso_z) <= float(a.corner_radius_mm)]
    have = set(int(x) for x in np.unique(body_rk)) - {0}
    body_source = {inv[i]: "spineps" for i in have if i in inv}
    for n in near:
        if LMAP[n] in have or n == "C1":
            continue
        sl, A_sub = _bbox_crop(lab == LMAP[n], affine, pad=2)
        b = VB.body_mask(lab[sl] == LMAP[n], A_sub, sup_axis=WORLD_SUPERIOR, lr=LR)
        if b is not None and b.any():
            view = body_rk[sl]
            view[b & (view == 0)] = LMAP[n]
            body_source[n] = "ostk.vertebral_body.body_mask (no SPINEPS body re-keyed to this level)"
    rk_path = seq / "sources" / f"{a.case}_body_msk_rekeyed.nii.gz"
    _save_nifti(body_rk, affine, li.header, np.int16, rk_path)

    # 5. the 3-D end-plate corners, once, on the source
    corners = plate_corners(lab, affine, LMAP, near, body_rk, body_source, a.rms_max, a.corner_body_mm)

    # 6. the crop: the S-I voxel axis around the isocentre level (the rendered field is ~200 mm at the isocentre)
    crop = None
    if float(a.crop_mm) > 0:
        A = affine
        ax = int(np.argmax(np.abs(A[2, :3]) / np.linalg.norm(A[:3, :3], axis=0)))
        sp_ax = float(np.linalg.norm(A[:3, ax]))
        c = float(stats[LMAP[iso]][1][ax])
        lo = max(0, int(math.floor(c - float(a.crop_mm) / sp_ax)))
        hi = min(lab.shape[ax], int(math.ceil(c + float(a.crop_mm) / sp_ax)) + 1)
        lo_v = [0, 0, 0]
        lo_v[ax] = lo
        Aw = A.copy()
        Aw[:3, 3] = A[:3, :3] @ np.asarray(lo_v, float) + A[:3, 3]
        crop = dict(axis=ax, lo=lo, hi=hi, half_mm=float(a.crop_mm), affine=Aw.tolist(), centre_level=iso,
                    note="warped volumes are this sub-grid of the source grid (same spacing and orientation, origin "
                         "moved to voxel lo): voxels pulled from beyond it read as air, as beyond the CT's own field")

    fid = [dict(name=g["name"], members=g["members"], ids=g["ids"], fixed=g["fixed"]) for g in groups]
    limitations = [
        r["note"],
        "VerSe labels are whole vertebrae: body truth comes from the SPINEPS body mask re-keyed to the VerSe names by "
        "overlap (>= 0.9 inside one vertebra label); levels without one near the isocentre use ostk's body isolation "
        "and say so (body_source)",
        "the fixed base replaces the generator's fixed pelvis. Its check (base_fixed) keeps pelvis_fixed's identity-"
        "transform test but judges the voxels as for one vertebra -- field p95 <= field_rigid_vox and Dice >= dice_min "
        "-- because pelvis_fixed's Dice >= 0.999 was set for the pelvis and a correct warp misses it on a base next to "
        "the largest moving segment; the 0.999 reading is recorded, not gated",
        f"caps are in vitro (7.5-10 N m); at frac {a.frac} each segment reaches {a.frac:g} x its cap",
        "soft tissue and the scanner table follow the blended field; the table is stripped per frame at render time",
        "one isocentre, fixed from frame 0: the spine moves in the field, it is not re-centred",
        "3-D mid-sagittal end-plate corners are not the 2-D silhouette corners a detector learned from film; the "
        "silhouette quad is written beside them as a second corner truth",
    ]
    plan = {
        "schema": SCHEMA, "created_utc": _now(), "node": platform.node(), "argv": sys.argv, "dry_run": bool(a.dry_run),
        "sequence": seq.name, "seq": stem_for(a.case, a.region, a.frac, 0).rsplit("_", 2)[0],
        "eval": {"held_out": False, "not_held_out": NOT_HELD_OUT,
                 "level_prototype": f'--not-held-out "{NOT_HELD_OUT}"',
                 "why": "every VerSe CT is inside the v9 training renders; nothing scored on these frames is held out"},
        "source": {"collection": "verse", "case": a.case, "series": a.case,
                   "ct": ct_rec or dict(path=ct_p, sha256=None, note="dry run: CT not read"),
                   "label": dict(path=lab_p, sha256=PM.sha256_file(lab_p), shape=list(lab.shape),
                                 dtype=str(li.get_data_dtype())),
                   "affine": affine.tolist(), "zooms": [float(z) for z in li.header.get_zooms()[:3]],
                   "axcodes": "".join(nib.aff2axcodes(affine)),
                   "body_spineps": dict(path=body_p, sha256=PM.sha256_file(body_p), grid=grid_note, id_guard=guard,
                                        naming="names from the overlap with the VerSe label (rekey_body_mask), not from "
                                               "the SPINEPS ids"),
                   "body_rekeyed": dict(path=str(rk_path), sha256=PM.sha256_file(str(rk_path)), table=rk_table,
                                        body_source=body_source)},
        "labels": dict(lab_rec, map=LMAP, present_ids=present, chain=chain, debris=debris,
                       debris_ids=sorted(LMAP[n] for n in debris), voxels=vcount),
        "motion": {"region": a.region, "top": r["top"], "base": r["base"], "iso": iso,
                   "iso_centroid_vox": [float(v) for v in stats[LMAP[iso]][1]],
                   "iso_centroid_world": [float(v) for v in cent[iso]], "segments": segs,
                   "caps": caps, "frac": float(a.frac), "multiplier": float(a.multiplier),
                   "multiplier_note": "m = 1: an ordinary (non-transitional) spine, as declared for this source",
                   "n_frames": n_frames, "fps": 15, "phase": "a_k = -sin(2 pi k / N)",
                   "sign": "positive = extension (lordosis-increasing): rotation about world +x (RAS) through the "
                           "midpoint of the two vertebral centroids, composed from the fixed base upward",
                   "verify_frame": verify_frame,
                   "verify_frame_note": "the build plan named frame 30 as the largest flexion; a_30 = 0 (neutral), so "
                                        "verify_equivalence runs on argmin a_k",
                   "hinges_world_mm": hinges,
                   "rom": {k: rom[k] for k in ("path", "sha256", "copied_from", "spec_sha256", "spec_sha256_lf",
                                               "spec_is_copied_version")},
                   "citations": {c.get("source"): rom["citations"].get(c.get("source")) for c in caps.values()}},
        "bodies": fid, "id_group": {str(i): g["name"] for g in groups for i in g["ids"]},
        "frames": frames,
        "corners": corners, "corner_screen": dict(rms_max_mm=a.rms_max, body_dist_max_mm=a.corner_body_mm,
                                                  radius_mm=a.corner_radius_mm, levels=near),
        "ignore_regions": ignore_regions(lab, affine, LMAP, chain, set(present)),
        "crop": crop,
        "render": dict(pool=a.pool, anchor_tag=a.anchor_tag, lat_deg=float(a.lat), tilt_deg=0.0, roll_deg=0.0,
                       card=a.card, down=int(a.down), seed=int(a.seed), field=a.field, out_px=1024),
        "limitations": limitations,
        "tool": {"path": "tools/polypose/cine_render.py", "sha256": PM.sha256_file(__file__)},
        "ostk": {m: PM.sha256_file(os.path.join(os.path.dirname(VB.__file__), f"{m}.py")) for m in ("vertebral_body", "labels")},
        "plan_seconds": round(time.time() - t0, 1),
    }
    _dump(seq / "frames.json", plan)
    (seq / "README.md").write_text(_readme(plan))
    ok_c = sum(1 for v in corners.values() if v.get("ok"))
    print(f"PLANNED {seq.name}: {n_frames} frames, region {a.region} ({segs[0]} .. {segs[-1]}, {r['base']} fixed), "
          f"frac {a.frac}; labels {lab_rec['chosen']} ({lab_rec['how']}); chain {chain[0]}..{chain[-1]}; "
          f"{len(groups)} bodies; corners ok {ok_c}/{len(corners)}; verify frame {verify_frame}; "
          f"crop {crop and (crop['lo'], crop['hi'])}; NOT HELD OUT ({NOT_HELD_OUT}) -> {seq}")
    return 0


def _readme(P):
    m = P["motion"]
    return f"""# {P['sequence']}: synthetic flexion-extension cine (tools/polypose/cine_render.py)

**NOT HELD OUT: {P['eval']['not_held_out']}.** Every VerSe CT is inside the v9 training renders. Run level_prototype on
these frames with `{P['eval']['level_prototype']}`; no number from them is a held-out result.

- Source: VerSe {P['source']['case']} ({P['source']['label']['path']}), label map `{P['labels']['chosen']}`
  ({P['labels']['how']}).
- Region `{m['region']}`: segments {', '.join(m['segments'])} move; {m['base']} is fixed; isocentre on {m['iso']}.
- Motion: {m['n_frames']} frames at {m['fps']} fps, {m['phase']}, segment angle = frac x m x (a*ext if a>0 else
  a*flex), frac {m['frac']}, m {m['multiplier']}; caps from {m['rom']['path']} (rows copied from sampling_spec.json).
- Frames: images/<stem>.png (device-styled), images_logor/<stem>.png (unstyled -log -> window_or); truth
  meta/<stem>.json; warped volumes volumes/f###_*.nii.gz; invariants checks/f###.json; QC qc/.

Limitations:
""" + "".join(f"- {x}\n" for x in P["limitations"])


# ============================================================================================ warp
def _crop_slices(P, shape):
    c = P.get("crop")
    if not c:
        return tuple(slice(0, n) for n in shape), np.asarray(P["source"]["affine"], float)
    sl = [slice(0, n) for n in shape]
    sl[int(c["axis"])] = slice(int(c["lo"]), int(c["hi"]))
    return tuple(sl), np.asarray(c["affine"], float)


def transforms_by_id(P, k) -> dict:
    fr = P["frames"][k]
    return {int(i): np.asarray(fr["group_T"][g], float) for i, g in P["id_group"].items()}


def frame_key(P, k) -> str:
    """sha256 of everything one warped frame depends on in the plan: its bodies' transforms, the body partition, the
    crop, the label map, whether it is the verify frame, and the source files' sha256. A re-plan into the same
    sequence directory (a label, corner or ROM fix at the same frac keeps the directory name) changes it whenever the
    warp would change, and only then."""
    k = int(k)
    fr = P["frames"][k]
    src = P["source"]
    obj = dict(frame=k, group_T=fr["group_T"], bodies=[[g["name"], g["ids"], bool(g["fixed"])] for g in P["bodies"]],
               id_group=P["id_group"], crop=P.get("crop"), label_map=P["labels"]["map"],
               verify=k == int(P["motion"]["verify_frame"]),
               sources={r: (src.get(r) or {}).get("sha256") for r in ("ct", "label", "body_rekeyed")})
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=_jsonable).encode()).hexdigest()


def _warp_record(seq, P, k):
    """checks/f###.json when it says the volumes on disk were warped for THIS plan's frame; None when there is no
    record (volumes placed by hand, e.g. a stand-in test); SystemExit when the record is another plan's, or a warp
    that never finished (render and gt would otherwise pair the current plan with stale volumes)."""
    p = Path(seq) / "checks" / f"f{int(k):03d}.json"
    if not p.exists():
        return None
    c = json.loads(p.read_text())
    want = frame_key(P, k)
    if c.get("frame_key") != want:
        state = "a warp that did not finish" if c.get("in_progress") else \
            "a refused warp" if c.get("refused") else "another plan"
        raise SystemExit(f"f{int(k):03d}: the volumes on disk are from {state} (checks frame_key "
                         f"{str(c.get('frame_key'))[:12]} != this plan's {want[:12]}): re-run `warp --frame {int(k)}`")
    return c


def base_fixed(src_label, out_label, disp, affine, T, fixed_ids, tol) -> dict:
    """The fixed base did not move, judged as ONE vertebra rather than by the pelvis's rule.

    polypose_invariants.RowCheck.pelvis_fixed holds the pelvis -- hips, sacrum and femora, millions of voxels, far from
    any moving segment -- to Dice >= 0.999. The cine's base is a single vertebra (L5 on the lumbar region) abutting the
    largest moving segment, and the polyrigid blend legitimately moves its facet voxels by up to about 2 voxels: a CPU
    re-computation of polypose_warp's field on the verse823 slab (review, 2026-09-26) read L5 Dice 0.99883 at frame 15
    on a CORRECT warp, with field p95 0.10 voxel, max 1.81, pose 0.18 deg / 0.05 mm. Gated here instead:
      1. pelvis_fixed's own test that every base id's transform is the identity (fused_transform_eps);
      2. the field inside each base id is that identity: field_matches_transforms' criterion, p95 <= field_rigid_vox,
         over the id's source and output voxels;
      3. Dice(source, output) >= dice_min, the rule label_rigidity holds every vertebra to against its rigid target
         (for the base, the source itself); label_rigidity also holds the base's moment pose to 1 deg / 0.5 mm.
    The pelvis rule's reading (worst Dice >= 0.999) is reported as pelvis_rule_0999, not gated. No base voxel in the
    warped slab fails: the invariant would be unverifiable."""
    import polypose_invariants as INV
    eps, vtol, dmin = float(tol["fused_transform_eps"]), float(tol["field_rigid_vox"]), float(tol["dice_min"])
    rng = np.random.default_rng(0)
    bad, per, n = [], {}, 0
    worst_d, worst_p95, worst_max = 1.0, 0.0, 0.0
    for i in sorted(int(x) for x in fixed_ids):
        Ti = np.asarray(T.get(i, np.eye(4)), float)
        if not np.allclose(Ti, np.eye(4), atol=eps):
            bad.append(f"{i}: transform not identity")
        a, b = np.asarray(src_label) == i, np.asarray(out_label) == i
        if not (a.any() or b.any()):
            continue
        n += 1
        d = INV.dice(a, b)
        idx = np.array(np.nonzero(a | b))
        if idx.shape[1] > 20000:
            idx = idx[:, rng.choice(idx.shape[1], 20000, replace=False)]
        M = INV.vox_to_vox(affine, Ti)
        rigid = M[:3, :3] @ idx.astype(float) + M[:3, 3:4] - idx
        err = np.linalg.norm(np.asarray(disp)[:, idx[0], idx[1], idx[2]] - rigid, axis=0)
        p95, mx = float(np.percentile(err, 95)), float(err.max())
        worst_d, worst_p95, worst_max = min(worst_d, d), max(worst_p95, p95), max(worst_max, mx)
        per[str(i)] = dict(dice=round(d, 5), field_p95_vox=round(p95, 4), field_max_vox=round(mx, 3),
                           voxels_src=int(a.sum()), voxels_out=int(b.sum()))
        if d < dmin:
            bad.append(f"{i}: Dice {d:.4f} < {dmin}")
        if p95 > vtol:
            bad.append(f"{i}: field vs identity p95 {p95:.2f} vox > {vtol}")
    if n == 0:
        bad.append("no base voxel in the warped volume: the fixed base is unverifiable")
    value = dict(dice_min=round(worst_d, 5), field_p95_vox=round(worst_p95, 4), field_max_vox=round(worst_max, 3),
                 pelvis_rule_0999=bool(n > 0 and worst_d >= 0.999), per_id=per)
    note = "; ".join(bad)
    note += (" | " if note else "") + ("replaces pelvis_fixed's Dice >= 0.999 (set for the pelvis) with the "
                                       "single-vertebra rule; pelvis rule "
                                       f"{'met' if value['pelvis_rule_0999'] else 'NOT met'} (recorded, not gated)")
    return INV.R("base_fixed", value, dict(transform_eps=eps, field_p95_vox=vtol, dice_min=dmin), not bad, note)


def cmd_warp(a) -> int:
    import nibabel as nib
    import torch
    import polypose_invariants as INV
    import polypose_warp as PW
    seq = Path(_x(a.seq_dir))
    P = _load_plan(seq)
    if P.get("dry_run"):
        print("REFUSED: a dry-run plan (the CT was not read); re-plan without --dry-run")
        return 3
    k = int(a.frame)
    fr = P["frames"][k]
    (seq / "volumes").mkdir(exist_ok=True)
    (seq / "checks").mkdir(exist_ok=True)
    outp = {r: seq / "volumes" / f"f{k:03d}_{r}.nii.gz" for r in ("ct", "label", "body_msk")}
    chk_p = seq / "checks" / f"f{k:03d}.json"
    key = frame_key(P, k)
    if not a.force and chk_p.exists() and all(p.exists() for p in outp.values()):
        prev = json.loads(chk_p.read_text())
        if prev.get("frame_key") == key:
            print(f"f{k:03d}: exists for this plan (frame_key {key[:12]}), skipped (--force to redo)")
            return 0
        print(f"f{k:03d}: the volumes on disk are not this plan's (checks frame_key {str(prev.get('frame_key'))[:12]} "
              f"!= {key[:12]}{'; a warp that did not finish' if prev.get('in_progress') else ''}): redoing")
    t0 = time.time()
    src = P["source"]
    for role, rec in (("label", src["label"]), ("ct", src["ct"]), ("body_rekeyed", src["body_rekeyed"])):
        if PM.sha256_file(rec["path"]) != rec["sha256"]:
            print(f"REFUSED: {role} {rec['path']} is not the file the plan read (sha256 differs)")
            return 2
    # before any volume is overwritten: a record that claims no plan, so a job killed mid-write leaves volumes that
    # render / gt / check refuse and the next warp redoes (frame_key is set only once all three volumes are written)
    plan_sha = PM.sha256_file(str(seq / "frames.json"))
    _dump(chk_p, dict(frame=k, stem=fr["stem"], frame_key=None, plan_frame_key=key, plan_sha256=plan_sha,
                      in_progress=True, started_utc=_now(), node=platform.node(), all_pass=False))
    ci, li, bi = nib.load(src["ct"]["path"]), nib.load(src["label"]["path"]), nib.load(src["body_rekeyed"]["path"])
    A = np.asarray(li.affine, float)
    sl, Aw = _crop_slices(P, li.shape)
    ct = np.asarray(ci.dataobj[sl], dtype=np.float32)
    lab = np.asarray(li.dataobj[sl]).astype(np.int16)
    body = np.asarray(bi.dataobj[sl]).astype(np.int16)
    zooms = tuple(float(z) for z in li.header.get_zooms()[:3])
    LMAP = {k_: int(v) for k_, v in P["labels"]["map"].items()}
    T = transforms_by_id(P, k)
    present = set(int(i) for i in np.unique(lab)) - {0}
    bodies_full, bodies_crop, dropped = [], [], []
    for g in P["bodies"]:
        Tg = np.asarray(fr["group_T"][g["name"]], float)
        bodies_full.append((g["ids"], Tg))
        ids_in = [i for i in g["ids"] if i in present]
        (bodies_crop.append((ids_in, Tg)) if ids_in else dropped.append(g["name"]))
    stray = sorted(present - {i for ids, _ in bodies_crop for i in ids})
    if stray:
        print(f"REFUSED: ids {stray} in the crop belong to no body")
        return 2
    dev = a.device if a.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu")
    if dev == "cpu":
        torch.set_num_threads(max(1, int(os.environ.get("SLURM_CPUS_PER_TASK", "4"))))
    # PolyPose's centred frame: torchio's own on the full source, and the formula on the crop only once it reproduces it
    Ac_full, _ = PW.centred_affine(src["ct"]["path"])
    ferr = float(np.abs(centred_affine(A, li.shape) - Ac_full).max())
    if ferr > 1e-3:
        print(f"REFUSED: the centred-frame formula disagrees with polypose_warp.centred_affine by {ferr:.2e}")
        return 2
    A_c = Ac_full if P.get("crop") is None else centred_affine(Aw, lab.shape)
    facts = dict(frame=k, stem=fr["stem"], phase=fr["phase"], total_flex_ext_deg=fr["total_flex_ext_deg"],
                 frame_key=None, plan_frame_key=key, plan_sha256=plan_sha,
                 bodies_dropped_by_crop=dropped, centred_formula_err=ferr, device=dev, kernel=a.kernel, node=platform.node())
    if k == int(P["motion"]["verify_frame"]):
        cvox = np.round(np.asarray(P["motion"]["iso_centroid_vox"], float))     # full-grid voxel of the isocentre level
        eq = PW.verify_equivalence(src["ct"]["path"], src["label"]["path"], bodies_full, A, cvox, size=64, device=dev,
                                   tmpdir=str(seq / "sources"), kernel=a.kernel)
        facts["equivalence"] = eq
        if not eq["ok"]:
            _dump(chk_p, dict(facts, all_pass=False, refused="chunked field disagrees with the PolyRigid class"))
            print(f"REFUSED f{k:03d}: equivalence failed {eq}")
            return 4
    res = PW.warp_volumes(ct, lab, body, Aw, A_c, zooms, bodies_crop, frame="moved", device=dev, kernel=a.kernel)
    samp = ct[::7, ::7, ::7]
    int_src = bool(np.all(samp == np.rint(samp)))
    if int_src:
        res["ct"] = np.rint(res["ct"])
    _save_nifti(res["ct"], Aw, ci.header, np.float32, outp["ct"])
    _save_nifti(res["label"], Aw, li.header, np.int16, outp["label"])
    _save_nifti(res["body"], Aw, bi.header, np.int16, outp["body_msk"])
    facts.update(warp=res["facts"], ct_rounded_to_integer_hu=int_src, seconds_warp=round(time.time() - t0, 1),
                 outputs={r: dict(path=str(p), sha256=PM.sha256_file(str(p))) for r, p in outp.items()},
                 frame_key=key)          # all three volumes are on disk and are this plan's frame
    # the fov-out voxels near the isocentre: pulled from beyond the crop or the CT, they read as air in the render
    ax = int(P["crop"]["axis"]) if P.get("crop") else int(np.argmax(np.abs(Aw[2, :3])))
    per = res["fov_out"].sum(axis=tuple(d for d in range(3) if d != ax))
    zs = Aw[2, ax] * np.arange(len(per)) + Aw[2, 3]
    iso_z = float(P["motion"]["iso_centroid_world"][2])
    facts["fov_out_within_150mm_of_iso"] = int(per[np.abs(zs - iso_z) <= 150.0].sum())
    # the geometric invariants of polypose_invariants (checker v4), on the arrays in memory
    fixed = {i for g in P["bodies"] if g["fixed"] for i in g["ids"] if i in present}
    row = {"applied_transforms": {str(i): M.tolist() for i, M in T.items()},
           "source": {"debris_ids": P["labels"]["debris_ids"]}, "tolerances": {}}
    chk = INV.RowCheck(row, rom=None, env=None)
    chk.src_label, chk.out_label, chk.field, chk.affine, chk.LMAP = lab, res["label"], res["disp"], Aw, LMAP
    results = {}
    # the fixed base plays the pelvis's part, judged as one vertebra (base_fixed's docstring says why not with
    # pelvis_fixed's Dice >= 0.999)
    for name, fn in (("label_rigidity", chk.label_rigidity), ("jacobian_positive", chk.jacobian_positive),
                     ("base_fixed", lambda: base_fixed(lab, res["label"], res["disp"], Aw, T, fixed, chk.tol)),
                     ("field_matches_transforms", chk.field_matches_transforms),
                     ("label_set_preserved", chk.label_set_preserved)):
        try:
            results[name] = fn()
        except Exception as e:  # noqa: BLE001
            results[name] = dict(name=name, status="fail", note=f"raised {e!r}"[:400])
    if all(np.allclose(M, np.eye(4), atol=1e-12) for M in T.values()):
        d_ct = float(np.abs(res["ct"] - ct).max())
        same = bool(np.array_equal(res["label"], lab) and np.array_equal(res["body"], body))
        results["identity_frame_exact"] = dict(name="identity_frame_exact", value=dict(labels_equal=same, ct_max_abs_hu=d_ct),
                                               threshold=0.5, status="pass" if same and d_ct <= 0.5 else "fail",
                                               note="every transform is the identity: the warp must return the source")
    facts["checker"] = INV.CHECKER_VERSION
    facts["checks"] = results
    facts["all_pass"] = all(v.get("status") in ("pass", "n/a") for v in results.values())
    facts["seconds_total"] = round(time.time() - t0, 1)
    _dump(chk_p, facts)
    bad = sorted(k_ for k_, v in results.items() if v.get("status") == "fail")
    print(f"{'WARP_OK' if not bad else 'WARP_CHECK_FAIL'} f{k:03d} phase {fr['phase']:+.3f} total "
          f"{fr['total_flex_ext_deg']:+.2f} deg {facts['seconds_total']} s" + (f" failed={bad}" if bad else ""))
    return 0 if not bad else 1


# ============================================================================================ render
def _pick_anchor(pool, tag):
    poses = [p for p in json.load(open(_x(pool)))["poses"] if not p.get("arc")]
    hit = [p for p in poses if p.get("tag") == tag]
    if len(hit) != 1:
        raise SystemExit(f"{len(hit)} poses tagged {tag!r} in {pool}")
    return hit[0]


def _strip_table(vol):
    """devcorpus_build.load_subject's table strip: keep the largest connected region above -300 HU after a small
    opening, set the rest to air."""
    from scipy.ndimage import binary_opening, label
    body = binary_opening(vol > -300.0, iterations=2)
    lab, n = label(body)
    if n > 1:
        sizes = np.bincount(lab.ravel())
        sizes[0] = 0
        body = lab == int(sizes.argmax())
    return np.where(body, vol, -1000.0).astype(np.float32)


def _volume_lps(seq, k, role):
    import spine_project as SP
    p = Path(seq) / "volumes" / f"f{k:03d}_{role}.nii.gz"
    if not p.exists():
        raise SystemExit(f"no {p}: the warp of frame {k} has not landed")
    return SP.load_lps(str(p))


def cmd_render(a) -> int:
    import carmlspine_labels as CL
    import deepfluoro_render as DR
    import device_style as DS
    import pose_arc as PA
    import spine_project as SP
    from PIL import Image
    seq = Path(_x(a.seq_dir))
    P = _load_plan(seq)
    k = int(a.frame)
    fr = P["frames"][k]
    R = P["render"]
    t0 = time.time()
    _warp_record(seq, P, k)                 # refuses volumes warped for another plan
    vol, org, sp = _volume_lps(seq, k, "ct")
    if not a.keep_table:
        vol = _strip_table(vol)
    dev = DS.load_device(R["card"])
    RP = DS.rp_tables()
    state_p = seq / "render_state.json"
    if k == 0:
        lab0, org_l, sp_l = _volume_lps(seq, 0, "label")   # frame 0's own volumes, guarded above
        if not (np.allclose(org_l, org) and np.allclose(sp_l, sp)):
            raise SystemExit("frame 0 label and CT are not on one grid")
        iso = P["motion"]["iso"]
        c0 = SP.centroid_mm(lab0 == int(P["labels"]["map"][iso]), org, sp)
        anchor = _pick_anchor(R["pool"], R["anchor_tag"])
        pose = PA.arc_pose(anchor, float(R["lat_deg"]), float(R["tilt_deg"]), float(R["roll_deg"]),
                           tag=f"cine/lat{R['lat_deg']:+.0f}")
        back = PA.angles_of(pose)
        org_new = org - c0 + np.asarray(anchor["anchor"], float)
        state = dict(created_utc=_now(), frame0_stem=fr["stem"], iso=iso, iso_centroid_lps_frame0=c0.tolist(),
                     org_lps=org.tolist(), sp=sp.tolist(), shape_zyx=list(vol.shape), org_new_lps=org_new.tolist(),
                     shift_lps=(org_new - org).tolist(), anchor_tag=anchor["tag"], anchor_lps=anchor["anchor"],
                     pose={k_: pose[k_] for k_ in ("K", "ext", "T", "nr", "nc", "px_mm", "anchor", "tag")},
                     angles=dict(lat_deg=back["lat_deg"], tilt_deg=back["tilt_deg"], roll_deg=back["roll_deg"]),
                     sod_mm=back["sod_mm"], sid_mm=abs(float(pose["K"][0][0])) * float(pose["px_mm"]),
                     down=int(R["down"]), pitch_mm=float(pose["px_mm"]) * int(R["down"]),
                     table_stripped=not a.keep_table, card=dict(name=R["card"],
                                                                 sha256=PM.sha256_file(str(DS.DOCS / f"{R['card']}.json"))),
                     seeds=dict(terms=[R["seed"], 11], noise=[R["seed"], 23], field=[R["seed"], 31]),
                     not_held_out=NOT_HELD_OUT)
        state["magnification"] = state["sid_mm"] / state["sod_mm"]
        state["px_mm_iso"] = state["pitch_mm"] / state["magnification"]
    else:
        if not state_p.exists():
            raise SystemExit(f"no {state_p}: render frame 0 first (the pose, isocentre and exposure are fixed from it)")
        state = json.loads(state_p.read_text())
        if not (np.allclose(state["org_lps"], org) and np.allclose(state["sp"], sp)):
            raise SystemExit(f"frame {k} is not on frame 0's grid")
    pose = state["pose"]
    org_new = np.asarray(state["org_new_lps"], float)
    d = dict(K=np.asarray(pose["K"], float), ext=np.asarray(pose["ext"], float), T=np.asarray(pose["T"], float),
             nr=pose["nr"], nc=pose["nc"], vol=vol, org=org_new, sp=sp)
    trans, water, bone, hit, trunc = DR.raycast(d, down=int(state["down"]))
    H, W = water.shape
    if k == 0:
        yy, xx = np.mgrid[0:H, 0:W]
        disc = ((yy - H / 2) ** 2 + (xx - W / 2) ** 2 <= (0.06 * min(H, W)) ** 2) & hit
        thick = float(np.median(water[disc])) if disc.any() else float("nan")
        t = DS.sample_terms(dev, 1, np.random.default_rng(state["seeds"]["terms"]),
                            cond={"thickness_cm": thick} if np.isfinite(thick) else None)[0]
        t["rot180"] = False
        state["thickness_cm_frame0"] = thick
        state["terms"] = {k_: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v) if isinstance(v, (int, float, np.integer, np.floating)) else v)
                          for k_, v in t.items()}
        if R["field"] == "card":
            field = DS.field_mask(dev, (H, W), np.random.default_rng(state["seeds"]["field"]), t)
            np.savez_compressed(seq / "render_field.npz", field=field)
        state.update(img_hw=[H, W], scale=1024.0 / max(H, W), field=R["field"])
        _dump(state_p, state)
    t = dict(state["terms"])
    field = np.load(seq / "render_field.npz")["field"] if state["field"] == "card" else np.ones((H, W), bool)
    img, _ = DS.style(water, bone, hit, dev, t, np.random.default_rng(state["seeds"]["noise"]), state["pitch_mm"],
                      field=field, RP=RP)
    atten = -np.log(np.clip(trans, 1e-6, 1.0))
    fm = field & hit if int((field & hit).sum()) > 100 else hit
    logor = CL.window_or(atten, fm)
    s = float(state["scale"])
    for sub, im in (("images", img), ("images_logor", logor)):
        (seq / sub).mkdir(exist_ok=True)
        pil = Image.fromarray(im)
        if s != 1.0:
            pil = pil.resize((int(round(W * s)), int(round(H * s))), Image.BILINEAR)
        pil.save(seq / sub / f"{fr['stem']}.png")
    (seq / "render").mkdir(exist_ok=True)
    np.savez_compressed(seq / "render" / f"f{k:03d}.npz", water_cm=water.astype(np.float16), bone_cm=bone.astype(np.float16),
                        hit=hit, trunc=trunc)
    rf = dict(frame=k, stem=fr["stem"], hit_frac=float(hit.mean()), trunc_frac_of_hit=float(trunc[hit].mean()) if hit.any() else 1.0,
              water_median_cm=float(np.median(water[hit])) if hit.any() else None, seconds=round(time.time() - t0, 1),
              table_stripped=not a.keep_table, not_held_out=NOT_HELD_OUT)
    _dump(seq / "render" / f"f{k:03d}.json", rf)
    print(f"RENDERED f{k:03d} {fr['stem']} hit {rf['hit_frac']:.2f} trunc {rf['trunc_frac_of_hit']:.3f} {rf['seconds']} s")
    return 0


# ============================================================================================ gt
def screen_corners(detail, plate_ok, img_w, img_h, margin=0.0) -> tuple:
    """(corners, partial, why) of one level from its projected plate corners (`detail`: image px of the SAVED frame).
    Order AS, AI, PI, PS. A corner is truth only when it passed the plate screens AND lies on the image,
    [margin, W - margin) x [margin, H - margin); `partial` nulls every corner that is not; `corners` needs all four,
    else it is null and the level is scored box-only (cine_eval scores `corners` alone). A vertebra clipped by the
    frame border has off-image corners no detector can place: T12 at the top edge of the verse823 stand-in carried
    its anterior-superior corner 87 px (16.7 mm) above the frame (review, 2026-09-26), and scoring it charged every
    correct detection 10-17 mm. Also writes `<side>_on_image` into each plate of `detail`."""
    W, H, m = float(img_w), float(img_h), float(margin)
    partial, why = [], []
    for tag, which, side in (("AS", "superior", "anterior"), ("AI", "inferior", "anterior"),
                             ("PI", "inferior", "posterior"), ("PS", "superior", "posterior")):
        pl = detail.get(which) or {}
        p = pl.get(side)
        if p is None:
            partial.append(None)
            why.append(f"{tag}: no plate ({pl.get('why') or 'not fitted'})")
            continue
        on = bool(m <= float(p[0]) < W - m and m <= float(p[1]) < H - m)
        pl[f"{side}_on_image"] = on
        if not pl.get(f"{side}_ok"):
            partial.append(None)
            why.append(f"{tag}: failed the plate screen")
        elif not on:
            partial.append(None)
            why.append(f"{tag}: off the image at ({float(p[0]):.1f}, {float(p[1]):.1f})")
        else:
            partial.append(p)
    ok = bool(plate_ok) and all(c is not None for c in partial)
    if not ok and not why:
        why.append("plate screen failed")
    return (partial if ok else None), partial, "; ".join(why)


def _geometry(state):
    pose = state["pose"]
    K = np.asarray(pose["K"], float)
    M = np.asarray(pose["ext"], float) @ np.linalg.inv(np.asarray(pose["T"], float))
    return K, M, int(state["down"]), int(pose["nr"]), int(pose["nc"])


def cmd_gt(a) -> int:
    import nibabel as nib
    import polypose_invariants as INV
    import spine_project as SP
    seq = Path(_x(a.seq_dir))
    P = _load_plan(seq)
    k = int(a.frame)
    fr = P["frames"][k]
    state_p = seq / "render_state.json"
    if not state_p.exists():
        raise SystemExit(f"no {state_p}: render frame 0 first")
    state = json.loads(state_p.read_text())
    K, M, down, nr, nc = _geometry(state)
    s = float(state["scale"])
    img_w, img_h = int(round(nc / down * s)), int(round(nr / down * s))     # the saved frame (render's resize)
    org_new = np.asarray(state["org_new_lps"], float)
    shift = np.asarray(state["shift_lps"], float)
    wrec = _warp_record(seq, P, k)          # refuses volumes warped for another plan
    body, org, sp = _volume_lps(seq, k, "body_msk")
    lab, org_l, _ = _volume_lps(seq, k, "label")
    if not (np.allclose(org, state["org_lps"]) and np.allclose(org_l, org)):
        raise SystemExit(f"frame {k} volumes are not on frame 0's grid")
    LMAP = {n: int(i) for n, i in P["labels"]["map"].items()}
    inv = {v: n for n, v in LMAP.items()}
    T = transforms_by_id(P, k)
    src_img = nib.load(P["source"]["body_rekeyed"]["path"])
    src_body = np.asarray(src_img.dataobj).astype(np.int16)
    A_src = np.asarray(src_img.affine, float)
    fov_cut = set(INV.truncated_levels(lab, LMAP))

    def proj_world_ras(P_ras, Tm):
        return _project(ras_to_lps(_move(Tm, P_ras)) + shift, M, K, down)

    boxes, xc_scored = [], []
    body_ids = sorted(set(int(i) for i in np.unique(body)) - {0})
    for i in body_ids:
        name = inv.get(i)
        if name is None or not PM.VERTEBRA_RE.match(name):
            continue
        m = body == i
        pm = SP.project_mask(m, org_new, sp, M, K, down, nr, nc, step=1)
        if pm is None:
            continue
        Pl = _mask_points_lps(m, org_new, sp, step=1)
        uv = _project(Pl, M, K, down)
        ins = _inside(uv, nr, nc, down)
        q = uv[ins]
        mine = _box(q)
        if max(abs(x - y) for x, y in zip(mine, pm["box"])) > 1e-6:
            raise RuntimeError(f"{name}: this file's projection does not reproduce spine_project.project_mask")
        # the exact cross-check: SOURCE body voxels moved by this frame's transform
        sv = _points_world(src_body == i, A_src)
        uv_s = proj_world_ras(sv, T[i]) if len(sv) else np.zeros((0, 2))
        in_s = _inside(uv_s, nr, nc, down) if len(uv_s) else np.zeros(0, bool)
        xc = iou(mine, _box(uv_s[in_s])) if in_s.sum() >= 10 else 0.0
        xc_p = iou(_box_pct(q), _box_pct(uv_s[in_s])) if in_s.sum() >= 10 else 0.0
        # clipped by the frame border: some of the body's voxels project off the image, so the box is the clipped
        # visible part and the min-area rectangle is of the clipped point set, not the body's silhouette
        clipped = not bool(ins.all())
        rect = None if clipped else min_area_rect(q)
        sil = canonical_slots(rect) * s if rect is not None else None
        sil_why = ("clipped by the frame border: the quad would be of the visible part only" if clipped else
                   "" if rect is not None else "no minimum-area rectangle (degenerate projection)")
        cr = P["corners"].get(name) or {}
        corners = partial = detail = None
        corners_why = "no end-plate corners planned for this level"
        if cr:
            detail = {}
            for which in ("superior", "inferior"):
                pl = cr.get(which) or {}
                if "anterior" in pl:
                    uvp = proj_world_ras(np.array([pl["anterior"], pl["posterior"]]), T[i]) * s
                    detail[which] = dict(anterior=uvp[0].round(3).tolist(), posterior=uvp[1].round(3).tolist(),
                                         anterior_ok=pl.get("anterior_ok", pl["ok"]),
                                         posterior_ok=pl.get("posterior_ok", pl["ok"]),
                                         ok=pl["ok"], why=pl.get("why", ""), rms_mm=pl.get("rms_mm"))
                else:
                    detail[which] = dict(ok=False, anterior_ok=False, posterior_ok=False, why=pl.get("why", "no plate"))
            # AS, AI, PI, PS; a corner that failed its screen or lies off the image is null in `partial`, and
            # `corners` needs all four (else the level is scored box-only)
            corners, partial, corners_why = screen_corners(detail, cr.get("ok"), img_w, img_h, a.corner_margin_px)
        role = "score"
        why = ""
        if name == "C1":
            role, why = "ignore", "C1 has no vertebral body"
        elif name in fov_cut:
            role, why = "ignore", "cut by the volume's field of view"
        elif pm["inside"] < a.min_inside:
            role, why = "ignore", f"inside {pm['inside']:.2f} < {a.min_inside}"
        b = dict(gt_id=name, cls=0, level=name, box=[round(v * s, 3) for v in mine],
                 box_p2_98=[round(v * s, 3) for v in _box_pct(q)], inside=round(float(pm["inside"]), 4), role=role,
                 role_why=why, clipped_by_border=clipped, corners=corners, corner_order=CORNER_ORDER,
                 corners_why=corners_why if corners is None else "", corners_partial=partial,
                 corners_silhouette=None if sil is None else sil.round(3).tolist(), corners_silhouette_order=SIL_ORDER,
                 corners_silhouette_why=sil_why,
                 corners_detail=detail, body_source=(P["source"]["body_rekeyed"]["body_source"] or {}).get(name),
                 xcheck_iou=round(xc, 4), xcheck_iou_p2_98=round(xc_p, 4))
        boxes.append(b)
        if role == "score":
            xc_scored.append(xc)
    # vertebrae visible without a body mask: their whole-vertebra box, ignored (neither a hit nor a false positive)
    have = {b["gt_id"] for b in boxes}
    for i in sorted(set(int(x) for x in np.unique(lab)) - {0}):
        name = inv.get(i)
        if name is None or name in have or not PM.VERTEBRA_RE.match(name):
            continue
        pm = SP.project_mask(lab == i, org_new, sp, M, K, down, nr, nc, step=2)
        if pm is not None:
            boxes.append(dict(gt_id=name, cls=0, level=name, box=[round(v * s, 3) for v in pm["box"]], inside=pm["inside"],
                              role="ignore", role_why="no body mask for this level: whole-vertebra box", corners=None,
                              corner_order=CORNER_ORDER))
    for ig in P["ignore_regions"]:
        anc = LMAP[ig["anchor"]]
        uv = proj_world_ras(np.asarray(ig["corners_world"], float), T[anc])
        bx = _box(uv)
        W_, H_ = nc / down, nr / down
        bx = [min(max(bx[0], 0.0), W_ - 1), min(max(bx[1], 0.0), H_ - 1), min(max(bx[2], 0.0), W_ - 1), min(max(bx[3], 0.0), H_ - 1)]
        if bx[2] > bx[0] and bx[3] > bx[1]:
            boxes.append(dict(gt_id=ig["gt_id"], cls=ig["cls"], level=None, box=[round(v * s, 3) for v in bx],
                              role="ignore", role_why=ig["rule"], corners=None, corner_order=CORNER_ORDER))
    # orientation of the saved frame, read off the projection (superior and anterior are RAS +z and +y)
    iso_id = LMAP[P["motion"]["iso"]]
    c_iso = np.asarray(P["motion"]["iso_centroid_world"], float)
    o = proj_world_ras(np.stack([c_iso, c_iso + [0, 0, 30.0], c_iso + [0, 30.0, 0]]), T[iso_id])
    sup, ant = o[1] - o[0], o[2] - o[0]
    orient = dict(superior="up" if sup[1] < -abs(sup[0]) else "down" if sup[1] > abs(sup[0]) else "sideways",
                  anterior="right" if ant[0] > abs(ant[1]) else "left" if ant[0] < -abs(ant[1]) else "vertical")
    wchk = wrec.get("all_pass") if wrec else None
    xmin = min(xc_scored) if xc_scored else None
    meta = {
        "schema": TRUTH_SCHEMA, "case": P["source"]["case"], "stem": fr["stem"], "seq": P["seq"], "frame": k, "view": "LAT",
        "px_mm": round(float(state["px_mm_iso"]) / s, 6), "px_mm_plane": "isocentre (detector pitch / magnification)",
        "px_mm_detector": round(float(state["pitch_mm"]) / s, 6), "img_px": [img_w, img_h],
        "held_out": False, "not_held_out": NOT_HELD_OUT,
        "boxes": boxes,
        "extras": {"angle": fr["total_flex_ext_deg"], "angle_def": "sum of the moving segments' flex_ext_deg (+ extension)",
                   "phase": fr["phase"], "frac": P["motion"]["frac"], "region": P["motion"]["region"],
                   "segments": fr["segments"], "orientation": orient,
                   "facing": {"left": "L", "right": "R"}.get(orient["anterior"]),   # the image side the anterior wall is on
                   "box_convention": "min/max of the projected warped SPINEPS body voxels inside the detector (box); "
                                     "2nd-98th percentile beside it (box_p2_98)",
                   "corner_screen": dict(margin_px=float(a.corner_margin_px), image_px=[img_w, img_h],
                                         rule="corners (AS, AI, PI, PS) are truth only when all four passed the plate "
                                              "screens and project onto the image; otherwise corners null (box-only), "
                                              "corners_partial keeps the ones that did, corners_why says why. "
                                              "corners_silhouette is null when any body voxel projects off the "
                                              "image (clipped_by_border)"),
                   "warp_frame_key": None if not wrec else wrec.get("frame_key"),
                   "xcheck": dict(iou_min_scored=xmin, threshold=a.xcheck_iou,
                                  ok=None if xmin is None else bool(xmin >= a.xcheck_iou),
                                  rule="IoU of the warped-mask box with the box of the SOURCE body voxels moved by the "
                                       "frame's rigid transform (RAS) -> LPS -> the same K and M"),
                   "warp_checks_all_pass": wchk,
                   "geometry": dict(K=state["pose"]["K"], down=down, M=M.tolist(), pitch_mm_detector=state["pitch_mm"],
                                    org_new_lps=state["org_new_lps"], shift_lps=state["shift_lps"], scale=s,
                                    anchor_tag=state["anchor_tag"], angles=state["angles"], sod_mm=state["sod_mm"],
                                    sid_mm=state["sid_mm"], magnification=state["magnification"])},
    }
    _dump(seq / "meta" / f"{fr['stem']}.json", meta)
    n_sc = sum(1 for b in boxes if b["role"] == "score")
    n_c = sum(1 for b in boxes if b["role"] == "score" and b.get("corners"))
    clip = [b["gt_id"] for b in boxes if b["role"] == "score" and b.get("clipped_by_border")]
    print(f"GT f{k:03d} {fr['stem']}: {n_sc} scored boxes ({n_c} with corners; clipped by the border: "
          f"{clip or 'none'}), xcheck IoU min "
          f"{xmin if xmin is None else round(xmin, 3)}, orientation {orient}, warp checks {wchk}")
    return 0 if (xmin is None or xmin >= a.xcheck_iou) else 1


# ============================================================================================ check
def cmd_check(a) -> int:
    from PIL import Image, ImageDraw
    seq = Path(_x(a.seq_dir))
    P = _load_plan(seq)
    N = len(P["frames"])
    probs, rows = [], []
    for fr in P["frames"]:
        k, stem = fr["frame"], fr["stem"]
        rec = dict(frame=k, stem=stem)
        for what, p in (("volumes", seq / "volumes" / f"f{k:03d}_ct.nii.gz"), ("checks", seq / "checks" / f"f{k:03d}.json"),
                        ("image", seq / "images" / f"{stem}.png"), ("image_logor", seq / "images_logor" / f"{stem}.png"),
                        ("meta", seq / "meta" / f"{stem}.json")):
            rec[what] = p.exists()
            if not p.exists():
                probs.append(f"f{k:03d}: no {what}")
        if rec["checks"]:
            c = json.loads((seq / "checks" / f"f{k:03d}.json").read_text())
            rec["warp_all_pass"] = c.get("all_pass")
            rec["frame_key_current"] = c.get("frame_key") == frame_key(P, k)
            if not rec["frame_key_current"]:
                probs.append(f"f{k:03d}: volumes not warped for this plan (checks frame_key "
                             f"{str(c.get('frame_key'))[:12]}{', in progress' if c.get('in_progress') else ''}): re-warp")
            rec["failed"] = sorted(n for n, v in (c.get("checks") or {}).items() if v.get("status") == "fail")
            rec["fov_out_within_150mm_of_iso"] = c.get("fov_out_within_150mm_of_iso")
            if "equivalence" in c:
                rec["equivalence"] = c["equivalence"]
                if not c["equivalence"].get("ok"):
                    probs.append(f"f{k:03d}: verify_equivalence failed")
            if not c.get("all_pass"):
                probs.append(f"f{k:03d}: warp invariants failed {rec['failed'] or c.get('refused')}")
        if rec["meta"]:
            m = json.loads((seq / "meta" / f"{stem}.json").read_text())
            x = m["extras"]["xcheck"]
            rec.update(xcheck_iou_min=x["iou_min_scored"], orientation=m["extras"]["orientation"],
                       scored=[b["gt_id"] for b in m["boxes"] if b["role"] == "score"],
                       with_corners=[b["gt_id"] for b in m["boxes"] if b["role"] == "score" and b.get("corners")])
            if x["iou_min_scored"] is not None and x["iou_min_scored"] < a.xcheck_iou:
                probs.append(f"f{k:03d}: truth cross-check IoU {x['iou_min_scored']:.3f} < {a.xcheck_iou}")
        rows.append(rec)
    if P["motion"]["verify_frame"] < N and not any("equivalence" in r for r in rows):
        probs.append("verify_equivalence has not run (no checks for the verify frame)")
    orients = {json.dumps(r.get("orientation"), sort_keys=True) for r in rows if r.get("orientation")}
    if len(orients) > 1:
        probs.append(f"the frame orientation changes within the sequence: {orients}")
    # the contact sheet: styled (top) and -log/window_or (bottom), truth drawn
    picks = [int(x) for x in a.frames.split(",")] if a.frames else sorted({0, N // 4, N // 2, (3 * N) // 4})
    tile = 512
    sheet = Image.new("RGB", (tile * len(picks), tile * 2), (0, 0, 0))
    col = dict(score=(90, 230, 90), ignore=(150, 150, 150))
    cc = [(255, 70, 70), (255, 170, 40), (70, 140, 255), (230, 80, 230)]       # AS, AI, PI, PS
    for j, k in enumerate(picks):
        fr = P["frames"][k]
        mp = seq / "meta" / f"{fr['stem']}.json"
        m = json.loads(mp.read_text()) if mp.exists() else {"boxes": [], "img_px": [1024, 1024]}
        for r_, sub in enumerate(("images", "images_logor")):
            ip = seq / sub / f"{fr['stem']}.png"
            if not ip.exists():
                continue
            im = Image.open(ip).convert("RGB")
            f = tile / max(im.size)
            im = im.resize((int(im.size[0] * f), int(im.size[1] * f)))
            dr = ImageDraw.Draw(im)
            for b in m["boxes"]:
                bb = [v * f for v in b["box"]]
                dr.rectangle(bb, outline=col.get(b["role"], (200, 200, 0)), width=1)
                if b.get("level") and b["role"] == "score":
                    dr.text((bb[0] + 2, bb[1] + 1), b["level"], fill=col["score"])
                if b.get("corners_silhouette"):
                    q = [(u * f, v * f) for u, v in b["corners_silhouette"]]
                    dr.line(q + [q[0]], fill=(80, 200, 220), width=1)
                for c_, pt in zip(cc, b.get("corners_partial") or b.get("corners") or []):
                    if pt is not None:
                        dr.ellipse([pt[0] * f - 2, pt[1] * f - 2, pt[0] * f + 2, pt[1] * f + 2], fill=c_)
            dr.text((4, 4), f"frame {k}  {fr['total_flex_ext_deg']:+.1f} deg", fill=(255, 255, 0))
            sheet.paste(im, (j * tile, r_ * tile))
    (seq / "qc").mkdir(exist_ok=True)
    sheet.save(seq / "qc" / "contact_sheet.png")
    out = dict(created_utc=_now(), sequence=P["sequence"], n_frames=N, not_held_out=NOT_HELD_OUT, problems=probs,
               ok=not probs, frames=rows, contact_sheet=str(seq / "qc" / "contact_sheet.png"), sheet_frames=picks,
               corners_ok={n: v.get("ok") for n, v in P["corners"].items()}, labels=P["labels"]["how"])
    _dump(seq / "qc" / "check.json", out)
    print(f"{'CHECK_OK' if not probs else 'CHECK_FAIL'} {P['sequence']}: {N} frames, {len(probs)} problems"
          + ("".join(f"\n  {p}" for p in probs[:30])) + f"\nNOT HELD OUT ({NOT_HELD_OUT}). Look at {out['contact_sheet']}")
    return 0 if not probs else 1


# ============================================================================================ self-test
def self_test() -> int:
    """Phantoms and injected faults, pure numpy/scipy (runs on Windows). Fails on purpose when a rule is broken."""
    import tempfile
    fails, n = [], 0

    def ck(name, cond, note=""):
        nonlocal n
        n += 1
        if not cond:
            fails.append(f"{name}: {note}")

    # 1. the phase and the verify frame
    a = [phase(k, 60) for k in range(60)]
    ck("phase_neutral", abs(a[0]) < 1e-12 and abs(a[30]) < 1e-12, f"a0 {a[0]} a30 {a[30]}")
    ck("phase_extremes", abs(a[15] + 1) < 1e-12 and abs(a[45] - 1) < 1e-12, f"a15 {a[15]} a45 {a[45]}")
    ck("verify_frame_is_max_flexion", int(np.argmin(a)) == 15, f"argmin {int(np.argmin(a))}")

    # 2. the ROM table on disk: lumbar usable, cervical and whole refused, a drifted copy refused
    rom = load_rom()
    try:
        caps = require_rows(rom, region_segments(ORDINARY, "lumbar"))
        ck("lumbar_rows", list(caps) == ["T10-T11", "T11-T12", "T12-L1", "L1-L2", "L2-L3", "L3-L4", "L4-L5"],
           f"{list(caps)}")
    except Refused as e:
        ck("lumbar_rows", False, str(e))
    for reg in ("cervical", "whole"):
        try:
            require_rows(rom, region_segments(ORDINARY, reg))
            ck(f"{reg}_refused_while_pending", False, "planned a region with pending rows")
        except Refused as e:
            ck(f"{reg}_refused_while_pending", "pending" in str(e), str(e)[:120])
    d = json.loads(ROM_DEFAULT.read_text(encoding="utf-8"))
    d["rom_deg"]["thoracolumbar_lumbar"]["L3-L4"]["flex"] = 99.0
    tp = Path(tempfile.mkdtemp()) / "rom.json"
    tp.write_text(json.dumps(d), encoding="utf-8")
    try:
        load_rom(tp)
        ck("drift_refused", False, "a hand-edited copied row was accepted")
    except ValueError:
        ck("drift_refused", True)
    bad = dict(rom, rows=dict(rom["rows"], **{"L3-L4": dict(rom["rows"]["L3-L4"], status="pending: re-read")}))
    try:
        require_rows(bad, ["L3-L4"])
        ck("pending_with_numbers_refused", False, "a pending row with numbers was used")
    except Refused:
        ck("pending_with_numbers_refused", True)

    # 3. the chain: base fixed, relative rotation = the requested one about +x, riders share the top's motion, sign
    chain = ORDINARY
    cent = {nm: np.array([0.0, 0.0, 700.0 - 28.0 * i]) for i, nm in enumerate(chain)}
    caps = {s: rom["rows"][s] for s in region_segments(chain, "lumbar")}
    sg = frame_segments(-1.0, caps, 1.0, 1.0)
    T, _ = chain_transforms(cent, chain, "L5", sg)
    from scipy.spatial.transform import Rotation
    ck("base_identity", np.allclose(T["L5"], np.eye(4)), "L5 moved")
    for s, v in sg.items():
        up, lo = s.split("-")
        rel = np.linalg.inv(T[lo]) @ T[up]
        rv = np.degrees(Rotation.from_matrix(rel[:3, :3]).as_rotvec())
        ck(f"relative_{s}", np.allclose(rv, [v["flex_ext_deg"], 0, 0], atol=1e-9), f"{rv} vs {v['flex_ext_deg']}")
        ck(f"flexion_{s}", abs(v["flex_ext_deg"] + caps[s]["flex"]) < 1e-9, f"{v['flex_ext_deg']} vs -{caps[s]['flex']}")
    top_l = REGIONS["lumbar"]["top"]
    ck("riders_share_top", all(np.array_equal(T[nm], T[top_l]) for nm in chain[:chain.index(top_l)]), "a rider moved apart")
    ext = frame_segments(1.0, caps, 1.0, 1.0)
    Te, _ = chain_transforms(cent, chain, "L5", ext)
    top = _move(Te["T12"], cent["T12"])[0]
    ck("sign_extension_is_posterior", top[1] < cent["T12"][1] - 1.0, f"T12 y {cent['T12'][1]} -> {top[1]:.2f} (RAS +y anterior)")
    groups = body_groups(chain, "lumbar", {nm: i + 1 for i, nm in enumerate(chain)}, set(range(1, 25)), {})
    ck("groups_lumbar", [g["name"] for g in groups] == ["T10+above", "T11", "T12", "L1", "L2", "L3", "L4", "L5(fixed)"],
       str([g["name"] for g in groups]))
    try:
        body_groups(chain, "lumbar", {nm: i + 1 for i, nm in enumerate(chain)}, set(range(1, 26)) | {63}, {})
        ck("stray_id_refused", False, "an id with no motion rule was accepted")
    except Refused:
        ck("stray_id_refused", True)

    # 4. the label map: a VerSe-coded phantom is detected v4 by ostk, and the anatomy picks the VerSe-native map
    try:
        import polypose_invariants as INV
        INV.find_ostk()
        ck("min_voxels_matches_checker", INV.MIN_VERTEBRA_VOXELS == MIN_VERTEBRA_VOXELS, "constant drifted")
        from ostk.labels import detect_scheme
        vol = np.zeros((12, 12, 24 * 6), np.int16)
        for i in range(1, 25):                                  # C1 (id 1) at the TOP: world z = index (identity affine)
            z0 = (24 - i) * 6
            vol[2:10, 2:10, z0:z0 + 5] = i                      # 320 voxels: above the 200-voxel debris floor
        aff = np.eye(4)
        st = label_stats(vol)
        ck("phantom_detected_legacy", detect_scheme(vol) == "v4", f"ostk says {detect_scheme(vol)}")
        LM, rec = resolve_label_map(vol, aff, st)
        ck("anatomy_picks_verse_native", LM["L1"] == 20 and LM["C1"] == 1 and rec["chosen"] != rec["detected"],
           f"chosen {rec['chosen']} L1={LM['L1']}")
        try:
            resolve_label_map(vol[:, :, ::-1].copy(), aff, label_stats(vol[:, :, ::-1].copy()))
            ck("upside_down_refused", False, "a spine upside down in world z was given a map")
        except Refused:
            ck("upside_down_refused", True)
    except ImportError as e:
        ck("ostk_importable", False, str(e))

    # 5. the projection mirrors spine_project.project_mask exactly; min-area rectangle and slots
    import spine_project as SP
    import pose_arc as PA
    anchor = dict(K=[[-7782.4, 0, 1022.5], [0, 7782.4, 1022.5], [0, 0, 1]], nr=2048, nc=2048, px_mm=0.15,
                  ext=[[-1, 0, 0, 0], [0, 0, -1, 0], [0, -1, 0, 744.0], [0, 0, 0, 1]], T=np.eye(4).tolist(),
                  anchor=[0.0, 0.0, 0.0], tag="phantom/AP")
    pose = PA.arc_pose(anchor, -90.0, 0.0, 0.0)
    K = np.asarray(pose["K"], float)
    M = np.asarray(pose["ext"], float) @ np.linalg.inv(np.asarray(pose["T"], float))
    mk = np.zeros((40, 50, 60), bool)
    mk[10:30, 12:40, 20:45] = True
    org, sp = np.array([-20.0, -25.0, -15.0]), np.array([0.8, 0.8, 0.8])
    pm = SP.project_mask(mk, org, sp, M, K, 2, 2048, 2048, step=1)
    uv = _project(_mask_points_lps(mk, org, sp), M, K, 2)
    mine = _box(uv[_inside(uv, 2048, 2048, 2)])
    ck("projection_mirrors_spine_project", pm is not None and max(abs(x - y) for x, y in zip(mine, pm["box"])) < 1e-9,
       f"{mine} vs {pm and pm['box']}")
    th = math.radians(17.0)
    R2 = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    rect = np.array([[0, 0], [40, 0], [40, 25], [0, 25]], float) @ R2.T + [300, 200]
    g = np.random.default_rng(0).uniform(0, 1, (4000, 2)) * [40, 25] @ R2.T + [300, 200]
    got = min_area_rect(np.vstack([g, rect]))
    ck("min_area_rect", got is not None and np.allclose(canonical_slots(got), canonical_slots(rect), atol=1e-6),
       f"{None if got is None else canonical_slots(got).round(2).tolist()}")
    sl = canonical_slots([[10, 50], [0, 0], [12, 1], [1, 49]])
    ck("canonical_slots", np.allclose(sl, [[0, 0], [12, 1], [10, 50], [1, 49]]), f"{sl.tolist()}")
    ck("centred_affine_formula", np.allclose(centred_affine(np.diag([2.0, 3.0, 4.0, 1.0]), (11, 21, 31))[:3, 3],
                                             [-10.0, -30.0, -60.0]), "formula")

    # 6. the frame stems key to the VerSe person (tools/patient_keys.py), so level_prototype's gate can key them
    try:
        import patient_keys as PK
        r_, why = PK.key_any(stem_for("verse823", "lumbar", 0.5, 17))
        ck("stem_keys_to_verse", r_ is not None and r_["key"] == "verse:verse823", f"{r_} {why}")
    except ImportError as e:
        ck("patient_keys_importable", False, str(e))

    # 7. corners: a level clipped by the frame border is box-only (corners null), never scored on off-image corners
    def det():
        return dict(superior=dict(anterior=[100.0, 50.0], posterior=[160.0, 55.0], anterior_ok=True, posterior_ok=True, ok=True),
                    inferior=dict(anterior=[102.0, 90.0], posterior=[158.0, 95.0], anterior_ok=True, posterior_ok=True, ok=True))
    c_, p_, w_ = screen_corners(det(), True, 1024, 1024)
    ck("corners_on_image_kept", c_ == [[100.0, 50.0], [102.0, 90.0], [158.0, 95.0], [160.0, 55.0]] and not w_, f"{c_} {w_}")
    d_ = det()
    d_["superior"]["anterior"] = [439.1, -87.1]                 # the review's T12 anterior-superior corner, frame 0
    c_, p_, w_ = screen_corners(d_, True, 1024, 1024)
    ck("corner_off_image_box_only", c_ is None and p_[0] is None and p_[1:] == [[102.0, 90.0], [158.0, 95.0], [160.0, 55.0]]
       and "AS: off the image" in w_ and d_["superior"]["anterior_on_image"] is False, f"{c_} {p_} {w_}")
    d_ = det()
    d_["inferior"]["posterior"] = [1024.0, 95.0]                # x == W is off the image: [0, W)
    ck("corner_at_W_is_off", screen_corners(d_, True, 1024, 1024)[0] is None, "x = W accepted")
    ck("corner_margin", screen_corners(det(), True, 1024, 1024, margin=60.0)[0] is None, "AS at y 50 kept with margin 60")
    d_ = det()
    d_["inferior"]["posterior_ok"] = False
    c_, p_, w_ = screen_corners(d_, False, 1024, 1024)
    ck("corner_screen_failed_null", c_ is None and p_[2] is None and p_[0] is not None and "PI: failed the plate screen" in w_, w_)
    d_ = dict(superior=dict(ok=False, anterior_ok=False, posterior_ok=False, why="the dens"), inferior=det()["inferior"])
    c_, p_, w_ = screen_corners(d_, False, 1024, 1024)
    ck("corner_no_plate", c_ is None and p_[0] is None and p_[3] is None and p_[1] is not None and "no plate (the dens)" in w_, w_)

    # 8. base_fixed: a single-vertebra base passes a correct warp that trims a facet sliver (Dice < 0.999, which the
    #    pelvis rule would fail), and fails a moved base, a non-identity transform, and a base with no voxels
    tol = dict(PM.TOLERANCE_DEFAULTS)
    src = np.zeros((40, 40, 60), np.int16)
    src[10:30, 10:30, 5:25] = 24                                # the base, 8000 voxels
    src[10:30, 10:30, 30:50] = 23                               # the moving neighbour
    aff1 = np.eye(4)
    Tb = {24: np.eye(4), 23: np.eye(4)}
    out = src.copy()
    disp = np.zeros((3,) + src.shape, np.float32)
    out[10:12, 10:30, 24] = 0                                   # 40 voxels (0.5 %) pulled from beside the base
    disp[2, 10:12, 10:30, 23:26] = 1.8
    r_ = base_fixed(src, out, disp, aff1, Tb, {24}, tol)
    ck("base_fixed_passes_sliver", r_["status"] == "pass" and r_["value"]["dice_min"] < 0.999
       and r_["value"]["pelvis_rule_0999"] is False, f"{r_['status']} {r_['value']['dice_min']} {r_['note']}")
    out2 = src.copy()
    out2[out2 == 24] = 0
    out2[12:32, 10:30, 5:25] = 24                               # the base moved 2 voxels
    disp2 = np.zeros_like(disp)
    disp2[0, 12:32, 10:30, 5:25] = -2.0                         # pull-back: source = output + disp
    r_ = base_fixed(src, out2, disp2, aff1, Tb, {24}, tol)
    ck("base_fixed_fails_moved_base", r_["status"] == "fail" and "Dice" in r_["note"] and "p95" in r_["note"], r_["note"])
    Tm = dict(Tb)
    Tm[24] = np.eye(4)
    Tm[24][0, 3] = 0.5
    r_ = base_fixed(src, src, np.zeros_like(disp), aff1, Tm, {24}, tol)
    ck("base_fixed_fails_non_identity", r_["status"] == "fail" and "transform not identity" in r_["note"], r_["note"])
    r_ = base_fixed(src, src, np.zeros_like(disp), aff1, Tb, {99}, tol)
    ck("base_fixed_fails_no_base", r_["status"] == "fail" and "unverifiable" in r_["note"], r_["note"])

    # 9. frame_key: changes with the frame's motion, not with what the warp does not read; stale volumes are refused
    import copy
    Pk = dict(frames=[dict(group_T={"A": np.eye(4).tolist(), "B": np.eye(4).tolist()})],
              bodies=[dict(name="A", ids=[1], fixed=False), dict(name="B", ids=[2], fixed=True)],
              id_group={"1": "A", "2": "B"}, crop=None, labels=dict(map={"L4": 1, "L5": 2}), motion=dict(verify_frame=0),
              source=dict(ct=dict(sha256="a"), label=dict(sha256="b"), body_rekeyed=dict(sha256="c")), corners={})
    k0 = frame_key(Pk, 0)
    P2 = copy.deepcopy(Pk)
    P2["frames"][0]["group_T"]["A"][1][3] = 0.25
    P3 = copy.deepcopy(Pk)
    P3["corners"] = {"L4": {"ok": True}}
    P3["created_utc"] = "later"
    ck("frame_key_follows_motion", frame_key(P2, 0) != k0 and frame_key(P3, 0) == k0, "key")
    sd = Path(tempfile.mkdtemp())
    ck("warp_record_none_without_checks", _warp_record(sd, Pk, 0) is None, "a record appeared")
    (sd / "checks").mkdir()
    (sd / "checks" / "f000.json").write_text(json.dumps(dict(frame_key=k0, all_pass=True)))
    ck("warp_record_current_accepted", (_warp_record(sd, Pk, 0) or {}).get("all_pass") is True, "refused a current record")
    for tag, rec_ in (("other_plan", dict(frame_key=frame_key(P2, 0))), ("in_progress", dict(frame_key=None, in_progress=True))):
        (sd / "checks" / "f000.json").write_text(json.dumps(rec_))
        try:
            _warp_record(sd, Pk, 0)
            ck(f"warp_record_refuses_{tag}", False, "stale volumes accepted")
        except SystemExit:
            ck(f"warp_record_refuses_{tag}", True)

    # 10. the committed-blob hash reads the same on a CRLF (Windows autocrlf) and an LF checkout
    tp2 = Path(tempfile.mkdtemp())
    (tp2 / "lf.json").write_bytes(b'{\n "a": 1\n}\n')
    (tp2 / "crlf.json").write_bytes(b'{\r\n "a": 1\r\n}\r\n')
    ck("sha256_lf_normalises_crlf", _sha256_lf(tp2 / "lf.json") == _sha256_lf(tp2 / "crlf.json")
       == hashlib.sha256(b'{\n "a": 1\n}\n').hexdigest(), "CRLF and LF differ")

    print(f"self-test: {n} checks  (rom_cine copied_from.sha256 {'==' if rom['spec_is_copied_version'] else '!='} "
          f"the spec's LF sha256 {rom['spec_sha256_lf'][:12]}: information, the rows are the refusal)")
    if fails:
        print("SELF-TEST FAILED:")
        for f in fails:
            print("  " + f)
        return 1
    print("SELF-TEST OK: phase and verify frame, pending ROM refused, drift refused, chain relative rotations and "
          "sign, rigid groups, the VerSe label map chosen by anatomy over ostk's detection, projection = "
          "spine_project, min-area rectangle, canonical slots, stems key to verse, off-image corners box-only, "
          "base_fixed (single-vertebra rule), frame_key and stale volumes refused, CRLF-normalised sha256")
    return 0


# ============================================================================================ CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("self-test")
    rc = sub.add_parser("rom-check", help="exit 3 when the region's ROM rows are pending (no volume read)")
    rc.add_argument("--region", choices=sorted(REGIONS), required=True)
    for p in (rc,):
        p.add_argument("--rom", default=str(ROM_DEFAULT))
        p.add_argument("--spec", default=str(SPEC_DEFAULT))
    p = sub.add_parser("plan", help="frames.json: per-frame segments and transforms, labels, bodies, corners (CPU)")
    p.add_argument("--region", choices=sorted(REGIONS), required=True)
    p.add_argument("--case", default="verse823", help="VerSe series (VerSeFusion unified scan-<case>)")
    p.add_argument("--ct", default=None)
    p.add_argument("--label", default=None)
    p.add_argument("--body", default=None, help="SPINEPS body mask (default spineps/bodies/VERSE_<case>_body_msk)")
    p.add_argument("--seq-dir", default=None, help=f"default {OUT_ROOT}/<case>_<region>_fe_f<frac*100>")
    p.add_argument("--frac", type=float, default=0.5)
    p.add_argument("--frames", type=int, default=60)
    p.add_argument("--multiplier", type=float, default=1.0)
    p.add_argument("--iso", default=None, help="isocentre level (default: lumbar L3, cervical C5, whole T7)")
    p.add_argument("--crop-mm", type=float, default=250.0, help="warp a slab of +-this along S-I around the isocentre "
                                                                 "level (0 = the whole volume)")
    p.add_argument("--corner-radius-mm", type=float, default=220.0)
    p.add_argument("--rms-max", type=float, default=2.0, help="plate rms gate (ostk.morphometry's own 2.0 mm)")
    p.add_argument("--corner-body-mm", type=float, default=6.0,
                   help="max corner distance to the SPINEPS body (see plate_corners for why 6)")
    p.add_argument("--lat", type=float, default=-90.0, help="pose_arc lat: -90 = the real Surgio lateral")
    p.add_argument("--pool", default=POOL_DEFAULT)
    p.add_argument("--anchor-tag", default="case29/AP")
    p.add_argument("--card", default="surgio_b51_dr")
    p.add_argument("--down", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--field", choices=("open", "card"), default="open", help="collimator field: open, or one draw from the card")
    p.add_argument("--rom", default=str(ROM_DEFAULT))
    p.add_argument("--spec", default=str(SPEC_DEFAULT))
    p.add_argument("--dry-run", action="store_true", help="plan without the CT (the warp refuses such a plan)")
    w = sub.add_parser("warp", help="one frame's CT, label and body mask through PolyPose (GPU, container)")
    w.add_argument("--seq-dir", required=True)
    w.add_argument("--frame", type=int, required=True)
    w.add_argument("--kernel", default=os.environ.get("PP_KERNEL", "gravity"))
    w.add_argument("--device", default=os.environ.get("PP_DEVICE", "auto"), choices=("auto", "cuda", "cpu"))
    w.add_argument("--force", action="store_true")
    r = sub.add_parser("render", help="one frame ray-cast and styled at the fixed pose (CPU, fluorogen)")
    r.add_argument("--seq-dir", required=True)
    r.add_argument("--frame", type=int, required=True)
    r.add_argument("--keep-table", action="store_true")
    g = sub.add_parser("gt", help="one frame's truth in the cine schema (CPU)")
    g.add_argument("--seq-dir", required=True)
    g.add_argument("--frame", type=int, required=True)
    g.add_argument("--min-inside", type=float, default=0.5)
    g.add_argument("--xcheck-iou", type=float, default=0.95)
    g.add_argument("--corner-margin-px", type=float, default=0.0,
                   help="a corner is truth only inside [m, W - m) x [m, H - m) of the saved frame (default 0: on the image)")
    c = sub.add_parser("check", help="contact sheet + summary; non-zero on any failure")
    c.add_argument("--seq-dir", required=True)
    c.add_argument("--frames", default=None, help="comma list for the sheet (default 0, N/4, N/2, 3N/4)")
    c.add_argument("--xcheck-iou", type=float, default=0.95)
    a = ap.parse_args()
    if a.cmd == "self-test":
        return self_test()
    return dict(**{"rom-check": cmd_rom_check}, plan=cmd_plan, warp=cmd_warp, render=cmd_render, gt=cmd_gt,
                check=cmd_check)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
