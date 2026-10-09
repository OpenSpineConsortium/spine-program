#!/usr/bin/env python
"""EVAL_LEAKS U1 closure: every quoted C-ArmLSpine naming number, old (allspine_v2_r1-initialised, lineage unresolved)
beside new (allspine_v9-initialised, lineage complete), through one code path.

WHAT IS COMPARED. The shipped case-grouped five-fold CV (proto/cv_fold*), the shipped acquisition-day three-fold CV
(proto/cvday_fold*) and the shipped zero-shot run (proto/zeroshot2_*) against their re-runs with the fold encoders
fine-tuned from allspine_v9 (slurm/carmlspine_cv_v9init.sh, slurm/carmlspine_cv_day_v9init.sh: the SAME merged
training banks, the SAME fold directories, the same epochs, seeds and prototype defaults; only --init differs) and the
zero-shot allspine_v9 encoder on the same frames. Coupling is read from the coupling.json that
SchwingNet/tools/coupling_report.py writes over the re-run (collect_cv_v9.sh) beside the shipped
SchwingNet/results/coupling.json.

THE GATE. Every NEW input is read through tools/rigor_fixes.cv_items, i.e. tools/eval_gate.carry on every score file,
with no declaration: a refusal is written into the output, never skipped. Every OLD input is read under a declared
--not-held-out reason (the strict gate refuses them: allspine_v2_r1's training bank is deleted), ONLY so the quoted
values are reproduced from the same files by the same code and sit beside the replacement. The strict-gate refusal of
each old family is recorded first.

STATISTICS. Exactly the shipped estimators, imported, not copied: rigor_fixes.prop_ci (case-cluster bootstrap, 2,000
resamples, seed 0: percentile, BCa, Wilson on the Kish-effective n), rigor_fixes.cluster_level_wilson,
rigor_fixes.paired_ci (lateral minus AP), carmlspine_pool_scores.boot (the percentile interval the shipped pooled JSON
and a9 print), and a7's abstention rule and threshold sweep.

    python SchwingNet/results/eval_gate/closure/cv_v9/closure_cv_v9.py --out <dir>/cv_v9.json \
        --coupling-new <dir>/coupling/coupling.json          # grid, CPU job (collect_cv_v9.sh)
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402
import rigor_fixes as RF  # noqa: E402
from carmlspine_pool_scores import boot as pool_boot  # noqa: E402

RS = "/rs/rs_grp_oschome/go2432/data/carmlspine"
PROTO_OLD, PROTO_NEW, POST_NEW = f"{RS}/proto", f"{RS}/proto_v9init", f"{RS}/proto_post_v9init"
KS = ["full", "5", "4", "3", "2", "1"]
OLD_DECL = ("EVAL_LEAKS U1 closure: reproduction of the QUOTED allspine_v2_r1-initialised cells beside their "
            "allspine_v9-initialised replacement; the strict gate refuses these inputs (allspine_v2_r1's training bank "
            "is deleted, UnresolvedLineage), so they are read here only to show the old value from the same files")
CONTROL_DECL = None  # the control's score files carry their own declared block


def md5(p):
    try:
        return hashlib.md5(open(p, "rb").read()).hexdigest()
    except OSError:
        return None


def jl(p):
    return json.load(open(p, encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ reading
def read_family(proto, pattern, boxes, ks, declared=None):
    """{k: (items, frames, files)} plus the merged verdict of every file read. A refusal is returned, not raised."""
    RF._GATE["blocks"], RF._GATE["not_held_out"] = [], declared
    try:
        got = RF.cv_items(proto, pattern, boxes, ks=ks)
        err = None
    except EG.EvalGateError as e:
        got, err = None, f"{type(e).__name__}: {str(e)[:1200]}"
    finally:
        blocks, RF._GATE["blocks"], RF._GATE["not_held_out"] = RF._GATE["blocks"], [], None
    gate = EG.merge(blocks) if blocks else None
    return got, gate, err


def gate_summary(g):
    if not g:
        return None
    roles = collections.Counter()
    ck = set()
    for c in g.get("checks") or []:
        ck.add(c.get("checkpoint"))
        roles[str(c.get("where", "")).rsplit("[", 1)[-1].rstrip("]")] += 1
    return dict(held_out=g.get("held_out"), not_held_out_reason=(g.get("not_held_out_reason") or None),
                n_checks=g.get("n_checks"), overlap=g.get("overlap"), unresolved=g.get("unresolved"),
                checkpoints=sorted(x for x in ck if x), checks_by_role=dict(roles))


# ------------------------------------------------------------------------------------------------ one cell
def cell(items, frames):
    I = items
    if not I:
        return None
    r = RF.prop_ci(I, "case", "exact")
    out = dict(k=r["k"], n=r["n"], clusters=r["clusters"], point=r["point"], clusters_with_error=r["clusters_with_error"],
               percentile=r.get("percentile"), bca=r.get("bca"), wilson_effective_n=r.get("wilson_effective_n"),
               n_effective=r.get("n_effective"), design_effect=r.get("design_effect"), ceiling_regime=r.get("ceiling_regime"))
    e, lo, hi = pool_boot(I, "exact")
    out["pool_boot_percentile"] = [lo, hi]
    out["all_correct_cases"] = RF.cluster_level_wilson(I, "case", "exact")
    ans = [x for x in I if not x["abstain"]]
    a = RF.prop_ci([dict(case=x["case"], v=int(not x["abstain"])) for x in I], "case", "v")
    out["answered"] = dict(k=a["k"], n=a["n"], point=a["point"], percentile=a.get("percentile"), bca=a.get("bca"))
    if ans:
        ea = RF.prop_ci(ans, "case", "exact")
        out["exact_on_answered"] = dict(k=ea["k"], n=ea["n"], point=ea["point"], percentile=ea.get("percentile"), bca=ea.get("bca"))
    out["errors_among_abstained"] = sum(1 for x in I if x["abstain"] and not x["exact"])
    out["errors_total"] = sum(1 for x in I if not x["exact"])
    sw = {}
    for t in (0.9, 0.95):
        A = [x for x in I if not ((x["call"] != x["single"]) or (x["prob"] is None) or (float(x["prob"]) < t))]
        aa = RF.prop_ci([dict(case=x["case"], v=int(x in A)) for x in I], "case", "v")
        ea = RF.prop_ci(A, "case", "exact") if A else None
        sw[f"{t:.2f}"] = dict(answered=aa["point"], answered_k=aa["k"],
                              exact_on_answered=(ea["point"] if ea else None), exact_on_answered_k=(ea["k"] if ea else None),
                              exact_on_answered_n=(ea["n"] if ea else None), exact_on_answered_percentile=(ea.get("percentile") if ea else None))
    out["abstain_sweep"] = sw
    out["within1"] = float(np.mean([x["within1"] for x in I]))
    F = frames
    tn = sum(f["n_truth_named"] for f in F)
    mn = sum(f["matched_named"] for f in F)
    out["recall_named"] = dict(matched=mn, truth=tn, point=(mn / tn if tn else None))
    out["frames"] = len({f["stem"] for f in F})
    per = collections.defaultdict(list)
    for x in I:
        per[x["truth"]].append(x["exact"])
    out["per_level"] = {lv: dict(n=len(v), exact=round(float(np.mean(v)), 4)) for lv, v in sorted(per.items())}
    conf = collections.Counter((x["truth"], x["call"]) for x in I if not x["exact"])
    out["confusions"] = [f"{t}->{c} x{n}" for (t, c), n in conf.most_common(10)]
    return out


def family_cells(got, views=("LAT", "AP")):
    out = {}
    for k, (items, frames, files) in (got or {}).items():
        for v in views:
            I = [x for x in items if x["view"] == v]
            F = [f for f in frames if f["view"] == v]
            c = cell(I, F)
            if c:
                c["files"] = len(files)
                out[f"{v}/k{k}"] = c
    return out


def paired_lat_ap(got):
    items = got["full"][0]
    by = collections.defaultdict(dict)
    for x in items:
        by[(x["case"], x["truth"])][x["view"]] = x
    rows = [dict(case=c, level=l, lat=v["LAT"]["exact"], ap=v["AP"]["exact"]) for (c, l), v in by.items() if "LAT" in v and "AP" in v]
    r = RF.paired_ci(rows, "case", "lat", "ap")
    keep = ("n_items", "n_clusters", "p_a", "p_b", "diff_pp", "percentile_pp", "bca_pp", "clusters_favouring_a",
            "clusters_favouring_b", "cluster_sign_test_p", "mcnemar_exact_p", "p_boot", "discordant_a_only", "discordant_b_only")
    return {k: r.get(k) for k in keep}


def min_det_conf(proto, pattern, sub="det/kfull"):
    """the lowest det_conf of any vertebra the prototype boxed (NUMBERS L221: the detector operating point)."""
    lo = None
    for d in sorted(glob.glob(os.path.join(proto, pattern, sub))):
        for f in glob.glob(os.path.join(d, "*.json")):
            if f.endswith("prototype_meta.json"):
                continue
            try:
                r = jl(f)
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(r, dict):          # prototype_results.json is a list (the per-frame index), not a frame
                continue
            for v in r.get("vertebrae") or []:
                c = v.get("det_conf")
                if c is not None and (lo is None or c < lo):
                    lo = c
    return lo


# ------------------------------------------------------------------------------------------------ control
def control(shipped_dir, ctrl_root, ks=("full", "3")):
    """per-item identity between a shipped fold's score files and today's re-run of the shipped fold model."""
    out = {}
    for k in ks:
        a, b = os.path.join(shipped_dir, f"det_score_k{k}.json"), os.path.join(ctrl_root, f"det_score_k{k}.json")
        if not (os.path.exists(a) and os.path.exists(b)):
            out[f"k{k}"] = dict(status="MISSING", shipped=os.path.exists(a), rerun=os.path.exists(b))
            continue
        A, B = jl(a), jl(b)
        ia = {(r["stem"], x["truth"]): (x["call"], bool(x["exact"]), bool(x["abstain"])) for r in A["frames"] for x in r["items"]}
        ib = {(r["stem"], x["truth"]): (x["call"], bool(x["exact"]), bool(x["abstain"])) for r in B["frames"] for x in r["items"]}
        same = sum(1 for key in ia if ib.get(key) == ia[key])
        out[f"k{k}"] = dict(status="COMPARED", shipped_items=len(ia), rerun_items=len(ib), identical=same,
                            only_shipped=len(set(ia) - set(ib)), only_rerun=len(set(ib) - set(ia)),
                            reproduces=(same == len(ia) == len(ib)), rerun_gate=gate_summary(B.get("eval_gate")))
    return out


# ------------------------------------------------------------------------------------------------ coupling
def coupling_rows(cj):
    """the quoted coupling cells, read from one coupling.json."""
    if not cj:
        return None
    C = cj["cells"]
    V = cj.get("cells_with_veridah_l6", {})

    out = {}
    for lab in ("det74/kfull", "det/kfull", "oracle/k5", "oracle_ext/k5", "oracle/kfull"):
        c = C.get(lab)
        if not c:
            continue
        out[lab] = {k: c.get(k) for k in (
            "frames", "cases", "frames_anchored", "bodies_counted", "classifier_exact", "coupled_exact",
            "classifier_exact_counted", "count_exact_counted", "coupled_exact_counted", "coupled_minus_count_counted",
            "coupled_minus_classifier_anchored", "classifier_exact_anchored", "coupled_exact_anchored",
            "disagreement_bodies", "disagreement_frames", "when_agree", "when_disagree", "calls", "calls_anchored",
            "non_ordinary_calls")}
        out[lab]["flags"] = c.get("flags")
    for lab in ("det/kfull", "det74/kfull"):
        v = V.get(lab)
        if v:
            out[f"veridah_l6:{lab}"] = dict(per_level_L6=(v.get("per_level") or {}).get("L6"))
    l6 = [r for r in cj.get("l6_patients", []) if r["arm"] == "det74" and r["field"] == "full"]
    anch = [r for r in l6 if (r.get("anchor") or {}).get("box") is not None]
    out["l6_patients_det74_full"] = dict(frames=len(l6), anchored=len(anch), l6_calls=sum(1 for r in anch if r["call"] == "L6"),
                                         l6_calls_flagged=sum(1 for r in anch if r["call"] == "L6" and r.get("flag")),
                                         calls=[(r["case"], r["view"], r["call"], r.get("flag_reason")) for r in l6])
    c42 = [r for r in l6 if r["case"] == "case42" and r["view"] == "LAT"]
    if c42:
        r = c42[0]
        out["case42_LAT_det74"] = {k: r.get(k) for k in ("anchor", "classifier", "count", "coupled", "p_classifier", "candidates",
                                                        "margin", "margin_next", "tau", "call", "flag", "flag_reason",
                                                        "truth_veridah", "truth_ts_read")}
    out["unchanged_check"] = cj.get("unchanged_check")
    out["eval_gate"] = gate_summary(cj.get("eval_gate")) if cj.get("eval_gate") else "no eval_gate block (written before the gate)"
    return out


def figure4_d(post_root):
    """Figure 4d's rows from the det74 coupler record of case42_LAT, fold 2, exactly as figure4_frame.py draws them."""
    p = os.path.join(post_root, "cv_fold2", "det", "kfull", "couple_c74", "couple_all.json")
    if not os.path.exists(p):
        return dict(status="MISSING", file=p)
    d = jl(p)
    fr = [f for f in d["frames"] if f["stem"] == "case42_LAT"]
    if not fr:
        return dict(status="NO case42_LAT", file=p)
    f = fr[0]
    rows, n_named, n_off = [], 0, 0
    for b in f["bodies"]:
        shape = "none" if b["abstain"] and b["classifier"] == "sacrum" else b["classifier"]
        if shape != "none":
            n_named += 1
            n_off += int(b["count"] != shape)
        rows.append(dict(ordinal=b["ordinal"], shape=shape, count=b["count"], call=b["coupled"], p_classifier=b.get("p_classifier"),
                         truth=b.get("truth"), drawn=f"{b['ordinal']}: shape {shape}, count {b['count']}, call {b['coupled']}"))
    return dict(status="OK", file=p, anchor=f.get("anchor"), call=f.get("call"), margin=f.get("margin"),
                margin_next=f.get("margin_next"), candidates=f.get("candidates"), flag=f.get("flag"), flag_reason=f.get("flag_reason"),
                rows=rows, count_differs_from_shape=f"{n_off} of {n_named}")


