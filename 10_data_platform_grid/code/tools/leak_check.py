#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/leak_check.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Is any test item -- or any ALIAS of it -- in any training set? One answer, per model and per bank, with a
non-zero exit when the answer is yes.

WHY THIS EXISTS. On 2026-09-22 the level banks were found to hold NHANES II twice: `~/films_drr` supplies it as
source `nhanes` with cases `NHANES_nhanes_cervical_00160`, and `~/nhanes_drr` supplies the SAME 543 films again as
source `nhanes_drr` with cases `NH_00160_c` / `NH_00160_l`. `tools/make_context_crops.py` draws its split per
SOURCE, so the two copies of one person were split independently and 48 of 54 validation patients had their twin
in training (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md). Every per-source disjointness check in the project
passed while that was true, because inside each source the split really was clean. The defect lives exactly in
the seam between sources, so the key this tool splits on must be CROSS-SOURCE: `nhanes_00160`,
`NHANES_nhanes_cervical_00160` and `NH_00160_c` are one patient and must collapse to one key, `nhanes:00160`.

THE TRAP THIS AVOIDS, stated as a rule. A path that matches NO keying rule is NOT treated as its own unique
patient. Treating an unrecognised name as unique is what makes a leak invisible: two names for one person look
like two people and every disjointness count comes out clean. Unkeyed items are collected, listed and reported,
and the run FAILS (exit 2) unless the collection explicitly declares `key_fallback` -- so silence about an item
is always a deliberate declaration in the table below, never a default. The same holds for aliased releases: the
DeepFluoro h5 (`~/deepfluoro/unpacked_full`) and the JHU Dataverse vendor DICOMs (`deepfluoro_vendor/unpacked`,
directories `03_cadaver_17-1882`) are the same six cadaveric pelves and the same 366 frames under two names; the
BUU Drive mirror is a byte-identical subset of BUU-LSPINE (docs/XRAY_DATASET_USAGE.md). Both are declared in
ALIAS_CORPORA and collapse by construction. What CANNOT be resolved from disk is declared in ALIAS_GAPS and
reported as a gap, never assumed away.

WHAT IS CHECKED (each is a count, with the offending items listed, capped at --cap and the total kept):
  (1) train/val/test disjointness inside every bank and dataset, on the key the BUILDER used -- corpus key
      qualified by the source name. This is the view that passed while NHANES was leaking; it is reported so the
      contrast with (2) is visible rather than argued.
  (2) the same, on the cross-source key after alias merging. Check (2) is the real one.
  (3) one source present twice in a bank under two names, detected STRUCTURALLY: for every pair of source names
      inside a collection, the share of the smaller source's patient keys that also appear under the other name.
      No name list is consulted, so a third double-inclusion is caught the same way NHANES would have been.
  (4) every evaluation set against every training set of the model scored on it (the lineage table / --lineage).
  (5) renders of one CT on both sides of a split: the pose-duplicate case, where `ctsp_0001_ap_p0` and
      `ctsp_0001_lat_p3` are two pictures of one patient.
  (6) styled corpora against the real frames of the device they were styled from, at two strengths: the device
      (`cios_fusion__elekta_xvi` carries Elekta style) and the pose donor (`s0224_00_17-1882-015_elekta_xvi_0`
      was rendered under the pose of DeepFluoro specimen 17-1882, so it is not independent of that specimen's
      real frames).

