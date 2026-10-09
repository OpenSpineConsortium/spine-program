# In-domain evidence for Figure 5 (a) and (b): inventory, gaps, fill runs

2026-09-23. This file covers every measured point showing how accuracy moves when the model trains on data from
the same device, modality and view protocol it is tested on. Each point is one row of `points.csv`: 617 rows,
built by `tools/indomain_inventory.py build` from the result files. The tables are generated, and the narrative
numbers are transcribed from them and from `points.csv`; the tables
below sit between GENERATED markers and are rewritten on every build.

Grid jobs, all CPU, nothing trained or re-inferred:
- 40426955: first pass. The views part completed. The census part crashed on a binary label cache and was rerun.
- 40426979: census plus views.
- 40426987: views scored against the pre-repair truth, as a self-check.

Outputs are in `/rs/rs_grp_oschome/go2432/data/or_ready/indomain/` and are mirrored in `grid/`. Code:
`tools/indomain_audit.py` (grid), `tools/indomain_inventory.py` (local), `tools/indomain_fill_plan.py` (fill design).

## Correction, 2026-09-24: the lateral body-convention numbers below measure the box drawn, not the vertebra found

Point 1 below, and Table A's LAT columns for every arm without C-ArmLSpine frames, must not be read as "detectors that
never saw this C-arm find about 5 % of its lateral vertebrae". Those arms learn their boxes from whole-vertebra truth (COBRA,
DeepFluoro, the styled renders). On the C-ArmLSpine lateral test view, the body box and the whole-vertebra box of the same
vertebra have median IoU 0.329, and 97.8 % of the 138 pairs fall below 0.5. So a whole-vertebra box scores as a miss under
the body rule even when it sits on the right vertebra.

Under the convention-free `centre` rule of `tools/lcurve_score.py`, the stage-2 background with no C-ArmLSpine frame finds
87.7 % (363/414) of lateral vertebrae at conf 0.25, over 3 seeds. At conf 0.74, 308 of the 309 lateral vertebrae it finds carry
a whole-vertebra box. One render shows it: `detfill/convention_check_case100_LAT.jpg`.

The detection fill, `det_fill.json`, separates the two effects:
- `box_style` counts what each detector drew.
- `reading` gives body and centre side by side.
- An outline-label control tests what in-domain frames add when they carry the background's own box convention.

Read those before quoting any lateral body number for an arm that never saw C-ArmLSpine labels.

The in-domain effect is real once the box convention is controlled. The control relabels 24 C-ArmLSpine frames from 12
patients with whole-vertebra boxes. Under the centre rule at conf 0.74, compared with N = 0 over 3 seeds, paired over test
patients, those frames add:
- lateral: +16.2 pp [+10.7, +22.8] (381/414 vs 314/414);
- AP: +25.6 pp [+19.3, +32.2] (391/429 vs 281/429).

At the same N they also beat 24 COBRA frames (+28.5 pp lateral, +20.7 pp AP) and 24 styled renders (+15.7 pp lateral,
+27.0 pp AP). All intervals and k/n are in `det_fill.json` `reading`.

At conf 0.25 the gain is small: +1.4 pp lateral and +3.0 pp AP.

## What the existing evidence already shows

Every number below carries k/n and a case-clustered 95 % interval (percentile bootstrap, 2,000 resamples) unless
it says why it cannot.

1. **Detection on the C-arm lateral protocol comes from data of that protocol.** The measure is vertebral-body
   boxes on C-ArmLSpine, read against the repaired truth.
   - No arm without C-ArmLSpine frames finds more than 7 of 138 lateral vertebrae at confidence 0.25. The best
     is the DeepFluoro-only arm at 5.1 % (7/138) [0.7, 10.1].
   - The arms that do not see the device include: the other C-arms' real frames, their styled renders, this
     device's own-geometry styled renders, COBRA's wide arc, and renders only.
   - Their best AP result is 42.7 % (61/143) [34.0, 51.1], from the design-A arm trained on DeepFluoro plus COBRA.
   - Adding 50 frames from 25 C-ArmLSpine patients gives, at 0.25, 88.4 % (122/138) lateral [83.8, 93.3] and
     92.3 % (132/143) AP [88.3, 95.8]. At the pre-stated 0.74 the figures are 81.2 % (112/138) [75.5, 86.6] and
     85.3 % (122/143) [80.1, 90.1].
   - After that the curve is flat. From 50 to 210 frames, ALL at 0.74 moves only between 81.5 % (234/287)
     [76.8, 86.0] and 86.8 % (249/287) [82.3, 90.9], and every interval overlaps.
   - The knee lies somewhere between 0 and 50 frames and has not been measured (gap G1).
2. **Naming transfers from films on the lateral protocol and not on the AP.** Both figures below are for the
   whole frame.
   - Zero-shot lateral is 96.3 % (594/617) [93.1, 98.7]. In-domain case-grouped CV gives 98.2 % (606/617)
     [95.7, 100.0].
   - Zero-shot AP is 37.9 % (239/631) [29.6, 45.9]. In-domain gives 96.7 % (610/631) [93.6, 99.1].
   - The in-domain gain grows as the field shrinks. With one vertebra in view, AP rises from 17.3 % (102/591)
     [14.8, 20.0] to 65.1 % (385/591) [61.6, 68.8].
   - These are unpaired intervals on the same matched vertebrae. No paired zero-shot-versus-in-domain difference
     has been computed.
   - No in-domain N sweep exists (gap G2), so the shape of that rise is not known.
3. **In-domain data is necessary but not sufficient on its own.** This is measured on the 28-case test split,
   with 26 or 27 cases carrying matched vertebrae.
   - C-ArmLSpine crops alone recover whole-frame AP as well as the mixed recipe: 95.2 % (118/124) [86.1, 100.0]
     in both.
   - With few vertebrae in view they lose: AP at 3 vertebrae is 66.5 % (147/221) [55.6, 76.9] against 86.4 %
     (191/221) [78.5, 93.3] for the mixed recipe.
   - So collect one protocol and keep the general bank beside it. This reading rests on one split with wide
     intervals.
