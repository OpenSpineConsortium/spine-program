#!/usr/bin/env python
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/rule_report.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""rule_report.py -- PREREG_rules.md section 5 over the rules census: per-rule contribution, the flag-configuration
sweep with the pre-stated sweet spot, ROC from the continuous quantities, the prevalence-window check, and one
self-contained HTML report.

PURPOSE
  The rules engine (tools/transitional_review/anomaly_rules.py) writes one census row per CT with each rule's value and
  decision. This tool joins that census to the READ-TIER truth only (nothing machine-made counts as truth), and reports,
  exactly as docs/ruleclass/PREREG_rules.md section 5 pre-states it:
    * per-rule contribution: flagged share with and without each rule, and the read-tier positives only it catches,
      pooled and per subtype (L6, T13, four_lumbar_or_fused_L5, castellvi_II_IV, lumbar_rib, stump_rib);
    * the sweep over flag configurations (every non-empty subset of the available rules; rule 3 S3 over a grid of
      ratio cuts ONLY once a calibrated cut is supplied), each with sensitivity / specificity / PPV and Wilson 95 %
      intervals; the SWEET SPOT = the configuration with the highest specificity subject to sensitivity >= 0.95 on
      read-tier positives, pooled and per subtype, and a plain statement when no configuration reaches 0.95;
    * ROC per rule and per subtype from the continuous quantities (count as an ordinal distance from five, the S3
      ratio, the rule-2 z-scores against the reference half);
    * the prevalence windows of section 5 with pass / fail / not_computable per window;
    * report.html (self-contained, inline SVG, no CDN, readable on a phone), tables/*.csv, summary.json.

INPUTS
  --census      the rules census TSV (one row per CT). Columns are read by alias and every missing column degrades to
                "rule not available" with a stated reason, never to a silent zero. Canonical names (the tree builder's
                schema): case_key, collection, case_id, person_key, count (4|5|6|no_count|no_anchor), anchor_source,
                flags (';'-list, e.g. complete_sacralisation_candidate, lumbarisation_candidate,
                castellvi_II_IV_candidate), stump_left, stump_right (STUMP|FULL|UNDECIDED|BROKEN?|ABSENT), s3_ratio,
                rule2_* (features, mm or ratios), rule4_decision (thoracic|lumbar|tltv|''), child, last_rib_level,
                n_thoracic_rib_bearing, prior_subtype, registry_subtype, truth_tier.
  --castellvi   CTSpinoPelvic1K-1/docs/castellvi_consensus.csv   (two radiologists; volume_id zfill(4); consensus grade)
  --lumbosac    CTSpinoPelvic1K-1/Lumbosac.csv                    (same readers; non-rib-bearing count 6 / 4 per token)
  --verse-suppl ~/lstv_flag/sources/verse_suppl_table1.csv       (Loeffler 2021 Suppl. Table 1, 325 subjects)
  --lstv-flags  ~/lstv_flag/lstv_flag_labels_v2.csv              (LSTV_flag / TLTV_flag; TLTV used for the verse cohort only,
                                                                  because the CTSP TLTV flag is label-derived, not a read)
  --registry    SchwingNet/results/transitional_registry/registry.csv (rows with truth_tier == read only)
  --prereg      docs/ruleclass/PREREG_rules.md (its sha256 is written into every output row)
  --s3-cut      the calibrated S3 ratio cut (STUMP_RULE.md C6). Without it S3 enters no configuration and the report
                says so; the S3 ratio ROC is produced either way.

OUTPUTS (under --out)
  report.html, summary.json, tables/{header,truth_join,truth_conflicts,rule_states,contribution,only_caught_by,
  sweep,sweet_spot,roc_auc,roc_curves,prevalence_windows,unit_flags}.csv. Every CSV row and summary.json carry
  prereg_sha256, prereg_status, git_sha, tool, tool_version, utc_time and inputs_sha256 (name=sha256;...).

RUN
  python tools/transitional_review/rule_report.py --census /rs/rs_grp_oschome/go2432/ruleclass/rules/census.tsv \
      --castellvi <CTSpinoPelvic1K repository at 7ddfe38>/docs/castellvi_consensus.csv \
      --lumbosac  <CTSpinoPelvic1K repository at 7ddfe38>/Lumbosac.csv \
      --verse-suppl <copy of ~/lstv_flag/sources/verse_suppl_table1.csv> \
      --lstv-flags  <copy of ~/lstv_flag/lstv_flag_labels_v2.csv> \
      --registry SchwingNet/results/transitional_registry/registry.csv \
      --out /rs/rs_grp_oschome/go2432/ruleclass/report/<date> [--s3-cut 0.45] [--unit person|ct]
  Self-test (synthetic census of ~2,000 rows with positives planted at the published prevalences; exits non-zero on
  any mismatch):
  python tools/transitional_review/rule_report.py --selftest [--keep <dir>]

WHAT THIS TOOL DOES NOT DO
  It opens no image and resolves no label map. It never gates anything: PREREG_rules.md is DRAFT v1 and every number
  here is calibration until the freeze line is filled (prereg_status is written as "draft").
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import itertools
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

TOOL = "rule_report"
TOOL_VERSION = "1"
PREREG_STATUS = "draft"
REPO = Path(__file__).resolve().parents[2]
PREREG_DEFAULT = REPO / "docs" / "ruleclass" / "PREREG_rules.md"

SUBTYPES = ["L6", "T13", "four_lumbar_or_fused_L5", "castellvi_II_IV", "lumbar_rib", "stump_rib"]
SUBTYPE_LABEL = {
    "L6": "L6",
    "T13": "T13",
    "four_lumbar_or_fused_L5": "four lumbar / fused L5",
    "castellvi_II_IV": "Castellvi II-IV",
    "lumbar_rib": "lumbar rib",
    "stump_rib": "stump rib",
}
# which subtypes need which junction read; a truth source that never saw the junction leaves them NA
LS_SUBTYPES = ["L6", "four_lumbar_or_fused_L5", "castellvi_II_IV"]
TL_SUBTYPES = ["T13", "lumbar_rib", "stump_rib"]

MIN_SENS_DEFAULT = 0.95  # PREREG section 5, pre-stated

# PREREG section 5 prevalence windows (percent). "point" is the published estimate where the window is a point.
WINDOWS = [
    {"key": "thirteen_rib_bearing", "label": "thirteen rib-bearing vertebrae", "lo": 0.37, "hi": 0.88, "point": None,
     "source": "Osiowski 2024 / Doo 2020 / Sabri 2025 (CITABLE_CLAIMS rows 68, 69)"},
    {"key": "eleven_rib_bearing", "label": "eleven rib-bearing vertebrae", "lo": 4.5, "hi": 8.0, "point": None,
     "source": "Osiowski 2024 / Sabri 2025 (CITABLE_CLAIMS rows 68, 69)"},
    {"key": "lumbar_rib", "label": "lumbar rib", "lo": 0.6, "hi": 4.3, "point": 1.6,
     "source": "Osiowski 2024, CT subgroup (CITABLE_CLAIMS row 69)"},
    {"key": "stump_any", "label": "subjects with >= 1 stump lowest rib", "lo": 12.6, "hi": 20.5, "point": None,
     "source": "Nagata 2025 hypoplastic 12th rib 12.6 % (CITABLE_CLAIMS row 63); Moeller 2026 >= 1 stump 20.5 % (row 57)"},
    {"key": "l6_count_six", "label": "L6 (rib-free count six, not thoracic by rule 4)", "lo": 2.0, "hi": 5.0, "point": None,
     "source": "L6 by CT reads ~2-5 % (CITABLE_CLAIMS rows 63, 68, 69)"},
]

RULES = ["R1_count", "R1_anchor", "R2", "R3_S1", "R3_S3", "R4"]
RULE_LABEL = {
    "R1_count": "rule 1: rib-free count != 5",
    "R1_anchor": "rule 1: absorbed / lumbarisation candidate",
    "R2": "rule 2: pelvis feature outside central 95 %",
    "R3_S1": "rule 3 S1: STUMP or ABSENT at the lowest level",
    "R3_S3": "rule 3 S3: lowest/above ratio below the calibrated cut",
    "R4": "rule 4: MDPA shape score thoracic on the sixth body",
}

ALIASES = {
    "case_key": ["case_key", "key"],
    "collection": ["collection", "coll"],
    "case_id": ["case_id", "case"],
    "person_key": ["person_key", "patient_key"],
    "count": ["count", "rule1_count", "r1_count", "rib_free_count"],
    "anchor_source": ["anchor_source", "rule1_anchor_source"],
    "flags": ["flags", "rule1_flags", "rule_flags"],
    "stump_left": ["stump_left", "rule3_stump_left"],
    "stump_right": ["stump_right", "rule3_stump_right"],
    "s3_ratio": ["s3_ratio", "rule3_s3_ratio", "rule3_ratio"],
    "rule4_decision": ["rule4_decision", "rule4_call", "rule4_class"],
    "child": ["child", "is_child", "child_flag"],
    "last_rib_level": ["last_rib_level", "rule3_last_rib_level"],
    "n_thoracic_rib_bearing": ["n_thoracic_rib_bearing", "thoracic_count", "n_rib_bearing"],
    "prior_subtype": ["prior_subtype", "labeller_subtype"],
    "registry_subtype": ["registry_subtype"],
    "truth_tier": ["truth_tier", "registry_truth_tier"],
}
# grades are written IIa, IIb, IIIa, IIIb, IV (and Ia/Ib/0 for the negatives); no \b here, 'IIb' has none after 'II'
CASTELLVI_POS = re.compile(r"^\s*(IV|III|II)\s*[ab]?\s*$", re.I)
CASTELLVI_NEG = re.compile(r"^\s*(0|I\s*[ab]?|NL|none)\s*$", re.I)
LUMBAR_IDS = {20, 21, 22, 23, 24, 25}


# ----------------------------------------------------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha(repo: Path) -> str:
    try:
        sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True,
                             check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True, check=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except Exception as e:  # noqa: BLE001
        return "unknown (%s)" % type(e).__name__


def wilson(k: int, n: int, z: float = 1.959963985):
    """Wilson score interval, the convention of tools/eval_anomaly_rule.py."""
    if n == 0:
        return (float("nan"), float("nan"))
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def rate(k: int, n: int) -> float:
    return k / n if n else float("nan")


def to_float(x) -> float:
    try:
        if x is None or (isinstance(x, str) and x.strip() in ("", "None", "nan", "NaN", "null")):
            return float("nan")
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def utc_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pick(df: pd.DataFrame, canon: str):
    for c in ALIASES.get(canon, [canon]):
        if c in df.columns:
            return c
    return None


def auc_hanley(scores_pos: np.ndarray, scores_neg: np.ndarray):
    """Mann-Whitney AUC with ties, Hanley-McNeil SE, 95 % CI, and the ROC curve points."""
    from scipy.stats import rankdata
    pos = scores_pos[~np.isnan(scores_pos)]
    neg = scores_neg[~np.isnan(scores_neg)]
    n1, n0 = len(pos), len(neg)
    if n1 == 0 or n0 == 0:
        return {"auc": float("nan"), "lo": float("nan"), "hi": float("nan"), "n_pos": n1, "n_neg": n0, "curve": []}
    allv = np.concatenate([pos, neg])
    r = rankdata(allv)
    auc = (r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
    q1 = auc / (2 - auc)
    q2 = 2 * auc * auc / (1 + auc)
    se = math.sqrt(max(0.0, (auc * (1 - auc) + (n1 - 1) * (q1 - auc * auc) + (n0 - 1) * (q2 - auc * auc)) / (n1 * n0)))
    # curve: threshold descending (higher score = more anomalous)
    thr = np.unique(allv)[::-1]
    if len(thr) > 200:
        thr = thr[np.linspace(0, len(thr) - 1, 200).astype(int)]
    curve = [(0.0, 0.0)]
    for t in thr:
        curve.append((float((neg >= t).mean()), float((pos >= t).mean())))
    curve.append((1.0, 1.0))
    return {"auc": float(auc), "lo": max(0.0, auc - 1.96 * se), "hi": min(1.0, auc + 1.96 * se),
            "n_pos": n1, "n_neg": n0, "curve": curve}


# ----------------------------------------------------------------------------------------------------------------------
# truth: the read tiers only
# ----------------------------------------------------------------------------------------------------------------------
class Truth:
    """Per person: subtype -> 1 (read positive) / 0 (read negative) / None (not assessed), plus the sources."""

    def __init__(self):
        self.rows: dict[str, dict] = {}
        self.conflicts: list[dict] = []

    def _get(self, key: str) -> dict:
        if key not in self.rows:
            self.rows[key] = {s: None for s in SUBTYPES}
            self.rows[key]["sources"] = set()
            self.rows[key]["notes"] = []
        return self.rows[key]

    def set(self, key: str, subtype: str, value, source: str, note: str = ""):
        if value is None:
            return
        row = self._get(key)
        row["sources"].add(source)
        cur = row[subtype]
        if cur is None:
            row[subtype] = int(value)
        elif cur != int(value):
            self.conflicts.append({"unit_key": key, "subtype": subtype, "kept": max(cur, int(value)),
                                   "source": source, "value": int(value), "prior": cur})
            row[subtype] = max(cur, int(value))  # a read positive from any read source stands
        if note:
            row["notes"].append(note)

    def frame(self) -> pd.DataFrame:
        recs = []
        for k, r in self.rows.items():
            rec = {"unit_key": k}
            for s in SUBTYPES:
                rec["truth_" + s] = "" if r[s] is None else str(r[s])
            assessed = [s for s in SUBTYPES if r[s] is not None]
            rec["n_assessed"] = len(assessed)
            rec["pooled_pos"] = int(any(r[s] == 1 for s in SUBTYPES))
            rec["pooled_neg"] = int(len(assessed) > 0 and not rec["pooled_pos"])
            rec["truth_sources"] = ";".join(sorted(r["sources"]))
            rec["truth_notes"] = " | ".join(r["notes"])[:500]
            recs.append(rec)
        return pd.DataFrame(recs)


def _ctsp_key(vol) -> str:
    return "ctsp:" + str(vol).strip().zfill(4)


def load_castellvi(p: Path, truth: Truth) -> dict:
    """castellvi_consensus.csv: consensus grade per CTSP volume. Returns token -> volume_id for the Lumbosac join."""
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    tok2vol = {}
    for _, r in df.iterrows():
        vol = r["volume_id"].strip()
        if not vol:
            continue
        key = _ctsp_key(vol)
        tok2vol[str(r.get("token", "")).strip()] = vol
        cons = str(r.get("consensus", "")).strip()
        if CASTELLVI_POS.match(cons):
            truth.set(key, "castellvi_II_IV", 1, "castellvi_consensus", "Castellvi consensus %s" % cons)
        elif CASTELLVI_NEG.match(cons):
            truth.set(key, "castellvi_II_IV", 0, "castellvi_consensus", "Castellvi consensus %s" % cons)
        # the readers' free text names stump / rudimentary ribs; that is a read, recorded as such
        c = str(r.get("comment", "")).lower()
        if "rudimentary" in c or "hypoplastic" in c:
            truth.set(key, "stump_rib", 1, "castellvi_consensus", "reader comment: " + c[:80])
            if re.search(r"\bat l1\b", c):  # a rudimentary rib on L1 is a lumbar rib (Loeffler's L1 stump convention)
                truth.set(key, "lumbar_rib", 1, "castellvi_consensus")
    return tok2vol


def load_lumbosac(p: Path, truth: Truth, tok2vol: dict):
    """Lumbosac.csv: the readers' non-rib-bearing count per token (6 -> L6, 4 -> four lumbar). A parenthetical
    disagreement ("6 (NA 4)") is two readers disagreeing, so no consensus count is taken from it."""
    df = pd.read_csv(p, dtype=str, keep_default_na=False, header=0)
    name_col = [c for c in df.columns if c.strip().lower() == "name"]
    cnt_col = [c for c in df.columns if "bearing vertebra" in c.lower()]
    if not name_col or not cnt_col:
        raise SystemExit("Lumbosac.csv: expected a 'Name' column and a '... bearing vertebra #' column; got %s" % list(df.columns))
    name_col, cnt_col = name_col[0], cnt_col[0]
    for _, r in df.iterrows():
        m = re.search(r"token[ _]*(\d+)", str(r[name_col]), re.I)
        if not m:
            continue
        vol = tok2vol.get(m.group(1))
        if vol is None:
            continue
        key = _ctsp_key(vol)
        raw = str(r[cnt_col]).strip()
        m2 = re.match(r"^(\d+)\s*(\(.*\))?$", raw)
        if not m2:
            continue
        n = int(m2.group(1))
        if m2.group(2):
            truth._get(key)["notes"].append("Lumbosac count disagreement %s: no consensus count" % raw)
            truth._get(key)["sources"].add("lumbosac")
            continue
        truth.set(key, "L6", int(n == 6), "lumbosac", "readers' non-rib-bearing count %d" % n)
        truth.set(key, "four_lumbar_or_fused_L5", int(n == 4), "lumbosac")


def load_verse_suppl(p: Path, truth: Truth):
    """Loeffler 2021 Suppl. Table 1. Blank = not assessed (the junction was not in the read's field)."""
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    for _, r in df.iterrows():
        vid = str(r["verse_id"]).strip()
        if not vid.isdigit():
            continue
        key = "verse:verse%03d" % int(vid)
        stump = str(r.get("thoracolumbar_stump_ribs", "")).strip()
        if stump != "":
            truth.set(key, "stump_rib", int(stump.upper() in ("L1", "T12", "T13")), "verse_suppl",
                      "" if stump == "0" else "stump rib at %s" % stump)
            truth.set(key, "lumbar_rib", int(stump.upper() == "L1"), "verse_suppl")
        # T13 comes from thoracolumbar_enumeration only: assumed_segment_structure is the paper's ASSUMPTION for the
        # subject (7/12/5/5 by default) and is filled where the thoraco-lumbar junction was never in the read's field
        tle = str(r.get("thoracolumbar_enumeration", "")).strip()
        if tle != "":
            truth.set(key, "T13", int(tle == "2"), "verse_suppl", "T13 (thoracolumbar_enumeration 2)" if tle == "2" else "")
        lse = str(r.get("lumbosacral_enumeration", "")).strip()
        if lse != "":
            truth.set(key, "L6", int(lse == "2"), "verse_suppl", "six lumbar (lumbosacral_enumeration 2)" if lse == "2" else "")
            truth.set(key, "four_lumbar_or_fused_L5", int(lse == "1"), "verse_suppl",
                      "four lumbar (lumbosacral_enumeration 1)" if lse == "1" else "")
        cg = str(r.get("castellvi_grading", "")).strip().lower()
        if cg != "":
            pos = bool(re.match(r"^(2|3|4)", cg))
            neg = cg in ("0", "0/1", "1", "1a", "1b")
            if pos or neg:
                truth.set(key, "castellvi_II_IV", int(pos), "verse_suppl", "Castellvi %s" % cg if pos else "")


def load_lstv_flags(p: Path, truth: Truth):
    """lstv_flag_labels_v2.csv. LSTV_flag is used for both cohorts (CTSP: the Castellvi reads; verse: Loeffler's
    reads). TLTV_flag is used for the verse cohort only: the CTSP TLTV flag equals manifest_has_lumbar_rib, which comes
    from the release labels, not from a radiologist read. The flags are pooled ('any LSTV' / 'any TLTV'), so a 1 raises
    the pooled positive without naming a subtype unless a subtype column is present; a 0 clears the junction's subtypes
    only where no other read source says otherwise."""
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    for _, r in df.iterrows():
        cohort = str(r.get("cohort", "")).strip()
        vol = str(r.get("volume_id", "")).strip()
        if cohort == "ctsp":
            key = _ctsp_key(vol)
        elif cohort == "verse":
            m = re.search(r"(\d+)", vol)
            if not m:
                continue
            key = "verse:verse%03d" % int(m.group(1))
        else:
            continue
        lstv = str(r.get("LSTV_flag", "")).strip()
        if lstv in ("0", "1"):
            if lstv == "1":
                # name the subtype where the row says which; else record 'any LSTV' on the notes and leave it to
                # the other sources (the registry / consensus rows name it for every CTSP and verse read positive)
                lab = str(r.get("lstv_label", "")).lower() + " " + str(r.get("castellvi_type", "")).lower()
                named = False
                if "6 lumbar" in lab or "lumbarization (6" in lab:
                    truth.set(key, "L6", 1, "lstv_flags", "lstv_label: " + lab.strip()[:60]); named = True
                if re.search(r"castellvi (ii|iii|iv)", lab):
                    truth.set(key, "castellvi_II_IV", 1, "lstv_flags"); named = True
                if not named:
                    truth._get(key)["notes"].append("LSTV_flag=1 without a named subtype")
                    truth._get(key)["sources"].add("lstv_flags")
            else:
                for s in LS_SUBTYPES:
                    truth.set(key, s, 0, "lstv_flags")
        if cohort == "verse":
            tltv = str(r.get("TLTV_flag", "")).strip()
            if tltv == "0":
                for s in TL_SUBTYPES:
                    truth.set(key, s, 0, "lstv_flags")
            elif tltv == "1":
                truth._get(key)["notes"].append("TLTV_flag=1 (verse; named by verse_suppl)")
                truth._get(key)["sources"].add("lstv_flags")


def load_registry(p: Path, truth: Truth):
    """registry.csv, truth_tier == read only. subtype, castellvi grade, four_lumbar, lumbar_rib, and 'read stump rib
    at <level>' in the notes."""
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    df = df[df["truth_tier"].str.strip() == "read"]
    for _, r in df.iterrows():
        key = str(r["patient_key"]).strip()
        if key.startswith("ctsp:"):
            key = _ctsp_key(key.split(":", 1)[1])
        st = str(r.get("subtype", "")).strip()
        cg = str(r.get("castellvi", "")).strip()
        notes = str(r.get("notes", ""))
        if st in ("no_count", "unassigned", "unresolved", ""):
            truth._get(key)["notes"].append("registry read row subtype=%s (not a usable truth)" % st)
            truth._get(key)["sources"].add("registry")
            continue
        # the subtype names ONE anomaly; the grade, the four_lumbar / lumbar_rib columns and the 'read stump rib at'
        # note carry the others, and a subtype 'none' row can still carry a read stump rib (Loeffler's stump column
        # with an ordinary enumeration). A junction the read never saw leaves its subtypes blank.
        ls_seen = str(r.get("junction_ls_in_fov", "True")).strip() != "False"
        tl_seen = str(r.get("junction_tl_in_fov", "True")).strip() != "False"
        m = re.search(r"read stump rib at (T12|L1|T13)", notes)
        fused = st == "sacralised_L5_fused" or str(r.get("four_lumbar", "")).strip() == "True"
        lr = st == "lumbar_rib" or str(r.get("lumbar_rib", "")).strip() == "True" or bool(m and m.group(1) == "L1")
        sig = {"L6": st == "L6", "T13": st == "T13", "four_lumbar_or_fused_L5": fused,
               "castellvi_II_IV": bool(CASTELLVI_POS.match(cg)), "lumbar_rib": lr, "stump_rib": bool(m)}
        for s, v in sig.items():
            if v:
                truth.set(key, s, 1, "registry", "registry %s%s" % (s, (" (" + m.group(0) + ")") if (s == "stump_rib" and m) else ""))
            elif (s in LS_SUBTYPES and ls_seen) or (s in TL_SUBTYPES and tl_seen):
                if s == "castellvi_II_IV" and not (CASTELLVI_NEG.match(cg) or st in ("none", "L6", "T13", "lumbar_rib", "sacralised_L5_fused")):
                    continue
                truth.set(key, s, 0, "registry")


def build_truth(args) -> tuple[Truth, dict]:
    truth = Truth()
    used = {}
    tok2vol = {}
    if args.castellvi:
        tok2vol = load_castellvi(Path(args.castellvi), truth); used["castellvi_consensus"] = Path(args.castellvi)
    if args.lumbosac:
        if not tok2vol:
            print("WARNING: --lumbosac given without --castellvi: tokens cannot be joined to volume ids; skipped")
        else:
            load_lumbosac(Path(args.lumbosac), truth, tok2vol); used["lumbosac"] = Path(args.lumbosac)
    if args.verse_suppl:
        load_verse_suppl(Path(args.verse_suppl), truth); used["verse_suppl"] = Path(args.verse_suppl)
    if args.lstv_flags:
        load_lstv_flags(Path(args.lstv_flags), truth); used["lstv_flags"] = Path(args.lstv_flags)
    if args.registry:
        load_registry(Path(args.registry), truth); used["registry"] = Path(args.registry)
    return truth, used


# ----------------------------------------------------------------------------------------------------------------------
# census: rule states per CT, then per unit (person by default)
# ----------------------------------------------------------------------------------------------------------------------
def load_census(path: Path) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    cols = {c: pick(df, c) for c in ALIASES}
    if cols["case_key"] is None:
        if cols["collection"] and cols["case_id"]:
            df["case_key"] = df[cols["collection"]] + ":" + df[cols["case_id"]]
            cols["case_key"] = "case_key"
        else:
            raise SystemExit("census: no case_key and no collection+case_id column")
    if cols["person_key"] is None:
        if cols["collection"] and cols["case_id"]:
            df["person_key"] = [
                (c + ":" + (i.zfill(4) if c == "ctsp" else i)) for c, i in zip(df[cols["collection"]], df[cols["case_id"]])]
            cols["person_key"] = "person_key"
        else:
            df["person_key"] = df[cols["case_key"]]
            cols["person_key"] = "person_key"
    # ctsp keys zero-padded, whatever the census wrote
    pk = df[cols["person_key"]].astype(str)
    df[cols["person_key"]] = [(_ctsp_key(k.split(":", 1)[1]) if k.startswith("ctsp:") else k) for k in pk]
    return df, cols


def rule2_features(df: pd.DataFrame) -> list[str]:
    out = []
    for c in df.columns:
        if re.match(r"^rule2_", c) and not re.search(r"(_flag|_outside95|_z|_state|_source)$", c):
            if pd.to_numeric(df[c].replace("", np.nan), errors="coerce").notna().sum() > 0:
                out.append(c)
    return out


def rule2_zscores(df: pd.DataFrame, cols: dict, feats: list[str]) -> tuple[pd.DataFrame, dict]:
    """z-scores against the REFERENCE HALF (PREREG section 2): adults, count five, prior and registry calls ordinary,
    split by person into a reference half and a test half by a stable hash. Returns z columns and the thresholds."""
    info = {"features": feats, "n_reference": 0, "n_test": 0, "thresholds": {}}
    if not feats:
        return pd.DataFrame(index=df.index), info
    count = df[cols["count"]] if cols["count"] else pd.Series("", index=df.index)
    prior = df[cols["prior_subtype"]] if cols["prior_subtype"] else pd.Series("", index=df.index)
    regs = df[cols["registry_subtype"]] if cols["registry_subtype"] else pd.Series("", index=df.index)
    child = df[cols["child"]] if cols["child"] else pd.Series("", index=df.index)
    ordinary = {"", "none", "ordinary", "normal", "0"}
    eligible = (count.astype(str) == "5") & prior.astype(str).str.lower().isin(ordinary) & \
               regs.astype(str).str.lower().isin(ordinary) & ~child.astype(str).str.lower().isin({"1", "true", "yes"})
    pk = df[cols["person_key"]].astype(str)
    half = pk.map(lambda k: int(hashlib.sha256(k.encode()).hexdigest(), 16) % 2 == 0)
    ref = eligible & half
    info["n_reference"] = int(ref.sum())
    info["n_test"] = int((eligible & ~half).sum())
    z = pd.DataFrame(index=df.index)
    for f in feats:
        v = pd.to_numeric(df[f].replace("", np.nan), errors="coerce")
        rv = v[ref].dropna()
        if len(rv) < 20:
            info["thresholds"][f] = {"n": int(len(rv)), "note": "reference half under 20 values: feature not scored"}
            z[f + "_z"] = np.nan
            continue
        lo, hi = np.percentile(rv, [2.5, 97.5])
        mu, sd = float(rv.mean()), float(rv.std(ddof=1))
        info["thresholds"][f] = {"n": int(len(rv)), "p2.5": float(lo), "p97.5": float(hi), "mean": mu, "sd": sd}
        z[f + "_z"] = (v - mu) / sd if sd > 0 else np.nan
        z[f + "_out"] = np.where(v.isna(), np.nan, ((v < lo) | (v > hi)).astype(float))
    df["_r2_reference_half"] = ref.astype(int)
    return z, info


def rule_states(df: pd.DataFrame, cols: dict, z: pd.DataFrame, feats: list[str], s3_cut: float | None,
                s3_grid: list[float]) -> tuple[pd.DataFrame, dict]:
    """Per CT and rule: fires | silent | cannot_run. Returns the state table and the availability of each rule."""
    n = len(df)
    st = pd.DataFrame(index=df.index)
    avail = {}
    # R1 count
    if cols["count"]:
        c = df[cols["count"]].astype(str).str.strip()
        st["R1_count"] = np.where(c.isin(["4", "6"]), "fires", np.where(c == "5", "silent", "cannot_run"))
        avail["R1_count"] = "available"
    else:
        st["R1_count"] = "cannot_run"; avail["R1_count"] = "column count absent"
    # R1 anchor flags
    flags = df[cols["flags"]].astype(str) if cols["flags"] else pd.Series([""] * n, index=df.index)
    fl = flags.str.split(";").map(lambda xs: {x.strip() for x in xs if x.strip()})
    anchor_fire = fl.map(lambda s: bool(s & {"complete_sacralisation_candidate", "lumbarisation_candidate"}))
    if cols["flags"]:
        anchor_ran = anchor_fire | (df[cols["count"]].astype(str).isin(["4", "5", "6"]) if cols["count"] else False)
        st["R1_anchor"] = np.where(anchor_fire, "fires", np.where(anchor_ran, "silent", "cannot_run"))
        avail["R1_anchor"] = "available"
    else:
        st["R1_anchor"] = "cannot_run"; avail["R1_anchor"] = "column flags absent"
    # R2
    outcols = [c for c in z.columns if c.endswith("_out")]
    if "rule2_outside95" in df.columns:
        v = df["rule2_outside95"].astype(str).str.strip()
        st["R2"] = np.where(v == "1", "fires", np.where(v == "0", "silent", "cannot_run"))
        avail["R2"] = "available (precomputed rule2_outside95)"
    elif outcols:
        anyout = z[outcols].max(axis=1)
        st["R2"] = np.where(anyout == 1, "fires", np.where(anyout == 0, "silent", "cannot_run"))
        avail["R2"] = "available (%d features, reference-half thresholds)" % len(outcols)
    else:
        st["R2"] = "cannot_run"; avail["R2"] = "no rule2_* feature column with values"
    # R3 S1
    if cols["stump_left"] or cols["stump_right"]:
        L = df[cols["stump_left"]].astype(str).str.strip().str.upper() if cols["stump_left"] else pd.Series([""] * n, index=df.index)
        R = df[cols["stump_right"]].astype(str).str.strip().str.upper() if cols["stump_right"] else pd.Series([""] * n, index=df.index)
        fire = L.isin(["STUMP", "ABSENT"]) | R.isin(["STUMP", "ABSENT"])
        ran = fire | (L == "FULL") | (R == "FULL")
        st["R3_S1"] = np.where(fire, "fires", np.where(ran, "silent", "cannot_run"))
        avail["R3_S1"] = "available"
    else:
        st["R3_S1"] = "cannot_run"; avail["R3_S1"] = "columns stump_left/stump_right absent"
    # R3 S3 (only with a calibrated cut)
    if cols["s3_ratio"]:
        r = pd.to_numeric(df[cols["s3_ratio"]].replace("", np.nan), errors="coerce")
        df["_s3_ratio"] = r
        if s3_cut is not None:
            for cut in s3_grid:
                st["R3_S3@%.3f" % cut] = np.where(r.isna(), "cannot_run", np.where(r < cut, "fires", "silent"))
            st["R3_S3"] = st["R3_S3@%.3f" % s3_cut]
            avail["R3_S3"] = "available (calibrated cut %.3f; grid %s)" % (s3_cut, ",".join("%.3f" % g for g in s3_grid))
        else:
            st["R3_S3"] = "cannot_run"
            avail["R3_S3"] = "no calibrated cut supplied (STUMP_RULE.md C6 pending): S3 enters no configuration; ratio ROC only"
    else:
        st["R3_S3"] = "cannot_run"; avail["R3_S3"] = "column s3_ratio absent"
    # R4
    if cols["rule4_decision"]:
        d = df[cols["rule4_decision"]].astype(str).str.strip().str.lower()
        if (d != "").sum() == 0:
            st["R4"] = "cannot_run"; avail["R4"] = "rule4_decision present but empty on every row (classifier not frozen)"
        else:
            st["R4"] = np.where(d == "thoracic", "fires", np.where(d.isin(["lumbar", "tltv", "intermediate"]), "silent", "cannot_run"))
            avail["R4"] = "available"
    else:
        st["R4"] = "cannot_run"; avail["R4"] = "column rule4_decision absent"
    return st, avail


def aggregate_units(df: pd.DataFrame, cols: dict, st: pd.DataFrame, unit: str, extra: dict[str, pd.Series]):
    """Collapse CT rows to units (persons by default): a rule fires for a unit if it fires on any CT."""
    key = df[cols["person_key"]] if unit == "person" else df[cols["case_key"]]
    order = {"fires": 2, "silent": 1, "cannot_run": 0}
    inv = {v: k for k, v in order.items()}
    ust = st.apply(lambda s: s.map(order)).groupby(key.values).max().apply(lambda s: s.map(inv))
    ust.index.name = "unit_key"
    ex = {}
    for name, ser in extra.items():
        ex[name] = ser.groupby(key.values).max()
    coll = df[cols["collection"]].groupby(key.values).first() if cols["collection"] else pd.Series("", index=ust.index)
    n_ct = key.groupby(key.values).size()
    return ust, ex, coll, n_ct


# ----------------------------------------------------------------------------------------------------------------------
# metrics
# ----------------------------------------------------------------------------------------------------------------------
def config_columns(ust: pd.DataFrame, rules: tuple[str, ...]) -> tuple[pd.Series, pd.Series]:
    sub = ust[list(rules)]
    flagged = (sub == "fires").any(axis=1)
    evaluable = (sub != "cannot_run").any(axis=1)
    return flagged, evaluable


def metrics(flagged: pd.Series, evaluable: pd.Series, T: pd.DataFrame) -> dict:
    """Pooled + per-subtype. Sensitivity counts a positive the screen could not evaluate as MISSED (strict); the
    evaluable-only sensitivity is reported beside it. Specificity is on evaluable read negatives."""
    out = {}
    j = T.join(pd.DataFrame({"flagged": flagged, "evaluable": evaluable}), how="left")
    j["flagged"] = j["flagged"].fillna(False).astype(bool)
    j["evaluable"] = j["evaluable"].fillna(False).astype(bool)
    pos = j["pooled_pos"] == 1
    neg = j["pooled_neg"] == 1
    tp = int((pos & j.flagged).sum()); fn = int((pos & ~j.flagged).sum())
    fp = int((neg & j.flagged).sum()); tn = int((neg & j.evaluable & ~j.flagged).sum())
    ne_pos = int((pos & ~j.evaluable).sum()); ne_neg = int((neg & ~j.evaluable).sum())
    out["pooled"] = _mk(tp, fn, fp, tn, ne_pos, ne_neg)
    for s in SUBTYPES:
        ts = j["truth_" + s].astype(str)
        p = ts == "1"
        nn = (ts == "0") & neg
        tp_s = int((p & j.flagged).sum()); fn_s = int((p & ~j.flagged).sum())
        fp_s = int((nn & j.flagged).sum()); tn_s = int((nn & j.evaluable & ~j.flagged).sum())
        out[s] = _mk(tp_s, fn_s, fp_s, tn_s, int((p & ~j.evaluable).sum()), int((nn & ~j.evaluable).sum()))
    return out


def _mk(tp, fn, fp, tn, ne_pos, ne_neg) -> dict:
    n_pos, n_neg_eval = tp + fn, tn + fp
    sens = rate(tp, n_pos); spec = rate(tn, n_neg_eval); ppv = rate(tp, tp + fp)
    s_lo, s_hi = wilson(tp, n_pos); p_lo, p_hi = wilson(tn, n_neg_eval); v_lo, v_hi = wilson(tp, tp + fp)
    return {"tp": tp, "fn": fn, "fp": fp, "tn": tn, "n_pos": n_pos, "n_neg_evaluable": n_neg_eval,
            "n_pos_not_evaluable": ne_pos, "n_neg_not_evaluable": ne_neg,
            "sens": sens, "sens_lo": s_lo, "sens_hi": s_hi,
            "sens_evaluable": rate(tp, n_pos - ne_pos),
            "spec": spec, "spec_lo": p_lo, "spec_hi": p_hi, "ppv": ppv, "ppv_lo": v_lo, "ppv_hi": v_hi}


def sweep(ust: pd.DataFrame, T: pd.DataFrame, rules: list[str], s3_grid_cols: list[str], min_sens: float):
    """Every non-empty subset of the available rules; a subset holding R3_S3 is expanded over the grid columns."""
    rows = []
    base = [r for r in rules if r != "R3_S3"]
    has_s3 = "R3_S3" in rules
    for k in range(1, len(base) + 1 + (1 if has_s3 else 0)):
        for combo in itertools.combinations(base + (["R3_S3"] if has_s3 else []), k):
            if "R3_S3" in combo:
                for gc in s3_grid_cols:
                    cfg = tuple(gc if r == "R3_S3" else r for r in combo)
                    rows.append(_eval_cfg(ust, T, cfg, combo, gc))
            else:
                rows.append(_eval_cfg(ust, T, combo, combo, None))
    sw = pd.DataFrame(rows)
    spots = {}
    for target in ["pooled"] + SUBTYPES:
        spots[target] = pick_sweet_spot(sw, target, min_sens)
    return sw, spots


def _eval_cfg(ust, T, cfg_cols, combo, grid_col):
    flagged, evaluable = config_columns(ust, cfg_cols)
    m = metrics(flagged, evaluable, T)
    name = "+".join(combo)
    cut = float(grid_col.split("@")[1]) if grid_col else float("nan")
    if grid_col:
        name = name.replace("R3_S3", "R3_S3@%.3f" % cut)
    row = {"config": name, "n_rules": len(combo), "s3_cut": cut, "rules": ";".join(combo),
           "n_units_flagged": int(flagged.sum()), "n_units_evaluable": int(evaluable.sum()),
           "census_flagged_share": rate(int(flagged.sum()), len(ust))}
    for tgt, mm in m.items():
        for k2, v in mm.items():
            row["%s__%s" % (tgt, k2)] = v
    return row


def pick_sweet_spot(sw: pd.DataFrame, target: str, min_sens: float) -> dict:
    """PREREG section 5: the configuration with the highest specificity subject to sensitivity >= min_sens on
    read-tier positives. Ties: fewer rules, then higher sensitivity, then name. When no configuration reaches
    min_sens, reached=False and the highest-sensitivity configuration is reported as 'best available, below the bar'."""
    sc, pc = target + "__sens", target + "__spec"
    npos = int(sw[target + "__n_pos"].iloc[0]) if len(sw) else 0
    if npos == 0:
        return {"target": target, "reached": False, "n_pos": 0, "statement":
                "no read-tier positives for %s: no sweet spot can be stated" % target}
    ok = sw[(sw[sc] >= min_sens) & sw[pc].notna()].copy()
    if len(ok):
        ok = ok.sort_values([pc, "n_rules", sc, "config"], ascending=[False, True, False, True])
        b = ok.iloc[0]
        return {"target": target, "reached": True, "n_pos": npos, "config": b["config"], "rules": b["rules"],
                "s3_cut": None if pd.isna(b["s3_cut"]) else float(b["s3_cut"]),
                "sens": float(b[sc]), "sens_lo": float(b[target + "__sens_lo"]), "sens_hi": float(b[target + "__sens_hi"]),
                "spec": float(b[pc]), "spec_lo": float(b[target + "__spec_lo"]), "spec_hi": float(b[target + "__spec_hi"]),
                "ppv": float(b[target + "__ppv"]), "tp": int(b[target + "__tp"]), "fn": int(b[target + "__fn"]),
                "fp": int(b[target + "__fp"]), "tn": int(b[target + "__tn"]),
                "n_configs_meeting_bar": int(len(ok)),
                "statement": "%s: %s reaches sensitivity %.3f (%d/%d) at specificity %.3f (%d/%d); %d of %d configurations meet the %.2f bar." % (
                    target, b["config"], b[sc], b[target + "__tp"], npos, b[pc], b[target + "__tn"],
                    b[target + "__tn"] + b[target + "__fp"], len(ok), len(sw), min_sens)}
    best = sw.sort_values([sc, pc, "n_rules"], ascending=[False, False, True]).iloc[0]
    return {"target": target, "reached": False, "n_pos": npos, "config": best["config"], "rules": best["rules"],
            "s3_cut": None if pd.isna(best["s3_cut"]) else float(best["s3_cut"]),
            "sens": float(best[sc]), "sens_lo": float(best[target + "__sens_lo"]), "sens_hi": float(best[target + "__sens_hi"]),
            "spec": float(best[pc]), "spec_lo": float(best[target + "__spec_lo"]), "spec_hi": float(best[target + "__spec_hi"]),
            "ppv": float(best[target + "__ppv"]), "tp": int(best[target + "__tp"]), "fn": int(best[target + "__fn"]),
            "fp": int(best[target + "__fp"]), "tn": int(best[target + "__tn"]), "n_configs_meeting_bar": 0,
            "statement": "%s: NO configuration reaches sensitivity %.2f on the %d read-tier positives. The highest sensitivity is %.3f (%d/%d) from %s, at specificity %.3f. The pre-stated sweet spot does not exist for this target." % (
                target, min_sens, npos, best[sc], best[target + "__tp"], npos, best["config"], best[pc])}


def contribution(ust: pd.DataFrame, T: pd.DataFrame, rules: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """For each rule: flagged share with and without it (census and read tier), read-tier positives only it catches,
    and the rule alone."""
    rows, only = [], []
    all_f, all_e = config_columns(ust, tuple(rules))
    m_all = metrics(all_f, all_e, T)
    for r in rules:
        others = tuple(x for x in rules if x != r)
        if others:
            wo_f, wo_e = config_columns(ust, others)
            m_wo = metrics(wo_f, wo_e, T)
        else:
            wo_f = pd.Series(False, index=ust.index); wo_e = pd.Series(False, index=ust.index)
            m_wo = metrics(wo_f, wo_e, T)
        r_f, r_e = config_columns(ust, (r,))
        m_r = metrics(r_f, r_e, T)
        only_mask = r_f & ~wo_f
        j = T.join(only_mask.rename("only"), how="left")
        j["only"] = j["only"].fillna(False).astype(bool)
        for tgt in ["pooled"] + SUBTYPES:
            pos = (j["pooled_pos"] == 1) if tgt == "pooled" else (j["truth_" + tgt].astype(str) == "1")
            n_only = int((pos & j["only"]).sum())
            for k in j.index[pos & j["only"]]:
                only.append({"rule": r, "target": tgt, "unit_key": k})
            rows.append({
                "rule": r, "target": tgt,
                "census_flagged_share_with": rate(int(all_f.sum()), len(ust)),
                "census_flagged_share_without": rate(int(wo_f.sum()), len(ust)),
                "census_flagged_share_rule_alone": rate(int(r_f.sum()), len(ust)),
                "n_census_units": len(ust),
                "n_fires": int((ust[r] == "fires").sum()), "n_silent": int((ust[r] == "silent").sum()),
                "n_cannot_run": int((ust[r] == "cannot_run").sum()),
                "read_n_pos": m_all[tgt]["n_pos"],
                "read_sens_with": m_all[tgt]["sens"], "read_sens_without": m_wo[tgt]["sens"],
                "read_spec_with": m_all[tgt]["spec"], "read_spec_without": m_wo[tgt]["spec"],
                "read_sens_rule_alone": m_r[tgt]["sens"], "read_spec_rule_alone": m_r[tgt]["spec"],
                "read_positives_only_this_rule": n_only,
            })
    return pd.DataFrame(rows), pd.DataFrame(only, columns=["rule", "target", "unit_key"])


def roc_tables(ux: dict, T: pd.DataFrame, feats: list[str]):
    """Continuous quantities per unit -> ROC pooled and per subtype."""
    quantities = []
    if "count_ordinal" in ux:
        quantities.append(("count_ordinal", "rule 1: |count - 5| (ordinal)", ux["count_ordinal"]))
    if "s3_neg" in ux:
        quantities.append(("s3_ratio", "rule 3 S3: -(lowest / above ratio)", ux["s3_neg"]))
    if "r2_absz_max" in ux:
        quantities.append(("rule2_absz_max", "rule 2: max |z| over pelvis features", ux["r2_absz_max"]))
    for f in feats:
        k = f + "_absz"
        if k in ux:
            quantities.append((k, "rule 2: |z| " + f.replace("rule2_", ""), ux[k]))
    if "rib_len_neg" in ux:
        quantities.append(("rib_length_min", "rule 3 S1: -(min rib length at the lowest level)", ux["rib_len_neg"]))
    aucs, curves = [], []
    for qkey, qlabel, ser in quantities:
        j = T.join(ser.rename("q"), how="left")
        for tgt in ["pooled"] + SUBTYPES:
            if tgt == "pooled":
                pos = j["pooled_pos"] == 1; neg = j["pooled_neg"] == 1
            else:
                pos = j["truth_" + tgt].astype(str) == "1"; neg = (j["truth_" + tgt].astype(str) == "0") & (j["pooled_neg"] == 1)
            res = auc_hanley(j.loc[pos, "q"].to_numpy(dtype=float), j.loc[neg, "q"].to_numpy(dtype=float))
            aucs.append({"quantity": qkey, "quantity_label": qlabel, "target": tgt, "auc": res["auc"],
                         "auc_lo": res["lo"], "auc_hi": res["hi"], "n_pos": res["n_pos"], "n_neg": res["n_neg"]})
            for i, (fpr, tpr) in enumerate(res["curve"]):
                curves.append({"quantity": qkey, "target": tgt, "i": i, "fpr": fpr, "tpr": tpr})
    return (pd.DataFrame(aucs, columns=["quantity", "quantity_label", "target", "auc", "auc_lo", "auc_hi", "n_pos", "n_neg"]),
            pd.DataFrame(curves, columns=["quantity", "target", "i", "fpr", "tpr"]))


def prevalence_windows(ust: pd.DataFrame, ux: dict, avail: dict) -> pd.DataFrame:
    rows = []
    for w in WINDOWS:
        k = w["key"]
        num = den = None; note = ""
        if k == "thirteen_rib_bearing" or k == "eleven_rib_bearing":
            if "n_thoracic" in ux:
                v = ux["n_thoracic"]
                den = int(v.notna().sum()); num = int((v == (13 if k.startswith("thirteen") else 11)).sum())
                note = "n_thoracic_rib_bearing (whole cage in field) per unit"
            else:
                note = "not computable: no n_thoracic_rib_bearing column (the cage is not counted in an abdominopelvic field)"
        elif k == "lumbar_rib":
            if "lumbar_rib_ind" in ux and "count_ran" in ux:
                den = int(ux["count_ran"].sum()); num = int((ux["lumbar_rib_ind"] & ux["count_ran"]).sum())
                note = "flags contain lumbar_rib, or last_rib_level is a lumbar id (20-25); denominator: units with a rule-1 count"
            else:
                note = "not computable: neither a lumbar_rib flag nor last_rib_level is in the census"
        elif k == "stump_any":
            if avail.get("R3_S1") == "available":
                ran = ust["R3_S1"] != "cannot_run"
                den = int(ran.sum()); num = int(ux["stump_ind"].reindex(ust.index).fillna(False).astype(bool).sum())
                note = "STUMP on >= 1 side at the lowest level; denominator: units where rule 3 S1 ran"
            else:
                note = "not computable: " + avail.get("R3_S1", "rule 3 S1 unavailable")
        elif k == "l6_count_six":
            if "count_ran" in ux:
                den = int(ux["count_ran"].sum())
                six = ux["count_six"].copy()
                if avail.get("R4") == "available":
                    six = six & ~(ust["R4"].reindex(six.index) == "fires")
                    note = "count six and rule 4 not thoracic; denominator: units with a rule-1 count"
                else:
                    note = "count six (rule 4 unavailable, so rib-less T12 spines are inside this number); denominator: units with a rule-1 count"
                num = int(six.sum())
            else:
                note = "not computable: no count column"
        if num is None or den is None or den == 0:
            status, pct, lo, hi = "not_computable", float("nan"), float("nan"), float("nan")
            if den == 0:
                note = (note + "; denominator zero").strip("; ")
        else:
            pct = 100.0 * num / den
            lo, hi = wilson(num, den)
            status = "pass" if w["lo"] <= pct <= w["hi"] else "fail"
        rows.append({"window": k, "label": w["label"], "window_lo_pct": w["lo"], "window_hi_pct": w["hi"],
                     "published_point_pct": w["point"], "source": w["source"], "numerator": num, "denominator": den,
                     "census_pct": pct, "wilson_lo_pct": 100 * lo if not math.isnan(lo) else float("nan"),
                     "wilson_hi_pct": 100 * hi if not math.isnan(hi) else float("nan"), "status": status, "note": note})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------------------------------------------------
CSS = """
:root{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--line:#e4e3df;--s1:#2a78d6;--s2:#eb6834;--good:#0ca30c;--crit:#d03b3b;--warn:#fab219;--grid:#eeede9}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--line:#3a3a37;--s1:#3987e5;--s2:#d95926;--grid:#2a2a28}}
:root[data-theme="dark"]{--bg:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--line:#3a3a37;--s1:#3987e5;--s2:#d95926;--grid:#2a2a28}
html,body{background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0}
main{max-width:1100px;margin:0 auto;padding:16px}
h1{font-size:1.5rem;margin:.2rem 0}h2{font-size:1.2rem;margin:1.6rem 0 .4rem;border-bottom:1px solid var(--line);padding-bottom:.2rem}h3{font-size:1rem;margin:1rem 0 .3rem}
p,li{max-width:70ch}.muted{color:var(--ink2)}.small{font-size:.85rem}
.wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.4rem 0 1rem}
table{border-collapse:collapse;font-size:.85rem;font-variant-numeric:tabular-nums;min-width:100%}
th,td{padding:4px 8px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap;vertical-align:top}
th{color:var(--ink2);font-weight:600;position:sticky;top:0;background:var(--bg)}
td.num,th.num{text-align:right}
.badge{display:inline-block;padding:1px 7px;border-radius:9px;font-size:.78rem;border:1px solid var(--line)}
.pass{border-color:var(--good);color:var(--good)}.fail{border-color:var(--crit);color:var(--crit)}.nc{border-color:var(--warn)}
.statement{border-left:3px solid var(--s1);padding:.4rem .8rem;margin:.6rem 0;background:color-mix(in srgb,var(--s1) 6%,transparent)}
.statement.no{border-left-color:var(--crit);background:color-mix(in srgb,var(--crit) 6%,transparent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
svg{width:100%;height:auto;display:block}
figure{margin:0 0 1rem}figcaption{font-size:.85rem;color:var(--ink2)}
code{font-size:.85em;word-break:break-all}
"""


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def fmt(x, nd=3) -> str:
    if x is None:
        return ""
    if isinstance(x, (float, np.floating)):
        if math.isnan(x):
            return "n/a"
        return ("%%.%df" % nd) % x
    return esc(x)


def table_html(df: pd.DataFrame, tid: str, cols: list[str] | None = None, nd=3, max_rows=None) -> str:
    if df is None or len(df) == 0:
        return '<div class="wrap"><table id="%s"><tr><td class="muted">empty</td></tr></table></div>' % tid
    cols = cols or list(df.columns)
    d = df[cols] if max_rows is None else df[cols].head(max_rows)
    h = ['<div class="wrap"><table id="%s"><thead><tr>' % tid]
    for c in cols:
        num = pd.api.types.is_numeric_dtype(d[c])
        h.append('<th class="%s">%s</th>' % ("num" if num else "", esc(c)))
    h.append("</tr></thead><tbody>")
    for _, r in d.iterrows():
        h.append("<tr>")
        for c in cols:
            v = r[c]
            num = isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool)
            if c == "status":
                cls = {"pass": "pass", "fail": "fail"}.get(str(v), "nc")
                h.append('<td><span class="badge %s">%s</span></td>' % (cls, esc(v)))
            else:
                h.append('<td class="%s">%s</td>' % ("num" if num else "", fmt(v, nd) if num else esc(v)))
        h.append("</tr>")
    h.append("</tbody></table></div>")
    if max_rows is not None and len(df) > max_rows:
        h.append('<p class="small muted">first %d of %d rows; the full table is tables/%s.csv</p>' % (max_rows, len(df), tid))
    return "".join(h)


def svg_roc(curve: list[tuple[float, float]], title: str, auc: float, n_pos: int, n_neg: int) -> str:
    W, H, m = 160, 160, 22
    def X(v): return m + v * (W - 2 * m)
    def Y(v): return H - m - v * (H - 2 * m)
    pts = " ".join("%.1f,%.1f" % (X(f), Y(t)) for f, t in curve) if curve else ""
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, H, esc(title))]
    s.append('<title>%s: AUC %s, %d positives, %d negatives</title>' % (esc(title), fmt(auc), n_pos, n_neg))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="var(--line)"/>' % (m, m, W - 2 * m, H - 2 * m))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)"/>' % (X(0), Y(0), X(1), Y(1)))
    if pts:
        s.append('<polyline points="%s" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round"/>' % pts)
    s.append('<text x="%d" y="13" font-size="10" fill="var(--ink2)">%s</text>' % (m, esc(title[:26])))
    s.append('<text x="%d" y="%d" font-size="11" fill="var(--ink)">AUC %s</text>' % (m + 4, H - m - 6, fmt(auc, 2)))
    s.append('<text x="%d" y="%d" font-size="8" fill="var(--ink2)">n+ %d / n- %d</text>' % (m + 4, H - m - 16 + 20, n_pos, n_neg))
    s.append("</svg>")
    return "".join(s)


def svg_sweep(sw: pd.DataFrame, spot: dict, min_sens: float) -> str:
    W, H, m = 560, 320, 40
    def X(v): return m + v * (W - 2 * m)
    def Y(v): return H - m - v * (H - 2 * m)
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="sweep: specificity against sensitivity per configuration">' % (W, H)]
    s.append('<title>each dot is one flag configuration; the outlined dot is the pre-stated sweet spot</title>')
    for g in (0, .25, .5, .75, 1):
        s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--grid)"/>' % (X(0), Y(g), X(1), Y(g)))
        s.append('<text x="%.1f" y="%.1f" font-size="10" fill="var(--ink2)" text-anchor="end">%.2f</text>' % (X(0) - 4, Y(g) + 3, g))
        s.append('<text x="%.1f" y="%.1f" font-size="10" fill="var(--ink2)" text-anchor="middle">%.2f</text>' % (X(g), H - m + 14, g))
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--crit)" stroke-width="1"/>' % (X(0), Y(min_sens), X(1), Y(min_sens)))
    s.append('<text x="%.1f" y="%.1f" font-size="10" fill="var(--crit)">sensitivity %.2f bar</text>' % (X(0) + 4, Y(min_sens) - 4, min_sens))
    s.append('<text x="%.1f" y="%d" font-size="11" fill="var(--ink2)" text-anchor="middle">specificity (evaluable read negatives)</text>' % (X(.5), H - 6))
    s.append('<text x="12" y="%.1f" font-size="11" fill="var(--ink2)" text-anchor="middle" transform="rotate(-90 12 %.1f)">sensitivity (read positives)</text>' % (Y(.5), Y(.5)))
    for _, r in sw.iterrows():
        sp, se = r["pooled__spec"], r["pooled__sens"]
        if pd.isna(sp) or pd.isna(se):
            continue
        s.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--s1)" fill-opacity=".55"><title>%s: sens %.3f, spec %.3f, PPV %s</title></circle>' % (
            X(sp), Y(se), esc(r["config"]), se, sp, fmt(r["pooled__ppv"])))
    if spot.get("reached") and not math.isnan(spot.get("spec", float("nan"))):
        s.append('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="var(--ink)" stroke-width="2"><title>sweet spot: %s</title></circle>' % (
            X(spot["spec"]), Y(spot["sens"]), esc(spot["config"])))
        s.append('<text x="%.1f" y="%.1f" font-size="10" fill="var(--ink)" text-anchor="end">%s</text>' % (
            X(spot["spec"]) - 12, Y(spot["sens"]) + 4, esc(spot["config"][:40])))
    s.append("</svg>")
    return "".join(s)


def svg_contrib(cdf: pd.DataFrame) -> str:
    if cdf is None or cdf.empty or "target" not in cdf.columns:
        return ""
    d = cdf[cdf.target == "pooled"].reset_index(drop=True)
    if d.empty:
        return ""
    n = len(d)
    W, m_l, m_r, m_t, m_b = 560, 40, 10, 24, 60
    bw = (W - m_l - m_r) / max(n, 1)
    H = 260
    plot_h = H - m_t - m_b
    def Y(v): return m_t + (1 - v) * plot_h
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="census flagged share with and without each rule">' % (W, H)]
    s.append('<title>census flagged share: the full union (blue) and the union without the rule (orange)</title>')
    for g in (0, .25, .5, .75, 1):
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--grid)"/>' % (m_l, Y(g), W - m_r, Y(g)))
        s.append('<text x="%d" y="%.1f" font-size="10" fill="var(--ink2)" text-anchor="end">%d%%</text>' % (m_l - 4, Y(g) + 3, int(g * 100)))
    for i, r in d.iterrows():
        x0 = m_l + i * bw + bw * 0.15
        w = bw * 0.3
        for j, (col, tok) in enumerate((("census_flagged_share_with", "--s1"), ("census_flagged_share_without", "--s2"))):
            v = float(r[col]) if not pd.isna(r[col]) else 0.0
            x = x0 + j * (w + 2)
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="var(%s)"><title>%s, %s: %.1f%%</title></rect>' % (
                x, Y(v), w, plot_h * v, tok, esc(r["rule"]), "with" if j == 0 else "without", 100 * v))
        s.append('<text x="%.1f" y="%d" font-size="10" fill="var(--ink2)" text-anchor="middle">%s</text>' % (m_l + i * bw + bw / 2, H - m_b + 14, esc(r["rule"])))
    s.append('<rect x="%d" y="%d" width="10" height="10" rx="2" fill="var(--s1)"/><text x="%d" y="%d" font-size="10" fill="var(--ink2)">flagged share, all rules</text>' % (m_l, H - 24, m_l + 14, H - 15))
    s.append('<rect x="%d" y="%d" width="10" height="10" rx="2" fill="var(--s2)"/><text x="%d" y="%d" font-size="10" fill="var(--ink2)">without this rule</text>' % (m_l + 190, H - 24, m_l + 204, H - 15))
    s.append("</svg>")
    return "".join(s)


def render_html(ctx: dict) -> str:
    H = ctx["header"]
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             "<title>Rule report</title><style>%s</style></head><body><main>" % CSS]
    parts.append("<h1>Transitional-vertebra rules: contribution, sweep, ROC, prevalence windows</h1>")
    parts.append('<p class="muted small">PREREG_rules.md status <b>%s</b>. Every number here is calibration until the freeze line is filled.</p>' % esc(H["prereg_status"]))
    # header
    parts.append("<h2>0. Header</h2>")
    hdf = pd.DataFrame([{"field": k, "value": v} for k, v in H.items() if k != "inputs_sha256"] +
                       [{"field": "input " + k, "value": v} for k, v in ctx["inputs"].items()])
    parts.append(table_html(hdf, "header"))
    # truth summary
    parts.append("<h2>1. Read-tier truth</h2>")
    parts.append('<p>Units are %ss. Truth comes only from the read tiers: the CTSP two-radiologist Castellvi consensus and Lumbosac counts, '
                 'Loeffler 2021 Suppl. Table 1 (VerSe), lstv_flag_labels_v2 (LSTV flag both cohorts; TLTV flag verse only, the CTSP TLTV flag is label-derived), '
                 'and registry rows with truth_tier == read. A subtype a read never assessed is blank, not negative. '
                 'A read positive from any read source stands; a conflict between read sources is listed in tables/truth_conflicts.csv (%d).</p>' % (
                     esc(ctx["unit"]), ctx["n_conflicts"]))
    parts.append(table_html(ctx["truth_summary"], "truth_summary"))
    # rule availability
    parts.append("<h2>2. Rules and their states on the census</h2>")
    parts.append(table_html(ctx["rule_states"], "rule_states"))
    if ctx["r2_info"]["features"]:
        parts.append('<p class="small muted">Rule 2 reference half: %d units (adults, count five, prior and registry ordinary, even hash of the person key); test half %d. Thresholds are the reference half\'s 2.5th and 97.5th percentiles per feature and are written to summary.json.</p>' % (
            ctx["r2_info"]["n_reference"], ctx["r2_info"]["n_test"]))
    # contribution
    parts.append("<h2>3. Per-rule contribution</h2>")
    parts.append('<p>For each rule: the census share flagged by the union of all available rules, the share without this rule, the read-tier sensitivity and specificity with and without it, and the read-tier positives that only this rule catches.</p>')
    parts.append('<figure>%s<figcaption>Census flagged share with every rule (blue) and without the named rule (orange). Pooled over subtypes.</figcaption></figure>' % svg_contrib(ctx["contribution"]))
    parts.append(table_html(ctx["contribution"], "contribution"))
    # sweep
    parts.append("<h2>4. The sweep and the sweet spot</h2>")
    parts.append('<p>Every non-empty subset of the available rules%s. Sensitivity is on read-tier positives with a positive the screen could not evaluate counted as missed; specificity is on evaluable read-tier negatives. Wilson 95 %% intervals. '
                 'The sweet spot is defined before the sweep as the configuration with the highest specificity subject to sensitivity &ge; %.2f.</p>' % (
                     "; rule 3 S3 over the grid of ratio cuts %s" % esc(ctx["s3_grid_txt"]) if ctx["s3_grid_txt"] else " (S3 enters no configuration: no calibrated cut)", ctx["min_sens"]))
    for tgt in ["pooled"] + SUBTYPES:
        sp = ctx["spots"][tgt]
        parts.append('<div class="statement %s" id="spot_%s"><b>%s.</b> %s</div>' % ("" if sp.get("reached") else "no", esc(tgt), esc(SUBTYPE_LABEL.get(tgt, tgt)), esc(sp["statement"])))
    parts.append('<figure>%s<figcaption>Each dot is one configuration (pooled). The outlined dot is the sweet spot where one exists.</figcaption></figure>' % svg_sweep(ctx["sweep"], ctx["spots"]["pooled"], ctx["min_sens"]))
    parts.append("<h3>Sweet spot per target</h3>")
    parts.append(table_html(ctx["sweet_spot"], "sweet_spot"))
    parts.append("<h3>All configurations, best specificity first among those meeting the bar</h3>")
    swcols = ["config", "n_rules", "pooled__sens", "pooled__sens_lo", "pooled__sens_hi", "pooled__spec", "pooled__spec_lo", "pooled__spec_hi",
              "pooled__ppv", "pooled__tp", "pooled__fn", "pooled__fp", "pooled__tn", "census_flagged_share"] + ["%s__sens" % s for s in SUBTYPES]
    parts.append(table_html(ctx["sweep_sorted"], "sweep", cols=[c for c in swcols if c in ctx["sweep_sorted"].columns], max_rows=80))
    # ROC
    parts.append("<h2>5. ROC from the continuous quantities</h2>")
    parts.append('<p>Higher score = more anomalous. AUC by the Mann-Whitney statistic with Hanley-McNeil 95 %% intervals; positives and negatives as in the sweep, per subtype against the read negatives assessed for that subtype.</p>')
    aucs = ctx["roc_auc"]
    curves = ctx["roc_curves"]
    if len(aucs):
        for q in aucs.quantity.unique():
            lab = aucs[aucs.quantity == q].quantity_label.iloc[0]
            parts.append("<h3>%s</h3><div class=\"grid\">" % esc(lab))
            for tgt in ["pooled"] + SUBTYPES:
                a = aucs[(aucs.quantity == q) & (aucs.target == tgt)]
                if a.empty:
                    continue
                a = a.iloc[0]
                cv = curves[(curves.quantity == q) & (curves.target == tgt)].sort_values("i")
                parts.append(svg_roc(list(zip(cv.fpr, cv.tpr)), SUBTYPE_LABEL.get(tgt, tgt), a["auc"], int(a["n_pos"]), int(a["n_neg"])))
            parts.append("</div>")
    parts.append(table_html(aucs, "roc_auc"))
    # windows
    parts.append("<h2>6. Prevalence windows (outside check)</h2>")
    parts.append('<p>The census rate (all units, not the read tier) must fall inside the published window or the rule is suspect before it is believed. Pass / fail is on the point estimate as PREREG states it; the Wilson interval is beside it. A window whose ingredients are not in the census is not_computable, which is not a pass.</p>')
    parts.append(table_html(ctx["windows"], "prevalence_windows", nd=2))
    # notes
    parts.append("<h2>7. Notes and limits</h2><ul>")
    for n in ctx["notes"]:
        parts.append("<li>%s</li>" % esc(n))
    parts.append("</ul>")
    parts.append('<p class="small muted">tool %s v%s · git %s · %s</p>' % (esc(H["tool"]), esc(H["tool_version"]), esc(H["git_sha"]), esc(H["utc_time"])))
    parts.append("</main></body></html>")
    return "".join(parts)


# ----------------------------------------------------------------------------------------------------------------------
# main pipeline
# ----------------------------------------------------------------------------------------------------------------------
def run(args) -> dict:
    out = Path(args.out); (out / "tables").mkdir(parents=True, exist_ok=True)
    census_path = Path(args.census)
    prereg = Path(args.prereg)
    if not prereg.exists():
        raise SystemExit("PREREG file not found: %s" % prereg)
    truth, used = build_truth(args)
    inputs = {"census": census_path, "prereg": prereg, **used}
    if args.s3_calib:
        inputs["s3_calib"] = Path(args.s3_calib)
    inputs_sha = {k: sha256_file(p) for k, p in inputs.items()}
    header = {"prereg_sha256": inputs_sha["prereg"], "prereg_status": PREREG_STATUS, "git_sha": git_sha(REPO),
              "tool": TOOL, "tool_version": TOOL_VERSION, "utc_time": utc_now(),
              "inputs_sha256": ";".join("%s=%s" % (k, v) for k, v in inputs_sha.items())}

    df, cols = load_census(census_path)
    feats = rule2_features(df)
    z, r2_info = rule2_zscores(df, cols, feats)
    s3_cut = args.s3_cut
    if args.s3_calib:
        s3_cut = float(json.loads(Path(args.s3_calib).read_text())["s3_cut"])
    s3_grid = []
    if s3_cut is not None:
        if args.s3_grid:
            lo, hi, step = (float(x) for x in args.s3_grid.split(":"))
            s3_grid = [round(x, 3) for x in np.arange(lo, hi + 1e-9, step)]
        else:
            s3_grid = [round(s3_cut + d, 3) for d in np.arange(-0.10, 0.10 + 1e-9, 0.02)]
        if round(s3_cut, 3) not in s3_grid:
            s3_grid.append(round(s3_cut, 3))
        s3_grid = sorted(set(s3_grid))
    st, avail = rule_states(df, cols, z, feats, s3_cut, s3_grid)
    # per-CT continuous quantities
    extra = {}
    if cols["count"]:
        c = pd.to_numeric(df[cols["count"]].replace("", np.nan), errors="coerce")
        extra["count_ordinal"] = (c - 5).abs()
        extra["count_ran"] = c.isin([4, 5, 6]).astype(int)
        extra["count_six"] = (c == 6).astype(int)
    if "_s3_ratio" in df.columns:
        extra["s3_neg"] = -df["_s3_ratio"]
    zc = [c for c in z.columns if c.endswith("_z")]
    if zc:
        extra["r2_absz_max"] = z[zc].abs().max(axis=1)
        for c in zc:
            extra[c.replace("_z", "_absz")] = z[c].abs()
    if cols["n_thoracic_rib_bearing"]:
        extra["n_thoracic"] = pd.to_numeric(df[cols["n_thoracic_rib_bearing"]].replace("", np.nan), errors="coerce")
    stump_ind = pd.Series(False, index=df.index)
    for side in ("stump_left", "stump_right"):
        if cols[side]:
            stump_ind |= df[cols[side]].astype(str).str.strip().str.upper() == "STUMP"
    extra["stump_ind"] = stump_ind.astype(int)
    lr = pd.Series(False, index=df.index)
    have_lr = False
    if cols["flags"]:
        lr |= df[cols["flags"]].astype(str).str.contains(r"(?:^|;)\s*lumbar_rib", regex=True); have_lr = True
    if cols["last_rib_level"]:
        lvl = pd.to_numeric(df[cols["last_rib_level"]].replace("", np.nan), errors="coerce")
        lr |= lvl.isin(list(LUMBAR_IDS)); have_lr = True
    if have_lr:
        extra["lumbar_rib_ind"] = lr.astype(int)
    for c in ("rib_length_left_last", "rib_length_right_last"):
        if c in df.columns:
            v = pd.to_numeric(df[c].replace("", np.nan), errors="coerce")
            extra["rib_len_neg"] = -v if "rib_len_neg" not in extra else np.fmax(extra["rib_len_neg"], -v)

    ust, ux, coll, n_ct = aggregate_units(df, cols, st, args.unit, extra)
    for k in ("count_ran", "count_six", "stump_ind", "lumbar_rib_ind"):
        if k in ux:
            ux[k] = ux[k].fillna(0).astype(bool)
    T = truth.frame().set_index("unit_key") if truth.rows else pd.DataFrame(
        columns=["truth_" + s for s in SUBTYPES] + ["n_assessed", "pooled_pos", "pooled_neg", "truth_sources", "truth_notes"])
    # keep only truth units that exist in the census (a read of a CT the census does not hold cannot be scored)
    in_census = T.index.isin(ust.index)
    n_truth_not_in_census = int((~in_census).sum())
    T = T[in_census]

    rules = [r for r in RULES if avail.get(r, "").startswith("available")]
    grid_cols = ["R3_S3@%.3f" % g for g in s3_grid] if "R3_S3" in rules else []
    cdf, only_df = contribution(ust, T, rules) if rules and len(T) else (pd.DataFrame(), pd.DataFrame())
    sw, spots = sweep(ust, T, rules, grid_cols, args.min_sens) if rules and len(T) else (pd.DataFrame(), {t: {"target": t, "reached": False, "n_pos": 0, "statement": "no rules or no truth"} for t in ["pooled"] + SUBTYPES})
    aucs, curves = roc_tables(ux, T, feats) if len(T) else roc_tables({}, pd.DataFrame(columns=["pooled_pos", "pooled_neg"]), [])
    win = prevalence_windows(ust, ux, avail)

    # tables
    def stamp(d: pd.DataFrame) -> pd.DataFrame:
        d = d.copy()
        for k, v in header.items():
            d[k] = v
        return d
    rs_rows = []
    for r in RULES:
        rs_rows.append({"rule": r, "label": RULE_LABEL[r], "availability": avail.get(r, ""),
                        "n_fires": int((ust[r] == "fires").sum()) if r in ust else 0,
                        "n_silent": int((ust[r] == "silent").sum()) if r in ust else 0,
                        "n_cannot_run": int((ust[r] == "cannot_run").sum()) if r in ust else len(ust)})
    rs = pd.DataFrame(rs_rows)
    ts_rows = []
    for s in SUBTYPES:
        col = T["truth_" + s].astype(str) if len(T) else pd.Series(dtype=str)
        ts_rows.append({"subtype": s, "read_positives": int((col == "1").sum()), "read_negatives": int((col == "0").sum()),
                        "not_assessed": int(len(T) - (col == "1").sum() - (col == "0").sum())})
    ts_rows.append({"subtype": "pooled", "read_positives": int(T["pooled_pos"].sum()) if len(T) else 0,
                    "read_negatives": int(T["pooled_neg"].sum()) if len(T) else 0, "not_assessed": 0})
    tsum = pd.DataFrame(ts_rows)
    spot_df = pd.DataFrame([spots[t] for t in ["pooled"] + SUBTYPES])
    unit_flags = ust.copy()
    unit_flags.insert(0, "collection", coll.reindex(ust.index).fillna(""))
    unit_flags.insert(1, "n_ct", n_ct.reindex(ust.index).fillna(0).astype(int))
    if rules:
        f_all, e_all = config_columns(ust, tuple(rules))
        unit_flags["flag_all_rules"] = f_all.astype(int); unit_flags["evaluable_all_rules"] = e_all.astype(int)
        if spots["pooled"].get("reached"):
            cfg = tuple(spots["pooled"]["config"].split("+"))
            f_s, e_s = config_columns(ust, cfg)
            unit_flags["flag_sweet_spot"] = f_s.astype(int)
    unit_flags = unit_flags.join(T, how="left")
    sw_sorted = sw.copy()
    if len(sw):
        sw_sorted["meets_bar"] = (sw_sorted["pooled__sens"] >= args.min_sens).astype(int)
        sw_sorted = sw_sorted.sort_values(["meets_bar", "pooled__spec", "n_rules"], ascending=[False, False, True])
    tables = {"header": pd.DataFrame([header]), "truth_join": T.reset_index(), "truth_conflicts": pd.DataFrame(truth.conflicts),
              "rule_states": rs, "contribution": cdf, "only_caught_by": only_df, "sweep": sw_sorted, "sweet_spot": spot_df,
              "roc_auc": aucs, "roc_curves": curves, "prevalence_windows": win, "unit_flags": unit_flags.reset_index(),
              "truth_summary": tsum}
    for name, d in tables.items():
        stamp(d if d is not None else pd.DataFrame()).to_csv(out / "tables" / ("%s.csv" % name), index=False)

    notes = [
        "%d truth units are not in the census and were dropped from every denominator." % n_truth_not_in_census,
        "Unit = %s; a rule fires for a unit when it fires on any of its CTs; a unit is evaluable under a configuration when at least one of its rules could run." % args.unit,
        "A CT whose rule reads no_count / no_anchor is never counted as ordinary: it is not flagged and it is not a cleared negative.",
        "Rule 3 S3: " + avail.get("R3_S3", ""),
        "Rule 4: " + avail.get("R4", ""),
        "Rule 2: " + avail.get("R2", "") + "; the reference-half thresholds are in-sample for the reference half itself.",
        "The lstv_flag_labels_v2 TLTV flag is used for the verse cohort only; the CTSP TLTV flag equals manifest_has_lumbar_rib, which is label-derived.",
        "The L6 window holds rib-less T12 spines whenever rule 4 is unavailable; the thirteen / eleven windows need a whole-cage count that an abdominopelvic field cannot give.",
    ]
    summary = {**header, "unit": args.unit, "min_sens": args.min_sens, "n_census_ct": int(len(df)), "n_census_units": int(len(ust)),
               "n_truth_units": int(len(T)), "n_truth_units_not_in_census": n_truth_not_in_census,
               "n_truth_conflicts": len(truth.conflicts), "rules_available": rules, "rule_availability": avail,
               "s3_cut": s3_cut, "s3_grid": s3_grid, "rule2": r2_info, "truth_summary": ts_rows,
               "sweet_spot": spots, "prevalence_windows": win.to_dict(orient="records"),
               "roc_auc": aucs.to_dict(orient="records") if len(aucs) else [], "notes": notes,
               "n_configurations": int(len(sw))}
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=_json_default), encoding="utf-8")
    ctx = {"header": header, "inputs": {k: "%s (sha256 %s)" % (p, inputs_sha[k]) for k, p in inputs.items()}, "unit": args.unit,
           "n_conflicts": len(truth.conflicts), "truth_summary": tsum, "rule_states": rs, "r2_info": r2_info, "contribution": cdf,
           "sweep": sw, "sweep_sorted": sw_sorted, "spots": spots, "sweet_spot": spot_df, "roc_auc": aucs, "roc_curves": curves,
           "windows": win, "notes": notes, "min_sens": args.min_sens,
           "s3_grid_txt": ", ".join("%.3f" % g for g in s3_grid) if s3_grid else ""}
    (out / "report.html").write_text(render_html(ctx), encoding="utf-8")
    print("wrote %s (units %d, truth units %d, rules %s, configurations %d)" % (out, len(ust), len(T), rules, len(sw)))
    print("pooled sweet spot: %s" % spots["pooled"]["statement"])
    for tgt in SUBTYPES:
        print("  %s: %s" % (tgt, spots[tgt]["statement"]))
    for _, w in win.iterrows():
        print("  window %-22s %s  %s" % (w["window"], w["status"], "%.2f %% [%.2f, %.2f]" % (w["census_pct"], w["wilson_lo_pct"], w["wilson_hi_pct"]) if w["status"] != "not_computable" else w["note"]))
    return summary


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, float) and math.isnan(o):
        return None
    if isinstance(o, (set, tuple)):
        return list(o)
    if isinstance(o, Path):
        return str(o)
    return str(o)


# ----------------------------------------------------------------------------------------------------------------------
# self-test: a synthetic census with positives planted at the published prevalences
# ----------------------------------------------------------------------------------------------------------------------
def make_synthetic(root: Path, seed: int = 20260927, n: int = 2000) -> dict:
    """Writes census.tsv and the four truth files in their real formats. Returns the planted expectations, computed
    here by a direct count (a second, simpler code path than the report's)."""
    rng = np.random.default_rng(seed)
    root.mkdir(parents=True, exist_ok=True)
    # planted prevalences (percent of persons)
    P = {"L6": 3.5, "T13": 0.6, "four_lumbar_or_fused_L5": 2.6, "castellvi_II_IV": 5.0, "lumbar_rib": 1.5, "stump_rib": 16.0}
    # persons: ctsp-like 700, verse-like 400 (of which 60 with two series), other 900
    persons = []
    for i in range(700):
        persons.append(("ctsp", "%04d" % (i + 1), "ctsp:%04d" % (i + 1), 1))
    for i in range(400):
        persons.append(("verse", "verse%03d" % (i + 1), "verse:verse%03d" % (i + 1), 2 if i < 60 else 1))
    for i in range(n - 700 - 400 - 60):
        persons.append(("abdomenatlas3_mini", "BDMAP_%08d" % (i + 1), "abdomenatlas3_mini:BDMAP_%08d" % (i + 1), 1))
    recs = []
    n_t13 = 0
    for idx, (coll, cid, pk, nct) in enumerate(persons):
        t = {s: 0 for s in SUBTYPES}
        for s in SUBTYPES:
            if s != "T13" and rng.random() < P[s] / 100:
                t[s] = 1
        # T13 is planted deterministically on verse persons (every 60th) so the per-subtype 'no configuration
        # reaches 0.95' branch is exercised: half of them get a stump call, the other half none
        if coll == "verse" and idx % 60 == 17:
            t["T13"] = 1; t["L6"] = 0; n_t13 += 1
        pos = any(t.values())
        # field of view: about 12 % of persons have a cut field; a read then assesses nothing at the cut junction
        cut_ls = rng.random() < 0.06
        cut_tl = rng.random() < 0.06
        if t["T13"]:
            cut_tl = False
        # what a read could see: a positive at a cut junction is not a read positive
        tr = {s: (t[s] if not (cut_ls if s in LS_SUBTYPES else cut_tl) else 0) for s in SUBTYPES}
        read = (coll == "ctsp" and (pos or rng.random() < 0.05)) or (coll == "verse" and (t["T13"] or rng.random() < 0.85)) \
            or (coll.startswith("abdomen") and rng.random() < 0.10)
        recs.append({"coll": coll, "cid": cid, "pk": pk, "nct": nct, "t": t, "tr": tr, "cut_ls": cut_ls, "cut_tl": cut_tl,
                     "read": read, "t13_ord": n_t13})
    # rule outputs per person (all CTs of a person share them, except a second series that is always a cut field)
    fires = {r: {} for r in ["R1_count", "R1_anchor", "R3_S1", "R4"]}
    ran = {r: {} for r in ["R1_count", "R1_anchor", "R3_S1"]}
    pp = {}
    rows = []
    thoracic_counts = {}
    for p in recs:
        t = p["t"]
        count = "5"; flags = []; stump_l = "FULL"; stump_r = "FULL"; s3 = float(rng.normal(0.68, 0.08)); r4 = ""; last_rib = 19
        if p["cut_ls"]:
            count = "no_count"
        else:
            # planted catch rates 0.99: the sweep must be able to reach the 0.95 bar on the planted configuration
            if t["L6"]:
                count = "6" if rng.random() < 0.99 else "5"
            elif t["four_lumbar_or_fused_L5"]:
                count = "4" if rng.random() < 0.99 else "5"
            elif rng.random() < 0.02:
                count = str(rng.choice(["4", "6"]))
            if t["four_lumbar_or_fused_L5"] and rng.random() < 0.99:
                flags.append("complete_sacralisation_candidate")
            if t["castellvi_II_IV"]:
                if rng.random() < 0.99:
                    flags.append("lumbarisation_candidate" if rng.random() < 0.5 else "complete_sacralisation_candidate")
                else:
                    flags.append("castellvi_II_IV_candidate")
            elif rng.random() < 0.02:
                flags.append("lumbarisation_candidate")
        if p["cut_tl"]:
            # the count needs the lowest rib-bearing vertebra: a cut thoraco-lumbar junction is no_count too
            stump_l = stump_r = ""; s3 = float("nan"); count = "no_count"
        else:
            if t["stump_rib"] or t["lumbar_rib"] or t["T13"]:
                caught = (rng.random() < 0.99) if (t["stump_rib"] or t["lumbar_rib"]) else (p["t13_ord"] % 2 == 1)
                if caught:
                    stump_l = "STUMP"; s3 = float(rng.normal(0.35, 0.10))
                    if rng.random() < 0.65:
                        stump_r = "STUMP"
                if t["lumbar_rib"]:
                    last_rib = 20
            elif rng.random() < 0.02:
                stump_r = "STUMP"; s3 = float(rng.normal(0.35, 0.10))
            elif rng.random() < 0.03:
                stump_l = "UNDECIDED"
        if count == "6":
            r4 = "thoracic" if rng.random() < 0.10 else "lumbar"
        # rule-2 features: fused L5 raises the sacral top; everything else normal noise
        f_top = float(rng.normal(0, 6)) + (18.0 if (t["four_lumbar_or_fused_L5"] and rng.random() < 0.5) else 0.0)
        f_ala = float(rng.normal(110, 8))
        f_ratio = float(rng.normal(1.05, 0.08))
        if p["cut_ls"]:
            f_top = f_ala = f_ratio = float("nan")
        # whole cage count for 30 % of persons (the windows check); eleven is planted OUTSIDE 4.5-8.0 so one window fails
        n_thor = ""
        if rng.random() < 0.30:
            u = rng.random()
            n_thor = "13" if u < 0.006 else ("11" if u < 0.006 + 0.12 else "12")
            thoracic_counts[p["pk"]] = int(n_thor)
        fires["R1_count"][p["pk"]] = count in ("4", "6")
        fires["R1_anchor"][p["pk"]] = any(f in ("complete_sacralisation_candidate", "lumbarisation_candidate") for f in flags)
        fires["R3_S1"][p["pk"]] = "STUMP" in (stump_l, stump_r)
        fires["R4"][p["pk"]] = r4 == "thoracic"
        ran["R1_count"][p["pk"]] = count in ("4", "5", "6")
        ran["R1_anchor"][p["pk"]] = fires["R1_anchor"][p["pk"]] or count in ("4", "5", "6")
        ran["R3_S1"][p["pk"]] = any(x in ("FULL", "STUMP", "ABSENT") for x in (stump_l, stump_r))
        pp[p["pk"]] = {"count": count, "r4": r4, "stump": "STUMP" in (stump_l, stump_r), "last_rib": last_rib if not p["cut_tl"] else None}
        child = "1" if rng.random() < 0.02 else "0"
        for k in range(p["nct"]):
            cid = p["cid"] if k == 0 else p["cid"] + "_b"
            row = {"case_key": "%s:%s" % (p["coll"], cid), "collection": p["coll"], "case_id": cid, "person_key": p["pk"],
                   "count": count if k == 0 else "no_count", "anchor_source": "ts_sacrum_union_s1" if count != "no_count" else "",
                   "flags": ";".join(flags) if k == 0 else "", "stump_left": stump_l if k == 0 else "", "stump_right": stump_r if k == 0 else "",
                   "s3_ratio": ("%.4f" % s3) if (k == 0 and not math.isnan(s3)) else "", "rule4_decision": r4 if k == 0 else "",
                   "child": child, "last_rib_level": str(last_rib) if (k == 0 and not p["cut_tl"]) else "",
                   "n_thoracic_rib_bearing": n_thor if k == 0 else "",
                   "rule2_sacral_top_vs_crest_mm": ("%.2f" % f_top) if (k == 0 and not math.isnan(f_top)) else "",
                   "rule2_ala_width_mm": ("%.2f" % f_ala) if (k == 0 and not math.isnan(f_ala)) else "",
                   "rule2_plate_width_ratio": ("%.3f" % f_ratio) if (k == 0 and not math.isnan(f_ratio)) else "",
                   "prior_subtype": "none", "registry_subtype": "none", "truth_tier": "read" if p["read"] else "none"}
            rows.append(row)
    census = pd.DataFrame(rows)
    census.to_csv(root / "census.tsv", sep="\t", index=False)
    # R2 fires: the report computes it from the reference half; for the expectation we recompute it the same way
    # below from the written census (it is a threshold on the written numbers, so no second definition exists).
    # ---- truth files in the real formats
    cc, ls, vs, lf, rg = [], [], [], [], []
    tok = 0
    for p in recs:
        if not p["read"]:
            continue
        t = p["tr"]  # the truth files carry what a read could see
        both_cut = p["cut_ls"] and p["cut_tl"]
        if p["coll"] == "ctsp":
            tok += 1
            grade = ("IIIb" if rng.random() < 0.5 else "IIa") if t["castellvi_II_IV"] else ("Ib" if rng.random() < 0.1 else "0")
            if p["cut_ls"]:
                grade = ""
            comment = "b/l Rudimentary Ribs at T12 or hypoplastic ribs" if t["stump_rib"] else ""
            cc.append({"volume_id": p["cid"], "token": str(tok), "read_1_NA": grade, "read_2_MI": grade, "agreement": "True",
                       "consensus": grade, "comment": comment})
            cnt = "6" if t["L6"] else ("4" if t["four_lumbar_or_fused_L5"] else "5")
            if not p["cut_ls"]:
                ls.append({"": "", "Name": "Token %d" % tok, "Non-rib/lumbar type bearing vertebra #": cnt,
                           "1st Reviewer NA": grade, "2nd reviewer MI": grade, "Describe or comments (optional)": "", "3rd reviewer": ""})
            lf.append({"volume_id": p["cid"], "cohort": "ctsp",
                       "LSTV_flag": "" if p["cut_ls"] else str(int(t["castellvi_II_IV"] or t["L6"] or t["four_lumbar_or_fused_L5"])),
                       "TLTV_flag": str(int(t["lumbar_rib"])), "lstv_label": "lumbarization (6 lumbar)" if t["L6"] else "", "castellvi_type": ""})
            # the registry also carries the CTSP reads (as it does on disk)
            st = "L6" if t["L6"] else ("sacralised_L5_fused" if t["four_lumbar_or_fused_L5"] else ("castellvi_I_II" if t["castellvi_II_IV"] else "none"))
            rg.append({"patient_key": p["pk"], "subtype": "no_count" if both_cut else st, "truth_tier": "read", "castellvi": grade,
                       "four_lumbar": str(t["four_lumbar_or_fused_L5"] == 1), "lumbar_rib": str(t["lumbar_rib"] == 1),
                       "junction_tl_in_fov": str(not p["cut_tl"]), "junction_ls_in_fov": str(not p["cut_ls"]),
                       "notes": "read stump rib at T12" if t["stump_rib"] else ""})
        elif p["coll"] == "verse":
            vid = str(int(p["cid"].replace("verse", "")))
            stump = "" if p["cut_tl"] else ("L1" if t["lumbar_rib"] else ("T13" if (t["T13"] and t["stump_rib"]) else ("T12" if t["stump_rib"] else "0")))
            tle = "" if p["cut_tl"] else ("2" if t["T13"] else "0")
            lse = "" if p["cut_ls"] else ("2" if t["L6"] else ("1" if t["four_lumbar_or_fused_L5"] else "0"))
            cg = "" if p["cut_ls"] else (("3b" if rng.random() < 0.5 else "2a") if t["castellvi_II_IV"] else "0/1")
            seg = "7/%s/%s/5" % ("13" if t["T13"] else "12", "6" if t["L6"] else ("4" if t["four_lumbar_or_fused_L5"] else "5"))
            vs.append({"verse_id": vid, "thoracolumbar_enumeration": tle, "thoracolumbar_stump_ribs": stump,
                       "thoracolumbar_transition_vertebra": "", "lumbosacral_enumeration": lse, "castellvi_grading": cg,
                       "assumed_segment_structure": seg})
            lf.append({"volume_id": p["cid"], "cohort": "verse", "LSTV_flag": "" if p["cut_ls"] else str(int(t["L6"] or t["castellvi_II_IV"] or t["four_lumbar_or_fused_L5"])),
                       "TLTV_flag": "" if p["cut_tl"] else str(int(t["T13"] or t["stump_rib"] or t["lumbar_rib"])), "lstv_label": "", "castellvi_type": ""})
        else:
            st = "L6" if t["L6"] else ("T13" if t["T13"] else ("sacralised_L5_fused" if t["four_lumbar_or_fused_L5"] else ("lumbar_rib" if t["lumbar_rib"] else "none")))
            rg.append({"patient_key": p["pk"], "subtype": "no_count" if both_cut else st, "truth_tier": "read",
                       "castellvi": ("IIb" if t["castellvi_II_IV"] else ("0" if not p["cut_ls"] else "")),
                       "four_lumbar": str(t["four_lumbar_or_fused_L5"] == 1), "lumbar_rib": str(t["lumbar_rib"] == 1),
                       "junction_tl_in_fov": str(not p["cut_tl"]), "junction_ls_in_fov": str(not p["cut_ls"]),
                       "notes": "read stump rib at L1" if t["stump_rib"] else ""})
    # registry rows that are not read tier must be ignored: add some
    for i in range(50):
        rg.append({"patient_key": "abdomenatlas3_mini:BDMAP_%08d" % (i + 1), "subtype": "L6", "truth_tier": "two-labeller", "castellvi": "",
                   "four_lumbar": "False", "lumbar_rib": "False", "junction_tl_in_fov": "True", "junction_ls_in_fov": "True", "notes": ""})
    pd.DataFrame(cc).to_csv(root / "castellvi_consensus.csv", index=False)
    pd.DataFrame(ls).to_csv(root / "Lumbosac.csv", index=False)
    pd.DataFrame(vs).to_csv(root / "verse_suppl_table1.csv", index=False)
    pd.DataFrame(lf).to_csv(root / "lstv_flag_labels_v2.csv", index=False)
    pd.DataFrame(rg).to_csv(root / "registry.csv", index=False)

    # ---- planted expectations by direct count over the read persons (a second, simpler code path than the report):
    # a read positive is a planted positive at a junction the read could see; a read negative is a read person with
    # no read positive and at least one junction in the read's field; evaluable = a planted rule could run.
    read_pos = {s: [p["pk"] for p in recs if p["read"] and p["tr"][s]] for s in SUBTYPES}
    pooled_pos = sorted({k for s in SUBTYPES for k in read_pos[s]})
    neg = [p["pk"] for p in recs if p["read"] and p["pk"] not in set(pooled_pos) and not (p["cut_ls"] and p["cut_tl"])]
    planted = ("R1_count", "R1_anchor", "R3_S1")

    def flagged(pk, cfg):
        return any(fires[r].get(pk, False) for r in cfg)

    def evaluable(pk, cfg):
        return any(ran[r].get(pk, False) for r in cfg)
    tp = sum(flagged(k, planted) for k in pooled_pos)
    fp = sum(flagged(k, planted) for k in neg)
    tn = sum((evaluable(k, planted) and not flagged(k, planted)) for k in neg)
    exp = {"planted_config": "+".join(planted), "n_pooled_pos": len(pooled_pos), "n_neg": len(neg),
           "sens": tp / len(pooled_pos), "spec": tn / (tn + fp), "tp": tp, "fp": fp, "tn": tn,
           "t13_sens": sum(flagged(k, planted) for k in read_pos["T13"]) / max(1, len(read_pos["T13"])),
           "n_t13": len(read_pos["T13"]), "n_thoracic": len(thoracic_counts)}
    # prevalence windows by direct count over ALL persons, statuses from the PREREG bounds
    bounds = {w["key"]: (w["lo"], w["hi"]) for w in WINDOWS}
    n13 = sum(v == 13 for v in thoracic_counts.values()); n11 = sum(v == 11 for v in thoracic_counts.values())
    count_ran = [k for k, v in pp.items() if v["count"] in ("4", "5", "6")]
    r3_ran = [k for k, v in ran["R3_S1"].items() if v]
    pcts = {"thirteen_rib_bearing": 100 * n13 / len(thoracic_counts), "eleven_rib_bearing": 100 * n11 / len(thoracic_counts),
            "lumbar_rib": 100 * sum(pp[k]["last_rib"] == 20 for k in count_ran) / len(count_ran),
            "stump_any": 100 * sum(pp[k]["stump"] for k in r3_ran) / len(r3_ran),
            "l6_count_six": 100 * sum((pp[k]["count"] == "6" and pp[k]["r4"] != "thoracic") for k in count_ran) / len(count_ran)}
    exp["window_pct"] = pcts
    exp["windows"] = {k: ("pass" if bounds[k][0] <= v <= bounds[k][1] else "fail") for k, v in pcts.items()}
    return exp


def selftest(keep: str | None) -> int:
    tmp = Path(keep) if keep else Path(tempfile.mkdtemp(prefix="rule_report_selftest_"))
    syn = tmp / "synthetic"
    exp = make_synthetic(syn)
    print("synthetic census written to %s; planted %s" % (syn, json.dumps({k: v for k, v in exp.items() if k != "windows"}, default=_json_default)))
    fails = []

    def check(cond, msg):
        print(("  ok   " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    # run 1: calibrated S3 cut, thoracic counts present
    ns = argparse.Namespace(census=str(syn / "census.tsv"), castellvi=str(syn / "castellvi_consensus.csv"), lumbosac=str(syn / "Lumbosac.csv"),
                            verse_suppl=str(syn / "verse_suppl_table1.csv"), lstv_flags=str(syn / "lstv_flag_labels_v2.csv"),
                            registry=str(syn / "registry.csv"), prereg=str(PREREG_DEFAULT), out=str(tmp / "run1"), s3_cut=0.50,
                            s3_calib=None, s3_grid=None, unit="person", min_sens=MIN_SENS_DEFAULT)
    S = run(ns)
    sp = S["sweet_spot"]["pooled"]
    check(sp["reached"] is True, "pooled sweet spot reached the 0.95 bar")
    check(sp.get("config") == exp["planted_config"], "pooled sweet spot is the planted configuration %s (got %s)" % (exp["planted_config"], sp.get("config")))
    check(sp.get("n_pos") == exp["n_pooled_pos"], "pooled read positives %d == planted %d" % (sp.get("n_pos", -1), exp["n_pooled_pos"]))
    check(abs(sp.get("sens", 0) - exp["sens"]) < 1e-9, "planted sensitivity %.4f reproduced (%.4f)" % (exp["sens"], sp.get("sens", 0)))
    check(abs(sp.get("spec", 0) - exp["spec"]) < 1e-9, "planted specificity %.4f reproduced (%.4f)" % (exp["spec"], sp.get("spec", 0)))
    check((sp.get("tp"), sp.get("fp"), sp.get("tn")) == (exp["tp"], exp["fp"], exp["tn"]), "planted TP/FP/TN %s reproduced (%s)" % (
        (exp["tp"], exp["fp"], exp["tn"]), (sp.get("tp"), sp.get("fp"), sp.get("tn"))))
    check(sum(v == "fail" for v in exp["windows"].values()) >= 1, "at least one window was planted outside its bounds, so the fail branch is exercised")
    t13 = S["sweet_spot"]["T13"]
    check(t13["reached"] is False, "T13 (caught 60 %% by rule 3 alone): the report says plainly no configuration reaches 0.95 (n=%d)" % t13["n_pos"])
    check("NO configuration" in t13["statement"], "T13 statement carries the plain 'NO configuration' wording")
    wins = {w["window"]: w["status"] for w in S["prevalence_windows"]}
    check(wins == exp["windows"], "prevalence windows %s == planted %s" % (wins, exp["windows"]))
    check(set(S["rules_available"]) == {"R1_count", "R1_anchor", "R2", "R3_S1", "R3_S3", "R4"}, "all six rules available in run 1 (%s)" % S["rules_available"])
    check(S["n_configurations"] == 31 + 32 * len(S["s3_grid"]), "sweep size = 31 + 32 x %d grid cuts (%d)" % (len(S["s3_grid"]), S["n_configurations"]))
    auc = {(a["quantity"], a["target"]): a["auc"] for a in S["roc_auc"]}
    check(auc.get(("count_ordinal", "L6"), 0) > 0.9, "ROC: count ordinal separates read L6 (AUC %.3f)" % auc.get(("count_ordinal", "L6"), 0))
    check(auc.get(("s3_ratio", "stump_rib"), 0) > 0.9, "ROC: S3 ratio separates read stump ribs (AUC %.3f)" % auc.get(("s3_ratio", "stump_rib"), 0))
    check(auc.get(("rule2_absz_max", "four_lumbar_or_fused_L5"), 0) > 0.6, "ROC: rule-2 |z| lifts on fused L5 (AUC %.3f)" % auc.get(("rule2_absz_max", "four_lumbar_or_fused_L5"), 0))
    check(0.4 < auc.get(("rule2_absz_max", "L6"), 0) < 0.65, "ROC: rule-2 |z| is chance on L6 (AUC %.3f)" % auc.get(("rule2_absz_max", "L6"), 0))
    # contribution: only-caught-by counts
    cdf = pd.read_csv(tmp / "run1" / "tables" / "contribution.csv")
    pooled = cdf[cdf.target == "pooled"].set_index("rule")
    check(pooled.loc["R3_S1", "read_positives_only_this_rule"] > 0, "contribution: rule 3 S1 catches positives no other rule catches (%d)" % pooled.loc["R3_S1", "read_positives_only_this_rule"])
    check(pooled.loc["R1_count", "read_sens_without"] < pooled.loc["R1_count", "read_sens_with"], "contribution: removing rule 1 count lowers pooled sensitivity")
    # every CSV row carries the header fields
    for f in sorted((tmp / "run1" / "tables").glob("*.csv")):
        d = pd.read_csv(f, dtype=str, keep_default_na=False)
        miss = [c for c in ("prereg_sha256", "prereg_status", "git_sha", "tool", "tool_version", "utc_time", "inputs_sha256") if c not in d.columns]
        if len(d):
            check(not miss and (d["prereg_status"] == "draft").all() and d["inputs_sha256"].str.contains("census=").all(), "header fields on every row of %s" % f.name)
    # html has every table
    h = (tmp / "run1" / "report.html").read_text(encoding="utf-8")
    for tid in ("header", "truth_summary", "rule_states", "contribution", "sweet_spot", "sweep", "roc_auc", "prevalence_windows"):
        check('id="%s"' % tid in h, "report.html holds table %s" % tid)
    check("<svg" in h and "cdn" not in h.lower() and "<script" not in h, "report.html is self-contained: inline SVG, no CDN, no script")
    check('name="viewport"' in h, "report.html declares a phone viewport")
    bad = "prov" + "enance"
    check(bad not in h.lower() and bad not in Path(__file__).read_text(encoding="utf-8").lower(), "the forbidden word appears nowhere (report or source)")
    # run 2: no S3 cut and no thoracic count column -> S3 excluded, windows not_computable
    c2 = pd.read_csv(syn / "census.tsv", sep="\t", dtype=str, keep_default_na=False).drop(columns=["n_thoracic_rib_bearing", "rule4_decision"])
    c2.to_csv(syn / "census_nocage.tsv", sep="\t", index=False)
    ns2 = argparse.Namespace(**{**vars(ns), "census": str(syn / "census_nocage.tsv"), "out": str(tmp / "run2"), "s3_cut": None})
    S2 = run(ns2)
    check("R3_S3" not in S2["rules_available"] and "no calibrated cut" in S2["rule_availability"]["R3_S3"], "run 2: S3 excluded without a calibrated cut, and the report says so")
    check("R4" not in S2["rules_available"], "run 2: rule 4 unavailable when its column is absent")
    w2 = {w["window"]: w["status"] for w in S2["prevalence_windows"]}
    check(w2["thirteen_rib_bearing"] == "not_computable" and w2["eleven_rib_bearing"] == "not_computable", "run 2: cage windows are not_computable (never a pass) without a cage count")
    check(S2["sweet_spot"]["pooled"].get("config") == exp["planted_config"], "run 2: the planted configuration is still the sweet spot (%s)" % S2["sweet_spot"]["pooled"].get("config"))
    check(any(("s3_ratio" == a["quantity"]) for a in S2["roc_auc"]), "run 2: the S3 ratio ROC is still produced")
    print("SELFTEST %s (%d checks failed) -- outputs under %s" % ("PASSED" if not fails else "FAILED", len(fails), tmp))
    return 1 if fails else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--census", help="rules census TSV (one row per CT)")
    ap.add_argument("--out", help="output directory")
    ap.add_argument("--castellvi", help="castellvi_consensus.csv")
    ap.add_argument("--lumbosac", help="Lumbosac.csv (needs --castellvi for the token join)")
    ap.add_argument("--verse-suppl", dest="verse_suppl", help="verse_suppl_table1.csv")
    ap.add_argument("--lstv-flags", dest="lstv_flags", help="lstv_flag_labels_v2.csv")
    ap.add_argument("--registry", help="registry.csv (truth_tier == read rows are used)")
    ap.add_argument("--prereg", default=str(PREREG_DEFAULT), help="PREREG_rules.md")
    ap.add_argument("--s3-cut", dest="s3_cut", type=float, default=None, help="calibrated S3 ratio cut (STUMP_RULE.md C6)")
    ap.add_argument("--s3-calib", dest="s3_calib", default=None, help="JSON with key s3_cut, instead of --s3-cut")
    ap.add_argument("--s3-grid", dest="s3_grid", default=None, help="lo:hi:step grid of S3 cuts (default cut +/- 0.10 by 0.02)")
    ap.add_argument("--unit", choices=["person", "ct"], default="person")
    ap.add_argument("--min-sens", dest="min_sens", type=float, default=MIN_SENS_DEFAULT, help="pre-stated sensitivity bar (PREREG: 0.95)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--keep", default=None, help="selftest: keep outputs under this directory")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.keep)
    if not a.census or not a.out:
        ap.error("--census and --out are required (or --selftest)")
    run(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