CONTENT EVIDENCE IS FOLDED IN WHEN THE INVENTORY LAYER SUPPLIES IT. `--ledger` (tools/data_ledger.py's
ledger.jsonl: sha256 / pix_sha256 / vol_sha256 / content_key / patient_key), `--canonical` and `--alias-groups`
(tools/data_alias.py's canonical.jsonl and alias_groups.json) each give groups of PATHS that are one thing;
those paths are translated through this run's inventory and the keys they touch are merged. Content evidence is
an ADDITION to the name rules, never a replacement: a film re-windowed, cropped into a bank and rendered has four
different byte hashes and one identity. And it is bounded -- a single token spanning more than --max-merge-span
patient keys (a blank frame hashes like every other blank frame) is reported rather than merged, because a false
merge manufactures leakage as convincingly as a missed one hides it.

`--hash` IS EVIDENCE, NOT IDENTITY, and that is a correction of this tool's own behaviour. It used to group the
files it hashed by sha256 and merge every patient key in a group. Byte identity arrives for reasons that have
nothing to do with a person: an empty placeholder PNG (the test fixture writes five of them and they share one
sha256), a solid-black frame, a 16-byte sentinel, the same calibration image copied into four corpora. Merging on
that fused distinct patients and then reported a train/val crossing between them that did not exist -- a
manufactured leak, which is the same failure as a missed one wearing the opposite sign. So now: a hash group whose
files all carry ONE patient key CORROBORATES the name rules; a hash group spanning TWO OR MORE patient keys is a
CONFLICT -- reported with both keys, the paths and the file size, counted in the report, and excluded from the
merge. A hash never creates a patient key and never joins two of them. Where two keys are a declared ALIAS_GAP the
conflict row says so, because that is exactly the evidence the gap asks for; acting on it means adding the pair to
--alias-file, deliberately, not having this tool infer it.

COLLECTIONS ARE DISCOVERED, NOT JUST DECLARED. `DEFAULT_COLLECTIONS` below is a hand list and a hand list cannot
notice what nobody added to it: it names twenty-five directories on a host that holds about a hundred, and the
`~/carm_cv{0..4}_fov96_ctx` cross-validation banks -- where a CV leak would live -- were not among them. So the
run now enumerates, before it scans: every root recorded in a `--ledger`, every root tools/data_ledger.py's
`discover_roots()` finds (its static table, its globbed families, tools/data_manifest.py ROOTS and
tools/corpus_manifold.py SETS), and every crop bank under BANK_GLOBS. Each directory is PROBED for a layout this
tool can scan (rung_*.npz, ann/, meta/ + images/, images/<split>/, <sub>/images/<split>/). The report states
"N collections discovered, M of them not in the hand list", and a discovered directory whose layout no scanner
handles is listed as UNSCANNABLE with the reason -- never silently absent, which is how the hand list hid things.
--no-discover restores the hand-list-only run; --fail-on-unscannable makes those directories an exit code.

Reads only. Nothing here is heavy enough to matter next to the I/O, but the banks live on the grid, so run it in
a job (never on the login node).

    python tools/leak_check.py check --out /rs/rs_grp_oschome/go2432/data/or_ready/leak
    python tools/leak_check.py check --out <dir> --ledger <dir>/ledger --canonical <dir>/canonical.jsonl \
                                     --lineage-graph <dir>/lineage.json --gen-dir <dir>/generated
                                     # --ledger takes the DIRECTORY of ledger_shard_*.jsonl, or a glob, or a file
    python tools/leak_check.py check --config my_collections.json --only-config --out /tmp/leak
    python tools/leak_check.py scan  --out /tmp/leak            # inventory only, no checks
    python tools/leak_check.py keys  --id NH_00160_c --id NHANES_nhanes_cervical_00160 --id nhanes_00160

EXIT CODES, AND THE DIFFERENCE A REVIEWER HAS TO BE ABLE TO SEE.
  0  the run was complete and found no leak.
  1  LEAKAGE FOUND. This is the only code that means "a check came back positive".
  2  items could not be keyed (the table is incomplete -- fix the table, do not silence it).
  3  COULD NOT RUN / incomplete coverage: nothing was read at all, a declared collection is absent from this host
     or present and empty, an input named on the command line is missing, empty or unparseable, a lineage ref
     names a collection this run never scanned, or the run raised. Nothing in this class is a statement about
     leakage; it is a statement that the question was not answered.
The worst outcome this tool could produce is a clean report computed over nothing, so a run that read zero items
exits 3 whatever flags it was given, --allow-missing cannot buy it a PASS, and an input file that was named and
could not be read cannot be passed over in silence. The lowest code wins when several apply, so a leak found on a
run that was also incomplete still exits 1 -- and `verdict.could_not_run` and the `LEAK_CHECK` line carry the
incompleteness separately, so the two are never confused for each other. An unhandled exception is caught at the
top and returned as 3: uncaught, Python would exit 1, which is this tool's code for "leakage found".

WHAT THIS TOOL STILL DOES NOT KNOW. Discovery finds directories; it does not find models. `DEFAULT_LINEAGE` is a
hand table of what each model trained on, and a model nobody entered there is checked by nothing -- pass
--lineage-graph from tools/data_lineage.py, which reads the checkpoints. Discovery also cannot key a corpus whose
filenames carry no subject id (see ALIAS_GAPS): CSXA is one image per patient by assumption, and Ljubljana, VinDr,
lateral236, SpineSAC and Geneva have nothing in the name to join on. A PASS is a statement about the census and
the discovery table printed in the report, and about nothing else.
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
H = os.path.expanduser("~")
D = "/rs/rs_grp_oschome/go2432/data"
IMG_EXT = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npy")

# --------------------------------------------------------------------------------------- the keying table
# Every rule: a regex over ONE identity string (the recorded patient id, else the recorded case, else the file
# stem, else the path relative to the collection root), and the (corpus, patient) it yields. `scope` restricts a
# rule to collections that declare that corpus, which is how bare numeric ids stay unambiguous. Unscoped rules
# are tried everywhere and are written to be distinctive (a DeepFluoro specimen is `17-1882`; a PMC article is
# `PMC10003423`). First match wins, in this order.
#
# Optional named groups beyond `pat`:
#   ct   -- the CT/subject a render was made from (renders and styled frames)
#   pose -- the specimen or case whose POSE the render was taken under (styled / calibrated renders)
#   dev  -- the device whose formation was applied
RULES = [
    # ---- NHANES II, the corpus the defect was found in: four spellings of one person
    dict(name="nhanes.patient_id", corpus="nhanes", pat=r"^nhanes_(?P<pat>\d{3,6})(?:_[cl])?$"),
    dict(name="nhanes.films_drr", corpus="nhanes", pat=r"^(?:NHANES_)?nhanes_(?:cervical|lumbar)_(?P<pat>\d{3,6})$"),
    dict(name="nhanes.nhanes_drr", corpus="nhanes", pat=r"^NH_(?P<pat>\d{3,6})_[cl]$"),
    dict(name="nhanes.zenodo_pickle", corpus="nhanes", pat=r"^[CL](?P<pat>\d{5})_(?:cervical|lumbar)_masks.*$"),
    # the raw release names a scan C00160.tiff / L00160.tiff (cervical / lumbar of one person; tools/fig_separation_hd.py
    # documents C00160 == nhanes_cervical_00160); the bare-number form is kept for the older copies
    dict(name="nhanes.tiff", corpus="nhanes", scope="nhanes", pat=r"^[CL]?(?P<pat>\d{4,6})(?:[_-].*)?$"),
    # tools/pseudolabel_real_films.py names a pseudo-labelled film `<source>_<raw stem>`: NHANESPS_C00156 is C00156.tiff
    dict(name="nhanes.pseudo", corpus="nhanes", pat=r"^NHANESPS_[CL](?P<pat>\d{3,6})$"),
    # ---- BUU-LSPINE: the release duplicates three files as "name (1).jpg"; the patient is the leading number
    dict(name="buu.case", corpus="buu", pat=r"^(?:BUU_FULL_)?buu_(?P<pat>\d{3,5})(?:-[MF]-\d+Y\d+)?(?:\s*\(\d\))?(?:_(?:AP|LA|LAT))?$"),
    dict(name="buu.raw_file", corpus="buu", scope="buu", pat=r"^(?P<pat>\d{3,5})-[MF]-\d+Y\d+(?:\s*\(\d\))?$"),
    # ---- CSXA (one image is treated as one patient; the release gives no patient identity -- see the report)
    dict(name="csxa.case", corpus="csxa", pat=r"^(?:CSXA_)?csxa_(?P<pat>[A-Za-z0-9\-.]+?)(?:_(?:AP|LAT|lat|ap))?$"),
    dict(name="csxa.raw", corpus="csxa", scope="csxa", pat=r"^(?P<pat>[A-Za-z0-9\-.]+?)(?:_(?:AP|LAT))?$"),
    # ---- Mendeley 5jdfdgp762, AASCE / BoostNet, Spinal-AI2024
    dict(name="mendeley.case", corpus="mendeley", pat=r"^(?:MEND_|mendeley_)(?P<pat>\d{2,6})(?:-[MF]-\d+Y\d+)?$"),
    # the Mendeley release also ships files named by whatever they were saved as (PARS_19-3-2021-PNG1_jumbo_jpeg,
    # Screenshot-2022-07-31-045959): one file is one case, which is all the release supports
    dict(name="mendeley.named_file", corpus="mendeley", pat=r"^(?:MEND_|mendeley_)(?P<pat>.+)$"),
    # the AASCE stems carry the view only sometimes (…-162_A_AP and …-20-Jul-2016-coronal1 are both real)
    dict(name="aasce.case", corpus="aasce", pat=r"^(?:AASCE_|aasce_)(?P<pat>.+?)(?:_(?:AP|LAT|ap|lat))?$"),
    dict(name="spinalai.case", corpus="spinalai", pat=r"^(?:SPINALAI_|spinalai_)(?P<pat>.+?)$"),
    # ---- VerSe (VerSe'19/'20 ids), CTSpinoPelvic1K, TotalSegmentator: CT corpora, rendered under many poses
    # ~/verse_drr holds thirteen GL cases under a DOUBLED prefix (gl003 and glgl003, identical .npy sizes). The
    # doubling is not assumed to be an alias here -- both spellings key to themselves and ALIAS_GAPS reports the pair
    # anchor_drr and the ws_* detector corpora spell a VerSe render verse_scan-verse533_ap (VerSeFusion's scan- prefix,
    # one render per view, no pose index)
    dict(name="verse.case", corpus="verse",
         pat=r"^(?:VERSE_|verse_)?(?:scan-)?(?:sub-)?(?P<pat>(?:gl)+\d{3,4}|verse\d{3,4})(?:_(?:lat|ap)(?:_p\d+)?)?$"),
    # ~/anchor_drr names one render per view with no pose index (ctsp_0001_ap); until 2026-09-23 that form fell
    # through to ctsp.case and keyed "0001_ap" as a patient
    dict(name="ctsp.render", corpus="ctsp", pat=r"^ctsp_(?P<pat>\d{4})(?:_v\d+)?_(?P<pose>(?:lat|ap)(?:_p\d+)?)$"),
    dict(name="ctsp.case", corpus="ctsp", pat=r"^(?:CTSP_|ctsp_)(?P<pat>[A-Za-z0-9_\-]+?)(?:_(?:lat|ap)_p\d+)?$"),
    dict(name="totalseg.render", corpus="totalseg",
         pat=r"^(?:TS_|totalseg_)?(?P<pat>s\d{4})(?:_v\d+)?(?:_(?P<pose>(?:lat|ap)(?:_p\d+)?))?$"),   # totalseg_s0001_ap too
    # ---- renders carrying a donor POSE: the render-only detector and the styled corpora
    #      s0224_00_17-1882-015.jpg          (anchor_none_v2_*: subject, pose index, pose specimen, pose frame)
    #      s0224_00_17-1882-015_elekta_xvi_0 (devcorpus/styled/<geometry>__<noise>)
    #      s0224_00_A102-0258_elekta_xvi_0   (a COBRA pose donor, centre+case A102, projection 0258)
    #      s0224_00_case114-LAT_surgio_b51_dr_0 (a C-ArmLSpine pose donor, case114, lateral)
    # Until 2026-09-23 only the DeepFluoro donor form was accepted, so every Elekta- and Surgio-geometry styled
    # frame -- two thirds of the device corpus the dc_* detectors trained on -- matched no rule and was unkeyed.
    #      s0224_00_case107-AP-arc003_surgio_b51_dr_0 (coverage_arms.py: an ARC pose drawn about that real anchor;
    #      `-arcNNN` is the draw index, not a person) -- unkeyed until 2026-09-25, which refused every coverage arm
    dict(name="render.pose_donor", corpus="totalseg",
         pat=r"^(?P<pat>s\d{3,5})_\d+_(?P<pose>1[78]-\d{4}|[A-G]\d{2,4}|case\d+)-(?:\d+|AP|LAT)(?:-arc\d+)?"
             r"(?:_(?P<dev>[a-z0-9_]+?)_\d+)?$"),
    dict(name="implant.render", corpus="implant", pat=r"^implant_(?P<pat>.+?)(?:_v\d+)?_(?P<pose>(?:lat|ap)_p\d+)$"),
    # ---- real fluoroscopy: DeepFluoro (h5 AND vendor DICOM), C-ArmLSpine, COBRA, Geneva, Ljubljana
    dict(name="deepfluoro.specimen", corpus="deepfluoro", pat=r"^(?:\d+_cadaver_)?(?P<pat>1[78]-\d{4})(?:[_-]\d+)?(?:_.*)?$"),
    # the export also writes case39_LAT2 (a second lateral), case118_OBL (the oblique) and, in carmlspine_multi,
    # case101_AP_k1_0 (the k-vertebra crop index): the person is the leading caseNNN in every form
    dict(name="carmlspine.frame", corpus="carmlspine",
         pat=r"^(?P<pat>case\d+)(?:_(?:AP|LAT|OBL)\d*(?:_\d+)?(?:_k(?:\d+|full)(?:_\d+)?)?)?$"),
    dict(name="cobra.frame", corpus="cobra", scope="cobra", pat=r"^(?P<pat>[A-G]\d{2,4})(?:_\d{1,5})?$"),
    # ONE resin phantom (D'Isidoro 2021) imaged at 19 positions: the position (`_p05`) is a view, not a patient. Keyed
    # per position before 2026-09-24 (EVAL_LEAKS), which would have passed a pose of the phantom as unseen by a model
    # trained on its other poses; the key is now the phantom, as tools/device_fit.SUBJECT_OF already had it.
    dict(name="geneva.frame", corpus="geneva", scope="geneva", pat=r"^(?P<pat>[A-Za-z]+)_p\d+(?:_.*)?$"),
    dict(name="ljubljana.frame", corpus="ljubljana", scope="ljubljana", pat=r"^(?P<pat>[A-Za-z]*\d+)(?:_.*)?$"),
    dict(name="spinesac.frame", corpus="spinesac", scope="spinesac", pat=r"^(?P<pat>[A-Za-z0-9\-]+?)(?:_\d+)?$"),
    # ---- literature panels: one article is one case (its panels are the same figure and often the same patient)
    dict(name="fluorocap.article", corpus="fluorocap", pat=r".*?(?P<pat>PMC\d{5,9}).*"),
    # a harvested panel id: one panel is keyed as one case because the panel -> article join lives in the FluoroCap
    # manifest, which this tool does not read (ALIAS_GAPS says so)
    dict(name="fluorocap.panel", corpus="fluorocap", pat=r"^(?:fluoro_)?(?P<pat>FLUO-\d{4,8})$"),
    # frames harvested from one video are one case: `fluoro_video_-wRtGXiWymY_00032` is frame 32 of that video
    # the level banks spell the same frame `video_panels:<video id>_<frame>__full` (a crop suffix after the __), and
    # the C-arm day-mix banks `video_panels_med:<video id>_<frame>__left` (the same videos' panels, another tier)
    dict(name="fluorocap.video_frame", corpus="fluorocap_video",
         pat=r"^(?:fluoro_)?video(?:_panels(?:_[a-z]+)?:|_)(?P<pat>[A-Za-z0-9_-]+?)_\d{4,6}$"),
    # ---- pseudo-labelled film corpora keyed by their own release id
    dict(name="vindr.study", corpus="vindr", scope="vindr", pat=r"^(?P<pat>[0-9a-f]{8,64})$"),
    # the same hex id carried with its corpus prefix (VINDRPS_<id> in the level banks, vindr_<id> in the hardware
    # detector corpus). One file id is keyed as one patient here, as the scoped rule above does: see ALIAS_GAPS
    dict(name="vindr.prefixed", corpus="vindr", pat=r"^(?:VINDRPS_|VINDR_|vindr_)(?P<pat>[0-9a-f]{8,64})$"),
    # LAT236PS_000001 is raw/lateral_236/000001.jpg (pseudolabel_real_films.py: `<source>_<raw stem>`), so it keys to
    # the same person the scoped rule below gives the raw file
    dict(name="lat236.pseudo", corpus="lat236", pat=r"^LAT236PS_(?P<pat>.+)$"),
    dict(name="lat236.film", corpus="lat236", scope="lat236", pat=r"^(?P<pat>.+?)$"),
]
for _r in RULES:
    _r["re"] = re.compile(_r["pat"])

# Source names as the banks record them -> the corpus they are. NOT READ BY ANY CHECK: check (1) qualifies the
# patient key with the raw source string and check (3) compares raw source names, both deliberately, so that a
# source name nobody listed here is still compared. Kept as documentation of what the source strings mean.
SOURCE_CORPUS = {"nhanes": "nhanes", "nhanes_drr": "nhanes", "nhanesps": "nhanes", "films_drr": "mixed",
                 "buu_full": "buu", "buu": "buu", "csxa": "csxa", "mendeley_drr": "mendeley", "mendeley": "mendeley",
                 "aasce_drr": "aasce", "spinalai_drr": "spinalai", "verse_drr": "verse", "ctsp_drr": "ctsp",
                 "ts_drr": "totalseg", "physics_drr": "ctsp", "carm": "carmlspine", "vindr_pseudo": "vindr"}

# Releases that are the same data under two names. Declared, not inferred: the keying rules above already collapse
# them, and this table says WHY, so a reader can check the claim instead of trusting the regex. It is copied into
# the report and drives NO merge -- the collapse is the regexes' doing, and only for copies that are actually
# scanned. `deepfluoro_h5` and `deepfluoro_vendor` are NOT in DEFAULT_COLLECTIONS, so on a default run neither copy
# is read and this row asserts something the run did not test.
ALIAS_CORPORA = [
    dict(corpus="deepfluoro", names=["deepfluoro_h5", "deepfluoro_vendor", "realxray/deepfluoro"],
         why="the JHU Dataverse vendor DICOMs (doi:10.7281/T1/IFSXNV, directories 03_cadaver_17-1882 ...) are the "
             "vendor-header copy of the same 366 frames of the same six cadaveric pelves as ipcai_2020_full_res_data.h5"),
    dict(corpus="buu", names=["buu_full", "buu_drive_mirror"],
         why="the BUU Drive mirror is a byte-identical subset of BUU-LSPINE (docs/XRAY_DATASET_USAGE.md); its 5,495 "
             "films add no patient"),
    dict(corpus="nhanes", names=["nhanes (films_drr)", "nhanes_drr", "nhanes_full"],
         why="one Zenodo release of 543 annotated NHANES II films, entered twice under two directory names; this is "
             "the defect of docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md"),
]

# Overlaps that are believed real and that CANNOT be resolved from the files on disk. Never assumed away: reported,
# and escalated to a failure when both spellings land on opposite sides of one split.
ALIAS_GAPS = [
    dict(a=r"^ctsp:\d{4}$", b=r"^ctsp:(?!\d{4}$).+$",
         why="physics_drr names a CTSpinoPelvic1K case by its release id (ctsp_0001) while ctsp_drr names the same CT "
             "by its original CTSpine1K/COLONOG name (CTSP_COLONOG_1). No mapping table is on disk here, so one CT can "
             "appear as two patients.",
         fix="join through the CTSpinoPelvic1K release case table and add the resolved pairs with --alias-file"),
    dict(a=r"^verse:gl\d+$", b=r"^verse:glgl\d+$",
         why="~/verse_drr holds thirteen VerSe GL cases twice: gl003 ... gl146 and glgl003 ... glgl146, the same "
             "thirteen numbers, written eight days apart, with identical .npy sizes (gl003 and glgl003 are both "
             "109,696 bytes; gl016 and glgl016 both 92,288). A doubled prefix is the obvious reading and it is not "
             "assumed here: the two spellings are two split groups in every bank built from that directory.",
         fix="confirm with the content layer (pix_sha256 of the two .npy files); if equal, add the thirteen pairs "
             "with --alias-file and rebuild any bank that drew a split over both"),
    dict(a=r"^fluorocap:FLUO-", b=r"^fluorocap:PMC",
         why="FluoroCap panels reach the detector corpus as FLUO-000001 and reach the panel roots as PMC ids. One "
             "panel is keyed as one case, so several panels of one article -- often one patient -- are several "
             "patients to this tool.",
         fix="join through the FluoroCap manifest (panel id -> article) and supply the groups with --alias-file"),
    dict(a=r"^vindr:", b=r"^vindr:",
         why="VinDr-SpineXR files are named by a hex id, and the patient is the study (docs/DATA_ACCOUNTING.md s4: "
             "StudyInstanceUID -> patient). Nothing joining the file id to its study is read here, so one file is keyed "
             "as one patient; if a study's AP and lateral carry two ids, one person is two keys.",
         fix="join the file id to study_id through the release's annotation table and supply the pairs with --alias-file"),
    dict(a=r"^csxa:", b=r"^csxa:",
         why="the CSXA release gives no patient identity, so one image is keyed as one patient. A patient who "
             "contributed several films would be split across train and test and this tool could not see it.",
         fix="none available from the release; state it as a limitation wherever CSXA is scored"),
]

# --------------------------------------------------------------------------------------- the collections
# kind: bank | drr | realxray | yolo | flat | styled | ledger
# corpus: declared when a whole root is one corpus (scopes the rules above and flags foreign names)
# key_fallback: "stem" -- the ONLY way an unrecognised name is allowed to pass, declared per collection
DEFAULT_COLLECTIONS = {
    # level banks: cases + splits live in the npz's small string members
    "allspine_v7_fov96_ctx": dict(kind="bank", path=f"{H}/allspine_v7_fov96_ctx"),
    "allspine_v6_fov96_ctx": dict(kind="bank", path=f"{H}/allspine_v6_fov96_ctx"),
    "allspine_v7nofluoro_fov96_ctx": dict(kind="bank", path=f"{H}/allspine_v7nofluoro_fov96_ctx"),
    "films_all2_fov96_ctx": dict(kind="bank", path=f"{H}/films_all2_fov96_ctx"),
    "films_ann_fov96_ctx": dict(kind="bank", path=f"{H}/films_ann_fov96_ctx"),
    "carm_fov96_ctx": dict(kind="bank", path=f"{H}/carm_fov96_ctx"),
    "carm_mix_fov96_ctx": dict(kind="bank", path=f"{H}/carm_mix_fov96_ctx"),
    "fluorocap_fov96_ctx": dict(kind="bank", path=f"{H}/fluorocap_fov96_ctx"),
    # render directories that feed the banks
    "films_drr": dict(kind="drr", path=f"{H}/films_drr"),
    "nhanes_drr": dict(kind="drr", path=f"{H}/nhanes_drr"),
    "aasce_drr": dict(kind="drr", path=f"{H}/aasce_drr"),
    "mendeley_drr": dict(kind="drr", path=f"{H}/mendeley_drr"),
    "ctsp_drr": dict(kind="drr", path=f"{H}/ctsp_drr"),
    "verse_drr": dict(kind="drr", path=f"{H}/verse_drr"),
    "ts_drr": dict(kind="drr", path=f"{H}/ts_drr"),
    "physics_drr": dict(kind="drr", path=f"{H}/physics_drr"),
    # real frames, one directory per device
    "rx_deepfluoro": dict(kind="realxray", path=f"{D}/realxray/deepfluoro", corpus="deepfluoro", device="cios_fusion"),
    "rx_carmlspine": dict(kind="realxray", path=f"{D}/realxray/carmlspine", corpus="carmlspine", device="surgio_b51_dr"),
    "rx_cobra_elekta": dict(kind="realxray", path=f"{D}/realxray/cobra_elekta", corpus="cobra", device="elekta_xvi"),
    "rx_geneva_hip": dict(kind="realxray", path=f"{D}/realxray/geneva_hip", corpus="geneva", device="bv_pulsera"),
    # detector corpora
    "yolo_v3": dict(kind="yolo", path=f"{H}/spine-detector/data/yolo_v3"),
    "yolo_v4z": dict(kind="yolo", path=f"{H}/spine-detector/data/yolo_v4z"),
    "yolo_v6f": dict(kind="yolo", path=f"{H}/spine-detector/data/yolo_v6f"),
    # renders under real poses, and the styled corpora built from them
    "anchor_none_v2_17-1882": dict(kind="yolo", path=f"{H}/model_night/anchor_none_v2_17-1882", device="cios_fusion"),
    "styled": dict(kind="styled", path=f"{D}/devcorpus/styled"),
}

# Which real corpus IS each device. Check (6) needs this and nothing else.
DEVICE_REAL = {"cios_fusion": "rx_deepfluoro", "elekta_xvi": "rx_cobra_elekta",
               "surgio_b51_dr": "rx_carmlspine", "bv_pulsera": "rx_geneva_hip"}

# --------------------------------------------------------------------------------------- the lineage
# model -> what it trained on, what it is scored on. `evidence` names the file the claim comes from; an entry
# without evidence is an assertion and is printed as one. "<collection>#<split>[,<split>]"; no # means every split.
DEFAULT_LINEAGE = {
    "level_encoder_allspine_v7": dict(
        train=["allspine_v7_fov96_ctx#train"], eval=["allspine_v7_fov96_ctx#val"],
        evidence="docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md (bank meta.json val_cases)"),
    "level_head_films_all2": dict(
        train=["films_all2_fov96_ctx#train"], eval=["films_all2_fov96_ctx#val"],
        evidence="docs/MANIFEST_DATA_MODELS_RESULTS.md 1.5"),
    "carm_finetune": dict(
        train=["carm_fov96_ctx#train", "carm_mix_fov96_ctx#train"], eval=["rx_carmlspine#test"],
        evidence="docs/carmlspine_ft_mix_test_2026-09-21.json; tools/or_audit_splits.audit_carm_banks"),
    "anchor_none_v2_17-1882": dict(
        train=["anchor_none_v2_17-1882#train,val"], eval=["rx_deepfluoro#test"],
        evidence="tools/or_audit_splits.audit_render_detector (renders under donor poses; held specimen 17-1882)"),
}


# --------------------------------------------------------------------------------------- keying
def identity_strings(rec):
    """The strings a rule may match, best identity first: what the file SAYS it is, then what it is called."""
    out = []
    for k in ("patient_id", "case", "stem", "rel"):
        v = rec.get(k)
        if v:
            out.append(str(v))
    return out


def key_for(ident, corpus_hint=None):
    """(dict(corpus, patient, pose, ct, device, rule), None) or (None, reason). Scoped rules first.

    A DOUBLE underscore marks a derived view, not a patient: the detector corpora hold `buu_0003-F-013Y0__zoom0`,
    `nhanes_cervical_00161__zoom1`, `fluoro_video_..._00032__r3` beside their parents. Keying those as new
    patients would put a zoom of a training film in validation and call it held out, so the suffix is cut and the
    parent name is keyed. Single underscores are never touched -- `NH_00160_c` is a whole name."""
    order = [r for r in RULES if r.get("scope") and r["scope"] == corpus_hint] + [r for r in RULES if not r.get("scope")]
    for attempt, s in enumerate((ident, ident.split("__")[0] if "__" in ident else None)):
        if s is None:
            continue
        for r in order:
            m = r["re"].match(s)
            if not m:
                continue
            g = m.groupdict()
            return dict(corpus=r["corpus"], patient=g["pat"], pose=g.get("pose"), device=g.get("dev"),
                        rule=r["name"] + (" (derived view)" if attempt else ""),
                        variant=ident[len(s):].lstrip("_") or None), None
    return None, f"no rule matches {ident!r}" + (f" (corpus hint {corpus_hint})" if corpus_hint else "")


def key_item(rec, corpus_hint=None, key_fallback=None):
    """Key one inventory record. Returns the record enriched, with `unkeyed` set when nothing matched."""
    for ident in identity_strings(rec):
        k, _ = key_for(ident, corpus_hint)
        if k:
            rec.update(corpus=k["corpus"], patient=k["patient"], rule=k["rule"], keyed_from=ident)
            rec["key"] = f"{k['corpus']}:{k['patient']}"
            if k.get("pose"):
                rec["pose"] = k["pose"]
                p, _ = key_for(k["pose"], None)
                rec["pose_key"] = f"{p['corpus']}:{p['patient']}" if p else f"pose:{k['pose']}"
            if k.get("device") and not rec.get("device"):
                rec["device"] = k["device"]
            # a name that resolves to a corpus the collection does not declare is worth seeing: it is how a test
            # device's frames turn up inside a training corpus
            if corpus_hint and k["corpus"] != corpus_hint:
                rec["corpus_conflict"] = f"{k['corpus']} inside {corpus_hint}"
            return rec
    if key_fallback == "stem":
        stem = rec.get("stem") or rec.get("case") or rec.get("rel") or "?"
        rec.update(corpus=corpus_hint or rec.get("collection", "?"), patient=stem, rule="declared key_fallback=stem")
        rec["key"] = f"{rec['corpus']}:{stem}"
        return rec
    rec["unkeyed"] = key_for(identity_strings(rec)[0] if identity_strings(rec) else "", corpus_hint)[1] or "no identity string"
    rec["key"] = None
    return rec


class Union:
    """Alias merging. Union-find over keys; every merge records WHY, so the report can name it."""

    def __init__(self):
        self.p = {}
        self.why = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b, why):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[rb] = ra
        self.why[(a, b)] = why
        return True


# --------------------------------------------------------------------------------------- scanners
def _items_from_npz(path, keys=("case", "split", "source")):
    """Only the small string members of a bank are touched; X is never decompressed."""
    import numpy as np
    # closed explicitly: every rung of every bank is opened now, not one file per bank
    with np.load(path, allow_pickle=False) as z:
        return {k: [str(v) for v in z[k]] for k in keys if k in z.files}


def scan_bank(name, cfg):
    """A context-crop bank: rung_*.npz carry (case, split, source) per crop; one record per distinct case.

    EVERY rung is read, not one of them. A rung is a context length and a case only appears in a rung it can
    fill, so the rungs hold DIFFERENT case sets -- `films_all2_fov96_ctx` has eight (rung_0 ... rung_full).
    Reading one file and calling it the bank leaves every case that lives only in another rung uninventoried,
    and a train/val crossing among those cases is then reported as clean with nothing saying otherwise. Only
    the small string members are touched, so this costs one zip-directory read per rung, never the array data."""
    root = Path(cfg["path"])
    npzs = sorted(root.glob("rung_*.npz"))
    out, seen, first = [], Counter(), {}
    for npz in npzs:
        a = _items_from_npz(npz)
        cases = a.get("case", [])
        # an older bank may carry no `split` or no `source` member; a missing member must not silently truncate the
        # scan to nothing (zip stops at the shortest), it must show as an empty field
        splits = a.get("split") or [""] * len(cases)
        sources = a.get("source") or [""] * len(cases)
        for case, split, src in zip(cases, splits, sources):
            k = (case, split, src)
            seen[k] += 1
            if k in first:
                first[k]["rungs"].add(npz.name)
                continue
            # a bank member has no file of its own: it is addressed as <npz>#<case>, the same way the inventory
            # layer enumerates crop-bank members from the bank's string arrays
            rec = dict(collection=name, kind="bank", item=case, case=case, split=split, source=src,
                       path=f"{npz}#{case}", file=str(npz), rungs={npz.name})
            first[k] = rec
            out.append(rec)
    if out:
        for rec in out:
            rec["n_crops"] = seen[(rec["case"], rec["split"], rec["source"])]
            rec["rungs"] = sorted(rec["rungs"])
        return out
    meta = root / "meta.json"
    if meta.exists():                      # a bank whose npz is gone still names its val cases
        M = json.load(open(meta))
        for c in M.get("val_cases", []):
            out.append(dict(collection=name, kind="bank", item=c, case=c, split="val", source="", path=str(meta),
                            note="from meta.json val_cases; the training side of this bank is not on disk"))
    return out


