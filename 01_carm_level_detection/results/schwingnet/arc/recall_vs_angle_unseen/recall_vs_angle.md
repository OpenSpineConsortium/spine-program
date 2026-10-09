# Recall vs C-arm angle (render sweep; held out under tools/eval_gate.py)

## Read this first (hand-written 2026-09-24; everything between the COMPARE markers is machine-written)

This curve replaces `../recall_vs_angle_selection_leaked/`, which was void: it was scored on the 17 subjects three of
the four detectors kept `best.pt` on. The set here is 40 TotalSegmentator v3 subjects that no scored detector, and
no checkpoint any of them was initialised from, trained or was selected on. The same anchor, angles, tilts, cards,
down-sampling and seed were used as in the void run, and the same scorer.

**How "held out" was established, twice.** `tools/eval_gate.py` passes every subject for every detector at three
points: at the choice (`subjects.json`), before rendering, and before scoring. The first key of
`recall_vs_angle.json` is the verdict: overlap 0, unresolved 0. The rx_lodo chain was followed to
anchor_none_v2_17-1882 and from there to the public COCO `yolo11m.pt`. A second check, independent of the gate code
(grid job 40429294; `indep_check/indep_check.json` and `indep_check/grid_indep.py` here, the rest in `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/arc_unseen/indep_check/`), read every `args.yaml` → `data.yaml` → train and val
list or image directory on each chain and took every `s####` token:
- **0 of the 40** occur in any train or val set of dc_P, dc_A, dc_B, rx_lodo or anchor_none_v2.
- The same scan finds all 17 void subjects in the dc_P, dc_A and dc_B val sets, 5 of them in anchor_none_v2's train
  set and 1 in its val set. That is the positive control.
- No chosen CT is filed under another TotalSegmentator id, and no chosen id was reissued between v201 and v300.
- The render parameters match the void run field for field.

Every headline recall was recomputed from `matches.json` with separate code and matched to three decimals.

**Did the conclusion change?**
1. **Where recall falls off: no.** The pooled detector drops below 90% of its lat-0 recall at −30°/+30° on both
   cards. The void run gave −30°/+30° on Elekta and −30°/+40° on Surgio. Of the 11 body curves with lat-0 recall ≥ 0.5
   in both runs, 8 put their falloff angles within one 10° grid step of the void values.
2. **Lat 0: no.** Pooled recall is 0.87 against 0.89 on Elekta and 0.92 against 0.91 on Surgio. Both difference
   intervals span 0: −0.02 [−0.13, +0.10] and +0.01 [−0.07, +0.10]. The selection leak did not measurably raise the
   centre of the curve.
3. **The lateral end: yes, and upward.** Pooled recall on Elekta rises from 0.39 to 0.64 at −90° (+0.25 [+0.02,
   +0.48]) and from 0.35 to 0.69 at +90° (+0.34 [+0.09, +0.56]). On Surgio it rises from 0.79 to 0.99 at −90° (+0.20
   [+0.06, +0.36]). LODO A rises at most angles. Removing a leak can only lower recall, so these rises come from the
   change of subjects, not from the leak.
   - How the sets differ: 10 of the void 17 were polytrauma CTs, and 3 had the sacrum cut by the scan. The new set
     holds no polytrauma CT, because every eligible polytrauma subject is among the 142 the detectors trained or were
     selected on.
   - Within the void set, the polytrauma subjects scored lower at ±90° than the others. Pooled recall was 0.33
     against 0.47 on Elekta and 0.72 against 0.96 on Surgio (means of per-subject recall).
   - That is consistent with the subjects explaining the rise. It was not tested further.
   - The void statement "pooled recall on the Elekta card collapses to 0.35–0.39 at the laterals" does not stand.
     The statement "on the Surgio card recall dips near ±50° and recovers at the laterals" does stand, more strongly:
     0.69 at −50° and 0.99 at −90°.

**New, and it limits how any number on this set can be read: the anchor alone scores about 0.67.**
- The arc set places every subject's L3 on one anchor, so at any given angle all 40 subjects' boxes fall in nearly
  the same place. Scoring another subject's TRUTH boxes against a subject's truth gives body recall 0.64–0.68 at
  every angle from −90° to +90° (`tools/arc_prior_check.py`, grid job 40429412, `prior_check.json`).
- Blank frames produce no boxes from any detector, so no detector is emitting a fixed layout.
- The pooled detector scores a subject's own frame above another subject's frame at the same angle in 15 of 18
  (angle, card) cells, by +0.17 to +0.29, each paired interval above 0. It is reading the frame in front of it. That
  includes the Surgio laterals (+0.28 and +0.29), where no vertebral body can be seen by eye.
- But at ±70° and ±90° on the Elekta card, pooled recall (0.59–0.69) is at the anchor floor. LODO A clears the floor
  only within about ±20° of AP on the Elekta card (0.80 at lat 0, against 0.68). LODO B never clears it.
- Read recall on this set against about 0.67, not against 0. The metric is per-body and class-level, at IoU 0.5,
  and it does not check which vertebra a box names.

**Caveats that stand.**
- *Surgio-card lateral underexposure.* The surgio_b51_dr card renders the thick lateral view as photon-starved
  mottle, while real C-ArmLSpine laterals show readable bodies. The pooled detector trained on this card's mottle,
  and it does extract subject-specific signal from it (see the previous item). Its 0.96–0.99 at Surgio ±90° is
  therefore performance on the card's rendering of a lateral, not on a real lateral. All 40 lateral frames are in
  the contact sheet `indep_check/sheet_new_surgio_b51_dr_lat-090.png`.
- *Elekta half-fan blades.* The blades black out part of the panel at every angle, and boxes under them count as
  misses (contact sheet `indep_check/sheet_new_elekta_xvi_lat+000.png`).
- *Children.* 5 of the 40 are children or small scans of unknown age: s1487 (age 0), s1540 (8), s1547 (7), s1741
  (5) and s2106 (age not recorded, 24 cm field). For comparison, 14 of the 125 training subjects and 3 of the void 17
  were children. Pooled lat-0 recall on Elekta is 0.47 on the four children of known age and 0.92 on the 35 adults.
- *Real-frame LODO* (rx_lodo_carmlspine_1024) is clean on these 40 through its whole chain, so it stays in the
  curve. It detects almost nothing at any angle, as before. It is labelled render-initialised, never "real-only".

Jobs: select 40428068 · render 40428069/70/71 · score 40428072 · independent check 40429294 · prior check 40429412.
Grid: set `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep_unseen`, outputs
`/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/arc_unseen/` (with `matches.json`, `survey.json`).

<!-- BEGIN:COMPARE -->

## Subjects, and what changed from the void curve

**40 TotalSegmentator v3 subjects, held out for all 4 detectors under `tools/eval_gate.py`**: for each, the patient is in neither the train nor the val set of the checkpoint nor of any checkpoint in its initialisation chain (`eval_gate` block, first key of `recall_vs_angle.json`; `checks`: devcorpus/dc_P_pooled/weights/best.pt overlap 0, 0 ancestor(s), devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt overlap 0, 0 ancestor(s), devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt overlap 0, 0 ancestor(s), realxray/rx_lodo_carmlspine_1024/weights/best.pt overlap 0, 1 ancestor(s)).

