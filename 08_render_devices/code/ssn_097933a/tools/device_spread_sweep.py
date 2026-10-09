#!/usr/bin/env python
"""How much of a device's learned distribution a styled frame can actually reach, and a gate that reaches nearly all of it.

THE DEFECT THIS MEASURES. `device_style.sample_terms` draws the per-frame vector from the card's fitted Gaussian
copula and then clips EVERY term to the card's central quantile band -- at `SPREAD = 0.2`, each term's 20th to 80th
percentile. The clip was added for a real reason: the first demo sheets paired an extreme photon count with an
extreme blur and looked like pure grain beside pure smear. But it is the wrong instrument for that problem, in two
ways that only show up when the terms are counted.

  * The problem was a JOINT one: a combination of terms the device never produces together.
    The clip is a MARGINAL operation: it shrinks every term independently.
  * `np.clip` SATURATES rather than truncates: a draw outside the band is pinned to the boundary VALUE, not
    redrawn. So each clipped term carries a point mass of weight s at each end of its range.

A marginal clip pays for joint plausibility in joint coverage, and the price compounds with the number of terms. With
k correlated terms each confined to the central 1-2s of its marginal, the reachable share of the fitted joint
distribution is the probability that all k normal scores land inside the band, which this file computes exactly under
the card's own fitted correlation. For nine to eleven terms at s = 0.2 it is not 60 %.

THE REPLACEMENT. Draw from the full copula and reject only the draws the device itself would not produce: those whose
Mahalanobis distance in copula normal scores exceeds the card's own 99th-percentile typicality threshold -- the same
statistic `device_fit.coverage` already validates the card against on held-out frames. That keeps every marginal
intact, reaches 99 % of the joint distribution by construction, and removes exactly the implausible COMBINATIONS the
clip was aimed at. The two are measured side by side here, and then on a detector, before either is adopted.

    python tools/device_spread_sweep.py --out docs --figure

Writes docs/DEVICE_SPREAD_SWEEP.{md,json} and docs/figures/fig_device_spread.png. Card-only: no frames are read, so
this is cheap and exactly reproducible from the committed cards.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
import device_style as DS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "devices"
SPREADS = [0.0, 0.025, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
N_MC = 200_000


def reach(cop, spreads, n=N_MC, seed=11, q=99.0):
    """For each spread: the share of the fitted joint distribution a clipped draw can reach, and the share of the
    device's TYPICAL draws (Mahalanobis within the card's own 99th percentile) that survive the clip.

    Exact in normal-score space: clipping term j to its [s, 1-s] marginal quantiles is clipping z_j to
    [Phi^-1(s), Phi^-1(1-s)], because the copula's marginal transform is monotone.
    """
    names = cop["names"]; C = np.array(cop["corr"], float); k = len(names)
    rng = np.random.default_rng(seed)
    Z = rng.multivariate_normal(np.zeros(k), C, size=n)
    Ci = np.linalg.inv(C + 1e-6 * np.eye(k))
    d2 = np.einsum("ij,jk,ik->i", Z, Ci, Z)
    thr = float(np.percentile(d2, q))
    typical = d2 <= thr
    out = []
    for s in spreads:
        if s <= 0:
            inside = np.ones(n, bool)
        else:
            lo, hi = norm.ppf(s), norm.ppf(1 - s)
            inside = np.all((Z >= lo) & (Z <= hi), axis=1)
        if s <= 0:
            n_pinned = np.zeros(n)
        else:
            n_pinned = ((Z < lo) | (Z > hi)).sum(axis=1).astype(float)
        out.append(dict(spread=round(float(s), 3),
                        joint_mass=float(inside.mean()),
                        per_term_mass=float(max(0.0, 1 - 2 * s)),
                        # np.clip SATURATES: an out-of-band draw is not rejected, it is pinned to the boundary VALUE.
                        # So the clip does not merely narrow each marginal, it puts a point mass of weight s at each
                        # end of it, and a frame carries one such pinned term for every term that fell outside.
                        frames_with_a_pinned_term=float((n_pinned > 0).mean()),
                        pinned_terms_per_frame=float(n_pinned.mean()),
                        typical_draws_kept=float((inside & typical).sum() / max(typical.sum(), 1)),
                        atypical_draws_kept=float((inside & ~typical).sum() / max((~typical).sum(), 1))))
    gate = dict(name="typicality", joint_mass=float(typical.mean()), per_term_mass=1.0,
                typical_draws_kept=1.0, atypical_draws_kept=0.0, d2_99=thr,
                how=f"draw from the full copula, reject d2 > the card's own {q:.0f}th percentile")
    return names, out, gate


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "docs"))
    ap.add_argument("--figure", action="store_true")
    a = ap.parse_args()
    res = {}
    for p in sorted(DOCS.glob("*.json")):
        if ".3free." in p.name:
            continue
        card = json.load(open(p))
        cop = (card.get("distribution") or {}).get("copula")
        if not cop or not cop.get("names"):
            continue
        names, rows, gate = reach(cop, SPREADS)
        res[p.stem] = dict(terms=names, k=len(names), copula_n=int(cop.get("n") or 0), rows=rows, gate=gate)
        cur = [r for r in rows if abs(r["spread"] - DS.SPREAD) < 1e-9]
        c = cur[0] if cur else rows[-1]
        print(f"{p.stem:<16} k={len(names):>2}  at spread {DS.SPREAD}: joint mass {c['joint_mass']:6.2%}  "
              f"typical draws kept {c['typical_draws_kept']:6.2%}   | typicality gate: {gate['joint_mass']:.2%}", flush=True)

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(spread_in_code=DS.SPREAD, spreads=SPREADS, devices=res), open(out / "DEVICE_SPREAD_SWEEP.json", "w"), indent=1)

    worst = min((v["rows"][[r["spread"] for r in v["rows"]].index(DS.SPREAD)]["joint_mass"] for v in res.values()), default=0)
    best = max((v["rows"][[r["spread"] for r in v["rows"]].index(DS.SPREAD)]["joint_mass"] for v in res.values()), default=0)
    L = [f"# How much of each C-arm's learned distribution a styled frame reaches", "",
         "Generated by `tools/device_spread_sweep.py` from the committed cards alone.", "",
         "## The finding", "",
         f"`device_style.SPREAD = {DS.SPREAD}` clips every per-frame term to its central "
         f"{1 - 2 * DS.SPREAD:.0%} of the fitted marginal. Because the clip is applied to all "
         f"{min(v['k'] for v in res.values())}-{max(v['k'] for v in res.values())} terms at once, the share of the "
         f"fitted JOINT distribution a styled frame can reach is between **{worst:.1%}** and **{best:.1%}**, not "
         f"{1 - 2 * DS.SPREAD:.0%}. The clip was added to stop draws that paired an extreme photon count with an "
         "extreme blur -- a joint implausibility -- and it is a marginal instrument, so it pays for that in joint "
         "coverage and the price compounds with the number of terms.", "",
         "A typicality gate does the intended job without the price: draw from the full copula and reject only the "
         "draws whose Mahalanobis distance in copula normal scores exceeds the card's own 99th percentile -- the same "
         "statistic `device_fit.coverage` already validates each card against on held-out frames. Every marginal stays "
         "intact and 99 % of the joint distribution stays reachable.", "",
         "| device | terms | frames fitted | joint mass at "
         f"spread {DS.SPREAD} | typical draws kept | joint mass, typicality gate |",
         "|---|---:|---:|---:|---:|---:|"]
    for d, v in sorted(res.items()):
        i = [r["spread"] for r in v["rows"]].index(DS.SPREAD)
        r = v["rows"][i]
        L.append(f"| `{d}` | {v['k']} | {v['copula_n']} | {r['joint_mass']:.1%} | {r['typical_draws_kept']:.1%} | "
                 f"{v['gate']['joint_mass']:.1%} |")
    L += ["", "## The clip saturates; it does not truncate", "",
          "`np.clip` pins an out-of-band draw to the boundary VALUE rather than rejecting it, so each clipped term",
          f"carries a point mass of weight {DS.SPREAD:.0%} at each end of its range. Per frame, at the spread in code:", "",
          "| device | frames with at least one pinned term | pinned terms per frame (of k) |", "|---|---:|---:|"]
    for d, v in sorted(res.items()):
        r = v["rows"][[x["spread"] for x in v["rows"]].index(DS.SPREAD)]
        L.append(f"| `{d}` | {r['frames_with_a_pinned_term']:.1%} | "
                 f"{r['pinned_terms_per_frame']:.1f} of {v['k']} |")
    L += ["", "This is visible in `docs/figures/fig_device_params.png` as spikes in the blue histograms: the kilovoltage",
          "of a clipped draw is not a narrowed distribution but a handful of stacked values.", "",
          "## Reachable joint mass against the clip width", "",
          "| device | " + " | ".join(f"s={s}" for s in SPREADS) + " |",
          "|---" * (len(SPREADS) + 1) + "|"]
    for d, v in sorted(res.items()):
        L.append(f"| `{d}` | " + " | ".join(f"{r['joint_mass']:.1%}" for r in v["rows"]) + " |")
    L += ["", "Neither number settles what a detector should be trained on: a sampler that reaches more of the",
          "distribution is not automatically better training data. That is measured on real frames in",
          "`slurm/device_spread_arm.sh`, which trains the same detector on a corpus styled under each rule.", ""]
    (out / "DEVICE_SPREAD_SWEEP.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote", out / "DEVICE_SPREAD_SWEEP.md")

    if a.figure:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
        for d, v in sorted(res.items()):
            s = [r["spread"] for r in v["rows"]]
            ax[0].plot(s, [100 * r["joint_mass"] for r in v["rows"]], marker="o", ms=3.5, label=f"{d} (k={v['k']})")
            ax[1].plot(s, [100 * r["typical_draws_kept"] for r in v["rows"]], marker="o", ms=3.5)
        for A, ttl, yl in ((ax[0], "Reachable share of the fitted joint distribution", "% of the fitted distribution"),
                           (ax[1], "Typical draws the clip keeps", "% of draws inside the card's own 99th pct")):
            A.axvline(DS.SPREAD, color="#c00000", lw=1.2)
            A.text(DS.SPREAD, A.get_ylim()[1] * .02 + 2, f" in code: {DS.SPREAD}", color="#c00000", fontsize=7)
            A.set_xlabel("clip width s (each term held to its central 1-2s)")
            A.set_ylabel(yl, fontsize=8); A.set_title(ttl, fontsize=9); A.grid(alpha=.3)
        ax[0].legend(fontsize=7, frameon=False)
        p = out / "figures" / "fig_device_spread.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(p, dpi=170)
        print("wrote", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
