# Inventory 1: `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet`

Read on 2026-10-08 from the laptop only (`ls`, `du`, `git`, `head`, `grep`). Nothing was run on the grid and no
credential file was opened. Every count below names where it came from. The row-level inventory is
`spinesurg_ct_nnunet.tsv` beside this note (209 rows, eight columns).

## 1. What the folder is

The private repository of the whole C-arm / film level-identification programme and of the data platform, plus
the handoff written today. Repository `github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` (`git remote -v`;
one remote, `origin`), private since 2026-09-14 (`HANDOFF/context/fluorocap-repo-private.md`). It began on
2026-04-18 as the nnU-Net training pipeline for CTSpinoPelvic1K (`CITATION.cff` date-released; first commits of
`tools/`, `slurm/`, `docs/`, `containers/`, `nnunet/`), became the FluoroCap and plain-film level-ID project on
2026-09-12 to 09-16, the C-arm sweep / physics / device line on 09-17 to 09-22, SchwingNet (paper 1 and 2) on
09-22 to 09-27, and the data platform and handoff on 2026-10-08 (`git log` first/last dates per folder, listed in
section 3).

| fact | value | source |
|---|---|---|
| branch, HEAD | `L6_Class`, `097933a` 2026-10-08 "HANDOFF: the handoff for a new student or a fresh Claude project" | `git log -1` |
| tracked files | 8,099 | `git ls-files | wc -l` |
| tracked per top folder | SchwingNet 4,820; tools 751; tmp 653; slurm 594; spine_data_review 272; HANDOFF 184; data_platform 181; docs 180; paper 152; results 86; benchmark 78; tests 32 | `git ls-files` by first path element |
| size on disk (excluding .git) | SchwingNet 2.1 GB; spine_data_review 1.8 GB (runs/, gitignored); tmp 40 MB; paper 36 MB; tools 29 MB; logs 22 MB; docs 20 MB; data_platform 9.8 MB; everything else under 5 MB each | `du -sh --exclude=.git *` |
| modified, uncommitted | 17 files: `tools/{carmlspine_eval,level_prototype,patient_keys,pipeline_state,test_patient_keys}.py`, `benchmark/{run_spineps_cases,run_spineps_ribs,spineps_to_oneshot}.py`, six `spine_data_review/` files, two `SchwingNet/packet_build/reference*.docx`, `grep.exe.stackdump` | `git status --porcelain` |
| untracked | 52 entries: `HANDOFF/GREG_ONLY/`, 15 packet PDFs + 6 logs in `SchwingNet/packet_build/`, `SchwingNet/results/{cine/,polypose/rom_cine.json,reader_e/smoke/}`, `benchmark/{run_spineps_patched,spineps_cc3d_patched}.py`, 8 `docs/*.md` (BOURNEMOUTH_QF_HARNESS, CINE_DEMO_BUILD_PLAN, CINE_DEMO_RECON, FLUORO_CINE_DATA_REQUESTS_DRAFT, FLUORO_VIDEO_REQUESTS_READY, FLUORO_VIDEO_SOURCES, FLUORO_VIDEO_YOUTUBE_SCAN, REVIEW_TRANSITIONAL) + `docs/fluoro_requests_eml/`, 5 `slurm/*.sh` (carm_sweep_case39, carm_sweep_regress134, cine_eval, cine_latency, polypose_cine), `tools/{bournemouth_qf_eval,carm_sweep,cine_eval,cine_latency}.py`, `tools/fluoro_video/`, `tools/polypose/cine_render.py`, `tools/transitional_review/`, `spine_data_review/runs/2026-09-23/`, two review tests, `pyflakes-4.0.0-*.whl` | `git status --porcelain` |
| grid checkout | `~/spinesurg-ct-nnunet` on go2432's HOME; the grid can no longer fetch the private repository (2026-10-08, cause not recorded); code ships by `git archive | ssh tar`, the shipped commit appended to `SHIPPED_COMMITS.txt` | `HANDOFF/RECIPES.md` section 0.2 |

What a reader would lose if the folder were dropped: the only copy of the SchwingNet manuscript and its
result-to-text audit chain, the frozen paper-2 comparator and reference standard, the transitional registry
(6,108 persons), the device cards, the data manifest of 211 sources and the migration plan, the handoff itself,
and about 1,300 scripts of which no grid copy is complete (the grid checkout is behind HEAD and never held the
untracked files). The CT dataset itself is not here (it lives in CTSpinoPelvic1K-1, on Zenodo and on the grid).

## 2. Which project family each part belongs to

The handoff names three projects (CTSpinoPelvic1K, SchwingNet, OpenSpineToolkit) and three cross-cutting
threads (the anomaly scan, the data platform, Beethoven) (`HANDOFF/README.md` section 1). Against the twelve
families of this seed the folder divides as:

| family | what in this folder | rows in the TSV |
|---|---|---|
| **carm_detection** | `SchwingNet/` (paper 1, its results, figures, tables, packets), `docs/` model card, datasheet, deployment evidence, physics/linking, sweep-count-confirm, prior art, cine harness, data requests, `service/`, `results/physics/`, `paper/rsnai/` and `paper/focused/` (superseded drafts), the pipeline tools (`level_prototype.py`, `eval_gate.py`, C-ArmLSpine, real-frame detectors, learning curves), `HANDOFF/` | 102 |
| **transitional_fluoro** | paper 2 (`SchwingNet/paper2_levelcheck/`, `LEVELCHECK_MODEL.md`, `results/fig6/`, `auto_reference/`, `dual_loss/`, `rare_class/`, `learning/`), `reader_space/`, the rare-class and transitional-detector tools, `LITERATURE_STATE.md` + `literature_state/` | 13 |
| **render_devices** | device cards (`docs/devices/`), DEVICE_PARAM_AUDIT, DeepFluoro calibration, PolyPose, FluoroGen, the manifold, `research_notes/`, `reports/`, about 90 `deepfluoro_* / device_* / cobra_* / spinesac_*` tools | 13 |
| **anomaly_scan_census** | the transitional registry, `docs/ruleclass/`, CT_LSTV_CLASSIFIER_PLAN, CENSUS_TABLE, REVIEW_TRANSITIONAL, `lit/ct_lstv_classifier/`, `disputed_renders/`, the acquisition / harvest / registry tools and `tools/transitional_review/` | 10 |
| **data_platform** | `data_platform/` entire, `HANDOFF/LEAKAGE.md` + `INFRASTRUCTURE.md`, DATA_ACCOUNTING, DATA_COMPLETENESS_AUDIT, PATIENT_IDENTITY_SPEC, the SPINEPS id census, the leak-check and inventory tools and their tests, `spine_data_review/` (the dataset scoping review), `env/`, grid job records | 25 |
| **ctsp_dataset** | the April-June nnU-Net era (`scripts/`, `containers/`, `docker/`, `data/README.md`, nnU-Net tools and slurm), `benchmark/` (CT competitors), BENCHMARK_PROTOCOL, ablations | 10 |
| **ct_morphometry_parity** | `results/reader_e/` (ostk morphometry as reader E; the diag renders that found the canal-closing regression), `pelvis_landmarks.py`, `plan_postop.py` | 3 |
| **plain_film_level_id** | the 2026-09-12 to 09-22 film line: `track5_results/`, `lumbar_diag_2026-09-16/`, `review_space/`, `logs/xray_gate/`, the context-ladder / interior-window / competitor / model-night tools and slurm | 8 |
| **qi_wrong_level** | `paper/qi_universal_protocol/`, WRONG_LEVEL_COST_EVIDENCE, WRONG_SITE_BURDEN_EVIDENCE, the `review_*.py` scoping-review tools | 4 |
| **archive** | FluoroCap (docs, 80 `fluorocap_*` tools, 14 slurm chains, `benchmark/data/fluorocap_v0.1`), the `hunt_*` image harvesters, older dated resumes, licence files | 9 |
| **exclude** | junk at the root, caches, the stray mangled-path folder, `tools_tmp_sync/`, `reader_space/_original_space/`, `HANDOFF/GREG_ONLY/` (reference only) | 12 |
| toolkit, grid_access_students, website | nothing of substance lives here; the Beethoven notes sit in `HANDOFF/GREG_ONLY/context_beethoven/` (six notes) and point to their own repositories; `docs/pacs*` does not exist here | 0 |

