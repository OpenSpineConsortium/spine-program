# CTSpinoPelvic1K — Test-set ensemble eval (Dataset803, merged)

**Test cases evaluated:** 174
**Overall mean foreground Dice:** 0.956

## Headline metrics

| Metric | Value | n |
|---|---|---|
| Junction-DSC (overall) | 0.924 | 52 |
| Junction-DSC Normal | 0.922 | 50 |
| Junction-DSC Lumbarization | **0.950** | 1 |
| **∆ Junction-DSC vs TS=0.357 (lumb)** | **+59.3 pts** | — |
| last_lumbar Dice on lumb | 0.678 | 3 |
| L4 Dice on sacr_count | 0.032 | 1 |
| last_lumbar specificity on sacr_count | 0.739 | — |
| Sacrum overall (vs TS=0.817) | 0.970 | 113 |
| **∆ Sacrum vs TS** | **+15.3 pts** | — |
| Normal mean fg Dice | 0.966 | 167 |
| Any-LSTV mean fg Dice | 0.712 | 7 |
| **Any-LSTV − Normal (fg Dice)** | **-0.254** | — |

## Hip class — per-side vs merged

| Metric | Value | n |
|---|---|---|
| left_hip Dice  | 0.957 | 113 |
| right_hip Dice | 0.944 | 113 |
| **hip_merged Dice (L+R as one class)** | **0.988** | 113 |

## Per-subtype Dice (mean ± SD)

| Subtype | n | L4 | last_lumbar | sacrum | hip_merged | junction_dsc | LL emit | mean fg |
|---|---|---|---|---|---|---|---|---|
| Normal | 167 | 0.971 ± 0.081 | 0.977 ± 0.028 | 0.972 ± 0.028 | 0.988 ± 0.013 | 0.922 ± 0.061 | 167/167 | 0.966 |
| Lumbarization | 3 | 0.225 ± 0.389 | 0.678 ± 0.041 | 0.947 ± 0.000 | 0.960 ± 0.000 | 0.950 ± 0.000 | 3/3 | 0.625 |
| Sacralization (count) | 1 | 0.032 ± 0.000 | — | — | — | — | 1/1 | 0.744 |
| Semisacralization | 0 | — | — | — | — | — | 0/0 | — |
| Sacralization (morph) | 2 | 0.006 ± 0.000 | 0.623 ± 0.000 | 0.921 ± 0.008 | 0.990 ± 0.013 | 0.961 ± 0.000 | 2/2 | 0.705 |
| Ambiguous | 1 | — | — | 0.860 ± 0.000 | 1.000 ± 0.000 | — | 1/1 | 0.953 |

## Voxel confusion blocks (paper Table 5)

### Block 1: GT==last_lumbar voxels on lumb cases (good signal)
n_cases = 3
| pred class | voxels | percent |
|---|---|---|
| background | 928 | 0.1% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 375407 | 46.3% |
| last_lumbar | 434499 | 53.5% |
| sacrum | 787 | 0.1% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

### Block 2: GT==L4 voxels on sacr_count cases (failure-mode signal)
n_cases = 1
| pred class | voxels | percent |
|---|---|---|
| background | 1114 | 0.8% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 2553 | 1.8% |
| last_lumbar | 140302 | 97.4% |
| sacrum | 30 | 0.0% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

### Block 3: pred==last_lumbar voxels on sacr_count cases (inverse)
n_cases = 1
| GT class | voxels | percent |
|---|---|---|
| background | 0 | 0.0% |
| L1 | 0 | 0.0% |
| L2 | 0 | 0.0% |
| L3 | 0 | 0.0% |
| L4 | 140302 | 100.0% |
| last_lumbar | 0 | 0.0% |
| sacrum | 0 | 0.0% |
| left_hip | 0 | 0.0% |
| right_hip | 0 | 0.0% |

**last_lumbar specificity on sacr_count** = 0.7389  (n_cases = 1)

Full per-class breakdown in `subgroup_summary.csv`; per-case dices in `per_case_dice.csv`; raw voxel-counts in `confusion_blocks.json`.
