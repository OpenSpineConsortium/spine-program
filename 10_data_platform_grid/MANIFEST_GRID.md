# MANIFEST_GRID.md: every grid path this project uses or produced

HOME = `/wsu/home/go/go24/go2432` (Panasas). Ceph = `/rs/rs_grp_oschome/go2432` (CephFS, 20 TB, group `oschome`,
allocated 2026-09-21). Every path below is spelled in full; only a GRIDLS section name quoted as it stands in that file (for example "ls ~/data") keeps the `~` of the listing script, where `~` = HOME. "GRIDLS" = `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`,
the one read-only pass of 2026-10-08 22:20 UTC (`ls`, `cat` of small files, `squeue`, `pan_quota`, `df-ceph`; nothing
written); "STATUS" = the per-batch file `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS`
captured in GRIDLS; "census" = `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` (jobs 40578909, 40580051,
40580052; apparent GB, 2026-10-07/08); "du 2026-09-01" = `code/data_platform/plan/layout_map.csv` size basis; "plan" =
`code/data_platform/MIGRATION_PLAN.md`. "verified" means a `verify_transfer.py` pass recorded in STATUS (counts, sizes,
links, hard-link groups, a SHA-256 sample) or a SHA-256 record named in the cited file; "listed only" means the path was
seen in a listing and nothing more. Sizes are bytes where a STATUS file measured them, GB where a census or a du did.

## 1. The two volumes at 22:20 UTC on 2026-10-08

| measure | value | source |
|---|---|---|
| HOME used | 4,050.75 GB of a 4,294.97 GB soft limit (8,589.93 hard); 2,921,043 files of 10,000,000 | GRIDLS "pan_quota"; unchanged from 2026-10-07 (`code/data_platform/DATA_MANIFEST.md` section 1) because no FINALIZE has run |
| Ceph used | 7 TB of 20 TB (39.39 %); `/rs/rs_grp_oschome/go2432/data` 5,333.691 GB, 4,579,361 files | GRIDLS "df-ceph"; census (job 40580051) |
| queue | `dp_migrate` 40580669, 40580671, 40580673 RUNNING 12:28:51 of 4-00:00:00 on `reqp` (B04, B07, B09 by elimination: the only batches with an item file and no STATUS); `data_census2` 40580052 RUNNING 15:47:17 on `secp`; Beethoven `hpcw_worker` 40580248 RUNNING, 40581552 PENDING (Dependency); `hpcw_access` 40584406 PENDING (BeginTime) | GRIDLS "squeue" |

## 2. The migration, batch by batch (truth = STATUS on the grid)

Vocabulary (plan section 3): VERIFIED / ABSENT / RSYNC_FAILED / VERIFY_FAILED / DST_EXISTS per item; "cut over" = the
HOME original renamed `<path>.pre-ceph` and a symlink left at the old path; FINALIZE = a second comparison, then the
`.pre-ceph` copy deleted (the only step that frees HOME quota). **Every batch with data was finalized on 2026-10-11;
on 2026-10-12 B05 and B10 were finalized, and the chain completed at 08:41 EDT with B11 and B13 finalized** (the three
paragraphs below; on 2026-10-08 every cut-over item still had its `.pre-ceph` twin in the HOME listing, GRIDLS
"ls HOME", "ls ~/data", "ls ~/CTSpinoPelvic1K/data").

