# Adversarial check of the counting evaluation

Checked 2026-09-23 against `SchwingNet/results/counting.json`, `SchwingNet/results/COUNTING.md`, the 21 cell files under `SchwingNet/results/counting/`, `tools/count_from_sacrum_eval.py`, and the raw dump `/rs/rs_grp_oschome/go2432/data/or_ready/lodo/sweeps/lodo_carm__carm_test.json` with the C-ArmLSpine test labels and metas pulled from the grid. Verdict per check, then the headline numbers as re-read from the JSON, then caveats the builder's report did not state.

Summary: checks 1-4 PASS. Check 5 PASSES for every scored number and FAILS on one sentence: the closing paragraph of COUNTING.md quotes two figures from `docs/SWEEP_PROTOCOL.md` that come from the morphology reading of the sweep (the 27-level model), and misquotes one of them.

## Check 1: self-test, then frames the builder did not build. PASS

`python tools/count_from_sacrum_eval.py --self-test` on Windows Python 3.12 / numpy 2.5.3 / scipy 1.18.1: `SELF_TEST_OK`, exit 0.

New frames, in `SchwingNet/tools/counting_check_synthetic.py` (imports `score_frame` and `pooled` unchanged; output `SYNTHETIC_CHECK_OK`, exit 0):

| frame | expectation | result |
|---|---|---|
| A. L6 spine: six truth bodies named L6, L5 ... L1 (the six-lumbar convention), all six detected | ordinals 1..6 on both sides, 6/6 correct, exact; the name check must disagree (L5 sits at ordinal 2) and must not touch the score | truth [1..6], det [1..6], 6/6 correct, exact True; `name_check {named: 5, agree: 0}`, score unaffected |
| B. the same L6 spine stored upside down | identical | truth [1..6], det [1..6], 6/6 |
| C. sacrum missed, all six bodies detected | `defined False`, `why 'sacrum not detected'`, no score keys | as expected; `n_correct`, `per_truth`, `n_matched` absent |
| C2. `pooled([C, clean])` | the undefined frame enters only `defined_share` (1/2) and the all-sacrum-frames denominator (6/12); `matched_correct` 6/6, `truth_correct_defined` den 6 | as expected |
| D. sacrum box at confidence 0.20 under a 0.25 threshold | undefined | `defined False`, `n_det_sacrum 0` |
| E. L6 spine plus a spurious S1 box between sacrum centre and first body | six one-offs, one unmatched detection | as expected |
| F. sacrum at the top of the image, a spurious box above it, six bodies below | the box above the sacrum is caudal and ignored; bodies read 1..6 | det [1,2,3,4,5,6,None], caudal ignored 1, 6/6 |
| G. sacrum mid-frame, three bodies above, two spurious boxes below | both spurious boxes ignored | det [1,2,3,None,None], caudal ignored 2 |
| H. one real body cranial, two spurious boxes caudal | the majority rule flips the axis; the real body must not be scored correct | real body scored `unranked`, det [None,1,2] |

H is the tool's known weak spot (the cranial side is the side with more boxes). It is recorded by the cells as `n_unranked`; that count is 0 in all 21 cells, so the rule never fired on real data.

## Check 2: hand recomputation on real frames from the raw dump. PASS

`SchwingNet/tools/counting_check_hand.py` imports nothing from the counting tool. It denormalises the YOLO label file by the meta's `size`, swaps each body box for the meta's `outline_box` at IoU >= 0.9, ranks bodies by plain Euclidean distance from the sacrum centre (the tool ranks by projection on an SVD axis), drops detections on the caudal side of the truth-derived cranial vector, and matches greedily in descending confidence at IoU >= 0.5. Output `HAND_CHECK_OK`; per-frame record in `SchwingNet/results/counting_check_hand.json`.

| frame | conf | hand per-truth | cell per-truth | det ordinals hand = cell | anchor IoU hand / cell |
|---|---:|---|---|---|---|
| case100_AP | 0.74 | correct x5 | correct x5 | [2,5,3,4,1] = [2,5,3,4,1] | 0.853 / 0.853 |
| case139_AP | 0.74 | one_off x5 (spurious S1 box, conf 0.7457, ordinal 1, matches nothing) | one_off x5 | [3,4,2,5,6,1] = same | 0.727 / 0.727 |
| case23_LAT | 0.74 | missed, correct x4 (ordinal 5 is a 62 px sliver, level None) | same | [1,2,3,4] = same | 0.747 / 0.747 |
| case11_LAT | 0.25 | one_off, one_off, correct x3 (a conf 0.38 box spanning two bodies takes ordinal 4) | same | [1,2,3,5,6,4] = same | 0.627 / 0.627 |
| case10_LAT | 0.25 | missed, correct x5 (six truth bodies; the top one, level None, 58 px, missed) | same | [2,3,4,1,5] = same | 0.552 / 0.552 |

Also over all 56 frames: the outline boxes the 0.74 cell used as truth equal the meta's kept cls-0 `outline_box` set one-to-one in 56/56 frames, so the duplicated SPINEPS body boxes (COUNTING.md truth note 1) did not collapse onto one outline.

