#!/usr/bin/env python
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/build_review_tree.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""build_review_tree.py -- lay out the transitional-vertebra review tree from the rules census.

PURPOSE
    PREREG_rules.md section 7 asks for a per-case review (stage 1 screen, stage 2 blinded confirm) of every CT the
    four rules flag. This script turns one row of the rules census into one self-contained case directory that a
    reviewer can open in ITK-SNAP or 3D Slicer: the CT, every mask that exists for it, a label descriptor per mask
    scheme, the paired radiographs with their camera geometry where they exist, the rule evidence, and a README
    that says what the case is, why it was flagged, which rules could not run, and what to look at. Nothing here
    scores a rule; the census is read verbatim and re-emitted. The sibling `review_app/` serves the tree.

INPUTS
    --census <tsv>       the rules census (tools/anomaly_rules.py output). Expected columns: case_key, collection,
                         case_id, count, anchor_source, flags (`;` list), stump_left, stump_right, s3_ratio,
                         rule2_* features, prior_subtype, registry_subtype, truth_tier, ct, spineps_inst,
                         spineps_sem, spineps_ctd, spineps_ids, ts, ts_class_map, moller_inst, pelvis, gt, has_xr,
                         xr_paths. Missing columns are tolerated (the row says what was absent). The tier lists
                         (`ruleclass/tiers/tier1.tsv`) are accepted as-is through column aliases (ct_path,
                         spineps_vert, spineps_spine, ts_output, gt_label, real_frames, ...).
    docs/ruleclass/PREREG_rules.md   hashed into every row (prereg_sha256, prereg_status draft|frozen).
    Optional joins, all hidden from the reviewer (evidence.json -> "hidden"; manifest columns registry_*, prior_*,
    truth_*): --registry registry.csv (person rows), --ah-root <anomaly_harvest> (labeller_b/<case>.json,
    calls/<case>.json, rows.csv), --consensus castellvi_consensus.csv, --lumbosac Lumbosac.csv,
    --ctsp-manifest manifest.json. Optional stores for paths the census does not carry: --moller-root,
    --pelvis-root, --ts-root, --carmlspine-root, --cobra-root.

OUTPUTS   (root default /rs/rs_grp_oschome/go2432/review_tree/<YYYY-MM-DD>/)
    <TYPE>/<case_dir>/           TYPE in {T13, L6, four_lumbar_or_fused_L5, lumbarised_S1, castellvi_II_IV,
                                 lumbar_rib, stump_rib, unresolved}; a case with several flags sits under its
                                 primary TYPE (TYPES order = priority) with `.also_in` listing the others; the
                                 other TYPE dirs carry an ALSO_IN.tsv pointer, never a second copy of the CT.
        ct.nii.gz                symlink (default) or copy (--copy) of the census CT; NEVER rewritten or reoriented
        masks/{spineps_inst,spineps_sem,ts_total,moller_ribs,pelvis803,gt_v11}.nii.gz   where they exist, verbatim
        masks/ts_roi/            the per-structure TotalSegmentator directory when that is all there is
        labels/<mask>.txt        ITK-SNAP descriptor whose id set is exactly np.unique(mask); <mask>.ctbl for Slicer
        xr/                      radiographs (xr_<view>.dcm), each as a single-slice NIfTI in the camera frame,
                                 xr_<view>[_refN]_cam_from_world.tfm (ITK, LPS world->camera), xr_<view>[_refN]_P.txt
                                 (OpenCV-convention 3x4 world->pixel), *_pose.json, POSE_STATUS.txt; COBRA sweeps
                                 (projections.mha + geometry.xml) are linked as they are
        previews/                pose overlay PNGs when they exist
        evidence.json            header (tool, version, prereg sha, git sha, UTC), the census row verbatim, every
                                 input with its sha256, mask id sets and checks, xr geometry, failures, and the
                                 hidden block (registry row, prior calls, reads) for the audit only
        README.md, make_slicer_scene.py (run INSIDE Slicer's Python; saves case.mrb), open_commands.json
    manifest.tsv, types.tsv, index.html (self-contained, sortable), SIZES.md, FAILURES.tsv, PREREG_rules.md (copy),
    runs.jsonl (append-only run log; the only file a re-run is allowed to change), <TYPE>.zip + .sha256 (--zip).

HOUSE RULES HONOURED HERE
    No volume is ever rewritten or reoriented (the only NIfTIs written are the derived radiograph slices). CTSP and
    Dataset803 masks are resolved through ostk.labels.labels_for and must come back v10 with the pelvis present
    (id 29 must be absent); SPINEPS, TS and Moller masks never go through it. SPINEPS instance masks pass
    tools/spineps_ids.check_ids; raw 1..N ids are refused (or relabelled through the ctd with --relabel-raw), never
    linked as names. CTSP case ids are zfill(4). A cut field (count == no_count) is `unresolved`, never ordinary.
    Failures are written as failures (evidence.json, FAILURES.tsv, exit code 2), never skipped silently.

RUN
    python tools/transitional_review/build_review_tree.py --census <rules_census.tsv> \
        --root /rs/rs_grp_oschome/go2432/review_tree/2026-09-27 [--copy] [--zip] \
        --registry SchwingNet/results/transitional_registry/registry.csv \
        --ah-root /rs/rs_grp_oschome/go2432/data/anomaly_harvest \
        --moller-root /rs/rs_grp_oschome/go2432/ruleclass/arms/moller_fast \
        --carmlspine-root /rs/rs_grp_oschome/go2432/data/carmlspine --cobra-root /rs/rs_grp_oschome/go2432/data/cobra2026/cases
    On the grid this reads every mask, so it is an sbatch job, not a login-node command:
        sbatch -D <logdir> -p reqp --qos=requeue --mem=16G --wrap "~/mambaforge/envs/spineps/bin/python <this> ..."
    python tools/transitional_review/build_review_tree.py --verify --root <tree>      # re-check a built tree
    python tools/transitional_review/build_review_tree.py --selftest [--keep]          # 4 synthetic cases, twice
    python tools/transitional_review/build_review_tree.py --selftest --samples <dir>   # + the real sample files
    Exit 0 clean, 2 when any case carries a failure (the tree is still complete), 1 on a fatal error.

The self-test builds four fake cases from small synthetic NIfTIs (an L6 with three flags and a paired radiograph,
a four-count with raw SPINEPS ids and a legacy-id pelvis that must both be refused, a no_count COBRA-style case,
and a T13 whose CT is missing), builds the tree twice, and checks: every path in manifest.tsv exists; every
descriptor's id set equals np.unique of its mask; the CT affine equals the source affine; the CTSP and pelvis
masks resolved v10 through labels_for; the radiograph slice re-projects to (col+0.5, row+0.5) through K [R|t];
the .tfm reads back through SimpleITK; the second run changed no file except runs.jsonl; the zips verify against
their sha256 manifests; no README contains the word "registry". Any mismatch exits non-zero.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import gzip
import hashlib
import html
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np

TOOL_NAME = "transitional_review.build_review_tree"
TOOL_VERSION = "1"
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
DEFAULT_PREREG = REPO / "docs" / "ruleclass" / "PREREG_rules.md"
RS = "/rs/rs_grp_oschome/go2432"
DET_MM_CARM = 307.2            # iRay Jupi1212X, 2048 x 150 um (tools/carmlspine_io.DET_MM); PREREG section 6
RUN_LOG = "runs.jsonl"          # the one root file a re-run may change

# ----------------------------------------------------------------------------------------------------- types
# Order = priority. A case carrying several types is housed under the first one present.
TYPES = ("T13", "L6", "four_lumbar_or_fused_L5", "lumbarised_S1", "castellvi_II_IV", "lumbar_rib", "stump_rib",
         "unresolved")
TYPE_MEANING = {
    "T13": "a thirteenth rib-bearing vertebra; decidable only when the whole cage is in the field (PREREG 3, 5)",
    "L6": "six free bodies between the lowest full rib and the sacrum: a true L6, or a T12 that lost its rib (rule 1, 1b)",
    "four_lumbar_or_fused_L5": "four free bodies, or a body more than half inside the sacrum label: a fused L5, or a "
                               "lumbar rib on L1 that took the count (rule 1 absorbed, rule 2)",
    "lumbarised_S1": "a free body lying wholly below the sacral anchor: a mobile S1 (rule 1 lumbarisation_candidate)",
    "castellvi_II_IV": "a body in contact with the sacrum, 0.10 <= f < 0.50: partial sacralisation candidate (rule 1)",
    "lumbar_rib": "a short rib on the first lumbar-shaped body (rule 3 with rule 1b)",
    "stump_rib": "the lowest rib is 38 mm or shorter along its path and not cut by the field edge, under a full rib "
                 "above; or a rib-less thoracic-shaped sixth body (rule 3, rule 4)",
    "unresolved": "the count could not be made (no_count / no_anchor), or the flags name no subtype; a cut field is "
                  "never ordinary",
}
# flag text (lower-cased) -> type. Order matters only for readability; every match is kept, priority is TYPES.
FLAG_RULES = (
    (r"t13|thirteen", "T13"),
    (r"(^|[^a-z0-9])l6([^a-z0-9]|$)|six|count_?6|ls_l6", "L6"),
    (r"four|count_?4|fused|sacralis|sacraliz|absorbed", "four_lumbar_or_fused_L5"),
    (r"lumbaris|lumbariz|mobile_s1|below_anchor", "lumbarised_S1"),
    (r"castellvi|contact", "castellvi_II_IV"),
    (r"lumbar_rib", "lumbar_rib"),
    (r"stump|aplastic|absent_rib|tl_?11|sixth_body_thoracic|rib_?less", "stump_rib"),
    (r"no_count|no_anchor|unresolved|review|disagree|untestable", "unresolved"),
)
TYPE_RULE = {"T13": "rule1", "L6": "rule1", "four_lumbar_or_fused_L5": "rule1", "lumbarised_S1": "rule1",
             "castellvi_II_IV": "rule1", "lumbar_rib": "rule3", "stump_rib": "rule3", "unresolved": "rule1"}
LOOK_AT = {
    "T13": ["Count rib-bearing vertebrae from T1 downward. If T1 (or the C7/T1 step) is not in the field, write that "
            "down: the case stays a candidate with its prior, it cannot be called T13 from this CT.",
            "Is the lowest rib a full rib or a stump? A stump on a thoracic-shaped body under eleven full pairs is the "
            "hypoplastic-twelfth alternative."],
    "L6": ["Start at the lowest rib that is clearly a rib (longer than 38 mm along its path, not a costal process). "
           "Count free bodies down to the first body whose lateral mass is fused to the ala or lies inside the sacrum.",
           "Six free bodies: look at the top one. Coronal (transverse) superior facet joint and a transverse process "
           "that sits behind the superior articular process = thoracic (a rib-less T12, ordinary lumbar count). "
           "Sagittal joint and a process in front of it = lumbar (a true L6).",
           "Check the lumbosacral segment for a transitional articulation (Castellvi) on either side."],
    "four_lumbar_or_fused_L5": ["Four free bodies: is the lowest body absorbed into the sacrum (a vestigial disc band "
                                "under the top plate; a top plate as narrow as a lumbar inferior plate; alae rising to "
                                "its transverse processes)?",
                                "Or does the first lumbar-shaped body carry a short rib that took the count (lumbar "
                                "rib on L1)? Look at the top free body's ribs and facet joint."],
    "lumbarised_S1": ["A free body below the sacral anchor: is there a mobile disc between it and the rest of the "
                      "sacrum? Are the alae attached to it or to the segment below? Count the sacral segments."],
    "castellvi_II_IV": ["Transverse process against the ala on each side: a gap (I), a pseudarthrosis with a joint "
                        "line (II), bony fusion (III), one of each (IV). Record the side.",
                        "Then re-count the free bodies above it: the same case may be an L6 or a four-count."],
    "lumbar_rib": ["A short rib articulating with a lumbar-shaped body (sagittal facet joint, process in front of the "
                   "superior articular process) is a lumbar rib; the same rib on a thoracic-shaped body is a T12 stump."],
    "stump_rib": ["On each side find the lowest rib. 38 mm or shorter along its path and not cut by the field edge = "
                  "stump; compare it with the rib above. A separate rib fragment near the measured end is a fracture "
                  "or a split segmentation, not a stump.",
                  "A rib-less thoracic-shaped body above five lumbar-type bodies is the aplastic-rib reading; note "
                  "its facet joint orientation."],
    "unresolved": ["Decide first whether the junction the count needs is in the field at all (sacrum with its top "
                   "plate; the lowest rib-bearing vertebra with a whole rib). If it is, name what blocked the count "
                   "(a merged instance, a missing sacrum label, a misnamed level)."],
}

# ----------------------------------------------------------------------------------------------------- label schemes
VERSE_NAMES = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
               20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6", 26: "sacrum", 27: "coccyx", 28: "T13"}
# TPTBox Location values as SPINEPS writes them into *_seg-spine_msk.nii.gz (printed from the grid spineps env).
SPINEPS_SEM_NAMES = {
    40: "Vertebra_Full", 41: "Arcus_Vertebrae", 42: "Spinosus_Process", 43: "Costal_Process_Left",
    44: "Costal_Process_Right", 45: "Superior_Articular_Left", 46: "Superior_Articular_Right",
    47: "Inferior_Articular_Left", 48: "Inferior_Articular_Right", 49: "Vertebra_Corpus_border",
    50: "Vertebra_Corpus", 51: "Dens_axis", 52: "Vertebral_Body_Endplate_Superior",
    53: "Vertebral_Body_Endplate_Inferior", 58: "Vertebra_Disc_Superior", 59: "Vertebra_Disc_Inferior",
    60: "Spinal_Cord", 61: "Spinal_Canal", 62: "Endplate", 63: "Rib_Left", 64: "Rib_Right",
    70: "Sacrum_Sacral_Ala_Left", 71: "Sacrum_Sacral_Ala_Right", 72: "Sacrum_Posterior_Sacral_Elements",
    73: "Sacrum_Body", 74: "Sacrum_Endplate", 80: "Metal", 100: "Vertebra_Disc",
}
# TotalSegmentator `total` class map (2.x; identical in the 2.4.0 bench store, the 2.18.0 arm and the
# anomaly_harvest ts_total store, checked 2026-09-27). The census row's ts_class_map file wins when present.
TS_DEFAULT_CLASS_MAP = {
    1: "spleen", 2: "kidney_right", 3: "kidney_left", 4: "gallbladder", 5: "liver", 6: "stomach", 7: "pancreas",
    8: "adrenal_gland_right", 9: "adrenal_gland_left", 10: "lung_upper_lobe_left", 11: "lung_lower_lobe_left",
    12: "lung_upper_lobe_right", 13: "lung_middle_lobe_right", 14: "lung_lower_lobe_right", 15: "esophagus",
    16: "trachea", 17: "thyroid_gland", 18: "small_bowel", 19: "duodenum", 20: "colon", 21: "urinary_bladder",
    22: "prostate", 23: "kidney_cyst_left", 24: "kidney_cyst_right", 25: "sacrum", 26: "vertebrae_S1",
    27: "vertebrae_L5", 28: "vertebrae_L4", 29: "vertebrae_L3", 30: "vertebrae_L2", 31: "vertebrae_L1",
    32: "vertebrae_T12", 33: "vertebrae_T11", 34: "vertebrae_T10", 35: "vertebrae_T9", 36: "vertebrae_T8",
    37: "vertebrae_T7", 38: "vertebrae_T6", 39: "vertebrae_T5", 40: "vertebrae_T4", 41: "vertebrae_T3",
    42: "vertebrae_T2", 43: "vertebrae_T1", 44: "vertebrae_C7", 45: "vertebrae_C6", 46: "vertebrae_C5",
    47: "vertebrae_C4", 48: "vertebrae_C3", 49: "vertebrae_C2", 50: "vertebrae_C1", 51: "heart", 52: "aorta",
    53: "pulmonary_vein", 54: "brachiocephalic_trunk", 55: "subclavian_artery_right", 56: "subclavian_artery_left",
    57: "common_carotid_artery_right", 58: "common_carotid_artery_left", 59: "brachiocephalic_vein_left",
    60: "brachiocephalic_vein_right", 61: "atrial_appendage_left", 62: "superior_vena_cava",
    63: "inferior_vena_cava", 64: "portal_vein_and_splenic_vein", 65: "iliac_artery_left", 66: "iliac_artery_right",
    67: "iliac_vena_left", 68: "iliac_vena_right", 69: "humerus_left", 70: "humerus_right", 71: "scapula_left",
    72: "scapula_right", 73: "clavicula_left", 74: "clavicula_right", 75: "femur_left", 76: "femur_right",
    77: "hip_left", 78: "hip_right", 79: "spinal_cord", 80: "gluteus_maximus_left", 81: "gluteus_maximus_right",
    82: "gluteus_medius_left", 83: "gluteus_medius_right", 84: "gluteus_minimus_left", 85: "gluteus_minimus_right",
    86: "autochthon_left", 87: "autochthon_right", 88: "iliopsoas_left", 89: "iliopsoas_right", 90: "brain",
    91: "skull", **{91 + n: f"rib_left_{n}" for n in range(1, 13)}, **{103 + n: f"rib_right_{n}" for n in range(1, 13)},
    116: "sternum", 117: "costal_cartilages",
}
MOLLER_UNASSIGNED = 255
MOLLER_RIB_OFFSET = 32          # rib id = vertebra id + 32 (arm B fast); the mask also carries the SPINEPS instances

MASK_SPECS = (   # (mask name in masks/, census column, scheme)
    ("spineps_inst", "spineps_inst", "verse"),
    ("spineps_sem", "spineps_sem", "spineps_sem"),
    ("ts_total", "ts", "ts"),
    ("moller_ribs", "moller_inst", "moller"),
    ("pelvis803", "pelvis", "v11_pelvis"),
    ("gt_v11", "gt", "v11"),
)
SCHEME_TITLE = {"verse": "SPINEPS + VERIDAH instances, VerSe-coded (L1-L6 20-25, sacrum 26, T13 28; disc = 100 + "
                         "the vertebra above it)",
                "spineps_sem": "SPINEPS semantic subregions (TPTBox Location values)",
                "ts": "TotalSegmentator total (class_map.json; sacrum = 25 UNION vertebrae_S1 26)",
                "moller": "Moller rib instances (rib id = VerSe vertebra id + 32; 255 unassigned) over the SPINEPS "
                          "instances",
                "v11_pelvis": "Dataset803 pelvis, post-processed to release ids (sacrum 26, hips 30/31)",
                "v11": "CTSpinoPelvic1K v11 release labels (VerSe-native; id 29 retired)"}

# census column aliases: canonical -> accepted spellings (tier1.tsv spellings included)
ALIASES = {
    "case_key": ("case_key", "key"), "collection": ("collection", "source"), "case_id": ("case_id", "case"),
    "person_key": ("person_key", "patient_key"), "tier": ("tier",), "count": ("count", "rule1_count"),
    "anchor_source": ("anchor_source",), "flags": ("flags", "flag"), "rules": ("rules",),
    "stump_left": ("stump_left",), "stump_right": ("stump_right",), "s3_ratio": ("s3_ratio", "rule3_ratio"),
    "last_rib_level": ("last_rib_level",), "prior_subtype": ("prior_subtype",),
    "registry_subtype": ("registry_subtype",), "truth_tier": ("truth_tier",),
    "no_count_reason": ("no_count_reason", "count_reason", "reasons"),
    "ct": ("ct", "ct_path"), "spineps_inst": ("spineps_inst", "spineps_vert"),
    "spineps_sem": ("spineps_sem", "spineps_spine"), "spineps_ctd": ("spineps_ctd", "ctd"),
    "spineps_ids": ("spineps_ids",), "ts": ("ts", "ts_output", "ts_total"), "ts_class_map": ("ts_class_map",),
    "ts_kind": ("ts_kind",), "ts_alt": ("ts_alt",), "moller_inst": ("moller_inst", "moller_ribs", "rib_inst"),
    "moller_csv": ("moller_csv", "rib_measurements"), "moller_measure_json": ("moller_measure_json", "measure_json"),
    "pelvis": ("pelvis", "pelvis803", "pelvis_post"), "pelvis_json": ("pelvis_json",),
    "gt": ("gt", "gt_label", "gt_v11"), "has_xr": ("has_xr", "paired", "real_frames"),
    "xr_paths": ("xr_paths", "xr"), "notes": ("notes",), "registry_flags": ("registry_flags",),
}
HIDDEN_PREFIXES = ("registry", "prior", "truth", "read_", "labeller", "consensus", "hidden")
AH_COLLECTION_DIR = {"ts": "totalsegmentator", "ribfrac": "other_ct/ribfrac", "ctspine1k": "other_ct/ctspine1k",
                     "carmlspine": "other_ct/carmlspine"}


# ----------------------------------------------------------------------------------------------------- small helpers
def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")


def write_if_changed(path: Path, data) -> bool:
    """Write bytes/str only when the content differs (a re-run must not touch identical files). Returns changed."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not path.is_symlink() and path.stat().st_size == len(data) and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True


def truthy(v) -> bool:
    return str(v if v is not None else "").strip().lower() in ("1", "true", "yes", "y", "t", "paired")


def blank(v) -> bool:
    return v is None or str(v).strip().lower() in ("", "nan", "none", "null")


def split_list(v):
    if blank(v):
        return []
    return [x.strip() for x in re.split(r"[;|]", str(v)) if x.strip()]


def safe_dirname(key: str) -> str:
    """A case key such as `ctsp:0005` as a directory name that works on Ceph and on Windows."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", key.strip()).strip("_") or "case"