Chosen by `tools/arc_unseen_subjects.py` (`subjects.json`): random.Random(0).sample(sorted(eligible), 40), then sorted from 353 eligible of 1939 (first failing reason: anatomy 1246, eligible 353, lr_cut 142, gate 141, identity 57). Criteria: identity -- the CT is not byte-identical to, nor a same-shape-and-affine re-export of, a CT under a different TotalSegmentator id, and its id names no different CT in the other release; gate -- tools/eval_gate.assess holds out for every --weights (train AND val of the checkpoint and every ancestor; unresolved is not clean); anatomy -- vertebrae_T12, vertebrae_L1, vertebrae_L2, vertebrae_L3, vertebrae_L4, vertebrae_L5, sacrum: each >= 200 voxels and touching no face of the volume; hip_left, hip_right: each >= 200 voxels; fewer than 20 voxels above 2500 HU inside T12..sacrum; lateral cut -- body outline touches a left/right face of the scan on at most 10% of lumbar slices.

| set | n | age median (range) | study types | T11 in scan | L6 mask | body cut at L/R face, median / max share of lumbar slices |
|---|---:|---|---|---:|---:|---|
| unseen (this curve) | 40 | 65.0 (0-87) | ct abdomen-pelvis 10, ct neck-chest-abdomen-pelvis 8, ? 5, ct chest-abdomen-pelvis 4 | 40 | 1 | 0.0 / 0.0684 |
| leaked 17 (void curve) | 17 | 55.0 (0-95) | ct polytrauma 10, ? 3, ct aortic valve 1, ct angiography neck-thx-abd-pelvis-leg 1 | 17 | 0 | 0.0 / 0.0 |

### Body recall, tilt 0°, conf 0.25: new (unseen) vs old (void)

Each cell: recall [subject-clustered 2.5-97.5%] (boxes). Difference: new minus old, interval from independent subject-clustered bootstraps of the two sets (2,000 each); the sets are different people, so nothing is paired.

| detector | card | lat | old (void) | new (unseen) | new − old [95%] |
|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | +0° | 0.89 [0.79, 0.97] (n 104) | 0.87 [0.79, 0.94] (n 240) | -0.02 [-0.13, +0.10] |
| Pooled (design P) | elekta_xvi | -50° | 0.68 [0.49, 0.86] (n 104) | 0.76 [0.65, 0.87] (n 241) | +0.08 [-0.12, +0.30] |
| Pooled (design P) | elekta_xvi | +50° | 0.83 [0.68, 0.95] (n 104) | 0.88 [0.80, 0.95] (n 242) | +0.05 [-0.09, +0.21] |
| Pooled (design P) | elekta_xvi | -90° | 0.39 [0.20, 0.59] (n 105) | 0.64 [0.51, 0.76] (n 243) | +0.25 [+0.02, +0.48] ** |
| Pooled (design P) | elekta_xvi | +90° | 0.35 [0.17, 0.56] (n 105) | 0.69 [0.56, 0.80] (n 243) | +0.34 [+0.09, +0.56] ** |
| Pooled (design P) | surgio_b51_dr | +0° | 0.91 [0.82, 0.97] (n 104) | 0.92 [0.87, 0.96] (n 240) | +0.01 [-0.07, +0.10] |
| Pooled (design P) | surgio_b51_dr | -50° | 0.61 [0.46, 0.75] (n 104) | 0.69 [0.57, 0.81] (n 241) | +0.08 [-0.10, +0.26] |
| Pooled (design P) | surgio_b51_dr | +50° | 0.78 [0.65, 0.89] (n 104) | 0.73 [0.61, 0.84] (n 242) | -0.05 [-0.21, +0.12] |
| Pooled (design P) | surgio_b51_dr | -90° | 0.79 [0.63, 0.93] (n 105) | 0.99 [0.98, 1.00] (n 243) | +0.20 [+0.06, +0.36] ** |
| Pooled (design P) | surgio_b51_dr | +90° | 0.85 [0.72, 0.96] (n 105) | 0.96 [0.91, 1.00] (n 243) | +0.12 [-0.01, +0.25] |
| LODO A, held Surgio | elekta_xvi | +0° | 0.78 [0.60, 0.92] (n 104) | 0.80 [0.70, 0.89] (n 240) | +0.02 [-0.16, +0.21] |
| LODO A, held Surgio | elekta_xvi | -50° | 0.41 [0.27, 0.57] (n 104) | 0.56 [0.46, 0.66] (n 241) | +0.15 [-0.03, +0.33] |
| LODO A, held Surgio | elekta_xvi | +50° | 0.40 [0.27, 0.55] (n 104) | 0.50 [0.38, 0.61] (n 242) | +0.09 [-0.09, +0.28] |
| LODO A, held Surgio | elekta_xvi | -90° | 0.19 [0.06, 0.35] (n 105) | 0.41 [0.31, 0.53] (n 243) | +0.22 [+0.03, +0.41] ** |
| LODO A, held Surgio | elekta_xvi | +90° | 0.19 [0.07, 0.33] (n 105) | 0.30 [0.20, 0.40] (n 243) | +0.11 [-0.07, +0.26] |
| LODO A, held Surgio | surgio_b51_dr | +0° | 0.26 [0.12, 0.42] (n 104) | 0.41 [0.30, 0.53] (n 240) | +0.15 [-0.04, +0.34] |
| LODO A, held Surgio | surgio_b51_dr | -50° | 0.16 [0.07, 0.28] (n 104) | 0.36 [0.26, 0.47] (n 241) | +0.20 [+0.05, +0.34] ** |
| LODO A, held Surgio | surgio_b51_dr | +50° | 0.15 [0.06, 0.26] (n 104) | 0.27 [0.18, 0.38] (n 242) | +0.12 [-0.02, +0.26] |
| LODO A, held Surgio | surgio_b51_dr | -90° | 0.21 [0.10, 0.33] (n 105) | 0.43 [0.32, 0.54] (n 243) | +0.22 [+0.06, +0.38] ** |
| LODO A, held Surgio | surgio_b51_dr | +90° | 0.18 [0.08, 0.30] (n 105) | 0.36 [0.27, 0.46] (n 243) | +0.18 [+0.03, +0.32] ** |
| LODO B, held Surgio (s1) | elekta_xvi | +0° | 0.54 [0.35, 0.72] (n 104) | 0.67 [0.54, 0.79] (n 240) | +0.13 [-0.10, +0.36] |
| LODO B, held Surgio (s1) | elekta_xvi | -50° | 0.50 [0.34, 0.67] (n 104) | 0.56 [0.45, 0.69] (n 241) | +0.06 [-0.14, +0.26] |
| LODO B, held Surgio (s1) | elekta_xvi | +50° | 0.42 [0.23, 0.63] (n 104) | 0.55 [0.42, 0.66] (n 242) | +0.12 [-0.11, +0.35] |
| LODO B, held Surgio (s1) | elekta_xvi | -90° | 0.19 [0.06, 0.36] (n 105) | 0.33 [0.22, 0.45] (n 243) | +0.14 [-0.07, +0.34] |
| LODO B, held Surgio (s1) | elekta_xvi | +90° | 0.21 [0.08, 0.36] (n 105) | 0.30 [0.21, 0.41] (n 243) | +0.10 [-0.09, +0.26] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +0° | 0.40 [0.24, 0.56] (n 104) | 0.38 [0.27, 0.50] (n 240) | -0.02 [-0.22, +0.18] |
| LODO B, held Surgio (s1) | surgio_b51_dr | -50° | 0.14 [0.05, 0.28] (n 104) | 0.29 [0.20, 0.39] (n 241) | +0.15 [-0.03, +0.29] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +50° | 0.14 [0.06, 0.25] (n 104) | 0.29 [0.19, 0.40] (n 242) | +0.15 [+0.00, +0.29] ** |
| LODO B, held Surgio (s1) | surgio_b51_dr | -90° | 0.13 [0.04, 0.26] (n 105) | 0.18 [0.11, 0.26] (n 243) | +0.04 [-0.10, +0.17] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +90° | 0.16 [0.04, 0.31] (n 105) | 0.34 [0.24, 0.44] (n 243) | +0.18 [-0.01, +0.33] |
| Real-frame LODO (render-initialised) | elekta_xvi | +0° | 0.03 [0.00, 0.06] (n 104) | 0.02 [0.00, 0.03] (n 240) | -0.01 [-0.05, +0.02] |
| Real-frame LODO (render-initialised) | elekta_xvi | -50° | 0.00 [0.00, 0.00] (n 104) | 0.01 [0.00, 0.02] (n 241) | +0.01 [+0.00, +0.02] |
| Real-frame LODO (render-initialised) | elekta_xvi | +50° | 0.02 [0.00, 0.05] (n 104) | 0.07 [0.03, 0.11] (n 242) | +0.05 [+0.00, +0.10] ** |
| Real-frame LODO (render-initialised) | elekta_xvi | -90° | 0.01 [0.00, 0.03] (n 105) | 0.03 [0.00, 0.06] (n 243) | +0.02 [-0.02, +0.06] |
| Real-frame LODO (render-initialised) | elekta_xvi | +90° | 0.02 [0.00, 0.05] (n 105) | 0.06 [0.02, 0.11] (n 243) | +0.04 [-0.01, +0.09] |
| Real-frame LODO (render-initialised) | surgio_b51_dr | +0° | 0.00 [0.00, 0.00] (n 104) | 0.00 [0.00, 0.00] (n 240) | +0.00 [+0.00, +0.00] |
| Real-frame LODO (render-initialised) | surgio_b51_dr | -50° | 0.01 [0.00, 0.03] (n 104) | 0.00 [0.00, 0.00] (n 241) | -0.01 [-0.03, +0.00] |
| Real-frame LODO (render-initialised) | surgio_b51_dr | +50° | 0.00 [0.00, 0.00] (n 104) | 0.00 [0.00, 0.01] (n 242) | +0.00 [+0.00, +0.01] |
| Real-frame LODO (render-initialised) | surgio_b51_dr | -90° | 0.04 [0.01, 0.07] (n 105) | 0.02 [0.00, 0.03] (n 243) | -0.02 [-0.06, +0.01] |
| Real-frame LODO (render-initialised) | surgio_b51_dr | +90° | 0.02 [0.00, 0.05] (n 105) | 0.01 [0.00, 0.03] (n 243) | -0.01 [-0.04, +0.02] |