4. **The same device under a different acquisition protocol** is covered only by case134's CBCT spin: 301
   projections at 111 kVp. It is one patient, so no interval is valid.
   - The detector that saw spot frames of 105 other C-ArmLSpine patients finds 93.6 % (1127/1204) at 0.25.
   - The arms that never saw the device find 29.7 % (357/1204) to 49.5 % (596/1204).
5. **COBRA:** in its own training convention (whole-vertebra boxes, 893 vertebrae, 27 test patients, at 0.74),
   recall grows with patients, not frames:
   - 0 patients: 12.9 % (115/893) [8.6, 16.8];
   - 2 patients: 24.6 % (220/893) [16.9, 31.8];
   - 17 patients: 22.8 % (204/893) [15.6, 29.5] with seed 0 and 45.5 % (406/893) [34.5, 54.9] with seed 1;
   - 110 patients: 93.2 % (832/893) [86.4, 97.7].

   Under body truth, COBRA arms read from 1.3 % (11/855) [0.0, 3.2] to 40.2 % (344/855) [34.9, 46.1]. That is
   the convention mismatch recorded in `bodybox_rescore/RESCORE.md`, not a learning effect.
6. **DeepFluoro** has one test specimen, so no case-clustered interval exists, and its curve is not monotone
   (N=238 gives 13.3 %, 11/83). It cannot carry Figure 5.
7. **Films:** the only in-domain N sweep for films is the 2026-09-17 scaling sweep on the v2 bank.
   - Real-film fractions of 0.25, 0.5 and 1.0 give 83.7 % (1850/2210) [80.5, 86.8], 84.2 % (1862/2210)
     [80.9, 87.4] and 88.2 % (1950/2210) [85.3, 91.0] on ordinary lumbar. The intervals are film-clustered.
   - The v2 bank leaks people between splits, so those rows are NOT ESTABLISHED.

## Corrections to the task text and the stored files

- **The contribution-matrix numbers were quoted wrongly.** "Own-device only 86.8 % vs other-device only 12.9 %"
  does not describe those two numbers.
  - 86.8 % is COBRA-only (E) on held-out C-ArmLSpine, and 12.9 % is DeepFluoro-only (D). Both use the whole-vertebra
    OUTLINE convention.
  - Under the body convention the same arms read 11.1 % (32/287) [7.3, 15.5] and 3.8 % (11/287) [1.4, 7.0]
    stored. On the repaired truth they read 11.8 % (34/287) [7.9, 16.1] and 3.5 % (10/287) [1.4, 6.1].
  - Own-device-only (`only_carm`) reads 89.9 % (258/287) [84.5, 94.7] at 0.25 stored, or 91.6 % (263/287)
    [87.4, 95.3] on the repaired truth.
  - "Renders only 31.7 %" and "equal-count −47.7 pp" are also outline numbers. In the body convention they are
    2.4 % (7/287) [0.7, 4.5] and −8.0 pp; the second is a difference of stored cells with no paired interval
    (RESCORE D6).
- **The C-ArmLSpine truth was rebuilt between the stored cells and today.**
  - `realxray/carmlspine/meta` was rewritten on 2026-09-23 at 04:49–05:22. The −58° frame of case118 became
    `case118_OBL` and is no longer a lateral.
  - Every stored C-ArmLSpine detector cell (lcurve.json, contribution_matrix.json, a1) was scored before that,
    with 287 vertebrae including the oblique frame's 6.
  - Self-check: scoring every dump against `carmlspine_pre_repair_2026-09-23/meta` reproduces all 30 stored cells
    exactly (`views_selfcheck.json`).
  - On today's truth, the arms trained on C-ArmLSpine gain about 5 hits, because the repaired oblique now matches
    4 or 5 of its 6 bodies. Held-out arms move by at most 2. No direction changes.
  - **Figure 5 should plot the repaired-truth rows** (`view_*` in points.csv). The lateral protocol is then 27
    frames and 138 vertebrae; AP is 28 frames and 143 vertebrae.
- **lcurve.md has two display errors.** Its header says C-ArmLSpine is read "against the whole-vertebra OUTLINE
  truth", but `at` has been body since job 40417427; the outline reading is at `alt.outline`. It also prints
  "Test split: 56 frames, [] cases", which is an empty-list printing bug; there are 28 cases.
- **case134_sweep.md says the pooled detector saw case134's two spot frames. The lists say it did not.**
  - `devcorpus/lists/P_pooled/train.txt` and `val.txt` hold 0 case134 entries.
  - `dc_P_pooled/weights/best.pt` was written 2026-09-23 at 01:46. The case134 frames were written to
    `images/train` at 05:28.
  - The pooled 93.6 % is therefore patient-held-out. It remains one patient with no interval.
  - The `real_lodo` curve reads exactly 0.500 in 15 of 19 angle bins, which looks mechanical. It is unexplained
    and not inventoried as evidence of anything.
- **Pose donors.**
  - The styled renders in this device's own geometry (`surgio_b51_dr__surgio_b51_dr`) are TotalSegmentator
    subjects rendered under the registered poses of 148 C-ArmLSpine cases, all 28 test cases among them.
  - Every stage-2 learning-curve cell and `dc_P_pooled` therefore saw the test frames' geometry, but not their
    patients.
  - Under the patient rule the verdict does not change. For a figure about in-domain data it has to be stated, or
    removed (G4).
- **Two real-only detectors on the C-ArmLSpine target are NOT HELD OUT.**
  - For `rx_lodo_deepfluoro_1024` and `rx_lodo_cobra_elekta_1024`, the validation (checkpoint selection) set is
    the C-ArmLSpine TEST split: `carmlspine/labels/test.cache` for DeepFluoro, and the test directory for COBRA.
  - Their C-ArmLSpine cells (`lodo_df` and `lodo_cobra` in the contribution matrix and in views.json) must not be
    plotted.
  - The eval gate flagged the same selection for `rx_lodo_carmlspine_1024` on COBRA and DeepFluoro. Our list
    census agrees on that pair.

## How to read points.csv

