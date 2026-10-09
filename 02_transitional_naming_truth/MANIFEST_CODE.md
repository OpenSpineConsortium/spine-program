# MANIFEST_CODE: the repositories this project depends on, and the files that matter

Nothing that lives in a repository needs copying; `code/` holds copies of a few files for a reader with only this
folder, each with a header naming its source path and commit. Commits are the laptop working copies as inventoried
on 2026-10-08 (`../_plan/PLAN.md` "Prefixes"; `docs/handoff/README.md` section 9). Access is granted by Greg; how a
student is added to a private repository is not recorded.

## 1. `spinesurg-ct-nnunet` (private): the whole C-arm and film programme

- URL `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet`; branch `L6_Class`; commit **097933a**
  ("HANDOFF: the handoff for a new student or a fresh Claude project"); the working tree had five modified tools
  (`tools/level_prototype.py`, `tools/carmlspine_eval.py`, `tools/patient_keys.py`, `tools/pipeline_state.py`,
  `tools/test_patient_keys.py`) and the untracked `tools/transitional_review/`, `docs/REVIEW_TRANSITIONAL.md`,
  `HANDOFF/GREG_ONLY/`. The grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` was at 4e3fe938 and cannot
  fetch; code ships by `git archive` over ssh (`docs/handoff/RECIPES.md` section 0 item 2).
- Private since 2026-09-14; never push level-identification code public (`memory/fluorocap-repo-private.md`).

### Paper 2 and the frozen comparator (`SchwingNet/`)

| path in the repository | what | in this folder |
|---|---|---|
| `SchwingNet/LEVELCHECK_MODEL.md` | the comparator, endpoint, freeze (section 9), flag F1 (12), accepted-person analysis (13), automated reference (14), primary detector (15); FROZEN ecae75f, 1897772, 2993f40, b511985, d0403de | `docs/LEVELCHECK_MODEL.md` (identical bytes) |
| `SchwingNet/LEVELCHECK_CLAIM.md` | the literature reading and the superseded 89-person inventory | `docs/LEVELCHECK_CLAIM.md` |
| `SchwingNet/PAPER1_SCOPE.md` | the scope rule: no G3 test transitional person in paper 1; the "H6 seen" caution | referenced |
| `SchwingNet/TITLE.md`, `NUMBERS.md`, `CLAIMS_LEDGER.md`, `numbers_manifest.json`, `REVISION_LOG3.md` (line 7: the blinded-gate job ids), `RESULTS_BUILD.md` | paper 1's records that paper 2 cites | referenced (01 owns paper 1) |
| `SchwingNet/paper2_levelcheck/` | moved passages, moved manifest keys, `tables/tab_levelcheck.*`, `open_gate_40438004/` | `manuscripts/paper2_levelcheck/` (whole) |
| `SchwingNet/results/fig6/` (top level) | gate records | `results/paper2/fig6/` |
| `SchwingNet/results/fig6/frozen/` (967 files, 62 MB; `v1/` is the laptop twin of Ceph `frozen_v1`; `auto_reference.json` + `.sha256`, `auto_truth.csv`), `verification/` (352 files, 71 MB), `bank_g3_v2/`, `gatecheck_v2/`, `heads_v2/`, `sets_v2/` | byte-exact artefacts checked by sha256; `SchwingNet/.gitattributes` (`* text=auto eol=lf`) must travel with any copy of `frozen/**` | referenced by path (not copied) |
| `SchwingNet/results/auto_reference/`, `dual_loss/`, `rare_class/`, `learning/`, `figure2/figure2_metrics.json`, `figure2/figure2_transitional.json` | the reference calibration, D1 and the saturation curve, the split plan and subtypes, the Figure 2 analyses and the Figure 2 metrics file (STATUS.md section 4: A1.2, A1.3, A1.5, A1.6, A1.8) | `results/paper2/` (`learning/figure2_metrics.json` and `learning/figure2_transitional.json` added 2026-10-08; arrays, the `qc/` renders and one `.npy` not copied) |
| `SchwingNet/results/figure2/` (the rest: `heldout_l6.npz` 7,917,464 B, `figure2_map.npz` 129,790 B, `bank_person_census.json` 982,464 B, `heldout_census.json`, `v9_keys_snapshot.json`, `zones_lateral*.json`, `occlusion_clean/`), `SchwingNet/figures/figure2.record.json` (`#never_seen`, A1.5) | paper 1's Figure 2 records; 01 owns the figure | referenced |
| `SchwingNet/results/ALPHABET_LOSS.md` | the alphabet-loss arm: L6 recall 56.1-72.4 % [SEL-SPLIT] | referenced |
| `SchwingNet/results/power/power.json`, `results/power_table.json`, `results/stats_review/recompute.json`, `results/stats_review2/recompute.json` | the power numbers (A16.5, E.1-E.6) | referenced (01 holds the figure line) |
| `SchwingNet/packet_src/persons_available_2026-09-24.json` | the persons-available block (A16.6, A16.7) | referenced |
| `SchwingNet/results/transitional_registry/` (`REGISTRY.md`, `registry.csv`, review queues, `contact_sheets/`, `cobra/rows.csv`, `acquisition/ACQUISITION_PLAN.md`) | the registry and review queues | referenced (06 owns) |
| `SchwingNet/results/spineps_ids/TS12_VERIFY.md`, `IMPACT.md` (line 230: 10 of 24) | the TS "L6" verification and the labeller calibration | referenced |
| `SchwingNet/results/eval_gate/EVAL_LEAKS.md` (item 5 CLEAN for v9 never-seen L6; item 6 the [SEL-SPLIT] mark), `results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` (A5.4, A5.5) | the held-out audit | referenced |
| `SchwingNet/tools/fig6_score.py` | the scorer with the path defect (F3) | `code/fig6_score.py` |
| `SchwingNet/tools/fig6_truth_join.py`, `fig6_freeze.py`, `fig6_manifest.py`, `fig6_sets.py`, `fig6_valset.py`, `fig6_tau.py`, `fig6_arch.py`, `fig6_bank_check.py`, `fig6_bank_keytest.py`, `fig6_bank_rename_keyable.py`, `fig6_detector_lineage.py`, `fig6_exclusions.py` | the gate pipeline | referenced |
| `SchwingNet/tools/fig_power.py`, `fig_claim.py`, `d1_saturation.py`, `stats_review_recompute.py`, `stats_review2_recompute.py`, `results_macros.py` | power figures, the saturation curve, the statistical re-computations, the manifest check | referenced |
| `SchwingNet/slurm/fig6_eval.sh` (sha256 5eae5ea2... at release), `fig6_gate_precheck.sh`, `g3_split.sh` (**never resubmit in place**), `coupling.sh`, `rare_class_ts_drr.sh`, `rare_ctsp_drr.sh`, `rare_max_{stage,verse,verify}.sh`, `anomalous_inventory.sh` | the jobs of record | referenced |

### Tools (`tools/`)

| path | what | in this folder |
|---|---|---|
| `tools/rare_class_annotate.py`, `rare_class_carmlspine_drr.py`, `rare_class_maximize.py`, `rare_class_render.py`, `rare_class_stratify.py`, `rare_class_ts_annotate.py`, `rare_class_ts_fixids.py`, `rare_class_ts_iddiag.py`, `rare_class_ts_report.py`, `rare_class_ts_verify.py`, `rare_class_verify.py` (11 tracked `rare_class_*.py` at 097933a) | rare-class render banks with subtype truth | `code/` |
| `tools/transitional_detectors.py`, `eval_transitional.py`, `eval_transitional_detectors.py`, `eval_global_anomaly_signature.py`, `eval_anomaly_rule.py` | the four transitional detectors and their evaluations; the refuted R + C = 22 rule | `code/transitional_detectors.py`; the rest referenced |
| `tools/triage_variant_encoder.py`, `triage_variants.py`, `tp_morphology.py`, `lstv_vmva.py` (Diff-VMVA), `correct_buu_schema.py`, `buu_l4_contact.py`, `buu_l4_junction.py`, `geometric_indices_buu.py` | variant triage and the BUU-side geometry | referenced |
| `tools/film_ncurve.py` | the film N-curve (shared with 07) | `code/` |
| `tools/learning_embed.py`, `learning_analyse.py`, `learning_bank_census.py`, `learning_gradients.py`, `learning_l6_confound.py`, `learning_zones.py`, `explain_level_model.py` | what the encoder learned about L6 / T13 (regenerates the `.npz` arrays not copied) | referenced |
| `tools/pool_variant_cv.py`, `score_m1_f1.py` (the M1 mechanism test and the F1 flag scorer of section 12), `verification_pages.py` (the real-frame verification worklist) | paper 2 scoring | `code/` |
| `tools/auto_reference_calibrate.py`, `auto_reference_readers_ab.py`, `auto_reference_ab_summary.py` | the automated reference standard (readers A-D) | `code/auto_reference_calibrate.py`; the rest referenced |
| `tools/rib_count_reader.py`, `rib_count_lastrib.py`, `rib_count_recall.py`, `rib_count_summary.py`, `rib_count_ts_prep.py` | reader C, the direct rib count | referenced |
| `tools/mine_spine_anomaly.py`, `mine_spine_final.py`, `mine_spine_report.py`, `mine_spine_validate.py`, `anomaly_cooccurrence.py`, `anomaly_cooccurrence_from_labels.py`, `anomaly_manifest.py` (default `--bank` points at the deleted v5 bank, OQ F22), `scan_anomalous_ann.py`, `scan_anomalous_anns.py`, `find_rare_cases.py`, `transitional_subtypes.py`, `anomalous_inventory.py`, `transitional_registry.py`, `test_ts_transitional_registry.py` | the anomaly scan side (06 owns the registry) | referenced |
| `tools/lstv_flag_*.py` (19), `lstv_eval_*.py` (4), `lstv2_probe.py` | the 2-D binary flag, REFUTED (CTSP AUC 0.577) and its learning curve | referenced; do not rebuild |
| `tools/make_split.py` (L978-981: the in-place rewrite), `patient_keys.py` (modified in the working tree), `eval_gate.py`, `leak_check.py`, `spineps_ids.py` (`relabel_by_ctd`), `alphabet_couple.py`, `level_prototype.py` (modified), `head_dual.py`, `stats_compare.py` (`--help` crashes, F20), `test_stats_compare.py` | the shared stack (01 and 10 own them) | referenced |
| `tools/transitional_review/` (untracked: `anomaly_rules.py`, `anomaly_rules_array.sh`, `build_review_tree.py`, `rule_report.py`, the review app) | the review tree; to be committed after its self-tests (OQ C21, F12) | referenced (06 owns) |

### Jobs (`slurm/`)

`slurm/auto_reference_*` (4) and `auto_reference_cpupatch/` (the readers A/B runs and the SPINEPS CBCT patch),
`body_mask*` (3), `eval_fold_checkpoint`, `eval_shortcut_controls`, `eval_films_vs_fluoro`, `eval_anomaly_rule`,
`pelvis_landmarks`, `pelvis_lm_femur_ts`, `sweep_rib`, `sweep_roles`, `sweep_l4`, `sweep_cns` (the count-from-sacrum
heads); `lstv_flag_*.sh` (the refuted line); `harvest_verse_{census,ts,ts_cpu,render}.sh`, `ctsp_registry_census.sh`,
`harvest_cobra_{cases,ts}.sh`, `harvest_validate_{a,b}_ctsp.sh`, `other_ct_fetch.sh`, `acquisition_submit.sh` (06);
`paired_sets_properties.sh` (the job template). All referenced.

### Documents (`docs/`)

| path | what |
|---|---|
| `docs/REVIEW_TRANSITIONAL.md` (untracked, 6,656 B, 2026-09-27 17:09) | the reviewer instructions for the two-stage read (to be committed) |
| `docs/ruleclass/PREREG_rules.md` (DRAFT v1, f15da62, 16,493 B), `CLASSIFIERS.md` (R9-R11 the labellers; R30; R36 the Dataset803 weights), `TIERS.md` | the pre-registration (section 9 freeze block), the labeller definitions, the tiers |
| `docs/RESUME_2026-09-22_PM.md` (checkpoint 17:55: the release procedure; L28-33 next steps; L63-68 the pelvis gate; L167, L197 Greg on Dataset803) | the resume file of the gate week |
| `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | every job cancelled on 2026-09-27 with its resume instruction |
| `docs/FLAGSHIP_PLAN.md` ("The claim (G6)" item 4: the 90 % and 85 % targets; "The split"; "Gates") | the pre-stated targets |
| `docs/DATA_ACCOUNTING.md` (section 5.2: a model descending from v8/v9 cannot score those persons), `docs/ANOMALY_RULE_EVALUATION.md`, `docs/CENSUS_TABLE_2026-09-25.md` (counts one high), `docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `docs/data_requests/SX-Stitch_request.md`, `docs/outreach/balgrist_data_request_2026-09-21.md` | accounting, the refuted rule, the census, the data requests (DAT-1) |
| `HANDOFF/` (`README`, `GLOSSARY`, `RECIPES`, `RESULTS_CATALOG`, `DATASET_USAGE`, `LEAKAGE`, `OPEN_QUESTIONS`, `INFRASTRUCTURE`, `MANUSCRIPTS`, `CONTEXT_EXPORT`, `RESEARCH_DIRECTIONS`, `LITERATURE_STATE`, `literature_state/`, `working_notes/`, `context/`); `HANDOFF/GREG_ONLY/` never copied | copied whole into `docs/handoff/` (the e-mail redactions in `MANIFEST_LOCAL.md`); `context/` became `memory/` |
| `reader_space/` (`README.md`, `app.py`, `carm.py`, `viewport.py`, `Dockerfile`, `requirements.txt`) | the reader study Space; `_original_space/` excluded (a superseded backup carrying the banned word) | `code/reader_space/` |

## 2. `CTSpinoPelvic1K` (public): the dataset and the CTSP read-tier truth

- URL `https://github.com/OpenSpineConsortium/CTSpinoPelvic1K` (remote `osc`; also
  `https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K`, remote `origin`); branch `master`; commit
  **7ddfe38** (working tree modified). Push to both remotes through WSL.
- Files that matter here: `CLAUDE.md` (the label-scheme and id-29 rules), `docs/castellvi_consensus.csv`
  (two radiology residents, columns `read_1_NA` and `read_2_MI`; 33 graded), `docs/castellvi_readers_2026-09-04.csv`,
  `docs/lstv_reread_queue.csv` (append re-read discrepancies here, never a new file), `docs/CORRECTIONS.md` (125
  source-GT corrections, all "pending (in review)"), `docs/CASTELLVI_SCREEN_BLIND_SPOT.md` (the refuted pelvic
  cues, D.21), `paper/mpda/main.tex` lines 919-921 (the whole-cohort Castellvi read), `morphometrics/` (the v11
  measurements), `Student_Projects/RECIPE.md` section 0 (who is who) and `BOARD.md` (nested repository
  `OpenSpineConsortium/Student_Projects`, `main`, local commit 3f1cf04 deliberately not pushed).

## 3. `OpenSpineToolkit` (public): the label resolver

- URL `https://github.com/OpenSpineConsortium/OpenSpineToolkit` (`osc`; also
  `https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit`, `origin`); branch `main`; commit **cb43197**.
- Files that matter: `ostk/labels.py` (`labels_for(volume)`: the only way to resolve a CTSP or Dataset803 label
  map); the canal-closing regression at 1b7005c is open (project 04) and the rule-4 canal features of
  `PREREG_rules.md` must not come from ostk at or after that commit.

## 4. `XRSpinoPelvic1K` (private): the X-ray and DRR level-localisation repository

- URL `https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K`; branch `main`; commit **4f22935** ("annot:
  check the two-head rule the guide has always stated"); private since 2026-09-26. No file of this folder depends
  on it; it is the sibling of project 07 and its `dataset2024.zip` (4.0 GB) is referenced by path there.

## 5. `spine-detector` (private GitHub; the local folder has no `.git`, commit not recorded)

- The radiograph corner-detector corpus (33,943 instances) and the detectors; grid `/wsu/home/go/go24/go2432/spine-detector/runs/` (GRIDLS section `ls ~/spine-detector/runs`, `../10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`).
  `det_g3_primary_s0` (the section 15 primary detector) and the real-frame detectors `rx_lodo_carmlspine_1024`
  descend from it. Project 01 holds the `src/` snapshot (`canonical_slots`). Referenced only.

## 6. Hugging Face and the Spaces

- `OpenSpineConsortium/spinopelvic-seg-checkpoints`: the Dataset803 pelvis weights (sacrum + hips, the caudal
  anchor of rule 1 and of TODO step 1); Dataset803 has no `results/` tree on the grid (`RECIPES.md` section 3.2;
  `CLASSIFIERS.md` R36). `OpenSpineConsortium/spinopelvic-seg` is the public code repository the NeurIPS
  camera-ready cites (commit 70de829 in `CTSpinoPelvic1K`); its live visibility was not re-checked.
- The reader study Space (`code/reader_space/`, `sdk: docker`, `hf_oauth: true`): its repository id is not
  recorded in this folder (the review-space ids are in project 11's memory note `review-space-repos`). The films,
  answers and reads live in private dataset repositories; the Space holds no model and no weights.
- The private weights repository behind the level service (project 12) is never served by the website.

## 7. Beethoven (how a student reaches the grid)

`https://github.com/OpenSpineConsortium/beethoven` and `beethoven-vscode` (private; project 11). Not a dependency
of this folder's work, which runs under Greg's account only (the v9 bank holds BUU pixels, `RECIPES.md` section 0
item 9).
