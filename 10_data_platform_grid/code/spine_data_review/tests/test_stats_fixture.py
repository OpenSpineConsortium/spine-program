"""Hand calculation of the SAP estimators on a tiny fixture, checked against sdr.stats.

WHY. `sdr.stats --selftest` compares DerSimonian-Laird against statsmodels, which is an
independent implementation but not a hand calculation: both could agree on a wrong convention
(continuity correction, the C term, the prediction-interval df). This test writes every step of
the arithmetic out in plain floats from tests/fixture_meta.json and compares the result to
`dl_logit`, `wilson`, `clopper_pearson`, `spearman_ci` and `epsilon_squared`. It is
deliberately naive (loops, math module, no numpy) so it cannot share a bug with the module.

Run from spine_data_review/:  ~/sdr_venv/bin/python tests/test_stats_fixture.py
Exit 0 on agreement (1e-9 for the closed forms, 1e-6 for the interval mapped through expit).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdr import stats as S  # noqa: E402

FIX = Path(__file__).with_name("fixture_meta.json")
Z = 1.959964


def expit(z):
    return 1 / (1 + math.exp(-z))


def hand_dl(x, n):
    """DL on the logit scale, step by step (Higgins & Thompson notation)."""
    y, v = [], []
    for xi, ni in zip(x, n):
        cc = xi == 0 or xi == ni
        xa, na = xi + (0.5 if cc else 0), ni + (1 if cc else 0)
        y.append(math.log(xa / (na - xa)))
        v.append(1 / xa + 1 / (na - xa))
    k = len(y)
    w = [1 / vi for vi in v]
    sw = sum(w)
    yfe = sum(wi * yi for wi, yi in zip(w, y)) / sw
    q = sum(wi * (yi - yfe) ** 2 for wi, yi in zip(w, y))
    c = sw - sum(wi * wi for wi in w) / sw
    tau2 = max(0.0, (q - (k - 1)) / c)
    ws = [1 / (vi + tau2) for vi in v]
    mu = sum(wi * yi for wi, yi in zip(ws, y)) / sum(ws)
    se = 1 / math.sqrt(sum(ws))
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0
    return {"tau2": tau2, "logit": mu, "se": se, "Q": q, "I2": i2, "estimate": expit(mu),
            "ci_low": expit(mu - Z * se), "ci_high": expit(mu + Z * se), "fixed_effect_logit": yfe}


def hand_wilson(x, n):
    p = x / n
    z2 = Z * Z
    centre = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = Z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return centre - half, centre + half


def hand_spearman(x, y):
    """No ties in the fixture, so rho = 1 - 6 sum d^2 / (n (n^2 - 1))."""
    def ranks(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0] * len(a)
        for rank, i in enumerate(order, 1):
            r[i] = rank
        return r
    rx, ry = ranks(x), ranks(y)
    n = len(x)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n * n - 1))


def main() -> int:
    fx = json.loads(FIX.read_text(encoding="utf-8"))
    bad = []

    def eq(name, a, b, tol):
        if a is None or b is None or abs(a - b) > tol:
            bad.append(f"{name}: hand {a} vs module {b}")

    for case in fx["dl"]:
        h, m = hand_dl(case["x"], case["n"]), S.dl_logit(case["x"], case["n"])
        for key in ("tau2", "logit", "se", "Q", "I2", "fixed_effect_logit"):
            eq(f"dl[{case['name']}].{key}", h[key], m[key], 1e-9)
        for key in ("estimate", "ci_low", "ci_high"):
            eq(f"dl[{case['name']}].{key}", h[key], m[key], 1e-6)
        if "expected_tau2" in case:      # the value typed from the arithmetic done on paper
            eq(f"dl[{case['name']}].tau2_paper", case["expected_tau2"], m["tau2"], 1e-6)
        if "expected_estimate" in case:
            eq(f"dl[{case['name']}].estimate_paper", case["expected_estimate"], m["estimate"], 1e-6)
        # the prediction interval uses t_{k-2}: recompute with scipy only for the quantile
        if m["k"] >= 3:
            from scipy.stats import t
            hh = t.ppf(0.975, m["k"] - 2) * math.sqrt(h["tau2"] + h["se"] ** 2)
            eq(f"dl[{case['name']}].pi_low", expit(h["logit"] - hh), m["pi_low"], 1e-6)
            eq(f"dl[{case['name']}].pi_high", expit(h["logit"] + hh), m["pi_high"], 1e-6)

    for case in fx["wilson"]:
        lo, hi = hand_wilson(case["x"], case["n"])
        m = S.wilson(case["x"], case["n"])
        eq(f"wilson[{case['x']}/{case['n']}].lo", max(0.0, lo), m["ci"][0], 1e-9)
        eq(f"wilson[{case['x']}/{case['n']}].hi", min(1.0, hi), m["ci"][1], 1e-9)
        eq(f"wilson[{case['x']}/{case['n']}].lo_paper", case["lo"], m["ci"][0], 5e-4)
        eq(f"wilson[{case['x']}/{case['n']}].hi_paper", case["hi"], m["ci"][1], 5e-4)

    for case in fx["clopper_pearson"]:
        m = S.clopper_pearson(case["x"], case["n"])
        eq(f"cp[{case['x']}/{case['n']}].lo_paper", case["lo"], m["ci_low"], 5e-4)
        eq(f"cp[{case['x']}/{case['n']}].hi_paper", case["hi"], m["ci_high"], 5e-4)

    for case in fx["spearman"]:
        m = S.spearman_ci(case["x"], case["y"])
        eq("spearman.rho", hand_spearman(case["x"], case["y"]), m.get("rho"), 1e-9)
        eq("spearman.rho_paper", case["rho"], m.get("rho"), 1e-9)

    for case in fx["epsilon2"]:
        eq("epsilon2", (case["h"] - case["k"] + 1) / (case["n"] - case["k"]), S.epsilon_squared(case["h"], case["k"], case["n"]), 1e-12)
        eq("epsilon2_paper", case["value"], S.epsilon_squared(case["h"], case["k"], case["n"]), 1e-9)

    print("stats fixture:", "ok" if not bad else "FAIL")
    for b in bad:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
