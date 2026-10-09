"""Re-derive the quoted cv_v9 cells from the raw per-fold score dumps and audit their eval_gate blocks (closure VERIFY.md).

    python verify_cv9.py     # writes verify_cv9_rederived.json beside this file
"""
import json, glob, os, collections
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw", "proto_v9init_prerepair")  # pulled 2026-09-24 15:32 EDT from grid /rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init_prerepair
CV9 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cv_v9")
out = {"cells": {}, "gate": {}, "keys": {}}
def cell(folds, view):
    k = n = 0; cases = set(); err_cases = set(); frames = 0
    for f in folds:
        d = json.load(open(f"{R}/{f}/det_score_kfull.json", encoding="utf-8"))
        for fr in d["frames"]:
            if fr["view"] != view: continue
            frames += 1
            for it in fr["items"]:
                n += 1; k += int(it["exact"]); cases.add(fr["case"])
                if not it["exact"]: err_cases.add(fr["case"])
    return dict(k=k, n=n, pct=round(100*k/n, 2), cases=len(cases), cases_with_error=len(err_cases), frames=frames)
cv = [f"cv_fold{i}" for i in range(5)]; day = [f"cvday_fold{i}" for i in range(3)]
out["cells"]["case_grouped_LAT_whole_frame"] = cell(cv, "LAT")
out["cells"]["case_grouped_AP_whole_frame"] = cell(cv, "AP")
out["cells"]["day_grouped_LAT_whole_frame"] = cell(day, "LAT")
out["cells"]["day_grouped_AP_whole_frame"] = cell(day, "AP")
# coupled at det74 from the five couple_all.json
cc = cnt = cls = ns = 0; frames = 0; cases = set()
for i in range(5):
    d = json.load(open(f"{CV9}/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold{i}/det/kfull/couple_c74/couple_all.json", encoding="utf-8"))
    for fr in d["frames"]:
        if not fr.get("anchor") or fr.get("n_scored_counted", 0) == 0: continue
        frames += 1; cases.add(fr["case"])
        ns += fr["n_scored_counted"]; cc += fr["coupled_correct"]; cnt += fr["count_correct"]; cls += fr["classifier_correct"]
out["cells"]["coupled_det74_anchored"] = dict(frames=frames, cases=len(cases), counted_bodies=ns, coupled=cc, count=cnt, classifier=cls,
                                              coupled_pct=round(100*cc/ns, 2), count_pct=round(100*cnt/ns, 2), classifier_pct=round(100*cls/ns, 2))
# gate blocks
per_fold = {}; sha_by_ck = collections.defaultdict(set); all_keys = {}
for f in cv + day:
    d = json.load(open(f"{R}/{f}/det_score_kfull.json", encoding="utf-8")); g = d["eval_gate"]
    pm = json.load(open(f"{R}/{f}/det/kfull/prototype_meta.json", encoding="utf-8"))
    chk = []
    for c in g["checks"]:
        sha_by_ck[os.path.basename(c["checkpoint"])].add(c["checkpoint_sha256"])
        chk.append(dict(checkpoint=os.path.basename(c["checkpoint"]), sha256_12=c["checkpoint_sha256"][:12], lineage_match=c["lineage_match"],
                        ancestors=[os.path.basename(a) for a in c["ancestors"]], n_items=c["n_items"], n_keys=c["n_keys"], keys_by_corpus=c["keys_by_corpus"],
                        n_unkeyed=c["n_unkeyed"], overlap=c["overlap"], unresolved=c["unresolved"], pose_donor_overlap=c["pose_donor_overlap"]))
    bound = dict(level_model=os.path.basename(pm["level_model"]), level_model_sha256_12=pm["level_model_sha256"][:12],
                 head=os.path.basename(pm.get("head", "")), detector_sha256_12=pm["detector_sha256"][:12])
    enc_chk = next(c for c in chk if c["checkpoint"] == bound["level_model"])
    frames_cases = sorted({fr["case"] for fr in d["frames"]})
    all_keys[f] = frames_cases
    per_fold[f] = dict(gate_version=g["gate_version"], held_out=g["held_out"], not_held_out_reason=g["not_held_out_reason"], n_checks=g["n_checks"],
                       overlap=g["overlap"], unresolved=g["unresolved"], carried_from=os.path.basename(os.path.dirname(g["carried_from"])),
                       level_model_sha_equals_check_sha=(enc_chk["sha256_12"] == bound["level_model_sha256_12"]),
                       bound=bound, checks=chk, n_cases_scored=len(frames_cases), n_keys_in_checks=sorted({c["n_keys"] for c in chk}))
out["gate"] = per_fold
out["gate_summary"] = dict(
    shared_checkpoints_one_sha_each={k: (len(v) == 1) for k, v in sha_by_ck.items()},
    encoder_ancestor_is_v9_everywhere=all(any(c["checkpoint"].startswith("model_rung_1_ft_") and c["ancestors"] == ["model_rung_1_aug2.pt"] for c in pf["checks"]) for pf in per_fold.values()),
    head_ancestors_are_encoder_then_v9=all(any(c["checkpoint"].startswith("head_") and len(c["ancestors"]) == 2 and c["ancestors"][1] == "model_rung_1_aug2.pt" for c in pf["checks"]) for pf in per_fold.values()),
    all_held_out=all(pf["held_out"] and pf["overlap"] == 0 and pf["unresolved"] == 0 for pf in per_fold.values()),
    all_bound=all(pf["level_model_sha_equals_check_sha"] for pf in per_fold.values()),
)
cvk = [set(all_keys[f]) for f in cv]; dayk = [set(all_keys[f]) for f in day]
out["keys"] = dict(case_folds_sizes=[len(s) for s in cvk], case_folds_disjoint=all(not (a & b) for i, a in enumerate(cvk) for b in cvk[i+1:]),
                   case_folds_union=len(set.union(*cvk)), day_folds_sizes=[len(s) for s in dayk], day_folds_disjoint=all(not (a & b) for i, a in enumerate(dayk) for b in dayk[i+1:]),
                   day_folds_union=len(set.union(*dayk)), union_equal=(set.union(*cvk) == set.union(*dayk)))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_cv9_rederived.json"), "w"), indent=1)
print(json.dumps(out["cells"], indent=1)); print(json.dumps(out["gate_summary"], indent=1)); print(json.dumps(out["keys"], indent=1))
for f, pf in per_fold.items():
    print(f, pf["gate_version"], "held_out", pf["held_out"], "checks", pf["n_checks"], "overlap", pf["overlap"], "unres", pf["unresolved"], "bound", pf["level_model_sha_equals_check_sha"], pf["bound"]["level_model"], pf["bound"]["level_model_sha256_12"], "keys", pf["n_keys_in_checks"], "cases scored", pf["n_cases_scored"])
