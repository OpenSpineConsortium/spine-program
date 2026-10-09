# MANIFEST_CODE.md — every repository this project uses, and the files that matter

Nothing that lives in a repository is copied into this folder, except the four items `code/` records as untracked or
local-only (`MANIFEST_LOCAL.md`). Commits are those of the laptop working trees on 2026-10-08.

## 1. Repositories

| repository | URL | branch | commit | visibility | role here |
|---|---|---|---|---|---|
| spinesurg-ct-nnunet | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet | `L6_Class` | 097933a (2026-10-08 16:40) | private (since 2026-09-14; never made public: it holds level-identification code) | every tool and job of the acquisition, the two-labeller screen, the harvest streams, the registry, the rule classifier and the review tree; the handoff |
| CTSpinoPelvic1K | https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K (origin) and https://github.com/OpenSpineConsortium/CTSpinoPelvic1K (osc; push to both) | `master` | 7ddfe38 (2026-09-28) | public | the two-reader Castellvi consensus, the reads, the re-read queue, the release labels (v11), the SPINEPS container recipe (untracked, copied) |
| OpenSpineToolkit | https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit (origin) and https://github.com/OpenSpineConsortium/OpenSpineToolkit (osc) | `main` | cb43197 (2026-09-25) | public | `ostk.labels.labels_for(volume)`, the label resolver every consumer of CTSpinoPelvic1K or Dataset803 output calls; the canal-closing regression at 1b7005c that rule 4 must avoid |
| XRSpinoPelvic1K | https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K | `main` | 4f22935 (2026-08-15) | private | not used by this project (project 07); listed because every folder names it |
| VerSeFusion | https://github.com/Gregory-Schwing-MD-PhD/VerSeFusion | `master` | 2b21cc4 (2026-05-12; 16 commits from 2026-05-11) | not recorded | the VerSe'19 + '20 refusion with VERIDAH corrections, the LSTV/TLTV audit, the PIR reorient, the splits and the HF export |
| lstv-detector | https://github.com/Gregory-Schwing-MD-PhD/lstv-detector | `no_angles` | 84636d6 (2026-06-13; 96 commits since 2026-02-18; other branches `main` dc5779a, `master` 78dc2ca, `spineps_only` 6f3966e) | not recorded | the MRI LSTV pipeline (SPINEPS + TotalSpineSeg + the Ian Pan disc localiser, Dice offset model) on the RSNA 2024 lumbar MRI set; no ground truth |
| spine-level-ai | https://github.com/Gregory-Schwing-MD-PhD/spine-level-ai | `master` | 5043793 (2026-02-09, one commit) | not recorded | a YOLOv8 landmark plan for the AACA 2026 deadline; superseded by lstv-detector |
| lstv-annotation-tool | https://github.com/Gregory-Schwing-MD-PhD/lstv-annotation-tool | `main` | 1c51db7 (2026-02-14, "first commit") | not recorded | the weak-label annotation tool of the AACA line; five working copies and zips existed beside it (by path only, `MANIFEST_LOCAL.md`); its Firebase key is excluded and must be revoked |
| CTSpinoPelvic1K-Syn | no remote (local git only) | `master` | 7098eb1 (2026-06-11) | — | copied whole into `code/ctspinopelvic1k_syn/`; whether it was ever pushed is not recorded |

## 2. spinesurg-ct-nnunet at 097933a: the files that matter

All paths are repository-relative. "tracked" means `git ls-files` lists it at 097933a.

**Documents (copies here under `docs/`):** `docs/CT_LSTV_CLASSIFIER_PLAN.md` (tracked, 74 KB, design only),
`docs/CENSUS_TABLE_2026-09-25.md` (tracked; off by one), `docs/ANOMALY_RULE_EVALUATION.md` + `docs/anomaly_rule_evaluation.json`
(tracked), `docs/LSTV_BENCHMARK.md` (tracked), `docs/REVIEW_TRANSITIONAL.md` (**untracked**), `docs/ruleclass/{README,CLASSIFIERS,
STUMP_RULE,MORPH_API,ARM_B_pelvis,TIERS,PREREG_rules}.md` (tracked; PREREG at f15da62), `tools/CT_MINE_REPORT.md` (tracked).
Not copied, read in the repository: `docs/RESUME_2026-09-22_PM.md` (the 2026-09-27 18:05 next steps, L28-33; the rule set
as Greg stated it, L116-122; the arm determination, L167, L197), `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` (every
job before the 2026-09-27 cancellation with its resume instruction), `data_platform/DATA_MANIFEST.md` (the census
off-by-one at L175 and L3698-3703; the acquisition cards in section 6), `HANDOFF/literature_state/power.md` (Greg-only).

