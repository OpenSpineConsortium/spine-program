# Rigor fixes: A1-A7, A9

Generated 2026-09-22 21:12 at code `6e1cf8d` by `tools/rigor_fixes.py report`. Every interval is a 2,000-resample bootstrap clustered at the case (percentile, with the BCa interval beside it and 'undefined' where the bias correction does not exist, which is the ceiling regime); Wilson intervals are on the Kish-effective n or, where the unit is the case, on the cases. Paired comparisons report the interval of the difference, McNemar's exact p over items, the exact sign test over cases and Holm across the four. Numbers under the ceiling regime carry their numerator, denominator and imperfect-case count, which is the report to quote there.

A8 (verse_drr millimetres) is a prohibition, not a computation: no millimetre from ~/verse_drr is quoted anywhere in SchwingNet.

## A1 - DONE
- held-out vertebra recall, outline truth, conf 0.25 (as quoted): **90.6 %** 95 % [85.1, 95.1] (BCa [84.5, 94.7]); n = 260/287 vertebrae over 28 cases (from `SchwingNet/results/a1.json#operating_points/conf_0.25_as_quoted`)
- held-out sacrum found, conf 0.25 (as quoted): **83.9 %** 95 % [73.2, 92.9] (BCa [69.6, 91.1]); n = 47/56 frames over 28 cases (from `SchwingNet/results/a1.json#operating_points/conf_0.25_as_quoted`)
- held-out vertebra recall, outline truth, cross-device threshold 0.74 (pre-stated): **80.5 %** 95 % [74.1, 86.8] (BCa [73.3, 86.2]); n = 231/287 vertebrae over 28 cases (from `SchwingNet/results/a1.json#operating_points/cross_device_0.74`)
- held-out sacrum found, cross-device threshold 0.74 (pre-stated): **76.8 %** 95 % [64.3, 89.3] (BCa [60.7, 85.7]); n = 43/56 frames over 28 cases (from `SchwingNet/results/a1.json#operating_points/cross_device_0.74`)

Operating points and how each was chosen:
- `conf_0.25_as_quoted` (conf 0.25): vertebra recall outline 90.6 [85.1, 95.1] BCa [84.5, 94.7], centre 90.9 [85.6, 95.4], precision 87.8, F1 0.892; sacrum found 83.9 [73.2, 92.9] BCa [69.6, 91.1]. the YOLO predict default; the value tools/or_lodo_rescore_outline.py printed and docs/RSNAI_CLAIMS.json quoted; not chosen on any data, not pre-stated with a rationale
- `cross_device_0.74` (conf 0.74): vertebra recall outline 80.5 [74.1, 86.8] BCa [73.3, 86.2], centre 80.5 [74.1, 86.8], precision 97.1, F1 0.880; sacrum found 76.8 [64.3, 89.3] BCa [60.7, 85.7]. best pooled vertebra F1 of THIS arm on its OTHER-device sweeps (COBRA Elekta, DeepFluoro, Geneva), read from curves.json cells/lodo_carm/carm_test/cross_device_threshold: chosen before looking at the C-ArmLSpine test, so a pre-deployment operating point
- `own_best_f1_outline_0.60` (conf 0.60): vertebra recall outline 87.1 [80.9, 92.3] BCa [79.6, 91.4], centre 87.5 [81.7, 92.4], precision 96.2, F1 0.914; sacrum found 80.4 [69.6, 91.1] BCa [64.3, 89.3]. best outline-convention F1 on THIS test set: test-tuned, optimistic, reported only as a bound

Recall-against-confidence curve, outline truth, 95 % percentile interval per threshold (the curve is the primary result):
| conf | vertebra recall | 95 % CI | BCa | sacrum found | 95 % CI |
|---|---|---|---|---|---|
| 0.01 | 92.7 | [87.4, 97.2] | [86.2, 96.5] | 91.1 | [83.9, 98.2] |
| 0.02 | 92.0 | [86.7, 96.4] | [85.6, 95.7] | 87.5 | [76.8, 96.4] |
| 0.03 | 91.6 | [86.4, 96.1] | [85.4, 95.4] | 85.7 | [75.0, 94.6] |
| 0.05 | 91.3 | [86.0, 95.8] | [85.2, 95.2] | 85.7 | [75.0, 94.6] |
| 0.08 | 90.9 | [85.6, 95.4] | [84.9, 95.0] | 85.7 | [75.0, 94.6] |
| 0.10 | 90.9 | [85.6, 95.4] | [84.9, 95.0] | 85.7 | [75.0, 94.6] |
| 0.15 | 90.9 | [85.6, 95.4] | [84.9, 95.0] | 85.7 | [75.0, 94.6] |
| 0.20 | 90.6 | [85.1, 95.1] | [84.5, 94.7] | 83.9 | [73.2, 92.9] |
| 0.25 | 90.6 | [85.1, 95.1] | [84.5, 94.7] | 83.9 | [73.2, 92.9] |
| 0.30 | 89.9 | [84.2, 94.7] | [83.2, 94.1] | 83.9 | [73.2, 92.9] |
| 0.40 | 88.2 | [82.2, 93.1] | [81.3, 92.4] | 82.1 | [71.4, 91.1] |
| 0.50 | 87.5 | [81.1, 92.7] | [79.9, 91.9] | 82.1 | [71.4, 91.1] |
| 0.60 | 87.1 | [80.9, 92.3] | [79.6, 91.4] | 80.4 | [69.6, 91.1] |
| 0.70 | 84.7 | [78.5, 90.3] | [77.7, 89.6] | 80.4 | [69.6, 91.1] |
| 0.74 | 80.5 | [74.1, 86.8] | [73.3, 86.2] | 76.8 | [64.3, 89.3] |
| 0.80 | 67.9 | [60.7, 75.3] | [60.5, 74.9] | 75.0 | [60.7, 87.5] |
| 0.90 | 0.0 | [0.0, 0.0] | [undefined] | 7.1 | [1.8, 14.3] |

## A2 - DONE
- rescore_outline cells computed / quoted: 1440 computed (864 vertebra-recall + 576 sacrum-found), 5 quoted (from `SchwingNet/results/a2.json#rescore_outline`)
- corpus_manifold cells computed / quoted: 120 computed (3 spaces x 2 classifiers x 19 corpora + pooled), 1 quoted (from `SchwingNet/results/a2.json#corpus_manifold`)
- leave-one-corpus-out excess over chance, features, logistic: **-0.7 pp** 95 % [-10.1, +8.6] (BCa [-8.7, +9.8]); n = 19 corpora, 7311 frames (from `SchwingNet/results/a2.json#corpus_manifold/excess_over_chance/features/logistic`)
- leave-one-corpus-out excess over chance, pca12, logistic: **+4.3 pp** 95 % [-5.1, +13.6] (BCa [-3.8, +14.9]); n = 19 corpora, 7311 frames (from `SchwingNet/results/a2.json#corpus_manifold/excess_over_chance/pca12/logistic`)
- leave-one-corpus-out excess over chance, embed3, logistic: **+2.5 pp** 95 % [-12.4, +18.1] (BCa [-10.6, +20.1]); n = 19 corpora, 7311 frames (from `SchwingNet/results/a2.json#corpus_manifold/excess_over_chance/embed3/logistic`)

**rescore_outline.md**: 6 arms x 3 sets x 16 thresholds x 3 box conventions = 864 vertebra-recall cells, plus 576 sacrum-found cells; 5 quoted (lodo_carm_heldout_vert_outline_025, lodo_carm_heldout_vert_body_025, lodo_carm_heldout_vert_centre_025, pooled_carm_vert_outline_025_control, lodo_carm_heldout_sacrum_025). Rule: arm and set are fixed by the question (the one arm that never trained on C-ArmLSpine, on the whole-frame test set): not a search. The truth convention was fixed in the tool's docstring before the numbers, with the pooled same-device arm as the control that must FALL under it; body and centre cells are quoted beside outline. The threshold 0.25 is the YOLO default and was not chosen on any data, but no rationale and no interval were printed; A1 replaces it with the cross-device threshold chosen on the other devices and gives intervals at both.

