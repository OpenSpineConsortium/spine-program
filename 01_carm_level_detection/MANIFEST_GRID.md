# MANIFEST_GRID: every grid path this project uses or produced

Grid: `go2432@grid.wayne.edu`. HOME = `/wsu/home/go/go24/go2432`. Ceph = `/rs/rs_grp_oschome/go2432` (20 TB, group
`oschome`; `df-ceph oschome` for usage). Everything below is written in full once per table and abbreviated HOME / CEPH
afterwards. "Verified" means read with `ls`, `head -c` or `wc -l` through `wsl -e bash -lc 'ssh grid ...'` on 2026-10-08
(the pass is recorded in `../10_data_platform_grid/`, PLAN.md section 2 rule 8); nothing was written on the grid. Sizes
are those a file or the pass recorded; "not recorded" otherwise. Migration states come from
`spinesurg-ct-nnunet:data_platform/LAYOUT.md`, `MIGRATION_PLAN.md`, `DATA_MANIFEST.md` and
`docs/handoff/OPEN_QUESTIONS.md` B30; the state of each batch is `../10_data_platform_grid/MANIFEST_GRID.md` section 2,
and the per-batch truth is `plan/runs/<B>/STATUS` on the grid (`docs/handoff/README.md` section 3).

Rules that apply to every path here: nothing runs on the login node; read a bank only inside a job; `go2432/` below the
Ceph gate stays closed to students, and every bank holding VinDr or BUU pixels is owner-only
(`docs/handoff/INFRASTRUCTURE.md` sections 2.2, 4). The case134 headers under `CEPH/data/carmlspine` carry a real
PatientID: never print a header field.

## 1. The reported stack: weights (HOME)

