# DATA — reaching this project's grid data through Beethoven, and the first experiment

Written 2026-10-11 for issue #11. The paths below are `MANIFEST_GRID.md` sections 1 to 3, spelled as the manifest spells
them (HOME and CEPH kept; its source is the one read-only grid pass of 2026-10-08, recorded in
`../10_data_platform_grid/`, PLAN.md section 2 rule 8; every size, date and count below comes from that manifest). The
access facts are Greg's, dated 2026-10-11, given in issue #11; where they and an older recorded statement disagree, both
are shown with their dates. What no file records is written "not recorded".

Reader: this folder is Greg-only (`CLAUDE.md`: SchwingNet and level-identification content; `../_plan/PLAN.md` section 3,
rank 1). A student claims work here only after Greg confirms a hand-out (issue #11).

Conventions. `HOME` = `/wsu/home/go/go24/go2432` (Greg's home directory, the Panasas volume);
`CEPH` = `/rs/rs_grp_oschome/go2432` (the Ceph volume, 20 TB, group `oschome`; `df-ceph oschome` for usage)
(`MANIFEST_GRID.md` header). In a student's shell `~` expands to the student's own HOME, so every check line writes the
full path. Every check line is read-only (`ls -ld` for a directory or a file, `head -c 200` for a text file) and runs
**from the Beethoven worker**, which is a batch job on a compute node
(`../11_students_grid_access/docs/beethoven/extension_README.md`) — never python, and never anything on the login node
warrior, which kills python, node, pip, md5sum, rsync, conda and others by name (`CLAUDE.md` "The grid";
`docs/handoff/RECIPES.md` section 0). A check marked **(Greg only)** names a HOME path, which the 2026-10-11 access facts
leave unreadable to students: the expected result of a student's check there is a refusal, and the item is marked **on
HOME, not reachable until migrated**. One rule binds every check under `CEPH/data/carmlspine`: the case134 headers carry
a real PatientID (`MANIFEST_GRID.md` header; `CLAUDE.md` traps) — **never print a header field**; the check there is
`ls -ld` only, never `head -c` on a DICOM.

## 1. The reported stack: weights (HOME) — `MANIFEST_GRID.md` section 1

Every path in this section is on HOME (Panasas), so under the 2026-10-11 access facts the whole section is unreadable to
students today: each item is **on HOME, not reachable until migrated**, with the batch (or its absence) as the manifest
records it, and every check is (Greg only).

- `/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` — HOME (Panasas). The naming
  detector `detector_v5z_final` (YOLO11m-pose, four corners, imgsz 1024, conf 0.35); the same file as
  `HOME/FluoroCap/detect_v5z_final_best.pt`; 42,233,939 B, 2026-09-14; registered, alias `detector_v5z_final`. The
  registry stays on HOME; whether `~/model_registry` survived the migration is `docs/handoff/OPEN_QUESTIONS.md` B31.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` — a
  42,233,939-byte file.
- `HOME/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt` — HOME (Panasas). The sacrum and vertebra
  detector (YOLO11m, classes vertebra / sacrum; trained on COBRA Elekta 110 + 8 cases and DeepFluoro 238 + 24 frames,
  3,094 frames; C-ArmLSpine never seen); 40,601,637 B, 2026-09-22; **no sha256 in the registry**
  (`docs/MODEL_CARD.md` 1.3) — S0 registers it. `~/spine-detector/data/*` is batch B04 (copying at the 2026-10-08 pass);
  whether `runs/` is in a batch is not recorded.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`.
- `HOME/spine-detector/runs/realxray/rx_pooled_1024/weights/best.pt` — HOME (Panasas). The pooled twin of the sacrum
  detector; size not recorded; registration not recorded. Migration as the row above.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_pooled_1024/weights/best.pt`.
- `HOME/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt` — HOME (Panasas). The pooled all-device detector
  `dc_P_pooled`; scores in `results/schwingnet/dc_P_pooled_scores.json`; `manuscripts/schwingnet/README.md` still records
  it as unfinished; 40,601,765 B, 2026-09-23; no sha256 (S0 registers it).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt`.
- `HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` — HOME (Panasas). The level encoder `allspine_v9` rung 1
  (ResNet-18, two-channel stem, 27 classes, 2 x 320 x 320 crop, target 96 px); 44,824,746 B, 2026-09-23; registered,
  alias `allspine_v9_fov96_ctx_rung_1_aug2`, sha256 prefix 188f9fcbfa3c6de1. Not in a recorded batch.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt`.
- `HOME/allspine_v9_fov96_ctx/rung_1.npz`, `meta.json` — HOME (Panasas). The v9 level bank the encoder, the film N-curve
  and the fold banks read; **holds BUU pixels, owner-only**; 5,449,315,625 B and 73,837 B.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/rung_1.npz` — the byte count above.
- `HOME/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (+ `.arch.json`) — HOME (Panasas). The recurrent
  head (Linear 512 to 256 + GELU, two-layer BiGRU(256), Linear 512 to 27; runs of 2 to 9 bodies; no alphabet loss);
  8,473,727 B, 2026-09-23; registration not stated; **the folder was not reached by the 2026-10-08 listing: not
  verified**, so the check below is also the read that settles that mark.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt`.
- `HOME/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt` — HOME (Panasas). The five case-grouped
  fold encoders behind Table 3 (v9init); the banks beside them hold 2,632 VinDr and 2,100 FluoroCap crops
  (`docs/handoff/DATASET_USAGE.md` 3.2); 3.37 to 3.41 GB per folder; aliases exist
  (`carm_cvmix0_fov96_ctx_rung_1_ft_cv0_v9init_aug2`), no sha256 (S0). Batch **B10** (`~/carm_*` to
  `CEPH/data/carmlspine/derived/`, `LAYOUT.md` L306-324), not started at the 2026-10-08 pass; B10 is among the batches
  running on 2026-10-12 (issue #11).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_v9init_aug2.pt` —
  the same line with k = 1 to 4 checks the other four. Once B10 lands, a student's check is
  `ls -ld /rs/rs_grp_oschome/go2432/data/carmlspine/derived`.
- `HOME/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_aug2.pt` (un-suffixed) — HOME (Panasas). v2-initialised
  fold models; **the evaluation gate refuses them (bank deleted). Do not use.** Size not recorded. Batch B10.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt` — a read
  check only; the file is never loaded.
- `HOME/model_night/heads_carm/` (36 files) — HOME (Panasas). The fold heads `head_cv{0..4}(_v9init).pt`,
  `head_cvday{0..2}(_v9init).pt`, `head_mix.pt`, `head_realonly.pt`, `.arch.json`, `mixed_cv*.json`; aliases for the
  v9init heads; no sha256 (S0); sizes not recorded.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/model_night/heads_carm` — a directory of 36 files.
- `HOME/carm_cvdaymix{0..2}_fov96_ctx`, `carm_cvdaymix0_v9_fov96_ctx` — HOME (Panasas). Day-grouped fold banks and
  models; sizes not recorded; aliases as above; batch B10.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/carm_cvdaymix0_fov96_ctx`.
- `HOME/carm_mix_fov96_ctx`, `carm_fov96_ctx`, `carm_cv{0..4}_{drr,fov96_ctx}`, `carm_cvday{0..2}_{drr,fov96_ctx}`,
  `carm_drr` — HOME (Panasas). The mixed and per-fold C-ArmLSpine banks; sizes not recorded; batch B10.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/carm_mix_fov96_ctx` — the same line, with its name, checks each of
  the others.
- `HOME/carm_base_cache`, `carm_base_cache_v9` — HOME (Panasas). Regenerable caches; sizes not recorded; B10 or delete;
  Greg decides (`docs/handoff/OPEN_QUESTIONS.md` A26).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/carm_base_cache /wsu/home/go/go24/go2432/carm_base_cache_v9`.
- `HOME/allspine_v7_fov96_ctx` — HOME (Panasas). The v7 bank: base of the fold banks and of 57 holdout references;
  **leaked (NHANES twice)** — never quoted (`CLAUDE.md` "Held out means held out"). Size not recorded; migration HOME.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/allspine_v7_fov96_ctx` — a read check only.
- `HOME/model_registry/` — HOME (Panasas). The content-addressed store `<sha>/`, `registry.jsonl` (106 lines by `wc -l`,
  2026-10-08), `aliases/` (79), `mlflow_runs.jsonl`; the mirror is the private Hugging Face repository
  `gregoryschwingmdphd/level-id-weights`. **Owner: project 10** (the store and the ledger); this project appends
  registration rows (S0) and never edits or repairs the ledger (10's TODO step 5 does). Whether `~/model_registry` still
  sits there is `docs/handoff/OPEN_QUESTIONS.md` B31.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/model_registry` — a directory; its presence answers B31's first
  part.
- `HOME/mlflow/mlflow.db`, `artifacts/` — HOME (Panasas). The MLflow ledger; 1,028,096 B (`mlflow.db`); OQ B31.
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/mlflow/mlflow.db`.
- `HOME/level_id_service/` — HOME (Panasas). The older service checkpoint set (`detect_v5z_epoch25`, M19) the container
  serves; size not recorded. The trap stands: the service is not the reported stack (`CLAUDE.md` traps; TODO S2).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/level_id_service`.

## 2. Real-frame data — `MANIFEST_GRID.md` section 2

Ceph unless stated. Every CEPH path below sits under `/rs/rs_grp_oschome/go2432/data/`, which the 2026-10-11 access
facts make readable by approved students; the HOME rows at the end are not reachable.

- `/rs/rs_grp_oschome/go2432/data/carmlspine` — Ceph. C-ArmLSpine, the real intraoperative test set of paper 1 (148
  scored cases, FIRST Surgio-B51; AP + LAT + CBCT); 86.834 GB; on Ceph (raw); the derived banks are batch B10.
  **Case134 headers carry a real PatientID: never print a header field.**
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/carmlspine` — a readable directory; `ls -ld` only, never `head -c` here.
- `CEPH/data/realxray/` — Ceph. 23 real-frame banks with projected labels: `carmlspine` (summary.json: 299 frames, 149
  cases, train 106 / val 15 / test 28; boxes per level L1 267 to sacrum 295, T12 63, T11 3), `carmlspine_sweep` (the
  301-frame case134 CBCT spin, detection-only), `carmlspine_crops`, `carmlspine_cv*`, `carmlspine_cvday*`,
  `carmlspine_cvfill`, `carmlspine_multi`, `carmlspine_pre_repair_2026-09-23*`, `cobra_elekta` (+ `_v2`, `_v3`, `_ap45`,
  `_g3test`, `_smoke`), `deepfluoro`, `geneva_hip`, `pelvis_landmarks`, `bournemouth_qf/raw` (`Cervical_Database.mat`
  24,380,812 B, 2026-09-26; no `meta/`, `images/`), `view_census.json`; no `cobra_varian`; 3.408 GB.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/realxray` — a readable directory.
- `CEPH/data/realxray_work/` — Ceph. Export work dirs `geneva_hip`, `deepfluoro`; size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/realxray_work`.
- `CEPH/data/cobra2026/` — Ceph. COBRA2026, 692 of 692 cases, 375,618 projections, Elekta + Varian
  (`COBRA_COMPLETE.md`); 145 Elekta cases in banks, 225 Varian never exported (`docs/handoff/DATASET_USAGE.md` 2.3 gives
  771 GB); 808.615 GB.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/cobra2026` — a readable directory.
- `CEPH/data/deepfluoro_h5/raw/deepfluoro` — Ceph. The DeepFluoro H5 release (6 cadaver specimens, 366 frames) +
  `ann/`, `img/`; 5,272,150,583 B; batch B00 cut over, VERIFIED.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro`.
- `CEPH/data/deepfluoro_vendor` — Ceph. The vendor DICOM deposit, 2,659 frames + 19 CT; 2,293 frames unused with no
  written criterion (`docs/handoff/OPEN_QUESTIONS.md` E5); 110.987 GB.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/deepfluoro_vendor`.
- `CEPH/data/geneva_hip_src` — Ceph. The unseen-device test (BV Pulsera phantom, 116 frames); size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/geneva_hip_src`.
- `CEPH/data/ljubljana` — Ceph. The 2D-3D-GS gold standard, 18 frames, PIXIUM 4600 (user guide in
  `docs/external_reports/`); size not recorded; **read-only under its ND licence** (Terms below).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ljubljana`.
- `CEPH/data/spinesac` — Ceph. Sawbone C-arm frames, no bone truth, **no licence** (Terms below); size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/spinesac`.
- `CEPH/data/external/fluoro_video/` — Ceph. Public fluoroscopy clips cut by `code/fluoro_video/`: `clips/` (REPORT.md,
  manifest.json, clips.csv, about 20 clip folders), `youtube/`, `pmc/`, `commons/`, `vimeo/`, `github/`, `ajr/`,
  `dysphagiabank_unm/`, `work/`; never scored; 262.801 GB.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/external/fluoro_video`.
- `CEPH/data/outline_conv` — Ceph. C-ArmLSpine outline conversions; size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/outline_conv`.
- `CEPH/data/devcorpus/{lists,poses,render,styled}` — Ceph. The device corpus (project 08); sizes not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/devcorpus` — a readable directory holding those four entries.
- `HOME/FluoroCap/` — HOME (Panasas). The FluoroCap test set (dropped from training; test only); also holds
  `detect_v5z_final_best.pt`; size not recorded. Batch **B09**, copying at the 2026-10-08 pass. **On HOME, not reachable
  until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/FluoroCap`.
- `HOME/spine-detector/` — HOME (Panasas). The live detector tree: `.git` (2026-09-12), `data/` (2026-09-20), `runs/`
  (2026-09-24), `dist`, `onnx_out`, `weights`, `logs`, `yolo11m-pose.pt`; 382 GB per the 2026-09-19 `du`. `data/*` is
  batch **B04**, copying at the 2026-10-08 pass; whether `runs/` is in a batch is not recorded. **On HOME, not reachable
  until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spine-detector`.
- `HOME/scaling/` — HOME (Panasas). Subset banks `s000_r100 ... s100_r100` cut from the deleted v2 bank; 129.2 GB;
  migration not recorded; a deletion candidate (`docs/handoff/OPEN_QUESTIONS.md` A26). **On HOME, not reachable until
  migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/scaling`.
- `HOME/scaling_curves/` — HOME (Panasas). `cross/`, `fig_scaling_curves.{pdf,png}`, `scaling_devices.json`,
  `scaling_fewshot.json`; size not recorded. **On HOME, not reachable until migrated** (no batch recorded in this
  folder).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/scaling_curves`.

## 3. Results and records — `MANIFEST_GRID.md` section 3

- `/rs/rs_grp_oschome/go2432/data/or_ready/` — Ceph. Paper 1's result root: `devices/` (8 cards incl.
  `surgio_b51_dr/raw/display`, `varian_halcyon`), `lodo/` (`rescore_outline.md` is the 90.6 / 83.9 % source), `audit/`,
  `eval_gate/`, `indomain/`, `lcurve/`, `arc/`, `coverage/`, `crossdev/`, `devlodo/`, `devpool/`, `fig3_detection*`,
  `fig4_pairs*`, `film_ncurve/`, `learning*`, `corpus_manifold/`, `auto_reference/`; 867.951 GB. The **B13** results
  move (627 GB) is Greg's decision (`docs/handoff/OPEN_QUESTIONS.md` A26); B13 is among the batches running on
  2026-10-12 (issue #11).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready` — a readable directory.
- `CEPH/data/or_ready/cine/` — **ABSENT** at the 2026-10-08 listing: no cine inference, tracking or latency run has ever
  happened. S1 and S2 write it.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/cine` — the expected result today is "No such file or
  directory"; a directory here means S1/S2 output has landed since.
- `CEPH/data/fig6/` (with `HOLD_README.txt`, `unblinding/`) — Ceph. Paper 2's blinded gate (project 02); **never release
  before a person writes `unblinding/RELEASE_v2.json`**; size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/fig6` — a read check only; nothing under `unblinding/` is written.
- `CEPH/data/figure1/` — Ceph. Figure 1 material; size not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/figure1`.
- `CEPH/model_night/` — Ceph. DeepFluoro anchor rounds of 2026-09-21; size not recorded. This path sits **outside**
  `CEPH/data/`, so the 2026-10-11 access facts do not speak to it: whether a student can read it is not recorded.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/model_night` — the mode shown settles its state today.
- `HOME/model_night/` — HOME (Panasas). The HOME results root: `PIPELINE_STATE.md` (the authority on stage state),
  `RESULTS.md`, `CHAIN_LEDGER.tsv`, `XRAY_DATASET_USAGE.md`, `anomaly_manifest/`, `heads_carm/`, `heads_mixed/` (not
  reached by the 2026-10-08 listing), `competitors/`, `benchmark_cina/`, `count_*/`, `detector_*` json,
  `ensemble/ensemble.json` (OQ B6), `sweep_v3/` (job 40384843; `cns/unseen_v9.txt`), `guided/{calib,far,main,near,rot,
  sloppy}` (job 40376577; contents not opened; corpus result NOT RECORDED), `fiducial/{ctsp_clamp,ctsp_skip_open,
  ctsp_skip_open_ext,ts_skip_open,ts_skip_open_ext}` (the fiducial walks the QI draft quotes), `logs/`; size not
  recorded. **On HOME, not reachable until migrated** (no batch recorded in this folder).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/model_night`.
- `HOME/bench/latency.json` — HOME (Panasas). The 2026-09-13 latency record: V100 (host voh4), detector at 1024 px
  22.9 ms median, level model 2.3 ms, head over 9 bodies 0.68 ms; CPU 8 threads detector 331 ms, level model 18.3 ms;
  **older models** (`films_ann` level model, `detect_v3`). The directory `/wsu/home/go/go24/go2432/bench` is shared with
  project 03 (its benchmark harness, 35.845 GB); this folder lists only the two latency files. **On HOME, not reachable
  until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/bench/latency.json` — JSON text.
- `HOME/bench/runtime_cost_workstation.json`, `fig_runtime_workstation.{png,pdf}` — HOME (Panasas). The contended
  Windows workstation run of 2026-09-22 (code_sha edf0801): crop 211 ms, encoder 3,350 ms, head 124 ms, link
  422,633 ms per pair reduced to 575 ms; **detector not measured**. **On HOME, not reachable until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/bench/runtime_cost_workstation.json` — JSON text.
- `HOME/bench/runtime_cost.json` — **ABSENT**: the uncontended GPU job of `docs/MODEL_CARD.md` 6.6 was never run, and no
  `slurm/runtime_cost.sh` exists in the repository. **S1 writes it** (the first experiment below).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/bench/runtime_cost.json` — the expected result today is "No such
  file or directory".
- `HOME/split_final.json`, `HOME/patient_keys*.json` — HOME (Panasas). The identity tables (one split over people);
  8,065,646 B (`split_final.json`). Batch **B11**, not started at the 2026-10-08 pass; B11 is among the batches running
  on 2026-10-12 (issue #11). **Owner: project 10** (its `MANIFEST_GRID.md` section 6, "owned here, read by every model
  folder"); read here, never redrawn. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/split_final.json` — a read check only; the tables are read in
  jobs, never printed.
- `HOME/corpus_final/` — **ABSENT**: gate G4 was never built (`docs/FLAGSHIP_PLAN.md`).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/corpus_final` — the expected result is "No such file or
  directory".
- `HOME/spinesurg-ct-nnunet/` — HOME (Panasas). The private repository checkout, `L6_Class` at
  4e3fe93862673e28613f7521d4c146c03a9dd405; **cannot fetch the private remote** (why is not recorded); ship by
  `git archive | ssh tar` and read `SHIPPED_COMMITS.txt` (`docs/handoff/RECIPES.md` section 0). The repository stays
  private (`CLAUDE.md` "Privacy of the work"). **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet`.
- `HOME/COBRA_dataset_paper.pdf`, `HOME/bpex_ad2baa.pdf` — HOME (Panasas). The COBRA dataset paper and a second PDF;
  7,084,212 B and 1,916,673 B. **On HOME, not reachable until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/COBRA_dataset_paper.pdf` — the bytes `%PDF`.
- `HOME/remote_wait.sh` — HOME (Panasas). The submit-and-wait helper; size not recorded;
  `docs/handoff/OPEN_QUESTIONS.md` B31 asks whether it still sits there. **On HOME, not reachable until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/remote_wait.sh` — shell text; its presence answers B31's
  last part.

## Terms

- **COBRA2026 is CC BY-NC 4.0**, and its validation and test cases — 175 of the 867 — are **embargoed to 2032-03-01**
  (issue #11). The folder's record: the 692-case training set is openly downloadable under CC BY-NC 4.0; the validation
  (about 60 GB) and test (about 140 GB) sets are embargoed until 1 March 2032, so only 692 of the 867 cases are usable
  now (`docs/research/research_paired_ct_projection_unverified_2026-09-21.md`; the verified companion
  `docs/research/research_paired_ct_projection_verified_2026-09-21.json` notes the embargo date was read from the paper
  and should be checked on the Zenodo record). `docs/DATASHEET.md` carries CC BY-NC 4.0 for both the Elekta and Varian
  halves.
- **CTSpine1K derivatives, DeepFluoro and COBRA are non-commercial**; the research track and any commercial track never
  cross (`CLAUDE.md` "Data"). DeepFluoro is CC BY-NC-SA 4.0 (`docs/DATASHEET.md`).
- **`CEPH/data/spinesac` has no licence** (`MANIFEST_GRID.md` section 2: "no bone truth, no licence";
  `docs/handoff/LITERATURE_STATE.md`: "none stated"). Its frames train or score nothing
  (`docs/handoff/DATASET_USAGE.md`).
- **`CEPH/data/ljubljana` is read-only under its ND licence**: CC BY-NC-ND or a signed agreement; ND forbids
  derivatives, and the user's guide forbids unauthorised distribution (`docs/DATASHEET.md`;
  `docs/handoff/RESEARCH_DIRECTIONS.md` dataset table; `docs/handoff/LITERATURE_STATE.md`, the `2D-3D-GS_UG.pdf` row).
- **No weight trained with BUU laterals leaves the grid until Greg has read the BUU licence** (`CLAUDE.md` "Data"). The
  v9 bank holds BUU pixels (`MANIFEST_GRID.md` section 1) — 3,603 BUU laterals (`TODO.md` part B, the RD row) — and S2
  ships weights off the grid to the private Hugging Face repository, so Greg decides first.
- Any other terms question is **not recorded in the folder**.

## Access — Greg's facts of 2026-10-11 (issue #11)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** (a named ACL entry on the
  volume root; other-read bits on folders and files), **including** `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- **The one closed path is**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`.
  **Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students**; items still there are being
  moved to the Ceph volume by the data-platform plan (batches B05, B10, B11, B13 running on 2026-10-12), and every such
  item above is marked "on HOME, not reachable until migrated".

These facts are newer than this folder's records and supersede the `MANIFEST_GRID.md` header rule where they disagree
(it says, as of 2026-10-08 and citing `docs/handoff/INFRASTRUCTURE.md` sections 2.2 and 4, that `go2432/` below the Ceph
gate stays closed to students and that every bank holding VinDr or BUU pixels is owner-only). The facts speak of
`/rs/rs_grp_oschome/go2432/data/`; `CEPH/model_night/` sits outside `data/`, and whether a student can read it is not
recorded. And whatever a student can read, this folder's content stays Greg-only until Greg confirms a hand-out
(`CLAUDE.md`; issue #11).

## Through Beethoven

A reader reaches the paths above from the Beethoven worker. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md`; the published pages are at
https://openspineconsortium.com/beethoven/ (issue #11).

A reader needs: a WSU AccessID with a grid account, the Google Authenticator grid code, a Claude Pro or Max
subscription, and Chrome on the invited Google account (`../11_students_grid_access/README.md`; issue #11). **Approved**
means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome` (issue #11;
`../11_students_grid_access/README.md`: "approval = `user:<AccessID>:rwx` on the root").

The two access facts, repeated: every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by an approved student
(the named ACL entry on the volume root; other-read bits on folders and files), including the VinDr and BUU folders,
because every approved student holds the PhysioNet credential and the VinDr and BUU agreements; the one closed path is
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, and nothing on
`/wsu/home/go/go24/go2432` is readable by students until the data-platform batches move it to Ceph.

## First experiment: S1, the latency of the reported stack (S0, the registration, comes first)

**S0 first** (`TODO.md` S0; issue #11): freeze and register the reference stack — `python tools/model_registry.py
register` for `rx_lodo_carmlspine_1024`, the five v9init fold encoders and heads and `dc_P_pooled`, with `--metrics`;
add `seed` and `code_sha` to `devcorpus_train.py` and the CV scorer; commit or keep as the record the five edited and
three untracked C-arm tools. Gate: every weight the paper quotes has a `HOME/model_registry/registry.jsonl` line with a
sha256; `git status` clean for the C-arm tools. S0 depends on nothing; S1 depends on S0.

**S1** (`TODO.md` S1; `docs/MODEL_CARD.md` 6.6): measure the uncontended latency of the reported stack.

1. Write the `docs/MODEL_CARD.md` section 6.6 job **as a file**, `slurm/runtime_cost.sh`, never `--wrap` (the card
   records how a multi-line `--wrap` body silently runs python with no arguments). The card's block: partition
   `gvohp,galhp`, qos `gpu`, one GPU, 16 CPUs, 64 G, `--time 08:00:00`, output under
   `/wsu/home/go/go24/go2432/model_night/logs/`, python `$HOME/mambaforge/envs/spinedet/bin/python`, submitted
   `sbatch -D ~/spinesurg-ct-nnunet` — a batch job, nothing on the login node.
2. The job runs `eval_runtime_cost.py --selftest` first (inside the job; it stops a run that would time a wrong
   architecture), then the GPU run with `--out $HOME/bench/runtime_cost.json`
   `--frames /rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images` `--bodies 6` `--threads 1 4 16`
   (`--repeats 30 --geo-repeats 5 --full-linker-repeats 3 --e2e-repeats 15` in the card's block).
3. **The gate** (issue #11; `TODO.md` S1): `HOME/bench/runtime_cost.json` exists **with the detector stage present and
   `machine_load_*` empty** (a non-empty load field means a contended machine and an upper bound, `docs/MODEL_CARD.md`
   6.5); the per-exposure time is written beside the 20 s to one minute the surgeons stated and the 4.7 s per image of
   the registration comparator (`docs/MODEL_CARD.md` section 6).
4. One wording in the card to resolve at S0: the printed 6.6 block names `--detector
   .../dc_A_held_elekta_xvi/weights/best.pt`, `--model .../model_rung_1_ft_cv0_aug2.pt` and `--head head_cv0.pt`, but
   `MANIFEST_GRID.md` section 1 marks the un-suffixed `ft_cv{k}_aug2.pt` fold models "Do not use" (the evaluation gate
   refuses them), and `TODO.md` S1's words are "the reported stack", whose weights S0 registers. Which weight files the
   S1 job must name is not recorded in the folder.
5. Also in S1 (`TODO.md`): run `cine_latency.py` on the case134 spin (`CEPH/data/realxray/carmlspine_sweep`) once its
   prototype outputs exist; `CEPH/data/or_ready/cine/` is ABSENT today (section 3 above) — no cine inference, tracking
   or latency run has ever happened.

**Reference, context only** (issue #11): `HOME/bench/latency.json`, 2026-09-13 — **older models** (`films_ann` level
model, `detect_v3`), V100 (host voh4): detector **22.9 ms median at 1024 px**, level model 2.3 ms, head over 9 bodies
0.68 ms; CPU 8 threads detector 331 ms, level model 18.3 ms (`MANIFEST_GRID.md` section 3). The QI draft's "17 ms per
frame" has no file and must not be repeated (`CLAUDE.md` traps).
