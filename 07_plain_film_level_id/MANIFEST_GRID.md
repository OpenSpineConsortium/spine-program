# MANIFEST_GRID.md: every grid path this project uses or produced

Grid: `go2432@grid.wayne.edu`. HOME = `/wsu/home/go/go24/go2432` (Panasas, 4,050.75 GB of a
4,294.97 GB soft quota on 2026-10-08 22:20 UTC, `pan_quota`). Ceph = `/rs/rs_grp_oschome/go2432`
(20 TB volume `rs_grp_oschome`, 7 TB used, 39.39 %, `df-ceph`). Both readings are from the one
read-only pass of 2026-10-08 22:20 UTC. GRIDLS below is that raw listing,
`10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` (3,213 lines; its script
`grid_remote_ls.sh` and a condensed copy sit beside it); the condensed inventory built from it is
`_plan/GRID_MANIFEST_2026-10-08.md`. A second read-only `ls` and `squeue` at 01:25 UTC 2026-10-09 is
cited where it changed a row.
Sizes come from the files named in each row; "census" means the 2026-10-07 census of the data
platform; "du 2026-09-19" means `DATA_MANIFEST.md` of `spinesurg-ct-nnunet` 097933a. "not sized"
means no file records a size.

Migration vocabulary (`spinesurg-ct-nnunet/data_platform/MIGRATION_PLAN.md` section 3): a batch
copies with `rsync -aH`, verifies counts, sizes, links and a hashed sample, writes
`data_platform/plan/runs/<B>/STATUS` (VERIFIED / ABSENT per item), then cuts over (the HOME path
becomes `<path>.pre-ceph` plus a symlink); FINALIZE deletes the `.pre-ceph` copy. **No batch was
finalized on 2026-10-08.** The three `dp_migrate` jobs running at 22:20 UTC (40580669, 40580671,
40580673, partition `reqp`, 12 h 28 min elapsed) are inferred to be B04, B07 and B09; `plan/runs/B04/STATUS`
did not exist yet (GRIDLS). At 01:25 UTC 2026-10-09 the same three jobs were still RUNNING at 15 h 36 min
(`squeue -u go2432`, read-only). Truth for any batch is its STATUS file on the grid, read in a job or with
`cat`, never with Python on the login node.

Restriction flags are those of `data_platform/plan/batch_items/*.tsv`: `restricted` = owner-only on
Ceph after `publish_visibility.sh` (BUU pixels, VinDr DUA, banks holding their pixels); `candidate` =
a deletion candidate Greg decides on.

