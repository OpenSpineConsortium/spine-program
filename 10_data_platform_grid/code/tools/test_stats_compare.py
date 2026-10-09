#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_stats_compare.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does tools/stats_compare.py give the right answer where the right answer is known?

A statistics library is the worst place for a plausible wrong number: every interval it prints looks like an
interval and nothing downstream will notice if it is half as wide as it should be. So every routine here is checked
against something outside itself -- a closed form, an exact enumeration, statsmodels where it is installed, or a
simulation whose truth is set by the generator.

The centrepiece is a COVERAGE measurement on case-clustered synthetic data, where the true proportion is known by
construction: a 95 % interval must contain the truth in about 95 % of replicates. It is run twice --

  independent items   (ICC = 0): the naive binomial interval is correct, and the cluster bootstrap must not be
                      wildly wider (a cluster method that throws away resolution on clean data is its own defect)
  clustered items     (ICC > 0): the naive interval demonstrably UNDER-COVERS, which is the fact the whole
                      case-level machinery exists for, measured rather than asserted

and a paired null where the two arms are truly equal but their disagreements cluster inside cases, which is where
McNemar's exact test -- correct under its own assumption -- rejects far more often than 5 % and the paired cluster
bootstrap does not. That simulation is the evidence for the library's advice about which of the two to prefer.

    python tools/test_stats_compare.py           # full run, exits non-zero on any failure
    python tools/test_stats_compare.py --quick   # fewer replicates (coverage is noisier)
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stats_compare as S  # noqa: E402

FAILS = []
NOTES = []


def check(name, cond, detail=""):
    ok = bool(cond)
    print(f"{'ok  ' if ok else 'FAIL'} {name}{('   ' + detail) if detail else ''}")
    if not ok:
        FAILS.append(name)
    return ok


def near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


# ------------------------------------------------------------------------------------------ 1. closed-form checks
def test_intervals():
    print("\n[1] interval primitives against closed forms")
    n, alpha = 30, 0.05
    lo, hi = S.clopper_pearson(n, n, alpha)
    check("Clopper-Pearson lower at k=n equals (alpha/2)^(1/n)",
          near(lo, (alpha / 2) ** (1 / n), 1e-9), f"{lo:.6f} vs {(alpha/2)**(1/n):.6f}")
    check("Clopper-Pearson upper at k=n is 1", near(hi, 1.0, 1e-12))
    lo0, hi0 = S.clopper_pearson(0, n, alpha)
    check("Clopper-Pearson upper at k=0 equals 1-(alpha/2)^(1/n)",
          near(hi0, 1 - (alpha / 2) ** (1 / n), 1e-9), f"{hi0:.6f}")
    check("one-sided lower at k=n equals alpha^(1/n)",
          near(S.clopper_pearson_lower(n, n, alpha), alpha ** (1 / n), 1e-12))

    # binomial tail functions against an independent brute-force sum
    from math import comb
    p, n2, k = 0.37, 40, 18
    brute = sum(comb(n2, i) * p ** i * (1 - p) ** (n2 - i) for i in range(k, n2 + 1))
    check("binom_sf matches a direct sum", near(S.binom_sf(k, n2, p), brute, 1e-12),
          f"{S.binom_sf(k, n2, p):.10f} vs {brute:.10f}")
    check("binom_cdf + binom_sf(k+1) = 1", near(S.binom_cdf(k, n2, p) + S.binom_sf(k + 1, n2, p), 1.0, 1e-12))

    try:
        from statsmodels.stats.proportion import proportion_confint
        w = S.wilson(17, 40)
        sm = proportion_confint(17, 40, method="wilson")
        check("Wilson matches statsmodels", near(w[0], sm[0], 1e-9) and near(w[1], sm[1], 1e-9),
              f"{w[0]:.6f},{w[1]:.6f} vs {sm[0]:.6f},{sm[1]:.6f}")
        cp = S.clopper_pearson(17, 40)
        smb = proportion_confint(17, 40, method="beta")
        check("Clopper-Pearson matches statsmodels", near(cp[0], smb[0], 1e-9) and near(cp[1], smb[1], 1e-9))
    except ImportError:
        NOTES.append("statsmodels not installed: the cross-check against it was skipped")


