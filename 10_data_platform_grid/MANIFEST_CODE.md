# MANIFEST_CODE.md: the repositories this project depends on

Nothing that lives in a repository needs copying; this file names the repository, its URL, branch and commit on
2026-10-08, and the files that matter to this project. The copies under `code/` here are records of those files at
the stated commit (see `MANIFEST_LOCAL.md`); the repository is the executable source.

## 1. Repositories

| repository | URL | branch | commit (2026-10-08) | visibility | role here |
|---|---|---|---|---|---|
| spinesurg-ct-nnunet | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet | `L6_Class` | 097933a (working tree had uncommitted edits to `tools/patient_keys.py`, `tools/test_patient_keys.py`, `tools/pipeline_state.py`, `tools/level_prototype.py`, `tools/carmlspine_eval.py` and six `spine_data_review/` files) | private; stays private | the data platform, the accounting and leak tools, the handoff, the environments, the scoping review |
| CTSpinoPelvic1K | https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K and https://github.com/OpenSpineConsortium/CTSpinoPelvic1K (push to both) | `master` | 7ddfe38 | public | the release repository whose v11 working copy B02 moved; its `CLAUDE.md` holds the label-scheme and grid rules restated in `CLAUDE.md` here |
| OpenSpineToolkit | https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit and https://github.com/OpenSpineConsortium/OpenSpineToolkit | `main` | cb43197 | public | `ostk.labels.labels_for(volume)`; the grid copy has no `.git` and its commit is unknown |
| XRSpinoPelvic1K | https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K | `main` | 4f22935 | private; stays private | the B05 data (`data/BUU-LSPINE`, `dataset2024.zip` 4,023,726,207 B, the xrsp1k DRRs) |
| spine-detector | private GitHub (URL not recorded in any file on 2026-10-08; the laptop folder has no `.git`) | not recorded | not recorded | private | the B04 raw corpora and the `yolo*` training sets live under its HOME checkout `/wsu/home/go/go24/go2432/spine-detector/data` |
| lstv-detector | https://github.com/Gregory-Schwing-MD-PhD/lstv-detector | `no_angles` | 84636d6 | not recorded (`OPEN_QUESTIONS.md` E16) | fetched RSNA 2024 lumbar MRI for an earlier project; no CT table entry |
| spinesurg-ct-annotator | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-annotator | `master` | 1083c4f | not recorded (E16) | annotator tooling (`11_students_grid_access`) |
| spinopelvic-seg | https://github.com/OpenSpineConsortium/spinopelvic-seg (also an anonymous mirror) | `main` | c105981 | public per the NeurIPS camera-ready | the public code repository the camera-ready cites; `/wsu/home/go/go24/go2432/spinopelvic-seg/nnunet/raw` is a B14 inspect-only entry |
| openspineconsortium.github.io | https://github.com/OpenSpineConsortium/openspineconsortium.github.io | `master` | c1800f8 | public | the website (`12_website_pacs_demo`) |
| beethoven, beethoven-vscode | https://github.com/OpenSpineConsortium/beethoven (2f90319), https://github.com/OpenSpineConsortium/beethoven-vscode (8d7fc65) | | per `../_plan/PLAN.md` project 11 | | how students reach the grid; the access-list gate (`11_students_grid_access`) |

The grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` is `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405
and cannot fetch the private remote (why: not recorded, `docs/handoff/OPEN_QUESTIONS.md` B32). Ship committed trees
with `git archive --format=tar HEAD <paths> | ssh wsu-grid "cd /wsu/home/go/go24/go2432/spinesurg-ct-nnunet && tar -xf -"` and append the
commit to `SHIPPED_COMMITS.txt` there (`docs/handoff/RECIPES.md` section 0 item 2). `git archive` ships only committed
files: commit the five edited tools first.

## 2. spinesurg-ct-nnunet at 097933a: the files that matter

### `data_platform/` (copied whole to `code/data_platform/`)

