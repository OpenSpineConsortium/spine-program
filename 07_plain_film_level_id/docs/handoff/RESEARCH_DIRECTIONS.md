# Research directions: what the holding supports, in the order it should be done

Written 2026-10-08 for Greg, for a student he hands it to, and for a fresh Claude project. It answers one request. Give real direction for an anomaly-aware fluoroscopy classifier and for other CT research. Give direction for the idea of using paired CT and fluoroscopy to learn how 3-D features appear in 2-D. The goal of that idea is parity between 3-D single-level classification from local morphology and 2-D.

How it was written. Six reader notes and three ranked proposals were produced from files on this laptop on 2026-10-08. This document judges the three proposals, keeps the strongest programme, grafts the best of the other two, and says where they disagreed. Nothing ran on the grid. No credential file was opened. Every number carries the file it came from, using the key at the end. A number named somewhere and not found is written "not on disk". A number this document computed from numbers on disk is marked "calc". Marks: measured means this programme's own result; published means a study, quoted as the file on disk records it; planned means a target with no measurement behind it.

This folder is private. It names the private repository, the paper split and the standing decisions. Nothing here is to be copied into CTSpinoPelvic1K, OpenSpineToolkit, Student_Projects or the website.

Before a student copy is made, cut three things. Cut the sentences naming the TTO and Part B in section 4's housekeeping paragraph, section 6 rank 15 and section 8 row 15. Cut the `notes, proposals` row of the file key and section 7, which judges the three proposals. Everything else is written to be student-safe, and no sentence names the commercial goal, note 6 flag F12; decision row 9. A twelve-line glossary for a first-week reader sits after the file key; fuller definitions are in `GLOSSARY.md`.

