# The corpus manifold

15154 frames from 38 sets (cap 500 per set), two feature spaces: `stats` = 37 image statistics (device_physics.image_stats), standardised inside each fold; `deep` = resnet50 avgpool (2048-d), standardised then PCA-256 fitted inside each fold. Classifiers: sklearn LinearSVC C=1 and sklearn LogisticRegression C=1 lbfgs. Clusters: person / specimen / phantom / CT subject / acquisition day (C-ArmLSpine), never the frame. Intervals: 2.5-97.5 percentiles of 2,000 cluster-resamples of the pooled out-of-fold predictions. Excluded from everything: FluoroCap grainy, FluoroCap real, Open-i, PMC 18M, PMC figure panels, Wikimedia Commons, yolo_v6f fluoro. Dropped as duplicates of another set: BUU-LSPINE (kept BUU-LSPINE AP + LA), CSXA (kept CSXA raw), NHANES II (kept NHANES II full), Mendeley raw (kept Mendeley). Embedded but not probed (earlier render generations): calibrated Cios render, physics rare, physics render.

## Sets

| set | source | modality | frames | clusters | probed |
|---|---|---|---|---|---|
| AASCE | AASCE | film | 481 | 370 | yes |
| BUU-LSPINE | BUU-LSPINE | film | 500 | 485 | no |
| BUU-LSPINE AP | BUU-LSPINE | film | 500 | 500 | yes |
| BUU-LSPINE LA | BUU-LSPINE | film | 500 | 500 | yes |
| C-ArmLSpine | C-ArmLSpine | fluoroscopy | 296 | 3 | yes |
| COBRA Elekta | COBRA Elekta | kV imager | 499 | 144 | yes |
| COBRA Varian | COBRA Varian | kV imager | 500 | 12 | yes |
| CSXA | CSXA | film | 500 | 500 | no |
| CSXA raw | CSXA | film | 499 | 499 | yes |
| DRR CTSpinoPelvic1K | DRR CTSpinoPelvic1K | vanilla DRR | 500 | 500 | yes |
| DRR TotalSegmentator | DRR TotalSegmentator | vanilla DRR | 454 | 454 | yes |
| DRR VerSe | DRR VerSe | vanilla DRR | 387 | 387 | yes |
| DeepFluoro | DeepFluoro | fluoroscopy | 366 | 6 | yes |
| Geneva | Geneva | fluoroscopy | 116 | 1 | yes |
| Lateral 236 | Lateral 236 | film | 236 | 236 | yes |
| Ljubljana | Ljubljana | film | 18 | 1 | yes |
| Mendeley | Mendeley | film | 500 | 500 | yes |
| Mendeley raw | Mendeley raw | film | 16 | 16 | no |
| NHANES II | NHANES II | film | 500 | 500 | no |
| NHANES II full | NHANES II | film | 500 | 500 | yes |
| SpineSAC | SpineSAC | fluoroscopy | 286 | 24 | yes |
| VinDr-SpineXR | VinDr-SpineXR | film | 500 | 500 | yes |
| calibrated Cios render | calibrated Cios render | styled DRR | 500 | 48 | no |
| physics rare | physics rare | physics render | 500 | 81 | no |
| physics render | physics render | physics render | 500 | 467 | no |
| render cios_fusion poses (unstyled) | unstyled render | vanilla DRR | 500 | 140 | yes |
| render elekta_xvi poses (unstyled) | unstyled render | vanilla DRR | 500 | 139 | yes |
| render surgio_b51_dr poses (unstyled) | unstyled render | vanilla DRR | 500 | 140 | yes |
| styled cios_fusion on cios_fusion poses | styled DRR | styled DRR | 370 | 17 | yes |
| styled cios_fusion on cios_fusion poses (typicality) | styled DRR | styled DRR | 370 | 17 | yes |
| styled elekta_xvi on cios_fusion poses | styled DRR | styled DRR | 370 | 17 | yes |
| styled elekta_xvi on cios_fusion poses (typicality) | styled DRR | styled DRR | 370 | 17 | yes |
| styled elekta_xvi on elekta_xvi poses | styled DRR | styled DRR | 272 | 17 | yes |
| styled elekta_xvi on elekta_xvi poses (typicality) | styled DRR | styled DRR | 272 | 17 | yes |
| styled surgio_b51_dr on cios_fusion poses | styled DRR | styled DRR | 370 | 17 | yes |
| styled surgio_b51_dr on cios_fusion poses (typicality) | styled DRR | styled DRR | 370 | 17 | yes |
| styled surgio_b51_dr on surgio_b51_dr poses | styled DRR | styled DRR | 370 | 17 | yes |
| styled surgio_b51_dr on surgio_b51_dr poses (typicality) | styled DRR | styled DRR | 366 | 17 | yes |

