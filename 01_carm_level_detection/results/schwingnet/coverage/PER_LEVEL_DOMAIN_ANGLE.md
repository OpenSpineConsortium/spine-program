# How the namer does at each level, in each domain, at each angle, and whether renders help

Greg, 2026-09-27: "How does it do at each level, in each domain and angle in fluoro, plain film, various
ratios of synthetic CT / real film, does it ever help. Figure a way to get to Dr to look at. Manifest."

This file is the manifest for that question: every number below names the result file and JSON pointer
it was read from, and says whether the number is held out, selection-split, or derived here. Nothing in it
is a new measurement except the rows marked DERIVED, which are read-only aggregations of committed rows.
Where a measurement does not exist, that is stated rather than filled.

## The answer in six sentences

1. **Per level, real C-arm (Surgio-B51, case-grouped CV):** L1–L5 all name at 96.8–98.5 % on whole lateral
   frames and 95.5–97.7 % on whole AP frames; the one-body field is where levels separate (L1 41 % LAT / 9.5 %
   AP; L4–L5 84–86 %). Zero-shot AP is a systematic one-level cranial shift (L4→L3 ×51, L3→L2 ×51 …).
2. **Per level, plain film:** measured nowhere in the manuscript. DERIVED from `results/a5_rows.csv`
   (v8 encoder, selection split): every lumbar level 96.4–98.4 % on BUU, 97.4–100 % on NHANES, cervical
   99.7–100 % on CSXA. On renders the floor is mid-thoracic (T7 55–59 %) and the rare classes
   (L6 20–42 %, T13 0/9 across sources).
3. **Per domain:** plain film 97.3–99.8 % (selection split) / 92.7–99.8 % held-out persons at every person;
   renders 45–94 % by source; real fluoroscopy zero-shot LAT 96.4 % vs AP 43.7 %, fine-tuned 97.4 / 96.4 %,
   day-grouped 92.1 / 94.8 %. VinDr, FluoroCap, DeepFluoro, COBRA, Geneva, Ljubljana: not scored for naming
   (no level truth or excluded).
4. **Per angle:** naming per angle does not exist anywhere. Detection per angle exists on three surfaces
   (one real 301-frame spin, a 40-subject render arc, COBRA gantry bands).
5. **Synthetic : real ratio:** never swept. `merge_banks.py` fixes `real_share = 0.5`, so every film N-curve
   cell is ~1 : 1 by rows (Table A). What was swept is N persons at fixed ratio.
6. **Do renders ever help?** Yes, when film is scarce: +6 to +22 points at 5–25 persons per corpus, every
   seed separated in all six scarce cells. From 100 persons the arms are not separated; with every person,
   level (NHANES +0.7, CSXA −0.2) or worse (BUU −1.6, separated). Of the nine pre-stated verdict cells, seven
   separated: six for, one against. For C-arm naming renders never substitute for in-domain persons.
   For detection they hurt on the C-arm (63.1 vs 80.5 at 0.74) and help on the kV imager (32.7 vs 18.5 at 0.25).

## Table A. The synthetic : real ratio that was actually trained (film N-curve, render-only arm)

Source: `results/coverage/film_ncurve/film_ncurve.json#cells/<cell>/encoder_ft/n_train` and `n_train_crops`;
render rows = render-only n_train − film-only n_train = 15,374 in every cell. Rule: `tools/merge_banks.py`
line 60, `k = round(real_share/(1−real_share) × 15,374 / n_crops)`, `real_share` 0.5.

