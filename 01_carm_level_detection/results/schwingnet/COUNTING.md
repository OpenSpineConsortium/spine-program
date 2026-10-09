# Counting from the sacrum on real C-arm frames

The product is detection plus COUNTING from the anchor. A level is an ordinal from the sacrum; a name follows by convention (ordinal 1 = L5 in a five-lumbar spine) and where it does not (L6, T13) the ordinal is still the answer. Nothing here uses a level classifier.

## Definition

- **Detected side.** The detected sacrum (the highest-confidence sacrum box at the stated confidence) is ordinal 0. Detected vertebral bodies are ordered along the spine axis (the principal direction of the box centres, sacrum included) moving away from the sacrum; the k-th body from the sacrum has ordinal k. A box on the sacrum's caudal side is not counted. The cranial side is the side holding more boxes; a tie goes to the side whose nearest box is nearer the sacrum.
- **Truth side.** The frame's labelled bodies (the YOLO label files under `realxray/<set>/labels/test`, denormalised with the meta's image size) ordered the same way from the truth sacrum; ordinal = rank among truth bodies. Name-free, so an L6 or T13 spine needs no special case. Ordering away from the sacrum needs no orientation flag: C-ArmLSpine AP and lateral frames of prone/supine patients and the DeepFluoro frames stored upside down are handled alike.
- **Matching.** One-to-one, greedy in descending confidence, each detection taking the unmatched truth box of highest IoU, a hit at IoU >= 0.5 (`tools/realxray_eval.sweep_matches`, the matching of the contribution matrix and `a1.json`; the wording "highest IoU first" in the task was read as this convention).
- **Score.** A matched truth body is counted correctly when its detection's ordinal equals its truth ordinal; within one when they differ by one. A missed body between the sacrum and a target shifts every ordinal above it, and so does a spurious box there: those are the counting errors measured. A truth body with no matched detection is missed.
- **Defined.** Counting is defined on a frame when truth has a sacrum and a sacrum was detected. When the sacrum is not in the frame, counting from that one frame is undefined; see the last section.
- **Truth convention.** C-ArmLSpine truth `box` is the vertebral body while every other device's truth is a whole-vertebra outline, so C-ArmLSpine is scored against the meta's `outline_box` (the convention of the contribution matrix), with the body reading kept beside it as a reference.
- **Intervals.** 2,000-resample bootstrap clustered by case (C-ArmLSpine case, DeepFluoro specimen, COBRA patient), percentile and BCa; one cluster gives no interval.

Tool: `tools/count_from_sacrum_eval.py` (`--self-test` builds synthetic frames: clean, one missed body, one spurious box, a caudal box, a flipped frame, a tilted frame, a sign tie, and asserts the ordinals). Runner: `SchwingNet/slurm/counting.sh`. This report: `SchwingNet/tools/counting_report.py`. Per-arm outputs with every frame's ordinals: `SchwingNet/results/counting/*.json`.

## Counting accuracy

Denominators, per cell: *defined* = frames with a truth sacrum whose sacrum was detected (share of frames with a truth sacrum); *anchor correct* = defined frames whose detected sacrum overlaps the truth sacrum at IoU >= 0.5; *matched* = truth bodies in defined frames matched to a detection; *ordinal correct* = matched bodies whose ordinals agree (percentile interval, then BCa); *per truth body* = every truth body in defined frames, split correct / one-off / off by more or unranked / missed, so recall and counting share one denominator; *all sacrum frames* = correct over every truth body in every frame that has a truth sacrum, a body in a frame whose sacrum went undetected counting as not counted (the strictest single number).

