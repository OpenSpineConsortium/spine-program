#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/score_m1_f1.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""M1 (the count against the count plus morphology) and F1 (the transitional flag), per person, exactly as
SchwingNet/LEVELCHECK_MODEL.md s12 defines them, on the s4 scored frame; and the validation-only choice of tau.

THE GOVERNING TEXT is LEVELCHECK_MODEL.md s4, s5, s9, s12 and s13 (F1b). This file implements it and changes nothing
in it. Where the text leaves a choice open, the choice is written into DEFINITIONS below and into every output, so it
is on record before unblinding (s9: "the mapping between the two is written down before unblinding").

INPUT: one dump per frame (a JSONL file, or a directory of .json files), schema

    {"stem": str, "person": str (G2 key), "set": "T2", "real": bool, "gate": "open" | "blinded",
     "truth": [{"box": [x0, y0, x1, y1], "level": "L3" | null}, ...],     # EVERY truth body box (cls 0), meta order
     "pred":  null | {                                                       # null = no model output for this frame
         "alphabet": "ordinary" | "L6" | "T13" | "both" | "L4" | "L4T13" | "no anchor" | "no alphabet",
         "alphabet_aliases": [...],                                          # alphabets giving the same names
         "bodies": [{"box": [...], "count": str | null, "morphology": str | null, "coupled": str | null,
                     "abstain": bool}, ...],                                 # detector boxes and the three namings
         "spine_prob": float | null}}                                        # the dual-loss arm's P(transitional)

`adapt` builds these from the Figure 6 outputs (tools/alphabet_couple.py couple_all.json per set/gate/variant, the
sets' persons.json and truth metas) plus a {stem: spine_prob} file. Truth is carried for every frame of BOTH gates,
because the s4 draw is computed from truth alone and must see every person the primary scorer sees.

THE SCORED FRAME (s4). A frame is eligible with at least four reference-named vertebral bodies, and for a person in
an at-risk stratum it must also be at risk (the s3 rule) -- both computed with SchwingNet/tools/fig6_score.py's own
`at_risk_names` and AT_RISK_STRATA, so this scorer and the primary scorer cannot drift. One eligible frame per person:
numpy.random.default_rng(20260923), persons in ascending key order, rng.integers(len(frames)) over the person's
eligible frames sorted by stem. The pool is the real frames (sets T2, T3) without the three C-ArmLSpine L6 patients,
which is fig6_score.py's primary pool; `--pool renders` gives the T1 draw, a labelled secondary. `--fig6-score`
checks the draw, and the COUPLED outcome, against the primary scorer's own output person by person.

CORRECT (s4, the matched endpoint). Every reference-named body is matched to a detected box (tools/alphabet_couple.py
match_truth: call centre inside the truth box, IoU >= 0.3, one to one, best first -- the coupler's own rule) and that
arm names it with its reference name. Not correct, as s4 lists them: a missed body; a detected body with no name; a
frame with no model output; for COUNT and COUPLED a frame without an anchor; and AN ABSTENTION -- a reference-named
body whose matched detection carries the prototype's per-body `abstain` (tools/level_prototype.py: the decoded name
differs from the single-crop name, or its probability is below --abstain-below, default 0.5; the "abstention" of
NUMBERS.md a7). The abstention applies to SchwingNet's own arms, MORPHOLOGY and COUPLED; COUNT is the surrogate
count and has none. SchwingNet/tools/fig6_score.py does NOT score an abstention as wrong for the primary ("counted
beside"), so its COUPLED outcome differs from s4 wherever a scored body abstains; s9 says LEVELCHECK_MODEL.md governs,
so M1 is decided on the s4 rule and the fig6_score rule is reported beside it (and is what `--fig6-score` compares).

M1 (s12). Persons of the lumbosacral transitional strata L6, both, sacralised_L5, four_lumbar (fig6_freeze.py's
strata for "L6; sacralised or fused L5; four-lumbar"; `both` carries an L6, so a count from the sacrum errs on it and
s12's reason for leaving T13 out does not apply). Three arms from one run: COUNT (ordinary alphabet at the ordinal
from the detected sacrum -- a within-study SURROGATE for a surgeon's count), MORPHOLOGY (the classifier's names),
COUPLED (the primary). Exact one-sided McNemar, COUPLED better than COUNT: b = COUPLED right and COUNT wrong, c = the
reverse, P = P(X >= b | b + c, 1/2), tested only if b + c >= 6 (below six discordant persons no outcome can reach
0.025: 1/32 > 0.025 >= 1/64), alpha 0.025. T13, ordinary and every other stratum: the same table, descriptive only.

F1 (s12, s13 F1b). Flag = (a) the coupling chose a non-ordinary alphabet (its call has no "ordinary" alias), OR (b)
the count and the morphology name some reference-named body differently, OR (c) -- the dual-loss arm only -- the
spine probability is at or above tau. Sensitivity over transitional test persons (pooled, then per subtype and per
stratum), specificity over ordinary test persons, Wilson 95 % (z = 1.959964, s11); target: sensitivity lower bound
>= 0.85 (FLAGSHIP_PLAN G6). One tau file per operating point (95 % and 97 % validation sensitivity).

TAU (s12, s13 F1b), `fix-tau`: on the G3 VALIDATION persons only (tools/head_dual.py writes their spine
probabilities, one s4-drawn validation film per person), tau = the largest value at which at least the target share
of transitional validation persons is at or above tau, i.e. the k-th largest probability with k = ceil(target * n)
computed exactly. The file is written once (never overwritten) with its sha256 beside it, and `score` refuses to
call F1(c) pre-specified unless the sha256 matches and the file's fixed_utc precedes the unblinding record.

UNBLINDING (s9) is the EARLIER of the first model run on a blinded person's frame and the first scoring. `adapt`
stamps every frame with `pred_written_utc`, the time its model output was written (the prototype run's
prototype_meta.json, else couple_all.json). The first `score` run that sees a model output for a blinded person
writes --unblinding-record exclusively: unblinded_utc = min(the earliest blinded model output, now), the UTC time of
this scoring, git rev-parse HEAD of --repo, and whether each pre-specification commit is its ancestor (true / false /
unknown when the commit is not in that clone). An existing record (this scorer's or the G6 evaluator's, which must
carry `unblinded_utc`) is read, never rewritten; if a dump shows a blinded model output earlier than it, the earlier
time governs and the output says so. The three C-ArmLSpine L6 patients do not trigger it (s4, s8: seen before the
freeze).

SUBSETS (`--subset NAME=FILE`, s14). The same M1 and F1 on a named subset of persons (a JSON list, a JSON object
keyed by person, or one key per line) -- e.g. the unanimous subset of the frozen automated reference. The draw is
made on the whole pool first, so a subset never moves a scored frame.

    python tools/score_m1_f1.py adapt --sets .../fig6/sets_v1 --runs .../fig6/eval_v1 --variant det74 \\
        [--spine-probs dual_spine_probs.json] --out dumps_primary.jsonl
    python tools/score_m1_f1.py fix-tau --val val_spine_<tag>.json --target 0.95 --out tau95.json
    python tools/score_m1_f1.py score --dumps dumps_dual.jsonl --strata .../frozen_v1/strata.json --arm dual \\
        --tau tau95.json --tau tau97.json --unblinding-record .../UNBLINDING_dual.json --out m1_f1_dual.json
    python tools/score_m1_f1.py self-test
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "SchwingNet" / "tools"))
from alphabet_couple import match_truth  # noqa: E402  the coupler's own truth matching
from fig6_score import AT_RISK_STRATA, SEED_DRAW, at_risk_names, wilson  # noqa: E402  the primary scorer's rules

ALPHA = 0.025
MIN_DISCORDANT = 6
F1_TARGET_LB = 0.85
LUMBOSACRAL_STRATA = ("L6", "both", "sacralised_L5", "four_lumbar")
TRANSITIONAL_SUBTYPES = ("L6", "T13", "both", "sacralised_L5_fused", "four_lumbar")
EXCLUDED_STRATA = ("carmlspine_three_L6",)
NO_ALPHABET = ("no anchor", "no alphabet")
ARMS = ("count", "morphology", "coupled")
SCHWINGNET_ARMS = ("morphology", "coupled")          # the arms that can abstain (s4); COUNT is the surrogate
PRESPEC_COMMITS = {"s1_to_s11_freeze": "ecae75f", "s12_M1_F1_D1": "1897772", "s13_S1_F1b": "2993f40",
                   "s14_auto_reference": "b511985"}

