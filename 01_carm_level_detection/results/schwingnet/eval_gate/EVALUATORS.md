# Every evaluator and every quoted result, checked against the held-out rule

Written 2026-09-23. It covers every script that turns a checkpoint and an evaluation set into a reported number, and
every number the manuscript quotes. Each number is traced to the checkpoint that produced it, that checkpoint's
initialisation chain, and the train and val (selection) lists of every link in the chain.

- Machine-readable rows: `quoted_results.json`. It had 406 rows after the 21:10 regeneration against the current
  NUMBERS.md, and 563 since the EVAL_LEAKS sweep of 2026-09-24 added every number drawn on a figure
  (`figures/figureN.record.json`). The sweep's row-by-row verdicts are in `EVAL_LEAKS.md`.
- Generator: `build_inventory.py`, in this directory. It rewrites only the `GENERATED` blocks below.
- **Since this was written** the gate exists and is wired in: `tools/eval_gate.py` (docs/DATA_ACCOUNTING.md §5.3), and
  leak_check CHK-9 re-checks every row here mechanically from `touched.json` and `eval_sets.json`
  (`chk9/CHK9_REPORT.md`). Where the two differ, CHK-9 is the computed reading: it finds UNRESOLVED 40 rows this
  inventory calls HELD OUT on a public-weights assumption for `allspine_v2_r1`, whose training bank is deleted.
- Lineage facts: read on the grid on 2026-09-23, from `args.yaml`, `data.yaml`, the devcorpus list files,
  `prototype_meta.json` and `registry.jsonl`. Each fact names the file it came from. No checkpoint was loaded.

**The rule.** An evaluation item counts as held out for a checkpoint only if its patient key is in none of these:

- the checkpoint's own train set;
- its own val (selection) set;
- the train or val set of any ancestor in its initialisation chain.

A render inherits the patient key of its source CT subject. Public COCO or ImageNet weights are the only exempt
ancestor, and only when their use is declared.

**Verdicts.** Each row gets one of:

- `HELD OUT`: established from recorded lists.
- `NOT HELD OUT`: an evaluation token appears in a train or val set somewhere on the chain.
- `MIXED`: the row pools pairs whose verdicts differ.
- `NOT ESTABLISHED`: lineage is missing.
- `N/A`: no checkpoint is involved (a count, a parameter value, arithmetic or a published number).

Pose-donor overlap is reported in its own column and does not change the verdict. A styled or anchor render is a
TotalSegmentator subject ray-cast under the registered pose of a real frame, so it carries that frame's pose but not
its patient.

Other agents were editing four gate files uncommitted while this was written: `tools/model_registry.py` (a new
`lineage.jsonl`), `tools/train_level_classifier.py` (now records `init`, `train_list`, `val_list`),
`tools/patient_keys.py`, and `tools/leak_check.py` (the pose-donor regex now accepts COBRA and C-ArmLSpine donors).
`tools/checkpoint_lineage.py` is referenced by those edits but does not exist yet, and `~/model_registry/lineage.jsonl`
is not on the grid. Everything below describes the code and the grid as they were read, before those changes land.

---

## 1. What this found

### 1.1 The arc leak is one of a class

The recall-against-angle curve scored four checkpoints on 17 TotalSegmentator subjects. Those subjects are the
validation subjects on which `dc_P_pooled`, `dc_A_held_surgio_b51_dr` and `dc_B_held_surgio_b51_dr_s1` chose
`best.pt`. `rx_lodo_carmlspine_1024` was initialised from `anchor_none_v2_17-1882`, whose training images include
14 renders each of s0585, s0970, s1045, s1159 and s1384, and whose validation images include 14 of s1062. This was
counted on the grid.

The curve is not quoted: Figure 4d is still `\PENDING{G4}`. Three quoted result families rest on the same mistake,
and a fourth is not patient-held-out by construction.