## 1. HOME: the film corpora and the detector tree

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spine-detector` | private repository checkout (`.git` 2026-09-12; `export_onnx.py`, `make_v4.py`, `shrink_onnx.py`, `slurm_export640.sh`, `scripts/`, `slurm/`, `src/`, `tests/`, `configs/`, `logs/`, `dist/`, `onnx_out/`, `weights/`); base weights `yolo11m-pose.pt` 42,459,307 B and `yolo11m.pt` 40,684,120 B | 382 GB (du 2026-09-19) | HOME stays for the checkout; the data moves in B04 (below) | `ls` 2026-10-08 (GRIDLS); the local snapshot's commit is not recorded (OPEN_QUESTIONS, plan section 7) |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/{aasce, buu_full, buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}` and `buu_2000 -> /wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/BUU-LSPINE` | the eleven film corpora as downloaded; `nhanes_full` is a 2,334,720-byte directory entry (about 17,000 TIFFs); `vindr` is DUA | B04 estimates: nhanes_annotated 159.0 GB (candidate), nhanes_full 91.0, vindr 48.0 (restricted), spinal_ai2024 2.7, lateral_236 1.3, mendeley_716 0.2, cm_spine 0.0 (candidate); csxa, buu_full (restricted), buu_v1 (restricted, candidate), aasce not sized (`plan/batch_items/B04.tsv`) | **B04 copying** at 22:20 UTC 2026-10-08; targets `$RS/data/{nhanes2_zenodo_landmarks, nhanes2_cdc_films, vindr_spinexr, spinal_ai2024, ieee_dataport_lateral_fullspine_236, csxa_cervical_xray_atlas, buu_lspine_3600, buu_lspine_v1_smoke, aasce2019_boostnet, cm_spine_drive_file}/raw/...` were all absent on Ceph; `$RS/data/mendeley_5jdfdgp762/raw` existed (filled by B14); `$RS/data/_staging/B04` existed with 2 entries | sources real directories in `ls` 2026-10-08; no STATUS yet |
| `/wsu/home/go/go24/go2432/spine-detector/data/interim` (`images/`, `manifest.parquet` rebuilt 2026-09-07: 33,943 instances on 5,401 films) and `data/{yolo, yolo_v2, yolo_v3, yolo_v4z, yolo_v5f_p00, yolo_v5f_p05, yolo_v5f_p08, yolo_v6f, yolo_hw, yolo_hw_fluoro, yolo_dr_s00f00, yolo_dr_s00f05, yolo_dr_s08f00, yolo_dr_s08f05, yolo_dr_s08f05x2}` | the corpus manifest and 16 YOLO export sets (`DATA_MANIFEST.md` card `spine_detector_corpus`) | not sized | B04 -> `$RS/data/spine_detector_corpus/derived/{interim, yolo*}` (restricted; `yolo*` a hard-link group); target absent 2026-10-08 | `ls` 2026-10-08 lists the 16 names |
| `/wsu/home/go/go24/go2432/spine-detector/runs/{detect, detect_v1, detect_v2, pose, g3, lcurve, coverage, eval_h2h, wholespine, realxray, devcorpus}` | `detect_v1` (the report in this folder, 2026-08-30 training); `detect_v2` (2026-09-08: AP50 0.970, PCK@0.1 0.812, PCK@0.2 0.942; weights `runs/pose/runs/detect_v2/weights/best.pt`; eval in `runs/detect_v2/eval/{metrics.json, report.txt, renders/}`, `memory/xray-corner-detector-status.md`); `realxray/rx_*` and `devcorpus/dc_*` are folder 01's real-frame and device-corpus detectors (not in the registry) | not sized | B13 (results, optional, 627 GB in all) not run; HOME | names listed 2026-10-08 (GRIDLS) |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K` | private repository checkout of 2026-08-10: `annot/`, `configs/`, `containers/`, `docker/`, `docs/`, `examples/`, `logs/` (36,864-byte entry), `nextflow/`, `pylibs/` (18 entries), `scripts/`, `slurm/`, `tests/`, `weights/`, `xrsp/`, `.scratch/` (51 entries), `Makefile`, `yolo11n.pt` 5,613,764 B; **tracked junk**: `Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica` 2,017 B (a Cerner session file) and `Unconfirmed 31234.crdownload` 2,749,895 B | 22.428 GB (census) | HOME stays for the checkout; `data/` moves in B05 (below) | `ls` 2026-10-08 (GRIDLS) |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data` | `BUU-LSPINE/` (the 2,000-pair subset), `dataset2024.zip` 4,023,726,207 B (identity not recorded), `buu_splits.json` 53,434 B (the 1398 / 301 / 301 split every number in `docs/xrspinopelvic1k/docs/RESULTS.md` rests on), `buu_yolo/`, `drr_yolo/`, `results/` (6 entries), `results_extrapolate/`, `results_standing_640/`, `results_standing_single/`, `results_standing_tiled/`, `runs/` (9 entries), `web_models/`, `web_ref/`, `xrsp1k/` (the 6,416 lateral DRRs of 822 pre-release cases, `MANIFEST_DATA_MODELS_RESULTS.md` line 198; directory entry 114,688 B, 804 links, dated 2026-08-07 08:26), `thoracic_cases.json` 252 B, `combined.yaml` 255 B, `README.md` 619 B; `ct -> /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/hf_export_v3/ct` and `labels -> .../hf_export_v3/labels` **dangle** (hf_export_v3 deleted in the B02 reclaim; built from 822 pre-release cases, `DATA_MANIFEST.md` defect 36) | in the 22.428 GB above | **B05 not started** (depends on B04): `dataset2024.zip` -> `$RS/data/buu_lspine_2000/raw/dataset2024.zip` (4.7 GB est., candidate); `BUU-LSPINE` -> `$RS/data/buu_lspine_2000/raw/BUU-LSPINE` (restricted); `xrsp1k` -> `$RS/data/xrspinopelvic1k/derived/xrsp1k` (`plan/batch_items/B05.tsv`); `$RS/data/buu_lspine_2000` absent 2026-10-08 | `ls` 2026-10-08; `xrsp1k` **present, unsized** (a read-only `ls` at 01:25 UTC 2026-10-09): the 22:20 listing missed it because `grid_remote_ls.sh` line 63 cuts that `ls` at `head -80` and `xrsp1k` sorts last; B05 moves it to `$RS/data/xrspinopelvic1k/derived/xrsp1k` |
| `/wsu/home/go/go24/go2432/dis_renders -> /rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived/dis_renders` (and `dis_renders.pre-ceph`, 2026-08-11) | five PNGs named by BUU films; what drew them is not recorded | 5 files 10,869,856 B | B14 item 002 **VERIFIED** (`VERIFY_OK files 5/5 bytes 10869856/10869856 sampled 5`; flags restricted, candidate); cut over 2026-10-08 11:02; not finalized | STATUS line read in GRIDLS |

