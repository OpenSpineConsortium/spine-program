# MANIFEST_CODE: every code repository this project depends on

Nothing under `code/` is copied: each file below lives in a repository at the commit named, so a reader with the
repository has the file. Sizes are bytes from `git ls-files` plus `stat` on the laptop checkout, 2026-10-08.
Disposition rows: ssn r132 (image formation tools), r133 (PolyPose), r150 (job scripts), all "reference"
(`../_plan/DISPOSITION.tsv`).

## 1. spinesurg-ct-nnunet (private)

- URL `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet.git`; branch `L6_Class`; commit `097933a`
  (2026-10-08, "HANDOFF: the handoff for a new student or a fresh Claude project"). Private since 2026-09-14;
  never made public (`memory/fluorocap-repo-private.md`).
- The grid checkout `~/spinesurg-ct-nnunet` is at `4e3fe93` (2026-09-27) and cannot fetch; ship changes with
  `git archive | ssh tar`; `make physics` hard-resets it (`docs/handoff/RECIPES.md` section 0).
- The PolyPose generator commit `1f4418f` (2026-09-23) is an ancestor of both `4e3fe93` and `097933a`
  (`git merge-base --is-ancestor`, laptop checkout 2026-10-08), and the laptop's remote-tracking `origin/L6_Class`
  (at 097933a) contains it; the memory note's "never pushed" predates that. GitHub itself was not queried.
- Working-tree state at 097933a that touches this folder: `SchwingNet/results/polypose/rom_cine.json` untracked
  (copied here); `tools/polypose/cine_render.py` (104,995 B, 2026-09-26) and its job script `slurm/polypose_cine.sh`
  (7,237 B, 2026-09-26: five stages plan, warp, rgt, check chained with `afterany`; a lumbar flexion-extension cine on
  the whole-spine VerSe CT `verse823` with L5 fixed; refuses the cervical and whole regions until their `rom_cine.json`
  rows are filled; not held out, every VerSe CT is in the v9 renders) untracked (not copied; `TODO.md` step 2 commits
  them). The other untracked cine files of the same day (`slurm/cine_eval.sh`, `slurm/cine_latency.sh`,
  `tools/cine_eval.py`, `tools/cine_latency.py`, `SchwingNet/results/cine/`, `docs/CINE_*_2026-09-26.md`,
  `docs/FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md`) belong to project 01 (`git status` of the laptop checkout,
  2026-10-08). The five
  edited tools of the plan (`level_prototype`, `carmlspine_eval`, `patient_keys`, `pipeline_state`,
  `test_patient_keys`) belong to projects 01 and 10; `patient_keys.py` keys every render to its CT's person and
  its uncommitted edit matters here too.

### 1.1 Renderers and bank builders