Sibling files written the same day: `README.md`, `RESULTS_CATALOG.md`, `RECIPES.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `LITERATURE_STATE.md` and `literature_state/`. This file gives direction; those give the record.

---

## Lead

The evidence supports one order of work: measurement first, human reads second, models third. On ordinary spines the 2-D system is at ceiling on plain film and near ceiling on the one real C-arm. It names 97.4 % of bodies on a whole lateral frame and 74.8 % with one body in view, NUM:463. On transitional spines no number exists on a real frame with a human read. The one fact that constrains every project is that the verified real-frame transitional test count is zero today, NUM:435; LS Lead. The best rendered L6 recall is 56.1 to 72.4 % on ten held-out persons, ALPHA Verdict. Human readers reach 32 % sensitivity for Castellvi type on radiographs against 76 % on CT, HANH lines 130 to 131 and 27 to 28. Greg's parity idea is sound, but its 3-D target is not yet in the form the goal needs. The published 0.990 for T12 against L1 divides five of its eleven features by the patient's median over three or more levels and leaves the six between-measure ratios undivided, SEP lines 55 to 80. Its dominant feature is the transverse-process span, which is coronal, SEP rerun 2026-10-08. No lumbosacral 3-D classifier exists at all, MPDA lines 335 to 342 and 905 to 907. So the first two projects are an hour on the laptop and a day on the grid. They define the single-vertebra 3-D target, then measure which 3-D features survive projection, per view, on exact-pose renders of the 802 labelled CTs. In the same week the reader work that creates power starts. That work is a one-hour coverage render on COBRA, a reader queue of 63 volumes, the seven CTSP re-reads, the VerSe mask count and the whole-cohort Castellvi read. Models wait for a frozen truth file and a clean encoder. The first clean model is expected to fail its validation screen, and that failure is itself the result the standing determination asks to be stated plainly, LTDG.

---

## 1. What is known

Every row is one result with its number, its n, its split and its file. Numbers from a leaked bank are marked and are not quotable.

### 1.1 2-D naming on ordinary spines

| result | number | n | split and protocol | file |
|---|---|---|---|---|
| C-ArmLSpine lateral, whole frame | 97.4 %, 601 of 617, Wilson on effective n [93.2, 99.0], design effect 4.47; plain Wilson [95.8, 98.4] (calc) | 141 cases | v9 lineage, case-grouped five-fold, eval gate held out | NUM:463 |
| same, day-grouped folds | 92.1 %, 568 of 617 | 141 cases | three folds by acquisition day; the day count is five by MAN line 13723 and four by IAF line 40 | NUM:464; MAN carmlspine; IAF |
| C-ArmLSpine AP, whole frame, fine-tuned | 96.4 %, 608 of 631 | 142 cases | held out | NUM:463 |
| C-ArmLSpine zero-shot, no frame of the device in training | lateral 96.4 %, 595 of 617; AP 43.7 %, 276 of 631 | 141 and 142 | held out; AP errors are a one-level cranial shift | NUM:419 to 420; PLDA Table C |
| three bodies in field, lateral | 93.1 %, 1,079 of 1,159 | 142 | held out | NUM:463 |
| one body in field, lateral and AP | 74.8 %, 451 of 603; 67.5 %, 399 of 591 | 142 and 143 | held out, v9 lineage; the 72.9 % one-body and 98.2 % whole-frame figures in TMT and LTDG are the earlier leaked-lineage run and are superseded | NUM:463; TMT; LTDG |
| one body in field per level, lateral | L1 41.2 % of 68; L2 83.1; L3 63.5; L4 84.1; L5 86.2; AP L1 9.5 % of 63 | per level | held out; printed in no manuscript table | PLDA Table C |
| abstention at the default rule | answered 81.5 %, 503 of 617; exact on answered 98.8 % | 141 | threshold never tuned | NUM:463 |
| count from the detected sacrum alone | 97.0 %, 979 of 1,009 bodies, [94.2, 99.2] | 130 cases, conf 0.74 | no classifier | NUM:427 |
| coupled count and morphology | 98.2 %, 991 of 1,009; +1.2 pp over the count [0.0, 3.2]; 3 cases better, 0 worse, exact sign P .25 | 130 cases | the whole gain is four frames called L6 on five-lumbar spines | NUM:466; RS2 N3 |
| plain film, held-out persons, every person used | NHANES 92.7 %, BUU 96.9 %, CSXA 99.8 % | per corpus | film N-curve endpoint | FNC |
| renders only, no film | NHANES 27.2 %, BUU 10.3 %, CSXA 3.2 % | 3 seeds | the film-free floor | FNC |
| interior lumbar windows, ordinary real film | 89.9 % [87.1, 92.7] | 453 films | v6 bank; pixel-defined, no anchor in view | FCM line 104 |
| whole lumbar film with the sacrum in view | 99.96 % [99.9, 100]; the sacrum-count rule alone scores 99.96 % | 520 films | the task is saturated by counting | FCM line 107 |
| plain film random window, selection split | CSXA 99.8 %, BUU 97.3 %, NHANES 99.1 % | 727, 549, 52 patients | selection split; BUU levels are counting-inferred | T3; A5 |
| real film single crop, 14-class bank | 95.0 to 95.4 % | not recorded | the 98.7 / 99.1 / 99.4 % headline was a cervical-dominated 14-class bank | FCM line 156; RHR |
| shortcut-free real film 99.02 %; selective 99 % at 35.7 % coverage | leaked | allspine_v2 | not quotable | NDI; SPH |

An interval labelled "Wilson on effective n" carries NUMBERS.md's cluster adjustment. A plain Wilson interval is used only for an unclustered count.

### 1.2 2-D naming and detection on transitional spines

| result | number | n | split and protocol | file |
|---|---|---|---|---|
| anomalous BUU films, interior windows, no anchor | 49.9 % [41.5, 58.9] against ordinary 89.9 % | 128 films, 607 windows | v6; truth is the authors' radiograph count; the earlier 66.0 % on 12 films was noise | FCM lines 104 to 105 |
| L6 named L6 on anomalous BUU films, no anchor | 44.9 %; with a cranial anchor 81.6 % | denominator not recorded | label-defined State C; BUU plain film, not C-ArmLSpine | FCM line 141; LS 7.2 |
| rendered L6 recall, mixed head, three seeds | lambda 0: 56.1 to 61.2 %; lambda 1.0: 67.4 to 72.4 %; false-L6 rate 0.14 to 0.18 % rising to 0.38 to 0.41 %; L6 precision 56 to 58 %; real film held at 98.9 % | 10 held-out L6 persons, 98 crops | allspine_v9, held out; VerSe persons only; 0 T13 evidence persons | ALPHA Verdict |
| how an L6-spine film fails | whole run shifted one level cranial 26 to 28 %; only the L6 missed 1 %; all right 31 % | 176 films | lambda 0 | ALPHA film patterns |
| G3 development curve, comparison arm | rendered L6 51.8 to 64.2 % across training fractions; T13 named in none of three full-size runs | per fraction | validation side | NUM:490 to 492 |
| single-crop L6 on held-out render crops | 0.800 [0.653, 0.922] of 150; 116 of the 150 are physics_rare, where ordinary L4 and L5 also fall to 33 to 36 % | 150 crops | v9 validation; style confound | LEARN section 2; L6C |
| real test sacra called L6 | 0.417 of 24; sacrum 0.375 | 24 sacra | C-ArmLSpine test | LEARN section 2 |
| embedding silhouette L6 against L5 | 0.35 [0.31, 0.39] against L5 against L4 0.23; never-seen L6 persons 0.10, 0.12, 0.16; named L6 in 84 of 180 crops | 98 crops, 10 persons; 3 persons | selection split; the three are the C-ArmLSpine one-labeller reads | NUM:430, 433 |
| classifier L6 calls | 75 of 98 L6 crops named L6; 111 of 1,012 L5 crops named L6; an L6 call right 40.3 % | crops | selection split | RS2 N5 |
| the three C-ArmLSpine L6 patients | classifier 0 of 5 bodies, coupled 1 of 5; 6 frames, 4 anchored | 3 cases | agreement with one automatic labeller, not correctness | NUM:467 |
| false L6 on ordinary real frames | 3 of 233 anchored frames at 0.74 on five-lumbar frames, all flagged, 4 counting case42's call; 5 anchored frames of 4 cases at 0.25 | 145 cases | the five-lumbar qualifier is stated for the 0.74 set only; the 0.74 count is recorded two ways, 3 in RES and 4 in TAB3 | NUM:466; NUM:66; LS 7.2 |
| binary LSTV flag on renders | CTSP alone AUC 0.577 [0.480, 0.669]; with VerSe 0.725 [0.663, 0.787]; junction crop 0.656 beats lumbar film 0.509 and wide 0.543 | 34 and 110 positives | patient-level CV; pooled 0.847 is a prevalence confound | FPL |
| binary LSTV flag on real BUU films | 5 of 144 anomalies in the top 144, chance 5.8 | 3,600 films | no signal | FPL |
| T13 on 2-D | 7 persons in all sources; 0 in any 2-D validation split; 0 of 9 render crops; 0 of 16 on four spines | 7 persons | cannot be measured on any bank | TAB2; A5; LMBC |
| pretrain on renders then fine-tune against mixing | 89.1 / 40.4 against 91.8 / 66.0 ordinary / anomalous | real film | leaked v2 bank; direction only | RR17 |
| decoder-named pseudolabels | +1.5 ordinary, minus 19 anomalous | real film | refuted | RR17 |
| Star Temporal Classification | 22 to 24 % against 39.8 % with names withheld | transitional stratum | refuted on structure | STC |
| sweep chain on held-out renders | the one L6 in the held-out set was named L5 | 1 | L6 not claimable from the sweep | SWP |

### 1.3 3-D naming from local morphology

| result | number | n | split and protocol | file |
|---|---|---|---|---|
| T12 against L1 on shape ratios | AUC 0.990, 97.3 % | 1,485 vertebrae | logistic regression, five measures and six ratios, each divided by the case median; grouped five-fold | MPDA line 336 |
| the same, rerun 2026-10-08 on the laptop | AUC 0.990, accuracy 0.972 | 1,486 vertebrae, 798 cases | the one-row difference is explained by no file | SEP; note 2 section 3.2 |
| thoracic against lumbar | AUC 0.998 | 5,233 | same | SEP |
| largest standardised weights | tp_span over case median minus 1.851; tp_span over body height minus 1.184; body height over case median minus 1.012; the design note prints minus 1.89 for the first | 1,486 | three of the top five weights need the case median | SEP; AOD line 349 |
| ratio-only, single-vertebra T12 against L1 AUC, no case median | not on disk | | the first experiment of section 3 | note 2 unknown 2 |
| lumbosacral 3-D shape classifier | none attempted; 15 records per rare stratum leave three per fold | | | MPDA lines 905 to 907 |
| CT L6 identification rate from the programme's own model | not on disk; voxel results only | | | LS 7.1 row 39; NIPS |
| TotalSegmentator on lumbarisation | L6 emitted on 0 of 1,152 records; L4 Dice 0.388, L5 0.291 over 14 patients; GT-L6 voxels labelled L5 95 % and 97 % in two of three junctions; junction Dice drop 29 points [10, 47] on 7 patients | 1,152 records | | NIPS lines 186 to 191, 313 to 332 |
| own unmerged nnU-Net with an explicit L6 class | GT-L6 predicted L5 in 83, 65, 66 and 97 % of voxels by fold; L6 Dice 0.01 to 0.13 | four folds, one lumbarisation case each; the patient count is not on disk | 1,153 records; the 14-patient figure belongs to the TotalSegmentator audit | NIPS lines 900 to 925 |
| L6 under twelvefold duplication of 18 cases | pseudo-Dice 0.000 every epoch; a rule counting decoder on 4-class truth found 6 of 6 L6 and over-counted 2 of 3 sacralisations | 18 cases | distinct cases, not gradient, are the lever | L6SC |
| superior-facet-joint angle, thoracic against upper lumbar | 72 to 83 against 21 to 47 degrees | 3 spines, unrendered | a probe, not a result | MAPI section 6.3 |
| Schinz 2026, shape-based thoracolumbar labelling | 100 % against nerve morphology; counting- and rib-based rules 92.6, 96.3 and 97.2 % | 1,242 CTs; the "108 of 108" in earlier notes is back-derived from the percentages (calc) | published | TLJ row 7; MPDA lines 341 to 344 |
| VERIDAH on CT | fully correct 99.18 %; LEA recall 97.22 %; TEA 96.30 %; ablation without labelled anomalies 96.30 to 25.93 % | 365 private test scans | published preprint; L6 and T13 never predicted as classes | AUTO C2; MORPH row 1 |
| VERIDAH against the CTSP readers | L6 called on 24 where readers say 10; T13 on 52 where readers say 0 | the readers' count runs over 789 countable records; 33 are Castellvi-graded | the labeller behind every census count | SPID line 23; LS 5.2; MPDA |
| VerSe'20 learnability | 85 L6 scans in VerSe'20, about 34 % of about 253 junction-visible scans; 28 in its training split sufficed; T13 with 6 never stabilised | 85 and 28 are two counts in one report | published, as recorded | SYN lines 93 to 94; N4 line 116 |
| what the 2-D encoder tracks of the 3-D gradients | anterior height R² 0.96, process span 0.95, wedge 0.90 with crop-LOO Q² 0.78; canal depth R² 0.02; posterior height Q² 0.03 | 7 levels, 663 to 802 records per measure and level, canal depth at L2 the fewest and process span the most | with seven levels every monotone gradient is collinear with the level index | LEARN section 5; GRAD `measures.*.n_records` |

### 1.4 DRR-to-real transfer

| result | number | n | split and protocol | file |
|---|---|---|---|---|
| renders raise plain-film naming while film is scarce | +21.9, +11.1, +18.7 points at 5 persons per corpus; +12.2, +6.0, +6.2 at 25; level with every person; BUU minus 1.6 | 3 seeds | 7 of 9 pre-stated cells separated | FNC |
| render fraction 0 to 0.5 at fixed real film | anomalous 34.0 to 53.2; ordinary minus 2 | real film | superseded model line | RR17 |
| SyntheX | zero real images 6.44 mm against real-trained 6.46; CycleGAN 6.62; ADDA 6.41 | 366 frames, 6 specimens | published, voted 3-0; "DeepDRR beats naive DRR" refuted 0-3 at scale, FCX line 62; on the matched benchmark before style transfer the realistic renders beat naive, 12.62 against 16.22 mm, SYN lines 69 to 71 | PAS; FCX line 62; SYN lines 69 to 71 |
| physics explains a real DeepFluoro frame | 80.9 % of attenuation variance; nine device terms add +4.3 held out; ceiling 99.5 % | 366 frames | measured | DFF section 2; LFR |
| per-device card criterion | not met; Cios Fusion fails the BCa interval; device-level sign-flip P .125 with four devices | 4 devices, 24 folds | | CL section 3 |
| styled renders against real frames, ImageNet-feature classifier | Cios Fusion 100 %, Surgio-B51 99.8 %, Elekta XVI 99.0 % [98.1, 99.6] | 736, 666 and 771 pairs | the defensible separability statement is the per-device Bhattacharyya range 0.005 to 0.675, FFB | NUM:461; `sn:results/manifold/probes.json` |
| film against fluoroscopy as a boundary | leave-one-corpus-out 71.1 % against a 71.8 % majority share | 37 corpora | each device keeps its own region | FFB |
| accuracy against acquisition space | 82.1 % at trained angles against 52.8 % over the 16 other bins | 40 unseen subjects | more frames at the same poses fill no gap | ASS |
| render-to-fluoro translation | SDXL dead at every strength; CUT moved the films-only model 12.1 to 14.1 % and dropped the render-trained one; CycleGAN and ADDA indistinguishable from none | | refuted | FGS; DFL |
| paired real data for a spine 2-D/3-D task | Zheng 2018: 140 paired images took failure 16.07 to 11.20 % | 420 real X-rays | published, pose regression | CIT row 11 |
| synthetic prior against real count | Barr 2026: worth 2.6 to 4.3 times at 100 to 400 real, gone at 600 to 700 | cervical landmarks | published; the de novo 7.42 at both 600 and 700 is flagged | SYN section 2, lines 30 to 39 |
| synthetic to real ratio | never swept by any DRR paper; adjacent fields flatten at 4:1 to 10:1 with real at 10 to 20 % | | published, as recorded | SRE; SYN section 1, line 26 |

### 1.5 Detection

| result | number | n | split and protocol | file |
|---|---|---|---|---|
| counting exactness, boxes given against detector boxes | 99.74 % against 39.52 % on clean renders; 71.73 % against 21.50 % under physics | renders | detection costs about 60 points, physics 11 to 28 | HPH section 1 |
| render-only detector on real film | 71.67 % of bodies against 99.14 % film-trained; 1.52 duplicate boxes per body | 233 bodies on 71 frames of 25 spines, `films_drr_buucorr` | conf 0.05; 0.25 is miscalibrated; DBC carries no denominator | DBC; HPH line 203 |
| same-device C-arm plateau | 82 to 85 % from 24 frames; on the 204 of 287 complete, agreed, SPINEPS-boxed bodies recall 96.9 %; slivers carry 340 of 489 misses | 287 bodies | the plateau is the truth denominator | CPD |
| held-out device recall | 80.5 % at the cross-device point 0.74; 90.6 % at the software default; Rao 2024 in-domain 0.964 | 28 cases | | CL section 1 |
| pooled against held-out detector, same cases | +14.3 points [5.4, 23.2]; 8 cases better, 0 worse | 28 cases | | NUM:131; RS2 N9 |
| count from the sacrum on the unseen device | ordinal correct 95.4 % [89.4, 99.5] on 197 matched bodies; defined on 46 of 56 frames; strict all-sacrum-frames 65.5 % | 56 frames | conf 0.74 | COUNT |
| COBRA kV imager held out | defined on 18.2 % of frames; ordinal correct 71.1 %, 54 of 76 | | | T3 |
| two detector operating points live | 0.05 for counting on film and renders; 0.74 for the cross-device sacrum anchor | | say which | HPH; COUNT |

### 1.6 Prior art

| study | number | file |
|---|---|---|
| Kwak 2025, the only 2-D LSTV model, 3,116 lateral films at 62.3 % positive | accuracy 76.4 %, sensitivity 85.1 %, specificity 61.9 %, AUC 0.84 on 313 test films; one surgeon 83.9 %; labels text-mined from MRI reports; Grad-CAM on the T12 rib; nothing released | AUTO C1; LDL |
| Hanhivaara 2024, four readers, 100 LSTV patients | radiograph sensitivity 32 %, specificity 85 %, kappa 0.22 [0.16, 0.32]; CT 76 / 93, kappa 0.66 [0.63, 0.71]; MRI 54 / 88; the brackets are the 95 % interval of one kappa, not a spread across readers; CT specificity reads 93 at line 28 and 94 at line 130 | HANH lines 27 to 28, 130 to 131, 263 and 265 |
| Hou 2020, AP film against coronal CT | within-radiograph kappa 0.89; radiograph against CT kappa 0.50; 35.2 % of types change | PREV line 44 |
| Farshad-Amacker 2014 | AP radiograph kappa 0.53 against MRI 0.93; "standard AP radiographs are insufficient" | LDL |
| Farshad 2013, the one positive single-lateral rule | mid-vertebral angle difference of the two lowest segments at or under +10 degrees detects a bony-bridged LSTV at sensitivity 94 %, specificity 74 %; fused types only | LDL |
| Huang 2022, registration-free naming on O-arm long film | 88.3 % on 100 cadaver images from 13 cadavers | RF18 findings 0 to 3 |
| Zhang 2023, VDVM | 73.3 % naming on 31 C-arm images, identity from a prior radiograph | RF22 S1a row |
| Rao 2024 | class-agnostic recall 0.964 and 0.982 on 578 C-arm images, 20 test images | RF22 5.1 |
| Killeen 2025 | per-level Dice 0.04 on real cadaver C-arm frames | RF22 5.3 |
| LevelCheck lineage | 99.998 % is a registration metric; all 47 simulated failures a one-vertebral-height shift; no published LevelCheck failure on an LSTV | RF18 findings 5 to 8; LCC sections 1 and 3 |
| Manbachi 2018 | five surgeons on 62 hard films: median error 30.4 % unassisted to 2.4 % with the overlay | HAI findings 1 to 2 |
| Nakagawa 2017 | LSTV in 71 of 550 lumbar operations, 12.9 %; the count was wrong in 38 of 71, 54 %; the plan changed in 11 | LCC section 2 |
| HealthOST K213944 | naming agreement 91.49 % [89.91, 92.89], T1 to L4, three radiologists, no transitional term; no 510(k) names levels from 2-D fluoroscopy content | CIT row 60; RF22 5.5 |
| Cina 2021 | 98.4 % presence vector over the whole film; not metric-comparable; the task is saturated by the sacrum count here | MLS; FCM |
| 2-D TLTV detector of any kind | none published | LDL |
| any study stratifying 2-D naming by anomalous spine | none | HAI finding 8 |
| Li 2016, Li 2017, ABLSpineLevelCheck 2024 | unread; any could overturn the naming-novelty claim; Li 2017 is the one title near the parity question | RF22 5.2 and 6; RFP |

### 1.7 The confusion structure

Which vertebrae are confused in 2-D, with numbers.

| pair or class | 2-D number | bank and split | file |
|---|---|---|---|
| L1 with one body in field, real C-arm | 41.2 % lateral of 68; 9.5 % AP of 63; L4 and L5 hold 84 to 86 % | v9 lineage, case-grouped; automatic truth | PLDA Table C |
| L3 with one body in field, real C-arm | 63.5 % lateral of 137, the largest error count in the one-body table; L3 to L2 x27, L3 to L4 x20, symmetric to both neighbours; then L1 to L2 x11, L4 to L3 x11 | v9 lineage, case-grouped; automatic truth | PLDA Table C; CV9 `families/pre:cv5_det/cells/LAT/k1/confusions` |
| zero-shot AP, whole frame | 43.7 %; L4 to L3 x51, L3 to L2 x51, L5 to L4 x48, L2 to L1 x46, L1 to T12 x21; a one-level cranial shift that fine-tuning removes | same | PLDA Table C |
| whole lateral frame, case-grouped | L4 to L5 x2, L3 to L4 x2, L2 to L3 x2, plus scattered far misses | same | PLDA Table C |
| classifier against count, 1,066 counted bodies | 1,032 on the diagonal by the line's own total; the listed off-diagonal cells are one-level neighbours except L2 to L4 x1 and L3 to L5 x1, two levels off, and sacrum to L5 x6; the listed cells sum to 51 against the 34 the total implies (calc), a disagreement inside the line | C-ArmLSpine | NUM:220 |
| L6 on render crops | named L5 on 136 of 205, exact 28.3 %; T13 0 of 9, named L1 6, L2 2, T12 1 | v8 selection split with the VerSe series leak; not quotable as held out | A5, derived in note 2 section 4.2 |
| ordinary render levels | T11 78.3 %, T12 76.6 %, L1 75.9 %, L4 73.9 %, L5 74.2 %; mid-thoracic T7 55.4 %; errors to both neighbours | same | A5 |
| real film, random windows | every error is a neighbour; L1 98.3 %, L2 96.8, L3 97.3, L4 96.4, L5 98.3 | 6,824 rows, selection split | A5 |
| where the lateral head looks | share of attribution below the target against on it: L4 43 % against 32 %, L5 42 % against 24 %, L6 36 % against 24 % | v9 validation, clean lateral crops | NUM:432 |
| region occlusion on interior L3 windows | whole target body masked costs 2.3 points; end-plates only 90.4 % against 90.0 %; identity is distributed, no single ratio load-bearing | 261 windows | FCM lines 70 to 73 |
| embedding | L6 against L5 0.35; L1 against T12 0.32; L5 against L4 0.23; L2 to L5 against the level above 0.16 to 0.23 | selection split | NUM:430 |

Which vertebrae are confused in 3-D.

| pair or class | 3-D number | file |
|---|---|---|
| T12 against L1, shape classifier | separable at AUC 0.990 | MPDA line 336 |
| L5 against L6 | no 3-D shape classifier exists; "one bone under two counts"; TotalSegmentator labels GT-L6 voxels L5 at 95 and 97 %; own unmerged nnU-Net 65 to 97 % by fold | MPDA lines 905 to 907; CPA; NIPS |
| L4 against last lumbar on the merged scheme | GT-L4 predicted last_lumbar 82.7 % on the one count-style case | NIPS `tab:confusion_blocks` |
| sacralised L5 | the rule decoder over-counts 2 of 3; all 9 count-style sacralisations are Castellvi IIIb and the label-map screen ranks IIIb at median 442 of 760 | L6SC; NIPS lines 614 to 630; CSB |
| T13 | 6 read persons in VerSe, 0 in CTSP; VerSe'20 never stabilised it with 6 | POS; SYN |
| rib phenotype by length | among ribs at or under 50 mm, 152 twelfth against 10 lumbar; a short-rib rule is wrong 94 % of the time | AOD |

The reading that decides the design. By rate the two hardest 2-D pairs are the two junctions, T12 with L1 at 41.2 % and L5 with L6 and the sacrum. By count the hardest level is L3, which is not a junction: 63.5 % of 137 with one body in field, 47 errors split to both neighbours, CV9. The junctions are where the 3-D morphology changes most and where the coronal features live. The mid-lumbar confusion is symmetric and is the one Greg asked about, so L2, L3 and L4 enter the PAR-2 pilot and the parity metric in section 3. The lateral head reads the body below the target at L4 to L6, which is a counting cue, not a shape cue, NUM:432.

---

## 2. An anomaly-aware fluoroscopy classifier

### 2.1 The question

Greg's phrase is "anomaly-aware fluoroscopy classifier". The standing determination of 2026-09-23 is narrower and stronger, LTDG. Name the level correctly on a transitional spine, L6, T13, sacralised L5 and four-lumbar, from C-arm exposures, at parity with an ordinary spine. Report "not at parity" plainly if that is the result. A flag is admissible only as the pre-specified high-sensitivity stop signal F1 of the frozen protocol, LCM section 12. The R + C = 22 rule was withdrawn for localising nothing, RC22. This document reads "anomaly-aware classifier" as that determination.

Two readings of the target bound what it can mean. Castellvi type I is a coronal transverse-process height of 19 mm or more, is 68 % of all LSTV, and is unrecoverable from a lateral film by construction, PREV; LDL. The count-changing types, II to IV at 9 to 11 % of CTs, are the ones a frame-based namer must catch, LCC section 2; PREV Bands. The parity target is therefore stated against count-changing anatomy, not against "LSTV".

### 2.2 What has been tried and what it returned

| mechanism | what it returned | status | file |
|---|---|---|---|
| rule counting decoder on 4-class CT truth | 6 of 6 L6 found; 2 of 3 sacralisations over-counted | measured, CT only | L6SC |
| L6 as a voxel class, 18 cases duplicated twelvefold | Dice 0.000 every epoch | measured | L6SC |
| anchored decode with T13 and L6 columns | 39.8 % of L6 bodies called L6 on 376 held-out renders against 63.0 % single-crop; the rare-penalty sweep result is not on disk | measured | LMBC |
| rare-class render banks, physics_rare | 1,482 annotations of 81 transitional subjects; random-window naming 45.1 % on physics_rare against 93.9 % on ctsp_drr | measured | PLDA Table D |
| v6 bank, all 144 anomalous BUU films held to validation | anomalous interior 49.9 % against ordinary 89.9 % | measured | FCM |
| CReST pseudolabel admission | anchored-only 88.4 / 36.2 against 91.8 / 66.0; the CReST cell itself is not on disk | measured in part | RR17 |
| Star Temporal Classification | 22 to 24 % against 39.8 % | refuted | STC |
| alphabet coupling of count and morphology | 98.2 % against the count's 97.0 %; the gain is 3 cases, P .25, carried by L6 calls on five-lumbar frames, 3 of 233 at 0.74 or 4 counting case42; three real L6 patients 0 of 5 and 1 of 5 | measured | NUM:466 to 467; NUM:66; RS2 N3 |
| alphabet loss in the head | L6 recall 56 to 61 % at lambda 0, 67 to 72 % at lambda 1.0; false-L6 0.14 to 0.18 % to 0.38 to 0.41 %; film held | measured, trade-off | ALPHA |
| dual-loss arm D1 and flag F1 | pre-specified; development curve only; the stop signal fired on 4 of 5 erring ordinary frames and 17 of 225 correct ones | planned | LCM section 12; NUM:221 |
| binary LSTV and TLTV whole-frame flag | renders CTSP 0.577, with VerSe 0.725; junction crop 0.656; real BUU films no signal | measured | FPL |
| selective prediction, conformal sets | 99 % at 35.7 % coverage on renders | leaked v2 bank; re-run needed | SPH |
| sweep from the sacrum with chain naming | 120 held-out CTSP renders 72.1 to 95.2 %; the one held-out L6 named L5 | measured, L6 not claimable | SWP |
| render-to-fluoro translation, SDXL, CUT, CycleGAN, ADDA | no gain in any arm | refuted | FGS; DFL |
| size in millimetres as a scalar feature | no gain, three times | refuted | LID13 |

The pattern is short. Every mechanism that reads morphology alone has been measured below the ordinary-spine accuracy on an extra body. Every mechanism that counts has been measured only on ordinary spines or on renders. The two have never been coupled on a real transitional frame with a verified read.

### 2.3 The design the evidence supports

Task definition. Per-vertebra naming from detected boxes in a limited field, with the count from the detected sacrum as the second mechanism and disagreement as the stop signal, TMT. The 27-level posterior stays as the cheap first answer. The endpoint is exact level on a transitional spine, person-clustered, with the strict all-sacrum-frames denominator printed beside any anchored number, COUNT.

Classes. The 27-level alphabet with the variant alphabets, ordinary, L6, T13, both, and the extended four-lumbar alphabet, scored by the classifier's posteriors over the count's ordinals, ACP. T13 on a lumbar frame is a count from the thoracolumbar junction, not a morphology, and the manuscript says so; seven T13 persons exist in all sources and none in any 2-D validation split, TAB2.

The counting decoder against the morphology head. On ordinary real frames the count alone names 97.0 % of anchored bodies and the coupling adds 1.2 points through false L6 calls that repaired miscounts, NUM:466. On rendered L6 spines the dominant morphology failure is a whole-run shift one level cranial, 26 to 28 % of films, which is exactly the error a count catches, ALPHA film patterns. The design therefore keeps both and measures their agreement on anomalous spines, which has never been done, TMT "What must be measured".

Selective prediction. Report accuracy among answered and the coverage together; re-run the curve on a clean bank because the measured one is on leaked v2, SPH. Abstention coverage is printed beside every headline, RAF.

Banks. The G3 person-disjoint split, applied 2026-09-23 with a leak audit PASS, ordinary 80/10/10 and transitional 50/10/40, every real transitional subject in test, SPLT; FP "The split". Encoder from ImageNet weights on G3 training persons only, because 92 of 97 transitional validation and test persons sit in the v8 and v9 training splits, TAB2 note d; NUM:69. Renders stay in training as the only labelled L6 and T13, FNC. Variants in 25 to 35 % of rendered CTs by which CTs are rendered, never by duplication, SYN section 6; L6SC. No decoder-named pseudolabels, RR17. FluoroCap in no training list, DD23. Every bank built through `tools/patient_keys.py`, and every quoted number passes `tools/eval_gate.py` with held out true, ACC section 5.3.

Training schedule. Mixed training with renders of every level in every batch is the default. The programme's own arm found pretrain-then-fine-tune lost 25.6 anomalous points, RR17. The verified mixing run says the real frames cover only T11 to S1, SRM. The two-stage recipe of the ratio report is an arm to run and report, not the default; two verified runs recommend opposite schedules and neither is clean, SYN section 6; note 6 flag F6.

The synthetic to real window. No DRR paper swept the ratio; adjacent fields flatten at 4:1 to 10:1 with real at 10 to 20 % of the mix, SRE. The 45-cell array is the experiment nobody has published, PLDA "What is not known", Ratio sweep row, line 251. Its cells are real share in 0.1, 0.25, 0.5, 0.75 and 0.9 at N 25 and N all, three seeds, L6 scored separately. PLDA Table A is the ratio actually trained, about 1 to 1 by rows. The array runs after the clean encoder exists.

Device handling. Each C-arm is its own low-dimensional domain; real-frame detectors on one device collapse to 1 to 2 % on others, KDN. Pooled is never quoted without the device-held-out arm beside it, BP "The rule that makes it fair". Devices with real frames: Surgio-B51, Cios Fusion, Elekta XVI, BV Pulsera never trained, PIXIUM one specimen, note 4 section 3.1. The device cards' every-device criterion was not met and six devices are needed for any two-sided P at or under 0.05, CL section 3; N4 row 1. Score a detector on a device held out whole, never on a held-out "domain", FFB.

### 2.4 The data

Section 5 holds the canonical counts for every source. This table keeps the columns that bear on the fluoroscopy classifier and uses section 5's numbers.

| source | persons | frames | transitional content | truth quality | restrictions | leakage state | file |
|---|---|---|---|---|---|---|---|
| C-ArmLSpine, FIRST Surgio-B51 | at most 149, living or cadaver not stated, PatientID empty on 59,307 of 59,609 files; five acquisition days by MAN line 13723, four by IAF line 40, three day-grouped folds by NUM:464 | 299 spot frames, AP 149, LAT 149, OBL 1; 602 sweep projections from 2 cases; 149 CBCTs, 137 with the sacrum | 3 L6 by one automatic labeller, case42, case121, case136; no T13; lumbar-only CBCT so no count | two automatic labellers agree on 814 of 910 vertebrae; T12 named on 10 %, T11 on 0 %; poses by edge registration, median NCC 0.37 AP and 0.21 LAT; no human read | CC BY 4.0; case134 headers carry a real name, never print; PixelSpacing 1.0 is a placeholder, true pitch 0.150 mm | zero-shot v9 numbers clean; the older `carm_cv*_drr` fine-tunes descend from the leaked v7 bank, and the 97.4 % in 1.1 is the gated v9-lineage rerun, NUM:463; the three L6 are test only | MAN carmlspine; CLE; CPD |
| COBRA2026, Elekta XVI and Varian kV imagers | 692 public cases of 867, living radiotherapy patients | 375,618 projections; 3,480 Elekta frames exported from 145 cases; Varian 225 never exported | planning-CT screen 91 calls, L6 38, T13 45, four-lumbar 8; 57 their own field supports; 7 with an exported frame and a two-labeller count; one labeller, not a radiologist read | automatic only; RTK geometry exact; T12 in 0 projected boxes, L1 in 10; whether L5 and the sacral ala are in the field is unverified | CC BY-NC 4.0; validation and test 175 cases embargoed to 2032-03-01; laterals photon-starved | all calls on the test side; 5,013 duplicate frames sat in one detector arm | MAN cobra2026; TAB2 note e; LS 7.1 row 15 |
| DeepFluoro, Siemens Cios Fusion | 6 cadaver pelves | 366 frames with exact pose; vendor deposit 2,659 frames, 2,293 without a pose | none; 2 to 3 lumbar levels in field | exact pose, 0.00 px reprojection; vertebrae ONE merged class, no spinal landmark | CC BY-NC or BY-NC-SA, quoted both ways; three copies key as one | detector training and device card; not in the level bank | MAN deepfluoro_h5; DFC |
| BUU-LSPINE | 3,600 cases, 3,598 by content | 7,200 films, 3,600 lateral and 3,600 AP | L4L6 sheet 129 four-lumbar, 15 six-lumbar; 144 by the flag table; 9 of 15 L6 reads are children aged 7 to 17 | levels counting-inferred by row order; radiograph-only truth read at 32 % sensitivity | "No License Provided" plus EULA; never redistribute; owner-only; a standing note says keep it out of flag training | 3,603 laterals sit in allspine_v8 and v9; the AP films are in no bank | MAN buu_lspine_3600; FCM; LDL |
| CSXA | 4,963 individuals, one image each assumed | 4,963 lateral cervical | none | expert corner keypoints C2 to C7 | CC BY 4.0 | all in v9 lineage | MAN csxa; XDU |
| NHANES II | 364 persons landmarked; 17,073 films on disk | 543 annotated; 16,531 unannotated in no trained bank | none read; the detector boxes the sacrum on 72 of 7,394 lumbar films, 1.8 %, AMS lines 33 to 34; LS line 886 records two region splits, 7,408 and 7,394 | expert landmarks on 543; the rest pseudo | public domain; landmarks CC BY 4.0 | 543 in v9; entered v2, v6, v7 twice under two names, 48 of 54 validation persons leaked | MAN nhanes2; AMS; NDI |
| VinDr-SpineXR | 5,000 studies, no PatientID | 10,466 images | a tier-B pseudo-flag count on frames without the junction was quoted as 209 in the notes; 209 is not on disk | lesion boxes only; pseudo levels | PhysioNet DUA; no WSU IRB determination covers it | 0 in v9; `vindrps` keyed per image with a 77.8 % validation leak; the release test split was consumed | MAN vindr; IAF |
| render banks: ctsp_drr 802; physics_drr 7,045 annotations, CTSP 2,430 from 798 people, TotalSegmentator 1,831, VerSe 1,463, implant 1,321, the 3,029-subject figure marked wrong on the card; physics_rare 1,482; verse_drr 387; ts_drr 2,905; xrsp1k 6,416 | the labelled CTs | per bank | physics_rare is the only labelled L6 and T13 at scale: 34 CTSP and 47 VerSe series; T13 2 of 6 scans missing | CT labels projected; exact pose by construction | CTSP renders CC BY-NC-SA | ctsp_drr, verse_drr, physics_drr, physics_rare are inside v9; TS bench inside v9 except 70 renders | MAN render cards, physics_drr lines 2577 and 2594; TSB |
| Geneva, Ljubljana, SpineSAC | 1 phantom; 1 cadaver L1 to L5; 3 sawbone phantoms | 116; 18; 286 raw | none | gold poses; gold poses per vertebra; no bone truth | BY-SA or BY-NC; BY-NC-ND; none stated | all test or unused | MAN cards |

### 2.5 Evaluation, the pre-stated gates and today's n

| gate | pre-stated value | today's n | power today | file |
|---|---|---|---|---|
| exact level on transitional real frames, Wilson lower bound at or above 90 % | 35 persons with no error; 53 at one; 69 at two; 113 at five | 0 verified; 7 unverified with a frame; best case at 7 is a 64.6 % bound | 0 | PJ; NUM:435 |
| variant sensitivity lower bound at or above 85 % | 22 carriers with no miss | 0 verified real carriers; 43 G3 test L6 persons by the split, of whom about 29 carry an L6 mask a render can score, SPLT line 35; 49 of 54 validation and test L6 are inside the current encoder's training | at a true recall of 72.4 % the probability of 22 of 22 is 0.0008; the bound is reached at no n | PJ; TAB2 note d; N4 row 8 |
| the 85 % bound on the G3 test L6 persons | on 43 persons at most 1 miss: 42 of 43 gives a Wilson lower bound of 87.9 %, 41 of 43 gives 84.5 %; on the about 29 render-scoreable persons zero misses: 29 of 29 gives 88.3 %, 28 of 29 gives 82.8 % | the clean encoder does not exist yet; the 14 audit-only test persons carry a read and no L6 mask until PLAN decision 3 segments them | at a true 72 % the probability of 42 of 43, or of 29 of 29, is near zero | calc, correcting the "at most 2 misses" in note 1 and proposal A; SPLT line 35; PLAN section 1a |
| paper 2 H1, superiority over 82.2 % | 19 at-risk real-frame persons with no error | 7 unverified | ineligible | LCM section 5 |
| paper 2 H2, superiority over 97.6 % | 152 with no error; power 0.22 at 152 if truly 99 %; 80 % power first at 708 | 0 | unreachable at any n in reach | LCM sections 5 and 7; N4 row 12 |
| paper 2 H6, ordinary non-inferiority at 92.6 % | 48 | at most 51 ordinary real-frame persons, 13 with a reference | 0.07 to 0.60 | LS section 4 row 14 |
| T13 | 22 carriers, about 55 T13 people in total under 50/10/40 | 7 persons in all sources, 3 CT test, 0 real; 44 to 138 expected in the whole holding, LS line 676; 38 to 119 over the 18 screened acquisition collections, N4 line 137 | 0 | LS section 5.2; N4 section 4 |
| the planning accuracies behind every power table | 95 to 99 % | the measured transitional figures are 49.9 % on films, 44.9 % L6 without an anchor, 56 to 72 % on renders | every transitional test is at or near zero power | RS2 N1; LS section 4 |

The anomalous-against-ordinary film difference is the one powered transitional statement available. It is 49.9 % on 128 films against 89.9 % on 453, and it needs 74 per arm at a design effect of 4. It holds with the truth tier stated as a radiograph count under an EULA, LS section 4 row 6.

### 2.6 The published method and number it is measured against

Kwak 2025 is the only 2-D LSTV model: accuracy 76.4 %, sensitivity 85.1 %, specificity 61.9 %, AUC 0.84 on 313 films at a 62.3 % positive rate, AUTO C1. Never benchmark against it on a balanced set; its positive rate is a surgical-cohort artefact and its labels are text-mined, LDL. Hanhivaara 2024 is the human ceiling for any single-view type inference: sensitivity 32 %, kappa 0.22 [0.16, 0.32] on radiographs against 76 % and 0.66 [0.63, 0.71] on CT, HANH lines 130 to 131, 263 and 265. Manbachi 2018 is the human naming number on hard intraoperative films: 69.6 % unassisted, 97.6 % assisted, HAI. Farshad 2013 is the one lateral rule, sensitivity 94 %, specificity 74 %, fused types only, LDL. A single-lateral flag that beats all three on an unenriched set has found something or has leaked.

### 2.7 The first experiment

Two things in the same week, neither a model.

First, the truth. A one-hour job projects the Dataset803 sacrum and L5 label of ten COBRA planning CTs through their RTK geometry onto their own Elekta projections and renders the result. The render answers by eye whether COBRA is spine data for the sacrum anchor, LS 7.1 row 15; CLAUDE "Render the mask". Then the reading protocol is frozen, PRER. The queue is 63 volumes: the 57 COBRA calls their own field supports, 11 L6, 38 T13 and 8 four-lumbar, the 3 COBRA re-read candidates and the 3 C-ArmLSpine CBCTs, TAB2 note e. The 34 unsupported calls, 27 L6 that see no L1 and 7 T13 over an ordinary thoracolumbar count, are read only if `ct_original` shows more field than `ct_def`. The queue goes through the two-stage review tree, read on the CT and not the frame, with the two-labeller disagreement list as the triage order and the truth tier recorded per person, REVT. A carrier confirmed on the planning CT is a real-frame test person only if its frame is exported. Today 145 of 692 cases have Elekta frames, the 225 Varian cases have none, and 7 of the 91 calls have a frame, NUM:435; MAN cobra2026. So the yield is recorded in two columns, confirmed on CT and scorable on a real frame.

Second, the clean encoder. Train the ResNet-18 two-channel encoder from ImageNet on G3 training persons only, renders and real films mixed in every batch, no pseudolabels, three seeds, heads at lambda 0 and lambda 1.0. Score the 11 G3 validation L6 persons on renders. Only 7 of them carry an L6 mask a render can score, SPLT line 35. The 4 audit-only persons carry a read and no mask id. Either PLAN decision 3 segments them first or the screen is stated at n 7. Score the single T13 person, the false-L6 rate on ordinary validation persons and the film pattern table beside it, each with the person-clustered interval. FLU-2 is an evaluation arm under G5's evaluation-arms clause, FP line 62. It closes no gate and is not the flagship training, which waits on G0 to G3, decision row 5. Its first grid step follows decision row 22: submit, estimate the wall time, write the job ids and ETA to the resume file, stop. Do not score the test side until paper 2's ledger carries an "H1 seen" entry, because paper 1 scores no G3 test transitional person, PS24; P1S. Then run `tools/alphabet_couple.py` on the same anomalous frames and tabulate how often the count catches the whole-run shift and how often the stop signal fires, TMT.

### 2.8 The stop rule

The validation screen is stated in misses per render-scoreable person. Zero or one miss of the 7 proceeds to three seeds and two heads. Two or more misses stops the fluoroscopy arm, and the manuscript says "not at parity" with the number, LTDG. This is a screen, not a bound. At a true recall of 72.4 % it passes 38 % of the time, and at a true 85 % it passes 72 % of the time, calc, exact binomial on 6 or more of 7. The same rule on 11 persons, 10 or more of 11, passes 15 % at 72.4 % and 49 % at 85 %, and its Wilson lower bound is 62.3 %, calc. Crop-level recall is scored beside it with the person-clustered paired interval, exactly as ALPHA does on 98 crops of 10 persons. That interval is about plus or minus 17 points, ALPHA line 75. The band and the screen then share a unit. The 22-carrier bound cannot be reached from COBRA alone, section 2.9. If the read confirms fewer than 22 carriers with an exported frame, the manuscript states that no fluoroscopy transitional sensitivity can be claimed and reports the render number only; DAT-1 is the only route to 22. If the count catches fewer than 80 % of the run-shifted L6 films, or the stop signal fires on fewer than half of the erring L6 films, the design is not anomaly-aware and must not be described as such.

### 2.9 What is missing and the exact step

| missing | the step | file |
|---|---|---|
| verified real-frame transitional persons, 0 of 22 or 35 | the 63-volume reader queue above. Expected yield at the labeller's PPV: the 11 field-supported L6 calls at 10 of 24 give about 5 (calc, 4.6); four-lumbar at most 8; T13 near zero at 0 of 52; about 13 verifiable on CT, at most 19 if every supported call confirms. 22 cannot be reached from COBRA alone; P(all 11 supported L6 confirm) is (10 of 24) to the 11th, 0.00007 (calc). Two PPV readings are on disk, CTSP 10 of 24, TAB2 note e, and VerSe 34 of 42, RS2 S4 line 361; N4 row 11 gives 0.30 at the upper Wilson limits; this document uses 10 of 24. Of the confirmed, only cases with an exported frame are real-frame persons, 7 of 91 calls today, NUM:435 | TAB2 note e; N4 row 11; RS2 S4; NUM:435 |
| real paired sets outside the holding | send the drafted letters this week, SX-Stitch, Balgrist, the fourteen cine letters, none recorded as sent; draft the two largest, LevelCheck's 178 patients with 398 intraoperative radiographs and Huashan's 140 with CT and intraoperative AP and lateral films; fetch the two free items, TCIA CMB XA frames and the NIT Warangal centroid files | LS section 2 rows A1, A3, A6, A10; MAN request cards |
| the BUU licence reading | Greg decides whether BUU-derived weights may leave; 3,603 BUU laterals sit in v9 under "No License Provided" plus an EULA | LDL; XDU; note 1 flag 4 |
| the whole-cohort Castellvi read on CT | section 4, project CT-3; it is the largest increase in read positives on data already held | MPDA lines 919 to 921; N4 section 4 |
| a two-labeller verification of every census flag before any is a label | the review tree; a segmenter call is never promoted without a read | POS header; TIERS |
| the open "use all" items before the final bank | 16,531 unannotated NHANES films into detector self-training; the 3,600 BUU AP films into a bank or a written exclusion; all 10,466 VinDr images under a determination; the COBRA Varian export; FluoroCap as a 200-panel annotated test set or written off | DD23; MAN section 4 rows 25, 30, 31 |
| a chest-CT route to T13 | the CT-RATE gate form, the INSPECT DUA and NLST beyond the pilot; expected T13 95, 86 and 109 at the low prior, LS B5, B6 and B3; Merlin is abdominal CT with an expected T13 of 2.1 and stays in the LSTV route, LS B1; two labellers blind to each other because the NLST pilot's 9.3 % fell to 1.5 % once a rib on the body was required | LS section 2 B rows; N2 section 8a; ACQ section 11 |

---

## 3. 3-D to 2-D parity on the paired sets

### 3.1 Greg's idea, stated precisely

The idea is to use paired CT and fluoroscopy to see how the 3-D features that name a vertebra are represented in a 2-D projection. The features could then be engineered into the 2-D model where it confuses levels. The goal is parity between 3-D single-level classification from local morphology and 2-D classification.

Three facts in the record bend that statement before it can be measured.

1. The 3-D number is a within-patient number. The 0.990 uses five measures each divided by the case's own median across its measured levels, plus six between-measure ratios, SEP lines 36 to 40 and 50 to 87; MPDA lines 335 to 342. A vertebra alone in a field has no case median. The six ratios are size-free on their own and would be the single-vertebra feature set. Their AUC without the case median is not on disk.
2. The 3-D discrimination at the thoracolumbar junction is coronal. Transverse-process span carries three of the top five standardised weights, minus 1.851 for `tp_span/case_median` on the 2026-10-08 rerun, SEP; note 2 section 3.2. On a lateral the process is superimposed on the body and the span cannot be read. Every 2-D naming number in the programme was built on lateral frames or lateral renders, MDD docstring "WHY LATERAL", and AP naming is 43.7 % zero-shot, NUM:420.
3. At the lumbosacral junction the 3-D target is undefined without the count. The article attempts no shape classifier there, MPDA lines 905 to 907. L5 and L6 are "one bone under two counts", CPA. No CT L6 identification rate from the programme's own model exists, LS 7.1 row 39.

So the parity question splits. At the thoracolumbar junction parity is measurable now and the obstacle is the view. At the lumbosacral junction parity needs a 3-D number first, and that number may not exist from local shape; the record routes the extra body to the count from the sacral anchor, TMT. The fused L5 is a third case where the pelvis carries the signal, sacral slope AUC 0.73, FCM line 36.

Only one real paired set carries level truth on a living spine, C-ArmLSpine, and its truth is automatic with the thoracolumbar junction removed. DeepFluoro has exact pose and one merged vertebra class. COBRA's spine coverage is unverified. Ljubljana is one specimen, note 4 flag 1. The exact pairs with full level truth are the programme's own renders of its labelled CTs. That is where the question is asked first, with the real sets as the check.

### 3.2 The 3-D feature inventory that names a level

Visibility columns are this document's reading of projection geometry and the published rows cited; they are hypotheses the visibility experiment measures, not results. Columns and files are given per feature.

| feature | what it is and how ostk or the release measures it | 3-D discriminating power | lateral | AP | oblique arc | 2-D analogue and published reliability | defect carried into 2-D |
|---|---|---|---|---|---|---|---|
| transverse-process span | bounding span; `tp_span_<L>_mm` in LG | T12 against L1, weight minus 1.851, the dominant feature | not readable, superimposed on the body | readable, the tips flank the body | readable from about 30 degrees off lateral, hypothesis | process tip to tip on the AP; reliability not on disk | 169 TP heights overstated by more than 5 mm by speckle before correction (CSB) |
| transverse-process height, lowest lumbar | craniocaudal extent of the largest component in a 12 mm slab at the tip; `tp_height.csv` | Castellvi I at 19 mm; the IIb and IIIa screen | not readable | readable, the Castellvi definition | partly | radiograph kappa 0.22 [0.16, 0.32] against CT 0.66 [0.63, 0.71], the brackets a 95 % interval (HANH lines 263 and 265) | the screen keys on an unfused process; IIIb rank 442 of 760 (CSB) |
| process to ilium gap | `tp_gap_*` in TM | Castellvi II and III | not readable | readable where ala and process overlap | partly | Ferguson view named only in an unverified sweep | three sacrum-side cues at chance, AUC 0.450, 0.415, 0.551 (CSB) |
| anterior body height | tallest column over a slab; `body_height_<L>_mm` in LG; ostk VBHa | monotone T11 to L5; weight minus 1.012 | readable, both plates in profile | partly, plates superimposed with tilt | readable | semi-automated lateral morphometry ICC above 0.95, unverified web | cohort sits about 6 mm above Panjabi; it is the cohort (BHI) |
| posterior body height | `body_height_post_<L>_mm`; ostk VBHp | a plateau 26.4 to 30.4 mm; the encoder ignores it, Q² 0.03 | readable | poorly | readable | as anterior height | ostk 1b7005c inflates VBHp 10 to 17 mm on about 1 in 7; use the release column (OCR) |
| wedge ratio | anterior over posterior height; `wedge_ratio_<L>` | monotone; crop-LOO Q² 0.78, the best interpolated | readable | partly | readable | Farshad 2013 is a wedge-type lateral rule, sensitivity 94 %, specificity 74 % | none recorded |
| end-plate width | body isolated by a cut at the anterior canal wall; `endplate_width_<L>_mm` T11 to L4; ostk EPWu, EPWl | rises caudally; weight minus 0.643 | not readable, the lateral shows depth | readable | partly | not on disk | L5 withheld: 95 of 760 over 60 mm, SD 1.58 times the widest published (LM section 2) |
| end-plate depth | corner chord; ostk EPDu, EPDl | not measured as a separator | readable | not readable | partly | not on disk; no published SD on file (MAPI section 2) | ostk 1b7005c inflates EPD; withheld until fixed |
| canal width, interpedicular | `canal_width_<L>_mm`; ostk SCW | rises caudally; weight minus 0.768 | not readable | readable between the pedicle ovals | partly | AP film is the standard projection; agreement against CT not on disk | within 0.2 to 2.9 mm of Panjabi (OVE) |
| canal depth, midsagittal | pedicle-slab midsagittal chord; `canal_ap_mm_<L>` in SM; ostk SCD | flat 16.6 to 17.8 mm; the encoder ignores it, R² 0.02 | partly, pedicle to posterior wall | not readable | poorly | not on disk | rewritten; records under 11 mm went 473 to 12 (LM section 1) |
| pedicle width | widest slice in the front third of the canal; `pedicle_mm_<L>` in SM; ostk PDW | widens into the lower lumbar, Zindrick 1987 | not readable as width | readable as the pedicle oval | partly | cervical radiograph against CT r² 0.665, unverified web; Zindrick by level, published | L5 20.70 against a published 16.20; ostk reads 15.10 but has not survived a full run (SPE "Pedicle width") |
| rib presence, 12th rib length, 12 to 11 ratio, lumbar rib | principal axis; `rib12_*`, `lumbar_rib_len_mm` in TM | thoracolumbar junction; Kwak's attention sits here | partly, rib heads overlap the body | readable, the rib shadow | readable | no published 2-D stump-rib detector; Möller CT F1 0.84 from the first 22 mm | ribs at or under 50 mm: 152 twelfth against 10 lumbar (AOD) |
| superior facet joint angle | plane fit to the apposed voxels, SPINEPS ids 45/46 against 47/48; MAPI section 6.2 F1 | thoracic 72 to 83 against upper lumbar 21 to 47 degrees on three spines, unrendered | not readable as an angle | partly, the facet ovals | readable near 45 degrees, hypothesis | Schinz 2026 criterion I, CT only | not built; n 3 |
| process position relative to the facet | centroid offsets; MAPI F2 | Schinz criterion II | not readable | partly | partly | not on disk | not built |
| costal fovea proxy | HU pit at the pedicle-body junction; MAPI F4 | Schinz criterion III | not readable | not readable | not readable | not on disk | not built; lowest priority |
| S1 superior plate angle, sacral slope | plate fitted to the whole sacrum under the lowest lumbar footprint; `sacral_slope_deg` in SM; `ostk.metrics2d` | the lumbosacral junction; v11 only | readable, the landmark SS is measured from | not readable | poorly | the 2-D port reproduces the 3-D angles on identical geometry (OM2) | id 29 retired; everything sacral recomputed from v11 (CLAUDE) |
| bony fusion L5 to ala, Castellvi III | ala rise per side; CSB "Closing the blind spot" | count-changing; 9 of 9 count-style sacralisations are IIIb | partly, Farshad 2013 | readable, the fused ala | partly | Farshad 2013, fused types only | a 12-case direction, not a validation |
| iliac crest level against L4 and L5 | `crest_above_l45_mm`, `crest_blocks_l45` in SM | the last lumbar vertebra | readable | readable | readable | iliac-crest tangent sign on MRI, sensitivity 81 % (PREV) | none recorded |
| sacral foramina count, sacrum width and height | sliding slab; `foramina_*` in TM | six-segment sacrum | not readable | readable | partly | not on disk | foramina counting failed at all 81 settings (LJ lines 110 to 120) |
| iliolumbar ligament origin | none | last lumbar in 95 % of controls | not readable | not readable | not readable | needs axial imaging (LDL) | not measurable in 2-D; dropped |

Rules binding every reader of these columns. Names through `ostk.labels.labels_for(volume)`, never a fixed map. Identifier 29 is retired and anything sacral is recomputed from v11, while `level_gradients.csv` is bit-for-bit identical across v10 and v11, SPE. `zfill(4)` before any join. The token is not the record id; token 149 is record 0208, CSB "A correction", line 75. `ostk/labels.py` line 64 still maps `"S1": 29` in `LABELS_V10`, verified today. A sacral quantity asked for by name can therefore reach an id no voxel carries and return a plausible zero, note 6 flag F2. Reader E's 3-D feature table at scale exists on the grid and was not read: 38,432 instance rows over 3,524 CT and mask pairs, `features_j1.csv`, MAPI lines 128 to 130. Its J2 spread gate passed canal depth and failed lower end-plate width, MAPI line 130.

### 3.3 The paired data

Section 5.3 holds the canonical pairing counts; this table adds the truth tier, the labels and the restrictions.

| set | pairing | truth on the 2-D side | persons | frames | labels | restrictions | file |
|---|---|---|---|---|---|---|---|
| C-ArmLSpine | one CBCT per case with same-session AP and lateral spot frames | automatic, two labellers agree on 814 of 910; T12 named 10 %, T11 0 %; poses by edge registration | at most 149, not provably persons | 299; 148 and 296 in every published number, the pre-repair count, MAN lines 13833 and 13905 | TotalSegmentator and SPINEPS plus VERIDAH where they agree; three one-labeller L6 | CC BY 4.0; day-grouped folds; verify pose by detector boxes, never by the registration score | MAN carmlspine; CLE; IAF |
| DeepFluoro | cadaver CT with real frames at exact pose | none per vertebra; one merged class spanning 90 to 112 mm; 14 pelvic landmarks | 6 pelves | 366 | 7-class 3-D segmentation; per-level truth needs a segmenter run on the six CTs | NC either way; 160 of 366 stored upside down | DFC; MAN deepfluoro_h5 |
| COBRA2026 | planning CT deformably registered to the CBCT, with the raw kV sweep | none; RTK geometry exact; L5 and ala coverage unverified | 692 public | 375,618 projections; 145 cases exported | masks on `ct_def`, not `ct_original`; two-labeller boxes on 150 Elekta exports | CC BY-NC; 175 cases embargoed to 2032; Elekta solved, Varian not | MAN cobra2026; PRER section 0 |
| Ljubljana 2D-3D-GS | one cadaveric L1 to L5 with CT, MR and 18 turntable radiographs | gold per vertebra, fiducial TRE about 0.2 mm | 1 | 18 | five named bodies; HU slope unknown | CC BY-NC-ND or a signed agreement; ND forbids derivatives | MAN ljubljana |
| Geneva | one resin phantom with fluoroscopic frames | gold transforms; whether it holds a lumbar column is unverified | 1 | 116 over 19 views | none for vertebrae | BY-SA or BY-NC, quoted both ways; the only never-trained device | MAN geneva_hip |
| SpineSAC | three sawbone phantom CTs with C-arm AP and lateral pairs | projection matrices; no bone truth | 3 phantoms | 286 raw, 118 processed | none; TotalSegmentator returned empty masks | no licence stated | MAN spinesac |
| the programme's renders | the labelled CTs projected at known poses | the CT label projected; exact by construction | CTSP 802, VerSe 374, TS 1,170 and 1,735, 81 transitional series in physics_rare | ctsp_drr 802; physics_drr 7,045; physics_rare 1,482; xrsp1k 6,416 lateral with end-plate corners; devcorpus arc 4,551 files | boxes only, except the XRSpinoPelvic1K corners; no bank projects pedicle, canal, process, rib facet or S1 plate | CTSP renders CC BY-NC-SA; xrsp1k sits on dangling symlinks to a deleted export and must be rebuilt from v11 | MAN render cards; MDD lines 195 to 225 |
| not held, by living subjects with truth on real frames | LevelCheck 178 patients with 398 radiographs; Huashan 140; VerSeg-Net 50; Charters 527; Petragallo 429; Jaganathan 55 CBCT sweeps; SJTU 64 biplanar; SX-Stitch 1,032 frames; TCIA CMB XA 16 free; NIT Warangal 9 free | | | | | no request recorded as sent | LS section 2 |

What no bank projects today: pedicle width, canal width or depth, transverse-process span or height, rib facets, or the S1 plate as a 2-D landmark, MDD `project_labels`; RPD docstring. That gap is the first thing the visibility experiment closes.

### 3.4 The visibility experiment

The experiment runs in three stages. Stage 1 is an hour on the laptop. Stage 2 is a day on the grid. Stage 3 is the real paired check and waits on a pose verdict.

**Stage 1. The single-vertebra 3-D target.** Copy `test_morphometric_separability.py` to a variant that drops the five case-median features and keeps the six between-measure ratios. Run T12 against L1 on `level_gradients.csv`, grouped five-fold by case, seed 0, exactly as the original does. Then fit the seven-level shape model T11 to L5 on the 643 ordinary records of `six_lumbar_readings.py`, ratio-only. The report prints 643 and the script's docstring says 644, `ctsp:results/six_lumbar_readings/report.txt` line 1 against `ctsp:scripts/six_lumbar_readings.py` line 16; this document uses the report's 643. Apply the model to every body of the 18 six-lumbar spines and tabulate the name each body receives. Then L6 against ordinary L5 on the ostk rows at commit 90a27a7. The six SEP ratios cannot be formed there. `ostk_level_morphometry.csv` carries VBHa, VBHp, EPWu, EPWl, EPDu, EPDl, SCW, SCD and PDW and no process span; `level_gradients.csv` and `transition_morphometrics.csv` have no L6 columns; widths at L5 and L6 are excluded by rule, LM section 2. The reduced feature set is VBHa/VBHp, SCW/VBHa, SCD/VBHa and PDW/VBHa, all from the ostk CSV. The ostk L6 rows are 0005, 0033, 0208, 0234, 0244, 0268, 0302, 0366, 0376, 0486, 0831, 0950, 0960 and 0999. Record 0033 is one of the seven disputed records, so 13 positives remain against 757 L5 rows, not about 780. Score leave-one-case-out, with the 1,000-permutation p-value on the cross-validated AUC and a case-grouped bootstrap; a fit on 13 positives scored in-sample is optimistic. A process span for L6 is not on disk and needs the extraction script run on the 18 L6 records first. The seven disputed CTSP records, 0008, 0021, 0033, 0049, 0176, 0179 and 0196, stay out of any L6 truth, PLAN section 1a table B. Render five L6 masks before any L6 row is believed.

Gate, pre-stated. Ratio-only T12 against L1 AUC at or above 0.95: a single-vertebra 3-D target exists and stage 2 inherits its feature list. Between 0.90 and 0.95: the target is one body plus one neighbour. Below 0.90: the parity target is a window of three or more bodies, and the 2-D one-body number of 74.8 % is compared to a window number, never to 0.990. For the L6 rows, a cross-validated AUC with a bootstrap lower bound above 0.5 on 13 positives shows some signal; otherwise the article's refusal stands.

Outside check. The sign of every ratio's weight against Panjabi 1991 Table 3 per-level means, PAN; `panjabi_reference.csv`. The dominant weight must stay on the transverse-process span or the variant has changed the question. Schinz 2026's 100 % against nerve morphology on 1,242 CTs, TLJ row 7; MPDA lines 341 to 344.

**Stage 2. Projected morphometry at exact pose on the 802 v11 label volumes.** On the grid, `reqp --qos=requeue`, outputs under `/rs/rs_grp_oschome/go2432/`; the label-only extractors take 15 to 30 minutes at 20 workers, REPRO section 1. Names through `labels_for`; axes from `aff2axcodes`, the volumes are P, I, R on disk, PIR; spacing through `pir_spacing`, because the renderer once wrote the A-P voxel size as the S-I row spacing, DRS. The public Hugging Face mirror is v10 with id 29 and must not be the source, HFM. The first grid step follows decision row 22: submit, estimate the wall time, write the job ids and ETA to the resume file, stop.

1. Rebuild the lateral and AP projected-landmark bank from the v11 tree on the respaced `ctsp_drr` geometry and the `render_physics_drr` perspective geometry. Poses are the canonical lateral 90 and AP 0, and the arc at 10-degree steps with tilt minus 15, 0 and 15. Record pose, magnification at the target body and detector pitch in every annotation.
2. Project every label and every SPINEPS subregion separately: body 49/50, costal and transverse processes 43/44, articular processes 45/46 and 47/48, ribs 34 to 61, sacrum 26, hips 30/31, MAPI section 6.2. Keep the overlap count where two silhouettes claim a pixel, as `project_labels` already does. SPINEPS masks before commit 147428d carry raw ids and must pass `tools/spineps_ids.py`, SPID.
3. Measure the 2-D analogues on the projected silhouettes and landmarks, never on the grey image. Lateral: anterior and posterior body height, wedge, canal depth, S1 plate angle, crest line. AP: end-plate width, interpedicular width, pedicle oval width, process span, process height, process to ala gap, rib presence and 12th rib length. On each arc pose, the same set where the silhouette exists. Divide by the recorded magnification.
4. Compare 2-D against 3-D per level and per view: bias, SD, ICC with case-clustered intervals, Bland-Altman limits; the share of records where the feature's silhouette is not separable from a neighbour, from the overlap count.
5. Rerun `test_morphometric_separability.py` unchanged on the 2-D readings, lateral only, AP only, both, and the best single arc pose, grouped by case. Report T12 against L1 beside 0.990, and the stage 1 ratio-only variant on each view.
6. At the lumbosacral junction report descriptively only. The 18 L6 records by label and 16 by the readers, and the 9 four-lumbar identifiers, with their projected process height, process gap, fusion, S1 plate and crest values against the 643 ordinary records. No AUC is fitted on 15 per stratum.
7. Render twenty records per view with every measured chord drawn before any number is believed, RDO; CLAUDE "Render the mask".

Gates, pre-stated. A feature is "represented" in a view when its 2-D ICC against the 3-D column is at or above 0.75 with the case-clustered lower bound above 0.60. Its per-level SD must also lie inside the widest published living-cohort SD in `level_references.csv`. "Partly represented" is an ICC point between 0.50 and 0.75. Below 0.50 is "not readable" in that view. The 0.50 and 0.75 cut points are the Koo and Li 2016 reliability bands, unverified, web; the paper is not on disk. They are fixed before the run. The junction verdict per view is the T12 against L1 AUC on the represented features: at or above 0.970 is parity at the geometry step; 0.90 to 0.97 is partial; below 0.90 is failure for that view. Two notes proposed single thresholds, 0.95 and within 0.02 of 0.990; this document reports the three tiers so both are visible.

Outside checks. The spread test that caught both defects in the dataset article, LM "How they were caught". The SD of each 2-D measure is held against the widest living-cohort SD, canal depth at L3 2.45 by Griffith and end-plate width at L5 5.54 by Yadav. The share below a floor is held against published prevalence. The share of AP process heights at or above 19 mm against the 33 graded Castellvi records and `tp_height.csv`. Lateral body heights against Panjabi and the radiograph series in `level_references.csv`, 355 rows across 5 to 18 series per quantity, NPR. Those series disagree with each other by 21 to 69 % of their own median. A 2-D feature that agrees with its 3-D twin no better than the series agree with each other carries no information. Magnification is 1 by construction and is stated. The Ljubljana specimen as an n 1 check of the projected-landmark step at gold pose, read-only under its ND licence. And a leak rule: if a lateral-only 2-D model matches the AP model on a coronal feature, something leaked.

Smallest experiment that changes a decision. Fifty records, lateral and AP, T12 to L4, two hours on `reqp`. This is a smoke test of the projection code, not a scored gate. An ICC of 0.75 on 50 records carries about plus or minus 0.13 and an AUC on 50 T12 and 50 L1 about plus or minus 0.03, calc, so the ICC and AUC tiers are scored on the 802. L2, L3 and L4 are in the pilot because L3 carries the largest one-body error count on the real C-arm, section 1.7.

**Stage 3. Real frames on C-ArmLSpine and COBRA2026.** Stage 3 waits on two things. The first is stage 2's definitions. The second is the pose verdict of project PAR-4 in section 6, which asks whether naming accuracy on C-ArmLSpine tracks the registered pose quality; no file has answered it, MAN carmlspine. Then:

1. Run `ostk.morphometry.level_morphometry` and the release extraction columns on each CBCT's agreed body labels for L1 to L5 and the sacrum. Ids are guarded by `tools/spineps_ids.py`. This runs after the ostk fix, CT-1, or uses the release scripts' columns.
2. Re-fit or verify the poses at the true 0.150 mm pitch, bounded around the header geometry, verified by detector boxes through `tools/carmlspine_pose_qc.py`.
3. Reject frames whose edge NCC is below the per-view median or whose box disagreement exceeds 0.25 body.
4. Project the per-vertebra 3-D landmarks onto each frame and render twenty overlays per view.
5. Regress each 3-D measure from the frozen encoder embedding of that body's crop, leave-case-out and day-grouped, per view. Regress it again from the projected landmarks measured on the frame. The two regressions separate "the encoder does not encode it" from "the projection does not carry it".
6. The primary table is built on complete, agreed, SPINEPS-boxed bodies. The 204 of 287 such bodies with recall 96.9 % are the 28-case C-ArmLSpine test split, CPD. Stage 3 fits over all 149 cases, so the clean-body filter is recomputed over all cases before the primary table is built; the 28-case split and the full set are reported beside it.
7. Report the three one-labeller L6 cases descriptively, as agreement, never as correctness.
8. COBRA's Elekta frames are the second device for the sacral features once sacral coverage is verified.

The real check already on disk: the render regression's real-frame check gives R² 0.65 for anterior height, 0.63 for process span, 0.75 for wedge and minus 1.76 for posterior height on L2 to L5 centroids, GRAD `real_check`. The thoracolumbar pair cannot be scored on real frames today because the C-ArmLSpine truth names T12 on 10 % and T11 on 0 %.

### 3.5 The feature-engineering and training variants the experiment would feed

Row 14 of the standing decisions binds this section: a new loss, head or augmentation is a published, validated method with its number, chosen from a survey, and Greg decides before anything is built, MDF. Each variant names its published analogue and the number on disk. None starts until stage 2 has said which features a view carries.

| variant | published analogue and number on disk | what it changes | first arm | gate | conflict with the record |
|---|---|---|---|---|---|
| V0, the measured 2-D feature arm | the features are measured, not learned; Farshad 2013 is the one lateral rule, sensitivity 94 %, specificity 74 %; per-feature analogues in section 3.2 | appends the stage 2 features measured from detected boxes and landmarks to the classifier posterior before the alphabet coupling | reproduce Farshad 2013 on the lateral renders of the 21 graded III and IV records and the 643 ordinary records with the published +10 degree threshold unchanged; then the ALPHABET_LOSS protocol with the feature vector appended | sensitivity at or above 0.75 transfers the rule; below 0.60 the lateral is declared empty for the fused class too; then HELPS, TRADE-OFF, HURTS or NOT SHOWN by the pre-stated rule | none, provided every feature carries the 3-D column it came from and the pose it was projected at |
| V1, feature-supervised auxiliary heads | multi-task auxiliary regression beside the class head; the closest lineage on disk is Payer 2020's landmark network, lumbar id rate 90.45 %; no paper on disk supervises a 2-D naming head with projected 3-D morphometry | adds regression targets, the "represented" features in the trained view, to the recurrent head; targets are size-free ratios because absolute size gave no gain three times (LID13) | the ALPHABET_LOSS protocol exactly: same bank, same windows, three seeds, paired case-cluster bootstrap against lambda 0 | the pre-stated rule on L6 recall, film held, false-L6 cost; plus T12 against L1 one-body accuracy on the real C-arm beside 41.2 % | a bespoke loss unless Greg accepts the multi-task framing as published practice |
| V2, projection-consistent training | multi-view consistency; the one published spine instance on disk is the Multi-View sequence loss, which the ladder design excludes because it re-injects the counting prior (CLD); no number on disk | asks the embedding of one vertebra at two arc poses of the same CT to agree on the stage 2 features, not on the name sequence | renders only; score on `tools/unseen_cases.py` renders and the case134 302-frame spin, n 1 real | the per-angle naming curve against 82.1 % at trained angles and 52.8 % elsewhere; recall against angle as a curve, never one number | must not become a sequence loss; any gain that vanishes at one body in field is counting |
| V3, DRR curricula and the ratio sweep | SyntheX parity at 6.44 against 6.46 mm; the own two-stage arm lost 89.1 / 40.4 against 91.8 / 66.0; the ratio was never swept | orders render exposure by pose and visibility, or sweeps the real share | the 45-cell array, three seeds, L6 scored separately | a cell that raises held-out L6 recall without lowering ordinary film by more than the seed spread, 1.0 point at full size (NUM:488) | mixing is the default; the curriculum is an arm |
| V4, pose-conditioned features | no spine paper on disk; the device cards carry nine fitted terms worth +4.3 held out | gives the head the pose as an input scalar so it can weight lateral and AP features differently | renders with the pose against the same renders with the pose withheld, per angle bin | a gain in the 16 untrained bins that survives on the case134 real spin | a head that needs the pose on a real frame needs a pose estimator, which is a second product |

Excluded by the record and not revisited without a new argument: Star Temporal Classification, STC; CycleGAN, ADDA, CUT and SDXL restyling, FGS; DFL; decoder-named pseudolabels, RR17; size in millimetres as a scalar, LID13. A learned refiner as the 2-D reference is excluded too, because it invents pixels, 68.1 % explained against 69.3 % calibrated, LFR.

### 3.6 The parity metric, defined

Parity is measured per level, on the same persons, as two single-level accuracies side by side on one label set. Both sides are scored on the seven levels T11 to L5. The junction pair T12 against L1 is reported as a second row, with the 2-D posterior restricted to T12 and L1 so that chance is the same on both sides. The 3-D side is the ratio-only single-vertebra shape model from stage 1, refit on the G3 training persons, with no case median, no position, no rib and no segmenter name. It is scored on the held-out bodies of the G3 validation persons. The 2-D side is the one-body-in-field accuracy of the 2-D classifier on renders of the same bodies at the view under test, and then on real frames of the same persons where they exist. The 2-D side waits on FLU-2's clean encoder, because 801 of 802 CTSP persons sit in v9 lineage, section 5.2. The persons are the 73 CTSP persons in G3 validation, SPLT line 64, because `level_gradients.csv` holds only the 802 CTSP cases. The VerSe and TotalSegmentator validation persons enter only if reader E's `features_j1.csv` is fetched from the grid and passes its J2 spread gate, MAPI lines 128 to 130; that fetch is added to PAR-2. Each side carries a person-clustered 95 % interval, and the difference carries the interval of the paired difference. Parity is a non-inferiority claim with a 5-point margin, pre-stated here. Parity at a level means the paired interval excludes a 2-D deficit larger than 5 points. An interval that merely includes zero is not parity, because at this n it would call a 7-point deficit parity, section 3.8. The published 0.990 is reported beside the two accuracies as the ceiling, never as the 3-D side of the comparison, because it needs three levels per case. L2, L3 and L4 are in the comparison because L3 carries the largest one-body error count on the real C-arm, section 1.7.

### 3.7 Gates and the stop rule

1. If projection kills the feature. A feature "not readable" in every view at exact pose with no noise leaves the inventory. No head is asked to predict it, no auxiliary target carries it, and the manuscript says the feature does not survive projection. If every feature that separates a pair is in that state, the pair is routed to the count from the anchor and the 2-D parity claim for that pair is withdrawn, TMT.
2. If the lateral and AP 2-D readings together do not reach T12 against L1 AUC 0.90 on exact-pose renders with no noise, no 2-D model on real frames will. The parity claim at the thoracolumbar junction is then withdrawn at the geometry step, before any network is trained.
3. If the feature survives on renders and dies on real frames, that is a formation or truth-denominator fact, not an anatomy fact, until it is tested on a second device, KDN. COBRA's Elekta frames are that device for the sacral features.
4. If the view that carries the feature is not the view the surgeon takes, an AP-only feature for the thoracolumbar junction is a true result and a workflow constraint. The programme states it and does not force it into a lateral model.
5. If the 3-D side has no number, no 2-D parity is claimed at that junction. At the lumbosacral junction nothing is claimed until a 3-D single-body number exists on the same persons, LS 7.1 row 39.
6. If the lineage is dirty, the number is not quoted. Any held-out render number for a v9-lineage model comes only from `tools/unseen_cases.py`, 70 TotalSegmentator, 1 CTSP, 0 VerSe, TSB.

### 3.8 n and power

Stage 1 and 2: 1,486 T12 and L1 vertebrae from 798 cases, paired on the same bodies. The AUC bootstrap interval at that n is about plus or minus 0.006, calc, so a 0.02 difference is decidable with power near 1. The limit is the grouping, which the case-grouped bootstrap handles. Per-feature ICC: 663 to 802 records per measure and level, canal depth at L2 the fewest and process span at L1, L2 and L4 the most; anterior body height alone runs 723 to 772, GRAD `measures.*.n_records`. L6: 13 ostk positives after the disputed 0033 is removed, against 757 L5 rows; 18 by label. At 13 positives an AUC of 0.80 carries an interval of roughly plus or minus 0.13, calc, so stage 1 separates "no signal" from "some signal" and nothing finer. The parity comparison of section 3.6: 73 CTSP persons in G3 validation, SPLT line 64, about 146 T12 and L1 bodies, calc, two per person. At 3-D 0.97 the person-clustered interval is about plus or minus 2.8 points and at 2-D 0.75 about plus or minus 7.0, so the paired difference carries about plus or minus 7.5 points, calc. The minimum detectable deficit is therefore about 8 points. The 5-point margin is decidable only if the 2-D side sits within 2 to 3 points of the 3-D side, or once the 93 CTSP test persons are added after "H1 seen". Stage 3: L1 is present in 76 lateral and 81 AP frames, L2 to L5 in 123 to 142 each, PLDA Table C. One C-arm model, so the device-against-anatomy confound is not resolvable on this set alone.

### 3.9 Outside checks

The spread test and the render, as in stage 2. Panjabi 1991 Table 3 for the sign of every weight, PAN. Schinz 2026 for the 3-D side. Hou 2020 for the rule that a 2-D feature agreeing with a 2-D read is not validated, kappa 0.50 against CT, PREV. Hanhivaara 2024's radiograph kappa 0.22 [0.16, 0.32], HANH line 263, as the bound on what an AP process feature can add. Rohlfing 2012 for the rule that overlap and similarity are not evidence of a correct mapping, RSP E1. Kwak 2025's T12-rib attention as the warning that a 2-D feature study can reproduce the counting prior it is meant to replace. The study must separate junction morphology from rib-counting cues or it reproduces that prior, note 6 flag F10.

---

## 4. CT-based projects

Ranked by how little stands between the holding and a result, and by what each unlocks. Every project names its outside check.

| rank | project | question | data | comparable published number | first experiment | gate | n or power | outside check | file |
|---|---|---|---|---|---|---|---|---|---|
| CT-1 | the ostk canal-closing fix, tested against the 0097 release rows | does restoring the per-section hole rule bring VBHp and EPD back within 1 mm of the release rows | `ostk/morphometry.py` `canal_dimensions` line 151, `level_morphometry` line 380; `ostk_level_morphometry.csv` at commit 90a27a7 as reference; record 0097 and twenty records | living canal floors 11.70 mm Čizmić 2023 and 11.07 mm Aly and Amin 2013; Framingham congenital stenosis 2.62 % | per-section hole area at least 18 mm², wall taken only from sections whose hole reaches the canal's median area, raised `min_vox`; run on 0097 and twenty records; render ten body cuts; then guard or remove `"S1": 29` so a by-name call raises | 0097 rows within 1 mm on VBHp, EPDl and SCD; share under 11.07 mm at or below 5.2 %, calc, twice the published 2.62 %, the J2 window rule, J3NS line 34; the number the fix must move is 15.8 % of reader E's J1 instances under that floor, six times the prevalence, J3NS line 14; per-level SD inside the widest published living SD; then refresh the grid copy | 802 records by five levels | the floors and prevalence; "the numbers moved toward the mean" is not a pass | OCR; LM; J3NS |
| CT-2 | the anterior pelvic plane over 802, and the spinopelvic open items | the anterior pelvic plane is unmeasured on this cohort: what is the APP-referenced sacral slope beside the scanner-axis one, and does the gap to Veilleux exist on v11 at all | 802 v11 label volumes with hips 30 and 31; 756 pass the plate gate; 8 records measure PI from a prosthetic head | two readings of the gap are on disk. SPE section 5, written before the 2026-09-11 plate fix, reads SS 33.1 against Veilleux 36.5, a 3.4 degree gap, with PI 52.6 and PT 19.6, SPE lines 153 and 180. The v11 release table reads SS 36.6 +/- 10.6 against 36.5 on n 756, PI 52.1 and PT 15.5, a 0.1 degree gap, MPDA lines 723 to 727; note 6 row 84. SPE's own head-to-head gives the release extraction code a median SS of 35.9 over 300 records, SPE line 106. This document uses the v11 table; SPE section 5 is stale, section 8 row 29. Veilleux PI 52.1, SS 36.5, PT 15.6 on 200; supine APP tilt median +5.1 degrees in 422 hips, Uemura, and +8.6 to +12.2 in Jenkinson; Suzuki 2020 ICC 0.856 for anatomical SS, SPE lines 172 and 194 | step 1, before any fit: recompute SS, PI and PT means and medians from the v11 release columns and print them beside Veilleux, to confirm the gap is 0.1 and not 3.4; then one script: ASIS and pubic tubercles as extremal points on the hip labels, APP, APPA, aSS and aPT; render ten fits first; report the 8 prosthetic records by Imai 2019 and Takahashi 2021; update REPRODUCE.md item 1 and rewrite SPE section 5 | APPA median inside the published supine band, +5.1 to +12.2, or the extraction is wrong; aSS is reported beside SS as the posture-independent parameter; no convention-against-cohort dichotomy is stated unless re-derived from the v11 numbers | 802; a stratified read of the 33 graded records for the 10 to 15 degree LSTV shift | Veilleux and the APP band; Suzuki's ICC 0.856; the identity PI = SS + PT is not a check; then a two-reader manual read of PI, SS and PT on 50 records with MAE, ICC and Bland-Altman, which no file holds | SPE section 5, stale; SPE line 106; MPDA lines 713 to 727; note 6 row 84 |
| CT-3 | the whole-cohort Castellvi read, the seven re-reads and the VerSe raw-mask L6 count | how many Castellvi II to IV spines does CTSP hold, and does the rib anomaly co-segregate with the lumbosacral one | 802 CTs, 789 countable, LS 5.2; 33 consensus grades, two residents, kappa 0.74, no senior read, NIPS lines 95 and 989, not in MPDA, whose line 707 records only the six resolved disagreements; queues `castellvi_reread_queue.csv` 25, `castellvi_type1_queue.csv` 214, `lstv_reread_queue.csv`; VerSe raw masks under `~/VerSeFusion/data/unified/scan-*/`, never `vf_813` | Castellvi II to IV 9.0 % of 3,855 CTs, type I 68 % of calls; CT inter-reader kappa 0.63 to 0.71; Nagata 2025 co-segregation; VerSe OR 3.61 [2.08, 6.27] on 280 graded | one script counts ids 25 and 28 per raw mask against the Loeffler table with the 37 duplicate series collapsed; a third reader blind to the first two reads 0008, 0021, 0033, 0049, 0176, 0179, 0196, 0172 and 0068; then two readers grade all 802 in the review tree with a senior adjudicator | the II to IV rate inside 9 to 18 % and type I near 68 % of calls or the read is suspect; second-reader kappa at or above 0.63 or a third reader before anything trains; a VerSe subject enters the L6 pool only when table and mask agree | 802 cases at 3 to 5 minutes is 40 to 67 reader-hours per stage, calc; expected positives 71 to 142, calc, 9 to 18 % of the 789 countable records; the stump-rib against II to IV test has power 0.98 at OR 3.61 and 0.59 to 0.81 at OR 2.1 | the prevalence band; the readers' CTSP L6 rate 16 of 789, 2.0 % [1.3, 3.3], against the 3.2 % prior; the token join through the manifest field only | MPDA lines 707 and 919 to 921; NIPS lines 95 and 989; CSB; PLAN section 1a; LS 5.2 and 7.2; proposal C calc |
| CT-4 | the 3-D single-body classifier at both junctions, and the CT phenotype classifier certified for LS-L6 only | can one rib-free body be called thoracic or lumbar from its own facet angle, process position and shape, with no case median; can a segmentation classifier pseudo-adjudicate LS-L6 at a PPV lower bound of 0.90 | unambiguous T11 and T12 bearing a rib of at least 38 mm and L1 to L5 of the same spines over CTSP, VerSe, TotalSegmentator and SPINEPS pairs, about 3,000 pairs; read-tier persons 202, LS-L6 93, 88 after contradictions | Schinz 2026, 100 % on 1,242 CTs, TLJ row 7; VERIDAH LEA 97.22 %; HealthOST 91.49 % naming agreement with three readers; no published CT LSTV classifier validated against radiologist Castellvi reads | the stage 1 ratio-only run; then J0, a 20-CT timing task across three segmenters; then logistic regression on F1 to F3 plus F5, StratifiedGroupKFold K 5, five seeds, P(thoracic) at or above 0.8 thoracic and at or below 0.2 lumbar; then the LS-L6 pool under grouped K-fold | J2 spread gate before J3; PPV lower bound at or above 0.90 on LS-L6, at most 3 errors on 88 or 0 on 35; segmenter invariance as a hard demotion; per-class prevalence inside the published windows | 1,486 for the pair; 88 for LS-L6; sacralised 24, Castellvi II 28, T13 6, four-lumbar 2 need +11, +7, +29, +33 zero-error reads | the published facet-angle series per level before any threshold; the TL-11 VerSe reads; render every call on the ambiguous body; VERIDAH's recall against its 10 of 24 agreement here | MAPI section 6; PLAN verdict and section 10; AUTO |
| CT-5 | level atlas revision: the vertebra's own frame and the SPINEPS corpus label | does measuring each vertebra in its own frame, and the end-plate from a corpus label, restore L5 and bring every per-level SD inside the published range | 802 CT and label pairs; SPINEPS subregions for 801 records on the grid; `surgical_morphometrics.csv`, `ostk_level_morphometry.csv`, `level_references.csv` | Bonczar 2024 L5 EPWu 48.81 over 1,481; Griffith 2022 SD 2.45 at L3; Čizmić floor 11.70 mm; Maeder 2023 obliquity by hand in 1,050 patients | rerun end-plate width at L1, L4 and L5 from the SPINEPS corpus label on the same 741, 773 and 764 records; score with the three columns LM uses | no rule ships unless it beats the shipped rule on all three columns; the last three attempts each won one and lost another | 802, paired | render twenty retained L5 masks before any number; if the corpus label's L5 SD stays above 5.54 the shoulders were not the whole story | LM section 2 and "Still open" |
| CT-6 | the L6 learnability curve on Dataset815 | at how many distinct six-lumbar cases does L6 Dice leave zero, and does the rib-free counting decoder beat it at every n | Dataset813 with stale flags, 23 against 34; Dataset815, 1,176 cases, 62 L6 by manifest, never preprocessed; VerSe masks with id 25 on 44 of 76 read L6 | VerSe'20: 85 L6 scans in the whole set, and 28 in its training split sufficed, SYN lines 93 to 94; VerTE-MT L6 Dice 81.03 % public, 75.96 % hidden, AUTO lines 217 to 218 | preprocess Dataset815 where singularity resolves, repair the flags from the deposit manifest, then one fold at 18, 36 and 62 distinct L6 with case-level oversampling and a lumbar-rib signature | the preflight refuses a validation fold with fewer than two variant cases; the endpoint is the rib-free count by status, not Dice | three points on a curve, 18, 36 and 62, read against the 28 training-split scans of VerSe'20, not the 85; qualitative, zero against not zero | the counting decoder on the same folds, 6 of 6 on truth input; the 25-presacral share 5.5 to 8.2 % | L6SC; MAN nnunet_dataset815; SYN lines 93 to 94; AUTO lines 217 to 218 |
| CT-7 | the anchor-ordinal design: detection by disagreement | do two dense ordinal fields, count from the sacrum and from the lowest rib-bearing body, plus a per-body type, flag the variant as a consistency violation | 802 CTSP; rib-free count against the source label, normal and transitional: count 4 in 21 and 8, count 5 in 736 and 7, count 6 in 9 and 18, AOD lines 389 to 392; the table sums to 799 while its caption says all 802, a disagreement inside the file | Schinz 2026; MPDA 0.990 | arms 1 and 2 of the design as a matched pair on the same folds; the delta is the result | an ROC on the count disagreement separating the 26 transitional-labelled records at counts 4 and 6, 8 plus 18, from the 757 normal-labelled records at counts 4 and 5, 21 plus 736, calc from AOD lines 389 to 392, at AUC above the rib-free count alone; the 7 transitional at count 5 and the 9 normal at count 6 are the cells a count alone cannot separate | 16 lumbar-rib cases stay 16 | patch geometry measured on the corpus, T11 to S1 about 265 mm, bi-iliac 278 mm median | AOD |
| CT-8 | the rib phenotype by the vertebra, not the rib | does the costal facet separate a hypoplastic twelfth rib from a lumbar rib where length cannot | 98 stump twelfth, 16 lumbar ribs; VerSe 12 read lumbar and 18 read hypoplastic; Möller masks | Möller F1 0.84 from the first 22 mm; Doo 2020 11, 12, 13 pairs 8.0, 91.6, 0.4 % | calibrate PREREG rule 3 on the VerSe masks against the Löffler stump column; then the costal-facet signal on named T12 and L1 bodies with SPINEPS subregions | Möller's reference distributions reproduced before the rule is used | 30 read positives; routed through the T12 against L1 pool of 1,485 | prevalence windows: thirteen rib-bearing 0.37 to 0.88 %, lumbar rib 1.6 % | STUMP; PRER rule 3 |
| CT-9 | the super-detector adjudication to a frozen rule | how many of the 1,052 positively flagged and 1,285 disagreement-flagged tier-1 CTs are transitional | 21,622 CTs; tier 1 5,094; 2,951 with both junctions in field; 850 CTs with a radiograph of the same person, COBRA 692 and C-ArmLSpine 149 among them, PRER line 20 | whole holding: expected L6 377, four-lumbar 188, T13 44 to 138, LS line 676; the 18 screened acquisition collections alone: L6 322, T13 38 to 119, N4 line 137 | finish the PREREG calibration list, fill the freeze line, run the flag over tier 1, open the review queue, paired cases first | the sweet spot, specificity maximised at sensitivity at or above 0.95 on read-tier positives, computed before the sweep | 1,052 cases is 50 to 90 reader-hours per stage | per-collection call rate against the prevalence windows; the 33-CT census discrepancy resolved | TIERS; PRER; REVT |
| CT-10 | the competitor benchmark, finished in one scoring space | on the same 802 records, what count and name does each public system give, and where does each fail on the 33 graded | `ssn:benchmark/cases.csv`; TotalSegmentator native outputs; SPINEPS plus VERIDAH relabelled stores; VISTA3D set up | VERIDAH 99.18 %; TotalSegmentator L6 0 of 1,152 here; HealthOST 91.49 % | run `ssn:benchmark/collect.py` and print the offset histogram and the whole-spine shift count per phenotype | every mask passes `assert_verse_monotonic`; truth scores Dice 1.000 through the same path | 802, 33 graded, 18 L6, 9 four-lumbar | a system's number on its private cohort and its number here are two numbers | CBM lines 10 and 14; SBM |
| CT-11 | segmental mobility from the 351 prone and supine pairs | per-segment lumbar angular change between prone and supine | 351 within-patient pairs; one acquisition per pair labelled | none on disk for paired-posture CT; Panjabi segmental ROM as the envelope | pseudolabel the second acquisition of 20 pairs out of fold; require PI to agree within its repeatability before any angle is read | PI invariance across the pair | 351 pairs | PI invariance | PSF; MPDA line 872 |

Two housekeeping items sit beside these and gate publication rather than research. The first is the dataset article resubmission at Medical Physics: seven items needing Greg, and REPRODUCE.md section 0 and Known-open item 1 corrected to v11 and to the solved 128-record failure, RLC; REPRO; note 6 flags F2 to F4. The second is paper 1's eight rigor fixes, held for the TTO's answer on Part B, RAF; CNS.

---

## 5. Datasets by project

"After migration" is a target path, not a state. No HOME imaging folder had moved on 2026-10-07, B06 was copied on 2026-10-08 with finalization unrecorded, and a direction that reads from `$RS` must first check `runs/<B>/STATUS` on the grid, MAN section 4 row 40; DDP; MP section 5.

### 5.1 The fluoroscopy classifier

| source | holds | labels, who made them | transitional content | restrictions | bank or split today | leakage into the current encoder | file |
|---|---|---|---|---|---|---|---|
| C-ArmLSpine | 149 sessions, 299 spot frames, 149 CBCTs | none released; two automatic labellers on the CBCT; poses by edge registration | 3 L6, one labeller, test only | CC BY 4.0; a real name in case134 headers | `realxray/carmlspine` 148 cases split 105/15/28, the pre-repair count, MAN lines 13833 and 13905, against 149 live; `carm_cv0..4`, `carm_cvday0..2` | the older `carm_cv*_drr` fine-tunes descend from v7; the zero-shot v9 numbers are clean, and the 97.4 % in 1.1 is the gated v9-lineage rerun, NUM:463 | MAN carmlspine |
| COBRA2026 | 692 cases, 375,618 projections | automatic; two-labeller boxes on 150 Elekta exports | 91 screen calls, 57 field-supported, 7 with a frame | CC BY-NC; 175 cases embargoed to 2032 | 145 cases in `realxray/cobra_elekta*`, 3,480 frames; Varian 0 | not in the level bank | MAN cobra2026 |
| DeepFluoro | 6 pelves, 366 frames with exact pose | one merged vertebra class; 14 pelvic landmarks | none | NC either way | `realxray/deepfluoro` 238/24/104 by specimen | detector and card only | MAN deepfluoro_h5 |
| BUU-LSPINE | 3,600 cases, 7,200 films | end-plate lines; levels counting-inferred; L4L6 sheet | 129 four-lumbar, 15 six-lumbar; 9 of 15 children | EULA; "No License Provided"; owner-only | 3,603 laterals in v9; AP films in no bank | all laterals in v9 lineage | MAN buu_lspine_3600 |
| CSXA | 4,963 lateral cervical | expert corners C2 to C7 | none | CC BY 4.0 | all in v9, 4,214 train, 749 val | all in v9 | MAN csxa |
| NHANES II | 17,073 films; 543 landmarked | expert landmarks on 543; pseudo on the rest | none read | public domain | 543 in v9; 16,531 in no trained bank | 543 in v9; v2, v6, v7 twice | MAN nhanes2 |
| VinDr-SpineXR | 10,466 images, 5,000 studies | lesion boxes; pseudo levels on 7,625 | a tier-B pseudo-flag count off the junction was quoted as 209 in the notes; 209 is not on disk | PhysioNet DUA; no WSU determination | 0 in v9; 7,625 in `vindrps` and v7 | `vindrps` 77.8 % validation leak | MAN vindr |
| render banks | ctsp_drr 802; physics_drr 7,045; physics_rare 1,482; verse_drr 387; ts_drr 2,905; xrsp1k 6,416 | CT labels projected | physics_rare: 34 CTSP plus 47 VerSe transitional series | inherit CT terms | v9 = films_drr + ctsp_drr + verse_drr + physics_drr + physics_rare | all inside v9; TS bench inside v9 except 70 | MAN render cards; TSB |
| the G3 split | 50/10/40 per subtype; every real transitional subject in test | | test L6 43 plus 3 real, of whom about 29 carry an L6 mask a render can score and 14 are audit-only; T13 3, sacralised 11, Castellvi 12, lumbar rib 6; validation L6 11, 7 render-scoreable and 4 audit-only; T13 1, SPLT lines 26 and 35 | | leak audit PASS 2026-09-23 | 92 of 97 validation and test persons sit in v8 or v9 training | SPLT; TAB2 note d |

### 5.2 CT projects

| source | holds | labels | transitional content | restrictions | state | leakage and traps | file |
|---|---|---|---|---|---|---|---|
| CTSpinoPelvic1K v11 | 802 records, one per patient; 422 supine, 377 prone, 3 decubitus | radiologist-sourced vertebrae; sacrum and hips expert where fused, pseudolabel otherwise; ribs student-corrected; Castellvi two-reader consensus on 33 | L6 18 by label, 16 by the readers; graded 33; sacralised fused 12 by label, 9 as truth; four-lumbar 9 two-labeller; no FOV reaches T1 | CT CC BY 3.0; labels CC BY-NC-SA 4.0; the HF mirror is v10 with id 29 | Zenodo v11; grid `~/data/CTSpinoPelvic1K/labels` | shipped folds never read the lumbar count; token is not the record id; 801 of 802 in v9 lineage via renders | MAN ctspinopelvic1k; HFM; CSB |
| CTSpine1K | 1,005 volumes | expert VerSe-convention masks | README lists 24 lumbarisation and 13 sacralisation, an authors' list; 3 new read-tier persons in MSD-T10 | CC BY-NC-SA 4.0 | Ceph-native | 782 COLONOG volumes are CTSP persons | MAN ctspine1k; DDP C02 |
| VerSe and VerSeFusion | 374 scans of 355 subjects | expert masks C1 to L6, T13 = 28; Loeffler 2021 table, two neuroradiologists | read tier L6 85, T13 6, sacralised 13, Castellvi II 27, lumbar rib 12, stump 18 | CC BY or BY-SA, quoted both ways | B06 copied 2026-10-08, finalization unrecorded | `has_T13` is wrong, 18 against 6; 39 of 85 L6 masks lack id 25; never `vf_813` for whole-spine work; verse707 conflict | MAN versefusion; VFT; VF8 |
| TotalSegmentator v2 and v3 | 1,228 and 1,935 scans | 117 structures, model output refined; no L6, T13 or lumbar-rib class; `sacrum` excludes S1 | two-labeller L6 14; outside reads on 70 CTs, 28 L6, found 12, 17 and 9 | CC BY 4.0 | B07 plan | 1,118 v3 CTs byte-identical to v2; `s####` not stable across releases | MAN totalsegmentator; TSS; DDP A05 |
| the acquisition tiers | 21,622 CTs; tier 1 5,094; tier 2 12,217 | two pseudo-labellers; no radiologist read on any acquired CT | flags L6 303, T13 82, review 1,168; expected over the 18 screened collections L6 322, T13 38 to 119, N4 line 137; over the whole holding T13 44 to 138, LS line 676 | open routes | Ceph-native | 127 exact folds merged; 1,186 near-duplicates unmerged | TIERS; LS section 5 |
| Dataset813 and Dataset815 | 802; 1,176 cases | nnU-Net raw | 18 L6; 62 L6 and 4 T13 by manifest | NC-SA | 815 never preprocessed | 813 flags stale; image links resolve only inside the container | MAN nnunet cards; D813 |
| RibFrac, RibSeg v2, Möller masks | 660 chest CTs | expert ribs 1 to 24; stump masks | T13 4 single-labeller | RibFrac CC BY-NC; Möller CC BY | Ceph-native | 648 of 743 analysed, 95 unexplained | MAN ribfrac; STUMP |
| RSNA 2022 cervical | 2,019 studies | per-level fracture labels | none | Kaggle, non-commercial | zip never unpacked | used by nothing | MAN rsna_2022 |

