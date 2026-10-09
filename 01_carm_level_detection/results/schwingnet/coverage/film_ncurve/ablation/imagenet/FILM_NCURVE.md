# Film N-curve, arm imagenet (generated 2026-09-25T20:40:54; 48 of 48 cells scored)

Arm: ablation: ImageNet init (no render pretraining), the SAME merged bank (render base + N film persons), 15 epochs.

Naming accuracy on the fixed v9 VAL films of each corpus against N training PERSONS of that corpus (tools/film_ncurve.py docstring). Random-length windows (2..9 vertebrae), exact level, patient-clustered percentile intervals. Nothing here is interpreted; the fit is tools/indomain_fit_coverage.py.

## nhanes

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 29.9 | s0 31.4 [24.7, 37.9]; s1 34.2 [27.9, 40.8]; s2 24.1 [18.2, 30.1] | buu_full 8.2, csxa 5.4 |
| 5 (5) | 3 | 48 | 75.5 | s0 72.2 [67.3, 76.9]; s1 79.5 [75.0, 83.6]; s2 74.8 [70.4, 79.2] | buu_full 43.0, csxa 10.4 |
| 10 (10) | 3 | 103 | 79.1 | s0 80.1 [76.0, 84.1]; s1 79.5 [74.9, 84.1]; s2 77.7 [73.1, 82.1] | buu_full 53.1, csxa 48.8 |
| 25 (25) | 3 | 229 | 83.0 | s0 83.4 [78.9, 87.6]; s1 83.0 [79.2, 86.8]; s2 82.6 [78.6, 86.1] | buu_full 55.6, csxa 21.6 |
| 50 (50) | 1 | 467 | 86.1 | s0 86.1 [82.2, 89.8] | buu_full 61.0, csxa 61.5 |
| 100 (100) | 1 | 891 | 86.8 | s0 86.8 [82.8, 90.5] | buu_full 65.5, csxa 62.3 |
| 200 (200) | 1 | 1774 | 89.8 | s0 89.8 [86.0, 93.5] | buu_full 67.6, csxa 72.2 |
| all (264) | 1 | 2357 | 92.3 | s0 92.3 [89.1, 95.2] | buu_full 66.4, csxa 62.1 |

## buu_full

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 18.1 | s0 11.4 [10.0, 12.9]; s1 23.5 [21.7, 25.2]; s2 19.4 [17.8, 21.2] | nhanes 25.8, csxa 4.9 |
| 5 (5) | 3 | 25 | 60.0 | s0 56.2 [54.4, 58.0]; s1 61.0 [59.1, 62.9]; s2 62.9 [61.2, 64.7] | nhanes 41.5, csxa 0.6 |
| 10 (10) | 3 | 50 | 67.6 | s0 71.3 [69.5, 73.1]; s1 66.6 [64.7, 68.5]; s2 65.0 [63.1, 67.0] | nhanes 45.0, csxa 0.4 |
| 25 (25) | 3 | 125 | 73.7 | s0 74.3 [72.3, 76.2]; s1 73.1 [71.1, 75.1]; s2 73.8 [71.9, 75.6] | nhanes 48.3, csxa 0.4 |
| 50 (50) | 1 | 250 | 79.3 | s0 79.3 [77.3, 81.3] | nhanes 47.2, csxa 0.1 |
| 100 (100) | 1 | 500 | 84.1 | s0 84.1 [82.2, 85.9] | nhanes 45.9, csxa 0.2 |
| 200 (200) | 1 | 1000 | 85.5 | s0 85.5 [83.6, 87.3] | nhanes 44.1, csxa 0.2 |
| all (2967) | 1 | 14844 | 97.2 | s0 97.2 [96.4, 98.0] | nhanes 45.7, csxa 0.1 |

## csxa

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 2.2 | s0 4.1 [3.4, 4.8]; s1 0.0 [0.0, 0.1]; s2 2.6 [1.9, 3.3] | nhanes 24.9, buu_full 13.9 |
| 5 (5) | 3 | 25 | 91.2 | s0 87.8 [86.6, 89.1]; s1 94.2 [93.3, 95.2]; s2 91.5 [90.3, 92.7] | nhanes 34.7, buu_full 3.5 |
| 10 (10) | 3 | 50 | 91.7 | s0 92.0 [90.8, 93.2]; s1 90.3 [88.9, 91.7]; s2 92.7 [91.6, 93.8] | nhanes 32.5, buu_full 4.1 |
| 25 (25) | 3 | 125 | 91.9 | s0 92.4 [91.4, 93.6]; s1 89.8 [88.4, 91.1]; s2 93.6 [92.5, 94.7] | nhanes 22.5, buu_full 4.0 |
| 50 (50) | 1 | 250 | 95.9 | s0 95.9 [95.0, 96.8] | nhanes 18.8, buu_full 4.5 |
| 100 (100) | 1 | 500 | 96.6 | s0 96.6 [95.7, 97.4] | nhanes 34.2, buu_full 12.1 |
| 200 (200) | 1 | 1000 | 97.5 | s0 97.5 [96.9, 98.2] | nhanes 33.8, buu_full 2.5 |
| all (4114) | 1 | 20570 | 99.8 | s0 99.8 [99.6, 99.9] | nhanes 40.8, buu_full 3.7 |

Encoder (render only): val exact None, n_train None, init None

Cells not scored: 0

