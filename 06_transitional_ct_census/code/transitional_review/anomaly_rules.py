#!/usr/bin/env python
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/anomaly_rules.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""anomaly_rules.py -- the transitional-vertebra screen over the CT census, PREREG_rules.md (DRAFT v1) sections 0-5.

PURPOSE
  One JSON and one flat TSV row per CT: rule 1 (rib-free lumbar count against a sacral anchor, with the per-body
  sacral fraction f and the candidate flags), rule 3 (stump call per side at the lowest rib level, guards G1-G4, the
  S3 ratio VALUE with no cut), rule 2 FEATURES (sacral top vs the iliac crests, ala-to-ala width, top-plate over the
  lowest presacral inferior plate, fused-segment count from the anterior contour, child flag), rule 1b and rule 4
  FEATURES for the most cranial rib-free body when the count is six (decisions null: no classifier is frozen), the
  prior calls as comparators, and the partial flag of section 5. Every row carries the sha256 of the pre-registration
  as read, prereg_status "draft", the repo git SHA, the tool name and version, the UTC time and the sha256 of every
  input file it read. Nothing here decides a subtype; it measures, flags and reports failures as failures.

INPUTS (per tier row: RS/ruleclass/tiers/tier{1,2}.tsv, columns in TIERS.md section 3)
  SPINEPS+VERIDAH seg-vert / seg-spine / ctd (VerSe-coded; raw stores relabelled in memory through
  tools/spineps_ids.relabel_by_ctd or refused), Moller arm B fast outputs under --moller-root
  (<coll>/<case>_rib-inst_msk.nii.gz, _rib-inst-t13_msk.nii.gz, _rib_measurements.csv, _done/<case>.measure.json),
  TotalSegmentator total (the tier row's ts_output, or the arm A multilabel under --ts-root/<coll>/<case>.nii.gz which
  has hips), Dataset803 pelvis post-processed under --pelvis-root/<coll>/<case>.nii.gz (+ .json; never _work/ or
  _failed_raw/), CTSP v11 labels (collection ctsp only; resolved through ostk.labels.labels_for), the CT header
  (field extent only; no intensity is read), and the comparators: the registry, AH/<coll>/{labeller_b,calls}/<case>.json
  and rows.csv, lstv_flag_labels_v2.csv, castellvi_consensus.csv, the CTSP manifest.

OUTPUTS
  <out>/<coll>/<case>.rules.json         everything, nested (see output_schema())
  <out>/<coll>/<case>.row.tsv            one header + one flat row (the census columns)
  <out>/_failed/<coll>__<case>.json      a case that raised (its .rules.json and .row.tsv still exist with status=failed)
  <out>/_claims/<coll>__<case>/          atomic-mkdir claims (run mode), stale after --stale-h hours, heartbeat 5 min
  <out>/census.tsv, census_summary.tsv, census_summary.json   (collect mode)

RUN
  one case:   python tools/transitional_review/anomaly_rules.py case --list <tier.tsv> --case-id 0005 --out <out>
  array task: python tools/transitional_review/anomaly_rules.py run --list <tier.tsv> --out <out> --claim --stale-h 2
              (anomaly_rules_array.sh wraps this; it is NOT submitted by this tool)
  collect:    python tools/transitional_review/anomaly_rules.py collect --out <out>
  self-test:  python tools/transitional_review/anomaly_rules.py --selftest --samples <dir>   (exit 1 on any mismatch)
  Every path default is the grid's; on another machine pass the roots (see --help).

HOUSE RULES kept here: nothing is reoriented or written as an image (masks are canonicalised only through their
affine, in memory); CTSP / Dataset803-post masks go through ostk.labels.labels_for and SPINEPS / TS masks never do;
CTSP ids are zfill(4); a cut field is no_count, never ordinary; a failure is written as a failure.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import math
import os
import re
import socket
import subprocess
import sys
import threading
import time
import traceback
from functools import lru_cache
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = TOOLS.parent
for p in (str(TOOLS), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
# ostk (OpenSpineToolkit) is not pip-installed anywhere in this lab: a checkout beside this repo, $OSTK_ROOT, or
# ~/OpenSpineToolkit (the grid). Only labels_for is used, and only for CTSP / Dataset803-post masks.
for cand in (os.environ.get("OSTK_ROOT", ""), str(REPO.parent / "OpenSpineToolkit"), str(Path.home() / "OpenSpineToolkit")):
    if cand and os.path.isdir(os.path.join(cand, "ostk")) and cand not in sys.path:
        sys.path.append(cand)
try:
    import spineps_ids  # tools/spineps_ids.py
except ImportError:  # pragma: no cover
    spineps_ids = None
try:
    from tp_morphology import axes_of as _tp_axes_of, tp_metrics as _tp_metrics  # tools/tp_morphology.py
except ImportError:  # pragma: no cover
    _tp_axes_of = _tp_metrics = None

TOOL = "anomaly_rules"
TOOL_VERSION = "1"                      # integer versions only (house rule)
PREREG_STATUS = "draft"
PREREG_PATH = REPO / "docs" / "ruleclass" / "PREREG_rules.md"

RS = "/rs/rs_grp_oschome/go2432"
AH = RS + "/data/anomaly_harvest"
HOME = "/wsu/home/go/go24/go2432"
DEFAULTS = dict(
    moller_root=RS + "/ruleclass/arms/moller_fast",
    ts_root=RS + "/ruleclass/arms/ts",
    pelvis_root=RS + "/ruleclass/arms/pelvis",
    ah_root=AH,
    registry=str(REPO / "SchwingNet/results/transitional_registry/registry.csv"),
    lstv_flags=HOME + "/lstv_flag/lstv_flag_labels_v2.csv",
    verse_suppl=HOME + "/lstv_flag/sources/verse_suppl_table1.csv",
    consensus=str(REPO.parent / "CTSpinoPelvic1K-1/docs/castellvi_consensus.csv"),
    ctsp_manifest=HOME + "/data/CTSpinoPelvic1K/manifest.json",
    confirmer="CONFIRMER",              # stage-2 reviewer placeholder: a config value, not a name on disk
)

# ---- thresholds, all from PREREG_rules.md (section given) ------------------------------------------------------
RIB_MM = 38.0                 # 1, 3: Moller / Wigh / Loffler stump threshold
F_FREE, F_ABSORBED = 0.10, 0.50   # 1: f < 0.10 free; 0.10 <= f < 0.50 contact; f >= 0.50 absorbed
SACRUM_MIN_ML = 5.0           # 0, 1: sacrum in field
ANCHOR_DIFF_MM = 20.0         # 1: Dataset803 vs TS anchors
G1_MM = 10.0                  # 3: unassigned rib component within 10 mm of the measured end -> BROKEN?
G2_FRAC, G2_MM, G2_MAX_LEN = 0.50, 2.0, 60.0   # 3: false rib along the costal process (implementation choice, see doc)
SFJ_CONTACT_MM = 2.5          # 1b: superior articular voxels within 2.5 mm of the inferior articular above
BODY_IDS = tuple(range(19, 26)) + (28,)        # 1: T12, L1..L6, T13
VERTEBRA_IDS = tuple(range(1, 26)) + (28,)
MIN_INST_VOX = 50             # spineps_ids floor for an instance to count as present
FRAGMENT_FRAC = 0.15          # spineps_ids relabel rule: < 15 % of the median named instance is a fragment
MORPH_MIN_VOX = 2000          # tp_morphology floor for a per-body measurement
PREVALENCE_WINDOWS = {        # 5: outside checks (percent of CTs)
    "six_count_share_pct": (2.0, 5.0),          # L6 by CT reads ~2-5 %
    "stump_subject_share_pct": (12.6, 20.5),    # stump twelfth rib 12.6 % (Nagata) / >= 1 stump 20.5 % (Moller)
    "lumbar_rib_share_pct": (0.6, 4.3),
}

VERSE_NAME = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
              **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "S", 27: "Co", 28: "T13"}
RANK = {**{i: float(i) for i in range(1, 27)}, 28: 19.5, 25: 24.5, 27: 27.0}      # anatomical order (T13 after T12)
SEM = dict(arcus=41, spinous=42, cp_left=43, cp_right=44, sap_left=45, sap_right=46, iap_left=47, iap_right=48,
           corpus_border=49, corpus=50, ep_sup=52, ep_inf=53, ala_left=70, ala_right=71, sac_post=72, sac_body=73,
           sac_plate=74, disc=100)


class RulesError(RuntimeError):
    """A case that cannot be scored; written as status=failed, never guessed."""


# ---- origin-free bookkeeping: hashes, git, time ----------------------------------------------------------------
@lru_cache(maxsize=4096)
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@lru_cache(maxsize=1)
def git_sha() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True,
                              timeout=30).stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


@lru_cache(maxsize=1)
def prereg_sha256() -> str:
    return sha256_file(str(PREREG_PATH))


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Inputs:
    """Every file read for a case, hashed once."""

    def __init__(self):
        self.files: dict[str, dict] = {}

    def add(self, role: str, path) -> str:
        p = str(path)
        if role not in self.files:
            self.files[role] = {"path": p, "sha256": sha256_file(p), "bytes": os.path.getsize(p)}
        return p


# ---- geometry (everything through the affine; array order is never assumed) -----------------------------------------
def load_img(path):
    import nibabel as nib
    return nib.load(str(path))


def as_int_array(img) -> np.ndarray:
    arr = np.asanyarray(img.dataobj)
    if arr.dtype.kind == "f":
        arr = np.rint(arr)
    return arr.astype(np.int32 if arr.max() > 32767 else np.int16, copy=False)


def same_grid(a_img, b_img, atol=1e-3) -> bool:
    return tuple(a_img.shape[:3]) == tuple(b_img.shape[:3]) and np.allclose(a_img.affine, b_img.affine, atol=atol)


def regrid_nearest(src_img, ref_img) -> np.ndarray:
    """Nearest-neighbour resample of a label image onto ref's grid, in memory only (never written)."""
    from scipy import ndimage
    src = as_int_array(src_img)
    M = np.linalg.inv(src_img.affine) @ ref_img.affine
    shp = ref_img.shape[:3]
    ii, jj, kk = np.meshgrid(np.arange(shp[0]), np.arange(shp[1]), np.arange(shp[2]), indexing="ij")
    coords = np.stack([ii.ravel(), jj.ravel(), kk.ravel(), np.ones(ii.size)], 0).astype(np.float64)
    v = (M @ coords)[:3]
    out = ndimage.map_coordinates(src, v, order=0, mode="constant", cval=0)
    return out.reshape(shp).astype(src.dtype)


