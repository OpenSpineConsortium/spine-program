"""The coupled cell (det74, whole frame) re-derived under tools/coupling_report.py cell()'s own rule; appends to verify_cv9_rederived.json.

    python verify_coupled.py   # after verify_cv9.py
"""
import json, os
CV9 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cv_v9")
frames = []
for i in range(5):
    d = json.load(open(f"{CV9}/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold{i}/det/kfull/couple_c74/couple_all.json", encoding="utf-8"))
    frames += d["frames"]
F = [f for f in frames if f.get("truth_source") == "labellers_agree"]
anch = [f for f in F if f["call"] not in ("no anchor", "no alphabet")]
bodies = [(f, b) for f in F for b in f["bodies"] if "truth" in b]
b_cnt = [(f, b) for f, b in bodies if b["ordinal"] is not None]
out = dict(frames_labellers_agree=len(F), cases=len({f["case"] for f in F}), frames_anchored=len(anch), cases_anchored=len({f["case"] for f in anch}),
           bodies_scored=len(bodies), bodies_counted=len(b_cnt), cases_counted=len({f["case"] for f, b in b_cnt}),
           coupled_exact_counted=sum(int(b["coupled_exact"]) for f, b in b_cnt), classifier_exact_counted=sum(int(b["classifier_exact"]) for f, b in b_cnt),
           count_exact_counted=sum(int(b.get("count_exact", b["count"] == b["truth"])) for f, b in b_cnt),
           truth_sources_all_frames={s: sum(1 for f in frames if f.get("truth_source") == s) for s in {f.get("truth_source") for f in frames}},
           rule="tools/coupling_report.py cell(): truth_source == labellers_agree; anchored = call not in (no anchor, no alphabet); counted = a truth-matched body with an ordinal")
out["coupled_pct"] = round(100 * out["coupled_exact_counted"] / out["bodies_counted"], 2)
out["classifier_pct"] = round(100 * out["classifier_exact_counted"] / out["bodies_counted"], 2)
out["count_pct"] = round(100 * out["count_exact_counted"] / out["bodies_counted"], 2)
print(json.dumps(out, indent=1))
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_cv9_rederived.json"); j = json.load(open(H)); j["cells"]["coupled_det74_counted_bodies_coupler_rule"] = out
json.dump(j, open(H, "w"), indent=1)
