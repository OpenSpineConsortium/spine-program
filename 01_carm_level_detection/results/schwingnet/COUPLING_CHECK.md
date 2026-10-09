# Coupling check: adversarial verification of the coupler (COUPLING.md) and the alphabet loss (ALPHABET_LOSS.md)

Verified 2026-09-23 01:30-01:55 EDT against `SchwingNet/results/coupling.json` (job 40416348, `COUPLING_EVAL_RC=0`, no MISSING
lines, rsynced at 01:26), `alphabet_loss.json`, `tools/alphabet_couple.py`, `SchwingNet/tools/coupling_report.py`,
`SchwingNet/tools/alphabet_loss_report.py` and the uncommitted diffs of `tools/head_mixed_length.py` and
`tools/level_prototype.py`. Verifier jobs: 40416441 (split read from the bank, CPU), 40416411 (v8 lambda = 0 control, GPU),
40416438 (oracle arm re-coupled with duplicate boxes dropped, CPU); 40416410 was the first split read, superseded by 40416441
after the verifier's own regex confused `CTSP_COLONOG_403` with VerSe subject 403. Every number below was re-read from a JSON or
recomputed from the per-frame `couple_all.json` files (`tmp/coupling_check/proto_post/`), not copied from the builders' prose.

| # | check | result |
|---|---|---|
| 1 | coupler `--self-test`, plus a T13 spine and a both-L6-and-T13 spine | **PASS** (11 cases, rc 0, locally and inside jobs 40416441 and 40416438) |
| 2 | one real L6 frame recounted by hand from its JSON | **PASS** (four frames, call / margin_next / names identical to `coupling.json`), and the recount exposed finding F1 |
| 3 | no truth enters the coupler's call | **PASS** |
| 4 | threshold on other folds only; intervals clustered by case | **PASS** (30 of 30 taus recomputed identically; bootstrap reproduced), with the standing case-is-not-person caveat |
| 5a | the true alphabet read from truth names only on training films | **PASS** |
| 5b | the evaluation spines are in the validation split | **PASS** (independent read of `rung_1.npz`: 10 of 10 subjects val-only, 98 L6 crops, 0 bank keys on both sides) |
| 5c | lambda = 0 reproduces the shipped seed-0 film numbers | **PASS** (v8 seed 0 run by the verifier: identical on every protocol and source, max abs diff 0.0; v9 seeds 0-2: 79,490 of 79,490 rows identical, builder's table re-read) |

Findings that change how the shipped numbers must be read: **F1** (the oracle arm counts a duplicated truth box twice; every one of
its five L6 calls on the three L6 patients rests on that, four flip to ordinary when the duplicate is dropped), **F2** (the
sweep_v3 table holds no T13 spine and one L6 spine, never called L6), **F3** (at the detector's default confidence the coupling
does not improve the agreed C-ArmLSpine frames; at the pre-stated 0.74 floor it is a wash on whole frames and cannot anchor crops).

## 1. Self-test, extended

`python tools/alphabet_couple.py --self-test` passed its seven original cases (a-g) unchanged. Added to `self_test()`:

- **(h) T13 spine.** Seven bodies above the sacrum; the classifier reads the lumbar five right, the 13th thoracic as `T12`
  (p 0.6, T13 0.3) and the real T12 as `T12`. Ordinary names ordinal 7 `T11`; only the T13 alphabet fits the top body. Asserted:
  call `T13`, margin 0.68, names `T12 T13 L1 L2 L3 L4 L5`, ordinals 7..1, one disagreement (that body), `flag_reason` disagreement,
  both `T13` and `ordinary` among the candidates (they are distinct here because the window reaches the junction). PASS.
- **(i) both L6 and T13.** Eight bodies; the sixth lumbar read `L5` (0.6 / L6 0.3), the 13th thoracic `T12` (0.6 / T13 0.3), the
  rest right. Asserted: call `both`, margin 4.54, names `T12 T13 L1 L2 L3 L4 L5 L6`, two disagreements, all four alphabets
  distinct candidates, S(both) > S(L6) > S(ordinary) and S(both) > S(T13). PASS.
- **(i')** the same eight boxes read as `T10..L5`: call ordinary, no disagreement, no flag. PASS.
- **(j) a body boxed twice** (finding F1 in miniature): with the copy counted the count names one copy `T12`; with posteriors shaped
  like case42 AP (top body reads L2, the run leans one name caudal, the bottom body L5 at 0.99) the copy makes the L6 alphabet win a
  five-body spine; `--dedupe-boxes` drops it and the call is ordinary. PASS.

The T13 cases confirm what the docstring says and the shipped C-ArmLSpine cells cannot show: a lumbar-only field collapses
`ordinary` and `T13` into one candidate (`candidate_aliases`), so no T13 was ever callable on those frames. Nothing in the shipped
run exercised the T13 or `both` alphabets on a real frame.

## 2. Hand recount of real L6 frames

Script: `tmp/coupling_check/` (scratch), reading the raw prototype JSON (`vertebrae[i].box`, `vertebrae[i].posterior`, `sacrum_box`)
with its own enumerator (projection of box centres on the sacrum-to-centroid direction, rank away from the sacrum) and its own
alphabet scores (mean log p over counted bodies, `sweep_map.alphabet` re-typed by hand).

| frame | my ordinals (top to bottom) | my S(ordinary) | my S(L6) | my call, margin_next | coupling.json |
|---|---|---|---|---|---|
| case42 LAT, det, kfull (fold 2; LODO sacrum conf 0.857) | 5 4 3 2 1 | -2.7851 | -0.7550 | L6, 2.0301, names L2 L3 L4 L5 L6 | identical |
| case42 AP, det, kfull (sacrum conf 0.877) | 5 4 3 2 1 | -1.3130 | -2.2011 | ordinary, 0.8881, names L1..L5 | identical |
| case42 AP, oracle, kfull (truth sacrum) | 5 **6** 4 3 2 1 | -3.2419 (T13 -3.2695) | -2.0154 | L6, 1.2265 | identical |
| case121 AP, oracle, kfull | **6** 5 4 3 2 1 | -3.0876 | -3.0218 | L6, 0.0658 | identical |

The arithmetic matches. What the recount shows about the numbers themselves:

- **case42 LAT det** is the one frame where the thesis mechanism is visible on a real frame: five keypoint boxes above a detected
  sacrum, posteriors L2 0.892 / L3 0.996 / L4 0.962 / L5 0.917 for the upper four, so the L6 alphabet (L2..L6) scores -0.755 against
  -2.785 for ordinary; the bottom body, which the decoded `level` called `sacrum`, is renamed L6. This agrees with VERIDAH.
- **case42 AP det**: the decoded `level` names are L1..L5 but the posterior argmaxes are L2, L3, L4, L4, L5 (0.85 / 0.72 / 0.84 /
  0.72 / 0.52). The "classifier" the report scores is the anchored run decode, not the argmax; the coupler scores the posteriors.
  With five ordinals the ordinary alphabet still wins (0.89 margin), so this frame lands on TotalSegmentator's reading.
- **case42 AP and case121 AP oracle**: the truth meta holds six class-0 boxes for five bodies -- boxes 0 and 1 have IoU 0.984 and
  0.989 (both CBCT labellers boxed the top body). `--boxes-dir` feeds all six to the prototype and the coupler gives both copies an
  ordinal (5 and 6 at the same projection, 818 px). The count then has six bodies, and the L6 alphabet wins because it is the only
  one that names six ordinals L1..L6. Dropping the copy (below), case42 AP scores ordinary -1.43 vs L6 -1.70 and case121 AP flips
  the same way. **The oracle arm's L6 calls on these patients are made by the duplicate, not by the morphology.** See F1.

## 3. No truth in the call

`couple_frame()` computes `ords` (line 238, from `sacrum_box` and the vertebra boxes) and `c = couple(P, level_order, ords, which)`
(line 242) before the first read of `meta` (line 277, `if meta is not None:`). `couple()` takes only the posteriors and the
ordinals. `--truth-variant` reaches only `truth_from_variant()`, which produces truth names for scoring. `apply_tau()` in the report
uses `frame_all_correct_coupled` (truth) only to choose the pool on the other folds. In the det arm the anchor is
`sacrum_source = sacrum_detector` (LODO detector on the raw frame) and the boxes are the keypoint detector's -- confirmed per frame
in `l6_patients[].anchor.source` and in the raw JSONs. In the oracle arm the boxes and the sacrum ARE truth geometry
(`--boxes-dir`, `--sacrum-from-meta`): that is the declared oracle-boxes convention, and truth NAMES still never enter. PASS.

## 4. Threshold and intervals

- **Tau.** Recomputed for every (variant, field, fold) from the per-frame `couple_all.json` files with the stated rule (5th
  percentile of `margin_next` over the other four folds' anchored, agreed-truth, fully-correct frames; >= 20 frames or none):
  30 of 30 values and pool sizes identical to `coupling.json#tau`. The pool cannot contain fold K (filter `f["fold"] != K`).
  det/k5 folds 3 and 4 both read tau 2.1105 on 101 frames because folds 3 and 4 each contribute 27 eligible frames
  (0: 29, 1: 24, 2: 21, 3: 27, 4: 27) and the 5th-percentile frame lies in folds 0-2 -- a coincidence, not a copy.
- **Intervals.** `boot_rate` / `boot_diff` cluster by `f["case"]`, 2,000 resamples, seed 0. Re-run on det/kfull coupled accuracy:
  1207/1248 = 96.71 % [94.72, 98.50] over 143 cases, identical to the report.
- **Caveat carried forward, not introduced here.** The identity audit found a C-ArmLSpine case is not a person and that the CV
  needs day-grouped folds. The folds used are `md5(case) % 5` (`tools/carmlspine_fold_dirs.py` default; the CV dirs pre-existed
  and were not rebuilt): every test fold mixes all three acquisition days (fold 0: 13/12/10 cases on days 0/1/2; fold 1: 15/5/5;
  fold 2: 10/7/11; fold 3: 14/13/9; fold 4: 14/6/4). The coupler is rule-based, so this touches the classifier's posteriors (the
  fold model may have seen a patient from another day), not the coupling rule; clustering by case is what was asked and what was
  done, but it is not clustering by person.

## 5. The alphabet loss

- **(a) Truth only on training films.** `tools/head_mixed_length.py`: `ord_of` and `film_alpha` are filled in
  `for f in tr_films:` (line 268); windows are built from `tr_films` (line 302); `wcand` comes from those windows; `score()` never
  touches the alphabet code. Validation films keep `ord_of = -1` and never enter the term. With `--alphabet-loss 0` no alphabet
  code runs in the batch loop and no extra RNG draw is made. PASS.
- **(b) Evaluation spines are held out.** `SchwingNet/tools/coupling_check_split.py` (job 40416441) reads `allspine_v9_fov96_ctx/
  rung_1.npz` (`case`, `split`, `source`, `y`; 103,052 crops, 18,565 films) and `patient_keys_v9.json` (20,278 keys) directly: the
  ten subjects the report calls evidence are val-only under the bank's own key -- verse403 (26 films: scans verse208 + verse255),
  verse406 (31: verse214 + verse261), 509 (17), 517 (18), 525 (17), 540 (22), 569 (23), 604 (20), 614 (1), 816 (1); 98 L6 crops in
  total, the report's 98; 0 keys on both sides of the split, 0 split-conflict films. `SchwingNet/results/coupling_check_split.json`.
  Two labels in ALPHABET_LOSS.md are scan/subject conflations: "verse403 [=255+403]" is subject 403 = scans 208 + 255, and
  "verse406 [=261+406]" is subject 406 = scans 214 + 261. The 164 "leaking persons" are under the builder's implant-alias rule;
  under the bank's own key there are none. `tools/rigor_fixes.py` a5-rows scores `split == "val"` films only (line 763).
- **(c) Regression control.** The task names the shipped v8 seed 0. The builders ran v9 (the v8 bank leaks VerSe series). Both
  now hold: v9 seeds 0/1/2 re-trained at lambda = 0 are identical to `mixed_allspine_v9_mixed_kmax4_seed{0,1,2}.json` on every
  per-source and overall figure and on 79,490 of 79,490 a5 rows (`alphabet_loss.json#reproduction`, re-read); and the verifier's
  v8 seed-0 run with the modified trainer (job 40416411, `SchwingNet/results/coupling_check_v8_mixed.json`, scratch `--out`, nothing
  under `heads_mixed/` touched) equals `mixed_allspine_v8_mixed_kmax4_seed0.json` exactly: overall 0.7999 / 0.8277 / 0.8468 /
  0.8564 at bands 3/5/7/9 and 0.8360 at the random window, real film 0.9744 / 0.9862 / 0.9931 / 0.9993 / 0.9878, max abs diff 0.0.
  The alphabet import (`from sweep_map import alphabet as sm_alphabet`) is the decoder's own; the trainer refuses a bank whose
  classes are not `LEVEL_ORDER` when the term is on.

**Headline numbers re-read from `alphabet_loss.json`** (random window, cluster = person, paired against lambda = 0 at the same seed):

| lambda | L6 recall (60/55/55 of 98 at lambda = 0) | paired vs 0 (pp) | false-L6 rate of 12,911 non-L6 bodies | paired (pp) | real film pooled | paired (pp) |
|---|---|---|---|---|---|---|
| 0 | 61.2 / 56.1 / 56.1 % | -- | 0.18 / 0.14 / 0.18 % (23/18/23) | -- | 98.89 / 98.88 / 98.89 | -- |
| 0.3 | 67.3 / 63.3 / 64.3 % (66/62/63) | +6.1 [0.0, +13.3], +7.1 [0.0, +17.2], +8.2 [+3.0, +13.2]* | 0.29 / 0.26 / 0.27 % | +0.12*, +0.12*, +0.09* | 98.82 / 98.89 / 98.83 | -0.07, +0.01, -0.06 (none excludes 0) |
| 1.0 | 72.4 / 69.4 / 67.3 % (71/68/66) | +11.2 [+5.6, +21.3]*, +13.3 [+6.1, +19.4]*, +11.2 [+6.4, +18.2]* | 0.41 / 0.38 / 0.40 % (53/49/51) | +0.23*, +0.24*, +0.22* | 98.88 / 98.88 / 98.85 | -0.01, 0.00, -0.04 (none excludes 0) |

L5 called L6: 2.2/1.8/2.2 % -> 3.7/3.2/3.4 % -> 5.1/4.7/4.9 % (of 1,012). L6 precision 72/75/71 -> 63/65/64 -> 57/58/56 %. The
verdict labels (lambda 1.0 TRADE-OFF, lambda 0.3 NOT SHOWN TO HELP) follow the pre-stated rule as written. The evidence base is
10 VerSe subjects (the seven CTSP L6 persons with validation films all have an implant twin in training and were excluded) and
**no T13 at all** in validation (six VerSe T13 subjects all train): the T13 half of the alphabet was never evaluated. The
alphabet term had 3,007-3,010 anchored windows of 22,443 per epoch to train on; its cross-entropy fell from 0.31 to 0.04 (0.3)
and 0.24 to 0.03 (1.0).

## F1. The oracle arm counts a duplicated truth box twice

`--boxes-dir` gives the prototype every class-0 truth box, and where both CBCT labellers boxed a body it arrives twice (IoU 0.98-0.99).
The coupler's enumerator has no duplicate rule for prediction boxes (only the truth side is deduped, and only for the variant
patients), so both copies take ordinals and every body above them shifts by one. Measured from the shipped `couple_all.json` files
(scratch script; `tmp/coupling_check/`):

| cell | anchored agreed frames | with a duplicate counted twice | count-only errors in them | "introduced" errors in them | L6 calls in them |
|---|---|---|---|---|---|
| oracle/kfull | 286 | 64 (22.4 %) | **31 of 31** (clean frames 1061/1061 = 100.0 %; dup frames 237/268 = 88.4 %) | 15 of 20 | 2 of 5 |
| oracle/k5 | 52 | 9 (17.3 %) | **4 of 4** (clean 212/212) | 8 of 8 | 1 of 3 |
| det/kfull, det/k5, det74/* | -- | 0 | -- | -- | -- |

So the shipped "count from the truth sacrum 97.7 %" is a perfect count spoiled by 64 double-boxed frames, and the oracle arm's
transitions (36 corrected / 20 introduced) and its five L6 calls are contaminated. On the three L6 patients **all five oracle L6
calls on whole frames sit on a duplicated top box** (ordinals `5 6 4 3 2 1` / `6 5 4 3 2 1` in the report's own table).

Re-coupled with a duplicate-drop (`tools/alphabet_couple.py --dedupe-boxes`, IoU > 0.9 to an earlier box; off by default so the
shipped outputs stay reproducible; self-test (j)) and re-pooled by the builder's unchanged `coupling_report.py` through
`SchwingNet/tools/coupling_check_dedupe.py` (job 40416438, `SchwingNet/results/coupling_check_dd/{coupling.json,COUPLING.md}`; the
det and det74 cells in that re-pool equal the shipped ones exactly):

| cell | classifier | coupled | count alone | corrected / introduced | L6 calls (all false; anchored agreed frames hold no L6) |
|---|---|---|---|---|---|
| oracle/kfull (shipped) | 94.4 [91.7, 96.9] (1274/1349) | 95.6 [93.7, 97.4] (1290/1349) | 97.7 (1298/1329) | 36 / 20 | 5 |
| oracle_dd/kfull | 94.4 [91.7, 96.8] (1239/1312) | **98.2 [96.4, 99.6]** (1288/1312) | **99.6** (1287/1292) | 56 / 7 | 3 (case132_LAT, case19_AP, case54_AP) |
| oracle/k5 (shipped) | 91.0 (1356/1491) | 92.1 (1373/1491) | 98.4 (253/257) | 25 / 8 | 3 |
| oracle_dd/k5 | 90.8 (1304/1436) | 92.6 (1330/1436) | 100.0 (250/250) | 26 / 0 | 2 |

L6 patients under oracle_dd, whole frames: case42 AP -> ordinary (margin_next 0.28), case121 AP -> ordinary (1.87), case136 AP ->
ordinary (0.63), case136 LAT -> ordinary (0.97); case42 LAT stays L6 (1.44), the same frame the det arm calls L6. So with the
duplicate gone the oracle arm agrees with VERIDAH on one frame of six and with TotalSegmentator on four, the same picture as the
det arm (1 and 4), instead of the shipped "VERIDAH on 2, calls L6 5". The denominators change (1349 -> 1312 bodies) because the
duplicate truth box was itself matched and scored: **the shipped oracle CLASSIFIER number, and every earlier oracle-boxes number in
the C-ArmLSpine CV, scores a double-boxed body twice and decodes a run over six boxes for five bodies.** That is older than this
task and was not re-run here; it is flagged for whoever quotes an oracle-boxes accuracy.

## F2. The sweep_v3 "anomalous renders" table is not L6/T13 evidence

`sweep_variant_calls.json` (62 arms): no arm contains a T13 spine; the only L6 spine in any CTSP arm is `CTSP_COLONOG_672`, one
spine, and the decoder never called it L6 (called `T13` in 24 arms, `ordinary` in 16; chain count on it 1/10 or 1/15, as an
ordinary count on an L6 spine must be). The TS arms hold L4 and ordinary spines only. Separately, the collector read every arm's
`args` as `None`, so the table's "sources / anchor / alphabets / NOT held out" column is unread, not a statement about the arms.
Nothing in COUPLING.md tests the T13 or `both` alphabets on a render; the synthetic cases (h)/(i) are the only such test.

## F3. What the det cells say, re-read

- det/kfull (LODO sacrum at conf 0.25, the default): classifier 97.4 % [95.3, 99.2] (1216/1248), coupled 96.7 % [94.7, 98.5]
  (1207/1248); on counted bodies it corrects 13 of 20 classifier errors and introduces 22. Six L6 calls, all on ordinary spines,
  all flagged. The coupling does not improve these frames at this operating point.
- det74/kfull (the pre-stated 0.74 floor): coupled 97.6 % [95.8, 99.1] vs classifier 97.4 %; corrects 13 of 16, introduces 11;
  four L6 calls, all false, all flagged; anchors 233 of 290 frames. The stop signal fires on 4 of 5 frames with a coupled error
  and 7.6 % of fully correct frames; unflagged coupled accuracy 99.9 % (921/922). A wash on accuracy, a usable flag.
- det/k5: coupled|anchored 90.1 % vs classifier 98.4 %, 58 introduced and 0 corrected, 13 false L6 calls: the LODO sacra on
  five-vertebra crops are false anchors. det74/k5 anchors 6 of 321 crops. The crop field cannot be coupled with this detector.
- The three L6 patients (det, whole frames, 5 of 6 anchored): coupled = VERIDAH on 1 (case42 LAT), = TotalSegmentator on 4;
  the classifier alone = VERIDAH on 0. That is the whole real-frame evidence for the L6 half of the thesis, and it is agreement
  with one CT labeller against another, as COUPLING.md says.

## Files written by the verifier

- `tools/alphabet_couple.py`: self-test cases (h), (i), (i'), (j); `--dedupe-boxes` (off by default; `couple_frame(dedupe_boxes=)`,
  `n_boxes_dropped_as_duplicates` in every frame record). Shipped outputs are unchanged by default.
- `SchwingNet/tools/coupling_check_split.py`, `SchwingNet/tools/coupling_check_dedupe.py`;
  `SchwingNet/slurm/coupling_check.sh`, `coupling_check_v8.sh`, `coupling_check_dd.sh`.
- `SchwingNet/results/coupling_check_split.json`, `coupling_check_v8_mixed.json`, `coupling_check_dd/{coupling.json,COUPLING.md}`;
  logs `tmp/coupling_check/coupling_check{,_v8,_dd}-*.out`; per-frame inputs under `tmp/coupling_check/proto_post/` and truth metas
  under `tmp/coupling_check/meta_cv/` (rsynced, not committed).
- Nothing was committed.
