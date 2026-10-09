# MANIFEST_CODE.md: every code repository this project uses

Nothing that lives in a repository is copied into this folder except the handful of files under
`code/` (each with its source commit in a header) and the documents under `docs/`. A reader with
grid access and these repositories can continue the work. Commits are as read on 2026-10-08 with
`git log -1` on the laptop checkouts; the grid checkouts may be behind (section 7).

## 1. `spinesurg-ct-nnunet` (private)

- URL: `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` (private since 2026-09-14;
  `memory/fluorocap-repo-private.md`). Branch `L6_Class`, commit **097933a** (2026-10-08). Working-tree
  edits at that commit, uncommitted: `tools/carmlspine_eval.py`, `tools/level_prototype.py`,
  `tools/patient_keys.py`, `tools/pipeline_state.py`, `tools/test_patient_keys.py`; untracked:
  `tools/transitional_review/`, `tools/fluoro_video/`, `tools/carm_sweep.py`, `tools/cine_eval.py`,
  `tools/cine_latency.py`, `tools/bournemouth_qf_eval.py`, `tools/polypose/cine_render.py`,
  `HANDOFF/GREG_ONLY/` (`git status` 2026-10-08).
- Grid checkout: `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` at 4e3fe93, behind the laptop and
  unable to fetch (OPEN_QUESTIONS B32); ship changes by `git archive | ssh tar`; never `make physics*`
  (it hard-resets) (`docs/handoff/RECIPES.md` section 0).

Files that matter for this folder (all tracked at 097933a unless marked):

