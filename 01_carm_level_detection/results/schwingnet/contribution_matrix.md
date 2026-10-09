# Contribution matrix: held-out device x training set

Every cell recomputed from per-frame raw predictions at confidence 0.25 and IoU 0.5; the interval is a 2000-resample case-cluster bootstrap (seed 0). C-ArmLSpine is scored under the outline convention (body beside it as a reference). `D` DeepFluoro / Cios Fusion, `S` C-ArmLSpine / Surgio-B51, `E` COBRA / Elekta XVI.

Self-check against scores.json: 85 cells, max |difference| 0.0000.

## Held-out cells (vertebra recall %, sacrum found %)

| training set | design | seed | target | frames | clusters | vertebra recall | sacrum found | file |
|---|---|---|---|---:|---:|---|---|---|
| A styled E + real E (`dc_A_held_cios_fusion_1dev_elekta_xvi`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 11.1 [7.3, 15.5] | 78.6 [67.9, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 22.4 / sacrum 89.3 (28 fr); LAT vert 0.0 / sacrum 67.9 (28 fr) | | | | | |
| A styled D + real D (`dc_A_held_elekta_xvi_1dev_cios_fusion`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 3.8 [1.4, 7.0] | 50.0 [50.0, 50.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_cios_fusion/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 2.1 / sacrum 100.0 (28 fr); LAT vert 5.6 / sacrum 0.0 (28 fr) | | | | | |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 21.6 [17.4, 26.0] | 80.4 [69.6, 91.1] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 42.7 / sacrum 96.4 (28 fr); LAT vert 0.7 / sacrum 64.3 (28 fr) | | | | | |
| A styled D + real D (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 3.8 [1.4, 7.0] | 50.0 [50.0, 50.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_cios_fusion/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 2.1 / sacrum 100.0 (28 fr); LAT vert 5.6 / sacrum 0.0 (28 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 11.1 [7.3, 15.5] | 78.6 [67.9, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 22.4 / sacrum 89.3 (28 fr); LAT vert 0.0 / sacrum 67.9 (28 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`) | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 3.1 [1.0, 5.8] | 37.5 [28.6, 46.4] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 6.3 / sacrum 71.4 (28 fr); LAT vert 0.0 / sacrum 3.6 (28 fr) | | | | | |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr_s1`) | A | 1 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 14.3 [9.3, 19.4] | 82.1 [73.2, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_s1/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 28.0 / sacrum 100.0 (28 fr); LAT vert 0.7 / sacrum 64.3 (28 fr) | | | | | |
| B styled D+E + real D+E (`dc_B_held_surgio_b51_dr_s1`) | B | 1 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 15.0 [11.0, 18.9] | 85.7 [76.8, 92.9] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_surgio_b51_dr_s1/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 30.1 / sacrum 100.0 (28 fr); LAT vert 0.0 / sacrum 71.4 (28 fr) | | | | | |
| real D+E (`lodo_carm`) | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 5.2 [2.4, 8.6] | 83.9 [73.2, 92.9] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json` |
| | | | by angle from AP: AP vert 9.8 / sacrum 96.4 (28 fr); LAT vert 0.7 / sacrum 71.4 (28 fr) | | | | | |
| renders only, no real frame (`render`) | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 2.4 [0.7, 4.5] | 53.6 [44.6, 62.5] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/render__carm_test.json` |
| | | | by angle from AP: AP vert 4.2 / sacrum 89.3 (28 fr); LAT vert 0.7 / sacrum 17.9 (28 fr) | | | | | |
| A styled E + real E (`dc_A_held_cios_fusion_1dev_elekta_xvi`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 86.8 [81.1, 91.8] | 78.6 [67.9, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 95.1 / sacrum 89.3 (28 fr); LAT vert 78.5 / sacrum 67.9 (28 fr) | | | | | |
| A styled D + real D (`dc_A_held_elekta_xvi_1dev_cios_fusion`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 12.9 [8.3, 18.1] | 50.0 [50.0, 50.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_cios_fusion/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 16.1 / sacrum 100.0 (28 fr); LAT vert 9.7 / sacrum 0.0 (28 fr) | | | | | |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 84.7 [77.7, 90.7] | 80.4 [69.6, 91.1] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 89.5 / sacrum 96.4 (28 fr); LAT vert 79.9 / sacrum 64.3 (28 fr) | | | | | |
| A styled D + real D (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 12.9 [8.3, 18.1] | 50.0 [50.0, 50.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_cios_fusion/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 16.1 / sacrum 100.0 (28 fr); LAT vert 9.7 / sacrum 0.0 (28 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 86.8 [81.1, 91.8] | 78.6 [67.9, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 95.1 / sacrum 89.3 (28 fr); LAT vert 78.5 / sacrum 67.9 (28 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`) | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 39.0 [33.2, 44.7] | 37.5 [28.6, 46.4] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 64.3 / sacrum 71.4 (28 fr); LAT vert 13.9 / sacrum 3.6 (28 fr) | | | | | |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr_s1`) | A | 1 | C-ArmLSpine test (outline truth) | 56 | 28 | 80.5 [72.5, 87.6] | 82.1 [73.2, 89.3] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_s1/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 84.6 / sacrum 100.0 (28 fr); LAT vert 76.4 / sacrum 64.3 (28 fr) | | | | | |
| B styled D+E + real D+E (`dc_B_held_surgio_b51_dr_s1`) | B | 1 | C-ArmLSpine test (outline truth) | 56 | 28 | 87.8 [81.7, 93.2] | 85.7 [76.8, 92.9] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_surgio_b51_dr_s1/eval_carmlspine_<split>.json` |
| | | | by angle from AP: AP vert 92.3 / sacrum 100.0 (28 fr); LAT vert 83.3 / sacrum 71.4 (28 fr) | | | | | |
| real D+E (`lodo_carm`) | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 90.6 [85.4, 95.2] | 83.9 [73.2, 92.9] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json` |
| | | | by angle from AP: AP vert 93.0 / sacrum 96.4 (28 fr); LAT vert 88.2 / sacrum 71.4 (28 fr) | | | | | |
| renders only, no real frame (`render`) | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 31.7 [27.1, 36.1] | 53.6 [44.6, 62.5] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/render__carm_test.json` |
| | | | by angle from AP: AP vert 57.3 / sacrum 89.3 (28 fr); LAT vert 6.2 / sacrum 17.9 (28 fr) | | | | | |
| A styled S + real S (`dc_A_held_cios_fusion_1dev_surgio_b51_dr`) | A | 0 | COBRA Elekta XVI test | 648 | 27 | 7.5 [3.5, 12.1] | 3.8 [1.8, 6.2] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_surgio_b51_dr/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 19.9 / sacrum 5.8 (208 fr); 30-60 vert 3.5 / sacrum 4.2 (202 fr); 60-90 vert 0.0 / sacrum 1.4 (238 fr) | | | | | |
| A styled D+S + real D+S (`dc_A_held_elekta_xvi`) | A | 0 | COBRA Elekta XVI test | 648 | 27 | 30.2 [26.3, 34.2] | 34.2 [29.6, 38.7] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 71.1 / sacrum 76.0 (208 fr); 30-60 vert 19.8 / sacrum 25.3 (202 fr); 60-90 vert 3.1 / sacrum 0.9 (238 fr) | | | | | |
| A styled D + real D (`dc_A_held_elekta_xvi_1dev_cios_fusion`) | A | 0 | COBRA Elekta XVI test | 648 | 27 | 38.1 [32.3, 44.5] | 40.6 [37.2, 44.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_cios_fusion/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 63.1 / sacrum 87.0 (208 fr); 30-60 vert 41.0 / sacrum 34.7 (202 fr); 60-90 vert 13.3 / sacrum 0.0 (238 fr) | | | | | |
| A styled S + real S (`dc_A_held_elekta_xvi_1dev_surgio_b51_dr`) | A | 0 | COBRA Elekta XVI test | 648 | 27 | 12.2 [8.0, 16.0] | 8.0 [5.3, 10.9] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_surgio_b51_dr/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 30.3 / sacrum 16.3 (208 fr); 30-60 vert 6.7 / sacrum 4.7 (202 fr); 60-90 vert 0.9 / sacrum 2.8 (238 fr) | | | | | |
| A styled D+S + real D+S (`dc_A_held_elekta_xvi_s1`) | A | 1 | COBRA Elekta XVI test | 648 | 27 | 31.4 [26.6, 35.4] | 29.9 [25.1, 34.5] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_s1/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 73.5 / sacrum 69.7 (208 fr); 30-60 vert 21.2 / sacrum 18.9 (202 fr); 60-90 vert 2.8 / sacrum 0.5 (238 fr) | | | | | |
| A styled D + real D (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`) | A | 0 | COBRA Elekta XVI test | 648 | 27 | 38.1 [32.3, 44.5] | 40.6 [37.2, 44.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_cios_fusion/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 63.1 / sacrum 87.0 (208 fr); 30-60 vert 41.0 / sacrum 34.7 (202 fr); 60-90 vert 13.3 / sacrum 0.0 (238 fr) | | | | | |
| B styled D+S + real D+S (`dc_B_held_elekta_xvi`) | B | 0 | COBRA Elekta XVI test | 648 | 27 | 32.7 [28.4, 36.2] | 36.5 [31.6, 40.9] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_elekta_xvi/eval_cobra_elekta_<split>.json` |
| | | | by angle from AP: 0-30 vert 69.3 / sacrum 76.9 (208 fr); 30-60 vert 31.1 / sacrum 26.8 (202 fr); 60-90 vert 1.5 / sacrum 5.2 (238 fr) | | | | | |
| real D+S (`lodo_cobra`) | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 18.5 [13.7, 22.8] | 13.3 [8.1, 18.8] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_cobra__cobra_test.json` |
| | | | by angle from AP: 0-30 vert 45.3 / sacrum 34.6 (208 fr); 30-60 vert 11.3 / sacrum 4.7 (202 fr); 60-90 vert 0.9 / sacrum 0.0 (238 fr) | | | | | |
| real S only (`only_carm`) | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 8.8 [5.0, 12.2] | 0.3 [0.0, 0.8] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm__cobra_test.json` |
| | | | by angle from AP: 0-30 vert 25.1 / sacrum 1.0 (208 fr); 30-60 vert 2.5 / sacrum 0.0 (202 fr); 60-90 vert 0.0 / sacrum 0.0 (238 fr) | | | | | |
| real S only (frames + crops) (`only_carm_multi`) | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 1.1 [0.0, 3.0] | 0.3 [0.0, 0.8] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm_multi__cobra_test.json` |
| | | | by angle from AP: 0-30 vert 3.1 / sacrum 0.5 (208 fr); 30-60 vert 0.0 / sacrum 0.5 (202 fr); 60-90 vert 0.3 / sacrum 0.0 (238 fr) | | | | | |
| renders only, no real frame (`render`) | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 37.8 [33.9, 42.1] | 30.9 [26.1, 35.7] | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/render__cobra_test.json` |
| | | | by angle from AP: 0-30 vert 67.2 / sacrum 70.7 (208 fr); 30-60 vert 39.9 / sacrum 21.6 (202 fr); 60-90 vert 9.9 / sacrum 0.0 (238 fr) | | | | | |
| A styled S+E + real S+E (`dc_A_held_cios_fusion`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 91.6 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 91.2 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| A styled E + real E (`dc_A_held_cios_fusion_1dev_elekta_xvi`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 92.8 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 92.5 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| A styled S + real S (`dc_A_held_cios_fusion_1dev_surgio_b51_dr`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 31.3 (1 cluster) | 6.7 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_surgio_b51_dr/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 31.2 / sacrum 6.2 (95 fr); 30-60 vert 33.3 / sacrum 11.1 (9 fr) | | | | | |
| A styled S+E + real S+E (`dc_A_held_cios_fusion_s1`) | A | 1 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 91.6 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 91.2 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| A styled S + real S (`dc_A_held_elekta_xvi_1dev_surgio_b51_dr`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 26.5 (1 cluster) | 10.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_surgio_b51_dr/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 25.0 / sacrum 6.2 (95 fr); 30-60 vert 66.7 / sacrum 44.4 (9 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 92.8 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 92.5 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`) | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 20.5 (1 cluster) | 50.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 20.0 / sacrum 50.6 (95 fr); 30-60 vert 33.3 / sacrum 44.4 (9 fr) | | | | | |
| B styled S+E + real S+E (`dc_B_held_cios_fusion`) | B | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 94.0 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 93.8 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| B styled S+E + real S+E (`dc_B_held_cios_fusion_s1`) | B | 1 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 94.0 (1 cluster) | 100.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_<split>.json` |
| | | | by angle from AP: 0-30 vert 93.8 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| real S+E (`lodo_df`) | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 95.2 (1 cluster) | 100.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_df__df_test.json` |
| | | | by angle from AP: 0-30 vert 95.0 / sacrum 100.0 (95 fr); 30-60 vert 100.0 / sacrum 100.0 (9 fr) | | | | | |
| real S only (`only_carm`) | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 10.8 (1 cluster) | 1.1 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm__df_test.json` |
| | | | by angle from AP: 0-30 vert 11.2 / sacrum 1.2 (95 fr); 30-60 vert 0.0 / sacrum 0.0 (9 fr) | | | | | |
| real S only (frames + crops) (`only_carm_multi`) | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 8.4 (1 cluster) | 5.6 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm_multi__df_test.json` |
| | | | by angle from AP: 0-30 vert 8.8 / sacrum 6.2 (95 fr); 30-60 vert 0.0 / sacrum 0.0 (9 fr) | | | | | |
| renders only, no real frame (`render`) | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 59.0 (1 cluster) | 67.8 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/render__df_test.json` |
| | | | by angle from AP: 0-30 vert 60.0 / sacrum 72.8 (95 fr); 30-60 vert 33.3 / sacrum 22.2 (9 fr) | | | | | |
| A styled S+E + real S+E (`dc_A_held_cios_fusion`) | A | 0 | DeepFluoro, all six specimens | 366 | 6 | 72.1 [59.1, 86.1] | 93.2 [74.9, 100.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 70.1 (n 137); 17-1905 61.1 (n 18); 18-0725 52.3 (n 44); 18-1109 91.6 (n 83); 18-2799 51.2 (n 82); 18-2800 93.9 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 71.7 / sacrum 93.1 (345 fr); 30-60 vert 90.0 / sacrum 95.0 (21 fr) | | | | | |
| A styled E + real E (`dc_A_held_cios_fusion_1dev_elekta_xvi`) | A | 0 | DeepFluoro, all six specimens | 366 | 6 | 75.3 [60.1, 95.0] | 93.5 [73.6, 100.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 65.0 (n 137); 17-1905 66.7 (n 18); 18-0725 95.5 (n 44); 18-1109 92.8 (n 83); 18-2799 46.3 (n 82); 18-2800 100.0 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 75.0 / sacrum 93.4 (345 fr); 30-60 vert 90.0 / sacrum 95.0 (21 fr) | | | | | |
| A styled S + real S (`dc_A_held_cios_fusion_1dev_surgio_b51_dr`) | A | 0 | DeepFluoro, all six specimens | 366 | 6 | 17.4 [2.1, 40.4] | 14.2 [2.9, 36.1] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_surgio_b51_dr/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 1.5 (n 137); 17-1905 0.0 (n 18); 18-0725 6.8 (n 44); 18-1109 31.3 (n 83); 18-2799 2.4 (n 82); 18-2800 63.6 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 17.1 / sacrum 14.2 (345 fr); 30-60 vert 30.0 / sacrum 15.0 (21 fr) | | | | | |
| A styled S+E + real S+E (`dc_A_held_cios_fusion_s1`) | A | 1 | DeepFluoro, all six specimens | 366 | 6 | 77.7 [64.8, 87.9] | 94.4 [78.0, 100.0] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 83.2 (n 137); 17-1905 55.6 (n 18); 18-0725 56.8 (n 44); 18-1109 91.6 (n 83); 18-2799 58.5 (n 82); 18-2800 92.4 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 77.4 / sacrum 94.7 (345 fr); 30-60 vert 90.0 / sacrum 90.0 (21 fr) | | | | | |
| B styled S+E + real S+E (`dc_B_held_cios_fusion`) | B | 0 | DeepFluoro, all six specimens | 366 | 6 | 78.6 [68.8, 92.0] | 95.0 [78.5, 99.8] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 66.4 (n 137); 17-1905 88.9 (n 18); 18-0725 75.0 (n 44); 18-1109 94.0 (n 83); 18-2799 68.3 (n 82); 18-2800 97.0 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 78.3 / sacrum 95.0 (345 fr); 30-60 vert 90.0 / sacrum 95.0 (21 fr) | | | | | |
| B styled S+E + real S+E (`dc_B_held_cios_fusion_s1`) | B | 1 | DeepFluoro, all six specimens | 366 | 6 | 75.3 [63.6, 90.9] | 94.1 [78.0, 99.8] | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_deepfluoro_<split>.json` |
| | | | per cluster: 17-1882 62.8 (n 137); 17-1905 77.8 (n 18); 18-0725 63.6 (n 44); 18-1109 94.0 (n 83); 18-2799 63.4 (n 82); 18-2800 100.0 (n 66) | | | | | |
| | | | by angle from AP: 0-30 vert 75.0 / sacrum 94.0 (345 fr); 30-60 vert 90.0 / sacrum 95.0 (21 fr) | | | | | |
| A styled S+E + real S+E (`dc_A_held_cios_fusion`) | A | 0 | Geneva hip phantom | 116 | 1 | 8.1 (1 cluster) | 12.6 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion/eval_geneva_hip_<split>.json` |
| A styled E + real E (`dc_A_held_cios_fusion_1dev_elekta_xvi`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 17.2 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi/eval_geneva_hip_<split>.json` |
| A styled S + real S (`dc_A_held_cios_fusion_1dev_surgio_b51_dr`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_1dev_surgio_b51_dr/eval_geneva_hip_<split>.json` |
| A styled S+E + real S+E (`dc_A_held_cios_fusion_s1`) | A | 1 | Geneva hip phantom | 116 | 1 | 45.9 (1 cluster) | 21.8 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_cios_fusion_s1/eval_geneva_hip_<split>.json` |
| A styled D+S + real D+S (`dc_A_held_elekta_xvi`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/eval_geneva_hip_<split>.json` |
| A styled D + real D (`dc_A_held_elekta_xvi_1dev_cios_fusion`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_cios_fusion/eval_geneva_hip_<split>.json` |
| A styled S + real S (`dc_A_held_elekta_xvi_1dev_surgio_b51_dr`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_1dev_surgio_b51_dr/eval_geneva_hip_<split>.json` |
| A styled D+S + real D+S (`dc_A_held_elekta_xvi_s1`) | A | 1 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi_s1/eval_geneva_hip_<split>.json` |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr`) | A | 0 | Geneva hip phantom | 116 | 1 | 8.1 (1 cluster) | 14.9 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/eval_geneva_hip_<split>.json` |
| A styled D + real D (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_cios_fusion/eval_geneva_hip_<split>.json` |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 17.2 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi/eval_geneva_hip_<split>.json` |
| A styled E + real E (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`) | A | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 25.3 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/eval_geneva_hip_<split>.json` |
| A styled D+E + real D+E (`dc_A_held_surgio_b51_dr_s1`) | A | 1 | Geneva hip phantom | 116 | 1 | 18.9 (1 cluster) | 20.7 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr_s1/eval_geneva_hip_<split>.json` |
| B styled S+E + real S+E (`dc_B_held_cios_fusion`) | B | 0 | Geneva hip phantom | 116 | 1 | 51.4 (1 cluster) | 57.5 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion/eval_geneva_hip_<split>.json` |
| B styled S+E + real S+E (`dc_B_held_cios_fusion_s1`) | B | 1 | Geneva hip phantom | 116 | 1 | 43.2 (1 cluster) | 28.7 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_cios_fusion_s1/eval_geneva_hip_<split>.json` |
| B styled D+S + real D+S (`dc_B_held_elekta_xvi`) | B | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_elekta_xvi/eval_geneva_hip_<split>.json` |
| B styled D+E + real D+E (`dc_B_held_surgio_b51_dr_s1`) | B | 1 | Geneva hip phantom | 116 | 1 | 13.5 (1 cluster) | 29.9 (1 cluster) | `/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_B_held_surgio_b51_dr_s1/eval_geneva_hip_<split>.json` |
| real D+E (`lodo_carm`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 10.8 (1 cluster) | 35.6 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__geneva_all.json` |
| real D+S (`lodo_cobra`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_cobra__geneva_all.json` |
| real S+E (`lodo_df`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 16.2 (1 cluster) | 34.5 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_df__geneva_all.json` |
| real S only (`only_carm`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm__geneva_all.json` |
| real S only (frames + crops) (`only_carm_multi`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/only_carm_multi__geneva_all.json` |
| real D+S+E (`pooled`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 27.0 (1 cluster) | 31.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/pooled__geneva_all.json` |
| renders only, no real frame (`render`) | real-only | 0 | Geneva hip phantom | 116 | 1 | 0.0 (1 cluster) | 0.0 (1 cluster) | `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/render__geneva_all.json` |

## In-training cells (reference only, never generalisation)

| training set | design | seed | target | frames | clusters | vertebra recall | sacrum found |
|---|---|---|---|---:|---:|---|---|
| A styled S+E + real S+E | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.9 [84.7, 94.4] | 96.4 [91.1, 100.0] |
| A styled S + real S | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 88.9 [83.0, 93.9] | 96.4 [91.1, 100.0] |
| A styled S+E + real S+E | A | 1 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 90.6 [85.4, 95.1] | 96.4 [91.1, 100.0] |
| A styled D+S + real D+S | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 88.2 [82.1, 93.5] | 98.2 [94.6, 100.0] |
| A styled S + real S | A | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.5 [84.3, 93.9] | 96.4 [91.1, 100.0] |
| A styled D+S + real D+S | A | 1 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 90.2 [85.1, 94.6] | 96.4 [91.1, 100.0] |
| B styled S+E + real S+E | B | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 88.9 [83.2, 93.6] | 96.4 [89.3, 100.0] |
| B styled S+E + real S+E | B | 1 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.5 [84.2, 94.4] | 98.2 [94.6, 100.0] |
| B styled D+S + real D+S | B | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 90.2 [84.6, 94.9] | 96.4 [91.1, 100.0] |
| real D+S | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.5 [83.7, 94.3] | 96.4 [91.1, 100.0] |
| real S+E | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.2 [83.8, 93.7] | 98.2 [94.6, 100.0] |
| real S only | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 89.9 [84.7, 94.7] | 98.2 [94.6, 100.0] |
| real S only (frames + crops) | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 88.9 [83.1, 93.5] | 96.4 [91.1, 100.0] |
| real D+S+E | real-only | 0 | C-ArmLSpine test (body truth, reference) | 56 | 28 | 90.6 [85.4, 95.1] | 98.2 [94.6, 100.0] |
| A styled S+E + real S+E | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.1 [38.6, 43.4] | 96.4 [91.1, 100.0] |
| A styled S + real S | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 39.7 [37.4, 41.9] | 96.4 [91.1, 100.0] |
| A styled S+E + real S+E | A | 1 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.5 [39.2, 43.6] | 96.4 [91.1, 100.0] |
| A styled D+S + real D+S | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 42.9 [39.7, 45.7] | 98.2 [94.6, 100.0] |
| A styled S + real S | A | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.8 [39.4, 44.1] | 96.4 [91.1, 100.0] |
| A styled D+S + real D+S | A | 1 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.8 [39.4, 44.1] | 96.4 [91.1, 100.0] |
| B styled S+E + real S+E | B | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.1 [38.8, 43.2] | 96.4 [89.3, 100.0] |
| B styled S+E + real S+E | B | 1 | C-ArmLSpine test (outline truth) | 56 | 28 | 40.1 [37.5, 42.4] | 98.2 [94.6, 100.0] |
| B styled D+S + real D+S | B | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 40.4 [38.2, 42.6] | 96.4 [91.1, 100.0] |
| real D+S | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 40.4 [38.1, 42.6] | 96.4 [91.1, 100.0] |
| real S+E | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.1 [38.8, 43.4] | 98.2 [94.6, 100.0] |
| real S only | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 41.5 [38.7, 44.1] | 98.2 [94.6, 100.0] |
| real S only (frames + crops) | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 38.3 [36.1, 40.4] | 96.4 [91.1, 100.0] |
| real D+S+E | real-only | 0 | C-ArmLSpine test (outline truth) | 56 | 28 | 40.8 [38.4, 42.9] | 98.2 [94.6, 100.0] |
| A styled S+E + real S+E | A | 0 | COBRA Elekta XVI test | 648 | 27 | 97.4 [94.1, 99.4] | 98.4 [96.8, 99.7] |
| A styled E + real E | A | 0 | COBRA Elekta XVI test | 648 | 27 | 97.0 [92.4, 99.6] | 99.0 [98.0, 99.8] |
| A styled S+E + real S+E | A | 1 | COBRA Elekta XVI test | 648 | 27 | 96.6 [91.0, 99.5] | 98.2 [95.8, 99.8] |
| A styled D+E + real D+E | A | 0 | COBRA Elekta XVI test | 648 | 27 | 96.8 [91.5, 99.5] | 98.7 [97.4, 99.7] |
| A styled E + real E | A | 0 | COBRA Elekta XVI test | 648 | 27 | 97.0 [92.4, 99.6] | 99.0 [98.0, 99.8] |
| A styled E + real E | A | 0 | COBRA Elekta XVI test | 648 | 27 | 48.5 [38.6, 56.7] | 70.8 [65.2, 76.0] |
| A styled D+E + real D+E | A | 1 | COBRA Elekta XVI test | 648 | 27 | 97.1 [92.5, 99.6] | 98.5 [96.8, 99.7] |
| B styled S+E + real S+E | B | 0 | COBRA Elekta XVI test | 648 | 27 | 96.4 [91.8, 99.2] | 98.5 [96.8, 99.8] |
| B styled S+E + real S+E | B | 1 | COBRA Elekta XVI test | 648 | 27 | 97.4 [93.6, 99.5] | 98.4 [96.5, 99.8] |
| B styled D+E + real D+E | B | 1 | COBRA Elekta XVI test | 648 | 27 | 96.9 [92.6, 99.3] | 98.5 [97.1, 99.7] |
| real D+E | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 97.3 [92.7, 99.7] | 98.9 [97.8, 99.7] |
| real S+E | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 96.9 [92.2, 99.5] | 99.3 [98.7, 99.8] |
| real D+S+E | real-only | 0 | COBRA Elekta XVI test | 648 | 27 | 97.4 [93.3, 99.8] | 97.9 [95.7, 99.5] |
| A styled D+S + real D+S | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 85.5 (1 cluster) | 97.8 (1 cluster) |
| A styled D + real D | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 92.8 (1 cluster) | 100.0 (1 cluster) |
| A styled D+S + real D+S | A | 1 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 92.8 (1 cluster) | 100.0 (1 cluster) |
| A styled D+E + real D+E | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 94.0 (1 cluster) | 100.0 (1 cluster) |
| A styled D + real D | A | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 92.8 (1 cluster) | 100.0 (1 cluster) |
| A styled D+E + real D+E | A | 1 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 86.7 (1 cluster) | 100.0 (1 cluster) |
| B styled D+S + real D+S | B | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 85.5 (1 cluster) | 98.9 (1 cluster) |
| B styled D+E + real D+E | B | 1 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 94.0 (1 cluster) | 100.0 (1 cluster) |
| real D+E | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 91.6 (1 cluster) | 100.0 (1 cluster) |
| real D+S | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 79.5 (1 cluster) | 95.6 (1 cluster) |
| real D+S+E | real-only | 0 | DeepFluoro test (specimen 18-1109) | 104 | 1 | 95.2 (1 cluster) | 100.0 (1 cluster) |

## Marginal contribution of each source (design A, paired case bootstrap of the difference)

| held-out target | source added | to base | pair recall | base recall | add-one delta (pp) | 95 % CI | clusters |
|---|---|---|---:|---:|---:|---|---:|
| DeepFluoro test (specimen 18-1109) | S | E (seed 0 pair) | 91.6 | 92.8 | -1.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | S | E (seed 0 pair) | 91.6 | 92.8 | -1.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | S | E (seed 0 pair) | 91.6 | 20.5 | +71.1 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | S | E (seed 1 pair) | 91.6 | 92.8 | -1.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | S | E (seed 1 pair) | 91.6 | 92.8 | -1.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | S | E (seed 1 pair) | 91.6 | 20.5 | +71.1 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | E | S (seed 0 pair) | 91.6 | 31.3 | +60.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | E | S (seed 0 pair) | 91.6 | 26.5 | +65.1 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | E | S (seed 1 pair) | 91.6 | 31.3 | +60.2 | one cluster | 1 |
| DeepFluoro test (specimen 18-1109) | E | S (seed 1 pair) | 91.6 | 26.5 | +65.1 | one cluster | 1 |
| DeepFluoro, all six specimens | S | E (seed 0 pair) | 72.1 | 75.3 | -3.3 | [-17.5, +3.5] | 6 |
| DeepFluoro, all six specimens | S | E (seed 1 pair) | 77.7 | 75.3 | +2.3 | [-16.1, +12.6] | 6 |
| DeepFluoro, all six specimens | E | S (seed 0 pair) | 72.1 | 17.4 | +54.7 | [+40.9, +64.1] | 6 |
| DeepFluoro, all six specimens | E | S (seed 1 pair) | 77.7 | 17.4 | +60.2 | [+40.9, +73.9] | 6 |
| COBRA Elekta XVI test | D | S (seed 0 pair) | 30.2 | 7.5 | +22.7 | [+17.0, +28.1] | 27 |
| COBRA Elekta XVI test | D | S (seed 0 pair) | 30.2 | 12.2 | +18.0 | [+13.2, +23.4] | 27 |
| COBRA Elekta XVI test | D | S (seed 1 pair) | 31.4 | 7.5 | +23.9 | [+18.1, +29.3] | 27 |
| COBRA Elekta XVI test | D | S (seed 1 pair) | 31.4 | 12.2 | +19.1 | [+14.6, +24.0] | 27 |
| COBRA Elekta XVI test | S | D (seed 0 pair) | 30.2 | 38.1 | -7.8 | [-12.5, -3.9] | 27 |
| COBRA Elekta XVI test | S | D (seed 0 pair) | 30.2 | 38.1 | -7.8 | [-12.5, -3.9] | 27 |
| COBRA Elekta XVI test | S | D (seed 1 pair) | 31.4 | 38.1 | -6.7 | [-12.5, -1.8] | 27 |
| COBRA Elekta XVI test | S | D (seed 1 pair) | 31.4 | 38.1 | -6.7 | [-12.5, -1.8] | 27 |
| C-ArmLSpine test (outline truth) | D | E (seed 0 pair) | 84.7 | 86.8 | -2.1 | [-6.0, +1.4] | 28 |
| C-ArmLSpine test (outline truth) | D | E (seed 0 pair) | 84.7 | 86.8 | -2.1 | [-6.0, +1.4] | 28 |
| C-ArmLSpine test (outline truth) | D | E (seed 0 pair) | 84.7 | 39.0 | +45.6 | [+39.5, +51.6] | 28 |
| C-ArmLSpine test (outline truth) | D | E (seed 1 pair) | 80.5 | 86.8 | -6.3 | [-9.8, -2.9] | 28 |
| C-ArmLSpine test (outline truth) | D | E (seed 1 pair) | 80.5 | 86.8 | -6.3 | [-9.8, -2.9] | 28 |
| C-ArmLSpine test (outline truth) | D | E (seed 1 pair) | 80.5 | 39.0 | +41.5 | [+34.1, +48.6] | 28 |
| C-ArmLSpine test (outline truth) | E | D (seed 0 pair) | 84.7 | 12.9 | +71.8 | [+63.4, +79.6] | 28 |
| C-ArmLSpine test (outline truth) | E | D (seed 0 pair) | 84.7 | 12.9 | +71.8 | [+63.4, +79.6] | 28 |
| C-ArmLSpine test (outline truth) | E | D (seed 1 pair) | 80.5 | 12.9 | +67.6 | [+57.6, +76.8] | 28 |
| C-ArmLSpine test (outline truth) | E | D (seed 1 pair) | 80.5 | 12.9 | +67.6 | [+57.6, +76.8] | 28 |

## Named paired comparisons (same frames, same case resamples)

| comparison | A | B | A recall | B recall | A - B (pp) | 95 % CI | clusters |
|---|---|---|---:|---:|---:|---|---:|
| equal-count E (240 real frames, 10 patients) minus E full (2,640 frames, 110 patients): the count lever | `dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238` | `dc_A_held_surgio_b51_dr_1dev_elekta_xvi` | 39.0 | 86.8 | -47.7 | [-53.7, -41.8] | 28 |
| equal-count E minus D only (same training size, 3,184 vs 3,180 entries): the content lever at equal count | `dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238` | `dc_A_held_surgio_b51_dr_1dev_cios_fusion` | 39.0 | 12.9 | +26.1 | [+18.2, +33.6] | 28 |
| D only, second run minus first run (same list, same seed): run-to-run variation on COBRA | `dc_A_held_elekta_xvi_1dev_cios_fusion` | `dc_A_held_surgio_b51_dr_1dev_cios_fusion` | 38.1 | 38.1 | +0.0 | [+0.0, +0.0] | 27 |
| S only, second run minus first run (same list, same seed): run-to-run variation on COBRA | `dc_A_held_elekta_xvi_1dev_surgio_b51_dr` | `dc_A_held_cios_fusion_1dev_surgio_b51_dr` | 12.2 | 7.5 | +4.7 | [+2.0, +7.5] | 27 |

## Design B minus design A on the same frames (own poses vs one pose pool)

| target | B arm | A arm | B - A (pp) | 95 % CI |
|---|---|---|---:|---|
| DeepFluoro test (specimen 18-1109) | dc_B_held_cios_fusion | dc_A_held_cios_fusion | +2.4 | one cluster |
| DeepFluoro test (specimen 18-1109) | dc_B_held_cios_fusion_s1 | dc_A_held_cios_fusion | +2.4 | one cluster |
| DeepFluoro test (specimen 18-1109) | dc_B_held_cios_fusion | dc_A_held_cios_fusion_s1 | +2.4 | one cluster |
| DeepFluoro test (specimen 18-1109) | dc_B_held_cios_fusion_s1 | dc_A_held_cios_fusion_s1 | +2.4 | one cluster |
| DeepFluoro, all six specimens | dc_B_held_cios_fusion | dc_A_held_cios_fusion | +6.5 | [-0.2, +16.7] |
| DeepFluoro, all six specimens | dc_B_held_cios_fusion_s1 | dc_A_held_cios_fusion | +3.3 | [-3.3, +11.0] |
| DeepFluoro, all six specimens | dc_B_held_cios_fusion | dc_A_held_cios_fusion_s1 | +0.9 | [-9.4, +14.3] |
| DeepFluoro, all six specimens | dc_B_held_cios_fusion_s1 | dc_A_held_cios_fusion_s1 | -2.3 | [-12.5, +8.8] |
| COBRA Elekta XVI test | dc_B_held_elekta_xvi | dc_A_held_elekta_xvi | +2.5 | [-0.9, +5.6] |
| COBRA Elekta XVI test | dc_B_held_elekta_xvi | dc_A_held_elekta_xvi_s1 | +1.3 | [-2.2, +4.7] |
| C-ArmLSpine test (outline truth) | dc_B_held_surgio_b51_dr_s1 | dc_A_held_surgio_b51_dr | +3.1 | [+0.3, +7.1] |
| C-ArmLSpine test (outline truth) | dc_B_held_surgio_b51_dr_s1 | dc_A_held_surgio_b51_dr_s1 | +7.3 | [+3.5, +11.5] |

## Seed spread (same arm, seeds 0 and 1)

| target | arm | status | seed 0 | seed 1 | spread (pp) |
|---|---|---|---:|---:|---:|
| DeepFluoro test (specimen 18-1109) | dc_A_held_cios_fusion | DEVICE-HELD-OUT | 91.6 | 91.6 | 0.0 |
| DeepFluoro test (specimen 18-1109) | dc_A_held_elekta_xvi | in-training-device | 85.5 | 92.8 | 7.2 |
| DeepFluoro test (specimen 18-1109) | dc_A_held_surgio_b51_dr | in-training-device | 94.0 | 86.7 | 7.2 |
| DeepFluoro test (specimen 18-1109) | dc_B_held_cios_fusion | DEVICE-HELD-OUT | 94.0 | 94.0 | 0.0 |
| DeepFluoro, all six specimens | dc_A_held_cios_fusion | DEVICE-HELD-OUT | 72.1 | 77.7 | 5.6 |
| DeepFluoro, all six specimens | dc_B_held_cios_fusion | DEVICE-HELD-OUT | 78.6 | 75.3 | 3.3 |
| COBRA Elekta XVI test | dc_A_held_cios_fusion | in-training-device | 97.4 | 96.6 | 0.8 |
| COBRA Elekta XVI test | dc_A_held_elekta_xvi | DEVICE-HELD-OUT | 30.2 | 31.4 | 1.1 |
| COBRA Elekta XVI test | dc_A_held_surgio_b51_dr | in-training-device | 96.8 | 97.1 | 0.3 |
| COBRA Elekta XVI test | dc_B_held_cios_fusion | in-training-device | 96.4 | 97.4 | 1.0 |
| C-ArmLSpine test (outline truth) | dc_A_held_cios_fusion | in-training-device | 41.1 | 41.5 | 0.3 |
| C-ArmLSpine test (outline truth) | dc_A_held_elekta_xvi | in-training-device | 42.9 | 41.8 | 1.0 |
| C-ArmLSpine test (outline truth) | dc_A_held_surgio_b51_dr | DEVICE-HELD-OUT | 84.7 | 80.5 | 4.2 |
| C-ArmLSpine test (outline truth) | dc_B_held_cios_fusion | in-training-device | 41.1 | 40.1 | 1.0 |
| C-ArmLSpine test (body truth, reference) | dc_A_held_cios_fusion | in-training-device | 89.9 | 90.6 | 0.7 |
| C-ArmLSpine test (body truth, reference) | dc_A_held_elekta_xvi | in-training-device | 88.2 | 90.2 | 2.1 |
| C-ArmLSpine test (body truth, reference) | dc_A_held_surgio_b51_dr | DEVICE-HELD-OUT | 21.6 | 14.3 | 7.3 |
| C-ArmLSpine test (body truth, reference) | dc_B_held_cios_fusion | in-training-device | 88.9 | 89.5 | 0.7 |
| Geneva hip phantom | dc_A_held_cios_fusion | DEVICE-HELD-OUT | 8.1 | 45.9 | 37.8 |
| Geneva hip phantom | dc_A_held_elekta_xvi | DEVICE-HELD-OUT | 0.0 | 0.0 | 0.0 |
| Geneva hip phantom | dc_A_held_surgio_b51_dr | DEVICE-HELD-OUT | 8.1 | 18.9 | 10.8 |
| Geneva hip phantom | dc_B_held_cios_fusion | DEVICE-HELD-OUT | 51.4 | 43.2 | 8.1 |

## Single-source cells and the source covariates

| source | target | recall | real train frames | real train clusters | card R2 held out | typicality_99 | pose pool | pose |lat| p90 | pair overlap (Bhattacharyya) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| E | D | 92.8 | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0176 |
| E | S | 86.8 [81.1, 91.8] | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0709 |
| S | D | 31.3 | 210 | 105 | 0.584 | 0.925 | 296 | 90.0 | 0.0401 |
| S | E | 7.5 [3.5, 12.1] | 210 | 105 | 0.584 | 0.925 | 296 | 90.0 | 0.0709 |
| D | E | 38.1 [32.3, 44.5] | 238 | 4 | 0.905 | 0.101 | 366 | 19.7 | 0.0176 |
| D | S | 12.9 [8.3, 18.1] | 238 | 4 | 0.905 | 0.101 | 366 | 19.7 | 0.0401 |
| S | D | 26.5 | 210 | 105 | 0.584 | 0.925 | 296 | 90.0 | 0.0401 |
| S | E | 12.2 [8.0, 16.0] | 210 | 105 | 0.584 | 0.925 | 296 | 90.0 | 0.0709 |
| D | E | 38.1 [32.3, 44.5] | 238 | 4 | 0.905 | 0.101 | 366 | 19.7 | 0.0176 |
| D | S | 12.9 [8.3, 18.1] | 238 | 4 | 0.905 | 0.101 | 366 | 19.7 | 0.0401 |
| E | D | 92.8 | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0176 |
| E | S | 86.8 [81.1, 91.8] | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0709 |
| E | D | 20.5 | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0176 |
| E | S | 39.0 [33.2, 44.7] | 2640 | 110 | 0.974 | 0.848 | 8418 | 54.0 | 0.0709 |

Spearman rank correlation of the single-source held-out recall with each covariate (over the cells above; the matrix is small and one seed each, so these rank, they do not test):

- src_real_train_frames: rho = 0.73 over 14 cells
- src_real_train_clusters: rho = 0.58 over 14 cells
- src_card_R2: rho = 0.73 over 14 cells
- src_typicality_99: rho = -0.19 over 14 cells
- src_pose_pool: rho = 0.73 over 14 cells
- src_pose_lat_p90: rho = -0.19 over 14 cells
- pair_overlap_bhattacharyya: rho = -0.27 over 14 cells

Source strength (mean held-out recall when this source is the only training device): D 25.5 (4 cells), S 19.4 (4 cells), E 69.8 (6 cells)
Target difficulty (held-out recall across every arm): D mean 62.2 range 8.4-95.2 (13 cells), S mean 61.4 range 12.9-90.6 (10 cells), E mean 23.3 range 1.1-38.1 (11 cells)