### 5.3 Paired sets for parity

| set | 3-D side | 2-D side | pose | per-vertebra 2-D truth | what it can test | file |
|---|---|---|---|---|---|---|
| C-ArmLSpine | 149 lumbar CBCTs | 299 spot frames, 2 sweeps | registration, verify by boxes | automatic, agreed levels | the only living-spine real pair; 3 L6 | MAN carmlspine |
| DeepFluoro | 6 pelvis CTs | 366 frames | exact | none per vertebra | the projection operator, not identity | DFC |
| COBRA2026 | 692 planning CTs on `ct_def` | 375,618 projections | exact by RTK | none; coverage unverified | second device for sacral features once verified | MAN cobra2026 |
| Ljubljana | 1 cadaver L1 to L5 | 18 radiographs | gold per vertebra | gold, five bodies | n 1 check of the projected-landmark step | MAN ljubljana |
| the programme's renders | 802 CTSP, 374 VerSe, TS, 81 transitional series | ctsp_drr, physics_drr, physics_rare, xrsp1k, devcorpus arc | exact by construction | full level truth; boxes and end-plate corners only | the visibility experiment | MAN render cards |

### 5.4 Holdings no model uses

| item | n | why unused, as recorded | what would change it | file |
|---|---|---|---|---|
| NHANES II unannotated films | 16,531 | never offered to the detector | directive D2, detector self-training | MAN nhanes2; XDU |
| BUU-LSPINE AP films | 3,600 | in no bank; no written criterion | a bank or a one-sentence written exclusion | MAN section 4 row 31 |
| VinDr in the shipped bank | 0 of 10,466 | pseudo levels; test split consumed; DUA | a determination and study-keyed splits | MAN vindr |
| AASCE 457, Spinal-AI 8,358, anchor_drr 7,842, Mendeley 584, lateral_236 212 | per row; the labelled-film counts are XDU lines 17 to 37, anchor_drr 7,842 is CORP note k | fed only deleted banks; anchor_drr's own split puts 301 of 801 CTSP people on both sides, MAN section 4 row 18; DDP C10; Spinal-AI has no person; Mendeley is a BUU redistribution | AASCE and Spinal-AI by directive D6, each wholly on one side; Mendeley stays out | XDU lines 17 to 37; CORP note k; MAN section 4 row 18; DDP B09 and C10 |
| RSNA 2022 cervical fracture CT | 2,019 studies | used by nothing | a cervical arm, none planned | MAN rsna_2022 |
| COBRA cases not exported; Varian | 547 of 692; 225 | exporter refuses Varian; the axis map was solved 2026-09-23 | write the Varian export; directive D4 | MAN cobra2026 |
| DeepFluoro vendor frames without a pose | 2,293 of 2,659 | no released pose | pose recovery, unrecorded | MAN deepfluoro_vendor |
| C-ArmLSpine sweep projections and the case134 spin | 602; 302 frames | only one script reads a sweep | export into the real-frame layout | MAN carmlspine; FP G4 |
| ts_drr_v3 | 1,735 renders | never benched | a held-out TS test by CT hash | DDP B04 |
| Dataset815 | 1,176 cases, 62 L6 | never preprocessed | `sbatch slurm/prep815.sh` where singularity resolves | MAN nnunet_dataset815 |
| tier-1 acquisition CTs | 20,280 screened | read by no one; in no bank by design | the reader queue | LS section 5.2 |
| FluoroCap | 29,500 panels | dropped by directive D1; the 200-panel test set does not exist | annotate about 200 or write it off | MAN fluorocap; DD23 |