| file(s) | what |
|---|---|
| `HANDOFF/` (12 documents, `context/`, `literature_state/`, `working_notes/`) | the 2026-10-08 handoff; the 12 documents, `literature_state/` and `working_notes/` (without `builders/`) copied into `docs/handoff/`, the 36 context notes of this folder's cut lists into `memory/`; `HANDOFF/GREG_ONLY/` is untracked and never copied (referenced by path from folder 01) |
| `tools/context_ladder.py` | how much spine a model needs to see to name a level (the ladder: full, 16, 12, 8, 6, 4, 2, 1 vertebrae; masking, not cropping); copied to `code/` |
| `tools/eval_shortcut_controls.py` | the negative controls with pre-written falsifiers (`permute`, `anatomy`, and the rest of its docstring); copied to `code/` (133,178 B) |
| `tools/{collect_context_curve, eval_interior_windows, eval_anchor_free, eval_windows_by_class, eval_fov_separability, eval_multiview, eval_raw_films, eval_error_taxonomy, eval_surgeon_benefit, eval_feasibility_claims, eval_scaling_curves, eval_level_flags}.py` | the plain-film evaluation line of 2026-09-12 to 09-22 (interior windows, feasibility claims, the superseded scaling curves) |
| `tools/{subset_bank, merge_banks, merge_ctx, build_allspine_v3, build_v6_bank, build_crest_bank}.py` | bank builders; `merge_banks.py` line 31 `--real-share` (default 0.5, used at line 60) is the flag the never-run ratio sweep would vary; `subset_bank.py` returns at once on `READY` (line 52) |
| `tools/{common_testset_eval, coverage_arms, train_competitors, ensemble_eval, ensemble_report, benchmark_cina, buu_baseline}.py` | the re-implemented published competitors (ours, Cina, Kim, VertX, Konya; design `docs/COMPETITOR_BENCHMARK.md`; result NOT RECORDED, C1.17) and the Cina whole-film benchmark (C1.16) |
| `tools/{train_role_head, role_ablation_report, train_contour_pointnet, make_contours, robustness_eval, train_lumbar_focus, train_orientation, train_view_classifier}.py` | the model-night arms (C1.9, C1.10) |
| `tools/{level_heatmap, level_logit_dump, level_posteriors, diag_level_model, bank_region_profile, c2_anchor_status, probe_c2_lands_on, probe_first_field}.py` | level-model diagnostics |
| `tools/{make_feasibility_figures, make_report, make_results_table, make_count_figures, make_sweep_figure, make_verify_bench, make_reading_set, lock_adjudication}.py` | figure and report makers; `make_feasibility_figures.py` lines 429-451 draw `fig9_scaling` (whether drawn: not recorded) |
| `tools/{aasce_to_drr, mendeley_to_render, spinal_ai2024_to_render, nhanes_box_convention, nhanes_to_drr_format, manifest_to_drr_format, check_level_naming, rib_bearing_ann}.py` | the film-corpus converters into the render format (`films_drr` is built from the spine-detector manifest by `manifest_to_drr_format.py`) |
| `tools/{corpus_xray_gate, corpus_xray_gate_contact, corpus_xray_gate_eval, corpus_xray_modality_cheap, corpus_xray_modality_vlm}.py` | the FluoroCap X-ray gate (its outputs `logs/xray_gate/` are untracked; by path in `MANIFEST_LOCAL.md`); FluoroCap is out of training (directive D1) |
| `tools/lumbar_*.py` (9 files), `tools/track5_*.py` (6), `tools/night_*.py` (8) | the mid-lumbar diagnosis (`results/lumbar_diag_2026-09-16/`), the Track 5 band-transfer line (`results/track5_results/`), the model-night driver (counts by `git ls-files` at 097933a; the inventory said 8 / 6 / 9) |
| `tools/{pseudolabel_films, pseudolabel_real_films, filter_pseudolabels, apply_review_corrections, build_review_pack, build_quiz_pack, build_reader_study, make_reviewer_codes, deploy_review_space, smoke_reader_study, smoke_review_sites, student_correction_pack, student_correction_score, panel_contamination_audit, panel_disagreement_sheet, panel_label_audit, panel_region_arbitration, panel_vs_film_stats}.py` | pseudolabelling of unlabelled films, the review and reader-study packs and Spaces, the FluoroCap panel audits |
| `review_space/{README.md, SPACE_README.md, app.py, Dockerfile, requirements.txt}` | the student film-review Space; copied to `code/review_space/` |
| `track5_results/` (9 text files), `lumbar_diag_2026-09-16/` (JSON, csv, txt, `render/`) | copied to `results/` (the four `render/*.png` by path) |
| `tools/film_ncurve.py`; `SchwingNet/slurm/{film_ncurve_prep, film_ncurve_encoder, film_ncurve, film_ncurve_collect, film_ncurve_ablation, film_ncurve_ablation_collect}.sh`; `SchwingNet/tools/{film_ncurve_ablation_read, make_supp_ablation_table}.py`; `SchwingNet/results/coverage/film_ncurve/{film_ncurve.json, FILM_NCURVE.md, cells.json, ablation/READ.md, ablation/ablation_read.json}`; `SchwingNet/results/coverage/{pooled_fit.json, PER_LEVEL_DOMAIN_ANGLE.md, PENDING_JOBS.json}` | the film N-curve and the render ablation (A10): owned by folder 01, cited here |
| `tools/eval_gate.py`, `tools/patient_keys.py` (edited, uncommitted), `tools/rigor_fixes.py` (`a5-rows`), `tools/head_mixed_length.py` | the evaluation gate every quoted score passes through; person keys (`key_any`: one CSXA film = one person; one four-digit BUU case = one person; NHANES by film number); the mixed-length head |
| `slurm/recurrent_head.sh` line 16; `tools/recurrent_order.py` line 56 | **say `films_all2` where the result was measured on `films_ann`** (C1.2; OPEN_QUESTIONS F5; TODO step 2) |
| `slurm/scaling_sweep.sh`, `slurm/night_arm.sh`, `tools/train_level_backbone.py` (lines 516-520) | the 2026-09-17 fraction sweep and why a rerun is both unsafe and a selection-split number (RECIPES section 1.8; OPEN_QUESTIONS F21) |
| `slurm/{night_*(11), scaling_sweep, eval_scaling_curves, interior_*(2), iso_rung_control, v3_arms, v4_arms, v5_*(2), v5c_chain, v6_chain, overnight_v7, allspine_bank, allspine_v2_*(2), build_allspine_v3, build_allspine_v4, anchor_c2, anchor_free, all_arms_real_films, arms_table_refresh, box_repair_ab, buu_baseline, benchmark_cina, aasce_*(2), nhanes_*(2), plainfilm_recount*(2), recount_*(2), vo_eval_nhanes, ctx_eval_nhanes, fov_separability, global_signature, explain, learning*, stc_arm, role_head, track5_*(5), zoom_fluoro_*(3), det_conf_sweeparm, detector_*(3), fleet_best, regression_baseline, smoke_*(2), review_pack*, rebuild_review_pack, quiz_pack, reader_study, fluorocap_*(12), hires_refresh, panel_stats, leads_chain, thoracic_widen}.sh` | the pre-SchwingNet film arms, the deleted v2-v7 banks' chains, the FluoroCap chains, the review-pack and reader-study deploys (578 tracked `slurm/*.sh` at 097933a; `fluorocap_*` 12 by `git ls-files`, the inventory said 14) |
| `tools/xray_dataset_usage.py` | the dataset-usage table; carries the `buu_2000` mislabel and substring keys (OPEN_QUESTIONS F7) |
| `tools/correct_buu_schema.py`, `tools/film_corpus_inventory.py` (`YOLO_BANKS`) | the BUU schema correction (`films_drr_buucorr`) and the film corpus inventory (job 40416535) |
| `docs/MANIFEST_DATA_MODELS_RESULTS.md` (sections 1.1, 2.1, 2.3, 5.2, 5.3, 7.1, 7.2, 8) | the record of the early film models and banks, the XRSpinoPelvic1K DRR set (6,416 lateral DRRs of 822 cases, line 198) and the detector versions |
| `docs/{COMPETITOR_BENCHMARK, NHANES_DOUBLE_INCLUSION_2026-09-22, MODEL_CARD, DATASHEET, DATA_COMPLETENESS_AUDIT, PATIENT_IDENTITY_SPEC, FEASIBILITY_REPRODUCE, STUDENT_FLUORO_CORRECTION_GUIDE}.md` | the design and audit documents cited by `STATUS.md` rows; `STUDENT_FLUORO_CORRECTION_GUIDE.md` is copied into folder 01 |
| `data_platform/{DATA_MANIFEST.md, MIGRATION_PLAN.md, LAYOUT.md, VERIFICATION.md, sources.json, plan/batch_items/B04.tsv, B05.tsv, B10.tsv, B11.tsv, plan/migration_batches.csv, dedup/}` | the source cards (`spine_detector_corpus`, `xrspinopelvic1k`, `buu_lspine_3600`, `buu_lspine_2000`, `csxa_cervical_xray_atlas`, `nhanes2_cdc_films`, `nhanes2_zenodo_landmarks`, `vindr_spinexr`, `aasce2019_boostnet`, `mendeley_5jdfdgp762`, `ieee_dataport_lateral_fullspine_236`, `spinal_ai2024`, `cm_spine_drive_file`) and the batches `MANIFEST_GRID.md` is cut from; owned by folder 10 |