def test_mcnemar_and_multiplicity():
    print("\n[2] McNemar and multiplicity against known values")
    check("McNemar(10,0) = 2*0.5^10", near(S.mcnemar_exact(10, 0), 2 * 0.5 ** 10, 1e-15),
          f"{S.mcnemar_exact(10, 0):.9f}")
    check("McNemar(0,0) = 1 (no discordant pairs, no information)", near(S.mcnemar_exact(0, 0), 1.0, 1e-15))
    check("McNemar(5,5) = 1", near(S.mcnemar_exact(5, 5), 1.0, 1e-15))
    check("McNemar is symmetric", near(S.mcnemar_exact(3, 11), S.mcnemar_exact(11, 3), 1e-15))
    check("McNemar's floor with 4 discordant pairs is 0.125, so it cannot reach 0.05",
          near(S.mcnemar_exact(4, 0), 0.125, 1e-15) and near(S.mcnemar_floor(4), 0.125, 1e-15),
          "this is the real two-arm detector case: 56 shared frames, 4 discordant, all one way")
    check("six discordant pairs is the first count that can reach 0.05",
          S.mcnemar_floor(5) > 0.05 >= S.mcnemar_floor(6),
          f"floor(5)={S.mcnemar_floor(5):.4f}, floor(6)={S.mcnemar_floor(6):.4f}")
    check("the floor is attained by the most lopsided split",
          all(near(S.mcnemar_exact(d, 0), S.mcnemar_floor(d), 1e-15) for d in range(2, 12)))
    try:
        from statsmodels.stats.contingency_tables import mcnemar as sm_mcnemar
        for b, c in [(10, 0), (3, 11), (7, 6), (25, 12)]:
            got = S.mcnemar_exact(b, c)
            want = float(sm_mcnemar([[0, b], [c, 0]], exact=True).pvalue)
            check(f"McNemar({b},{c}) matches statsmodels", near(got, want, 1e-12), f"{got:.8f} vs {want:.8f}")
    except ImportError:
        NOTES.append("statsmodels not installed: McNemar cross-check skipped")

    pv = {"a": 0.01, "b": 0.02, "c": 0.03, "d": 0.04, "e": 0.05}
    h = S.holm(pv)
    check("Holm on 0.01..0.05 gives 0.05,0.08,0.09,0.09,0.09",
          all(near(h[k], v, 1e-12) for k, v in zip("abcde", [0.05, 0.08, 0.09, 0.09, 0.09])),
          str({k: round(v, 4) for k, v in h.items()}))
    bh = S.benjamini_hochberg(pv)
    check("BH on 0.01..0.05 gives 0.05 throughout", all(near(v, 0.05, 1e-12) for v in bh.values()),
          str({k: round(v, 4) for k, v in bh.items()}))
    check("Holm is never smaller than BH", all(h[k] >= bh[k] - 1e-12 for k in pv))
    check("adjusted p values are monotone in the raw ones",
          all(h[x] <= h[y] + 1e-12 for x, y in zip("abcd", "bcde")))
    try:
        from statsmodels.stats.multitest import multipletests
        raw = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
        names = [f"t{i}" for i in range(len(raw))]
        d = dict(zip(names, raw))
        for meth, key in (("holm", "holm"), ("bh", "fdr_bh")):
            got = S.adjust(d, meth)
            want = multipletests(raw, method=key)[1]
            check(f"{meth} matches statsmodels on a 10-test family",
                  all(near(got[n], w, 1e-12) for n, w in zip(names, want)))
    except ImportError:
        pass


def test_permutation_and_effects():
    print("\n[3] permutation tests by enumeration, and effect sizes")
    r = S.permutation_diff_means([1, 2, 3], [4, 5, 6])
    check("exact permutation p for the most extreme split of 3 vs 3 is 2/20",
          r["exact"] and near(r["p"], 0.1, 1e-12), f"p={r['p']:.4f} over {r['permutations']} splits")
    r2 = S.permutation_diff_means([1, 2, 3], [1, 2, 3])
    check("identical groups give p = 1", near(r2["p"], 1.0, 1e-12))
    r3 = S.permutation_paired_diff([0.02, 0.03, 0.01, 0.04, 0.02, 0.05])
    check("paired sign-flip over 6 pairs, all same sign, gives the floor 2/64",
          r3["exact"] and near(r3["p"], 2 / 64, 1e-12), f"p={r3['p']:.5f}, floor={r3['smallest_possible_p']:.5f}")

    # type-I error of the Monte-Carlo path: under the null the p value should be near-uniform
    rng = np.random.default_rng(7)
    rej = 0
    trials = 300
    for i in range(trials):
        x = rng.normal(0, 1, 9)
        y = rng.normal(0, 1, 9)
        rej += S.permutation_diff_means(x, y, n_perm=400, seed=int(i), max_exact=10)["p"] <= 0.05
    rate = rej / trials
    check("permutation type-I error near 5 % under the null", 0.015 <= rate <= 0.09, f"measured {rate:.3f}")
    NOTES.append(f"permutation type-I error under the null (300 trials, n=9 vs 9): {rate:.3f}")

    check("Cohen's h for 0.75 vs 0.25 is pi/3", near(S.cohens_h(0.75, 0.25), math.pi / 3, 1e-12),
          f"{S.cohens_h(0.75, 0.25):.6f}")
    check("Cohen's h is 0 for equal proportions", near(S.cohens_h(0.42, 0.42), 0.0, 1e-15))
    check("Cohen's h is antisymmetric", near(S.cohens_h(0.9, 0.8), -S.cohens_h(0.8, 0.9), 1e-15))
    check("h near 1 is larger than the same raw gap near 0.5",
          abs(S.cohens_h(0.98, 0.96)) > abs(S.cohens_h(0.52, 0.50)),
          f"{S.cohens_h(0.98,0.96):.4f} vs {S.cohens_h(0.52,0.50):.4f}")
    nd = S.newcombe_diff(90, 100, 80, 100)
    check("Newcombe interval brackets the observed difference", nd[0] < 0.10 < nd[1],
          f"[{nd[0]:.4f}, {nd[1]:.4f}] around 0.1000")


