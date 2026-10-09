# A28 body-box rescore of every quoted detector number

Date 2026-09-23. Grid job 40419569 (cancelled: grid-mismatch bug), 40419582 (complete). Files: `rescore.json` (machine rows), grid outputs under
`/rs/rs_grp_oschome/go2432/data/or_ready/bodybox_rescore/` (mirrored in `grid/` here). Intervals: 2,000-resample bootstrap clustered by case/person, percentile (BCa alongside in the scored files), seed 0.

**Conventions, beside every value.** WV = the retired whole-vertebra outline (CT/CBCT-projected release labels).
BODY = the A28 vertebral body (SPINEPS instance x semantic corpus 49/50, `tools/body_masks.py`). The sacrum keeps
the whole-sacrum box in both conventions: SPINEPS defines no corpus for the sacrum, so every sacrum number is
convention-free and unchanged.

## What was built and how it was checked

- **COBRA body truth** (/rs/rs_grp_oschome/go2432/data/or_ready/bodybox_rescore/truth/cobra_elekta): the SPINEPS `bodies_cobra` masks projected through each test frame's own
  `pose.K`/`pose.ext` with the released export's box rule. **855 of 893** WV truth vertebrae got a body box (drops: {'body_too_small': 22, 'visible_frac<0.5': 16};
  the 22 `body_too_small` are all one case's L5 -- D152, whose SPINEPS body holds 191 voxels, under the 200 floor).
  Each TS vertebra was bridged to its SPINEPS instance in world space (covers >= 0.3 of it, one-to-one greedy;
  observed coverages 0.46-0.94, median ~0.87).
- **Geometry self-check**: the released WV boxes re-projected through this code reproduce themselves at median
  IoU 0.9999, minimum 0.9796 (n=38); the build fails below 0.90/0.70.
- **Number self-check (outside the computation)**: every quoted WV number re-derived from the raw dumps against the released meta before the body rescore was read: pooled 832/893 = 93.2, design-B lodo 90/893 = 10.1 with PR-AUC 0.266/0.391, lodo_carm 814/893, dc_P 842/893, render 338/893 = 37.8, D-only 340/893 = 38.1 -- all exact.
- C-ArmLSpine and the plain-film banks need no truth change (their `box` is already the body); their body readings
  were re-read from the stored conventions (a1, a3, lcurve, contribution matrix, fig3, counting, dc_P).

## The finding, stated plainly

1. **The two conventions cross, on every device.** Arms trained on real C-ArmLSpine frames read ~89-91 % BODY and
   ~40 % WV on the C-arm; arms trained on renders or COBRA/DF frames read the reverse (80.5 % WV / 5.2 % BODY for
   the reported held-out detector). This is the learning-curve reversal already recorded, now confirmed on every
   scorer.
2. **NEW -- COBRA has the same mismatch in reverse, and it includes the control.** COBRA's own training truth is
   WV (planning-CT projected), so on genuine SPINEPS body truth the same-device control falls 93.2 % (832/893 WV)
   -> 35.8 % (306/855 BODY) [29.5, 42.0] while its WV reading on the same 855-vertebra subset stays 93.7 %. No
   COBRA number has a fair body score until the G4 corpus rebuild retrains on body boxes; until then the BODY
   column below records the convention mismatch, with its denominator.
3. **Counting, naming and coupling denominators are matching-defined.** Under body truth the WV-trained detector's
   matched sets collapse (197 -> 14 bodies on the C-arm; 76 -> 45 on COBRA), so their body columns are recorded
   artefacts; the usable body-convention versions are owed at G5 with the body-trained flagship.

## Rows

One row per quoted number. `kind` says where the body value comes from: stored (was on disk), computed (job
40419582 against the new body truth), derived (difference of stored body cells, no paired interval), declared
(no body truth exists; reason given), unchanged / already body.