## 2. `XRSpinoPelvic1K` (private)

- URL: `https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K`. Branch `main`, commit
  **4f22935** (2026-08-15, "annot: check the two-head rule the guide has always stated"); 124 commits
  since 2026-06-24; 129 tracked files; in sync with origin on 2026-10-08. Made private on 2026-09-26
  because it held `localize.py` and a Cerner `.ica` file (`docs/handoff/MANUSCRIPTS.md` section 10).
- Grid checkout: `/wsu/home/go/go24/go2432/XRSpinoPelvic1K` (2026-08-10; `MANIFEST_GRID.md` section 1).
- **Tracked at 4f22935 and to be purged from history**: `Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica`
  and `Unconfirmed 31234.crdownload` (TODO step 1). Five more `.ica` files are untracked beside the
  laptop checkout.
- Code: Apache-2.0 (`LICENSE`, `NOTICE`); rendered DRRs inherit CTSpinoPelvic1K's CC BY-NC 4.0
  (`docs/xrspinopelvic1k/docs/dataset_card.md`).

| file(s) | what |
|---|---|
| `README.md`, `CITATION.cff`, `docs/{RESULTS, ROADMAP, PIPELINE, HPC, dataset_card, reader_study_protocol}.md`, `docs/reader_measurements_template.csv`, `docs/figures/{drr_0001, drr_0003}.png`, `annot/README.md` | copied into `docs/xrspinopelvic1k/`; `docs/figures/phase0_buu_*.png` by path (BUU pixels) |
| `xrsp/oblique.py` | arbitrary-angle DRR with labels re-projected through the identical geometry; four corners per vertebra; `sample_view(rng, yaw_deg=12, pitch_deg=8, roll_deg=6)` |
| `xrsp/project_labels.py`, `xrsp/drr.py`, `xrsp/build_dataset.py` (`--oblique N`) | 3-D masks to 2-D footprints and per-level landmarks; parallel-beam DRR; the dataset builder |
| `xrsp/measure.py`, `xrsp/unified.py`, `xrsp/hipfit.py`, `xrsp/femhead.py` | PI / SS / PT / LL from landmarks; the unified model; the classical circle fit (unusable: "converged" on 301 / 301); the femoral-head head |
| `xrsp/splits.py`, `xrsp/dataset.py`, `xrsp/heatmaps.py`, `xrsp/model.py`, `xrsp/evalmetrics.py`, `xrsp/evalplots.py`, `xrsp/geom_aug.py`, `xrsp/labels.py`, `xrsp/localize.py`, `xrsp/buu.py` | splits (patient-grouped, LSTV-stratified, leakage assertion), loaders (letterboxed since the anisotropy fix), the heatmap model, the one metric implementation every number in RESULTS.md shares |
| `scripts/{buu_to_yolo, train_yolo_pose, evaluate_yolo, tabulate_experiments}.py`; `slurm/xrsp_yolo.sh` | the YOLO-pose corner detector: Bansal Table 4 hyperparameters with every augmentation zeroed; conversion verified by round trip to 0.0014 px (RESULTS.md section 6) |
| `scripts/{standing_scale_sweep, extrapolate_above_l1, buu_convention, make_buu_splits, fetch_buu, drr_to_yolo, evaluate, evaluate_buu, evaluate_unified, hip_agreement, make_reader_set, make_splits, measure_pi, measure_pi_unified, render_failures, train_corners_buu, train_femhead, train_landmarks, train_localizer, train_unified, validate_hip_circlefit, generate_case, smoke_test, smoke_union, upload_xrsp1k, ship_xrsp1k.sh, build_and_push.sh, gen_xrsp1k.slurm, make_reader_set.slurm}` | the standing-framing sweep (4b), the extrapolation test (4c), the BUU convention check against BUU-LSPINE 400, the reader set, the uploader (the Hugging Face repository id is passed on the command line; none recorded) |
| `annot/` (Space: Docker, HF OAuth; `seed_cases.py`) | the two-click femoral-head annotation Space; no automatic proposal is ever shown; two annotators per film, agreement at 2 % of image width |
| `data/buu_splits.json` (on the grid, 53,434 B) | the frozen 1398 / 301 / 301 split; every number in RESULTS.md rests on it; never regenerate silently |
| `Makefile`, `docker/`, `containers/`, `nextflow/` | `make image` (Docker Hub `gregoryschwingmdphd/xrspinopelvic`), `make container`, `make generate / splits / train / eval / eval-buu / reader-set` (HPC.md); **`OSTK_REF` defaults to 09dd9c5** (the first OpenSpineToolkit `main` commit with `ostk.drr` + `ostk.project2d`); a change there moves every label |

