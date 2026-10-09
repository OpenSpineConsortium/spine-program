"""The estimators of statistical_analysis_plan.md, written out once in numpy and checked against published values.

WHY THE FORMULAE LIVE APART FROM THE ANALYSES. The SAP names estimators the allowed libraries
lack or hide (Kruskal-Wallis epsilon-squared, Dunn with a tie term and Holm, the Bonett-Wright
interval on Spearman's rho, DerSimonian-Laird on the logit scale with I-squared and its Q-profile
interval, Wilson and Clopper-Pearson intervals) and asks that each be written explicitly and
checked against a published or library value before any review data is pooled. Keeping them in
one module that reads no file means the check (`selftest`) sits beside the arithmetic it checks,
every analysis in sdr/stats.py calls the same function, and no manuscript number is the product
of two implementations of one formula. `--selftest` compares DL against statsmodels
`combine_effects(method_re="dl")` to 1e-6 (statsmodels does not truncate tau2 at zero, so the
comparison is against max(0, tau2)), Wilson and Clopper-Pearson against a hand-computed 7/20 cell,
and epsilon-squared against its definition.

Every function returns plain dicts and lists of Python floats (JSON-native); a statistic that is
undefined on its input (constant vector, empty group) is None with a `note`, never NaN, because
json.dumps would write the non-standard token NaN and a downstream reader would choke on it.
CLI: python -m sdr.estimators --selftest
"""
from __future__ import annotations

import argparse
import math
import sys
from collections import Counter

import numpy as np
from scipy import optimize, stats

Z = 1.959964


def wilson(x: int, n: int) -> dict:
    """Wilson score interval without continuity correction (SAP general rules)."""
    if n == 0:
        return {"numerator": x, "denominator": n, "proportion": None, "ci": None}
    p, d = x / n, 1 + Z * Z / n
    c, h = (p + Z * Z / (2 * n)) / d, Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return {"numerator": x, "denominator": n, "proportion": p, "ci": [max(0.0, c - h), min(1.0, c + h)]}


def clopper_pearson(x: int, n: int) -> dict:
    """Exact binomial interval from beta quantiles (SAP A5 per-dataset rows)."""
    lo = 0.0 if x == 0 else float(stats.beta.ppf(0.025, x, n - x + 1))
    hi = 1.0 if x == n else float(stats.beta.ppf(0.975, x + 1, n - x))
    return {"x": x, "n": n, "p": x / n, "ci_low": lo, "ci_high": hi}


def expit(z: float) -> float:
    return float(1 / (1 + math.exp(-z)))


def dl_logit(x, n) -> dict:
    """DerSimonian-Laird random effects on the logit scale (SAP A5.3a), written out: y_i = logit(p_i),
    v_i = 1/x_i + 1/(n_i - x_i) with 0.5 added to x_i and 1 to n_i for zero or full cells only;
    Q = sum w (y - y_FE)^2, C = sum w - sum w^2 / sum w, tau2 = max(0, (Q - (k-1)) / C);
    w* = 1/(v + tau2); pooled logit, SE = (sum w*)^-1/2, Wald interval; t_{k-2} prediction interval;
    I2 = max(0, (Q - (k-1)) / Q) with a Q-profile interval (Higgins-Thompson)."""
    x, n = np.asarray(x, float), np.asarray(n, float)
    cc = (x == 0) | (x == n)
    xa, na = x + 0.5 * cc, n + 1.0 * cc
    y, v = np.log(xa / (na - xa)), 1 / xa + 1 / (na - xa)
    k, w = len(y), 1 / v
    yfe = float(np.sum(w * y) / np.sum(w))
    q = float(np.sum(w * (y - yfe) ** 2))
    c = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    tau2 = max(0.0, (q - (k - 1)) / c)
    ws = 1 / (v + tau2)
    mu, se = float(np.sum(ws * y) / np.sum(ws)), float(np.sum(ws) ** -0.5)
    pi = [None, None]
    if k >= 3:
        h = float(stats.t.ppf(0.975, k - 2)) * math.sqrt(tau2 + se * se)
        pi = [expit(mu - h), expit(mu + h)]
    return {"k": k, "Q": q, "df": k - 1, "p_Q": float(stats.chi2.sf(q, k - 1)), "C": c, "tau2": tau2,
            "I2": max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0, "I2_ci": i2_qprofile(y, v, k), "logit": mu, "se": se,
            "estimate": expit(mu), "ci_low": expit(mu - Z * se), "ci_high": expit(mu + Z * se), "pi_low": pi[0], "pi_high": pi[1],
            "continuity_corrected": int(cc.sum()), "weights_re": (ws / ws.sum()).tolist(), "fixed_effect_logit": yfe,
            "estimator": "DerSimonian-Laird, logit scale (SAP A5.3a)"}


