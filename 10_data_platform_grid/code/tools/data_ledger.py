#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/data_ledger.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""One record per physical imaging file in the project, carrying the keys that make "is this the same picture?"
answerable. The INVENTORY layer of the data accounting; the leakage audit reads these records, it does not build them.

WHY THIS EXISTS. On 2026-09-22 the level banks were found to hold NHANES II twice. ~/films_drr carries the 543
annotated films as source `nhanes` with `patient_id` `nhanes_00160`; ~/nhanes_drr carries the SAME films again as
`NH_00160_c` with no source field; the split is drawn per source, so 48 of 54 validation patients had their other
copy in training (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md). Nothing in the pipeline could say those two files
are one person's film, because nothing held an identity for a file that survives being re-encoded, renamed and
re-rendered. This tool writes that identity down, for every root the project touches, before any audit runs.

FOUR KEYS, BECAUSE THE BYTE HASH ALONE IS NOT ENOUGH.
  sha256        the file's bytes. It catches an exact copy under a second name and nothing else. The same NHANES
                film stored as a 16-bit .tiff and as a uint8 .npy render has two unrelated byte hashes -- which is
                precisely how the double inclusion stayed invisible for months.
  pix_sha256    the DECODED pixels after a fixed normalisation (greyscale, 0.5/99.5-percentile stretch to uint8,
                hashed with the shape). It matches an exact re-container -- PNG against .npy, 16-bit against the
                8-bit export of the same window. MEASURED LIMITS: it does NOT match across a resize, a crop, a
                lossy re-encode, an inverted copy, or TWO DIFFERENT WINDOWINGS of one 16-bit film (windowing
                clips and requantises, and the percentile stretch cannot undo that; dhash bridged that pair at
                Hamming 2 and the pixel key did not bridge it at all).
  dhash         64 bits from an 8x9 BOX downsample of that normalised image (adjacent-column comparisons). It
                survives rescaling, a change of window and lossy re-encoding, so a thumbnail, a rescaled copy
                and a figure reproduction of one film land within a few bits of each other. It does NOT survive
                a CROP or an inversion. Hamming distance is the audit's business; this layer records the bits.
  degenerate    true when the normalised picture is constant. It has to be recorded because a solid-black frame,
                a solid-white frame and a blank .npy of the same shape all normalise to zeros and therefore
                share one pix_sha256 and dhash 0000000000000000. That is an empty frame, not a duplicate, and
                the merge holds those records out of the repeat count.
  vol_sha256    volumes: a fixed 64^3 trilinear downsample, percentile-quantised to int16, hashed together with the
                shape and the rounded spacing. It survives gzip level changes and float32/int16 recompression.

DECLARED ALIASES, because no pixel key relates a container to its unpacking. DeepFluoro ships as one HDF5
(`~/deepfluoro/unpacked_full/ipcai_2020_full_res_data.h5`) and again as vendor DICOMs
(`.../deepfluoro_vendor/unpacked`) -- the same six cadavers and 366 frames, in two packagings whose bytes share
nothing. Treating them as two corpora inflates every count and lets one leak into the other's held-out set. Every
root therefore carries an `alias_group`, and roots that are packagings of one acquisition share it
(deepfluoro_ipcai2020, nhanes_ii, buu_lspine, carmlspine, cobra2026, ...). The declared table is the belt; the
pixel keys are the braces. `patient_key` is normalised ACROSS roots inside an alias group, so `C00160.tiff`,
`NH_00160_c` and `nhanes_00160` all resolve to `nhanes_ii/160` -- the join the bank splits did not have.

NOT KNOWN, AND NOT INVENTED: the CTSpinoPelvic1K render stems (`CTSP_COLONOG_1`) and the release case ids
(`0001_ct.nii.gz`) are two different namings of the same cohort and this layer does not join them; they get
namespaces `ctsp_drr/...` and `ctsp_release/...`. A patient_key joins only within its namespace. Files with no
matching rule get patient_key null rather than a guess.

TRAPS THIS AVOIDS
  * A whole volume is never loaded. Headers give shape/spacing; the content key comes from a strided read
    (`dataobj[::s,::s,::s]`, one decompression pass, no full array held) resampled to 64^3. Volumes whose
    uncompressed size exceeds --max-load-gb are recorded header-only, with a note, never silently skipped.
  * DICOM without a .dcm extension is real (the DeepFluoro vendor `fluoro/*/dicom` trees): an extensionless file
    is sniffed for the "DICM" magic at offset 128.
  * UIDs are recorded but never used to group: every C-ArmLSpine CBCT slice carries its own SeriesInstanceUID
    (tools/carmlspine_io.py, trap 1) and its PixelSpacing is a placeholder. Grouping is by DIRECTORY, and that
    means the root-relative path, not the stem. Three corpora put the subject in the directory and a constant
    in the filename -- TotalSegmentator `s0000/ct.nii.gz`, C-ArmLSpine `case1/CBCT/0060.dcm`, the DeepFluoro
    vendor tree `03_cadaver_17-1882/.../0001` -- so every record carries `rel`, and the patient rules are tried
    against `rel` when the stem yields nothing. `case` is the STEM and collides across subjects in exactly
    those corpora ('ct' for all 1228 TotalSegmentator CTs); never group on it outside a render bank.
  * Shard membership is sha1(path) % n_shards, not enumeration index, so adding a file does not move every other
    file to a different shard and invalidate a half-finished run.
  * Resume truncates a torn last line before appending. A killed job leaves a partial JSON line; parsing around it
    and then appending would corrupt the rest of the file.
  * One file, one record: roots overlap (a corpus_manifold SETS glob can point inside a root already listed), so a
    path is claimed by the first root that yields it and the overlap is counted in the summary, never re-hashed.

STAGES: source | render | crop | styled | detector-set | eval. A record is `physical` unless it names a member
inside a container (`<file.npz>#1234`, `<file.h5>#/dataset`), which is marked `physical: false` and carries the
parent's sha256 -- crop-bank members are enumerated from the bank's small string arrays (case/split/source) only
and never carry a pixel key (--no-bank-members turns the listing off entirely; there is no per-member decode).

WHAT THIS LAYER STILL CANNOT KEY, so that nobody reads a null as an absence of risk. Three patient rules capture
to end of string (aasce, mendeley, ctsp), so their "patient key" is really the filename: `AASCE_sunhl-...-162_A_AP`
and `..._B_AP` are two people to this table, where the NHANES rule correctly joins `NH_00160_c` to `NH_00160_l`.
Raw Mendeley (`3729-F-067Y1.jpg`), raw AASCE (`01-July-2019-1.jpg`), Ljubljana, VinDr, lateral236, SpineSAC and
Geneva have nothing in the name to key on, and SpinalAI (`SPAI_000002`) has neither a rule nor an alias entry,
so its renders and its raw films are two unrelated corpora here. For all of those the pixel key and the dhash
are the ONLY evidence, and neither survives a crop.