**Results (copies here under `results/transitional_registry/`):** `SchwingNet/results/transitional_registry/` (tracked:
`REGISTRY.md`, `registry.csv`, `registry.json`, the five streams, `acquisition/`, `maximize/`; the renders and 26 contact
sheets by path). Not copied: `SchwingNet/results/anomalous_inventory.{json,md}` (D.4), `SchwingNet/results/rare_class/
{transitional_subtypes.csv, split_plan.md, ts12_subtype_override.json}` (A16.1, A16.4), `SchwingNet/results/spineps_ids/
{IMPACT.md, TS12_VERIFY.md}` (A16.3, A16.8), `SchwingNet/results/stats_review2/recompute.json` (S4),
`SchwingNet/packet_src/persons_available_2026-09-24.json` (A16.6-A16.7), `SchwingNet/lit/ct_lstv_classifier/` (copied here
under `docs/ct_lstv_classifier_lit/`).

**Tools (tracked), by stage of `docs/handoff/RECIPES.md` section 3.1:**

| stage | tools |
|---|---|
| 1 anomaly manifest | `tools/anomaly_manifest.py` (default `--bank` is a deleted path, L553: OQ F22), `tools/anomaly_cooccurrence.py`, `tools/anomaly_cooccurrence_from_labels.py` |
| 2 inventory | `tools/anomalous_inventory.py` (job `SchwingNet/slurm/anomalous_inventory.sh`) |
| 3 subtypes | `tools/transitional_subtypes.py` (`--ctsp`, `--aux`, `--out` required; `--ts-override` a path) |
| 4 person split | `tools/make_split.py` (`SchwingNet/slurm/g3_split.sh`; frozen, never rerun in place) |
| 5 harvest streams | verse: `tools/harvest_verse_census.py`, `harvest_verse_registry.py`, `harvest_verse_render.py` (`slurm/harvest_verse_{census,ts,ts_cpu,render}.sh`); ctsp: `tools/ctsp_registry_census.py`, `ctsp_registry_ts.py`, `ctsp_registry_build.py`, `ctsp_recount.py`, `ctsp_ts_runner.py`, `ctsp_regrid_ct.py`, `ctsp_sacrum_look.py` (`slurm/ctsp_registry_{census,ts,retry}.sh`, `ctsp_recount.sh`, `ctsp_release_audit.sh`, `ctsp_sacrum_look.sh`, `ctsp_spineps_0665*.sh`, `ctsp_ts_retry.sh`); totalsegmentator: `tools/ts_transitional_screen.py`, `ts_transitional_registry.py`, `transitional_ts_count.py`, `ts_v3_l6_probe.py`, `ts_v3_link_reused.py`, `ts_spineps_crop_prep.py`, `ts_spineps_diagnose.py`, `ts_spineps_failure_classes.py`, `ts_clean_subjects.py`, `test_ts_transitional_registry.py` (`slurm/ts_registry_{screen,rescreen,rescreen_patch,aggregate,probe,smoke}.sh`, `ts_spineps_{crop,diagnose,patch}.sh`); cobra: `tools/harvest_cobra.py`, `harvest_cobra_validation.py`, `harvest_validate_a_ctsp.py`, `harvest_validate_b_score.py`, `cobra_lstv_screen.py`, `cobra_lstv_summary.py` (`slurm/harvest_cobra_{cases,ts}.sh`, `harvest_validate_{a,b}_ctsp.sh`, `cobra_lstv_{screen,summary,rename}.sh`); other_ct: `tools/other_ct_fetch.py`, `other_ct_screen.py`, `other_ct_dedupe.py`, `other_ct_look.py`, `other_ct_summary.py` (`slurm/other_ct_{fetch,find,seg,cpu,ts_cpu}.sh`); shared: `tools/dual_seg_compare.py`, `body_masks.py`, `harvest_ls_slices.py`, `transitional_mask_census.py`, `transitional_detectors.py` |
| 6 registry | `tools/transitional_registry.py` |
| 7 renders | `tools/rare_class_maximize.py` (`SchwingNet/slurm/rare_max_{stage,verse,verify}.sh`, `rare_*_drr*.sh`, `rare_*_verify.sh`) |
| 8 acquisition | `tools/acquisition_fetch.py`, `acquisition_screen.py` (`confirm_t13_by_rib`), `acquisition_census.py` (priors L17-26; `--calibration`, `--aa3-meta`, `--nbia-fdg`, `--out` all required), `acquisition_census_addendum.py`, `acquisition_calibrate_fov.py`, `acquisition_dedupe.py`, `acquisition_t13_check.py`, `acquisition_validate.py`, `acquisition_validation_cases.py` (`slurm/acquisition_{submit,env,fetch,fetch_smoke,cpu,ts,spineps,t13_check,calibrate_fov,validation_prep}.sh`) |
| 9 census table | `tools/census_table_2026-09-25.py` |
| 10 ruleclass arms | on the grid only: `/rs/rs_grp_oschome/go2432/ruleclass/code/` (`MANIFEST_GRID.md`); record `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` |
| 11 rules, tree, report | `tools/transitional_review/` (**untracked**; copy here `code/transitional_review/`): `anomaly_rules.py`, `anomaly_rules_array.sh`, `build_review_tree.py`, `rule_report.py`, `pose_to_viewer.py`, `cobra_geometry_to_P.py`, `refit_carmlspine_poses.sh`, `review_app/` |
| rule evaluation | `tools/eval_anomaly_rule.py` (D.24; job 40414996) |
| SPINEPS ids | `tools/spineps_ids.py` (`relabel_by_ctd`), `spineps_ids_{f5_checks,impact,probe,rederive,rederive_census,render,rescore_report,verify}.py` (`slurm/spineps_{cases,ctsp,id_census,id_census_smoke,id_components,ids_repair,label_census,ts_retry,ts_v3,ts_verse}.sh`) |
| VerSeFusion adjudication | `tools/versefusion_adjudicate_t13.py`, `versefusion_disputed.py`, `versefusion_fov.py`, `versefusion_render_disputed.py`, `versefusion_totalseg.py`, `convert_versefusion.py`, `merge_versefusion_corpus.py` (`slurm/versefusion_{adjudicate,convert,fov,qc,render_disputed,tl_morphometrics,totalseg}.sh`, `verse_path_missing.sh`) |
| the 2-D flag jobs (history; project 07 and the archive) | `slurm/lstv_flag_*.sh` (19), `lstv_arm.sh`, `lstv_eval_proto.sh`, `lstv_vmva.sh`, `d815_flags.sh`, `d815_resplit.sh`, `prep815.sh`, `regen_lstv_cases.sh`, `scan_anom.sh`, `anomaly_cooc.sh`, `transitional_with_head.sh`, `variant_cv.sh`, `variant_triage.sh`, `tp_morphology.sh`, `registry_sync_loop.sh`, `vindr_*.sh` |
| the gate every quoted score passes | `tools/eval_gate.py`; `tools/patient_keys.py` (working tree, uncommitted edit on 2026-10-08) |