`**` = the difference interval excludes 0. 9 such cells: Pooled (design P) / elekta_xvi at -90°: +0.25; Pooled (design P) / elekta_xvi at +90°: +0.34; Pooled (design P) / surgio_b51_dr at -90°: +0.20; LODO A, held Surgio / elekta_xvi at -90°: +0.22; LODO A, held Surgio / surgio_b51_dr at -50°: +0.20; LODO A, held Surgio / surgio_b51_dr at -90°: +0.22; LODO A, held Surgio / surgio_b51_dr at +90°: +0.18; LODO B, held Surgio (s1) / surgio_b51_dr at +50°: +0.15; Real-frame LODO (render-initialised) / elekta_xvi at +50°: +0.05

### Falloff at conf 0.25: first lateral angle below 90% of the same curve's lat-0 recall, old → new

`noise-level` marks a curve whose lat-0 recall is below 0.5: a 90%-of-lat-0 threshold on it is not a falloff.

| detector | card | class | tilt | old: r0, −side / +side | new: r0, −side / +side | same? |
|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.87, -30° / +40° | 0.83, -30° / +40° | same |
| Pooled (design P) | elekta_xvi | body | +0° | 0.89, -30° / +30° | 0.87, -30° / +30° | same |
| Pooled (design P) | elekta_xvi | body | +15° | 0.78, -40° / +50° | 0.80, -30° / +40° | moved |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.93, -10° / +30° | 0.81, -20° / +40° | moved |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.89, -10° / +40° | 0.81, -30° / +30° | moved |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.69, -60° / +30° | 0.72, -10° / +20° | moved |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.97, -20° / +30° | 0.94, -30° / +30° | moved |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.91, -30° / +40° | 0.92, -30° / +30° | moved |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.91, -40° / +20° | 0.89, -30° / +30° | moved |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.80, -40° / +30° | 0.84, -30° / +40° | moved |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 1.00, -40° / +10° | 0.90, -30° / +30° | moved |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.81, -40° / +30° | 0.88, -30° / +20° | moved |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.79, -10° / +30° | 0.74, -30° / +40° | moved |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.78, -30° / +40° | 0.80, -30° / +30° | moved |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.72, -40° / +30° | 0.78, -20° / +20° | moved |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.60, -10° / +10° | 0.58, -20° / +30° | moved |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.44, -20° / +40° | 0.62, -30° / +30° | moved (noise-level) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.44, -10° / +50° | 0.32, -50° / +50° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.17, -10° / +50° | 0.43, -50° / +50° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.26, -10° / +50° | 0.41, -50° / +50° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.20, -60° / +40° | 0.38, -50° / +50° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.07, -40° / +50° | 0.13, -50° / +50° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.11, -10° / +20° | 0.19, -50° / +20° | moved (noise-level) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.12, -50° / +10° | 0.16, -50° / +50° | moved (noise-level) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.61, -10° / +30° | 0.49, -40° / +50° | moved (noise-level) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.54, -40° / +30° | 0.67, -10° / +10° | moved |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.50, -20° / +10° | 0.54, -20° / +20° | moved |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.07, -60° / +50° | 0.06, -40° / +70° | moved (noise-level) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.11, -70° / +10° | 0.19, -30° / +10° | moved (noise-level) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.12, -20° / +30° | 0.08, -50° / +10° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.21, -10° / +50° | 0.51, -10° / +40° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.40, -10° / +20° | 0.38, -50° / +50° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.20, -50° / +60° | 0.42, -10° / +40° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.07, -20° / +40° | 0.06, -20° / +50° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.00, never / never | 0.05, -60° / +50° | moved (noise-level) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.00, never / never | 0.08, -10° / +10° | moved (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | -15° | 0.00, never / never | 0.01, -10° / +10° | moved (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +0° | 0.03, -20° / +50° | 0.02, -10° / +10° | moved (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +15° | 0.01, -20° / +10° | 0.01, -30° / +10° | moved (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | -15° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +0° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +15° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | -15° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +0° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +15° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | -15° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +0° | 0.00, never / never | 0.00, never / never | same (noise-level) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +15° | 0.00, never / never | 0.00, never / never | same (noise-level) |

Body curves with lat-0 recall >= 0.5 in both runs: falloff angles identical on 2 of 11, and within one 10° grid step on both sides on 8 of 11. The rule takes the FIRST grid angle below the threshold, so a curve that grazes 90% of its lat-0 value moves by a whole step on a small change.

### Exposure at the laterals, old vs new (the card, not the detector)

| card | lat | old: thickness cm, truncated-ray share | new: thickness cm, truncated-ray share |
|---|---|---|---|
| elekta_xvi | -90° | 31.6, 0.030 | 30.4, 0.009 |
| elekta_xvi | -50° | 25.1, 0.002 | 26.6, 0.001 |
| elekta_xvi | +0° | 19.0, 0.017 | 21.9, 0.015 |
| elekta_xvi | +50° | 25.5, 0.014 | 26.6, 0.005 |
| elekta_xvi | +90° | 31.9, 0.028 | 30.6, 0.012 |
| surgio_b51_dr | -90° | 31.6, 0.030 | 30.4, 0.009 |
| surgio_b51_dr | -50° | 25.1, 0.002 | 26.6, 0.001 |
| surgio_b51_dr | +0° | 19.0, 0.017 | 21.9, 0.015 |
| surgio_b51_dr | +50° | 25.5, 0.014 | 26.6, 0.005 |
| surgio_b51_dr | +90° | 31.9, 0.028 | 30.6, 0.012 |

### Reading the frame, or placing boxes where they usually are (`tools/arc_prior_check.py`)

The arc set puts every subject's L3 on one anchor, so at a given angle every subject's boxes land in nearly the same place. Body recall at tilt 0, conf 0.25, on four inputs scored against subject i's truth: **own** = subject i's frame (reproduces the curve); **swap** = another subject's frame at the same angle (fixed derangement, shift by n/2); **blank** = a uniform frame at the frame's mean grey; **layout** = no detector, the other subject's TRUTH boxes as predictions -- what a detector that read the other subject perfectly would score here, i.e. what the anchor alone gives away. own − swap: paired subject-clustered bootstrap (2,000; one resample of subjects drives both terms).

| detector | card | lat | own | swap | blank | layout (anchor) | own − swap [95%] |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | -90° | 0.64 [0.51, 0.76] | 0.48 [0.36, 0.60] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.16 [-0.01, +0.33] |
| Pooled (design P) | elekta_xvi | -70° | 0.64 [0.53, 0.76] | 0.50 [0.38, 0.62] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | +0.14 [-0.03, +0.31] |
| Pooled (design P) | elekta_xvi | -50° | 0.76 [0.65, 0.87] | 0.55 [0.43, 0.67] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.21 [+0.06, +0.37] ** |
| Pooled (design P) | elekta_xvi | -30° | 0.70 [0.58, 0.81] | 0.52 [0.40, 0.63] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.18 [+0.06, +0.32] ** |
| Pooled (design P) | elekta_xvi | +0° | 0.87 [0.79, 0.94] | 0.68 [0.55, 0.81] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.19 [+0.06, +0.32] ** |
| Pooled (design P) | elekta_xvi | +30° | 0.75 [0.65, 0.85] | 0.57 [0.45, 0.70] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.18 [+0.03, +0.33] ** |
| Pooled (design P) | elekta_xvi | +50° | 0.88 [0.80, 0.95] | 0.64 [0.51, 0.78] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.23 [+0.09, +0.37] ** |
| Pooled (design P) | elekta_xvi | +70° | 0.59 [0.45, 0.72] | 0.49 [0.36, 0.63] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.10 [-0.06, +0.25] |
| Pooled (design P) | elekta_xvi | +90° | 0.69 [0.56, 0.80] | 0.48 [0.34, 0.61] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.21 [+0.00, +0.43] ** |
| Pooled (design P) | surgio_b51_dr | -90° | 0.99 [0.98, 1.00] | 0.71 [0.58, 0.84] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.28 [+0.16, +0.41] ** |
| Pooled (design P) | surgio_b51_dr | -70° | 0.92 [0.85, 0.97] | 0.65 [0.52, 0.78] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | +0.27 [+0.14, +0.40] ** |
| Pooled (design P) | surgio_b51_dr | -50° | 0.69 [0.57, 0.81] | 0.44 [0.32, 0.57] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.24 [+0.06, +0.42] ** |
| Pooled (design P) | surgio_b51_dr | -30° | 0.79 [0.69, 0.88] | 0.59 [0.47, 0.72] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.20 [+0.04, +0.35] ** |
| Pooled (design P) | surgio_b51_dr | +0° | 0.92 [0.87, 0.96] | 0.65 [0.53, 0.78] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.27 [+0.15, +0.39] ** |
| Pooled (design P) | surgio_b51_dr | +30° | 0.80 [0.71, 0.87] | 0.57 [0.46, 0.69] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.22 [+0.10, +0.35] ** |
| Pooled (design P) | surgio_b51_dr | +50° | 0.73 [0.61, 0.84] | 0.57 [0.43, 0.70] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.17 [+0.02, +0.31] ** |
| Pooled (design P) | surgio_b51_dr | +70° | 0.88 [0.79, 0.95] | 0.65 [0.52, 0.78] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.23 [+0.07, +0.38] ** |
| Pooled (design P) | surgio_b51_dr | +90° | 0.96 [0.91, 1.00] | 0.67 [0.54, 0.80] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.29 [+0.15, +0.42] ** |
| LODO A, held Surgio | elekta_xvi | -90° | 0.41 [0.31, 0.53] | 0.29 [0.20, 0.40] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.12 [-0.03, +0.27] |
| LODO A, held Surgio | elekta_xvi | -70° | 0.40 [0.31, 0.50] | 0.31 [0.22, 0.40] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | +0.10 [-0.04, +0.23] |
| LODO A, held Surgio | elekta_xvi | -50° | 0.56 [0.46, 0.66] | 0.39 [0.29, 0.49] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.18 [+0.04, +0.31] ** |
| LODO A, held Surgio | elekta_xvi | -30° | 0.61 [0.49, 0.72] | 0.46 [0.35, 0.59] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.15 [-0.01, +0.29] |
| LODO A, held Surgio | elekta_xvi | +0° | 0.80 [0.70, 0.89] | 0.62 [0.50, 0.75] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.18 [+0.04, +0.31] ** |
| LODO A, held Surgio | elekta_xvi | +30° | 0.63 [0.50, 0.76] | 0.49 [0.36, 0.63] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.14 [-0.05, +0.32] |
| LODO A, held Surgio | elekta_xvi | +50° | 0.50 [0.38, 0.61] | 0.38 [0.27, 0.50] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.12 [-0.04, +0.27] |
| LODO A, held Surgio | elekta_xvi | +70° | 0.21 [0.13, 0.31] | 0.19 [0.10, 0.27] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.03 [-0.10, +0.17] |
| LODO A, held Surgio | elekta_xvi | +90° | 0.30 [0.20, 0.40] | 0.19 [0.11, 0.27] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.11 [-0.03, +0.26] |
| LODO A, held Surgio | surgio_b51_dr | -90° | 0.43 [0.32, 0.54] | 0.36 [0.25, 0.47] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.07 [-0.07, +0.21] |
| LODO A, held Surgio | surgio_b51_dr | -70° | 0.24 [0.15, 0.34] | 0.24 [0.16, 0.34] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | -0.01 [-0.13, +0.12] |
| LODO A, held Surgio | surgio_b51_dr | -50° | 0.36 [0.26, 0.47] | 0.32 [0.22, 0.42] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.05 [-0.10, +0.19] |
| LODO A, held Surgio | surgio_b51_dr | -30° | 0.47 [0.36, 0.57] | 0.40 [0.29, 0.51] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.07 [-0.03, +0.17] |
| LODO A, held Surgio | surgio_b51_dr | +0° | 0.41 [0.30, 0.53] | 0.38 [0.28, 0.49] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.03 [-0.10, +0.16] |
| LODO A, held Surgio | surgio_b51_dr | +30° | 0.47 [0.34, 0.59] | 0.33 [0.21, 0.44] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.14 [+0.00, +0.29] ** |
| LODO A, held Surgio | surgio_b51_dr | +50° | 0.27 [0.18, 0.38] | 0.21 [0.12, 0.30] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.07 [-0.07, +0.20] |
| LODO A, held Surgio | surgio_b51_dr | +70° | 0.20 [0.12, 0.29] | 0.19 [0.12, 0.27] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.01 [-0.10, +0.12] |
| LODO A, held Surgio | surgio_b51_dr | +90° | 0.36 [0.27, 0.46] | 0.26 [0.18, 0.36] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.10 [-0.04, +0.23] |
| LODO B, held Surgio (s1) | elekta_xvi | -90° | 0.33 [0.22, 0.45] | 0.26 [0.16, 0.37] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.07 [-0.10, +0.24] |
| LODO B, held Surgio (s1) | elekta_xvi | -70° | 0.35 [0.24, 0.47] | 0.25 [0.16, 0.35] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | +0.10 [-0.07, +0.27] |
| LODO B, held Surgio (s1) | elekta_xvi | -50° | 0.56 [0.45, 0.69] | 0.41 [0.29, 0.53] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.16 [+0.00, +0.31] |
| LODO B, held Surgio (s1) | elekta_xvi | -30° | 0.55 [0.42, 0.70] | 0.38 [0.26, 0.52] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.17 [-0.01, +0.34] |
| LODO B, held Surgio (s1) | elekta_xvi | +0° | 0.67 [0.54, 0.79] | 0.47 [0.34, 0.61] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.19 [+0.03, +0.36] ** |
| LODO B, held Surgio (s1) | elekta_xvi | +30° | 0.46 [0.32, 0.60] | 0.36 [0.24, 0.48] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.10 [-0.08, +0.28] |
| LODO B, held Surgio (s1) | elekta_xvi | +50° | 0.55 [0.42, 0.66] | 0.40 [0.29, 0.53] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.14 [-0.02, +0.30] |
| LODO B, held Surgio (s1) | elekta_xvi | +70° | 0.31 [0.20, 0.42] | 0.27 [0.17, 0.37] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.04 [-0.10, +0.19] |
| LODO B, held Surgio (s1) | elekta_xvi | +90° | 0.30 [0.21, 0.41] | 0.21 [0.12, 0.30] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.10 [-0.05, +0.25] |
| LODO B, held Surgio (s1) | surgio_b51_dr | -90° | 0.18 [0.11, 0.26] | 0.13 [0.07, 0.20] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.81] | +0.05 [-0.05, +0.16] |
| LODO B, held Surgio (s1) | surgio_b51_dr | -70° | 0.17 [0.10, 0.25] | 0.13 [0.07, 0.19] | 0.00 (0.0 boxes/frame) | 0.66 [0.54, 0.79] | +0.04 [-0.05, +0.14] |
| LODO B, held Surgio (s1) | surgio_b51_dr | -50° | 0.29 [0.20, 0.39] | 0.18 [0.10, 0.26] | 0.00 (0.0 boxes/frame) | 0.67 [0.55, 0.80] | +0.11 [-0.00, +0.23] |
| LODO B, held Surgio (s1) | surgio_b51_dr | -30° | 0.40 [0.30, 0.50] | 0.30 [0.20, 0.40] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.78] | +0.10 [-0.04, +0.23] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +0° | 0.38 [0.27, 0.50] | 0.33 [0.22, 0.46] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.80] | +0.05 [-0.10, +0.18] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +30° | 0.44 [0.33, 0.55] | 0.33 [0.22, 0.44] | 0.00 (0.0 boxes/frame) | 0.64 [0.52, 0.77] | +0.11 [-0.03, +0.27] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +50° | 0.29 [0.19, 0.40] | 0.22 [0.14, 0.31] | 0.00 (0.0 boxes/frame) | 0.65 [0.53, 0.79] | +0.07 [-0.05, +0.19] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +70° | 0.17 [0.10, 0.24] | 0.15 [0.08, 0.23] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.81] | +0.01 [-0.09, +0.11] |
| LODO B, held Surgio (s1) | surgio_b51_dr | +90° | 0.34 [0.24, 0.44] | 0.27 [0.18, 0.36] | 0.00 (0.0 boxes/frame) | 0.68 [0.55, 0.82] | +0.07 [-0.09, +0.23] |

