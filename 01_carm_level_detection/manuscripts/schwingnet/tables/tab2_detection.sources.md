# Sources for every cell of Table 2 (`tab2_detection.tex` / `tab2_detection.md`)

Files (repo-relative; `#` marks a JSON path, `~1` is the JSON-pointer escape for `/`):

- **A1** `SchwingNet/results/a1.json` — arm `lodo_carm` on the C-ArmLSpine test frames: `#operating_points/cross_device_0.74` and `#operating_points/conf_0.25_as_quoted`, each with `vertebra_recall_outline`, `vertebra_recall_body`, `sacrum_found_outline` (k, n, clusters, percentile, bca).
- **LC** `SchwingNet/results/lcurve/lcurve.json` — `#devices/<device>/points[0]` (kind `stage1`, the design-B leave-one-device-out arm) and `#devices/<device>/all_real[]` (the controls), each with `at/0.74` and `at/0.25` → `vertebra_recall`, `sacrum_found` (point, k, n, clusters, percentile, bca, frame_level), and `pr_auc_vertebra`, `pr_auc_sacrum`. Since A28 the C-ArmLSpine (`surgio_b51_dr`) entries hold the **body** convention under `at` and the whole-vertebra outline cells printed in Table 2 under `alt/outline/<0.74|0.25>` (and `alt/outline/pr_auc_vertebra`); the sacrum is convention-free, so `at/<thr>/sacrum_found` and `pr_auc_sacrum` are unchanged. COBRA2026 and DeepFluoro entries still hold the whole-vertebra reading under `at`.
- **CM** `SchwingNet/results/contribution_matrix.json#cells[]` — one cell per arm × dataset × splits × convention at conf 0.25: `vert_recall`, `vert_truth`, `vert_ci`, `sacrum_found`, `sacrum_frames`, `sacrum_ci`, `interval`, `status`. Numerators are `round(vert_recall × vert_truth)` and `round(sacrum_found × sacrum_frames)`; every one is an exact integer (checked 2026-09-23: the products differ from an integer by < 1e-9).
- **A3** `SchwingNet/results/a3.json#comparisons/render_vs_film_detector/conf_0.05` and `conf_0.25` — `p_a` (film-trained), `p_b` (render-trained), `n_items` 233, `n_clusters` 25, `diff_pp`, `percentile_pp`, `bca_pp`, `clusters_favouring_a/b`, `bodies_from_spines_in_holdout_train` 196.
- **A2** `SchwingNet/results/a2.json#rescore_outline` — the convention definitions (body / outline / centre) and the selection rule.
- **F3** `SchwingNet/results/fig3_detection/scored/<arm>__<set>.json#conventions/<convention>/at/<0.74|0.25>` — the figure-3 job's re-score of the same sweep dumps at both operating points (`vertebra_recall`, `sacrum_found` with k, n, clusters, percentile, bca); it reproduces A1 exactly for `lodo_carm__carm_test` and the LC controls for `pooled__*`, and supplies the 0.74 cells of the render-only and real-only held-out arms.

Design labels: design A = `geometry: cios_fusion poses for every card` (one pose pool), design B = `every device's own poses` (CM `#arms`). Test-set sizes: CM cells (`frames`, `cases`, `vert_truth`, `sacrum_frames`) and A1 (`frames` 56, `cases` 28, `truth_vertebrae` 287, `frames_with_sacrum` 56).

## C-ArmLSpine block (truth: whole-vertebra outline boxes; CM convention `outline`; test split 56 frames / 28 cases / 287 vertebrae / 56 sacra)