## 2. HOME: films in render format and the crop banks (all read by the level encoders)

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/films_drr` | 9,109 real films in the render format: CSXA 4,963 + BUU 3,603 lateral + NHANES 543; every level bank reads it | 36 GB (`docs/handoff/RECIPES.md` section 5) | B11 -> `$RS/data/multisource_banks/derived/films_drr` (restricted); **not started**; `$RS/data/multisource_banks` absent 2026-10-08 | listed 2026-10-08 (dir 2026-09-13) |
| `/wsu/home/go/go24/go2432/films_drr_buucorr` | the schema-corrected BUU copy (`S1a -> L6`, `transitional: sacralised`, flagged `needs_review`; `tools/correct_buu_schema.py`); no review verdicts recorded | not sized | B11 (restricted) | listed (dir 2026-09-17) |
| `/wsu/home/go/go24/go2432/films_ap_drr` | the 3,600 BUU AP films in render format; in no bank; never used (`DATASET_USAGE.md` section 2.1; OPEN_QUESTIONS E5) | 11.325 GB (census) | B10 -> `$RS/data/buu_lspine_3600/derived/films_ap_drr` (restricted); not started | listed |
| `/wsu/home/go/go24/go2432/films_ann_fov96_ctx` | the CSXA + NHANES crop bank (28,032 crops = 19,610 train + 8,422 val); **the bank behind C1.1 and C1.2** (the 96.7 % ladder and the 98.69 / 99.13 / 99.41 / 99.48 % recurrent head) | 13.861 GB (census); dedup A18 | B11 (no restriction flag); not started | listed (dir 2026-09-13) |
| `/wsu/home/go/go24/go2432/films_all2_fov96_ctx` | the cervical + lumbar film bank with the full eight-rung ladder (49,719 crops, 9,853 films, `results/track5_results/bank_audit_films_all2.txt`); produced C1.3 (98.84 / 99.13 / 99.42 / 99.38 %) and C1.10; wrongly credited with C1.2 | 26.278 GB (census); rungs 3, 4, 6, 8 likely byte twins of rung 2 (dedup A17) | B11 (restricted); not started | listed |
| `/wsu/home/go/go24/go2432/films_all2_fov128m_ctx` | empty | 0 | B11 (candidate) | listed (dir 2026-09-14) |
| `/wsu/home/go/go24/go2432/films_smoke` | a smoke bank | not sized | B10 -> `csxa_cervical_xray_atlas/derived/films_smoke` (candidate) | listed |
| `/wsu/home/go/go24/go2432/allspine_fov96_ctx` (v1), `allspine_v6_fov96_ctx`, `allspine_v7_fov96_ctx`, `allspine_v7nofluoro_fov96_ctx`, `allspine_v8_fov96_ctx` | the all-spine banks: v1 4.542 GB; v6 23.018 GB (leaked: NHANES twins, 48 of 54 validation patients); v7 9.117 GB (leaked); v7nofluoro 31.068 GB (the FluoroCap ablation bank); v8 5.494 GB (VerSe keyed by series: 5 people on both sides; dedup A22 unsettled); **v2 through v5c were deleted 2026-09-20** (206.5 GB; `memory/`-adjacent note `grid-quota-and-deleted-banks` in folder 10) | census values as given | B11 (restricted; v1, v6, v7nofluoro candidates); not started | listed |
| `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` | the current level bank (folder 01 owns it); the film N-curve reads its `rung_1.npz` and `meta.json` | not sized here | B11 (restricted) | listed |
| `/wsu/home/go/go24/go2432/buu_fov96_ctx`, `buu_yolo` | the BUU crop bank (9.981 GB) and the BUU YOLO export (3.960 GB) | census | B10 -> `buu_lspine_3600/derived/` (restricted) | listed (dirs 2026-09-13, 2026-09-18) |
| `/wsu/home/go/go24/go2432/extra_fov96_ctx` | extra crop bank | 12.282 GB (census) | B11 (restricted) | listed |
| `/wsu/home/go/go24/go2432/vindr_fov96_ctx`, `vindrps_fov96_ctx`, `vindr_pseudo`, `vindr_pseudo_drr`, `vindr_det_drr`, `vindr_lat_ids.txt`, `vindr_views.csv`, `vindr_variant_audit.json` | the VinDr-SpineXR banks (744-film crop bank; `vindrps` carries a 77.8 % validation leak and never re-enters a bank) and tables; DUA | not sized | B10 -> `vindr_spinexr/{derived, meta}` (restricted); not started | listed |
| `/wsu/home/go/go24/go2432/nhanes_pseudo`, `nhanesps_fov96_ctx`, `nhanes_ctx`, `nhanes_split_ctx`, `nhanes_drr`, `nhanes_pvariant_strata.json` | 16,530 pseudo-labelled NHANES films (fed only the deleted v5) and their banks | `nhanes_pseudo` 74 GB (du 2026-09-19) | B10 -> `nhanes2_cdc_films/derived`, `nhanes2_zenodo_landmarks/derived`; not started | listed |
| `/wsu/home/go/go24/go2432/mendeley_fov96_ctx`, `mendeley_drr`, `lat236ps_fov96_ctx`, `lateral236_pseudo`, `aasce_fov96_ctx`, `aasce_drr`, `spinalai_drr` | the Mendeley (excluded from training by directive D6), lateral-236, AASCE and Spinal-AI2024 banks | `spinalai_drr` 4.4 GB, `mendeley_drr` 1.3 GB (B10.tsv); rest not sized | B10; not started | listed |
| `/wsu/home/go/go24/go2432/m_fov96_ctx`, `m_mask22_scale_ctx`, `merged_ctx`, `verse_ctx`, `verse_only_ctx_plus_nh`, `sd_fov96_ctx`, `mv_bands`, `pseudo_filtered`, `yolo_levels`, `sacrum_yolo`, `quiz_pack`, `reader_study`, `review_pack`, `review_pack_v2`, `review_pack_smoke`, `verify_bench`, `film_style_ds` | B11 banks and the review / quiz / reader-study packs (roles per `DATA_MANIFEST.md` Appendix A); `yolo_levels` 6.7 GB; `film_style_ds` 0.962 GB | as given; rest not sized | B11; not started | listed |
| `/wsu/home/go/go24/go2432/scaling` | the 2026-09-17 subset banks of the deleted v2 (the fraction sweep, C2.1); the trap of RECIPES section 1.8: a rerun that finds these re-emits the leaky curve | 129.2 GB (B11.tsv) | B11 (candidate); not started | listed |
| `/wsu/home/go/go24/go2432/split_final.json`, `patient_keys*.json`, `bank_splits.json` | the identity tables (the G3 person split is FROZEN, job 40426793) | small | B11 | listed |

## 3. HOME: result files behind the RECORD ONLY rows of `STATUS.md` (none re-read on 2026-10-08)

| path | holds | STATUS.md row |
|---|---|---|
| `/wsu/home/go/go24/go2432/tmp/ladder_summary.json` | the context-ladder result on `films_ann`; **not found on 2026-10-08** (a read-only `ls` at 01:25 UTC 2026-10-09; `~/tmp` itself is present with 268 entries); the memory note `level-id-2d-results-2026-09-13.md` and RESULTS_CATALOG C1.1 are the only record | C1.1 |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json`, `recurrent_all2.json`; `bench/robust/*.json`; `bench/model_registry.md` (M96) | the recurrent-head results (job 40215812, 2026-09-13 13:28, log prints `embedded 28032 crops`), the corruption suite; `~/bench` 35.8 GB | C1.2, C1.3, C1.10 |
| `/wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json`; `model_night/recurrent_allspine_v2.json`; `model_night/stc/`; `model_night/interior_windows/`; `model_night/panel_stats/`; `model_night/scaling/SCALING_CURVE.json`; `model_night/ensemble/ensemble.json` (listing truncated; OPEN_QUESTIONS B6); `model_night/heads_mixed/` (not reached); `model_night/figures_feasibility/` (whether `fig9_scaling` was drawn: not recorded, B13) | the model-night arms on allspine v2 | C1.4, C1.5, C1.7, C1.14, C1.11, C2.1, C1.17 |
| `/wsu/home/go/go24/go2432/selective/SELECTIVE.md` | selective prediction on the leaked v2 bank (job 40291753) | C1.8 |
| `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`, `LEARNING_CURVE.md`, `sources/buu3600_lstv_labels.csv` | the 2-D LSTV / TLTV flags (refuted) and their learning curve (date and job not recorded) | C1.12, C1.13 |
| `/wsu/home/go/go24/go2432/track5/track5_recurrent_frozen.py` | the frozen Track 5 script, sha256 `fc6e4ddc…` = `tools/recurrent_order.py` at the time (`results/track5_results/frozen_sha.txt`) | `results/track5_results/` |
| `/wsu/home/go/go24/go2432/scaling_curves/` | `eval_scaling_curves.py` outputs (devices / cases / fewshot) | C2.3 |
| `/wsu/home/go/go24/go2432/FluoroCap/detect_v5z_*_best.pt`, `detect_v6f_best.pt`; `/wsu/home/go/go24/go2432/level_id_service/weights/detector.pt` | HOME copies of the later detector weights (`DATA_MANIFEST.md` card `spine_detector_corpus`); FluoroCap itself was B09 copying | folder 01 |

