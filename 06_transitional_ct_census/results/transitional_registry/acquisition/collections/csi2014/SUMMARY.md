# csi2014 -- two-labeller transitional screen

Labeller A: SPINEPS+VERIDAH, names from the ctd POI json (tools/spineps_ids guard). Labeller B: TotalSegmentator vertebrae_body disc intervals + rib-head levels (geometric count; TS names unused). Pseudo-truth: no radiologist read exists for these CTs.

| denominator | n |
|---|---:|
| catalogue units verified by the fetch | 20 |
| CTs converted and usable (<= 3 mm) | 20 |
| CTs through the FOV gate (SPINEPS run) | 20 |
| CTs called | 20 |
| CTs with a lumbosacral count from at least one labeller | 19 |
| CTs with a count from T1 from at least one labeller | 18 |

| subtype | tier | n |
|---|---|---:|
| ordinary | single-labeller | 14 |
| ordinary | two-labeller | 3 |
| unassigned | single-labeller | 2 |
| no_count | - | 1 |

Refusals at convert: {}

| no-count reason (B first, then A) | n |
|---|---:|
| LS: no sacrum with the lumbosacral disc just above it in the field / guard refused: /rs/rs_grp_oschome/go#/data/anomaly_harvest/csi#/spineps | 1 |

Review queue: 0 cases with renders under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/csi2014/review.
