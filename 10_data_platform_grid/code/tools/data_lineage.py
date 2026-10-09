#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/data_lineage.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""The data pathway, as a graph over CANONICAL ITEMS rather than file names.

WHY THIS EXISTS. On 2026-09-22 the same 543 NHANES II films were found in one level bank twice, under two
source names (`nhanes` from ~/films_drr and `nhanes_drr` from ~/nhanes_drr), and the split was drawn per
source, so 48 of 54 validation patients had their duplicate in training (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md).
Nothing raised. Every per-dataset check passed, because each copy was internally consistent: the defect only
exists BETWEEN datasets, and no tool looked there. The same shape of error is what the aliased DeepFluoro roots
invite (`deepfluoro_h5`, the JHU subset, and `deepfluoro_vendor`, the vendor DICOMs of the SAME frames) and what
two names for one CT corpus invite (`ctsp_drr` cases `CTSP_COLONOG_<stem>` beside `physics_drr` cases `ctsp_<nnnn>`).
That second one is NOT readable off the names: the Dataset813 imagesTr symlinks say COLONOG_100 is release 0145, and
of the 802 links exactly one agrees with its own index, so `--collapse ctsp` requires `--d813` (the symlink names) or
`--patient-keys` (tools/patient_keys.py) and is refused without one rather than guessing from the number.

THE TRAP THIS AVOIDS is checking leakage on the name of a file. A file name is a label a builder chose; the same
photograph, the same patient and the same cadaver arrive under several of them. So every item is reduced to a
CANONICAL ID naming the physical thing it came from -- a CT subject, a plain film's patient, a real C-arm frame,
a pose -- and disjointness is checked on those ids. A derived image (a DRR, a crop, a styled render) is never a
canonical thing: it inherits the id or ids of its parents, so a crop of a render of subject s0224 is s0224.

EVERY LINK SAYS HOW IT WAS ESTABLISHED. Each canonical id carries the rule that produced it, and each rule is
marked `recorded field` (the ann/meta/json on disk says so) or `file name` (the tool parsed a naming convention).
A link that cannot be made from disk is written into the output as an `unresolved` row with its reason -- never
guessed, never silently dropped. Candidate aliases (two names that MIGHT be one thing) are reported as
candidates with the count they would collapse, and are not collapsed unless asked for by name.

WHAT IT READS (all read-only, all small files):
  <home>/*_drr/ann/*.json          render and film banks: case, source, patient_id, scheme/source_case
  <home>/*_ctx/meta.json           context-crop banks: classes, rungs, val_cases, merged_from
  <home>/*_ctx/rung_*.npz          the bank's own case / split / source arrays (X is never touched)
  <home>/spine-detector/data/*/data.yaml     detector datasets and the chains between them
  <data>/devcorpus/render/*/*.json           subject + pose of every device render
  <data>/devcorpus/styled/*/images/*/*.jpg   styled images (stem prefix -> render)
  <data>/devcorpus/lists/*/{train,val}.txt   leave-one-device-out membership
  <data>/realxray/*/splits.json, meta/*.json real frames per device
  <data>/or_ready/*/*.json                   result files (case lists where they carry one)
  ~/model_registry/registry.jsonl            which bank each model was trained on

TWO NAMES FOR ONE CORPUS ARE COLLAPSED BY DECLARATION (CORPUS_ALIAS: buu_full = buu, nhanes_drr = nhanes, ...),
and a detector image is matched to the film bank's patient by prefix when one exists (R8b), because without that
the same film is `film:buu/0001` in one stage and `film:buu_full/buu_0001` in the other, each stage is internally
clean, and the pair is never compared -- which is the failure this tool exists to end.

OUTPUT. `lineage.json` (schema `data_lineage/1`, documented in SCHEMA_DOC below) and `lineage.md` beside it: a
stage table, the leakage table, the unresolved table, the alias table and a mermaid diagram of the pathway. A
clean leakage table means clean AMONG THE ITEMS THAT COULD BE KEYED: every row carries the node's `unkeyed`
count and the run prints the caution when nothing leaked but something was unresolved.

WHERE TO RUN IT. It opens tens of thousands of small JSONs over CephFS, so it belongs in a batch job, never on
the login node.

    python tools/data_lineage.py build --out /rs/rs_grp_oschome/go2432/data/or_ready/lineage/lineage.json \
        --d813 ~/spinesurg-ct-nnunet/nnunet/raw/Dataset813_SpineSurgLSTVFullRibs --collapse ctsp
    python tools/data_lineage.py build --out ./lineage.json --home ./sample --data ./sample --sections drr,crops
    python tools/data_lineage.py check --lineage .../lineage.json     # exit 1 if a canonical id straddles a split
    python tools/data_lineage.py show  --lineage .../lineage.json

This is the LINEAGE layer. It consumes the checksum ledger when one is given (`--ledger`), and joins on it by
file path or hash; without one it still runs, and says so in the output. It does not hash pixels and it does not
look for near-duplicates: that is tools/or_audit_dupes.py (NCC32/NCC64), which finds the same picture under two
names when no recorded field connects them. The two are complements -- this tool finds what the records say,
that one finds what the records omit.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import platform
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA = "data_lineage/1"

SCHEMA_DOC = {
    "schema": "the string 'data_lineage/1'; bump it when a field changes meaning",
    "built/host/git/argv": "when, where, which commit, which command line",
    "roots": "the home and data roots that were scanned, and whether each section ran",
    "ledger": "the checksum ledger this run joined against (null when none was given), with the join rate",
    "rules": "id -> {what, basis: 'recorded field'|'file name'|'declared'|'none', inferred, n_items}. Every "
             "canonical id was made by exactly one rule; `inferred` is true when the rule read a naming "
             "convention rather than a field",
    "nodes": "[{id: '<stage>:<name>', stage, name, path, present, n_items, n_canonical, key_rule (Counter), "
             "by (per-source/per-split counts), examples, notes}]. n_items counts files/rows on disk; "
             "n_canonical counts distinct physical things behind them",
    "edges": "[{src, dst, kind: 'derives'|'merges'|'trained_on'|'evaluated_on'|'references', n_items, evidence, "
             "inferred, note}]. `evidence` names the file and field that establishes the edge",
    "models": "[{name, sha, stage, bank, bank_node, train:{n_items,n_canonical}, eval:{...}, "
              "overlap:{n_canonical_shared, examples}, unresolved[]}]",
    "leakage": "[{check, node, namespace, side_a, n_a, side_b, n_b, n_shared, examples, severity: 'leak'|"
               "'by design'|'candidate'|'clean', explanation}] -- side_a/side_b name the two sides being compared "
               "(train vs val, train+val vs test, ...); severity 'leak' with n_shared>0 is what `check` fails on",
    "aliases": "[{group, members, status: 'collapsed'|'candidate'|'declared', evidence, n_items}]",
    "shared": "[{a, b, n_shared, namespace, examples}] -- canonical ids held by two nodes at once; this is the "
              "pathway seen from the item's side, and the input to any picture of it",
    "unresolved": "[{what, where, reason, n_items}] -- every link that could NOT be made from disk",
}

# ---------------------------------------------------------------- canonical-id rules
RULES = {
    "R1":  dict(what="CT id from the ann's own scheme + source_case fields", basis="recorded field", inferred=False),
    "R2":  dict(what="film id from the ann's patient_id, corpus prefix stripped", basis="recorded field", inferred=False),
    "R3a": dict(what="NHANES id from the ann's source_file pickle name (C|L<id>_...)", basis="recorded field", inferred=False),
    "R3b": dict(what="NHANES id from the case name NH_<id>_<c|l>", basis="file name", inferred=True),
    "R4":  dict(what="TotalSegmentator subject from the case name TS_s####", basis="file name", inferred=True),
    "R5":  dict(what="CTSpinoPelvic1K Dataset813 stem from the case name CTSP_<COLONOG_...>; the stem is kept whole "
                     "(34 of the 802 are COLONOG_CTC-<accession>, not an integer) and is NOT read as a release id",
                basis="file name", inferred=True),
    "R5x": dict(what="CTSpinoPelvic1K release id reached from the Dataset813 stem through the imagesTr symlink "
                     "crosswalk (COLONOG_100 -> 0145): the only thing on disk that ties the two namings",
                basis="recorded field", inferred=False),
    "R6":  dict(what="VerSe subject = the case name of a verse render directory", basis="file name", inferred=True),
    "R7":  dict(what="no rule matched: the item is its own canonical id", basis="none", inferred=True),
    "R8":  dict(what="detector film id from the image stem <corpus>_<rest>, with __zoom<k>/__aug<k> stripped", basis="file name", inferred=True),
    "R8a": dict(what="NHANES id from the trailing digits of a detector stem", basis="file name", inferred=True),
    "R8b": dict(what="detector stem resolved to a film bank's patient id by verified prefix match", basis="verified prefix match", inferred=False),
    "R9":  dict(what="render subject and pose from the render json's own subject/pose fields", basis="recorded field", inferred=False),
    "R10": dict(what="styled image inherits the render whose stem is its longest matching prefix", basis="verified prefix match", inferred=False),
    "R11": dict(what="real frame id from the realxray meta's case/stem fields", basis="recorded field", inferred=False),
    "R12": dict(what="crop-bank case resolved through the DRR ann index (so it carries the ann's rule)", basis="recorded field", inferred=False),
    "R13": dict(what="ledger join: the canonical id came from the checksum ledger", basis="recorded field", inferred=False),
    "R14": dict(what="DeepFluoro frame id <specimen>/<index> read off a case name in a bank that names deepfluoro "
                     "(so the vendor DICOMs and the JHU h5 land on one id instead of two)",
                basis="file name", inferred=True),
}

