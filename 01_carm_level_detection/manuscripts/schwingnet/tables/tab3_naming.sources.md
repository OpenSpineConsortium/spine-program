# Sources for every row of Table 3 (`tab3_naming.tex` / `tab3_naming.md`)

Files (repo-relative; `#` marks a JSON path, `~1` is the JSON-pointer escape for `/`):

- **A4** `SchwingNet/results/a4.json#cells/<det~1VIEW~1FIELD>` — case-grouped five-fold CV; each cell carries `k`, `n`, `clusters`, `clusters_with_error`, `percentile`, `bca`, `within1`, `answered`, `exact_on_answered`, `cluster_level_wilson_all_correct`.
- **A7** `SchwingNet/results/a7.json#cells/<cv5|zeroshot2>~1det~1VIEW~1FIELD` — `exact_full_coverage`, `default_rule/answered`, `default_rule/exact_on_answered` (k, n, clusters, percentile, bca), `abstain_sweep`; the zero-shot arm (no C-ArmLSpine frame in training).
- **A9** `SchwingNet/results/a9.json#cv/cvday_acquisition_day_folds/cells/<det~1VIEW~1FIELD>` — `exact`, `exact_ci_percentile_pool_scores`, `exact_ci_bca`, `vertebrae`, `cases`, `within1`, `answered`; numerators are `round(exact × vertebrae)`.
- **CV5** `docs/carmlspine_cv5_mixed_2026-09-21.json#oracle/LAT/kfull` — truth boxes at complete coverage.
- **A5** `SchwingNet/results/a5.json#per_protocol/random/<source>/patient_clustered` — plain film (k, n, clusters = patients, clusters_with_error, percentile, bca) and `films`.
- **CNT** `SchwingNet/results/counting.json#cells[]` (matched by `arm`, `set`, `conf`, `convention`) — `frames`, `cases`, `frames_with_truth_sacrum`, `frames_defined`, `defined_share`, `anchor_correct_share`, `matched_correct`, `matched_within_one`, `truth_correct_defined` (point, num, den, n_clusters, percentile, bca); `#pooled_across_devices[0]` for the pooled family.
- **CPL** `SchwingNet/results/coupling.json#cells/<variant~1field>` — `classifier_exact_counted`, `count_exact_counted`, `coupled_exact_counted`, `coupled_minus_count_counted`, `coupled_minus_classifier`, `disagreement_frames`, `flags/*` (k, n, cases, ci95 percentile); `#cells_with_veridah_l6/det~1kfull/per_level/L6` for the three L6 cases.

## Morphology rows