| column | meaning |
|---|---|
| task | detection or naming |
| target_dataset / device / modality / view_protocol | where the test frames come from; `carmlspine_AP` / `_LAT` / `_OBL` are the view-split rows |
| training_domain | same device, other C-arm, film, vanilla render, styled render, or a `+` mix |
| training_detail | the arm, its run name, and any correction to the counts |
| n_train_frames_target, n_train_cases_target | unique real frames and cases **of the target dataset** in the checkpoint's own train list, from the grid census (lists read on disk). For crop banks, cases are counted from the bank's `case` array. The `rx_*` directories were read as they are today and corrected for case134 and case39_LAT2, which were written after training |
| k, n, value_pct, ci_lo_pct, ci_hi_pct | proportion with a case-clustered percentile bootstrap (2,000 resamples, seed 0). Naming rows on single crops cluster by person. One-cluster rows (DeepFluoro, case134, the OBL frame) carry no interval, and the `interval` column says so |
| box_convention | body (A28) is the paper convention. Whole-vertebra rows are kept only where no body truth exists (DeepFluoro) or where they are the target's own training convention (COBRA); both are labelled |
| heldout_status, heldout_check | our list intersection. The checkpoint's chain (itself plus every ancestor) train+val cases are intersected with the test cases, pose donors are reported separately, and unresolved links are named. The zero-shot level model's bank is deleted, so its verdict rests on timestamps (EVALUATORS.md §1.2) |
| source | file#key the number was read from |

## Tables (GENERATED; do not edit by hand)

### A. C-ArmLSpine detection, body boxes, repaired truth, split by protocol

Every row is a HELD OUT checkpoint by list intersection. The `lodo_df` and `lodo_cobra` arms are omitted because
they are not held out.

<!-- GENERATED:detection_carm -->
| training arm | domain | C-ArmLSpine train frames (cases) | ALL @0.74 | AP @0.74 | LAT @0.74 | ALL @0.25 | AP @0.25 | LAT @0.25 | held out |
|---|---|---|---|---|---|---|---|---|---|
| stage 1: other C-arms (real x2) + their styled renders (`dc_B_held_surgio_b51_dr_s1`) | other C-arm + styled render | 0 (0) | 12.5 (36/287) [9.0, 16.1] | 25.2 (36/143) [18.1, 32.2] | 0.0 (0/138) [0.0, 0.0] | 15.0 (43/287) [10.9, 19.1] | 30.1 (43/143) [21.9, 38.4] | 0.0 (0/138) [0.0, 0.0] | HELD OUT |
| stage 2, N = 0: + own-geometry styled renders (`lc_surgio_b51_dr_N0_s0`) | styled render (own geometry) + other C-arm | 0 (0) | 7.0 (20/287) [4.2, 10.1] | 14.0 (20/143) [8.4, 20.3] | 0.0 (0/138) [0.0, 0.0] | 8.0 (23/287) [4.7, 11.9] | 15.4 (22/143) [9.3, 22.5] | 0.7 (1/138) [0.0, 2.2] | HELD OUT |
| renders only (DeepFluoro geometry) (`render`) | vanilla/styled render only (DeepFluoro-geometry renders) | 0 (0) | 0.0 (0/287) [0.0, 0.0] | 0.0 (0/143) [0.0, 0.0] | 0.0 (0/138) [0.0, 0.0] | 2.4 (7/287) [0.7, 4.5] | 4.2 (6/143) [1.4, 7.6] | 0.7 (1/138) [0.0, 2.2] | HELD OUT |
| real frames of the other two C-arms only (a1 detector) (`lodo_carm`) | other C-arm | 0 (0) | 4.9 (14/287) [2.1, 8.1] | 9.1 (13/143) [4.1, 15.3] | 0.7 (1/138) [0.0, 2.2] | 4.9 (14/287) [2.1, 8.1] | 9.1 (13/143) [4.1, 15.3] | 0.7 (1/138) [0.0, 2.2] | HELD OUT |
| COBRA real + styled only (`dc_A_held_surgio_b51_dr_1dev_elekta_xvi`) | other C-arm + styled render | 0 (0) | 10.5 (30/287) [6.9, 14.3] | 21.0 (30/143) [13.9, 28.7] | 0.0 (0/138) [0.0, 0.0] | 11.8 (34/287) [7.9, 16.1] | 23.8 (34/143) [15.8, 32.4] | 0.0 (0/138) [0.0, 0.0] | HELD OUT |
| DeepFluoro real + styled only (`dc_A_held_surgio_b51_dr_1dev_cios_fusion`) | other C-arm + styled render | 0 (0) | 0.3 (1/287) [0.0, 1.1] | 0.7 (1/143) [0.0, 2.1] | 0.0 (0/138) [0.0, 0.0] | 3.5 (10/287) [1.4, 6.1] | 2.1 (3/143) [0.0, 4.7] | 5.1 (7/138) [0.7, 10.1] | HELD OUT |
| stage 2 + 50 C-ArmLSpine frames (`lc_surgio_b51_dr_N50_s0`) | same device + styled render + other C-arm | 50 (25) | 82.9 (238/287) [78.5, 87.2] | 85.3 (122/143) [80.1, 90.1] | 81.2 (112/138) [75.5, 86.6] | 89.9 (258/287) [85.9, 93.6] | 92.3 (132/143) [88.3, 95.8] | 88.4 (122/138) [83.8, 93.3] | HELD OUT |
| stage 2 + 100 frames, seed 0 (`lc_surgio_b51_dr_N100_s0`) | same device + styled render + other C-arm | 100 (50) | 83.3 (239/287) [79.4, 87.1] | 85.3 (122/143) [81.0, 89.5] | 81.2 (112/138) [76.4, 85.9] | 89.5 (257/287) [86.0, 93.0] | 93.0 (133/143) [89.0, 96.5] | 86.2 (119/138) [82.1, 90.4] | HELD OUT |
| stage 2 + 100 frames, seed 1 (`lc_surgio_b51_dr_N100_s1`) | same device + styled render + other C-arm | 100 (50) | 81.9 (235/287) [77.5, 86.2] | 84.6 (121/143) [80.0, 89.3] | 79.7 (110/138) [74.1, 85.3] | 90.6 (260/287) [86.7, 94.0] | 95.1 (136/143) [91.2, 98.6] | 87.0 (120/138) [82.0, 91.9] | HELD OUT |
| stage 2 + 200 frames, seed 0 (`lc_surgio_b51_dr_N200_s0`) | same device + styled render + other C-arm | 200 (100) | 81.5 (234/287) [76.8, 86.0] | 84.6 (121/143) [80.0, 89.3] | 79.0 (109/138) [71.7, 85.3] | 90.9 (261/287) [86.9, 94.7] | 92.3 (132/143) [87.8, 96.4] | 90.6 (125/138) [86.5, 94.8] | HELD OUT |
| stage 2 + 200 frames, seed 1 (`lc_surgio_b51_dr_N200_s1`) | same device + styled render + other C-arm | 200 (100) | 83.6 (240/287) [79.5, 87.7] | 84.6 (121/143) [80.0, 89.3] | 83.3 (115/138) [78.2, 88.3] | 90.9 (261/287) [86.9, 94.7] | 93.0 (133/143) [89.0, 96.5] | 89.9 (124/138) [85.3, 94.2] | HELD OUT |
| C-ArmLSpine real frames only (COCO init) (`only_carm`) | same device | 210 (105) | 85.7 (246/287) [81.5, 89.7] | 86.7 (124/143) [82.7, 90.8] | 84.8 (117/138) [80.1, 89.6] | 91.6 (263/287) [87.4, 95.3] | 94.4 (135/143) [89.9, 98.5] | 89.1 (123/138) [83.9, 94.1] | HELD OUT |
| C-ArmLSpine real + own styled only (`dc_A_held_cios_fusion_1dev_surgio_b51_dr`) | same device + styled render | 210 (105) | 85.0 (244/287) [80.6, 89.0] | 86.0 (123/143) [81.6, 90.1] | 84.1 (116/138) [79.6, 88.6] | 90.6 (260/287) [86.5, 94.6] | 92.3 (132/143) [87.8, 96.4] | 89.1 (123/138) [84.7, 93.4] | HELD OUT |
| real frames of all three C-arms (`pooled`) | same device + other C-arm | 210 (105) | 83.3 (239/287) [79.1, 87.2] | 86.0 (123/143) [82.1, 90.0] | 81.2 (112/138) [75.9, 86.3] | 92.3 (265/287) [88.6, 95.7] | 94.4 (135/143) [90.5, 97.9] | 90.6 (125/138) [85.9, 94.9] | HELD OUT |
| everything: styled renders + all real (`dc_P_pooled`) | same device + other C-arm + styled render | 210 (105) | 86.8 (249/287) [82.3, 90.9] | 86.0 (123/143) [81.6, 90.6] | 87.7 (121/138) [83.1, 92.6] | 91.3 (262/287) [87.7, 94.7] | 92.3 (132/143) [88.4, 95.8] | 90.6 (125/138) [86.5, 94.8] | HELD OUT |
<!-- /GENERATED:detection_carm -->