# Aliases this project has to hold in mind. `collapsed` ones are made one id by the rules above; `candidate`
# ones are NOT collapsed, because nothing on disk proves they are the same thing.
DECLARED_ALIASES = [
    dict(group="nhanes_two_directories", members=["~/films_drr (source 'nhanes')", "~/nhanes_drr (source 'nhanes_drr')"],
         status="collapsed", evidence="films_drr ann.patient_id 'nhanes_01311' and nhanes_drr case 'NH_01311_l' / "
                                      "source_file 'L01311_lumbar_masks_4.pkl' carry the same NHANES id (R2 + R3a)"),
    dict(group="deepfluoro_h5_vs_vendor", members=["~/deepfluoro/unpacked_full (JHU subset, h5)",
                                                   "<data>/deepfluoro_vendor/unpacked (vendor DICOMs)"],
         status="declared", evidence="tools/data_manifest.py ROOTS: deepfluoro_vendor is 'vendor DICOM headers of the "
                                     "same frames' as deepfluoro_h5. Both would reduce to frame:deepfluoro/<specimen>/<idx>"),
    dict(group="deepfluoro_pose_vs_frame", members=["devcorpus pose <specimen>/<idx>", "realxray/deepfluoro frame <specimen>_<idx>"],
         status="candidate", evidence="checked at run time: the pose count in devcorpus/poses/cios_fusion.json against the "
                                      "number of real DeepFluoro frames on disk"),
    dict(group="ctsp_colonog_vs_ctsp", members=["~/ctsp_drr cases CTSP_COLONOG_<stem>", "~/physics_drr ann.source_case <nnnn> (scheme ctsp)"],
         status="candidate", evidence="both name CTSpinoPelvic1K, and the ONE thing on disk that ties them is the Dataset813 "
                                      "symlink imagesTr/<stem>_0000.nii.gz -> <release id>_ct.nii.gz. That map is NOT the "
                                      "identity: of its 802 entries only ONE (COLONOG_1 -> 0001) has index == release id, "
                                      "and 34 stems are COLONOG_CTC-<accession> with no index at all. Pass --d813 (or "
                                      "--patient-keys) with --collapse ctsp; the collapse is refused without one"),
    dict(group="yolo_v4z_zoom_crops", members=["yolo_v3 films", "yolo_v4z <stem>__zoom<k>"],
         status="collapsed", evidence="a v4z stem is a v3 stem plus __zoom<k>; R8 strips the suffix"),
]

# One film corpus, several directory names. Collapsing these is what lets a film in the detector corpus and the
# same film in a level bank be recognised as one patient; without it each corpus is internally clean and the pair
# is never compared. Every entry here is a DECLARED equivalence of corpus NAMES, not of items.
CORPUS_ALIAS = {"buu_full": "buu", "buu_lspine": "buu", "nhanes_drr": "nhanes", "nhanes_full": "nhanes",
                "mendeley_716": "mendeley", "csxa_raw": "csxa", "mendeley_raw": "mendeley"}

AUG_SUFFIX = re.compile(r"__(?:zoom|aug|crop)\d+$")
RE_NH_CASE = re.compile(r"^NH_(\d{4,6})_[a-z]$")
RE_NH_PKL = re.compile(r"^[CL](\d{4,6})_")
RE_TS = re.compile(r"^TS_(s\d{3,5})$")
RE_COLONOG = re.compile(r"^CTSP_(COLONOG_[A-Za-z0-9.-]+)$")
RE_DF_STEM = re.compile(r"^(\d\d-\d{4})[_/](\d+)$")


def sh(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=10).decode().strip()
    except Exception:  # noqa: BLE001
        return ""


def jload(p, cap=64 << 20):
    """json or None, with the reason kept out of the way; files above `cap` bytes are refused, not read."""
    try:
        if os.path.getsize(p) > cap:
            return None
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None


def stem_of(p):
    return os.path.splitext(os.path.basename(p))[0]


def norm_path(p):
    """One spelling for a path on both sides of the ledger join. Without abspath a ledger of absolute paths never
    meets a scan given a relative --home, and the join rate silently reads 0."""
    return os.path.normcase(os.path.abspath(os.path.expanduser(str(p))))


def disp(p):
    """One separator in the output whichever host wrote it, so a path can be grepped for on either."""
    return None if p is None else str(p).replace("\\", "/")


def strip_prefix(ident, corpus):
    """'nhanes_01311' with corpus 'nhanes' -> '01311'. Leaves anything else alone."""
    for pre in (corpus + "_", corpus.upper() + "_"):
        if ident.startswith(pre):
            return ident[len(pre):]
    return ident


def film_id(corpus, ident):
    """film:<corpus>/<identifier> with the corpus name put through CORPUS_ALIAS and its prefix stripped off the
    identifier, so ~/films_drr source 'buu_full' patient 'buu_0001' and a detector stem 'buu_0001-...' can meet."""
    c = CORPUS_ALIAS.get(str(corpus), str(corpus))
    return f"film:{c}/{strip_prefix(strip_prefix(str(ident), str(corpus)), c)}"


# ---------------------------------------------------------------- the canonical id
def canon_from_ann(case, ann, root_name):
    """(canonical ids, rule id, note). A DRR/film ann is one picture of one physical thing."""
    ann = ann or {}
    if ann.get("scheme") and ann.get("source_case"):
        return [f"ct:{ann['scheme']}/{ann['source_case']}"], "R1", ""
    pid = ann.get("patient_id")
    if pid:
        return [film_id(str(ann.get("source") or root_name), pid)], "R2", ""
    sf = ann.get("source_file") or ""
    m = RE_NH_PKL.match(os.path.basename(str(sf)))
    if m:
        return [f"film:nhanes/{m.group(1)}"], "R3a", f"source_file {os.path.basename(str(sf))}"
    return canon_from_case(case, root_name, str(ann.get("source") or ""))


def canon_from_case(case, root_name, source=""):
    """(canonical ids, rule id, note) from a case name alone -- every branch here is a naming convention.
    `source` is the ann's own source string when it has one; it is used only to decide which corpus a plain stem
    belongs to, never to invent an id."""
    m = RE_NH_CASE.match(case)
    if m:
        return [f"film:nhanes/{m.group(1)}"], "R3b", ""
    m = RE_TS.match(case)
    if m:
        return [f"ct:ts/{m.group(1)}"], "R4", ""
    m = RE_COLONOG.match(case)
    if m:
        return [f"ct:ctsp_colonog/{m.group(1)}"], "R5", ""
    if root_name.startswith("verse"):
        return [f"ct:verse/{case}"], "R6", ""
    # A DeepFluoro frame arriving through some other stage -- the vendor DICOMs, say -- must land on the SAME id as
    # the h5 subset in realxray/deepfluoro, or the aliased roots are two clean halves that are never compared.
    # Gated on the bank naming deepfluoro, because <nn>-<nnnn>_<k> is too plain a shape to claim on its own.
    if "deepfluoro" in (root_name + " " + source).lower():
        m = RE_DF_STEM.match(case)
        if m:
            return [f"frame:deepfluoro/{m.group(1)}/{m.group(2)}"], "R14", ""
    return [f"item:{root_name}/{case}"], "R7", "no rule matched this case name"


RE_NH_DIGITS = re.compile(r"(\d{4,6})$")


def canon_from_detector_stem(st, film_patients=None):
    """A detector image's stem. `film_patients` is the set of film ids the DRR film banks recorded; when the stem
    begins with one of them the id is that patient's, which is how a film in the detector corpus and the same film
    in a level bank become one item instead of two."""
    base = AUG_SUFFIX.sub("", st)
    if "_" not in base:
        return [f"item:detector/{base}"], "R7", "stem carries no <corpus>_ prefix"
    corpus, rest = base.split("_", 1)
    corpus = CORPUS_ALIAS.get(corpus, corpus)
    if corpus == "nhanes":
        m = RE_NH_DIGITS.search(rest)
        if m:
            return [f"film:nhanes/{m.group(1)}"], "R8a", ""
    cand = []
    for p in (film_patients or ()):
        pre = f"film:{corpus}/"
        if not p.startswith(pre):
            continue
        pid = p[len(pre):]
        if rest == pid or rest.startswith(pid + "-") or rest.startswith(pid + "_"):
            cand.append(pid)
    if cand:
        best = max(cand, key=len)
        if sum(1 for c in cand if len(c) == len(best)) == 1:
            return [f"film:{corpus}/{best}"], "R8b", ""
    return [f"film:{corpus}/{rest}"], "R8", ""


def ns_of(cid):
    return cid.split(":", 1)[0]


RE_D813_LINK = re.compile(r"^(COLONOG_[A-Za-z0-9.-]+)_0000\.nii\.gz$")


def load_ctsp_crosswalk(args):
    """{Dataset813 stem -> CTSpinoPelvic1K release id}, and where it came from.

    This is the ONLY statement on disk that ties `CTSP_COLONOG_<stem>` (ctsp_drr) to `ctsp_<release id>` (physics_drr),
    and it is not an identity: 801 of the 802 links disagree with the index, and 34 stems carry an accession instead
    of an index. Read exactly as tools/patient_keys.py reads it -- the link NAMES, never followed, because the targets
    are container paths that dangle on the host.
    """
    src = ""
    out = {}
    pk = getattr(args, "patient_keys", None)
    if pk:
        j = jload(os.path.expanduser(pk)) or {}
        for case, key in (j.get("keys") or {}).items():
            m = RE_COLONOG.match(str(case))
            if m and str(key).startswith("ctsp:"):
                out[m.group(1)] = str(key).split(":", 1)[1]
        if out:
            return out, f"{pk} (tools/patient_keys.py output, {len(out)} Dataset813 stems)"
    d813 = getattr(args, "d813", None)
    if d813:
        p = Path(os.path.expanduser(d813)) / "imagesTr"
        if p.is_dir():
            for f in sorted(p.iterdir()):
                m = RE_D813_LINK.match(f.name)
                if not m:
                    continue
                try:
                    tgt = os.readlink(f) if f.is_symlink() else ""
                except OSError:
                    tgt = ""
                mm = re.search(r"(\d{3,5})_ct\.nii\.gz$", str(tgt))
                if mm:
                    out[m.group(1)] = mm.group(1)
            src = f"{p} imagesTr symlink names ({len(out)} stems)"
    return out, src


