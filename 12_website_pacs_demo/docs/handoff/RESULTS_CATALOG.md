# Results catalog

Every result found on disk on 2026-10-08, one row each, grouped by programme and then by question. Built from the six
reader notes in `working_notes/` (which carry fuller tables, every contradiction and every unknown) and checked against
the files they cite. Nothing was re-run.

## How to read a row

**Columns.** `id` | the claim with its number | the file that holds the number | model, bank, split and truth |
the tool and grid job that produced it | status | the manuscript figure or table it feeds.

**Path prefixes.** `ssn:` = `<laptop Desktop>/spinesurg-ct-nnunet/` (private, branch `L6_Class`);
`sn:` = `ssn:SchwingNet/`; `ctsp:` = `<laptop Desktop>/CTSpinoPelvic1K-1/`; `ostk:` =
`<laptop Desktop>/OpenSpineToolkit/`; `mem:` = a memory note, copied in `HANDOFF/context/` (the same thing other files write `context/`; a few notes are in
`HANDOFF/GREG_ONLY/context/`, see `context/INDEX.md`); `~` = grid
HOME `/wsu/home/go/go24/go2432`; `$RS` = grid Ceph `/rs/rs_grp_oschome/go2432`. A file under `~` or `$RS` exists only on
the grid and was not re-verified. `#` after a JSON file is a JSON pointer.

**Status words.**
- CURRENT: printed in the manuscript as last built (SchwingNet grid builds 40483839 review / 40483840 camera-ready,
  2026-09-27, commit 05e05dc) or the standing value in its document.
- CURRENT-SEL: printed, but measured on the split that chose the checkpoint, and labelled so.
- HELD-OUT, NOT QUOTED: passes the evaluation gate, sits in a result file, not in the text.
- SUPERSEDED: replaced by a named later number. Do not quote.
- DISPUTED: two files disagree; the trusted reading is given.
- REFUTED: the hypothesis it supported was tested and failed.
- RECORD ONLY: pre-SchwingNet exploration, kept for history, not quotable.
- NOT RECORDED: the run is known, its result is in no file on the laptop.
- OPEN: a known defect or an unfinished item.

**Rigor marks** (from the 2026-09-22 adversarial rigor audit, `mem:rigor-audit-findings.md`, answered item by item in
`sn:results/RIGOR_FIXES.md`, plus the eval-gate verdicts of `sn:results/eval_gate/EVAL_LEAKS.md`):