**curves.json**: 42 arm x dataset cells at 99 thresholds; the recall-vs-confidence curves computed by tools/or_recall_curves.py; every cell is printed in table.md with a JSON path, none selected.

**corpus_manifold**: 120 cells (3 spaces x 2 classifiers x (19 corpora + pooled)); quoted: manifold_lofo_pooled, manifold_lofo_chance. Pooled leave-one-corpus-out logistic accuracy: features 71.1, pca12 76.1, embed3 74.3; chance (majority share) 71.8. Three feature spaces were computed and one (the full standardised feature space) was quoted; it is the only one below the majority-class share. In the 12-component PCA space and the 3-D embedding the leave-one-corpus-out accuracy is above chance. No space was pre-registered. All three are reported here with a corpus-cluster bootstrap of the excess over chance; the claim 'film vs fluoroscopy does not transfer to an unseen corpus' survives only in the weak form: the excess over chance is at most a few points in the best space, and the fluoroscopy corpora are mostly labelled film.

| space | classifier | pooled acc | chance | excess (pp) | 95 % CI (pp) | BCa (pp) | p_boot | fluoro corpora labelled fluoro | film corpora labelled film |
|---|---|---|---|---|---|---|---|---|---|
| features | logistic | 71.1 | 71.8 | -0.7 | [-10.1, +8.6] | [-8.7, +9.8] | 0.810 | 35.4 | 83.1 |
| features | knn15 | 81.0 | 71.8 | +9.2 | [-0.5, +19.7] | [+1.4, +23.4] | 0.065 | 45.4 | 97.4 |
| pca12 | logistic | 76.1 | 71.8 | +4.3 | [-5.1, +13.6] | [-3.8, +14.9] | 0.425 | 45.7 | 85.8 |
| pca12 | knn15 | 80.2 | 71.8 | +8.4 | [-0.9, +18.8] | [+0.6, +21.6] | 0.083 | 46.3 | 96.9 |
| embed3 | logistic | 74.3 | 71.8 | +2.5 | [-12.4, +18.1] | [-10.6, +20.1] | 0.820 | 44.4 | 89.0 |
| embed3 | knn15 | 72.6 | 71.8 | +0.8 | [-11.1, +12.6] | [-9.6, +14.2] | 0.959 | 38.7 | 90.3 |

The dev/test selection machinery exists (`/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json`: 52 cells, 2214 dev / 2215 test films) and is the model for any future search; neither table above was a search over a reported cell, so it is declared rather than re-selected.

## A3 - DONE
- paired difference: render_vs_film_detector: **+27.5 pp** 95 % [+20.5, +35.2] (BCa [+20.9, +35.6]); n = bodies, cluster = spine; p_boot 5.00e-04 (Holm 0.0020); exact cluster test p 2.38e-07 (Holm 7.15e-07) (from `SchwingNet/results/a3.json#comparisons/render_vs_film_detector`)
- paired difference: zeroshot_lateral_vs_ap: **+57.7 pp** 95 % [+48.9, +66.4] (BCa [+48.8, +66.2]); n = vertebrae, cluster = case; p_boot 5.00e-04 (Holm 0.0020); exact cluster test p 2.53e-23 (Holm 1.01e-22) (from `SchwingNet/results/a3.json#comparisons/zeroshot_lateral_vs_ap`)
- paired difference: card_vs_uncalibrated_physics: **+3.8 pp** 95 % [+2.0, +5.7] (BCa [+2.2, +6.1]); n = held-out R2 x 100, mean over 24 folds; p_boot 5.00e-04 (Holm 0.0020); exact cluster test p 2.00e-04 (Holm 4.00e-04) (from `SchwingNet/results/a3.json#comparisons/card_vs_uncalibrated_physics`)
- paired difference: pooled_vs_heldout_detector: **+14.3 pp** 95 % [+5.4, +23.2] (BCa [+5.4, +21.4]); n = frames with the sacrum found at conf 0.25, cluster = case; p_boot 5.00e-04 (Holm 0.0020); exact cluster test p 0.0078 (Holm 0.0078) (from `SchwingNet/results/a3.json#comparisons/pooled_vs_heldout_detector`)

**render_vs_film_detector** - DONE
- conf_0.05: film 99.14 vs render 71.67 on the same 233 bodies / 25 spines; difference +27.47 pp, 95 % [+20.52, +35.24], BCa [+20.91, +35.59]; McNemar p 1.08e-19 (64 film-only, 0 render-only); spines favouring film 23, render 0, sign test p 2.38e-07; spines by source {'nhanes': 25}; bodies from spines in the v7 train split: 196
- conf_0.25: film 98.71 vs render 43.35 on the same 233 bodies / 25 spines; difference +55.36 pp, 95 % [+46.95, +63.60], BCa [+46.53, +63.44]; McNemar p 2.94e-39 (129 film-only, 0 render-only); spines favouring film 25, render 0, sign test p 5.96e-08; spines by source {'nhanes': 25}; bodies from spines in the v7 train split: 196
  Caveat: the shipped run passed no --holdout-bank, so whether detect_v5z_final trained on any of these 25 spines was never checked. Measured here: every spine is an NHANES II film and 196 of 233 bodies come from spines whose case names sit in the allspine_v7 TRAIN split (the film corpora the film detector was trained from). The film-trained recall is therefore NOT a held-out number and must not be quoted as one; the render-trained recall is (that detector saw no real image). The paired difference is a lower bound on the sim-to-real gap only in the sense that a held-out film detector could score lower, not higher.

**zeroshot_lateral_vs_ap** - DONE
- lateral 96.1 vs AP 38.4 on the same 593 vertebrae / 140 cases (matched by case and level; 24 lateral-only, 38 AP-only dropped); difference +57.7 pp, 95 % [+48.9, +66.4], BCa [48.8, 66.2]; McNemar p 2.16e-92; cases favouring lateral 86, AP 2, sign test p 2.53e-23. Marginals (all vertebrae): lateral 96.3 [93.1, 98.7], AP 37.9 [29.6, 45.9].

**card_vs_uncalibrated_physics** - DONE
- mean gain over 24 folds +0.0376 R2, 95 % [+0.0205, +0.0573], BCa [+0.0219, +0.0606]; median +0.0341 [+0.0126, +0.0381]; 4 of 24 folds negative; sign-flip p 2.00e-04. Per device in A6.

**pooled_vs_heldout_detector** - DONE
- conf_0.25_both (pooled 0.25 / lodo 0.25):
    - sacrum_found_outline: pooled 98.2 vs held-out 83.9 on 56 items / 28 cases; difference +14.3 pp, 95 % [+5.4, +23.2], BCa [+5.4, +21.4]; McNemar p 0.0078 (floor 0.0078); cases favouring pooled 8, held-out 0, sign p 0.0078
    - vertebra_found_centre: pooled 91.6 vs held-out 90.9 on 287 items / 28 cases; difference +0.7 pp, 95 % [+0.0, +1.8], BCa [+0.0, +2.1]; McNemar p 0.5000 (floor 0.5000); cases favouring pooled 2, held-out 0, sign p 0.5000
    - vertebra_found_outline: pooled 40.8 vs held-out 90.6 on 287 items / 28 cases; difference -49.8 pp, 95 % [-54.3, -44.5], BCa [-53.6, -43.3]; McNemar p 6.55e-42 (floor 4.48e-44); cases favouring pooled 0, held-out 28, sign p 7.45e-09
    - vertebra_found_body: pooled 90.6 vs held-out 5.2 on 287 items / 28 cases; difference +85.4 pp, 95 % [+79.5, +90.8], BCa [+79.1, +90.5]; McNemar p 6.88e-71 (floor 2.21e-75); cases favouring pooled 28, held-out 0, sign p 7.45e-09