# -------------------------------------------------------------------- 4. clustered coverage: the measured claim
def make_clustered(rng, n_cases, m, p, icc):
    """Beta-binomial: case rate ~ Beta(a,b) with mean p and intra-class correlation icc = 1/(a+b+1); items are
    Bernoulli given the case. The TRUE population proportion is p by construction, so coverage is measurable."""
    rows = []
    if icc <= 0:
        for c in range(n_cases):
            for j in range(m):
                rows.append({"case": f"c{c}", "y": int(rng.random() < p)})
        return rows
    s = 1.0 / icc - 1.0
    a, b = p * s, (1 - p) * s
    for c in range(n_cases):
        pc = rng.beta(a, b)
        for j in range(m):
            rows.append({"case": f"c{c}", "y": int(rng.random() < pc)})
    return rows


def coverage_run(label, n_cases, m, p, icc, sims, n_boot, seed):
    rng = np.random.default_rng(seed)
    cov_boot = cov_naive = 0
    w_boot, w_naive, deffs = [], [], []
    for i in range(sims):
        rows = make_clustered(rng, n_cases, m, p, icc)
        r = S.boot_proportion(rows, "case", "y", n_boot=n_boot, seed=int(i), alpha=0.05)
        lo, hi = r["ci"]
        nlo, nhi = r["naive_wilson"]
        cov_boot += int(lo <= p <= hi)
        cov_naive += int(nlo <= p <= nhi)
        w_boot.append(r["width_pp"])
        w_naive.append(r["naive_width_pp"])
        if r.get("design_effect"):
            deffs.append(r["design_effect"])
    out = dict(label=label, icc=icc, cases=n_cases, items=n_cases * m, sims=sims,
               coverage_cluster=cov_boot / sims, coverage_naive=cov_naive / sims,
               width_cluster_pp=float(np.mean(w_boot)), width_naive_pp=float(np.mean(w_naive)),
               design_effect=float(np.mean(deffs)) if deffs else None,
               design_effect_expected=1 + (m - 1) * icc)
    print(f"  {label:<26} ICC={icc:.2f}  {n_cases} cases x {m} items   "
          f"coverage: cluster {out['coverage_cluster']*100:5.1f} %   naive {out['coverage_naive']*100:5.1f} %   "
          f"width: {out['width_cluster_pp']:.2f} vs {out['width_naive_pp']:.2f} pp   "
          f"deff {out['design_effect']:.2f} (Kish {out['design_effect_expected']:.2f})")
    return out


def test_coverage(sims, n_boot):
    print("\n[4] coverage of a 95 % interval, measured against a known truth")
    ind = coverage_run("independent items", 30, 8, 0.85, 0.0, sims, n_boot, seed=11)
    clu = coverage_run("items clustered in cases", 30, 8, 0.85, 0.30, sims, n_boot, seed=12)
    big = coverage_run("more cases, same clustering", 120, 5, 0.90, 0.25, sims, n_boot, seed=13)

    check("naive interval covers correctly when items ARE independent",
          0.90 <= ind["coverage_naive"] <= 0.99, f"{ind['coverage_naive']*100:.1f} %")
    check("cluster bootstrap also covers when items are independent",
          0.88 <= ind["coverage_cluster"] <= 0.99, f"{ind['coverage_cluster']*100:.1f} %")
    check("cluster bootstrap is not wasteful on independent data (< 1.4x the naive width)",
          ind["width_cluster_pp"] / ind["width_naive_pp"] < 1.4,
          f"ratio {ind['width_cluster_pp']/ind['width_naive_pp']:.2f}")
    check("naive interval UNDER-COVERS on clustered data (this is why the library exists)",
          clu["coverage_naive"] < 0.85, f"{clu['coverage_naive']*100:.1f} % against a nominal 95 %")
    check("cluster bootstrap recovers coverage on clustered data",
          clu["coverage_cluster"] >= 0.88, f"{clu['coverage_cluster']*100:.1f} %")
    check("cluster bootstrap still covers with more, smaller clusters",
          big["coverage_cluster"] >= 0.89, f"{big['coverage_cluster']*100:.1f} %")
    check("measured design effect tracks Kish's 1+(m-1)*ICC",
          abs(clu["design_effect"] - clu["design_effect_expected"]) < 0.6,
          f"{clu['design_effect']:.2f} vs {clu['design_effect_expected']:.2f}")
    NOTES.append(f"clustered ICC=0.30, 30 cases x 8 items: naive coverage "
                 f"{clu['coverage_naive']*100:.1f} %, cluster bootstrap {clu['coverage_cluster']*100:.1f} %, "
                 f"widths {clu['width_naive_pp']:.2f} vs {clu['width_cluster_pp']:.2f} pp")
    return [ind, clu, big]


