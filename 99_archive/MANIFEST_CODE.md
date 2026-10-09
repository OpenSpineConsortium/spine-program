# MANIFEST_CODE for 99_archive

Every code repository this folder refers to, with URL, branch, commit and the files that matter, so that nothing that
lives in a repository needs copying. Commits are as of 2026-10-08 (`git log -1` on the laptop checkouts). The prefixes
used by the copied records resolve here: `ssn:` = spinesurg-ct-nnunet, `sn:` = its `SchwingNet/`, `ctsp:` =
CTSpinoPelvic1K, `ostk:` = OpenSpineToolkit, `xrsp:` = XRSpinoPelvic1K, `mem:` = the memory notes (copied in
`ssn:HANDOFF/context/`).

## 1. spinesurg-ct-nnunet (private)

`https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet.git`, branch `L6_Class`, commit 097933a (2026-10-08,
"HANDOFF: the handoff for a new student or a fresh Claude project"). The grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet`
is at 4e3fe93, behind the laptop, and cannot fetch; ship by `git archive | ssh tar`, never `make physics*` (it hard-resets;
`docs/handoff/RECIPES.md` section 0). Apache-2.0 (`LICENSE`, 11,313 B; `NOTICE`, 166 B; DISPOSITION ssn r5, r6).
`.gitignore` (3,040 B; ssn r9). `.github/workflows/ci.yml` (964 B; a syntax-only CI on branch `main` while the work is on
`L6_Class`; ssn r11).

Files that matter to this archive:

| file | last commit | what it is for this folder |
|---|---|---|
| `docs/HANDOFF_2026-09-21_PM.md` | fb14892, 2026-09-22 | copied to `docs/checkpoints/` |
| `docs/RESUME_2026-09-22_PM.md` | 465bec6, 2026-09-27 | copied to `docs/checkpoints/` with the banned word rewritten and three redactions (`MANIFEST_LOCAL.md`) |
| `docs/RESUME_2026-09-22.md`, `docs/DAILY_REPORT_2026-09-22.md` | 9f2af48, 2026-09-22 | copied |
| `docs/MORNING_BRIEF_2026-09-16.md` | 6984446, 2026-09-17 | copied |
| `docs/FLUOROCAP_README.md`, `FLUOROCAP_PROTOCOL.md`, `FLUOROCAP_QC_2026-09-14.md`, `FLUOROCAP_MORNING_2026-09-14.md` | 116b6ef, a6e36b3, 351808c, 0439616 (2026-09-13 / 14) | copied |
| `docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md`, `docs/pathology_source_sweep_2026-09-14.json` | b1469ae, 2026-09-14 | copied; the JSON with two named contact addresses and the banned word rewritten |
| `docs/PIPELINE_RESUME.md`, `docs/pipeline.md`, `docs/troubleshooting.md` | 6d71003, 2026-09-18; the two others 2026-04-24 | the FluoroCap pipeline resume and the old nnU-Net notes; copied into `01_carm_level_detection/docs/` (DISPOSITION line 1273); `PIPELINE_RESUME.md` runs `python` on the login node, against the standing rule |
| `docs/ablations.md`, `docs/xrsp1k_seg.md` | 2026-04-24; 2026-06-29 | old nnU-Net and XRSpinoPelvic1K segmentation notes; copied into `03_ctspinopelvic1k_dataset/docs/` (DISPOSITION line 1280) |
| `tools/fluorocap_*.py` (73 files with that prefix on 2026-10-08), `tools/fluorocap.py`, `tools/validate_sources.py`, `tools/make_fluoro_selftrain.py`, `make_metal_pseudolabels.py`, `make_hardware_dataset.py`, `make_implant_ct.py`, `finetune_level_fluoro.py`, `tools/hunt_*.py` (12: hunt_atlases, hunt_bookshelf, hunt_common, hunt_commons, hunt_contactsheet, hunt_journals, hunt_licprobe, hunt_oer, hunt_pdtexts, hunt_selftest, hunt_summary, hunt_terms) | tree 097933a | the FluoroCap harvesters (PMC, OpenAlex, Open-i, Commons, YouTube, Reddit, Instagram, patents), the constraint decoder, hardware detection, the anatomy-image hunt (ssn r143). Dormant; nothing here runs them |
| `tools/pipeline_state.py` | tree 097933a | the FluoroCap pipeline state tool `PIPELINE_RESUME.md` points at; writes `~/model_night/PIPELINE_STATE.md` |
| `slurm/fluorocap_ablation.sh`, `fluorocap_finetune_chain.sh`, `fluorocap_hwdet.sh`, `fluorocap_hwdet2.sh`, `fluorocap_orient.sh`, `fluorocap_recount.sh`, `fluorocap_refresh.sh`, `fluorocap_rerun_chain.sh`, `fluorocap_run_infer.sh`, `fluorocap_run_rest.sh`, `fluorocap_v2.sh`, `fluorocap_v2_pipeline.sh` | tree 097933a | the 12 FluoroCap slurm chains present on 2026-10-08 (the inventory counted 14 by a wider pattern) |
| `slurm/night_*.sh` (11), `slurm/scaling_sweep.sh`, the v2-v7 bank chains (`slurm/build_allspine_v*.sh`, `overnight_v7.sh`) | tree 097933a | the superseded film arms and the leaked banks; `scaling_sweep.sh` is not keyed on `BASE` (OQ F21) |
| `slurm/recurrent_head.sh` line 16, `tools/recurrent_order.py` line 56 | tree 097933a | still say `films_all2` for the C1.2 head that ran on `films_ann_fov96_ctx` (OQ F5) |
| `tools/level_selective.py`, `tools/head_mixed_length.py`, `tools/benchmark_cina.py`, `tools/train_competitors.py`, `tools/ensemble_eval.py`, `tools/lstv_flag_learning_curve.py`, `tools/lstv_flag_curve_plot.py` | tree 097933a | the tools behind C1.8, C1.6, C1.16, C1.17, C1.13 |
| `tools/eval_anomaly_rule.py`; `docs/ANOMALY_RULE_EVALUATION.md`, `anomaly_rule_evaluation.json` | tree 097933a | the R + C = 22 refutation (D.24; job 40414996); owned by 06 |
| `benchmark/data/fluorocap_v0.1/` (named as on disk): `LOCK_A.json`, `LOCK_B.json`, `classifier_report.json`, `infer_comparison.md`, `infer_summary.json`, `infer_summary_v5z_aug2.json`, `infer_summary_v5z_aug3.json`, `infer_summary_v5zearly.json`, `license_review_queue.csv`, `montage_included_sample.png` (1,454,894 B), `stats.json` | tree 097933a | the frozen FluoroCap release record of 2026-09-13 / 14 (12 files) |
| `benchmark/data/model_registry.csv`, `model_registry.md` (2026-09-14) | tree 097933a | the pre-registry model list of the FluoroCap era |
| `paper/rsnai/web/index.html` (65,805 B) | tree 097933a | a styled web rendering of the first C-arm draft (ssn r180); superseded |
| `paper/rsnai/main.tex` (6506470, 2026-09-20), `main_v2.tex` + `claims.tex` (c508f5b), `graveyard.tex`, `refs.bib`; `paper/focused/main.tex` (f61cd72, 2026-09-22) | as given | the superseded C-arm drafts (`docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md` section 4); copied into `01_carm_level_detection/manuscripts/superseded/`; `main_v2.tex` title page says Neurosurgery |
| `docs/RSNAI_PLAN.md`, `docs/RSNAI_CLAIMS.json`, `docs/RSNAI_DATA_MANIFEST.json`, `docs/FEASIBILITY_REPRODUCE.md`, `docs/FLAGSHIP_PLAN.md` | tree 097933a | the superseded plans; in 01 as history flagged superseded |
| `docs/carmlspine_*_2026-09-21.json`, `carmlspine_ftdet_*_2026-09-22.json` (8 files) | tree 097933a | the v2-lineage C-ArmLSpine cross-validation and zero-shot scores (A2.9, A3.11, C4.7); in `01/results/` |
| `docs/or_ready_audit_track_2026-09-22.json` | tree 097933a | the split audit; the "100 % sacrum on DeepFluoro" is a same-device number; in 01 and 08 |
| `SchwingNet/tables/tab3_naming.md`, `SchwingNet/atlas/model.json`, `SchwingNet/packet/atlas/model.json`, `SchwingNet/packet_cameraready/atlas/model.json` | tree 097933a | still print the superseded A2.9 and A3.11 rows; fixed in 01 |
| `SchwingNet/NUMBERS.md` "Numbers deliberately absent"; `SchwingNet/results/RIGOR_FIXES.md`; `SchwingNet/results/eval_gate/EVAL_LEAKS.md` | tree 097933a | the lists `SUPERSEDED_NUMBERS.md` rests on |
| `SchwingNet/results/indomain/grid/scaling_curve_2026-09-17.json`; `SchwingNet/results/indomain/INVENTORY.md` lines 299-304 | tree 097933a | the 2026-09-17 sweep (C2.1) and its NOT ESTABLISHED marks |
| `SchwingNet/packet/`, `packet_cameraready/` (89 MB each), the 16 earlier `packet_build` PDFs | tree 097933a | regenerable submission packets; the two 2026-09-27 PDFs are copied into 01; the rest by path |
| `HANDOFF/` (184 tracked files) | 097933a | the eight student-readable files are copied whole into `docs/handoff/`; `MANUSCRIPTS.md`, `LITERATURE_STATE.md` + `literature_state/`, `RESEARCH_DIRECTIONS.md`, `CONTEXT_EXPORT.md`, `working_notes/` are Greg-only files copied whole into 01, 02, 07, 08 and 09; the sections assigned here are extracted in `docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md`; `HANDOFF/GREG_ONLY/` (untracked) is never copied |
| `HANDOFF/context/` (141 notes + `INDEX.md`, `COPIED_AT.txt`) | 097933a | the redacted memory copies; 28 copied into `memory/` |
| `docs/MODEL_CARD.md` section 4.6, section 5.3, section 6 | tree 097933a | the styled-corpus seed spread, the selective-prediction caveat, the unmeasured latency; owned by 01 |
| `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` lines 17-19, `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` | tree 097933a | why the v2 to v7 banks are leaked; owned by 10 |
| `docs/CONTINUANCE_2026-09-19.md` line 24 | tree 097933a | the RSNA fetch on the login node and the exposed Kaggle token |
| `tools/other_ct_fetch.py` lines 13-21, 200-241; `slurm/other_ct_fetch.sh`; `slurm/rsna_cspine_fetch.sh` | tree 097933a | the RSNA 2022 header census (every study refused) and the fetch script |
| `data_platform/DATA_MANIFEST.md` (card `rsna_2022_cspine`; line 1989 on the token), `MIGRATION_PLAN.md`, `LAYOUT.md`, `plan/batch_items/B08.tsv`, `B09.tsv`, `B14.tsv` | 097933a | the migration state of every path in `MANIFEST_GRID.md`; owned by 10 |

## 2. CTSpinoPelvic1K (public)

`https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K.git` (origin) and
`https://github.com/OpenSpineConsortium/CTSpinoPelvic1K.git` (osc), branch `master`, commit 7ddfe38 (2026-09-28); the
working tree had uncommitted edits on 2026-10-08 (the NeurIPS camera-ready, `checklist.tex`, `references.bib`,
`.gitignore`, the reprint-check PDF). Commits go directly to master and are pushed to both remotes, only when Greg asks.