| corpus | N persons | distinct film crops (seed 0) | repeat k | film rows | merged train rows | render : film ROWS | render : film DISTINCT images |
|---|---:|---:|---:|---:|---:|---|---|
| NHANES | 0 | 0 | – | 0 | 15,374 | renders only | – |
| NHANES | 5 | 48 (s1 50, s2 38) | 320 | 15,360 | 30,734 | 1.00 : 1 | 320 : 1 |
| NHANES | 10 | 103 | 149 | 15,347 | 30,721 | 1.00 : 1 | 149 : 1 |
| NHANES | 25 | 229 | 67 | 15,343 | 30,717 | 1.00 : 1 | 67 : 1 |
| NHANES | 50 | 467 | 33 | 15,411 | 30,785 | 1.00 : 1 | 33 : 1 |
| NHANES | 100 | 891 | 17 | 15,147 | 30,521 | 1.01 : 1 | 17 : 1 |
| NHANES | 200 | 1,774 | 9 | 15,966 | 31,340 | 0.96 : 1 | 8.7 : 1 |
| NHANES | all (264) | 2,357 | 7 | 16,499 | 31,873 | 0.93 : 1 | 6.5 : 1 |
| BUU | 5 | 25 | 615 | 15,375 | 30,749 | 1.00 : 1 | 615 : 1 |
| BUU | 10 | 50 | 307 | 15,350 | 30,724 | 1.00 : 1 | 307 : 1 |
| BUU | 25 | 125 | 123 | 15,375 | 30,749 | 1.00 : 1 | 123 : 1 |
| BUU | 50 | 250 | 61 | 15,250 | 30,624 | 1.01 : 1 | 61 : 1 |
| BUU | 100 | 500 | 31 | 15,500 | 30,874 | 0.99 : 1 | 31 : 1 |
| BUU | 200 | 1,000 | 15 | 15,000 | 30,374 | 1.02 : 1 | 15 : 1 |
| BUU | all (2,967) | 14,844 | 1 | 14,844 | 30,218 | 1.04 : 1 | 1.04 : 1 |
| CSXA | 5 / 10 / 25 / 50 / 100 / 200 | 25 / 50 / 125 / 250 / 500 / 1,000 | 615 / 307 / 123 / 61 / 31 / 15 | 15,375 / 15,350 / 15,375 / 15,250 / 15,500 / 15,000 | 30,749 / 30,724 / 30,749 / 30,624 / 30,874 / 30,374 | 1.00 : 1 | 615 : 1 → 15 : 1 |
| CSXA | all (4,114) | 20,570 | 1 | 20,570 | 35,944 | 0.75 : 1 | 0.75 : 1 |

The row ratio is a constant of the design, not a swept variable. The only ratio variation is incidental
(BUU all 1.04 : 1, CSXA all 0.75 : 1). The 2026-09-17 film level model (memory `remedies-refuted-2026-09-17`)
is the one place a render FRACTION was swept with real film fixed: fraction 0 → 0.5 moved anomalous-spine
accuracy 34.0 → 53.2 while ordinary fell 2 points. That model line is superseded and not quotable.

## Table B. Do renders help? Render-only minus film-only, by corpus and N (points, seed mean)

Source: `results/coverage/film_ncurve/ablation/READ.md` lines 9–16, 22–29, 35–42; `ablation_read.json`.
"sep" = every seed separated outside the patient-clustered 95 % intervals (rule pre-stated in
REVISION_LOG3 §13; verdict cells are N = 5, 25, all). Seeds: 3 at N ≤ 25, **1 above**.