def scan_drr(name, cfg):
    """A render directory: ann/<case>.json carries case, and sometimes source / patient_id / split."""
    root = Path(cfg["path"])
    out = []
    for p in sorted((root / "ann").glob("*.json")):
        try:
            hdr = json.load(open(p))
        except Exception:                                    # noqa: BLE001
            hdr = {}
        out.append(dict(collection=name, kind="drr", item=p.stem, case=hdr.get("case") or p.stem,
                        patient_id=hdr.get("patient_id") or "", source=str(hdr.get("source") or root.name),
                        split=hdr.get("split") or "", stem=p.stem, path=str(p),
                        source_file=hdr.get("source_file") or ""))
    return out


def scan_realxray(name, cfg):
    """A real-frame dataset: splits.json is case-level truth, meta/<stem>.json is frame-level truth."""
    root = Path(cfg["path"])
    out = []
    case_split = {}
    sp = root / "splits.json"
    if sp.exists():
        S = json.load(open(sp))
        for s in ("train", "val", "test"):
            for c in S.get(s, []) or []:
                case_split[c] = s
    metas = sorted((root / "meta").glob("*.json"))
    if metas:
        for p in metas:
            try:
                m = json.load(open(p))
            except Exception:                                # noqa: BLE001
                m = {}
            stem = m.get("stem") or p.stem
            case = m.get("case") or stem.split("_")[0]
            out.append(dict(collection=name, kind="realxray", item=stem, case=case, stem=stem,
                            split=m.get("split") or case_split.get(case, ""), source=name,
                            device=cfg.get("device"), path=str(root / "images" / (m.get("split") or "") / f"{stem}.png")))
    else:
        for s in ("train", "val", "test"):
            for p in sorted((root / "images" / s).glob("*")):
                if p.suffix.lower() in IMG_EXT:
                    out.append(dict(collection=name, kind="realxray", item=p.stem, stem=p.stem, split=s,
                                    source=name, device=cfg.get("device"), path=str(p)))
    for c, s in case_split.items():                          # cases declared in splits.json with no frame on disk
        if not any(r.get("case") == c for r in out):
            out.append(dict(collection=name, kind="realxray", item=c, case=c, split=s, source=name,
                            device=cfg.get("device"), path=str(sp), note="declared in splits.json, no frame found"))
    return out


def scan_yolo(name, cfg):
    """images/<split>/<stem>.<ext>: the detector corpora and the render-only detector share this layout."""
    root = Path(cfg["path"])
    out = []
    for s in ("train", "val", "test", "real_test"):
        for p in sorted((root / "images" / s).glob("*")) + (sorted((root / s).glob("*")) if s == "real_test" else []):
            if p.suffix.lower() in IMG_EXT:
                out.append(dict(collection=name, kind="yolo", item=p.stem, stem=p.stem, split=s, source=name,
                                device=cfg.get("device"), path=str(p)))
    return out


def scan_styled(name, cfg):
    """devcorpus/styled/<geometry>__<noise>/images/<split>/<stem>.jpg -- one collection per styled corpus."""
    root = Path(cfg["path"])
    out = []
    for d in sorted(p for p in root.glob("*") if p.is_dir()):
        geom, _, noise = d.name.partition("__")
        for s in ("train", "val", "test"):
            for p in sorted((d / "images" / s).glob("*")):
                if p.suffix.lower() in IMG_EXT:
                    out.append(dict(collection=f"{name}/{d.name}", kind="styled", item=p.stem, stem=p.stem, split=s,
                                    source=d.name, device=noise or geom, geometry=geom, style=noise, path=str(p)))
    return out


def scan_flat(name, cfg):
    """A glob per split, or one glob with a declared split: `path` may hold {split}."""
    out = []
    splits = cfg.get("splits") or {cfg.get("split", ""): cfg["path"]}
    for s, pat in splits.items():
        for p in sorted(glob.glob(pat, recursive=True)):
            q = Path(p)
            if q.is_file() and (q.suffix.lower() in IMG_EXT or cfg.get("any_ext")):
                out.append(dict(collection=name, kind="flat", item=q.stem, stem=q.stem, split=s,
                                source=cfg.get("source", name), device=cfg.get("device"), path=p))
    return out


SCANNERS = dict(bank=scan_bank, drr=scan_drr, realxray=scan_realxray, yolo=scan_yolo, styled=scan_styled, flat=scan_flat)


# --------------------------------------------------------------------------------------- discovery
# A hand list cannot notice what nobody added to it, so the run enumerates as well as reads the table. Three
# sources, each named in the report so a reader knows how a collection got here:
#   ledger        every `root` a --ledger jsonl RECORDED, with its directory reconstructed from path minus rel.
#                 This is the strongest source: those directories were walked file by file by another tool.
#   data_ledger   tools/data_ledger.py discover_roots() -- its static table, its globbed families, and anything
#                 in tools/data_manifest.py ROOTS / tools/corpus_manifold.py SETS that no root already claims.
#   bank glob     crop banks by layout, so discovery still finds them when data_ledger will not import (it needs
#                 numpy at module scope; this tool does not, outside an actual bank read).
BANK_GLOBS = (f"{H}/*_ctx", f"{H}/*_fov*_ctx", f"{H}/*_bank", f"{D}/*_ctx", f"{D}/banks/*", f"{D}/or_ready/*_ctx")
SPLIT_DIRS = ("train", "val", "valid", "test", "real_test")


def _entries(path, cap=400):
    """(dirs, files) of one directory, capped. A probe must never walk a corpus of two million crops to decide
    what kind it is, and on CephFS an uncapped scandir of a detector corpus is minutes. (None, None) if the
    directory cannot be read -- which is itself an answer, and is reported as unscannable rather than skipped."""
    dirs, files = [], []
    try:
        with os.scandir(path) as it:
            for i, e in enumerate(it):
                if i >= cap:
                    break
                try:
                    (dirs if e.is_dir() else files).append(e.name)
                except OSError:
                    files.append(e.name)
    except OSError:
        return None, None
    return dirs, files


def probe_kind(path):
    """Which scanner can read this directory, decided by LAYOUT and never by name -> (kind, why) | (None, why not).

    Name-based classification is what this whole tool exists not to do: `~/carm_cvmix3_fov96_ctx` and
    `~/allspine_v7_fov96_ctx` are both banks and share no name pattern with `~/films_drr`, which is a render
    directory. The layouts are the contract the scanners above already depend on, so they are what is probed.

    The named tests are STATS, not a listing, and they come first. _entries() is capped so that a probe cannot
    walk a corpus of two million crops, and a capped listing of a directory holding ten thousand loose files
    could miss the `images/` beside them and file a detector corpus as unscannable -- a wrong answer produced by
    an optimisation, which is this project's recurring shape."""
    j = os.path.join
    if not os.path.isdir(path):
        return None, "not a directory on this host"
    if glob.glob(j(path, "rung_*.npz")):
        return "bank", "rung_*.npz"
    if os.path.isfile(j(path, "meta.json")):
        try:
            M = json.load(open(j(path, "meta.json"), encoding="utf-8"))
        except Exception:                                    # noqa: BLE001
            M = {}
        if isinstance(M, dict) and M.get("val_cases"):
            return "bank", "meta.json carrying val_cases (the rungs are not on disk)"
    if os.path.isdir(j(path, "ann")):
        return "drr", "ann/*.json"
    if os.path.isdir(j(path, "images")):
        if os.path.isdir(j(path, "meta")) or os.path.isfile(j(path, "splits.json")):
            return "realxray", "images/ beside meta/ or splits.json"
        hit = [s for s in SPLIT_DIRS if os.path.isdir(j(path, "images", s))]
        if hit:
            return "yolo", f"images/<split>/ ({', '.join(hit)})"
    dirs, _files = _entries(path)
    if dirs is None:
        return None, "the directory could not be read (permissions, or it moved during the run)"
    for d in dirs[:50]:                                      # a styled parent: one level down is <child>/images/
        if os.path.isdir(j(path, d, "images")):
            return "styled", f"<child>/images/ (e.g. {d}/)"
    return None, ("no layout any scanner here handles (looked for rung_*.npz, meta.json val_cases, ann/, "
                  "images/+meta/, images/<split>/, <child>/images/)")


def _root_dir_of(path, rel):
    """The root directory of a ledger record: its path with its root-relative part removed. A member record
    addresses itself as `<file.npz>#case`, so the container is taken first."""
    p = str(path).replace("\\", "/").split("#")[0]
    r = str(rel or "").replace("\\", "/").strip("/")
    if r and p.endswith("/" + r):
        return os.path.normpath(p[: -(len(r) + 1)])
    return os.path.normpath(os.path.dirname(p))


def roots_from_ledger(paths):
    """Every root a ledger recorded. Streamed line by line, not read_records(): a real ledger is millions of
    rows and this pass needs four fields of each. A root that the ledger holds and this host does not is kept,
    with path=None, so it is reported as unscannable instead of vanishing."""
    out = {}
    for p in paths or []:
        if not os.path.isfile(p):
            continue
        base = os.path.basename(p)
        try:
            with open(p, encoding="utf-8") as fh:
                for ln in fh:
                    ln = ln.strip()
                    if not ln or ln[0] != "{":
                        continue
                    try:
                        r = json.loads(ln)
                    except json.JSONDecodeError:
                        continue
                    root, path = r.get("root"), (r.get("path") or r.get("file"))
                    if not root or not path:
                        continue
                    e = out.setdefault(str(root), dict(name=str(root), path=None, n_records=0, stages=set(),
                                                       evidence=f"ledger {base}"))
                    e["n_records"] += 1
                    if r.get("stage"):
                        e["stages"].add(str(r["stage"]))
                    if e["path"] is None:
                        e["path"] = _root_dir_of(path, r.get("rel"))
        except OSError:
            continue
    for e in out.values():
        e["stages"] = sorted(e["stages"])
    return list(out.values())


def roots_from_data_ledger():
    """tools/data_ledger.py's own root table. Its absence is returned as a note, never as silence: without it
    discovery is down to the ledger files and the bank globs, and the report has to say so."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import data_ledger                                   # type: ignore  # noqa: PLC0415
        specs = data_ledger.discover_roots(verbose=False)
    except Exception as e:                                   # noqa: BLE001
        return [], f"tools/data_ledger.py root table not consulted ({e.__class__.__name__}: {e})"
    out = [dict(name=str(s.get("name")), path=s.get("path"), n_records=None, stages=[s.get("stage")],
                evidence="data_ledger.discover_roots") for s in specs if s.get("path")]
    return out, f"tools/data_ledger.py: {len(out)} roots in its table"


def roots_from_bank_globs():
    out = []
    for pat in BANK_GLOBS:
        for p in sorted(glob.glob(pat)):
            if os.path.isdir(p):
                out.append(dict(name=os.path.basename(p.rstrip("/\\")), path=os.path.normpath(p), n_records=None,
                                stages=["crop"], evidence="bank glob"))
    return out


def discover_collections(hand, ledger_paths=(), verbose=True):
    """Enumerate the collections a hand list does not name, and report the difference.

    RULES, because this decides what a PASS covers.
      * The hand list WINS on a path it already declares: its entry carries `corpus`, `device` and
        `key_fallback`, which a probe cannot infer and which the keying rules need.
      * A discovered directory whose layout no scanner handles is UNSCANNABLE. It is listed with its reason and
        counted; it is never dropped, because a collection that is absent from the report is exactly how the
        hand list hid `~/carm_cv*_fov96_ctx`.
      * Discovery adds directories, never lineage: a model nobody declared is still checked by nothing.
    """
    hand_paths = {}
    for n, c in (hand or {}).items():
        if c.get("path"):
            hand_paths[os.path.normpath(os.path.expanduser(str(c["path"])))] = n
    cands, notes = [], []
    cands += roots_from_ledger(ledger_paths)
    dl, note = roots_from_data_ledger()
    cands += dl
    notes.append(note)
    cands += roots_from_bank_globs()

    merged = {}                                              # one row per normalised path, evidences accumulated
    off_host = []
    for c in cands:
        if not c.get("path"):
            off_host.append(dict(name=c["name"], path=None, evidence=c["evidence"], n_records=c.get("n_records"),
                                 why="recorded in the ledger with no reconstructable directory"))
            continue
        k = os.path.normpath(os.path.expanduser(str(c["path"])))
        m = merged.setdefault(k, dict(name=c["name"], path=k, evidence=[], n_records=c.get("n_records"),
                                      stages=list(c.get("stages") or [])))
        if c["evidence"] not in m["evidence"]:
            m["evidence"].append(c["evidence"])
        if m["n_records"] is None:
            m["n_records"] = c.get("n_records")

    rows, unscannable, add = [], list(off_host), {}
    used = set(hand or ())
    claimed = set(hand_paths)                                # paths already scanned by somebody

    def inside(child, parent):
        c, p = os.path.normcase(child), os.path.normcase(parent)
        return c != p and c.startswith(p.rstrip("\\/") + os.sep)

    def take(name, path, kind, why, evidence):
        n = re.sub(r"[^A-Za-z0-9_.-]+", "_", name) or "discovered"
        if n in used:
            n = f"{n}__{os.path.basename(os.path.dirname(path)) or len(used)}"
        while n in used:
            n += "_"
        used.add(n)
        claimed.add(path)
        add[n] = dict(kind=kind, path=path, discovered=True, discovered_by=evidence, layout=why)
        return n

    def children_of(path, evidence, depth_rows):
        """One level down, for a directory this tool cannot scan as a whole. `<ceph>/or_ready` and
        `~/data/CTSpinoPelvic1K` are trees, not corpora: their CHILDREN are the corpora, and a tree that is
        merely reported as unscannable hides every child nobody happened to list -- which is the defect."""
        dirs, _ = _entries(path)
        for d in (dirs or [])[:50]:
            q = os.path.join(path, d)
            if q in merged or q in claimed or any(inside(q, c) or q == c for c in claimed):
                continue
            k2, w2 = probe_kind(q)
            r2 = dict(name=f"{os.path.basename(path)}_{d}", path=q, evidence=f"child of {os.path.basename(path)} "
                      f"({evidence})", n_ledger_records=None, in_hand_list=False, hand_name=None, kind=k2, why=w2)
            if k2:
                depth_rows.append(r2)
                take(r2["name"], q, k2, w2, r2["evidence"])

    # PARENTS FIRST, so a directory that a shallower collection already scans is never scanned twice. Double
    # counting is not harmless here: the same crossing would be reported under two collection names and every
    # census number would be inflated, which is a different way of publishing a count nobody can check.
    for k, m in sorted(merged.items(), key=lambda kv: (len(Path(kv[0]).parts), kv[0])):
        in_hand = k in hand_paths
        row = dict(name=m["name"], path=k, evidence=", ".join(m["evidence"]), n_ledger_records=m["n_records"],
                   in_hand_list=in_hand, hand_name=hand_paths.get(k))
        rows.append(row)
        if not os.path.isdir(k):
            row["kind"] = None
            row["why"] = "declared in a root table or a ledger and not a directory on this host"
            unscannable.append(row)
            continue
        owner = next((c for c in claimed if inside(k, c)), None)
        if owner and not in_hand:
            row["kind"], row["why"] = None, f"already scanned as part of {owner}"
            row["covered_by"] = owner
            continue
        kind, why = probe_kind(k)
        row["kind"], row["why"] = kind, why
        if kind is None:
            unscannable.append(row)
            children_of(k, row["evidence"], rows)            # the tree is not a corpus; its children may be
            continue
        if in_hand:
            claimed.add(k)
            continue
        contains = sorted(c for c in claimed if inside(c, k))
        if contains:
            # scanning this as one collection would read the declared collections inside it a second time
            row["contains_declared"] = contains[:10]
            row["why"] = f"{why}; NOT scanned as one collection: it contains {len(contains)} already declared " \
                         f"({', '.join(os.path.basename(c) for c in contains[:4])})"
            children_of(k, row["evidence"], rows)
            continue
        take(m["name"], k, kind, why, row["evidence"])
    n_new = sum(1 for r in rows if not r["in_hand_list"] and r.get("kind"))
    rep = dict(enabled=True, notes=notes, n_candidates=len(cands), n_discovered=len(rows),
               n_not_in_hand_list=sum(1 for r in rows if not r["in_hand_list"]), n_added=len(add),
               n_scannable_new=n_new, n_unscannable=len(unscannable), n_hand_list=len(hand or {}),
               hand_list_not_discovered=sorted(set(hand or ()) - {r.get("hand_name") for r in rows}),
               discovered=rows, unscannable=unscannable, added=sorted(add))
    if verbose:
        print(f"discovery: {len(rows)} collections discovered, {rep['n_not_in_hand_list']} of them not in the hand "
              f"list ({len(hand or {})} entries); {len(add)} added to this run, {len(unscannable)} unscannable",
              flush=True)
        for n in notes:
            print(f"  discovery: {n}", flush=True)
    return add, rep


def scan(collections, verbose=True):
    items, census = [], {}
    for name, cfg in collections.items():
        fn = SCANNERS.get(cfg.get("kind"))
        if fn is None:
            census[name] = dict(present=False, note=f"unknown kind {cfg.get('kind')!r}")
            continue
        if not os.path.exists(cfg["path"]):
            census[name] = dict(present=False, path=cfg["path"], discovered=bool(cfg.get("discovered")),
                                note="not on this host")
            if verbose:
                print(f"{name}: MISSING {cfg['path']}", flush=True)
            continue
        got = fn(name, cfg)
        for r in got:
            r.setdefault("collection", name)
            r["discovered"] = bool(cfg.get("discovered"))
            key_item(r, cfg.get("corpus"), cfg.get("key_fallback"))
        items += got
        if not got:
            # the directory is there and the scanner found nothing in it -- a bank whose rung_*.npz were deleted
            # to free quota, a corpus whose images/ was renamed. Without this row the collection appears in NO
            # part of the report: not in the census, not in missing_collections, nothing. A clean report computed
            # over nothing is the failure shape this tool exists to prevent, so it is recorded and it fails.
            census[name] = dict(present=True, path=cfg["path"], kind=cfg.get("kind"), device=cfg.get("device"),
                                discovered=bool(cfg.get("discovered")), discovered_by=cfg.get("discovered_by"),
                                n=0, splits={}, sources={}, corpora={}, unkeyed=0,
                                note="the path exists and the scanner found nothing in it; NOTHING WAS CHECKED here")
        for r in got:
            census.setdefault(r["collection"], dict(present=True, path=cfg["path"], kind=cfg.get("kind"),
                                                    device=cfg.get("device"), discovered=bool(cfg.get("discovered")),
                                                    discovered_by=cfg.get("discovered_by"),
                                                    n=0, splits=Counter(), sources=Counter(),
                                                    corpora=Counter(), unkeyed=0))
            c = census[r["collection"]]
            c["n"] += 1
            c["splits"][r.get("split") or "?"] += 1
            c["sources"][r.get("source") or "?"] += 1
            c["corpora"][r.get("corpus") or "?"] += 1
            c["unkeyed"] += bool(r.get("unkeyed"))
        if verbose:
            print(f"{name}: {len(got)} items, {sum(1 for r in got if r.get('unkeyed'))} unkeyed", flush=True)
    for c in census.values():
        for k in ("splits", "sources", "corpora"):
            if isinstance(c.get(k), Counter):
                c[k] = dict(c[k].most_common())
    return items, census


# --------------------------------------------------------------------------------------- alias merging
def load_data_alias():
    """tools/data_alias.py is written by the ledger layer and may not exist yet. Accept either an ALIAS_GROUPS
    list of key lists, or a function alias_groups(). Absence is reported, never silently ignored."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import data_alias                                     # type: ignore  # noqa: PLC0415
    except Exception as e:                                    # noqa: BLE001
        return [], f"tools/data_alias.py not imported ({e.__class__.__name__}: {e}); only this file's ALIAS_CORPORA applied"
    groups = None
    for attr in ("ALIAS_GROUPS", "GROUPS", "ALIASES"):
        if hasattr(data_alias, attr):
            groups = getattr(data_alias, attr)
            break
    if groups is None and hasattr(data_alias, "alias_groups"):
        groups = data_alias.alias_groups()
    if groups is None:
        return [], "tools/data_alias.py imported but exposes no ALIAS_GROUPS / alias_groups()"
    out = []
    for g in groups:
        g = [str(x) for x in (g if isinstance(g, (list, tuple, set)) else [g])]
        if len(g) > 1:
            out.append(g)
    return out, f"tools/data_alias.py: {len(out)} alias groups"