def world_of(idx: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Voxel indices (N,3) -> world RAS mm (N,3)."""
    return idx @ A[:3, :3].T + A[:3, 3]


def s_of(idx: np.ndarray, A: np.ndarray) -> np.ndarray:
    return idx @ A[2, :3] + A[2, 3]


def bbox(mask: np.ndarray, pad: int = 0):
    nz = np.nonzero(mask)
    if nz[0].size == 0:
        return None
    sl = []
    for k in range(3):
        lo, hi = int(nz[k].min()) - pad, int(nz[k].max()) + 1 + pad
        sl.append(slice(max(lo, 0), min(hi, mask.shape[k])))
    return tuple(sl)


def grid_corners_world(shape, A) -> np.ndarray:
    c = np.array([[i, j, k] for i in (0, shape[0] - 1) for j in (0, shape[1] - 1) for k in (0, shape[2] - 1)],
                 float)
    return world_of(c, A)


def slice_spacing_S(A) -> float:
    """The voxel step along world S (the largest |A[2, axis]|), i.e. the caudal-slice tolerance."""
    return float(np.max(np.abs(A[2, :3])))


def voxel_ml(A) -> float:
    return abs(float(np.linalg.det(A[:3, :3]))) / 1000.0


def largest_component(mask: np.ndarray):
    """(largest 26-connected component mask, n_components, fraction in the largest). Give it a CROP, never a full
    volume: a full-volume label pass costs 8 s on a 512^3 grid."""
    from scipy import ndimage
    if not mask.any():
        return mask, 0, 0.0
    lab, n = ndimage.label(mask, structure=np.ones((3, 3, 3), bool))
    if n == 1:
        return mask, 1, 1.0
    cnt = np.bincount(lab.ravel())
    cnt[0] = 0
    k = int(np.argmax(cnt))
    return lab == k, int(n), float(cnt[k] / mask.sum())


def label_index(arr: np.ndarray) -> dict:
    """{id: bounding-box slices} for every non-zero id, in ONE pass (ndimage.find_objects). Everything downstream
    works inside these boxes; the full-volume nonzero scans this replaces were 70 % of the run time."""
    from scipy import ndimage
    objs = ndimage.find_objects(arr)
    return {i + 1: sl for i, sl in enumerate(objs) if sl is not None}


def union_slices(regs, shape, pad: int = 0):
    regs = [r for r in regs if r is not None]
    if not regs:
        return None
    return tuple(slice(max(min(r[k].start for r in regs) - pad, 0), min(max(r[k].stop for r in regs) + pad, shape[k]))
                 for k in range(3))


def pad_slices(reg, shape, pad: int):
    return tuple(slice(max(reg[k].start - pad, 0), min(reg[k].stop + pad, shape[k])) for k in range(3))


def offset_of(reg) -> np.ndarray:
    return np.array([s.start for s in reg])


def full_from_crop(shape, reg, crop: np.ndarray) -> np.ndarray:
    out = np.zeros(shape, bool)
    out[reg] = crop
    return out


def extent_pct(v: np.ndarray, lo=0.5, hi=99.5) -> float | None:
    if v.size < 5:
        return None
    return float(np.percentile(v, hi) - np.percentile(v, lo))


def rnd(x, n=2):
    if x is None:
        return None
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    try:
        if isinstance(x, (float, np.floating)) and (math.isnan(x) or math.isinf(x)):
            return None
        return round(float(x), n)
    except (TypeError, ValueError):
        return x


def cid_norm(collection: str, case_id: str) -> str:
    """CTSP ids are zero padded to four (the release form); everything else is passed through."""
    if collection == "ctsp" and case_id.isdigit():
        return case_id.zfill(4)
    return case_id


def safe(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if (np.isnan(o) or np.isinf(o)) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, slice):
        return [o.start, o.stop]
    return o


# ---- the SPINEPS pair -------------------------------------------------------------------------------------------------
class Spine:
    """The SPINEPS instance + semantic masks of one CT, on the instance grid, with per-instance statistics."""

    def __init__(self, vert_img, spine_img, ids_info: dict, vert_arr: np.ndarray | None = None):
        self.img = vert_img
        self.A = np.asarray(vert_img.affine, float)
        self.vert = vert_arr if vert_arr is not None else as_int_array(vert_img)
        if same_grid(spine_img, vert_img):
            self.sem = as_int_array(spine_img)
            self.sem_regridded = False
        else:
            self.sem = regrid_nearest(spine_img, vert_img)
            self.sem_regridded = True
        self.ids_info = ids_info
        self.shape = self.vert.shape
        self.vox_ml = voxel_ml(self.A)
        self.objs = label_index(self.vert)          # one pass: every instance's box
        self.sem_objs = label_index(self.sem)       # one pass: every subregion's box
        self.inst: dict[int, dict] = {}
        self._stats()

    def _stats(self):
        v = self.vert
        vols = {}
        for i, reg in self.objs.items():
            if not 0 < i < 100:
                continue
            m = v[reg] == i
            n = int(m.sum())
            if n < MIN_INST_VOX:
                continue
            idx = np.argwhere(m) + offset_of(reg)
            W = world_of(idx, self.A)
            vols[i] = n
            self.inst[i] = dict(id=i, name=VERSE_NAME.get(i, str(i)), vox=n, ml=n * self.vox_ml,
                                centroid=W.mean(0), s_min=float(W[:, 2].min()), s_max=float(W[:, 2].max()),
                                x_min=float(W[:, 0].min()), x_max=float(W[:, 0].max()), bbox=reg,
                                rank=RANK.get(i, float(i)))
        named = [n for i, n in vols.items() if i in VERTEBRA_IDS and i not in (26, 27)]
        med = float(np.median(named)) if named else 0.0
        for i, d in self.inst.items():
            d["fragment"] = bool(i not in (26, 27) and med > 0 and d["vox"] < FRAGMENT_FRAC * med)
        self.median_vertebra_vox = med

    def mask(self, i: int) -> np.ndarray:
        """Full-size boolean of one instance, built from its box (no full-volume compare)."""
        reg = self.objs.get(i)
        if reg is None:
            return np.zeros(self.shape, bool)
        return full_from_crop(self.shape, reg, self.vert[reg] == i)

    def inst_crop(self, i: int, pad: int = 0):
        reg = self.objs.get(i)
        if reg is None:
            return None, None
        if pad:
            reg = pad_slices(reg, self.shape, pad)
        return reg, self.vert[reg] == i

    def sub_crop(self, sem_id: int, inst_id: int | None = None, region=None):
        """(box, crop) of a semantic subregion, inside one instance's box when inst_id is given, else its own box.
        (None, None) when absent."""
        if region is None:
            region = self.objs.get(inst_id) if inst_id is not None else self.sem_objs.get(sem_id)
        if region is None:
            return None, None
        m = self.sem[region] == sem_id
        if inst_id is not None:
            m &= self.vert[region] == inst_id
        return region, m

    def sub(self, sem_id: int, inst_id: int | None = None, region=None) -> np.ndarray:
        """Full-size semantic subregion (optionally inside one instance); the compare runs inside a box only."""
        reg, m = self.sub_crop(sem_id, inst_id, region)
        if reg is None:
            return np.zeros(self.shape, bool)
        return full_from_crop(self.shape, reg, m)

    def vertebrae_by_S(self) -> list[int]:
        """Instance ids of vertebrae (not sacrum/coccyx/discs), cranial to caudal by world S centroid."""
        ids = [i for i in self.inst if i in VERTEBRA_IDS and i not in (26, 27)]
        return sorted(ids, key=lambda i: -self.inst[i]["centroid"][2])

    def sacrum_component(self):
        """SPINEPS's own sacrum instance 26: the component under the lumbar column (never the whole instance)."""
        if 26 not in self.inst:
            return None
        reg, m = self.inst_crop(26)
        from scipy import ndimage
        lab, n = ndimage.label(m, structure=np.ones((3, 3, 3), bool))
        if n <= 1:
            comp = m
        else:
            # the component whose top lies nearest below the lowest vertebra instance
            verts = self.vertebrae_by_S()
            ref_s = self.inst[verts[-1]]["centroid"][2] if verts else None
            best, best_d = None, None
            for k in range(1, n + 1):
                ck = lab == k
                if ck.sum() < MIN_INST_VOX:
                    continue
                s = s_of(np.argwhere(ck) + offset_of(reg), self.A)
                d = abs(float(s.max()) - ref_s) if ref_s is not None else -float(ck.sum())
                if best is None or d < best_d:
                    best, best_d = ck, d
            comp = best if best is not None else m
        W = world_of(np.argwhere(comp) + offset_of(reg), self.A)
        return dict(bbox=reg, crop=comp, world=W, vox=int(comp.sum()), ml=int(comp.sum()) * self.vox_ml,
                    s_max=float(W[:, 2].max()), s_min=float(W[:, 2].min()), n_components=int(n))


def load_spine(row: dict, inputs: Inputs) -> Spine:
    """The tier row's SPINEPS pair, id-guarded: verse_coded masks pass the guard (a raised guard is recorded, since the
    count needs instances, not names), raw masks are relabelled in memory through the ctd or the case is refused."""
    if spineps_ids is None:
        raise RulesError("tools/spineps_ids.py not importable: the ids cannot be shown to be names")
    vp, sp, cp = row.get("spineps_vert") or "", row.get("spineps_spine") or "", row.get("spineps_ctd") or ""
    if not vp or not os.path.exists(vp):
        raise RulesError(f"no SPINEPS seg-vert mask ({vp!r})")
    if not sp or not os.path.exists(sp):
        raise RulesError(f"no SPINEPS seg-spine mask ({sp!r})")
    inputs.add("spineps_vert", vp)
    inputs.add("spineps_spine", sp)
    if cp and os.path.exists(cp):
        inputs.add("spineps_ctd", cp)
    else:
        cp = spineps_ids.find_ctd(vp) or ""
        if cp:
            inputs.add("spineps_ctd", cp)
    vimg, simg = load_img(vp), load_img(sp)
    info = {"ids_state": row.get("spineps_ids", ""), "ctd": cp or None}
    arr = None
    if row.get("spineps_ids", "") == "raw":
        pts = spineps_ids.read_ctd(cp) if cp else None
        if not pts:
            raise RulesError("raw SPINEPS ids and no ctd: refused (a raw id read as a name is a plausible wrong answer)")
        a0, A0, _ = spineps_ids.load_mask(vp)
        sa, sA, _ = spineps_ids.load_mask(sp)
        try:
            arr, rep = spineps_ids.relabel_by_ctd(a0, A0, pts, semantic=(sa, sA))
            info.update(ids_verdict="relabelled_in_memory", ids_notes=str(rep.get("notes", ""))[:500])
            arr = arr.astype(np.int16 if arr.max() < 32767 else np.int32)
        except spineps_ids.SpinepsIdError as e:
            raise RulesError(f"raw SPINEPS ids refused by relabel_by_ctd: {str(e)[:400]}") from e
    else:
        rep = spineps_ids.check_ids(vp, cp or "auto")
        v = rep.get("verdict", "")
        info.update(ids_verdict=v, ids_reasons=rep.get("reasons", [])[:4],
                    veridah_skipped_names=[g.get("missing") for g in rep.get("veridah_skipped_names", [])],
                    ctd_labels=rep.get("ctd_labels"))
        if v in ("not_verse_ids", "raw_or_scrambled"):
            raise RulesError(f"SPINEPS ids are not VerSe names [{v}]: {'; '.join(rep.get('reasons', []))[:300]}")
        info["ids_guard_raised"] = v not in ("verse_ok", "empty", "misnamed_1_2_levels") \
            or bool(rep.get("veridah_skipped_names"))
    return Spine(vimg, simg, info, arr)


# ---- the field --------------------------------------------------------------------------------------------------------
def field_extent(row: dict, spine: Spine, inputs: Inputs) -> dict:
    """World extent of the imaged field from the CT header (no intensity read); the SPINEPS grid if the CT is absent."""
    out = {"field_source": "spineps_grid"}
    ct = row.get("ct_path") or ""
    if ct and os.path.exists(ct):
        try:
            img = load_img(ct)
            inputs.add("ct_header", ct)
            W = grid_corners_world(img.shape[:3], np.asarray(img.affine, float))
            out.update(field_source="ct_header", ct_shape=list(img.shape[:3]),
                       ct_axcodes=list(__import__("nibabel").aff2axcodes(img.affine)),
                       ct_grid_matches_spineps=bool(same_grid(img, spine.img)),
                       slice_S_mm=slice_spacing_S(np.asarray(img.affine, float)))
        except Exception as e:  # noqa: BLE001
            out["ct_header_error"] = repr(e)[:200]
            W = grid_corners_world(spine.shape, spine.A)
            out["slice_S_mm"] = slice_spacing_S(spine.A)
    else:
        W = grid_corners_world(spine.shape, spine.A)
        out["slice_S_mm"] = slice_spacing_S(spine.A)
        out["ct_missing"] = True
    out.update(S_min=float(W[:, 2].min()), S_max=float(W[:, 2].max()), x_min=float(W[:, 0].min()),
               x_max=float(W[:, 0].max()), y_min=float(W[:, 1].min()), y_max=float(W[:, 1].max()))
    return out


# ---- sacral anchors: CTSP GT (labels_for), Dataset803 post (labels_for), TS sacrum union S1 -----------------------
def crop_of_ids(arr: np.ndarray, objs: dict, ids, shape, pad: int = 0):
    """(box, crop mask) of the union of label ids in arr, using the one-pass index; (None, None) when absent."""
    reg = union_slices([objs.get(i) for i in ids], shape, pad)
    if reg is None:
        return None, None
    sub = arr[reg]
    m = np.zeros(sub.shape, bool)
    for i in ids:
        m |= sub == i
    return reg, m


def _sacrum_summary(name: str, shape, reg, cmask, A: np.ndarray, field: dict, hips: dict | None = None) -> dict:
    """Largest component, volume, top S, caudal-slice contact; hips' crest tops when given. All work inside boxes;
    the returned `mask` is full-size (built by assignment) and `bbox` is its box."""
    vml = voxel_ml(A)
    if reg is None or cmask is None or not cmask.any():
        return dict(source=name, present=False, vox=0, ml=0.0, n_components=0, largest_fraction=None, largest_ml=0.0,
                    top_S_mm=None, bottom_S_mm=None, touches_caudal_slice=None, mask=None, bbox=None, in_field=False,
                    not_in_field_reason="sacrum absent")
    comp, ncomp, frac = largest_component(cmask)
    d = dict(source=name, present=True, vox=int(cmask.sum()), ml=float(cmask.sum() * vml),
             n_components=ncomp, largest_fraction=rnd(frac, 3))
    W = world_of(np.argwhere(comp) + offset_of(reg), A)
    tol = 1.01 * field.get("slice_S_mm", 1.0)
    d.update(largest_ml=float(comp.sum() * vml), top_S_mm=float(W[:, 2].max()), bottom_S_mm=float(W[:, 2].min()),
             touches_caudal_slice=bool(W[:, 2].min() <= field["S_min"] + tol),
             touches_cranial_slice=bool(W[:, 2].max() >= field["S_max"] - tol),
             x_mid_mm=float(np.median(W[:, 0])), mask=full_from_crop(shape, reg, comp), bbox=reg)
    d["in_field"] = bool(d["largest_ml"] >= SACRUM_MIN_ML and not d["touches_caudal_slice"])
    d["not_in_field_reason"] = None if d["in_field"] else (
        f"sacrum {d['largest_ml']:.1f} mL < {SACRUM_MIN_ML} mL" if d["largest_ml"] < SACRUM_MIN_ML
        else "sacrum touches the caudal slice")
    if hips:
        for side in ("left", "right"):
            hreg, hm = hips.get(side, (None, None))
            if hm is None or not hm.any():
                d[f"hip_{side}_crest_top_S_mm"] = None
                d[f"hip_{side}_ml"] = 0.0
                continue
            hc, _, _ = largest_component(hm)
            hs = s_of(np.argwhere(hc) + offset_of(hreg), A)
            d[f"hip_{side}_crest_top_S_mm"] = float(hs.max())
            d[f"hip_{side}_ml"] = float(hc.sum() * vml)
        tops = [d.get(f"hip_{s}_crest_top_S_mm") for s in ("left", "right")]
        tops = [t for t in tops if t is not None]
        d["hips_present"] = len(tops)
        d["mean_crest_top_S_mm"] = float(np.mean(tops)) if tops else None
    return d


def _on_spine_grid(img, spine: Spine, note: dict, key: str) -> np.ndarray:
    if same_grid(img, spine.img):
        return as_int_array(img)
    note.setdefault("regridded_to_spineps_grid", []).append(key)
    return regrid_nearest(img, spine.img)


def anchor_ctsp_gt(row: dict, spine: Spine, field: dict, inputs: Inputs, note: dict) -> dict | None:
    """CTSP v11 label through ostk.labels.labels_for (never a fixed map). Only for collection ctsp."""
    gt = row.get("gt_label") or ""
    if row.get("collection") != "ctsp" or not gt or "CTSpinoPelvic1K" not in gt or not os.path.exists(gt):
        return None
    if "labels_v10" in gt:
        return dict(source="ctsp_gt", refused="labels_v10 carries the retired id 29 and is not read")
    try:
        from ostk.labels import labels_for, detect_scheme, SchemeError
    except ImportError:
        return dict(source="ctsp_gt", refused="ostk not importable: the label scheme cannot be resolved")
    inputs.add("ctsp_gt_label", gt)
    img = load_img(gt)
    arr = _on_spine_grid(img, spine, note, "ctsp_gt")
    ids, cnt = np.unique(arr, return_counts=True)
    counts = dict(zip(ids.tolist(), cnt.tolist()))
    try:
        scheme = detect_scheme(None, counts=counts)
    except SchemeError as e:
        return dict(source="ctsp_gt", refused=f"labels_for could not resolve the scheme: {e}")
    L = labels_for(None, counts=counts)
    pelvis_vox = sum(counts.get(L[k], 0) for k in ("left_hip", "right_hip", "femur_left", "femur_right"))
    objs = label_index(arr)
    reg, cm = crop_of_ids(arr, objs, [L["sacrum"]], spine.shape)
    d = _sacrum_summary("ctsp_gt", spine.shape, reg, cm, spine.A, field,
                        hips={"left": crop_of_ids(arr, objs, [L["left_hip"]], spine.shape),
                              "right": crop_of_ids(arr, objs, [L["right_hip"]], spine.shape)})
    d.update(scheme=scheme, scheme_by_default=bool(pelvis_vox == 0), sacrum_id=L["sacrum"],
             gt_ids_present=sorted(int(i) for i in ids if i),
             gt_lumbar_ids=[VERSE_NAME.get(i) for i in (20, 21, 22, 23, 24, 25) if counts.get(L[VERSE_NAME[i]], 0)
                            >= MIN_INST_VOX] if scheme == "v10" else None,
             gt_has_T13=bool(counts.get(L.get("T13", -1), 0) >= MIN_INST_VOX),
             gt_has_lumbar_rib=bool(counts.get(L.get("rib_left_lumbar", -1), 0) + counts.get(L.get("rib_right_lumbar", -1), 0) > 0),
             gt_has_id29=bool(counts.get(29, 0) > 0 and scheme == "v10"))
    if d["gt_has_id29"]:
        d["warning"] = "identifier 29 present in a v11 label (retired id): check the label source"
    return d


def anchor_dataset803(row: dict, spine: Spine, field: dict, inputs: Inputs, note: dict, pelvis_root: str) -> dict | None:
    """Dataset803 post-processed pelvis (sacrum 26, hips 30/31 after pelvis_post.py). _work/ and _failed_raw/ are never read."""
    coll, cid = row["collection"], row["case_id"]
    cands = [Path(pelvis_root) / coll / f"{cid}.nii.gz"]
    for sub in sorted(Path(pelvis_root).glob("*")) if os.path.isdir(pelvis_root) else []:
        if sub.is_dir() and not sub.name.startswith("_"):
            cands.append(sub / coll / f"{cid}.nii.gz")
    path = next((c for c in cands if c.exists() and "_work" not in c.parts and "_failed_raw" not in c.parts), None)
    if path is None:
        return None
    side = path.with_suffix("").with_suffix(".json")
    meta = {}
    if side.exists():
        inputs.add("dataset803_json", side)
        meta = json.loads(side.read_text())
        if meta.get("status") not in (None, "ok"):
            return dict(source="dataset803", refused=f"sidecar status {meta.get('status')!r}", path=str(path))
    try:
        from ostk.labels import labels_for, SchemeError
    except ImportError:
        return dict(source="dataset803", refused="ostk not importable: the label scheme cannot be resolved", path=str(path))
    inputs.add("dataset803_nii", path)
    img = load_img(path)
    arr = _on_spine_grid(img, spine, note, "dataset803")
    ids, cnt = np.unique(arr, return_counts=True)
    counts = dict(zip(ids.tolist(), cnt.tolist()))
    try:
        L = labels_for(None, counts=counts)
    except SchemeError as e:
        return dict(source="dataset803", refused=f"labels_for could not resolve the scheme: {e}", path=str(path))
    want = {"sacrum": 26, "left_hip": 30, "right_hip": 31}
    got = {k: L[k] for k in want}
    if got != want:
        return dict(source="dataset803", refused=f"labels_for resolved {got}, contract requires {want}", path=str(path))
    extra = sorted(int(i) for i in ids if i and int(i) not in (26, 30, 31))
    if extra:
        return dict(source="dataset803", refused=f"ids outside the contract {{0,26,30,31}}: {extra} (a raw prediction?)",
                    path=str(path))
    objs = label_index(arr)
    reg, cm = crop_of_ids(arr, objs, [26], spine.shape)
    d = _sacrum_summary("dataset803", spine.shape, reg, cm, spine.A, field,
                        hips={"left": crop_of_ids(arr, objs, [30], spine.shape), "right": crop_of_ids(arr, objs, [31], spine.shape)})
    d.update(path=str(path), sidecar_sacrum_top_S_mm=meta.get("sacrum_top_S_mm"), sidecar_mode=meta.get("mode"),
             sidecar_laterality=meta.get("laterality"))
    return d


def load_ts(row: dict, spine: Spine, inputs: Inputs, note: dict, ts_root: str) -> dict | None:
    """TotalSegmentator total: the arm A multilabel (has hips) when present, else the tier row's ts_output (multilabel
    or the roi-subset directory, which has no hips). Returns arrays on the SPINEPS grid + the class map, or None."""
    coll, cid = row["collection"], row["case_id"]
    out = {"ts_source": None}
    arma = Path(ts_root) / coll / f"{cid}.nii.gz"
    cmap_path = Path(ts_root) / "class_map.json"
    multi = None
    if arma.exists() and cmap_path.exists():
        multi, cmap_p, out["ts_source"] = arma, cmap_path, "arm_a_total_multilabel"
    elif (row.get("ts_kind") or "").startswith("total_multilabel") and os.path.exists(row.get("ts_output") or ""):
        multi, cmap_p, out["ts_source"] = Path(row["ts_output"]), Path(row.get("ts_class_map") or ""), "tier_total_multilabel"
    if multi is not None:
        if not cmap_p.exists():
            return dict(ts_source=out["ts_source"], refused=f"class map missing: {cmap_p}")
        inputs.add("ts_multilabel", multi)
        inputs.add("ts_class_map", cmap_p)
        cmap = {int(k): v for k, v in json.loads(Path(cmap_p).read_text()).items()}
        name2id = {v: k for k, v in cmap.items()}
        img = load_img(multi)
        arr = _on_spine_grid(img, spine, note, "ts")
        out.update(arr=arr, name2id=name2id, has_hips=True, path=str(multi), objs=label_index(arr),
                   counts=np.bincount(arr.ravel(), minlength=256))
        return out
    d = row.get("ts_output") or ""
    if (row.get("ts_kind") or "").startswith("roi_subset") and os.path.isdir(d):
        pieces = {}
        for nm in ("sacrum", "vertebrae_S1", "vertebrae_L5", "vertebrae_L4", "vertebrae_L1", "vertebrae_T12"):
            p = Path(d) / f"{nm}.nii.gz"
            if p.exists():
                inputs.add(f"ts_roi_{nm}", p)
                pieces[nm] = (_on_spine_grid(load_img(p), spine, note, f"ts_roi_{nm}") > 0).astype(np.uint8)
        if "sacrum" not in pieces:
            return dict(ts_source="roi_subset_dir", refused="no sacrum.nii.gz in the roi-subset directory")
        out.update(ts_source="roi_subset_dir_no_hips", pieces=pieces, has_hips=False, path=d)
        return out
    return None


def anchor_ts(ts: dict | None, spine: Spine, field: dict) -> dict | None:
    if not ts or ts.get("refused"):
        return dict(source="ts_sacrum_union_s1", refused=ts.get("refused")) if ts else None
    if "arr" in ts:
        arr, n2i, objs = ts["arr"], ts["name2id"], ts["objs"]
        reg, cm = crop_of_ids(arr, objs, [n2i["sacrum"], n2i["vertebrae_S1"]], spine.shape)
        hips = {"left": crop_of_ids(arr, objs, [n2i["hip_left"]], spine.shape),
                "right": crop_of_ids(arr, objs, [n2i["hip_right"]], spine.shape)}
        d = _sacrum_summary("ts_sacrum_union_s1", spine.shape, reg, cm, spine.A, field, hips=hips)
        d["s1_ml"] = float(ts["counts"][n2i["vertebrae_S1"]] * spine.vox_ml) if n2i["vertebrae_S1"] < len(ts["counts"]) else None
    else:
        P = ts["pieces"]
        u = P["sacrum"].copy()
        if "vertebrae_S1" in P:
            u |= P["vertebrae_S1"]
        objs = label_index(u)
        reg, cm = crop_of_ids(u, objs, [1], spine.shape)
        d = _sacrum_summary("ts_sacrum_union_s1", spine.shape, reg, cm, spine.A, field, hips=None)
        d["s1_ml"] = float(P["vertebrae_S1"].sum() * spine.vox_ml) if "vertebrae_S1" in P else None
        d["hips_present"] = 0
    d["ts_source"] = ts["ts_source"]
    return d


# ---- Moller arm B ------------------------------------------------------------------------------------------------
def _fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _bool(x):
    return str(x).strip().lower() in ("true", "1", "yes")


def load_moller(row: dict, spine: Spine, inputs: Inputs, note: dict, moller_root: str) -> dict:
    """The rib table of the variant used (t13_admitted where it exists, else upstream), the rib-inst mask on the
    SPINEPS grid, and the assigned-rib levels from the done json."""
    coll, cid = row["collection"], row["case_id"]
    d = Path(moller_root) / coll
    csvp, done = d / f"{cid}_rib_measurements.csv", d / "_done" / f"{cid}.measure.json"
    out = dict(present=False, variant=None, rows=[], levels=None, inst=None)
    if not csvp.exists() and not done.exists():
        out["missing"] = f"no Moller output under {d}"
        return out
    meta = {}
    if done.exists():
        inputs.add("moller_measure_json", done)
        meta = json.loads(done.read_text())
        out["moller_ok"] = meta.get("ok")
        out["moller_skipped"] = meta.get("skipped")
        out["moller_ids_verdict"] = meta.get("ids_verdict")
    rows = []
    if csvp.exists():
        inputs.add("moller_csv", csvp)
        with open(csvp, encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    variants = sorted({r.get("variant", "upstream") for r in rows})
    out["variants_present"] = variants
    variant = "t13_admitted" if "t13_admitted" in variants or f"levels_t13_admitted" in meta else "upstream"
    out["variant"] = variant
    table = []
    for r in rows:
        if r.get("variant", "upstream") != variant:
            continue
        v = r.get("vertebra")
        try:
            v = int(float(v))
        except (TypeError, ValueError):
            continue
        table.append(dict(vertebra=v, side=r.get("side"), rib_length=_fl(r.get("rib_length")),
                          sr=_bool(r.get("sr")), seg_at_border=_bool(r.get("seg_at_border")),
                          rib_volume=_fl(r.get("rib_volume")), is_last_v=_bool(r.get("is_last_v")),
                          n_path_points=_fl(r.get("n_path_points")), measure_error=r.get("measure_error") or None,
                          pdrc=_fl((r.get("f_49_start_to_com_direction") or "").split(";")[0])))
    out["rows"] = table
    out["rows_upstream"] = [dict(vertebra=int(float(r["vertebra"])), side=r["side"], rib_length=_fl(r["rib_length"]),
                                 seg_at_border=_bool(r.get("seg_at_border")))
                            for r in rows if r.get("variant", "upstream") == "upstream" and r.get("vertebra")]
    lv = meta.get(f"levels_{variant}") or meta.get("levels_upstream") or {}
    if lv:
        out["levels"] = {int(k): v for k, v in (lv.get("rib_bearing") or {}).items()}
        out["unassigned_rib_vox"] = lv.get("unassigned_rib_vox")
    inst_p = d / (f"{cid}_rib-inst-t13_msk.nii.gz" if variant == "t13_admitted" else f"{cid}_rib-inst_msk.nii.gz")
    if not inst_p.exists():
        inst_p = d / f"{cid}_rib-inst_msk.nii.gz"
    if inst_p.exists():
        inputs.add("moller_rib_inst", inst_p)
        img = load_img(inst_p)
        out["inst"] = _on_spine_grid(img, spine, note, "moller_rib_inst")
        out["inst_objs"] = label_index(out["inst"])
        out["inst_path"] = str(inst_p)
    out["present"] = bool(table) or bool(out["levels"])
    return out


def rib_summary(moller: dict) -> dict:
    """Per vertebra: max length per side, border flags, rib-bearing (> 38 mm on >= 1 side, PREREG 1)."""
    per = {}
    for r in moller["rows"]:
        e = per.setdefault(r["vertebra"], {"left": None, "right": None})
        if r["side"] in ("left", "right") and r["rib_length"] is not None:
            cur = e[r["side"]]
            if cur is None or r["rib_length"] > cur["rib_length"]:
                e[r["side"]] = r
    out = {}
    for v, e in per.items():
        lens = {s: (e[s]["rib_length"] if e[s] else None) for s in ("left", "right")}
        full = [s for s in ("left", "right") if lens[s] is not None and lens[s] > RIB_MM]
        out[v] = dict(vertebra=v, name=VERSE_NAME.get(v, str(v)), left=e["left"], right=e["right"], lens=lens,
                      rib_bearing=bool(full), full_sides=full,
                      whole_rib=any(not e[s]["seg_at_border"] for s in full) if full else False)
    return out


# ---- rule 1 ---------------------------------------------------------------------------------------------------------
def choose_anchor(anchors: dict) -> tuple[str | None, list[str]]:
    """Priority: ctsp_gt (ground truth) > dataset803 > ts_sacrum_union_s1. Returns (source, reasons for no_anchor)."""
    reasons = []
    for src in ("ctsp_gt", "dataset803", "ts_sacrum_union_s1"):
        a = anchors.get(src)
        if a is None:
            continue
        if a.get("refused"):
            reasons.append(f"{src}: {a['refused']}")
            continue
        if not a.get("present"):
            reasons.append(f"{src}: sacrum absent")
            continue
        if not a.get("in_field"):
            reasons.append(f"{src}: {a.get('not_in_field_reason')}")
            continue
        return src, reasons
    if not reasons:
        reasons.append("no sacrum source on disk (no CTSP GT, no Dataset803, no TS output)")
    return None, reasons


def anchor_plane(anchor: dict, spine: Spine) -> dict:
    """The anchor S: SPINEPS sacral end-plate (74) where it lies inside the anchor sacrum, else the sacrum top."""
    m = anchor["mask"]
    reg, pc = spine.sub_crop(SEM["sac_plate"])
    plate = (pc & m[reg]) if reg is not None else None
    n = int(plate.sum()) if plate is not None else 0
    if n >= 100:
        s = s_of(np.argwhere(plate) + offset_of(reg), spine.A)
        return dict(anchor_S_mm=float(np.median(s)), anchor_definition="spineps74_in_sacrum", plate74_vox=n,
                    plate74_S_mm=float(np.median(s)), sacrum_top_S_mm=anchor["top_S_mm"])
    return dict(anchor_S_mm=anchor["top_S_mm"], anchor_definition="sacrum_top_S", plate74_vox=n,
                plate74_S_mm=None, sacrum_top_S_mm=anchor["top_S_mm"])


def count_under(anchor: dict, plane: dict, spine: Spine, lowest_rb: int | None, order: list[int]) -> dict:
    """PREREG 1: per instance in 19-25/28 caudal to the lowest rib-bearing vertebra, f = |inst ∩ sacrum| / |inst|."""
    m = anchor["mask"]
    bodies = []
    if lowest_rb is None:
        cand = []
    else:
        pos = order.index(lowest_rb) if lowest_rb in order else -1
        cand = [i for i in order[pos + 1:] if i in BODY_IDS] if pos >= 0 else []
    for i in cand:
        d = spine.inst[i]
        reg = d["bbox"]
        im = spine.vert[reg] == i
        inter = int((im & m[reg]).sum())
        f = inter / d["vox"]
        cls = "free" if f < F_FREE else ("contact" if f < F_ABSORBED else "absorbed")
        below = bool(d["s_max"] < plane["anchor_S_mm"])
        bodies.append(dict(id=i, name=d["name"], vox=d["vox"], ml=rnd(d["ml"], 1), fragment=d["fragment"], f=rnd(f, 4),
                           cls=cls, counted=cls != "absorbed", wholly_below_anchor=below,
                           lumbarisation_candidate=bool(cls == "free" and below), centroid_S_mm=rnd(d["centroid"][2], 1)))
    counted = [b for b in bodies if b["counted"]]
    return dict(bodies=bodies, count=len(counted), count_excluding_fragments=len([b for b in counted if not b["fragment"]]),
                absorbed=[b["name"] for b in bodies if b["cls"] == "absorbed"],
                contact=[b["name"] for b in bodies if b["cls"] == "contact"],
                lumbarisation_candidates=[b["name"] for b in bodies if b["lumbarisation_candidate"]],
                most_cranial_free_body=(counted[0]["id"] if counted else None),
                lowest_free_body=(counted[-1]["id"] if counted else None),
                lowest_free_body_nonfragment=next((b["id"] for b in reversed(counted) if not b["fragment"]), None))


def rule1(spine: Spine, anchors: dict, moller: dict, ribs: dict, field: dict) -> dict:
    out = dict(rule="1", count=None, count_status=None, reasons=[], anchor_source=None)
    order = spine.vertebrae_by_S()
    out["instances_by_S"] = [spine.inst[i]["name"] for i in order]
    order_by_rank = sorted(order, key=lambda i: spine.inst[i]["rank"])
    if order_by_rank != order:
        out["reasons"].append("instance order by world S differs from VerSe rank order; S order used")
    # the lowest rib-bearing vertebra (Moller > 38 mm on >= 1 side); stump-only levels pass to rule 3
    rb = [v for v, e in ribs.items() if e["rib_bearing"] and v in spine.inst]
    lowest_rb = None
    if rb:
        lowest_rb = min(rb, key=lambda v: spine.inst[v]["centroid"][2])
        out["lowest_rib_bearing"] = dict(id=lowest_rb, name=VERSE_NAME.get(lowest_rb), lens=ribs[lowest_rb]["lens"],
                                         whole_rib=ribs[lowest_rb]["whole_rib"], source="moller_measured")
    elif moller.get("levels"):
        # ribs assigned but none measured over 38 mm: the lowest assigned level is not rib-bearing for the count;
        # an unmeasured higher level cannot be shown to carry a whole rib either -> no_count
        out["reasons"].append("Moller assigned ribs but measured none over 38 mm: the lowest rib-bearing vertebra is not shown")
    # anchors
    src, no_anchor_reasons = choose_anchor(anchors)
    out["anchor_source"] = src
    out["no_anchor_reasons"] = no_anchor_reasons
    out["tl_gate"] = "ok" if lowest_rb is not None else "no rib-bearing vertebra with a rib > 38 mm in field (cut field or no Moller output)"
    if lowest_rb is not None and not ribs[lowest_rb]["whole_rib"]:
        out["tl_gate"] = "rib over 38 mm but truncated at the field edge (rib-bearing stands; rule 3 UNDECIDED there)"
    planes, counts = {}, {}
    for s in ("ctsp_gt", "dataset803", "ts_sacrum_union_s1"):
        a = anchors.get(s)
        if a and a.get("present") and a.get("mask") is not None:
            planes[s] = anchor_plane(a, spine)
            counts[s] = count_under(a, planes[s], spine, lowest_rb, order)
    out["anchor_S_by_source"] = {s: rnd(p["anchor_S_mm"], 1) for s, p in planes.items()}
    out["count_by_source"] = {s: c["count"] for s, c in counts.items()}
    out["absorbed_by_source"] = {s: c["absorbed"] for s, c in counts.items()}
    # A (TS) vs B (Dataset803) absorbed disagreement, PREREG 1 last bullet
    if "dataset803" in counts and "ts_sacrum_union_s1" in counts:
        out["absorbed_disagreement_A_vs_B"] = counts["dataset803"]["absorbed"] != counts["ts_sacrum_union_s1"]["absorbed"]
    else:
        out["absorbed_disagreement_A_vs_B"] = None
    if "ctsp_gt" in counts and "ts_sacrum_union_s1" in counts:
        out["absorbed_disagreement_gt_vs_ts"] = counts["ctsp_gt"]["absorbed"] != counts["ts_sacrum_union_s1"]["absorbed"]
        out["anchor_diff_gt_vs_ts_mm"] = rnd(abs(planes["ctsp_gt"]["anchor_S_mm"] - planes["ts_sacrum_union_s1"]["anchor_S_mm"]), 1)
    # 803 vs TS anchor distance with no GT -> no_anchor
    if "dataset803" in planes and "ts_sacrum_union_s1" in planes:
        diff = abs(planes["dataset803"]["anchor_S_mm"] - planes["ts_sacrum_union_s1"]["anchor_S_mm"])
        out["anchor_diff_803_vs_ts_mm"] = rnd(diff, 1)
        if diff > ANCHOR_DIFF_MM and "ctsp_gt" not in planes and src != "ctsp_gt":
            src = None
            out["anchor_source"] = None
            out["no_anchor_reasons"].append(f"Dataset803 and TS anchors differ by {diff:.1f} mm > {ANCHOR_DIFF_MM} with no ground truth")
    if src is None:
        out.update(count="no_count", count_status="no_anchor")
        out["reasons"] += out["no_anchor_reasons"]
    elif lowest_rb is None:
        out.update(count="no_count", count_status="no_rib_bearing_in_field")
        out["reasons"].append(out["tl_gate"])
    else:
        c = counts[src]
        out.update(c)
        out["count_status"] = "counted"
        out["anchor"] = planes[src]
        if c["count"] == 0:
            out.update(count="no_count", count_status="zero_bodies_between_rib_and_sacrum")
            out["reasons"].append("no presacral body between the lowest rib-bearing vertebra and the sacrum")
        # RBC convention (Wigh): a stump-only vertebra stays thoracic; the prereg count is the RLBC form
        stump_only = [v for v, e in ribs.items() if not e["rib_bearing"] and any(l is not None for l in e["lens"].values())]
        in_count = [v for v in stump_only if v in [b["id"] for b in c["bodies"] if b["counted"]]]
        out["count_rbc_convention"] = (c["count"] - len(in_count)) if isinstance(out["count"], int) else out["count"]
        out["stump_only_levels_in_count"] = [VERSE_NAME.get(v) for v in in_count]
        out["castellvi_II_IV_candidate"] = bool(c["contact"])
        out["complete_sacralisation_candidate"] = bool(c["absorbed"])
        out["lumbarisation_candidate"] = bool(c["lumbarisation_candidates"])
        # SPINEPS's own sacrum against the anchor: the 0005 signature (a mobile body swallowed by instance 26)
        sc = spine.sacrum_component()
        if sc is not None:
            # SPINEPS 26 above the ANCHOR SACRUM'S TOP (not the plate plane, which lies ~15-20 mm under the alae)
            Wsc = sc["world"]
            top = anchors[src]["top_S_mm"]
            ml_above = float((Wsc[:, 2] > top + 3.0).sum() * spine.vox_ml)
            # a disc instance with SPINEPS sacrum both above and below it in its own 10 mm column (the 0005 signature)
            disc_inside = []
            for di, dreg in spine.objs.items():
                if not 100 < di < 200:
                    continue
                Wd = world_of(np.argwhere(spine.vert[dreg] == di) + offset_of(dreg), spine.A)
                c = Wd.mean(0)
                col = Wsc[(np.abs(Wsc[:, 0] - c[0]) < 10.0) & (np.abs(Wsc[:, 1] - c[1]) < 10.0)]
                if col.size and (col[:, 2] > Wd[:, 2].max() + 2.0).any() and (col[:, 2] < Wd[:, 2].min() - 2.0).any():
                    disc_inside.append(VERSE_NAME.get(di - 100, str(di)))
            out["spineps_sacrum_top_S_mm"] = rnd(sc["s_max"], 1)
            out["spineps_sacrum_above_anchor_top_ml"] = rnd(ml_above, 1)
            out["discs_inside_spineps_sacrum"] = disc_inside
            out["swallowed_body_candidate"] = bool(ml_above >= 8.0 or disc_inside)
    out["flag"] = bool(isinstance(out["count"], int) and out["count"] != 5) or bool(out.get("complete_sacralisation_candidate")) \
        or bool(out.get("lumbarisation_candidate"))
    return out


# ---- rule 3: the lowest rib against the rib above -------------------------------------------------------------------
def _rib_voxels(moller: dict, spine: Spine, v: int, side: str):
    """World coordinates of the assigned rib voxels of vertebra v on one side (TPTBox rib id = v + 32; T13 -> 53)."""
    inst = moller.get("inst")
    if inst is None or v not in spine.inst:
        return None
    rid = 53 if v == 28 else v + 32
    reg = moller["inst_objs"].get(rid)
    if reg is None:
        return None
    W = world_of(np.argwhere(inst[reg] == rid) + offset_of(reg), spine.A)
    cx = spine.inst[v]["centroid"][0]
    sel = W[:, 0] > cx if side == "right" else W[:, 0] < cx      # RAS +x is the patient's right
    return W[sel] if sel.any() else None


def guard_g1_broken(moller: dict, spine: Spine, v: int, side: str) -> dict:
    """G1: an unassigned rib component (255) within 10 mm of the rib's far end -> BROKEN?. Measured on the mask,
    because the CSV's start/end points are crop-frame voxel indices and cannot be mapped to world."""
    W = _rib_voxels(moller, spine, v, side)
    inst = moller.get("inst")
    if W is None or inst is None:
        return dict(g1_broken=None, g1_min_mm=None)
    creg, corpus = spine.sub_crop(SEM["corpus_border"], v)
    if creg is None or not corpus.any():
        creg, corpus = spine.inst_crop(v)
    c = world_of(np.argwhere(corpus) + offset_of(creg), spine.A).mean(0)
    far = W[np.argmax(np.linalg.norm(W - c, axis=1))]
    ureg = moller["inst_objs"].get(255)
    if ureg is None:
        return dict(g1_broken=False, g1_min_mm=None, rib_far_end_mm=[rnd(x, 1) for x in far])
    U = world_of(np.argwhere(inst[ureg] == 255) + offset_of(ureg), spine.A)
    # 255 voxels on the same side only
    cx = spine.inst[v]["centroid"][0]
    U = U[(U[:, 0] > cx) if side == "right" else (U[:, 0] < cx)]
    if U.size == 0:
        return dict(g1_broken=False, g1_min_mm=None, rib_far_end_mm=[rnd(x, 1) for x in far])
    dmin = float(np.min(np.linalg.norm(U - far, axis=1)))
    return dict(g1_broken=bool(dmin <= G1_MM), g1_min_mm=rnd(dmin, 1), rib_far_end_mm=[rnd(x, 1) for x in far])


def guard_g2_costal(moller: dict, spine: Spine, v: int, side: str, length: float | None) -> dict:
    """G2: share of the rib's voxels within 2 mm of this vertebra's costal process (43/44). A short 'rib' hugging the
    process over most of its voxels is COSTAL-PROCESS? (journal App. B (D))."""
    from scipy import ndimage
    inst = moller.get("inst")
    if inst is None or v not in spine.inst:
        return dict(g2_costal_contact_frac=None, g2_costal_process=None)
    rid = 53 if v == 28 else v + 32
    cpreg, cpc = spine.sub_crop(SEM["cp_left"] if side == "left" else SEM["cp_right"], v)
    if cpreg is None or not cpc.any():
        return dict(g2_costal_contact_frac=None, g2_costal_process=None, g2_note="no costal process 43/44 for this vertebra")
    if moller["inst_objs"].get(rid) is None:
        return dict(g2_costal_contact_frac=None, g2_costal_process=None)
    cx = spine.inst[v]["centroid"][0]
    # the contact question lives within 30 voxels of the costal process: crop there, not to the whole rib
    reg = pad_slices(cpreg, spine.shape, 30)
    ribr = inst[reg] == rid
    idx = np.argwhere(ribr)
    W = world_of(idx + offset_of(reg), spine.A)
    sel = (W[:, 0] > cx) if side == "right" else (W[:, 0] < cx)
    if not sel.any():
        return dict(g2_costal_contact_frac=None, g2_costal_process=None)
    zo = [float(z) for z in np.abs(spine.A[:3, :3]).max(0)]      # per array axis mm
    cp = (spine.sem[reg] == (SEM["cp_left"] if side == "left" else SEM["cp_right"])) & (spine.vert[reg] == v)
    edt = ndimage.distance_transform_edt(~cp, sampling=zo)
    dist = edt[tuple(idx[sel].T)]
    # share of ALL the rib's voxels on this side (a voxel outside the 30-voxel crop is far from the process)
    Wall = _rib_voxels(moller, spine, v, side)
    n_side_all = len(Wall) if Wall is not None else int(sel.sum())
    frac = float((dist <= G2_MM).sum() / max(n_side_all, 1))
    return dict(g2_costal_contact_frac=rnd(frac, 3),
                g2_costal_process=bool(frac > G2_FRAC and (length is None or length <= G2_MAX_LEN)))


def rule3(spine: Spine, moller: dict, ribs: dict, field: dict, ts: dict | None, lowest_rb: int | None) -> dict:
    out = dict(rule="3", status=None, last_rib_level=None, reasons=[])
    if not moller.get("present"):
        out.update(status="no_measurement", reasons=[moller.get("missing") or moller.get("moller_skipped") or "no Moller rows"])
        return out
    measured = [v for v in ribs if v in spine.inst and any(l is not None for l in ribs[v]["lens"].values())]
    if not measured:
        out.update(status="no_measurement", reasons=["Moller measured no rib on a vertebra present in the SPINEPS mask"])
        return out
    by_s = sorted(measured, key=lambda v: spine.inst[v]["centroid"][2])       # caudal first
    last, above = by_s[0], (by_s[1] if len(by_s) > 1 else None)
    out["last_rib_level"] = dict(id=last, name=VERSE_NAME.get(last), veridah_name=VERSE_NAME.get(last))
    out["above_level"] = dict(id=above, name=VERSE_NAME.get(above)) if above else None
    out["g3_last_rib_is_count_level"] = bool(lowest_rb is None or lowest_rb == last or not ribs[last]["rib_bearing"])
    # G4: corpus label present for the level
    _, c49 = spine.sub_crop(SEM["corpus_border"], last)
    _, c50 = spine.sub_crop(SEM["corpus"], last)
    out["g4_corpus_present"] = bool((c49 is not None and c49.any()) or (c50 is not None and c50.any()))
    calls, ratios = {}, {}
    e = ribs[last]
    for side in ("left", "right"):
        r = e[side]
        c = dict(side=side, s1_call=None, call=None, rib_length=None, seg_at_border=None)
        if r is None:
            other = e["right" if side == "left" else "left"]
            # at the field edge laterally? (the vertebra's side within 60 mm of the field's lateral boundary)
            cx = spine.inst[last]["centroid"][0]
            edge = (field["x_max"] - cx < 60.0) if side == "right" else (cx - field["x_min"] < 60.0)
            if other is not None:
                c["call"] = "UNDECIDED" if edge else "ABSENT"
                c["s1_call"] = c["call"]
                c["reason"] = "no rib assigned on this side" + (" (lateral field edge)" if edge else "")
            else:
                c["call"] = None
            calls[side] = c
            continue
        L, border = r["rib_length"], r["seg_at_border"]
        c.update(rib_length=rnd(L, 1), seg_at_border=border, rib_volume=r["rib_volume"], n_path_points=r["n_path_points"],
                 upstream_sr=r["sr"], measure_error=r["measure_error"], pdrc=rnd(r["pdrc"], 2))
        if L is None or r["measure_error"]:
            c["s1_call"] = "UNDECIDED"
        elif L > RIB_MM:
            c["s1_call"] = "FULL"
        elif not border:
            c["s1_call"] = "STUMP"
        else:
            c["s1_call"] = "UNDECIDED"
        c.update(guard_g1_broken(moller, spine, last, side))
        c.update(guard_g2_costal(moller, spine, last, side, L))
        c["call"] = c["s1_call"]
        if c.get("g1_broken"):
            c["call"] = "BROKEN?"
        elif c.get("g2_costal_process"):
            c["call"] = "COSTAL-PROCESS?"
        # S3 ratio value: last / above on the same side, both untruncated (no cut yet)
        if above is not None:
            ra = ribs[above][side]
            if ra is not None and ra["rib_length"] and L and not border and not ra["seg_at_border"]:
                ratios[side] = rnd(L / ra["rib_length"], 4)
                c["above_rib_length"] = rnd(ra["rib_length"], 1)
            else:
                ratios[side] = None
                c["above_rib_length"] = rnd(ra["rib_length"], 1) if ra else None
                c["s3_reason"] = "no untruncated pair" if ra is not None else "no rib above on this side"
        calls[side] = c
    out["stump_left"], out["stump_right"] = calls["left"]["call"], calls["right"]["call"]
    out["sides"] = calls
    out["stump_bilateral"] = bool(out["stump_left"] == "STUMP" and out["stump_right"] == "STUMP")
    out["stump_any"] = bool("STUMP" in (out["stump_left"], out["stump_right"]))
    out["absent_any"] = bool("ABSENT" in (out["stump_left"], out["stump_right"]))
    out["s3_ratio_left"], out["s3_ratio_right"] = ratios.get("left"), ratios.get("right")
    out["s3_cut"] = None                    # pending calibration C6 (PREREG 3): the value is emitted, no call
    out["s3_call"] = None
    out["s1_x_s3_disagreement"] = None      # defined once s3_cut exists
    # the level above, reported too (a unilateral T12 stump under a normal T11 is the common form)
    if above is not None:
        ea = ribs[above]
        out["above"] = {s: (dict(rib_length=rnd(ea[s]["rib_length"], 1), seg_at_border=ea[s]["seg_at_border"],
                                 s1_call=("FULL" if ea[s]["rib_length"] and ea[s]["rib_length"] > RIB_MM else
                                          ("STUMP" if ea[s]["rib_length"] is not None and not ea[s]["seg_at_border"] else "UNDECIDED")))
                            if ea[s] else None) for s in ("left", "right")}
    # both conventions (PREREG 3 last bullet)
    stump_both = all(calls[s].get("s1_call") in ("STUMP", "ABSENT") for s in ("left", "right"))
    out["rbc_last_thoracic_level"] = VERSE_NAME.get(last)                       # Wigh: a < 38 mm rib keeps its vertebra thoracic
    out["rlbc_last_thoracic_level"] = VERSE_NAME.get(above) if (stump_both and above is not None) else VERSE_NAME.get(last)
    # G3 log: TotalSegmentator's own numbering at this level (logged, never overriding)
    if ts and "arr" in ts:
        arr, n2i, objs, cnt = ts["arr"], ts["name2id"], ts["objs"], ts["counts"]
        c = spine.inst[last]["centroid"]
        best, bd = None, None
        for nm, i in n2i.items():
            if not nm.startswith("vertebrae_") or i not in objs or cnt[i] < MIN_INST_VOX:
                continue
            reg = objs[i]
            cc = world_of(np.argwhere(arr[reg] == i) + offset_of(reg), spine.A).mean(0)
            d = float(np.linalg.norm(cc - c))
            if bd is None or d < bd:
                best, bd = nm.replace("vertebrae_", ""), d
        out["g3_ts_name_at_last_rib_level"] = best
        out["g3_ts_name_distance_mm"] = rnd(bd, 1)
        ribs_l = sorted(int(nm.split("_")[-1]) for nm, i in n2i.items() if nm.startswith("rib_left_") and cnt[i] >= MIN_INST_VOX)
        ribs_r = sorted(int(nm.split("_")[-1]) for nm, i in n2i.items() if nm.startswith("rib_right_") and cnt[i] >= MIN_INST_VOX)
        out["g3_ts_lowest_rib_number"] = dict(left=(ribs_l[-1] if ribs_l else None), right=(ribs_r[-1] if ribs_r else None))
    out["status"] = "ok"
    out["flag"] = bool(out["stump_any"] or out["absent_any"])
    return out


# ---- rule 2 features ----------------------------------------------------------------------------------------------
def _lr_extent_in_slab(reg, crop, A: np.ndarray, s_lo: float, s_hi: float, min_vox=100):
    """Left-right extent (0.5-99.5 pct) of the crop's voxels whose world S lies in [s_lo, s_hi]."""
    if reg is None or crop is None:
        return None, 0
    idx = np.argwhere(crop) + offset_of(reg)
    if idx.size == 0:
        return None, 0
    W = world_of(idx, A)
    sel = (W[:, 2] >= s_lo) & (W[:, 2] <= s_hi)
    if sel.sum() < min_vox:
        return None, int(sel.sum())
    return extent_pct(W[sel, 0]), int(sel.sum())


def fused_segments(anchor: dict, plane: dict, spine: Spine) -> dict:
    """Anterior-contour version of MORPH_API section 4 'number of fused segments': along the sacral midline
    (SPINEPS 73 inside the anchor sacrum where present, else the sacrum within 8 mm of its mid-line), the anterior
    extent per 2 mm S bin from the plate down to the apex; vestigial discs are anterior notches (local minima of
    prominence >= 1.5 mm). No HU is read (the CT is not opened), so this is the mask-contour variant only."""
    from scipy.signal import find_peaks
    m = anchor["mask"]
    reg, bc = spine.sub_crop(SEM["sac_body"])
    used = "spineps73_in_sacrum"
    body = (bc & m[reg]) if reg is not None else None
    if body is None or body.sum() < 500:
        reg = anchor["bbox"]
        body, used = m[reg], "sacrum_midline_slab"
    idx = np.argwhere(body) + offset_of(reg)
    W = world_of(idx, spine.A)
    xm = float(np.median(W[:, 0]))
    sel = np.abs(W[:, 0] - xm) <= 8.0
    W = W[sel]
    top = plane["anchor_S_mm"]
    bins = np.arange(top, W[:, 2].min() - 2.0, -2.0)
    prof, cent = [], []
    for b in bins:
        q = (W[:, 2] <= b) & (W[:, 2] > b - 2.0)
        if q.sum() < 5:
            prof.append(np.nan)
        else:
            prof.append(float(np.percentile(W[q, 1], 99)))       # anterior extent (RAS +y = anterior)
        cent.append(b - 1.0)
    prof = np.array(prof)
    ok = ~np.isnan(prof)
    if ok.sum() < 8:
        return dict(method=used, fused_segments_est=None, n_notches=None, note="profile too short")
    p = prof.copy()
    p[~ok] = np.interp(np.flatnonzero(~ok), np.flatnonzero(ok), prof[ok])
    k = np.ones(3) / 3.0
    ps = np.convolve(p, k, mode="same")
    # a vestigial disc is a SHORT anterior dip (1.5-10 mm within a 26 mm window); the plate edge (first 6 mm) and the
    # apex fall-off (last 12 mm) are not notches
    peaks, props = find_peaks(-ps, prominence=(1.5, 10.0), wlen=13)
    keep = [j for j, i in enumerate(peaks) if 6.0 <= (top - cent[i]) <= (top - cent[-1]) - 12.0]
    peaks = peaks[keep]
    props = {k2: np.asarray(v)[keep] for k2, v in props.items()}
    depth_mm = [rnd(top - cent[i], 1) for i in peaks]
    spacing = np.diff([top - cent[i] for i in peaks]) if len(peaks) > 1 else []
    return dict(method=used, n_notches=int(len(peaks)), fused_segments_est=int(len(peaks)) + 1,
                notch_depth_below_plate_mm=depth_mm, notch_prominence_mm=[rnd(x, 2) for x in props.get("prominences", [])],
                first_notch_below_plate_mm=(depth_mm[0] if depth_mm else None),
                median_notch_spacing_mm=(rnd(float(np.median(spacing)), 1) if len(spacing) else None),
                profile_length_mm=rnd(float(top - cent[-1]), 1))


def child_flag(row: dict, manifest_rec: dict | None) -> dict:
    age, src = None, None
    for k, v in row.items():
        if k and "age" in k.lower() and str(v).strip():
            try:
                age, src = float(str(v).strip()), f"tier:{k}"
                break
            except ValueError:
                continue
    if age is None and manifest_rec and manifest_rec.get("age") is not None:
        try:
            age, src = float(manifest_rec["age"]), "ctsp_manifest:age"
        except (TypeError, ValueError):
            pass
    notes = (row.get("notes") or "") + " " + (row.get("person_key") or "")
    ped = bool(re.search(r"age\s*<\s*18|pediatric|paediatric|child", notes, re.I))
    if age is not None:
        return dict(child=bool(age < 18.0), age_years=age, age_source=src, pediatric_note=ped)
    if ped:
        return dict(child=True, age_years=None, age_source="tier:notes", pediatric_note=True)
    return dict(child=None, age_years=None, age_source=None, pediatric_note=False)


def rule2(spine: Spine, anchors: dict, r1: dict, row: dict, manifest_rec: dict | None) -> dict:
    out = dict(rule="2", status=None, reasons=[], thresholds="none frozen: features only (PREREG 2)")
    out.update(child_flag(row, manifest_rec))
    # pelvis source: Dataset803 if present else TS hips + TS sacrum-union; CTSP GT kept as a comparator
    by_src = {}
    for s in ("dataset803", "ts_sacrum_union_s1", "ctsp_gt"):
        a = anchors.get(s)
        if not a or not a.get("present") or a.get("mask") is None:
            continue
        d = dict(sacrum_top_S_mm=rnd(a["top_S_mm"], 1), sacrum_ml=rnd(a["largest_ml"], 1),
                 sacral_S_extent_mm=rnd(a["top_S_mm"] - a["bottom_S_mm"], 1), n_components=a["n_components"],
                 mean_crest_top_S_mm=rnd(a.get("mean_crest_top_S_mm"), 1), hips_present=a.get("hips_present", 0))
        if a.get("mean_crest_top_S_mm") is not None:
            d["sacral_top_minus_crest_mm"] = rnd(a["top_S_mm"] - a["mean_crest_top_S_mm"], 1)
            for side in ("left", "right"):
                t = a.get(f"hip_{side}_crest_top_S_mm")
                d[f"sacral_top_minus_{side}_crest_mm"] = rnd(a["top_S_mm"] - t, 1) if t is not None else None
        else:
            d["sacral_top_minus_crest_mm"] = None
        by_src[s] = d
    out["by_source"] = by_src
    src = "dataset803" if "dataset803" in by_src else ("ts_sacrum_union_s1" if "ts_sacrum_union_s1" in by_src else None)
    out["pelvis_source"] = src
    out["pelvis_source_comparator"] = "ctsp_gt" if "ctsp_gt" in by_src else None
    if src:
        out["sacral_top_minus_crest_mm"] = by_src[src]["sacral_top_minus_crest_mm"]
        if by_src[src]["sacral_top_minus_crest_mm"] is None:
            out["reasons"].append(f"{src}: no hips (roi-subset TS has none; Dataset803 absent)")
    # the anchor used by rule 1 carries the plate-level features
    asrc = r1.get("anchor_source")
    a = anchors.get(asrc) if asrc else None
    if a is None or a.get("mask") is None or "anchor" not in r1:
        out["status"] = "partial" if by_src else "no_pelvis"
        out["reasons"].append("no anchor sacrum: plate-level features not computed")
        out["flag"] = None
        return out
    plane = r1["anchor"]
    top = plane["anchor_S_mm"]
    m = a["mask"]
    areg = union_slices([spine.sem_objs.get(SEM["ala_left"]), spine.sem_objs.get(SEM["ala_right"])], spine.shape)
    if areg is not None:
        sa = spine.sem[areg]
        alae = ((sa == SEM["ala_left"]) | (sa == SEM["ala_right"])) & m[areg]
    else:
        alae = None
    w, n = _lr_extent_in_slab(areg, alae, spine.A, top - 15.0, top + 5.0, min_vox=200)
    out["ala_to_ala_width_mm"], out["ala_vox_in_slab"] = rnd(w, 1), n
    preg, pc = spine.sub_crop(SEM["sac_plate"])
    plate = (pc & m[preg]) if preg is not None else None
    pw, pn = _lr_extent_in_slab(preg, plate, spine.A, -1e9, 1e9, min_vox=100)
    out["top_plate_width_mm"], out["plate74_vox"] = rnd(pw, 1), pn
    low = r1.get("lowest_free_body_nonfragment")     # a fragment's "inferior plate" is not a plate (CTSP 0005's 810-voxel L5)
    if low is not None:
        ereg, ep = spine.sub_crop(SEM["ep_inf"], low)
        ew, en = _lr_extent_in_slab(ereg, ep, spine.A, -1e9, 1e9, min_vox=100)
        if ew is None:            # no inferior end plate: the lowest 5 mm of the corpus
            creg, corp = spine.sub_crop(SEM["corpus_border"], low)
            if creg is not None and corp.any():
                s = s_of(np.argwhere(corp) + offset_of(creg), spine.A)
                ew, en = _lr_extent_in_slab(creg, corp, spine.A, float(s.min()), float(s.min()) + 5.0, min_vox=50)
                out["lowest_presacral_inferior_plate_method"] = "corpus49_lowest_5mm"
        else:
            out["lowest_presacral_inferior_plate_method"] = "spineps53"
        out["lowest_presacral_body"] = VERSE_NAME.get(low)
        out["lowest_presacral_inferior_plate_width_mm"] = rnd(ew, 1)
        out["top_plate_over_lowest_inferior_plate"] = rnd(pw / ew, 3) if (pw and ew) else None
    else:
        out["top_plate_over_lowest_inferior_plate"] = None
    try:
        out["fused_segments"] = fused_segments(a, plane, spine)
    except Exception as e:  # noqa: BLE001
        out["fused_segments"] = dict(error=repr(e)[:200])
    out["absorbed_disagreement_A_vs_B"] = r1.get("absorbed_disagreement_A_vs_B")
    out["status"] = "ok"
    out["flag"] = None          # no reference-half thresholds yet: this rule gates nothing (PREREG 2)
    return out


# ---- per-body morphology: F1-F3 (rule 1b) and the MDPA five (rule 4) -----------------------------------------------
def _pca_plane_angle_axial(W: np.ndarray) -> float | None:
    """Angle (deg) between the plane normal's axial projection and the left-right axis: 0 = sagittal joint (lumbar),
    90 = coronal joint (thoracic)."""
    if len(W) < 12:
        return None
    P = W - W.mean(0)
    _, _, vt = np.linalg.svd(P, full_matrices=False)
    n = vt[-1]
    nx, ny = abs(n[0]), abs(n[1])
    if nx + ny < 1e-6:
        return None
    return float(math.degrees(math.atan2(ny, nx)))


def body_features(spine: Spine, v: int, above: int | None) -> dict:
    """All per-side, in world axes on the SPINEPS grid. Never a feature: list position, level name, rib presence."""
    from scipy import ndimage
    d = spine.inst[v]
    out = dict(id=v, name=d["name"], vox=d["vox"], ml=rnd(d["ml"], 1))
    if d["vox"] < MORPH_MIN_VOX:
        out["note"] = "too small for morphology"
        return out
    reg = pad_slices(spine.objs[v], spine.shape, 4)
    off = offset_of(reg)
    inst = spine.vert[reg] == v
    sem = spine.sem[reg]
    A = spine.A
    zo = [float(z) for z in np.abs(A[:3, :3]).max(0)]

    def W_of(m):
        return world_of(np.argwhere(m) + off, A)

    Wi = W_of(inst)
    out["tp_span_mm"] = rnd(extent_pct(Wi[:, 0]), 1)
    # F3 via tools/tp_morphology.tp_metrics (axes from the affine)
    if _tp_metrics is not None and _tp_axes_of is not None:
        ax = _tp_axes_of(A)
        if len(ax) == 3:
            try:
                tp = _tp_metrics(inst, tuple(float(z) for z in zo), ax)
                out["tp"] = {k: tp[k] for k in tp if k != "body_half_mm"}
                out["tp_body_half_mm"] = tp.get("body_half_mm")
            except Exception as e:  # noqa: BLE001
                out["tp_error"] = repr(e)[:120]
    # corpus, end plates, canal
    corp = inst & ((sem == SEM["corpus_border"]) | (sem == SEM["corpus"]))
    if corp.sum() >= 200:
        Wc = W_of(corp)
        y = Wc[:, 1]
        ant = y >= np.percentile(y, 75)
        post = y <= np.percentile(y, 25)
        out["vbha_mm"] = rnd(extent_pct(Wc[ant, 2], 1, 99), 1)
        out["vbhp_mm"] = rnd(extent_pct(Wc[post, 2], 1, 99), 1)
        out["corpus_depth_mm"] = rnd(extent_pct(y), 1)
        out["corpus_centre"] = [rnd(x, 1) for x in Wc.mean(0)]
        sup = inst & (sem == SEM["ep_sup"])
        if sup.sum() >= 100:
            out["epw_mm"], out["epw_method"] = rnd(extent_pct(W_of(sup)[:, 0]), 1), "spineps52"
        else:
            top = Wc[:, 2] >= Wc[:, 2].max() - 5.0
            out["epw_mm"], out["epw_method"] = rnd(extent_pct(Wc[top, 0]), 1), "corpus_top_5mm"
        # canal: the hole the arch and body enclose in axial sections through the corpus centre (+-3 mm S)
        try:
            zc = Wc[:, 2].mean()
            si_axis = int(np.argmax(np.abs(A[2, :3])))
            filled = np.zeros_like(inst)
            for k in range(inst.shape[si_axis]):
                sl = [slice(None)] * 3
                sl[si_axis] = k
                sl = tuple(sl)
                if not inst[sl].any():
                    continue
                filled[sl] = ndimage.binary_fill_holes(inst[sl])
            hole = filled & ~inst
            if hole.any():
                Wh = W_of(hole)
                q = np.abs(Wh[:, 2] - zc) <= 3.0
                if q.sum() >= 30:
                    out["scw_mm"] = rnd(extent_pct(Wh[q, 0], 2, 98), 1)
                    out["scd_mm"] = rnd(extent_pct(Wh[q, 1], 2, 98), 1)
                    out["canal_method"] = "axial_fill_holes_of_instance"
        except Exception as e:  # noqa: BLE001
            out["canal_error"] = repr(e)[:120]
    # F1 / F2 per side
    for side, sap, iap, cp in (("left", SEM["sap_left"], SEM["iap_left"], SEM["cp_left"]),
                               ("right", SEM["sap_right"], SEM["iap_right"], SEM["cp_right"])):
        f = {}
        sm = inst & (sem == sap)
        cm = inst & (sem == cp)
        if cm.sum() >= 30 and sm.sum() >= 30:
            Wcp, Wsap = W_of(cm), W_of(sm)
            f["f2_cp_ap_offset_mm"] = rnd(Wcp[:, 1].mean() - Wsap[:, 1].mean(), 2)     # + = anterior
            f["f2_cp_top_minus_sap_top_mm"] = rnd(np.percentile(Wcp[:, 2], 99) - np.percentile(Wsap[:, 2], 99), 2)
            f["cp_length_mm"] = rnd(extent_pct(Wcp[:, 0]), 1)
        if above is not None and sm.sum() >= 30:
            # the joint: this body's superior articular process against the inferior articular process of the body above
            reg2 = union_slices([spine.objs.get(v), spine.objs.get(above)], spine.shape, pad=3)
            off2 = offset_of(reg2)
            sm2 = (spine.vert[reg2] == v) & (spine.sem[reg2] == sap)
            im2 = (spine.vert[reg2] == above) & (spine.sem[reg2] == iap)
            if im2.sum() >= 30 and sm2.sum() >= 30:
                edt = ndimage.distance_transform_edt(~im2, sampling=zo)
                contact = sm2 & (edt <= SFJ_CONTACT_MM)
                n = int(contact.sum())
                f["sfj_contact_vox"] = n
                if n >= 12:
                    Wj = world_of(np.argwhere(contact) + off2, A)
                    f["f1_sfj_angle_deg"] = rnd(_pca_plane_angle_axial(Wj), 1)
                    f["sfj_centre"] = [rnd(x, 1) for x in Wj.mean(0)]
                    if cm.sum() >= 30:
                        f["f2_cp_top_minus_sfj_centre_mm"] = rnd(np.percentile(W_of(cm)[:, 2], 99) - Wj[:, 2].mean(), 2)
        out[side] = f
    a = [out[s].get("f1_sfj_angle_deg") for s in ("left", "right")]
    a = [x for x in a if x is not None]
    out["f1_sfj_angle_mean_deg"] = rnd(float(np.mean(a)), 1) if a else None
    out["f1_sfj_tropism_deg"] = rnd(abs(a[0] - a[1]), 1) if len(a) == 2 else None
    o = [out[s].get("f2_cp_ap_offset_mm") for s in ("left", "right")]
    o = [x for x in o if x is not None]
    out["f2_cp_ap_offset_mean_mm"] = rnd(float(np.mean(o)), 2) if o else None
    return out


MDPA_BASE = ("epw_mm", "vbha_mm", "vbhp_mm", "scw_mm", "tp_span_mm")     # endplate_width, body_height, body_height_post,
#                                                                          canal_width, tp_span of the released atlas


def normalise_bodies(bodies: list[dict]) -> dict:
    """Each measure over the case's own median across its measured bodies (>= 3), plus the six ratios of
    test_morphometric_separability.py. Returns {id: {...}}."""
    med = {}
    for b in MDPA_BASE:
        v = [x[b] for x in bodies if x.get(b)]
        if len(v) >= 3:
            med[b] = float(np.median(v))
    spans = [x["tp_span_mm"] for x in bodies if x.get("tp_span_mm")]
    med_span = float(np.median(spans)) if len(spans) >= 3 else None
    out = {}
    for x in bodies:
        n = {"case_median": {k: rnd(v, 1) for k, v in med.items()}, "n_bodies_measured": len(bodies)}
        for b in MDPA_BASE:
            n[b + "/case_median"] = rnd(x[b] / med[b], 4) if (x.get(b) and b in med) else None
        ew, bh, bhp, cw, tp = (x.get("epw_mm"), x.get("vbha_mm"), x.get("vbhp_mm"), x.get("scw_mm"), x.get("tp_span_mm"))
        n["tp_span/endplate_width"] = rnd(tp / ew, 4) if (tp and ew) else None
        n["canal_width/endplate_width"] = rnd(cw / ew, 4) if (cw and ew) else None
        n["body_height/endplate_width"] = rnd(bh / ew, 4) if (bh and ew) else None
        n["anterior/posterior_height"] = rnd(bh / bhp, 4) if (bh and bhp) else None
        n["tp_span/body_height"] = rnd(tp / bh, 4) if (tp and bh) else None
        n["canal_width/body_height"] = rnd(cw / bh, 4) if (cw and bh) else None
        n["f3_span_over_case_median"] = rnd(tp / med_span, 4) if (tp and med_span) else None
        n["mdpa_complete"] = all(n.get(b + "/case_median") is not None for b in MDPA_BASE)
        out[x["id"]] = n
    return out


def rules_1b_4(spine: Spine, r1: dict, bodies: list[dict], norm: dict) -> tuple[dict, dict]:
    applies = r1.get("count") == 6
    tgt = r1.get("most_cranial_free_body") if applies else None
    r1b = dict(rule="1b", applies=applies, target_body=None, decision=None, p_thoracic=None,
               classifier="not frozen (PREREG 1b: logistic model on F1-F3 trained on named T12/L1, pending)")
    r4 = dict(rule="4", applies=applies, target_body=None, decision=None, score=None, operating_threshold=None,
              classifier="not frozen (PREREG 4: MDPA model never applied to a SPINEPS body; canal terms unverified)")
    if not applies or tgt is None:
        return r1b, r4
    order = spine.vertebrae_by_S()
    pos = order.index(tgt)
    above = order[pos - 1] if pos > 0 else None
    bt = next((b for b in bodies if b["id"] == tgt), None)
    ba = next((b for b in bodies if b["id"] == above), None) if above else None
    r1b.update(target_body=VERSE_NAME.get(tgt), target_veridah_name=VERSE_NAME.get(tgt),
               features={k: bt.get(k) for k in ("f1_sfj_angle_mean_deg", "f1_sfj_tropism_deg", "f2_cp_ap_offset_mean_mm",
                                                "left", "right", "tp", "tp_span_mm")} if bt else None,
               f3_span_over_case_median=norm.get(tgt, {}).get("f3_span_over_case_median"),
               body_above=VERSE_NAME.get(above) if above else None,
               features_above={k: ba.get(k) for k in ("f1_sfj_angle_mean_deg", "f2_cp_ap_offset_mean_mm", "tp_span_mm")} if ba else None,
               probe_ranges="thoracic SFJ 72-83 deg, upper lumbar 21-47 deg (MORPH_API 6.3, n=3, unrendered)")
    r4.update(target_body=VERSE_NAME.get(tgt), measures={b: (bt.get(b) if bt else None) for b in MDPA_BASE},
              normalised=norm.get(tgt), body_above=VERSE_NAME.get(above) if above else None,
              normalised_above=norm.get(above) if above else None)
    return r1b, r4


# ---- comparators: the prior calls, carried, never used --------------------------------------------------------------
@lru_cache(maxsize=8)
def _csv_index(path: str, key: str, delimiter: str = ",") -> dict:
    out = {}
    if not path or not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=delimiter):
            k = (r.get(key) or "").strip()
            if k and k not in out:
                out[k] = r
    return out


@lru_cache(maxsize=1)
def _manifest_index(path: str) -> dict:
    if not path or not os.path.exists(path):
        return {}
    m = json.loads(Path(path).read_text())
    recs = m.get("records", m) if isinstance(m, dict) else m
    return {str(r.get("volume_id")).zfill(4): r for r in recs if isinstance(r, dict)}


def comparators(row: dict, cfg: dict, inputs: Inputs) -> dict:
    coll, cid, pk = row["collection"], row["case_id"], row.get("person_key") or ""
    out = {}
    reg = _csv_index(cfg["registry"], "patient_key")
    if reg:
        inputs.add("registry_csv", cfg["registry"])
        r = reg.get(pk)
        out["registry"] = {k: r.get(k) for k in ("subtype", "call", "truth_tier", "castellvi", "four_lumbar", "lumbar_rib",
                                                  "labeller_a", "labeller_b", "agree", "n_thoracic_rib_bearing", "n_lumbar",
                                                  "fused_mask_representation", "disagreement")} if r else None
    ah = Path(cfg["ah_root"]) / coll
    rows_csv = ah / "rows.csv"
    if rows_csv.exists():
        inputs.add("ah_rows_csv", rows_csv)
        r = _csv_index(str(rows_csv), "case").get(cid)
        out["ah_rows"] = {k: r.get(k) for k in ("subtype", "castellvi", "four_lumbar", "lumbar_rib", "truth_tier", "labeller_a",
                                                 "labeller_b", "agree", "n_thoracic_rib_bearing", "n_lumbar",
                                                 "junction_tl_in_fov", "junction_ls_in_fov")} if r else None
    for sub in ("labeller_b", "calls"):
        p = ah / sub / f"{cid}.json"
        if p.exists():
            inputs.add(f"ah_{sub}_json", p)
            try:
                j = json.loads(p.read_text())
            except Exception as e:  # noqa: BLE001
                out[f"ah_{sub}"] = {"error": repr(e)[:120]}
                continue
            if sub == "calls":
                out["ah_calls"] = {"A": {k: (j.get("A") or {}).get(k) for k in ("ls_call", "tl_call", "status")},
                                   "B": {k: (j.get("B") or {}).get(k) for k in ("ls_call", "tl_call", "n_lumbar", "subtype", "status")},
                                   "subtype": j.get("subtype"), "call": j.get("call")}
            else:
                out["ah_labeller_b"] = {k: j.get(k) for k in ("version", "subtype", "n_lumbar", "ls_call", "tl_call", "sacrum_ml",
                                                              "n_discs", "n_discs_inside_sacrum", "problems") if k in j}
    if coll == "ctsp":
        lf = _csv_index(cfg["lstv_flags"], "volume_id")
        if lf:
            inputs.add("lstv_flags_csv", cfg["lstv_flags"])
            r = lf.get(cid)
            out["lstv_flags_v2"] = {k: r.get(k) for k in ("LSTV_flag", "TLTV_flag", "lstv_label", "lstv_class", "castellvi_type",
                                                         "has_L6", "n_lumbar_labelled", "n_rib_bearing", "has_lumbar_rib",
                                                         "has_T13_vertebra", "age", "sex")} if r else None
        cs = _csv_index(cfg["consensus"], "volume_id")
        if cs:
            inputs.add("castellvi_consensus_csv", cfg["consensus"])
            r = cs.get(cid)
            out["castellvi_consensus"] = {k: r.get(k) for k in ("read_1_NA", "read_2_MI", "agreement", "consensus", "comment")} if r else None
        man = _manifest_index(cfg["ctsp_manifest"])
        if man:
            inputs.add("ctsp_manifest_json", cfg["ctsp_manifest"])
            r = man.get(cid)
            out["ctsp_manifest"] = {k: r.get(k) for k in ("lstv_label", "lstv_class", "castellvi_type", "castellvi_agreement",
                                                          "has_l6", "n_lumbar_labels", "has_lumbar_rib", "lumbar_rib_side",
                                                          "prov_pelvis", "prov_spine", "age", "sex")} if r else None
            out["_manifest_rec"] = r
    if coll == "verse":
        m = re.match(r"verse:(\d+)$", pk)
        vs = _csv_index(cfg["verse_suppl"], "verse_id")
        if m and vs:
            inputs.add("verse_suppl_table1_csv", cfg["verse_suppl"])
            r = vs.get(str(int(m.group(1))))
            out["verse_suppl_table1"] = {k: r.get(k) for k in ("thoracolumbar_enumeration", "thoracolumbar_stump_ribs",
                                                              "thoracolumbar_transition_vertebra", "lumbosacral_enumeration",
                                                              "castellvi_grading", "assumed_segment_structure", "age_years")} if r else None
    return out


# ---- the case driver ----------------------------------------------------------------------------------------------
def score_case(row: dict, cfg: dict) -> dict:
    t0 = time.time()
    row = dict(row)
    row["case_id"] = cid_norm(row.get("collection", ""), row.get("case_id", ""))
    inputs = Inputs()
    inputs.add("prereg", PREREG_PATH)
    res = dict(status="ok", errors=[], case=dict(collection=row.get("collection"), case_id=row["case_id"],
                                                 person_key=row.get("person_key"), tier=row.get("tier"),
                                                 ct_path=row.get("ct_path"), real_frames=row.get("real_frames"),
                                                 registry_flags=row.get("registry_flags"), notes=row.get("notes")))
    note = {}
    try:
        spine = load_spine(row, inputs)
        res["spineps"] = dict(spine.ids_info, sem_regridded=spine.sem_regridded,
                              instances={d["name"]: dict(vox=d["vox"], ml=rnd(d["ml"], 1), fragment=d["fragment"],
                                                         S_mm=rnd(d["centroid"][2], 1)) for d in spine.inst.values()},
                              median_vertebra_vox=int(spine.median_vertebra_vox))
        field = field_extent(row, spine, inputs)
        res["field"] = field
        anchors = {}
        a = anchor_ctsp_gt(row, spine, field, inputs, note)
        if a is not None:
            anchors["ctsp_gt"] = a
        a = anchor_dataset803(row, spine, field, inputs, note, cfg["pelvis_root"])
        if a is not None:
            anchors["dataset803"] = a
        ts = load_ts(row, spine, inputs, note, cfg["ts_root"])
        a = anchor_ts(ts, spine, field)
        if a is not None:
            anchors["ts_sacrum_union_s1"] = a
        res["anchors"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("mask", "bbox")} for k, v in anchors.items()}
        res["regridded"] = note.get("regridded_to_spineps_grid", [])
        moller = load_moller(row, spine, inputs, note, cfg["moller_root"])
        ribs = rib_summary(moller)
        res["moller"] = dict(present=moller["present"], variant=moller["variant"], variants_present=moller.get("variants_present"),
                             missing=moller.get("missing"), ok=moller.get("moller_ok"), skipped=moller.get("moller_skipped"),
                             assigned_levels={VERSE_NAME.get(k, str(k)): v for k, v in (moller.get("levels") or {}).items()},
                             unassigned_rib_vox=moller.get("unassigned_rib_vox"),
                             per_vertebra={e["name"]: dict(lens={s: rnd(l, 1) for s, l in e["lens"].items()}, rib_bearing=e["rib_bearing"],
                                                           at_border={s: (e[s]["seg_at_border"] if e[s] else None) for s in ("left", "right")})
                                           for e in ribs.values()})
        r1 = rule1(spine, anchors, moller, ribs, field)
        res["rule1"] = r1
        lowest_rb = (r1.get("lowest_rib_bearing") or {}).get("id")
        res["rule3"] = rule3(spine, moller, ribs, field, ts, lowest_rb)
        comp = comparators(row, cfg, inputs)
        man = comp.pop("_manifest_rec", None)
        res["rule2"] = rule2(spine, anchors, r1, row, man)
        # per-body morphology for every vertebra instance (the case median needs them all)
        order = spine.vertebrae_by_S()
        bodies = []
        for k, v in enumerate(order):
            above = order[k - 1] if k > 0 else None
            try:
                bodies.append(body_features(spine, v, above))
            except Exception as e:  # noqa: BLE001
                bodies.append(dict(id=v, name=VERSE_NAME.get(v), error=repr(e)[:200]))
        norm = normalise_bodies([b for b in bodies if "error" not in b and b.get("vox", 0) >= MORPH_MIN_VOX])
        res["bodies"] = bodies
        res["bodies_normalised"] = {VERSE_NAME.get(k, str(k)): v for k, v in norm.items()}
        res["rule1b"], res["rule4"] = rules_1b_4(spine, r1, bodies, norm)
        res["comparators"] = comp
        # section 5: the partial flag (rules 2 and 4 have no thresholds yet)
        raised = []
        if r1.get("flag"):
            raised.append("rule1")
        if res["rule3"].get("flag"):
            raised.append("rule3")
        res["flag"] = dict(flag=bool(raised), rules=raised, rule2_flag=None, rule4_flag=None,
                           adjudication=(r1.get("count_status") == "no_anchor"),
                           note="rule 2 and rule 4 gate nothing until the reference-half freeze / classifier freeze")
    except RulesError as e:
        res["status"] = "failed"
        res["errors"].append(str(e))
    except Exception as e:  # noqa: BLE001
        res["status"] = "failed"
        res["errors"].append(repr(e)[:500])
        res["trace"] = traceback.format_exc()[-2500:]
    res["meta"] = dict(tool=TOOL, tool_version=TOOL_VERSION, prereg_path=str(PREREG_PATH), prereg_sha256=prereg_sha256(),
                       prereg_status=PREREG_STATUS, git_sha=git_sha(), utc_time=utc_now(), host=socket.gethostname(),
                       python=sys.version.split()[0], seconds=rnd(time.time() - t0, 1), confirmer=cfg.get("confirmer"),
                       inputs_sha256=inputs.files)
    return jsonable(res)


