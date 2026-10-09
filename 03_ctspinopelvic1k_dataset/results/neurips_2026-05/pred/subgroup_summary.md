# CTSpinoPelvic1K — Test-set ensemble eval (Dataset803, merged)

**Test cases evaluated:** 104
**Overall mean foreground Dice:** 0.948

## Headline metrics

| Metric | Value | n |
|---|---|---|
| last_lumbar Dice on lumb cases | 0.667 | 2 |
| Normal mean fg Dice | 0.957 | 99 |
| Any-LSTV mean fg Dice | 0.765 | 5 |
| **Any-LSTV − Normal (fg Dice)** | **-0.192** | — |

## Hip class — per-side vs merged

Asymmetric per-side Dice with high right-hip variance is consistent with L/R label noise in CTPelvic1K source annotations. The merged hip class collapses labels 7 + 8 into a single 'hip' class on both prediction and GT, characterizing hip segmentation quality independent of laterality assignment.

| Metric | Value | n |
|---|---|---|
| left_hip Dice  | 0.921 | 70 |
| right_hip Dice | 0.910 | 70 |
| **hip_merged Dice (L+R as one class)** | **0.986** | 70 |

## Per-subtype Dice (mean ± SD)

| Subtype | n | L4 | last_lumbar | sacrum | left_hip | right_hip | hip_merged | mean fg |
|---|---|---|---|---|---|---|---|---|
| Normal | 99 | 0.974 ± 0.028 | 0.974 ± 0.028 | 0.972 ± 0.028 | 0.918 ± 0.154 | 0.906 ± 0.173 | 0.987 ± 0.014 | 0.957 |
| Lumbarization | 2 | 0.267 ± 0.376 | 0.667 ± 0.033 | 0.943 ± 0.000 | 0.960 ± 0.000 | 0.961 ± 0.000 | 0.961 ± 0.000 | 0.729 |
| Sacralization (count) | 0 | — | — | — | — | — | — | — |
| Semisacralization | 0 | — | — | — | — | — | — | — |
| Sacralization (morph) | 2 | 0.059 ± 0.000 | 0.559 ± 0.000 | 0.934 ± 0.053 | 0.973 ± 0.003 | 0.978 ± 0.006 | 0.987 ± 0.015 | 0.703 |
| Ambiguous | 1 | — | — | 0.882 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.960 |

Full per-class breakdown in `subgroup_summary.csv`; per-case dices in `per_case_dice.csv`.