On the builder's sentence "ordinal 5: 18/41 missed at the field edge": of the 15 top-ordinal misses at ordinal 5 in defined frames at 0.74, 13 are within 5 px of the image edge or under 100 px tall (fragments at the CT's superior boundary; the meta's `visible_frac` is 0.62-1.0), and 2 are whole bodies missed away from the edge: case135_LAT (92 px tall, 20 px from the edge, visible_frac 1.0) and case37_LAT (139 px, 17 px). "Mostly at the field edge" is accurate; "at the field edge" for all 18 is not quite.

## Check 3: the ordering axis. PASS, with one wording finding

Code: `order_from_anchor` projects box centres on the first singular vector of the centres (sacrum included), or on the sacrum-to-body vector when there are fewer than three points; the sign is chosen so the side with more boxes is cranial, a tie going to the side whose nearest box is nearer the sacrum; boxes on the other side get ordinal None. Image y never enters. Synthetic frames B, F and G above are the discriminating cases: a top-down or bottom-up image-y count would give the wrong ordinals on F and G and the tool does not.

Real data: in every defined frame with two or more bodies, the tool's truth ordinal equals the rank of |projection| from the sacrum (checked over the C-ArmLSpine 0.74 cell, 46 frames; the DeepFluoro all-six dc_B cell, 128 frames; the COBRA lodo cell, 36 frames). In all of them the sacrum lies below the bodies; none is stored upside down. The reason: the realxray DeepFluoro metas carry `rot_180_for_up: 1 ... applied to image and boxes`, so the copy that was scored is already upright. COUNTING.md's sentence "the DeepFluoro frames stored upside down are handled alike" therefore describes an invariance no scored frame exercised; it is true of the tool (frame B) but should not be read as a real-data result.

## Check 4: clustering and denominators. PASS

- `pooled()` groups by the frame's `case` field. Distinct values per cell: C-ArmLSpine `case100` ... 28 (both views of a case in one cluster); DeepFluoro `18-1109` 1 for the test split, 6 for all six specimens; COBRA `A053` ... 27. `n_clusters` in every interval equals that count.
- The pooled-across-devices families prefix the set name to the case (`counting_report.py` line 49), so the 56 clusters are 28 + 1 + 27 with no collision.
- Every ratio in the JSON carries `num`, `den`, `n_clusters`, the percentile interval, the BCa interval or the reason it is undefined, and the resample count. The table states each denominator (46/56, 197 matched, 232 bodies in defined frames, 287 in all sacrum frames, 41/46 frames). One-cluster cells print "(1 cluster)" and no interval. The two design-B families with a member missing are declared incomplete rather than pooled.
- `bca_ratio` resamples clusters with replacement and takes the ratio of sums; the jackknife for the acceleration is over clusters. Correct for a ratio estimator.

## Check 5: no number from the 27-level classifier or a leaked bank. PASS for every scored number; FAIL for one quoted sentence

Scored numbers:
- Every cell's source is a `realxray_eval.py --dump-raw` file of a YOLO detector (headline weights `spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`). The raw rows hold only classes 0 (vertebra) and 1 (sacrum): 470 + 87 boxes across the 56 frames, minimum confidence 0.0103. No embedding, no bank, no level head anywhere in the tool.
- The dump's own `naming` block is `realxray_eval.naming_at`, a sacrum-anchored gap rule, not the classifier; COUNTING.md does not quote it.
- `lodo:carmlspine` in `tools/realxray_train.py` trains on every ready dataset except the held one and drops `carmlspine_multi` (the crop set) from the ready list, so the held device's crops cannot enter. The C-ArmLSpine split is case-grouped (`splits.json`: 105 train / 15 val / 28 test cases, AP and LAT of a case together) and the 28 test cases appear in neither train nor val.
- Design A/B corpora (`tools/devcorpus_build.py`) render TotalSegmentator subjects; for a held device the lists take styled corpora of the other two geometries and real frames of the other two devices only. C-ArmLSpine contributes camera poses (K, ext) to the surgio pose pool, not pixels or anatomy.
- The 0.74 operating point was chosen on the LODO arm's other-device sweeps (`a1.json`, `cross_device_0.74`, `how_chosen`); 0.25 is the YOLO default.
- The `lstv_*` pointers (story_rows_f3/f6) are count-based: `fig_story_rows.row_confirm` records `correct = (located == names[ti])` where `located` is the chain node reached by counting `ordv` bodies from the anchor; the truth names only label the node.

