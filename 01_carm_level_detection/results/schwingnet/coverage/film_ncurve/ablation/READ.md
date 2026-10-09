# Film N-curve ablation, read against the rule of REVISION_LOG3 section 13

Cells scored: renderonly 48, imagenet 48, filmonly 39 (film-only skips N = 0: nothing to train on).

## NHANES

| N persons | seeds | render-only (reported) | ImageNet init, same bank | film only | rule |
|---|---|---|---|---|---|
| 0 | 3 | **27.2** (24.9 [19.8, 30.2]; 28.3 [23.2, 33.1]; 28.3 [23.3, 33.6]) | **29.9** (31.4 [24.7, 37.9]; 34.2 [27.9, 40.8]; 24.1 [18.2, 30.1]) | not run | n/a |
| 5 | 3 | **77.8** (77.7 [73.0, 82.0]; 81.0 [77.0, 85.1]; 74.6 [69.5, 79.2]) | **75.5** (72.2 [67.3, 76.9]; 79.5 [75.0, 83.6]; 74.8 [70.4, 79.2]) | **55.9** (51.7 [47.5, 56.3]; 56.1 [50.6, 61.9]; 60.0 [55.5, 64.6]) | renders HELP (separated) |
| 10 | 3 | **82.3** (84.1 [80.0, 87.9]; 81.7 [77.7, 85.7]; 81.0 [76.5, 85.2]) | **79.1** (80.1 [76.0, 84.1]; 79.5 [74.9, 84.1]; 77.7 [73.1, 82.1]) | **65.2** (67.8 [63.5, 72.5]; 64.9 [59.7, 69.9]; 62.9 [58.6, 67.3]) | renders HELP (separated) |
| 25 | 3 | **87.8** (87.9 [84.7, 91.0]; 88.3 [85.0, 91.4]; 87.2 [83.5, 90.5]) | **83.0** (83.4 [78.9, 87.6]; 83.0 [79.2, 86.8]; 82.6 [78.6, 86.1]) | **75.6** (77.0 [72.4, 81.7]; 75.5 [70.3, 80.2]; 74.4 [69.5, 79.0]) | renders HELP (separated) |
| 50 | 1 | **89.2** (89.2 [86.1, 92.1]) | **86.1** (86.1 [82.2, 89.8]) | **81.5** (81.5 [77.1, 85.6]) | renders HELP (separated) |
| 100 | 1 | **89.6** (89.6 [86.1, 92.7]) | **86.8** (86.8 [82.8, 90.5]) | **85.7** (85.7 [81.9, 89.0]) | not separated |
| 200 | 1 | **92.5** (92.5 [89.2, 95.3]) | **89.8** (89.8 [86.0, 93.5]) | **90.1** (90.1 [86.4, 93.4]) | not separated |
| all | 1 | **92.7** (92.7 [89.5, 95.6]) | **92.3** (92.3 [89.1, 95.2]) | **92.0** (92.0 [88.7, 94.9]) | not separated |

## BUU

| N persons | seeds | render-only (reported) | ImageNet init, same bank | film only | rule |
|---|---|---|---|---|---|
| 0 | 3 | **10.3** (11.2 [9.9, 12.5]; 12.8 [11.6, 14.0]; 6.9 [6.0, 7.8]) | **18.1** (11.4 [10.0, 12.9]; 23.5 [21.7, 25.2]; 19.4 [17.8, 21.2]) | not run | n/a |
| 5 | 3 | **65.0** (65.1 [63.1, 67.2]; 67.6 [65.7, 69.5]; 62.2 [60.2, 64.2]) | **60.0** (56.2 [54.4, 58.0]; 61.0 [59.1, 62.9]; 62.9 [61.2, 64.7]) | **53.9** (54.3 [52.6, 56.0]; 54.6 [52.9, 56.2]; 52.7 [51.1, 54.4]) | renders HELP (separated) |
| 10 | 3 | **70.3** (70.8 [68.8, 72.7]; 73.0 [71.1, 74.9]; 67.2 [65.3, 69.0]) | **67.6** (71.3 [69.5, 73.1]; 66.6 [64.7, 68.5]; 65.0 [63.1, 67.0]) | **60.6** (64.2 [62.3, 66.2]; 58.3 [56.5, 59.9]; 59.3 [57.5, 61.1]) | renders HELP (separated) |
| 25 | 3 | **76.7** (77.0 [75.1, 78.8]; 75.6 [73.6, 77.6]; 77.4 [75.5, 79.3]) | **73.7** (74.3 [72.3, 76.2]; 73.1 [71.1, 75.1]; 73.8 [71.9, 75.6]) | **70.7** (70.9 [69.0, 72.8]; 68.1 [66.1, 69.9]; 72.9 [71.1, 74.8]) | renders HELP (separated) |
| 50 | 1 | **81.2** (81.2 [79.3, 83.0]) | **79.3** (79.3 [77.3, 81.3]) | **77.7** (77.7 [75.9, 79.6]) | not separated |
| 100 | 1 | **82.7** (82.7 [80.8, 84.5]) | **84.1** (84.1 [82.2, 85.9]) | **83.8** (83.8 [81.9, 85.6]) | not separated |
| 200 | 1 | **85.1** (85.1 [83.3, 86.8]) | **85.5** (85.5 [83.6, 87.3]) | **87.2** (87.2 [85.3, 89.0]) | not separated |
| all | 1 | **96.9** (96.9 [96.0, 97.8]) | **97.2** (97.2 [96.4, 98.0]) | **98.5** (98.5 [98.0, 99.0]) | renders HURT (separated) |