# ------------------------------------------- 4b. the ceiling, where every number in this project actually sits
def test_ceiling_coverage(sims, n_boot):
    """The coverage run above is at p = 0.85 and 0.90. EVERY headline this library is applied to is 0.91-0.99,
    and the percentile bootstrap degrades near a boundary. Measuring coverage only where the method works is how
    a library gets trusted outside the range it was checked in, so the operating point is measured here too.

    The result is not the comfortable one: at the ceiling the case-cluster interval under-covers badly, and at
    the shape of the held-out-device test it under-covers WORSE than the naive Wilson interval it replaces. The
    mechanism is degeneracy -- when every resampled case is perfect the interval collapses onto the point
    estimate -- so the failures are one-sided: the interval sits above the truth. These numbers are the evidence
    for boot_proportion's `ceiling_warning`, which this function also checks actually fires."""
    print("\n[4b] coverage AT THE REAL OPERATING POINT (0.94-0.98), where the paper's numbers live")
    rows = []
    shapes = [("p=0.85  34 cases x 9   (below the ceiling)", 34, 9, 0.85, 0.68),
              ("p=0.94  34 cases x 9   (fold 0, all views)", 34, 9, 0.94, 0.68),
              ("p=0.97  34 cases x 4   (fold 0, lateral)", 34, 4, 0.97, 0.90),
              ("p=0.98  28 cases x 2   (held-out-device test)", 28, 2, 0.98, 0.50)]
    for label, C, m, p, icc in shapes:
        rng = np.random.default_rng(41)
        cov = covn = above = below = degen = warned = 0
        for i in range(sims):
            r = S.boot_proportion(make_clustered(rng, C, m, p, icc), "case", "y",
                                  n_boot=n_boot, seed=int(i), alpha=0.05)
            lo, hi = r["ci"]
            nlo, nhi = r["naive_wilson"]
            cov += int(lo <= p <= hi)
            covn += int(nlo <= p <= nhi)
            above += int(p > hi)
            below += int(p < lo)
            degen += int(r["ci_degenerate"])
            warned += int("ceiling_warning" in r)
        d = dict(label=label, p=p, cases=C, items=m, icc=icc, coverage_cluster=cov / sims,
                 coverage_naive=covn / sims, truth_below_ci=below / sims, degenerate=degen / sims,
                 warned=warned / sims)
        rows.append(d)
        print(f"  {label:<46} cluster {100*d['coverage_cluster']:5.1f} %   naive {100*d['coverage_naive']:5.1f} %"
              f"   interval sat above the truth {100*d['truth_below_ci']:5.1f} %"
              f"   degenerate {100*d['degenerate']:5.1f} %   warned {100*d['warned']:5.0f} %")

    lowp, ceil97, ceil98 = rows[0], rows[2], rows[3]
    check("below the ceiling the cluster bootstrap does its job",
          lowp["coverage_cluster"] >= 0.88, f"{lowp['coverage_cluster']*100:.1f} % at p=0.85")
    check("AT the ceiling it does NOT: p=0.97 coverage is far below nominal",
          ceil97["coverage_cluster"] < 0.88, f"{ceil97['coverage_cluster']*100:.1f} % against a nominal 95 %")
    check("and at the held-out-device shape the naive interval BEATS it (the library's advice inverts here)",
          ceil98["coverage_naive"] > ceil98["coverage_cluster"],
          f"naive {ceil98['coverage_naive']*100:.1f} % vs cluster {ceil98['coverage_cluster']*100:.1f} %")
    miss_high = 1 - ceil97["coverage_cluster"] - ceil97["truth_below_ci"]   # truth was ABOVE the interval
    check("the failure is one-sided: the interval sits ABOVE the truth, i.e. it claims too much",
          ceil97["truth_below_ci"] > 4 * miss_high,
          f"{ceil97['truth_below_ci']*100:.1f} % too optimistic against {100*miss_high:.1f} % too pessimistic")
    # ceiling_warning is a SCREEN, not an oracle: it is measured here as one, with both error rates on record.
    # It caught 90-100 % of the replicates in the three broken regimes and fired on 17 % of the sound p=0.85 one.
    check("ceiling_warning catches almost every replicate in the regimes that are actually broken",
          min(r["warned"] for r in rows[1:]) >= 0.85,
          f"min {100*min(r['warned'] for r in rows[1:]):.0f} % over the three ceiling shapes")
    check("and is mostly quiet below the ceiling, where coverage is fine (a warning that always fires is noise)",
          lowp["warned"] < 0.30, f"{100*lowp['warned']:.0f} % at p=0.85 where coverage is "
                                 f"{100*lowp['coverage_cluster']:.1f} % -- a false-alarm rate, not a defect")
    NOTES.append(f"ceiling_warning as a screen: fires on "
                 f"{100*min(r['warned'] for r in rows[1:]):.0f}-{100*max(r['warned'] for r in rows[1:]):.0f} % of "
                 f"replicates where the interval is broken and on {100*lowp['warned']:.0f} % where it is not")
    NOTES.append("at the real operating point the case-cluster interval covers "
                 + ", ".join(f"{100*r['coverage_cluster']:.0f} % (p={r['p']})" for r in rows[1:])
                 + f" against a nominal 95 %; at p=0.98 the naive Wilson covers "
                   f"{100*ceil98['coverage_naive']:.0f} % and the cluster bootstrap "
                   f"{100*ceil98['coverage_cluster']:.0f} % -- near the ceiling report counts, not an interval")
    return rows