# ---------------------------------------------------------------- the graph
class Lineage:
    def __init__(self, args):
        self.a = args
        self.nodes, self.edges, self.unresolved = {}, [], []
        self.rule_hits = Counter()
        self.case_index = {}          # DRR case name -> dict(canon, rule, node)
        self.node_canon = defaultdict(set)   # node id -> set of canonical ids
        self.leakage, self.models, self.shared = [], [], []
        self.aliases = [dict(a) for a in DECLARED_ALIASES]   # filled in as the scans learn their counts
        self.aug_stripped = 0
        self.node_unkeyed = Counter()   # items whose canonical id is just themselves (rule R7): a check over a node
                                        # with these is only as wide as the items that DID get an id
        self.collapse = set(x.strip() for x in (args.collapse or "").split(",") if x.strip())
        self.ledger = None            # {"by_path": {...}, "by_sha": {...}, ...}
        self.ctsp_cross, self.ctsp_cross_src = load_ctsp_crosswalk(args)
        self.ctsp_uncrossed = Counter()   # Dataset813 stems the crosswalk does not name
        self.ctsp_stems_seen = set()      # every Dataset813 stem met, before any collapse rewrote it
        self.ctsp_release_from_ann = set()   # release ids an ann itself stated (scheme ctsp + source_case), R1 only
        self.shared_truncated = 0
        if "ctsp" in self.collapse and not self.ctsp_cross:
            raise SystemExit(
                "--collapse ctsp needs the Dataset813 crosswalk, and none was found.\n"
                "  A COLONOG stem is NOT a release id: of the 802 imagesTr links only COLONOG_1 -> 0001 agrees,\n"
                "  COLONOG_100 is release 0145, and 34 stems are COLONOG_CTC-<accession> with no index at all.\n"
                "  Collapsing on the number would merge 528 pairs of DIFFERENT patients and miss every true pair.\n"
                "  Pass --d813 <Dataset813 root with imagesTr/> or --patient-keys <tools/patient_keys.py output>.")

    # -- structure
    def node(self, stage, name, path=None, present=True, **kw):
        nid = f"{stage}:{name}"
        n = self.nodes.setdefault(nid, dict(id=nid, stage=stage, name=name, path=disp(path), present=present,
                                            n_items=0, n_canonical=0, key_rule={}, by={}, examples=[], notes=[]))
        n.update({k: v for k, v in kw.items() if v is not None})
        return n

    def edge(self, src, dst, kind, n_items=None, evidence="", inferred=False, note=""):
        self.edges.append(dict(src=src, dst=dst, kind=kind, n_items=n_items, evidence=evidence,
                               inferred=bool(inferred), note=note))

    def unres(self, what, where, reason, n_items=None):
        self.unresolved.append(dict(what=what, where=disp(where), reason=reason, n_items=n_items))

    def add_item(self, nid, cids, rule):
        n = self.nodes[nid]
        n["n_items"] += 1
        n["key_rule"][rule] = n["key_rule"].get(rule, 0) + 1
        self.rule_hits[rule] += 1
        if rule == "R7":
            self.node_unkeyed[nid] += 1
        for c in cids:
            if c.startswith("ct:ctsp_colonog/"):
                self.ctsp_stems_seen.add(c.split("/", 1)[1])   # kept BEFORE the collapse, so the alias row can still
            if rule == "R1" and c.startswith("ct:ctsp/"):      # say how many stems there were once they are gone,
                self.ctsp_release_from_ann.add(c.split("/", 1)[1].zfill(4))   # and which release ids an ann stated
            self.node_canon[nid].add(self.apply_collapse(c))

    def apply_collapse(self, cid):
        """Optional, asked-for-by-name collapse of a CANDIDATE alias. Off by default, and recorded when on."""
        if "ctsp" in self.collapse and cid.startswith("ct:ctsp_colonog/"):
            stem = cid.split("/", 1)[1]
            rel = self.ctsp_cross.get(stem)
            if not rel:
                # NOT guessed from the number: a stem the crosswalk does not name stays its own item and is counted.
                self.ctsp_uncrossed[stem] += 1
                return cid
            return "ct:ctsp/" + rel.zfill(4)
        if "deepfluoro" in self.collapse and cid.startswith("pose:") and "/" in cid.split(":", 1)[1]:
            dev, rest = cid.split(":", 1)[1].split("/", 1)
            if RE_DF_STEM.match(rest.replace("/", "_")):
                return "frame:deepfluoro/" + rest
        return cid

    # -- ledger
    def load_ledger(self, path):
        rows = []
        try:
            if path.endswith(".jsonl"):
                rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
            else:
                obj = jload(path)
                if isinstance(obj, dict):
                    for k in ("items", "records", "entries", "files"):
                        if isinstance(obj.get(k), list):
                            rows = obj[k]; break
                    else:
                        rows = [v for v in obj.values() if isinstance(v, dict)]
                elif isinstance(obj, list):
                    rows = obj
        except Exception as e:  # noqa: BLE001
            self.unres("checksum ledger", path, f"could not be read: {type(e).__name__}")
            return
        if not rows:
            self.unres("checksum ledger", path, "no records found in any of items/records/entries/files")
            return
        pathk = ("path", "file", "abspath", "source_path", "filename")
        shak = ("sha256", "sha", "checksum", "hash", "md5")
        canonk = ("canonical_id", "canonical", "cid", "item_id", "key", "canonical_key")
        by_path, by_sha, used = {}, {}, Counter()
        for r in rows:
            if not isinstance(r, dict):
                continue
            c = next((str(r[k]) for k in canonk if r.get(k)), None)
            if not c:
                continue
            for k in pathk:
                if r.get(k):
                    by_path[norm_path(str(r[k]))] = c; used[k] += 1
            for k in shak:
                if r.get(k):
                    by_sha[str(r[k])] = c; used[k] += 1
        self.ledger = dict(path=path, records=len(rows), by_path=by_path, by_sha=by_sha,
                           fields_used=dict(used), joined=0, canonical_field=[k for k in canonk if any(k in r for r in rows[:50] if isinstance(r, dict))])
        print(f"ledger: {len(rows)} records, {len(by_path)} keyed by path, {len(by_sha)} by hash")

    def ledger_canon(self, path):
        if not self.ledger:
            return None
        c = self.ledger["by_path"].get(norm_path(path))
        if c:
            self.ledger["joined"] += 1
        return c

    # -- checks
    def split_check(self, nid, a_set, b_set, severity, explanation, side_a="train", side_b="val", namespace=None):
        """a_set/b_set are {canonical id}. One row per namespace, so a film leak is not hidden by a clean CT count."""
        rows = []
        spaces = sorted({ns_of(c) for c in set(a_set) | set(b_set)}) if namespace is None else [namespace]
        for ns in spaces:
            t = {c for c in a_set if ns_of(c) == ns}
            v = {c for c in b_set if ns_of(c) == ns}
            sh_ = sorted(t & v)
            rows.append(dict(check=f"{side_a} vs {side_b} disjointness by canonical id", node=nid, namespace=ns,
                             side_a=side_a, n_a=len(t), side_b=side_b, n_b=len(v),
                             n_shared=len(sh_), examples=sh_[:8], items_unkeyed=self.node_unkeyed.get(nid, 0),
                             severity=severity if sh_ else "clean", explanation=explanation))
        self.leakage.extend(rows)
        return rows


# ---------------------------------------------------------------- section: DRR / film banks
def scan_drr(L, home):
    roots = sorted(set(glob.glob(os.path.join(home, "*_drr")) + list(L.a.drr or [])))
    if not roots:
        L.unres("DRR banks", home, "no <home>/*_drr directory found")
        return
    for root in roots:
        name = os.path.basename(root)
        anns = sorted(glob.glob(os.path.join(root, "ann", "*.json")))
        nid = L.node("drr_bank", name, path=root, present=bool(anns))["id"]
        if not anns:
            L.unres("DRR bank items", root, "no ann/*.json on disk"); continue
        if L.a.max_items:
            anns = anns[:L.a.max_items]
        by_source, corpora = Counter(), Counter()
        for p in anns:
            ann = jload(p) or {}
            case = ann.get("case") or stem_of(p)
            lc = L.ledger_canon(p)
            if lc:
                cids, rule, note = [lc], "R13", ""
            else:
                cids, rule, note = canon_from_ann(case, ann, name)
            src = str(ann.get("source") or name)
            by_source[src] += 1
            for c in cids:
                corpora[":".join(c.split("/")[0:1])] += 1
            L.add_item(nid, cids, rule)
            coll = [L.apply_collapse(c) for c in cids]     # compare like with like: `canon` is stored collapsed, so
            prev = L.case_index.get(case)                  # comparing it against the raw ids made every repeated
            if prev and prev["canon"] != coll:             # case name look like a disagreement under --collapse
                L.unres("case name in two DRR banks with different canonical ids", case,
                        f"{prev['node']} says {prev['canon']}, {nid} says {coll}")
            L.case_index[case] = dict(canon=coll, rule=rule, node=nid, source=src)
            if note and len(L.nodes[nid]["notes"]) < 3:
                L.nodes[nid]["notes"].append(f"{case}: {note}")
        n = L.nodes[nid]
        n["by"] = dict(source=dict(by_source.most_common()))
        n["n_canonical"] = len(L.node_canon[nid])
        n["examples"] = sorted(L.node_canon[nid])[:5]
        for corpus in sorted(corpora):
            cn = L.node("corpus", corpus.replace(":", "/"), path=None)
            L.edge(cn["id"], nid, "derives", n_items=corpora[corpus],
                   evidence="ann fields (case/source/patient_id/scheme) of this bank", inferred=False)
        print(f"drr_bank {name:<18} {n['n_items']:>6} items  {n['n_canonical']:>6} canonical  "
              f"sources {dict(by_source.most_common(4))}")