def git_head(cwd: Path):
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(cwd), capture_output=True, text=True, timeout=20)
        if out.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", out.stdout.strip()):
            return out.stdout.strip(), None
        return None, (out.stderr or out.stdout).strip()[:200]
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"[:200]


def prereg_status_of(text: str) -> str:
    m = re.search(r"sha256 of this file:\s*([0-9a-fA-F_]+)", text or "")
    return "frozen" if (m and re.fullmatch(r"[0-9a-fA-F]{64}", m.group(1))) else "draft"


def id_rgb(idx: int):
    """A distinct colour per id (golden-angle hue, alternating value/saturation), as the dataset's reviewtool does."""
    import colorsys
    if idx <= 0:
        return (0, 0, 0)
    hue = (idx * 0.6180339887498949) % 1.0
    sat = 1.0 if (idx % 3) else 0.72
    val = 1.0 if (idx % 2 == 0) else 0.74
    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (int(r * 255), int(g * 255), int(b * 255))


def itksnap_descriptor(ids, names, title: str) -> str:
    lines = ["################################################", "# ITK-SnAP Label Description File",
             f"# {title}", "# ids = exactly np.unique of the mask this file sits beside; do not renumber",
             '# Fields: IDX  -R-  -G-  -B-  -A--  VIS MSH  "LABEL"', "################################################"]
    for i in ids:
        i = int(i)
        if i == 0:
            lines.append('    0     0    0    0        0  0  0    "Clear Label"')
            continue
        r, g, b = id_rgb(i)
        lines.append(f'{i:5d} {r:5d} {g:4d} {b:4d}        1  1  1    "{names.get(i, f"unknown_{i}")}"')
    return "\n".join(lines) + "\n"


def slicer_ctbl(ids, names, title: str) -> str:
    lines = [f"# Color table file: {title}", "# id name r g b a  (0-255)"]
    for i in ids:
        i = int(i)
        if i == 0:
            lines.append("0 background 0 0 0 0")
            continue
        r, g, b = id_rgb(i)
        nm = re.sub(r"\s+", "_", names.get(i, f"unknown_{i}"))
        lines.append(f"{i} {nm} {r} {g} {b} 255")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------------------------------- optional imports
def import_ostk(ostk_path):
    """ostk.labels, from the environment or from --ostk-path (default: a sibling OpenSpineToolkit checkout)."""
    cands = [ostk_path] if ostk_path else []
    cands += [os.environ.get("OSTK_PATH"), str(REPO.parent / "OpenSpineToolkit"), os.path.expanduser("~/OpenSpineToolkit")]
    for c in cands:
        if c and os.path.isdir(c) and str(c) not in sys.path:
            sys.path.insert(0, str(c))
    try:
        from ostk import labels as L  # noqa: N812
        return L, None
    except Exception as exc:  # noqa: BLE001
        return None, f"ostk not importable ({type(exc).__name__}: {exc}); pass --ostk-path"


def import_spineps_ids():
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    try:
        from tools import spineps_ids as S  # noqa: N812
        return S, None
    except Exception as exc:  # noqa: BLE001
        return None, f"tools.spineps_ids not importable ({type(exc).__name__}: {exc})"


# ----------------------------------------------------------------------------------------------------- census
def read_census(path: Path):
    """Rows as dicts with canonical keys (aliases resolved), plus the list of canonical columns found and the
    raw rows (verbatim, for evidence.json). Everything is a string; nothing is coerced."""
    import pandas as pd
    df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cols = list(df.columns)
    lower = {c.lower(): c for c in cols}
    found = {}
    for canon, names in ALIASES.items():
        for n in names:
            if n.lower() in lower:
                found[canon] = lower[n.lower()]
                break
    rows = []
    for i, raw in enumerate(df.to_dict(orient="records")):
        r = {canon: raw.get(src, "") for canon, src in found.items()}
        r["_raw"] = raw
        r["_index"] = i
        r["_rule2"] = {c: raw[c] for c in cols if c.lower().startswith("rule2_")}
        r["_hidden_cols"] = {c: raw[c] for c in cols if c.lower().startswith(HIDDEN_PREFIXES)}
        rows.append(r)
    return rows, found, cols


def norm_case(r: dict) -> None:
    """Fill collection / case_id / case_key / person_key from each other; zfill(4) CTSP ids."""
    coll = (r.get("collection") or "").strip()
    cid = (r.get("case_id") or "").strip()
    key = (r.get("case_key") or "").strip()
    if not key and (r.get("person_key") or "").strip() and not coll:
        key = r["person_key"].strip()
    if not coll and ":" in key:
        coll = key.split(":", 1)[0]
    if not cid and ":" in key:
        cid = key.split(":", 1)[1]
    if coll == "ctsp" and cid.isdigit():
        cid = cid.zfill(4)
    if not key or (coll == "ctsp" and key != f"{coll}:{cid}"):
        key = f"{coll}:{cid}" if coll else cid
    r["collection"], r["case_id"], r["case_key"] = coll, cid, key
    if blank(r.get("person_key")):
        r["person_key"] = key
    r["case_dir_name"] = safe_dirname(key)


def types_of(r: dict):
    """(primary type, also_in types, rules raising) from flags, count and the stump columns."""
    flags = split_list(r.get("flags"))
    found = set()
    for f in flags:
        fl = f.lower()
        for rx, t in FLAG_RULES:
            if re.search(rx, fl):
                found.add(t)
    cnt = (r.get("count") or "").strip().lower()
    if cnt == "6":
        found.add("L6")
    elif cnt == "4":
        found.add("four_lumbar_or_fused_L5")
    elif cnt in ("no_count", "no_anchor", "none", "nan") or (cnt == "" and (r.get("anchor_source") or "").lower()
                                                               .startswith("no_anchor")):
        found.add("unresolved")
    for side in ("stump_left", "stump_right"):
        v = (r.get(side) or "").strip().upper()
        if v in ("STUMP", "ABSENT"):
            found.add("stump_rib")
    positives = [t for t in TYPES if t in found and t != "unresolved"]
    if positives:
        primary, also = positives[0], positives[1:] + (["unresolved"] if "unresolved" in found else [])
    else:
        primary, also = "unresolved", []
    rules = split_list(r.get("rules"))
    if not rules:
        rs = []
        for t in [primary] + also:
            rs.append(TYPE_RULE[t])
        low = " ".join(flags).lower()
        if r.get("_rule2") and any(re.search(r"out|flag|abnormal|beyond|1$|true", str(v).lower())
                                   for k, v in r["_rule2"].items() if k.lower().endswith(("_flag", "_outside"))):
            rs.append("rule2")
        if "rule2" in low or "sacral_shape" in low:
            rs.append("rule2")
        if "rule4" in low or "thoracic" in low:
            rs.append("rule4")
        rules = sorted(set(rs), key=lambda x: ("rule1", "rule1b", "rule2", "rule3", "rule4").index(x)
                       if x in ("rule1", "rule1b", "rule2", "rule3", "rule4") else 9)
    return primary, also, rules


def rules_not_run(r: dict, present: dict) -> list:
    """Which rules could not run on this CT and why, from the census row and from which inputs exist."""
    out = []
    cnt = (r.get("count") or "").strip().lower()
    why = (r.get("no_count_reason") or "").strip() or (r.get("anchor_source") or "").strip()
    if cnt in ("no_count", "no_anchor", "") or cnt is None:
        out.append({"rule": "rule1", "why": f"count is {cnt or 'blank'}" + (f" ({why})" if why else "") +
                    "; a cut field is no_count, never ordinary (PREREG 0)"})
    if not present.get("moller_ribs"):
        out.append({"rule": "rule3", "why": "no Moller rib measurement on disk for this CT (arm B fast not yet run, "
                                            "or refused)"})
    if not present.get("pelvis803"):
        out.append({"rule": "rule2", "why": "no Dataset803 pelvis yet; rule 1's anchor is the TS sacrum UNION S1 "
                                            "(anchor_source says so) and rule 2 has no Dataset803 features"})
    else:
        out.append({"rule": "rule2", "why": "scored but gates nothing: no validated threshold before the "
                                            "reference-half freeze (PREREG 2)"})
    if cnt == "6":
        out.append({"rule": "rule1b", "why": "the sixth-body classifier is not yet trained on named T12/L1 "
                                             "(PREREG 1b); the reviewer's facet/process reading is the arbiter"})
        out.append({"rule": "rule4", "why": "the MDPA shape score has no operating threshold recorded yet and has "
                                            "never been applied to an unnamed body (PREREG 4)"})
    if (r.get("collection") or "") == "carmlspine":
        out.append({"rule": "rule1/3/4", "why": "C-ArmLSpine: the thoraco-lumbar junction is in field on ~13 % of "
                                                "cases; mostly rule-2 evidence is available (PREREG 6)"})
    return out


