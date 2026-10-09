# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/leak_effect.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""How much did the training leak inflate the sweep numbers?

The clean way to ask is inside a single run: the same code, the same seed, the same RNG stream, split only
by whether each spine was in the namer's train split. Comparing the old arm against a fresh held-out arm
would confound the leak with run-to-run variation, which at n=120 is worth about two points of chain
completion on its own.

Accuracy is pooled per vertebra named, not per frame, and the interval is a cluster bootstrap over spines
because the frames of one spine are not independent.

    python tools/leak_effect.py --sweep ~/model_night/sweep2 --bank ~/allspine_v3_fov96_ctx \
        --arms ctsp_ii9_o2_gt films_ii9_o2_gt verse_ii9_o1_gt
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

ROUTES = [("single_frame", "the frame on its own pixels"),
          ("sweep_morph", "shape only, on the sweep"),
          ("sweep_hybrid", "matched onto the sweep")]


def per_spine_counts(rec, k, route):
    """(correct, total) vertebra names for one spine at one frame length"""
    ok = tot = 0
    for q in rec.get("queries", []):
        if q.get("K") != k:
            continue
        gt = q.get("gt") or []
        pr = q.get(route) or []
        if len(gt) != len(pr):
            continue
        ok += sum(int(g == p) for g, p in zip(gt, pr))
        tot += len(gt)
    return ok, tot


def cluster_boot(pairs, iters=2000, seed=0):
    """resample SPINES, not frames"""
    if not pairs:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    a = np.array([p[0] for p in pairs], float); b = np.array([p[1] for p in pairs], float)
    n = len(a)
    out = []
    for _ in range(iters):
        i = rng.integers(0, n, n)
        t = b[i].sum()
        if t:
            out.append(a[i].sum() / t)
    if not out:
        return (float("nan"), float("nan"))
    return (float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", required=True)
    ap.add_argument("--bank", required=True)
    ap.add_argument("--arms", nargs="+", required=True)
    ap.add_argument("--out", default="~/model_night/leak_effect.json")
    a = ap.parse_args()

    z = np.load(Path(os.path.expanduser(a.bank)) / "rung_1.npz", allow_pickle=True)
    c = np.array([str(x) for x in z["case"]]); s = np.array([str(x) for x in z["split"]])
    train = set(c[s == "train"].tolist())
    print(f"bank {Path(a.bank).name}: {len(train):,} case ids in the train split\n")

    rep = {}
    for arm in a.arms:
        p = Path(os.path.expanduser(a.sweep)) / arm / "sweep.json"
        if not p.exists():
            print(f"{arm}: absent"); continue
        recs = [r for r in json.load(open(p))["records"] if "skipped" not in r]
        seen = [r for r in recs if str(r["case"]) in train]
        held = [r for r in recs if str(r["case"]) not in train]
        print("=" * 84)
        print(f"{arm}:  {len(seen)} spines the namer was trained on, {len(held)} it was not")
        if not held or not seen:
            print("  one side is empty; nothing to compare\n"); continue

        ks = sorted({q.get("K") for r in recs for q in r.get("queries", []) if q.get("K")})
        ent = {"n_trained_on": len(seen), "n_held_out": len(held), "rows": {}}
        print(f"  {'route':<30} {'K':>2}  {'trained on':>22}  {'held out':>22}  {'gap':>7}")
        for route, lbl in ROUTES:
            for k in ks:
                ps_ = [per_spine_counts(r, k, route) for r in seen]
                ph_ = [per_spine_counts(r, k, route) for r in held]
                ps_ = [x for x in ps_ if x[1]]; ph_ = [x for x in ph_ if x[1]]
                if not ps_ or not ph_:
                    continue
                vs = sum(x[0] for x in ps_) / sum(x[1] for x in ps_)
                vh = sum(x[0] for x in ph_) / sum(x[1] for x in ph_)
                los, his = cluster_boot(ps_); loh, hih = cluster_boot(ph_)
                print(f"  {lbl:<30} {k:>2}  {100*vs:6.2f}% [{100*los:5.1f},{100*his:5.1f}]  "
                      f"{100*vh:6.2f}% [{100*loh:5.1f},{100*hih:5.1f}]  {100*(vs-vh):+6.2f}")
                ent["rows"][f"{route}_K{k}"] = {
                    "trained_on": {"p": round(vs, 4), "ci95": [round(los, 4), round(his, 4)],
                                   "spines": len(ps_), "names": sum(x[1] for x in ps_)},
                    "held_out": {"p": round(vh, 4), "ci95": [round(loh, 4), round(hih, 4)],
                                 "spines": len(ph_), "names": sum(x[1] for x in ph_)},
                    "gap": round(vs - vh, 4)}
        # and the registration step on its own
        for k in ks:
            f = lambda R: (sum(int(bool(q.get("mapped_right"))) for r in R for q in r.get("queries", []) if q.get("K") == k),
                           sum(1 for r in R for q in r.get("queries", []) if q.get("K") == k))
            ks_, ns_ = f(seen); kh_, nh_ = f(held)
            if ns_ and nh_:
                print(f"  {'frame placed at the right node':<30} {k:>2}  {100*ks_/ns_:6.2f}%"
                      f"{'':17}{100*kh_/nh_:6.2f}%{'':17}{100*(ks_/ns_ - kh_/nh_):+6.2f}")
                ent["rows"][f"mapped_right_K{k}"] = {"trained_on": {"p": round(ks_ / ns_, 4), "n": ns_},
                                                     "held_out": {"p": round(kh_ / nh_, 4), "n": nh_},
                                                     "gap": round(ks_ / ns_ - kh_ / nh_, 4)}
        rep[arm] = ent
        print()

    out = Path(os.path.expanduser(a.out)); out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(rep, open(out, "w"), indent=1)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