def figure4_b(proto):
    p = os.path.join(proto, "cv_fold3", "det", "k3", "case11_LAT_k3_1.json")
    if not os.path.exists(p):
        return dict(status="MISSING", file=p)
    r = jl(p)
    rows = []
    for v in r.get("vertebrae") or []:
        rows.append(dict(level=v.get("level"), level_prob=v.get("level_prob"), abstain=v.get("abstain"), det_conf=v.get("det_conf"),
                         drawn=("none" if v.get("abstain") else f"{v.get('level')} {v.get('level_prob', 0):.2f}")))
    return dict(status="OK", file=p, rows=rows)


# ------------------------------------------------------------------------------------------------ main
# Two truths. PRE = the export as it was when every quoted number was scored (realxray/carmlspine_pre_repair_2026-09-23,
# mirrored by prerepair_fold_dirs.py): old and new differ by the initialisation alone, so these are the replacements.
# REP = the export as it stands today (rewritten 2026-09-23 04:49-05:28): reported beside, with the SHIPPED models
# re-run on it (declared controls) so the truth repair and the change of initialisation can be told apart.
TRUTHS = {
    "pre": dict(new=f"{RS}/proto_v9init_prerepair", post=f"{RS}/proto_post_v9init_prerepair",
                ctrl_case="control_shipped_case_fold*", ctrl_day="control_shipped_day_fold*"),
    "rep": dict(new=f"{RS}/proto_v9init", post=f"{RS}/proto_post_v9init",
                ctrl_case="control_shipped_repaired_case_fold*", ctrl_day="control_shipped_repaired_day_fold*"),
}