`**` = own − swap interval above 0: the detector scores subject i better on subject i's frame than on another subject's frame at the same angle, so it is reading the subject in front of it. 19 of 54 cells. A perfect detector would score own 1.0 and swap about the layout value, so own − swap cannot exceed about 1 − layout.
Blank frames: recall above 0 in 0 cells, at most 0.0 body boxes per frame -- no detector places boxes without image content.
Cells whose own − swap interval includes 0 (reading the subject NOT shown; not the same as shown to be a prior): Pooled (design P) / elekta_xvi at -90°; Pooled (design P) / elekta_xvi at -70°; Pooled (design P) / elekta_xvi at +70°; LODO A, held Surgio / elekta_xvi at -90°; LODO A, held Surgio / elekta_xvi at -70°; LODO A, held Surgio / elekta_xvi at -30°; LODO A, held Surgio / elekta_xvi at +30°; LODO A, held Surgio / elekta_xvi at +50°; LODO A, held Surgio / elekta_xvi at +70°; LODO A, held Surgio / elekta_xvi at +90°; LODO A, held Surgio / surgio_b51_dr at -90°; LODO A, held Surgio / surgio_b51_dr at -70°; LODO A, held Surgio / surgio_b51_dr at -50°; LODO A, held Surgio / surgio_b51_dr at -30°; LODO A, held Surgio / surgio_b51_dr at +0°; LODO A, held Surgio / surgio_b51_dr at +50°; LODO A, held Surgio / surgio_b51_dr at +70°; LODO A, held Surgio / surgio_b51_dr at +90°; LODO B, held Surgio (s1) / elekta_xvi at -90°; LODO B, held Surgio (s1) / elekta_xvi at -70°; LODO B, held Surgio (s1) / elekta_xvi at -50°; LODO B, held Surgio (s1) / elekta_xvi at -30°; LODO B, held Surgio (s1) / elekta_xvi at +30°; LODO B, held Surgio (s1) / elekta_xvi at +50°; LODO B, held Surgio (s1) / elekta_xvi at +70°; LODO B, held Surgio (s1) / elekta_xvi at +90°; LODO B, held Surgio (s1) / surgio_b51_dr at -90°; LODO B, held Surgio (s1) / surgio_b51_dr at -70°; LODO B, held Surgio (s1) / surgio_b51_dr at -50°; LODO B, held Surgio (s1) / surgio_b51_dr at -30°; LODO B, held Surgio (s1) / surgio_b51_dr at +0°; LODO B, held Surgio (s1) / surgio_b51_dr at +30°; LODO B, held Surgio (s1) / surgio_b51_dr at +50°; LODO B, held Surgio (s1) / surgio_b51_dr at +70°; LODO B, held Surgio (s1) / surgio_b51_dr at +90°.