# ----------------------------------------------------- 5. paired null: which test to prefer, measured not argued
def test_paired_null(sims, n_boot):
    print("\n[5] two arms that are truly equal, with their disagreements clustered inside cases")
    rng = np.random.default_rng(21)
    n_cases, m, tau, mu = 25, 8, 2.2, 2.0
    rej_mcnemar = rej_boot = 0
    for i in range(sims):
        rows = []
        for c in range(n_cases):
            d = rng.normal(0.0, tau)                       # this case favours A or B; mean zero over cases
            pa = 1 / (1 + math.exp(-(mu + d / 2)))
            pb = 1 / (1 + math.exp(-(mu - d / 2)))
            for j in range(m):
                rows.append({"case": f"c{c}", "__a": int(rng.random() < pa), "__b": int(rng.random() < pb)})
        r = S.paired_compare(rows, "case", "__a", "__b", n_boot=n_boot, seed=int(i))
        rej_mcnemar += int(r["mcnemar_exact_p"] <= 0.05)
        rej_boot += int(r["excludes_zero"])
    pm, pb_ = rej_mcnemar / sims, rej_boot / sims
    print(f"  false-positive rate at 5 %:  McNemar exact {pm*100:5.1f} %   paired cluster bootstrap {pb_*100:5.1f} %")
    check("McNemar over-rejects when discordant items cluster inside cases",
          pm > 0.10 and pm > 2 * pb_, f"{pm*100:.1f} % against the bootstrap's {pb_*100:.1f} %")
    check("paired cluster bootstrap keeps its false-positive rate near 5 %", pb_ <= 0.12, f"{pb_*100:.1f} %")
    NOTES.append(f"paired null with clustered disagreements ({n_cases} cases x {m} items): McNemar rejects "
                 f"{pm*100:.1f} % of the time, the paired cluster bootstrap {pb_*100:.1f} % (nominal 5 %)")

    # and a real difference must still be found, or the bootstrap is merely inert
    def two_arms(seed, shared):
        """Arms scored on the same cases. `shared` puts a case-level difficulty into BOTH arms, which is the real
        situation (a dark, collimated, instrumented case is hard for every model)."""
        rng2 = np.random.default_rng(seed)
        rows = []
        for c in range(40):
            z = rng2.normal(0, 1.2) if shared else 0.0
            pa = 1 / (1 + math.exp(-(2.6 + z)))
            pb = 1 / (1 + math.exp(-(1.3 + z)))
            for j in range(6):
                rows.append({"case": f"c{c}", "__a": int(rng2.random() < pa), "__b": int(rng2.random() < pb)})
        return rows

    rows = two_arms(5, shared=True)
    r = S.paired_compare(rows, "case", "__a", "__b", n_boot=max(n_boot, 800), seed=0)
    check("a real double-digit difference is detected", r["excludes_zero"] and r["mcnemar_exact_p"] < 0.01,
          f"diff {r['diff_pp']:+.1f} pp, CI [{r['ci_pp'][0]:+.1f}, {r['ci_pp'][1]:+.1f}] pp, "
          f"McNemar p={r['mcnemar_exact_p']:.2e}")
    check("pairing narrows the interval when the two arms share case difficulty",
          r["pairing_narrowed_by"] is not None and r["pairing_narrowed_by"] > 1.1,
          f"unpaired/paired width = {r['pairing_narrowed_by']:.2f}x")
    ri = S.paired_compare(two_arms(6, shared=False), "case", "__a", "__b", n_boot=max(n_boot, 800), seed=0)
    check("and buys nothing when the arms are independent (pairing is not a free narrowing)",
          0.8 < ri["pairing_narrowed_by"] < 1.3, f"unpaired/paired width = {ri['pairing_narrowed_by']:.2f}x")
    NOTES.append(f"pairing narrows the interval of the difference by {r['pairing_narrowed_by']:.2f}x when the arms "
                 f"share case difficulty and by {ri['pairing_narrowed_by']:.2f}x when they do not")
    check("the point estimate matches a direct count",
          near(r["p_a"], np.mean([x["__a"] for x in rows]), 1e-12))