## 3. `OpenSpineConsortium/spine-detector` (private)

- URL: `https://github.com/OpenSpineConsortium/spine-detector` (private). Commit: **not recorded**;
  the live tree with `.git` (2026-09-12) is the grid checkout `/wsu/home/go/go24/go2432/spine-detector`;
  the laptop snapshot (files 2026-09-01 to 2026-09-12) has no `.git`. Whether the GitHub repository
  equals the grid tree is not recorded (plan section 7).
- The snapshot's `src/` is copied into `01_carm_level_detection/code/` because the runtime needs
  `manifest.py::canonical_slots` (`_plan/PLAN.md` section 4); this folder holds the `report/` of the
  same snapshot under `results/spine_detector_report/`.

| file(s) | what |
|---|---|
| `src/train.py` | YOLO11m-pose, class-agnostic vertebra with four corners, imgsz 1024; **`fliplr=0.0` and `mosaic=0.0`**: a horizontal flip swaps the anterior / posterior corner slots and the head silently fails to converge (docstring) |
| `src/build_dataset.py`, `src/converters/{buu, mendeley, nhanes}.py` | converters per source; levels never invented (annotated / inferred_from_position / unknown recorded per instance in `level_source`) |
| `src/ignore.py` | ignore-region loss mask, written but not wired in at report time (the report states the missing ablation) |
| `src/run_eval.py`, `src/evaluate.py`, `src/render_prediction.py`, `src/manifest.py`, `src/normalize.py`, `src/export_onnx.py`, `src/export_yolo.py`, `src/check_fp16_*.py`, `tests/test_manifest.py` | the 558-instance held-out evaluation, the renders in `results/spine_detector_report/renders/`, the manifest and its slot convention, the ONNX export (the exports themselves are weights: never copied; removed from the public website on 2026-09-14) |
| `report/{build_report.py, make_assets.py}` | copied; `make_assets.py` reads `manifest.parquet` and `renders/` into `assets.json`, `build_report.py` assembles `report.html` from it (the copy in this folder was regenerated from the redacted `assets.json`) |
| `scripts/download_sources.py`, `scripts/make_zoom_dataset.py` | grid-only raw downloads; the zoomed windows of `yolo_v4z` |