| corpus | N | render-only | ImageNet init, same bank | film only | render − film | verdict |
|---|---:|---:|---:|---:|---:|---|
| NHANES | 5 | 77.8 | 75.5 | 55.9 | +21.9 | HELP (sep) |
| NHANES | 10 | 82.3 | 79.1 | 65.2 | +17.1 | HELP (sep) |
| NHANES | 25 | 87.8 | 83.0 | 75.6 | +12.2 | HELP (sep) |
| NHANES | 50 | 89.2 | 86.1 | 81.5 | +7.7 | HELP (sep) |
| NHANES | 100 | 89.6 | 86.8 | 85.7 | +3.9 | not separated |
| NHANES | 200 | 92.5 | 89.8 | 90.1 | +2.4 | not separated |
| NHANES | all 264 | 92.7 [89.5, 95.6] | 92.3 | 92.0 [88.7, 94.9] | +0.7 | not separated |
| BUU | 5 | 65.0 | 60.0 | 53.9 | +11.1 | HELP (sep) |
| BUU | 10 | 70.3 | 67.6 | 60.6 | +9.7 | HELP (sep) |
| BUU | 25 | 76.7 | 73.7 | 70.7 | +6.0 | HELP (sep) |
| BUU | 50 | 81.2 | 79.3 | 77.7 | +3.5 | not separated |
| BUU | 100 | 82.7 | 84.1 | 83.8 | −1.1 | not separated |
| BUU | 200 | 85.1 [83.3, 86.8] | 85.5 | 87.2 [85.3, 89.0] | −2.1 | not separated |
| BUU | all 2,967 | 96.9 [96.0, 97.8] | 97.2 | 98.5 [98.0, 99.0] | −1.6 | HURT (sep) |
| CSXA | 5 | 94.2 | 91.2 | 75.4 | +18.7 | HELP (sep) |
| CSXA | 10 | 93.0 | 91.7 | 80.8 | +12.2 | HELP (sep) |
| CSXA | 25 | 96.4 | 91.9 | 90.2 | +6.2 | HELP (sep) |
| CSXA | 50 | 97.3 | 95.9 | 94.4 | +2.9 | HELP (sep) |
| CSXA | 100 | 97.3 | 96.6 | 96.3 | +1.0 | not separated |
| CSXA | 200 | 98.0 | 97.5 | 97.0 | +1.0 | not separated |
| CSXA | all 4,114 | 99.8 | 99.8 | 99.9 | −0.2 | not separated |

N = 0 (renders only, no film): NHANES 27.2, BUU 10.3, CSXA 3.2 (render-only init); 29.9 / 18.1 / 2.2
(ImageNet init). The ImageNet-init-same-bank column isolates the render *pretraining* from the render *rows*:
most of the scarce-N gain is the rows, 2–5 points is the pretraining. Cross-corpus film-to-film transfer from
the same cells (FILM_NCURVE.md): NHANES-trained → CSXA peaks 74.3 % at N = 200, → BUU 73.2 % at all;
BUU-trained → CSXA ≤ 12.6 %; CSXA-trained → BUU ≤ 12.6 %, → NHANES ≤ 43.7 %.

## Table C. Per-level naming on real C-arm frames (C-ArmLSpine)

Source: `results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:cv5_det/cells/<VIEW>/<k>/per_level`
(v9 lineage, case-grouped five-fold; exact %, n in brackets). **Not printed in any table of the manuscript;
Table 3 prints view × field only.** Truth = agreement of two automatic CBCT labellers; no L6/T13 in this truth.

| level | LAT whole | AP whole | LAT 3 in field | AP 3 in field | LAT 1 in field | AP 1 in field | zero-shot LAT whole | zero-shot AP whole | day-grouped LAT whole |
|---|---|---|---|---|---|---|---|---|---|
| L1 | 97.4 (76) | 97.5 (81) | 86.8 (76) | 54.1 (74) | 41.2 (68) | 9.5 (63) | 98.7 | 53.1 | 94.7 |
| L2 | 96.8 (123) | 95.5 (133) | 91.0 (255) | 80.6 (273) | 83.1 (130) | 71.2 (125) | 96.8 | 42.9 | 91.1 |
| L3 | 97.2 (141) | 95.7 (141) | 93.4 (411) | 87.4 (411) | 63.5 (137) | 56.0 (134) | 95.7 | 41.8 | 91.5 |
| L4 | 97.2 (141) | 95.8 (142) | 95.0 (282) | 92.3 (285) | 84.1 (145) | 85.5 (145) | 95.7 | 42.3 | 91.5 |
| L5 | 98.5 (136) | 97.7 (133) | 95.6 (135) | 92.5 (133) | 86.2 (123) | 84.7 (124) | 96.3 | 42.1 | 92.7 |
| T12 | – | 100 (1) | – | – | – | – | – | 100 (1) | – |

Confusions (pre:cv5_det, LAT whole): L4→L5 ×2, L3→L4 ×2, L2→L3 ×2, L4→T3, L5→T4, L3→T2, L2→T1, L1→C7,
L4→L3, L3→L2. Zero-shot AP whole: L4→L3 ×51, L3→L2 ×51, L5→L4 ×48, L2→L1 ×46, L1→T12 ×21 — a systematic
one-level cranial shift, which fine-tuning on the device removes.