### 5.5 Missing sets and the step to get each

| set | adds | state | the step | file |
|---|---|---|---|---|
| LevelCheck clinical cohort | 178 patients, 178 CTs, 398 intraoperative radiographs; about 16 at-risk persons at 9 % | no request drafted | Greg drafts a letter to the I-STAR group | LS A1 |
| Huashan | 140 patients, CT with intraoperative AP and lateral; about 13 at-risk | no request drafted | email [e-mail withheld] for device, headers, frames per patient, DUA terms | LS A3 |
| SX-Stitch | 1,032 overlapping intraoperative frames with masks | drafted 2026-09-23, not sent | send | SXS |
| Balgrist ex-vivo | 13 plus 6 specimens, three C-arms | drafted, not sent | send | MAN balgrist card |
| fourteen cine letters, Bournemouth among them | real cine with level-named tracks | drafted, not sent | send | MAN cine requests card |
| Charters 2024, UCLA | 527 patients, 2,486 paired kV with DICOM REG | not drafted | write | LS A22 |
| Jaganathan and Maier | 55 thoracolumbar CBCT sweeps | never released | ask FAU or Siemens under a DUA | LS A32 |
| TCIA CMB-MML and CMB-AML XA | 16 patients, one spine procedure | open, not fetched | anonymous NBIA fetch as a Slurm job | LS A6 |
| NIT Warangal | 9 level-named patients | public | download | LS A10 |
| Merlin, Stanford AIMI | E_low 1,260 transitional people, more than all of tier 1 at 831 | gated, no form signed | Greg accepts the AIMI DUA | LS B1; ACQ section 7 |
| CT-RATE, INSPECT, NLST beyond the pilot | T13 95, 86 and 109 expected at the low prior | gated or held by the stopping rule | the HF gate form; the AIMI DUA; finish the tier-1 screen | LS B3, B5, B6 |
| Griffith 2022 per-level SDs | the closest matched comparator for the atlas | paywalled | interlibrary request | LM "Still open" |
| Li 2016, Li 2017, ABLSpineLevelCheck 2024 | the naming-novelty risk; the one title near the parity question | IEEE Xplore blocked | a library request before any submission | RFP |