## 4. `CTSpinoPelvic1K` (public)

- URLs: `https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K` (`origin`) and
  `https://github.com/OpenSpineConsortium/CTSpinoPelvic1K` (`osc`); push to both. Branch `master`,
  commit **7ddfe38** (2026-09-28); working tree modified on 2026-10-08. Release v11 on Zenodo
  10.5281/zenodo.22797014 (concept DOI 10.5281/zenodo.22139642); owned by folder 03.
- Files that matter here: `CLAUDE.md` (the label-scheme and orientation traps), `paper/mpda/REPRODUCE.md`,
  `docs/SPINOPELVIC_ESTIMATOR.md` (the ostk defects the film spinopelvic numbers inherit),
  `docs/LEVEL_MORPHOMETRY.md`, `morphometrics/`, `tools/`, `zenodo/`. The scratchpad results copied
  into `results/corner_detector_buu/` and `figures/buu_vs_drr/` came from its working tree
  (`MANIFEST_LOCAL.md`); the laptop folder also holds the film datasets referenced by path there.

## 5. `OpenSpineToolkit` (public)

- URLs: `https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit` and
  `https://github.com/OpenSpineConsortium/OpenSpineToolkit`. Branch `main`, commit **cb43197**
  (2026-09-25). Owned by folder 04. The grid copy has no `.git`; rsync it again from cb43197 when
  needed.
- Files that matter here: `ostk.labels.labels_for(volume)`; `ostk.project2d`, `ostk.drr` (first on
  `main` at 09dd9c5, the `OSTK_REF` XRSpinoPelvic1K pins); `ostk.spine.endplate_corners` (medial band
  + outlier rejection, which drops the sacral ala); `ostk.metrics2d` (SS / LL / PI / PT from corners;
  the BUU numbers in RESULTS.md section 2 are computed with it). Open defect: the canal-closing
  regression of 1b7005c inflates posterior body height and end-plate depth by 10-17 mm on about one
  vertebra in seven (`RESULTS_CATALOG.md` G.2-G.3; folder 04's fix blocks any 3-D twin of the film
  numbers).

## 6. Hugging Face repositories named by this folder (not checked; no network was used)

| repository | role | named in |
|---|---|---|
| `gregoryschwingmdphd/level-review-ledger` (dataset, private) | the review Space's decision ledger; `tools/apply_review_corrections.py` reads it | `code/review_space/README.md` |
| the private film repository and Space of the review tool; the femoral-head annotation Space (`<org>/xrsp-femhead-annot`, `<org>/xrsp-femhead-images`, ids never recorded in the repository) | the review and annotation Spaces | `code/review_space/README.md`; `docs/xrspinopelvic1k/annot/README.md`; the exact ids of the review Spaces are in the memory note `review-space-repos` carried by folder 11 |
| `gregoryschwingmdphd/level-id-weights` (private) | the model-registry mirror | `MANIFEST_GRID.md` section 4 |
| `gregoryschwingmdphd/xrspinopelvic` (Docker Hub image) | the XRSpinoPelvic1K container | `docs/xrspinopelvic1k/docs/HPC.md` |

## 7. What the commits do not settle

- The commit of the spine-detector snapshot whose `report/` is copied here (not recorded).
- Whether the grid `~/spinesurg-ct-nnunet` (4e3fe93) carries the `tools/` and `slurm/` versions that
  produced the RECORD ONLY rows (OPEN_QUESTIONS B17).
- Who wrote the XRSpinoPelvic1K corner projection and whether its corners were validated against a
  reader (RESEARCH_DIRECTIONS unknown 25): `scripts/buu_convention.py` compares scale-free quantities
  against BUU-LSPINE 400 readers (`wedge_L5` out of band: 13.6 against 0.4-10.6, README), not corner
  for corner.