Figure: `fig_old_vs_new.png` (old and new body recall at tilt 0, with the anchor-layout floor).

<!-- END:COMPARE -->

Set: `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep_unseen` — 40 TotalSegmentator subjects (held out under tools/eval_gate.py) (s0086, s0139, s0178, s0236, s0243, s0244, s0355, s0370, s0550, s0586, s0657, s0667, s0669, s0733, s0830, s0859, s0869, s0913, s0979, s0983, s1111, s1230, s1294, s1347, s1364, s1395, s1404, s1487, s1540, s1547, s1574, s1741, s1807, s1815, s1868, s1935, s1949, s1973, s2021, s2106), Surgio-B51 geometry (anchor `case29/AP`), lat -90..90° step 10°, tilt [-15, 0, 15], roll 0, styled per card. Frames per card: {'elekta_xvi': 2280, 'surgio_b51_dr': 2280}.

Denominator per cell: projected boxes with >= 25% of the mask inside the panel, pooled over subjects; boxes at 2-25% are ignored (predictions on them are not false positives). Matching: greedy descending-confidence, IoU >= 0.5, per class (realxray_eval conventions). Intervals: subject-clustered bootstrap, 2000 resamples, 2.5-97.5 percentile.

EXPOSURE CONFOUND (looked at, 2026-09-23): the surgio_b51_dr card renders the thick lateral view as photon-starved mottle in which the spine is NOT visible, while REAL C-ArmLSpine laterals show readable bodies -- this is a property of the card's exposure conditioning that the styled TRAINING corpus carries too, so recall at large |lat| conflates geometry with synthetic underexposure. The elekta_xvi card additionally draws the XVI half-fan blades, so part of the panel is black at every angle and boxes under the blades count as misses. The table below quantifies both: mean exposed panel share (pixels above the collimated black level) and mean water-equivalent thickness, per lateral angle.