---

## 6. The ranked project list

| rank | project | first step | gate | n today against n needed | the decision it returns | depends on |
|---|---|---|---|---|---|---|
| 1 | PAR-1, the single-vertebra 3-D target | the ratio-only variant of `test_morphometric_separability.py`, T12 against L1, one hour on the laptop | AUC at or above 0.95, 0.90 to 0.95, or below 0.90 | 1,486 against 1,486; L6 13 positives against 757, nothing finer than "some signal" | what parity is measured against: one body, one body plus a neighbour, or a window | nothing |
| 2 | PAR-2, projected morphometry at exact pose on 802 v11 volumes | fifty records, lateral and AP, T12 to L4, a two-hour smoke test on `reqp`, with the job ids and ETA written to the resume file; then all 802 and the arc, where the gates are scored | per-feature ICC tiers 0.75 and 0.50; junction AUC tiers 0.97 and 0.90 | 1,486 against 1,486 | the per-feature, per-view visibility table and the view each confusion pair needs | PAR-1's feature list; the v11 tree on the grid |
| 3 | FLU-1, the real-frame transitional truth file | the one-hour COBRA coverage render; then the 63-volume reader queue under a frozen protocol; then the Elekta export of every confirmed case | 22 carriers for 85 %; 35 at-risk persons for 90 %; 19 for paper 2 H1 | 0 verified against 22 or 35; expected about 5 to 13 verifiable on CT, at most 19 if every supported call confirms, calc at the labeller's PPV of 10 of 24; 22 cannot be reached from COBRA alone; scorable on a real frame only where a frame is exported, 7 of 91 calls today, NUM:435 | whether any anomaly-aware claim on real frames can ever be powered from the holding; DAT-1 is the only route to 22 | a reader; the protocol freeze; the Varian exporter or a written Varian exclusion |
| 4 | CT-3, the re-reads, the VerSe mask count and the whole-cohort Castellvi read | the VerSe raw-mask count script, under an hour; the nine CTSP re-reads with a third reader | II to IV rate inside 9 to 18 %; second-reader kappa at or above 0.63 | 33 graded against 71 to 142 expected | the lumbosacral truth pools and the rib co-occurrence test at power 0.98 | two readers and an adjudicator |
| 5 | CT-1 and CT-2, the ostk fix and the anterior pelvic plane | 0097 alone, under an hour; fifty records with ten renders, two hours | 0097 within 1 mm; APPA inside the supine band; the v11 gap to Veilleux confirmed at 0.1 before the fit | 802 | safe 3-D columns for every twin; the APP-referenced sacral slope beside the scanner-axis one | nothing |
| 6 | DAT-1, send the drafted requests, draft two, fetch two | the letters out this week; record "sent" in the manifest card | a reply naming a DUA route for at least one set of 100 or more living patients | 0 sets against 19, 35 or 60 persons | whether real transitional n can come from outside the holding | Greg's signature |
| 7 | PAR-3, Farshad 2013 on lateral renders | the 21 graded III and IV records and 100 ordinary renders, half a day | sensitivity at or above 0.75 transfers; below 0.60 the lateral is empty for the fused class | 21 positives, 643 negatives | the one literature-grounded lateral feature, or its absence | the v11 end-plate corners from PAR-2 step 1 |
| 8 | PAR-4, pose quality against naming on C-ArmLSpine, and the sacra called L6 | the exactness-by-NCC-quartile table, two hours; render the 24 sacrum crops and the four off-bone laterals | odds of an error per 0.25 body of disagreement with an interval excluding 1 | 617 lateral and 631 AP bodies; 24 sacra | go or no-go for the real paired probe; a crop rule or a class problem for the sacrum | the per-frame registration scores on the grid |
| 9 | FLU-2, the clean-lineage encoder on G3, validation side, with the count-against-morphology agreement | one seed, lambda 0, job ids and ETA written to the resume file; scored on the 7 render-scoreable of the 11 validation L6 persons; then three seeds, two heads, and `alphabet_couple.py` on the same frames | the screen of section 2.8: zero or one miss of 7 proceeds, two or more stops, before any test or real arm; the count catches at least 80 % of run-shifted films | 7 render-scoreable of 11 validation persons; about 29 of 43 test persons after "H1 seen", zero misses of 29 for the 85 % bound; at a true 72.4 % the screen passes 38 % of the time and at 85 % 72 %, calc | the first quotable held-out render number, or the "not at parity" sentence; whether the two mechanisms are a measured property | FLU-1's protocol; PLAN decision 3 for the audit-only persons; the paper 2 ledger entry before any test person; the BUU licence decision before any weight leaves |
| 10 | CT-4, the 3-D single-body classifier and the LS-L6 certification | J0 timing on 20 CTs; the facet-angle model on unambiguous bodies | PPV lower bound 0.90 on LS-L6, at most 3 errors on 88 | 88 against 88; every other phenotype short by 7 to 33 reads | the 3-D side of parity at both junctions; reader E for the fusion | CT-1; CT-3's re-reads; Greg's fourteen decisions |
| 11 | PAR-5, the real paired probe on C-ArmLSpine | `level_morphometry` on the CBCTs; the pose re-fit at 0.150 mm; the embedding regression per feature per view | Q² above 0.5 on the lateral for any feature beyond height and wedge, or the parity work moves to AP | L1 in 76 lateral frames; L2 to L5 in 123 to 142 | which 3-D features a real frame carries, per view, on living spines | PAR-2's definitions; PAR-4's verdict; CT-1 |
| 12 | PAR-6, the measured 2-D feature arm and the V1 to V4 variants | V0 under the ALPHABET_LOSS protocol; each variant only after Greg's decision | HELPS, TRADE-OFF, HURTS or NOT SHOWN by the pre-stated rule | evidence persons 10 held-out L6 and 0 T13 | whether explicit 2-D morphometry moves the junction pairs, with a number | PAR-2, PAR-3, PAR-5, FLU-2 |
| 13 | CT-6, the L6 learnability curve on Dataset815 | preprocess 815 where singularity resolves; repair the flags | Dice leaves zero at 36 or stays zero at 62 | 62 distinct L6 with a read | whether L6 is learnable as a voxel class from this corpus | GPU time; CT-3's flags |
| 14 | CT-5, CT-7, CT-8, CT-9, CT-10 | as in section 4 | as in section 4 | as in section 4 | atlas revision; the anchor-ordinal premise; the rib phenotype; the census adjudication; the benchmark | CT-1; the PREREG freeze; readers |
| 15 | PUB-1, the dataset article resubmission and paper 1's rigor fixes | the seven items to Greg as a list; `build.sh --reprint`; the eight fixes on existing outputs | ten published pages; `eval_gate` held out on every quoted row | none by policy | a citable dataset article; a submittable paper 1 held for the TTO | Greg; the TTO answer |
| 16 | CT-11, prone and supine mobility | twenty pairs pseudolabelled out of fold | PI invariance | 351 pairs | a later paper | recorded as not a now-thing |