DEFINITIONS = {
    "governing_text": "SchwingNet/LEVELCHECK_MODEL.md s4, s5, s9, s12, s13 (F1b), s14",
    "m1_population": "frozen strata L6, both, sacralised_L5, four_lumbar (s12: 'L6; sacralised or fused L5; "
                     "four-lumbar'). 'both' carries an L6: a count from the sacrum errs on it, so s12's reason for "
                     "leaving T13 out does not apply; it is also shown on its own in by_stratum_descriptive",
    "correct": "s4: every reference-named body matched to a box and given its reference name by the arm; missed, "
               "unnamed, no model output, unanchored (COUNT, COUPLED) or ABSTAINED (MORPHOLOGY, COUPLED: the "
               "prototype's per-body abstain on a matched reference-named body) = not correct",
    "correct_fig6_rule": "the same without the abstention clause: SchwingNet/tools/fig6_score.py's rule for the primary "
                         "(abstentions counted beside). Reported beside M1, never the decision; --fig6-score compares it",
    "f1_transitional": "frozen subtype in L6, T13, both, sacralised_L5_fused, four_lumbar -- the dual head's training "
                       "label (tools/head_dual.py); a sacralised_L5_fused person whose L5 keeps its label (stratum "
                       "variant_naming_unaffected) is transitional here",
    "f1_ordinary": "frozen stratum 'ordinary' (everyone strata.json does not list)",
    "f1_other": "Castellvi I/II, lumbar rib, unassigned, unreadable: in neither denominator; flag rate reported",
    "excluded": "stratum carmlspine_three_L6 (s4), from the draw and from every table",
    "flag_b_bodies": "reference-named bodies matched to a box, as s12 words it; 'flag_ab_truth_free' (b over every "
                     "counted body, usable without truth) is reported beside it as a labelled secondary",
    "unanchored": "a frame without an anchor fires neither (a) nor (b); such persons are counted in each F1 block",
    "abstain": "s4: an abstention is not correct (see 'correct'); the count of abstentions on scored frames is "
               "printed beside every table",
    "tau": "k-th largest validation spine probability among transitional validation persons, k = ceil(target * n) "
           "exactly; one s4-drawn validation film per person; (c) alone, which bounds the combined flag's validation "
           "sensitivity from below",
    "unblinding": "the earlier of the first blinded model output (pred_written_utc) and the first scoring (s9); a tau "
                  "is pre-specified only if fixed strictly before it and its sha256 sidecar matches",
    "subsets": "M1 and F1 recomputed on a named person subset AFTER the whole-pool draw (s14: unanimous automated "
               "reference beside the rule's full subset)",
}


# ================================================================================================ small pieces
def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def parse_utc(s):
    return datetime.datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def mtime_utc(path):
    t = os.stat(path).st_mtime
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git_state(repo):
    """HEAD of `repo` and, per pre-specification commit, True / False / None (commit absent from this clone)."""
    def run(*args):
        try:
            return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=30)
        except Exception:  # noqa: BLE001
            return None
    r = run("rev-parse", "HEAD")
    head = r.stdout.strip() if (r is not None and r.returncode == 0) else None
    anc = {}
    for name, c in PRESPEC_COMMITS.items():
        rr = run("merge-base", "--is-ancestor", c, "HEAD") if head else None
        anc[name] = {"commit": c, "is_ancestor": (True if rr is not None and rr.returncode == 0 else
                                                  False if rr is not None and rr.returncode == 1 else None)}
    return {"repo": str(repo), "head": head, "prespec": anc}


def mcnemar_one_sided(b, c):
    """Exact one-sided McNemar: P(X >= b | X ~ Binomial(b + c, 1/2))."""
    n = b + c
    if n == 0:
        return 1.0
    return sum(math.comb(n, x) for x in range(b, n + 1)) / 2 ** n


def rate(k, n):
    return {"k": k, "n": n, "rate": (round(k / n, 4) if n else None), "wilson95": wilson(k, n)}


# ================================================================================================ persons and frames
def person_info(strata_doc, key):
    s = strata_doc["strata"].get(key)
    if s is None:
        d = strata_doc.get("default", {})
        info = {"stratum": d.get("stratum", "ordinary"), "subtype": "ordinary", "alphabet": d.get("alphabet"),
                "side": None, "gate": d.get("gate", "open"), "listed": False}
    else:
        info = {"stratum": s["stratum"], "subtype": s.get("subtype") or s["stratum"], "alphabet": s.get("alphabet"),
                "side": s.get("side"), "gate": s.get("gate"), "listed": True}
    info["f1_class"] = ("transitional" if info["subtype"] in TRANSITIONAL_SUBTYPES else
                        "ordinary" if info["stratum"] == "ordinary" else "other")
    return info


def truth_stats(truth_levels, info):
    """(number of reference-named bodies, at risk) -- fig6_score.py's frame rule."""
    named = [lv for lv in truth_levels if lv]
    risk = at_risk_names(info["alphabet"])
    return len(named), any(risk.get(n, False) for n in named)


def is_eligible(n_named, at_risk, stratum):
    if n_named < 4:
        return False
    return bool(at_risk) if stratum in AT_RISK_STRATA else True


def draw_scored_frames(eligible_by_person):
    """s4: default_rng(20260923), persons ascending, rng.integers over the eligible frames sorted by stem."""
    rng = np.random.default_rng(SEED_DRAW)
    out = {}
    for k in sorted(eligible_by_person):
        fl = sorted(eligible_by_person[k])
        if fl:
            out[k] = fl[int(rng.integers(len(fl)))]
    return out


def anchored(pred):
    return bool(pred) and pred.get("alphabet") is not None and pred.get("alphabet") not in NO_ALPHABET


def matched_named(rec):
    """[(reference name, matched body or None)] for every reference-named truth body of the frame."""
    pred = rec.get("pred") or {}
    bodies = pred.get("bodies") or []
    truth = rec["truth"]
    m = match_truth([b["box"] for b in bodies], [t["box"] for t in truth]) if (bodies and truth) else {}
    inv = {j: i for i, j in m.items()}
    return [(t["level"], bodies[inv[j]] if j in inv else None) for j, t in enumerate(truth) if t.get("level")]


def arm_correct(rec, arm, abstain_wrong=True):
    """s4 'correct' for one arm on one frame. abstain_wrong=False is fig6_score.py's rule (reported beside)."""
    pred = rec.get("pred")
    if not pred:
        return False
    if arm in ("count", "coupled") and not anchored(pred):
        return False
    pairs = matched_named(rec)
    if not pairs or any(b is None or b.get(arm) != lv for lv, b in pairs):
        return False
    if abstain_wrong and arm in SCHWINGNET_ARMS and any(b.get("abstain") for _, b in pairs):
        return False
    return True


def flag_a(pred):
    if not anchored(pred):
        return False
    return "ordinary" not in (pred.get("alphabet_aliases") or [pred["alphabet"]])


def _disagree(b):
    return b is not None and b.get("count") is not None and b.get("morphology") is not None and b["count"] != b["morphology"]


def flag_b(rec):
    return any(_disagree(b) for _, b in matched_named(rec))


def flag_b_truth_free(pred):
    return any(_disagree(b) for b in ((pred or {}).get("bodies") or []))


def flag_c(pred, tau):
    p = (pred or {}).get("spine_prob")
    return p is not None and float(p) >= float(tau)


def load_dumps(path):
    p = Path(path)
    recs = []
    if p.is_dir():
        for f in sorted(p.glob("*.json")):
            recs.append(json.load(open(f)))
    else:
        for line in open(p):
            if line.strip():
                recs.append(json.loads(line))
    return recs


# ================================================================================================ tau
def fix_tau(val_doc, target):
    """tau = the k-th largest transitional validation probability, k = ceil(target * n) exactly."""
    persons = val_doc["persons"]
    tr = sorted((float(v["p"]) for v in persons.values() if v.get("transitional") and v.get("p") is not None), reverse=True)
    n = len(tr)
    if n == 0:
        raise SystemExit("no transitional validation person carries a spine probability: tau cannot be fixed")
    k = math.ceil(Fraction(str(target)) * n)
    tau = tr[k - 1]
    ordn = [float(v["p"]) for v in persons.values() if v.get("f1_class") == "ordinary" and v.get("p") is not None]
    k_sens = sum(1 for p in tr if p >= tau)
    k_spec = sum(1 for p in ordn if p < tau)
    return {"tau": tau, "target_sensitivity": float(target), "k_required": k, "n_transitional_val_persons": n,
            "val_sensitivity": rate(k_sens, n), "val_specificity": rate(k_spec, len(ordn)),
            "by_subtype": {s: rate(sum(1 for v in persons.values() if v.get("subtype") == s and v.get("transitional")
                                       and v.get("p") is not None and float(v["p"]) >= tau),
                                   sum(1 for v in persons.values() if v.get("subtype") == s and v.get("transitional")
                                       and v.get("p") is not None))
                           for s in sorted({v.get("subtype") for v in persons.values() if v.get("transitional")})}}


def write_tau(val_path, target, out_path, repo=REPO, arm="D1"):
    raw = open(val_path, "rb").read()
    val_doc = json.loads(raw)
    t = fix_tau(val_doc, target)
    rec = {"what": "tau for F1(c), SchwingNet/LEVELCHECK_MODEL.md s12 (95 %) / s13 F1b (97 %)", "arm": arm,
           **t, "rule": DEFINITIONS["tau"], "validation_file": str(Path(val_path).resolve()),
           "validation_sha256": sha256_bytes(raw), "validation_tag": val_doc.get("tag"),
           "fixed_utc": now_utc(), "git": git_state(repo), "host": platform.node(),
           "tool": "tools/score_m1_f1.py fix-tau"}
    body = json.dumps(rec, indent=1).encode()
    with open(out_path, "xb") as f:          # a fixed value is never rewritten
        f.write(body)
    with open(str(out_path) + ".sha256", "x") as f:
        f.write(f"{sha256_bytes(body)}  {Path(out_path).name}\n")
    return rec


