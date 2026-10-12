# DATA.md: this folder's data on the grid, reached through Beethoven

How a reader reaches the grid material of `07_plain_film_level_id` and runs the first measurement:
the XRSpinoPelvic1K corner-detector evaluation on the 301 held-out BUU films (`STATUS.md` section 1b;
`TODO.md` step 5). This folder is Greg-only (`CLAUDE.md` first paragraph); a student claims work here
only after Greg confirms a hand-out. Nothing below runs on the login node: every computation, render
and plot is an `sbatch -D <dir>` job (`CLAUDE.md` rule 7).

The paths below are every row of `MANIFEST_GRID.md` sections 1 to 5, spelled as that manifest spells
them: HOME = `/wsu/home/go/go24/go2432` (Panasas), Ceph = `/rs/rs_grp_oschome/go2432` (the 20 TB
volume `rs_grp_oschome`). What each path holds, its size and its migration state come from
`MANIFEST_GRID.md`, whose one read-only pass is 2026-10-08 22:20 UTC (GRIDLS), with a second
read-only `ls` and `squeue` at 01:25 UTC 2026-10-09 cited where it changed a row; what no file
records is written "not recorded". The migration state at that read: **B04 copying; B05, B10, B11
not started on 2026-10-08** (`MANIFEST_GRID.md` header and sections 1-2). The state of each batch
since is `../10_data_platform_grid/MANIFEST_GRID.md` section 2. Truth for any batch is its
STATUS file, `data_platform/plan/runs/<B>/STATUS`, read in a job or with `cat`, never with python on
the login node.

Every check line below is read-only (`ls -ld <path>` for a directory or a link, `head -c 200 <file>`
for a file) and runs from the Beethoven worker — a session on a compute node — never python on the
login node. Set once, then paste a check line:

```
H=/wsu/home/go/go24/go2432; C=/rs/rs_grp_oschome/go2432
```

A check line on a HOME path works only for Greg: nothing on HOME is readable by students (see
"Access", below). Every HOME row is therefore marked **on HOME, not reachable until migrated**, with
the manifest's migration state beside it.

## 1. HOME: the film corpora and the detector tree (`MANIFEST_GRID.md` section 1)