| file | bytes | what it is |
|---|---:|---|
| `tools/render_physics_drr.py` | 18,934 | the physics renderer (perspective, polychromatic, scatter, noise; `--per-case 2 --det-px 640`) behind `physics_drr` and `physics_rare` |
| `tools/make_drr_dataset.py` | 28,297 | parallel-beam DRR banks (`--scheme ds813|verse`, `--respace`, `--paths2-only`, `--perturb physics`) behind `ctsp_drr`, `verse_drr`, the oblique sets and the sweeps |
| `tools/ts_to_drr.py` | 10,050 | TotalSegmentator lateral DRRs (`ts_drr`, `ts_drr_v3`); cites the v1 Zenodo record wrongly |
| `tools/make_anchor_drr.py` | 12,867 | the anchor-detection renders (`anchor_drr`) |
| `tools/spine_project.py` | 10,988 | projection utilities |
| `tools/strong_dr.py` | 20,632 | strong domain randomisation (SyntheX's lever 2) |
| `tools/dr_eval_report.py`, `tools/dr_smoke_check.py` | 5,616; 9,032 | domain-randomisation arm reports |
| `tools/film_match_augment.py`, `tools/film_style_dataset.py` | 12,088; 8,529 | film-styled twins (`*_film` banks, `film_style_ds`) |
| `tools/label_preservation_gate.py` | 5,716 | the gate that a styled or translated render keeps its boxes |

### 1.2 Device cards, styling, the device corpus

| file | bytes | what it is |
|---|---|---|
| `tools/device_fit.py` | 120,524 | pairs per device, the nine-term leave-one-group-out fit, Gaussian copula, AEC regression, coverage (`typicality_99`), the card writer (`docs/devices/<device>.json`, `.frames.csv`, `.3free.json`) |
| `tools/device_physics.py` | 19,155 | the forward physics the fit and the styler share; `image_stats` (the 37 statistics of the manifold) |
| `tools/device_style.py` | 28,809 | one styled frame = one copula draw through `device_fit.forward`; `SPREAD = 0.2` (the clip, the default; line 110 at 097933a); `SAMPLE_MODE = os.environ.get("DEVICE_SAMPLE_MODE", "clip")` (line 118: the default is `clip`; `typicality`, the gate at `TYPICALITY_Q = 99.0`, and `full` are opt-in through the environment variable, so the gate is off unless the variable is set, as `CLAUDE.md`, `STATUS.md` A12.6 and `docs/DEVICE_SPREAD_SWEEP.md` say); `demo` and `stats` |
| `tools/device_spread_sweep.py` | 11,447 | generates `docs/DEVICE_SPREAD_SWEEP.md` from the cards alone |
| `tools/device_param_audit.py` | 19,345 | generates `docs/DEVICE_PARAM_AUDIT.md` from the cards and the header census |
| `tools/device_census.py` | 23,421 | DICOM header and image census per device (`docs/devices/census/`) |
| `tools/device_refit.py`, `tools/card_refit_v2_diag.py` | 11,299; 12,399 | the refits (`or_ready/devices_refit*`) and their diagnostic |
| `tools/device_manifold.py` | 10,375 | per-device manifold |
| `tools/test_device_gate.py` | (in `tools/`) | asserts the typicality gate (named in `memory/device-sampling-audit.md`) |
| `tools/devcorpus_build.py` | 32,385 | `poses` per device, `render` once per geometry, `style` per device, `lists --design A|B|P` (only P refuses a split subject) |
| `tools/devcorpus_train.py` | 8,045 | COCO-init YOLO11m at 1024 on a styled corpus; `scores.json` under `~/spine-detector/runs/devcorpus/` |
| `tools/diag_bone_contact.py`, `tools/diag_card_lateral.py` | 6,427; 5,222 | card diagnostics |
| `tools/diagnostics/diag_aec_effect.py`, `diag_bone_share.py`, `diag_sweep_bone.py`, `diag_sweep_collimate.py` | 2,681; 1,623; 3,318; 3,634 | the three-defects diagnostics (`docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`) |

### 1.3 DeepFluoro calibration (23 files)

| file | bytes | what it is |
|---|---|---|
| `tools/deepfluoro_calibrate.py` | 25,461 | the nine-term calibration (`calibration_best.json`; +4.1 / +4.3) |
| `tools/deepfluoro_convention.py` | 6,381 | scores every projection convention by landmark reprojection (0.00 px) |
| `tools/deepfluoro_render.py` | 13,415 | renders the 366 projections at their own pose |
| `tools/deepfluoro_residual.py`, `_residual_all.py`, `_residual_regions.py`, `_smooth_decomp.py`, `_edge_bias.py`, `_explain_residual.py` | 7,890; 9,656; 9,722; 3,676; 5,306; 5,895 | the residual analyses of `docs/DEEPFLUORO_FORMATION.md` sections 2 and 5 |
| `tools/deepfluoro_photons.py`, `_pedestal.py`, `_noise_floor.py`, `_bandgain.py` | 6,956; 8,717; 9,330; 10,245 | photon, pedestal, noise-floor and band-gain terms |
| `tools/deepfluoro_anchor.py`, `_anchor_baseline.py`, `_anchor_report.py`, `_best_synthetic.py`, `_refine.py`, `_transfer.py`, `_show_calibrated.py`, `_poses.py` | 42,338; 3,857; 4,862; 11,172; 17,079; 9,179; 5,473; 6,606 | the render-only detector arms on DeepFluoro and the learned-refiner arms (C4.1, C4.4) |
| `tools/dl_deepfluoro.py` | 2,516 | the download |
| `tools/reg_deepfluoro.py`, `reg_deepfluoro_fakeh5.py`, `reg_env_test.py`, `reg_level_harness.py`, `reg_level_harness_analysis.py` | 35,909; 7,434; 17,957; 36,889; 6,898 | 2-D/3-D registration harness |
| `tools/drr_register.py` | 31,273 | DRR registration (shared with project 01) |

### 1.4 The corpus manifold, translation and the paired real sets

| file | bytes | what it is |
|---|---|---|
| `tools/corpus_manifold.py`, `tools/manifold_examples.py`, `tools/corpus_resolution.py`, `tools/formation_gap.py` | 65,204; 4,629; 1,236; 8,119 | `results/manifold/` (Figure S2), its example sheets and `formation_gap/` |
| `tools/paired_sets_properties.py` | 10,394 | properties of the paired (render, real) sets |
| `tools/drr2fluoro_cut.py` | 16,264 | CUT translation (refuted) |
| `tools/fluorogen_generate.py`, `_dataset.py`, `_check.py` | 12,966; 7,950; 5,358 | FluoroGen SDXL + ControlNet + LoRA (refuted route) |
| `tools/cobra_fetch.py`, `cobra_handedness.py`, `cobra_pairs.py`, `cobra_pairs_merge.py`, `cobra_varian_geometry.py`, `cobra_window_diag.py` | 10,555; 4,786; 14,340; 6,803; 38,206; 24,324 | COBRA Elekta frames, the Varian geometry map (solved 2026-09-23) |
| `tools/spinesac_bind_bodies.py`, `_ct.py`, `_ct_probe.py`, `_detect.py`, `_fetch.py`, `_inventory.py`, `_score.py`, `_sheets.py`, `_truth.py` | 13,600; 10,440; 3,432; 3,309; 9,154; 25,526; 19,986; 3,681; 17,972 | SpineSAC pairs |
| `tools/ljubljana_pairs.py` | 11,848 | the PIXIUM 4600 pairs |

### 1.5 PolyPose (`tools/polypose/` 16 files + `tools/polypose_*.py` 12)

| file | bytes | what it is |
|---|---|---|
| `tools/polypose_sample.py` | 89,612 | the generator: `generate|finalize|head`; samples whole sagittal profiles within the spec |
| `tools/polypose_warp.py` | 19,690 | the forward polyrigid warp (true matrix inverse, not diffdrr's rigid inverse) |
| `tools/polypose_invariants.py` | 99,946 | the self-failing invariant checks (Jacobian > 0, fused junction zero motion, pelvis fixed, profile in envelope) |
| `tools/polypose_manifest.py` | 63,301 | the manifest row per output; `evaluate_profile()` reads `docs/polypose_reference_envelope.json` |
| `tools/polypose_forward_test.py`, `_eval_ours.py`, `_reproduction_report.py`, `_hf_vs_h5.py`, `_apply_pose_flip.py`, `_drr_diag.py`, `_drr_diag2.py`, `_drr_diag3.py` | 19,816; 10,873; 16,280; 4,340; 4,611; 7,300; 6,389; 6,378 | the DeepFluoro reproduction and its diagnostics (`results/polypose/REPRODUCTION.md`) |
| `tools/polypose/build_sampling_spec_v2.py`, `check_sampling_spec.py`, `add_citations_v2.py`, `gen_rom_csv.py`, `wilke2017_rows.py`, `inspect_sources.py` | 36,644; 17,037; 23,445; 4,882; 2,801; 5,916 | the sampling spec, its checker (exits non-zero on a mismatch) and the ROM table |
| `tools/polypose/cohort_from_release.py`, `cohort_reduce.py`, `cohort_sagittal.py`, `measure_sagittal.py` | 10,959; 12,936; 27,976; 15,897 | the cohort re-measurement; `measure_sagittal.measure_image` is the one measurement path (G.7) |
| `tools/polypose/validation_cases.csv`, `validation_render.py`, `validation_report.py`, `fig2_panels.py` | 1,231; 15,775; 33,402; 5,072 | the validation chain's cases, renders and reporter (its output does not exist yet) |
| `tools/polypose/cine_render.py` | untracked (104,995 B, 2026-09-26) | the flexion-extension cine reader of `rom_cine.json` (`rom-check`, plan, warp, render, gt); its job script is the untracked `slurm/polypose_cine.sh` (section 1 and 1.6) |

### 1.6 Job scripts (`slurm/`, 127 files matched on 2026-10-08)

`slurm/device_census.sh`, `device_fit.sh` (`CMD=pairs|fit|display|cobra-thickness`, `DEVICE=`, `EXTRA=`; reqp,
16 CPU, 96 GB, 12 h, env `fluorogen`), `device_gate_smoke.sh`, `device_manifold.sh`, `device_param_audit.sh`,
`device_refit.sh`, `device_refit_c.sh`, `device_spread_arm.sh` (the A/B, not run), `device_spread_sweep.sh`,
`device_style.sh`; `devcorpus.sh`, `devcorpus_pooled.sh`, `devcorpus_train.sh` (`DESIGN`, `HELD`);
`deepfluoro_*.sh` (21: `acquire`, `pairs`, `pairs_control`, `calibrate`, `calibrate_v2`, `linear`, `orwindow`,
`pedestal`, `photons`, `refine_arm`, `residual_regions`, `v2`, `v2_crosseval`, `anchor*` (5), `ablate_edge`,
`vendor_fetch`, `vendor_unpack`); `dr_chain.sh`, `dr_corpus.sh`, `dr_eval.sh`, `dr_smoke.sh`, `dr_train_one.sh`;
`cut_drr2fluoro.sh`; `drr_register_landscape.sh`, `drr_register_selftest.sh`; `film_lora_apply.sh`,
`train_film_lora.sh`, `films_degraded_stage0.sh`; `fluorogen_generate.sh`, `fluorogen_lora.sh`,
`fluoro_selftrain.sh`; `render_detector_on_real.sh`, `render_smoke.sh`, `path_render.sh`; `cobra_*.sh` (17);
`spinesac_*.sh` (14); `polypose_*.sh` (23: `setup`, `env`, `selftest`, `check`, `probe`, `probe2`, `deepfluoro`,
`repro2`, `eval`, `identity`, `kernel_exp`, `diag`, `diag2`, `diag3`, `validate_gen`, `validate_render`,
`validate_fin`, `validate_submit`, ...), the untracked `polypose_cine.sh` (7,237 B, 2026-09-26; section 1 above) and
`polypose_cohort.sbatch`, `polypose_cohort_reduce.sbatch`;
`slurm/env/polypose.yml`, `polypose.requirements.lock.txt`, `polypose.freeze.txt`, `polypose.pose_flip.diff`,
`polypose.pose_flip_record.json`, `polypose.setup_status.json`; `ts_drr.sh`, `verse_totalseg.sh`;
`corpus_manifold.sh`, `corpus_expand.sh`, `paired_sets_properties.sh`; `row2_anatomy.sh`, `row3_overlap.sh`,
`row4_fluorohash.sh`, `row4_probe.sh`; the figure jobs `fig1_compose.sh`, `fig2_heldout.sh`,
`fig2_occlusion_clean.sh`, `fig3_example_v3.sh`, `fig6_tau_val.sh`, `fig_row5_corpus.sh`, `fig_row6_arch.sh`,
`figure1_panels.sh`, `figure1_spec.json`, `figure1_spec_t13.json`, `gallery_panels.sh`, `gallery_spec.json`.
The physics render stage itself is `slurm/fluorocap_v2.sh` (`STAGE=physics PSCHEME=ctsp|verse|totalseg|implant`),
referenced from project 01. The physics reproduction is the `Makefile` targets `physics`, `physics-tables`,
`physics-check` (`docs/HANDOFF_PHYSICS.md`).

### 1.7 Shared with other projects, named here because the renders depend on them

`tools/patient_keys.py` (every render inherits its CT's person; uncommitted edit on 2026-10-08), `tools/eval_gate.py`,
`tools/leak_check.py`, `tools/make_context_crops.py --patient-json`, `tools/merge_banks.py` (`real_share` 0.5, line
60), `tools/realxray_banks.json`, `tools/find_rare_cases.py`, `tools/make_implant_ct.py`, `tools/unseen_cases.py`,
`data_platform/reacquire/reacquire.py --grid <id>` (prints the runnable rebuild of `ctsp_drr`, `verse_drr`,
`physics_drr`, `physics_rare`, `ts_drr`, `ts_drr_v3`, `devcorpus`).

## 2. CTSpinoPelvic1K (public)

- URL `https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K.git` (`origin`) and
  `https://github.com/OpenSpineConsortium/CTSpinoPelvic1K.git` (`osc`); branch `master`; commit `7ddfe38`
  (2026-09-28). Push to both.
- What this folder needs from it: the v11 labels on the grid (identifier 29 retired) for every CTSP render; the
  case-id convention (`zfill(4)`); `paper/mpda/REPRODUCE.md`; `docs/SPINOPELVIC_ESTIMATOR.md` (the plate fits that
  `measure_sagittal.py` reproduces). The untracked `infobot/` under its root is referenced by path only
  (`MANIFEST_LOCAL.md`).

## 3. OpenSpineToolkit (public)

- URL `https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit.git` (`origin`) and
  `https://github.com/OpenSpineConsortium/OpenSpineToolkit.git` (`osc`); branch `main`; commit `cb43197` (2026-09-25).
- `ostk/labels.py` line 135 `labels_for(volume=None, *, scheme=None, counts=None)`: the only way to resolve a label
  name; line 64 `LABELS_V10` still maps `"S1": 29` (catalog G.3, open). `ostk/vertebral_body.py` lines 98-132: the
  canal-closing regression of 1b7005c (G.2, open; do not trust post-commit VBHp / EPD).

## 4. XRSpinoPelvic1K (private)

- URL `https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K.git`; branch `main`; commit `4f22935` (2026-08-15).
- 6,416 lateral DRRs built from 822 cases of a pre-release export; its `data/ct` and `data/labels` links dangle;
  rebuild from v11 with `labels_for` before any reuse (`DATA_MANIFEST.md` section 4 row 36). `dataset2024.zip`
  (4.0 GB) is never copied.

## 5. spine-detector (private GitHub; no `.git` on the laptop copy)

- URL `https://github.com/OpenSpineConsortium/spine-detector` (private; `../_plan/PLAN.md` section 3, project 01
  "Repositories referenced" and project 07 "Grid paths it owns"); branch not recorded; commit not recorded: the
  laptop folder has no `.git` (`../_plan/PLAN.md` section 7) and the grid checkout `~/spine-detector` has a `.git`
  (`../_plan/PLAN.md` line 235) whose `HEAD` was not read in the 2026-10-08 pass. `TODO.md` step 25 reads it in the
  next read-only grid pass and writes the commit here.
- The detector runtime whose `runs/devcorpus/` on the grid holds the styled-corpus detectors; project 01 carries the
  `src/` snapshot. Its corpus is migrating under B04.

## 6. Third-party code pinned by this folder

- PolyPose `github.com/eigenvivek/polypose` at `909a9bb2eeccf05065c7bc1d3703fb99f87b35b9` (MIT), `xvr` at
  `3e0b26eb51ef4a9c37615611bb05e0e200e48092`; env hash `f94fd57e...`, python 3.10.21, uv 0.12.18, apptainer 1.2.2
  (`results/polypose/REPRODUCTION.md`; `slurm/env/polypose.*`).
- DeepFluoro data: Hugging Face `eigenvivek/xvr-data` revision `a17273e3eadbd793bd861f3598a80ce4590c1124`
  (byte-identical to the H5 specimens; `results/polypose/REPRODUCTION.md`).


## 6. SpineSurg-CT (public) at 0051074: the sacralisation-synthesis line of March-April 2026 (added in the final pass of 2026-10-08)

| item | value |
|---|---|
| URL | https://github.com/Gregory-Schwing-MD-PhD/SpineSurg-CT (the laptop nested clone's `origin`) |
| commit | 0051074 ('up', 2026-04-09; `git log -1` of `<laptop:Desktop>/SpineSurg-CT/SpineSurg-CT/`, 2026-10-08); branch not recorded in this pass |
| files that matter | `src/augmentation/sacralization_synthesis.py` (22,908 B), `src/utils/augmentation_qc.py` (43,384 B), `src/utils/pelvic_alignment_qc.py` (28,049 B), `src/utils/pelvic_grid_panel.py` (29,067 B), `slurm/run_augmentation_qc.sh` (3,937 B); all five copied to `code/spinesurg_ct_0051074/` |
| result | `augmentation_quality_report.csv` (1,488 B) and `augmentation_quality_summary.txt` (1,023 B), laptop-only under `<laptop:Desktop>/SpineSurg-CT/augmentation/metrics/` (outside the nested clone), copied to `results/superseded/sacralization_synthesis_2026-04/` |
| role here | the ancestor of CTSpinoPelvic1K-Syn (project 06) and of the PolyPose / morphology-synthesis work; superseded, kept as lineage; its label ids are the 2026-04 scheme, not v11 |
| also named by | `../03_ctspinopelvic1k_dataset/MANIFEST_CODE.md` (the repository, for `metadata_colonog.csv` and `data_split.txt` only) |

### Section 1 addendum: copies now held here

The nine scripts of section 1 with a copy in `code/ssn_097933a/` are `tools/render_physics_drr.py`, `make_drr_dataset.py`, `spine_project.py`, `device_fit.py`, `device_style.py`, `device_spread_sweep.py`, `deepfluoro_calibrate.py`, `polypose_sample.py`, `polypose_warp.py` (byte-identical to 097933a; `MANIFEST_LOCAL.md` final pass). The two untracked files of the working tree, `tools/polypose/cine_render.py` and `slurm/polypose_cine.sh`, are in `code/ssn_untracked_2026-10-08/`; `TODO.md` step 2 commits them.