def load_tau(path, unblinded_utc):
    raw = open(path, "rb").read()
    d = json.loads(raw)
    sha = sha256_bytes(raw)
    side = Path(str(path) + ".sha256")
    recorded = side.read_text().split()[0] if side.exists() else None
    why = []
    if recorded != sha:
        why.append("sha256 sidecar missing or does not match the file")
    if unblinded_utc is not None and not (parse_utc(d["fixed_utc"]) < parse_utc(unblinded_utc)):
        why.append(f"fixed {d['fixed_utc']}, not before unblinding {unblinded_utc}")
    return {"path": str(Path(path).resolve()), "tau": float(d["tau"]), "target": d.get("target_sensitivity"),
            "sha256": sha, "sha256_recorded": recorded, "fixed_utc": d.get("fixed_utc"),
            "pre_specified": not why, "why_not": why}


# ================================================================================================ the scoring
def unblinding_record(path, arm, repo, first_output_utc=None, tool="tools/score_m1_f1.py score",
                      event="first scoring of a model output for a blinded-stratum G3 test person"):
    """Read the record, or write it exclusively: unblinded_utc = min(first blinded model output, now) (s9)."""
    p = Path(path)
    if p.exists():
        rec = json.load(open(p))
        if "unblinded_utc" not in rec:
            raise SystemExit(f"{p}: an unblinding record without `unblinded_utc` (keys {sorted(rec)[:8]})")
        return rec, False
    p.parent.mkdir(parents=True, exist_ok=True)
    now = now_utc()
    first = first_output_utc if (first_output_utc and parse_utc(first_output_utc) < parse_utc(now)) else None
    rec = {"unblinded_utc": first or now,
           "unblinding_event": ("the first model output on a blinded person's frame (earlier than this scoring)" if first
                                else event),
           "first_blinded_model_output_utc": first_output_utc, "recorded_utc": now, "event_recorded": event,
           "arm": arm, "tool": tool, "host": platform.node(), "git": git_state(repo)}
    with open(p, "x") as f:
        json.dump(rec, f, indent=1)
    return rec, True


def first_blinded_output(recs, info_of):
    """Earliest pred_written_utc over every frame of a blinded person that carries a model output (any pool)."""
    ts = [r["pred_written_utc"] for r in recs
          if r.get("pred") is not None and r.get("pred_written_utc")
          and info_of[r["person"]]["gate"] != "open" and info_of[r["person"]]["stratum"] not in EXCLUDED_STRATA]
    return min(ts, key=parse_utc) if ts else None


def f1_block(persons, flagged):
    """Sensitivity (transitional), specificity (ordinary), per subtype and stratum, for one flag rule."""
    tr = [p for p in persons if p["f1_class"] == "transitional"]
    od = [p for p in persons if p["f1_class"] == "ordinary"]
    ot = [p for p in persons if p["f1_class"] == "other"]
    sens = rate(sum(1 for p in tr if flagged(p)), len(tr))
    spec = rate(sum(1 for p in od if not flagged(p)), len(od))
    lb = sens["wilson95"][0] if sens["wilson95"] else None
    return {"sensitivity": sens, "specificity": spec,
            "target_sensitivity_lower_bound": F1_TARGET_LB,
            "target_met": (lb is not None and lb >= F1_TARGET_LB),
            "sensitivity_by_subtype": {s: rate(sum(1 for p in tr if p["subtype"] == s and flagged(p)),
                                               sum(1 for p in tr if p["subtype"] == s))
                                       for s in sorted({p["subtype"] for p in tr})},
            "sensitivity_by_stratum": {s: rate(sum(1 for p in tr if p["stratum"] == s and flagged(p)),
                                               sum(1 for p in tr if p["stratum"] == s))
                                       for s in sorted({p["stratum"] for p in tr})},
            "other_flag_rate_by_stratum": {s: rate(sum(1 for p in ot if p["stratum"] == s and flagged(p)),
                                                   sum(1 for p in ot if p["stratum"] == s))
                                           for s in sorted({p["stratum"] for p in ot})},
            "transitional_unanchored": sum(1 for p in tr if not p["anchored"]),
            "transitional_without_prediction": sum(1 for p in tr if not p["has_pred"])}


def three_arm(persons, key="correct"):
    """COUNT / MORPHOLOGY / COUPLED on one person set, and the discordant pairs of COUPLED against COUNT."""
    n = len(persons)
    b = sum(1 for p in persons if p[key]["coupled"] and not p[key]["count"])
    c = sum(1 for p in persons if p[key]["count"] and not p[key]["coupled"])
    return {"n": n, "rule": key, **{arm: rate(sum(1 for p in persons if p[key][arm]), n) for arm in ARMS},
            "discordant": {"coupled_right_count_wrong": b, "count_right_coupled_wrong": c},
            "mcnemar_one_sided_P": round(mcnemar_one_sided(b, c), 6),
            "abstentions_on_scored_frames": sum(p["abstentions"] for p in persons),
            "persons_with_an_abstained_scored_body": sum(1 for p in persons if p["abstained_named"])}


def m1_block(persons):
    ls = [p for p in persons if p["stratum"] in LUMBOSACRAL_STRATA]
    pooled = three_arm(ls)
    n_disc = sum(pooled["discordant"].values())
    tested = n_disc >= MIN_DISCORDANT
    return {"population": "lumbosacral transitional strata " + ", ".join(LUMBOSACRAL_STRATA),
            "count_arm_is_a_surrogate": "the ordinary alphabet counted up from the detected sacrum: a within-study "
                                        "surrogate for a surgeon's count, never a surgeon",
            "pooled": pooled,
            "test": {"exact_one_sided_mcnemar": "coupled better than count", "alpha": ALPHA,
                     "outcome_rule": "s4 (an abstention is not correct)",
                     "min_discordant": MIN_DISCORDANT, "discordant": n_disc, "tested": tested,
                     "P": pooled["mcnemar_one_sided_P"] if tested else None,
                     "rejected": bool(tested and pooled["mcnemar_one_sided_P"] <= ALPHA),
                     "status": ("tested" if tested else f"descriptive: {n_disc} discordant < {MIN_DISCORDANT}")},
            "pooled_fig6_rule_beside": dict(three_arm(ls, "correct_fig6_rule"),
                                            note="abstentions not scored (SchwingNet/tools/fig6_score.py's rule for the "
                                                 "primary); reported beside, NOT the M1 decision"),
            "by_stratum_descriptive": {s: three_arm([p for p in persons if p["stratum"] == s])
                                       for s in sorted({p["stratum"] for p in persons})}}


def f1_blocks(persons, tau_recs):
    f1 = {"a_or_b": f1_block(persons, lambda p: p["flag"]["a"] or p["flag"]["b"]),
          "a_or_b_truth_free_secondary": f1_block(persons, lambda p: p["flag"]["a"] or p["flag"]["b_truth_free"])}
    for t in tau_recs:
        key = f"c@{t['tau']:.6g}"
        f1[f"a_or_b_or_c@tau{t['target']}"] = dict(f1_block(persons, lambda p, key=key: p["flag"]["a"] or p["flag"]["b"]
                                                               or p["flag"][key]),
                                                    tau=t["tau"], pre_specified=t["pre_specified"], why_not=t["why_not"])
        f1[f"c_alone@tau{t['target']}"] = f1_block(persons, lambda p, key=key: p["flag"][key])
    return f1


def load_subset(path):
    p = Path(path)
    txt = p.read_text()
    try:
        d = json.loads(txt)
    except json.JSONDecodeError:
        return {ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.startswith("#")}
    if isinstance(d, dict):
        d = d.get("persons", d)
    return set(d)


