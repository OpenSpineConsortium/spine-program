# MANIFEST_CODE — the repositories this project depends on

Written 2026-10-08. Nothing that lives in a repository at the commit named here was copied into this
folder except the documents a reader opens first (`docs/ctsp/`, `docs/ctsp_root/`, `docs/release/`,
`manuscripts/`), the benchmark and the five `scripts/` of the private repository (`code/`), each of which
carries a header naming its repository path and commit (`MANIFEST_LOCAL.md`). Remotes and heads were read
with `git remote -v` and `git log -1` on 2026-10-08; none of the remotes was queried over the network, so
whether `origin` and `osc` carry the same history is not verified.

## 1. CTSpinoPelvic1K (public) — the dataset's own repository

| item | value |
|---|---|
| URL | `origin` https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K ; `osc` https://github.com/OpenSpineConsortium/CTSpinoPelvic1K (the copy the article cites; push to both, `memory/push-both-github-remotes.md`) |
| branch, commit | `master`, **7ddfe38** (2026-09-28, "CLAUDE.md: grid etiquette from C&IT"); 1,090 tracked files |
| working tree on 2026-10-08 | six tracked files modified and uncommitted: `.gitignore`, `CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`, `CAMERA_READY_NEURIPS/src/{bib/references.bib,checklist.tex,neurips_2026.pdf,neurips_2026.tex}`, `paper/mpda/CTSpinoPelvic1K_reprint_check.pdf`; untracked of value: `CAMERA_READY_NEURIPS/src/appendix/` (11 tex), `src/figs/fig_app_construction.pdf`, `docs/{ids.txt,ajnr.html,ukb.html,HANDOFF_2026-09-21_PM.md}`; `paper/cns2026/` is kept out through `.git/info/exclude`. The copies in `manuscripts/` are from the **working tree**: 7ddfe38 does not hold the 2026-09-27 camera-ready edits (`TODO.md` step 2) |
| last commits of interest | `70de829` 2026-09-25 `paper/mpda/main.tex` (camera-ready cites the public code repository; MPDA five-of-six Castellvi wording); `38b0cb9` 2026-09-25 camera-ready affiliation and 21 pages; `45df97d` 2026-09-26 stops tracking the CNS generator; `567ec54` 2026-09-19 arXiv carries the supplement; `2232bde` the v10-to-v11 spinopelvic comparison and the S1 carve audit; `83f7f95` Panjabi 1991 Table 3 into `make_reference_table.py`; `028210a` the direction-blind tilt gate fixed (2026-09-11); `20ff26a` abstract removed from the main document (2026-09-21); `31e1b16`, `f14c9b9` Castellvi wording and the F30 funding line; `2ba362f` the Fisher test removed; `e659ad4`; `90a27a7` `ostk_level_morphometry.csv` before the ostk regression; `7f44959` the deleted CTSpine1K selector (recoverable) |
| grid checkout | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` at a0c5139, behind the laptop (`MANIFEST_GRID.md` section 4) |
| older clone | a second local clone at 4fb4a62 (2026-04-28, origin only) is an ancestor of 7ddfe38 (`git merge-base --is-ancestor` true); nothing tracked there is missing from this repository |

**The files that matter** (all at 7ddfe38 unless marked):

| path | what | used by |
|---|---|---|
| `scripts/label_scheme.py` | the scheme contract: ids, names, `RETIRED_IDS`, the `OLD_TO_NEW_V9` / `OLD_TO_NEW_V10` remaps; mirrored in the deposit's `dataset_labels.json` | everything |
| `scripts/merge_s1_into_sacrum.py`, `scripts/check_s1_merge.py` | the v10 -> v11 step and its check (the count of 155,093,558 voxels returned on 801 of 802 records is a note's record, `STATUS.md` F.7; the docstring does not carry it) | `TODO.md` step 4 (mirror) |
| `scripts/check_release_invariants.py`, `scripts/qc_rib_vertebra_incidence.py` | the release gates (802 / 802 must pass; they stop the chain) | `docs/handoff/RECIPES.md` section 9 item 2 |
| `scripts/extract_level_gradients.py`, `extract_surgical_morphometrics.py` (with `_canal_column`, `_canal_ap`), `extract_pelvic_shape.py`, `extract_transition_morphometrics.py`, `extract_degenerative.py`, `extract_opportunistic.py`, `extract_proximal_femur.py` | the seven extractors of `manuscripts/mpda/REPRODUCE.md` section 1 | `TODO.md` step 5; project 05 |
| `scripts/audit_s1_carve.py`, `scripts/compare_v10_v11_spinopelvic.py` | the carve audit and the v10 / v11 comparison (`STATUS.md` F.5, F.6) | record |
| `scripts/compare_ctspine1k_pathcsv.py`, `scripts/test_morphometric_separability.py`, `scripts/six_lumbar_readings.py`, `scripts/shift_hypothesis_test.py`, `scripts/sweep_foramina_params.py`, `scripts/height_probe.py`, `edge_probe.py`, `render_height.py`, `scripts/extract_pelvic_shape.py` | the analyses behind `STATUS.md` F.2, F.27, F.28, F.35, F.39, F.42 | record |
| `scripts/make_fig_anchors.py`, `scripts/select_anchor_cases.py`, `scripts/render_anchors.py` | Figure 2 (four phenotypes: 0704, 0428, 0094, 0005); trap: a check on retired id 29 once swapped a case silently | `docs/handoff/RECIPES.md` section 9 item 5 |
| `scripts/render_hardware.py`, `scripts/render_hardware_gallery.py` | Figure S1; which made the committed PDF is not recorded (`OPEN_QUESTIONS.md` E14) | same |
| `scripts/make_census_table.py`, `scripts/label_census_v7.py`, `scripts/extract_pseudolabel_dice.py`, `scripts/eval_vs_manual.py` (written, never run) | Table S3, the census CSV, Table S1 | same |
| `scripts/qc_v4_ribs_and_verts.py`, `scripts/qc_version_progression.py`, `scripts/refresh_lstv_from_labels.py`, `scripts/screen_missed_castellvi.py` | the rib review-set rule (152 cases), the version progression, the LSTV flag refresh, the Castellvi screen | `memory/canonical-rib-triage.md`; `docs/ctsp/VERSION_PROGRESSION.md` |
| `scripts/build_v3_totalseg.py`, `build_v4_ribs.py`, `build_v6.py`, `build_final_dataset.py`, `renumber_labels.py`; `benchmark_{totalseg,spineps,moller}.py`; `fill_hpr_determination.py`; `scripts/adhoc/` (the root ad-hoc scripts duplicated) | the build chain (`docs/ctsp/BUILD_CHAIN.md`, 13 steps) and the renumbering | record |
| `scripts/LSTVReviewer.py` | the tracked twin of `code/lstv_review_tool/LSTVReviewer.py` | — |
| `scripts/demo_pelvic_width_dimorphism.py` | the student demo (its committed report used S1 width on v10; `STATUS.md` F.45) | project 11 |
| `paper/mpda/` (422 tracked) | the article: `main.tex`, `main_OL.tex`, `title_page.tex`, `cover_letter.md`, `REPRODUCE.md`, `PLAN.md`, `ARXIV_SUBMISSION.md`, `CITATION_CHECK.md`, `STUDENT_REVIEW_RESPONSE.md`, `build.sh`, `make_submission.py`, `make_arxiv.sh`, `make_overleaf.py`, `make_figures.py`, `make_levelatlas_fig.py`, `make_fov_fig.py`, `make_abstract_text.py`, `make_coauthor_docs.py`, `page_estimate.py`, `apply_compliance.py`, `audit_ms.py`, `audit_artifacts.py`, `audit_pdfs.py`, bib and bst, `figures/`, `arxiv/`, `overleaf/`, `tools/` | copied to `manuscripts/mpda/` (text, scripts, figures, final PDFs); the `_others/`, `_schehr/`, `_upd/` workings (280 files) by reference only |
| `morphometrics/` (46 tracked) | `surgical_morphometrics.csv` (Table III), `level_gradients.csv`, `level_references.csv` (365 rows), `level_atlas.csv`, `panjabi_reference.csv`, `pedicle_width_references.csv`, `ostk_level_morphometry.csv` (commit 90a27a7), `transition_morphometrics.csv`, `pelvic_shape.csv`, `degenerative.csv`, `opportunistic.csv`, `proximal_femur.csv`, `metal.csv`, `s1_carve_audit.csv`, `castellvi_grades.csv` (stale), `label_census_v{7,9,10,11}.csv`, `anchor_cases.json`, `make_reference_table.py`, `annotation_counts.csv` | owned by project 05; **`annotator_names.csv` carries student names in a public repository** (`TODO.md` step 5) |
| `slurm/` (129): `level_gradients.sh`, `morphometrics.sh`, `pelvic_shape.sh`, `degenerative.sh`, `opportunistic.sh`, `proximal_femur.sh`, `finalize_release.sh`, `fov_check.sh`, `refresh_lstv_v3.sh`, `ship_v3.sh` | the batch wrappers; still point at `data/v5_final` and `-q primary` (edit before reuse) | `docs/handoff/RECIPES.md` section 9 item 3 |
| `zenodo/` (18): `assemble_deposit.py`, `new_version.py`, `upload.py`, `finalize_v9.py`, `make_croissant.py`, `reconstruct_ct.py`, `fetch_from_tcia.py`, `README.md`, `KNOWN_ISSUES.md`, `hf_dataset_card.md`; `hf/push_v9.py` | the deposit and mirror tools (integer versions only; token from `~/.zenodo_token`) | `TODO.md` step 4 |
| `tests/` (25), `configs/` (3), `containers/` (2), `docker/Dockerfile`, `docker/Dockerfile.totalsegmentator`, `docker/Dockerfile.spineps` + `fetch_spineps_weights.py` (untracked), `review_service/` (9), `reviewtool/` (4), `data/README.md`, `data/itksnap_v4_labels.txt`, `.github/workflows/ci.yml`, `Makefile`, `pyproject.toml`, `requirements.txt` | pipeline, review Space and packaging | reference |
| `CAMERA_READY_NEURIPS/` (15 tracked + untracked appendix) | the NeurIPS 3474 camera-ready | copied from the working tree |
| `docs/` (61 tracked) | the working knowledge | copied to `docs/ctsp/` (three untracked saved web pages and the C-arm note left out) |
| `results/`, `hardware_review/`, `qc_final/`, `qc_hardware/` | result and QC tables | copied (renders and volumes left out) |
| `Student_Projects/` | a nested repository, https://github.com/OpenSpineConsortium/Student_Projects, head 3f1cf04 (2026-09-27, local; whether pushed is not verified, `OPEN_QUESTIONS.md` A25); `board.json` / `BOARD.md` name students | project 11; never copied here |
| `paper/clinical/main.tex` | the iliac-crest clinical paper (v5-era number, `STATUS.md` F.41) | project 09 |

## 2. spinesurg-ct-nnunet (private) — the nnU-Net tools, the benchmark and the HANDOFF

| item | value |
|---|---|
| URL | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet (private since 2026-09-14; `memory/fluorocap-repo-private.md`); never made public, never pushed to a public remote |
| branch, commit | `L6_Class`, **097933a** (2026-10-08) |
| working tree on 2026-10-08 | `benchmark/run_spineps_cases.py`, `run_spineps_ribs.py`, `spineps_to_oneshot.py` modified and uncommitted; `benchmark/run_spineps_patched.py`, `spineps_cc3d_patched.py` untracked (the copies in `code/benchmark/` say so in their headers); `HANDOFF/GREG_ONLY/` untracked and never copied |
| grid checkout | `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` at 4e3fe93, and the grid can no longer fetch the private remote; ship by `git archive | ssh tar` (`docs/handoff/RECIPES.md` section 0 item 2) |

**The files that matter for this project:**

| path | what |
|---|---|
| `HANDOFF/` (184 tracked) | the 2026-10-08 handoff; the eight student-readable files are in `docs/handoff/`; `MANUSCRIPTS.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md`, `CONTEXT_EXPORT.md` are Greg-only and appear here only as extracts (`docs/handoff/EXTRACTS.md`); `context/` holds the 141 redacted memory copies (55 are in `memory/`) |
| `docs/BENCHMARK_PROTOCOL.md`, `docs/COMPETITOR_BENCHMARK.md`, `docs/ablations.md`, `docs/xrsp1k_seg.md`, `data/README.md` | copied to `docs/spinesurg_ct_nnunet/` |
| `docs/LSTV_BENCHMARK.md`, `docs/ruleclass/PREREG_rules.md` (rule 4 cites `STATUS.md` F.28), `docs/ruleclass/CLASSIFIERS.md` (R36), `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` (the cancelled chains and how each resumes), `docs/PATIENT_IDENTITY_SPEC.md` (line 119: 802 / 802 one person per record), `docs/REVIEW_TRANSITIONAL.md` (untracked) | referenced by `STATUS.md` and `TODO.md`; owned by projects 06, 10 and 02 |
| `tools/convert_hf_to_nnunet.py`, `aggregate_folds.py`, `compare_ablations.py`, `eval_full.py`, `eval_ensemble_test.py`, `eval_ensemble_test_sep_hips.py`, `eval_subgroups.py`, `eval_oneshot.py`, `decode_sequence.py`, `enumerate_decoder.py`, `lstv_biased_dataloader.py`, `nnunet_wandb_variant.py`, `preflight_lstv.py`, `reshape_patch.py`, `visualize_patch_sizes.py`, `sync_splits_to_nnunet.py`, `fast_scan.py`, `l6_report.py`, `dx.py`, `d815_flags_and_integrity.py`, `ds813_to_v10.py`, `make_halved_dataset.py`, `make_quaternary_dataset.py`, `check_countfree_disc.py`, `split_column.py`, `test_dataset_803_pipeline.py`, `xrsp1k_to_nnunet.py`, `eval_xrsp1k_seg.py` | the April-June nnU-Net era: HF to nnU-Net conversion, the LSTV-aware dataloader, ablation aggregation, Dataset803/810/813/815 evaluation, the counting decoder (`STATUS.md` C5.2) |
| `tools/eval_gate.py`, `tools/patient_keys.py`, `tools/ct_inventory.py`, `tools/spineps_ids.py`, `tools/disclosure_audit.py` | the evaluation gate, the identity keys, the CT census, the SPINEPS id guard, the disclosure audit (run before any talk or upload) |
| `slurm/spine_prep.sh`, `spine_train_fold.sh`, `spine_train_array.sh`, `spine_eval_*.sh` (3), `spine_predict_803_best*.sh`, `spine_pred_803_best_array.sh`, `spine_ensemble_803_best.sh`, `spine_ablation.sh`, `spine_convert.sh`, `launch_*.sh` (10), `relaunch_fullribs.sh`, `switch_to_fullribs.sh`, `resubmit_round2.sh`, `push99_chain.sh`, `queue_surgio_chain.sh`, `queue_all_2026-09-22.sh`, `spineps_cases.sh`, `spineps_ctsp.sh`, `spineps_ts_v3.sh`, `spineps_ts_verse.sh`, `competitor_ensemble.sh`, `xr_bench.sh`, `mv_bench.sh`, `sync_to_nnunet.sh`, `convert_hf_to_nnet.sh`, `decoder_oracle.sh`, `product_select.sh`, `README_fused_only_ablation.md` | the nnU-Net preprocess, train, evaluate and ablate arrays for Dataset802-815 and the CT competitor runs |
| `benchmark/` (78 files) | copied to `code/benchmark/` (`data/fluorocap_v0.1/`, the dormant FluoroCap freeze, left out) |
| `scripts/` (5), `containers/build_container.sh`, `docker/Dockerfile` | copied to `code/` |
| `CITATION.cff` (ORCID placeholder; its `version` field reads `0.1.0`, the file's own string quoted as written), `pyproject.toml` (packages = tools), `requirements.txt` (host-side only; nnU-Net lives in the container) | reference |

## 3. OpenSpineToolkit (public) — the measurement library

| item | value |
|---|---|
| URL | `origin` https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit ; `osc` https://github.com/OpenSpineConsortium/OpenSpineToolkit |
| branch, commit | `main`, **cb43197** (2026-09-25); 19 modules, 94 test functions (`docs/handoff/RESULTS_CATALOG.md` G.1) |
| files that matter here | `ostk/labels.py` (`labels_for(volume)`; line 64 still maps `"S1": 29` in `LABELS_V10`, G.3), `ostk/spine.py` lines 473-474 (the whole-sacrum fallback), `ostk/vertebral_body.py` lines 98-132 and `ostk/morphometry.py` (the 1b7005c canal-closing regression, G.2), `SPEC.md`, `tests/test_labels.py`, `tests/test_cobb.py` (one failing test, `OPEN_QUESTIONS.md` F18) |
| grid copy | `/wsu/home/go/go24/go2432/OpenSpineToolkit`; whether the regression is fixed there is not recorded (B29) |
| owner | project 04; this project only consumes its numbers after the fixes |

## 4. spinopelvic-seg (public) — the Dataset803 pseudolabeller the camera-ready cites

| item | value |
|---|---|
| URL | `osc` https://github.com/OpenSpineConsortium/spinopelvic-seg (the citation in `manuscripts/neurips_camera_ready/src/neurips_2026.tex`, commit 70de829 of the CTSpinoPelvic1K repository); `origin` https://github.com/anonymous-neurips-ED/spinopelvic-seg (the review-time anonymous copy) |
| branch, commit | `main`, **c105981** (2026-06-23); clean working tree |
| files that matter | `tools/eval_full.py`, `tools/nnunet_wandb_variant.py`, `tools/lstv_biased_dataloader.py`, `scripts/generate_5fold_splits.py` (the patient-grouped LSTV-stratified splitter; its twin is in `code/spinesurg_scripts/`), `slurm/*.sh`, `tests/` |
| checkpoints | Hugging Face `OpenSpineConsortium/spinopelvic-seg-checkpoints` (and the review-time `anonymous-neurips-ED/spinopelvic-seg-checkpoints`); the five Dataset803 folds behind `STATUS.md` F.4 |
| open | still carries an anonymised citation and `anonymous-neurips-ED` as author (`CAMERA_READY_CHANGES.md` item 14); its live visibility was not re-checked (`OPEN_QUESTIONS.md` E16); the MLHC-anonymised twin `anonymous-mlhc/spinopelvic-seg` (master 91b7e9e) differs only in README, Makefile, pyproject and two scripts and is not referenced |

## 5. Lineage repositories (record only)

| repository | URL, branch, commit | what it adds |
|---|---|---|
| SpineSurg-CT | https://github.com/Gregory-Schwing-MD-PhD/SpineSurg-CT, `main`, 0051074 (2026-04-09, 136 commits) | the project's first incarnation (March-April 2026): COLONOG matching and mask fusion scripts, `src/` train and eval, `metadata_colonog.csv/.xlsx`, `metadata_hnscc.xlsx`, `data_split.txt`, `path.csv`, `tokens/qc_figures`, `cit.bib`; the March arXiv draft and lab-notebook memos around it are in `manuscripts/spinesurgct_arxiv_2026-03/` and `docs/labnotebook_2026-03/` |
| VerSeFusion | https://github.com/Gregory-Schwing-MD-PhD/VerSeFusion, `master`, 2b21cc4 (2026-05-12) | the VerSe unification (374 scans; `has_T13` wrong, `memory` note in project 06); its README says it accompanies a NeurIPS D&B submission that is not recorded as submitted (`OPEN_QUESTIONS.md` A8) |
| spinesurg-ct-annotator | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-annotator, `master`, 1083c4f (2026-04-24) | the April 2026 HF Space annotator, superseded by `ctsp:review_service/` + `reviewtool/`; `assignments.json` may name students |
| XRSpinoPelvic1K | https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K (private), `main`, 4f22935 (2026-08-15) | the radiograph twin; touches this project only through `docs/spinesurg_ct_nnunet/xrsp1k_seg.md` and the two converters named in section 2 |

## 6. Hosted data and records

| host | id | state |
|---|---|---|
| Zenodo | concept 10.5281/zenodo.22139642; v10 10.5281/zenodo.22642578 (published 2026-09-07); **v11 10.5281/zenodo.22797014** (published 2026-09-18 per four documents; live state not re-checked, E7); build archive 10.5281/zenodo.22647933 | token file `~/.zenodo_token` on the laptop (name only; `memory/zenodo-deposit.md`) |
| Hugging Face | `OpenSpineConsortium/CTSpinoPelvic1K` (the public mirror; **v10 with id 29** on 2026-09-27; card says CC BY-NC 4.0); `anonymous-mlhc/CTSpinoPelvic1K` (the review-time dataset at `@v4`...; `memory/canonical-rib-triage.md`); `anonymous-mlhc/CTSpinoPelvic1K-reviews-{ribs,spine,nerve,ili,classfix,triaged}` (the private review ledgers: **never copy**, `memory/review-space-repos.md`); `OpenSpineConsortium/spinopelvic-seg-checkpoints` | Greg's handle `gregoryschwingmdphd` (`memory/hf-identity.md`); org tokens are file-only and their notes are Greg-only |
| arXiv | 2609.22760 (v1 of the dataset article, 2026-09-19); replacement not decided (`OPEN_QUESTIONS.md` A22) | `manuscripts/mpda/ARXIV_SUBMISSION.md` |
| OpenReview | NeurIPS 2026 submission 3474, id D8yRWDAGQF, accepted poster 2026-09-24 | `manuscripts/neurips_camera_ready/REVIEWER_CRITIQUES.txt` |
| TCIA | CT COLONOGRAPHY (ACRIN 6664), 825 patients, 3,451 series; the CT behind every record (`docs/handoff/EXTRACTS.md` L1.1) | `ctsp:zenodo/fetch_from_tcia.py` |