### A2. The three real L6 patients (case42, case121, case136): 6 frames, 35 vertebrae, 3 clusters

Read these as counts. With 3 clusters the interval is unreliable.

<!-- GENERATED:detection_trans -->
| cell | AP @0.74 | LAT @0.74 | ALL @0.74 |
|---|---|---|---|
| stage1_surgio_b51_dr | 27.8 (5/18) [0.0, 50.0] | 0.0 (0/17) [0.0, 0.0] | 14.3 (5/35) [0.0, 25.0] |
| lc_surgio_b51_dr_N0_s0 | 16.7 (3/18) [0.0, 33.3] | 0.0 (0/17) [0.0, 0.0] | 8.6 (3/35) [0.0, 16.7] |
| lc_surgio_b51_dr_N50_s0 | 77.8 (14/18) [66.7, 83.3] | 70.6 (12/17) [66.7, 80.0] | 74.3 (26/35) [66.7, 81.8] |
| lc_surgio_b51_dr_N100_s0 | 77.8 (14/18) [66.7, 83.3] | 70.6 (12/17) [66.7, 80.0] | 74.3 (26/35) [66.7, 81.8] |
| lc_surgio_b51_dr_N100_s1 | 77.8 (14/18) [66.7, 83.3] | 70.6 (12/17) [66.7, 80.0] | 74.3 (26/35) [66.7, 81.8] |
| lc_surgio_b51_dr_N200_s0 | 77.8 (14/18) [66.7, 83.3] | 64.7 (11/17) [50.0, 80.0] | 71.4 (25/35) [58.3, 81.8] |
| lc_surgio_b51_dr_N200_s1 | 77.8 (14/18) [66.7, 83.3] | 70.6 (12/17) [66.7, 80.0] | 74.3 (26/35) [66.7, 81.8] |
<!-- /GENERATED:detection_trans -->

### B. C-ArmLSpine naming: zero-shot against in-domain cross-validation

The table gives exact level over detector-matched vertebrae, at full coverage. The zero-shot model never saw a
C-arm frame. The CV folds train on 82–95 C-ArmLSpine cases (case-grouped) or 67–93 (day-grouped). The same
matched vertebrae are used in every column.

<!-- GENERATED:naming_cv -->
| field of view | view | zero-shot, all cases (no C-arm frame) | in-domain, case-grouped 5-fold CV | in-domain, acquisition-day 3-fold CV |
|---|---|---|---|---|
| whole frame | LAT | 96.3 (594/617) [93.1, 98.7] | 98.2 (606/617) [95.7, 100.0] | 92.5 (571/617) [87.7, 96.4] |
| whole frame | AP | 37.9 (239/631) [29.6, 45.9] | 96.7 (610/631) [93.6, 99.1] | 96.7 (610/631) [93.7, 99.1] |
| 5 vertebrae | LAT | 90.3 (602/667) [85.6, 94.5] | 97.0 (647/667) [93.3, 99.8] | 92.8 (619/667) [87.0, 97.4] |
| 5 vertebrae | AP | 47.1 (324/688) [38.7, 55.4] | 95.1 (654/688) [91.1, 98.3] | 93.6 (644/688) [88.0, 98.2] |
| 3 vertebrae | LAT | 86.9 (1010/1162) [83.1, 90.3] | 92.9 (1079/1162) [89.6, 95.6] | 87.6 (1018/1162) [83.3, 91.6] |
| 3 vertebrae | AP | 37.9 (446/1176) [33.0, 42.6] | 86.3 (1015/1176) [83.1, 89.4] | 85.0 (1000/1176) [81.5, 88.5] |
| 1 vertebra | LAT | 63.1 (381/604) [58.5, 67.6] | 72.8 (440/604) [69.0, 76.2] | 66.6 (402/604) [62.6, 70.6] |
| 1 vertebra | AP | 17.3 (102/591) [14.8, 20.0] | 65.1 (385/591) [61.6, 68.8] | 60.4 (357/591) [57.4, 63.7] |
<!-- /GENERATED:naming_cv -->

