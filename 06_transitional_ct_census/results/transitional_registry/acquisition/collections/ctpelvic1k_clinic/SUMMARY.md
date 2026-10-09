# ctpelvic1k_clinic -- two-labeller transitional screen

Labeller A: SPINEPS+VERIDAH, names from the ctd POI json (tools/spineps_ids guard). Labeller B: TotalSegmentator vertebrae_body disc intervals + rib-head levels (geometric count; TS names unused). Pseudo-truth: no radiologist read exists for these CTs.

| denominator | n |
|---|---:|
| catalogue units verified by the fetch | 2 |
| CTs converted and usable (<= 3 mm) | 172 |
| CTs through the FOV gate (SPINEPS run) | 6 |
| CTs called | 172 |
| CTs with a lumbosacral count from at least one labeller | 1 |
| CTs with a count from T1 from at least one labeller | 0 |

| subtype | tier | n |
|---|---|---:|
| no_count | - | 171 |
| unassigned | single-labeller | 1 |

Refusals at convert: {"same voxels as ctpelvic_dataset#_CLINIC_metal_#": 3, "same voxels as ctpelvic_dataset#_CLINIC_#": 3}

| no-count reason (B first, then A) | n |
|---|---:|
| LS: no rib-bearing level with a disc below it (no thoracolumbar reference) / not run: FOV: no sacrum+rib region and no rib cage -- no count  | 157 |
| fewer than two intervertebral discs on the column / not run: fewer than two intervertebral discs on the column | 5 |
| LS: no rib-bearing level with a disc below it (no thoracolumbar reference) / LS: no thoracic name above L# in the field | 4 |
| fewer than three body/disc objects in the field / not run: fewer than three body/disc objects in the field | 3 |
| no TotalSegmentator vertebrae_body output / not run: no TotalSegmentator vertebrae_body output | 1 |
| LS: no sacrum with the lumbosacral disc just above it in the field / guard refused: /rs/rs_grp_oschome/go#/data/anomaly_harvest/ctpelvic#k_c | 1 |

Review queue: 0 cases with renders under /rs/rs_grp_oschome/go2432/data/anomaly_harvest/ctpelvic1k_clinic/review.
