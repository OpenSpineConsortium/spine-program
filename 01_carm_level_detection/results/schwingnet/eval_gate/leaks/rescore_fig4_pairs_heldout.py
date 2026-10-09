#!/usr/bin/env python
"""EVAL_LEAKS rerun: the Figure S2a body-region R^2 (formerly Figure 4a) under the fold fit that HELD OUT each pair's
group, instead of under the median of all six fold fits.

WHY. SchwingNet/tools/fig4_pairs_pull.py scores every calibration pair under the card's fitted MEDIANS, the median over
six leave-one-group-out fits; each group was fitted by the five fits that did not hold it out, so every R^2 on Figure
S2a (the shown pair's and the device median) is in-sample for its subject (CHK-9 row card_median:<device>: SEEN). The
card records each fold's theta (docs/devices/<card>.json#physics_terms/folds[].theta, `held` = the group it left
out), so the held-out version is a forward pass per pair, no refit: pair -> its group -> the fold that held that group
out (md5 fold assignment exactly as device_fit.py when a device has more groups than --max-folds 6) -> R^2 under that
fold's theta, over the same body region (fit mask & water-equivalent path > 5 mm).

For Cios Fusion (groups = the six DeepFluoro specimens) and Elekta XVI (groups = COBRA cases, md5-folded) the
held-out fold did not fit the pair's subject: PATIENT-held-out. BV Pulsera is one phantom and PIXIUM 4600 one cadaver:
their held-out fold left out the pair's VIEW or FRAME group but fitted the same subject, so the number is within-subject
whatever fold is used; it is reported, and labelled so.

    python SchwingNet/results/eval_gate/leaks/rescore_fig4_pairs_heldout.py --out <json>      # grid (pairs on /rs, ~)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "SchwingNet" / "tools"))
import device_fit as DF  # noqa: E402
import device_style as DS  # noqa: E402
import eval_gate as EG  # noqa: E402
import fig4_pairs_pull as FP  # noqa: E402

PATIENT_GROUPS = {"cios_fusion": True, "elekta_xvi": True, "bv_pulsera": False, "pixium_4600": False}


def pct(xs, q):
    xs = [x for x in xs if x is not None and np.isfinite(x)]
    return float(np.percentile(xs, q)) if xs else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-folds", type=int, default=6)
    ap.add_argument("--chosen", default=str(REPO / "SchwingNet" / "results" / "fig4_pairs" / "fig4_pairs.json"))
    a = ap.parse_args()
    RP = DS.rp_tables()
    chosen = json.load(open(a.chosen)).get("devices", {}) if Path(a.chosen).exists() else {}
    res = dict(what=__doc__.split("\n")[0], region="body: fit mask & water-equivalent path > 5 mm", devices={})
    for name in FP.CARDS:
        t0 = time.time()
        dev = DF.DEVICES[name]
        card = json.load(open(REPO / "docs" / "devices" / f"{name}.json"))
        med = {k: float(card["physics_terms"]["fitted"][k]["median"]) for k in DF.NAMES9}
        med.update(sigma_p=0.0, s_t=0.0, b4=0.0)
        theta_of = {}
        for f in card["physics_terms"]["folds"]:
            th = dict(f["theta"])
            for k in ("sigma_p", "s_t", "b4"):
                th.setdefault(k, 0.0)
            theta_of[f["held"]] = th
        frames = FP.load_pairs_with_paths(dev, name)
        # the fold group exactly as device_fit.load_frames forms it: the pair's spec, or its pid on a device whose one
        # subject is held out frame by frame (group_by_pid: PIXIUM 4600)
        for d in frames:
            d["grp"] = d["pid_"] if dev.get("group_by_pid") else d["spec"]
        groups = sorted({d["grp"] for d in frames})
        remap = len(groups) > a.max_folds
        fold_of = {g: (f"fold{int(hashlib.md5(g.encode()).hexdigest(), 16) % a.max_folds}" if remap else g) for g in groups}
        missing = sorted({fold_of[g] for g in groups} - set(theta_of))
        rows = []
        for d in frames:
            d["m_body"] = d["m"] & (d["water"] > FP.BODY_WATER_CM)
            fold = fold_of[d["grp"]]
            r = dict(pair=f"{d['case']}_{d['pid_']}", group=d["grp"], subject_spec=d["spec"], fold=fold)
            for tag, th in (("r2_median_theta", med), ("r2_heldout_fold", theta_of.get(fold))):
                if th is None or d["m_body"].sum() < 50:
                    r[tag] = None
                    continue
                sse, sst = DF.sse_sst(th, d, RP, mkey="m_body")
                r[tag] = float(1.0 - sse / sst) if sst > 0 else None
            rows.append(r)
        # the gate record for the held-out version: per fold, the subjects it scored against the subjects its fit saw
        hint, const = DF.SUBJECT_OF.get(name, (None, None))
        checks = []
        for fold in sorted({r["fold"] for r in rows}):
            held = sorted({r["subject_spec"] for r in rows if r["fold"] == fold})
            fitted = sorted({r["subject_spec"] for r in rows if r["fold"] != fold})
            ev = [const] if const else [dict(case=g, hint=hint) for g in held]
            seen = {const} if const else EG.key_items([dict(case=g, hint=hint) for g in fitted])[0]
            checks.append(EG.assess(ev, None, f"leaks/rescore_fig4_pairs_heldout.py {name} {fold}", eval_set=f"{name} {fold}",
                                    also_seen={f"fold fit that held out {fold}": seen}))
        blk = EG.block(checks)
        ch = chosen.get(name) or {}
        pick = next((r for r in rows if r["pair"] == f"{ch.get('case')}_{ch.get('pid')}"), None)
        med_all = pct([r["r2_median_theta"] for r in rows], 50)
        med_ho = pct([r["r2_heldout_fold"] for r in rows], 50)
        res["devices"][name] = dict(
            eval_gate=blk, patient_held_out=PATIENT_GROUPS[name] and blk["held_out"], n_pairs=len(rows), n_groups=len(groups),
            n_folds=len({r["fold"] for r in rows}), folds_without_theta=missing,
            device_median_r2_median_theta=med_all, device_median_r2_heldout_fold=med_ho,
            p10_heldout_fold=pct([r["r2_heldout_fold"] for r in rows], 10), p90_heldout_fold=pct([r["r2_heldout_fold"] for r in rows], 90),
            shown_pair=dict(pair=pick["pair"] if pick else None, as_drawn=ch.get("r2_chosen"),
                            r2_median_theta=pick and pick["r2_median_theta"], r2_heldout_fold=pick and pick["r2_heldout_fold"],
                            fold=pick and pick["fold"]),
            as_drawn_device_median=ch.get("r2_median"), seconds=round(time.time() - t0, 1), rows=rows)
        print(f"{name}: {len(rows)} pairs, {len(groups)} groups -> {res['devices'][name]['n_folds']} folds; device median body R2 "
              f"{med_all} (median theta) -> {med_ho} (held-out fold); missing fold thetas {missing}; shown pair {ch.get('case')}_{ch.get('pid')} "
              f"{pick and pick['r2_median_theta']} -> {pick and pick['r2_heldout_fold']}; gate held_out {blk['held_out']} "
              f"overlap {blk['overlap']}; {time.time() - t0:.0f} s", flush=True)
    json.dump(res, open(a.out, "w"), indent=1, default=float)
    print("FIG4_PAIRS_HELDOUT_DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
