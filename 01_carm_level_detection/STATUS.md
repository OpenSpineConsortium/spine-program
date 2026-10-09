# STATUS: the results in hand, with their numbers, files and rigor marks

Cut from `docs/handoff/RESULTS_CATALOG.md` (2026-10-08) Parts A (paper 1), C3 (the sweep line), C4 (DeepFluoro and
devices) and E (power), and from the memory notes' statuses (`MEMORY.md`). Status words and rigor marks are the catalog's:
CURRENT (printed in the manuscript as last built, grid jobs 40483839 / 40483840, 2026-09-27, commit 05e05dc), CURRENT-SEL
(measured on the split that chose the checkpoint), HELD-OUT NOT QUOTED, SUPERSEDED, DISPUTED, RECORD ONLY, NOT RECORDED,
OPEN; marks [THR] threshold chosen after seeing a result, [SEL-SPLIT], [LEAK], [ONE-SEED], [AUTO-TRUTH] (two automatic
labellers agreeing, no human read), [DERIVED], [WORDING], [E] expectation, [X] extrapolation. `sn:` = `manuscripts/schwingnet/`
and `results/schwingnet/` here; `~` = HOME `/wsu/home/go/go24/go2432`; `$RS` = `/rs/rs_grp_oschome/go2432`.

**The truth behind every C-ArmLSpine row.** Two automatic CBCT labellers (TotalSegmentator, SPINEPS + VERIDAH) scored
only where they agree: 814 of 910 vertebrae (89.5 %), T11 0 of 3, T12 6 of 63. No level truth in the study was set by a
human (`docs/MODEL_CARD.md` section 5.1). PRE truth = the export before the 2026-09-23 repairs (every printed naming
number); REP truth = after. Every naming row carries [AUTO-TRUTH]. The 149 released cases (148 scored, 141 to 142 with
whole-frame naming) are acquisitions on five dates, not known persons (OQ E1).

## 1. The model (`docs/handoff/DATASET_USAGE.md` section 1)