| path | volume | what it holds | size | migration state | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spine-detector` | HOME | the private spine-detector repository checkout (`.git` 2026-09-12; `export_onnx.py`, `make_v4.py`, `shrink_onnx.py`, `slurm_export640.sh`, `scripts/`, `slurm/`, `src/`, `tests/`, `configs/`, `logs/`, `dist/`, `onnx_out/`, `weights/`); base weights `yolo11m-pose.pt` 42,459,307 B and `yolo11m.pt` 40,684,120 B; the local snapshot's commit is not recorded | 382 GB (du 2026-09-19) | on HOME, not reachable until migrated; HOME stays for the checkout, the data moves in B04 | `ls -ld $H/spine-detector` |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/{aasce, buu_full, buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}` and `buu_2000 -> /wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/BUU-LSPINE` | HOME | the eleven film corpora as downloaded; `nhanes_full` is a 2,334,720-byte directory entry (about 17,000 TIFFs); `vindr` is DUA | B04 estimates (`plan/batch_items/B04.tsv`): nhanes_annotated 159.0 GB (candidate), nhanes_full 91.0, vindr 48.0 (restricted), spinal_ai2024 2.7, lateral_236 1.3, mendeley_716 0.2, cm_spine 0.0 (candidate); csxa, buu_full (restricted), buu_v1 (restricted, candidate), aasce not sized | on HOME, not reachable until migrated; **B04 copying** at 22:20 UTC 2026-10-08; the targets `$RS/data/{nhanes2_zenodo_landmarks, nhanes2_cdc_films, vindr_spinexr, spinal_ai2024, ieee_dataport_lateral_fullspine_236, csxa_cervical_xray_atlas, buu_lspine_3600, buu_lspine_v1_smoke, aasce2019_boostnet, cm_spine_drive_file}/raw/...` were all absent on Ceph at that read; `$RS/data/mendeley_5jdfdgp762/raw` existed (filled by B14) | `ls -ld $H/spine-detector/data/raw` |
| `/wsu/home/go/go24/go2432/spine-detector/data/interim` (`images/`, `manifest.parquet` rebuilt 2026-09-07: 33,943 instances on 5,401 films) and `data/{yolo, yolo_v2, yolo_v3, yolo_v4z, yolo_v5f_p00, yolo_v5f_p05, yolo_v5f_p08, yolo_v6f, yolo_hw, yolo_hw_fluoro, yolo_dr_s00f00, yolo_dr_s00f05, yolo_dr_s08f00, yolo_dr_s08f05, yolo_dr_s08f05x2}` | HOME | the corpus manifest and 16 YOLO export sets (`DATA_MANIFEST.md` card `spine_detector_corpus`) | not sized | on HOME, not reachable until migrated; B04 -> `$RS/data/spine_detector_corpus/derived/{interim, yolo*}` (restricted in the plan; readable by approved students after job 40599886; `yolo*` a hard-link group); target absent 2026-10-08 | `ls -ld $H/spine-detector/data/interim` |
| `/wsu/home/go/go24/go2432/spine-detector/runs/{detect, detect_v1, detect_v2, pose, g3, lcurve, coverage, eval_h2h, wholespine, realxray, devcorpus}` | HOME | `detect_v1` (the report in this folder, 2026-08-30 training); `detect_v2` (2026-09-08: AP50 0.970, PCK@0.1 0.812, PCK@0.2 0.942; weights `runs/pose/runs/detect_v2/weights/best.pt`; eval in `runs/detect_v2/eval/`); `realxray/rx_*` and `devcorpus/dc_*` are folder 01's detectors (not in the registry) | not sized | on HOME, not reachable until migrated; B13 (results, optional, 627 GB in all) not run | `ls -ld $H/spine-detector/runs/detect_v2` |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K` | HOME | the private XRSpinoPelvic1K repository checkout of 2026-08-10: `annot/`, `configs/`, `containers/`, `docker/`, `docs/`, `examples/`, `logs/`, `nextflow/`, `pylibs/`, `scripts/`, `slurm/`, `tests/`, `weights/`, `xrsp/`, `.scratch/`, `Makefile`, `yolo11n.pt` 5,613,764 B; **tracked junk**: `Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica` 2,017 B (a Cerner session file, never copied; TODO step 1) and `Unconfirmed 31234.crdownload` 2,749,895 B | 22.428 GB (census) | on HOME, not reachable until migrated; HOME stays for the checkout, `data/` moves in B05 | `ls -ld $H/XRSpinoPelvic1K` |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data` | HOME | `BUU-LSPINE/` (the 2,000-pair subset), `dataset2024.zip` 4,023,726,207 B (identity not recorded), `buu_splits.json` 53,434 B (the frozen 1398 / 301 / 301 split every number in `docs/xrspinopelvic1k/docs/RESULTS.md` rests on), `buu_yolo/`, `drr_yolo/`, `results/`, `results_extrapolate/`, `results_standing_640/`, `results_standing_single/`, `results_standing_tiled/`, `runs/`, `web_models/`, `web_ref/`, `xrsp1k/` (the 6,416 lateral DRRs of 822 pre-release cases; present, unsized, by the 01:25 UTC 2026-10-09 `ls`), `thoracic_cases.json` 252 B, `combined.yaml` 255 B, `README.md` 619 B; the links `ct ->` and `labels -> .../hf_export_v3/...` **dangle** (hf_export_v3 deleted in the B02 reclaim) | in the 22.428 GB above | on HOME, not reachable until migrated; **B05 not started** (depends on B04): `dataset2024.zip` -> `$RS/data/buu_lspine_2000/raw/dataset2024.zip` (4.7 GB est., candidate); `BUU-LSPINE` -> `$RS/data/buu_lspine_2000/raw/BUU-LSPINE` (restricted in the plan; readable by approved students after job 40599886); `xrsp1k` -> `$RS/data/xrspinopelvic1k/derived/xrsp1k`; `$RS/data/buu_lspine_2000` absent 2026-10-08 | `head -c 200 $H/XRSpinoPelvic1K/data/buu_splits.json` |
| `/wsu/home/go/go24/go2432/dis_renders -> /rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived/dis_renders` (and `dis_renders.pre-ceph`, 2026-08-11, until B14's FINALIZE) | HOME link to Ceph | five PNGs named by BUU films; what drew them is not recorded | 5 files 10,869,856 B | B14 item 002 **VERIFIED** (`VERIFY_OK files 5/5 bytes 10869856/10869856 sampled 5`; flags restricted, candidate); cut over 2026-10-08 11:02; finalized 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md` section 2); readable by approved students after job 40599886 | `ls -ld $H/dis_renders` |

## 2. HOME: films in render format and the crop banks (`MANIFEST_GRID.md` section 2)

All read by the level encoders. Every row is on HOME, not reachable until migrated.

| path | volume | what it holds | size | migration state | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/films_drr` | HOME | 9,109 real films in the render format: CSXA 4,963 + BUU 3,603 lateral + NHANES 543; every level bank reads it | 36 GB (`docs/handoff/RECIPES.md` section 5) | on HOME, not reachable until migrated; B11 -> `$RS/data/multisource_banks/derived/films_drr` (restricted in the plan; readable by approved students after job 40599867); **not started**; `$RS/data/multisource_banks` absent 2026-10-08 | `ls -ld $H/films_drr` |
| `/wsu/home/go/go24/go2432/films_drr_buucorr` | HOME | the schema-corrected BUU copy (`S1a -> L6`, `transitional: sacralised`, flagged `needs_review`; `tools/correct_buu_schema.py`); no review verdicts recorded | not sized | on HOME, not reachable until migrated; B11 (restricted in the plan; readable by approved students after job 40599867); not started | `ls -ld $H/films_drr_buucorr` |
| `/wsu/home/go/go24/go2432/films_ap_drr` | HOME | the 3,600 BUU AP films in render format; in no bank; never used (`DATASET_USAGE.md` section 2.1; OPEN_QUESTIONS E5) | 11.325 GB (census) | on HOME, not reachable until migrated; B10 -> `$RS/data/buu_lspine_3600/derived/films_ap_drr` (restricted in the plan; readable by approved students after job 40599886); not started | `ls -ld $H/films_ap_drr` |
| `/wsu/home/go/go24/go2432/films_ann_fov96_ctx` | HOME | the CSXA + NHANES crop bank (28,032 crops = 19,610 train + 8,422 val); **the bank behind C1.1 and C1.2** (the 96.7 % ladder and the 98.69 / 99.13 / 99.41 / 99.48 % recurrent head) | 13.861 GB (census); dedup A18 | on HOME, not reachable until migrated; B11 (no restriction flag); not started | `ls -ld $H/films_ann_fov96_ctx` |
| `/wsu/home/go/go24/go2432/films_all2_fov96_ctx` | HOME | the cervical + lumbar film bank with the full eight-rung ladder (49,719 crops, 9,853 films, `results/track5_results/bank_audit_films_all2.txt`); produced C1.3 and C1.10; wrongly credited with C1.2 | 26.278 GB (census); rungs 3, 4, 6, 8 likely byte twins of rung 2 (dedup A17) | on HOME, not reachable until migrated; B11 (restricted in the plan; readable by approved students after job 40599867); not started | `ls -ld $H/films_all2_fov96_ctx` |
| `/wsu/home/go/go24/go2432/films_all2_fov128m_ctx` | HOME | empty | 0 | on HOME, not reachable until migrated; B11 (candidate) | `ls -ld $H/films_all2_fov128m_ctx` |
| `/wsu/home/go/go24/go2432/films_smoke` | HOME | a smoke bank | not sized | on HOME, not reachable until migrated; B10 -> `csxa_cervical_xray_atlas/derived/films_smoke` (candidate) | `ls -ld $H/films_smoke` |
| `/wsu/home/go/go24/go2432/allspine_fov96_ctx` (v1), `allspine_v6_fov96_ctx`, `allspine_v7_fov96_ctx`, `allspine_v7nofluoro_fov96_ctx`, `allspine_v8_fov96_ctx` | HOME | the all-spine banks: v1; v6 (leaked: NHANES twins, 48 of 54 validation patients); v7 (leaked); v7nofluoro (the FluoroCap ablation bank); v8 (VerSe keyed by series: 5 people on both sides; dedup A22 unsettled); **v2 through v5c were deleted 2026-09-20** (206.5 GB) | v1 4.542 GB; v6 23.018 GB; v7 9.117 GB; v7nofluoro 31.068 GB; v8 5.494 GB (census) | on HOME, not reachable until migrated; B11 (restricted in the plan; v1, v6, v7nofluoro candidates; readable by approved students after job 40599867); not started | `ls -ld $H/allspine_v8_fov96_ctx` |
| `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` | HOME | the current level bank (folder 01 owns it); the film N-curve reads its `rung_1.npz` and `meta.json` | not sized here | on HOME, not reachable until migrated; B11 (restricted in the plan; readable by approved students after job 40599867) | `ls -ld $H/allspine_v9_fov96_ctx` |
| `/wsu/home/go/go24/go2432/buu_fov96_ctx`, `buu_yolo` | HOME | the BUU crop bank and the BUU YOLO export | 9.981 GB and 3.960 GB (census) | on HOME, not reachable until migrated; B10 -> `buu_lspine_3600/derived/` (restricted in the plan; readable by approved students after job 40599886) | `ls -ld $H/buu_fov96_ctx` |
| `/wsu/home/go/go24/go2432/extra_fov96_ctx` | HOME | extra crop bank | 12.282 GB (census) | on HOME, not reachable until migrated; B11 (restricted in the plan; readable by approved students after job 40599867) | `ls -ld $H/extra_fov96_ctx` |
| `/wsu/home/go/go24/go2432/vindr_fov96_ctx`, `vindrps_fov96_ctx`, `vindr_pseudo`, `vindr_pseudo_drr`, `vindr_det_drr`, `vindr_lat_ids.txt`, `vindr_views.csv`, `vindr_variant_audit.json` | HOME | the VinDr-SpineXR banks (744-film crop bank; `vindrps` carries a 77.8 % validation leak and never re-enters a bank) and tables; DUA | not sized | on HOME, not reachable until migrated; B10 -> `vindr_spinexr/{derived, meta}` (restricted in the plan; readable by approved students after job 40599886); not started | `ls -ld $H/vindr_fov96_ctx` |
| `/wsu/home/go/go24/go2432/nhanes_pseudo`, `nhanesps_fov96_ctx`, `nhanes_ctx`, `nhanes_split_ctx`, `nhanes_drr`, `nhanes_pvariant_strata.json` | HOME | 16,530 pseudo-labelled NHANES films (fed only the deleted v5) and their banks | `nhanes_pseudo` 74 GB (du 2026-09-19); rest not sized | on HOME, not reachable until migrated; B10 -> `nhanes2_cdc_films/derived`, `nhanes2_zenodo_landmarks/derived`; not started | `ls -ld $H/nhanes_pseudo` |
| `/wsu/home/go/go24/go2432/mendeley_fov96_ctx`, `mendeley_drr`, `lat236ps_fov96_ctx`, `lateral236_pseudo`, `aasce_fov96_ctx`, `aasce_drr`, `spinalai_drr` | HOME | the Mendeley (excluded from training by directive D6), lateral-236, AASCE and Spinal-AI2024 banks | `spinalai_drr` 4.4 GB, `mendeley_drr` 1.3 GB (B10.tsv); rest not sized | on HOME, not reachable until migrated; B10; not started | `ls -ld $H/mendeley_fov96_ctx` |
| `/wsu/home/go/go24/go2432/m_fov96_ctx`, `m_mask22_scale_ctx`, `merged_ctx`, `verse_ctx`, `verse_only_ctx_plus_nh`, `sd_fov96_ctx`, `mv_bands`, `pseudo_filtered`, `yolo_levels`, `sacrum_yolo`, `quiz_pack`, `reader_study`, `review_pack`, `review_pack_v2`, `review_pack_smoke`, `verify_bench`, `film_style_ds` | HOME | B11 banks and the review / quiz / reader-study packs (roles per `DATA_MANIFEST.md` Appendix A) | `yolo_levels` 6.7 GB; `film_style_ds` 0.962 GB; rest not sized | on HOME, not reachable until migrated; B11; not started | `ls -ld $H/yolo_levels` |
| `/wsu/home/go/go24/go2432/scaling` | HOME | the 2026-09-17 subset banks of the deleted v2 (the fraction sweep, C2.1); the trap of RECIPES section 1.8: a rerun that finds these re-emits the leaky curve | 129.2 GB (B11.tsv) | on HOME, not reachable until migrated; B11 (candidate); not started | `ls -ld $H/scaling` |
| `/wsu/home/go/go24/go2432/split_final.json`, `patient_keys*.json`, `bank_splits.json` | HOME | the identity tables (the G3 person split is FROZEN, job 40426793) | small | on HOME, not reachable until migrated; B11 | `head -c 200 $H/split_final.json` |

## 3. HOME: result files behind the RECORD ONLY rows of `STATUS.md` (`MANIFEST_GRID.md` section 3; none re-read on 2026-10-08)

Every row is on HOME, not reachable until migrated; no migration batch is recorded for these rows in
`MANIFEST_GRID.md` except where stated.

| path | volume | what it holds (STATUS.md row) | size | migration state | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/tmp/ladder_summary.json` | HOME | the context-ladder result on `films_ann` (C1.1); **not found on 2026-10-08** (read-only `ls` at 01:25 UTC 2026-10-09; `~/tmp` itself present with 268 entries); `memory/level-id-2d-results-2026-09-13.md` and RESULTS_CATALOG C1.1 are the only record | not sized | not recorded | `ls -ld $H/tmp/ladder_summary.json` (expected to fail: the file was absent) |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json`, `recurrent_all2.json`; `bench/robust/*.json`; `bench/model_registry.md` (M96) | HOME | the recurrent-head results (job 40215812, 2026-09-13; log prints `embedded 28032 crops`) and the corruption suite (C1.2, C1.3, C1.10) | `~/bench` 35.8 GB | not recorded | `head -c 200 $H/bench/xr_fov/recurrent.json` |
| `/wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json`; `model_night/recurrent_allspine_v2.json`; `model_night/stc/`; `model_night/interior_windows/`; `model_night/panel_stats/`; `model_night/scaling/SCALING_CURVE.json`; `model_night/ensemble/ensemble.json` (listing truncated; OPEN_QUESTIONS B6); `model_night/heads_mixed/` (not reached by the listing); `model_night/figures_feasibility/` | HOME | the model-night arms on allspine v2 (C1.4, C1.5, C1.7, C1.14, C1.11, C2.1, C1.17) | not sized | not recorded | `ls -ld $H/model_night` |
| `/wsu/home/go/go24/go2432/selective/SELECTIVE.md` | HOME | selective prediction on the leaked v2 bank (job 40291753; C1.8) | not sized | not recorded | `head -c 200 $H/selective/SELECTIVE.md` |
| `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`, `LEARNING_CURVE.md`, `sources/buu3600_lstv_labels.csv` | HOME | the 2-D LSTV / TLTV flags (refuted) and their learning curve (date and job not recorded; C1.12, C1.13) | not sized | not recorded | `head -c 200 $H/lstv_flag/LSTV_FLAG_RESULTS.md` |
| `/wsu/home/go/go24/go2432/track5/track5_recurrent_frozen.py` | HOME | the frozen Track 5 script, sha256 `fc6e4ddc…` = `tools/recurrent_order.py` at the time (`results/track5_results/frozen_sha.txt`) | not sized | not recorded | `head -c 200 $H/track5/track5_recurrent_frozen.py` |
| `/wsu/home/go/go24/go2432/scaling_curves/` | HOME | `eval_scaling_curves.py` outputs (devices / cases / fewshot; C2.3) | not sized | not recorded | `ls -ld $H/scaling_curves` |
| `/wsu/home/go/go24/go2432/FluoroCap/detect_v5z_*_best.pt`, `detect_v6f_best.pt`; `/wsu/home/go/go24/go2432/level_id_service/weights/detector.pt` | HOME | HOME copies of the later detector weights (`DATA_MANIFEST.md` card `spine_detector_corpus`); the weights belong to folder 01 and are private | not sized | FluoroCap itself was B09 copying on 2026-10-08; the rest not recorded | `ls -ld $H/FluoroCap` |

## 4. HOME: the model registry entries of this line (`MANIFEST_GRID.md` section 4)

| path | volume | what it holds | size | migration state | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/model_registry/<sha16>/`, with `registry.jsonl` and `aliases/` | HOME | the content-addressed weights store: `registry.jsonl` (106 lines; a sync loop re-registered `orientation_net_v2` sixteen times, so 106 lines is not 106 models) and `aliases/` (79 symlinks); the weights are private (`CLAUDE.md` rule 8) | per-alias bytes below; the store itself not sized in this manifest | on HOME, not reachable until migrated; migration state not recorded in `MANIFEST_GRID.md` | `ls -ld $H/model_registry/aliases` |
| `/wsu/home/go/go24/go2432/mlflow/mlflow.db` | HOME | the MLflow database | 1,028,096 B | on HOME, not reachable until migrated; migration state not recorded in `MANIFEST_GRID.md` | `ls -ld $H/mlflow/mlflow.db` |

The registry entries of this line, as `MANIFEST_GRID.md` section 4 lists them (store paths are under
`$H/model_registry/`):

| alias | store | bytes | role |
|---|---|---|---|
| `films_all2_rung1_aug2` | `d081b4ab18b331a7/model_rung_1_aug2.pt` (registered 2026-09-15) | 44,824,746 | superseded film encoder |
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
`head_allspine_v9_mixed_kmax4_seed0` (`model_night/heads_mixed/`, not reached by the listing). The
mirror (the private Hugging Face repository `gregoryschwingmdphd/level-id-weights`) was not checked;
no network was used on 2026-10-08.

## 5. Ceph: what is already there (`MANIFEST_GRID.md` section 5)

Ceph rows are readable by approved students (see "Access", below); the rows flagged restricted were
owner-only until 2026-10-12 and open with visibility jobs 40599886 and 40599867.

| path | volume | what it holds | size | migration state | check line |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/inventory/films/` | Ceph | `FILM_CORPUS_INVENTORY.md` 2,839 B, `nhanes_film_manifest.csv` 2,109,890 B, `vindr_film_manifest.csv` 1,388,674 B, `film_corpus_inventory.json` 3,362 B, `box_convention/` (9 entries); all 2026-09-23 (job 40416535, `DATASET_USAGE.md` section 8) | about 3.5 MB | Ceph-native | `ls -ld $C/data/inventory/films` |
| `/rs/rs_grp_oschome/go2432/data/inventory/vindr_age_sex.csv` | Ceph | the VinDr age and sex table, DUA-derived: never redistribute | 830,061 B (2026-09-24) | Ceph-native | `head -c 200 $C/data/inventory/vindr_age_sex.csv` |
| `/rs/rs_grp_oschome/go2432/data/thoracic_xr` | Ceph | the AASCE open mirror (609 labelled films) | 0.859 GB (census); 962 files byte-identical to the HOME copy (dedup A15) | Ceph-native | `ls -ld $C/data/thoracic_xr` |
| `/rs/rs_grp_oschome/go2432/data/vindr` | Ceph | a three-file placeholder, **not** the DUA data (that is still `spine-detector/data/raw/vindr`, B04) | 0.002 GB | Ceph-native | `ls -ld $C/data/vindr` |
| `/rs/rs_grp_oschome/go2432/data/mendeley_5jdfdgp762/raw/spondy_landmark` | Ceph | the second download of Mendeley 5jdfdgp762 (`~/data/spondy_landmark` cut over) | 1,416 files 89,020,337 B | B14 **VERIFIED** (candidate; duplicate of `mendeley_716` pending a sha check, dedup A14) | `ls -ld $C/data/mendeley_5jdfdgp762/raw/spondy_landmark` |
| `/rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived/dis_renders` | Ceph | five PNGs named by BUU films (owner-only until 2026-10-12; readable by approved students after job 40599886) | 5 files 10,869,856 B | B14 item 002 **VERIFIED**; restricted, candidate | `ls -ld $C/data/xrspinopelvic1k/derived/dis_renders` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/obl2_fov96_ctx` | Ceph | the oblique crop bank | 9 files 13,327,845,295 B | B06 **VERIFIED**, cut over | `ls -ld $C/data/versefusion/derived/obl2_fov96_ctx` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/verse_only_ctx` | Ceph | the VerSe-only crop bank | 42 files 743,721,823 B | B06 **VERIFIED**, cut over | `ls -ld $C/data/versefusion/derived/verse_only_ctx` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/film_ncurve/` | Ceph | the film N-curve chain outputs: `cells.json`, `manifest.txt`, `render_bank/`, `test_ctx/`, `pool_*/`, `base_cache/`, `cells/<cell>/` with DONE markers, `film_ncurve.json`, `FILM_NCURVE.md` (2026-09-24; jobs 40437808 -> 40437809 -> 40437810 array 0-47 -> 40437811); `ablation/{imagenet, filmonly}/` (jobs 40451157, 40451158; collects 40451159, 40451160) | inside `or_ready` (868 GB) | Ceph-native (folder 01's result root); not re-verified 2026-10-08; the copies the paper reads are `SchwingNet/results/coverage/film_ncurve/` in `spinesurg-ct-nnunet` 097933a | `ls -ld $C/data/or_ready/film_ncurve` |

**Reconciling the two dates.** The tables above record the grid as read on 2026-10-08 22:20 UTC, when
the B04 targets (`vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `spine_detector_corpus`
and the rest) were absent on Ceph. Greg's access facts of 2026-10-11 (issue #13, below) name those
folders under `/rs/rs_grp_oschome/go2432/data/` as present and readable, so B04 landed in between;
no file in this folder records the per-item outcome, and the truth for each item is
`data_platform/plan/runs/B04/STATUS`, read in a job or with `cat` (`MANIFEST_GRID.md` header).

