"""Arithmetic for the topic-4 note. Every function below is copied from a repository file so the numbers are the
repository's method applied to today's n, not a new method:
  wilson / p_exact / k_crit / power  : SchwingNet/LEVELCHECK_MODEL.md section 11 (verbatim)
  cohens_h / n_two_proportions       : tools/stats_compare.py (verbatim logic)
Prevalence arithmetic: priors from tools/acquisition_census.py (P_LSTV_LOW 0.09, P_LSTV_HIGH 0.18, P_COUNT 0.048
= L6 0.032 + four-lumbar 0.016, P_T13 0.0064-0.020) times countable people taken from the files named per row.
"""
import json
import math
from statistics import NormalDist
from scipy.stats import binom, beta

Z = 1.959963984540054
ND = NormalDist()


def wilson(k, n):
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def p_exact(k, n, p0):
    return binom.sf(k - 1, n, p0)


import numpy as np
_KC = {}


def k_crit(n, p0, alpha=0.025):
    # same definition as LEVELCHECK_MODEL.md s11 (smallest k with P(X >= k) <= alpha), vectorised for speed
    key = (n, p0, alpha)
    if key not in _KC:
        ks = np.arange(n + 1)
        ok = np.nonzero(binom.sf(ks - 1, n, p0) <= alpha)[0]
        _KC[key] = int(ks[ok[0]]) if ok.size else None
    return _KC[key]


def power(n, p0, p1, alpha=0.025):
    k = k_crit(n, p0, alpha)
    return 0.0 if k is None else float(binom.sf(k - 1, n, p1))


def wilson_target_prob(n, target, p_true):
    """P(Wilson lower bound >= target) when the true accuracy is p_true: the largest error count e whose bound
    still meets the target, then P(errors <= e)."""
    e_max = None
    for e in range(n + 1):
        if wilson(n - e, n)[0] >= target:
            e_max = e
        else:
            break
    if e_max is None:
        return 0.0, None
    return float(binom.cdf(e_max, n, 1 - p_true)), e_max


def cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def n_two_proportions(p1, p2, alpha=0.05, pw=0.8, deff=1.0, ratio=1.0):
    h = abs(cohens_h(p1, p2))
    z = ND.inv_cdf(1 - alpha / 2) + ND.inv_cdf(pw)
    n1 = deff * (1 + 1.0 / ratio) * (z / h) ** 2
    return math.ceil(n1), math.ceil(n1 * ratio), h


out = {}

# 1. LevelCheck hypotheses at TODAY's n (n values from the files cited in the note)
H = {"H1_822": 0.822, "H6_926": 0.926, "H2_976": 0.976}
ns = {"real_at_risk_two_labeller_7": 7, "at_risk_CT_test_51": 51, "screen_supported_calls_57": 57,
      "H6_open_gate_ref_ordinary_13": 13, "H6_ordinary_upper_bound_51": 51, "H6_open_gate_T2_32": 32}
res = {}
for hn, p0 in H.items():
    for nn, n in ns.items():
        row = {"k_crit": k_crit(n, p0)}
        for t in (0.90, 0.95, 0.97, 0.99):
            row[f"power_true_{int(t*100)}"] = round(power(n, p0, t), 4)
        res[f"{hn}@{nn}"] = row
out["levelcheck_power_today"] = res

# first n with 80 / 90 % power for H1 at true 0.90/0.95/0.97 (unadjusted 0.025) -- cross-check of S1
def first_n(p0, p1, target, alpha=0.025, nmax=1300):
    for n in range(1, nmax):
        if power(n, p0, p1, alpha) >= target:
            return n
    return None

def always_from(p0, p1, target, alpha=0.025, nmax=1300):
    last_fail = None
    for n in range(1, nmax):
        if power(n, p0, p1, alpha) < target:
            last_fail = n
    return None if last_fail is None else last_fail + 1

fn = {}
for p0 in (0.822, 0.926, 0.976):
    for p1 in (0.90, 0.95, 0.97, 0.98, 0.99):
        if p1 <= p0:
            continue
        for tgt in (0.8, 0.9):
            fn[f"p0_{p0}_true_{p1}_power_{tgt}"] = {"first_n": first_n(p0, p1, tgt), "always_from": always_from(p0, p1, tgt)}
out["first_n_power"] = fn

# 2. Wilson targets (paper 1 G6): probability the bound is met, and n for 80/90 % probability
wt = {}
for target in (0.90, 0.85):
    for n in (3, 7, 22, 35, 43, 51, 57):
        for t in (0.95, 0.97, 0.98, 0.99):
            pr, e = wilson_target_prob(n, target, t)
            wt[f"target_{target}_n_{n}_true_{t}"] = {"prob": round(pr, 4), "errors_allowed": e}
    for t in (0.724, 0.90, 0.95, 0.97, 0.98, 0.99):
        for goal in (0.8, 0.9):
            first = None
            for n in range(1, 1300):
                pr, _ = wilson_target_prob(n, target, t)
                if pr >= goal:
                    first = n
                    break
            wt[f"target_{target}_true_{t}_first_n_prob_{goal}"] = first