def score(recs, strata_doc, arm="primary", taus=(), pool="real", unblinding_path=None, repo=REPO,
          fig6_score_path=None, fig6_key=None, subsets=None):
    if arm != "dual" and taus:
        raise SystemExit("F1(c) is the dual-loss arm's rule only (s12); no tau is applied to arm " + repr(arm))
    want_real = (pool == "real")
    info_of, frames, excluded = {}, {}, Counter()
    for r in recs:
        info_of.setdefault(r["person"], person_info(strata_doc, r["person"]))
    for r in recs:
        k = r["person"]
        info = info_of[k]
        if info["stratum"] in EXCLUDED_STRATA:
            excluded[info["stratum"]] += 1
            continue
        if bool(r.get("real")) != want_real:
            continue
        if r["stem"] in frames:
            raise SystemExit(f"frame {r['stem']} appears twice in the dumps")
        n_named, at_risk = truth_stats([t.get("level") for t in r["truth"]], info)
        frames[r["stem"]] = dict(r, _n_named=n_named, _at_risk=at_risk,
                                 _eligible=is_eligible(n_named, at_risk, info["stratum"]))
    eligible_by_person = defaultdict(list)
    for stem, fr in frames.items():
        if fr["_eligible"]:
            eligible_by_person[fr["person"]].append(stem)
    draw = draw_scored_frames(eligible_by_person)

    # ---- unblinding (s9): the earlier of the first blinded model output and this scoring. Every frame of every
    # pool in the dumps counts, not only the drawn ones: s9 says "any frame of a G3 test person".
    blinded_with_pred = sorted({r["person"] for r in recs if r.get("pred") is not None
                                and info_of[r["person"]]["gate"] != "open"
                                and info_of[r["person"]]["stratum"] not in EXCLUDED_STRATA})
    first_out = first_blinded_output(recs, info_of)
    unb, created = (None, False)
    if blinded_with_pred and unblinding_path:
        unb, created = unblinding_record(unblinding_path, arm, repo, first_out)
    elif blinded_with_pred:
        raise SystemExit(f"{len(blinded_with_pred)} blinded persons carry a model output: pass --unblinding-record")
    unb_utc = unb.get("unblinded_utc") if unb else None
    earlier_output = bool(unb_utc and first_out and parse_utc(first_out) < parse_utc(unb_utc))
    eff_utc = first_out if earlier_output else unb_utc
    tau_recs = [load_tau(t, eff_utc) for t in taus]

    persons = []
    for k, stem in sorted(draw.items()):
        fr, info = frames[stem], info_of[k]
        pred = fr.get("pred")
        pairs = matched_named(fr) if pred else []
        p = {"person": k, "frame": stem, "set": fr.get("set"), "gate": fr.get("gate"), **{x: info[x] for x in (
             "stratum", "subtype", "f1_class", "side")},
             "n_named": fr["_n_named"], "has_pred": pred is not None, "anchored": anchored(pred),
             "alphabet": (pred or {}).get("alphabet"), "spine_prob": (pred or {}).get("spine_prob"),
             "abstentions": sum(1 for b in ((pred or {}).get("bodies") or []) if b.get("abstain")),
             "abstained_named": any(b is not None and b.get("abstain") for _, b in pairs),
             "correct": {a_: arm_correct(fr, a_) for a_ in ARMS},
             "correct_fig6_rule": {a_: arm_correct(fr, a_, abstain_wrong=False) for a_ in ARMS},
             "flag": {"a": flag_a(pred), "b": flag_b(fr), "b_truth_free": flag_b_truth_free(pred)}}
        for t in tau_recs:
            p["flag"][f"c@{t['tau']:.6g}"] = flag_c(pred, t["tau"])
        persons.append(p)

    m1 = m1_block(persons)
    f1 = f1_blocks(persons, tau_recs)
    sub_out = {}
    for name, keys in (subsets or {}).items():
        sp = [p for p in persons if p["person"] in keys]
        sub_out[name] = {"persons_listed": len(keys), "persons_scored": len(sp),
                         "listed_not_drawn": len(set(keys) - {p["person"] for p in persons}),
                         "M1": m1_block(sp), "F1": f1_blocks(sp, tau_recs)}

    # ---- the primary scorer's own output, person by person (its rule: abstentions not scored)
    cross = None
    if fig6_score_path:
        d = json.load(open(fig6_score_path))
        theirs = d["draws"]["primary_real" if want_real else "T1_renders"]
        mism = sorted(k for k in set(theirs) | set(draw) if theirs.get(k) != draw.get(k))
        cross = {"file": str(Path(fig6_score_path).resolve()), "draw_persons_here": len(draw),
                 "draw_persons_there": len(theirs), "draw_mismatches": mism[:50], "n_draw_mismatches": len(mism)}
        if fig6_key:
            pp = d["results"].get(fig6_key, {}).get("per_person", {})
            cm = sorted(p["person"] for p in persons if p["person"] in pp
                        and bool(pp[p["person"]]["correct"]["coupled"]) != p["correct_fig6_rule"]["coupled"])
            cross.update({"results_key": fig6_key, "compared_rule": "correct_fig6_rule",
                          "coupled_compared": sum(1 for p in persons if p["person"] in pp),
                          "coupled_mismatches": cm[:50], "n_coupled_mismatches": len(cm),
                          "s4_differs_from_fig6_rule": sorted(p["person"] for p in persons
                                                              if p["correct"]["coupled"] != p["correct_fig6_rule"]["coupled"])})

    no_pred = [p["person"] for p in persons if not p["has_pred"]]
    return {"generated_utc": now_utc(), "tool": "tools/score_m1_f1.py score", "arm": arm, "pool": pool,
            "role": ("SECONDARY analyses outside the H1-H6 family (s12); never confirmatory" +
                     ("; renders: a labelled secondary" if pool == "renders" else "")),
            "git_at_scoring": git_state(repo), "host": platform.node(),
            "unblinding": {"record": unb, "created_now": created, "path": unblinding_path,
                           "first_blinded_model_output_in_dumps_utc": first_out,
                           "effective_unblinded_utc": eff_utc,
                           "a_dump_output_precedes_the_record": earlier_output},
            "tau": tau_recs, "definitions": DEFINITIONS,
            "draw_rule": "numpy.random.default_rng(20260923); persons ascending; rng.integers(len(frames)) over eligible "
                         "frames sorted by stem; truth only; pool " + pool + " without carmlspine_three_L6",
            "excluded_frames": dict(excluded), "frames_in_pool": len(frames),
            "persons_scored": len(persons), "persons_by_stratum": dict(Counter(p["stratum"] for p in persons)),
            "persons_not_test_side": sorted(p["person"] for p in persons if p["side"] not in (None, "test")),
            "incomplete": bool(no_pred), "scored_frames_without_prediction": no_pred[:100],
            "n_scored_frames_without_prediction": len(no_pred),
            "M1": m1, "F1": f1, "subsets": sub_out, "fig6_crosscheck": cross, "draw": draw, "persons": persons}


# ================================================================================================ adapt
def cmd_adapt(a):
    probs = json.load(open(a.spine_probs)) if a.spine_probs else {}
    sets = Path(a.sets)
    out = []
    for st in [s.strip() for s in a.set_names.split(",") if s.strip()]:
        pj = sets / st / "persons.json"
        if not pj.exists():
            continue
        persons = json.load(open(pj))
        for gate in ("open", "blinded"):
            ca = Path(a.runs) / st / gate / a.variant / "couple" / "couple_all.json"
            couple, written, written_from = {}, None, None
            if ca.exists():
                ca_doc = json.load(open(ca))
                couple = {r["stem"]: r for r in ca_doc["frames"]}
                # when the model ran on these frames (s9): the prototype run's prototype_meta.json, written before
                # its first image is read; the couple file only when that directory is not reachable from here
                pm = Path(os.path.expanduser(str((ca_doc.get("args") or {}).get("pred") or ""))) / "prototype_meta.json"
                cands = [(mtime_utc(pm), str(pm))] if (pm.name and pm.exists() and pm.is_file()) else []
                cands.append((mtime_utc(ca), str(ca)))
                written, written_from = min(cands, key=lambda t: parse_utc(t[0]))
            for k, p in persons.items():
                for stem in p["frames"][gate]:
                    m = json.load(open(sets / st / gate / "meta" / f"{stem}.json"))
                    truth = [{"box": [float(v) for v in b["box"][:4]], "level": b.get("level")}
                             for b in m.get("boxes", []) if b.get("cls") == 0]
                    r = couple.get(stem)
                    pred = None
                    if r is not None:
                        pred = {"alphabet": r["call"], "alphabet_aliases": r.get("call_aliases") or [r["call"]],
                                "bodies": [{"box": b["box"], "count": b.get("count"), "morphology": b.get("classifier"),
                                            "coupled": b.get("coupled"), "abstain": bool(b.get("abstain"))}
                                           for b in r["bodies"]],
                                "spine_prob": probs.get(stem), "couple_n_truth_named": r.get("n_truth_named")}
                    out.append({"stem": stem, "person": k, "set": st, "real": st != "T1", "gate": gate,
                                "truth": truth, "pred": pred,
                                "pred_written_utc": written if pred is not None else None,
                                "pred_written_from": written_from if pred is not None else None})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    print(f"wrote {len(out)} frame dumps ({sum(1 for r in out if r['pred'])} with a model output) to {a.out}")
    return 0


def cmd_fix_tau(a):
    rec = write_tau(a.val, a.target, a.out, repo=Path(a.repo), arm=a.arm)
    print(json.dumps({k: rec[k] for k in ("tau", "target_sensitivity", "k_required", "n_transitional_val_persons",
                                          "val_sensitivity", "val_specificity", "fixed_utc")}, indent=1))
    print(f"wrote {a.out} and {a.out}.sha256")
    return 0


def summary_lines(res, head=""):
    L = []
    m = res["M1"]
    rows = [("M1 pooled (s4 rule)", m["pooled"]), ("M1 pooled, fig6 rule (beside)", m["pooled_fig6_rule_beside"])]
    rows += [(f"   {s}", v) for s, v in m["by_stratum_descriptive"].items()]
    for name, blk in rows:
        L.append(f"{head}{name:<34} n={blk['n']:>4}  count {blk['count']['k']:>3}  morphology {blk['morphology']['k']:>3}  "
                 f"coupled {blk['coupled']['k']:>3}  discordant b={blk['discordant']['coupled_right_count_wrong']} "
                 f"c={blk['discordant']['count_right_coupled_wrong']}  P={blk['mcnemar_one_sided_P']}  "
                 f"abstained-scored persons {blk['persons_with_an_abstained_scored_body']}")
    t = m["test"]
    L.append(f"{head}M1 test: {t['status']}; P={t['P']} rejected={t['rejected']}")
    for name, blk in res["F1"].items():
        s, sp = blk["sensitivity"], blk["specificity"]
        L.append(f"{head}F1 {name:<34} sens {s['k']}/{s['n']} {s['wilson95']}  spec {sp['k']}/{sp['n']} {sp['wilson95']}  "
                 f"target_met={blk['target_met']}" + (f"  pre_specified={blk['pre_specified']}" if "pre_specified" in blk else ""))
    for name, sub in (res.get("subsets") or {}).items():
        L.append(f"SUBSET {name}: {sub['persons_scored']} scored of {sub['persons_listed']} listed")
        L += summary_lines(dict(sub, subsets=None), head=f"  [{name}] ")
    return L


