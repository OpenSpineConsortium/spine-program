#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/data_alias.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Canonical identity for every row of the data ledger: which files are the SAME picture or the SAME scan.

WHY THIS EXISTS. The ledger says where every X-ray and every CT lives. It cannot say whether two of its rows are
one thing. This project holds at least five ways for one image to appear twice under two names. ONE of them has
already cost something and is written up; the other four are the same shape and nothing has yet looked:

  * DeepFluoro reaches us as the JHU h5 subset (~/deepfluoro/unpacked_full) AND as the vendor DICOMs
    (data/deepfluoro_vendor/unpacked). Same frames, same six cadaveric pelves, two roots in data_manifest.py.
  * NHANES II entered the level banks twice, as source `nhanes` inside ~/films_drr and again as the whole of
    ~/nhanes_drr. The split is drawn per source, so 48 of 54 validation patients had their own duplicate in
    training (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md). Nothing raised; the accuracy simply came out high.
  * The film corpora appear as detector crops (spine-detector/data/yolo_v3/images/*/buu_*, csxa_*, nhanes_*,
    mendeley_*) and again as their raw roots. tools/corpus_manifold.py SETS plots several of those pairs as
    separate corpora, so "these corpora separate" can be a statement about the same pictures twice.
  * A device pair store (or_ready/devices/<dev>/pairs) and the realxray copy hold the same frames.
  * CTSpinoPelvic1K CT reaches Dataset813 through symlinks, so one volume has two paths (and the release pads the
    case id to four digits while the old CSVs do not -- `1` and `0001` are one case).

THE TRAP IT AVOIDS is the one this project keeps hitting: a number that is wrong but plausible. A held-out set
that is the training set re-encoded still returns a finite, reasonable accuracy, and no internal check fires. So
identity is decided here, once, by content, and every downstream count is made against `canonical_id` rather than
against a path or a corpus name.

THE LADDER, cheapest first; each rung states what it can and cannot see.

  0  same realpath / same inode      symlink or hard link. Costs a stat, so it works only where the files ARE --
                                     off-host it sees only the realpath / inode / device the ledger recorded, and
                                     canonical.jsonl does not carry those. Catches Dataset813. An inode is matched
                                     only together with its DEVICE: inode numbers are unique within one
                                     filesystem and the grid has at least two, so (None, inode) merged unrelated
                                     files at score 1.0. Rows whose device is unknown are skipped and counted.
  1  byte SHA-256                    a plain copy. Exact, and no false positives EXCEPT on a file with no
                                     identity to assert: every empty file has one byte hash and every blank
                                     render of one canvas has one pixel hash, so on rungs 1 and 2 they all
                                     merged into a single "picture" spanning every corpus that held one. Empty
                                     and constant files are counted and merged with nothing.
  2  decoded-pixel SHA-256           re-container (TIFF -> PNG, PNG -> PNG re-save) with identical 8-bit grey
                                     pixels. A 16-bit store exported to 8-bit does NOT match here; it falls to 3.
  3  perceptual hash + NCC check     re-encode (JPEG q85: measured 2 bits), resize (0.5x: 2 bits), and a mirrored
                                     export (indexed as a second hash). NOT a crop: a centre crop at 0.64 of the
                                     frame measured 30 bits and NCC64 0.67, so crops fall to rung 5, not here.
                                     pHash proposes, NCC decides: a candidate merges only when NCC at 64x64 is at
                                     least --ncc (default 0.97), the same control tools/or_audit_dupes.py uses,
                                     because two different patients imaged the same way score high at 32x32.
                                     NCC READS THE FILES, so this rung confirms nothing on a host where they are
                                     not mounted: those pairs are counted as unverified and NOT merged.
                                     Every proposal the NCC rejected is COUNTED, and that count is the false-
                                     positive control; the rows themselves are capped (5,000 file pairs, then
                                     collapsed to at most 400 pairs of groups in alias_groups.json and 25 in
                                     ALIAS_SUMMARY.md), and the report says how many it is showing of how many.
  4  volume key                      shape + spacing + a digest of the subsampled array, then a correlation check
                                     that also re-reads the files, and so is likewise lost off-host.
  5  derivation key (NAME evidence)  same patient key and same view in two roots, ONE file per root, e.g.
                                     yolo_v3/images/train/buu_00123_ap.png and the raw
                                     buu_full/BUU-LSPINEv1/AP/0123.jpg. A crop does not match its parent by
                                     pixels, so without this rung the derived film corpora look independent of
                                     their raw roots. Name evidence is marked as such in every output and can be
                                     switched off with --no-name-merge.

Identity is also reported at PATIENT level, which is the level a split has to be drawn at. One person reached
through two roots is a leak even when no two files are the same picture, and that key (nhanes_00160 == NH_00160_c)
is the cross-source key the NHANES note says does not exist.

WHAT IT CANNOT SEE, stated plainly: a re-windowed or inverted copy (grey mapping changed), a rotated copy, a crop
named differently from its parent, a duplicate whose two names share no patient key this file knows about, a file
no reader here can open (.dcm without pydicom), and one frame inside a container that holds many (the DeepFluoro
h5 is one row, so it can only meet another container). An unreadable file is counted by EXTENSION and never
called unique -- but only under --pixels, because without it nothing is opened here and so nothing can be found
unreadable. All of that would otherwise be missed silently, which is why the known-alias checklist below runs on
every `canon` run and prints NOT FOUND with the per-side member counts, so "we did not find it" is separable from
"that root was not in the ledger".

    python tools/data_alias.py canon --ledger <ledger.jsonl> --out <dir> --pixels --workers 16
    python tools/data_alias.py selftest    # synthetic images: the distance and NCC measured for each case, the
                                           # thresholds in force, and what merged on which rung
    python tools/data_alias.py paths       # every corpus in corpus_manifold.SETS and data_manifest.ROOTS through
                                           # the rules; exits 1 on a corpus with no rule
    python tools/data_alias.py explain --groups <dir>/alias_groups.json --path <some path>

Outputs in --out: canonical.jsonl (path -> canonical_id, one row per ledger file, nothing truncated),
alias_groups.json (one entry per multi-member group -- roots, analysis units, the evidence that merged them,
whether the group spans corpora the analyses treat as independent, and its members up to --max-members with the
number dropped recorded), alias_edges.csv (every merge edge with its measured score, nothing truncated) and
ALIAS_SUMMARY.md, which is a READING copy and says so on every table: the largest 200 cross-root groups, the
largest 50 name-only groups, the 100 patients reached through most roots and the 25 NEAREST misses of the NCC
gate, each table printing how many more there are and where the rest of them live.

canonical.jsonl carries the digests it computed, so it is also the digest cache: compute once with --pixels where
the data is (a compute node), then re-run rungs 1, 2, 4 (digest) and 5 anywhere by passing that file as --ledger,
and pass the old one as --prev so the ids survive the rebuild. NOT the whole ladder: rung 0 needs the files or a
ledger carrying realpath/inode/device (canonical.jsonl carries neither), and rungs 3 and 4's correlation open the
files to confirm, so away from the data they merge nothing and the pairs are reported as unverified. --prev never
hands one id to two groups: a group that SPLIT since the previous run cannot have both halves inherit the
parent's id, which would say two pictures are one thing.

READ AGAINST tools/data_ledger.py, WHICH WRITES THE LEDGER. Its `pix_sha256`, `vol_sha256`, `patient_key` and
`alias_group` are all read here. Its `dhash` is deliberately NOT read as a pHash: it is a difference hash on an
8x9 box downsample, a different function from the DCT phash64 below, and reading one as the other would put two
hash spaces in one index where every pair sits about 32 bits apart -- nothing would ever match and the run would
still report full pHash coverage. Rung 3 therefore needs --pixels, and the run says so when it sees a dhash.
"""
from __future__ import annotations

import argparse
import collections
import csv
import gzip
import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------------------------------------- ledger input
# The ledger is written by a sibling tool. Field names are read tolerantly so this file does not break when that
# tool renames a column; the run prints exactly which ledger fields it found and which it had to compute.
FIELD = {
    "path": ["path", "file", "filepath", "abs_path", "full_path"],
    "sha256": ["sha256", "byte_sha256", "content_sha256", "hash", "sha256_full"],
    "bytes": ["bytes", "size", "nbytes", "filesize", "size_bytes"],
    "kind": ["kind", "media", "filetype", "type"],
    "root": ["root", "root_name", "dataset_root"],
    "corpus": ["corpus", "source", "dataset", "set", "corpus_name"],
    "stage": ["stage", "step", "pipeline_stage"],
    "case": ["case", "case_id", "stem", "id"],
    "patient": ["patient", "patient_id", "subject", "subject_id"],
    "pixel_sha256": ["pixel_sha256", "decoded_sha256", "pix_sha256", "pixels_sha256"],
    "phash": ["phash", "p_hash", "perceptual_hash"],
    "phash_mirror": ["phash_mirror", "phash_flip"],
    "realpath": ["realpath", "real_path", "resolved", "link_target"],
    "inode": ["inode", "ino"],
    "device": ["device", "dev", "st_dev"],
    "shape": ["shape", "dims", "volume_shape", "decoded_shape"],
    "spacing": ["spacing", "voxel_spacing", "zooms", "pixdim", "spacing_mm"],
    # tools/data_ledger.py writes `vol_sha256`; without it here the whole volume rung reads zero coverage against
    # the real ledger and every CT comes back unique, quietly
    "vol_digest": ["vol_digest", "volume_digest", "downsample_digest", "vol_sha256"],
    # data_ledger's cross-root patient key ("nhanes_ii/160") -- the join the NHANES note says was missing. It is
    # ALREADY namespaced, which patient_key() below relies on; see the note there about not re-namespacing it.
    "patient": ["patient", "patient_id", "subject", "subject_id", "patient_key"],
    "alias_group": ["alias_group", "alias", "population"],
}
# NOT an alias of `phash`. tools/data_ledger.py writes `dhash`: a 64-bit DIFFERENCE hash on an 8x9 box downsample,
# a different function from the DCT phash64 below. Reading one as the other would put two hash spaces in one index
# where every distance is about 32 bits, nothing would ever match, and the run would still report a pHash
# coverage of 100%. So the ledger's dhash is deliberately not read; the run warns when it sees one, because that
# means rung 3 needs --pixels.
LEDGER_DHASH_FIELDS = ("dhash", "d_hash", "difference_hash")
IMG_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp", ".pgm", ".npy", ".npz"}
# the device pair stores keep the real frame inside an .npz beside the render and the hit mask; without reading
# that member the pair stores are invisible to every content rung, and 'pairs vs realxray copy' can never be found
NPZ_IMAGE_KEYS = ("real", "image", "img", "frame", "x")
VOL_EXT = {".nii", ".nii.gz", ".mha", ".mhd", ".nrrd", ".h5", ".hdf5"}
# a DICOM frame is a picture, not a volume: the vendor side of the DeepFluoro alias is a directory of .dcm files
# and treating them as volumes sent every one of them to nibabel, which cannot read them, so they merged with
# nothing and said nothing. Reading them needs pydicom; without it they are counted as unreadable, by extension.
DICOM_EXT = {".dcm", ".ima"}
IMG_EXT |= DICOM_EXT

# ------------------------------------------------------------------------------------- roots and analysis units
# `python tools/data_alias.py paths` runs every corpus in tools/corpus_manifold.py SETS and tools/data_manifest.py
# ROOTS through this table and EXITS 1 on any that no rule matches. Three do not, and they are left that way on
# purpose rather than covered by a blanket rule: `or_ready` and `devcorpus` are trees holding many different
# things (only their devices/pairs, spinesac/display, wholespine/eval and styled/ subtrees are corpora), and one
# rule over either would give every file in it ONE unit -- which is how the single `/FluoroCap/` rule below hid a
# duplicate between two of the five FluoroCap harvests. `carmlspine_pose` holds poses, not images, and the ledger
# this reads is one row per imaging file. Extending the table means adding a rule per SUBTREE that is a corpus.
#
# (regex on the posix path, root label, analysis unit, pipeline stage).
# THE UNIT NAMES ARE THE NAMES THE ANALYSES USE. Where a path is one of tools/corpus_manifold.py SETS, the unit is
# that SETS key, so "this group spans units the analyses treat as independent" means exactly what Figure 1 row (d)
# means when it says two corpora separate. Order matters: first match wins.
ROOT_RULES = [
    (r"/deepfluoro/unpacked_full/", "deepfluoro_h5", "DeepFluoro", "raw"),
    (r"/deepfluoro_vendor/unpacked", "deepfluoro_vendor", "DeepFluoro (vendor DICOM)", "raw"),
    (r"/realxray/deepfluoro/", "realxray/deepfluoro", "DeepFluoro", "derived"),
    (r"/realxray/carmlspine/", "realxray/carmlspine", "C-ArmLSpine", "derived"),
    (r"/realxray/cobra_elekta/", "realxray/cobra_elekta", "COBRA Elekta", "derived"),
    (r"/realxray/geneva_hip/", "realxray/geneva_hip", "Geneva", "derived"),
    (r"/realxray/([^/]+)/", "realxray/{1}", "realxray {1}", "derived"),
    # the pair store of a device IS a corpus_manifold SETS entry for some devices; where it is, use the SETS name,
    # because that is the name Figure 1 row (d) prints
    (r"/or_ready/devices/varian_halcyon/pairs/", "devices/varian_halcyon/pairs", "COBRA Varian", "derived"),
    (r"/or_ready/devices/([^/]+)/pairs/", "devices/{1}/pairs", "device pairs {1}", "derived"),
    (r"/or_ready/spinesac/display/raw/", "spinesac_display", "SpineSAC", "derived"),
    (r"/or_ready/wholespine/data/eval/aasce/", "aasce", "AASCE", "raw"),
    (r"/carmlspine/unpacked/", "carmlspine_raw", "C-ArmLSpine", "raw"),
    (r"/cobra2026/cases/", "cobra2026_raw", "COBRA Elekta", "raw"),
    (r"/geneva_hip/", "geneva_raw", "Geneva", "raw"),
    (r"/ljubljana/", "ljubljana", "Ljubljana", "raw"),
    (r"/spinesac/", "spinesac", "SpineSAC", "raw"),
    # film detector banks: the corpus is carried by the stem prefix
    (r"/spine-detector/data/yolo_[^/]*/images/[^/]*/buu_", "yolo_crops", "BUU-LSPINE", "derived"),
    (r"/spine-detector/data/yolo_[^/]*/images/[^/]*/csxa_", "yolo_crops", "CSXA", "derived"),
    (r"/spine-detector/data/yolo_[^/]*/images/[^/]*/nhanes_", "yolo_crops", "NHANES II", "derived"),
    (r"/spine-detector/data/yolo_[^/]*/images/[^/]*/mendeley_", "yolo_crops", "Mendeley", "derived"),
    (r"/spine-detector/data/yolo_v6f/", "yolo_v6f", "yolo_v6f fluoro", "bank"),
    (r"/spine-detector/data/yolo_([^/]*)/", "yolo_{1}", "detector bank yolo_{1}", "bank"),
    # raw film roots
    (r"/spine-detector/data/raw/buu_full/.*/AP/", "buu_raw", "BUU-LSPINE AP", "raw"),
    (r"/spine-detector/data/raw/buu_full/.*/LA/", "buu_raw", "BUU-LSPINE LA", "raw"),
    (r"/spine-detector/data/raw/buu_full/", "buu_raw", "BUU-LSPINE raw", "raw"),
    (r"/spine-detector/data/raw/csxa/", "csxa_raw", "CSXA raw", "raw"),
    (r"/spine-detector/data/raw/nhanes_full/", "nhanes_raw", "NHANES II full", "raw"),
    (r"/spine-detector/data/raw/mendeley_716/", "mendeley_raw", "Mendeley raw", "raw"),
    # render / crop banks
    (r"/films_drr/.*(?:^|/)nhanes[_-]", "films_drr", "films_drr:nhanes", "bank"),
    (r"/films_drr/.*(?:^|/)csxa[_-]", "films_drr", "films_drr:csxa", "bank"),
    (r"/films_drr/.*(?:^|/)buu[_-]", "films_drr", "films_drr:buu", "bank"),
    (r"/films_drr/", "films_drr", "films_drr", "bank"),
    (r"/nhanes_drr/", "nhanes_drr", "nhanes_drr (second NHANES copy)", "bank"),
    (r"/ctsp_drr/", "ctsp_drr", "DRR CTSpinoPelvic1K", "bank"),
    (r"/verse_drr/", "verse_drr", "DRR VerSe", "bank"),
    (r"/ts_drr/", "ts_drr", "DRR TotalSegmentator", "bank"),
    (r"/physics_drr/", "physics_drr", "physics render", "bank"),
    (r"/physics_rare/", "physics_rare", "physics rare", "bank"),
    (r"/vindr_pseudo/", "vindr_pseudo", "VinDr-SpineXR", "raw"),
    (r"/lateral236_pseudo/", "lateral236_pseudo", "Lateral 236", "raw"),
    (r"/model_night/anchor_[^/]*/images/", "cios_calibrated", "calibrated Cios render", "bank"),
    (r"/devcorpus/styled/([^/]+)/", "styled/{1}", "styled {1}", "bank"),
    # THE FIVE FluoroCap SETS ARE FIVE CORPORA, not one. corpus_manifold plots "FluoroCap real", "FluoroCap
    # grainy", "Open-i", "Wikimedia Commons", "PMC 18M" and "PMC figure panels" separately, and the literature
    # harvests overlap by construction (the same PMC figure is reached by more than one of them). A single
    # `/FluoroCap/` rule gave them all one root and one unit, so a duplicate BETWEEN two of them was neither
    # cross-root nor cross-unit and appeared in no table in ALIAS_SUMMARY.md.
    (r"/FluoroCap/panels/", "fluorocap_panels", "PMC figure panels", "raw"),
    (r"/FluoroCap/real_fluoro_only/", "fluorocap_real", "FluoroCap real", "raw"),
    (r"/FluoroCap/real_grainy/", "fluorocap_grainy", "FluoroCap grainy", "raw"),
    (r"/FluoroCap/openi/", "fluorocap_openi", "Open-i", "raw"),
    (r"/FluoroCap/commons/", "fluorocap_commons", "Wikimedia Commons", "raw"),
    (r"/FluoroCap/pmc18m/", "fluorocap_pmc18m", "PMC 18M", "raw"),
    (r"/FluoroCap/", "fluorocap", "FluoroCap", "raw"),
    # CT volumes
    (r"Dataset8\d\d[^/]*/", "nnunet_dataset", "CTSpinoPelvic1K (Dataset813 link)", "bank"),
    (r"/CTSpinoPelvic1K/(ct|labels)/", "ctsp_release", "CTSpinoPelvic1K", "raw"),
    (r"/hf_export/(ct|labels)/", "ctsp_release", "CTSpinoPelvic1K", "raw"),
    (r"/Totalsegmentator_dataset", "ts_subjects", "TotalSegmentator", "raw"),
    (r"/VerSeFusion/", "versefusion", "VerSe", "raw"),
]
# Unit pairs already known to be one population, so a group spanning them is a double-inclusion risk but not a
# surprise. Anything else spanning two units contradicts an independence the analyses assume.
SAME_POPULATION = {frozenset({"DeepFluoro", "DeepFluoro (vendor DICOM)"}),
                   frozenset({"BUU-LSPINE AP", "BUU-LSPINE LA"})}

