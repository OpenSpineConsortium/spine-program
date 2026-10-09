# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/pool_variant_cv.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Pool the cross-validated variant sweeps into one held-out number per spine class.

Each fold contributes the patients its own encoder never saw, so pooling over folds scores every variant
patient exactly once, held out. Two things the pooling must respect and a naive concatenation would not.

One patient contributes several renders and several projections, and those are not independent samples; a
patient with eight oblique projections would otherwise count eight times and narrow the interval by a
factor it has not earned. So accuracy is pooled per vertebra named, and the interval is a bootstrap over
PATIENTS, resampling every projection of a patient together.

And a fold that produced no encoder contributes nothing rather than silently shrinking the denominator, so
a partial run reads as partial instead of as a smaller clean result.

    python tools/pool_variant_cv.py --sweep ~/model_night/sweep_variantcv --folds ~/model_night/folds --k 3
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

import numpy as np


def patient_of(case: str) -> str:
    s = str(case)
    for _ in range(3):
        s = re.sub(r"_(p\d+|s\d+|obl\d*|ap|lat)$", "", s)
    return s


def boot_by_patient(per_patient, iters=4000, seed=0):
    """per_patient: {patient: [correct, total]}"""
    if not per_patient:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    a = np.array([v[0] for v in per_patient.values()], float)
    b = np.array([v[1] for v in per_patient.values()], float)
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
    ap.add_argument("--folds", required=True)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--ks", type=int, nargs="+", default=[2, 3, 4])
    ap.add_argument("--out", default="~/model_night/variant_cv.json")
    a = ap.parse_args()

    root = Path(os.path.expanduser(a.sweep))
    fdir = Path(os.path.expanduser(a.folds))

    seen_folds, records = [], []
    for k in range(a.k):
        got = False
        for d in sorted(root.glob(f"cv{k}_*")):
            p = d / "sweep.json"
            if not p.exists():
                continue
            S = json.load(open(p))
            cfg = S["summary"]["config"]
            if not cfg.get("held_out"):
                print(f"  {d.name}: NOT marked held out -- refusing to pool it"); continue
            for r in S["records"]:
                if "skipped" in r:
                    continue
                r["_fold"] = k
                r["_arm"] = d.name
                records.append(r)
            got = True
        if got:
            seen_folds.append(k)
        else:
            print(f"  fold {k}: no sweep output; it contributes nothing")
    if not records:
        print("nothing to pool"); return 1
    print(f"pooled folds {seen_folds} ({len(records)} spine-runs)\n")

    # how many distinct patients, by class
    by_class_pat = defaultdict(set)
    for r in records:
        by_class_pat[str(r["class"])].add(patient_of(r["case"]))

    rep = {"folds": seen_folds, "n_spine_runs": len(records), "by_class": {}}
    classes = sorted({str(r["class"]) for r in records})
    print(f"{'class':<15} {'patients':>9} {'runs':>6} {'chain':>8}  " +
          "  ".join(f"{'K'+str(k)+' alone':>12} {'K'+str(k)+' swept':>12}" for k in a.ks))
    for cl in classes + ["VARIANT (pooled)", "all"]:
        if cl == "VARIANT (pooled)":
            rs = [r for r in records if str(r["class"]) in ("lumbosacral", "thoracolumbar", "both")]
        elif cl == "all":
            rs = records
        else:
            rs = [r for r in records if str(r["class"]) == cl]
        if not rs:
            continue
        pats = {patient_of(r["case"]) for r in rs}
        ch = defaultdict(lambda: [0, 0])
        for r in rs:
            ok = (r["duplicates"] == 0 and r["missed"] == 0 and r["false_positive"] == 0 and r["conflict"] == 0)
            q = ch[patient_of(r["case"])]
            q[0] += int(ok); q[1] += 1
        chain = sum(v[0] for v in ch.values()) / max(1, sum(v[1] for v in ch.values()))
        cells, ent = [], {"patients": len(pats), "runs": len(rs), "chain_complete": round(chain, 4), "k": {}}
        for k in a.ks:
            for route in ("single_frame", "sweep_hybrid"):
                pp = defaultdict(lambda: [0, 0])
                for r in rs:
                    for q in r.get("queries", []):
                        if q.get("K") != k:
                            continue
                        gt, pr = q.get("gt") or [], q.get(route) or []
                        if len(gt) != len(pr):
                            continue
                        t = pp[patient_of(r["case"])]
                        t[0] += sum(int(x == y) for x, y in zip(gt, pr)); t[1] += len(gt)
                pp = {kk: v for kk, v in pp.items() if v[1]}
                if not pp:
                    cells.append(f"{'-':>12}"); continue
                v = sum(x[0] for x in pp.values()) / sum(x[1] for x in pp.values())
                lo, hi = boot_by_patient(pp)
                cells.append(f"{100*v:11.1f}%")
                ent["k"].setdefault(k, {})[route] = {"p": round(v, 4), "ci95": [round(lo, 4), round(hi, 4)],
                                                     "patients": len(pp)}
        print(f"{cl:<15} {len(pats):>9} {len(rs):>6} {100*chain:7.1f}%  " + "  ".join(cells))
        rep["by_class"][cl] = ent

    print("\nintervals are a bootstrap over PATIENTS, resampling every projection of a patient together")
    for cl in ("VARIANT (pooled)", "ordinary"):
        e = rep["by_class"].get(cl)
        if not e:
            continue
        print(f"\n  {cl}: {e['patients']} patients")
        for k in a.ks:
            kk = e["k"].get(k) or e["k"].get(str(k))
            if not kk:
                continue
            for route, lbl in (("single_frame", "alone"), ("sweep_hybrid", "swept")):
                if route in kk:
                    r = kk[route]
                    print(f"    K{k} {lbl:<6} {100*r['p']:6.2f}%  [{100*r['ci95'][0]:.1f}, {100*r['ci95'][1]:.1f}]")

    out = Path(os.path.expanduser(a.out)); out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(rep, open(out, "w"), indent=1)
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