HOW TO ADD A ROOT. Easiest: drop it under a family that is already globbed (~/*_drr, ~/*_ctx, ~/*_pseudo,
~/spine-detector/data/raw/*, ~/spine-detector/data/yolo_*, <ceph>/realxray/*, <ceph>/devcorpus/styled/*,
~/FluoroCap/*). Otherwise add one line to STATIC_ROOTS below, or add it to tools/data_manifest.py ROOTS or
tools/corpus_manifold.py SETS -- both tables are imported and anything in them that no root already claims becomes
a root here automatically. Add a patient rule to PATIENT_RULES if its filenames carry a subject id. To try a
directory before it earns a line anywhere: --extra-root "name|stage|path".

    python tools/data_ledger.py roots                                   # what exists, what is missing (stat only)
    python tools/data_ledger.py roots --count                           # + file counts and bytes (walks; use a job)
    python tools/data_ledger.py build --out DIR --shard 3 --n-shards 16 --workers 8
    python tools/data_ledger.py build --out DIR --extra-root "trial|render|~/new_drr" --roots trial
    python tools/data_ledger.py summary --out DIR                       # merge the shard summaries
"""
from __future__ import annotations

import argparse
import fnmatch
import glob as _glob
import hashlib
import json
import os
import re
import socket
import sys
import time
from pathlib import Path

import numpy as np

LEDGER_VERSION = 2                  # v2: the `origin` column + verbatim ann patient_key (PolyPose hook)
H = os.path.expanduser("~")
D = "/rs/rs_grp_oschome/go2432/data"
OUT_DEFAULT = f"{D}/or_ready/data_ledger"

IMG_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".npy"}
VOL_EXT = {".nii", ".nii.gz", ".mha", ".mhd", ".nrrd"}
CONTAINER_EXT = {".h5", ".hdf5"}
DCM_EXT = {".dcm", ".ima", ".dicom"}
BANK_EXT = {".npz"}
RAW_EXT = {".raw", ".rad"}          # Ljubljana ships .raw + .rad; no decoder here, byte identity only

STAGES = ("source", "render", "crop", "styled", "detector-set", "eval", "synthetic")

# THE ORIGIN COLUMN. Every record says where its content ultimately came from: "acquired" (a scanner saw a
# person, or a derivation of that file -- renders, crops and styled copies keep origin "acquired" because their
# anatomy is an acquisition's) versus a GENERATOR name for volumes whose anatomy was synthesised or warped
# ("polypose": tools/polypose_manifest.py). A generated volume enters this census under its SOURCE patient key
# (taken VERBATIM from its ann sidecar, never re-derived by regex -- 'ctsp_release/0244' put through the stem
# rules would come back as a ctsp_drr key and join to nobody), so it sits on the source person's side of every
# split, and the origin column is what keeps it countable as synthetic rather than as a new patient.
ORIGIN_DEFAULT = "acquired"


# --------------------------------------------------------------------------------------------- identity rules
# (regex, namespace/template, strip_leading_zeros). Searched, case-insensitive, first match wins. Applied to the
# ann's patient_id when the ann has one, else to the file stem. Root-scoped rules are tried before these.
#
# NO \b NEXT TO A DIGIT OR A LETTER IN THESE. Every id in this project is glued to its neighbours with an
# underscore, and `_` is a WORD character: `\b` does not exist between `r` and `_`, nor between `2` and `_`.
# So `\b(1[78]-\d{4})\b` never fired on `03_cadaver_17-1882` or on `17-1882_000`, which is how DeepFluoro is
# written everywhere, and `\bcsxa` never fired on `CSXA_csxa_0001035`, which is what a crop bank stores. The
# boundaries below are explicit lookarounds instead: `(?<![a-z0-9])` before, `(?![0-9])` after.
PATIENT_RULES = [
    # films_drr stems the corpus, the view and the id together: NHANES_nhanes_cervical_00160, ann patient_id
    # nhanes_00160. A crop bank keeps only the stem, so the rule has to survive the words in between.
    (r"nhanes(?:[_-][a-z]+)*[_-]0*(\d+)", "nhanes_ii/{0}", True),
    (r"(?<![a-z0-9])NH[_-]0*(\d+)", "nhanes_ii/{0}", True),  # nhanes_drr case          NH_00160_c
    (r"buu[_-]?0*(\d+)", "buu_lspine/{0}", True),           # films_drr / BUU_FULL_buu_0001-F-037Y1
    (r"(?<![a-z0-9])csxa[_-](\d+)", "csxa/{0}", False),     # films_drr case            CSXA_csxa_0001035
    (r"(?<![a-z0-9])mendeley[_-](.+)$", "mendeley_716/{0}", False),
    (r"^aasce[_-](.+)$", "aasce/{0}", False),               # the same AASCE films sit in yolo_v3 and the eval set
    (r"(?<![a-z0-9])case(\d+)(?![0-9])", "carmlspine/case{0}", False),   # C-ArmLSpine case1/CBCT/0060.dcm
    (r"(?<![0-9])(1[78]-\d{4})(?![0-9])", "deepfluoro_ipcai2020/{0}", False),  # 03_cadaver_17-1882, 17-1882_000
    (r"(?<![a-z0-9])TS[_-]?s(\d{4})(?![0-9])", "totalsegmentator/s{0}", False),
    (r"^s(\d{4})$", "totalsegmentator/s{0}", False),
    (r"(?<![a-z0-9])(gl\d{3,4}|sub-verse\d{3,4}|verse\d{3,4})(?![0-9])", "verse/{0}", False),
    (r"^CTSP[_-](.+?)$", "ctsp_drr/{0}", False),            # NOT joined to ctsp_release; see the module docstring
    (r"^([A-G]\d{3})(?![0-9])", "cobra2026/{0}", False),    # COBRA centre-letter case ids
]

# Root name substring -> patient rules for THAT root, tried before the global ones. A raw corpus names its files
# the way its release does, with nothing in the stem to say which corpus it is: NHANES II ships `C00160.tiff`
# (cervical) and `L00160.tiff` (lumbar) of one person, BUU ships `0001-F-037Y1.jpg`. Without these the raw films
# get no patient key at all and never join to the renders made from them -- which is how the duplication survived.
ROOT_PATIENT_RULES = [
    ("nhanes", ((r"^[CL]0*(\d+)", "nhanes_ii/{0}", True),)),
    ("buu", ((r"^0*(\d+)-", "buu_lspine/{0}", True),)),
    ("csxa", ((r"^(\d+)$", "csxa/{0}", False),)),
    # TotalSegmentator names the SUBJECT with the directory and every file inside it `ct.nii.gz`, so the stem
    # carries no identity at all; the second rule reads the subject out of the root-relative PATH.
    ("ts_", ((r"^s(\d{4})$", "totalsegmentator/s{0}", False),
             (r"(?:^|/)(s\d{4})(?:/|$)", "totalsegmentator/{0}", False))),
]


def rules_for_name(name: str):
    low = name.lower()
    for frag, rules in ROOT_PATIENT_RULES:
        if frag in low:
            return rules
    return ()


# Root name substring -> alias group, for the dynamically discovered families. An alias group says "these roots are
# packagings of ONE acquisition set and must never be counted, split or scored as independent corpora".
ALIAS_BY_NAME = [
    ("deepfluoro", "deepfluoro_ipcai2020"), ("carmlspine", "carmlspine"), ("carm_", "carmlspine"),
    ("cobra", "cobra2026"), ("geneva", "geneva_hip"), ("ljubljana", "ljubljana"), ("spinesac", "spinesac"),
    ("nhanes", "nhanes_ii"), ("buu", "buu_lspine"), ("csxa", "csxa"), ("mendeley", "mendeley_716"),
    ("aasce", "aasce"), ("vindr", "vindr_spinexr"), ("lateral", "lateral_236"), ("verse", "verse"),
    ("ts_", "totalsegmentator"), ("ctsp", "ctspinopelvic1k"), ("fluorocap", "fluorocap"),
]
# The film DRR directories mix corpora under one root; the ann's `source` field decides the alias per record.
ALIAS_BY_SOURCE = {"nhanes": "nhanes_ii", "nhanes_drr": "nhanes_ii", "buu_full": "buu_lspine", "buu": "buu_lspine",
                   "csxa": "csxa", "mendeley": "mendeley_716", "aasce": "aasce"}


def alias_for_name(name: str):
    low = name.lower()
    for frag, al in ALIAS_BY_NAME:
        if frag in low:
            return al
    return None


def _root(name, path, stage, corpus, **kw):
    d = dict(name=name, path=path, stage=stage, corpus=corpus,
             domain=kw.pop("domain", None), alias=kw.pop("alias", alias_for_name(name)),
             include=kw.pop("include", None), exclude=tuple(kw.pop("exclude", ())),
             split_from=kw.pop("split_from", None), ann=kw.pop("ann", False),
             patient_rules=tuple(kw.pop("patient_rules", rules_for_name(name))), note=kw.pop("note", None),
             alias_by_source=kw.pop("alias_by_source", None), origin=kw.pop("origin", ORIGIN_DEFAULT))
    if kw:
        raise TypeError(f"_root({name}): unknown keys {sorted(kw)}")
    return d


# ------------------------------------------------------------------------------------------------- root table
STATIC_ROOTS = [
    # ---- CT / CBCT sources
    _root("ctsp_ct", f"{H}/data/CTSpinoPelvic1K/ct", "source", "CTSpinoPelvic1K CT", domain="ct",
          include=("*.nii.gz",), patient_rules=((r"^(\d{4})_ct$", "ctsp_release/{0}", False),)),
    _root("ctsp_labels", f"{H}/data/CTSpinoPelvic1K/labels", "source", "CTSpinoPelvic1K labels", domain="label",
          include=("*.nii.gz",), patient_rules=((r"^(\d{4})", "ctsp_release/{0}", False),),
          note="label volumes; recorded so a render can be traced to the mask it was projected from"),
    _root("verse_unified", f"{H}/VerSeFusion/data/unified", "source", "VerSe (unified masks + CT)", domain="ct"),
    _root("ts_ct", f"{H}/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300", "source",
          "TotalSegmentator v2 CT", domain="ct", include=("*/ct.nii.gz",),
          note="segmentations/ are excluded by the include pattern (117 masks per subject, not images)"),
    _root("deepfluoro_h5", f"{H}/deepfluoro/unpacked_full", "source", "DeepFluoro (IPCAI 2020 HDF5)",
          domain="fluoro", include=("*.h5",),
          note="ONE container holding 6 specimens, 366 frames and their CTs; --expand-h5 lists the datasets"),
    _root("deepfluoro_vendor", f"{D}/deepfluoro_vendor/unpacked", "source", "DeepFluoro vendor DICOMs",
          domain="fluoro", note="THE SAME frames as deepfluoro_h5 in vendor packaging -- alias, never a 2nd corpus"),
    _root("carmlspine_src", f"{D}/carmlspine/unpacked/C-ArmLSpine", "source", "C-ArmLSpine (C-arm + CBCT)",
          domain="fluoro", note="per-slice SeriesInstanceUID and placeholder PixelSpacing; group by directory"),
    _root("cobra2026", f"{D}/cobra2026/cases", "source", "COBRA2026", domain="fluoro"),
    _root("ljubljana", f"{D}/ljubljana", "source", "Ljubljana 2D-3D-GS", domain="film",
          exclude=("2D-3D-GS.zip", "Matlab/*", "Documents/*", "Results/*")),
    _root("geneva_hip_src", f"{D}/realxray_work/geneva_hip", "source", "Geneva hip (Yareta)", domain="fluoro"),
    _root("spinesac", f"{D}/spinesac", "source", "SpineSAC", domain="fluoro"),
    _root("carmlspine_pose", f"{D}/carmlspine/pose", "eval", "C-ArmLSpine registered poses", domain="pose",
          note="not images; recorded because a pose file is an input a render inherits"),
    # ---- render banks that are not caught by the ~/*_drr family
    _root("physics_rare", f"{H}/physics_rare", "render", "physics render (rare anatomy)", domain="render",
          ann=True),
    # Stems here are `s0467_00_18-1109-021.jpg`: TotalSegmentator subject s0467 rendered at DeepFluoro pose
    # 18-1109. The ANATOMY is what leaks, so the root rule takes s0467 and the global deepfluoro rule -- which
    # would otherwise fire first and name this bank after a cadaver it contains no anatomy from -- does not run.
    _root("anchor_none_v2", f"{H}/model_night/anchor_none_v2_17-1882", "render",
          "calibrated Cios Fusion render bank", domain="render", include=("images/*/*.jpg", "images/*/*.png"),
          split_from="parent", patient_rules=((r"^(s\d{4})_", "totalsegmentator/{0}", False),),
          note="TotalSegmentator anatomy at DeepFluoro poses; the pose specimen is in the stem and is NOT the "
               "patient. Any other bank whose stems embed a pose id needs the same root rule."),
    # ---- eval sets that live outside realxray/
    _root("wholespine_eval", f"{D}/or_ready/wholespine/data/eval", "eval", "whole-spine eval sets", domain="film",
          include=("*/images/*/*.png", "*/images/*/*.jpg")),
    # ---- generated volumes (never acquired): each carries an ann sidecar written by
    # `tools/polypose_manifest.py sidecars` whose patient_key IS the source person's ledger key, taken verbatim.
    # A volume here with no sidecar gets patient_key null and shows up in nulls_by_root -- which is the alarm,
    # because the generator writes the sidecar in the same transaction as the volume.
    _root("polypose_bank", f"{D}/polypose", "synthetic", "PolyPose-warped CT variants", domain="ct",
          include=("volumes/*.nii.gz", "drr/*.png"), ann=True, origin="polypose", alias=None,
          note="warped copies of source CTs + their check DRRs; the person is the SOURCE patient (ann "
               "patient_key, verbatim -- `tools/polypose_manifest.py sidecars` writes ann/<stem>.json for every "
               "output), the origin column says 'polypose'; manifest/rows.jsonl in the bank is the audit trail"),
]

