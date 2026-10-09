# validation_ts -- two-labeller transitional screen

Labeller A: SPINEPS+VERIDAH, names from the ctd POI json (tools/spineps_ids guard). Labeller B: TotalSegmentator vertebrae_body disc intervals + rib-head levels (geometric count; TS names unused). Pseudo-truth: no radiologist read exists for these CTs.

| denominator | n |
|---|---:|
| catalogue units verified by the fetch | ? |
| CTs converted and usable (<= 3 mm) | 70 |
| CTs through the FOV gate (SPINEPS run) | 69 |
| CTs called | 70 |
| CTs with a lumbosacral count from at least one labeller | 61 |
| CTs with a count from T1 from at least one labeller | 36 |

| subtype | tier | n |
|---|---|---:|
| ordinary | two-labeller | 23 |
| review | review | 14 |
| L6 | two-labeller | 10 |
| ordinary | single-labeller | 8 |
| T13 | single-labeller | 7 |
| no_count | - | 6 |
| L6 | single-labeller | 2 |

Refusals at convert: {}

| no-count reason (B first, then A) | n |
|---|---:|
| LS: no sacrum with the lumbosacral disc just above it in the field / guard refused: /rs/rs_grp_oschome/go#/data/anomaly_harvest/validation_t | 2 |
| LS: the lowest rib-bearing level has only short ribs ([#.#] mm): hypoplastic #th rib or lumbar rib, the reference is ambiguous / SPINEPS not | 1 |
| LS: no rib-bearing level with a disc below it (no thoracolumbar reference) / not run: FOV: no sacrum+rib region and no rib cage -- no count  | 1 |
| LS: no sacrum with the lumbosacral disc just above it in the field / SPINEPS not run or failed (see gate.csv / timing) | 1 |
| LS: a rib cut by the field edge sits at or below the lowest whole rib-bearing level / LS: no thoracic name above L# in the field | 1 |

Review queue: 14 cases with renders under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/validation_ts/review.
