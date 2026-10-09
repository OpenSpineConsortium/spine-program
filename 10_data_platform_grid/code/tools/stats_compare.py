#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/stats_compare.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""The statistical machinery the paper's comparisons need, in one place, with the assumption of each test written
beside it and the failure mode it exists to stop.

WHY THIS FILE EXISTS. Every headline in this project is a proportion measured over vertebrae or frames that are
grouped inside a handful of patients, and every comparative claim is two such proportions measured on the SAME
patients. Both facts break the interval and the test that a reader would otherwise assume:

  1. FRAMES OF ONE CASE ARE NOT INDEPENDENT.  The C-ArmLSpine lateral result is 617 vertebrae -- but they come
     from 141 cases, roughly four to five vertebrae each, and a case that is dark, collimated or instrumented is
     wrong on all of them together. A binomial interval on 617 assumes 617 independent draws and is therefore too
     narrow; how much too narrow is a property of the data, not a guess, and `prop` measures it (the design effect
     and the effective sample size are printed beside the point estimate). Use the case-cluster bootstrap.

  2. TWO ARMS ON THE SAME CASES ARE NOT TWO INDEPENDENT SAMPLES.  Render-trained against film-trained detector on
     the same 233 bodies; lateral against AP on the same cases; the nine-term card against uncalibrated physics on
     the same six folds. Comparing two marginal percentages, or checking whether two confidence intervals overlap,
     is the wrong test and throws away the pairing that makes the comparison sensitive. Use `paired`, which reports
     the CI of the DIFFERENCE (the quantity a "beats" claim is about) and McNemar's exact test beside it.

  3. A P VALUE IS NOT AN EFFECT.  On 600 vertebrae a half-point difference can be "significant" and invisible to a
     surgeon. Every comparison here carries a difference in percentage points with an interval, and Cohen's h.

  4. MANY TESTS, ONE PAPER.  Nine physics terms, six devices, six folds, five arms: some p value will be small.
     `adjust` applies Holm (control the chance of ANY false claim) or Benjamini-Hochberg (control the share of
     false claims among those called). See adjust()'s docstring for when NOT to adjust -- a pre-stated primary
     comparison is not adjusted for the exploratory ones around it.

  5. AN EXPERIMENT THAT CANNOT PASS ITS OWN CRITERION.  The plan pre-states "counting grade = >= 97 % sacrum found
     and >= 97 % vertebra recall" and the held-out-device test is 28 cases. `power-criterion` computes how often a
     truly-90 % system passes a >= 97 % criterion at that n (often enough to matter), and `plan` says how many
     cases a prospective phantom / cadaver / human arm would need. These are design calculations from stated
     assumptions, never measurements, and the tool labels them as such in its output.

  6. THE CLUSTER BOOTSTRAP ITSELF FAILS NEAR THE CEILING, AND THAT IS WHERE THIS PROJECT LIVES. Every headline
     here is 0.91-0.99. Measured against a known truth (test_ceiling_coverage in tools/test_stats_compare.py):
     at p = 0.94 with fold 0's clustering the nominal-95 % case-cluster interval covers 85 %, at p = 0.97 with
     the lateral clustering 68-76 %, and at p = 0.98 with the two-frames-per-case layout of the held-out-device
     test 56 % -- while the naive Wilson interval, the one point 1 warns against, covers 95 % there. Below the
     ceiling the ranking is the other way round (p = 0.85: naive 59-70 %, cluster 90-95 %). Both are true; the
     library reports both and `ceiling_warning` says which regime you are in. Near the ceiling the defensible
     report is the numerator, the denominator, the case count and how many cases carry every error -- not an
     interval. The same discreteness breaks `paired`: when only a handful of cases disagree, "excludes zero" is
     decided by how few cases they land in rather than by the effect, so `excludes_zero_fragile` and an exact
     sign test over cases are reported beside it.

WHAT IS NOT HERE, DELIBERATELY. No test invents data. Every subcommand reads records from a file on disk and the
JSON it writes names that file, the seed, the resample count and the code SHA, so a number can be traced back.
The SHA is useless if the tree is dirty, so `meta` carries `code_dirty` and says so.

    # one proportion, case-clustered, beside the naive binomial interval it replaces
    python tools/stats_compare.py prop --rows cv_fold0_det_kfull.json --record-path 'frames[].items[]' \
        --cluster case --value exact --where view=LAT

    # two detector arms scored on the same frames: CI of the difference + McNemar
    python tools/stats_compare.py paired --rows-a lodo_carm__carm_test.json --rows-b lodo_cobra__carm_test.json \
        --record-path 'frames[]' --key stem --cluster case --value sacrum_found

    # a difference in means over folds (the physics-card comparisons)
    python tools/stats_compare.py perm --x docs/devices/elekta_xvi.json:fit.R2_held_out_by_fold \
                                       --y docs/devices/pixium_4600.json:fit.R2_held_out_by_fold

    python tools/stats_compare.py adjust --p sacrum=0.004 --p vertebra=0.03 --p naming=0.21 --method holm
    python tools/stats_compare.py power-criterion --n 28 --threshold 0.97 --p-true 0.90
    python tools/stats_compare.py plan --arm phantom:0.97:0.90 --arm cadaver:0.95:0.90 --icc 0.25 --items-per-case 5

Import it instead of copying: `from stats_compare import boot_proportion, paired_compare, adjust`.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from statistics import NormalDist

import numpy as np

TOOL = "tools/stats_compare.py"
ND = NormalDist()


# --------------------------------------------------------------------------------------------------- housekeeping
def code_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=str(Path(__file__).resolve().parents[1])).decode().strip()
    except Exception:  # noqa: BLE001
        return None


def code_dirty():
    """True when THIS file differs from the commit `code_sha` names. Without it the meta block is a false
    attribution: a result written from an uncommitted working tree carries a SHA whose content did not produce
    it, which is exactly the traceability the meta block exists to provide."""
    try:
        out = subprocess.check_output(["git", "status", "--porcelain", "--", str(Path(__file__).resolve())],
                                      cwd=str(Path(__file__).resolve().parents[1])).decode().strip()
        return bool(out)
    except Exception:  # noqa: BLE001
        return None


def meta(inputs, seed=None, **kw):
    """The block every result JSON carries, so a number can be attributed to a run (plan box E4)."""
    dirty = code_dirty()
    d = dict(tool=TOOL, code_sha=code_sha(), code_dirty=dirty, date=time.strftime("%Y-%m-%d %H:%M:%S"),
             inputs=[str(i) for i in (inputs if isinstance(inputs, (list, tuple)) else [inputs]) if i],
             python=sys.version.split()[0], numpy=np.__version__)
    if dirty:
        d["code_sha_note"] = ("the working copy of this tool differs from that commit: the SHA does NOT identify "
                              "the code that produced this number; commit before quoting it")
    if seed is not None:
        d["seed"] = int(seed)
    d.update(kw)
    return d


def as_bool(v):
    """0/1 from bool, int, float or the usual strings. Raises rather than guessing -- a silent coercion of an
    unexpected value to False is exactly how a proportion comes out plausible and wrong."""
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, np.integer)):
        if v in (0, 1):
            return int(v)
    if isinstance(v, (float, np.floating)):
        if v in (0.0, 1.0):
            return int(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("1", "true", "t", "yes", "y"):
            return 1
        if s in ("0", "false", "f", "no", "n"):
            return 0
    raise ValueError(f"not a 0/1 outcome: {v!r}")


# ------------------------------------------------------------------------------------------- interval primitives
def wilson(k, n, alpha=0.05):
    """Wilson score interval. ASSUMES n independent Bernoulli draws. On clustered data (frames of one case) it is
    too narrow -- it is kept here as the naive reference the cluster bootstrap is reported against, never as the
    interval for a per-vertebra proportion."""
    if n <= 0:
        return (0.0, 1.0)
    z = ND.inv_cdf(1 - alpha / 2)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _log_binom_pmf(k, n, p):
    if k < 0 or k > n:
        return -math.inf
    if p <= 0.0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if k == n else -math.inf
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))