| path | holds | bytes, date | registered | verified | migration |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` | naming detector `detector_v5z_final` (YOLO11m-pose, four corners, imgsz 1024, conf 0.35); the same file as `HOME/FluoroCap/detect_v5z_final_best.pt` | 42,233,939 B, 2026-09-14 | yes, alias `detector_v5z_final` | `ls` 2026-10-08 | registry stays on HOME; whether `~/model_registry` survived the migration is `OPEN_QUESTIONS.md` B31 |
| `HOME/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt` | sacrum / vertebra detector (YOLO11m, classes vertebra / sacrum; trained on COBRA Elekta 110 + 8 cases and DeepFluoro 238 + 24 frames, 3,094 frames; C-ArmLSpine never seen) | 40,601,637 B, 2026-09-22 | **no sha256 in the registry** (`docs/MODEL_CARD.md` 1.3): S0 | `ls` 2026-10-08 | `~/spine-detector/data/*` is batch B04 (copying); whether `runs/` is in a batch is not recorded |
| `HOME/spine-detector/runs/realxray/rx_pooled_1024/weights/best.pt` | the pooled twin of the sacrum detector | not recorded | not recorded | listed (carm r94) | as above |
| `HOME/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt` | pooled all-device detector `dc_P_pooled`; scores in `results/schwingnet/dc_P_pooled_scores.json`; `manuscripts/schwingnet/README.md` still records it as unfinished | 40,601,765 B, 2026-09-23 | S0 | `ls` 2026-10-08 | as above |
| `HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` | level encoder `allspine_v9` rung 1 (ResNet-18, two-channel stem, 27 classes, 2 x 320 x 320 crop, target 96 px) | 44,824,746 B, 2026-09-23 | yes, alias `allspine_v9_fov96_ctx_rung_1_aug2`, sha256 prefix 188f9fcbfa3c6de1 | `ls` 2026-10-08 | HOME; not in a recorded batch |
| `HOME/allspine_v9_fov96_ctx/rung_1.npz`, `meta.json` | the v9 level bank the encoder, the film N-curve and the fold banks read; holds BUU pixels, owner-only | 5,449,315,625 B; 73,837 B | n/a | listed (grid r139) | HOME |
| `HOME/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (+ `.arch.json`) | the recurrent head (Linear 512 to 256 + GELU, two-layer BiGRU(256), Linear 512 to 27; runs of 2 to 9 bodies; no alphabet loss) | 8,473,727 B, 2026-09-23 | not stated | **folder not reached by the 2026-10-08 listing: not verified** | HOME |
| `HOME/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt` | the five case-grouped fold encoders behind Table 3 (v9init); the banks beside them hold 2,632 VinDr and 2,100 FluoroCap crops (`DATASET_USAGE.md` 3.2) | 3.37 to 3.41 GB per folder | aliases exist (`carm_cvmix0_fov96_ctx_rung_1_ft_cv0_v9init_aug2`); no sha256 (S0) | cv0 listed 2026-10-08 | **B10**: `~/carm_*` to `CEPH/data/carmlspine/derived/` (`LAYOUT.md` L306-324); not started on 2026-10-08 |
| `HOME/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_aug2.pt` (un-suffixed) | v2-initialised fold models; the evaluation gate refuses them (bank deleted). Do not use | not recorded | refused | listed | B10 |
| `HOME/model_night/heads_carm/` (36 files) | fold heads `head_cv{0..4}(_v9init).pt`, `head_cvday{0..2}(_v9init).pt`, `head_mix.pt`, `head_realonly.pt`, `.arch.json`, `mixed_cv*.json` | not recorded | aliases for the v9init heads; no sha256 (S0) | listed (grid r176) | HOME |
| `HOME/carm_cvdaymix{0..2}_fov96_ctx`, `carm_cvdaymix0_v9_fov96_ctx` | day-grouped fold banks and models | not recorded | as above | listed (grid r170) | B10 |
| `HOME/carm_mix_fov96_ctx`, `carm_fov96_ctx`, `carm_cv{0..4}_{drr,fov96_ctx}`, `carm_cvday{0..2}_{drr,fov96_ctx}`, `carm_drr` | the mixed and per-fold C-ArmLSpine banks | not recorded | n/a | listed (grid r171) | B10 |
| `HOME/carm_base_cache`, `carm_base_cache_v9` | regenerable caches | not recorded | n/a | listed (grid r172) | B10 or delete; Greg decides (OQ A26) |
| `HOME/allspine_v7_fov96_ctx` | the v7 bank: base of the fold banks and of 57 holdout references; leaked (NHANES twice) | not recorded | n/a | listed (grid r141) | HOME |
| `HOME/model_registry/` | content-addressed store `<sha>/`, `registry.jsonl` (106 lines, `wc -l` 2026-10-08), `aliases/` (79), `mlflow_runs.jsonl`; mirror is the private HF repo `gregoryschwingmdphd/level-id-weights` | not recorded | n/a | `wc -l` 2026-10-08 | OQ B31 **Owner: project 10** (the store and the ledger `registry.jsonl`; its `MANIFEST_GRID.md` section 4). This project appends registration rows (S0) and never edits or repairs the ledger (10's TODO step 5 does). Decided in the final pass of 2026-10-08. |
| `HOME/mlflow/mlflow.db`, `artifacts/` | the MLflow ledger | 1,028,096 B | n/a | listed (grid r174) | OQ B31 |
| `HOME/level_id_service/` | the older service checkpoint set (`detect_v5z_epoch25`, M19) the container serves | not recorded | `detector_v5z_epoch25` alias | listed (carm r91 context) | HOME |

## 2. Real-frame data (Ceph unless stated)

| path | holds | size | verified | migration |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/carmlspine` | C-ArmLSpine, the real intraoperative test set of paper 1 (148 scored cases, FIRST Surgio-B51; AP + LAT + CBCT); case134 headers carry a real PatientID | 86.834 GB | `ls` 2026-10-08 | on Ceph (raw); derived banks are B10 |
| `CEPH/data/realxray/` | 23 real-frame banks with projected labels: `carmlspine` (summary.json: 299 frames, 149 cases, train 106 / val 15 / test 28; boxes per level L1 267 to sacrum 295, T12 63, T11 3), `carmlspine_sweep` (the 301-frame case134 CBCT spin, detection-only), `carmlspine_crops`, `carmlspine_cv*`, `carmlspine_cvday*`, `carmlspine_cvfill`, `carmlspine_multi`, `carmlspine_pre_repair_2026-09-23*`, `cobra_elekta` (+ `_v2`, `_v3`, `_ap45`, `_g3test`, `_smoke`), `deepfluoro`, `geneva_hip`, `pelvis_landmarks`, `bournemouth_qf/raw` (`Cervical_Database.mat` 24,380,812 B, 2026-09-26; no `meta/`, `images/`), `view_census.json`; no `cobra_varian` | 3.408 GB | `ls` 2026-10-08 | on Ceph |
| `CEPH/data/realxray_work/` | export work dirs `geneva_hip`, `deepfluoro` | not recorded | listed (grid r33) | on Ceph |
| `CEPH/data/cobra2026/` | COBRA2026, 692 of 692 cases, 375,618 projections, Elekta + Varian (`COBRA_COMPLETE.md`); 145 Elekta cases in banks, 225 Varian never exported (`DATASET_USAGE.md` 2.3 gives 771 GB) | 808.615 GB | `ls` 2026-10-08 | on Ceph |
| `CEPH/data/deepfluoro_h5/raw/deepfluoro` | DeepFluoro H5 release (6 cadaver specimens, 366 frames) + `ann/`, `img/` | 5,272,150,583 B | B00 VERIFIED | B00 cut over |
| `CEPH/data/deepfluoro_vendor` | vendor DICOM deposit, 2,659 frames + 19 CT; 2,293 frames unused with no written criterion (OQ E5) | 110.987 GB | listed (grid r30) | on Ceph |
| `CEPH/data/geneva_hip_src` | the unseen-device test (BV Pulsera phantom, 116 frames) | not recorded | listed (grid r35) | on Ceph |
| `CEPH/data/ljubljana` | 2D-3D-GS gold standard, 18 frames, PIXIUM 4600 (user guide in `docs/external_reports/`) | not recorded | listed (grid r36) | on Ceph |
| `CEPH/data/spinesac` | sawbone C-arm frames, no bone truth, no licence | not recorded | listed (grid r37) | on Ceph |
| `CEPH/data/external/fluoro_video/` | public fluoroscopy clips cut by `code/fluoro_video/`: `clips/` (REPORT.md, manifest.json, clips.csv, about 20 clip folders), `youtube/`, `pmc/`, `commons/`, `vimeo/`, `github/`, `ajr/`, `dysphagiabank_unm/`, `work/`; never scored | 262.801 GB | `ls` 2026-10-08 | on Ceph |
| `CEPH/data/outline_conv` | C-ArmLSpine outline conversions | not recorded | listed (grid r77) | on Ceph |
| `CEPH/data/devcorpus/{lists,poses,render,styled}` | the device corpus (project 08) | not recorded | listed | on Ceph |
| `HOME/FluoroCap/` | the FluoroCap test set (dropped from training; test only); also holds `detect_v5z_final_best.pt` | not recorded | listed | **B09** copying |
| `HOME/spine-detector/` | the live detector tree: `.git` (2026-09-12), `data/` (2026-09-20), `runs/` (2026-09-24), `dist`, `onnx_out`, `weights`, `logs`, `yolo11m-pose.pt`; 382 GB per the 2026-09-19 `du` | 382 GB (2026-09-19) | listed (inv3 r91) | `data/*` is **B04** copying |
| `HOME/scaling/` | subset banks `s000_r100 ... s100_r100` cut from the deleted v2 bank | 129.2 GB | listed (grid r181) | not recorded; a deletion candidate (OQ A26) |
| `HOME/scaling_curves/` | `cross/`, `fig_scaling_curves.{pdf,png}`, `scaling_devices.json`, `scaling_fewshot.json` | not recorded | listed (grid r182) | HOME |

## 3. Results and records

| path | holds | size | verified | migration |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/or_ready/` | paper 1's result root: `devices/` (8 cards incl. `surgio_b51_dr/raw/display`, `varian_halcyon`), `lodo/` (`rescore_outline.md` is the 90.6 / 83.9 % source), `audit/`, `eval_gate/`, `indomain/`, `lcurve/`, `arc/`, `coverage/`, `crossdev/`, `devlodo/`, `devpool/`, `fig3_detection*`, `fig4_pairs*`, `film_ncurve/`, `learning*`, `corpus_manifold/`, `auto_reference/` | 867.951 GB | `ls` 2026-10-08 | **B13** results move (627 GB) is Greg's decision (OQ A26) |
| `CEPH/data/or_ready/cine/` | **ABSENT** (`ls` 2026-10-08): no cine inference, tracking or latency run has ever happened | — | absent | — |
| `CEPH/data/fig6/` (with `HOLD_README.txt`, `unblinding/`) | paper 2's blinded gate (project 02); never release before a person writes `unblinding/RELEASE_v2.json` | not recorded | listed (grid r43) | on Ceph |
| `CEPH/data/figure1/` | Figure 1 material | not recorded | listed (grid r44) | on Ceph |
| `CEPH/model_night/` | DeepFluoro anchor rounds of 2026-09-21 | not recorded | listed (grid r46) | on Ceph |
| `HOME/model_night/` | the HOME results root: `PIPELINE_STATE.md` (the authority on stage state), `RESULTS.md`, `CHAIN_LEDGER.tsv`, `XRAY_DATASET_USAGE.md`, `anomaly_manifest/`, `heads_carm/`, `heads_mixed/` (not reached), `competitors/`, `benchmark_cina/`, `count_*/`, `detector_*` json, `ensemble/ensemble.json` (OQ B6), `sweep_v3/` (job 40384843; `cns/unseen_v9.txt`), `guided/{calib,far,main,near,rot,sloppy}` (job 40376577; contents not opened; corpus result NOT RECORDED), `fiducial/{ctsp_clamp,ctsp_skip_open,ctsp_skip_open_ext,ts_skip_open,ts_skip_open_ext}` (the fiducial walks the QI draft quotes), `logs/` | not recorded | listed (grid r175, carm r106) | HOME |
| `HOME/bench/latency.json` | 2026-09-13: V100 (host voh4) detector at 1024 px 22.9 ms median, level model 2.3 ms, head over 9 bodies 0.68 ms; CPU 8 threads detector 331 ms, level model 18.3 ms; **older models** (`films_ann` level model, `detect_v3`) | not recorded | `head -c` 2026-10-08 | HOME The directory `/wsu/home/go/go24/go2432/bench` is shared with project 03, which lists the benchmark harness under it (35.845 GB); this folder lists only the two latency files. |
| `HOME/bench/runtime_cost_workstation.json`, `fig_runtime_workstation.{png,pdf}` | the contended Windows workstation run of 2026-09-22 (code_sha edf0801): crop 211 ms, encoder 3,350 ms, head 124 ms, link 422,633 ms per pair reduced to 575 ms; detector not measured | not recorded | `head -c` 2026-10-08 | HOME |
| `HOME/bench/runtime_cost.json` | **ABSENT**: the uncontended GPU job of `docs/MODEL_CARD.md` 6.6 was never run; no `slurm/runtime_cost.sh` exists in the repository | — | absent (listing 2026-10-08) | S1 writes it |
| `HOME/split_final.json`, `HOME/patient_keys*.json` | the identity tables (one split over people) | 8,065,646 B (split_final) | listed | **B11** not started **Owner: project 10** (its `MANIFEST_GRID.md` section 6, 'owned here, read by every model folder'); read here, never redrawn. |
| `HOME/corpus_final/` | **ABSENT**: gate G4 never built (`docs/FLAGSHIP_PLAN.md`) | — | absent | — |
| `HOME/spinesurg-ct-nnunet/` | the private repository checkout, `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405; **cannot fetch the private remote** (why not recorded); ship by `git archive | ssh tar` and read `SHIPPED_COMMITS.txt` (`docs/handoff/RECIPES.md` section 0) | not recorded | listed (grid r113) | HOME |
| `HOME/COBRA_dataset_paper.pdf`, `HOME/bpex_ad2baa.pdf` | the COBRA dataset paper and a second PDF | 7,084,212 B; 1,916,673 B | listed (grid r212) | HOME |
| `HOME/remote_wait.sh` | the submit-and-wait helper | not recorded | OQ B31 asks whether it still sits there | HOME |

