# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/transitional_detectors.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Four independent detectors of an extra presacral segment, each a continuous score, each failing differently.

WHY FOUR AND NOT ONE. The template decoder's own variant posterior fired on ZERO of 16,234 NHANES films. That
cannot be right: published prevalence for a lumbosacral transitional vertebra runs from about 4% to 36%
depending on the definition used, and for a purely numerical variant (a presacral count that is not 24) around
5% to 10%. A detector that never fires is not conservative, it is broken, and the reason was a fixed six-nat
prior charged once per run which the evidence on a six-body lumbar window never overcame. Replacing a bad
threshold with a differently bad threshold would teach nothing, so this module instead produces four scores
whose failure modes are different, calibrates them where ground truth exists, and reports where they agree.

THE FOUR, and the mechanism each one actually uses:

  D1  TEMPLATE LIKELIHOOD RATIO. The log-likelihood of the best spine template containing an extra segment
      against the best ordinary one, with NO prior. This is the decoder's own evidence, exposed as a continuous
      statistic instead of being collapsed by a threshold chosen in advance. It fails when the per-vertebra
      classifier is uncertain across the board, because then every template fits about equally.

  D2  ANCHOR-AND-COUNT DISAGREEMENT. Find the sacrum, count upward naming L5, L4 and so on, and compare that
      naming with the template fit. This is the paradigm published systems use, and its failure mode is the
      point: on a spine with an extra presacral segment, counting from an anchor shifts every name below the
      extra body by exactly one, while template fitting does not. So the DISAGREEMENT between them is evidence
      about the anatomy rather than noise. It fails when the sacrum is not in the field, which is why it
      abstains rather than scoring zero in that case.

  D3  EXPECTED LUMBAR COUNT. The posterior expected number of lumbar-type bodies between the thoracolumbar
      junction and the sacrum. An ordinary spine gives five, a sixth-lumbar spine six, and the expectation
      moves continuously between them, so no discrete decision is taken anywhere. It fails when the field of
      view cuts the lumbar column, which is detectable and is reported as an abstention.

  D4  COUNT-VERSUS-MORPHOLOGY DISAGREEMENT. The fraction of the run where the counted name and the shape-only
      name differ. A transitional body looks like neither of its neighbours, so the two readings part company
      around the junction. It fails on any out-of-domain image, where the two readings disagree everywhere for
      reasons that have nothing to do with anatomy.

D1 and D3 both read the same posterior, so they are NOT independent; D2 and D4 bring genuinely different
information. That is stated rather than hidden, because treating four correlated scores as four votes would
manufacture confidence that is not there.