def merge_keys(items, key_groups, path_groups, max_span=8):
    """Union-find over keys. Three kinds of evidence, each labelled so the report can name it:
      * key groups  -- alias groups given as `corpus:patient` keys (--alias-file, tools/data_alias.py);
      * path groups -- groups of FILE PATHS from the inventory layer (canonical.jsonl, alias_groups.json, a
        ledger's content_key / patient_key). Paths are translated through this run's own inventory.
    A group spanning more than `max_span` distinct keys is NOT merged: a degenerate content key (a blank frame
    hashes like every other blank frame) would otherwise fuse a whole corpus into one patient and manufacture
    leakage. Those groups are reported instead."""
    u = Union()
    by_path = defaultdict(set)
    for it in items:
        if it.get("key"):
            u.find(it["key"])
            if it.get("path"):
                by_path[str(it["path"]).replace("\\", "/")].add(it["key"])
    merges = Counter()
    degenerate = []
    for label, group in [("alias group", g) for g in key_groups]:
        g = sorted(set(group))
        for b in g[1:]:
            merges[label] += u.union(g[0], b, label)
    for label, paths in path_groups:
        keys = sorted({k for p in paths for k in by_path.get(str(p).replace("\\", "/"), ())})
        if len(keys) < 2:
            continue
        if len(keys) > max_span:
            degenerate.append(dict(evidence=label, n_keys=len(keys), keys=keys[:10],
                                   why=f"a single {label} spans {len(keys)} patient keys; not merged"))
            continue
        for b in keys[1:]:
            merges[label] += u.union(keys[0], b, label)
    # which evidence fused each group. A content merge (a sha256, a ledger content_key) and a name merge are
    # NOT the same claim: four black frames share a sha256 and are four patients, so a row of check (2) that
    # exists only because of a content merge has to say so or it cannot be told from a real leak.
    ev = defaultdict(set)
    for (x, y), label in u.why.items():
        ev[u.find(x)].add(label)
    for it in items:
        it["merged_key"] = u.find(it["key"]) if it.get("key") else None
        it["merged_by"] = sorted(ev.get(it["merged_key"], ())) if it.get("merged_key") else []
    return u, dict(merges=dict(merges), alias_merges=sum(v for k, v in merges.items() if "alias" in k),
                   checksum_merges=sum(v for k, v in merges.items() if "alias" not in k),
                   n_degenerate_groups=len(degenerate), degenerate_groups=degenerate[:20])


def local_key(it):
    """The key the BUILDER split on: the patient key qualified by the source name it arrived under. This is the
    view under which the NHANES double inclusion looked clean."""
    if not it.get("key"):
        return None
    return f"{it.get('source') or it['collection']}|{it['key']}"


# --------------------------------------------------------------------------------------- checks
# `val` is training for any model whose lineage says train=[...#train,val] -- the render-only detector
# anchor_none_v2_17-1882 is declared exactly that way -- so val|real_test and test|real_test are leaks too and
# were not being looked for.
SPLIT_PAIRS = (("train", "val"), ("train", "test"), ("train", "real_test"), ("val", "test"),
               ("val", "real_test"), ("test", "real_test"))


def cross_split(items, keyf, cap=50):
    by = defaultdict(lambda: defaultdict(list))
    for it in items:
        k = keyf(it)
        if k and it.get("split"):
            by[k][it["split"]].append(it)
    rows = []
    for k, bysp in by.items():
        hits = [f"{a}|{b}" for a, b in SPLIT_PAIRS if a in bysp and b in bysp]
        if hits:
            rows.append(dict(key=k, crossings=hits,
                             n_items={s: len(v) for s, v in bysp.items()},
                             items={s: sorted(i["item"] for i in v)[:4] for s, v in bysp.items()},
                             sources=sorted({i.get("source") or "" for v in bysp.values() for i in v}),
                             merged_by=sorted({e for v in bysp.values() for i in v for e in i.get("merged_by") or []}),
                             collections=sorted({i["collection"] for v in bysp.values() for i in v})))
    rows.sort(key=lambda r: (-sum(r["n_items"].values()), r["key"]))
    return dict(n=len(rows), total_items=sum(sum(r["n_items"].values()) for r in rows), shown=rows[:cap])


def check_1_local(items, cap):
    out = {}
    for coll, group in by_collection(items).items():
        r = cross_split(group, local_key, cap)
        if r["n"]:
            out[coll] = r
    return dict(n=sum(v["n"] for v in out.values()), by_collection=out,
                note="the builder's-eye view: patient key qualified by source name. A clean result here means only "
                     "that each source was split cleanly ON ITS OWN -- exactly what was true while NHANES leaked.")


def check_2_merged(items, cap):
    out = {}
    for coll, group in by_collection(items).items():
        r = cross_split(group, lambda i: i.get("merged_key"), cap)
        if r["n"]:
            out[coll] = r
    return dict(n=sum(v["n"] for v in out.values()), by_collection=out,
                note="cross-source patient key after alias and checksum merging. This is the check that matters.")


def check_3_double_source(items, cap, frac=0.5, minimum=2):
    """One source present twice under two names, found structurally: two source names inside one collection whose
    patient-key sets largely coincide. No name list is consulted."""
    rows = []
    for coll, group in by_collection(items).items():
        keys = defaultdict(set)
        split_of = defaultdict(dict)
        for it in group:
            if it.get("merged_key"):
                keys[it.get("source") or "?"].add(it["merged_key"])
                split_of[it.get("source") or "?"][it["merged_key"]] = it.get("split")
        names = sorted(keys)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                inter = keys[a] & keys[b]
                if len(inter) < minimum:
                    continue
                cont = len(inter) / max(1, min(len(keys[a]), len(keys[b])))
                if cont < frac:
                    continue
                crossed = sorted(k for k in inter if split_of[a].get(k) and split_of[b].get(k)
                                 and split_of[a][k] != split_of[b][k])
                rows.append(dict(collection=coll, source_a=a, source_b=b, n_a=len(keys[a]), n_b=len(keys[b]),
                                 n_shared=len(inter), containment=round(cont, 4),
                                 n_split_disagreement=len(crossed), examples=sorted(inter)[:cap],
                                 split_disagreement_examples=crossed[:cap],
                                 reading=f"{len(inter)} of {min(len(keys[a]), len(keys[b]))} patients of the smaller "
                                         f"source appear under both names; {len(crossed)} of them were given "
                                         f"different splits by the two copies"))
    rows.sort(key=lambda r: -r["n_shared"])
    return dict(n=len(rows), shown=rows[:cap],
                note="a source entered twice under two names. The split is drawn per source, so the two copies of a "
                     "patient are split independently -- the NHANES defect, detected without naming NHANES.")


def resolve_ref(ref, items):
    """'<collection>#train,val' -> the items. A collection glob is allowed: 'styled/*#train'."""
    name, _, sp = ref.partition("#")
    want = {s.strip() for s in sp.split(",") if s.strip()}
    got = [it for it in items if (it["collection"] == name or fnmatch.fnmatch(it["collection"], name))
           and (not want or it.get("split") in want)]
    return got


def check_4_lineage(items, lineage, cap):
    rows = []
    for model, spec in sorted(lineage.items()):
        tr, ev = [], []
        missing = []
        for r in spec.get("train", []):
            g = resolve_ref(r, items)
            tr += g
            if not g:
                missing.append(f"train {r}")
        for r in spec.get("eval", []):
            g = resolve_ref(r, items)
            ev += g
            if not g:
                missing.append(f"eval {r}")
        trk = {i["merged_key"] for i in tr if i.get("merged_key")}
        evk = {i["merged_key"] for i in ev if i.get("merged_key")}
        both = sorted(trk & evk)
        rows.append(dict(model=model, evidence=spec.get("evidence"), train=spec.get("train"), eval=spec.get("eval"),
                         n_train_items=len(tr), n_eval_items=len(ev), n_train_keys=len(trk), n_eval_keys=len(evk),
                         n_eval_keys_in_train=len(both),
                         share_of_eval_leaked=round(len(both) / len(evk), 4) if evk else None,
                         examples=both[:cap], unresolved_refs=missing))
    bad = [r for r in rows if r["n_eval_keys_in_train"]]
    return dict(n=len(bad), models=rows, shown=bad[:cap],
                note="every evaluation set against every training set of the model scored on it. An entry whose "
                     "refs did not resolve on this host is reported, not skipped silently.")


def check_5_pose_duplicates(items, cap):
    """Two renders of one CT on opposite sides of a split: the same patient key, different render/pose names.
    Only items whose NAME records a pose count here (`ctsp_0001_ap_p0`, `s0224_00_17-1882-015_...`); two films of
    one patient are a leak, but they are check (2)'s, not a pose duplicate."""
    rows = []
    for coll, group in by_collection(items).items():
        by = defaultdict(lambda: defaultdict(list))
        for it in group:
            if it.get("merged_key") and it.get("split") and (it.get("pose") or it.get("pose_key")):
                by[it["merged_key"]][it["split"]].append(it)
        for k, bysp in by.items():
            hits = [f"{a}|{b}" for a, b in SPLIT_PAIRS if a in bysp and b in bysp]
            names = {i["item"] for v in bysp.values() for i in v}
            if hits and len(names) > 1:
                rows.append(dict(collection=coll, key=k, crossings=hits,
                                 n_items={s: len(v) for s, v in bysp.items()},
                                 items={s: sorted(i["item"] for i in v)[:4] for s, v in bysp.items()}))
    rows.sort(key=lambda r: -sum(r["n_items"].values()))
    return dict(n=len(rows), shown=rows[:cap],
                note="renders of one CT under different poses, split apart. Rung crops of one film are not counted "
                     "here: they carry one case name, so they are one item.")


def check_6_styled_vs_real(items, lineage, cap):
    """A styled or pose-borrowing render is not independent of two things, and they are different things:
    the DEVICE whose formation was applied (`cios_fusion__elekta_xvi` carries Elekta style), and the SPECIMEN
    whose pose it was rendered under (`s0224_00_17-1882-015_...` stands where DeepFluoro 17-1882 stood). The
    donor is checked against the real frames of EVERY real corpus, because the donor's corpus need not be the
    styled corpus's device."""
    rows = []
    by_coll = by_collection(items)
    real = {}                                                  # collection -> {split: {merged_key}}
    dev_real = {}                                              # device -> [collections of real frames]
    for coll, group in by_coll.items():
        if not any(i["kind"] == "realxray" for i in group):
            continue
        d = defaultdict(set)
        for i in group:
            if i.get("merged_key"):
                d[i.get("split") or "?"].add(i["merged_key"])
        real[coll] = d
        dev = next((i.get("device") for i in group if i.get("device")), None)
        if dev:
            dev_real.setdefault(dev, []).append(coll)
    for dev, coll in DEVICE_REAL.items():
        if coll in real and coll not in dev_real.get(dev, []):
            dev_real.setdefault(dev, []).append(coll)
    for coll, group in by_coll.items():
        styled = [i for i in group if i["kind"] == "styled" or i.get("pose_key")]
        if not styled:
            continue
        dev = next((i.get("device") for i in styled if i.get("device")), None)
        pose_keys = {i["pose_key"] for i in styled if i.get("pose_key")}
        row = dict(collection=coll, device=dev, real_collections_of_device=dev_real.get(dev or "", []),
                   n_items=len(styled), n_pose_donors=len(pose_keys), pose_donors=sorted(pose_keys)[:cap],
                   donor_in_real=[], n_donor_in_real_heldout=0)
        for rc, d in real.items():
            for sp, keys in d.items():
                hit = sorted(pose_keys & keys)
                if hit:
                    row["donor_in_real"].append(dict(real_collection=rc, split=sp, n=len(hit), keys=hit[:cap]))
                    if sp in ("test", "val", "real_test"):
                        row["n_donor_in_real_heldout"] += len(hit)
        # the lineage form: styled frames in training while that device's real frames are what the model is scored on
        for model, spec in lineage.items():
            tr = {r.partition("#")[0] for r in spec.get("train", [])}
            ev = {r.partition("#")[0] for r in spec.get("eval", [])}
            if any(fnmatch.fnmatch(coll, t) for t in tr) and (ev & set(dev_real.get(dev or "", []))):
                row.setdefault("models_training_on_it_and_scored_on_that_device", []).append(model)
        rows.append(row)
    bad = [r for r in rows if r["n_donor_in_real_heldout"] or r.get("models_training_on_it_and_scored_on_that_device")]
    return dict(n=len(bad), all_styled=rows[:cap], shown=bad[:cap],
                note="a styled frame carries a device's formation AND, when its name records one, the pose of a real "
                     "specimen. Training on it and scoring on that device's held-out frames is not a device-held-out "
                     "result, and training on a render taken under a held-out specimen's pose is not held out either.")


# --------------------------------------------------------------------------------------- CHK-9
# WHY. Checks (1)-(6) compare the splits of banks and ask whether a TEST item is in a TRAIN set. On 2026-09-23 a curve
# was scored on the subjects its detectors were SELECTED on (their val split), and on a detector whose parent had
# trained on them; every one of (1)-(6) was blind to both, because val counted as evaluation and nothing followed a
# checkpoint to what it was initialised from. CHK-9 asks the question of every QUOTED number instead of every bank:
# for each (checkpoint, evaluation set) pair behind a row of SchwingNet/results/eval_gate/quoted_results.json, the
# evaluation set's patient keys (eval_sets.json, `tools/eval_gate.py eval-sets`) must not meet the train OR val keys
# of the checkpoint or of any ancestor (touched.json, tools/checkpoint_lineage.py). An unresolved chain FAILS: unknown
# is not clean. The comparison is tools/eval_gate.assess -- the same code every evaluator runs before it scores.
def _chk9_instances(path_field, store):
    """quoted `path` (';'-separated components; {K}, <k>, <seed> templates) -> ({bind K or '': [store keys]}, [why])."""
    import eval_gate as EG
    comps = [c.strip().split(" (")[0].strip() for c in str(path_field or "").split(";") if c.strip()]
    got, missing = defaultdict(list), []
    for c in comps:
        rx = re.escape(EG.norm_path(c)).replace("<k>", r"\d+").replace("<seed>", r"\d+")
        rx = rx.replace(r"\{K\}", r"(?P<K>\d+)", 1).replace(r"\{K\}", r"(?P=K)")   # one fold K per path
        rx = re.compile(rx)
        n = 0
        for k in store.entries:
            m = rx.fullmatch(k)
            if m:
                got[m.groupdict().get("K") or ""].append(k)
                n += 1
        if not n:
            missing.append(f"no lineage row matches {c}")
    return got, missing


CHK9_CARDS = REPO / "docs" / "devices"


