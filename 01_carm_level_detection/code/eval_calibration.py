#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/eval_calibration.py [tracked at 097933a]
"""Does the number on the screen mean what it says? Calibration, selective prediction and set-valued prediction
for the level model and for the detector.

A surgeon does not act on an accuracy, they act on ONE named level with a confidence beside it. Two different
questions hide behind that confidence and this project has so far answered neither:

  CALIBRATION   when the model writes 0.90, is it right 90 % of the time? The only evidence on hand says no,
                and says it in the worst place: ~/selective/SELECTIVE.md reports T13 at mean top posterior
                0.804 and 0 % accuracy (n = 11), T9 at 0.625 and 46 %. A selective or conformal guarantee is
                read AGAINST the calibration, so it is measured first, per band length and per class.
  SELECTION     when it abstains, does what remains get better, and by how much? tools/level_selective.py
                already answers this on a crop bank with a pure-softmax rule. It is not enough for the paper:
                (a) it runs on the plain-film bank, not on the intraoperative C-arm frames the manuscript
                reports; (b) the SHIPPED abstain rule is not the rule it studies -- level_prototype.py abstains
                when `decoded != single OR prob < 0.5`, a TWO-term rule whose terms have never been separated;
                (c) it reports no interval on any coverage, and (d) its conformal section reports set sizes but
                never the empirical coverage, which is the one number that says whether the guarantee held.

WHAT THIS ADDS, AND THE TRAPS IT IS BUILT AROUND.

  ECE is not a number, it is a number PLUS a binning rule, and a small ECE can be pure finite-sample noise.
  Both binnings are reported (equal-mass, stated as the primary; equal-width beside it) and every ECE is given
  with a case-cluster bootstrap interval AND with a NULL: the ECE that a perfectly calibrated model of this
  size would show by chance, simulated by drawing correctness from the model's own confidences. An observed
  ECE below its null is not evidence of miscalibration, and this reports the share of null draws at or above
  the observed value as a p-value. That is the "check against something outside the computation" rule applied
  to a statistic that otherwise always looks non-zero.

  A threshold chosen on the test set is not a held-out number. Every recalibration (temperature, Platt,
  isotonic) and every conformal quantile here is fit on CALIBRATION CASES and applied unchanged to TEST CASES,
  split by case and never by vertebra, because two crops from one spine are not independent.

  A coverage figure with no interval cannot be distinguished from its neighbour. Every coverage, accuracy and
  set size carries a 2,000-resample case-cluster bootstrap interval (numpy default_rng, percentile method),
  the same convention as tools/carmlspine_pool_scores.py and tools/or_recall_curves.py.

  For the detector, confidence is a claim about a BOX: "0.25" should mean one box in four at that confidence is
  a real vertebra. docs/PHYSICS_LINKING.md records that 0.25 is miscalibrated; this quantifies it per device as
  the signed gap between the mean confidence of the kept boxes and their precision, with an interval.

WHAT IT CANNOT DO WITH WHAT IS ON DISK. The C-ArmLSpine score files (tools/carmlspine_eval.py) keep only the
TOP-1 probability per vertebra, not the 27-vector. Full conformal SETS therefore cannot be built from them;
what can be built, and is, is a distribution-free SELECTIVE risk guarantee (a threshold whose selective error
rate is bounded at a stated confidence), which needs only the top-1 score. The set-valued analysis runs on a
posteriors jsonl (tools/level_posteriors.py) where the whole vector exists. The report says which it used.

  A per-item guarantee is not a guarantee when the items arrive nine to a case. The distribution-free selective
  rule below is chosen at the EFFECTIVE sample size, and the correction is not cosmetic: on the pooled
  band-length data the uncorrected rule missed its own target out of sample (5.91 % realised against a 5 %
  promise, 11.99 % against 10 %) and the corrected one holds (3.94 % and 9.21 %), with design effects of 3.8
  and 6.3. Every result file records the design effect it used.

    python tools/eval_calibration.py selftest
    python tools/eval_calibration.py report --result ~/calibration/carm/calibration_level.json   # md + figure
    python tools/eval_calibration.py level --scores '/rs/.../carmlspine/proto/cv_fold*/det_score_k*.json' \
        --out ~/calibration/carm
    python tools/eval_calibration.py level --posteriors ~/selective/post_val.jsonl --out ~/calibration/bank
    python tools/eval_calibration.py detector --sweeps '/rs/.../or_ready/lodo/sweeps/*.json' \
        --out ~/calibration/detector
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from level_selective import REGION, clopper_pearson_lower  # noqa: E402  (one region DAG, not two)

BOOT = 2000
SEED = 20260922
NBINS = 15
MACRO_MIN_N = 5      # a class with fewer items than this cannot carry a macro (balanced) average
AUC_MIN_N = 5        # a rank AUC needs this many of BOTH classes before it means anything

# dataviz reference palette
INK, INK2, GRID_C, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]


def code_sha():
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=str(HERE.parent)).decode().strip()
    except Exception:  # noqa: BLE001
        return None


def clopper_pearson_upper(k, n, alpha=0.05):
    """One-sided upper bound on a proportion, exact. k failures out of n."""
    if n == 0:
        return 1.0
    if k == 0:
        return 1.0 - alpha ** (1.0 / n)
    try:
        from scipy.stats import beta
        return float(beta.ppf(1.0 - alpha, k + 1, n - k)) if k < n else 1.0
    except Exception:  # noqa: BLE001
        p = k / n
        se = math.sqrt(max(p * (1 - p), 1e-12) / n)
        return min(1.0, p + 1.645 * se)


# ------------------------------------------------------------------------------------------------- calibration core
def ece_bins(conf, correct, n_bins=NBINS, scheme="equal_mass"):
    """Expected calibration error with its binning rule stated in the output.

    equal_mass  sort by confidence, cut the sorted order into n_bins contiguous blocks of as near equal size as
                the count allows (ties fall where the sort puts them). No bin is empty, so no bin's mean is
                undefined, which is the failure mode of equal-width binning on a model whose confidences pile
                up near 1.
    equal_width n_bins bins of width 1/n_bins on [0,1]; empty bins contribute nothing and are reported as such.

    Returns (ece, mce, rows). ece = sum_b (n_b/n) |mean conf_b - mean correct_b|; mce = the largest such gap.
    """
    conf = np.asarray(conf, float)
    corr = np.asarray(correct, float)
    n = len(conf)
    if n == 0:
        return None, None, []
    if scheme == "equal_mass":
        order = np.argsort(conf, kind="mergesort")
        cut = np.linspace(0, n, min(n_bins, n) + 1).astype(int)
        groups = [order[cut[i]:cut[i + 1]] for i in range(len(cut) - 1) if cut[i + 1] > cut[i]]
    elif scheme == "equal_width":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
        idx = np.clip(np.digitize(conf, edges[1:-1], right=False), 0, n_bins - 1)
        groups = [np.flatnonzero(idx == b) for b in range(n_bins)]
    else:
        raise ValueError(scheme)
    ece = 0.0
    mce = 0.0
    rows = []
    for g in groups:
        if len(g) == 0:
            continue
        c = float(conf[g].mean())
        a = float(corr[g].mean())
        w = len(g) / n
        ece += w * abs(c - a)
        mce = max(mce, abs(c - a))
        rows.append(dict(n=int(len(g)), conf=c, accuracy=a, gap=c - a,
                         lo=float(conf[g].min()), hi=float(conf[g].max())))
    return float(ece), float(mce), rows


def brier_decomposition(conf, correct, rows):
    """Binary Brier score on `top-1 is correct`, and the Murphy decomposition over the same bins as the ECE.
    brier = reliability - resolution + uncertainty. Reliability is the calibration term (lower is better),
    resolution is how much the confidences separate easy from hard (higher is better)."""
    conf = np.asarray(conf, float)
    corr = np.asarray(correct, float)
    n = len(conf)
    if n == 0:
        return None
    base = float(corr.mean())
    brier = float(np.mean((conf - corr) ** 2))
    rel = sum((r["n"] / n) * (r["conf"] - r["accuracy"]) ** 2 for r in rows)
    res = sum((r["n"] / n) * (r["accuracy"] - base) ** 2 for r in rows)
    unc = base * (1 - base)
    return dict(brier=brier, reliability=float(rel), resolution=float(res), uncertainty=float(unc),
                base_rate=base, check_sum=float(rel - res + unc))


def ece_null(conf, n_draws=500, n_bins=NBINS, scheme="equal_mass", seed=SEED):
    """The ECE a PERFECTLY calibrated model with these confidences would show at this sample size, by drawing
    correctness ~ Bernoulli(conf). Without this a 0.02 ECE reads as miscalibration when it is arithmetic."""
    conf = np.asarray(conf, float)
    if len(conf) == 0:
        return None
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_draws):
        y = (rng.random(len(conf)) < conf).astype(float)
        e, _, _ = ece_bins(conf, y, n_bins, scheme)
        vals.append(e)
    v = np.asarray(vals, float)
    return dict(mean=float(v.mean()), p95=float(np.percentile(v, 95)), draws=int(n_draws))


def boot_cases(cases, items, fn, n=None, seed=SEED):
    """Case-cluster bootstrap of fn(list of items) -> float|None. `cases` is the per-item case key."""
    n = int(n or BOOT)
    by = collections.defaultdict(list)
    for c, it in zip(cases, items):
        by[c].append(it)
    keys = sorted(by)
    if len(keys) < 2:
        return [None, None]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        pick = rng.integers(0, len(keys), len(keys))
        v = fn([x for i in pick for x in by[keys[i]]])
        if v is not None and np.isfinite(v):
            vals.append(float(v))
    if not vals:
        return [None, None]
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


# ------------------------------------------------------------------------------------------------- recalibration
def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -60, 60)))


def platt_fit(conf, correct, ridge=1e-6, iters=200):
    """Two-parameter logistic recalibration of a confidence.

    Damped Newton with a backtracking line search, not plain IRLS. Plain IRLS diverges here and the selftest
    caught it: where the confidences saturate near 1 the Fisher information collapses, the Newton step is the
    gradient divided by the ridge alone, and the coefficients ran to 2.7e7 -- producing a recalibration that
    made the ECE WORSE while returning finite, ordinary-looking numbers. Exactly the failure this repo keeps
    meeting, in a twenty-line helper.
    """
    p = np.clip(np.asarray(conf, float), 1e-6, 1 - 1e-6)
    x = np.log(p / (1 - p))
    X = np.stack([x, np.ones_like(x)], 1)
    y = np.asarray(correct, float)
    n = max(len(y), 1)

    def obj(v):
        z = np.clip(X @ v, -60, 60)
        return float(np.mean(np.logaddexp(0.0, z) - y * z)) + 0.5 * ridge * float(v @ v)

    w = np.zeros(2)
    f = obj(w)
    for _ in range(iters):
        q = _sigmoid(X @ w)
        W = np.clip(q * (1 - q), 1e-8, None)
        g = X.T @ (y - q) / n - ridge * w
        H = (X * W[:, None]).T @ X / n + (ridge + 1e-8) * np.eye(2)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        t, moved = 1.0, False
        for _ in range(50):
            w2 = w + t * step
            f2 = obj(w2)
            if f2 <= f - 1e-14:
                moved = True
                break
            t *= 0.5
        if not moved:
            break
        done = abs(f - f2) < 1e-13
        w, f = w2, f2
        if done:
            break
    return w


def platt_apply(w, conf):
    p = np.clip(np.asarray(conf, float), 1e-6, 1 - 1e-6)
    return _sigmoid(w[0] * np.log(p / (1 - p)) + w[1])


def isotonic_fit(conf, correct):
    """Pool-adjacent-violators. Returns (x, y) knots of a non-decreasing step function."""
    o = np.argsort(np.asarray(conf, float), kind="mergesort")
    x = np.asarray(conf, float)[o]
    y = np.asarray(correct, float)[o]
    val = list(y)
    wt = [1.0] * len(y)
    idx = list(range(len(y)))
    i = 0
    while i < len(val) - 1:
        if val[i] <= val[i + 1] + 1e-12:
            i += 1
            continue
        nw = wt[i] + wt[i + 1]
        nv = (val[i] * wt[i] + val[i + 1] * wt[i + 1]) / nw
        val[i:i + 2] = [nv]
        wt[i:i + 2] = [nw]
        idx[i:i + 2] = [idx[i]]
        if i > 0:
            i -= 1
    xs, ys = [], []
    k = 0
    for v, w_ in zip(val, wt):
        k += int(round(w_))
        xs.append(float(x[min(k - 1, len(x) - 1)]))
        ys.append(float(v))
    return np.asarray(xs), np.asarray(ys)


def isotonic_apply(knots, conf):
    xs, ys = knots
    if len(xs) == 0:
        return np.asarray(conf, float)
    return np.interp(np.asarray(conf, float), xs, ys, left=ys[0], right=ys[-1])


def temperature_fit(logp, y_idx, lo=-3.0, hi=3.0, iters=80):
    """Temperature scaling on log-probabilities (softmax(log p / T) recovers the original at T = 1). Golden
    section on log T against the NLL, so no optimiser dependency."""
    logp = np.asarray(logp, float)
    y_idx = np.asarray(y_idx, int)

    def nll(t):
        z = logp / t
        z = z - z.max(1, keepdims=True)
        return float(np.mean(-(z[np.arange(len(y_idx)), y_idx] - np.log(np.exp(z).sum(1)))))

    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = nll(math.exp(c)), nll(math.exp(d))
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = nll(math.exp(c))
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = nll(math.exp(d))
    t = math.exp((a + b) / 2)
    return float(t), nll(t), nll(1.0)


def temperature_apply(logp, t):
    z = np.asarray(logp, float) / t
    z = z - z.max(1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(1, keepdims=True)


# ------------------------------------------------------------------------------------------------- selective
def rc_curve(conf, correct):
    """Risk-coverage by walking the confidence threshold down. Returns coverage, selective accuracy, AUGRC.

    `implementable` marks the prefixes a real threshold can actually produce. The scores here are rounded to
    three decimals, so hundreds of vertebrae share a confidence; a prefix that stops in the middle of a tied
    block corresponds to no rule at all -- you cannot answer half the vertebrae that scored 0.900. Reading the
    best coverage off every prefix therefore reports an operating point that cannot be shipped, and it reports
    it optimistically, because the scan is free to stop just after the correct members of a tied block. Every
    coverage and threshold below is taken at a tie boundary only.
    """
    cf = np.asarray(conf, float)
    o = np.argsort(-cf, kind="mergesort")
    c = np.asarray(correct, bool)[o]
    s = cf[o]
    n = len(c)
    cov = np.arange(1, n + 1) / n
    acc = np.cumsum(c) / np.arange(1, n + 1)
    impl = np.ones(n, bool)
    if n > 1:
        impl[:-1] = s[:-1] > s[1:]
    return dict(coverage=cov, accuracy=acc, risk=1.0 - acc, sorted_conf=s, implementable=impl,
                augrc=float(np.mean((1.0 - acc) * cov)), order=o)


def acc_at_coverage(conf, correct, target_cov, bound=True):
    """The selective accuracy when the rule answers the `target_cov` most confident share. The question the task
    asks in the direction a product manager asks it: we must answer 95 % of them, how good is it then?

    Only a threshold that lands on a tie boundary is a rule, so the reported coverage is the largest
    implementable one at or below the target, and it is reported rather than assumed to equal the target."""
    cur = rc_curve(conf, correct)
    n = len(cur["accuracy"])
    if n == 0:
        return None
    want = min(n - 1, max(0, int(math.ceil(target_cov * n)) - 1))
    cand = np.flatnonzero(cur["implementable"][:want + 1])
    i = int(cand[-1]) if len(cand) else int(np.flatnonzero(cur["implementable"])[0])
    k = int(round(cur["accuracy"][i] * (i + 1)))
    return dict(coverage=float(cur["coverage"][i]), accuracy=float(cur["accuracy"][i]), n_answered=int(i + 1),
                target_coverage=float(target_cov), threshold=float(cur["sorted_conf"][i]),
                lower95=clopper_pearson_lower(k, i + 1) if bound else None)


def coverage_at_accuracy(conf, correct, target_acc, n_min=30, bound=True):
    """The largest coverage whose selective accuracy still reaches the target.

    The exact lower bound is computed ONCE, on the chosen point. Computing it inside the scan called scipy's
    beta.ppf a thousand times per bootstrap resample and turned a two-second statistic into a two-minute one.
    """
    cur = rc_curve(conf, correct)
    acc, cov = cur["accuracy"], cur["coverage"]
    start = min(n_min, len(acc)) - 1
    if start < 0:
        return None
    ok = (acc >= target_acc) & cur["implementable"]
    ok[:start] = False
    hits = np.flatnonzero(ok)
    if len(hits) == 0:
        return None
    i = int(hits[-1])
    k = int(round(acc[i] * (i + 1)))
    return dict(coverage=float(cov[i]), accuracy=float(acc[i]), n_answered=int(i + 1),
                threshold=float(cur["sorted_conf"][i]),
                lower95=clopper_pearson_lower(k, i + 1) if bound else None)


def design_effect(conf, ok, cases, t, boot=400, seed=SEED):
    """How much wider the selective risk's sampling distribution is than a binomial of the same size, because a
    case contributes several vertebrae and they fail together. var_cluster / var_binomial, floored at 1.

    This is the correction the first version of this function lacked, and the lack was visible: on the pooled
    band-length data an exact Clopper-Pearson bound built per VERTEBRA chose a threshold whose realised error on
    the held-out cases was 5.91 % against a 5 % target and 11.99 % against 10 %. An exact bound that fails out of
    sample is not a bound; the unit of exchangeability here is the case, not the vertebra.
    """
    m = conf >= t
    n = int(m.sum())
    if n < 2:
        return 1.0
    risk = float((~ok[m]).mean())
    var_bin = max(risk * (1 - risk) / n, 1e-12)
    by = collections.defaultdict(list)
    for c, a, o in zip(cases, m, ok):
        by[c].append((bool(a), bool(o)))
    keys = sorted(by)
    if len(keys) < 2:
        return 1.0
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(boot):
        pick = rng.integers(0, len(keys), len(keys))
        num = den = 0
        for i in pick:
            for a, o in by[keys[i]]:
                if a:
                    den += 1
                    num += (not o)
        if den:
            vals.append(num / den)
    if len(vals) < 20:
        return 1.0
    return float(max(1.0, np.var(vals, ddof=1) / var_bin))


def selective_risk_control(cal, test, alpha, delta=0.05, grid=None, n_min=20,
                           cal_cases=None, test_cases=None, cluster=True):
    """A distribution-free bound where only the top-1 score exists, so conformal SETS cannot be formed.

    Learn-then-Test over a PRE-STATED grid of thresholds (0.00 to 1.00 in steps of 0.01, 101 of them). At each
    threshold the selective error rate is bounded above by an exact Clopper-Pearson bound at level delta/101
    (Bonferroni over the grid, so the family-wise error is at most delta); the threshold kept is the LOWEST one
    whose bound still clears alpha, which is the one that answers most often. The realised risk and coverage are
    then reported on the TEST cases, which the calibration never saw.

    Why a Bonferroni grid and not a fixed sequence down the observed scores: the selftest showed that a fixed
    sequence starting at the single most confident item can never reject (an exact bound on one observation is
    0.95) and so stops at the first step, returning nothing for every alpha. A number that is always "not
    reached" is not a conservative answer, it is a broken one.

    Why the design effect: vertebrae are not independent draws, they arrive nine to a case and fail together, so
    the binomial bound is anti-conservative by exactly the factor `design_effect` measures. With `cluster=True`
    the exact bound is evaluated at the EFFECTIVE sample size n/deff, which is the standard survey correction;
    the uncorrected bound is reported beside it so the size of the correction is visible rather than assumed.

    cal/test are lists of (conf, correct); cal_cases/test_cases are the matching case keys.
    """
    if not cal or not test:
        return dict(alpha=alpha, delta=delta, threshold=None,
                    note=f"the split by cluster left {len(cal)} calibration and {len(test)} test items, so no "
                         f"rule can be chosen on one half and checked on the other; a source with a single "
                         f"case cannot carry a held-out risk bound at all")
    if grid is None:
        grid = np.round(np.arange(0.0, 1.0001, 0.01), 3)
    G = len(grid)
    cc = np.asarray([c for c, _ in cal], float)
    ok = np.asarray([bool(o) for _, o in cal])
    use_cluster = bool(cluster and cal_cases is not None and len(set(cal_cases)) > 1)
    chosen = chosen_naive = None
    deff = 1.0
    for t in grid:  # ascending: the first that passes is the most permissive
        m = cc >= t
        n = int(m.sum())
        if n < n_min:
            continue
        k = int((~ok[m]).sum())
        raw = clopper_pearson_upper(k, n, delta / G)
        if raw > alpha:
            continue
        if chosen_naive is None:
            chosen_naive = float(t)
        if not use_cluster:
            chosen = float(t)
            break
        d = design_effect(cc, ok, cal_cases, t)
        if clopper_pearson_upper(k / d, n / d, delta / G) <= alpha:
            chosen, deff = float(t), d
            break
    if chosen is None:
        return dict(alpha=alpha, delta=delta, threshold=None, grid=G, n_min=n_min,
                    clustered=use_cluster, threshold_uncorrected=chosen_naive,
                    note=f"no threshold on the {G}-point grid bounds the selective error at alpha={alpha} "
                         f"with {len(cal)} calibration items"
                         + ("" if chosen_naive is None else
                            f" once the case clustering is accounted for; ignoring it would have chosen "
                            f"{chosen_naive:.3f}, which is the anti-conservative answer"))
    tc = np.asarray([c for c, _ in test], float)
    to = np.asarray([bool(o) for _, o in test])
    m = tc >= chosen
    n = int(m.sum())
    d_test = design_effect(tc, to, test_cases, chosen) if (test_cases is not None and n) else 1.0
    return dict(alpha=alpha, delta=delta, threshold=chosen, grid=G, n_min=n_min, clustered=use_cluster,
                design_effect=deff, threshold_uncorrected=chosen_naive,
                correction=(f"Bonferroni over {G} pre-stated thresholds, exact Clopper-Pearson at delta/{G}"
                            + (f", evaluated at the effective sample size n/{deff:.2f} (case clustering)"
                               if use_cluster else "")),
                cal_answered=int((cc >= chosen).sum()), cal_n=len(cal),
                test_coverage=(n / len(test)) if test else None, test_answered=n, test_n=len(test),
                test_risk=(float((~to[m]).mean()) if n else None),
                test_risk_upper95=(clopper_pearson_upper(int((~to[m]).sum()) / d_test, n / d_test, delta)
                                   if n else None),
                held=bool(n and float((~to[m]).mean()) <= alpha))


# ------------------------------------------------------------------------------------------------- conformal sets
def conformal_sets(cal_probs, cal_true, test_probs, order, alpha, method="lac", mondrian=False):
    """Split conformal over the class axis. Returns per-test-item the kept class names.

    lac   score = 1 - p[true]; the smallest set that keeps every class whose complement clears the quantile.
          Smallest average size, but coverage is spread unevenly over classes.
    aps   score = the cumulative probability down the sorted vector to and including the true class
          (non-randomised, so the guarantee is conservative). Sets adapt to how flat the posterior is.
    mondrian applies the quantile of the TRUE class to each candidate class, giving class-conditional coverage
          where a class has enough calibration examples; classes with fewer than ceil(1/alpha)-1 examples cannot
          have a finite quantile and are reported rather than silently given one.
    """
    K = len(order)
    idx = {n: i for i, n in enumerate(order)}
    cal_probs = np.asarray(cal_probs, float)
    test_probs = np.asarray(test_probs, float)
    ti = np.asarray([idx[t] for t in cal_true], int)

    if method == "lac":
        s = 1.0 - cal_probs[np.arange(len(ti)), ti]
    elif method == "aps":
        o = np.argsort(-cal_probs, 1, kind="mergesort")
        cs = np.take_along_axis(np.cumsum(np.take_along_axis(cal_probs, o, 1), 1),
                                np.argsort(o, 1, kind="mergesort"), 1)
        s = cs[np.arange(len(ti)), ti]
    else:
        raise ValueError(method)

    def q_of(scores):
        n = len(scores)
        if n == 0:
            return None
        lvl = math.ceil((n + 1) * (1 - alpha)) / n
        if lvl > 1.0:
            return None
        return float(np.quantile(scores, lvl, method="higher"))

    thin = []
    if mondrian:
        qs = {}
        for k in range(K):
            m = ti == k
            if m.sum() == 0:
                continue
            q = q_of(s[m])
            if q is None:
                thin.append(dict(level=order[k], n=int(m.sum()),
                                 need=int(math.ceil(1 / alpha) - 1)))
            qs[k] = q
        default = q_of(s)
        qvec = np.array([qs.get(k) if qs.get(k) is not None else (default if default is not None else 1.0)
                         for k in range(K)], float)
    else:
        q = q_of(s)
        qvec = np.full(K, q if q is not None else 1.0, float)

    sets = []
    for row in test_probs:
        if method == "lac":
            keep = [order[k] for k in range(K) if (1.0 - row[k]) <= qvec[k]]
        else:
            o = np.argsort(-row, kind="mergesort")
            cum = np.cumsum(row[o])
            keep = []
            for r, k in enumerate(o):
                keep.append(order[k])
                if cum[r] >= qvec[k]:
                    break
        if not keep:
            keep = [order[int(row.argmax())]]
        sets.append(keep)
    return sets, qvec, thin


def set_stats(sets, truths):
    """Coverage IS the number that says whether the guarantee held. Reported first, then the cost of it."""
    n = len(sets)
    if n == 0:
        return None
    cov = float(np.mean([t in s for s, t in zip(sets, truths)]))
    size = float(np.mean([len(s) for s in sets]))
    single = [i for i, s in enumerate(sets) if len(s) == 1]
    single_ok = float(np.mean([sets[i][0] == truths[i] for i in single])) if single else None
    onereg = [i for i, s in enumerate(sets) if len({REGION.get(x, "?") for x in s}) == 1]
    onereg_ok = (float(np.mean([REGION.get(truths[i], "?") in {REGION.get(x, "?") for x in sets[i]}
                                for i in onereg])) if onereg else None)
    return dict(empirical_coverage=cov, mean_set_size=size, median_set_size=float(np.median([len(s) for s in sets])),
                singleton_rate=len(single) / n, singleton_accuracy=single_ok,
                one_region_rate=len(onereg) / n, one_region_accuracy=onereg_ok, n=n)


# ------------------------------------------------------------------------------------------------- readers
def read_carm_scores(patterns):
    """tools/carmlspine_eval.py score files. One row per matched vertebra:
    conf = the level model's top posterior, correct = the exact-level flag, plus the pieces of the SHIPPED
    two-term abstain rule (prob < 0.5 OR decoded != single-crop call) so the terms can be separated."""
    rows = []
    files = []
    for pat in patterns:
        files += sorted(glob.glob(os.path.expanduser(pat)))
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        tag = d.get("tag", "")
        fold = Path(f).parent.name
        boxes = "oracle" if "oracle" in Path(f).name else "det"
        m = re.search(r"_k(full|\d+)\.json$", Path(f).name)
        k = m.group(1) if m else "?"
        for r in d.get("frames", []):
            for it in r.get("items", []):
                p = it.get("prob")
                if p is None:
                    continue
                rows.append(dict(conf=float(p), correct=bool(it.get("exact")), within1=bool(it.get("within1")),
                                 region_ok=bool(it.get("region")), truth=it.get("truth"), call=it.get("call"),
                                 single=it.get("single"), single_exact=bool(it.get("single_exact")),
                                 abstain=bool(it.get("abstain")), case=str(r.get("case")), view=r.get("view"),
                                 k=k, boxes=boxes, fold=fold, tag=tag, file=f))
    return rows, files


def read_posteriors(path):
    """tools/level_posteriors.py jsonl: the full 27-vector, which is what set-valued prediction needs."""
    rows = []
    order = None
    for line in open(os.path.expanduser(path), encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except Exception:  # noqa: BLE001
            continue
        if r.get("level_order"):
            order = r["level_order"]
        if r.get("probs") and r.get("true"):
            rows.append(r)
    if order is None and rows:
        order = sorted({r["true"] for r in rows})
    return rows, order


def cluster_key_of(r):
    """The unit that must not straddle the calibration/test split, and the unit the bootstrap resamples.

    In a posteriors dump `case` is the RENDER name -- one pose of one view of one CT -- and `group` is the CT
    subject behind it (tools/diag_level_model.group_of: ctsp_0001_ap_p3 -> 0001). Clustering on `case` therefore
    treats 24 renders of one spine as 24 independent spines: measured on ~/selective/post_val.jsonl, 16,392
    vertebrae carry 2,927 `case` names but only 1,960 subjects, and a 50/50 split by `case` puts renders of 217
    subjects on BOTH sides -- 37.2 % of the test vertebrae have another render of the same spine in the
    calibration half. Every interval built on `case` is then a render-cluster interval sold as a case-cluster
    one, and every conformal quantile is fitted partly on the spines it is tested on. Prefer `group`.
    """
    g = r.get("group")
    if g:
        return str(g), "group"
    return str(r.get("case")), "case"


def split_by_case(cases, frac, seed=SEED):
    ks = sorted(set(cases))
    rng = np.random.default_rng(seed)
    rng.shuffle(ks)
    n = int(len(ks) * frac)
    return set(ks[:n]), set(ks[n:])


# ------------------------------------------------------------------------------------------------- level command
def calib_block(conf, correct, cases, label, n_bins=NBINS, nulls=500):
    conf = np.asarray(conf, float)
    correct = np.asarray(correct, float)
    out = dict(label=label, n=int(len(conf)), cases=int(len(set(cases))),
               accuracy=float(correct.mean()) if len(conf) else None,
               mean_confidence=float(conf.mean()) if len(conf) else None)
    if len(conf) == 0:
        return out
    out["signed_gap"] = out["mean_confidence"] - out["accuracy"]
    out["signed_gap_ci"] = boot_cases(cases, list(zip(conf, correct)),
                                      lambda v: float(np.mean([a for a, _ in v]) - np.mean([b for _, b in v])))
    for scheme in ("equal_mass", "equal_width"):
        e, m, rows = ece_bins(conf, correct, n_bins, scheme)
        out[f"ece_{scheme}"] = e
        out[f"mce_{scheme}"] = m
        if scheme == "equal_mass":
            out["bins"] = rows
            out["ece_ci"] = boot_cases(cases, list(zip(conf, correct)),
                                       lambda v: ece_bins([a for a, _ in v], [b for _, b in v], n_bins, "equal_mass")[0])
            out["brier"] = brier_decomposition(conf, correct, rows)
            if nulls:
                nul = ece_null(conf, nulls, n_bins, scheme)
                out["ece_null_perfectly_calibrated"] = nul
                if nul:
                    rng = np.random.default_rng(SEED + 1)
                    ge = 0
                    for _ in range(nulls):
                        y = (rng.random(len(conf)) < conf).astype(float)
                        if ece_bins(conf, y, n_bins, "equal_mass")[0] >= e:
                            ge += 1
                    out["ece_p_vs_null"] = (ge + 1) / (nulls + 1)
    return out


def cmd_level(a):
    t0 = time.time()
    src = {}
    if a.scores:
        rows, files = read_carm_scores(a.scores)
        if not rows:
            print("no score rows matched", a.scores)
            return 2
        src = dict(kind="carmlspine_score_json", files=files, n_items=len(rows),
                   cluster_key="case", n_clusters=len({r["case"] for r in rows}),
                   n_frames=len({(r["file"], r["case"], r["view"]) for r in rows}),
                   note="top-1 posterior only; conformal SETS need tools/level_posteriors.py")
        probs = None
        order = None
    else:
        pr, order = read_posteriors(a.posteriors)
        if not pr:
            print("no posterior rows in", a.posteriors)
            return 2
        P = np.asarray([r["probs"] for r in pr], float)
        P = P / np.clip(P.sum(1, keepdims=True), 1e-12, None)
        ck = [cluster_key_of(r) for r in pr]
        rows = [dict(conf=float(P[i].max()), correct=(order[int(P[i].argmax())] == pr[i]["true"]),
                     within1=None, region_ok=(REGION.get(order[int(P[i].argmax())], "?") == REGION.get(pr[i]["true"], "!")),
                     truth=pr[i]["true"], call=order[int(P[i].argmax())], single=None, single_exact=None,
                     abstain=bool(P[i].max() < 0.5), case=ck[i][0], render=str(pr[i].get("case")), view="-", k="crop",
                     boxes="-", fold="-", tag="", file=a.posteriors) for i in range(len(pr))]
        probs = P
        src = dict(kind="posteriors_jsonl", files=[a.posteriors], n_items=len(rows), classes=len(order),
                   cluster_key=ck[0][1] if ck else "case",
                   n_clusters=len({c for c, _ in ck}), n_render_names=len({str(r.get("case")) for r in pr}),
                   cluster_note=("the split and every interval cluster on the CT SUBJECT (`group`); clustering on "
                                 "the render name would put several poses of one spine on both sides of the split"
                                 if (ck and ck[0][1] == "group") else
                                 "this dump carries no `group` field, so the cluster is the render name and "
                                 "several renders of one spine may straddle the split -- regenerate the dump with "
                                 "tools/level_posteriors.py to get `group`"))

    # filter by INDEX, never by rebuilding the list and looking each row up again: list.index on dicts is a
    # linear scan with a dict comparison at every step, so the "harmless" lookup is O(n^2) and a 16,000-row
    # posterior dump never returns.
    sel = [i for i, r in enumerate(rows)
           if (not a.boxes or r["boxes"] == a.boxes)
           and (not a.view or r["view"] == a.view)
           and (not a.k or str(r["k"]) == a.k)]
    if not sel:
        print("filters removed every row")
        return 2
    rows = [rows[i] for i in sel]
    if probs is not None:
        probs = probs[np.asarray(sel, int)]

    conf = np.asarray([r["conf"] for r in rows], float)
    corr = np.asarray([r["correct"] for r in rows], float)
    cases = [r["case"] for r in rows]
    # A row is a READING, not a vertebra. The band-length crops overlap and the same vertebra is scored in
    # several of them: pooling k=1..5 and the whole frame gives 10,264 rows over 1,286 distinct (case, view,
    # level) vertebrae -- eight readings each, up to fourteen -- and even within k=2 alone 1,979 rows are 1,175
    # vertebrae. The case bootstrap absorbs the dependence, but "10,264 vertebrae" is eight times the truth and
    # the pooled ECE is weighted by how many crops the cropping script happened to cut, not by anything clinical.
    vert_id = {(r["case"], r["view"], r["truth"]) for r in rows}
    src["n_readings"] = len(rows)
    src["n_distinct_vertebrae"] = len(vert_id)
    src["readings_per_vertebra"] = round(len(rows) / max(len(vert_id), 1), 2)
    res = dict(tool="tools/eval_calibration.py level", written=time.strftime("%Y-%m-%d %H:%M %Z"),
               code_sha=code_sha(), seed=SEED, bootstrap=BOOT, bins=NBINS, source=src,
               filters=dict(boxes=a.boxes, view=a.view, k=a.k), alpha=a.alpha)

    # ---------- 1. calibration, pooled and by band length, and by level
    print(f"  {len(rows)} items, {len(set(cases))} cases: calibration ...", flush=True)
    res["calibration_pooled"] = calib_block(conf, corr, cases, "all items")
    res["calibration_by_band_length"] = {}
    for k in sorted({r["k"] for r in rows}, key=lambda s: (s == "full", int(s) if str(s).isdigit() else 99)):
        I = [i for i, r in enumerate(rows) if r["k"] == k]
        if len(I) >= 30:
            res["calibration_by_band_length"][k] = calib_block(conf[I], corr[I], [cases[i] for i in I],
                                                               f"band length k={k}", nulls=200)
    res["calibration_by_view"] = {}
    for v in sorted({r["view"] for r in rows}):
        I = [i for i, r in enumerate(rows) if r["view"] == v]
        if len(I) >= 30:
            res["calibration_by_view"][v] = calib_block(conf[I], corr[I], [cases[i] for i in I], f"view {v}", nulls=200)
    per = collections.defaultdict(list)
    for i, r in enumerate(rows):
        per[r["truth"]].append(i)
    res["per_level"] = {}
    for lv, I in per.items():
        res["per_level"][lv] = dict(n=len(I), cases=len({cases[i] for i in I}),
                                    accuracy=float(corr[I].mean()), mean_confidence=float(conf[I].mean()),
                                    signed_gap=float(conf[I].mean() - corr[I].mean()),
                                    accuracy_lower95=clopper_pearson_lower(int(corr[I].sum()), len(I)),
                                    lower95_note="exact binomial over VERTEBRAE; it assumes the n here are "
                                                 "independent draws, which vertebrae of one case are not")
    res["micro_accuracy"] = float(corr.mean())
    # A macro (balanced) average weights a class with one vertebra exactly as heavily as one with 283, so on
    # this test set -- whose whole-frame per-level census is L1-L5 plus a single T12 -- the entire micro/macro
    # gap can be one or two vertebrae of a class that is barely present. Measured: whole frames micro 97.44,
    # macro over all six classes 97.91, macro over the five with n >= 5 97.49; pooled over band lengths
    # micro 89.12, macro over all six 81.92, macro over the five with n >= 5 88.31. Quoting the unrestricted
    # macro as "what a test set of easy classes buys" attributes 7.2 points to class imbalance when 6.4 of them
    # are two vertebrae of T12. Both are reported, with the classes that carry the difference named.
    res["macro_min_n"] = MACRO_MIN_N
    res["macro_accuracy_all_classes"] = float(np.mean([v["accuracy"] for v in res["per_level"].values()]))
    kept = {k: v for k, v in res["per_level"].items() if v["n"] >= MACRO_MIN_N}
    res["macro_accuracy"] = float(np.mean([v["accuracy"] for v in kept.values()])) if kept else None
    res["macro_classes"] = len(kept)
    res["macro_classes_all"] = len(res["per_level"])
    res["macro_thin_classes"] = {k: v["n"] for k, v in res["per_level"].items() if v["n"] < MACRO_MIN_N}

    # ---------- 1b. what IS this number the probability of?
    # level_prototype.py writes `level_prob` = the blended posterior's mass at the label the CONSTRAINED anchor
    # decode chose. The decode uses an ordering constraint the marginal does not contain, so the number is not
    # the probability that the shipped decision is right, and there is no reason for it to be calibrated
    # against it. Scoring the same number against the three events it might plausibly be about says which.
    alt = {}
    for key, lab in (("correct", "the decoded name (the shipped call) is right"),
                     ("single_exact", "the single-crop name is right"),
                     ("within1", "the call is within one level")):
        vals = [r.get(key) for r in rows]
        if any(v is None for v in vals):
            continue
        y = np.asarray([bool(v) for v in vals], float)
        e, _, _ = ece_bins(conf, y, NBINS, "equal_mass")
        alt[key] = dict(event=lab, rate=float(y.mean()), mean_confidence=float(conf.mean()),
                        signed_gap=float(conf.mean() - y.mean()), ece_equal_mass=e)
    if alt:
        res["what_the_confidence_is_about"] = alt

    # ---------- 2. recalibration, fit on calibration CASES and applied to test CASES
    print("  recalibration ...", flush=True)
    cal_c, test_c = split_by_case(cases, a.cal_frac)
    ci = [i for i, c in enumerate(cases) if c in cal_c]
    ti = [i for i, c in enumerate(cases) if c in test_c]
    recal = dict(cal_cases=len(cal_c), test_cases=len(test_c), cal_items=len(ci), test_items=len(ti))
    if len(ci) >= 50 and len(ti) >= 50:
        # ECE alone is MINIMISED by throwing the score away: a constant equal to the base rate has almost no
        # calibration error and no information at all. Measured on the whole C-arm frames, the shipped score
        # reads ECE 20.03 % with resolution 0.0019, Platt takes it to 3.47 % with resolution 0.0019 and the
        # SAME rank AUC 0.692, and a constant at the base rate reaches 4.29 % -- i.e. the "fix" is arithmetically
        # close to printing one number for every vertebra. So every row below carries the Brier decomposition
        # and the rank AUC beside the ECE, and the constant predictor is one of the rows, because a
        # recalibration that does not beat it has bought nothing a threshold can be set on.
        def _row(p, y, **extra):
            e, _, bb = ece_bins(p, y, NBINS, "equal_mass")
            br = brier_decomposition(p, y, bb)
            au = _auc(p, np.asarray(y, bool))
            d = dict(ece_equal_mass=e, mean_confidence=float(np.mean(p)),
                     signed_gap=float(np.mean(p) - np.mean(y)), brier=br["brier"],
                     reliability=br["reliability"], resolution=br["resolution"], uncertainty=br["uncertainty"],
                     ranking_auc=au, conf_min=float(np.min(p)), conf_max=float(np.max(p)))
            d.update(extra)
            return d

        raw = calib_block(conf[ti], corr[ti], [cases[i] for i in ti], "test half, raw", nulls=200)
        recal["raw"] = {k: raw[k] for k in ("n", "accuracy", "mean_confidence", "signed_gap",
                                            "ece_equal_mass", "ece_ci", "ece_p_vs_null")}
        recal["raw"].update(_row(conf[ti], corr[ti]))
        w = platt_fit(conf[ci], corr[ci])
        recal["platt"] = _row(platt_apply(w, conf[ti]), corr[ti], a=float(w[0]), b=float(w[1]))
        kn = isotonic_fit(conf[ci], corr[ci])
        recal["isotonic"] = _row(isotonic_apply(kn, conf[ti]), corr[ti], knots=int(len(kn[0])))
        recal["constant_base_rate"] = _row(np.full(len(ti), float(corr[ci].mean())), corr[ti],
                                           note="no score at all: the calibration half's accuracy printed for "
                                                "every vertebra. Any recalibration that does not beat this "
                                                "row's Brier and rank AUC has removed the miscalibration by "
                                                "removing the information.")
        recal["recalibration_keeps_information"] = bool(
            recal["platt"]["resolution"] > recal["constant_base_rate"]["resolution"] * 1.5
            or (recal["isotonic"]["resolution"] > recal["constant_base_rate"]["resolution"] * 1.5))
        if probs is not None:
            idx = {n: i for i, n in enumerate(order)}
            logp = np.log(np.clip(probs, 1e-12, None))
            yi = np.asarray([idx[rows[i]["truth"]] for i in range(len(rows))], int)
            T, nll_t, nll_1 = temperature_fit(logp[ci], yi[ci])
            Q = temperature_apply(logp[ti], T)
            tc = Q.max(1)
            recal["temperature"] = _row(tc, corr[ti], T=T, nll_at_T=nll_t, nll_at_1=nll_1,
                                        reading=("over-confident (T>1 sharpens nothing; the fit had to soften it)"
                                                 if T > 1.02 else "under-confident" if T < 0.98 else "already near T=1"))
    else:
        recal["note"] = "too few items to fit and test a recalibration by case"
    res["recalibration"] = recal

    # ---------- 3. selective prediction: the curve, and the SHIPPED rule's place on it
    print("  selective prediction ...", flush=True)
    cur = rc_curve(conf, corr)
    step = max(1, len(cur["coverage"]) // 500)
    sel_out = dict(augrc=cur["augrc"], full_coverage_accuracy=float(corr.mean()),
                   note="AUGRC is the average risk of the failures the rule let through; lower is better",
                   curve=dict(coverage=[float(v) for v in cur["coverage"][::step]],
                              accuracy=[float(v) for v in cur["accuracy"][::step]],
                              implementable=[bool(v) for v in cur["implementable"][::step]],
                              implementable_share=float(cur["implementable"].mean()),
                              note=f"every {step}th point of the {len(cur['coverage'])}-point curve, so the "
                                   f"figure can be redrawn from this file without the per-item rows. "
                                   f"`implementable` marks the prefixes a threshold can actually produce: the "
                                   f"scores are rounded to three decimals, so a prefix that stops inside a tied "
                                   f"block is no rule at all. Only {100 * cur['implementable'].mean():.0f} % of "
                                   f"the prefixes here are rules, and almost none of them below a quarter "
                                   f"coverage, so the left arm of the curve must be read as an envelope and not "
                                   f"as operating points."))
    for cv in (0.95, 0.99, 1.0):
        p = acc_at_coverage(conf, corr, cv)
        if p:
            p["accuracy_ci"] = boot_cases(cases, list(zip(conf, corr)),
                                          lambda v, _c=cv: (acc_at_coverage([x for x, _ in v], [y for _, y in v], _c, bound=False) or {}).get("accuracy"))
            sel_out[f"accuracy_at_coverage_{int(cv * 100)}"] = p
    for ta in (0.99, 0.975, 0.95):
        p = coverage_at_accuracy(conf, corr, ta)
        if p:
            # boot_cases DROPS a resample whose fn returns None, and coverage_at_accuracy returns None when the
            # target accuracy is not reachable in that resample. The count is recorded so a percentile taken
            # over a surviving subset can never be read as a percentile over 2,000 draws.
            reach = [0]

            def _cov(v, _t=ta, _r=reach):
                q = coverage_at_accuracy([x for x, _ in v], [y for _, y in v], _t, bound=False)
                if q is None:
                    _r[0] += 1
                    return None
                return q["coverage"]

            p["coverage_ci"] = boot_cases(cases, list(zip(conf, corr)), _cov)
            p["ci_resamples_unreachable"] = int(reach[0])
            p["ci_note"] = (f"{reach[0]} of {BOOT} resamples could not reach {ta:.3f} at any threshold and were "
                            f"dropped from the percentile; the interval is conditional on reachability"
                            if reach[0] else f"all {BOOT} resamples reached the target")
            p["lower95_per_vertebra"] = p.pop("lower95", None)
            d = design_effect(conf, corr.astype(bool), cases, p["threshold"])
            k = int(round(p["accuracy"] * p["n_answered"]))
            p["design_effect"] = d
            p["lower95_clustered"] = clopper_pearson_lower(k / d, p["n_answered"] / d)
            p["bound_note"] = ("the per-vertebra exact bound assumes independent draws; the clustered one takes "
                               "the same exact bound at the effective sample size n/design_effect, which is the "
                               "correction the risk-control section below shows is not optional on this data")
        sel_out[f"coverage_at_accuracy_{int(ta * 1000)}"] = p
    reg = np.asarray([bool(r["region_ok"]) for r in rows], float)
    if reg.any():
        sel_out["region"] = {f"coverage_at_accuracy_{int(t * 1000)}": coverage_at_accuracy(conf, reg, t)
                             for t in (0.99, 0.975, 0.95)}

    # the two terms of the shipped rule, separated
    have_single = any(r["single"] is not None for r in rows)
    rules = {}
    ans = np.asarray([not r["abstain"] for r in rows], bool)
    rules["shipped_compound"] = dict(
        description=("level_prototype.py: abstain when prob < 0.5 OR the decoded name differs from the single-crop "
                     "name" if have_single else
                     "abstain when prob < 0.5; this source has no decode, so the agreement term of the shipped "
                     "rule does not exist here and this row equals the pure-confidence rule"),
        coverage=float(ans.mean()), accuracy_answered=float(corr[ans].mean()) if ans.any() else None,
        accuracy_abstained=float(corr[~ans].mean()) if (~ans).any() else None,
        accuracy_answered_ci=boot_cases([c for c, m in zip(cases, ans) if m],
                                        [y for y, m in zip(corr, ans) if m], lambda v: float(np.mean(v))))
    m = conf >= 0.5
    rules["prob_only_0.5"] = dict(description="abstain when prob < 0.5 alone", coverage=float(m.mean()),
                                  accuracy_answered=float(corr[m].mean()) if m.any() else None,
                                  accuracy_answered_ci=boot_cases([c for c, x in zip(cases, m) if x],
                                                                  [y for y, x in zip(corr, m) if x], lambda v: float(np.mean(v))))
    if have_single:
        agree = np.asarray([r["call"] == r["single"] for r in rows], bool)
        rules["agreement_only"] = dict(description="abstain when the decoded name differs from the single-crop name alone",
                                       coverage=float(agree.mean()),
                                       accuracy_answered=float(corr[agree].mean()) if agree.any() else None,
                                       accuracy_answered_ci=boot_cases([c for c, x in zip(cases, agree) if x],
                                                                       [y for y, x in zip(corr, agree) if x], lambda v: float(np.mean(v))))
        # Is the shipped point on the frontier? The comparator is a pure-confidence threshold TUNED ON THESE
        # SAME items to land at the shipped rule's coverage, while the shipped rule is fixed -- so the
        # comparison is biased in the comparator's favour and the difference is not a held-out number. On the
        # whole C-arm frames it comes to one vertebra (981/1001 against 982/1001), so the gap is reported with a
        # paired case-cluster interval and with the same threshold refitted on calibration cases and scored on
        # test cases. A difference whose interval spans zero is not a finding about the agreement term.
        eq = acc_at_coverage(conf, corr, float(ans.mean()))
        if eq:
            thr = eq["threshold"]
            rules["prob_only_at_shipped_coverage"] = dict(
                description="the pure-confidence rule tuned to answer exactly as often as the shipped rule",
                coverage=eq["coverage"], accuracy_answered=eq["accuracy"], threshold=thr,
                in_sample=True,
                caveat="this threshold is chosen on the items it is then scored on; the shipped rule is not",
                accuracy_answered_ci=boot_cases([c for c, x in zip(cases, conf >= thr) if x],
                                                [y for y, x in zip(corr, conf >= thr) if x],
                                                lambda v: float(np.mean(v))))
            rules["frontier_gap_pp"] = (100 * ((rules["shipped_compound"]["accuracy_answered"] or 0) - eq["accuracy"]))
            rules["frontier_gap_pp_ci"] = boot_cases(
                cases, list(zip(corr, ans, conf)),
                lambda v, _t=thr: (100 * (float(np.mean([y for y, m, _ in v if m]))
                                          - float(np.mean([y for y, _, c2 in v if c2 >= _t]))))
                if any(m for _, m, _ in v) and any(c2 >= _t for _, _, c2 in v) else None)
            rules["frontier_gap_n_vertebrae"] = int(abs(round(rules["shipped_compound"]["accuracy_answered"]
                                                             * int(ans.sum()))
                                                       - round(eq["accuracy"] * eq["n_answered"])))
            if len(ci) >= 50 and len(ti) >= 50:
                eqc = acc_at_coverage(conf[ci], corr[ci], float(ans[ci].mean()))
                if eqc:
                    mt = conf[ti] >= eqc["threshold"]
                    at = ans[ti]
                    rules["frontier_held_out"] = dict(
                        description="the same comparison with the comparator threshold fitted on calibration "
                                    "cases and both rules scored on the test cases",
                        threshold=eqc["threshold"],
                        tuned_coverage=float(mt.mean()),
                        tuned_accuracy=float(corr[ti][mt].mean()) if mt.any() else None,
                        shipped_coverage=float(at.mean()),
                        shipped_accuracy=float(corr[ti][at].mean()) if at.any() else None,
                        gap_pp=(100 * (float(corr[ti][at].mean()) - float(corr[ti][mt].mean()))
                                if (at.any() and mt.any()) else None))
    sel_out["rules"] = rules
    res["selective"] = sel_out

    # ---------- 4. conformal
    print("  conformal ...", flush=True)
    conf_out = {}
    cal_rows = [i for i in range(len(rows)) if cases[i] in cal_c]
    test_rows = [i for i in range(len(rows)) if cases[i] in test_c]
    for al in a.alpha:
        block = dict(alpha=al)
        block["selective_risk_control"] = selective_risk_control(
            [(conf[i], bool(corr[i])) for i in cal_rows], [(conf[i], bool(corr[i])) for i in test_rows], al,
            cal_cases=[cases[i] for i in cal_rows], test_cases=[cases[i] for i in test_rows])
        if probs is not None and len(cal_rows) > 50:
            truths = [rows[i]["truth"] for i in test_rows]
            for meth, mond in (("lac", False), ("aps", False), ("lac", True)):
                name = f"{meth}{'_mondrian' if mond else ''}"
                sets, qv, thin = conformal_sets(probs[cal_rows], [rows[i]["truth"] for i in cal_rows],
                                                probs[test_rows], order, al, meth, mond)
                st = set_stats(sets, truths)
                st["thin_classes"] = thin
                st["coverage_ci"] = boot_cases([cases[i] for i in test_rows],
                                               list(zip(sets, truths)),
                                               lambda v: float(np.mean([t in s for s, t in v])))
                st["set_size_ci"] = boot_cases([cases[i] for i in test_rows], sets,
                                               lambda v: float(np.mean([len(s) for s in v])))
                # Not a hidden 2-pp fudge: the guarantee is marginal over the calibration draw, so the honest
                # reading is whether the target sits inside the interval the same run already computed.
                cc95 = st.get("coverage_ci") or [None, None]
                st["guarantee_held"] = (None if cc95[0] is None else bool(cc95[1] >= 1 - al))
                st["guarantee_rule"] = ("the upper end of the case-cluster interval on the EMPIRICAL coverage "
                                        "reaches the 1-alpha target")
                st["coverage_shortfall_pp"] = 100 * (st["empirical_coverage"] - (1 - al))
                st["exchangeability_caveat"] = (
                    "split conformal is valid when calibration and test ITEMS are exchangeable. Here they are "
                    "vertebrae clustered in spines: the split is drawn by cluster, which keeps a spine off both "
                    "sides, but it does not make two vertebrae of one spine exchangeable with two of different "
                    "spines. Read the empirical coverage as the test of the guarantee, not the target as a proof.")
                block[name] = st
        else:
            block["note_sets"] = ("prediction SETS need the full posterior vector; the score JSON keeps only the "
                                  "top-1 probability, so only the selective risk bound is computed here")
        conf_out[f"alpha_{al}"] = block
    res["conformal"] = conf_out

    out = Path(os.path.expanduser(a.out))
    out.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out / "calibration_level.json", "w"), indent=1, default=float)
    md = level_report(res)
    (out / "CALIBRATION_LEVEL.md").write_text(md, encoding="utf-8")
    print(md)
    if not a.no_fig:
        try:
            fig_level(res, rows, conf, corr, cases, out)
        except Exception as e:  # noqa: BLE001
            print("figure skipped:", e)
    print(f"\nwrote {out}/calibration_level.json and CALIBRATION_LEVEL.md  ({time.time() - t0:.0f} s)")
    return 0


def _pct(v, d=1):
    return "n/a" if v is None else f"{100 * v:.{d}f}"


def _ci(v, d=1):
    """A missing interval and an impossible one are different facts and must not print the same string.

    The first version returned "[1 case]" for both, so a row whose CI was simply never computed advertised a
    single-cluster dataset (the level report's `prob_only_at_shipped_coverage` printed "[1 case]" on a run with
    143 cases), and a detector row with no kept boxes printed "n/a [1 case]" for a precision that did not exist.
    """
    if v is None:
        return "[no CI]"
    if not len(v) or v[0] is None:
        return "[1 cluster]"
    return f"[{100 * v[0]:.{d}f}, {100 * v[1]:.{d}f}]"


def _ciraw(v, d=2):
    """A set SIZE is a count, not a percentage: the percentage formatter would print a mean size of 2.7 as
    [256.0, 289.0]."""
    if not v or v[0] is None:
        return ""
    return f"[{v[0]:.{d}f}, {v[1]:.{d}f}]"


def level_report(r):
    s = r["source"]
    L = [f"# Does the level model's confidence mean what it says?", "",
         f"Source: `{s['kind']}`, {s['n_items']} items from {len(s['files'])} file(s). "
         f"Filters {r['filters']}. Code {r['code_sha']}, seed {r['seed']}, {r['bootstrap']} case-cluster resamples, "
         f"{r['bins']} bins.", ""]
    c = r["calibration_pooled"]
    nd = s.get("n_distinct_vertebrae")
    rep = (f" -- these are READINGS, not vertebrae: {nd} distinct (case, view, level) vertebrae read "
           f"{s.get('readings_per_vertebra')} times each, because the band-length crops overlap"
           if nd and s.get("readings_per_vertebra", 1) > 1.05 else "")
    L += ["## Calibration", "",
          f"- {c['n']} readings over {c['cases']} {s.get('cluster_key', 'case')}s; accuracy "
          f"**{_pct(c['accuracy'])} %**, mean confidence **{_pct(c['mean_confidence'])} %**" + rep,
          f"- signed gap (confidence minus accuracy): **{100 * c['signed_gap']:+.1f} pp** {_ci(c['signed_gap_ci'])} "
          f"-- positive is over-confident",
          f"- ECE equal-mass **{_pct(c['ece_equal_mass'], 2)} %** {_ci(c.get('ece_ci'), 2)}; "
          f"equal-width {_pct(c['ece_equal_width'], 2)} %; MCE {_pct(c['mce_equal_mass'], 1)} %"]
    nul = c.get("ece_null_perfectly_calibrated")
    if nul:
        L += [f"- a PERFECTLY calibrated model of this size would show ECE {_pct(nul['mean'], 2)} % by chance "
              f"(95th percentile {_pct(nul['p95'], 2)} %); p = {c.get('ece_p_vs_null'):.3f} that the observed ECE "
              f"is chance alone"]
    b = c.get("brier")
    if b:
        L += [f"- Brier on `top-1 is correct` {b['brier']:.4f} = reliability {b['reliability']:.4f} "
              f"- resolution {b['resolution']:.4f} + uncertainty {b['uncertainty']:.4f}"]
    if "macro_thin_classes" not in r:      # a result file written before the minimum-n rule existed
        L += ["", f"Micro accuracy {_pct(r['micro_accuracy'])} % against macro (balanced over every level "
                  f"present, including any with one or two vertebrae) **{_pct(r.get('macro_accuracy'))} %**. "
                  f"This file predates the minimum-n rule, so the macro here can be moved by a class that "
                  f"barely appears; re-run `level` to get both numbers.", ""]
        thin = None
    else:
        thin = r.get("macro_thin_classes") or {}
    if thin is not None:
        L += ["", f"Micro accuracy {_pct(r['micro_accuracy'])} % against macro (balanced over the "
              f"{r.get('macro_classes', '?')} levels with n >= {r.get('macro_min_n', MACRO_MIN_N)}) "
              f"**{_pct(r.get('macro_accuracy'))} %**. Over ALL {r.get('macro_classes_all', '?')} levels present "
              f"the macro is {_pct(r.get('macro_accuracy_all_classes'))} %"
              + (f", and the difference between those two is carried entirely by "
                 f"{', '.join(f'{k} (n={v})' for k, v in sorted(thin.items()))} -- a class with one or two "
                 f"vertebrae weighs as much in a balanced average as one with hundreds, so the unrestricted "
                 f"macro must not be quoted as evidence of class imbalance." if thin else
                 " (no level here has fewer than the minimum, so the two agree)."), ""]
    if r.get("what_the_confidence_is_about"):
        L += ["### What is this number the probability of?", "",
              "The shipped confidence is the blended posterior's mass at the label the CONSTRAINED anchor decode "
              "chose. The decode uses an ordering the marginal does not contain, so the number has no reason to "
              "be the probability that the shipped call is right. Scored against each event it might be about:", "",
              "| event | rate | mean confidence | signed gap (pp) | ECE |", "|---|---|---|---|---|"]
        for _k, v in r["what_the_confidence_is_about"].items():
            L.append(f"| {v['event']} | {_pct(v['rate'])} | {_pct(v['mean_confidence'])} | "
                     f"{100 * v['signed_gap']:+.1f} | {_pct(v['ece_equal_mass'], 2)} |")
        L.append("")
    if r["calibration_by_band_length"]:
        L += ["### Over- and under-confidence by band length", "",
              "| band | n | accuracy | mean conf | signed gap (pp) | ECE |", "|---|---|---|---|---|---|"]
        for k, v in r["calibration_by_band_length"].items():
            L.append(f"| k={k} | {v['n']} | {_pct(v['accuracy'])} | {_pct(v['mean_confidence'])} | "
                     f"{100 * v['signed_gap']:+.1f} {_ci(v['signed_gap_ci'])} | {_pct(v['ece_equal_mass'], 2)} |")
        L.append("")
    if r["calibration_by_view"]:
        L += ["### By view", "", "| view | n | accuracy | mean conf | signed gap (pp) | ECE |", "|---|---|---|---|---|---|"]
        for k, v in r["calibration_by_view"].items():
            L.append(f"| {k} | {v['n']} | {_pct(v['accuracy'])} | {_pct(v['mean_confidence'])} | "
                     f"{100 * v['signed_gap']:+.1f} | {_pct(v['ece_equal_mass'], 2)} |")
        L.append("")
    L += ["### Per level, where a marginal number hides the class the product exists for", "",
          "| level | n | cases | accuracy | 95% lower (per-vertebra) | mean conf | signed gap (pp) |",
          "|---|---|---|---|---|---|---|"]
    for lv, v in sorted(r["per_level"].items(), key=lambda kv: -kv[1]["n"]):
        L.append(f"| {lv} | {v['n']} | {v.get('cases', '?')} | {_pct(v['accuracy'])} | "
                 f"{_pct(v['accuracy_lower95'])} | {_pct(v['mean_confidence'])} | {100 * v['signed_gap']:+.1f} |")
    L += ["", "The lower bound in that column is an exact binomial over VERTEBRAE and so assumes the n in the "
              "first column are independent draws. They are not -- the `cases` column says how few spines they "
              "come from -- and the risk-control section below measures how large the correction is. Read it as "
              "the most optimistic bound available, not as the bound.", ""]
    rc = r["recalibration"]
    L += ["## Can it be fixed by rescaling?", "",
          f"Fit on {rc['cal_cases']} calibration cases ({rc.get('cal_items', 0)} items), applied unchanged to "
          f"{rc['test_cases']} test cases ({rc.get('test_items', 0)} items).", ""]
    if "raw" in rc:
        def _rrow(lab, v):
            au = v.get("ranking_auc")
            return (f"| {lab} | {_pct(v['ece_equal_mass'], 2)} | {_pct(v['mean_confidence'])} | "
                    f"{100 * v['signed_gap']:+.1f} | {v.get('brier', float('nan')):.4f} | "
                    f"{v.get('resolution', float('nan')):.4f} | "
                    f"{('%.3f' % au) if au is not None else 'n/a'} |")

        L += ["| map | ECE on test | mean conf | signed gap (pp) | Brier | resolution | rank AUC |",
              "|---|---|---|---|---|---|---|", _rrow("none (as shipped)", rc["raw"])]
        if "temperature" in rc:
            L.append(_rrow(f"temperature T={rc['temperature']['T']:.3f}", rc["temperature"]))
        L.append(_rrow(f"Platt (a={rc['platt']['a']:.3f}, b={rc['platt']['b']:.3f})", rc["platt"]))
        L.append(_rrow(f"isotonic ({rc['isotonic']['knots']} knots)", rc["isotonic"]))
        if "constant_base_rate" in rc:
            L.append(_rrow("**no score at all** (a constant = the calibration half's accuracy)",
                           rc["constant_base_rate"]))
        if "temperature" in rc:
            L += ["", f"Temperature reading: {rc['temperature']['reading']}."]
        L += ["", "**Read the last three columns before the first.** ECE is minimised by throwing the score away, "
                  "so an ECE that falls is not on its own evidence that anything was gained. Every map here is "
                  "monotone, so none of them can change the ordering: the rank AUC is identical down the column "
                  "by construction, and what moves is only the scale. The question a threshold actually depends "
                  "on is the RESOLUTION -- how far the confidences separate the calls that are right from the "
                  "ones that are not. The last row is a predictor with no information at all, and the small "
                  "resolution it still shows is the noise floor of binning, not signal."]
        if rc.get("recalibration_keeps_information") is False:
            L += ["", "On this input the score's resolution does not clear that floor. Recalibrating it makes "
                      "the printed number honest without making it informative, so 'recalibrate, then set a "
                      "threshold' does not follow from this table: after the map the rule would still be "
                      "separating the same calls just as poorly, and the abstain rule has to get its evidence "
                      "somewhere else."]
        L.append("")
    else:
        L += [rc.get("note", ""), ""]
    se = r["selective"]
    L += ["## Selective prediction", "",
          f"Accuracy at full coverage **{_pct(se['full_coverage_accuracy'])} %**. AUGRC {se['augrc']:.4f}.", "",
          "| rule | answers | accuracy among answered |", "|---|---|---|"]
    for k, v in se["rules"].items():
        if not isinstance(v, dict) or v.get("coverage") is None:
            continue   # `frontier_held_out` is a comparison, not a rule; it has its own paragraph below
        L.append(f"| {k} | {_pct(v.get('coverage'))} % | {_pct(v.get('accuracy_answered'))} "
                 f"{_ci(v.get('accuracy_answered_ci'))} |")
    if "frontier_gap_pp" in se["rules"]:
        g = se["rules"]["frontier_gap_pp"]
        gci = se["rules"].get("frontier_gap_pp_ci") or [None, None]
        nv = se["rules"].get("frontier_gap_n_vertebrae")
        word = "the same accuracy" if abs(g) < 0.05 else ("%.2f pp less" % abs(g) if g > 0 else "%.2f pp more" % abs(g))
        L += ["", "At the coverage the shipped rule actually achieves, a pure-confidence threshold reaches "
                  + word + ": the agreement term is worth %+.2f pp at equal coverage" % g
                  + ("" if gci[0] is None else ", paired case-cluster interval [%+.2f, %+.2f] pp" % (gci[0], gci[1]))
                  + ("" if nv is None else ", which is %d vertebra%s" % (nv, "" if nv == 1 else "e")) + ".",
              "",
              "That comparator threshold is chosen on the same items it is then scored on while the shipped rule "
              "is fixed, so the comparison is tilted toward the comparator. If the interval spans zero the "
              "agreement term has not been shown to be worth anything either way."]
        fh = se["rules"].get("frontier_held_out")
        if fh and fh.get("gap_pp") is not None:
            L += ["", "Refitting that threshold on the calibration cases and scoring both rules on the test "
                      "cases: tuned answers %s %% at %s %%, shipped answers %s %% at %s %%, gap %+.2f pp."
                  % (_pct(fh["tuned_coverage"]), _pct(fh["tuned_accuracy"]), _pct(fh["shipped_coverage"]),
                     _pct(fh["shipped_accuracy"]), fh["gap_pp"])]
    L += ["", "| question | answer |", "|---|---|"]
    for cv in (95, 99, 100):
        k = f"accuracy_at_coverage_{cv}"
        if k in se:
            v = se[k]
            # a bootstrap of an accuracy at its ceiling has zero width and prints [100.0, 100.0]; the exact
            # one-sided bound is carried beside it so a degenerate interval cannot be read as certainty
            L.append(f"| accuracy when {cv} % are answered | {_pct(v['accuracy'])} % {_ci(v.get('accuracy_ci'))} "
                     f"(threshold {v['threshold']:.3f}, n={v['n_answered']}, exact 95 % lower bound "
                     f"{_pct(v.get('lower95'))} %) |")
    for ta, lab in ((990, "99"), (975, "97.5"), (950, "95")):
        k = f"coverage_at_accuracy_{ta}"
        v = se.get(k)
        if not v:
            L.append(f"| coverage reachable at {lab} % accuracy | not reached |")
            continue
        drop = v.get("ci_resamples_unreachable") or 0
        L.append(f"| coverage reachable at {lab} % accuracy | {_pct(v['coverage'])} % {_ci(v.get('coverage_ci'))} "
                 f"(n={v['n_answered']}; 95 % lower bound on the accuracy "
                 f"{_pct(v.get('lower95_per_vertebra', v.get('lower95')))} % "
                 f"per vertebra, {_pct(v.get('lower95_clustered'))} % at the effective sample size "
                 f"n/{(v.get('design_effect') or 1.0):.2f})"
                 + (f" -- **{drop} of {BOOT} bootstrap resamples never reached {lab} % at any threshold and were "
                    f"dropped from that interval**" if drop else "") + " |")
    if "region" in se:
        for ta, lab in ((990, "99"), (950, "95")):
            v = se["region"].get(f"coverage_at_accuracy_{ta}")
            L.append(f"| REGION coverage at {lab} % accuracy | " + (f"{_pct(v['coverage'])} % |" if v else "not reached |"))
    L.append("")
    L += ["## Set-valued and risk-controlled prediction", ""]
    for key, blk in r["conformal"].items():
        al = blk["alpha"]
        s = blk.get("selective_risk_control") or {}
        L += [f"### error rate {al}", ""]
        if s.get("threshold") is None:
            L += [f"- selective risk control: {s.get('note', 'not computed')}", ""]
        else:
            extra = ""
            if s.get("clustered"):
                extra = (f" The case clustering inflates the sampling variance {s['design_effect']:.2f}-fold, so the "
                         f"bound is taken at the effective sample size; ignoring it would have chosen "
                         + (f"{s['threshold_uncorrected']:.3f}." if s.get("threshold_uncorrected") is not None
                            else "a lower threshold."))
            L += [f"- distribution-free selective rule: answer when confidence >= **{s['threshold']:.3f}**, chosen on "
                  f"{s['cal_n']} calibration items. On the held-out cases it answers **{_pct(s['test_coverage'])} %** "
                  f"({s['test_answered']}/{s['test_n']}) with error **{_pct(s['test_risk'], 2)} %** "
                  f"(upper 95 % bound {_pct(s['test_risk_upper95'], 2)} %); the bound "
                  f"{'HELD' if s['held'] else 'DID NOT HOLD'} on the test half." + extra, ""]
        if any(k in blk for k in ("lac", "aps", "lac_mondrian")):
            L += ["| method | empirical coverage (target " + f"{1 - al:.2f}) | mean set size | singletons | "
                  "accuracy among singletons | one region |", "|---|---|---|---|---|---|"]
            for m in ("lac", "aps", "lac_mondrian"):
                v = blk.get(m)
                if not v:
                    continue
                L.append(f"| {m} | {_pct(v['empirical_coverage'], 2)} % {_ci(v.get('coverage_ci'), 2)} | "
                         f"{v['mean_set_size']:.2f} {_ciraw(v.get('set_size_ci'))} | "
                         f"{_pct(v['singleton_rate'])} % | {_pct(v['singleton_accuracy'])} % | {_pct(v['one_region_rate'])} % |")
                if v.get("thin_classes"):
                    L.append(f"| | classes with too few calibration examples for a class-conditional quantile: "
                             f"{', '.join(t['level'] for t in v['thin_classes'])} | | | | |")
            L.append("")
        elif "note_sets" in blk:
            L += [f"- {blk['note_sets']}", ""]
    return "\n".join(L)


# ------------------------------------------------------------------------------------------------- detector command
def cmd_detector(a):
    t0 = time.time()
    from realxray_eval import sweep_matches  # the canonical matcher; never a second copy
    files = []
    for pat in a.sweeps:
        files += sorted(glob.glob(os.path.expanduser(pat)))
    if not files:
        print("no sweeps matched", a.sweeps)
        return 2
    cells = {}
    for f in files:
        name = Path(f).stem
        det, ds = (name.split("__", 1) + ["?"])[:2]
        d = json.load(open(f, encoding="utf-8"))
        rows = [r for r in d.get("frames", []) if r.get("raw") is not None and r.get("truth") is not None]
        if not rows:
            # a sweep written without realxray_eval.py --dump-raw keeps no per-prediction confidences, and a
            # calibration figure cannot be invented from pooled recall
            print(f"  {name}: no per-prediction dump (re-run the sweep with --dump-raw); skipped", flush=True)
            continue
        per_class = {}
        for cls, cname in ((0, "vertebra"), (1, "sacrum")):
            pts = []
            for r in rows:
                pred = [(int(c), b, float(s)) for c, b, s in r["raw"]]
                truth = [(int(c), b, lv) for c, b, lv in r["truth"]]
                for cc, tp in sweep_matches(pred, truth, cls):
                    pts.append((float(cc), bool(tp), str(r.get("case")), r.get("stem")))
            if not pts:
                continue
            conf = np.asarray([p[0] for p in pts], float)
            tp = np.asarray([p[1] for p in pts], float)
            cases = [p[2] for p in pts]
            n_truth = sum(sum(1 for t in r["truth"] if int(t[0]) == cls) for r in rows)
            blk = dict(n_predictions=len(pts), n_truth=int(n_truth), frames=len(rows), cases=len(set(cases)))
            blk["all_boxes"] = calib_block(conf, tp, cases, f"{cname}: every box the detector emitted", nulls=a.nulls)
            for t in a.thresholds:
                m = conf >= t
                if m.sum() == 0:
                    blk[f"at_{t}"] = dict(threshold=t, kept=0)
                    continue
                prec = float(tp[m].mean())
                mc = float(conf[m].mean())
                kept = int(m.sum())
                k_tp = int(tp[m].sum())
                pci = boot_cases([c for c, x in zip(cases, m) if x], [y for y, x in zip(tp, m) if x],
                                 lambda v: float(np.mean(v)))
                # A percentile bootstrap of a proportion at its boundary is DEGENERATE: 0 of 26 sacrum boxes
                # correct resamples to 0 every time, and the tool then printed "[0.0, 0.0]" as a 95 % interval
                # for a precision whose exact interval is [0, 13.3] %. Three rows of the real table did this.
                # Where the bootstrap collapses, or the count sits at 0 or n, the exact Clopper-Pearson interval
                # is substituted and the method is recorded, so no row claims a certainty it does not have.
                meth = "case-cluster bootstrap"
                if kept and (k_tp in (0, kept) or (pci[0] is not None and abs(pci[1] - pci[0]) < 1e-12)):
                    pci = [clopper_pearson_lower(k_tp, kept, 0.025),
                           1.0 - clopper_pearson_lower(kept - k_tp, kept, 0.025)]
                    meth = ("exact Clopper-Pearson over BOXES (the case bootstrap of a %d/%d proportion has zero "
                            "width, and would print a point as an interval); it ignores the case clustering, so "
                            "it is a floor on the width, not a case-level interval" % (k_tp, kept))
                gci = boot_cases([c for c, x in zip(cases, m) if x],
                                 [(cf, y) for cf, y, x in zip(conf, tp, m) if x],
                                 lambda v: float(np.mean([q for q, _ in v]) - np.mean([w for _, w in v])))
                gmeth = "paired case-cluster bootstrap of (mean confidence - precision)"
                if meth.startswith("exact") and gci[0] is not None:
                    # the precision half of the gap is pinned at the boundary in every resample, so the paired
                    # interval moves only with the confidence and reads far tighter than the gap really is:
                    # 0/26 sacrum boxes gave [+33.7, +44.3] pp when the precision alone spans [0, 13.2] %.
                    gci = [gci[0] - (pci[1] - prec), gci[1] + (prec - pci[0])]
                    gmeth += ("; widened by the exact precision interval because the bootstrap cannot move a "
                              "proportion off its boundary")
                blk[f"at_{t}"] = dict(
                    threshold=t, kept=kept, true_positives=k_tp, precision=prec,
                    recall=float(tp[m].sum() / n_truth) if n_truth else None,
                    mean_confidence=mc, signed_gap=mc - prec,
                    precision_ci=pci, precision_ci_method=meth,
                    signed_gap_ci=gci, signed_gap_ci_method=gmeth,
                    ece_equal_mass=ece_bins(conf[m], tp[m], NBINS, "equal_mass")[0])
            # the confidence a target precision would actually require, read off this device's own curve
            need = {}
            for target in a.precision_targets:
                got = None
                for t in np.unique(np.round(conf, 3))[::-1]:
                    m = conf >= t
                    if m.sum() >= 20 and tp[m].mean() >= target:
                        got = float(t)
                if got is None:
                    need[str(target)] = None
                else:
                    m = conf >= got
                    kk = int(tp[m].sum())
                    nn = int(m.sum())
                    # this threshold is picked on the very boxes its precision is then read from, so the
                    # precision is optimistic and the exact one-sided bound is what a reader should quote:
                    # the sacrum's 0.66 on the held-out C-arm reads 91.8 % with a 95 % lower bound of 82.3 %,
                    # i.e. the 90 % target it is described as meeting is not established.
                    need[str(target)] = dict(threshold=got, kept=nn, true_positives=kk, precision=float(kk / nn),
                                             precision_lower95=clopper_pearson_lower(kk, nn),
                                             recall=float(tp[m].sum() / n_truth) if n_truth else None,
                                             selected_in_sample=True)
            blk["threshold_for_precision"] = need
            n1 = int(tp.sum())
            n0 = int(len(tp) - n1)
            # A rank AUC of 1.000 computed from ONE true box says nothing, and the prose under the table tells
            # the reader that a high AUC means a per-device threshold will fix the calibration. Sixteen of the
            # real table's AUCs rest on five or fewer positives (seven on exactly one), all of them sacrum cells
            # in the collimated crops, where the whole dataset contains 11 and 13 truth sacra. The number is
            # withheld below AUC_MIN_N of either class and the support is printed instead.
            blk["ranking_auc"] = _auc(conf, tp) if min(n1, n0) >= AUC_MIN_N else None
            blk["ranking_auc_support"] = [n1, n0]
            if min(n1, n0) < AUC_MIN_N:
                blk["ranking_auc_note"] = (f"withheld: {n1} true and {n0} false boxes; an AUC needs at least "
                                           f"{AUC_MIN_N} of each before it separates 'wrong scale' from 'no order'")
            per_class[cname] = blk
        cells[name] = dict(detector=det, dataset=ds, sweep=f, classes=per_class)
        print(f"  {name}: " + ", ".join(f"{c} n={b['n_predictions']} ECE={100 * b['all_boxes']['ece_equal_mass']:.1f}%"
                                        for c, b in per_class.items()), flush=True)
    res = dict(tool="tools/eval_calibration.py detector", written=time.strftime("%Y-%m-%d %H:%M %Z"),
               code_sha=code_sha(), seed=SEED, bootstrap=BOOT, bins=NBINS,
               thresholds=a.thresholds, precision_targets=a.precision_targets,
               matching="greedy one-to-one at IoU >= 0.5, descending confidence (realxray_eval.sweep_matches)",
               definition=("a detector confidence is calibrated when, among boxes at that confidence, that share "
                           "is a true positive; the signed gap is mean confidence minus precision"),
               cells=cells, files=files)
    out = Path(os.path.expanduser(a.out))
    out.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out / "calibration_detector.json", "w"), indent=1, default=float)
    md = detector_report(res)
    (out / "CALIBRATION_DETECTOR.md").write_text(md, encoding="utf-8")
    print(md)
    if not a.no_fig:
        try:
            fig_detector(res, out)
        except Exception as e:  # noqa: BLE001
            print("figure skipped:", e)
    print(f"\nwrote {out}/calibration_detector.json and CALIBRATION_DETECTOR.md  ({time.time() - t0:.0f} s)")
    return 0


def _auc(conf, tp):
    """Does confidence RANK true boxes above false ones, whatever its absolute value means? A model can be badly
    calibrated and still rank perfectly; the two failures need different fixes."""
    tp = np.asarray(tp, bool)
    if tp.all() or not tp.any():
        return None
    o = np.argsort(np.asarray(conf, float), kind="mergesort")
    r = np.empty(len(conf), float)
    r[o] = np.arange(1, len(conf) + 1)
    # average ranks for ties
    cs = np.asarray(conf, float)
    for v in np.unique(cs):
        m = cs == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    n1 = int(tp.sum())
    n0 = len(tp) - n1
    return float((r[tp].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cell_status(det, ds):
    """DEVICE-HELD-OUT / SAME-DEVICE HELD-OUT CASE / IN-TRAINING-DEVICE, from the one place that defines it.
    A calibration gap on a device the arm trained on is a different statement from a gap on an unseen machine,
    and the table is unreadable without saying which."""
    try:
        from or_recall_curves import DETECTORS, DATASETS, STATUS, status as _st
        if det in DETECTORS and ds in DATASETS:
            k = _st(det, ds)
            return STATUS[k], k
    except Exception:  # noqa: BLE001
        pass
    return "?", "?"


def detector_report(r):
    L = ["# Does a detector confidence mean what it says, and what does 0.25 mean on each device?", "",
         f"{len(r['cells'])} arm x dataset cells. Matching: {r['matching']}. Code {r['code_sha']}, "
         f"{r['bootstrap']} case-cluster resamples.", "",
         r["definition"] + ".", "",
         "| arm | dataset | status | class | cases | truth boxes | pred boxes | ECE (all) | rank AUC | "
         "at 0.25: kept | precision [95% CI] | mean conf | signed gap (pp) | conf needed for 90 % precision |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, c in r["cells"].items():
        for cname, b in c["classes"].items():
            a25 = b.get("at_0.25") or {}
            n90 = (b.get("threshold_for_precision") or {}).get("0.9")
            auc = b.get("ranking_auc")
            sup = b.get("ranking_auc_support") or [None, None]
            auc_s = ("%.3f" % auc) if auc is not None else (
                "n/a (%s true, %s false)" % (sup[0], sup[1]) if sup[0] is not None else "n/a")
            gap = a25.get("signed_gap")
            gap_s = "n/a" if gap is None else "%+.1f" % (100 * gap)
            n90_s = ("not reachable" if not n90 else
                     "%.2f (keeps %d, recall %s %%, precision >= %s %% at 95 %%)"
                     % (n90["threshold"], n90["kept"], _pct(n90["recall"]), _pct(n90.get("precision_lower95"))))
            st, _k = cell_status(c["detector"], c["dataset"])
            L.append("| %s | %s | %s | %s | %d | %d | %d | %s | %s | %s | %s %s | %s | %s | %s |" % (
                c["detector"], c["dataset"], st, cname, b.get("cases", 0), b.get("n_truth", 0),
                b["n_predictions"], _pct(b["all_boxes"]["ece_equal_mass"], 2), auc_s,
                a25.get("kept", 0) if a25 else 0,
                _pct(a25.get("precision")), _ci(a25.get("precision_ci")) if a25.get("kept") else "[no boxes]",
                _pct(a25.get("mean_confidence")), gap_s, n90_s))
    L += ["", "A positive signed gap is a detector that says 0.25 and delivers less than 0.25; a negative gap is a "
              "detector whose boxes are better than their confidence claims. The rank AUC separates the two "
              "failures: a high AUC with a large gap means the ordering is usable and only the scale is wrong, "
              "which a per-device threshold fixes; a low AUC means no threshold fixes it.", "",
          "**Read the `truth boxes` and `cases` columns first.** A precision is a statement about how many truth "
          "objects the kept boxes found, and the collimated crop sets barely contain the anchor: the C-ArmLSpine "
          "3-vertebra set has 11 truth sacra across 175 frames and the 1-vertebra set has 13 across 287, so a "
          "sacrum precision of 0.0 % there is a statement about eleven objects and not a calibration curve. For "
          "the same reason a rank AUC is withheld wherever either class has fewer than five boxes; the column "
          "then prints how many true boxes there were. Two of the datasets -- DeepFluoro (one specimen) and the "
          "Geneva phantom -- are a SINGLE case, so no case-cluster interval exists for them at all and their "
          "rows print `[1 cluster]`; an interval that is absent is not an interval that is narrow.", "",
          "**Which box convention this is, and where it changes the reading.** These sweeps match at IoU >= 0.5 "
          "against the TIGHT BODY box. The same predictions matched against the vertebral OUTLINE reach a very "
          "different recall on C-ArmLSpine whole frames (rescore_outline.md: body 5.2 % against outline 90.6 % at "
          "0.25 for the held-out arm), because the predicted boxes are the right place and the wrong aspect "
          "(1.53 predicted against 1.45 body and 1.66 outline). A VERTEBRA precision here is therefore a joint "
          "statement about the confidence and the convention, and cannot be quoted as a calibration figure for a "
          "manuscript number measured under the outline rule. The SACRUM is not affected in that cell -- body and "
          "outline both give 83.9 % -- so the anchor's calibration below is convention-free, and the anchor is "
          "what the counting starts from.", ""]
    return "\n".join(L)


# ------------------------------------------------------------------------------------------------- figures
def _mpl():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": GRID_C,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True,
                         "grid.color": GRID_C, "grid.linewidth": 0.8, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF,
                         "legend.frameon": False})
    return plt


def fig_level(res, rows=None, conf=None, corr=None, cases=None, out=None):
    plt = _mpl()
    from _figfit import fit
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.4))
    # 1 reliability
    b = res["calibration_pooled"]["bins"]
    ax[0].plot([0, 1], [0, 1], color=INK2, lw=1.2, ls="--")
    ax[0].plot([x["conf"] for x in b], [x["accuracy"] for x in b], "-o", color=CAT[0], ms=4, lw=2)
    for x in b:
        ax[0].plot([x["conf"], x["conf"]], [x["conf"], x["accuracy"]], color=CAT[1], lw=1, alpha=0.7)
    ax[0].set_xlabel("confidence"); ax[0].set_ylabel("accuracy")
    c = res["calibration_pooled"]
    ax[0].set_title(f"reliability, {c['n']} vertebrae\nECE {100 * c['ece_equal_mass']:.2f} %"
                    f" (chance {100 * (c.get('ece_null_perfectly_calibrated') or {}).get('mean', float('nan')):.2f} %)",
                    color=INK, fontsize=12)
    # 2 signed gap by band length
    kk = list(res["calibration_by_band_length"].items())
    if kk:
        xs = np.arange(len(kk))
        g = [100 * v["signed_gap"] for _, v in kk]
        lo = [100 * (v["signed_gap_ci"][0] if v["signed_gap_ci"][0] is not None else v["signed_gap"]) for _, v in kk]
        hi = [100 * (v["signed_gap_ci"][1] if v["signed_gap_ci"][1] is not None else v["signed_gap"]) for _, v in kk]
        ax[1].bar(xs, g, color=[CAT[0] if v >= 0 else CAT[2] for v in g], width=min(0.62, 0.62))
        ax[1].errorbar(xs, g, yerr=[np.array(g) - np.array(lo), np.array(hi) - np.array(g)], fmt="none",
                       ecolor=INK2, lw=1.2, capsize=3)
        ax[1].axhline(0, color=INK2, lw=1)
        ax[1].set_xticks(xs)
        ax[1].set_xticklabels([str(k) for k, _ in kk])
        # A run filtered to ONE band length (every --view run, and the headline whole-frame run) left matplotlib
        # to autoscale a single category to +-0.5, so a bar of width 0.62 filled the whole panel and read as a
        # solid block rather than a bar. The panel is pinned to the categories it has, with a margin.
        pad = 0.8 if len(kk) > 2 else 1.5
        ax[1].set_xlim(-pad, len(kk) - 1 + pad)
        ax[1].set_xlabel("vertebrae in the band")
        ax[1].set_ylabel("confidence minus accuracy (pp)")
        ax[1].set_title("over-confidence by band length", color=INK, fontsize=12)
    # 3 risk-coverage, from the stored curve so the panel is reproducible from the result file alone
    cur = res["selective"].get("curve")
    if cur is None:
        cur = rc_curve(conf, corr)
    # The table refuses operating points inside a tied block of confidences, and the curve must refuse them too:
    # only 39 % of the prefixes on the real whole-frame data are rules, and below a quarter coverage only 13 of
    # 312 are, so a reader tracing the left arm reads coverages no threshold can produce. The implementable
    # points are drawn on top of the faint envelope, and the caption says which is which.
    cvv = np.asarray(cur["coverage"], float)
    acv = np.asarray(cur["accuracy"], float)
    imp = np.asarray(cur.get("implementable", np.ones(len(cvv), bool)), bool)
    ax[2].plot(cvv, acv, color=CAT[0], lw=1.0, alpha=0.30, label="envelope (incl. non-rules)")
    ax[2].plot(cvv[imp], acv[imp], color=CAT[0], lw=2, label="thresholds that exist")
    sh = res["selective"]["rules"]["shipped_compound"]
    if sh.get("accuracy_answered") is not None:
        ax[2].plot([sh["coverage"]], [sh["accuracy_answered"]], "o", color=CAT[1], ms=9, zorder=6,
                   markeredgecolor="white", markeredgewidth=1.2, label="shipped abstain rule")
    ax[2].axhline(0.99, color=INK2, lw=1, ls=":")
    ax[2].set_xlabel("coverage"); ax[2].set_ylabel("accuracy among answered")
    ax[2].set_title("risk-coverage", color=INK, fontsize=12)
    ax[2].legend(loc="upper right", fontsize=9.5)
    # 4 per level accuracy vs confidence
    pl = res["per_level"]
    xs = [v["mean_confidence"] for v in pl.values()]
    ys = [v["accuracy"] for v in pl.values()]
    ns = [max(12, 3 * math.sqrt(v["n"])) for v in pl.values()]
    ax[3].plot([0, 1], [0, 1], color=INK2, lw=1.2, ls="--")
    # a class with one or two vertebrae sits at accuracy 0 or 1 by arithmetic; the area encoding bottoms out at
    # 12 pt so it cannot say that, and the label is suppressed, leaving an unexplained dot. Draw those hollow.
    thin_i = [i for i, v in enumerate(pl.values()) if v["n"] < MACRO_MIN_N]
    fat_i = [i for i, v in enumerate(pl.values()) if v["n"] >= MACRO_MIN_N]
    if fat_i:
        ax[3].scatter([xs[i] for i in fat_i], [ys[i] for i in fat_i], s=[ns[i] for i in fat_i],
                      color=CAT[3], edgecolor=INK, lw=0.6, zorder=3)
    if thin_i:
        ax[3].scatter([xs[i] for i in thin_i], [ys[i] for i in thin_i], s=[ns[i] for i in thin_i],
                      facecolor="none", edgecolor=INK2, lw=1.0, zorder=3,
                      label=f"n < {MACRO_MIN_N}")
        ax[3].legend(loc="lower right", fontsize=9)
    for i, ((lv, v), x, y) in enumerate(zip(pl.items(), xs, ys)):
        if v["n"] >= 5:
            dx, dy = ((4, 5) if i % 2 == 0 else (4, -11))
            t = ax[3].annotate(lv, (x, y), fontsize=10, color=INK, xytext=(dx, dy), textcoords="offset points")
            fit(fig, t, 1.0)
    ax[3].set_xlabel("mean confidence"); ax[3].set_ylabel("accuracy")
    ax[3].set_title("per level (area ~ n)", color=INK, fontsize=12)
    # panels 0, 2 and 3 are all on a 0-1 axis; panel 1 is a bar chart indexed by band, and a shared xlim here
    # silently clipped it to its first two bars while the table beside it listed six. Rendering the figure is
    # what caught that, which is the second time in this project that a picture settled what numbers did not.
    for x in (ax[0], ax[2], ax[3]):
        x.set_xlim(0, 1.02)
    fig.tight_layout()
    # bbox_inches="tight" because the outer panels' centred titles and the y tick labels of the
    # last panel overflow a fixed 13-inch canvas: the saved PNG ended "...at 0.25 (p" and the first
    # title lost its leading letter. Trimming to the real extent is the only fix that cannot clip.
    fig.savefig(out / "fig_calibration_level.png", dpi=200, bbox_inches="tight", pad_inches=0.06)
    fig.savefig(out / "fig_calibration_level.pdf", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", out / "fig_calibration_level.png")


PRIMARY_HELD = {"lodo_carm__carm_test": "C-arm, whole frame", "lodo_carm__carm_k3": "C-arm, 3-vertebra field",
                "lodo_carm__carm_k1": "C-arm, 1-vertebra field", "lodo_cobra__cobra_test": "Elekta XVI",
                "lodo_df__df_test": "Cios Fusion", "pooled__geneva_all": "BV Pulsera phantom"}


def fig_detector(res, out):
    plt = _mpl()
    from _figfit import fit
    cells = res["cells"]
    # 21 device-held-out cells is 21 lines and a legend that covers the axes. Draw the arm each device is
    # actually held out of -- the cell the generalisation claim is made from -- and leave the rest to the table.
    keys = [k for k in PRIMARY_HELD if k in cells]
    if not keys:
        keys = [k for k in sorted(cells) if cell_status(cells[k]["detector"], cells[k]["dataset"])[1] == "held"][:6]
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for i, name in enumerate(keys):
        c = cells[name]
        lab = PRIMARY_HELD.get(name, name)
        for j, cname in enumerate(("vertebra", "sacrum")):
            b = c["classes"].get(cname)
            if not b:
                continue
            rows = b["all_boxes"]["bins"]
            ax[j].plot([x["conf"] for x in rows], [x["accuracy"] for x in rows], "-", color=CAT[i % len(CAT)],
                       lw=2, marker="o", ms=3, label=lab)
    for j, cname in enumerate(("vertebra", "sacrum")):
        ax[j].plot([0, 1], [0, 1], color=INK2, lw=1.2, ls=":")
        ax[j].axvline(0.25, color=INK2, lw=1.0, ls="--")
        ax[j].set_xlabel("detector confidence")
        ax[j].set_ylabel("share that is a true box")
        # the vertebra panel is matched against the TIGHT BODY box; the same predictions score very differently
        # under the outline convention, so the panel must say which rule drew it (see the note under the table)
        tt = ax[j].set_title(f"{cname} boxes (body box), device held out" if cname == "vertebra"
                             else f"{cname} boxes, device held out", color=INK, fontsize=12)
        fit(fig, tt, 3.8)
        ax[j].set_xlim(0, 1.02)
        ax[j].set_ylim(0, 1.02)
    if ax[0].get_legend_handles_labels()[0]:
        ax[0].legend(loc="upper left", fontsize=9.5, ncol=1)
    # panel 3: the question the project asked -- what does 0.25 deliver, per device
    labs, gaps, los, his, cols = [], [], [], [], []
    hatches = []
    for i, name in enumerate(keys):
        for cname, mark in (("vertebra", ""), ("sacrum", " (sacrum)")):
            b = cells[name]["classes"].get(cname)
            a25 = (b or {}).get("at_0.25") or {}
            if a25.get("signed_gap") is None or not a25.get("kept"):
                continue
            ci = a25.get("signed_gap_ci") or [None, None]
            # A bar with no interval is not a precise bar. DeepFluoro is one specimen and the Geneva phantom is
            # one object, so their case-cluster bootstrap cannot run at all and the first version drew them with
            # zero-length caps -- next to bars whose caps are honest, they read as the tightest estimates in the
            # panel. They are hatched and named instead.
            nocap = ci[0] is None
            labs.append(PRIMARY_HELD.get(name, name) + mark + (" [1 cluster]" if nocap else ""))
            gaps.append(100 * a25["signed_gap"])
            los.append(100 * ci[0] if not nocap else 100 * a25["signed_gap"])
            his.append(100 * ci[1] if not nocap else 100 * a25["signed_gap"])
            cols.append(CAT[i % len(CAT)])
            hatches.append("//" if nocap else "")
    y = np.arange(len(labs))
    bars = ax[2].barh(y, gaps, color=cols, height=0.7)
    for bar, h in zip(bars, hatches):
        if h:
            bar.set_hatch(h)
            bar.set_edgecolor("white")
            bar.set_linewidth(0.8)
    drawn = np.array([h == "" for h in hatches], bool)
    if drawn.any():
        ax[2].errorbar(np.asarray(gaps)[drawn], y[drawn],
                       xerr=[(np.array(gaps) - np.array(los))[drawn], (np.array(his) - np.array(gaps))[drawn]],
                       fmt="none", ecolor=INK2, lw=1.1, capsize=2)
    ax[2].axvline(0, color=INK2, lw=1)
    ax[2].set_yticks(y)
    ax[2].set_yticklabels(labs, fontsize=9)
    ax[2].invert_yaxis()
    # the long y tick labels push the axes right and the full sentence then ran off the canvas: the saved PNG
    # ended "...at 0.25 (p". Shortened and fitted to the panel.
    xl = ax[2].set_xlabel("conf. minus precision at 0.25 (pp)", fontsize=10)
    fit(fig, xl, 3.4)
    t = ax[2].set_title("what 0.25 delivers, by device", color=INK, fontsize=12)
    fit(fig, t, 3.0)
    fig.tight_layout()
    fig.savefig(out / "fig_calibration_detector.png", dpi=200, bbox_inches="tight", pad_inches=0.06)
    fig.savefig(out / "fig_calibration_detector.pdf", bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", out / "fig_calibration_detector.png")


# ------------------------------------------------------------------------------------------------- selftest
def cmd_selftest(a):
    """Every estimator here is checked against data whose answer is known by construction. A calibration tool that
    has not been run on a KNOWN miscalibration is a tool that reports plausible numbers."""
    rng = np.random.default_rng(7)
    K, N = 27, 8000
    fails = []

    def chk(name, cond, got):
        print(f"  {'PASS' if cond else 'FAIL'}  {name}: {got}")
        if not cond:
            fails.append(name)

    # a model with true logits, distorted by a KNOWN temperature
    z = rng.normal(0, 2.2, (N, K))
    y = np.array([rng.choice(K, p=np.exp(zz - zz.max()) / np.exp(zz - zz.max()).sum()) for zz in z])
    cases = [f"c{i // 6}" for i in range(N)]

    def probs_at(T):
        w = z / T
        w = w - w.max(1, keepdims=True)
        e = np.exp(w)
        return e / e.sum(1, keepdims=True)

    print("1. ECE of a perfectly calibrated model is at its own null")
    P1 = probs_at(1.0)
    c1, k1 = P1.max(1), (P1.argmax(1) == y).astype(float)
    e1, _, _ = ece_bins(c1, k1, NBINS, "equal_mass")
    nul = ece_null(c1, 200)
    chk("ECE(T=1) <= null p95", e1 <= nul["p95"] * 1.5, f"ECE {e1:.4f} vs null mean {nul['mean']:.4f} p95 {nul['p95']:.4f}")

    print("2. a KNOWN over-confidence is recovered with the right sign")
    P2 = probs_at(0.5)
    c2, k2 = P2.max(1), (P2.argmax(1) == y).astype(float)
    e2, _, _ = ece_bins(c2, k2, NBINS, "equal_mass")
    gap2 = c2.mean() - k2.mean()
    chk("sharpened model reads over-confident", gap2 > 0.05 and e2 > 3 * e1, f"gap {gap2:+.3f}, ECE {e2:.4f}")
    P3 = probs_at(2.0)
    c3, k3 = P3.max(1), (P3.argmax(1) == y).astype(float)
    chk("softened model reads under-confident", (c3.mean() - k3.mean()) < -0.02, f"gap {c3.mean() - k3.mean():+.3f}")

    print("3. temperature scaling recovers the temperature that was applied")
    lp = np.log(np.clip(P2, 1e-12, None))
    T, _, _ = temperature_fit(lp[:N // 2], y[:N // 2])
    chk("fitted T ~ 2.0 undoes T = 0.5", abs(T - 2.0) < 0.25, f"T = {T:.3f}")
    Q = temperature_apply(lp[N // 2:], T)
    eT, _, _ = ece_bins(Q.max(1), (Q.argmax(1) == y[N // 2:]).astype(float), NBINS, "equal_mass")
    chk("ECE falls after scaling", eT < e2 / 2, f"{e2:.4f} -> {eT:.4f}")

    print("4. Platt and isotonic recalibrate a top-1 confidence")
    w = platt_fit(c2[:N // 2], k2[:N // 2])
    ep, _, _ = ece_bins(platt_apply(w, c2[N // 2:]), k2[N // 2:], NBINS, "equal_mass")
    chk("Platt lowers ECE", ep < e2 / 2, f"{e2:.4f} -> {ep:.4f}")
    kn = isotonic_fit(c2[:N // 2], k2[:N // 2])
    ei, _, _ = ece_bins(isotonic_apply(kn, c2[N // 2:]), k2[N // 2:], NBINS, "equal_mass")
    chk("isotonic lowers ECE", ei < e2 / 2, f"{e2:.4f} -> {ei:.4f}")
    chk("isotonic map is non-decreasing", bool(np.all(np.diff(kn[1]) >= -1e-9)), f"{len(kn[0])} knots")

    print("5. conformal sets reach the coverage they promise")
    order = [f"L{i}" for i in range(K)]
    for al in (0.05, 0.10):
        for meth, mond in (("lac", False), ("aps", False), ("lac", True)):
            sets, _, _ = conformal_sets(P2[:N // 2], [order[i] for i in y[:N // 2]], P2[N // 2:], order, al, meth, mond)
            st = set_stats(sets, [order[i] for i in y[N // 2:]])
            chk(f"{meth}{'_mondrian' if mond else ''} alpha={al} coverage >= {1 - al:.2f} - 0.02",
                st["empirical_coverage"] >= 1 - al - 0.02,
                f"coverage {st['empirical_coverage']:.4f}, mean size {st['mean_set_size']:.2f}")

    print("6. the selective risk bound holds out of sample, and refuses when the risk is not reachable")
    # a generator whose achievable selective risk is known: P(correct | conf) = conf exactly
    u = rng.uniform(0.02, 0.999, 12000)
    uk = (rng.random(12000) < u)
    ucal = list(zip(u[:6000], uk[:6000]))
    utst = list(zip(u[6000:], uk[6000:]))
    # the property under test is VALIDITY (when it answers, the risk is bounded), never power: refusing to
    # certify a rate this many calibration items cannot support is the correct answer, not a failure
    for al in (0.05, 0.10, 0.20):
        s = selective_risk_control(ucal, utst, al)
        got = ("refused (not certifiable at n=%d)" % len(ucal) if s.get("threshold") is None else
               "thr %.3f, coverage %.3f, risk %.4f (bound %.4f)"
               % (s["threshold"], s["test_coverage"], s["test_risk"], s["test_risk_upper95"]))
        chk("risk control alpha=%s: refuses or holds" % al,
            s.get("threshold") is None or s["test_risk"] <= al + 0.02, got)
    # the same machinery on a model whose best selective risk is ~0.23: the honest answer is "no threshold"
    cal = list(zip(c2[:N // 2], k2[:N // 2].astype(bool)))
    tst = list(zip(c2[N // 2:], k2[N // 2:].astype(bool)))
    s = selective_risk_control(cal, tst, 0.05)
    top = float(1 - k2[np.argsort(-c2)[:200]].mean())
    chk("refuses alpha=0.05 when even the top 200 items err at %.0f %%" % (100 * top),
        s.get("threshold") is None, s.get("note", "returned a threshold"))
    # validity under repetition: the share of independent runs whose realised risk exceeds alpha
    exceed, ran = 0, 0
    for rep in range(200):
        r2 = np.random.default_rng(1000 + rep)
        uu = r2.uniform(0.02, 0.999, 12000)
        kk = (r2.random(12000) < uu)
        s2 = selective_risk_control(list(zip(uu[:6000], kk[:6000])), list(zip(uu[6000:], kk[6000:])), 0.10)
        if s2.get("threshold") is not None and s2.get("test_risk") is not None:
            ran += 1
            exceed += int(s2["test_risk"] > 0.10)
    chk("over 200 independent runs the realised risk exceeds alpha rarely",
        ran >= 20 and exceed / max(ran, 1) <= 0.12,
        "%d of the 200 runs returned a threshold; %d of those exceeded alpha=0.10 on the held-out half" % (ran, exceed))

    print("6b. clustered items break the per-item bound, and the design-effect correction repairs it")
    # a generator that fails in whole cases, which is what a spine does: the vertebrae of one frame go wrong
    # together, so the effective sample size is nearer the case count than the vertebra count
    def clustered(seed, n_case=260, per=8):
        r3 = np.random.default_rng(seed)
        cf, okv, cs = [], [], []
        for i in range(n_case):
            b = r3.random() < 0.5
            for _ in range(per):
                c = r3.uniform(0.55, 0.999)
                p = float(np.clip(c + (0.2 if b else -0.2), 0.0, 1.0))
                cf.append(c); okv.append(r3.random() < p); cs.append("case%d" % i)
        return np.asarray(cf), np.asarray(okv), cs

    AL = 0.20
    ex_naive = ex_clust = ran_n = ran_c = 0
    deffs = []
    for rep in range(60):
        cf, okv, cs = clustered(5000 + rep)
        h = len(cf) // 2
        cal, tst = list(zip(cf[:h], okv[:h])), list(zip(cf[h:], okv[h:]))
        sn = selective_risk_control(cal, tst, AL, cluster=False)
        sc = selective_risk_control(cal, tst, AL, cal_cases=cs[:h], test_cases=cs[h:], cluster=True)
        if sn.get("test_risk") is not None:
            ran_n += 1; ex_naive += int(sn["test_risk"] > AL)
        if sc.get("test_risk") is not None:
            ran_c += 1; ex_clust += int(sc["test_risk"] > AL)
            deffs.append(sc.get("design_effect", 1.0))
    rn = ex_naive / max(ran_n, 1); rcl = ex_clust / max(ran_c, 1)
    chk("both bounds were exercised on clustered data", ran_n >= 30 and ran_c >= 20,
        "per-item returned a threshold in %d/60 runs, clustered in %d/60" % (ran_n, ran_c))
    chk("the correction does not exceed alpha more often than the per-item bound", rcl <= rn + 1e-9,
        "per-item %d/%d = %.3f, clustered %d/%d = %.3f" % (ex_naive, ran_n, rn, ex_clust, ran_c, rcl))
    chk("the measured design effect is above 1 on clustered data", bool(deffs) and float(np.median(deffs)) > 1.2,
        "median deff %.2f over %d runs" % (float(np.median(deffs)) if deffs else float("nan"), len(deffs)))

    print("7. risk-coverage is monotone where confidence ranks correctness")
    cur = rc_curve(c2, k2)
    chk("accuracy at 50 % coverage beats full coverage", cur["accuracy"][N // 2] > cur["accuracy"][-1],
        f"{cur['accuracy'][N // 2]:.4f} vs {cur['accuracy'][-1]:.4f}")
    chk("acc_at_coverage agrees with the curve", abs(acc_at_coverage(c2, k2, 1.0)["accuracy"] - k2.mean()) < 1e-9,
        f"{acc_at_coverage(c2, k2, 1.0)['accuracy']:.6f}")

    print("8. a detector whose confidence IS its precision reads calibrated; one that is not, does not")
    cc = rng.uniform(0.01, 0.99, 6000)
    good = (rng.random(6000) < cc).astype(float)
    eg, _, _ = ece_bins(cc, good, NBINS, "equal_mass")
    bad = (rng.random(6000) < np.clip(cc - 0.3, 0, 1)).astype(float)
    eb, _, _ = ece_bins(cc, bad, NBINS, "equal_mass")
    chk("honest detector ECE small", eg < 0.03, f"{eg:.4f}")
    chk("30 pp over-confident detector is caught", abs(eb - 0.3) < 0.06, f"{eb:.4f} (truth 0.30)")
    chk("rank AUC ~ 0.5 when confidence carries no ranking", abs(_auc(rng.random(4000), rng.integers(0, 2, 4000)) - 0.5) < 0.05,
        f"{_auc(rng.random(4000), rng.integers(0, 2, 4000)):.3f}")

    print("9. the case-cluster bootstrap is wider than an item bootstrap when cases are correlated")
    cor = np.repeat(rng.random(N // 6) < 0.5, 6)[:N].astype(float)
    ci_case = boot_cases(cases, list(cor), lambda v: float(np.mean(v)), n=400)
    ci_item = boot_cases([str(i) for i in range(N)], list(cor), lambda v: float(np.mean(v)), n=400)
    chk("case CI wider than item CI", (ci_case[1] - ci_case[0]) > 1.5 * (ci_item[1] - ci_item[0]),
        f"case {ci_case[1] - ci_case[0]:.4f} vs item {ci_item[1] - ci_item[0]:.4f}")

    print("10. the reporting guards: a missing number must not print as a measured one")
    chk("a missing CI and a single-cluster CI print differently",
        _ci(None) != _ci([None, None]) and "no CI" in _ci(None),
        f"{_ci(None)!r} vs {_ci([None, None])!r}")
    # a percentile bootstrap of a proportion at its boundary has ZERO width and would be printed as a 95 %
    # interval; the exact interval that replaces it must actually contain something
    zero_boot = boot_cases([f"c{i // 4}" for i in range(40)], [0.0] * 40, lambda v: float(np.mean(v)), n=200)
    lo_e = clopper_pearson_lower(0, 26, 0.025)
    hi_e = 1.0 - clopper_pearson_lower(26, 26, 0.025)
    chk("a 0-of-n proportion bootstraps to zero width, and the exact interval does not",
        (zero_boot[1] - zero_boot[0]) == 0.0 and hi_e > 0.05,
        f"bootstrap [{zero_boot[0]:.3f}, {zero_boot[1]:.3f}] against exact [{lo_e:.3f}, {hi_e:.3f}] for 0/26")
    # a macro average must not be moved by a class with one member
    fake = {"L1": dict(n=300, accuracy=0.95), "L2": dict(n=300, accuracy=0.95), "X": dict(n=1, accuracy=0.0)}
    m_all = float(np.mean([v["accuracy"] for v in fake.values()]))
    keep = {k: v for k, v in fake.items() if v["n"] >= MACRO_MIN_N}
    m_min = float(np.mean([v["accuracy"] for v in keep.values()]))
    chk("the minimum-n macro ignores a one-member class that moves the unrestricted one by 30 pp",
        abs(m_all - 0.6333) < 1e-3 and abs(m_min - 0.95) < 1e-9,
        f"all classes {m_all:.4f}, n >= {MACRO_MIN_N} {m_min:.4f}")
    chk("a rank AUC on one positive is withheld, not printed",
        AUC_MIN_N >= 2 and _auc(np.arange(10) / 10.0, np.array([0] * 9 + [1], bool)) == 1.0,
        f"the raw estimator returns 1.000 from a single positive; AUC_MIN_N = {AUC_MIN_N} suppresses it")
    chk("the cluster key prefers the CT subject over the render name",
        cluster_key_of(dict(case="ctsp_0001_ap_p3", group="0001")) == ("0001", "group")
        and cluster_key_of(dict(case="gl003")) == ("gl003", "case"),
        f"{cluster_key_of(dict(case='ctsp_0001_ap_p3', group='0001'))}")
    # a risk-coverage curve over rounded scores must refuse prefixes inside a tied block
    tied = np.repeat([0.9, 0.8, 0.7], 5)
    cur2 = rc_curve(tied, np.array([1, 1, 1, 1, 0] * 3, bool))
    chk("only tie boundaries are implementable operating points", int(cur2["implementable"].sum()) == 3,
        f"{int(cur2['implementable'].sum())} of {len(tied)} prefixes are rules")

    print("")
    if fails:
        print("SELFTEST FAILED:", ", ".join(fails))
        return 1
    print("SELFTEST OK")
    return 0


def cmd_report(a):
    """Rewrite the markdown (and, for the detector, the figure) from a result JSON already on disk. Every number
    in the report comes out of that file, so a wording or a table fix never costs a recomputation and never
    risks a number moving between the JSON and the prose that quotes it."""
    res = json.load(open(os.path.expanduser(a.result), encoding="utf-8"))
    out = Path(os.path.expanduser(a.out or str(Path(os.path.expanduser(a.result)).parent)))
    out.mkdir(parents=True, exist_ok=True)
    kind = res.get("tool", "")
    if "detector" in kind:
        md = detector_report(res)
        (out / "CALIBRATION_DETECTOR.md").write_text(md, encoding="utf-8")
        if not a.no_fig:
            try:
                fig_detector(res, out)
            except Exception as e:  # noqa: BLE001
                print("figure skipped:", e)
    else:
        md = level_report(res)
        (out / "CALIBRATION_LEVEL.md").write_text(md, encoding="utf-8")
        if not a.no_fig and res.get("selective", {}).get("curve"):
            try:
                fig_level(res, out=out)
            except Exception as e:  # noqa: BLE001
                print("figure skipped:", e)
        elif not a.no_fig:
            print("(this result file predates the stored risk-coverage curve; re-run `level` to redraw the figure)")
    print(md)
    return 0


def main() -> int:
    global BOOT
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("level", help="calibration + selective + conformal for the level model")
    p.add_argument("--scores", nargs="*", default=[], help="glob(s) of tools/carmlspine_eval.py score_k*.json")
    p.add_argument("--posteriors", default=None, help="tools/level_posteriors.py jsonl (full vectors: enables SETS)")
    p.add_argument("--out", required=True)
    p.add_argument("--boxes", default=None, choices=[None, "det", "oracle"], help="filter the score files")
    p.add_argument("--view", default=None, help="LAT or AP")
    p.add_argument("--k", default=None, help="band length: full, 5 .. 1")
    p.add_argument("--cal-frac", type=float, default=0.5, help="share of CASES used to fit every calibrator")
    p.add_argument("--alpha", type=float, nargs="*", default=[0.01, 0.05, 0.10])
    p.add_argument("--boot", type=int, default=BOOT, help="case-cluster bootstrap resamples")
    p.add_argument("--no-fig", action="store_true")
    p.set_defaults(fn=cmd_level)

    d = sub.add_parser("detector", help="is a detector confidence a probability? per device")
    d.add_argument("--sweeps", nargs="+", required=True, help="glob(s) of or_ready/*/sweeps/<arm>__<dataset>.json")
    d.add_argument("--out", required=True)
    d.add_argument("--thresholds", type=float, nargs="*", default=[0.25, 0.5])
    d.add_argument("--precision-targets", type=float, nargs="*", default=[0.9, 0.95])
    d.add_argument("--nulls", type=int, default=200)
    d.add_argument("--boot", type=int, default=BOOT, help="case-cluster bootstrap resamples")
    d.add_argument("--no-fig", action="store_true")
    d.set_defaults(fn=cmd_detector)

    q = sub.add_parser("report", help="rewrite the markdown/figure from a result JSON, with no recomputation")
    q.add_argument("--result", required=True)
    q.add_argument("--out", default=None)
    q.add_argument("--no-fig", action="store_true")
    q.set_defaults(fn=cmd_report)

    s = sub.add_parser("selftest", help="every estimator against data whose answer is known by construction")
    s.set_defaults(fn=cmd_selftest)

    a = ap.parse_args()
    if getattr(a, "boot", None):
        BOOT = int(a.boot)
    if a.cmd == "level" and not a.scores and not a.posteriors:
        ap.error("level needs --scores or --posteriors")
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