`README.md`; `DATA_MANIFEST.md` (211 cards, 938,971 B); `sources.json` / `sources.yaml` (edit the JSON, then
`sync_sources_yaml.py`); `LAYOUT.md`; `MIGRATION_PLAN.md`; `VERIFICATION.md` + `verify_planning.py` +
`verification_report.json` + `spot_checks.json`; `plan/` (`build_plan.py`, `census_merge.py`, `layout_map.csv` 255 rows,
`migration_batches.csv`, `batch_items/B00-B14.tsv` (no B12; byte-identical to the grid copies the jobs read),
`readme_yaml/` per-source READMEs, `disk_map.csv`, `path_refs_{files,summary,by_item}.csv`, `plan_summary.json`,
`preflight.sbatch`, `migrate_batch.sbatch`, `verify_transfer.py`, `cutover.sh` (FINALIZE and ROLLBACK),
`publish_visibility.sh`, `remap_manifest.py`, `test_migration.sh`, `RSNAI_DATA_MANIFEST.remapped.json`); `dedup/`
(`DEDUP_PLAN.md`, `build_dedup_plan.py`, `dedup_groups.json`, `dedup_plan.tsv`, `INDEX_ALIASES.md` + `index_aliases.csv`,
`HASH_RESULTS.md`, `hash_results/A01-A23`, `dedup_hash.sbatch`, `dedup_apply.sbatch`, `dedup_guard.sh`, `dedup_lib.sh`,
`test_dedup.sh`); `db/` (`SCHEMA.sql`, `build_index.py`, `build_index.sbatch`, `test_build_index.py`, `README.md`);
`reacquire/` (`reacquire.py`, dry run by default, `--run` only in a job; `reacquire.sbatch`; `test_reacquire.py`;
`README.md`); `lib/mini_yaml.py`.

### `tools/` (the accounting, identity, leak and SPINEPS-id tools; copied to `code/tools/`)

| file | what | state |
|---|---|---|
| `patient_keys.py`, `test_patient_keys.py` | one key per person across every naming scheme (`canon_key`); the test shows both historical leaks collapse | uncommitted edit on 2026-10-08 |
| `leak_check.py`, `test_leak_check.py`, `leak_effect.py` | the bank and split audit (CHK-1 to CHK-5, CHK-8, CHK-9); the test fails on one stale Geneva fixture (F17) | committed |
| `data_ledger.py`, `data_alias.py`, `data_lineage.py`, `data_manifest.py` | content-addressed ledger, alias grouping (CHK-6, CHK-7 by pixel key), the lineage graph, the hashed-root manifest check | committed |
| `diagnostics/make_fake_corpus.py`, `diagnostics/ctsp_crosswalk_leak.py` | the planted-leak corpus the chain is proved on; the CTSP crosswalk leak check | committed |
| `or_audit_splits.py`, `or_audit_dupes.py`, `or_audit_report.py`, `audit_film_corpora.py`, `audit_realxray_lists.py`, `audit_case_shifts.py` | the real-corpus audits (near-duplicates, lists, case shifts) | committed |
| `ct_inventory.py`, `xray_dataset_usage.py` (`buu_2000` mislabel; substring keys: F7), `film_corpus_inventory.py`, `corpus_level_report.py`, `level_inventory.py`, `level_integrity.py`, `source_quality_report.py`, `excluded_sources.py` | the inventories and usage tables | committed |
| `export_vindr_identity.py`, `inspect_dicom_tree.py`, `jhu_dataverse_fetch.py`, `jhu_dataverse_info.py`, `repair_image_links.py`, `restore_container_links.py` | identity export (VinDr, job 40416449), DICOM inspection, the JHU fetch, the Dataset813 link repair (run only inside the container) | committed |
| `spineps_ids.py` + `spineps_ids_{f5_checks,impact,probe,rederive,rederive_census,render,rescore_report,verify}.py`, `spineps_id_census.py`, `spineps_label_census.py`, `spineps_relabel_from_poi.py`, `spineps_veridah_check.py`, `ts12_verify_ids.py`, `test_spineps_ids.py` | the SPINEPS instance-id guard, census, relabel and verification behind `results/spineps_ids/` | committed |
| `ctsp0533_{bone_check,cast,dicom_to_nifti,series_check,verify}.py` | the CT 0533 repair (`memory/grid-ct-0533-truncated.md`) | committed |
| `pipeline_state.py` | the pipeline state tool (run it in a job, never over ssh on the login node: F10) | uncommitted edit |
| `holdout.py` | raises on an unreadable holdout bank | committed |
| `model_registry.py` | the registry CLI (`list`, `register`, `resolve`, `link`, `restore`, `sync`, `backfill`, `lineage`) | committed |
| `build_audit_doc.py`, `checkpoint_lineage.py` + `test_checkpoint_lineage.py`, `stats_compare.py` + `test_stats_compare.py` (`--help` crashes on an unescaped `%`: F20), `test_device_gate.py`, `test_masked_link.py`, `test_realxray_banks.py`, `test_decoder_oracle.py`, `test_dataset_803_pipeline.py`, `test_spinesac_bind_smoke.py`, `test_ts_transitional_registry.py` | the audit document builder and the laptop self-tests | committed |
| `tools/identity/` | empty at 097933a (F14) | |
| not copied, referenced: `eval_gate.py` (the evaluation gate every quoted score passes; level-identification code, `01_carm_level_detection`), `make_split.py` (the G3 split, FROZEN; never resubmit `g3_split.sh` as a check), `realxray_train.py check`, `validate_sources.py`, `path_census.py` | | |

