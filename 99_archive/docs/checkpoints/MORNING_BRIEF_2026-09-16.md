# Morning brief — 2026-09-16

## What changed overnight

- **Resolution is not the lever for naming.** 1,467 paired panels / 6,652 vertebrae, 36 px → 88 px: **−0.33 pp** (CI95 −0.88, +0.22). A new decimation ladder (696 panels / 3,195 vertebrae) proves the harness *can* see resolution — 19.15% at 37 px, 11.86% at 10 px, 5.51% at 5.5 px — so the null is real and the knee is below ~20 px, under everything the refetch touched.
- **It is the lever for finding.** Same detector, 397 paired panels: panels where it returned nothing fell **60 → 39** (28 vs 7, McNemar z 3.38).
- **The X-ray gate buys less than it looks.** Matched draw 0.1972 → 0.2884 raw, → **0.2352** with the level mix fixed; composition supplies **58.3%** [50.2, 68.5] of the gain. Corrected from "about two-thirds", which the interval excludes.
- **TTA + a within-film monotone decode, same weights: 95.09% → 98.80% (n=7,339).** On the 4,196 annotated, test-eligible crops: **98.67% → 99.71%**, 47 fixed / 3 broken. The 3.7-point headline is largely BUU.
- **33 of 618 lumbar films (5.3%)** name every lumbar body one anatomical step off, one end pinned — 112 of 316 wrong lumbar crops. Ids in `shifted_films.txt`.
- **Seed is not the uncertainty; the backend is.** 10 seeds, 8,422 targets: sd 0.04–0.07 pp. The same 504 doubly-computed cells, V100 vs CPU: mean 0.48 pp, max 4.40.

## The resolution question, answered

Real films are natively several times larger than the literature panels:

| source | native vertebra height | magnified to reach 96 px |
|---|---|---|
| NHANES | 198–212 px | 0% |
| BUU | 176 px | 0% |
| CSXA | 162 px | 0% |
| literature panels | median 49 px | 81% (48% >2×) |

Corrected: the audit's "85 / 58 px" were medians of panel medians; true per-vertebra medians are **64 px** (2,943 refetched panels) and **45 px** (8,528 not). 34,700 of 56,852 vertebrae (61.0%) remain below 60 px. Hi-res originals were obtainable; paired on identical panels and boxes they bought:

| contrast | Δ exact agreement |
|---|---|
| 36 vs 88 px, model 1 | −0.33 pp (CI −0.88, +0.22) |
| model 2 | −0.03 pp |
| caption-only labels (903 panels) | −0.53 pp |
| all three, montage-free 1,294 panels | −0.25 / −0.38 / −0.60 |
| full res vs the real pre-refetch JPEG | +0.39; +0.86 (CI to +1.49) |

Headroom is smaller than reported: **video_panels is a median 3.13× in pixels (1.77× linear), not 6.25×** — six of twenty probe rows divided by a crop-window height, not a frame height — and its "20/20 resolved" was a format listing, not an image match. PDF routes are at the ceiling (s2 1/15 at 1.56×; oa 1/15 at 0.72×, web copy smaller than the PDF raster); 268 commons/reddit/archives/openverse panels already hold the original. The cross-sectional rise from 14.8% (<30 px) to 26.1% (70–96 px) is a property of which panels have big vertebrae; magnifying the same vertebra reproduces none of it.

## The corpus after filtering

| set | panels | vertebrae | agreement |
|---|---|---|---|
| all | 4,740 | 22,684 | 0.2010 |
| kept | 2,607 (55.0%) | 8,711 (38.4%) | 0.2827 [0.2692–0.2993] |
| rejected | 2,133 | 13,973 | 0.1494 |
| kept, level-standardised | — | — | **0.2352** |

Standardised gain **+0.0341 [0.0260, 0.0422]**, P(gain≤0)=0.0000; second model +0.0331. Rejections: resolution 1,509, pixel modality 575, montage 479, blind-read modality 100, non-monotonic 52, label/box 30; agreement on what each cut: 0.158 / 0.127 / 0.115 / 0.127 / 0.095.