## Terms

- **VinDr-SpineXR** is held under a personal PhysioNet credentialed account (CITI training) and a
  data use agreement (`results/spine_detector_report/report.html`; `docs/handoff/DATASET_USAGE.md`
  section 2.1 row VinDr-SpineXR). It stays on the grid under its DUA (`CLAUDE.md` rule 9); no WSU
  IRB determination covers it, and the determination number is Greg's open item (OPEN_QUESTIONS A5;
  `TODO.md` step 3). The DUA-derived table `vindr_age_sex.csv` (section 5 above) is never
  redistributed.
- **BUU-LSPINE** is "No License Provided" plus an end-user licence agreement; recorded as not open;
  **never redistribute its images or crops**; terms for derived labels are not addressed in any file
  read, so they are treated as non-redistributable (`MANIFEST_LOCAL.md` section 3a, quoting
  `DATA_MANIFEST.md` card `buu_lspine_3600`). **No weight trained with BUU laterals leaves the grid
  until Greg has read the licence** (`CLAUDE.md` rule 8; `TODO.md` step 3).
- **Mendeley 5jdfdgp762** re-encodes BUU: about 500 BUU people (and 13 VinDr images) are
  redistributed among its 714 jpg, and the crop bank cut from it, `mendeley_fov96_ctx`, holds 584
  crops. It is excluded from training by directive D6 (`MANIFEST_GRID.md` section 2;
  `docs/handoff/DATASET_USAGE.md` section 2.1 row Mendeley 5jdfdgp762;
  `memory/data-directives-2026-09-23.md`: "Mendeley-716 stays out: redistribution of BUU-LSPINE,
  duplicate subjects — that is the written justification").
- **FluoroCap** is out of training by directive D1: it is reproductions of published figures
  (72.8 % of panels with zero pixel residual), a test set at most
  (`docs/handoff/DATASET_USAGE.md` section 2.1 row FluoroCap; `memory/data-directives-2026-09-23.md`;
  `CLAUDE.md` rule 9).
- **The Cerner `.ica` file in the XRSpinoPelvic1K checkout**
  (`Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica`, 2,017 B, tracked at 4f22935 and present in the
  grid clone) **is never copied** anywhere; it is to be purged from history (`MANIFEST_GRID.md`
  section 7; `TODO.md` step 1).
- The terms of the other corpora the manifest lists (NHANES II public domain, AASCE request form,
  and the rest) are in `docs/handoff/DATASET_USAGE.md` section 2.1, one row per source.

## Access (Greg's facts of 2026-10-11, issue #13)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** — a
  named ACL entry on the volume root, other-read bits on folders and files — including
  `vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and
  `spine_detector_corpus`, because every approved student holds the PhysioNet credential and the
  VinDr and BUU agreements.
- **On 2026-10-12 the VinDr and BUU items inside those folders opened too.** Until then the plan's
  `restricted` flag still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`,
  `buu_v1`, BUU-LSPINE 2000, the VinDr and BUU banks of B10 and B11, `dis_renders`); the script was
  fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs 40599886 (the B04, B05, B10 and B14
  folders) and 40599867 (after B13's finalize, every chain folder including `multisource_banks`)
  open them (issue #65).
- **Two paths stay closed (owner-only):**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, private
  build material and not a dataset, and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, until Greg reads its
  Zenodo upload scripts for a token (issue #65;
  `../10_data_platform_grid/code/data_platform/plan/publish_visibility.sh`, from spinesurg-ct-nnunet
  d9b388d).
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students; items still
  there are moved to the Ceph volume by the data-platform plan, whose batch-by-batch state is
  `../10_data_platform_grid/MANIFEST_GRID.md` section 2. Every HOME row above is marked 'on HOME, not
  reachable until migrated'.
- Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

## Through Beethoven

The way in is Beethoven, the lab's Chrome extension: install and use it per
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (the same pages are at
https://openspineconsortium.com/beethoven/). A reader needs: a WSU AccessID with a grid account, the
Google Authenticator grid code, Claude Pro or Max, and Chrome on the invited Google account.
Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

The two access facts, again, because everything above depends on them:

- every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL
  entry on the volume root; other-read bits on folders and files), and since 2026-10-12 the VinDr
  and BUU items inside them; two paths stay closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (private
  build material, not a dataset) and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its
  Zenodo upload scripts for a token);
- nothing on `/wsu/home/go/go24/go2432` is readable by students until the data-platform plan has
  moved it to Ceph.

Run the check lines above from the Beethoven worker. Every computation this folder sends to the grid
is an `sbatch -D <dir>` job on a compute node, chained with `afterany`, with job ids and the ETA
written to `TODO.md`'s checkpoint line — never a command on the login node (`CLAUDE.md` rule 7;
`TODO.md` header).