- cross_device_each (pooled 0.76 / lodo 0.74):
    - sacrum_found_outline: pooled 96.4 vs held-out 76.8 on 56 items / 28 cases; difference +19.6 pp, 95 % [+8.9, +32.1], BCa [+8.9, +32.1]; McNemar p 9.77e-04 (floor 9.77e-04); cases favouring pooled 9, held-out 0, sign p 0.0039
    - vertebra_found_centre: pooled 81.2 vs held-out 80.5 on 287 items / 28 cases; difference +0.7 pp, 95 % [-3.5, +4.9], BCa [-3.5, +5.1]; McNemar p 0.8555 (floor 1.86e-09); cases favouring pooled 9, held-out 8, sign p 1.0000
    - vertebra_found_outline: pooled 40.1 vs held-out 80.5 on 287 items / 28 cases; difference -40.4 pp, 95 % [-46.1, -34.3], BCa [-45.4, -33.3]; McNemar p 1.64e-28 (floor 1.47e-39); cases favouring pooled 1, held-out 27, sign p 2.16e-07
    - vertebra_found_body: pooled 81.2 vs held-out 5.2 on 287 items / 28 cases; difference +76.0 pp, 95 % [+69.5, +81.8], BCa [+69.3, +81.7]; McNemar p 7.35e-63 (floor 2.97e-67); cases favouring pooled 28, held-out 0, sign p 7.45e-09
  the two arms learned different box conventions (pooled: C-ArmLSpine body boxes; lodo_carm: whole-vertebra outlines), so the vertebra comparison is reported under the convention-free mutual-centre rule first and under both IoU conventions beside it; the sacrum box is the same under both. Cluster = case (each contributes two frames).

| comparison | difference (pp) | 95 % CI | BCa | p_boot | Holm | exact cluster p | Holm |
|---|---|---|---|---|---|---|---|
| render_vs_film_detector | +27.47 | [+20.52, +35.24] | [+20.91, +35.59] | 5.00e-04 | 0.0020 | 2.38e-07 | 7.15e-07 |
| zeroshot_lateral_vs_ap | +57.67 | [+48.86, +66.43] | [+48.81, +66.16] | 5.00e-04 | 0.0020 | 2.53e-23 | 1.01e-22 |
| card_vs_uncalibrated_physics | +3.76 | [+2.05, +5.73] | [+2.19, +6.06] | 5.00e-04 | 0.0020 | 2.00e-04 | 4.00e-04 |
| pooled_vs_heldout_detector | +14.29 | [+5.36, +23.21] | [+5.36, +21.43] | 5.00e-04 | 0.0020 | 0.0078 | 0.0078 |

Holm over the four pre-listed comparisons, applied separately to the paired-bootstrap p and to the exact cluster-level test p; the family is the four comparisons the audit named, none added after seeing the data

## A4 - DONE
- C-ArmLSpine lateral whole frame, exact level, five-fold CV, full coverage: **98.2 %** 95 % [95.7, 100.0] (BCa [95.0, 99.5]); percentile / BCa, cluster = case; n = 606/617 vertebrae over 141 cases, 3 cases carry every error (from `SchwingNet/results/a4.json#cells/det~1LAT~1kfull`)
- same, Wilson on the Kish-effective n: **98.2 %** 95 % [94.6, 99.4]; n = n_eff 147.6 of 617 (design effect 4.18) (from `SchwingNet/results/a4.json#cells/det~1LAT~1kfull/wilson_effective_n`)
- share of lateral cases with every vertebra right (cluster-level Wilson): **97.9 %** 95 % [93.9, 99.3]; Wilson, unit = case; n = 138/141 cases (from `SchwingNet/results/a4.json#cells/det~1LAT~1kfull/cluster_level_wilson_all_correct`)

| cell | exact | percentile | BCa | Wilson (n_eff) | design effect | cases with an error | cases all right (Wilson) | answered | exact on answered | reproduces shipped |
|---|---|---|---|---|---|---|---|---|---|---|
| det/LAT/kfull | 98.2 (606/617) | [95.7, 100.0] | [95.0, 99.5] | [94.6, 99.4] | 4.18 | 3/141 | 97.9 [93.9, 99.3] (138/141) | 83.1 | 98.4 [96.2, 100.0] | True |
| det/AP/kfull | 96.7 (610/631) | [93.6, 99.1] | [92.9, 98.7] | [92.7, 98.5] | 3.87 | 6/142 | 95.8 [91.1, 98.0] (136/142) | 77.3 | 97.5 [95.3, 99.4] | True |
| det/LAT/k5 | 97.0 (647/667) | [93.3, 99.8] | [91.7, 99.2] | [91.5, 99.0] | 6.77 | 4/131 | 96.9 [92.4, 98.8] (127/131) | 83.4 | 97.7 [94.4, 100.0] | True |
| det/AP/k5 | 95.1 (654/688) | [91.1, 98.3] | [90.0, 97.8] | [90.0, 97.6] | 5.04 | 7/125 | 94.4 [88.9, 97.3] (118/125) | 77.3 | 96.1 [92.7, 98.7] | True |
| det/LAT/k4 | 95.7 (1013/1058) | [92.1, 98.4] | [91.5, 98.1] | [91.4, 98.0] | 6.71 | 10/142 | 93.0 [87.5, 96.1] (132/142) | 80.7 | 97.3 [94.4, 99.4] | True |
| det/AP/k4 | 94.0 (1025/1091) | [91.4, 96.3] | [91.0, 96.1] | [90.9, 96.0] | 3.22 | 24/143 | 83.2 [76.2, 88.5] (119/143) | 77.7 | 95.3 [92.7, 97.5] | True |
| det/LAT/k3 | 92.9 (1079/1162) | [89.6, 95.6] | [89.1, 95.4] | [89.2, 95.3] | 4.12 | 29/142 | 79.6 [72.2, 85.4] (113/142) | 80.0 | 95.6 [93.0, 97.7] | True |
| det/AP/k3 | 86.3 (1015/1176) | [83.1, 89.4] | [83.0, 89.3] | [82.8, 89.2] | 2.65 | 62/143 | 56.6 [48.5, 64.5] (81/143) | 76.2 | 90.5 [87.3, 93.3] | True |
| det/LAT/k2 | 89.5 (868/970) | [86.3, 92.3] | [86.2, 92.2] | [86.1, 92.1] | 2.44 | 51/143 | 64.3 [56.2, 71.7] (92/143) | 80.6 | 93.4 [90.4, 95.8] | True |
| det/AP/k2 | 79.8 (805/1009) | [76.3, 83.1] | [76.2, 82.9] | [76.2, 82.9] | 1.85 | 92/143 | 35.7 [28.3, 43.8] (51/143) | 74.6 | 85.7 [82.5, 88.6] | True |
| det/LAT/k1 | 72.8 (440/604) | [69.0, 76.2] | [69.0, 76.2] | [69.1, 76.3] | 1.04 | 103/142 | 27.5 [20.8, 35.3] (39/142) | 74.3 | 82.9 [78.9, 86.4] | True |
| det/AP/k1 | 65.1 (385/591) | [61.6, 68.8] | [61.6, 68.7] | [61.4, 68.7] | 0.91 | 114/143 | 20.3 [14.5, 27.6] (29/143) | 77.3 | 73.5 [69.6, 77.7] | True |

## A5 - DONE
- film level naming, CSXA cervical radiographs, random windows, v8 head (clean split): **99.8 %** 95 % [99.6, 100.0] (BCa [99.5, 99.9]); percentile / BCa, cluster = patient; n = 3629/3635 vertebrae over 727 patients (727 films); 3 patients carry every error (from `SchwingNet/results/a5.json#per_protocol/random/csxa/patient_clustered`)
- film level naming, BUU-LSPINE lumbar radiographs, random windows, v8 head (clean split): **97.3 %** 95 % [96.5, 98.0] (BCa [96.4, 98.0]); percentile / BCa, cluster = patient; n = 2671/2744 vertebrae over 549 patients (549 films); 51 patients carry every error (from `SchwingNet/results/a5.json#per_protocol/random/buu_full/patient_clustered`)
- film level naming, NHANES II radiographs, random windows, v8 head (clean split): **99.1 %** 95 % [98.2, 99.8] (BCa [98.0, 99.8]); percentile / BCa, cluster = patient; n = 441/445 vertebrae over 52 patients (76 films); 4 patients carry every error (from `SchwingNet/results/a5.json#per_protocol/random/nhanes/patient_clustered`)

