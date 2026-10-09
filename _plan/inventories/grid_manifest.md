# INVENTORY 5: what is on the grid, and what is not (2026-10-08)

Written 2026-10-08 for the seed folder `spine-program/`. It is the grid manifest by project family: every grid
path a project uses or produced, what it holds, its size where a file records one, its migration state, whether a
job verified it, and which project needs it; then the model weights and the registry; then the result roots; then
what is known to be missing from the grid. Every number carries the file it came from. What no file records is
written "not recorded".

Path spelling: `~` and `HOME` = `/wsu/home/go/go24/go2432` (Panasas); `$RS` = `/rs/rs_grp_oschome/go2432` (CephFS);
`ssn:` = `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet` (private repository, branch `L6_Class`, laptop commit
097933a); `dp:` = `ssn:data_platform/`; `scr:` = this session's scratchpad
`C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/`;
`GRIDLS` = `scr:seed/grid_ls_2026-10-08.out`, the one read-only grid pass of this inventory (3,213 lines; a condensed
copy is `scr:seed/grid_ls_condensed.txt`, the script `scr:seed/grid_remote_ls.sh`).

## 0. How this was read

Files on disk first: `dp:DATA_MANIFEST.md` §1, §3, §4, §5 (family A hazards), §6 (family B summary), §7 (`realxray_layout`,
`or_ready` cards), §8 (the three request cards), §10 (unknowns); `dp:MIGRATION_PLAN.md` §0-§10; `dp:LAYOUT.md` §1-§5;
`dp:plan/batch_items/B00-B14.tsv`, `plan/migration_batches.csv`, `plan/plan_summary.json`, `plan/layout_map.csv`;
`dp:dedup/DEDUP_PLAN.md`, `dedup/HASH_RESULTS.md`, `dedup/hash_results/`; `dp:VERIFICATION.md` §5.6, §6;
`ssn:HANDOFF/INFRASTRUCTURE.md` §1-§6, §13; `HANDOFF/RECIPES.md` §0, §3, §5-§8; `HANDOFF/DATASET_USAGE.md` §0-§8;
`HANDOFF/OPEN_QUESTIONS.md` (B rows); `HANDOFF/RESULTS_CATALOG.md` Part A1-A5, Part D; `HANDOFF/context/INDEX.md`;
`ssn:docs/MODEL_REGISTRY.md`; `ssn:docs/ruleclass/README.md`; `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`
(header and summary table); the memory notes `grid-access`, `grid-ceph-volume-oschome`, `grid-quota-and-deleted-banks`,
`grid-ct-0533-truncated`, `grid-bash-4-2-quoting`, `grid-access-list-gate`, `grid-apptainer-module-works`,
`grid-local-singularity-is-broken`, `grid-slurm-inside-apptainer`, `grid-ssh-second-factor`,
`grid-ashley-deletion-2026-09-28`, `model-registry`, `ruleclass-super-detector-run`, `data-platform-migration-2026-10`,
`level-model-bank-coverage`, `ts-bench-inside-v9-bank`, `xray-corner-detector-status`, `fluorocap-dataset`,
`fluorocap-prototype-and-lstv-arm`, `fluorocap-pipeline-resume`, `spine-data-review-and-ts-bench`, `hf-mirror-is-v10`,
`zenodo-deposit`, `lstv-oneshot-training-run`, `data-audit-99-gaps`, `carmlspine-level-experiment`,
`level-service-serving`, `no-jobs-on-login-node`; and the laptop census copies `scr:census/{census.json,
census_merged_partial.tsv, toplevel_listing.txt, _du_home.txt, _du_data.txt, ceph/census.tsv, home_after_F/census.tsv}`.

Then one read-only pass on the grid at 22:20 UTC on 2026-10-08 (GRIDLS): `pan_quota`, `df-ceph oschome`,
`squeue -u go2432`, `ls` of HOME, `$RS`, `$RS/data` and about sixty named sub-folders, `cat` of the nine
`plan/runs/<B>/STATUS` files, of `$RS/ruleclass/arms/ts/STATUS.md` and `arms/pelvis/_timing/DECISION.json`, of the
registry ledger (`wc -l` and the first 400 characters of forty lines) and of `.git/HEAD` of three checkouts. No `du`,
no `find`, no python, nothing written. Rules obeyed: `ctsp:CLAUDE.md` "Grid", memory note `no-jobs-on-login-node`.

## 1. The two volumes at 22:20 UTC on 2026-10-08 (GRIDLS)

| measure | value | source |
|---|---|---|
| HOME used | 4,050.75 GB of a 4,294.97 GB soft limit (8,589.93 hard); 2,921,043 files of 10,000,000 | `pan_quota` in GRIDLS. Unchanged from the 4,050 GB of 2026-10-07 (`dp:DATA_MANIFEST.md` §1): no FINALIZE has run, so nothing moved off HOME yet |
| Ceph used | 7 TB of 20 TB (39.39 %) | `df-ceph oschome` in GRIDLS. `$RS/data` alone was 5,333.691 GB with 4,579,361 files on 2026-10-08 (census job 40580051, `scr:census/census_merged_partial.tsv`) |
| queue | 7 jobs: `dp_migrate` 40580669 (hao1), 40580671 (mmi9), 40580673 (sfx5), all RUNNING 12:28:51 of 4-00:00:00 on reqp; `data_census2` 40580052 RUNNING 15:47:17 on secp; Beethoven `hpcw_worker` 40580248 RUNNING, 40581552 PENDING (Dependency), `hpcw_access` 40584406 PENDING (BeginTime) | `squeue` in GRIDLS. The three `dp_migrate` jobs are B04, B07 and B09 by elimination: those are the only batches with an item file and no `plan/runs/<B>/STATUS` (GRIDLS "STATUS files"); `dp:plan/logs/dp_migrate_40580669.out` (517 B), `_40580671.out` (441 B), `_40580673.out` (441 B) are still being written |

## 2. Migration state, batch by batch (truth = `~/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS`, read in GRIDLS)

Procedure and vocabulary: `dp:MIGRATION_PLAN.md` §3 (VERIFIED / ABSENT / cut over = `<path>.pre-ceph` + symlink /
FINALIZE deletes the `.pre-ceph` copy). **No batch is finalized**: every cut-over item still has its `.pre-ceph`
original beside the symlink in the HOME listing (GRIDLS "ls HOME", "ls ~/data", "ls ~/CTSpinoPelvic1K/data"), and
`pan_quota` is unchanged. `$RS/data/_index` does not exist (GRIDLS): the holding index was never built. `$RS/results`
does not exist: B13 was not run. `$RS/data/_staging/B04` exists (2 entries): B04's hard-link group is landing.
`dp:dedup/applied/` holds only `.gitkeep` on the laptop and on the grid: nothing has been linked.