# ---------------------------------------------------------------- section: context-crop banks
def npz_strings(path, keys=("case", "split", "source")):
    """Only the small string members of a bank npz; X is never decompressed."""
    try:
        import numpy as np
    except ImportError:
        return None, "numpy is not importable in this environment"
    try:
        with np.load(path, allow_pickle=False) as z:       # closed explicitly: 37 banks, 37 open zip handles
            out = {k: [str(v) for v in z[k]] for k in keys if k in z.files}
        return out, "" if out else "the npz holds none of case/split/source"
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {str(e)[:120]}"


def scan_crops(L, home):
    banks = sorted(set(glob.glob(os.path.join(home, "*_ctx")) + list(L.a.bank or [])))
    if not banks:
        L.unres("crop banks", home, "no <home>/*_ctx directory found")
        return
    for b in banks:
        name = os.path.basename(b)
        meta = jload(os.path.join(b, "meta.json"))
        nid = L.node("crop_bank", name, path=b, present=meta is not None)["id"]
        if meta is None:
            L.unres("crop bank meta", b, "meta.json missing or unreadable"); continue
        L.nodes[nid]["by"] = dict(classes=len(meta.get("classes") or []), rungs=meta.get("rungs"),
                                  size=meta.get("size"), tgt_px=meta.get("tgt_px"), mode=meta.get("mode"),
                                  val_cases=len(meta.get("val_cases") or []))
        for parent in meta.get("merged_from") or []:
            pn = L.node("crop_bank", os.path.basename(str(parent)), path=str(parent))
            L.edge(pn["id"], nid, "merges", n_items=None,
                   evidence=f"{os.path.join(b, 'meta.json')} field merged_from", inferred=False)
        rungs = sorted(glob.glob(os.path.join(b, "rung_*.npz")), key=lambda p: os.path.getsize(p))
        if L.a.rung:
            want = [p for p in rungs if stem_of(p) == f"rung_{L.a.rung}"]
            rungs = want or rungs
        if not rungs:
            L.unres("crop bank membership", b, "no rung_*.npz on disk; meta.json lists val_cases but not train cases",
                    n_items=len(meta.get("val_cases") or []))
            continue
        arrs, err = npz_strings(rungs[0])
        if not arrs or "case" not in arrs:
            L.unres("crop bank membership", rungs[0], err or "no case array"); continue
        cases, splits = arrs["case"], arrs.get("split", [])
        sources = arrs.get("source", [])
        if not splits:
            L.unres("crop bank split membership", rungs[0],
                    "the npz carries no `split` array, so train and val cannot be separated and this bank's "
                    "disjointness is NOT checked here", n_items=len(cases))
        L.nodes[nid]["notes"].append(f"membership read from {os.path.basename(rungs[0])} "
                                     f"({len(cases)} crops); other rungs hold the same cases by construction")
        per_split_cases = defaultdict(set)
        per_source = Counter()
        src_of_case = {}
        for i, c in enumerate(cases):
            sp = splits[i] if i < len(splits) else "?"
            per_split_cases[sp].add(c)
            if i < len(sources):
                per_source[sources[i]] += 1
                src_of_case[c] = sources[i]
        train_c, val_c = set(), set()
        n_unres = 0
        for c in set(cases):
            hit = L.case_index.get(c)
            if hit:
                cids, rule = hit["canon"], "R12"
            else:
                cids, rule, _ = canon_from_case(c, src_of_case.get(c, name))
                if rule == "R7":
                    n_unres += 1
            cids = [L.apply_collapse(x) for x in cids]
            L.add_item(nid, cids, rule)
            if c in per_split_cases.get("val", set()):
                val_c.update(cids)
            if c in per_split_cases.get("train", set()):
                train_c.update(cids)
        n = L.nodes[nid]
        n["n_canonical"] = len(L.node_canon[nid])
        n["by"].update(dict(crops=len(cases), cases=len(set(cases)),
                            crops_per_split={k: sum(1 for i, s in enumerate(splits) if s == k) for k in sorted(set(splits))},
                            cases_per_split={k: len(v) for k, v in sorted(per_split_cases.items())},
                            crops_per_source=dict(per_source.most_common())))
        n["examples"] = sorted(L.node_canon[nid])[:5]
        if n_unres:
            L.unres("crop-bank case not found in any DRR ann", b,
                    "the case is in the bank but no scanned <home>/*_drr/ann/*.json names it, so its canonical id "
                    "was made from the case name alone", n_items=n_unres)
        # bank <- source: the source string is either an ann's own source field (exact) or a DRR directory name
        for srcname in per_source:
            owners = sorted({v["node"] for v in L.case_index.values() if v["source"] == srcname})
            if owners:
                for o in owners:
                    L.edge(o, nid, "derives", n_items=per_source[srcname],
                           evidence=f"rung npz `source` array value {srcname!r} matches ann.source in {o}", inferred=False)
            elif f"drr_bank:{srcname}" in L.nodes:
                L.edge(f"drr_bank:{srcname}", nid, "derives", n_items=per_source[srcname],
                       evidence="the bank's `source` string equals a DRR directory basename; make_context_crops.py "
                                "sets source to the directory basename when the ann carries none", inferred=True)
            else:
                L.unres("crop-bank source has no directory on disk", f"{b} source={srcname}",
                        "no scanned DRR bank carries this source name and no <home>/" + srcname + " was scanned",
                        n_items=per_source[srcname])
        L.split_check(nid, train_c, val_c, "leak",
                      "a canonical id in both sides of this bank's split: the same physical thing was trained on "
                      "and validated on (the NHANES II defect of 2026-09-22)")
        sh_ = sum(r["n_shared"] for r in L.leakage if r["node"] == nid)
        print(f"crop_bank {name:<26} {len(set(cases)):>6} cases  {n['n_canonical']:>6} canonical  "
              f"train/val {len(train_c)}/{len(val_c)}  SHARED {sh_}")


# ---------------------------------------------------------------- section: detector datasets
def parse_data_yaml(p):
    """path/train/val/test only, scalars or [a, b, c]. A real yaml parser is not needed and is not imported."""
    out = {}
    try:
        txt = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return out
    for line in txt.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if k not in ("path", "train", "val", "test"):
            continue
        if v.startswith("[") and v.endswith("]"):
            out[k] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        elif v:
            out[k] = [v]
    return out