| card | lat | frames | exposed share | thickness (cm) |
|---|---|---|---|---|
| elekta_xvi | -90° | 120 | 0.68 | 30.4 |
| elekta_xvi | -80° | 120 | 0.69 | 30.1 |
| elekta_xvi | -70° | 120 | 0.69 | 29.4 |
| elekta_xvi | -60° | 120 | 0.70 | 28.1 |
| elekta_xvi | -50° | 120 | 0.71 | 26.6 |
| elekta_xvi | -40° | 120 | 0.68 | 25.3 |
| elekta_xvi | -30° | 120 | 0.69 | 24.0 |
| elekta_xvi | -20° | 120 | 0.71 | 23.0 |
| elekta_xvi | -10° | 120 | 0.69 | 22.2 |
| elekta_xvi | +0° | 120 | 0.68 | 21.9 |
| elekta_xvi | +10° | 120 | 0.68 | 22.3 |
| elekta_xvi | +20° | 120 | 0.68 | 23.0 |
| elekta_xvi | +30° | 120 | 0.67 | 23.9 |
| elekta_xvi | +40° | 120 | 0.70 | 25.2 |
| elekta_xvi | +50° | 120 | 0.69 | 26.6 |
| elekta_xvi | +60° | 120 | 0.69 | 28.1 |
| elekta_xvi | +70° | 120 | 0.68 | 29.4 |
| elekta_xvi | +80° | 120 | 0.69 | 30.4 |
| elekta_xvi | +90° | 120 | 0.70 | 30.6 |
| surgio_b51_dr | -90° | 120 | 1.00 | 30.4 |
| surgio_b51_dr | -80° | 120 | 1.00 | 30.1 |
| surgio_b51_dr | -70° | 120 | 1.00 | 29.4 |
| surgio_b51_dr | -60° | 120 | 1.00 | 28.1 |
| surgio_b51_dr | -50° | 120 | 1.00 | 26.6 |
| surgio_b51_dr | -40° | 120 | 1.00 | 25.3 |
| surgio_b51_dr | -30° | 120 | 1.00 | 24.0 |
| surgio_b51_dr | -20° | 120 | 1.00 | 23.0 |
| surgio_b51_dr | -10° | 120 | 1.00 | 22.2 |
| surgio_b51_dr | +0° | 120 | 1.00 | 21.9 |
| surgio_b51_dr | +10° | 120 | 1.00 | 22.3 |
| surgio_b51_dr | +20° | 120 | 1.00 | 23.0 |
| surgio_b51_dr | +30° | 120 | 1.00 | 23.9 |
| surgio_b51_dr | +40° | 120 | 1.00 | 25.2 |
| surgio_b51_dr | +50° | 120 | 1.00 | 26.6 |
| surgio_b51_dr | +60° | 120 | 1.00 | 28.1 |
| surgio_b51_dr | +70° | 120 | 1.00 | 29.4 |
| surgio_b51_dr | +80° | 120 | 1.00 | 30.4 |
| surgio_b51_dr | +90° | 120 | 1.00 | 30.6 |

## Falloff at conf 0.25 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.834 | -30° | +40° | 0.416 (+90°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.871 | -30° | +30° | 0.562 (+80°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.803 | -30° | +40° | 0.204 (+70°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.806 | -20° | +40° | 0.176 (-40°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.809 | -30° | +30° | 0.217 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.720 | -10° | +20° | 0.125 (+70°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.943 | -30° | +30° | 0.567 (-40°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.921 | -30° | +30° | 0.689 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.885 | -30° | +30° | 0.421 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.839 | -30° | +40° | 0.059 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 0.905 | -30° | +30° | 0.318 (-60°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.880 | -30° | +20° | 0.217 (-60°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.737 | -30° | +40° | 0.169 (+80°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.800 | -30° | +30° | 0.215 (+70°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.779 | -20° | +20° | 0.079 (+90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.581 | -20° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.619 | -30° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.320 | -50° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.425 | -50° | +50° | 0.115 (+60°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.412 | -50° | +50° | 0.128 (+60°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.377 | -50° | +50° | 0.124 (+70°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.129 | -50° | +50° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.191 | -50° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.160 | -50° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.494 | -40° | +50° | 0.165 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.667 | -10° | +10° | 0.269 (+80°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.537 | -20° | +20° | 0.080 (+70°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.065 | -40° | +70° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.191 | -30° | +10° | 0.000 (+60°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.080 | -50° | +10° | 0.000 (-80°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.506 | -10° | +40° | 0.090 (-70°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.379 | -50° | +50° | 0.145 (+60°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.418 | -10° | +40° | 0.056 (+60°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.065 | -20° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.048 | -60° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.080 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | -15° | 0.012 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +0° | 0.017 | -10° | +10° | 0.004 (-70°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +15° | 0.008 | -30° | +10° | 0.000 (-80°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-80°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-30°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Falloff at conf 0.74 (recall < 90% of the same curve's lat-0 value)

