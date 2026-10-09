#!/usr/bin/env python
"""Two small readings over the v9-initialised C-ArmLSpine re-run (grid, CPU; no checkpoint is loaded).

(1) MATRIX. The count-versus-classifier matrix of NUMBERS.md "(d) matrix, rows classifier ... against columns count"
    (drawn nowhere since fig5_naming was retired; kept as a NUMBERS row), recomputed from the det74/kfull coupler
    records of the re-run exactly as SchwingNet/results/fig5_naming_data.json#d/matrix was built: frames with
    truth_source = labellers_agree, call != "no anchor", bodies with an ordinal.
(2) PAIRS. Zero-shot (allspine_v9 + its head, no C-ArmLSpine frame in training) against the fine-tuned fold models
    (case-grouped, day-grouped) on the SAME detected vertebrae (paired by case, frame stem and truth level), whole
    frame, lateral and AP: paired difference in percentage points, case-clustered bootstrap (2,000 resamples, seed 0,
    percentile), cases favouring each side, exact two-sided sign test. This is the number the accuracy-saturation
    reading needs (how much same-device fine-tuning adds once the lateral view is already near its ceiling, and
    whether it holds across acquisition days).

The gate: every score file read here was written by tools/carmlspine_eval.py behind level_prototype.py's gate and
carries its own eval_gate block; the block is read and reported (held_out, overlap, unresolved), not recomputed.

    python cv_v9_extras.py --truth pre --out cv_v9_extras_pre.json
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import math
import os

import numpy as np

RS = "/rs/rs_grp_oschome/go2432/data/carmlspine"
ROOTS = {"pre": (f"{RS}/proto_v9init_prerepair", f"{RS}/proto_post_v9init_prerepair"),
         "rep": (f"{RS}/proto_v9init", f"{RS}/proto_post_v9init")}
LEVELS = ["T12", "L1", "L2", "L3", "L4", "L5", "sacrum"]


def jl(p):
    return json.load(open(p, encoding="utf-8"))


def gate_of(obj):
    g = obj.get("eval_gate") or {}
    return dict(gate_version=g.get("gate_version"), held_out=g.get("held_out"), overlap=g.get("overlap"),
                unresolved=g.get("unresolved"), n_checks=g.get("n_checks"))


def matrix(post):
    rows = collections.Counter()
    n_frames = n_bodies = 0
    gates = []
    for K in range(5):
        p = os.path.join(post, f"cv_fold{K}", "det", "kfull", "couple_c74", "couple_all.json")
        d = jl(p)
        gates.append(dict(file=p, **gate_of(d)))
        for f in d["frames"]:
            if f.get("truth_source") != "labellers_agree" or f.get("call") == "no anchor":
                continue
            n_frames += 1
            for b in f["bodies"]:
                if b.get("ordinal") is None:
                    continue
                n_bodies += 1
                rows[(b["classifier"], b["count"])] += 1
    cls = sorted({a for a, _ in rows}, key=lambda x: (LEVELS.index(x) if x in LEVELS else 99, x))
    cnt = sorted({b for _, b in rows}, key=lambda x: (LEVELS.index(x) if x in LEVELS else 99, x))
    table = {c: {k: rows.get((c, k), 0) for k in cnt} for c in cls}
    diag = sum(v for (a, b), v in rows.items() if a == b)
    off = sorted(((a, b, v) for (a, b), v in rows.items() if a != b), key=lambda x: -x[2])
    return dict(frames_anchored_agreed=n_frames, bodies_counted=n_bodies, on_diagonal=diag,
                diagonal={c: rows.get((c, c), 0) for c in cls}, off_diagonal=[f"{a}->{b} {v}" for a, b, v in off],
                table=table, gates=gates)


def items_of(score_file, view):
    """{(case, stem, truth): (exact, abstain)} for one carmlspine_eval score file, one view."""
    d = jl(score_file)
    out = {}
    for fr in d["frames"]:
        if fr.get("view") != view:
            continue
        for it in fr["items"]:
            out[(fr["case"], fr["stem"], it["truth"])] = (int(bool(it["exact"])), int(bool(it["abstain"])))
    return out, gate_of(d)


def family(root, pattern, view):
    items, gates = {}, []
    for p in sorted(glob.glob(os.path.join(root, pattern))):
        it, g = items_of(p, view)
        gates.append(dict(file=p, **g))
        items.update(it)
    return items, gates


def paired(a, b, seed=0, n_boot=2000):
    """a, b: {(case, stem, truth): (exact, abstain)}; the paired difference a - b over the common keys."""
    keys = sorted(set(a) & set(b))
    by_case = collections.defaultdict(list)
    for k in keys:
        by_case[k[0]].append((a[k][0], b[k][0]))
    cases = sorted(by_case)
    pa = np.array([x for c in cases for x, _ in by_case[c]], float)
    pb = np.array([y for c in cases for _, y in by_case[c]], float)
    diff = float(pa.mean() - pb.mean()) * 100
    rng = np.random.default_rng(seed)
    arrs = {c: np.array(by_case[c], float) for c in cases}
    boots = []
    for _ in range(n_boot):
        pick = rng.choice(cases, size=len(cases), replace=True)
        m = np.concatenate([arrs[c] for c in pick])
        boots.append((m[:, 0].mean() - m[:, 1].mean()) * 100)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    fav_a = sum(1 for c in cases if sum(x for x, _ in by_case[c]) > sum(y for _, y in by_case[c]))
    fav_b = sum(1 for c in cases if sum(x for x, _ in by_case[c]) < sum(y for _, y in by_case[c]))
    n = fav_a + fav_b
    p_sign = (sum(math.comb(n, i) for i in range(0, min(fav_a, fav_b) + 1)) * 2 / 2 ** n) if n else None
    p_sign = min(1.0, p_sign) if p_sign is not None else None
    disc_a = sum(1 for k in keys if a[k][0] == 1 and b[k][0] == 0)
    disc_b = sum(1 for k in keys if a[k][0] == 0 and b[k][0] == 1)
    return dict(n_items=len(keys), n_cases=len(cases), p_a=float(pa.mean()), p_b=float(pb.mean()), k_a=int(pa.sum()),
                k_b=int(pb.sum()), diff_pp=diff, percentile_pp=[float(lo), float(hi)], cases_favouring_a=fav_a,
                cases_favouring_b=fav_b, cluster_sign_test_p=p_sign, discordant_a_only=disc_a, discordant_b_only=disc_b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--truth", choices=["pre", "rep"], default="pre")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    new, post = ROOTS[a.truth]
    res = dict(truth=a.truth, roots=dict(new=new, post=post))
    res["matrix_det74_kfull"] = matrix(post)
    res["pairs"] = {}
    for view in ("LAT", "AP"):
        zs, g_zs = family(new, "zs_fold*/v9head/det_score_kfull.json", view)
        zs0, g_zs0 = family(new, "zs_fold*/v9nohead/det_score_kfull.json", view)
        cv, g_cv = family(new, "cv_fold*/det_score_kfull.json", view)
        day, g_day = family(new, "cvday_fold*/det_score_kfull.json", view)
        res["pairs"][view] = {
            "n": dict(zeroshot_v9head=len(zs), zeroshot_v9nohead=len(zs0), cv5_case=len(cv), cvday=len(day)),
            "cv5_case minus zeroshot_v9head": paired(cv, zs),
            "cvday minus zeroshot_v9head": paired(day, zs),
            "cv5_case minus cvday": paired(cv, day),
            "zeroshot_v9head minus zeroshot_v9nohead": paired(zs, zs0),
            "gates": dict(zeroshot_v9head=g_zs, zeroshot_v9nohead=g_zs0, cv5_case=g_cv, cvday=g_day),
        }
    # the same pairing at every field size (zs_v9_kfield.sh scored zero-shot at k = 1..5 on the same crops)
    res["pairs_by_k"] = {}
    for view in ("LAT", "AP"):
        res["pairs_by_k"][view] = {}
        for k in ("1", "2", "3", "4", "5", "full"):
            zs, _ = family(new, f"zs_fold*/v9head/det_score_k{k}.json", view)
            cv, _ = family(new, f"cv_fold*/det_score_k{k}.json", view)
            day, _ = family(new, f"cvday_fold*/det_score_k{k}.json", view)
            if not (set(zs) & set(cv)):
                res["pairs_by_k"][view][f"k{k}"] = dict(status="no common items", n_zs=len(zs), n_cv=len(cv))
                continue
            res["pairs_by_k"][view][f"k{k}"] = {
                "cv5_case minus zeroshot_v9head": paired(cv, zs),
                "cvday minus zeroshot_v9head": paired(day, zs),
                "cv5_case minus cvday": paired(cv, day),
            }
    json.dump(res, open(a.out, "w"), indent=1)
    print("wrote", a.out)
    for view in ("LAT", "AP"):
        for k, blk in res["pairs_by_k"][view].items():
            v = blk.get("cv5_case minus zeroshot_v9head")
            if v:
                print(f"{view} {k} cv5 minus zs: {v['k_a']}/{v['n_items']} vs {v['k_b']}/{v['n_items']} = {v['diff_pp']:+.1f} pp "
                      f"[{v['percentile_pp'][0]:+.1f}, {v['percentile_pp'][1]:+.1f}] cases {v['cases_favouring_a']}:{v['cases_favouring_b']}")
    m = res["matrix_det74_kfull"]
    print("matrix det74/kfull:", m["frames_anchored_agreed"], "frames,", m["bodies_counted"], "bodies,", m["on_diagonal"],
          "on the diagonal;", m["off_diagonal"])
    for view in ("LAT", "AP"):
        for k, v in res["pairs"][view].items():
            if k in ("n", "gates"):
                continue
            print(f"{view} {k}: {v['k_a']}/{v['n_items']} vs {v['k_b']}/{v['n_items']} = {v['diff_pp']:+.1f} pp "
                  f"{v['percentile_pp']} cases {v['cases_favouring_a']}:{v['cases_favouring_b']} p={v['cluster_sign_test_p']}")
    bad = [g for view in res["pairs"] for fam in res["pairs"][view]["gates"].values() for g in fam if not g["held_out"]]
    bad += [g for g in m["gates"] if not g["held_out"]]
    print("files not held out:", len(bad))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
