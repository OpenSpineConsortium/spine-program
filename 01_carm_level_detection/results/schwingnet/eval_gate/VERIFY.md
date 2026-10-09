# VERIFY: an adversarial check of the evaluation gate, the leak sweep and the arc re-score

Written 2026-09-24. This check tried to get a leaked number past `tools/eval_gate.py`. It then re-checked, without the
gate's code, three rows that `EVAL_LEAKS.md` calls CLEAN and the claim that the 40 new arc subjects are unseen. Nothing
in the manuscript, the gate or the evaluators was edited. Every script and result this check wrote is in `verify/`:

- `verify/*.py` and `*.json`: the local checks for items 1b, 2 and 3. They read copies of grid files from a `grid/`
  folder beside them, which is not committed: the list files, the label caches, `SET_INFO.json`, `matches.json` and
  the TotalSegmentator fingerprints. Each script names the grid path it copies.
- `verify/grid_jobs/`: the grid job scripts, their outputs (`*.out`), one log per call (`logs/`) and the small result
  files (`out/`).

The grid fixtures are under `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/verify/`.

## Verdicts

| item | verdict | in one line |
|---|---|---|
| 1a. Every wired evaluator, called on patients its checkpoint or an ancestor saw | **PASS** | 26 of 26 calls that reached their gate raised an `eval_gate` exception before anything was scored, and none wrote a result. One call exited before its gate and was replaced by two calls that reach it. |
| 1b. Other routes past the gate | **FAIL** | Three routes let a leaked number through carrying `held_out: true`: `arc_recall_eval.py --matches`, `carry()` trusting any block, and pre-formed patient keys. The first re-emitted all 456 pooled cells of the void arc curve as held out. |
| 1c. Evaluators that still do not call `assert_unseen` | **FAIL (contract)** | 27 weight-loading scripts in EVALUATORS.md do not call it. The inventory lists all 27 as off the quoted path. Two Figure 2 evaluators that are on the quoted path are not in EVALUATORS.md and do not call it either. |
| 2. Three CLEAN rows, re-checked from the trainer configs | **PASS** | Overlap 0 for every pair: NUMBERS:L105, FIG3:005 and FIGREC:figS4/01. A fourth row, whose evaluator makes no gate call (FIGREC:figure2/06, /08, /10), is also 0. |
| 3. The 40 new arc subjects, and two curve cells | **PASS** | None of the 40 is in any train or val list of any scored chain, and none has a duplicate CT under another TotalSegmentator id. Three cells re-derived from `matches.json` match to 1e-12, bootstrap bands included. |
| 4. `tests/test_eval_gate.py` | **PASS** | 25 passed, 0 skipped: the 20 gate tests, including the 7 that read the real store, and the 5 in `test_eval_leaks.py`. |

The gate refuses every leaked input it is shown. It trusts three things it should check: a verdict already written
in a dump, the predictions `--matches` hands it, and a patient key supplied instead of a name. Item 1b and the Figure 2
evaluators are the work left.

---

## 1. Getting a leaked number past the gate

### 1a. Every wired evaluator, called on patients it saw (grid jobs 40430642, 40430844 and 40430994)

Every evaluator ran through its own command line on the grid, against the grid store
(`or_ready/eval_gate/touched.json` plus `ondemand/`), with the checkpoints on disk (matched by path and sha256). The
grid copies of 17 files have the same md5 as this checkout: `eval_gate`, `patient_keys`, `leak_check`,
`checkpoint_lineage` and the 13 evaluators called below. They are listed at the top of
`verify/grid_jobs/verify_gate_40430642.out`.

Job 40430642 was cancelled while running G19. That G19 used the default film spines, which the quoted a3a rows never
used, so job 40430994 re-ran G19 with `--only-prefix NHANES_nhanes_lumbar` (the quoted 25), then G20 onward.

Three kinds of input were used:

- **ARC17**: the 17 subjects of the void arc curve. They are VAL (selection) subjects of every `dc_*` arm.
- **s0970**: a subject in the TRAIN set of `anchor_none_v2_17-1882` only. That checkpoint is the parent of
  `rx_lodo_carmlspine_1024`, and s0970 is in none of rx_lodo's own lists.
- **CTSP_0001**: a subject in the TRAIN set of `model_scal_pt_render.pt` only. That checkpoint is the parent of
  `model_scal_pt_ft.pt`.