## 4. HOME: the model registry entries of this line

`/wsu/home/go/go24/go2432/model_registry/<sha16>/` with `registry.jsonl` (106 lines; a sync loop
re-registered `orientation_net_v2` sixteen times, so 106 lines is not 106 models) and `aliases/`
(79 symlinks); MLflow `/wsu/home/go/go24/go2432/mlflow/mlflow.db` 1,028,096 B. All from GRIDLS
`ls ~/model_registry`, `aliases`, `registry.jsonl` (2026-10-08).

| alias | store | bytes | role |
|---|---|---|---|
| `films_all2_rung1_aug2` | `d081b4ab18b331a7/model_rung_1_aug2.pt` (registered 2026-09-15 05:55:27 from `films_all2_fov96_ctx/runs/`) | 44,824,746 | superseded film encoder |
| `films_all2_rung1` | `3654e9ba4c64d2d5/model_rung_1.pt` | 44,824,116 | superseded |
| `films_all2_rung2_aug2` | `964e17f18bdc3f4e/model_rung_2_aug2.pt` | 44,824,746 | superseded |
| `films_all2_rung2` | `de9a5dfe03e6a691/model_rung_2.pt` | 44,824,116 | superseded |
| `recurrent_head_films_all2_r1` | `f4ec9180c718ea8b/recurrent_head_films_all2_fov96_ctx_d081b4ab_r1.pt` | 8,473,844 | **the registered head is a films_all2 head**; the 98.7 / 99.1 / 99.4 % of C1.2 was measured on `films_ann` and its weights were never saved (OPEN_QUESTIONS F5) |
| `detector_v5z_final` | `797de71a9e0e42f7/detect_v5z_final_best.pt` | 42,233,939 | the SchwingNet body detector (folder 01) |
| `detector_v5z_epoch25` | `5fde3060dbc15b71` | 168,005,677 | shipped in `level_id_service` |
| `detector_v6f` | `479db0ab0d2b4c2f` | not recorded | the FluoroCap self-training arm |
| `competitor_cina`, `competitor_kim`, `competitor_vertx` | `8f17aa30…`, `30b981af…`, `f0267ca3…` (2026-09-18) | not recorded | the re-implemented published competitors (C1.17) |
| `allspine_v2_r1` | `00e84a90afa7ec52` | not recorded | the v2 encoder; its bank is deleted and `eval_gate.py` refuses it |
| `allspine_v8_fov96_ctx_rung_1_aug2` | `a8f55ab9c546f192` | not recorded | the v8 encoder behind A15 (selection split) |
| `allspine_v9_fov96_ctx_rung_1_aug2` | `188f9fcbfa3c6de1/model_rung_1_aug2.pt` (2026-09-23) | not recorded | the current encoder (folder 01) |

