# CTSpinoPelvic1K — 5-fold cross-fold + ensemble eval

Per-fold per-class means aggregated across 5 folds; reported as mean ± std (1σ across folds).

## Headline metrics

| Metric | 5-fold mean ± std | Ensemble | n folds |
|---|---|---|---|
| mean_fg_dice_overall | 0.952 ± 0.003 | 0.956 | 5 |
| hip_merged_dice_overall | 0.988 ± 0.001 | 0.988 | 5 |
| left_hip_dice_overall | 0.952 ± 0.005 | 0.957 | 5 |
| right_hip_dice_overall | 0.938 ± 0.012 | 0.944 | 5 |
| sacrum_dice_overall | 0.969 ± 0.002 | 0.970 | 5 |
| sacrum_minus_TS_overall_pts | 15.190 ± 0.159 | 15.279 | 5 |
| junction_dsc_overall | 0.908 ± 0.016 | 0.924 | 5 |
| junction_dsc_normal | 0.907 ± 0.016 | 0.922 | 5 |
| junction_dsc_lumb | 0.946 ± 0.007 | 0.950 | 5 |
| junction_dsc_lumb_minus_TS_pts | 58.917 ± 0.745 | 59.294 | 5 |
| last_lumbar_dice_on_lumb | 0.698 ± 0.038 | 0.678 | 5 |
| L4_dice_on_sacr_count | 0.187 ± 0.337 | 0.032 | 5 |
| last_lumbar_specificity_on_sacr_count | 0.778 ± 0.074 | 0.739 | 5 |
| normal_mean_fg_dice | 0.963 ± 0.002 | 0.966 | 5 |
| any_lstv_mean_fg_dice | 0.705 ± 0.028 | 0.712 | 5 |
| any_lstv_minus_normal_fg_dice | -0.258 ± 0.027 | -0.254 | 5 |

## Per-subtype — 5-fold cross-fold mean ± std

| Subtype | n_cases (per fold) | L4 | last_lumbar | sacrum | hip_merged | junction_dsc | LL emit (sum) | mean fg |
|---|---|---|---|---|---|---|---|
| Normal | 167/167/167/167/167 | 0.967 ± 0.005 | 0.971 ± 0.005 | 0.971 ± 0.002 | 0.988 ± 0.001 | 0.907 ± 0.016 | 835/835 | 0.963 ± 0.002 |
| Lumbarization | 3/3/3/3/3 | 0.213 ± 0.114 | 0.698 ± 0.038 | 0.946 ± 0.004 | 0.960 ± 0.002 | 0.946 ± 0.007 | 15/15 | 0.620 ± 0.073 |
| Sacralization (count) | 1/1/1/1/1 | 0.187 ± 0.337 | — | — | — | — | 5/5 | 0.717 ± 0.162 |
| Semisacralization | 0/0/0/0/0 | — | — | — | — | — | 0/0 | — |
| Sacralization (morph) | 2/2/2/2/2 | 0.062 ± 0.083 | 0.583 ± 0.136 | 0.910 ± 0.039 | 0.989 ± 0.000 | 0.927 ± 0.068 | 10/10 | 0.702 ± 0.012 |
| Ambiguous | 1/1/1/1/1 | — | — | 0.862 ± 0.012 | 1.000 ± 0.000 | — | 5/5 | 0.954 ± 0.004 |

## Voxel confusion blocks (summed voxel counts across folds)

### Block 1 — GT==last_lumbar voxels on lumb cases
n_cases (sum across folds) = 15; voxel total = 4058105
| pred class | voxels | percent |
|---|---|---|
| background | 48291 | 1.2% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 1628982 | 40.1% |
| last_lumbar | 2363027 | 58.2% |
| sacrum | 17805 | 0.4% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

### Block 2 — GT==L4 voxels on sacr_count cases
n_cases (sum across folds) = 5; voxel total = 719995
| pred class | voxels | percent |
|---|---|---|
| background | 15627 | 2.2% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 107240 | 14.9% |
| last_lumbar | 595291 | 82.7% |
| sacrum | 1837 | 0.3% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

### Block 3 — pred==last_lumbar voxels on sacr_count cases
n_cases (sum across folds) = 5; voxel total = 595291
| GT class | voxels | percent |
|---|---|---|
| background | 0 | 0.0% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 595291 | 100.0% |
| last_lumbar | 0 | 0.0% |
| sacrum | 0 | 0.0% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

**last_lumbar specificity on sacr_count (across folds)** = 0.7784  (n_cases = 5)

Per-fold raw values in `cross_fold_summary.csv` (column `<class>_nfolds` shows how many folds contributed); per-fold confusion sums in `cross_fold_confusion.json`.