An evaluator whose evaluation set is fixed got the leak it can actually receive instead. Each input is a fixture in
`verify/grid_jobs/verify_setup.py` and exists only to put a seen patient in front of the evaluator.

| test | evaluator | checkpoint | input | raised | seen where |
|---|---|---|---|---|---|
| G01 | `realxray_eval.py` | dc_P_pooled | ARC17 frames | SeenInEvaluation | 17 in VAL of dc_P_pooled |
| G02 | `realxray_eval.py` | rx_lodo_carmlspine_1024 | s0970 frame | SeenInEvaluation | TRAIN of anchor_none_v2_17-1882 (ancestor) |
| G03 | `realxray_eval.py` | rx_lodo_carmlspine_1024 | real COBRA test | SeenInEvaluation | 27 of 27 in VAL of rx_lodo (its selection split) |
| G04 | `arc_recall_eval.py` | the four arc arms | the real old set (`devcorpus_arc/anglesweep`) | SeenInEvaluation | 17 in VAL of dc_P_pooled |
| G05 | `arc_recall_eval.py` | real_lodo | s0970 set | SeenInEvaluation | ancestor TRAIN |
| G06 | `arc_prior_check.py` | the four arc arms | the real old set | SeenInEvaluation | 17 in VAL of dc_P_pooled |
| G07 | `arc_prior_check.py` | real_lodo | s0970 set | SeenInEvaluation | ancestor TRAIN |
| G08 | `arc_angle_set.py --gate-weights` | the four arc arms | ARC17 subjects file | SeenInEvaluation (before rendering) | 17 in VAL of dc_P_pooled |
| G09 | `arc_angle_set.py --gate-weights` | real_lodo | s0970 | SeenInEvaluation (before rendering) | ancestor TRAIN |
| G10 | `case134_sweep.py score` | rx_pooled_1024 | the real case134 spin | SeenInEvaluation | case134 in TRAIN of rx_pooled_1024 |
| G11 | `case134_sweep.py score` | dc_P_pooled with rx_pooled_1024 grafted on as its parent (synthetic store) | the real case134 spin | SeenInEvaluation | TRAIN of rx_pooled_1024 (ancestor) |
| G12 | `level_prototype.py` | detector dc_P_pooled | ARC17 images | SeenInEvaluation | 17 in VAL, at the detector |
| G13 | `level_prototype.py` | detector rx_lodo_carmlspine_1024 | s0970 image | SeenInEvaluation | ancestor TRAIN, at the detector |
| G14 | `level_prototype.py` | detector dc_P_pooled, encoder model_scal_pt_ft | CTSP_0001 image | SeenInEvaluation | the detector passed; the encoder was refused through its ancestor model_scal_pt_render |
| G15 | `head_mixed_length.py` | dc_P_pooled as `--model` (the gate runs before the model is loaded) | bank whose val is ARC17 | SeenInEvaluation | 17 in VAL |
| G16 | `head_mixed_length.py` | model_scal_pt_ft | bank whose val is CTSP_0001 | SeenInEvaluation | ancestor TRAIN |
| G17 | `learning_embed.py` | model_scal_pt_ft | bank whose val is CTSP_0001 | *not reached* | the script exits before its gate: the wrapped encoder has no `layer4` |
| G17b | `learning_embed.py` | allspine_v9 encoder | the real v9 bank, real keys map | SeenInEvaluation | 1,685 of 1,804 val patients in VAL, 73 in TRAIN |
| G17c | `learning_embed.py` | allspine_v9 encoder with model_scal_pt_render grafted on as its parent (synthetic store) | CTSP_0001 bank | SeenInEvaluation | ancestor TRAIN |
| G18 | `rigor_fixes.py a5-rows` | v8 encoder and head (defaults) | the real v8 val films | SeenInEvaluation | 1,784 of 1,784 in VAL, 192 in TRAIN |
| G19 | `rigor_fixes.py a3a-rows --only-prefix NHANES_nhanes_lumbar` | render and film detectors (defaults) | the quoted 25 NHANES lumbar spines | SeenInEvaluation | render detector passed (25 held out); film detector 24 of 25: 22 TRAIN and 2 VAL, its own lists and its ancestor detect_v3's |
| G20 | `SchwingNet/tools/fig4_pairs_pull.py` | none: the card's fold fits | the real calibration pairs, no declaration | SeenInEvaluation | geneva:phantom fitted in this run (the median is over every fold) |
| G21 | `lcurve_score.py` | read from the dump | real pre-gate dump `or_ready/lodo/sweeps/lodo_carm__cobra_test.json` | SeenInEvaluation (gated now through `carry`) | 27 of 27 in VAL of rx_lodo |
| G22 | `count_from_sacrum_eval.py` | read from the dump | the same dump | SeenInEvaluation (through `carry`) | 27 of 27 in VAL of rx_lodo |
| G23 | `device_fit.fold_gate`, the call `fit` makes | none | real pair names of four cards, plus one fold list with a specimen filed under two group names | SeenInEvaluation for bv_pulsera, pixium_4600 and the aliased specimen; cios_fusion and elekta_xvi pass | one phantom or one cadaver per card; 18-1109 on both sides of the aliased fold |