## (i) Film vs fluoroscopy, real frames only

Leave-one-source-out (the transfer number) beside case-grouped 5-fold (sources mixed across folds). Chance = majority share.

| space / classifier / variant | LOSO acc [CI] | LOSO bacc [CI] | LOSO AUC [CI] | case-grouped acc [CI] | chance | n (film + fluoro) |
|---|---|---|---|---|---|---|
| stats/svm/film_vs_carm_and_kv | 63.4% [57.6, 69.2] | 54.9% [50.0, 60.6] | 52.5% [43.9, 60.8] | 92.7% [89.6, 95.6] | 64.4% | 5797 (3734 + 2063) |
| stats/svm/film_vs_carm_only | 72.4% [63.9, 81.1] | 51.1% [46.2, 56.8] | 40.7% [25.9, 55.4] | 92.9% [88.5, 96.7] | 77.8% | 4798 (3734 + 1064) |
| stats/logistic/film_vs_carm_and_kv | 66.4% [60.7, 72.0] | 58.1% [52.8, 63.4] | 54.8% [45.6, 64.0] | 92.9% [90.1, 95.5] | 64.4% | 5797 (3734 + 2063) |
| stats/logistic/film_vs_carm_only | 73.7% [65.5, 82.0] | 55.1% [47.5, 65.8] | 50.0% [35.3, 63.8] | 95.6% [93.1, 97.9] | 77.8% | 4798 (3734 + 1064) |
| deep/svm/film_vs_carm_and_kv | 85.0% [79.4, 90.0] | 80.6% [73.6, 87.2] | 87.8% [78.0, 96.4] | 98.9% [98.3, 99.4] | 64.4% | 5797 (3734 + 2063) |
| deep/svm/film_vs_carm_only | 83.0% [74.6, 90.9] | 65.4% [51.7, 79.5] | 74.3% [61.6, 85.1] | 99.2% [98.6, 99.7] | 77.8% | 4798 (3734 + 1064) |
| deep/logistic/film_vs_carm_and_kv | 82.8% [77.1, 88.2] | 77.7% [70.8, 84.1] | 86.2% [75.4, 95.9] | 99.5% [99.2, 99.7] | 64.4% | 5797 (3734 + 2063) |
| deep/logistic/film_vs_carm_only | 81.9% [73.1, 90.8] | 61.1% [51.1, 72.4] | 65.4% [46.6, 80.6] | 99.5% [99.0, 99.8] | 77.8% | 4798 (3734 + 1064) |

Per held-out source (stats/svm/film_vs_carm_and_kv): accuracy = the share of its frames given the right modality, with the majority-of-training baseline.