### B2. The released 28-case test split: zero-shot, mixed fine-tune, C-ArmLSpine-only fine-tune

The fine-tunes train on 103 C-ArmLSpine cases.

<!-- GENERATED:naming_test28 -->
| field of view | view | zero-shot | C-ArmLSpine crops mixed 1:1 with films/renders | C-ArmLSpine crops ONLY |
|---|---|---|---|---|
| whole frame | LAT | 93.7 (104/111) [83.5, 100.0] | 94.6 (105/111) [86.0, 100.0] | 89.2 (99/111) [76.4, 100.0] |
| whole frame | AP | 24.2 (30/124) [9.0, 41.7] | 95.2 (118/124) [86.1, 100.0] | 95.2 (118/124) [86.1, 100.0] |
| 5 vertebrae | LAT | 84.6 (99/117) [71.4, 95.1] | 94.9 (111/117) [84.1, 100.0] | 83.8 (98/117) [67.5, 100.0] |
| 5 vertebrae | AP | 34.4 (45/131) [16.4, 52.9] | 93.1 (122/131) [79.5, 100.0] | 77.9 (102/131) [60.1, 93.2] |
| 3 vertebrae | LAT | 82.2 (176/214) [72.8, 91.0] | 87.4 (187/214) [76.7, 96.3] | 77.1 (165/214) [66.5, 87.3] |
| 3 vertebrae | AP | 36.2 (80/221) [27.1, 45.5] | 86.4 (191/221) [78.5, 93.3] | 66.5 (147/221) [55.6, 76.9] |
| 1 vertebra | LAT | 60.2 (68/113) [50.5, 69.6] | 70.8 (80/113) [61.2, 79.7] | 73.5 (83/113) [65.1, 81.5] |
| 1 vertebra | AP | 15.5 (17/110) [8.9, 22.4] | 62.7 (69/110) [55.0, 70.4] | 58.2 (64/110) [50.9, 65.5] |
<!-- /GENERATED:naming_test28 -->

### C. Other targets

These are COBRA (whole-vertebra and body), DeepFluoro, the case134 spin, films, and single-crop naming, all at
0.74 where detection applies.