out["wilson_targets"] = wt

# 3. transitional vs ordinary, two proportions (stats_compare form)
tvo = {}
for name, p1, p2 in [("film_interior_ordinary_918_vs_anomalous_660", 0.918, 0.660),
                     ("film_interior_v5_935_vs_573", 0.935, 0.573),
                     ("render_L6_recall_724_vs_ordinary_film_988", 0.988, 0.724),
                     ("carm_whole_frame_982_vs_L6_classifier_449", 0.982, 0.449)]:
    for pw in (0.8, 0.9):
        for deff in (1.0, 4.0):
            n1, n2, h = n_two_proportions(p1, p2, 0.05, pw, deff)
            tvo[f"{name}_power{pw}_deff{deff}"] = {"n_per_arm": n1, "cohens_h": round(h, 3)}
out["transitional_vs_ordinary"] = tvo

# 4. device-level exact sign-flip: smallest attainable two-sided P with k devices
out["device_level_min_two_sided_p"] = {k: round(2 / 2 ** k, 4) for k in range(3, 9)}
# paired exact sign test over cases: discordant cases needed (all one way) for two-sided P <= 0.05 and <= 0.0125
def min_disc(alpha):
    for m in range(1, 40):
        if 2 * 0.5 ** m <= alpha:
            return m
out["sign_test_min_discordant_all_one_way"] = {"alpha_0.05": min_disc(0.05), "alpha_0.0125_holm4": min_disc(0.0125),
                                               "alpha_0.025": min_disc(0.025)}

# 5. prevalence arithmetic
P_LSTV_LOW, P_LSTV_HIGH, P_COUNT, P_L6, P_4L = 0.09, 0.18, 0.048, 0.032, 0.016
P_T13_LOW, P_T13_HIGH = 0.0064, 0.020
prev = {}
def block(name, countable_ls, cage):
    d = {"countable_ls": countable_ls, "cage": cage,
         "L6": round(countable_ls * P_L6, 1), "four_lumbar": round(countable_ls * P_4L, 1),
         "count_anomalies": round(countable_ls * P_COUNT, 1),
         "castellvi_II_IV_low": round(countable_ls * P_LSTV_LOW, 1), "castellvi_II_IV_high": round(countable_ls * P_LSTV_HIGH, 1)}
    if cage is not None:
        d["T13_low"] = round(cage * P_T13_LOW, 1)
        d["T13_high"] = round(cage * P_T13_HIGH, 1)
    prev[name] = d
block("ctsp_802x0.984", 802 * 0.984, 0.0)
block("ts_v2_1228_sumP", 483.0, 471.0)
block("cobra_readable_435", 435, None)
prev["census_table_18_collections"] = {"L6": 322, "four_lumbar": 161, "castellvi_II_IV_low": 907, "castellvi_II_IV_high": 1813,
                                       "T13_low": 38, "T13_high": 119, "gate_pass": 12123}
prev["ribfrac_ranking"] = {"T13_low": 2.9, "T13_high": 9.2}
tot = {"L6": 0, "four_lumbar": 0, "castellvi_II_IV_low": 0, "castellvi_II_IV_high": 0, "T13_low": 0, "T13_high": 0}
for k, v in prev.items():
    for f in tot:
        tot[f] += v.get(f, 0) or 0
prev["total_excluding_verse_carmlspine_phantoms_rsna"] = {k: round(v, 1) for k, v in tot.items()}
# observed CTSP rates against the prior
prev["ctsp_L6_18_of_789_wilson"] = [round(x * 100, 2) for x in wilson(18, 789)]
prev["ctsp_L6_18_of_802_pct"] = round(18 / 802 * 100, 2)
prev["ctsp_four_lumbar_9_of_789_wilson"] = [round(x * 100, 2) for x in wilson(9, 789)]
prev["ctsp_count_anomaly_27_of_789_wilson"] = [round(x * 100, 2) for x in wilson(27, 789)]
prev["cobra_L6_38_of_435_wilson"] = [round(x * 100, 2) for x in wilson(38, 435)]
prev["cobra_four_lumbar_8_of_435_wilson"] = [round(x * 100, 2) for x in wilson(8, 435)]
prev["cobra_L6_registry_3_of_435_wilson"] = [round(x * 100, 2) for x in wilson(3, 435)]
out["prevalence"] = prev

# 6. what the L6 render recall implies for the 85 % sensitivity bound
out["l6_recall_724_all_correct_prob"] = {n: round(0.724 ** n, 5) for n in (3, 7, 22, 43)}

print(json.dumps(out, indent=1))
# written next to this script (it once wrote to a session scratchpad path, which fails on any other machine)
import os
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "power_calc.json"), "w"), indent=1)