## First experiment: the corner-detector evaluation on the 301 held-out BUU films

The first measurement `STATUS.md` section 1b and `TODO.md` step 5 name: the XRSpinoPelvic1K
corner-detector evaluation on the 301 test films of the frozen patient-grouped, sex x age-band
stratified 1398 / 301 / 301 split, `buu_splits.json` (53,434 B; never regenerate it silently,
`MANIFEST_CODE.md` section 2).

- **Where the data is.** `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data` (section 1 above) — on
  HOME, so today only Greg can run it. Batch B05 (not started on 2026-10-08; its state since is
  `../10_data_platform_grid/MANIFEST_GRID.md` section 2) moves `BUU-LSPINE` and
  `dataset2024.zip` to `$RS/data/buu_lspine_2000` and `xrsp1k` to
  `$RS/data/xrspinopelvic1k/derived`; after the cut-over the XRSpinoPelvic1K `DATA_ROOT` is
  repointed (`TODO.md` step 18).
- **What runs.** The one metric implementation every number in
  `docs/xrspinopelvic1k/docs/RESULTS.md` shares: `xrsp/evalmetrics.py` of XRSpinoPelvic1K at commit
  4f22935 (`MANIFEST_CODE.md` section 2). The recorded entry points that rest on it are
  `scripts/evaluate_yolo.py` and `make eval-buu` (HPC.md, per `MANIFEST_CODE.md` section 2); which
  entry produced each RESULTS.md table is not recorded in this folder. Run it as an
  `sbatch -D <dir>` job from the checkout, never on the login node; write the job id and the ETA to
  `TODO.md`'s checkpoint line.
- **Expected numbers** (`STATUS.md` section 1b, from `docs/xrspinopelvic1k/docs/RESULTS.md`
  sections 1.2 and 2): corner localisation, YOLOv8l-Pose at 1024 px, **92.4 % of corners within
  0.55 % of the image diagonal** (Bansal's "5 px" on 640 px, converted), **median 0.203 % of the
  diagonal** (about 6.4 px on a median 3,167 px diagonal); sacral slope from predicted corners
  (v8l_640) **ICC(2,1) 0.952**, MAE 2.01 degrees.
- **The mark these numbers carry** (`STATUS.md` section 1b): repository-internal, held out by
  patient within BUU, through the repository's own evaluator, **not** through `tools/eval_gate.py`;
  the BUU levels are assigned by position, so "level" here measures position, not identity. They are
  to be regenerated on the v11 rebuild (`TODO.md` step 5), and `TODO.md` step 5 pre-states the gate:
  corner localisation at or above 92.4 % within 0.55 % of the diagonal on the 301 test films after
  the rebuild, SS ICC(2,1) at or above 0.95.
- **What must not leave.** The films and crops are BUU-LSPINE (Terms, above): never redistributed,
  and no weight trained on them leaves the grid until Greg has read the licence (`TODO.md` step 3).