### A a1 held-out detector, C-ArmLSpine test

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| A1 | vertebra recall at pre-stated 0.74 | 80.5 % (231/287) [74.1, 86.8] | 5.2 % (15/287) [2.4, 8.5] | stored | tables/tab2_detection.tex row 1; main.tex abstract + key results; sections/results.tex detection para; Figure 3a/c |
| A1s | sacrum found at pre-stated 0.74 | 76.8 % (43/56) [64.3, 89.3] | 76.8 % (43/56) [64.3, 89.3] | unchanged | tables/tab2_detection.tex row 1; main.tex abstract + key results; sections/results.tex |
| A2 | vertebra recall at YOLO default 0.25 | 90.6 % (260/287) [85.1, 95.1] | 5.2 % (15/287) [2.4, 8.5] | stored | tables/tab2_detection.tex row 1; main.tex abstract + key results; sections/results.tex detection para; Figure 3a/c |
| A2s | sacrum found at YOLO default 0.25 | 83.9 % (47/56) [73.2, 92.9] | 83.9 % (47/56) [73.2, 92.9] | unchanged | tables/tab2_detection.tex row 1; main.tex abstract + key results; sections/results.tex |
| A3 | vertebra recall at own best-F1 0.60 | 87.1 % (250/287) [80.9, 92.3] | 5.2 % (15/287) [2.4, 8.5] | stored | results/a1.json only |
| A3s | sacrum found at own best-F1 0.60 | 80.4 % (45/56) [69.6, 91.1] | 80.4 % (45/56) [69.6, 91.1] | unchanged | results/a1.json only |

- WV = CBCT-projected whole-vertebra outline; BODY = same WV-trained detector read against the SPINEPS body boxes the C-ArmLSpine meta already carries -- a convention mismatch of the detector, not a retrained score
- the sacrum keeps the whole-sacrum box in both conventions (SPINEPS defines no corpus for the sacrum)

### B a3 paired comparisons

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| B1 | pooled-vs-heldout sacrum found at 0.25 (paired diff) | 14.3 pp (n=56) [5.4, 23.2] | 14.3 pp (n=56) [5.4, 23.2] | unchanged | sections/results.tex: 'The same-device control found the sacrum on 98.2%..., a paired difference of 14.3 points' |
| B2 | pooled-vs-heldout vertebra at 0.25 (paired diff) | -49.8 pp (n=287) [-54.3, -44.5] | 85.4 pp (n=287) [79.5, 90.8] | stored | results/a3.json (labelled box-convention artefact); NUMBERS.md |
| B3_0.05 | film-trained vs render-trained detector on 233 film bodies at 0.05 | -- | 27.5 pp (n=233) [20.5, 35.2] | already body | sections/results.tex render-vs-film sentence; tables/tab2 film block; Figure 3c |
| B3_0.25 | film-trained vs render-trained detector on 233 film bodies at 0.25 | -- | 55.4 pp (n=233) [47.0, 63.6] | already body | sections/results.tex render-vs-film sentence; tables/tab2 film block; Figure 3c |

- identical in both conventions by construction
- outline -49.8 pp and body +85.4 pp are two readings of the same box-convention mismatch (pooled arm carries real carm frames that teach body boxes; the held-out arm does not); centre-rule +0.7 pp [0.0, 1.8] is the convention-insensitive comparison
- truth is the human vertebral-body corner annotation: no WV value exists and nothing changes