# ------------------------------------ 5b. the sparse-discordance regime the real two-arm comparison sits in
def test_sparse_paired(n_boot):
    """The paired null above generates dozens of disagreements per replicate. The comparison the library was
    actually applied to has FOUR: two leave-one-device-out detector arms on 56 shared frames from 28 cases.
    In that regime "excludes zero" stops being about the effect and becomes about how few cases the four
    disagreements happen to land in, because a percentile interval can only reach zero by drawing a resample
    containing none of them -- probability ((C-k)/C)^C, which is a step function of k.

    This checks the arithmetic of that step, checks that `excludes_zero_fragile` fires, and demonstrates the
    consequence: the SAME marginals with the same four disagreements moved into three cases no longer exclude
    zero, while McNemar's p does not move at all."""
    print("\n[5b] a difference carried by four frames: when 'excludes zero' is a property of the case layout")

    def build(disc_cases, C=28, per=2):
        rows = [{"case": f"c{c}", "__a": 1, "__b": 1} for c in range(C) for _ in range(per)]
        for i, c in enumerate(disc_cases):
            # one frame of case c flips; several entries of disc_cases may name the same case
            for r in rows:
                if r["case"] == f"c{c}" and r["__a"] == 1:
                    r["__a"] = 0
                    break
        return rows

    four_cases = S.paired_compare(build([0, 5, 11, 19]), "case", "__a", "__b", n_boot=max(n_boot, 4000), seed=0)
    three_cases = S.paired_compare(build([0, 0, 5, 11]), "case", "__a", "__b", n_boot=max(n_boot, 4000), seed=0)
    check("four discordant frames in four cases: the percentile interval excludes zero",
          four_cases["excludes_zero"], f"CI [{four_cases['ci_pp'][0]:+.2f}, {four_cases['ci_pp'][1]:+.2f}] pp")
    check("the same 4-frame difference packed into three cases does NOT exclude zero",
          not three_cases["excludes_zero"],
          f"CI [{three_cases['ci_pp'][0]:+.2f}, {three_cases['ci_pp'][1]:+.2f}] pp")
    check("McNemar is identical in both, because it never saw the case layout",
          near(four_cases["mcnemar_exact_p"], three_cases["mcnemar_exact_p"], 1e-12),
          f"{four_cases['mcnemar_exact_p']:.4f} both ways")
    check("the exact sign test over CASES agrees with McNemar in the four-case layout and cannot reject",
          near(four_cases["cluster_sign_test_p"], 0.125, 1e-12)
          and four_cases["cluster_sign_smallest_possible_p"] > 0.05,
          f"sign-test p={four_cases['cluster_sign_test_p']:.4f}, floor "
          f"{four_cases['cluster_sign_smallest_possible_p']:.4f}")
    check("so excludes_zero_fragile fires and the output refuses to call it established",
          four_cases["excludes_zero_fragile"] and "fragility_note" in four_cases,
          four_cases.get("fragility_note", "")[:96] + "...")
    check("bootstrap_zero_mass matches ((C-k)/C)^C",
          near(four_cases["bootstrap_zero_mass"], (24 / 28) ** 28, 1e-12),
          f"{four_cases['bootstrap_zero_mass']:.4f} against the 0.025 percentile threshold")
    # and the guard must NOT fire on a difference that many cases carry
    rng = np.random.default_rng(9)
    rows = []
    for c in range(40):
        for j in range(6):
            rows.append({"case": f"c{c}", "__a": int(rng.random() < 0.95), "__b": int(rng.random() < 0.75)})
    big = S.paired_compare(rows, "case", "__a", "__b", n_boot=max(n_boot, 2000), seed=0)
    check("and does NOT fire on a difference that most cases carry",
          big["excludes_zero"] and not big["excludes_zero_fragile"],
          f"{big['n_clusters_differing']}/{big['n_clusters']} cases differ, sign test "
          f"p={big['cluster_sign_test_p']:.2e}")
    NOTES.append(f"four discordant frames in four of 28 cases give a CI that excludes zero "
                 f"({four_cases['ci_pp'][0]:+.2f}, {four_cases['ci_pp'][1]:+.2f} pp) only because a resample "
                 f"misses all four with probability {four_cases['bootstrap_zero_mass']:.4f} < 0.025; the same "
                 f"marginals in three cases do not, and the exact sign test over cases is 0.125 either way")