1. **Plain-film naming, all three corpora: NOT HELD OUT.**
   - Quoted as CSXA 99.8 %, BUU-LSPINE 97.3 % and NHANES II 99.1% (`results/a5.json`).
   - It appears in the Table 3 "validation" rows, in `sections/results.tex:55` ("patient-keyed film validation read
     97.3–99.8 % exact") and in `sections/methods.tex:43` ("Film validation is keyed by patient").
   - The films scored are the `allspine_v8` validation split.
   - `tools/train_level_classifier.py` kept the best of 40 epochs by exact accuracy on that same split: `best_state`,
     lines 410–472, launched by `slurm/allspine_v8_train.sh`.
   - The a5 "leak check" (0 validation patients in training) compared val against train only, so it could not see
     this.
2. **`rx_lodo_carmlspine_1024` on COBRA or DeepFluoro: NOT HELD OUT.**
   - This is the headline detector. Its `data.yaml` sets `val` to the COBRA **test** and DeepFluoro **test** splits,
     so `best.pt` was selected on them. `sections/methods.tex:49` says so.
   - Its numbers on C-ArmLSpine are clean, and those are the ones quoted.
   - Its numbers on `cobra_test` and `df_test` are selection-set numbers. They appear only in `lcurve.md` and in
     rescore rows `C_cobra_ar_C-ArmLSpine_held_out_{0.74,0.25}` (814/893 = 91.2 %), not in `main.tex`.
   - `rx_lodo_cobra_elekta_1024` and `rx_lodo_deepfluoro_1024` were selected the same way, on the other two devices'
     test splits. Only their own held-out device is quoted.
3. **Film-trained detector in the render-vs-film comparison: NOT HELD OUT.**
   - Quoted as 99.14 % against 71.67 %, a +27.5-point difference (`a3.json#comparisons/render_vs_film_detector`,
     Figure 3c, Table 2).
   - It is already declared in-sample: 196 of the 233 bodies come from spines in the `allspine_v7` train split.
   - The declaration was made against the wrong list. `rigor_fixes a3a-rows` called `holdout.trained_on`, which is
     the only gate call on any manuscript path, but it pointed it at the level bank `allspine_v7`. The detector's
     own film train and val lists are recorded nowhere: its registry entry has `bank ''`.
   - The paired difference is therefore MIXED: the render-trained side is held out, the film side is not.
4. **Device cards: MIXED.**
   - `tools/device_fit.py` fits leave-one-group-out.
   - The groups are patients for Cios Fusion (the DeepFluoro specimen) and Elekta XVI (the COBRA case).
   - BV Pulsera has one phantom and its groups are views. PIXIUM 4600 has one cadaver and its groups are frames.
   - So the per-device gains for BV Pulsera and PIXIUM, the pooled 24-fold +0.0376, and the "held-out R²" columns of
     Table 1 and Table S1 all include folds that are not patient-held-out.
   - The Figure 4a pair R² values are computed under the median of the six fold fits, and five of those six fits saw
     the pair's own group (`SchwingNet/tools/fig4_pairs_pull.py:209`). They are in-sample and illustrative. The
     figure as drawn (`figures/fig4_formation.record.json` `panel_a`) shows 0.973 / 0.888 / 0.975 / 0.655.
     NUMBERS.md:164–167 still lists the earlier pick (0.964 / 0.888 / 0.979 / 0.655); see 1.4.

### 1.2 What passes the rule

These families are HELD OUT under the patient-key rule; the reasons are in the lineage table in §4:

- the held-out detector on C-ArmLSpine: 80.5 %, 90.6 %, 76.8 %, 83.9 % and the whole a1 curve;
- the same-device control comparison (a3 pooled vs held-out);
- counting from the sacrum;
- coupling;
- C-ArmLSpine naming with case folds and with day folds (a4, a7, a9);
- zero-shot naming (96.3 % / 37.9 %);
- every contribution-matrix cell;
- the learning-curve stage-1 and all-real control cells on their own device (except the two rows in 1.1.2);
- every detector cell of Figure 3.

Two of these rest on file timestamps rather than recorded lists:

- **Zero-shot.** `zeroshot2/prototype_meta.json` records `detector_v5z_final` (sha 797de71a…) and `allspine_v2_r1`
  (sha 00e84a90…), with no head. The detector file was written at 2026-09-14 09:33 and the encoder registered at
  2026-09-15 08:13. C-ArmLSpine reached the grid through fetch job 40409970, whose log closed on 2026-09-21 at
  17:44. The file times inside the unpacked archive read 2026-09-15 16:55, and even those are later than both
  models.
- **C-ArmLSpine fold models.** Their chain runs `allspine_v2_r1` → ImageNet-if-cached. Fold K's cases were excluded
  from fold K's bank by `carmlspine_to_bank --fold K`.

A C-ArmLSpine "case" is an acquisition session, not a proven person. This is why the day-grouped folds exist, and
every C-ArmLSpine verdict carries that caveat.

### 1.3 Pose-donor dependencies (reported, not scored)

The rule is about patients, so none of these changes a verdict. They are listed because `tools/leak_check.py` check (6)
treats a pose donor as a dependency, and the coordinator may decide the rule should too. All counts were read from the
list files on 2026-09-23.

- **`anchor_none_v2_17-1882`.** It trained and validated on 294 renders under the poses of DeepFluoro test specimen
  18-1109 (255 train, 39 val). It is the ancestor of every `rx_*` arm, so `rx_lodo_deepfluoro_1024`, `rx_pooled_1024`
  and the render arm itself carry that dependency on `df_test`.
- **Design A arms.** These put every card under the Cios Fusion pose pool. `dc_A_held_cios_fusion` holds out
  DeepFluoro but trained and validated on 1,756 renders under 18-1109's poses (and under the other DeepFluoro
  specimens' poses). It is then scored on those specimens' real frames: Table 2's "six specimens" rows and the seed
  spread.
- **`dc_P_pooled`.** 658 renders under C-ArmLSpine test-case poses, 412 under COBRA test-case poses, and 2,634 under
  18-1109's poses.
- **Learning-curve fine-tunes (`lc_*`).** Every list holds all 7,322 styled renders. Those include 598 under
  C-ArmLSpine test-case poses, 368 under COBRA test-case poses and 762 under 18-1109's poses. Figure 3b already draws
  these points (`fig3_detection.numbers.json` panel b, `points[1..7]`). NUMBERS.md's Figure 3 table predates that.
- **The guard that did not look.** `tools/devcorpus_build.py:cmd_pooled` checks two things: that the styled corpora
  agree on validation subjects, and that no real specimen sits on two sides of a split. It does not compare the pose
  donors of styled renders against the real test splits.

### 1.4 Sentences that are wrong or stale

These are named here, not edited. The manuscript files belong to the manuscript workflow.

| where | what it says | what the files say |
|---|---|---|
| `SchwingNet/NUMBERS.md:113` | "detector: YOLO11m from COCO, 80 epochs …" (`rx_lodo_carmlspine_1024/args.yaml`) | `args.yaml` `model:` = `runs/pose/anchor_none_v2_17-1882/weights/best.pt`. The chain is COCO → anchor → lodo. `atlas/model.json` already says this correctly. |
| `results/lcurve/lcurve.json` `all_real` description | "rx_only_carmlspine_1024 … COCO init" | Its init is the same anchor. |
| `SchwingNet/tools/contribution_matrix.py` `LODO_ARMS["render"].note` | "CTSpinoPelvic1K renders under DeepFluoro specimen 17-1882's poses" | The renders are TotalSegmentator subjects, under the poses of the five other specimens. 17-1882 is the held specimen, with 0 renders. |
| `results/arc/case134_sweep.json` `contamination.pooled` | "the pooled detector saw this patient's two SPOT frames in training" | `P_pooled/{train,val}.txt` hold 0 case134 lines. The case134 frames entered `realxray/carmlspine/images/train` on 2026-09-23 at 05:28, after `dc_P_pooled` `best.pt` (01:46). The claim errs in the conservative direction. From now on, though, case134 **is** in the C-ArmLSpine train split: no detector trained on that split after 05:28 is held out for the case134 spin. |
| `tables/tab_corpus.tex:43` | "styled device corpus (142 subjects, 17 held out)" | The 17 are the validation (selection) subjects of every `dc_*` arm. |
| `sections/methods.tex:43`, `sections/results.tex:55`, Table 3 "validation" rows | film validation as a held-out result | It is the encoder's selection split (1.1.1). |
| `results/anomalous_inventory.json` `note`; `sections/results.tex:16` ("65 in the training half of the bank behind the accuracies below") | "validation = usable as evidence for the level model" | Under the rule, the v8 validation half is not evidence either. |
| `tools/learning_embed.py` docstring | "read off HELD-OUT crops only … the validation split of the crop bank" | Same mistake: the val split is the encoder's selection set. |
| `SchwingNet/NUMBERS.md:164–167` (Figure 4a) | BV Pulsera pair p02 / 071kv, R² 0.964; Elekta XVI pair A004 / 0264, R² 0.979 | The drawn figure (`fig4_formation.record.json` `panel_a`, re-picked in commit 421138c) shows BV Pulsera p20 / 085kv, R² 0.973, and Elekta C005 / 0136, R² 0.975. Cios Fusion and PIXIUM are unchanged. |
| `tools/needle_confirm.py` | `--holdout-bank` is `required=True` | The argument is never read: the source has no `a.holdout_bank`, and `--allow-trained-on` defaults to True. No quoted number depends on this script. |

---

## 2. Why the contract did not catch it (read from the code)

**(1) The gate is opt-in, and no evaluator on a manuscript path opts in.**

- The scripts that load a checkpoint and score an evaluation set make **zero** gate calls: `tools/realxray_eval.py`,
  `tools/arc_recall_eval.py`, `tools/case134_sweep.py score`, `tools/level_prototype.py`,
  `tools/head_mixed_length.py`, `tools/devcorpus_train.py score`, `tools/lcurve_train.py`,
  `tools/or_recall_curves.py sweep`, and `tools/rigor_fixes.py a5-rows`.
- `rigor_fixes a3a-rows` is the single call to `holdout.trained_on` on any manuscript path, and it points at the
  wrong bank (1.1.3).
- Some tools do take `--holdout-bank`: `sweep_map`, `validate_guided`, `fiducial_walk`, `needle_confirm`,
  `detector_quality` and `detector_failures`. None of them produces a quoted number.

**(2) Every gate treats only `split == "train"` as seen.**

- `holdout.trained_on` returns the `train` case ids only. `sweep_map.py:1870` repeats the same loop.
- The a5 leak check compares val with train.
- `data_lineage.scan_models` records a model's bank val split as its `eval` ("what the trainer scores on").
- `leak_check.lineage_from_graph` maps every registry model to `train=bank#train`, `eval=bank#val`. It therefore
  declares the selection split as the evaluation split.
- `leak_check.DEFAULT_LINEAGE` has exactly one entry that books `train,val` as seen: the anchor detector's.
- `or_recall_curves.DETECTORS` knows that the lodo arms were `selected_on_test`, but uses it only as a curve label.
- The status labels in `devcorpus_train` and `contribution_matrix` (`DEVICE-HELD-OUT` and so on) are hand-derived
  from the arm's design, not from lineage.

**(3) There is no lineage to check against.**

- `~/model_registry/registry.jsonl` has 66 lines. It holds **none** of the YOLO runs that produced the detection
  numbers: the 7 `rx_*`, 19 `dc_*` and 19 `lc_*` runs, and the `anchor_none_v2_*` runs. It does hold the eight
  C-ArmLSpine fold encoders and the v8 encoder, but none of the run heads.
- Where an entry exists, it records `bank` only, with no parent and no val list. `detector_v5z_final` has
  `bank ''`.
- The dumps do record the weights path: `realxray_eval` writes `weights`, and `prototype_meta.json` writes both
  sha256. So a gate at the scoring step could resolve lineage, if lineage were stored anywhere.
- Today the parent of a YOLO run is readable only from its `args.yaml` `model:`. The parent of a level fine-tune is
  readable only from the `--init` in a slurm script.

---

## 3. The evaluators

### 3.1 On the path of a quoted number

This table shows where a gate has to sit: at the step where the checkpoint and the evaluation set first meet. Later
steps read dumps and must carry that verdict forward, because every dump names its weights and nothing else does.

| step | entry point | checkpoint arrives as | evaluation set arrives as | gate today |
|---|---|---|---|---|
| detector score | `tools/realxray_eval.py` (main) | `--weights` path | `--data <realxray bank> --split <split>` | none |
| arm sweep | `tools/or_recall_curves.py sweep` | hand `DETECTORS` table (weights paths) | hand `DATASETS` table | none (`trained_on` / `selected_on_test` are labels) |
| devcorpus arm | `tools/devcorpus_train.py train/score` | the run's `weights/best.pt` | every device's `test` split | none (status hand-derived) |
| learning curve | `tools/lcurve_train.py` | parent `best.pt` → fine-tuned `best.pt` | device `test` split | none |
| angle sweep | `tools/arc_recall_eval.py` (main) | `--weights name=path` (repeatable) | `--set-root` (`SET_INFO.json` subjects) | none |
| real spin | `tools/case134_sweep.py score` | `--weights name=path` | `realxray/carmlspine_sweep` | none (contamination text hand-written) |
| level naming | `tools/level_prototype.py` (main) | `--detector`, `--model`, `--head`, else registry aliases `detector_v5z_final` / `allspine_v2_r1` | `--image <dir>` (+ `--boxes-dir` for oracle) | none (`model_registry.resolve` is a resolver) |
| film naming | `tools/head_mixed_length.py`; `tools/rigor_fixes.py a5-rows` | `--model` (+ trained head) | the bank's `split == "val"` films | own train/val read; no gate |
| render vs film | `tools/rigor_fixes.py a3a-rows` | `--det-render`, `--det-film` | `--drr ~/films_drr_buucorr` (first 25 spines) | `holdout.trained_on(--holdout-bank allspine_v7)`, the level bank rather than the detector's lists |
| device cards | `tools/device_fit.py` | the nine-term fit per fold | the held group | leave-one-group-out by device `group` |
| scorers over dumps | `lcurve_score`, `or_lodo_rescore_outline`, `fig3_detection_grid`, `count_from_sacrum_eval`, `alphabet_couple`, `carmlspine_eval`, `SchwingNet/tools/{contribution_matrix,counting_report,coupling_report}`, `rigor_fixes a1/a3/a4/a7/a9` | read from the dump (`weights`) or not at all | the dump's frames | none |
| body-box rescore | `or_ready/bodybox_rescore/bin/bodybox_rescore.sh` (grid only, not in the repo) | sweep / lcurve / devcorpus dumps | COBRA test with SPINEPS body truth | none; its SPINEPS masks belong to the `results/spineps_ids/` audit |

### 3.2 Every scanned script

Scanned statically: `tools/*eval*.py`, `SchwingNet/tools/*.py`, and every script named in the task. The "gate today"
column comes from the source text:

- `holdout.trained_on`: the script calls it;
- `reads split == 'train' itself`: the source compares a split with `"train"`. That is a split read, and it is a
  gate only if the script refuses on it;
- `patient_keys` / `leak_check`: the script references the tool;
- `model_registry.resolve`: a resolver, not a gate.

<!-- BEGIN:GENERATED scripts -->
| script | entry point | on the path of a quoted number | checkpoint in | evaluation set in | loads weights | gate today |
|---|---|---|---|---|---|---|
| `SchwingNet/tools/alphabet_loss_report.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --bank | - | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `SchwingNet/tools/bank_index.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --ctx | - | reads split == 'train' itself (a split read; a gate only if it refuses); patient_keys |
| `SchwingNet/tools/check_claim_checklist.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/check_limits.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/cobra_r2_strat.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/cobra_window_tables.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/contribution_matrix.py` | main | re-scores every arm's raw dump; the DEVICE-HELD-OUT status is a hand table (LODO_ARMS) | - | - | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `SchwingNet/tools/counting_check_hand.py` | main | verifier of chosen counting frames (no checkpoint) | --dump | --meta | - | none |
| `SchwingNet/tools/counting_check_synthetic.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/counting_outside_check.py` | main | verifier of the counting cells from the raw dumps (no checkpoint) | --dump | --meta --set | - | none |
| `SchwingNet/tools/counting_report.py` | main | collects count_from_sacrum_eval outputs (no checkpoint) | - | - | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `SchwingNet/tools/coupling_check_dedupe.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/coupling_check_split.py` | main | verifier: reads the level bank split for the alphabet-loss spines (patient_keys) | - | --ctx --subjects | - | reads split == 'train' itself (a split read; a gate only if it refuses); patient_keys |
| `SchwingNet/tools/coupling_report.py` | main | collects alphabet_couple outputs; tau set on the other folds (no checkpoint) | - | --folds --root | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `SchwingNet/tools/fig2_flow.py` | main | draws the flow of cases (counts; no checkpoint) | - | - | - | none |
| `SchwingNet/tools/fig3_naming.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/fig4_detection.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/fig4_pairs_pull.py` | main | Figure 4a pairs: R^2 under the card's fold MEDIANS (in-sample for the pair's group) | - | --cobra-meta | - | eval_gate.assert_unseen (mandatory, before scoring) |
| `SchwingNet/tools/fig4_pixium_blob_diag.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/fig5_contribution.py` | main | draws Figure S2 from contribution_matrix.json (no checkpoint) | - | - | - | none |
| `SchwingNet/tools/fig6_bank_check.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --bank | - | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `SchwingNet/tools/fig6_detector_lineage.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --split | - | none |
| `SchwingNet/tools/fig6_freeze.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --cobra-lstv --split | - | patient_keys |
| `SchwingNet/tools/fig6_manifest.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --detector --encoder --head-tag --heads-dir | --bank | - | none |
| `SchwingNet/tools/fig6_score.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --sets | - | none |
| `SchwingNet/tools/fig6_sets.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --carm --cobra --sets | - | patient_keys |
| `SchwingNet/tools/figS_supplement.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/fig_claim.py` | main | draws Figure 6 and writes power_table.json (arithmetic; no checkpoint) | - | - | - | none |
| `SchwingNet/tools/fig_detection.py` | main | draws Figure 3 from the scored files | - | - | - | none |
| `SchwingNet/tools/fig_detection_numbers.py` | main | rewrites NUMBERS.md's Figure 3 section from fig3_detection.numbers.json (no checkpoint) | - | - | - | none |
| `SchwingNet/tools/fig_formation.py` | main | draws Figure 4 from device cards, fig4_pairs and the manifold | - | - | - | none |
| `SchwingNet/tools/fig_manifold.py` | main | ImageNet ResNet-50 features + LOSO SVM | - | - | - | none |
| `SchwingNet/tools/fig_naming.py` | main | draws Figure 5 from a4/a9/counting/coupling | - | - | - | none |
| `SchwingNet/tools/fig_power.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure1.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure2.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure2_analyse.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | patient_keys |
| `SchwingNet/tools/figure2_transitional.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure3_network.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure4_frame.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/figure_set.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/gen_claim_checklist.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | patient_keys |
| `SchwingNet/tools/make_lists_eqcount.py` | main | builds the TRAINING lists of the eq238 arm (an input to a scored checkpoint, not an evaluator) | - | - | - | none |
| `SchwingNet/tools/make_packet.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/make_refs.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/make_supp_device_table.py` | main | writes Table S1 from docs/devices/*.json (fold medians and held-out R^2; no checkpoint) | - | - | - | none |
| `SchwingNet/tools/patch_atlas_cards.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/patch_claim_checklist.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/patch_claim_verdicts.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/render_pdf.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/stats_review_recompute.py` | main | independent recomputation of quoted quantities from result files (no checkpoint) | - | - | - | none |
| `SchwingNet/tools/sweep_variant_calls.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --root | - | none |
| `SchwingNet/tools/tables_check.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `SchwingNet/tools/write_figures_md.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/alphabet_couple.py` | main | couples classifier posteriors with the count (no checkpoint) | --pred | --meta | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/arc_angle_set.py` | main | builds the angle-sweep set from STYLE_INFO val subjects (the 17 selection subjects) | --gate-weights | --subjects-file | - | eval_gate.assert_unseen (mandatory, before scoring) |
| `tools/arc_recall_eval.py` | main | LOADS every --weights and scores the angle-sweep set (the leak that started this) | --weights | --set-root | YOLO( | eval_gate.assert_unseen (mandatory, before scoring) |
| `tools/carmlspine_eval.py` | main | scores prototype outputs against the projected CBCT labels (no checkpoint) | --pred | --data --meta | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/carmlspine_pool_scores.py` | main | pools carmlspine_eval scores over splits (no checkpoint) | - | --root --splits | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/case134_sweep.py` | main | LOADS every --weights and scores the case134 spin; its contamination text is hand-written | --weights | - | YOLO( | eval_gate.assert_unseen (mandatory, before scoring) |
| `tools/common_testset_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --banks | load_level_model( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/corpus_manifold.py` | main | image-statistics features and the leave-one-corpus-out classifier (a2) | - | - | - | none |
| `tools/corpus_xray_gate_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --root | load_level_model( | none |
| `tools/count_from_sacrum_eval.py` | main | counting from a detector dump (no checkpoint) | --dump | --meta --set | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/detector_failures.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --detector | --drr --holdout-bank | YOLO( | holdout.trained_on |
| `tools/detector_quality.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --detector | --drr --holdout-bank | YOLO( | holdout.trained_on |
| `tools/devcorpus_train.py` | main | trains a dc_* arm and scores it with realxray_eval on every device's test split; status label DEVICE-HELD-OUT is hand-derived from the design, not from lineage | --init | - | YOLO( | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/device_fit.py` | main | fits the nine-term card leave-one-group-out and scores the held group | - | --cases | - | eval_gate.assert_unseen (mandatory, before scoring); leak_check |
| `tools/dr_eval_report.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/ensemble_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/eval_anchor_free.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | --ctx | load_level_model( load_state_dict( torch.load( | none |
| `tools/eval_anomaly_rule.py` | main (masks, eval) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --root | - | none |
| `tools/eval_calibration.py` | main (level, detector, report, selftest) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/eval_ensemble_test.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --predictions_dir | - | - | none |
| `tools/eval_ensemble_test_sep_hips.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --predictions_dir | - | - | none |
| `tools/eval_error_taxonomy.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --images --meta | - | none |
| `tools/eval_feasibility_claims.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | --ctx | load_level_model( load_state_dict( torch.load( | none |
| `tools/eval_fov_separability.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --drr | load_level_model( | none |
| `tools/eval_full.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --predictions_dir | - | - | none |
| `tools/eval_gate.py` | main (check, eval-sets) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --ckpt | --image-dir --set-info --split | - | eval_gate.assert_unseen (mandatory, before scoring); reads split == 'train' itself (a split read; a gate only if it refuses); patient_keys; leak_check |
| `tools/eval_global_anomaly_signature.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --drr | load_level_model( | none |
| `tools/eval_interior_windows.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | --ctx | load_level_model( load_state_dict( torch.load( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/eval_level_flags.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --bank --drr | load_level_model( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/eval_multiview.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | - | - | none |
| `tools/eval_oneshot.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --predictions_dir | --dataset_json | - | none |
| `tools/eval_raw_films.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --bank | load_level_model( | none |
| `tools/eval_runtime_cost.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --detector --head --model | - | YOLO( load_state_dict( torch.load( | none |
| `tools/eval_scaling_curves.py` | main (devices, cases, fewshot-lists, fewshot, figure, selftest) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --ctx --metas | load_level_model( | reads split == 'train' itself (a split read; a gate only if it refuses); patient_keys |
| `tools/eval_shortcut_controls.py` | main (anatomy, scale, permute, order, anchor, chain, dupes, report, selftest) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --bs-head --head --model --weights | --ctx --drr --splits | YOLO( load_level_model( load_state_dict( torch.load( | reads split == 'train' itself (a split read; a gate only if it refuses); patient_keys; leak_check |
| `tools/eval_subgroups.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --predictions_csv | --splits_file | - | none |
| `tools/eval_surgeon_benefit.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --drr | load_level_model( | none |
| `tools/eval_transitional.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | --bank --drr | load_level_model( load_state_dict( torch.load( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/eval_transitional_detectors.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | - | load_level_model( | none |
| `tools/eval_windows_by_class.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --head --model | --ctx | load_level_model( load_state_dict( torch.load( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/eval_xrsp1k_seg.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --pred | - | - | none |
| `tools/fiducial_walk.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --detector --head --model | --cases --drr --holdout-bank | YOLO( | holdout.trained_on |
| `tools/fig3_detection_grid.py` | main | re-scores sweep dumps for Figure 3 with lcurve_score (no checkpoint) | - | - | - | none |
| `tools/fluorocap_ablation_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --ctx | load_level_model( | none |
| `tools/head_mixed_length.py` | main | LOADS an encoder, trains a head on the bank's train films and scores the bank's VAL films (the encoder's selection set) | --init-head --model | --ctx | load_level_model( load_state_dict( torch.load( | eval_gate.assert_unseen (mandatory, before scoring); reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/lcurve_report.py` | main | assembles lcurve.json from scored dumps; the all-real descriptions are hand text | - | - | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/lcurve_score.py` | main | scores one dump (no checkpoint) | --dump | --meta-dirs | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/lcurve_train.py` | main | fine-tunes lc_* from the dc_B parent and scores it with realxray_eval | --init | - | YOLO( | none |
| `tools/learning_embed.py` | main | LOADS an encoder and reads the bank's VAL crops as 'held-out' | --model | --bank --carm --cobra --cobra-per-case | load_level_model( | eval_gate.assert_unseen (mandatory, before scoring); patient_keys |
| `tools/level_prototype.py` | main | LOADS detector + encoder + head (defaults resolved through the registry) and names every vertebra in --image; writes prototype_meta.json with both sha256 | --box-detector --detector --head --model --sacrum-detector | --image | YOLO( load_level_model( load_state_dict( torch.load( | eval_gate.assert_unseen (mandatory, before scoring); model_registry.resolve (a resolver, not a gate) |
| `tools/lstv_eval_physics.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/lstv_eval_prep.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --bank --root | - | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/lstv_eval_probe.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/lstv_eval_score.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --root | - | none |
| `tools/lstv_flag_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | - | - | none |
| `tools/lumbar_combine_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | - | --bank | - | none |
| `tools/needle_confirm.py` | main | not on the path of a quoted number; takes --holdout-bank (required) and NEVER reads it, and --allow-trained-on defaults to True | - | --drr --holdout-bank | - | none |
| `tools/night_eval_realpanels.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --model | --holdout-frac --holdout-only --root | load_level_model( | none |
| `tools/or_crossdev_score.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --pred | --splits | - | none |
| `tools/or_lodo_rescore_outline.py` | main | re-scores the sweep dumps under the outline convention (no checkpoint) | - | --meta-dirs --root --sets | - | eval_gate.carry (the input's verdict carried or gated at scoring) |
| `tools/or_recall_curves.py` | main | sweep: runs realxray_eval for every arm in its hand DETECTORS table x every set; the table carries trained_on / selected_on_test as LABELS only | --det | --root | - | eval_gate.carry (the input's verdict carried or gated at scoring); reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/polypose_eval_ours.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --models | --subjects | - | none |
| `tools/realxray_eval.py` | main | LOADS a YOLO checkpoint (--weights) and scores --data/--split; writes the dump every detector number is re-scored from (records weights path, data, split) | --dump-raw --weights | --data --split | YOLO( | eval_gate.assert_unseen (mandatory, before scoring) |
| `tools/realxray_robustness.py` | main (prior, run, plot) | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --weights | --data --datasets --root --split | YOLO( | reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/rigor_fixes.py` | main | a3a-rows and a5-rows LOAD checkpoints; a1/a3/a4/a7/a9 are statistics over dumps; a3a-rows is the only evaluator that calls holdout.trained_on, and it checks the level bank allspine_v7, not the detector's own train list | --det-film --det-render --head --model | --ctx --drr --holdout-bank | YOLO( load_level_model( load_state_dict( torch.load( | eval_gate.assert_unseen (mandatory, before scoring); eval_gate.carry (the input's verdict carried or gated at scoring); holdout.trained_on; reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/robustness_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --dump --model | --ctx | load_state_dict( torch.load( | none |
| `tools/sweep_map.py` | main | LOADS encoder/head/detector; its --holdout-bank read is now holdout.trained_on (train + val, since 2026-09-23); not on a quoted path | --detector --head --model --role-head | --cases --drr --fold --holdout-bank | YOLO( load_level_model( load_state_dict( torch.load( | holdout.trained_on; reads split == 'train' itself (a split read; a gate only if it refuses) |
| `tools/thoracic_xr_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --det | --data | YOLO( | none |
| `tools/validate_guided.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --anchor-detector --detector --head --model | --drr --holdout-bank | YOLO( | holdout.trained_on |
| `tools/wholespine_eval.py` | main | not on the path of a quoted number (no NUMBERS.md / tables / rescore.json row reads its output) | --weights | --set | YOLO( | none |
<!-- END:GENERATED scripts -->

---

## 4. The quoted results

**Row sources:**

- every table row of `SchwingNet/NUMBERS.md`;
- the rows of `SchwingNet/CLAIMS_LEDGER.md` that carry a number of ours;
- the 69 rows of `results/bodybox_rescore/rescore.json`;
- the 84 entries of `figures/fig3_detection.numbers.json`;
- `figures/fig4_formation.record.json` and `figures/fig_manifold.record.json`.

**How each row is mapped.** Each row maps to a family: an evaluator chain plus an output file. It also maps to one or
more (checkpoint, evaluation set) pairs, found from the file the row cites and from its own words, using the rules
in `build_inventory.classify`.

**Limitation of the mapping.** For contribution-matrix rows, the pairs come from the arm names and dataset words in
the row, not from reading each cell. `quoted_results.json` lists the pairs on every row so the mapping can be
checked.

### 4.1 Counts by verdict

<!-- BEGIN:GENERATED counts -->
| source | rows | HELD OUT | NOT HELD OUT | MIXED | NOT ESTABLISHED | N/A |
|---|---:|---:|---:|---:|---:|---:|
| NUMBERS | 234 | 137 | 20 | 13 | 0 | 64 |
| CLAIMS | 9 | 3 | 2 | 1 | 0 | 3 |
| FIG3 | 84 | 82 | 1 | 0 | 0 | 1 |
| FIG4REC | 7 | 0 | 5 | 0 | 0 | 2 |
| MANIFOLDREC | 3 | 0 | 0 | 0 | 0 | 3 |
| FIGREC | 157 | 96 | 27 | 5 | 1 | 28 |
| RESCORE | 69 | 62 | 5 | 2 | 0 | 0 |
| **all** | **563** | 380 | 60 | 21 | 1 | 101 |
<!-- END:GENERATED counts -->

### 4.2 Every row that is not a clean HELD OUT

<!-- BEGIN:GENERATED not_held_out -->
| row | quoted (truncated) | why |
|---|---|---|
| `NUMBERS:L39` | nearest other-person crop same level 74.9 % [72.2, 77.6], within one 93.8 % [92.7, 94.9] (Results) / `results/figure2/figure2_metrics.json#nearest_other_person` (`same_le | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L40` | silhouette L6 vs L5 0.349 [0.310, 0.386] (98 crops, 10 persons); L5 vs L4 0.227 [0.205, 0.249] (721 persons); lumbar pairs 0.159-0.227 (L3/L2 0.159, L4/L3 0.170, L2/L1 0. | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L41` | within one render source the L6/L5 order reversed in physics_drr: 0.140 [0.107, 0.200] (5 persons) against L5/L4 0.208; held in physics_rare (0.243 vs 0.157) and verse_dr | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L42` | classifier named 75 of 98 validation L6 crops L6 (0.765) (Results) / `results/figure2/figure2_metrics.json#validation_neighbours_and_calls/L6/called_own` × n 98 | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L45` | occlusion enrichment, ten clean lateral crops per level: sacrum target 4.513 [3.421, 5.788]; L4 below 1.291 [1.126, 1.440]; L5 below 1.261 [1.090, 1.453] (Results) / `res | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L48` | LevelCheck comparator: model r(1 − e), r = 1.0 (published 0.993-1.000); H1 at risk pooled 82.2 % (Peh 1999), n_min 19; H2 97.6 % (Manbachi 2018), 152; H3-H5 82.2 %, 19; H | NOT HELD OUT: allspine_v9_encoder on v9_val: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `NUMBERS:L89` | CSXA 99.8 % = 3,629/3,635, 727 patients (3 with an error); [99.6, 100.0]; BCa [99.5, 99.9] / `results/a5.json#per_protocol/random/csxa/patient_clustered` | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L90` | BUU-LSPINE 97.3 % = 2,671/2,744, 549 patients (51); [96.5, 98.0]; BCa [96.4, 98.0] / `results/a5.json#per_protocol/random/buu_full/patient_clustered` | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L91` | NHANES II 99.1 % = 441/445, 52 patients / 76 films (4); [98.2, 99.8]; BCa [98.0, 99.8] / `results/a5.json#per_protocol/random/nhanes/patient_clustered` | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L92` | leak check: 0 validation patients in training for csxa, buu_full, nhanes (v8 bank) / `results/a5.json#leak_check_by_patient_key`; `results/RIGOR_FIXES.md` A5 | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L93` | render-trained vs film-trained detector on 233 bodies / 25 spines, conf 0.05: 71.67 % vs 99.14 %; +27.5 pp [20.5, 35.2], BCa [20.9, 35.6]; sign test 23 vs 0; 196 of 233 b | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `NUMBERS:L108` | Holm over the four comparisons named before adjustment (the family was named by the analysis audit after the data were seen; REVIEW_STATS F16): exact/cluster p 2.5e-23, 2 | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `NUMBERS:L114` | mean gain over 24 folds +0.0376 [0.0205, 0.0573], BCa [0.0219, 0.0606]; 4 of 24 negative; sign-flip p 2.0e-4 (Holm 4.0e-4) / `results/a3.json#comparisons/card_vs_uncalibr | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L115` | BV Pulsera +0.0417 [0.0348, 0.0528], BCa [0.0354, 0.0574], 0/6 negative; 40 of 116 frames fitted / `results/a6.json#per_device/bv_pulsera`; `docs/devices/bv_pulsera.json` | NOT HELD OUT: bv_pulsera: folds by view (ONE Geneva phantom, 19 poses) |
| `NUMBERS:L118` | PIXIUM 4600 +0.0703 [0.0063, 0.1312], BCa [0.0018, 0.1243], 2/6 negative, two folds hold one frame; 14 of 18 / `results/a6.json#per_device/pixium_4600`; `docs/devices/pix | NOT HELD OUT: pixium_4600: folds by frame by pose id (ONE Ljubljana cadaver, 18 radiographs) |
| `NUMBERS:L119` | criterion C3 (every device's gain > 0 with the interval excluding 0) holds only on the six-fold percentile bootstrap; fails on BCa for Cios Fusion; on six-fold t interval | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L120` | card gain, inference at the device level: 24 folds nested in 4 devices; frame-weighted mean 0.025 (835 frames), median 0.034; all four device means positive (BV Pulsera 0 | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L121` | held-out R² medians, card vs uncalibrated physics: Cios 0.905 vs 0.899; Pulsera 0.952 vs 0.917; Elekta 0.974 vs 0.964; PIXIUM 0.679 vs 0.650 / `docs/devices/{cios_fusion, | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L167` | Table 1, every cell: modality and device, role, distinct subjects and split unit, frames or renders, truth source, released column, footnotes a-k / `tables/tab_corpus.sou | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L219` | CSXA 99.8 % Wilson on n_eff [99.5, 99.9]; NHANES II 99.1 % Wilson on n_eff [97.8, 99.6] / Table 3 / `results/a5.json#per_protocol/random/{csxa,nhanes}/patient_clustered/w | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L223` | same-device minus held-out sacrum at 0.25: +14.3 pp [5.4, 23.2], $P=.008$ (sign test 8 vs 0, p 0.0078, Holm 0.0078) / Results / `results/a3.json#primary_with_holm`; `reco | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `NUMBERS:L224` | film- minus render-trained detector at 0.05: +27.5 pp [20.5, 35.2], $P<.001$ (23 vs 0 spines, Holm 7.2e-7); in-sample for 196 of 233 bodies / Results, Table 2 footnote f  | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `NUMBERS:L225` | card gain: frame-weighted 0.025; over folds $P<.001$; four of four device means positive, $P=.13$ (exact 0.125); Cios Fusion six-fold t interval (−0.003, 0.034) / abstrac | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L228` | films at three bodies: BUU-LSPINE 95.0 % (2,606/2,744), CSXA 99.6 % (3,622/3,635), NHANES II 94.6 % (421/445); printed as 94.6–99.6 % / Results, Table 3 footnote f / `res | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `NUMBERS:L241` | (a) frame choice: the calibration pair whose $R^2$ under the card's fitted medians (per-frame linear display match, fit mask) is nearest the device's median over all its  | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `NUMBERS:L242` | (a) BV Pulsera: pair p02 / 071kv, $R^2$ 0.964 (device median 0.964 over 116 pairs), 0.781 mm per pixel, water-equivalent thickness 13.8 cm, not stored inverted / `results | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `NUMBERS:L243` | (a) Cios Fusion: pair 18-0725 / 013, $R^2$ 0.888 (median 0.888 over 366), 0.776 mm per pixel, 18.4 cm, lateral angle −0.1° / `results/fig4_pairs/fig4_pairs.json#devices/c | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `NUMBERS:L244` | (a) Elekta XVI: pair A004 / 0264 (AP, 6.2° off axis, 120 kVp, half-fan), $R^2$ 0.979 (median 0.979 over 335), 0.8 mm per pixel, 21.9 cm / `results/fig4_pairs/fig4_pairs.j | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `NUMBERS:L245` | (a) PIXIUM 4600: pair LJ-L1L5 / 001, $R^2$ 0.655 (median 0.635 over 18), 0.858 mm per pixel, 5.8 cm / `results/fig4_pairs/fig4_pairs.json#devices/pixium_4600` | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `NUMBERS:L272` | Table 1, device parameters: frames fitted / total and median held-out R² card vs physics: Cios Fusion 40 / 366, 0.905 vs 0.899; Elekta XVI 40 / 335, 0.974 vs 0.964; BV Pu | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `NUMBERS:L276` | Table 2, plain radiographs: render-trained 71.7 % (167/233) at 0.05 and 43.3 % (101/233) at 0.25; film-trained 99.1 % (231/233) and 98.7 % (230/233); paired difference at | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `NUMBERS:L358` | c / real film: film-trained detector (in-sample), 233 bodies / 25 spines, conf 0.05 / 99.14 % / no case interval (one cluster) / `results/a3.json#comparisons/render_vs_fi | NOT HELD OUT: detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 printed before was counted against the a |
| `NUMBERS:L375` | Table S1, every fitted-term median, fold minimum-maximum, unit, bound, frames fitted / total and held-out R-squared per device / generated verbatim by `tools/make_supp_de | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `CLAIMS:L108` | BV Pulsera / +0.0417 [0.0348, 0.0528] / 40 of 116 / 0 of 6 folds negative | NOT HELD OUT: bv_pulsera: folds by view (ONE Geneva phantom, 19 poses) |
| `CLAIMS:L109` | Cios Fusion / +0.0153 [0.0029, 0.0274] / 40 of 366 / **fails the pre-stated criterion on the BCa interval** ([−0.0005, 0.0269]) and on the six-fold t interval ([−0.003, 0 | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `CLAIMS:L111` | PIXIUM 4600 / +0.0703 [0.0063, 0.1312] / 14 of 18 / two folds hold one frame | NOT HELD OUT: pixium_4600: folds by frame by pose id (ONE Ljubljana cadaver, 18 radiographs) |
| `FIG3:075` | real film: film-trained detector (in-sample), 233 bodies / 25 spines, conf 0.05: 99.14 % None | NOT HELD OUT: detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 printed before was counted against the a |
| `FIG4REC:panel_a/bv_pulsera` | bv_pulsera: pair p20/085kv, R2 0.973247735547385 (device median 0.9732045801994922) | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIG4REC:panel_a/cios_fusion` | cios_fusion: pair 18-0725/013, R2 0.8882111225573952 (device median 0.8884212479108157) | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIG4REC:panel_a/elekta_xvi` | elekta_xvi: pair C005/0136, R2 0.9749808808717764 (device median 0.9757061939213917) | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIG4REC:panel_a/pixium_4600` | pixium_4600: pair LJ-L1L5/001, R2 0.6553982015567879 (device median 0.6348178925850393) | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIG4REC:panel_d` | PENDING G4 (results/arc present, kept pending by --d-pending: under ARC_CHECK, not yet adopted) | NOT HELD OUT: dc_P_pooled on arc17: NOT HELD OUT (['ts:s0585', 'ts:s0970', 'ts:s1045', 'ts:s1062', 'ts:s1159', 'ts:s1384', 'ts:s1535', 'ts:s1579', 'ts:s1700', 'ts:s1836', 'ts:s1842', 'ts:s1872', 'ts:s1880', 'ts:s1883', 'ts:s1902', 'ts:s2033', 'ts:s2053', 'ts:val17'] in the  |
| `FIGREC:figure2/02` | window (t-SNE units): box of validation L6 and sacrum (2nd-98th percentile) and never-seen L6 (10th-90th), padded 6 % -- {"lo": [-34.58, -28.91], "hi": [26.83, 28.53]} | MIXED: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder); allspine_v9_encoder on carm_l6_never_seen: HELD OUT |
| `FIGREC:figure2/03` | share of never-seen L6 crops inside the window -- 0.9 | MIXED: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder); allspine_v9_encoder on carm_l6_never_seen: HELD OUT |
| `FIGREC:figure2/04` | direct labels [level, map x, map y, validation points of that level inside the window] -- [["L5", 15.77, 14.84, 408], ["L6", 5.15, 22.35, 98], ["sacrum", 22.97, 1.81, 65] | MIXED: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder); allspine_v9_encoder on carm_l6_never_seen: HELD OUT |
| `FIGREC:figure2/07` | silhouette L6/L5, validation split: mean, 95 % person-cluster interval, crops, people -- [0.3491, [0.3096, 0.3865], 98, 10] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/09` | silhouette L5/L4, validation split: mean, 95 % person-cluster interval, crops, people -- [0.2272, [0.2052, 0.2485], 1012, 721] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/11` | silhouette L4/L3, validation split: mean, 95 % person-cluster interval, crops, people -- [0.1698, [0.156, 0.1836], 1073, 733] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/13` | silhouette L3/L2, validation split: mean, 95 % person-cluster interval, crops, people -- [0.1587, [0.1464, 0.1716], 1085, 733] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/15` | silhouette L2/L1, validation split: mean, 95 % person-cluster interval, crops, people -- [0.194, [0.1773, 0.2107], 1036, 734] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/16` | silhouette L1/T12, validation split: mean, 95 % person-cluster interval, crops, people -- [0.3236, [0.2941, 0.3515], 1005, 743] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/17` | silhouette T12/T11, validation split: mean, 95 % person-cluster interval, crops, people -- [0.1437, [0.1175, 0.1653], 422, 196] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/20` | L4: occlusion subjects (crops, distinct people, sources, named right) -- [10, 10, ["ctsp_drr"], 1.0] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/21` | L5: occlusion subjects (crops, distinct people, sources, named right) -- [10, 10, ["ctsp_drr"], 0.9] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/22` | L6: occlusion subjects (crops, distinct people, sources, named right) -- [10, 10, ["verse_drr"], 0.8] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/23` | sacrum: occlusion subjects (crops, distinct people, sources, named right) -- [10, 10, ["ctsp_drr"], 1.0] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/24` | L4 occlusion enrichment, above: mean, 95 % interval over the ten crops -- [0.618, [0.555, 0.695]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/25` | L4 occlusion enrichment, target: mean, 95 % interval over the ten crops -- [1.689, [1.445, 1.967]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/26` | L4 occlusion enrichment, below: mean, 95 % interval over the ten crops -- [1.291, [1.126, 1.44]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/27` | L5 occlusion enrichment, above: mean, 95 % interval over the ten crops -- [0.756, [0.642, 0.882]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/28` | L5 occlusion enrichment, target: mean, 95 % interval over the ten crops -- [1.391, [1.149, 1.626]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/29` | L5 occlusion enrichment, below: mean, 95 % interval over the ten crops -- [1.261, [1.09, 1.453]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/30` | L6 occlusion enrichment, above: mean, 95 % interval over the ten crops -- [0.748, [0.6, 0.899]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/31` | L6 occlusion enrichment, target: mean, 95 % interval over the ten crops -- [1.473, [1.191, 1.761]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/32` | L6 occlusion enrichment, below: mean, 95 % interval over the ten crops -- [1.082, [0.878, 1.27]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/33` | sacrum occlusion enrichment, above: mean, 95 % interval over the ten crops -- [1.048, [0.807, 1.297]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/34` | sacrum occlusion enrichment, target: mean, 95 % interval over the ten crops -- [4.513, [3.421, 5.788]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figure2/35` | sacrum occlusion enrichment, below: mean, 95 % interval over the ten crops -- [0.315, [0.221, 0.404]] | NOT HELD OUT: allspine_v9_encoder on v9_val_clean: NOT HELD OUT (['v9:val'] in the VAL/selection set of allspine_v9_encoder) |
| `FIGREC:figS2/00` | BV Pulsera: body-region R² of the shown pair; device median over its pairs; pairs; mm per pixel (bar = 50 mm at the detector) -- [0.973247735547385, 0.9732045801994922, 1 | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIGREC:figS2/01` | Cios Fusion: body-region R² of the shown pair; device median over its pairs; pairs; mm per pixel (bar = 50 mm at the detector) -- [0.8882111225573952, 0.8884212479108157, | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIGREC:figS2/02` | Elekta XVI: body-region R² of the shown pair; device median over its pairs; pairs; mm per pixel (bar = 50 mm at the detector) -- [0.9749808808717764, 0.9757061939213917,  | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIGREC:figS2/03` | PIXIUM 4600: body-region R² of the shown pair; device median over its pairs; pairs; mm per pixel (bar = 50 mm at the detector) -- [0.6553982015567879, 0.6348178925850393, | NOT HELD OUT: the R^2 is computed under the MEDIAN of the six fold fits, five of which were fitted on the pair's own group (fig4_pairs_pull.py: th = fitted[k]['median']); illustrative, not the held-out R^2 of Table 1 |
| `FIGREC:figS2/05` | held-out R² gain of the fitted card over uncalibrated physics, per fold (24 folds in four devices); device mean with six-fold t interval -- {"bv_pulsera": {"fold_gains":  | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `FIGREC:figS2/06` | pooled: mean gain over 24 folds [percentile], negative folds, exact sign-flip p over folds, over the four device means -- {"mean": 0.03764601426198082, "percentile": [0.0 | MIXED: leave-one-group-out folds: patient-held-out for cios_fusion (specimen) and elekta_xvi (case); NOT patient-held-out for bv_pulsera (one phantom, folds by view) and pixium_4600 (one cadaver, folds by frame) -- a pooled 24-fold number mixes both; a single-device  |
| `FIGREC:figS2/07` | refit gate per device: held-out R² and image-statistic distance under the refit's own noisy, statistic-aware evaluation, published card vs free and constrained refit; fra | NOT ESTABLISHED: card_refit writes n_train / n_held only, not which frames (or subjects) were fitted and which held out; the 'published' row is the released card, whose fold fits cover every group of the device, so its R^2 on these frames is not subject-held-out either |
| `RESCORE:B3_0.05` | B3_0.05 B a3 paired comparisons: film-trained vs render-trained detector on 233 film bodies at 0.05; WV None (None/None) None; BODY 27.5 (None/233) [20.5, 35.2] | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `RESCORE:B3_0.25` | B3_0.25 B a3 paired comparisons: film-trained vs render-trained detector on 233 film bodies at 0.25; WV None (None/None) None; BODY 55.4 (None/233) [47.0, 63.6] | MIXED: anchor_det_v1 on nhanes25: HELD OUT; detector_v5z_final on nhanes25: NOT HELD OUT (in-sample: 24 of the 25 spines (225 of 233 bodies) are in the film detector's own train (22) or val (2) directories and those of its parent detect_v3 (touched.json); the 196 pri |
| `RESCORE:C_cobra_ar_C-ArmLSpine_held_out_0.74` | C_cobra_ar_C-ArmLSpine_held_out_0.74 C learning curve, COBRA Elekta: COBRA all-real control 'C-ArmLSpine held out': vertebra recall at 0.74; WV 91.2 (814/893) [83.4, 96.3 | NOT HELD OUT: rx_lodo_carmlspine_1024 on cobra_test: NOT HELD OUT (['cobra:test'] in the VAL/selection set of rx_lodo_carmlspine_1024) |
| `RESCORE:C_cobra_ar_C-ArmLSpine_held_out_0.25` | C_cobra_ar_C-ArmLSpine_held_out_0.25 C learning curve, COBRA Elekta: COBRA all-real control 'C-ArmLSpine held out': vertebra recall at 0.25; WV 97.3 (869/893) [92.7, 99.7 | NOT HELD OUT: rx_lodo_carmlspine_1024 on cobra_test: NOT HELD OUT (['cobra:test'] in the VAL/selection set of rx_lodo_carmlspine_1024) |
| `RESCORE:I_CSXA` | I_CSXA I plain-film naming: CSXA exact naming; WV None (None/None) None; BODY 99.8 (3629/3635) [99.6, 100.0] | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `RESCORE:I_BUU` | I_BUU I plain-film naming: BUU exact naming; WV None (None/None) None; BODY 97.3 (2671/2744) [96.5, 98.0] | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
| `RESCORE:I_NHANES` | I_NHANES I plain-film naming: NHANES II exact naming; WV None (None/None) None; BODY 99.1 (441/445) [98.2, 99.8] | NOT HELD OUT: allspine_v8_encoder on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder); allspine_v8_head_seed0 on v8_val: NOT HELD OUT (['v8:val'] in the VAL/selection set of allspine_v8_encoder (ancestor)) |
<!-- END:GENERATED not_held_out -->

### 4.3 Pose-donor overlap on quoted rows

<!-- BEGIN:GENERATED pose_donor -->
| checkpoint | evaluation set | pose-donor renders in the checkpoint's train+val (or an ancestor's) | rows |
|---|---|---|---:|
| anchor_none_v2_17-1882 | df_test | 294 renders in anchor_none_v2_17-1882 train+val carry the pose of df:18-1109 | 12 |
| dc_A_held_cios_fusion | df_all6 | 1756 renders in dc_A_held_cios_fusion train+val carry the pose of df:18-1109 | 8 |
| dc_A_held_cios_fusion | df_test | 1756 renders in dc_A_held_cios_fusion train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_cios_fusion_1dev_elekta_xvi | df_all6 | 878 renders in dc_A_held_cios_fusion_1dev_elekta_xvi train+val carry the pose of df:18-1109 | 6 |
| dc_A_held_cios_fusion_1dev_elekta_xvi | df_test | 878 renders in dc_A_held_cios_fusion_1dev_elekta_xvi train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_cios_fusion_1dev_surgio_b51_dr | df_all6 | 878 renders in dc_A_held_cios_fusion_1dev_surgio_b51_dr train+val carry the pose of df:18-1109 | 7 |
| dc_A_held_cios_fusion_1dev_surgio_b51_dr | df_test | 878 renders in dc_A_held_cios_fusion_1dev_surgio_b51_dr train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_cios_fusion_s1 | df_all6 | 1756 renders in dc_A_held_cios_fusion_s1 train+val carry the pose of df:18-1109 | 7 |
| dc_A_held_cios_fusion_s1 | df_test | 1756 renders in dc_A_held_cios_fusion_s1 train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_elekta_xvi_1dev_surgio_b51_dr | df_all6 | 878 renders in dc_A_held_elekta_xvi_1dev_surgio_b51_dr train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_elekta_xvi_1dev_surgio_b51_dr | df_test | 878 renders in dc_A_held_elekta_xvi_1dev_surgio_b51_dr train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_surgio_b51_dr_1dev_elekta_xvi | df_test | 878 renders in dc_A_held_surgio_b51_dr_1dev_elekta_xvi train+val carry the pose of df:18-1109 | 1 |
| dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238 | df_test | 878 renders in dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238 train+val carry the pose of df:18-1109 | 2 |
| dc_P_pooled | carm_test | 658 renders in dc_P_pooled train+val carry the pose of carm:test | 3 |
| dc_P_pooled | cobra_test | 412 renders in dc_P_pooled train+val carry the pose of cobra:test | 3 |
| dc_P_pooled | df_test | 2634 renders in dc_P_pooled train+val carry the pose of df:18-1109 | 1 |
| lc_cios_fusion | df_test | 762 renders in lc_cios_fusion train+val carry the pose of df:18-1109 | 6 |
| lc_elekta_xvi | cobra_test | 368 renders in lc_elekta_xvi train+val carry the pose of cobra:test | 11 |
| lc_surgio_b51_dr | carm_test | 598 renders in lc_surgio_b51_dr train+val carry the pose of carm:test | 10 |
| rx_lodo_deepfluoro_1024 | df_test | 294 renders in anchor_none_v2_17-1882 train+val carry the pose of df:18-1109 | 15 |
| rx_only_carmlspine_1024 | df_test | 294 renders in anchor_none_v2_17-1882 train+val carry the pose of df:18-1109 | 1 |
| rx_pooled_1024 | df_test | 294 renders in anchor_none_v2_17-1882 train+val carry the pose of df:18-1109 | 11 |
<!-- END:GENERATED pose_donor -->

### 4.4 Checkpoint lineage, as read

<!-- BEGIN:GENERATED lineage -->
| checkpoint | init chain (to a public root) | train | val / selection | selected how | read from |
|---|---|---|---|---|---|
| `anchor_none_v2_17-1882` | anchor_none_v2_17-1882 -> coco_yolo11m | ts:anchor_train + s0585 s0970 s1045 s1159 s1384 | ts:anchor_val + s1062 | best.pt = best fitness on images/val (ultralytics) | args.yaml (model yolo11m.pt, data model_night/anchor_none_v2_17-1882/data.yaml); image names read 2026-09-23: TotalSegmentator subjects, 14 renders each of s0585 s0970 s1045 s1159 s1384 in train and of s1062 in val; pose |
| `rx_lodo_carmlspine_1024` | rx_lodo_carmlspine_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | cobra:train, cobra:val, df:train, df:val | cobra:test, df:test | best.pt = best fitness on the COBRA and DeepFluoro TEST splits | args.yaml model = anchor_none_v2_17-1882/weights/best.pt; data.yaml train = cobra_elekta train+val, deepfluoro train+val; val = cobra_elekta test, deepfluoro test |
| `rx_lodo_cobra_elekta_1024` | rx_lodo_cobra_elekta_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | carm:train, carm:val, df:train, df:val | carm:test, df:test | best.pt = best fitness on the C-ArmLSpine and DeepFluoro TEST splits | args.yaml; data.yaml |
| `rx_lodo_deepfluoro_1024` | rx_lodo_deepfluoro_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | carm:train, carm:val, cobra:train, cobra:val | carm:test, cobra:test | best.pt = best fitness on the C-ArmLSpine and COBRA TEST splits | args.yaml; data.yaml |
| `rx_pooled_1024` | rx_pooled_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | carm:train, cobra:train, df:train | carm:val, cobra:val, df:val | best.pt = best fitness on the three val splits | args.yaml; data.yaml |
| `rx_only_carmlspine_1024` | rx_only_carmlspine_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | carm:train | carm:val | best.pt on carmlspine val | args.yaml (init anchor_none_v2_17-1882, NOT COCO as results/lcurve/lcurve.json describes it); data.yaml |
| `rx_only_carmlspine_multi_1024` | rx_only_carmlspine_multi_1024 -> anchor_none_v2_17-1882 -> coco_yolo11m | carm:train | carm:val | best.pt on carmlspine_multi val | args.yaml; data.yaml |
| `detector_v5z_final` | detector_v5z_final (root init NOT RECORDED) | films:v5z_unrecorded | films:v5z_unrecorded | not recorded | registry.jsonl (sha 797de71a..., bank ''); file written 2026-09-14 09:33, before C-ArmLSpine landed on the grid (fetch job 40409970, log closed 2026-09-21 17:44; even the archive's internal file times, 2026-09-15 16:55,  |
| `anchor_det_v1` | anchor_det_v1 (root init NOT RECORDED) | ctsp:anchor_drr | ctsp:anchor_drr | not recorded | tools/model_registry.py BACKFILL (bank ~/anchor_drr: CTSpinoPelvic1K renders); written 2026-09-14 |
| `allspine_v2_r1` | allspine_v2_r1 -> imagenet (root init NOT RECORDED) | allspine_v2:train | allspine_v2:val | best epoch on allspine_v2 val exact (train_level_classifier best_state) | registry.jsonl 2026-09-15 (sha 00e84a90...); predates C-ArmLSpine on the grid; bank deleted so its lists survive only in logs; whether ImageNet init was used is not recorded |
| `carm_cv_fold_models` | carm_cv_fold_models -> allspine_v2_r1 -> imagenet (root init NOT RECORDED) | allspine_v7:train_sample, carm:not_scored_fold | allspine_v7:sample, carm:not_scored_fold | encoder: best epoch on the fold bank's val (--val-frac 0.2 of the non-test folds' crops); head: final epoch | slurm/carmlspine_cv.sh (INIT=resolve('allspine_v2_r1'); carmlspine_to_bank --fold K excludes the scored fold; merge over allspine_v7 rung_1); atlas/model.json Limitations (7): '0 test cases in any fold's DRR, crop or mix |
| `carm_cvday_fold_models` | carm_cvday_fold_models -> allspine_v2_r1 -> imagenet (root init NOT RECORDED) | allspine_v7:train_sample, carm:not_scored_fold | carm:not_scored_fold | as the case folds | slurm/carmlspine_cv_day.sh; rigor_fixes a9 |
| `allspine_v8_encoder` | allspine_v8_encoder -> imagenet (root init NOT RECORDED) | v8:train | v8:val | best epoch of 40 on allspine_v8 VAL exact (train_level_classifier best_state) | slurm/allspine_v8_train.sh (no --init); tools/train_level_classifier.py lines 410-472 (best_state on val) |
| `allspine_v8_head_seed0` | allspine_v8_head_seed0 -> allspine_v8_encoder -> imagenet (root init NOT RECORDED) | v8:train | - | final epoch (no selection on val) | tools/head_mixed_length.py (torch.save after the last epoch) |
| `allspine_v9_encoder` | allspine_v9_encoder -> imagenet | v9:train | v9:val | best epoch on allspine_v9 VAL exact (train_level_classifier best_state); figure2_metrics.json gate_verdict_validation_split: 'NOT HELD OUT (selection split)' | results/figure2/figure2_metrics.json encoder + encoder_sha256 188f9fcb...; touched.json row (no parent, no carmlspine key in train or val) |
| `dc_P_pooled` | dc_P_pooled -> coco_yolo11m | carm:train, cobra:train, df:train, ts:train125 | carm:val, cobra:val, df:val, ts:val17 | best.pt on P_pooled/val.txt (1,752 styled renders of the 17 TotalSegmentator val subjects + 246 real val frames) | args.yaml (yolo11m.pt, 60 epochs); list files counted 2026-09-23 (0 real test frames in train or val; case134 absent: 0 lines) |
| `dc_A_held_surgio_b51_dr` | dc_A_held_surgio_b51_dr -> coco_yolo11m | cobra:train, df:train, ts:train125 | cobra:val, df:val, ts:val17 | best.pt on lists/A_held_surgio_b51_dr/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_surgio_b51_dr_s1` | dc_A_held_surgio_b51_dr_s1 -> coco_yolo11m | cobra:train, df:train, ts:train125 | cobra:val, df:val, ts:val17 | best.pt on lists/A_held_surgio_b51_dr_s1/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_surgio_b51_dr_1dev_elekta_xvi` | dc_A_held_surgio_b51_dr_1dev_elekta_xvi -> coco_yolo11m | cobra:train, ts:train125 | cobra:val, ts:val17 | best.pt on lists/A_held_surgio_b51_dr_1dev_elekta_xvi/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_surgio_b51_dr_1dev_cios_fusion` | dc_A_held_surgio_b51_dr_1dev_cios_fusion -> coco_yolo11m | df:train, ts:train125 | df:val, ts:val17 | best.pt on lists/A_held_surgio_b51_dr_1dev_cios_fusion/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_elekta_xvi` | dc_A_held_elekta_xvi -> coco_yolo11m | carm:train, df:train, ts:train125 | carm:val, df:val, ts:val17 | best.pt on lists/A_held_elekta_xvi/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_elekta_xvi_s1` | dc_A_held_elekta_xvi_s1 -> coco_yolo11m | carm:train, df:train, ts:train125 | carm:val, df:val, ts:val17 | best.pt on lists/A_held_elekta_xvi_s1/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_elekta_xvi_1dev_surgio_b51_dr` | dc_A_held_elekta_xvi_1dev_surgio_b51_dr -> coco_yolo11m | carm:train, ts:train125 | carm:val, ts:val17 | best.pt on lists/A_held_elekta_xvi_1dev_surgio_b51_dr/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_elekta_xvi_1dev_cios_fusion` | dc_A_held_elekta_xvi_1dev_cios_fusion -> coco_yolo11m | df:train, ts:train125 | df:val, ts:val17 | best.pt on lists/A_held_elekta_xvi_1dev_cios_fusion/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_cios_fusion` | dc_A_held_cios_fusion -> coco_yolo11m | carm:train, cobra:train, ts:train125 | carm:val, cobra:val, ts:val17 | best.pt on lists/A_held_cios_fusion/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_cios_fusion_s1` | dc_A_held_cios_fusion_s1 -> coco_yolo11m | carm:train, cobra:train, ts:train125 | carm:val, cobra:val, ts:val17 | best.pt on lists/A_held_cios_fusion_s1/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_cios_fusion_1dev_surgio_b51_dr` | dc_A_held_cios_fusion_1dev_surgio_b51_dr -> coco_yolo11m | carm:train, ts:train125 | carm:val, ts:val17 | best.pt on lists/A_held_cios_fusion_1dev_surgio_b51_dr/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_cios_fusion_1dev_elekta_xvi` | dc_A_held_cios_fusion_1dev_elekta_xvi -> coco_yolo11m | cobra:train, ts:train125 | cobra:val, ts:val17 | best.pt on lists/A_held_cios_fusion_1dev_elekta_xvi/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238` | dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238 -> coco_yolo11m | cobra:train, ts:train125 | cobra:val, ts:val17 | best.pt on lists/A_held_surgio_b51_dr_1dev_elekta_xvi_eq238/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_B_held_surgio_b51_dr` | dc_B_held_surgio_b51_dr -> coco_yolo11m | cobra:train, df:train, ts:train125 | cobra:val, df:val, ts:val17 | best.pt on lists/B_held_surgio_b51_dr/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_B_held_surgio_b51_dr_s1` | dc_B_held_surgio_b51_dr_s1 -> coco_yolo11m | cobra:train, df:train, ts:train125 | cobra:val, df:val, ts:val17 | best.pt on lists/B_held_surgio_b51_dr_s1/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_B_held_elekta_xvi` | dc_B_held_elekta_xvi -> coco_yolo11m | carm:train, df:train, ts:train125 | carm:val, df:val, ts:val17 | best.pt on lists/B_held_elekta_xvi/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_B_held_cios_fusion` | dc_B_held_cios_fusion -> coco_yolo11m | carm:train, cobra:train, ts:train125 | carm:val, cobra:val, ts:val17 | best.pt on lists/B_held_cios_fusion/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `dc_B_held_cios_fusion_s1` | dc_B_held_cios_fusion_s1 -> coco_yolo11m | carm:train, cobra:train, ts:train125 | carm:val, cobra:val, ts:val17 | best.pt on lists/B_held_cios_fusion_s1/val.txt (17 TotalSegmentator val subjects' styled renders + real val frames of the training devices) | args.yaml (yolo11m.pt); list files counted 2026-09-23 |
| `lc_surgio_b51_dr` | lc_surgio_b51_dr -> dc_B_held_surgio_b51_dr_s1 -> coco_yolo11m | carm:train(N frames), cobra:train, df:train, ts:train125 | carm:val | best.pt on the target device's real val split (lists/lcurve_surgio_b51_dr_N*/val.txt) | args.yaml of lc_* runs (model = parent best.pt); list files counted 2026-09-23 (7,322 styled in train incl. the target device's card) |
| `lc_elekta_xvi` | lc_elekta_xvi -> dc_B_held_elekta_xvi -> coco_yolo11m | carm:train, cobra:train(N frames), df:train, ts:train125 | cobra:val | best.pt on the target device's real val split (lists/lcurve_elekta_xvi_N*/val.txt) | args.yaml of lc_* runs (model = parent best.pt); list files counted 2026-09-23 (7,322 styled in train incl. the target device's card) |
| `lc_cios_fusion` | lc_cios_fusion -> dc_B_held_cios_fusion -> coco_yolo11m | carm:train, cobra:train, df:train(N frames), ts:train125 | df:val | best.pt on the target device's real val split (lists/lcurve_cios_fusion_N*/val.txt) | args.yaml of lc_* runs (model = parent best.pt); list files counted 2026-09-23 (7,322 styled in train incl. the target device's card) |
<!-- END:GENERATED lineage -->