### C learning curve, C-ArmLSpine

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| C1_0.74 | stage 1 (styled renders of two other C-arms; Table 2 carm design-B row): vertebra recall at 0.74 | 63.1 % (181/287) [54.8, 71.0] | 12.5 % (36/287) [9.2, 15.9] | stored | tables/tab2_detection.tex C-ArmLSpine design-B row (WV); results.tex PENDING{G5}{learning curve...} |
| C1_0.25 | stage 1 (styled renders of two other C-arms; Table 2 carm design-B row): vertebra recall at 0.25 | 87.8 % (252/287) [81.4, 93.2] | 15.0 % (43/287) [11.0, 19.0] | stored | tables/tab2_detection.tex C-ArmLSpine design-B row (WV); results.tex PENDING{G5}{learning curve...} |
| C2_0.74 | fine-tuned on 50 real frames: vertebra recall at 0.74 | 39.7 % (114/287) [36.6, 42.6] | 81.5 % (234/287) [76.1, 86.8] | stored | Figure 3b (pending G5); results.tex PENDING{G5}{learning curve...} |
| C2_0.25 | fine-tuned on 50 real frames: vertebra recall at 0.25 | 43.2 % (124/287) [40.2, 46.2] | 88.5 % (254/287) [82.7, 93.5] | stored | Figure 3b (pending G5); results.tex PENDING{G5}{learning curve...} |
| C3_0.74 | fine-tuned on 200 real frames: vertebra recall at 0.74 | 39.4 % (113/287) [36.8, 42.0] | 80.1 % (230/287) [74.5, 85.7] | stored | Figure 3b (pending G5); results.tex PENDING{G5}{learning curve...} |
| C3_0.25 | fine-tuned on 200 real frames: vertebra recall at 0.25 | 41.8 % (120/287) [38.7, 45.0] | 89.5 % (257/287) [83.8, 94.6] | stored | Figure 3b (pending G5); results.tex PENDING{G5}{learning curve...} |
| C_ar_only_C-ArmLSpine_0.74 | all-real control 'only C-ArmLSpine': vertebra recall at 0.74 | 40.4 % (116/287) [37.8, 42.9] | 84.0 % (241/287) [78.2, 89.2] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |
| C_ar_only_C-ArmLSpine_0.25 | all-real control 'only C-ArmLSpine': vertebra recall at 0.25 | 41.5 % (119/287) [38.8, 44.0] | 89.9 % (258/287) [84.5, 94.7] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |
| C_ar_pooled_real_0.74 | all-real control 'pooled real': vertebra recall at 0.74 | 40.1 % (115/287) [37.7, 42.3] | 81.9 % (235/287) [76.4, 87.0] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |
| C_ar_pooled_real_0.25 | all-real control 'pooled real': vertebra recall at 0.25 | 40.8 % (117/287) [38.4, 43.0] | 90.6 % (260/287) [85.4, 95.1] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |
| C_ar_renders_+_all_real_0.74 | all-real control 'renders + all real': vertebra recall at 0.74 | 38.7 % (111/287) [35.9, 41.2] | 85.0 % (244/287) [79.3, 90.3] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |
| C_ar_renders_+_all_real_0.25 | all-real control 'renders + all real': vertebra recall at 0.25 | 39.0 % (112/287) [36.8, 41.3] | 89.5 % (257/287) [83.7, 94.3] | stored | tables/tab2_detection.tex footnote d (body values at 0.25 already quoted); results/lcurve/lcurve.md |

- C-ArmLSpine truth carries both conventions; primary `at` = body since job 40417427, WV now at #alt/outline. NUMBERS.md/tab2 citation paths that read #points[]/at now return the BODY value: stale citations
- controls trained on real carm frames learn BODY boxes, so WV penalises them (the reversed mismatch)

