# Table 3 (printed third since 2026-09-24, when the LevelCheck table moved to paper 2; Table 4 in the 2026-09-23 six-figure wrap) — Level naming, counting and coupling (same rows as `tab3_naming.tex`, plus the rows the page could not hold; cell sources in `tab3_naming.sources.md`)

Level naming by morphology, counting from the detected sacrum, and the coupled call, per stratum and field size: each row is one share with its numerator and denominator, the clusters it is bootstrapped over and its 95 % interval. Rows marked **twin only** are in this file and `NUMBERS.md` but not on the printed page.

| Mechanism | Test set; stratum; grouping | View; field (b); operating point | Measure | % (k/n) | Clusters (with an error) | 95 % percentile | BCa |
|---|---|---|---|---|---|---|---|
| Morphology (level model) | C-ArmLSpine, agreed truth (a); case-grouped folds | lateral; whole frame | exact level, full coverage | 98.2 (606/617) | 141 (3) | Wilson (g) [94.6, 99.4]; percentile [95.7, 100.0] | [95.0, 99.5] |
| | | lateral; whole frame | within one level | 100.0 (617/617) | 141 (0) | [100.0, 100.0] | degenerate (twin only) |
| | | lateral; whole frame | cases with every vertebra right | 97.9 (138/141) | 141 | Wilson [93.9, 99.3] | — (twin only) |
| | | lateral; whole frame | answered at the default abstention rule | 83.1 (513/617) | 141 | [79.7, 86.3] | [79.5, 86.2] (twin only) |
| | | lateral; whole frame | exact on the answered share | 98.4 (505/513) | 141 (3) | Wilson (g) [95.1, 99.5]; percentile [96.2, 100.0] | [95.0, 99.6] (twin only) |
| | | AP; whole frame | exact level | 96.7 (610/631) | 142 (6) | Wilson (g) [92.7, 98.5]; percentile [93.6, 99.1] | [92.9, 98.7] |
| | | AP; whole frame | answered at the default rule | 77.3 (488/631) | 142 | [74.2, 80.5] | [74.0, 80.3] (twin only) |
| | | AP; whole frame | exact on the answered share | 97.5 (476/488) | 142 | Wilson (g) [94.6, 98.9]; percentile [95.3, 99.4] | [94.6, 99.0] (twin only) |
| | | lateral; five in field | exact level | 97.0 (647/667) | 131 (4) | Wilson (g) [91.5, 99.0]; percentile [93.3, 99.8] | [91.7, 99.2] (twin only) |
| | | lateral; three in field | exact level | 92.9 (1,079/1,162) | 142 (29) | [89.6, 95.6] | [89.1, 95.4] |
| | | lateral; one in field | exact level | 72.8 (440/604) | 142 (103) | [69.0, 76.2] | [69.0, 76.2] |
| | | AP; five in field | exact level | 95.1 (654/688) | 125 (7) | [91.1, 98.3] | [90.0, 97.8] (twin only) |
| | | AP; three in field | exact level | 86.3 (1,015/1,176) | 143 (62) | [83.1, 89.4] | [83.0, 89.3] (twin only) |
| | | AP; one in field | exact level | 65.1 (385/591) | 143 (114) | [61.6, 68.8] | [61.6, 68.7] (twin only) |
| | the same; day-grouped folds | lateral; whole frame | exact level | 92.5 (571/617) | 141 | [87.7, 96.4] | [87.0, 96.1] |
| | | lateral; whole frame | within one level | 95.1 (587/617) | 141 | — | — (twin only) |
| | | AP; whole frame | exact level | 96.7 (610/631) | 142 | [93.7, 99.1] | [92.7, 98.7] (twin only) |
| | | lateral; three in field | exact level | 87.6 (1,018/1,162) | 142 | [83.3, 91.6] | [82.3, 91.2] (twin only) |
| | | lateral; one in field | exact level | 66.6 (402/604) | 142 | [62.6, 70.6] | [62.4, 70.4] (twin only) |
| | the same; no C-ArmLSpine frame in training | lateral; whole frame | exact level | 96.3 (594/617) | 141 (6) | Wilson (g) [92.0, 98.3]; percentile [93.1, 98.7] | [92.3, 98.5] |
| | | AP; whole frame | exact level | 37.9 (239/631) | 142 (91) | [29.6, 45.9] | [30.1, 46.4] |
| | the same; truth boxes at complete coverage, case-grouped | lateral; whole frame | exact level | 93.6 (633/676) | 143 | [90.0, 96.8] | — (twin only) |
| | CSXA selection split (f) | cervical lateral | exact level | 99.8 (3,629/3,635) | 727 patients (3) | Wilson (g) [99.5, 99.9]; percentile [99.6, 100.0] | [99.5, 99.9] |
| | BUU-LSPINE selection split (f) | lumbar lateral | exact level | 97.3 (2,671/2,744) | 549 (51) | [96.5, 98.0] | [96.4, 98.0] |
| | NHANES II selection split (f) | lateral | exact level | 99.1 (441/445) | 52 patients (4) | Wilson (g) [97.8, 99.6]; percentile [98.2, 99.8] | [98.0, 99.8] |
| Count from the detected sacrum, no classifier (c) | C-ArmLSpine test, reported detector | whole frame; conf 0.74 | counting defined (a sacrum detected) | 82.1 (46/56) | 28 | [69.6, 92.9] | [69.6, 91.1] |
| | | | detected sacrum is the true sacrum | 93.5 (43/46) | 28 | [85.7, 100.0] | [82.4, 98.0] (twin only) |
| | | | ordinal correct, matched bodies | 95.4 (188/197) | 28 | [89.4, 99.5] | [85.2, 98.9] |
| | | | ordinal within one, matched bodies | 100.0 (197/197) | 28 | [100.0, 100.0] | undefined (twin only) |
| | | | truth bodies at the right ordinal, defined frames | 81.0 (188/232) | 28 | [73.8, 87.6] | [73.5, 87.1] |
| | | whole frame; conf 0.25 | counting defined | 91.1 (51/56) | 28 | [83.9, 96.4] | [82.1, 96.4] (twin only) |
| | | | ordinal correct, matched bodies | 84.7 (199/235) | 28 | [77.4, 90.7] | [76.5, 90.4] |
| | | | ordinal within one, matched bodies | 95.7 (225/235) | 28 | [92.2, 98.7] | [91.3, 98.3] (twin only) |
| | COBRA2026 test, held-out detector | conf 0.25 | counting defined | 18.2 (111/609) | 27 | [13.4, 23.5] | [13.5, 23.6] (twin only) |
| | | | ordinal correct, matched bodies | 71.1 (54/76) | 27 | [56.6, 80.3] | [57.7, 80.6] |
| | DeepFluoro test specimen (90 frames with a sacrum), held-out detector | conf 0.25 | ordinal correct, matched bodies | 79.1 (53/67) | 1 | one cluster | — (twin only) |
| | pooled over the three held-out devices | conf 0.25 | counting defined | 33.4 (252/755) | 56 | [20.4, 50.5] | [22.3, 57.5] (twin only) |
| | | | ordinal correct, matched bodies | 81.0 (306/378) | 56 | [75.7, 85.8] | [75.7, 85.8] |
| | | | ordinal within one, matched bodies | 96.8 (366/378) | 56 | [93.8, 98.8] | [93.8, 98.8] (twin only) |
| Coupled: classifier and count (d) | C-ArmLSpine folds, agreed truth | whole frame; conf 0.25 | classifier alone, counted bodies | 98.3 (1,129/1,149) | 139 | [96.5, 99.6] | — |
| | | | count alone | 96.1 (1,104/1,149) | 139 | [93.5, 98.3] | — |
| | | | coupled | 97.5 (1,120/1,149) | 139 | [95.7, 99.0] | — |
| | | | coupled minus count, percentage points | +1.4 | 139 | [0.0, 3.4] | — (twin only) |
| | | | coupled minus classifier, percentage points | −0.7 | 143 | [−2.4, 1.0] | — (twin only) |
| | | | disagreement frames (the stop signal) | 6.8 (18/266) | 142 | [3.5, 10.2] | — |
| | | | flag sensitivity to a frame with an error | 90.0 (9/10) | 10 | [70.0, 100.0] | — (twin only) |
| | | | flag false alarm on correct frames | 7.1 (18/252) | 135 | [3.9, 10.8] | — (twin only) |
| | | | coupled exact on unflagged frames | 99.9 (1,040/1,041) | 130 | [99.7, 100.0] | — (twin only) |
| | | whole frame; conf 0.74 (printed first, the Results quote it) | classifier alone | 98.4 (993/1,009) | 130 | [96.8, 99.7] | — |
| | | | count alone | 97.0 (979/1,009) | 130 | [94.2, 99.2] | — |
| | | | coupled | 98.6 (995/1,009) | 130 | [97.2, 99.7] | — |
| | | | disagreement frames (the stop signal) | 5.2 (12/233) | 132 | [2.5, 8.7] | — |
| | | | L6 calls on five-lumbar frames, all stopped | 1.7 (4/233) | 132 (3) | — | — |
| | | | coupled minus count, percentage points | +1.6 | 130 | [0.0, 3.8] | — (twin only) |
| | | | coupled minus classifier, percentage points (same 1,009 bodies) | +0.2 | 130 | [−1.7, 2.1] | — (twin only) |
| | | | flag sensitivity to a frame with an error | 80.0 (4/5) | 5 | [40.0, 100.0], five clusters, descriptive | — (twin only) |
| | | | flag false alarm on correct frames | 7.6 (17/225) | 128 | [4.0, 11.6] | — (twin only) |
| | | | coupled exact on unflagged bodies | 99.9 (921/922) | 123 | percentile [99.7, 100.0] (one error; not a valid interval, see g) | — (twin only) |
| | | five in field; conf 0.25 | classifier alone | 98.6 (654/663) | 105 | — (percentile [96.5, 100.0] reached 100 % with 9 errors; no per-frame file here for a Wilson interval) | — (twin only) |
| | | | count alone | 88.5 (587/663) | 105 | [83.9, 92.6] | — (twin only) |
| | | | coupled | 89.9 (596/663) | 105 | [85.8, 93.5] | — (twin only) |
| | the same; truth boxes and truth sacrum (oracle; 64 of 286 anchored frames carry a truth body boxed twice, and all 31 count-only errors lie in them) | whole frame | classifier alone | 94.7 (1,259/1,329) | 141 | [91.8, 97.0] | — (twin only) |
| | | | count alone | 97.7 (1,298/1,329) | 141 | [96.7, 98.5] | — (twin only) |
| | | | coupled | 95.9 (1,275/1,329) | 141 | [94.1, 97.5] | — (twin only) |
| Transitional, real exposures | three C-ArmLSpine cases read as L6 by one labeller (e) (Table 2) | whole frame; conf 0.25 | agrees with that read on the L6 body: coupled; classifier | 1 of 5; 0 of 5 | 3 | no interval | — |
| | | whole frame; conf 0.74 | anchored frames called L6 | 1 of 4 | 3 | no interval | — |