**State on 2026-10-11 (Greg's data-platform record).** Greg's record of 2026-10-11 (issue #49). Every batch with data
is copied, verified, cut over and FINALIZED, the `.pre-ceph` originals deleted after a full comparison: B00, B01, B02
(5 items), B04 (27), B06 (14), B07 (5), B08, B09 (7; FluoroCap 316 GB), B14 (9); B03 had nothing to move; B12 was
dropped. HOME went from 4,051 GB to 1,902 GB of the 4,295 GB soft limit. B05 (BUU-LSPINE 2000), B10 and B11 (the
banks) and B13 (results, 627 GB) were submitted as one chain on 2026-10-11 (migrate, cut over, finalize, visibility)
and were running on 2026-10-12; their HOME items are "on HOME, not reachable until migrated" until that chain's
finalize, after which the Ceph target of each item in `batch_items/B05`, `B10`, `B11`, `B13`
(`code/data_platform/plan/batch_items/`) is the readable path. Dedup links were applied on 2026-10-11 for groups A01
(185 VerSe'19 files, 8.4 GB), A05 (1,226 TotalSegmentator v2.0.1 CTs, 22.5 GB), A06 (3), A11 (77) and A15 (965); A14
(Mendeley twice) was refused on 1,412 read-only files and is to be rerun after a chmod; the A04 and A13 removals and
A07 wait on Greg; the guarded deletion job for the TotalSegmentator release zips and the NHANES extracted pickles was
submitted on 2026-10-11. Visibility as of 2026-10-11: every folder under `/rs/rs_grp_oschome/go2432/data/` is readable
by approved students, including the VinDr, BUU, Mendeley and `spine_detector_corpus` folders (at folder level; the
items inside them are the next paragraph).

**State on 2026-10-12 (read on the grid, issue #65).** B05 (BUU-LSPINE 2000): 3/3 VERIFY_OK, cut over, finalized.
B10: 64/64, cut over, finalized. B11: 64/64, cut over; its finalize was running at 03:30 EDT. B13: two items verified
(`/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` 299 GB, `/wsu/home/go/go24/go2432/ablate` 202 GB), cut
over, finalize running; the state of `/wsu/home/go/go24/go2432/bench`, B13's third item in the plan, is not recorded.
HOME held 1,334 GB of the 4,295 GB soft limit; Ceph `oschome` 9 of 20 TB. Visibility: until 2026-10-12 the plan's
`restricted` flag (`code/data_platform/plan/batch_items/`) still closed, item by item, the VinDr and BUU items inside the
folders opened on 2026-10-11 (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and BUU banks of B10 and B11,
`dis_renders`), mode `drwx--S---`. `publish_visibility.sh` was fixed (spinesurg-ct-nnunet d9b388d; the copy here is
`code/data_platform/plan/publish_visibility.sh`), and two visibility jobs open those items: 40599886 (the B04, B05, B10
and B14 folders) and 40599867 (after B13's finalize, every chain folder including `multisource_banks`); the outcome of
40599886 is not recorded here, and that of 40599867 is the next paragraph. Two paths were then owner-only:
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (private build material, not a
dataset) and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg read its Zenodo
upload scripts for a token); `s1v11` opened later that day (next paragraph).

**End of the chain, 2026-10-12 (Greg, issues #68, #69 and #72).** The chain completed at 08:41 EDT: every batch with
data is copied, verified, cut over and finalized (B13 3/3), with no refusal. Visibility job 40599867 opened the VinDr
and BUU banks in `multisource_banks`. `dedup_delete` job 40599718 deleted the TotalSegmentator v3.0.0 zip (37.4 GB) and
the NHANES extracted pickles (159 GB); job 40602927 deletes the v2.0.1 zip (23.58 GB). Dedup group A14 linked 1,413
files. HOME held 520 GB of the 4,295 GB soft limit (4,051 GB on 2026-10-08); Ceph `oschome` 9 of 20 TB. `s1v11` was
opened to approved students without the token check: spinesurg-ct-nnunet 0ab783f drops it from
`FIXED_RESTRICTED_PATHS` in `data_platform/plan/publish_visibility.sh`, and visibility job 40602925 opened
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (the copy
`code/data_platform/plan/publish_visibility.sh` here is still the file of d9b388d). One path stays owner-only,
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, because its one file is the
annotator map, students' personal data rather than a dataset or a token. Job 40602926 opened
`/rs/rs_grp_oschome/go2432/envs/spineps212` and `/rs/rs_grp_oschome/go2432/results` (B13's target) to approved
students. Whether job 40602927 has run is not recorded.

The table is the 2026-10-08 pass; its STATUS and state columns are superseded by the three paragraphs above.

| batch | HOME source (full path) | Ceph target (full path) | STATUS on the grid | size | state | verified |
|---|---|---|---|---|---|---|
| B00 | `/wsu/home/go/go24/go2432/deepfluoro` | `/rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro` | 001 VERIFIED, 76/76 files, 76 sampled | 5,272,150,583 B (STATUS) | cut over; `deepfluoro.pre-ceph` dated 2026-09-20 in GRIDLS | yes (STATUS; hashed root `deepfluoro_h5` list_sha256 in the RSNAI data manifest, plan section 5) |
| B01 | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia` (raw DICOM) | `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/raw` | 001 ABSENT | 721 GB (du 2026-09-01) | **gone from HOME and never on Ceph**; the Ceph folder holds `meta/` only (GRIDLS "ls RS/data/tcia_ct_colonography"); nothing records the deletion; `/wsu/home/go/go24/go2432/cleanup_v1v3_tcia.sh` (1,136 B, 2026-09-01) is the likely script, unread | no copy to verify |
| B01 | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia_nifti` | `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/converted` | 002 ABSENT | 336 GB (du 2026-09-01; regenerable by dcm2niix) | as above | no copy |
| B01 | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/patient_db.json`, `patient_db.pkl`, `patient_db_summary.txt` (same folder) | `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta/` | 003-005 VERIFIED | 9,909,285 B; 2,409,446 B; 663 B (STATUS) | cut over (symlinks in GRIDLS "ls ~/CTSpinoPelvic1K/data"); the `.pre-ceph` twins have the same bytes per STATUS | yes |
| B02 | `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` (the v11 working copy: 802 CTs + labels; `HF_EXPORT_DIR` of the Dataset810/813/815 containers) | `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | 001 VERIFIED, 2,417/2,417 files, 200 sampled; flags hardlink_group, irreplaceable; "hard-link rsync rc=0" | 196,195,055,488 B (STATUS) | cut over | yes |
| B02 | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/0816_label_v4.nii.gz` | `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz` | 025 VERIFIED | 1,106,588 B | cut over | yes |
| B02 | `/wsu/home/go/go24/go2432/build_archive`, `build_archive_private`, `build_archive_stage` | `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive*` | 027 VERIFIED 13 files; 028 VERIFIED 1 file; 029 VERIFIED 2,474 files | 6,236,530,062 B; 592 B; 3,035,170,658 B | cut over; the build archive is the staging of Zenodo 22647933 | yes |
| B02 | 25 build-tree folders (STATUS rows 002-024, 026, 030) under `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/` (`hf_export_osc`, `placed`, `hf_export_v6/v5/v4/v2`, `zenodo_v6`, `zenodo_v7`, `v5_final`, `zenodo_upload`, `s1_recarve`, `hardware_fix`, `hf_export_v2_work`, `fix_0816*`, `hip_crossover_backup`, `hf_export_v3_work`, `v5_smoke`, `hardware_final_predust`, `hardware_final`, `hip_transpose_backup`, `thoracic_fix`, `fix_0816_pseudo_work`) | (various) | ABSENT | 64.1 GB net of shared bytes (plan) | reclaim phases A and B ran (settles `DATA_MANIFEST.md` section 10 family-A unknowns 3-4); `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data` now holds json/txt remnants, `qc_dashboard/` and three symlinks (GRIDLS); `hf_export` and `hf_export_v3` also gone (`layout_map.csv` rows 98, 102), which is why `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/{ct,labels}` dangle | no copy |
| B03 | `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctspine1k`; `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctpelvic1k` | `/rs/rs_grp_oschome/go2432/data/ctspine1k/raw/home_copy`; `/rs/rs_grp_oschome/go2432/data/ctpelvic1k/raw/ctpelvic1k` (STATUS targets) | 001 ABSENT; 002 ABSENT | 190 GB; 36 GB (du 2026-09-01) | CTSpine1K stands on Ceph (`/rs/rs_grp_oschome/go2432/data/ctspine1k`: 162.350 GB census; `raw_data/`, `metadata/`, `hf_listing.json` 618,236 B, `fetch_status.json`; sha256-verified per file 2026-09-23 per plan section 8). **CTPelvic1K datasets 1-5 are on neither volume**: no `/rs/rs_grp_oschome/go2432/data/ctpelvic1k` (GRIDLS); only `/rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` (datasets 6-7, 14.832 GB census) | CTSpine1K yes (2026-09-23 record); CTPelvic1K no copy |
| B04 | `/wsu/home/go/go24/go2432/spine-detector/data/raw/{aasce, buu_full, buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}` (`buu_2000` is a symlink to `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/BUU-LSPINE`); `spine-detector/data/{interim, yolo, yolo_dr_*, yolo_hw*, yolo_v2..v6f}` (one hard-link group) | `/rs/rs_grp_oschome/go2432/data/{nhanes2_zenodo_landmarks, nhanes2_cdc_films, vindr_spinexr, spinal_ai2024, ieee_dataport_lateral_fullspine_236, csxa_cervical_xray_atlas, buu_lspine_3600, buu_lspine_v1_smoke, aasce2019_boostnet, cm_spine_drive_file, spine_detector_corpus, mendeley_5jdfdgp762}` | no STATUS; job running | 302.2 GB sized, 6 unsized, 159.0 GB candidates (plan) | copying; HOME sources still real directories (GRIDLS "ls ~/spine-detector/data"); targets absent on Ceph except `mendeley_5jdfdgp762/raw` (filled by B14); `/rs/rs_grp_oschome/go2432/data/_staging/B04` exists with 2 entries (the hard-link group landing) | not yet |
| B05 | `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/{BUU-LSPINE, dataset2024.zip (4,023,726,207 B), xrsp1k DRRs}` | `/rs/rs_grp_oschome/go2432/data/buu_lspine_2000`; `/rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived` | not started (depends on B04) | 4.7 GB sized, 2 unsized | on HOME; `data/ct` and `data/labels` there are dangling links to the deleted `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/hf_export_v3` (GRIDLS) | no |
| B06 | `/wsu/home/go/go24/go2432/implant_verse`; `VerSeFusion/data`; `vf_813`; `ctsp_drr_obl`; `ctsp_drr_obl2`; `obl2_fov96_ctx`; `verse_drr`; `verse_drr_film`; `verse_drr_obl`; `verse_drr_obl2`; `verse_only_ctx`; `verse_soft_drr`; `vf_813_probe`; `vf_v10` | `/rs/rs_grp_oschome/go2432/data/versefusion/{raw,derived}/...` | 14/14 VERIFIED | `implant_verse` 2,254 files 159,368,901,079 B (candidate); `VerSeFusion/data` 6,951 files 194,191,642,435 B; `vf_813` 1,130 files 49,427,512,778 B; `ctsp_drr_obl` 2,512 files 365,536,630 B; `ctsp_drr_obl2` 5,022 files 729,979,464 B; `obl2_fov96_ctx` 9 files 13,327,845,295 B; `verse_drr` 1,492 files 477,053,118 B; `verse_drr_film` 757 files 98,040,685 B; `verse_drr_obl` 2,988 files 386,300,026 B; `verse_drr_obl2` 5,978 files 773,608,215 B; `verse_only_ctx` 42 files 743,721,823 B; `verse_soft_drr` 748 files 97,063,296 B; `vf_813_probe` 4 files 139,428,370 B; `vf_v10` 374 files 319,212,368 B (STATUS) | cut over: each HOME path a symlink with a `.pre-ceph` twin (GRIDLS); B06 and its visibility pass finished 12:35 on 2026-10-08 (`memory/data-platform-migration-2026-10.md`). The measured VerSeFusion/data is 194.2 GB, not the 138.1 of the 2026-09-01 du | yes |
| B07 | `/wsu/home/go/go24/go2432/data/TotalSegmentator` (v2.0.1 zip + tree), `data/TotalSegmentator_v3` (v3.0.0), their DRR banks, `implant_ts` | `/rs/rs_grp_oschome/go2432/data/totalsegmentator_v201`; `/rs/rs_grp_oschome/go2432/data/totalsegmentator_v300` | no STATUS; job running | 210.8 GB sized, 2 unsized, 100.0 GB candidates (the two zips, 37.4 + 23.6 GB) | copying; `totalsegmentator_v300/raw` exists (1 entry), `totalsegmentator_v201` absent; HOME trees still real (GRIDLS). `ts_subjects` is a hashed root (plan) | not yet |
| B08 | `/wsu/home/go/go24/go2432/data/rsna_cspine`; `data/ribs` | `/rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw`; `/rs/rs_grp_oschome/go2432/data/ribfrac/raw` | 001 VERIFIED 4 files (candidate); 002 VERIFIED 89 files | 203,321,991,870 B; 78,699,138,633 B (STATUS) | cut over (symlinks + `.pre-ceph` in `/wsu/home/go/go24/go2432/data`). The RSNA zip is used by nothing and awaits Greg (`docs/handoff/OPEN_QUESTIONS.md` A19) | yes |
| B09 | `/wsu/home/go/go24/go2432/FluoroCap`; FluoroGen | `/rs/rs_grp_oschome/go2432/data/fluorocap/raw`; `/rs/rs_grp_oschome/go2432/data/fluorogen_synthetic` | no STATUS; job running | 316.0 GB sized, 6 unsized, 181.0 GB candidate (`youtube/`) | copying; `fluorocap/raw` exists (1 entry), `fluorogen_synthetic` absent; `/wsu/home/go/go24/go2432/FluoroCap` still real (GRIDLS). `/wsu/home/go/go24/go2432/.fluorocap` (credentials) never moves | not yet |
| B10 | 64 single-source banks on HOME (CT renders, film banks, C-arm fold banks; `/wsu/home/go/go24/go2432/nhanes_pseudo` 74 GB) | `/rs/rs_grp_oschome/go2432/data/<source>/derived/<bank>` (`carmlspine/derived`, `ctspinopelvic1k/derived`, `nhanes2_*`, `vindr_spinexr`, ...) | not started (after B02, B04, B06, B07) | 79.7 GB sized, 61 unsized (plan) | every HOME bank still a real directory (GRIDLS); targets absent | no |
| B11 | 64 multi-source banks, review packs, the `/wsu/home/go/go24/go2432/lstv_flag` render folders, and the identity tables `/wsu/home/go/go24/go2432/{patient_keys.json, patient_keys_v9.json, patient_keys_final.json (+2 dated copies), split_final.json, bank_splits.json, ctsp_patient_crosswalk.csv, ctsp_vid2patient.json, fluorocap_patient_keys.json}`; `/wsu/home/go/go24/go2432/allspine_*`, `/wsu/home/go/go24/go2432/films_*`, `/wsu/home/go/go24/go2432/scaling` | `/rs/rs_grp_oschome/go2432/data/multisource_banks/...` | not started (after B10) | 176.2 GB sized, 59 unsized, 129.2 GB candidates; identity tables 803,531 B; 803,566 B; 5,913,937 B; 8,065,646 B; 2,807,421 B; 115,094 B; 30,821 B; 112,088 B (GRIDLS) | all on HOME; `multisource_banks` absent on Ceph. **Back the identity tables up to Ceph with SHA-256 before this batch**; `slurm/allspine_v9_bank.sh` line 21 `rm -rf` means never rerun a bank in place | no |
| B12 | `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` | (none) | dropped 2026-10-08 | | stays on HOME: fifteen slurm scripts bind it into containers with no Ceph path (plan section 5) | n/a |
| B13 | `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` (348.6 GB), `/wsu/home/go/go24/go2432/ablate` (234.8 GB), `/wsu/home/go/go24/go2432/bench` (44 GB) | `/rs/rs_grp_oschome/go2432/results/` | not run; `/rs/rs_grp_oschome/go2432/results` does not exist (GRIDLS) | 627.4 GB (plan) | results, not imaging; Greg decides | no |
| B14 | `/wsu/home/go/go24/go2432/qc.tar.gz`; `/wsu/home/go/go24/go2432/dis_renders`; `/wsu/home/go/go24/go2432/pitest`; `/wsu/home/go/go24/go2432/pdwtest`; `/wsu/home/go/go24/go2432/ostk_level_morphometry.csv`; `/wsu/home/go/go24/go2432/pdw_why.py`; `/wsu/home/go/go24/go2432/pi_ostk2.csv`; `/wsu/home/go/go24/go2432/s1v11`; `/wsu/home/go/go24/go2432/data/spondy_landmark` | into the folders of their sources (`ctspinopelvic1k_build_tree`, `xrspinopelvic1k/derived/dis_renders`, `mendeley_5jdfdgp762/raw`, ...) | 9/9 VERIFIED | 196,147,947 B; 5 files 10,869,856 B (restricted, candidate); 10 files 13,899,387 B; 2 files 2,710,749 B; 302,994 B; 1,761 B; 662 B; `s1v11` 835 files 1,189,924,200 B (restricted, irreplaceable); `spondy_landmark` 1,416 files 89,020,337 B (candidate) (STATUS) | cut over (nine symlinks in GRIDLS); three entries still inspect-only (two 2022 download leftovers and `/wsu/home/go/go24/go2432/spinopelvic-seg/nnunet/raw`) | yes |

Jobs that produced the state above, from `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/logs/` (24
logs, GRIDLS "plan/logs"): preflight 40580053; migrate 40580054, 40580667, 40580668, 40580669, 40580670, 40580671,
40580672, 40580673, 40580947, 40581405; cutover 40580666, 40580686, 40580944, 40580945, 40580955, 40581192, 40581423;
visibility 40580683, 40580692, 40580739, 40580956, 40581193, 40581424. Duplicate-census hash jobs 40581845 and 40581924
(`code/data_platform/dedup/HASH_RESULTS.md`).

## 3. The platform's own records on the grid

| path | holds | size | state | verified |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/{B00,B01,B02,B03,B04,B06,B07,B08,B09,B14,markers}` | STATUS and `<n>.verify.json` per item; `markers/` records which source wrote which destination | small | HOME, inside the checkout; the STATUS texts are captured in GRIDLS | the STATUS files are the verification |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/logs/*.out` (24) | the job logs named above | small; `dp_migrate_40580669.out` 517 B, `_40580671.out` 441 B, `_40580673.out` 441 B still being written at 22:20 UTC | HOME | listed only |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A01-A23.{json,tsv}`; `dedup/logs/dedup_hash_40581845.out`, `dedup_hash_40581924.out`; `dedup/applied/` (only `.gitkeep`: nothing linked) | the duplicate-census verdicts | 3.7 MB | HOME; also in `code/data_platform/dedup/` here | the verdicts are hash comparisons (HASH_RESULTS.md) |
| `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/` | `census.json` 47,128 B, `census.py`, `census_job.sh`, `census_job2.sh`, `ceph/`, `home_after_F/`, `slurm_40578909.out` 4,973 B, `slurm_data_census2_40580051.out` 1,465 B, `slurm_data_census2_40580052.out` 50,676 B (still growing), `toplevel.sh`, `toplevel_listing.txt` 51,915 B, `_du_home.txt`, `_du_data.txt` | small | Ceph-native; laptop copies of all but the two `slurm_data_census2_*.out` and `census_job2.sh` are in `docs/grid_read_2026-10-08/census/` | listed only |
| `/rs/rs_grp_oschome/go2432/data/_staging/B04` | transient landing of B04's hard-link group (2 entries) | not recorded | removed by the job when the group is in place | n/a |
| `/rs/rs_grp_oschome/go2432/data/_index` | the holding index `holding.sqlite` | does not exist | never built (`TODO.md` step 3) | n/a |
| `/rs/rs_grp_oschome/go2432/README` | the Ceph root README of 2026-09-21 | small | says finished rounds go to `archive/` | listed only |
| `/rs/rs_grp_oschome/go2432/archive` | empty | 0 | contradicts the README; nothing archived | listed only |
| `/rs/rs_grp_oschome/go2432/data/morphdef` | three empty folders (`logs`, `out`, `src`) | 0 | removal candidate (plan section 8 gives the `rmdir` job) | listed only |
| `/rs/rs_grp_oschome/go2432/data/ctsp_april` | an April CTSP tree; shares no CT bytes with the release (hash group A08/A10) | not recorded | **world-writable** (flag for Greg) | hash verdict only |
| `/rs/rs_grp_oschome/go2432/tmp` | `hpcworker` temp folders (2026-10-03) | 30.278 GB (census) | Beethoven's; `11_students_grid_access` | listed only |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | the private repository checkout, `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405 (GRIDLS "grid checkout HEAD") against the laptop's 097933a; cannot fetch the private remote; ships by `git archive \| ssh tar` | 363 GB du 2026-09-19 (code + `nnunet/`) | HOME; code stays | listed only |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` | the public repository checkout (7.7 GB after the 2026-09-07 reclaim); contains a stray directory named `"\` and `.token` (38 B) | 7.7 GB (census) | HOME | listed only |
| `/wsu/home/go/go24/go2432/OpenSpineToolkit` | a copy with no `.git`; commit unknown; rsync again from cb43197 when needed | not recorded | HOME | listed only |
| `/wsu/home/go/go24/go2432/remote_wait.sh` | the allowed `squeue` poller; beside it `sweep3.sh`, `g3_launch_train.sh`, `g3_launch_truth.sh`, `fig6_release_open_gate.sh`, `grid_ff_checkout*.sh` (no longer work: the grid cannot fetch), `clip_sheets.{py,sbatch}`, `pick_demo_clips.py`, `export_envs.sbatch`, `env_spineps.yml`, `env_fluorogen.yml` | small | HOME root | listed only |

## 4. The model registry and MLflow (GRIDLS "ls ~/model_registry", "aliases", "registry.jsonl", "mlflow")

**Owner.** This project owns `/wsu/home/go/go24/go2432/model_registry` and its ledger `registry.jsonl` (PLAN.md section 3 listed the path under both 01 and 10; settled in the final pass of 2026-10-08, `../_plan/BUILD_RECORD.md`). Project 01 appends registration rows (its TODO S0) and project 12 names weights by registry id; neither edits the ledger. The repair of the ledger (the `orientation_net_v2` loop) is TODO step 5 here.

| path | holds | size | state |
|---|---|---|---|
| `/wsu/home/go/go24/go2432/model_registry/<sha256[:16]>/<file>` | one read-only directory per weight file; at least 57 entries (the `head -60` listing), dated 2026-09-15 to 2026-09-24 | not recorded | HOME; survived the migration (answers `OPEN_QUESTIONS.md` B31 for this path) |
| `/wsu/home/go/go24/go2432/model_registry/registry.jsonl` | the append-only ledger: **106 lines**, of which `orientation_net_v2` repeats once every twenty minutes from 15:39 to 20:57 on 2026-09-15 (a sync loop re-registering one sha: 17 lines carry that name, the first registration at 15:39:56 plus 16 repeats to 20:57:21), so 106 lines is not 106 models | small | HOME |
| `/wsu/home/go/go24/go2432/model_registry/aliases/<name>` | **79 symlinks** to the newest registration of each name | small | HOME; the aliases that matter to `01_carm_level_detection` are listed in that folder's manifest |
| `/wsu/home/go/go24/go2432/model_registry/mlflow_runs.jsonl` | sha to MLflow run id for after-the-fact registrations | small | HOME |
| `/wsu/home/go/go24/go2432/mlflow/mlflow.db`; `mlflow/artifacts/` | the MLflow SQLite store (2026-09-18 21:03) and artifacts | 1,028,096 B | HOME; survived (B31) |
| `hf://gregoryschwingmdphd/level-id-weights/registry/<name>/<sha>.<ext>` | the private off-cluster mirror | 1.1 GB for the sixteen backfilled models (`docs/MODEL_REGISTRY.md`) | not checked from here (no network) |
| not in the registry | the real-frame detectors `/wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_*/weights/best.pt` and `runs/devcorpus/dc_*`; the shipped head `head_allspine_v9_mixed_kmax4_seed0` (`/wsu/home/go/go24/go2432/model_night/heads_mixed`, not reached in the pass); `anchor_det_c2_v1.pt` in `/wsu/home/go/go24/go2432/FluoroCap`; the nnU-Net checkpoints under `nnunet/results` (Dataset802/810/813); the Dataset803 checkpoints (HF only) | | `docs/handoff/INFRASTRUCTURE.md` section 5 "gaps" |

## 5. Environments, toolchains, containers (reference only; nothing here is copied)

| path | holds | size | source |
|---|---|---|---|
| `/wsu/home/go/go24/go2432/mambaforge/envs/{spineps, fluorogen, spinedet, nextflow}` | the CPU env (`spineps`, Python 3.11, the one with a working MLflow SQLite backend), the GPU env (`fluorogen`), the detector env (`spinedet`); YAML exports in `code/env/` | 14 GB du | GRIDLS; `code/env/README.md` |
| `/rs/rs_grp_oschome/go2432/envs/{acq, fluoroclip, spineps212 (10.8 GB), spineps_cu128 (10.8), tsv3 (9.2), u251_drug, ytdl}` | Ceph-side environments | 39.923 GB | census |
| `/rs/rs_grp_oschome/go2432/singularity_cache`; `/wsu/home/go/go24/go2432/singularity_cache` (2026-09-26) | container caches | 17.040 GB (Ceph, census); HOME not recorded | census; GRIDLS |
| `/wsu/home/go/go24/go2432/.cache` | pip/torch/huggingface caches | 10.484 GB (census; was 103.9 GB on 2026-09-20) | census; `memory/grid-quota-and-deleted-banks.md` |
| `/wsu/home/go/go24/go2432/{totalseg_weights, spineps_models, NV-Segment-CTMR, rib-segmentation, Multi-View-Vertebra, gcc-14.2.0, gcc-9.1.0, cmake-4.0.2-linux-x86_64, intel, R, myvenv, condainstall, anaconda3}` | tool weights and toolchains | not recorded | GRIDLS |
| `/rs/rs_grp_oschome/go2432/containers/bioconductor-minfi_1.48.0.sif` | a U251 container (another study) | 555,257,856 B | census |

## 6. The identity tables and the real corpus (owned here, read by every model folder)

| path | holds | size | state |
|---|---|---|---|
| `/wsu/home/go/go24/go2432/patient_keys_final.json` (+ `patient_keys.json`, `patient_keys_v9.json`, two dated copies) | one key per person across every naming scheme (`code/tools/patient_keys.py`) | 5,913,937 B; 803,531 B; 803,566 B | HOME; moves in B11; irreplaceable |
| `/wsu/home/go/go24/go2432/split_final.json` | the G3 person split (FROZEN, apply 2026-09-23 20:18:48, job 40426793; never redraw: `docs/handoff/RECIPES.md` section 10) | 8,065,646 B | HOME; B11 |
| `/wsu/home/go/go24/go2432/bank_splits.json` | split lists recovered after the 2026-09-20 deletions | 2,807,421 B | HOME; B11 |
| `/wsu/home/go/go24/go2432/{ctsp_patient_crosswalk.csv, ctsp_vid2patient.json, fluorocap_patient_keys.json}` | the CTSP token crosswalk and the FluoroCap keys | 115,094 B; 30,821 B; 112,088 B | HOME; B11 |
| `/rs/rs_grp_oschome/go2432/data/or_ready/data_accounting/` | the content-hash chain's output | does not exist | never run on the real corpus (`docs/handoff/LEAKAGE.md` section 7 item 1) |
| `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/{touched.json, chk9/}` | the evaluation gate's record of every file every job touched; CHK-9 reports | `touched.json` 55.3 MB on the laptop copy (not copied here) | Ceph |
| `/rs/rs_grp_oschome/go2432/data/inventory/films/` (`nhanes_film_manifest.csv`, `FILM_CORPUS_INVENTORY.md`) | per-image film manifests (job 40416535) | not recorded | Ceph |
| `/rs/rs_grp_oschome/go2432/tmp/realxray_lists_audit.json`; `tmp/film_corpora_audit.json` | the real-frame list audit and the film-corpora audit | not recorded | Ceph `tmp/` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` | the RSNA 2022 header census (2,022 study directories) | not recorded | Ceph |

## 7. Credential files on HOME (by name only; contents never read; nothing copied)

`/wsu/home/go/go24/go2432/github` (41 B, a GitHub personal access token in plain text; mode 600 since 2026-10-08; **Greg rotates and
deletes**), `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token` (38 B, inside a public checkout), `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/*.ica`, `/wsu/home/go/go24/go2432/.fluorocap/`,
`/wsu/home/go/go24/go2432/.hf_org_token`, `/wsu/home/go/go24/go2432/.hf_osc_token`, `/wsu/home/go/go24/go2432/.zenodo_token`, `/wsu/home/go/go24/go2432/.kaggle/`, `/wsu/home/go/go24/go2432/.netrc`, `/wsu/home/go/go24/go2432/.ssh/`, `/wsu/home/go/go24/go2432/.google_authenticator`,
`/wsu/home/go/go24/go2432/.gdrive_token`, `/wsu/home/go/go24/go2432/.geo_ftp_pass`, `/wsu/home/go/go24/go2432/pass_file`, `/wsu/home/go/go24/go2432/private`, `/wsu/home/go/go24/go2432/.certs`, `/wsu/home/go/go24/go2432/.huggingface`, `/wsu/home/go/go24/go2432/.copilot`, `/wsu/home/go/go24/go2432/.claude`
(GRIDLS "ls HOME"). The laptop's `.beethoven-vendor` folder is never read. The rule: tokens are read from files, never
echoed, never on a command line or in `sbatch --export`.

## 8. Known to be missing from the grid, or not yet there (as of 2026-10-08)

| item | evidence | what replaces it or what to do |
|---|---|---|
| TCIA CT Colonography raw DICOM (721 GB) and NIfTI (336 GB) | B01 STATUS rows 001/002 ABSENT; `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography` holds `meta/` only; no deletion record | re-acquire with `code/data_platform/reacquire/reacquire.py tcia_ct_colonography` (route `tcia_ctsp_download`) in a job, or write the deletion record (`TODO.md` step 5); the 802 release CTs are safe in the v11 working copy |
| CTPelvic1K datasets 1-5 (Zenodo 4588403) | B03 row 002 ABSENT; no `/rs/rs_grp_oschome/go2432/data/ctpelvic1k` | re-download in a job; `ctpelvic1k_clinic` (datasets 6-7) is on Ceph |
| the 25 CTSP build-tree intermediates, `hf_export`, `hf_export_v3` | B02 ABSENT; `layout_map.csv` rows 98, 102 `gone` | Zenodo build archive 22647933 and its Ceph staging `build_archive` (6.24 GB) |
| `allspine_v2..v5c` crop banks (206.5 GB) | deleted 2026-09-20 (`memory/grid-quota-and-deleted-banks.md`) | rebuildable from `slurm/build_allspine_v*.sh`; every number scored on them is LEAKED or SUPERSEDED |
| `buu_drive` mirror (9.3 GB), `films_all4`, `extra3`, `extra4`, `obl_fov96_ctx`, `allspine_v2sd` | `layout_map.csv` row 126 `gone`; no deletion record (`DATA_MANIFEST.md` section 10 family-D unknown 29) | none needed |
| the holding index | no `/rs/rs_grp_oschome/go2432/data/_index` | `sbatch -D "$PWD" code/data_platform/db/build_index.sbatch` after the batches |
| `/rs/rs_grp_oschome/go2432/results` (B13) | absent | Greg decides |
| FINALIZE of any batch | every `.pre-ceph` present; HOME 4,050.75 GB | Greg's call per batch |
| TotalSegmentator v2.0.1, BUU-LSPINE, CSXA, NHANES II, VinDr, AASCE, Mendeley-716, lateral-236, Spinal-AI2024, the spine-detector `interim`/`yolo*`, FluoroCap, FluoroGen on Ceph | B04, B07, B09 copying at 22:20 UTC | wait for jobs 40580669, 40580671, 40580673; then cut over |
| every HOME render and crop bank, the identity tables, `/wsu/home/go/go24/go2432/scaling` on Ceph | B10, B11 not started | after B04, B06, B07 land (`migration_batches.csv` depends_on) |
| the content-hash chain on the real corpus | `or_ready/data_accounting/` absent | `docs/handoff/RECIPES.md` section 10 |
| the grid checkout at 097933a | at 4e3fe93; cannot fetch | ship by archive |

## 9. Unknowns left by the 2026-10-08 pass, and flags for Greg

Unknowns: (1) which `dp_migrate` job is which batch (inferred, not read from the logs); (2) the current sizes of HOME
entries after `films_ap_drr` alphabetically (census job 40580052 was still running; `docs/grid_read_2026-10-08/census/home_after_F/census.tsv`
ends at `films_ap_drr/img`); (3) whether `/wsu/home/go/go24/go2432/model_night/heads_mixed/` and `ensemble/ensemble.json` exist (listing
truncated); (4) what `/wsu/home/go/go24/go2432/FluoroCap` holds beyond its first 80 names; (5) whether the Ceph `tcia_ct_colonography/meta`
files are the only surviving TCIA metadata (the `.pre-ceph` twins have the same bytes per STATUS); (6) `/wsu/home/go/go24/go2432/VerseFusion`
(a 24,769 B file) and `/wsu/home/go/go24/go2432/VerSeFusion.tar.gz`; (7) the role of about twenty HOME scratch folders named in
`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` beyond name and date; (8) the live state of the HF mirror and
Zenodo v11 (no network); (9) why the grid can no longer fetch the private repository (`OPEN_QUESTIONS.md` B32).

Flags: `/wsu/home/go/go24/go2432/github` (rotate and delete); `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token` and `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/*.ica` inside checkouts;
`/rs/rs_grp_oschome/go2432/data/ctsp_april` world-writable; the stray `"\` directory in `/wsu/home/go/go24/go2432/CTSpinoPelvic1K`; the
registry ledger's 17-line `orientation_net_v2` loop; `/rs/rs_grp_oschome/go2432/archive` empty against its README; `/rs/rs_grp_oschome/go2432/data/morphdef`
three empty folders; 1,590.3 GB of deletion candidates await decisions. The 2026-10-08 flag "no batch is finalized"
no longer holds: every batch with data was finalized on 2026-10-11, B05 and B10 on 2026-10-12, and B11 and B13 when
the chain completed at 08:41 EDT on 2026-10-12, after which HOME held 520 GB of the 4,295 GB soft limit (section 2).