def i2_qprofile(y: np.ndarray, v: np.ndarray, k: int) -> list | None:
    """Q-profile interval for tau2 mapped to I2 = tau2 / (tau2 + s2), s2 = (k-1) sum w / (sum w^2 - sum w^2);
    the generalised Q(tau2) is solved against chi2_{k-1} quantiles with brentq. None when k < 3."""
    if k < 3:
        return None
    w = 1 / v
    s2 = (k - 1) * w.sum() / (w.sum() ** 2 - (w ** 2).sum())

    def gq(t2):
        ww = 1 / (v + t2)
        return float(np.sum(ww * (y - np.sum(ww * y) / ww.sum()) ** 2))

    def solve(target):
        if gq(0.0) <= target:
            return 0.0
        hi = 1.0
        while gq(hi) > target and hi < 1e6:
            hi *= 10
        return float(optimize.brentq(lambda t: gq(t) - target, 0.0, hi))

    lo, hi = solve(float(stats.chi2.ppf(0.975, k - 1))), solve(float(stats.chi2.ppf(0.025, k - 1)))
    return [float(lo / (lo + s2)), float(hi / (hi + s2))]


def epsilon_squared(h: float, k: int, n: int) -> float | None:
    """Kruskal-Wallis effect size (H - k + 1) / (n - k)."""
    return None if n <= k else float((h - k + 1) / (n - k))


def kruskal(groups: dict, posthoc: bool = True) -> dict:
    """Kruskal-Wallis over groups with >= 5 values. With `posthoc` (the SAP A4.3 primary stratum) the
    epsilon-squared effect size and Dunn-Holm pairs (when p < 0.05) are added; without it they are
    None and the note says the stratum is exploratory-secondary."""
    g = {k: [float(x) for x in v] for k, v in sorted(groups.items()) if len(v) >= 5}
    n = sum(len(v) for v in g.values())
    if len(g) < 2:
        return {"H": None, "p": None, "epsilon2": None, "groups": {k: len(v) for k, v in g.items()}, "note": "fewer than two groups with >= 5 values"}
    h, p = stats.kruskal(*g.values())
    out = {"H": float(h), "p": float(p), "k": len(g), "n": n, "epsilon2": epsilon_squared(float(h), len(g), n) if posthoc else None,
           "groups": {k: {"n": len(v), "median": float(np.percentile(v, 50)), "iqr": [float(np.percentile(v, 25)), float(np.percentile(v, 75))]}
                      for k, v in g.items()}, "dunn_holm": dunn_holm(g) if posthoc and p < 0.05 else None}
    if not posthoc:
        out["note"] = "exploratory-secondary stratum: epsilon2 and Dunn are computed on the annotated stratum only (SAP A4.3)"
    return out


def dunn_holm(groups: dict) -> list[dict]:
    """Dunn's z_ij = (Rbar_i - Rbar_j) / sqrt((N(N+1)/12 - sum(t^3 - t)/(12(N-1))) (1/n_i + 1/n_j)),
    two-sided normal p, Holm over all pairs."""
    names = list(groups)
    allv = np.concatenate([np.asarray(groups[k], float) for k in names])
    ranks, big_n = stats.rankdata(allv), len(allv)
    tie = sum(t ** 3 - t for t in Counter(allv.tolist()).values()) / (12 * (big_n - 1))
    means, off = {}, 0
    for k in names:
        means[k] = float(ranks[off:off + len(groups[k])].mean())
        off += len(groups[k])
    pairs = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            z = (means[a] - means[b]) / math.sqrt((big_n * (big_n + 1) / 12 - tie) * (1 / len(groups[a]) + 1 / len(groups[b])))
            pairs.append({"a": a, "b": b, "z": float(z), "p": float(2 * stats.norm.sf(abs(z)))})
    running = 0.0
    for rank, i in enumerate(sorted(range(len(pairs)), key=lambda i: pairs[i]["p"])):
        running = max(running, min(1.0, (len(pairs) - rank) * pairs[i]["p"]))
        pairs[i]["p_holm"] = running
    return pairs