### C learning curve, COBRA Elekta

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| C_cobra_stage1_0.74 | COBRA stage 1 (design B lodo): vertebra recall at 0.74 | 10.1 % (90/893) [6.7, 13.1] | 1.3 % (11/855) [0.0, 3.2] | computed | Table 2 COBRA design-B row; results/lcurve/lcurve.md |
| C_cobra_stage1_0.25 | COBRA stage 1 (design B lodo): vertebra recall at 0.25 | 32.7 % (292/893) [28.4, 36.2] | 7.5 % (64/855) [4.0, 10.9] | computed | Table 2 COBRA design-B row; results/lcurve/lcurve.md |
| C_cobra_N48_s0_0.74 | COBRA N=48 s0: vertebra recall at 0.74 | 24.6 % (220/893) [16.9, 31.8] | 12.2 % (104/855) [8.2, 15.9] | computed | Figure 3b pending; results/lcurve/lcurve.md |
| C_cobra_N48_s0_0.25 | COBRA N=48 s0: vertebra recall at 0.25 | 52.9 % (472/893) [42.6, 61.8] | 19.4 % (166/855) [14.5, 24.2] | computed | Figure 3b pending; results/lcurve/lcurve.md |
| C_cobra_N408_s1_0.74 | COBRA N=408 s1: vertebra recall at 0.74 | 45.5 % (406/893) [34.5, 54.9] | 8.8 % (75/855) [5.0, 12.4] | computed | Figure 3b pending; results/lcurve/lcurve.md |
| C_cobra_N408_s1_0.25 | COBRA N=408 s1: vertebra recall at 0.25 | 83.2 % (743/893) [74.5, 89.7] | 17.8 % (152/855) [12.6, 23.2] | computed | Figure 3b pending; results/lcurve/lcurve.md |
| C_cobra_ar_pooled_real_0.74 | COBRA all-real control 'pooled real': vertebra recall at 0.74 | 93.2 % (832/893) [86.4, 97.7] | 35.8 % (306/855) [29.5, 42.0] | computed | tables/tab2_detection.tex COBRA control row (pooled real, WV) |
|  | ... WV on the 855-vertebra body subset | 93.7 % (801/855) [86.9, 98.3] |  |  |  |
| C_cobra_ar_pooled_real_0.25 | COBRA all-real control 'pooled real': vertebra recall at 0.25 | 97.4 % (870/893) [93.3, 99.8] | 36.3 % (310/855) [30.1, 42.3] | computed | tables/tab2_detection.tex COBRA control row (pooled real, WV) |
|  | ... WV on the 855-vertebra body subset | 97.8 % (836/855) [93.7, 99.9] |  |  |  |
| C_cobra_ar_C-ArmLSpine_held_out_0.74 | COBRA all-real control 'C-ArmLSpine held out': vertebra recall at 0.74 | 91.2 % (814/893) [83.4, 96.3] | 26.3 % (225/855) [20.5, 33.0] | computed | results/lcurve/lcurve.md all-real lines |
|  | ... WV on the 855-vertebra body subset | 92.3 % (789/855) [84.6, 97.0] |  |  |  |
| C_cobra_ar_C-ArmLSpine_held_out_0.25 | COBRA all-real control 'C-ArmLSpine held out': vertebra recall at 0.25 | 97.3 % (869/893) [92.7, 99.7] | 27.0 % (231/855) [21.0, 33.7] | computed | results/lcurve/lcurve.md all-real lines |
|  | ... WV on the 855-vertebra body subset | 97.2 % (831/855) [92.3, 99.7] |  |  |  |
| C_cobra_ar_renders_+_all_real_0.74 | COBRA all-real control 'renders + all real': vertebra recall at 0.74 | 94.3 % (842/893) [88.4, 98.0] | 40.2 % (344/855) [34.9, 46.1] | computed | results/lcurve/lcurve.md all-real lines |
|  | ... WV on the 855-vertebra body subset | 95.1 % (813/855) [89.3, 98.6] |  |  |  |
| C_cobra_ar_renders_+_all_real_0.25 | COBRA all-real control 'renders + all real': vertebra recall at 0.25 | 97.5 % (871/893) [93.5, 99.6] | 40.6 % (347/855) [35.2, 46.5] | computed | results/lcurve/lcurve.md all-real lines |
|  | ... WV on the 855-vertebra body subset | 97.7 % (835/855) [93.4, 99.8] |  |  |  |

- the lcurve cell's `at` block is labelled body but scores the released WV CT-projected boxes (893); the true BODY truth covers 855 of 893 vertebrae (22 SPINEPS-body too small, 16 body not visible >= 0.5)
- COBRA real-frame training truth is itself WV (planning-CT projected), so even the same-device control collapses on SPINEPS body truth: the convention mismatch, not a detection failure -- the WV reading on the 855-vertebra body subset stays at 93.7%. A fair body score on COBRA needs the G4 body-box retrain