KNOWN_ALIASES = [
    dict(name="DeepFluoro: JHU h5 subset vs vendor DICOMs", a=r"/deepfluoro/unpacked_full/", b=r"/deepfluoro_vendor/unpacked",
         note="the same 366 frames of the same six cadaveric pelves, two roots in tools/data_manifest.py"),
    dict(name="device pair store vs realxray copy", a=r"/or_ready/devices/[^/]+/pairs/", b=r"/realxray/[^/]+/images/",
         note="the same real frames in the common layout and in the per-device pair store"),
    dict(name="BUU-LSPINE: detector crops vs raw root", a=r"/yolo_[^/]*/images/[^/]*/buu_", b=r"/raw/buu_full/",
         note="corpus_manifold plots 'BUU-LSPINE' and 'BUU-LSPINE AP/LA' as separate sets"),
    dict(name="CSXA: detector crops vs raw root", a=r"/yolo_[^/]*/images/[^/]*/csxa_", b=r"/raw/csxa/", note=""),
    dict(name="NHANES II: detector crops vs raw TIFFs", a=r"/yolo_[^/]*/images/[^/]*/nhanes_", b=r"/raw/nhanes_full/", note=""),
    dict(name="Mendeley: detector crops vs raw root", a=r"/yolo_[^/]*/images/[^/]*/mendeley_", b=r"/raw/mendeley_716/", note=""),
    dict(name="NHANES II twice in the level banks", a=r"/films_drr/", b=r"/nhanes_drr/",
         note="docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md: split per source, 48 of 54 val patients leaked"),
    dict(name="CTSpinoPelvic1K CT: Dataset813 link vs real path", a=r"Dataset8\d\d", b=r"/(CTSpinoPelvic1K|hf_export)/ct/",
         note="imagesTr symlinks; also the zero-padding trap, case 1 == case 0001"),
]

# ------------------------------------------------------------------------------------------------- patient keys
# One person / one specimen, written the same way whatever root reached them. This is the cross-source key the
# NHANES note says is missing: nhanes_00160 and NH_00160_c are one patient.
VIEW_WORDS = [(r"(?:^|[_-])(?:ap|frontal|front|pa)(?:[_-]|$)", "ap"),
              (r"(?:^|[_-])(?:la|lat|lateral)(?:[_-]|$)", "lat"),
              (r"(?:^|[_-])(?:c|cerv|cervical)(?:[_-]|$)", "cerv"),
              (r"(?:^|[_-])(?:l|lumb|lumbar)(?:[_-]|$)", "lumb")]


def posix(p: str) -> str:
    return str(p).replace("\\", "/")


def classify(path: str):
    """(root, analysis unit, stage) from the path. Unknown paths keep their parent directory as the root.

    THE UNCLASSIFIED UNIT CARRIES ITS ROOT. A bare "unclassified" made every corpus with no rule one unit, so a
    duplicate between two unknown corpora had spans_units False and appeared in no table. The root is still the
    last directory component, which DOES collide across corpora (`vindr_pseudo/img` and `lateral236_pseudo/img`
    are both root `img`); that is a known remaining hole and the reason the rule table above is worth extending
    rather than relying on the fallback."""
    s = posix(path)
    for pat, root, unit, stage in ROOT_RULES:
        m = re.search(pat, s)
        if m:
            def sub(t):
                for i, g in enumerate(m.groups() or (), start=1):
                    t = t.replace("{%d}" % i, str(g))
                return t
            return sub(root), sub(unit), stage
    root = posix(os.path.dirname(s)).split("/")[-1] or "?"
    return root, f"unclassified:{root}", "?"


def view_token(stem: str, family: str) -> str:
    # the extension is stripped first: without that, 'buu_00123_ap.png' has no view (the token is followed by '.'
    # and not by [_-] or the end of the string) while 'buu_00123_ap_crop.png' has one, and the two never meet
    s = re.sub(r"\.(nii\.gz|[A-Za-z0-9]+)$", "", str(stem)).lower()
    for pat, tok in VIEW_WORDS:
        if re.search(pat, s):
            if family == "nhanes" and tok in ("ap", "lat"):
                continue                      # NHANES names its two films _c and _l -- cervical and lumbar
            if family in ("buu", "csxa", "mendeley") and tok in ("cerv", "lumb"):
                return "lat" if tok == "lumb" else tok   # BUU's LA is lateral; a bare _l there is not "lumbar"
            return tok
    # the raw film roots put the view in a directory of its own (BUU-LSPINEv1/AP/0123.jpg), and the last segment
    # has no trailing slash, so this matches SEGMENTS rather than looking for '/ap/' in the string
    segs = [x for x in posix(s).split("/") if x]
    for seg in segs:
        if seg in ("ap", "frontal", "pa"):
            return "ap"
        if seg in ("la", "lat", "lateral"):
            return "lat"
        if seg in ("c", "cerv", "cervical"):
            return "cerv"
        if seg in ("l", "lumb", "lumbar"):
            return "lumb"
    return ""


def patient_key(path: str, unit: str, ledger_patient: str = "", alias_group: str = "") -> str:
    """A cross-root patient / specimen key, or '' when this file does not know one for that corpus."""
    s = posix(path)
    base = os.path.basename(s)
    stem = re.sub(r"\.(nii\.gz|[A-Za-z0-9]+)$", "", base)
    hay = f"{s}|{ledger_patient}"
    m = re.search(r"(17-1882|17-1905|18-0725|18-1109|18-2799|18-2800)", hay)
    if m:
        return f"deepfluoro:{m.group(1)}"
    if re.search(r"nhanes|/NH_|(?:^|/)NH_|C\d{5}_cervical|C\d{5}_lumbar", hay, re.I):
        # the raw root spells the case as the bare file name (nhanes_full/00160.tiff); without this the raw TIFFs
        # carry no key at all and can never meet their crops
        m = re.search(r"/nhanes_full/0*(\d{3,6})\b", hay, re.I) or re.search(r"(?:nhanes[_-]|NH_|C)0*(\d{3,6})", hay, re.I)
        if m:
            return f"nhanes:{int(m.group(1)):05d}"
    if re.search(r"buu", hay, re.I):
        m = re.search(r"buu[_-]?0*(\d{1,6})", hay, re.I) or re.search(r"/(?:AP|LA)/0*(\d{1,6})\b", hay)
        if m:
            return f"buu:{int(m.group(1)):05d}"
    if re.search(r"csxa", hay, re.I):
        m = re.search(r"csxa[_-]([A-Za-z0-9]+)", hay, re.I)
        return f"csxa:{(m.group(1) if m else stem).lower()}"
    if re.search(r"mendeley", hay, re.I):
        # THE BASENAME, NOT THE PATH. The raw root is literally named `mendeley_716`, so searching the whole path
        # read the root's own name as a case id and returned `mendeley:716` for all 716 films -- 716 people
        # collapsed into one patient, and the crops (`mendeley_0007.png`, keyed 0007) could never meet the raw
        # films they were cut from. Neither showed up as an error; the patient table just had one enormous row.
        m = re.search(r"mendeley[_-]([A-Za-z0-9]+)", base, re.I)
        k = (m.group(1) if m else stem).lower()
        return f"mendeley:{int(k):05d}" if k.isdigit() else f"mendeley:{k}"   # 0007 and 7 are one film
    if re.search(r"ctsp|CTSpinoPelvic1K|Dataset8\d\d|hf_export", hay, re.I):
        # NOT \b after the digits: nnU-Net writes CTSP_0001_0000.nii.gz and '_' is a word character, so \b never
        # fires there and every Dataset813 image silently lost its key
        m = re.search(r"(?:ctsp|CTSP)[_-]?(\d{1,4})(?![0-9])", hay) or re.search(r"(?:^|/)(\d{1,4})(?:_0000)?\.nii", hay)
        if m:
            return f"ctsp:{int(m.group(1)):04d}"          # the release pads to four digits, the old CSVs do not
    m = re.search(r"(case\d{1,4})", hay)
    if m:
        # A CASE NUMBER ON ITS OWN NAMES NOTHING. case07 exists in C-ArmLSpine, in COBRA and in a device pair
        # store, and a global 'carmlspine:case07' merged a COBRA frame into a C-ArmLSpine patient -- the same
        # shape of error as resolving a label against the wrong map. The corpus has to come from the path, and
        # where the path does not say (a device pair store is named by DEVICE, not by corpus) the key is scoped to
        # the device and those files meet their copies by content instead.
        d = re.search(r"/devices/([^/]+)/", hay)
        if re.search(r"carmlspine|C-ArmLSpine", hay, re.I):
            return f"carmlspine:{m.group(1)}"
        if re.search(r"cobra", hay, re.I):
            return f"cobra:{m.group(1)}"
        if re.search(r"geneva", hay, re.I):
            return f"geneva:{m.group(1)}"
        if re.search(r"ljubljana", hay, re.I):
            return f"ljubljana:{m.group(1)}"
        if d:
            return f"device:{d.group(1)}:{m.group(1)}"
        return ""
    if re.search(r"totalseg|ts_drr", hay, re.I):
        m = re.search(r"(?:^|/|totalseg[_-])(s\d{4})(?:/|_|$)", hay)
        if m:
            return f"ts:{m.group(1)}"                     # renders are named totalseg_s0123_lat_p001
    m = re.search(r"(sub-verse\d{3,4}|verse\d{3,4})", hay, re.I)
    if m:
        return f"verse:{m.group(1).lower().replace('sub-', '')}"
    if ledger_patient:
        # DO NOT NAMESPACE BY ANALYSIS UNIT. Prefixing the ledger's own patient id with the unit gave one person
        # a different key in every unit they appear in -- `films_drr:VND-0001`, `detector bank yolo_v9:VND-0001`,
        # `unclassified:VND-0001` -- so the ledger's cross-root patient id could join a patient only WITHIN one
        # unit, which is the one case where the join is not needed. It also did not even buy the collision safety
        # it cost, because every corpus with no rule shares the namespace `unclassified`.
        # An id the ledger has already namespaced (tools/data_ledger.py writes `nhanes_ii/160`) is used verbatim;
        # otherwise the declared alias group is the namespace, because that is the population, not the bank.
        # An id the ledger has already namespaced (tools/data_ledger.py writes `nhanes_ii/160`) is used verbatim;
        # otherwise the declared alias group is the namespace, because that is the POPULATION, not the bank.
        # With neither, the key stays scoped to the unit -- a bare id cannot be joined safely, since `case07`
        # exists in C-ArmLSpine, in COBRA and in a device pair store -- and those rows are counted and named in
        # the run so the reader knows the join was not attempted rather than attempted and found nothing.
        p = str(ledger_patient).strip()
        if "/" in p or ":" in p:
            return p
        if alias_group:
            return f"{str(alias_group).strip().lower()}/{p}"
        return f"{unit.split(':')[0].strip().lower()}:{p}#unitscoped"
    return ""


def family_of(pkey: str) -> str:
    return pkey.split(":")[0] if pkey else ""


# ---------------------------------------------------------------------------------------------------- digests
def _to_uint8(a: np.ndarray) -> np.ndarray:
    """Display-like 8 bit. 16-bit TIFFs and DICOM-derived PNGs saturate under PIL's convert('L'); scale on the
    0.5-99.5 percentiles instead (the same reading tools/corpus_manifold.py uses)."""
    a = np.asarray(a)
    if a.dtype == np.uint8:
        return a
    a = a.astype(np.float64)
    lo, hi = np.percentile(a, (0.5, 99.5))
    return np.clip(255.0 * (a - lo) / max(hi - lo, 1e-9), 0, 255).astype(np.uint8)


