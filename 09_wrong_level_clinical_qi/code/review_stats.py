# Copied 2026-10-08 into spine-program/09_wrong_level_clinical_qi/code/ from spinesurg-ct-nnunet
# (private, branch L6_Class, commit 097933a) tools/review_stats.py; last commit 3d91ecd 2026-09-15. The repository is the
# source of truth; this copy is a record. Its default paths (~/review, ~/FluoroCap_lstv, ~/FluoroCap_s2)
# are the laptop's WSL home, not the grid: see MANIFEST_GRID.md and TODO.md step 0.
"""Statistics over the charted scoping-review data: what the sources actually show.

Six questions, each answered with a named test, an effect size with an interval, and the n the answer
rests on. Every charted field carries an explicit / inferred / absent flag, and every test is run twice:
on the explicit subset, which is the primary analysis, and on explicit-plus-inferred, which is the
sensitivity analysis and is never reported as the result.

    python tools/review_stats.py --out ~/review

Writes REVIEW_STATS.md and REVIEW_STATS.json.

Nothing here has passed human charting. Every p-value describes what the patterns extracted from the
text, not what the literature says; the two are the same thing only to the extent that the validation
sample, which is still unread, says they are.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_patterns import (  # noqa: E402
    COUNTERMEASURE_CLASS,
    MECHANISM_CLASS,
    RX_PREV,
    ascertainment_of,
    evaluation_status,
    sentences,
)
from review_screen import load_text_index, read_jsonl  # noqa: E402

STRATA = [("explicit", "primary"), ("any", "sensitivity")]


# ------------------------------------------------------------------ estimators

def wilson(k, n, z=1.959963985):
    """Wilson score interval: behaves at 0 and at n, which a Wald interval does not."""
    if n == 0:
        return None, None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def fmt_ci(p, lo, hi, pct=True):
    if p is None:
        return "-"
    if pct:
        return "%.1f%% (95%% CI %.1f to %.1f)" % (100 * p, 100 * lo, 100 * hi)
    return "%.3g (95%% CI %.3g to %.3g)" % (p, lo, hi)


def two_by_two(a, b, c, d):
    """Fisher exact throughout: the cell counts in the primary stratum are small enough that the
    chi-square approximation would not hold, and using one test in both strata keeps them comparable.
    The odds-ratio interval uses the Haldane-Anscombe correction (add 0.5 to every cell), which is
    what makes it defined when a cell is zero."""
    table = [[a, b], [c, d]]
    try:
        orr, p = stats.fisher_exact(table)
    except Exception:
        orr, p = float("nan"), float("nan")
    a_, b_, c_, d_ = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    log_or = math.log((a_ * d_) / (b_ * c_))
    se = math.sqrt(1 / a_ + 1 / b_ + 1 / c_ + 1 / d_)
    lo, hi = math.exp(log_or - 1.959963985 * se), math.exp(log_or + 1.959963985 * se)
    chi2 = chi2_p = None
    if min(a, b, c, d) >= 5:
        chi2, chi2_p, _, _ = stats.chi2_contingency(table, correction=False)
    return {"table": table, "n": a + b + c + d,
            "odds_ratio": None if not np.isfinite(orr) else round(float(orr), 4),
            "odds_ratio_haldane": round(math.exp(log_or), 4),
            "ci_low": round(lo, 4), "ci_high": round(hi, 4),
            "fisher_p": None if not np.isfinite(p) else float(p),
            "chi2": None if chi2 is None else round(float(chi2), 4),
            "chi2_p": None if chi2_p is None else float(chi2_p),
            "test": "Fisher exact (two-sided)" + ("; chi-square also reported" if chi2 is not None else
                                                  "; chi-square not used, a cell is under 5")}


def cochran_armitage(scores, k, n):
    """Trend in a proportion across ordered groups. scores are the group scores (years here)."""
    scores, k, n = np.asarray(scores, float), np.asarray(k, float), np.asarray(n, float)
    N = n.sum()
    if N == 0 or k.sum() == 0 or k.sum() == N:
        return None, None
    pbar = k.sum() / N
    sbar = (n * scores).sum() / N
    num = (k * (scores - sbar)).sum()
    var = pbar * (1 - pbar) * (n * (scores - sbar) ** 2).sum()
    if var <= 0:
        return None, None
    z = num / math.sqrt(var)
    return float(z), float(2 * stats.norm.sf(abs(z)))


# ------------------------------------------------------------------ data

def load(out):
    ex = list(read_jsonl(os.path.join(out, "extraction.jsonl")))
    rates = list(csv.DictReader(open(os.path.join(out, "incidence_reported.csv"), encoding="utf-8")))
    return ex, rates


def items(rec, field, stratum):
    if stratum == "explicit":
        return [i for i in rec[field] if i["confidence"] == "explicit"]
    return list(rec[field])


def flag(rec, field, stratum):
    c = rec[field]["confidence"]
    return c == "explicit" if stratum == "explicit" else c in ("explicit", "inferred")


def classes(rec, field, stratum, mapping):
    return {mapping.get(i["item"]) for i in items(rec, field, stratum)} - {None}


def wrong_level_sources(ex, stratum):
    """Sources that discuss a wrong-level event. In the explicit stratum this is exact: an item is
    flagged explicit only when it was matched in a sentence that also named a wrong-level event."""
    out = []
    for r in ex:
        if stratum == "explicit":
            hit = (any(i["confidence"] == "explicit" for i in r["mechanisms"])
                   or any(i["confidence"] == "explicit" for i in r["countermeasures"])
                   or r["incidence_verbatim"]["confidence"] == "explicit"
                   or r["transitional_implicated"]["confidence"] == "explicit")
        else:
            hit = bool(r["mechanisms"] or r["countermeasures"]
                       or r["incidence_verbatim"]["value"] is not None
                       or r["transitional_implicated"]["value"])
        if hit:
            out.append(r)
    return out


# ------------------------------------------------------------------ 1. the central claim

def q1_alignment(ex, stratum):
    pop = [r for r in ex if classes(r, "countermeasures", stratum, COUNTERMEASURE_CLASS)]
    a = b = c = d = 0
    for r in pop:
        mech = classes(r, "mechanisms", stratum, MECHANISM_CLASS)
        ctr = classes(r, "countermeasures", stratum, COUNTERMEASURE_CLASS)
        imech = "anatomical or radiological" in mech
        ictr = "radiological" in ctr
        if imech and ictr:
            a += 1
        elif imech and not ictr:
            b += 1
        elif not imech and ictr:
            c += 1
        else:
            d += 1
    res = two_by_two(a, b, c, d)
    res["population"] = "sources naming at least one countermeasure"
    res["exposure"] = "names an anatomical or radiological mechanism"
    res["outcome"] = "names a radiological countermeasure"
    res["cells"] = {"mech+/ctr_rad+": a, "mech+/ctr_rad-": b, "mech-/ctr_rad+": c, "mech-/ctr_rad-": d}
    p1, l1, h1 = wilson(a, a + b)
    p0, l0, h0 = wilson(c, c + d)
    res["risk_exposed"] = {"k": a, "n": a + b, "p": p1, "lo": l1, "hi": h1}
    res["risk_unexposed"] = {"k": c, "n": c + d, "p": p0, "lo": l0, "hi": h0}
    res["risk_difference"] = None if (p1 is None or p0 is None) else round(p1 - p0, 4)
    # the same sources, counted the other way: what kind of countermeasure gets named at all
    res["countermeasure_class_counts"] = dict(Counter(
        cls for r in pop for cls in classes(r, "countermeasures", stratum, COUNTERMEASURE_CLASS)))
    res["mechanism_class_counts"] = dict(Counter(
        cls for r in ex for cls in classes(r, "mechanisms", stratum, MECHANISM_CLASS)))
    return res


# ------------------------------------------------------------------ 2. evaluation status

STATUS_ORDER = ["evaluated against an outcome", "evaluated against confidence or perception",
                "proposed only", "not stated"]


def q2_evaluation(ex, stratum, sents_by_id=None):
    """Evaluation status read over every sentence in the record that mentions that countermeasure.

    Reading it from the single sentence that first named the countermeasure puts 90 per cent of
    mentions in "not stated", because a paper names a technique in its methods and evaluates it in its
    results. The status is therefore the strongest one found in any sentence of that record that
    mentions the countermeasure, and the sentence that gave it is kept.
    """
    per = defaultdict(Counter)
    evidence = defaultdict(list)
    for r in ex:
        pool = (sents_by_id or {}).get(r["record_id"])
        for i in items(r, "countermeasures", stratum):
            name = i["item"]
            cands = []
            if pool:
                rx = RX_PREV[name]
                cands = [s for s in pool if rx.search(s)]
            if not cands:
                cands = [i["quote"] or ""]
            best, best_sent = "not stated", None
            for s in cands:
                st = evaluation_status(s)
                if STATUS_ORDER.index(st) < STATUS_ORDER.index(best):
                    best, best_sent = st, s
            per[name][best] += 1
            if best != "not stated" and len(evidence[(name, best)]) < 3:
                evidence[(name, best)].append({"record_id": r["record_id"], "sentence": (best_sent or "")[:300]})
    rows = []
    for name, c in per.items():
        n = sum(c.values())
        k = c["evaluated against an outcome"]
        p, lo, hi = wilson(k, n)
        rows.append({"countermeasure": name, "class": COUNTERMEASURE_CLASS.get(name, ""),
                     "n_named": n,
                     "evaluated_against_an_outcome": k,
                     "evaluated_against_confidence": c["evaluated against confidence or perception"],
                     "proposed_only": c["proposed only"], "not_stated": c["not stated"],
                     "p_outcome": p, "ci_low": lo, "ci_high": hi,
                     "examples": evidence.get((name, "evaluated against an outcome"), [])})
    rows.sort(key=lambda d: -d["n_named"])
    res = {"rows": rows, "n_countermeasure_mentions": sum(r["n_named"] for r in rows),
           "test": "Wilson score interval per countermeasure; Spearman rank correlation across "
                   "countermeasures between how often one is named and how often it is evaluated; "
                   "Fisher exact for the class contrast"}
    # The contrast the table makes visible: the countermeasures that act on the level-determination
    # step itself - count from a landmark, a marker, an intraoperative radiograph, a second reader -
    # against navigation, which is a technology with a trial literature, and against the organisational
    # countermeasure. This split is declared here rather than read off the result.
    LEVEL_STEP = {"count from a fixed landmark", "compare with the preoperative study",
                  "intraoperative radiograph with a marker", "implanted or skin marker",
                  "second reader or radiologist"}
    grp = {"level-determination countermeasures": Counter(), "navigation or computer assistance": Counter(),
           "organisational": Counter()}
    for r in rows:
        g = ("level-determination countermeasures" if r["countermeasure"] in LEVEL_STEP
             else "navigation or computer assistance" if r["countermeasure"] == "navigation or computer assistance"
             else "organisational")
        grp[g]["n"] += r["n_named"]
        grp[g]["k"] += r["evaluated_against_an_outcome"]
    res["by_group"] = []
    for g, c in grp.items():
        p, lo, hi = wilson(c["k"], c["n"])
        res["by_group"].append({"group": g, "k": c["k"], "n": c["n"], "p": p, "lo": lo, "hi": hi})
    a = grp["level-determination countermeasures"]
    b = Counter({"k": grp["navigation or computer assistance"]["k"] + grp["organisational"]["k"],
                 "n": grp["navigation or computer assistance"]["n"] + grp["organisational"]["n"]})
    res["level_step_vs_rest"] = two_by_two(a["k"], a["n"] - a["k"], b["k"], b["n"] - b["k"])
    res["level_step_vs_rest"]["contrast"] = ("countermeasures acting on the level-determination step, "
                                             "against navigation and the organisational countermeasure")
    if len(rows) >= 3:
        x = [r["n_named"] for r in rows]
        y = [r["p_outcome"] for r in rows]
        rho, p = stats.spearmanr(x, y)
        res["spearman_named_vs_evaluated"] = {
            "rho": None if not np.isfinite(rho) else round(float(rho), 4),
            "p": None if not np.isfinite(p) else float(p),
            "n_countermeasures": len(rows),
            "reading": "a negative rho is the claim that the most-named are the least-evaluated"}
    return res


# ------------------------------------------------------------------ 3. rate and ascertainment

def q3_rates(rates, ex, association=None):
    """association='adjacent' is the primary analysis: the rate sits within 40 characters of the
    wrong-level term it is attributed to. Widening to every anchored rate admits sentences where the
    nearest rate belongs to a different complication, and one where "100% preventable" is read as an
    incidence, so the wider set is the sensitivity analysis."""
    by_id = {r["record_id"]: r for r in ex}
    anchored = [r for r in rates if r["wrong_level_anchored"] == "yes"]
    if association:
        anchored = [r for r in anchored if r["event_association"] == association]
    norm = []
    for r in anchored:
        if not r["rate_per_10000"]:
            continue
        try:
            v = float(r["rate_per_10000"])
        except ValueError:
            continue
        if v <= 0:
            continue  # a zero rate has no logarithm; counted and reported separately
        rec = by_id.get(r["record_id"])
        norm.append({"record_id": r["record_id"], "rate": v, "log10": math.log10(v),
                     "denominator_nature": r["rate_denominator_nature"] or "(not stated)",
                     "design": r["design"] or "(not stated)",
                     "ascertainment": ascertainment_of(r["design"]),
                     "association": r["event_association"],
                     "denominator_n": (rec or {}).get("denominator", {}).get("n"),
                     "as_reported": r["rate_as_reported"], "quote": r["quote"][:300]})
    res = {"n_anchored": len(anchored),
           "n_normalisable": sum(1 for r in anchored if r["rate_per_10000"]),
           "n_positive_for_log": len(norm),
           "n_zero_rates_excluded_from_log": sum(
               1 for r in anchored if r["rate_per_10000"] and float(r["rate_per_10000"]) == 0)}
    if norm:
        v = sorted(x["rate"] for x in norm)
        res["overall"] = {"median": float(np.median(v)), "min": v[0], "max": v[-1],
                          "iqr_low": float(np.percentile(v, 25)), "iqr_high": float(np.percentile(v, 75)),
                          "orders_of_magnitude": round(math.log10(v[-1] / v[0]), 2) if v[0] > 0 else None}

    def group(key):
        g = defaultdict(list)
        for x in norm:
            g[x[key]].append(x)
        out, arrays, labels = [], [], []
        for k, xs in sorted(g.items(), key=lambda kv: -len(kv[1])):
            vals = sorted(x["rate"] for x in xs)
            out.append({"group": k, "n": len(xs), "median": float(np.median(vals)),
                        "min": vals[0], "max": vals[-1]})
            if len(xs) >= 3:
                arrays.append([x["log10"] for x in xs])
                labels.append(k)
        r = {"groups": out, "groups_tested": labels,
             "test": "Kruskal-Wallis on log10(rate per 10,000); groups with fewer than three "
                     "sources are described but not tested"}
        if len(arrays) >= 2:
            h, p = stats.kruskal(*arrays)
            r["H"] = round(float(h), 4)
            r["p"] = float(p)
            r["df"] = len(arrays) - 1
            # epsilon-squared, the rank effect size for Kruskal-Wallis
            n = sum(len(x) for x in arrays)
            # epsilon-squared goes below zero when H is smaller than its degrees of freedom, which means
            # the groups separate less than chance would; it is reported as zero and the raw H is above.
            eps = (h - len(arrays) + 1) / (n - len(arrays)) if n > len(arrays) else None
            r["epsilon_squared"] = None if eps is None else round(float(max(0.0, eps)), 4)
            r["epsilon_squared_uncorrected"] = None if eps is None else round(float(eps), 4)
            if len(arrays) == 2:
                u, pu = stats.mannwhitneyu(arrays[0], arrays[1], alternative="two-sided")
                n1, n2 = len(arrays[0]), len(arrays[1])
                r["mann_whitney_U"] = float(u)
                r["mann_whitney_p"] = float(pu)
                r["rank_biserial"] = round(float(1 - 2 * u / (n1 * n2)), 4)
        else:
            r["p"] = None
            r["note"] = "fewer than two groups reach three sources; no test was run"
        return r

    res["by_denominator_nature"] = group("denominator_nature")
    res["by_ascertainment"] = group("ascertainment")
    pairs = [(x["denominator_n"], x["rate"]) for x in norm
             if isinstance(x["denominator_n"], (int, float)) and x["denominator_n"]]
    res["rate_vs_denominator_size"] = {"n_pairs": len(pairs)}
    if len(pairs) >= 4:
        rho, p = stats.spearmanr([a for a, _ in pairs], [b for _, b in pairs])
        res["rate_vs_denominator_size"].update({
            "spearman_rho": round(float(rho), 4), "p": float(p),
            "test": "Spearman rank correlation between the stated denominator and the stated rate",
            "reading": "a negative rho is what ascertainment predicts: the larger the denominator, "
                       "the lower the rate"})
    else:
        res["rate_vs_denominator_size"]["note"] = (
            "fewer than four sources state both a denominator and a normalisable rate; "
            "no correlation was computed")
    res["rows"] = norm
    return res


# ------------------------------------------------------------------ 4. transitional anatomy

def q4_transitional(ex, stratum):
    pop = wrong_level_sources(ex, stratum)
    k = sum(1 for r in pop if flag(r, "transitional_implicated", stratum))
    p, lo, hi = wilson(k, len(pop))
    res = {"population": "sources discussing a wrong-level event", "n": len(pop), "k": k,
           "proportion": p, "ci_low": lo, "ci_high": hi,
           "test": "Wilson score interval; Fisher exact for the two contrasts"}

    def region_has(r, name):
        return any(i["item"] == name and (i["confidence"] == "explicit" or stratum == "any")
                   for i in r["spinal_region"])

    ls = [r for r in pop if region_has(r, "lumbar or lumbosacral") and not region_has(r, "thoracic")]
    th = [r for r in pop if region_has(r, "thoracic") and not region_has(r, "lumbar or lumbosacral")]
    a = sum(1 for r in ls if flag(r, "transitional_implicated", stratum))
    c = sum(1 for r in th if flag(r, "transitional_implicated", stratum))
    res["by_region"] = two_by_two(a, len(ls) - a, c, len(th) - c)
    res["by_region"].update({
        "contrast": "lumbosacral-only sources versus thoracic-only sources",
        "lumbosacral": {"k": a, "n": len(ls), **dict(zip(("p", "lo", "hi"), wilson(a, len(ls))))},
        "thoracic": {"k": c, "n": len(th), **dict(zip(("p", "lo", "hi"), wilson(c, len(th))))}})

    old = [r for r in pop if r["year"] and r["year"] < 2010]
    new = [r for r in pop if r["year"] and r["year"] >= 2010]
    a2 = sum(1 for r in new if flag(r, "transitional_implicated", stratum))
    c2 = sum(1 for r in old if flag(r, "transitional_implicated", stratum))
    res["by_era"] = two_by_two(a2, len(new) - a2, c2, len(old) - c2)
    res["by_era"].update({
        "contrast": "2010 and later versus before 2010",
        "from_2010": {"k": a2, "n": len(new), **dict(zip(("p", "lo", "hi"), wilson(a2, len(new))))},
        "before_2010": {"k": c2, "n": len(old), **dict(zip(("p", "lo", "hi"), wilson(c2, len(old))))}})
    return res


# ------------------------------------------------------------------ 5. time

def q5_time(ex, stratum, min_year=2000, max_year=2025):
    pop = [r for r in ex if r["year"] and min_year <= r["year"] <= max_year]
    years = sorted({r["year"] for r in pop})
    rows = []
    for y in years:
        sub = [r for r in pop if r["year"] == y]
        img = sum(1 for r in sub
                  if "radiological" in classes(r, "countermeasures", stratum, COUNTERMEASURE_CLASS))
        org = sum(1 for r in sub
                  if "organisational" in classes(r, "countermeasures", stratum, COUNTERMEASURE_CLASS))
        p, lo, hi = wilson(img, len(sub))
        rows.append({"year": y, "n_included": len(sub), "n_imaging_countermeasure": img,
                     "n_organisational_countermeasure": org,
                     "proportion_imaging": p, "ci_low": lo, "ci_high": hi})
    res = {"rows": rows, "n": len(pop), "window": [min_year, max_year],
           "measure": ("the proportion of that year's included sources naming an imaging "
                       "countermeasure, not the raw count: the corpus itself grows steeply with "
                       "year, so a count would measure the corpus and not the literature"),
           "test": "Cochran-Armitage trend test on the proportion across years, with year as the "
                   "score; Spearman rank correlation as a second look"}
    z, p = cochran_armitage([r["year"] for r in rows],
                            [r["n_imaging_countermeasure"] for r in rows],
                            [r["n_included"] for r in rows])
    res["trend_imaging_countermeasure"] = {"z": None if z is None else round(z, 4), "p": p}
    z2, p2 = cochran_armitage([r["year"] for r in rows],
                              [r["n_organisational_countermeasure"] for r in rows],
                              [r["n_included"] for r in rows])
    res["trend_organisational_countermeasure"] = {"z": None if z2 is None else round(z2, 4), "p": p2}
    ys = [r["year"] for r in rows if r["n_included"] >= 5]
    ps = [r["proportion_imaging"] for r in rows if r["n_included"] >= 5]
    if len(ys) >= 4:
        rho, pr = stats.spearmanr(ys, ps)
        res["spearman_year_vs_proportion"] = {"rho": round(float(rho), 4), "p": float(pr),
                                              "n_years_with_at_least_5_sources": len(ys)}
    res["raw_counts_for_reference"] = {str(r["year"]): r["n_included"] for r in rows}
    return res


# ------------------------------------------------------------------ report

def md_ci(d, key="proportion"):
    return fmt_ci(d.get(key), d.get("ci_low"), d.get("ci_high"))


def p_str(p):
    if p is None:
        return "-"
    if p < 0.001:
        return "< 0.001"
    return "%.3f" % p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.expanduser("~/review"))
    ap.add_argument("--lstv", default=os.path.expanduser("~/review/corpus_snapshot/lstv"))
    ap.add_argument("--s2", default=os.path.expanduser("~/review/corpus_snapshot/s2"))
    ap.add_argument("--abstracts", default=os.path.expanduser("~/review/abstracts.jsonl"))
    a = ap.parse_args()
    out = os.path.expanduser(a.out)
    ex, rates = load(out)

    # every sentence held for each included source, so evaluation status can be read where it is
    # written rather than only where the countermeasure was first named
    idx, _ = load_text_index(a.lstv, a.s2)
    if os.path.exists(a.abstracts):
        for r in read_jsonl(a.abstracts):
            if r.get("abstract"):
                idx[r["record_id"]].append(("abstract", "ABSTRACT", r["abstract"]))
    want = {r["record_id"] for r in ex}
    pmc = {r["pmcid"]: r["record_id"] for r in ex if r.get("pmcid")}
    sents_by_id = {}
    for key, tl in idx.items():
        rid = key if key in want else pmc.get(key.split(":", 1)[-1])
        if not rid or rid not in want:
            continue
        bag = sents_by_id.setdefault(rid, [])
        for _f, sec, t in tl:
            if str(sec or "").upper().startswith("REF"):
                continue
            bag.extend(sentences(t))
    print("sentence pools built for %d of %d included sources" % (len(sents_by_id), len(ex)), flush=True)

    # how many included sources rest on an abstract alone, read from the screening ledger
    n_no_fulltext = sum(1 for r in read_jsonl(os.path.join(out, "screening.jsonl"))
                        if r.get("record_type") == "record" and r.get("decision") == "include"
                        and not r.get("fulltext_retrieved"))

    R = {"n_included_sources": len(ex), "n_rate_rows": len(rates),
         "strata": {"primary": "explicit only", "sensitivity": "explicit plus inferred"},
         "mechanism_class_map": MECHANISM_CLASS, "countermeasure_class_map": COUNTERMEASURE_CLASS,
         "caveat": ("No part of this has passed human charting. Every p-value describes what the "
                    "patterns extracted from the text.")}
    for stratum, role in STRATA:
        R[role] = {
            "stratum": stratum,
            "q1_alignment": q1_alignment(ex, stratum),
            "q2_evaluation": q2_evaluation(ex, stratum, sents_by_id),
            "q4_transitional": q4_transitional(ex, stratum),
            "q5_time": q5_time(ex, stratum),
        }
    R["primary"]["q3_rates"] = q3_rates(rates, ex, association="adjacent")
    R["sensitivity"]["q3_rates"] = q3_rates(rates, ex, association=None)

    with open(os.path.join(out, "REVIEW_STATS.json"), "w", encoding="utf-8") as fh:
        json.dump(R, fh, indent=1, default=float)

    P, S = R["primary"], R["sensitivity"]
    L = ["# What the charted sources show", "",
         "**None of this has passed human charting. Every p-value below is provisional and describes "
         "what the named patterns extracted from the text, not what the literature says. The two are "
         "the same thing only to the degree the validation sample says they are, and that sample "
         "(`validation_sample.csv`, 200 rows) is still unread. No number here should be quoted as a "
         "finding about wrong-level surgery without reading the sources behind it.**", "",
         "Produced by `tools/review_stats.py` from `extraction.jsonl` (%d included sources) and "
         "`incidence_reported.csv` (%d rate rows). Every charted field carries an explicit / inferred / "
         "absent flag. **The primary analysis is the explicit subset**, where the pattern matched inside "
         "a sentence that also named a wrong-level event. The explicit-plus-inferred version is reported "
         "beside it as a sensitivity analysis and is never the result." % (len(ex), len(rates)), "",
         "---", "", "## 1. Is the prevention literature aimed at the failing step?", "",
         "Per source, whether it names an anatomical or radiological mechanism, against whether it names "
         "a radiological countermeasure. Population: sources naming at least one countermeasure, because "
         "the outcome is undefined otherwise. The class maps are in `tools/review_patterns.py` and are "
         "written into `REVIEW_STATS.json` so the assignment can be disputed.", ""]

    for role, tag in (("primary", "Primary (explicit)"), ("sensitivity", "Sensitivity (explicit + inferred)")):
        q = R[role]["q1_alignment"]
        c = q["cells"]
        L += ["### " + tag + " - n = %d" % q["n"], "",
              "| | names a radiological countermeasure | does not |", "|---|---:|---:|",
              "| names an anatomical or radiological mechanism | %d | %d |" % (c["mech+/ctr_rad+"], c["mech+/ctr_rad-"]),
              "| does not | %d | %d |" % (c["mech-/ctr_rad+"], c["mech-/ctr_rad-"]), "",
              "- Test: %s" % q["test"],
              "- Odds ratio %.2f (95%% CI %.2f to %.2f), Fisher p = %s"
              % (q["odds_ratio_haldane"], q["ci_low"], q["ci_high"], p_str(q["fisher_p"])),
              "- Naming an imaging mechanism, %s name an imaging countermeasure; not naming one, %s"
              % (fmt_ci(q["risk_exposed"]["p"], q["risk_exposed"]["lo"], q["risk_exposed"]["hi"]),
                 fmt_ci(q["risk_unexposed"]["p"], q["risk_unexposed"]["lo"], q["risk_unexposed"]["hi"])),
              "- Risk difference %s" % ("-" if q["risk_difference"] is None else "%+.1f points" % (100 * q["risk_difference"])),
              ""]
    L += ["Countermeasure classes named, primary stratum: " +
          ", ".join("%s %d" % (k, v) for k, v in sorted(P["q1_alignment"]["countermeasure_class_counts"].items())) +
          ". Mechanism classes named: " +
          ", ".join("%s %d" % (k, v) for k, v in sorted(P["q1_alignment"]["mechanism_class_counts"].items())) + ".", ""]

    L += ["---", "", "## 2. How far has each countermeasure been taken?", "",
          "Status is the strongest one found in any sentence of that source that mentions that "
          "countermeasure, by the patterns in `EVALUATION_STATUS`. Reading it only from the sentence "
          "that first named the countermeasure put 90 per cent of mentions in `not stated`, because a "
          "paper names a technique in its methods and evaluates it in its results. A sentence reporting "
          "an outcome usually also carries a recommending verb, so `proposed only` is tested last, not "
          "first. `not stated` means the source mentions the countermeasure without saying how far it "
          "has been taken - most often a technique described in use.", ""]
    for role, tag in (("primary", "Primary (explicit)"), ("sensitivity", "Sensitivity (explicit + inferred)")):
        q = R[role]["q2_evaluation"]
        L += ["### " + tag + " - %d countermeasure mentions" % q["n_countermeasure_mentions"], "",
              "| countermeasure | class | named | outcome | confidence | proposed only | not stated | "
              "proportion evaluated against an outcome |", "|---|---|---:|---:|---:|---:|---:|---|"]
        for r in q["rows"]:
            L.append("| %s | %s | %d | %d | %d | %d | %d | %s |"
                     % (r["countermeasure"], r["class"], r["n_named"], r["evaluated_against_an_outcome"],
                        r["evaluated_against_confidence"], r["proposed_only"], r["not_stated"],
                        fmt_ci(r["p_outcome"], r["ci_low"], r["ci_high"])))
        sp = q.get("spearman_named_vs_evaluated")
        if sp:
            L += ["", "- Spearman rho = %s across %d countermeasures, p = %s. %s"
                  % (sp["rho"], sp["n_countermeasures"], p_str(sp["p"]), sp["reading"])]
        L += ["", "Grouped, evaluated against an outcome:", ""]
        for g in q["by_group"]:
            L.append("- %s: %d of %d, %s" % (g["group"], g["k"], g["n"], fmt_ci(g["p"], g["lo"], g["hi"])))
        lv = q["level_step_vs_rest"]
        L += ["- %s: odds ratio %.2f (95%% CI %.2f to %.2f), Fisher p = %s"
              % (lv["contrast"], lv["odds_ratio_haldane"], lv["ci_low"], lv["ci_high"], p_str(lv["fisher_p"])), ""]

    L += ["---", "", "## 3. Reported frequency and ascertainment", "",
          "The primary set is the **adjacent** rates: the rate sits within 40 characters of the "
          "wrong-level term it is attributed to. Widening to every anchored rate admits sentences where "
          "the nearest rate belongs to a different complication, and one where \"100% preventable\" is "
          "read as an incidence, so the wider set is the sensitivity analysis. A rate is either stated "
          "in a sentence naming a wrong-level event or it is not, so there is no confidence stratum here.", ""]
    for role, tag in (("primary", "Primary (adjacent rates)"), ("sensitivity", "Sensitivity (all anchored rates)")):
        q = R[role]["q3_rates"]
        L += ["### " + tag, "",
              "%d rates, of which %d are on a per-10,000 scale and %d are strictly positive and so have a "
              "logarithm (%d zero rates are described but cannot be logged)."
              % (q["n_anchored"], q["n_normalisable"], q["n_positive_for_log"],
                 q["n_zero_rates_excluded_from_log"]), ""]
        if q.get("overall"):
            o = q["overall"]
            L += ["Median %.1f per 10,000, interquartile range %.1f to %.1f, span %.2f to %.0f - %s orders "
                  "of magnitude." % (o["median"], o["iqr_low"], o["iqr_high"], o["min"], o["max"],
                                     o["orders_of_magnitude"]), ""]
        for key, title in (("by_denominator_nature", "what the rate is a rate of"),
                           ("by_ascertainment", "ascertainment (design class)")):
            g = q[key]
            L += ["By " + title + ":", "", "| group | n | median per 10,000 | min | max |",
                  "|---|---:|---:|---:|---:|"]
            for row in g["groups"]:
                L.append("| %s | %d | %.2f | %.2f | %.1f |" % (row["group"], row["n"], row["median"],
                                                               row["min"], row["max"]))
            L += ["", "- Test: %s" % g["test"]]
            if g.get("p") is not None:
                L.append("- Groups tested: %s. H = %s on %d df, p = %s, epsilon-squared = %s"
                         % (", ".join(g["groups_tested"]), g["H"], g["df"], p_str(g["p"]),
                            g.get("epsilon_squared")))
                if g.get("mann_whitney_p") is not None:
                    L.append("- Two groups, so also Mann-Whitney U = %.1f, p = %s, rank-biserial %s"
                             % (g["mann_whitney_U"], p_str(g["mann_whitney_p"]), g["rank_biserial"]))
            else:
                L.append("- " + g.get("note", "no test run"))
            L.append("")
        rv = q["rate_vs_denominator_size"]
        if rv.get("spearman_rho") is not None:
            L += ["Rate against the size of the denominator: Spearman rho = %s on %d pairs, p = %s. %s"
                  % (rv["spearman_rho"], rv["n_pairs"], p_str(rv["p"]), rv["reading"]), ""]
        else:
            L += ["Rate against the size of the denominator: %s (%d pairs available)."
                  % (rv.get("note", ""), rv["n_pairs"]), ""]

    L += ["---", "", "## 4. Transitional and numerical anatomy", "",
          "Among sources discussing a wrong-level event, the share implicating transitional or numerical "
          "anatomy. In the primary stratum the population is exact: a field is flagged explicit only when "
          "it was matched in a sentence that also named a wrong-level event.", ""]
    for role, tag in (("primary", "Primary (explicit)"), ("sensitivity", "Sensitivity (explicit + inferred)")):
        t = R[role]["q4_transitional"]
        L += ["### " + tag, "",
              "- %d of %d sources implicate transitional or numerical anatomy: %s"
              % (t["k"], t["n"], md_ci(t)),
              "- Lumbosacral-only sources %s (n = %d) against thoracic-only %s (n = %d); "
              "odds ratio %.2f (95%% CI %.2f to %.2f), Fisher p = %s"
              % (fmt_ci(t["by_region"]["lumbosacral"]["p"], t["by_region"]["lumbosacral"]["lo"],
                        t["by_region"]["lumbosacral"]["hi"]), t["by_region"]["lumbosacral"]["n"],
                 fmt_ci(t["by_region"]["thoracic"]["p"], t["by_region"]["thoracic"]["lo"],
                        t["by_region"]["thoracic"]["hi"]), t["by_region"]["thoracic"]["n"],
                 t["by_region"]["odds_ratio_haldane"], t["by_region"]["ci_low"], t["by_region"]["ci_high"],
                 p_str(t["by_region"]["fisher_p"])),
              "- From 2010 %s (n = %d) against before 2010 %s (n = %d); odds ratio %.2f "
              "(95%% CI %.2f to %.2f), Fisher p = %s"
              % (fmt_ci(t["by_era"]["from_2010"]["p"], t["by_era"]["from_2010"]["lo"],
                        t["by_era"]["from_2010"]["hi"]), t["by_era"]["from_2010"]["n"],
                 fmt_ci(t["by_era"]["before_2010"]["p"], t["by_era"]["before_2010"]["lo"],
                        t["by_era"]["before_2010"]["hi"]), t["by_era"]["before_2010"]["n"],
                 t["by_era"]["odds_ratio_haldane"], t["by_era"]["ci_low"], t["by_era"]["ci_high"],
                 p_str(t["by_era"]["fisher_p"])),
              ""]

    L += ["---", "", "## 5. Is attention to the imaging step growing?", "",
          P["q5_time"]["measure"].capitalize() + ".", ""]
    for role, tag in (("primary", "Primary (explicit)"), ("sensitivity", "Sensitivity (explicit + inferred)")):
        t = R[role]["q5_time"]
        L += ["### " + tag + " - %d sources, %d to %d" % (t["n"], t["window"][0], t["window"][1]), "",
              "- Imaging countermeasure, Cochran-Armitage z = %s, p = %s"
              % (t["trend_imaging_countermeasure"]["z"], p_str(t["trend_imaging_countermeasure"]["p"])),
              "- Organisational countermeasure, z = %s, p = %s"
              % (t["trend_organisational_countermeasure"]["z"],
                 p_str(t["trend_organisational_countermeasure"]["p"]))]
        sp = t.get("spearman_year_vs_proportion")
        if sp:
            L.append("- Spearman year against the yearly proportion, rho = %s, p = %s, over %d years "
                     "with at least five sources" % (sp["rho"], p_str(sp["p"]),
                                                     sp["n_years_with_at_least_5_sources"]))
        L += ["", "| year | included | imaging countermeasure | organisational | proportion imaging |",
              "|---:|---:|---:|---:|---|"]
        for r in t["rows"]:
            if r["n_included"] < 5:
                continue
            L.append("| %d | %d | %d | %d | %s |" % (r["year"], r["n_included"], r["n_imaging_countermeasure"],
                                                     r["n_organisational_countermeasure"],
                                                     fmt_ci(r["proportion_imaging"], r["ci_low"], r["ci_high"])))
        L += ["", "Years with fewer than five included sources are counted in the trend test but left out "
              "of the table, where a proportion over two or three sources would read as a finding.", ""]

    # ---- 6. what the corpus cannot support
    q1p = P["q1_alignment"]
    q2p = P["q2_evaluation"]
    t4 = P["q4_transitional"]
    L += ["---", "", "## 6. What the corpus cannot support", "",
          "Tests that were not run, and what each would need.", "",
          "1. **Any multivariable model.** With %d sources in the primary 2x2 for question 1 and the "
          "smallest cell at %d, a logistic regression adjusting for design, region and year would be "
          "fitting more parameters than there are events. It would need the explicit stratum to be an "
          "order of magnitude larger, which means human charting of the full text, not more patterns."
          % (q1p["n"], min(q1p["cells"].values())),
          "2. **A pooled incidence.** One source states a numerator and a denominator in one sentence. "
          "A random-effects proportion meta-analysis needs a numerator and a denominator per study, on "
          "one denominator; this corpus has %d adjacent rates spread over %d different kinds of "
          "denominator. It would need those sources read and their tables charted by hand."
          % (P["q3_rates"]["n_anchored"],
             len({r["denominator_nature"] for r in P["q3_rates"]["rows"]})),
          "3. **Mechanism-specific countermeasure alignment.** Cross-tabulating each of the eleven "
          "mechanisms against each of the seven countermeasures is a 77-cell table over %d sources with "
          "both flagged explicitly. Almost every cell would be zero or one. It would need either a much "
          "larger explicit subset or a deliberate collapse of the classes agreed before the counting, "
          "not after." % sum(1 for r in ex if any(i["confidence"] == "explicit" for i in r["mechanisms"])
                             and any(i["confidence"] == "explicit" for i in r["countermeasures"])),
          "4. **Publication-bias or small-study tests.** Funnel plots and Egger's test need a standard "
          "error per estimate. These rates are sentences, mostly without a denominator; %d of the %d "
          "anchored rates carry a stated denominator at all."
          % (P["q3_rates"]["rate_vs_denominator_size"]["n_pairs"], P["q3_rates"]["n_anchored"]),
          "5. **Country and setting comparisons.** Country is charted from whatever sentence named a "
          "country, and a review describing another country's registry charts that country. Comparing "
          "rates or practices by country would be comparing charting artefacts. It would need the "
          "affiliation field, which neither source file stores.",
          "6. **Anything about the sources with no abstract and no full text.** 990 records were never "
          "judged. If they differ systematically from the judged ones - and closed-access surgical "
          "journals are exactly where registry and litigation series appear - every proportion here is "
          "conditioned on open access. Nothing in the corpus can measure that. It would need the "
          "abstracts of the 990, which is a request to the publishers, not a query.",
          "7. **Evaluation status as a property of a study.** It is charted per countermeasure, so a "
          "source that evaluates one countermeasure and merely proposes another contributes to both "
          "columns. Per-source evaluation status would need the methods and results read, and %d of the "
          "%d included sources have no full text at all - for those the whole evidence is an abstract."
          % (n_no_fulltext, len(ex)),
          "8. **A time trend before 2000 or after 2025.** Years outside the window carry too few sources "
          "to estimate a proportion, and 2026 is a partial year in a corpus fetched in September 2026.",
          "",
          "",
          "One more, stated because it is the largest: **the explicit stratum is small.** The primary "
          "analyses rest on %d sources naming a mechanism explicitly and %d naming a countermeasure "
          "explicitly, out of %d included. The explicit flag requires the pattern and a wrong-level term "
          "in one sentence, and window-mined passages break sentences."
          % (sum(1 for r in ex if any(i["confidence"] == "explicit" for i in r["mechanisms"])),
             sum(1 for r in ex if any(i["confidence"] == "explicit" for i in r["countermeasures"])),
             len(ex)),
          "",
          "**The two strata do not agree everywhere, and where they disagree the primary one governs.** "
          "Comparing the two on each test:", ""]
    agree = []
    for label, path in (("1, alignment of mechanism and countermeasure", ("q1_alignment", "fisher_p")),
                        ("2, level-step countermeasures against the rest",
                         ("q2_evaluation", "level_step_vs_rest", "fisher_p")),
                        ("4, transitional by region", ("q4_transitional", "by_region", "fisher_p")),
                        ("4, transitional by era", ("q4_transitional", "by_era", "fisher_p")),
                        ("5, trend in imaging countermeasures",
                         ("q5_time", "trend_imaging_countermeasure", "p"))):
        def dig(d, keys):
            for k in keys:
                d = d.get(k) if isinstance(d, dict) else None
                if d is None:
                    return None
            return d
        pp, ps = dig(P, path), dig(S, path)
        same = (pp is not None and ps is not None and (pp < 0.05) == (ps < 0.05))
        agree.append("| %s | %s | %s | %s |" % (label, p_str(pp), p_str(ps),
                                                "agree" if same else "**disagree**"))
    L += ["| test | primary p | sensitivity p | |", "|---|---|---|---|"] + agree
    L += ["", "Where they disagree, the sensitivity stratum is the one counting matches that were never "
          "tied to a wrong-level event in the same sentence. It is the larger number and the weaker "
          "evidence, and it is reported so the disagreement is visible rather than so it can be quoted.", ""]
    _ = (q2p, t4)

    with open(os.path.join(out, "REVIEW_STATS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print("wrote REVIEW_STATS.md and REVIEW_STATS.json in " + out)
    print("q1 primary n=%d OR=%.2f p=%s | q3 anchored n=%d positive=%d | q4 primary %d/%d"
          % (q1p["n"], q1p["odds_ratio_haldane"], p_str(q1p["fisher_p"]),
             P["q3_rates"]["n_anchored"], P["q3_rates"]["n_positive_for_log"], t4["k"], t4["n"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
