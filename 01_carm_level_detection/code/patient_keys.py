#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/patient_keys.py [working tree, uncommitted edit at 097933a]
"""One key per PERSON across every naming scheme, so a split can be drawn on people instead of on file names.

WHY THIS EXISTS. `tools/make_context_crops.py` draws its split per SOURCE directory. Two directories that hold the
same person under different names therefore split independently, and the person lands in training through one and
in validation through the other. This has happened twice in this project, and neither was visible in any score:

  NHANES II   `~/films_drr` anns carry source `nhanes` and patient_id `nhanes_00160`; `~/nhanes_drr` holds the same
              543 films as `NH_00160_c` / `NH_00160_l` with no patient_id. In banks v2, v6 and v7, 48 of the 54
              NHANES validation patients had their other copy in training
              (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md).
  CTSpinoPelvic1K  `~/ctsp_drr` names a case `CTSP_COLONOG_<n>` (the Dataset813 stem) while `~/physics_drr` and
              `~/physics_rare` name the same patient `ctsp_<release id>_<view>_p<k>` (`source_case` in the ann).
              Measured on 2026-09-22: 371 patients on both sides of the v6 and v7 split, 357 of them purely
              because the two banks name one CT two ways.

WHAT IT DOES. Walks the ann directories of the render and film banks and writes {case: patient_key}. The key is
the person, not the file: every pose, every view, every noise draw and every naming scheme of one person collapses
to one key. Cases whose scheme is not recognised are written to `unmatched` and NOT given a key, so a caller can
fail loudly instead of treating them as unique people (the failure mode this file exists to stop).

THE CROSSWALK. CTSpinoPelvic1K is the one scheme that cannot be read off the name: the Dataset813 stem
COLONOG_<n> is tied to the release id <id> only by the symlink imagesTr/COLONOG_<n>_0000.nii.gz -> <id>_ct.nii.gz.
Those links are container paths that dangle on the host (docs: dataset813-image-links-are-container-paths), so the
link TARGET NAME is read, never followed.

    python tools/patient_keys.py --drr ~/ctsp_drr --drr ~/physics_drr --drr ~/physics_rare --drr ~/verse_drr \
        --drr ~/films_drr --drr ~/nhanes_drr --drr ~/ts_drr \
        --d813 ~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs --out ~/patient_keys.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# case-name schemes, most specific first. Each returns (corpus, person) or None.
SCHEMES = [
    # a VerSe series rendered into the ctsp_drr_obl* banks, spelled by NAME (the ann says the same through its
    # patient_id, which _key_for reads first): CTSP_VERSE_verse004_p0 is VerSe series verse004, not a CTSP patient
    ("ctsp_verse_name", re.compile(r"^CTSP_VERSE_((?:gl|verse)\d+[a-z]?)(?:_p\d+)?$")),
    # CTSpinoPelvic1K, Dataset813 stem: CTSP_COLONOG_149  (needs the crosswalk to reach the release id)
    ("ctsp_d813", re.compile(r"^CTSP_(COLONOG_[A-Za-z0-9-]+)$")),
    # CTSpinoPelvic1K, physics render: ctsp_0149_lat_p3
    ("ctsp_release", re.compile(r"^ctsp_(\d{3,5})_(?:lat|ap)_p\d+$")),
    # VerSe, whose names vary more than any other corpus: gl003, glgl017 (a doubled prefix), verse547,
    # verse_gl003_lat_p2, verse_scan-verse547_ap_p0. The person is the LAST (gl|verse)<digits> token in the
    # stem, which is the only part every variant shares.
    # anchor_drr / ws_* name one render per view with no pose index (verse_scan-verse533_ap): the `_p<k>` is optional
    ("verse_any", re.compile(r"^(?:.*?)((?:gl|verse)\d+[a-z]?)(?:_(?:lat|ap)(?:_p\d+)?)?$")),
    # TotalSegmentator: TS_s0585 / totalseg_s0585_lat_p1
    ("ts_plain", re.compile(r"^TS_(s\d+)$")),
    ("ts_render", re.compile(r"^totalseg_(s\d+)_(?:lat|ap)(?:_p\d+)?$")),   # totalseg_s0001_ap: one render per view
    # implant renders: implant_<case>_lat_p0
    ("implant", re.compile(r"^implant_(.+?)_(?:lat|ap)_p\d+$")),
    # NHANES II, the second copy: NH_00160_c / NH_00160_l  (c and l are one person's two films)
    ("nhanes_drr", re.compile(r"^NH_(\d+)_[cl]$")),
    # film corpora in films_drr: NHANES_nhanes_cervical_00160, CSXA_csxa_0001035, BUU_FULL_buu_1673-F-064Y1(1)
    ("nhanes_film", re.compile(r"^NHANES_nhanes_(?:cervical|lumbar)_(\d+)$")),
    ("csxa_film", re.compile(r"^CSXA_csxa_(\w+)$")),
    ("buu_film", re.compile(r"^BUU_FULL_buu_(\d+)-")),
    ("mendeley_film", re.compile(r"^MENDELEY_mendeley_(\w+?)(?:\(\d+\))?$")),
]
# which corpus a scheme belongs to: the person is identified WITHIN a corpus, and two corpora never share people
# unless a scheme pair says so (ctsp_d813 and ctsp_release are the same people; nhanes_drr and nhanes_film are too)
CORPUS_OF = {"ctsp_verse_name": "verse", "ctsp_d813": "ctsp", "ctsp_release": "ctsp", "verse_any": "verse",
             "ts_plain": "ts", "ts_render": "ts", "implant": "implant", "nhanes_drr": "nhanes",
             "nhanes_film": "nhanes", "csxa_film": "csxa", "buu_film": "buu", "mendeley_film": "mendeley",
             "bournemouth_event": "bournemouth", "carmlspine_sweep": "carmlspine"}
# SCOPED schemes: tried (by key_any, ahead of every other rule) ONLY when the corpus hint names the corpus -- a path
# under realxray/<root>/ through _REALXRAY_ROOT_CORPUS, or an item's own hint -- because their ids are too short to
# be distinctive anywhere else. The same device as `scope` in tools/leak_check.RULES. key_for, which keys the render
# and film BANKS by name alone, never sees them.
#   bournemouth_event  Bournemouth cervical quantitative fluoroscopy (Cervical_Database.mat): ImageEvent HV01a / P05b
#                      is one recorded event of healthy volunteer HV01 / patient P05, and every person has exactly two,
#                      a and b (126 events, 63 people, checked against the .mat 2026-09-26). The stem is the event
#                      with whatever frame suffix the exporter adds (HV01a_flex_f0000); a bare person id (HV01) is
#                      accepted too. The event is captured and _norm_person drops the a/b, so HV01a and HV01b are
#                      ONE person and can never sit on two sides of anything.
#   carmlspine_sweep   a C-ArmLSpine CBCT projection sweep (tools/case134_sweep.py; the case39 sweep of
#                      docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md 3): frame ### of patient case<N>'s 301-frame spin is
#                      stem case<N>_sw### under realxray/carmlspine_sweep*/. tools/leak_check's carmlspine.frame rule
#                      reads the spot-frame suffixes (_AP, _LAT2, _OBL, _k<k>) only, so without this row every sweep
#                      frame was unkeyed and level_prototype -- which gates on the frame's path alone -- raised
#                      UnkeyedEvalItem on both sweeps. Anchored at both ends: any other carmlspine stem falls through.
SCOPED_SCHEMES = {
    "bournemouth": ("bournemouth_event", re.compile(r"^((?:HV|P)\d{2}[ab]?)(?:_.*)?$")),
    "carmlspine": ("carmlspine_sweep", re.compile(r"^(case\d+)_sw\d{3}$")),
}


def d813_crosswalk(root):
    """COLONOG_<n> -> release id, from the imagesTr symlink NAMES (never followed: they are container paths)."""
    out = {}
    p = Path(os.path.expanduser(root)) / "imagesTr"
    if not p.exists():
        return out
    for f in sorted(p.iterdir()):
        m = re.match(r"^(COLONOG_[A-Za-z0-9-]+)_0000\.nii\.gz$", f.name)
        if not m:
            continue
        try:
            tgt = os.readlink(f) if f.is_symlink() else ""
        except OSError:
            tgt = ""
        mm = re.search(r"(\d{4})_ct\.nii\.gz$", tgt)
        if mm:
            out[m.group(1)] = mm.group(1)
    return out


def verse_subjects(manifest):
    """series_id -> patient_id from the VerSe manifest, so a SERIES is never mistaken for a person.

    Measured 2026-09-22 (docs/PATIENT_IDENTITY_SPEC.md, alias 7): the organisers' table groups 37 series into
    18 subjects -- verse400 owns series 090 and 155, verse405 owns 212, 258 and 259 -- and every other series is
    its own subject. The v8 bank keyed on the series token and put five of those eighteen people on both sides
    of its split, 10.5 % of the VerSe validation entries. The `gl###` rows carry patient_id == series_id.
    """
    import csv
    p = Path(os.path.expanduser(manifest))
    if not p.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(p, newline="")):
        s, pid = (r.get("series_id") or "").strip(), (r.get("patient_id") or "").strip()
        if s and pid:
            out[s] = pid
    return out


def key_for(case, ann, cross, verse_map=None):
    """(corpus, person, scheme) for one case, or None when no scheme matches.

    The ann's own patient_id wins when it carries one, because it is the corpus's own statement of identity; it is
    normalised into the same (corpus, person) form so that `nhanes_00160` and `NH_00160_c` meet. A VerSe person is
    then resolved from series to SUBJECT through the manifest (`verse_subjects`), whichever route produced it.
    """
    k = _key_for(case, ann, cross)
    if k is None:
        return None
    corpus, person, scheme = k
    if corpus == "verse" and verse_map:
        subj = verse_map.get(person)
        if subj and subj != person:
            return (corpus, subj, scheme + "+verse_manifest")
    return k


def _key_for(case, ann, cross):
    pid = (ann or {}).get("patient_id") or ""
    if pid:
        # ctsp_drr_obl / ctsp_drr_obl2 name 314 VerSe series `CTSP_VERSE_<series>` and write that as the ann's
        # patient_id; the plain split below would file them as corpus `ctsp`, person `VERSE_<series>` -- a VerSe
        # subject counted as a CTSpinoPelvic1K patient (docs/PATIENT_IDENTITY_SPEC.md, alias 8). The bank name
        # is not the corpus; the series token is.
        mv = re.match(r"^CTSP_VERSE_((?:gl|verse)\d+[a-z]?)$", str(pid))
        if mv:
            return ("verse", mv.group(1), "patient_id_ctsp_verse")
        m = re.match(r"^([a-zA-Z]+)_?(\w+)$", str(pid))
        if m:
            return (m.group(1).lower(), m.group(2), "patient_id")
    sc = (ann or {}).get("scheme") or ""
    src_case = (ann or {}).get("source_case") or ""
    if sc == "ctsp" and src_case:
        return ("ctsp", str(src_case).zfill(4), "ann_source_case")
    for name, rx in SCHEMES:
        m = rx.match(case)
        if not m:
            continue
        person = m.group(1)
        if name == "ctsp_d813":
            rel = cross.get(person)
            if not rel:
                return None                      # a stem with no crosswalk entry is NOT silently unique
            person = rel
        if name == "ctsp_release":
            person = person.zfill(4)
        if name in ("nhanes_drr", "nhanes_film"):
            person = str(int(person)).zfill(5)    # 00160 and 160 are one person
        return (CORPUS_OF[name], person, name)
    return None


# ------------------------------------------------------------------------------------------------ one entry point
# WHY. The schemes above key the render and film BANKS. tools/leak_check.py's RULES key everything else a model can
# have seen: real C-arm frames (DeepFluoro specimen, C-ArmLSpine case, COBRA centre+case), detector-corpus stems
# with __zoom suffixes, and pose-donor renders (s0224_00_17-1882-015_elekta_xvi_0). Two tables keyed two halves of
# the data and nothing joined them, so a checkpoint's training list and an evaluation list could be keyed by
# different code and never meet. key_any() is the one call both sides use (tools/checkpoint_lineage.py for what a
# checkpoint touched; an evaluation gate for what it is scored on). It adds NO naming rule: it tries this module's
# schemes first (they carry the Dataset813 crosswalk and the VerSe subject map), then leak_check.RULES, and
# normalises the one corpus the two tables spell differently ("totalseg" there is "ts" here).
_LEAK_CORPUS = {"totalseg": "ts"}
_RE_D813 = dict(SCHEMES)["ctsp_d813"]   # by name: a scheme inserted ahead of it must not move the guard
# a real-frame directory -> the corpus whose scoped rule keys its stems. The four roots are the devices of
# tools/leak_check.DEFAULT_COLLECTIONS; re-exports reach a root through tools/realxray_banks.json `derived_of`.
# The prefix row is a DECLARATION for export directories that are in neither table (carmlspine_cv, cobra_elekta_v3):
# the exporters name them after the corpus, and a directory matching none of these gets no hint and fails loudly.
# bournemouth_qf is not a leak_check collection: it is an evaluation-only corpus (tools/bournemouth_qf_eval.py), keyed
# here so that the gate can PROVE no model saw it rather than being told so with --not-held-out.
_REALXRAY_ROOT_CORPUS = {"carmlspine": "carmlspine", "cobra_elekta": "cobra", "cobra_varian": "cobra",
                         "deepfluoro": "deepfluoro", "geneva_hip": "geneva", "bournemouth_qf": "bournemouth"}
_REALXRAY_PREFIX = (("carmlspine", "carmlspine"), ("cobra_", "cobra"), ("deepfluoro", "deepfluoro"),
                    ("geneva", "geneva"), ("bournemouth", "bournemouth"))
_PATH_HINTS = (("/raw/nhanes_full/", "nhanes"), ("/raw/buu_full/", "buu"), ("/raw/csxa/", "csxa"),
               ("/ljubljana", "ljubljana"), ("/spinesac", "spinesac"), ("/vindr", "vindr"), ("lateral236", "lat236"),
               # the raw release directory is spelled with an underscore (slurm/corpus_expand.sh:88)
               ("/raw/lateral_236/", "lat236"))
_RX_BANKS = None


def _realxray_derived():
    global _RX_BANKS
    if _RX_BANKS is None:
        try:
            _RX_BANKS = json.load(open(Path(__file__).resolve().parent / "realxray_banks.json"))["banks"]
        except Exception:  # noqa: BLE001  (absent registry: only the declared roots and prefixes apply)
            _RX_BANKS = {}
    return _RX_BANKS


def corpus_hint_for_path(*paths):
    """The corpus a file's location declares, or None. Pass the listed path AND its realpath: a list entry is often a
    symlink (devcorpus/lists/lcurve_*/firstval/images/A158_0000.png -> realxray/cobra_elekta/images/val/...) and only
    the target says which corpus the frame belongs to."""
    banks = _realxray_derived()
    for p in paths:
        s = str(p or "").replace("\\", "/")
        m = re.search(r"/realxray/([^/]+)/", s)
        if m:
            ds, seen = m.group(1), set()
            while ds not in seen and ds not in _REALXRAY_ROOT_CORPUS:
                seen.add(ds)
                ds = (banks.get(ds) or {}).get("derived_of") or ds
            if ds in _REALXRAY_ROOT_CORPUS:
                return _REALXRAY_ROOT_CORPUS[ds]
            for pre, corpus in _REALXRAY_PREFIX:
                if m.group(1).startswith(pre):
                    return corpus
        for frag, corpus in _PATH_HINTS:
            if frag in s:
                return corpus
    return None


def _norm_person(corpus, person):
    person = str(person)
    if corpus == "nhanes" and person.isdigit():
        return str(int(person)).zfill(5)
    if corpus == "ctsp" and person.isdigit():
        return person.zfill(4)
    if corpus == "bournemouth":
        return re.sub(r"(?<=\d)[ab]$", "", person)      # HV01a and HV01b are two events of ONE person, HV01
    return person


# ------------------------------------------------------------------------------------------------ one spelling per key
# WHY. A gate compares a checkpoint's train/val keys with an evaluation's keys by set intersection, so one person
# spelled two ways is two people and the intersection comes back EMPTY -- the leak is there and the check is clean.
# SchwingNet/results/eval_gate/touched.json (2026-09-23) holds exactly that: the C-ArmLSpine fold banks
# (carm_cvmix*, carm_cvdaymix*, carm_mix) carry ann patient_id `case100`, which key_for's patient_id branch splits
# as corpus `case`, person `100`, while a C-ArmLSpine frame keys to `carmlspine:case100`. The ablation banks do the
# same to VerSe (`gl:017` for `verse:gl017`); pseudo-labelled lateral_236 films keep their prefix under the scoped
# rule (`lat236:LAT236PS_000001` for `lat236:000001`); AASCE and Mendeley detector-corpus stems keep a derived-view
# suffix (`__zoom1`). canon_key maps every spelling seen in a real key set to one form. It is applied to BOTH sides of
# every comparison (tools/eval_gate.py, leak_check CHK-9), and it changes no function above: key_for / key_any
# still return what they returned, so a split or a registry built from them is not moved under anybody's feet.
_CANON_CORPUS = {"totalseg": "ts", "case": "carmlspine", "gl": "verse"}


def canon_key(key):
    """'<corpus>:<person>' in the one spelling every comparison uses; a string that is not a key comes back as it is."""
    key = str(key)
    corpus, sep, person = key.partition(":")
    if not sep or not corpus or not person:
        return key
    raw_corpus = corpus
    corpus = _CANON_CORPUS.get(corpus, corpus)
    if "__" in person:                                   # a derived view (`__zoom1`, `__full`) is its parent's person
        person = person.split("__")[0]
    if raw_corpus == "case" and person.isdigit():
        person = f"case{int(person)}"
    if raw_corpus == "gl" and person.isdigit():
        person = f"gl{person}"
    if corpus == "carmlspine":
        m = re.fullmatch(r"case0*(\d+)", person)
        if m:
            person = f"case{int(m.group(1))}"
    if corpus == "lat236":
        person = re.sub(r"^LAT236PS_", "", person)
    if corpus == "mendeley":
        m = re.match(r"^(\d+)-[MF]-", person)          # the BUU-style name: the patient is the leading number
        if m:
            person = m.group(1)
    return f"{corpus}:{_norm_person(corpus, person)}"


_RE_IMPLANT =re.compile(r"^implant_(.+?)(_v\d+)?_(?:lat|ap)(?:_p\d+)?$")


# ------------------------------------------------------------------------------------------------ a key names a person
# WHY. tools/eval_gate.py used to take a pre-formed '<corpus>:<id>' as given whenever the corpus was one it knew. Two
# things passed that way that are not people (SchwingNet/results/eval_gate/VERIFY.md item 1b-iii): `implant:0001_v0`,
# a RENDER of ctsp:0001 with metal painted in (~/patient_keys_v9.json spells 194 v9 validation cases that way, and the
# gate then missed 91 persons the v9 encoder trained on), and any well-formed string in a known corpus (`ts:bogus`).
# resolve_key is the one test a key handed to a gate must pass: canonical spelling (canon_key), an implant key mapped
# to its SOURCE CT (key_any's implant rule: make_implant_ct's hardware record, else the one declared build whose case
# format fits), and a person id of the shape that corpus's own naming produces. The shapes below are the person-id
# grammar of SCHEMES and tools/leak_check.RULES; every one of the 34,276 canonical keys in the lineage store
# (touched.json of 2026-09-23, 15 corpora) and every key of eval_sets.json fits its corpus's shape. A shape check says the key COULD name a person of that corpus; it is not a
# registry of who exists (ts:s9999 fits), which no corpus here ships for every release.
PERSON_FORMAT = {
    "ts": r"s\d{3,5}",
    "ctsp": r"\d{4}",
    "verse": r"(?:gl)+\d{3,4}[a-z]?|verse\d{3,4}[a-z]?|\d{1,4}[a-z]?",
    "carmlspine": r"case\d+",
    "cobra": r"[A-G]\d{2,4}",
    "deepfluoro": r"\d{2}-\d{4}",
    "nhanes": r"\d{5,6}",
    "buu": r"\d{3,5}",
    "csxa": r"[A-Za-z0-9\-.]+",
    "mendeley": r".+",
    "aasce": r".+",
    "spinalai": r".+",
    "geneva": r"[A-Za-z]+",
    "ljubljana": r"[A-Za-z]*\d+",
    "spinesac": r"[A-Za-z0-9\-]+",
    "fluorocap": r"PMC\d{5,9}|FLUO-\d{4,8}",
    "fluorocap_video": r"[A-Za-z0-9_-]+",
    "vindr": r"[0-9a-f]{8,64}",
    "lat236": r"[A-Za-z0-9_.\-]+",
    "bournemouth": r"(?:HV|P)\d{2}",
}


def resolve_key(key, implant_map=None, implant_builds=None, cross=None, verse_map=None):
    """(canonical key, None) when `key` names a person; (None, why) when it does not.

    An `implant:<case>[_v<k>]` key is a render, never a person: it resolves to its source CT's key through the implant
    records / declared builds, or it does not resolve at all."""
    k = canon_key(key)
    corpus, sep, person = k.partition(":")
    if not sep or not corpus or not person:
        return None, f"{key!r} is not a '<corpus>:<person>' key"
    if corpus == "implant":
        r, why = key_any(f"implant_{person}_ap_p0", None, cross, verse_map, None, implant_map, implant_builds)
        if not r:
            return None, (f"{key}: an implant key names a RENDER of a source CT, not a person, and that source cannot "
                          f"be read here ({why})")
        src, why2 = resolve_key(r["key"])
        return (src, None) if src else (None, f"{key} -> {r['key']}: {why2}")
    fmt = PERSON_FORMAT.get(corpus)
    if fmt is None:
        return None, f"{key}: corpus {corpus!r} has no person-id grammar (patient_keys.PERSON_FORMAT), so no person is known by it"
    if not re.fullmatch(fmt, person):
        return None, f"{key}: {person!r} is not a {corpus} person id (the corpus names its people {fmt})"
    return k, None


def implant_sources(roots):
    """'<case>_v<k>' -> (scheme, case), read from tools/make_implant_ct.py's <dst>/hardware/<case>_v<k>.json records.

    An implant render (`implant_0001_v0_ap`) is a render of a SOURCE CT with metal painted in; make_implant_ct names
    its output after the source case and records the source scheme (ctsp / verse / totalseg). Keyed on its name
    alone it becomes a patient called `implant:0001_v0`, which never meets `ctsp:0001` -- the same patient's plain
    renders -- so a split could put the two on opposite sides and no check would see it."""
    out = {}
    for r in roots:
        d = Path(os.path.expanduser(str(r)))
        if not d.is_dir():
            continue
        for f in d.glob("*.json"):
            if f.name.startswith("build_stats"):
                continue
            try:
                j = json.load(open(f))
            except Exception:  # noqa: BLE001
                continue
            if j.get("case") and j.get("scheme"):
                out[f.stem] = (str(j["scheme"]), str(j["case"]))
    return out


# tools/make_implant_ct.list_cases: the case id each --scheme produces, which is the <case> of its <case>_v<k> output
# (ctsp: the release id of <id>_label.nii.gz; totalseg: the subject directory s####; verse: the VerSeFusion unified
# directory, scan-gl003 / verse547). The three are disjoint, so when a build's hardware records are gone (~/implant_ct,
# deleted with the quota cleanup) the source scheme of `implant_0004_v0_ap` is read from its name -- but ONLY among the
# schemes a launch script declares a make_implant_ct build for (`implant_builds`), and only when exactly one fits.
IMPLANT_CASE_FORMAT = {"ctsp": re.compile(r"\d{4}"), "totalseg": re.compile(r"s\d{4}"),
                       "verse": re.compile(r"(?:scan-|sub-)?(?:gl)*(?:gl|verse)\d+[a-z]?")}
# a stem that carries its BANK in front: ~/buu_yolo names images `<bank>__<bank case>` (ctsp_drr__CTSP_COLONOG_1,
# ctsp_drr_obl2__CTSP_VERSE_verse004_p0, vindr_pseudo__VINDRPS_<id>). leak_check keys the part before a double
# underscore (its derived-view rule, right for `buu_0003__zoom0`), which here is the bank; the person is the part
# after it. Only render/pseudo-label bank directory names (`*_drr`, `*_drr_<x>`, `*_pseudo`) are taken as a prefix.
_RE_BANK_PREFIX = re.compile(r"^(?P<bank>[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*?_(?:drr(?:_[A-Za-z0-9]+)?|pseudo))__(?P<rest>.+)$")


def key_any(ident, ann=None, cross=None, verse_map=None, corpus_hint=None, implant_map=None, implant_builds=None):
    """({"key": "<corpus>:<person>", "scheme": ..., "pose_key": ... or None}, None), or (None, reason).

    `ident` is a case name or a file stem. A name no rule keys comes back as (None, reason) and is NEVER a patient
    of its own; the caller counts and reports it. A Dataset813 stem without a crosswalk entry, and a
    CTSpinoPelvic1K name that is not a release id, are refused rather than passed to a looser rule, because both
    are the alias gap that put 357 patients on two sides of the v6/v7 split. An implant render is keyed to its
    SOURCE CT through `implant_map` (implant_sources()); without a record for it, through the one declared build
    whose case format its name fits (`implant_builds`, a set of make_implant_ct --scheme values read from launch
    scripts); failing both it is refused, not keyed as a patient called `implant:<case>`."""
    cross = cross or {}
    ident = str(ident)
    if corpus_hint in SCOPED_SCHEMES:                   # scoped first, as in leak_check.key_for; no match falls through
        sname, srx = SCOPED_SCHEMES[corpus_hint]
        ms = srx.match(ident)
        if ms:
            corpus = CORPUS_OF[sname]
            return {"key": f"{corpus}:{_norm_person(corpus, ms.group(1))}", "scheme": sname, "pose_key": None}, None
    mb = _RE_BANK_PREFIX.match(ident)
    if mb:
        r, why = key_any(mb.group("rest"), ann, cross, verse_map, corpus_hint, implant_map, implant_builds)
        if r:
            r = {**r, "scheme": f"bank_prefix:{mb.group('bank')}+" + r["scheme"]}
        return r, why
    mi = _RE_IMPLANT.match(ident)
    if mi:
        name = mi.group(1) + (mi.group(2) or "")
        src = (implant_map or {}).get(name) or (implant_map or {}).get(mi.group(1))
        how = "implant_source"
        if not src and implant_builds:
            fits = sorted({s for s in implant_builds
                           if s in IMPLANT_CASE_FORMAT and IMPLANT_CASE_FORMAT[s].fullmatch(mi.group(1))})
            if len(fits) == 1:
                src, how = (fits[0], mi.group(1)), "implant_build_declared"
        if not src:
            return None, (f"{ident}: an implant render with no make_implant_ct hardware record for {name!r}"
                          + (f" and no single declared build ({sorted(implant_builds)}) whose case format fits it"
                             if implant_builds else "")
                          + "; its source CT cannot be read, and it is not keyed as a patient of its own")
        scheme, case = src
        if scheme == "ctsp":
            r, why = key_any(f"ctsp_{str(case).zfill(4)}_ap_p0", None, cross, verse_map)
        elif scheme == "totalseg":
            r, why = key_any(f"TS_{case}", None, cross, verse_map)
        else:
            r, why = key_any(str(case), None, cross, verse_map)
        if r:
            r = {**r, "scheme": f"{how}:{scheme}+" + r["scheme"]}
        return r, why
    m = _RE_D813.match(ident)
    if m and m.group(1) not in cross and not (ann or {}).get("patient_id"):
        return None, f"{ident}: a Dataset813 stem with no crosswalk entry (pass the Dataset813 imagesTr links)"
    k = key_for(ident, ann, cross, verse_map)
    if k is not None:
        corpus, person, scheme = k
        return {"key": f"{corpus}:{_norm_person(corpus, person)}", "scheme": scheme, "pose_key": None}, None
    try:
        import leak_check as _lc
    except ImportError:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import leak_check as _lc
    lk, why = _lc.key_for(ident, corpus_hint)
    if lk is None:
        return None, why
    corpus = _LEAK_CORPUS.get(lk["corpus"], lk["corpus"])
    person = _norm_person(corpus, lk["patient"])
    if corpus == "ctsp" and not re.fullmatch(r"\d{4}", person):
        return None, f"{ident}: a CTSpinoPelvic1K name that is not a release id ({person}); not keyed"
    pose_key = None
    if lk.get("pose"):
        pose = lk["pose"]
        hint = "cobra" if re.fullmatch(r"[A-G]\d{2,4}", pose) else None
        pk, _ = key_any(pose, corpus_hint=hint) if not re.fullmatch(r"(?:lat|ap)(?:_p\d+)?", pose) else (None, None)
        pose_key = pk["key"] if pk else None
    return {"key": f"{corpus}:{person}", "scheme": "leak_check:" + lk["rule"], "pose_key": pose_key}, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drr", action="append", required=True, help="a bank root holding ann/*.json")
    ap.add_argument("--d813", default="~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs")
    ap.add_argument("--out", required=True)
    ap.add_argument("--read-ann", action="store_true", default=True,
                    help="open every ann for patient_id / scheme / source_case (default; the names alone are not enough)")
    ap.add_argument("--verse-manifest", default="~/VerSeFusion/data/manifest/manifest.csv",
                    help="series_id -> patient_id; a VerSe series is keyed to its SUBJECT (pass '' to disable)")
    a = ap.parse_args()
    cross = d813_crosswalk(a.d813)
    print(f"crosswalk: {len(cross)} Dataset813 stems -> release ids", flush=True)
    vmap = verse_subjects(a.verse_manifest) if a.verse_manifest else {}
    n_multi = sum(1 for s, p in vmap.items() if s != p)
    print(f"verse manifest: {len(vmap)} series -> {len(set(vmap.values()))} subjects "
          f"({n_multi} series belong to a subject that owns more than one)", flush=True)
    keys, unmatched, by_scheme = {}, [], {}
    for root in a.drr:
        r = Path(os.path.expanduser(root))
        anns = sorted((r / "ann").glob("*.json")) if (r / "ann").exists() else []
        n_ok = 0
        for p in anns:
            case = p.stem
            ann = None
            if a.read_ann:
                try:
                    ann = json.load(open(p))
                except Exception:                 # noqa: BLE001  (a torn ann must not stop the audit)
                    ann = None
            k = key_for(case, ann, cross, vmap)
            if k is None:
                unmatched.append(f"{r.name}/{case}")
                continue
            corpus, person, scheme = k
            keys[case] = f"{corpus}:{person}"
            by_scheme[scheme] = by_scheme.get(scheme, 0) + 1
            n_ok += 1
        print(f"  {r.name:<16} {len(anns):>6} cases, {n_ok} keyed", flush=True)
    people = sorted(set(keys.values()))
    print(f"{len(keys)} cases -> {len(people)} people; schemes used: {by_scheme}")
    print(f"unmatched (NOT keyed, a caller must fail on these): {len(unmatched)}")
    for u in unmatched[:20]:
        print("   ", u)
    out = Path(os.path.expanduser(a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump({"keys": keys, "unmatched": unmatched, "n_people": len(people), "by_scheme": by_scheme,
               "crosswalk_n": len(cross), "roots": [str(Path(os.path.expanduser(x))) for x in a.drr]},
              open(out, "w"), indent=1)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