## 3. CTSpinoPelvic1K at 7ddfe38: the files that matter

`docs/castellvi_consensus.csv` (34 lines: 33 graded + the 0016 reference), `docs/castellvi_readers_2026-09-04.csv`,
`docs/castellvi_reread_queue.csv` (25), `docs/castellvi_type1_queue.csv` (214), `docs/lstv_reread_queue.csv` (append
here, never a new file), `docs/CASTELLVI_SCREEN_BLIND_SPOT.md` (the refuted pelvic cues, D.21), `Lumbosac.csv` (the
readers' worksheet; untracked at the root), `paper/cns2026/prep_v8_table.py` (copied the census table's high figures),
`docker/Dockerfile.spineps` + `docker/fetch_spineps_weights.py` (untracked; copied here under `code/`),
`docker/Dockerfile.totalsegmentator` (tracked). The Castellvi csv files are copied into projects 03 and 05 by the plan.

## 4. OpenSpineToolkit at cb43197

`ostk/labels.py` (`labels_for`), `ostk/morphometry.py` (`canal_dimensions` L151, `level_morphometry` L380; the
canal-closing regression at 1b7005c that rule 4's canal features must not come from), `tests/`.

## 5. VerSeFusion at 2b21cc4

`configs/veridah_corrections.csv` (25 rows), `README.md` (13.5 KB of 2026-05-12; the 24.8 KB card of 2026-05-14 is
`results/nextpaper/README.md`), `Makefile` (9 KB; the 27.5 KB one of 2026-05-14 is `results/nextpaper/Makefile`:
reorient, veridah, audit, orient, manifest, splits, hf stages; `make qc-slurm` regenerates the 374 QC PNGs),
`dataset_interface.py` (also in `results/versefusion_grid_derived/hf_staging_lstv/`).

## 6. lstv-detector at 84636d6, spine-level-ai at 5043793, lstv-annotation-tool at 1c51db7

lstv-detector: `README.md` (47 KB; sections 15-17 state no ground truth and 65-90 % estimated accuracy),
`Abstract.md` (the AACA 2026 draft with placeholders the `results/aaca_lstv_mri/` tables fill),
`slurm_scripts/00_download_data.sh` (L100: the RSNA 2024 Kaggle set), `spineps_single.sh`. spine-level-ai: the Docker
plan of its one commit. lstv-annotation-tool: the tool; its Firebase configuration must never be committed with a key.

## 6b. lstv-fusion at 3c8f5c1 (added in the final pass of 2026-10-08)

| item | value |
|---|---|
| URL | https://github.com/Gregory-Schwing-MD-PhD/lstv-fusion (visibility not recorded; the laptop clone's `origin`) |
| branch, commit | `main`, 3c8f5c1 'first commit' (2026-02-16; the only commit) |
| laptop clone | `<laptop:Desktop>/nsurg/AACA/fm/files (1)/lstv-fusion/` (the `.gitignore` there is untracked) |
| files that matter | `src/fuse_consensus.py` (26,105 B: SPINEPS + uncertainty-detection fusion, writes `fusion_summary.csv`), `src/calculate_real_performance.py` (22,385 B: scores the fusion against the clinical audit), `src/generate_viewer.py` (15,118 B: the hover-overlay viewer), `README.md`, `USAGE.md`, `example.sh`, `requirements.txt`, `docker/Dockerfile`, `docker/build.sh` |
| role here | the pipeline behind the AACA 2026 Tech Fair result ('Harnessing Algorithmic Disagreement for Automated LSTV Detection', 2026-06-12 to 15) and the tables `results/aaca_lstv_mri/lstv_cohort_summary.csv`, `lstv_per_study.csv`; all nine tracked files are copied to `code/aaca_lstv_mri/lstv_fusion/` (`MANIFEST_LOCAL.md`, final pass) |
| not in | lstv-detector 84636d6, spine-level-ai 5043793, lstv-annotation-tool 1c51db7 (`git ls-files` of the local clones; `fuse_consensus` is in none of them) |

## 7. External code and weights, by identifier

TotalSegmentator 2.18.0 `total` (arm A, labeller B); SPINEPS 2.1.1 + VERIDAH, TPTBox 0.8.2 (labeller A; masks before
commit 147428d of spinesurg-ct-nnunet carry raw ids); the Moller rib nnU-Net, Zenodo 14864106, folds 0-2 (arm B; the
method is arXiv:2505.05004, the PDF by path in `MANIFEST_LOCAL.md`); Dataset803 pelvis ensemble on Hugging Face
`OpenSpineConsortium/spinopelvic-seg-checkpoints` (the pelvis arm); fhofmann/VertebralBodiesCT-Labels `data.csv` (the 70
outside L6 / T13 reads); the VerSe'20 variant table (Loeffler 2021, Supplementary Table 1).