def list_images(d, cap=0):
    if not os.path.isdir(d):
        return []
    out = []
    with os.scandir(d) as it:
        for e in it:
            if e.is_file() and os.path.splitext(e.name)[1].lower() in (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"):
                out.append(e.name)
                if cap and len(out) >= cap:
                    break
    return sorted(out)


def scan_detector(L, home):
    yamls = sorted(glob.glob(os.path.join(home, "spine-detector", "data", "*", "data.yaml")))
    if not yamls:
        L.unres("detector datasets", os.path.join(home, "spine-detector", "data"), "no */data.yaml found")
        return
    owner_of_dir = {}
    for y in yamls:
        ds = os.path.basename(os.path.dirname(y))
        owner_of_dir[os.path.normpath(os.path.dirname(y))] = f"detector_dataset:{ds}"
    film_patients = {c for v in L.case_index.values() for c in v["canon"] if c.startswith("film:")}
    if not film_patients:
        L.unres("detector film identity", os.path.join(home, "spine-detector", "data"),
                "no film bank was scanned in this run, so a detector stem could not be matched to a patient id; "
                "its canonical id is the stem itself and cross-corpus duplication is not checked")
    for y in yamls:
        ds = os.path.basename(os.path.dirname(y))
        root = os.path.dirname(y)
        cfg = parse_data_yaml(y)
        nid = L.node("detector_dataset", ds, path=root)["id"]
        base = (cfg.get("path") or [root])[0]
        per_split, canon_split = {}, {}
        for split in ("train", "val", "test"):
            dirs = cfg.get(split) or []
            names, srcs = [], []
            for d in dirs:
                dd = d if os.path.isabs(d) else os.path.join(base, d)
                got = list_images(dd, L.a.max_items)
                names += got
                srcs.append(dict(dir=dd, n=len(got)))
                own = owner_of_dir.get(os.path.normpath(os.path.dirname(os.path.dirname(dd))))
                if own and own != nid:
                    L.edge(own, nid, "references", n_items=len(got),
                           evidence=f"{y} {split}: points at {dd}", inferred=False,
                           note=f"images of {own.split(':')[1]} are used as this dataset's {split}")
            per_split[split] = srcs
            cs = set()
            for nm in names:
                st = stem_of(nm)
                if AUG_SUFFIX.search(st):
                    L.aug_stripped += 1
                cids, rule, _ = canon_from_detector_stem(st, film_patients)
                cids = [L.apply_collapse(c) for c in cids]
                L.add_item(nid, cids, rule)
                cs.update(cids)
            canon_split[split] = cs
        n = L.nodes[nid]
        n["by"] = dict(splits={k: [dict(dir=s["dir"], n=s["n"]) for s in v] for k, v in per_split.items()},
                       canonical_per_split={k: len(v) for k, v in canon_split.items()})
        n["n_canonical"] = len(L.node_canon[nid])
        n["examples"] = sorted(L.node_canon[nid])[:5]
        L.split_check(nid, canon_split["train"], canon_split["val"], "leak",
                      "a film in both train and val of this detector dataset after augmentation suffixes are stripped")
        L.split_check(nid, canon_split["train"] | canon_split["val"], canon_split["test"], "leak",
                      "a film in both train+val and test of this detector dataset after augmentation suffixes are "
                      "stripped (a zoom crop of a test film is a test film)",
                      side_a="train+val", side_b="test")
        print(f"detector {ds:<16} " + "  ".join(f"{k} {len(v)}" for k, v in canon_split.items()))


# ---------------------------------------------------------------- section: device corpus
def scan_devcorpus(L, data):
    rroot = os.path.join(data, "devcorpus", "render")
    render_canon = {}      # render stem -> [canonical ids]
    for gdir in sorted(glob.glob(os.path.join(rroot, "*"))):
        if not os.path.isdir(gdir):
            continue
        geom = os.path.basename(gdir)
        nid = L.node("device_render", geom, path=gdir)["id"]
        files = sorted(p for p in glob.glob(os.path.join(gdir, "*.json")) if os.path.basename(p) != "RENDER_INFO.json")
        if L.a.max_items:
            files = files[:L.a.max_items]
        info = jload(os.path.join(gdir, "RENDER_INFO.json")) or {}
        subj_missing = 0
        for p in files:
            j = jload(p) or {}
            st = stem_of(p)
            cids = []
            if j.get("subject"):
                cids.append(f"ct:ts/{j['subject']}")
            if j.get("pose"):
                cids.append(f"pose:{geom}/{j['pose']}")
            if not cids:
                subj_missing += 1
                cids, rule, _ = [f"item:render_{geom}/{st}"], "R7", ""
            else:
                rule = "R9"
            cids = [L.apply_collapse(c) for c in cids]
            render_canon[st] = cids
            L.add_item(nid, cids, rule)
        n = L.nodes[nid]
        n["by"] = dict(render_info=info, json_files=len(files))
        n["n_canonical"] = len(L.node_canon[nid])
        n["examples"] = sorted(L.node_canon[nid])[:5]
        n["notes"].append("the render json names its subject as 's0224' and does not name the CT corpus; "
                          "'ct:ts/...' reads it as a TotalSegmentator subject, which RENDER_INFO's subject count "
                          "and ~/model_night/ts_clean_subjects.txt support but the file itself does not state")
        if subj_missing:
            L.unres("render json without subject/pose", gdir, "the json carries neither field", n_items=subj_missing)
        print(f"device_render {geom:<16} {len(files):>5} renders  {n['n_canonical']:>5} canonical")

    for sdir in sorted(glob.glob(os.path.join(data, "devcorpus", "styled", "*"))):
        if not os.path.isdir(sdir):
            continue
        name = os.path.basename(sdir)
        nid = L.node("device_styled", name, path=sdir)["id"]
        info = jload(os.path.join(sdir, "STYLE_INFO.json")) or {}
        geom = info.get("geometry") or name.split("__")[0]
        stems = sorted(render_canon) if render_canon else []
        by_split, unres_n = Counter(), 0
        canon_split = defaultdict(set)
        for split in ("train", "val"):
            for nm in list_images(os.path.join(sdir, "images", split), L.a.max_items):
                st = stem_of(nm)
                hit = None
                for k in range(len(st), 3, -1):     # longest prefix that IS a render stem
                    if st[:k] in render_canon:
                        hit = st[:k]; break
                if hit:
                    cids = render_canon[hit]; rule = "R10"
                else:
                    cids, rule, _ = [f"item:styled_{name}/{st}"], "R7", ""
                    unres_n += 1
                L.add_item(nid, cids, rule)
                canon_split[split].update(cids)
                by_split[split] += 1
        n = L.nodes[nid]
        n["by"] = dict(style_info=info, images_per_split=dict(by_split),
                       canonical_per_split={k: len(v) for k, v in canon_split.items()})
        n["n_canonical"] = len(L.node_canon[nid])
        if f"device_render:{geom}" in L.nodes:
            L.edge(f"device_render:{geom}", nid, "derives", n_items=sum(by_split.values()),
                   evidence="each styled stem begins with an existing render stem in devcorpus/render/" + geom,
                   inferred=False)
        else:
            L.unres("styled corpus geometry", sdir, f"no device_render node for geometry {geom!r}")
        if unres_n:
            L.unres("styled image with no matching render", sdir,
                    "no render json stem is a prefix of this image's stem", n_items=unres_n)
        L.split_check(nid, canon_split["train"], canon_split["val"], "leak",
                      "a CT subject or pose in both sides of this styled corpus's own split")
        print(f"device_styled {name:<30} {sum(by_split.values()):>5} images  {n['n_canonical']:>5} canonical")

    for ldir in sorted(glob.glob(os.path.join(data, "devcorpus", "lists", "*"))):
        if not os.path.isdir(ldir):
            continue
        name = os.path.basename(ldir)
        nid = L.node("device_list", name, path=ldir)["id"]
        info = jload(os.path.join(ldir, "LIST_INFO.json")) or {}
        canon_split, counts = defaultdict(set), {}
        for split in ("train", "val"):
            p = os.path.join(ldir, f"{split}.txt")
            lines = []
            if os.path.exists(p):
                lines = [l.strip() for l in open(p, encoding="utf-8", errors="replace") if l.strip()]
            counts[split] = len(lines)
            miss = 0
            for ln in lines:
                st = stem_of(ln)
                hit = None
                for k in range(len(st), 3, -1):
                    if st[:k] in render_canon:
                        hit = st[:k]; break
                if hit:
                    canon_split[split].update(render_canon[hit]); rule = "R10"
                else:
                    miss += 1; rule = "R7"
                L.add_item(nid, render_canon.get(hit, [f"item:list_{name}/{st}"]), rule)
                sc = os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname(ln))))
                sn = f"device_styled:{os.path.basename(sc)}"
                if sn in L.nodes and not any(e["src"] == sn and e["dst"] == nid for e in L.edges):
                    L.edge(sn, nid, "derives", n_items=None,
                           evidence=f"{p} lists images under {sc}", inferred=False)
            if miss:
                L.unres("list entry with no matching render", p,
                        "the listed image's stem matches no render json stem", n_items=miss)
        n = L.nodes[nid]
        n["by"] = dict(list_info=info, lines=counts,
                       canonical_per_split={k: len(v) for k, v in canon_split.items()})
        n["n_canonical"] = len(L.node_canon[nid])
        L.split_check(nid, canon_split["train"], canon_split["val"], "by design",
                      "these arms hold a DEVICE out, not a subject: a canonical CT subject on both sides is the "
                      "design when the styled corpora share a subject split, and a leak only if the arm is read as "
                      "subject-held-out. The pose namespace is the one that must stay disjoint for a device claim")
        print(f"device_list {name:<40} train {counts.get('train', 0)} / val {counts.get('val', 0)}")


# ---------------------------------------------------------------- section: real frames
def realxray_root_bank(ds, _cache={}):
    """The independent bank a realxray directory is a second rendering of, from tools/realxray_banks.json.

    cobra_elekta_v2 (re-windowed), cobra_elekta_ap45 and cobra_elekta_v2_ap45 (symlink view subsets) hold the same
    exposures of the same 145 patients as cobra_elekta, and each ships its own meta/*.json. Keyed by directory
    name, one COBRA frame would become four canonical real frames here and COBRA would count 10,228 real frames
    instead of 3,480. Same root cause as the training-list defect (docs/DATA_COMPLETENESS_AUDIT.md Repairs
    2026-09-23); same registry, so there is one place that says what a bank is.
    """
    if not _cache:
        try:
            _cache.update(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "realxray_banks.json")))["banks"])
        except Exception:  # noqa: BLE001
            _cache["_"] = {}
    seen = set()
    while ds not in seen:
        seen.add(ds)
        parent = (_cache.get(ds) or {}).get("derived_of")
        if not parent:
            return ds
        ds = parent
    return ds