# ---- the flat row ---------------------------------------------------------------------------------------------------
def _g(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return default if d is None else d


def flatten(res: dict) -> dict:
    m, c, r1, r2, r3, r1b, r4 = (res.get(k, {}) for k in ("meta", "case", "rule1", "rule2", "rule3", "rule1b", "rule4"))
    cp = res.get("comparators", {})
    j = lambda x: json.dumps(x, separators=(",", ":")) if x not in (None, "", [], {}) else ""   # noqa: E731
    row = {
        "collection": c.get("collection"), "case_id": c.get("case_id"), "person_key": c.get("person_key"), "tier": c.get("tier"),
        "status": res.get("status"), "errors": j(res.get("errors")),
        "ids_verdict": _g(res, "spineps", "ids_verdict"), "ids_guard_raised": _g(res, "spineps", "ids_guard_raised"),
        "field_source": _g(res, "field", "field_source"),
        "anchor_source": r1.get("anchor_source"), "anchor_definition": _g(r1, "anchor", "anchor_definition"),
        "anchor_S_mm": rnd(_g(r1, "anchor", "anchor_S_mm"), 1),
        "sacrum_in_field_gt": _g(res, "anchors", "ctsp_gt", "in_field"), "sacrum_in_field_803": _g(res, "anchors", "dataset803", "in_field"),
        "sacrum_in_field_ts": _g(res, "anchors", "ts_sacrum_union_s1", "in_field"),
        "sacrum_ml_anchor": rnd(_g(res, "anchors", r1.get("anchor_source") or "", "largest_ml"), 1),
        "r1_count": r1.get("count"), "r1_count_status": r1.get("count_status"), "r1_count_rbc": r1.get("count_rbc_convention"),
        "r1_count_excluding_fragments": r1.get("count_excluding_fragments"),
        "r1_count_by_source": j(r1.get("count_by_source")), "r1_anchor_S_by_source": j(r1.get("anchor_S_by_source")),
        "r1_lowest_rib_bearing": _g(r1, "lowest_rib_bearing", "name"), "r1_tl_gate": r1.get("tl_gate"),
        "r1_most_cranial_free_body": VERSE_NAME.get(r1.get("most_cranial_free_body")) if r1.get("most_cranial_free_body") else None,
        "r1_lowest_free_body": VERSE_NAME.get(r1.get("lowest_free_body")) if r1.get("lowest_free_body") else None,
        "r1_bodies_f": j([[b["name"], b["f"], b["cls"]] for b in r1.get("bodies", [])]),
        "r1_absorbed": j(r1.get("absorbed")), "r1_contact": j(r1.get("contact")),
        "r1_castellvi_II_IV_candidate": r1.get("castellvi_II_IV_candidate"),
        "r1_complete_sacralisation_candidate": r1.get("complete_sacralisation_candidate"),
        "r1_lumbarisation_candidate": r1.get("lumbarisation_candidate"),
        "r1_absorbed_disagreement_A_vs_B": r1.get("absorbed_disagreement_A_vs_B"),
        "r1_anchor_diff_803_vs_ts_mm": r1.get("anchor_diff_803_vs_ts_mm"),
        "r1_anchor_diff_gt_vs_ts_mm": r1.get("anchor_diff_gt_vs_ts_mm"),
        "r1_swallowed_body_candidate": r1.get("swallowed_body_candidate"),
        "r1_spineps_sacrum_above_anchor_top_ml": r1.get("spineps_sacrum_above_anchor_top_ml"),
        "r1_reasons": j(r1.get("reasons")), "r1_flag": r1.get("flag"),
        "r3_status": r3.get("status"), "r3_last_rib_level": _g(r3, "last_rib_level", "name"), "r3_above_level": _g(r3, "above_level", "name"),
        "r3_stump_left": r3.get("stump_left"), "r3_stump_right": r3.get("stump_right"), "r3_stump_bilateral": r3.get("stump_bilateral"),
        "r3_len_left_mm": _g(r3, "sides", "left", "rib_length"), "r3_len_right_mm": _g(r3, "sides", "right", "rib_length"),
        "r3_border_left": _g(r3, "sides", "left", "seg_at_border"), "r3_border_right": _g(r3, "sides", "right", "seg_at_border"),
        "r3_g1_broken_left": _g(r3, "sides", "left", "g1_broken"), "r3_g1_broken_right": _g(r3, "sides", "right", "g1_broken"),
        "r3_g2_costal_left": _g(r3, "sides", "left", "g2_costal_contact_frac"), "r3_g2_costal_right": _g(r3, "sides", "right", "g2_costal_contact_frac"),
        "r3_g3_ts_name_at_last_rib": r3.get("g3_ts_name_at_last_rib_level"), "r3_g4_corpus_present": r3.get("g4_corpus_present"),
        "r3_s3_ratio_left": r3.get("s3_ratio_left"), "r3_s3_ratio_right": r3.get("s3_ratio_right"), "r3_s3_cut": r3.get("s3_cut"),
        "r3_rbc_last_thoracic": r3.get("rbc_last_thoracic_level"), "r3_rlbc_last_thoracic": r3.get("rlbc_last_thoracic_level"),
        "r3_flag": r3.get("flag"),
        "r2_status": r2.get("status"), "r2_pelvis_source": r2.get("pelvis_source"), "r2_child": r2.get("child"), "r2_age_years": r2.get("age_years"),
        "r2_sacral_top_minus_crest_mm": r2.get("sacral_top_minus_crest_mm"),
        "r2_sacral_top_minus_crest_gt_mm": _g(r2, "by_source", "ctsp_gt", "sacral_top_minus_crest_mm"),
        "r2_ala_to_ala_width_mm": r2.get("ala_to_ala_width_mm"), "r2_top_plate_width_mm": r2.get("top_plate_width_mm"),
        "r2_lowest_inferior_plate_width_mm": r2.get("lowest_presacral_inferior_plate_width_mm"),
        "r2_top_plate_over_lowest_inferior_plate": r2.get("top_plate_over_lowest_inferior_plate"),
        "r2_fused_segments_est": _g(r2, "fused_segments", "fused_segments_est"), "r2_first_notch_below_plate_mm": _g(r2, "fused_segments", "first_notch_below_plate_mm"),
        "r2_flag": r2.get("flag"),
        "r1b_applies": r1b.get("applies"), "r1b_target": r1b.get("target_body"), "r1b_decision": r1b.get("decision"),
        "r1b_f1_sfj_mean_deg": _g(r1b, "features", "f1_sfj_angle_mean_deg"), "r1b_f1_tropism_deg": _g(r1b, "features", "f1_sfj_tropism_deg"),
        "r1b_f2_cp_ap_offset_mm": _g(r1b, "features", "f2_cp_ap_offset_mean_mm"), "r1b_f3_span_over_median": r1b.get("f3_span_over_case_median"),
        "r1b_f1_above_deg": _g(r1b, "features_above", "f1_sfj_angle_mean_deg"),
        "r4_applies": r4.get("applies"), "r4_decision": r4.get("decision"), "r4_normalised": j(r4.get("normalised")),
        "flag": _g(res, "flag", "flag"), "flag_rules": j(_g(res, "flag", "rules")), "adjudication": _g(res, "flag", "adjudication"),
        "cmp_registry_subtype": _g(cp, "registry", "subtype"), "cmp_registry_truth_tier": _g(cp, "registry", "truth_tier"),
        "cmp_registry_n_lumbar": _g(cp, "registry", "n_lumbar"), "cmp_registry_castellvi": _g(cp, "registry", "castellvi"),
        "cmp_ah_subtype": _g(cp, "ah_rows", "subtype"), "cmp_ah_n_lumbar": _g(cp, "ah_rows", "n_lumbar"),
        "cmp_ah_calls_A_ls": _g(cp, "ah_calls", "A", "ls_call"), "cmp_ah_calls_B_ls": _g(cp, "ah_calls", "B", "ls_call"),
        "cmp_lstv_flag": _g(cp, "lstv_flags_v2", "LSTV_flag"), "cmp_tltv_flag": _g(cp, "lstv_flags_v2", "TLTV_flag"),
        "cmp_castellvi_consensus": _g(cp, "castellvi_consensus", "consensus"), "cmp_manifest_lstv_label": _g(cp, "ctsp_manifest", "lstv_label"),
        "cmp_manifest_has_l6": _g(cp, "ctsp_manifest", "has_l6"), "cmp_gt_lumbar_ids": j(_g(res, "anchors", "ctsp_gt", "gt_lumbar_ids")),
        "cmp_verse_suppl_ls": _g(cp, "verse_suppl_table1", "lumbosacral_enumeration"),
        "moller_variant": _g(res, "moller", "variant"), "regridded": j(res.get("regridded")),
        "tool": m.get("tool"), "tool_version": m.get("tool_version"), "prereg_sha256": m.get("prereg_sha256"), "prereg_status": m.get("prereg_status"),
        "git_sha": m.get("git_sha"), "utc_time": m.get("utc_time"), "host": m.get("host"), "seconds": m.get("seconds"),
        "inputs_sha256": j({k: v["sha256"] for k, v in (m.get("inputs_sha256") or {}).items()}),
    }
    return {k: ("" if v is None else v) for k, v in row.items()}


COLUMNS = list(flatten({"meta": {}, "case": {}}).keys())


def write_case(res: dict, out_root: Path) -> tuple[Path, Path]:
    coll, cid = res["case"]["collection"], res["case"]["case_id"]
    d = out_root / coll
    d.mkdir(parents=True, exist_ok=True)
    jp, tp = d / f"{cid}.rules.json", d / f"{cid}.row.tsv"
    tmp = jp.with_name(jp.name + f".{os.getpid()}.part")
    tmp.write_text(json.dumps(res, indent=1))
    os.replace(tmp, jp)
    row = flatten(res)
    tmp = tp.with_name(tp.name + f".{os.getpid()}.part")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerow(row)
    os.replace(tmp, tp)
    if res.get("status") != "ok":
        fd = out_root / "_failed"
        fd.mkdir(exist_ok=True)
        (fd / f"{coll}__{safe(cid)}.json").write_text(json.dumps({"collection": coll, "case_id": cid, "errors": res.get("errors"),
                                                                  "trace": res.get("trace"), "utc_time": res["meta"]["utc_time"]}, indent=1))
    return jp, tp


# ---- claims (ts_arm_run.py's pattern: atomic mkdir, owner file, heartbeat, stale takeover) --------------------------
class Heartbeat(threading.Thread):
    def __init__(self, path: Path, every_s: float = 300.0):
        super().__init__(daemon=True)
        self.path, self.every_s, self.stop = path, every_s, threading.Event()

    def run(self):
        while not self.stop.wait(self.every_s):
            try:
                os.utime(self.path, None)
            except OSError:
                pass


def claim(claims: Path, key: str, stale_h: float, tag: str, retry_failed: bool = False) -> bool:
    d = claims / key
    try:
        d.mkdir()
        (d / "owner").write_text(tag)
        return True
    except FileExistsError:
        pass
    try:
        age_h = (time.time() - d.stat().st_mtime) / 3600.0
    except FileNotFoundError:
        return False
    failed = (d / "failed").exists()
    if failed and not retry_failed:
        return False
    if not failed and age_h < stale_h:
        return False
    try:  # take over a stale claim: only one renamer wins
        os.rename(d, claims / f"{key}.stale.{tag.replace(' ', '_')}.{int(time.time())}")
        d.mkdir()
        (d / "owner").write_text(tag + " (took over stale claim)")
        return True
    except OSError:
        return False


def read_list(path: str) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def cfg_from_args(a) -> dict:
    cfg = dict(DEFAULTS)
    for k in DEFAULTS:
        v = getattr(a, k, None)
        if v:
            cfg[k] = v
    return cfg


def cmd_case(a) -> int:
    rows = read_list(a.list)
    want = [r for r in rows if cid_norm(r["collection"], r["case_id"]) == cid_norm(r["collection"], a.case_id)
            and (not a.collection or r["collection"] == a.collection)]
    if not want:
        print(f"case {a.case_id!r} not in {a.list}", file=sys.stderr)
        return 2
    cfg = cfg_from_args(a)
    out_root = Path(a.out)
    rc = 0
    for r in want:
        res = score_case(r, cfg)
        jp, tp = write_case(res, out_root)
        print(json.dumps(flatten(res), indent=1))
        print(f"wrote {jp}\nwrote {tp}")
        rc |= int(res["status"] != "ok")
    return rc


def cmd_run(a) -> int:
    rows = read_list(a.list)
    cfg = cfg_from_args(a)
    root = Path(a.out)
    claims, fdir = root / "_claims", root / "_failed"
    for d in (root, claims, fdir):
        d.mkdir(parents=True, exist_ok=True)
    job = os.environ.get("SLURM_ARRAY_JOB_ID") or os.environ.get("SLURM_JOB_ID") or "local"
    task = os.environ.get("SLURM_ARRAY_TASK_ID", "0")
    tag = f"{job}_{task} {socket.gethostname()}"
    if a.reverse:
        rows = rows[::-1]
    print(f"RULES task {tag} list={Path(a.list).name} rows={len(rows)} out={root} prereg={prereg_sha256()[:12]} git={git_sha()[:8]}",
          flush=True)
    t_start = time.time()
    n_done = n_skip = n_fail = n_busy = 0
    for r in rows:
        if a.limit and n_done + n_fail >= a.limit:
            break
        if a.max_hours and (time.time() - t_start) / 3600.0 > a.max_hours:
            print("max-hours reached; not claiming more", flush=True)
            break
        cid = cid_norm(r["collection"], r["case_id"])
        key = f"{r['collection']}__{safe(cid)}"
        out = root / r["collection"] / f"{cid}.rules.json"
        if out.exists() and not a.force:
            n_skip += 1
            continue
        if a.claim and not claim(claims, key, a.stale_h, tag, a.retry_failed):
            n_busy += 1
            continue
        if out.exists() and not a.force:
            n_skip += 1
            continue
        hb = Heartbeat(claims / key) if a.claim else None
        if hb:
            hb.start()
        t0 = time.time()
        try:
            res = score_case(r, cfg)
            write_case(res, root)
            ok = res["status"] == "ok"
        except Exception as e:  # noqa: BLE001  (score_case catches; this is the writer)
            ok = False
            (fdir / f"{key}.json").write_text(json.dumps({"key": key, "error": repr(e)[:500], "trace": traceback.format_exc()[-1500:]}))
            res = {"rule1": {}, "rule3": {}}
        if hb:
            hb.stop.set()
        if ok:
            n_done += 1
        else:
            n_fail += 1
            if a.claim:
                try:
                    (claims / key / "failed").write_text("failed")
                except OSError:
                    pass
        print(f"{key} ok={ok} {time.time() - t0:.1f}s count={res.get('rule1', {}).get('count')} "
              f"anchor={res.get('rule1', {}).get('anchor_source')} stump={res.get('rule3', {}).get('stump_left')}/"
              f"{res.get('rule3', {}).get('stump_right')} {('; '.join(res.get('errors', [])))[:160]}", flush=True)
    print(f"RULES_END {tag}: done {n_done}, skipped(have) {n_skip}, held by others {n_busy}, failed {n_fail}, "
          f"{(time.time() - t_start) / 3600:.2f} h", flush=True)
    return 0


def cmd_collect(a) -> int:
    root = Path(a.out)
    rows = []
    for p in sorted(root.glob("*/*.row.tsv")):
        with open(p, encoding="utf-8", newline="") as fh:
            rows += list(csv.DictReader(fh, delimiter="\t"))
    cols = list(COLUMNS)
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    cen = root / "census.tsv"
    with open(cen, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    # per-collection summary
    summ = {}
    by = {}
    for r in rows:
        by.setdefault(r["collection"], []).append(r)
    by["ALL"] = rows
    for coll, rr in by.items():
        n = len(rr)
        ok = [r for r in rr if r["status"] == "ok"]
        counts = {}
        for r in ok:
            counts[r["r1_count"] or "none"] = counts.get(r["r1_count"] or "none", 0) + 1
        status = {}
        for r in ok:
            status[r["r1_count_status"] or "none"] = status.get(r["r1_count_status"] or "none", 0) + 1
        anc = {}
        for r in ok:
            anc[r["anchor_source"] or "none"] = anc.get(r["anchor_source"] or "none", 0) + 1
        counted = [r for r in ok if r["r1_count"] in ("4", "5", "6")]
        nc = len(counted)
        six = sum(r["r1_count"] == "6" for r in counted)
        four = sum(r["r1_count"] == "4" for r in counted)
        stump = [r for r in ok if r["r3_status"] == "ok"]
        stump_any = sum(("STUMP" in (r["r3_stump_left"], r["r3_stump_right"])) for r in stump)
        agree = [r for r in counted if r["cmp_registry_n_lumbar"] not in ("", None)]
        agree_n = sum(str(r["r1_count"]) == str(r["cmp_registry_n_lumbar"]) for r in agree)
        d = dict(n=n, n_ok=len(ok), n_failed=n - len(ok), r1_count=counts, r1_count_status=status, anchor_source=anc,
                 n_counted=nc, six_count_share_pct=rnd(100.0 * six / nc, 2) if nc else None,
                 four_count_share_pct=rnd(100.0 * four / nc, 2) if nc else None,
                 n_rule3=len(stump), stump_subject_share_pct=rnd(100.0 * stump_any / len(stump), 2) if stump else None,
                 flagged_share_pct=rnd(100.0 * sum(r["flag"] == "True" for r in ok) / len(ok), 2) if ok else None,
                 adjudication_n=sum(r["adjudication"] == "True" for r in ok),
                 registry_n_lumbar_agreement=f"{agree_n}/{len(agree)}" if agree else None,
                 prevalence_windows_pct=PREVALENCE_WINDOWS,
                 six_in_window=(PREVALENCE_WINDOWS["six_count_share_pct"][0] <= 100.0 * six / nc <= PREVALENCE_WINDOWS["six_count_share_pct"][1]) if nc >= 50 else None,
                 stump_in_window=(PREVALENCE_WINDOWS["stump_subject_share_pct"][0] <= 100.0 * stump_any / len(stump) <= PREVALENCE_WINDOWS["stump_subject_share_pct"][1]) if len(stump) >= 50 else None,
                 prereg_sha256=sorted({r["prereg_sha256"] for r in rr}), git_sha=sorted({r["git_sha"] for r in rr}))
        summ[coll] = d
    (root / "census_summary.json").write_text(json.dumps(summ, indent=1))
    with open(root / "census_summary.tsv", "w", newline="", encoding="utf-8") as fh:
        keys = ["collection", "n", "n_ok", "n_failed", "n_counted", "six_count_share_pct", "four_count_share_pct", "n_rule3",
                "stump_subject_share_pct", "flagged_share_pct", "adjudication_n", "registry_n_lumbar_agreement", "r1_count",
                "r1_count_status", "anchor_source", "six_in_window", "stump_in_window"]
        w = csv.writer(fh, delimiter="\t")
        w.writerow(keys)
        for coll, d in summ.items():
            w.writerow([coll] + [json.dumps(d[k]) if isinstance(d[k], (dict, list)) else d[k] for k in keys[1:]])
    print(f"census: {len(rows)} rows -> {cen}; summary -> {root / 'census_summary.tsv'}")
    for coll, d in summ.items():
        print(f"  {coll}: n={d['n']} ok={d['n_ok']} failed={d['n_failed']} counts={d['r1_count']} anchors={d['anchor_source']} "
              f"six%={d['six_count_share_pct']} stump%={d['stump_subject_share_pct']} registry_agree={d['registry_n_lumbar_agreement']}")
    return 0


def output_schema() -> dict:
    return {
        "per_ct_json": "<out>/<coll>/<case>.rules.json: {status, errors, case{collection,case_id,person_key,tier,ct_path}, "
                       "spineps{ids_verdict,ids_guard_raised,instances}, field{field_source,S_min,S_max,...}, "
                       "anchors{ctsp_gt|dataset803|ts_sacrum_union_s1: {present,largest_ml,top_S_mm,touches_caudal_slice,in_field,"
                       "hip_*_crest_top_S_mm,mean_crest_top_S_mm,scheme,refused}}, moller{variant,assigned_levels,per_vertebra}, "
                       "rule1{count (4|5|6|no_count), count_status, anchor_source, anchor{anchor_S_mm,anchor_definition}, "
                       "lowest_rib_bearing, bodies[{name,f,cls,counted,fragment,lumbarisation_candidate}], absorbed, contact, "
                       "castellvi_II_IV_candidate, complete_sacralisation_candidate, lumbarisation_candidate, "
                       "absorbed_disagreement_A_vs_B, count_by_source, count_rbc_convention, swallowed_body_candidate, reasons, flag}, "
                       "rule3{last_rib_level, stump_left|right in {STUMP,FULL,UNDECIDED,BROKEN?,COSTAL-PROCESS?,ABSENT,null}, "
                       "sides{...g1,g2}, stump_bilateral, s3_ratio_left|right, s3_cut=null, above, rbc/rlbc, g3_ts_*, g4_corpus_present, flag}, "
                       "rule2{child, age_years, pelvis_source, sacral_top_minus_crest_mm, ala_to_ala_width_mm, top_plate_width_mm, "
                       "lowest_presacral_inferior_plate_width_mm, top_plate_over_lowest_inferior_plate, fused_segments{...}, by_source, flag=null}, "
                       "bodies[per-instance F1-F3 + MDPA measures], bodies_normalised{...}, rule1b{applies,target_body,features,decision=null}, "
                       "rule4{applies,target_body,measures,normalised,decision=null}, comparators{registry,ah_rows,ah_calls,lstv_flags_v2,"
                       "castellvi_consensus,ctsp_manifest,verse_suppl_table1}, flag{flag,rules,adjudication}, "
                       "meta{tool,tool_version,prereg_sha256,prereg_status,git_sha,utc_time,host,inputs_sha256{role:{path,sha256,bytes}}}}",
        "per_ct_row_tsv_and_census_tsv_columns": COLUMNS,
        "census_summary": "census_summary.tsv/json: per collection n, n_ok, n_failed, r1_count distribution, count_status, anchor_source, "
                          "six/four-count share %, stump subject share %, flagged share %, adjudication n, registry n_lumbar agreement, "
                          "prevalence windows (PREREG 5) and whether the share falls inside",
    }


# ---- self-test ------------------------------------------------------------------------------------------------------
SAMPLE_PREFIX_MAP = [   # grid path prefix -> sample sub-directory (the sample tree mirrors the grid layout)
    ("/rs/rs_grp_oschome/go2432/data/anomaly_harvest", "anomaly_harvest"),
    ("/rs/rs_grp_oschome/go2432/data/spineps/ctsp", "data/spineps/ctsp"),
    ("/wsu/home/go/go24/go2432/bench/totalsegmentator", "bench/totalsegmentator"),
    ("/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K/labels", "data/CTSpinoPelvic1K/labels"),
]
SAMPLE_CT_STUBS = {     # the CT header stubs (zeros with the CT's exact header; no intensity is ever read)
    "/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K/ct/0001_ct.nii.gz": "ct_header_stubs/ctsp_0001.nii.gz",
    "/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K/ct/0005_ct.nii.gz": "ct_header_stubs/ctsp_0005.nii.gz",
    "/rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini/raw/BDMAP_00000016/ct.nii.gz": "ct_header_stubs/aa3_BDMAP_00000016.nii.gz",
}


def _remap(path: str, samples: Path) -> str:
    if not path:
        return path
    if path in SAMPLE_CT_STUBS:
        return str(samples / SAMPLE_CT_STUBS[path])
    for pre, sub in SAMPLE_PREFIX_MAP:
        if path.startswith(pre):
            return str(samples / sub / path[len(pre):].lstrip("/"))
    return path


def selftest(samples: Path, out: Path) -> int:
    """Scores CTSP 0005 (read L6; VERIDAH calls its L1 'T13'), CTSP 0001 (ordinary five) and abdomenatlas
    aa3_BDMAP_00000016 (Moller output, TS multilabel with hips) from the sample tree and checks the pre-registered
    behaviour. Exit 1 on any mismatch."""
    fails: list[str] = []

    def check(cond, msg):
        print(("  ok   " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    tier = samples / "ruleclass/tiers/tier_sample.tsv"
    if not tier.exists():
        print(f"selftest: sample tier list missing: {tier}")
        return 1
    rows = read_list(str(tier))
    for r in rows:
        for k in ("ct_path", "spineps_vert", "spineps_spine", "spineps_ctd", "ts_output", "ts_class_map", "gt_label"):
            r[k] = _remap(r.get(k, ""), samples)
    cfg = dict(DEFAULTS)
    cfg.update(moller_root=str(samples / "ruleclass/arms/moller_fast"), ts_root=str(samples / "ruleclass/arms/ts"),
               pelvis_root=str(samples / "ruleclass/arms/pelvis"), ah_root=str(samples / "anomaly_harvest"),
               lstv_flags=str(samples / "lstv_flag/lstv_flag_labels_v2.csv"),
               verse_suppl=str(samples / "lstv_flag/sources/verse_suppl_table1.csv"),
               ctsp_manifest=str(samples / "data/CTSpinoPelvic1K/manifest.json"))
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for r in rows:
        t0 = time.time()
        res = score_case(r, cfg)
        jp, tp = write_case(res, out)
        results[(r["collection"], cid_norm(r["collection"], r["case_id"]))] = res
        print(f"\n== {r['collection']} {r['case_id']} ({time.time() - t0:.1f}s) status={res['status']} {res.get('errors')}")
        print(json.dumps(flatten(res), indent=1))

    # -- the pre-registered expectations
    k5, k1, ka = ("ctsp", "0005"), ("ctsp", "0001"), ("abdomenatlas3_mini", "aa3_BDMAP_00000016")
    for k in (k5, k1, ka):
        check(k in results and results[k]["status"] == "ok", f"{k}: scored ok")
    r5, r1_, ra = (results.get(k, {}) for k in (k5, k1, ka))
    check(r5.get("rule1", {}).get("count") == 6, "0005: rule-1 count is 6")
    check(r5.get("rule1", {}).get("anchor_source") == "ctsp_gt", "0005: anchor is the CTSP GT sacrum")
    check(r5.get("rule1", {}).get("count_by_source", {}).get("ctsp_gt") == 6, "0005: count under the GT anchor is 6")
    check((r5.get("rule1", {}).get("lowest_rib_bearing") or {}).get("name") == "T12",
          "0005: lowest rib-bearing vertebra is VERIDAH's T12 (ribs 162/168 mm)")
    check(r5.get("rule1", {}).get("most_cranial_free_body") == 28, "0005: most cranial rib-free body is VERIDAH's 'T13' (id 28)")
    check(r5.get("rule1b", {}).get("applies") is True and r5.get("rule1b", {}).get("decision") is None,
          "0005: rule 1b applies (six) and its decision is null")
    check(r5.get("rule4", {}).get("applies") is True and r5.get("rule4", {}).get("decision") is None,
          "0005: rule 4 applies (six) and its decision is null")
    f1 = (r5.get("rule1b", {}).get("features") or {}).get("f1_sfj_angle_mean_deg")
    check(f1 is not None, f"0005: F1 SFJ angle computed on the sixth body ({f1} deg; probe said ~30)")
    check(r5.get("rule3", {}).get("stump_left") == "FULL" and r5.get("rule3", {}).get("stump_right") == "FULL",
          "0005: rule 3 both sides FULL at T12")
    check(r5.get("rule3", {}).get("s3_cut") is None, "0005: S3 cut is null (pending calibration)")
    check(any(b["fragment"] for b in r5.get("rule1", {}).get("bodies", [])), "0005: the 810-voxel 'L5' is flagged as a fragment")
    check(r5.get("rule1", {}).get("swallowed_body_candidate") is True, "0005: SPINEPS sacrum above the GT anchor -> swallowed-body candidate")
    check(r1_.get("rule1", {}).get("count") == 5, "0001: rule-1 count is 5")
    check(r1_.get("rule1", {}).get("anchor_source") == "ctsp_gt", "0001: anchor is the CTSP GT sacrum")
    check(r1_.get("rule1", {}).get("flag") is False and r1_.get("flag", {}).get("flag") is False, "0001: not flagged")
    check(r1_.get("rule1b", {}).get("applies") is False, "0001: rule 1b does not apply")
    ra1 = ra.get("rule1", {})
    check(ra1.get("anchor_source") == "ts_sacrum_union_s1" or ra1.get("count") == "no_count",
          f"aa16: anchor is TS sacrum union S1 (no GT, no Dataset803) or no_count with a reason: {ra1.get('anchor_source')} / {ra1.get('reasons')}")
    check(ra1.get("count") in (5, "no_count"), f"aa16: count is 5 or no_count ({ra1.get('count')}, {ra1.get('count_status')})")
    check(ra.get("rule2", {}).get("pelvis_source") == "ts_sacrum_union_s1" and
          ra.get("rule2", {}).get("sacral_top_minus_crest_mm") is not None,
          "aa16: rule-2 sacral top vs crest from the arm A TS multilabel (hips present)")
    check(ra.get("comparators", {}).get("ah_rows") is not None, "aa16: AH rows.csv comparator joined")
    # -- the bookkeeping every row must carry
    for k, res in results.items():
        m = res["meta"]
        check(re.fullmatch(r"[0-9a-f]{64}", m["prereg_sha256"] or "") is not None, f"{k}: prereg_sha256 present")
        check(m["prereg_status"] == "draft", f"{k}: prereg_status draft")
        check(bool(m["git_sha"]) and m["git_sha"] != "unknown", f"{k}: git sha {m['git_sha'][:8]}")
        check(m["tool"] == TOOL and m["tool_version"] == TOOL_VERSION, f"{k}: tool name/version")
        check(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", m["utc_time"]) is not None, f"{k}: UTC time")
        roles = set(m["inputs_sha256"])
        need = {"prereg", "spineps_vert", "spineps_spine", "spineps_ctd", "moller_csv", "moller_rib_inst", "ct_header"}
        check(need <= roles, f"{k}: sha256 of every input read ({len(roles)} files; missing {sorted(need - roles)})")
        check(all(re.fullmatch(r"[0-9a-f]{64}", v["sha256"]) for v in m["inputs_sha256"].values()), f"{k}: input hashes well formed")
        check(res["case"]["case_id"] == (res["case"]["case_id"].zfill(4) if res["case"]["collection"] == "ctsp" else res["case"]["case_id"]),
              f"{k}: case id form")
        row = flatten(res)
        check(list(row.keys()) == COLUMNS, f"{k}: flat row has the census columns")
    check("ctsp_gt" in r1_.get("anchors", {}) and r1_["anchors"]["ctsp_gt"].get("scheme") == "v10",
          "0001: GT resolved through labels_for to scheme v10 (never a fixed map)")
    # -- collect
    rc = cmd_collect(argparse.Namespace(out=str(out)))
    cen = out / "census.tsv"
    n = len(read_list(str(cen))) if cen.exists() else 0
    check(rc == 0 and n == 3, f"collect: census.tsv has 3 rows ({n})")
    check((out / "census_summary.tsv").exists() and (out / "census_summary.json").exists(), "collect: summary written")
    # -- the claim protocol (mkdir, busy, stale takeover, failed marker)
    cl = out / "_claims_test"
    cl.mkdir(exist_ok=True)
    check(claim(cl, "k1", 2.0, "a") is True, "claim: first taker wins")
    check(claim(cl, "k1", 2.0, "b") is False, "claim: second taker refused while fresh")
    old = time.time() - 3 * 3600
    os.utime(cl / "k1", (old, old))
    check(claim(cl, "k1", 2.0, "b") is True, "claim: a 3 h old claim is taken over at stale 2 h")
    (cl / "k1" / "failed").write_text("x")
    check(claim(cl, "k1", 2.0, "c") is False and claim(cl, "k1", 2.0, "c", retry_failed=True) is True,
          "claim: a failed claim is retaken only with retry_failed")
    # -- a failure is written as a failure
    bad = dict(rows[0])
    bad["spineps_vert"] = str(samples / "does_not_exist.nii.gz")
    bad["case_id"] = "9999"
    res = score_case(bad, cfg)
    write_case(res, out)
    check(res["status"] == "failed" and res["errors"] and (out / "_failed" / "ctsp__9999.json").exists(),
          "a missing input is reported as status=failed with the reason, never as a count")
    print(f"\nSELFTEST {'PASSED' if not fails else 'FAILED'}: {len(fails)} mismatch(es)")
    for f in fails:
        print("   - " + f)
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--samples", default=os.environ.get("TR_SAMPLES", ""), help="sample tree for --selftest")
    ap.add_argument("--selftest-out", default="", help="where --selftest writes (default <samples>/_selftest_out)")
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--out", required=True)
        for k, v in DEFAULTS.items():
            p.add_argument(f"--{k.replace('_', '-')}", default="", help=f"default {v}")

    p = sub.add_parser("case", help="score one case from a tier list")
    p.add_argument("--list", required=True)
    p.add_argument("--case-id", required=True)
    p.add_argument("--collection", default="")
    common(p)
    p = sub.add_parser("run", help="walk a tier list (array worker)")
    p.add_argument("--list", required=True)
    p.add_argument("--claim", action="store_true", help="atomic-mkdir claims under <out>/_claims (several workers)")
    p.add_argument("--stale-h", type=float, default=2.0)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--max-hours", type=float, default=0.0)
    p.add_argument("--reverse", action="store_true")
    p.add_argument("--force", action="store_true", help="rescore cases that already have a rules.json")
    p.add_argument("--retry-failed", action="store_true")
    common(p)
    p = sub.add_parser("collect", help="merge the per-case rows into census.tsv + summary")
    p.add_argument("--out", required=True)
    p = sub.add_parser("schema", help="print the output schema")
    a = ap.parse_args()
    if a.selftest:
        if not a.samples:
            ap.error("--selftest needs --samples <dir> (or TR_SAMPLES)")
        s = Path(a.samples)
        return selftest(s, Path(a.selftest_out) if a.selftest_out else s / "_selftest_out")
    if a.cmd == "case":
        return cmd_case(a)
    if a.cmd == "run":
        return cmd_run(a)
    if a.cmd == "collect":
        return cmd_collect(a)
    if a.cmd == "schema":
        print(json.dumps(output_schema(), indent=1))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