The quoted CSXA 99.87 % of 3,720 and BUU-LSPINE 98.04 % of 2,698 were computed on the allspine_v2 bank, whose validation split leaks NHANES II and CTSpinoPelvic1K patients into training (docs/RESUME_2026-09-22_PM.md). CSXA and BUU films are keyed by their own corpus ids (one film = one CSXA person; one 4-digit BUU case = one person), so a CSXA or BUU validation film cannot leak through the NHANES/CTSP defect; that is the sense in which the per-source figures are unaffected. They cannot be re-scored: the v2 bank was deleted on 2026-09-20 and head_mixed_length.py saved no per-vertebra prediction. The numbers below are the SAME protocol on the clean v8 bank, which is the bank the manuscript must quote; v8's known leak is VerSe (CT renders), which touches no film source.

Leak check on the v8 bank by patient key (validation patients also in training): {"buu_full": {"val_patients": 549, "val_patients_also_in_train": 0, "unparsed_keys": 0}, "csxa": {"val_patients": 727, "val_patients_also_in_train": 0, "unparsed_keys": 0}, "ctsp_drr": {"val_patients": 112, "val_patients_also_in_train": 0, "unparsed_keys": 112}, "nhanes": {"val_patients": 52, "val_patients_also_in_train": 0, "unparsed_keys": 0}, "physics_drr": {"val_patients": 1081, "val_patients_also_in_train": 0, "unparsed_keys": 1081}, "physics_rare": {"val_patients": 273, "val_patients_also_in_train": 0, "unparsed_keys": 273}, "verse_drr": {"val_patients": 72, "val_patients_also_in_train": 0, "unparsed_keys": 72}}

Per-source point estimates reproduced from the re-score (must equal mixed_allspine_v8_mixed_kmax4_seed0.json): {"buu_full": {"n": 2744, "exact": 0.9734}, "csxa": {"n": 3635, "exact": 0.9983}, "ctsp_drr": {"n": 1006, "exact": 0.9394}, "nhanes": {"n": 445, "exact": 0.991}, "physics_drr": {"n": 5856, "exact": 0.7642}, "physics_rare": {"n": 1863, "exact": 0.4509}, "verse_drr": {"n": 832, "exact": 0.8329}}

| protocol maximal_band3 | source | exact | patient-clustered 95 % | BCa | film-clustered 95 % | Wilson n_eff | patients | films | patients with an error |
|---|---|---|---|---|---|---|---|---|---|
| maximal_band3 | buu_full | 94.97 (2606/2744) | [93.70, 96.10] | [93.64, 96.03] | [93.70, 96.10] | [93.64, 96.03] | 549 | 549 | 76 |
| maximal_band3 | csxa | 99.64 (3622/3635) | [99.31, 99.89] | [99.09, 99.83] | [99.31, 99.89] | [99.20, 99.84] | 727 | 727 | 7 |
| maximal_band3 | ctsp_drr | 93.24 (938/1006) | [89.37, 96.51] | [88.58, 96.12] | [89.37, 96.51] | [88.92, 95.95] | 112 | 112 | 17 |
| maximal_band3 | nhanes | 94.61 (421/445) | [91.91, 97.09] | [91.55, 96.92] | [91.67, 97.23] | [91.25, 96.72] | 52 | 76 | 14 |
| maximal_band3 | physics_drr | 69.60 (4076/5856) | [67.61, 71.54] | [67.55, 71.48] | [67.61, 71.54] | [67.63, 71.51] | 1082 | 1082 | 625 |
| maximal_band3 | physics_rare | 42.24 (787/1863) | [37.97, 46.54] | [38.18, 46.79] | [37.97, 46.54] | [37.96, 46.65] | 328 | 328 | 276 |
| maximal_band3 | verse_drr | 78.49 (653/832) | [71.48, 84.52] | [70.62, 83.96] | [71.48, 84.52] | [71.34, 84.25] | 72 | 72 | 38 |
| maximal_band3 | real film pooled (buu_full, csxa, nhanes) | 97.44 (6649/6824) | [96.92, 97.95] | [96.84, 97.91] | | [96.84, 97.92] | 1328 | | 97 |

| protocol maximal_band5 | source | exact | patient-clustered 95 % | BCa | film-clustered 95 % | Wilson n_eff | patients | films | patients with an error |
|---|---|---|---|---|---|---|---|---|---|
| maximal_band5 | buu_full | 97.27 (2669/2744) | [96.43, 98.03] | [96.35, 97.96] | [96.43, 98.03] | [96.35, 97.96] | 549 | 549 | 47 |
| maximal_band5 | csxa | 99.78 (3627/3635) | [99.50, 100.00] | [99.23, 99.94] | [99.50, 100.00] | [99.33, 99.93] | 727 | 727 | 3 |
| maximal_band5 | ctsp_drr | 93.74 (943/1006) | [89.96, 97.01] | [89.40, 96.52] | [89.96, 97.01] | [89.44, 96.36] | 112 | 112 | 16 |
| maximal_band5 | nhanes | 97.53 (434/445) | [95.61, 99.08] | [95.08, 98.87] | [95.60, 99.11] | [95.02, 98.79] | 52 | 76 | 8 |
| maximal_band5 | physics_drr | 74.91 (4387/5856) | [72.90, 76.93] | [72.78, 76.82] | [72.90, 76.93] | [72.84, 76.88] | 1082 | 1082 | 498 |
| maximal_band5 | physics_rare | 44.02 (820/1863) | [39.40, 48.69] | [39.59, 48.84] | [39.40, 48.69] | [39.38, 48.76] | 328 | 328 | 268 |
| maximal_band5 | verse_drr | 81.61 (679/832) | [74.45, 87.70] | [73.86, 87.15] | [74.45, 87.70] | [74.30, 87.20] | 72 | 72 | 33 |
| maximal_band5 | real film pooled (buu_full, csxa, nhanes) | 98.62 (6730/6824) | [98.25, 98.97] | [98.18, 98.94] | | [98.20, 98.95] | 1328 | | 58 |

| protocol maximal_band7 | source | exact | patient-clustered 95 % | BCa | film-clustered 95 % | Wilson n_eff | patients | films | patients with an error |
|---|---|---|---|---|---|---|---|---|---|
| maximal_band7 | buu_full | 98.62 (2706/2744) | [98.18, 99.02] | [98.07, 98.98] | [98.18, 99.02] | [98.11, 98.99] | 549 | 549 | 38 |
| maximal_band7 | csxa | 99.86 (3630/3635) | [99.67, 100.00] | [99.48, 99.97] | [99.67, 100.00] | [99.55, 99.96] | 727 | 727 | 3 |
| maximal_band7 | ctsp_drr | 94.43 (950/1006) | [90.88, 97.42] | [90.14, 96.93] | [90.88, 97.42] | [90.26, 96.88] | 112 | 112 | 14 |
| maximal_band7 | nhanes | 99.10 (441/445) | [97.89, 100.00] | [97.18, 99.78] | [98.00, 100.00] | [97.23, 99.71] | 52 | 76 | 3 |
| maximal_band7 | physics_drr | 78.60 (4603/5856) | [76.50, 80.67] | [76.38, 80.52] | [76.50, 80.67] | [76.45, 80.61] | 1082 | 1082 | 413 |
| maximal_band7 | physics_rare | 45.36 (845/1863) | [40.47, 50.27] | [40.68, 50.53] | [40.47, 50.27] | [40.36, 50.45] | 328 | 328 | 249 |
| maximal_band7 | verse_drr | 83.65 (696/832) | [76.57, 89.77] | [75.47, 89.27] | [76.57, 89.77] | [75.89, 89.27] | 72 | 72 | 26 |
| maximal_band7 | real film pooled (buu_full, csxa, nhanes) | 99.31 (6777/6824) | [99.09, 99.52] | [99.06, 99.49] | | [99.07, 99.49] | 1328 | | 44 |