### The time order and the dependencies

Week one has no model in it. PAR-1 runs on the laptop in an hour and tells everyone what parity is measured against. The COBRA coverage render and the VerSe mask count run as single one-hour jobs on `reqp`. PAR-2's fifty-record pilot and CT-1's 0097 test run the same day. The drafted letters go out and the two new drafts are written, because they cost nothing and set the clock on the only route to real transitional persons outside the holding. The reader queues open: the seven CTSP re-reads plus 0172 and 0068 first, then the 63 field-supported volumes, then the 802 for Castellvi grade. If a reader is free on Monday, the 11 field-supported COBRA L6 calls are the single most decisive afternoon in the holding, because they can retire the real-frame transitional claim before any model is built.

Weeks two to six. PAR-2 runs on all 802 and the arc. CT-2 closes the anterior pelvic plane and REPRODUCE.md item 1. PAR-3 reproduces the one lateral rule. PAR-4 decides whether the registered poses are good enough for a real paired probe. FLU-2 trains the clean encoder from ImageNet and is read on the validation side only. CT-3's Castellvi read proceeds at 3 to 5 minutes a case.

After CT-1 and CT-3's re-reads. CT-4 runs J0 and then the facet-angle model and the LS-L6 pool. CT-6 preprocesses Dataset815 when a singularity partition is free. PAR-5 runs when PAR-2 has frozen its definitions and PAR-4 has passed.