def spearman_ci(x: list, y: list) -> dict:
    """Spearman rho, 95 % interval on Fisher's z with the Bonett-Wright SE sqrt((1 + rho^2/2) / (n - 3)).
    A constant input leaves rho undefined: None with a note, never NaN."""
    n = len(x)
    if n < 4:
        return {"rho": None, "p": None, "ci": None, "n": n, "note": "fewer than four pairs"}
    if len(set(x)) < 2 or len(set(y)) < 2:
        return {"rho": None, "p": None, "ci": None, "n": n, "note": "constant input; rho undefined"}
    rho, p = stats.spearmanr(x, y)
    rho = float(rho)
    se, zr = math.sqrt((1 + rho * rho / 2) / (n - 3)), math.atanh(max(-0.999999, min(0.999999, rho)))
    return {"rho": rho, "p": float(p), "ci": [math.tanh(zr - Z * se), math.tanh(zr + Z * se)], "n": n}


def trend_test(counts: list[list[int]]) -> dict | None:
    """Linear-by-linear association over year bands (SAP A3.5), equivalent to Cochran-Armitage for 2 x k."""
    from statsmodels.stats.contingency_tables import Table
    arr = np.asarray(counts)
    if arr.shape[1] < 2 or arr.sum() == 0 or (arr.sum(axis=0) == 0).any():
        return None
    r = Table(arr).test_ordinal_association(row_scores=np.array([0, 1]), col_scores=np.arange(1, arr.shape[1] + 1))
    return {"statistic": float(r.statistic), "p": float(r.pvalue), "zscore": float(r.zscore)}


def selftest() -> list[str]:
    """DL against statsmodels on a heterogeneous three-study example (1e-6); Wilson and Clopper-Pearson
    on a hand-computed cell (7/20); epsilon-squared on a hand value; the constant-input rule of
    spearman_ci. Returns the list of failed checks (empty when all hold) and prints one line."""
    from statsmodels.stats.meta_analysis import combine_effects
    fails = []
    x, n = np.array([5, 40, 30]), np.array([100, 150, 400])
    r, sm = dl_logit(x, n), combine_effects(np.log(x / (n - x)), 1 / x + 1 / (n - x), method_re="dl")
    if not (abs(max(0.0, sm.tau2) - r["tau2"]) < 1e-6 and abs(sm.mean_effect_re - r["logit"]) < 1e-6 and abs(sm.sd_eff_w_re - r["se"]) < 1e-6):
        fails.append("DL vs statsmodels")
    w, cp = wilson(7, 20), clopper_pearson(7, 20)
    if not (abs(w["ci"][0] - 0.1812) < 5e-4 and abs(w["ci"][1] - 0.5671) < 5e-4):      # p = 0.35, n = 20, z = 1.96 by hand
        fails.append("Wilson 7/20")
    if not (abs(cp["ci_low"] - 0.1539) < 5e-4 and abs(cp["ci_high"] - 0.5922) < 5e-4):
        fails.append("Clopper-Pearson 7/20")
    if abs(epsilon_squared(6.2, 3, 30) - (6.2 - 2) / 27) >= 1e-12:
        fails.append("epsilon2")
    if spearman_ci([1, 1, 1, 1], [1, 2, 3, 4])["rho"] is not None or "note" not in spearman_ci([1, 1, 1, 1], [1, 2, 3, 4]):
        fails.append("spearman constant input -> None")
    if kruskal({"a": [1, 2, 3, 4, 5], "b": [3, 4, 5, 6, 7]}, posthoc=False)["epsilon2"] is not None:
        fails.append("kruskal posthoc=False -> no epsilon2")
    print("estimators selftest (DL vs statsmodels, Wilson, Clopper-Pearson, epsilon2, spearman, kruskal):",
          "ok" if not fails else "FAIL " + ", ".join(fails),
          f"(tau2 {r['tau2']:.6f} vs {sm.tau2:.6f}; I2 {r['I2']:.3f}, I2 CI {[round(c, 3) for c in r['I2_ci']]})")
    return fails


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sdr.estimators", description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true", help="check every formula against a published or library value")
    a = ap.parse_args(argv)
    if not a.selftest:
        ap.print_help()
        return 2
    return 1 if selftest() else 0


if __name__ == "__main__":
    sys.exit(main())
