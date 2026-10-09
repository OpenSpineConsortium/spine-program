# nlst_pilot -- two-labeller transitional screen

Labeller A: SPINEPS+VERIDAH, names from the ctd POI json (tools/spineps_ids guard). Labeller B: TotalSegmentator vertebrae_body disc intervals + rib-head levels (geometric count; TS names unused). Pseudo-truth: no radiologist read exists for these CTs.

| denominator | n |
|---|---:|
| catalogue units verified by the fetch | 500 |
| CTs converted and usable (<= 3 mm) | 500 |
| CTs through the FOV gate (SPINEPS run) | 498 |
| CTs called | 500 |
| CTs with a lumbosacral count from at least one labeller | 0 |
| CTs with a count from T1 from at least one labeller | 338 |

| subtype | tier | n |
|---|---|---:|
| no_count | - | 495 |
| T13 | single-labeller | 5 |

Refusals at convert: {}

| no-count reason (B first, then A) | n |
|---|---:|
| LS: a rib cut by the field edge sits at or below the lowest whole rib-bearing level / LS: no sacrum in the field | 308 |
| LS: no sacrum with the lumbosacral disc just above it in the field / LS: no sacrum in the field | 137 |
| LS: a rib cut by the field edge sits at or below the lowest whole rib-bearing level / LS: no thoracic name above L# in the field | 33 |
| LS: a rib cut by the field edge sits at or below the lowest whole rib-bearing level / SPINEPS not run or failed (see gate.csv / timing) | 6 |
| LS: a rib cut by the field edge sits at or below the lowest whole rib-bearing level / guard refused: /rs/rs_grp_oschome/go#/data/anomaly_har | 5 |
| LS: no sacrum with the lumbosacral disc just above it in the field / SPINEPS not run or failed (see gate.csv / timing) | 3 |
| LS: no sacrum with the lumbosacral disc just above it in the field / not run: FOV: no sacrum+rib region and no rib cage -- no count possible | 2 |
| LS: no sacrum with the lumbosacral disc just above it in the field / guard refused: /rs/rs_grp_oschome/go#/data/anomaly_harvest/nlst_pilot/s | 1 |

Review queue: 0 cases with renders under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/nlst_pilot/review.