AP = anteroposterior; BCa = bias-corrected and accelerated bootstrap interval; conf = detector confidence threshold. Intervals are 95 % bootstraps of 2,000 resamples clustered by case (intraoperative) or patient (film); "—" = not computed.

- (a) Agreed truth = the levels both automatic CBCT labellers name (814 of 910 vertebrae), which withholds T11 and most of T12; ordinary spines. Case-grouped = five folds by case, day-grouped = three folds by acquisition day (a C-ArmLSpine case is an acquisition session, not a proven person); "with an error" counts the clusters carrying at least one error.
- (b) Field: whole frame, or crops holding five, three or one vertebra. Exact level scores every vertebra the film-trained keypoint detector (`detector_v5z_final`, confidence 0.35, never shown C-ArmLSpine) boxed, on its decoded name: 617 of 676 agreed lateral vertebrae; with the 59 undetected counted wrong, zero-shot 87.9 % (594/676), case-grouped 89.6 % (606/676) (`stats_review/recompute.json#R5_ceiling`); the untuned abstention rule withholds a name when the decoded and single-crop names disagree or the posterior is below 0.5.
- (c) Ordinal = rank of the detected body along the spine axis away from the detected sacrum, scored name-free against the same rank from the truth sacrum; counting is defined on a frame when truth has a sacrum and one was detected; bodies match one-to-one at intersection over union ≥ 0.5 in the whole-vertebra convention of Table 2; a missed truth body counts as wrong in the defined-frames row. C-ArmLSpine test = 28 cases, 56 AP and lateral frames, the reported detector, which never saw the device; COBRA2026 test = 27 patients, 609 frames with a sacrum at all gantry angles, the detector trained on DeepFluoro and C-ArmLSpine real frames; pooled = each real-frame detector on the device it never saw.
- (d) C-ArmLSpine five-fold CV frames with agreed truth (145 cases, 290 frames), the sacrum from the held-out detector. Classifier = the level model's name; count = the ordinary alphabet at the ordinal (L5 at one); coupled = the alphabet (ordinary, L6, T13, both) that best fits the classifier's posteriors at the ordinals; percentile intervals only.
- (e) Agreement with that read, not correctness: the two labellers segment the same five bodies and disagree only on the names (L1–L5 against L2–L6) on a lumbar-only CBCT; six frames, three clusters, no interval.
- (f) Patient-keyed validation split, the same split that chose the encoder checkpoint (`tools/train_level_classifier.py` keeps the best validation epoch), so these are validation accuracies with a small optimism, single seed; random window of two to nine bodies; at three bodies (`a5.json#per_protocol/maximal_band3`) BUU-LSPINE 95.0 % (2,606/2,744), CSXA 99.6 % (3,622/3,635), NHANES II 94.6 % (421/445); three seeds of the later v9 bank give NHANES II 96.9–97.6 % (`v9_a5_seeds.json`); NHANES II 76 films of 52 patients.
- (g) Wilson 95 % interval on the design-effect-adjusted count (`wilson_effective_n` of the cell in `a4.json`, `a7.json`, `a5.json`), replacing the percentile interval where the result file flags errors concentrated in few clusters (`ceiling_regime`; REVIEW_STATS F3). Twin-only rows whose percentile limit reaches 100 % with errors observed and whose file carries no Wilson interval (detected sacrum is the true sacrum 43/46; flag sensitivity 9/10 and 4/5; coupled exact on unflagged bodies) are kept for the record and are not valid intervals.