G01–G22 had to fail and write nothing. Two runs left a directory behind: `arc_recall_eval` creates its `--out`
directory before the gate, and the G04 and G05 directories are empty. Where an evaluator takes several checkpoints
(G04, G06, G08), the first refused arm stops the run. The other arms were refused one by one in
`test_real_arc_leak_every_scored_detector` (item 4), and s0970 refused `real_lodo` in G05, G07 and G09.

G11 and G17c use a synthetic store because no real checkpoint in the store has the right shape:

- No checkpoint in `touched.json` descends from one that trained on case134, so G11 grafts rx_pooled_1024 onto
  dc_P_pooled as a parent.
- The one level encoder with an ancestor-only subject is `model_scal_pt_ft`, which `learning_embed` refuses to load, so
  G17c grafts model_scal_pt_render onto the v9 encoder as a parent.

In both, every other row of the store is the real one. The two stores are
`synthetic_touched_case134.json` and `synthetic_touched_v9.json`, in the grid verify directory.

Controls, which had to pass, did:

- C01: `eval_gate.py check`, rx_lodo_carmlspine_1024 on carm_test. HELD OUT, 28 patients over 56 frames, 2 checkpoints
  in the chain.
- C02: `realxray_eval.py` on the same pair. It passed the gate, scored all 56 frames and wrote `held_out=True`.
- C03: the four arc arms on the 40 new subjects. HELD OUT for all four, 40 keys each.
- G23's cios_fusion and elekta_xvi folds passed.

Nothing was written under `or_ready/arc/` (checked by mtime at the end of the job).

### 1b. Three routes past the gate that do not go through an evaluator's own gate call

**(i) `tools/arc_recall_eval.py --matches` checks the weights named on the command line, not the ones that made the
predictions (demonstrated).**

- The gate runs on `--weights`. With `--matches`, the records come from a previous run's `matches.json`, which records
  its own `weights`.
- Nothing compares the two. Nothing carries the old file's verdict, and the void run's `matches.json` has no
  `eval_gate` block.
- Demonstration: `--weights pooled=FluoroCap/detect_v5z_final_best.pt` is a checkpoint the gate passes for the 17
  subjects, with its lineage complete. It was run with `--matches` pointing at the void run's `matches.json`, whose
  `pooled` is dc_P_pooled.
- Result: a `recall_vs_angle.json` with `eval_gate.held_out: true`, overlap 0, unresolved 0. All 456 pooled cells equal
  the void curve's. At conf 0.25, tilt 0, Elekta lat 0 is 0.894 and lat +90 is 0.352.
- `tools/arc_curve_compare.py` checks only `eval_gate.held_out is True` and would accept this file.
- The run was local, on the repo `touched.json`, so the checkpoint was matched by path rather than sha256. That changes
  nothing here: the flaw is which weights get checked. The leaked output was not kept. What it carried is in
  `verify/matches_bypass_demo.json`.
- Fix: refuse `--matches` unless the file's `weights` equal `--weights` and its own `eval_gate` block says held out, or
  gate the file's `weights` instead of the command line's.

**(ii) `eval_gate.carry()` accepts any block that has `gate_version`, `held_out` and a `checks` list (demonstrated,
`verify/verify_trust.json`).**