# ---------------------------------------------------------------------------------- 6. power and design helpers
def test_power():
    print("\n[6] power, minimum detectable difference, certification")
    want = math.ceil(math.log(0.05) / math.log(0.99))
    got = S.n_for_lower_bound(0.99, 0.05, 0)
    check("n for a 99 % one-sided bound with no errors equals ceil(ln a / ln t)",
          got["n"] == want, f"{got['n']} (closed form {want}); lower bound {got['lower_bound']:.5f}")
    check("that bound really reaches the target",
          S.clopper_pearson_lower(got["n"], got["n"], 0.05) >= 0.99 > S.clopper_pearson_lower(got["n"] - 1,
                                                                                             got["n"] - 1, 0.05))
    one_err = S.n_for_lower_bound(0.99, 0.05, 1)
    check("one observed error costs more cases", one_err["n"] > got["n"], f"{one_err['n']} vs {got['n']}")

    mdd = S.mdd_two_proportions(600, 600, 0.90, power=0.8)
    pw = S.power_two_proportions(600, 600, 0.90, mdd["detectable_worse"], deff=1.0)
    check("power at the minimum detectable difference is the requested 80 %", near(pw, 0.80, 0.02),
          f"MDD {mdd['mdd_pp_worse']:.2f} pp -> power {pw:.3f}")
    nn = S.n_two_proportions(0.90, 0.80, power=0.8)
    pw2 = S.power_two_proportions(nn["n1"], nn["n2"], 0.90, 0.80)
    check("n_two_proportions returns an n that reaches the requested power", pw2 >= 0.79,
          f"n={nn['n1']} per arm -> power {pw2:.3f}")

    # against a Monte-Carlo of the test the formula approximates
    rng = np.random.default_rng(3)
    n1 = n2 = 300
    p1, p2 = 0.90, 0.82
    z = S.ND.inv_cdf(0.975)
    hit = 0
    trials = 2000
    for _ in range(trials):
        k1 = rng.binomial(n1, p1)
        k2 = rng.binomial(n2, p2)
        h = S.cohens_h(k1 / n1, k2 / n2)
        hit += int(abs(h) / math.sqrt(1 / n1 + 1 / n2) > z)
    mc = hit / trials
    formula = S.power_two_proportions(n1, n2, p1, p2)
    check("power formula agrees with a simulation of the same test", abs(mc - formula) < 0.05,
          f"simulated {mc:.3f} vs formula {formula:.3f}")

    # The pre-stated ">= 97 %" rule, read from both sides. The first version of this test asserted the obvious
    # failure (a bad system passing by luck) and FAILED, which is the useful half of the exercise: on 28 units the
    # rule rounds up to 28 of 28, so the binding problem is the opposite one -- a system that genuinely is 97 %
    # fails its own criterion most of the time. Both numbers are now computed and both are checked.
    cp = S.criterion_pass_probability(28, 0.97, 0.90)
    check("'>= 97 %' on 28 units really demands 28/28 (integer counts round the rule up)",
          cp["successes_needed"] == 28 and near(cp["effective_threshold"], 1.0, 1e-12),
          f"needs {cp['successes_needed']}/28 = {cp['effective_threshold']:.4f}")
    check("a truly 97 % system FAILS that criterion more often than it passes",
          cp["false_fail_probability"] > 0.5,
          f"false-fail {cp['false_fail_probability']*100:.1f} %, false-pass (true 90 %) "
          f"{cp['pass_probability']*100:.1f} %")
    check("the verdict names the underpowered direction", "cannot pass or fail" in cp["verdict"], cp["verdict"])
    NOTES.append(f"pre-stated criterion 'observed >= 97 %' on n=28 means 28/28: a truly 97 % system fails it "
                 f"{cp['false_fail_probability']*100:.1f} % of the time, and a truly 90 % one passes it "
                 f"{cp['pass_probability']*100:.1f} % of the time -- the experiment cannot settle its own criterion")
    cp2 = S.criterion_pass_probability(300, 0.97, 0.90)
    check("at n=300 the criterion at least separates 97 % from 90 %",
          cp2["pass_probability"] < 0.01 and cp2["discrimination"] > 0.5,
          f"false-pass {cp2['pass_probability']*100:.3f} %, discrimination {cp2['discrimination']:.2f}")
    check("larger n makes the rule less granular",
          S.criterion_pass_probability(300, 0.97, 0.90)["effective_threshold"] < cp["effective_threshold"],
          f"{cp2['effective_threshold']:.4f} vs {cp['effective_threshold']:.4f}")

    deff = S.design_effect_from_icc(5, 0.25)
    check("Kish design effect for 5 items at ICC 0.25 is 2.0", near(deff, 2.0, 1e-12))
    clustered = S.n_two_proportions(0.90, 0.80, deff=deff)
    check("clustering doubles the required n at deff 2", clustered["n1"] == 2 * nn["n1"],
          f"{clustered['n1']} vs {nn['n1']}")
    arm = S.plan_arm("phantom", 0.97, 0.90, items_per_case=5, icc=0.25)
    check("plan_arm returns a case count and states its assumptions",
          arm["cases_needed"] > 0 and "not a measurement" in arm["note"],
          f"{arm['cases_needed']} cases ({arm['items_needed']} vertebrae) at deff {arm['design_effect']:.2f}")