### C learning curve, DeepFluoro

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| C_df_stage1_0.74 | DF stage 1 (design B lodo; Table 2 DF row): vertebra recall at 0.74 | 69.9 % (58/83) | -- | declared WV | tables/tab2_detection.tex DeepFluoro rows |
| C_df_stage1_0.25 | DF stage 1 (design B lodo; Table 2 DF row): vertebra recall at 0.25 | 94.0 % (78/83) | -- | declared WV | tables/tab2_detection.tex DeepFluoro rows |

- DF truth is whole-vertebra boxes projected from the specimen CT segmentation; one test specimen, no case interval

### D contribution matrix, C-ArmLSpine target

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| D1 | E-only (wide-arc COBRA source) on held-out C-arm, 0.25 | 86.8 % (249/287) [81.1, 91.8] | 11.1 % (32/287) [7.3, 15.5] | stored | sections/results.tex 'Transfer followed angular coverage' sentence (WV paragraph); tables/tab2 single-source rows; Figure S2 |
| D2 | D-only (cadaver Cios source) on held-out C-arm, 0.25 | 12.9 % (37/287) [8.3, 18.1] | 3.8 % (11/287) [1.4, 7.0] | stored | sections/results.tex 'Transfer followed angular coverage' sentence (WV paragraph); tables/tab2 single-source rows; Figure S2 |
| D3 | E cut to 240 frames on held-out C-arm, 0.25 | 39.0 % (112/287) [33.2, 44.7] | 3.1 % (9/287) [1.0, 5.8] | stored | sections/results.tex 'Transfer followed angular coverage' sentence (WV paragraph); tables/tab2 single-source rows; Figure S2 |
| D4 | renders-only on held-out C-arm, 0.25 | 31.7 % (91/287) [27.1, 36.1] | 2.4 % (7/287) [0.7, 4.5] | stored | sections/results.tex 'Transfer followed angular coverage' sentence (WV paragraph); tables/tab2 single-source rows; Figure S2 |
| D5 | add wide-arc E to D: marginal gain at 0.25 (paired) | 71.8 pp (n=287) [63.4, 79.6] | 17.8 pp (n=287) | derived | main.tex abstract + key results (+71.8); sections/results.tex |
| D6 | equal-count control: E cut to 240 vs full E, 0.25 (paired) | -47.7 pp (n=287) [-53.7, -41.8] | -8.0 pp (n=287) | derived | sections/results.tex 'cutting the wide-arc frames from 2,640 to 240 dropped it by 47.7 points' |

- WV-trained arms read low on body truth (convention mismatch); arms carrying real carm frames read high on body and low on WV -- the two conventions cross, which is why one convention must be stated everywhere
- abstract and key results quote +71.8 without a box convention; the derived body-convention gain is +17.8 pp
- same sign in both conventions; the results paragraph declares WV in its opening sentence

### D contribution matrix

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| D7 | seed spread on device-held-out cells (seed 0 vs seed 1) | 1.1-5.6 pp (COBRA 1.1; DF 3.3-5.6; C-ArmLSpine outline 4.2) | 7.3 pp (C-ArmLSpine body-truth reading 21.6 vs 14.3) | stored | sections/results.tex 'seed repeats moved it 1.1--5.6 points' |

- the body-convention spread reaches 7.3 pp and the sentence quotes only the WV 1.1-5.6

### D contribution matrix, COBRA target

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| D8 | S-only (C-arm source) on held-out COBRA, 0.25 | 12.2 % (109/893) [8.0, 16.0] | 8.9 % (76/855) [4.4, 13.1] | computed | tables/tab2 single-source rows; Figure S2 |
| D9 | D-only (Cios source) on held-out COBRA, 0.25 | 38.1 % (340/893) [32.3, 44.5] | 4.1 % (35/855) [2.5, 6.5] | computed | tables/tab2 single-source rows; Figure S2 |
| D10 | design A held-COBRA (S+D) on held-out COBRA, 0.25 | 30.2 % (270/893) [26.3, 34.2] | 6.5 % (56/855) [4.5, 8.2] | computed | tables/tab2 single-source rows; Figure S2 |