- T1: a dump of dc_P_pooled on the 17 arc subjects, with a hand-written block `{held_out: true, checks: []}`, is
  carried as held out. An empty `checks` list is accepted.
- T2: a genuine block from another checkpoint, pasted onto a dump whose `weights` is dc_P_pooled, is carried as held
  out. `carry()` never checks that the block's `checkpoint` equals the dump's `weights`, or that its keys cover the
  dump's frames.
- T3 shows the same dump with no block is refused (SeenInEvaluation), and so is an rx_lodo dump on s0970.
- Every scorer that reads a dump goes through `carry()`: lcurve_score, lcurve_report, fig3_detection_grid, the
  contribution matrix, counting, coupling, carmlspine_eval, `rigor_fixes a1`–`a9`, or_recall_curves and
  or_lodo_rescore_outline. So a dump whose block is stale, pasted or hand-written sails through all of them.
- Fix: in `carry()`, refuse a block with no checks, and refuse one whose `checks[].checkpoint` does not cover the dump's
  `weights`. Where the dump records its frames, re-gate it against the current store.

**(iii) A patient key handed to the gate is used as given, so a key the store never uses matches nothing (demonstrated;
measured on the real v9 bank).**

- `key_items()` passes any string of the form `corpus:id` straight through when `corpus` is known, and `implant` is a
  known corpus. A dict that carries `key` returns that key and never keys its `case` or `stem` (T4: `{key: ts:s9999,
  case: TS_s0585}` is checked as `ts:s9999` only).
- `patient_keys.key_any` deliberately refuses to make a patient called `implant:<case>`: it keys an implant render to
  its source CT. But `implant:0001_v0` handed in as a key is accepted. The store holds no `implant:` key at all (0 in
  306 rows), so the key passes: `implant:0001_v0` against model_scal_pt_render, which trained on ctsp:0001, is HELD OUT.
- `tools/learning_embed.py` gates the bank's val crops as `keys.get(case) or dict(case=case)`, with
  `--keys ~/patient_keys_v9.json`. That map sends 194 of the 2,811 v9 val cases to `implant:<case>_v<k>` keys
  (job 40430856, `verify/grid_jobs/out/K1_implant_keys.json`).
- Keying every case itself, the gate finds 164 val persons in the v9 encoder's TRAIN keys. Handed the map, it finds 73.
  **91 persons the encoder trained on are invisible to the gate on this route** (ctsp:0001, 0010, 0018, …).
- G17b still raises, because the whole v9 val split is the encoder's selection set, so no number passed. But the
  overlap the gate reports is under half the true figure. Any encoder not selected on that split would be passed on
  those 91 persons.
- Fix: key the case and the supplied key both, and use the union, as `key_items` already does for case and stem. Or
  canonicalise `implant:` keys through `patient_keys.implant_sources` and refuse the ones it cannot resolve.

Smaller things found while doing this. None of them passed a number.

- `tools/arc_angle_set.py` gates only when `--gate-weights` is given (`_gate` returns None otherwise), so a set can be
  built with no verdict. The scorers gate again, so this is defence in depth only.
- `arc_recall_eval.py` writes `matches.json`, stamped with the gate's verdict, before it checks that every scored
  subject is in `SET_INFO.json`. It then exits.
- The anglesweep frame stem (`s0585_lat+000_tilt+00`) matches no keying rule. A frame keyed by its stem alone raises
  UnkeyedEvalItem, which is safe but fails for the wrong reason. The fixtures in 1a carry `case: TS_<s>`.
- The a5 (v8) and v9 val splits are more than selection sets. Keyed as the gate keys them, 192 v8 val persons and 73
  v9 val persons are also in their encoder's TRAIN keys. That is 164 for v9 when the implant renders are keyed to their
  source CT (iii). Every example the gate prints is a CTSpinoPelvic1K person (`ctsp:####`), so this is a person-level
  split leak inside those banks. `fig2_occlusion_clean.py`'s docstring names one cause, implant renders keyed apart from
  their source CT. The rest was not traced here. It adds to the NOT HELD OUT verdict on those rows and does not change
  it.

### 1c. Evaluators that still do not call `assert_unseen`

Taken from the generated table in `EVALUATORS.md` §3.2: every row whose "loads weights" column is not `-`, grepped for
`assert_unseen`, `carry`, and a subprocess into `realxray_eval.py`.