# --------------------------------------------------------------------------------------- 7. loader and coercion
def test_loader(tmp):
    print("\n[7] record loader, inheritance and the refusal to guess")
    import json
    doc = {"tag": "run7", "frames": [
        {"stem": "case1_LAT", "case": "case1", "view": "LAT", "truth": "frame-level",
         "items": [{"truth": "L4", "exact": True}, {"truth": "L5", "exact": False}]},
        {"stem": "case2_AP", "case": "case2", "view": "AP",
         "items": [{"truth": "L3", "exact": True}]}]}
    p = Path(tmp) / "nested.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    rows = S.load_records(str(p), "frames[].items[]")
    check("flattening yields one record per item", len(rows) == 3, f"{len(rows)}")
    check("each item inherited its frame's case id", all("case" in r for r in rows) and rows[0]["case"] == "case1")
    check("each item inherited the top-level tag", rows[0]["tag"] == "run7")
    check("the item's own field wins over the frame's", rows[0]["truth"] == "L4")
    kept, log = S.apply_where(rows, ["view=LAT"])
    check("--where filters and reports what it removed", len(kept) == 2 and log[0]["removed"] == 1, str(log))
    b = S.boot_proportion(rows, "case", "exact", n_boot=200, seed=0)
    check("proportion over the flattened rows is 2/3", near(b["p"], 2 / 3, 1e-12), f"{b['p']:.4f}")

    for bad in ("maybe", None, 2, 0.5):
        try:
            S.as_bool(bad)
            check(f"as_bool refuses {bad!r}", False)
        except ValueError:
            check(f"as_bool refuses {bad!r}", True)
    check("as_bool accepts the forms real files use",
          [S.as_bool(v) for v in (True, False, 1, 0, "true", "False", 1.0, 0.0)] == [1, 0, 1, 0, 1, 0, 1, 0])

    # an empty selection is a bug, not an answer: a mistyped path used to yield 0 rows, p=None and exit 0
    check("a --record-path that matches nothing yields no records (so the CLI must refuse it)",
          S.load_records(str(p), "frame[].items[]") == [])
    for fn, why in ((lambda: S.require_rows([], str(p), "frame[].items[]", None, []), "bad record-path"),
                    (lambda: S.require_rows([], str(p), "frames[].items[]", ["veiw=LAT"],
                                            [dict(filter="veiw=LAT", before=3, after=0, removed=3)]),
                     "filter that removed everything")):
        try:
            fn()
            check(f"require_rows stops on a {why}", False)
        except SystemExit as e:
            check(f"require_rows stops on a {why}", True, str(e)[:78])

    # load_values must survive a Windows absolute path: 'C:\\...json:dotted' splits at the WRONG colon under
    # str.partition and the numbers come back as a float-parse error on the drive letter.
    jf = Path(tmp) / "vals.json"
    jf.write_text(json.dumps({"fit": {"R2_held_out_by_fold": [0.9, 0.95, 0.97]}}), encoding="utf-8")
    v, src, _ = S.load_values(f"{jf}:fit.R2_held_out_by_fold")
    check("load_values reads an ABSOLUTE path with a drive letter", v == [0.9, 0.95, 0.97], f"from {src}")
    v2, _, _ = S.load_values("0.9,0.95,0.97")
    check("and still reads a plain comma list", v2 == [0.9, 0.95, 0.97])
    try:
        S.load_values(str(Path(tmp) / "missing.json") + ":fit.x")
        check("load_values names a missing file instead of parsing it as floats", False)
    except SystemExit as e:
        check("load_values names a missing file instead of parsing it as floats", True, str(e)[:78])

    m = S.meta("some/input.json", seed=3)
    check("meta records whether the working tree is dirty, so a SHA is not a false attribution",
          "code_dirty" in m and (m["code_dirty"] is None or ("code_sha_note" in m) == bool(m["code_dirty"])),
          f"code_sha={m['code_sha']} code_dirty={m['code_dirty']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="fewer replicates; coverage figures get noisier")
    ap.add_argument("--tmp", default=None, help="directory for the loader's scratch file "
                                                "(default: a fresh temp dir -- the old default of '.' dropped "
                                                "nested.json into whatever directory the suite was run from)")
    a = ap.parse_args()
    sims = 120 if a.quick else 400
    n_boot = 300 if a.quick else 600

    test_intervals()
    test_mcnemar_and_multiplicity()
    test_permutation_and_effects()
    cov = test_coverage(sims, n_boot)
    ceil_rows = test_ceiling_coverage(sims, n_boot)
    test_paired_null(max(sims // 2, 60), n_boot)
    test_sparse_paired(n_boot)
    test_power()
    tmp = a.tmp or tempfile.mkdtemp(prefix="stats_compare_test_")
    test_loader(tmp)

    print("\n--- measured, for the Methods paragraph ---")
    for n in NOTES:
        print("  " + n)
    print(f"\n  coverage table ({sims} replicates, {n_boot} bootstrap resamples each):")
    print(f"  {'setting':<28}{'ICC':>6}{'naive':>10}{'cluster':>10}{'naive w':>10}{'cluster w':>11}{'deff':>7}")
    for c in cov:
        print(f"  {c['label']:<28}{c['icc']:>6.2f}{c['coverage_naive']*100:>9.1f}%{c['coverage_cluster']*100:>9.1f}%"
              f"{c['width_naive_pp']:>10.2f}{c['width_cluster_pp']:>11.2f}{c['design_effect']:>7.2f}")

    print(f"\nfailures: {len(FAILS)}" + ("" if not FAILS else "  -> " + ", ".join(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
