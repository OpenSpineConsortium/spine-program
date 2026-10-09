# Film N-curve (generated 2026-09-24T23:25:30; 48 of 48 cells scored)

Naming accuracy on the fixed v9 VAL films of each corpus against N training PERSONS of that corpus; the encoder is the film-free render-only encoder fine-tuned per cell (tools/film_ncurve.py docstring). Random-length windows (2..9 vertebrae), exact level, patient-clustered percentile intervals. Nothing here is interpreted; the fit is tools/indomain_fit_coverage.py.

## nhanes

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 27.2 | s0 24.9 [19.8, 30.2]; s1 28.3 [23.2, 33.1]; s2 28.3 [23.3, 33.6] | buu_full 8.6, csxa 0.6 |
| 5 (5) | 3 | 48 | 77.8 | s0 77.7 [73.0, 82.0]; s1 81.0 [77.0, 85.1]; s2 74.6 [69.5, 79.2] | buu_full 47.8, csxa 22.5 |
| 10 (10) | 3 | 103 | 82.3 | s0 84.1 [80.0, 87.9]; s1 81.7 [77.7, 85.7]; s2 81.0 [76.5, 85.2] | buu_full 52.4, csxa 64.8 |
| 25 (25) | 3 | 229 | 87.8 | s0 87.9 [84.7, 91.0]; s1 88.3 [85.0, 91.4]; s2 87.2 [83.5, 90.5] | buu_full 62.5, csxa 62.9 |
| 50 (50) | 1 | 467 | 89.2 | s0 89.2 [86.1, 92.1] | buu_full 64.7, csxa 68.5 |
| 100 (100) | 1 | 891 | 89.6 | s0 89.6 [86.1, 92.7] | buu_full 65.3, csxa 71.1 |
| 200 (200) | 1 | 1774 | 92.5 | s0 92.5 [89.2, 95.3] | buu_full 68.1, csxa 74.3 |
| all (264) | 1 | 2357 | 92.7 | s0 92.7 [89.5, 95.6] | buu_full 73.2, csxa 66.2 |

## buu_full

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 10.3 | s0 11.2 [9.9, 12.5]; s1 12.8 [11.6, 14.0]; s2 6.9 [6.0, 7.8] | nhanes 30.7, csxa 0.9 |
| 5 (5) | 3 | 25 | 65.0 | s0 65.1 [63.1, 67.2]; s1 67.6 [65.7, 69.5]; s2 62.2 [60.2, 64.2] | nhanes 59.8, csxa 11.9 |
| 10 (10) | 3 | 50 | 70.3 | s0 70.8 [68.8, 72.7]; s1 73.0 [71.1, 74.9]; s2 67.2 [65.3, 69.0] | nhanes 47.5, csxa 1.0 |
| 25 (25) | 3 | 125 | 76.7 | s0 77.0 [75.1, 78.8]; s1 75.6 [73.6, 77.6]; s2 77.4 [75.5, 79.3] | nhanes 54.5, csxa 3.3 |
| 50 (50) | 1 | 250 | 81.2 | s0 81.2 [79.3, 83.0] | nhanes 59.4, csxa 5.6 |
| 100 (100) | 1 | 500 | 82.7 | s0 82.7 [80.8, 84.5] | nhanes 53.2, csxa 2.7 |
| 200 (200) | 1 | 1000 | 85.1 | s0 85.1 [83.3, 86.8] | nhanes 55.0, csxa 4.9 |
| all (2967) | 1 | 14844 | 96.9 | s0 96.9 [96.0, 97.8] | nhanes 56.5, csxa 1.4 |

## csxa

| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |
|---:|---:|---:|---:|---|---|
| 0 (0) | 3 | 0 | 3.2 | s0 5.3 [4.4, 6.2]; s1 2.5 [1.9, 3.1]; s2 1.8 [1.3, 2.4] | nhanes 29.6, buu_full 9.2 |
| 5 (5) | 3 | 25 | 94.2 | s0 93.9 [92.9, 94.7]; s1 94.3 [93.0, 95.4]; s2 94.5 [93.4, 95.4] | nhanes 38.2, buu_full 8.6 |
| 10 (10) | 3 | 50 | 93.0 | s0 93.6 [92.5, 94.6]; s1 90.7 [89.2, 92.2]; s2 94.7 [93.7, 95.7] | nhanes 37.3, buu_full 12.6 |
| 25 (25) | 3 | 125 | 96.4 | s0 97.2 [96.5, 97.9]; s1 96.3 [95.4, 97.2]; s2 95.6 [94.5, 96.6] | nhanes 39.7, buu_full 7.0 |
| 50 (50) | 1 | 250 | 97.3 | s0 97.3 [96.5, 98.0] | nhanes 38.9, buu_full 11.6 |
| 100 (100) | 1 | 500 | 97.3 | s0 97.3 [96.6, 98.0] | nhanes 38.0, buu_full 11.0 |
| 200 (200) | 1 | 1000 | 98.0 | s0 98.0 [97.3, 98.6] | nhanes 34.9, buu_full 6.5 |
| all (4114) | 1 | 20570 | 99.8 | s0 99.8 [99.6, 99.9] | nhanes 43.7, buu_full 7.3 |

Encoder (render only): val exact 0.6640106241699867, n_train 47976, init None

Cells not scored: 0