def _chk9_card(device, cards=None):
    """A device card's per-fold gate: `eval_gate` inside docs/devices/<device>.json (tools/device_fit.py fit) or the
    record eval_gate/<device>.json (tools/device_fit.py gate). No record is UNRESOLVED, never clean."""
    d = Path(cards or CHK9_CARDS)
    blk = None
    for p in (d / "eval_gate" / f"{device}.json", d / f"{device}.json"):
        if p.exists():
            try:
                j = json.load(open(p, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            blk = j if "checks" in j and "held_out" in j else j.get("eval_gate")
            if blk:
                src = str(p)
                break
    if not blk:
        return dict(verdict="UNRESOLVED", why=f"device card {device}: no per-fold gate record ({d}/eval_gate/{device}.json "
                                              f"or `eval_gate` in {device}.json); run `tools/device_fit.py gate --device {device}`")
    ov = int(blk.get("overlap") or 0); un = int(blk.get("unresolved") or 0)
    v = ("DECLARED" if blk.get("not_held_out_reason") else "SEEN" if ov else "UNRESOLVED" if un else
         "HELD OUT" if blk.get("held_out") else "UNRESOLVED")
    held = [c.get("eval_set") for c in blk.get("checks") or [] if c.get("overlap")]
    return dict(verdict=v, why=f"{src}: {blk.get('n_checks')} folds, {len(held)} whose held subjects were also fitted on"
                               f"{(' (' + ', '.join(map(str, held[:6])) + ')') if held else ''}"
                               + (f"; declared: {blk['not_held_out_reason']}" if blk.get("not_held_out_reason") else ""),
                instances=[dict(checkpoint=f"card:{device}", fold=c.get("eval_set"), verdict=("SEEN" if c.get("overlap") else "HELD OUT"),
                                n_eval_keys=c.get("n_keys"), overlap=c.get("overlap"), overlap_at=c.get("overlap_by") or {},
                                unresolved=c.get("unresolved")) for c in blk.get("checks") or []])


CHK9_FIG4_PAIRS = REPO / "SchwingNet" / "results" / "fig4_pairs" / "fig4_pairs.json"


def _chk9_card_median(device, cards=None, pairs_json=None):
    """A number computed under the MEDIAN of a card's fold fits (Figure S2a, fig4_pairs_pull.py). The gate verdict that
    fig4_pairs_pull now writes into fig4_pairs.json is used when present. A pre-gate output is decided from the card's
    per-fold record: the median is taken over every fold's fit, and fold k fitted every group but k, so with two or more
    folds every group -- the pair's included -- was fitted by at least one of the fits the median is taken over."""
    pj = Path(pairs_json or CHK9_FIG4_PAIRS)
    if pj.exists():
        try:
            blk = ((json.load(open(pj, encoding="utf-8")).get("devices") or {}).get(device) or {}).get("eval_gate")
        except Exception:  # noqa: BLE001
            blk = None
        if isinstance(blk, dict) and "held_out" in blk:
            ov = int(blk.get("overlap") or 0)
            v = ("DECLARED" if blk.get("not_held_out_reason") else "SEEN" if ov else "UNRESOLVED" if blk.get("unresolved")
                 else "HELD OUT" if blk.get("held_out") else "UNRESOLVED")
            return dict(verdict=v, why=f"{pj}#devices/{device}/eval_gate (overlap {ov})"
                        + (f"; declared: {blk['not_held_out_reason']}" if blk.get("not_held_out_reason") else ""),
                        instances=[])
    card = _chk9_card(device, cards)
    folds = [i.get("fold") for i in card.get("instances") or []]
    if len(folds) < 2:
        return dict(verdict="UNRESOLVED", why=f"card {device}: {pj} carries no eval_gate block (written before the gate) "
                                              f"and the per-fold record lists {len(folds)} fold(s), so which fits saw "
                                              "which group cannot be read", instances=[])
    return dict(verdict="SEEN", why=f"{pj} carries no eval_gate block (written before the gate); the median is over "
                                    f"{len(folds)} fold fits of {device} and each group ({', '.join(map(str, folds[:6]))}) was "
                                    f"fitted by the {len(folds) - 1} fits that did not hold it out (per-fold record: "
                                    f"{card.get('why', '')[:160]})",
                instances=[dict(checkpoint=f"card_median:{device}", fold=f, verdict="SEEN", n_eval_keys=None,
                                overlap=1, overlap_at={f"median over {len(folds)} fold fits": len(folds) - 1},
                                unresolved=0) for f in folds])


def check_9_eval_vs_selection_lineage(quoted, store, eval_sets, declared=None, cap=50):
    """Every quoted row's (checkpoint, evaluation set) pairs through eval_gate.assess. Row verdicts: HELD OUT, SEEN
    (a key in a train/val set on the chain), UNRESOLVED (a link, a checkpoint or its lineage unknown), NO EVAL KEYS
    (the evaluation set could not be listed or keyed), DECLARED (not held out, and a declaration says why), N/A."""
    import eval_gate as EG
    declared = declared or {}
    ck_table = quoted.get("checkpoints") or {}
    sets = (eval_sets or {}).get("sets") or {}
    memo = {}
    rows = []
    for r in quoted.get("rows") or []:
        pairs = r.get("per_pair") or []
        out = dict(id=r.get("id"), source=r.get("source"), quoted=str(r.get("quoted") or "")[:200],
                   inventory_verdict=r.get("heldout_under_rule"), pairs=[])
        if not pairs:
            iv = r.get("heldout_under_rule")
            if iv in ("NOT HELD OUT", "MIXED", "NOT ESTABLISHED"):
                # the inventory found a reason this number is not held out, or could not tell, and names no pair this
                # check can test: that is not a pass (2026-09-24: Figure S2a sat here as N/A while the inventory said
                # NOT HELD OUT)
                out["verdict"] = "UNRESOLVED"
                out["pairs"] = [dict(checkpoint=None, eval_set=None, verdict="UNRESOLVED", instances=[],
                                     why=f"inventory verdict {iv} with no (checkpoint, evaluation set) pair to check: "
                                         f"{str(r.get('why') or '')[:400]}")]
            else:
                out["verdict"] = "N/A"
            rows.append(out)
            continue
        for p in pairs:
            ck, es = p.get("checkpoint"), p.get("eval_set")
            spec = ck_table.get(ck)
            prow = dict(checkpoint=ck, eval_set=es, instances=[])
            if str(ck).startswith("card_median:"):
                prow.update(_chk9_card_median(str(ck)[len("card_median:"):]))
                out["pairs"].append(prow)
                continue
            if str(ck).startswith("card:"):
                # a device-card fit is not a checkpoint: its folds are gated by tools/device_fit.py (fit, or `gate` alone),
                # which writes the per-fold verdict beside the card; that record is what this row is checked against
                prow.update(_chk9_card(str(ck)[5:]))
                out["pairs"].append(prow)
                continue
            S = sets.get(es)
            if S is None:
                prow.update(verdict="NO EVAL KEYS", why=f"evaluation set {es!r} is not in eval_sets.json (no key list: "
                                                         "`tools/eval_gate.py eval-sets` has no spec for it or failed)")
                out["pairs"].append(prow)
                continue
            if not spec or spec.get("public") or not spec.get("path"):
                prow.update(verdict="UNRESOLVED", why=f"checkpoint {ck!r} has no path in quoted_results.json "
                                                       "checkpoints, so no lineage row can be found for it (a device-card "
                                                       "fit or an unlisted model is not a checkpoint the store describes)")
                out["pairs"].append(prow)
                continue
            inst, missing = _chk9_instances(spec["path"], store)
            if missing or not inst:
                prow.update(verdict="UNRESOLVED", why="; ".join(missing) or f"no lineage row matches {spec['path']}")
                out["pairs"].append(prow)
                continue
            verdicts = []
            for bind, cks in sorted(inst.items()):
                fold = (S.get("folds") or {}).get(bind) if bind else None
                keys = (fold or S)["keys"]
                n_unk = (fold or S).get("n_unkeyed", 0)
                for c in cks:
                    mk = (c, es, bind)
                    if mk not in memo:
                        memo[mk] = EG.assess(keys, c, "tools/leak_check.py CHK-9", eval_set=f"{es}{'#fold' + bind if bind else ''}",
                                             touched=store, compute=False)
                    h = memo[mk]
                    v = ("SEEN" if h["overlap"] else "UNRESOLVED" if h["unresolved"] else
                         "NO EVAL KEYS" if (not h["n_keys"] or n_unk) else "HELD OUT")
                    verdicts.append(v)
                    prow["instances"].append(dict(checkpoint=c, fold=bind or None, verdict=v, n_eval_keys=h["n_keys"],
                                                  n_eval_unkeyed=n_unk, overlap=h["overlap"], overlap_keys=h["overlap_keys"][:10],
                                                  overlap_at=h.get("overlap_by") or {}, unresolved=h["unresolved"],
                                                  unresolved_what=[f"{u.get('at')}: {u.get('what')}" for u in h["unresolved_rows"][:5]],
                                                  pose_donor_overlap=h["pose_donor_overlap"]))
            prow["verdict"] = next((v for v in ("SEEN", "UNRESOLVED", "NO EVAL KEYS") if v in verdicts), "HELD OUT")
            out["pairs"].append(prow)
        pv = [p["verdict"] for p in out["pairs"]]
        # a pair already declared not held out (a device card fitted with --not-held-out) makes the row DECLARED, never HELD OUT
        out["verdict"] = next((v for v in ("SEEN", "UNRESOLVED", "NO EVAL KEYS", "DECLARED") if v in pv), "HELD OUT")
        if out["verdict"] != "HELD OUT" and declared.get(out["id"]):
            out["declared_not_held_out"] = declared[out["id"]]
            out["verdict_before_declaration"] = out["verdict"]
            out["verdict"] = "DECLARED"
        rows.append(out)
    c = Counter(r["verdict"] for r in rows)
    bad = [r for r in rows if r["verdict"] in ("SEEN", "UNRESOLVED", "NO EVAL KEYS")]
    # rows the hand-mapped inventory (EVALUATORS.md) and this check read differently, in either direction: an inventory
    # HELD OUT that CHK-9 finds seen or cannot establish, and a CHK-9 HELD OUT the inventory did not grant
    disagree = [dict(id=r["id"], chk9=r["verdict"], inventory=r["inventory_verdict"]) for r in rows
                if r["verdict"] == "HELD OUT" and r["inventory_verdict"] not in ("HELD OUT",)
                or r["verdict"] in ("SEEN", "UNRESOLVED", "NO EVAL KEYS") and r["inventory_verdict"] == "HELD OUT"]
    return dict(n=c.get("SEEN", 0), n_seen=c.get("SEEN", 0), n_unresolved=c.get("UNRESOLVED", 0),
                n_no_eval_keys=c.get("NO EVAL KEYS", 0), n_held_out=c.get("HELD OUT", 0), n_declared=c.get("DECLARED", 0),
                n_not_applicable=c.get("N/A", 0), n_rows=len(rows), shown=bad[:cap], rows=rows,
                disagree_with_inventory=disagree[:cap], n_disagree_with_inventory=len(disagree),
                note="every quoted (checkpoint, evaluation set) pair: the evaluation patients against the train AND "
                     "val/selection keys of the checkpoint and of every ancestor in its initialisation chain "
                     "(tools/eval_gate.assess over touched.json). SEEN fails the run as a leak; UNRESOLVED and NO EVAL "
                     "KEYS fail it as not established (unknown is not clean); DECLARED rows name their reason.")


def run_chk9(quoted_path, touched_path, eval_sets_path, declared_path=None, cap=50):
    """(check dict, problems). Every input is named; one that cannot be read is a problem, never a skip."""
    import eval_gate as EG
    problems, docs = [], {}
    for flag, p in (("--quoted-results", quoted_path), ("--touched", touched_path), ("--eval-sets", eval_sets_path),
                    ("--declared", declared_path)):
        if p is None:
            if flag != "--declared":
                problems.append(dict(flag=flag, path="(not given)", why="CHK-9 needs --quoted-results, --touched and "
                                                                          "--eval-sets together"))
            continue
        try:
            docs[flag] = json.load(open(p, encoding="utf-8")) if flag != "--touched" else EG.Store(p)
        except Exception as e:  # noqa: BLE001
            problems.append(dict(flag=flag, path=str(p), why=f"{type(e).__name__}: {e}"))
    if problems:
        return None, problems
    res = check_9_eval_vs_selection_lineage(docs["--quoted-results"], docs["--touched"], docs["--eval-sets"],
                                            docs.get("--declared"), cap)
    res["inputs"] = dict(quoted_results=str(quoted_path), touched=str(touched_path), eval_sets=str(eval_sets_path),
                         declared=str(declared_path) if declared_path else None,
                         eval_sets_failed=(docs["--eval-sets"].get("failed") or {}))
    return res, []


def write_chk9_md(res, path):
    L = ["# CHK-9: evaluation vs selection and lineage (generated by `tools/leak_check.py chk9` -- do not edit)\n",
         f"{res['n_rows']} quoted rows: **{res['n_seen']} SEEN**, **{res['n_unresolved']} UNRESOLVED**, "
         f"{res['n_no_eval_keys']} NO EVAL KEYS, {res['n_held_out']} HELD OUT, {res['n_declared']} DECLARED, "
         f"{res['n_not_applicable']} N/A.\n", f"\n{res['note']}\n",
         f"\nInputs: {json.dumps(res['inputs'])}\n",
         "\n| row | verdict | pair | why |\n|---|---|---|---|\n"]
    for r in res["rows"]:
        if r["verdict"] in ("HELD OUT", "N/A"):
            continue
        for p in r["pairs"]:
            if p["verdict"] == "HELD OUT":
                continue
            why = p.get("why") or "; ".join(
                (f"{i['checkpoint'].split('/runs/')[-1]}{'#' + i['fold'] if i.get('fold') else ''}: "
                 + (f"{i['overlap']} of {i['n_eval_keys']} seen at {i['overlap_at']}" if i["overlap"] else
                    f"unresolved {i['unresolved_what']}" if i["unresolved"] else f"{i['n_eval_unkeyed']} unkeyed"))
                for i in p["instances"] if i["verdict"] != "HELD OUT")
            L.append(f"| `{r['id']}` | {r['verdict']} | {p['checkpoint']} on {p['eval_set']} | {_c(why[:700])} |\n")
    if res["disagree_with_inventory"]:
        L.append("\n## Rows where CHK-9 and EVALUATORS.md disagree\n\n| row | CHK-9 | inventory |\n|---|---|---|\n")
        for d in res["disagree_with_inventory"]:
            L.append(f"| `{d['id']}` | {d['chk9']} | {d['inventory']} |\n")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    open(path, "w", encoding="utf-8").write("".join(L))


def cmd_chk9(a):
    res, problems = run_chk9(a.quoted_results, a.touched, a.eval_sets, a.declared, a.cap)
    if problems:
        for p in problems:
            print(f"CHK9 COULD NOT RUN: {p['flag']} {p['path']}: {p['why']}")
        print("CHK9_EXIT 3 (COULD NOT RUN)")
        return 3
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out / "chk9_report.json", "w"), indent=1, default=str)
    write_chk9_md(res, out / "CHK9_REPORT.md")
    ex = 1 if res["n_seen"] else (3 if (res["n_unresolved"] or res["n_no_eval_keys"]) else 0)
    print(f"CHK9 {'PASS' if ex == 0 else 'FAIL'}  rows {res['n_rows']}  seen {res['n_seen']}  unresolved "
          f"{res['n_unresolved']}  no_eval_keys {res['n_no_eval_keys']}  held_out {res['n_held_out']}  declared "
          f"{res['n_declared']}  n/a {res['n_not_applicable']}  -> {out / 'chk9_report.json'}")
    meaning = {0: "checked, nothing seen", 1: "LEAK FOUND", 3: "NOT ESTABLISHED"}[ex]
    print(f"CHK9_EXIT {ex} ({meaning})")
    return ex


def padding_gaps(items, cap):
    r"""Two keys of one corpus whose patient ids are the same number written with different leading zeros.

    `ctsp_0001` and `ctsp_1`, `nhanes_00160` and `nhanes_160`, `buu_003` and `buu_0003` are one patient and two
    keys, and every rule in the table above accepts both spellings (`\d{3,6}`, `\d{3,5}`). This is the form the
    identity defect takes in this project often enough to be written into its house rules: "case ids are
    zero-padded in the release (0001) and were not in the old CSVs (1); zfill(4) before diffing." The pair is
    NOT merged -- a merge on a guess manufactures leakage -- it is reported, and it fails only when the two
    spellings land on opposite sides of one split, which is the same escalation the declared gaps get."""
    rows = []
    for coll, group in by_collection(items).items():
        by_num = defaultdict(lambda: defaultdict(set))
        for it in group:
            k = it.get("merged_key") or ""
            corpus, _, pat = k.partition(":")
            if pat.isdigit():
                by_num[(corpus, int(pat))][k].add(it.get("split") or "?")
        for (corpus, num), spellings in sorted(by_num.items()):
            if len(spellings) < 2:
                continue
            sides = {k: sorted(v) for k, v in spellings.items()}
            straddle = any({"train"} & set(a) and {"val", "test", "real_test"} & set(b)
                           for a in sides.values() for b in sides.values() if a is not b)
            rows.append(dict(collection=coll, a=f"^{corpus}:0*{num}$", b=f"^{corpus}:0*{num}$",
                             why=f"{corpus} patient {num} is keyed under {len(sides)} spellings that differ only "
                                 f"by leading zeros ({', '.join(sorted(sides))}); the rules accept both and "
                                 f"nothing on disk relates them",
                             fix="normalise the id at the source, or supply the pair with --alias-file",
                             n_a={s: 1 for k in sides for s in sides[k]}, n_b={},
                             spellings=sides, both_spellings_straddle_a_split=straddle))
    return rows[:cap]


def check_alias_gaps(items, cap):
    """Declared-but-unresolvable aliases: report always, escalate when both spellings straddle one split."""
    rows = []
    for gap in ALIAS_GAPS:
        ra, rb = re.compile(gap["a"]), re.compile(gap["b"])
        # a gap whose two spellings are the SAME pattern (csxa: one image is one patient, because the release
        # gives no patient identity) put every key in the first branch of the if/elif below, left b_sp empty and
        # so was never emitted at all -- a declared limitation that no run could ever print.
        self_gap = gap["a"] == gap["b"]
        for coll, group in by_collection(items).items():
            a_sp = defaultdict(set)
            b_sp = defaultdict(set)
            for it in group:
                k = it.get("merged_key") or ""
                if ra.match(k):
                    a_sp[it.get("split") or "?"].add(k)
                elif rb.match(k):
                    b_sp[it.get("split") or "?"].add(k)
            if self_gap:
                if a_sp:
                    rows.append(dict(collection=coll, a=gap["a"], b=gap["b"], why=gap["why"], fix=gap["fix"],
                                     n_a={s: len(v) for s, v in a_sp.items()}, n_b={},
                                     both_spellings_straddle_a_split=False,
                                     note="one spelling: this gap cannot be tested from names. It is listed so a "
                                          "clean result over this corpus is not read as a verified one."))
                continue
            if a_sp and b_sp:
                straddle = bool({"train"} & set(a_sp)) and bool({"val", "test"} & set(b_sp)) or \
                           bool({"train"} & set(b_sp)) and bool({"val", "test"} & set(a_sp))
                rows.append(dict(collection=coll, a=gap["a"], b=gap["b"], why=gap["why"], fix=gap["fix"],
                                 n_a={s: len(v) for s, v in a_sp.items()}, n_b={s: len(v) for s, v in b_sp.items()},
                                 both_spellings_straddle_a_split=straddle))
    rows += padding_gaps(items, cap)
    return dict(n=sum(1 for r in rows if r["both_spellings_straddle_a_split"]), shown=rows[:cap],
                note="overlaps that are believed real and cannot be resolved from the files on disk. Not assumed "
                     "away: listed, and counted as a failure only when both spellings land on opposite sides.")