def read_gray(path: str):
    """2-D array for an image, None for anything that is not one (a volume, an unreadable file)."""
    try:
        if path.lower().endswith(".npz"):
            with np.load(path, allow_pickle=False) as z:
                key = next((k for k in NPZ_IMAGE_KEYS if k in z.files), None)
                if key is None:
                    key = next((k for k in z.files if getattr(z[k], "ndim", 0) == 2), None)
                if key is None:
                    return None
                a = np.asarray(z[key])
            return a if a.ndim == 2 else None
        if path.lower().endswith(".npy"):
            a = np.load(path, allow_pickle=False)
            if a.ndim == 3 and a.shape[-1] in (3, 4):
                a = a.mean(-1)
            if a.ndim != 2:
                return None
            return a
        if os.path.splitext(path.lower())[1] in DICOM_EXT:
            import pydicom
            a = np.asarray(pydicom.dcmread(path).pixel_array)
            if a.ndim == 3 and a.shape[-1] in (3, 4):
                a = a.mean(-1)
            return a if a.ndim == 2 else None              # a multi-frame DICOM is a container, not one picture
        from PIL import Image
        im = Image.open(path)
        a = np.asarray(im)
        if a.ndim == 3:
            a = a[..., :3].mean(-1)
        if a.ndim != 2:
            return None
        return a
    except Exception:                                      # noqa: BLE001 -- an unreadable row is reported, not fatal
        return None


_DCT = {}


def dct_matrix(n: int) -> np.ndarray:
    if n not in _DCT:
        k = np.arange(n)[:, None]
        i = np.arange(n)[None, :]
        _DCT[n] = np.cos(np.pi * (2 * i + 1) * k / (2 * n))
    return _DCT[n]