| protocol maximal_band9 | source | exact | patient-clustered 95 % | BCa | film-clustered 95 % | Wilson n_eff | patients | films | patients with an error |
|---|---|---|---|---|---|---|---|---|---|
| maximal_band9 | buu_full | 99.93 (2742/2744) | [99.82, 100.00] | [99.70, 100.00] | [99.82, 100.00] | [99.73, 99.98] | 549 | 549 | 2 |
| maximal_band9 | csxa | 99.94 (3633/3635) | [99.83, 100.00] | [99.67, 100.00] | [99.83, 100.00] | [99.71, 99.99] | 727 | 727 | 1 |
| maximal_band9 | ctsp_drr | 94.63 (952/1006) | [91.03, 97.70] | [90.29, 97.22] | [91.03, 97.70] | [90.29, 97.10] | 112 | 112 | 12 |
| maximal_band9 | nhanes | 99.78 (444/445) | [99.27, 100.00] | [98.84, 100.00] | [99.31, 100.00] | [98.71, 99.96] | 52 | 76 | 1 |
| maximal_band9 | physics_drr | 80.36 (4706/5856) | [78.23, 82.46] | [78.17, 82.41] | [78.23, 82.46] | [78.13, 82.42] | 1082 | 1082 | 349 |
| maximal_band9 | physics_rare | 45.46 (847/1863) | [40.24, 50.58] | [40.50, 50.84] | [40.24, 50.58] | [40.19, 50.84] | 328 | 328 | 234 |
| maximal_band9 | verse_drr | 84.74 (705/832) | [77.37, 91.06] | [76.34, 90.59] | [77.37, 91.06] | [76.65, 90.37] | 72 | 72 | 21 |
| maximal_band9 | real film pooled (buu_full, csxa, nhanes) | 99.93 (6819/6824) | [99.84, 99.99] | [99.79, 99.97] | | [99.80, 99.97] | 1328 | | 4 |

| protocol random | source | exact | patient-clustered 95 % | BCa | film-clustered 95 % | Wilson n_eff | patients | films | patients with an error |
|---|---|---|---|---|---|---|---|---|---|
| random | buu_full | 97.34 (2671/2744) | [96.54, 98.03] | [96.44, 97.97] | [96.54, 98.03] | [96.47, 98.00] | 549 | 549 | 51 |
| random | csxa | 99.83 (3629/3635) | [99.61, 100.00] | [99.46, 99.94] | [99.61, 100.00] | [99.49, 99.95] | 727 | 727 | 3 |
| random | ctsp_drr | 93.94 (945/1006) | [89.99, 97.31] | [89.07, 96.82] | [89.99, 97.31] | [89.28, 96.64] | 112 | 112 | 14 |
| random | nhanes | 99.10 (441/445) | [98.15, 99.79] | [97.96, 99.77] | [98.17, 99.78] | [97.81, 99.63] | 52 | 76 | 4 |
| random | physics_drr | 76.42 (4475/5856) | [74.36, 78.45] | [74.23, 78.38] | [74.36, 78.45] | [74.27, 78.44] | 1082 | 1082 | 477 |
| random | physics_rare | 45.09 (840/1863) | [40.07, 49.97] | [40.47, 50.37] | [40.07, 49.97] | [40.10, 50.17] | 328 | 328 | 250 |
| random | verse_drr | 83.29 (693/832) | [76.04, 89.36] | [74.83, 88.63] | [76.04, 89.36] | [75.58, 88.93] | 72 | 72 | 31 |
| random | real film pooled (buu_full, csxa, nhanes) | 98.78 (6741/6824) | [98.45, 99.10] | [98.41, 99.06] | | [98.41, 99.07] | 1328 | | 58 |

## A6 - DONE
- card gain over uncalibrated physics, bv_pulsera (mean over 6 folds): **+0.0417** 95 % [+0.0348, +0.0528] (BCa [+0.0354, +0.0574]); n = folds [6, 14, 22, 39, 18, 17] frames; spread +0.0315 to +0.0680, 0 negative; sign-flip p 0.03125; C3 PASS (from `SchwingNet/results/a6.json#per_device/bv_pulsera`)
- card gain over uncalibrated physics, cios_fusion (mean over 6 folds): **+0.0153** 95 % [+0.0029, +0.0274] (BCa [-0.0005, +0.0269]); n = folds [111, 24, 24, 104, 48, 55] frames; spread -0.0128 to +0.0360, 1 negative; sign-flip p 0.125; C3 PASS (from `SchwingNet/results/a6.json#per_device/cios_fusion`)
- card gain over uncalibrated physics, elekta_xvi (mean over 6 folds): **+0.0232** 95 % [+0.0054, +0.0453] (BCa [+0.0061, +0.0469]); n = folds [22, 21, 88, 102, 62, 40] frames; spread -0.0010 to +0.0710, 1 negative; sign-flip p 0.0625; C3 PASS (from `SchwingNet/results/a6.json#per_device/elekta_xvi`)
- card gain over uncalibrated physics, pixium_4600 (mean over 6 folds): **+0.0703** 95 % [+0.0063, +0.1312] (BCa [+0.0018, +0.1243]); n = folds [4, 4, 1, 4, 4, 1] frames; spread -0.0412 to +0.1754, 2 negative; sign-flip p 0.125; C3 PASS (from `SchwingNet/results/a6.json#per_device/pixium_4600`)

Criterion: docs/RSNAI_PLAN.md C3: gain > 0 on every device with the CI excluding 0. Verdict: on the percentile interval C3 holds = **True** (passing ['bv_pulsera', 'cios_fusion', 'elekta_xvi', 'pixium_4600'], failing []); on the BCa interval C3 holds = **False** (failing ['cios_fusion']); the exact sign-flip test rejects at 0.05 on ['bv_pulsera'] only. evaluated on the mean held-out gain over the device's six folds with a 2,000-resample bootstrap over folds (percentile; BCa beside it) and the exact sign-flip test (floor 2/64 = 0.031); six folds is a coarse design: the percentile interval is what the criterion text asks for, the BCa interval is the stricter reading, and the exact test can reject only when every fold is positive. The per-fold spread is the primary report.

| device | folds (frames) | gains per fold | mean [95 %] | BCa | median [95 %] | negative folds | sign-flip p | promoted median | C3 |
|---|---|---|---|---|---|---|---|---|---|
| bv_pulsera | [6, 14, 22, 39, 18, 17] | +0.0680, +0.0379, +0.0315, +0.0378, +0.0350, +0.0399 | +0.0417 [+0.0348, +0.0528] | [+0.0354, +0.0574] | +0.0379 [+0.0333, +0.0540] | 0/6 | 0.03125 | +0.0379 | PASS |
| cios_fusion | [111, 24, 24, 104, 48, 55] | +0.0333, +0.0132, -0.0128, +0.0360, +0.0126, +0.0097 | +0.0153 [+0.0029, +0.0274] | [-0.0005, +0.0269] | +0.0129 [-0.0015, +0.0347] | 1/6 | 0.125 | +0.0129 | PASS |
| elekta_xvi | [22, 21, 88, 102, 62, 40] | +0.0031, +0.0285, +0.0014, +0.0363, -0.0010, +0.0710 | +0.0232 [+0.0054, +0.0453] | [+0.0061, +0.0469] | +0.0158 [+0.0002, +0.0536] | 1/6 | 0.0625 | +0.0158 | PASS |
| pixium_4600 | [4, 4, 1, 4, 4, 1] | +0.0991, -0.0412, +0.1754, -0.0203, +0.0805, +0.1284 | +0.0703 [+0.0063, +0.1312] | [+0.0018, +0.1243] | +0.0898 [-0.0308, +0.1519] | 2/6 | 0.125 | +0.0898 | PASS |