def by_collection(items):
    out = defaultdict(list)
    for it in items:
        out[it["collection"]].append(it)
    return out


# --------------------------------------------------------------------------------------- report
def _c(x):
    """One Markdown table cell: a pipe inside a key (`nhanes|nhanes:00160`) or a crossing (`train|val`) would open
    a new column, so it is escaped here rather than in every call site."""
    return str(x).replace("|", "\\|")


def write_md(rep, path):
    L = []
    v = rep["verdict"]
    L.append("# Data leakage report (generated by `tools/leak_check.py` -- do not edit by hand)\n")
    L.append(f"Generated {rep['generated']} on `{rep['host']}`.\n")
    n_read = sum(1 for c in rep["census"].values() if c.get("present") and c.get("n"))
    L.append(f"**{'PASS' if v['pass'] else 'FAIL'}** -- {rep['n_items']} items over {n_read} of "
             f"{len(rep['census'])} declared collections, "
             f"{rep['keying']['n_unkeyed']} unkeyed, {len(v.get('missing_collections') or [])} collections absent, "
             f"{len(v.get('empty_collections') or [])} present but empty. " +
             (f"Over those {n_read} collections, no test item and no alias of one is in a training set of the "
              "model scored on it. This says nothing about any collection not listed in the census below.\n"
              if v["pass"] else
              f"Failing: {', '.join(v['failed']) or ('unkeyed items' if v.get('unkeyed_fails') else 'nothing was read')}.\n"))
    L.append(f"\nExit {v['exit']}: "
             + {0: "checked, no leak.", 1: "**LEAKAGE FOUND.**", 2: "items could not be keyed.",
                3: "**COULD NOT RUN / incomplete coverage** -- this is not a statement about leakage."}[v["exit"]]
             + (f" The run was also incomplete ({'; '.join(v.get('could_not_run_reasons') or [])}), which the exit "
                "code cannot say because a found leak outranks it.\n" if v.get("could_not_run") and v["exit"] == 1
                else "\n"))
    if v.get("read_nothing"):
        L.append("\n**Nothing was read at all.** Every check below is a count over an empty inventory and none of "
                 "them means anything. Fix the paths, or the host, and run it again.\n")
    if rep.get("input_problems"):
        L.append(f"\n### Inputs named on the command line that were not usable ({len(rep['input_problems'])})\n\n"
                 "The run was told to use this evidence and did not, so it cannot report a clean sheet.\n\n"
                 "| flag | path | why |\n|---|---|---|\n")
        for p in rep["input_problems"]:
            L.append(f"| `{p['flag']}` | `{p['path']}` | {p['why']} |\n")
    if v.get("empty_collections"):
        L.append(f"\nPresent on this host but EMPTY, therefore NOT CHECKED: {', '.join(v['empty_collections'])}. "
                 "The path exists and the scanner found nothing in it.\n")
    if v.get("unresolved_lineage_refs"):
        L.append(f"\nLineage refs that name a collection this run did not scan, so the model's row in check (4) "
                 f"was computed over an unread training set: {', '.join(v['unresolved_lineage_refs'])}.\n")
    if v.get("missing_collections"):
        L.append(f"\nNot on this host, therefore NOT CHECKED: {', '.join(v['missing_collections'])}. "
                 "Nothing below says anything about them.\n")
    if v.get("collections_without_splits"):
        L.append(f"\nNo split recorded, so no disjointness could be checked inside them: "
                 f"{', '.join(v['collections_without_splits'])}. Their items still count towards every check that "
                 "compares collections.\n")
    L.append("\n## How the identity key is built\n")
    L.append("An item's key is `corpus:patient`, from the first of (recorded patient id, recorded case, file stem, "
             "relative path) that a rule in `RULES` matches. The key is CROSS-SOURCE by construction: "
             "`nhanes_00160`, `NHANES_nhanes_cervical_00160` and `NH_00160_c` all key to `nhanes:00160`. "
             "**A path matching no rule is not treated as unique** -- it is reported below and fails the run.\n")
    L.append(f"\nAlias sources: {rep['keying']['alias_note']}; "
             f"{rep['keying']['alias_merges']} alias merges, {rep['keying']['checksum_merges']} content merges "
             f"({rep['keying'].get('merges') or 'none'}).\n")
    for n in rep["keying"].get("identity_files") or []:
        L.append(f"- identity evidence: {n}\n")
    if rep["keying"].get("n_degenerate_groups"):
        L.append(f"\n{rep['keying']['n_degenerate_groups']} identity token(s) spanned more than the allowed number of "
                 "patients and were NOT merged (a blank or near-blank frame hashes like every other one):\n\n")
        for g in rep["keying"]["degenerate_groups"]:
            L.append(f"- {g['evidence']}: {g['n_keys']} keys, e.g. {', '.join(g['keys'][:5])}\n")
    if rep["keying"]["n_unkeyed"]:
        nd = rep["keying"].get("n_unkeyed_in_discovered") or 0
        L.append(f"\n### Unkeyed items ({rep['keying']['n_unkeyed']})\n\n")
        if nd:
            L.append(f"{nd} of them are in DISCOVERED collections -- directories no hand list named, which "
                     "therefore declare no corpus and no `key_fallback`. That is discovery working: the names "
                     "were always there and nothing was reading them. Give the collection an entry (with "
                     "`corpus`, and `key_fallback` if its names carry no subject) or add a rule.\n\n")
        L.append("| collection | item | why |\n|---|---|---|\n")
        for r in rep["keying"]["unkeyed"]:
            L.append(f"| {r['collection']} | `{r['item']}` | {r['why']} |\n")
    if rep["keying"]["corpus_conflicts"]:
        L.append(f"\n### Names resolving to a corpus their directory does not declare "
                 f"({rep['keying']['n_corpus_conflicts']})\n\n| collection | item | resolved |\n|---|---|---|\n")
        for r in rep["keying"]["corpus_conflicts"]:
            L.append(f"| {r['collection']} | `{r['item']}` | {r['conflict']} |\n")
    h = rep.get("hash_evidence")
    if h:
        L.append("\n## Byte identity (`--hash`): evidence, not identity\n\n"
                 f"{h['n_hashed']} files hashed ({h['n_container_members']} bank members have no file of their "
                 f"own, {h['n_over_cap']} were over the size cap, {h['n_no_file_on_disk']} had no file on disk, "
                 f"{h['n_failed']} were unreadable). {h['n_groups']} groups of byte-identical files: "
                 f"**{h['n_corroborating']} corroborate one patient key, {h['n_conflicts']} span two or more "
                 f"patient keys and were NOT merged**, and {h['n_merges']} merges were made from bytes alone.\n\n"
                 f"{h['note']}\n")
        if h["conflicts"]:
            L.append("\n### Hash conflicts: one file content, two or more patients\n\n"
                     "| sha256 | files | bytes | patient keys | splits | collections | why equal | declared gap |\n"
                     "|---|---:|---:|---|---|---|---|---|\n")
            for r in h["conflicts"]:
                L.append(f"| `{r['sha256']}` | {r['n_files']} | {r['size_bytes']} | "
                         f"{_c(', '.join(r['keys']))} | {_c(', '.join(r['splits']))} | "
                         f"{_c(', '.join(r['collections']))} | {r['why_equal']} | "
                         f"{'yes -- ' + r['declared_gap'][:80] if r['declared_gap'] else 'no'} |\n")
            L.append("\nPaths of the first conflicts, so the claim can be checked by hand:\n\n")
            for r in h["conflicts"][:10]:
                L.append(f"- `{r['sha256']}` ({', '.join(r['keys'])}): {', '.join('`%s`' % p for p in r['paths'])}\n")
        if h["hints"]:
            L.append(f"\n### Hints for unkeyed items ({h['n_hints']})\n\nByte-identical to a file the rules could "
                     "key. This is a rule waiting to be written, not a key: nothing below was merged on it.\n\n"
                     "| sha256 | keyed as | unkeyed items |\n|---|---|---|\n")
            for r in h["hints"]:
                L.append(f"| `{r['sha256']}` | `{_c(r['key'])}` | {_c(', '.join(r['unkeyed_items']))} |\n")
    d = rep.get("discovery") or {}
    L.append("\n## What was enumerated\n\n")
    if not d.get("enabled"):
        L.append(f"**Collection discovery was OFF** ({d.get('why', '?')}). The census below is the hand list, and "
                 "a hand list cannot notice a collection nobody added to it. Nothing here says anything about any "
                 "directory that is not in the table.\n")
    else:
        L.append(f"**{d['n_discovered']} collections discovered, {d['n_not_in_hand_list']} of them not in the hand "
                 f"list** ({d.get('n_hand_list', 0)} entries). {d['n_added']} were added to this run and "
                 f"{d['n_unscannable']} could not be scanned. Sources: a --ledger's own roots, "
                 "`data_ledger.discover_roots()` (its static table, its globbed families, "
                 "`tools/data_manifest.py` ROOTS and `tools/corpus_manifold.py` SETS) and the crop-bank globs.\n")
        for n in d.get("notes") or []:
            L.append(f"\n- {n}")
        if d.get("hand_list_not_discovered"):
            L.append(f"\n\nDeclared by hand and NOT found by discovery (so they are on no root table and match no "
                     f"glob -- check the path): {', '.join(d['hand_list_not_discovered'])}.\n")
        new = [r for r in d.get("discovered") or [] if not r.get("in_hand_list") and r.get("kind")]
        if new:
            L.append(f"\n### Discovered and NOT in the hand list ({len(new)})\n\n"
                     "| collection | kind | layout that identified it | found by | path |\n|---|---|---|---|---|\n")
            for r in new[:200]:
                L.append(f"| {r['name']} | {r['kind']} | {r['why']} | {r['evidence']} | `{r['path']}` |\n")
        if d.get("unscannable"):
            L.append(f"\n### Discovered and UNSCANNABLE ({d['n_unscannable']})\n\n"
                     "Enumerated, and no scanner here can read them. They are NOT checked and nothing below "
                     "covers them; they are listed because a collection absent from this report is exactly how "
                     "the hand list hid the cross-validation banks.\n\n"
                     "| name | why | found by | path |\n|---|---|---|---|\n")
            for r in d["unscannable"][:200]:
                L.append(f"| {r.get('name')} | {r.get('why')} | {r.get('evidence')} | `{r.get('path')}` |\n")
    L.append("\n## Census\n\n| collection | kind | source | items | splits | sources | unkeyed |\n"
             "|---|---|---|---:|---|---|---:|\n")
    for name, c in sorted(rep["census"].items()):
        src = "discovered" if c.get("discovered") else "declared"
        if not c.get("present"):
            L.append(f"| {name} | - | {src} | - | not on this host | | |\n")
            continue
        L.append(f"| {name} | {c.get('kind')} | {src} | {c['n']} | {c['splits']} | "
                 f"{', '.join(list(c['sources'])[:4])} | {c['unkeyed']} |\n")
    titles = {"1_within_collection_builder_key": "(1) split disjointness on the builder's key (per source)",
              "2_within_collection_merged_key": "(2) split disjointness on the cross-source key -- THE CHECK",
              "3_source_entered_twice": "(3) one source entered twice under two names",
              "4_eval_vs_training": "(4) evaluation sets against the training sets of the model scored on them",
              "5_render_pose_duplicates": "(5) renders of one CT split apart",
              "6_styled_vs_real_device": "(6) styled corpora against the real frames of their device",
              "alias_gaps": "(x) declared aliases that cannot be resolved from disk",
              "9_eval_vs_selection_lineage": "(CHK-9) quoted results against the train AND val sets of the scored "
                                             "checkpoint and every ancestor"}
    for k, title in titles.items():
        if k not in rep["checks"]:
            if k == "9_eval_vs_selection_lineage":
                L.append(f"\n## {title}\n\n**NOT RUN**: no --quoted-results was given, so no quoted number was checked "
                         "against what its checkpoint was selected on. `tools/leak_check.py chk9` runs it alone.\n")
            continue
        c = rep["checks"][k]
        L.append(f"\n## {title}\n\n**{c['n']}** flagged. {c['note']}\n")
        if k == "9_eval_vs_selection_lineage":
            L.append(f"\n{c['n_seen']} SEEN, {c['n_unresolved']} UNRESOLVED, {c['n_no_eval_keys']} NO EVAL KEYS, "
                     f"{c['n_held_out']} HELD OUT, {c['n_declared']} DECLARED, {c['n_not_applicable']} N/A, of "
                     f"{c['n_rows']} quoted rows.\n\n| row | verdict | pairs not held out |\n|---|---|---|\n")
            for r in c["shown"]:
                ps = "; ".join(f"{p['checkpoint']} on {p['eval_set']}: {p['verdict']}" for p in r["pairs"]
                               if p["verdict"] != "HELD OUT")
                L.append(f"| `{r['id']}` | {r['verdict']} | {_c(ps[:400])} |\n")
            continue
        if k in ("1_within_collection_builder_key", "2_within_collection_merged_key"):
            for coll, r in sorted(c.get("by_collection", {}).items()):
                L.append(f"\n`{coll}`: {r['n']} keys on both sides ({r['total_items']} items)\n\n"
                         "| key | crossings | items | fused by |\n|---|---|---|---|\n")
                for row in r["shown"]:
                    it = "; ".join(f"{s}: {', '.join(v)}" for s, v in row["items"].items())
                    # a row that exists only because a content token fused two keys is a different claim from a
                    # row the name rules produced: four black frames share a sha256 and are four patients
                    L.append(f"| `{_c(row['key'])}` | {_c(', '.join(row['crossings']))} | {_c(it)} | "
                             f"{_c(', '.join(row.get('merged_by') or [])) or 'the name rules alone'} |\n")
        elif k == "3_source_entered_twice":
            if c["shown"]:
                L.append("\n| collection | source A | source B | shared patients | containment | split disagreement |\n"
                         "|---|---|---|---:|---:|---:|\n")
                for r in c["shown"]:
                    L.append(f"| {r['collection']} | {r['source_a']} ({r['n_a']}) | {r['source_b']} ({r['n_b']}) | "
                             f"{r['n_shared']} | {r['containment']} | {r['n_split_disagreement']} |\n")
        elif k == "4_eval_vs_training":
            L.append("\n| model | eval keys | in training | share | refs that did not resolve | evidence |\n"
                     "|---|---:|---|---:|---|---|\n")
            for r in c["models"]:
                # a model whose TRAINING refs did not resolve was not checked at all; printing 0 in that column
                # makes it look identical to a model that was checked and came back clean
                unres = r.get("unresolved_refs") or []
                n_in = "NOT CHECKED" if any(u.startswith("train ") for u in unres) else r["n_eval_keys_in_train"]
                L.append(f"| {r['model']} | {r['n_eval_keys']} | {n_in} | "
                         f"{r['share_of_eval_leaked']} | {_c('; '.join(unres)) or '-'} | "
                         f"{r['evidence'] or 'asserted, no file named'} |\n")
        elif k == "5_render_pose_duplicates":
            for r in c["shown"]:
                L.append(f"- `{r['collection']}` `{r['key']}`: {', '.join(r['crossings'])} -- {r['items']}\n")
        elif k == "6_styled_vs_real_device":
            L.append("\n| styled / pose-borrowing corpus | device | real corpora of that device | pose donors | "
                     "donors in a real held-out split |\n|---|---|---|---:|---:|\n")
            for r in c["all_styled"]:
                L.append(f"| {r['collection']} | {r['device']} | {', '.join(r['real_collections_of_device']) or '-'} | "
                         f"{r['n_pose_donors']} | {r['n_donor_in_real_heldout']} |\n")
        elif k == "alias_gaps":
            for r in c["shown"]:
                L.append(f"- `{r['collection']}`: `{r['a']}` vs `{r['b']}` -- {r['why']} "
                         f"{'**both spellings straddle a split**' if r['both_spellings_straddle_a_split'] else ''} "
                         f"Fix: {r['fix']}\n")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    open(path, "w", encoding="utf-8").write("".join(L))


def write_gen_fragment(rep, gen_dir):
    """The `leak_results` fragment docs/DATA_ACCOUNTING.md splices between its BEGIN/END GENERATED markers.

    WHY THIS IS HERE. The runner (slurm/data_accounting.sh) reads $OUT/generated/<name>.md and, when a fragment is
    missing, writes "NOT GENERATED" into the document. No tool wrote any of them, so the document's results
    section was six permanent NOT GENERATED blocks. This writes the one this tool owns. It is a SHORT fragment on
    purpose: the long report is DATA_LEAKAGE_REPORT.md beside it, and a document section that restates a hundred
    rows is a section nobody reads."""
    v, k = rep["verdict"], rep["keying"]
    d = rep.get("discovery") or {}
    n_read = sum(1 for c in rep["census"].values() if c.get("present") and c.get("n"))
    meaning = {0: "checked, no leak", 1: "LEAK FOUND", 2: "items could not be keyed",
               3: "COULD NOT RUN / incomplete coverage"}.get(v["exit"], "?")
    L = [f"**{'PASS' if v['pass'] else 'FAIL'}** (exit {v['exit']}: {meaning}) -- {rep['n_items']} items over "
         f"{n_read} of {len(rep['census'])} collections, {k['n_unkeyed']} unkeyed, generated {rep['generated']} "
         f"on `{rep['host']}`.\n\n"]
    if v.get("could_not_run"):
        L.append("This run was INCOMPLETE and its verdict covers only what it read: "
                 + "; ".join(v.get("could_not_run_reasons") or []) + ".\n\n")
    L.append("| check | flagged |\n|---|---:|\n")
    for name, c in rep["checks"].items():
        L.append(f"| {name} | {c['n']} |\n")
    if d.get("enabled"):
        L.append(f"\nCollections: {d['n_discovered']} discovered, {d['n_not_in_hand_list']} of them not in the "
                 f"hand list ({d.get('n_hand_list', 0)} entries), {d['n_added']} added to this run, "
                 f"{d['n_unscannable']} unscannable (listed in the full report).\n")
    else:
        L.append(f"\nCollection discovery was OFF ({d.get('why', '?')}): the census is the hand list and says "
                 "nothing about any directory not in it.\n")
    h = rep.get("hash_evidence")
    if h:
        L.append(f"\nByte identity (`--hash`): {h['n_hashed']} files hashed, {h['n_groups']} groups of identical "
                 f"bytes, {h['n_corroborating']} corroborating one patient key, **{h['n_conflicts']} spanning two "
                 f"or more patient keys and therefore NOT merged**.\n")
    p = Path(gen_dir) / "leak_results.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(L), encoding="utf-8")
    return str(p)