def phash64(gray: np.ndarray, n: int = 32, keep: int = 8) -> int:
    """DCT perceptual hash, 63 bits in a 64-bit int. Scale-free by construction (the image is box-resized to
    n x n first), so a 0.5x copy and a JPEG re-encode land within a few bits of the original."""
    from PIL import Image
    im = Image.fromarray(_to_uint8(gray)).resize((n, n), Image.BOX)
    x = np.asarray(im, np.float64)
    M = dct_matrix(n)
    d = M @ x @ M.T
    v = d[:keep, :keep].ravel()[1:]                        # drop DC: it is the mean brightness, not structure
    bits = v > np.median(v)
    h = 0
    for i, b in enumerate(bits):
        if b:
            h |= (1 << i)
    return int(h)


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def pixel_digest(gray: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(f"{gray.shape}|{gray.dtype}".encode())
    h.update(np.ascontiguousarray(gray).tobytes())
    return h.hexdigest()


# A DEGENERATE FILE HAS NO IDENTITY TO ASSERT. The byte hash of every empty file is one value, and every blank
# render of one canvas size has one pixel hash, so rungs 1 and 2 -- the rungs the ladder above calls "exact, no
# false positives" -- merged three zero-byte stubs in three corpora into one "picture", flagged the group as
# spanning independent units, and exited 1 under --fail-on-cross-unit. A failed download and a render that came
# out with no bone (docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md) are both common enough to expect. Such files are
# now counted and reported, never merged on content: they are not unique and they are not the same picture, and
# saying either would be inventing a number.
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()


def byte_sha256(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def volume_key(path: str, grid: int = 24):
    """(shape, spacing, digest of the subsampled array, the array itself) for a 3-D scan, or None.

    The array is read through nibabel's dataobj with a stride, so a 500 MB CT costs a few MB of reads."""
    try:
        import nibabel as nib
        img = nib.load(path)
        sh = tuple(int(x) for x in img.shape[:3])
        sp = tuple(round(float(z), 4) for z in img.header.get_zooms()[:3])
        st = tuple(max(1, s // grid) for s in sh)
        a = np.asarray(img.dataobj[::st[0], ::st[1], ::st[2]], dtype=np.float32)
        q = _to_uint8(a)
        h = hashlib.sha256(f"{sh}|{sp}".encode())
        h.update(q.tobytes())
        return dict(shape=sh, spacing=sp, digest=h.hexdigest(), small=q.astype(np.float32))
    except Exception:                                      # noqa: BLE001
        return None


def digest_one(job):
    """Worker: (index, path, kind, want_bytes) -> the digests that file can supply."""
    i, path, kind, want_bytes = job
    out = dict(i=i, ok=False, err=None)
    if not os.path.exists(path):
        out["err"] = "missing"
        return out
    try:
        if want_bytes:
            out["sha256"] = byte_sha256(path)
        if kind == "volume":
            vk = volume_key(path)
            if vk:
                if float(np.ptp(vk["small"])) == 0.0:
                    out["degenerate"] = "blank (constant) volume"
                    out.update(shape=list(vk["shape"]), spacing=list(vk["spacing"]), ok=True)
                else:
                    out.update(vol_digest=vk["digest"], shape=list(vk["shape"]), spacing=list(vk["spacing"]), ok=True)
            else:
                out["err"] = "volume unreadable"
            return out
        g = read_gray(path)
        if g is None:
            out["err"] = "not a 2-D image"
            return out
        if g.size == 0 or float(np.ptp(np.asarray(g, np.float64))) == 0.0:
            out["degenerate"] = "blank (constant) image"
            out["ok"] = True
            return out                                     # no digests: see EMPTY_SHA256 above
        out["pixel_sha256"] = pixel_digest(g)
        out["phash"] = phash64(g)
        out["phash_mirror"] = phash64(np.ascontiguousarray(g[:, ::-1]))
        out["ok"] = True
    except Exception as e:                                 # noqa: BLE001
        out["err"] = f"{type(e).__name__}: {e}"
    return out


# ------------------------------------------------------------------------------------------- NCC verification
_VEC = {}


def ncc_vec(path: str, n: int, mirror: bool = False):
    key = (path, n, mirror)
    if key in _VEC:
        return _VEC[key]
    g = read_gray(path)
    v = None
    if g is not None:
        from PIL import Image
        if mirror:
            g = np.ascontiguousarray(g[:, ::-1])
        a = np.asarray(Image.fromarray(_to_uint8(g)).resize((n, n), Image.BOX), np.float32).ravel()
        a -= a.mean()
        s = float(np.linalg.norm(a))
        v = a / s if s > 1e-6 else None
    if len(_VEC) > 200000:
        _VEC.clear()
    _VEC[key] = v
    return v


def ncc(pa: str, pb: str, n: int, mirror: bool = False):
    a, b = ncc_vec(pa, n), ncc_vec(pb, n, mirror)
    return float(a @ b) if a is not None and b is not None else None


# ------------------------------------------------------------------------------------------------- union-find
class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra
            return True
        return False


# ---------------------------------------------------------------------------------------------- ledger reading
def pick(rec, key):
    for name in FIELD[key]:
        if name in rec and rec[name] not in (None, ""):
            return rec[name]
    return None


def ledger_files(spec):
    """THE LEDGER IS SHARDED. tools/data_ledger.py writes `ledger_shard_000_of_016.jsonl` per array task and its
    `summary` command never concatenates them, so a `--ledger <one file>` could not name the real artifact at all
    and the run would read whichever single shard was pointed at -- a clean-looking answer over 1/16th of the
    data. A directory, a glob, or one file are all accepted, and the run prints how many files it read."""
    s = str(spec)
    if os.path.isdir(s):
        import glob as _glob
        got = sorted(_glob.glob(os.path.join(s, "ledger_shard_*.jsonl*")))
        return got or sorted(_glob.glob(os.path.join(s, "*.jsonl*")))
    if any(c in s for c in "*?["):
        import glob as _glob
        return sorted(_glob.glob(s))
    return [s]


def read_ledger(path):
    op = gzip.open if str(path).endswith(".gz") else open
    bad = 0
    with op(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                yield json.loads(line)
            except Exception:                              # noqa: BLE001
                bad += 1
                if bad <= 3:
                    print(f"  ledger: unparsable line skipped ({line[:70]}...)", flush=True)
    if bad:
        print(f"  ledger: {bad} unparsable lines skipped", flush=True)


def as_hash_int(v):
    """A pHash from the ledger, however it was written: an int, a decimal string, or a 16-character hex string
    (which is what this file writes, so a canonical.jsonl can be fed straight back in). A 16-character string is
    read as hex; anything shorter is tried as decimal first, then as hex. Unreadable values are dropped, not
    guessed -- a mis-read hash would silently stop the mirror index from ever matching."""
    if v in (None, ""):
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip().lower().removeprefix("0x")
    try:
        return int(s, 16) if len(s) == 16 else int(s)
    except ValueError:
        try:
            return int(s, 16)
        except ValueError:
            return None


def kind_of(path, declared):
    if declared in ("image", "volume", "other"):
        return declared
    s = path.lower()
    if s.endswith(".nii.gz"):
        return "volume"
    ext = os.path.splitext(s)[1]
    if ext in VOL_EXT:
        return "volume"
    if ext in IMG_EXT:
        return "image"
    return "other"


def load_rows(ledger, only_root, skip_root, only_kind):
    rows, seen_fields = [], collections.Counter()
    files = ledger_files(ledger)
    if not files:
        print(f"  ledger: nothing matched {ledger!r}")
    elif len(files) > 1:
        print(f"  ledger: {len(files)} shard files ({os.path.basename(files[0])} .. "
              f"{os.path.basename(files[-1])})")
    seen_paths, dupe_lines = set(), 0
    for rec in (r for f in files for r in read_ledger(f)):
        p = pick(rec, "path")
        if not p:
            continue
        # one file, one row: the shards overlap when a scan is re-run, and data_ledger's own summary drops the
        # repeated path lines the same way. Two rows for one path inflate every group size that holds it.
        if str(p) in seen_paths:
            dupe_lines += 1
            continue
        seen_paths.add(str(p))
        for k in FIELD:
            if pick(rec, k) is not None:
                seen_fields[k] += 1
        path = posix(str(p))
        root, unit, stage = classify(path)
        lroot = pick(rec, "root")
        if lroot:
            root = str(lroot) if root == "?" else root
        kind = kind_of(path, str(pick(rec, "kind") or ""))
        if only_kind and kind != only_kind:
            continue
        if only_root and not any(re.search(x, root) or re.search(x, path) for x in only_root):
            continue
        if skip_root and any(re.search(x, root) or re.search(x, path) for x in skip_root):
            continue
        pat = str(pick(rec, "patient") or "")
        rows.append(dict(path=path, root=root, unit=unit, stage=str(pick(rec, "stage") or stage), kind=kind,
                         sha256=pick(rec, "sha256"), pixel_sha256=pick(rec, "pixel_sha256"),
                         phash=as_hash_int(pick(rec, "phash")), phash_mirror=as_hash_int(pick(rec, "phash_mirror")),
                         vol_digest=pick(rec, "vol_digest"), shape=pick(rec, "shape"), spacing=pick(rec, "spacing"),
                         realpath=pick(rec, "realpath"), inode=pick(rec, "inode"), device=pick(rec, "device"),
                         bytes=pick(rec, "bytes"), ledger_corpus=pick(rec, "corpus"),
                         ledger_dhash=next((rec[f] for f in LEDGER_DHASH_FIELDS if rec.get(f)), None),
                         # the ledger layer already marks blank frames and holds them out of its own duplicate
                         # count; take its word for it rather than re-deciding, or the two layers disagree
                         degenerate=("ledger: degenerate" if rec.get("degenerate") else None),
                         patient=patient_key(path, unit, pat, str(pick(rec, "alias_group") or "")),
                         ledger_patient=pat))
    if dupe_lines:
        print(f"  ledger: {dupe_lines} repeated path lines dropped (one file, one row)")
    return rows, seen_fields


# -------------------------------------------------------------------------------------------------- the stages
def stage_links(rows, edges, uf, resolve):
    """Rung 0: two paths, one file. Symlinks (Dataset813) and hard links.

    AN INODE WITHOUT A DEVICE IS NOT AN IDENTITY. Inode numbers are unique within ONE filesystem and collide
    freely across filesystems, and the grid holds at least two (the Panasas home and the CephFS volume
    /rs/rs_grp_oschome). Keying on (device, inode) with a missing device meant keying on (None, inode), so two
    unrelated files that happened to share an inode number merged under rule `same_inode` with score 1.0 -- the
    one rung with no threshold, no content check and no false-positive control. A row whose device the ledger
    did not record is now skipped and counted instead."""
    by_real, by_ino, n_res, n_nodev = {}, {}, 0, 0
    for i, r in enumerate(rows):
        rp = r.get("realpath")
        if not rp and resolve and os.path.exists(r["path"]):
            try:
                rp = posix(os.path.realpath(r["path"]))
                n_res += 1
                st = os.stat(r["path"])
                if r.get("inode") is None:
                    r["inode"], r["device"] = st.st_ino, st.st_dev
            except OSError:
                rp = None
        if rp:
            rp = posix(str(rp))
            r["realpath"] = rp
            if rp in by_real:
                if uf.union(by_real[rp], i):
                    edges.append(dict(a=by_real[rp], b=i, rule="same_realpath", score=1.0, detail=rp))
            else:
                by_real[rp] = i
        if r.get("inode") not in (None, 0):
            if r.get("device") in (None, ""):
                n_nodev += 1
                continue
            k = (r.get("device"), r.get("inode"))
            if k in by_ino:
                if uf.union(by_ino[k], i):
                    edges.append(dict(a=by_ino[k], b=i, rule="same_inode", score=1.0, detail=str(k)))
            else:
                by_ino[k] = i
    return dict(paths_resolved=n_res, realpaths=len(by_real), inode_keys=len(by_ino),
                inode_without_device_skipped=n_nodev)


def stage_exact(rows, edges, uf, field, rule):
    """Rungs 1 and 2: equality of a hash. No threshold, so no false positive EXCEPT a degenerate file, whose hash
    is shared by every other degenerate file: see EMPTY_SHA256. Those are skipped here and counted."""
    first, n, n_deg = {}, 0, 0
    for i, r in enumerate(rows):
        v = r.get(field)
        if not v:
            continue
        if r.get("degenerate") or (field == "sha256" and (str(v) == EMPTY_SHA256 or r.get("bytes") == 0)):
            n_deg += 1
            continue
        v = str(v)
        if v in first:
            if uf.union(first[v], i):
                edges.append(dict(a=first[v], b=i, rule=rule, score=1.0, detail=v[:16]))
                n += 1
        else:
            first[v] = i
    return dict(rule=rule, n_edges=n, n_keys=len(first), coverage=sum(1 for r in rows if r.get(field)),
                degenerate_skipped=n_deg)


def stage_phash(rows, edges, uf, a, report):
    """Rung 3: pHash proposes within a band bucket, NCC at 64x64 decides.

    Banded index: B bands of 64/B bits; two hashes within Hamming distance < B must share a band (pigeonhole), so
    every pair below that distance IS examined. The default (8 bands, --phash-max 6) therefore misses nothing it
    claims to cover. Buckets larger than --max-bucket are dropped and counted: a bucket that size is a blank or
    saturated image sharing every band with hundreds of others, and pairing it is O(n^2) for nothing."""
    idx = [i for i, r in enumerate(rows)
           if r["kind"] == "image" and r.get("phash") not in (None, "") and not r.get("degenerate")]
    if not idx:
        return dict(n_indexed=0, note="no image rows carry a pHash")
    width = 64 // a.bands
    mask = (1 << width) - 1
    buckets = collections.defaultdict(list)
    for i in idx:
        variants = [("o", int(rows[i]["phash"]))]
        if not a.no_mirror and rows[i].get("phash_mirror") not in (None, ""):
            variants.append(("m", int(rows[i]["phash_mirror"])))
        for var, h in variants:
            for b in range(a.bands):
                buckets[(b, (h >> (b * width)) & mask)].append((i, var))
    cand, dropped = set(), 0
    for key, mem in buckets.items():
        if len(mem) > a.max_bucket:
            dropped += 1
            continue
        for x in range(len(mem)):
            for y in range(x + 1, len(mem)):
                (i, vi), (j, vj) = mem[x], mem[y]
                if i == j:
                    continue
                cand.add((min(i, j), max(i, j), vi != vj))
    proposed, merged, rejected, unverified, already = 0, 0, [], 0, 0
    for i, j, mirrored in sorted(cand):
        # a mirrored candidate is scored as (i, mirror of j); when only i carries a mirror hash -- a ledger that
        # supplies some digests and not others -- it is scored as (mirror of i, j) instead, never with int(None)
        if mirrored:
            if rows[j].get("phash_mirror") not in (None, ""):
                hi, hj = int(rows[i]["phash"]), int(rows[j]["phash_mirror"])
            elif rows[i].get("phash_mirror") not in (None, ""):
                hi, hj = int(rows[i]["phash_mirror"]), int(rows[j]["phash"])
            else:
                continue
        else:
            hi, hj = int(rows[i]["phash"]), int(rows[j]["phash"])
        d = hamming(hi, hj)
        if d > a.phash_max:
            continue
        proposed += 1
        if uf.find(i) == uf.find(j):
            already += 1
            continue                                        # already one thing by an exact rung
        r64 = ncc(rows[i]["path"], rows[j]["path"], 64, mirrored)
        r32 = ncc(rows[i]["path"], rows[j]["path"], 32, mirrored)
        rec = dict(a=rows[i]["path"], b=rows[j]["path"], phash_d=d, ncc32=None if r32 is None else round(r32, 4),
                   ncc64=None if r64 is None else round(r64, 4), mirrored=bool(mirrored),
                   unit_a=rows[i]["unit"], unit_b=rows[j]["unit"])
        if r64 is None:
            unverified += 1
            rec["reason"] = "not verifiable here (file not readable on this host)"
            if a.merge_unverified:
                uf.union(i, j)
                edges.append(dict(a=i, b=j, rule="phash_unverified", score=float(d), detail=f"d={d}"))
                merged += 1
            else:
                rejected.append(rec)
            continue
        if r64 >= a.ncc:
            if uf.union(i, j):
                edges.append(dict(a=i, b=j, rule="phash_mirror" if mirrored else "phash",
                                  score=round(r64, 4), detail=f"d={d} ncc64={r64:.4f}"))
                merged += 1
        else:
            rec["reason"] = f"ncc64 {r64:.4f} < {a.ncc}"
            rejected.append(rec)
    rejected.sort(key=lambda r: -(r["ncc64"] or 0))
    # THE LIST IS CAPPED; THE COUNT IS NOT. res["rejected_file_pairs"] used to be len(of this capped list), so
    # once more than 5000 pairs were refused the summary printed "5000 did not" and its own arithmetic stopped
    # closing (6362 proposed = 0 already + 0 merged + 5000 refused). The false-positive control is the one number
    # in this file that must not be quietly rounded down.
    report["rejected_total"] = len(rejected)
    report["rejected_by_ncc"] = rejected[:5000]
    report["rejected_listed"] = len(report["rejected_by_ncc"])
    return dict(n_indexed=len(idx), buckets=len(buckets), buckets_dropped=dropped, candidate_pairs=len(cand),
                proposed_within_phash_max=proposed, already_one_thing=already, merged=merged, rejected=len(rejected),
                unverified=unverified, phash_max=a.phash_max, bands=a.bands, guaranteed_recall_below=a.bands,
                ncc_threshold=a.ncc)


def stage_volumes(rows, edges, uf, a):
    """Rung 4: identical subsample digest merges; equal shape+spacing only proposes, and the small arrays decide."""
    by_dig, by_geom = {}, collections.defaultdict(list)
    n_dig, n_badgeom = 0, 0
    for i, r in enumerate(rows):
        if r["kind"] != "volume":
            continue
        d = r.get("vol_digest")
        if d and r.get("degenerate"):
            d = None                                       # a constant volume: see EMPTY_SHA256
        if d:
            if d in by_dig:
                if uf.union(by_dig[d], i):
                    edges.append(dict(a=by_dig[d], b=i, rule="volume_digest", score=1.0, detail=str(d)[:16]))
                    n_dig += 1
            else:
                by_dig[d] = i
        if r.get("shape") and r.get("spacing"):
            # THE FIELD NAMES ARE READ TOLERANTLY; THE VALUES WERE NOT. A ledger that spells spacing
            # "0.7x0.7x1.0" (a CSV- or SimpleITK-derived writer) raised ValueError here, AFTER the digest pass --
            # hours of hashing on a compute node thrown away at the last stage. A geometry this file cannot parse
            # means one bucket fewer, not a dead run, so it is counted and the row keeps its digest rung.
            try:
                by_geom[(tuple(r["shape"]), tuple(round(float(x), 3) for x in r["spacing"]))].append(i)
            except (TypeError, ValueError):
                n_badgeom += 1
    n_corr, checked = 0, 0
    if a.volume_corr:
        for _, mem in by_geom.items():
            if len(mem) < 2 or len(mem) > a.max_bucket:
                continue
            small = {}
            for i in mem:
                vk = volume_key(rows[i]["path"])
                if vk:
                    small[i] = vk["small"].ravel()
            for x in range(len(mem)):
                for y in range(x + 1, len(mem)):
                    i, j = mem[x], mem[y]
                    if i not in small or j not in small or uf.find(i) == uf.find(j):
                        continue
                    A, B = small[i] - small[i].mean(), small[j] - small[j].mean()
                    den = float(np.linalg.norm(A) * np.linalg.norm(B))
                    checked += 1
                    if den > 1e-9 and float(A @ B) / den >= a.volume_corr:
                        if uf.union(i, j):
                            edges.append(dict(a=i, b=j, rule="volume_corr", score=round(float(A @ B) / den, 4),
                                              detail="same shape+spacing"))
                            n_corr += 1
    return dict(n_volumes=sum(1 for r in rows if r["kind"] == "volume"), digest_edges=n_dig,
                geometry_buckets=len(by_geom), corr_checked=checked, corr_edges=n_corr,
                unparsable_geometry=n_badgeom)


def stage_names(rows, edges, uf, a):
    """Rung 5: NAME evidence. Same patient key and same view in two different roots, ONE file per root.

    This is the only rung that can see a derived crop against the film it was cut from. It is also the only rung
    that could merge two different pictures of one patient, so the one-file-per-root rule is what keeps it honest:
    when a root holds several files under one (patient, view) key -- every frame of a C-arm sweep of case001 in the
    AP view, say -- nothing is merged and the key is counted as ambiguous, because the names do not say which frame
    pairs with which. Those cases are not lost: they are reported at PATIENT level instead (cross_root_patients),
    which is the level the split has to be drawn at anyway. Every edge here is marked `name_key`."""
    groups = collections.defaultdict(list)
    for i, r in enumerate(rows):
        if not r["patient"] or r["kind"] == "other":
            continue
        fam = family_of(r["patient"])
        # the view is in the file name for the derived banks (buu_00123_ap.png) and in the DIRECTORY for the raw
        # roots (BUU-LSPINEv1/AP/0123.jpg); without the second reading the two never share a key
        v = view_token(os.path.basename(r["path"]), fam) or view_token(os.path.dirname(r["path"]), fam)
        groups[(r["patient"], v)].append(i)
    n, skipped = 0, 0
    for (pkey, v), mem in groups.items():
        by_root = collections.defaultdict(list)
        for i in mem:
            by_root[rows[i]["root"]].append(i)
        if len(by_root) < 2:
            continue
        # ambiguity is about distinct PICTURES, not distinct paths: two files a content rung has already merged
        # (one file under two bank names) are one thing and say nothing about which frame pairs with which
        if any(len({uf.find(i) for i in x}) > 1 for x in by_root.values()):
            skipped += 1
            continue
        reps = [x[0] for x in by_root.values()]
        for k in range(1, len(reps)):
            if uf.union(reps[0], reps[k]):
                edges.append(dict(a=reps[0], b=reps[k], rule="name_key", score=0.0, detail=f"{pkey}|{v or 'noview'}"))
                n += 1
    return dict(keys=len(groups), edges=n, skipped_ambiguous_keys=skipped,
                rule="one file per root per (patient, view) key")


def patient_report(rows, gof):
    """Identity at PATIENT level, which is the level a split must be drawn at: one person reached through two roots
    is a leak even when no two files are the same picture (a cervical film here, a lumbar film there).

    This is the cross-source key docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md says does not exist: nhanes_00160 in
    ~/films_drr and NH_00160_c in ~/nhanes_drr are one person, and the bank builder split them independently."""
    by_pat = collections.defaultdict(list)
    for r in rows:
        if r["patient"]:
            by_pat[r["patient"]].append(r)
    out = []
    for pkey, mem in by_pat.items():
        roots = sorted({r["root"] for r in mem})
        if len(roots) < 2:
            continue
        units = sorted({r["unit"] for r in mem})
        cids = sorted({gof[r["path"]]["canonical_id"] for r in mem})
        # WHICH ROOTS A PICTURE IS IN, not how many ids there are. `len(cids) < len(mem)` said "same picture in
        # two roots" for a patient whose duplication is entirely INSIDE one root -- BUU-LSPINE's three "(1)"
        # files, say -- because any duplication anywhere makes ids fewer than files. That column is the one a
        # reader uses to decide whether a split leaked, so it has to mean what it says.
        roots_of_cid = collections.defaultdict(set)
        for r in mem:
            roots_of_cid[gof[r["path"]]["canonical_id"]].add(r["root"])
        out.append(dict(patient_key=pkey, n_files=len(mem), roots=roots, units=units, n_canonical_ids=len(cids),
                        spans_independent_units=len(units) > 1,
                        same_picture_in_two_roots=any(len(v) > 1 for v in roots_of_cid.values()),
                        duplicated_within_one_root=len(cids) < len(mem) and not any(len(v) > 1 for v in roots_of_cid.values()),
                        example=[r["path"] for r in mem[:4]]))
    out.sort(key=lambda d: (-len(d["roots"]), -d["n_files"], d["patient_key"]))
    return out, len(by_pat)


# ------------------------------------------------------------------------------------------------------ output
STAGE_RANK = {"raw": 0, "derived": 1, "bank": 2, "result": 3, "?": 4}


def content_key(r):
    """The key the canonical_id is derived from. A DEGENERATE DIGEST IS NOT A CONTENT KEY: every empty file
    carries EMPTY_SHA256, so two empty files that the rungs correctly refuse to merge were still handed the same
    canonical_id -- one id on two groups, which is the collision this file exists to prevent, arriving by the
    other door. Such a row is keyed by its path, which belongs to exactly one group."""
    if not r.get("degenerate"):
        for f, tag in (("sha256", "b"), ("pixel_sha256", "p"), ("vol_digest", "v")):
            v = r.get(f)
            if v and str(v) != EMPTY_SHA256:
                return f"{tag}:{v}"
        if r.get("phash") not in (None, ""):
            return f"h:{int(r['phash']):016x}"
    return f"n:{r['path']}"


def build_groups(rows, uf, edges, prev):
    members = collections.defaultdict(list)
    for i in range(len(rows)):
        members[uf.find(i)].append(i)
    ev_of = collections.defaultdict(list)
    for e in edges:
        ev_of[uf.find(e["a"])].append(e)
    name_only = set()
    touched = collections.defaultdict(list)
    for e in edges:
        touched[e["a"]].append(e["rule"])
        touched[e["b"]].append(e["rule"])
    for i, rules in touched.items():
        if all(r.startswith("name_key") for r in rules):
            name_only.add(i)
    out = []
    # AN ID CARRIED FORWARD MUST STILL BE UNIQUE. --prev let every member of a new group vote for its old id and
    # took the majority, with no check that the winner had already been handed to a different group in the SAME
    # run. So whenever a group SPLIT between runs -- --no-name-merge, a raised --ncc, a file that has moved, or
    # simply re-running the ladder off the ledger on a host where the pixels are not mounted -- both halves
    # inherited one id and canonical.jsonl then said two different pictures were one thing, which is the exact
    # error this file exists to prevent, produced by the option that exists to keep the output stable. The voted
    # id is now taken by the group with the strongest claim and refused to every other; the rest keep their
    # content-derived id, and the count of refusals is reported.
    taken, prev_reassigned = {}, 0
    for root, mem in members.items():
        # THE REPRESENTATIVE IS THE FILE TO KEEP: one that content evidence attached (never one joined by name
        # alone, which may be a crop of the others), then the earliest pipeline stage, then the path, so the choice
        # is deterministic and a rebuild does not silently move it.
        mem.sort(key=lambda i: (i in name_only, STAGE_RANK.get(rows[i]["stage"], 4), rows[i]["path"]))
        keys = sorted(content_key(rows[i]) for i in mem)
        kinds = sorted({rows[i]["kind"] for i in mem})
        cid = ("vol" if kinds == ["volume"] else "img" if kinds == ["image"] else "mix") + "-" + \
              hashlib.sha256(keys[0].encode()).hexdigest()[:16]
        votes = collections.Counter(prev[rows[i]["path"]] for i in mem if rows[i]["path"] in prev) if prev \
            else collections.Counter()
        units = sorted({rows[i]["unit"] for i in mem})
        roots = sorted({rows[i]["root"] for i in mem})
        pats = sorted({rows[i]["patient"] for i in mem if rows[i]["patient"]})
        ev = collections.Counter(e["rule"] for e in ev_of.get(root, []))
        pairs = [frozenset({units[x], units[y]}) for x in range(len(units)) for y in range(x + 1, len(units))]
        declared = bool(pairs) and all(p in SAME_POPULATION for p in pairs)
        out.append(dict(canonical_id=cid, n=len(mem), kinds=kinds, roots=roots, units=units, patient_keys=pats,
                        spans_roots=len(roots) > 1, spans_units=len(units) > 1,
                        spans_independent_units=bool(len(units) > 1 and not declared),
                        declared_same_population=declared,
                        evidence={k: int(v) for k, v in ev.items()},
                        content_evidence=bool(set(ev) - {"name_key", "name_key_same_root"}),
                        representative=rows[mem[0]]["path"],
                        members=[rows[i]["path"] for i in mem],
                        member_units=[rows[i]["unit"] for i in mem],
                        edges=[dict(a=rows[e["a"]]["path"], b=rows[e["b"]]["path"], rule=e["rule"],
                                    score=e["score"], detail=e["detail"]) for e in ev_of.get(root, [])],
                        _root=root, _cidc=cid, _votes=votes))
    # Content keys are unique per group in every case this file can construct, but a ledger that lists ONE path
    # twice (two shard files concatenated, a resume that re-appended) can hand two groups the key `n:<that path>`.
    # A duplicate id is resolved and counted here rather than asserted, because a 1M-row run that has already
    # paid for the digest pass must not die at the last stage over a ledger it did not write.
    n_dup_keys = 0
    for g in sorted(out, key=lambda g: g["_cidc"]):
        cid = g["_cidc"]
        if cid in taken:
            n = 2
            while f"{cid}~{n}" in taken:
                n += 1
            cid = f"{cid}~{n}"
            g["canonical_id"] = cid
            n_dup_keys += 1
        taken[cid] = g
    if prev:
        ranked = []
        for g in out:
            if g["_votes"]:
                old, n = sorted(g["_votes"].items(), key=lambda kv: (-kv[1], kv[0]))[0]
                ranked.append((-n, g["_cidc"], old, g))
        for _, _, old, g in sorted(ranked, key=lambda t: (t[0], t[1])):
            if old in taken:
                prev_reassigned += 1                       # another group has the stronger claim on that id
                continue
            taken.pop(g["canonical_id"], None)
            g["canonical_id"] = old
            taken[old] = g
    for g in out:
        g.pop("_cidc", None)
        g.pop("_votes", None)
    if len({g["canonical_id"] for g in out}) != len(out):   # must never happen: an id that is not an identity
        raise RuntimeError("canonical_id is not unique across groups -- refusing to write it")
    return out, prev_reassigned, n_dup_keys


def known_alias_check(rows, groups):
    out = []
    for ka in KNOWN_ALIASES:
        ra, rb = re.compile(ka["a"]), re.compile(ka["b"])
        na = sum(1 for r in rows if ra.search(r["path"]))
        nb = sum(1 for r in rows if rb.search(r["path"]))
        hit = [g for g in groups if any(ra.search(m) for m in g["members"]) and any(rb.search(m) for m in g["members"])]
        out.append(dict(name=ka["name"], note=ka["note"], members_side_a=na, members_side_b=nb,
                        found=bool(hit), n_groups=len(hit),
                        n_files_merged=sum(g["n"] for g in hit),
                        example=hit[0]["members"][:2] if hit else None,
                        why_not=None if hit else ("side A absent from the ledger" if not na else
                                                  "side B absent from the ledger" if not nb else
                                                  "both sides present, NO group joins them -- either they are not the "
                                                  "same files or every rung missed them")))
    return out


def write_markdown(path, res, groups):
    cross = sorted([g for g in groups if g["spans_roots"]], key=lambda g: -g["n"])
    L = []
    L.append("# Alias groups: which files in the ledger are one picture or one scan\n")
    L.append(f"Generated {res['generated']} by `tools/data_alias.py` from `{res['ledger']}`.\n")
    c = res["counts"]
    L.append(f"{c['rows']} ledger rows -> {c['groups']} canonical ids; {c['multi_groups']} groups hold more than one "
             f"file ({c['aliased_files']} files), {c['cross_root_groups']} of those span more than one root and "
             f"{c['cross_unit_groups']} span analysis units the figures treat as independent.\n")
    t = res["thresholds"]
    L.append(f"Thresholds: pHash Hamming <= {t['phash_max']} over {t['bands']} bands (every pair below distance "
             f"{t['bands']} is examined), confirmed by NCC64 >= {t['ncc']}; volume correlation >= {t['volume_corr']}; "
             f"mirrored copies {'indexed' if t['mirror'] else 'NOT indexed'}; name evidence "
             f"{'used' if t['name_merge'] else 'off'}.\n")
    L.append("\n## Cross-root groups, largest first\n")
    if not cross:
        L.append("None. Either the ledger holds one root, or nothing is duplicated across roots.\n")
    else:
        L.append("| n | canonical_id | roots | analysis units | evidence | independent units? | representative (the copy to keep) |")
        L.append("|---:|---|---|---|---|---|---|")
        for g in cross[:200]:
            ev = ", ".join(f"{k} x{v}" for k, v in sorted(g["evidence"].items()))
            L.append(f"| {g['n']} | `{g['canonical_id']}` | {', '.join(g['roots'])} | {', '.join(g['units'])} | "
                     f"{ev or '-'} | {'**YES**' if g['spans_independent_units'] else 'no'} | `{g['representative']}` |")
        if len(cross) > 200:
            L.append(f"\n... and {len(cross) - 200} more in alias_groups.json.\n")
    nameonly = [g for g in cross if not g["content_evidence"]]
    L.append(f"\n{len(nameonly)} of those cross-root groups rest on NAME evidence alone (same patient key and view in "
             "two roots, no pixel evidence at all). A derived crop does not match its parent film by pixels, so name "
             "evidence is the only thing that can join them; it is also the one rung that could merge two different "
             "pictures of one patient, so it is separated out here and can be switched off with `--no-name-merge`.\n")
    if nameonly:
        L.append("| n | canonical_id | roots | representative |")
        L.append("|---:|---|---|---|")
        for g in sorted(nameonly, key=lambda g: -g["n"])[:50]:
            L.append(f"| {g['n']} | `{g['canonical_id']}` | {', '.join(g['roots'])} | `{g['representative']}` |")
        # EVERY TABLE HERE SAYS HOW MUCH OF ITSELF IT IS SHOWING. This one and the patient table below were cut
        # silently, so a reader counting rows read 50 name-only groups where the run had found several hundred --
        # and this document is the copy anybody actually reads.
        if len(nameonly) > 50:
            L.append(f"\n... and {len(nameonly) - 50} more, in alias_groups.json.\n")
    L.append("\n## The same patient through two roots\n")
    pats = res.get("cross_root_patients", [])
    L.append(f"{res['counts']['patients_keyed']} patient keys were recognised over "
             f"{res['counts']['rows'] - res['counts']['files_without_patient_key']} files "
             f"({res['counts']['files_without_patient_key']} files carry no key this tool knows). "
             f"{res['counts']['cross_root_patients']} patients are reached through more than one root. A split drawn "
             "per root or per source puts those two copies on the two sides independently, which is how 48 of 54 "
             "NHANES validation patients came to have their duplicate in training.\n")
    if pats:
        L.append("| patient key | files | canonical ids | roots | analysis units | one picture in two roots? |")
        L.append("|---|---:|---:|---|---|---|")
        for p in pats[:100]:
            same = ("yes" if p["same_picture_in_two_roots"] else
                    "no (but duplicated inside one root)" if p.get("duplicated_within_one_root") else "no")
            L.append(f"| `{p['patient_key']}` | {p['n_files']} | {p['n_canonical_ids']} | {', '.join(p['roots'])} | "
                     f"{', '.join(p['units'])} | {same} |")
        cut = (int(res.get("cross_root_patients_truncated", 0))
               or max(0, int(res["counts"]["cross_root_patients"]) - len(pats)))
        if cut or len(pats) > 100:
            L.append(f"\n... and {cut + max(0, len(pats) - 100)} more, in alias_groups.json "
                     "(--max-members controls how many are kept there).\n")
    L.append("\n## Known aliases, checked on every canon run\n")
    L.append("| alias | files side A | files side B | found | groups | note |")
    L.append("|---|---:|---:|---|---:|---|")
    for k in res["known_aliases"]:
        L.append(f"| {k['name']} | {k['members_side_a']} | {k['members_side_b']} | "
                 f"{'yes' if k['found'] else '**NO** (' + str(k['why_not']) + ')'} | {k['n_groups']} | {k['note']} |")
    L.append("\n## False-positive control: pHash proposals the NCC refused\n")
    rej = res.get("rejected_by_ncc", [])
    ph = res["stages"]["phash"]
    listed, total = res.get("rejected_file_pairs_listed", len(rej)), res.get("rejected_file_pairs", len(rej))
    L.append(f"{ph.get('proposed_within_phash_max', 0)} file pairs came within the pHash threshold; "
             f"{ph.get('already_one_thing', 0)} of them were already one thing by an exact rung, "
             f"{ph.get('merged', 0)} passed NCC64 and merged, {total} did not"
             + (f" (of which {listed} are kept in alias_groups.json; the rest are counted, not listed)"
                if listed < total else "")
             + f", over {res.get('rejected_group_pairs', len(rej))} distinct pairs of groups"
             + (f", and {ph.get('unverified', 0)} could not be checked here because the files were not readable on "
                "this host (those are NOT merged; run this where the data is).\n" if ph.get("unverified") else ".\n"))
    L.append("pHash proposes and NCC decides. A refused pair is two subjects imaged the same way: exactly what a "
             "32x32 correlation confuses, and the reason pHash is never allowed to merge anything on its own. If "
             "this list is empty the gate was never exercised -- that is not evidence that it works.\n"
             if not rej else
             "pHash proposes and NCC decides; each row below is a pair that looked alike and is not the same "
             "picture. Read a few: if any of them IS the same picture, the NCC threshold is too high.\n")
    if rej:
        L.append("| ncc64 | ncc32 | pHash d | file pairs | a | b |")
        L.append("|---:|---:|---:|---:|---|---|")
        for r in rej[:25]:
            L.append(f"| {r['ncc64']} | {r['ncc32']} | {r['phash_d']} | {r.get('file_pairs', 1)} | `{r['a']}` | `{r['b']}` |")
        if len(rej) > 25:
            L.append(f"\nThe 25 nearest misses of {res.get('rejected_group_pairs_listed', len(rej))} listed here "
                     f"(of {res.get('rejected_group_pairs', len(rej))} pairs of groups refused); the rest are in "
                     "alias_groups.json.\n")
    if c.get("degenerate_files") or c.get("empty_files"):
        L.append(f"\n### Files with no identity to assert\n\n{c.get('empty_files', 0)} files are empty and "
                 f"{c.get('degenerate_files', 0)} decode to a blank (constant) image or volume. Every empty file "
                 "shares one byte hash and every blank render of one canvas shares one pixel hash, so on the "
                 "exact rungs they would all merge into a single 'picture' spanning every corpus that holds one. "
                 "They are counted here and merged with nothing. That is not the same as being unique.\n")
    L.append("\n## What this cannot see\n")
    L.append("- A copy whose grey mapping was changed (inverted, re-windowed) or that was rotated: pHash moves far "
             "and NCC falls. Only the name rung would catch it.\n"
             "- A crop tight enough to lose the pHash whose name shares no patient key with its parent.\n"
             "- Any corpus whose patient key is not in `patient_key()`; those rows carry `patient: \"\"` and the "
             "name rung never fires for them.\n"
             "- A device pair store is named by DEVICE, not by corpus, so its case key is scoped to the device "
             "(`device:surgio_b51:case012`) and it does not join its corpus's patient in the table above. It joins "
             "its realxray copy by content instead, which is the row in the group table.\n"
             "- A CONTAINER holding many frames is one row and can only match another container. The DeepFluoro h5 "
             "(366 frames in one file) therefore cannot be matched frame by frame against the vendor DICOMs; the "
             "two roots meet at specimen level in the patient table above, and frame by frame only through the "
             "per-frame export under `realxray/deepfluoro`.\n")
    un = res.get("unreadable") or {}
    if un.get("by_extension"):
        L.append("\n### Files no reader here could open\n")
        L.append("| extension | files |")
        L.append("|---|---:|")
        for k, v in sorted(un["by_extension"].items(), key=lambda kv: -kv[1]):
            L.append(f"| `{k}` | {v} |")
        L.append("\nThese merged with nothing, and that is not the same as being unique. `.dcm` needs pydicom; "
                 "`.h5`/`.hdf5` are containers this tool does not open.\n")
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------------- canon
def cmd_canon(a):
    t0 = time.time()
    print(f"ledger: {a.ledger}")
    rows, seen = load_rows(a.ledger, a.only_root, a.skip_root, a.only_kind)
    if not rows:
        print("no usable rows (every record needs a path field)")
        return 2
    print(f"{len(rows)} rows; fields present in the ledger: " +
          ", ".join(f"{k}={v}" for k, v in sorted(seen.items())))
    by_kind = collections.Counter(r["kind"] for r in rows)
    print("kinds: " + ", ".join(f"{k}={v}" for k, v in by_kind.most_common()))
    print("roots: " + ", ".join(f"{k}={v}" for k, v in collections.Counter(r["root"] for r in rows).most_common(12)))
    n_unclass = sum(1 for r in rows if r["unit"].startswith("unclassified"))
    n_dhash = sum(1 for r in rows if r.get("ledger_dhash"))
    if n_dhash and not any(r.get("phash") not in (None, "") for r in rows):
        print(f"  {n_dhash} rows carry a ledger `dhash`. That is a DIFFERENCE hash, not the DCT pHash this file "
              f"uses, so it is deliberately NOT read as one -- mixing the two would put every pair about 32 bits "
              f"apart and still report full coverage. Rung 3 needs --pixels on a host that can open the files.")
    if n_unclass:
        print(f"  {n_unclass} rows matched no rule in ROOT_RULES (unit 'unclassified'); they can still merge by "
              f"content but carry no independence claim")

    # --- digests: from the ledger where it has them, computed here where it does not
    unreadable = {}
    need = [i for i, r in enumerate(rows)
            if r["kind"] in ("image", "volume")
            and ((r["kind"] == "image" and (r.get("phash") in (None, "") or not r.get("pixel_sha256")))
                 or (r["kind"] == "volume" and not r.get("vol_digest"))
                 or (a.hash_bytes and not r.get("sha256")))]
    if a.pixels and need:
        jobs = [(i, rows[i]["path"], rows[i]["kind"], bool(a.hash_bytes and not rows[i].get("sha256"))) for i in need]
        print(f"computing digests for {len(jobs)} rows with {a.workers} worker(s) ...", flush=True)
        results = []
        if a.workers > 1:
            from multiprocessing import Pool
            with Pool(a.workers) as pool:
                for k, out in enumerate(pool.imap_unordered(digest_one, jobs, chunksize=16), 1):
                    results.append(out)
                    if k % 5000 == 0:
                        print(f"  {k}/{len(jobs)}", flush=True)
        else:
            for k, j in enumerate(jobs, 1):
                results.append(digest_one(j))
                if k % 5000 == 0:
                    print(f"  {k}/{len(jobs)}", flush=True)
        errs, unread_ext, deg = collections.Counter(), collections.Counter(), collections.Counter()
        for out in results:
            if out.get("err"):
                errs[out["err"].split(":")[0]] += 1
                p = rows[out["i"]]["path"].lower()
                unread_ext[".nii.gz" if p.endswith(".nii.gz") else (os.path.splitext(p)[1] or "(none)")] += 1
            if out.get("degenerate"):
                deg[out["degenerate"]] += 1
            for k in ("sha256", "pixel_sha256", "phash", "phash_mirror", "vol_digest", "shape", "spacing",
                      "degenerate"):
                if out.get(k) is not None:
                    rows[out["i"]][k] = out[k]
        if deg:
            print("  blank / constant files (counted, never merged on content): " +
                  ", ".join(f"{k} x{v}" for k, v in deg.most_common()))
        if errs:
            print("  digest problems: " + ", ".join(f"{k} x{v}" for k, v in errs.most_common()))
            # BY EXTENSION, because that is what says which reader is missing. A whole corpus that quietly read as
            # nothing merges with nothing and looks clean.
            print("  unreadable by extension: " + ", ".join(f"{k} x{v}" for k, v in unread_ext.most_common(10)))
        unreadable = dict(by_reason=dict(errs.most_common()), by_extension=dict(unread_ext.most_common()))
    elif need:
        print(f"{len(need)} rows lack a digest and --pixels was not given: rungs 2-4 will cover only what the ledger "
              f"already carried")
    cov = dict(byte=sum(1 for r in rows if r.get("sha256")), pixel=sum(1 for r in rows if r.get("pixel_sha256")),
               phash=sum(1 for r in rows if r.get("phash") not in (None, "")),
               volume=sum(1 for r in rows if r.get("vol_digest")))
    print("digest coverage: " + ", ".join(f"{k}={v}" for k, v in cov.items()))

    # --- the ladder
    uf, edges, report = UF(len(rows)), [], {}
    st = {}
    st["links"] = stage_links(rows, edges, uf, a.resolve_links)
    st["byte"] = stage_exact(rows, edges, uf, "sha256", "byte_sha256")
    st["pixel"] = stage_exact(rows, edges, uf, "pixel_sha256", "pixel_sha256")
    st["phash"] = stage_phash(rows, edges, uf, a, report)
    st["volume"] = stage_volumes(rows, edges, uf, a)
    st["name"] = stage_names(rows, edges, uf, a) if not a.no_name_merge else dict(edges=0, note="--no-name-merge")
    for k, v in st.items():
        print(f"  stage {k:<7} {json.dumps(v)[:200]}")

    prev = {}
    if a.prev and os.path.exists(a.prev):
        for rec in read_ledger(a.prev):
            if rec.get("path") and rec.get("canonical_id"):
                prev[posix(rec["path"])] = rec["canonical_id"]
        print(f"carried {len(prev)} canonical ids forward from {a.prev}")

    groups, prev_reassigned, n_dup_keys = build_groups(rows, uf, edges, prev)
    if n_dup_keys:
        print(f"  {n_dup_keys} groups shared a content key with another group (the ledger lists one path more "
              f"than once); their ids carry a '~n' suffix so no two groups share an id")
    if prev_reassigned:
        print(f"  --prev: {prev_reassigned} groups could NOT keep their old canonical_id because another group in "
              f"this run has a stronger claim on it (a group that SPLIT since the previous run); those keep their "
              f"content-derived id, so no two things share an id")
    gof = {}
    for g in groups:
        for m in g["members"]:
            gof[m] = g
    multi = [g for g in groups if g["n"] > 1]
    cross = [g for g in multi if g["spans_roots"]]
    xunit = [g for g in multi if g["spans_independent_units"]]
    pats, n_pat = patient_report(rows, gof)
    counts = dict(rows=len(rows), groups=len(groups), multi_groups=len(multi),
                  aliased_files=sum(g["n"] for g in multi), cross_root_groups=len(cross),
                  cross_unit_groups=len(xunit), name_only_groups=sum(1 for g in multi if not g["content_evidence"]),
                  patients_keyed=n_pat, cross_root_patients=len(pats),
                  files_without_patient_key=sum(1 for r in rows if not r["patient"]),
                  degenerate_files=sum(1 for r in rows if r.get("degenerate")),
                  empty_files=sum(1 for r in rows if r.get("bytes") == 0 or r.get("sha256") == EMPTY_SHA256),
                  unit_scoped_patient_keys=sum(1 for r in rows if str(r["patient"]).endswith("#unitscoped")),
                  prev_ids_refused=prev_reassigned, duplicate_content_keys=n_dup_keys)

    os.makedirs(a.out, exist_ok=True)
    cpath = os.path.join(a.out, "canonical.jsonl")
    with open(cpath, "w", encoding="utf-8") as fh:
        for r in rows:
            g = gof[r["path"]]
            fh.write(json.dumps(dict(path=r["path"], canonical_id=g["canonical_id"], kind=r["kind"], root=r["root"],
                                     analysis_unit=r["unit"], stage=r["stage"], patient_key=r["patient"],
                                     group_size=g["n"], representative=(g["representative"] == r["path"]),
                                     group_roots=g["roots"], group_units=g["units"],
                                     evidence=sorted(g["evidence"]),
                                     spans_independent_units=g["spans_independent_units"],
                                     sha256=r.get("sha256"), pixel_sha256=r.get("pixel_sha256"),
                                     phash=None if r.get("phash") in (None, "") else f"{int(r['phash']):016x}",
                                     phash_mirror=None if r.get("phash_mirror") in (None, "") else f"{int(r['phash_mirror']):016x}",
                                     shape=r.get("shape"), spacing=r.get("spacing"),
                                     vol_digest=r.get("vol_digest"))) + "\n")
    res = dict(generated=time.strftime("%Y-%m-%d %H:%M"), ledger=str(a.ledger), host=os.environ.get("HOSTNAME", ""),
               thresholds=dict(phash_max=a.phash_max, bands=a.bands, ncc=a.ncc, volume_corr=a.volume_corr,
                               mirror=not a.no_mirror, name_merge=not a.no_name_merge,
                               merge_unverified=bool(a.merge_unverified)),
               counts=counts, digest_coverage=cov, unreadable=unreadable, stages=st, seconds=int(time.time() - t0))
    res["known_aliases"] = known_alias_check(rows, groups)
    # one row per pair of THINGS, not per pair of files: nine members of one group against two of another is one
    # refusal repeated eighteen times, and a list like that does not get read
    collapsed = {}
    for r in report.get("rejected_by_ncc", []):
        key = tuple(sorted((gof[r["a"]]["canonical_id"], gof[r["b"]]["canonical_id"])))
        cur = collapsed.get(key)
        if cur is None:
            collapsed[key] = dict(r, file_pairs=1)
        else:
            cur["file_pairs"] += 1
            if (r["ncc64"] or 0) > (cur["ncc64"] or 0):
                collapsed[key] = dict(r, file_pairs=cur["file_pairs"])
    res["rejected_by_ncc"] = sorted(collapsed.values(), key=lambda r: -(r["ncc64"] or 0))[:400]
    res["rejected_file_pairs"] = int(report.get("rejected_total", len(report.get("rejected_by_ncc", []))))
    res["rejected_file_pairs_listed"] = int(report.get("rejected_listed", len(report.get("rejected_by_ncc", []))))
    res["rejected_group_pairs"] = len(collapsed)
    res["rejected_group_pairs_listed"] = len(res["rejected_by_ncc"])
    res["cross_root_patients"] = pats[:a.max_members]
    res["cross_root_patients_truncated"] = max(0, len(pats) - a.max_members)
    keep = sorted(multi, key=lambda g: (-g["n"], g["canonical_id"]))
    for g in keep:
        g.pop("_root", None)
        if len(g["members"]) > a.max_members:
            g["members_truncated"] = len(g["members"]) - a.max_members
            g["members"] = g["members"][:a.max_members]
            g["member_units"] = g["member_units"][:a.max_members]
        if len(g["edges"]) > 50:
            g["edges"] = g["edges"][:50]
    res["groups"] = keep
    gpath = os.path.join(a.out, "alias_groups.json")
    json.dump(res, open(gpath, "w", encoding="utf-8"), indent=1)
    epath = os.path.join(a.out, "alias_edges.csv")
    with open(epath, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rule", "score", "detail", "a_path", "b_path", "a_root", "b_root", "a_unit", "b_unit"])
        for e in edges:
            w.writerow([e["rule"], e["score"], e["detail"], rows[e["a"]]["path"], rows[e["b"]]["path"],
                        rows[e["a"]]["root"], rows[e["b"]]["root"], rows[e["a"]]["unit"], rows[e["b"]]["unit"]])
    mpath = os.path.join(a.out, "ALIAS_SUMMARY.md")
    write_markdown(mpath, res, groups)

    print(f"\n{counts['rows']} files -> {counts['groups']} canonical ids")
    print(f"{counts['multi_groups']} alias groups covering {counts['aliased_files']} files; "
          f"{counts['cross_root_groups']} span roots; {counts['cross_unit_groups']} span units the analyses treat as "
          f"independent; {counts['name_only_groups']} rest on name evidence alone")
    print(f"{counts['patients_keyed']} patient keys; {counts['cross_root_patients']} patients reached through more "
          f"than one root; {counts['files_without_patient_key']} files carry no patient key")
    print("known aliases:")
    for k in res["known_aliases"]:
        mark = "found" if k["found"] else "NOT FOUND"
        print(f"  [{mark:>9}] {k['name']}  (A {k['members_side_a']} files, B {k['members_side_b']} files"
              f"{'' if k['found'] else '; ' + str(k['why_not'])})")
    for p in (cpath, gpath, epath, mpath):
        print("wrote", p)
    if a.fail_on_cross_unit and xunit:
        print(f"FAIL: {len(xunit)} groups span analysis units treated as independent")
        return 1
    return 0


# ------------------------------------------------------------------------------------------------------ paths
# THE EXAMPLE SET IS DERIVED, NOT CHOSEN. It used to be a hand-written list of 21 paths, and a hand-written list
# holds exactly the corpora somebody remembered: it covered 12 of the 32 sets in tools/corpus_manifold.py and 3 of
# the 12 roots in tools/data_manifest.py, it printed "0 matched no rule in ROOT_RULES" every time, and the corpus
# most likely to be missing from it was the corpus whose rule was missing too -- the one case this command exists
# to find. One example per corpus is now built FROM those two tables, so a corpus with no rule fails this command
# instead of being absent from it, and adding a corpus to either table adds it here.
#
#   corpus_manifold.py SETS   the corpora Figure 1 row (d) plots as independent. Its `glob` / `rglob` / `pairs`
#                             say where each one lives; the analysis unit classify() returns for a path under it
#                             MUST be that SETS key, because "this alias group spans independent units" is a
#                             statement about exactly those names.
#   data_manifest.py ROOTS    the dataset roots Table 1 is checked against. ROOTS records a root's PATH and not
#                             its internal layout, so the example is <root>/ANY/0001.png -- one directory level
#                             in, which every corpus here has -- and that is said in the output rather than
#                             presented as a file that exists.
#
# Neither table is imported for its data alone: a wildcard is filled with a token that cannot decide the answer.
# The film banks are keyed on the STEM PREFIX (`yolo_v3/images/*/buu_*`), so a wildcard filled with `buu_0001`
# would make every detector bank classify as BUU-LSPINE and the dry run would pass by construction a second time.
DIR_TOKEN, FILE_STEM = "ANY", "0001"


def _expand_call(node, ns):
    import ast
    fn = node.func
    name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
    if name == "expanduser" and node.args:
        return os.path.expanduser(str(_literal_node(node.args[0], ns)))
    if name == "dict":
        return {kw.arg: _literal_node(kw.value, ns) for kw in node.keywords}
    return None


def _literal_node(node, ns):
    """Enough of a literal reader for the two tables: constants, names, f-strings, dicts and dict() calls."""
    import ast
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return ns.get(node.id)
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                out.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                got = _literal_node(v.value, ns)
                if got is None:
                    return None
                out.append(str(got))
            else:
                return None
        return "".join(out)
    if isinstance(node, ast.Dict):
        return {_literal_node(k, ns): _literal_node(v, ns) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Call):
        return _expand_call(node, ns)
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_literal_node(e, ns) for e in node.elts]
    return None


def _read_assignments(path, names):
    """Module-level assignments read out of the SOURCE, for a host where the module will not import.

    tools/corpus_manifold.py imports numpy and two device modules at module level. If any of those is missing the
    import raises, and the ONLY acceptable answer then is still the whole table: falling back to a shorter list
    would be the original defect wearing a different hat. So the table is parsed instead, and which way it was
    read is printed.
    """
    import ast
    tree = ast.parse(open(path, encoding="utf-8").read())
    ns, want = {}, {}
    for st in tree.body:
        if not isinstance(st, ast.Assign):
            continue
        for tgt in st.targets:
            if isinstance(tgt, ast.Name):
                ns[tgt.id] = _literal_node(st.value, ns)
                if tgt.id in names:
                    want[tgt.id] = ns[tgt.id]
    return want


def corpus_tables():
    """(SETS, STYLED, ROOTS, how) -- imported where the modules import, parsed out of the source where they do not."""
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        import corpus_manifold as CM
        import data_manifest as DM
        return dict(CM.SETS), CM.STYLED, dict(DM.ROOTS), "imported"
    except Exception as e:                                  # noqa: BLE001
        cm = _read_assignments(os.path.join(here, "corpus_manifold.py"), {"SETS", "STYLED"})
        dm = _read_assignments(os.path.join(here, "data_manifest.py"), {"ROOTS"})
        return (cm.get("SETS") or {}), cm.get("STYLED"), (dm.get("ROOTS") or {}), f"read from source ({type(e).__name__})"


def example_from_pattern(pat, is_dir=False, leaf=f"{FILE_STEM}.png"):
    """One concrete path from a glob (or from a directory, with `leaf` appended). Wildcards become fixed tokens.

    A directory wildcard becomes `ANY` and a file wildcard becomes `0001`, neither of which is a corpus name: the
    point is to exercise the RULE, and a token that looks like a corpus would answer the question it is asking.
    """
    s = posix(str(pat))
    if is_dir:
        s = s.rstrip("/") + "/" + leaf
    out = []
    parts = s.split("/")
    for i, seg in enumerate(parts):
        if not re.search(r"[*?\[]", seg):
            out.append(seg)
            continue
        if i < len(parts) - 1:
            out.append(re.sub(r"\[[^\]]*\]|[*?]+", DIR_TOKEN, seg))
            continue
        name, dot, ext = seg.rpartition(".")
        if not dot:
            name, ext = seg, ""
        name = re.sub(r"\[[^\]]*\]|[*?]+", FILE_STEM, name)
        ext = re.sub(r"\[[^\]]*\]|[*?]+", "png", ext)
        out.append(f"{name}.{ext}" if ext else f"{name}.png")
    s = "/".join(out)
    if "." not in os.path.basename(s):
        s += ".png"
    return s


def coverage_cases():
    """One case per corpus, from the two tables. Returns (rows, how the tables were read).

    A row is (source table, corpus name, expected analysis unit or None, example path, note).
    `expected` is set only where the table's name IS the unit name -- that is the promise ROOT_RULES makes about
    corpus_manifold SETS. data_manifest ROOTS names a root, not an analysis unit, so those rows only require that
    SOME rule matches.
    """
    sets, styled, roots, how = corpus_tables()
    rows = []
    for name, spec in sorted((sets or {}).items()):
        spec = spec if isinstance(spec, dict) else {}
        if spec.get("glob"):
            p, note = example_from_pattern(spec["glob"]), ""
        elif spec.get("rglob"):
            p, note = example_from_pattern(spec["rglob"], is_dir=True, leaf="PMC7123456_fig2_a.jpg"), "rglob root"
        elif spec.get("pairs"):
            p, note = example_from_pattern(spec["pairs"], is_dir=True, leaf="case07_p003.npz"), "pair store"
        else:
            rows.append(("corpus_manifold SETS", name, name, "", "no glob/rglob/pairs in the table"))
            continue
        rows.append(("corpus_manifold SETS", name, name, p, note))
    if styled:
        rows.append(("corpus_manifold STYLED", "styled <device>", "styled ", example_from_pattern(styled),
                     "one corpus per <geometry>__<noise>, added at run time"))
    for name, meta in sorted((roots or {}).items()):
        p = (meta or {}).get("path") if isinstance(meta, dict) else None
        if not p:
            rows.append(("data_manifest ROOTS", name, None, "", "no path in the table"))
            continue
        rows.append(("data_manifest ROOTS", name, None,
                     example_from_pattern(p, is_dir=True, leaf=f"{DIR_TOKEN}/{FILE_STEM}.png"),
                     "layout not in data_manifest.py: example is one level in"))
    return rows, how


# The cross-root joins THIS FILE's own rules and comments name, each with the key it must produce. They are
# assertions, not illustrations: the NHANES defect was a patient reached under two spellings, and a dry run that
# only printed what it computed could not tell anybody that the two spellings had stopped meeting.
KEY_CASES = [
    ("NHANES II raw TIFF", "~/spine-detector/data/raw/nhanes_full/00160.tiff", "nhanes:00160"),
    ("NHANES II detector crop", "~/spine-detector/data/yolo_v3/images/train/nhanes_00160_c.png", "nhanes:00160"),
    ("NHANES II in films_drr", "~/films_drr/ann/nhanes_00160_c.json", "nhanes:00160"),
    ("NHANES II in nhanes_drr, the second copy", "~/nhanes_drr/img/NH_00160_c.npy", "nhanes:00160"),
    ("NHANES II source pickle", "~/nhanes_drr/src/C00160_cervical_masks_4.pkl", "nhanes:00160"),
    ("BUU-LSPINE raw AP film", "~/spine-detector/data/raw/buu_full/BUU-LSPINEv1/AP/0123.jpg", "buu:00123"),
    ("BUU-LSPINE detector crop", "~/spine-detector/data/yolo_v3/images/train/buu_00123_ap.png", "buu:00123"),
    ("CSXA raw film", "~/spine-detector/data/raw/csxa/images/datasets-PNG/0421.png", "csxa:0421"),
    ("CSXA detector crop", "~/spine-detector/data/yolo_v3/images/val/csxa_0421.png", "csxa:0421"),
    ("Mendeley detector crop", "~/spine-detector/data/yolo_v3/images/train/mendeley_0007.png", "mendeley:00007"),
    ("CTSpinoPelvic1K release CT", "~/data/CTSpinoPelvic1K/ct/0001.nii.gz", "ctsp:0001"),
    ("CTSpinoPelvic1K, the old CSV spelling of the same case", "~/data/CTSpinoPelvic1K/ct/1.nii.gz", "ctsp:0001"),
    ("CTSpinoPelvic1K through the Dataset813 link",
     "~/nnUNet_raw/Dataset813_LSTV/imagesTr/CTSP_0001_0000.nii.gz", "ctsp:0001"),
    ("DeepFluoro h5 specimen", "~/deepfluoro/unpacked_full/17-1882/frame_000.png", "deepfluoro:17-1882"),
    ("DeepFluoro vendor DICOM of that specimen",
     "/rs/rs_grp_oschome/go2432/data/deepfluoro_vendor/unpacked/17-1882/IM000001.dcm", "deepfluoro:17-1882"),
    ("TotalSegmentator subject",
     "~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300/s0123/ct.nii.gz", "ts:s0123"),
    ("a case number is scoped to its corpus",
     "/rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images/train/case012_ap_f004.png", "carmlspine:case012"),
    ("a device pair store is scoped to the DEVICE, not to a corpus",
     "/rs/rs_grp_oschome/go2432/data/or_ready/devices/varian_halcyon/pairs/case07_p003.npz",
     "device:varian_halcyon:case07"),
    ("a literature figure panel names no patient, and is not given one",
     "~/FluoroCap/panels/PMC7123456_fig2_a.jpg", ""),
]


def classify_row(p):
    pp = posix(os.path.expanduser(p)) if str(p).startswith("~") else posix(p)
    root, unit, stage = classify(pp)
    pk = patient_key(pp, unit)
    view = view_token(os.path.basename(pp), family_of(pk)) or view_token(os.path.dirname(pp), family_of(pk))
    return pp, root, unit, stage, pk, view


def cmd_paths(a):
    if a.file:
        print(f"{'root':<22} {'analysis unit':<34} {'stage':<8} {'patient key':<20} {'view':<5} path")
        n_un = 0
        for line in open(a.file, encoding="utf-8"):
            p = line.strip()
            if not p:
                continue
            pp, root, unit, stage, pk, view = classify_row(p)
            n_un += unit.startswith("unclassified")
            print(f"{root:<22} {unit:<34} {stage:<8} {pk or '-':<20} {view or '-':<5} {p}")
        print(f"\n{n_un} of the paths in {a.file} matched no rule in ROOT_RULES")
        return 1 if (n_un and not a.allow_gaps) else 0

    rows, how = coverage_cases()
    print(f"corpora taken from tools/corpus_manifold.py SETS and tools/data_manifest.py ROOTS ({how})")
    print(f"{len(rows)} corpora to classify; the example path is BUILT from each table's own glob or root, with "
          f"'{DIR_TOKEN}' for a directory wildcard and '{FILE_STEM}' for a file one\n")
    print(f"{'':<6} {'corpus':<26} {'root':<22} {'analysis unit':<34} {'patient key':<20} example")
    gaps, wrong = [], []
    for src, name, expect, p, note in rows:
        if not p:
            gaps.append((name, src, note))
            print(f"{'FAIL':<6} {name:<26} {'-':<22} {'-':<34} {'-':<20} {note}")
            continue
        pp, root, unit, stage, pk, _ = classify_row(p)
        bad = ""
        if unit.startswith("unclassified"):
            bad = "no rule in ROOT_RULES"
            gaps.append((name, src, bad))
        elif expect and not (unit == expect or (expect.endswith(" ") and unit.startswith(expect))):
            bad = f"unit is {unit!r}, the table calls this corpus {expect!r}"
            wrong.append((name, src, bad))
        print(f"{'FAIL' if bad else 'ok':<6} {name:<26} {root:<22} {unit:<34} {pk or '-':<20} {pp}")
        if a.verbose:
            print(f"{'':<6} from {src}" + (f"   ({note})" if note else "") + (f"   <- {bad}" if bad else ""))

    print(f"\n{len(rows)} corpora: {len(gaps)} have NO rule in ROOT_RULES, {len(wrong)} resolve to an analysis "
          f"unit the table does not call them.")
    if gaps:
        print("CORPORA WITH NO RULE (every file of these carries unit 'unclassified:<parent directory>', so a "
              "duplicate between two of them spans no units and appears in no table of ALIAS_SUMMARY.md):")
        for name, src, why in gaps:
            print(f"    {name}   [{src}]   {why}")
    if wrong:
        print("CORPORA WHOSE RULE NAMES A DIFFERENT UNIT (a group spanning these is measured against the wrong "
              "independence claim):")
        for name, src, why in wrong:
            print(f"    {name}   [{src}]   {why}")

    print("\npatient keys -- the cross-root joins this file's own rules name, each checked against the key it "
          "must produce")
    kbad = 0
    for label, p, want in KEY_CASES:
        pp, _, unit, _, got, _ = classify_row(p)
        ok = got == want
        kbad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {label:<52} {got or '(none)':<28} "
              + ("" if ok else f"expected {want or '(none)'!r}   {pp}"))
    if kbad:
        print(f"  {kbad} patient key(s) are not what the rule promises: two roots that should meet cannot meet.")
    print(f"\nA corpus with no rule carries no independence claim and no patient key, so it can merge on content "
          f"alone; that is the gap this list measures, and it is not the same as 'nothing is duplicated there'.")
    bad = len(gaps) + len(wrong) + kbad
    if bad and a.allow_gaps:
        print(f"{bad} failure(s); --allow-gaps was given, so this exits 0")
        return 0
    return 1 if bad else 0


# ---------------------------------------------------------------------------------------------------- explain
def cmd_explain(a):
    res = json.load(open(a.groups, encoding="utf-8"))
    hits = [g for g in res["groups"] if any(a.path in m for m in g["members"])]
    if not hits:
        print(f"no alias group holds a member matching {a.path!r} (it is its own canonical id, or not in the ledger)")
        return 0
    for g in hits:
        print(f"{g['canonical_id']}  n={g['n']}  roots={g['roots']}  units={g['units']}  evidence={g['evidence']}")
        for m in g["members"]:
            print("   ", m)
        for e in g["edges"][:10]:
            print(f"    edge {e['rule']} {e['score']} {e['detail']}")
    return 0


# --------------------------------------------------------------------------------------------------- selftest
def _phantom(seed, h=384, w=256, bodies=7):
    """A radiograph-like phantom: a column of bright blocks on a soft-tissue gradient with grain. Two seeds give
    two DIFFERENT subjects imaged the SAME way, which is exactly the pair that must not merge."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w]
    img = 90 + 40 * np.exp(-((x - w / 2) ** 2) / (2 * (w / 2.6) ** 2)) + 12 * (y / h)
    y0 = 30 + rng.integers(0, 20)
    for k in range(bodies):
        cy = y0 + k * (h - 60) // bodies + rng.integers(-3, 4)
        cx = w // 2 + rng.integers(-6, 7)
        bh, bw = 18 + rng.integers(0, 6), 30 + rng.integers(0, 10)
        m = (np.abs(y - cy) < bh) & (np.abs(x - cx) < bw)
        img = np.where(m, img + 95 + rng.integers(0, 25), img)
        m2 = (np.abs(y - (cy + bh + 6)) < 4) & (np.abs(x - cx) < bw - 8)
        img = np.where(m2, img + 30, img)
    img = img + rng.normal(0, 4, img.shape)
    return np.clip(img, 0, 255).astype(np.uint8)


def cmd_selftest(a):
    """Build a corpus whose LAYOUT is the real one (the known-alias patterns are matched against these paths), then
    show which files merge, which do not, and by what measured evidence."""
    from PIL import Image
    out = a.out or tempfile.mkdtemp(prefix="data_alias_selftest_")
    os.makedirs(out, exist_ok=True)

    def P(*parts):
        p = os.path.join(out, *parts)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p):
            os.remove(p)      # a second run into the same --out must rebuild the corpus, not trip over the old
        return p              # hard link (os.link raises FileExistsError, and copyfile then raises SameFileError)

    A, B = _phantom(1), _phantom(2)
    h, w = A.shape
    # --- the film corpus: raw root, detector crop bank, second detector bank (paths shaped like the real ones)
    pRaw = P("spine-detector", "data", "raw", "buu_full", "BUU-LSPINEv1", "AP", "0123.jpg")
    Image.fromarray(A).save(pRaw, quality=95)
    pV3 = P("spine-detector", "data", "yolo_v3", "images", "train", "buu_00123_ap.png")
    Image.fromarray(A).save(pV3)                                  # re-encode of the same film: rung 3
    pV4 = P("spine-detector", "data", "yolo_v4z", "images", "train", "buu_00123_ap.png")
    try:
        os.link(pV3, pV4)                                         # two detector banks sharing one file: rung 0
        link_kind = "hard link"
    except OSError:
        shutil.copyfile(pV3, pV4)
        link_kind = "copy (os.link unavailable)"
    pCrop = P("FluoroCap", "panels", "buu_00123_ap_crop.png")
    Image.fromarray(A[int(0.18 * h):int(0.82 * h), int(0.18 * w):int(0.82 * w)]).save(pCrop)   # rung 5 only
    pRawB = P("spine-detector", "data", "raw", "buu_full", "BUU-LSPINEv1", "AP", "0456.jpg")
    Image.fromarray(B).save(pRawB, quality=95)                    # a DIFFERENT subject, imaged the same way
    # --- generic re-encodings of A, in a root the rules do not know (they merge on content alone)
    pCopy = P("misc", "copy_of_A.png")
    Image.fromarray(A).save(pCopy)
    shutil.copyfile(pV3, pCopy)                                   # byte identical: rung 1
    pTif = P("misc", "A_as_tiff.tif")
    Image.fromarray(A).save(pTif)                                 # same pixels, other container: rung 2
    pJpg = P("misc", "A_q85.jpg")
    Image.fromarray(A).save(pJpg, quality=85)                     # lossy re-encode: rung 3
    pHalf = P("misc", "A_half.png")
    Image.fromarray(A).resize((w // 2, h // 2), Image.BILINEAR).save(pHalf)                    # 0.5x: rung 3
    pMir = P("misc", "A_mirror.png")
    Image.fromarray(A[:, ::-1]).save(pMir)                        # mirrored export: rung 3 (mirror index)
    # --- NHANES II reaching two banks under two names (the defect of 2026-09-22)
    N = _phantom(5)
    pN1 = P("films_drr", "img", "nhanes_00160_c.npy")
    np.save(pN1, N)
    pN2 = P("nhanes_drr", "img", "NH_00160_c.npy")
    np.save(pN2, N.copy())
    # --- a device pair store beside the realxray copy of the same frame (the frame lives INSIDE the npz)
    F = _phantom(6)
    pPair = P("or_ready", "devices", "surgio_b51", "pairs", "case012_p004.npz")
    np.savez_compressed(pPair, real=F.astype(np.float32), hit=np.ones_like(F, bool))
    pReal = P("realxray", "carmlspine", "images", "train", "case012_ap_f004.png")
    Image.fromarray(F).save(pReal)
    # --- a file no reader here can open: it must be COUNTED, not silently treated as unique
    pDcm = P("deepfluoro_vendor", "unpacked", "17-1882", "IM000001.dcm")
    Path(pDcm).write_bytes(b"DICM not really a dicom")
    # --- files with NO IDENTITY TO ASSERT, in three corpora the analyses treat as independent. Every empty file
    # has one byte hash and every blank render of one canvas has one pixel hash, so the exact rungs used to call
    # these one picture, flag the group as spanning independent units and exit 1 under --fail-on-cross-unit.
    pE1 = P("spine-detector", "data", "raw", "csxa", "images", "datasets-PNG", "0999.png")
    pE2 = P("spine-detector", "data", "raw", "nhanes_full", "00999.tiff")
    for p in (pE1, pE2):
        open(p, "wb").close()
    pB1 = P("ctsp_drr", "img", "blank.png")
    pB2 = P("verse_drr", "img", "blank.npy")
    Image.fromarray(np.zeros((192, 192), np.uint8)).save(pB1)
    np.save(pB2, np.zeros((192, 192), np.uint8))
    # --- the same PMC figure harvested into two FluoroCap SETS: one rule used to give both the unit "FluoroCap",
    # so the duplicate was neither cross-root nor cross-unit and appeared in no table
    G = _phantom(9)
    pO1 = P("FluoroCap", "openi", "PMC7123456_fig2_a.jpg")
    pO2 = P("FluoroCap", "pmc18m", "PMC7123456_fig2_a.jpg")
    for p in (pO1, pO2):
        Image.fromarray(G).save(p, quality=97)
    # --- two unrelated films on two filesystems that share an inode number, with no device recorded
    pI1 = P("home", "spine-detector", "data", "raw", "csxa", "images", "datasets-PNG", "0001.png")
    pI2 = P("ceph", "realxray", "carmlspine", "images", "train", "case001_ap_f001.png")
    Image.fromarray(_phantom(21)).save(pI1)
    Image.fromarray(_phantom(22)).save(pI2)
    paths = [pRaw, pV3, pV4, pCrop, pRawB, pCopy, pTif, pJpg, pHalf, pMir, pN1, pN2, pPair, pReal, pDcm,
             pE1, pE2, pB1, pB2, pO1, pO2, pI1, pI2]
    inode_of = {posix(pI1): 1179700, posix(pI2): 1179700}

    vol_ok = True
    try:
        import nibabel as nib
        vA = _phantom(3, 64, 64, 5)[None].repeat(40, 0).astype(np.int16).transpose(1, 2, 0)
        vB = _phantom(4, 64, 64, 5)[None].repeat(40, 0).astype(np.int16).transpose(1, 2, 0)
        aff = np.diag([0.8, 0.8, 1.5, 1.0])
        pVol = P("data", "CTSpinoPelvic1K", "ct", "0001.nii.gz")
        nib.save(nib.Nifti1Image(vA, aff), pVol)
        pVol2 = P("nnUNet_raw", "Dataset813_LSTV", "imagesTr", "CTSP_0001_0000.nii.gz")
        nib.save(nib.Nifti1Image(vA.astype(np.float32), aff), pVol2)   # same scan, re-saved: different bytes
        pVolB = P("data", "CTSpinoPelvic1K", "ct", "0002.nii.gz")
        nib.save(nib.Nifti1Image(vB, aff), pVolB)
        paths += [pVol, pVol2, pVolB]
    except Exception as e:                                       # noqa: BLE001
        vol_ok = False
        print(f"(nibabel unavailable: {e}; the volume rung is not exercised)")

    led = os.path.join(out, "ledger.jsonl")
    with open(led, "w", encoding="utf-8") as fh:
        for p in paths:
            rec = dict(path=posix(p), corpus="selftest")
            if posix(p) in inode_of:
                rec["inode"] = inode_of[posix(p)]         # inode but NO device: the grid's two filesystems
            fh.write(json.dumps(rec) + "\n")
    print(f"synthetic ledger: {len(paths)} files under {out}   (second detector bank made by {link_kind})\n")

    # measured distances against the raw film, printed BEFORE any decision is taken
    gA = read_gray(pRaw)
    hA, pxA, shaA = phash64(gA), pixel_digest(gA), byte_sha256(pRaw)
    print(f"{'file':<34} {'bytes=':>7} {'pixels=':>8} {'pHash d':>8} {'d(mirror)':>10} {'ncc32':>7} {'ncc64':>7} {'ncc64 mir':>10}")
    measured = {}
    for p in paths:
        if p.endswith(".nii.gz"):
            continue
        g = read_gray(p)
        if g is None:
            print(f"{os.path.relpath(p, out).replace(chr(92), '/')[-34:]:<34} "
                  f"{'no reader here could open this file -- it is counted, not merged':>60}")
            continue
        d, dm = hamming(hA, phash64(g)), hamming(hA, phash64(np.ascontiguousarray(g[:, ::-1])))
        r32, r64, r64m = ncc(pRaw, p, 32), ncc(pRaw, p, 64), ncc(pRaw, p, 64, True)
        measured[os.path.basename(p)] = dict(d=d, dm=dm, ncc64=r64, ncc64_mirror=r64m)
        # a blank image has ZERO variance, so its NCC vector has no norm and every correlation with it is
        # undefined -- not 0.0, undefined. Printing a number there would be inventing one
        def f3(x):
            return "   n/a " if x is None else f"{x:>7.3f}"
        print(f"{os.path.relpath(p, out).replace(chr(92), '/')[-34:]:<34} {str(byte_sha256(p) == shaA):>7} "
              f"{str(pixel_digest(g) == pxA):>8} {d:>8} {dm:>10} {f3(r32)} {f3(r64)} {f3(r64m):>10}")
    print()

    ns = argparse.Namespace(ledger=led, out=out, pixels=True, workers=1, hash_bytes=True, phash_max=a.phash_max,
                            bands=8, ncc=a.ncc, volume_corr=0.99, no_mirror=False, no_name_merge=False,
                            merge_unverified=False, resolve_links=True, prev=None, only_root=[], skip_root=[],
                            only_kind=None, max_bucket=5000, max_members=200, fail_on_cross_unit=False)
    rc = cmd_canon(ns)
    if rc not in (0, 1):
        return rc
    canon = {}
    for rec in read_ledger(os.path.join(out, "canonical.jsonl")):
        canon[posix(rec["path"])] = rec["canonical_id"]
    rules = collections.defaultdict(set)
    with open(os.path.join(out, "alias_edges.csv"), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rules[row["rule"]].add((os.path.basename(row["a_path"]), os.path.basename(row["b_path"])))
    res = json.load(open(os.path.join(out, "alias_groups.json"), encoding="utf-8"))
    ka = {k["name"]: k for k in res["known_aliases"]}

    def same(x, y):
        return canon.get(posix(x)) == canon.get(posix(y))

    def rule_touched(rule, *names):
        return any(all(n in pair for n in names) for pair in rules.get(rule, ()))

    checks = [("byte-identical copy merges (rung 1)", same(pV3, pCopy), True),
              ("... and rung 1 is what did it", rule_touched("byte_sha256", "copy_of_A.png"), True),
              ("same pixels, other container merges (rung 2)", same(pV3, pTif), True),
              ("... and rung 2 is what did it", rule_touched("pixel_sha256", "A_as_tiff.tif"), True),
              ("JPEG q85 re-encode merges (rung 3)", same(pV3, pJpg), True),
              ("0.5x resize merges (rung 3)", same(pV3, pHalf), True),
              ("mirrored export merges (rung 3, mirror index)", same(pV3, pMir), True),
              ("... and the mirror rule is what did it", bool(rules.get("phash_mirror")), True),
              ("two banks sharing one file merge", same(pV3, pV4), True),
              ("raw film and its detector re-encode merge", same(pRaw, pV3), True),
              ("tight crop merges on NAME evidence only", same(pRaw, pCrop), True),
              ("... and it took the name rung to do it", rule_touched("name_key", "buu_00123_ap_crop.png"), True),
              ("a DIFFERENT subject, same imaging, does NOT merge", same(pRaw, pRawB), False),
              ("NHANES II under two names in two banks merges", same(pN1, pN2), True),
              ("a device pair store and the realxray copy of the frame merge (the frame is inside the .npz)",
               same(pPair, pReal), True),
              ("a file no reader could open is counted, not called unique",
               bool((res.get("unreadable") or {}).get("by_extension", {}).get(".dcm")), True),
              ("... and that group is flagged as spanning independent units",
               any(g["spans_independent_units"] and any("nhanes_drr" in m for m in g["members"]) for g in res["groups"]), True),
              ("known alias 'NHANES II twice in the level banks' is found",
               ka["NHANES II twice in the level banks"]["found"], True),
              ("known alias 'BUU-LSPINE: detector crops vs raw root' is found",
               ka["BUU-LSPINE: detector crops vs raw root"]["found"], True),
              ("a known alias whose roots are absent reports NOT FOUND, with the reason",
               (not ka["DeepFluoro: JHU h5 subset vs vendor DICOMs"]["found"]
                and "absent from the ledger" in str(ka["DeepFluoro: JHU h5 subset vs vendor DICOMs"]["why_not"])), True)]
    checks += [("two EMPTY files in two corpora are NOT called one picture", same(pE1, pE2), False),
               ("two BLANK renders in two banks are NOT called one picture", same(pB1, pB2), False),
               ("... and the blank files are counted, not silently dropped",
                (res["counts"]["degenerate_files"] >= 2 and res["counts"]["empty_files"] >= 2), True),
               ("an inode with no device does NOT merge two files on two filesystems", same(pI1, pI2), False),
               ("... and the skip is counted, so the rung is not silently off",
                res["stages"]["links"]["inode_without_device_skipped"] == 2, True),
               ("the same figure in two FluoroCap SETS merges", same(pO1, pO2), True),
               ("... and that group is reported as spanning independent units",
                any(g["spans_independent_units"] and any("/openi/" in m for m in g["members"])
                    for g in res["groups"]), True),
               ("the NCC refusal count in the JSON is the TOTAL, not the length of the truncated list",
                res["rejected_file_pairs"] == res["stages"]["phash"]["rejected"], True)]
    if vol_ok:
        checks += [("one scan re-saved under a Dataset813 path merges (rung 4)", same(pVol, pVol2), True),
                   ("... and the volume digest is what did it", rule_touched("volume_digest", "CTSP_0001_0000.nii.gz"), True),
                   ("a different scan of the same geometry does NOT merge", same(pVol, pVolB), False),
                   ("known alias 'CTSpinoPelvic1K CT: Dataset813 link vs real path' is found",
                    ka["CTSpinoPelvic1K CT: Dataset813 link vs real path"]["found"], True)]
    # --- the false-positive control, forced: at the default pHash threshold the different subject (d 20) is never
    # even proposed, so the NCC gate is not exercised. Run the same corpus again with the proposer left wide open
    # and watch the gate do its job; this is the only way to show it works rather than to assert that it would.
    loose = os.path.join(out, "loose_phash_24")
    ns2 = argparse.Namespace(**{**vars(ns), "out": loose, "phash_max": 24})
    print(f"\n--- second pass, pHash threshold opened to {ns2.phash_max} so the NCC gate is exercised ---")
    cmd_canon(ns2)
    res2 = json.load(open(os.path.join(loose, "alias_groups.json"), encoding="utf-8"))
    canon2 = {posix(r["path"]): r["canonical_id"] for r in read_ledger(os.path.join(loose, "canonical.jsonl"))}
    rej = res2["rejected_by_ncc"]
    def rejected_between(x, y):
        cx, cy = canon2.get(posix(x)), canon2.get(posix(y))
        return any({canon2.get(posix(r["a"])), canon2.get(posix(r["b"]))} == {cx, cy} for r in rej)

    checks += [("opening the proposer to pHash d <= 24 puts the different subject up for merging",
                rejected_between(pRaw, pRawB), True),
               ("... and the NCC gate refuses it, so it STILL does not merge",
                canon2.get(posix(pRaw)) == canon2.get(posix(pRawB)), False)]

    # --- --prev, on the run where it can do harm: the SAME ledger with the name rung switched off, so the
    # crop-and-parent group SPLITS. Both halves vote for the parent's old id; only one may have it.
    split = os.path.join(out, "prev_split_no_name_merge")
    ns3 = argparse.Namespace(**{**vars(ns), "out": split, "no_name_merge": True,
                               "prev": os.path.join(out, "canonical.jsonl")})
    print("\n--- third pass, --no-name-merge with --prev: the crop group splits and both halves claim one id ---")
    cmd_canon(ns3)
    rows3 = list(read_ledger(os.path.join(split, "canonical.jsonl")))
    cid3 = {posix(r["path"]): r["canonical_id"] for r in rows3}
    n_by_id = collections.Counter(r["canonical_id"] for r in rows3)
    # the invariant that makes canonical_id an identity at all: the id partitions the rows into exactly the
    # groups the run says it found. A collision shows up as group_size 1 on a row whose id two rows carry.
    partition_ok = all(n_by_id[r["canonical_id"]] == r["group_size"] for r in rows3)
    kept = [posix(p) for p in (pRaw, pCrop) if cid3[posix(p)] == canon.get(posix(p))]
    checks += [("--prev: the crop and its parent are two things again", cid3[posix(pRaw)] == cid3[posix(pCrop)], False),
               ("--prev: canonical_id still partitions the rows into the groups this run found", partition_ok, True),
               ("--prev: exactly one of the two halves keeps the old id", len(kept) == 1, True)]

    print("\nchecks")
    bad = 0
    for name, got, want in checks:
        ok = bool(got) == want
        bad += not ok
        print(f"  [{'ok' if ok else 'FAIL'}] {name}: got={bool(got)}, expected={want}")
    print("\nmeasured threshold behaviour (this run, these phantoms)")
    for k, v in measured.items():
        n1 = "undefined (blank)" if v["ncc64"] is None else f"{v['ncc64']:.3f}"
        n2 = "undefined" if v["ncc64_mirror"] is None else f"{v['ncc64_mirror']:.3f}"
        print(f"  {k:<30} pHash d {v['d']:>2} (mirror {v['dm']:>2})  ncc64 {n1} (mirrored {n2})")
    print(f"  threshold in force: pHash d <= {a.phash_max} AND ncc64 >= {a.ncc}")
    # NAMED EXPLICITLY, not filtered by exclusion: the corpus also holds copies of OTHER phantoms (the pair store
    # and its realxray twin), and an exclusion list quietly counted those as copies of this one -- a number that
    # reads fine and is computed over the wrong set
    copy_names = [os.path.basename(p) for p in (pRaw, pV3, pV4, pCopy, pTif, pJpg, pHalf)]
    copies = [measured[k] for k in dict.fromkeys(copy_names) if k in measured]
    other, crop = measured["0456.jpg"], measured["buu_00123_ap_crop.png"]
    print(f"  Read the gap, not the threshold: the {len(copies)} true copies sit at pHash d <= "
          f"{max(v['d'] for v in copies if v['d'] < 32)} with ncc64 >= {min(v['ncc64'] for v in copies):.3f}, the "
          f"different subject at d {other['d']} / ncc64 {other['ncc64']:.3f}, the crop at d {crop['d']} / ncc64 "
          f"{crop['ncc64']:.3f}. Nothing here sits near the threshold, so this test does NOT measure where the "
          "boundary should be -- it shows the ladder assigns each case to the rung it belongs on. On real corpora "
          "pairs will sit in that gap, which is why every pHash proposal is confirmed by NCC at 64x64, every "
          "refusal is counted, and the nearest of them are written to alias_groups.json to be read.")
    print("  The crop is the honest case: pixels and pHash BOTH miss it, and only the name rung joins it.")
    print("\nSELFTEST_OK" if not bad else f"\nSELFTEST_FAILED {bad}")
    if not a.keep and not a.out:
        shutil.rmtree(out, ignore_errors=True)
    else:
        print("kept", out)
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("canon", help="assign a canonical_id to every ledger row")
    c.add_argument("--ledger", default=None,
                   help="the ledger: one JSONL (.gz accepted), a glob, or a DIRECTORY of ledger_shard_*.jsonl "
                        "(the sharded form tools/data_ledger.py writes). Default: --out")
    c.add_argument("--out", required=True, help="directory for canonical.jsonl / alias_groups.json / ALIAS_SUMMARY.md")
    c.add_argument("--pixels", action="store_true", help="open the files and compute the digests the ledger lacks")
    c.add_argument("--hash-bytes", action="store_true", help="also compute the byte SHA-256 when the ledger has none")
    c.add_argument("--workers", type=int, default=8)
    c.add_argument("--phash-max", type=int, default=6, help="pHash Hamming distance a candidate may have (0-64)")
    c.add_argument("--bands", type=int, default=8, help="LSH bands; every pair below this distance is examined")
    c.add_argument("--ncc", type=float, default=0.97, help="NCC64 a pHash candidate must reach to merge")
    c.add_argument("--volume-corr", type=float, default=0.99, help="correlation for two volumes of equal geometry; 0 = off")
    c.add_argument("--no-mirror", action="store_true", help="do not index the horizontally flipped pHash")
    c.add_argument("--no-name-merge", action="store_true", help="content evidence only (drops crop-vs-parent links)")
    c.add_argument("--merge-unverified", action="store_true",
                   help="merge pHash candidates whose files cannot be opened here (off: they are reported, not merged)")
    c.add_argument("--resolve-links", action="store_true", default=True)
    c.add_argument("--prev", default=None, help="a previous canonical.jsonl, so ids survive a rebuild")
    c.add_argument("--only-root", action="append", default=[], help="regex on the root or path; repeatable")
    c.add_argument("--skip-root", action="append", default=[])
    c.add_argument("--only-kind", choices=["image", "volume", "other"], default=None)
    c.add_argument("--max-bucket", type=int, default=5000, help="LSH buckets bigger than this are dropped and counted")
    c.add_argument("--max-members", type=int, default=200, help="members listed per group in the JSON")
    c.add_argument("--fail-on-cross-unit", action="store_true", help="exit 1 if any group spans independent units")

    s = sub.add_parser("selftest", help="synthetic images: what merges, what does not, and at what distance")
    s.add_argument("--out", default=None, help="keep the synthetic corpus here instead of a temp directory")
    s.add_argument("--keep", action="store_true")
    s.add_argument("--phash-max", type=int, default=6)
    s.add_argument("--ncc", type=float, default=0.97)

    e = sub.add_parser("explain", help="print the alias group a path belongs to")
    e.add_argument("--groups", required=True)
    e.add_argument("--path", required=True)

    p = sub.add_parser("paths", help="run every corpus in corpus_manifold.SETS and data_manifest.ROOTS through "
                                     "the rules; exit 1 if any of them has no rule")
    p.add_argument("--file", default=None, help="classify the paths in this file instead of the derived corpus set")
    p.add_argument("--verbose", action="store_true", help="also print which table each corpus came from")
    p.add_argument("--allow-gaps", action="store_true",
                   help="report corpora with no rule but still exit 0 (for a caller that wants the table, not the "
                        "verdict); the gaps are printed either way")

    # slurm/data_accounting.sh runs every reader tool as `<tool> --out DIR` with no subcommand, and argparse then
    # exited 2 before reading a single row -- the alias stage of the chain could not run at all. The default verb
    # is the one the chain wants.
    import sys as _sys
    argv = _sys.argv[1:]
    if argv and argv[0].startswith("-") and argv[0] not in ("-h", "--help"):
        argv = ["canon"] + argv
    a = ap.parse_args(argv)
    if a.cmd == "canon" and not a.ledger:
        a.ledger = a.out                                   # the shards land beside the outputs
    return dict(canon=cmd_canon, selftest=cmd_selftest, explain=cmd_explain, paths=cmd_paths)[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
