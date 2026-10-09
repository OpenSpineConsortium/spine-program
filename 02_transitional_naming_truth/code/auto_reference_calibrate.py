#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/auto_reference_calibrate.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Calibrate and FREEZE the automated reference standard (SchwingNet/LEVELCHECK_MODEL.md section 14, R2-R3).

Reads the four readers' per-person calls (A: SPINEPS ctd names behind tools/spineps_ids.py; B: TotalSegmentator
geometry; C: the direct CT rib count; D: A/B/C on the COBRA CBCT), joins every person to the FROZEN G3 split
(results/fig6/frozen/v1/split_final.json, the same bytes as ~/split_final.json on the grid, sha256 asserted), builds
the human-read truth of CTSpinoPelvic1K and VerSe, and calibrates the three pre-specified consensus rules on the
NON-TEST persons of those two corpora only (zero test persons: asserted, and the test truth is never read here).
The chosen rule is then applied to every person of every corpus, and the assignment table is frozen with its SHA-256
BEFORE any SchwingNet model runs on a G3 test person.

Truth classes (the rule's vocabulary, R2): ordinary, L6, T13, four_lumbar (sacralised / four-lumbar: a fused body
that carries NO separate lumbar id, so a reader sees four rib-free bodies above the sacrum), both (T13 + L6). A
sacralised L5 that keeps its own id has the ordinary alphabet (L1..L5; section 3 lists it as "variant, naming
unaffected"), and is scored as `ordinary` for naming; a second row of the calibration table scores it as
four_lumbar instead so that convention is visible. Castellvi I/II and a lumbar rib keep the ordinary alphabet.
Persons whose truth is `unassigned` (four lumbar ids and no read) or who have no read at all are outside the
calibration set.

Rules (R2): unanimity (A, B and C all count and agree); 2-of-3 (at least two of A, B, C make the same call; the third
may abstain or disagree); Dawid-Skene (latent-class EM fitted on the calibration persons' calls only, abstentions as
missing; a person is assigned when the posterior of one class is at least DS_POSTERIOR). Selection (R2): the rule
with the highest calibration coverage whose PPV has a Wilson lower bound of at least 0.90 for every subtype it
assigns. If no rule qualifies for every subtype, the pre-specified fallback is per subtype: for each subtype the
qualifying rule (lower bound >= 0.90 for that subtype) with the highest coverage of that subtype; a subtype no rule
qualifies for is NOT assignable, and a person whose call is such a subtype is excluded with that reason. Reader D
(COBRA CBCT) never adds a vote: a CBCT call that disagrees with the planning-CT assignment excludes the person.

    python tools/auto_reference_calibrate.py            (writes results/auto_reference/{CALIBRATION.md,calibration.json})
    python tools/auto_reference_calibrate.py --freeze   (also writes results/fig6/frozen/{auto_reference.json,
                                                         auto_truth.csv,auto_reference.sha256}; refuses to overwrite)
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RES = REPO / "SchwingNet" / "results"
AR = RES / "auto_reference"
FROZEN_V1 = RES / "fig6" / "frozen" / "v1"
SPLIT_SHA = "65a57eb0c7a6e202207a9eb63307da37c6bac88f3e7f956e14543413af2bca71"   # RUN_v2.json; ~/split_final.json on the grid
CLASSES = ["ordinary", "L6", "T13", "four_lumbar", "both"]
READERS = ["A", "B", "C"]
CORPORA = ["ctsp", "verse", "cobra_ct", "carmlspine"]
CALIB_CORPORA = ["ctsp", "verse"]
DS_POSTERIOR = 0.95
PPV_LB_MIN = 0.90
Z = 1.959964
LUMBAR_NAMES = {"ordinary": "L1 L2 L3 L4 L5", "L6": "L1 L2 L3 L4 L5 L6", "T13": "L1 L2 L3 L4 L5",
                "four_lumbar": "L1 L2 L3 L4", "both": "L1 L2 L3 L4 L5 L6"}
ALPHABET = {"ordinary": (False, False, False), "L6": (True, False, False), "T13": (False, True, False),
            "four_lumbar": (False, False, True), "both": (True, True, False)}
N_MIN = {"at_risk (H1, H3-H5; p0 0.822)": 19, "ordinary (H6; p0 0.926)": 48, "at_risk vs published (H2; p0 0.976)": 152}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rd(p: Path):
    return list(csv.DictReader(open(p, newline="", encoding="utf-8")))


def wilson(k: int, n: int):
    if n == 0:
        return None, None, None
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def norm_call(s: str) -> str:
    """Reader vocabulary -> rule vocabulary. Reader C's sacralised_fused (a TS lumbar body joined to the sacrum) and
    every reader's four_lumbar are one class, as R2 says."""
    return {"sacralised_fused": "four_lumbar"}.get(s, s)


# ------------------------------------------------------------------------------------------------ readers
def _rank_str(r: dict):
    """tools/auto_reference_readers_ab.py::_rank on csv strings: which series speaks for a person with several."""
    return (r["subtype_call"] == "no_count",
            not (r["junction_tl_in_fov"] == "True" and r["junction_ls_in_fov"] == "True"),
            r["n_rib_bearing"] == "", r["case"])


def collapse_c(rows: list) -> dict:
    by = defaultdict(list)
    for r in rows:
        by[r["person_key"]].append(r)
    out = {}
    for pk, rs in by.items():
        rs = sorted(rs, key=_rank_str)
        best = dict(rs[0])
        if len(rs) > 1:
            counted = {norm_call(x["subtype_call"]) for x in rs if x["subtype_call"] != "no_count"}
            best["series_note"] = (("SERIES DISAGREE: " if len(counted) > 1 else "") +
                                   f"{len(rs)} series; chosen {best['case']}; others " +
                                   ", ".join(f"{x['case']}={x['subtype_call']}" for x in rs[1:]))
        out[pk] = best
    return out


def load_readers(corpus: str):
    """{person_key: {"A": call, "B": call, "C": call, "case":..., "g3_side_table":..., "notes": {...}}}"""
    ab = rd(AR / "readersAB" / "tables" / f"{corpus}.csv")
    c = collapse_c(rd(AR / "readerC" / f"{corpus}.csv"))
    per = {}
    for r in ab:
        p = per.setdefault(r["person_key"], {"case": r["case"], "corpus": corpus, "g3_side_table": r.get("g3_side", ""),
                                             "calls": {}, "refusal": {}, "notes": {}})
        p["calls"][r["reader"]] = norm_call(r["subtype_call"])
        p["refusal"][r["reader"]] = r["refusal_reason"]
        p["notes"][r["reader"]] = r.get("notes", "")
        p.setdefault("nT", {})[r["reader"]] = r["n_rib_bearing"]
    for pk, r in c.items():
        p = per.setdefault(pk, {"case": r["case"], "corpus": corpus, "g3_side_table": "", "calls": {}, "refusal": {}, "notes": {}})
        p["calls"]["C"] = norm_call(r["subtype_call"])
        p["refusal"]["C"] = r["refusal_reason"]
        p["notes"]["C"] = r.get("series_note", "")
        p.setdefault("nT", {})["C"] = r["n_rib_bearing"]
    for pk, p in per.items():
        for rdr in READERS:
            p["calls"].setdefault(rdr, "not_run")
            p.setdefault("nT", {}).setdefault(rdr, "")
    return per


def load_reader_d():
    """COBRA CBCT: A and B from the readersAB table, C from readerC (reader 'D' there). {person: {reader: call}}"""
    out = defaultdict(dict)
    for r in rd(AR / "readersAB" / "tables" / "cobra_cbct.csv"):
        out[r["person_key"]][r["reader"]] = norm_call(r["subtype_call"])
    for r in rd(AR / "readerC" / "cobra_cbct.csv"):
        out[r["person_key"]]["C"] = norm_call(r["subtype_call"])
    return out


# ------------------------------------------------------------------------------------------------ truth
def truth_ctsp(all_persons):
    """CTSpinoPelvic1K: transitional_subtypes.csv (two-reader Castellvi consensus + release ids) for the transitional
    persons; every other release person is ordinary by its release labels (five lumbar ids, no LSTV flag)."""
    t = {}
    for r in rd(FROZEN_V1 / "transitional_subtypes.csv"):
        if r["source"] != "ctsp":
            continue
        t[r["patient_key"]] = {"subtype": r["subtype"], "four_lumbar_mask": r["four_lumbar_mask"] == "True",
                               "n_lumbar": r["n_lumbar_labelled"], "confidence": r["confidence"],
                               "source": "transitional_subtypes.csv (" + r["truth_source"] + ")"}
    for pk in all_persons:
        t.setdefault(pk, {"subtype": "ordinary", "four_lumbar_mask": False, "n_lumbar": "5",
                          "confidence": "release labels", "source": "release labels: not in transitional_subtypes.csv"})
    return t


def truth_verse():
    """VerSe: the Loffler 2021 two-neuroradiologist read as parsed into transitional_registry/verse/screened.csv
    (final_subtype per series; series of one person agree). 'none' with a read count is ordinary; an empty read or
    'unassigned' is no truth."""
    t = {}
    for r in rd(FROZEN_V1 / "transitional_registry" / "verse" / "screened.csv"):
        pk = r["patient_key"]
        sub = r["final_subtype"]
        if sub == "none":
            if r["read"] == "":
                rec = {"subtype": "no_read", "source": "screened.csv: no read"}
            else:
                rec = {"subtype": "ordinary", "source": "screened.csv: read " + r["read"]}
        else:
            rec = {"subtype": sub, "source": "screened.csv: read " + r["read"] + " final_subtype " + sub}
        rec["four_lumbar_mask"] = sub == "sacralised_L5_fused" and r["read"].split("/")[2:3] == ["4"]
        rec["n_lumbar"] = r["read"].split("/")[2] if r["read"].count("/") >= 2 else ""
        rec["confidence"] = "Loffler 2021 consensus read" if r["read"] else ""
        prev = t.get(pk)
        if prev and prev["subtype"] != rec["subtype"] and rec["subtype"] != "no_read":
            if prev["subtype"] == "no_read":
                t[pk] = rec
            else:
                raise SystemExit(f"VerSe series of {pk} disagree on truth: {prev['subtype']} vs {rec['subtype']}")
        elif not prev:
            t[pk] = rec
    return t


def truth_class(rec: dict, own_id_sacralised_as: str = "ordinary"):
    """Truth record -> rule class, or None when there is no usable truth."""
    s = rec["subtype"]
    if s in ("unassigned", "no_read"):
        return None
    if s in ("ordinary", "castellvi_I_II", "lumbar_rib"):
        return "ordinary"
    if s == "L6":
        return "L6"
    if s == "T13":
        return "T13"
    if s == "sacralised_L5_fused":
        return "four_lumbar" if rec["four_lumbar_mask"] else own_id_sacralised_as
    raise SystemExit(f"unknown truth subtype {s}")


# ------------------------------------------------------------------------------------------------ rules
def rule_unanimity(calls: dict):
    v = [calls[r] for r in READERS]
    if any(x in ("no_count", "not_run") for x in v):
        return None
    return v[0] if len(set(v)) == 1 else None


def rule_two_of_three(calls: dict):
    v = [calls[r] for r in READERS if calls[r] not in ("no_count", "not_run")]
    if len(v) < 2:
        return None
    c, n = Counter(v).most_common(1)[0]
    return c if n >= 2 else None


class DawidSkene:
    def __init__(self, classes, readers, iters=200, smooth=0.01):
        self.K, self.J, self.iters, self.smooth = classes, readers, iters, smooth
        self.prior = None
        self.conf = None

    def fit(self, calls_list):
        K, J = self.K, self.J
        n = len(calls_list)
        # initialise from the majority vote (soft over ties)
        post = []
        for calls in calls_list:
            v = [calls[r] for r in J if calls[r] in K]
            w = {k: 0.0 for k in K}
            if v:
                c = Counter(v)
                top = max(c.values())
                tied = [k for k in K if c.get(k, 0) == top]
                for k in tied:
                    w[k] = 1.0 / len(tied)
            else:
                for k in K:
                    w[k] = 1.0 / len(K)
            post.append(w)
        for _ in range(self.iters):
            # M step
            prior = {k: (sum(p[k] for p in post) + self.smooth) for k in K}
            tot = sum(prior.values())
            prior = {k: v / tot for k, v in prior.items()}
            conf = {j: {k: {l: self.smooth for l in K} for k in K} for j in J}
            for calls, p in zip(calls_list, post):
                for j in J:
                    if calls[j] in K:
                        for k in K:
                            conf[j][k][calls[j]] += p[k]
            for j in J:
                for k in K:
                    s = sum(conf[j][k].values())
                    for l in K:
                        conf[j][k][l] /= s
            # E step
            new = []
            for calls in calls_list:
                w = {}
                for k in K:
                    x = math.log(prior[k])
                    for j in J:
                        if calls[j] in K:
                            x += math.log(conf[j][k][calls[j]])
                    w[k] = x
                m = max(w.values())
                e = {k: math.exp(v - m) for k, v in w.items()}
                s = sum(e.values())
                new.append({k: v / s for k, v in e.items()})
            delta = max(abs(a[k] - b[k]) for a, b in zip(post, new) for k in K)
            post = new
            if delta < 1e-8:
                break
        self.prior, self.conf = prior, conf
        return self

    def posterior(self, calls: dict):
        if not any(calls[j] in self.K for j in self.J):
            return None
        w = {}
        for k in self.K:
            x = math.log(self.prior[k])
            for j in self.J:
                if calls[j] in self.K:
                    x += math.log(self.conf[j][k][calls[j]])
            w[k] = x
        m = max(w.values())
        e = {k: math.exp(v - m) for k, v in w.items()}
        s = sum(e.values())
        return {k: v / s for k, v in e.items()}

    def call(self, calls: dict):
        p = self.posterior(calls)
        if p is None:
            return None
        k, v = max(p.items(), key=lambda kv: kv[1])
        return k if v >= DS_POSTERIOR else None


# ------------------------------------------------------------------------------------------------ metrics
def metrics(rule_calls: dict, truth: dict):
    """rule_calls {pk: class|None}; truth {pk: class}. Per class PPV, sensitivity, coverage with Wilson intervals."""
    n = len(truth)
    assigned = {pk: c for pk, c in rule_calls.items() if c is not None}
    out = {"n_calibration": n, "n_assigned": len(assigned), "coverage": wilson(len(assigned), n), "per_class": {}}
    for c in CLASSES:
        as_c = [pk for pk, v in assigned.items() if v == c]
        truth_c = [pk for pk, v in truth.items() if v == c]
        tp = sum(1 for pk in as_c if truth[pk] == c)
        wrong = Counter(truth[pk] for pk in as_c if truth[pk] != c)
        covered_c = sum(1 for pk in truth_c if pk in assigned)          # truth-c persons the rule assigns (any class)
        out["per_class"][c] = {"n_truth": len(truth_c), "n_assigned": len(as_c), "n_correct": tp,
                               "ppv": wilson(tp, len(as_c)), "sensitivity": wilson(tp, len(truth_c)),
                               "class_coverage": wilson(covered_c, len(truth_c)) if truth_c else (None, None, None),
                               "wrong_truths": dict(wrong)}
    return out


def qualifies(m: dict, c: str):
    pc = m["per_class"][c]
    return pc["n_assigned"] > 0 and pc["ppv"][1] is not None and pc["ppv"][1] >= PPV_LB_MIN


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--out", default=str(AR))
    a = ap.parse_args()
    outd = Path(a.out)
    outd.mkdir(parents=True, exist_ok=True)
    frozen_dir = RES / "fig6" / "frozen"
    frozen_files = [frozen_dir / "auto_reference.json", frozen_dir / "auto_truth.csv", frozen_dir / "auto_reference.sha256"]
    if a.freeze and any(p.exists() for p in frozen_files):
        raise SystemExit("REFUSED: frozen files exist; the freeze happens once (" + ", ".join(str(p) for p in frozen_files) + ")")
    unbl = RES / "fig6" / "unblinding"
    if unbl.exists() and any(unbl.iterdir()):
        raise SystemExit(f"REFUSED: {unbl} is not empty: unblinding has happened; the reference cannot be frozen after it")

    inputs = {}
    split_p = FROZEN_V1 / "split_final.json"
    s = sha(split_p)
    assert s == SPLIT_SHA, f"split_final.json sha256 {s} != frozen {SPLIT_SHA}"
    inputs["split_final.json"] = {"path": str(split_p.relative_to(REPO)), "sha256": s,
                                  "note": "identical bytes to ~/split_final.json on the grid (sha256sum checked 2026-09-24)"}
    side_of = json.load(open(split_p))["side_of_person"]
    for name in ["transitional_subtypes.csv", "transitional_registry/verse/screened.csv"]:
        inputs[name] = {"path": str((FROZEN_V1 / name).relative_to(REPO)), "sha256": sha(FROZEN_V1 / name)}
    for corpus in CORPORA + ["cobra_cbct"]:
        for src in ["readersAB/tables", "readerC"]:
            p = AR / src / f"{corpus}.csv"
            inputs[f"{src}/{corpus}.csv"] = {"path": str(p.relative_to(REPO)), "sha256": sha(p)}
    inputs["readersAB/code/MD5"] = {"path": str((AR / "readersAB" / "MD5").relative_to(REPO)),
                                    "content": (AR / "readersAB" / "MD5").read_text().strip().splitlines()}

    readers = {c: load_readers(c) for c in CORPORA}
    reader_d = load_reader_d()
    for c in CORPORA:
        for pk, p in readers[c].items():
            side = side_of.get(pk)
            if side is None:
                raise SystemExit(f"{pk} is not in split_final.json")
            if p["g3_side_table"] and p["g3_side_table"] != side:
                raise SystemExit(f"{pk}: reader table side {p['g3_side_table']} != split_final {side}")
            p["side"] = side

    # ---- truth and the calibration set: CTSP + VerSe, NON-test only
    truth_rec = {}
    truth_rec.update(truth_ctsp(list(readers["ctsp"].keys())))
    truth_rec.update(truth_verse())
    calib = {}          # pk -> truth class (own-id sacralised L5 = ordinary)
    calib_alt = {}      # pk -> truth class (own-id sacralised L5 = four_lumbar)
    excluded_from_calib = Counter()
    for c in CALIB_CORPORA:
        for pk, p in readers[c].items():
            if p["side"] == "test":
                excluded_from_calib[f"{c}: G3 test person (truth never read here)"] += 1
                continue
            rec = truth_rec.get(pk)
            if rec is None:
                excluded_from_calib[f"{c}: no truth record"] += 1
                continue
            tc = truth_class(rec)
            if tc is None:
                excluded_from_calib[f"{c}: truth {rec['subtype']}"] += 1
                continue
            calib[pk] = tc
            calib_alt[pk] = truth_class(rec, own_id_sacralised_as="four_lumbar")
    assert not any(readers[c][pk]["side"] == "test" for c in CALIB_CORPORA for pk in calib if pk in readers[c]), "test person in calibration"
    n_test_in_calib = sum(1 for pk in calib if side_of[pk] == "test")
    assert n_test_in_calib == 0
    calib_calls = {pk: readers["ctsp" if pk.startswith("ctsp:") else "verse"][pk]["calls"] for pk in calib}

    # ---- the three rules
    ds = DawidSkene(CLASSES, READERS).fit([calib_calls[pk] for pk in sorted(calib)])
    rules = {"unanimity": rule_unanimity, "two_of_three": rule_two_of_three, "dawid_skene": ds.call}
    rule_calls = {name: {pk: fn(calib_calls[pk]) for pk in calib} for name, fn in rules.items()}
    table = {name: metrics(rc, calib) for name, rc in rule_calls.items()}
    table_alt = {name: metrics(rc, calib_alt) for name, rc in rule_calls.items()}
    per_corpus = {name: {c: metrics({pk: v for pk, v in rc.items() if pk.startswith(c + ":")},
                                    {pk: v for pk, v in calib.items() if pk.startswith(c + ":")})
                         for c in CALIB_CORPORA} for name, rc in rule_calls.items()}
    reader_solo = {}
    for rdr in READERS:
        rc = {pk: (calib_calls[pk][rdr] if calib_calls[pk][rdr] in CLASSES else None) for pk in calib}
        reader_solo[rdr] = metrics(rc, calib)

    # ---- selection (R2)
    global_ok = {name: all(qualifies(m, c) for c in CLASSES if m["per_class"][c]["n_assigned"] > 0) for name, m in table.items()}
    chosen = {"mode": None, "rule": None, "per_class": {}}
    cands = [n for n, ok in global_ok.items() if ok]
    if cands:
        best = max(cands, key=lambda n: table[n]["coverage"][0])
        chosen = {"mode": "global", "rule": best,
                  "per_class": {c: best for c in CLASSES if table[best]["per_class"][c]["n_assigned"] > 0}}
    else:
        chosen["mode"] = "per_subtype (no rule reached a PPV lower bound of 0.90 for every subtype it assigns)"
        for c in CLASSES:
            q = [n for n in rules if qualifies(table[n], c)]
            if q:
                chosen["per_class"][c] = max(q, key=lambda n: table[n]["per_class"][c]["class_coverage"][0])
    assignable = sorted(chosen["per_class"].keys())

    # ---- apply to every person of every corpus
    sets = {}
    for t in ["T2", "T3"]:
        for pk, v in json.load(open(RES / "fig6" / "sets_v2" / f"{t}_persons.json")).items():
            sets[pk] = {"set": t, "stratum": v["stratum"], "gate": v["gate"],
                        "has_frames": bool(v["frames"]["open"] or v["frames"]["blinded"]),
                        "withheld": ";".join(f"{k}={v2}" for k, v2 in (v.get("withheld") or {}).items())}
    rows = []
    for c in CORPORA:
        for pk in sorted(readers[c]):
            p = readers[c][pk]
            calls = p["calls"]
            calls_by_rule = {name: fn(calls) for name, fn in rules.items()}
            unanimous = calls_by_rule["unanimity"] is not None
            votes = {}
            for cls, rname in chosen["per_class"].items():
                if calls_by_rule[rname] == cls:
                    votes[cls] = rname
            status, reason, assigned, rule_used = "excluded", "", "", ""
            if len(votes) == 1:
                assigned, rule_used = next(iter(votes.items()))
                status = "assigned_unanimous" if unanimous else "assigned_rule"
            elif len(votes) > 1:
                reason = "conflict between the rules chosen per subtype: " + ", ".join(f"{k} by {v}" for k, v in votes.items())
            else:
                counted = {r: calls[r] for r in READERS if calls[r] in CLASSES}
                if not counted:
                    reason = "no reader could count (" + "; ".join(f"{r}: {p['refusal'][r][:60]}" for r in READERS if p["refusal"].get(r)) + ")"
                else:
                    any_call = {n: v for n, v in calls_by_rule.items() if v is not None}
                    if any_call and all(v not in assignable for v in any_call.values()):
                        reason = "subtype not calibrated to PPV lower bound >= 0.90: " + ", ".join(f"{n}={v}" for n, v in any_call.items())
                    elif any_call:
                        reason = "the rule chosen for this subtype does not assign it: " + ", ".join(f"{n}={v}" for n, v in any_call.items())
                    else:
                        reason = "readers disagree or too few counted: " + ", ".join(f"{r}={v}" for r, v in counted.items())
            d_note = ""
            if c == "cobra_ct":
                d = reader_d.get(pk, {})
                dc = {r: v for r, v in d.items() if v in CLASSES}
                if dc and assigned:
                    if all(v == assigned for v in dc.values()):
                        d_note = "CBCT agrees: " + ", ".join(f"{r}={v}" for r, v in dc.items())
                    else:
                        d_note = "CBCT DISAGREES: " + ", ".join(f"{r}={v}" for r, v in dc.items())
                        status, reason, assigned, rule_used = "excluded", "reader D (CBCT) disagrees with the planning-CT assignment: " + d_note, "", ""
                elif dc:
                    d_note = "CBCT counted: " + ", ".join(f"{r}={v}" for r, v in dc.items())
                else:
                    d_note = "CBCT: no count (A/B/C on the CBCT all abstained)"
            rec = truth_rec.get(pk) if c in CALIB_CORPORA else None
            st = sets.get(pk, {})
            al = ALPHABET.get(assigned, ("", "", ""))
            rows.append({"person_key": pk, "corpus": c, "case": p["case"], "g3_side": p["side"],
                         "real_frame_test_set": st.get("set", ""), "frozen_stratum": st.get("stratum", ""),
                         "has_real_frames": st.get("has_frames", ""), "withheld": st.get("withheld", ""),
                         "call_A": calls["A"], "call_B": calls["B"], "call_C": calls["C"],
                         "n_rib_bearing_A": p["nT"]["A"], "n_rib_bearing_B": p["nT"]["B"], "n_rib_bearing_C": p["nT"]["C"],
                         "t13_excluded_by_anchored_count": any(p["nT"][r] == "12" for r in READERS),
                         "unanimous": unanimous, "unanimity": calls_by_rule["unanimity"] or "",
                         "two_of_three": calls_by_rule["two_of_three"] or "", "dawid_skene": calls_by_rule["dawid_skene"] or "",
                         "status": status, "assigned_subtype": assigned, "rule_used": rule_used,
                         "lumbar_names": LUMBAR_NAMES.get(assigned, ""),
                         "alphabet_l6": al[0], "alphabet_t13": al[1], "alphabet_l4": al[2],
                         "exclusion_reason": reason, "reader_D": d_note,
                         "human_truth_subtype": (rec["subtype"] if rec else ""),
                         "human_truth_class": (truth_class(rec) or "") if rec else "",
                         "human_truth_source": (rec["source"] if rec else ""),
                         "in_calibration": pk in calib,
                         "primary_reference": ("human read (section 4)" if rec and truth_class(rec) else
                                               ("automated reference" if assigned else "none"))})

    # ---- report: real-frame test persons usable per subtype
    usable = {}
    for t in ["T2", "T3"]:
        tr = [r for r in rows if r["real_frame_test_set"] == t]
        rep = {"persons": len(tr), "persons_with_frames": sum(1 for r in tr if r["has_real_frames"]),
               "by_assigned_subtype": {}, "excluded_reasons": Counter(), "frozen_stratum_vs_assigned": Counter()}
        for r in tr:
            key = r["assigned_subtype"] or "excluded"
            d = rep["by_assigned_subtype"].setdefault(key, Counter())
            d["all"] += 1
            d["with_frames"] += int(bool(r["has_real_frames"]))
            d["unanimous"] += int(r["status"] == "assigned_unanimous")
            d["unanimous_with_frames"] += int(r["status"] == "assigned_unanimous" and bool(r["has_real_frames"]))
            d["t13_excluded_by_anchored_count"] += int(r["t13_excluded_by_anchored_count"])
            d["withheld_varian_not_exported"] += int("varian_not_exported" in r["withheld"])
            d["withheld_no_exported_frame"] += int("no_exported_frame" in r["withheld"])
            if r["status"] == "excluded":
                rep["excluded_reasons"][r["exclusion_reason"].split(":")[0]] += 1
            rep["frozen_stratum_vs_assigned"][f"{r['frozen_stratum']} -> {key}"] += 1
        rep["by_assigned_subtype"] = {k: dict(v) for k, v in rep["by_assigned_subtype"].items()}
        rep["excluded_reasons"] = dict(rep["excluded_reasons"])
        rep["frozen_stratum_vs_assigned"] = dict(sorted(rep["frozen_stratum_vs_assigned"].items()))
        usable[t] = rep

    # ---- transportability of the ordinary PPV: was the thoracic count anchored (T13 excluded) where 'ordinary' was assigned?
    transport = {}
    for name, rc in rule_calls.items():
        anch = {pk: any(readers["ctsp" if pk.startswith("ctsp:") else "verse"][pk]["nT"][r] == "12" for r in READERS) for pk in calib}
        as_o = [pk for pk, v in rc.items() if v == "ordinary"]
        sub = {}
        for lab, keep in (("anchored", True), ("unanchored", False)):
            g = [pk for pk in as_o if anch[pk] == keep]
            tp = sum(1 for pk in g if calib[pk] == "ordinary")
            sub[lab] = {"n_assigned_ordinary": len(g), "n_correct": tp, "ppv": wilson(tp, len(g)),
                        "wrong_truths": dict(Counter(calib[pk] for pk in g if calib[pk] != "ordinary"))}
        transport[name] = sub
    t2_rows = [r for r in rows if r["real_frame_test_set"] == "T2" and r["assigned_subtype"] == "ordinary"]
    transport["T2_assigned_ordinary"] = {
        "n": len(t2_rows), "anchored": sum(1 for r in t2_rows if r["t13_excluded_by_anchored_count"]),
        "by_frozen_stratum": dict(Counter(r["frozen_stratum"] for r in t2_rows)),
        "by_frozen_stratum_with_frames": dict(Counter(r["frozen_stratum"] for r in t2_rows if r["has_real_frames"])),
        "note": "T13 prevalence in the calibration set is 4/945; an unanchored 'ordinary' call does not exclude T13, so the "
                "ordinary PPV measured here bounds the T13 error only at that prevalence. No reader anchored a thoracic "
                "count on any COBRA planning CT, so the T2 ordinary assignments rest on the lumbar count alone."}

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout.strip() != ""
    utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    calibration = {
        "_about": "Calibration of the automated reference (LEVELCHECK_MODEL.md section 14, R2) on the NON-test persons of "
                  "CTSpinoPelvic1K and VerSe. Every number is computed by tools/auto_reference_calibrate.py from the "
                  "inputs listed. No G3 test person's truth was read.",
        "git_head": head, "git_dirty": dirty, "utc": utc, "tool": "tools/auto_reference_calibrate.py",
        "parameters": {"classes": CLASSES, "readers": READERS, "ds_posterior_threshold": DS_POSTERIOR,
                       "ppv_wilson_lower_bound_min": PPV_LB_MIN, "z": Z, "lumbar_names": LUMBAR_NAMES,
                       "truth_class_map": {"ordinary|castellvi_I_II|lumbar_rib": "ordinary", "L6": "L6", "T13": "T13",
                                           "sacralised_L5_fused with four lumbar ids": "four_lumbar",
                                           "sacralised_L5_fused with its own L5 id": "ordinary (alt table: four_lumbar)",
                                           "unassigned | no read": "not in the calibration set"},
                       "reader_call_map": {"sacralised_fused": "four_lumbar"},
                       "series_rule": "one series per VerSe person: tools/auto_reference_readers_ab.py::_rank"},
        "inputs": inputs,
        "calibration_set": {"n": len(calib), "by_corpus": dict(Counter(pk.split(":")[0] for pk in calib)),
                            "by_side": dict(Counter(side_of[pk] for pk in calib)),
                            "by_truth_class": dict(Counter(calib.values())),
                            "by_truth_class_alt": dict(Counter(calib_alt.values())),
                            "test_persons_in_calibration": n_test_in_calib,
                            "excluded_from_calibration": dict(excluded_from_calib)},
        "reader_calls_in_calibration": {r: dict(Counter(calib_calls[pk][r] for pk in calib)) for r in READERS},
        "readers_alone": reader_solo,
        "rules": table, "rules_alt_truth_convention": table_alt, "rules_per_corpus": per_corpus,
        "dawid_skene": {"prior": ds.prior, "confusion": ds.conf},
        "global_qualifies": global_ok, "chosen": chosen, "assignable_subtypes": assignable,
        "real_frame_test_persons": usable, "n_min": N_MIN, "transportability": transport,
        "assignment_counts": {c: dict(Counter(f"{r['g3_side']} | {r['status']} | {r['assigned_subtype'] or r['exclusion_reason'].split(':')[0]}"
                                              for r in rows if r["corpus"] == c)) for c in CORPORA},
    }
    json.dump(calibration, open(outd / "calibration.json", "w"), indent=1, default=str)
    (outd / "CALIBRATION.md").write_text(render_md(calibration), encoding="utf-8")
    print(f"wrote {outd / 'calibration.json'} and CALIBRATION.md; chosen {chosen}")

    if a.freeze:
        frozen_dir.mkdir(parents=True, exist_ok=True)
        cols = list(rows[0].keys())
        with open(frozen_files[1], "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        fz = {"_about": "The FROZEN automated reference (LEVELCHECK_MODEL.md section 14): the rule, its parameters, the "
                        "calibration table with intervals, and the assignment of every person (auto_truth.csv). Written "
                        "BEFORE any SchwingNet model ran on a G3 test person (results/fig6/unblinding/ empty; f6eval "
                        "40431765/40431766 held; 40427984 failed in 2 s with no model). Never edited after this write.",
              "git_head": head, "git_dirty": dirty, "utc": utc, "prespecification_commit": "b511985",
              "rule": chosen, "assignable_subtypes": assignable, "parameters": calibration["parameters"],
              "calibration_table": table, "calibration_set": calibration["calibration_set"],
              "dawid_skene": calibration["dawid_skene"], "inputs": inputs,
              "auto_truth_csv": {"path": str(frozen_files[1].relative_to(REPO)), "sha256": sha(frozen_files[1]),
                                 "rows": len(rows), "columns": cols},
              "real_frame_test_persons": usable, "n_min": N_MIN,
              "use": "R3: human-verified truth (section 4) is primary wherever it exists; a person with no human read "
                     "enters the primary analysis only with status assigned_*; every automated result is reported on "
                     "the unanimous subset and on the full rule subset, labelled with the calibration PPV."}
        json.dump(fz, open(frozen_files[0], "w"), indent=1, default=str)
        lines = [f"{sha(frozen_files[0])}  {frozen_files[0].name}", f"{sha(frozen_files[1])}  {frozen_files[1].name}"]
        with open(frozen_files[2], "w", encoding="utf-8", newline="\n") as f:      # LF: sha256sum -c reads it on the grid
            f.write("\n".join(lines) + "\n")
        print("FROZEN:\n" + "\n".join(lines))
    return 0


def fmt(t):
    if t is None or t[0] is None:
        return "n/a"
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def render_md(c: dict) -> str:
    L = ["# Automated reference: calibration (LEVELCHECK_MODEL.md section 14, R2)", "",
         f"Written {c['utc']} at git HEAD `{c['git_head'][:12]}`{' (working tree dirty)' if c['git_dirty'] else ''} by "
         f"`{c['tool']}`. Every number here is computed from the inputs in `calibration.json`; no G3 test person's "
         f"truth was read (test persons in the calibration set: {c['calibration_set']['test_persons_in_calibration']}, "
         f"asserted).", "",
         "## Calibration set", "",
         f"CTSpinoPelvic1K and VerSe persons on the G3 train and val sides with a human read: "
         f"n = {c['calibration_set']['n']} ({c['calibration_set']['by_corpus']}; sides {c['calibration_set']['by_side']}). "
         f"Truth classes: {c['calibration_set']['by_truth_class']}. A sacralised L5 that keeps its own id is scored as "
         f"`ordinary` (its alphabet is L1..L5; section 3: variant, naming unaffected); the alternative convention, "
         f"scoring it as `four_lumbar`, gives {c['calibration_set']['by_truth_class_alt']} and is tabulated below.",
         f"Outside the calibration set: {c['calibration_set']['excluded_from_calibration']}.", "",
         "Reader calls on the calibration set: " + "; ".join(f"{r}: {v}" for r, v in c["reader_calls_in_calibration"].items()), ""]

    def block(title, tab):
        L.extend([f"## {title}", "", "| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95 %] | sensitivity | class coverage | wrong truths |",
                  "|---|---:|---|---:|---:|---:|---|---|---|---|"])
        for name, m in tab.items():
            for cls, pc in m["per_class"].items():
                if pc["n_truth"] == 0 and pc["n_assigned"] == 0:
                    continue
                L.append(f"| {name} | {fmt(m['coverage'])} ({m['n_assigned']}/{m['n_calibration']}) | {cls} | {pc['n_truth']} | "
                         f"{pc['n_assigned']} | {pc['n_correct']} | {fmt(pc['ppv'])} | {fmt(pc['sensitivity'])} | "
                         f"{fmt(pc['class_coverage'])} | {pc['wrong_truths']} |")
        L.append("")

    block("Each reader alone (descriptive)", c["readers_alone"])
    block("The three pre-specified rules (own-id sacralised L5 = ordinary)", c["rules"])
    block("The same rules, own-id sacralised L5 scored as four_lumbar (sensitivity table)", c["rules_alt_truth_convention"])
    for name, per in c["rules_per_corpus"].items():
        block(f"Rule {name} per corpus", per)
    L.extend(["## Selection", "",
              f"A rule qualifies for a subtype when the PPV Wilson lower bound is at least {c['parameters']['ppv_wilson_lower_bound_min']}. "
              f"Qualifies for every subtype it assigns: {c['global_qualifies']}.",
              f"**Chosen:** mode `{c['chosen']['mode']}`; rule per subtype {c['chosen']['per_class']}; "
              f"assignable subtypes: {c['assignable_subtypes']}. A person whose call is a subtype outside this list is "
              f"excluded with the reason written in `auto_truth.csv`.", "",
              f"Dawid-Skene (fitted on the calibration persons only, abstentions as missing, posterior threshold "
              f"{c['parameters']['ds_posterior_threshold']}): prior " +
              ", ".join(f"{k} {v:.3f}" for k, v in c["dawid_skene"]["prior"].items()) + ".", ""])
    for r, conf in c["dawid_skene"]["confusion"].items():
        L.append(f"- reader {r}, P(call | truth): " + "; ".join(
            f"{k}: " + ", ".join(f"{l} {v:.2f}" for l, v in row.items() if v >= 0.02) for k, row in conf.items()))
    L.extend(["", "## Real-frame G3 test persons (T2 = COBRA, T3 = C-ArmLSpine) under the frozen rule", "",
              f"n_min (section 5): {c['n_min']}. Counts are persons; `with_frames` = persons with an exported real frame.", ""])
    for t, rep in c["real_frame_test_persons"].items():
        L.append(f"### {t}: {rep['persons']} persons, {rep['persons_with_frames']} with real frames")
        L.append("")
        L.append("| assigned subtype | persons | with frames | unanimous | unanimous with frames | T13 excluded by an anchored count | withheld: Varian not exported | withheld: no exported frame |")
        L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for k, v in rep["by_assigned_subtype"].items():
            L.append(f"| {k} | {v['all']} | {v['with_frames']} | {v['unanimous']} | {v['unanimous_with_frames']} | "
                     f"{v['t13_excluded_by_anchored_count']} | {v['withheld_varian_not_exported']} | {v['withheld_no_exported_frame']} |")
        L.append("")
        L.append("Excluded, by reason: " + json.dumps(rep["excluded_reasons"]))
        L.append("")
        L.append("Frozen stratum (stratify.json, VERIDAH-based for COBRA) -> automated assignment: " + json.dumps(rep["frozen_stratum_vs_assigned"]))
        L.append("")
    L.extend(["## Transportability of the ordinary PPV (anchored thoracic count or not)", "",
              "| rule | subset | assigned ordinary | correct | PPV [Wilson 95 %] | wrong truths |", "|---|---|---:|---:|---|---|"])
    for name, sub in c["transportability"].items():
        if name == "T2_assigned_ordinary":
            continue
        for lab, v in sub.items():
            L.append(f"| {name} | {lab} | {v['n_assigned_ordinary']} | {v['n_correct']} | {fmt(v['ppv'])} | {v['wrong_truths']} |")
    t2 = c["transportability"]["T2_assigned_ordinary"]
    L.extend(["", f"T2 persons assigned ordinary: {t2['n']}, of whom {t2['anchored']} had a thoracic count anchored at T1; by frozen "
                  f"(VERIDAH) stratum {t2['by_frozen_stratum']}; with frames {t2['by_frozen_stratum_with_frames']}. {t2['note']}", ""])
    L.extend(["## Assignment counts per corpus (side, status, subtype or exclusion reason)", ""])
    for corpus, d in c["assignment_counts"].items():
        L.append(f"- **{corpus}**: " + "; ".join(f"{k}: {v}" for k, v in sorted(d.items(), key=lambda kv: -kv[1])))
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