def pooled(got_det, got_or):
    """the drop-in twin of docs/carmlspine_cv5_mixed_2026-09-21.json (same field names, same estimator)."""
    out = {}
    for boxes, g in (("det", got_det), ("oracle", got_or)):
        for k, (items, frames, files) in (g or {}).items():
            for v in ("LAT", "AP"):
                I = [x for x in items if x["view"] == v]
                F = [f for f in frames if f["view"] == v]
                if not I:
                    continue
                e, lo, hi = pool_boot(I, "exact")
                ans = [x for x in I if not x["abstain"]]
                ea, alo, ahi = pool_boot(ans, "exact") if ans else (None, None, None)
                tn = sum(f["n_truth_named"] for f in F)
                mn = sum(f["matched_named"] for f in F)
                fe = [f for f in F if f["all_exact"] is not None]
                per = collections.defaultdict(list)
                for x in I:
                    per[x["truth"]].append(x["exact"])
                conf = collections.Counter((x["truth"], x["call"]) for x in I if not x["exact"])
                out[f"{boxes}/{v}/k{k}"] = dict(
                    cases=len({x["case"] for x in I}), vertebrae=len(I), recall_named=(mn / tn if tn else None),
                    exact=e, exact_ci=[lo, hi], within1=float(np.mean([x["within1"] for x in I])),
                    answered=len(ans) / len(I), exact_answered=ea, exact_answered_ci=[alo, ahi],
                    frame_exact=(float(np.mean([f["all_exact"] for f in fe])) if fe else None), frames=len(F),
                    per_level={lv: dict(n=len(vv), exact=round(float(np.mean(vv)), 3)) for lv, vv in sorted(per.items())},
                    confusions=[f"{t}->{c} x{n}" for (t, c), n in conf.most_common(8)])
    return out