Not in the registry: `detect_v1`, `detect_v2` (`spine-detector/runs/`), the real-frame detectors
`runs/realxray/rx_*`, the device-corpus detectors `runs/devcorpus/dc_*`, the shipped head
`head_allspine_v9_mixed_kmax4_seed0` (`model_night/heads_mixed/`, not reached by the listing).
Mirror: the private Hugging Face repository `gregoryschwingmdphd/level-id-weights`
(`docs/MODEL_REGISTRY.md` of `spinesurg-ct-nnunet`); not checked, no network was used.

## 5. Ceph: what is already there

| path | holds | size | state | verified |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/inventory/films/` | `FILM_CORPUS_INVENTORY.md` 2,839 B, `nhanes_film_manifest.csv` 2,109,890 B, `vindr_film_manifest.csv` 1,388,674 B, `film_corpus_inventory.json` 3,362 B, `box_convention/` (9 entries); all 2026-09-23 (job 40416535, `DATASET_USAGE.md` section 8) | about 3.5 MB | Ceph-native | `ls` 2026-10-08 |
| `/rs/rs_grp_oschome/go2432/data/inventory/vindr_age_sex.csv` | the VinDr age and sex table, DUA-derived: never redistribute | 830,061 B (2026-09-24) | Ceph-native | `ls` 2026-10-08 |
| `/rs/rs_grp_oschome/go2432/data/thoracic_xr` | the AASCE open mirror (609 labelled films) | 0.859 GB (census); 962 files byte-identical to the HOME copy (dedup A15) | Ceph-native | listed (dir 2026-09-22) |
| `/rs/rs_grp_oschome/go2432/data/vindr` | a three-file placeholder, **not** the DUA data (that is still `spine-detector/data/raw/vindr`, B04) | 0.002 GB | Ceph-native | listed |
| `/rs/rs_grp_oschome/go2432/data/mendeley_5jdfdgp762/raw/spondy_landmark` | the second download of Mendeley 5jdfdgp762 (`~/data/spondy_landmark` cut over) | 1,416 files 89,020,337 B | B14 **VERIFIED** (candidate; duplicate of `mendeley_716` pending a sha check, dedup A14) | STATUS read in GRIDLS |
| `/rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived/dis_renders` | five PNGs named by BUU films (owner-only) | 5 files 10,869,856 B | B14 item 002 **VERIFIED**; restricted, candidate | STATUS read |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/obl2_fov96_ctx` | the oblique crop bank | 9 files 13,327,845,295 B | B06 **VERIFIED**, cut over | STATUS read |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/verse_only_ctx` | the VerSe-only crop bank | 42 files 743,721,823 B | B06 **VERIFIED**, cut over | STATUS read |
| `/rs/rs_grp_oschome/go2432/data/or_ready/film_ncurve/` | the film N-curve chain outputs: `cells.json`, `manifest.txt`, `render_bank/`, `test_ctx/`, `pool_*/`, `base_cache/`, `cells/<cell>/` with DONE markers, `film_ncurve.json`, `FILM_NCURVE.md` (2026-09-24 23:25; jobs 40437808 -> 40437809 -> 40437810 array 0-47 -> 40437811); `ablation/{imagenet, filmonly}/` (jobs 40451157, 40451158; collects 40451159, 40451160) | inside `or_ready` (868 GB) | Ceph-native (folder 01's result root) | not re-verified 2026-10-08; the copies the paper reads are `SchwingNet/results/coverage/film_ncurve/` in `spinesurg-ct-nnunet` 097933a |

## 6. Not on the grid, or not yet there

| item | evidence | what to do |
|---|---|---|
| The Ceph copies of every film corpus (`nhanes2_*`, `vindr_spinexr`, `spinal_ai2024`, `ieee_dataport_lateral_fullspine_236`, `csxa_cervical_xray_atlas`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `aasce2019_boostnet`, `cm_spine_drive_file`, `spine_detector_corpus`) | all absent in `ls` 2026-10-08 22:20 UTC; B04 copying | wait for the `dp_migrate` jobs; read `plan/runs/B04/STATUS`; then cut over (folder 10) |
| `$RS/data/buu_lspine_2000` and `$RS/data/xrspinopelvic1k/derived/xrsp1k` | B05 not started; the source `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/xrsp1k` is present on HOME (section 1) | after B04 |
| `/wsu/home/go/go24/go2432/tmp/ladder_summary.json`, the file behind C1.1 | absent (a read-only `ls` at 01:25 UTC 2026-10-09) | nothing to run: C1.1 is RECORD ONLY; `memory/level-id-2d-results-2026-09-13.md` and RESULTS_CATALOG C1.1 are its only record |
| `$RS/data/multisource_banks` (every `films_*`, `allspine_*`, the packs, `scaling`) and the B10 single-source banks | B10, B11 not started; `multisource_banks` absent | after B04, B06, B07 (`plan/migration_batches.csv` depends_on) |
| `allspine_v2`, `v3`, `v4`, `v5`, `v5c` | deleted 2026-09-20 (206.5 GB) | every number scored on them is LEAKED or SUPERSEDED; rebuildable from `slurm/build_allspine_v*.sh` but not wanted |
| `buu_drive` mirror (9.3 GB), `films_all4`, `extra3`, `extra4`, `obl_fov96_ctx`, `allspine_v2sd` | `layout_map.csv` row 126 `gone`; no deletion record | none needed |
| XRSpinoPelvic1K `data/ct`, `data/labels` | dangling links to the deleted `hf_export_v3` (822 pre-release cases) | rebuild from the v11 tree with `labels_for` (TODO step 1) |
| a held-out per-level film table | OPEN_QUESTIONS C4 | a committed aggregation tool on held-out persons (TODO) |
| a clean selective-prediction run | OPEN_QUESTIONS C13 | re-run on the v9 lineage with coverage chosen on a separate split (TODO) |
| film N-curve seeds 1-2 at N >= 50; the synthetic:real ratio sweep | OPEN_QUESTIONS A9, C5, C6 | Greg's yes / no (TODO step 5) |
| the competitor ensemble result in any document | C1.17 NOT RECORDED; `~/model_night/ensemble/ensemble.json` unread (B6) | read it in a job |
| the VinDr-SpineXR determination number | OPEN_QUESTIONS A5 | Greg |
| the BUU licence reading | RESEARCH_DIRECTIONS section 6 (the closing paragraph) | Greg |
| a human level read on any real film | RESEARCH_DIRECTIONS unknown 4 | the review Space's ledger (`code/review_space/README.md`) holds student reads of pseudolabelled films; whether any were collected is not recorded here |
| FINALIZE of any batch | every `.pre-ceph` still present; HOME at 94 % | Greg's call per batch (OPEN_QUESTIONS A26) |

## 7. Credentials on the grid this folder must act on (paths only, never contents)

Two items: `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica` (a Cerner session
file tracked at 4f22935: purge from history and from the grid clone, `TODO.md` step 1) and
`/wsu/home/go/go24/go2432/github` (41 B, mode 600 since 2026-10-08: rotate and delete). Every other credential path on the
grid is listed once, in `_plan/PLAN.md` section 6, and not repeated here.