# --------------------------------------------------------------------------------------- driver
def lineage_from_graph(path):
    """tools/data_lineage.py writes lineage.json with models[] = {name, bank, bank_node, train, eval, ...}. Its
    node ids live in another namespace, so only the BANK name is carried over, and a bank this run did not scan
    becomes an unresolved ref in check (4) rather than a silent omission. The two tools compute leakage
    independently; where they disagree, one of them is wrong and that is worth knowing."""
    out = {}
    doc = json.load(open(path, encoding="utf-8"))
    for m in doc.get("models", []) or []:
        bank = m.get("bank") or str(m.get("bank_node") or "").split(":")[-1]
        if not m.get("name") or not bank:
            continue
        out[str(m["name"])] = dict(train=[f"{bank}#train"], eval=[f"{bank}#val"],
                                   evidence=f"{path} models[] (bank {bank}, node {m.get('bank_node')})")
    return out


def load_config(a, verbose=True):
    """(collections, lineage, aliases, discovery report, problems).

    Every file named on the command line is opened inside a try: an unparseable --config used to raise out of
    main(), and an uncaught exception leaves Python exiting 1 -- which is this tool's code for LEAKAGE FOUND. A
    file that was named and could not be read is a `problem`, the run cannot PASS with one, and it exits 3
    (could not run), which is a different sentence from "a leak was found"."""
    problems = []

    def load(flag, p):
        if not os.path.exists(p):
            problems.append(dict(flag=flag, path=p, why="named on the command line and not on disk"))
            print(f"{flag} {p}: MISSING", flush=True)
            return None
        try:
            if os.path.getsize(p) == 0:
                problems.append(dict(flag=flag, path=p, why="named on the command line and EMPTY (0 bytes)"))
                return None
            return json.load(open(p, encoding="utf-8"))
        except Exception as e:                               # noqa: BLE001
            problems.append(dict(flag=flag, path=p, why=f"unreadable: {e.__class__.__name__}: {e}"))
            print(f"{flag} {p}: UNREADABLE ({e.__class__.__name__}: {e})", flush=True)
            return None

    collections = {} if a.only_config else dict(DEFAULT_COLLECTIONS)
    lineage = {} if a.only_config else dict(DEFAULT_LINEAGE)
    aliases = []
    for p in a.config or []:
        C = load("--config", p)
        if C is None:
            continue
        if not (C.get("collections") or C.get("lineage") or C.get("aliases")):
            problems.append(dict(flag="--config", path=p,
                                 why="holds no `collections`, `lineage` or `aliases` key: nothing was taken from it"))
        collections.update(C.get("collections", {}))
        lineage.update(C.get("lineage", {}))
        aliases += [list(g) for g in C.get("aliases", [])]
    for p in a.alias_file or []:
        A = load("--alias-file", p)
        if A is None:
            continue
        aliases += [list(g) for g in ((A.get("aliases") or []) if isinstance(A, dict) else A)]
    for p in a.lineage_graph or []:
        if not os.path.exists(p):
            problems.append(dict(flag="--lineage-graph", path=p, why="named on the command line and not on disk"))
            print(f"lineage graph {p}: MISSING", flush=True)
            continue
        try:
            got = lineage_from_graph(p)
        except Exception as e:                               # noqa: BLE001
            problems.append(dict(flag="--lineage-graph", path=p, why=f"unreadable: {e.__class__.__name__}: {e}"))
            continue
        if not got:
            problems.append(dict(flag="--lineage-graph", path=p, why="carries no models[]: no model came from it"))
        lineage.update(got)
    if a.lineage:
        L = load("--lineage", a.lineage)
        if L:
            lineage.update(L)
    # ------------------------------------------------------------------ discovery, before any narrowing
    # --only-config means "use ONLY the config": the operator has named the census on purpose, so discovery is
    # off with it. Everywhere else the hand list is a SUPPLEMENT to what is on disk, not the census.
    disc = dict(enabled=False, why="--no-discover" if getattr(a, "no_discover", False) else
                ("--only-config: the census is the config, by request" if a.only_config else "off"),
                n_discovered=0, n_not_in_hand_list=0, n_added=0, n_unscannable=0, discovered=[], unscannable=[])
    if not a.only_config and not getattr(a, "no_discover", False):
        add, disc = discover_collections(collections, ledger_paths=(a.ledger or []), verbose=verbose)
        for k, v in add.items():
            collections.setdefault(k, v)
    if a.only:
        collections = {k: v for k, v in collections.items() if any(fnmatch.fnmatch(k, o) for o in a.only)}
    for s in a.skip or []:
        collections = {k: v for k, v in collections.items() if not fnmatch.fnmatch(k, s)}
    return collections, lineage, aliases, disc, problems


def read_records(path):
    """A .jsonl (one record per line, as tools/data_ledger.py writes) or a .json holding a list, an {'items': []},
    a {'groups': []} or a flat {path: value} map. Returns a list of dicts."""
    txt = open(path, encoding="utf-8").read().strip()
    if not txt:
        return []
    if txt[0] == "{":                                          # jsonl, including a one-line one
        objs = []
        for ln in (l.strip() for l in txt.splitlines()):
            if not ln:
                continue
            try:
                o = json.loads(ln)
            except json.JSONDecodeError:
                objs = None
                break
            if not isinstance(o, dict):
                objs = None
                break
            objs.append(o)
        # a ONE-line jsonl -- a filtered ledger, `grep deepfluoro canonical.jsonl > one.jsonl` -- used to fall
        # through to the flat-map branch below, which turned the record's FIELD NAMES into paths and so
        # contributed no identity evidence at all, in silence. It is a jsonl record if it looks like one; a
        # one-line {path: sha256} map still is not.
        if objs and (len(objs) > 1 or any(k in objs[0] for k in ("path", "file", "canonical_id", "members"))):
            return objs
    try:
        J = json.loads(txt)
    except json.JSONDecodeError:
        return [json.loads(ln) for ln in txt.splitlines() if ln.strip()]
    if isinstance(J, list):
        return J
    for k in ("items", "groups", "records", "rows"):
        if isinstance(J.get(k), list):
            return J[k]
    return [dict(path=k, **(v if isinstance(v, dict) else dict(sha256=v))) for k, v in J.items() if isinstance(v, (str, dict))]


def expand_inputs(a, verbose=True):
    """--ledger / --canonical / --alias-groups may name a DIRECTORY or a glob, and are expanded in place.

    WHY. tools/data_ledger.py writes `ledger_shard_000_of_016.jsonl` ... there is no single ledger.jsonl, and
    shard membership is sha1(path) % n, so the two copies of one film are in different shards by construction.
    A chain that passed one file, or a path that was never written, got partial evidence or none -- and before
    this, none of that was visible in the report. A glob that matches nothing is a `problem`: it means the stage
    that was supposed to write those files did not."""
    # A directory is expanded by the NAME the writing tool uses, most specific first, and only that: sweeping
    # every .json in a results directory would hand this tool a config file and call it evidence.
    DIRPATS = dict(ledger=("ledger_shard_*.jsonl", "ledger*.jsonl", "*.jsonl"),
                   canonical=("canonical*.jsonl", "*.jsonl"),
                   alias_groups=("alias_groups*.json", "*.json"))
    problems = []
    for flag in ("ledger", "canonical", "alias_groups"):
        vals = getattr(a, flag, None)
        if not vals:
            continue
        out = []
        for p in vals:
            if os.path.isdir(p):
                got = []
                for pat in DIRPATS[flag]:
                    got = sorted(glob.glob(os.path.join(p, pat)))
                    if got:
                        break
                if not got:
                    problems.append(dict(flag=f"--{flag.replace('_', '-')}", path=p,
                                         why=f"is a directory holding none of {', '.join(DIRPATS[flag])}"))
                out += got
            elif any(c in p for c in "*?["):
                got = sorted(glob.glob(p))
                if not got:
                    problems.append(dict(flag=f"--{flag.replace('_', '-')}", path=p, why="glob matched no file"))
                out += got
            else:
                out.append(p)
        if verbose and out != vals:
            print(f"--{flag.replace('_', '-')}: {len(vals)} argument(s) expanded to {len(out)} file(s)", flush=True)
        setattr(a, flag, out)
    return problems


def identity_path_groups(a, verbose=True):
    """Groups of file PATHS that the inventory layer says are one thing. Consumes, in this order of trust:
      --canonical     tools/data_alias.py canonical.jsonl  (path -> canonical_id, decided by content)
      --alias-groups  tools/data_alias.py alias_groups.json (groups[].members = paths, with their evidence)
      --ledger        tools/data_ledger.py ledger.jsonl    (content_key / sha256, and its own patient_key)
    Nothing here is required. But a file NAMED on the command line and not usable is a different thing from a
    file nobody asked for: it is returned in `problems`, and a run carrying any of those cannot PASS. An operator
    who wrote `--ledger $OUT/ledger.jsonl` against a path the ledger stage never wrote was, before this, told
    nothing and given a clean sheet computed without the evidence they asked for."""
    groups, notes, problems = [], [], []

    def usable(flag, p):
        """(records, None) or (None, problem). The existence check comes FIRST: read_records() opens the file, so
        an absent --ledger/--canonical used to raise FileNotFoundError and exit 1 -- this tool's code for
        "leakage found"."""
        if not os.path.exists(p):
            return None, dict(flag=flag, path=p, why="named on the command line and not on disk")
        try:
            if os.path.getsize(p) == 0:
                return None, dict(flag=flag, path=p, why="named on the command line and EMPTY (0 bytes)")
            recs = read_records(p)
        except Exception as e:                               # noqa: BLE001
            return None, dict(flag=flag, path=p, why=f"unreadable: {e.__class__.__name__}: {e}")
        if not recs:
            return None, dict(flag=flag, path=p, why="parsed to zero records")
        return recs, None

    # Accumulated ACROSS files, not per file. The ledger is written as sixteen shards and shard membership is
    # sha1(path) % n, so the two copies of one film are in different shards by construction -- grouping inside
    # each file would have missed exactly the pair this tool exists to find.
    by_canon = defaultdict(list)
    for p in a.canonical or []:
        recs, prob = usable("--canonical", p)
        if prob:
            problems.append(prob); notes.append(f"{p}: {prob['why']} -- no identity evidence from it"); continue
        n = 0
        for r in recs:
            if r.get("path") and r.get("canonical_id"):
                by_canon[r["canonical_id"]].append(r["path"]); n += 1
        notes.append(f"{p}: {n} rows with a canonical id")
        if not n:
            problems.append(dict(flag="--canonical", path=p,
                                 why=f"{len(recs)} records, none carrying both `path` and `canonical_id`"))
    groups += [("canonical_id", v) for v in by_canon.values() if len(v) > 1]
    if by_canon:
        notes.append(f"--canonical: {sum(1 for v in by_canon.values() if len(v) > 1)} multi-file canonical ids "
                     f"over {len(a.canonical or [])} file(s)")
    for p in a.alias_groups or []:
        recs, prob = usable("--alias-groups", p)
        if prob:
            problems.append(prob); notes.append(f"{p}: {prob['why']}"); continue
        n = 0
        for g in recs:
            mem = g.get("members") or g.get("paths") or []
            if len(mem) > 1:
                groups.append((f"alias_groups.json:{g.get('evidence') or g.get('canonical_id', '?')}", mem)); n += 1
        notes.append(f"{p}: {n} groups")
    by_content, by_patient = defaultdict(list), defaultdict(list)
    for p in a.ledger or []:
        recs, prob = usable("--ledger", p)
        if prob:
            problems.append(prob); notes.append(f"{p}: {prob['why']}"); continue
        n = 0
        for r in recs:
            path = r.get("path") or r.get("file")
            if not path:
                continue
            n += 1
            ck = r.get("content_key") or r.get("pix_sha256") or r.get("vol_sha256") or r.get("sha256") or r.get("checksum")
            if ck:
                by_content[ck].append(path)
            if r.get("patient_key"):
                by_patient[r["patient_key"]].append(path)
        notes.append(f"{p}: {n} rows")
        if not n:
            problems.append(dict(flag="--ledger", path=p,
                                 why=f"{len(recs)} records, none carrying a `path`: this is not a ledger"))
    groups += [("ledger content_key", v) for v in by_content.values() if len(v) > 1]
    groups += [("ledger patient_key", v) for v in by_patient.values() if len(v) > 1]
    if by_content or by_patient:
        notes.append(f"--ledger: {sum(1 for v in by_content.values() if len(v) > 1)} shared content keys, "
                     f"{sum(1 for v in by_patient.values() if len(v) > 1)} shared patient keys, over "
                     f"{len(a.ledger or [])} shard file(s)")
    if verbose:
        for n in notes:
            print("identity:", n, flush=True)
    return groups, notes, problems


def hash_items(items, cap_bytes, verbose=True):
    """sha256 of every scanned file that has one, annotated onto the item. Returns the arithmetic of the pass.

    Every file that was NOT hashed is counted and named by reason. "not hashed" and "hashed and unique" are
    different states, and a report that shows only the second lets a reader believe a corpus was compared when
    nothing in it was opened. A bank member has no file of its own (`<rung.npz>#case`) and is counted apart."""
    n = big = members = absent = failed = 0
    for it in items:
        p = it.get("path")
        if p and "#" in str(p):
            members += 1
            continue
        if not p or not os.path.isfile(p):
            absent += 1
            continue
        try:
            sz = os.path.getsize(p)
            if sz > cap_bytes:
                big += 1
                it["sha256_skipped"] = f"{sz} bytes, over --hash-max-bytes {cap_bytes}"
                continue
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for b in iter(lambda: fh.read(1 << 20), b""):
                    h.update(b)
            it["sha256"], it["bytes"] = h.hexdigest(), sz
            n += 1
        except OSError as e:                                 # noqa: PERF203
            failed += 1
            it["sha256_skipped"] = f"{e.__class__.__name__}: {e}"
            continue
    stats = dict(n_hashed=n, n_over_cap=big, n_container_members=members, n_no_file_on_disk=absent, n_failed=failed,
                 cap_bytes=cap_bytes)
    if verbose:
        print(f"hashed {n} files ({big} over the size cap, {members} container members, {absent} with no file on "
              f"disk, {failed} unreadable)", flush=True)
    return stats


def _declared_gap_between(k1, k2, gaps=ALIAS_GAPS):
    """Is this pair of keys a declared, unresolvable naming gap? Then byte identity is the evidence that gap asks
    for -- and still not a licence for this tool to merge them (ALIAS_GAPS says: confirm, then add --alias-file)."""
    for g in gaps:
        ra, rb = re.compile(g["a"]), re.compile(g["b"])
        if (ra.match(k1) and rb.match(k2)) or (ra.match(k2) and rb.match(k1)):
            return g["why"]
    return None


def hash_evidence(items, cap=50):
    """What byte identity is ALLOWED to say. It is evidence, and it is not identity.

    THE DEFECT THIS REPLACES. `--hash` used to group the files it hashed by sha256 and feed those groups into the
    key merge, so every patient key in a group was fused. Byte identity arrives for reasons that have nothing to
    do with a person -- an empty placeholder PNG, a solid-black frame, one calibration image copied into four
    corpora -- and the fusion then produced a train/val crossing between two people who share nothing but a
    degenerate file. A manufactured leak is as wrong as a missed one, and it is more expensive: somebody rebuilds
    a bank over it.

    THE RULE NOW. A group whose files all carry ONE patient key corroborates the name rules. A group spanning TWO
    OR MORE patient keys is a CONFLICT: reported with both keys, the paths, the collections, the splits and the
    file size, counted, and excluded from the merge. A hash never creates a key and never joins two of them. A
    group holding a keyed and an unkeyed file is a HINT -- the name the rules could not read is byte-identical to
    one they could -- and it is printed for a human to turn into a rule, not applied."""
    by = defaultdict(list)
    for it in items:
        if it.get("sha256"):
            by[it["sha256"]].append(it)
    conflicts, hints, corroborating, n_groups = [], [], 0, 0
    for s, g in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(g) < 2:
            continue
        n_groups += 1
        keys = sorted({i["key"] for i in g if i.get("key")})
        unkeyed = sorted({i["item"] for i in g if not i.get("key")})
        size = g[0].get("bytes")
        why_equal = ("every file in this group is EMPTY (0 bytes): byte identity here is the absence of content, "
                     "not a shared subject" if size == 0 else
                     f"{len(g)} files of {size} bytes are byte-identical")
        if len(keys) <= 1:
            corroborating += 1
            if keys and unkeyed:
                hints.append(dict(sha256=s[:16], key=keys[0], n_files=len(g), size_bytes=size,
                                  unkeyed_items=unkeyed[:6],
                                  paths=[str(i["path"]) for i in g][:6],
                                  note="byte-identical to a file the rules could key. Add a rule (or an "
                                       "--alias-file entry); this tool does not key on bytes."))
            continue
        gap = None
        for i, k1 in enumerate(keys):
            for k2 in keys[i + 1:]:
                gap = gap or _declared_gap_between(k1, k2)
        conflicts.append(dict(sha256=s[:16], n_files=len(g), n_keys=len(keys), size_bytes=size, keys=keys[:10],
                              collections=sorted({i["collection"] for i in g})[:10],
                              splits=sorted({i.get("split") or "?" for i in g}),
                              paths=[str(i["path"]) for i in g][:6],
                              why_equal=why_equal, declared_gap=gap,
                              note=("this pair of keys is a DECLARED alias gap: the bytes are the confirmation it "
                                    "asks for. Add the pair with --alias-file to act on it." if gap else
                                    "two or more patient keys share these bytes. NOT merged: merging would "
                                    "manufacture a crossing between them.")))
    return dict(n_groups=n_groups, n_corroborating=corroborating, n_conflicts=len(conflicts),
                n_merges=0, n_hints=len(hints), conflicts=conflicts[:cap], hints=hints[:cap],
                note="byte identity is evidence here, never identity: a group spanning two patient keys is "
                     "reported as a conflict and excluded from the merge, because a false merge manufactures "
                     "leakage as convincingly as a missed one hides it.")