---

## 5. What is not established here

- **Train and val lists that are not recorded anywhere read here.**
  - `detector_v5z_final`: its film lists are unrecorded. Its C-ArmLSpine verdict rests on its timestamp; its
    NHANES verdict rests on the declared in-sample caveat.
  - `anchor_det_v1`: only the registry BACKFILL bank `~/anchor_drr` is recorded.
  - `allspine_v2_r1`: its bank was deleted on 2026-09-20, so its lists survive only in logs.
- **ImageNet initialisation.** Whether the level encoders started from ImageNet is not recorded.
  `train_level_classifier` uses ImageNet weights only when they are cached on the node, and random initialisation
  otherwise. The chains above treat this root as public. That is an assumption.
- **Split-level tokens only.** Real corpora are tokenised at split level: `carm:test`, `cobra:test`, `df:test`. A
  patient under two case ids inside one corpus would not show. No such alias is known for COBRA, C-ArmLSpine or
  DeepFluoro. The 74,364 COBRA near-duplicate pairs at NCC32 ≥ 0.97 are, per `atlas/dataset.json` Noise (8),
  different patients at the same gantry angle.
- **C-ArmLSpine person identity** is not established (149 cases on five dates).
- **The COBRA body truth** in the body-box rescore is built from SPINEPS masks. Whether those instance ids can be
  trusted is the `results/spineps_ids/` audit's question, not this one's.
- **Evaluators this document did not cover.** It lists every evaluator on a manuscript path and scans the rest
  statically. Scripts that produced numbers for other documents (FluoroCap, the level banks v2–v7, the competitor
  benchmark) are listed in 3.2 without verdicts on their results.