HOW A THRESHOLD IS CHOSEN, AND WHY NOT FROM PREVALENCE. Tuning each threshold until the firing rate matches a
published prevalence would guarantee the headline number and measure nothing. Instead every threshold is fitted
on the CT renders, where the transitional status of each case IS known from the dataset manifest, at a stated
operating point. The rate the detector then produces on real radiographs is a PREDICTION, and comparing it with
published prevalence is a real external check that can fail.
"""
from __future__ import annotations

import numpy as np

from ordinal_spine_decode import CONFIGS, VARIANT_CONFIGS, marginalize, decode_run

LUMBAR = [f"L{i}" for i in range(1, 7)]
THORACIC = [f"T{i}" for i in range(1, 13)] + ["T13"]


def _idx(class_names):
    return {n: i for i, n in enumerate(class_names)}


def d1_template_llr(log_probs, class_names):
    """Log-likelihood ratio of the best variant template against the best ordinary one, no prior.

    Positive means the evidence favours an extra presacral segment. The units are nats over the whole run, so
    the score grows with the number of vertebrae seen; that is correct, since a longer run carries more
    evidence, but it means a threshold is not transferable between runs of very different length. `per_vertebra`
    is the same quantity divided by the run length, for when it is.
    """
    lp = np.asarray(log_probs, float)
    n = lp.shape[0]
    if n < 2:
        return {"score": 0.0, "per_vertebra": 0.0, "abstain": True,
                "reason": "fewer than two vertebrae: no sequence to fit a template to"}
    ix = _idx(class_names)
    best = {}
    for cname, template in CONFIGS.items():
        cols = [ix.get(t) for t in template]
        if any(c is None for c in cols):
            continue
        b = -np.inf
        for s in range(0, max(1, len(template) - n + 1)):
            if s + n > len(template):
                continue
            b = max(b, sum(lp[t, cols[s + t]] for t in range(n)))
        best[cname] = b
    ordn = best.get("ordinary", -np.inf)
    var = max((best[c] for c in VARIANT_CONFIGS if c in best), default=-np.inf)
    if not np.isfinite(ordn) or not np.isfinite(var):
        return {"score": 0.0, "per_vertebra": 0.0, "abstain": True, "reason": "no template fitted"}
    llr = float(var - ordn)
    return {"score": llr, "per_vertebra": llr / n, "abstain": False,
            "best_variant": max((c for c in VARIANT_CONFIGS if c in best), key=lambda c: best[c]),
            "reason": "log-likelihood of the best variant template against the best ordinary one"}


def d2_anchor_count(log_probs, class_names, sacrum_min=0.30):
    """Disagreement between counting up from the sacrum and fitting a whole-spine template.

    The count is the paradigm published systems use: identify one landmark, then walk the chain. Under an extra
    presacral segment it shifts everything above the extra body relative to a template fit, so the signed size
    of the disagreement carries the anatomy. It abstains when no body is confidently the sacrum, because a count
    from a landmark that is not in the picture is not a weak answer, it is no answer.
    """
    lp = np.asarray(log_probs, float)
    n = lp.shape[0]
    ix = _idx(class_names)
    if n < 3 or "sacrum" not in ix:
        return {"score": 0.0, "abstain": True, "reason": "run too short, or no sacrum class"}
    p = np.exp(lp)
    sac_col = p[:, ix["sacrum"]]
    j = int(np.argmax(sac_col))
    if float(sac_col[j]) < sacrum_min or j == 0:
        return {"score": 0.0, "abstain": True,
                "reason": f"no vertebra reaches p(sacrum) >= {sacrum_min:.2f}; the anchor is not in the field"}
    # count upward from the sacrum through the ORDINARY sequence, which is what an anchor-and-count system does
    counted = [None] * n
    counted[j] = "sacrum"
    ladder = [f"L{i}" for i in range(5, 0, -1)] + [f"T{i}" for i in range(12, 0, -1)] + \
             [f"C{i}" for i in range(7, 0, -1)]
    k = 0
    for i in range(j - 1, -1, -1):
        counted[i] = ladder[k] if k < len(ladder) else None
        k += 1
    dec = decode_run(lp, class_names, allow_variants=True, variant_prior=0.0)
    fitted = dec.get("names") or []
    if len(fitted) != n:
        return {"score": 0.0, "abstain": True, "reason": "template fit returned a different run length"}
    dis = sum(1 for a, b in zip(counted[:j], fitted[:j]) if a is not None and a != b)
    above = max(1, j)
    return {"score": float(dis / above), "abstain": False, "n_disagree": dis, "n_above_anchor": above,
            "anchor_index": j, "p_sacrum": float(sac_col[j]),
            "counted": [c for c in counted if c], "fitted": fitted,
            "reason": "fraction of bodies above the sacral anchor where counting and template fitting differ"}


def d3_expected_lumbar_count(log_probs, class_names, variant_prior=0.0, temperature=1.0):
    """Posterior expected number of lumbar-type bodies. Five for an ordinary spine, six for a sixth lumbar.

    Read from the placement marginal rather than from any single naming, so it moves continuously and never
    takes a discrete decision. It abstains unless the run shows BOTH ends of the lumbar column, because a
    partial view of the lumbar spine gives a count that is small for reasons of framing rather than anatomy.
    """
    lp = np.asarray(log_probs, float)
    n = lp.shape[0]
    if n < 3:
        return {"score": 0.0, "abstain": True, "reason": "run too short"}
    marg, p_variant, _ = marginalize(lp, class_names, variant_prior=variant_prior, temperature=temperature)
    ix = _idx(class_names)
    lum_cols = [ix[l] for l in LUMBAR if l in ix]
    tho_cols = [ix[t] for t in THORACIC if t in ix]
    sac = ix.get("sacrum")
    exp_lumbar = float(marg[:, lum_cols].sum())
    p_any_thoracic = float(marg[:, tho_cols].sum(1).max()) if tho_cols else 0.0
    p_any_sacrum = float(marg[:, sac].max()) if sac is not None else 0.0
    missing = []
    if p_any_thoracic < 0.5:
        missing.append("no thoracic body above the lumbar column")
    if p_any_sacrum < 0.5:
        missing.append("no sacrum below it")
    return {"score": exp_lumbar, "abstain": bool(missing), "missing": missing,
            "p_variant_from_marginal": float(p_variant),
            "reason": "expected number of lumbar-type bodies between the thoracolumbar junction and the sacrum"}


def d4_count_vs_morphology(log_probs, class_names, variant_prior=0.0):
    """Fraction of the run where the counted name and the shape-only name disagree.

    The shape-only name is the per-vertebra argmax, which uses no sequence information at all. The counted name
    comes from the template fit. A transitional body resembles neither neighbour, so the two readings part
    company near the junction; an out-of-domain image makes them part company everywhere, which is why this is
    the least specific of the four and is never used alone.
    """
    lp = np.asarray(log_probs, float)
    n = lp.shape[0]
    if n < 3:
        return {"score": 0.0, "abstain": True, "reason": "run too short"}
    morph = [class_names[int(i)] for i in lp.argmax(1)]
    dec = decode_run(lp, class_names, allow_variants=True, variant_prior=variant_prior)
    fitted = dec.get("names") or []
    if len(fitted) != n:
        return {"score": 0.0, "abstain": True, "reason": "template fit returned a different run length"}
    dis = sum(1 for a, b in zip(morph, fitted) if a != b)
    return {"score": float(dis / n), "abstain": False, "n_disagree": dis, "n": n,
            "reason": "fraction of the run where the shape-only name and the counted name differ"}


DETECTORS = {
    "D1_template_llr": d1_template_llr,
    "D2_anchor_count": d2_anchor_count,
    "D3_expected_lumbar": d3_expected_lumbar_count,
    "D4_count_vs_morph": d4_count_vs_morphology,
}

# Published prevalence, for the external check. Each figure carries the DEFINITION it was measured under,
# because the reported range for a lumbosacral transitional vertebra spans roughly 4% to 36% and almost all of
# that spread is definitional rather than biological. These are targets to compare against, never to tune to.
PREVALENCE = {
    "LSTV_any_Castellvi": (0.04, 0.36, "any Castellvi type; the spread is mostly definition and modality"),
    "numerical_variant": (0.05, 0.10, "a presacral count that is not 24"),
    "six_lumbar": (0.02, 0.05, "six mobile lumbar bodies"),
    "thirteenth_thoracic": (0.005, 0.02, "thirteen rib-bearing vertebrae"),
}


def score_all(log_probs, class_names, **kw):
    """Every detector on one run, as a dict of dicts. Nothing is combined here; combination needs calibration."""
    out = {}
    for name, fn in DETECTORS.items():
        try:
            out[name] = fn(log_probs, class_names, **({} if name != "D3_expected_lumbar" else
                                                      {"variant_prior": kw.get("variant_prior", 0.0)}))
        except Exception as e:  # noqa: BLE001
            out[name] = {"score": 0.0, "abstain": True, "reason": f"errored: {e}"}
    return out