def cmd_score(a):
    subsets = {}
    for s in a.subset:
        name, _, path = s.partition("=")
        if not path:
            raise SystemExit(f"--subset {s!r}: expected NAME=FILE")
        subsets[name] = load_subset(path)
    res = score(load_dumps(a.dumps), json.load(open(a.strata)), arm=a.arm, taus=a.tau, pool=a.pool,
                unblinding_path=a.unblinding_record, repo=Path(a.repo), fig6_score_path=a.fig6_score,
                fig6_key=a.fig6_key, subsets=subsets)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("\n".join(summary_lines(res)))
    if res["unblinding"]["a_dump_output_precedes_the_record"]:
        print(f"NOTE: a blinded model output ({res['unblinding']['first_blinded_model_output_in_dumps_utc']}) precedes "
              f"the unblinding record ({res['unblinding']['record']['unblinded_utc']}); the earlier time governs")
    if res["incomplete"]:
        print(f"WARNING: {res['n_scored_frames_without_prediction']} scored frames carry no model output; "
              f"they are scored wrong and unflagged")
    print(f"wrote {a.out}")
    return 0


# ================================================================================================ self-test
def _frame(stem, person, truth, count=None, morph=None, coupled=None, alphabet="ordinary", aliases=None,
           spine=None, drop=(), real=True, gate="open", pred=True, abstain=(), written=None):
    """Bodies stacked in a column; predicted boxes equal the truth boxes except the `drop` indices (missed);
    `abstain` indices carry the prototype's per-body abstain; `written` is the frame's pred_written_utc."""
    boxes = [[100.0, 100.0 * i, 200.0, 100.0 * i + 80.0] for i in range(len(truth))]
    rec = {"stem": stem, "person": person, "set": "T2" if real else "T1", "real": real, "gate": gate,
           "truth": [{"box": b, "level": lv} for b, lv in zip(boxes, truth)], "pred": None, "pred_written_utc": None}
    if pred:
        count = count if count is not None else [None] * len(truth)
        rec["pred"] = {"alphabet": alphabet, "alphabet_aliases": aliases or [alphabet], "spine_prob": spine,
                       "bodies": [{"box": b, "count": c, "morphology": m_, "coupled": cp, "abstain": i in abstain}
                                  for i, (b, c, m_, cp) in enumerate(zip(boxes, count, morph, coupled)) if i not in drop]}
        rec["pred_written_utc"] = written
    return rec