- stored cell had only `default` = WV; body truth now exists (855/893)

### E Figure 3a

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| E1_0.74 | renders-only on C-ArmLSpine: vertebra at 0.74 | 0.3 % (1/287) [0.0, 1.1] | 0.0 % (0/287) [0.0, 0.0] | stored | Figure 3a; sections/results.tex 'Renders alone found 31.7%...'; tables/tab2 renders row |
| E1_0.25 | renders-only on C-ArmLSpine: vertebra at 0.25 | 31.7 % (91/287) [27.0, 36.0] | 2.4 % (7/287) [0.7, 4.5] | stored | Figure 3a; sections/results.tex 'Renders alone found 31.7%...'; tables/tab2 renders row |
| E2_0.74 | renders-only on COBRA: vertebra at 0.74 | 5.2 % (46/893) [3.0, 7.4] | 0.0 % (0/855) [0.0, 0.0] | computed | Figure 3a; NUMBERS.md Fig 3 block |
| E2_0.25 | renders-only on COBRA: vertebra at 0.25 | 37.8 % (338/893) [33.9, 42.1] | 3.3 % (28/855) [1.7, 5.6] | computed | Figure 3a; NUMBERS.md Fig 3 block |
| E3_0.74 | design-A lodo (real S+D frames) on COBRA: vertebra at 0.74 | 6.2 % (55/893) [2.9, 9.4] | 5.4 % (46/855) [1.7, 9.2] | computed | Figure 3a; NUMBERS.md Fig 3 block |
| E3_0.25 | design-A lodo (real S+D frames) on COBRA: vertebra at 0.25 | 18.5 % (165/893) [13.7, 22.8] | 13.6 % (116/855) [7.9, 19.6] | computed | Figure 3a; NUMBERS.md Fig 3 block |
| E4 | render / lodo_df on DeepFluoro (all four cells) | 0.0 / 59.0 / 74.7 / 95.2 (0/83, 49/83, 62/83, 79/83) | -- | declared WV | Figure 3a |

- WV quoted; body stored beside it
- the scored fig3 cobra files carry ONLY a `body` block that is in fact the WV CT-projected truth (has_outline_truth=false); the genuine body reading is this job's
- one specimen, no case interval; fig3 file's `body` label is WV

### E Figure 3a/S2

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| E5 | Geneva phantom cells (all arms) | e.g. dc_P 27.0 (10/37) | -- | declared WV | Figure S2; results/dc_P_pooled_scores.json |

- one phantom cluster

### F counting from the sacrum

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| F1 | C-ArmLSpine lodo_carm 0.74: matched bodies at the right ordinal | 95.4 % (188/197) [89.4, 99.5] | 92.9 % (13/14) [75.0, 100.0] | stored | main.tex abstract + key results ('Counting placed 188 of 197...'); sections/results.tex; Table 3; Figure 5b |
| F2 | C-ArmLSpine lodo_carm 0.25: matched-ordinal / within-one | 84.7 % (199/235) [77.4, 90.7] | 78.6 % (11/14) [44.4, 100.0] | stored | sections/results.tex; results/COUNTING.md |
| F3_0.25 | COBRA lodo_cobra 0.25: defined share / matched-ordinal (body truth) | 18.2 % (111/609); ordinal 54/76 = 71.1 [56.6, 80.3] (WV truth) | 55.6 % (25/45) [28.6, 72.5]; defined 111/609; within-one 44/45 | computed | Table 3 COBRA row; results/COUNTING.md |
| F3_0.74 | COBRA lodo_cobra 0.74: defined share / matched-ordinal (body truth) | -- | 45.5 % (5/11) [0.0, 100.0]; defined 22/609; within-one 9/11 | computed | Table 3 COBRA row; results/COUNTING.md |
| F4 | DeepFluoro 79.1 (53/67) and pooled three devices 81.0 (306/378) [75.7, 85.8] | 81.0 % (306/378) [75.7, 85.8] | -- | declared: DF has no body truth, so the pooled three-device counting row cannot be rescored whole | sections/results.tex pooled counting; Table 3 |

