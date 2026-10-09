# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/level_selective.py [tracked at 097933a]
"""What can this system promise, and on how many cases? A risk-coverage analysis of vertebral level identification.

The target asked for is 99% per-level accuracy. No published system reaches that on plain radiographs; the best
whole-spine MRI identification found in the literature is 96.5%, and that model can count from C2. The honest
form of the claim is therefore not an accuracy but a pair: among the vertebrae it NAMES, it is right 99% of the
time, and it names X% of them. This computes X, for three kinds of answer:

  leaf          the vertebra's name, one of 27
  region        the DAG node above it - cervical, upper thoracic, lower thoracic, upper lumbar, lower lumbar,
                lumbosacral junction, sacral - which is a clinically actionable answer when the leaf is not
                available, and which annotators have been shown to prefer over a flat set of candidate names
  run           every vertebra in the frame named correctly, which is what a surgeon actually acts on

and for two rules for deciding when to answer:

  softmax       answer when the top posterior clears a threshold; the baseline nothing has reliably beaten
  conformal     split conformal, optionally class-conditional (Mondrian), calibrated on a held-out set; answer
                when the prediction set is a singleton, or when it collapses to a single DAG node

A warning this implements rather than ignores: below about 50% accuracy at full coverage, abstention is not
guaranteed to raise accuracy on the answered set and can lower it (Jones et al., ICLR 2021, Proposition 1). The
report prints full-coverage accuracy first, per stratum, so that every curve below it is read in that light.

    python tools/level_selective.py --posteriors post.jsonl --out ~/selective
    python tools/level_selective.py --model ... --ctx ... --rung 1 --out ~/selective     # computes them first
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

REGION = {}
for i in range(1, 8):
    REGION[f"C{i}"] = "cervical"
for i in range(1, 8):
    REGION[f"T{i}"] = "upper thoracic"
for i in range(8, 14):
    REGION[f"T{i}"] = "lower thoracic"
for i in (1, 2, 3):
    REGION[f"L{i}"] = "upper lumbar"
for i in (4, 5, 6):
    REGION[f"L{i}"] = "lower lumbar"
REGION["sacrum"] = "sacral"


def clopper_pearson_lower(k, n, alpha=0.05):
    """one-sided lower bound on a proportion, exact."""
    if n == 0:
        return 0.0
    if k == n:
        return alpha ** (1.0 / n)
    try:
        from scipy.stats import beta
        return float(beta.ppf(alpha, k, n - k + 1)) if k > 0 else 0.0
    except Exception:
        p = k / n
        se = math.sqrt(max(p * (1 - p), 1e-12) / n)
        return max(0.0, p - 1.645 * se)


def risk_coverage(scores, correct, region_correct=None):
    """Sort by confidence and walk the threshold down. Returns the curve and the area under the generalized
    risk-coverage curve, which is the average risk of the failures the rule did not catch."""
    o = np.argsort(-np.asarray(scores, float))
    c = np.asarray(correct, bool)[o]
    n = len(c)
    cov = np.arange(1, n + 1) / n
    acc = np.cumsum(c) / np.arange(1, n + 1)
    risk = 1.0 - acc
    augrc = float(np.mean(risk * cov))
    out = {"coverage": cov, "accuracy": acc, "risk": risk, "augrc": augrc, "order": o}
    if region_correct is not None:
        rc = np.asarray(region_correct, bool)[o]
        out["region_accuracy"] = np.cumsum(rc) / np.arange(1, n + 1)
    return out


def coverage_at(curve, target_acc, key="accuracy", n_min=30):
    """The largest coverage at which selective accuracy is at least target, with its exact lower bound."""
    acc = curve[key]; cov = curve["coverage"]; n = len(acc)
    best = None
    for i in range(n_min - 1, n):
        if acc[i] >= target_acc:
            k = int(round(acc[i] * (i + 1)))
            best = {"coverage": float(cov[i]), "accuracy": float(acc[i]), "n_answered": i + 1,
                    "lower95": clopper_pearson_lower(k, i + 1)}
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--posteriors", required=True, help="jsonl: one row per vertebra with probs, true, case, stratum")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cal-frac", type=float, default=0.5, help="share of CASES used to calibrate; the rest is test")
    ap.add_argument("--alpha", type=float, nargs="*", default=[0.01, 0.05, 0.10])
    ap.add_argument("--seed", type=int, default=20260915)
    a = ap.parse_args()

    rows = []
    for l in open(os.path.expanduser(a.posteriors), encoding="utf-8", errors="replace"):
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("probs") and r.get("true"):
            rows.append(r)
    if not rows:
        print("no rows"); return 2
    order = rows[0].get("level_order") or sorted({r["true"] for r in rows})
    idx = {n: i for i, n in enumerate(order)}
    print(f"{len(rows)} vertebrae, {len({r.get('case') for r in rows})} cases, {len(order)} classes")

    # split by CASE, never by vertebra: two crops from one spine are not independent
    cases = sorted({str(r.get("case")) for r in rows})
    rng = np.random.default_rng(a.seed); rng.shuffle(cases)
    n_cal = int(len(cases) * a.cal_frac)
    cal_cases = set(cases[:n_cal]); test_cases = set(cases[n_cal:])
    cal = [r for r in rows if str(r.get("case")) in cal_cases]
    test = [r for r in rows if str(r.get("case")) in test_cases]
    print(f"calibration {len(cal)} vertebrae / {len(cal_cases)} cases; test {len(test)} / {len(test_cases)} cases")

    def top(r):
        p = np.asarray(r["probs"], float)
        i = int(p.argmax())
        return order[i], float(p[i]), p

    lines = ["# What the level model can promise, and on how many vertebrae", "",
             f"Held-out vertebrae: {len(rows)} from {len(cases)} cases. Split by case, "
             f"{len(cal_cases)} calibrating and {len(test_cases)} testing. Classes: {len(order)}.", ""]

    # ---- full coverage first, because everything below is read in its light
    acc_full = np.mean([top(r)[0] == r["true"] for r in test])
    reg_full = np.mean([REGION.get(top(r)[0], "?") == REGION.get(r["true"], "?") for r in test])
    lines += ["## Accuracy at full coverage", "",
              f"- leaf (the vertebra's name): **{100 * acc_full:.1f}%**",
              f"- region (the DAG node above it): **{100 * reg_full:.1f}%**", ""]
    if acc_full < 0.5:
        lines += ["> Below 50% at full coverage, abstention is not guaranteed to raise accuracy on the answered",
                  "> set and can lower it (Jones et al., ICLR 2021, Proposition 1, proven for a class of margin",
                  "> distributions in a binary framing). The curves below are reported with that in mind.", ""]

    # ---- softmax-response risk-coverage
    s = [top(r)[1] for r in test]
    ok = [top(r)[0] == r["true"] for r in test]
    ok_reg = [REGION.get(top(r)[0], "?") == REGION.get(r["true"], "?") for r in test]
    curve = risk_coverage(s, ok, ok_reg)
    lines += ["## Risk-coverage, softmax response", "",
              f"AUGRC (average risk of the failures the rule let through, lower is better): **{curve['augrc']:.4f}**", "",
              "| target accuracy among answered | leaf: coverage | n answered | 95% lower bound | region: coverage |",
              "|---|---|---|---|---|"]
    for t in (0.99, 0.975, 0.95, 0.90):
        L = coverage_at(curve, t)
        R = coverage_at(curve, t, key="region_accuracy") if "region_accuracy" in curve else None
        lines.append(f"| {100 * t:.1f}% | " +
                     (f"**{100 * L['coverage']:.1f}%** | {L['n_answered']} | {100 * L['lower95']:.1f}% | " if L else "not reached | - | - | ") +
                     (f"**{100 * R['coverage']:.1f}%** |" if R else "not reached |"))
    lines.append("")

    # ---- split conformal, marginal and class-conditional
    lines += ["## Conformal prediction", "",
              "Split conformal on the calibration cases, then applied unchanged to the test cases. A vertebra is "
              "ANSWERED when its prediction set is a singleton; otherwise the set is reported, and if every member "
              "of the set shares a region the region is still answerable.", "",
              "| alpha | set size (mean) | singletons | accuracy among singletons | one region | accuracy among those |",
              "|---|---|---|---|---|---|"]
    cal_scores = np.array([1.0 - np.asarray(r["probs"], float)[idx[r["true"]]] for r in cal])
    for alpha in a.alpha:
        n = len(cal_scores)
        q_level = min(1.0, math.ceil((n + 1) * (1 - alpha)) / n)
        qhat = float(np.quantile(cal_scores, q_level, method="higher")) if n else 1.0
        sizes = []; singles = []; single_ok = []; one_reg = []; one_reg_ok = []
        for r in test:
            p = np.asarray(r["probs"], float)
            keep = [order[i] for i in range(len(order)) if 1.0 - p[i] <= qhat]
            if not keep:
                keep = [order[int(p.argmax())]]
            sizes.append(len(keep))
            if len(keep) == 1:
                singles.append(1); single_ok.append(keep[0] == r["true"])
            else:
                singles.append(0)
            regs = {REGION.get(k, "?") for k in keep}
            if len(regs) == 1:
                one_reg.append(1); one_reg_ok.append(REGION.get(r["true"], "?") in regs)
            else:
                one_reg.append(0)
        ns = sum(singles); nr = sum(one_reg)
        lines.append(f"| {alpha:.2f} | {np.mean(sizes):.2f} | {100 * ns / len(test):.1f}% | "
                     + (f"{100 * np.mean(single_ok):.1f}%" if ns else "-")
                     + f" | {100 * nr / len(test):.1f}% | "
                     + (f"{100 * np.mean(one_reg_ok):.1f}%" if nr else "-") + " |")
    lines.append("")

    # ---- per class, because a marginal guarantee can be met while a rare class is never right
    lines += ["## Per class, at full coverage", "",
              "A marginal number can look well while the class the system exists to get right is never right.", "",
              "| level | n | accuracy | mean top posterior |", "|---|---|---|---|"]
    per = defaultdict(list)
    for r in test:
        t, c, _ = top(r)
        per[r["true"]].append((t == r["true"], c))
    for lv in order:
        v = per.get(lv)
        if v:
            lines.append(f"| {lv} | {len(v)} | {100 * np.mean([x[0] for x in v]):.1f}% | {np.mean([x[1] for x in v]):.3f} |")
    lines.append("")

    # ---- whole run, which is what a surgeon acts on
    by_case = defaultdict(list)
    for r in test:
        by_case[str(r.get("case"))].append(r)
    run_ok = []; run_conf = []
    for c, rs in by_case.items():
        preds = [top(r) for r in rs]
        run_ok.append(all(p[0] == r["true"] for p, r in zip(preds, rs)))
        run_conf.append(min(p[1] for p in preds))
    rcurve = risk_coverage(run_conf, run_ok)
    lines += ["## Whole run", "",
              f"A run is correct when every vertebra in the frame is named correctly. At full coverage: "
              f"**{100 * np.mean(run_ok):.1f}%** of {len(run_ok)} runs.", "",
              "| target | coverage | runs answered | 95% lower bound |", "|---|---|---|---|"]
    for t in (0.99, 0.95, 0.90):
        L = coverage_at(rcurve, t, n_min=10)
        lines.append(f"| {100 * t:.0f}% | " + (f"**{100 * L['coverage']:.1f}%** | {L['n_answered']} | {100 * L['lower95']:.1f}% |"
                                              if L else "not reached | - | - |"))
    lines += ["", "To certify 99% selective accuracy one-sided at 95% confidence with no observed error takes about",
              "298 answered cases; with a handful of errors, roughly double. Coverage figures resting on fewer",
              "answered cases than that are descriptive, not certified.", ""]

    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    (out / "SELECTIVE.md").write_text("\n".join(lines), encoding="utf-8")
    json.dump({"n": len(rows), "acc_full": float(acc_full), "region_full": float(reg_full),
               "augrc": curve["augrc"], "cal_cases": len(cal_cases), "test_cases": len(test_cases)},
              open(out / "selective.json", "w"), indent=1)
    print("\n".join(lines))
    print(f"\nwrote {out}/SELECTIVE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
