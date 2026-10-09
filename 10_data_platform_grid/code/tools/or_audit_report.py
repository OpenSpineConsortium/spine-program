#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/or_audit_report.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Leakage and independence audit, part 3: the report (AUDIT.md) and the lineage figure from the audit JSONs.

    python tools/or_audit_report.py --dir <audit dir>   # reads splits.json, dupes.json, pose_qc.json
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

# lineage matrix: rows = data, columns = models; cells = one of the states below.
# Programmatic where a data.yaml exists (the rx_* runs); stated from the build logs and bank metas otherwise.
STATES = {"T": ("trained on", "#2a78d6"), "V": ("val / checkpoint selection", "#1baf7a"), "C": ("real pixels fitted the device terms", "#eb6834"),
          "P": ("poses only (geometry, no pixels)", "#eda100"), "E": ("evaluated on (test)", "#ffffff")}
ROWS = ["DeepFluoro 17-1882 frames", "DeepFluoro 17-1905 frames", "DeepFluoro 18-0725 frames", "DeepFluoro 18-1109 frames (TEST)",
        "DeepFluoro 18-2799 frames", "DeepFluoro 18-2800 frames", "DeepFluoro poses (all six)",
        "C-ArmLSpine train (105 cases)", "C-ArmLSpine val (15)", "C-ArmLSpine test (28, TEST)",
        "COBRA train (110)", "COBRA val (8)", "COBRA test (27, TEST)", "Geneva phantom (TEST)",
        "FluoroCap literature panels", "Plain films (BUU/CSXA/NHANES/Mendeley/AASCE)", "CT renders (CTSP/VerSe/TotalSeg subjects)"]


def rx_column(run):
    col = {}
    tr = run.get("train", []); va = run.get("val", [])
    m = {"carmlspine/images/train": "C-ArmLSpine train (105 cases)", "carmlspine/images/val": "C-ArmLSpine val (15)",
         "carmlspine/images/test": "C-ArmLSpine test (28, TEST)", "cobra_elekta/images/train": "COBRA train (110)",
         "cobra_elekta/images/val": "COBRA val (8)", "cobra_elekta/images/test": "COBRA test (27, TEST)",
         "carmlspine_multi/images/train": "C-ArmLSpine train (105 cases)", "carmlspine_multi/images/val": "C-ArmLSpine val (15)"}
    df = {"deepfluoro/images/train": ["DeepFluoro 17-1882 frames", "DeepFluoro 17-1905 frames", "DeepFluoro 18-2799 frames", "DeepFluoro 18-2800 frames"],
          "deepfluoro/images/val": ["DeepFluoro 18-0725 frames"], "deepfluoro/images/test": ["DeepFluoro 18-1109 frames (TEST)"]}
    for d in tr:
        for r in [m[d]] if d in m else df.get(d, []):
            col[r] = "T"
    for d in va:
        for r in [m[d]] if d in m else df.get(d, []):
            col.setdefault(r, "V")
    # initialised from the render-only detector: inherits its pose and calibration exposure
    if "anchor_none_v2_17-1882" in str(run.get("init", "")):
        col.setdefault("DeepFluoro poses (all six)", "P"); col.setdefault("CT renders (CTSP/VerSe/TotalSeg subjects)", "T")
        for s in ("17-1905", "18-0725", "18-1109", "18-2799", "18-2800"):
            col.setdefault(f"DeepFluoro {s} frames" + (" (TEST)" if s == "18-1109" else ""), "C")
    for k in run.get("scores", {}):
        ds, sp = k.split("/")
        key = {"carmlspine": "C-ArmLSpine", "cobra_elekta": "COBRA", "deepfluoro": "DeepFluoro"}[ds]
        for r in ROWS:
            if ds == "deepfluoro":
                if sp == "test" and "18-1109" in r:
                    col.setdefault(r, "E")
            elif r.startswith(key) and r.split(" ")[1].startswith(sp):
                col.setdefault(r, "E")
    return col