After FLU-1's read. If 19 or more at-risk persons are verified with an exported frame, paper 2's power is recomputed under the replacement detector and the gate is unblinded under the frozen protocol. If fewer, paper 2 is restated as awaiting verified cases and DAT-1's replies decide its future. Only then is any G3 test transitional person scored, and only after the "H1 seen" entry.

Last and conditional. PAR-6 and the V1 to V4 variants, each as an arm Greg has decided on, each under the ALPHABET_LOSS protocol, each reported with its false-variant cost beside its recall.

Three things run through the whole order. If CT-3's re-reads move a record, the G3 split changes and the leak audit is re-run before FLU-2 scores anyone, SPLT header. No weight trained with BUU laterals leaves until Greg has read the licence. Nothing trains on the flagship recipe before gates G0 to G3 close, and which gates are formally closed is not written in one place on this laptop; `tools/pipeline_state.py` on the grid is the authority, FP "Gates"; note 6 Unknowns.

---

## 7. Where the proposals disagreed and what was decided

The three proposals agreed on the facts and disagreed on the axis of ranking.

Proposal A ranked by how soon a number comes back that changes a decision, using only data in the holding. It put the hour-long ratio-only 3-D run first and the clean encoder ninth.

Proposal B made Greg's parity idea the spine. It put the full projected-morphometry study first, wrote the richest feature inventory and the model variants with their published analogues, and placed the human reads second.

Proposal C ranked by whether a pre-stated claim can be decided at the n on disk in a paper that already has a home. It put paper 1's close-out and the whole-cohort Castellvi read first, placed the parity study seventh, and named the claims unreachable at any n.

This document takes B as the programme. Greg's three asks are its structure, and its feature-level specification is what a student can act on. Every proposal agreed that the geometry experiment needs no reads, no decisions and no network. It grafts from A the "smallest experiment that changes a decision" for every project. It also takes A's ordering of the ratio-only 3-D run before the full projection study, since the full study inherits its feature list from the hour-long one. It grafts from C the venue and power discipline and the list of claims unreachable at any n. It takes from C the whole-cohort Castellvi read, the single largest increase in read positives on data already held, and the week-one sending of the drafted letters, which A excluded by its own rule. Where B put the geometry experiment ahead of the reads, this document runs them in the same week. The reads are the binding constraint for the fluoroscopy classifier and the geometry experiment is the binding constraint for the parity claim, and neither waits on the other.

| item | proposal A | proposal B | proposal C | decided here |
|---|---|---|---|---|
| rank 1 | the ratio-only 3-D target, laptop, one hour | projected morphometry at exact pose, grid, one day | paper 1 close-out | the ratio-only run first, the projection study second; paper 1's fixes are housekeeping, not research |
| the reads | ranks 3 and 4 | rank 2 | ranks 2 and 4 | the same week as the geometry work |
| sending the drafted requests | excluded by rule | rank 10, "this week, zero cost", B line 357 | rank 5, "this week" | week one, zero cost |
| the junction AUC gate for the projection study | not stated as a single number | three tiers, 0.97 and 0.90 | within 0.02 of 0.990, or below 0.95 stops | the three tiers, so both earlier thresholds are visible |
| the 85 % bound on 43 test L6 persons | at most 2 misses, from the n 45 row | at most 1 miss, by calculation | at most 2 misses | at most 1 miss; 42 of 43 gives 87.9 %, 41 of 43 gives 84.5 % (calc); on the about 29 render-scoreable test persons zero misses, 29 of 29 gives 88.3 % (calc) |
| the lumbosacral parity target | scope parity to the thoracolumbar junction and the fused L5 unless the 14-row run surprises | no claim until a 3-D single-body number exists on the same persons | excluded from the projection study as undefined in 3-D | B's rule, with A's 14-row run as the first test and C's exclusion from any AUC |
| the clean encoder | rank 9, expected to fail its gate, which is the decision | rank 6, after the protocol freeze | rank 6, validation side only | rank 9, validation side first, one seed at lambda 0 as the smallest step |
| the model variants V1 to V4 | deferred until the projection study and the lateral rule return | each an arm, each needing Greg's decision | not ranked | B's table, placed last, each after Greg's decision |
| paper close-outs | not ranked | not ranked | ranks 1, 9 and 11 | listed as housekeeping beside the research list |

---

## 8. Unknowns

What is not on disk, where it was looked for, and why it matters.