## 3. Folder by folder

Dates are first and last commit touching the folder (`git log --diff-filter=A` / `git log -1`).

### 3.1 `SchwingNet/` (2026-09-22 to 09-27; 4,820 tracked files; 2.1 GB)

Paper 1 and everything that feeds it, assembled on 2026-09-22 from the rigor audit and built only from numbers
that pass it (`SchwingNet/README.md` first paragraph). Since 2026-09-24 evening paper 1 is five figures and three
tables; the LevelCheck / surgeon comparison is paper 2 in `paper2_levelcheck/` (`README.md` "State since
2026-09-24"; `PAPER1_SCOPE.md`).

| subfolder or file | what | current or superseded | copy or reference |
|---|---|---|---|
| `main.tex`, `sections/`, `supplement.tex`, style files, `refs.bib` | the manuscript | CURRENT (last 2026-09-25/27); one placeholder (VinDr determination), supplement 13 pages vs 12 cap, held from submission pending the TTO (`MANUSCRIPTS.md` 2.3, 2.6, 2.7) | copy |
| `numbers_manifest.json` -> `tools/results_macros.py` -> `generated/` | the results-driven build (`\RESULT{key}`; 79 resolved, 0 pending 2026-09-27) | CURRENT; the house pattern (`RESULTS_BUILD.md`) | copy |
| `NUMBERS.md`, `CLAIMS_LEDGER.md`, `CLAIM_CHECKLIST.*`, `PAPER1_SCOPE.md`, `TITLE.md` | number trace, claims map, CLAIM 2020 | CURRENT | copy |
| `LEVELCHECK_MODEL.md` | paper 2 comparator, FROZEN 2026-09-23 | CURRENT, frozen | copy (never edit) |
| `LEVELCHECK_CLAIM.md`, `FINAL_CHECK.md`, `atlas/` cards, `packet/`, `packet_cameraready/` | earlier claim table; 09-22/23 check; ATLAS cards; Word packets of 2026-09-25 | SUPERSEDED or STALE (`MANUSCRIPTS.md` 2.2, 2.6) | reference (packet 89 MB each) |
| `REVIEW*`, `REVISION_LOG1-3` | internal reviews and change logs | history, CURRENT as record | copy |
| `figures/` (104 files, 210 MB) | figures 1-5, S1-S4, Figure-1 panels, gallery; PNG + PDF + caption + record.json; TIFFs | CURRENT; Figures 3 and 4 marked PENDING GREG'S VERDICT in `FIGURES.md` (that table predates the 09-24 restructure) | copy PNG/PDF/caption/record; exclude .tif (figure1.tif 39 MB) |
| `tables/` (34 files, 6.7 MB) | Tables 1-3, S1-S4 with `.sources.md` | CURRENT; `.md` twins of Tables 2 and 3 stale, `tabS4_ablation` lacks twins (`OPEN_QUESTIONS.md` F4) | copy |
| `results/` (102 entries, 1.5 GB) | see the table below | mixed | selective |
| `packet_build/` (46 files, 253 MB, untracked) | grid-built PDFs; the two of 2026-09-27 are the manuscript as last compiled (jobs 40483839 / 40483840, commit 05e05dc; `RESULTS_CATALOG.md` status words) | the 09-27 pair CURRENT; 16 earlier PDFs superseded | copy the two 09-27 PDFs only |
| `packet_src/` (2.2 MB) | front matter, statements, cover letter, supplement_technical.tex, `persons_available_2026-09-24.json` (the seven real at-risk persons), CLAIM 2024 map, `build/BUILD_REPORT.md` | CURRENT | copy |
| `paper2_levelcheck/` (3.9 MB) | `MOVED_FROM_PAPER1.md` (verbatim passages with file and line at dd8f4a5), the moved manifest keys, `tables/tab_levelcheck.*`, `open_gate_40438004/` (open gate scored names only; path bug in `tools/fig6_score.py`, F3) | CURRENT for paper 2 | copy |
| `lit/` (5 MB) | `CITABLE_CLAIMS.md`; `ct_lstv_classifier/` (positives census: 93 read L6 persons; 88 after the five scan-contradicted VerSe reads) | CURRENT | copy |
| `tools/` (80), `slurm/` (101) | figure/table builders, packet, limits, paper-2 gate (`fig6_*`), reader E, `compile.sh` | CURRENT | reference; copy `results_macros.py`, `make_packet.py`, `check_limits.py`, `figure_set.py`, `fig_power.py`, `figure2.py` |
| `main.pdf`, `supplement.pdf`, logs | 2026-09-24 local compiles | superseded by packet_build 09-27 | exclude |

`SchwingNet/results/` by subfolder (file counts from `find`, sizes from `du`):

| subfolder | files, size | holds | family | disposition |
|---|---|---|---|---|
| top-level `a1..a9.json`, `rigor_fixes.json`, `RIGOR_FIXES.md`, `*_CHECK.md`, `counting.json`, `coupling.json`, `contribution_matrix.*`, `power_table.json`, `age_sex_by_source.*`, `corpus_census.*`, `anomalous_inventory.*`, `cobra_lstv_screen.*`, `JOBS*.txt` | small | every quoted paper-1 number traces here (`RESULTS_CATALOG.md` A1-A19) | carm | copy |
| `eval_gate/` | 268, 78 MB | `EVAL_LEAKS.md`, `EVALUATORS.md`, `LINEAGE.md`, `closure/MANUSCRIPT_CORRECTIONS.md`, cv_v9 re-runs; `touched.json` 55 MB | carm | copy all but `touched.json` |
| `coverage/` | 211, 182 MB | `PER_LEVEL_DOMAIN_ANGLE.md`, `COVERAGE.md`, `POOLED_FIT.md`, `PENDING_JOBS.json` (resume-vs-reproduce rule), `film_ncurve/ablation/READ.md` | carm | copy md/json/csv |
| `indomain/`, `counting/`, `lcurve/`, `arc/`, `cobra_window/`, `window_probe/`, `bodybox_rescore/` | 53+21+30+64+45+36+149 | learning curves, counting arms, angle sweeps, window diagnostics | carm | copy |
| `transitional_registry/` | 1,023, 360 MB | `REGISTRY.md`, `registry.csv` (6,131 rows -> 6,108 persons, L6 146, T13 14; `RESULTS_CATALOG.md` D.8), per-stream `SUMMARY.md` + `rows.csv`, `contact_sheets/` (26 JPG, 17 MB) | anomaly | copy the md/csv/json; renders by path |
| `fig6/` | 1,369, 132 MB | paper-2 gate records; `frozen/` (62 MB) and `verification/` (69 MB) are the byte-exact automated reference standard (`.gitattributes -text`) | transitional | copy top-level md/json; reference the frozen trees by path |
| `rare_class/`, `auto_reference/`, `dual_loss/` | 171 (21 MB), 28, 126 (22 MB) | `split_plan.md` (49 of 54 L6 val+test people are in the v8/v9 lineage, D.6), `transitional_subtypes.*` (194 persons), `CALIBRATION.md`, D1 saturation + 24 slurm logs | transitional | copy md/csv/json |
| `learning/` | 19, 147 MB | `LEARNING.md`, analyses (what the encoder learned, L6 confound); five `.npz` of 7-33 MB | transitional | copy md/json; exclude npz |
| `manifold/` | 31, 133 MB | `MANIFOLD.md`, pairwise separability CSVs; `deep.npy` 124 MB | render_devices | copy all but `deep.npy` |
| `reader_e/` | 211, 83 MB | reader E (ostk morphometry) code map, cases, timings, `diag/` renders; `features_j1.csv` 40 MB (the `.gz` twin is under 25 MB) | ct_morphometry_parity | copy all but the 40 MB csv |
| `spineps_ids/` | 123, 57 MB | the SPINEPS id census and repair (`CENSUS.md`, `IMPACT.md`, `REPAIRS.md`, `VERIFY.md`) | data_platform | copy md/json |
| `polypose/` | 111, 16 MB | `REPRODUCTION.md` (REPRODUCED), `SAMPLING_SPEC.md`, cohort files, `rom_cine.json` (untracked); `VALIDATION.md` does not exist (G.6) | render_devices | copy |
| `fig3_detection/`, `fig4_frames/`, `fig4_pairs/`, `fig5_frames/`, `figure1/`, `figure2/`, `gallery/`, `supplement_figs/`, `inputs/` | ~190 | figure inputs and local copies of grid inputs | carm | copy (figure2/ 23 MB: json/csv first) |
| `alpha_*`, `v9_seed*`, `coupling_*`, `repairs/`, `stats_review*/`, `power/`, `cine/`, `corpus_manifold/`, `alphabet_loss_inputs/` | small | seeds, checks, power.json (Figure 5a), `cine/tracker_config.json` frozen before any Bournemouth frame | carm | copy |
| `age_sex_cache/` | 19, 35 MB | cached per-source tables | carm | exclude (product is `age_sex_by_source.json`) |

### 3.2 `docs/` (2026-04-18 to 09-27; 135 entries, 180 tracked, 20 MB)

About 120 documents. The current ones for the hospital path: `MODEL_CARD.md` (43 KB; intended use, out of
scope, "the truth is two machines", runtime cost, what is not measured), `DATASHEET.md`,
`CARM_DEPLOYMENT_EVIDENCE.md` (one vendor route: Siemens Cios OpenApps, K181560 / K203504; no published compute
figure), `REAL_XRAY_DATASETS_SPEC.md`, `FLUORO_DATASET_STRATEGY.md`, the untracked cine set
(`CINE_DEMO_BUILD_PLAN_2026-09-26.md` names the primary weights stack in its section 0;
`CINE_DEMO_RECON_2026-09-26.md`; `BOURNEMOUTH_QF_HARNESS.md`: no Bournemouth frame scored yet), the data
requests (`FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `fluoro_requests_eml/` 11 drafts, `data_requests/`,
`outreach/`; all `requested_not_sent`, `MANUSCRIPTS.md` 16), `IRB/HPR_determination_VinDr-SpineXR_draft.md`
(regulatory; `[FILL]` marks remain), the five `PRIOR_ART_*.md`, `RESUME_2026-09-22_PM.md` (367 KB, the last
session checkpoint, newest block 2026-09-27 18:05) and `grid_records/JOBS_RECORD_2026-09-27_1544.*` (every job
cancelled that day and how to resume it).

Current for the other families: `DEVICE_PARAM_AUDIT.md`, `DEVICE_SPREAD_SWEEP.md`, `DEEPFLUORO_FORMATION.md`,
`devices/` (four fitted cards: bv_pulsera, cios_fusion, elekta_xvi, pixium_4600), `MORPHOLOGY_SYNTHESIS_PRIOR_ART.md`
(render_devices); `ruleclass/` (rescued 2026-09-27: `CLASSIFIERS.md` R1-R33 at 282 KB, `STUMP_RULE.md`,
`MORPH_API.md`, `ARM_B_pelvis.md`, `TIERS.md`, `PREREG_rules.md` DRAFT v1 unsigned), `CT_LSTV_CLASSIFIER_PLAN.md`
(74 KB, DESIGN ONLY), `CENSUS_TABLE_2026-09-25.md` (off-by-one, F13), `REVIEW_TRANSITIONAL.md`,
`ANOMALY_RULE_EVALUATION.*` (anomaly_scan_census); `DATA_ACCOUNTING.md`, `DATA_COMPLETENESS_AUDIT.md` (361 KB,
99 gaps), `PATIENT_IDENTITY_SPEC.md`, `NHANES_DOUBLE_INCLUSION_2026-09-22.md`, `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`,
`CT_INVENTORY.md`, `XRAY_DATASET_USAGE.md`, `MANIFEST_DATA_MODELS_RESULTS.md` (data_platform);
`BENCHMARK_PROTOCOL.md`, `COMPETITOR_BENCHMARK.md`, `ablations.md` (ctsp_dataset).

Superseded or record-only: `RSNAI_CLAIMS.json` + `RSNAI_PLAN.md` + `RSNAI_DATA_MANIFEST.json` (the main_v2
draft; the manifest is reused by `data_platform/plan/RSNAI_DATA_MANIFEST.remapped.json`), the eight
`carmlspine_*.json` of 09-21/22 (C4.7), `FLAGSHIP_PLAN.md` (partly superseded by the paper split),
`FEASIBILITY_REPRODUCE.md`, `PATENT_PACKAGE.md` (superseded by the provisional package), the four dated resumes and
briefs, the four FluoroCap documents and `PATHOLOGY_SOURCE_SWEEP_2026-09-14.*` (DORMANT: FluoroCap is figures of
published articles, 72.8 % of panels with zero pixel residual; out of training by directive D1).

Private-only (named in the task): `INVENTION_DISCLOSURE.md` (2026-09-18, five aspects A-E), `DISCLOSURE_MEMO.md`,
`provisional/` (SPECIFICATION 54 KB, CLAIMS, COVER_SHEET, FILING_CHECKLIST, README; FIG. 1-13 not drawn),
`disclosure_audit.json`, `disclosure_forensics.json`, `disclosure_evidence/`, `research_patent_2026-09-18.json`,
`research_registration_free_2026-09-18.json`. The TSV marks them `reference` (keep in this private repository,
cite by path and commit) and flags them for Greg's decision. The sweep / count / confirm documents
(`COUNTING_EVIDENCE.md`, `SWEEP_PROTOCOL.md`, `SWEEP_TIME_EVIDENCE.md`, `GUIDED_ACQUISITION.md`,
`SIMULATION_FIDELITY.md`) describe invention aspects A, B and E and stay private too (`MANUSCRIPTS.md` 4 and 15)
but are research documents; the TSV copies them into carm_detection with that caution.

Redaction needed on copy: `fluoro_requests_eml/*.eml`, `FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`,
`FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md`, `data_requests/SX-Stitch_request.md`,
`outreach/balgrist_data_request_2026-09-21.md` carry named researchers' e-mail addresses and Greg's personal
address (grep on 2026-10-08: 25 distinct addresses). Replace each with the institution. The Balgrist draft also
reads "[a neurosurgery resident; confirm title]" (affiliation trap, `MANUSCRIPTS.md` C5).

### 3.3 `tools/` (2026-04-18 to 09-26; 723 `.py` + 5 `.sh`, 751 tracked, 29 MB) grouped by purpose

Counts are from `ls tools/*.py | wc -l` and the name groups; one-line purposes are each file's first docstring
line (extracted on 2026-10-08).

| group | files | the ones a project folder must copy into `code/` | the rest |
|---|---|---|---|
| the deployable pipeline and its gates (carm) | `level_prototype.py` (one frame in, names + abstain flag), `sweep_map.py`, `alphabet_couple.py`, `count_from_sacrum_eval.py`, `eval_gate.py`, `holdout.py`, `checkpoint_lineage.py`, `unseen_cases.py`, `patient_keys.py`, `excluded_sources.py`, `stats_compare.py`, `model_registry.py`, `publish_checkpoints.py`, `deploy_service.py`, `latency_bench.py`, `eval_runtime_cost.py`, `level_flags.py`, `eval_calibration.py`, `level_selective.py` (19) | all 19, with path + commit; note `patient_keys.py` and `level_prototype.py` are modified-uncommitted; `stats_compare.py --help` crashes (F20) | - |
| C-ArmLSpine (carm) | `carmlspine_*.py` (30), `case134_*.py` (2), `carm_sweep.py`, `carm_denominator_repair.py`, `carm_miss_diagnostic.py`, `carm_variant_survey.py` | `carmlspine_io.py` (the only correct reader), `carmlspine_eval.py` (modified-uncommitted), `carmlspine_labels.py`, `carmlspine_pose.py` | reference |
| real-frame detectors, learning curves, cross-device, G3 split (carm) | `realxray_*.py` (12), `lcurve_*.py` (5), `indomain_*.py` (9), `or_crossdev_*.py` (7), `or_lodo_rescore_outline.py`, `or_recall_curves.py`, `or_position_prior.py`, `g3_detector.py`, `g3_leak_intersect.py`, `g3_split_verify.py`, `make_split.py`, `consolidate_splits.py`, `make_fold_banks.py` | `realxray_train.py`, `realxray_eval.py`, `make_split.py` | reference |
| angle / arc (carm) | `arc_*.py` (5), `pose_arc.py`, `pose_arc_proof.py`, `pose_pool_audit.py` | - | reference |
| cine (carm, hospital test harness) | `cine_eval.py`, `cine_latency.py`, `bournemouth_qf_eval.py`, `fluoro_video/` (22 files, pinned env) | all (UNTRACKED on 2026-10-08: commit first) | - |
| encoder and head training (carm) | `make_context_crops.py`, `train_level_backbone.py`, `train_level_classifier.py`, `recurrent_order.py`, `head_mixed_length.py`, `head_dual.py`, `stc_head.py`, `train_stc_head.py`, `message_fusion.py`, `ordinal_spine_decode.py`, `decode_sequence.py` | `make_context_crops.py` (draws ONE split over people, refuses unkeyed cases) | reference; `recurrent_order.py` L56 wrong-bank note (F5) |
| detectors on films (carm) | `detect_films.py`, `detector_*.py` (4), `build_sacrum_dataset.py`, `make_zoom_dataset.py`, `check_fluoro_degrade.py`, `wholespine_*.py` (6), `thoracic_xr_*.py` (4), `draw_film_boxes.py`, `zoom_crop_figure.py` | - | reference |
| sweep / count / confirm / guided / physics (carm, PRIVATE) | `needle_confirm.py`, `fiducial_walk.py`, `acquisition.py`, `guided_console.py`, `validate_guided.py`, `link_probe.py`, `test_masked_link.py`, `link_surface_figure.py`, `sweep_*.py` (5), `counting_brief.py`, `recovery_brief.py`, `reproduce_physics.py`, `collect_physics_results.py`, `physics_figures.py`, `physics_validate.py`, `fluoro_physics.py`, `render_physics_drr.py`, `param_census.py`, `path_census.py`, `frame_levels.py`, `window_probe.py` | `collect_physics_results.py` (`make physics-tables`, no grid) | reference; `reproduce_physics.py` resets the grid checkout (RECIPES 0.2) |
| manuscript machinery and audits | `claims_check.py`, `claims_fill.py`, `rsnai_table1.py`, `bib_audit.py`, `bib_apply_resolved.py`, `wordcount_tex.py`, `disclosure_audit.py`, `disclosure_forensics.py` | `disclosure_audit.py` ("run it before any submission, talk or release") | reference |
| figure builders | about 45 `fig*.py`, `gallery_*.py`, `make_formation_figure.py`, `render_*.py`, `contact_sheet.py`, `_figfit.py` | - | reference |
| image formation and devices (render_devices) | `device_*.py` (8), `deepfluoro_*.py` (23), `devcorpus_*.py` (2), `make_drr_dataset.py`, `ts_to_drr.py`, `drr_register.py`, `reg_*.py` (5), `spine_project.py`, `strong_dr.py`, `dr_*.py` (2), `film_match_augment.py`, `film_style_dataset.py`, `label_preservation_gate.py`, `fluorogen_*.py` (3), `drr2fluoro_cut.py`, `formation_gap.py`, `make_anchor_drr.py`, `dl_deepfluoro.py`, `ljubljana_pairs.py`, `spinesac_*.py` (9), `cobra_*.py` (6 of the 9), `paired_sets_properties.py`, `card_refit_v2_diag.py`, `diag_*.py`, `manifold_examples.py`, `corpus_manifold.py`, `corpus_resolution.py`, `diagnostics/diag_*.py` (4) (~90) | `device_fit.py`, `device_style.py`, `device_spread_sweep.py`, `deepfluoro_calibrate.py`, `make_drr_dataset.py`, `render_physics_drr.py` | reference |
| PolyPose (render_devices) | `polypose/` (16) + `polypose_*.py` (12) | `polypose/polypose_sample.py` and `polypose_warp.py` (the sampler and the forward warp) | reference; generator commit 1f4418f never pushed (G.6) |
| rare class, transitional detectors, reference standard (transitional_fluoro) | `rare_class_*.py` (12), `transitional_detectors.py`, `eval_transitional*.py` (2), `eval_global_anomaly_signature.py`, `eval_anomaly_rule.py`, `triage_variant*.py` (2), `tp_morphology.py`, `lstv_vmva.py`, `correct_buu_schema.py`, `buu_l4_*.py` (2), `geometric_indices_buu.py`, `film_ncurve.py`, `learning_*.py` (5), `explain_level_model.py`, `pool_variant_cv.py`, `score_m1_f1.py`, `verification_pages.py`, `auto_reference_*.py` (3), `rib_count_*.py` (5), `mine_spine_*.py` (4), `anomaly_*.py` (3), `scan_anomalous_ann*.py` (2), `find_rare_cases.py` | `film_ncurve.py`, `auto_reference_calibrate.py`, `verification_pages.py`, `transitional_detectors.py` | reference; `anomaly_manifest.py` defaults to a deleted bank (F22) |
| the 2-D transitional flag (REFUTED line) | `lstv_flag_*.py` (19), `lstv_eval_*.py` (4), `lstv2_probe.py` | - | reference |
| the anomaly scan (anomaly_scan_census) | `acquisition_*.py` (10), `harvest_*.py` (7), `transitional_registry.py`, `transitional_subtypes.py`, `transitional_ts_count.py`, `transitional_mask_census.py`, `ts_transitional_*.py` (2), `ts_v3_*.py` (2), `ts_spineps_*.py` (3), `ts12_verify_ids.py`, `ts_clean_subjects.py`, `other_ct_*.py` (5), `ctsp_registry_*.py` (3), `ctsp_recount.py`, `ctsp_ts_runner.py`, `ctsp_regrid_ct.py`, `ctsp_sacrum_look.py`, `cobra_lstv_*.py` (2), `dual_seg_compare.py`, `body_masks.py`, `census_table_2026-09-25.py`, `anomalous_inventory.py`, `versefusion_*.py` (5), `convert_versefusion.py`, `merge_versefusion_corpus.py`, `harvest_ls_slices.py`, `transitional_review/` (10, untracked), `CT_MINE_REPORT.md` | `transitional_registry.py`, `transitional_ts_count.py`, `ts_transitional_screen.py`, `acquisition_screen.py`, `transitional_review/` (after committing and removing the banned word from `anomaly_rules.py` and `build_review_tree.py`) | reference |
| SPINEPS ids (data_platform) | `spineps_ids*.py` (12), `spineps_id_census.py`, `spineps_label_census.py`, `spineps_relabel_from_poi.py`, `spineps_veridah_check.py`, `test_spineps_ids.py` | `spineps_ids.py` + its test (imported by 13 readers) | reference |
| data accounting, leak checks, inventories (data_platform) | `data_ledger.py`, `data_alias.py`, `data_lineage.py`, `data_manifest.py`, `leak_check.py`, `leak_effect.py`, `or_audit_*.py` (3), `audit_*.py` (3), `ct_inventory.py`, `xray_dataset_usage.py`, `film_corpus_inventory.py`, `corpus_level_report.py`, `level_inventory.py`, `level_integrity.py`, `source_quality_report.py`, `export_vindr_identity.py`, `inspect_dicom_tree.py`, `jhu_dataverse_*.py` (2), `repair_image_links.py`, `restore_container_links.py`, `pipeline_state.py`, `build_audit_doc.py`, `ctsp0533_*.py` (5), `diagnostics/make_fake_corpus.py`, `diagnostics/ctsp_crosswalk_leak.py`, `identity/` (empty, F14) | `patient_keys.py`, `leak_check.py`, `data_ledger.py`, `data_alias.py`, `data_lineage.py`, `ct_inventory.py`, `xray_dataset_usage.py` (buu_2000 mislabel, F7), `pipeline_state.py`, `diagnostics/make_fake_corpus.py` | reference |
| self-tests | `test_*.py` (14) | `test_patient_keys.py`, `test_stats_compare.py`, `test_leak_check.py` (fails on one stale Geneva fixture, F17), `test_device_gate.py`, `test_spineps_ids.py` | reference |
| nnU-Net era (ctsp_dataset) | `convert_hf_to_nnunet.py`, `aggregate_folds.py`, `compare_ablations.py`, `eval_full.py`, `eval_ensemble_test*.py` (2), `eval_subgroups.py`, `eval_oneshot.py`, `enumerate_decoder.py`, `lstv_biased_dataloader.py`, `nnunet_wandb_variant.py`, `preflight_lstv.py`, `reshape_patch.py`, `visualize_patch_sizes.py`, `sync_splits_to_nnunet.py`, `fast_scan.py`, `l6_report.py`, `dx.py`, `d815_flags_and_integrity.py`, `ds813_to_v10.py`, `make_halved_dataset.py`, `make_quaternary_dataset.py`, `check_countfree_disc.py`, `split_column.py`, `test_dataset_803_pipeline.py`, `xrsp1k_to_nnunet.py`, `eval_xrsp1k_seg.py` | `convert_hf_to_nnunet.py`, `eval_oneshot.py`, `decode_sequence.py` | reference; no evaluated one-shot model exists on disk (C5.3) |
| the plain-film line 2026-09-12 to 09-22 (plain_film_level_id) | `context_ladder.py`, `collect_context_curve.py`, `eval_interior_windows.py`, `eval_anchor_free.py`, `eval_windows_by_class.py`, `eval_fov_separability.py`, `eval_multiview.py`, `eval_raw_films.py`, `eval_shortcut_controls.py`, `eval_error_taxonomy.py`, `eval_surgeon_benefit.py`, `eval_feasibility_claims.py`, `eval_scaling_curves.py`, `eval_level_flags.py`, `subset_bank.py`, `merge_banks.py`, `merge_ctx.py`, `build_allspine_v3.py`, `build_v6_bank.py`, `build_crest_bank.py`, `common_testset_eval.py`, `coverage_arms.py`, `train_competitors.py`, `ensemble_*.py` (2), `benchmark_cina.py`, `buu_baseline.py`, `train_role_head.py`, `role_ablation_report.py`, `train_contour_pointnet.py`, `make_contours.py`, `robustness_eval.py`, `train_lumbar_focus.py`, `train_orientation.py`, `train_view_classifier.py`, `level_heatmap.py`, `level_logit_dump.py`, `level_posteriors.py`, `diag_level_model.py`, `bank_region_profile.py`, `c2_anchor_status.py`, `probe_*.py` (2), `make_feasibility_figures.py`, `make_report.py`, `make_results_table.py`, `make_count_figures.py`, `make_sweep_figure.py`, `make_verify_bench.py`, `make_reading_set.py`, `lock_adjudication.py`, the film converters (`aasce_to_drr.py`, `mendeley_to_render.py`, `spinal_ai2024_to_render.py`, `nhanes_*.py`, `manifest_to_drr_format.py`), `check_level_naming.py`, `rib_bearing_ann.py`, `corpus_xray_*.py` (5), `lumbar_*.py` (8), `track5_*.py` (6), `night_*.py` (9); the pseudolabel / review / reader-study pack tools (18) | `eval_shortcut_controls.py` (the negative controls) | reference; results RECORD ONLY or [LEAK] (`RESULTS_CATALOG.md` C1-C2) |
| FluoroCap and the image hunt (archive) | `fluorocap_*.py` (80), `fluorocap.py`, `validate_sources.py`, `make_fluoro_selftrain.py`, `make_metal_pseudolabels.py`, `make_hardware_dataset.py`, `make_implant_ct.py`, `finetune_level_fluoro.py`, `hunt_*.py` (11) | none | reference; DORMANT |
| the wrong-level scoping review (qi_wrong_level) | `review_*.py` (9), `prior_art_weak.py`, `prior_art_wrong_level.py`, `fluorocap_wrong_level_report.py` | `review_prisma.py`, `review_stats.py` | reference |
| CT-side (ct_morphometry_parity / toolkit) | `pelvis_landmarks.py`, `plan_postop.py` | - | reference |

### 3.4 `slurm/` (2026-04-18 to 10-08; 594 entries, 583 `.sh` + 2 folders + text lists, 3.4 MB)

One job per stage; each names its output and completion marker (`README.md` section 9). Grouped the same way as
the tools they call (first comment line of each script extracted on 2026-10-08): the shipped-model jobs
(`allspine_v9_{bank,keys,train,a5,submit}.sh`, `carmlspine_cv_v9init.sh`, 28 `carmlspine_*`, 16 `realxray_*`,
16 `or_*`, 5 `arc_*`, `d1_*`, `eval_gate.sh`, `eval_leaks*.sh`, the untracked `cine_*.sh`); the private sweep /
count / physics jobs (16 `sweep_*`, 9 `physics_*`, 8 `story_rows*`, `fiducial_walk.sh`, `needle_*`); the device and
render jobs (10 `device_*`, 21 `deepfluoro_*`, 17 `cobra_*`, 23 `polypose_*` + `env/polypose.*` pins, 14
`spinesac_*`, 2 `fluorogen_*`, the figure render jobs with `figure1_spec*.json` and `gallery_spec.json`); the anomaly
scan (11 `acquisition_*`, 8 `harvest_*`, 6 `ts_registry_*`, 5 `other_ct_*`, 9 `spineps_*`, 7 `versefusion_*`,
4 `vindr_*`, 19 `lstv_flag_*`); data accounting and setup (`data_accounting.sh`, `data_ledger.sh`, 6 `audit_*`,
8 `ctsp0533_*`, `grid_ff_checkout*.sh` which no longer work); the nnU-Net arrays (`spine_*`, 10 `launch_*`,
`spine_ablation.sh`); and the superseded film arms (11 `night_*`, `scaling_sweep.sh`, the v2-v7 bank chains, 14
`fluorocap_*`). All reference by path; the five project folders should name, not copy, these scripts.
`allspine_v9_bank.sh` lists every source of the level bank; `carmlspine_cv_v9init.sh` lines 11 and 67 reuse the v7
fold banks (VinDr and FluoroCap inside; `DATASET_USAGE.md` 0.4); `scaling_sweep.sh` is not keyed on `BASE` (F21).

### 3.5 `results/physics/` (2026-09-20; 86 tracked, 736 KB)

The physics / linking results `collect_physics_results.py` pulls off the grid (phys_best, phys_detconf,
phys_detector, phys_global, phys_jitter, phys_overlap, phys_tightlast, link_probe, recover, regression,
physics_figs). Finding CURRENT (detection is the binding constraint), numbers RECORD ONLY (`RESULTS_CATALOG.md`
C3.10). Copy; `make physics-tables` prints them without the grid.

### 3.6 `service/` (2026-09-14; 6 files, 29 KB)

The level-identification service (FastAPI `app.py`, `model_defs.py`, Dockerfile, `modal_app.py`): detector +
single-vertebra model + run labeller behind `POST /infer`, weights from a private HF repo at start-up; the website
never holds parameters (`service/README.md`). No weights here. Copy into carm_detection; it is the serving shape a
hospital test would start from, but it serves the September detector/level model, not the five-piece SchwingNet
stack named in `DATASET_USAGE.md` 1 (not re-verified in code).

### 3.7 `benchmark/` (2026-09-08 to 09-23; 78 files, 4.1 MB)

The CT competitor benchmark on CTSpinoPelvic1K: TotalSegmentator, SPINEPS, VISTA3D mapped into the Dataset810
one-shot space (`benchmark/README.md`); `cases.csv` (802 records), `mappings/`, run scripts (three modified and two
untracked), `figs/`, `data/` (model registry csv/md, V100 latency, training series, robustness). ctsp_dataset;
copy. `data/fluorocap_v0.1/` is the dormant FluoroCap freeze (archive).

### 3.8 `paper/` (2026-09-17 to 09-23; 152 tracked, 36 MB)

| folder | manuscript | state | note |
|---|---|---|---|
| `rsnai/main.tex` | "Naming Vertebrae Without an Anchor" (09-17 to 09-19) | superseded; leaky banks; 14 citing sentences uncorrected | private |
| `rsnai/graveyard.tex` | cut material, negative results | record | |
| `rsnai/main_v2.tex` + `claims.tex` | "Navigation from the C-arm alone" (09-22) | superseded the same evening by SchwingNet; 54/54 claims verified (job 40414708) | title page says Neurosurgery (wrong) |
| `rsnai/main_kdevices_skeleton.tex` | the k-devices skeleton | superseded | |
| `rsnai/refs.bib` (57 KB), `rsnai/figures/` (93) | bibliography source; the story-row figures | current as sources | `fig5_confirm_fluoro` of paper 1 was copied from here |
| `focused/main.tex` (86 KB) + `_drafts/` | "Making the Intraoperative Count Exact" (09-19 to 09-22) | superseded; its TikZ Figure 6 is the model for the numbered panorama | private: the overlapping-exposure sweep |
| `qi_universal_protocol/main.tex` | "The Universal Protocol with a level in it" (JCJQPS, SQUIRE 2.0), 9 pages, built 2026-09-22 | draft, not submitted | private until the provisional is filed; affiliation reads Neurosurgery; "~15 minutes" citation unverified (`MANUSCRIPTS.md` 5) |

All carry `.aux/.log/.bbl/.fls` build files (exclude). Lineage: `rsnai/main.tex` -> `focused/main.tex` ->
`rsnai/main_v2.tex` -> `SchwingNet/main.tex` (`MANUSCRIPTS.md` 2.1).

### 3.9 `data_platform/` (2026-10-08; 181 tracked, 9.8 MB)

Where every source came from (211 cards, `DATA_MANIFEST.md` 939 KB), how to fetch it again (`reacquire/`),
where it goes on Ceph (`LAYOUT.md`), how to move it (`MIGRATION_PLAN.md`, batches B00-B14; `plan/batch_items/`
has B00-B11, B13, B14 and no B12), how to index it (`db/`), the dedup census (`dedup/hash_results/A01-A23`,
`DEDUP_PLAN.md` 126 KB, `index_aliases.csv` 583 KB) and the verification (`VERIFICATION.md`,
`verification_report.json`). Every file is under 1.1 MB (`sources.json` 1.04 MB, `sources.yaml` 1.0 MB). Copy the
whole folder into data_platform. The migration state as last recorded: B00, B01, B02, B03, B06, B08, B14 cut over;
B04, B07, B09 copying; TotalSegmentator v2.0.1, BUU, FluoroCap and the banks not yet on Ceph; B01's raw TCIA CT
Colonography trees found on neither HOME nor Ceph (`HANDOFF/README.md` section 3; `OPEN_QUESTIONS.md` B30).
Per-batch truth is `plan/runs/<B>/STATUS` on the grid, which was not read.

### 3.10 `HANDOFF/` (2026-10-08; 184 tracked + `GREG_ONLY/` untracked; 2.6 MB)

Written today for a new student or a fresh Claude project; two readers (`HANDOFF/README.md` top table).
Student-readable once Greg confirms (A29): `README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`,
`DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`. Greg and the Claude project only:
`MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `context/` (141 notes with statuses; three redacted), `working_notes/`
(six topic notes of 60-97 KB with the full tables; `builders/`), `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md`
+ `literature_state/` (power.md, power_calc.py, bibliography), `GREG_ONLY/` (PRIVATE_STATE.md with credential
names and locations and the withheld contact data; the original MEMORY.md; six Beethoven notes). These are the
backbone of every project folder's STATUS.md (RESULTS_CATALOG parts A-G), TODO.md (OPEN_QUESTIONS A-G,
RESEARCH_DIRECTIONS 6, MANUSCRIPTS 21), MEMORY.md (context/INDEX.md statuses) and MANIFEST_CODE.md
(INFRASTRUCTURE 1, 8). `GREG_ONLY/` should not be copied by default (reference; Greg decides A29/A30). Note that
`HANDOFF/README.md` says the folder must never be copied into CTSpinoPelvic1K, OpenSpineToolkit,
Student_Projects, the website or a handout; a new private repository is none of those, but the reader split
should be carried.

### 3.11 The smaller folders

| folder | dates | what | family, disposition |
|---|---|---|---|
| `spine_data_review/` | 2026-09-20 (272 tracked; `runs/` 1.8 GB gitignored) | a PRISMA-ScR scoping review of every public spine CT / radiograph dataset, run by code (`sdr/` 22 modules); `PROTOCOL.md` 101 KB; `manuscript/main.tex` generated; six files modified-uncommitted | data_platform; copy the tracked part; `runs/` by path (nine `hf.jsonl` over 25 MB; `runs/2026-09-23` is the real run, 8.3 MB) |
| `reader_space/` | 2026-09-18 | the surgeon reader study Space (unaided vs assisted naming); `_original_space/` is a superseded review_service backup carrying the banned word in five files | transitional_fluoro; copy the app, exclude `_original_space/` |
| `review_space/` | 2026-09-17/18 | the student film-review Space (one name fixes the run; L6 / T13 ticks) | plain_film_level_id; copy |
| `research_notes/` | 2026-09-23 | 14 verified literature notes (synthetic:real ratio; spine synthesis prior art) | render_devices; copy |
| `reports/` | 2026-09-23 | "Synthetic real ratio X-ray detectors" (44 KB): gains plateau near 10:1; no DRR paper swept the ratio | render_devices; copy |
| `lumbar_diag_2026-09-16/` | 2026-09-17 | the mid-lumbar error diagnosis (JSON + two renders) | plain_film_level_id; RECORD ONLY; copy |
| `track5_results/` | 2026-09-17 | band-transfer reports | plain_film_level_id; RECORD ONLY [WRONG-BANK]; copy |
| `disputed_renders/` | 2026-09-17 | 7 PNG of the VerSeFusion disputed phenotypes | anomaly_scan_census; copy |
| `tests/` | 2026-05-01 to 09-25 | 61 files; `test_eval_gate.py` 58 passed on 2026-10-08 | reference; copy `test_eval_gate.py` beside `eval_gate.py` |
| `tmp/` | 2026-09-23 | 653 TRACKED scratch files (40 MB), coupling-check outputs | reference; products are in `SchwingNet/results/` |
| `tools_tmp_sync/` | 2026-09-23 | 3 stale copies | exclude |
| `logs/xray_gate/` | 2026-04-18 (.gitkeep); files 2026-09-16 | the FluoroCap X-ray gate outputs; `sheets/` 21 MB of contact sheets | plain_film_level_id; reference |
| `env/` | 2026-09-17/18 | spineps.yml + lock, fluorogen.yml, README (PYTHONNOUSERSITE) | data_platform; copy |
| `containers/`, `docker/`, `scripts/`, `data/README.md` | 2026-04-18 to 09-18 | the nnU-Net container build, the HF download and the 5-fold splitter; the data README's label table is the OLD 10-class scheme | ctsp_dataset; copy with the trap noted |
| `.github/`, `nnunet/`, `figures/` | 2026-04-18 | CI on branch main; placeholders | exclude |

## 4. Files over 25 MB (reference by path, never copy)

`SchwingNet/figures/figure1.tif` 39.0 MB; `SchwingNet/packet/figures/Figure 1.tif` and
`packet_cameraready/figures/Figure 1.tif`; `SchwingNet/results/eval_gate/touched.json` 55.3 MB;
`SchwingNet/results/learning/{embeddings,embeddings_cpu_replicate,gradcam}.npz` 31.8-32.8 MB and
`learning/lateral/gradcam.npz`; `SchwingNet/results/manifold/deep.npy` 124.1 MB;
`SchwingNet/results/reader_e/features_j1.csv` 40.3 MB; nine `spine_data_review/runs/*/records/hf.jsonl`
(gitignored) (`find -size +25M`, 2026-10-08). 518 further files sit between 1 and 25 MB, mostly figure PNG/PDF/TIFF
and the packet PDFs.

## 5. Grid paths this folder's documents name (not re-verified today)

HOME `/wsu/home/go/go24/go2432`: `~/spinesurg-ct-nnunet` (grid checkout, `SHIPPED_COMMITS.txt`),
`~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (the level encoder), `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt`
(the head), `~/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (the body detector), `~/spine-detector/runs/`
(detector arms incl. `rx_lodo_carmlspine_1024`), `~/model_night/` (sweep_v3, anomaly_manifest, fiducial, scaling,
interior_windows, ensemble, PIPELINE_STATE.md), `~/bench/` (xr_fov, robust, runtime_cost_workstation.json),
`~/lstv_flag/` (`lstv_flag_labels_v2.csv`, LEARNING_CURVE.md), `~/FluoroCap`, `~/FluoroCap_lstv2`, `~/ablate`
(202-235 GB, numbers never recorded), `~/vf_813`, `~/ctsp_drr`, `~/films_drr`, `~/verse_drr`, `~/ts_drr`,
`~/s1v11`, `~/split_final.json`, `~/patient_keys.json`, `~/mambaforge/envs/{spineps,fluorogen,spinedet}`.
Ceph `/rs/rs_grp_oschome/go2432`: `data/` (the migration target; `data/or_ready/` real-frame sets, lodo, lcurve,
cine; `data/realxray/bournemouth_qf/`), `model_night/`, `ruleclass/` (the SUPER DETECTOR RUN over 21,622 CTs),
`archive/`, `tmp/`, `private_ip/git_bundles_2026-09-26/`, `plan/runs/<B>/STATUS` (sources: `RESULTS_CATALOG.md`
header and Part A; `RECIPES.md` 0; `CINE_DEMO_BUILD_PLAN_2026-09-26.md` 0; `BOURNEMOUTH_QF_HARNESS.md` 1;
`HANDOFF/README.md` 2-3; `MANUSCRIPTS.md` 15). The MANIFEST_GRID.md of each project should take its rows from
`data_platform/DATA_MANIFEST.md`, `LAYOUT.md`, `MIGRATION_PLAN.md` and `HANDOFF/INFRASTRUCTURE.md` 2; nothing here
was checked against the grid.

## 6. What a project folder must copy, in one list

carm_detection: `HANDOFF/` (eight student files + MANUSCRIPTS, CONTEXT_EXPORT, context/, working_notes topic1/4/5),
`SchwingNet/` manuscript + NUMBERS/CLAIMS_LEDGER/PAPER1_SCOPE/TITLE/RESULTS_BUILD/LEVELCHECK_MODEL + `results/`
top-level JSON + eval_gate (minus touched.json) + coverage md + indomain + counting + lcurve + arc + figures
(PNG/PDF/caption/record) + tables + packet_src + the two 09-27 PDFs, `docs/` MODEL_CARD, DATASHEET,
CARM_DEPLOYMENT_EVIDENCE, REAL_XRAY_DATASETS_SPEC, FLUORO_DATASET_STRATEGY, the cine set, the data requests
(redacted), IRB/ (regulatory/), PRIOR_ART_*, physics set, RESUME_2026-09-22_PM (banned word removed),
grid_records, `results/physics/`, `service/`, `paper/rsnai` + `paper/focused` tex/pdf/bib (manuscripts/superseded),
and 19 pipeline scripts + `carmlspine_io.py` + the untracked cine tools into `code/` with path and commit 097933a.

transitional_fluoro: paper2_levelcheck, fig6 top-level records, auto_reference, rare_class, dual_loss, learning
md/json, reader_space app, LITERATURE_STATE + literature_state/, the memory notes tagged SN that concern
transitional anatomy. render_devices: docs/devices, DEVICE_*_AUDIT/SWEEP, DEEPFLUORO_FORMATION,
MORPHOLOGY_SYNTHESIS_PRIOR_ART, results/manifold md/csv, results/polypose, research_notes, reports.
anomaly_scan_census: transitional_registry md/csv/json, docs/ruleclass, CT_LSTV_CLASSIFIER_PLAN, CENSUS_TABLE,
REVIEW_TRANSITIONAL, lit/ct_lstv_classifier, disputed_renders, CT_MINE_REPORT. data_platform: data_platform/
whole, LEAKAGE + INFRASTRUCTURE, DATA_ACCOUNTING, DATA_COMPLETENESS_AUDIT, PATIENT_IDENTITY_SPEC, the two leak
notes, CT_INVENTORY, XRAY_DATASET_USAGE, MANIFEST_DATA_MODELS_RESULTS, spineps_ids md, spine_data_review tracked
part, env/, the accounting tools and their tests. ctsp_dataset: benchmark/, scripts/, containers/docker,
data/README (with the label-scheme warning), BENCHMARK_PROTOCOL, COMPETITOR_BENCHMARK, ablations.
ct_morphometry_parity: results/reader_e (minus the 40 MB csv). plain_film_level_id: track5_results,
lumbar_diag, review_space, STUDENT_FLUORO_CORRECTION_GUIDE. qi_wrong_level: paper/qi_universal_protocol (Greg
decides), WRONG_LEVEL_COST_EVIDENCE, WRONG_SITE_BURDEN_EVIDENCE.

## 7. Unknowns

1. Whether any grid path in section 5 still exists or has moved under the migration; nothing was read on the grid.
2. What `out.bin` (51 KB HTML) and `recept_out.json` (eight receptor-type fractions) are; no document names them.
3. Whether `tmp/` (653 tracked coupling-check files) is needed by anything; the products appear in
   `SchwingNet/results/coupling_check_*.json`.
4. Whether the five `tools/` edits and the untracked cine / transitional_review files were meant to be committed;
   the grid never received them (RECIPES 0.2).
5. Whether `service/` serves the SchwingNet five-piece stack or the September single model (not re-read in code).
6. Whether `SchwingNet/packet_build/*_2026-09-27.pdf` is the copy Greg means by "submitted" (OPEN_QUESTIONS A1).
7. Which `HANDOFF/GREG_ONLY/` content, if any, Greg wants inside spine-program (A29, A30).
8. Whether the three private-only research documents (INVENTION_DISCLOSURE.md, provisional/, the QI paper) may
   enter a private spine-program repository before the provisional is filed.
9. `spine_data_review/runs/2026-09-23/` is untracked although its `.gitignore` says a run's small files are
   committed; whether that run was ever finished is not recorded.

## 8. Flags

- Banned word: 10 tracked files carry it (`docs/RESUME_2026-09-22_PM.md`, `docs/RSNAI_PLAN.md`, five files
  under `reader_space/_original_space/`, `spine_data_review/tests/check_template_prose.py`,
  `tools/transitional_review/anomaly_rules.py`, `tools/transitional_review/build_review_tree.py`; `grep -rli`
  2026-10-08). Clean on copy; the TSV, this note and the generator script carry it nowhere (checked).
- Personal data: the fluoroscopy data-request drafts hold 25 distinct e-mail addresses including Greg's personal
  one; redact before copying. `HANDOFF/README.md` holds only institutional addresses (IRBQuestions@, hpc@).
  No token-like string was found in `docs/CREDENTIALS_SETUP.md`, `service/`, the Spaces, `env/`, `HANDOFF/*.md`
  or `data_platform/*.md` (pattern scan 2026-10-08).
- Private-only material noted as the task asked: `HANDOFF/GREG_ONLY/`, `docs/provisional/`,
  `docs/INVENTION_DISCLOSURE.md` (+ DISCLOSURE_MEMO, disclosure_audit/forensics/evidence), `paper/qi_universal_protocol/`;
  also private by content: `paper/focused/`, the sweep / count / guided documents and tools, everything SchwingNet.
- The stray folder whose name is a mangled Windows path (6 tracked duplicates of `docs/disclosure_evidence/`)
  should be `git rm`-ed in the source repository.
- Modified-uncommitted and untracked files (section 1) must be committed before any `git archive` ships, or the
  cine harness and the transitional review tree never reach the grid.
- `CLAUDE.md` and `docs/PIPELINE_RESUME.md` still instruct running python over ssh on the login node (killed by
  name there); `containers/build_container.sh` likewise (OPEN_QUESTIONS F10).
- `data/README.md` documents the OLD 10-class label scheme (L1 = 1); the release is v11 (L1 = 20, sacrum 26,
  hips 30/31, id 29 retired). Any copy must say so.
- The affiliation reads "Department of Neurosurgery" in `paper/rsnai/main_v2.tex`, `paper/qi_universal_protocol/main.tex`
  and the Balgrist draft (`MANUSCRIPTS.md` C5); General Surgery is binding.
- `.gitattributes` must travel with any copy of `SchwingNet/results/fig6/frozen/**` (byte-exact, CRLF).