# Dynamically discovered families: (glob of the root directory, stage, corpus template, kwargs). A new directory
# that matches a family is picked up with no code change.
FAMILIES = [
    (f"{H}/*_drr", "render", "DRR / physics render bank", dict(domain="render", ann=True)),
    (f"{H}/physics_drr", "render", "physics render bank", dict(domain="render", ann=True)),
    (f"{H}/*_pseudo", "source", "pseudo-labelled film corpus", dict(domain="film")),
    (f"{H}/*_ctx", "crop", "context-crop bank", dict(domain="crop")),
    (f"{H}/spine-detector/data/raw/*", "source", "raw film corpus", dict(domain="film")),
    (f"{H}/spine-detector/data/yolo_*", "detector-set", "detector dataset", dict(domain="mixed",
                                                                                split_from="parent")),
    (f"{D}/realxray/*", "eval", "real-frame export", dict(domain="fluoro", split_from="parent")),
    (f"{D}/devcorpus/styled/*", "styled", "styled render corpus", dict(domain="styled", split_from="parent")),
    (f"{H}/FluoroCap/*", "source", "FluoroCap literature harvest", dict(domain="literature")),
]


def parse_extra_root(s: str):
    """--extra-root "name|stage|path" (or "name|path"). Pipe-separated because a Windows path carries a colon.
    An ad-hoc root, for trying a new directory before it earns a line in STATIC_ROOTS."""
    parts = [x.strip() for x in s.split("|")]
    if len(parts) == 2:
        name, stage, path = parts[0], "source", parts[1]
    elif len(parts) == 3:
        name, stage, path = parts
    else:
        raise SystemExit(f"--extra-root {s!r}: expected name|path or name|stage|path")
    if stage not in STAGES:
        raise SystemExit(f"--extra-root {s!r}: stage must be one of {STAGES}")
    return _root(name, os.path.abspath(os.path.expanduser(path)), stage, f"ad-hoc root: {name}",
                 note="from --extra-root")


def discover_roots(verbose=False, extra=()):
    """STATIC_ROOTS, then --extra-root, then the families, then anything in tools/data_manifest.py ROOTS and
    tools/corpus_manifold.py SETS that no root above already covers. Order fixes which root claims a shared path."""
    roots, seen_paths, seen_names = [], set(), set()

    def add(spec):
        p = os.path.normpath(spec["path"]) if spec.get("path") else None
        if p in seen_paths:
            return
        if p:
            seen_paths.add(p)
        # Names index the spec table the workers read, so two roots may never share one.
        if spec["name"] in seen_names:
            spec = dict(spec, name=f"{spec['name']}__{len(roots)}")
            print(f"  NOTE: two roots wanted the name {spec['name'].rsplit('__', 1)[0]!r}; "
                  f"{spec['path']} is recorded as {spec['name']!r}", flush=True)
        seen_names.add(spec["name"])
        roots.append(spec)

    for s in STATIC_ROOTS:
        add(s)
    for s in extra:
        add(parse_extra_root(s))
    for pat, stage, corpus, kw in FAMILIES:
        for p in sorted(_glob.glob(pat)):
            if not os.path.isdir(p):
                continue
            name = os.path.basename(p.rstrip("/"))
            parent = os.path.basename(os.path.dirname(p.rstrip("/")))
            if parent in ("raw", "styled", "realxray", "FluoroCap"):
                name = f"{parent.lower()}_{name}"        # 'panels' alone says nothing; 'fluorocap_panels' does
            add(_root(name, p, stage, f"{corpus}: {os.path.basename(p)}", **kw))
    # tools/corpus_manifold.py SETS: pattern-only roots, so a corpus added there for Figure 1 appears here too.
    # SPECIFIC BEFORE GENERAL, and this ordering is load-bearing: data_manifest.ROOTS holds whole trees
    # (<ceph>/or_ready, <ceph>/devcorpus, <ceph>/realxray) and several SETS live INSIDE them -- COBRA Varian at
    # or_ready/devices/varian_halcyon/pairs, SpineSAC at or_ready/spinesac/display/raw. Claiming by the coarse
    # root first filed those corpora as nameless project output with domain None and no alias group, which is
    # exactly what the manifold figure would then have recoloured them as.
    def add_sets():
        import corpus_manifold as CM  # noqa: PLC0415
        dom2stage = {"render": "render", "styled": "styled"}
        for name, spec in CM.SETS.items():
            pat = spec.get("glob") or spec.get("rglob") or spec.get("pairs")
            if not pat:
                continue
            if spec.get("rglob"):
                pat, inc = spec["rglob"], None
            elif spec.get("pairs"):
                pat, inc = spec["pairs"], ("pair_*.npz",)
            else:
                base = pat.split("*")[0]                 # the fixed prefix of the glob is the root
                base = base if base.endswith(os.sep) or base.endswith("/") else os.path.dirname(base)
                pat, inc = base.rstrip("/"), (os.path.relpath(spec["glob"], base).replace("\\", "/"),)
            if not os.path.isdir(pat):
                continue
            add(_root("set_" + re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower(), pat,
                      dom2stage.get(spec.get("domain"), "source"), f"corpus_manifold: {name}",
                      domain=spec.get("domain"), include=inc, note="from tools/corpus_manifold.py SETS"))

    def add_manifest():
        import data_manifest as DMAN  # noqa: PLC0415
        for name, meta in DMAN.ROOTS.items():
            if os.path.isdir(meta["path"]):
                add(_root(f"manifest_{name}", meta["path"], "source", meta.get("source", name),
                          note="from tools/data_manifest.py ROOTS"))

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    for label, fn in (("corpus_manifold", add_sets), ("data_manifest", add_manifest)):
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            if verbose:
                print(f"  ({label} not importable: {e})", flush=True)
    return roots


# ------------------------------------------------------------------------------------------------ enumeration
def ext_of(path: str) -> str:
    q = path.lower()
    if q.endswith(".nii.gz"):
        return ".nii.gz"
    return os.path.splitext(q)[1]