- **Gated (9):** `realxray_eval`, `arc_recall_eval`, `case134_sweep`, `level_prototype`, `head_mixed_length`,
  `learning_embed` and `rigor_fixes` call it themselves. `devcorpus_train` and `lcurve_train` load YOLO only to train,
  then score through a `realxray_eval.py` subprocess that runs the gate.
- **Not gated (27):** `common_testset_eval`, `corpus_xray_gate_eval`, `detector_failures`, `detector_quality`,
  `eval_anchor_free`, `eval_feasibility_claims`, `eval_fov_separability`, `eval_global_anomaly_signature`,
  `eval_interior_windows`, `eval_level_flags`, `eval_raw_films`, `eval_runtime_cost`, `eval_scaling_curves`,
  `eval_shortcut_controls`, `eval_surgeon_benefit`, `eval_transitional`, `eval_transitional_detectors`,
  `eval_windows_by_class`, `fiducial_walk`, `fluorocap_ablation_eval`, `night_eval_realpanels`, `realxray_robustness`,
  `robustness_eval`, `sweep_map` (`holdout.trained_on` only), `thoracic_xr_eval`, `validate_guided`, `wholespine_eval`.
  - EVALUATORS.md marks every one "not on the path of a quoted number". A grep of NUMBERS.md, main.tex, sections/,
    tables/ and CLAIMS_LEDGER.md for their names finds none.
  - They still break the contract in `docs/DATA_ACCOUNTING.md` §5.3: "It is not opt-in. Every evaluator that loads a
    checkpoint and scores an evaluation set calls `assert_unseen`". Each one is a way to produce a number that never
    meets the gate.
- **On the quoted path, not in EVALUATORS.md, not gated (2):** `tools/fig2_occlusion_clean.py` and
  `tools/fig2_heldout_embed.py`. Both are untracked files. `main.tex:115` names both as sources of Figure 2.
  - `fig2_occlusion_clean` drives NUMBERS:L45 (occlusion enrichment). It drops a crop only when its person is in the
    encoder's TRAIN keys, so what it draws from is still the encoder's selection split, and it makes no gate call.
  - `fig2_heldout_embed` trusts a renderer's `held_out: true` field.
  - CHK-9 does check their rows afterwards (L45 is LEAKED on `v9_val_clean`; the carm L6 rows run on
    `carm_l6_never_seen`), so no number escapes CHK-9. But the evaluators themselves refuse nothing.
- **Stale:** the generated table says `lcurve_train.py` and `fig3_detection_grid.py` have gate "none". Both are gated,
  through `realxray_eval` and through `lcurve_score.carry`; `build_inventory.py`'s scan does not see the delegation. The
  table also omits scripts added since it was generated. Four of them are gated: `arc_prior_check` and `head_dual` call
  `assert_unseen`, `lcurve_fill` calls it and `carry`, and `indomain_name_fill` scores through `level_prototype`. The
  two Figure 2 evaluators above are not.
  - One watch item in `indomain_name_fill.py` (untracked, live workflow): its series rows are labelled
    `held_out="gate + lists"` when `r.get("gate_held_out", True)`, so a row that records no gate verdict at all is
    labelled held out. Cells built at line 691 always record one. Rows from anywhere else would not.

---

## 2. Three CLEAN rows and a fourth, re-checked without the gate (`verify/verify_clean_rows.py`, `.json`)

Each checkpoint's lists come from its own `args.yaml` → `data.yaml`, read on the grid. The files were:

- the list `.txt` files;
- the Ultralytics label caches written at launch, where one survives;
- the directories as they stand today, where it does not.

Keys follow DATA_ACCOUNTING §4, written out in the script rather than imported: C-ArmLSpine `^(case\d+)_`, COBRA
`^[A-Z]\d{3}_`, DeepFluoro specimen id, TotalSegmentator `s\d{4}`. The evaluation set is the directory the number was
scored on. The C-ArmLSpine test export was rewritten on 2026-09-23 between 05:12 and 05:17, so its case set was also read
from the label cache of 2026-09-21 23:53. Both hold the same 28 cases.