| row | value | file → field |
|---|---|---|
| case-grouped, lateral whole frame, exact | 98.2 (606/617), 141 (3), printed Wilson on n_eff [94.6, 99.4] (percentile [95.7, 100.0] reached 100 % with 11 errors), BCa [95.0, 99.5] | A4 `det~1LAT~1kfull/wilson_effective_n`; A4 `det~1LAT~1kfull` (k, n, clusters, clusters_with_error, percentile, bca); A7 `cv5~1det~1LAT~1kfull/exact_full_coverage` identical |
| within one level (twin) | 100.0 (617/617) | A4 `det~1LAT~1kfull/within1` |
| cases with every vertebra right (twin) | 97.9 (138/141), Wilson [93.9, 99.3] | A4 `det~1LAT~1kfull/cluster_level_wilson_all_correct` |
| answered at the default rule | 83.1 (513/617), [79.7, 86.3], [79.5, 86.2] | A7 `cv5~1det~1LAT~1kfull/default_rule/answered` |
| exact on the answered share | 98.4 (505/513), 141 (3), [96.2, 100.0], [95.0, 99.6] | A7 `cv5~1det~1LAT~1kfull/default_rule/exact_on_answered` |
| AP whole frame, exact | 96.7 (610/631), 142 (6), printed Wilson on n_eff [92.7, 98.5] (percentile [93.6, 99.1]; flagged), BCa [92.9, 98.7] | A4 `det~1AP~1kfull` (`wilson_effective_n`) |
| AP answered / exact on answered (twin) | 77.3 (488/631) [74.2, 80.5] {74.0, 80.3}; 97.5 (476/488) [95.3, 99.4] {94.6, 99.0} | A7 `cv5~1det~1AP~1kfull/default_rule` |
| lateral five in field (twin) | 97.0 (647/667), 131 (4), [93.3, 99.8], [91.7, 99.2] | A4 `det~1LAT~1k5` |
| lateral three in field | 92.9 (1,079/1,162), 142 (29), [89.6, 95.6], [89.1, 95.4] | A4 `det~1LAT~1k3` |
| lateral one in field | 72.8 (440/604), 142 (103), [69.0, 76.2], [69.0, 76.2] | A4 `det~1LAT~1k1` |
| AP five / three / one in field (twin) | 95.1 (654/688) 125 (7) [91.1, 98.3] {90.0, 97.8}; 86.3 (1,015/1,176) 143 (62) [83.1, 89.4] {83.0, 89.3}; 65.1 (385/591) 143 (114) [61.6, 68.8] {61.6, 68.7} | A4 `det~1AP~1k5`, `det~1AP~1k3`, `det~1AP~1k1` |
| day-grouped, lateral whole frame | 92.5 (571/617), 141, [87.7, 96.4], [87.0, 96.1] | A9 `det~1LAT~1kfull` (exact 0.92545 × 617 = 571.0) |
| day-grouped, within one (twin) | 95.1 (587/617) | A9 `det~1LAT~1kfull/within1` 0.95138 × 617 = 587.0 |
| day-grouped AP whole; lateral three; lateral one (twin) | 96.7 (610/631) [93.7, 99.1] {92.7, 98.7}; 87.6 (1,018/1,162) [83.3, 91.6] {82.3, 91.2}; 66.6 (402/604) [62.6, 70.6] {62.4, 70.4} | A9 `det~1AP~1kfull`, `det~1LAT~1k3`, `det~1LAT~1k1` |
| no C-ArmLSpine frame in training, lateral whole | 96.3 (594/617), 141 (6), printed Wilson on n_eff [92.0, 98.3] (percentile [93.1, 98.7]; flagged `ceiling_regime`), BCa [92.3, 98.5] | A7 `zeroshot2~1det~1LAT~1kfull/exact_full_coverage` (`wilson_effective_n`) |
| the same, AP whole | 37.9 (239/631), 142 (91), [29.6, 45.9], [30.1, 46.4] | A7 `zeroshot2~1det~1AP~1kfull/exact_full_coverage` |
| truth boxes at complete coverage (twin) | 93.6 (633/676), 143, [90.0, 96.8] | CV5 `oracle/LAT/kfull` exact 0.93639 × 676 = 633.0, exact_ci, cases 143 |
| CSXA validation | 99.8 (3,629/3,635), 727 patients (3), printed Wilson on n_eff [99.5, 99.9] (percentile [99.6, 100.0]), BCa [99.5, 99.9] | A5 `csxa/patient_clustered` (`wilson_effective_n`) |
| BUU-LSPINE validation | 97.3 (2,671/2,744), 549 (51), [96.5, 98.0], [96.4, 98.0] | A5 `buu_full/patient_clustered` |
| NHANES II validation | 99.1 (441/445), 52 patients (4), 76 films, printed Wilson on n_eff [97.8, 99.6] (percentile [98.2, 99.8]; flagged), BCa [98.0, 99.8] | A5 `nhanes/patient_clustered`, `nhanes/films` 76 (`wilson_effective_n`) |
| footnote a, agreed truth 814 of 910 | | `docs/DATASHEET.md` §2.3 (`levels.json` summary) |
| footnote b, abstention rule | disagreement or posterior < 0.5 | A7 `#default_rule` |

## Counting rows