def run(a):
    pre = expand_inputs(a, verbose=not a.quiet)              # before load_config: discovery reads a.ledger
    collections, lineage, cfg_aliases, disc, problems = load_config(a, verbose=not a.quiet)
    problems = pre + problems
    items, census = scan(collections, verbose=not a.quiet)
    groups, alias_note = load_data_alias()
    groups = groups + cfg_aliases
    path_groups, id_notes, id_problems = identity_path_groups(a, verbose=not a.quiet)
    problems += id_problems
    # --hash no longer feeds the merge. Byte identity is read as evidence AFTER the keys are settled: see
    # hash_evidence() for the manufactured crossings that the old fusion produced.
    hash_stats, hash_rep = None, None
    if a.hash:
        hash_stats = hash_items(items, a.hash_max_bytes, verbose=not a.quiet)
    _, merge_note = merge_keys(items, groups, path_groups, a.max_merge_span)
    if a.hash:
        hash_rep = hash_evidence(items, a.cap)
        hash_rep.update(hash_stats)
        if not a.quiet:
            print(f"hash evidence: {hash_rep['n_groups']} groups of byte-identical files, "
                  f"{hash_rep['n_corroborating']} corroborating one patient key, {hash_rep['n_conflicts']} "
                  f"spanning two or more keys (reported, NOT merged), {hash_rep['n_hints']} hints for unkeyed "
                  f"items", flush=True)

    unkeyed = [dict(collection=i["collection"], item=i["item"], why=i["unkeyed"]) for i in items if i.get("unkeyed")]
    conflicts = [dict(collection=i["collection"], item=i["item"], conflict=i["corpus_conflict"])
                 for i in items if i.get("corpus_conflict")]
    rep = dict(generated=time.strftime("%Y-%m-%d %H:%M:%S"), host=os.uname().nodename if hasattr(os, "uname") else os.environ.get("COMPUTERNAME", "?"),
               argv=sys.argv[1:], n_items=len(items), census=census, discovery=disc, input_problems=problems,
               hash_evidence=hash_rep,
               keying=dict(n_unkeyed=len(unkeyed), unkeyed=unkeyed[:a.cap], n_corpus_conflicts=len(conflicts),
                           corpus_conflicts=conflicts[:a.cap], alias_note=alias_note, identity_files=id_notes,
                           alias_corpora=ALIAS_CORPORA, rules=[r["name"] for r in RULES],
                           rules_used=dict(Counter(i.get("rule") for i in items if i.get("rule")).most_common()),
                           n_unkeyed_in_discovered=sum(1 for i in items if i.get("unkeyed") and i.get("discovered")),
                           n_with_checksum=sum(1 for i in items if i.get("sha256")), **merge_note),
               checks={})
    rep["checks"]["1_within_collection_builder_key"] = check_1_local(items, a.cap)
    rep["checks"]["2_within_collection_merged_key"] = check_2_merged(items, a.cap)
    rep["checks"]["3_source_entered_twice"] = check_3_double_source(items, a.cap, a.dup_source_frac, a.dup_source_min)
    rep["checks"]["4_eval_vs_training"] = check_4_lineage(items, lineage, a.cap)
    rep["checks"]["5_render_pose_duplicates"] = check_5_pose_duplicates(items, a.cap)
    rep["checks"]["6_styled_vs_real_device"] = check_6_styled_vs_real(items, lineage, a.cap)
    rep["checks"]["alias_gaps"] = check_alias_gaps(items, a.cap)
    # CHK-9 runs over the QUOTED results, not the banks: it needs the three files the evaluation gate reads. A SEEN row
    # fails the run as a leak (exit 1); an UNRESOLVED or unkeyed row fails it as not established (exit 3).
    chk9_unestablished = 0
    if getattr(a, "quoted_results", None):
        res9, p9 = run_chk9(a.quoted_results, a.touched, a.eval_sets, getattr(a, "declared", None), a.cap)
        if p9:
            problems += p9
        else:
            rep["checks"]["9_eval_vs_selection_lineage"] = res9
            chk9_unestablished = res9["n_unresolved"] + res9["n_no_eval_keys"]
            if not a.quiet:
                print(f"CHK-9: {res9['n_seen']} seen, {res9['n_unresolved']} unresolved, {res9['n_no_eval_keys']} "
                      f"without eval keys, {res9['n_held_out']} held out, {res9['n_declared']} declared, "
                      f"{res9['n_not_applicable']} n/a (of {res9['n_rows']} quoted rows)", flush=True)

    failing = [k for k, v in rep["checks"].items() if v["n"] and k != "1_within_collection_builder_key"]
    if a.fail_on_builder_key and rep["checks"]["1_within_collection_builder_key"]["n"]:
        failing.append("1_within_collection_builder_key")
    unkeyed_fail = bool(unkeyed) and not a.allow_unkeyed
    # A collection that is not on this host was NOT checked, and a clean report over nothing is the most
    # dangerous output this tool could produce -- it is the shape of every defect this project has had. So a
    # missing collection is a failure of its own until somebody says it is expected.
    missing = sorted(k for k, v in census.items() if not v.get("present"))
    # a path that IS there and yielded nothing was not checked either, and used to leave no trace at all
    empty = sorted(k for k, v in census.items() if v.get("present") and not v.get("n"))
    # a lineage ref naming a collection this run never scanned is a missing collection wearing another name: the
    # model's row in check (4) then reads "0 evaluation keys in training" over a training set nobody read
    unresolved_refs = sorted({r for m in rep["checks"]["4_eval_vs_training"]["models"]
                              for r in m.get("unresolved_refs") or []})
    # a collection whose items carry no split was not checked for disjointness either -- a render directory has no
    # split by design, a bank without one is a bank whose own record of what it trained on is gone
    unsplit = sorted(k for k, v in census.items() if v.get("present") and set(v.get("splits") or {}) <= {"?", ""})
    # --only / --skip is the operator saying "I am narrowing this run on purpose", so an unresolved lineage ref
    # is expected there. An unnarrowed run that claims full coverage and cannot resolve a model's TRAINING set
    # has checked that model against nothing, and says so with an exit code.
    narrowed = bool(a.only or a.skip)
    # a DISCOVERED directory whose layout no scanner handles was not checked either. It is always reported (that
    # is the whole point of discovery); it fails the run only when asked, because on the real host the tables
    # name CT source trees and pose directories this tool has no scanner for and never claimed to check.
    unscannable = [r for r in (disc.get("unscannable") or [])]
    unscannable_fail = bool(unscannable) and bool(getattr(a, "fail_on_unscannable", False))
    missing_fail = bool(missing or empty or (unresolved_refs and not narrowed)) and not a.allow_missing
    # --allow-missing says "this host holds part of the data". It cannot say "this host holds none of it": a
    # report computed over zero items is the worst output this tool has, and no flag may buy it a PASS.
    read_nothing = not items
    # An input NAMED on the command line that is missing, empty or unparseable is not the same as one nobody
    # asked for: the run was told to use evidence it did not use, so it cannot report a clean sheet. No flag
    # excuses it -- the fix is to correct the command line, which is the defect this catches.
    input_fail = bool(problems)
    could_not_run_reasons = ([f"{p['flag']} {p['path']}: {p['why']}" for p in problems]
                             + (["nothing was read at all"] if read_nothing else [])
                             + ([f"collections absent from this host: {', '.join(missing)}"] if missing else [])
                             + ([f"collections present and empty: {', '.join(empty)}"] if empty else [])
                             + ([f"lineage refs naming unscanned collections: {', '.join(unresolved_refs)}"]
                                if unresolved_refs and not narrowed else [])
                             + ([f"{len(unscannable)} discovered directories no scanner here can read"]
                                if unscannable else [])
                             + ([f"CHK-9: {chk9_unestablished} quoted rows whose lineage or evaluation keys are not "
                                 "established (unknown is not clean)"] if chk9_unestablished else []))
    could_not_run = bool(read_nothing or input_fail or missing_fail or unscannable_fail or chk9_unestablished)
    ok = not failing and not unkeyed_fail and not could_not_run
    rep["verdict"] = dict(**{"pass": ok}, failed=failing,
                          unkeyed_fails=unkeyed_fail, missing_collections=missing, n_items=len(items),
                          empty_collections=empty, unresolved_lineage_refs=unresolved_refs,
                          collections_without_splits=unsplit,
                          unscannable_discovered=[r.get("path") or r.get("name") for r in unscannable][:50],
                          n_unscannable_discovered=len(unscannable), unscannable_fails=unscannable_fail,
                          missing_fails=missing_fail, read_nothing=read_nothing, input_fails=input_fail,
                          # `could_not_run` is carried SEPARATELY from the exit code on purpose: exit 1 (leak
                          # found) wins over exit 3 when both apply, and a reviewer has to be able to see that
                          # the run which found the leak was also incomplete.
                          could_not_run=could_not_run, could_not_run_reasons=could_not_run_reasons,
                          exit=1 if failing else (2 if unkeyed_fail else (3 if could_not_run else 0)))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    json.dump(rep, open(out / "leak_report.json", "w"), indent=1, default=str)
    if a.inventory:
        json.dump(items, open(out / "leak_inventory.json", "w"), indent=1, default=str)
    md = a.md or str(out / "DATA_LEAKAGE_REPORT.md")
    write_md(rep, md)
    gen = write_gen_fragment(rep, getattr(a, "gen_dir", None) or str(out / "generated"))
    for k, v in rep["checks"].items():
        print(f"  {k}: {v['n']}", flush=True)
    print(f"wrote {out / 'leak_report.json'}, {md} and {gen}")
    why = ",".join(failing) or ("unkeyed_items" if unkeyed_fail else
                                (";".join(could_not_run_reasons)[:200] if could_not_run else "-"))
    ex = rep["verdict"]["exit"]
    meaning = {0: "checked, no leak", 1: "LEAK FOUND", 2: "items could not be keyed",
               3: "COULD NOT RUN / incomplete coverage"}[ex]
    print(f"LEAK_CHECK {'PASS' if rep['verdict']['pass'] else 'FAIL'}  items {len(items)}  unkeyed {len(unkeyed)}  "
          f"missing_collections {len(missing)}  empty_collections {len(empty)}  "
          f"unresolved_lineage_refs {len(unresolved_refs)}  failed {why}")
    # the two failures a reviewer must never confuse, printed as two separate facts
    print(f"LEAK_CHECK_EXIT {ex} ({meaning})  leak_found={'yes' if failing else 'no'}  "
          f"could_not_run={'yes' if could_not_run else 'no'}"
          + (f"  [{'; '.join(could_not_run_reasons)[:300]}]" if could_not_run else ""))
    return ex


def cmd_scan(a):
    pre = expand_inputs(a, verbose=not a.quiet)
    collections, _, _, disc, problems = load_config(a, verbose=not a.quiet)
    problems = pre + problems
    items, census = scan(collections, verbose=not a.quiet)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(generated=time.strftime("%Y-%m-%d %H:%M:%S"), census=census, discovery=disc,
                   input_problems=problems, items=items),
              open(out / "leak_inventory.json", "w"), indent=1, default=str)
    n_un = sum(1 for i in items if i.get("unkeyed"))
    print(f"wrote {out / 'leak_inventory.json'}: {len(items)} items, {n_un} unkeyed, "
          f"{disc.get('n_discovered', 0)} collections discovered ({disc.get('n_not_in_hand_list', 0)} of them not "
          f"in the hand list), {len(problems)} unusable inputs")
    # an inventory of nothing is not an inventory: `scan` used to return 0 over zero items, which reads as a
    # clean survey of a host that in fact yielded not one file
    if not items:
        print("SCAN COULD NOT RUN: zero items. Nothing here is a survey of anything.")
        return 3
    if problems:
        print(f"SCAN COULD NOT RUN: {len(problems)} input(s) named on the command line were not usable.")
        return 3
    return 2 if (n_un and not a.allow_unkeyed) else 0


def cmd_keys(a):
    bad = 0
    if not a.id:
        print("keys: no --id given, so nothing was resolved. This is not a pass.")
        return 3
    for ident in a.id:
        k, why = key_for(ident, a.corpus)
        if k:
            print(f"{ident:<40} -> {k['corpus']}:{k['patient']:<16} rule {k['rule']}"
                  + (f"  pose {k['pose']}" if k.get("pose") else "") + (f"  device {k['device']}" if k.get("device") else ""))
        else:
            print(f"{ident:<40} -> UNKEYED ({why})")
            bad += 1
    return 2 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["check", "scan", "keys", "chk9"])
    ap.add_argument("--quoted-results", default=None,
                    help="CHK-9: SchwingNet/results/eval_gate/quoted_results.json (every quoted number, its checkpoints and "
                         "evaluation sets). `check` runs CHK-9 only when this is given; `chk9` runs it alone")
    ap.add_argument("--touched", default=None, help="CHK-9: touched.json from tools/checkpoint_lineage.py")
    ap.add_argument("--eval-sets", default=None, help="CHK-9: eval_sets.json from tools/eval_gate.py eval-sets")
    ap.add_argument("--declared", default=None,
                    help="CHK-9: JSON {row id: reason} for quoted rows declared NOT held out; such a row is DECLARED, "
                         "not failed, and its reason is printed")
    ap.add_argument("--out", default=str(REPO / "docs" / "leak"), help="directory for leak_report.json")
    ap.add_argument("--md", default=None, help="the generated Markdown report (default <out>/DATA_LEAKAGE_REPORT.md)")
    ap.add_argument("--config", action="append", help="JSON with collections / lineage / aliases; repeatable")
    ap.add_argument("--only-config", action="store_true", help="use ONLY the config, not the built-in tables")
    ap.add_argument("--lineage", help="JSON replacing/extending the model lineage table")
    ap.add_argument("--lineage-graph", action="append",
                    help="lineage.json from tools/data_lineage.py; its models[] become model entries here")
    ap.add_argument("--alias-file", action="append", help="JSON list of alias groups (lists of corpus:patient keys)")
    ap.add_argument("--canonical", action="append", help="canonical.jsonl from tools/data_alias.py (path -> canonical_id)")
    ap.add_argument("--alias-groups", action="append", help="alias_groups.json from tools/data_alias.py")
    ap.add_argument("--ledger", action="append",
                    help="ledger shards from tools/data_ledger.py (content_key / patient_key). A FILE, a GLOB or "
                         "the DIRECTORY holding ledger_shard_*.jsonl -- the ledger is sharded and one shard is "
                         "a sixteenth of the evidence; repeatable")
    ap.add_argument("--max-merge-span", type=int, default=8,
                    help="a single identity token spanning more than this many patient keys is reported, not merged: "
                         "a degenerate content key (every blank frame hashes alike) would manufacture leakage")
    ap.add_argument("--hash", action="store_true",
                    help="compute sha256 for every scanned file and read it as EVIDENCE (run in a job): a group of "
                         "byte-identical files spanning two patient keys is reported as a conflict and is never "
                         "merged -- an empty placeholder or a blank frame is not a shared patient")
    ap.add_argument("--hash-max-bytes", type=int, default=64 << 20)
    ap.add_argument("--no-discover", action="store_true",
                    help="do not enumerate collections from the ledger / root tables / bank globs; use the hand "
                         "list alone, which cannot notice a collection nobody added to it")
    ap.add_argument("--fail-on-unscannable", action="store_true",
                    help="a discovered directory whose layout no scanner here handles fails the run. It is always "
                         "reported; this makes it an exit code")
    ap.add_argument("--gen-dir", default=None,
                    help="where to write leak_results.md, the fragment docs/DATA_ACCOUNTING.md splices between "
                         "its BEGIN/END GENERATED markers (default <out>/generated)")
    ap.add_argument("--only", action="append", help="collection name or glob; repeatable")
    ap.add_argument("--skip", action="append", help="collection name or glob; repeatable")
    ap.add_argument("--cap", type=int, default=50, help="max offending items listed per check (totals are kept)")
    ap.add_argument("--dup-source-frac", type=float, default=0.5)
    ap.add_argument("--dup-source-min", type=int, default=2)
    ap.add_argument("--allow-unkeyed", action="store_true", help="survey mode: unkeyed items do not fail the run")
    ap.add_argument("--allow-missing", action="store_true",
                    help="a declared collection that is absent, empty, or named only by a lineage ref does not fail "
                         "the run. Needed on any host that holds PART of the data. It cannot excuse a host that "
                         "holds none: a run that read zero items exits 3 with or without it")
    ap.add_argument("--fail-on-builder-key", action="store_true", help="also fail on check (1)")
    ap.add_argument("--inventory", action="store_true", help="also write leak_inventory.json from `check`")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--id", action="append", default=[], help="keys: an identity string to resolve")
    ap.add_argument("--corpus", default=None, help="keys: the corpus hint of the collection it came from")
    a = ap.parse_args()
    try:
        if a.cmd == "chk9" and not (a.quoted_results and a.touched and a.eval_sets):
            print("chk9 needs --quoted-results, --touched and --eval-sets; nothing was checked, which is not a pass")
            return 3
        return dict(check=run, scan=cmd_scan, keys=cmd_keys, chk9=cmd_chk9)[a.cmd](a)
    except KeyboardInterrupt:
        print("LEAK_CHECK_EXIT 3 (COULD NOT RUN / incomplete coverage)  interrupted", file=sys.stderr)
        return 3
    except Exception as e:                                   # noqa: BLE001
        # Uncaught, Python exits 1 -- and 1 is this tool's code for LEAKAGE FOUND. A crash would then be read,
        # by a human or by slurm/data_accounting.sh, as a positive finding. It is a run that did not happen: 3.
        import traceback                                     # noqa: PLC0415
        traceback.print_exc()
        print(f"LEAK_CHECK_EXIT 3 (COULD NOT RUN / incomplete coverage)  leak_found=no  "
              f"could_not_run=yes  [{e.__class__.__name__}: {e}]", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