| file | state at 7ddfe38 | what it is for this folder |
|---|---|---|
| `docs/HANDOFF_2026-09-21_PM.md` | untracked | the 1,551 B audit-track block of 2026-09-22 05:30; copied to `docs/checkpoints/HANDOFF_2026-09-21_PM_ctsp_audit_track.md` |
| `TechFair_LSTV_Schwing.pptx` | untracked | copied to `manuscripts/talks/` (the one copy) |
| `docs/CASTELLVI_SCREEN_BLIND_SPOT.md` | tracked | the refuted pelvic Castellvi cues (D.21); owned by 06 |
| `docs/LAB_JOURNAL.md` "Negative results"; `scripts/sweep_foramina_params.py` | tracked | sacral foramina counting refuted (F.39; 93 cases x 81 settings); owned by 03 / 05 |
| `docs/ROADMAP.md` | tracked | still says MLHC "in review, score 2.75/4": stale; the outcome is rejected (contradiction C8) |
| `mlhc/full-paper-template.tex`, `_paper_text.txt`, `_rebuttal_r2.txt`, `_rebuttal_r3.txt`, `_rebuttal_f65r.txt` | tracked / untracked | the MLHC 2026 submission and rebuttals (rejected; `docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md` section 8); owned by 03 |
| `paper/cns2026/` | excluded from git (`.git/info/exclude`, since 45df97d) | the CNS 2026 deck generators; copied into `03/manuscripts/talks/cns2026/`; never pushed |
| `MDPA.pdf` (2026-09-16), `MDPA_OL.zip` (2026-09-06), `dist/` | untracked / regenerable | superseded builds of the dataset article; by path only (`EXCLUDED.md` section 6) |
| `PIG/PIG_LEVELCHECK.pdf` | untracked | Goswami 2020, IEEE Access, with seven pig CBCT / CT / planar zips (about 205 MB); literature by path |
| the root literature PDFs, `MANUAL_REFS/`, `Spine chapters.zip` | untracked | `LITERATURE_BY_PATH.md` |
| `docs/ajnr.html`, `docs/ukb.html`, `docs/ids.txt`, `sp_978-3-030-00937-3_12.html`, `sp_978-3-030-87240-3_28.html` | untracked / tracked (not checked) | saved web pages and a 36-byte id list; not copied (ctsp r14) |
| `CLAUDE.md` | tracked | the source of the label-scheme, identifier-29, `zfill(4)`, orientation and grid rules restated in `CLAUDE.md` here |

