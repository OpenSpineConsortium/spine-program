# VERIFY: the eval-gate closure checked from outside its own outputs (2026-09-24 15:50 EDT)

Written on the resume of 15:28. No grid job was submitted: the CHK-9 re-run had already completed (job 40437099,
11:15:11-11:15:57, 46 s, reqp, exit 0:0) and its outputs were sitting on the grid uncollected. Everything here is
read from files, re-derived locally from raw per-fold dumps pulled to `closure/verify/raw/` (848 KB, 15:32 EDT),
or read from the lineage store's on-demand cache with login-node `grep`. No manuscript file was edited. Scripts and
their outputs are under `closure/verify/` (`verify_cv9.py`, `verify_coupled.py`, `lineage_check.py`,
`verify_cv9_rederived.json`, `lineage_check.json`, `lineage_rows.txt`).

## 1. CHK-9 over quoted_results.json with the cv_v9 rows substituted: before and after

Inputs (from `closure/chk9_cv_v9/chk9cv9_40437099.out`): staged eval_gate/2 code (`tools/leak_check.py` md5
229f0db6, `tools/eval_gate.py` 2b0c9e05 = GATE_VERSION "eval_gate/2", `patient_keys.py` 83b8650d,
`checkpoint_lineage.py` 14c09384; all equal to this checkout); lineage store `touched.json` of 2026-09-23 19:53:07
with 629 on-demand files (each v9-init fold encoder present in 2 of them, each head in 1); `eval_sets.json` of
2026-09-24 07:59:09; `quoted_results_before.json` md5 2f5b1cfd (the committed file) against
`quoted_results_cv_v9.json` md5 0af3e716 (`make_quoted_cv_v9.py`: 59 rows moved from the deleted `allspine_v2_r1`
lineage to the `allspine_v9` one; nothing else changed). Nothing was written under the store (the job's final `find`).

| count | before | after |
|---|---:|---:|
| rows | 563 | 563 |
| CLEAN (HELD OUT) | 323 | **380** |
| LEAKED (SEEN) | 81 | 81 |
| UNRESOLVED | 58 | **1** |
| NO EVAL KEYS | 0 | 0 |
| DECLARED | 0 | 0 |
| N/A | 101 | 101 |

- **57 rows moved, all inside the 59 substituted rows, every one UNRESOLVED -> HELD OUT** (the 40 NUMBERS rows,
  CLAIMS L211, the 14 Figure 4 records, `figure5/03`, RESCORE G1/H1/H2 of MANUSCRIPT_CORRECTIONS §7.2). Zero rows
  outside the substituted set changed verdict.
- The other 2 substituted rows (`NUMBERS:L108`, `L223`) stay SEEN: their pair `detector_v5z_final on nhanes25` is
  the as-quoted 25-spine render-vs-film comparison (24 of 25 spines in that detector's own lists), which §3a
  already replaced by the 17-spine held-out rerun; the substitution did not touch that pair.
- **The one row still UNRESOLVED is `FIGREC:figS2/07`**, the device-card refit gate: it names no (checkpoint,
  evaluation set) pair at all, because `card_refit` records `n_train` / `n_held` and not which frames were fitted
  and held. The hand inventory already says NOT ESTABLISHED. It is not a cv_v9 row and no re-run resolves it; it
  needs `tools/device_fit.py` to write the fitted / held frame keys per fold (a code change for the device-card
  owner, then a CPU re-fit).
- The 81 SEEN rows are the same set before and after (identity checked, not just the count). Their driving pairs:
  `allspine_v9_encoder on v9_val_clean` 31 and `on v9_val` 1 (the checkpoint-selection split; the manuscript
  labels every such number "selection split"), `allspine_v8_encoder` / `v8_head_seed0 on v8_val` 9 + 9 (same),
  the device cards `card:bv_pulsera` / `card:pixium_4600` 13 + 13 and `card_median:*` 16 (the within-subject
  folds §3b re-read), `detector_v5z_final on nhanes25` 9 (§3a's replaced comparison), `rx_lodo_carmlspine_1024 on
  cobra_test` 2, and the void 17-subject arc 4. **CHK-9 against the hand inventory (EVALUATORS.md) after the
  substitution: 0 rows disagree.**
- Both runs exit 1 ("LEAK FOUND") because the 81 SEEN rows exist in both; that is the file's known state, not a
  new leak.

**Verdict.** CLEAN 323 -> 380, LEAKED 81 -> 81, UNRESOLVED 58 -> 1. Not done: the repo's
`results/eval_gate/quoted_results.json` still carries the old rows; `quoted_results_cv_v9.json` becomes the file
of record when the eval-gate workflow adopts it (the manuscript already prints the §7 numbers, see
MANUSCRIPT_CORRECTIONS_ORDERED.md).

## 2. Three cv_v9 cells re-derived from the raw fold dumps (and two more)

Raw inputs: `det_score_kfull.json` of `cv_fold0-4` and `cvday_fold0-2` under grid
`/rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init_prerepair/` (written 08:41-08:57, job 40436580), copied
to `closure/verify/raw/`; the five `couple_all.json` already under `cv_v9/fig4_inputs_pre/`. The cell is the sum
over frames of `items[].exact` (the whole-frame, detector-matched vertebrae), clustered by `case`; nothing is
read from the aggregate files these cells were quoted from (`rigor_pre/a4.json`, `a9.json`,
`carmlspine_cv5_v9init_pre.json`, `coupling_pre/coupling.json`).

| cell | quoted (MANUSCRIPT_CORRECTIONS §7.1 / §7.2) | re-derived | equal |
|---|---|---|---|
| lateral, whole frame, case-grouped | 97.4 % (601/617), 141 cases, 4 with an error | 601/617 = 97.41 %, 141 cases, 4 with an error, 148 frames | yes |
| AP, whole frame, case-grouped | 96.4 % (608/631), 142 cases, 7 with an error | 608/631 = 96.35 %, 142 cases, 7 with an error | yes |
| lateral, whole frame, day-grouped | 92.1 % (568/617), 12 of 141 cases | 568/617 = 92.06 %, 141 cases, 12 with an error | yes |
| AP, whole frame, day-grouped | 94.8 % (598/631), 9 cases | 598/631 = 94.77 %, 142 cases, 9 with an error | yes |
| coupled at 0.74, counted bodies | coupled 991, classifier 986, count 979 of 1,009; 233 anchored frames; 130 cases | 991 / 986 / 979 of 1,009; 233 anchored frames of 290 with agreed truth; 130 cases | yes |

The coupled cell reproduces only under the coupler report's own rule (`SchwingNet/tools/coupling_report.py
cell()`): frames whose `truth_source` is `labellers_agree` (290 of 296; the 6 others are the frames of the three
one-labeller L6 cases scored under the `variant_alphabet:L6` truth), anchored = a call other than "no anchor" /
"no alphabet", counted = a truth-matched body with an ordinal. A first pass that took every frame with an accepted
anchor and summed `n_scored_counted` gave 996 / 994 / 979 of 1,029 over 234 frames; the 20 extra bodies are those
six variant-truth frames. That is recorded so nobody repeats the detour.

## 3. The eval_gate blocks on those dumps are genuine

Per dump, from `eval_gate` in `det_score_kfull.json` and `det/kfull/prototype_meta.json`
(`verify_cv9_rederived.json#gate`):

| fold | gate | held out | checks | overlap | unresolved | keys checked = cases scored | encoder sha256 in the check = `prototype_meta.level_model_sha256` |
|---|---|---|---|---|---|---|---|
| cv_fold0 | eval_gate/1 | true | 5 | 0 | 0 | 35 = 35 | 071a7b8c… yes |
| cv_fold1 | eval_gate/1 | true | 5 | 0 | 0 | 25 = 25 | be4eb8af… yes |
| cv_fold2 | eval_gate/1 | true | 5 | 0 | 0 | 28 = 28 | a7cb4dac… yes |
| cv_fold3 | eval_gate/1 | true | 5 | 0 | 0 | 36 = 36 | af14c417… yes |
| cv_fold4 | eval_gate/1 | true | 5 | 0 | 0 | 24 = 24 | a143ae31… yes |
| cvday_fold0 | eval_gate/1 | true | 5 | 0 | 0 | 66 = 66 | cb33045f… yes |
| cvday_fold1 | eval_gate/1 | true | 5 | 0 | 0 | 43 = 43 | 07dc5ff6… yes |
| cvday_fold2 | eval_gate/1 | true | 5 | 0 | 0 | 39 = 39 | c57be844… yes |

- The five checks of every dump are the detector (`detect_v5z_final_best.pt`, ancestor `detect_v3`, public root
  COCO yolo11m-pose), the fold encoder (ancestor `allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt`, public root
  ImageNet resnet18), the fold head (ancestors: the fold encoder, then the v9 encoder), and the two flag models
  (`lstv_flag_v2.pt`, `tltv_flag_v2.pt`, no ancestors). Every check says `lineage_match: path + sha256 verified`,
  `n_unkeyed 0`, `pose_donor_overlap 0`, `keys_by_corpus {carmlspine: n}`.
- Every checkpoint that appears in more than one dump carries one sha256 across them (19 checkpoints checked).
- The five case folds are disjoint and their union is 148 cases; the three day folds are disjoint with the same
  union. Frames scored per fold equal the keys the gate checked.
- Caveat, as §7.0 already says: the grid clone's gate was eval_gate/1 when these were scored, so the blocks carry
  `checkpoint_sha256` per check but no dump-level `weights_sha256`; an eval_gate/2 scorer refuses them until the
  evaluators are re-run under it or the read is declared. The verdicts are the same under both versions (the keys
  and the store are what changed nothing).

## 4. No test case in any v9 ancestor list (read from the lineage store, not from the gate's verdict)

The on-demand lineage rows the gate computed for the eight fold encoders and cached under
`or_ready/eval_gate/ondemand/` were read with login-node `grep` (`closure/verify/lineage_rows.txt`) and
intersected locally with each fold's test cases (`lineage_check.py`, `lineage_check.json`):

| fold model | own train + val persons (C-ArmLSpine, keyed `case:<n>`) | test cases | test in own train or val | test in `touched_keys` | C-ArmLSpine keys in the `allspine_v9` ancestor row |
|---|---|---|---|---|---|
| cv0 | 87 + 23 = 110 | 35 | none | 0 | 0 |
| cv1 | 95 + 27 = 122 | 25 | none | 0 | 0 |
| cv2 | 82 + 36 = 118 | 28 | none | 0 | 0 |
| cv3 | 85 + 24 = 109 | 36 | none | 0 | 0 |
| cv4 | 86 + 35 = 121 | 24 | none | 0 | 0 |
| cvday0 | 67 + 12 = 79 | 66 | none | 0 | 0 |
| cvday1 | 86 + 17 = 103 | 43 | none | 0 | 0 |
| cvday2 | 93 + 15 = 108 | 39 | none | 0 | 0 |

- The fold banks key a C-ArmLSpine person as `case:10`; the evaluation keys it as `carmlspine:case10`.
  `tools/patient_keys.canon_key` maps `case:10` -> `carmlspine:case10` (run locally), and `eval_gate.assess` applies
  `canon_key` to both sides (`_canon_set`), so the fold model's overlap 0 is a real comparison of the same
  spelling, not an empty intersection between two spellings. The intersections above were computed on the
  canonical keys.
- The `allspine_v9` encoder row (train 15,754 items, val 2,811; key corpora buu, csxa, ctsp, fluorocap,
  fluorocap_video, nhanes, ts, verse, vindr) holds **zero** keys of the carmlspine corpus in either spelling. All
  220 `case:` keys in the fold-0 cache file sit in the fold model's own row (train 87, val 23, touched 110).
- Not checked here: the zero-shot head `head_allspine_v9_mixed_kmax4_seed0.pt` has no on-demand row (its row is in
  `touched.json` itself, per `make_quoted_cv_v9.py`); its training list is the v9 bank's train split, the same
  list whose keys are tabulated above, so the conclusion carries, but that row was not re-read.
- Each fold model's train + val persons fall 1-3 short of the non-test case count (113 / 123 / 120 / 112 / 124 for
  the case folds). The shortfall equals, fold by fold, the number of the three one-labeller L6 cases (case42,
  case121, case136) outside that fold's test set, which fits those three being kept out of every fold bank. That
  is an inference from counts, not a list read.

## 5. What this closure did not do

- No manuscript edit; no commit (the coordinator commits).
- `quoted_results.json` was not replaced (section 1).
- `FIGREC:figS2/07` stays UNRESOLVED (section 1).
- The eval_gate/2 re-runs of `leaks/render_vs_film_unseen_rerun.json`, the published unseen arc curve and the
  device-card sidecars (MANUSCRIPT_CORRECTIONS §5.4, §6.4) were not run; their numbers are not in question.
- The zero-shot head's `touched.json` row was not re-read (section 4).
