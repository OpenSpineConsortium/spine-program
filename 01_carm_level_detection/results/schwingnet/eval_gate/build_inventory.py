#!/usr/bin/env python
"""Every evaluator and every quoted result, with the checkpoint lineage each one rests on.

Writes, beside itself:
  quoted_results.json   one row per number the manuscript quotes (SchwingNet/NUMBERS.md table rows, CLAIMS_LEDGER.md
                        rows that carry a number of ours, results/bodybox_rescore/rescore.json rows, and the entries of
                        figures/*.numbers.json and figures/*.record.json), each with the checkpoint(s) scored, the
                        evaluation set and the file that lists its items, the output file, and a verdict under the
                        held-out rule below
  EVALUATORS.md         only the blocks between <!-- BEGIN:GENERATED <name> --> and <!-- END:GENERATED <name> --> are
                        rewritten; the prose around them is hand-written and is not touched

THE RULE (Greg, 2026-09-23). An evaluation item is HELD OUT for a checkpoint only if its patient key (a render inherits
its source CT subject) is in NEITHER the train NOR the val/selection set of that checkpoint NOR of any ancestor in its
initialisation chain. Public ImageNet / COCO weights are the only exempt ancestor, and only when declared.

WHERE THE LINEAGE FACTS COME FROM. Nothing here reads a checkpoint. The facts in CHECKPOINTS were read on the grid on
2026-09-23 (args.yaml `model:` and `data:` of every run, data.yaml train/val of every run, the devcorpus list files,
prototype_meta.json of the C-ArmLSpine prototype runs, the registry ledger) and are written here with the file they
came from. A fact that could not be read is written as unknown and yields NOT ESTABLISHED, never a pass.

Tokens. A split is a set of tokens `<corpus>:<split>` (`carm:test`, `cobra:val`, `df:test` = specimen 18-1109, ...);
a TotalSegmentator subject is `ts:<sXXXX>`. Pose donors are tracked apart (`pose:carm:test`, `pose:cobra:test`,
`pose:df:18-1109`): a styled or anchor render is a TotalSegmentator subject ray-cast under the registered pose of a
real frame, so it carries the pose, not the patient. The rule as written is about patients, so a pose-donor overlap
does not change the verdict; it is reported in its own field because leak_check.py check (6) treats a pose donor as a
dependency and the coordinator may decide it should.

    python SchwingNet/results/eval_gate/build_inventory.py          # from the repo root; no grid access needed
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SN = REPO / "SchwingNet"
RS = "/rs/rs_grp_oschome/go2432/data"
HOMEG = "/wsu/home/go/go24/go2432"
RUNS = f"{HOMEG}/spine-detector/runs"
TS17 = ["s0585", "s0970", "s1045", "s1062", "s1159", "s1384", "s1535", "s1579", "s1700", "s1836", "s1842", "s1872",
        "s1880", "s1883", "s1902", "s2033", "s2053"]

# ------------------------------------------------------------------------------------------------ checkpoints
# train / val: token sets. pose: {token: count of renders} over train+val. parent: key or None.
CHECKPOINTS = {
    "coco_yolo11m": dict(
        label="yolo11m.pt (ultralytics COCO release)", public=True, parent=None, train=set(), val=set(), pose={},
        declared="args.yaml `model: yolo11m.pt` of every run that starts from it",
        evidence="args.yaml"),
    "imagenet": dict(
        label="torchvision ImageNet weights", public=True, parent=None, train=set(), val=set(), pose={},
        declared="fig_manifold.record.json deep.weights = IMAGENET1K_V2; for the level encoders the use of ImageNet is "
                 "NOT recorded (train_level_classifier uses them only when cached on the node, random init otherwise)",
        evidence="figures/fig_manifold.record.json; tools/train_level_classifier.py"),
    "anchor_none_v2_17-1882": dict(
        label="render-only detector (arm `render`; ancestor of every rx_* arm)",
        path=f"{RUNS}/pose/anchor_none_v2_17-1882/weights/best.pt", parent="coco_yolo11m",
        train={"ts:anchor_train", "ts:s0585", "ts:s0970", "ts:s1045", "ts:s1159", "ts:s1384"},
        val={"ts:anchor_val", "ts:s1062"},
        pose={"pose:df:18-1109": 294, "pose:df:17-1905": 64, "pose:df:18-0725": 58, "pose:df:18-2799": 120,
              "pose:df:18-2800": 117},
        selection="best.pt = best fitness on images/val (ultralytics)",
        lists=f"{HOMEG}/model_night/anchor_none_v2_17-1882/images/{{train,val}} (569 / 84 renders)",
        evidence="args.yaml (model yolo11m.pt, data model_night/anchor_none_v2_17-1882/data.yaml); image names read "
                 "2026-09-23: TotalSegmentator subjects, 14 renders each of s0585 s0970 s1045 s1159 s1384 in train and "
                 "of s1062 in val; pose donors in train 17-1905 53, 18-0725 53, 18-1109 255, 18-2799 102, 18-2800 106, "
                 "in val 11 / 5 / 39 / 18 / 11; 17-1882 is the held specimen (0)"),
    "rx_lodo_carmlspine_1024": dict(
        label="arm `lodo_carm` / `real_lodo`: real COBRA + DeepFluoro frames, C-ArmLSpine held out (the headline detector)",
        path=f"{RUNS}/realxray/rx_lodo_carmlspine_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"cobra:train", "cobra:val", "df:train", "df:val"}, val={"cobra:test", "df:test"}, pose={},
        selection="best.pt = best fitness on the COBRA and DeepFluoro TEST splits",
        lists=f"{RUNS}/realxray/rx_lodo_carmlspine_1024/data.yaml",
        evidence="args.yaml model = anchor_none_v2_17-1882/weights/best.pt; data.yaml train = cobra_elekta train+val, "
                 "deepfluoro train+val; val = cobra_elekta test, deepfluoro test"),
    "rx_lodo_cobra_elekta_1024": dict(
        label="arm `lodo_cobra`: real C-ArmLSpine + DeepFluoro frames, COBRA held out",
        path=f"{RUNS}/realxray/rx_lodo_cobra_elekta_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"carm:train", "carm:val", "df:train", "df:val"}, val={"carm:test", "df:test"}, pose={},
        selection="best.pt = best fitness on the C-ArmLSpine and DeepFluoro TEST splits",
        lists=f"{RUNS}/realxray/rx_lodo_cobra_elekta_1024/data.yaml", evidence="args.yaml; data.yaml"),
    "rx_lodo_deepfluoro_1024": dict(
        label="arm `lodo_df`: real C-ArmLSpine + COBRA frames, DeepFluoro held out",
        path=f"{RUNS}/realxray/rx_lodo_deepfluoro_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"carm:train", "carm:val", "cobra:train", "cobra:val"}, val={"carm:test", "cobra:test"}, pose={},
        selection="best.pt = best fitness on the C-ArmLSpine and COBRA TEST splits",
        lists=f"{RUNS}/realxray/rx_lodo_deepfluoro_1024/data.yaml", evidence="args.yaml; data.yaml"),
    "rx_pooled_1024": dict(
        label="arm `pooled` (same-device control, 'pooled real'): real train frames of all three devices",
        path=f"{RUNS}/realxray/rx_pooled_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"carm:train", "cobra:train", "df:train"}, val={"carm:val", "cobra:val", "df:val"}, pose={},
        selection="best.pt = best fitness on the three val splits",
        lists=f"{RUNS}/realxray/rx_pooled_1024/data.yaml", evidence="args.yaml; data.yaml"),
    "rx_only_carmlspine_1024": dict(
        label="arm `only_carm` ('only C-ArmLSpine'): C-ArmLSpine real train frames",
        path=f"{RUNS}/realxray/rx_only_carmlspine_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"carm:train"}, val={"carm:val"}, pose={}, selection="best.pt on carmlspine val",
        lists=f"{RUNS}/realxray/rx_only_carmlspine_1024/data.yaml",
        evidence="args.yaml (init anchor_none_v2_17-1882, NOT COCO as results/lcurve/lcurve.json describes it); data.yaml"),
    "rx_only_carmlspine_multi_1024": dict(
        label="arm `only_carm_multi`: C-ArmLSpine train frames + crops",
        path=f"{RUNS}/realxray/rx_only_carmlspine_multi_1024/weights/best.pt", parent="anchor_none_v2_17-1882",
        train={"carm:train"}, val={"carm:val"}, pose={}, selection="best.pt on carmlspine_multi val",
        lists=f"{RUNS}/realxray/rx_only_carmlspine_multi_1024/data.yaml", evidence="args.yaml; data.yaml"),
    "detector_v5z_final": dict(
        label="film keypoint detector (boxes for the C-ArmLSpine naming runs; film side of the render-vs-film comparison)",
        path=f"{HOMEG}/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt", parent=None, parent_unknown=True,
        train={"films:v5z_unrecorded"}, val={"films:v5z_unrecorded"}, pose={},
        selection="not recorded",
        lists="NOT RECORDED: registry entry 2026-09-15 has bank ''",
        evidence="registry.jsonl (sha 797de71a..., bank ''); file written 2026-09-14 09:33, before C-ArmLSpine landed on "
                 "the grid (fetch job 40409970, log closed 2026-09-21 17:44; even the archive's internal file times, "
                 "2026-09-15 16:55, are later), so it cannot hold a C-ArmLSpine frame; its film "
                 "train/val lists are not recorded anywhere read here"),
    "anchor_det_v1": dict(
        label="render-trained detector (render side of the render-vs-film comparison)",
        path=f"{HOMEG}/FluoroCap/anchor_det_v1.pt", parent=None, parent_unknown=True,
        train={"ctsp:anchor_drr"}, val={"ctsp:anchor_drr"}, pose={},
        selection="not recorded", lists="~/anchor_drr (registry BACKFILL bank)",
        evidence="tools/model_registry.py BACKFILL (bank ~/anchor_drr: CTSpinoPelvic1K renders); written 2026-09-14"),
    "allspine_v2_r1": dict(
        label="level encoder allspine_v2 rung 1 (zero-shot C-ArmLSpine arm; init of every C-ArmLSpine fold model)",
        path=f"{HOMEG}/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt", parent="imagenet", parent_unknown=True,
        train={"allspine_v2:train"}, val={"allspine_v2:val"}, pose={},
        selection="best epoch on allspine_v2 val exact (train_level_classifier best_state)",
        lists="~/allspine_v2_fov96_ctx/rung_1.npz (DELETED 2026-09-20)",
        evidence="registry.jsonl 2026-09-15 (sha 00e84a90...); predates C-ArmLSpine on the grid; bank deleted so its "
                 "lists survive only in logs; whether ImageNet init was used is not recorded"),
    "carm_cv_fold_models": dict(
        label="C-ArmLSpine five-fold models: model_rung_1_ft_cv{K}_aug2.pt + head_cv{K}.pt (per fold K)",
        path=f"{HOMEG}/carm_cvmix{{K}}_fov96_ctx/runs/model_rung_1_ft_cv{{K}}_aug2.pt; {HOMEG}/model_night/heads_carm/head_cv{{K}}.pt",
        parent="allspine_v2_r1",
        train={"carm:not_scored_fold", "allspine_v7:train_sample"}, val={"carm:not_scored_fold", "allspine_v7:sample"},
        pose={}, selection="encoder: best epoch on the fold bank's val (--val-frac 0.2 of the non-test folds' crops); "
                           "head: final epoch",
        lists=f"{HOMEG}/carm_cv{{K}}_fov96_ctx and carm_cvmix{{K}}_fov96_ctx rung_1.npz (case/split arrays); fold "
              f"membership {RS}/realxray/carmlspine_cv/fold{{K}}",
        evidence="slurm/carmlspine_cv.sh (INIT=resolve('allspine_v2_r1'); carmlspine_to_bank --fold K excludes the "
                 "scored fold; merge over allspine_v7 rung_1); atlas/model.json Limitations (7): '0 test cases in any "
                 "fold's DRR, crop or mixed bank'"),
    "carm_cvday_fold_models": dict(
        label="C-ArmLSpine acquisition-day three-fold models (same recipe, folds by DICOM StudyDate)",
        # the weights, as tools/checkpoint_lineage.py found them (touched.json): the fold encoder and the fold head
        path=f"{HOMEG}/carm_cvdaymix{{K}}_fov96_ctx/runs/model_rung_1_ft_cvday{{K}}_aug2.pt; "
             f"{HOMEG}/model_night/heads_carm/head_cvday{{K}}.pt", parent="allspine_v2_r1",
        train={"carm:not_scored_fold", "allspine_v7:train_sample"}, val={"carm:not_scored_fold"}, pose={},
        selection="as the case folds", lists="results/carmlspine_day_groups.json; slurm/carmlspine_cv_day.sh",
        evidence="slurm/carmlspine_cv_day.sh; rigor_fixes a9"),
    "allspine_v8_encoder": dict(
        label="level encoder allspine_v8 rung 1 (the film-naming numbers)",
        path=f"{HOMEG}/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt", parent="imagenet", parent_unknown=True,
        train={"v8:train"}, val={"v8:val"}, pose={},
        selection="best epoch of 40 on allspine_v8 VAL exact (train_level_classifier best_state)",
        lists=f"{HOMEG}/allspine_v8_fov96_ctx/rung_1.npz arrays case/split/source",
        evidence="slurm/allspine_v8_train.sh (no --init); tools/train_level_classifier.py lines 410-472 (best_state on val)"),
    "allspine_v8_head_seed0": dict(
        label="mixed-length run head on the v8 encoder (seed 0)",
        path=f"{HOMEG}/model_night/heads_mixed/head_allspine_v8_mixed_kmax4_seed0.pt", parent="allspine_v8_encoder",
        train={"v8:train"}, val=set(), pose={}, selection="final epoch (no selection on val)",
        lists=f"{HOMEG}/allspine_v8_fov96_ctx/rung_1.npz split == train",
        evidence="tools/head_mixed_length.py (torch.save after the last epoch)"),
    "allspine_v9_encoder": dict(
        label="level encoder allspine_v9 rung 1 (Figure 2: embedding, silhouettes, occlusion, never-seen L6)",
        path=f"{HOMEG}/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt", parent="imagenet",
        train={"v9:train"}, val={"v9:val"}, pose={},
        selection="best epoch on allspine_v9 VAL exact (train_level_classifier best_state); figure2_metrics.json "
                  "gate_verdict_validation_split: 'NOT HELD OUT (selection split)'",
        lists=f"{HOMEG}/allspine_v9_fov96_ctx/rung_1.npz arrays case/split/source",
        evidence="results/figure2/figure2_metrics.json encoder + encoder_sha256 188f9fcb...; touched.json row (no parent, "
                 "no carmlspine key in train or val)"),
    "dc_P_pooled": dict(
        label="design P pooled detector (styled renders of every card + real train frames of every device)",
        path=f"{RUNS}/devcorpus/dc_P_pooled/weights/best.pt", parent="coco_yolo11m",
        train={"ts:train125", "carm:train", "cobra:train", "df:train"},
        val={"ts:val17", *(f"ts:{s}" for s in TS17), "carm:val", "cobra:val", "df:val"},
        pose={"pose:carm:test": 658, "pose:cobra:test": 412, "pose:df:18-1109": 2634},
        selection="best.pt on P_pooled/val.txt (1,752 styled renders of the 17 TotalSegmentator val subjects + 246 real val frames)",
        lists=f"{RS}/devcorpus/lists/P_pooled/{{train,val}}.txt",
        evidence="args.yaml (yolo11m.pt, 60 epochs); list files counted 2026-09-23 (0 real test frames in train or val; "
                 "case134 absent: 0 lines)"),
}


def _dc(name, design, held, train_devs, pose, extra=""):
    real_tr = {f"{d}:train" for d in train_devs}
    real_va = {f"{d}:val" for d in train_devs}
    CHECKPOINTS[name] = dict(
        label=f"devcorpus design {design}, held {held}{extra}", path=f"{RUNS}/devcorpus/{name}/weights/best.pt",
        parent="coco_yolo11m", train={"ts:train125", *real_tr}, val={"ts:val17", *(f"ts:{s}" for s in TS17), *real_va},
        pose=pose, selection=f"best.pt on lists/{name[3:]}/val.txt (17 TotalSegmentator val subjects' styled renders + "
                              f"real val frames of the training devices)",
        lists=f"{RS}/devcorpus/lists/{name[3:]}/{{train,val}}.txt",
        evidence="args.yaml (yolo11m.pt); list files counted 2026-09-23")


DEV = {"surgio_b51_dr": "carm", "elekta_xvi": "cobra", "cios_fusion": "df"}
# pose-donor counts over train+val, read from the list files (pose_donor_counts below)
POSE_A_FULL = {"pose:df:18-1109": 1756}
POSE_A_1DEV = {"pose:df:18-1109": 878}
for held in DEV:
    others = [DEV[d] for d in DEV if d != held]
    for sfx in ("", "_s1"):
        _dc(f"dc_A_held_{held}{sfx}", "A", held, others, POSE_A_FULL, " (every card under the Cios Fusion / DeepFluoro pose pool)")
    for one in DEV:
        if one != held:
            _dc(f"dc_A_held_{held}_1dev_{one}", "A", held, [DEV[one]], POSE_A_1DEV, f", one source device {one}")
_dc("dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238", "A", "surgio_b51_dr", ["cobra"], POSE_A_1DEV,
    ", Elekta real frames cut to 240 (10 patients)")
_dc("dc_B_held_surgio_b51_dr", "B", "surgio_b51_dr", ["cobra", "df"], {"pose:cobra:test": 412, "pose:df:18-1109": 878})
_dc("dc_B_held_surgio_b51_dr_s1", "B", "surgio_b51_dr", ["cobra", "df"], {"pose:cobra:test": 412, "pose:df:18-1109": 878})
_dc("dc_B_held_elekta_xvi", "B", "elekta_xvi", ["carm", "df"], {"pose:carm:test": 658, "pose:df:18-1109": 878})
_dc("dc_B_held_cios_fusion", "B", "cios_fusion", ["carm", "cobra"], {"pose:carm:test": 658, "pose:cobra:test": 412})
_dc("dc_B_held_cios_fusion_s1", "B", "cios_fusion", ["carm", "cobra"], {"pose:carm:test": 658, "pose:cobra:test": 412})

# learning-curve fine-tunes: styled renders of EVERY card (7,322) + N real frames of the target + the others' real frames
LC_PARENT = {"surgio_b51_dr": "dc_B_held_surgio_b51_dr_s1", "elekta_xvi": "dc_B_held_elekta_xvi",
             "cios_fusion": "dc_B_held_cios_fusion"}
for dev, par in LC_PARENT.items():
    t = DEV[dev]
    CHECKPOINTS[f"lc_{dev}"] = dict(
        label=f"learning-curve fine-tune lc_{dev}_N<k>_s<seed>", path=f"{RUNS}/lcurve/lc_{dev}_N<k>_s<seed>/weights/best.pt",
        parent=par, train={"ts:train125", f"{t}:train(N frames)", *(f"{DEV[d]}:train" for d in DEV if d != dev)},
        val={f"{t}:val"}, pose={"pose:carm:test": 598, "pose:cobra:test": 368, "pose:df:18-1109": 762},
        selection=f"best.pt on the target device's real val split (lists/lcurve_{dev}_N*/val.txt)",
        lists=f"{RS}/devcorpus/lists/lcurve_{dev}_N<k>_s<seed>/{{train,val}}.txt",
        evidence="args.yaml of lc_* runs (model = parent best.pt); list files counted 2026-09-23 (7,322 styled in train "
                 "incl. the target device's card)")

CARDS = {
    "cios_fusion": dict(group="specimen (six DeepFluoro cadavers)", patient_heldout=True),
    "elekta_xvi": dict(group="case (COBRA patients, md5-folded into six)", patient_heldout=True),
    "bv_pulsera": dict(group="view (ONE Geneva phantom, 19 poses)", patient_heldout=False),
    "pixium_4600": dict(group="frame by pose id (ONE Ljubljana cadaver, 18 radiographs)", patient_heldout=False),
}

# ------------------------------------------------------------------------------------------------ evaluation sets
EVALSETS = {
    "carm_test": dict(desc="C-ArmLSpine test: 28 cases, 56 frames (287 vertebrae, 56 sacra)", tokens={"carm:test"},
                      pose="pose:carm:test", items=f"{RS}/realxray/carmlspine/splits.json#test (local copy SchwingNet/results/inputs/splits.json); images/test",
                      unit="case (an acquisition session; person identity not established)"),
    "carm_k": dict(desc="C-ArmLSpine test cut to k vertebrae (k1/k3 crops)", tokens={"carm:test"}, pose="pose:carm:test",
                   items=f"{RS}/realxray/carmlspine_crops/k{{1,3}}/test", unit="case"),
    "cobra_test": dict(desc="COBRA2026 Elekta test: 27 patients, 648 frames (893 vertebrae, 609 sacra)", tokens={"cobra:test"},
                       pose="pose:cobra:test", items=f"{RS}/realxray/cobra_elekta/splits.json#test", unit="patient"),
    "df_test": dict(desc="DeepFluoro test specimen 18-1109: 104 frames (83 vertebrae, 90 sacra), one cluster", tokens={"df:test"},
                    pose="pose:df:18-1109", items=f"{RS}/realxray/deepfluoro/splits.json#test", unit="specimen"),
    "df_all6": dict(desc="DeepFluoro all six specimens, 366 frames", tokens={"df:train", "df:val", "df:test"},
                    pose="pose:df:18-1109", items=f"{RS}/realxray/deepfluoro/splits.json (train+val+test)", unit="specimen"),
    "geneva_all": dict(desc="Geneva hip phantom, 116 frames, one phantom", tokens={"geneva:all"}, pose=None,
                       items=f"{RS}/realxray/geneva_hip", unit="phantom"),
    "carm_cv": dict(desc="C-ArmLSpine five case-grouped folds, every case scored by the fold model that excluded it",
                    tokens={"carm:scored_fold"}, pose=None, items=f"{RS}/realxray/carmlspine_cv/fold{{0..4}} "
                    "(tools/carmlspine_fold_dirs.py); per-fold scores carmlspine/proto/cv_fold*/{det,oracle}_score_k*.json",
                    unit="case"),
    "carm_cvday": dict(desc="C-ArmLSpine three acquisition-day folds", tokens={"carm:scored_fold"}, pose=None,
                       items="SchwingNet/results/carmlspine_day_groups.json; carmlspine/proto/cvday_fold*", unit="acquisition day"),
    "carm_all148": dict(desc="C-ArmLSpine all 148 built cases (train + val + test of the realxray split)",
                        tokens={"carm:train", "carm:val", "carm:test"}, pose=None,
                        items=f"{RS}/carmlspine/proto/zeroshot2_{{det,oracle}}_{{train,val,test}}/score_k*.json", unit="case"),
    "v8_val": dict(desc="allspine_v8 VALIDATION films of CSXA / BUU-LSPINE / NHANES II (2,890 films of all sources)",
                   tokens={"v8:val"}, pose=None, items=f"{HOMEG}/allspine_v8_fov96_ctx/rung_1.npz split == 'val'; rows in "
                   "SchwingNet/results/a5_rows.csv", unit="patient"),
    "nhanes25": dict(desc="25 NHANES II spines, 233 truth bodies (films_drr_buucorr, first 25 annotated spines with a sacrum)",
                     tokens={"nhanes:a3_25"}, pose=None, items="SchwingNet/results/a3a_rows.csv (column spine); "
                     f"{HOMEG}/films_drr_buucorr/ann", unit="spine / patient"),
    "arc17": dict(desc="angle-sweep set: 17 TotalSegmentator subjects x 19 lat x 3 tilt x 2 cards",
                  tokens={"ts:val17", *(f"ts:{s}" for s in TS17)}, pose=None,
                  items=f"{RS}/devcorpus_arc/anglesweep/SET_INFO.json#subjects", unit="subject"),
    "case134_spin": dict(desc="case134 real 301-frame CBCT spin (one patient)", tokens={"carm:case134"}, pose=None,
                         items=f"{RS}/realxray/carmlspine_sweep", unit="one patient"),
    "v9_val_clean": dict(desc="allspine_v9 VALIDATION crops after dropping persons whose key is in the v9 train keys "
                              "(13,009 crops of 1,612 persons; Figure 2)", tokens={"v9:val"}, pose=None,
                         items=f"{HOMEG}/allspine_v9_fov96_ctx/rung_1.npz split == 'val' minus the train split's keys "
                               "(results/figure2/figure2_metrics.json#cleaning)", unit="person"),
    "v9_val": dict(desc="allspine_v9 VALIDATION split (the encoder's selection split), every person", tokens={"v9:val"},
                   pose=None, items=f"{HOMEG}/allspine_v9_fov96_ctx/rung_1.npz split == 'val'", unit="person"),
    "carm_l6_never_seen": dict(desc="three C-ArmLSpine patients read L6 by one labeller (case42, case121, case136): CBCT "
                                    "renders under six device cards, 180 L6 crops", tokens={"carm:l6_three"}, pose=None,
                               items="SchwingNet/results/figure2/figure2_metrics.json#heldout_gate_check/patients",
                               unit="patient (case)"),
}
# case134: the two spot frames were added to realxray/carmlspine/images/train at 2026-09-23 05:28; every detector scored
# on the spin was trained before that (dc_P_pooled best.pt 01:46; P_pooled lists hold 0 case134 lines).

# ------------------------------------------------------------------------------------------------ verdicts
def chain(ck):
    out, k = [], ck
    while k:
        out.append(k)
        k = CHECKPOINTS[k].get("parent")
    return out


def verdict(ck, es):
    """(verdict, why, pose) for one checkpoint on one evaluation set."""
    if ck not in CHECKPOINTS:
        return "NOT ESTABLISHED", f"checkpoint {ck} has no lineage entry", []
    E = EVALSETS[es]["tokens"]
    whys, unknown, pose = [], [], []
    for c in chain(ck):
        C = CHECKPOINTS[c]
        if C.get("public"):
            continue
        tr, va = C.get("train", set()), C.get("val", set())
        if es in ("carm_cv", "carm_cvday") and c in ("carm_cv_fold_models", "carm_cvday_fold_models"):
            pass                                   # the scored fold is excluded by construction (carmlspine_to_bank --fold K)
        else:
            if E & tr:
                whys.append(f"{sorted(E & tr)} in the TRAIN set of {c}" + ("" if c == ck else " (ancestor)"))
            if E & va:
                whys.append(f"{sorted(E & va)} in the VAL/selection set of {c}" + ("" if c == ck else " (ancestor)"))
        if C.get("parent_unknown"):
            unknown.append(f"{c}: initialisation not recorded")
        pt = EVALSETS[es].get("pose")
        if pt:
            for k, n in C.get("pose", {}).items():
                if k == pt or (es == "df_all6" and k.startswith("pose:df:")):
                    pose.append(f"{n} renders in {c} train+val carry the pose of {k.split(':', 1)[1]}")
    if whys:
        return "NOT HELD OUT", "; ".join(whys), pose
    if es == "nhanes25" and ck == "detector_v5z_final":
        # 2026-09-23 EVAL_LEAKS: the 196 was counted against the allspine_v7 level bank, not the detector's lists. Its
        # own lists (touched.json: data/yolo_v3 + yolo_v4z images/{train,val}, read on the grid) hold 24 of the 25 spines.
        return "NOT HELD OUT", ("in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own "
                                "train (22) or val (2) directories and those of its parent detect_v3 (touched.json); "
                                "the 196 printed before was counted against the allspine_v7 level bank, the wrong list"), pose
    return "HELD OUT", ("no evaluation token in the train or val set of the checkpoint or its ancestors"
                        + (f"; {'; '.join(unknown)} (a public-weights assumption)" if unknown else "")), pose


def combine(pairs):
    """pairs: [(ck, es)] -> row-level verdict fields."""
    if not pairs:
        return dict(verdict="N/A", why="no checkpoint: a count, a parameter value, arithmetic or a published number",
                    per_pair=[], pose_donor=[])
    per, vs, pose = [], set(), []
    for ck, es in pairs:
        v, why, p = verdict(ck, es)
        per.append(dict(checkpoint=ck, eval_set=es, verdict=v, why=why, pose_donor=p))
        vs.add(v)
        pose += [f"{ck} on {es}: {x}" for x in p]
    v = vs.pop() if len(vs) == 1 else "MIXED"
    return dict(verdict=v, why="; ".join(f"{d['checkpoint']} on {d['eval_set']}: {d['verdict']}"
                                         + (f" ({d['why']})" if d["verdict"] != "HELD OUT" else "") for d in per),
                per_pair=per, pose_donor=pose)


# ------------------------------------------------------------------------------------------------ families
ARM_CK = {"render": "anchor_none_v2_17-1882", "lodo_carm": "rx_lodo_carmlspine_1024", "real_lodo": "rx_lodo_carmlspine_1024",
          "lodo_cobra": "rx_lodo_cobra_elekta_1024", "lodo_df": "rx_lodo_deepfluoro_1024", "pooled": "rx_pooled_1024",
          "only_carm": "rx_only_carmlspine_1024", "only_carm_multi": "rx_only_carmlspine_multi_1024"}
SWEEP_SET = {"carm_test": "carm_test", "carm_k1": "carm_k", "carm_k3": "carm_k", "cobra_test": "cobra_test",
             "cobra_test_v3": "cobra_test", "df_test": "df_test", "geneva_all": "geneva_all", "df_all6": "df_all6"}

FAMILIES = {
    "lodo_detector_on_carm": dict(
        label="held-out detector on C-ArmLSpine test (a1)",
        chain="tools/or_recall_curves.py sweep -> tools/realxray_eval.py --dump-raw -> or_ready/lodo/sweeps/lodo_carm__carm_test.json "
              "-> tools/rigor_fixes.py a1 (bootstrap)",
        output="SchwingNet/results/a1.json", pairs=[("rx_lodo_carmlspine_1024", "carm_test")]),
    "pooled_vs_lodo_carm": dict(
        label="same-device control vs held-out detector, paired, C-ArmLSpine test (a3)",
        chain="or_ready/lodo/sweeps/{pooled,lodo_carm}__carm_test.json -> tools/rigor_fixes.py a3",
        output="SchwingNet/results/a3.json#comparisons/pooled_vs_heldout_detector",
        pairs=[("rx_pooled_1024", "carm_test"), ("rx_lodo_carmlspine_1024", "carm_test")]),
    "render_vs_film": dict(
        label="render-trained vs film-trained detector on 25 NHANES spines (a3)",
        chain="tools/rigor_fixes.py a3a-rows (runs both YOLO detectors itself) -> a3a_rows.csv -> rigor_fixes a3",
        output="SchwingNet/results/a3.json#comparisons/render_vs_film_detector; a3a_rows.csv",
        pairs=[("anchor_det_v1", "nhanes25"), ("detector_v5z_final", "nhanes25")]),
    "carm_cv_naming": dict(
        label="C-ArmLSpine naming, case-grouped five-fold CV (a4/a7/a9)",
        chain="slurm/carmlspine_cv.sh: tools/level_prototype.py (fold encoder + head + detector_v5z_final boxes) -> "
              "tools/carmlspine_eval.py score -> carmlspine/proto/cv_fold*/det_score_k*.json -> tools/rigor_fixes.py a4/a7/a9",
        output="SchwingNet/results/a4.json, a7.json, a9.json",
        pairs=[("carm_cv_fold_models", "carm_cv"), ("detector_v5z_final", "carm_cv")]),
    "carm_cvday_naming": dict(
        label="C-ArmLSpine naming, acquisition-day three-fold CV (a9)",
        chain="slurm/carmlspine_cv_day.sh (same chain) -> carmlspine/proto/cvday_fold*/det_score_k*.json -> rigor_fixes a9",
        output="SchwingNet/results/a9.json#cv/cvday_acquisition_day_folds",
        pairs=[("carm_cvday_fold_models", "carm_cvday"), ("detector_v5z_final", "carm_cvday")]),
    "carm_cv_oracle": dict(
        label="C-ArmLSpine naming with truth boxes (no detector)",
        chain="slurm/carmlspine_cv.sh oracle branch -> carmlspine_eval score",
        output="docs/carmlspine_cv5_mixed_2026-09-21.json oracle/*", pairs=[("carm_cv_fold_models", "carm_cv")]),
    "carm_zeroshot": dict(
        label="C-ArmLSpine naming, no C-ArmLSpine frame in training (zeroshot2)",
        chain="slurm/carmlspine_proto.sh TAG=zeroshot2 -> tools/level_prototype.py (defaults: detector_v5z_final, "
              "allspine_v2_r1, no head; prototype_meta.json records both sha256) -> carmlspine_eval score -> rigor_fixes a7 / a3",
        output="SchwingNet/results/a7.json#cells/zeroshot2~1*, a3.json#comparisons/zeroshot_lateral_vs_ap",
        pairs=[("allspine_v2_r1", "carm_all148"), ("detector_v5z_final", "carm_all148")]),
    "film_naming_v8": dict(
        label="plain-film naming on the allspine_v8 validation films (a5)",
        chain="slurm/allspine_v8_train.sh -> tools/head_mixed_length.py (scores the val films) ; tools/rigor_fixes.py "
              "a5-rows (re-scores the val films, one row per vertebra) -> rigor_fixes a5",
        output="SchwingNet/results/a5.json; a5_rows.csv; a5_rows_meta.json",
        pairs=[("allspine_v8_encoder", "v8_val"), ("allspine_v8_head_seed0", "v8_val")]),
    "counting": dict(
        label="counting from the detected sacrum (count_from_sacrum_eval)",
        chain="or_ready/lodo/sweeps/<arm>__<set>.json + meta -> tools/count_from_sacrum_eval.py -> SchwingNet/tools/counting_report.py",
        output="SchwingNet/results/counting.json; results/counting/*.json", pairs=None),
    "coupling": dict(
        label="classifier x count coupling on the C-ArmLSpine CV folds",
        chain="level_prototype --dump-posterior per fold -> tools/alphabet_couple.py (sacrum from rx_lodo_carmlspine_1024 "
              "boxes, conf >= 0.25 / 0.74) -> SchwingNet/tools/coupling_report.py (tau on the other four folds)",
        output="SchwingNet/results/coupling.json; results/coupling_c74/*.json",
        pairs=[("carm_cv_fold_models", "carm_cv"), ("detector_v5z_final", "carm_cv"), ("rx_lodo_carmlspine_1024", "carm_all148")]),
    "contribution": dict(
        label="contribution matrix (24 arms x held-out devices)",
        chain="devcorpus_train.py score / or_recall_curves sweep -> realxray_eval --dump-raw -> SchwingNet/tools/contribution_matrix.py",
        output="SchwingNet/results/contribution_matrix.json", pairs=None),
    "lcurve": dict(
        label="real-frame learning curve and all-real controls",
        chain="tools/lcurve_train.py / realxray_eval --dump-raw -> tools/lcurve_score.py -> tools/lcurve_report.py",
        output="SchwingNet/results/lcurve/lcurve.json", pairs=None),
    "fig3_scored": dict(
        label="Figure 3 re-scores of the sweep dumps",
        chain="tools/fig3_detection_grid.py (lcurve_score over or_ready/lodo/sweeps) -> SchwingNet/tools/fig_detection.py",
        output="SchwingNet/results/fig3_detection/scored/*.json; figures/fig3_detection.numbers.json", pairs=None),
    "device_cards": dict(
        label="per-device image-formation cards, leave-one-group-out",
        chain="tools/device_fit.py (run_loso: fit on 40 frames of the other groups, score the held group) -> docs/devices/*.json "
              "-> rigor_fixes a6 / a3 card_vs_uncalibrated_physics",
        output="docs/devices/*.json; SchwingNet/results/a6.json; a3.json#comparisons/card_vs_uncalibrated_physics", pairs=None),
    "fig4a_pairs": dict(
        label="Figure 4a example pairs: R^2 under the card's fitted MEDIANS over the six folds",
        chain="SchwingNet/tools/fig4_pairs_pull.py", output="SchwingNet/results/fig4_pairs/*.json", pairs=None),
    "manifold": dict(
        label="corpus manifold / film-vs-fluoro classifier (no persisted checkpoint; corpus held out whole)",
        chain="tools/corpus_manifold.py -> rigor_fixes a2; SchwingNet/tools/fig_manifold.py (ImageNet ResNet-50 features)",
        output="SchwingNet/results/a2.json#corpus_manifold; results/corpus_manifold/*; figures/fig_manifold.record.json", pairs=[]),
    "arc": dict(
        # VOID curve (scored on the 17 selection subjects), renamed 2026-09-23. Its replacement,
        # results/arc/recall_vs_angle_unseen/, is certified by its own eval_gate block and by CHK-9's `arc_unseen` set
        # (tools/eval_gate.EVAL_SET_SPECS), NOT by a row here: this table spells the 125 training subjects as the one
        # symbolic token ts:train125, so explicit ts:s#### keys can never meet it and a row would pass for that reason.
        label="recall against C-arm angle on styled renders of 17 TotalSegmentator subjects (VOID: selection subjects)",
        chain="tools/arc_angle_set.py -> tools/arc_recall_eval.py (loads every --weights)",
        output="SchwingNet/results/arc/recall_vs_angle_selection_leaked/recall_vs_angle.json",
        pairs=[("dc_P_pooled", "arc17"), ("dc_A_held_surgio_b51_dr", "arc17"), ("dc_B_held_surgio_b51_dr_s1", "arc17"),
               ("rx_lodo_carmlspine_1024", "arc17")]),
    "case134": dict(
        label="case134 real CBCT spin, recall against angle",
        chain="slurm/case134_export_score.sh -> tools/case134_sweep.py score (loads every --weights)",
        output="SchwingNet/results/arc/case134_sweep.json",
        pairs=[("dc_P_pooled", "case134_spin"), ("dc_A_held_surgio_b51_dr", "case134_spin"),
               ("dc_B_held_surgio_b51_dr_s1", "case134_spin"), ("rx_lodo_carmlspine_1024", "case134_spin")]),
    "embedding_v9": dict(
        label="Figure 2: what the v9 level encoder learned (validation split = its selection split; three never-seen L6 patients)",
        chain="grid tools/fig2_heldout_embed.py, fig2_occlusion_clean.py -> SchwingNet/tools/figure2_analyse.py -> "
              "results/figure2/figure2_metrics.json, zones_lateral_clean.json",
        output="SchwingNet/results/figure2/figure2_metrics.json; results/figure2/zones_lateral_clean.json",
        pairs=[("allspine_v9_encoder", "v9_val_clean")]),
    "card_refit": dict(
        label="Figure S2d: the card refit and its own gate (published card vs free / constrained refit on held-out frames)",
        chain="grid or_ready/devices_refit*/ -> SchwingNet/results/supplement_figs/card_refit/{full,constrained}/<device>.refit.json",
        output="SchwingNet/results/supplement_figs/card_refit/*/<device>.refit.json#held_out", pairs=[]),
    "count_only": dict(label="a count, a dataset property, arithmetic, a parameter value or a published number", chain="-",
                       output="-", pairs=[]),
}


def arms_in(text):
    """(checkpoint, eval set) pairs named in a row: dc_* run names, lodo sweep arms, and the dataset words around them."""
    out = []
    t = text
    ds = []
    if re.search(r"C-ArmLSpine|carm_test|surgio_b51_dr arm|held-out C-arm", t):
        ds.append("carm_test")
    if re.search(r"COBRA|cobra_test|elekta_xvi arm", t):
        ds.append("cobra_test")
    if re.search(r"six specimens|DeepFluoro six|df_all6", t):
        ds.append("df_all6")
    if re.search(r"test specimen|df_test|cios_fusion arm|18-1109", t):
        ds.append("df_test")
    if re.search(r"Geneva|geneva|bv_pulsera", t):
        ds.append("geneva_all")
    for m in re.finditer(r"\b(dc_[AB]_held_[a-z0-9_]+?|dc_P_pooled)(?:\{[^}]*\})?(?=[`\s,;)|]|$)", t):
        name = m.group(1)
        base = re.sub(r"_s1$", "", name)
        for cand in (name, base):
            if cand in CHECKPOINTS:
                for d in ds or ["carm_test"]:
                    out.append((cand, d))
                break
    return out


def lcurve_pairs(t):
    out = []
    LES = {"surgio_b51_dr": "carm_test", "elekta_xvi": "cobra_test", "cios_fusion": "df_test"}
    for dev, es in LES.items():
        if f"devices/{{surgio_b51_dr,elekta_xvi,cios_fusion}}/points[0]" in t:
            out.append((LC_PARENT[dev], es))
    for m in re.finditer(r"devices/(surgio_b51_dr|elekta_xvi|cios_fusion)/points\[(\d+)\]", t):
        dev, k = m.group(1), int(m.group(2))
        out.append((LC_PARENT[dev] if k == 0 else f"lc_{dev}", LES[dev]))   # points[0] = stage 1 as is; >= 1 = fine-tunes
    if "all_real" in t:
        if re.search(r"only C-ArmLSpine|real only", t):
            out.append(("rx_only_carmlspine_1024", "carm_test"))
        if re.search(r"pooled real on C-ArmLSpine|surgio_b51_dr/all_real\[1\]|two C-ArmLSpine controls", t):
            out.append(("rx_pooled_1024", "carm_test"))
        if re.search(r"pooled real on COBRA|elekta_xvi/all_real\[0\]", t):
            out.append(("rx_pooled_1024", "cobra_test"))
        if re.search(r"DeepFluoro test specimen|cios_fusion/all_real\[0\]", t):
            out.append(("rx_pooled_1024", "df_test"))
    return out


TABLE2_CELLS = [  # tables/tab2_detection.sources.md cells behind NUMBERS.md 'Table 2, single-source and render-only arms'
    ("dc_A_held_surgio_b51_dr_1dev_elekta_xvi", "carm_test"), ("dc_A_held_surgio_b51_dr_1dev_cios_fusion", "carm_test"),
    ("dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238", "carm_test"), ("anchor_none_v2_17-1882", "carm_test"),
    ("rx_lodo_cobra_elekta_1024", "cobra_test"), ("dc_A_held_elekta_xvi_1dev_cios_fusion", "cobra_test"),
    ("dc_A_held_elekta_xvi_1dev_surgio_b51_dr", "cobra_test"), ("anchor_none_v2_17-1882", "cobra_test"),
    ("dc_B_held_cios_fusion", "df_all6"), ("dc_A_held_cios_fusion", "df_all6"), ("dc_A_held_cios_fusion_s1", "df_all6"),
    ("dc_A_held_cios_fusion_1dev_elekta_xvi", "df_all6"), ("dc_A_held_cios_fusion_1dev_surgio_b51_dr", "df_all6"),
    ("rx_lodo_deepfluoro_1024", "df_test"), ("anchor_none_v2_17-1882", "df_test")]
SEED_SPREAD = [("dc_A_held_elekta_xvi", "cobra_test"), ("dc_A_held_elekta_xvi_s1", "cobra_test"),
               ("dc_A_held_cios_fusion", "df_all6"), ("dc_A_held_cios_fusion_s1", "df_all6"),
               ("dc_B_held_cios_fusion", "df_all6"), ("dc_B_held_cios_fusion_s1", "df_all6"),
               ("dc_A_held_surgio_b51_dr", "carm_test"), ("dc_A_held_surgio_b51_dr_s1", "carm_test")]
ADD_E_TO_D = [("dc_A_held_surgio_b51_dr", "carm_test"), ("dc_A_held_surgio_b51_dr_s1", "carm_test"),
              ("dc_A_held_surgio_b51_dr_1dev_cios_fusion", "carm_test")]
EQCOUNT = [("dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238", "carm_test"), ("dc_A_held_surgio_b51_dr_1dev_elekta_xvi", "carm_test"),
           ("dc_A_held_surgio_b51_dr_1dev_cios_fusion", "carm_test")]
B_MINUS_A = [("dc_B_held_surgio_b51_dr_s1", "carm_test"), ("dc_A_held_surgio_b51_dr", "carm_test"), ("dc_A_held_surgio_b51_dr_s1", "carm_test")]
PARAMETER_ONLY = re.compile(r"physics_terms/fitted|fit_pitch_mm|physics_defaults|n_frames_total|column headers|scale bar|"
                            r"not an evaluation|Elekta XVI footnote|pixel-to-mm")


def classify(text, cite):
    """(family, pairs) for one quoted row, from the file it cites and its own words."""
    t = f"{text} || {cite}"
    if PARAMETER_ONLY.search(t) and not re.search(r"held.out R|held_out_r2|R² card|R\^2 card|gain", t):
        return "count_only", []
    if re.search(r"persons per subtype|power_table|Wilson 95 % lower bound|inventory marker", t):
        return "count_only", []          # counts and arithmetic; the v8-split tag they carry is discussed in EVALUATORS.md
    # Figure 2 (added 2026-09-23 by the EVAL_LEAKS sweep: these rows fell through to count_only, so CHK-9 passed them
    # unchecked). A row that only counts the evaluation set (#cleaning, the transitional census) stays a count.
    # the pooled card gain (recompute.json#R2_card) is over all four devices, even where the row names one of them
    if re.search(r"R2_card", t):
        return "device_cards", []
    # L6 recall on v9 validation spines (LEVELCHECK_MODEL.md section 8 item 3 calls them held out; they are the
    # encoder's selection split)
    if re.search(r"render L6 recall", t):
        return "embedding_v9", [("allspine_v9_encoder", "v9_val")]
    if re.search(r"results/figure2/|figure2_metrics|zones_lateral", t):
        if re.search(r"figure2_metrics\.json#(cleaning|bank_transitional_census|sacralised_in_validation)", t) \
                and not re.search(r"heldout_l6|silhouette|nearest_other|called_own|zones_lateral", t):
            return "count_only", []
        if re.search(r"never-seen|heldout_l6|heldout_gate_check", t):
            return "embedding_v9", [("allspine_v9_encoder", "carm_l6_never_seen")]
        return "embedding_v9", FAMILIES["embedding_v9"]["pairs"]
    if "tab2_detection.sources.md" in t and re.search(r"single-source|render-only", t):
        return "contribution", TABLE2_CELLS
    if "seed_spread" in t or "seed spread" in t:
        return "contribution", SEED_SPREAD
    if re.search(r"equal-count|named_paired_comparisons", t):
        return "contribution", EQCOUNT
    if "design_B_minus_A" in t or "design B minus A" in t:
        return "contribution", B_MINUS_A
    if re.search(r"\+71\.8", t) and "contribution_matrix" in t:
        return "contribution", ADD_E_TO_D
    if re.search(r"arc/recall_vs_angle|recall_vs_angle\.json", t):
        return "arc", FAMILIES["arc"]["pairs"]
    if "case134_sweep" in t:
        return "case134", FAMILIES["case134"]["pairs"]
    if re.search(r"zeroshot2|zero-shot|zeroshot_lateral_vs_ap|no C-ArmLSpine frame in training", t):
        return "carm_zeroshot", FAMILIES["carm_zeroshot"]["pairs"]
    if re.search(r"cvday|day-grouped|acquisition-day", t):
        return "carm_cvday_naming", FAMILIES["carm_cvday_naming"]["pairs"]
    if re.search(r"oracle/LAT|oracle~1|oracle boxes|truth boxes", t) and "coupling" not in t:
        return "carm_cv_oracle", FAMILIES["carm_cv_oracle"]["pairs"]
    if re.search(r"a4\.json|a9\.json#cv/cv5|a7\.json#cells/cv5|carmlspine_cv5_mixed|fig5_naming_data\.json#a|model_rung_1_ft_cv", t):
        return "carm_cv_naming", FAMILIES["carm_cv_naming"]["pairs"]
    if re.search(r"a5\.json|a5_rows|v8 bank|plain-film naming|CSXA exact|BUU exact|NHANES II exact", t):
        return "film_naming_v8", FAMILIES["film_naming_v8"]["pairs"]
    if re.search(r"render_vs_film|a3a_rows|film-trained|render-trained|real film", t):
        if re.search(r"film-trained detector \(in-sample\)", text) and "render-trained" not in text:
            return "render_vs_film", [("detector_v5z_final", "nhanes25")]
        if re.search(r"render-trained detector, same bodies", text):
            return "render_vs_film", [("anchor_det_v1", "nhanes25")]
        pairs = list(FAMILIES["render_vs_film"]["pairs"])
        if re.search(r"renders-only arm is at 31\.7", text):
            pairs.append(("anchor_none_v2_17-1882", "carm_test"))
        return "render_vs_film", pairs
    if re.search(r"pooled_vs_heldout|same-device control \(pooled|same comparison, vertebra", t):
        return "pooled_vs_lodo_carm", FAMILIES["pooled_vs_lodo_carm"]["pairs"]
    if re.search(r"primary_with_holm", t):
        return "count_only", (FAMILIES["render_vs_film"]["pairs"] + FAMILIES["pooled_vs_lodo_carm"]["pairs"]
                              + FAMILIES["carm_zeroshot"]["pairs"])
    if re.search(r"coupling|coupling_c74|fig5_naming_data\.json#d|COUPLING", t):
        return "coupling", FAMILIES["coupling"]["pairs"]
    if re.search(r"counting\.json|results/counting/|ordinal", t):
        pairs = [("rx_lodo_carmlspine_1024", "carm_test")]
        if re.search(r"COBRA|lodo_cobra", t):
            pairs.append(("rx_lodo_cobra_elekta_1024", "cobra_test"))
        if re.search(r"DeepFluoro|lodo_df|pooled over the three|pooled three", t):
            pairs += [("rx_lodo_cobra_elekta_1024", "cobra_test"), ("rx_lodo_deepfluoro_1024", "df_test")]
        return "counting", sorted(set(pairs))
    if re.search(r"a1\.json", t):
        return "lodo_detector_on_carm", FAMILIES["lodo_detector_on_carm"]["pairs"]
    if re.search(r"fig4_pairs", t):
        return "fig4a_pairs", []
    if re.search(r"a6\.json|card_vs_uncalibrated|docs/devices|held-out R|physics_terms|Table S1|nine terms|make_supp_device_table", t) \
            or re.match(r"^(BV Pulsera|Cios Fusion|Elekta XVI|PIXIUM 4600) \| \+0\.\d", text):
        return "device_cards", []
    if re.search(r"corpus_manifold|overlap\.json|embedding\.csv|a2\.json#corpus|film vs fluoro|manifold", t):
        return "manifold", []
    if re.search(r"a2\.json#rescore_outline|multiplicity", t):
        return "count_only", []
    if "lcurve.json" in t:
        return "lcurve", lcurve_pairs(t)
    m = re.search(r"fig3_detection/scored/([a-z_]+?)__([a-z0-9_]+)\.json", t)
    if m:
        return "fig3_scored", [(ARM_CK[m.group(1)], SWEEP_SET.get(m.group(2), m.group(2)))]
    m = re.search(r"fig3_detection/examples/([a-z0-9_]+)\.json", t)
    if m:
        ex = {"surgio_b51_dr": ("rx_lodo_carmlspine_1024", "carm_test"), "elekta_xvi": ("rx_lodo_cobra_elekta_1024", "cobra_test"),
              "cios_fusion": ("rx_lodo_deepfluoro_1024", "df_test"), "bv_pulsera": ("rx_pooled_1024", "geneva_all")}
        return "fig3_scored", [ex[m.group(1)]]
    # "add X to Y" rows of the contribution matrix that say "same pairs" and name no run (EVAL_LEAKS 2026-09-23: they
    # fell through to count_only). Held device from the set the row names; the base arm is the one-source A run.
    m = re.search(r"add ([DES]) to ([DES]), (held-out C-ArmLSpine|DeepFluoro six|held-out COBRA)", text)
    if m:
        es, held = {"held-out C-ArmLSpine": ("carm_test", "surgio_b51_dr"), "DeepFluoro six": ("df_all6", "cios_fusion"),
                    "held-out COBRA": ("cobra_test", "elekta_xvi")}[m.group(3)]
        pairs = [(f"dc_A_held_{held}", es), (f"dc_A_held_{held}_s1", es)]
        for letter in {m.group(1), m.group(2)}:
            base = f"dc_A_held_{held}_1dev_{ADD_LETTER[letter]}"
            if base in CHECKPOINTS:
                pairs.append((base, es))
        return "contribution", sorted(set(pairs))
    if re.search(r"contribution_matrix|dc_[ABP]_|renders only|\blodo_carm\b", t):
        pairs = arms_in(t)
        if re.search(r"`render`|renders only|or_ready/lodo/sweeps/render", t):
            for d in [x for x in ("carm_test", "cobra_test", "df_test") if x in {p[1] for p in pairs} or not pairs]:
                pairs.append(("anchor_none_v2_17-1882", d))
        if re.search(r"`lodo_carm`|real frames only D\+E", t):
            pairs.append(("rx_lodo_carmlspine_1024", "carm_test"))
        return "contribution", sorted(set(pairs))
    return "count_only", []


ADD_LETTER = {"D": "cios_fusion", "E": "elekta_xvi", "S": "surgio_b51_dr"}


# ------------------------------------------------------------------------------------------------ row sources
def md_table_rows(path):
    """(line number, cells, section heading) for every table body row of a markdown file."""
    out, sec = [], ""
    for i, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            sec = line.lstrip("# ").strip()
        if line.startswith("|") and not re.match(r"^\|\s*-", line) and not re.match(r"^\|\s*(number|panel|claim|study|source|corpus|device|candidate sentence|id)\s*\|", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append((i, cells, sec))
    return out


def rows_numbers():
    rows = []
    for ln, cells, sec in md_table_rows(SN / "NUMBERS.md"):
        text = " | ".join(cells)
        cite = cells[-1] if cells else ""
        rows.append(dict(id=f"NUMBERS:L{ln}", source=f"SchwingNet/NUMBERS.md:{ln}", section=sec, quoted=text[:600], cites=cite))
    return rows


def rows_claims():
    rows = []
    for ln, cells, sec in md_table_rows(SN / "CLAIMS_LEDGER.md"):
        text = " | ".join(cells)
        ours = re.search(r"results/|docs/devices|a1\.json|a6\.json|contribution_matrix|coupling|anomalous|\+0\.\d{3,4} \[", text)
        num = re.search(r"\d+(\.\d+)?\s*(%|pp)|\+0\.\d{3,4}", text)
        if not (ours and num):
            continue                                    # published comparators and pending claims carry no number of ours
        rows.append(dict(id=f"CLAIMS:L{ln}", source=f"SchwingNet/CLAIMS_LEDGER.md:{ln}", section=sec, quoted=text[:600], cites=text))
    return rows


def rows_rescore():
    d = json.load(open(SN / "results/bodybox_rescore/rescore.json", encoding="utf-8"))
    rows = []
    for r in d["rows"]:
        wv, bd = r.get("whole_vertebra") or {}, r.get("body") or {}
        q = (f"{r['id']} {r['group']}: {r['quantity']}; WV {wv.get('value')} ({wv.get('k')}/{wv.get('n')}) {wv.get('ci')}; "
             f"BODY {bd.get('value')} ({bd.get('k')}/{bd.get('n')}) {bd.get('ci')}")
        rows.append(dict(id=f"RESCORE:{r['id']}", source=f"SchwingNet/results/bodybox_rescore/rescore.json#rows[id={r['id']}]",
                         section=r["group"], quoted=q, cites=f"{r['group']} {r['quantity']} {r.get('body_kind', '')}",
                         consumers=r.get("consumers")))
    return rows


RESCORE_MAP = {
    "A": ("lodo_detector_on_carm", [("rx_lodo_carmlspine_1024", "carm_test")]),
    "B1": ("pooled_vs_lodo_carm", FAMILIES["pooled_vs_lodo_carm"]["pairs"]),
    "B2": ("pooled_vs_lodo_carm", FAMILIES["pooled_vs_lodo_carm"]["pairs"]),
    "B3": ("render_vs_film", FAMILIES["render_vs_film"]["pairs"]),
    "C1": ("lcurve", [("dc_B_held_surgio_b51_dr_s1", "carm_test")]),
    "C2": ("lcurve", [("lc_surgio_b51_dr", "carm_test")]), "C3": ("lcurve", [("lc_surgio_b51_dr", "carm_test")]),
    "C_ar_only": ("lcurve", [("rx_only_carmlspine_1024", "carm_test")]),
    "C_ar_pooled": ("lcurve", [("rx_pooled_1024", "carm_test")]),
    "C_ar_renders": ("lcurve", [("dc_P_pooled", "carm_test")]),
    "C_cobra_stage1": ("lcurve", [("dc_B_held_elekta_xvi", "cobra_test")]),
    "C_cobra_N": ("lcurve", [("lc_elekta_xvi", "cobra_test")]),
    "C_cobra_ar_pooled": ("lcurve", [("rx_pooled_1024", "cobra_test")]),
    "C_cobra_ar_C-ArmLSpine": ("lcurve", [("rx_lodo_carmlspine_1024", "cobra_test")]),
    "C_cobra_ar_renders": ("lcurve", [("dc_P_pooled", "cobra_test")]),
    "C_df_stage1": ("lcurve", [("dc_B_held_cios_fusion", "df_test")]),
    "D1": ("contribution", [("dc_A_held_surgio_b51_dr_1dev_elekta_xvi", "carm_test")]),
    "D2": ("contribution", [("dc_A_held_surgio_b51_dr_1dev_cios_fusion", "carm_test")]),
    "D3": ("contribution", [("dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238", "carm_test")]),
    "D4": ("contribution", [("anchor_none_v2_17-1882", "carm_test")]),
    "D5": ("contribution", [("dc_A_held_surgio_b51_dr", "carm_test"), ("dc_A_held_surgio_b51_dr_1dev_cios_fusion", "carm_test")]),
    "D6": ("contribution", [("dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238", "carm_test"), ("dc_A_held_surgio_b51_dr_1dev_elekta_xvi", "carm_test")]),
    "D7": ("contribution", [("dc_A_held_elekta_xvi", "cobra_test"), ("dc_A_held_cios_fusion", "df_all6"),
                            ("dc_B_held_cios_fusion", "df_all6"), ("dc_A_held_surgio_b51_dr", "carm_test")]),
    "D8": ("contribution", [("dc_A_held_elekta_xvi_1dev_surgio_b51_dr", "cobra_test")]),
    "D9": ("contribution", [("dc_A_held_elekta_xvi_1dev_cios_fusion", "cobra_test")]),
    "D10": ("contribution", [("dc_A_held_elekta_xvi", "cobra_test")]),
    "E1": ("fig3_scored", [("anchor_none_v2_17-1882", "carm_test")]),
    "E2": ("fig3_scored", [("anchor_none_v2_17-1882", "cobra_test")]),
    "E3": ("fig3_scored", [("rx_lodo_cobra_elekta_1024", "cobra_test")]),
    "E4": ("fig3_scored", [("anchor_none_v2_17-1882", "df_test"), ("rx_lodo_deepfluoro_1024", "df_test")]),
    "E5": ("fig3_scored", [(c, "geneva_all") for c in ("anchor_none_v2_17-1882", "rx_lodo_carmlspine_1024",
                                                        "rx_lodo_cobra_elekta_1024", "rx_lodo_deepfluoro_1024", "rx_pooled_1024")]),
    "F1": ("counting", [("rx_lodo_carmlspine_1024", "carm_test")]), "F2": ("counting", [("rx_lodo_carmlspine_1024", "carm_test")]),
    "F3": ("counting", [("rx_lodo_cobra_elekta_1024", "cobra_test")]),
    "F4": ("counting", [("rx_lodo_carmlspine_1024", "carm_test"), ("rx_lodo_cobra_elekta_1024", "cobra_test"),
                        ("rx_lodo_deepfluoro_1024", "df_test")]),
    "G1": ("coupling", FAMILIES["coupling"]["pairs"]),
    "H1": ("carm_cv_naming", FAMILIES["carm_cv_naming"]["pairs"]),
    "H2": ("carm_zeroshot", FAMILIES["carm_zeroshot"]["pairs"]),
    "I_": ("film_naming_v8", FAMILIES["film_naming_v8"]["pairs"]),
    "J1": ("contribution", [("dc_P_pooled", "carm_test")]), "J2": ("contribution", [("dc_P_pooled", "cobra_test")]),
    "J3": ("contribution", [("dc_P_pooled", "df_test"), ("dc_P_pooled", "geneva_all")]),
    "K1": ("lcurve", [("rx_pooled_1024", "cobra_test"), ("anchor_none_v2_17-1882", "cobra_test")]),
}
# D1 / D2 note: NUMBERS.md names dc_A_held_surgio_b51_dr_1dev_elekta_xvi for 'E only' and ..._1dev_cios_fusion for
# 'D only' on the C-arm; D8 / D9 are the S-only and D-only arms scored on COBRA.


def rescore_family(rid):
    for k in sorted(RESCORE_MAP, key=len, reverse=True):
        if rid.startswith(k) and (len(rid) == len(k) or not (k[-1].isdigit() and rid[len(k)].isdigit())):
            return RESCORE_MAP[k]
    return ("count_only", [])


def rows_fig3():
    d = json.load(open(SN / "figures/fig3_detection.numbers.json", encoding="utf-8"))
    return [dict(id=f"FIG3:{i:03d}", source=f"SchwingNet/figures/fig3_detection.numbers.json#numbers[{i}]",
                 section=f"Figure 3 panel {n.get('panel')}", quoted=f"{n.get('label')}: {n.get('value')} {n.get('interval')}",
                 cites=f"{n.get('label')} || {n.get('source')}") for i, n in enumerate(d["numbers"])]


def rows_records():
    rows = []
    f4 = json.load(open(SN / "figures/fig4_formation.record.json", encoding="utf-8"))
    for dev, v in (f4.get("panel_a") or {}).items():
        rows.append(dict(id=f"FIG4REC:panel_a/{dev}", source=f"SchwingNet/figures/fig4_formation.record.json#panel_a/{dev}",
                         section="Figure 4a", quoted=f"{dev}: pair {v.get('case')}/{v.get('pid')}, R2 {v.get('r2_chosen')} "
                         f"(device median {v.get('r2_median')})", cites="fig4_pairs"))
    rows.append(dict(id="FIG4REC:panel_b", source="SchwingNet/figures/fig4_formation.record.json#panel_b",
                     section="Figure 4b", quoted=f"{len(f4.get('panel_b') or {})} fitted-term cells (median, min, max over six folds)",
                     cites="parameter values of docs/devices/*.json (not an evaluation)"))
    rows.append(dict(id="FIG4REC:panel_c", source="SchwingNet/figures/fig4_formation.record.json#panel_c",
                     section="Figure 4c", quoted=json.dumps({k: (f4.get("panel_c") or {}).get(k) for k in ("n", "n_real", "pca_explained")}),
                     cites="corpus_manifold embedding.csv"))
    rows.append(dict(id="FIG4REC:panel_d", source="SchwingNet/figures/fig4_formation.record.json#panel_d",
                     section="Figure 4d", quoted=str(f4.get("panel_d")), cites="arc/recall_vs_angle (PENDING G4, not quoted)"))
    fm = json.load(open(SN / "figures/fig_manifold.record.json", encoding="utf-8"))
    for k in ("film_vs_fluoro_loso_svm", "transfer_svm", "pairwise"):
        rows.append(dict(id=f"MANIFOLDREC:{k}", source=f"SchwingNet/figures/fig_manifold.record.json#{k}",
                         section="fig_manifold", quoted=json.dumps(fm.get(k))[:500], cites="manifold (ImageNet ResNet-50 features)"))
    return rows + rows_figure_records()


# ------------------------------------------------------------------------------------------------ the six-figure records
# EVAL_LEAKS sweep (2026-09-24). NUMBERS.md says "every number on Figures 1-5 is traced in that figure's own
# figures/figureN.record.json" and lists only the numbers the TEXT quotes, so until now a number drawn on a figure and
# not repeated in the text (a Figure 2 silhouette above L1, every Figure S3 cell, the whole Figure S4 spin) was in no
# row of this file and CHK-9 never saw it. Every entry of `numbers` / `numbers_on_figure` of the current figures is a
# row now. Rows whose checkpoint is fixed by the record itself carry their pairs here (`_fixed`); the rest go through
# classify() like any other row.
FIG_RECORDS = ("figure1", "figure2", "figure4", "figure5", "figS1", "figS2", "figS3", "figS4")
S3_ARM = {"lodo_carm": "rx_lodo_carmlspine_1024", "lodo_cobra": "rx_lodo_cobra_elekta_1024", "lodo_df": "rx_lodo_deepfluoro_1024",
          "only_carm": "rx_only_carmlspine_1024", "render": "anchor_none_v2_17-1882", "pooled": "rx_pooled_1024"}
S3_SET = {("deepfluoro", "train+val+test"): "df_all6", ("deepfluoro", "test"): "df_test", ("cobra_elekta", "test"): "cobra_test",
          ("carmlspine", "test"): "carm_test"}
S3_TARGET = {"C-ArmLSpine": "carm_test", "DeepFluoro, all six": "df_all6", "COBRA": "cobra_test"}


def _s3_ck(arm):
    return S3_ARM.get(arm, arm if arm in CHECKPOINTS else None)


def _short(v, n=260):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + " ..."


def rows_figure_records():
    rows = []
    for fig in FIG_RECORDS:
        p = SN / "figures" / f"{fig}.record.json"
        if not p.exists():
            continue
        rec = json.load(open(p, encoding="utf-8"))
        src0 = f"SchwingNet/figures/{fig}.record.json"
        nums = rec.get("numbers")
        if nums is None:
            nums = rec.get("numbers_on_figure")
        if isinstance(nums, dict):                                  # figure5: {name: {value, source}}
            items = []
            for k, v in nums.items():
                if k == "counts_and_intervals" and isinstance(v, list):
                    items.append(dict(panel="c-d", what=f"{len(v)} persons-per-subtype counts and their Wilson intervals",
                                      value=None, source="; ".join(sorted({str(x.get('source', ''))[:80] for x in v}))[:400]))
                    continue
                v = v if isinstance(v, dict) else dict(value=v)
                items.append(dict(panel=k, what=k, value=v.get("value", v.get("values")), source=v.get("source", "")))
            nums = items
        for i, n in enumerate(nums or []):
            panel, what, src = str(n.get("panel", "")), str(n.get("what") or ""), str(n.get("source") or "")
            base = dict(id=f"FIGREC:{fig}/{i:02d}", source=f"{src0}#numbers[{i}]", section=f"{fig} panel {panel}")
            if fig == "figS3" and isinstance(n.get("value"), (dict, list)):
                rows += _s3_rows(base, n)
                continue
            drawn = n.get("drawn")
            q = " -- ".join(x for x in (str(drawn) if drawn is not None else "", what,
                                        _short(n.get("value")) if n.get("value") is not None else "") if x)
            r = dict(base, quoted=q[:600], cites=f"{src} {n.get('also') or ''}".strip())
            fixed = _fixed_pairs(fig, panel, what, src, drawn)
            if fixed is not None:
                r["_fixed"] = fixed
            rows.append(r)
    return rows


def _fixed_pairs(fig, panel, what, src, drawn):
    """(family, pairs) where the record names the checkpoint more exactly than classify() can, else None."""
    if fig == "figure4":
        if "boxed by the keypoint detector" in what:            # detection recall: the keypoint detector alone
            return "carm_cv_naming", [("detector_v5z_final", "carm_cv")]
        if "sacrum the held-out-device detector found" in what:
            return "coupling", [("rx_lodo_carmlspine_1024", "carm_all148")]
        if panel == "c":                                        # the count from the sacrum: boxes + sacrum, no encoder
            return "coupling", [("detector_v5z_final", "carm_cv"), ("rx_lodo_carmlspine_1024", "carm_all148")]
        if panel == "b" and "crop_b_pred" in src:               # names drawn by the fold-3 level model on case11
            return "carm_cv_naming", FAMILIES["carm_cv_naming"]["pairs"]
    if fig == "figure2":
        if re.search(r"#(per_level_n|map\.n|bank_transitional_census|sacralised_in_validation)", src):
            return "count_only", []
        if "figure2_map.npz" in src:                            # read off the encoder's t-SNE of both sets
            return "embedding_v9", [("allspine_v9_encoder", "v9_val_clean"), ("allspine_v9_encoder", "carm_l6_never_seen")]
        if "occlusion_clean" in src:
            return "embedding_v9", [("allspine_v9_encoder", "v9_val_clean")]
    if fig == "figS2":
        if panel == "b":
            return "count_only", []
        if panel == "d" or "card_refit" in src:
            return "card_refit", []
    if fig == "figS4":
        if panel == "b-c":
            return "case134", FAMILIES["case134"]["pairs"]
        return "count_only", []                                 # frame angles, registration NCC, pose refinement
    if fig in ("figure1", "figS1"):
        return ("manifold", []) if fig == "figS1" else ("count_only", [])
    if fig == "figure5" and "a4.json" not in src:
        return "count_only", []
    return None


def _s3_rows(base, n):
    """Figure S3: one row per drawn cell, with the arm and the target the cell names."""
    out = []
    v = n["value"]
    panel = str(n.get("panel"))
    cells = []
    if isinstance(v, dict):
        for key, cell in v.items():
            if isinstance(cell, str):
                continue                                         # "not scored" / "target device in training": no number drawn
            parts = key.split("|")
            ck = _s3_ck(parts[0])
            if panel == "a":
                es = S3_SET.get((parts[1], parts[2])) if len(parts) == 3 else None
            else:                                                # panel b: view (C-ArmLSpine) or gantry band (COBRA)
                es = "carm_test" if parts[-1] in ("AP", "LAT") else "cobra_test"
            cells.append((key, cell, [(ck, es)] if ck and es else []))
    else:
        for j, cell in enumerate(v):
            es = next((s for t, s in S3_TARGET.items() if t in str(cell.get("target"))), None)
            prs = [(c, es) for c in (_s3_ck(cell.get("pair_arm")), _s3_ck(cell.get("base_arm"))) if c and es]
            cells.append((f"{cell.get('row')} seed {cell.get('pair_seed')} base {cell.get('base_arm')}", cell, prs))
    for j, (key, cell, prs) in enumerate(cells):
        out.append(dict(base, id=f"{base['id']}/{j:02d}", source=f"{base['source']} [{key}]",
                        quoted=f"{key}: {_short(cell, 400)}"[:600], cites=str(n.get("source") or ""),
                        _fixed=("contribution", prs) if prs else ("contribution", []),
                        _unmapped=None if prs else f"cell {key}: arm or target not in the checkpoint table"))
    return out


# ------------------------------------------------------------------------------------------------ evaluator scan
CK_ARG = re.compile(r"weight|model|ckpt|checkpoint|detector|^--det|head|init|encoder|--pred|--dump", re.I)
CK_NOT = re.compile(r"conf|allow|rib-weight|failures|head-k|head-set|save-head|dump-posterior|--dets$", re.I)
SET_ARG = re.compile(r"--data|--split|--bank|--set|--image|--drr|--root|--meta|--cases|--fold|--list|--ctx|--carm|--cobra|--subjects|--holdout", re.I)
GATES = {
    "eval_gate.assert_unseen (mandatory, before scoring)": re.compile(r"EG\.assert_unseen|assert_unseen_all\(|fold_gate\("),
    "eval_gate.carry (the input's verdict carried or gated at scoring)": re.compile(r"EG\.carry(_proto)?\(|_gate_input\("),
    "holdout.trained_on":re.compile(r"HO\.trained_on\(|holdout\.trained_on\(|^\s*import holdout|from holdout import"),
    "reads split == 'train' itself (a split read; a gate only if it refuses)": re.compile(r"^(?!.*\bcmd\b).*==\s*[\"']train[\"']"),
    "patient_keys": re.compile(r"patient_keys"),
    "leak_check": re.compile(r"\bleak_check\b"),
    "model_registry.resolve (a resolver, not a gate)": re.compile(r"from model_registry import resolve|resolve_default\("),
}


def scan(rel):
    p = REPO / rel
    src = p.read_text(encoding="utf-8", errors="replace")
    ck, es = [], []
    try:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "add_argument":
                flags = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-")]
                for f in flags:
                    if CK_NOT.search(f):
                        continue
                    if CK_ARG.search(f):
                        ck.append(f)
                    elif SET_ARG.search(f):
                        es.append(f)
        doc = (ast.get_docstring(tree) or "").strip().splitlines()
        doc = doc[0] if doc else ""
    except SyntaxError:
        doc = "(not parseable)"
    subs = re.findall(r"add_parser\(\s*[\"']([\w-]+)", src)
    loads = sorted({x for x in ("YOLO(", "torch.load(", "load_state_dict(", "load_level_model(") if x in src})
    gates = [g for g, rx in GATES.items() if any(rx.search(l) for l in src.splitlines())]
    return dict(script=rel, doc=doc[:150], subcommands=subs, checkpoint_args=sorted(set(ck)), evalset_args=sorted(set(es)),
                loads_weights=loads, gate_today=gates or ["none"])


# the scripts on the path of a quoted number, with the role each plays (hand map; everything else is scanned only)
ON_PATH = {
    "tools/realxray_eval.py": "LOADS a YOLO checkpoint (--weights) and scores --data/--split; writes the dump every detector number is re-scored from (records weights path, data, split)",
    "tools/or_recall_curves.py": "sweep: runs realxray_eval for every arm in its hand DETECTORS table x every set; the table carries trained_on / selected_on_test as LABELS only",
    "tools/or_lodo_rescore_outline.py": "re-scores the sweep dumps under the outline convention (no checkpoint)",
    "tools/devcorpus_train.py": "trains a dc_* arm and scores it with realxray_eval on every device's test split; status label DEVICE-HELD-OUT is hand-derived from the design, not from lineage",
    "tools/lcurve_train.py": "fine-tunes lc_* from the dc_B parent and scores it with realxray_eval",
    "tools/lcurve_score.py": "scores one dump (no checkpoint)",
    "tools/lcurve_report.py": "assembles lcurve.json from scored dumps; the all-real descriptions are hand text",
    "tools/fig3_detection_grid.py": "re-scores sweep dumps for Figure 3 with lcurve_score (no checkpoint)",
    "tools/arc_recall_eval.py": "LOADS every --weights and scores the angle-sweep set (the leak that started this)",
    "tools/arc_angle_set.py": "builds the angle-sweep set from STYLE_INFO val subjects (the 17 selection subjects)",
    "tools/case134_sweep.py": "LOADS every --weights and scores the case134 spin; its contamination text is hand-written",
    "tools/level_prototype.py": "LOADS detector + encoder + head (defaults resolved through the registry) and names every vertebra in --image; writes prototype_meta.json with both sha256",
    "tools/carmlspine_eval.py": "scores prototype outputs against the projected CBCT labels (no checkpoint)",
    "tools/carmlspine_pool_scores.py": "pools carmlspine_eval scores over splits (no checkpoint)",
    "tools/head_mixed_length.py": "LOADS an encoder, trains a head on the bank's train films and scores the bank's VAL films (the encoder's selection set)",
    "tools/rigor_fixes.py": "a3a-rows and a5-rows LOAD checkpoints; a1/a3/a4/a7/a9 are statistics over dumps; a3a-rows is the only evaluator that calls holdout.trained_on, and it checks the level bank allspine_v7, not the detector's own train list",
    "tools/count_from_sacrum_eval.py": "counting from a detector dump (no checkpoint)",
    "tools/alphabet_couple.py": "couples classifier posteriors with the count (no checkpoint)",
    "tools/device_fit.py": "fits the nine-term card leave-one-group-out and scores the held group",
    "tools/corpus_manifold.py": "image-statistics features and the leave-one-corpus-out classifier (a2)",
    "tools/learning_embed.py": "LOADS an encoder and reads the bank's VAL crops as 'held-out'",
    "tools/sweep_map.py": "LOADS encoder/head/detector; its --holdout-bank read is now holdout.trained_on (train + val, since 2026-09-23); not on a quoted path",
    "SchwingNet/tools/contribution_matrix.py": "re-scores every arm's raw dump; the DEVICE-HELD-OUT status is a hand table (LODO_ARMS)",
    "SchwingNet/tools/counting_report.py": "collects count_from_sacrum_eval outputs (no checkpoint)",
    "SchwingNet/tools/coupling_report.py": "collects alphabet_couple outputs; tau set on the other folds (no checkpoint)",
    "SchwingNet/tools/fig_detection.py": "draws Figure 3 from the scored files",
    "SchwingNet/tools/fig_naming.py": "draws Figure 5 from a4/a9/counting/coupling",
    "SchwingNet/tools/fig_formation.py": "draws Figure 4 from device cards, fig4_pairs and the manifold",
    "SchwingNet/tools/fig4_pairs_pull.py": "Figure 4a pairs: R^2 under the card's fold MEDIANS (in-sample for the pair's group)",
    "SchwingNet/tools/fig_manifold.py": "ImageNet ResNet-50 features + LOSO SVM",
    "SchwingNet/tools/fig5_contribution.py": "draws Figure S2 from contribution_matrix.json (no checkpoint)",
    "SchwingNet/tools/make_supp_device_table.py": "writes Table S1 from docs/devices/*.json (fold medians and held-out R^2; no checkpoint)",
    "SchwingNet/tools/fig_claim.py": "draws Figure 6 and writes power_table.json (arithmetic; no checkpoint)",
    "SchwingNet/tools/fig2_flow.py": "draws the flow of cases (counts; no checkpoint)",
    "SchwingNet/tools/make_lists_eqcount.py": "builds the TRAINING lists of the eq238 arm (an input to a scored checkpoint, not an evaluator)",
    "SchwingNet/tools/fig_detection_numbers.py": "rewrites NUMBERS.md's Figure 3 section from fig3_detection.numbers.json (no checkpoint)",
    "SchwingNet/tools/stats_review_recompute.py": "independent recomputation of quoted quantities from result files (no checkpoint)",
    "SchwingNet/tools/counting_outside_check.py": "verifier of the counting cells from the raw dumps (no checkpoint)",
    "SchwingNet/tools/counting_check_hand.py": "verifier of chosen counting frames (no checkpoint)",
    "SchwingNet/tools/coupling_check_split.py": "verifier: reads the level bank split for the alphabet-loss spines (patient_keys)",
    "tools/needle_confirm.py": "not on the path of a quoted number; takes --holdout-bank (required) and NEVER reads it, and --allow-trained-on defaults to True",
}


def all_scripts():
    names = set(ON_PATH)
    names |= {f"tools/{p.name}" for p in (REPO / "tools").glob("*eval*.py")}
    names |= {f"SchwingNet/tools/{p.name}" for p in (REPO / "SchwingNet/tools").glob("*.py")}
    names |= {"tools/learning_embed.py", "tools/sweep_map.py", "tools/detector_quality.py", "tools/detector_failures.py",
              "tools/validate_guided.py", "tools/fiducial_walk.py", "tools/needle_confirm.py", "tools/or_crossdev_score.py",
              "tools/wholespine_eval.py", "tools/thoracic_xr_eval.py", "tools/realxray_robustness.py", "tools/common_testset_eval.py"}
    return sorted(n for n in names if (REPO / n).exists())


# ------------------------------------------------------------------------------------------------ build
def build():
    rows = []
    for r in rows_numbers() + rows_claims() + rows_fig3() + rows_records():
        fam, pairs = r.pop("_fixed", None) or classify(r["quoted"], r["cites"])
        rows.append(dict(r, family=fam, pairs=pairs))
    for r in rows_rescore():
        fam, pairs = rescore_family(r["id"].split(":", 1)[1])
        rows.append(dict(r, family=fam, pairs=pairs))
    out = []
    for r in rows:
        F = FAMILIES[r["family"]]
        v = combine([tuple(p) for p in r["pairs"]])
        if r["family"] == "device_cards":
            v = dict(verdict="MIXED", why="leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and "
                     "elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 "
                     "(one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device row takes that "
                     "device's verdict", per_pair=[dict(checkpoint=f"card:{k}", eval_set=f"held {c['group']}",
                     verdict="HELD OUT" if c["patient_heldout"] else "NOT HELD OUT") for k, c in CARDS.items()], pose_donor=[])
            pooled = re.search(r"R2_card|four device|24 folds|all four", f"{r['quoted']} {r.get('cites') or ''}")
            for dev, c in ({} if pooled else CARDS).items():
                if dev in r["quoted"] or {"bv_pulsera": "Pulsera", "cios_fusion": "Cios", "elekta_xvi": "Elekta", "pixium_4600": "PIXIUM"}[dev] in r["quoted"]:
                    if sum(1 for d2 in ("Pulsera", "Cios", "Elekta", "PIXIUM") if d2 in r["quoted"]) == 1:
                        v["verdict"] = "HELD OUT" if c["patient_heldout"] else "NOT HELD OUT"
                        v["why"] = f"{dev}: folds by {c['group']}"
                        # the row's pairs are that device's alone (leak_check CHK-9 checks every listed pair; listing
                        # all four made a Cios Fusion row fail on the Geneva phantom's folds)
                        v["per_pair"] = [p for p in v["per_pair"] if p["checkpoint"] == f"card:{dev}"]
        if r["family"] == "fig4a_pairs":
            # a `card_median:<device>` pair per device the row names, so leak_check CHK-9 checks it from the device's
            # per-fold gate record instead of passing it as N/A (it did, 2026-09-23: no pair, no check)
            devs = [d for d, w in (("bv_pulsera", "Pulsera"), ("cios_fusion", "Cios"), ("elekta_xvi", "Elekta"),
                                   ("pixium_4600", "PIXIUM")) if d in r["quoted"] or w in r["quoted"]] or list(CARDS)
            v = dict(verdict="NOT HELD OUT", why="the R^2 is computed under the MEDIAN of the six fold fits, five of which "
                     "were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, "
                     "not the held-out R^2 of Table 1",
                     per_pair=[dict(checkpoint=f"card_median:{d}", eval_set=f"{d} pairs", verdict="NOT HELD OUT",
                                    why="median over every fold fit") for d in devs], pose_donor=[])
        if r["family"] == "card_refit":
            v = dict(verdict="NOT ESTABLISHED", why="card_refit writes n_train / n_held only, not which frames (or subjects) "
                     "were fitted and which held out; the 'published' row is the released card, whose fold fits cover every "
                     "group of the device, so its R^2 on these frames is not subject-held-out either", per_pair=[], pose_donor=[])
        if r.get("_unmapped"):
            v = dict(verdict="NOT ESTABLISHED", why=r["_unmapped"], per_pair=[], pose_donor=[])
        if r["family"] == "manifold":
            v = dict(verdict="N/A", why="no persisted checkpoint: the classifier is refit per fold with one CORPUS held out "
                     "whole; the deep features are public ImageNet weights, declared in fig_manifold.record.json", per_pair=[], pose_donor=[])
        es = sorted({p[1] for p in r["pairs"]})
        cks = sorted({p[0] for p in r["pairs"]})
        out.append(dict(
            id=r["id"], source=r["source"], section=r.get("section"), quoted=r["quoted"], cites=r.get("cites"),
            family=r["family"], evaluator_chain=F["chain"], output_file=F["output"],
            checkpoints=[dict(key=c, path=CHECKPOINTS[c].get("path") if c in CHECKPOINTS else None,
                              init_chain=chain(c) if c in CHECKPOINTS else None,
                              selection=CHECKPOINTS[c].get("selection") if c in CHECKPOINTS else None) for c in cks],
            eval_sets=[dict(key=e, desc=EVALSETS[e]["desc"], items_listed_in=EVALSETS[e]["items"], unit=EVALSETS[e]["unit"]) for e in es],
            heldout_under_rule=v["verdict"], why=v["why"], per_pair=v.get("per_pair", []), pose_donor=v.get("pose_donor", []),
            consumers=r.get("consumers")))
    return out


def md_counts(out):
    from collections import Counter
    L = ["| source | rows | HELD OUT | NOT HELD OUT | MIXED | NOT ESTABLISHED | N/A |", "|---|---:|---:|---:|---:|---:|---:|"]
    by = {}
    for r in out:
        by.setdefault(r["id"].split(":")[0], Counter())[r["heldout_under_rule"]] += 1
    for s, c in by.items():
        L.append(f"| {s} | {sum(c.values())} | {c['HELD OUT']} | {c['NOT HELD OUT']} | {c['MIXED']} | {c['NOT ESTABLISHED']} | {c['N/A']} |")
    tot = Counter(r["heldout_under_rule"] for r in out)
    L.append(f"| **all** | **{len(out)}** | {tot['HELD OUT']} | {tot['NOT HELD OUT']} | {tot['MIXED']} | {tot['NOT ESTABLISHED']} | {tot['N/A']} |")
    return "\n".join(L)


def md_not_held(out):
    L = ["| row | quoted (truncated) | why |", "|---|---|---|"]
    for r in out:
        if r["heldout_under_rule"] in ("NOT HELD OUT", "MIXED", "NOT ESTABLISHED"):
            q = r["quoted"].replace("|", "/")[:170]
            w = r["why"].replace("|", "/")[:260]
            L.append(f"| `{r['id']}` | {q} | {r['heldout_under_rule']}: {w} |")
    return "\n".join(L)


def md_pose(out):
    seen, L = set(), ["| checkpoint | evaluation set | pose-donor renders in the checkpoint's train+val (or an ancestor's) | rows |", "|---|---|---|---:|"]
    agg = {}
    for r in out:
        for p in r["per_pair"]:
            for x in p.get("pose_donor", []):
                k = (p["checkpoint"], p["eval_set"], x)
                agg[k] = agg.get(k, 0) + 1
    for (ck, es, x), n in sorted(agg.items()):
        L.append(f"| {ck} | {es} | {x} | {n} |")
    return "\n".join(L)


def md_lineage():
    L = ["| checkpoint | init chain (to a public root) | train | val / selection | selected how | read from |", "|---|---|---|---|---|---|"]
    for k, c in CHECKPOINTS.items():
        if c.get("public"):
            continue
        ch = " -> ".join(chain(k)) + (" (root init NOT RECORDED)" if any(CHECKPOINTS[x].get("parent_unknown") for x in chain(k)) else "")
        tr = ", ".join(sorted(x for x in c.get("train", set()) if not x.startswith("ts:s"))) or "-"
        if any(x.startswith("ts:s") for x in c.get("train", set())):
            tr += " + " + " ".join(sorted(x[3:] for x in c["train"] if x.startswith("ts:s")))
        va = ", ".join(sorted(x for x in c.get("val", set()) if not x.startswith("ts:s"))) or "-"
        if any(x.startswith("ts:s") for x in c.get("val", set())) and "ts:val17" not in c.get("val", set()):
            va += " + " + " ".join(sorted(x[3:] for x in c["val"] if x.startswith("ts:s")))
        L.append(f"| `{k}` | {ch} | {tr} | {va} | {c.get('selection', '')} | {c.get('evidence', '')[:220]} |")
    return "\n".join(L)


def md_scripts():
    L = ["| script | entry point | on the path of a quoted number | checkpoint in | evaluation set in | loads weights | gate today |",
         "|---|---|---|---|---|---|---|"]
    for s in all_scripts():
        d = scan(s)
        role = ON_PATH.get(s, "not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output)")
        entry = "main" + (f" ({', '.join(d['subcommands'])})" if d["subcommands"] else "")
        L.append(f"| `{s}` | {entry} | {role} | {' '.join(d['checkpoint_args']) or '-'} | {' '.join(d['evalset_args']) or '-'} | "
                 f"{' '.join(d['loads_weights']) or '-'} | {'; '.join(d['gate_today'])} |")
    return "\n".join(L)


def fill(md_path, blocks):
    txt = md_path.read_text(encoding="utf-8")
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- BEGIN:GENERATED {name} -->\r?\n)(?:.*?\r?\n)?(<!-- END:GENERATED {name} -->)", re.S)
        if not pat.search(txt):
            raise SystemExit(f"EVALUATORS.md has no block {name}")
        txt = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), txt)
    md_path.write_text(txt, encoding="utf-8")


def main() -> int:
    out = build()
    doc = dict(
        schema="eval_gate/quoted_results/1", built_by="SchwingNet/results/eval_gate/build_inventory.py",
        rule=("an evaluation item is HELD OUT for a checkpoint only if its patient key (a render inherits its source CT "
              "subject) is in neither the train nor the val/selection set of that checkpoint nor of any ancestor in its "
              "initialisation chain; public ImageNet / COCO weights are the only exempt ancestor, and only when declared"),
        verdicts={"HELD OUT": "established from recorded lists", "NOT HELD OUT": "an eval token is in a train or val/selection set on the chain",
                  "MIXED": "the row pools pairs with different verdicts", "NOT ESTABLISHED": "lineage missing",
                  "N/A": "no checkpoint (count, parameter, arithmetic, published number)"},
        pose_donor_note=("pose-donor overlap is reported, not scored: a styled/anchor render is a TotalSegmentator subject "
                         "under the registered pose of a real frame. leak_check.py check (6) treats the donor as a dependency."),
        checkpoints={k: {kk: (sorted(vv) if isinstance(vv, set) else vv) for kk, vv in c.items()} for k, c in CHECKPOINTS.items()},
        eval_sets={k: {kk: (sorted(vv) if isinstance(vv, set) else vv) for kk, vv in e.items()} for k, e in EVALSETS.items()},
        families={k: {kk: vv for kk, vv in f.items() if kk != "pairs"} for k, f in FAMILIES.items()},
        n_rows=len(out), rows=out)
    json.dump(doc, open(HERE / "quoted_results.json", "w", encoding="utf-8"), indent=1)
    md = HERE / "EVALUATORS.md"
    if md.exists():
        fill(md, {"counts": md_counts(out), "not_held_out": md_not_held(out), "pose_donor": md_pose(out),
                  "lineage": md_lineage(), "scripts": md_scripts()})
    print(md_counts(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