## 3. OpenSpineToolkit (public)

`https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit.git` and `https://github.com/OpenSpineConsortium/OpenSpineToolkit.git`,
branch `main`, commit cb43197 (2026-09-25). Relevant here only as the home of `ostk.labels.labels_for(volume)` (the rule in
`CLAUDE.md`) and of commit 1b7005c (2026-09-10), the canal-closing regression recorded in the handoff timeline. The grid
copy has no `.git`, so its commit is not recorded; rsync from the laptop when needed.

## 4. XRSpinoPelvic1K (private)

`https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K.git`, branch `main`, commit 4f22935 (2026-08-15). Relevant here:
`journal.pone.0347290.pdf` (1,784,881 B; CC-BY; copied into `07_plain_film_level_id`; listed in `LITERATURE_BY_PATH.md`);
`dataset2024.zip` (4.0 GB; identity not recorded); five untracked and one tracked Cerner `.ica` session files that Greg
rotates (`PLAN.md` section 6).

## 5. The older and side repositories

| repository | URL | branch, commit | why it is named here |
|---|---|---|---|
| spinesurg-ct-annotator | `https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-annotator.git` | `master`, 1083c4f (2026-04-24) | the April 2026 annotator, superseded by `review_service/` + `reviewtool/` in CTSpinoPelvic1K; its grid backup is `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` (2026-08-10); its `assignments.json` carries student names (never copied); owned by 11 as a reference |
| SpineSurg-CT | `https://github.com/Gregory-Schwing-MD-PhD/SpineSurg-CT.git` | `main`, 0051074 (2026-04-09; 136 commits) | the ancestor in substance of CTSpinoPelvic1K (the COLONOG matching and mask fusion, the March 2026 arXiv draft `SpineSurgCT_arxiv.tex`, copied into `03/manuscripts/spinesurgct_arxiv_2026-03/`); the literature PDFs beside the checkout are in `LITERATURE_BY_PATH.md` |
| lstv-detector | `https://github.com/Gregory-Schwing-MD-PhD/lstv-detector.git` | `no_angles`, 84636d6 (2026-06-13) | the older MRI LSTV project (RSNA 2024 lumbar MRI); its cohort CSVs are owned by 06; named here because `docs/handoff/DATASET_USAGE.md` section 7 keeps it out of the CT table |
| spine-level-ai | `https://github.com/Gregory-Schwing-MD-PhD/spine-level-ai.git` | `master`, 5043793 (2026-02-09, the only commit) | the AACA 2026 LSTV MRI plan (a YOLOv8 landmark plan for the March 3 deadline) under `nsurg/AACA`; the Tech Fair deck grew from this line |
| lstv-annotation-tool | `https://github.com/Gregory-Schwing-MD-PhD/lstv-annotation-tool` | commit not recorded (five working copies of 2026-02-14) | the AACA-era annotation tool |
| openspineconsortium.github.io | `https://github.com/OpenSpineConsortium/openspineconsortium.github.io.git` | `master`, c1800f8 (2026-10-02) | `contributions/manifest.json` (2026-05-19) lists the twelve CNS 2026 abstracts (`docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md` section 13.1); owned by 12 |
| beethoven, beethoven-vscode | `https://github.com/OpenSpineConsortium/beethoven`, `.../beethoven-vscode` | release 14.0.0 (2f90319, 2026-10-03; `docs/handoff/INFRASTRUCTURE.md` section 1) | the superseded `AshleyBridge-6.0.0-tester-package.zip` and `Ashley Bridge for testers/` are kept by path only (`EXCLUDED.md` section 6); owned by 11 |
| Multi-View-Vertebra | upstream URL not recorded | grid clone of 2026-09-13 at `/wsu/home/go/go24/go2432/Multi-View-Vertebra` | the MICCAI 2023 reference code; the sequence loss the ladder design excludes |
| spine-program | the private repository this folder lives in; URL not recorded (Greg creates and pushes it) | — | `_plan/PLAN.md`, `DISPOSITION.tsv`, `EXCLUDED.md`, `ROOT_FILES.md` are the division this folder follows |

No code in this folder is run. `code/fuc/` holds a 2026-02-14 viewer bug note and a fixed JavaScript file from a
folder that was never a repository (`MANIFEST_LOCAL.md`); its successor is the NiiVue PACS demo owned by 12.
