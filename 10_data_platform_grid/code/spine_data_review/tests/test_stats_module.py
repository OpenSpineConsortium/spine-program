"""Hand calculations against sdr/quality.py, sdr/stats.py and sdr/figures.py on tests/fixtures/stats.

Every expected value below is derived on paper (or by a pure-Python loop that a reader can follow
without numpy) from the fixture that tests/make_fixture.py writes, then compared with what the
modules wrote into runs/review_stats/a. A failing check is a finding of the review, not a fixture
error: each assertion says which rule of quality_rubric.md or statistical_analysis_plan.md it
tests. Run after tests/run_stats_review.sh:  ~/sdr_venv/bin/python tests/test_stats_module.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr import stats as S  # noqa: E402
from sdr import quality as Q  # noqa: E402

A = ROOT / "runs" / "review_stats" / "a" / "analysis"
FAILS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def close(a, b, tol=1e-9) -> bool:
    return a is not None and b is not None and abs(a - b) <= tol


def load(name: str) -> dict:
    return json.loads((A / name).read_text(encoding="utf-8"))["value"]


# ----------------------------------------------------------------------------- estimators by hand
def logit(p): return math.log(p / (1 - p))
def expit(z): return 1 / (1 + math.exp(-z))


def dl_by_hand(x, n):
    """SAP A5.3(a) written as loops; 0.5 / 1 continuity on zero or full cells only."""
    y, v = [], []
    for xi, ni in zip(x, n):
        if xi == 0 or xi == ni:
            xi, ni = xi + 0.5, ni + 1.0
        y.append(math.log(xi / (ni - xi)))
        v.append(1 / xi + 1 / (ni - xi))
    w = [1 / vi for vi in v]
    k = len(y)
    yfe = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
    q = sum(wi * (yi - yfe) ** 2 for wi, yi in zip(w, y))
    c = sum(w) - sum(wi * wi for wi in w) / sum(w)
    tau2 = max(0.0, (q - (k - 1)) / c)
    ws = [1 / (vi + tau2) for vi in v]
    mu = sum(wi * yi for wi, yi in zip(ws, y)) / sum(ws)
    se = sum(ws) ** -0.5
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0
    return {"k": k, "Q": q, "tau2": tau2, "mu": mu, "se": se, "I2": i2}


def ranks(vals):
    """Average ranks with ties, no library."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        for t in range(i, j + 1):
            r[order[t]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman_by_hand(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den


def kruskal_by_hand(groups):
    allv = [v for g in groups for v in g]
    r, big_n = ranks(allv), len(allv)
    off, h = 0, 0.0
    for g in groups:
        rs = r[off:off + len(g)]
        h += len(g) * (sum(rs) / len(rs) - (big_n + 1) / 2) ** 2
        off += len(g)
    h *= 12 / (big_n * (big_n + 1))
    ties = {}
    for v in allv:
        ties[v] = ties.get(v, 0) + 1
    corr = 1 - sum(t ** 3 - t for t in ties.values()) / (big_n ** 3 - big_n)
    return h / corr


def main() -> int:
    print("== estimators (unit checks against paper values)")
    w = S.wilson(3, 10)
    # p = 0.3, n = 10, z = 1.959964: centre 0.35551, half-width 0.24771 -> [0.1078, 0.6032]
    check("Wilson 3/10 = [0.1078, 0.6032]", close(w["ci"][0], 0.1078, 5e-4) and close(w["ci"][1], 0.6032, 5e-4), str(w["ci"]))
    cp = S.clopper_pearson(0, 20)
    # upper = 1 - 0.025^(1/20) = 0.16843
    check("Clopper-Pearson 0/20 = [0, 0.1684]", cp["ci_low"] == 0.0 and close(cp["ci_high"], 1 - 0.025 ** (1 / 20), 1e-9), str(cp))
    check("Clopper-Pearson 20/20 upper = 1", S.clopper_pearson(20, 20)["ci_high"] == 1.0)
    x, n = [12, 0, 5, 45, 60, 2], [100, 150, 60, 300, 500, 25]     # the six poolable LSTV rows of the fixture
    hand, mod = dl_by_hand(x, n), S.dl_logit(x, n)
    for key, mk in (("Q", "Q"), ("tau2", "tau2"), ("mu", "logit"), ("se", "se"), ("I2", "I2")):
        check(f"DL {key} matches the loop version", close(hand[key], mod[mk], 1e-9), f"{hand[key]} vs {mod[mk]}")
    check("DL continuity applied to exactly one cell (0/150)", mod["continuity_corrected"] == 1)
    # Q-profile: the tau2 bounds must solve Q(tau2) = chi2 quantiles; recover tau2 from the reported I2 and s2.
    from scipy import stats as sp
    yv = [math.log((xi + 0.5 * (xi in (0, ni))) / ((ni + (xi in (0, ni))) - (xi + 0.5 * (xi in (0, ni))))) for xi, ni in zip(x, n)]
    vv = [1 / (xi + 0.5 * (xi in (0, ni))) + 1 / ((ni + (xi in (0, ni))) - (xi + 0.5 * (xi in (0, ni)))) for xi, ni in zip(x, n)]
    ww = [1 / v for v in vv]
    s2 = (len(x) - 1) * sum(ww) / (sum(ww) ** 2 - sum(v * v for v in ww))
    def gq(t2):
        wt = [1 / (v + t2) for v in vv]
        m = sum(a * b for a, b in zip(wt, yv)) / sum(wt)
        return sum(a * (b - m) ** 2 for a, b in zip(wt, yv))
    lo_i2, hi_i2 = mod["I2_ci"]
    t_lo, t_hi = lo_i2 * s2 / (1 - lo_i2), hi_i2 * s2 / (1 - hi_i2)
    check("I2 Q-profile lower bound solves Q(tau2) = chi2_0.975", close(gq(t_lo), sp.chi2.ppf(0.975, 5), 1e-5) or (t_lo == 0 and gq(0) <= sp.chi2.ppf(0.975, 5)),
          f"Q(t_lo)={gq(t_lo):.4f} vs {sp.chi2.ppf(0.975, 5):.4f}")
    check("I2 Q-profile upper bound solves Q(tau2) = chi2_0.025", close(gq(t_hi), sp.chi2.ppf(0.025, 5), 1e-5), f"Q(t_hi)={gq(t_hi):.4f} vs {sp.chi2.ppf(0.025, 5):.4f}")
    check("prediction interval uses t_{k-2} (k=6 -> t_4 = 2.7764)",
          close(logit(mod["pi_high"]) - mod["logit"], 2.776445 * math.sqrt(mod["tau2"] + mod["se"] ** 2), 1e-5))
    # Spearman with the Bonett-Wright interval on a tiny hand set: x = 1..5, y = [2,1,4,3,5]: d = [1,-1,1,-1,0], rho = 1 - 6*4/(5*24) = 0.8
    sc = S.spearman_ci([1, 2, 3, 4, 5], [2, 1, 4, 3, 5])
    se = math.sqrt((1 + 0.64 / 2) / 2)
    check("Spearman rho 0.8 on the hand set", close(sc["rho"], 0.8, 1e-12))
    check("Bonett-Wright interval on the hand set", close(sc["ci"][0], math.tanh(math.atanh(0.8) - 1.959964 * se), 1e-9)
          and close(sc["ci"][1], math.tanh(math.atanh(0.8) + 1.959964 * se), 1e-9))
    # Kruskal-Wallis with ties: groups [16,19,13,14,13] and [14,16,15,15,15] (the fixture's annotated stratum by route)
    g1, g2 = [16, 19, 13, 14, 13], [14, 16, 15, 15, 15]
    kw = S.kruskal({"open-download": g1, "registration": g2})
    check("Kruskal-Wallis H with tie correction matches the loop version", close(kw["H"], kruskal_by_hand([g1, g2]), 1e-9), f"{kw['H']} vs {kruskal_by_hand([g1, g2])}")
    check("epsilon2 = (H - k + 1)/(n - k)", close(kw["epsilon2"], (kw["H"] - 1) / 8, 1e-12))
    # Dunn z for one pair, by hand: mean ranks from the pooled ranking, tie term sum(t^3-t)/(12(N-1))
    dn = S.dunn_holm({"a": g1, "b": g2})[0]
    r = ranks(g1 + g2)
    tie = sum(t ** 3 - t for t in {v: (g1 + g2).count(v) for v in set(g1 + g2)}.values()) / (12 * 9)
    z = (sum(r[:5]) / 5 - sum(r[5:]) / 5) / math.sqrt((10 * 11 / 12 - tie) * (1 / 5 + 1 / 5))
    check("Dunn z by hand", close(dn["z"], z, 1e-9), f"{dn['z']} vs {z}")
    check("Holm with one pair leaves p unchanged", close(dn["p_holm"], dn["p"], 1e-12))

    print("== quality.json against the hand-scored rubric")
    qj = json.loads((A / "quality.json").read_text(encoding="utf-8"))
    expect_total = {"ds01": 16, "ds02": 19, "ds03": 14, "ds04": 13, "ds05": 16, "ds06": 11, "ds07": 14, "ds08": 15, "ds09": 12, "ds10": 15, "ds11": 13, "ds12": 15}
    for did, t in expect_total.items():
        got = qj["per_dataset"][did]
        check(f"{did} total {t}", got["total"] == t, f"got {got['total']}: " + "; ".join(v["rule"] for v in got["items"].values() if v["score"] != 2))
    items01 = {q: v["score"] for q, v in qj["per_dataset"]["ds01"]["items"].items()}
    check("ds01 items = Q1 2, Q2 2, Q3 2, Q4 2, Q5 1, Q6 2, Q7 2, Q8 1, Q9 2, Q10 0",
          items01 == {"Q1": 2, "Q2": 2, "Q3": 2, "Q4": 2, "Q5": 1, "Q6": 2, "Q7": 2, "Q8": 1, "Q9": 2, "Q10": 0}, str(items01))
    check("ds03 Q7 = 1 (landing probes agree, no file evidence: rule P3, file_url null)", qj["per_dataset"]["ds03"]["items"]["Q7"]["score"] == 1)
    check("ds06 Q7 = 0 (both probes 404)", qj["per_dataset"]["ds06"]["items"]["Q7"]["score"] == 0)
    check("ds09 (unannotated) Q1 still 2 because states_annotation_protocol is waived", qj["per_dataset"]["ds09"]["items"]["Q1"]["score"] == 2)
    fit = {d: qj["per_dataset"][d]["fit_level_id"] for d in expect_total}
    check("fit_level_id fails only ds05 (F2), ds06 (F3), ds09 (F1), ds10 (F4)",
          [d for d, f in fit.items() if not f] == ["ds05", "ds06", "ds09", "ds10"], str([d for d, f in fit.items() if not f]))
    fr = {d: qj["per_dataset"][d]["fit_level_id_fail_rule"] for d in ("ds05", "ds06", "ds09", "ds10")}
    check("fail rules F2/F3/F1/F4", fr == {"ds05": "F2", "ds06": "F3", "ds09": "F1", "ds10": "F4"}, str(fr))
    check("fit_stitching = ds02, ds04, ds11 (thoracic or whole-spine among fit)",
          sorted(d for d in expect_total if qj["per_dataset"][d]["fit_stitching"]) == ["ds02", "ds04", "ds11"])
    check("bands: 11 -> medium, 13 -> medium, 14 -> high", (qj["per_dataset"]["ds06"]["band"], qj["per_dataset"]["ds04"]["band"], qj["per_dataset"]["ds03"]["band"]) == ("medium", "medium", "high"))
    check("summary.n_fit_level_id = 8", qj["summary"]["n_fit_level_id"] == 8)
    check("usable_for_training also true for ds05 (F2 not required)", qj["per_dataset"]["ds05"]["usable_for_training"])

    print("== flow.json against the fixture's counts (SAP A1)")
    f = load("flow.json")
    sa = f["search_arm"]
    check("identified 15 (prisma_counts.json)", sa["identified"] == 15)
    check("after_merge 12", sa["after_merge"] == 12)
    check("duplicates_removed 3", sa["duplicates_removed"] == 3)
    check("prescreen pass 7 / uncertain 1 / non-english 1 / fail 3", (sa["prescreen"]["pass"], sa["prescreen"]["uncertain"], sa["prescreen"]["non_english_route"], sa["prescreen"]["fail_total"]) == (7, 1, 1, 3))
    check("screened 10", sa["screened"] == 10)
    check("screen_excluded_by_code E1 2, I3 1; use_only 1", sa["screen_excluded_by_code"] == {"E1": 2, "I3": 1} and sa["use_only"] == 1, str(sa["screen_excluded_by_code"]))
    check("sought_for_full_text 6, not_retrieved 2", (sa["sought_for_full_text"], sa["not_retrieved"]) == (6, 2))
    check("full_text_excluded_by_code E2 1, I5 1; included_records 4", sa["full_text_excluded_by_code"] == {"E2": 1, "I5": 1} and sa["included_records"] == 4)
    oa = f["other_arm"]
    check("other arm: screened 2, included 1, excluded 1", (oa["screened"], oa["included_records"], oa["excluded"]) == (2, 1, 1))
    check("chase forward 1 / backward 1 / manual 1", (oa["chase_forward"], oa["chase_backward"], oa["chase_manual"]) == (1, 1, 1))
    check("known_items 3", oa["known_items"] == 3)
    # per_source counts the SEARCH arm only: openalex ran three search records (openalex_01) plus two
    # chase records (openalex_03_W1, openalex_03r_W2), and the chase pair is counted in other_arm.
    check("per_source n_identified pubmed 6, zenodo 4, openalex 3 (chase excluded)",
          {s: r["n_identified"] for s, r in f["per_source"].items()} == {"pubmed": 6, "zenodo": 4, "openalex": 3},
          str({s: r["n_identified"] for s, r in f["per_source"].items()}))
    check("the two openalex chase records are the other arm's forward + backward (3 + 2 = the 5 openalex rows)",
          (oa["chase_forward"] or 0) + (oa["chase_backward"] or 0) == 2 and f["per_source"]["openalex"]["n_identified"] + 2 == 5,
          f"forward {oa['chase_forward']} backward {oa['chase_backward']}")
    check("per_source openalex cap_hit lists openalex_01", f["per_source"]["openalex"]["cap_hit"] == ["openalex_01"])
    check("all nine identities True", all(v is True for v in f["identities"].values()), str(f["identities"]))
    check("every dataset maps from an included record (A1 mapping identity, True branch)",
          f["datasets"]["mapped_from_included_records"] == sorted(expect_total) and f["datasets"]["not_mapped_from_included"] == []
          and f["datasets"]["included_records_unmapped"] == [], str(f["datasets"]["not_mapped_from_included"]))
    check("merge_rules holds only rule counts (rule_6_skipped_many_dois is a diagnostic, not a merge rule)", "rule_6_skipped_many_dois" not in sa["merge_rules"], str(sa["merge_rules"]))
    check("datasets: total 12, derived 1, figure-derived 1", (f["datasets"]["total"], f["datasets"]["derived"], f["datasets"]["figure_derived"]) == (12, 1, 1))
    check("no missing inputs", f["missing_inputs"] == [], str(f["missing_inputs"]))
    # Identity 1: tamper with prisma_counts.json in a scratch run dir (duplicates_removed = 99 while
    # identified 15 and after_merge 12 stay); a real check must report False.
    import shutil
    tam = ROOT / "runs" / "review_stats" / "tamper"
    if tam.exists():
        shutil.rmtree(tam)
    shutil.copytree(ROOT / "runs" / "review_stats", tam, ignore=shutil.ignore_patterns("a", "b", "tamper", "limit3"))
    pc = json.loads((tam / "prisma_counts.json").read_text(encoding="utf-8"))
    pc["duplicates_removed"] = 99
    (tam / "prisma_counts.json").write_text(json.dumps(pc), encoding="utf-8")
    from sdr.common import RunDir
    tf = S.flow(RunDir(tam), ROOT / "tests" / "fixtures" / "stats" / "screening", ROOT / "tests" / "fixtures" / "stats", [], ROOT / "tests" / "fixtures" / "stats" / "screening")["value"]
    check("identity 'identified - duplicates = after_merge' reads duplicates_removed from prisma_counts.json (99 -> False)",
          tf["identities"]["identified - duplicates = after_merge"] is False,
          f"duplicates_removed reported as {tf['search_arm']['duplicates_removed']}: computed as identified - len(merged), so the identity cannot fail")
    # Identity 9, False branch: chart a thirteenth dataset whose only record (rid[7] = lit:000000000008)
    # the fixture excludes at title-abstract, and leave it out of dataset_sources.csv. The dataset count
    # rises to 13 while the mapping still reaches 12, so a real check must report False and name it.
    import copy
    FS = ROOT / "tests" / "fixtures" / "stats"
    ds_all = S.load_datasets(FS / "charting")
    orphan = copy.deepcopy(ds_all[0])
    orphan["id"] = "ds13"
    orphan["source_record"]["record_ids"] = ["lit:000000000008"]
    args = (RunDir(ROOT / "runs" / "review_stats"), FS / "screening", FS, None, FS / "screening")
    pos = S.flow(*args[:3], ds_all, args[4])["value"]
    neg = S.flow(*args[:3], ds_all + [orphan], args[4])["value"]
    key = "datasets = |map(included_records_search U included_records_other)|"
    check("A1 mapping identity is True on the twelve charted datasets", pos["identities"][key] is True, str(pos["datasets"]["not_mapped_from_included"]))
    check("A1 mapping identity goes False when a dataset is charted from an excluded record",
          neg["identities"][key] is False and neg["datasets"]["not_mapped_from_included"] == ["ds13"],
          f"identity {neg['identities'][key]}, unmapped datasets {neg['datasets']['not_mapped_from_included']}")

    print("== descriptives.json (SAP A2 general rules)")
    d = load("descriptives.json")
    tk = d["totals_rule"]
    check("ds04 excluded from totals as family duplicate of ds01", tk["excluded"].get("ds04", "").startswith("parent family duplicate of ds01"), str(tk["excluded"]))
    check("ds06 (figure-derived) and ds11 (estimated) excluded from totals", "ds06" in tk["excluded"] and "ds11" in tk["excluded"])
    # Subjects in totals: ds01 100 + ds02 200 + ds03 150 + ds05 60 + ds07 300 + ds08 500 + ds09 25 + ds10 15 + ds12 70 = 1420, minus n_shared 50 = 1370
    check("n_subjects_sum = 1420 - 50 shared (SAP: 'where n_shared is known, totals subtract it')", d["totals"]["n_subjects_sum"] == 1370,
          f"got {d['totals']['n_subjects_sum']} (subtract = {tk['subtract']}); the overlap is listed on ds08 only and ds08 > ds01 so subtract is skipped")
    bm = d["by_modality"]
    check("by_modality.CT.n_datasets = 7 (ds01 02 04 07 08 10 12)", bm["CT"]["n_datasets"] == 7, str({k: v["n_datasets"] for k, v in bm.items()}))
    # SAP A2: multi-modal datasets contribute n_per_modality to the per-modality rows, never their overall count.
    # CT row: ds01 100 + ds02 200 + ds07 (CT) 200 + ds08 500 + ds10 15 + ds12 70 = 1085 (ds04 family-excluded)
    check("by_modality.CT.n_subjects_sum uses n_per_modality for ds07 (1085, not 1185)", bm["CT"]["n_subjects_sum"] == 1085, f"got {bm['CT']['n_subjects_sum']}")
    # radiograph row: ds03 150 + ds05 60 + ds07 (XR) 120 + ds09 25 = 355 (not 535)
    check("by_modality.radiograph.n_subjects_sum uses n_per_modality for ds07 (355, not 535)", bm["radiograph"]["n_subjects_sum"] == 355, f"got {bm['radiograph']['n_subjects_sum']}")
    cum = d["cumulative_subjects_by_year_modality"]
    check("cumulative CT by 2026 = 1085 (same rule, so the two must agree)", cum["CT"]["2026"] == 1085, f"got {cum['CT']['2026']}")
    check("by_variant_labelling explicit-label 10, neither 1 (ds11), reported-in-text not a row -> 'neither' 2",
          d["by_variant_labelling"].get("explicit-label", {}).get("n_datasets") == 10 and d["by_variant_labelling"].get("neither", {}).get("n_datasets") == 2,
          str({k: v["n_datasets"] for k, v in d["by_variant_labelling"].items()}))
    # the schema enum seeds every category, so 'partial' is present with a zero and must be asserted
    check("by_level_names yes 11 / partial 0 / no 1 (categories seeded from the schema enum)",
          {k: v["n_datasets"] for k, v in d["by_level_names"].items()} == {"yes": 11, "partial": 0, "no": 1},
          str({k: v["n_datasets"] for k, v in d["by_level_names"].items()}))
    check("by_annotation_origin counting-inferred absent, expert-manual 10", d["by_annotation_origin"].get("expert-manual", {}).get("n_datasets") == 10)

    print("== availability.json (SAP A3)")
    av = load("availability.json")
    # all six routes of the schema enum are seeded, so the four the fixture does not use read 0 rather than being absent
    check("route distribution open 6 / registration 5 / unavailable 1, the other four routes seeded at 0",
          av["route_distribution"]["overall"] == {"commercial": 0, "data-use-agreement": 0, "open-download": 6, "registration": 5,
                                                  "request-to-authors": 0, "unavailable": 1},
          str(av["route_distribution"]["overall"]))
    dp = av["described_public_downloads"]
    check("described public: 11 datasets, 6 open-download", (dp["primary"]["denominator"], dp["primary"]["numerator"]) == (11, 6))
    # file_url: 10 datasets carry file_url_probed; every one has two 206 file probes in charting/probes/<id>.json
    check("file_url row counts the file probes in charting/probes/<id>.json (10/10, not 0/10)", (dp["file_url"]["numerator"], dp["file_url"]["denominator"]) == (10, 10),
          f"got {dp['file_url']['numerator']}/{dp['file_url']['denominator']}: stats reads access_probe[], availability.py keeps file_probes[] in charting/probes/")
    check("recipe_eligible 11/11 (ds06 is described_as_public = no)", (dp["recipe_eligible"]["numerator"], dp["recipe_eligible"]["denominator"]) == (11, 11), str(dp["recipe_eligible"]))
    bands = av["unavailable_x_year_band"]
    check("unavailable by band: 2021-2026 has 1/4 (ds05 ds06 ds07 ds11)", (bands["2021-2026"]["numerator"], bands["2021-2026"]["denominator"]) == (1, 4), str({k: (b["numerator"], b["denominator"]) for k, b in bands.items()}))
    check("trend test present (four bands)", av["trend_unavailable_by_band"] is not None)

    print("== quality_analysis.json (SAP A4)")
    qa = load("quality_analysis.json")
    totals_all = sorted(expect_total.values())
    check("median of all 12 totals = 14.5, IQR [13, 15.25] (numpy linear)", close(qa["total"]["median"], 14.5) and close(qa["total"]["q1"], 13.0) and close(qa["total"]["q3"], 15.25),
          f"{qa['total']['median']} {qa['total']['q1']} {qa['total']['q3']} from {totals_all}")
    years = {"ds01": 2015, "ds02": 2017, "ds03": 2019, "ds04": 2020, "ds05": 2021, "ds06": 2022, "ds07": 2023, "ds08": 2018, "ds10": 2016, "ds11": 2024, "ds12": 2009}
    rho = spearman_by_hand([years[k] for k in years], [expect_total[k] for k in years])
    check("Spearman rho (annotated stratum, n = 11) matches the rank loop", close(qa["total_vs_year"]["annotated"]["rho"], rho, 1e-9) and qa["total_vs_year"]["annotated"]["n"] == 11,
          f"{qa['total_vs_year']['annotated']['rho']} vs {rho}")
    kr = qa["total_vs_route"]["annotated"]
    check("Kruskal (annotated, by route) uses open 5 / registration 5, unavailable dropped (< 5)", set(kr["groups"]) == {"open-download", "registration"} and kr["n"] == 10)
    check("Kruskal H (annotated) = hand value", close(kr["H"], kruskal_by_hand([g1, g2]), 1e-9), f"{kr['H']}")
    check("fitness.fit_level_id.n = 8", qa["fitness"]["fit_level_id"]["n"] == 8)
    check("fail_rule distribution F1 1, F2 1, F3 1, F4 1", qa["fitness"]["fail_rule"] == {"F1": 1, "F2": 1, "F3": 1, "F4": 1})
    check("quality.json carries the merged A4 blocks the manuscript reads", "total" in qj.get("summary", {}) and "fitness" in qj and "total_vs_year" in qj)

    print("== pooled_variants.json (SAP A5)")
    pv = load("pooled_variants.json")
    L = pv["LSTV"]
    ids = [r["id"] for r in L["per_dataset"]]
    check("LSTV rows sorted by year then id", ids == sorted(ids, key=lambda i: (years.get(i, 2012 if i == "ds09" else 0), i)), str(ids))
    check("LSTV k_eligible = 6 (ds01 ds03 ds05 ds07 ds08 ds09)", L["k_eligible"] == 6 and sorted(r["id"] for r in L["per_dataset"] if r["poolable"]) == ["ds01", "ds03", "ds05", "ds07", "ds08", "ds09"],
          str(sorted(r["id"] for r in L["per_dataset"] if r["poolable"])))
    reasons = {r["id"]: r["ineligible_reasons"] for r in L["per_dataset"]}
    check("ds04 family duplicate, ds06 figure-derived, ds10 n<20, ds12 unverified, ds02 enriched",
          "family/overlap duplicate" in reasons["ds04"] and "figure-derived" in reasons["ds06"] and "n<20" in reasons["ds10"] and "unverified" in reasons["ds12"]
          and L["enriched"]["ids"] == ["ds02"], str(reasons))
    check("pooled LSTV logit/tau2/se equal the loop version on the same six rows", close(L["pooled"]["logit"], hand["mu"], 1e-9) and close(L["pooled"]["tau2"], hand["tau2"], 1e-9)
          and close(L["pooled"]["se"], hand["se"], 1e-9))
    check("pooled estimate = expit(mu), CI = expit(mu +/- 1.96 se)", close(L["pooled"]["estimate"], expit(hand["mu"]), 1e-9)
          and close(L["pooled"]["ci_low"], expit(hand["mu"] - 1.959964 * hand["se"]), 1e-9))
    check("L6 not pooled (k = 1 < 5)", pv["L6"]["pooled"] is None and pv["L6"]["k_eligible"] == 1 and "k = 1" in pv["L6"]["note"])
    check("enriched stratum not pooled (k = 1)", L["enriched"]["pooled"] is None)
    cp3 = next(r for r in L["per_dataset"] if r["id"] == "ds03")
    check("ds03 0/150 exact interval [0, 0.0243]", cp3["ci_low"] == 0.0 and close(cp3["ci_high"], 1 - 0.025 ** (1 / 150), 1e-9))

    print("== grid_coverage.json (SAP A7)")
    g = load("grid_coverage.json")
    check("overall: on grid 1, reachable 11, reachable not on grid 10", (g["overall"]["n_on_grid"], g["overall"]["n_reachable"], g["overall"]["n_reachable_not_on_grid"]) == (1, 11, 10), str(g["overall"]))
    check("recipe_order = fit & reachable & not on grid, quality desc then id: ds02 ds08 ds12 ds03 ds07 ds04 ds11",
          [r["id"] for r in g["recipe_order"]] == ["ds02", "ds08", "ds12", "ds03", "ds07", "ds04", "ds11"], str([r["id"] for r in g["recipe_order"]]))
    check("fit_level_id_on_grid = 1/8", (g["fit_level_id_on_grid"]["numerator"], g["fit_level_id_on_grid"]["denominator"]) == (1, 8))

    print("== figures")
    fdir = A.parent / "figures"
    for name in ("fig1_prisma_flow", "fig2_datasets_per_year", "fig3_access_by_modality", "fig4_quality", "fig5_forest_LSTV", "fig5_forest_L6"):
        check(f"{name}.pdf and .png written", (fdir / f"{name}.pdf").exists() and (fdir / f"{name}.png").exists())
    check("fig5_forest_T13 skipped (no rows)", not (fdir / "fig5_forest_T13.pdf").exists())
    pdf = (fdir / "fig5_forest_LSTV.pdf").read_bytes()
    sha = __import__("hashlib").sha1((A / "pooled_variants.json").read_bytes()).hexdigest()
    check("forest PDF Subject carries the sha1 of pooled_variants.json", sha.encode() in pdf)
    check("PDF carries no wall-clock CreationDate/ModDate (determinism rule)", b"/CreationDate" not in pdf and b"/ModDate" not in pdf)

    print(f"\n{len(FAILS)} failing check(s)" + (":\n  - " + "\n  - ".join(FAILS) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