def self_test():
    ok = []

    def check(name, got, want):
        good = (abs(got - want) < 1e-9) if isinstance(want, float) else (got == want)
        ok.append(good)
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: got {got!r}, want {want!r}")

    print("1. Wilson intervals against the values printed in LEVELCHECK_MODEL.md s2 (an outside check)")
    for (k, n), want in {(33, 71): [0.354, 0.580], (6, 34): [0.083, 0.335], (10, 48): [0.117, 0.343],
                         (20, 20): [0.839, 1.0], (373, 410): [0.878, 0.934], (12, 885): [0.008, 0.024]}.items():
        # fig6_score.wilson rounds to 4 decimals and the document prints 0.1 %: compare within both roundings
        # (rounding the 4-decimal value again would turn 0.08349 -> 0.0835 -> 0.084 against the printed 8.3 %)
        w = wilson(k, n)
        check(f"wilson({k},{n}) = {w} within 0.06 points of {want}",
              max(abs(w[0] - want[0]), abs(w[1] - want[1])) <= 0.0006, True)

    print("2. exact one-sided McNemar and the six-discordant rule")
    check("P(X>=8 | 9, 1/2) = 10/512", mcnemar_one_sided(8, 1), 10 / 512)
    check("P(X>=9 | 10, 1/2) = 11/1024", mcnemar_one_sided(9, 1), 11 / 1024)
    check("P(X>=6 | 6, 1/2) = 1/64", mcnemar_one_sided(6, 0), 1 / 64)
    check("P(X>=5 | 5, 1/2) = 1/32 > 0.025 (why six)", mcnemar_one_sided(5, 0) > ALPHA, True)
    check("P(X>=6 | 7, 1/2) = 8/128", mcnemar_one_sided(6, 1), 8 / 128)
    try:
        from scipy.stats import binomtest
        check("McNemar P == scipy binomtest(9, 10, 0.5, 'greater') (an independent implementation)",
              round(mcnemar_one_sided(9, 1), 12), round(float(binomtest(9, 10, 0.5, alternative="greater").pvalue), 12))
    except ImportError:
        print("  (scipy absent: the independent binomial check is skipped)")

    # ------------------------------------------------------------------ the synthetic study
    L6 = {"l6": True, "t13": False, "l4": False}
    L4 = {"l6": False, "t13": False, "l4": True}
    T13 = {"l6": False, "t13": True, "l4": False}
    BOTH = {"l6": True, "t13": True, "l4": False}
    OA = {"l6": False, "t13": False, "l4": False}
    strata = {"default": {"stratum": "ordinary", "alphabet": OA, "gate": "open"}, "strata": {}}

    def put(k, stratum, subtype, al, gate="blinded", into=strata):
        into["strata"][k] = {"stratum": stratum, "subtype": subtype, "alphabet": al, "side": "test", "gate": gate}

    recs = []
    t6 = ["L3", "L4", "L5", "L6"]
    shifted6 = ["L2", "L3", "L4", "L5"]
    # the excluded patient sorts FIRST: were it drawn, every later draw would shift
    put("carmlspine:case042", "carmlspine_three_L6", "L6", L6)
    recs += [_frame(f"carm42_{i}", "carmlspine:case042", t6, shifted6, t6, t6, "L6", spine=0.9, gate="blinded")
             for i in range(3)]

    def person(k, stratum, subtype, al, n_frames, gate="blinded", **kw):
        if stratum != "ordinary":
            put(k, stratum, subtype, al, gate)
        for i in range(n_frames):
            recs.append(_frame(f"{k.replace(':', '_')}_f{i}", k, gate=gate, **kw))
        # a three-body frame whose outcome is the opposite: never eligible, so it must never be drawn
        tr3 = kw["truth"][:3]
        recs.append(_frame(f"{k.replace(':', '_')}_z3", k, tr3, count=tr3, morph=tr3, coupled=tr3,
                           alphabet="ordinary", spine=0.0, gate=gate) if kw.get("alphabet") != "ordinary" else
                    _frame(f"{k.replace(':', '_')}_z3", k, tr3, count=["C1"] * 3, morph=["C2"] * 3, coupled=["C3"] * 3,
                           alphabet="L6", spine=1.0, gate=gate))

    for i, c in enumerate("abcdef"):   # coupling wins: the count shifts every name, the morphology calls L6 an L5
        person(f"ctsp:L6{c}", "L6", "L6", L6, 1 + i % 3, truth=t6, count=shifted6, morph=["L3", "L4", "L5", "L5"],
               coupled=t6, alphabet="L6", spine=0.8)
    person("ctsp:L6g", "L6", "L6", L6, 2, truth=t6, count=t6, morph=t6, coupled=shifted6, alphabet="L6", spine=0.7)
    person("ctsp:L6h", "L6", "L6", L6, 1, truth=t6, count=t6, morph=t6, coupled=t6, alphabet="ordinary", spine=0.9)
    person("ctsp:L6i", "L6", "L6", L6, 2, truth=t6, count=shifted6, morph=t6, coupled=t6, alphabet="L6", spine=0.5,
           drop=(0,))
    # an L6 + T13 spine: the count from the sacrum errs on it exactly as on an L6 spine, so it is in M1
    person("verse:BOTHa", "both", "both", BOTH, 1, truth=t6, count=shifted6, morph=["L3", "L4", "L5", "L5"],
           coupled=t6, alphabet="both", spine=0.2)
    t4 = ["L1", "L2", "L3", "L4"]
    for c in "ab":
        person(f"verse:SL5{c}", "sacralised_L5", "sacralised_L5_fused", L4, 2, truth=t4, count=["L2", "L3", "L4", "L5"],
               morph=["L2", "L3", "L4", "L5"], coupled=t4, alphabet="L4", spine=0.3)
    person("cobra:FLa", "four_lumbar", "four_lumbar", L4, 1, truth=t4, count=[None] * 4, morph=t4, coupled=t4,
           alphabet="no anchor", spine=0.2)
    t13 = ["T12", "T13", "L1", "L2"]
    person("verse:T13a", "T13", "T13", T13, 1, truth=t13, count=["T11", "T12", "L1", "L2"],
           morph=["T12", "T12", "L1", "L2"], coupled=t13, alphabet="T13", spine=0.4)
    person("verse:T13b", "T13", "T13", T13, 1, truth=t13, count=["T11", "T12", "L1", "L2"],
           morph=["T11", "T12", "L1", "L2"], coupled=["T11", "T12", "L1", "L2"], alphabet="ordinary", spine=0.1)
    to = ["L2", "L3", "L4", "L5"]
    person("verse:VNUa", "variant_naming_unaffected", "sacralised_L5_fused", OA, 1, truth=to, count=to, morph=to,
           coupled=to, alphabet="ordinary", spine=0.95)
    for i, c in enumerate("abcd"):
        person(f"ctsp:O{c}", "ordinary", "ordinary", OA, 1 + i % 2, gate="open", truth=to, count=to, morph=to,
               coupled=to, alphabet="ordinary", spine=0.1 + 0.05 * i)
    person("ctsp:Oe", "ordinary", "ordinary", OA, 1, gate="open", truth=to, count=to, morph=["L2", "L3", "L4", "L4"],
           coupled=to, alphabet="ordinary", spine=0.2)
    person("ctsp:Of", "ordinary", "ordinary", OA, 1, gate="open", truth=to, count=to, morph=to, coupled=to,
           alphabet="ordinary", spine=0.65)
    person("cobra:Ua", "unreadable", None, None, 1, truth=to, count=to, morph=to, coupled=to, alphabet="L6",
           aliases=["L6"], spine=0.3)
    # a render of an ordinary person: outside the real pool
    recs.append(_frame("render_x", "ctsp:Oa", to, to, to, to, real=False, gate="open"))

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # ---- tau on synthetic validation persons, BEFORE any test output is scored
        print("3. tau on validation: 20 transitional persons at p = 0.05..1.00, 10 ordinary at 0.00..0.45")
        val = {"tag": "selftest", "persons": {}}
        for i in range(20):
            val["persons"][f"v:t{i:02d}"] = {"transitional": True, "f1_class": "transitional",
                                             "subtype": "L6" if i % 2 else "T13", "p": round(0.05 * (i + 1), 2)}
        for i in range(10):
            val["persons"][f"v:o{i:02d}"] = {"transitional": False, "f1_class": "ordinary", "subtype": "ordinary",
                                             "p": round(0.05 * i, 2)}
        vp = td / "val.json"
        json.dump(val, open(vp, "w"))
        r95 = write_tau(vp, 0.95, td / "tau95.json")
        r97 = write_tau(vp, 0.97, td / "tau97.json")
        check("tau at 95 %: k = ceil(19.0) = 19 -> 19th largest = 0.10", r95["tau"], 0.10)
        check("tau at 97 %: k = ceil(19.4) = 20 -> smallest = 0.05", r97["tau"], 0.05)
        check("validation sensitivity at tau95 = 19/20", r95["val_sensitivity"]["k"], 19)
        check("validation specificity at tau95 (p < 0.10: 0.00, 0.05) = 2/10", r95["val_specificity"]["k"], 2)
        check("tau95 is the LARGEST passing value: one step above it, sensitivity falls below 95 %",
              sum(1 for v in val["persons"].values() if v["transitional"] and v["p"] >= 0.10 + 1e-9) / 20 < 0.95, True)
        try:
            write_tau(vp, 0.95, td / "tau95.json")
            check("a tau file is never overwritten", False, True)
        except FileExistsError:
            check("a tau file is never overwritten", True, True)
        # a deliberately different operating point, used for the known-answer F1 below
        val6 = {"tag": "selftest06", "persons": {f"v:t{i}": {"transitional": True, "f1_class": "transitional",
                                                             "subtype": "L6", "p": p} for i, p in enumerate([0.6] * 20)}}
        json.dump(val6, open(td / "val06.json", "w"))
        write_tau(td / "val06.json", 0.95, td / "tau06.json")

        print("4. the draw (s4): the excluded patient, three-body frames and the render never drawn")
        unb = td / "UNBLINDING_dual.json"
        res = score(recs, strata, arm="dual", taus=[str(td / "tau06.json")], pool="real", unblinding_path=str(unb))
        # expected draw, written out separately from draw_scored_frames: sorted keys, each drawing once
        elig = defaultdict(list)
        for r in recs:
            k = r["person"]
            if k == "carmlspine:case042" or not r["real"] or r["stem"].endswith("_z3"):
                continue
            elig[k].append(r["stem"])
        rng = np.random.default_rng(20260923)
        want = {}
        for k in sorted(elig):
            s = sorted(elig[k])
            want[k] = s[int(rng.integers(len(s)))]
        check("draw equals the hand-built s4 draw", res["draw"], want)
        check("no three-body frame drawn", any(v.endswith("_z3") for v in res["draw"].values()), False)
        check("excluded patient absent", "carmlspine:case042" in res["draw"], False)
        check("persons scored (23 in the real pool, the three-L6 patient out)", res["persons_scored"], 23)

        print("5. M1 known answers: pooled L6 x9, both x1, sacralised_L5 x2, four_lumbar x1")
        m = res["M1"]
        check("pooled n", m["pooled"]["n"], 13)
        check("'both' is in the M1 population", "both" in m["population"], True)
        check("COUPLED right 10 (L6 a-f, L6h, BOTHa, SL5 a-b)", m["pooled"]["coupled"]["k"], 10)
        check("COUNT right 2 (L6g, L6h)", m["pooled"]["count"]["k"], 2)
        check("MORPHOLOGY right 3 (L6g, L6h, FLa unanchored)", m["pooled"]["morphology"]["k"], 3)
        check("discordant b = 9", m["pooled"]["discordant"]["coupled_right_count_wrong"], 9)
        check("discordant c = 1", m["pooled"]["discordant"]["count_right_coupled_wrong"], 1)
        check("tested (10 >= 6)", m["test"]["tested"], True)
        check("P = 11/1024", m["test"]["P"], round(11 / 1024, 6))
        check("rejected at 0.025", m["test"]["rejected"], True)
        check("L6 stratum, descriptive: b=6 c=1 P=8/128", m["by_stratum_descriptive"]["L6"]["mcnemar_one_sided_P"],
              round(8 / 128, 6))
        check("both stratum, descriptive: coupled 1/1, count 0/1", (m["by_stratum_descriptive"]["both"]["coupled"]["k"],
                                                                   m["by_stratum_descriptive"]["both"]["count"]["k"]), (1, 0))
        check("T13 descriptive, coupled 1/2", m["by_stratum_descriptive"]["T13"]["coupled"]["k"], 1)
        check("T13 is NOT in the M1 population", m["pooled"]["n"] == sum(
            1 for p in res["persons"] if p["stratum"] in ("L6", "both", "sacralised_L5", "four_lumbar")), True)
        check("missed body (L6i): every arm wrong",
              [p["correct"] for p in res["persons"] if p["person"] == "ctsp:L6i"][0],
              {"count": False, "morphology": False, "coupled": False})
        check("no abstention in this study: the fig6 rule agrees with s4",
              m["pooled_fig6_rule_beside"]["coupled"]["k"], m["pooled"]["coupled"]["k"])

        print("6. F1 known answers at tau = 0.6: 16 transitional, 6 ordinary")
        f = res["F1"]
        check("a OR b sensitivity 12/16", f["a_or_b"]["sensitivity"]["k"], 12)
        check("a OR b specificity 5/6 (Oe: count and morphology disagree)", f["a_or_b"]["specificity"]["k"], 5)
        blk = f["a_or_b_or_c@tau0.95"]
        check("a OR b OR c sensitivity 14/16 (+L6h 0.9, +VNUa 0.95)", blk["sensitivity"]["k"], 14)
        check("a OR b OR c specificity 4/6 (+Of 0.65)", blk["specificity"]["k"], 4)
        check("c alone 9/16", f["c_alone@tau0.95"]["sensitivity"]["k"], 9)
        check("per subtype: sacralised_L5_fused 3/3 with c", blk["sensitivity_by_subtype"]["sacralised_L5_fused"]["k"], 3)
        check("per subtype: four_lumbar 0/1 (unanchored, p 0.2)", blk["sensitivity_by_subtype"]["four_lumbar"]["k"], 0)
        check("per subtype: T13 1/2", blk["sensitivity_by_subtype"]["T13"]["k"], 1)
        check("per subtype: both 1/1 (flag a)", blk["sensitivity_by_subtype"]["both"]["k"], 1)
        w = wilson(14, 16)
        check("sensitivity interval = Wilson(14, 16)", blk["sensitivity"]["wilson95"], w)
        check("sensitivity lower bound at 14/16 below 0.85", blk["sensitivity"]["wilson95"][0] < 0.85, True)
        check("target (lower bound >= 0.85) not met at 14/16", blk["target_met"], False)
        check("unreadable person reported as other, flagged 1/1",
              blk["other_flag_rate_by_stratum"]["unreadable"]["k"], 1)
        check("transitional unanchored counted (FLa)", blk["transitional_unanchored"], 1)
        check("tau fixed before unblinding -> pre-specified", blk["pre_specified"], True)
        check("unblinding record created", res["unblinding"]["created_now"] and unb.exists(), True)
        check("unblinding record carries git HEAD", bool(res["unblinding"]["record"]["git"]["head"]), True)

        print("7. unblinding is written once; a tau fixed after it, or altered, is not pre-specified")
        res2 = score(recs, strata, arm="dual", taus=[str(td / "tau06.json")], unblinding_path=str(unb))
        check("existing record read, not rewritten", res2["unblinding"]["created_now"], False)
        check("same unblinding time", res2["unblinding"]["record"]["unblinded_utc"],
              res["unblinding"]["record"]["unblinded_utc"])
        write_tau(td / "val06.json", 0.95, td / "tau_late.json")
        res3 = score(recs, strata, arm="dual", taus=[str(td / "tau_late.json")], unblinding_path=str(unb))
        check("tau fixed after unblinding -> not pre-specified", res3["tau"][0]["pre_specified"], False)
        raw = open(td / "tau06.json").read().replace('"arm": "D1"', '"arm": "Dx"')
        open(td / "tau06.json", "w").write(raw)
        res4 = score(recs, strata, arm="dual", taus=[str(td / "tau06.json")], unblinding_path=str(unb))
        check("altered tau file (sha256 mismatch) -> not pre-specified", res4["tau"][0]["pre_specified"], False)
        try:
            score(recs, strata, arm="primary", taus=[str(td / "tau95.json")], unblinding_path=str(unb))
            check("primary arm refuses a tau (c is the dual arm's rule)", False, True)
        except SystemExit:
            check("primary arm refuses a tau (c is the dual arm's rule)", True, True)
        try:
            score(recs, strata, arm="primary", unblinding_path=None)
            check("blinded outputs without an unblinding record are refused", False, True)
        except SystemExit:
            check("blinded outputs without an unblinding record are refused", True, True)

        print("8. cross-check against the primary scorer's output (its rule: abstentions not scored)")
        per_person = {p["person"]: {"correct": {"coupled": p["correct_fig6_rule"]["coupled"]}} for p in res["persons"]}
        fake = {"draws": {"primary_real": dict(res["draw"]), "T1_renders": {}},
                "results": {"T2|open|det74": {"per_person": per_person}}}
        json.dump(fake, open(td / "f6.json", "w"))
        r5 = score(recs, strata, arm="primary", unblinding_path=str(unb), fig6_score_path=str(td / "f6.json"),
                   fig6_key="T2|open|det74")
        check("identical draw and COUPLED outcome -> 0 mismatches",
              (r5["fig6_crosscheck"]["n_draw_mismatches"], r5["fig6_crosscheck"]["n_coupled_mismatches"]), (0, 0))
        fake["draws"]["primary_real"]["ctsp:L6a"] = "somewhere_else"
        fake["results"]["T2|open|det74"]["per_person"]["ctsp:L6g"]["correct"]["coupled"] = True
        json.dump(fake, open(td / "f6.json", "w"))
        r6 = score(recs, strata, arm="primary", unblinding_path=str(unb), fig6_score_path=str(td / "f6.json"),
                   fig6_key="T2|open|det74")
        check("one moved draw and one flipped outcome are both caught",
              (r6["fig6_crosscheck"]["n_draw_mismatches"], r6["fig6_crosscheck"]["n_coupled_mismatches"]), (1, 1))

        print("9. a scored frame with no model output is wrong, unflagged and reported")
        recs_np = [dict(r, pred=None) if r["person"] == "ctsp:L6h" else r for r in recs]
        r7 = score(recs_np, strata, arm="dual", taus=[str(td / "tau95.json")], unblinding_path=str(unb))
        check("incomplete flagged", (r7["incomplete"], r7["n_scored_frames_without_prediction"]), (True, 1))
        check("COUPLED pooled falls to 9", r7["M1"]["pooled"]["coupled"]["k"], 9)

        print("10. six discordant persons all favouring COUPLED reject; five are descriptive")
        few = [r for r in recs if not r["person"].startswith(("verse:SL5", "ctsp:L6g", "ctsp:L6f", "verse:BOTH"))]
        r8 = score(few, strata, arm="primary", unblinding_path=str(unb))
        check("5 discordant -> descriptive", (r8["M1"]["test"]["discordant"], r8["M1"]["test"]["tested"]), (5, False))
        few6 = [r for r in recs if not r["person"].startswith(("verse:SL5b", "ctsp:L6g", "ctsp:L6f", "verse:BOTH"))]
        r9 = score(few6, strata, arm="primary", unblinding_path=str(unb))
        check("6 discordant, 6-0 -> P = 1/64, rejected", (r9["M1"]["test"]["P"], r9["M1"]["test"]["rejected"]),
              (round(1 / 64, 6), True))

        print("11. adapt: the REAL coupler (tools/alphabet_couple.couple_frame) -> couple_all.json -> dumps -> score")
        import alphabet_couple as AC
        from make_context_crops import LEVEL_ORDER
        sets, runs = td / "sets", td / "runs"

        def proto(names_true, called):
            """A prototype record: bodies stacked above the sacrum, posteriors peaked on `called` (the classifier's
            name), with 0.4 left on the true name where the two differ."""
            vert, boxes = [], []
            for i, (nt, nc) in enumerate(zip(names_true, called)):
                b = [100.0, 100.0 * i, 200.0, 100.0 * i + 80.0]
                v = AC._peaked(LEVEL_ORDER, nc, 0.9) if nt == nc else AC._peaked(LEVEL_ORDER, nc, 0.55, nt, 0.4)
                vert.append({"box": b, "posterior": [float(x) for x in v], "level": nc, "abstain": False})
                boxes.append(b)
            sac = [90.0, 100.0 * len(names_true), 210.0, 100.0 * len(names_true) + 100.0]
            meta = {"case": "x", "boxes": [{"cls": 0, "box": b, "level": nt} for b, nt in zip(boxes, names_true)]
                    + [{"cls": 1, "box": sac, "level": "sacrum"}]}
            return {"image": "x.png", "vertebrae": vert}, sac + [0.9], meta

        st2 = {"default": {"stratum": "ordinary", "alphabet": OA, "gate": "open"},
               "strata": {"ctsp:A6": {"stratum": "L6", "subtype": "L6", "alphabet": L6, "side": "test",
                                      "gate": "blinded"}}}
        frames_def = {("ctsp:A6", "blinded", "T2__A6_0"): (t6, ["L3", "L4", "L5", "L5"]),
                      ("ctsp:B0", "open", "T2__B0_0"): (to, to)}
        persons_json, couple_out = {}, defaultdict(list)
        for (k, gate, stem), (tn, cn) in frames_def.items():
            rec, sac, meta = proto(tn, cn)
            rec["image"] = f"{stem}.png"
            (sets / "T2" / gate / "meta").mkdir(parents=True, exist_ok=True)
            json.dump(meta, open(sets / "T2" / gate / "meta" / f"{stem}.json", "w"))
            persons_json.setdefault(k, {"frames": {"open": [], "blinded": []}})["frames"][gate].append(stem)
            couple_out[gate].append(AC.couple_frame(rec, sac, LEVEL_ORDER, meta=meta, which="std",
                                                    sacrum_min_conf=0.74))
        json.dump(persons_json, open(sets / "T2" / "persons.json", "w"))
        # the blinded prototype run wrote its prototype_meta.json at a known earlier time
        proto_dir = td / "proto_blinded"
        proto_dir.mkdir()
        (proto_dir / "prototype_meta.json").write_text("{}")
        t_run = datetime.datetime(2026, 9, 24, 1, 2, 3, tzinfo=datetime.timezone.utc).timestamp()
        os.utime(proto_dir / "prototype_meta.json", (t_run, t_run))
        for gate, fr in couple_out.items():
            (runs / "T2" / gate / "det74" / "couple").mkdir(parents=True, exist_ok=True)
            json.dump({"args": {"pred": str(proto_dir) if gate == "blinded" else str(td / "absent")}, "frames": fr},
                      open(runs / "T2" / gate / "det74" / "couple" / "couple_all.json", "w"))
        json.dump({"T2__A6_0": 0.81}, open(td / "sp.json", "w"))
        cmd_adapt(argparse.Namespace(sets=str(sets), runs=str(runs), variant="det74", set_names="T2",
                                     spine_probs=str(td / "sp.json"), out=str(td / "dumps.jsonl")))
        dumps = {r["stem"]: r for r in load_dumps(td / "dumps.jsonl")}
        check("adapt stamps the blinded frame with the prototype run's time",
              (dumps["T2__A6_0"]["pred_written_utc"], Path(dumps["T2__A6_0"]["pred_written_from"]).name),
              ("2026-09-24T01:02:03.000000Z", "prototype_meta.json"))
        check("an unreachable prototype dir falls back to couple_all.json",
              Path(dumps["T2__B0_0"]["pred_written_from"]).name, "couple_all.json")
        r10 = score(list(dumps.values()), st2, arm="dual", taus=[str(td / "tau95.json")],
                    unblinding_path=str(td / "U2.json"))
        check("the new unblinding record takes the earlier model run, not the scoring time",
              r10["unblinding"]["record"]["unblinded_utc"], "2026-09-24T01:02:03.000000Z")
        cf = {f["stem"]: f for fr in couple_out.values() for f in fr}
        pa = {p["person"]: p for p in r10["persons"]}
        check("the coupler calls the L6 frame L6", cf["T2__A6_0"]["call"], "L6")
        check("COUPLED here == the coupler's frame_all_correct_coupled", pa["ctsp:A6"]["correct"]["coupled"],
              cf["T2__A6_0"]["frame_all_correct_coupled"])
        check("COUNT here == (the coupler's count_correct == n_truth_named)", pa["ctsp:A6"]["correct"]["count"],
              cf["T2__A6_0"]["count_correct"] == cf["T2__A6_0"]["n_truth_named"])
        check("MORPHOLOGY here == the coupler's frame_all_correct_classifier", pa["ctsp:A6"]["correct"]["morphology"],
              cf["T2__A6_0"]["frame_all_correct_classifier"])
        check("L6 frame: coupled right, count wrong, morphology wrong", pa["ctsp:A6"]["correct"],
              {"count": False, "morphology": False, "coupled": True})
        check("L6 frame: flags a and b; spine probability carried through adapt",
              (pa["ctsp:A6"]["flag"]["a"], pa["ctsp:A6"]["flag"]["b"], pa["ctsp:A6"]["spine_prob"]), (True, True, 0.81))
        check("ordinary frame: every arm right, no flag",
              (pa["ctsp:B0"]["correct"], pa["ctsp:B0"]["flag"]["a"], pa["ctsp:B0"]["flag"]["b"]),
              ({"count": True, "morphology": True, "coupled": True}, False, False))

        print("12. s4 abstention: an abstained reference-named body is not correct for SchwingNet's arms")
        st3 = {"default": {"stratum": "ordinary", "alphabet": OA, "gate": "open"}, "strata": {}}
        for k in ("ctsp:X1", "ctsp:X2", "ctsp:X3"):
            put(k, "L6", "L6", L6, into=st3)
        ab = [_frame("X1_f0", "ctsp:X1", t6, shifted6, t6, t6, "L6", gate="blinded", abstain=(3,)),
              _frame("X2_f0", "ctsp:X2", t6, shifted6, t6, t6, "L6", gate="blinded"),
              _frame("X3_f0", "ctsp:X3", t6, t6, t6, shifted6, "L6", gate="blinded", abstain=(0,))]
        # X2's abstention sits on an extra detected box that matches no truth body: it is not a scored body
        ab[1]["pred"]["bodies"].append({"box": [500.0, 900.0, 600.0, 980.0], "count": "L1", "morphology": "L1",
                                        "coupled": "L1", "abstain": True})
        r11 = score(ab, st3, arm="primary", unblinding_path=str(td / "U3.json"))
        px = {p["person"]: p for p in r11["persons"]}
        check("X1 (abstains on its L6 body), s4: every arm wrong", px["ctsp:X1"]["correct"],
              {"count": False, "morphology": False, "coupled": False})
        check("X1, fig6 rule beside: morphology and coupled right", px["ctsp:X1"]["correct_fig6_rule"],
              {"count": False, "morphology": True, "coupled": True})
        check("X2 (abstains only on an unmatched box): coupled right under s4", px["ctsp:X2"]["correct"]["coupled"], True)
        check("X3 (abstains, count right): COUNT is not an abstaining arm", px["ctsp:X3"]["correct"]["count"], True)
        check("M1 pooled coupled: s4 1/3, fig6 rule 2/3",
              (r11["M1"]["pooled"]["coupled"]["k"], r11["M1"]["pooled_fig6_rule_beside"]["coupled"]["k"]), (1, 2))
        check("persons with an abstained scored body: X1, X3",
              r11["M1"]["pooled"]["persons_with_an_abstained_scored_body"], 2)

        print("13. unblinding is the EARLIER of the first blinded model output and the scoring (s9)")
        T0 = "2026-09-20T00:00:00.000000Z"
        stamped = []
        for r in recs:
            r2 = dict(r)
            if r2.get("pred") is not None:
                r2["pred_written_utc"] = ("2020-01-01T00:00:00.000000Z" if r2["person"] == "carmlspine:case042"
                                          else T0 if r2["gate"] != "open" else "2019-01-01T00:00:00.000000Z")
            stamped.append(r2)
        # a blinded person's RENDER output, earlier still: s9 counts any frame of the person, not only real ones
        rend = _frame("render_L6a", "ctsp:L6a", t6, shifted6, t6, t6, "L6", real=False, gate="blinded",
                      written="2026-09-19T00:00:00.000000Z")
        r12 = score(stamped + [rend], strata, arm="dual", taus=[str(td / "tau95.json")],
                    unblinding_path=str(td / "U4.json"))
        check("new record: unblinded_utc = the earliest blinded output (the render), not the scoring time",
              r12["unblinding"]["record"]["unblinded_utc"], "2026-09-19T00:00:00.000000Z")
        check("the three excluded L6 patients (2020) and the open persons (2019) do not set it",
              r12["unblinding"]["first_blinded_model_output_in_dumps_utc"], "2026-09-19T00:00:00.000000Z")
        check("a tau fixed today, after that output -> not pre-specified", r12["tau"][0]["pre_specified"], False)
        r13 = score(stamped, strata, arm="dual", taus=[str(td / "tau95.json")], unblinding_path=str(unb))
        check("existing record, but a dump output precedes it -> the earlier time governs",
              (r13["unblinding"]["a_dump_output_precedes_the_record"], r13["unblinding"]["effective_unblinded_utc"]),
              (True, T0))
        check("... and the tau fixed between the two is no longer pre-specified", r13["tau"][0]["pre_specified"], False)
        # a model run strictly between the tau fixing and this scoring (the midpoint: no assumption about how fast
        # this machine runs the sections above)
        fixed = parse_utc(json.load(open(td / "tau95.json"))["fixed_utc"])
        mid = fixed + (parse_utc(now_utc()) - fixed) / 2
        after = mid.isoformat(timespec="microseconds").replace("+00:00", "Z")
        late = [dict(r, pred_written_utc=after) if r.get("pred") is not None and r["gate"] != "open" else r
                for r in recs]
        r14 = score(late, strata, arm="dual", taus=[str(td / "tau95.json")], unblinding_path=str(td / "U5.json"))
        check("model run after tau was fixed (and before this scoring) -> it sets unblinding; tau pre-specified",
              (r14["unblinding"]["record"]["unblinded_utc"], r14["tau"][0]["pre_specified"], mid > fixed),
              (after, True, True))

        print("14. --subset: M1 and F1 on a named subset, the whole-pool draw unchanged")
        six = {f"ctsp:L6{c}" for c in "abcdef"}
        (td / "six.json").write_text(json.dumps(sorted(six)))
        r15 = score(recs, strata, arm="dual", taus=[str(td / "tau06.json")], unblinding_path=str(unb),
                    subsets={"six": load_subset(td / "six.json")})
        s6 = r15["subsets"]["six"]
        check("the draw is the whole pool's (all 23 persons, same frames)", (len(r15["draw"]), r15["draw"] == res["draw"]),
              (23, True))
        check("subset M1: n 6, coupled 6, count 0, P = 1/64, rejected",
              (s6["M1"]["pooled"]["n"], s6["M1"]["pooled"]["coupled"]["k"], s6["M1"]["pooled"]["count"]["k"],
               s6["M1"]["test"]["P"], s6["M1"]["test"]["rejected"]), (6, 6, 0, round(1 / 64, 6), True))
        check("subset F1 a OR b: 6/6 (flag a on every one)", s6["F1"]["a_or_b"]["sensitivity"]["k"], 6)
        check("the whole-pool M1 is unchanged by the subset", r15["M1"]["pooled"]["coupled"]["k"], 10)
        (td / "six.txt").write_text("# one key per line\n" + "\n".join(sorted(six)) + "\n")
        check("a text subset file reads the same", load_subset(td / "six.txt"), six)

    n_ok = sum(ok)
    print(f"\nSELF-TEST {'PASSED' if all(ok) else 'FAILED'}: {n_ok}/{len(ok)} checks")
    return 0 if all(ok) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("adapt", help="Figure 6 couple outputs + sets -> one dump per frame (JSONL)")
    p.add_argument("--sets", required=True)
    p.add_argument("--runs", required=True, help="eval root: <set>/<gate>/<variant>/couple/couple_all.json")
    p.add_argument("--variant", default="det74", help="det74 is the s4 primary (detector confidence 0.74)")
    p.add_argument("--set-names", default="T1,T2,T3")
    p.add_argument("--spine-probs", default=None, help="{stem: spine probability} from the dual-loss arm")
    p.add_argument("--out", required=True)
    p = sub.add_parser("fix-tau", help="tau on the G3 validation persons only; written once with its sha256")
    p.add_argument("--val", required=True, help="val_spine_<tag>.json from tools/head_dual.py")
    p.add_argument("--target", type=float, required=True, help="0.95 (s12) or 0.97 (s13 F1b)")
    p.add_argument("--out", required=True)
    p.add_argument("--arm", default="D1")
    p.add_argument("--repo", default=str(REPO))
    p = sub.add_parser("score", help="M1 and F1 per s12")
    p.add_argument("--dumps", required=True)
    p.add_argument("--strata", required=True, help="the frozen strata.json (fig6_freeze.py)")
    p.add_argument("--arm", default="primary", choices=["primary", "dual"])
    p.add_argument("--tau", action="append", default=[], help="a fix-tau file (dual arm only); repeat per operating point")
    p.add_argument("--pool", default="real", choices=["real", "renders"])
    p.add_argument("--unblinding-record", default=None)
    p.add_argument("--repo", default=str(REPO), help="the clone whose HEAD is recorded (the grid clone cannot pull)")
    p.add_argument("--fig6-score", default=None, help="fig6_score.py output: draw and COUPLED checked person by person")
    p.add_argument("--fig6-key", default=None, help="its results key, e.g. 'T2|blinded|det74'")
    p.add_argument("--subset", action="append", default=[], metavar="NAME=FILE",
                   help="also report M1 and F1 on this person subset (s14: e.g. the unanimous automated reference)")
    p.add_argument("--out", required=True)
    sub.add_parser("self-test")
    a = ap.parse_args()
    if a.cmd == "adapt":
        return cmd_adapt(a)
    if a.cmd == "fix-tau":
        return cmd_fix_tau(a)
    if a.cmd == "score":
        return cmd_score(a)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