# ----------------------------------------------------------------------------------------------------- placing files
class Placer:
    def __init__(self, copy: bool, hash_limit_mb: float | None):
        self.copy = copy
        self.hash_limit = hash_limit_mb
        self._sha = {}
        self.symlink_ok = None

    def sha(self, src: Path):
        """{sha256, bytes} of a file; for a directory, the sha256 over the sorted "sha  relpath" lines of its files
        plus the per-file table, so a directory input is identified as exactly as a file is."""
        src = Path(src)
        k = str(src)
        if k in self._sha:
            return self._sha[k]
        if src.is_dir():
            files = {}
            total = 0
            for p in sorted(x for x in src.rglob("*") if x.is_file()):
                rel = p.relative_to(src).as_posix()
                files[rel] = sha256_file(p)
                total += p.stat().st_size
            digest = sha256_bytes("".join(f"{s}  {n}\n" for n, s in files.items()).encode("utf-8"))
            v = {"sha256": digest, "bytes": total, "sha256_of": "sorted 'sha256  relpath' lines of the directory's files",
                 "files": files}
            self._sha[k] = v
            return v
        try:
            size = src.stat().st_size
        except OSError:
            return None
        if self.hash_limit is not None and size > self.hash_limit * 1e6:
            v = {"sha256": None, "bytes": size, "sha256_skipped": f"file larger than --hash-limit-mb {self.hash_limit}"}
        else:
            v = {"sha256": sha256_file(src), "bytes": size}
        self._sha[k] = v
        return v

    def place(self, src: Path, dst: Path) -> str:
        """Symlink (default) or copy `src` at `dst`. Never rewrites the bytes. Returns the link mode used.
        A destination that already is what we want is left alone, so a re-run touches nothing."""
        src = Path(src)
        dst = Path(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        target = os.path.abspath(str(src))
        want_link = (not self.copy) and self.symlink_ok is not False
        copied_mode = "copy" if self.copy else "copy_fallback"
        if dst.is_symlink():
            if want_link and os.readlink(str(dst)) == target:
                return "symlink"
            dst.unlink()
        elif dst.is_dir():
            if not want_link:
                return copied_mode + "_dir"
            shutil.rmtree(dst)
        elif dst.exists():
            if not want_link and src.is_file() and dst.stat().st_size == src.stat().st_size \
                    and sha256_file(dst) == (self.sha(src) or {}).get("sha256", object()):
                return copied_mode
            dst.unlink()
        if want_link:
            try:
                os.symlink(target, str(dst), target_is_directory=src.is_dir())
                self.symlink_ok = True
                return "symlink"
            except (OSError, NotImplementedError):
                self.symlink_ok = False          # Windows without the privilege: copy from here on, and say so
                copied_mode = "copy_fallback"
        if src.is_dir():
            shutil.copytree(src, dst)
            return copied_mode + "_dir"
        shutil.copy2(src, dst)
        return copied_mode


def image_info(path: Path) -> dict:
    """Header facts without loading voxels: nibabel first (NIfTI), SimpleITK for everything else."""
    p = str(path)
    if p.endswith((".nii", ".nii.gz")):
        import nibabel as nib
        img = nib.load(p)
        return {"shape": [int(x) for x in img.shape], "zooms": [round(float(z), 5) for z in img.header.get_zooms()],
                "axcodes": "".join(nib.aff2axcodes(img.affine)), "affine": np.round(img.affine, 5).tolist(),
                "dtype": str(img.get_data_dtype())}
    import SimpleITK as sitk
    rd = sitk.ImageFileReader()
    rd.SetFileName(p)
    rd.ReadImageInformation()
    return {"shape": list(rd.GetSize()), "zooms": [round(float(s), 5) for s in rd.GetSpacing()],
            "origin_lps": list(rd.GetOrigin()), "direction": list(rd.GetDirection()),
            "dtype": rd.GetPixelIDTypeAsString(), "axcodes": None}


def load_mask(path: Path):
    import nibabel as nib
    img = nib.load(str(path))
    arr = np.asanyarray(img.dataobj)
    ids, n = np.unique(arr, return_counts=True)
    return img, arr, [int(i) for i in ids], {int(i): int(c) for i, c in zip(ids, n)}


def verse_name(i: int):
    if i in VERSE_NAMES:
        return VERSE_NAMES[i]
    if 100 < i <= 128 and (i - 100) in VERSE_NAMES:
        return f"disc_below_{VERSE_NAMES[i - 100]}"
    return None


def names_for(scheme: str, ids, ctx: dict) -> dict:
    out = {}
    for i in ids:
        if i == 0:
            continue
        nm = None
        if scheme == "verse":
            nm = verse_name(i)
        elif scheme == "spineps_sem":
            nm = SPINEPS_SEM_NAMES.get(i)
        elif scheme == "ts":
            nm = ctx["ts_map"].get(i)
        elif scheme == "moller":
            nm = verse_name(i)
            if nm is None and (i - MOLLER_RIB_OFFSET) in VERSE_NAMES:
                nm = f"rib_of_{VERSE_NAMES[i - MOLLER_RIB_OFFSET]}"
            if nm is None and i == MOLLER_UNASSIGNED:
                nm = "unassigned_rib"
        elif scheme in ("v11", "v11_pelvis"):
            nm = ctx["v11_names"].get(i)
        out[i] = nm or f"unknown_{i}"
    return out


# ----------------------------------------------------------------------------------------------------- radiographs
def is_pose_json(p: Path) -> bool:
    try:
        d = json.loads(Path(p).read_text(encoding="utf-8-sig"))
        return isinstance(d, dict) and all(k in d for k in ("K", "R", "t"))
    except Exception:  # noqa: BLE001
        return False


def tfm_text(R, t) -> str:
    R = np.asarray(R, float).reshape(3, 3)
    t = np.asarray(t, float).reshape(3)
    p = " ".join(f"{v:.10g}" for v in list(R.ravel()) + list(t))
    return ("#Insight Transform File V1.0\n#Transform 0\nTransform: AffineTransform_double_3_3\n"
            f"Parameters: {p}\nFixedParameters: 0 0 0\n")


def radiograph_nifti_bytes(pix: np.ndarray, K, sid: float) -> bytes:
    """A single-slice NIfTI of the frame placed on the detector plane of the camera frame (LPS, mm): the ray of pixel
    centre (u, v) = (col + 0.5, row + 0.5) meets z = sid at ((u - cx) sid / fx, (v - cy) sid / fy, sid). Written
    with a deterministic gzip header so a re-run produces identical bytes."""
    import nibabel as nib
    K = np.asarray(K, float)
    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    A = np.eye(4)
    A[0, 0] = sid / fx
    A[1, 1] = sid / fy
    A[0, 3] = (0.5 - cx) * sid / fx
    A[1, 3] = (0.5 - cy) * sid / fy
    A[2, 3] = sid
    lps_to_ras = np.diag([-1.0, -1.0, 1.0, 1.0])
    data = np.ascontiguousarray(pix.T[:, :, None])          # (cols, rows, 1): voxel i = column, j = row
    img = nib.Nifti1Image(data, lps_to_ras @ A)
    img.header.set_xyzt_units("mm")
    raw = img.to_bytes()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        gz.write(raw)
    return buf.getvalue()


def read_frame_pixels(path: Path):
    """(pixel array float32/uint16 [rows, cols], header dict) of a DICOM spot frame, or (None, why)."""
    try:
        import pydicom
    except Exception as exc:  # noqa: BLE001
        return None, f"pydicom not importable ({exc})"
    try:
        ds = pydicom.dcmread(str(path))
        pix = ds.pixel_array
        hdr = {k: (str(getattr(ds, k)) if getattr(ds, k, None) is not None else None) for k in
               ("Modality", "Rows", "Columns", "PositionerPrimaryAngle", "PositionerSecondaryAngle",
                "DistanceSourceToDetector", "DistanceSourceToPatient", "KVP", "PixelSpacing", "ImagerPixelSpacing",
                "PhotometricInterpretation", "BitsStored")}
        return np.asarray(pix), hdr
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def collect_xr(r: dict, args) -> list:
    """[{kind: frame|pose|other|preview, path}] from xr_paths, else from the collection's store."""
    items = []
    for p in split_list(r.get("xr_paths")):
        P = Path(p)
        if not P.exists():
            items.append({"kind": "missing", "path": str(P)})
        elif P.suffix.lower() == ".json" and is_pose_json(P):
            items.append({"kind": "pose", "path": str(P)})
        elif P.suffix.lower() in (".png", ".jpg", ".jpeg"):
            items.append({"kind": "preview", "path": str(P)})
        elif P.suffix.lower() in (".mha", ".mhd", ".xml", ".yaml", ".yml", ".txt", ".csv"):
            items.append({"kind": "other", "path": str(P)})
        else:
            items.append({"kind": "frame", "path": str(P)})
    coll, cid = r.get("collection"), r.get("case_id")
    if not items and coll == "carmlspine" and args.carmlspine_root:
        root = Path(args.carmlspine_root)
        for pj in sorted((root / "pose").glob(f"{cid}_*_ref*.json")):
            if is_pose_json(pj):
                items.append({"kind": "pose", "path": str(pj)})
        case_dir = root / "unpacked" / "C-ArmLSpine" / cid
        frames = set()
        for it in [i for i in items if i["kind"] == "pose"]:
            fr = json.loads(Path(it["path"]).read_text(encoding="utf-8-sig")).get("frame")
            if fr:
                hits = [p for p in case_dir.rglob(Path(fr).name)] if case_dir.exists() else []
                for h in hits[:1]:
                    frames.add(str(h))
        for f in sorted(frames):
            items.append({"kind": "frame", "path": f})
    if not items and coll == "cobra" and args.cobra_root:
        cdir = Path(args.cobra_root) / cid
        for nm in ("projections.mha", "geometry.xml", "metadata.yaml", "reconstruction.yaml"):
            if (cdir / nm).exists():
                items.append({"kind": "other", "path": str(cdir / nm)})
        for pv in sorted(cdir.glob("overview_*.png")) if cdir.exists() else []:
            items.append({"kind": "preview", "path": str(pv)})
    return items


def write_xr(case_dir: Path, r: dict, items: list, placer: Placer, evid: dict, failures: list) -> dict:
    """Place the radiographs and derive the viewer geometry. Returns the xr block for evidence.json."""
    xr = {"items": [], "views": [], "pose_status": None, "projection_convention": None}
    if not items:
        return xr
    xdir = case_dir / "xr"
    pdir = case_dir / "previews"
    poses = [i for i in items if i["kind"] == "pose"]
    frames = [i for i in items if i["kind"] == "frame"]
    frame_by_name = {Path(f["path"]).name: f["path"] for f in frames}
    placed_frames = {}
    # views: name each frame by the pose that uses it, else by order
    view_of_frame = {}
    for it in poses:
        d = json.loads(Path(it["path"]).read_text(encoding="utf-8-sig"))
        fr = d.get("frame")
        if fr and Path(fr).name in frame_by_name and Path(fr).name not in view_of_frame:
            view_of_frame[Path(fr).name] = str(d.get("view") or "view")
    n_unnamed = 0
    for f in frames:
        nm = Path(f["path"]).name
        view = view_of_frame.get(nm)
        if view is None:
            n_unnamed += 1
            view = f"frame{n_unnamed}"
        dst = xdir / f"xr_{view}.dcm"
        mode = placer.place(Path(f["path"]), dst)
        info = placer.sha(Path(f["path"]))
        evid["inputs"][f"xr_frame_{view}"] = {"source": f["path"], "placed_as": str(dst.relative_to(case_dir)).replace(os.sep, "/"),
                                              "link_mode": mode, **(info or {})}
        placed_frames[nm] = {"view": view, "dst": dst, "src": f["path"]}
        xr["views"].append(view)
    statuses = []
    nifti_done = {}
    for it in poses:
        d = json.loads(Path(it["path"]).read_text(encoding="utf-8-sig"))
        info = placer.sha(Path(it["path"]))
        view = str(d.get("view") or "view")
        tag = str(d.get("tag") or "")
        suffix = "" if tag in ("", "_ref") else tag
        name = f"{view}{suffix}"
        K = np.asarray(d["K"], float).reshape(3, 3)
        R = np.asarray(d["R"], float).reshape(3, 3)
        t = np.asarray(d["t"], float).reshape(3)
        sid = float(d.get("sid") or 0) or float(K[0, 0]) * float(d.get("px_mm") or 1)
        px = d.get("px_mm")
        cols = None
        fr = d.get("frame")
        frec = placed_frames.get(Path(fr).name) if fr else None
        # pose status: PREREG section 6 -- every C-ArmLSpine pose was fit at 300 mm / 2048 px (0.1465 mm) while the
        # panel is 307.2 mm (0.150 mm); such a pose is exported but marked stale.
        status = "ok"
        if px is not None and r.get("collection") == "carmlspine":
            if abs(float(px) - DET_MM_CARM / 2048.0) > 1e-6:
                status = "stale_px_mm_needs_refit"
        statuses.append(status)
        source_world = (-R.T @ t).tolist()                      # drr_register: source = -R^T t
        r_resid = float(np.abs(R @ R.T - np.eye(3)).max())      # a float32 fit is orthonormal to ~1e-7
        K_cv = K.copy()
        K_cv[0, 2] -= 0.5
        K_cv[1, 2] -= 0.5
        P = K_cv @ np.hstack([R, t.reshape(3, 1)])
        ptxt = "\n".join(" ".join(f"{v:.10g}" for v in row) for row in P) + "\n"
        write_if_changed(xdir / f"xr_{name}_P.txt", ptxt)
        write_if_changed(xdir / f"xr_{name}_cam_from_world.tfm", tfm_text(R, t))
        nifti_rel = None
        if frec is not None:
            nifti_rel = f"xr/xr_{frec['view']}.nii.gz"
            if nifti_rel not in nifti_done:
                pix, hdr = read_frame_pixels(Path(frec["src"]))
                if pix is None:
                    failures.append({"what": f"xr {name}", "why": f"frame pixels unreadable: {hdr}"})
                    nifti_rel = None
                else:
                    cols = int(pix.shape[1])
                    write_if_changed(case_dir / nifti_rel, radiograph_nifti_bytes(pix, K, sid))
                    nifti_done[nifti_rel] = cols
            else:
                cols = nifti_done[nifti_rel]
        pose_out = {"source_pose_json": it["path"], "pose_sha256": (info or {}).get("sha256"), "view": view,
                    "tag": tag, "frame": fr, "K": K.tolist(), "R": R.tolist(), "t": t.tolist(),
                    "px_mm": px, "sid_mm": sid, "sod_mm": d.get("sod"), "frame_cols": cols,
                    "px_mm_expected_from_panel": (DET_MM_CARM / cols) if (cols and r.get("collection") == "carmlspine") else None,
                    "pose_status": status, "source_world_lps_mm": source_world,
                    "R_orthonormality_residual": r_resid,
                    "world_frame": "the CT volume's SimpleITK physical frame (LPS mm), as tools/drr_register.py uses it",
                    "camera_model": "p_cam = R p_world + t; pixel = K p_cam / z with pixel centre (col + 0.5, row + 0.5)",
                    "P_txt": {"file": f"xr/xr_{name}_P.txt", "convention": "OpenCV: 3x4 = K' [R | t], K' = K with "
                              "(cx, cy) shifted by -0.5 so pixel centres are integer (col, row); world in LPS mm"},
                    "tfm": {"file": f"xr/xr_{name}_cam_from_world.tfm", "convention": "ITK AffineTransform, LPS, "
                            "maps world (CT) -> camera; in 3D Slicer put the radiograph slice under this transform node"},
                    "radiograph_nifti": nifti_rel, "edge_ncc": d.get("edge_ncc"), "int_ncc": d.get("int_ncc"),
                    "margin": d.get("margin"), "hypothesis": d.get("hypothesis") or d.get("hyp")}
        write_if_changed(xdir / f"xr_{name}_pose.json", canonical_json(pose_out))
        evid["inputs"][f"xr_pose_{name}"] = {"source": it["path"], "placed_as": f"xr/xr_{name}_pose.json",
                                             "link_mode": "derived", **(info or {})}
        xr["items"].append(pose_out)
        png = Path(it["path"]).with_suffix(".png")
        if png.exists():
            mode = placer.place(png, pdir / f"xr_{name}_overlay.png")
            evid["inputs"][f"xr_overlay_{name}"] = {"source": str(png), "placed_as": f"previews/xr_{name}_overlay.png",
                                                    "link_mode": mode, **(placer.sha(png) or {})}
    for it in [i for i in items if i["kind"] in ("other", "preview")]:
        src = Path(it["path"])
        dst = (pdir if it["kind"] == "preview" else xdir) / src.name
        mode = placer.place(src, dst)
        evid["inputs"][f"xr_{it['kind']}_{src.name}"] = {"source": str(src), "placed_as": str(dst.relative_to(case_dir)).replace(os.sep, "/"),
                                                         "link_mode": mode, **(placer.sha(src) or {})}
        xr["items"].append({"kind": it["kind"], "file": str(dst.relative_to(case_dir)).replace(os.sep, "/"),
                            "note": ("COBRA kV sweep with RTK geometry; masks live on ct_def; no per-projection matrix "
                                     "is exported here (RTK -> OpenCV conversion is not part of this tool)"
                                     if src.suffix in (".mha", ".xml") else None)})
    for it in [i for i in items if i["kind"] == "missing"]:
        failures.append({"what": "xr", "why": f"xr path does not exist: {it['path']}"})
    if statuses:
        xr["pose_status"] = "stale_px_mm_needs_refit" if any(s != "ok" for s in statuses) else "ok"
        write_if_changed(xdir / "POSE_STATUS.txt",
                         f"pose_status: {xr['pose_status']}\n" +
                         ("These poses were fit at px_mm 0.146484375 (300 mm / 2048) while the panel is 307.2 mm "
                          "(0.150 mm/px). PREREG_rules.md section 6: poses are refit at 0.150 before any matrix is "
                          "used for a measurement. The matrices here are for orientation in the viewer only.\n"
                          if xr["pose_status"] != "ok" else "Poses consistent with the panel pitch.\n"))
        xr["projection_convention"] = "see xr/*_pose.json"
    return xr


# ----------------------------------------------------------------------------------------------------- hidden joins
class Joins:
    """Registry / prior calls / reads, all hidden from the reviewer. Loaded once, looked up per case."""

    def __init__(self, args, placer: Placer):
        self.args = args
        self.placer = placer
        self.registry = {}
        self.consensus = {}
        self.lumbosac = {}
        self.manifest = {}
        self.sources = {}
        if args.registry and Path(args.registry).exists():
            with open(args.registry, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    self.registry[row.get("patient_key", "")] = row
            self.sources["registry"] = str(args.registry)
        if args.consensus and Path(args.consensus).exists():
            with open(args.consensus, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    self.consensus[str(row.get("volume_id", "")).zfill(4)] = row
            self.sources["consensus"] = str(args.consensus)
        if args.lumbosac and Path(args.lumbosac).exists():
            with open(args.lumbosac, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    m = re.search(r"(\d+)", str(row.get("Name", "")))
                    if m:
                        self.lumbosac.setdefault(m.group(1), []).append(row)   # keyed by TCIA token
            self.sources["lumbosac"] = str(args.lumbosac)
        if args.ctsp_manifest and Path(args.ctsp_manifest).exists():
            d = json.loads(Path(args.ctsp_manifest).read_text(encoding="utf-8-sig"))
            for e in (d if isinstance(d, list) else d.get("records", [])):
                self.manifest[str(e.get("volume_id", "")).zfill(4)] = e
            self.sources["ctsp_manifest"] = str(args.ctsp_manifest)

    def for_case(self, r: dict, evid: dict) -> dict:
        h = {"note": "audit only; withheld from both review stages (PREREG 7)"}
        pk, coll, cid = r.get("person_key"), r.get("collection"), r.get("case_id")
        for nm, p in self.sources.items():
            evid["inputs"].setdefault(f"hidden_source_{nm}", {"source": p, **(self.placer.sha(Path(p)) or {})})
        if self.registry:
            h["registry_row"] = self.registry.get(pk) or self.registry.get(r.get("case_key")) or None
        if r.get("_hidden_cols"):
            h["census_hidden_columns"] = r["_hidden_cols"]
        for k in ("prior_subtype", "registry_subtype", "truth_tier", "registry_flags"):
            if not blank(r.get(k)):
                h[k] = r[k]
        if coll == "ctsp":
            if self.consensus:
                h["castellvi_consensus"] = self.consensus.get(cid)
            m = self.manifest.get(cid) if self.manifest else None
            if m:
                h["ctsp_manifest"] = {k: m.get(k) for k in ("volume_id", "token", "lstv_label", "castellvi_type",
                                                             "castellvi_agreement", "has_l6", "n_lumbar_labels",
                                                             "has_lumbar_rib", "lumbar_rib_side", "prov_pelvis",
                                                             "prov_spine", "hardware")}
                tok = str(m.get("token", ""))
                if self.lumbosac and tok in self.lumbosac:
                    h["lumbosac_worksheet"] = self.lumbosac[tok]
        ah = self.args.ah_root
        if ah:
            sub = AH_COLLECTION_DIR.get(coll, coll)
            base = Path(ah) / sub
            for kind in ("labeller_b", "calls"):
                p = base / kind / f"{cid}.json"
                if p.exists():
                    try:
                        h[f"prior_{kind}"] = json.loads(p.read_text(encoding="utf-8-sig"))
                    except Exception as exc:  # noqa: BLE001
                        h[f"prior_{kind}"] = {"unreadable": str(exc)}
                    evid["inputs"][f"hidden_prior_{kind}"] = {"source": str(p), **(self.placer.sha(p) or {})}
            rows = base / "rows.csv"
            if rows.exists():
                key = f"{sub}:{cid}"
                if key not in self._rows_cache(rows):
                    key = cid
                row = self._rows_cache(rows).get(key)
                if row:
                    h["prior_rows_csv"] = row
                    evid["inputs"]["hidden_prior_rows_csv"] = {"source": str(rows), **(self.placer.sha(rows) or {})}
        return h

    _cache = {}

    def _rows_cache(self, rows: Path) -> dict:
        k = str(rows)
        if k not in self._cache:
            d = {}
            with open(rows, encoding="utf-8-sig", newline="") as f:
                for row in csv.DictReader(f):
                    d[row.get("case", "")] = row
                    d[row.get("patient_key", "")] = row
            self._cache[k] = d
        return self._cache[k]


# ----------------------------------------------------------------------------------------------------- one case
SLICER_TEMPLATE = r'''# make_slicer_scene.py -- build the 3D Slicer scene for this review case and save case.mrb.
# Run INSIDE Slicer's Python:   Slicer --no-main-window --python-script make_slicer_scene.py
# or in View > Python Console:  exec(open(r"<this file>").read())
# Loads the CT, every mask as a label volume with its colour table (and as a segmentation), the radiograph
# slices under their world->camera transforms with the X-ray source as a fiducial, then saves case.mrb beside
# this script. Nothing is resampled or reoriented; Slicer converts LPS/RAS on load.
# Written by transitional_review.build_review_tree v__VERSION__ for case __CASE__.
import json
import os

SPEC = json.loads(r"""__SPEC__""")
CASE_DIR = os.environ.get("REVIEW_CASE_DIR") or (os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd())
MAKE_SURFACES = os.environ.get("REVIEW_SURFACES", "0") == "1"      # closed surfaces are slow on 512^3 masks


def P(rel):
    return os.path.join(CASE_DIR, *rel.split("/"))


def main():
    import slicer
    ct = None
    if SPEC.get("ct") and os.path.exists(P(SPEC["ct"])):
        ct = slicer.util.loadVolume(P(SPEC["ct"]), properties={"name": "CT " + SPEC["case"]})
    for m in SPEC["masks"]:
        if not os.path.exists(P(m["path"])):
            print("missing mask", m["path"])
            continue
        color = slicer.util.loadColorTable(P(m["ctbl"]))
        props = {"name": m["name"], "labelmap": True}
        if color is not None:
            props["colorNodeID"] = color.GetID()
        lab = slicer.util.loadLabelVolume(P(m["path"]), properties=props)
        try:
            seg = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", m["name"] + "_seg")
            slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(lab, seg)
            if MAKE_SURFACES:
                seg.CreateClosedSurfaceRepresentation()
        except Exception as exc:  # noqa: BLE001
            print("segmentation import failed for", m["name"], exc)
    for x in SPEC["xr"]:
        if not (x.get("nifti") and os.path.exists(P(x["nifti"])) and os.path.exists(P(x["tfm"]))):
            print("radiograph or transform missing for", x["name"])
            continue
        tnode = slicer.util.loadTransform(P(x["tfm"]))
        vol = slicer.util.loadVolume(P(x["nifti"]), properties={"name": "XR " + x["name"], "singleFile": True})
        vol.SetAndObserveTransformNodeID(tnode.GetID())
        fid = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "source " + x["name"])
        s = x["source_world_lps_mm"]
        fid.AddControlPoint(-s[0], -s[1], s[2])          # LPS -> RAS
        fid.SetNthControlPointLabel(0, "X-ray source " + x["name"] + " (" + x["pose_status"] + ")")
    if ct is not None:
        slicer.util.setSliceViewerLayers(background=ct)
    out = P("case.mrb")
    ok = slicer.util.saveScene(out)
    print("saved" if ok else "SAVE FAILED", out)
    return 0 if ok else 1


rc = main()
if os.environ.get("REVIEW_EXIT_SLICER", "1") == "1" and "__file__" in globals():   # --python-script mode
    try:
        import slicer
        slicer.util.exit(rc)
    except Exception:  # noqa: BLE001
        pass
'''


def build_case(r: dict, args, root: Path, placer: Placer, meta: dict, ctx: dict, joins: Joins) -> dict:
    """Write one case directory; return its manifest row."""
    primary, also, rules = types_of(r)
    case_dir = root / primary / r["case_dir_name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    failures = []
    evid = {"header": dict(meta), "case": {}, "rules_row": {}, "rules_not_run": [], "inputs": {}, "masks": {},
            "xr": {}, "failures": failures, "hidden": {}}
    evid["header"]["census_row_index"] = r["_index"]
    evid["case"] = {"case_key": r["case_key"], "case_id": r["case_dir_name"], "collection": r["collection"],
                    "source_case_id": r["case_id"], "person_key": r["person_key"], "tier": r.get("tier", ""),
                    "type": primary, "also_in": also, "flags": split_list(r.get("flags")), "rules": rules,
                    "paired": bool(truthy(r.get("has_xr")) or split_list(r.get("xr_paths"))),
                    "count": r.get("count", ""), "anchor_source": r.get("anchor_source", "")}
    evid["rules_row"] = {k: v for k, v in r["_raw"].items() if not k.lower().startswith(HIDDEN_PREFIXES)}
    present = {}
    rel = lambda p: str(Path(p).relative_to(case_dir)).replace(os.sep, "/")  # noqa: E731

    # --- CT
    ct_src = (r.get("ct") or "").strip()
    ct_rel = None
    if not ct_src:
        failures.append({"what": "ct", "why": "census row has no CT path"})
    elif not Path(ct_src).exists():
        failures.append({"what": "ct", "why": f"CT path does not exist: {ct_src}"})
    else:
        ext = ".nii.gz" if ct_src.endswith(".nii.gz") else Path(ct_src).suffix
        dst = case_dir / f"ct{ext}"
        mode = placer.place(Path(ct_src), dst)
        ct_rel = rel(dst)
        info = {"source": ct_src, "placed_as": ct_rel, "link_mode": mode, **(placer.sha(Path(ct_src)) or {})}
        try:
            info.update(image_info(Path(ct_src)))
            info["reoriented"] = False
        except Exception as exc:  # noqa: BLE001
            failures.append({"what": "ct", "why": f"header unreadable: {exc}"})
        evid["inputs"]["ct"] = info
        if r.get("collection") == "cobra":
            info["note"] = "COBRA: masks live on ct_def (planning CT deformed to the CBCT), which is what the census points at"

    # --- masks
    masks_spec = []
    for mname, col, scheme in MASK_SPECS:
        src = (r.get(col) or "").strip()
        if not src and mname == "moller_ribs" and args.moller_root:
            cand = Path(args.moller_root) / r["collection"] / f"{r['case_id']}_rib-inst_msk.nii.gz"
            src = str(cand) if cand.exists() else ""
        if not src and mname == "pelvis803" and args.pelvis_root:
            cand = Path(args.pelvis_root) / r["collection"] / f"{r['case_id']}.nii.gz"
            src = str(cand) if cand.exists() else ""
        if src and mname == "ts_total" and Path(src).is_dir():
            roi_dir = Path(src)
            alt = Path(args.ts_root) / r["collection"] / f"{r['case_id']}.nii.gz" if args.ts_root else None
            if alt and alt.exists():
                src = str(alt)
            else:
                mode = placer.place(roi_dir, case_dir / "masks" / "ts_roi")
                evid["inputs"]["ts_roi"] = {"source": str(roi_dir), "placed_as": "masks/ts_roi", "link_mode": mode,
                                            "note": "per-structure TotalSegmentator directory (no hips); no multilabel "
                                                    "file exists for this CT, so ts_total is absent",
                                            **(placer.sha(roi_dir) or {})}
                present["ts_roi"] = True
                src = ""
        if not src:
            evid["masks"][mname] = {"present": False}
            continue
        sp = Path(src)
        if mname == "pelvis803" and re.search(r"(^|[\\/])(_work|_failed_raw)([\\/]|$)", src):
            failures.append({"what": mname, "why": f"refused: raw Dataset803 prediction path ({src}); only "
                                                    "post-processed pelvis files are read (ARM_B_pelvis 2)"})
            evid["masks"][mname] = {"present": False, "refused": src}
            continue
        if not sp.exists():
            failures.append({"what": mname, "why": f"path does not exist: {src}"})
            evid["masks"][mname] = {"present": False, "missing": src}
            continue
        try:
            img, arr, ids, counts = load_mask(sp)
        except Exception as exc:  # noqa: BLE001
            failures.append({"what": mname, "why": f"unreadable: {exc}"})
            evid["masks"][mname] = {"present": False, "unreadable": src}
            continue
        import nibabel as nib
        mrec = {"present": True, "source": src, "scheme": scheme, "scheme_title": SCHEME_TITLE[scheme],
                "shape": [int(x) for x in img.shape], "zooms": [round(float(z), 5) for z in img.header.get_zooms()],
                "axcodes": "".join(nib.aff2axcodes(img.affine)), "ids": ids, "ids_counts": {str(k): v for k, v in counts.items()},
                "checks": {}, "reoriented": False}
        ok = True
        names = {}
        if scheme == "verse":
            mrec["checks"]["ids_column"] = (r.get("spineps_ids") or "").strip() or None
            S = ctx["spineps_ids"]
            if S is None:
                mrec["checks"]["guard"] = f"not run: {ctx['spineps_ids_error']}"
                if (r.get("spineps_ids") or "").strip().lower() == "raw":
                    ok = False
                    failures.append({"what": mname, "why": "refused: census says raw 1..N ids and the guard could "
                                                            "not run; relabel upstream (tools/spineps_ids.py relabel)"})
            else:
                ctd = (r.get("spineps_ctd") or "").strip() or "auto"
                try:
                    rep = S.check_ids(str(sp), ctd)
                    v = rep.get("verdict")
                    mrec["checks"]["guard"] = {k: rep.get(k) for k in ("verdict", "reasons", "ctd", "ctd_agree",
                                                                       "ctd_disagree", "mono_verse",
                                                                       "order_top_to_bottom", "veridah_skipped_names")}
                    if rep.get("ctd") and os.path.exists(str(rep["ctd"])):
                        evid["inputs"]["spineps_ctd"] = {"source": str(rep["ctd"]), **(placer.sha(Path(rep["ctd"])) or {})}
                    accepted = v in ("verse_ok", "misnamed_1_2_levels", "empty") or \
                        (v == "verse_ok_no_ctd" and (r.get("spineps_ids") or "").lower() in ("verse_coded", "relabelled"))
                    if not accepted and args.relabel_raw and v in ("raw_or_scrambled", "not_verse_ids", "not_verse_order"):
                        pts = S.read_ctd(str(rep["ctd"])) if rep.get("ctd") and os.path.exists(str(rep["ctd"])) else None
                        if pts:
                            sem = None
                            semp = (r.get("spineps_sem") or "").strip()
                            if semp and Path(semp).exists():
                                simg = nib.load(semp)
                                sem = (np.asanyarray(simg.dataobj), simg.affine)
                            try:
                                out, rrep = S.relabel_by_ctd(arr, img.affine, pts, semantic=sem)
                                dst = case_dir / "masks" / "spineps_inst.nii.gz"
                                new = nib.Nifti1Image(out.astype(np.int16), img.affine, img.header)
                                new.set_data_dtype(np.int16)
                                raw = new.to_bytes()
                                buf = io.BytesIO()
                                with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
                                    gz.write(raw)
                                write_if_changed(dst, buf.getvalue())
                                arr = out
                                ids = [int(i) for i in np.unique(arr)]
                                counts = {int(i): int(c) for i, c in zip(*np.unique(arr, return_counts=True))}
                                mrec.update(ids=ids, ids_counts={str(k): v for k, v in counts.items()},
                                            relabelled_by_ctd={k: rrep.get(k) for k in ("mapping", "dropped", "labels", "post_check")},
                                            placed_as="masks/spineps_inst.nii.gz", link_mode="relabelled_copy_same_affine")
                                accepted = True
                                v = "relabelled"
                            except Exception as exc:  # noqa: BLE001
                                failures.append({"what": mname, "why": f"relabel refused: {exc}"})
                    if not accepted:
                        ok = False
                        failures.append({"what": mname, "why": f"refused: SPINEPS ids are not shown to be VerSe names "
                                                                f"[{v}] {'; '.join(rep.get('reasons') or [])}; relabel "
                                                                "upstream or pass --relabel-raw"})
                    if v == "verse_ok_no_ctd" and accepted:
                        mrec["checks"]["note"] = "no ctd beside the mask: names rest on the census's spineps_ids column"
                except Exception as exc:  # noqa: BLE001
                    ok = False
                    failures.append({"what": mname, "why": f"guard failed to run: {exc}"})
            names = names_for("verse", ids, ctx)
        elif scheme == "spineps_sem":
            names = names_for(scheme, ids, ctx)
        elif scheme == "ts":
            cm_path = (r.get("ts_class_map") or "").strip() or args.ts_class_map
            ts_map = dict(TS_DEFAULT_CLASS_MAP)
            if cm_path and Path(cm_path).exists():
                try:
                    ts_map = {int(k): str(v) for k, v in json.loads(Path(cm_path).read_text(encoding="utf-8-sig")).items()}
                    evid["inputs"]["ts_class_map"] = {"source": cm_path, **(placer.sha(Path(cm_path)) or {})}
                    mrec["checks"]["class_map"] = cm_path
                except Exception as exc:  # noqa: BLE001
                    mrec["checks"]["class_map"] = f"unreadable ({exc}); embedded 2.x map used"
            else:
                mrec["checks"]["class_map"] = "embedded TotalSegmentator 2.x total map"
            names = names_for("ts", ids, {"ts_map": ts_map})
            mrec["checks"]["sacrum_note"] = "sacrum = 25 UNION vertebrae_S1 26 (disjoint in TS v2)"
        elif scheme == "moller":
            names = names_for("moller", ids, ctx)
            ribs = sorted(i for i in ids if 33 <= i <= 60)
            mrec["checks"]["rib_bearing_ids"] = {str(i): VERSE_NAMES.get(i - MOLLER_RIB_OFFSET) for i in ribs}
            mrec["checks"]["unassigned_rib_vox"] = counts.get(MOLLER_UNASSIGNED, 0)
            stem = sp.name[: -len("_rib-inst_msk.nii.gz")] if sp.name.endswith("_rib-inst_msk.nii.gz") else sp.stem
            csvp = Path(r.get("moller_csv") or (sp.parent / f"{stem}_rib_measurements.csv"))
            mj = Path(r.get("moller_measure_json") or (sp.parent / "_done" / f"{stem}.measure.json"))
            if csvp.exists():
                with open(csvp, encoding="utf-8-sig", newline="") as f:
                    rows = list(csv.DictReader(f))
                keep = ("collection", "case_id", "variant", "vertebra", "vertebra_name", "side", "is_last_v",
                        "rib_length", "sr", "seg_at_border", "rib_volume", "n_path_points", "ids_verdict")
                mrec["rib_measurements"] = [{k: row.get(k) for k in keep if k in row} for row in rows]
                evid["inputs"]["moller_rib_measurements"] = {"source": str(csvp), **(placer.sha(csvp) or {})}
                placer.place(csvp, case_dir / "masks" / "moller_rib_measurements.csv")
            else:
                mrec["checks"]["rib_measurements"] = f"absent: {csvp}"
            if mj.exists():
                try:
                    J = json.loads(mj.read_text(encoding="utf-8-sig"))
                    mrec["measure_json"] = {k: J.get(k) for k in J if k.startswith("levels_") or k in
                                            ("ids_verdict", "ids_state", "vert_labels", "ok", "n_rows")}
                    evid["inputs"]["moller_measure_json"] = {"source": str(mj), **(placer.sha(mj) or {})}
                except Exception as exc:  # noqa: BLE001
                    mrec["checks"]["measure_json"] = f"unreadable: {exc}"
        elif scheme in ("v11", "v11_pelvis"):
            L = ctx["ostk"]
            if L is None:
                ok = False
                failures.append({"what": mname, "why": f"refused: {ctx['ostk_error']} (CTSP / Dataset803 masks are "
                                                        "resolved through ostk.labels.labels_for only)"})
            else:
                try:
                    lab = L.labels_for(counts=counts)
                    sch = L.detect_scheme(None, counts=counts)
                    hips = {n: counts.get(lab[n], 0) for n in ("left_hip", "right_hip", "sacrum")}
                    mrec["checks"]["labels_for"] = {"scheme": sch, "sacrum_id": lab["sacrum"], "left_hip_id": lab["left_hip"],
                                                    "right_hip_id": lab["right_hip"], "voxels": hips,
                                                    "id29_present": 29 in counts}
                    if sch != "v10":
                        ok = False
                        failures.append({"what": mname, "why": f"labels_for resolved scheme {sch!r}, not the release "
                                                                "scheme: wrong map or wrong file"})
                    elif hips["sacrum"] == 0 or (hips["left_hip"] == 0 and hips["right_hip"] == 0):
                        ok = False
                        failures.append({"what": mname, "why": "labels_for fell back to the default scheme: no sacrum "
                                                                "or hips under release ids (a raw Dataset803 1-9 file, "
                                                                "or a legacy-map label); refused"})
                    if 29 in counts:
                        ok = False
                        failures.append({"what": mname, "why": "identifier 29 present: this is a v10 carve, not v11; "
                                                                "read labels/, not labels_v10/"})
                    if scheme == "v11_pelvis":
                        extra = sorted(set(ids) - {0, lab["sacrum"], lab["left_hip"], lab["right_hip"]})
                        if extra:
                            ok = False
                            failures.append({"what": mname, "why": f"pelvis file holds ids {extra} beyond sacrum/hips; "
                                                                    "not a post-processed Dataset803 pelvis"})
                    names = {v: k for k, v in lab.items() if v != 29}
                    names = {i: names.get(i, f"unknown_{i}") for i in ids if i != 0}
                    mrec["checks"]["ids_named"] = {str(i): names[i] for i in ids if i != 0}
                except Exception as exc:  # noqa: BLE001
                    ok = False
                    failures.append({"what": mname, "why": f"labels_for raised: {exc}"})
        unknown = sorted(i for i, n in names.items() if n.startswith("unknown_"))
        if unknown:
            mrec["checks"]["unknown_ids"] = unknown
        if not ok:
            mrec["present"] = False
            mrec["refused"] = True
            evid["masks"][mname] = mrec
            evid["inputs"][f"mask_{mname}_refused"] = {"source": src, **(placer.sha(sp) or {})}
            continue
        dst = case_dir / "masks" / f"{mname}.nii.gz"
        if mrec.get("link_mode") != "relabelled_copy_same_affine":
            mode = placer.place(sp, dst)
            mrec["placed_as"], mrec["link_mode"] = rel(dst), mode
        desc = itksnap_descriptor(ids, names, f"{mname}: {SCHEME_TITLE[scheme]}")
        ctbl = slicer_ctbl(ids, names, f"{mname}: {SCHEME_TITLE[scheme]}")
        write_if_changed(case_dir / "labels" / f"{mname}.txt", desc)
        write_if_changed(case_dir / "labels" / f"{mname}.ctbl", ctbl)
        mrec["descriptor"] = f"labels/{mname}.txt"
        mrec["ctbl"] = f"labels/{mname}.ctbl"
        mrec["names"] = {str(i): names[i] for i in ids if i != 0}
        evid["masks"][mname] = mrec
        evid["inputs"][f"mask_{mname}"] = {"source": src, "placed_as": mrec["placed_as"], "link_mode": mrec["link_mode"],
                                          **(placer.sha(sp) or {})}
        present[mname] = True
        masks_spec.append({"name": mname, "path": mrec["placed_as"], "ctbl": mrec["ctbl"]})
        if mname == "pelvis803":
            pj = Path(r.get("pelvis_json") or sp.with_suffix("").with_suffix(".json"))
            if pj.exists():
                try:
                    J = json.loads(pj.read_text(encoding="utf-8-sig"))
                    mrec["sidecar"] = {k: J.get(k) for k in ("status", "sacrum_top_S_mm", "sacrum_height_S_mm",
                                                              "left_hip_crest_top_S_mm", "right_hip_crest_top_S_mm",
                                                              "laterality", "pelvis_present", "scheme_detected")}
                    evid["inputs"]["pelvis803_json"] = {"source": str(pj), **(placer.sha(pj) or {})}
                except Exception as exc:  # noqa: BLE001
                    mrec["sidecar"] = {"unreadable": str(exc)}

    # --- radiographs
    xr_items = collect_xr(r, args)
    if evid["case"]["paired"] and not xr_items:
        failures.append({"what": "xr", "why": "census says paired (has_xr) but no radiograph or pose was found; pass "
                                              "xr_paths or --carmlspine-root / --cobra-root"})
    evid["xr"] = write_xr(case_dir, r, xr_items, placer, evid, failures)
    if xr_items:
        evid["case"]["paired"] = True

    # --- rules not run, hidden joins
    evid["rules_not_run"] = rules_not_run(r, present)
    evid["hidden"] = joins.for_case(r, evid)

    # --- also_in
    if also:
        write_if_changed(case_dir / ".also_in", "\n".join(also) + "\n")
    elif (case_dir / ".also_in").exists():
        (case_dir / ".also_in").unlink()

    # --- Slicer scene script + open commands
    xr_spec = [{"name": f"{x['view']}{'' if x['tag'] in ('', '_ref') else x['tag']}", "nifti": x.get("radiograph_nifti"),
                "tfm": x["tfm"]["file"], "source_world_lps_mm": x["source_world_lps_mm"], "pose_status": x["pose_status"]}
               for x in evid["xr"].get("items", []) if isinstance(x, dict) and "tfm" in x]
    spec = {"case": r["case_key"], "ct": ct_rel, "masks": masks_spec, "xr": xr_spec}
    script = SLICER_TEMPLATE.replace("__SPEC__", json.dumps(spec, sort_keys=True)).replace("__CASE__", r["case_key"]) \
        .replace("__VERSION__", TOOL_VERSION)
    write_if_changed(case_dir / "make_slicer_scene.py", script)
    cmds = {}
    if ct_rel:
        for m in masks_spec:
            cmds[f"itksnap_{m['name']}"] = f'itksnap -g "{ct_rel}" -s "{m["path"]}" -l "labels/{m["name"]}.txt"'
        if not masks_spec:
            cmds["itksnap"] = f'itksnap -g "{ct_rel}"'
    cmds["slicer"] = "Slicer --no-main-window --python-script make_slicer_scene.py   (then open case.mrb)"
    ptx = sorted(p.name for p in (case_dir / "xr").glob("xr_*_P.txt")) if (case_dir / "xr").exists() else []
    if ptx:
        cmds["imfusion"] = ("ImFusion Suite: open " + (ct_rel or "the CT") + ", then X-Ray & CT > import projection "
                            "matrix (OpenCV 3x4, world in LPS mm): " + ", ".join(f"xr/{p}" for p in ptx))
    write_if_changed(case_dir / "open_commands.json", canonical_json(cmds))

    # --- evidence.json (built_utc preserved when nothing else changed)
    ev_path = case_dir / "evidence.json"
    payload = json.loads(canonical_json(evid))
    payload["header"].pop("built_utc", None)
    payload_sha = sha256_bytes(canonical_json(payload))
    built = meta["built_utc"]
    if ev_path.exists():
        try:
            old = json.loads(ev_path.read_text(encoding="utf-8"))
            if old.get("header", {}).get("payload_sha256") == payload_sha:
                built = old["header"].get("built_utc", built)
        except Exception:  # noqa: BLE001
            pass
    evid["header"]["built_utc"] = built
    evid["header"]["payload_sha256"] = payload_sha
    write_if_changed(ev_path, canonical_json(evid))

    # --- README
    write_if_changed(case_dir / "README.md", readme_text(r, evid, primary, also, rules, masks_spec, ct_rel, cmds))

    # --- manifest row
    files = sorted(str(p.relative_to(case_dir)).replace(os.sep, "/") for p in case_dir.rglob("*")
                   if (p.is_file() or p.is_symlink()) and not p.is_dir())
    b_tree, b_ref = dir_sizes(case_dir)
    row = {"case_id": r["case_dir_name"], "type": primary, "also_in": ";".join(also), "paired": int(evid["case"]["paired"]),
           "has_xr": int(evid["case"]["paired"]),
           "flags": ";".join(evid["case"]["flags"]), "rules": ";".join(rules), "priority": 1 + len(also),
           "collection": r["collection"], "person_key": r["person_key"], "case_key": r["case_key"],
           "case_dir": f"{primary}/{r['case_dir_name']}", "tier": r.get("tier", ""), "count": r.get("count", ""),
           "anchor_source": r.get("anchor_source", ""), "stump_left": r.get("stump_left", ""),
           "stump_right": r.get("stump_right", ""), "s3_ratio": r.get("s3_ratio", ""),
           "xr_views": ";".join(evid["xr"].get("views", [])), "ct": ct_rel or "",
           "masks": ";".join(m["name"] for m in masks_spec), "n_masks": len(masks_spec),
           "n_failures": len(failures), "failures": " | ".join(f"{f['what']}: {f['why']}" for f in failures),
           "files": ";".join(files), "bytes_tree": b_tree, "bytes_referenced": b_ref,
           "stage1_status": "pending", "stage1_verdict": "", "stage2_status": "pending", "stage2_verdict": "",
           "built_utc": built, "prereg_sha256": meta["prereg_sha256"], "prereg_status": meta["prereg_status"],
           "git_sha": meta["git_sha"] or "", "tool": TOOL_NAME, "tool_version": TOOL_VERSION,
           "registry_subtype": r.get("registry_subtype", ""), "prior_subtype": r.get("prior_subtype", ""),
           "truth_tier": r.get("truth_tier", "")}
    return row


def dir_sizes(d: Path):
    """(bytes the tree itself holds, bytes including symlink targets)."""
    tree = ref = 0
    for p in d.rglob("*"):
        try:
            st = p.lstat()
        except OSError:
            continue
        if stat.S_ISLNK(st.st_mode):
            try:
                ref += p.stat().st_size
            except OSError:
                pass
        elif stat.S_ISREG(st.st_mode):
            tree += st.st_size
            ref += st.st_size
    return tree, ref


def readme_text(r, evid, primary, also, rules, masks_spec, ct_rel, cmds) -> str:
    c = evid["case"]
    L = [f"# {r['case_key']} -- {primary}", "",
         f"Collection `{r['collection']}`, case `{r['case_id']}`, person `{r['person_key']}`"
         + (f", tier {r['tier']}" if r.get("tier") else "") + f". Paired radiographs: {'yes' if c['paired'] else 'no'}.",
         "", f"**Primary type: {primary}** -- {TYPE_MEANING[primary]}."]
    if also:
        L.append("Also flagged as: " + ", ".join(f"`{t}`" for t in also) +
                 " (this directory is the only copy; the other type folders point here through ALSO_IN.tsv).")
    L += ["", "## Why it was flagged", ""]
    L.append(f"- flags: {', '.join(f'`{f}`' for f in c['flags']) or '(none recorded)'}")
    L.append(f"- rules that raised it: {', '.join(rules) or '(none)'}")
    cnt = r.get("count", "")
    L.append(f"- rule 1 (rib-free count): count = `{cnt or 'blank'}`, anchor = `{r.get('anchor_source') or 'not stated'}`"
             + (f", most cranial rib-free body = `{r['last_rib_level']}`" if not blank(r.get("last_rib_level")) else ""))
    if r.get("_rule2"):
        L.append("- rule 2 (pelvis / sacral shape), scored, no validated threshold: " +
                 ", ".join(f"{k} = {v}" for k, v in r["_rule2"].items() if not blank(v)))
    L.append(f"- rule 3 (lowest rib against the rib above): left `{r.get('stump_left') or '-'}`, right "
             f"`{r.get('stump_right') or '-'}`, S3 ratio `{r.get('s3_ratio') or '-'}`")
    mr = evid["masks"].get("moller_ribs", {})
    if mr.get("rib_measurements"):
        L.append("  - Moller rows (variant, vertebra, side, length mm, at border, last):")
        for row in mr["rib_measurements"][:16]:
            L.append(f"    - {row.get('variant')}, {row.get('vertebra_name') or row.get('vertebra')}, {row.get('side')}, "
                     f"{float(row['rib_length']):.1f}, border={row.get('seg_at_border')}, last={row.get('is_last_v')}"
                     if row.get("rib_length") not in (None, "") else f"    - {row}")
    L += ["", "## Rules that could not run", ""]
    for x in evid["rules_not_run"]:
        L.append(f"- {x['rule']}: {x['why']}")
    if not evid["rules_not_run"]:
        L.append("- every rule had its inputs")
    L += ["", "## What to look at", ""]
    for t in [primary] + also:
        for s in LOOK_AT[t]:
            L.append(f"- ({t}) {s}")
    if evid["failures"]:
        L += ["", "## Failures on this case", ""]
        for f in evid["failures"]:
            L.append(f"- **{f['what']}**: {f['why']}")
    L += ["", "## Files", ""]
    if ct_rel:
        ci = evid["inputs"].get("ct", {})
        L.append(f"- `{ct_rel}` -- the CT ({ci.get('link_mode')}; shape {ci.get('shape')}, zooms {ci.get('zooms')}, "
                 f"axes {ci.get('axcodes')}); never rewritten or reoriented")
    else:
        L.append("- CT: **missing** (see failures)")
    for m in masks_spec:
        mm = evid["masks"][m["name"]]
        L.append(f"- `{m['path']}` -- {mm['scheme_title']}; ids {mm['ids']}; descriptor `labels/{m['name']}.txt`, "
                 f"Slicer `labels/{m['name']}.ctbl`")
    for nm, mm in evid["masks"].items():
        if not mm.get("present") and nm not in [m["name"] for m in masks_spec]:
            L.append(f"- masks/{nm}: absent" + (" (refused, see failures)" if mm.get("refused") else ""))
    if evid["inputs"].get("ts_roi"):
        L.append("- `masks/ts_roi/` -- per-structure TotalSegmentator files (no hips)")
    for x in evid["xr"].get("items", []):
        if isinstance(x, dict) and "tfm" in x:
            L.append(f"- radiograph {x['view']}{x['tag'] if x['tag'] not in ('', '_ref') else ''}: "
                     f"`{x.get('radiograph_nifti') or '(pixels not converted)'}`, transform `{x['tfm']['file']}`, "
                     f"projection `{x['P_txt']['file']}`, pose status **{x['pose_status']}**")
        elif isinstance(x, dict) and x.get("file"):
            L.append(f"- `{x['file']}`" + (f" -- {x['note']}" if x.get("note") else ""))
    if evid["xr"].get("pose_status") == "stale_px_mm_needs_refit":
        L.append("- **Pose status: stale.** Fit at 0.1465 mm/px against a 0.150 mm/px panel; good for orientation "
                 "in the viewer, not for a measurement (PREREG section 6).")
    L += ["- `evidence.json` -- the census row, every input with its sha256, the mask id sets and checks",
          "- `make_slicer_scene.py` -- builds and saves `case.mrb` inside Slicer", "",
          "## Open it", "", "```"]
    for k, v in cmds.items():
        L.append(f"# {k}\n{v}")
    L += ["```", "", "## Notes", "",
          "- Every volume is the source file itself (link or byte copy). Analysis canonicalised nothing here; the "
          "viewer shows the CT in its stored orientation.",
          "- Mask ids are named per scheme (see each descriptor's header); an id the scheme does not know is shown as "
          "`unknown_<id>` and listed in evidence.json.",
          "- Calls made earlier by other labellers and readers are withheld from this page and from the review "
          "screens; they sit under `hidden` in evidence.json for the audit table only.",
          f"- Built by {TOOL_NAME} v{TOOL_VERSION}, PREREG {evid['header']['prereg_status']} "
          f"sha256 {evid['header']['prereg_sha256'][:12]}..., repository {str(evid['header'].get('git_sha'))[:12]}."]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------------------------------- root files
MANIFEST_COLS = ["case_id", "type", "also_in", "paired", "has_xr", "flags", "rules", "priority", "collection", "person_key",
                 "case_key", "case_dir", "tier", "count", "anchor_source", "stump_left", "stump_right", "s3_ratio",
                 "xr_views", "ct", "masks", "n_masks", "n_failures", "failures", "files", "bytes_tree",
                 "bytes_referenced", "stage1_status", "stage1_verdict", "stage2_status", "stage2_verdict",
                 "built_utc", "prereg_sha256", "prereg_status", "git_sha", "tool", "tool_version",
                 "registry_subtype", "prior_subtype", "truth_tier"]


def write_manifest(root: Path, rows: list) -> None:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=MANIFEST_COLS, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for row in sorted(rows, key=lambda x: (TYPES.index(x["type"]), x["case_id"])):
        w.writerow({k: ("" if v is None else v) for k, v in row.items()})
    write_if_changed(root / "manifest.tsv", buf.getvalue())
    tb = "type\trank\tmeaning\n" + "".join(f"{t}\t{i}\t{TYPE_MEANING[t]}\n" for i, t in enumerate(TYPES))
    write_if_changed(root / "types.tsv", tb)
    fb = "case_id\ttype\twhat\twhy\n"
    for row in sorted(rows, key=lambda x: x["case_id"]):
        for f in [x for x in row["failures"].split(" | ") if x]:
            what, _, why = f.partition(": ")
            fb += f"{row['case_id']}\t{row['type']}\t{what}\t{why}\n"
    write_if_changed(root / "FAILURES.tsv", fb)
    # ALSO_IN pointers per type
    for t in TYPES:
        pts = [(row["case_id"], row["type"]) for row in rows if t in row["also_in"].split(";")]
        p = root / t / "ALSO_IN.tsv"
        if pts:
            write_if_changed(p, "case_id\thoused_under\n" + "".join(f"{c}\t{h}/{c}\n" for c, h in sorted(pts)))
        elif p.exists():
            p.unlink()


def write_sizes(root: Path, rows: list, zips: dict) -> None:
    per = {}
    for row in rows:
        d = per.setdefault(row["type"], {"n": 0, "tree": 0, "ref": 0})
        d["n"] += 1
        d["tree"] += int(row["bytes_tree"])
        d["ref"] += int(row["bytes_referenced"])
    L = ["# SIZES", "", "Bytes per type. `tree` counts the bytes the review tree itself holds (symlinks count 0); "
         "`referenced` follows the links to the CTs and masks. Zips are written beside each type directory with "
         "`--zip` and dereference every link.", "",
         "| type | cases | tree bytes | referenced bytes | zip bytes |", "|---|---:|---:|---:|---:|"]
    tt = tr = tz = 0
    for t in TYPES:
        d = per.get(t)
        if not d:
            continue
        z = zips.get(t, {}).get("bytes", 0)
        tt += d["tree"]
        tr += d["ref"]
        tz += z
        L.append(f"| {t} | {d['n']} | {d['tree']:,} | {d['ref']:,} | {z:,} |")
    L += ["", f"Total without zips: tree {tt:,} bytes ({tt / 1e9:.2f} GB), referenced {tr:,} bytes ({tr / 1e9:.2f} GB).",
          f"Total with zips: tree {tt + tz:,} bytes ({(tt + tz) / 1e9:.2f} GB), referenced {tr + tz:,} bytes "
          f"({(tr + tz) / 1e9:.2f} GB).", ""]
    write_if_changed(root / "SIZES.md", "\n".join(L))


def write_index(root: Path, rows: list, meta: dict) -> None:
    cols = ["type", "case_id", "collection", "paired", "flags", "rules", "count", "anchor_source", "stump_left",
            "stump_right", "s3_ratio", "also_in", "masks", "xr_views", "n_failures", "bytes_referenced",
            "stage1_status", "stage2_status"]
    body = []
    for row in sorted(rows, key=lambda x: (TYPES.index(x["type"]), x["case_id"])):
        tds = []
        for c in cols:
            v = html.escape(str(row.get(c, "")))
            if c == "case_id":
                v = f'<a href="{html.escape(row["case_dir"])}/README.md">{v}</a>'
            tds.append(f"<td>{v}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    counts = {}
    for row in rows:
        counts[row["type"]] = counts.get(row["type"], 0) + 1
    summary = " &middot; ".join(f"{t}: {counts[t]}" for t in TYPES if t in counts)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Transitional review tree</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{{--bg:#fff;--fg:#1b1b1b;--mut:#666;--line:#ddd;--head:#f3f3f3;--acc:#0b5cad}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151515;--fg:#eee;--mut:#aaa;--line:#333;--head:#222;--acc:#7db4ec}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif}}
h1{{font-size:20px;margin:0 0 4px}} .mut{{color:var(--mut)}} input{{padding:6px;margin:8px 0;width:min(480px,100%)}}
table{{border-collapse:collapse;width:100%;font-size:13px}} th,td{{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}}
th{{background:var(--head);cursor:pointer;position:sticky;top:0}} th.asc::after{{content:" \\25B2"}} th.desc::after{{content:" \\25BC"}}
a{{color:var(--acc)}} .wrap{{overflow-x:auto}}
</style></head><body>
<h1>Transitional-vertebra review tree</h1>
<div class="mut">{len(rows)} cases &middot; {summary} &middot; PREREG {html.escape(meta['prereg_status'])} {html.escape(meta['prereg_sha256'][:12])} &middot; {html.escape(TOOL_NAME)} v{TOOL_VERSION}</div>
<input id="q" placeholder="filter (type, collection, flag, case) ..." oninput="filt()">
<div class="wrap"><table id="t"><thead><tr>{''.join(f'<th onclick="sortBy({i})">{html.escape(c)}</th>' for i, c in enumerate(cols))}</tr></thead>
<tbody>{''.join(body)}</tbody></table></div>
<script>
var dir={{}};
function sortBy(i){{var t=document.getElementById('t'),tb=t.tBodies[0],rows=[].slice.call(tb.rows);dir[i]=!dir[i];
var num=rows.every(function(r){{var v=r.cells[i].textContent.trim();return v===''||!isNaN(parseFloat(v))}});
rows.sort(function(a,b){{var x=a.cells[i].textContent.trim(),y=b.cells[i].textContent.trim();
if(num){{x=parseFloat(x)||0;y=parseFloat(y)||0;return dir[i]?x-y:y-x}}return dir[i]?x.localeCompare(y):y.localeCompare(x)}});
rows.forEach(function(r){{tb.appendChild(r)}});[].forEach.call(t.tHead.rows[0].cells,function(c,j){{c.className=j===i?(dir[i]?'asc':'desc'):''}})}}
function filt(){{var q=document.getElementById('q').value.toLowerCase();[].forEach.call(document.getElementById('t').tBodies[0].rows,function(r){{r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'':'none'}})}}
</script></body></html>
"""
    write_if_changed(root / "index.html", page)


def write_zips(root: Path, rows: list) -> dict:
    """<TYPE>.zip beside each type dir (links dereferenced, deterministic entries) + sha256 manifests."""
    out = {}
    for t in TYPES:
        tdir = root / t
        if not any(row["type"] == t for row in rows):
            continue
        entries = sorted(p for p in tdir.rglob("*") if p.is_file())
        zpath = root / f"{t}.zip"
        sums = []
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for p in entries:
                arc = f"{t}/{p.relative_to(tdir).as_posix()}"
                data = p.read_bytes()
                zi = zipfile.ZipInfo(arc, date_time=(1980, 1, 1, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                zf.writestr(zi, data)
                sums.append(f"{sha256_bytes(data)}  {arc}")
        data = buf.getvalue()
        write_if_changed(zpath, data)
        write_if_changed(root / f"{t}.zip.sha256", f"{sha256_bytes(data)}  {t}.zip\n")
        write_if_changed(root / f"{t}.zip.SHA256SUMS", "\n".join(sums) + "\n")
        out[t] = {"bytes": len(data), "sha256": sha256_bytes(data), "n_files": len(entries)}
    return out


# ----------------------------------------------------------------------------------------------------- build
def build(args) -> int:
    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    prereg = Path(args.prereg).expanduser().resolve()
    if not prereg.exists():
        print(f"FATAL: PREREG not found at {prereg}", file=sys.stderr)
        return 1
    ptext = prereg.read_text(encoding="utf-8", errors="replace")
    git_sha, git_err = git_head(REPO)
    census = Path(args.census).expanduser().resolve()
    meta = {"tool": TOOL_NAME, "tool_version": TOOL_VERSION, "prereg_path": str(prereg),
            "prereg_sha256": sha256_file(prereg), "prereg_status": prereg_status_of(ptext), "git_sha": git_sha,
            "git_sha_error": git_err, "built_utc": utc_now(), "census_path": str(census),
            "census_sha256": sha256_file(census), "root": str(root), "copy": bool(args.copy)}
    write_if_changed(root / "PREREG_rules.md", prereg.read_bytes())
    placer = Placer(args.copy, args.hash_limit_mb)
    ostk, ostk_err = import_ostk(args.ostk_path)
    S, S_err = import_spineps_ids()
    ctx = {"ostk": ostk, "ostk_error": ostk_err, "spineps_ids": S, "spineps_ids_error": S_err,
           "ts_map": TS_DEFAULT_CLASS_MAP, "v11_names": {}}
    joins = Joins(args, placer)
    rows_in, found, cols = read_census(census)
    print(f"census {census}: {len(rows_in)} rows; columns recognised: {sorted(found)}; "
          f"missing: {sorted(set(ALIASES) - set(found))}")
    if ostk is None:
        print(f"WARNING: {ostk_err}: CTSP and Dataset803 masks will be refused", file=sys.stderr)
    if S is None:
        print(f"WARNING: {S_err}: SPINEPS guard cannot run", file=sys.stderr)
    only_cases = set(split_list(args.cases)) if args.cases else None
    only_types = set(split_list(args.types)) if args.types else None
    rows_out = []
    n_fail = 0
    for r in rows_in:
        norm_case(r)
        if only_cases and r["case_key"] not in only_cases and r["case_dir_name"] not in only_cases:
            continue
        if only_types and types_of(r)[0] not in only_types:
            continue
        if args.limit and len(rows_out) >= args.limit:
            break
        try:
            row = build_case(r, args, root, placer, meta, ctx, joins)
        except Exception as exc:  # noqa: BLE001
            import traceback
            row = {"case_id": r["case_dir_name"], "type": types_of(r)[0], "also_in": "", "paired": 0, "flags": r.get("flags", ""),
                   "rules": "", "priority": 0, "collection": r["collection"], "person_key": r["person_key"],
                   "case_key": r["case_key"], "case_dir": f"{types_of(r)[0]}/{r['case_dir_name']}", "n_failures": 1,
                   "failures": f"builder: {type(exc).__name__}: {exc}", "files": "", "bytes_tree": 0, "bytes_referenced": 0,
                   "stage1_status": "pending", "stage2_status": "pending", "built_utc": meta["built_utc"],
                   "prereg_sha256": meta["prereg_sha256"], "prereg_status": meta["prereg_status"], "git_sha": git_sha or "",
                   "tool": TOOL_NAME, "tool_version": TOOL_VERSION}
            traceback.print_exc()
        rows_out.append(row)
        if int(row.get("n_failures", 0)):
            n_fail += 1
        print(f"  {row['type']:24s} {row['case_id']:24s} masks={row.get('masks', '')} xr={row.get('xr_views', '')} "
              f"failures={row.get('n_failures', 0)}")
    write_manifest(root, rows_out)
    zips = write_zips(root, rows_out) if args.zip else {}
    write_sizes(root, rows_out, zips)
    write_index(root, rows_out, meta)
    with open(root / RUN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({**meta, "n_cases": len(rows_out), "n_cases_with_failures": n_fail, "zips": zips,
                            "argv": sys.argv[1:]}, sort_keys=True) + "\n")
    print(f"wrote {len(rows_out)} cases under {root}; {n_fail} with failures (FAILURES.tsv)")
    return 2 if n_fail else 0


# ----------------------------------------------------------------------------------------------------- verify
def verify_tree(root: Path, expect_prereg_sha: str | None = None) -> list:
    """Check a built tree the way the self-test does. Returns a list of problems (empty = clean)."""
    import nibabel as nib
    probs = []
    root = Path(root)
    mp = root / "manifest.tsv"
    if not mp.exists():
        return [f"{mp} missing"]
    with open(mp, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for req in ("case_id", "type", "case_dir", "files", "prereg_sha256", "built_utc", "tool", "tool_version"):
        if rows and req not in rows[0]:
            probs.append(f"manifest lacks column {req}")
    seen = set()
    for row in rows:
        cid = row["case_id"]
        if cid in seen:
            probs.append(f"{cid}: duplicate case_id")
        seen.add(cid)
        cdir = root / row["case_dir"]
        if not cdir.is_dir():
            probs.append(f"{cid}: case_dir missing {row['case_dir']}")
            continue
        for rel in [x for x in row.get("files", "").split(";") if x]:
            p = cdir / rel
            if not (p.exists() or p.is_symlink()):
                probs.append(f"{cid}: listed file missing {rel}")
            elif p.is_symlink() and not p.exists():
                probs.append(f"{cid}: dangling symlink {rel}")
        for nm in ("README.md", "evidence.json", "make_slicer_scene.py"):
            if not (cdir / nm).exists():
                probs.append(f"{cid}: {nm} missing")
        try:
            ev = json.loads((cdir / "evidence.json").read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            probs.append(f"{cid}: evidence.json unreadable: {exc}")
            continue
        h = ev.get("header", {})
        for k in ("prereg_sha256", "prereg_status", "git_sha", "tool", "tool_version", "built_utc"):
            if k not in h:
                probs.append(f"{cid}: evidence header lacks {k}")
        if expect_prereg_sha and h.get("prereg_sha256") != expect_prereg_sha:
            probs.append(f"{cid}: prereg_sha256 mismatch")
        for k, v in ev.get("inputs", {}).items():
            if isinstance(v, dict) and "sha256" not in v:
                probs.append(f"{cid}: input {k} has no sha256 field")
        readme = (cdir / "README.md").read_text(encoding="utf-8")
        for bad in ("registry", "origin"):
            if re.search(rf"\b{bad}\b", readme, flags=re.I):
                probs.append(f"{cid}: README contains the word '{bad}'")
        # descriptor ids == np.unique(mask)
        for m in sorted((cdir / "masks").glob("*.nii.gz")) if (cdir / "masks").exists() else []:
            desc = cdir / "labels" / (m.name[: -len(".nii.gz")] + ".txt")
            ctbl = cdir / "labels" / (m.name[: -len(".nii.gz")] + ".ctbl")
            if not desc.exists() or not ctbl.exists():
                probs.append(f"{cid}: descriptor missing for {m.name}")
                continue
            ids_desc = {int(l.split()[0]) for l in desc.read_text(encoding="utf-8").splitlines()
                        if l.strip() and not l.startswith("#")}
            ids_ctbl = {int(l.split()[0]) for l in ctbl.read_text(encoding="utf-8").splitlines()
                        if l.strip() and not l.startswith("#")}
            ids_mask = {int(i) for i in np.unique(np.asanyarray(nib.load(str(m)).dataobj))}
            if ids_desc != ids_mask:
                probs.append(f"{cid}: {desc.name} ids {sorted(ids_desc)} != mask ids {sorted(ids_mask)}")
            if ids_ctbl != ids_mask:
                probs.append(f"{cid}: {ctbl.name} ids != mask ids")
            rec = ev.get("masks", {}).get(m.name[: -len(".nii.gz")], {})
            if rec.get("ids") and set(rec["ids"]) != ids_mask:
                probs.append(f"{cid}: evidence ids for {m.name} differ from the file")
        # CT affine equals the source affine (never reoriented)
        ci = ev.get("inputs", {}).get("ct")
        if ci and row.get("ct") and str(ci.get("source", "")).endswith((".nii", ".nii.gz")) and Path(ci["source"]).exists():
            a_src = nib.load(ci["source"]).affine
            a_dst = nib.load(str(cdir / row["ct"])).affine
            if not np.allclose(a_src, a_dst):
                probs.append(f"{cid}: CT affine differs from the source (reoriented?)")
        if row.get("also_in"):
            al = cdir / ".also_in"
            if not al.exists() or al.read_text().split() != row["also_in"].split(";"):
                probs.append(f"{cid}: .also_in does not match manifest also_in")
        # radiograph geometry round trip
        for x in ev.get("xr", {}).get("items", []):
            if not (isinstance(x, dict) and "tfm" in x):
                continue
            tfm = cdir / x["tfm"]["file"]
            ptxt = cdir / x["P_txt"]["file"]
            if not tfm.exists() or not ptxt.exists():
                probs.append(f"{cid}: xr files missing for {x['view']}")
                continue
            P = np.loadtxt(str(ptxt))
            if P.shape != (3, 4):
                probs.append(f"{cid}: {ptxt.name} is not 3x4")
            try:
                import SimpleITK as sitk
                T = sitk.AffineTransform(sitk.ReadTransform(str(tfm)))
                Rm = np.array(T.GetMatrix()).reshape(3, 3)
                if not np.allclose(Rm, np.array(x["R"]), atol=1e-6) or not np.allclose(T.GetTranslation(), x["t"], atol=1e-6):
                    probs.append(f"{cid}: {tfm.name} does not hold R, t")
            except Exception as exc:  # noqa: BLE001
                probs.append(f"{cid}: {tfm.name} unreadable by SimpleITK: {exc}")
            if x.get("radiograph_nifti") and (cdir / x["radiograph_nifti"]).exists():
                img = nib.load(str(cdir / x["radiograph_nifti"]))
                A_ras = img.affine
                A_lps = np.diag([-1.0, -1.0, 1.0, 1.0]) @ A_ras
                K = np.array(x["K"])
                for (i, j) in ((0, 0), (5, 7), (img.shape[0] - 1, img.shape[1] - 1)):
                    pc = A_lps @ np.array([i, j, 0, 1.0])
                    uv = K @ pc[:3]
                    uv = uv[:2] / uv[2]
                    if not np.allclose(uv, [i + 0.5, j + 0.5], atol=1e-6):
                        probs.append(f"{cid}: radiograph slice does not re-project to pixel centres ({uv} vs {(i + 0.5, j + 0.5)})")
                        break
                Rw = np.array(x["R"])
                tw = np.array(x["t"])
                src_w = np.array(x["source_world_lps_mm"])
                # R comes from a float32 fit; R R^T - I is ~1e-7, which over |t| ~ 750 mm is ~1e-4 mm
                if not np.allclose(Rw @ src_w + tw, 0, atol=1e-3):
                    probs.append(f"{cid}: source position is not the camera origin (residual "
                                 f"{np.abs(Rw @ src_w + tw).max():.2e} mm)")
    for nm in ("index.html", "SIZES.md", "types.tsv", "FAILURES.tsv", "PREREG_rules.md"):
        if not (root / nm).exists():
            probs.append(f"root file missing: {nm}")
    for z in root.glob("*.zip"):
        s = (root / (z.name + ".sha256")).read_text().split()[0]
        if sha256_file(z) != s:
            probs.append(f"{z.name}: sha256 mismatch")
        with zipfile.ZipFile(z) as zf:
            names = set(zf.namelist())
            sums = (root / (z.name + ".SHA256SUMS")).read_text().splitlines()
            for line in sums:
                sh, _, arc = line.partition("  ")
                if arc not in names:
                    probs.append(f"{z.name}: {arc} listed but not in zip")
                elif sha256_bytes(zf.read(arc)) != sh:
                    probs.append(f"{z.name}: {arc} sha mismatch inside the zip")
    return probs


def tree_snapshot(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if rel == RUN_LOG:
            continue
        if p.is_symlink():
            out[rel] = "link:" + os.readlink(str(p))
        elif p.is_file():
            out[rel] = sha256_file(p)
    return out


# ----------------------------------------------------------------------------------------------------- self-test
def _write_nifti(path: Path, arr: np.ndarray, affine: np.ndarray, dtype=np.uint8) -> None:
    import nibabel as nib
    path.parent.mkdir(parents=True, exist_ok=True)
    img = nib.Nifti1Image(np.asarray(arr).astype(dtype), affine)
    nib.save(img, str(path))


def _png_bytes(arr: np.ndarray) -> bytes:
    import struct
    import zlib
    h, w = arr.shape
    raw = b"".join(b"\x00" + arr[y].astype(np.uint8).tobytes() for y in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def _write_fake_dicom(path: Path, pix: np.ndarray, angle: float) -> bool:
    try:
        import pydicom
        from pydicom.dataset import FileDataset, FileMetaDataset
        from pydicom.uid import ExplicitVRLittleEndian, generate_uid
    except Exception:  # noqa: BLE001
        return False
    fm = FileMetaDataset()
    fm.MediaStorageSOPClassUID = pydicom.uid.XRayAngiographicImageStorage
    fm.MediaStorageSOPInstanceUID = generate_uid()
    fm.TransferSyntaxUID = ExplicitVRLittleEndian
    ds = FileDataset(str(path), {}, file_meta=fm, preamble=b"\0" * 128)
    ds.Modality = "XA"
    ds.Rows, ds.Columns = pix.shape
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PositionerPrimaryAngle = angle
    ds.DistanceSourceToDetector = 1140.0
    ds.DistanceSourceToPatient = 745.0
    ds.KVP = 79.0
    ds.PixelSpacing = [1.0, 1.0]
    ds.PixelData = pix.astype(np.uint16).tobytes()
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        ds.save_as(str(path), enforce_file_format=True)
    except TypeError:                                   # pydicom < 3
        ds.save_as(str(path), write_like_original=False)
    return True


def _column(shape, order, slab=5, gap=1, top=61, sacrum_h=14, box_frac=(0.25, 0.75)):
    """A synthetic vertebral column in a canonical (x, y, s) array, s increasing cranially: `order` cranial first,
    each body a `slab`-thick box, a 1-voxel disc (100 + the body above) in every gap, the sacrum `sacrum_h` thick."""
    a = np.zeros(shape, np.int32)
    bx = slice(int(shape[0] * box_frac[0]), int(shape[0] * box_frac[1]))
    by = slice(int(shape[1] * box_frac[0]), int(shape[1] * box_frac[1]))
    s = top
    for v in order:
        h = sacrum_h if v == 26 else slab
        a[bx, by, s - h:s] = v
        s -= h
        if v != 26 and gap:
            a[bx, by, s - gap:s] = 100 + v
            s -= gap
    return a


def _to_pir(c: np.ndarray) -> np.ndarray:
    """Canonical (x, y, s) -> the (P, I, R) voxel order the CTSP CTs are stored in: i = y, j = reversed s, k = x."""
    return np.ascontiguousarray(np.transpose(c, (1, 2, 0))[:, ::-1, :])


def _ctd_for(arr: np.ndarray, affine: np.ndarray, labels) -> list:
    """A TPTBox-style POI json (header zoom/origin/rotation + voxel points) whose points sit at instance centroids."""
    zoom = np.sqrt((affine[:3, :3] ** 2).sum(0))
    rot = affine[:3, :3] / zoom
    pts = {}
    for v in labels:
        w = np.argwhere(arr == v)
        if len(w):
            pts[str(int(v))] = {"50": [float(x) for x in w.mean(0)]}
    return [{"direction": ["P", "I", "R"], "zoom": zoom.tolist(), "origin": affine[:3, 3].tolist(),
             "rotation": rot.tolist(), "shape": list(arr.shape), "format": "POI"}, pts]


def make_fake_inputs(base: Path) -> Path:
    """Four synthetic cases; returns the census path. Voxels are 2 mm so a body is ~16 mL (the guard's size test)."""
    src = base / "src"
    src.mkdir(parents=True, exist_ok=True)
    cshape = (40, 40, 64)                                  # canonical (x, y, s)
    aff_pir = np.array([[0, 0, 2.0, -40.0], [-2.0, 0, 0, 40.0], [0, -2.0, 0, 130.0], [0, 0, 0, 1.0]])
    aff_ras = np.diag([2.0, 2.0, 2.0, 1.0])
    aff_ras[:3, 3] = [-40.0, -40.0, 0.0]
    rng = np.random.default_rng(0)
    order = [19, 20, 21, 22, 23, 24, 25, 26]
    inst_c = _column(cshape, order)
    sem_c = np.zeros(cshape, np.int32)
    for k, v in enumerate([41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 70, 71, 72, 73, 74, 100]):
        sem_c[10:30, 10:30, 3 + 3 * k:6 + 3 * k] = v
    ts_c = _column(cshape, [32, 31, 30, 29, 28, 27, 26, 25], gap=0, sacrum_h=6)
    ts_c[ts_c == 25] = 25
    ts_c[0:5, 10:30, 2:20] = 77
    ts_c[-5:, 10:30, 2:20] = 78
    ts_c[0:3, 10:30, 0:2] = 75
    ts_c[-3:, 10:30, 0:2] = 76
    ts_c[2:5, 5:9, 50:56] = 102
    ts_c[-5:-2, 5:9, 50:56] = 115
    mol_c = inst_c.copy()
    mol_c[2:6, 5:9, 56:61] = 50           # rib of T11 (18 + 32) left of the column
    mol_c[-6:-2, 5:9, 56:61] = 51         # rib of T12 (19 + 32)
    mol_c[2:6, 5:9, 40:44] = 255          # an unassigned fragment
    pel_c = np.zeros(cshape, np.int32)
    pel_c[inst_c == 26] = 26
    pel_c[0:5, 10:30, 2:20] = 30
    pel_c[-5:, 10:30, 2:20] = 31
    gt_c = inst_c.copy()
    gt_c[gt_c >= 100] = 0
    gt_c[0:5, 10:30, 2:20] = 30
    gt_c[-5:, 10:30, 2:20] = 31
    gt_c[0:3, 10:30, 0:2] = 32
    gt_c[-3:, 10:30, 0:2] = 33
    gt_c[2:6, 5:9, 56:61] = 45            # rib_left_12
    gt_c[-6:-2, 5:9, 56:61] = 58          # rib_right_12
    gt_c[2:6, 5:9, 40:44] = 60            # rib_left_lumbar
    pshape = _to_pir(inst_c).shape

    # --- case A: ctsp 5 -> 0005, L6 + castellvi + stump, paired; everything stored P,I,R like the release CTs
    A = src / "A"
    _write_nifti(A / "0005_ct.nii.gz", rng.normal(0, 50, pshape).astype(np.float32), aff_pir, np.float32)
    inst_p = _to_pir(inst_c)
    _write_nifti(A / "CTSP_0005_seg-vert_msk.nii.gz", inst_p, aff_pir, np.uint16)
    _write_nifti(A / "CTSP_0005_seg-spine_msk.nii.gz", _to_pir(sem_c), aff_pir, np.uint16)
    (A / "CTSP_0005_ctd.json").write_text(json.dumps(_ctd_for(inst_p, aff_pir, order)))
    _write_nifti(A / "COLONOG_4.nii.gz", _to_pir(ts_c), aff_pir, np.uint8)
    (A / "class_map.json").write_text(json.dumps({str(k): v for k, v in TS_DEFAULT_CLASS_MAP.items()}))
    _write_nifti(A / "0005_rib-inst_msk.nii.gz", _to_pir(mol_c), aff_pir, np.uint8)
    (A / "0005_rib_measurements.csv").write_text(
        "collection,case_id,person_key,tier,ids_verdict,variant,rib_length,sr,seg_at_border,rib_volume,vertebra,"
        "side,is_last_v,vertebra_name,n_path_points\n"
        "ctsp,0005,ctsp:0005,1,verse_ok,upstream,161.6,False,False,100434,19,right,True,T12,20\n"
        "ctsp,0005,ctsp:0005,1,verse_ok,upstream,31.2,False,False,9000,19,left,True,T12,5\n"
        "ctsp,0005,ctsp:0005,1,verse_ok,upstream,180.1,False,False,120000,18,left,False,T11,24\n")
    (A / "_done").mkdir(exist_ok=True)
    (A / "_done" / "0005.measure.json").write_text(json.dumps({"ids_verdict": "verse_ok", "levels_upstream": {
        "rib_bearing": {"18": {"left": 1000, "right": 900}, "19": {"left": 60, "right": 800}}, "unassigned_rib_vox": 12}}))
    _write_nifti(A / "0005_pelvis.nii.gz", _to_pir(pel_c), aff_pir, np.uint8)
    (A / "0005_pelvis.json").write_text(json.dumps({"status": "ok", "sacrum_top_S_mm": 12.3, "pelvis_present": True}))
    _write_nifti(A / "0005_label.nii.gz", _to_pir(gt_c), aff_pir, np.uint8)
    pix = (rng.random((64, 64)) * 4000).astype(np.uint16)
    have_dcm = _write_fake_dicom(A / "0001.dcm", pix, 0.1)
    px = 300.0 / 64
    sid = 1140.0
    K = [[-sid / px, 0.0, 32.0], [0.0, sid / px, 32.0], [0.0, 0.0, 1.0]]
    th = np.deg2rad(3.0)
    Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
    R = (Rz @ np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]], float)).tolist()
    pose = {"K": K, "R": R, "t": [2.7, 2.9, 748.7], "edge_ncc": 0.37, "int_ncc": 0.23, "margin": 1.37,
            "case": "case0005", "view": "AP", "angle": 0.1, "sid": sid, "sod": 745.0, "px_mm": px, "kvp": 79.0,
            "frame": "0001.dcm", "tag": "_ref", "hypothesis": {"rot": 180, "mirror": -1}}
    (A / "case0005_AP_ref.json").write_text(json.dumps(pose))
    (A / "case0005_AP_ref.png").write_bytes(_png_bytes((rng.random((32, 48)) * 255).astype(np.uint8)))
    xr_paths = [str(A / "case0005_AP_ref.json")] + ([str(A / "0001.dcm")] if have_dcm else [])

    # --- case B: amos22 0203, four-count, raw SPINEPS ids (refused), legacy-id pelvis (refused), ts roi dir
    B = src / "B"
    _write_nifti(B / "amos_0203.nii.gz", rng.normal(0, 50, cshape).astype(np.float32), aff_ras, np.float32)
    raw = _column(cshape, [1, 2, 3, 4, 5, 6, 7], gap=0)
    _write_nifti(B / "amos_0203_seg-vert_msk.nii.gz", raw, aff_ras, np.uint16)
    _write_nifti(B / "amos_0203_seg-spine_msk.nii.gz", sem_c, aff_ras, np.uint16)
    roi = B / "ts"
    _write_nifti(roi / "sacrum.nii.gz", (inst_c == 26).astype(np.uint8), aff_ras, np.uint8)
    _write_nifti(roi / "vertebrae_L5.nii.gz", (inst_c == 24).astype(np.uint8), aff_ras, np.uint8)
    legacy = np.zeros(cshape, np.uint8)
    legacy[inst_c == 26] = 6
    legacy[0:5, 10:30, 2:20] = 7
    legacy[-5:, 10:30, 2:20] = 8
    _write_nifti(B / "amos_0203_pelvis_legacy.nii.gz", legacy, aff_ras, np.uint8)

    # --- case C: cobra A002, no_count, ts multilabel only, COBRA-style xr files
    C = src / "C"
    _write_nifti(C / "A002_ct.nii.gz", rng.normal(0, 50, cshape).astype(np.float32), aff_ras, np.float32)
    _write_nifti(C / "A002_ts.nii.gz", ts_c, aff_ras, np.uint8)
    (C / "projections.mha").write_bytes(b"ObjectType = Image\nNDims = 3\nDimSize = 2 2 2\nElementType = MET_UCHAR\n"
                                         b"ElementDataFile = LOCAL\n" + bytes(8))
    (C / "geometry.xml").write_text("<RTKThreeDCircularGeometry/>\n")
    (C / "overview_A002.png").write_bytes(_png_bytes((rng.random((16, 16)) * 255).astype(np.uint8)))

    # --- case D: ts s0001, T13 flag, CT path missing, VerSe-coded SPINEPS mask without a ctd
    D = src / "D"
    _write_nifti(D / "s0001_seg-vert_msk.nii.gz", inst_c, aff_ras, np.uint16)

    hdr = ["case_key", "collection", "case_id", "person_key", "tier", "count", "anchor_source", "flags", "stump_left",
           "stump_right", "s3_ratio", "rule2_top_to_crest_mm", "rule2_outside_flag", "prior_subtype",
           "registry_subtype", "truth_tier", "ct", "spineps_inst", "spineps_sem", "spineps_ctd", "spineps_ids", "ts",
           "ts_class_map", "moller_inst", "pelvis", "pelvis_json", "gt", "has_xr", "xr_paths"]
    rows = [
        ["ctsp:5", "ctsp", "5", "ctsp:0005", "1", "6", "ts_sacrum_union_s1", "L6;castellvi_II_IV_candidate;stump_left",
         "STUMP", "FULL", "0.19", "-11.2", "0", "L6", "L6", "read", str(A / "0005_ct.nii.gz"),
         str(A / "CTSP_0005_seg-vert_msk.nii.gz"), str(A / "CTSP_0005_seg-spine_msk.nii.gz"),
         str(A / "CTSP_0005_ctd.json"), "verse_coded", str(A / "COLONOG_4.nii.gz"), str(A / "class_map.json"),
         str(A / "0005_rib-inst_msk.nii.gz"), str(A / "0005_pelvis.nii.gz"), str(A / "0005_pelvis.json"),
         str(A / "0005_label.nii.gz"), "1", ";".join(xr_paths)],
        ["amos22:0203", "amos22", "amos_0203", "amos22:0203", "2", "4", "ts_sacrum_union_s1",
         "complete_sacralisation_candidate", "FULL", "FULL", "", "", "", "", "", "", str(B / "amos_0203.nii.gz"),
         str(B / "amos_0203_seg-vert_msk.nii.gz"), str(B / "amos_0203_seg-spine_msk.nii.gz"), "", "raw", str(roi), "",
         "", str(B / "amos_0203_pelvis_legacy.nii.gz"), "", "", "0", ""],
        ["cobra:A002", "cobra", "A002", "cobra:A002", "1", "no_count", "no_anchor: sacrum touches the caudal slice",
         "", "", "", "", "", "", "no_count", "no_count", "", str(C / "A002_ct.nii.gz"), "", "", "", "",
         str(C / "A002_ts.nii.gz"), "", "", "", "", "", "1",
         ";".join([str(C / "projections.mha"), str(C / "geometry.xml"), str(C / "overview_A002.png")])],
        ["ts:s0001", "ts", "s0001", "ts:s0001", "1", "5", "ts_sacrum_union_s1", "T13", "FULL", "FULL", "0.9", "", "",
         "", "T13", "single-labeller", str(D / "s0001_ct_MISSING.nii.gz"), str(D / "s0001_seg-vert_msk.nii.gz"), "",
         "", "verse_coded", "", "", "", "", "", "", "0", ""],
    ]
    cp = base / "fake_census.tsv"
    with open(cp, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(hdr)
        w.writerows(rows)
    return cp


def selftest(args) -> int:
    fails = []

    def check(cond, msg):
        (print("  ok   " + msg) if cond else (fails.append(msg), print("  FAIL " + msg)))

    keep = args.keep
    base = Path(args.selftest_dir).resolve() if args.selftest_dir else Path(tempfile.mkdtemp(prefix="review_tree_selftest_"))
    base.mkdir(parents=True, exist_ok=True)
    print(f"selftest in {base}")
    census = make_fake_inputs(base)
    root = base / "tree"
    ns = argparse.Namespace(**vars(args))
    ns.census, ns.root, ns.zip, ns.copy = str(census), str(root), True, args.copy
    ns.cases = ns.types = None
    ns.limit = 0
    rc1 = build(ns)
    check(rc1 == 2, f"first build exit code is 2 (failures were expected and reported), got {rc1}")
    snap1 = tree_snapshot(root)
    probs = verify_tree(root, sha256_file(Path(ns.prereg)))
    for p in probs:
        print("  verify: " + p)
    check(not probs, f"verify_tree clean ({len(probs)} problems)")
    with open(root / "manifest.tsv", encoding="utf-8", newline="") as f:
        rows = {r["case_id"]: r for r in csv.DictReader(f, delimiter="\t")}
    check(set(rows) == {"ctsp_0005", "amos22_0203", "cobra_A002", "ts_s0001"}, f"four cases, ids sanitised: {sorted(rows)}")
    a = rows.get("ctsp_0005", {})
    check(a.get("type") == "L6" and a.get("also_in") == "castellvi_II_IV;stump_rib", f"case A primary L6, also_in castellvi_II_IV;stump_rib (got {a.get('type')}, {a.get('also_in')})")
    check(a.get("case_key") == "ctsp:0005" and a.get("case_dir") == "L6/ctsp_0005", "case A key zfill(4) and case_dir L6/ctsp_0005")
    check(set(a.get("masks", "").split(";")) == {"spineps_inst", "spineps_sem", "ts_total", "moller_ribs", "pelvis803", "gt_v11"}, f"case A has all six masks: {a.get('masks')}")
    check(a.get("paired") == "1" and a.get("xr_views") == "AP", f"case A paired with view AP (got {a.get('xr_views')})")
    check(a.get("n_failures") == "0", f"case A has no failures: {a.get('failures')}")
    ev_a = json.loads((root / a["case_dir"] / "evidence.json").read_text(encoding="utf-8"))
    check(ev_a["masks"]["gt_v11"]["checks"]["labels_for"]["scheme"] == "v10" and
          ev_a["masks"]["pelvis803"]["checks"]["labels_for"]["scheme"] == "v10", "case A gt_v11 and pelvis803 resolved v10 through labels_for")
    check(ev_a["masks"]["spineps_inst"]["checks"]["guard"]["verdict"] in ("verse_ok", "misnamed_1_2_levels"), f"case A SPINEPS guard verdict {ev_a['masks']['spineps_inst']['checks']['guard'].get('verdict')}")
    check(ev_a["xr"]["pose_status"] == "ok", "case A (not carmlspine) pose status ok")
    check(ev_a["masks"]["moller_ribs"]["names"].get("50") == "rib_of_T11" and ev_a["masks"]["moller_ribs"]["names"].get("255") == "unassigned_rib", "Moller ids named rib_of_<vertebra> / unassigned")
    check(ev_a["hidden"].get("registry_subtype") == "L6" and "registry_subtype" not in ev_a["rules_row"], "prior/registry columns live only under hidden")
    check(all("sha256" in v for v in ev_a["inputs"].values()), "every input of case A carries a sha256")
    check(ev_a["header"]["prereg_status"] == "draft" and ev_a["header"]["prereg_sha256"] == sha256_file(Path(ns.prereg)), "header carries the draft PREREG sha")
    b = rows.get("amos22_0203", {})
    check(b.get("type") == "four_lumbar_or_fused_L5", f"case B type four_lumbar_or_fused_L5 (got {b.get('type')})")
    check("spineps_inst" not in b.get("masks", "") and "raw" in b.get("failures", "").lower() or "not shown to be VerSe" in b.get("failures", ""), f"case B raw SPINEPS ids refused: {b.get('failures')[:160]}")
    check("pelvis803" not in b.get("masks", "") and "pelvis803" in b.get("failures", ""), "case B legacy-id pelvis refused by the labels_for check")
    check((root / b["case_dir"] / "masks" / "ts_roi").exists(), "case B ts roi directory placed as masks/ts_roi")
    c = rows.get("cobra_A002", {})
    check(c.get("type") == "unresolved" and c.get("paired") == "1", f"case C no_count -> unresolved, paired (got {c.get('type')}, {c.get('paired')})")
    check((root / c["case_dir"] / "xr" / "projections.mha").exists() and (root / c["case_dir"] / "previews" / "overview_A002.png").exists(), "case C COBRA sweep + overview placed")
    ev_c = json.loads((root / c["case_dir"] / "evidence.json").read_text(encoding="utf-8"))
    check(any(x["rule"] == "rule1" for x in ev_c["rules_not_run"]), "case C says rule 1 could not run")
    d = rows.get("ts_s0001", {})
    check(d.get("type") == "T13" and "CT path does not exist" in d.get("failures", ""), f"case D T13 with the missing CT reported as a failure: {d.get('failures')[:80]}")
    check((root / "castellvi_II_IV" / "ALSO_IN.tsv").exists() and "ctsp_0005" in (root / "castellvi_II_IV" / "ALSO_IN.tsv").read_text(), "ALSO_IN pointer written under castellvi_II_IV")
    check((root / "L6.zip").exists() and (root / "L6.zip.sha256").exists(), "zips + sha256 written")
    for t in TYPES:
        z = root / f"{t}.zip"
        if z.exists():
            with zipfile.ZipFile(z) as zf:
                check(any(n.endswith("/README.md") for n in zf.namelist()), f"{t}.zip holds a README")
    # second run: nothing but runs.jsonl may change
    rc2 = build(ns)
    snap2 = tree_snapshot(root)
    changed = sorted(k for k in set(snap1) | set(snap2) if snap1.get(k) != snap2.get(k))
    for k in changed[:20]:
        print("  changed: " + k)
    check(rc2 == rc1 and not changed, f"second run changed nothing ({len(changed)} files differ)")
    # real samples, when present
    if args.samples:
        sroot = Path(args.samples)
        cs = make_sample_census(sroot, base)
        if cs is None:
            print("  skip real samples: none of the expected files found under " + str(sroot))
        else:
            ns2 = argparse.Namespace(**vars(ns))
            ns2.census, ns2.root, ns2.zip = str(cs), str(base / "tree_real"), False
            rc3 = build(ns2)
            probs3 = verify_tree(Path(ns2.root), sha256_file(Path(ns.prereg)))
            for p in probs3:
                print("  verify(real): " + p)
            check(not probs3, f"real-sample tree verifies ({len(probs3)} problems), exit {rc3}")
            with open(Path(ns2.root) / "manifest.tsv", encoding="utf-8", newline="") as f:
                rr = {r["case_id"]: r for r in csv.DictReader(f, delimiter="\t")}
            for cid, row in rr.items():
                print(f"    {cid}: type={row['type']} masks={row['masks']} xr={row['xr_views']} failures={row['failures'][:120]}")
            if "ctsp_0005" in rr:
                ev = json.loads((Path(ns2.root) / rr["ctsp_0005"]["case_dir"] / "evidence.json").read_text(encoding="utf-8"))
                check(ev["masks"]["spineps_inst"]["checks"]["guard"]["verdict"] == "verse_ok", "real CTSP_0005 SPINEPS guard verse_ok")
                check(ev["masks"]["gt_v11"]["checks"]["labels_for"]["scheme"] == "v10" and not ev["masks"]["gt_v11"]["checks"]["labels_for"]["id29_present"], "real 0005 v11 label: v10 scheme, id 29 absent")
            if "carmlspine_case42" in rr:
                ev = json.loads((Path(ns2.root) / rr["carmlspine_case42"]["case_dir"] / "evidence.json").read_text(encoding="utf-8"))
                check(ev["xr"]["pose_status"] == "stale_px_mm_needs_refit", "real case42 poses flagged stale (0.1465 vs 0.150 mm/px)")
                check(sorted(ev["xr"]["views"]) == ["AP", "LAT"], f"real case42 frames AP + LAT ({ev['xr']['views']})")
    print()
    if fails:
        print(f"SELFTEST FAILED: {len(fails)} check(s)")
        for f in fails:
            print("  - " + f)
    else:
        print("SELFTEST PASSED")
    if not keep and not args.selftest_dir:
        shutil.rmtree(base, ignore_errors=True)
    else:
        print(f"kept {base}")
    return 1 if fails else 0


def make_sample_census(sroot: Path, base: Path):
    """A census over the real sample files scp'd from the grid (tr_samples layout), if they are there."""
    rows = []
    c = sroot / "ctsp"
    if (c / "CTSP_0005_seg-vert_msk.nii.gz").exists():
        rows.append({"case_key": "ctsp:0005", "collection": "ctsp", "case_id": "0005", "person_key": "ctsp:0005",
                     "tier": "1", "count": "6", "anchor_source": "ts_sacrum_union_s1", "flags": "L6;castellvi_II_IV_candidate",
                     "stump_left": "", "stump_right": "", "s3_ratio": "", "registry_subtype": "L6", "truth_tier": "read",
                     "ct": str(c / "0005_ct.nii.gz") if (c / "0005_ct.nii.gz").exists() else "",
                     "spineps_inst": str(c / "CTSP_0005_seg-vert_msk.nii.gz"), "spineps_sem": str(c / "CTSP_0005_seg-spine_msk.nii.gz"),
                     "spineps_ctd": str(c / "CTSP_0005_ctd.json"), "spineps_ids": "verse_coded",
                     "ts": str(c / "COLONOG_4.nii.gz") if (c / "COLONOG_4.nii.gz").exists() else "",
                     "ts_class_map": str(c / "class_map.json") if (c / "class_map.json").exists() else "",
                     "moller_inst": str(c / "0005_rib-inst_msk.nii.gz") if (c / "0005_rib-inst_msk.nii.gz").exists() else "",
                     "moller_csv": str(c / "0005_rib_measurements.csv"), "moller_measure_json": str(c / "0005.measure.json"),
                     "pelvis": "", "gt": str(c / "0005_label.nii.gz") if (c / "0005_label.nii.gz").exists() else "",
                     "has_xr": "0", "xr_paths": ""})
    k = sroot / "carmlspine"
    if (k / "case42_seg-vert_msk.nii.gz").exists():
        xr = [str(p) for p in sorted(k.glob("case42_*_ref*.json"))] + [str(k / n) for n in ("0001.dcm", "0002.dcm") if (k / n).exists()]
        rows.append({"case_key": "carmlspine:case42", "collection": "carmlspine", "case_id": "case42",
                     "person_key": "carmlspine:case42", "tier": "1", "count": "no_count",
                     "anchor_source": "no_count: thoraco-lumbar junction out of field", "flags": "L6;L6?morph",
                     "registry_subtype": "L6", "truth_tier": "morphology-only",
                     "ct": str(k / "case42_cbct.nii.gz") if (k / "case42_cbct.nii.gz").exists() else "",
                     "spineps_inst": str(k / "case42_seg-vert_msk.nii.gz"), "spineps_sem": str(k / "case42_seg-spine_msk.nii.gz"),
                     "spineps_ctd": str(k / "case42_ctd.json"), "spineps_ids": "verse_coded",
                     "ts": str(k / "case42.nii.gz") if (k / "case42.nii.gz").exists() else "",
                     "ts_class_map": str(k / "ts_total_class_map.json") if (k / "ts_total_class_map.json").exists() else "",
                     "has_xr": "1", "xr_paths": ";".join(xr)})
    if not rows:
        return None
    cols = sorted({kk for r in rows for kk in r})
    cp = base / "sample_census.tsv"
    with open(cp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return cp


# ----------------------------------------------------------------------------------------------------- CLI
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--census", help="rules census TSV")
    ap.add_argument("--root", help=f"tree root (default {RS}/review_tree/<today>)")
    ap.add_argument("--prereg", default=str(DEFAULT_PREREG))
    ap.add_argument("--copy", action="store_true", help="copy the CTs and masks instead of symlinking")
    ap.add_argument("--zip", action="store_true", help="write <TYPE>.zip beside each type dir with sha256 manifests")
    ap.add_argument("--relabel-raw", action="store_true", help="relabel raw 1..N SPINEPS ids through the ctd instead of refusing")
    ap.add_argument("--hash-limit-mb", type=float, default=None, help="skip sha256 of inputs larger than this (recorded)")
    ap.add_argument("--registry", default=str(REPO / "SchwingNet/results/transitional_registry/registry.csv"))
    ap.add_argument("--ah-root", default=None, help=f"anomaly_harvest root ({RS}/data/anomaly_harvest)")
    ap.add_argument("--consensus", default=None, help="CTSpinoPelvic1K docs/castellvi_consensus.csv")
    ap.add_argument("--lumbosac", default=None, help="CTSpinoPelvic1K Lumbosac.csv")
    ap.add_argument("--ctsp-manifest", default=None, help="CTSpinoPelvic1K manifest.json")
    ap.add_argument("--moller-root", default=None, help=f"{RS}/ruleclass/arms/moller_fast (fallback when the census has no path)")
    ap.add_argument("--pelvis-root", default=None, help="post-processed Dataset803 pelvis root (<root>/<coll>/<case>.nii.gz)")
    ap.add_argument("--ts-root", default=None, help=f"{RS}/ruleclass/arms/ts (multilabel fallback for roi-subset rows)")
    ap.add_argument("--ts-class-map", default=None)
    ap.add_argument("--carmlspine-root", default=None, help=f"{RS}/data/carmlspine")
    ap.add_argument("--cobra-root", default=None, help=f"{RS}/data/cobra2026/cases")
    ap.add_argument("--ostk-path", default=None, help="OpenSpineToolkit checkout if ostk is not installed")
    ap.add_argument("--cases", default=None, help="only these case keys (`;` list)")
    ap.add_argument("--types", default=None, help="only these primary types (`;` list)")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--verify", action="store_true", help="verify an existing tree at --root and exit")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-dir", default=None, help="where the self-test builds (default: a temp dir, removed)")
    ap.add_argument("--samples", default=None, help="selftest: also build from the real sample files under this dir")
    ap.add_argument("--keep", action="store_true", help="selftest: keep the temp dir")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args)
    if args.verify:
        if not args.root:
            ap.error("--verify needs --root")
        probs = verify_tree(Path(args.root))
        for p in probs:
            print("PROBLEM " + p)
        print("clean" if not probs else f"{len(probs)} problem(s)")
        return 1 if probs else 0
    if not args.census:
        ap.error("--census is required (or --selftest / --verify)")
    if not args.root:
        args.root = f"{RS}/review_tree/{_dt.date.today().isoformat()}"
    return build(args)


if __name__ == "__main__":
    sys.exit(main())