## A7 - DONE
- cv5/det/LAT/kfull: exact at FULL coverage: **98.2 %** 95 % [95.7, 100.0] (BCa [95.0, 99.5]); n = 606/617 over 141 cases (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/kfull`)
- cv5/det/LAT/kfull: answered share at the default rule (p < 0.5 or disagreement abstains): **83.1 %** 95 % [79.7, 86.3] (BCa [79.5, 86.2]); n = 513/617 (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/kfull/default_rule`)
- cv5/det/LAT/kfull: exact on the answered share: **98.4 %** 95 % [96.2, 100.0] (BCa [95.0, 99.6]); n = 505/513; 3 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/kfull/default_rule`)
- cv5/det/AP/kfull: exact at FULL coverage: **96.7 %** 95 % [93.6, 99.1] (BCa [92.9, 98.7]); n = 610/631 over 142 cases (from `SchwingNet/results/a7.json#cells/cv5/det/AP/kfull`)
- cv5/det/AP/kfull: answered share at the default rule (p < 0.5 or disagreement abstains): **77.3 %** 95 % [74.2, 80.5] (BCa [74.0, 80.3]); n = 488/631 (from `SchwingNet/results/a7.json#cells/cv5/det/AP/kfull/default_rule`)
- cv5/det/AP/kfull: exact on the answered share: **97.5 %** 95 % [95.3, 99.4] (BCa [94.6, 99.0]); n = 476/488; 9 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/cv5/det/AP/kfull/default_rule`)
- cv5/det/LAT/k3: exact at FULL coverage: **92.9 %** 95 % [89.6, 95.6] (BCa [89.1, 95.4]); n = 1079/1162 over 142 cases (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k3`)
- cv5/det/LAT/k3: answered share at the default rule (p < 0.5 or disagreement abstains): **80.0 %** 95 % [76.9, 83.3] (BCa [76.9, 83.2]); n = 930/1162 (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k3/default_rule`)
- cv5/det/LAT/k3: exact on the answered share: **95.6 %** 95 % [93.0, 97.7] (BCa [92.5, 97.5]); n = 889/930; 42 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k3/default_rule`)
- cv5/det/LAT/k1: exact at FULL coverage: **72.8 %** 95 % [69.0, 76.2] (BCa [69.0, 76.2]); n = 440/604 over 142 cases (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k1`)
- cv5/det/LAT/k1: answered share at the default rule (p < 0.5 or disagreement abstains): **74.3 %** 95 % [70.4, 78.0] (BCa [70.3, 77.8]); n = 449/604 (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k1/default_rule`)
- cv5/det/LAT/k1: exact on the answered share: **82.9 %** 95 % [78.9, 86.4] (BCa [78.8, 86.4]); n = 372/449; 87 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/cv5/det/LAT/k1/default_rule`)
- zeroshot2/det/LAT/kfull: exact at FULL coverage: **96.3 %** 95 % [93.1, 98.7] (BCa [92.3, 98.5]); n = 594/617 over 141 cases (from `SchwingNet/results/a7.json#cells/zeroshot2/det/LAT/kfull`)
- zeroshot2/det/LAT/kfull: answered share at the default rule (p < 0.5 or disagreement abstains): **83.1 %** 95 % [79.6, 86.3] (BCa [79.8, 86.4]); n = 513/617 (from `SchwingNet/results/a7.json#cells/zeroshot2/det/LAT/kfull/default_rule`)
- zeroshot2/det/LAT/kfull: exact on the answered share: **97.5 %** 95 % [94.8, 99.6] (BCa [93.5, 99.2]); n = 500/513; 10 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/zeroshot2/det/LAT/kfull/default_rule`)
- zeroshot2/det/AP/kfull: exact at FULL coverage: **37.9 %** 95 % [29.6, 45.9] (BCa [30.1, 46.4]); n = 239/631 over 142 cases (from `SchwingNet/results/a7.json#cells/zeroshot2/det/AP/kfull`)
- zeroshot2/det/AP/kfull: answered share at the default rule (p < 0.5 or disagreement abstains): **17.4 %** 95 % [14.9, 20.1] (BCa [14.8, 19.9]); n = 110/631 (from `SchwingNet/results/a7.json#cells/zeroshot2/det/AP/kfull/default_rule`)
- zeroshot2/det/AP/kfull: exact on the answered share: **36.4 %** 95 % [26.2, 47.6] (BCa [26.4, 47.8]); n = 40/110; 322 errors sit among the abstained (from `SchwingNet/results/a7.json#cells/zeroshot2/det/AP/kfull/default_rule`)

tools/level_prototype.py:355 abstains when the decoded name disagrees with the single-crop name OR its probability is below --abstain-below (default 0.5, never tuned). 'exact (full coverage)' scores every matched vertebra on its decoded name whether or not the rule abstains; 'answered' is the share the rule does not abstain on; 'exact on answered' is accuracy on that share