def lineage(A, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = {}
    rd = A["render_detector"]
    c = {"DeepFluoro poses (all six)": "P", "CT renders (CTSP/VerSe/TotalSeg subjects)": "T", "DeepFluoro 17-1882 frames": "E"}
    for s in rd["calibration"]["real_frames_that_fitted_theta"]:
        c[f"DeepFluoro {s} frames" + (" (TEST)" if s == "18-1109" else "")] = "C"
    cols["render-only detector\nanchor_none_v2_17-1882"] = c
    cols["film detector\nv5z (keypoints)"] = {"Plain films (BUU/CSXA/NHANES/Mendeley/AASCE)": "T"}
    for name, run in A["rx_runs"].items():
        cols[name.replace("_1024", "").replace("rx_", "") + "\n(box detector)"] = rx_column(run)
    cols["zero-shot level model\nallspine_v2_r1 / v7 bank"] = {"CT renders (CTSP/VerSe/TotalSeg subjects)": "T", "Plain films (BUU/CSXA/NHANES/Mendeley/AASCE)": "T",
                                                             "FluoroCap literature panels": "T", "C-ArmLSpine test (28, TEST)": "E", "DeepFluoro 18-1109 frames (TEST)": "E"}
    cols["fine-tuned level model\ncarm_mix"] = {"CT renders (CTSP/VerSe/TotalSeg subjects)": "T", "Plain films (BUU/CSXA/NHANES/Mendeley/AASCE)": "T",
                                             "FluoroCap literature panels": "T", "C-ArmLSpine train (105 cases)": "T", "C-ArmLSpine val (15)": "V",
                                             "C-ArmLSpine test (28, TEST)": "E"}
    cols["level model CV folds\ncarm_cvmix0-4"] = {"CT renders (CTSP/VerSe/TotalSeg subjects)": "T", "Plain films (BUU/CSXA/NHANES/Mendeley/AASCE)": "T",
                                                "FluoroCap literature panels": "T", "C-ArmLSpine train (105 cases)": "T", "C-ArmLSpine val (15)": "T",
                                                "C-ArmLSpine test (28, TEST)": "T"}
    names = list(cols)
    fig, ax = plt.subplots(figsize=(1.35 * len(names) + 4.5, 0.42 * len(ROWS) + 2.2))
    ax.set_facecolor("#fcfcfb")
    for j, nm in enumerate(names):
        for i, r in enumerate(ROWS):
            st = cols[nm].get(r)
            if st:
                ax.add_patch(plt.Rectangle((j + 0.05, i + 0.05), 0.9, 0.9, facecolor=STATES[st][1], edgecolor="#0b0b0b" if st == "E" else "none", linewidth=1.2))
                ax.text(j + 0.5, i + 0.5, st, ha="center", va="center", fontsize=9, color="#0b0b0b" if st in ("E", "P", "V") else "white", fontweight="bold")
            else:
                ax.add_patch(plt.Rectangle((j + 0.05, i + 0.05), 0.9, 0.9, facecolor="#ebebe8", edgecolor="none"))
    ax.set_xlim(0, len(names)); ax.set_ylim(len(ROWS), 0)
    ax.set_xticks([j + 0.5 for j in range(len(names))]); ax.set_xticklabels(names, fontsize=8)
    ax.set_yticks([i + 0.5 for i in range(len(ROWS))]); ax.set_yticklabels(ROWS, fontsize=8)
    ax.tick_params(length=0); ax.xaxis.set_ticks_position("top")
    for sp in ax.spines.values():
        sp.set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor=v[1], edgecolor="#0b0b0b" if k == "E" else "none", label=f"{k}: {v[0]}") for k, v in STATES.items()],
              loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3, fontsize=8, frameon=False)
    ax.set_title("What each model saw: real frames per device against every detector and level model", fontsize=10, pad=14)
    fig.tight_layout(); fig.savefig(path, dpi=160); plt.close(fig)
    # the CV column's "T" on the test split means: each fold's held-out cases sit in the OTHER folds' training banks; see AUDIT.md (f).