def scan_realxray(L, data):
    roots = sorted(glob.glob(os.path.join(data, "realxray", "*")))
    df_frames = 0
    for r in roots:
        if not os.path.isdir(r):
            continue
        ds = os.path.basename(r)
        root_ds = realxray_root_bank(ds)
        sp = jload(os.path.join(r, "splits.json"))
        metas = sorted(glob.glob(os.path.join(r, "meta", "*.json")))
        nid = L.node("real_frames", ds, path=r, present=bool(metas or sp),
                     root_bank=root_ds, derived=(root_ds != ds))["id"]
        if not metas:
            L.unres("real frame membership", r, "no meta/*.json on disk"); continue
        if L.a.max_items:
            metas = metas[:L.a.max_items]
        canon_split, cases_split = defaultdict(set), defaultdict(set)
        for p in metas:
            m = jload(p) or {}
            st = m.get("stem") or stem_of(p)
            case = str(m.get("case") or st)
            split = str(m.get("split") or "?")
            cid = f"frame:{root_ds}/{case}/{st}"   # root_ds, not ds: a re-display is not a second exposure
            if root_ds == "deepfluoro":
                mm = RE_DF_STEM.match(st)
                if mm:
                    cid = f"frame:deepfluoro/{mm.group(1)}/{mm.group(2)}"
                    df_frames += 1
            cid = L.apply_collapse(cid)
            L.add_item(nid, [cid], "R11")
            canon_split[split].add(cid)
            cases_split[split].add(case)
        n = L.nodes[nid]
        n["by"] = dict(frames_per_split={k: len(v) for k, v in sorted(canon_split.items())},
                       cases_per_split={k: len(v) for k, v in sorted(cases_split.items())},
                       splits_json=({k: len(v) for k, v in sp.items() if isinstance(v, list)} if isinstance(sp, dict) else None))
        n["n_canonical"] = len(L.node_canon[nid])
        n["examples"] = sorted(L.node_canon[nid])[:5]
        tr = cases_split.get("train", set()) | cases_split.get("val", set())
        te = cases_split.get("test", set())
        L.leakage.append(dict(check="train+val vs test disjointness by case", node=nid, namespace="case",
                              side_a="train+val", n_a=len(tr), side_b="test", n_b=len(te),
                              n_shared=len(tr & te), examples=sorted(tr & te)[:8],
                              severity="leak" if tr & te else "clean",
                              explanation="a case (specimen or patient) on both sides of the fixed split, read from "
                                          "the per-frame meta files"))
        print(f"real_frames {ds:<22} {n['n_items']:>5} frames  splits {n['by']['cases_per_split']}")
    # the pose/frame alias, checked rather than asserted
    pf = os.path.join(data, "devcorpus", "poses", "cios_fusion.json")
    npz = jload(pf, cap=512 << 20)
    npose = (npz or {}).get("n")
    for al in L.aliases:
        if al["group"] == "deepfluoro_pose_vs_frame":
            al["evidence"] += f"; poses n={npose}, DeepFluoro frames on disk={df_frames}"
            if npose is None:
                # nothing was measured: saying "counts differ" here would state a comparison that never happened
                al["status"] = "candidate (pose pool not read)"
                al["evidence"] += f" -- {pf} is missing or unreadable, so the counts were never compared"
            elif "deepfluoro" in L.collapse:
                # the collapse is applied during the scan, BEFORE this count exists, so it is recorded either way
                al["status"] = "collapsed" if npose == df_frames else "collapsed DESPITE disagreeing counts"
            else:
                al["status"] = "candidate (counts agree)" if npose == df_frames else "candidate (counts differ)"
            al["n_items"] = df_frames
            if "deepfluoro" in L.collapse and npose != df_frames:
                L.unres("pose <-> real frame collapse", pf,
                        f"--collapse deepfluoro rewrote every pose id into a DeepFluoro frame id during the scan, "
                        f"before the counts were read; they do not agree ({npose} poses, {df_frames} frames), so "
                        "every count in this document that touches a pose rests on an unverified equality")
    if npose is not None and df_frames and npose != df_frames:
        L.unres("pose <-> real frame identity", pf,
                f"the pose pool holds {npose} poses and realxray/deepfluoro holds {df_frames} frames; the pose "
                "string is <specimen>/<index> but nothing on disk states it is that frame's registered pose")


# ---------------------------------------------------------------- section: models
def scan_models(L, home):
    p = L.a.registry or os.path.join(home, "model_registry", "registry.jsonl")
    if not os.path.exists(p):
        L.unres("model registry", p, "registry.jsonl not on disk; no model -> bank edge can be made")
        return
    rows = []
    for line in open(p, encoding="utf-8", errors="replace"):
        try:
            rows.append(json.loads(line))
        except Exception:  # noqa: BLE001
            pass
    for r in rows:
        name = r.get("name", "?")
        nid = L.node("model", f"{name}@{str(r.get('sha', ''))[:8]}", path=r.get("store_path"),
                     n_items=1, by=dict(stage=r.get("stage"), ts=r.get("ts"), git=r.get("git"),
                                        metrics=r.get("metrics"), source_path=r.get("source_path")))["id"]
        bank = str(r.get("bank") or "")
        rec = dict(name=name, sha=r.get("sha"), stage=r.get("stage"), bank=bank, bank_node=None,
                   train=None, eval=None, overlap=None, unresolved=[])
        if not bank:
            rec["unresolved"].append("the registry entry names no bank, so nothing on disk says what this model saw")
            L.unres("model training set", nid, "registry entry has an empty `bank` field")
        else:
            bn = f"crop_bank:{os.path.basename(bank.rstrip('/'))}"
            if bn in L.nodes:
                rec["bank_node"] = bn
                L.edge(bn, nid, "trained_on", n_items=L.nodes[bn]["n_canonical"],
                       evidence=f"{p}: entry {name} field bank={bank}", inferred=False)
                rows_for = [x for x in L.leakage if x["node"] == bn and x["side_a"] == "train"]
                tr = sum(x["n_a"] for x in rows_for); va = sum(x["n_b"] for x in rows_for)
                shd = sum(x["n_shared"] for x in rows_for)
                ex = [e for x in rows_for for e in x["examples"]][:8]
                rec["train"] = dict(n_canonical=tr, source="the bank's train split")
                rec["eval"] = dict(n_canonical=va, source="the bank's val split (what the trainer scores on)",
                                   inferred=True)
                rec["overlap"] = dict(n_canonical_shared=shd, examples=ex)
                L.nodes[nid]["n_canonical"] = tr + va
                if shd:
                    L.leakage.append(dict(check="model train vs eval by canonical id", node=nid, namespace="all",
                                          side_a="train", n_a=tr, side_b="eval", n_b=va,
                                          n_shared=shd, examples=ex, severity="leak",
                                          explanation=f"inherited from {bn}: this model was validated on physical "
                                                      "items it was also trained on"))
            else:
                rec["unresolved"].append(f"bank {bank} was not scanned (not under the scanned home), so the model's "
                                         "items are unknown")
                L.unres("model training set", nid, f"bank path {bank} has no scanned crop_bank node")
        rec["unresolved"].append("evaluation outside the bank's own val split (or_ready result files) is not linked: "
                                 "the result JSONs do not name the weight file they scored")
        L.models.append(rec)
    print(f"models: {len(rows)} registry entries, "
          f"{sum(1 for m in L.models if m['bank_node'])} linked to a scanned bank")


# ---------------------------------------------------------------- section: results
def scan_orready(L, data):
    root = os.path.join(data, "or_ready")
    if not os.path.isdir(root):
        L.unres("result files", root, "or_ready is not on disk here")
        return
    keys = ("cases", "test", "val", "train", "specimens", "subjects", "held", "val_cases", "test_cases")
    for d in sorted(glob.glob(os.path.join(root, "*"))):
        if not os.path.isdir(d):
            continue
        name = os.path.basename(d)
        allf = sorted(glob.glob(os.path.join(d, "*.json")))
        cap = L.a.max_items or L.a.max_results
        files = allf[:cap] if cap else allf
        nid = L.node("results", name, path=d, n_items=len(files))["id"]
        if len(files) < len(allf):      # a silent cap makes an accounting file wrong without saying so
            L.unres("result files beyond the cap", d,
                    f"{len(allf)} result JSONs are on disk and only the first {len(files)} were read "
                    f"(--max-results {cap}); this node's counts are partial", n_items=len(allf) - len(files))
        named = {}
        for f in files:
            j = jload(f, cap=4 << 20)
            if isinstance(j, dict):
                got = {k: len(v) for k, v in j.items() if k in keys and isinstance(v, list)}
                if got:
                    named[os.path.basename(f)] = got
        L.nodes[nid]["by"] = dict(json_files=len(files), files_naming_items=named)
        if files and not named:
            L.unres("evaluation membership of a result directory", d,
                    "no result JSON here carries a top-level list of cases/subjects, so which items were scored "
                    "cannot be read from the result itself", n_items=len(files))
    print(f"results: {sum(1 for n in L.nodes.values() if n['stage'] == 'results')} or_ready directories")


# ---------------------------------------------------------------- shared-item table
def build_shared(L, cap=400):
    owners = defaultdict(set)
    for nid, cs in L.node_canon.items():
        for c in cs:
            owners[c].add(nid)
    pair = Counter()
    ex = defaultdict(list)
    for c, ns in owners.items():
        if len(ns) < 2:
            continue
        ns = sorted(ns)
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                k = (ns[i], ns[j], ns_of(c))
                pair[k] += 1
                if len(ex[k]) < 5:
                    ex[k].append(c)
    for (a, b, nsp), n in pair.most_common(cap):
        L.shared.append(dict(a=a, b=b, namespace=nsp, n_shared=n, examples=ex[(a, b, nsp)]))
    if len(pair) > cap:      # anything drawn from `shared` would otherwise under-report without saying so
        L.shared_truncated = len(pair) - cap
        L.unres("node pairs sharing a canonical item, beyond the table's cap", "shared[]",
                f"{len(pair)} node pairs share at least one item and only the {cap} largest are listed; a figure "
                "drawn from this table is missing the rest", n_items=len(pair) - cap)
    return len(owners)


# ---------------------------------------------------------------- aliases
def finalise(L):
    """Fill the abstract corpus nodes from the ids that actually appeared, and count DISTINCT ids per namespace
    (summing per-node counts would count one patient once per stage it passed through)."""
    all_ids = set()
    for cs in L.node_canon.values():
        all_ids |= cs
    for n in list(L.nodes.values()):
        if n["stage"] != "corpus":
            continue
        pre = n["name"].replace("/", ":", 1) + "/"
        ids = {c for c in all_ids if c.startswith(pre)}
        n["n_canonical"] = len(ids)
        n["n_items"] = sum(e["n_items"] or 0 for e in L.edges if e["src"] == n["id"])
        n["examples"] = sorted(ids)[:5]
        if n["n_items"] and not ids and L.collapse:
            # otherwise the row reads "4 items, 0 canonical", which looks like items that named nothing
            n["notes"].append("every id of this corpus was rewritten into another corpus by --collapse "
                              f"{','.join(sorted(L.collapse))}; the items are counted under that one")
    return Counter(ns_of(c) for c in all_ids), len(all_ids)