| detector | card | class | tilt | recall@0° | first below -side | first below +side | min (at) |
|---|---|---|---|---|---|---|---|
| Pooled (design P) | elekta_xvi | body | -15° | 0.462 | -30° | +40° | 0.148 (+80°) |
| Pooled (design P) | elekta_xvi | body | +0° | 0.629 | -10° | +10° | 0.376 (+70°) |
| Pooled (design P) | elekta_xvi | body | +15° | 0.443 | -10° | +20° | 0.076 (+70°) |
| Pooled (design P) | elekta_xvi | sacrum | -15° | 0.484 | -10° | +10° | 0.000 (+60°) |
| Pooled (design P) | elekta_xvi | sacrum | +0° | 0.476 | -20° | +10° | 0.087 (-70°) |
| Pooled (design P) | elekta_xvi | sacrum | +15° | 0.320 | -10° | +20° | 0.083 (+70°) |
| Pooled (design P) | surgio_b51_dr | body | -15° | 0.680 | -20° | +10° | 0.269 (-40°) |
| Pooled (design P) | surgio_b51_dr | body | +0° | 0.679 | -20° | +20° | 0.398 (-50°) |
| Pooled (design P) | surgio_b51_dr | body | +15° | 0.566 | -20° | +20° | 0.154 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | -15° | 0.613 | -30° | +20° | 0.000 (-50°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +0° | 0.619 | -30° | +20° | 0.091 (+70°) |
| Pooled (design P) | surgio_b51_dr | sacrum | +15° | 0.600 | -10° | +20° | 0.000 (+60°) |
| LODO A, held Surgio | elekta_xvi | body | -15° | 0.206 | -30° | +30° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | body | +0° | 0.429 | -10° | +10° | 0.025 (+90°) |
| LODO A, held Surgio | elekta_xvi | body | +15° | 0.275 | -10° | +10° | 0.000 (-70°) |
| LODO A, held Surgio | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +0° | 0.143 | -10° | +10° | 0.000 (-90°) |
| LODO A, held Surgio | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | -15° | 0.012 | -50° | +60° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | body | +0° | 0.054 | -20° | +30° | 0.000 (+50°) |
| LODO A, held Surgio | surgio_b51_dr | body | +15° | 0.025 | -10° | +10° | 0.000 (-80°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +0° | 0.048 | -30° | +20° | 0.000 (-90°) |
| LODO A, held Surgio | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | -15° | 0.121 | -30° | +10° | 0.004 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +0° | 0.271 | -10° | +10° | 0.070 (-70°) |
| LODO B, held Surgio (s1) | elekta_xvi | body | +15° | 0.139 | -10° | +10° | 0.004 (+70°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +0° | 0.048 | -10° | +20° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | -15° | 0.004 | -60° | +50° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +0° | 0.013 | -50° | +60° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | body | +15° | 0.016 | -10° | +10° | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| LODO B, held Surgio (s1) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +0° | 0.004 | -10° | +10° | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | elekta_xvi | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | body | +15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | -15° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +0° | 0.000 | never | never | 0.000 (-90°) |
| Real-frame LODO (render-initialised) | surgio_b51_dr | sacrum | +15° | 0.000 | never | never | 0.000 (-90°) |

## Per-angle body recall, tilt 0°, conf 0.25 (denominators in brackets)

### Pooled (design P) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.638 | [0.510, 0.762] |
| -80° | 243 | 0.741 | [0.632, 0.840] |
| -70° | 241 | 0.643 | [0.528, 0.760] |
| -60° | 241 | 0.585 | [0.446, 0.720] |
| -50° | 241 | 0.763 | [0.654, 0.866] |
| -40° | 241 | 0.759 | [0.643, 0.863] |
| -30° | 240 | 0.700 | [0.585, 0.812] |
| -20° | 240 | 0.842 | [0.743, 0.928] |
| -10° | 240 | 0.842 | [0.760, 0.909] |
| +0° | 240 | 0.871 | [0.788, 0.937] |
| +10° | 240 | 0.842 | [0.744, 0.923] |
| +20° | 240 | 0.858 | [0.774, 0.929] |
| +30° | 240 | 0.750 | [0.646, 0.848] |
| +40° | 241 | 0.743 | [0.622, 0.850] |
| +50° | 242 | 0.876 | [0.800, 0.947] |
| +60° | 242 | 0.661 | [0.534, 0.785] |
| +70° | 242 | 0.587 | [0.451, 0.718] |
| +80° | 242 | 0.562 | [0.430, 0.692] |
| +90° | 243 | 0.691 | [0.561, 0.803] |

### Pooled (design P) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.992 | [0.979, 1.000] |
| -80° | 243 | 0.967 | [0.908, 1.000] |
| -70° | 241 | 0.917 | [0.850, 0.968] |
| -60° | 241 | 0.751 | [0.628, 0.860] |
| -50° | 241 | 0.689 | [0.566, 0.810] |
| -40° | 241 | 0.730 | [0.606, 0.843] |
| -30° | 240 | 0.792 | [0.691, 0.883] |
| -20° | 240 | 0.883 | [0.798, 0.952] |
| -10° | 240 | 0.904 | [0.840, 0.958] |
| +0° | 240 | 0.921 | [0.870, 0.963] |
| +10° | 240 | 0.925 | [0.879, 0.966] |
| +20° | 240 | 0.883 | [0.818, 0.945] |
| +30° | 240 | 0.796 | [0.711, 0.869] |
| +40° | 241 | 0.722 | [0.621, 0.816] |
| +50° | 242 | 0.731 | [0.614, 0.841] |
| +60° | 242 | 0.785 | [0.687, 0.870] |
| +70° | 242 | 0.876 | [0.789, 0.946] |
| +80° | 242 | 0.955 | [0.913, 0.988] |
| +90° | 243 | 0.963 | [0.911, 0.996] |

### LODO A, held Surgio — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.412 | [0.307, 0.527] |
| -80° | 243 | 0.395 | [0.297, 0.498] |
| -70° | 241 | 0.402 | [0.310, 0.500] |
| -60° | 241 | 0.394 | [0.293, 0.500] |
| -50° | 241 | 0.564 | [0.465, 0.660] |
| -40° | 241 | 0.627 | [0.520, 0.737] |
| -30° | 240 | 0.608 | [0.494, 0.723] |
| -20° | 240 | 0.792 | [0.702, 0.873] |
| -10° | 240 | 0.767 | [0.661, 0.865] |
| +0° | 240 | 0.800 | [0.703, 0.891] |
| +10° | 240 | 0.796 | [0.690, 0.894] |
| +20° | 240 | 0.767 | [0.654, 0.870] |
| +30° | 240 | 0.629 | [0.496, 0.762] |
| +40° | 241 | 0.544 | [0.411, 0.682] |
| +50° | 242 | 0.496 | [0.380, 0.614] |
| +60° | 242 | 0.260 | [0.165, 0.368] |
| +70° | 242 | 0.215 | [0.130, 0.307] |
| +80° | 242 | 0.293 | [0.192, 0.404] |
| +90° | 243 | 0.296 | [0.203, 0.398] |

### LODO A, held Surgio — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.432 | [0.324, 0.544] |
| -80° | 243 | 0.461 | [0.354, 0.574] |
| -70° | 241 | 0.237 | [0.150, 0.336] |
| -60° | 241 | 0.274 | [0.180, 0.375] |
| -50° | 241 | 0.361 | [0.264, 0.466] |
| -40° | 241 | 0.502 | [0.393, 0.619] |
| -30° | 240 | 0.467 | [0.363, 0.573] |
| -20° | 240 | 0.446 | [0.340, 0.563] |
| -10° | 240 | 0.458 | [0.344, 0.571] |
| +0° | 240 | 0.412 | [0.301, 0.530] |
| +10° | 240 | 0.458 | [0.340, 0.581] |
| +20° | 240 | 0.421 | [0.306, 0.548] |
| +30° | 240 | 0.467 | [0.341, 0.590] |
| +40° | 241 | 0.373 | [0.276, 0.482] |
| +50° | 242 | 0.273 | [0.181, 0.377] |
| +60° | 242 | 0.128 | [0.068, 0.196] |
| +70° | 242 | 0.202 | [0.120, 0.293] |
| +80° | 242 | 0.273 | [0.191, 0.361] |
| +90° | 243 | 0.362 | [0.270, 0.456] |

### LODO B, held Surgio (s1) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.329 | [0.219, 0.448] |
| -80° | 243 | 0.403 | [0.290, 0.518] |
| -70° | 241 | 0.353 | [0.241, 0.473] |
| -60° | 241 | 0.432 | [0.309, 0.556] |
| -50° | 241 | 0.564 | [0.448, 0.689] |
| -40° | 241 | 0.598 | [0.466, 0.724] |
| -30° | 240 | 0.554 | [0.417, 0.698] |
| -20° | 240 | 0.662 | [0.540, 0.780] |
| -10° | 240 | 0.558 | [0.438, 0.671] |
| +0° | 240 | 0.667 | [0.545, 0.785] |
| +10° | 240 | 0.562 | [0.423, 0.697] |
| +20° | 240 | 0.658 | [0.532, 0.773] |
| +30° | 240 | 0.458 | [0.325, 0.600] |
| +40° | 241 | 0.527 | [0.396, 0.663] |
| +50° | 242 | 0.545 | [0.422, 0.660] |
| +60° | 242 | 0.335 | [0.228, 0.451] |
| +70° | 242 | 0.310 | [0.202, 0.425] |
| +80° | 242 | 0.269 | [0.160, 0.393] |
| +90° | 243 | 0.305 | [0.205, 0.412] |

### LODO B, held Surgio (s1) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.177 | [0.106, 0.261] |
| -80° | 243 | 0.198 | [0.122, 0.282] |
| -70° | 241 | 0.170 | [0.101, 0.246] |
| -60° | 241 | 0.203 | [0.123, 0.293] |
| -50° | 241 | 0.290 | [0.196, 0.394] |
| -40° | 241 | 0.394 | [0.292, 0.508] |
| -30° | 240 | 0.400 | [0.301, 0.498] |
| -20° | 240 | 0.483 | [0.381, 0.588] |
| -10° | 240 | 0.467 | [0.360, 0.571] |
| +0° | 240 | 0.379 | [0.270, 0.498] |
| +10° | 240 | 0.508 | [0.389, 0.633] |
| +20° | 240 | 0.475 | [0.365, 0.591] |
| +30° | 240 | 0.442 | [0.329, 0.551] |
| +40° | 241 | 0.456 | [0.348, 0.570] |
| +50° | 242 | 0.289 | [0.193, 0.398] |
| +60° | 242 | 0.145 | [0.081, 0.222] |
| +70° | 242 | 0.165 | [0.097, 0.243] |
| +80° | 242 | 0.207 | [0.125, 0.300] |
| +90° | 243 | 0.337 | [0.244, 0.435] |

### Real-frame LODO (render-initialised) — elekta_xvi

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.029 | [0.000, 0.065] |
| -80° | 243 | 0.021 | [0.004, 0.044] |
| -70° | 241 | 0.004 | [0.000, 0.013] |
| -60° | 241 | 0.017 | [0.000, 0.046] |
| -50° | 241 | 0.008 | [0.000, 0.025] |
| -40° | 241 | 0.041 | [0.012, 0.079] |
| -30° | 240 | 0.021 | [0.000, 0.047] |
| -20° | 240 | 0.017 | [0.004, 0.034] |
| -10° | 240 | 0.004 | [0.000, 0.013] |
| +0° | 240 | 0.017 | [0.004, 0.033] |
| +10° | 240 | 0.013 | [0.000, 0.029] |
| +20° | 240 | 0.042 | [0.016, 0.075] |
| +30° | 240 | 0.029 | [0.004, 0.064] |
| +40° | 241 | 0.021 | [0.000, 0.050] |
| +50° | 242 | 0.066 | [0.029, 0.112] |
| +60° | 242 | 0.012 | [0.000, 0.029] |
| +70° | 242 | 0.021 | [0.000, 0.059] |
| +80° | 242 | 0.050 | [0.008, 0.103] |
| +90° | 243 | 0.058 | [0.020, 0.106] |

### Real-frame LODO (render-initialised) — surgio_b51_dr

| lat | n | recall | 95% band |
|---|---|---|---|
| -90° | 243 | 0.016 | [0.004, 0.033] |
| -80° | 243 | 0.000 | [0.000, 0.000] |
| -70° | 241 | 0.004 | [0.000, 0.013] |
| -60° | 241 | 0.000 | [0.000, 0.000] |
| -50° | 241 | 0.000 | [0.000, 0.000] |
| -40° | 241 | 0.004 | [0.000, 0.013] |
| -30° | 240 | 0.000 | [0.000, 0.000] |
| -20° | 240 | 0.004 | [0.000, 0.013] |
| -10° | 240 | 0.000 | [0.000, 0.000] |
| +0° | 240 | 0.000 | [0.000, 0.000] |
| +10° | 240 | 0.000 | [0.000, 0.000] |
| +20° | 240 | 0.004 | [0.000, 0.013] |
| +30° | 240 | 0.000 | [0.000, 0.000] |
| +40° | 241 | 0.000 | [0.000, 0.000] |
| +50° | 242 | 0.004 | [0.000, 0.013] |
| +60° | 242 | 0.008 | [0.000, 0.021] |
| +70° | 242 | 0.004 | [0.000, 0.013] |
| +80° | 242 | 0.012 | [0.000, 0.029] |
| +90° | 243 | 0.012 | [0.000, 0.028] |