| cell | exact, full coverage | answered (default) | exact on answered | errors among abstained / answered | t=0.0 | t=0.3 | t=0.5 | t=0.7 | t=0.9 | t=0.95 |
|---|---|---|---|---|---|---|---|---|---|---|
| cv5/det/LAT/kfull | 98.2 [95.7, 100.0] (606/617, 141 cases) | 83.1 [79.7, 86.3] | 98.4 [96.2, 100.0] BCa [95.0, 99.6] | 3 / 8 | cov 88 / acc 98.3 [96.1, 100.0] | cov 88 / acc 98.5 [96.4, 100.0] | cov 83 / acc 98.4 [96.2, 100.0] | cov 74 / acc 98.9 [97.3, 100.0] | cov 54 / acc 99.4 [98.1, 100.0] | cov 43 / acc 99.6 [98.8, 100.0] |
| cv5/det/AP/kfull | 96.7 [93.6, 99.1] (610/631, 142 cases) | 77.3 [74.2, 80.5] | 97.5 [95.3, 99.4] BCa [94.6, 99.0] | 9 / 12 | cov 83 / acc 97.7 [95.6, 99.4] | cov 82 / acc 97.7 [95.6, 99.4] | cov 77 / acc 97.5 [95.3, 99.4] | cov 71 / acc 97.5 [95.1, 99.3] | cov 53 / acc 98.2 [95.8, 99.7] | cov 43 / acc 99.3 [98.1, 100.0] |
| cv5/det/LAT/k5 | 97.0 [93.3, 99.8] (647/667, 131 cases) | 83.4 [79.6, 86.8] | 97.7 [94.4, 100.0] BCa [92.8, 99.5] | 7 / 13 | cov 88 / acc 97.8 [94.8, 100.0] | cov 88 / acc 97.8 [94.7, 100.0] | cov 84 / acc 97.7 [94.4, 100.0] | cov 71 / acc 98.5 [96.5, 100.0] | cov 50 / acc 98.5 [96.5, 100.0] | cov 38 / acc 98.4 [95.9, 100.0] |
| cv5/det/AP/k5 | 95.1 [91.1, 98.3] (654/688, 125 cases) | 77.3 [74.1, 80.7] | 96.1 [92.7, 98.7] BCa [91.6, 98.3] | 13 / 21 | cov 82 / acc 96.3 [93.1, 98.8] | cov 82 / acc 96.3 [93.0, 98.8] | cov 77 / acc 96.1 [92.7, 98.7] | cov 65 / acc 96.2 [92.5, 99.0] | cov 47 / acc 96.0 [91.4, 99.1] | cov 35 / acc 96.3 [91.9, 99.2] |
| cv5/det/LAT/k4 | 95.7 [92.1, 98.4] (1013/1058, 142 cases) | 80.7 [77.2, 84.1] | 97.3 [94.4, 99.4] BCa [92.9, 99.1] | 22 / 23 | cov 86 / acc 97.1 [94.4, 99.2] | cov 85 / acc 97.2 [94.4, 99.3] | cov 81 / acc 97.3 [94.4, 99.4] | cov 68 / acc 97.8 [95.2, 99.6] | cov 47 / acc 98.4 [96.4, 99.8] | cov 33 / acc 99.2 [97.8, 100.0] |
| cv5/det/AP/k4 | 94.0 [91.4, 96.3] (1025/1091, 143 cases) | 77.7 [74.9, 80.5] | 95.3 [92.7, 97.5] BCa [92.4, 97.3] | 26 / 40 | cov 81 / acc 95.5 [93.0, 97.6] | cov 81 / acc 95.5 [93.0, 97.6] | cov 78 / acc 95.3 [92.7, 97.5] | cov 68 / acc 95.4 [92.7, 97.7] | cov 48 / acc 95.6 [92.5, 98.0] | cov 36 / acc 95.2 [91.3, 98.2] |
| cv5/det/LAT/k3 | 92.9 [89.6, 95.6] (1079/1162, 142 cases) | 80.0 [76.9, 83.3] | 95.6 [93.0, 97.7] BCa [92.5, 97.5] | 42 / 41 | cov 85 / acc 95.3 [92.7, 97.5] | cov 84 / acc 95.3 [92.6, 97.4] | cov 80 / acc 95.6 [93.0, 97.7] | cov 68 / acc 96.2 [93.7, 98.2] | cov 46 / acc 97.6 [95.5, 99.2] | cov 33 / acc 97.9 [95.7, 99.5] |
| cv5/det/AP/k3 | 86.3 [83.1, 89.4] (1015/1176, 143 cases) | 76.2 [73.8, 78.8] | 90.5 [87.3, 93.3] BCa [86.9, 93.0] | 76 / 85 | cov 80 / acc 90.1 [87.1, 92.8] | cov 79 / acc 90.1 [87.0, 92.9] | cov 76 / acc 90.5 [87.3, 93.3] | cov 69 / acc 91.4 [88.4, 94.1] | cov 46 / acc 92.1 [88.6, 95.2] | cov 33 / acc 94.3 [91.3, 96.9] |
| cv5/det/LAT/k2 | 89.5 [86.3, 92.3] (868/970, 143 cases) | 80.6 [77.6, 83.5] | 93.4 [90.4, 95.8] BCa [90.0, 95.6] | 50 / 52 | cov 86 / acc 92.6 [89.6, 95.1] | cov 86 / acc 92.9 [90.0, 95.4] | cov 81 / acc 93.4 [90.4, 95.8] | cov 69 / acc 94.2 [91.4, 96.5] | cov 43 / acc 97.8 [95.3, 99.8] | cov 32 / acc 98.7 [96.9, 100.0] |
| cv5/det/AP/k2 | 79.8 [76.3, 83.1] (805/1009, 143 cases) | 74.6 [72.1, 77.1] | 85.7 [82.5, 88.6] BCa [82.3, 88.4] | 96 / 108 | cov 80 / acc 85.4 [82.3, 88.4] | cov 79 / acc 85.5 [82.3, 88.5] | cov 75 / acc 85.7 [82.5, 88.6] | cov 65 / acc 87.1 [83.9, 90.1] | cov 45 / acc 92.9 [89.5, 95.9] | cov 33 / acc 95.9 [93.1, 98.3] |
| cv5/det/LAT/k1 | 72.8 [69.0, 76.2] (440/604, 142 cases) | 74.3 [70.4, 78.0] | 82.9 [78.9, 86.4] BCa [78.8, 86.4] | 87 / 77 | cov 87 / acc 77.8 [74.1, 81.4] | cov 84 / acc 80.0 [76.2, 83.6] | cov 75 / acc 82.7 [78.7, 86.2] | cov 54 / acc 86.3 [82.4, 89.9] | cov 26 / acc 95.5 [91.4, 98.8] | cov 15 / acc 98.9 [96.6, 100.0] |
| cv5/det/AP/k1 | 65.1 [61.6, 68.8] (385/591, 143 cases) | 77.3 [74.2, 80.5] | 73.5 [69.6, 77.7] BCa [69.7, 77.7] | 85 / 121 | cov 84 / acc 70.9 [67.1, 74.9] | cov 83 / acc 71.2 [67.4, 75.2] | cov 77 / acc 73.5 [69.6, 77.7] | cov 63 / acc 79.0 [74.7, 82.9] | cov 39 / acc 89.7 [85.8, 93.5] | cov 32 / acc 93.1 [89.3, 96.4] |
| zeroshot2/det/LAT/kfull | 96.3 [93.1, 98.7] (594/617, 141 cases) | 83.1 [79.6, 86.3] | 97.5 [94.8, 99.6] BCa [93.5, 99.2] | 10 / 13 | cov 85 / acc 97.3 [94.6, 99.4] | cov 85 / acc 97.3 [94.6, 99.4] | cov 83 / acc 97.5 [94.8, 99.6] | cov 72 / acc 97.7 [95.1, 99.8] | cov 47 / acc 99.0 [97.0, 100.0] | cov 32 / acc 99.5 [98.4, 100.0] |
| zeroshot2/det/AP/kfull | 37.9 [29.6, 45.9] (239/631, 142 cases) | 17.4 [14.9, 20.1] | 36.4 [26.2, 47.6] BCa [26.4, 47.8] | 322 / 70 | cov 38 / acc 39.2 [30.3, 48.2] | cov 34 / acc 39.8 [30.8, 48.8] | cov 17 / acc 36.4 [26.2, 47.6] | cov 4 / acc 33.3 [17.2, 51.9] | cov 0 / acc 50.0 [0.0, 100.0] | cov 0 / acc n/a [undefined] |
| zeroshot2/det/LAT/k5 | 90.3 [85.6, 94.5] (602/667, 131 cases) | 81.7 [77.8, 85.6] | 93.9 [90.5, 96.8] BCa [89.9, 96.4] | 32 / 33 | cov 84 / acc 94.1 [90.8, 96.9] | cov 84 / acc 94.1 [90.8, 96.9] | cov 82 / acc 93.9 [90.5, 96.8] | cov 68 / acc 96.0 [93.4, 98.1] | cov 40 / acc 98.5 [96.4, 100.0] | cov 25 / acc 98.8 [96.9, 100.0] |
| zeroshot2/det/AP/k5 | 47.1 [38.7, 55.4] (324/688, 125 cases) | 15.1 [12.5, 17.7] | 45.2 [33.3, 57.0] BCa [34.2, 58.0] | 307 / 57 | cov 37 / acc 44.7 [35.4, 53.6] | cov 33 / acc 44.6 [34.3, 54.4] | cov 15 / acc 45.7 [33.7, 57.4] | cov 2 / acc 29.4 [11.8, 52.9] | cov 0 / acc 0.0 [undefined] | cov 0 / acc n/a [undefined] |
| zeroshot2/det/LAT/k4 | 88.5 [83.9, 92.3] (936/1058, 142 cases) | 79.5 [76.1, 82.6] | 92.0 [88.5, 95.2] BCa [88.2, 95.0] | 55 / 67 | cov 82 / acc 91.5 [87.6, 94.6] | cov 82 / acc 91.4 [87.6, 94.6] | cov 80 / acc 92.0 [88.5, 95.2] | cov 65 / acc 95.5 [93.1, 97.5] | cov 34 / acc 98.0 [95.9, 99.5] | cov 18 / acc 97.4 [94.3, 99.5] |
| zeroshot2/det/AP/k4 | 41.2 [35.5, 47.2] (450/1091, 143 cases) | 15.0 [12.8, 17.3] | 44.5 [35.1, 53.6] BCa [35.3, 54.0] | 550 / 91 | cov 37 / acc 43.0 [36.2, 49.9] | cov 33 / acc 42.1 [35.2, 48.8] | cov 15 / acc 44.8 [35.3, 53.9] | cov 2 / acc 36.0 [18.5, 57.1] | cov 0 / acc 0.0 [undefined] | cov 0 / acc n/a [undefined] |
| zeroshot2/det/LAT/k3 | 86.9 [83.1, 90.3] (1010/1162, 142 cases) | 79.1 [75.8, 82.1] | 91.1 [87.9, 93.9] BCa [87.6, 93.7] | 70 / 82 | cov 82 / acc 90.5 [87.3, 93.5] | cov 82 / acc 90.7 [87.5, 93.6] | cov 79 / acc 91.1 [87.9, 94.0] | cov 62 / acc 94.0 [90.8, 96.5] | cov 29 / acc 97.1 [94.3, 99.1] | cov 15 / acc 100.0 [100.0, 100.0] |
| zeroshot2/det/AP/k3 | 37.9 [33.0, 42.6] (446/1176, 143 cases) | 18.8 [16.6, 20.9] | 36.2 [29.6, 43.3] BCa [29.7, 43.3] | 589 / 141 | cov 42 / acc 39.1 [33.9, 44.5] | cov 38 / acc 38.5 [33.4, 44.0] | cov 19 / acc 36.2 [29.6, 43.3] | cov 4 / acc 26.1 [11.9, 40.9] | cov 0 / acc 0.0 [0.0, 0.0] | cov 0 / acc n/a [undefined] |
| zeroshot2/det/LAT/k2 | 82.6 [78.6, 86.3] (801/970, 143 cases) | 81.9 [78.8, 84.7] | 87.7 [84.1, 90.9] BCa [84.0, 90.8] | 71 / 98 | cov 87 / acc 86.5 [82.8, 89.9] | cov 87 / acc 86.8 [83.1, 90.1] | cov 82 / acc 87.7 [84.1, 90.9] | cov 58 / acc 91.9 [88.5, 94.6] | cov 23 / acc 95.2 [91.8, 98.1] | cov 12 / acc 99.1 [97.2, 100.0] |
| zeroshot2/det/AP/k2 | 27.8 [23.9, 31.8] (281/1009, 143 cases) | 25.1 [22.6, 27.5] | 18.2 [13.5, 23.1] BCa [13.7, 23.2] | 521 / 207 | cov 47 / acc 25.9 [21.7, 30.1] | cov 42 / acc 25.8 [21.4, 30.5] | cov 25 / acc 18.2 [13.5, 23.1] | cov 8 / acc 7.7 [2.5, 14.3] | cov 1 / acc 0.0 [0.0, 0.0] | cov 0 / acc 0.0 [0.0, 0.0] |
| zeroshot2/det/LAT/k1 | 63.1 [58.5, 67.6] (381/604, 142 cases) | 75.8 [71.9, 79.6] | 74.0 [69.3, 78.7] BCa [69.1, 78.4] | 104 / 119 | cov 94 / acc 67.0 [62.5, 71.2] | cov 92 / acc 67.9 [63.3, 72.4] | cov 76 / acc 74.0 [69.3, 78.7] | cov 44 / acc 83.9 [78.6, 88.7] | cov 10 / acc 88.9 [80.3, 95.6] | cov 3 / acc 89.5 [72.2, 100.0] |
| zeroshot2/det/AP/k1 | 17.3 [14.8, 20.0] (102/591, 143 cases) | 30.1 [26.5, 33.8] | 9.0 [5.2, 13.1] BCa [5.6, 13.9] | 327 / 162 | cov 90 / acc 16.6 [14.0, 19.6] | cov 72 / acc 16.0 [13.1, 19.0] | cov 30 / acc 9.0 [5.2, 13.1] | cov 13 / acc 5.2 [1.2, 10.7] | cov 4 / acc 0.0 [0.0, 0.0] | cov 2 / acc 0.0 [0.0, 0.0] |