def check_aliases(L, data):
    for al in L.aliases:
        if al["group"] == "yolo_v4z_zoom_crops":
            al["n_items"] = L.aug_stripped
            al["evidence"] += f"; {L.aug_stripped} detector images carried such a suffix and were folded into their film"
        if al["group"] == "nhanes_two_directories":
            ids = {c for cs in L.node_canon.values() for c in cs if c.startswith("film:nhanes/")}
            al["n_items"] = len(ids)
            al["evidence"] += f"; {len(ids)} distinct NHANES patients after collapsing"
        if al["group"] == "ctsp_colonog_vs_ctsp":
            # Both sides are recorded pre-collapse, so this row reads the same whether or not --collapse ran, and
            # the release ids counted are only those an ann itself stated (R1) -- never ones the collapse created.
            a = set(L.ctsp_stems_seen)
            b = set(L.ctsp_release_from_ann)
            # The overlap is counted THROUGH THE CROSSWALK or not at all. Counting stems whose number happens to be
            # a release id counts a coincidence of numbering: 767 of the 768 numeric stems name a different patient
            # than their own number does, so that count was right-looking and meaningless.
            if L.ctsp_cross:
                uncrossed = {x for x in a if x not in L.ctsp_cross}
                mapped = {L.ctsp_cross[x].zfill(4) for x in a - uncrossed}
                both = mapped & b
                al["n_items"] = len(both)
                al["status"] = "collapsed" if "ctsp" in L.collapse else "candidate (crosswalk read, not applied)"
                al["evidence"] += (f"; crosswalk from {L.ctsp_cross_src}; Dataset813 stems present {len(a)}, named by "
                                   f"the crosswalk {len(a) - len(uncrossed)}, scheme-ctsp source_cases present "
                                   f"{len(b)}, SAME PATIENT under both namings {len(both)}, stems the crosswalk does "
                                   f"not name {len(uncrossed)}")
            else:
                both = set()
                al["n_items"] = None
                al["evidence"] += (f"; Dataset813 stems present {len(a)}, scheme-ctsp source_cases present {len(b)}, "
                                   "overlap NOT COUNTED: it cannot be read off the names, and counting stems whose "
                                   "index happens to equal a release id would count a coincidence of numbering "
                                   "(only 1 of the 802 links agrees with its index). Pass --d813 or --patient-keys")
            if a and b and not L.ctsp_cross:
                L.unres("CTSpinoPelvic1K release id behind a Dataset813 stem", "ctsp_drr vs physics_drr",
                        "no --d813 / --patient-keys was given, so the two namings of CTSpinoPelvic1K were treated as "
                        "different corpora and the leak measured at 357 people in docs/SPLIT_LEAK_CROSS_NAMING_"
                        "2026-09-22.md is NOT checked by this run", n_items=len(a))
            if both and "ctsp" not in L.collapse:
                L.leakage.append(dict(check="candidate alias not collapsed", node="corpus:ct/ctsp_colonog",
                                      namespace="ct", side_a="Dataset813 stems", n_a=len(a),
                                      side_b="scheme-ctsp source_cases", n_b=len(b), n_shared=len(both),
                                      examples=sorted(both)[:8], severity="candidate",
                                      explanation="ctsp_drr (CTSP_<stem>) and physics_drr (scheme ctsp, source_case "
                                                  "<nnnn>) are two namings of CTSpinoPelvic1K, and the Dataset813 "
                                                  "imagesTr crosswalk says these patients are under both. A bank "
                                                  "holding both split them independently, as NHANES was "
                                                  "(docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md). --collapse ctsp "
                                                  "recomputes every count with them as one person"))
        if al["group"] == "deepfluoro_h5_vs_vendor":
            vend = os.path.join(data, "deepfluoro_vendor", "unpacked")
            # A path test alone is nearly inert: a bank BUILT from the vendor root sits under <home>/*_drr and its
            # path never names the vendor. So the ann's own `source` string is read too -- that is what a bank drawn
            # from the vendor DICOMs actually records.
            used = [n["id"] for n in L.nodes.values() if n.get("path") and os.path.normpath(vend) in os.path.normpath(str(n["path"]))]
            by_src = sorted({n["id"] for n in L.nodes.values()
                             for s in ((n.get("by") or {}).get("source") or {})
                             if "deepfluoro_vendor" in str(s)})
            used = sorted(set(used) | set(by_src))
            al["n_items"] = len(used)
            al["evidence"] += ("; no scanned stage names the vendor root, by path or by ann.source" if not used else
                               f"; ALSO CONSUMED BY {used}")
            if used:
                L.leakage.append(dict(check="aliased dataset consumed twice", node=",".join(used), namespace="frame",
                                      side_a="deepfluoro_h5", n_a=0, side_b="deepfluoro_vendor", n_b=0,
                                      n_shared=len(used), examples=used, severity="leak",
                                      explanation="the vendor DICOMs and the JHU h5 hold the same frames; a stage "
                                                  "drawing from both counts them twice"))


# ---------------------------------------------------------------- markdown
def cell(x):
    """A markdown table cell: a pipe inside a rule description must not start a new column."""
    return str(x).replace("|", r"\|").replace("\n", " ")


def rule_key(k):
    m = re.match(r"R(\d+)([a-z]*)", k)
    return (int(m.group(1)), m.group(2)) if m else (99, k)


def to_markdown(doc):
    o = []
    A = o.append
    A(f"# Data lineage ({doc['schema']})")
    A("")
    A(f"Built {doc['built']} on {doc['host']} at commit `{doc['git'] or '?'}`.")
    A(f"Roots: home `{doc['roots']['home']}`, data `{doc['roots']['data']}`. Sections: {', '.join(doc['roots']['sections'])}.")
    led = doc.get("ledger")
    A(f"Checksum ledger: `{led['path']}` ({led['records']} records, {led['joined']} items joined)." if led else
      "Checksum ledger: none given, so every canonical id here came from a field or a naming rule, not a hash.")
    A("")
    A("## Stages")
    A("")
    A("| stage | dataset | items | canonical items | rules used | derived from |")
    A("|---|---|---:|---:|---|---|")
    froms = defaultdict(list)
    for e in doc["edges"]:
        if e["kind"] in ("derives", "merges", "references", "trained_on"):
            froms[e["dst"]].append(e["src"].split(":", 1)[1] + ("*" if e["inferred"] else ""))
    for n in sorted(doc["nodes"], key=lambda x: (x["stage"], x["name"])):
        rules = ", ".join(f"{k}:{v}" for k, v in sorted(n["key_rule"].items(), key=lambda kv: rule_key(kv[0])))
        src = ", ".join(sorted(set(froms.get(n["id"], [])))[:6]) or "-"
        A(f"| {n['stage']} | {cell(n['name'])} | {n['n_items']} | {n['n_canonical']} | {rules or '-'} | {cell(src)} |")
    A("")
    A("`*` on a source means the edge was established by a naming convention, not by a field on disk.")
    A("")
    A("## Canonical-id rules")
    A("")
    A("| rule | what it does | basis | inferred | items |")
    A("|---|---|---|---|---:|")
    for k in sorted(doc["rules"], key=rule_key):
        v = doc["rules"][k]
        A(f"| {k} | {cell(v['what'])} | {v['basis']} | {'yes' if v['inferred'] else 'no'} | {v.get('n_items', 0)} |")
    A("")
    A("## Split disjointness, by canonical id")
    A("")
    A("| check | node | namespace | side a | n a | side b | n b | shared | unkeyed | severity |")
    A("|---|---|---|---|---:|---|---:|---:|---:|---|")
    for r in sorted(doc["leakage"], key=lambda x: (-x["n_shared"], x["node"])):
        if r["severity"] == "clean" and not r["n_shared"] and not r.get("items_unkeyed"):
            continue
        A(f"| {cell(r['check'])} | {cell(r['node'])} | {r['namespace']} | {r['side_a']} | {r['n_a']} | "
          f"{r['side_b']} | {r['n_b']} | {r['n_shared']} | {r.get('items_unkeyed', 0)} | {r['severity']} |")
    A("")
    A("`unkeyed` counts items of that node whose canonical id is the item itself, because no rule and no ledger "
      "record named the thing behind it. A check is only as wide as the items it could key.")
    nclean = sum(1 for r in doc["leakage"] if r["severity"] == "clean")
    A("")
    A(f"{nclean} further checks came back clean (shared = 0); they are in the JSON.")
    A("")
    A("## Aliases")
    A("")
    A("| group | status | members | items | evidence |")
    A("|---|---|---|---:|---|")
    for a in doc["aliases"]:
        A(f"| {a['group']} | {a['status']} | {cell(' + '.join(a['members']))} | "
          f"{a.get('n_items') if a.get('n_items') is not None else '-'} | {cell(a['evidence'])} |")
    A("")
    A("## Unresolved")
    A("")
    A("| what | where | why | items |")
    A("|---|---|---|---:|")
    for u in doc["unresolved"]:
        A(f"| {cell(u['what'])} | `{cell(u['where'])}` | {cell(u['reason'])} | "
          f"{u.get('n_items') if u.get('n_items') is not None else '-'} |")
    A("")
    A("## Items held by two nodes at once")
    A("")
    A("| a | b | namespace | shared canonical items |")
    A("|---|---|---|---:|")
    for s in doc["shared"][:60]:
        A(f"| {s['a']} | {s['b']} | {s['namespace']} | {s['n_shared']} |")
    A("")
    A("## The pathway")
    A("")
    A("```mermaid")
    A("graph LR")
    seen = set()
    for e in doc["edges"]:
        if e["kind"] not in ("derives", "merges", "references", "trained_on"):
            continue
        k = (e["src"], e["dst"])
        if k in seen:
            continue
        seen.add(k)
        if len(seen) > 120:
            A("  more[more edges in lineage.json]")
            break
        lab = e["kind"] + (f" {e['n_items']}" if e.get("n_items") else "") + ("*" if e["inferred"] else "")
        A(f'  {mermaid_id(e["src"])}["{e["src"]}"] -->|{lab}| {mermaid_id(e["dst"])}["{e["dst"]}"]')
    A("```")
    A("")
    return "\n".join(o)


def mermaid_id(nid):
    return re.sub(r"[^A-Za-z0-9]", "_", nid)