## 4. Jobs of record

| job | what | file |
|---|---|---|
| 40483839 / 40483840 | the review and camera-ready builds of paper 1, 2026-09-27, commit 05e05dc | `manuscripts/schwingnet/packet/` |
| 40415667 to 40415670 | v9 keys, bank, train, a5 | `docs/handoff/DATASET_USAGE.md` section 1 |
| 40448862, 40448892 | the miss diagnostic and the denominator repair | `results/schwingnet/indomain/` |
| 40384843 | sweep_v3 (the only sweep on the right field size) | `HOME/model_night/sweep_v3/` |
| 40376577 | the guided-loop corpus arms; result NOT RECORDED | `docs/GUIDED_ACQUISITION.md` |
| 40438005 (held) and 40431765 / 66 | the paper 2 f6eval jobs at the 2026-09-27 cancellation (OQ B11) | `../10_data_platform_grid/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` |
| queue on 2026-10-08 | 7 jobs of go2432 (`squeue -u go2432 -h | wc -l`) | the grid pass |

## 5. What this project will write on the grid (not yet there)

`HOME/model_registry/registry.jsonl` lines with sha256 for the sacrum detector, the five v9init fold encoders and heads
and `dc_P_pooled` (S0); `HOME/bench/runtime_cost.json` and a `runtime_cost.sh` job file (S1); `CEPH/data/or_ready/cine/`
with the parity run of `cine_latency.py` on the case134 spin (S1, S2); device census files in the format of
`spinesurg-ct-nnunet:docs/devices/census/*_headers.md` for the hospital's C-arm (S3). Each goes under Ceph when large,
with its job id and timestamp written into this project's `results/JOBS.txt` as the recipes require.