Floor sweep, **corrected** — the track's table came from the superseded pre-pixel-model gate:

| floor | panels kept | vertebrae | agreement |
|---|---|---|---|
| 0 px | 4,740 | 22,684 | 0.2457 |
| 24 px | 3,437 (72.5%) | 13,132 | — |
| 48 px (primary) | 2,607 (55.0%) | 8,711 | 0.2827 |
| 80 px | — | — | 0.3017 |
| 96 px | 1,154 (24.3%) | 3,235 | 0.2947 |
| 160 px | — | — | 0.2762 |

Above ~80 px the floor selects zoomed fluoroscopy with one or two vertebrae and no counting context. Thoracic is where the 19.7% lives: 0.0381 → 0.0605 (7,349 → 1,569 crops), only 22.5% getting any thoracic name; lumbar 0.3373 → 0.3854. All pre-completion — **3,108 of 4,740 panels (65.6%) still have no blind modality read** and the finalise job never ran.

## Real radiographs

| | L1 | L2 | L3 | L4 | L5 | T12 | C4 | C7 | all (n=7,339) |
|---|---|---|---|---|---|---|---|---|---|
| before | 91.8 | 87.1 | 82.9 | 89.8 | 97.3 | 91.2 | 98.7 | 99.1 | **95.09** |
| after | 97.1 | 97.3 | 97.3 | 97.7 | 98.4 | 98.2 | 99.6 | 99.6 | **98.80** |

Split by label type, which the track did not do:

| surface | n | before → after |
|---|---|---|
| annotated, test-eligible (CSXA+NHANES, 824 films) | 4,196 | 98.67 → 99.71 |
| buu_full (levels counted down the film, `test_eligible: false`) | 2,698 | 90.29 → 97.85 |
| annotated L3 only | 42 | 83.3 → 97.6 |

Quote L3 82.9 → 97.3 as BUU-LSPINE. The decoder's input is deployable, not a label: sorting by centroid row reproduces true order in 1,441 of 1,443 films.

| hypothesis for the mid-lumbar floor | evidence | verdict |
|---|---|---|
| native resolution | error by height quartile 89.2 / 88.1 / 90.9 / 90.9% over 84–311 px (n=3,098); at L3 wrong crops are *larger*, 176 vs 171 px | refuted |
| BUU counting labels noisier than NHANES | L2 .870/.875, L3 .832/.812, L4 .898/.900 | refuted; n=80, no power |
| annotation geometry | height CV .1023 vs .0983 p=0.19; ratio p=0.082; age p=0.97 | refuted |
| ensembling existing arms | 11 of 11 below r18_ce alone (best 94.95%) | refuted |
| "no whole-film shifts" (our own) | units bug: T13/L6 sit between levels, so one step is two positions | self-refuted → 33 films |

## The run-level head

| bank, 10 seeds | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| allspine_v2 (16,392) | 83.42 ± 0.09 | 86.23 ± 0.26 | 86.13 ± 0.16 | 88.70 ± 0.19 |
| films_all2 (8,422) | 98.81 ± 0.05 | 99.23 ± 0.07 | 99.33 ± 0.06 | 99.36 ± 0.04 |

The published 98.69 / 99.13 / 99.41 / **99.48** sits inside the band at k=1–3 and **above the 10-seed maximum (99.4182) at k=4**, ~2.8 sd out; three of four earlier runs also exceed it and `recurrent.json` has no `_meta`. Retire the seed caveat at k=1–3; **at k=4 it stands, and the discrepancy is systematic, not seed noise.** The band axis is not real: films_all2 holds no film over 7 vertebrae, the arm labelled "9" has mean band 5.07 with 0.0% of targets at 9, and k=3 and k=4 train on the identical 8,200 windows.