## A9 - DONE
- C-ArmLSpine lateral whole frame, exact, cv5_case_md5_folds: **98.2 %** 95 % [95.7, 100.0] (BCa [95.0, 99.5]); n = 617 vertebrae / 141 cases / 141 frames with a scored vertebra (from `SchwingNet/results/a9.json#cv/cv5_case_md5_folds`)
- C-ArmLSpine lateral whole frame, exact, cvday_acquisition_day_folds: **92.5 %** 95 % [87.7, 96.4] (BCa [87.0, 96.1]); n = 617 vertebrae / 141 cases / 141 frames with a scored vertebra (from `SchwingNet/results/a9.json#cv/cvday_acquisition_day_folds`)

**cv5_case_md5_folds** - DONE (5 score files)
| cell | exact | percentile (pool_scores.boot) | BCa | Wilson n_eff | vertebrae / cases / frames | within one | answered |
|---|---|---|---|---|---|---|---|
| det/LAT/kfull | 98.22 | [95.7, 100.0] | [95.0, 99.5] | [94.6, 99.4] | 617 / 141 / 141 | 100.0 | 83.1 |
| det/AP/kfull | 96.67 | [93.6, 99.1] | [92.9, 98.7] | [92.7, 98.5] | 631 / 142 / 142 | 100.0 | 77.3 |
| det/LAT/k5 | 97.00 | [93.3, 99.8] | [91.7, 99.2] | [91.5, 99.0] | 667 / 131 / 159 | 100.0 | 83.4 |
| det/AP/k5 | 95.06 | [91.1, 98.3] | [90.0, 97.8] | [90.0, 97.6] | 688 / 125 / 156 | 99.9 | 77.3 |
| det/LAT/k4 | 95.75 | [92.1, 98.4] | [91.5, 98.1] | [91.4, 98.0] | 1058 / 142 / 301 | 100.0 | 80.7 |
| det/AP/k4 | 93.95 | [91.4, 96.3] | [91.0, 96.1] | [90.9, 96.0] | 1091 / 143 / 299 | 99.7 | 77.7 |
| det/LAT/k3 | 92.86 | [89.6, 95.6] | [89.1, 95.4] | [89.2, 95.3] | 1162 / 142 / 441 | 98.7 | 80.0 |
| det/AP/k3 | 86.31 | [83.1, 89.4] | [83.0, 89.3] | [82.8, 89.2] | 1176 / 143 / 441 | 99.7 | 76.2 |
| det/LAT/k2 | 89.48 | [86.3, 92.3] | [86.2, 92.2] | [86.1, 92.1] | 970 / 143 / 552 | 97.8 | 80.6 |
| det/AP/k2 | 79.78 | [76.3, 83.1] | [76.2, 82.9] | [76.2, 82.9] | 1009 / 143 / 560 | 99.1 | 74.6 |
| det/LAT/k1 | 72.85 | [69.0, 76.2] | [69.0, 76.2] | [69.1, 76.3] | 604 / 142 / 602 | 90.2 | 74.3 |
| det/AP/k1 | 65.14 | [61.6, 68.8] | [61.6, 68.7] | [61.4, 68.7] | 591 / 143 / 590 | 93.6 | 77.3 |

**cvday_acquisition_day_folds** - DONE (3 score files)
| cell | exact | percentile (pool_scores.boot) | BCa | Wilson n_eff | vertebrae / cases / frames | within one | answered |
|---|---|---|---|---|---|---|---|
| det/LAT/kfull | 92.54 | [87.7, 96.4] | [87.0, 96.1] | [86.9, 95.9] | 617 / 141 / 141 | 95.1 | 74.9 |
| det/AP/kfull | 96.67 | [93.7, 99.1] | [92.7, 98.7] | [92.6, 98.5] | 631 / 142 / 142 | 100.0 | 74.2 |
| det/LAT/k5 | 92.80 | [87.0, 97.4] | [85.8, 97.0] | [85.8, 96.5] | 667 / 131 / 159 | 96.9 | 75.6 |
| det/AP/k5 | 93.60 | [88.0, 98.2] | [86.4, 97.5] | [86.3, 97.1] | 688 / 125 / 156 | 100.0 | 73.5 |
| det/LAT/k4 | 90.26 | [85.1, 94.9] | [84.2, 94.3] | [84.3, 94.1] | 1058 / 142 / 301 | 95.0 | 73.1 |
| det/AP/k4 | 91.75 | [88.1, 95.1] | [87.3, 94.6] | [87.5, 94.6] | 1091 / 143 / 299 | 99.9 | 71.5 |
| det/LAT/k3 | 87.61 | [83.3, 91.6] | [82.3, 91.2] | [82.8, 91.2] | 1162 / 142 / 441 | 94.8 | 73.1 |
| det/AP/k3 | 85.03 | [81.5, 88.5] | [81.1, 88.2] | [81.2, 88.2] | 1176 / 143 / 441 | 99.6 | 71.3 |
| det/LAT/k2 | 81.44 | [77.4, 85.5] | [77.1, 85.3] | [77.1, 85.1] | 970 / 143 / 552 | 94.3 | 73.3 |
| det/AP/k2 | 76.61 | [73.0, 80.1] | [72.9, 79.9] | [72.9, 80.0] | 1009 / 143 / 560 | 97.6 | 69.4 |
| det/LAT/k1 | 66.56 | [62.6, 70.6] | [62.4, 70.4] | [62.5, 70.4] | 604 / 142 / 602 | 85.3 | 69.9 |
| det/AP/k1 | 60.41 | [57.4, 63.7] | [57.5, 63.8] | [57.1, 63.6] | 591 / 143 / 590 | 92.0 | 72.1 |