def holm_with(ps, pz):
    q = dict(ps, zeroshot_lateral_vs_ap=pz)
    order = sorted(q, key=q.get)
    holm, run = {}, 0.0
    for i, kk in enumerate(order):
        run = max(run, min(1.0, (len(q) - i) * q[kk]))
        holm[kk] = run
    return holm["zeroshot_lateral_vs_ap"], q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--coupling-pre", required=True, help="coupling.json from coupling_report over the pre-repair re-run")
    ap.add_argument("--coupling-rep", required=True, help="coupling.json from coupling_report over the repaired-truth re-run")
    ap.add_argument("--coupling-old", default=str(REPO / "SchwingNet" / "results" / "coupling.json"))
    ap.add_argument("--a3", default=str(REPO / "SchwingNet" / "results" / "a3.json"))
    a = ap.parse_args()
    od = os.path.dirname(os.path.abspath(a.out))
    res = dict(written=time.strftime("%Y-%m-%d %H:%M"), host=os.uname().nodename if hasattr(os, "uname") else None,
               script=str(Path(__file__).relative_to(REPO)), proto_old=PROTO_OLD, truths=TRUTHS,
               declaration_for_old=OLD_DECL, families={}, strict_gate_on_old={}, zero_shot_paired={}, controls={},
               figure4={})
    fams = {"cv5_det": ("cv_fold*", "det", KS), "cv5_oracle": ("cv_fold*", "oracle", KS),
            "cvday_det": ("cvday_fold*", "det", KS)}

    # the shipped (old) cells: a declared read, and the strict gate's verdict on them
    for name, (pat, boxes, ks) in fams.items():
        go, gate_o, err_o = read_family(PROTO_OLD, pat, boxes, ks, declared=OLD_DECL)
        _, _, strict_err = read_family(PROTO_OLD, pat, boxes, ["full"])
        res["strict_gate_on_old"][name] = strict_err or "HELD OUT (unexpected: the old family passed the strict gate)"
        res["families"][f"old:{name}"] = dict(gate=gate_summary(gate_o), error=err_o, cells=family_cells(go))
    # the old zero-shot run has k = 1..5 cells too (a7's zeroshot2 arm); the new zero-shot k cells are written by
    # zs_v9_kfield.sh (job 40436982) beside the kfull cells of the v9init arrays
    g, gate, err = read_family(PROTO_OLD, "zeroshot2", "det", KS, declared=OLD_DECL)
    res["families"]["old:zeroshot2"] = dict(gate=gate_summary(gate), error=err, cells=family_cells(g),
                                            paired_lat_minus_ap=(paired_lat_ap(g) if g and g["full"][0] else None))
    _, _, strict_err = read_family(PROTO_OLD, "zeroshot2", "det", ["full"])
    res["strict_gate_on_old"]["zeroshot2"] = strict_err or "HELD OUT (unexpected)"
    # the existing lineage-complete zero-shot run (2026-09-23 00:34, before the repair: the shipped truth)
    g, gate, err = read_family(PROTO_OLD, "zeroshot_v9", "det", ["full"])
    res["families"]["pre:zeroshot_v9_existing"] = dict(gate=gate_summary(gate), error=err, cells=family_cells(g),
                                                       paired_lat_minus_ap=(paired_lat_ap(g) if g and g["full"][0] else None))

    for tr, T in TRUTHS.items():
        got_new = {}
        for name, (pat, boxes, ks) in fams.items():
            gn, gate_n, err_n = read_family(T["new"], pat, boxes, ks)
            got_new[name] = gn
            res["families"][f"{tr}:{name}"] = dict(gate=gate_summary(gate_n), error=err_n, cells=family_cells(gn))
        for zname in ("v9head", "v9nohead"):
            g, gate, err = read_family(T["new"], f"zs_fold*/{zname}", "det", (KS if zname == "v9head" else ["full"]))
            res["families"][f"{tr}:zs_{zname}"] = dict(gate=gate_summary(gate), error=err, cells=family_cells(g),
                                                       paired_lat_minus_ap=(paired_lat_ap(g) if g and g["full"][0] else None))
        # the shipped models re-run on this truth (declared controls; their own blocks say so)
        for cname, pat in (("case", T["ctrl_case"]), ("day", T["ctrl_day"])):
            g, gate, err = read_family(T["new"], pat, "det", KS, declared="control (declared in its own score files)")
            files = (g or {}).get("full", ([], [], []))[2]
            res["families"][f"{tr}:control_shipped_{cname}"] = dict(
                gate=gate_summary(gate), error=err, cells=family_cells(g),
                folds=sorted({os.path.basename(os.path.dirname(f)) for f in files}))
        json.dump(pooled(got_new["cv5_det"], got_new["cv5_oracle"]),
                  open(os.path.join(od, f"carmlspine_cv5_v9init_{tr}.json"), "w"), indent=1)
        gd_or, _, _ = read_family(T["new"], "cvday_fold*", "oracle", KS)
        json.dump(pooled(got_new["cvday_det"], gd_or), open(os.path.join(od, f"carmlspine_cvday_v9init_{tr}.json"), "w"),
                  indent=1)
        res[f"detector_min_det_conf_{tr}"] = dict(cv=min_det_conf(T["new"], "cv_fold*"),
                                                  zs_v9head=min_det_conf(T["new"], "zs_fold*/v9head"))
        res["figure4"][f"b_{tr}"] = figure4_b(T["new"])
        res["figure4"][f"d_{tr}"] = figure4_d(T["post"])
    res["detector_min_det_conf_old"] = min_det_conf(PROTO_OLD, "cv_fold*")
    res["figure4"]["b_old"] = figure4_b(PROTO_OLD)
    res["figure4"]["d_old"] = figure4_d(f"{RS}/proto_post")

    # verification: the shipped model on the pre-repair mirror, item for item against the shipped score files (at kfull
    # it must reproduce them; at k = 1..5 the regenerated crops may differ, and this measures by how much)
    for mode, pre, n in (("case", "cv_fold", 5), ("day", "cvday_fold", 3)):
        for K in range(n):
            res["controls"][f"pre_{mode}_fold{K}"] = control(
                os.path.join(PROTO_OLD, f"{pre}{K}"), os.path.join(TRUTHS["pre"]["new"], f"control_shipped_{mode}_fold{K}"), KS)
            res["controls"][f"rep_{mode}_fold{K}"] = control(
                os.path.join(PROTO_OLD, f"{pre}{K}"), os.path.join(TRUTHS["rep"]["new"], f"control_shipped_repaired_{mode}_fold{K}"), KS)

    # Holm across the four comparisons named before adjustment (a3.json#primary_with_holm), with ONLY the zero-shot
    # member replaced; two of the other three are LEAKED (EVAL_LEAKS L2, L6), so the step is reported, not certified
    try:
        ps = {k: v["p_exact"] for k, v in jl(a.a3)["primary_with_holm"].items()}
        for name in ("pre:zeroshot_v9_existing", "pre:zs_v9head", "pre:zs_v9nohead", "rep:zs_v9head", "rep:zs_v9nohead"):
            pz = (res["families"].get(name, {}).get("paired_lat_minus_ap") or {}).get("cluster_sign_test_p")
            if pz is not None:
                h, q = holm_with(ps, pz)
                res["zero_shot_paired"][name] = dict(
                    p_exact=pz, p_exact_holm=h, family=q,
                    family_note="render_vs_film_detector and card_vs_uncalibrated_physics are LEAKED (EVAL_LEAKS L2, L6)")
    except Exception as e:  # noqa: BLE001
        res["zero_shot_paired"]["error"] = f"{type(e).__name__}: {e}"

    res["coupling"] = {}
    for tag, p in (("old", a.coupling_old), ("pre", a.coupling_pre), ("rep", a.coupling_rep)):
        cj = jl(p) if os.path.exists(p) else None
        res["coupling"][tag] = dict(file=p, md5=md5(p), rows=coupling_rows(cj))

    json.dump(res, open(a.out, "w"), indent=1, default=RF._jsonable)
    print("wrote", a.out)
    for name, blk in res["families"].items():
        c = (blk.get("cells") or {}).get("LAT/kfull")
        gs = blk.get("gate") or {}
        print(f"{name:34s} held_out={gs.get('held_out')} overlap={gs.get('overlap')} unresolved={gs.get('unresolved')} "
              f"err={bool(blk.get('error'))} LAT/kfull "
              + (f"{c['k']}/{c['n']} = {100 * c['point']:.1f} % {c['percentile']}" if c else "-"))
    for k, v in res["controls"].items():
        print("control", k, {kk: (vv.get("reproduces"), vv.get("identical"), vv.get("shipped_items"), vv.get("rerun_items"))
                             for kk, vv in v.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


