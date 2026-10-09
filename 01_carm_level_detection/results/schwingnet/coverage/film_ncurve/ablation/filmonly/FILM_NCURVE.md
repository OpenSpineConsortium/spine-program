# Film N-curve, arm filmonly (generated 2026-09-25T23:25:01; 39 of 48 cells scored)

Arm: ablation: ImageNet init, the merged bank with every render row removed (the N persons' crops at the same oversampled count, the selection crops as val), 15 epochs; no N = 0 cell (nothing to train on).

Naming accuracy on the fixed v9 VAL films of each corpus against N training PERSONS of that corpus (tools/film_ncurve.py docstring). Random-length windows (2..9 vertebrae), exact level, patient-clustered percentile intervals. Nothing here is interpreted; the fit is tools/indomain_fit_coverage.py.

## nhanes

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 5 (5) | 3 | 48 | 55.9 | s0 51.7 [47.5, 56.3]; s1 56.1 [50.6, 61.9]; s2 60.0 [55.5, 64.6] | buu_full 31.8, csxa 2.8 |
| 10 (10) | 3 | 103 | 65.2 | s0 67.8 [63.5, 72.5]; s1 64.9 [59.7, 69.9]; s2 62.9 [58.6, 67.3] | buu_full 40.8, csxa 10.9 |
| 25 (25) | 3 | 229 | 75.6 | s0 77.0 [72.4, 81.7]; s1 75.5 [70.3, 80.2]; s2 74.4 [69.5, 79.0] | buu_full 55.8, csxa 17.8 |
| 50 (50) | 1 | 467 | 81.5 | s0 81.5 [77.1, 85.6] | buu_full 62.2, csxa 30.1 |
| 100 (100) | 1 | 891 | 85.7 | s0 85.7 [81.9, 89.0] | buu_full 61.5, csxa 37.5 |
| 200 (200) | 1 | 1774 | 90.1 | s0 90.1 [86.4, 93.4] | buu_full 70.5, csxa 38.0 |
| all (264) | 1 | 2357 | 92.0 | s0 92.0 [88.7, 94.9] | buu_full 73.2, csxa 40.6 |

## buu_full

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 5 (5) | 3 | 25 | 53.9 | s0 54.3 [52.6, 56.0]; s1 54.6 [52.9, 56.2]; s2 52.7 [51.1, 54.4] | nhanes 23.8, csxa 0.0 |
| 10 (10) | 3 | 50 | 60.6 | s0 64.2 [62.3, 66.2]; s1 58.3 [56.5, 59.9]; s2 59.3 [57.5, 61.1] | nhanes 26.5, csxa 0.0 |
| 25 (25) | 3 | 125 | 70.7 | s0 70.9 [69.0, 72.8]; s1 68.1 [66.1, 69.9]; s2 72.9 [71.1, 74.8] | nhanes 29.1, csxa 0.0 |
| 50 (50) | 1 | 250 | 77.7 | s0 77.7 [75.9, 79.6] | nhanes 28.9, csxa 0.0 |
| 100 (100) | 1 | 500 | 83.8 | s0 83.8 [81.9, 85.6] | nhanes 32.0, csxa 0.0 |
| 200 (200) | 1 | 1000 | 87.2 | s0 87.2 [85.3, 89.0] | nhanes 34.7, csxa 0.0 |
| all (2967) | 1 | 14844 | 98.5 | s0 98.5 [98.0, 99.0] | nhanes 34.4, csxa 0.0 |

## csxa

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 5 (5) | 3 | 25 | 75.4 | s0 68.0 [66.6, 69.5]; s1 79.2 [77.8, 80.6]; s2 79.1 [77.6, 80.5] | nhanes 12.6, buu_full 0.0 |
| 10 (10) | 3 | 50 | 80.8 | s0 78.4 [77.0, 79.8]; s1 80.0 [78.4, 81.5]; s2 84.2 [82.8, 85.5] | nhanes 15.9, buu_full 0.0 |
| 25 (25) | 3 | 125 | 90.2 | s0 90.6 [89.5, 91.8]; s1 90.9 [89.6, 92.2]; s2 88.9 [87.6, 90.2] | nhanes 17.9, buu_full 0.0 |
| 50 (50) | 1 | 250 | 94.4 | s0 94.4 [93.5, 95.3] | nhanes 15.4, buu_full 0.0 |
| 100 (100) | 1 | 500 | 96.3 | s0 96.3 [95.5, 97.1] | nhanes 19.9, buu_full 0.0 |
| 200 (200) | 1 | 1000 | 97.0 | s0 97.0 [96.2, 97.7] | nhanes 20.3, buu_full 0.0 |
| all (4114) | 1 | 20570 | 99.9 | s0 99.9 [99.8, 100.0] | nhanes 25.2, buu_full 0.0 |

Encoder (render only): val exact None, n_train None, init None

Cells not scored: 9 -- ['nhanes_N0_s0', 'nhanes_N0_s1', 'nhanes_N0_s2', 'buu_full_N0_s0', 'buu_full_N0_s1', 'buu_full_N0_s2', 'csxa_N0_s0', 'csxa_N0_s1', 'csxa_N0_s2']