| row | pairs | lists read | overlap |
|---|---|---|---|
| `NUMBERS:L105` (pooled real-frame detector minus held-out, sacrum at 0.25) | rx_pooled_1024 and rx_lodo_carmlspine_1024 on carm_test | see below | **0** |
| `FIG3:005` (Surgio arm 3, 252/287 = 87.8 %) | dc_B_held_surgio_b51_dr_s1 on carm_test | see below | **0** |
| `FIGREC:figS4/01` (case134 spin, four detectors) | dc_P_pooled, dc_A, dc_B, rx_lodo_carmlspine_1024 on case134_spin | see below | **0** |
| `FIGREC:figure2/06`, `/08`, `/10` (never-seen L6), a fourth row, chosen because its evaluator makes no gate call | allspine_v9 encoder on case42, case121, case136 | see below | **0** |

**NUMBERS:L105.**

- a3.json names the pair through `sweeps/pooled__carm_test.json` and `sweeps/lodo_carm__carm_test.json`. The `weights`
  of those dumps are rx_pooled_1024 and rx_lodo_carmlspine_1024.
- rx_pooled_1024 trains on the C-ArmLSpine train directory and selects on its val directory, so this is the one pair of
  the three where the same corpus sits on both sides.
  - Its train directory today holds 106 cases: the 105 of the 2026-09-22 cache, plus case134, added on 2026-09-23 at
    05:28. Its val directory holds 15.
  - Its own launch caches were overwritten by later scans, so its lists at launch (2026-09-21 22:00) are bounded by the
    export's split rule, `md5(case) % 10`, not read directly. That rule holds for all 149 cases on disk with 0
    violations, and the 28 test cases are exactly its test bucket.
  - Its COBRA and DeepFluoro lists and its parent anchor (TotalSegmentator only) cannot meet C-ArmLSpine.
- rx_lodo_carmlspine_1024 (launch caches): train 118 COBRA and 5 DeepFluoro patients, val 27 COBRA and 1 DeepFluoro.
  Its parent's lists are TotalSegmentator only.

**FIG3:005.**

- lcurve.json `devices/surgio_b51_dr/points[0].run` = dc_B_held_surgio_b51_dr_s1.
- `args.yaml`: `model: yolo11m.pt`, `data: B_held_surgio_b51_dr_s1/data.yaml`.
- Train: 239 patients (125 TotalSegmentator, 110 COBRA, 4 DeepFluoro). Val: 26 (17, 8, 1). There are no C-ArmLSpine
  lines, and no renders under C-ArmLSpine poses, because Surgio is held out and design B renders each card under its
  own device.

**FIGREC:figS4/01.**

- `slurm/case134_export_score.sh` names the four weights.
- The P_pooled lists hold 105 C-ArmLSpine train cases (420 lines) and 15 val cases, with no case134 line. They were
  written 2026-09-22 17:42, before case134 entered the train export on 2026-09-23 at 05:28. No render uses a case134
  pose.
- The A and B lists hold no C-ArmLSpine line, and rx_lodo's lists hold no C-ArmLSpine at all.
- `results/arc/case134_sweep.json` itself carries no `eval_gate` block and records no weight paths: it was scored at
  2026-09-23 17:24, before the gate. Its sentence "the pooled detector saw this patient's two SPOT frames in training"
  is false in the conservative direction, as EVALUATORS.md §1.4 already says.

**FIGREC:figure2/06, /08, /10** (grid jobs 40430879 and 40430973; `verify_l6_rows.py`, `verify_v9_sources.py`).

- The encoder's result json records no initialisation; the store gives ImageNet as its only root.
- Its bank, `allspine_v9_fov96_ctx/rung_1.npz`, holds 103,052 crops: 87,154 train and 15,898 val. They come from seven
  sources: buu_full, csxa, nhanes, ctsp_drr, verse_drr, physics_drr and physics_rare.
- The case names follow seven shapes: `BUU_FULL_buu_#…`, `CSXA_csxa_#`, `CTSP_COLONOG_#`, `NHANES_nhanes_*_#`,
  `ctsp_/totalseg_s/implant_/verse_scan-…_p#`, `verse#` and `gl#`.
- No case name mentions carm, cbct or `case<n>`. The only names containing 42, 121 or 136 are `CTSP_COLONOG_42`,
  `_121` and `_136`: CTSpinoPelvic1K records, a different corpus.
- The held-out root `rare_class/carmlspine_cbct_drr` names only case42, case121 and case136.
- The three patients are in no list the encoder trained or was selected on. The row stays CLEAN, although the evaluator
  that made it never called the gate (1c).