Naming detector `detector_v5z_final` (conf 0.35); sacrum / vertebra detector `rx_lodo_carmlspine_1024` (conf 0.74
"cross-device" or 0.25; trained on 3,094 real COBRA Elekta + DeepFluoro frames; C-ArmLSpine never seen); level encoder
`~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (sha256 prefix 188f9fcbfa3c6de1); head
`head_allspine_v9_mixed_kmax4_seed0`; the five `v9init` fold models for fine-tuned numbers; count and coupling with no
learned parameters. Not part of it: the un-suffixed v2-initialised fold models (bank deleted; refused by the gate),
`detect_v5z_epoch25` and M19 (the service's older release), the device-corpus detectors `dc_A/B/P_*`.

## 2. Zero-shot naming on the unseen C-arm (A2; model never saw the device)

| id | result | file | status |
|---|---|---|---|
| A2.1 | lateral, whole frame: 595 / 617 (96.4 %), 141 cases (6 with an error); Wilson on effective n [92.3, 98.4] (design effect 3.84); percentile [93.3, 98.9]; BCa [92.5, 98.7]; answered 83.0 %, exact on answered 97.7 % | `results/schwingnet/eval_gate/leaks/zeroshot_v9.json`; `results/schwingnet/eval_gate/closure/cv_v9/cv_v9.json` | CURRENT, HELD OUT [AUTO-TRUTH]; Key Point 1, Table 3 |
| A2.2 | AP, whole frame: 276 / 631 (43.7 %), 142 cases (83 with an error) [34.9, 51.9]; answered 20.9 %, exact on answered 47.0 % | same | CURRENT, HELD OUT |
| A2.3 | lateral minus AP +54.3 points [45.6, 62.9] on 593 vertebrae of 140 cases; cases 79 : 1; sign test p 1.34e-22, Holm 5.4e-22 | `results/schwingnet/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` section 4 | CURRENT |
| A2.4 | lateral with three / one vertebrae in field: 970 / 1,159 (83.7 %) [79.6, 87.5]; 385 / 603 (63.8 %) [59.8, 67.9] | `results/schwingnet/eval_gate/closure/cv_v9/cv_v9.json` | CURRENT, HELD OUT; Table 3 |
| A2.5 | AP with three / one in field: 391 / 1,176 (33.2 %); 112 / 591 (19.0 %) | `results/schwingnet/eval_gate/closure/cv_v9/cv_v9.json#families/pre:zs_v9head` | HELD-OUT, NOT QUOTED |
| A2.6 | counting the 59 undetected bodies as wrong: 595 / 676 = 88.0 % | Table 3 note b | CURRENT |
| A2.7 | naming-detector recall of agreed lateral bodies: 617 / 676 (91.3 %) | `results/carmlspine_v2_lineage_2026-09-21/carmlspine_cv5_mixed_2026-09-21.json` key `det/LAT/kfull` against `oracle/LAT/kfull` (flat keys with slashes) | CURRENT |
| A2.8 | zero-shot AP errors are a one-level cranial shift: L4 to L3 x51, L3 to L2 x51, L5 to L4 x48, L2 to L1 x46, L1 to T12 x21 | `results/schwingnet/coverage/PER_LEVEL_DOMAIN_ANGLE.md` Table C | HELD-OUT, NOT QUOTED [DERIVED] |
| A2.9 | first zero-shot run on `allspine_v2_r1`: 594 / 617 (96.3 %), 239 / 631 (37.9 %) | `results/schwingnet/a7.json`; `results/carmlspine_v2_lineage_2026-09-21/carmlspine_zeroshot2_pooled_all_2026-09-21.json` | **SUPERSEDED** (the encoder's bank was deleted); still printed in `manuscripts/schwingnet/tables/tab3_naming.md` and `atlas/model.json`: fix before submission |

## 3. Fine-tuned cross-validation on C-ArmLSpine (A3; v9init fold models)

| id | result | status |
|---|---|---|
| A3.1 | lateral whole frame, case-grouped: 601 / 617 (97.4 %), 141 cases (4 with an error); Wilson [93.2, 99.0]; BCa [93.2, 99.4]; answered 503 / 617 (81.5 %), exact on answered 497 / 503 (98.8 %) | CURRENT, HELD OUT [AUTO-TRUTH]; abstract, Table 3 |
| A3.2 | AP whole frame, case-grouped: 608 / 631 (96.4 %), 142 cases (7); Wilson [92.5, 98.3] | CURRENT, HELD OUT; Key Point 2 |
| A3.3 | lateral three / one in field: 1,079 / 1,159 (93.1 %) [89.2, 96.2]; 451 / 603 (74.8 %) [70.9, 78.7] | CURRENT; Key Point 2 |
| A3.4 | AP three / one in field: 1,005 / 1,176 (85.5 %); 399 / 591 (67.5 %) | CURRENT; Table 3 |
| A3.5 | day-grouped whole frame: lateral 568 / 617 (92.1 %) [87.5, 96.0]; AP 598 / 631 (94.8 %) [90.1, 97.3] | CURRENT; limitations ("below zero-shot") |
| A3.6 | day-grouped three in field: lateral 1,016 / 1,159 (87.7 %); AP 1,011 / 1,176 (86.0 %) | CURRENT |
| A3.7 | paired, lateral: case-grouped minus zero-shot +1.0 [-1.9, 4.0], cases 4 : 2, p .69; day-grouped minus zero-shot -4.4 [-9.1, 0.2], 4 : 10, p .18; case minus day +5.3 [2.1, 9.1], 8 : 0, p .008 (last not printed) | CURRENT (first two) |
| A3.8 | paired, AP: case-grouped minus zero-shot +52.6 [44.1, 61.3], 78 : 2 | CURRENT |
| A3.9 | per level, lateral whole frame: L1 97.4 (n 76), L2 96.8 (123), L3 97.2 (141), L4 97.2 (141), L5 98.5 (136); AP 95.5 to 97.7; one in field L1 41.2 % lateral / 9.5 % AP is the weakest cell | `PER_LEVEL_DOMAIN_ANGLE.md` Table C; HELD-OUT, NOT QUOTED [DERIVED]; a Table S5 awaits Greg (A9) |
| A3.10 | reading: lateral naming is saturated before any same-device frame; AP is a coverage hole the device's own frames fill; same-device data helps most at one body in field (+10.9 [+6.4, +15.5]) | `MANUSCRIPT_CORRECTIONS.md` section 8; CURRENT reading [WORDING] |
| A3.11 | v2-lineage CV: lateral 606 / 617 (98.2 %), AP 96.7 %, k5 97.0, k3 92.9, k1 72.8 | **SUPERSEDED**; still in the `tab3_naming.md` twin and the ATLAS cards |

## 4. Counting from the detected sacrum (A4), coupling and the stop signal (A5)

| id | result | status |
|---|---|---|
| A4.1 | C-ArmLSpine test (28 cases, 56 frames) at 0.74, outline boxes: counting defined 46 / 56 (82.1 %) [69.6, 92.9]; detected sacrum true 43 / 46; ordinal correct 188 / 197 matched (95.4 %) [89.4, 99.5]; within one 197 / 197; truth bodies right over defined frames 188 / 232 (81.0 %) [73.8, 87.6] | CURRENT, HELD OUT [THR]; Table 3 |
| A4.2 | same at 0.25: defined 51 / 56; ordinal correct 199 / 235 (84.7 %) [77.4, 90.7]; within one 225 / 235 | CURRENT |
| A4.3 | misses by ordinal: 25 of 35 missed bodies at ordinals 5-6; 16 within 6 px of the frame border | `results/schwingnet/fig5_naming_data.json#b`; printed in an earlier revision only |
| A4.4 | COBRA2026 test at 0.25: defined 111 / 609 (18.2 %); ordinal correct 54 / 76 (71.1 %) [56.6, 80.3] | CURRENT |
| A4.5 | DeepFluoro test specimen at 0.25: 53 / 67 (79.1 %), one cluster, no interval | twin only |
| A4.6 | pooled over three held-out devices at 0.25: defined 252 / 755 (33.4 %); ordinal correct 306 / 378 (81.0 %) [75.7, 85.8]; within one 366 / 378 | CURRENT |
| A4.7 | count alone on anchored fold frames at 0.74: 979 / 1,009 (97.0 %) [94.2, 99.2], 130 cases (no encoder) | CURRENT; Key Point 2 |
| A5.1 | on 1,009 counted bodies at 0.74: classifier 986 (97.7 %) [95.9, 99.2]; count 979 (97.0 %) [94.2, 99.2]; coupled 991 (98.2 %) [96.5, 99.5] | CURRENT, HELD OUT; Key Point 2 |
| A5.2 | coupled minus count +1.2 points [0.0, 3.2]; minus classifier +0.5 [-1.5, 2.4] | CURRENT |
| A5.3 | disagreement frames 13 / 233 (5.6 %) [2.6, 9.2]; stop on 23 / 233 (9.9 %) [5.7, 14.5] (13 disagreement + 10 low margin); catches 5 of 6 erring frames | CURRENT |
| A5.4 | L6 calls on 3 of 233 anchored frames (case139 AP + LAT, case44 LAT), all stopped; coupled exact on their 12 bodies, count 0 / 12 | CURRENT |
| A5.5 | the three one-labeller L6 patients: 6 frames, 4 anchored, one L6 call (case42 LAT, flagged); classifier 0 / 5, coupled 1 / 5 on the five bodies one labeller reads L6 (agreement, not correctness) | CURRENT [AUTO-TRUTH]; Figure 4d |
| A5.6 | at 0.25 (266 anchored, 1,149 bodies): classifier 97.7 %; count 96.1 %; coupled 97.1 %; disagreement 19 / 266 | CURRENT |
| A5.7 | v2-lineage coupling (993 / 995 of 1,009; 12 / 233 disagreement) and oracle-box rows | `results/schwingnet/coupling.json`; SUPERSEDED; twin only |

## 5. Detection on the held-out device and what carries it (A6, A7)

| id | result | status |
|---|---|---|
| A6.1 | vertebra / sacrum recall at 0.74: 231 / 287 (80.5 %) [74.1, 86.8]; 43 / 56 (76.8 %) [64.3, 89.3]; "short of the pre-stated 97 %" | CURRENT, HELD OUT [THR]; Table S2 |
| A6.2 | at 0.25: 260 / 287 (90.6 %) [84.3, 94.5]; sacrum 47 / 56 (83.9 %) [73.2, 92.9] | CURRENT |
| A6.3 | at 0.60 (own best F1, tuned on the test split, a bound only): 87.1 %; sacrum 80.4 % | `a1.json`, not a headline [THR] |
| A6.4 | recall against confidence, 17 thresholds: 0.01 gives 92.7 %, 0.74 gives 80.5 %, 0.80 gives 67.9 %, 0.90 gives 0.0 % | `results/schwingnet/RIGOR_FIXES.md` A1; CURRENT |
| A6.5 | on the repaired denominator: 201 / 214 (93.9 %) [90.4, 97.1]; re-scored on the rebuilt truth the released denominator reads 236 / 287 | `results/schwingnet/indomain/denominator_repair.json` (job 40448892); CURRENT (both printed) |
| A6.6 | sacrum anchored on fold frames at 0.74: 233 of the 286 frames showing a sacrum (81.5 %) | `manuscripts/schwingnet/REVIEW2_STATS.md` N15; CURRENT |
| A6.7 | same-device control minus held-out, sacrum at 0.25: 98.2 % vs 83.9 %, +14.3 [5.4, 23.2]; sign test 8 : 0; Holm P = .009 | `a3.json#comparisons/pooled_vs_heldout_detector`; CURRENT |
| A6.8 | same-device controls under the outline rule 40.4 / 41.5 % (a box-convention artefact); under the body rule 89.9 % and 90.6 % | `results/schwingnet/lcurve/lcurve.json`; CURRENT; Table S2 |
| A6.9 | COBRA2026 held out (Elekta never seen): 6.2 % (55 / 893) at 0.74, 18.5 % at 0.25; sacrum 21 / 609 at 0.74 | `a1.json`; CURRENT |
| A6.10 | DeepFluoro test specimen held out: 74.7 % (62 / 83) at 0.74, 95.2 % at 0.25, sacrum 90 / 90 (one cluster) | `a1.json`; CURRENT |
| A6.11 | design B (styled renders of the other two devices + their real frames): C-ArmLSpine 63.1 % at 0.74, 87.8 % at 0.25; COBRA 10.1 / 32.7 %; DeepFluoro 69.9 / 94.0 % | `a1.json`; CURRENT |
| A6.12 | renders only: C-ArmLSpine 0.3 % (1 / 287) at 0.74, 31.7 % at 0.25 | `a1.json`; CURRENT |
| A6.13 | the pre-stated counting-grade target (at least 97 % vertebra and sacrum, `docs/RSNAI_PLAN.md` C7) is met by no held-out cell; `MODEL_CARD.md` 4.6 says "not met on two of the three devices" though its Cios row (91.6 to 94.0 %) is also below 97; the primary C7 criterion (paired bootstrap against the LODO baseline) was never run | CURRENT (not met) [WORDING in MODEL_CARD] |
| A7.1 | radiotherapy imager (Elekta) frames alone to C-ArmLSpine: 86.8 % (249 / 287) [81.1, 91.8] | CURRENT, HELD OUT; Figure S4 |
| A7.2 | cadaver C-arm (Cios / DeepFluoro) alone to C-ArmLSpine: 12.9 % (37 / 287) [8.3, 18.1] | CURRENT |
| A7.3 | adding E to D +71.8 [63.4, 79.6]; adding D to E -2.1 [-6.0, +1.4] | CURRENT |
| A7.4 | cutting E's real frames 2,640 to 240: -47.7 [-53.7, -41.8] | CURRENT |
| A7.5 | COBRA held out: add D to S +18.0 to +23.9; add S to D -7.8 [-12.5, -3.9] | CURRENT |
| A7.6 | seed spread on multi-cluster held-out cells 1.1 to 5.6 points (7.3 under body) | CURRENT |
| A7.7 | no arm isolates angle: E differs from D in device, anatomy, frame count and angle together | `manuscripts/schwingnet/CLAIMS_LEDGER.md` section 1 (REWRITE verdict F13); CURRENT caution |
| A7.8 | design B hurts on the C-arm at 0.74 (63.1 vs 80.5) and helps on the Elekta imager (32.7 vs 18.5 at 0.25) | HELD-OUT reading |

## 6. Same-device learning curve and its plateau (A8), naming against training persons (A9)

| id | result | status |
|---|---|---|
| A8.1 | no frame of the device: 7.0 % (20 / 287) body at 0.74; stage 1 alone 12.5 %; the N = 0 floor is a box-convention artefact | `results/schwingnet/indomain/det_fill.json`, `INDOMAIN.md` section 2; CURRENT, HELD OUT |
| A8.2 | body at 0.74, both views pooled: N 0 7.7 %, 4 72.4 %, 10 76.0 %, 24 84.0 % (723 / 861), 50 82.5 %; at N = 24 lateral 84.1 %, AP 84.6 % | `FIT_N.md`; `power.json#panel_c_detection/curves`; CURRENT; Figure 5c |
| A8.3 | 50 to 210 frames read 81.5 to 86.8 %; every interval from 50 frames up overlaps | `lcurve.json`; CURRENT |
| A8.4 | one-view arms (25 or 50 frames, two seeds): own view 83.0 to 86.4 %; the other view 0.0 to 39.5 % | CURRENT |
| A8.5 | model-free plateau check: N 24 vs N 200 lateral +2.2 [-1.1, +6.0], AP +1.7 [0.0, 3.8] | HELD-OUT, NOT QUOTED |
| A8.6 | in-domain frames vs substitutes at N = 24: lateral +28.5 points over COBRA frames, +15.7 over styled renders; AP +20.7 / +27.0 | `INDOMAIN.md` section 3; HELD-OUT, NOT QUOTED |
| A8.7 | **the plateau is the truth denominator**: 30 of 287 missed by all ten plateau arms, 208 hit by all; CBCT-cut vertebrae missed 51.5 % of the time vs 6.7 % for complete ones; on complete, agreed, SPINEPS-boxed bodies (204 of 287) the arms read 96.9 %; on the repaired denominator N 24 reads 95.6 % [92.9, 98.0] (614 / 642), N 200 94.9 % | `indomain/miss_diagnostic/MISS_DIAGNOSTIC.md` (job 40448862); `denominator_repair.json#summary` (job 40448892); CURRENT; the text change is left for Greg (A10) |
| A8.8 | asymptote fits (inverse power law, 2,000 case-clustered resamples): lateral 81.7 % [76.7, 86.6], AP 85.3 % [81.0, 90.7]; 95 % of the asymptote at 10.0 [5.1, 23.5] lateral and 11.9 [6.7, 33.5] AP frames; 90 % absolute recall "not reached"; at 0.25 asymptotes 92.3 / 93.9 % (centre rule), 91.3 / 93.8 % (body rule); same-device naming asymptotes not identified at 87 persons | `FIT_N.md`; `fit.json` (n_boot 2,000); HELD-OUT, NOT QUOTED; `INDOMAIN.md` (10 resamples) is stale against `fit.json` |
| A8.9 | caveat: the device's styled renders were posed on the registered geometry of all 148 cases, test cases included | `INVENTORY.md` "Pose donors"; CURRENT caveat |
| A8.10 | the earlier real-frame learning curve (2026-09-23): N 0 7.3 %, about 50 81.5 %, about 200 80.1 / 82.2 %, all real 81.9 % (210 frames); C-ArmLSpine transitional row 74.3 % (26 / 35) from N = 50, three clusters | `results/schwingnet/lcurve/lcurve.md`; CURRENT in supplement; superseded for Figure 5 by A8.2 |
| A9.1 | lateral protocol, whole frame: N 0 93.7 %, 5 96.7, 10 96.5, 25 97.5, 50 98.1, all 98.1 % | CURRENT, HELD OUT; Figure 5b |
| A9.2 | AP protocol, whole frame: 33.8 to 90.8 (5 persons) to 94.7 to 95.4 to 95.4 to 98.1 % (all, 84 to 96 per fold) | CURRENT |
| A9.3 | lateral-trained, read on AP: 32.2 to 54.7 % | CURRENT |
| A9.4 | both protocols trained, all persons: lateral 98.1 %, AP 97.0 % (v9-base fold models with no VinDr or FluoroCap, REP truth per protocol cell) | CURRENT |
| A9.5 | narrow fields: AP three in view 28.5 to 87.6 %, one in view 15.7 to 74.6 %; lateral three 83.6 to 93.1, one 63.9 to 77.1 %; still rising at 88 persons | `INDOMAIN.md` sections 5, 8; HELD-OUT, NOT QUOTED |
| A9.6 | substitutes at the same person count (AP whole frame): same-protocol plain films 80.6 to 96.4 %; CT renders 26.2 to 53.7 %, vs in-domain 90.8 to 98.1 %; exchange rate film 3.6 at N 5, 1.7 at 25, 1.2 at 50; renders "millions" [X] | `INDOMAIN.md` section 6; HELD-OUT, NOT QUOTED |
| A9.7 | collection guidance: about 12 patients (24 frames, both views) of a device for detection; whole-frame AP naming 68 persons for 97 %, 1,071 for 99 % [X]; for collimated fields keep collecting | `INDOMAIN.md` section 8; not quoted |
| A9.8 | zero-shot references on REP truth: lateral 96.3 % (600 / 623), AP 43.9 % (278 / 633) | `INDOMAIN.md` section 5; HELD-OUT, NOT QUOTED |

## 7. What the encoder learned (A1, selection split), the corpus (A18), the integrity numbers (A19)

A1.1 nearest crop of another person is the same level 9,740 of 13,009 (74.9 % [72.2, 77.6]), 1,612 persons; A1.2
silhouette L6/L5 0.35 [0.31, 0.39] vs L5/L4 0.23, L1/T12 0.32; A1.3 75 of 98 L6 crops named L6, 111 of 1,012 L5 crops named
L6; A1.5 never-seen L6 (C-ArmLSpine case42, case121, case136): two-cluster silhouette 0.10 / 0.12 / 0.16, 84 of 180 crops
named L6 (CURRENT, HELD OUT [AUTO-TRUTH: one labeller's read]); A1.7 occlusion: for L4 to L6 more attribution on the body
below (36 to 43 %) than on the target (24 to 32 %); A1.8 no T13 crop in validation (44 in training). All CURRENT-SEL unless
stated (`results/schwingnet/figure2/figure2_metrics.json`).

A18.1 median age 36 y (CSXA) to 66 y (COBRA2026); female 42.5 to 64.5 %; none released for the intraoperative, cadaveric or
phantom sets (`results/schwingnet/age_sex_by_source.json`); A18.2 corpus totals 4,093 renders, 9,108 level-annotated films,
4,276 real exposures (778 C-arm): **DISPUTED** (A18.5: Table 1 counts `ts_drr` and `ts_drr_v3`, which the v9 build never
reads, and omits `physics_drr` and `physics_rare`; trust the build script `slurm/allspine_v9_bank.sh`; Table 1 needs
correcting, OQ F6); A18.4 7,045 vs 7,048 physics-styled renders, recorded unexplained. A19.2 CHK-9 over 563 quoted numbers:
after the v9 closure 380 held out, 81 seen, 1 unresolved, 101 not applicable (`results/schwingnet/eval_gate/EVAL_LEAKS.md`);
A19.3 306 checkpoints in the lineage census, 133 with an unreadable link; A19.4 57 quoted numbers traced to the deleted
`allspine_v2_r1` bank, re-run on v9; A19.5 NHANES II in the banks twice, 48 of 54 validation patients twinned (v6, v7);
A19.7 69 quoted detector numbers re-scored in both box conventions (`results/schwingnet/bodybox_rescore/RESCORE.md`);
A19.10 COBRA2026 frames counted up to four times in one arm: 5,013 duplicate entries (`results/schwingnet/repairs/`).

## 8. The sweep / chain / confirmation line (C3; private) and DeepFluoro / devices (C4)

| id | result | status |
|---|---|---|
| C3.1 | sweep_v3 (respaced renders), 120 held-out CTSP spines, 2-body overlap, 9-inch field: naming 72.1 to 95.2 %; chain 97.5 %; with the end rule 120 / 120 | `~/model_night/sweep_v3/` (job 40384843); RECORD ONLY. Only sweep_v3 counts: every earlier sweep used the wrong field size |
| C3.2 | TotalSegmentator bench, 522 spines from the sacrum: 98.5 % chains; 203 from C2 95.1 % | held out only for the v7-lineage encoder; for v9 only 71 cases are unseen |
| C3.3 | 25 real lumbar films: chain 100 % with true boxes; 21 / 25 with the detector | RECORD ONLY |
| C3.4 | 2 bodies of overlap optimal (97.5 % chains) | `docs/SWEEP_PROTOCOL.md`; protocol recommendation |
| C3.5 | counting with boxes given: 99.66 % of 6,255 walks (801 CTSP); C2 down on 262 real films 1,204 / 1,209 | `docs/COUNTING_EVIDENCE.md`; RECORD ONLY |
| C3.6 | counting with detector boxes: render detector 30.06 % (anchor by class 44.07 %, 507 of 625 refused) | REFUTED as deployable |
| C3.7 | needle confirmation: 99.31 % of 5,385 vs 99.48 % needle-free; TS cervical 84.58 % vs 93.09 % | RECORD ONLY |
| C3.8 | search window widened 0.6 to 2.1 bodies leaves counting at 98.9 to 99.6 % (the window is not the mechanism) | RECORD ONLY |
| C3.9 | transitional confirmation (18 CTSP L6 spines x 3 seeds): clean 45 / 54 exact chains, 36 named L6 | `$RS/data/or_ready/story_rows_f3/summary.json`; RECORD ONLY |
| C3.10 | linking under physics: boxes given 99.74 % clean / 71.73 % physics; detector boxes 39.52 % / 21.50 %: detection is the binding constraint (about sixty points) where realistic physics costs eleven to twenty-eight | `docs/PHYSICS_LINKING.md`, `../08_render_devices/docs/HANDOFF_PHYSICS.md`, `results/physics/`; the finding is CURRENT, the numbers RECORD ONLY; nothing measured under `--perturb physics` before the bone-path fix is quotable |
| C3.11 | three physics defects: only the AEC extrapolation changed an image; the display window hides the lateral spine | `../08_render_devices/docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`; RECORD ONLY |
| C3.12 | guided acquisition: engine built; phantom only (geometry to 1.2 mm); corpus result of job 40376577 | `docs/GUIDED_ACQUISITION.md` STATUS; **NOT RECORDED**; nothing quotable |
| C3.13 | runtime: full-resolution link 422.6 s per pair vs 575 ms reduced; a 3-exposure sweep 12.6 s, 7 exposures 27.2 s, excluding the detector, contended CPU, synthetic exposures; the "same answer" claim withdrawn | `docs/MODEL_CARD.md` section 6.3; `~/bench/runtime_cost_workstation.json`; not in any manuscript; whether the GPU job ran: NOT RECORDED (it did not: no file exists) |
| C4.1 | render-only detector on DeepFluoro real frames, sacrum recall (6 specimens, 365 frames, conf 0.05): 76.9 % (by specimen 47.8 to 96.2 %; the seed alone moves 26 points); about 40 % before fixing 160 / 366 frames stored upside down | `memory/learned-formation-refuted-calibrate-instead.md`; RECORD ONLY |
| C4.2 | calibrate, don't learn: exact geometry + attenuation explains 80.9 %; nine terms +4.1 (v2 +4.3, `calibration_best.json`); ceiling 99.5 %; a learned refiner better on 21 % of frames only | the decision stands; numbers RECORD ONLY |
| C4.3 | DeepFluoro frames were converted wrongly (log of a log); fix `DF_CONVERSION=linear` | OPEN: a refit of the cards under the linear conversion is not confirmed in any file (OQ B9) |
| C4.5 | first real-frame LODO detector table: C-ArmLSpine held out 90.6 % vertebrae / 83.9 % sacrum at 0.25, outline | `$RS/data/or_ready/lodo/rescore_outline.json`; became `a1.json` (A6); the 1,440-cell table was a [SEL-REP] item |
| C4.6 | styled-corpus LODO: Cios held out 0.9157 to 0.9398; Elekta 0.3024 to 0.3270; Surgio 0.1429 to 0.1498 | `~/spine-detector/runs/devcorpus/*/scores.json`; SUPERSEDED by the contribution-matrix scoring; box convention not recorded |
| C4.7 | fixed-split fine-tunes (28 test cases): mixed 94.6 / 95.2 % whole; real-only 89.2 / 95.2 %; detector fine-tunes multi 97.4 / 95.9, pooled 93.1 / 100 % | `results/carmlspine_v2_lineage_2026-09-21/`; RECORD ONLY |
| C4.8 | deployment evidence: one vendor route (Siemens Cios OpenApps, K181560 / K203504; external box LessRay K180038); no published compute figure for any C-arm | `docs/CARM_DEPLOYMENT_EVIDENCE.md`; evidence document |
| C4.9 | sweep timing: a 3 to 5 exposure sweep is about 2 to 5 min, dominated by C-arm moves (36 to 49 s each); a literature synthesis, not a measurement | `docs/SWEEP_TIME_EVIDENCE.md` |
| C4.10, C4.11 | film vs fluoroscopy: devices separate pairwise, the modality boundary does not transfer; DRR-to-fluoro levers measured (fidelity, strong DR, scale); CycleGAN and ADDA refuted | `memory/film-fluoro-boundary-not-transferable.md`, `memory/drr-to-fluoro-levers.md`; CURRENT findings |

## 9. Power and sample size (E)

| id | result | status |
|---|---|---|
| E.1 | Wilson lower bound with 0 errors: 88.65 % at n 30, 92.13 at 45, 93.98 at 60, 95.42 at 80, 96.30 at 100, 97.13 at 130; one error 83.33 / 88.43 / 91.14 / 93.25 / 94.55 / 95.77; two 78.68 / 85.17 / 88.64 / 91.34 / 93.00 / 94.56; five 66.44 / 76.50 / 81.93 / 86.19 / 88.82 / 91.31 | `results/schwingnet/power_table.json#lower_bound_pct_by_k_then_n` (every cell checked against scipy); CURRENT |
| E.2 | smallest n meeting the targets: 90 % exact-level bound needs 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; 85 % variant sensitivity 22 / 34 / 45 / 74 carriers | `results/schwingnet/power/power.json#panel_a`, `#n_needed_zero_errors`; re-derived by `docs/handoff/working_notes/t2_wilson_check.py`; CURRENT (Figure 5a) |
| E.3 | error-free bounds: 64.57 % at n 7, 90.59 at 37, 93.00 at 51, 95.86 at 89 (the n 7 = 4 two-labeller + 3 single-labeller persons) | CURRENT (arithmetic) |
| E.4 | 80 % power for the 90 % bound: 99 persons at a true 97 %, 69 at 98 % (planning values; no transitional measurement behind them) | `results/schwingnet/stats_review/recompute.json` R4_wilson; CURRENT, conditional |
| E.5 | power at 51 persons, zero errors allowed: 0.07 / 0.21 / 0.36 / 0.60 at a true 95 / 97 / 98 / 99 % | `docs/handoff/literature_state/power.md` section 2; CURRENT |
| E.6 | LevelCheck comparison (paper 2): n_min 19 / 48 / 152 for p0 0.822 / 0.926 / 0.976; the 97.6 % comparator cannot be exceeded at any reachable n | FROZEN (project 02) |
| E.9 | selective prediction: certifying 99 % with zero errors takes about 298 answered cases; class-conditional 99 % needs at least 99 real calibration cases per class | CURRENT arithmetic (the measured 99 % is LEAKED) |
| E.10 | QI protocol: "powered to estimate, not to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" | CURRENT statement (project 09) |
| E.11 | device-level claims cannot be tested with 4 devices (smallest two-sided sign-flip P 0.125); the one comparison decided at its n is LODO vs pooled detection on one device (28 cases, 8 : 0) | CURRENT |
| E.13 | no power calculation exists for the synthetic:real ratio, for device-level differences, or for LODO across devices; the person-level intraclass correlation is unknown | OPEN |
| E.14 | every powered statement rests on planning accuracies of 95 to 99 % that no transitional measurement supports; no held-out transitional measurement exists; paper 1 needs 35 error-free at-risk persons, paper 2's H1 needs 19, today 7 unverified | CURRENT as a planning statement |

## 10. Latency: what is recorded (`docs/MODEL_CARD.md` section 6)

| measurement | hardware | numbers | caveat |
|---|---|---|---|
| `~/bench/latency.json`, 2026-09-13 | Tesla V100 (host voh4); CPU 1 / 4 / 8 threads | detector at 1024 px 22.9 ms median; level model batch 1 2.3 ms; head over 9 bodies 0.68 ms; CPU 8 threads detector 331 ms, level model 18.3 ms | **older models** (`films_ann`, `detect_v3`), not the reported stack |
| `MODEL_CARD.md` 6.3, 2026-09-22 | Windows workstation, 8 cores, no GPU, contended | crop 211 ms; encoder 3,350 ms (4 crops x 2 TTA); head 124 ms; link 422,633 ms per pair reduced to 575 ms; 3-exposure sweep 12.6 s reduced / 856 s; detector not measured; synthetic exposures | upper bound; the 734x reduction has no accuracy result on real frames |
| the uncontended GPU job (6.6) | a Slurm GPU job | would give the detector stage and every GPU figure | never run: no `~/bench/runtime_cost.json`, no `slurm/runtime_cost.sh` (S1) |
| `code/cine_latency.py` | one GPU type | per-stage per-frame latency on a cine, parity-gated | written 2026-09-26, never run; `$RS/data/or_ready/cine/` absent |
| the level service on the login node, 2026-09-14 | 8 old CPUs; V100 | 1.6 to 2.3 s per 2048 px film end to end, about 0.9 s fixed overhead | the service's older release |
| comparator | literature | LevelCheck registration 4.7 s per image (2012 card), 17 to 72 s per registration in theatre; surgeons would wait 20 s to one minute, more than a minute in 60.6 % (305 / 503) of helpful cases | as recorded in `MODEL_CARD.md` section 6 |

## 11. Superseded, leaked and record-only, and what replaces each

| item | status | what replaces it |
|---|---|---|
| 98.22 % lateral CV, 96.3 / 37.9 zero-shot, 72.9 % one body, 44.9 % L6 (v2 lineage; `two-mechanisms-thesis`, `lstv-tltv-detection-goal`, `carmlspine-level-experiment` numbers) | SUPERSEDED (bank deleted) | A3.1 97.4 %, A2.1 96.4 %, A2.2 43.7 %, A3.3 74.8 %; still printed in `tab3_naming.md` and `atlas/model.json` (fix) |
| 99 % at 35.7 % / 55.7 % coverage (`selective-prediction-the-honest-99`) | LEAKED (v2 bank, own test half) | no clean re-run (OQ C13); the arithmetic (E.9) stands |
| 97.47 % at 3 vertebrae, 99.02 % "shortcut-free" (`mixed-length-head-and-sota`) | LEAKED (allspine v2, NHANES II twice) | the film N-curve on held-out persons (A10.1 to A10.3, project 07) |
| 98.7 / 99.1 / 99.4 % recurrent head (`xr-benchmark-and-robustness-2026-09-13`) | RECORD ONLY [WRONG-BANK] | OQ F5 |
| 96.7 % single-crop on real films (`level-id-2d-results-2026-09-13`) | RECORD ONLY (cervical-dominated `films_ann` bank) | A9, A10 |
| the FOV feasibility report's accuracies (`feasibility-claims-measured`) | RECORD ONLY [LEAK] | the claim-by-claim reading stands |
| pretrain-on-DRR, film-noise, anchored-only, CReST refutations (`remedies-refuted-2026-09-17`) | LEAKED numbers; not re-run on v9 | RD unknown 24 |
| film N-curve "all help" reading (`film-ncurve-ablation-result`) | SUPERSEDED reading | `results/schwingnet/coverage/film_ncurve/ablation/READ.md`: 7 of 9 cells separated, six help, one hurts |
| the "100 % sacrum on DeepFluoro" | a same-device number | `docs/or_ready_audit_track_2026-09-22.json` |
| any guided-loop corpus number | NOT RECORDED | job 40376577's output, unread |
| `RSNAI_PLAN.md`, `paper/rsnai/main_v2.tex`, `paper/focused/main.tex` | superseded manuscripts | `manuscripts/schwingnet/main.tex`; kept under `manuscripts/superseded/` for their deployment and "latency unmeasured" paragraphs |
| `FLAGSHIP_PLAN.md` G6 | moved to paper 2 on 2026-09-24 | `PAPER1_SCOPE.md` |