def is_dicom_magic(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            f.seek(128)
            return f.read(4) == b"DICM"
    except OSError:
        return False


def classify(path: str, ext: str, sniff: bool = True):
    if ext in IMG_EXT:
        return "image"
    if ext in VOL_EXT:
        return "volume"
    if ext in CONTAINER_EXT:
        return "container"
    if ext in DCM_EXT:
        return "dicom"
    if ext in BANK_EXT:
        return "bank"
    if ext in RAW_EXT:
        return "raw"
    if ext == "" and sniff and is_dicom_magic(path):
        return "dicom"
    return None


def iter_root_files(spec, sniff=True):
    """Deterministic, sorted paths of every imaging file under one root."""
    root = spec["path"]
    if not root or not os.path.isdir(root):
        return
    out = []
    if spec.get("include"):
        for pat in spec["include"]:
            out.extend(sorted(_glob.glob(os.path.join(root, pat), recursive=True)))
    else:
        for dp, dn, fn in os.walk(root):
            dn.sort()
            for f in sorted(fn):
                out.append(os.path.join(dp, f))
    seen = set()
    for p in out:
        if p in seen or not os.path.isfile(p):
            continue
        seen.add(p)
        rel = os.path.relpath(p, root).replace("\\", "/")
        if any(fnmatch.fnmatch(rel, x) for x in spec["exclude"]):
            continue
        k = classify(p, ext_of(p), sniff)
        if k is None:
            continue
        yield p, k


def shard_of(path: str, n: int) -> int:
    return int(hashlib.sha1(path.encode("utf-8", "surrogateescape")).hexdigest()[:8], 16) % n


# ------------------------------------------------------------------------------------------------------- keys
def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def norm_u8(a: np.ndarray) -> np.ndarray:
    """THE fixed normalisation. Greyscale float -> uint8 by the 0.5/99.5 percentiles, so the same picture stored
    8-bit, 16-bit or float, windowed differently, gives the same bytes. Degenerate (flat) images give zeros."""
    a = np.nan_to_num(np.asarray(a, np.float64), nan=0.0, posinf=0.0, neginf=0.0)
    if a.size == 0:
        return np.zeros((0,), np.uint8)
    lo, hi = np.percentile(a, (0.5, 99.5))
    if hi - lo < 1e-9:
        lo, hi = float(a.min()), float(a.max())
    if hi - lo < 1e-9:
        return np.zeros(a.shape, np.uint8)
    return np.clip(np.rint(255.0 * (a - lo) / (hi - lo)), 0, 255).astype(np.uint8)


def pix_key(u8: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(f"pix1|{list(u8.shape)}|".encode())
    h.update(np.ascontiguousarray(u8).tobytes())
    return h.hexdigest()


def dhash64(u8: np.ndarray):
    """64-bit difference hash on an 8x9 BOX downsample: survives rescaling and lossy re-encoding, which the pixel
    hash does not. Returns None for anything that is not a 2-D image."""
    if u8.ndim != 2 or min(u8.shape) < 2:
        return None
    from PIL import Image
    small = np.asarray(Image.fromarray(u8).resize((9, 8), Image.BOX), np.int16)
    bits = (small[:, :-1] > small[:, 1:]).ravel()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return f"{v:016x}"


def decode_gray(path: str, ext: str):
    """2-D float array + a note, or (None, note). RGB collapses to its channel mean; a 3-D .npy that is not RGB is
    kept whole for the pixel key (its dhash is then None)."""
    if ext == ".npy":
        a = np.load(path, allow_pickle=False, mmap_mode="r")
        a = np.asarray(a)
    else:
        from PIL import Image
        im = Image.open(path)
        im.load()
        a = np.asarray(im)
    note = None
    if a.ndim == 3 and a.shape[-1] in (3, 4):
        a = a[..., :3].astype(np.float64).mean(-1)
        note = "rgb collapsed to channel mean"
    return a, note


def is_flat(u8: np.ndarray) -> bool:
    """A constant picture. norm_u8 maps EVERY constant image to zeros, so a solid-black frame, a solid-white
    frame and a blank .npy of the same shape all carry one pix_sha256 and dhash 0000000000000000. That is not a
    duplicate, it is an empty frame, and the audit has to be able to drop them before it counts repeats."""
    return bool(u8.size) and int(u8.max()) == int(u8.min())


def image_record(path: str, ext: str, want_dhash=True):
    a, note = decode_gray(path, ext)
    u8 = norm_u8(a)
    rec = {"pix_sha256": pix_key(u8), "decoded_shape": list(a.shape), "decoded_dtype": str(np.asarray(a).dtype)}
    if a.ndim == 2:
        rec["height"], rec["width"] = int(a.shape[0]), int(a.shape[1])
    rec["dhash"] = dhash64(u8) if want_dhash else None
    rec["degenerate"] = is_flat(u8)
    if note:
        rec["note"] = note
    return rec


def _interp_axis(a: np.ndarray, ax: int, n: int) -> np.ndarray:
    m = a.shape[ax]
    if m == n:
        return a
    if m == 1:
        return np.repeat(a, n, axis=ax)
    x = np.linspace(0.0, m - 1.0, n)
    i0 = np.floor(x).astype(int)
    i1 = np.minimum(i0 + 1, m - 1)
    w = (x - i0).astype(np.float32)
    sh = [1, 1, 1]
    sh[ax] = n
    return np.take(a, i0, axis=ax) * (1 - w.reshape(sh)) + np.take(a, i1, axis=ax) * w.reshape(sh)


def tri64(a: np.ndarray, n: int = 64) -> np.ndarray:
    """Separable trilinear resample to n^3. Separable because the axes are independent and this needs no scipy."""
    out = np.asarray(a, np.float32)
    for ax in range(3):
        out = _interp_axis(out, ax, n)
    return out


def volume_content_key(sub: np.ndarray, shape, spacing, n=64) -> str:
    v = tri64(np.nan_to_num(sub, nan=0.0, posinf=0.0, neginf=0.0), n)
    lo, hi = np.percentile(v, (0.5, 99.5))
    if hi - lo < 1e-9:
        lo, hi = float(v.min()), float(v.max())
    q = (np.zeros(v.shape, np.int16) if hi - lo < 1e-9
         else np.clip(np.rint(32767.0 * (v - lo) / (hi - lo)), 0, 32767).astype(np.int16))
    h = hashlib.sha256()
    h.update(f"vol1|{list(map(int, shape))}|{[round(float(s), 4) for s in spacing]}|".encode())
    h.update(np.ascontiguousarray(q).tobytes())
    return h.hexdigest()


def read_mha_header(path: str):
    """MetaImage ships a plain-text header before the data, so shape and spacing cost 2 KB, not a decode."""
    hdr, off = {}, 0
    with open(path, "rb") as f:
        blob = f.read(8192)
    for line in blob.split(b"\n"):
        off += len(line) + 1
        if b"=" not in line:
            break
        k, _, v = line.decode("latin-1", "replace").partition("=")
        hdr[k.strip()] = v.strip()
        if k.strip() == "ElementDataFile":
            break
    return hdr, off


def volume_record(path: str, ext: str, grid: int, max_load_gb: float, cap: int = 128):
    """Shape and spacing from the header; the content key from a strided read resampled to grid^3. A whole volume
    is never materialised: the stride is chosen so the read is at most ~cap^3 voxels."""
    rec = {}
    if ext in (".nii", ".nii.gz"):
        import nibabel as nib
        img = nib.load(path)
        shape = list(map(int, img.shape))
        zooms = [float(z) for z in img.header.get_zooms()]
        rec.update(shape=shape, spacing_mm=[round(z, 5) for z in zooms[:3]],
                   axcodes="".join(nib.aff2axcodes(img.affine)),
                   dtype=str(img.get_data_dtype()))
        nvox = float(np.prod(shape)) * max(1, np.dtype(img.get_data_dtype()).itemsize)
        if nvox / 1e9 > max_load_gb:
            rec["note"] = f"header only: {nvox/1e9:.1f} GB uncompressed exceeds --max-load-gb"
            return rec
        st = [max(1, int(np.floor(s / cap))) for s in shape[:3]]
        sl = tuple(slice(None, None, st[i]) for i in range(3)) + tuple(slice(0, 1) for _ in shape[3:])
        sub = np.asanyarray(img.dataobj[sl])
        while sub.ndim > 3:
            sub = sub[..., 0]
        rec["downsample_shape"] = list(map(int, sub.shape))
        rec["vol_sha256"] = volume_content_key(sub, shape, zooms[:3], grid)
        return rec
    if ext in (".mha", ".mhd"):
        hdr, off = read_mha_header(path)
        dim = [int(x) for x in hdr.get("DimSize", "").split()] or None
        sp = [float(x) for x in (hdr.get("ElementSpacing") or hdr.get("ElementSize") or "").split()] or None
        rec.update(shape=dim, spacing_mm=sp, dtype=hdr.get("ElementType"),
                   compressed=hdr.get("CompressedData", "False").lower() == "true")
        mhtype = {"MET_SHORT": np.int16, "MET_USHORT": np.uint16, "MET_UCHAR": np.uint8, "MET_CHAR": np.int8,
                  "MET_FLOAT": np.float32, "MET_DOUBLE": np.float64, "MET_INT": np.int32, "MET_UINT": np.uint32}
        dt = mhtype.get(rec["dtype"] or "")
        local = (hdr.get("ElementDataFile", "").strip().upper() == "LOCAL")
        if dim and sp and dt is not None and local and not rec["compressed"] and len(dim) == 3:
            want = int(np.prod(dim)) * np.dtype(dt).itemsize
            if want / 1e9 <= max_load_gb:
                mm = np.memmap(path, dtype=dt, mode="r", offset=off, shape=tuple(dim[::-1]))
                st = [max(1, int(np.floor(s / cap))) for s in dim[::-1]]
                sub = np.asarray(mm[::st[0], ::st[1], ::st[2]])
                rec["downsample_shape"] = list(map(int, sub.shape))
                rec["vol_sha256"] = volume_content_key(sub, dim, sp[:3], grid)
                del mm
                return rec
        try:                                    # compressed or non-local: only SimpleITK can read it cheaply
            import SimpleITK as sitk  # noqa: PLC0415
            im = sitk.ReadImage(path)
            arr = sitk.GetArrayFromImage(im)
            while arr.ndim > 3:
                arr = arr[0]
            st = [max(1, int(np.floor(s / cap))) for s in arr.shape]
            rec["vol_sha256"] = volume_content_key(arr[::st[0], ::st[1], ::st[2]], list(im.GetSize()),
                                                   list(im.GetSpacing()), grid)
            rec["shape"] = list(im.GetSize())
            rec["spacing_mm"] = [round(float(s), 5) for s in im.GetSpacing()]
        except Exception as e:  # noqa: BLE001
            rec["note"] = f"no content key (compressed MetaImage, SimpleITK unavailable: {type(e).__name__})"
        return rec
    if ext == ".nrrd":
        try:
            import nrrd  # noqa: PLC0415
            data, hdr = nrrd.read(path)
            rec.update(shape=list(map(int, data.shape)),
                       spacing_mm=[round(float(x), 5) for x in np.diag(np.array(hdr.get("space directions", np.eye(3)), float))[:3]])
            st = [max(1, int(np.floor(s / cap))) for s in data.shape[:3]]
            rec["vol_sha256"] = volume_content_key(data[::st[0], ::st[1], ::st[2]], data.shape, rec["spacing_mm"], grid)
        except Exception as e:  # noqa: BLE001
            rec["note"] = f"no content key (pynrrd unavailable: {type(e).__name__})"
        return rec
    rec["note"] = f"no reader for {ext}"
    return rec


def dicom_record(path: str, want_pixels: bool):
    """Header first (UIDs are recorded, never used to group -- see the module docstring), pixels only if asked."""
    import pydicom
    ds = pydicom.dcmread(path, stop_before_pixels=not want_pixels, force=True)
    g = lambda k: (str(getattr(ds, k)) if getattr(ds, k, None) is not None else None)  # noqa: E731
    sp = getattr(ds, "PixelSpacing", None) or getattr(ds, "ImagerPixelSpacing", None)
    rec = {"modality": g("Modality"), "series_uid": g("SeriesInstanceUID"), "sop_uid": g("SOPInstanceUID"),
           "study_uid": g("StudyInstanceUID"), "instance": g("InstanceNumber"),
           "manufacturer": g("Manufacturer"), "model": g("ManufacturerModelName"),
           "rows": int(getattr(ds, "Rows", 0) or 0), "cols": int(getattr(ds, "Columns", 0) or 0),
           "spacing_mm": [round(float(x), 5) for x in sp] if sp else None}
    if not want_pixels:
        return rec
    a = ds.pixel_array
    if a.ndim == 3 and a.shape[-1] in (3, 4):
        a = a[..., :3].astype(np.float64).mean(-1)
    if a.ndim == 2:
        u8 = norm_u8(a)
        rec["pix_sha256"] = pix_key(u8)
        rec["dhash"] = dhash64(u8)
        rec["degenerate"] = is_flat(u8)
    elif a.ndim == 3:                       # multi-frame cine: one key for the stack, dhash of the middle frame
        u8 = norm_u8(a)
        rec["pix_sha256"] = pix_key(u8)
        rec["frames"] = int(a.shape[0])
        rec["dhash"] = dhash64(norm_u8(a[a.shape[0] // 2]))
        rec["degenerate"] = is_flat(u8)
    return rec


def h5_record(path: str):
    import h5py
    tree = []
    with h5py.File(path, "r") as f:
        f.visititems(lambda n, o: tree.append((n, list(getattr(o, "shape", ()) or ()), str(getattr(o, "dtype", ""))))
                     if isinstance(o, h5py.Dataset) else None)
    tree.sort()
    h = hashlib.sha256()
    for n, s, d in tree:
        h.update(f"{n}|{s}|{d}\n".encode())
    return {"h5_datasets": len(tree), "h5_tree_sha256": h.hexdigest()}, tree


# ------------------------------------------------------------------------------------- identity of one record
def stem_of(path: str) -> str:
    b = os.path.basename(path)
    for e in (".nii.gz", ".tar.gz"):
        if b.lower().endswith(e):
            return b[: -len(e)]
    return os.path.splitext(b)[0]


def patient_key(text: str, rules) -> tuple:
    for pat, tmpl, strip0 in list(rules) + PATIENT_RULES:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            gs = [str(int(g)) if (strip0 and g and g.isdigit()) else g for g in m.groups()]
            return tmpl.format(*gs), pat
    return None, None


_SPLITS_CACHE: dict = {}


def split_from_splits_json(root: str, case: str):
    """realxray and friends keep splits.json as {split: [case, ...]}; cached per root."""
    if root not in _SPLITS_CACHE:
        p = os.path.join(root, "splits.json")
        m = {}
        try:
            j = json.load(open(p))
            for k, v in j.items():
                if isinstance(v, list):
                    for c in v:
                        m[str(c)] = k
        except Exception:  # noqa: BLE001
            m = {}
        _SPLITS_CACHE[root] = m
    m = _SPLITS_CACHE[root]
    if case in m:
        return m[case]
    for c, sp in m.items():                          # frame stems are <case>_<nnn>
        if case.startswith(c + "_"):
            return sp
    return None


def rel_of(root: str, path: str):
    """The root-relative path, forward-slashed. Recorded on every record because for a directory-organised corpus
    the SUBJECT is the directory and the stem is a constant: TotalSegmentator ships `s0000/ct.nii.gz`,
    C-ArmLSpine `case1/CBCT/0060.dcm`, the DeepFluoro vendor tree `03_cadaver_17-1882/.../0001`. `case` alone
    therefore collides across subjects in those corpora and must never be used as their grouping key."""
    try:
        return os.path.relpath(path, root).replace("\\", "/") if root else None
    except ValueError:                       # different drive on Windows
        return None


def identity_of(spec, path: str, kind: str):
    """case / patient_key / split / source, from the ann beside the file, the directory, or the filename."""
    root = spec["path"]
    case = stem_of(path)
    out = {"case": case, "rel": rel_of(root, path), "split": None, "source_field": None, "patient_raw": None,
           "patient_key": None, "patient_rule": None, "alias_group": spec.get("alias"),
           "origin": spec.get("origin") or ORIGIN_DEFAULT}
    ann = None
    if spec.get("ann") or os.path.isdir(os.path.join(root, "ann")):
        ap = os.path.join(root, "ann", case + ".json")
        if os.path.isfile(ap):
            try:
                ann = json.load(open(ap))
            except Exception:  # noqa: BLE001
                ann = None
    if ann:
        out["source_field"] = str(ann.get("source") or "") or None
        out["split"] = ann.get("split") or None
        out["patient_raw"] = str(ann.get("patient_id") or "") or None
        if ann.get("case"):
            out["case"] = str(ann["case"])
        if ann.get("origin"):
            out["origin"] = str(ann["origin"])
        # An ann that states `patient_key` states it in the ledger's OWN namespace and it is taken VERBATIM --
        # this is how a generated volume (origin != acquired) joins to its SOURCE person. Re-deriving it by
        # regex would rename it into whatever namespace the stem happens to resemble (module docstring: a
        # ctsp_release key regexed from a render-like stem joins to nobody). alias_group likewise.
        if ann.get("patient_key"):
            out["patient_key"], out["patient_rule"] = str(ann["patient_key"]), "ann:verbatim"
            if ann.get("alias_group"):
                out["alias_group"] = str(ann["alias_group"])
            elif out["alias_group"] is None:
                out["alias_group"] = out["patient_key"].split("/")[0]
    if spec.get("split_from") == "parent" and out["split"] is None:
        for part in Path(path).parts[::-1]:
            if part in ("train", "val", "test", "valid"):
                out["split"] = "val" if part == "valid" else part
                break
    if out["split"] is None and os.path.isfile(os.path.join(root, "splits.json")):
        out["split"] = split_from_splits_json(root, out["case"])
    if out["patient_rule"] == "ann:verbatim":
        return out                               # the key and alias are stated; only the split was still open
    al = (spec.get("alias_by_source") or ALIAS_BY_SOURCE).get((out["source_field"] or "").lower())
    if al:
        out["alias_group"] = al
    key, rule = patient_key(out["patient_raw"] or out["case"], spec["patient_rules"])
    if key is None and out["patient_raw"] is None and out["rel"] and out["rel"] != os.path.basename(path):
        # The stem said nothing and the file sits in a subdirectory: try the whole relative path. This is the
        # only thing that keys C-ArmLSpine (case1/...), the DeepFluoro vendor DICOMs (03_cadaver_17-1882/...)
        # and the TotalSegmentator CTs (s0000/ct.nii.gz) -- without it the declared deepfluoro alias has no
        # patient-level join and the CT that a keyed render was made from is itself unkeyed.
        key, rule = patient_key(out["rel"], spec["patient_rules"])
    out["patient_key"], out["patient_rule"] = key, rule
    if key and out["alias_group"] is None:
        out["alias_group"] = key.split("/")[0]
    return out


# -------------------------------------------------------------------------------------------------- the job
_CTX: dict = {}


def _init(specs, flags):
    _CTX["specs"] = {s["name"]: s for s in specs}
    _CTX["flags"] = flags


def record_for(path: str, root_name: str, kind: str, spec=None, flags=None) -> dict:
    spec = spec or _CTX["specs"][root_name]
    f = flags or _CTX["flags"]
    t0 = time.time()
    # Every field is declared here, so a record whose stat or decode raised has the SAME schema as one that did
    # not. Filling them only on success made an unreadable file a record with no case, no patient_key and no
    # content_key, which a reader counting nulls cannot distinguish from a file that simply has no identity.
    rec = {"v": LEDGER_VERSION, "path": path, "root": root_name, "corpus": spec["corpus"], "stage": spec["stage"],
           "domain": spec.get("domain"), "kind": kind, "ext": ext_of(path), "physical": True, "error": None,
           "bytes": None, "mtime": None, "sha256": None, "case": None, "rel": None, "split": None,
           "source_field": None, "patient_raw": None, "patient_key": None, "patient_rule": None,
           "alias_group": None, "origin": spec.get("origin") or ORIGIN_DEFAULT,
           "content_key": None, "content_key_kind": None}
    try:
        st = os.stat(path)
        rec["bytes"] = int(st.st_size)
        rec["mtime"] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(st.st_mtime))
        rec["sha256"] = sha256_file(path)
        rec.update(identity_of(spec, path, kind))
        if kind == "image" and not f["no_pixels"]:
            rec.update(image_record(path, rec["ext"]))
        elif kind == "volume":
            rec.update(volume_record(path, rec["ext"], f["grid"], f["max_load_gb"]))
        elif kind == "dicom":
            rec.update(dicom_record(path, f["dicom_pixels"] and not f["no_pixels"]))
        elif kind == "container":
            head, _tree = h5_record(path)
            rec.update(head)
        elif kind == "bank":
            rec.update(bank_head(path))
        elif kind == "raw":
            rec["note"] = "byte identity only (no decoder for this format here)"
        rec["content_key"] = (rec.get("pix_sha256") or rec.get("vol_sha256") or rec.get("h5_tree_sha256")
                              or rec["sha256"])
        rec["content_key_kind"] = ("pix" if rec.get("pix_sha256") else "vol" if rec.get("vol_sha256")
                                   else "h5tree" if rec.get("h5_tree_sha256") else "bytes")
    except Exception as e:  # noqa: BLE001
        rec["error"] = f"{type(e).__name__}: {e}"
        # A decode that raised must not throw the BYTE key away too: two truncated copies of one file are
        # byte-identical, and without this they carry no content_key and never reach the duplicate count.
        if rec.get("sha256") and not rec.get("content_key"):
            rec["content_key"], rec["content_key_kind"] = rec["sha256"], "bytes"
    rec["seconds"] = round(time.time() - t0, 3)
    return rec


def bank_head(path: str) -> dict:
    """A crop bank's small string arrays only. X is never touched (it is gigabytes and the audit does not need it)."""
    out = {}
    try:
        z = np.load(path, allow_pickle=False)
        out["bank_members"] = int(len(z["case"])) if "case" in z.files else None
        out["bank_arrays"] = sorted(z.files)
    except Exception as e:  # noqa: BLE001
        out["note"] = f"npz head unreadable: {type(e).__name__}"
    return out


def bank_member_records(path: str, parent: dict, spec) -> list:
    """One record per crop-bank member: case / split / source, and NO pixel key. A bank keeps every crop in one
    compressed X array, so keying one member means decompressing all of them (tens of GB); the member joins to its
    render by `case` instead, which is the join a split audit needs anyway. Said here so nobody assumes otherwise."""
    rows = []
    try:
        z = np.load(path, allow_pickle=False)
        keys = [k for k in ("case", "split", "source", "y") if k in z.files]
        if "case" not in keys:
            return rows
        cols = {k: [str(v) for v in z[k]] for k in keys}
        n = len(cols["case"])
        for i in range(n):
            case = cols["case"][i]
            key, rule = patient_key(case, spec["patient_rules"])
            rows.append({"v": LEDGER_VERSION, "path": f"{path}#{i}", "physical": False, "parent_path": path,
                         "parent_sha256": parent.get("sha256"), "root": parent["root"], "corpus": parent["corpus"],
                         "stage": parent["stage"], "domain": parent.get("domain"), "kind": "crop_member",
                         "case": case, "split": cols.get("split", [None] * n)[i],
                         "source_field": cols.get("source", [None] * n)[i], "patient_key": key,
                         "patient_rule": rule,
                         "alias_group": (ALIAS_BY_SOURCE.get(str(cols.get("source", [""] * n)[i]).lower())
                                         or (key.split("/")[0] if key else parent.get("alias_group"))),
                         "content_key": None, "content_key_kind": "none",
                         "note": "crop-bank member; joins to its render by case, no pixel key", "error": None})
    except Exception as e:  # noqa: BLE001
        rows.append({"v": LEDGER_VERSION, "path": f"{path}#members", "physical": False, "parent_path": path,
                     "root": parent["root"], "kind": "crop_member", "error": f"{type(e).__name__}: {e}"})
    return rows


def _job(arg):
    path, root_name, kind = arg
    spec = _CTX["specs"][root_name]
    f = _CTX["flags"]
    rec = record_for(path, root_name, kind, spec, f)
    out = []
    if kind == "bank" and f["bank_members"] and not rec.get("error"):
        out += bank_member_records(path, rec, spec)
    if kind == "container" and f["expand_h5"] and not rec.get("error"):
        out += h5_member_records(path, rec)
    # The PARENT goes last, because load_done resumes on the physical path alone. Parent first, a kill between
    # the parent line and its members left the bank marked done with 3 of its 10 crop members recorded and no
    # error anywhere. Parent last, the same kill simply re-does the bank and cmd_summary drops the repeated
    # member paths -- a silent loss traded for a counted, self-healing repeat.
    out.append(rec)
    return out


def h5_member_records(path: str, parent: dict) -> list:
    """One record per 2-D dataset inside an HDF5 container, with the same pixel key an image file would get -- this
    is what lets the DeepFluoro h5 frames be matched against the vendor DICOMs of the same frames."""
    rows = []
    try:
        import h5py
        with h5py.File(path, "r") as f:
            names = []
            f.visititems(lambda n, o: names.append(n) if isinstance(o, h5py.Dataset) else None)
            for n in sorted(names):
                d = f[n]
                if d.ndim != 2 or min(d.shape) < 64:
                    continue
                u8 = norm_u8(np.asarray(d[...]))
                # The dataset NAME carries the specimen ('17-1882/projections/000/image'); without keying it the
                # h5 packaging and the vendor DICOMs of the same frames share an alias_group and nothing else.
                key, rule = patient_key(n, ())
                rows.append({"v": LEDGER_VERSION, "path": f"{path}#{n}", "physical": False, "parent_path": path,
                             "parent_sha256": parent.get("sha256"), "root": parent["root"],
                             "corpus": parent["corpus"], "stage": parent["stage"], "domain": parent.get("domain"),
                             "kind": "h5_image", "case": n, "rel": n,
                             "patient_key": key, "patient_rule": rule,
                             "alias_group": parent.get("alias_group") or (key.split("/")[0] if key else None),
                             "decoded_shape": list(map(int, d.shape)), "pix_sha256": pix_key(u8),
                             "dhash": dhash64(u8), "degenerate": is_flat(u8),
                             "content_key": pix_key(u8), "content_key_kind": "pix",
                             "error": None})
    except Exception as e:  # noqa: BLE001
        rows.append({"v": LEDGER_VERSION, "path": f"{path}#datasets", "physical": False, "parent_path": path,
                     "root": parent["root"], "kind": "h5_image", "error": f"{type(e).__name__}: {e}"})
    return rows


# ------------------------------------------------------------------------------------------------- resume I/O
def load_done(jsonl: str) -> set:
    """Paths already recorded. Truncates a torn last line first: a killed job leaves half a JSON object and
    appending after it would corrupt every later reader."""
    if not os.path.exists(jsonl):
        return set()
    with open(jsonl, "rb+") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        if size:
            f.seek(max(0, size - 1))
            if f.read(1) != b"\n":
                f.seek(0)
                data = f.read()
                cut = data.rfind(b"\n")
                f.truncate(cut + 1 if cut >= 0 else 0)
                print(f"  resume: truncated a torn last line ({size - (cut + 1)} bytes)", flush=True)
    done = set()
    with open(jsonl, "r", encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if r.get("physical", True):
                done.add(r.get("path"))
    return done


# ----------------------------------------------------------------------------------------------- subcommands
def cmd_roots(a) -> int:
    roots = discover_roots(verbose=True, extra=a.extra_root)
    if a.roots:
        want = {x.strip() for x in a.roots.split(",")}
        roots = [r for r in roots if r["name"] in want]
    print(f"{len(roots)} roots\n")
    print(f"{'root':<34}{'stage':<14}{'alias':<22}{'present':<9}{'files':>9}{'GB':>9}  path")
    tot_f = tot_b = 0
    for r in roots:
        present = bool(r["path"]) and os.path.isdir(r["path"])
        n = b = 0
        if present and a.count:
            for p, _k in iter_root_files(r, sniff=not a.no_sniff):
                n += 1
                try:
                    b += os.path.getsize(p)
                except OSError:
                    pass
            tot_f += n
            tot_b += b
        print(f"{r['name']:<34}{r['stage']:<14}{str(r['alias']):<22}{'yes' if present else 'MISSING':<9}"
              f"{n:>9}{b/1e9:>9.2f}  {r['path']}")
    groups = {}
    for r in roots:
        groups.setdefault(r["alias"], []).append(r["name"])
    print("\nDeclared alias groups (roots that are packagings of ONE acquisition set):")
    for g, names in sorted((g, n) for g, n in groups.items() if g and len(n) > 1):
        print(f"  {g:<24} {', '.join(sorted(names))}")
    if a.count:
        print(f"\ntotal {tot_f} files, {tot_b/1e9:.2f} GB")
    return 0


def cmd_build(a) -> int:
    os.makedirs(a.out, exist_ok=True)
    roots = discover_roots(verbose=True, extra=a.extra_root)
    if a.roots:
        want = {x.strip() for x in a.roots.split(",")}
        roots = [r for r in roots if r["name"] in want]
    flags = {"no_pixels": a.no_pixels, "grid": a.grid, "max_load_gb": a.max_load_gb,
             "dicom_pixels": not a.no_dicom_pixels, "bank_members": not a.no_bank_members,
             "expand_h5": a.expand_h5}
    print(f"ledger v{LEDGER_VERSION} shard {a.shard}/{a.n_shards} on {socket.gethostname()}  "
          f"pixels={not a.no_pixels} dicom_pixels={flags['dicom_pixels']} expand_h5={a.expand_h5}", flush=True)
    for mod in ("PIL", "nibabel", "pydicom", "h5py", "SimpleITK"):
        try:
            __import__(mod)
            ok = "yes"
        except Exception as e:  # noqa: BLE001
            ok = f"NO ({type(e).__name__})"
        print(f"  decoder {mod:<12} {ok}", flush=True)

    # Enumerate EVERY root in every shard (walks are cheap next to hashing) so the "first root claims a shared
    # path" rule is identical in all shards; only the work is split.
    jobs, claimed, overlap = [], set(), {}
    t0 = time.time()
    for r in roots:
        n = 0
        for p, kind in iter_root_files(r, sniff=not a.no_sniff):
            if p in claimed:
                overlap[r["name"]] = overlap.get(r["name"], 0) + 1
                continue
            claimed.add(p)
            n += 1
            if shard_of(p, a.n_shards) == a.shard:
                jobs.append((p, r["name"], kind))
        print(f"  {r['name']:<34} {n:>8} files"
              + (f"   ({overlap[r['name']]} already claimed by an earlier root)" if r["name"] in overlap else ""),
              flush=True)
    print(f"{len(claimed)} files enumerated in {time.time()-t0:.0f} s; {len(jobs)} in this shard", flush=True)

    jsonl = os.path.join(a.out, f"ledger_shard_{a.shard:03d}_of_{a.n_shards:03d}.jsonl")
    done = set() if a.force else load_done(jsonl)
    if done:
        print(f"  resume: {len(done)} paths already recorded", flush=True)
    jobs = [j for j in jobs if j[0] not in done]
    # AFTER the resume filter, not before: sliced first, a second `--limit N` re-selects the same N paths,
    # finds them all done and hashes nothing, so the flag could never walk a root a slice at a time.
    if a.limit:
        jobs = jobs[: a.limit]
        print(f"  --limit: {len(jobs)} jobs", flush=True)
    print(f"{len(jobs)} files to hash", flush=True)

    from multiprocessing import get_context
    ctx = get_context("fork" if hasattr(os, "fork") else "spawn")
    n_out = n_err = 0
    by_root, bytes_by_root, by_stage, by_kind, by_origin = {}, {}, {}, {}, {}
    t0 = time.time()
    with open(jsonl, "a", encoding="utf-8") as fh:
        def emit(rows):
            nonlocal n_out, n_err
            for rec in rows:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_out += 1
                n_err += bool(rec.get("error"))
                if rec.get("physical", True):
                    by_root[rec["root"]] = by_root.get(rec["root"], 0) + 1
                    bytes_by_root[rec["root"]] = bytes_by_root.get(rec["root"], 0) + int(rec.get("bytes") or 0)
                    by_stage[rec.get("stage")] = by_stage.get(rec.get("stage"), 0) + 1
                by_kind[rec.get("kind")] = by_kind.get(rec.get("kind"), 0) + 1
                o = rec.get("origin") or ORIGIN_DEFAULT
                by_origin[o] = by_origin.get(o, 0) + 1

        if a.workers <= 1:
            _init(roots, flags)
            for i, j in enumerate(jobs, 1):
                emit(_job(j))
                if i % a.progress == 0:
                    fh.flush()
                    el = time.time() - t0
                    print(f"  {i}/{len(jobs)} files  {el:.0f} s  {i/max(el,1e-9):.1f} files/s  {n_err} errors",
                          flush=True)
        else:
            with ctx.Pool(a.workers, initializer=_init, initargs=(roots, flags), maxtasksperchild=200) as pool:
                for i, rows in enumerate(pool.imap_unordered(_job, jobs, chunksize=4), 1):
                    emit(rows)
                    if i % a.progress == 0:
                        fh.flush()
                        el = time.time() - t0
                        print(f"  {i}/{len(jobs)} files  {el:.0f} s  {i/max(el,1e-9):.1f} files/s  "
                              f"{n_err} errors", flush=True)
    summary = {"ledger_version": LEDGER_VERSION, "shard": a.shard, "n_shards": a.n_shards,
               "host": socket.gethostname(), "written": time.strftime("%Y-%m-%d %H:%M"),
               "records": n_out, "errors": n_err, "seconds": int(time.time() - t0),
               "files_enumerated_all_shards": len(claimed), "files_this_shard": len(jobs) + len(done),
               "overlap_skipped_by_root": overlap, "records_by_root": by_root, "bytes_by_root": bytes_by_root,
               "records_by_stage": by_stage, "records_by_kind": by_kind, "records_by_origin": by_origin,
               "flags": flags, "jsonl": os.path.basename(jsonl)}
    sp = os.path.join(a.out, f"summary_shard_{a.shard:03d}_of_{a.n_shards:03d}.json")
    json.dump(summary, open(sp, "w"), indent=1)
    print(f"wrote {n_out} records ({n_err} with an error) to {jsonl}\nwrote {sp}", flush=True)
    return 0


def cmd_summary(a) -> int:
    """Merge whatever shards are on disk. Counts only -- the leakage arithmetic is another tool's job.

    WHAT IT COUNTS, AND THE ONE THAT WAS MISSING. A record with no `patient_key` is a file this layer could not
    join to any person: it takes part in no alias group, no cross-source comparison and no leakage check, and a
    root that is 100 % null contributes nothing but its bytes to the accounting. That share was discoverable only
    by reading the JSONL, which nobody does, so a summary could report two million records over thirty roots and
    say nothing about how many of them were anonymous. `nulls_by_root` puts it on the face of the file and in the
    printed table: records, no_patient_key, share, per root, and a loud line for any root at 100 %. The nulls are
    counted over EVERY record of the root, physical files and container members alike, because a bank member with
    no key is exactly the crop that cannot be traced back to a film.

    THREE WAYS A MERGE LIES, all of them silent before they were checked here.
      * Two shard SETS in one --out. The run is resumable and the out dir is fixed, so a second array of a
        different width leaves ledger_shard_*_of_004 beside ledger_shard_*_of_016. Every file is then counted
        twice AND reported as an exact content repeat. Records are deduplicated on `path`, first line wins.
      * A missing shard. Nothing said so: a merge of 11 of 16 tasks printed a clean summary. The shard indices
        present are now checked against the width the filenames declare.
      * Mixed flags. --no-pixels moves content_key from the picture to the bytes, so one shard's keys do not
        compare with another's. The per-shard summaries carry `flags` and they are now compared.
    """
    files = sorted(_glob.glob(os.path.join(a.out, "ledger_shard_*.jsonl")))
    if not files:
        print(f"no shards under {a.out}")
        return 1
    complaints = []
    widths = sorted({int(re.search(r"_of_(\d+)\.jsonl$", f).group(1)) for f in files
                     if re.search(r"_of_(\d+)\.jsonl$", f)})
    if len(widths) > 1:
        complaints.append(f"MIXED SHARD WIDTHS {widths}: {a.out} holds more than one run. Every file that both "
                          f"runs saw is counted once here (deduplicated on path), but move the older set aside.")
    for w in widths:
        have = {int(re.search(r"_shard_(\d+)_of_%03d\.jsonl$" % w, f).group(1)) for f in files
                if re.search(r"_shard_(\d+)_of_%03d\.jsonl$" % w, f)}
        missing = sorted(set(range(w)) - have)
        if missing:
            complaints.append(f"INCOMPLETE: shards {missing} of {w} were never written. This summary is a "
                              f"count of part of the data and cannot support any statement about leakage.")
    flagsets = {}
    for sp in sorted(_glob.glob(os.path.join(a.out, "summary_shard_*.json"))):
        try:
            k = json.dumps(json.load(open(sp)).get("flags"), sort_keys=True)
        except Exception:  # noqa: BLE001
            continue
        flagsets[k] = flagsets.get(k, 0) + 1
    if len(flagsets) > 1:
        complaints.append(f"MIXED FLAGS across shards {list(flagsets)}: content_key does not mean the same "
                          f"thing in every shard, so the duplicate count below is not comparable.")

    n = err = dupe_lines = 0
    by_root, bytes_by_root, by_stage, by_kind, by_alias, by_origin = {}, {}, {}, {}, {}, {}
    all_by_root, null_by_root, null_by_stage = {}, {}, {}
    keys, seen_paths, degenerate = {}, set(), 0
    for f in files:
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            p = r.get("path")
            if p in seen_paths:                 # the same file recorded by two runs: count it once
                dupe_lines += 1
                continue
            seen_paths.add(p)
            n += 1
            err += bool(r.get("error"))
            degenerate += bool(r.get("degenerate"))
            if r.get("physical", True):
                by_root[r.get("root")] = by_root.get(r.get("root"), 0) + 1
                bytes_by_root[r.get("root")] = bytes_by_root.get(r.get("root"), 0) + int(r.get("bytes") or 0)
            # counted over every record, member or not: a crop with no key is exactly the crop that cannot be
            # traced back to a film, and it is the bank members that carry the splits
            all_by_root[r.get("root")] = all_by_root.get(r.get("root"), 0) + 1
            if not r.get("patient_key"):
                null_by_root[r.get("root")] = null_by_root.get(r.get("root"), 0) + 1
                null_by_stage[r.get("stage")] = null_by_stage.get(r.get("stage"), 0) + 1
            by_stage[r.get("stage")] = by_stage.get(r.get("stage"), 0) + 1
            by_kind[r.get("kind")] = by_kind.get(r.get("kind"), 0) + 1
            by_alias[r.get("alias_group")] = by_alias.get(r.get("alias_group"), 0) + 1
            # v1 records predate the column; everything the ledger saw before a generator existed was acquired
            o = r.get("origin") or ORIGIN_DEFAULT
            by_origin[o] = by_origin.get(o, 0) + 1
            ck = r.get("content_key")
            if ck and not r.get("degenerate"):  # a blank frame is not a duplicate of every other blank frame
                keys[ck] = keys.get(ck, 0) + 1
    dup = sum(1 for v in keys.values() if v > 1)
    # The unkeyed share, per root, on the face of the output. A null patient_key is a file that joins to nobody:
    # it cannot be compared across roots, cannot enter an alias group, and cannot be caught leaking. A root at
    # 100 % null is contributing bytes and nothing else, and that has to be readable without opening the JSONL.
    nulls_by_root = {k: dict(records=all_by_root[k], no_patient_key=null_by_root.get(k, 0),
                             share=round(null_by_root.get(k, 0) / max(1, all_by_root[k]), 4))
                     for k in sorted(all_by_root, key=lambda x: (-null_by_root.get(x, 0), str(x)))}
    n_null = sum(null_by_root.values())
    all_null = [k for k, v in nulls_by_root.items() if v["share"] == 1.0 and v["records"]]
    for c in complaints:
        print("!! " + c)
    print(f"{len(files)} shards, {n} records, {err} errors, {dupe_lines} repeated path lines dropped, "
          f"{degenerate} blank/constant frames held out of the duplicate count")
    print(f"{n_null} of {n} records ({n_null / max(1, n):.1%}) carry NO patient key: they join to nobody and take "
          f"part in no leakage check")
    print("\nrecords = physical files; all_rec = every record of the root, container members included")
    print(f"{'root':<34}{'records':>10}{'GB':>10}{'all_rec':>10}{'no_key':>9}{'no_key%':>9}")
    for k in sorted(by_root, key=lambda x: -by_root[x]):
        nb = nulls_by_root.get(k, dict(records=0, no_patient_key=0, share=0.0))
        print(f"{str(k):<34}{by_root[k]:>10}{bytes_by_root.get(k,0)/1e9:>10.2f}"
              f"{nb['records']:>10}{nb['no_patient_key']:>9}{nb['share']:>8.1%}")
    for k in sorted(all_by_root):                    # roots that hold ONLY container members have no by_root row
        if k not in by_root:
            nb = nulls_by_root[k]
            print(f"{str(k):<34}{'-':>10}{'-':>10}{nb['records']:>10}{nb['no_patient_key']:>9}{nb['share']:>8.1%}")
    if all_null:
        print(f"\n!! {len(all_null)} root(s) carry NO patient key at all -- every record in them is anonymous to "
              f"this layer and joins to nothing: {', '.join(str(k) for k in all_null[:12])}"
              + (" ..." if len(all_null) > 12 else ""))
    print("\nrecords with no patient key by stage:", dict(sorted(null_by_stage.items(), key=lambda kv: -kv[1])))
    print("\nby stage:", dict(sorted(by_stage.items(), key=lambda kv: -kv[1])))
    print("by kind :", dict(sorted(by_kind.items(), key=lambda kv: -kv[1])))
    print("by origin:", dict(sorted(by_origin.items(), key=lambda kv: -kv[1])),
          "(non-acquired records are generated volumes counted under their SOURCE patient key)")
    print("by declared alias group:", dict(sorted(by_alias.items(), key=lambda kv: -kv[1])))
    print(f"\ncontent keys: {len(keys)} distinct, {dup} keys held by more than one record "
          f"(EXACT content repeats; the audit layer decides what each one means)")
    out = os.path.join(a.out, "summary.json")
    S = {"shards": len(files), "records": n, "errors": err, "records_by_root": by_root,
         "bytes_by_root": bytes_by_root, "records_by_stage": by_stage, "records_by_kind": by_kind,
         "records_by_origin": by_origin,
         "records_by_alias_group": by_alias, "distinct_content_keys": len(keys),
         "content_keys_with_more_than_one_record": dup, "repeated_path_lines_dropped": dupe_lines,
         "degenerate_records_excluded": degenerate,
         "records_without_patient_key": n_null,
         "share_without_patient_key": round(n_null / max(1, n), 4),
         "nulls_by_root": nulls_by_root, "roots_wholly_without_patient_key": all_null,
         "records_without_patient_key_by_stage": null_by_stage,
         "complete": not complaints, "complaints": complaints}
    json.dump(S, open(out, "w"), indent=1)
    print("wrote", out)
    gen = write_summary_fragment(S, a.gen_dir or os.path.join(a.out, "generated"))
    print("wrote", gen)
    if complaints:
        print("NOT A COMPLETE LEDGER -- see the !! lines above; summary.json records complete=false")
        return 2
    return 0


def write_summary_fragment(S, gen_dir):
    """The `ledger_summary` fragment docs/DATA_ACCOUNTING.md splices between its BEGIN/END GENERATED markers.

    WHY HERE. slurm/data_accounting.sh reads $OUT/generated/<name>.md and writes "NOT GENERATED" into the document
    when a fragment is absent. No tool wrote any of them, so the document's results section was six permanent NOT
    GENERATED blocks. This writes the one this tool owns, and it carries the unkeyed share: a document that
    reports how many files were inventoried without reporting how many of them join to a person is stating the
    easy half of the accounting."""
    nb = S["nulls_by_root"]
    L = [f"{S['records']} records over {len(nb)} roots in {S['shards']} shards, "
         f"{S['errors']} errors, {sum(S['bytes_by_root'].values()) / 1e12:.2f} TB. "
         f"{S['distinct_content_keys']} distinct content keys, {S['content_keys_with_more_than_one_record']} of "
         f"them held by more than one record (exact content repeats).\n\n",
         f"**{S['records_without_patient_key']} records ({S['share_without_patient_key']:.1%}) carry no patient "
         f"key**: they join to nobody, enter no alias group and take part in no leakage check.\n\n"]
    bo = S.get("records_by_origin") or {}
    gen = {k: v for k, v in bo.items() if k != ORIGIN_DEFAULT}
    if gen:
        L.append("Origin: " + ", ".join(f"{v} records {k}" for k, v in sorted(gen.items(), key=lambda kv: -kv[1]))
                 + f", {bo.get(ORIGIN_DEFAULT, 0)} acquired. Generated volumes are counted under their SOURCE "
                   f"patient key and are synthetic copies of those people, never new patients.\n\n")
    if not S.get("complete"):
        L.append("**This is not a complete ledger.** " + " ".join(S.get("complaints") or []) + "\n\n")
    if S.get("roots_wholly_without_patient_key"):
        L.append(f"Roots with NO patient key at all: {', '.join(str(k) for k in S['roots_wholly_without_patient_key'])}.\n\n")
    L.append("| root | records | GB | records incl. members | no patient key | share |\n|---|---:|---:|---:|---:|---:|\n")
    for k in sorted(S["records_by_root"], key=lambda x: -S["records_by_root"][x]):
        r = nb.get(k, dict(records=0, no_patient_key=0, share=0.0))
        L.append(f"| {k} | {S['records_by_root'][k]} | {S['bytes_by_root'].get(k, 0) / 1e9:.2f} | "
                 f"{r['records']} | {r['no_patient_key']} | {r['share']:.1%} |\n")
    for k in sorted(nb):
        if k not in S["records_by_root"]:
            r = nb[k]
            L.append(f"| {k} | - | - | {r['records']} | {r['no_patient_key']} | {r['share']:.1%} |\n")
    os.makedirs(gen_dir, exist_ok=True)
    p = os.path.join(gen_dir, "ledger_summary.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("".join(L))
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["roots", "build", "summary"])
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--roots", default=None, help="comma list of root names (default: every root)")
    ap.add_argument("--extra-root", action="append", default=[],
                    help="an ad-hoc root, 'name|path' or 'name|stage|path'; repeat for several")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--progress", type=int, default=200, help="print a line every N files")
    ap.add_argument("--limit", type=int, default=0, help="stop after N files in this shard (a smoke test)")
    ap.add_argument("--force", action="store_true", help="ignore what is already in the shard file")
    ap.add_argument("--count", action="store_true", help="roots: also walk each root and count files/bytes")
    ap.add_argument("--no-pixels", action="store_true", help="byte hashes only; no decode (fast inventory)")
    ap.add_argument("--no-dicom-pixels", action="store_true", help="DICOM headers only, no pixel decode")
    ap.add_argument("--no-bank-members", action="store_true", help="do not list crop-bank members")
    ap.add_argument("--expand-h5", action="store_true", help="also key every 2-D dataset inside an HDF5 container")
    ap.add_argument("--no-sniff", action="store_true", help="do not sniff extensionless files for DICM")
    ap.add_argument("--grid", type=int, default=64, help="volume content key grid (n^3)")
    ap.add_argument("--max-load-gb", type=float, default=4.0,
                    help="volumes bigger than this uncompressed are recorded header-only, with a note")
    ap.add_argument("--gen-dir", default=None,
                    help="summary: where to write ledger_summary.md, the fragment docs/DATA_ACCOUNTING.md splices "
                         "between its BEGIN/END GENERATED markers (default <out>/generated)")
    a = ap.parse_args()
    if not (0 <= a.shard < a.n_shards):
        raise SystemExit(f"--shard {a.shard} outside 0..{a.n_shards-1}")
    return {"roots": cmd_roots, "build": cmd_build, "summary": cmd_summary}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