- the WV-trained detector's boxes rarely reach IoU 0.5 against body truth, so almost no bodies match; a body-convention counting number needs the G5 body-trained flagship
- same mismatch as F1
- defined share is anchor-driven (sacrum, convention-free) and stays 18.2%; matched bodies fall 76 -> 45 and ordinal accuracy 71.1 -> 55.6 [28.6, 72.5] because the WV-trained detector's boxes miss body-truth IoU
- COBRA part rescored above; DF part declared; pooled body row owed at G5

### G coupling (classifier x count)

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| G1 | det74/kfull: anchored frames, disagreement, flags (whole block) | 233/290 anchored; 1,009 counted; disagree 3.2% [1.4, 5.4]; unflagged 921/922 | -- | declared: anchored on the WV detector's sacrum box; the sacrum box is identical in both conventions, but the count runs over detector body-box matches, so the body recompute is owed with the G5 body-trained flagship | sections/results.tex coupled-call paragraph; Table 3; Table 4; Figure 5c/d |

- classifier numbers are convention-free (it crops by name); only the count arm carries the box convention

### H naming, C-ArmLSpine

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| H1 | cv5 lateral exact 98.2 (606/617) [95.7, 100.0] and the whole a4/a7/a9 family | 98.2 % (606/617) [95.7, 100.0] | -- | declared: the denominators | main.tex abstract + key results; sections/results.tex naming paragraph; Table 3; Figure 5a |
| H2 | zero-shot lateral 96.3 (594/617) vs AP 37.9 (239/631), delta +57.7 [48.9, 66.4] | 96.3 % (594/617) [93.1, 98.7] | -- | declared | main.tex abstract; sections/results.tex |

- no stored body variant exists in a4/a7/a9; the C-ArmLSpine meta carries body boxes, so the re-match is possible once the flagship's body-trained detector defines the matched set
- as H1

### I plain-film naming

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| I_CSXA | CSXA exact naming | -- | 99.8 % (3629/3635) [99.6, 100.0] | already body | sections/results.tex 'patient-keyed film validation read 97.3%-99.8%'; Table 3 |
| I_BUU | BUU exact naming | -- | 97.3 % (2671/2744) [96.5, 98.0] | already body | sections/results.tex 'patient-keyed film validation read 97.3%-99.8%'; Table 3 |
| I_NHANES | NHANES II exact naming | -- | 99.1 % (441/445) [98.2, 99.8] | already body | sections/results.tex 'patient-keyed film validation read 97.3%-99.8%'; Table 3 |

- truth was annotated as body boxes from the start

### J pooled all-device detector (dc_P)

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| J1 | C-ArmLSpine test recall at 0.25 | 39.0 % (112/287) | 89.5 % (257/287) | stored | results/lcurve/lcurve.md all-real lines; not yet in a table |
| J2 | COBRA test recall (eval 97.5 = 871/893 at 0.25) | 97.5 % (871/893) [93.5, 99.6] | 40.6 % (347/855) [35.2, 46.5] | computed | results/lcurve/lcurve.md; not yet in a table |
| J3 | DeepFluoro 97.6 (81/83) and Geneva 27.0 (10/37) | 97.6 / 27.0 | -- | declared WV | results/dc_P_pooled_scores.json |

- dc_P trains on real carm frames, so body >> WV here
- same COBRA training-truth mismatch as the control row; WV on the body subset 97.7% (835/855)
- as E4/E5