### `slurm/` (reference only; the job scripts of this project)

`data_accounting.sh` (the content-hash chain: `STAGE=ledger` array then `STAGE=rest`), `data_ledger.sh`,
`data_manifest.sh`, `data_fixes.sh`, `data_fixes2.sh`, `audit_*.sh` (6), `film_corpus_inventory.sh` (job 40416535),
`ct_inventory.sh`, `ctsp0533_*.sh` (8), `fix_splits.sh`, `generate_splits.sh`, `consolidate.sh`, `merge_vf.sh`,
`repair_symlinks.sh`, `disk_cleanup.sh`, `cleanup_tmp.sh`, `tmp_reclaim.sh`, `gzcheck.sh`, `node_probe.sh`,
`grid_ff_checkout.sh`, `grid_ff_checkout2.sh` (no longer work: the grid cannot fetch), `totalseg_setup.sh`,
`totalseg_setup2.sh`, `unpack_dataset.sh`, `jhu_dataverse_info.sh`, `rsna_cspine_fetch.sh` (ran on the login node on
2026-09-19; forbidden now), `xray_usage_regen.sh`, `xray_gate_*.sh` (5), `plan_sizes.sh`, `make_plan_variants.sh`,
`reshape_plans.sh`; `allspine_v9_bank.sh` (line 21 `rm -rf`: never rerun a bank in place); `versefusion_totalseg.sh`
(must bind `/rs/rs_grp_oschome/go2432` after B06); `eval_gate.sh` (`STAGE=chk9`).

### `tests/` (reference only; 61 files)

`test_eval_gate.py` (58 passed on 2026-10-08), `test_eval_leaks.py`, `test_acquisition.py`, `test_carm_viewport.py`,
`test_polypose_frame.py`, `test_label_scheme_toggle.py`, `test_verse_remap.py`, `test_versefusion_totalseg.py`, the
May nnU-Net tests, `integration/test_real_nnunet_integration.py`, `run_all_tests.sh`.

### `docs/` (copied: see `MANIFEST_LOCAL.md`; the rest by reference)