| arm (training) | target | status | conf | frames (no truth sacrum) | defined | anchor correct | matched | ordinal correct % [pct] [BCa] | within one % | frames all matched correct | frames exact | per truth body: correct / one-off / more / missed % | correct, all sacrum frames % | file |
|---|---|---|---:|---|---|---|---:|---|---|---|---|---|---|---|
| lodo_carm: real D+E frames only (C-ArmLSpine never seen) | C-ArmLSpine test (28 cases, AP + lateral) | DEVICE-HELD-OUT | 0.74 | 56 (0) | 46/56 = 82.1 [69.6, 92.9] | 93.5 [85.7, 100.0] | 197 | 95.4 [89.4, 99.5] [85.2, 98.9] | 100.0 [100.0, 100.0] | 41/46 = 89.1 [77.6, 98.0] | 20/46 = 43.5 [26.0, 60.9] | 232 bodies: 81.0 [73.8, 87.6] / 3.9 [0.4, 9.0] / 0.0 [0.0, 0.0] / 15.1 [10.0, 20.9] | 188/287 = 65.5 [53.7, 77.0] | `SchwingNet/results/counting/lodo_carm__carm_test__outline__0.74.json` |
| lodo_carm: real D+E frames only (C-ArmLSpine never seen) | C-ArmLSpine test (28 cases, AP + lateral) | DEVICE-HELD-OUT | 0.25 | 56 (0) | 51/56 = 91.1 [83.9, 96.4] | 92.2 [84.0, 98.1] | 235 | 84.7 [77.4, 90.7] [76.5, 90.4] | 95.7 [92.2, 98.7] | 36/50 = 72.0 [61.2, 82.2] | 24/51 = 47.1 [31.4, 61.2] | 259 bodies: 76.8 [68.3, 83.8] / 10.0 [5.9, 14.8] / 3.9 [1.2, 7.1] / 9.3 [4.6, 15.3] | 199/287 = 69.3 [57.6, 79.8] | `SchwingNet/results/counting/lodo_carm__carm_test__outline__0.25.json` |
| dc_A_held_surgio_b51_dr: design A: styled + real D+E (one pose pool for every card), seed 0 | C-ArmLSpine test (28 cases, AP + lateral) | DEVICE-HELD-OUT | 0.25 | 56 (0) | 46/56 = 82.1 [73.2, 91.1] | 97.8 [92.7, 100.0] | 206 | 78.6 [67.1, 88.4] [65.3, 87.4] | 96.6 [93.1, 99.5] | 30/45 = 66.7 [52.9, 79.6] | 17/46 = 37.0 [21.4, 52.2] | 234 bodies: 69.2 [58.5, 78.5] / 15.8 [7.6, 26.0] / 3.0 [0.5, 6.1] / 12.0 [6.9, 18.8] | 162/287 = 56.4 [44.1, 67.8] | `SchwingNet/results/counting/dc_A_held_surgio_b51_dr__carm_test__outline__0.25.json` |
| dc_A_held_surgio_b51_dr_s1: design A: styled + real D+E (one pose pool for every card), seed 1 | C-ArmLSpine test (28 cases, AP + lateral) | DEVICE-HELD-OUT | 0.25 | 56 (0) | 47/56 = 83.9 [75.0, 91.1] | 97.9 [93.3, 100.0] | 197 | 65.5 [58.0, 71.9] [57.6, 71.7] | 83.8 [77.4, 89.4] | 16/45 = 35.6 [25.0, 44.7] | 11/47 = 23.4 [13.7, 32.6] | 238 bodies: 54.2 [44.5, 62.4] / 15.1 [12.0, 18.6] / 13.4 [8.8, 18.7] / 17.2 [10.2, 25.4] | 129/287 = 44.9 [34.7, 54.9] | `SchwingNet/results/counting/dc_A_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` |
| dc_B_held_surgio_b51_dr_s1: design B: styled + real D+E (each device's own poses), seed 1 | C-ArmLSpine test (28 cases, AP + lateral) | DEVICE-HELD-OUT | 0.25 | 56 (0) | 50/56 = 89.3 [82.1, 96.4] | 96.0 [90.0, 100.0] | 225 | 64.9 [58.1, 72.1] [58.1, 72.2] | 84.4 [77.1, 91.1] | 20/49 = 40.8 [30.0, 52.2] | 9/50 = 18.0 [8.5, 28.3] | 256 bodies: 57.0 [50.8, 63.5] / 17.2 [11.9, 22.4] / 13.7 [7.7, 20.6] / 12.1 [6.3, 18.8] | 146/287 = 50.9 [43.7, 57.9] | `SchwingNet/results/counting/dc_B_held_surgio_b51_dr_s1__carm_test__outline__0.25.json` |
| pooled: real D+S+E frames (in-training device; a body-box detector scored against OUTLINE truth, so it matches 117 of 287 bodies, recall 40.8 %, and its 100 % is over those 117 only) | C-ArmLSpine test (28 cases, AP + lateral) | in-training-device (reference) | 0.25 | 56 (0) | 56/56 = 100.0 [100.0, 100.0] | 98.2 [94.6, 100.0] | 117 | 100.0 [100.0, 100.0]  | 100.0 [100.0, 100.0] | 31/31 = 100.0 [100.0, 100.0] | 4/56 = 7.1 [1.8, 14.3] | 287 bodies: 40.8 [38.4, 42.9] / 0.0 [0.0, 0.0] / 0.0 [0.0, 0.0] / 59.2 [57.1, 61.6] | 117/287 = 40.8 [38.4, 42.9] | `SchwingNet/results/counting/pooled__carm_test__outline__0.25.json` |
| lodo_carm: real D+E frames only (C-ArmLSpine never seen) | C-ArmLSpine test (28 cases, AP + lateral) (body truth, reference) | DEVICE-HELD-OUT | 0.74 | 56 (0) | 46/56 = 82.1 [69.6, 92.9] | 93.5 [85.7, 100.0] | 14 | 92.9 [75.0, 100.0] [42.9, 100.0] | 100.0 [100.0, 100.0] | 8/9 = 88.9 [66.7, 100.0] | 0/46 = 0.0 [0.0, 0.0] | 232 bodies: 5.6 [2.3, 9.6] / 0.4 [0.0, 1.4] / 0.0 [0.0, 0.0] / 94.0 [90.0, 97.3] | 13/287 = 4.5 [2.0, 7.8] | `SchwingNet/results/counting/lodo_carm__carm_test__body__0.74.json` |
| lodo_carm: real D+E frames only (C-ArmLSpine never seen) | C-ArmLSpine test (28 cases, AP + lateral) (body truth, reference) | DEVICE-HELD-OUT | 0.25 | 56 (0) | 51/56 = 91.1 [83.9, 96.4] | 92.2 [84.0, 98.1] | 14 | 78.6 [44.4, 100.0] [36.4, 100.0] | 100.0 [100.0, 100.0] | 7/9 = 77.8 [44.4, 100.0] | 0/51 = 0.0 [0.0, 0.0] | 259 bodies: 4.2 [1.6, 7.4] / 1.2 [0.0, 3.1] / 0.0 [0.0, 0.0] / 94.6 [91.1, 97.5] | 11/287 = 3.8 [1.4, 6.8] | `SchwingNet/results/counting/lodo_carm__carm_test__body__0.25.json` |
| lodo_df: real S+E frames only (DeepFluoro never seen) | DeepFluoro test (specimen 18-1109) | DEVICE-HELD-OUT | 0.25 | 104 (14) | 90/90 = 100.0 (1 cluster) | 100.0 (1 cluster) | 67 | 79.1 (1 cluster)  | 100.0 (1 cluster) | 49/63 = 77.8 (1 cluster) | 46/63 = 73.0 (1 cluster) | 71 bodies: 74.6 (1 cluster) / 19.7 (1 cluster) / 0.0 (1 cluster) / 5.6 (1 cluster) | 53/71 = 74.6 (1 cluster) | `SchwingNet/results/counting/lodo_df__df_test__body__0.25.json` |
| dc_A_held_cios_fusion: design A: styled + real S+E (one pose pool for every card), seed 0 | DeepFluoro test (specimen 18-1109) | DEVICE-HELD-OUT | 0.25 | 104 (14) | 90/90 = 100.0 (1 cluster) | 100.0 (1 cluster) | 64 | 98.4 (1 cluster)  | 100.0 (1 cluster) | 58/59 = 98.3 (1 cluster) | 55/63 = 87.3 (1 cluster) | 71 bodies: 88.7 (1 cluster) / 1.4 (1 cluster) / 0.0 (1 cluster) / 9.9 (1 cluster) | 63/71 = 88.7 (1 cluster) | `SchwingNet/results/counting/dc_A_held_cios_fusion__df_test__body__0.25.json` |
| dc_A_held_cios_fusion_s1: design A: styled + real S+E (one pose pool for every card), seed 1 | DeepFluoro test (specimen 18-1109) | DEVICE-HELD-OUT | 0.25 | 104 (14) | 90/90 = 100.0 (1 cluster) | 98.9 (1 cluster) | 66 | 56.1 (1 cluster)  | 98.5 (1 cluster) | 35/63 = 55.6 (1 cluster) | 30/63 = 47.6 (1 cluster) | 71 bodies: 52.1 (1 cluster) / 39.4 (1 cluster) / 1.4 (1 cluster) / 7.0 (1 cluster) | 37/71 = 52.1 (1 cluster) | `SchwingNet/results/counting/dc_A_held_cios_fusion_s1__df_test__body__0.25.json` |
| dc_B_held_cios_fusion: design B: styled + real S+E (each device's own poses), seed 0 | DeepFluoro test (specimen 18-1109) | DEVICE-HELD-OUT | 0.25 | 104 (14) | 90/90 = 100.0 (1 cluster) | 100.0 (1 cluster) | 67 | 88.1 (1 cluster)  | 100.0 (1 cluster) | 51/59 = 86.4 (1 cluster) | 51/63 = 81.0 (1 cluster) | 71 bodies: 83.1 (1 cluster) / 11.3 (1 cluster) / 0.0 (1 cluster) / 5.6 (1 cluster) | 59/71 = 83.1 (1 cluster) | `SchwingNet/results/counting/dc_B_held_cios_fusion__df_test__body__0.25.json` |
| dc_B_held_cios_fusion_s1: design B: styled + real S+E (each device's own poses), seed 1 | DeepFluoro test (specimen 18-1109) | DEVICE-HELD-OUT | 0.25 | 104 (14) | 90/90 = 100.0 (1 cluster) | 100.0 (1 cluster) | 66 | 51.5 (1 cluster)  | 100.0 (1 cluster) | 32/58 = 55.2 (1 cluster) | 32/63 = 50.8 (1 cluster) | 71 bodies: 47.9 (1 cluster) / 45.1 (1 cluster) / 0.0 (1 cluster) / 7.0 (1 cluster) | 34/71 = 47.9 (1 cluster) | `SchwingNet/results/counting/dc_B_held_cios_fusion_s1__df_test__body__0.25.json` |
| dc_A_held_cios_fusion: design A: styled + real S+E (one pose pool for every card), seed 0 | DeepFluoro, all six specimens | DEVICE-HELD-OUT | 0.25 | 366 (28) | 333/338 = 98.5 [94.5, 100.0] | 94.3 [76.3, 100.0] | 292 | 90.4 [71.0, 98.8] [56.4, 98.1] | 100.0 [100.0, 100.0] | 221/248 = 89.1 [65.8, 98.6] | 173/278 = 62.2 [39.4, 81.9] | 407 bodies: 64.9 [41.3, 83.3] / 6.9 [0.9, 18.0] / 0.0 [0.0, 0.0] / 28.3 [15.0, 40.8] | 264/416 = 63.5 [38.8, 83.3] | `SchwingNet/results/counting/dc_A_held_cios_fusion__df_all6__body__0.25.json` |
| dc_A_held_cios_fusion_s1: design A: styled + real S+E (one pose pool for every card), seed 1 | DeepFluoro, all six specimens | DEVICE-HELD-OUT | 0.25 | 366 (28) | 332/338 = 98.2 [94.1, 100.0] | 95.5 [81.2, 99.8] | 321 | 79.8 [59.6, 93.5] [60.0, 93.5] | 99.4 [98.5, 100.0] | 205/265 = 77.4 [56.4, 93.1] | 156/278 = 56.1 [34.9, 71.1] | 410 bodies: 62.4 [42.1, 77.0] / 15.4 [5.4, 29.4] / 0.5 [0.0, 1.1] / 21.7 [11.7, 34.1] | 256/416 = 61.5 [40.8, 76.5] | `SchwingNet/results/counting/dc_A_held_cios_fusion_s1__df_all6__body__0.25.json` |
| dc_B_held_cios_fusion: design B: styled + real S+E (each device's own poses), seed 0 | DeepFluoro, all six specimens | DEVICE-HELD-OUT | 0.25 | 366 (28) | 336/338 = 99.4 [98.7, 100.0] | 95.5 [78.9, 100.0] | 327 | 89.0 [80.5, 95.4] [79.4, 95.0] | 100.0 [100.0, 100.0] | 235/270 = 87.0 [75.6, 94.4] | 183/283 = 64.7 [47.5, 83.6] | 416 bodies: 70.0 [58.6, 85.5] / 8.7 [3.7, 15.0] / 0.0 [0.0, 0.0] / 21.4 [7.9, 30.6] | 291/416 = 70.0 [58.6, 85.5] | `SchwingNet/results/counting/dc_B_held_cios_fusion__df_all6__body__0.25.json` |
| dc_B_held_cios_fusion_s1: design B: styled + real S+E (each device's own poses), seed 1 | DeepFluoro, all six specimens | DEVICE-HELD-OUT | 0.25 | 366 (28) | 335/338 = 99.1 [97.7, 100.0] | 94.9 [79.4, 100.0] | 311 | 75.2 [59.8, 86.9] [58.3, 86.0] | 99.4 [98.1, 100.0] | 196/267 = 73.4 [57.7, 84.8] | 139/281 = 49.5 [35.7, 70.3] | 414 bodies: 56.5 [46.9, 73.0] / 18.1 [9.3, 32.0] / 0.5 [0.0, 1.5] / 24.9 [9.9, 36.0] | 234/416 = 56.2 [46.4, 73.0] | `SchwingNet/results/counting/dc_B_held_cios_fusion_s1__df_all6__body__0.25.json` |
| lodo_cobra: real D+S frames only (COBRA never seen) | COBRA Elekta XVI test (27 patients) | DEVICE-HELD-OUT | 0.25 | 648 (39) | 111/609 = 18.2 [13.4, 23.5] | 73.0 [57.3, 84.6] | 76 | 71.1 [56.6, 80.3] [57.7, 80.6] | 97.4 [92.3, 100.0] | 37/54 = 68.5 [54.1, 79.4] | 33/91 = 36.3 [24.7, 46.7] | 149 bodies: 36.2 [23.4, 46.3] / 13.4 [8.9, 18.8] / 1.3 [0.0, 3.4] / 49.0 [39.7, 61.0] | 54/847 = 6.4 [3.3, 9.4] | `SchwingNet/results/counting/lodo_cobra__cobra_test__body__0.25.json` |
| dc_A_held_elekta_xvi: design A: styled + real D+S (one pose pool for every card), seed 0 | COBRA Elekta XVI test (27 patients) | DEVICE-HELD-OUT | 0.25 | 648 (39) | 280/609 = 46.0 [41.8, 50.0] | 74.3 [64.9, 82.6] | 240 | 66.2 [57.4, 74.9] [57.5, 75.0] | 96.7 [94.8, 98.7] | 111/180 = 61.7 [50.6, 71.7] | 90/248 = 36.3 [27.1, 45.7] | 400 bodies: 39.8 [31.6, 48.5] / 18.2 [13.9, 22.3] / 2.0 [0.7, 3.3] / 40.0 [32.5, 47.5] | 159/847 = 18.8 [14.9, 22.8] | `SchwingNet/results/counting/dc_A_held_elekta_xvi__cobra_test__body__0.25.json` |
| dc_A_held_elekta_xvi_s1: design A: styled + real D+S (one pose pool for every card), seed 1 | COBRA Elekta XVI test (27 patients) | DEVICE-HELD-OUT | 0.25 | 648 (39) | 237/609 = 38.9 [35.2, 42.4] | 75.9 [64.8, 86.0] | 232 | 74.1 [67.5, 80.7] [66.8, 80.2] | 97.0 [94.7, 98.9] | 118/167 = 70.7 [61.8, 79.3] | 95/209 = 45.5 [35.6, 55.4] | 338 bodies: 50.9 [42.8, 58.8] / 15.7 [10.9, 20.7] / 2.1 [0.7, 3.6] / 31.4 [23.3, 40.9] | 172/847 = 20.3 [16.2, 24.2] | `SchwingNet/results/counting/dc_A_held_elekta_xvi_s1__cobra_test__body__0.25.json` |
| dc_B_held_elekta_xvi: design B: styled + real D+S (each device's own poses), seed 0 | COBRA Elekta XVI test (27 patients) | DEVICE-HELD-OUT | 0.25 | 648 (39) | 278/609 = 45.6 [40.9, 50.0] | 77.7 [68.4, 85.4] | 242 | 64.9 [56.5, 73.8] [56.1, 73.1] | 93.0 [87.3, 97.9] | 111/174 = 63.8 [53.7, 73.7] | 79/245 = 32.2 [23.0, 42.2] | 405 bodies: 38.8 [33.3, 45.2] / 16.8 [11.4, 23.2] / 4.2 [1.3, 7.4] / 40.2 [34.2, 46.9] | 157/847 = 18.5 [15.5, 21.6] | `SchwingNet/results/counting/dc_B_held_elekta_xvi__cobra_test__body__0.25.json` |

Sources per cell (the raw per-frame dumps the ordinals were computed from):

- lodo_carm / carm_test / outline / conf 0.74: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- lodo_carm / carm_test / outline / conf 0.25: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- dc_A_held_surgio_b51_dr / carm_test / outline / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/eval_carmlspine_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- dc_A_held_surgio_b51_dr_s1 / carm_test / outline / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_s1/eval_carmlspine_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- dc_B_held_surgio_b51_dr_s1 / carm_test / outline / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_surgio_b51_dr_s1/eval_carmlspine_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- pooled / carm_test / outline / conf 0.25: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/pooled__carm_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 258/258
- lodo_carm / carm_test / body / conf 0.74: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 254/258
- lodo_carm / carm_test / body / conf 0.25: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json`; label files `56` frames, label-vs-dump boxes mismatched 0, truth-order name check 254/258
- lodo_df / df_test / body / conf 0.25: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_df__df_test.json`; label files `104` frames, label-vs-dump boxes mismatched 0, truth-order name check 71/71
- dc_A_held_cios_fusion / df_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_test.json`; label files `104` frames, label-vs-dump boxes mismatched 0, truth-order name check 71/71
- dc_A_held_cios_fusion_s1 / df_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_test.json`; label files `104` frames, label-vs-dump boxes mismatched 0, truth-order name check 71/71
- dc_B_held_cios_fusion / df_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_test.json`; label files `104` frames, label-vs-dump boxes mismatched 0, truth-order name check 71/71
- dc_B_held_cios_fusion_s1 / df_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_test.json`; label files `104` frames, label-vs-dump boxes mismatched 0, truth-order name check 71/71
- dc_A_held_cios_fusion / df_all6 / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_train.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_val.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_test.json`; label files `366` frames, label-vs-dump boxes mismatched 0, truth-order name check 318/318
- dc_A_held_cios_fusion_s1 / df_all6 / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_train.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_val.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_test.json`; label files `366` frames, label-vs-dump boxes mismatched 0, truth-order name check 318/318
- dc_B_held_cios_fusion / df_all6 / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_train.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_val.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_test.json`; label files `366` frames, label-vs-dump boxes mismatched 0, truth-order name check 318/318
- dc_B_held_cios_fusion_s1 / df_all6 / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_train.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_val.json`, `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_test.json`; label files `366` frames, label-vs-dump boxes mismatched 0, truth-order name check 318/318
- lodo_cobra / cobra_test / body / conf 0.25: `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_cobra__cobra_test.json`; label files `648` frames, label-vs-dump boxes mismatched 0, truth-order name check 829/829
- dc_A_held_elekta_xvi / cobra_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/eval_cobra_elekta_test.json`; label files `648` frames, label-vs-dump boxes mismatched 0, truth-order name check 829/829
- dc_A_held_elekta_xvi_s1 / cobra_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_s1/eval_cobra_elekta_test.json`; label files `648` frames, label-vs-dump boxes mismatched 0, truth-order name check 829/829
- dc_B_held_elekta_xvi / cobra_test / body / conf 0.25: `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_elekta_xvi/eval_cobra_elekta_test.json`; label files `648` frames, label-vs-dump boxes mismatched 0, truth-order name check 829/829

## Pooled across the held-out devices

One held-out cell per device (C-ArmLSpine test, DeepFluoro test, COBRA test) pooled over all their cases with the same case-cluster bootstrap; the DeepFluoro test split is one specimen, so it contributes one cluster of the total. A family with a member not on disk is not pooled.

| family | conf | frames (no truth sacrum) | clusters | defined | matched | ordinal correct % [pct] [BCa] | within one % | frames all matched correct | per truth body correct % / missed % | correct, all sacrum frames % | files |
|---|---:|---|---:|---|---:|---|---|---|---|---|---|
| real-only LODO arms, each on its held-out device (lodo_carm on S, lodo_df on D, lodo_cobra on E) | 0.25 | 808 (53) | 56 | 252/755 = 33.4 [20.4, 50.5] | 378 | 81.0 [75.7, 85.8] [75.7, 85.8] | 96.8 [93.8, 98.8] | 122/167 = 73.1 [62.7, 78.2] | 479 bodies: 63.9 [55.1, 71.3] / 21.1 [14.0, 29.6] | 306/1205 = 25.4 [17.0, 37.0] | `SchwingNet/results/counting/lodo_carm__carm_test__outline__0.25.json`, `SchwingNet/results/counting/lodo_df__df_test__body__0.25.json`, `SchwingNet/results/counting/lodo_cobra__cobra_test__body__0.25.json` |
| design A seed 0, each on its held-out device | 0.25 | 808 (53) | 56 | 416/755 = 55.1 [46.2, 66.4] | 510 | 75.3 [66.7, 82.9] [67.8, 84.2] | 97.1 [95.0, 98.6] | 199/284 = 70.1 [55.7, 81.4] | 705 bodies: 54.5 [44.7, 64.5] / 27.7 [20.4, 35.0] | 384/1205 = 31.9 [24.2, 42.6] | `SchwingNet/results/counting/dc_A_held_surgio_b51_dr__carm_test__outline__0.25.json`, `SchwingNet/results/counting/dc_A_held_cios_fusion__df_test__body__0.25.json`, `SchwingNet/results/counting/dc_A_held_elekta_xvi__cobra_test__body__0.25.json` |
| design A seed 1, each on its held-out device | 0.25 | 808 (53) | 56 | 374/755 = 49.5 [40.2, 62.1] | 495 | 68.3 [63.4, 73.8] [62.9, 73.4] | 91.9 [87.8, 94.8] | 169/275 = 61.5 [54.9, 68.8] | 647 bodies: 52.2 [46.3, 57.5] / 23.5 [17.4, 30.6] | 338/1205 = 28.0 [22.9, 34.4] | `SchwingNet/results/counting/dc_A_held_surgio_b51_dr_s1__carm_test__outline__0.25.json`, `SchwingNet/results/counting/dc_A_held_cios_fusion_s1__df_test__body__0.25.json`, `SchwingNet/results/counting/dc_A_held_elekta_xvi_s1__cobra_test__body__0.25.json` |
| design B seed 0, each on its held-out device | 0.25 | incomplete: dc_B_held_surgio_b51_dr/carm_test/outline/0.25 | | | | | | | | | |
| design B seed 1, each on its held-out device | 0.25 | incomplete: dc_B_held_elekta_xvi_s1/cobra_test/body/0.25 | | | | | | | | | |

## Where counting fails: by truth ordinal from the sacrum

Truth bodies in defined frames, by their ordinal (1 = the body next to the sacrum). No interval: a breakdown, not a headline.

**lodo_carm on C-ArmLSpine test (28 cases, AP + lateral), conf 0.74**

| ordinal | n | correct | one-off | off by more | unranked | missed | correct % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 46 | 44 | 1 | 0 | 0 | 1 | 95.7 |
| 2 | 46 | 44 | 1 | 0 | 0 | 1 | 95.7 |
| 3 | 46 | 41 | 2 | 0 | 0 | 3 | 89.1 |
| 4 | 46 | 38 | 3 | 0 | 0 | 5 | 82.6 |
| 5 | 41 | 21 | 2 | 0 | 0 | 18 | 51.2 |
| 6 | 7 | 0 | 0 | 0 | 0 | 7 | 0.0 |

By view / angle from AP: AP: 24 frames, ordinal correct 93.2 % of 103 matched, 79.3 % of 121 truth bodies; LAT: 22 frames, ordinal correct 97.9 % of 94 matched, 82.9 % of 111 truth bodies

**lodo_carm on C-ArmLSpine test (28 cases, AP + lateral), conf 0.25**

| ordinal | n | correct | one-off | off by more | unranked | missed | correct % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 51 | 46 | 3 | 0 | 0 | 2 | 90.2 |
| 2 | 51 | 46 | 4 | 0 | 0 | 1 | 90.2 |
| 3 | 51 | 44 | 4 | 2 | 0 | 1 | 86.3 |
| 4 | 51 | 38 | 7 | 5 | 0 | 1 | 74.5 |
| 5 | 46 | 25 | 7 | 3 | 0 | 11 | 54.3 |
| 6 | 9 | 0 | 1 | 0 | 0 | 8 | 0.0 |

By view / angle from AP: AP: 27 frames, ordinal correct 78.7 % of 127 matched, 73.0 % of 137 truth bodies; LAT: 24 frames, ordinal correct 91.7 % of 108 matched, 81.1 % of 122 truth bodies

**dc_A_held_surgio_b51_dr on C-ArmLSpine test (28 cases, AP + lateral), conf 0.25**

| ordinal | n | correct | one-off | off by more | unranked | missed | correct % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 46 | 40 | 4 | 0 | 0 | 2 | 87.0 |
| 2 | 46 | 39 | 5 | 0 | 0 | 2 | 84.8 |
| 3 | 46 | 34 | 10 | 1 | 0 | 1 | 73.9 |
| 4 | 46 | 31 | 10 | 3 | 0 | 2 | 67.4 |
| 5 | 42 | 18 | 7 | 3 | 0 | 14 | 42.9 |
| 6 | 8 | 0 | 1 | 0 | 0 | 7 | 0.0 |

By view / angle from AP: AP: 27 frames, ordinal correct 70.7 % of 123 matched, 63.5 % of 137 truth bodies; LAT: 19 frames, ordinal correct 90.4 % of 83 matched, 77.3 % of 97 truth bodies

**dc_A_held_surgio_b51_dr_s1 on C-ArmLSpine test (28 cases, AP + lateral), conf 0.25**

| ordinal | n | correct | one-off | off by more | unranked | missed | correct % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 47 | 41 | 2 | 0 | 0 | 4 | 87.2 |
| 2 | 47 | 39 | 4 | 1 | 0 | 3 | 83.0 |
| 3 | 47 | 23 | 17 | 4 | 0 | 3 | 48.9 |
| 4 | 47 | 16 | 7 | 16 | 0 | 8 | 34.0 |
| 5 | 42 | 10 | 6 | 11 | 0 | 15 | 23.8 |
| 6 | 8 | 0 | 0 | 0 | 0 | 8 | 0.0 |

By view / angle from AP: AP: 28 frames, ordinal correct 48.8 % of 121 matched, 41.3 % of 143 truth bodies; LAT: 19 frames, ordinal correct 92.1 % of 76 matched, 73.7 % of 95 truth bodies

**dc_B_held_surgio_b51_dr_s1 on C-ArmLSpine test (28 cases, AP + lateral), conf 0.25**

| ordinal | n | correct | one-off | off by more | unranked | missed | correct % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 50 | 44 | 1 | 1 | 0 | 4 | 88.0 |
| 2 | 50 | 42 | 3 | 4 | 0 | 1 | 84.0 |
| 3 | 50 | 26 | 17 | 6 | 0 | 1 | 52.0 |
| 4 | 50 | 21 | 13 | 13 | 0 | 3 | 42.0 |
| 5 | 45 | 13 | 10 | 9 | 0 | 13 | 28.9 |
| 6 | 11 | 0 | 0 | 2 | 0 | 9 | 0.0 |

By view / angle from AP: AP: 28 frames, ordinal correct 57.6 % of 132 matched, 53.1 % of 143 truth bodies; LAT: 22 frames, ordinal correct 75.3 % of 93 matched, 61.9 % of 113 truth bodies

## Worked example

Frame `case100_AP` (lodo_carm, confidence 0.74, outline truth; file `SchwingNet/results/counting/lodo_carm__carm_test__outline__0.74.json`).

Truth, ordered away from the truth sacrum (ordinal 0). The level name is shown only so the reader can check the ordering; it plays no part in the score.

| truth ordinal | level | box (x0, y0, x1, y1) | distance from sacrum centre along the axis (px) |
|---:|---|---|---:|
| 1 | L5 | (337.6, 622.3, 706.1, 795.8) | 179.2 |
| 2 | L4 | (401.7, 464.5, 650.6, 643.9) | 333.7 |
| 3 | L3 | (384.0, 289.5, 647.5, 493.8) | 496.6 |
| 4 | L2 | (392.7, 110.5, 622.7, 323.0) | 671.6 |
| 5 | L1 | (385.2, 4.2, 582.1, 145.4) | 814.5 |

Detected sacrum: box (257.6, 768.2, 844.1, 1024.0), confidence 0.8093, IoU with the truth sacrum 0.853.

Detections, ordered away from the detected sacrum:

| detected ordinal | confidence | box | matched truth ordinal | IoU | counted |
|---:|---:|---|---:|---:|---|
| 1 | 0.7809 | (353.6, 609.3, 705.6, 831.8) | 1 | 0.752 | correct |
| 2 | 0.8758 | (387.8, 455.1, 673.6, 662.5) | 2 | 0.753 | correct |
| 3 | 0.8435 | (382.2, 283.4, 664.9, 507.6) | 3 | 0.849 | correct |
| 4 | 0.8182 | (371.8, 107.8, 646.5, 341.4) | 4 | 0.762 | correct |
| 5 | 0.8551 | (364.1, 0.0, 619.6, 163.7) | 5 | 0.665 | correct |

Result: 5 of 5 truth bodies matched, 5 counted correctly, 0 within one, 0 missed; per truth body from ordinal 1 upward: correct, correct, correct, correct, correct. Frame exact: True.

Drawn: `SchwingNet/results/counting_example_case100_AP.png` (blue = truth ordinals from the truth sacrum, red = detections with their ordinal from the detected sacrum, orange = detected sacrum).

### A counting error, for contrast

Frame `case139_AP` (lodo_carm, confidence 0.74, outline truth; file `SchwingNet/results/counting/lodo_carm__carm_test__outline__0.74.json`).

Truth, ordered away from the truth sacrum (ordinal 0). The level name is shown only so the reader can check the ordering; it plays no part in the score.

| truth ordinal | level | box (x0, y0, x1, y1) | distance from sacrum centre along the axis (px) |
|---:|---|---|---:|
| 1 | L5 | (414.9, 540.3, 683.0, 718.1) | 219.8 |
| 2 | L4 | (424.8, 387.6, 663.9, 550.5) | 380.0 |
| 3 | L3 | (419.7, 226.6, 641.7, 411.7) | 530.4 |
| 4 | L2 | (418.8, 59.8, 635.3, 241.4) | 698.9 |
| 5 | L1 | (423.1, 2.0, 594.0, 94.9) | 801.9 |

Detected sacrum: box (291.7, 734.1, 837.6, 1024.0), confidence 0.8904, IoU with the truth sacrum 0.727.

Detections, ordered away from the detected sacrum:

| detected ordinal | confidence | box | matched truth ordinal | IoU | counted |
|---:|---:|---|---:|---:|---|
| 1 | 0.7457 | (352.1, 643.1, 748.5, 881.4) | - | - | no truth box (spurious) |
| 2 | 0.8532 | (389.7, 522.2, 704.2, 723.7) | 1 | 0.752 | within one |
| 3 | 0.891 | (395.5, 381.3, 681.1, 579.2) | 2 | 0.689 | within one |
| 4 | 0.878 | (395.9, 213.6, 672.3, 435.4) | 3 | 0.67 | within one |
| 5 | 0.8433 | (396.3, 50.3, 653.8, 265.6) | 4 | 0.709 | within one |
| 6 | 0.8061 | (411.3, 0.0, 642.7, 108.9) | 5 | 0.63 | within one |

Result: 5 of 5 truth bodies matched, 0 counted correctly, 5 within one, 0 missed; per truth body from ordinal 1 upward: one_off, one_off, one_off, one_off, one_off. Frame exact: False.

Drawn: `SchwingNet/results/counting_example_case139_AP.png`.

## Truth notes

- The C-ArmLSpine label builder (`tools/carmlspine_labels.py`, `build_case`) loops over TotalSegmentator vertebrae and attaches the SPINEPS body of whatever name the level map assigns; when TS and SPINEPS disagree by one level the same SPINEPS body box is written twice under two TS names (15 such pairs in 13 of the 56 test frames, centres < 2 px apart), while the two `outline_box` entries remain distinct TS vertebrae. Under the outline convention the truth ordering is therefore physically right (name check 258/258 and the rendered frames case10_AP, case133_AP agree); under the body convention the duplicated body boxes sit at one height and the order between them is arbitrary (name check 254/258). That is one more reason the body reading is a reference only.
- A TS vertebra cut by the field edge (visible fraction just above the 0.5 keep threshold, a sliver of ~30 px) is a truth body at the top ordinal that no detection can match; it counts as missed there, which lowers recall at the top ordinal but shifts nothing below it.
- Frames without a truth sacrum: counting is undefined and they are excluded from every denominator except `frames`; the count is in the table (DeepFluoro test 14 of 104, COBRA test 39 of 648, C-ArmLSpine test 0 of 56).
- The dumps' own truth rows were checked against the label files box by box (IoU >= 0.9, same count per class): mismatches are listed per cell above (all zero when this was written).
- Most one-off errors at ordinal 1 come from an unmatched box between the sacrum centre and the first body: on DeepFluoro at confidence 0.25 these boxes carry confidence 0.29 to 0.47 (they would not survive the 0.74 operating point), on C-ArmLSpine case139_AP one carries 0.75. They sit where the S1 body is; that reading was checked on the rendered C-ArmLSpine frame, not on DeepFluoro.

## Outside check

`SchwingNet/tools/counting_outside_check.py` re-implements the matching and re-derives the ordinals by a different rule, importing nothing from the counting tool; result `SchwingNet/results/counting_outside_check.json`, all pass.
- conf 0.25: greedy IoU >= 0.5 matches over all frames 260/287 against `a1.json` `conf_0.25_as_quoted` k = 260/287; matches in defined frames 235 (cell: 235) + in undefined frames 25 = 260; per-body verdict under Euclidean-distance ordering vs the cell's SVD-axis ordering: 259 agree, 0 differ: PASS.
- conf 0.74: greedy IoU >= 0.5 matches over all frames 231/287 against `a1.json` `cross_device_0.74` k = 231/287; matches in defined frames 197 (cell: 197) + in undefined frames 34 = 231; per-body verdict under Euclidean-distance ordering vs the cell's SVD-axis ordering: 232 agree, 0 differ: PASS.

## Operating points

- 0.74 is the LODO arm's cross-device operating point (best pooled vertebra F1 on its OTHER-device sweeps, chosen before looking at C-ArmLSpine; `SchwingNet/results/a1.json`, `cross_device_0.74`).
- 0.25 is the YOLO predict default, the point `scores.json`, the contribution matrix and the manuscript's device-held-out recall use; not chosen on any data.

## Pooled design P

- dc_P_pooled not scored: ~/spine-detector/runs/devcorpus/dc_P_pooled/scores.json was not on disk when this ran (Wed Sep 23 01:01:44 EDT 2026); job 40415009 state: RUNNING

## When the sacrum is not in the frame

Counting from one frame is then undefined: an ordinal needs the anchor in the same picture, and no frame-local rule can supply it (naming a body by its shape would be the 27-level classifier, which is not the product). The table reports how many frames have no truth sacrum and how many with a sacrum had none detected; both are outside the counting denominators, never scored as right. The product's answer for those frames is the level-map sweep: a short series of overlapping exposures from the sacrum to the level of interest, linked frame to frame, so every later spot image is placed on a map that contains the anchor (`docs/SWEEP_PROTOCOL.md`). Its measured results are on disk under the `lstv_*` ids of `docs/RSNAI_CLAIMS.json`, each with its file and JSON path; the recorded expectations are quoted here, not re-verified by this report:

- `lstv_runs`: runs per arm (18 CTSpinoPelvic1K spines with L6, 3 seeds): 54
- `lstv_clean_exact_chain`: clean frames: chains with exactly one node per body: 45
- `lstv_clean_l6`: clean frames: the instrument's exposure placed on the chain named L6: 36
- `lstv_film_exact_chain`: film noise model: chains with one node per body: 45
- `lstv_film_l6`: film noise model: the instrument's exposure named L6: 35

and the chain-completion numbers in `docs/SWEEP_PROTOCOL.md` (chains complete on 92 / 96 / 99 % of spines for a collimated / 9-inch / 12-inch field; linking only). That page's naming-on-the-sweep figures come from the 27-level model (`sweep_morph` / `sweep_hybrid`) and are not counting results; they are not quoted here.