Coupled detector + classifier per level (`coupling.json#cells/det74~1kfull/per_level`, classifier / coupled):
L1 98.1 / 98.1 (157), L2 96.9 / 96.9 (256), L3 97.2 / 97.2 (282), L4 97.2 / 97.2 (283), L5 98.1 / 98.9 (269).
The three patients one automatic labeller reads as L6: classifier 0/5, coupled 1/5 (agreement with a labeller,
not correctness).

## Table D. Per-domain naming

Random windows of 2–9 vertebrae unless stated. Film/render rows: `results/a5.json` (v8 encoder + mixed head,
patient-keyed **selection** split, not held out). N-curve rows: `film_ncurve.json` (render-only encoder +
N persons, **held-out test persons**). C-arm: `cv_v9.json` (v9 lineage).

| domain | corpus | measure | value | file # pointer |
|---|---|---|---|---|
| plain film | CSXA cervical | exact, random windows | 99.83 % (3,629/3,635; 727 pts) | `a5.json#per_protocol/random/csxa/patient_clustered` |
| plain film | BUU-LSPINE lumbar | same | 97.34 % (2,671/2,744; 549) | `a5.json#…/buu_full` |
| plain film | NHANES II | same | 99.10 % (441/445; 52 pts, 76 films) | `a5.json#…/nhanes` |
| plain film | CSXA / BUU / NHANES | three bodies in view | 99.6 / 95.0 / 94.6 % | `a5.json#per_source_reproduced/maximal_band3`; supplement.tex line 117 |
| plain film, held-out persons | NHANES / BUU / CSXA, all persons | N-curve endpoint | 92.7 / 96.9 / 99.8 % | `film_ncurve.json#curves/<src>/all` |
| plain film, held-out persons | same, N = 0 (renders only) | film-free floor | 27.2 / 10.3 / 3.2 % | `film_ncurve.json#curves/<src>/0` |
| render | ctsp_drr | random | 93.9 % (1,006) | `a5.json#per_source_reproduced/random/ctsp_drr` |
| render | verse_drr | random | 83.3 % (832) | same/verse_drr |
| render | physics_drr (TotalSegmentator) | random | 76.4 % (5,856) | same/physics_drr |
| render | physics_rare (L6/T13 renders) | random | 45.1 % (1,863) | same/physics_rare |
| real fluoroscopy | C-ArmLSpine Surgio-B51, zero-shot | LAT / AP whole frame | 96.4 % (595/617) / 43.7 % (276/631) | `cv_v9.json` pre:zeroshot_v9_existing; `tables/tab3_naming.tex` 66–67 |
| real fluoroscopy | same, case-grouped CV | LAT / AP whole frame | 97.4 % (601/617) / 96.4 % (608/631) | tab3_naming.tex 69–70 |
| real fluoroscopy | same, day-grouped CV | LAT / AP whole frame | 92.1 / 94.8 % | tab3_naming.tex 75–76 |
| real fluoroscopy | same, three in field | LAT / AP | 93.1 / 85.5 % | tab3_naming.tex 71–72 |
| real fluoroscopy | same, one in field | LAT / AP | 74.8 / 67.5 % | tab3_naming.tex 73–74 |
| real fluoroscopy, count only | C-ArmLSpine test, no classifier | ordinal correct, matched bodies @0.74 | 95.4 % (188/197) | tab3_naming.tex 82; `counting.json` |
| kV imager, count only | COBRA2026 Elekta test | ordinal correct @0.25 | 71.1 % (54/76) | tab3_naming.tex 85 |
| cadaver C-arm, count only | DeepFluoro test specimen | ordinal correct @0.25 | 79.1 % (53/67), one cluster | `tab3_naming.sources.md` 54 |
| NOT SCORED for naming | VinDr-SpineXR | – | 0 films in the level bank; vindrps leaked | NUMBERS.md 12, 195 |
| NOT SCORED | FluoroCap | – | excluded source; 19.7 % "agreement" not quotable | NUMBERS.md 513 |
| NOT SCORED | DeepFluoro / COBRA / Geneva / Ljubljana / case134 spin | naming | no level truth | `case134_sweep.md` 11; tab2_detection.tex |