def _logsumexp(vals):
    vals = [v for v in vals if v > -math.inf]
    if not vals:
        return -math.inf
    m = max(vals)
    return m + math.log(sum(math.exp(v - m) for v in vals))


def binom_sf(k, n, p):
    """P(X >= k) for X ~ Binomial(n, p), in log space so it is stable at n in the thousands and p near 1."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return min(1.0, math.exp(_logsumexp([_log_binom_pmf(i, n, p) for i in range(int(k), n + 1)])))


def binom_cdf(k, n, p):
    """P(X <= k)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, math.exp(_logsumexp([_log_binom_pmf(i, n, p) for i in range(0, int(k) + 1)])))


def clopper_pearson(k, n, alpha=0.05):
    """Exact (conservative) two-sided interval. ASSUMES independence like Wilson; used for counts that really are
    one draw per unit (e.g. 54 independent L6 runs) and as the exact reference in the tests."""
    if n <= 0:
        return (0.0, 1.0)
    try:
        from scipy.stats import beta
        lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
        hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
        return (lo, hi)
    except Exception:  # noqa: BLE001
        lo = 0.0 if k == 0 else _bisect(lambda p: binom_sf(k, n, p) - alpha / 2, 0.0, 1.0)
        hi = 1.0 if k == n else _bisect(lambda p: binom_cdf(k, n, p) - alpha / 2, 0.0, 1.0)
        return (lo, hi)


def clopper_pearson_lower(k, n, alpha=0.05):
    """One-sided exact lower bound -- the form a safety claim takes ("at least X % with 95 % confidence")."""
    if n <= 0:
        return 0.0
    if k >= n:
        return alpha ** (1.0 / n)
    if k <= 0:
        return 0.0
    try:
        from scipy.stats import beta
        return float(beta.ppf(alpha, k, n - k + 1))
    except Exception:  # noqa: BLE001
        return _bisect(lambda p: binom_sf(k, n, p) - alpha, 0.0, 1.0)