| held-out source | label | n | clusters | acc [CI] | majority baseline |
|---|---|---|---|---|---|
| AASCE | film | 481 | 370 | 87.9% [85.0, 90.7] | 100.0% |
| BUU-LSPINE | film | 1000 | 921 | 86.9% [84.8, 89.0] | 100.0% |
| C-ArmLSpine | fluoro | 296 | 3 | 0.3% [0.0, 1.2] | 0.0% |
| COBRA Elekta | fluoro | 499 | 144 | 14.4% [11.7, 17.5] | 0.0% |
| COBRA Varian | fluoro | 500 | 12 | 21.8% [12.1, 31.1] | 0.0% |
| CSXA | film | 499 | 499 | 67.1% [63.1, 71.3] | 100.0% |
| DeepFluoro | fluoro | 366 | 6 | 43.7% [22.9, 66.9] | 0.0% |
| Geneva | fluoro | 116 | 1 | 100.0% [100.0, 100.0] | 0.0% |
| Lateral 236 | film | 236 | 236 | 100.0% [100.0, 100.0] | 100.0% |
| Ljubljana | film | 18 | 1 | 0.0% [0.0, 0.0] | 100.0% |
| Mendeley | film | 500 | 500 | 95.8% [94.0, 97.4] | 100.0% |
| NHANES II | film | 500 | 500 | 89.6% [86.8, 92.2] | 100.0% |
| SpineSAC | fluoro | 286 | 24 | 24.1% [19.1, 54.0] | 0.0% |
| VinDr-SpineXR | film | 500 | 500 | 71.8% [67.8, 75.8] | 100.0% |

## (ii) Source identity, case-grouped 5-fold

| space / classifier | acc [CI] | balanced acc [CI] | chance (majority) | chance (1/K) | n |
|---|---|---|---|---|---|
| stats/svm | 90.9% [88.6, 92.5] | 79.8% [79.1, 80.9] | 28.8% | 5.3% | 12138 |
| stats/logistic | 92.1% [89.8, 93.7] | 81.2% [80.5, 82.3] | 28.8% | 5.3% | 12138 |
| deep/svm | 91.7% [89.3, 93.3] | 81.0% [80.0, 81.9] | 28.8% | 5.3% | 12138 |
| deep/logistic | 92.4% [89.9, 94.0] | 81.8% [80.8, 82.6] | 28.8% | 5.3% | 12138 |

Per-source recall (stats/svm):

| source | n | clusters | recall [CI] |
|---|---|---|---|
| AASCE | 481 | 370 | 93.6% [91.1, 95.7] |
| BUU-LSPINE | 1000 | 921 | 91.8% [90.1, 93.5] |
| C-ArmLSpine | 296 | 3 | 97.3% [93.6, 100.0] |
| COBRA Elekta | 499 | 144 | 93.8% [91.1, 96.4] |
| COBRA Varian | 500 | 12 | 94.0% [89.6, 97.5] |
| CSXA | 499 | 499 | 99.0% [98.0, 99.8] |
| DRR CTSpinoPelvic1K | 500 | 500 | 92.0% [89.6, 94.2] |
| DRR TotalSegmentator | 454 | 454 | 85.0% [81.5, 88.1] |
| DRR VerSe | 387 | 387 | 38.8% [33.9, 43.4] |
| DeepFluoro | 366 | 6 | 98.4% [97.0, 99.4] |
| Geneva | 116 | 1 | 0.0% [0.0, 0.0] |
| Lateral 236 | 236 | 236 | 96.6% [94.1, 98.7] |
| Ljubljana | 18 | 1 | 0.0% [0.0, 0.0] |
| Mendeley | 500 | 500 | 89.2% [86.4, 91.8] |
| NHANES II | 500 | 500 | 99.4% [98.6, 100.0] |
| SpineSAC | 286 | 24 | 84.6% [80.9, 100.0] |
| VinDr-SpineXR | 500 | 500 | 69.6% [65.4, 73.4] |
| styled DRR | 3500 | 17 | 97.1% [96.3, 97.7] |
| unstyled render | 1500 | 142 | 95.2% [93.3, 96.8] |

## (iii) The transfer test

Per device card: a render family against the real frames of that device, case-grouped 5-fold; the same CT subject never sits on both sides of a fold. Chance = majority share; balanced accuracy has chance 50%.