The a5 film numbers (99.1 / 97.3 / 99.8) and the N-curve endpoints (92.7 / 96.9 / 99.8) come from different
encoders on different splits; quote them as what they are, never side by side as one curve.

## Table E. DERIVED per-level plain-film naming (not reported anywhere; computed read-only for this file)

From `results/a5_rows.csv`, protocol = random, grouped by source × truth. v8 encoder
(`allspine_v8 model_rung_1_aug2.pt`, head `head_allspine_v8_mixed_kmax4_seed0.pt`; `a5_rows_meta.json`) on the
**selection** split. Before any of this is quoted, it must be re-run on held-out persons and written by a
committed tool.

| source | per level (correct/n, %) |
|---|---|
| NHANES II | C2 36/36 100; C3 38/38 100; C4 38/38 100; C5 36/37 97.3; C6 31/31 100; C7 22/22 100; T12 26/26 100; L1 37/38 97.4; L2 37/38 97.4; L3 38/38 100; L4 37/38 97.4; L5 38/38 100; sacrum 26/26 100 |
| BUU-LSPINE | L1 540/549 98.4; L2 530/548 96.7; L3 533/549 97.1; L4 529/549 96.4; L5 539/549 98.2 |
| CSXA | C3 726/727 99.9; C4 725/727 99.7; C5 726/727 99.9; C6 727/727 100; C7 725/727 99.7 |
| ctsp_drr | T10 94.5; T11 95.5; T12 92.0; L1 93.8; L2 92.9; L3 93.8; L4 92.0; L5 94.4; L6 1/5 20.0; sacrum 112/112 100 |
| physics_drr | C1 93.0; C5 71.6; T7 59.1 (floor); T9 62.7; T12 75.0; L1 75.8; L3 80.3; L4 83.1; L5 82.8; L6 10/35 28.6; T13 0/1 |
| physics_rare | T2 5.9; T6 34.1; T10 55.7; T12 64.1; L1 57.3; L3 44.9; L5 32.5; L6 42/153 27.5; T13 0/7 |
| verse_drr | C1–C2 100; C5 73.7; T7 55.6; T12 90.0; L1 92.9; L5 85.2; L6 5/12 41.7; T13 0/1 |

Older per-level film numbers in memory (`fluoro-panel-gap-diagnosed.md` line 15: "L3 82.9, L2 87.1, L4 89.8"
on the leaked allspine_v2 bank) are superseded and not quotable.

## Table F. Per-angle DETECTION (no per-angle naming exists)

**(1) Real:** case134's 301-frame Surgio spin (`tools/case134_sweep.py`; `results/arc/case134_sweep.md` 46–64),
poses from headers refined by edge registration, vertebral-body boxes projected from the case's own CBCT,
body recall per 10° bin of lateral angle @0.25. **One patient, no interval, no names.**