## CSXA

| N persons | seeds | render-only (reported) | ImageNet init, same bank | film only | rule |
|---|---|---|---|---|---|
| 0 | 3 | **3.2** (5.3 [4.4, 6.2]; 2.5 [1.9, 3.1]; 1.8 [1.3, 2.4]) | **2.2** (4.1 [3.4, 4.8]; 0.0 [0.0, 0.1]; 2.6 [1.9, 3.3]) | not run | n/a |
| 5 | 3 | **94.2** (93.9 [92.9, 94.7]; 94.3 [93.0, 95.4]; 94.5 [93.4, 95.4]) | **91.2** (87.8 [86.6, 89.1]; 94.2 [93.3, 95.2]; 91.5 [90.3, 92.7]) | **75.4** (68.0 [66.6, 69.5]; 79.2 [77.8, 80.6]; 79.1 [77.6, 80.5]) | renders HELP (separated) |
| 10 | 3 | **93.0** (93.6 [92.5, 94.6]; 90.7 [89.2, 92.2]; 94.7 [93.7, 95.7]) | **91.7** (92.0 [90.8, 93.2]; 90.3 [88.9, 91.7]; 92.7 [91.6, 93.8]) | **80.8** (78.4 [77.0, 79.8]; 80.0 [78.4, 81.5]; 84.2 [82.8, 85.5]) | renders HELP (separated) |
| 25 | 3 | **96.4** (97.2 [96.5, 97.9]; 96.3 [95.4, 97.2]; 95.6 [94.5, 96.6]) | **91.9** (92.4 [91.4, 93.6]; 89.8 [88.4, 91.1]; 93.6 [92.5, 94.7]) | **90.2** (90.6 [89.5, 91.8]; 90.9 [89.6, 92.2]; 88.9 [87.6, 90.2]) | renders HELP (separated) |
| 50 | 1 | **97.3** (97.3 [96.5, 98.0]) | **95.9** (95.9 [95.0, 96.8]) | **94.4** (94.4 [93.5, 95.3]) | renders HELP (separated) |
| 100 | 1 | **97.3** (97.3 [96.6, 98.0]) | **96.6** (96.6 [95.7, 97.4]) | **96.3** (96.3 [95.5, 97.1]) | not separated |
| 200 | 1 | **98.0** (98.0 [97.3, 98.6]) | **97.5** (97.5 [96.9, 98.2]) | **97.0** (97.0 [96.2, 97.7]) | not separated |
| all | 1 | **99.8** (99.8 [99.6, 99.9]) | **99.8** (99.8 [99.6, 99.9]) | **99.9** (99.9 [99.8, 100.0]) | not separated |

## Verdict at the pre-stated N (5, 25, largest)

- NHANES, N = 5: renders HELP (separated); render-only minus film-only = +21.9 points (mean over seeds)
- NHANES, N = 25: renders HELP (separated); render-only minus film-only = +12.2 points (mean over seeds)
- NHANES, N = all: not separated; render-only minus film-only = +0.7 points (mean over seeds)
- BUU, N = 5: renders HELP (separated); render-only minus film-only = +11.1 points (mean over seeds)
- BUU, N = 25: renders HELP (separated); render-only minus film-only = +6.0 points (mean over seeds)
- BUU, N = all: renders HURT (separated); render-only minus film-only = -1.6 points (mean over seeds)
- CSXA, N = 5: renders HELP (separated); render-only minus film-only = +18.7 points (mean over seeds)
- CSXA, N = 25: renders HELP (separated); render-only minus film-only = +6.2 points (mean over seeds)
- CSXA, N = all: not separated; render-only minus film-only = -0.2 points (mean over seeds)

Cells separated outside the intervals: 7 of 9. Mixed: see the table.

Every arm keeps its renders for the rare classes (L6, T13): no released film carries a human-read one. This test is about ordinary levels only.