The failing sentence, COUNTING.md's last line: "the field-size / overlap numbers in `docs/SWEEP_PROTOCOL.md` (93-95 % naming at two vertebrae of overlap; chains complete on 92 / 96 / 99 % of spines for a collimated / 9-inch / 12-inch field)".
- The naming-on-the-sweep numbers that page reports are the morphology reading: `tools/sweep_map.py` names each chain "by counting from the anchor and by the morphology model" and its summary row prints `single_frame / sweep_morph / sweep_hybrid` (line 2216); `tools/sweep_spacing_curve.py` reads `K{K}_sweep_morph` (line 48). `sweep_morph` and `sweep_hybrid` both run `namer.run` (the level model); `sweep_count` is computed but is not the reported figure. So "93-95 % naming" is a classifier-derived number imported into the counting report.
- It is also misquoted: the page says 93-95 % for a two-vertebra spot image at ONE body of overlap, not "two vertebrae of overlap".
- The chain-completion figures (92 / 96 / 99 %) are linking only and may stay.
- Fix: delete the naming parenthetical, or replace it with the `sweep_count` reading re-derived from the same runs.

## Headline numbers re-read from counting.json (lodo_carm on C-ArmLSpine test, outline truth, 28 case clusters, 2,000 resamples, seed 0)

conf 0.74: defined 46/56 = 82.1 % [69.6, 92.9]; anchor correct 43/46 = 93.5 %; matched 197; ordinal correct 188/197 = 95.4 % [89.4, 99.5] BCa [85.2, 98.9]; within one 197/197 = 100 %; frames all matched correct 41/46 = 89.1 % [77.6, 98.0]; frames exact 20/46 = 43.5 %; per truth body (232) correct 81.0 % [73.8, 87.6] / one-off 9 = 3.9 % / off by more 0 / missed 35 = 15.1 %; all sacrum frames 188/287 = 65.5 % [53.7, 77.0]. By ordinal: 1: 44/46 = 95.7 %, 2: 44/46 = 95.7, 3: 41/46 = 89.1, 4: 38/46 = 82.6, 5: 21/41 = 51.2 (18 missed), 6: 0/7 (7 missed). AP 96/103 = 93.2 % of matched, LAT 92/94 = 97.9 %.

conf 0.25: defined 51/56 = 91.1 % [83.9, 96.4]; matched 235; ordinal correct 199/235 = 84.7 % [77.4, 90.7] BCa [76.5, 90.4]; within one 225/235 = 95.7 %; frames all matched correct 36/50 = 72.0 %; per truth body (259) 76.8 / 10.0 / 3.9 / 9.3 %; all sacrum frames 199/287 = 69.3 % [57.6, 79.8].

Other cells, ordinal correct % of matched at 0.25, as re-read: DeepFluoro test (1 cluster) lodo_df 53/67 = 79.1; dc_A 63/64 = 98.4, s1 37/66 = 56.1; dc_B 59/67 = 88.1, s1 34/66 = 51.5. All six specimens: dc_A 264/292 = 90.4 [71.0, 98.8], s1 256/321 = 79.8, dc_B 291/327 = 89.0 [80.5, 95.4], s1 234/311 = 75.2. COBRA (27 clusters): lodo_cobra 54/76 = 71.1 [56.6, 80.3], defined 111/609; dc_A 159/240 = 66.2, s1 172/232 = 74.1, dc_B 157/242 = 64.9. C-ArmLSpine styled arms: dc_A 162/206 = 78.6 [67.1, 88.4], s1 129/197 = 65.5, dc_B_s1 146/225 = 64.9. Pooled families (56 clusters): real-only LODO 306/378 = 81.0 [75.7, 85.8]; design A seed 0 384/510 = 75.3 [66.7, 82.9]; seed 1 338/495 = 68.3 [63.4, 73.8]; design B seed 0 and seed 1 incomplete. Frames with no truth sacrum: 0/56, 14/104, 39/648. All agree with the builder's report.

## Caveats the builder's report did not state

1. The "in-training-device (reference)" row (pooled arm, 100 % of 117 matched) is a detector trained on C-ArmLSpine BODY boxes scored against OUTLINE truth: it matches 117 of 287 bodies (recall 40.8 %) because its boxes are body-sized. The table row does not say so; a reader could take 100 % as the in-domain counting ceiling. It is a ceiling on 41 % of the bodies.
2. `realxray_train.arm_sets` validates a LODO arm on the OTHER devices' test splits, so `rx_lodo_carmlspine_1024/best.pt` was checkpoint-selected on DeepFluoro and COBRA test frames, and the 0.74 operating point was then chosen on the same frames. Neither touches the C-ArmLSpine number. It does mean those frames were used twice for that arm.
3. The DeepFluoro metas flag `unlabelled_vertebra_in_field` (a vertebra above the CT's superior boundary with no box). Such a detection is cranial to every labelled body, so it cannot shift a labelled ordinal; it inflates `det_unmatched` only.
4. The task said "highest IoU first"; the implemented matching is descending confidence, each taking its highest-IoU unmatched truth (the `sweep_matches` convention). The hand recomputation used the same convention, so this check does not test the alternative.

## Files

- `SchwingNet/tools/counting_check_synthetic.py`: frames A-H above; run `python SchwingNet/tools/counting_check_synthetic.py`.
- `SchwingNet/tools/counting_check_hand.py`: the hand recomputation; needs the raw dump, `labels/test` and `meta` of `realxray/carmlspine`.
- `SchwingNet/results/counting_check_hand.json`: its per-frame record, the 56-frame outline check and the top-ordinal misses.