| lateral bin | n | pooled (trained on this device's spot frames) | styled-render sweep, nearest lateral |
|---|---:|---:|---:|
| [−130, −120) | 28 | 0.571 | – |
| [−110, −100) | 72 | 0.903 | – |
| [−90, −80) | 72 | 0.750 | 0.790 |
| [−70, −60) | 64 | 1.000 | 0.788 |
| [−50, −40) | 68 | 0.985 | 0.606 |
| [−30, −20) | 68 | 1.000 | 0.788 |
| [−10, 0) | 68 | 1.000 | 0.933 |
| [+20, +30) | 68 | 1.000 | 0.952 |
| [+40, +50) | 64 | 0.984 | 0.740 |
| [+50, +60) | 52 | 0.942 | 0.779 |

Whole spin: pooled 93.6 % @0.25 / 78.1 % @0.74; the reported held-out detector (real_lodo) 49.5 / 49.4 % —
"exactly half of the boxes in 15 of 19 bins", recorded as UNEXPLAINED in `figS4.record.json`; lodoA 37.2;
lodoB 29.6. Sacrum: no truth (CBCT fragment).

**(2) Rendered:** 40 unseen TotalSegmentator subjects, Surgio card, matched N, seed-mean body recall @0.25 by
lateral angle (`results/power/power.json#panel_d_angle`; Figure 5d).

| arm (N train, H*_lat) | −90 | −70 | −60 | −50 | −40 | −30 | −20 | 0 | +20 | +30 | +40 | +50 | +60 | +70 | +90 | trained bins | 16 untrained bins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| low: AP+LAT poses (2,646, 0.24) | 85 | 65 | 34 | 30 | 24 | 50 | 71 | 81 | 67 | 39 | 26 | 30 | 37 | 57 | 81 | 82.1 | 52.8 |
| low2n: same poses ×2 (5,290, 0.24) | 98 | 88 | 55 | 41 | 35 | 54 | 81 | 89 | 72 | 44 | 32 | 38 | 55 | 81 | 96 | 94.2 | 64.8 |
| high: arc poses (2,646, 0.99) | 87 | 84 | 77 | 74 | 76 | 80 | 75 | 69 | 75 | 77 | 76 | 75 | 73 | 79 | 87 | 80.7 | 77.1 |

Elekta XVI arms: zero on every bin and on the real test. Caveat: the Surgio card renders thick laterals
photon-starved, so the ±90 bins conflate geometry with underexposure. The same render-only arms on the REAL
Surgio test: 0.7–9.1 % (`EXPERIMENT.md`).

**(3) Real kV imager gantry bands,** COBRA Elekta test, vertebra / sacrum recall @0.25
(`contribution_matrix.md`): real-only lodo_cobra 0–30° 45.3 / 34.6, 30–60° 11.3 / 4.7, 60–90° 0.9 / 0.0;
renders only 67.2 / 70.7, 39.9 / 21.6, 9.9 / 0.0; design B 69.3 / 76.9, 31.1 / 26.8, 1.5 / 5.2; same-device
control 97.4 overall. DeepFluoro specimen (lodo_df): 0–30° 95.0, 30–60° 100 (9 frames). C-ArmLSpine by view
(lodo_carm, outline): AP 93.0 / LAT 88.2; renders only AP 57.3 / LAT 6.2.

## Table G. Renders help / stop helping / hurt — every measured instance

| task | setting | renders help? | numbers | file |
|---|---|---|---|---|
| film naming, ordinary levels | 5–25 persons per corpus, ~1 : 1 rows | HELP, +6 to +22 pts, 6/6 scarce cells separated | Table B | `ablation/READ.md` |
| film naming | 50 persons | NHANES / CSXA help (+7.7 / +2.9, sep); BUU not separated (+3.5) | Table B | same |
| film naming | 100–200 persons | no separated difference (−2.1 to +3.9) | Table B | same |
| film naming | every person | level (NHANES +0.7, CSXA −0.2) or HURT (BUU −1.6, sep) | Table B | same |
| film naming, N = 0 | renders only, no film | 27.2 / 10.3 / 3.2 % — near useless as a film namer | FILM_NCURVE.md 9/22/35 | `film_ncurve.json` |
| rare classes L6 / T13 | any | renders are the ONLY labelled source; they stay in regardless | READ.md 58 | – |
| C-arm naming, renders as substitute for C-arm persons | AP whole frame | never: 26.2 → 53.7 % vs in-domain 90.8 → 98.1 % | INDOMAIN.md §6 | `fit.json` |
| C-arm naming | LAT whole frame | no gain over the 93.7 % zero-shot floor (92.1–93.7 %) | INDOMAIN.md §6 | `fit.json` |
| C-arm detection, renders only | C-ArmLSpine | 0.3 % @0.74, 31.7 % @0.25 (real-only 80.5 / 90.6) | tab2_detection.tex 53 | a1 / fig3 |
| C-arm detection, renders + other devices' real (design B) vs real-only | C-ArmLSpine | HURT at 0.74: 63.1 [54.8, 71.0] vs 80.5 [74.1, 86.8]; −2.8 at 0.25 | tab2 48–49 | `lcurve.json` |
| same | COBRA Elekta | HELP: 32.7 vs 18.5 @0.25; 10.1 vs 6.2 @0.74; renders-only 37.8 beats real-only 18.5 | tab2 57–58; CM 71 | `contribution_matrix.json` |
| same | DeepFluoro specimen | none: 94.0 vs 95.2 (one cluster) | tab2 62–64 | – |
| styled renders at matched N vs 24 in-domain frames | C-ArmLSpine | in-domain +15.7 pp LAT, +27.0 pp AP | INDOMAIN.md §3 line 43 | `det_fill.json` |
| render arc coverage (matched N) | unseen render sweep | HELP off-axis: untrained bins 52.8 → 77.1 %; costs 1.4 pts on trained bins; 2× same-pose frames fill no gap | Table F(2) | `power.json` |
| render-only coverage arms | REAL device test | ~0 (0.0–9.1 %) whatever the coverage | EXPERIMENT.md 7–18 | `scores.json` |
| plain-radiograph detection | 17 NHANES lumbar films | render-trained 67.7 % vs film-trained 99.4 % @0.05 | tab2 67–68 | `a3.json` |
| 2026-09-17 film level model | pretrain on renders then fine-tune | HURT: 89.1 / 40.4 vs 91.8 / 66.0 (ordinary / anomalous) | memory remedies-refuted 14–20 | ~/model_night |
| same | renders + real mixed, 8 epochs | HURT: 88.2 / 36.2 | same | – |
| same | render FRACTION 0 → 0.5, real fixed | anomalous 34.0 → 53.2, ordinary −2 | same 27–29 | – |
| literature (119 refs) | any DRR paper | no ratio sweep exists; adjacent fields flatten at 4 : 1–10 : 1 (real 10–20 %) | memory synthetic-real-ratio-evidence | reports/ |

## What is not known, and what it would take

| gap | why it matters | what closes it |
|---|---|---|
| Per-angle naming | the manuscript's angle story is detection only | level truth on the case134 spin (VERIDAH read C1–C5 on a lumbar CBCT; needs a human read) or a second spin with a labelled CBCT |
| Per-level film naming on held-out persons | Table E is selection-split | a committed tool aggregating the N-curve test rows per level, through the manifest |
| Ratio sweep | the design fixed 1 : 1 | one array: `real_share` ∈ {0.1, 0.25, 0.5, 0.75, 0.9} at N = 25 and N = all, three seeds; ~45 cells × 15 epochs |
| Seeds above N = 25 | the "not separated" and BUU-all reversal rest on one run each | seeds 1–2 at N = 50–all (18 cells × 2 arms) |
| Rare-class accuracy on anything real | no human-read L6/T13 film or C-arm frame exists | the transitional review tree (this week's build) is the route to a human-read L6/T13 set |
| Fluoroscopy naming beyond one device | one device, one site, automatic truth | C-ArmLSpine is the only public C-arm set with level-resolvable CBCT; the cine requests drafted 2026-09-26 are the other route |

## Getting it in front of a doctor

Two forms, both read-only from committed files, neither typed by hand:

1. **Supplement table S5 "Per level"** — L1–L5 × {LAT, AP} × {whole, 3, 1} from `cv_v9.json`, written by
   a tool into `tables/tabS5_per_level.tex` through `\RESULT` keys so `--check` covers it (today 167 bare
   numerals sit in tables that `--check` never scans; this table should not add to them). The body is at
   2,998 / 3,000 words, so it is a supplement row plus one clause in Results.
2. **The one-page read for Dr Tech** — Tables C and G of this file, with the two sentences a surgeon needs:
   lateral whole-frame naming is at ceiling per level on this device; the one-body AP field at L1 is where it
   fails, and it fails toward the cranial neighbour.

Neither is done. Both wait on Greg's decision whether a per-level table belongs in this submission.
