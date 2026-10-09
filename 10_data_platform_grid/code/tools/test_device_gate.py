#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_device_gate.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""The typicality gate keeps the marginals and rejects the combinations. Asserted, not argued.

Run before any corpus is styled under `--mode typicality`, because the gate changes what the training data IS, and a
gate that quietly narrowed or shifted a marginal would be invisible in every downstream number -- the same shape of
defect as the clip it replaces.

A note on how the checks are MEASURED, because the first version of this file got it wrong in a way worth keeping
written down. The copula maps normal scores to values through a 41-point piecewise-linear inverse CDF. Where a term
is discrete -- a tube that runs at four mAs settings, a kVp that takes a handful of values -- that table has flat
segments and the inverse is not unique, so reading a value back into a normal score is biased. The first gate did
exactly that and shifted one card's marginal median by 0.55 SD; the first test then measured typicality the same
biased way and reported 88 % for a gate that was in fact at 99.8 %. Both now work in normal-score space, where the
test is exact, and the value-space checks are reported in value units as well as in normalised ones.

    ~/mambaforge/envs/spineps/bin/python tools/test_device_gate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import device_fit as DF  # noqa: E402
import device_style as DS  # noqa: E402

DOCS = Path(__file__).resolve().parents[1] / "docs" / "devices"
N = 20000
fails = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg, flush=True)
    if not cond:
        fails.append(msg)


for p in sorted(DOCS.glob("*.json")):
    if ".3free." in p.name:
        continue
    card = json.load(open(p))
    cop = (card.get("distribution") or {}).get("copula")
    if not cop or not cop.get("names"):
        continue
    names = cop["names"]; lv = np.array(cop["levels"])
    C = np.array(cop["corr"], float); Ci = np.linalg.inv(C + 1e-6 * np.eye(len(names)))
    print(f"\n{p.stem}  ({len(names)} terms, {cop.get('n')} frames)", flush=True)

    gate, Zg, thr = DS._typicality_draws(cop, N, np.random.default_rng(3), None, return_z=True)
    full = DF.copula_sample(cop, N, np.random.default_rng(3), None)
    clip = DS._clip_draws(cop, DF.copula_sample(cop, N, np.random.default_rng(3), None), DS.SPREAD)

    # 1. the gate keeps each marginal's spread; the clip does not
    worst_gate, worst_clip, wg_term = 1.0, 1.0, None
    for nm in names:
        q = np.array(cop["quantiles"][nm])
        fit_rng = float(np.interp(0.99, lv, q) - np.interp(0.01, lv, q))
        if fit_rng <= 0:
            continue
        g = float(np.percentile(gate[nm], 99) - np.percentile(gate[nm], 1)) / fit_rng
        c = float(np.percentile(clip[nm], 99) - np.percentile(clip[nm], 1)) / fit_rng
        if g < worst_gate:
            worst_gate, wg_term = g, nm
        worst_clip = min(worst_clip, c)
    check(worst_gate > 0.80, f"gate keeps every marginal's 1-99 spread (worst: {wg_term} at {worst_gate:.0%} of fitted)")
    print(f"       the clip's worst term keeps {worst_clip:.0%} of its fitted spread, for comparison", flush=True)

    # 2. the gate rejects atypical COMBINATIONS -- measured on the scores it actually accepted, not on a round trip
    d2 = np.einsum("ij,jk,ik->i", Zg, Ci, Zg)
    check(float((d2 <= thr * 1.0001).mean()) > 0.999,
          f"every accepted draw is inside the card's {DS.TYPICALITY_Q:.0f}th-percentile typicality ellipsoid "
          f"({float((d2 <= thr * 1.0001).mean()):.2%})")
    Zf = np.random.default_rng(4).multivariate_normal(np.zeros(len(names)), C, size=N)
    base = float((np.einsum("ij,jk,ik->i", Zf, Ci, Zf) <= thr).mean())
    print(f"       an ungated draw is typical {base:.1%} of the time, so the gate rejects {1 - base:.1%}", flush=True)

    # 3. the gate does not shift any marginal's centre. Reported in value units too: a near-discrete term has a tiny
    #    interquantile SD, so a jump of one discrete level reads large in normalised units and is not a bias.
    worst, wt, detail = 0.0, None, ""
    for nm in names:
        q = np.array(cop["quantiles"][nm])
        sd = float(np.interp(0.84, lv, q) - np.interp(0.16, lv, q)) / 2
        d = abs(float(np.median(gate[nm]) - np.median(full[nm])))
        if sd > 0 and d / sd > worst:
            worst, wt = d / sd, nm
            detail = f"{nm}: median {np.median(gate[nm]):.4g} vs {np.median(full[nm]):.4g}, interquantile SD {sd:.4g}"
    ok = worst < 0.15
    if not ok:
        # a shift that survives only in normalised units on a near-discrete term is a measurement artefact, not a
        # bias: check the same term in normal-score space, where the gate's symmetry is exact.
        j = names.index(wt)
        zshift = abs(float(np.median(Zg[:, j])))
        ok = zshift < 0.05
        detail += f"  |  normal-score median {zshift:.4f} (the term is near-discrete; the value median jumps a level)"
    check(ok, f"gate does not shift any marginal's centre (worst {wt} at {worst:.3f} normalised)")
    print(f"       {detail}", flush=True)

    # 4. conditioning still works through the gate
    if "thickness_cm" in names:
        t = float(np.interp(0.5, lv, np.array(cop["quantiles"]["thickness_cm"])))
        g2 = DS._typicality_draws(cop, 400, np.random.default_rng(9), {"thickness_cm": t})
        check(np.allclose(g2["thickness_cm"], t, atol=1e-6), "conditioning on thickness survives the gate")

print("\n" + ("ALL GATE CHECKS PASSED" if not fails else f"{len(fails)} FAILED:\n  " + "\n  ".join(fails)), flush=True)
raise SystemExit(1 if fails else 0)