| row | value | file → field |
|---|---|---|
| C-ArmLSpine, conf 0.74, counting defined | 82.1 (46/56), 28, [69.6, 92.9], [69.6, 91.1] | CNT cell `lodo_carm` / `carm_test` / 0.74 / outline: `defined_share` |
| detected sacrum is the true sacrum (twin) | 93.5 (43/46), [85.7, 100.0], [82.4, 98.0] | same cell, `anchor_correct_share` |
| ordinal correct, matched bodies | 95.4 (188/197), 28, [89.4, 99.5], [85.2, 98.9] | same cell, `matched_correct` |
| ordinal within one (twin) | 100.0 (197/197), BCa undefined | same cell, `matched_within_one` |
| truth bodies at the right ordinal, defined frames | 81.0 (188/232), [73.8, 87.6], [73.5, 87.1] | same cell, `truth_correct_defined` |
| conf 0.25, counting defined (twin) | 91.1 (51/56), [83.9, 96.4], [82.1, 96.4] | CNT cell `lodo_carm` / `carm_test` / 0.25 / outline: `defined_share` |
| conf 0.25, ordinal correct | 84.7 (199/235), [77.4, 90.7], [76.5, 90.4] | same cell, `matched_correct` |
| conf 0.25, within one (twin) | 95.7 (225/235), [92.2, 98.7], [91.3, 98.3] | same cell, `matched_within_one` |
| COBRA2026, counting defined (twin) | 18.2 (111/609), 27, [13.4, 23.5], [13.5, 23.6] | CNT cell `lodo_cobra` / `cobra_test` / 0.25 / body: `defined_share` |
| COBRA2026, ordinal correct | 71.1 (54/76), 27, [56.6, 80.3], [57.7, 80.6] | same cell, `matched_correct` |
| DeepFluoro test specimen (twin) | 79.1 (53/67), one cluster | CNT cell `lodo_df` / `df_test` / 0.25 / body: `matched_correct` |
| pooled, counting defined (twin) | 33.4 (252/755), 56, [20.4, 50.5], [22.3, 57.5] | CNT `#pooled_across_devices[0]/defined_share` |
| pooled, ordinal correct | 81.0 (306/378), 56, [75.7, 85.8], [75.7, 85.8] | CNT `#pooled_across_devices[0]/matched_correct` |
| pooled, within one (twin) | 96.8 (366/378), [93.8, 98.8], [93.8, 98.8] | CNT `#pooled_across_devices[0]/matched_within_one` |
| footnote c, definitions and the outside check | | CNT `#definition`, `#interval`, `#outside_check` (both cells agree with a1.json's matching, 0 ordering differences) |

## Coupled rows

| row | value | file → field |
|---|---|---|
| conf 0.25, whole frame: classifier / count / coupled | 98.3 (1,129/1,149) [96.5, 99.6]; 96.1 (1,104/1,149) [93.5, 98.3]; 97.5 (1,120/1,149) [95.7, 99.0]; 139 cases | CPL `det~1kfull/classifier_exact_counted`, `count_exact_counted`, `coupled_exact_counted` |
| coupled minus count (twin) | +1.4 [0.0, 3.4] | CPL `det~1kfull/coupled_minus_count_counted` |
| coupled minus classifier (twin) | −0.7 [−2.4, 1.0], 143 cases | CPL `det~1kfull/coupled_minus_classifier` |
| disagreement frames | 6.8 (18/266), 142, [3.5, 10.2] | CPL `det~1kfull/disagreement_frames` |
| flag sensitivity | 90.0 (9/10), 10, [70.0, 100.0] | CPL `det~1kfull/flags/sensitivity_frame_error` |
| flag false alarm (twin) | 7.1 (18/252), 135, [3.9, 10.8] | CPL `det~1kfull/flags/false_alarm_frame_correct` |
| coupled exact on unflagged (twin) | 99.9 (1,040/1,041), 130, [99.7, 100.0] | CPL `det~1kfull/flags/coupled_exact_unflagged` |
| conf 0.74, whole frame (printed first since the statistical revision, F10): classifier / count / coupled; disagreement frames 5.2 (12/233) [2.5, 8.7], 132 cases | 98.4 (993/1,009) [96.8, 99.7]; 97.0 (979/1,009) [94.2, 99.2]; 98.6 (995/1,009) [97.2, 99.7]; 130 cases | CPL `det74~1kfull/...` (`classifier_exact_counted`, `count_exact_counted`, `coupled_exact_counted`, `disagreement_frames`); reproduced by `results/stats_review/recompute.json#R6_coupling_074` |
| five in field, conf 0.25 | 98.6 (654/663) [96.5, 100.0]; 88.5 (587/663) [83.9, 92.6]; 89.9 (596/663) [85.8, 93.5]; 105 cases | CPL `det~1k5/...` |
| oracle boxes (twin) | 94.7 (1,259/1,329) [91.8, 97.0]; 97.7 (1,298/1,329) [96.7, 98.5]; 95.9 (1,275/1,329) [94.1, 97.5]; 141 cases; the F1 caveat | CPL `oracle~1kfull/...`; `SchwingNet/results/COUPLING_CHECK.md` F1 (64 of 286 anchored frames double-boxed, 31 of 31 count-only errors in them) |
| frames and cases of the coupled block | 145 cases, 290 frames, 266 anchored | CPL `det~1kfull/cases`, `frames`, `frames_anchored` |
| footnote d, definitions | | CPL `#definitions` (classifier, coupled, count, anchor, ordinal, truth, intervals, tau) |

## Transitional rows

| row | value | file → field |
|---|---|---|
| held-out transitional persons | `\PENDING{G5}{transitional naming, counting and coupling}` | `docs/FLAGSHIP_PLAN.md` G3 (the split is not built), G5; `results/rare_class/transitional_subtypes.md` ("TotalSegmentator's 12 L6 subjects are all v9 training; the three C-ArmLSpine cases are the only transitional spines no level model has seen") |
| frames called L6 at conf 0.74 (truth five lumbar), each stopped: 1.7 (4/233), 132 clusters (3 with the call) | | CPL `#cells/det74~1kfull/calls_anchored` (`L6` 4), `/frames_anchored` 233, `/non_ordinary_calls` (`frames` 4, 3 cases, `flagged` 4); 132 = `/flags/frames_flagged_anchored/cases`; same as `figures/figure4.record.json` panel d `l6_calls_on_agreed_five_lumbar` |
| three C-ArmLSpine cases, conf 0.74: coupled call L6 on 1 of 4 anchored frames | | CPL `#l6_patients[arm=det74, field=full]` (six frames; case121 AP and LAT unanchored; case42 LAT called L6, flagged `disagreement`); `figures/figure4.record.json` panel d `l6_calls_on_them` |
| three C-ArmLSpine cases read as L6: coupled 1 of 5, classifier 0 of 5 | | CPL `#cells_with_veridah_l6/det~1kfull/per_level/L6` (`n` 5, `classifier` 0.0, `coupled` 0.2); `#l6_patients[]` (frames of case42, case121, case136); `#definitions/truth` (`truth_source = variant_alphabet:L6`) |
| footnote e, the VERIDAH read | L1–L5 against L2–L6 on a lumbar-only CBCT | `results/rare_class/transitional_subtypes.csv` rows `carmlspine_real` (notes); `SchwingNet/CLAIMS_LEDGER.md` §6 |

Statistical revision 2026-09-23 (REVIEW_STATS F3, F10, F20): the percentile column prints the Wilson interval on the design-effect-adjusted count (`wilson_effective_n`) wherever the cell's result file flags `ceiling_regime`; the coupled block leads with confidence 0.74, the cross-device point the Results quote; the five-in-field coupling rows moved to the Markdown twin (their classifier interval reached 100 % with 9 errors and no per-frame file is here to compute a Wilson interval); footnote f names the checkpoint-selection split and the three-body rates (`a5.json#per_protocol/maximal_band3`).