### K COBRA panel-aware (cobra_window)

| id | quantity | WV | BODY | kind | consumers |
|---|---|---|---|---|---|
| K1 | pooled all-real conf 0.74: 93.2% (832/893); whole-panel-only 95.4% (333/349); renders 5.2% (46/893) | 93.2 % (832/893) [86.4, 97.7] | 35.8 % (306/855) [29.5, 42.0] | computed for the pooled 93.2 and renders 5.2 | tables/tab2 via lcurve all_real; panel split not yet quoted |

- all WV COBRA truth today; renders at 0.74 read 0/855 on body truth

## Sentences the body values alter (named, not edited)

1. **[A1]** main.tex key results: 'A detector trained on the real exposures of two other C-arms found 231 of 287 vertebrae (80.5%...)' and abstract: 'The held-out detector found 231 of 287 vertebrae (80.5%...)' state no box convention; under the paper's adopted body convention the same arm reads 5.2%, so these two sentences must say 'whole-vertebra' (results.tex and tab2 already do)
2. **[C1_0.74]** tables/tab2_detection.tex design-B row quotes 63.1 (181/287) citing lcurve #points[0]/at, but that path now returns the BODY 12.5% (36/287): the value printed is right for WV, the cited path is stale
3. **[C_cobra_stage1_0.74]** tables/tab2_detection.tex COBRA design-B row 10.1 (90/893): value unchanged for WV, but the row's source path (lcurve #at) is labelled body while being WV -- the label, not the number, is wrong
4. **[C_cobra_ar_pooled_real_0.74]** tables/tab2_detection.tex COBRA control row '93.2 (832/893)': the table's header note declares WV so the row stands, but footnote d's body-convention remark covers only C-ArmLSpine; COBRA's control reads 35.8% (306/855) on body truth and the footnote does not say so
5. **[D5]** main.tex key results: '...the training source whose exposures span the gantry arc carried the transfer (+71.8 percentage points; 63.4, 79.6)' states no box convention (WV); under body truth the same margin is +17.8 pp of a 21.6% ceiling -- direction unchanged, size convention-dependent
6. **[D7]** sections/results.tex: 'and seed repeats moved it 1.1--5.6 points' omits the 7.3-pp spread the same arms show under the body convention (NUMBERS.md's own row says the sentence should carry '(7.3 under the body convention)')
7. **[F1]** main.tex abstract: 'Counting placed 188 of 197 matched bodies at the right ordinal (95.4%)' and sections/results.tex 'put 95.4% of 197 matched bodies at the right ordinal (188...)' state no box convention (the Figure 5 caption does); under body truth the matched set collapses to 14

Everything else quoted in the manuscript either states the whole-vertebra convention in the same sentence or
paragraph (results.tex detection paragraph: 'whole-vertebra boxes throughout'; tab2 header note and footnotes a/d),
is convention-free (sacrum, classifier, Table 1, device cards, manifold, power table), or is already in the body
convention (film truth, C-ArmLSpine body columns) -- those sentences do not change.

## Not rescored here, and why

- **DeepFluoro and Geneva**: no SPINEPS body masks exist for the specimen CTs / phantom; A28(iii) says convert or
  declare -- declared WV in every row above.
- **COBRA whole-panel split (95.4 % = 333/349)**: owned by the cobra-window workflow; the body truth it needs is
  now on disk (`or_ready/bodybox_rescore/truth/cobra_elekta`).
- **Naming re-match (H) and coupling (G)**: possible only against a body-trained detector's boxes; gate G5, as
  NUMBERS.md already records.
- **Stale citation paths**: NUMBERS.md and tab2 cite `lcurve.json#points[0]/at` for the C-ArmLSpine design-B row;
  since job 40417427 that path returns the BODY value (12.5 %), the printed WV 63.1 lives at `#alt/outline`. The
  same relabel applies to the COBRA/DF lcurve cells, whose `at` is labelled body but scores WV boxes.