<!-- GENERATED:other_targets -->
| target | point | training domain | target train frames (cases) | value | convention | held out |
|---|---|---|---|---|---|---|
| cobra_elekta | det_elekta_xvi_points_stage_1_as_is_no_fine_tune__0.74_body | other C-arm | 0 (0) | 1.3 (11/855) [0.0, 3.2] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_stage_1_as_is_no_fine_tune__0.74_wv | other C-arm | 0 (0) | 10.1 (90/893) [6.7, 13.1] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_0_s0_0.74_body | styled render (own geometry) + other C-arm | 0 (0) | 1.5 (13/855) [0.1, 2.9] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_0_s0_0.74_wv | styled render (own geometry) + other C-arm | 0 (0) | 12.9 (115/893) [8.6, 16.8] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_48_s0_0.74_body | same device + styled render + other C-arm | 48 (2) | 12.2 (104/855) [8.2, 15.9] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_48_s0_0.74_wv | same device + styled render + other C-arm | 48 (2) | 24.6 (220/893) [16.9, 31.8] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_96_s0_0.74_body | same device + styled render + other C-arm | 96 (4) | 12.9 (110/855) [8.1, 17.0] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_96_s0_0.74_wv | same device + styled render + other C-arm | 96 (4) | 22.1 (197/893) [15.5, 28.0] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_192_s0_0.74_body | same device + styled render + other C-arm | 192 (8) | 12.5 (107/855) [7.7, 16.8] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_192_s0_0.74_wv | same device + styled render + other C-arm | 192 (8) | 31.2 (279/893) [20.5, 40.8] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_408_s0_0.74_body | same device + styled render + other C-arm | 408 (17) | 10.6 (91/855) [6.5, 14.5] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_408_s0_0.74_wv | same device + styled render + other C-arm | 408 (17) | 22.8 (204/893) [15.6, 29.5] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_96_s1_0.74_body | same device + styled render + other C-arm | 96 (4) | 4.6 (39/855) [2.3, 6.8] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_96_s1_0.74_wv | same device + styled render + other C-arm | 96 (4) | 19.0 (170/893) [15.3, 23.2] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_408_s1_0.74_body | same device + styled render + other C-arm | 408 (17) | 8.8 (75/855) [5.0, 12.4] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_points_N_408_s1_0.74_wv | same device + styled render + other C-arm | 408 (17) | 45.5 (406/893) [34.5, 54.9] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_pooled_real_0.74_body | same device + other C-arm | 2640 (110) | 35.8 (306/855) [29.5, 42.0] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_pooled_real_0.74_wv | same device + other C-arm | 2640 (110) | 93.2 (832/893) [86.4, 97.7] | whole-vertebra | HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_C_ArmLSpine_held_out_0.74_body | same device + other C-arm (C-ArmLSpine excluded) | 2640 (110) | 26.3 (225/855) [20.5, 33.0] | body | NOT HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_C_ArmLSpine_held_out_0.74_wv | same device + other C-arm (C-ArmLSpine excluded) | 2640 (110) | 91.2 (814/893) [83.4, 96.3] | whole-vertebra | NOT HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_renders_all_real_0.74_body | same device + other C-arm + styled render | 2640 (110) | 40.2 (344/855) [34.9, 46.1] | body | HELD OUT |
| cobra_elekta | det_elekta_xvi_all_real_all_real_renders_all_real_0.74_wv | same device + other C-arm + styled render | 2640 (110) | 94.3 (842/893) [88.4, 98.0] | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_stage_1_as_is_no_fine_tune__0.74_wv | other C-arm | 0 (0) | 69.9 (58/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_0_s0_0.74_wv | styled render (own geometry) + other C-arm | 0 (0) | 9.6 (8/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_48_s0_0.74_wv | same device + styled render + other C-arm | 48 (1) | 33.7 (28/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_127_s0_0.74_wv | same device + styled render + other C-arm | 127 (3) | 79.5 (66/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_238_s0_0.74_wv | same device + styled render + other C-arm | 238 (4) | 13.3 (11/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_103_s1_0.74_wv | same device + styled render + other C-arm | 103 (2) | 49.4 (41/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_points_N_214_s1_0.74_wv | same device + styled render + other C-arm | 214 (3) | 55.4 (46/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_all_real_all_real_pooled_real_0.74_wv | same device + other C-arm | 238 (4) | 73.5 (61/83) | whole-vertebra | HELD OUT |
| deepfluoro | det_cios_fusion_all_real_all_real_C_ArmLSpine_held_out_0.74_wv | same device + other C-arm (C-ArmLSpine excluded) | 238 (4) | 78.3 (65/83) | whole-vertebra | NOT HELD OUT |
| deepfluoro | det_cios_fusion_all_real_all_real_renders_all_real_0.74_wv | same device + other C-arm + styled render | 238 (4) | 80.7 (67/83) | whole-vertebra | HELD OUT |
| carmlspine | name_singlecrop_v9_carm_test | film + render (no C-arm frame) | 0 (0) | 54.8 (125/228) [49.0, 60.5] | n/a | HELD OUT |
| cobra_elekta | name_singlecrop_v9_cobra_test | film + render (no C-arm frame) | 0 (0) | 22.6 (66/292) [15.3, 28.5] | n/a | HELD OUT |
| nhanes_film | cmp_film_target_film_conf_0.05 | same modality (film-trained detector, detect_v5z_final) |  () | 99.1 (231/233) | body | NOT HELD OUT |
| nhanes_film | cmp_film_target_render_conf_0.05 | vanilla render only (anchor_det_v1, no real image) | 0 (0) | 71.7 (167/233) | body | HELD OUT |
| nhanes_film | cmp_film_target_film_conf_0.25 | same modality (film-trained detector, detect_v5z_final) |  () | 98.7 (230/233) | body | NOT HELD OUT |
| nhanes_film | cmp_film_target_render_conf_0.25 | vanilla render only (anchor_det_v1, no real image) | 0 (0) | 43.3 (101/233) | body | HELD OUT |
| case134 | case134_pooled_0.25 | same device (spot frames) + other C-arm + styled render | 210 (105) | 93.6 (1127/1204) | body | HELD OUT |
| case134 | case134_pooled_0.74 | same device (spot frames) + other C-arm + styled render | 210 (105) | 78.1 (940/1204) | body | HELD OUT |
| case134 | case134_lodoA_0.25 | other C-arm + styled render | 0 (0) | 37.2 (448/1204) | body | HELD OUT |
| case134 | case134_lodoA_0.74 | other C-arm + styled render | 0 (0) | 29.2 (351/1204) | body | HELD OUT |
| case134 | case134_lodoB_0.25 | other C-arm + styled render | 0 (0) | 29.7 (357/1204) | body | HELD OUT |
| case134 | case134_lodoB_0.74 | other C-arm + styled render | 0 (0) | 23.5 (283/1204) | body | HELD OUT |
| case134 | case134_real_lodo_0.25 | other C-arm (real only) | 0 (0) | 49.5 (596/1204) | body | HELD OUT |
| case134 | case134_real_lodo_0.74 | other C-arm (real only) | 0 (0) | 49.4 (595/1204) | body | HELD OUT |
| film_v2_heldout | film_scaling_s000_r100_ordinary_lumbar | film + render | 1.0 of the v2 film train split () | 89.5 (1977/2210) [86.9, 92.0] | n/a | NOT ESTABLISHED |
| film_v2_heldout | film_scaling_s025_r100_ordinary_lumbar | film + render | 1.0 of the v2 film train split () | 87.6 (1937/2210) [84.6, 90.5] | n/a | NOT ESTABLISHED |
| film_v2_heldout | film_scaling_s050_r100_ordinary_lumbar | film + render | 1.0 of the v2 film train split () | 87.4 (1931/2210) [84.3, 90.2] | n/a | NOT ESTABLISHED |
| film_v2_heldout | film_scaling_s100_r025_ordinary_lumbar | film + render | 0.25 of the v2 film train split () | 83.7 (1850/2210) [80.5, 86.8] | n/a | NOT ESTABLISHED |
| film_v2_heldout | film_scaling_s100_r050_ordinary_lumbar | film + render | 0.5 of the v2 film train split () | 84.2 (1862/2210) [80.9, 87.4] | n/a | NOT ESTABLISHED |
| film_v2_heldout | film_scaling_s100_r100_ordinary_lumbar | film + render | 1.0 of the v2 film train split () | 88.2 (1950/2210) [85.3, 91.0] | n/a | NOT ESTABLISHED |
<!-- /GENERATED:other_targets -->

### D. Held-out tally

<!-- GENERATED:heldout -->
| verdict | rows |
|---|---|
| HELD OUT | 567 |
| NOT HELD OUT | 32 |
| NOT ESTABLISHED | 18 |

Rows that are NOT HELD OUT (never plot these as held-out evidence):

- `det_elekta_xvi_all_real_all_real_C_ArmLSpine_held_out_0.74_body`: list intersection cobra_test: 27/27 test cases in chain train+val ['A053', 'A169', 'A268', 'A280', 'A294', 'B005']; as pose donors of styled renders 0/27; a train/val DIRECTORY was read as it is today
- `det_cios_fusion_all_real_all_real_C_ArmLSpine_held_out_0.74_wv`: list intersection df_test: 1/1 test cases in chain train+val ['18-1109']; as pose donors of styled renders 0/1; a train/val DIRECTORY was read as it is today
- `cm_lodo_df_carmlspine_outline`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; label caches name val=carmlspine/test; a train/val DIRECTORY
- `cm_lodo_cobra_deepfluoro_default`: list intersection df_test: 1/1 test cases in chain train+val ['18-1109']; as pose donors of styled renders 0/1; a train/val DIRECTORY was read as it is today
- `cm_lodo_cobra_carmlspine_outline`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; a train/val DIRECTORY was read as it is today
- `cm_lodo_carm_deepfluoro_default`: list intersection df_test: 1/1 test cases in chain train+val ['18-1109']; as pose donors of styled renders 0/1; a train/val DIRECTORY was read as it is today
- `cm_lodo_carm_cobra_elekta_default`: list intersection cobra_test: 27/27 test cases in chain train+val ['A053', 'A169', 'A268', 'A280', 'A294', 'B005']; as pose donors of styled renders 0/27; a train/val DIRECTORY was read as it is today
- `view_sweeps__lodo_cobra__carm_test_ALL_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; a train/val DIRECTORY was read as it is today
- `view_sweeps__lodo_cobra__carm_test_AP_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; a train/val DIRECTORY was read as it is today
- `view_sweeps__lodo_cobra__carm_test_LAT_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; a train/val DIRECTORY was read as it is today
- `view_sweeps__lodo_cobra__carm_test_OBL_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; a train/val DIRECTORY was read as it is today
- `view_sweeps__lodo_df__carm_test_ALL_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; label caches name val=carmlspine/test; a train/val DIRECTORY
- `view_sweeps__lodo_df__carm_test_AP_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; label caches name val=carmlspine/test; a train/val DIRECTORY
- `view_sweeps__lodo_df__carm_test_LAT_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; label caches name val=carmlspine/test; a train/val DIRECTORY
- `view_sweeps__lodo_df__carm_test_OBL_0.74`: list intersection carm_test: 28/28 test cases in chain train+val ['case10', 'case100', 'case11', 'case112', 'case114', 'case116']; as pose donors of styled renders 0/28; label caches name val=carmlspine/test; a train/val DIRECTORY
- `cmp_film_target_film_conf_0.05`: eval gate family render_vs_film
<!-- /GENERATED:heldout -->

## Gaps that stop a curve from being drawn, and the fill run for each

The cell lists come from `tools/indomain_fill_plan.py`, which proves before writing anything that every
committed subset is unchanged (`fill/FILL_CHECK.json`: `existing_identical` is true for all 7). Nothing has
been submitted.

### G1. Detection has no C-ArmLSpine point between 0 and 50 real frames

**Runs.** The 19 cells in `fill/lcurve_fill_manifest.txt`:
- N = 2, 4, 10 and 20 frames (1, 2, 5 and 10 cases), each with seeds 0, 1 and 2.
- N = 50 with seeds 1 and 2; N = 100 and 200 with seed 2.
- N = 0 with seeds 1 and 2, which measures the training-seed floor.
- N = 208 (all 104 pool cases) with seed 0, as the same-recipe endpoint.

**Subsets.**
- They are drawn by `lcurve_lists.draw()` with the ladder extended downward, over the census the committed curve
  used (`fill/lcurve_cases_2026-09-23T0136.json`: 104 cases, 2 frames each, case121 excluded).
- Every pool case has 2 frames, so each subset is a prefix of the seed's shuffled order. That makes the new cells
  nested inside the existing N = 50.
- The subsets are in `fill/subsets_fill.json`, a verified superset of `SchwingNet/results/lcurve/subsets.json`.

**Code change needed before submission.** `tools/lcurve_lists.py` counts real frames with `glob(f"{c}_*.png")`.
Since 2026-09-23, `images/train/` also holds `case39_LAT2.png`, so `build()` will REFUSE every cell whose subset
contains case39: s0 N208, s1 N20/N50, and s2 N20/N50/N100/N200. Make `census()` and `build()` count only
`{case}_AP.png` and `{case}_LAT.png` for carmlspine. That is the rule the committed subsets were drawn under.
The same edit carries the view filter that G3 needs:

```python
# lcurve_lists.py, build() and census(), for real == "carmlspine" only
VIEWS = os.environ.get("LCURVE_VIEWS", "AP,LAT").split(",")
frames = [p for v in VIEWS for p in [os.path.join(RX, real, "images", "train", f"{c}_{v}.png")] if os.path.exists(p)]
# and suffix run / list names with the view when LCURVE_VIEWS != "AP,LAT" (lc_surgio_b51_dr_N50_s0_LAT)
```

**Commands.** On the grid clone, with the patch scp'd in and CRLF stripped:

```bash
cp SchwingNet/results/indomain/fill/subsets_fill.json SchwingNet/results/lcurve/subsets.json   # superset, existing entries identical
sbatch -D ~/spinesurg-ct-nnunet --array=0-18 --export=ALL,MANIFEST=SchwingNet/results/indomain/fill/lcurve_fill_manifest.txt SchwingNet/slurm/lcurve.sh
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<array> SchwingNet/slurm/indomain_audit.sh   # re-scores every dump ALL / AP / LAT / OBL on the repaired truth
```

**Scoring.** `lcurve_train.py` already scores each cell with `lcurve_score.py` (case-clustered bootstrap, body
convention). `indomain_audit.py views` picks up the new dumps through its glob and splits them by protocol.

**Cost.** 19 GPU cells. The committed 19 cells took about 2 h each on gvohp/galhp (array 40416378).

### G2. Naming has no in-domain N sweep, only zero-shot against all cases

**Runs.** The 80 cells in `fill/naming_fill_manifest.txt`, across the 5 case-grouped folds:
- N = 2, 5, 10 and 20 C-ArmLSpine training cases, each with seeds 0, 1 and 2.
- N = 40 with seeds 0 and 1.
- N = 0 with seed 0.
- N = all with seed 0.

**Subsets.**
- The fold rule is that of `tools/carmlspine_to_bank.py`: `md5(case) % 5 == K` is the test fold and `(K + 1) % 5`
  is the val fold.
- Within a fold's training cases, `random.Random(1000*K + seed)` shuffles once and N takes the first N, so the
  subsets are nested. They are in `fill/naming_subsets.json`.
- Both views of each case are kept. Val and test folds stay fixed at every N.

**Recipe.** The recipe is `slurm/carmlspine_cv.sh`, verbatim except for N and the seed. It fine-tunes from
`allspine_v2_r1`, merges 1:1 with the `allspine_v7` sample (`merge_banks --per-class 600 --real-share 0.5`),
trains `train_level_classifier --epochs 15 --lr 1e-4 --augment 2` and then `head_mixed_length --train-mode mixed`.
Keeping the recipe means N = all reproduces a4 within the release repair.

**Code change needed.**
- `carmlspine_to_bank.py` needs `--train-cases <json list>`: after `fold_split`, skip train-split cases not in the
  list. This is five lines, and val and test are untouched.
- N = 0 is the same call with an empty list. The merged bank is then the base sample plus the C-ArmLSpine
  val-fold crops, which are kept for checkpoint selection as at every N.
- Pass `--seed s` to `merge_banks`, `train_level_classifier` and `head_mixed_length`. Tag the outputs
  `cv{K}_N{n}_s{s}` and write the proto output to `/rs/.../carmlspine/proto_fill/N{n}_s{s}/cv_fold{K}`.

**Evaluation.**
- Evaluate `det` boxes only, at `kfull`, `k3` and `k1`. That is 3 prototype passes instead of 12.
- Aggregate each (N, seed) with the a4 code path: `rigor_fixes.cv_items(root, "cv_fold*", "det")` and then
  `prop_ci(items, "case", "exact")` per view and k.

**Known distortion.** With `--real-share 0.5`, the repeat factor is about (base crops ÷ real crops). The shipped
fold-0 bank holds about 15,700 base crops, so N = 2 cases tiles a few dozen real crops several hundred times.
Record the repeat factor, which `merge_banks` prints. If it dominates, add a capped-repeat arm; do not change the recipe
silently.

**Protocol arm.** Add `--views LAT` (lateral crops only) and `--views AP` at N = all: 5 folds × 2 = 10 cells. This
asks whether in-domain lateral data fixes AP naming, and the reverse.

**Cost.**
- About 90 GPU jobs. The limit is 6 h each, and most time goes to bank building and 15 epochs.
- A cheaper pilot on the released 103/28 split has 19 cells (`slurm/carmlspine_finetune.sh` pattern), but its
  test intervals are about ±9 pp.

**Release changes.** The fill folds include case134 (restored 2026-09-23) and score case118's oblique frame as
OBL, not LAT. The fill's N = all is therefore the new baseline, and a4 is its check.

### G3. AP and lateral are not separated in the detection curve

**(i) Scoring: FILLED here.** `grid/views.json` holds every existing C-ArmLSpine dump in both views: 38 dumps.
That covers 6 stage-2 learning-curve cells, 18 device-corpus arms (stage 1 among them), 7 real-only sweeps and
7 transitional dumps. The split uses the
same scorer and the same bootstrap, and the views sum to ALL for every dump. Table A is the result.

**(ii) Training on one protocol: not fillable by scoring.** The 12 cells in `fill/protocol_fill_manifest.txt`
train on one view only:
- LCURVE_VIEWS=AP or LAT.
- Cases are taken from the both-view subsets s{seed}/N10, N50 and N208, giving 5, 25 and 104 cases at one frame
  per case.
- Seeds 0 and 1.

Each cell is scored on both views, which gives the cross-protocol cell (AP-trained read on LAT). There are two
comparators:
- the both-view cell with the same cases (N = 10, 50, 208), for the same patients;
- the both-view cell with the same frame count (N = 4 against 5 cases, and so on), for the same images.

This needs the G1 patch.

```bash
sbatch -D ~/spinesurg-ct-nnunet --array=0-11 --export=ALL,MANIFEST=<protocol manifest as "device N seed">,LCURVE_VIEWS=<AP|LAT per line> SchwingNet/slurm/lcurve.sh
```

`lcurve.sh` reads three fields per line. A two-line wrapper should export `LCURVE_VIEWS` from the fourth field of
`protocol_fill_manifest.txt`.

### G4. Pose-donor overlap in every stage-2 cell

The own-geometry styled corpus borrows the poses of all 28 C-ArmLSpine test cases. That is reported, and it
does not change the verdict.

**Run.** Rebuild the stage-2 lists without styled renders whose filename names a test-split case: the census
found them by `case\d+` in the stem. Rerun N = 0 s0 and N = 50 s0 (2 cells) to measure the effect before deciding
whether the fill cells need it. The mechanism is an env var in `lcurve_lists.build()` that drops `own_tr` entries
matching the test cases.

### G5. COBRA has no fair body-convention curve

COBRA's real training truth is whole-vertebra (planning-CT projected). No body number is a learning effect until
the G4 body-box rebuild (RESCORE.md), so this is not a fill run. Plot COBRA, if at all, in its own convention
and label it.

### G6. DeepFluoro has one test specimen

No interval exists, and the curve is not monotone. The only fix is a leave-one-specimen-out curve over the 6
specimens. The recommendation is to leave DeepFluoro out of Figure 5.

### G7. Transitional patients

There are 3 patients and 35 vertebrae, so no interval is usable. Figure 6's transitional renders are the
instrument for that question.

### G8. Films

The film N sweep exists only on the leaky v2 bank. A clean one would take `slurm/scaling_sweep.sh` with
`BASE=~/allspine_v9_fov96_ctx` (6 GPU points, 40 h limit). It is needed only if Figure 5 must show film.

## Suggested Figure 5 (a) and (b), from what exists now plus G1 and G3

- **(a) Detection.**
  - x axis: C-ArmLSpine training frames (cases), on a log scale with 0 drawn apart.
  - y axis: body recall at 0.74 (pre-stated), one line for AP and one for LAT (Table A, repaired truth).
  - Reference points at x = 0: other C-arms, renders only, own-geometry renders.
  - The G1 cells fill the 0–50 range; the G3 (ii) cells add AP-only and LAT-only training.
- **(b) Naming.**
  - Grouped bars or dots of exact level: zero-shot against in-domain, by protocol (AP, LAT) and field of view
    (whole frame, 3 vertebrae, 1 vertebra), from Table B.
  - Once G2 lands this becomes a curve over training cases.