| # | unknown | where it was looked for | why it matters |
|---|---|---|---|
| 1 | the ratio-only single-vertebra T12 against L1 AUC, with no case median | SEP; AOD; `ctsp:docs`; `paper/mpda` | the 3-D side of parity; PAR-1 answers it in an hour |
| 2 | any per-feature, per-level, per-view measurement of what survives projection, anywhere | the research JSONs, `SchwingNet/lit`, `research_notes`, `reports`, `ctsp:docs`; grep for "visib", "shape model", "reconstruct" | none exists; PAR-2 is the first |
| 3 | any CT L6 or lumbosacral naming rate from the programme's own model | NIPS, voxel-level only; TAB2; LS 7.1 row 39 | parity cannot be claimed against an unmeasured number |
| 4 | a human level read on any real fluoroscopic frame | RES; MAN carmlspine; LS 7.1 row 1 | every real 2-D number is against automatic truth |
| 5 | whether COBRA2026 projections cover L5 and the sacral ala | PAIRED, marked unverified; LS 7.1 row 15 | decides whether COBRA is spine data for the sacrum anchor and whether its 91 calls can be scored |
| 6 | how many of the 57 field-supported COBRA calls and the 303 L6 and 82 T13 acquisition flags are transitional | TAB2 note e; TIERS; no read exists | the whole yield of FLU-1 and CT-9 |
| 7 | whether C-ArmLSpine's 149 cases are 149 living people, under what ethics approval, and how its pose was obtained | FOURTH unknowns; LS 7.1 row 7 | the person unit of every real-frame interval |
| 8 | whether naming accuracy on C-ArmLSpine tracks registered pose quality | MAN carmlspine, "not measured" | PAR-4 and PAR-5 depend on it |
| 9 | the 3-D morphometrics of the C-ArmLSpine CBCTs | nowhere on disk | the input to PAR-5 |
| 10 | whether any drafted data request was sent or answered | the three manifest request cards, "Sent: not recorded"; LS 7.1 row 8 | DAT-1's whole premise |
| 11 | what Li 2016, Li 2017 and ABLSpineLevelCheck 2024 report | RF22 sections 5.2 and 6; IEEE Xplore blocked | could overturn paper 1's naming-novelty sentence; Li 2017 is the one title near the parity question |
| 12 | the true person-level transitional naming accuracy of any arm on real frames | PJ; RS2 S2; LCM section 8 | every power row needs it; every planning value assumed 95 to 99 % |
| 13 | which gates G0 to G7 are formally closed | FP; the top of the resume log; NUM | the time order assumes G3 is built and G4 is not; `tools/pipeline_state.py` on the grid is the authority |
| 14 | the state of the data migration and whether any batch is finalized | MP, no `runs/<B>/STATUS` on this laptop; DDP | every "run this on the grid" step |
| 15 | the TTO's answer on Part B | CNS | paper 1 and the QI protocol cannot leave without it |
| 16 | which licence reading holds for CTPelvic1K, VerSe, DeepFluoro, Geneva and Ljubljana, and the BUU EULA terms for derived labels | MAN section 4 row 8; LS 7.1 row 26 | which banks may back released weights |
| 17 | the VerSe L6 count, 85, 47, 50 or 87 | CORR; POS; LS 7.2 | a count from the raw masks has not been done; CT-3 does it |
| 18 | how many LSTV a whole-cohort Castellvi read adds | MPDA lines 919 to 921; N4 section 4 | 71 to 142 is a prior |
| 19 | whether the 1.6 % four-lumbar and 0.64 to 2.0 % T13 priors trace to a verified primary | PLAN Appendix A | every expected transitional yield inherits them |
| 20 | the source of "about 0.7 AUC from 2-D angles alone" and of "best whole-spine identification 96.5 % on MRI" | PPD; SPH; LS 7.1 row 32 | not used as checks here |
| 21 | whether the SyntheX deposit 2PGJQU and the CT Colonography localizers are on disk | LS D12 and E15 | a matched real-and-render hip set; same-patient scouts for up to 754 CTSP people |
| 22 | a manual spinopelvic read on any CTSP record | SPE; `ostk:projects/README.md`; BIBM | the only outside check on PI, SS and PT; CT-2 adds it |
| 23 | the denominator of "L6 44.9 %" and the v6 interior result files | FCM line 141; the grid-only `~/model_night/interior_windows` | the quotable anomalous film numbers come from a memory note |
| 24 | whether the 2026-09-17 refutation of pretrain-then-fine-tune was ever re-run on a clean bank | RR17 | the training-schedule default rests on a leaked-bank arm |
| 25 | who wrote the XRSpinoPelvic1K corner projection and whether its corners were validated against a reader | MAN xrspinopelvic1k, "status not recorded" | PAR-2's starting bank |
| 26 | the Ferguson view as a verified definition | the pathology sweep, whose skeptic pass never ran | the AP projection the Castellvi literature uses |
| 27 | the person counts behind AASCE's 217 index groups, CSXA's one-image-one-patient assumption and VinDr studies per patient | PIS section 4 | every leak check is only as good as these keys |
| 28 | a validated reject rule or variance decomposition for any 3-D measure | LM "Still open" | the yardstick for how much 2-D error is method |
| 29 | the spinopelvic numbers SPE section 5 argues from, PI 52.6, SS 33.1, PT 19.6, against the v11 release table's 52.1, 36.6, 15.5 | SPE lines 153 and 180; MPDA lines 723 to 727; note 6 row 84 | SPE section 5 predates the 2026-09-11 plate fix and is stale; its 3.4 degree gap is 0.1 on v11; the section needs a rewrite, and CT-2 checks the gap before fitting anything |
| 30 | the source of the VinDr tier-B pseudo-flag count of 209 | MAN vindr; XDU; TIERS; LS | quoted in the direction notes; not on disk |

Two numbers quoted in the direction notes have no on-disk source and are not used as checks: the "about 0.7 AUC from 2-D angles" paper and a TotalSegmentator Dice of 0.943, note 4 flag 8.

---

## File key

Roots.

| key | path |
|---|---|
| `ssn:` | `<repo:spinesurg-ct-nnunet 097933a>/` |
| `sn:` | `ssn:SchwingNet/` |
| `ctsp:` | `<repo:CTSpinoPelvic1K 7ddfe38>/` |
| `ostk:` | `<repo:OpenSpineToolkit cb43197>/` |
| `np:` | `<laptop:NextPaper (folders 03, 99)>/` |
| `mem:` | `<live memory folder; HANDOFF/context/ holds the copies>/` |
| notes, proposals | `<laptop:Temp scratchpad>{notes,proposals}/`; note 1 to note 6 are `topic1_*.md` to `topic6_*.md`; proposals A, B, C are `A_fastest_to_decisive_evidence.md`, `angle_B_parity_spine.md`, `angle_C_powered_claims.md` |
| `$RS` | `/rs/rs_grp_oschome/go2432` on the grid |

Abbreviations, alphabetical.

| key | file |
|---|---|
| A5 | `sn:results/a5_rows.csv` with `a5_rows_meta.json` |
| ACC | `ssn:docs/DATA_ACCOUNTING.md` |
| ACP | `ssn:tools/alphabet_couple.py` |
| ACQ | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| ALPHA | `sn:results/ALPHABET_LOSS.md` |
| AMS | `mem:anomaly-manifest-sources.md` |
| AOD | `ctsp:docs/ANCHOR_ORDINAL_DESIGN.md` |
| ASS | `mem:acquisition-space-saturation.md` |
| AUTO | `sn:lit/ct_lstv_classifier/lit_ct_lstv_automation.md` |
| BHI | `ctsp:docs/BODY_HEIGHT_INVESTIGATION.md` |
| BIBM | `np:bibm-spinopelvic/main.tex` |
| BP | `ssn:docs/BENCHMARK_PROTOCOL.md` |
| CBM | `mem:competitor-benchmark.md` |
| CIT | `sn:lit/CITABLE_CLAIMS.md` |
| CL | `sn:CLAIMS_LEDGER.md` |
| CLAUDE | `ctsp:CLAUDE.md` |
| CLD | `mem:context-ladder-2d-level-experiment.md` |
| CLE | `mem:carmlspine-level-experiment.md` |
| CNS | `mem:cns-deck-v2-2026-09-25.md` |
| CORP | `sn:tables/tab_corpus.md` |
| CORR | `sn:lit/ct_lstv_classifier/CORRECTIONS.md` |
| COUNT | `sn:results/COUNTING.md` |
| CPA | `ctsp:docs/COUNTING_PRIOR_ART.md` |
| CPD | `mem:carm-plateau-is-the-denominator.md` |
| CSB | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` |
| CV9 | `sn:results/eval_gate/closure/cv_v9/cv_v9.json` |
| D813 | `mem:dataset813-image-links-are-container-paths.md` |
| DBC | `mem:detection-is-the-binding-constraint.md` |
| DD23 | `mem:data-directives-2026-09-23.md` |
| DDP | `ssn:data_platform/dedup/DEDUP_PLAN.md` |
| DFC | `mem:deepfluoro-convention.md` |
| DFF | `ssn:docs/DEEPFLUORO_FORMATION.md` |
| DFL | `mem:drr-to-fluoro-levers.md` |
| DRS | `mem:drr-row-spacing-defect.md` |
| FCM | `mem:feasibility-claims-measured.md` |
| FCX | `ssn:HANDOFF/context/feasibility-claims-measured.md` |
| FFB | `mem:film-fluoro-boundary-not-transferable.md` |
| FGS | `mem:fluorogen-synthetic.md` |
| FNC | `sn:results/coverage/film_ncurve/ablation/READ.md`; `mem:film-ncurve-ablation-result.md` |
| FOURTH | `ssn:docs/research_datasets_fourth_pass_verified_2026-09-22.json` |
| FP | `ssn:docs/FLAGSHIP_PLAN.md` |
| FPL | `mem:fluorocap-prototype-and-lstv-arm.md` |
| GRAD | `sn:results/learning/gradient_regression.json` |
| HAI | `ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` |
| HANH | `sn:lit/ct_lstv_classifier/sources/hanhivaara2024_castellvi_CR_CT_MRI_accepted_manuscript.txt` |
| HFM | `mem:hf-mirror-is-v10.md` |
| HPH | `ssn:docs/HANDOFF_PHYSICS.md` |
| IAF | `mem:identity-audit-findings.md` |
| J3NS | `sn:results/reader_e/J3_NOT_SUBMITTED.md` |
| KDN | `mem:k-devices-one-network.md` |
| L6C | `sn:results/learning/l6_confound.json` |
| L6SC | `mem:l6-sample-count-and-counting-decoder.md` |
| LCC | `sn:LEVELCHECK_CLAIM.md` |
| LCM | `sn:LEVELCHECK_MODEL.md` |
| LDL | `mem:lstv-data-landscape.md` |
| LEARN | `sn:results/learning/LEARNING.md` |
| LFR | `mem:learned-formation-refuted-calibrate-instead.md` |
| LG | `ctsp:morphometrics/level_gradients.csv` |
| LID13 | `mem:level-id-2d-results-2026-09-13.md` |
| LJ | `ctsp:docs/LAB_JOURNAL.md` |
| LM | `ctsp:docs/LEVEL_MORPHOMETRY.md` |
| LMBC | `mem:level-model-bank-coverage.md` |
| LS | `ssn:HANDOFF/LITERATURE_STATE.md`, section given |
| LSB | `ssn:docs/LSTV_BENCHMARK.md` |
| LTDG | `mem:lstv-tltv-detection-goal.md` |
| MAN | `ssn:data_platform/DATA_MANIFEST.md`, the card named |
| MAPI | `ssn:docs/ruleclass/MORPH_API.md` |
| MDD | `ssn:tools/make_drr_dataset.py` |
| MDF | `mem:morphology-deformation-feasibility.md` |
| MLS | `mem:mixed-length-head-and-sota.md` |
| MORPH | `ssn:docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` |
| MP | `ssn:data_platform/MIGRATION_PLAN.md` |
| MPDA | `ctsp:paper/mpda/main.tex` |
| N2 | `ssn:HANDOFF/literature_state/dataset_landscape_by_task.md` |
| N4 | `ssn:HANDOFF/literature_state/power.md` |
| NDI | `mem:nhanes-double-inclusion.md` |
| NIPS | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.tex` |
| NPR | `ctsp:docs/NEXT_PAPER_REFERENCES.md` |
| NUM:n | `sn:NUMBERS.md`, line n |
| OCR | `mem:ostk-canal-closing-regression.md` |
| OM2 | `ostk:ostk/metrics2d.py` |
| OVE | `ctsp:docs/OSTK_VS_EXTRACTION.md` |
| P1S | `sn:PAPER1_SCOPE.md` |
| PAIRED | `ssn:docs/research_paired_ct_projection_verified_2026-09-21.json` |
| PAN | `mem:panjabi-1991-page-892.md`; `<laptop:Desktop>/PANJABI_1991_FULL.pdf` |
| PAS | `ssn:docs/PRIOR_ART_SYNTHETIC_AND_SELF_TRAINING.md` |
| PIR | `mem:ct-volumes-are-pir-not-ras.md` |
| PIS | `ssn:docs/PATIENT_IDENTITY_SPEC.md` |
| PJ | `sn:results/power/power.json` |
| PLAN | `ssn:docs/CT_LSTV_CLASSIFIER_PLAN.md` |
| PLDA | `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` |
| POS | `sn:lit/ct_lstv_classifier/positives_census.md` |
| PPD | `mem:polypose-decision.md` |
| PRER | `ssn:docs/ruleclass/PREREG_rules.md` |
| PREV | `sn:lit/ct_lstv_classifier/lit_prevalence_and_definitions.md` |
| PS24 | `mem:paper-split-2026-09-24.md` |
| PSF | `mem:prone-supine-flexibility-future.md` |
| RAF | `mem:rigor-audit-findings.md` |
| RC22 | `mem:anomaly-rule-rc22-evaluated.md` |
| RDO | `ssn:tools/render_drr_overlay.py` |
| REPRO | `ctsp:paper/mpda/REPRODUCE.md` |
| RES | `sn:sections/results.tex` |
| REVT | `ssn:docs/REVIEW_TRANSITIONAL.md` |
| RF18 | `ssn:docs/research_registration_free_2026-09-18.json` |
| RF22 | `ssn:docs/research_registration_free_search_2026-09-22.md` |
| RFP | `mem:registration-free-prior-art.md` |
| RHR | `mem:recurrent-head-restored-2026-09-16.md` |
| RLC | `ctsp:docs/RELEASE_CHECKLIST.md` |
| RPD | `ssn:tools/render_physics_drr.py` |
| RR17 | `mem:remedies-refuted-2026-09-17.md` |
| RS2 | `sn:REVIEW2_STATS.md` |
| RSP | `ssn:research_notes/spine synthesis prior art/registration.md` |
| SBM | `ctsp:docs/SPINEPS_BENCHMARK.md` |
| SEP | `ctsp:scripts/test_morphometric_separability.py` |
| SM | `ctsp:morphometrics/surgical_morphometrics.csv` |
| SPE | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` |
| SPH | `mem:selective-prediction-the-honest-99.md` |
| SPID | `mem:spineps-ids-can-be-scrambled.md` |
| SPLT | `sn:results/rare_class/split_plan.md` |
| SRE | `mem:synthetic-real-ratio-evidence.md` |
| SRM | `ssn:docs/research_sim_real_mixing_verified_2026-09-21.json` |
| STC | `mem:stc-does-not-transfer.md` |
| STUMP | `ssn:docs/ruleclass/STUMP_RULE.md` |
| SWP | `mem:sweep-map-replaces-registration.md` |
| SXS | `ssn:docs/data_requests/SX-Stitch_request.md` |
| SYN | `ssn:reports/Synthetic real ratio X-ray detectors.md` |
| T3 | `sn:tables/tab3_naming.md` |
| TAB3 | `sn:tables/tab3_naming.md`, the same file as T3 |
| TAB2 | `sn:tables/tab4_transitional.md` |
| TIERS | `ssn:docs/ruleclass/TIERS.md` |
| TLJ | `sn:lit/ct_lstv_classifier/lit_tl_junction_and_enumeration.md` |
| TM | `ctsp:morphometrics/transition_morphometrics.csv` |
| TMT | `mem:two-mechanisms-thesis.md` |
| TSB | `mem:ts-bench-inside-v9-bank.md` |
| TSS | `mem:ts-sacrum-excludes-s1.md` |
| VF8 | `mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` |
| VFT | `mem:versefusion-t13-flag-wrong.md` |
| XDU | `ssn:docs/XRAY_DATASET_USAGE.md` |


Glossary, twelve lines for a first-week reader. Fuller definitions are in `GLOSSARY.md`.

| term | meaning and where it is defined |
|---|---|
| G3 split | the person-disjoint split of 2026-09-23, ordinary 80/10/10 and transitional 50/10/40; `GLOSSARY.md` "G3 split"; SPLT |
| G0 to G7 | the gates of the flagship programme, from data complete to manuscript; `GLOSSARY.md` "G0-G7"; FP lines 57 to 64 |
| paper 1 and paper 2 | paper 1 is SchwingNet's five-figure manuscript and scores no G3 test transitional person; paper 2 is the LevelCheck and surgeon comparison; PS24; P1S |
| "H1 seen" | the entry paper 2's ledger must carry before any G3 test transitional person is scored; PS24 lines 24 to 26 state the rule for H6 as "H6 seen", and the H1 wording is this document's counterpart, not on disk |
| the ledger | `sn:CLAIMS_LEDGER.md`, where every quoted claim carries its file and its gate verdict; CL |
| eval_gate | `ssn:tools/eval_gate.py`, which refuses to score a seen or unresolved item and stamps every result; ACC section 5.3; `GLOSSARY.md` "the gate" |
| alphabet | the set of level names a frame may use, ordinary, L6, T13 or both, chosen from the classifier posteriors and the count; ACP; `GLOSSARY.md` "coupling, alphabet, stop signal" |
| State C | the label-defined unanchored condition: no labelled anchor such as the sacrum in the window, so no count is possible; FCM line 18 |
| physics_rare | the render bank of 1,482 physics-based cone-beam renders of 34 CTSP ids and 47 VerSe series; MAN physics_rare line 2643; `GLOSSARY.md` "*_drr render banks" |
| Dataset803 | the nnU-Net pelvic pseudolabeller, sacrum and hips, used to put a sacrum label on CTs that have none; `GLOSSARY.md` "Dataset803 / 810 / 813 / 815" |
| the review tree | per-flagged-CT case folders for the two-stage human read; REVT; `GLOSSARY.md` "review tree" |
| reqp, RTK | `reqp` is the preemptible CPU partition on the grid, used with `--qos=requeue`, CLAUDE "Grid"; RTK is the cone-beam projection geometry COBRA2026 ships with every projection, PRER line 20 |