| length behaviour (allspine_v2) | result |
|---|---|
| train band 3 → test 9 | 88.31 ± 0.31 vs 88.64 ± 0.13; −0.33 pp is inside its own interval (3 seeds) |
| train band 9 → test 3 | −3.21 pp pooled (CPU 3.37 / GPU 3.06); 3 vertebrae is the intra-operative case |
| one band-5 head at band 7 vs retraining at k=3 | +1.8 to +2.1 pp; the reported 2.03 was a cross-device subtraction |

L5 falls to 68.81 ± 1.80 at k=3 (n=1,534) while the aggregate barely moves; 89.5% of those errors are L5 called L4. The anchor-loss reading is refuted by the evaluator's own code — the band is centred and clipped, so it only grows with k, and L1 is inside the L5 band on 0.0 / 0.0 / 0.2 / 99.8% of the 540 BUU films at k=1–4. The cause is training-side and unexplained. No real film in either bank exceeds 7 vertebrae, so the long-band half is about DRRs only; T13 0.00% at every k and seed (n=14), L6 45.3–53.1% (n=132), both 0% real.

## Ready for the students this morning

Open `~/FluoroCap/student_pack/`: `sheets/student_NN/` and `verdicts/student_NN_*.csv`, with `docs/STUDENT_FLUORO_CORRECTION_GUIDE.md`.

| | |
|---|---|
| panels | 372 (371 rendered; FLUO-007107 has rows, no image) |
| readings | 428, of which 56 double-read, never by the same student |
| vertebra rows | 3,027 |
| per student | three get 24 panels / 182–184 rows; ten get 36 / 241–251 |
| time | ~1 h each at an assumed 30–60 panels/h — **nobody has been timed** |

The priority queues (region_disagree 53, extrapolated 49, transitional 49, run_shape 49) settle what resolution no longer competes for: whether the 34.5% region-level label/network disagreement is label error or model error. The transitional queue settles whether the labels' 146 T13-or-L6 panels against the network's 35 are anatomy or decoder noise — 18 claim both and only 2 are the full 27-class run, so it is not the decoder reciting its vocabulary. Three cautions: the 179-panel bench is equal-allocation stratified, not uniform (no-caption over-weighted 7.7×), so report per stratum, not the pooled rate `student_correction_score.py` prints; 65 of the 179 sit outside the audited pool; the priority head still runs a median 6 vertebrae per panel against the pool's 4.

## Still unknown

| question | state |
|---|---|
| NN resize on the hires arm vs the anti-aliased control | untested; ladder bounds it as small |
| are the +6.4% detector boxes correct | no precision measured; per-panel sign test null (94 vs 84). Only 28-vs-7 is clean |
| the gate under a complete blind read | 65.6% unread; the pixel model's behavioural validation is circular with the gate's metric. Its contact sheet (16/16 not radiographs) is not |
| is the decode's BUU gain circular | BUU names came from position, the decode forces names increasing with position. Against: +9.05 pts on 210 annotated NHANES lumbar crops, strict-consecutive worse (97.75%). Unsettled |
| the 33 shifted films: anatomy or bias | prevalence matches the published 4–8%; no power (mean P(L6) 0.0003 vs 0.0001). Send to `docs/lstv_reread_queue.csv` |
| 11.3% of the real-film denominator is not held out | 830 of 7,339 val crops sit in an NHANES film whose second ingest is in train. Removing them raises both numbers (95.61 → 99.03), so it did not manufacture the gain — but it contaminates the published 95.09% too |
| why L5 collapses at training band ≥7 | unexplained |
| what produced the published k=4 99.4776 | no `_meta`, no git history for that path |
| are the banks patient-grouped | zero case-id overlap; no patient key exists |
| "population beats window length" (9–12 pp) | confounded: long_train 100% DRR vs short_train 62% real, both scored on DRR val; 15,748 vs 4,734 windows |
| jobs | 40295416 / 40295545 dead, exit 127 on a Windows python path (`hires_detect_det600.json` never appears); 40295431 never ran; 40294972 still running, nothing taken from it |
| never re-read by a verifier | the 12/12 blind-read, 11/12 montage, 11/12 non-monotonic contact sheets; the DP-vs-brute-force check; the 33 shifted films against an anatomy read |