| row | cell | value | file → field |
|---|---|---|---|
| Reported detector | 0.74 vertebra | 80.5 (231/287) [74.1, 86.8] {73.3, 86.2} | A1 `#operating_points/cross_device_0.74/vertebra_recall_outline` |
| | 0.74 sacrum | 76.8 (43/56) [64.3, 89.3] {60.7, 85.7} | A1 `.../cross_device_0.74/sacrum_found_outline` |
| | 0.25 vertebra | 90.6 (260/287) [85.1, 95.1] {84.5, 94.7}; printed Wilson [84.3, 94.5] (flagged `ceiling_regime`) | A1 `.../conf_0.25_as_quoted/vertebra_recall_outline` (`wilson_effective_n`) (CM `lodo_carm`/carmlspine/outline reads the same 0.906 under a different bootstrap seed, [85.4, 95.2]) |
| | 0.25 sacrum | 83.9 (47/56) [73.2, 92.9] {69.6, 91.1} | A1 `.../conf_0.25_as_quoted/sacrum_found_outline` |
| | PR-AUC | — | not computed for this arm under the outline convention (LC has no lodo_carm point on C-ArmLSpine; `results/inputs/curves.json` AP50 for it is under body truth) |
| Design B, seed 1 | all four cells, PR-AUC 0.890 / 0.900 | 63.1 (181/287) [54.8, 71.0] {54.1, 70.2}; 66.1 (37/56) [53.6, 78.6] {50.0, 76.8}; 87.8 (252/287) [81.4, 93.2] {80.2, 92.5}; 85.7 (48/56) [76.8, 92.9] {75.0, 91.1} | LC `#devices/surgio_b51_dr/points[0]` (run `dc_B_held_surgio_b51_dr_s1`; the seed-0 run has an empty weights directory, `stage1_note`), vertebra cells `alt/outline/0.74` and `alt/outline/0.25`, sacrum cells `at/0.74`, `at/0.25`, `alt/outline/pr_auc_vertebra` 0.8904 (the top-level `pr_auc_vertebra` 0.067 is the body convention since A28), `pr_auc_sacrum` 0.8996 |
| Design A, seed 0; seed 1 | 0.25 vertebra | 84.7 (243/287) [77.7, 90.7]; 80.5 (231/287) [72.5, 87.6] | CM `dc_A_held_surgio_b51_dr`/carmlspine/outline (0.84669 × 287 = 243); `dc_A_held_surgio_b51_dr_s1` (0.80488 × 287 = 231) |
| | 0.25 sacrum | 80.4 (45/56) [69.6, 91.1]; 82.1 (46/56) [73.2, 89.3] | same cells, `sacrum_found` × 56 |
| Elekta XVI only | 0.25 | 86.8 (249/287) [81.1, 91.8]; 78.6 (44/56) [67.9, 89.3] | CM `dc_A_held_surgio_b51_dr_1dev_elekta_xvi`/carmlspine/outline (bit-identical to `dc_A_held_cios_fusion_1dev_elekta_xvi`) |
| Cios Fusion only | 0.25 | 12.9 (37/287) [8.3, 18.1]; sacrum printed as AP 28/28, lateral 0/28, no interval (pooled 50.0, 28/56, zero-width [50.0, 50.0]) | CM `dc_A_held_surgio_b51_dr_1dev_cios_fusion`/carmlspine/outline (`by_view`); `stats_review/recompute.json#R5_ceiling/cios_only_sacrum_note` |
| Elekta XVI only, 240 frames / 10 patients | 0.25 | 39.0 (112/287) [33.2, 44.7]; 37.5 (21/56) [28.6, 46.4] | CM `dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238`/carmlspine/outline (`train_real_entries` 480 = 240 frames × 2) |
| Renders only | 0.74 | 0.3 (1/287) [0.0, 1.1] {0.0, 1.8}; sacrum 5.4 (3/56) [0.0, 12.5] {0.0, 10.7} | F3 `render__carm_test.json#conventions/outline/at/0.74` |
| | 0.25 | 31.7 (91/287) [27.1, 36.1]; 53.6 (30/56) [44.6, 62.5] | CM `render`/carmlspine/outline (F3's re-score of the same cell reads [27.0, 36.0] under its own bootstrap seed) |
| Control, C-ArmLSpine real only | all four, PR-AUC 0.367 / 0.979 | 40.4 (116/287) [37.8, 42.9] {37.9, 43.0}; 94.6 (53/56) [85.7, 100.0] {77.4, 98.2}; 41.5 (119/287) [38.8, 44.0] {38.7, 44.0}; 98.2 (55/56) [94.6, 100.0] {91.1, 100.0}; sacrum cells printed as Wilson [85.4, 98.2] (53/56) and [90.6, 99.7] (55/56) | LC `#devices/surgio_b51_dr/all_real[0]` (`rx_only_carmlspine_1024`, description "the 210 C-ArmLSpine real train frames only … COCO init, no renders"): vertebra cells `alt/outline/0.74`, `alt/outline/0.25`, PR-AUC `alt/outline/pr_auc_vertebra` 0.367; sacrum `at/<thr>/sacrum_found`; Wilson `stats_review/recompute.json#R5_ceiling/table2_sacrum_wilson`; body reading 89.9 (258/287) from `at/0.25` (body since A28) |
| Control, pooled real | all four, PR-AUC 0.385 / 0.982 | 40.1 (115/287) [37.7, 42.3] {37.6, 42.2}; 96.4 (54/56) [89.3, 100.0] {82.1, 100.0}; 40.8 (117/287) [38.4, 43.0] {38.2, 42.8}; 98.2 (55/56); sacrum cells printed as Wilson [87.9, 99.0] (54/56) and [90.6, 99.7] (55/56) | LC `#devices/surgio_b51_dr/all_real[1]` (`rx_pooled_1024`): vertebra cells `alt/outline/0.74`, `alt/outline/0.25`, PR-AUC `alt/outline/pr_auc_vertebra` 0.385; sacrum `at/<thr>/sacrum_found`; Wilson as above; body reading 90.6 (260/287) from `at/0.25` (body since A28) |
| Flagship | five cells | `\PENDING{G5}{...}` | `results/final/*.json` does not exist (docs/FLAGSHIP_PLAN.md G5) |
| footnote a, body convention | 5.2 (15/287) at 0.25 | A1 `#operating_points/conf_0.25_as_quoted/vertebra_recall_body` |

## COBRA2026 block (truth: whole-vertebra boxes projected from the registered planning CT; CM convention `default`, LC convention `body`; test split 648 frames / 27 patients / 893 vertebrae / 609 frames with a sacrum)

| row | cell | value | file → field |
|---|---|---|---|
| Real D+S, device never seen | 0.74 | 6.2 (55/893) [2.9, 9.4] {3.5, 10.4}; sacrum 3.4 (21/609) [1.3, 5.9] {1.6, 6.3} | F3 `lodo_cobra__cobra_test.json#conventions/body/at/0.74` |
| | 0.25 | 18.5 (165/893) [13.7, 22.8]; 13.3 (81/609) [8.1, 18.8] | CM `lodo_cobra`/cobra_elekta/test (0.18477 × 893 = 165; 0.13300 × 609 = 81); F3 identical |
| Design B | all four, PR-AUC 0.266 / 0.391 | 10.1 (90/893) [6.7, 13.1] {7.0, 13.3}; 13.0 (79/609) [9.0, 17.1] {9.1, 17.4}; 32.7 (292/893) [28.4, 36.2] {28.2, 36.0}; 36.5 (222/609) [31.6, 40.9] {31.1, 40.7} | LC `#devices/elekta_xvi/points[0]` (run `dc_B_held_elekta_xvi`) |
| Design A, seed 0; seed 1 | 0.25 | 30.2 (270/893) [26.3, 34.2]; 31.4 (280/893) [26.6, 35.4]; sacrum 34.2 (208/609) [29.6, 38.7]; 29.9 (182/609) [25.1, 34.5] | CM `dc_A_held_elekta_xvi` and `dc_A_held_elekta_xvi_s1`/cobra_elekta/test |
| Cios Fusion only | 0.25 | 38.1 (340/893) [32.3, 44.5]; 40.6 (247/609) [37.2, 44.0] | CM `dc_A_held_elekta_xvi_1dev_cios_fusion`/cobra_elekta/test (bit-identical to `dc_A_held_surgio_b51_dr_1dev_cios_fusion`) |
| Surgio-B51 only, two runs | 0.25 | 7.5 (67/893) [3.5, 12.1]; 12.2 (109/893) [8.0, 16.0]; sacrum 3.8 (23/609) [1.8, 6.2]; 8.0 (49/609) [5.3, 10.9] | CM `dc_A_held_cios_fusion_1dev_surgio_b51_dr` and `dc_A_held_elekta_xvi_1dev_surgio_b51_dr`/cobra_elekta/test |
| Renders only | 0.25 | 37.8 (338/893) [33.9, 42.1]; 30.9 (188/609) [26.1, 35.7] | CM `render`/cobra_elekta/test |
| Control, pooled real | all four, PR-AUC 0.963 / 0.985 | 93.2 (832/893) [86.4, 97.7] {83.8, 97.0}; 90.6 (552/609) [83.8, 96.3] {82.6, 95.7}; 97.4 (870/893) [93.3, 99.8] {90.9, 99.4}; 97.9 (596/609) [95.7, 99.5] {95.0, 99.3} | LC `#devices/elekta_xvi/all_real[0]` (`rx_pooled_1024`) |
| Flagship | five cells | `\PENDING{G5}{...}` | as above |

## DeepFluoro block (truth: whole-vertebra boxes projected from the registered CT; six specimens 366 frames / 430 vertebrae / 338 frames with a sacrum for held-out arms; test specimen 18-1109 104 frames / 83 vertebrae / 90 with a sacrum)

| row | cell | value | file → field |
|---|---|---|---|
| Real E+S, device never seen; test specimen | 0.74 | 74.7 (62/83); 100.0 (90/90); one cluster | F3 `lodo_df__df_test.json#conventions/body/at/0.74` |
| | 0.25 | 95.2 (79/83); 100.0 (90/90); one cluster | CM `lodo_df`/deepfluoro/test (0.95181 × 83 = 79); F3 identical |
| Design B, six specimens | 0.25 | 78.6 (338/430) [68.8, 92.0]; 95.0 (321/338) [78.5, 99.8] | CM `dc_B_held_cios_fusion`/deepfluoro/train+val+test (6 clusters) |
| Design B, test specimen | all four, PR-AUC 0.923 / 0.954 | 69.9 (58/83); 87.8 (79/90); 94.0 (78/83); 100.0 (90/90); frame-level intervals [61.1, 78.7], [81.1, 94.4], [88.5, 98.7] | LC `#devices/cios_fusion/points[0]` (run `dc_B_held_cios_fusion`), `at/0.74`, `at/0.25` (`frame_level` intervals; `warning` "one cluster") |
| Design A, seed 0; seed 1; six specimens | 0.25 | 72.1 (310/430) [59.1, 86.1]; 77.7 (334/430) [64.8, 87.9]; sacrum 93.2 (315/338) [74.9, 100.0]; 94.4 (319/338) [78.0, 100.0] | CM `dc_A_held_cios_fusion` and `dc_A_held_cios_fusion_s1`/deepfluoro/train+val+test |
| Elekta XVI only, six specimens | 0.25 | 75.3 (324/430) [60.1, 95.0]; 93.5 (316/338) [73.6, 100.0] | CM `dc_A_held_cios_fusion_1dev_elekta_xvi`/deepfluoro/train+val+test |
| Surgio-B51 only, six specimens | 0.25 | 17.4 (75/430) [2.1, 40.4]; 14.2 (48/338) [2.9, 36.1] | CM `dc_A_held_cios_fusion_1dev_surgio_b51_dr`/deepfluoro/train+val+test |
| Control, pooled real; test specimen | all four, PR-AUC 0.685 / 0.968 | 73.5 (61/83); 100.0 (90/90); 95.2 (79/83); 100.0 (90/90) | LC `#devices/cios_fusion/all_real[0]` (`rx_pooled_1024`) |
| Flagship | five cells | `\PENDING{G5}{...}` | as above |
| Markdown twin only: renders only, test specimen | 0.74; 0.25 | 0.0 (0/83), 1.1 (1/90); 59.0 (49/83), 67.8 (61/90) | F3 `render__df_test.json`; CM `render`/deepfluoro/test |
| Markdown twin only: renders only on COBRA | 0.74; 0.25 | 5.2 (46/893) [3.0, 7.4], 3.0 (18/609) [1.7, 4.3]; 37.8 (338/893) [33.9, 42.1], 30.9 (188/609) [26.1, 35.7] | F3 `render__cobra_test.json#conventions/body/at/0.74`; CM `render`/cobra_elekta/test |
| Markdown twin only: reported detector on COBRA (in training) | 0.74 / 0.25 | 91.2 (814/893) [83.4, 96.3] {80.5, 95.5}; 97.3 (869/893) [92.7, 99.7] {90.0, 99.5}; sacrum 93.1 (567/609), 98.9 (602/609); PR-AUC 0.966 / 0.990 | LC `#devices/elekta_xvi/all_real[1]` (`rx_lodo_carmlspine_1024`, "its best.pt was selected on this test split") |
| Markdown twin only: reported detector on the DeepFluoro test specimen (in training) | 0.74 / 0.25 | 78.3 (65/83); 91.6 (76/83); sacrum 98.9 (89/90), 100.0 (90/90); PR-AUC 0.774 / 0.963 | LC `#devices/cios_fusion/all_real[1]` |

## Plain radiographs block (25 NHANES II films / 25 spines / 233 vertebral bodies; conf 0.05 and 0.25)

| row | cell | value | file → field |
|---|---|---|---|
| Render-trained detector | 0.05; 0.25 | 71.7 (167/233); 43.3 (101/233) | A3 `conf_0.05/p_b` 0.71674 (× 233 = 167), `conf_0.25/p_b` 0.43348 (× 233 = 101) |
| Film-trained detector | 0.05; 0.25 | 99.1 (231/233); 98.7 (230/233) | A3 `conf_0.05/p_a` 0.99142 (231), `conf_0.25/p_a` 0.98712 (230); `bodies_from_spines_in_holdout_train` 196 |
| footnote f, paired difference | 0.05; 0.25 | +27.5 [20.5, 35.2] {20.9, 35.6}, 23 vs 0 spines; +55.4 [47.0, 63.6] {46.5, 63.4}, 25 vs 0 | A3 `conf_0.05/diff_pp`, `percentile_pp`, `bca_pp`, `clusters_favouring_a`; `conf_0.25/...` |

## Footnotes

| footnote | value | file |
|---|---|---|
| b, threshold 0.74 | best pooled vertebra F1 over the arm's sweeps on COBRA2026, DeepFluoro and the Geneva phantom; no C-ArmLSpine frame; adopted after the 0.25 result was reported | A1 `#operating_points/cross_device_0.74/how_chosen`; `#arm` ("best.pt selected on those devices' test splits") |
| c, PR-AUC definition | non-interpolated average precision over the confidence sweep | `results/lcurve/lcurve.md` header |
| d, body reading of the controls | 89.9 (258/287); 90.6 (260/287) | LC `#devices/surgio_b51_dr/all_real[0]/at/0.25`, `all_real[1]/at/0.25` (body since A28) (also CM `only_carm` and `pooled`/carmlspine/body) |
| e, one cluster | frame-level intervals understate | LC `frame_level.note` ("frames of ONE specimen resampled: frames are not exchangeable") |
| design A / B definitions | one pose pool / own poses | CM `#arms/*/geometry` |