| batch | STATUS on the grid | what that means |
|---|---|---|
| B00 DeepFluoro H5 | 001 VERIFIED: `~/deepfluoro` -> `$RS/data/deepfluoro_h5/raw/deepfluoro`, 76/76 files, 5,272,150,583 B, 76 sampled | cut over (symlink + `deepfluoro.pre-ceph` 2026-09-20 in GRIDLS) |
| B01 TCIA CT Colonography | 001 ABSENT `~/CTSpinoPelvic1K/data/tcia`; 002 ABSENT `.../tcia_nifti`; 003-005 VERIFIED `patient_db.json` 9,909,285 B, `patient_db.pkl` 2,409,446 B, `patient_db_summary.txt` 663 B | **resolves `HANDOFF/OPEN_QUESTIONS.md` B30**: "B01 cut over" means the three meta files only. The 721 GB raw DICOM and 336 GB NIfTI (du 2026-09-01, `dp:plan/batch_items/B01.tsv`) are gone from HOME and were never on Ceph: `$RS/data/tcia_ct_colonography` holds `meta/` only (GRIDLS). Nothing records what removed them; `~/cleanup_v1v3_tcia.sh` (1,136 B, 2026-09-01, HOME root in GRIDLS) is the likely script, unread |
| B02 CTSP release + build tree | "hard-link rsync rc=0"; 001 VERIFIED `~/data/CTSpinoPelvic1K` -> `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`, 2,417/2,417 files, 196,195,055,488 B, 200 sampled, flags hardlink_group,irreplaceable; 025 VERIFIED `0816_label_v4.nii.gz` 1,106,588 B; 027 VERIFIED `~/build_archive` 13 files 6,236,530,062 B; 028 `~/build_archive_private` 1 file 592 B; 029 `~/build_archive_stage` 2,474 files 3,035,170,658 B; **24 items ABSENT** (`hf_export_osc`, `placed`, `hf_export_v6/v5/v4/v2`, `zenodo_v6`, `zenodo_v7`, `v5_final`, `zenodo_upload`, `s1_recarve`, `hardware_fix`, `hf_export_v2_work`, `fix_0816*`, `hip_crossover_backup`, `hf_export_v3_work`, `v5_smoke`, `hardware_final_predust`, `hardware_final`, `hip_transpose_backup`, `thoracic_fix`, `fix_0816_pseudo_work`) | cut over; the ABSENT rows settle family-A unknowns 3-4 and family-E unknown 3 of `dp:DATA_MANIFEST.md` §10: the reclaim phases A and B did run, and `~/CTSpinoPelvic1K/data` now holds only json/txt remnants, `qc_dashboard/` and three symlinks (GRIDLS "ls ~/CTSpinoPelvic1K/data"). The build archive on Ceph (6.24 GB) is the staging of Zenodo 22647933 (memory note `zenodo-deposit`) |
| B03 HOME copies of CTSpine1K, CTPelvic1K | 001 ABSENT `.../ctspine1k`; 002 ABSENT `.../ctpelvic1k` | nothing to move. CTSpine1K exists on Ceph (`$RS/data/ctspine1k`, 162.350 GB census; `raw_data/`, `metadata/`, `hf_listing.json` 618,236 B, `fetch_status.json`). **CTPelvic1K datasets 1-5 are on neither volume**: `$RS/data/ctpelvic1k` does not exist (GRIDLS); only `ctpelvic1k_clinic` (datasets 6-7, 14.832 GB) is there |
| B04 plain-film corpora + spine-detector | no STATUS yet; job running | copying. HOME sources still real directories (`~/spine-detector/data/raw/{aasce, buu_full, buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}`, `buu_2000 -> ~/XRSpinoPelvic1K/data/BUU-LSPINE`; `data/{interim, yolo, yolo_dr_*, yolo_hw*, yolo_v2..v6f}` in GRIDLS). Targets `nhanes2_zenodo_landmarks`, `nhanes2_cdc_films`, `vindr_spinexr`, `spinal_ai2024`, `ieee_dataport_lateral_fullspine_236`, `csxa_cervical_xray_atlas`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `aasce2019_boostnet`, `cm_spine_drive_file`, `spine_detector_corpus` do not exist yet on Ceph; `$RS/data/mendeley_5jdfdgp762/raw` exists (filled by B14's `spondy_landmark`) |
| B05 XRSpinoPelvic1K data | not started (depends on B04) | `$RS/data/buu_lspine_2000` absent; `$RS/data/xrspinopelvic1k/derived` holds only `dis_renders` (B14). `~/XRSpinoPelvic1K/data/{BUU-LSPINE, dataset2024.zip 4,023,726,207 B, xrsp1k?}` still on HOME; `data/ct` and `data/labels` are dangling links to the deleted `~/CTSpinoPelvic1K/data/hf_export_v3` (GRIDLS) |
| B06 VerSe / VerSeFusion | 14/14 VERIFIED: `implant_verse` 2,254 files 159,368,901,079 B (candidate); `VerSeFusion/data` 6,951 files 194,191,642,435 B; `vf_813` 1,130 files 49,427,512,778 B; `ctsp_drr_obl` 2,512 files 365,536,630 B; `ctsp_drr_obl2` 5,022 files 729,979,464 B; `obl2_fov96_ctx` 9 files 13,327,845,295 B; `verse_drr` 1,492 files 477,053,118 B; `verse_drr_film` 757 files 98,040,685 B; `verse_drr_obl` 2,988 files 386,300,026 B; `verse_drr_obl2` 5,978 files 773,608,215 B; `verse_only_ctx` 42 files 743,721,823 B; `verse_soft_drr` 748 files 97,063,296 B; `vf_813_probe` 4 files 139,428,370 B; `vf_v10` 374 files 319,212,368 B | cut over: each HOME path is a symlink into `$RS/data/versefusion/{raw,derived}` with a `.pre-ceph` twin (GRIDLS). The STATUS sizes are measured, not the 2026-09-01 du: VerSeFusion/data is 194.2 GB, not 138.1 |
| B07 TotalSegmentator v2.0.1 / v3.0.0 | no STATUS yet; job running | copying; `$RS/data/totalsegmentator_v300/raw` exists (1 entry), `totalsegmentator_v201` absent; `~/data/TotalSegmentator` (172,032-byte directory) and `~/data/TotalSegmentator_v3` still real (GRIDLS) |
| B08 RSNA 2022 + RibFrac | 001 VERIFIED `~/data/rsna_cspine` 4 files 203,321,991,870 B (candidate); 002 VERIFIED `~/data/ribs` 89 files 78,699,138,633 B | cut over (symlinks + `.pre-ceph` in `~/data`) |
| B09 FluoroCap + FluoroGen | no STATUS yet; job running | copying; `$RS/data/fluorocap/raw` exists (1 entry); `fluorogen_synthetic` absent; `~/FluoroCap` (53,248-byte directory, 2026-09-20) still real |
| B10 single-source banks (64 items) | not started | every HOME bank still a real directory (GRIDLS); `$RS/data/carmlspine/derived`, `.../ctspinopelvic1k/derived`, `nhanes2_*`, `vindr_spinexr` absent |
| B11 multi-source banks, identity tables (64 items) | not started | `$RS/data/multisource_banks` absent; `~/allspine_*`, `~/films_*`, `~/scaling`, `~/patient_keys*.json`, `~/split_final.json`, `~/bank_splits.json` all on HOME |
| B12 | dropped 2026-10-08 (`dp:MIGRATION_PLAN.md` §5) | `nnunet/raw` stays on HOME |
| B13 results (optional) | not run | `$RS/results` absent; `~/ablate`, `~/bench`, `nnunet/results` on HOME |
| B14 identified 2026-10-08 | 9/9 VERIFIED: `qc.tar.gz` 196,147,947 B; `dis_renders` 5 files 10,869,856 B (restricted, candidate); `pitest` 10 files 13,899,387 B; `pdwtest` 2 files 2,710,749 B; `ostk_level_morphometry.csv` 302,994 B; `pdw_why.py` 1,761 B; `pi_ostk2.csv` 662 B; `s1v11` 835 files 1,189,924,200 B (restricted, irreplaceable); `~/data/spondy_landmark` 1,416 files 89,020,337 B (candidate) | cut over (nine symlinks in GRIDLS) |

Jobs that produced this, from `dp:plan/logs/` on the grid (GRIDLS): preflight 40580053; migrate 40580054, 40580667,
40580668, 40580669, 40580670, 40580671, 40580672, 40580673, 40580947, 40581405; cutover 40580666, 40580686, 40580944,
40580945, 40580955, 40581192, 40581423; visibility 40580683, 40580692, 40580739, 40580956, 40581193, 40581424. Dedup
hash jobs 40581845 and 40581924 (`dp:dedup/HASH_RESULTS.md`; their `hash_results/A01-A23.{json,tsv}` are on the grid
and in the laptop repository).

## 3. Grid holdings by project family

Sizes: "census" = `scr:census/census_merged_partial.tsv` (Ceph rows from job 40580051, HOME rows from jobs 40578909
and 40580052, apparent GB, dated 2026-10-07/08); "STATUS" = bytes in `plan/runs/<B>/STATUS`; "du 2026-09-01/19/20" =
`dp:plan/layout_map.csv` size_basis. "verified" = a verify_transfer pass (STATUS) or a sha256 record named in the
cited file; otherwise "listed only".

### 3.1 carm_detection (intraoperative C-arm level detection, SchwingNet paper 1 and 2)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `$RS/data/carmlspine` | C-ArmLSpine (Zenodo 22768651): `C-ArmLSpine.zip` 15,581,614,253 B + `.ok`, `unpacked/C-ArmLSpine`, `pose/`, `cases.csv`, `catalogue.json`, `compare_veridah*.csv`, `headers_dossier.json` 1,863,754 B, `dossier_look/` | 86.834 GB census | Ceph-native, stays | zip `.ok` marker; sha not read | the test device of paper 1; 149 cases, 299 spot frames after the 2026-09-23 repair (`dp:DATA_MANIFEST.md` §4 #20); case134 headers carry a real PatientID (#21): never print |
| `$RS/data/realxray` | 23 real-frame banks: `carmlspine`, `carmlspine_crops`, `carmlspine_cv`, `carmlspine_cv_prerepair`, `carmlspine_cvday(_prerepair)`, `carmlspine_cvfill`, `carmlspine_multi`, `carmlspine_pre_repair_2026-09-23(_crops)`, `carmlspine_sweep`, `cobra_elekta`, `_ap45`, `_g3test`, `_smoke`, `_v2`, `_v2_ap45`, `_v3`, `deepfluoro`, `geneva_hip`, `pelvis_landmarks`, `bournemouth_qf`, `view_census.json` | 3.408 GB census | Ceph-native | listed only | **no `cobra_varian` bank** (confirmed in GRIDLS): the 225 Varian cases were never exported (`HANDOFF/DATASET_USAGE.md` §2.3); `cobra_elekta_v3` and `_g3test` exist on the grid though the laptop `tools/realxray_banks.json` lacks them (`DATASET_USAGE.md` §6) |
| `$RS/data/realxray_work` | export work dirs `geneva_hip`, `deepfluoro` | 0.325 GB census | Ceph-native | listed only | |
| `$RS/data/cobra2026` | COBRA2026: 692 cases, 375,618 projections; `cases/` 42.16 GB | 808.615 GB census | Ceph-native | per `dp:DATA_MANIFEST.md` cobra2026 card | only 145 Elekta cases in any bank; Varian 0 of 225 (`DATASET_USAGE.md` §0 item 6) |
| `$RS/data/deepfluoro_h5/raw/deepfluoro` | DeepFluoro H5 release (6 specimens, 366 frames) + `ann/`, `img/` | 5,272,150,583 B STATUS | B00 cut over | VERIFIED (76 sampled); hashed root `list_sha256 2ccfdf83...` in `ssn:docs/RSNAI_DATA_MANIFEST.json` (`dp:MIGRATION_PLAN.md` §5) | `~/deepfluoro` symlink; `~/user/diffdrr_data` link resolves through it |
| `$RS/data/deepfluoro_vendor` | vendor DICOM deposit (2,659 frames + 19 CT; `unpacked/` 72.71 GB) | 110.987 GB census | Ceph-native | listed only | 2,293 frames unused (`DATASET_USAGE.md` §2.3) |
| `$RS/data/geneva_hip_src` | Geneva hip phantom (BV Pulsera) source archive | 1.111 GB census | Ceph-native | `archive.sha256` named in `dp:DATA_MANIFEST.md` family C unknown 24 (not read) | the never-trained unseen-device test |
| `$RS/data/ljubljana` | 2D-3D-GS (18 frames, PIXIUM 4600) + `2D-3D-GS.zip` | 0.307 GB census | Ceph-native | listed only | no truth bank built |
| `$RS/data/spinesac` | SpineSAC sawbone frames (`drive/` 4.15 GB) | 4.279 GB census | Ceph-native | listed only | no bone truth; no data licence (`dp:DATA_MANIFEST.md` §4 #27) |
| `$RS/data/devcorpus`, `devcorpus_arc` | styled device corpus (142 TS v3 whole spines, 5 styled corpora) | 18.280 + 0.721 GB census | Ceph-native | listed only | `DATASET_USAGE.md` §3.3 |
| `$RS/data/external` | `fluoro_video` public clips | 262.801 GB census (731,842 files) | Ceph-native | listed only | contents not read (family E unknown 14) |
| `$RS/data/or_ready` | the OR-readiness results root, 60 entries (GRIDLS): `alphabet_loss`, `arc`, `audit`, `auto_reference`, `bodybox_rescore`, `census`, `cobra_window`, `corpus_manifold`, `coverage`, `crossdev`, `devices`, `devices_refit(_constrained,_v2)`, `devlodo`, `devpool`, `diag_card`, `dual_loss`, `eval_gate`, `fig3_detection(_v3)`, `fig4_pairs(_v2..v5)`, `fig4_pixium_blob`, `figure2`, `film_ncurve`, `indomain`, `lcurve`, `learning(_cpu,_lat,_lat_cpu)`, `lodo`, `manifold`, `prior`, `rewindow`, `robust(_smoke)`, `spineps_ids`, `spinesac`, `story_rows(_f..f6,_final)`, `thoracic`, `v9`, `wholespine`, `window_probe`, `QUEUE_2026-09-22.txt`, `d1_selftest_*.out`, `v9_chain_jobs.txt` | 867.951 GB census (340,064 files) | Ceph-native, results | listed only | the numbers of paper 1 come from here (`HANDOFF/RESULTS_CATALOG.md` Part A); which sub-folders hold the 682 GB of models is not recorded (`dp:DATA_MANIFEST.md` or_ready card). `devices_refit*` exist, so whether the DeepFluoro cards were refitted under `DF_CONVERSION=linear` (OPEN_QUESTIONS B9) can now be read there |
| `$RS/data/fig6`, `figure1`, `gallery` | paper-2 Figure 6 (LevelCheck) material; Figure 1; gallery renders | 13.920 / 0.027 / 0.106 GB census | Ceph-native | listed only | `sn:results/fig6/frozen/v1/` is the laptop twin (`RECIPES.md` §3.1) |
| `$RS/model_night` | DeepFluoro anchor rounds `anchor_none_lin*`, `anchor_pairs_lin*_<specimen>`, `p2bend` | 0.831 GB census | Ceph-native | listed only | 2026-09-21 |
| `~/model_night` | the HOME results root (36,864-byte directory): `PIPELINE_STATE.md/.json`, `RESULTS.md`, `CHAIN_LEDGER.tsv`, `XRAY_DATASET_USAGE.md`, `anomaly_manifest/`, `benchmark_cina/`, `competitors/`, `count_*`, `detector_*json`, `heads_carm/` (36 files: `head_cv{0..4}(_v9init)`, `head_cvday{0..2}(_v9init)`, `head_mix`, `head_realonly`, `mixed_cv*.json`), `ensemble/` (not reached in the `head -120` listing), `logs/` | not sized (census had not reached it; see §6) | stays on HOME (526 code files name it: `dp:MIGRATION_PLAN.md` §7) | listed only | `PIPELINE_STATE.md` header still says to run the tool on the login node (stale; `HANDOFF/RECIPES.md` §0). **`heads_mixed/` (the shipped head `head_allspine_v9_mixed_kmax4_seed0.pt`, `DATASET_USAGE.md` §1) was not reached by the listing's `head -40`**: not verified in this pass |
| `~/allspine_v9_fov96_ctx` | the level bank: `rung_1.npz` 5,449,315,625 B, `meta.json` 73,837 B, `runs/model_rung_1_aug2.pt` 44,824,746 B (the SchwingNet encoder), `runs/result_rung_1_aug2.json` | 5.494 GB census | HOME; B11 not started; restricted (BUU pixels) | encoder registered: alias `allspine_v9_fov96_ctx_rung_1_aug2 -> model_registry/188f9fcbfa3c6de1/model_rung_1_aug2.pt` (GRIDLS aliases) | `ssn:slurm/allspine_v9_bank.sh` L21 `rm -rf`s this folder on rerun (`RECIPES.md` §5): never rerun in place |
| `~/carm_cvmix{0..4}_fov96_ctx` | fold banks + `runs/model_rung_1_ft_cv{k}(_v9init)_aug2.pt` | 3.371-3.410 GB each census | HOME; B11 | fold models registered (aliases `carm_cvmix{k}_fov96_ctx_rung_1_ft_cv{k}_v9init_aug2`, GRIDLS) | hold 2,632 VinDr and 2,100 FluoroCap crops (`DATASET_USAGE.md` §3.2) |
| `~/carm_cvdaymix{0..2}_fov96_ctx`, `carm_cvdaymix0_v9_fov96_ctx`, `carm_mix_fov96_ctx`, `carm_fov96_ctx`, `carm_cv{0..4}_{drr,fov96_ctx}`, `carm_cvday{0..2}_{drr,fov96_ctx}`, `carm_drr`, `carm_base_cache` (8.412 GB), `carm_base_cache_v9` (5.536 GB) | C-ArmLSpine frame and crop banks, caches | 3.33-3.41 GB per cvdaymix; others not sized | HOME; B10/B11 | listed only | `carm_drr` holds REAL frames in the DRR layout (`dp:DATA_MANIFEST.md` §4 #22); every HOME carm bank predates the 2026-09-23 repair (#20) |
| `~/spine-detector/runs/realxray/{rx_lodo_carmlspine_1024, rx_lodo_cobra_elekta_1024, rx_lodo_deepfluoro_1024, rx_only_carmlspine_1024, rx_only_carmlspine_multi_1024, rx_pooled_1024, rx_pooled_1024_init18}` | real-frame detectors; `rx_lodo_carmlspine_1024/weights/best.pt` is the SchwingNet sacrum/vertebra detector (`DATASET_USAGE.md` §1) | not sized | HOME (code checkout; `runs/` not in the plan) | **not in the registry**: no `rx_*` alias in GRIDLS; agrees with `ssn:docs/MODEL_REGISTRY.md` gap "no k-devices weight file has a SHA-256" | `runs/devcorpus/dc_{A,B}_held_*`, `dc_P_pooled` (21 arms) also present (GRIDLS); `runs/{coverage, detect, detect_v1, detect_v2, eval_h2h, g3, lcurve, pose, wholespine}` |
| `~/level_id_service` | `app.py`, `model_defs.py`, `weights/`, `service.log`, `service.pid` (2026-09-14) | not sized | HOME | listed only | a different product with `detect_v5z_epoch25` (`DATASET_USAGE.md` §1); the website never serves weights (memory `level-service-serving`) |
| `~/scaling`, `~/scaling_curves` | subset banks `s000_r100 ... s100_r100` (7); `scaling_curves/{cross, fig_scaling_curves.pdf, .png, scaling_devices.json, scaling_fewshot.json}` | 129.2 GB du 2026-09-20 / not sized | HOME; B11 (candidate) | listed only | answers OPEN_QUESTIONS B13 in part: `fig_scaling_curves` was drawn; the v2-lineage sweep is SUPERSEDED [LEAK] (`RESULTS_CATALOG.md` C2) |
| `~/corpus_final` | — | — | **does not exist** (GRIDLS) | — | OPEN_QUESTIONS B21: the G4 corpus was never built |
| `~/bench` | `ct_by_case` (802 links), `gt`, `spineps`, `totalsegmentator`, `vista3d`, `robust`, `xr_fov`, `fov`, `patch_context*`, `latency.json`, `runtime_cost_workstation.json`, `fig_runtime_workstation.{pdf,png}`, `model_registry.{csv,md}`, `mappings` | 35.845 GB census | HOME; B13 optional | listed only | OPEN_QUESTIONS B8: a workstation runtime-cost file exists |
| HOME identity tables | `patient_keys.json` 803,531 B; `patient_keys_v9.json` 803,566 B; `patient_keys_final.json` 5,913,937 B (+ `.20260923_191858` 1,170,983 B, `.20260923_193933` 4,301,704 B); `split_final.json` 8,065,646 B; `bank_splits.json` 2,807,421 B; `ctsp_patient_crosswalk.csv` 115,094 B; `ctsp_vid2patient.json` 30,821 B; `fluorocap_patient_keys.json` 112,088 B | sizes from GRIDLS | HOME; B10/B11, flagged irreplaceable | listed only | `~/split_final.json` is the frozen G3 split: a rerun of `g3_split.sh` overwrites it with no backup (`RECIPES.md` §3.1 row 4) |

### 3.2 render_devices (DRR banks, device cards, synthetic CTs)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `~/physics_drr`, `~/physics_rare`, `~/physics_drr_film`, `~/physics_rare_film`, `~/physics_smoke` | 7,045 physics renders (ctsp 2,430, totalseg 1,831, verse 1,463, implant 1,321) and 1,482 rare-anatomy renders (`DATASET_USAGE.md` §3.1) | not sized | HOME; B11 (`physics_*`), B10 (`physics_smoke`) | listed only (`ann/`, `img/` in GRIDLS) | the only route by which TotalSegmentator reaches the v9 bank |
| `~/ctsp_drr` (0.686 GB), `~/ctsp_drr_film`, `~/anchor_drr` (0.713 GB), `~/anchor_drr_c2`, `~/ts_drr`, `~/ts_drr_v3`, `~/implant_ts`, `~/implant_ct_smoke`, `~/implant_verse_smoke`, `~/cut_physics(_v2)` (1.236 GB each), `~/cut_rare(_v2)` (0.610 GB each), `~/cut_v1`, `~/cut_v2`, `~/fluorogen`, `~/spinalai_drr`, `~/mendeley_drr`, `~/aasce_drr`, `~/films_ap_drr` (11.325 GB), `~/vindr_det_drr`, `~/vindr_pseudo_drr`, `~/nhanes_drr`, `~/nhanes_pseudo` (74 GB du 2026-09-19), `~/lateral236_pseudo`, `~/vindr_pseudo`, `~/exp3_*` (4), `~/height_renders`, `~/ped_renders`, `~/postop_render`, `~/postop_smoke`, `~/render_smoke`, `~/rib_fragments_release`, `~/rib_fragments_v4`, `~/lstv_flag/renders*`, `~/polypose` | single-source render, pseudo-label and synthetic banks | as given, else not sized | HOME; B10/B11 not started | listed only | `ts_drr` path maps were computed from the v3 root (`dp:DATA_MANIFEST.md` §4 #19); `ts_drr_v3` read by nothing; `implant_ts` unfinished (355 subjects); `anchor_drr`'s own split leaks 301 of 801 people (#18) |
| `$RS/data/versefusion/derived/{implant_verse 159.4 GB, verse_drr, verse_drr_film, verse_drr_obl, verse_drr_obl2, verse_soft_drr, ctsp_drr_obl, ctsp_drr_obl2, obl2_fov96_ctx 13.3 GB, verse_only_ctx, vf_813 49.4 GB, vf_813_probe, vf_v10}` | VerSe render banks and conversions | STATUS bytes in §2 | B06 cut over | VERIFIED | `verse_drr` holds 13 `glgl*` byte twins (dedup A04, `removal_preferred`); `verse_soft_drr` has the row-spacing defect on 181 of 374; `ctsp_drr_obl*` are VerSe renders under a CTSP prefix |
| `$RS/data/polypose` | PolyPose synthetic + the HF DeepFluoro re-host under `hf/` | 87.713 GB census | Ceph-native | listed only | `VALIDATION.{json,md}` does not exist (OPEN_QUESTIONS C18) |
| `$RS/data/or_ready/devices`, `devices_refit`, `devices_refit_constrained`, `devices_refit_v2` | fitted device cards (nine terms per device) | inside or_ready | Ceph-native | listed only | the shipped cards live in `ssn:docs/devices/<device>.json` of the grid checkout (`RECIPES.md` §6); the Surgio-B51 card exists only on the grid |
| `~/data/TotalSegmentator` (v2.0.1, 1,228 CTs), `~/data/TotalSegmentator_v3` (1,939) | the two TS releases, zips + unpacked | 82.0 / 89.8 GB du (`dp:plan/batch_items/B07.tsv`) | HOME; B07 copying | not yet | `$RS/data/validation_ts/raw/*` links point into the v2 tree (`dp:LAYOUT.md` §4) |

### 3.3 transitional_fluoro and anomaly_scan_census (the transitional harvest, registry, ruleclass)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `$RS/ruleclass` | `CORPUS.md` 30,381 B, `ARM_B.md` 19,613 B, `corpus_counts.json` 20,963 B, `arms/{ts, moller_fast, moller, pelvis}`, `tiers/` (8), `code/` (21 entries; `ts_arm_gpu.sh`, `armb/*.sh`, `pelvis/*.sh`), `logs/` (802), `moller_masks/` (7), `containers/` 7.719 GB | 48.579 GB census (163,587 files) | Ceph-native; grows | listed only | memory note `ruleclass-super-detector-run`; `CORPUS.md` says 21,655 CTs against the tiers' 21,622 (OPEN_QUESTIONS B3), still unexplained |
| `$RS/ruleclass/arms/ts/STATUS.md` | Arm A (TotalSegmentator) status at 2026-09-29 04:23:52: tier 1 5,094 CTs = done 3,166 + exists 1,927 + failed 1 (remaining 1); tier 2 12,217 = done 10,398 + exists 968 + failed 3 + pending 848 (remaining 851, 19.7 GPU-h at measured mean, within budget) | — | — | read in GRIDLS | **answers OPEN_QUESTIONS B1 for arm A**: tier 1 complete but one CT; tier 2 848 pending (kidney_thoraxabdomen 176, nlst_pilot 484, panorama 155, idc 22, aortaseg60 2, quadra_hc 4, abdomenatlas 3, fdg 2) |
| `$RS/ruleclass/arms/pelvis/_timing/DECISION.json` (621 B, 2026-09-29 08:21) | `mode: tta`, `mode_reason: "no Dice on 0 TTA CTs: rule not met, keep the released TTA; WARNING only 0/0 timing CTs ok"`, `n_timing 0`, `tier2_go false`, `tier2_note: "tier 2 ready, NOT submitted: no projection"`; beside it `SUMMARY.md` 429 B, `agree_timing20.tsv` 3,569 B, `census.tsv` 2,989,732 B, `renders/` (20) | — | — | read in GRIDLS | **answers B1 for the pelvis arm**: the gate file was written, but from zero timing CTs; the production array never ran. `arms/pelvis/` holds per-collection folders (abdomenatlas3_mini, amos22, aortaseg60, barts_crl, cobra, ctsp, ctspine1k, idc, kidney_thoraxabdomen, ribfrac, tcia_fdg_pet_ct_lesions, ts, verse, waw_tace), `_agree`, `_model`, `_work`; what they contain is not recorded |
| `$RS/ruleclass/arms/moller_fast` (23 collection folders + `JOBS_ACCEL.txt`, `_claims_measure`, `_claims_predict`), `arms/moller` (15 entries) | Arm B Moller rib masks, fast and full configuration | inside 48.6 GB | Ceph-native | listed only | counts after 2026-09-27 (fast pass was 1,801 of 5,094 tier-1 CTs at 17:00 that day, `RESULTS_CATALOG.md` D.20) not recorded: read `JOBS_ACCEL.txt` and `_claims_*` in a job |
| `$RS/data/anomaly_harvest` | 24 entries: `acquisition/` (manifests, `jobs.txt`, logs, `alias_pairs*.csv`), `other_ct/`, `verse/`, `ctsp/`, `totalsegmentator/`, `validation_ts/`, `cobra/`, and one screen folder per fetched collection (`panorama/` holds `calls/`, `rows.csv`, `registry_rows.csv`, `gate*.csv`, `SUMMARY.md`, `review/`) | 325.817 GB census (1,063,032 files) | Ceph-native | listed only | **answers OPEN_QUESTIONS B2 in part**: PANORAMA has `calls/`, `rows.csv` and `registry_rows.csv` on disk (GRIDLS); their row counts were not read |
| `$RS/data/{idc 706.083, abdomenatlas3_mini 570.557, tcia_fdg_pet_ct_lesions 393.872, panorama 194.439, ctspine1k 162.350, amos22 102.615, pengwin2026 83.499, ribfrac 78.200, kidney_thoraxabdomen 75.938, nlst_pilot 73.544, waw_tace 47.151, curvas 29.994, deep_psma 24.253, quadra_hc 20.413, barts_crl 20.313, curvas_pdacvi 16.879, aortaseg60 15.929, ctpelvic1k_clinic 14.832, csi2014 6.641}` GB census | the family-B CT acquisitions (raw/, nifti/, fetch/) | as listed | Ceph-native | `fetch/verified.jsonl` per collection (not read) | fetched counts per collection: `dp:DATA_MANIFEST.md` §6 summary table; archives were deleted after unpack (family B unknown) |
| `$RS/data/{spineps 8.834, rare_class 5.797, validation_ts 0 (links), thoracic_xr 0.859, ctsp_april 86.883, d815_repair 0.001, vindr 0.002 (3 files), outline_conv 0 (243 files)}` GB census | SPINEPS harvest masks; rare-class renders; the 70-CT validation links; the AASCE open mirror; the April release inputs; Dataset815 flag repair; a VinDr placeholder; outline conversions | as listed | Ceph-native | listed only | `ctsp_april` is `drwxrwxrwx` (`dp:DATA_MANIFEST.md` §5 hazard 5) |
| `~/bench_ts` | SPINEPS+VERIDAH over 1,228 TS v2 + 374 VerSe CTs (`cases.csv`, `spineps/native/`) | 1.511 GB census | HOME; B11 | listed only | 31 "relabelled" masks are links back to raw masks (`RECIPES.md` §3.5) |
| `~/lstv_flag` | `LEARNING_CURVE.md`, `LSTV_FLAG_RESULTS.md`, `ANOMALY_INVENTORY.md`, `_lstv_phenotypes.csv`, `models/` (`lstv_flag_v1/v2.pt`, `tltv_flag_v1/v2.pt`, `sex_control_v1.pt`: registered, GRIDLS aliases), `curve/`, `buu_scores*`, `eval_*`, `folds_*`, `renders*` (B11) | not sized | HOME; `models/` and results stay | flag models registered | answers OPEN_QUESTIONS B15: `LEARNING_CURVE.md` exists; the master flag table `lstv_flag_labels_v2.csv` not seen in the `head -30` |
| `~/model_night/anomaly_manifest` | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (2026-09-17) | not sized | HOME | listed (folder) | `RESULTS_CATALOG.md` D.1 |
| `~/FluoroCap` | the literature harvest: `releases/FluoroCap_v0.1_{A,B}` (2026-09-13 22:35), `articles.jsonl`, `captions_*.jsonl`, `annotate/`, `archives/`, `commons/`, anchor and consistency JSONs, `PROTOCOL.md`, `README.md`, `MORNING_REPORT.md`, the weights `anchor_det_v1.pt`, `anchor_det_c2_v1.pt` (first 80 names in GRIDLS) | 316 GB du 2026-09-19 (`youtube/` 181-265 GB) | HOME; B09 copying; flagged irreplaceable + candidate | not yet | test set only by directive D1; 72.8 % of panels are reproductions (`dp:DATA_MANIFEST.md` §4 #35) |
| `~/fluorocap_drr`, `_drr_smoke`, `_fov96_ctx`, `_pack` | FluoroCap render and crop banks | not sized | HOME; B09 | listed only | dedup A16 |
| `~/REPORT.md` 20,227 B, `~/REPORT_interim.md` 16,115 B (2026-09-13) | FluoroCap night reports | small | HOME root | listed only | not in a repository as far as recorded |
| `$RS/review_tree` | — | — | **does not exist** (not in the `$RS` listing) | — | the transitional review tree was never built (`dp:DATA_MANIFEST.md` family B unknown) |

### 3.4 ctsp_dataset (CTSpinoPelvic1K release, build, nnU-Net datasets, NeurIPS appendix)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | the v11 working copy: `ct/` (802), `labels/` (802, 2026-09-16), `labels_v10/` (802), `labels.zip` 883,912,953 B, `manifest.json` 1,100,037 B, `splits_5fold.json` 247,222 B, `dataset_labels.json` 4,100 B, `dataset_labels_v10.json`, `KNOWN_ISSUES.md` 8,894 B, `README.md` 20,159 B, `SHA256SUMS.txt` 73,633 B, `LICENSE`, `fetch_from_tcia.py`, `reconstruct_ct.py` | 196,195,055,488 B, 2,417 files STATUS | B02 cut over; `~/data/CTSpinoPelvic1K` symlink; `.pre-ceph` kept | VERIFIED (200 sampled, link counts) | the only grid copy of the 802 CTs and of the v11 labels; HF still serves v10 (memory `hf-mirror-is-v10`); `labels/` checked file by file against Zenodo's SHA256SUMS per `dp:dedup/DEDUP_PLAN.md` §7 row 5 |
| `$RS/data/ctspinopelvic1k_build_tree/derived` | `build_archive` (13 files, 6,236,530,062 B), `build_archive_stage` (2,474 files, 3,035,170,658 B), `build_archive_private` (592 B), `qc_2026-06-12.tar.gz` 196,147,947 B, `s1v11/` (835 files, 1,189,924,200 B; restricted), `scratch_2026-09-10/{pitest, pdwtest, ostk_level_morphometry.csv, pdw_why.py, pi_ostk2.csv}`, `0816_label_v4.nii.gz` | as listed (STATUS) | B02 + B14 cut over | VERIFIED | `s1v11/out/v11_labels` = the release labels byte for byte (dedup A07, 802 identical, 1.19 GB; held for Greg's review) |
| `$RS/data/ctsp0533_repair` | the CT 0533 rebuild work tree incl. `0533_ct.TRUNCATED.20e673dc6c2a.nii.gz` | 0.604 GB census | Ceph-native | sha in memory `grid-ct-0533-truncated` | dedup A09: release file = repair candidate |
| `$RS/data/tcia_ct_colonography/meta` | `patient_db.json` 9,909,285 B, `patient_db.pkl` 2,409,446 B, `patient_db_summary.txt` 663 B (May 2026) | 12.3 MB | B01 cut over | VERIFIED | the only TCIA material left on either volume |
| `~/CTSpinoPelvic1K` | the public repository checkout: `master` at a0c51390970f57011fdd05123745bd2d79944c91 (GRIDLS `.git/refs/heads/master`; the laptop is at 7ddfe38); `morphometrics/` (26 CSV/PNG: `surgical_morphometrics.csv`, `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv`, `level_gradients.csv`, `castellvi_grades.csv`, `label_census*.csv` ...), `data/` remnants (`l6_audit.json` 68,138 B, `l6_truth.json` 71,737 B, `hip_crossover_*.json`, `itksnap_v4/5/6_labels.txt`, `qc_dashboard/`), `docs/`, `configs/`, `hardware_review/`, `gallery_*`, `fov_check/` | 7.699 GB census | stays on HOME | — | **flag**: `~/CTSpinoPelvic1K/.token` (38 B, 2026-05-20) is a credential file inside the checkout; a stray directory literally named `"\` with a file `md5sum \` (2026-09-10) is a heredoc-backslash leftover. OPEN_QUESTIONS B27 (recomputed on v11?) is not answered by names alone |
| `~/spinesurg-ct-nnunet/nnunet/raw` | `Dataset802_SpineSurgCTFull`, `Dataset803_SpineSurgCTFullMerged`, `Dataset804_SpineSurgCTFusedOnly`, `Dataset810_SpineSurgLSTVOneShot`, `Dataset813_SpineSurgLSTVFullRibs`, `Dataset815_SpineSurgLSTVVerSe` | not sized (links + labelsTr) | stays on HOME (B12 dropped) | listed only | imagesTr links are container paths: never repair (memory `dataset813-image-links-are-container-paths`) |
| `~/spinesurg-ct-nnunet/nnunet/results` | `Dataset802_SpineSurgCTFull`, `Dataset810_SpineSurgLSTVOneShot`, `Dataset813_SpineSurgLSTVFullRibs` | 348.6 GB du 2026-09-20 | HOME; B13 optional | listed only | **no `Dataset815` results**: the L6 VerSe set was never trained (memory `data-audit-99-gaps`); whether the Dataset813 folds finished and were scored is not shown by the listing (OPEN_QUESTIONS C19) |
| `$RS/neurips_v11` (10.174 GB), `$RS/neurips_tsv3` (2.250 GB), `$RS/neurips_spineps` (36 files), `$RS/data/ctsp_april` (86.883 GB) | the NeurIPS appendix chains (SPINEPS on the April release, v11 summaries, TotalSegmentator v3), cancelled 2026-09-27 (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`: jobs 40480728-33, 40480757, 40481314/15/23) | as listed | Ceph-native | listed only | OPEN_QUESTIONS A7: resubmit or cut Appendices I-J |
| `~/spinopelvic-seg` | the Dataset803 pseudolabeller checkout; `nnunet/raw` inspect-only in B14 | 27 GB du (`dp:MIGRATION_PLAN.md` §10) | HOME | — | Dataset803 has no `results/` tree on the grid; checkpoints on HF `OpenSpineConsortium/spinopelvic-seg-checkpoints` (`RECIPES.md` §3.2) |
| `~/CTSpinoPelvic1K-review` (2026-05-26), `~/ctspinopelvic1k-review-triaged` (2026-06-01), `~/spinesurg-ct-annotator.backup` (2026-08-10) | review Space material | not sized | HOME | listed only | may hold reviewer usernames: never copy |
| `~/qc.tar.gz` -> Ceph | pelvis-propagation QC PNGs 2026-06-12 | 196,147,947 B | B14 | VERIFIED | possibly the only copy (`dp:MIGRATION_PLAN.md` §8) |

### 3.5 ct_morphometry_parity and toolkit (ostk on the grid)

| path | holds | size | state | notes |
|---|---|---|---|---|
| `~/OpenSpineToolkit` | an rsync copy of ostk; **no `.git`** (`cat .git/HEAD` failed in GRIDLS) | not sized | HOME | commit unknown; the canal-closing regression (1b7005c) state in this copy is OPEN_QUESTIONS B29, unanswered |
| `~/ostk.tgz` (186,470 B, 2026-09-10), `~/ostk_run`, `~/ostk_shards`, `~/ostk_morph_out`, `~/logs_ostkext_40183713_*`, `logs_ostkmorph_*`, `logs_peddev_*`, `logs_pedbatch_*`, `logs_rheight_*` (2026-09-10) | the 2026-09-10 shard run of per-level morphometry and pedicle width | small | HOME root | the run whose PDW column came back empty (OPEN_QUESTIONS D2) |
| `$RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/{ostk_level_morphometry.csv 302,994 B, pi_ostk2.csv 662 B, pdw_why.py 1,761 B, pitest, pdwtest}` | that day's outputs and label copies | small | B14 cut over, VERIFIED | |
| `~/spinopelvic_all.csv` (63,562 B, 2026-09-10), `~/agg_spinopelvic.py`, `~/show_pi.py`, `~/ss_probe.py`, `~/disc_probe*.py`, `~/height_probe.py`, `~/cmp_pdw.py`, `~/lm_probe.py` | spinopelvic estimator scratch | small | HOME root | not in a repository as far as recorded |

### 3.6 plain_film_level_id (films, detector corpus, crop banks)

| path | holds | size | state | notes |
|---|---|---|---|---|
| `~/spine-detector` | private repository checkout (`.git` 2026-09-12): `data/raw/*` (the film corpora), `data/interim`, `data/yolo*` (16 export sets), `runs/`, `weights/`, `yolo11m-pose.pt` 42,459,307 B, `yolo11m.pt` 40,684,120 B, `export_onnx.py`, `onnx_out/`, `dist/` | 382 GB du 2026-09-19 | HOME; `data/raw/*`, `interim`, `yolo*` move in B04 (copying) | `nhanes_full` is a 2,334,720-byte directory (about 17,000 TIFFs); `vindr/` is DUA (owner-only on Ceph) |
| `~/films_drr` (36 GB), `~/films_all2_fov96_ctx` 26.278 GB, `~/films_ann_fov96_ctx` 13.861 GB, `~/allspine_fov96_ctx` 4.542, `~/allspine_v6_fov96_ctx` 23.018, `~/allspine_v7_fov96_ctx` 9.117, `~/allspine_v7nofluoro_fov96_ctx` 31.068, `~/allspine_v8_fov96_ctx` 5.494, `~/extra_fov96_ctx` 12.282, `~/buu_fov96_ctx` 9.981, `~/buu_yolo` 3.960, `~/film_style_ds` 0.962, `~/vindr_fov96_ctx`, `~/vindrps_fov96_ctx`, `~/nhanes_ctx`, `~/nhanes_split_ctx`, `~/nhanesps_fov96_ctx`, `~/mendeley_fov96_ctx`, `~/aasce_fov96_ctx`, `~/lat236ps_fov96_ctx`, `~/m_fov96_ctx`, `~/m_mask22_scale_ctx`, `~/merged_ctx`, `~/verse_ctx`, `~/verse_only_ctx_plus_nh`, `~/sd_fov96_ctx`, `~/mv_bands`, `~/pseudo_filtered`, `~/yolo_levels`, `~/sacrum_yolo`, `~/quiz_pack`, `~/reader_study`, `~/review_pack(_smoke,_v2)`, `~/verify_bench`, `~/films_all2_fov128m_ctx` (empty), `~/films_smoke` | crop banks and packs | census where given | HOME; B10/B11 not started; most superseded by v9 (`DATASET_USAGE.md` §1 lineage) | `allspine_v2..v5c` were deleted 2026-09-20 (memory `grid-quota-and-deleted-banks`); `allspine_v8` registered (alias `allspine_v8_fov96_ctx_rung_1_aug2 -> a8f55ab9c546f192`) |
| `~/XRSpinoPelvic1K` | private repository checkout: `data/BUU-LSPINE`, `data/dataset2024.zip` 4,023,726,207 B, `buu_splits.json`, `buu_yolo`, `drr_yolo`, `results*` (5), `runs`, `web_models`, `web_ref`, `annot/`, `weights/`, `yolo11n.pt`; `data/ct` and `data/labels` are dangling links to `~/CTSpinoPelvic1K/data/hf_export_v3/{ct,labels}` (deleted) | 22.428 GB census | HOME; B05 after B04 | **flag**: the checkout root holds `Q2VybmVyNzE1LlBvd2VyQ2hhcnQgRHJhZ29uIFByb2Q-.ica` (2,017 B, 2026-08-10, a Cerner session file) and `Unconfirmed 31234.crdownload`; never copy either |
| `$RS/data/inventory/films` | `FILM_CORPUS_INVENTORY.md` 2,839 B, `nhanes_film_manifest.csv` 2,109,890 B, `vindr_film_manifest.csv` 1,388,674 B, `film_corpus_inventory.json`, `box_convention/`; beside it `vindr_age_sex.csv` 830,061 B | small | Ceph-native | job 40416535 (`DATASET_USAGE.md` §8) |
| `$RS/data/thoracic_xr` | the AASCE open mirror (609 labelled) | 0.859 GB census | Ceph-native | dedup A15: 962 files identical to the HOME copy |

### 3.7 data_platform (the migration's own records)

| path | holds | size | state |
|---|---|---|---|
| `$RS/data/inventory/census_2026-10-07` | `census.json` 47,128 B, `census.py`, `census_job.sh`, `census_job2.sh`, `ceph/`, `home_after_F/`, `slurm_40578909.out` 4,973 B, `slurm_data_census2_40580051.out` 1,465 B, `slurm_data_census2_40580052.out` 50,676 B (still growing), `toplevel.sh`, `toplevel_listing.txt` 51,915 B, `_du_home.txt`, `_du_data.txt` | small | Ceph-native; laptop copies of all but the two `slurm_data_census2_*.out` and `census_job2.sh` in `scr:census/` |
| `~/spinesurg-ct-nnunet/data_platform/plan/{runs/B00,B01,B02,B03,B04,B06,B07,B08,B09,B14,markers}`, `plan/logs/*.out` (24), `dedup/hash_results/A01-A23`, `dedup/logs/dedup_hash_40581845.out`, `dedup_hash_40581924.out` | the migration's STATUS files, verify JSONs, job logs, hash verdicts | small | HOME (inside the checkout); STATUS texts captured in GRIDLS; `hash_results/` also in the laptop repository |
| `~/spinesurg-ct-nnunet` | the private repository checkout, `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405 (GRIDLS) against the laptop's 097933a; the grid cannot fetch the private remote, so folders ship by `git archive | ssh tar` (`RECIPES.md` §0 item 2) | 363 GB du 2026-09-19 (code + `nnunet/`) | HOME; code stays |

### 3.8 grid_access_students (Beethoven)

`$RS/hpcworker` 1.076 GB (`worker/`, `wayne-worker/`, `workspaces/`, `probe/`, `bptest/`, `.gate`), `$RS/hpcworker-ci` 0.010 GB,
`$RS/ashley` 2.136 GB (`containers/` 1.13 GB, `npm/`, `cache/`), `/rs/rs_grp_oschome/shared/{beethoven, access, ashley -> beethoven}`
(the shared tree is other-readable; the volume root is `drwxrws--T` with named-user ACL entries: memory `grid-access-list-gate`),
HOME `~/.beethoven` (`.ashley` -> `.beethoven`), `~/.hpcworker`, `~/hpcworker_src`, `~/ashley-bridge`, `~/ashley-test`,
`~/hpcworker-access-20261007-*`, `~/hpcw_probe_97845`, `$RS/tmp` 30.278 GB of `hpcworker` temp folders (2026-10-03, GRIDLS). All
census 40580051 / GRIDLS; nothing read beyond names. `~/.beethoven-vendor` is never read (`ctsp:CLAUDE.md`).

### 3.9 Environments, toolchains, containers (reference only)

`~/mambaforge` (envs `spineps`, `fluorogen`, `spinedet`, `nextflow`; 14 GB du), `~/anaconda3`, `~/miniforge`? (not listed; students
build `~/miniforge3`), `$RS/envs` 39.923 GB (`acq`, `fluoroclip`, `spineps212` 10.8, `spineps_cu128` 10.8, `tsv3` 9.2, `u251_drug`, `ytdl`),
`~/singularity_cache` (2026-09-26), `$RS/singularity_cache` 17.040 GB, `$RS/containers/bioconductor-minfi_1.48.0.sif` 555,257,856 B (U251),
`~/.cache` 10.484 GB census (was 103.9 GB on 2026-09-20), `~/totalseg_weights`, `~/spineps_models`, `~/NV-Segment-CTMR`, `~/rib-segmentation`
(2026-09-27), `~/Multi-View-Vertebra` (reference code), `~/gcc-14.2.0`, `~/gcc-9.1.0`, `~/cmake-4.0.2-linux-x86_64`, `~/intel`, `~/R`,
`~/myvenv`, `~/condainstall`. Sources: GRIDLS, census, `dp:LAYOUT.md` §3.

### 3.10 Not spine, personal, or credentials (never copied; listed so nothing is lost by accident)

- U251 (another study): `$RS/u251_multiomics` 1,115.871 GB, `u251_science` 594.039, `u251_host` 434.177, `u251_meth` 59.799,
  `u251_geo_meth` 0.187, `u251_envs`, `u251_raw`; `~/u251-xenograft-murine-RNASeq-study` (194 GB du), `~/u251_pull_backup_20260926(_1916)`,
  `~/gsea_home`, `$RS/Rlib`, `$RS/Rlib_cibersort`, `~/BrainGMTv2_*.gmt.txt` (census; GRIDLS).
- `$RS/private_ip` 0.634 GB (9 files): Greg's private records (`ctsp:CLAUDE.md`-era rule in the task brief).
- Credentials on HOME (listed in GRIDLS, contents never read): `~/.fluorocap/`, `~/.hf_org_token`, `~/.hf_osc_token`, `~/.zenodo_token`,
  `~/.kaggle/`, `~/.netrc`, `~/.ssh/`, `~/.google_authenticator`, `~/.gdrive_token`, `~/.geo_ftp_pass`, `~/pass_file`, `~/private`,
  `~/github` (41 B, a GitHub personal access token; mode 600 since 2026-10-08; **Greg rotates and deletes**), `~/.certs`,
  `~/CTSpinoPelvic1K/.token`, `~/XRSpinoPelvic1K/*.ica`, `~/.huggingface`, `~/.copilot`, `~/.claude`.
- Molecular simulation and old toolchains (2001-2024): `~/3`, `~/6`, `~/ada`, `~/output`, `~/v`, `~/testGOMC`, `~/gauss14`, `~/packmol`,
  `~/vmd-1.9.3`, `~/vmd_install_dir`, `~/wolf`, `~/xdr`, `~/rdf`, `~/prot`, `~/scl`, `~/la1.0`, `~/la101psx.tar`, `~/orient.tar`,
  `~/orient`, `~/Anaconda2-5.3.0-Linux-x86_64.sh` 647,650,387 B, `~/Anaconda3-2021.11-Linux-x86_64.sh` 608,680,744 B,
  `~/Mambaforge-Linux-x86_64.sh` 87,007,772 B, `~/Miniforge3-Linux-x86_64.sh` 82,862,660 B, `~/gcc-*.tar.*` (92 and 124 MB), `~/cmake-*.tar.gz`,
  `~/gdrive_*.tar.gz`, `~/git-lfs*`, `~/__MACOSX`, `~/to_greg.zip?origin_team=T5G027G83` (125,527 B, 2022-05-26), `~/view?usp=sharing`
  (67,453 B, 2022-01-26), PBS leftovers (`~/3_job_run.pbs`, `~/useSSHKeys.pbs`, `~/builder*`, `~/copy*`).

## 4. Model weights and the registry (GRIDLS "ls ~/model_registry", "aliases", "registry.jsonl"; `ssn:docs/MODEL_REGISTRY.md`)

- Store `~/model_registry/<sha16>/` (directories dated 2026-09-15 to 2026-09-24; 57 of them in the `head -60` listing, so the store
  holds at least 57 entries), ledger `registry.jsonl` **106 lines**, `aliases/` **79 symlinks**, `mlflow_runs.jsonl`; MLflow
  `~/mlflow/mlflow.db` 1,028,096 B (2026-09-18 21:03) and `~/mlflow/artifacts/`. The ledger repeats `orientation_net_v2` once every
  twenty minutes from 15:39 to 20:57 on 2026-09-15 (a sync loop re-registering the same sha), so 106 lines is not 106 models.
- Mirror: private HF `gregoryschwingmdphd/level-id-weights` (`MODEL_REGISTRY.md`); not checked from here (no network).
- Aliases that matter, with their store hash prefixes (all from GRIDLS):

| alias | store | role |
|---|---|---|
| `allspine_v9_fov96_ctx_rung_1_aug2` | `188f9fcbfa3c6de1/model_rung_1_aug2.pt` (2026-09-23) | the SchwingNet level encoder (`DATASET_USAGE.md` §1); settles "whether the v9 encoder is registered" (`RECIPES.md` §5): yes |
| `allspine_v8_fov96_ctx_rung_1_aug2` | `a8f55ab9c546f192` | v8 encoder |
| `allspine_v2_r1` | `00e84a90afa7ec52` | v2 encoder (its bank deleted; the gate refuses it) |
| `allspine_v1_rung1_aug2` | `4970f6bb30217f8e` | |
| `detector_v5z_final` | `797de71a9e0e42f7/detect_v5z_final_best.pt` (42,233,939 B) | the SchwingNet body detector |
| `detector_v5z_epoch25` | `5fde3060dbc15b71` (168,005,677 B) | shipped in `~/level_id_service` |
| `detector_v6f` | `479db0ab0d2b4c2f` | self-training arm |
| `det_g3_primary_s0` | `fe00a1732032e81a/best.pt` (2026-09-24) | the G3 detector |
| `carm_cvmix{0..4}_fov96_ctx_rung_1_ft_cv{k}_v9init_aug2`, `carm_cvdaymix{0..2}_..._v9init_aug2` | `071a7b8c…`, `be4eb8af…`, `a7cb4dac…`, `af14c417…`, `a143ae31…`; `cb33045f…`, `07dc5ff6…`, `c57be844…` | the fine-tuned fold models of Table 3 |
| the un-suffixed `..._ft_cv{k}_aug2`, `..._ft_cvday{k}_aug2`, `carm_fov96_ctx_rung_1_ft_realonly_aug2`, `carm_mix_fov96_ctx_rung_1_ft_mix_aug2` | 2026-09-21/22 | v2-lineage folds (SUPERSEDED, gate refuses) |
| `head_cv{0..4}_v9init`, `head_cvday{0..2}_v9init` | `74c9f287…`, `c99e00a7…`, `2be978cc…`, `b3e3bbca…`, `f25da830…`; `d1900dcf…`, `9dca735f…`, `f4de2c88…` | fold heads |
| `head_fig6_g3clean_{dual,lam0,lam1.0}_seed{0,1,2}`, `head_fig6_g3clean_dual_f{0.0625,0.125,0.25,0.5}_seed{0,1,2}` (21) | 2026-09-24 | paper-2 heads |
| `bank_g3_v2_rung_1_g3clean_aug2` | `629f0e058649ca1d` | G3 encoder |
| `recurrent_head_films_all2_r1` | `f4ec9180c718ea8b` | the 98.7/99.1/99.4 head: wrong-bank attribution (`OPEN_QUESTIONS.md` F5) |
| `films_all2_rung{1,2}(_aug2)` | `d081b4ab…`, `3654e9ba…`, `964e17f1…`, `de9a5dfe…` | superseded film models |
| `competitor_cina`, `competitor_kim`, `competitor_vertx` | `8f17aa30…`, `30b981af…`, `f0267ca3…` (2026-09-18) | re-implemented competitors; their ensemble result is in `~/model_night/ensemble/ensemble.json` (not read; OPEN_QUESTIONS B6) |
| `anchor_detector_v1`, `hardware_detector_v1/v2`, `panel_classifier`, `orientation_net`, `orientation_net_v2`, `fluorogen_lora_v1`, `cut_drr2fluoro_G`, `cut_drr2fluoro_G_v2`, `fluoro_ft_v3`, `lstv_flag_v1/v2`, `tltv_flag_v1/v2`, `sex_control_v1` | 2026-09-15 | FluoroCap-era and flag models |

- **Not in the registry** (no alias in GRIDLS): the real-frame detectors `~/spine-detector/runs/realxray/rx_*/weights/best.pt`
  (including `rx_lodo_carmlspine_1024`, the SchwingNet sacrum detector) and the device-corpus detectors `runs/devcorpus/dc_*`;
  the shipped head `head_allspine_v9_mixed_kmax4_seed0` (its folder `~/model_night/heads_mixed` was not reached in this pass);
  `anchor_det_c2_v1.pt` in `~/FluoroCap`; the nnU-Net checkpoints under `nnunet/results` (Dataset802/810/813); the Dataset803
  checkpoints (on HF only).

## 5. Result roots, in one place

`$RS/data/or_ready` (868 GB; paper 1), `$RS/data/fig6` (paper 2), `~/model_night` (HOME; `PIPELINE_STATE.md`, heads, ensemble,
anomaly manifest, logs), `$RS/model_night` (anchor rounds), `$RS/ruleclass` (census arms; `arms/ts/STATUS.md` and
`arms/pelvis/_timing/DECISION.json` read), `$RS/data/anomaly_harvest/<collection>/{rows.csv, registry_rows.csv, SUMMARY.md}`,
`~/bench` (35.8 GB), `~/ablate` (201.6 GB: `v5_all`, `v5_minus_all`, `v5_minus_extras`, `v5_minus_obl`, `v5_minus_pseudo`; OPEN_QUESTIONS B16:
the five ablation arms exist, their outcome not read), `~/scaling_curves`, `~/lstv_flag`, `~/FluoroCap` (reports, releases),
`$RS/neurips_v11`, `neurips_tsv3`, `neurips_spineps`, `$RS/cns2026_posterior` (5 files), `~/mlflow`, and about 300 loose audit scripts
and JSON outputs in the HOME root dated 2026-08-28, 2026-09-20 and 2026-09-22 (`_adv_*.py`, `_v*_*.py`, `verify_*.py`, `ts_*.py`,
`df_*.py`, `fc*.py`, `nh_*.py`, `mend_*.py`, `*.json`, `*.png`): the identity-audit scratch whose conclusions are
`ssn:docs/PATIENT_IDENTITY_SPEC.md` and `ssn:docs/DATA_COMPLETENESS_AUDIT.md` (names only; GRIDLS).

## 6. What is known to be MISSING from the grid, or not yet there

| item | evidence | what replaces it or what to do |
|---|---|---|
| TCIA CT Colonography raw DICOM (721 GB) and `tcia_nifti` (336 GB) | B01 STATUS rows 001/002 ABSENT; `$RS/data/tcia_ct_colonography` holds `meta/` only (GRIDLS); nothing records the deletion (`dp:DATA_MANIFEST.md` family A unknowns 1-2) | re-acquire with route `tcia_ctsp_download` (`dp:reacquire/reacquire.py tcia_ct_colonography`); the 802 release CTs themselves are safe in the v11 working copy |
| CTPelvic1K datasets 1-5 (Zenodo 4588403) | B03 row 002 ABSENT; no `$RS/data/ctpelvic1k` (GRIDLS) | re-download in a job; only `ctpelvic1k_clinic` (datasets 6-7) is on Ceph |
| CTSpine1K HOME copy | B03 row 001 ABSENT | the Ceph copy `$RS/data/ctspine1k` (162 GB, sha-verified 2026-09-23) stands |
| the CTSP build-tree intermediates (`hf_export_osc`, `placed`, `v5_final`, `hf_export_v2..v6`, `zenodo_v6/v7`, `s1_recarve`, `hardware_*`, `fix_0816*`, `hip_*`; 24 B02 items) and `hf_export`, `hf_export_v3` | B02 STATUS ABSENT; `dp:plan/layout_map.csv` rows 98, 102 `gone` | Zenodo build archive 22647933 and its Ceph staging `build_archive` (6.24 GB); `~/XRSpinoPelvic1K/data/{ct,labels}` links dangle because of this |
| `allspine_v2..v5c` crop banks (206.5 GB) | deleted 2026-09-20 (memory `grid-quota-and-deleted-banks`); `~/scaling` subset banks were cut from v2 | rebuildable from `slurm/build_allspine_v*.sh`; every number scored on them is LEAKED/SUPERSEDED (`HANDOFF/context/INDEX.md`) |
| `buu_drive` mirror (9.3 GB), `films_all4`, `extra3`, `extra4`, `obl_fov96_ctx`, `allspine_v2sd` | `layout_map.csv` row 126 `gone`; family D unknown 29 (no deletion record) | none needed |
| `Dataset815_SpineSurgLSTVVerSe` training | raw exists, `nnunet/results` has no Dataset815 (GRIDLS) | both prep jobs died on a missing singularity path (memory `data-audit-99-gaps`); never preprocessed |
| COBRA Varian frames (225 cases) | no `cobra_varian` under `$RS/data/realxray` (GRIDLS) | geometry map solved 2026-09-23, acceptance render pending (`DATASET_USAGE.md` §2.3) |
| Ljubljana truth bank; SpineSAC bone truth | no `ljubljana` bank in `realxray`; `or_ready/spinesac` holds predictions only | `DATASET_USAGE.md` §2.3 |
| the transitional review tree | no `$RS/review_tree` | `tools/transitional_review/` untracked; PREREG unsigned (`OPEN_QUESTIONS.md` A16, F12) |
| the flagship corpus G4 | no `~/corpus_final` (GRIDLS) | `ssn:docs/FLAGSHIP_PLAN.md` |
| the holding index | no `$RS/data/_index` | `sbatch -D "$PWD" dp:db/build_index.sbatch` after the batches |
| `$RS/results` (B13) | absent | Greg decides |
| FINALIZE of any batch | every `.pre-ceph` still present; HOME 4,050.75 GB | Greg's call per batch |
| TotalSegmentator v2.0.1, BUU-LSPINE, CSXA, NHANES II, VinDr, AASCE, Mendeley-716, lateral-236, Spinal-AI2024, the spine-detector `interim`/`yolo*`, FluoroCap, FluoroGen on Ceph | B04, B07, B09 still copying at 22:20 UTC (no STATUS) | wait for the three `dp_migrate` jobs; then cut over |
| every HOME render and crop bank, the identity tables, `~/scaling` on Ceph | B10, B11 not started | run after B04/B06/B07 land (`dp:plan/migration_batches.csv` depends_on) |
| the pelvis arm production run; tier-2 arm A remainder (848 CTs); Moller full configuration | `DECISION.json` tier2_go false, n_timing 0; `arms/ts/STATUS.md` | `$RS/ruleclass/code/pelvis/*.sh`, `ts_arm_gpu.sh` (held jobs 40481415-16, 40481574, 40481679 were cancelled 2026-09-27) |
| the three unsent data requests (14 fluoroscopy cine requests of 2026-09-26; SX-Stitch 1,032 intraoperative C-arm images; Balgrist ex-vivo CT + C-arm, 13 + 6 specimens) | `dp:DATA_MANIFEST.md` §8 cards `fluoro_cine_requests_2026_09_26`, `sx_stitch_request`, `balgrist_exvivo_request`: "Where it is now: Nowhere"; sent: not recorded | drafts in `ssn:docs/fluoro_requests_eml/`, `ssn:docs/data_requests/SX-Stitch_request.md`, `ssn:docs/outreach/balgrist_data_request_2026-09-21.md`; Greg sends |
| the seven gated CT collections (Stanford Merlin 18,317, RSNA RATIC 3,147, CT-RATE 21,304, Stanford INSPECT 19,402, CADS 753, RSNA RSPECT 7,279, MAGIC-CT 562) | `dp:DATA_MANIFEST.md` §6 group B7: no agreement signed | Merlin alone is estimated at about 447 L6 people (`RESULTS_CATALOG.md` D.13) |
| the 23 planned tier-2 and deferred collections (NLST 26,254 series 2.3 TB, LIDC-IDRI 1,010, STOIC 2,000, UniToChest 623, VSDFullBody 109, ENHANCE.PET 1,683, LUMOS 280, the TS task sets, AbdomenAtlas 2.0 Mini 10,135 ...) | `dp:DATA_MANIFEST.md` §6 groups B5-B6 "planned" | refused by the stopping rule until tier 1 is screened (`RESULTS_CATALOG.md` D.11) |
| CT Colonography remainder (21-23 people beyond the 802) | group B4 "planned (held)" | |
| human verdicts: `greg_verdict` on 546 registry review cases, FluoroCap reader verdicts, Castellvi whole-cohort read | `RESULTS_CATALOG.md` D.9; `dp:DATA_MANIFEST.md` §4 #35 | none on disk |
| the VinDr HPR determination number | `OPEN_QUESTIONS.md` A5 | |
| `OpenSpineToolkit` grid copy's commit | no `.git` (GRIDLS) | rsync again from the laptop (cb43197) when needed |
| the grid `spinesurg-ct-nnunet` checkout is behind the laptop (4e3fe93 vs 097933a) and cannot fetch | GRIDLS; `RECIPES.md` §0 | ship by `git archive | ssh tar`; `make physics*` must not be used (it hard-resets) |

## 7. Unknowns left by this pass, and flags

Unknowns: (1) which `dp_migrate` job is which batch (inferred B04/B07/B09 by elimination, not read from the logs); (2) the current
sizes of HOME entries after `films_ap_drr` alphabetically (`~/FluoroCap`, `~/model_night`, `~/nhanes_*`, `~/physics_*`,
`~/spine-detector`, `~/spinesurg-ct-nnunet`, `~/u251-*`, `~/vindr*`): census job 40580052 was still running and the laptop copy
`scr:census/home_after_F/census.tsv` ends at `films_ap_drr/img`; (3) whether `~/model_night/heads_mixed/` and `ensemble/ensemble.json`
exist (listing truncated); (4) what `~/FluoroCap` holds beyond its first 80 names; (5) counts inside `$RS/ruleclass/arms/moller_fast`
and `arms/pelvis/<collection>` after 2026-09-27; (6) PANORAMA's row counts; (7) whether the Ceph `tcia_ct_colonography/meta` files
are the only surviving TCIA metadata or whether `~/CTSpinoPelvic1K/data/patient_db.json.pre-ceph` differs (same bytes per STATUS);
(8) `~/VerseFusion` (24,769 B file) and `~/VerSeFusion.tar.gz` contents; (9) the two 2022 download leftovers; (10) the role of
`~/orient_v2`, `~/audit_out`, `~/filmid_out`, `~/spai_verify`, `~/ts_verify_out`, `~/ostk_morph_out`, `~/ostk_shards`,
`~/track5`, `~/reg`, `~/selective`, `~/plm`, `~/contours`, `~/ct_mine`, `~/ctr_smoke`, `~/space_backup`,
`~/gridtree_backup_20260924_1741`, `~/mpda_build`, `~/user` beyond name and date; (11) the live state of the HF mirror and
Zenodo v11 (no network).

Flags for Greg: `~/github` (token file; rotate and delete); `~/CTSpinoPelvic1K/.token` and `~/XRSpinoPelvic1K/*.ica` inside
checkouts; `$RS/data/ctsp_april` world-writable; `~/CTSpinoPelvic1K` contains a stray directory named `"\`; the registry ledger's
`orientation_net_v2` re-registration loop (16 identical lines); `PIPELINE_STATE.md` and `MODEL_REGISTRY.md` still tell a reader to
run python or `mlflow ui` on the login node; `$RS/archive` is empty although the Ceph README says finished rounds go there;
`$RS/data/morphdef` is three empty folders (removal candidate); B13 (627 GB) and 1,590.3 GB of deletion candidates
(`dp:MIGRATION_PLAN.md` §8) await decisions; no batch is finalized, so HOME stays at 94 % until Greg says FINALIZE.
