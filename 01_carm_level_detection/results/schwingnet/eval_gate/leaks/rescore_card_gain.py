#!/usr/bin/env python
"""EVAL_LEAKS re-read: the pooled image-formation card gain on the patient-held-out folds only.

WHY. The 24-fold card gain (results/stats_review/recompute.json#R2_card; NUMBERS 'card gain'; supplement 'raised held-out
R^2 by 0.038 ... over 24 folds') pools four leave-one-group-out fits. Two are held out by PATIENT: Cios Fusion (folds are
the six DeepFluoro specimens) and Elekta XVI (folds are COBRA cases, md5-folded). Two are not: BV Pulsera is ONE Geneva
phantom (folds by view) and PIXIUM 4600 is ONE Ljubljana cadaver (folds by frame), so every fold of those two scores the
subject the card was fitted on (CHK-9: SEEN; docs/devices/eval_gate/{bv_pulsera,pixium_4600}.json). Nothing about them
can be made patient-held-out -- there is no second subject -- so the only unseen subset is the 12 Cios Fusion + Elekta XVI
folds. This re-reads results/a6.json (per-fold gain and frames, as fitted) and recomputes the pooled statistics on them.

    python SchwingNet/results/eval_gate/leaks/rescore_card_gain.py      # writes leaks/card_gain_unseen.json
"""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE.parents[1]                      # SchwingNet/results
A6 = RES / "a6.json"
GATES = RES.parents[1] / "docs" / "devices" / "eval_gate"
B, SEED = 10000, 0


def folds_of(dev):
    d = json.load(open(A6, encoding="utf-8"))["per_device"][dev]
    return [dict(device=dev, held=f["held"], n=int(f["n_frames"]), gain=float(f["gain"])) for f in d["folds"]]


def signflip_exact(vals):
    if len(vals) > 16:     # 2^24 sign patterns is minutes in pure Python; the 24-fold value is read from recompute.json
        return json.load(open(RES / "stats_review" / "recompute.json", encoding="utf-8"))["R2_card"]["signflip_exact_24_folds"]
    obs = sum(vals) / len(vals)
    ge = 0
    for signs in itertools.product((1, -1), repeat=len(vals)):
        if sum(s * v for s, v in zip(signs, vals)) / len(vals) >= obs - 1e-15:
            ge += 1
    return ge / 2 ** len(vals)


def boot(vals, weights=None):
    rng = random.Random(SEED)
    out = []
    idx = list(range(len(vals)))
    for _ in range(B):
        pick = [rng.choice(idx) for _ in idx]
        if weights:
            w = sum(weights[i] for i in pick)
            out.append(sum(vals[i] * weights[i] for i in pick) / w)
        else:
            out.append(sum(vals[i] for i in pick) / len(pick))
    out.sort()
    return [out[int(0.025 * B)], out[int(0.975 * B) - 1]]


def summary(F):
    g = [f["gain"] for f in F]
    n = [f["n"] for f in F]
    return dict(n_folds=len(F), frames=sum(n), negative_folds=sum(1 for x in g if x < 0),
                mean_unweighted=sum(g) / len(g), mean_unweighted_ci_percentile=boot(g),
                mean_frame_weighted=sum(a * b for a, b in zip(g, n)) / sum(n), mean_frame_weighted_ci_percentile=boot(g, n),
                median=sorted(g)[len(g) // 2] if len(g) % 2 else sum(sorted(g)[len(g) // 2 - 1:len(g) // 2 + 1]) / 2,
                signflip_exact=signflip_exact(g))


def main() -> int:
    held, within = [], []
    gates = {}
    for dev in ("cios_fusion", "elekta_xvi", "bv_pulsera", "pixium_4600"):
        g = json.load(open(GATES / f"{dev}.json", encoding="utf-8"))
        gates[dev] = dict(held_out=g.get("held_out"), overlap=g.get("overlap"), n_checks=g.get("n_checks"))
        (held if g.get("held_out") else within).extend(folds_of(dev))
    out = dict(
        source=str(A6.relative_to(RES.parents[1])), gate_records=gates, bootstrap=f"{B} resamples of folds, seed {SEED}, percentile",
        all_24=summary(held + within), patient_held_out_12=summary(held), within_subject_12=summary(within),
        devices_patient_held_out=sorted({f["device"] for f in held}), devices_within_subject=sorted({f["device"] for f in within}))
    json.dump(out, open(HERE / "card_gain_unseen.json", "w", encoding="utf-8"), indent=1)
    for k in ("all_24", "patient_held_out_12", "within_subject_12"):
        s = out[k]
        print(f"{k:22s} folds {s['n_folds']:2d} frames {s['frames']:4d} neg {s['negative_folds']}  mean {s['mean_unweighted']:.4f} "
              f"{[round(x, 4) for x in s['mean_unweighted_ci_percentile']]}  frame-weighted {s['mean_frame_weighted']:.4f} "
              f"{[round(x, 4) for x in s['mean_frame_weighted_ci_percentile']]}  median {s['median']:.4f}  sign-flip p {s['signflip_exact']:.5f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