**The COCO root of every `dc_*` arm.** Their `args.yaml` says `model: yolo11m.pt`, a relative path. Both copies it
could have resolved to (`~/spine-detector/yolo11m.pt` and `~/spinesurg-ct-nnunet/yolo11m.pt`) have sha256
`d5ffc1a6…5b95`, and both carry `train_args.data = …/coco.yaml`, dated 2024-09-25 (job 40430642).

---

## 3. The 40 new arc subjects (`verify/verify_arc_lists.py`, `.json`)

The subject list is the same in the repo `subjects.json`, the grid `subjects.json` and the rendered set's
`SET_INFO.json`. The script imports nothing from the gate. It reads every basename in every list for `s####` tokens,
and also does a raw substring search for each of the 40 ids.

| chain | list (split) | lines | TotalSegmentator subjects | new 40 | old 17 (control) |
|---|---|---:|---:|---:|---:|
| pooled (dc_P_pooled → COCO) | P_pooled/train.txt | 18,906 | 125 | 0 | 0 |
| | P_pooled/val.txt | 1,998 | 17 | 0 | 17 |
| lodoA (dc_A_held_surgio_b51_dr → COCO) | train.txt | 11,164 | 125 | 0 | 0 |
| | val.txt | 956 | 17 | 0 | 17 |
| lodoB (dc_B_held_surgio_b51_dr_s1 → COCO) | train.txt | 10,432 | 125 | 0 | 0 |
| | val.txt | 858 | 17 | 0 | 17 |
| real_lodo (rx_lodo_carmlspine_1024) | train, launch cache (4 dirs) | 3,094 | 0 | 0 | 0 |
| | val, launch cache (2 dirs) | 752 | 0 | 0 | 0 |
| → anchor_none_v2_17-1882 | train, launch cache (= today's dir) | 569 | 42 | 0 | 5 |
| | val, launch cache (= today's dir) | 84 | 6 | 0 | 1 |

The control reproduces the ARC workflow's own finding exactly: 17 in each dc val set, 5 in the anchor's train and 1 in
its val.

**Identity.** `~/ts_dupscan_out/ct_fingerprints.json` covers both releases, v201 and v300. None of the 40 v300 CTs has
the same md5, or the same shape and affine, as a CT under any other TotalSegmentator id, and none is missing from the
fingerprints. So no chosen subject is filed under a second id that could sit in a list. The styled training corpus
(`devcorpus_build.py`) and the arc set (`arc_angle_set.py`) both render from `spine_project.TS`, the v300 release.

**Curve cells re-derived from `matches.json`** (grid `or_ready/eval_gate/arc_unseen/matches.json`). Its `eval_gate`
block says held out, with overlap 0 and unresolved 0, over the same four checkpoints as `subjects.json`, and its records
hold exactly the 40 subjects. Recall and the subject-clustered bootstrap (2,000 resamples, seed 0) were re-implemented:

| cell (conf 0.25, body, tilt 0) | n | hits | recall, recomputed | band, recomputed | published |
|---|---:|---:|---|---|---|
| pooled, Elekta XVI, lat −90 | 243 | 155 | 0.6379 | [0.5102, 0.7615] | identical |
| real_lodo, Surgio-B51, lat 0 | 240 | 0 | 0.0000 | [0.0000, 0.0000] | identical |
| lodoA, Elekta XVI, lat 0 | 240 | 192 | 0.8000 | [0.7029, 0.8912] | identical |

---

## 4. Tests

`python -m pytest tests/test_eval_gate.py tests/test_eval_leaks.py -v` gave 25 passed in 1.3 s, with 0 skipped. The
real-store tests ran against the repo `touched.json` and `results/arc/recall_vs_angle_unseen/`:

- the arc leak refused on every scored detector;
- the headline pair held out;
- selection on COBRA test seen;
- the fold-bank spelling;
- the unseen arc set passing all four arms;
- the curve's verdict;
- the prior check reproducing the curve.

None of the tests covers a route in 1b. A test for each would pin the fixes:

- `--matches` with mismatched weights must raise;
- `carry()` of a block with no checks, or with another checkpoint, must raise;
- a pre-formed `implant:` key must resolve or raise.