def _bisect(f, lo, hi, tol=1e-10, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------------------- case-cluster bootstrap
def _boot_ratios(rng, k, n, n_boot, num2=None):
    """Bootstrap ratio-of-sums over clusters, in blocks so memory stays bounded. The naive form allocates a
    (n_boot, C) index matrix plus two gathers of the same shape; at 10 000 resamples and a few thousand clusters
    that is over a gigabyte, which on a --mem=8G grid job is a crash rather than a number. Blocks keep it at a
    few MB whatever n_boot and C are. If `num2` is given the SAME resample drives both numerators, which is what
    makes the paired comparison paired."""
    C = len(k)
    n_boot = int(n_boot)
    block = max(1, min(n_boot, int(2_000_000 // max(C, 1)) or 1))
    out, out2 = [], []
    done = 0
    while done < n_boot:
        b = min(block, n_boot - done)
        idx = rng.integers(0, C, size=(b, C))
        den = n[idx].sum(1)
        out.append(k[idx].sum(1) / den)
        if num2 is not None:
            out2.append(num2[idx].sum(1) / den)
        done += b
    return (np.concatenate(out), np.concatenate(out2) if num2 is not None else None)


def cluster_arrays(rows, cluster, value):
    """(names, successes per cluster, items per cluster). One cluster = one patient/case: the unit that is
    exchangeable. Choosing the cluster too small (the frame) leaves the correlation in; too large (the device)
    throws away almost all the resolution."""
    by = collections.OrderedDict()
    for r in rows:
        if cluster not in r:
            raise KeyError(f"record has no cluster field {cluster!r}: keys={sorted(r)[:12]}")
        c = str(r[cluster])
        v = as_bool(r[value])
        k, n = by.get(c, (0, 0))
        by[c] = (k + v, n + 1)
    names = list(by)
    return names, np.array([by[c][0] for c in names], float), np.array([by[c][1] for c in names], float)


def boot_proportion(rows, cluster, value, n_boot=10000, seed=0, alpha=0.05):
    """Case-cluster bootstrap of a proportion: resample CASES with replacement, keep every item of a drawn case,
    recompute sum(correct)/sum(items), take percentiles.

    ASSUMES cases are exchangeable and there are enough of them for the percentile method (below ~20 clusters the
    interval is unreliable and the result carries a `warning`). It makes no assumption about how items correlate
    inside a case, which is the point.

    FAILURE MODE AVOIDED: a binomial interval on the item count, which on this project's data is 1.5-2x too narrow
    and would let a difference that is within case-to-case noise be reported as established. `design_effect` is the
    measured variance ratio (cluster variance / binomial variance) and `n_effective` is the item count divided by
    it -- the honest denominator.

    FAILURE MODE *NOT* AVOIDED, AND MEASURED: near the ceiling this interval stops covering. test_ceiling_coverage()
    in tools/test_stats_compare.py measures it against a known truth at the shapes this project's own results have:
    at p = 0.94 with fold 0's all-view clustering the nominal-95 % interval covers 85 %, at p = 0.97 with the
    lateral clustering 68-76 %, and at p = 0.98 with the two-frames-per-case layout of the held-out-device test
    56 % -- where the *naive* Wilson interval covers 95 %. The mechanism is visible in `ci_degenerate`: when every
    resampled case is perfect the percentile interval collapses onto the point estimate, so the failures are
    almost all in one direction (the interval sits ABOVE the truth and claims more than the data support). The
    driver is `clusters_with_error`: when a handful of cases carry every error, resampling cases cannot describe
    the uncertainty. `ceiling_warning` fires in that regime. There is no drop-in replacement -- a Clopper-Pearson
    bound on the effective n was measured too and reaches only 70-100 % one-sided coverage over the same shapes --
    so the honest move near the ceiling is to report the numerator and denominator and the count of imperfect
    cases, not an interval."""
    names, k, n = cluster_arrays(rows, cluster, value)
    C, N, K = len(names), float(n.sum()), float(k.sum())
    if C == 0 or N == 0:
        return dict(p=None, n_items=0, n_clusters=0, note="no records")
    p = K / N
    out = dict(p=p, successes=int(K), n_items=int(N), n_clusters=C,
               items_per_cluster=float(N / C), n_boot=int(n_boot), seed=int(seed), alpha=alpha)
    wlo, whi = wilson(int(K), int(N), alpha)
    out["naive_wilson"] = [wlo, whi]
    out["naive_width_pp"] = 100 * (whi - wlo)
    if C < 2:
        out.update(ci=[None, None], warning="one cluster: no case-level interval is possible")
        return out
    rng = np.random.default_rng(seed)
    ratios, _ = _boot_ratios(rng, k, n, n_boot)
    lo, hi = np.percentile(ratios, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    out["ci"] = [float(lo), float(hi)]
    out["width_pp"] = float(100 * (hi - lo))
    out["boot_sd"] = float(ratios.std(ddof=1))
    # Monte-Carlo error of the ENDPOINTS themselves, from batch means. A percentile from B resamples is an
    # estimate too: at the old default of 2000 the lower end of fold 0's all-view interval moves +-0.27 pp
    # across seeds (86.24-87.16), and the implied ICC of its lateral subset moves 0.85-1.00 -- so an endpoint
    # quoted to two decimals from 2000 resamples is quoting noise. Raise n_boot until this is below the last
    # digit you intend to print.
    g = 20
    if int(n_boot) >= 4 * g:
        b = (int(n_boot) // g) * g
        batches = ratios[:b].reshape(g, -1)
        qlo = np.percentile(batches, 100 * alpha / 2, axis=1)
        qhi = np.percentile(batches, 100 * (1 - alpha / 2), axis=1)
        out["ci_mc_se_pp"] = [float(100 * qlo.std(ddof=1) / math.sqrt(g)),
                              float(100 * qhi.std(ddof=1) / math.sqrt(g))]
    out["ci_degenerate"] = bool(hi - lo < 1e-12)
    out["clusters_with_error"] = int(np.sum(k < n))
    binom_sd = math.sqrt(max(p * (1 - p), 1e-12) / N)
    out["design_effect"] = float((out["boot_sd"] / binom_sd) ** 2) if binom_sd > 0 else None
    out["n_effective"] = float(N / out["design_effect"]) if out["design_effect"] else None
    out["width_ratio_vs_naive"] = float(out["width_pp"] / out["naive_width_pp"]) if out["naive_width_pp"] else None
    # ICC implied by the measured design effect, for planning the prospective arms (Kish, equal-size approximation).
    # Clamped to [0, 1]: a design effect above the items-per-case would imply an impossible correlation and is a
    # sign of too few clusters, not of correlation above 1.
    m = N / C
    if out["design_effect"] and m > 1:
        raw = (out["design_effect"] - 1) / (m - 1)
        out["icc_implied"] = float(min(max(raw, 0.0), 1.0))
        if raw > 1.0 or raw < 0.0:
            out["icc_note"] = f"raw ICC estimate {raw:.2f} clamped into [0,1]; it is unstable at {C} clusters"
    else:
        out["icc_implied"] = None
    if C < 20:
        out["warning"] = f"only {C} clusters: percentile bootstrap intervals are unreliable below about 20"
    # Near-ceiling guard. Measured, not asserted: see test_ceiling_coverage() and boot_proportion's docstring.
    # `pin` is the probability a resample contains no imperfect case at all, which is when the percentile
    # interval collapses onto the point estimate. A first version of this guard triggered on `clusters_with_error
    # < 10` alone and fired on half the replicates at p = 0.85, where coverage is in fact 93 % -- a warning that
    # fires where nothing is wrong is noise, so the trigger is the regime the coverage run actually found broken.
    few = out["clusters_with_error"]
    pin = ((C - few) / C) ** C if C else 1.0
    out["resample_all_perfect_prob"] = float(pin)
    if out["ci_degenerate"] or pin > alpha / 2 or (p >= 0.90 and C < 100):
        out["ceiling_warning"] = (
            f"near the ceiling: {few} of {C} cases carry every error"
            + (" and the percentile interval has collapsed to a point" if out["ci_degenerate"] else "")
            + f". Measured coverage of this nominal {100*(1-alpha):.0f} % interval at shapes like this one is "
              f"56-85 %, not 95 % (test_ceiling_coverage in tools/test_stats_compare.py), and it fails by sitting "
              f"ABOVE the truth. Report {int(K)}/{int(N)} over {C} cases and the {few} imperfect "
              f"case{'' if few == 1 else 's'}; do not "
              f"quote this interval as a 95 % interval.")
    return out


def boot_statistic(rows, cluster, fn, n_boot=10000, seed=0, alpha=0.05):
    """Case-cluster bootstrap of ANY statistic fn(list of rows) -> float or None (F1, AP, a mean, a rate over a
    subset). Slower than boot_proportion because fn is re-evaluated per resample; same assumptions."""
    by = collections.defaultdict(list)
    for r in rows:
        by[str(r[cluster])].append(r)
    names = sorted(by)
    if len(names) < 2:
        return dict(point=fn(rows) if rows else None, ci=[None, None], n_clusters=len(names),
                    warning="fewer than two clusters")
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(int(n_boot)):
        pick = rng.integers(0, len(names), len(names))
        v = fn([r for i in pick for r in by[names[i]]])
        if v is not None:
            vals.append(float(v))
    lo, hi = (np.percentile(vals, [100 * alpha / 2, 100 * (1 - alpha / 2)]) if vals else (None, None))
    return dict(point=fn(rows), ci=[float(lo), float(hi)] if vals else [None, None],
                n_clusters=len(names), n_boot=int(n_boot), seed=int(seed),
                boot_sd=float(np.std(vals, ddof=1)) if len(vals) > 1 else None)


def boot_diff_unpaired(rows_a, rows_b, cluster, value, n_boot=10000, seed=0, alpha=0.05):
    """Difference of two proportions measured on DIFFERENT cases (e.g. two devices). Clusters are resampled
    independently in each arm. Prefer paired_compare whenever the two arms saw the same cases -- an unpaired
    interval on paired data is wider than it needs to be and can miss a real difference."""
    na, ka, nna = cluster_arrays(rows_a, cluster, value)
    nb, kb, nnb = cluster_arrays(rows_b, cluster, value)
    shared = set(na) & set(nb)
    pa, pb = ka.sum() / nna.sum(), kb.sum() / nnb.sum()
    rng = np.random.default_rng(seed)
    da_, _ = _boot_ratios(rng, ka, nna, n_boot)
    db_, _ = _boot_ratios(rng, kb, nnb, n_boot)
    d = da_ - db_
    lo, hi = np.percentile(d, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    out = dict(p_a=float(pa), p_b=float(pb), diff=float(pa - pb), diff_pp=float(100 * (pa - pb)),
               ci=[float(lo), float(hi)], ci_pp=[float(100 * lo), float(100 * hi)],
               excludes_zero=bool(lo > 0 or hi < 0), n_clusters_a=len(na), n_clusters_b=len(nb),
               n_items_a=int(nna.sum()), n_items_b=int(nnb.sum()), n_boot=int(n_boot), seed=int(seed),
               paired=False,
               newcombe_ci_pp=[100 * v for v in newcombe_diff(int(ka.sum()), int(nna.sum()),
                                                              int(kb.sum()), int(nnb.sum()), alpha)],
               newcombe_note=("NAIVE reference only: Newcombe assumes independent items in each arm. It is "
                              "printed beside the cluster interval so the cost of ignoring clustering is "
                              "visible, and must never be quoted as the interval for clustered data."))
    if shared:
        out["warning"] = (f"{len(shared)} case ids appear in BOTH arms -- these are paired data; "
                          f"use `paired` (an unpaired interval here is too wide and discards the pairing)")
    return out


def mcnemar_exact(b, c):
    """Exact two-sided McNemar: b = A right & B wrong, c = B right & A wrong, tested against 0.5.

    TWO WAYS IT MISLEADS, in opposite directions, and both have been seen in this project's own data:

      too small -- it ASSUMES the discordant pairs are INDEPENDENT. When several vertebrae of one case flip
                   together the effective number of independent disagreements is far smaller than the count, and
                   the p value is anti-conservative (measured in tools/test_stats_compare.py: 18 % false positives
                   at a nominal 5 % on clustered synthetic data).
      too large  -- it cannot be small when the disagreements are few. With d discordant pairs the smallest
                   attainable two-sided p is mcnemar_floor(d) = 2^(1-d), so d < 6 can never reach 0.05 however
                   lopsided the split. On the two held-out-device detector arms (56 shared frames, 4 discordant,
                   all one way) McNemar returns exactly its floor of 0.125 while the paired case-cluster interval
                   on the same data is [-14.3, -1.8] pp and excludes zero.

    So: report McNemar because reviewers expect it, make the claim from the paired bootstrap's interval, and when
    the floor is above alpha say so rather than writing "no significant difference"."""
    n = int(b) + int(c)
    if n == 0:
        return 1.0
    k = min(int(b), int(c))
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / (2.0 ** n)
    return float(min(1.0, 2 * tail))


def mcnemar_floor(d):
    """Smallest two-sided p McNemar can return with d discordant pairs: 2^(1-d), capped at 1. If this exceeds
    your alpha, the test had no chance of rejecting and a non-significant result means nothing at all."""
    d = int(d)
    return 1.0 if d <= 1 else float(min(1.0, 2.0 ** (1 - d)))


def sign_test_exact(pos, neg):
    """Exact two-sided sign test over CLUSTERS: of the clusters whose two arms differ, `pos` favour A and `neg`
    favour B. This is McNemar's logic moved up to the resampling unit, so it does not assume that vertebrae of one
    case disagree independently. With k = pos + neg non-zero clusters its floor is 2^(1-k), same as McNemar's."""
    return mcnemar_exact(pos, neg)


def paired_compare(rows, cluster, a, b, n_boot=10000, seed=0, alpha=0.05):
    """Two arms scored on the SAME items, with the items grouped in cases.

    `rows` each carry the cluster id and two 0/1 outcomes (fields `a` and `b`). Returns:
      - each arm's proportion on the matched items (the same denominator for both -- this is what makes it paired),
      - the difference with a case-cluster paired bootstrap CI: resample CASES, recompute both arms inside the
        drawn cases, take the difference each time. The pairing is preserved because a drawn case contributes its
        items to both arms.
      - McNemar's exact p over the discordant items, with the caveat above.
      - Cohen's h and the difference in percentage points, because "significant" is not "a surgeon would notice".

    FAILURE MODE AVOIDED: comparing two marginal percentages, or declaring "no difference" because two intervals
    overlap. Overlapping marginal intervals are routinely compatible with a difference whose own interval excludes
    zero, and the reverse also happens."""
    names = []
    seen = collections.OrderedDict()
    ka = collections.defaultdict(int)
    kb = collections.defaultdict(int)
    nn = collections.defaultdict(int)
    disc_b = disc_c = 0
    for r in rows:
        c = str(r[cluster])
        va, vb = as_bool(r[a]), as_bool(r[b])
        ka[c] += va
        kb[c] += vb
        nn[c] += 1
        if c not in seen:
            seen[c] = 1
            names.append(c)
        disc_b += int(va == 1 and vb == 0)
        disc_c += int(va == 0 and vb == 1)
    C = len(names)
    N = sum(nn.values())
    if C == 0 or N == 0:
        return dict(note="no matched records", n_items=0)
    KA = np.array([ka[c] for c in names], float)
    KB = np.array([kb[c] for c in names], float)
    NN = np.array([nn[c] for c in names], float)
    pa, pb = float(KA.sum() / N), float(KB.sum() / N)
    out = dict(p_a=pa, p_b=pb, diff=pa - pb, diff_pp=100 * (pa - pb),
               n_items=int(N), n_clusters=C, paired=True,
               discordant_a_only=int(disc_b), discordant_b_only=int(disc_c),
               mcnemar_exact_p=mcnemar_exact(disc_b, disc_c),
               mcnemar_smallest_possible_p=mcnemar_floor(disc_b + disc_c),
               cohens_h=cohens_h(pa, pb), n_boot=int(n_boot), seed=int(seed))
    if out["mcnemar_smallest_possible_p"] > alpha:
        out["mcnemar_note"] = (f"only {disc_b + disc_c} discordant items: McNemar's smallest attainable two-sided p "
                               f"is {out['mcnemar_smallest_possible_p']:.3f}, above alpha={alpha}, so it could not "
                               f"have rejected whatever the data did -- do not read its p as evidence of no effect")
    if C >= 2:
        rng = np.random.default_rng(seed)
        ra, rb = _boot_ratios(rng, KA, NN, n_boot, num2=KB)   # ONE resample drives both arms: this is the pairing
        d = ra - rb
        lo, hi = np.percentile(d, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        out["ci"] = [float(lo), float(hi)]
        out["ci_pp"] = [float(100 * lo), float(100 * hi)]
        out["excludes_zero"] = bool(lo > 0 or hi < 0)
        out["boot_sd_pp"] = float(100 * d.std(ddof=1))
        # the unpaired interval on the same data, to show what the pairing bought
        ua, _ = _boot_ratios(rng, KA, NN, n_boot)
        ub, _ = _boot_ratios(rng, KB, NN, n_boot)
        du = ua - ub
        ulo, uhi = np.percentile(du, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        out["unpaired_ci_pp"] = [float(100 * ulo), float(100 * uhi)]
        out["pairing_narrowed_by"] = (float((uhi - ulo) / (hi - lo)) if hi > lo else None)
        if C < 20:
            out["warning"] = f"only {C} clusters: percentile bootstrap intervals are unreliable below about 20"
    else:
        out["ci"] = [None, None]
        out["warning"] = "fewer than two clusters"

    # ---- the sign test at the CLUSTER level, and the fragility of "excludes zero" when few clusters differ.
    # A percentile interval can only put mass at zero by drawing a resample that contains none of the clusters
    # whose arms differ; that happens with probability ((C-k)/C)^C. With k small this is a step function of k,
    # so "excludes zero" is decided by how few cases the disagreements happen to land in rather than by the size
    # of the effect. Measured on this project's own data: the two held-out-device detector arms disagree on four
    # frames that fall in four distinct cases, giving ((28-4)/28)^28 = 0.0134 < 0.025 and an interval that
    # excludes zero -- move those same four frames into three cases and the same 51-vs-55 marginals no longer do.
    pos = int(np.sum(KA - KB > 0))
    neg = int(np.sum(KA - KB < 0))
    kdiff = pos + neg
    out["n_clusters_favouring_a"] = pos
    out["n_clusters_favouring_b"] = neg
    out["n_clusters_differing"] = kdiff
    out["cluster_sign_test_p"] = sign_test_exact(pos, neg)
    out["cluster_sign_smallest_possible_p"] = mcnemar_floor(kdiff)
    out["bootstrap_zero_mass"] = (float(((C - kdiff) / C) ** C) if C >= 1 else None)
    fragile = bool(out.get("excludes_zero") and out["cluster_sign_test_p"] > alpha)
    out["excludes_zero_fragile"] = fragile
    if fragile:
        out["fragility_note"] = (
            f"the interval excludes zero but only {kdiff} of {C} cases differ at all, and the exact sign test "
            f"over those cases gives p={out['cluster_sign_test_p']:.4f} (its floor at {kdiff} differing cases is "
            f"{out['cluster_sign_smallest_possible_p']:.4f}). A resample containing none of them has probability "
            f"{out['bootstrap_zero_mass']:.4f}, so the verdict turns on that number falling below alpha/2="
            f"{alpha/2:.4f} rather than on the size of the effect. Do not report this as an established "
            f"difference; report the counts and say the design cannot settle it.")
    if kdiff and mcnemar_floor(kdiff) > alpha:
        out["cluster_sign_note"] = (f"only {kdiff} cases differ: no exact test on this design can reach "
                                    f"alpha={alpha} (floor {mcnemar_floor(kdiff):.4f})")
    out["prefer"] = (
        "the paired cluster bootstrap CI of the difference, PROVIDED enough cases differ: McNemar's p assumes "
        "independent discordant items, which clustered items violate, but the percentile interval is itself "
        "unreliable when few clusters differ (see excludes_zero_fragile / cluster_sign_test_p). When both the "
        "McNemar floor and the cluster sign test sit above alpha, neither test can settle the comparison and the "
        "honest report is the counts.")
    return out


# --------------------------------------------------------------------------------------------- permutation tests
def permutation_diff_means(x, y, n_perm=10000, seed=0, alternative="two-sided", max_exact=50000):
    """Difference in means with no distributional assumption: relabel which group each value belongs to.

    ASSUMES only exchangeability under the null (the values could have come from either group). Use for the
    physics-term comparisons, where six folds per device is far too few for a t test's normality to be checked and
    an R2 is bounded above by 1 so its errors are skewed.

    Enumerates every split when there are few (the p value is then exact); otherwise samples n_perm of them and
    reports (r+1)/(B+1), which can never be 0 -- an honest floor rather than "p < 0.0001"."""
    x = np.asarray(list(x), float)
    y = np.asarray(list(y), float)
    nx, ny = len(x), len(y)
    if nx == 0 or ny == 0:
        return dict(note="empty group")
    obs = float(x.mean() - y.mean())
    pool = np.concatenate([x, y])
    n = nx + ny
    exact = math.comb(n, nx) <= max_exact
    if exact:
        from itertools import combinations
        diffs = []
        total = pool.sum()
        for comb in combinations(range(n), nx):
            sx = pool[list(comb)].sum()
            diffs.append(sx / nx - (total - sx) / ny)
        diffs = np.asarray(diffs)
        if alternative == "two-sided":
            p = float((np.abs(diffs) >= abs(obs) - 1e-12).mean())
        elif alternative == "greater":
            p = float((diffs >= obs - 1e-12).mean())
        else:
            p = float((diffs <= obs + 1e-12).mean())
        n_used = len(diffs)
    else:
        rng = np.random.default_rng(seed)
        diffs = np.empty(int(n_perm))
        for i in range(int(n_perm)):
            perm = rng.permutation(n)
            sx = pool[perm[:nx]].sum()
            diffs[i] = sx / nx - (pool.sum() - sx) / ny
        if alternative == "two-sided":
            r = int((np.abs(diffs) >= abs(obs) - 1e-12).sum())
        elif alternative == "greater":
            r = int((diffs >= obs - 1e-12).sum())
        else:
            r = int((diffs <= obs + 1e-12).sum())
        p = (r + 1) / (int(n_perm) + 1)
        n_used = int(n_perm)
    floor = (2.0 / n_used if (exact and alternative == "two-sided") else
             (1.0 / n_used if exact else 1.0 / (n_used + 1)))
    out = dict(mean_x=float(x.mean()), mean_y=float(y.mean()), diff=obs, p=float(p), exact=bool(exact),
               n_x=nx, n_y=ny, permutations=n_used, alternative=alternative, seed=int(seed),
               smallest_possible_p=float(floor),
               assumption="exchangeability under the null; no normality, no equal variance")
    if abs(p - floor) < 1e-12:
        out["note"] = ("the observed split is the most extreme of all of them, so this p is the smallest the "
                       "design can produce; with these group sizes no data could give a smaller one")
    return out


def permutation_paired_diff(d, n_perm=10000, seed=0, alternative="two-sided", max_exact=20):
    """Paired version: the null is that each pair's sign is arbitrary, so flip signs rather than relabel groups.
    Exact by enumeration when 2^n is small -- with six folds it is 64 splits, so the p value is exact and its
    smallest possible value is 2/64 = 0.031, which is itself worth stating in a paper."""
    d = np.asarray(list(d), float)
    n = len(d)
    if n == 0:
        return dict(note="no pairs")
    obs = float(d.mean())
    if n <= max_exact:
        means = []
        for mask in range(1 << n):
            s = np.array([1.0 if (mask >> i) & 1 else -1.0 for i in range(n)])
            means.append(float((d * s).mean()))
        means = np.asarray(means)
        exact = True
        n_used = len(means)
    else:
        rng = np.random.default_rng(seed)
        signs = rng.choice([-1.0, 1.0], size=(int(n_perm), n))
        means = (signs * d).mean(1)
        exact = False
        n_used = int(n_perm)
    if alternative == "two-sided":
        hits = int((np.abs(means) >= abs(obs) - 1e-12).sum())
    elif alternative == "greater":
        hits = int((means >= obs - 1e-12).sum())
    else:
        hits = int((means <= obs + 1e-12).sum())
    p = hits / n_used if exact else (hits + 1) / (n_used + 1)
    return dict(mean_diff=obs, p=float(p), exact=bool(exact), n_pairs=n, permutations=n_used,
                smallest_possible_p=(2.0 / n_used if exact and alternative == "two-sided" else None),
                alternative=alternative, seed=int(seed))


# ------------------------------------------------------------------------------------------------- multiplicity
def holm(pvals):
    """Holm-Bonferroni. Controls the probability of making ANY false claim (family-wise error). Use when a single
    false positive would be damaging -- e.g. claiming any one of nine physics terms matters when none does."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running = {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, (m - i) * p)
        out[k] = float(min(1.0, running))
    return {k: out[k] for k in pvals}


def benjamini_hochberg(pvals):
    """Benjamini-Hochberg. Controls the expected SHARE of false claims among those called (false discovery rate).
    Use for a screen -- which of six devices moved, which of nine terms to look at next -- where a few false leads
    are acceptable. Assumes the tests are independent or positively dependent."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running = {}, 1.0
    for i in range(m - 1, -1, -1):
        k, p = items[i]
        running = min(running, m * p / (i + 1))
        out[k] = float(min(1.0, running))
    return {k: out[k] for k in pvals}


def adjust(pvals, method="holm"):
    """Adjusted p values from {name: p}.

    WHEN NOT TO ADJUST. A primary comparison that was pre-stated in the plan before the data were read is one test,
    not one of many, and adjusting it for the exploratory comparisons that happen to sit in the same paper makes it
    harder to detect the effect the study was designed around. Adjust WITHIN a family of exchangeable tests asked
    at once (the nine physics terms; the six devices; the five arms of a sweep), report the family and the method
    beside the numbers, and never adjust a set assembled after seeing which p values were small. If you adjusted,
    say over what family; if you did not, say why."""
    if method == "holm":
        return holm(pvals)
    if method in ("bh", "fdr", "benjamini-hochberg"):
        return benjamini_hochberg(pvals)
    if method in ("none", "raw"):
        return dict(pvals)
    raise ValueError(f"unknown method {method}")


# -------------------------------------------------------------------------------------------------- effect sizes
def cohens_h(p1, p2):
    """Cohen's h = 2 asin(sqrt p1) - 2 asin(sqrt p2). Scale-free and, unlike a raw difference, it does not shrink
    just because both proportions are near 1 -- 0.98 vs 0.96 is a bigger change than 0.52 vs 0.50 even though both
    are two points. Conventional reading: 0.2 small, 0.5 medium, 0.8 large."""
    p1 = min(max(float(p1), 0.0), 1.0)
    p2 = min(max(float(p2), 0.0), 1.0)
    return float(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))


def cohens_h_ci(p1, n1, p2, n2, alpha=0.05, deff1=1.0, deff2=1.0):
    """Interval for h from the arcsine variance (1/n per arm), with the design effect dividing each n so that
    clustered items do not pretend to be independent ones. For paired data prefer bootstrapping h directly."""
    h = cohens_h(p1, p2)
    se = math.sqrt(deff1 / max(n1, 1e-9) + deff2 / max(n2, 1e-9))
    z = ND.inv_cdf(1 - alpha / 2)
    return dict(h=h, se=se, ci=[h - z * se, h + z * se],
                magnitude=("negligible" if abs(h) < 0.2 else "small" if abs(h) < 0.5
                           else "medium" if abs(h) < 0.8 else "large"))


def newcombe_diff(k1, n1, k2, n2, alpha=0.05):
    """Newcombe's hybrid-score interval for a difference of two INDEPENDENT proportions. Better behaved than the
    Wald interval near 0 and 1, which is where every number in this paper sits. Not for paired or clustered data --
    use paired_compare there."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, alpha)
    l2, u2 = wilson(k2, n2, alpha)
    lo = (p1 - p2) - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = (p1 - p2) + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (max(-1.0, lo), min(1.0, hi))


def design_effect_from_icc(m, icc):
    """Kish: deff = 1 + (m - 1) * icc, for m items per cluster. The bridge between a measured clustering and a
    sample size for the next study."""
    return 1.0 + (max(m, 1.0) - 1.0) * icc


# ----------------------------------------------------------------------------------- power / minimum detectable
def power_two_proportions(n1, n2, p1, p2, alpha=0.05, deff=1.0):
    """Power of a two-sided test of two proportions, in the arcsine (Cohen's h) form, which stays sensible when
    both proportions are near 1. n1/n2 are ITEM counts; deff divides them so clustered items count for less.
    This is a design calculation from assumed inputs, not a measurement."""
    h = abs(cohens_h(p1, p2))
    se = math.sqrt(deff * (1.0 / max(n1, 1e-9) + 1.0 / max(n2, 1e-9)))
    if se <= 0:
        return 1.0
    z = ND.inv_cdf(1 - alpha / 2)
    lam = h / se
    return float(ND.cdf(lam - z) + ND.cdf(-lam - z))


def n_two_proportions(p1, p2, alpha=0.05, power=0.8, deff=1.0, ratio=1.0):
    """Items per arm needed to detect p1 vs p2 at the given power; ratio = n2/n1. Multiply by deff for clustering;
    divide by items-per-case to get CASES."""
    h = abs(cohens_h(p1, p2))
    if h == 0:
        return dict(n1=None, n2=None, note="no difference to detect")
    z = ND.inv_cdf(1 - alpha / 2) + ND.inv_cdf(power)
    n1 = deff * (1 + 1.0 / ratio) * (z / h) ** 2
    return dict(n1=math.ceil(n1), n2=math.ceil(n1 * ratio), cohens_h=h, alpha=alpha, power=power, deff=deff)


def mdd_two_proportions(n1, n2, p1, alpha=0.05, power=0.8, deff=1.0):
    """MINIMUM DETECTABLE DIFFERENCE: with the sample already in hand, how far from p1 must the other arm be
    before this design would find it at the stated power? The number that says whether an experiment can pass or
    fail its own pre-stated criterion. Returns both directions, because near 1 they are not symmetric."""
    z = ND.inv_cdf(1 - alpha / 2) + ND.inv_cdf(power)
    se = math.sqrt(deff * (1.0 / max(n1, 1e-9) + 1.0 / max(n2, 1e-9)))
    h = z * se
    phi1 = 2 * math.asin(math.sqrt(min(max(p1, 0.0), 1.0)))
    down = math.sin(max(phi1 - h, 0.0) / 2) ** 2
    up = math.sin(min(phi1 + h, math.pi) / 2) ** 2
    return dict(p1=p1, n1=int(n1), n2=int(n2), required_h=h, deff=deff, alpha=alpha, power=power,
                detectable_worse=down, detectable_better=(up if phi1 + h <= math.pi else None),
                mdd_pp_worse=100 * (p1 - down),
                mdd_pp_better=(100 * (up - p1) if phi1 + h <= math.pi else None))


def criterion_pass_probability(n, threshold, p_true):
    """A pre-stated criterion of the form "observed rate >= threshold" on n units, read from BOTH sides, because
    a criterion fails in two different ways and only one of them is obvious.

      false pass  -- a system worse than the criterion passes by luck: P(pass | p_true).
      false fail  -- a system that genuinely meets the criterion fails it: 1 - P(pass | p = threshold). At small n
                     this is the larger problem, and it is invisible unless you compute it. On n = 28 a ">= 97 %"
                     rule rounds up to "28 of 28 correct", so a system that truly is 97 % fails its own
                     pre-stated criterion more than half the time.

    `effective_threshold` is k/n, the rate the rule really demands once counts are integers: between 27/28 and
    28/28 there is nothing, so on 28 units every threshold from 96.5 % to 100 % is the same rule.

    A design calculation from assumed rates, not a measurement."""
    n = int(n)
    k_needed = int(math.ceil(threshold * n - 1e-9))
    p_pass_true = binom_sf(k_needed, n, p_true)
    p_pass_at_thr = binom_sf(k_needed, n, threshold)
    return dict(n=n, threshold=threshold, p_true=p_true, successes_needed=k_needed,
                effective_threshold=(k_needed / n if n else None),
                pass_probability=p_pass_true,
                pass_probability_at_threshold=p_pass_at_thr,
                false_fail_probability=1.0 - p_pass_at_thr,
                discrimination=p_pass_at_thr - p_pass_true,
                verdict=("this n cannot pass or fail the criterion informatively: a system exactly at the "
                         f"criterion fails it {(1-p_pass_at_thr)*100:.0f} % of the time"
                         if p_pass_at_thr < 0.7 else
                         f"a system at {p_true:.0%} passes {p_pass_true*100:.1f} % of the time"),
                note="design calculation from assumed true rates; not a measurement")


def power_one_sample_exact(n, p0, p_true, alpha=0.05):
    """Exact binomial power for H0: p <= p0 against p = p_true, one-sided. Reports the critical count so the
    criterion can be written as "k of n or better", which is what a pre-registered pass rule should say."""
    k = None
    for cand in range(0, int(n) + 1):
        if binom_sf(cand, int(n), p0) <= alpha:
            k = cand
            break
    if k is None:
        return dict(n=int(n), p0=p0, alpha=alpha, critical_k=None, power=0.0,
                    note="no critical value exists at this n: the test cannot reject at this alpha")
    return dict(n=int(n), p0=p0, p_true=p_true, alpha=alpha, critical_k=int(k),
                size=binom_sf(k, int(n), p0), power=binom_sf(k, int(n), p_true),
                note="design calculation; exact binomial, one-sided")


def n_for_lower_bound(target, alpha=0.05, errors=0, nmax=200000):
    """Smallest n whose one-sided exact lower bound reaches `target` when `errors` of them fail. With errors = 0,
    target 0.99 and alpha 0.05 this is ceil(ln alpha / ln target) = 299 -- the cheapest honest statement of what a
    "99 %" claim costs. (298 gives 0.98999...; the test asserts the closed form.)"""
    n = max(int(errors) + 1, 1)
    while n < nmax:
        if clopper_pearson_lower(n - int(errors), n, alpha) >= target:
            return dict(n=n, target=target, alpha=alpha, errors=int(errors),
                        lower_bound=clopper_pearson_lower(n - int(errors), n, alpha))
        n += 1
    return dict(n=None, target=target, alpha=alpha, errors=int(errors), note=f"no n below {nmax}")


def plan_arm(name, p_expected, threshold, alpha=0.05, power=0.8, items_per_case=1.0, icc=0.0):
    """One planned prospective arm: how many CASES to show p_expected beats the criterion `threshold`, allowing
    for items clustered inside cases. Everything here is assumption in, arithmetic out -- the output states both."""
    deff = design_effect_from_icc(items_per_case, icc)
    if p_expected <= threshold:
        return dict(arm=name, p_expected=p_expected, threshold=threshold,
                    note="expected performance is not above the criterion; no n can show it")
    h = abs(cohens_h(p_expected, threshold))
    z = ND.inv_cdf(1 - alpha) + ND.inv_cdf(power)      # one-sided: beating a fixed criterion
    n_items = deff * (z / h) ** 2
    cases = math.ceil(n_items / max(items_per_case, 1e-9))
    exact = n_for_lower_bound(threshold, alpha, errors=0)
    return dict(arm=name, p_expected=p_expected, threshold=threshold, alpha=alpha, power=power,
                items_per_case=items_per_case, icc=icc, design_effect=deff,
                items_needed=math.ceil(n_items), cases_needed=cases, cohens_h=h,
                perfect_run_items_for_bound=exact.get("n"),
                note="design calculation from assumed inputs (one-sided, arcsine approximation); not a measurement")


# ------------------------------------------------------------------------------------------------------- loaders
def _descend(obj, segs, ctx):
    if not segs:
        if isinstance(obj, dict):
            rec = dict(ctx)
            rec.update(obj)
            return [rec]
        rec = dict(ctx)
        rec["value"] = obj
        return [rec]
    seg, rest = segs[0], segs[1:]
    islist = seg.endswith("[]")
    key = seg[:-2] if islist else seg
    merged = ctx
    if key:
        if not isinstance(obj, dict) or key not in obj:
            return []
        merged = dict(ctx)
        merged.update({k: v for k, v in obj.items() if not isinstance(v, (dict, list))})
        obj = obj[key]
    out = []
    if islist:
        for el in (obj or []):
            out.extend(_descend(el, rest, merged))
    else:
        out.extend(_descend(obj, rest, merged))
    return out


def load_records(path, record_path=None):
    """Flat list of records from .json / .jsonl / .csv.

    `record_path` is dotted with [] marking a list to walk, e.g. 'frames[].items[]'. Scalar fields of every
    ancestor dict are carried into each record unless the record already has that key -- so a per-vertebra item
    inherits its frame's `case`, which is exactly the cluster key. The record's own field always wins, so an item
    named `truth` is never overwritten by a frame-level `truth`."""
    p = str(path)
    if p.endswith(".jsonl"):
        return [json.loads(line) for line in open(p, encoding="utf-8") if line.strip()]
    if p.endswith(".csv"):
        with open(p, newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    obj = json.load(open(p, encoding="utf-8"))
    if record_path:
        return _descend(obj, record_path.split("."), {})
    if isinstance(obj, list):
        return obj
    lists = [k for k, v in obj.items() if isinstance(v, list) and v and isinstance(v[0], dict)]
    if len(lists) == 1:
        return _descend(obj, [lists[0] + "[]"], {})
    raise SystemExit(f"{p}: give --record-path (candidate lists: {lists})")


def apply_where(rows, wheres):
    """--where key=value filters, compared as strings. Every filter is a denominator decision, so the CLI prints
    how many records each one removed."""
    kept, log = rows, []
    for w in wheres or []:
        k, _, v = w.partition("=")
        before = len(kept)
        kept = [r for r in kept if str(r.get(k)).lower() == v.lower()]
        log.append(dict(filter=w, before=before, after=len(kept), removed=before - len(kept)))
    return kept, log


def load_values(spec):
    """Numbers from 'a,b,c' or from 'file.json:dotted.path' (a list, or a dict whose values are the numbers --
    docs/devices/<dev>.json:fit.R2_held_out_by_fold is exactly that)."""
    # rpartition, not partition: on Windows an absolute path starts 'C:\...' and splitting at the FIRST colon
    # hands back a path of "C" that does not exist, after which the spec is parsed as a comma list of floats and
    # the user gets "could not convert string to float: '<laptop drive>/Users\\...'" instead of their numbers.
    head, sep, dotted = spec.rpartition(":")
    looks_like_file = bool(sep) and (os.sep in head or "/" in head
                                     or head.lower().endswith((".json", ".jsonl", ".csv")))
    if sep and looks_like_file and not os.path.exists(head):
        raise SystemExit(f"load_values: {head!r} looks like a file but does not exist "
                         f"(spec was {spec!r}; the form is 'file.json:dotted.path')")
    if sep and os.path.exists(head):
        path = head
        obj = json.load(open(path, encoding="utf-8"))
        for seg in dotted.split("."):
            obj = obj[seg]
        if isinstance(obj, dict):
            return [float(v) for _, v in sorted(obj.items())], path, sorted(obj)
        return [float(v) for v in obj], path, None
    return [float(v) for v in spec.split(",") if v.strip()], None, None


def require_rows(rows, path, record_path, wheres, log):
    """An empty selection is a bug, not a result. A mistyped --record-path or --where silently yields zero
    records, boot_proportion then returns p=None, the job exits 0 and an empty JSON lands in the results
    directory looking like an answer. Stop instead, and say which step emptied it."""
    if rows:
        return rows
    culprit = next((l for l in (log or []) if l["after"] == 0 and l["before"] > 0), None)
    if culprit:
        raise SystemExit(f"{path}: filter {culprit['filter']!r} removed all {culprit['before']} records "
                         f"(check the field name and its spelling in the file)")
    raise SystemExit(f"{path}: --record-path {record_path!r} matched no records "
                     f"(a path that does not exist returns an empty list rather than raising)")


def _dump(a, payload):
    print(json.dumps(payload, indent=2, default=float))
    if getattr(a, "out", None):
        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
        json.dump(payload, open(a.out, "w", encoding="utf-8"), indent=2, default=float)
        print(f"\nwrote {a.out}", file=sys.stderr)


# ----------------------------------------------------------------------------------------------------------- CLI
def cmd_prop(a):
    rows = load_records(a.rows, a.record_path)
    rows, log = apply_where(rows, a.where)
    require_rows(rows, a.rows, a.record_path, a.where, log)
    res = boot_proportion(rows, a.cluster, a.value, a.n_boot, a.seed, a.alpha)
    res["filters"] = log
    res["meta"] = meta(a.rows, seed=a.seed, cluster=a.cluster, value=a.value, record_path=a.record_path)
    _dump(a, res)


def cmd_diff(a):
    ra = load_records(a.rows_a, a.record_path)
    rb = load_records(a.rows_b, a.record_path)
    ra, la = apply_where(ra, a.where)
    rb, lb = apply_where(rb, a.where)
    require_rows(ra, a.rows_a, a.record_path, a.where, la)
    require_rows(rb, a.rows_b, a.record_path, a.where, lb)
    res = boot_diff_unpaired(ra, rb, a.cluster, a.value, a.n_boot, a.seed, a.alpha)
    res["filters"] = dict(a=la, b=lb)
    res["meta"] = meta([a.rows_a, a.rows_b], seed=a.seed, cluster=a.cluster, value=a.value)
    _dump(a, res)


def cmd_paired(a):
    ra = load_records(a.rows_a, a.record_path)
    rb = load_records(a.rows_b, a.record_path)
    ra, la = apply_where(ra, a.where)
    rb, lb = apply_where(rb, a.where)
    require_rows(ra, a.rows_a, a.record_path, a.where, la)
    require_rows(rb, a.rows_b, a.record_path, a.where, lb)
    keys = a.key.split(",")

    def kf(r):
        return tuple(str(r.get(k)) for k in keys)

    da = {kf(r): r for r in ra}
    db = {kf(r): r for r in rb}
    if len(da) != len(ra) or len(db) != len(rb):
        raise SystemExit(f"--key {a.key} is not unique (a: {len(ra)} rows -> {len(da)} keys; "
                         f"b: {len(rb)} rows -> {len(db)} keys); add fields to --key")
    shared = [k for k in da if k in db]
    rows = [{a.cluster: da[k][a.cluster], "__a": da[k][a.value], "__b": db[k][a.value]} for k in shared]
    if not shared:
        raise SystemExit(f"--key {a.key} matched nothing between the two files "
                         f"(a: {len(da)} keys, b: {len(db)} keys); check the field name")
    res = paired_compare(rows, a.cluster, "__a", "__b", a.n_boot, a.seed, a.alpha)
    res["matched"] = len(shared)
    res["dropped_a_only"] = len(da) - len(shared)
    res["dropped_b_only"] = len(db) - len(shared)
    # A paired test silently conditions on the intersection. If the rows only one arm has are systematically
    # easier or harder than the matched ones, the difference it reports is not about the whole population -- and
    # a count alone does not show that. Measured on this project's own data: det-vs-oracle naming drops 21
    # vertebrae the detector never found, and the oracle names those correctly 76.2 % of the time against 91.4 %
    # on the matched 291, so the matched comparison is conditioned on an outcome-dependent subset.
    sh = set(shared)
    for side, d, label in (("a", da, a.rows_a), ("b", db, a.rows_b)):
        only = [k for k in d if k not in sh]
        if only:
            try:
                rate = sum(as_bool(d[k][a.value]) for k in only) / len(only)
            except (KeyError, ValueError):
                rate = None
            matched_rate = res["p_a"] if side == "a" else res["p_b"]
            res[f"dropped_{side}_only_rate"] = rate
            if rate is not None and matched_rate is not None and abs(rate - matched_rate) > 0.03:
                res[f"dropped_{side}_only_warning"] = (
                    f"the {len(only)} rows only {label} has score {100*rate:.1f} % against {100*matched_rate:.1f} % "
                    f"on the {len(shared)} matched ones: the pairing conditions on an outcome-dependent subset, so "
                    f"this difference describes the matched rows only, not the whole set")
    res["arm_a"], res["arm_b"] = a.rows_a, a.rows_b
    res["filters"] = dict(a=la, b=lb)
    res["meta"] = meta([a.rows_a, a.rows_b], seed=a.seed, cluster=a.cluster, value=a.value, key=a.key)
    _dump(a, res)


def cmd_perm(a):
    x, px, nx = load_values(a.x)
    y, py, ny = load_values(a.y)
    if a.paired:
        if len(x) != len(y):
            raise SystemExit(f"--paired needs equal lengths ({len(x)} vs {len(y)})")
        res = permutation_paired_diff([xi - yi for xi, yi in zip(x, y)], a.n_perm, a.seed, a.alternative)
        res["mean_x"], res["mean_y"] = float(np.mean(x)), float(np.mean(y))
    else:
        res = permutation_diff_means(x, y, a.n_perm, a.seed, a.alternative)
    res["x"], res["y"] = x, y
    res["x_labels"], res["y_labels"] = nx, ny
    res["meta"] = meta([px, py], seed=a.seed, x_spec=a.x, y_spec=a.y, paired=bool(a.paired))
    _dump(a, res)


def cmd_adjust(a):
    pv = {}
    if a.json:
        pv.update({k: float(v) for k, v in json.load(open(a.json, encoding="utf-8")).items()})
    for item in a.p or []:
        k, _, v = item.partition("=")
        pv[k] = float(v)
    if not pv:
        raise SystemExit("give --p name=value (repeatable) or --json file")
    res = dict(raw=pv, method=a.method, adjusted=adjust(pv, a.method), family=a.family, n_tests=len(pv),
               guidance=" ".join(adjust.__doc__.split("WHEN NOT TO ADJUST.")[-1].split()))
    res["meta"] = meta(a.json, method=a.method, family=a.family)
    _dump(a, res)


def cmd_power_criterion(a):
    res = dict(criterion=criterion_pass_probability(a.n, a.threshold, a.p_true),
               exact_power=power_one_sample_exact(a.n, a.p0 if a.p0 is not None else a.threshold, a.p_true, a.alpha))
    res["meta"] = meta([], n=a.n, threshold=a.threshold, p_true=a.p_true)
    _dump(a, res)


def cmd_power_diff(a):
    res = dict(mdd=mdd_two_proportions(a.n1, a.n2 if a.n2 else a.n1, a.p1, a.alpha, a.power, a.deff))
    if a.p2 is not None:
        res["power_at_p2"] = power_two_proportions(a.n1, a.n2 if a.n2 else a.n1, a.p1, a.p2, a.alpha, a.deff)
        res["n_needed"] = n_two_proportions(a.p1, a.p2, a.alpha, a.power, a.deff)
    res["meta"] = meta([], n1=a.n1, n2=a.n2, p1=a.p1, p2=a.p2, deff=a.deff)
    _dump(a, res)


def cmd_certify(a):
    res = dict(zero_error=n_for_lower_bound(a.target, a.alpha, 0))
    res["with_errors"] = [n_for_lower_bound(a.target, a.alpha, e) for e in range(1, a.errors + 1)] if a.errors else []
    res["meta"] = meta([], target=a.target, alpha=a.alpha)
    _dump(a, res)


def cmd_plan(a):
    icc, m, src, caution = a.icc, a.items_per_case, None, None
    if a.icc_from:
        rows = load_records(a.icc_from, a.record_path)
        rows, log = apply_where(rows, a.where)
        require_rows(rows, a.icc_from, a.record_path, a.where, log)
        # The ICC is a function of the bootstrap SD, so it inherits the Monte-Carlo error of the resampling.
        # The old cap of 2000 resamples made it move by 0.15 across seeds on this project's own lateral fold-0
        # data (0.85 to 1.00 over twelve seeds), which then moved every case count below it. Spend the samples.
        b = boot_proportion(rows, a.cluster, a.value, max(a.n_boot, 20000), a.seed, a.alpha)
        if b.get("icc_implied") is not None:
            icc, m, src = b["icc_implied"], b["items_per_cluster"], a.icc_from
            caution = (f"ICC {icc:.3f} and {m:.2f} items per case were measured on {b['n_clusters']} clusters of "
                       f"{a.icc_from}; an ICC from few clusters is itself uncertain, so treat the case counts "
                       f"below as an order of magnitude and report the ICC you assumed")
            if b.get("icc_note"):
                caution += f". {b['icc_note']}"
            if b.get("ceiling_warning"):
                caution += (f". The source proportion is near the ceiling, where the bootstrap SD this ICC is "
                            f"derived from is itself unreliable: {b['ceiling_warning']}")
    arms = []
    for spec in a.arm:
        parts = spec.split(":")
        if len(parts) != 3:
            raise SystemExit("--arm name:expected:threshold")
        arms.append(plan_arm(parts[0], float(parts[1]), float(parts[2]), a.alpha, a.power, m, icc))
    res = dict(arms=arms, icc=icc, items_per_case=m, icc_measured_from=src, caution=caution,
               meta=meta([a.icc_from], seed=a.seed, alpha=a.alpha, power=a.power))
    _dump(a, res)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, rows=True):
        if rows:
            p.add_argument("--record-path", help="dotted path with [] per list, e.g. 'frames[].items[]'")
            p.add_argument("--cluster", default="case", help="the resampling unit (default: case)")
            p.add_argument("--value", default="exact", help="the 0/1 outcome field")
            p.add_argument("--where", action="append", help="key=value filter, repeatable")
        p.add_argument("--n-boot", type=int, default=10000,
                       help="bootstrap resamples; the endpoints are Monte-Carlo estimates too "
                            "(see ci_mc_se_pp in the output)")
        p.add_argument("--seed", type=int, default=0)
        p.add_argument("--alpha", type=float, default=0.05)
        p.add_argument("--out", help="write the result JSON here")

    p = sub.add_parser("prop", help="one proportion with a case-cluster bootstrap CI (and the naive one beside it)")
    p.add_argument("--rows", required=True)
    common(p)
    p.set_defaults(fn=cmd_prop)

    p = sub.add_parser("diff", help="difference of two proportions measured on DIFFERENT cases")
    p.add_argument("--rows-a", required=True)
    p.add_argument("--rows-b", required=True)
    common(p)
    p.set_defaults(fn=cmd_diff)

    p = sub.add_parser("paired", help="two arms on the SAME items: CI of the difference + McNemar")
    p.add_argument("--rows-a", required=True)
    p.add_argument("--rows-b", required=True)
    p.add_argument("--key", default="stem", help="field(s) joining the two files, comma separated")
    common(p)
    p.set_defaults(fn=cmd_paired)

    p = sub.add_parser("perm", help="permutation test for a difference in means (the physics-term comparisons)")
    p.add_argument("--x", required=True, help="'a,b,c' or 'file.json:dotted.path'")
    p.add_argument("--y", required=True)
    p.add_argument("--paired", action="store_true", help="sign-flip test over matched folds")
    p.add_argument("--alternative", default="two-sided", choices=["two-sided", "greater", "less"])
    p.add_argument("--n-perm", type=int, default=10000)
    common(p, rows=False)
    p.set_defaults(fn=cmd_perm)

    p = sub.add_parser("adjust", help="Holm / Benjamini-Hochberg over a family of p values")
    p.add_argument("--p", action="append", help="name=value, repeatable")
    p.add_argument("--json", help="{name: p} file")
    p.add_argument("--method", default="holm", choices=["holm", "bh", "none"])
    p.add_argument("--family", help="what family these tests are, in words -- written into the output")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_adjust)

    p = sub.add_parser("power-criterion", help="can this n pass/fail a pre-stated threshold at all?")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--threshold", type=float, required=True)
    p.add_argument("--p-true", type=float, required=True)
    p.add_argument("--p0", type=float, help="null rate for the exact test (default: the threshold)")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_power_criterion)

    p = sub.add_parser("power-diff", help="minimum detectable difference / power / n for two proportions")
    p.add_argument("--n1", type=int, required=True)
    p.add_argument("--n2", type=int)
    p.add_argument("--p1", type=float, required=True)
    p.add_argument("--p2", type=float)
    p.add_argument("--deff", type=float, default=1.0, help="design effect from clustering (see prop's output)")
    p.add_argument("--power", type=float, default=0.8)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_power_diff)

    p = sub.add_parser("certify", help="n needed for a one-sided exact lower bound (the 99 % claim's price)")
    p.add_argument("--target", type=float, default=0.99)
    p.add_argument("--errors", type=int, default=0, help="also report n for 1..E observed failures")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_certify)

    p = sub.add_parser("plan", help="cases needed for the planned prospective arms (phantom, cadaver, human)")
    p.add_argument("--arm", action="append", required=True, help="name:expected:threshold, repeatable")
    p.add_argument("--items-per-case", type=float, default=1.0)
    p.add_argument("--icc", type=float, default=0.0)
    p.add_argument("--icc-from", help="measure the ICC and items-per-case from a real records file instead")
    p.add_argument("--power", type=float, default=0.8)
    common(p)
    p.set_defaults(fn=cmd_plan)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