| mark | meaning |
|---|---|
| [THR] | threshold-dependent: the operating point was chosen after a result was seen, or tuned on the test split; quote with its curve and its name ("cross-device", never "pre-stated") |
| [SEL-REP] | selective reporting: one of several analyses or cells reported (rigor audit items: `rescore_outline` 1,440 cells; the manifold's three feature spaces) |
| [WRONG-BANK] | the result is attributed to the wrong training bank in a file |
| [LEAK] | trained or selected on a bank with a known leak, or test persons seen |
| [SEL-SPLIT] | scored on the split that selected the checkpoint (not held out) |
| [ONE-SEED] | rests on a single training run |
| [AUTO-TRUTH] | the truth is automatic (two labellers agreeing) or one labeller's read, not a human read |
| [DERIVED] | computed read-only by an agent from committed rows, not by a committed tool |
| [WORDING] | the printed sentence overstates or loosens what the file shows |
| [E] / [X] | an expectation (prior times measured probability) / an extrapolation beyond measured N |

The house rules that produced most marks: nothing is quoted from allspine v2, v6, v7, v8-for-VerSe, `anchor_drr` or
`vindrps` (`sn:NUMBERS.md` rule paragraph); a deliberately absent list is `sn:NUMBERS.md` "Numbers deliberately absent".

**The five files to open before any other** (`working_notes/topic1_schwingnet_carm_results.md` §0):
`sn:NUMBERS.md` (every number ever printed, row by row, with its file; section headings below the first carry old
figure numbers), `sn:numbers_manifest.json` + `sn:generated/numbers_audit.md` (74 keyed numbers and 5 figures the build
reads, with file SHA-256), `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` (per level, domain and angle, 2026-09-27),
`sn:results/eval_gate/EVAL_LEAKS.md` + `sn:results/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` (the held-out audit of
563 quoted numbers and the re-runs), `sn:PAPER1_SCOPE.md` (what paper 1 may report).

---

## Part A. SchwingNet, paper 1 (Radiology: Artificial Intelligence)

Shape of the paper (`sn:main.tex` lines 125-227): Figures 1 phenotypes, 2 embedding, 3 network, 4 one exposure, 5
persons/views/angles; Tables 1 corpus (`tables/tab_corpus.tex`), 2 transitional persons (`tables/tab4_transitional.tex`),
3 naming/counting/coupling (`tables/tab3_naming.tex`). Supplement: Figures S1 flow (`fig2_flow`), S2 corpus manifold
(`figS1`), S3 image formation (`figS2`), S4 which source carries the detector (`figS3`), S5 detection against angle
(`figS4`) (the file names run one below the printed numbers); Tables S1 device terms, S2 detection per device and arm,
S3 corpus by source with age and sex, S4 film N-curve ablation (`sn:supplement.tex`; `sn:NUMBERS.md` lines 23-27).

The model ("the SchwingNet model"; `DATASET_USAGE.md` §1): naming detector `detector_v5z_final` (YOLO11m-pose, conf
0.35); sacrum/vertebra detector `rx_lodo_carmlspine_1024` (YOLO11m on real COBRA2026 Elekta + DeepFluoro frames,
C-ArmLSpine never seen); level encoder `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (ResNet-18, 27 classes);
head `head_allspine_v9_mixed_kmax4_seed0` (BiGRU over 2-9 bodies); for fine-tuned numbers five `v9init_pre` C-ArmLSpine
fold models; count (`tools/count_from_sacrum_eval.py`) and coupling (`tools/alphabet_couple.py`) have no learned
parameters.

C-ArmLSpine truth: two automatic CBCT labellers (TotalSegmentator, SPINEPS+VERIDAH) scored only where they agree: 814 of
910 vertebrae (89.5 %), T11 0/3, T12 6/63; no level truth in the study was set by a human (`ssn:docs/MODEL_CARD.md`
§5.1). PRE truth = the export before the 2026-09-23 repairs (every printed naming number); REP truth = after (in
`cv_v9.json#families/rep:*`, not quoted). Every C-ArmLSpine naming row below therefore carries [AUTO-TRUTH].

### A1. What the level encoder learned (Figure 2), v9 encoder on v9 VAL (the checkpoint-selection split)

All rows: model v9 encoder; split v9 VAL (1,612 of 1,612 persons in v9's validation set, EVAL_LEAKS L5); tools
`sn:tools/figure2.py`, `figure2_analyse.py` (grid `tools/fig2_heldout_embed.py`, `fig2_occlusion_clean.py`); embeddings
grid jobs 40416675 (GPU) and 40416700 (CPU) (`sn:results/learning/LEARNING.md`). Status CURRENT-SEL [SEL-SPLIT], labelled
"checkpoint-selection split" in the text, unless stated.

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A1.1 | nearest crop of another person is the same level: 9,740 of 13,009 (74.9 % [72.2, 77.6]), 1,612 persons; within one level 93.8 % [92.7, 94.9] (cut from text); 2,889 crops of 164 persons in the training keys dropped first | `sn:results/figure2/figure2_metrics.json#nearest_other_person`, `#cleaning` | CURRENT-SEL | Figure 2, Results |
| A1.2 | L6 separates from L5 more than any ordinary pair: silhouette L6/L5 0.35 [0.31, 0.39] (98 crops, 10 persons; leave-person-out 0.34 [0.30, 0.38]); L5/L4 0.23 [0.21, 0.25]; L4/L3 0.17; L3/L2 0.16; L2/L1 0.19; L1/T12 0.32 [0.29, 0.35] | same `#silhouette/pairs/*`, `#heldout_l6/...` | CURRENT-SEL | abstract, Key Point 3, Results |
| A1.3 | classifier calls: 75 of 98 L6 crops named L6; 111 of 1,012 L5 crops named L6 | same `#validation_neighbours_and_calls` | CURRENT-SEL | Results |
| A1.4 | within one render source: VerSe renders 0.52 [0.45, 0.57] vs control 0.38 (10 persons); physics_rare 0.24 [0.20, 0.29] vs 0.16 (8); physics_drr reversed 0.14 [0.11, 0.20] vs 0.21 (5 persons, 11 crops) | same `#silhouette_within_source/sources` | CURRENT-SEL | supplement |
| A1.5 | never-seen L6 (C-ArmLSpine case42, case121, case136): two-cluster silhouette 0.10 / 0.12 / 0.16 vs validation L6 0.34; their L3-L5 -0.09 to -0.01; 84 of 180 crops named L6; under the body box -0.07 and 13 of 180 | same `#heldout_l6`; `sn:figures/figure2.record.json#never_seen` | CURRENT, HELD OUT (EVAL_LEAKS item 5 CLEAN for v9) [AUTO-TRUTH: one labeller's read] | supplement |
| A1.6 | fused L5 (four validation persons): last free vertebra nearer L5 in 2 of 4 (-0.13, -0.18; both named L5); ordinary L4 0.24 (70 of 1,066 below zero); control L3 0.01 and -0.26 | `sn:results/figure2/figure2_transitional.json#fused_L5` | CURRENT-SEL | supplement |
| A1.7 | occlusion: target enrichment 1.39-4.51 over six levels (T12 1.89, L3 2.26, L4 1.69, L5 1.39, L6 1.47, sacrum 4.51); for L4-L6 more attribution on the body below (36-43 %) than on the target (24-32 %) | `sn:results/figure2/zones_lateral_clean.json#sets/v9_val/<level>/maps/occlusion` | CURRENT-SEL | Results |
| A1.8 | no T13 crop in validation: 44 T13 crops in training, 0 in validation | `figure2_metrics.json#bank_transitional_census` | CURRENT (a census) | Results |

### A2. Zero-shot naming on the unseen C-arm (C-ArmLSpine, Surgio-B51)

All rows: v9 encoder + v9 head, no C-ArmLSpine frame in training; naming boxes from `detector_v5z_final` at 0.35; PRE
truth [AUTO-TRUTH]. Files `sn:results/eval_gate/leaks/zeroshot_v9.json` and
`sn:results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:zeroshot_v9_existing`, `#pre:zs_v9head`. Jobs: zs9kfield
40436982, closure re-run 40437081 (`sn:REVISION_LOG2.md` line 340).

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A2.1 | lateral, whole frame: 595 / 617 (96.4 %), 141 cases (6 with an error); Wilson on effective n [92.3, 98.4] (ceiling regime, design effect 3.84); percentile [93.3, 98.9]; BCa [92.5, 98.7]; answered 83.0 %, exact on answered 97.7 % | as above | CURRENT, HELD OUT | Key Point 1, abstract, Results, Table 3 |
| A2.2 | AP, whole frame: 276 / 631 (43.7 %), 142 cases (83 with an error) [34.9, 51.9]; answered 20.9 %, exact on answered 47.0 % | as above | CURRENT, HELD OUT | same |
| A2.3 | lateral minus AP: +54.3 points [45.6, 62.9] on 593 vertebrae of 140 cases; cases 79 : 1; exact sign test p 1.34e-22, Holm 5.4e-22 | `sn:results/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` §4 | CURRENT | abstract, Results |
| A2.4 | lateral with three / one vertebrae in field: 970 / 1,159 (83.7 %) [79.6, 87.5]; 385 / 603 (63.8 %) [59.8, 67.9] | `cv_v9.json` | CURRENT, HELD OUT | Results, Table 3 |
| A2.5 | AP with three / one in field: 391 / 1,176 (33.2 %); 112 / 591 (19.0 %) | `cv_v9.json#families/pre:zs_v9head` | HELD-OUT, NOT QUOTED | — |
| A2.6 | counting the 59 undetected bodies as wrong: 595 / 676 = 88.0 % | Table 3 note b | CURRENT | Table 3 |
| A2.7 | naming detector recall of agreed lateral bodies: 617 / 676 (91.3 %) | `ssn:docs/carmlspine_cv5_mixed_2026-09-21.json`, key `det/LAT/kfull` (`vertebrae` 617, `recall_named` 0.9127) against key `oracle/LAT/kfull` (`vertebrae` 676); the keys are flat strings that contain slashes, not JSON pointers | CURRENT | Results |
| A2.8 | zero-shot AP errors are a one-level cranial shift: L4->L3 x51, L3->L2 x51, L5->L4 x48, L2->L1 x46, L1->T12 x21 | `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` Table C (from `cv_v9.json`) | HELD-OUT, NOT QUOTED [DERIVED] | — |
| A2.9 | first zero-shot run on `allspine_v2_r1`: 594 / 617 (96.3 %), 239 / 631 (37.9 %), +57.7 points | `sn:results/a7.json#cells/zeroshot2~1det~1{LAT,AP}~1kfull`; `ssn:docs/carmlspine_zeroshot2_pooled_all_2026-09-21.json` | SUPERSEDED (UNRESOLVED U1: the encoder's bank was deleted); disclosed only as "first zero-shot run, not used" in Table 3 note h. **Still printed in the stale twin `sn:tables/tab3_naming.md` and in the ATLAS cards `sn:atlas/model.json`, `sn:packet/atlas/model.json`, `sn:packet_cameraready/atlas/model.json`: fix before submission** | — |

### A3. Fine-tuned cross-validation naming on C-ArmLSpine

All rows: `v9init_pre` fold models (same merged fold banks, epochs, seeds and defaults as the shipped folds, encoder
fine-tuned from v9 instead of `allspine_v2_r1`); case-grouped five folds (`md5(case) % 5`) or acquisition-day-grouped
three folds (66 / 43 / 40 cases, `sn:results/carmlspine_day_groups.json`); PRE truth [AUTO-TRUTH]. File
`sn:results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:cv5_det/...`, `#pre:cvday_det/...`; paired contrasts
`cv_v9_extras_pre.json#pairs`. Jobs `carmcv9i` 40431706, closure 40436862 (after the `min_det_conf` fix), extras 40436901
(`sn:results/eval_gate/closure/cv_v9/CV_V9.md`). **The fold banks behind every row were built from `allspine_v7` and
hold 2,632 VinDr crops, 2,100 FluoroCap crops and both NHANES copies** (`ssn:docs/MODEL_CARD.md` §3.2;
`DATASET_USAGE.md` §3): no quoted number scores NHANES with them, but the composition breaks directive D1 and the IRB
scope. Settled by Greg on 2026-10-14: every dataset is permitted, its data use agreement filed, so these rows may
be quoted; FluoroCap still stays out of new training (root CLAUDE.md rule 9).

| id | claim | status | feeds |
|---|---|---|---|
| A3.1 | lateral whole frame, case-grouped: 601 / 617 (97.4 %), 141 cases (4 with an error); Wilson [93.2, 99.0]; BCa [93.2, 99.4]; answered 503 / 617 (81.5 %), exact on answered 497 / 503 (98.8 %) | CURRENT, HELD OUT | abstract, Results, Table 3 |
| A3.2 | AP whole frame, case-grouped: 608 / 631 (96.4 %), 142 cases (7); Wilson [92.5, 98.3] | CURRENT, HELD OUT | Key Point 2, abstract, Results, Table 3 |
| A3.3 | lateral three / one in field: 1,079 / 1,159 (93.1 %) [89.2, 96.2]; 451 / 603 (74.8 %) [70.9, 78.7] | CURRENT | Key Point 2, Results, Table 3 |
| A3.4 | AP three / one in field: 1,005 / 1,176 (85.5 %); 399 / 591 (67.5 %) | CURRENT | Table 3 |
| A3.5 | day-grouped whole frame: lateral 568 / 617 (92.1 %) [87.5, 96.0]; AP 598 / 631 (94.8 %) Wilson [90.1, 97.3] | CURRENT | Results, Table 3, limitations ("below zero-shot") |
| A3.6 | day-grouped three in field: lateral 1,016 / 1,159 (87.7 %); AP 1,011 / 1,176 (86.0 %) | CURRENT | Table 3 |
| A3.7 | paired, lateral: case-grouped minus zero-shot +1.0 point [-1.9, 4.0], cases 4 : 2, p .69; day-grouped minus zero-shot -4.4 [-9.1, 0.2], 4 : 10, p .18; case minus day +5.3 [2.1, 9.1], 8 : 0, p .008 (last not printed) | CURRENT (first two) | Results |
| A3.8 | paired, AP: case-grouped minus zero-shot +52.6 [44.1, 61.3], 78 : 2 | CURRENT | Results |
| A3.9 | per level, lateral whole frame (case-grouped): L1 97.4 (n 76), L2 96.8 (123), L3 97.2 (141), L4 97.2 (141), L5 98.5 (136); AP 95.5-97.7; one in field L1 41.2 % lateral / 9.5 % AP is the weakest cell, L4-L5 84-86 % | `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` Table C | HELD-OUT, NOT QUOTED [DERIVED]; a supplement Table S5 from `cv_v9.json` through `\RESULT` keys awaits Greg's yes/no | (proposed S5) |
| A3.10 | reading recorded: lateral naming is saturated before any same-device frame is seen; AP is a coverage hole the device's own frames fill; on the lateral view a held-out acquisition day reads below never seeing the device, -4.4 points [-9.1, +0.2], 4 : 10 cases, p .18 (A3.7), an interval that includes zero; on AP the day-grouped model is about 51 points above zero-shot (94.8 % day-grouped, A3.5, against 43.7 % zero-shot, A2.2); same-device data helps most at one body in field (+10.9 [+6.4, +15.5]) | `MANUSCRIPT_CORRECTIONS.md` §8 | CURRENT reading [WORDING]: the file's "worse than never seeing the device" holds only as a lateral point estimate | Discussion |
| A3.11 | v2-lineage CV: lateral 606 / 617 (98.2 %), AP 96.7 %, k5 97.0, k3 92.9, k1 72.8 | `ssn:docs/carmlspine_cv5_mixed_2026-09-21.json` | SUPERSEDED (UNRESOLVED U1). Still in `sn:tables/tab3_naming.md` twin and the ATLAS cards | — |

### A4. Counting from the detected sacrum (no classifier)

Tool `ssn:tools/count_from_sacrum_eval.py` (self-test with synthetic frames), runner `sn:slurm/counting.sh`, report
`sn:tools/counting_report.py`; final job 40416281 (2026-09-23 01:01, 21 cells, outside check against `a1.json` PASS)
(`sn:results/JOBS.txt`). File `sn:results/counting.json`, per frame `sn:results/counting/*.json`. Detector
`rx_lodo_carmlspine_1024` (C-ArmLSpine never seen). The 0.74 operating point is "cross-device" [THR]: the best pooled
F1 of the `lodo_carm` arm over COBRA2026, DeepFluoro and the Geneva phantom, adopted as headline after the 0.25 result
was seen (`sn:results/a1.json#operating_points`; `sn:CLAIMS_LEDGER.md` §1 row 1).

| id | claim | status | feeds |
|---|---|---|---|
| A4.1 | C-ArmLSpine test (28 cases, 56 frames) at 0.74, outline boxes: counting defined 46 / 56 (82.1 %) [69.6, 92.9]; detected sacrum true 43 / 46; ordinal correct 188 / 197 matched (95.4 %) [89.4, 99.5]; within one 197 / 197; truth bodies right over defined frames 188 / 232 (81.0 %) [73.8, 87.6] | CURRENT, HELD OUT [THR] | abstract, Discussion, Table 3 |
| A4.2 | same at 0.25: defined 51 / 56; ordinal correct 199 / 235 (84.7 %) [77.4, 90.7]; within one 225 / 235 | CURRENT | Table 3 |
| A4.3 | misses by ordinal: 25 of 35 missed bodies at ordinals 5-6; 16 within 6 px of the frame border | `sn:results/fig5_naming_data.json#b` | printed in an earlier revision only | — |
| A4.4 | COBRA2026 test at 0.25: defined 111 / 609 (18.2 %); ordinal correct 54 / 76 (71.1 %) [56.6, 80.3] | CURRENT | Table 3 |
| A4.5 | DeepFluoro test specimen at 0.25: 53 / 67 (79.1 %), one cluster, no interval | twin only | — |
| A4.6 | pooled over three held-out devices at 0.25: defined 252 / 755 (33.4 %); ordinal correct 306 / 378 (81.0 %) [75.7, 85.8]; within one 366 / 378 | CURRENT | Table 3 |
| A4.7 | count alone on anchored fold frames at 0.74: 979 / 1,009 (97.0 %) [94.2, 99.2], 130 cases (no encoder, so unchanged by the v9 re-run) | CURRENT | Key Point 2, abstract, Results |

### A5. Coupling and the stop signal

File `sn:results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` (v9init_pre folds; gate HELD OUT, 420 checks);
coupler `ssn:tools/alphabet_couple.py`, runner `sn:slurm/coupling.sh`, collector job 40436581 (`sn:REVISION_LOG2.md`
line 214); posteriors from `tools/level_prototype.py --dump-posterior --sacrum-detector`. 290 frames / 145 cases with
agreed truth; 233 anchored at 0.74 [AUTO-TRUTH].

| id | claim | status | feeds |
|---|---|---|---|
| A5.1 | on 1,009 counted bodies at 0.74: classifier 986 (97.7 %) [95.9, 99.2]; count 979 (97.0 %) [94.2, 99.2]; coupled 991 (98.2 %) [96.5, 99.5] | CURRENT, HELD OUT | Key Point 2, abstract, Results, Table 3 |
| A5.2 | coupled minus count +1.2 points [0.0, 3.2]; minus classifier +0.5 [-1.5, 2.4] | CURRENT | Results, Table 3 |
| A5.3 | disagreement frames 13 / 233 (5.6 %) [2.6, 9.2]; stop on 23 / 233 (9.9 %) [5.7, 14.5] (13 disagreement + 10 low margin); catches 5 of 6 erring frames | CURRENT | Results, Table 3 |
| A5.4 | L6 calls on 3 of 233 anchored frames (case139 AP + LAT, case44 LAT), all stopped; coupled exact on their 12 bodies 12 / 12, count 0 / 12 | CURRENT | Results, Table 3 |
| A5.5 | the three one-labeller L6 patients: 6 frames, 4 anchored, one L6 call (case42 LAT, flagged); classifier 0 / 5, coupled 1 / 5 on the five bodies one labeller reads L6 (agreement, not correctness) | CURRENT [AUTO-TRUTH] | Results, Table 3, Figure 4d |
| A5.6 | at 0.25 (266 anchored, 1,149 bodies): classifier 1,122 (97.7 %); count 1,104 (96.1 %); coupled 1,116 (97.1 %); disagreement 19 / 266 | CURRENT | Table 3 |
| A5.7 | v2-lineage coupling (993 / 995 of 1,009; 12 / 233 disagreement; 4 of 5 flagged; 921 / 922 unflagged); oracle-box rows 94.7 / 97.7 / 95.9 % of 1,329 | `sn:results/coupling.json` | SUPERSEDED (U1); oracle rows twin only | — |

### A6. Detection on the held-out device (Table S2, Results)

Arm `lodo_carm` (`rx_lodo_carmlspine_1024`): trained on COBRA Elekta + DeepFluoro real frames; C-ArmLSpine test 56 frames
/ 28 cases / 287 vertebrae / 56 sacra; outline truth; IoU 0.5. File `sn:results/a1.json` (`ssn:tools/rigor_fixes.py`, code
6e1cf8d; RIGOR_CHAIN jobs gpu 40415602, cpu 40415603/04/14/26/32, cvday 40415610, pool 40415625, `sn:results/JOBS.txt`;
report `sn:results/RIGOR_FIXES.md`).

| id | claim | status | feeds |
|---|---|---|---|
| A6.1 | vertebra / sacrum recall at 0.74: 231 / 287 (80.5 %) [74.1, 86.8]; 43 / 56 (76.8 %) [64.3, 89.3]; "short of the pre-stated 97 %" | CURRENT, HELD OUT [THR] | Results, Table S2 |
| A6.2 | at 0.25: 260 / 287 (90.6 %), Wilson on effective n [84.3, 94.5]; sacrum 47 / 56 (83.9 %) [73.2, 92.9] | CURRENT | Table S2 |
| A6.3 | at 0.60 (own best F1, tuned on the test split, a bound only): 250 / 287 (87.1 %); sacrum 45 / 56 (80.4 %) | in `a1.json`, not a headline [THR] | — |
| A6.4 | recall against confidence, 17 thresholds: 0.01 -> 92.7 %, 0.74 -> 80.5 %, 0.80 -> 67.9 %, 0.90 -> 0.0 % (answers rigor item A1) | `sn:results/RIGOR_FIXES.md` A1 | CURRENT | supplement |
| A6.5 | on the repaired denominator: 201 / 214 (93.9 %) [90.4, 97.1]; re-scored on the rebuilt truth the released denominator reads 236 / 287 (the text's 231 / 287 was scored before the 05:22 rebuild) | `sn:results/indomain/denominator_repair.json` (job 40448892) | CURRENT (both printed) | Results, supplement |
| A6.6 | sacrum anchored on fold frames at 0.74: 233 of the 286 frames showing a sacrum (81.5 %) (supersedes 233 of 290, 80.3 %: four frames have no truth sacrum) | `sn:REVIEW2_STATS.md` N15 | CURRENT | Results |
| A6.7 | same-device control minus held-out, sacrum at 0.25: 98.2 % vs 83.9 %, +14.3 points [5.4, 23.2]; sign test 8 : 0; Holm P = .009 | `sn:results/a3.json#comparisons/pooled_vs_heldout_detector` | CURRENT | supplement |
| A6.8 | same-device controls on C-ArmLSpine under the outline rule: real-only 40.4 / 41.5 %, pooled real 40.1 / 40.8 % at 0.74 / 0.25 (a box-convention artefact); under the body rule 89.9 % (258 / 287) and 90.6 % (260 / 287) | `sn:results/lcurve/lcurve.json#devices/surgio_b51_dr/all_real[]` | CURRENT | Table S2 |
| A6.9 | COBRA2026 held out (Elekta never seen): 6.2 % (55 / 893) at 0.74, 18.5 % (165 / 893) at 0.25; sacrum 21 / 609 at 0.74 | `a1.json` | CURRENT | Table S2 |
| A6.10 | DeepFluoro test specimen held out: 74.7 % (62 / 83) at 0.74, 95.2 % at 0.25, sacrum 90 / 90 (one cluster) | `a1.json` | CURRENT | Table S2 |
| A6.11 | design B (styled renders of the other two devices + their real frames): C-ArmLSpine 63.1 % (181 / 287) at 0.74, 87.8 % at 0.25; COBRA 10.1 / 32.7 %; DeepFluoro 69.9 / 94.0 % | `a1.json` | CURRENT | Table S2 |
| A6.12 | renders only: C-ArmLSpine 0.3 % (1 / 287) at 0.74, 31.7 % (91 / 287) at 0.25 | `a1.json` | CURRENT | supplement, Table S2 |
| A6.13 | the pre-stated counting-grade target (>= 97 % vertebra and sacrum, `ssn:docs/RSNAI_PLAN.md` C7) is not met by any held-out cell; `ssn:docs/MODEL_CARD.md` §4.6 writes "not met on two of the three devices" although its own Cios row (91.6-94.0 %) is also below 97 %; the primary C7 criterion (paired bootstrap against the LODO baseline) was never run | `MODEL_CARD.md` §4.6 | CURRENT (not met) [WORDING in MODEL_CARD] | Results |

### A7. Which training source carries detection (Figure S4)

File `sn:results/contribution_matrix.json` (`sn:tools/contribution_matrix.py`; grid jobs 40415588 and rerun 40415691; 24
arms, 85 held-out cells, self-check max |difference| 0.0000; conf 0.25, outline). The prose in
`sn:results/DATA_CONTRIBUTION.md` predates the rerun; **the JSON is authoritative** (its preamble lists nine corrections).

| id | claim | status | feeds |
|---|---|---|---|
| A7.1 | radiotherapy imager (Elekta, E) frames alone -> C-ArmLSpine: 86.8 % (249 / 287) [81.1, 91.8] (body rule 11.1 %) | CURRENT, HELD OUT | Results (`\RESULT{a3_e_only_carm_pct}`), Figure S4 |
| A7.2 | cadaver C-arm (Cios / DeepFluoro, D) alone -> C-ArmLSpine: 12.9 % (37 / 287) [8.3, 18.1] (body 3.8 %) | CURRENT | Results, Figure S4 |
| A7.3 | adding E to D +71.8 points [63.4, 79.6] (seed 1 +67.6 [57.6, 76.8]); adding D to E -2.1 [-6.0, +1.4] (seed 1 -6.3 [-9.8, -2.9]) | CURRENT | Results, supplement |
| A7.4 | cutting E's real frames 2,640 -> 240: -47.7 points [-53.7, -41.8] (body -8.0, no paired interval) | CURRENT | supplement |
| A7.5 | COBRA held out: add D to S +18.0 ... +23.9; add S to D -7.8 [-12.5, -3.9] | CURRENT | supplement |
| A7.6 | seed spread on multi-cluster held-out cells 1.1-5.6 points (7.3 under body) | CURRENT | supplement |
| A7.7 | no arm isolates angle: E differs from D in device, anatomy (110 patients vs 4 specimens), frame count and angle together | `sn:CLAIMS_LEDGER.md` §1 (REWRITE verdict F13) | CURRENT caution | Discussion |
| A7.8 | renders plus other devices' real frames (design B) hurt on the C-arm at 0.74 (63.1 [54.8, 71.0] vs real-only 80.5) and help on the Elekta kV imager (32.7 vs 18.5 at 0.25) | `PER_LEVEL_DOMAIN_ANGLE.md` Table G | HELD-OUT reading | — |

### A8. Same-device detection learning curve and its plateau (Figure 5c)

Files `sn:results/indomain/det_fill.json` (jobs named in the file: 40425531/32, 40427581, 40429284, 40449438; lcfill array
40429442_0-5, collect lcfcoll 40436400 COMPLETED 2026-09-24 08:07 per `sn:results/coverage/PENDING_JOBS.json`),
`sn:results/lcurve/lcurve.json`, `sn:results/indomain/{INVENTORY,INDOMAIN,FIT_N}.md`, `fit.json`. Tools
`ssn:tools/lcurve_fill.py`, `lcurve_train.py`, `lcurve_score.py`, `indomain_fit.py`, `indomain_fit_docs.py`,
`indomain_fit_N.py`. Test = the released 28-patient test split, repaired truth (LAT 27 patients / 138 vertebrae, AP 28 /
143); body rule at 0.74 is the reported convention.

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A8.1 | no frame of the device (stage 2: own-geometry styled renders + other C-arms): 7.0 % (20 / 287) [4.2, 10.1] body at 0.74; stage 1 alone 12.5 % (36 / 287); N = 0 floor is a box-convention artefact (whole-vertebra boxes scored as misses) | `det_fill.json`; `INDOMAIN.md` §2 | CURRENT, HELD OUT | Results, supplement |
| A8.2 | body at 0.74, both views pooled: N 0 7.7 % (66 / 861), 4 72.4 %, 10 76.0 %, 24 84.0 % (723 / 861), 50 82.5 %; at N = 24 lateral 84.1 %, AP 84.6 % | `FIT_N.md`; `sn:results/power/power.json#panel_c_detection/curves` | CURRENT | Figure 5c, Results |
| A8.3 | 50-210 frames read 81.5-86.8 % (234-249 / 287); every interval from 50 frames up overlaps | `lcurve.json` | CURRENT | supplement |
| A8.4 | one-view arms (25 or 50 frames, two seeds): own view 83.0-86.4 %; the other view 0.0-39.5 % | `power.json#panel_c_detection/summary` | CURRENT | Results, supplement |
| A8.5 | model-free plateau check (body at 0.74): N 24 vs N 200 lateral +2.2 [-1.1, +6.0], AP +1.7 [0.0, 3.8] | `INDOMAIN.md` §2 | HELD-OUT, NOT QUOTED | — |
| A8.6 | in-domain frames vs substitutes at N = 24 (centre rule, 0.74): lateral +28.5 points over COBRA frames, +15.7 over styled renders; AP +20.7 / +27.0 | `INDOMAIN.md` §3 | HELD-OUT, NOT QUOTED | — |
| A8.7 | **the plateau is the truth denominator**: 30 of 287 missed by all ten plateau arms, 208 hit by all; CBCT-cut vertebrae missed 51.5 % of the time vs 6.7 % for complete ones; on complete, agreed, SPINEPS-boxed bodies (204 of 287) the arms read 96.9 %; on the repaired denominator N 24 reads 95.6 % [92.9, 98.0] (614 / 642), N 200 94.9 % [91.3, 97.9] (406 / 428) | `sn:results/indomain/miss_diagnostic/MISS_DIAGNOSTIC.md` (job 40448862, `ssn:tools/carm_miss_diagnostic.py`); `denominator_repair.json#summary` (job 40448892, `ssn:tools/carm_denominator_repair.py`) | CURRENT; the text change it implies was left for Greg ("NOT yet applied", `sn:REVISION_LOG3.md` §11). `mem:carm-plateau-is-the-denominator.md` uses 204 / 96.9 %; the repair uses 214 (different rules) | Results, supplement |
| A8.8 | asymptote fits (inverse power law, 2,000 case-clustered resamples): lateral 81.7 % [76.7, 86.6], AP 85.3 % [81.0, 90.7]; 95 % of the asymptote at 10.0 [5.1, 23.5] lateral and 11.9 [6.7, 33.5] AP frames; 90 % absolute recall "not reached" in 100 % / 96 % of resamples; at 0.25 asymptotes 92.3 / 93.9 % lateral / AP by the centre rule (`det_carm_*_centre025`), 91.3 / 93.8 % by the body rule, the reported convention (`det_carm_*_body025`) (`sn:results/indomain/FIT_N.md` L23-26); detection lateral centre at 0.74 0.825 [0.781, 0.871]; same-device naming asymptotes NOT identified at 87 persons | `FIT_N.md`; `fit.json` (11:59, n_boot 2,000) | HELD-OUT, NOT QUOTED. `INDOMAIN.md` (10:43, 10 resamples, "no interval") is stale against `fit.json` | — |
| A8.9 | caveat: the device's styled renders were posed on the registered geometry of all 148 cases, test cases included | `INVENTORY.md` "Pose donors" | CURRENT caveat | supplement |
| A8.10 | the earlier real-frame learning curve (`lcurve`, 2026-09-23): C-ArmLSpine body at 0.74 N 0 7.3 %, ~50 81.5 %, ~100 81.5 / 80.5 %, ~200 80.1 / 82.2 %, all real 81.9 % (210 frames); COBRA Elekta 12.9 -> 93.2 % (2,640 frames; the body-truth figures are a box-convention mismatch); DeepFluoro one specimen, not monotone; C-ArmLSpine transitional row 74.3 % (26 / 35) from N = 50, three clusters | `sn:results/lcurve/lcurve.md` (prep 40416377, array 40416378_0-18, report 40416379) | CURRENT in supplement; superseded for Figure 5 by A8.2 | supplement |

### A9. C-arm naming against training persons, by view (Figure 5b, C-arm)

File `sn:results/indomain/name_fill.json#figure5b` (`ssn:tools/indomain_name_fill.py collect`, 2026-09-24T08:36:19; arrays
namefill 40429416 and 40429901, retry namefillr 40436049_0-9; 250 / 250 cells; runners `sn:slurm/name_fill*.sh`;
per-case rows `sn:results/indomain/fit/name_percase.json`, job 40436856). Fine-tunes of the v9 encoder per cell
(recipe `ssn:slurm/carmlspine_cv_v9.sh`); REP truth (623 LAT / 633 AP vertebrae) [AUTO-TRUTH]; three seeds at small N.
Printed through `\RESULT{name_carm_*}`.

| id | claim | status | feeds |
|---|---|---|---|
| A9.1 | lateral protocol, whole frame: N 0 93.7 %, 5 96.7, 10 96.5, 25 97.5, 50 98.1, all 98.1 % | CURRENT, HELD OUT | Figure 5b, Results |
| A9.2 | AP protocol, whole frame: 33.8 -> 90.8 (5 persons) -> 94.7 -> 95.4 -> 95.4 -> 98.1 % (all, 84-96 per fold) | CURRENT | Figure 5b |
| A9.3 | lateral-trained, read on AP: 32.2 -> 54.7 % (all persons) | CURRENT | Results |
| A9.4 | both protocols trained, all persons: lateral 98.1 %, AP 97.0 % | CURRENT | Results |
| A9.5 | narrow fields: AP three in view 28.5 -> 87.6 %, one in view 15.7 -> 74.6 %; lateral three 83.6 -> 93.1, one 63.9 -> 77.1 %; still rising at 88 persons, asymptotes not identified | `INDOMAIN.md` §5, §8 | HELD-OUT, NOT QUOTED | — |
| A9.6 | substitutes at the same person count (AP whole frame): same-protocol plain films 80.6 -> 96.4 %; CT renders 26.2 -> 53.7 %, vs in-domain 90.8 -> 98.1 %; exchange rate (substitute persons per in-domain person) film 3.6 at N 5, 1.7 at 25, 1.2 at 50; renders "millions" [X] | `INDOMAIN.md` §6 | HELD-OUT, NOT QUOTED | — |
| A9.7 | collection guidance from the fits: about 12 patients (24 frames, both views) of a device for detection; whole-frame AP naming 68 persons for 97 %, 1,071 for 99 % [X]; for collimated fields keep collecting | `INDOMAIN.md` §8 | not quoted | — |
| A9.8 | zero-shot references on REP truth: lateral 96.3 % (600 / 623), AP 43.9 % (278 / 633) | `INDOMAIN.md` §5 | HELD-OUT, NOT QUOTED (same model as A2.1 on REP truth) | — |

### A10. Plain-film naming against training persons, and the render ablation (Figure 5b film, Table S4, Discussion)

Film N-curve: `sn:results/coverage/film_ncurve/film_ncurve.json` + `FILM_NCURVE.md` (2026-09-24T23:25:30, 48 of 48 cells;
`ssn:tools/film_ncurve.py`). Encoder: a new render-only encoder (the v9 bank minus every film row: physics_drr,
physics_rare, ctsp_drr, verse_drr; 47,976 train / 9,036 val crops; ImageNet start, v9 recipe; own val exact 0.664)
fine-tuned per cell on N persons of one corpus merged 1:1 with the render bank's per-class-600 sample (15 epochs), then
`head_mixed_length --train-mode mixed`; TEST = the v9 VAL persons of that corpus (never trained or selected on by any cell
or by this encoder); scoring `tools/rigor_fixes.py a5-rows` with `tools/eval_gate.py` first; every cell "HELD OUT".
Seeds 0-2 at N <= 25, **seed 0 only above** [ONE-SEED above N = 25]. Chain fnprep 40437808 -> fnenc 40437809 -> fncell
40437810 (array 0-47%16) -> fncoll 40437811 (`sn:results/coverage/PENDING_JOBS.json#chains/film_ncurve`).

| id | claim | status | feeds |
|---|---|---|---|
| A10.1 | NHANES II exact level, persons N = 0 / 5 / 10 / 25 / 50 / 100 / 200 / all: 27.2 / 77.8 / 82.3 / 87.8 / 89.2 / 89.6 / 92.5 / 92.7 % (264 persons) | CURRENT, HELD OUT | Figure 5b, Results |
| A10.2 | BUU-LSPINE: 10.3 / 65.0 / 70.3 / 76.7 / 81.2 / 82.7 / 85.1 / 96.9 % (2,967) | CURRENT, HELD OUT | Figure 5b |
| A10.3 | CSXA: 3.2 / 94.2 / 93.0 / 96.4 / 97.3 / 97.3 / 98.0 / 99.8 % (4,114) | CURRENT, HELD OUT | Figure 5b |
| A10.4 | cross-corpus transfer peaks at 74.3 % (NHANES -> CSXA at N = 200, 749 films); NHANES-trained 73.2 % on BUU (all); BUU <-> CSXA <= 12.6 %; CSXA -> NHANES <= 43.7 % | CURRENT | Results (`\RESULT{film_transfer_*}`) |
| A10.5 | pooled-fit asymptotes: NHANES 95.9 % (all point 3.2 below), BUU 100 % (3.1 below), CSXA 100 % (reached) | `sn:results/coverage/pooled_fit.json#admissibility` | HELD-OUT, NOT QUOTED | — |
| A10.6 | **ablation** (Greg 2026-09-25: "if renders are my only source of rare classes they have to be included right? run this test"): render-only minus film-only at N = 5: NHANES +21.9, BUU +11.1, CSXA +18.7 points, every seed separated | `sn:results/coverage/film_ncurve/ablation/READ.md`, `ablation_read.json` (reader `sn:tools/film_ncurve_ablation_read.py`, 2026-09-27 13:07); arrays 40451157 (imagenet, 48 / 48), 40451158 (filmonly, 39 / 48: every cell but N = 0), collects 40451159 / 40451160; reading rule stated before the numbers in `sn:REVISION_LOG3.md` §13 | CURRENT, HELD OUT | Discussion, Table S4 |
| A10.7 | at N = 25: +12.2, +6.0, +6.2, every seed separated | same | CURRENT | Table S4 |
| A10.8 | at every person: NHANES +0.7 (level), CSXA -0.2 (level), **BUU -1.6, separated: renders hurt** (96.9 [96.0, 97.8] vs 98.5 [98.0, 99.0]) | same | CURRENT [ONE-SEED] | Discussion ("one corpus 1.6 points the other way"), Table S4 |
| A10.9 | seven of nine verdict cells separated: six help, one hurts | same | **DISPUTED**: `mem:film-ncurve-ablation-result.md` and `sn:REVISION_LOG3.md` §13 say "all help"; trust `READ.md` (tool output). The Discussion sentence (`sn:sections/discussion_motivation.tex` L53-56) places "7 of 9 cells" inside "five to twenty-five persons", where only six verdict cells lie [WORDING]; wording is Greg's call | Discussion |
| A10.10 | ImageNet init on the same merged bank sits between (NHANES N = 5: 75.5 vs 77.8 render-only vs 55.9 film-only); most of the scarce-N gain is the render rows, 2-5 points is the pretraining; at 50 persons NHANES and CSXA still separate (+7.7, +2.9); at 100 and 200 persons nothing separates; at every person BUU separates the other way (renders hurt, A10.8; `sn:results/coverage/film_ncurve/ablation/READ.md`) | same | CURRENT | Table S4 |
| A10.11 | the synthetic:real ratio was ~1 : 1 by rows in every cell (`ssn:tools/merge_banks.py` line 60, `real_share` 0.5; 15,374 render rows per cell) while the distinct-image ratio ran 615 : 1 (BUU / CSXA N = 5) to 0.75 : 1 (CSXA all); **never swept** | `PER_LEVEL_DOMAIN_ANGLE.md` Table A | CURRENT fact | — |
| A10.12 | do not plot the N-curve endpoints (92.7 / 96.9 / 99.8) beside the a5 film numbers (99.1 / 97.3 / 99.8): different encoders on different splits | `PER_LEVEL_DOMAIN_ANGLE.md` Table D note | rule | — |

### A11. Angle, acquisition-space coverage and the pooled fit (Figure 5d, Figure S5)

| id | claim | file | tool / job | status | feeds |
|---|---|---|---|---|---|
| A11.1 | matched-N render-only detectors, Surgio card, 2,646 renders of 125 subjects, conf 0.25, scored on 40 unseen TotalSegmentator subjects over 19 lateral bins: `low` (AP+LAT real-pool poses) 82.1 % at trained angles, 52.8 % over 16 untrained bins, 57.4 % all; `low2n` (twice the frames, same poses) 94.2 / 64.8 / 69.5 %; `high` (arc poses) 80.7 / 77.1 / 77.7 % | `sn:results/power/power.json#panel_d_angle/summary`; `sn:results/coverage/experiment/EXPERIMENT.md`, `scores.json`, `runs/*/unseen/recall_vs_angle.json` | `ssn:tools/coverage_arms.py`; covrender 40437812 (array 0-3) -> covarm 40437813 (array 0-11) -> covcoll 40437814; rescore covscore 40443105, covcoll2 40443106 | CURRENT (on renders); caveat: the Surgio card renders thick laterals photon-starved, so the +/-90 degree bins mix geometry with underexposure (`power.json#panel_d_angle/exposure_caveat`) | Results, Figure 5d |
| A11.2 | Elekta XVI arms printed "scored zero"; `EXPERIMENT.md` shows 0.0 for four arms and 1.6 % / 0.4 % for the two low2n seeds; the pooled fit treats all six as 0.0 | `EXPERIMENT.md`; `sn:generated/numbers_audit.md` key `cov_pooled_n_points` | same | CURRENT [WORDING] | Results |
| A11.3 | the same render-only arms on the REAL Surgio test: 0.7-9.1 % whatever the coverage (low 4.9 / 9.1, low2n 1.4 / 2.4, high 0.7 / 1.0 % by seed) | `EXPERIMENT.md`; `PER_LEVEL_DOMAIN_ANGLE.md` Table G | same | HELD-OUT, NOT QUOTED | — |
| A11.4 | one real 301-frame rotational acquisition (case134): pooled detector 93.6 % of bodies at 0.25 (78.1 % at 0.74); the reported held-out detector 49.5 %, "exactly half of the boxes in 15 of 19 bins", recorded UNEXPLAINED | `sn:figures/figS4.record.json` (record `real_lodo_flat_half`); `sn:results/arc/case134_sweep.md` | `ssn:tools/case134_sweep.py`; job 40431371, requeued under eval_gate/2 as 40436881 | CURRENT; cause OPEN | Results (`\RESULT{s5_*}`), Figure S5 |
| A11.5 | nested pooled fit over 105 points (film N-curve H* = 0; C-arm naming cells; same-device detection cells; matched-N arms): M1 (N + lateral-angle coverage) beats M0 (N alone) by AICc 26.0; LR 29.1, p 6.7e-08; g = +19.96 points per unit H*_lat [12.24, 27.69] at conf 0.25; **at conf 0.74 it reverses** (dAICc -3.1, p .82, g -0.7 [-8.8, +7.4]); arms restricted to trained ones dAICc +32.0, g +24.2; g is identified only by the two render-arm corpora | `sn:results/coverage/pooled_fit.json`, `POOLED_FIT.md`, `sensitivity/pooled_fit_conf074.json`, `sensitivity/pooled_fit_trained_only.json` | `ssn:tools/indomain_fit_coverage.py --film` (local, 2026-09-25 10:02); the flag behind `pooled_fit_trained_only.json` is not recorded | CURRENT [THR] (printed as "at confidence 0.25 ... not at 0.74", `sn:sections/results.tex` L123-125); not drawn since the 2026-09-25 afternoon build | Results |
| A11.6 | real Surgio pose pool: 148 AP (within 10 degrees) + 148 lateral, none between 10 and 60 degrees; 3 of 18 lateral bins (normalised entropy 0.19), 6 % of joint bins; the case134 spin covers 83 % of lateral bins | `sn:results/coverage/coverage.json`, `COVERAGE.md`; `sn:results/arc/audit/pose_pools.json` | `ssn:tools/acq_coverage.py`; acqcov job recorded as 40436995 (topic 1 note) and as 40437098 COMPLETED 11:30 2026-09-24 (`PENDING_JOBS.json`, topic 2 note): both ids recorded, which one wrote the file is not settled | CURRENT | supplement |
| A11.7 | unseen render angle sweep, pooled detector: below 90 % of its AP recall by +/-30 degrees on both cards; Surgio card 0.69 at -50 degrees, 0.99 at -90; another subject's truth boxes already score 0.64-0.68 (anchor floor ~0.67) | `sn:results/arc/recall_vs_angle_unseen/recall_vs_angle.json` | job 40428072 | CURRENT (this re-score replaced the void leaked curve, EVAL_LEAKS L1) | supplement |
| A11.8 | per-angle **naming** does not exist; detection per angle exists only on case134, the 40-subject render arc and COBRA gantry bands | `PER_LEVEL_DOMAIN_ANGLE.md` §"What is not known", Table F | — | OPEN | — |

### A12. Image-formation device cards (Table S1, Figure S3)

Tool `ssn:tools/device_fit.py` (+ `tools/device_physics.py`, `ssn:slurm/device_fit.sh`); cards `ssn:docs/devices/<device>.json`
(code_sha 6e1cf8d). Nine terms fitted leave-one-group-out on up to 40 frames (PIXIUM 14 of 18). Table builder
`sn:tools/make_supp_device_table.py`.

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A12.1 | held-out R^2, card vs uncalibrated physics: Cios Fusion 0.905 vs 0.899 (40 / 366 frames); BV Pulsera 0.952 vs 0.917 (40 / 116); Elekta XVI 0.974 vs 0.964 (40 / 335); PIXIUM 4600 0.679 vs 0.650 (14 / 18) | `ssn:docs/devices/*.json#physics_terms` | CURRENT | Table S1, Figure S3 |
| A12.2 | gain on the 12 patient-held-out folds (Cios, Elekta; 701 frames): +0.019 [0.008, 0.033]; frame-weighted 0.023 [0.010, 0.033]; 2 of 12 negative; exact sign-flip P = .004, Holm .009 | `sn:results/eval_gate/leaks/card_gain_unseen.json` | CURRENT | supplement |
| A12.3 | within-subject folds (Pulsera phantom, PIXIUM cadaver): 0.056 [0.025, 0.088], not held out (one object each) | same | CURRENT, labelled | supplement |
| A12.4 | criterion C3 (every device's gain > 0 with an interval excluding 0) **not met**: holds only on six-fold percentile intervals; on six-fold t intervals only BV Pulsera excludes 0 | `sn:results/a6.json#verdict`; `sn:results/stats_review/recompute.json#R2_card` | CURRENT (answers rigor A6) | supplement |
| A12.5 | a refit with image noise in the loss failed its own acceptance gate on every device; the published parameters stand | `sn:figures/figS2.record.json` panel d; `sn:results/supplement_figs/card_refit/` | CURRENT | Figure S3 |
| A12.6 | the exposure clip defect: `device_style.SPREAD = 0.2` reaches 1.7-5.1 % of each device's joint distribution; 94.9-98.3 % of styled frames carry a pinned term; a typicality gate (99 % joint) is written but the clip is still the default | `ssn:docs/DEVICE_SPREAD_SWEEP.md`; `ssn:docs/DEVICE_PARAM_AUDIT.md`; `mem:device-sampling-audit.md` | OPEN ("a defect not repaired" in the supplement); A/B on real frames would run `ssn:slurm/device_spread_arm.sh` | supplement |
| A12.7 | the 24-fold gain +0.0376 [0.0205, 0.0573] | older supplement text | SUPERSEDED [LEAK] (EVAL_LEAKS L6: two devices have one subject) | — |
| A12.8 | `docs/devices/surgio_b51_dr.json` exists only on the grid | `sn:results/DATA_CONTRIBUTION.md` correction ix | fact | — |

### A13. Corpus manifold: is film separable from fluoroscopy (Figure S2)

| id | claim | file | tool / job | status | feeds |
|---|---|---|---|---|---|
| A13.1 | film vs fluoroscopy, one corpus held out (19 corpora, 7,311 frames): -0.7 to +9.2 points over the 71.8 % majority share across six pooled cells; no percentile interval excludes zero; two knn15 BCa intervals do | `sn:results/a2.json#corpus_manifold/excess_over_chance`; `sn:results/corpus_manifold/` | features job 40414107; 40414544/45 | CURRENT; all three feature spaces now reported (answers [SEL-REP] audit item A2) | Figure S2, supplement |
| A13.2 | films vs C-arm + kV frames, one source held out (5,797 frames): image statistics 63.4 % [57.6, 69.2] vs majority 64.4 %; deep features 85.0 % [79.4, 90.0] | `sn:figures/figS1.record.json`; `sn:results/manifold/probes.json` | jobs 40416696-98, `ssn:tools/corpus_manifold.py` (`sn:slurm/manifold.sh`) | CURRENT | Figure S2 |
| A13.3 | styled renders vs the device's real frames stay separable: Cios 100 % (n 736), Surgio 99.8 % (666), Elekta 99.0 % [98.1, 99.6] (771) | same | same | CURRENT | Figure S2 |
| A13.4 | per-device overlaps Bhattacharyya 0.005 (DeepFluoro-Geneva) to 0.675 (Elekta-Geneva) | `ssn:docs/RSNAI_CLAIMS.json` manifold_carm_pair_min/max; `mem:film-fluoro-boundary-not-transferable.md` | — | HELD-OUT, NOT QUOTED | — |
| A13.5 | first manifold (37 corpora): every held-out C-arm corpus labelled FILM; LOFO pooled 71.1 % vs chance 71.8 % | `$RS/data/or_ready/corpus_manifold/overlap.json` | — | SUPERSEDED by A13.1 | — |

### A14. Render-trained vs film-trained detector on plain films

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A14.1 | 17 NHANES II lumbar spines neither detector saw, conf 0.05: film-trained (`detect_v5z_final`) 99.4 % (160 / 161) vs render-trained (`anchor_det_v1`, 6,650 renders, no real image) 67.7 % (109 / 161), +31.7 points [21.0, 45.4], 16 : 0 spines; at 0.25 98.8 vs 34.8 % | `sn:results/eval_gate/leaks/render_vs_film_unseen_rerun.json` (job 40429839) | CURRENT, HELD OUT | supplement |
| A14.2 | the 25-spine version: 99.14 vs 71.67 %, +27.5 | older text | SUPERSEDED [LEAK] (EVAL_LEAKS L2: 24 of 25 spines in the film detector's own lists) | — |

### A15. Plain-film naming (selection split only)

File `sn:results/a5.json#per_protocol/random/*/patient_clustered` (v8 encoder `allspine_v8 model_rung_1_aug2.pt`, head
`head_allspine_v8_mixed_kmax4_seed0.pt`, seed 0; `sn:results/a5_rows_meta.json`: leak check by patient key 0 of 549 BUU,
727 CSXA, 52 NHANES val patients in train). Every annotated patient of these corpora is in v8's training or selection
split, so **no held-out plain-film accuracy exists in paper 1** (EVAL_LEAKS L4). Status CURRENT-SEL [SEL-SPLIT], printed
in the supplement section "Plain-film naming on the selection split" (answers rigor A5: patient-clustered, not by
vertebra).

| id | claim | status | feeds |
|---|---|---|---|
| A15.1 | CSXA cervical: 3,629 / 3,635 (99.8 %), 727 patients, Wilson [99.5, 99.9]; three bodies 99.6 % | CURRENT-SEL | supplement |
| A15.2 | BUU-LSPINE lumbar: 2,671 / 2,744 (97.3 %), 549 cases [96.5, 98.0]; three bodies 95.0 % | CURRENT-SEL | supplement |
| A15.3 | NHANES II: 441 / 445 (99.1 %), 52 patients / 76 films, Wilson [97.8, 99.6]; three bodies 94.6 % | CURRENT-SEL | supplement |
| A15.4 | v9, three seeds: NHANES 96.9-97.6 % | `sn:results/v9_a5_seeds.json` | CURRENT-SEL | Table 3 twin note f |
| A15.5 | per-level film naming: BUU L1-L5 96.4-98.4 %, NHANES 97.4-100 %, CSXA 99.7-100 %; renders floor at T7 (55-59 %), L6 20-42 %, T13 0 / 9 | `PER_LEVEL_DOMAIN_ANGLE.md` Table E (from `sn:results/a5_rows.csv`) | [DERIVED] [SEL-SPLIT]; not quotable until a committed tool re-runs it on held-out persons | — |
| A15.6 | the v9-bank re-score of A5 (chain 40415667 -> 40415670) "had not landed" (`sn:README.md`); whether it did later | — | NOT RECORDED | — |

### A16. Transitional persons, the split and the sample-size argument (Table 2, Figure 5a)

| id | claim | file | tool / job | status | feeds |
|---|---|---|---|---|---|
| A16.1 | 194 transitional persons in the sources: L6 110 (CTSP 18 / VerSe 86 / TS 3 / C-ArmLSpine 3), T13 7 (VerSe 6 / TS 1), sacralised L5 28 (12 four-lumbar), Castellvi I/II 31, lumbar rib 14, unassigned 4; per source 52 / 135 / 4 / 3 | `sn:results/rare_class/transitional_subtypes.csv` (2026-09-23 18:54) | `ssn:tools/transitional_subtypes.py --ts-override` | CURRENT | Table 2 |
| A16.2 | no spine carries both L6 and T13, in any source | `sn:results/rare_class/transitional_subtypes.md` | same | CURRENT | Results |
| A16.3 | eight of twelve TotalSegmentator "L6" spines are normal by an independent rib count; four are transitional | `sn:results/spineps_ids/TS12_VERIFY.md` | — | CURRENT | — |
| A16.4 | the built G3 split, test side: L6 43 + 3 real, T13 3, sacralised 11 (5 four-lumbar + 6 five-lumbar), Castellvi 12, lumbar rib 6, unassigned 2 = 77 CT + 3 real; 92 of 97 val+test persons sit in v8/v9 training | `sn:results/rare_class/split_plan.md` | `ssn:tools/make_split.py` apply 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS | CURRENT | Table 2 |
| A16.5 | pre-stated targets: exact-level Wilson lower bound >= 90 % needs 35 error-free at-risk persons; variant sensitivity >= 85 % needs 22 carriers | `sn:results/power/power.json#n_needed_zero_errors` | `sn:tools/fig_power.py`; independent check `sn:results/stats_review/recompute.json#R4_wilson` (PASS); re-derived 2026-10-08 by `HANDOFF/working_notes/t2_wilson_check.py` (match) | CURRENT | Figure 5a, Results |
| A16.6 | COBRA2026 screen: 91 unread test-side calls (L6 38, T13 45, four-lumbar 8); a count of persons with both junctions in field and an exported frame finds 7 at-risk persons, **4 two-labeller and 3 single-labeller** (L6 3 = 2 + 1; sacralised L5 or four-lumbar 4 = 2 + 2; T13 0) -> error-free Wilson bound 64.6 % | `sn:packet_src/persons_available_2026-09-24.json#rows/<row>/real_counted_with_frame` and `#rows/<row>/real_counted_by_tier` (rows `at_risk_pooled`, `L6`, `sacralised_L5`, `T13`; a verbatim copy of the persons-available block of `sn:results/power/power.json` as `sn:tools/fig_power.py` wrote it on 2026-09-24 10:33, git 8d6a4f4); `sn:results/transitional_registry/REGISTRY.md` table C (COBRA L6: 2 two-labeller + 1 single-labeller); `sn:results/transitional_registry/cobra/rows.csv` | — | CURRENT [AUTO-TRUTH] [WORDING]: `sn:sections/results.tex` L94-97 prints "a two-labeller count ... found seven", but 3 of the 7 are single-labeller. The pointer `sn:figures/figure5.record.json#numbers_on_figure/counts_and_intervals` (still in `sn:NUMBERS.md` L435 and `sn:CLAIMS_LEDGER.md` L271) no longer exists: the record of 2026-09-25 13:41 lists the panel a-d curves only (key retired in rebuilds 12925ad and 7bb37ed) | Figure 5a, Results |
| A16.7 | at-risk CT test persons: 51 (L6 43, four-lumbar 5, T13 3), 36 rendered -> 93.0 % if error-free; most are in the encoder's training lineage | `sn:packet_src/persons_available_2026-09-24.json#rows/at_risk_pooled/ct_test`, `#.../ct_rendered`, `#rows/<row>/ct_test` (not the retired figure-record key) | — | CURRENT | Results, Table 2 |
| A16.8 | labeller calibration: VERIDAH's L6 call matched the CTSP readers in 10 of 24; T13 in 0 of 52 | `sn:results/spineps_ids/IMPACT.md` line 230; `sn:results/stats_review2/recompute.json#S4_cobra_call_yield` | — | CURRENT | supplement |
| A16.9 | no released radiograph or C-arm frame carries a human-read T13 or Castellvi grade | `sn:figures/figure1.record.json#not_shown_and_why` | — | CURRENT | Figure 1 |
| A16.10 | 57 "field-supported" COBRA calls / 93.7 % best case; the 89 / 37 / 90.6 % inventory projection (12 TS spines read from raw SPINEPS ids); the 98.2 %-planning-accuracy power curve (69 / 4,276) | — | — | SUPERSEDED. **The twin `sn:tables/tab4_transitional.md` still prints "91 (57) ... 93.7"; the printed `.tex` reads "91 (7) ... 93.0 (51 CT); 64.6 (7 real)"** | — |

### A17. Development learning curve of the split-trained (paper 2) arm

File `sn:results/dual_loss/saturation.json`, `saturation_curve.csv`, `saturation_epochs.csv` (`sn:tools/d1_saturation.py`;
d1lcurve array 40436887, d1cover 40436997; logs `sn:results/dual_loss/`). ImageNet-init encoder + head on G3 training
persons, nested fractions, three seeds, read on the validation side that chose the epoch. Status CURRENT, validation
side only ("development numbers ...; no test person", `#status`); this head belongs to the paper-2 LevelCheck model
(`sn:LEVELCHECK_MODEL.md` §12). Feeds: supplement.

| id | claim |
|---|---|
| A17.1 | training persons 563 / 1,121 / 2,240 / 4,477 / 8,950; random windows overall 68.9 % -> 74.0 % (last doubling +0.6; seed spread 1.0 at full size) |
| A17.2 | real films 98.2 % (563) -> 98.7 % (8,950), last doubling +0.1; three bodies 97.2-97.5 % at every size |
| A17.3 | CT renders 59.6 -> 66.2 % (+0.8 last doubling); rendered L6 bodies 51.8 -> 64.2 % (+1.7; seed spread 3.4); rendered T13 named in none of three full-size runs |
| A17.4 | epochs: within 0.5 points of final by epoch 8-12 |

### A18. Study population and corpus totals

| id | claim | file | status | feeds |
|---|---|---|---|---|
| A18.1 | median age 36 y (CSXA) to 66 y (COBRA2026, age on 115 of 145); female 42.5 % (TotalSegmentator) to 64.5 % (CSXA); none released for the intraoperative, cadaveric or phantom sets | `sn:results/age_sex_by_source.json` (`sn:tools/age_sex_by_source.py`; VinDr headers job 40438307) | CURRENT | abstract, Results, Table S3 |
| A18.2 | corpus totals 4,093 renders, 9,108 level-annotated films, 4,276 real exposures (778 C-arm) | `sn:tables/tab_corpus.sources.md` "Totals row (footnote j)" (L173: 4,093 = 801 + 1,170 + 1,735 + 387) | **DISPUTED** (see A18.5): the 4,093 includes the TotalSegmentator `ts_drr` 1,170 and `ts_drr_v3` 1,735 renders, which the v9 build never reads, and leaves out the `physics_drr` (7,045) and `physics_rare` (1,482) renders the v9 bank does read; footnote j and the abstract inherit Table 1's TotalSegmentator error and must be recomputed from the v9 build roots (`ssn:slurm/allspine_v9_bank.sh`). The 9,108 counts the 542 NHANES films that carry landmarks; `~/films_drr` holds 9,109 annotation files because the 543rd NHANES film has no TIFF (`ssn:docs/DATASHEET.md` L165) | Table 1, abstract |
| A18.3 | Figure 1 persons aged 24-89 y | `sn:figures/figure1.record.json#components[].demographics` | CURRENT | Figure 1 |
| A18.4 | 7,045 physics-styled renders in Table 1 footnote a vs 7,048 items in that root | `sn:supplement.tex` "Corpus census" | recorded unexplained | Table 1 |
| A18.5 | Table 1 says TotalSegmentator v2 and v3 renders (1,170 / 1,735) are in the level bank; the v9 build script has no `ts_drr` or `ts_drr_v3` root (TS enters only as 1,831 `physics_drr` renders) | `sn:tables/tab_corpus.md` vs `ssn:slurm/allspine_v9_bank.sh`, `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 66, 511 | **DISPUTED**: trust the build script; Table 1 needs correcting | Table 1 |

### A19. Data-integrity numbers printed in the supplement ("Data integrity and quality controls")

| id | claim | file |
|---|---|---|
| A19.1 | 99 data gaps = 31 criterion + 28 bug + 21 unfinished + 4 budget + 15 unknown | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` "Every gap, worst first" |
| A19.2 | CHK-9 over 563 quoted numbers: 323 held out, 81 seen, 58 unreadable lineage, 101 no checkpoint (job 40429833); after the v9 closure 380 held out, 81 seen, 1 unresolved, 101 not applicable | `sn:results/eval_gate/EVAL_LEAKS.md`; `sn:results/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md` |
| A19.3 | 306 checkpoints in the lineage census, 133 with an unreadable link | `sn:results/eval_gate/LINEAGE.md` |
| A19.4 | 57 quoted numbers traced to the deleted `allspine_v2_r1` bank, re-run on v9 | `MANUSCRIPT_CORRECTIONS.md` §7.0 |
| A19.5 | NHANES II in the banks twice; 48 of 54 validation patients twinned in training | `ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `ssn:tools/leak_check.py` docstring |
| A19.6 | 2,437 harvested SPINEPS masks with raw ids 1..N; 3,490 relabelled | `sn:results/spineps_ids/CENSUS.md`, `IMPACT.md` §0, `REPAIRS.md` |
| A19.7 | 69 quoted detector numbers re-scored in both box conventions | `sn:results/bodybox_rescore/RESCORE.md` (job 40419582) |
| A19.8 | Mendeley: 500 of 584 films re-encode BUU-LSPINE | `ssn:tools/excluded_sources.py` REASONS |
| A19.9 | CTSpinoPelvic1K 0533 truncated download 17,301,504 -> rebuilt 250,067,995 bytes | `sn:results/repairs/ct0533_CHECK.md` |
| A19.10 | COBRA2026 frames counted up to four times in one arm: 5,013 duplicate entries | `sn:results/repairs/cobra-dup-leak_CHECK.md` (job 40416578) |

All CURRENT, supplement.

---

## Part B. Paper 2: SchwingNet against registration-assisted surgeons (LevelCheck)

Nothing here is printed in paper 1 (`sn:PAPER1_SCOPE.md`; moved 2026-09-24, `mem:paper-split-2026-09-24.md`).

| id | claim | file | status |
|---|---|---|---|
| B.1 | LevelCheck's published numbers are registration accuracy; the level name is imported from the preoperative CT: Otake 2012 99.998 % simulated; Lo 2015 100 % at 200 multistarts; Manbachi 2018 median error 30.4 % -> 2.4 %; five surgeons 69.6 % unassisted -> 97.6 % with LevelCheck; "LevelCheck fails on transitional anatomy" is not citable | `sn:LEVELCHECK_CLAIM.md` §1, §3 | CURRENT literature reading |
| B.2 | frozen comparator: H1 at-risk 82.2 % (Peh 1999) n_min 19; H2 97.6 % (Manbachi 2018) n_min 152; H6 ordinary non-inferiority 92.6 % (margin 5) n 48 | `sn:LEVELCHECK_MODEL.md` (frozen by ecae75f 2026-09-23 19:50:36; then 1897772, 2993f40, b511985 (§14), d0403de (§15)) | FROZEN; never edit |
| B.3 | automated reference: only ordinary spines qualify (Dawid-Skene PPV 0.971 [0.957, 0.981], coverage 0.886); no rule reaches a PPV lower bound of 0.90 for L6, T13 or four-lumbar; every transitional test person needs a human read | `sn:results/auto_reference/CALIBRATION.md`; frozen `sn:results/fig6/frozen/auto_reference.json` (57782cad...) | CURRENT |
| B.4 | ordinary COBRA test persons on automated truth: 56 assigned ordinary (44 with frames); H6 short of n_min 48 by 4 | `ssn:docs/RESUME_2026-09-22_PM.md` 2026-09-24 15:47 block | CURRENT |
| B.5 | open gate 40438004 (ordinary strata only) ran 2026-09-25 04:22-06:02Z; harvest-name scores only; **the reference-standard score was never written because `sn:tools/fig6_score.py` read `T1/blinded/meta_ref/` instead of `T1/open/meta_ref/`** | `sn:paper2_levelcheck/open_gate_40438004/README.md` | OPEN BUG: fix the path and re-score the dumps on disk |
| B.6 | blinded gate: memory names f6eval 40438005; `sn:REVISION_LOG3.md` line 7 names f6eval 40431765 / 40431766; held for Greg's truth decision, then cancelled 2026-09-27 15:50 with every non-ruleclass job; must not be released before `$RS/data/fig6/unblinding/RELEASE_v2.json` exists (written by a person after a frozen human truth) | `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; `mem:paper-split-2026-09-24.md` | OPEN; which job carries the post-§15 detector is not recorded |
| B.7 | why it left paper 1: ordinary-only superiority over 97.6 % needs 152 zero-error persons; the transitional strata need human reads that do not exist | `mem:paper-split-2026-09-24.md` | CURRENT |
| B.8 | prior-art rates used: wrong-level 1 in 3,110 (Mody 2008), 12.8 / 10,000 (Jhawar 2007), 0.12 % of 34,544 (Furuya 2026); LSTV 12.9 % with 54 % miscounted at clinic (Nakagawa 2017); Castellvi II-IV ~9 % of CT (Hanhivaara 2020) | `sn:LEVELCHECK_CLAIM.md` §2 | CURRENT (as recorded) |
| B.9 | the old Figure 6d Wilson table: all 30 cells equal scipy Wilson lower bounds | `sn:results/power_table.json` (`sn:tools/fig_claim.py`) | RECORD ONLY |
| B.10 | moved material, verbatim with file and line | `sn:paper2_levelcheck/MOVED_FROM_PAPER1.md` (8 items from dd8f4a5), `numbers_manifest_moved.json`, `tables/tab_levelcheck.*` | CURRENT |

---

## Part C. The C-arm and film programme before SchwingNet (2026-09-12 to 2026-09-22)

These built the programme; almost none is quotable now. Grid files under `~` and `$RS`.

### C1. Plain-film level identification and the early level models

| id | claim | file | model / bank | tool / job | status |
|---|---|---|---|---|---|
| C1.1 | context ladder on real films: single vertebra n = 1 96.7 %, 3 vertebrae 98.8 %, 5 vertebrae 99.1 %; lumbar n = 1 80.7 % (85.4 % at 96 px) | `~/tmp/ladder_summary.json`; `mem:level-id-2d-results-2026-09-13.md` | `films_ann` bank (cervical-dominated) | — | RECORD ONLY |
| C1.2 | recurrent head over single-crop embeddings: 98.69 / 99.13 / 99.41 / 99.48 % at 3 / 5 / 7 / 9 vertebrae, n 8,422; 14 of 27 classes live; head worth ~+0.4 over single-crop 96.95-98.98 %; weights never saved | `~/bench/xr_fov/recurrent.json` | **`films_ann_fov96_ctx`, not `films_all2`** (job log prints 28,032 crops = films_ann; films_all2 inputs were created after the result; `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` §1.1) | job 40215812 (2026-09-13 13:28) | RECORD ONLY [WRONG-BANK]: `ssn:slurm/recurrent_head.sh` line 16, `ssn:tools/recurrent_order.py` line 56 and `~/bench/model_registry.md` M96 still say films_all2 (uncorrected on 2026-10-08) |
| C1.3 | films_all2 head: 98.84 / 99.13 / 99.42 / 99.38 | `~/bench/xr_fov/recurrent_all2.json` | films_all2 | — | RECORD ONLY |
| C1.4 | whole-spine 27-class single crop: 78.74 % [78.11, 79.37], n 16,392; T13 0.0 % (n 14), L6 64.4 % | `~/model_night/runs/result_r18_ce.json` | allspine_v2 | — | RECORD ONLY [LEAK] |
| C1.5 | restored recurrent head on allspine_v2: 83.38 / 86.12 / 86.16 / 88.95 % at 3 / 5 / 7 / 9 (+10.2 at 9); T6-T8 floor 62-65 % | `~/model_night/recurrent_allspine_v2.json`; `mem:recurrent-head-restored-2026-09-16.md` | allspine_v2 | job 40293790 | RECORD ONLY [LEAK] |
| C1.6 | mixed-length head: 97.47 / 98.45 / 99.29 / 99.92 at 3 / 5 / 7 / 9; random window 99.02 % ("shortcut-free") | `mem:mixed-length-head-and-sota.md` | pools NHANES twice | `tools/head_mixed_length.py` | SUPERSEDED [LEAK] (the note's own 2026-09-22 correction); clean per-source v2 CSXA 99.87 %, BUU 98.04 % are in "Numbers deliberately absent" |
| C1.7 | Star Temporal Classification loss loses to cross-entropy everywhere; transitional 22-24 % vs 39.8 % | `~/model_night/stc/`; `mem:stc-does-not-transfer.md` | — | — | REFUTED |
| C1.8 | selective prediction: 99 % accuracy at 35.7 % coverage (exact level), 55.7 % (region); AUGRC 0.0466 | `~/selective/SELECTIVE.md`; `mem:selective-prediction-the-honest-99.md` | leaked v2 bank | job 40291753, `tools/level_selective.py` | NOT QUOTABLE [LEAK][SEL-REP]: computed on the test half (~8,280 vertebrae, not the 16,392 in the file header) with coverage chosen on the same half (`ssn:docs/MODEL_CARD.md` §5.3); a clean re-run is not recorded |
| C1.9 | model-night arms: CORN 78.44, ordinal focal 75.05, frozen 30.12 %; four ViT arms produced no result | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` §5.2, §7.2 | — | — | RECORD ONLY |
| C1.10 | corruption suite: films_all2 rung 1 clean 99.10 %, over-exposure severity 5 16.93 %; augmentation tier 2 79.18 % (motivates `--augment 2`) | `~/bench/robust/*.json` | films_all2 | — | RECORD ONLY |
| C1.11 | literature panels (FluoroCap): 19.7 % agreement with weak labels, n 7,065; resolution does not move naming (-0.33 points paired) | `~/model_night/panel_stats/`; `mem:fluoro-panel-gap-diagnosed.md` | — | — | not an accuracy; FluoroCap is figures of published articles, 72.8 % of panels with zero pixel residual (`mem:fluorocap-is-reproductions-not-fluoroscopy.md`) |
| C1.12 | LSTV / TLTV 2-D flags: CTSP AUC 0.577 [0.480, 0.669] (contains 0.5); VerSe 0.724; sex as positive control 0.951 on renders / 0.829 on real BUU | `~/lstv_flag/LSTV_FLAG_RESULTS.md` | — | — | REFUTED as a flag |
| C1.13 | LSTV flag learning curve, VerSe held-out (67 patients, 31 positive): 10 positives AUC 0.652, 20 0.688, 40 0.704, 80 0.685, 120 0.713; "tripling the positives bought under 0.01 AUC" | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` L659; `~/lstv_flag/LEARNING_CURVE.md` (grid) | — | `ssn:tools/lstv_flag_learning_curve.py`, `lstv_flag_curve_plot.py`; date and job not recorded | RECORD ONLY |
| C1.14 | feasibility interior windows: v2 ordinary lumbar 91.8 % [89.4, 94.1]; anomalous 66.0 % (12 films); v6 anomalous interior 49.9 % [41.5, 58.9] (128 films) | `~/model_night/interior_windows/`; `mem:feasibility-claims-measured.md` | v2 / v5 / v6 | job 40321368 | RECORD ONLY [LEAK] |
| C1.15 | remedies (film-noise randomisation, pretrain on renders, renders mixed 8 epochs, anchored-only admission) all lose to the v2 baseline (91.8 / 66.0) | `mem:remedies-refuted-2026-09-17.md` | v2 | — | REFUTED |
| C1.16 | Cina-style whole-film benchmark: v2 99.96 % = the sacrum-count rule 99.96 %; saturated, only the limited field discriminates | `mem:feasibility-claims-measured.md` | v2 | `tools/benchmark_cina.py`, job 40323179 | RECORD ONLY |
| C1.17 | re-implemented published competitors (ours, cina, kim, vertx, konya; 124 cells, dev / test halves) and their ensemble | design `ssn:docs/COMPETITOR_BENCHMARK.md`; output `~/model_night/ensemble/ensemble.json` | — | `tools/train_competitors.py`, `tools/ensemble_eval.py`; `make competitors`, `make ensemble-report` | **NOT RECORDED** in any repository document |
| C1.18 | two-mechanisms table: L6 44.9 % in State C; one body 72.9 %, five bodies 97.0 %, whole 98.2 % | `mem:two-mechanisms-thesis.md` | v2-lineage CV | — | SUPERSEDED (the framing still governs the paper) |
| C1.19 | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | `mem:xray-corner-detector-status.md` | — | — | DATED |

### C2. The 2026-09-17 synthetic / real fraction sweep and `eval_scaling_curves`

| id | claim | file | status |
|---|---|---|---|
| C2.1 | six encoders on subsets of the v2 bank, scored on 455 held-out real lumbar films (interior windows): render fraction 0 / 0.25 / 0.5 / 1.0 at real 1.0 gave ordinary 89.5 / 87.7 / 87.4 / 88.2 % and anomalous (12 films, 47 windows) 34.0 / 44.7 / 53.2 / 36.2 %; real 0.5 and 0.25 at render 1.0 gave ordinary 84.3 / 83.7 %, anomalous 53.2 / 38.3 %; cervical 97.1-98.8 % throughout | `sn:results/indomain/grid/scaling_curve_2026-09-17.json` (copy of `~/model_night/scaling/SCALING_CURVE.json`); `mem:remedies-refuted-2026-09-17.md`; `ssn:paper/rsnai/graveyard.tex` L65 | **SUPERSEDED [LEAK] [SEL-SPLIT]**: v2 split each source separately; the twin count (48 of 54 NHANES validation patients with their twin in training) was measured on v6 and v7, and v2 was built the same way but not counted before it was deleted (`ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` lines 17-19). Selection split: each subset encoder (`ssn:slurm/night_arm.sh` -> `ssn:tools/train_level_backbone.py`) keeps its best epoch by accuracy on the subset bank's validation rows (L516-520), and the interior evaluation scores those same rows (`ssn:slurm/scaling_sweep.sh` step 4: "validation rows are identical in every subset bank"), so even a v9 rerun of this script is a selection-split number; `sn:results/indomain/INVENTORY.md` L299-304 marks every row NOT ESTABLISHED; v2 deleted 2026-09-20. Also: every anomalous interval overlaps every other and the curve is not monotone. Built by `ssn:slurm/scaling_sweep.sh` (job id not recorded); figure `fig9_scaling` from `ssn:tools/make_feasibility_figures.py` L429-451 (whether drawn: not recorded) |
| C2.2 | reading at the time: "renders buy variant anatomy, not the film domain" (render fraction 0 -> 0.5 moved anomalous 34.0 -> 53.2 % while ordinary fell 2 points; cutting real film to a quarter cost ~5 points) | same | SUPERSEDED; the only render-ratio sweep ever run, on a superseded line |
| C2.3 | `eval_scaling_curves` devices axis measured at k = 1 for three held-out devices and k = 2 for Elekta only; the tool refuses a fit with two distinct k; one derivable cell: Elekta held out, Cios-only design-A model 38.1 % [32.3, 44.5] at 0.25 (would move the drawn Elekta slope from +19.2 to +6.3 points per device); `fewshot` never ran; `cases` needed a v8 encoder that did not exist then | foot of `ssn:slurm/eval_scaling_curves.sh`; `sn:results/indomain/INDOMAIN.md` L13 ("Superseded by the lcurve/det_fill cells") | PARTIAL; superseded. Whether `cases` ever ran: NOT RECORDED. Not on the path of a quoted number (`sn:results/eval_gate/EVALUATORS.md` L326) |

### C3. The sweep / chain / confirmation line (counting across overlapping exposures; private)

| id | claim | file | status |
|---|---|---|---|
| C3.1 | sweep_v3 (respaced renders), 120 held-out CTSP spines, 2-body overlap, 9-inch field: naming 72.1 -> 95.2 %; chain 97.5 %; with the end rule 120 / 120 | `~/model_night/sweep_v3/` (job 40384843; `ssn:slurm/sweep_v3.sh`; `ssn:tools/make_results_table.py`); `mem:sweep-map-replaces-registration.md` | RECORD ONLY. Only sweep_v3 counts: `sweep2`, `sweep_holdout_v2`, `sweep_protocol`, `sweep_improve`, `sweep_fix` used the wrong field size (`mem:drr-row-spacing-defect.md`) |
| C3.2 | TotalSegmentator bench, 522 spines from the sacrum: 98.5 % chains; 203 from C2 95.1 % | same | held out only for the v7-lineage encoder; for v9 only 71 cases are unseen (`~/model_night/sweep_v3/cns/unseen_v9.txt`; `mem:ts-bench-inside-v9-bank.md`) |
| C3.3 | 25 real lumbar films: chain 100 % with true boxes; 21 / 25 with the detector | same | RECORD ONLY |
| C3.4 | overlap ladder: 2 bodies of overlap optimal (97.5 % chains) | same; `ssn:docs/SWEEP_PROTOCOL.md` | protocol recommendation |
| C3.5 | counting with boxes given: 99.66 % of 6,255 walks (801 CTSP); C2 down on 262 real films 1,204 / 1,209 (99.67 %) | `ssn:docs/COUNTING_EVIDENCE.md` (generated by `tools/counting_brief.py`) | RECORD ONLY |
| C3.6 | counting with detector boxes: render detector 30.06 % (anchor by class 44.07 %, 507 of 625 refused) | same | REFUTED as deployable |
| C3.7 | needle confirmation: 99.31 % of 5,385 vs 99.48 % needle-free (801 CTSP); TS cervical 84.58 % vs 93.09 % (the metal is not free) | same | RECORD ONLY |
| C3.8 | search window widened 0.6 -> 2.1 bodies leaves counting at 98.9-99.6 % (the window is not the mechanism) | same | RECORD ONLY |
| C3.9 | transitional confirmation (18 CTSP L6 spines x 3 seeds): clean 45 / 54 exact chains, 36 named L6; film-noise 45 and 35 | `$RS/.../or_ready/story_rows_f3/summary.json`, `story_rows_f6/summary.json`; `ssn:docs/RSNAI_CLAIMS.json` lstv_* | RECORD ONLY (was Figure 2 of the 2026-09-22 set) |
| C3.10 | linking under physics: boxes given 99.74 % clean / 71.73 % physics; detector boxes 39.52 % / 21.50 % at conf 0.05 (0.25 miscalibrated); detection is the binding constraint, about sixty points, where realistic physics costs eleven to twenty-eight | `ssn:docs/PHYSICS_LINKING.md`; `ssn:docs/HANDOFF_PHYSICS.md`; `ssn:results/physics/`; `mem:detection-is-the-binding-constraint.md` | the finding is CURRENT; numbers RECORD ONLY; anything measured under `--perturb physics` before the bone-path fix is not quotable (`ssn:docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`); `make physics` reproduces every number and exits non-zero if one moved |
| C3.11 | three physics defects: only the AEC extrapolation changed an image (PIXIUM 4,607 -> 103,084 photons/mm^2 once capped); the display window hides the lateral spine | `ssn:docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`; `mem:physics-three-defects-measured.md` | RECORD ONLY |
| C3.12 | guided acquisition: engine built; phantom only (geometry to 1.2 mm); corpus result of job 40376577 | `ssn:docs/GUIDED_ACQUISITION.md` STATUS (2026-09-18) | **NOT RECORDED**; nothing quotable |
| C3.13 | runtime: full-resolution link 422.6 s per pair vs 575 ms reduced; a 3-exposure sweep 12.6 s, 7 exposures 27.2 s, excluding the detector, contended CPU, synthetic exposures; the "same answer" claim withdrawn | `ssn:docs/MODEL_CARD.md` §6.3; `~/bench/runtime_cost_workstation.json` | not in any manuscript; whether the GPU / detector job (`slurm/runtime_cost.sh`, MODEL_CARD §6.6) ran: NOT RECORDED |

### C4. DeepFluoro, image formation and devices (2026-09-20 to 09-22)

| id | claim | file | status |
|---|---|---|---|
| C4.1 | render-only detector on DeepFluoro real frames, sacrum recall (6 specimens, 365 frames, conf 0.05): 76.9 % (by specimen 47.8-96.2 %; the seed alone moves 26 points); ~40 % before fixing 160 / 366 frames stored upside down | `mem:learned-formation-refuted-calibrate-instead.md`; `ssn:docs/DEEPFLUORO_FORMATION.md` | RECORD ONLY |
| C4.2 | calibrate, don't learn: exact geometry + attenuation explains 80.9 %; nine terms leave-one-specimen-out +4.1, v2 +4.3 (`calibration_best.json`); ceiling 99.5 %; a learned refiner better on 21 % of frames only | same | the decision stands; numbers RECORD ONLY |
| C4.3 | DeepFluoro frames were converted wrongly (log of a log); fix `DF_CONVERSION=linear` | same | OPEN: a refit of the cards under the linear conversion is not confirmed in any file read |
| C4.4 | learned arms vs none on TS renders: none_v2 64.0 %; rffull 71.7, rfhp 72.2, fda 74.2 %; pairs 90.0-95.0 % | `tools/deepfluoro_anchor_report.py`; same memory note | RECORD ONLY |
| C4.5 | first real-frame LODO detector table: C-ArmLSpine held out 90.6 % vertebrae / 83.9 % sacrum at 0.25, outline (5.2 % under body = convention) | `$RS/.../or_ready/lodo/rescore_outline.json`; `ssn:docs/RSNAI_CLAIMS.json` | became `a1.json` (A6); the 1,440-cell `rescore_outline` was one of the two [SEL-REP] items of the rigor audit |
| C4.6 | styled-corpus LODO (dc arms): Cios held out 0.9157-0.9398 vertebra recall (test specimen); Elekta 0.3024-0.3270; Surgio 0.1429-0.1498; one -> two training devices Elekta 0.1221 -> 0.3024 | `~/spine-detector/runs/devcorpus/*/scores.json`; `ssn:docs/MODEL_CARD.md` §4.6 | SUPERSEDED by the contribution-matrix scoring; the box convention of these rows is not recorded and `dc_B_held_cios_fusion_s1` has no row (MODEL_CARD says so) |
| C4.7 | fixed-split fine-tunes (28 test cases): mixed fine-tune lateral / AP 94.6 / 95.2 % whole, 87.4 / 86.4 % at 3; real-only fine-tune 89.2 / 95.2 % (lost laterals); detector fine-tunes multi 97.4 / 95.9, pooled 93.1 / 100 % | `ssn:docs/carmlspine_ft_mix_test_2026-09-21.json`, `_ft_realonly_`, `_ftdet_multi_test_2026-09-22.json`, `_ftdet_pooled_` | RECORD ONLY |
| C4.8 | deployment evidence: one vendor route (Siemens Cios OpenApps, K181560 / K203504); no published compute figure for any C-arm | `ssn:docs/CARM_DEPLOYMENT_EVIDENCE.md` | evidence document |
| C4.9 | sweep timing: a 3-5 exposure sweep is about 2-5 min, dominated by C-arm moves (36-49 s each); a synthesis of literature, not a measurement | `ssn:docs/SWEEP_TIME_EVIDENCE.md` | evidence document |
| C4.10 | film vs fluoroscopy: devices separate pairwise, the modality boundary does not transfer to an unseen corpus | `mem:film-fluoro-boundary-not-transferable.md` | CURRENT finding |
| C4.11 | DRR-to-fluoro levers measured: fidelity, strong domain randomisation, scale; CycleGAN and ADDA refuted | `mem:drr-to-fluoro-levers.md` | CURRENT finding |

### C5. CT segmentation ablations (CTSpinoPelvic1K nnU-Net)

| id | claim | file | status |
|---|---|---|---|
| C5.1 | six ablations of the segmentation model (fused_only 803, no_partial 804, no_lstv_oversample, short 100 epochs, ResEnc L, fused-only test 805) submitted by `ssn:slurm/spine_ablation.sh` (`make ablate`), aggregated by `ssn:tools/compare_ablations.py` into `tables/ablations.tex` | `ssn:docs/ablations.md` (first commit 2026-04-18) | **NOT RECORDED**: no `tables/` directory locally; the grid holds `~/ablate` (202-235 GB) |
| C5.2 | L6 pseudo-Dice 0.000 for 27+ epochs under 12x duplication (Dataset813); a counting decoder finds 6 / 6 L6 on four-class truth; Dataset815 raises L6 cases 18 -> 62 | `mem:l6-sample-count-and-counting-decoder.md` | DATED: a distinct-case count signal, not a trainer bug |
| C5.3 | Dataset810 one-shot model launched 2026-09-07, retired 2026-09-08 for Dataset813 (numbered ribs); whether Dataset813 folds finished or were scored | `mem:lstv-oneshot-training-run.md`; `ssn:docs/ruleclass/CLASSIFIERS.md` R36 | NOT RECORDED; no evaluated single-shot model exists on disk (contradicts the RPPR and the CNS 66629 title, `MANUSCRIPTS.md`) |

---

## Part D. The anomaly scan (transitional harvest, registry, ruleclass)

| id | claim | file | tool / job | status |
|---|---|---|---|---|
| D.1 | anomaly manifest (2026-09-17): 749 anomalous spines; tier A certain 355 (VerSe 163, BUU 144 real films, CTSP 48), tier B pseudolabel 211 (VinDr 209, LAT236 2), tier C FluoroCap captions 183; four-class over 1,113 CT spines 902 ordinary / 98 LS-only / 47 TL-only / 66 both | `~/model_night/anomaly_manifest/{anomaly_manifest.csv, spine_classes.json, summary.json}`; `mem:anomaly-manifest-sources.md` | `ssn:tools/anomaly_manifest.py` | DATED; the count was once 34/16/2 because only the 802-row CTSP manifest was read; the master flag table is `~/lstv_flag/lstv_flag_labels_v2.csv` |
| D.2 | co-occurrence of thoracolumbar and lumbosacral variants: OR VerSe 4.30 [2.59, 7.14], CTSP 4.00 [1.00, 16.03]; the pooled 12.8 is Simpson's paradox; the audit's VerSe 280 fully graded 3.61 [2.08, 6.27] (morphology-only 3.2 [1.8, 5.8]) | `mem:anomaly-manifest-sources.md`; `mem:feasibility-claims-measured.md` | `ssn:tools/anomaly_cooccurrence_from_labels.py` | DISPUTED: trust 3.61 (count-coupled rows removed); never quote 12.8; CTSP's own 4.00 is underpowered (a both-cell of two) |
| D.3 | BUU anomaly labels in `KIOM2022_dataset_report.xlsx` sheet `L4L6` (129 L4, 15 L6); 9 of the 15 "L6" are children | `mem:anomaly-manifest-sources.md`; `mem:feasibility-claims-measured.md` | — | CURRENT caution |
| D.4 | anomalous inventory (2026-09-23): VerSe 56 (L6 50, T13 6), CTSP 18 L6, TotalSegmentator 4 (3 L6, 1 T13), C-ArmLSpine real 3 L6 = 81 | `sn:results/anomalous_inventory.{json,md}` | `ssn:tools/anomalous_inventory.py`, job 40416205 | DATED |
| D.5 | transitional subtypes 194 persons; G3 split | A16.1, A16.4 | — | CURRENT |
| D.6 | 49 of 54 L6 val+test people of the G3 split are in the v8 / v9 training lineage | `sn:results/rare_class/split_plan.md` | — | CURRENT; limits what any v8/v9 descendant can claim |
| D.7 | five harvest streams (workflow wf_babed05b-84a): verse 374 series / 355 persons (L6 85, T13 6, sacralised 13, Castellvi I/II 27, lumbar rib 12, unassigned 23); ctsp 64 positive rows (L6 29: 17 read, 11 two-labeller, 1 single; sacralised 12; Castellvi I/II 4; lumbar rib 14; unassigned 5); totalsegmentator 1,935 v300 keys (L6 22, T13 4, unassigned 26, unresolved 74); cobra 692 (L6 3, unassigned 6, unresolved 11, TEST only); other_ct 3,066 (CTSpine1K L6 3, sacralised 2; RibFrac T13 4, L6 1) | `sn:results/transitional_registry/<stream>/` (`SUMMARY.md`, `rows.csv`) | tools listed in `RECIPES.md` §3 | DATED |
| D.8 | the one registry (2026-09-24 11:07): 6,131 rows -> 6,108 persons (5 phantoms as rows); 782 alias edges; persons per subtype: **L6 146** (read 103, two-labeller 29, single 10, morphology-only 4; 6 real-frame TEST), **T13 14** (read 6, two-labeller 3, single 5), sacralised L5 27, Castellvi I-II 31, lumbar rib 26, unassigned 62, unresolved 129, none 1,686, no_count 3,987; against the subtype table L6 110 -> 146 (106 kept, 3 dropped, 40 new), T13 7 -> 14 | `sn:results/transitional_registry/REGISTRY.md`, `registry.csv` | `ssn:tools/transitional_registry.py` | CURRENT for persons |
| D.9 | review queues for Greg: verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87 (+103 labeller-validation), all rendered (contact sheets `sn:results/transitional_registry/contact_sheets/`); `greg_verdict` filled on 0 | `REGISTRY.md` "Review queues" | — | OPEN |
| D.10 | MAXIMIZE (render every registry person the recipe allows): rendered before 87; planned 165, rendered 109, held by the ID guard 54, stopped 2; waiting for adjudication 39; real-frame TEST 13; unavailable 2; rendered transitional CTs now 196 | `sn:results/transitional_registry/maximize/MAXIMIZE.md`, `jobs.json` | `ssn:tools/rare_class_maximize.py`; `sn:slurm/rare_max_{stage,verse,verify}.sh` | CURRENT |
| D.11 | acquisition plan tier 1: 45 routes + NLST pilot, 15,233 CTs, expected transitional people E_low / E_high 831 / 1,703, E_count 460; stopping rule stated before any fetch (no collection below 20 expected per TB; no fetch under 5 TB free; 8 TB cap; measure tier 1 before tier 2; nothing beyond tier 1 while > 5,000 fetched CTs are unscreened) | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` §1-3; priors `ssn:tools/acquisition_census.py` L17-26; P(countable) from job 40425064 (`fov_calibration.json`) | — | [E] expectation, not observation |
| D.12 | **NLST pilot T13 9.3 % (34 of 367, all from labeller A alone, 5-15x the prior) was wrong but plausible**; requiring a rib on the named body brought it to 1.5 % (prior 0.6-2.0 %); `acquisition_screen.confirm_t13_by_rib` now runs at every call stage | `ACQUISITION_PLAN.md` §11 | jobs 40436876/77, `tools/acquisition_t13_check.py` | CURRENT; the house example of checking outside the computation |
| D.13 | census of every collection (2026-09-25): 18 collections, 18,873 listed, 16,898 on disk, 12,123 passing the field gate; expected L6 322, four-lumbar 161, Castellvi II-IV 907-1,813, T13 38-119 [E]; called L6 two-labeller 21, single 18; T13 single 16; review 84; 843 GPU-hours spent; tier 2 (chest) 29,479 CTs, 2.9 TB, NLST 2.3 TB for ~110 T13 people (refused by the stopping rule); gated Merlin alone ~447 L6 and 224 four-lumbar [E]; storage 4,482 GB of 20 TB; all of it ~15.5 TB | `ssn:docs/CENSUS_TABLE_2026-09-25.md` (`ssn:tools/census_table_2026-09-25.py`) | — | DISPUTED: "on disk" and "field gate" counts are one high in every collection checked except PANORAMA (`ssn:data_platform/DATA_MANIFEST.md` L175, L3698-3703); the CNS 2026 table copies the high figures (`ctsp:paper/cns2026/prep_v8_table.py`); cause NOT RECORDED |
| D.14 | labellers on 70 externally labelled TotalSegmentator CTs: A (SPINEPS+VERIDAH) found 12 of 28 L6 (6 no count), B (TotalSegmentator geometry) 17 of 28 (9 no count), both 9; T13: A 5 of 7, B 0 of 7 (7 no count); false L6 A 2, B 1 | `sn:results/transitional_registry/acquisition/validation/VALIDATION.md` (the "both 9" is read from its cross table, not stated in it); the reading "halve it for what the current two-labeller rule will confirm without a human" is `ssn:docs/CENSUS_TABLE_2026-09-25.md` L83 | — | CURRENT |
| D.15 | A and B (COBRA code) on CTSP against reader truth, before / after the 2026-09-24 rules: two-labeller L6 12 calls, 6 right [25.4, 74.6] -> 7 calls, 5 right [35.9, 91.8]; L6 reaching the two-labeller tier 6 of 18 -> 5 of 18 | `sn:results/transitional_registry/cobra/labeller_validation_ctsp.md` | — | CURRENT |
| D.16 | TotalSegmentator-stream two-labeller L6 on CTSP: right 6 of 10 | `REGISTRY.md` "What is not known" | — | CURRENT |
| D.17 | Moller-mask stump flag against the VerSe read: 65.7 % sensitive; the foramina counter fails on normals | `ssn:docs/ruleclass/CLASSIFIERS.md` R27, R31 | — | CURRENT |
| D.18 | CTSP read prevalence against priors: L6 18 / 789 = 2.3 % (prior 3.2 %); four-lumbar 9 / 789 = 1.1 % (1.6 %); only 33 Castellvi-graded against 71-142 expected | `HANDOFF/literature_state/power.md` §4 | — | CURRENT |
| D.19 | ruleclass tier lists (2026-09-27 00:20-00:40, `tiers/build_tiers.py`, file listing only): 21,622 CTs (21,603 persons); tier 1 5,094 (CTSP 802 + TS-benchmark natives 1,602 + COBRA 692 + 1,997 flagged + 1); tier 2 12,217; untiered 4,311 (gate-refused, PANORAMA pending 1,114, 210 TS scans where SPINEPS failed); tier-1 flags L6 148 (registry) + 303 (screens), T13 14 + 82, unresolved 129, review 1,168; children 114 / 442; both junctions in field 2,951 / 8,050; raw-id SPINEPS masks 108 / 422 | `ssn:docs/ruleclass/TIERS.md` | grid `$RS/ruleclass/code/` | CURRENT lists. DISPUTED small counts: `RESUME_2026-09-22_PM.md` L134 says 5,095 / 12,218 / 4,312 (trust TIERS.md); `CORPUS.md` (grid) says 21,655, a 33-CT difference recorded as unexplained |
| D.20 | ruleclass state on 2026-09-27 17:00: 228 jobs running, 315 pending; Moller fast pass 1,801 of 5,094 tier-1 CTs; pelvis 0; total_v3 0 | `ssn:docs/RESUME_2026-09-22_PM.md` L29, L55 | arm jobs in `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | **what the arms finished after 2026-09-27: NOT RECORDED on the laptop** |
| D.21 | every earlier pelvic cue for Castellvi on CTSP was falsified or weak: ala rise AUC 0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599 | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` | — | REFUTED cues (rule 2 of the pre-registration gates nothing until a reference half is frozen) |
| D.22 | rule 1's second step already ran on CTSP: 18 six-lumbar spines split A 11 / C 4 / B 1 / B-or-C 2 | `CLASSIFIERS.md` R30 | — | CURRENT (see also F.27) |
| D.23 | four-rule pre-registration `PREREG_rules.md` DRAFT v1 (commit f15da62, 2026-09-27 16:47): freeze block (signer, date, sha256) blank; "every number this document produces is calibration, not a result" | `ssn:docs/ruleclass/PREREG_rules.md` | — | OPEN (unsigned) |
| D.24 | the R + C = 22 rule: it is one count (N != 23); computable on 14 of 1,175 spines (1.2 %; VerSe 14 / 374, CTSP 0 / 801); C1 is labelled on every VerSe case carrying C2, so a detector that boxes C1 flags every normal spine (specificity 0.000); the 1.00 / 1.00 is circular; holding false alarm at 5 % needs a per-body miss rate <= 0.223 %; centre-to-centre spacing (p99 ratio 1.17, threshold 1.6) finds a missing body | `ssn:docs/ANOMALY_RULE_EVALUATION.md`, `anomaly_rule_evaluation.json` | job 40414996, `ssn:tools/eval_anomaly_rule.py` | REFUTED; removed from the manuscript on Greg's order |
| D.25 | `~/verse_drr` holds 13 exact duplicate renders (`glgl003` ... repeating `gl003` ...) | same | — | CURRENT fact |
| D.26 | VerSeFusion manifest `has_T13` claims 18 spines; truth 6 (six of the eighteen carry an L6 instead); `verse707` is a genuine table-vs-mask conflict | `mem:versefusion-t13-flag-wrong.md` | — | CURRENT trap |
| D.27 | distinct transitional people by date, never mix them: 749 anomalous spines (09-17); 81 (09-23 inventory); 89 (09-23, superseded: 12 TS raw-id selections); 194 persons (09-23 subtypes); registry L6 146 / T13 14 (09-24); 196 rendered CTs (09-24); tier-1 flags L6 148 + 303 (09-27) | `working_notes/topic2_scaling_samples_anomaly_power.md` B.4 | — | reference |

---

## Part E. Power calculations

The complete inventory with its own reproduced checks is `HANDOFF/literature_state/power.md` (written 2026-10-08,
`literature_state/power_calc.py` -> `power_calc.json`, using the exact-binomial code of `sn:LEVELCHECK_MODEL.md` §11 and
`ssn:tools/stats_compare.py`). Targets come from `ssn:docs/FLAGSHIP_PLAN.md` "The claim (G6)" item 4 (exact level on
transitional real frames with Wilson lower bound >= 90 %; variant sensitivity lower bound >= 85 %; "If the bound is not
met, the manuscript says so"). Wilson 95 % score interval, z = 1.959964.

| id | claim | file | status |
|---|---|---|---|
| E.1 | Wilson lower bound with 0 errors: 88.65 % at n 30, 92.13 at 45, 93.98 at 60, 96.30 at 100 | `sn:results/power_table.json` (`sn:tools/fig_claim.py`) | CURRENT; its 89-person inventory block is superseded |
| E.2 | smallest n meeting the targets: 90 % exact-level bound needs 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; 85 % variant sensitivity needs 22 / 34 / 45 / 74 carriers | `sn:results/power/power.json#panel_a`, `#n_needed_zero_errors` | CURRENT (Figure 5a); re-derived exactly by `working_notes/t2_wilson_check.py` |
| E.3 | error-free bounds: 64.57 % at n 7, 90.59 at 37, 93.00 at 51, 95.86 at 89 | same (the n 7 is A16.6: 4 two-labeller + 3 single-labeller persons, not a two-labeller count) | CURRENT (arithmetic) |
| E.4 | probability the target is met; n for 80 % power: 99 persons at a true 97 %, 69 at 98 % (planning values with no transitional measurement behind them) | `sn:results/stats_review/recompute.json` R4_wilson | CURRENT, conditional |
| E.5 | power at 51 persons with no error allowed: 0.07 / 0.21 / 0.36 / 0.60 at a true 95 / 97 / 98 / 99 % | `literature_state/power.md` §2 rows 8-10 | CURRENT |
| E.6 | LevelCheck comparison: n_min 19 / 48 / 152 for p0 0.822 / 0.926 / 0.976; the 97.6 % comparator cannot be exceeded at any reachable n; power is 0 at any true accuracy <= 0.822 | `sn:LEVELCHECK_MODEL.md` §5, §7, §13 (frozen §9); `sn:results/stats_review2/recompute.json` S1-S4, S9, S12; `sn:REVIEW2_STATS.md` | FROZEN (paper 2) |
| E.7 | earlier LevelCheck claim table: 89-person inventory gives test n ~36, target met only with zero errors; 3 real transitional subjects give 43.9 % | `sn:LEVELCHECK_CLAIM.md` §4 | SUPERSEDED inventory |
| E.8 | older Figure 5 panel b (exact binomial): 80 % power for the 90 % bound at 69; exceeding 97.6 % first at 4,276 | `sn:NUMBERS.md` L52 | SUPERSEDED 2026-09-24 |
| E.9 | selective prediction: certifying 99 % selective accuracy with zero errors takes about 298 answered cases; class-conditional 99 % needs >= 99 real calibration cases per class | `mem:selective-prediction-the-honest-99.md` | CURRENT arithmetic |
| E.10 | QI protocol: "powered to estimate, not to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" | `ssn:paper/qi_universal_protocol/main.tex` L229-231 | CURRENT statement |
| E.11 | device-level claims cannot be tested with 4 devices: the smallest two-sided sign-flip P is 0.125; the one comparison decided at its n is LODO vs pooled detection on one device (28 cases, 8 : 0) | `literature_state/power.md` §6 | CURRENT |
| E.12 | T13 is the scarce class: 44-138 T13 people expected in the whole holding [E] against about 55 needed for 22 test carriers under the 50/10/40 split | `literature_state/power.md` §4 | CURRENT |
| E.13 | no power calculation exists for the synthetic:real ratio, for device-level differences, or for LODO across devices; the person-level intraclass correlation for transitional endpoints is unknown | `literature_state/power.md` §8 | OPEN |
| E.14 | the plain reading: every powered statement rests on planning accuracies of 95-99 % that no transitional measurement supports; the transitional figures on disk (render L6 recall 56.1-72.4 % [SEL-SPLIT]: the v9 encoder kept its best epoch on the split these spines belong to, `sn:results/eval_gate/EVAL_LEAKS.md` item 6; real C-arm L6 classifier 44.9 % SUPERSEDED: the v2-lineage two-mechanisms table, C1.18; film interior anomalous 66.0 % RECORD ONLY [LEAK]: measured on v2, C1.14) put every transitional test at or near zero power, but **no held-out transitional measurement exists**, so this stands as a planning statement only; paper 1 needs 35 error-free at-risk persons, paper 2's H1 needs 19, today 7 unverified real at-risk persons exist (A16.6) | `literature_state/power.md` §6 | CURRENT as a planning statement; none of the three figures is quotable |
| E.15 | two-proportion power, n per arm, minimum detectable difference | `ssn:tools/stats_compare.py` (tool only; `tools/test_stats_compare.py`: a naive 95 % interval covers 70.8 % when frames are clustered) | tool, no saved output |

---

## Part F. CTSpinoPelvic1K: the dataset and its measurements

Release v11 (VerSe-native ids; 29 retired). Article `ctsp:paper/mpda/main.tex` ("MPDA", Medical Physics). Figures and
tables of the article and their generators are in `RECIPES.md` §9.

### F1. Building the dataset

| id | claim | file | status | feeds |
|---|---|---|---|---|
| F.1 | 802 records from TCIA CT COLONOGRAPHY: 342 fused (spine and pelvis on one series), 351 separate, 89 spine only, 20 pelvis only; 422 supine, 377 prone, 3 decubitus; 562 at 1.0 mm, 232 at 1.25 mm, 8 other | `ctsp:paper/mpda/main.tex` Sources and Figure 1 TikZ | CURRENT | MPDA Figure 1 |
| F.2 | CTSpine1K's selector never selected (the retained series is whichever the directory walk reached last); `Path.csv` names no position for 217 of 782 annotated records; CTPelvic1K: 702 of 713 masks resolve to the series chosen by bone overlap | `ctsp:paper/mpda/main.tex` Sources; `ctsp:morphometrics/ctspine1k_pathcsv_agreement.csv` (`ctsp:scripts/compare_ctspine1k_pathcsv.py`); `mem:ctspine1k-selection-code-deleted.md` | CURRENT | MPDA Sources |
| F.3 | source ground-truth corrections: 112 spine corrections in 103 cases, 13 pelvic in 12 | `ctsp:paper/mpda/main.tex` Figure 1 | **DISPUTED**: every row of `ctsp:docs/CORRECTIONS.md` (last changed 2026-07-21) still reads "pending (in review)"; final state per row NOT RECORDED | MPDA Figure 1 |
| F.4 | pelvic pseudolabeller (Dataset803, five-fold nnU-Net, out of fold on 440 records) held-out Dice against manual CTPelvic1K labels: sacrum 0.980 +/- 0.003 (no fold below 0.977), left hip 0.970 +/- 0.016, right hip 0.971 +/- 0.015 | `ctsp:results/pseudolabel_dice/README.md`, `dataset803_fold_validation_dice*.csv` (`ctsp:scripts/extract_pseudolabel_dice.py`) | CURRENT, with the caveat recorded there: these are nnU-Net's patch-based online validation Dice read from the checkpoints; `scripts/eval_vs_manual.py` was written but never run | MPDA Table S1 |
| F.5 | S1 carve audit (v3-v10 id 29): median craniocaudal extent 57.6 mm (a real first sacral segment is near 30); 221 of 801 records with S1 over half the sacrum (CSV count; `CLAUDE.md` and commit 2232bde say 222); 580 in 0.15-0.50; failures shaved the ventral cortex; found by rendering | `ctsp:morphometrics/s1_carve_audit.csv` (`ctsp:scripts/audit_s1_carve.py`); `ctsp:docs/qc/s1_carve_0428_vs_0704.png` | CURRENT (221 vs 222 not settled) | reason for v11 |
| F.6 | effect of the carve on the angles: on the 580 sound carves PI 52.7 / PT 19.6 (Hasegawa 53.4 / 19.2); on the 221 degenerate PI 68.5 / PT 33.6; the plate gate fired on 96 % of the second group and 4 % of the first | commit 2232bde; `ctsp:scripts/compare_v10_v11_spinopelvic.py` | CURRENT | — |
| F.7 | v11 merge returned 155,093,558 voxels to the sacrum on 801 of 802 records (1000 never had an S1) | `ctsp:scripts/merge_s1_into_sacrum.py` docstring; `ctsp:scripts/check_s1_merge.py` | CURRENT | — |
| F.8 | rib checks, pseudolabel vs release (same code): two numbers on one bone 151 / 584 -> 0 / 0; detached 37 / 40 -> 0 / 0; split inside the field 119 / 280 -> 6 / 7; offset 24 / 170 -> 0 / 2; no vertebra within reach 38 -> 11; rib on a lumbar body 14 / 21 -> 0 / 0 | `ctsp:results/rib_qc_v4_vs_release/README.md` (grid job 40220664) | CURRENT | MPDA Table II |
| F.9 | release rib incidence: 11,560 ribs, 5,796 skipped (own vertebra outside the field), 11 no contact, 5,753 evaluable, 5,751 match, 2 offset (0.035 %), 0 misnumbered cases | `ctsp:results/rib_qc_v4_vs_release/incidence_release.json` | CURRENT | MPDA Validation |
| F.10 | rib review: all 152 worklist cases corrected, 149 finalised by a second read; not finalised: token 46 (case 0068), 61 (0090), 518 (0730) | `ctsp:results/rib_qc_v4_vs_release/README.md` (checked against ledger `anonymous-mlhc/CTSpinoPelvic1K-reviews-ribs` 2026-09-14) | CURRENT (an earlier "148 of 152" was a stale worklist) | MPDA |
| F.11 | lumbar ribs (60 / 61): 16 records (13 bilateral, 3 right only) | `ctsp:paper/mpda/main.tex` Label scheme; `ctsp:morphometrics/label_census_v11.csv` | CURRENT (case 0787 was the 15-vs-16 disagreement) | MPDA |
| F.12 | stump twelfth ribs (lowest-rib ratio < 0.33) in 98 of 789 records (12.4 %); lumbar ribs 2.0 %, against 12.6 % and 1.5 % in Nagata 2025 | `ctsp:paper/mpda/main.tex` Descriptive Analysis; `ctsp:morphometrics/transition_morphometrics.csv` column `rib12_11_ratio_min` | CURRENT (CSV written on v10 labels; ribs unaffected by v11) | MPDA |
| F.13 | surgical hardware: 52 detections -> 11 kept (kept >= 2,586 mm^3, rejected <= 1,768 mm^3); eight arthroplasties, one osteosynthesis, one SI fixation, one cage pair (0068); 1,538,852 voxels reclaimed; femoral head used for PI/PT is an implant in eight records | `ctsp:zenodo/KNOWN_ISSUES.md` §3, §8; `ctsp:paper/mpda/main.tex` | CURRENT (`ctsp:docs/HARDWARE_CLASSES.md` says nine: stale) | MPDA Figure S1 |
| F.14 | Castellvi: 34 records read by two radiology residents (reads dated 2026-09-04): 33 graded as an LSTV and 1 graded `0` (normal); six disagreements resolved by consensus; consensus IIIb 16, IIb 6, IV 4, IIa 4, Ib 2, IIIa 1, 0 1; kappa 0.737 (0.553-0.920) full, 0.696 type only; 768 of 802 unread (null means ungraded, not normal) | `ctsp:docs/castellvi_consensus.csv`, `castellvi_readers_2026-09-04.csv`; `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` row 19 | CURRENT. Stale distributions: `ctsp:morphometrics/castellvi_grades.csv`, `ctsp:zenodo/README.md`, `ctsp:Lumbosac.csv`, `Desktop/NeurIPS/Lumbosac_Castelvii_Class.csv` (IIIb 19) | MPDA, NeurIPS |
| F.15 | manifest `has_l6`, `n_lumbar_labels`, `has_lumbar_rib`, `lumbar_rib_side` recomputed from volumes 2026-08-23; current census 18 L6 records | `ctsp:docs/RELEASE_CHECKLIST.md`; `label_census_v11.csv` | CURRENT | MPDA |
| F.16 | `n_voxels_fg` is broken (0 in 340 of 802); `spine_bone_pct` is over vertebra ids only and nothing says so | `mem:grid-ct-0533-truncated.md` | OPEN | — |
| F.17 | splits: five disjoint folds, no held-out test set; the splitter never read the lumbar count (strata lumbarization 15 / sacralization 15 / semi 2 / ambiguous 2 / normal 768; record 0500 sits in lumbarization on a phantom L6) | `ctsp:paper/mpda/main.tex` Data Format; `context/splits-origin-and-v3-resplit.md` | OPEN (why 0500 was flagged: NOT RECORDED) | MPDA |
| F.18 | identity: one release id = one person, 802 / 802, prone / supine duplication ruled out (zero shared signatures over 1,728 acquisitions) | `ssn:docs/PATIENT_IDENTITY_SPEC.md` line 119; `mem:identity-audit-findings.md` | CURRENT; whether the 768 numeric-id and 34 `CTC-` records overlap as humans: NOT RECORDED | — |
| F.19 | known defects: 0533 truncated, repaired 2026-09-23 (job 40416624) and HF replaced (40419665); 16 records with no thoracic vertebra (2026-08-19 list); top labelled vertebra cut in 553 of 802; 27,738 detached label pieces in 741 records; six `pelvic_native` cases never reviewed; 0172 in the re-read queue; LCC post-processing deletes the loose lamina of a spondylolytic vertebra | `ctsp:zenodo/KNOWN_ISSUES.md`; `ctsp:docs/LAB_JOURNAL.md`; `ctsp:docs/RELEASE_CHECKLIST.md`; `mem:grid-ct-0533-truncated.md`; `mem:spondylolysis-and-border-anomaly-findings.md` | mixed; `KNOWN_ISSUES.md` (v10) lacks 0533, the mirrored CTs (tokens 75, 480) and COLONOG_299's misplaced L5 | — |
| F.20 | version progression with identical checks: fragmented labels 366 -> 1,146 (v3, ribs arrive) -> 377; rib offset 10.83 % -> 7.69 % (a version-comparison metric only) | `ctsp:docs/VERSION_PROGRESSION.md` (`ctsp:scripts/qc_version_progression.py`) | RECORD | — |

### F2. Spinopelvic and per-level measurements

| id | claim | file | status | feeds |
|---|---|---|---|---|
| F.21 | v11 spinopelvic over 756 of 802 records: PI 52.1 +/- 11.1, SS 36.6 +/- 10.6, PT 15.5 +/- 7.9, LL 51.7 +/- 13.3, PI-LL 0.3 +/- 10.3; medians PI 51.5, PT 15.0; plate gate rejects 44 (reason blank on 43); comparators Veilleux 2020 (n 200) 52.1 / 36.5 / 15.6, Hasegawa 2018 (n 24) 53.4 / 34.1 / 19.2 | `ctsp:morphometrics/surgical_morphometrics.csv` (`ctsp:scripts/extract_surgical_morphometrics.py`, commit 2232bde); recomputed from the CSV 2026-10-08 and matching | CURRENT (which two records besides the 44 lack PI: NOT RECORDED; commit 2232bde says 14 rejections, never checked against the CSV) | MPDA Table III; CNS v12_public deck |
| F.22 | estimator defects found and fixed: (1) label scheme assumed, not detected ("S1" -> C7, "femur_left" -> T4); (2) the S1 plate fitted two wrong ways (whole sacrum: median PI 54.7, 3.4 % impossible; carved: the near-vertical promontory face, SS near 88 on 9.4 %); (3) two wrong numbers summing correctly: SS ~9 degrees low and LL ~12 low on every case while PI = SS + PT held, caught only against outside references; (4) QC flags attached only when a value was None | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` §1-4 | fixed | MPDA |
| F.23 | the 128 low pelvic incidences: the 60-degree tilt gate was blind to direction (39 / 39 with PI <= 17 leaned posteriorly); a gate rejecting a normal with no anterior component was added; afterwards no PI below 22.4 or PT below -15 | commit 028210a; `SPINOPELVIC_ESTIMATOR.md` "Still open" | SOLVED 2026-09-11 | — |
| F.24 | SS 3.4 degrees low, PT 4.0 high, PI 0.5 high against Veilleux (pre-v11 reading): the anterior-pelvic-plane explanation fails on sign; the cohort explanation fits (Hasegawa: older, symptomatic, supine CT) | `SPINOPELVIC_ESTIMATOR.md` §5 | OPEN: the decisive experiment (fit the APP from the hip labels, report aSS = SS - APPA) not done | — |
| F.25 | still open in the estimator: eight records measure PI from a prosthetic femoral head; LSTV shifts PI by 10-15 degrees depending on which end-plate is called S1 (stratified sensitivity analysis not done); the anterior pelvic plane is not measured | `SPINOPELVIC_ESTIMATOR.md` "Still open" | OPEN (`ctsp:CLAUDE.md` "three that are still open") | — |
| F.26 | extraction script vs ostk on the same 300 records: PI median 49.2 vs 45.8; outside plausible 6.3 % vs 16.0 %; ostk's S1 surface fit is bimodal (28.3 % land on a steeper surface, PI near 18.6) | `SPINOPELVIC_ESTIMATOR.md` "Which estimator" | CURRENT (the release reports the extraction script) | MPDA |
| F.27 | six-lumbar readings (18 records): true L6 11, lumbarized S1 4, T12 with aplastic ribs 1, needs a reader 2 (0376, 1053) | `ctsp:results/six_lumbar_readings/report.txt`, `.png` (`ctsp:scripts/six_lumbar_readings.py`, `shift_hypothesis_test.py`) | CURRENT | — |
| F.28 | T12 vs L1 separable on shape alone (patient-median-normalised features, logistic regression, case-grouped folds): AUC 0.990, accuracy 97.3 % over 1,485 vertebrae; thoracic vs lumbar AUC 0.998; dominant feature transverse-process span | `ctsp:scripts/test_morphometric_separability.py`; `ssn:docs/LSTV_BENCHMARK.md` | CURRENT | MPDA Introduction; rule 4 of `PREREG_rules.md` |
| F.29 | rib-free count: 744 five, 29 four, 28 six, 1 blank (current CSV); 734 / 35 / 26 on 2026-08-19 | `ctsp:morphometrics/transition_morphometrics.csv`; `ctsp:docs/LAB_JOURNAL.md` | CURRENT for the CSV, which was written on v10 labels; recompute on v11 before any new claim | — |
| F.30 | lowest-rib ratio is bimodal (modes near 0.68-0.69 and 0.32-0.33) | `ctsp:paper/mpda/main.tex`; `LAB_JOURNAL.md`; `ctsp:paper/mpda/PLAN.md` | CURRENT | MPDA |
| F.31 | rib / lumbosacral co-occurrence: OR 19.6 over 796 (2x2 of TL/LS variants, `LAB_JOURNAL.md` 2026-08-19); OR 2.8, p 0.09 (stump ribs vs sacralization, commit e659ad4); CTSP OR 4.00 [1.00, 16.03] (voxel-flag master) | as named | DISPUTED: three definitions; none is in the MPDA (hypothesis tests are forbidden there; the Fisher test was removed, commit 2ba362f); the article reports counts only (stump ribs with 4 of 14 sacralizations vs 94 of 775 others) | MPDA (counts) |
| F.32 | canal depth, before the fix: L3 SD ~3.9 against the widest published 2.45; 157 of 736 records under 11 mm at L3 (21 %) against a congenital-stenosis prevalence of 2.62 % (Framingham) | `ctsp:docs/LEVEL_MORPHOMETRY.md` | SUPERSEDED (defect evidence; caught by spread, not the median) | — |
| F.33 | canal depth after the rewrite (pedicle-plane slab, midsagittal strip, ring closed only to find the hole): below-11 mm count 473 -> 12; per-level SD T11-L4 1.55-4.37 -> 1.55-2.04; L5 median 21.0 -> 17.4; about 5 % of levels rejected (reported missing) | same; `ctsp:scripts/extract_surgical_morphometrics.py` `_canal_column`, `_canal_ap` | CURRENT | MPDA Figure 3 |
| F.34 | end-plate width at L5: SD ~8.7 against 5.54; 95 of 760 over 60 mm (walking from the 48.81 mm body width toward the 85.91 mm transverse-process span); three fixes failed, a fourth lost on spread; **L5 end-plate width and L5 pedicle width are withheld** in `level_atlas.csv` and Figure 3; per-case CSVs keep raw L5 | same | CURRENT (withheld) | MPDA Figure 3 |
| F.35 | body height sits ~6 mm above Panjabi: estimator, tilt, millimetre scale and label dilation each excluded; the label edge sits 0.00 mm from where bone ends; what is left is 12 dried cadaveric spines vs 802 living patients over 50 | `ctsp:docs/BODY_HEIGHT_INVESTIGATION.md` (`ctsp:scripts/height_probe.py`, `edge_probe.py`, `render_height.py`) | CURRENT | MPDA |
| F.36 | pedicle width tracks 13 published series except L5 (20.70 vs 16.20; withheld); ostk reads L5 15.10 on individual cases | `SPINOPELVIC_ESTIMATOR.md` "Pedicle width" | CURRENT | MPDA Figure 3(c) |
| F.37 | ostk vs the extraction scripts over 802 records against Panjabi 1992: ostk closer on posterior body height at every level (L5 error +7.5 -> +2.3 mm), worse on every width (no transverse-process removal) | `ctsp:docs/OSTK_VS_EXTRACTION.md`; `ctsp:morphometrics/ostk_level_morphometry.csv` (commit 90a27a7, before the ostk regression) | CURRENT (the figure keeps the scripts' values) | — |
| F.38 | Panjabi 1991 page 892 Table 3 obtained by interlibrary loan 2026-09-13: EPWu T11 34.9 +/- 0.97, T12 39.0 +/- 0.58; VBHp T11 21.3 +/- 0.71, T12 22.7 +/- 1.04, now in `make_reference_table.py` | commit 83f7f95; `mem:panjabi-1991-page-892.md` | CURRENT; **the MPDA Figure 3 caption and `ctsp:paper/mpda/REPRODUCE.md` §2 still say "digitised from Figure 4A"** | MPDA Figure 3 |
| F.39 | sacral foramina counting does not work (93 cases x 81 settings; best 31-39 % per case) | `ctsp:docs/LAB_JOURNAL.md` "Negative results" (`ctsp:scripts/sweep_foramina_params.py`) | REFUTED | — |
| F.40 | the Castellvi screen recovers subtle grades and misses gross ones: IIb median leave-one-out rank 4, IIIb 442 | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` | CURRENT | — |
| F.41 | iliac crest >= 12 mm above L4-5 in 24.7 % (195 / 789) | `ctsp:README.md` "Release QC - v5"; `ctsp:paper/clinical/main.tex` | SUPERSEDED-PENDING: a v5-era number; touches the pelvis, so recompute on v11 before use | clinical paper |
| F.42 | PI does not separate by sex (51.3 vs 50.5); pelvic shape does; corrected pelvic inlet 131.4 mm women vs 125.4 men (6.5 mm against a published 6.8) | `ctsp:scripts/extract_pelvic_shape.py` docstring; `ctsp:morphometrics/pelvic_shape.csv` | the CSV was written 2026-09-10 on v10 labels with S1 = 29: recompute on v11 | — |
| F.43 | opportunistic L1 trabecular attenuation median 157.2 HU, n 801 | `ctsp:morphometrics/opportunistic.csv` | DATED (pre-v11; vertebral) | — |
| F.44 | four CSVs written before v11 that touch the sacrum or lumbosacral disc and must be recomputed: `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv` (L5-S1 disc height), plus `opportunistic.csv`, `proximal_femur.csv` (pre-v11, not sacral) | `ctsp:morphometrics/` (`git log`) | OPEN | — |
| F.45 | student pelvic-width demo: the committed report used S1 width (v10); the current script measures femoral-head separation | `ctsp:results/pelvic_width/report.txt`; `ctsp:scripts/demo_pelvic_width_dimorphism.py` | OPEN (stale report) | student project |

### F3. NeurIPS 2026 paper 3474 (CTSP line)

| id | claim | file | status |
|---|---|---|---|
| F.46 | every segmentation number was computed on the April 2026 release (1,153 records, ten-class scheme merged to nine, record-level split 805 train / 174 validation / 174 test of a 979-record pool), not on v11; the Castellvi grades are the September two-reader reads | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` rows 14-23 and "Version note" | CURRENT fact |
| F.47 | headline defect A: TotalSegmentator sacrum Dice 0.817 counts TS's separate S1 class as a miss (TS `sacrum` excludes S1; the whole sacrum is the union, `mem:ts-sacrum-excludes-s1.md`); defect B: junction comparisons subtract two window definitions | `CAMERA_READY_CHANGES.md` item 21 | OPEN: still in the main text |
| F.48 | per-case evidence for the camera-ready numbers | `Desktop/NeurIPS/bm/benchmark_per_case.csv`, `bm/benchmark_per_case_record_level.csv`, `ens/per_case_dice.csv`; recomputation scripts only in `<laptop Temp scratchpad, swept>/neurips_fixes/cr_apply/` | OPEN: copy the scripts into the repository before Temp is swept |
| F.49 | 134 `[pending]` slots in Appendices I (SPINEPS) and J (v11 summaries); their jobs (40481323 -> 40481314 -> 40481315; 40480728/31/32, 40480730/33; total_v3 40481824-26) were cancelled 2026-09-27 15:50 | `CAMERA_READY_CHANGES.md` items 19-20; `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | OPEN |
| F.50 | the twelve CNS 2026 student abstracts were computed by May 2026, before the spinopelvic-estimator and canal / end-plate fixes | `Desktop/openspineconsortium.github.io/contributions/manifest.json`; `ctsp:docs/SPINOPELVIC_ESTIMATOR.md`; `LEVEL_MORPHOMETRY.md` | NOT VERIFIED: whether the May numbers predate the fixes is not recorded; re-check before the posters are shown (2 Nov) |

---

## Part G. OpenSpineToolkit and the related tools

| id | claim | file | status |
|---|---|---|---|
| G.1 | 94 test functions across `tests/` (`tests/test_labels.py` covers scheme detection) | `ostk:tests/` (count of `def test_`) | CURRENT |
| G.2 | **regression**: commit 1b7005c (2026-09-10 22:52) added a 2 mm ring closing in `canal_mask`; the closing bridges the laminae, the anterior canal edge is taken as the wall and inherited by lower sections: case 0097 T12 VBHp 38.4 vs 28.9 mm, EPDl 52.0 vs 34.8; about one vertebra in seven inflated by 10-17 mm with no gate firing; `min_vox = 20` admits 3 mm "canals" (16 % of chords below the 11.07 mm living floor vs 2.6 % published). Do not trust ostk `level_morphometry` VBHp / EPD / EPWl computed after that commit; the committed `ostk_level_morphometry.csv` predates it | `mem:ostk-canal-closing-regression.md`; `ostk:ostk/vertebral_body.py` lines 98-132; renders `sn:results/reader_e/diag/*.png` | OPEN: no fix through cb43197 (2026-09-25); fix plan in the memory note; found by rendering |
| G.3 | **new finding 2026-10-08 (by reading code, not run)**: `LABELS_V10` still maps `"S1": 29`; on a v11 volume no voxel is 29, so `endplate_from_label(..., "S1", ...)` falls back to the whole sacrum, which the function's own docstring calls "a last resort ... drives pelvic incidence far too low", and no QC flag marks the fallback; `python -m ostk all` on v11 labels runs the branch documented as wrong | `ostk:ostk/labels.py` line 64; `ostk:ostk/spine.py` lines 473-474; `working_notes/topic6_ctspinopelvic1k_and_toolkit.md` §9.5 | OPEN; fix = port the extraction script's lowest-lumbar footprint isolation into ostk and flag the fallback |
| G.4 | `PDW` (pedicle width) is empty in all 4,744 rows of `ostk_level_morphometry.csv`; the 2026-09-10 shard run produced pedicle columns for about two of ~5,600 level-instances | `ctsp:morphometrics/ostk_level_morphometry.csv`; `SPINOPELVIC_ESTIMATOR.md` "Pedicle width" | unexplained |
| G.5 | post-operative synthesis (`ostk.surgery`): demo case 0003, ALIF L1-S1, age 50, LL 45.7 -> 55.0, PI-LL 9.8 -> 0.5, five cages; re-measuring the synthesised image collapses LL 45.7 -> ~24 (voxel roughness), so post-op numbers are carried analytically and the image is display only | `mem:postop-spine-synthesis.md`; `mem:postop-jaggedness-future.md` | prototype |
| G.6 | PolyPose (in `ssn:`): DeepFluoro reproduction "REPRODUCED" (Dice pelvis 0.992, femora 0.978 / 0.980; one pose-flip deviation documented); generator commit 1f4418f never pushed; `VALIDATION.{json,md}` does not exist; whether a bank was used in training is not recorded | `sn:results/polypose/REPRODUCTION.md`, `REPRODUCIBILITY.md`; `mem:polypose-generator-build.md` | OPEN (validation not written) |
| G.7 | the old ostk-primitive path read PI 3.6 / LL -8.9 on PIR case 0874 (truth 53 / 54); PolyPose now measures through the release plate fits (`tools/polypose/measure_sagittal.measure_image`) | `mem:polypose-generator-build.md` | CURRENT trap |
| G.8 | PACS X-ray demo latency 40,018 ms -> 1,360 ms (http redirect disabled WebGPU and service workers; COEP refused the CDN so onnxruntime-web is vendored; 1024 -> 640 export); since 2026-09-14 the X-ray model runs behind the level service | `mem:pacs-website-latency-root-cause.md`; website commit ea0086c | DATED |

---

## Where the catalog came from, and what it leaves to the notes

Each part condenses one reader note: parts A-C from `working_notes/topic1_schwingnet_carm_results.md` (§3-6), parts C2,
D and E from `working_notes/topic2_scaling_samples_anomaly_power.md`, part F from
`working_notes/topic6_ctspinopelvic1k_and_toolkit.md` (§3-6) and part G from topic 6 §9-11. The notes keep the full
contradiction tables (topic 1 §8, topic 2 Part E, topic 6 §14) and every unknown; `OPEN_QUESTIONS.md` gathers the
unknowns in one table.