# ---------------------------------------------------------------- commands
def cmd_build(a):
    out = Path(a.out)
    if out.exists():          # checked BEFORE the scan: a grid run is minutes long and must not die at the end
        old = jload(str(out))
        if not (isinstance(old, dict) and old.get("schema") == SCHEMA):
            raise SystemExit(f"refusing to overwrite {out}: it is not a {SCHEMA!r} document "
                             f"(schema {(old or {}).get('schema') if isinstance(old, dict) else 'not json'!r})")
    md_out = out.with_suffix(".md")
    if md_out.exists():       # the .md is written from the .json's stem, so --out docs/<anything>.json would
        head = ""             # silently destroy docs/<anything>.md -- a file this tool never wrote
        try:
            head = md_out.read_text(encoding="utf-8", errors="replace")[:200]
        except OSError:
            head = ""
        if not head.startswith(f"# Data lineage ({SCHEMA})"):
            raise SystemExit(f"refusing to overwrite {md_out}: it is not a {SCHEMA} markdown report, and the "
                             f"markdown is written from --out's stem. Choose another --out.")
    L = Lineage(a)
    home = os.path.expanduser(a.home)
    data = os.path.expanduser(a.data)
    sections = [s.strip() for s in a.sections.split(",") if s.strip()]
    if a.ledger:
        L.load_ledger(os.path.expanduser(a.ledger))
    else:
        print("no --ledger given: canonical ids will come from recorded fields and naming rules only")
    if a.max_items:
        L.unres("every count in this document", "--max-items " + str(a.max_items),
                "the run was capped at that many items per node, so counts are partial and a disjointness check "
                "that came back clean saw only the first items of each node", n_items=a.max_items)
        print(f"WARNING: --max-items {a.max_items} is in force; this is a smoke run, not an audit")
    t0 = time.time()
    if "drr" in sections:
        scan_drr(L, home)
    if "crops" in sections:
        scan_crops(L, home)
    if "detector" in sections:
        scan_detector(L, home)
    if "devcorpus" in sections:
        scan_devcorpus(L, data)
    if "realxray" in sections:
        scan_realxray(L, data)
    if "models" in sections:
        scan_models(L, home)
    if "results" in sections:
        scan_orready(L, data)
    if L.ledger:
        # Say plainly how far the ledger actually reached. It is consulted in ONE place (the DRR/film anns), and
        # only by path -- the hash index is built and not read. Without this the output shows hash fields in
        # `fields_used` and reads as though checksums keyed the graph.
        if L.ledger["by_sha"]:
            L.unres("checksum ledger hash index", L.ledger["path"],
                    f"{len(L.ledger['by_sha'])} records carry a hash, but no stage looks an item up by hash: the "
                    "join is by file path only, so identical bytes under two paths are still two items here "
                    "(that is tools/or_audit_dupes.py's question)", n_items=len(L.ledger["by_sha"]))
        L.unres("checksum ledger coverage", L.ledger["path"],
                f"the ledger is consulted for DRR/film ann files only ({L.ledger['joined']} joined); crop banks, "
                "detector datasets, device renders, styled images, real frames and results were keyed by rule, not "
                "by the ledger", n_items=L.ledger["records"])
    check_aliases(L, data)
    if L.ctsp_uncrossed:
        L.unres("Dataset813 stem with no crosswalk entry", "--collapse ctsp",
                f"{len(L.ctsp_uncrossed)} stem(s) are not named by the crosswalk and were left uncollapsed rather "
                f"than guessed: {sorted(L.ctsp_uncrossed)[:5]}", n_items=len(L.ctsp_uncrossed))
    build_shared(L)
    ns_counts, n_canon = finalise(L)
    rules = {k: dict(v, n_items=L.rule_hits.get(k, 0)) for k, v in RULES.items()}
    doc = dict(schema=SCHEMA, schema_doc=SCHEMA_DOC, built=time.strftime("%Y-%m-%d %H:%M"),
               host=platform.node(), git=sh(["git", "-C", str(Path(__file__).resolve().parents[1]), "rev-parse", "--short", "HEAD"]),
               argv=sys.argv, roots=dict(home=home, data=data, sections=sections,
                                         collapsed=sorted(L.collapse)),
               ledger=({k: v for k, v in L.ledger.items() if k not in ("by_path", "by_sha")} if L.ledger else None),
               rules=rules, nodes=sorted(L.nodes.values(), key=lambda n: (n["stage"], n["name"])),
               edges=L.edges, models=L.models, leakage=L.leakage, aliases=L.aliases, shared=L.shared,
               unresolved=L.unresolved,
               totals=dict(nodes=len(L.nodes), edges=len(L.edges), canonical_items=n_canon,
                           by_namespace=dict(ns_counts.most_common()),
                           items=sum(n["n_items"] for n in L.nodes.values()),
                           leaks=sum(1 for r in L.leakage if r["severity"] == "leak" and r["n_shared"]),
                           unresolved=len(L.unresolved)))
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(doc, open(out, "w", encoding="utf-8"), indent=1)
    md = md_out
    md.write_text(to_markdown(doc), encoding="utf-8")
    print(f"\n{len(L.nodes)} nodes, {len(L.edges)} edges, {n_canon} canonical items "
          f"({', '.join(f'{k} {v}' for k, v in ns_counts.most_common())})")
    print(f"leaks {doc['totals']['leaks']}   unresolved {len(L.unresolved)}   "
          f"unkeyed items {sum(L.node_unkeyed.values())}   {time.time() - t0:.1f} s")
    if L.unresolved or sum(L.node_unkeyed.values()):
        # printed whether or not something leaked: a run that finds one leak still has to say what it did not check
        lead = ("no leak was found, and that covers only what could be keyed" if not doc["totals"]["leaks"] else
                f"{doc['totals']['leaks']} leak row(s) above, and what was checked covers only what could be keyed")
        print(f"NOTE: {lead} -- {len(L.unresolved)} link(s) unresolved, "
              f"{sum(L.node_unkeyed.values())} item(s) with no canonical id. "
              "Read the unresolved table before calling anything clean.")
    print(f"wrote {out}\nwrote {md}")
    return 1 if (a.strict and doc["totals"]["leaks"]) else 0


def cmd_check(a):
    doc = jload(a.lineage)
    if not doc or doc.get("schema") != SCHEMA:
        raise SystemExit(f"{a.lineage} is not a {SCHEMA} document")
    bad = 0
    for r in doc["leakage"]:
        if r["n_shared"] and r["severity"] in ("leak",):
            bad += 1
            print(f"LEAK  {r['node']:<40} {r['namespace']:<6} {r['n_shared']:>5} shared  {r['check']}")
            print(f"      {', '.join(r['examples'][:5])}")
        elif r["n_shared"] and r["severity"] != "clean":
            print(f"{r['severity'].upper():<10} {r['node']:<36} {r['namespace']:<6} {r['n_shared']:>5}  {r['check']}")
    for u in doc["unresolved"]:
        print(f"unresolved  {u['what']} @ {u['where']}: {u['reason']}")
    unkeyed = max([r.get("items_unkeyed", 0) for r in doc["leakage"]] or [0])
    print(f"\n{bad} leak row(s), {len(doc['unresolved'])} unresolved link(s), "
          f"worst node carries {unkeyed} item(s) with no canonical id")
    if not bad:
        print("no leak among the items that could be keyed; the unresolved rows above are what this did NOT check")
    return 1 if bad else 0


def cmd_show(a):
    doc = jload(a.lineage)
    if not doc or doc.get("schema") != SCHEMA:
        raise SystemExit(f"{a.lineage} is not a {SCHEMA} document")
    print(to_markdown(doc))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="scan the roots and write lineage.json + lineage.md")
    b.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "docs" / "lineage.json"))
    b.add_argument("--home", default=os.path.expanduser("~"), help="the root holding *_drr, *_ctx, spine-detector, model_registry")
    b.add_argument("--data", default="/rs/rs_grp_oschome/go2432/data", help="the CephFS root holding devcorpus, realxray, or_ready")
    b.add_argument("--ledger", default=None, help="checksum ledger to join canonical ids from (json or jsonl)")
    b.add_argument("--sections", default="drr,crops,detector,devcorpus,realxray,models,results")
    b.add_argument("--drr", action="append", default=[], help="an extra DRR directory to scan")
    b.add_argument("--bank", action="append", default=[], help="an extra crop bank to scan")
    b.add_argument("--registry", default=None, help="model registry jsonl (default <home>/model_registry/registry.jsonl)")
    b.add_argument("--rung", default=None, help="which rung npz to read membership from (default: the smallest)")
    b.add_argument("--max-items", type=int, default=0, help="cap items per node (smoke runs only; counts are then partial)")
    b.add_argument("--max-results", type=int, default=200, help="cap on result JSONs read per or_ready directory "
                                                                "(0 = all); a cap that bites is recorded as unresolved")
    b.add_argument("--collapse", default="", help="comma list of CANDIDATE aliases to collapse anyway: ctsp, deepfluoro. "
                                                  "`ctsp` needs --d813 or --patient-keys and is refused without one")
    b.add_argument("--d813", default=None, help="Dataset813 root holding imagesTr/; its symlink NAMES are the "
                                                "COLONOG_<stem> -> CTSpinoPelvic1K release-id crosswalk (never followed)")
    b.add_argument("--patient-keys", default=None, help="tools/patient_keys.py output ({case: 'corpus:person'}); its "
                                                        "ctsp keys are read as the same crosswalk")
    b.add_argument("--strict", action="store_true", help="exit 1 when any leak row is non-zero")
    c = sub.add_parser("check", help="re-read a lineage.json and fail on any leak row")
    c.add_argument("--lineage", default=str(Path(__file__).resolve().parents[1] / "docs" / "lineage.json"))
    s = sub.add_parser("show", help="print the markdown of a lineage.json")
    s.add_argument("--lineage", default=str(Path(__file__).resolve().parents[1] / "docs" / "lineage.json"))
    a = ap.parse_args()
    return dict(build=cmd_build, check=cmd_check, show=cmd_show)[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