def loso_figure(A, path):
    """The clean per-specimen render-only sacrum recall as a curve against confidence, all seeds, beside the exposed number."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    L = A["render_detector"]["loso_evals"]
    specs = ["17-1882", "17-1905", "18-0725", "18-1109", "18-2799", "18-2800"]
    fig, ax = plt.subplots(figsize=(7, 4.2)); ax.set_facecolor("#fcfcfb")
    for k, s in enumerate(specs):
        for seed in ("", "_s1", "_s2"):
            e = L.get(s + seed)
            if not e:
                continue
            keys = sorted(e, key=float); xs = [float(c) for c in keys]; ys = [100 * e[c]["sacrum_recall"] for c in keys]
            lw = 2.4 if s == "18-1109" else 1.4
            ax.plot(xs, ys, marker="o", ms=4, lw=lw, color="#e34948" if s == "18-1109" else "#2a78d6", alpha=1.0 if seed == "" else 0.45,
                    label=(f"{s} held out" + (" (realxray TEST specimen)" if s == "18-1109" else "")) if seed == "" and s in ("18-1109", "17-1882") else None)
    pooled = A["rx_runs"].get("rx_pooled_1024", {}).get("scores", {}).get("deepfluoro/test", {}).get("sacrum_recall")
    if pooled is not None:
        ax.plot([0.25], [100 * pooled], marker="s", ms=9, color="#eb6834", ls="none", label="rx_pooled on 18-1109 (trained on the other five specimens; init exposed)")
    ax.set_xlabel("detector confidence threshold"); ax.set_ylabel("sacrum recall, %"); ax.set_ylim(0, 102); ax.grid(True, color="#e6e6e3")
    ax.set_title("Sacrum recall on DeepFluoro real frames: leave-one-specimen-out render-only arms (blue: other specimens)", fontsize=9)
    ax.legend(fontsize=8, frameon=False, loc="lower left")
    for sp in ax.spines.values():
        sp.set_visible(False)
    fig.tight_layout(); fig.savefig(path, dpi=160); plt.close(fig)


def md_table(rows, header):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); a = ap.parse_args()
    A = json.load(open(os.path.join(a.dir, "splits.json")))
    D = json.load(open(os.path.join(a.dir, "dupes.json"))) if os.path.exists(os.path.join(a.dir, "dupes.json")) else None
    Q = json.load(open(os.path.join(a.dir, "pose_qc.json"))) if os.path.exists(os.path.join(a.dir, "pose_qc.json")) else None
    lineage(A, os.path.join(a.dir, "lineage.png"))
    loso_figure(A, os.path.join(a.dir, "loso_sacrum_recall.png"))
    defects, L = [], []
    L.append(f"# Leakage and independence audit\n\nGenerated {A['generated']} by tools/or_audit_splits.py, or_audit_dupes.py, or_audit_report.py; "
             "pose offsets by tools/carmlspine_pose_qc.py. Every number below is a count read from disk on the grid; nothing was re-trained.\n")
    # (a)
    L.append("## (a) Split disjointness by case\n")
    rows = []
    for ds, d in A["datasets"].items():
        rows.append([ds, d["n_meta"], d["frames_per_split"], d["cases_per_split"], d["n_cross_split_case_overlap"], d["n_meta_split_disagrees"],
                     d["n_image_wrong_dir"], d["n_image_without_meta"], d["n_image_missing"], len(d["case_in_two_split_lists"])])
        if d["n_cross_split_case_overlap"] or d["n_meta_split_disagrees"] or d["n_image_wrong_dir"] or d["case_in_two_split_lists"]:
            defects.append(f"{ds}: split defect (overlap {d['n_cross_split_case_overlap']}, meta/splits disagreements {d['n_meta_split_disagrees']}, wrong dir {d['n_image_wrong_dir']})")
    L.append(md_table(rows, ["dataset", "metas", "frames/split", "cases/split", "cases in >1 split", "meta split != splits.json", "image in wrong split dir", "image without meta", "meta without image", "case listed twice"]))
    cd = A["carmlspine_derived"]
    L.append(f"\nC-ArmLSpine crops (carmlspine_crops/k1..k5): {cd['crops']['n']} crop metas, {cd['crops']['n_wrong_split']} in a split other than their case's. "
             f"carmlspine_multi: {json.dumps(cd['multi']['per_split'])}; {cd['multi']['n_wrong_split']} images in a split other than their case's; {cd['multi']['n_unparsed']} stems unparsed.")
    if cd["crops"]["n_wrong_split"] or cd["multi"]["n_wrong_split"]:
        defects.append("C-ArmLSpine crops/multi: crops outside their case's split")
    df = A["deepfluoro_specimens"]
    L.append(f"\nDeepFluoro: splits {json.dumps(df['splits'])}; frames per specimen per split {json.dumps(df['frames_per_specimen_per_split'])}; "
             f"test-specimen frames in train or val: **{df['n_leak']}**.")
    if df["n_leak"]:
        defects.append("DeepFluoro test specimen frames in train/val")
    # CV folds
    L.append("\n### C-ArmLSpine five-fold CV (rule md5(case) % 5 == k = test fold)\n")
    rows = []
    for k in range(5):
        f = A["cv_folds"][f"fold{k}"]
        b1 = f.get(f"carm_cv{k}_fov96_ctx") or {}; b2 = f.get(f"carm_cvmix{k}_fov96_ctx") or {}
        rows.append([k, f["n_fold_cases"], f["fold_view_cases"], f["fold_view_equals_rule"], f["drr_ann_patients"], f["drr_ann_splits"], len(f["drr_ann_in_fold_test"]),
                     f["n_drr_ann_split_rule_violations"], b1.get("n_real"), len(b1.get("real_patients_in_fold_test", [])), b2.get("n_real"), len(b2.get("real_patients_in_fold_test", [])),
                     b2.get("source_counts")])
        if f["drr_ann_in_fold_test"] or b1.get("real_patients_in_fold_test") or b2.get("real_patients_in_fold_test") or not f["fold_view_equals_rule"]:
            defects.append(f"CV fold {k}: test cases present in a training bank or fold view differs from rule")
    L.append(md_table(rows, ["fold", "test cases (rule)", "cases in fold view", "view == rule", "DRR-bank patients", "DRR-bank splits", "test cases in DRR bank", "ann split-rule violations",
                             "ctx bank real crops", "test cases in ctx bank", "mix bank real crops", "test cases in mix bank", "mix bank sources"]))
    cb = A["carm_banks"]
    L.append("\n### C-ArmLSpine fine-tune banks vs the fixed 28-case test split\n")
    rows = [[b, v and v["n"], v and v["n_real"], v and v["real_patients"], v and len(v["real_patients_in_fixed_test"]), v and v["real_split_by_patient"], v and v["source_counts"]] for b, v in cb.items()]
    L.append(md_table(rows, ["bank", "crops", "real crops", "real patients", "fixed-test patients present", "case split -> bank split", "sources"]))
    for b, v in cb.items():
        if v and v["real_patients_in_fixed_test"]:
            defects.append(f"{b}: fixed test cases present: {v['real_patients_in_fixed_test']}")
    # (b)
    L.append("\n## (b) Near-duplicate images across splits (NCC32 >= threshold; pairs re-scored at 64x64)\n")
    if D:
        rows = []
        for ds, w in D["within"].items():
            for cmp_, c in w["comparisons"].items():
                rows.append([ds, cmp_, c.get("n_a"), c.get("n_b"), c.get("n_pairs"), c.get("n_same_case"), c.get("n_cross_case"), c.get("cross_case_pairs_involving_cases"),
                             None if c.get("max_ncc32") is None else round(c["max_ncc32"], 3), c.get("n_ncc64_ge_thr"), c.get("nearest_hist")])
        L.append(md_table(rows, ["dataset", "A | B", "n A", "n B", "pairs >= thr", "same case", "cross case", "B cases involved", "max NCC32", "cross pairs with NCC64 >= thr (of top 40)", "nearest-neighbour hist (bins -1,.5,.8,.9,.95,.97,.98,.99,1)"]))
        L.append("\nSame-case pairs across splits are impossible when the split is by case; the 'same case' column must be 0. Cross-case pairs are two different "
                 "patients photographed alike; the contact sheets dupes_<dataset>_*.png show the strongest ones for the eye.\n")
        L.append("### Across corpora: every realxray frame against the film corpus, FluoroCap panels and yolo_v6f\n")
        rows = []
        for name, c in D["across"]["corpora"].items():
            rows.append([name, c.get("n"), c.get("n_pairs"), c.get("pairs_per_dataset_split"), c.get("n_ncc64_ge_thr"),
                         {k: f"med {v['median']:.2f} p90 {v['p90']:.2f} max {v['max']:.3f} (>=0.9: {v['n_ge_0_9']})" for k, v in (c.get("nearest_by_dataset") or {}).items()}])
        L.append(md_table(rows, ["external corpus", "images", "pairs >= thr", "per dataset/split", "NCC64 >= thr (of top 40)", "nearest external match per realxray dataset"]))
        for ds, w in D["within"].items():
            for cmp_, c in w["comparisons"].items():
                if c.get("n_same_case"):
                    defects.append(f"{ds} {cmp_}: {c['n_same_case']} same-case cross-split near-duplicates")
    else:
        L.append("dupes.json missing: the duplicate job did not finish.")
    # (c)
    rd = A["render_detector"]
    L.append("\n## (c) The render-only detector anchor_none_v2_17-1882: what it saw\n")
    L.append(f"- Training renders: {rd['train']['n']} (val {rd['val']['n']}) from {rd['train']['synthetic_subjects']} synthetic TotalSegmentator subjects; no real frame is in images/train or images/val.\n"
             f"- Renders per POSE specimen (train): {json.dumps(rd['train']['renders_per_pose_specimen'])}; distinct poses per specimen {json.dumps(rd['train']['distinct_poses_per_specimen'])}. "
             f"The held-out specimen is 17-1882; the realxray TEST specimen 18-1109 contributed {rd['train']['renders_per_pose_specimen'].get('18-1109', 0)} of {rd['train']['n']} training renders "
             f"({100 * rd['train']['renders_per_pose_specimen'].get('18-1109', 0) / max(rd['train']['n'], 1):.1f}%) through its poses.\n"
             f"- Calibration: fold held={rd['calibration']['held']}; the nine device terms were fitted on the REAL frames of {json.dumps(rd['calibration']['real_frames_that_fitted_theta'])} "
             f"= {rd['calibration']['n_real_frames_that_fitted_theta']} frames, which include all 104 real frames of 18-1109. Photon range under this fold: {json.dumps(rd.get('photons', {}).get('specimens'))}.\n"
             f"- Its real_test is 17-1882 ({rd['real_test']['n']} frames). Its eval on 18-1109 in the realxray layout is therefore NOT a held-out test of the render-only method: 18-1109's geometry and pixels shaped the training set.\n")
    L.append("Leave-one-specimen-out arms (anchor_none_v2_<spec>, the clean number for each specimen; sacrum recall % at conf 0.05 / 0.10 / 0.25 / 0.40):\n")
    rows = []
    for k, e in sorted(rd["loso_evals"].items()):
        rows.append([k] + [f"{100 * e[c]['sacrum_recall']:.1f}" for c in sorted(e, key=float)] + [e[sorted(e, key=float)[0]]["n"]])
    L.append(md_table(rows, ["arm", "0.05", "0.10", "0.25", "0.40", "n frames"]))
    pooled = A["rx_runs"].get("rx_pooled_1024", {}).get("scores", {}).get("deepfluoro/test", {})
    only = A["rx_runs"].get("rx_only_carmlspine_1024", {}).get("scores", {}).get("deepfluoro/test", {})
    L.append(f"\nFor comparison at conf 0.25 on 18-1109: rx_pooled_1024 (fine-tuned on the other five DeepFluoro specimens + C-ArmLSpine + COBRA, initialised from the exposed render detector) "
             f"sacrum recall {100 * pooled.get('sacrum_recall', float('nan')):.1f}%; rx_only_carmlspine_1024 (C-ArmLSpine frames only, same init) {100 * only.get('sacrum_recall', float('nan')):.1f}%.\n")
    defects.append("The '100% sacrum on DeepFluoro test' number is rx_pooled_1024, trained on five DeepFluoro specimens of the same C-arm and initialised from a render detector whose "
                   "training poses were 45% the test specimen's; it is not the render-only method, and not comparable with the manuscript's 76.9% LOSO figure")
    # (d)
    fd = A["film_detector"]
    L.append("\n## (d) The film keypoint detector v5z\n")
    L.append(f"- Registry: {json.dumps(fd['registry'])}\n- Weight mtimes: {json.dumps(fd['weights'])}\n- Dataset arrival on the grid: {json.dumps(fd['downloads'])}\n")
    rows = [[k, v.get("data_yaml_mtime"), v.get("source_prefix_counts"), v.get("n_stems_naming_a_test_dataset")] for k, v in fd["corpus"].items()]
    L.append(md_table(rows, ["corpus", "data.yaml mtime", "image stems by source prefix", "stems naming DeepFluoro/COBRA/C-ArmLSpine/Geneva"]))
    L.append("\nThe v5z run directory was not found under ~/spine-detector/runs; its corpus is inferred from the data.yaml chain of the same date (yolo_v4z = yolo_v3 + yolo_v4z) and is stated as unverified. "
             "Its weights predate every real-fluoroscopy download except the DeepFluoro archive, whose h5 arrived 2026-09-20; no corpus stem names any of the four datasets.\n")
    # (e)
    L.append("\n## (e) The whole-spine level bank (allspine_v7, superset of the deleted v2)\n")
    rows = [[b, v and v["n"], v and v["distinct_cases"], v and v["source_counts"], v and v["case_name_hits"], v and v.get("merged_from")] for b, v in A["allspine"].items()]
    L.append(md_table(rows, ["bank", "crops", "distinct cases", "source counts", "case names hitting deepfluoro/physics/carm/cobra/geneva", "merged from"]))
    # (f)
    L.append("\n## (f) The C-ArmLSpine fine-tuned level models\n\nSee the CV table in (a) and the bank table: the per-fold context banks hold no crop of their fold's test cases; carm_fov96_ctx and carm_mix hold no crop of the fixed 28 test cases.\n")
    # (g)
    L.append("\n## (g) Truth construction and pose quality\n")
    L.append("Truth boxes are TotalSegmentator + SPINEPS masks of the case's own CBCT projected through a pose registered to the frame (edge correlation, bounded around the device geometry). "
             "A wrong pose displaces or mis-sizes every truth BOX of that frame, so it can bias detection recall and IoU-matched naming scores in either direction; it cannot change a level NAME, "
             "which comes from the two labellers on the 3-D volume and is agreed independently of the frame. The name a counting method assigns is scored against that agreed name.\n")
    for ds, d in A["datasets"].items():
        L.append(f"- {ds} edge NCC from the metas: {json.dumps(d['edge_ncc'])}")
    if Q:
        L.append("\nDetector-vs-truth offset (tools/carmlspine_pose_qc.py; film detector boxes against projected truth boxes, name-free nearest pairing, in body heights):\n")
        rows = []
        for v in ("AP", "LAT"):
            Rr = [r for r in Q if r["view"] == v]
            if Rr:
                dy = np.array([r["dy_body"] for r in Rr]); dx = np.array([r["dx_body"] for r in Rr])
                rows.append([v, len(Rr), f"{np.median(dy):+.3f}", f"{np.percentile(dy, 25):+.2f}..{np.percentile(dy, 75):+.2f}", f"{np.median(dx):+.3f}",
                             int((np.abs(dy) > 0.25).sum()), int((np.abs(dy) > 0.4).sum()), f"{np.median([r['body_px'] for r in Rr]):.0f}"])
        L.append(md_table(rows, ["view", "frames", "median dy (bodies)", "IQR dy", "median dx (bodies)", "|dy| > 0.25", "|dy| > 0.4", "median body px"]))
    else:
        L.append("\npose_qc.json missing: the pose QC step did not run.")
    # lodo caution
    L.append("\n## Other observations\n")
    for name, run in A["rx_runs"].items():
        if name.startswith("rx_lodo"):
            L.append(f"- {name}: checkpoint selection (val) on {run.get('val')}: these are the TEST splits of the other devices, so this run's numbers on those splits are selection-biased; only its held-out device's numbers are clean.")
    L.append("\n## Defects found\n")
    L += [f"- {d}" for d in defects] if defects else ["- none beyond the observations above"]
    L.append("\n## Figures\n- lineage.png: which data touched which model.\n- loso_sacrum_recall.png: leave-one-specimen-out render-only sacrum recall as a curve against confidence.\n- dupes_*.png, xcorpus_*.png: near-duplicate contact sheets.\n")
    open(os.path.join(a.dir, "AUDIT.md"), "w").write("\n".join(L))
    json.dump(defects, open(os.path.join(a.dir, "defects.json"), "w"), indent=1)
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