| device | comparison | space / clf | acc [CI] | bacc [CI] | AUC [CI] | chance | n (A + B) | clusters (A + B) |
|---|---|---|---|---|---|---|---|---|
| cios_fusion | vanilla_vs_real | stats/svm | 99.9% [99.5, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 6 |
| cios_fusion | vanilla_vs_real | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 6 |
| cios_fusion | vanilla_vs_real | stats/logistic | 99.9% [99.5, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 6 |
| cios_fusion | vanilla_vs_real | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 6 |
| cios_fusion | unstyled_vs_real | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 6 |
| cios_fusion | unstyled_vs_real | deep/svm | 99.9% [99.6, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 6 |
| cios_fusion | unstyled_vs_real | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 6 |
| cios_fusion | unstyled_vs_real | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses | stats/svm | 99.9% [99.5, 100.0] | 99.9% [99.5, 100.0] | 99.7% [99.1, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses | deep/logistic | 99.9% [99.5, 100.0] | 99.9% [99.5, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses | stats/svm | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 99.9% [99.8, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses | deep/svm | 98.0% [96.4, 99.3] | 97.9% [96.1, 99.3] | 99.6% [98.8, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses | stats/logistic | 99.7% [99.2, 100.0] | 99.7% [99.2, 100.0] | 99.6% [99.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses | deep/logistic | 97.8% [95.2, 99.7] | 97.4% [94.3, 99.6] | 99.6% [98.7, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses (typicality) | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses (typicality) | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | styled_vs_real|styled cios_fusion on cios_fusion poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.3% | 736 (370 + 366) | 17 + 6 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | vanilla_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | stats/svm | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 99.9% [99.8, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | deep/svm | 97.6% [96.2, 98.9] | 97.4% [95.7, 98.8] | 99.7% [99.2, 99.9] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 99.9% [99.7, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| cios_fusion | unstyled_vs_styled|styled cios_fusion on cios_fusion poses (typicality) | deep/logistic | 97.1% [94.7, 99.1] | 96.7% [93.8, 98.9] | 99.6% [99.1, 99.9] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | vanilla_vs_real | stats/svm | 99.9% [99.5, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 60.5% | 750 (454 + 296) | 454 + 3 |
| surgio_b51_dr | vanilla_vs_real | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 60.5% | 750 (454 + 296) | 454 + 3 |
| surgio_b51_dr | vanilla_vs_real | stats/logistic | 99.9% [99.5, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 60.5% | 750 (454 + 296) | 454 + 3 |
| surgio_b51_dr | vanilla_vs_real | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 60.5% | 750 (454 + 296) | 454 + 3 |
| surgio_b51_dr | unstyled_vs_real | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.8% | 796 (500 + 296) | 140 + 3 |
| surgio_b51_dr | unstyled_vs_real | deep/svm | 99.9% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 62.8% | 796 (500 + 296) | 140 + 3 |
| surgio_b51_dr | unstyled_vs_real | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.8% | 796 (500 + 296) | 140 + 3 |
| surgio_b51_dr | unstyled_vs_real | deep/logistic | 99.6% [98.9, 100.0] | 99.5% [98.1, 100.0] | 100.0% [100.0, 100.0] | 62.8% | 796 (500 + 296) | 140 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses | deep/svm | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses | deep/logistic | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses | stats/svm | 99.8% [99.3, 100.0] | 99.8% [99.4, 100.0] | 99.8% [99.3, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses | stats/svm | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 100.0% [99.9, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses | deep/svm | 99.9% [99.6, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/svm | 99.7% [99.2, 100.0] | 99.7% [99.3, 100.0] | 99.7% [99.1, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/svm | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/logistic | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 99.9% [99.8, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/svm | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on cios_fusion poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses | stats/svm | 99.5% [98.7, 100.0] | 99.6% [98.9, 100.0] | 99.9% [99.7, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses | deep/svm | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses | stats/logistic | 99.5% [98.7, 100.0] | 99.6% [99.0, 100.0] | 99.9% [99.8, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses | deep/logistic | 99.8% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.6% | 666 (370 + 296) | 17 + 3 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | stats/svm | 99.4% [98.8, 99.9] | 99.4% [98.6, 99.9] | 100.0% [99.8, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 140 + 17 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/svm | 99.1% [97.7, 99.8] | 99.2% [98.3, 99.9] | 99.1% [98.1, 100.0] | 55.3% | 662 (366 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/svm | 99.8% [99.5, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.3% | 662 (366 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/logistic | 99.2% [98.3, 99.9] | 99.3% [98.5, 99.9] | 99.5% [98.4, 100.0] | 55.3% | 662 (366 + 296) | 17 + 3 |
| surgio_b51_dr | styled_vs_real|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/logistic | 99.8% [99.5, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 55.3% | 662 (366 + 296) | 17 + 3 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.3, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 17 |
| surgio_b51_dr | vanilla_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.4% | 820 (454 + 366) | 454 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/svm | 99.7% [99.2, 100.0] | 99.7% [99.3, 100.0] | 100.0% [99.9, 100.0] | 57.7% | 866 (500 + 366) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | stats/logistic | 99.8% [99.4, 100.0] | 99.8% [99.5, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 17 |
| surgio_b51_dr | unstyled_vs_styled|styled surgio_b51_dr on surgio_b51_dr poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 57.7% | 866 (500 + 366) | 140 + 17 |
| elekta_xvi | vanilla_vs_real | stats/svm | 99.9% [99.7, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 52.4% | 953 (454 + 499) | 454 + 144 |
| elekta_xvi | vanilla_vs_real | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 52.4% | 953 (454 + 499) | 454 + 144 |
| elekta_xvi | vanilla_vs_real | stats/logistic | 99.9% [99.7, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 52.4% | 953 (454 + 499) | 454 + 144 |
| elekta_xvi | vanilla_vs_real | deep/logistic | 99.9% [99.7, 100.0] | 99.9% [99.7, 100.0] | 100.0% [100.0, 100.0] | 52.4% | 953 (454 + 499) | 454 + 144 |
| elekta_xvi | unstyled_vs_real | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.1% | 999 (500 + 499) | 139 + 144 |
| elekta_xvi | unstyled_vs_real | deep/svm | 98.8% [97.9, 99.5] | 98.8% [97.9, 99.5] | 99.9% [99.8, 100.0] | 50.1% | 999 (500 + 499) | 139 + 144 |
| elekta_xvi | unstyled_vs_real | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 50.1% | 999 (500 + 499) | 139 + 144 |
| elekta_xvi | unstyled_vs_real | deep/logistic | 99.6% [99.1, 99.9] | 99.6% [99.1, 99.9] | 100.0% [100.0, 100.0] | 50.1% | 999 (500 + 499) | 139 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses | stats/svm | 99.4% [98.9, 99.9] | 99.4% [98.8, 99.8] | 99.5% [98.6, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses | deep/svm | 99.3% [98.7, 99.9] | 99.2% [98.4, 99.8] | 100.0% [99.9, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses | stats/logistic | 99.5% [99.1, 99.9] | 99.5% [98.9, 99.9] | 99.6% [98.9, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses | deep/logistic | 99.4% [98.8, 99.9] | 99.4% [98.8, 99.9] | 100.0% [99.9, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses | stats/svm | 99.7% [99.2, 100.0] | 99.6% [99.2, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses | deep/svm | 98.9% [98.1, 99.6] | 98.8% [98.0, 99.6] | 100.0% [99.9, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses | stats/logistic | 99.8% [99.4, 100.0] | 99.7% [99.3, 100.0] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses | deep/logistic | 98.9% [98.0, 99.6] | 98.7% [97.7, 99.6] | 100.0% [99.9, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses (typicality) | stats/svm | 99.2% [98.3, 99.9] | 99.1% [98.0, 99.9] | 99.1% [97.5, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses (typicality) | deep/svm | 99.5% [99.1, 99.9] | 99.5% [99.0, 99.9] | 100.0% [100.0, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses (typicality) | stats/logistic | 99.2% [98.2, 100.0] | 99.1% [97.9, 100.0] | 99.2% [98.0, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on cios_fusion poses (typicality) | deep/logistic | 99.4% [98.7, 100.0] | 99.4% [98.6, 100.0] | 100.0% [99.9, 100.0] | 57.4% | 869 (370 + 499) | 17 + 144 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | stats/svm | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | stats/logistic | 99.9% [99.6, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 55.1% | 824 (454 + 370) | 454 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | stats/svm | 99.4% [98.8, 99.9] | 99.4% [98.6, 99.9] | 99.5% [98.3, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | deep/svm | 99.4% [98.9, 99.9] | 99.4% [98.8, 99.8] | 100.0% [100.0, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | stats/logistic | 99.3% [98.7, 99.9] | 99.3% [98.5, 99.9] | 99.5% [98.5, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on cios_fusion poses (typicality) | deep/logistic | 98.9% [98.0, 99.6] | 98.7% [97.8, 99.6] | 100.0% [99.9, 100.0] | 57.5% | 870 (500 + 370) | 139 + 17 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses | stats/svm | 99.9% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses | deep/svm | 99.0% [98.1, 99.6] | 99.0% [98.1, 99.7] | 100.0% [99.9, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses | stats/logistic | 99.9% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses | deep/logistic | 99.7% [99.3, 100.0] | 99.7% [99.2, 100.0] | 100.0% [100.0, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses | stats/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses | stats/svm | 99.4% [98.6, 99.9] | 99.2% [98.3, 99.9] | 99.8% [99.4, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses | deep/svm | 98.8% [98.0, 99.6] | 98.9% [98.1, 99.6] | 99.9% [99.8, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses | stats/logistic | 99.2% [98.4, 99.9] | 99.1% [98.1, 99.9] | 100.0% [99.9, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses | deep/logistic | 98.7% [97.8, 99.6] | 98.3% [97.1, 99.5] | 99.9% [99.8, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses (typicality) | stats/svm | 99.9% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses (typicality) | deep/svm | 98.8% [97.9, 99.6] | 98.8% [97.7, 99.6] | 100.0% [99.9, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses (typicality) | stats/logistic | 99.9% [99.6, 100.0] | 99.8% [99.4, 100.0] | 100.0% [100.0, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | styled_vs_real|styled elekta_xvi on elekta_xvi poses (typicality) | deep/logistic | 99.1% [98.3, 99.7] | 98.9% [97.8, 99.7] | 100.0% [99.9, 100.0] | 64.7% | 771 (272 + 499) | 17 + 144 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | stats/svm | 99.9% [99.5, 100.0] | 99.9% [99.6, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | deep/svm | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | stats/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | vanilla_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | deep/logistic | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 100.0% [100.0, 100.0] | 62.5% | 726 (454 + 272) | 454 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | stats/svm | 99.5% [99.0, 99.9] | 99.4% [98.8, 99.9] | 99.9% [99.8, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | deep/svm | 98.6% [97.6, 99.4] | 98.6% [97.6, 99.5] | 99.8% [99.5, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | stats/logistic | 99.2% [98.6, 99.7] | 99.1% [98.4, 99.7] | 99.6% [98.8, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |
| elekta_xvi | unstyled_vs_styled|styled elekta_xvi on elekta_xvi poses (typicality) | deep/logistic | 98.8% [98.0, 99.6] | 98.5% [97.5, 99.5] | 99.9% [99.9, 100.0] | 64.8% | 772 (500 + 272) | 139 + 17 |

## (iv) Pairwise source separability

Balanced accuracy of a linear classifier told two sources apart, case-grouped 5-fold; chance 50%. Full matrices in `pairwise_<space>_<clf>.csv`.

| space / clf | min | median | max | pairs |
|---|---|---|---|---|
| stats/svm | 83.4% | 99.8% | 100.0% | 136 |
| stats/logistic | 83.7% | 99.8% | 100.0% | 136 |
| deep/svm | 82.3% | 99.9% | 100.0% | 136 |
| deep/logistic | 84.1% | 99.9% | 100.0% | 136 |

Embeddings: {"tsne_stats": {"perplexity": 30, "seed": 0, "init": "pca", "input_dim": 37, "seconds": 30.2}, "umap_stats": {"n_neighbors": 30, "min_dist": 0.2, "seed": 0, "input_dim": 37, "seconds": 42.6}, "tsne_deep": {"perplexity": 30, "seed": 0, "init": "pca", "input_dim": 50, "seconds": 33.1}, "umap_deep": {"n_neighbors": 30, "min_dist": 0.2, "seed": 0, "input_dim": 50, "seconds": 20.4}}

Deep backbone: {"torch": "2.6.0+cu124", "torchvision": "0.21.0+cu124", "preprocessing": "grey -> short side 256 -> centre crop 224 -> 3 channels -> ImageNet mean/sd", "layer": "avgpool", "backbone": "resnet50", "weights": "IMAGENET1K_V2 (torchvision)", "dim": 2048, "device": "cpu", "unreadable": 0, "n": 15154}

## Figure

`SchwingNet/tools/fig_manifold.py` -> `SchwingNet/figures/fig_manifold.{pdf,tif,png}` (7.0 x 9.05 in, smallest font 12 pt, every on-page number carried with its denominator and chance in `fig_manifold.record.json`).

- **(a) and (b)** draw the **deep** t-SNE (resnet50 avgpool -> PCA-50 -> t-SNE, perplexity 30, seed 0) of 11,638 frames from 18 sources: the in-figure frames (duplicates and earlier render generations excluded) minus Mendeley's 500, whose points and medoid label are kept out of both scatter panels because Mendeley duplicates BUU-LSPINE — its only appearance is the matrix row in (d). The deep space is the canvas because it is the only space in which the film/fluoroscopy boundary is visible at all; the stats t-SNE would draw a boundary panel for a probe that sits at chance.
- **(b)** writes both spaces' film-vs-C-arm/kV leave-one-source-out numbers on the panel — stats/svm 63.4 % [57.6, 69.2] (at chance) and deep/svm 85.0 % [79.4, 90.0] against chance 64.4 % (n = 5,797: 3,734 film + 2,063 C-arm/kV) — precisely so the two spaces can disagree in front of the reader: 37 image statistics do not carry modality across sources, ImageNet features partly do.
- **(c)** quotes **deep**/svm accuracies (case-grouped 5-fold, 95 % case-cluster intervals) for the three fitted device cards, one row per comparison, the styled-on-own-poses non-typicality card where one exists (every other card and both classifiers are in the record and in (iii) above; stats/svm reads the same). Deep is the harder space for the styling claim: a separation at ~100 % in ImageNet features cannot be dismissed as a first-order intensity residue. The panel states the finding plainly: vanilla vs styled 100.0 % — the styling measurably changes the image — while styled vs real still separates at 99.0–100.0 % (chance 50.3–64.7 %; n = 666–771 per pair), so the styling does not move the render to the real frame.
- **(d)** is the **deep**/svm pairwise matrix (balanced accuracy, case-grouped 5-fold, chance 50 %, 136 pairs), the matrix that holds the two informative low cells the text leans on: DRR TotalSegmentator vs DRR VerSe 0.823 and BUU-LSPINE vs Mendeley 0.919, both boxed and numbered on the panel (cells below 0.96). The Mendeley row is the set's only appearance in the figure, and its 0.92 against BUU-LSPINE is the evidence for excluding it from (a) and (b) as a duplicate. Geneva and Ljubljana are dropped from the matrix — one acquisition cluster each, so no case-grouped pair is evaluable.

The stats-space variant of the whole page is one command for the supplement: `python SchwingNet/tools/fig_manifold.py --space stats --suffix _supp`.