Copied: `DATA_ACCOUNTING.md`, `DATA_COMPLETENESS_AUDIT.md`, `PATIENT_IDENTITY_SPEC.md`,
`NHANES_DOUBLE_INCLUSION_2026-09-22.md`, `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`, `CT_INVENTORY.md`,
`XRAY_DATASET_USAGE.md`, `MANIFEST_DATA_MODELS_RESULTS.md`, `bank_profile_v3.json`, `MODEL_REGISTRY.md`,
`pipeline.md`, `troubleshooting.md`, `grid_records/JOBS_RECORD_2026-09-27_1544.{md,tsv}`. By reference:
`RSNAI_DATA_MANIFEST.json` (the hashed-root manifest `data_manifest.py check` reads; its remapped twin is in
`code/data_platform/plan/`), `CONTINUANCE_2026-09-19.md`, `RESUME_2026-09-22_PM.md` (lines 2130-2164: directives D1-D9),
`FLAGSHIP_PLAN.md`, `PIPELINE_RESUME.md` (login-node instruction to replace: F10), `CREDENTIALS_SETUP.md` (credential
locations; not copied), `CENSUS_TABLE_2026-09-25.md`.

### `HANDOFF/` at 097933a

Copied whole: `README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`,
`OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md` (section 9 already moved out of it; one username redacted here);
`context/INDEX.md` and `COPIED_AT.txt`; `working_notes/builders/*.py`; `literature_state/{dataset_landscape_by_task.md,
ranking_joined.csv, join_ranking.py, assemble.py, biblio_sorted.py, calc_addendum.py, calc_addendum.json, calc_review.py,
calc_review.json, t3_ratios.py}`. Extracted by section into `docs/handoff/extracts/`: `RESEARCH_DIRECTIONS.md`
(Lead, 5, DAT-1, 6, 7, 8, File key), `LITERATURE_STATE.md` (status, Lead, How to read, 2, 7), `MANUSCRIPTS.md`
(0, 1, 16, 20, 21), `CONTEXT_EXPORT.md` (1, 2, 3 digest, 4, 5). Never copied: `GREG_ONLY/` (credential locations,
commercial stance, withheld contacts, the original memory index, the Beethoven notes), `working_notes/topic*.md`.

### `spine_data_review/` (tracked part copied to `code/spine_data_review/`)

The PRISMA-ScR scoping review of every public spine CT and radiograph dataset: `PROTOCOL.md`, `PIPELINE.md`,
`README.md`, `PRISMA-ScR_checklist.md`, `information_sources.md`, `charting_schema.json`, `quality_rubric.md`,
`statistical_analysis_plan.md`, `licence_tiers.csv`, `grid_inventory.csv`, `Makefile`, `run_all.sh`, `requirements.txt`,
`sdr/` (21 modules), `manuscript/{main.tex, refs.bib, template.tex, build.sh, allowed_literals.txt}`, `tables/`,
`queries/`, `charting/`, `screen/`, `recipe/`, `tests/`, `_drafts/`, `data/`, `runs/pilot-2026-09-19/queries.json`.
The gitignored `runs/` (7,567 files, 1,857,122,129 B, nine `records/hf.jsonl` over 25 MB) stays in the repository
folder on the laptop and is not a dependency of anything here.

### `env/` (copied to `code/env/`)

`README.md` (the `PYTHONNOUSERSITE=1` and `python -P` rules), `spineps.yml` + `spineps.lock.txt` (CPU env),
`fluorogen.yml` (GPU env).

## 3. CTSpinoPelvic1K at 7ddfe38: the files this project reads

`CLAUDE.md` (the label-scheme, identifier 29, `zfill(4)`, RAS and grid rules), `paper/mpda/REPRODUCE.md` (the
pipeline and its traps), `docs/SPINOPELVIC_ESTIMATOR.md`, `slurm/*.sh` (default to the old grid paths `data/v5_final`
and `data/hf_export/ct` and `-q primary`: edit before reuse; `docs/handoff/INFRASTRUCTURE.md` section 13 row 4),
`Student_Projects/RECIPE.md` (job skeleton rules 3, 4, 13), `zenodo/KNOWN_ISSUES.md` (lacks the 0533 repair: F10).

## 4. OpenSpineToolkit at cb43197

`ostk/labels.py` (`labels_for(volume)`), `CLAUDE.md` (to be checked for login-node instructions the same way: F8,
F10), `tests/` (`python -m pytest`: 1 failed, 100 passed on 2026-10-08; `tests/test_cobb.py` line 91, cause not
investigated: F18).
