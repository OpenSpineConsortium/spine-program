# DATA.md: the grid paths of this folder, reached through Beethoven

This file lists every grid path of `MANIFEST_GRID.md` sections 2 to 6, spelled as the manifest spells it, with its
volume, what it holds, its batch and its state on 2026-10-08 (the one read-only grid pass of 22:20 UTC,
`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`, "GRIDLS"), and one read-only check line per path. The access facts
are Greg's, dated 2026-10-11 (issue #4). Every number below restates `MANIFEST_GRID.md`, which names the file each one
comes from (STATUS, GRIDLS, the census, the plan); where a size or a fact is not in any file, this file writes "not
recorded".

**How to run a check line.** Every check runs from the Beethoven worker (`11_students_grid_access`), never python,
rsync or `du` on the login node (`CLAUDE.md` rule 7 of this folder). A directory gets `ls -ld <path>`; a file gets
`head -c 200 <file>`. A check line written with `{a,b}` expands in bash and covers each member; the braces carry no
spaces. A check on an ABSENT path is expected to answer "No such file or directory" — that answer is the check.

**Volumes.** HOME = `/wsu/home/go/go24/go2432` (Panasas). Ceph = `/rs/rs_grp_oschome/go2432` (CephFS, 20 TB, group
`oschome`). `.pre-ceph` beside a cut-over path is the HOME original until that batch's FINALIZE deletes it; which
batches are finalized is `MANIFEST_GRID.md` section 2 (the state of 2026-10-12 is in section 1 below).

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
by approved students, including the VinDr, BUU, Mendeley and `spine_detector_corpus` folders (at folder level; section 1
gives the items inside them and the one closed path as of 2026-10-12).

**State at the chain's end, 2026-10-12 (Greg, issue #68; `MANIFEST_GRID.md` section 2).** The chain completed at 08:41
EDT: every batch with data is copied, verified, cut over and finalized (B13 3/3), with no refusal, so the Ceph target of
each item in `batch_items/B05`, `B10`, `B11` and `B13` is the readable path. Visibility job 40599867 opened the VinDr
and BUU banks in `multisource_banks`. `dedup_delete` job 40599718 deleted the TotalSegmentator v3.0.0 zip (37.4 GB) and
the NHANES extracted pickles (159 GB); job 40602927 deletes the v2.0.1 zip (23.58 GB). Dedup group A14 linked 1,413
files. HOME held 520 GB of the 4,295 GB soft limit (4,051 GB on 2026-10-08); Ceph `oschome` 9 of 20 TB.

## 1. Access on 2026-10-11 (Greg, issue #4) and 2026-10-12 (issues #65, #69 and #72)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- On 2026-10-12 the VinDr and BUU items inside those folders opened too. Until then the plan's `restricted` flag
  still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and
  BUU banks of B10 and B11, `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain folder including
  `multisource_banks`) open them (issue #65).
- 2026-10-12: the copy `code/data_platform/plan/publish_visibility.sh` in this folder was replaced by the file of
  spinesurg-ct-nnunet d9b388d (issue #65), and later the same day by the file of 0ab783f, which it is now (issue #80,
  pull request #82).
- One path stays closed (owner-only):
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, whose one file is the
  annotator map, students' personal data rather than a dataset or a token (Greg, issue #69).
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` opened to approved students on 2026-10-12
  without the token check: spinesurg-ct-nnunet 0ab783f drops it from `FIXED_RESTRICTED_PATHS`, and visibility job
  40602925 opened it (Greg, issue #69). On 2026-10-12 the copy `code/data_platform/plan/publish_visibility.sh` here
  was replaced by the file of 0ab783f, which no longer lists it (issue #80).
- Job 40602926 opened `/rs/rs_grp_oschome/go2432/envs/spineps212` and `/rs/rs_grp_oschome/go2432/results` to approved
  students on 2026-10-12 (issue #72; `../11_students_grid_access/STUDENT_ENV.md`); both sit beside
  `/rs/rs_grp_oschome/go2432/data/`, not under it.
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students. Items still there are moved to
  the Ceph volume by the data-platform plan; on 2026-10-12 the chain completed at 08:41 EDT and every batch with data
  is finalized (`MANIFEST_GRID.md` section 2). Every such item in the tables below is marked **on HOME,
  not reachable until migrated**; a cut-over item's data is already readable at its Ceph target, and only the HOME
  symlink (and, until its batch's FINALIZE, the `.pre-ceph` twin) is out of reach.

## 2. Through Beethoven

Beethoven is the way a student reaches these paths. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (pages at https://openspineconsortium.com/beethoven/).

A student needs: a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and Chrome
on the invited Google account (issue #4). Approved means a named ACL entry `user:<AccessID>:rwx` on
`/rs/rs_grp_oschome`.

The two access facts again, because they decide what a check line can answer:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the volume
  root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`,
  `mendeley_5jdfdgp762` and `spine_detector_corpus` and, since 2026-10-12, the VinDr and BUU items inside them and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`; one path stays closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (the annotator map,
  students' personal data).
- Nothing on `/wsu/home/go/go24/go2432` is readable by students; items still there are marked **on HOME, not reachable
  until migrated** below, and Greg runs the HOME check lines until the batches land.

## 3. The migration paths (`MANIFEST_GRID.md` section 2)

State words are the manifest's: VERIFIED, copying, not started, ABSENT (plus "cut over" and B12's "dropped").

| path (as the manifest spells it) | volume | holds | batch | state on 2026-10-08 | check, from the Beethoven worker |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/deepfluoro` | HOME | the DeepFluoro h5 deposit: 76 files, 5,272,150,583 B (STATUS) | B00 | VERIFIED, cut over; `deepfluoro.pre-ceph` dated 2026-09-20; on HOME, not reachable until migrated (read the Ceph target); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/deepfluoro` |
| `/rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro` | Ceph | the verified copy of the above | B00 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/deepfluoro_h5/raw/deepfluoro` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia` | HOME | was the TCIA CT Colonography raw DICOM, 721 GB (du 2026-09-01) | B01 | ABSENT: gone from HOME and never on Ceph; nothing records the deletion (`/wsu/home/go/go24/go2432/cleanup_v1v3_tcia.sh`, 1,136 B, 2026-09-01, is the likely script, unread) | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/raw` | Ceph | planned target, never filled; the parent holds `meta/` only (GRIDLS) | B01 | ABSENT | `ls -ld /rs/rs_grp_oschome/go2432/data/tcia_ct_colonography` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia_nifti` | HOME | was the converted NIfTI, 336 GB (du 2026-09-01; regenerable by dcm2niix) | B01 | ABSENT, as above | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/tcia_nifti` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/converted` | Ceph | planned target, never filled | B01 | ABSENT | `ls -ld /rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/converted` (expect: no such file) |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/patient_db.json`, `patient_db.pkl`, `patient_db_summary.txt` (same folder) | HOME | the TCIA patient metadata: 9,909,285 B; 2,409,446 B; 663 B (STATUS) | B01 | VERIFIED (rows 003-005), cut over (symlinks); on HOME, not reachable until migrated (read the Ceph target); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/{patient_db.json,patient_db.pkl,patient_db_summary.txt}` |
| `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta/` | Ceph | the three metadata files above | B01 | VERIFIED | `head -c 200 /rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta/patient_db_summary.txt` |
| `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` | HOME | the v11 working copy: 802 CTs + labels; `HF_EXPORT_DIR` of the Dataset810/813/815 containers; 2,417 files, 196,195,055,488 B, hard-link group, irreplaceable (STATUS) | B02 | VERIFIED (200 sampled), cut over; on HOME, not reachable until migrated (read the Ceph target); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | Ceph | the verified v11 working copy | B02 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/0816_label_v4.nii.gz` | HOME | one repaired label file, 1,106,588 B (STATUS) | B02 | VERIFIED (row 025), cut over; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/0816_label_v4.nii.gz` |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz` | Ceph | the verified copy | B02 | VERIFIED | `head -c 200 /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz` |
| `/wsu/home/go/go24/go2432/build_archive`, `build_archive_private`, `build_archive_stage` | HOME | the staging of Zenodo 22647933: 13 files 6,236,530,062 B; 1 file 592 B; 2,474 files 3,035,170,658 B (STATUS) | B02 | VERIFIED (rows 027-029), cut over; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/{build_archive,build_archive_private,build_archive_stage}` |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive*` | Ceph | the verified copies; `.../derived/build_archive_private` is **the one closed path** (section 1; its one file is the annotator map) | B02 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive*` (`build_archive_private` answers "Permission denied" for a student: that answer is the check) |
| 25 build-tree folders (STATUS rows 002-024, 026, 030) under `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/` (`hf_export_osc`, `placed`, `hf_export_v6/v5/v4/v2`, `zenodo_v6`, `zenodo_v7`, `v5_final`, `zenodo_upload`, `s1_recarve`, `hardware_fix`, `hf_export_v2_work`, `fix_0816*`, `hip_crossover_backup`, `hf_export_v3_work`, `v5_smoke`, `hardware_final_predust`, `hardware_final`, `hip_transpose_backup`, `thoracic_fix`, `fix_0816_pseudo_work`) | HOME | were the CTSP build intermediates, 64.1 GB net of shared bytes (plan); the reclaim phases ran; what replaces them is Zenodo build archive 22647933 and its Ceph staging | B02 | ABSENT; `hf_export` and `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/hf_export_v3` also gone (`layout_map.csv` rows 98, 102), which is why `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/{ct,labels}` dangle; the folder now holds json/txt remnants, `qc_dashboard/` and three symlinks (GRIDLS) | `ls -la /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctspine1k` | HOME | was a HOME copy of CTSpine1K, 190 GB (du 2026-09-01) | B03 | ABSENT | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctspine1k` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/ctspine1k/raw/home_copy` | Ceph | STATUS target, never filled; CTSpine1K stands beside it (next row) | B03 | ABSENT | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspine1k/raw/home_copy` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/ctspine1k` | Ceph | CTSpine1K Ceph-native: `raw_data/`, `metadata/`, `hf_listing.json` 618,236 B, `fetch_status.json`; 162.350 GB (census); sha256-verified per file 2026-09-23 (plan section 8) | B03 | standing (not a migration copy) | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspine1k` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctpelvic1k` | HOME | was a HOME copy of CTPelvic1K, 36 GB (du 2026-09-01) | B03 | ABSENT | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/data/ctpelvic1k` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/ctpelvic1k/raw/ctpelvic1k` | Ceph | STATUS target; CTPelvic1K datasets 1-5 are on neither volume | B03 | ABSENT (no `/rs/rs_grp_oschome/go2432/data/ctpelvic1k` at all, GRIDLS) | `ls -ld /rs/rs_grp_oschome/go2432/data/ctpelvic1k` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` | Ceph | CTPelvic1K datasets 6-7, 14.832 GB (census) | — | standing | `ls -ld /rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` |
| `/wsu/home/go/go24/go2432/spine-detector/data/raw/{aasce, buu_full, buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}` (`buu_2000` is a symlink to `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/BUU-LSPINE`) | HOME | the raw film datasets of the detector corpus | B04 | copying (job running at 22:20 UTC); sources still real directories (GRIDLS); on HOME, not reachable until migrated; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/spine-detector/data/raw/{aasce,buu_full,buu_v1,cm_spine,csxa,lateral_236,mendeley_716,nhanes_annotated,nhanes_full,spinal_ai2024,vindr}` |
| `spine-detector/data/{interim, yolo, yolo_dr_*, yolo_hw*, yolo_v2..v6f}` (one hard-link group; under `/wsu/home/go/go24/go2432/spine-detector/data`) | HOME | the detector working trees | B04 | copying; on HOME, not reachable until migrated; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -la /wsu/home/go/go24/go2432/spine-detector/data` |
| `/rs/rs_grp_oschome/go2432/data/{nhanes2_zenodo_landmarks, nhanes2_cdc_films, vindr_spinexr, spinal_ai2024, ieee_dataport_lateral_fullspine_236, csxa_cervical_xray_atlas, buu_lspine_3600, buu_lspine_v1_smoke, aasce2019_boostnet, cm_spine_drive_file, spine_detector_corpus, mendeley_5jdfdgp762}` | Ceph | the B04 targets | B04 | copying; targets absent on 2026-10-08 except `mendeley_5jdfdgp762/raw` (filled by B14); readable by approved students on 2026-10-11, the VinDr and BUU items inside them after job 40599886 (section 1); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/{nhanes2_zenodo_landmarks,nhanes2_cdc_films,vindr_spinexr,spinal_ai2024,ieee_dataport_lateral_fullspine_236,csxa_cervical_xray_atlas,buu_lspine_3600,buu_lspine_v1_smoke,aasce2019_boostnet,cm_spine_drive_file,spine_detector_corpus,mendeley_5jdfdgp762}` |
| `/rs/rs_grp_oschome/go2432/data/_staging/B04` | Ceph | the transient landing of B04's hard-link group, 2 entries | B04 | copying; removed by the job when the group is in place; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/_staging/B04` |
| `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/{BUU-LSPINE, dataset2024.zip (4,023,726,207 B), xrsp1k DRRs}` | HOME | the BUU-LSPINE 2000 release, its zip, the xrsp1k DRRs; `data/ct` and `data/labels` there dangle (links to the deleted `hf_export_v3`, GRIDLS) | B05 | not started on 2026-10-08 (depends on B04); 3/3 VERIFY_OK, cut over and FINALIZED 2026-10-12 (issue #65); on HOME, not reachable until migrated (read the Ceph targets); the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/XRSpinoPelvic1K/data` then `ls -ld /wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/{BUU-LSPINE,dataset2024.zip}` |
| `/rs/rs_grp_oschome/go2432/data/buu_lspine_2000` | Ceph | B05 target | B05 | not started (absent on 2026-10-08); FINALIZED 2026-10-12 (issue #65) | `ls -ld /rs/rs_grp_oschome/go2432/data/buu_lspine_2000` |
| `/rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived` | Ceph | B05 target | B05 | not started (absent on 2026-10-08); FINALIZED 2026-10-12 (issue #65) | `ls -ld /rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived` |
| `/wsu/home/go/go24/go2432/implant_verse`; `VerSeFusion/data`; `vf_813`; `ctsp_drr_obl`; `ctsp_drr_obl2`; `obl2_fov96_ctx`; `verse_drr`; `verse_drr_film`; `verse_drr_obl`; `verse_drr_obl2`; `verse_only_ctx`; `verse_soft_drr`; `vf_813_probe`; `vf_v10` (all HOME-root entries except `VerSeFusion/data`; full spellings in `code/data_platform/LAYOUT.md` rows 267-283) | HOME | the VerSe-derived corpus: `implant_verse` 2,254 files 159,368,901,079 B; `VerSeFusion/data` 6,951 files 194,191,642,435 B; `vf_813` 1,130 files 49,427,512,778 B; eleven render banks and probes (per-item bytes in `MANIFEST_GRID.md` section 2 row B06) | B06 | VERIFIED 14/14, cut over (each HOME path a symlink with a `.pre-ceph` twin); on HOME, not reachable until migrated (read the Ceph target); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/{implant_verse,VerSeFusion/data,vf_813,ctsp_drr_obl,ctsp_drr_obl2,obl2_fov96_ctx,verse_drr,verse_drr_film,verse_drr_obl,verse_drr_obl2,verse_only_ctx,verse_soft_drr,vf_813_probe,vf_v10}` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/{raw,derived}/...` | Ceph | the verified B06 copies | B06 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/{raw,derived}` then `ls /rs/rs_grp_oschome/go2432/data/versefusion/derived` |
| `/wsu/home/go/go24/go2432/data/TotalSegmentator` (v2.0.1 zip + tree), `data/TotalSegmentator_v3` (v3.0.0), their DRR banks (`/wsu/home/go/go24/go2432/ts_drr`, `/wsu/home/go/go24/go2432/ts_drr_v3`, `code/data_platform/LAYOUT.md` rows 287-288), `implant_ts` (`/wsu/home/go/go24/go2432/implant_ts`) | HOME | the TotalSegmentator releases and their derived banks; 210.8 GB sized, 2 unsized (plan); `ts_subjects` is a hashed root (plan) | B07 | copying (job running at 22:20 UTC); HOME trees still real (GRIDLS); on HOME, not reachable until migrated; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/data/{TotalSegmentator,TotalSegmentator_v3} /wsu/home/go/go24/go2432/{ts_drr,ts_drr_v3,implant_ts}` |
| `/rs/rs_grp_oschome/go2432/data/totalsegmentator_v201` | Ceph | B07 target | B07 | copying; absent on 2026-10-08; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/totalsegmentator_v201` |
| `/rs/rs_grp_oschome/go2432/data/totalsegmentator_v300` | Ceph | B07 target; `raw` existed with 1 entry on 2026-10-08 | B07 | copying; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/totalsegmentator_v300` |
| `/wsu/home/go/go24/go2432/data/rsna_cspine` | HOME | the RSNA 2022 cervical archive, 4 files 203,321,991,870 B (STATUS); used by nothing, awaits Greg (`docs/handoff/OPEN_QUESTIONS.md` A19) | B08 | VERIFIED, cut over; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/data/rsna_cspine` |
| `/rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw` | Ceph | the verified copy | B08 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw` |
| `/wsu/home/go/go24/go2432/data/ribs` | HOME | RibFrac, 89 files 78,699,138,633 B (STATUS) | B08 | VERIFIED, cut over; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/data/ribs` |
| `/rs/rs_grp_oschome/go2432/data/ribfrac/raw` | Ceph | the verified copy | B08 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/ribfrac/raw` |
| `/wsu/home/go/go24/go2432/FluoroCap` | HOME | the FluoroCap capture corpus (316.0 GB sized over B09, 181.0 GB candidate `youtube/`, plan); out of training, a test set at most (root `CLAUDE.md` rule 9) | B09 | copying (job running at 22:20 UTC); still real (GRIDLS); on HOME, not reachable until migrated; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/FluoroCap` |
| FluoroGen (the manifest's spelling; `~/fluorogen`, i.e. `/wsu/home/go/go24/go2432/fluorogen`, per `code/data_platform/LAYOUT.md` row 301) | HOME | FluoroGen synthetic frames and the film-look LoRA | B09 | copying; on HOME, not reachable until migrated; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/fluorogen` |
| `/rs/rs_grp_oschome/go2432/data/fluorocap/raw` | Ceph | B09 target; existed with 1 entry on 2026-10-08 | B09 | copying; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/fluorocap/raw` |
| `/rs/rs_grp_oschome/go2432/data/fluorogen_synthetic` | Ceph | B09 target | B09 | copying; absent on 2026-10-08; FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /rs/rs_grp_oschome/go2432/data/fluorogen_synthetic` |
| 64 single-source banks on HOME (CT renders, film banks, C-arm fold banks; the manifest spells only `/wsu/home/go/go24/go2432/nhanes_pseudo`, 74 GB; the per-item list is `code/data_platform/LAYOUT.md`) | HOME | the single-source derived banks, 79.7 GB sized, 61 unsized (plan) | B10 | not started on 2026-10-08 (after B02, B04, B06, B07); 64/64, cut over and FINALIZED 2026-10-12 (issue #65); on HOME, not reachable until migrated (read the Ceph targets); the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/nhanes_pseudo` |
| `/rs/rs_grp_oschome/go2432/data/<source>/derived/<bank>` (`carmlspine/derived`, `ctspinopelvic1k/derived`, `nhanes2_*`, `vindr_spinexr`, ...) | Ceph | B10 targets | B10 | not started; targets absent on 2026-10-08; FINALIZED 2026-10-12 (issue #65) | `ls -ld /rs/rs_grp_oschome/go2432/data/carmlspine/derived /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/derived` |
| 64 multi-source banks, review packs, the `/wsu/home/go/go24/go2432/lstv_flag` render folders, `/wsu/home/go/go24/go2432/allspine_*`, `/wsu/home/go/go24/go2432/films_*`, `/wsu/home/go/go24/go2432/scaling`, and the identity tables (section 7 below) | HOME | the multi-source banks and the identity tables; 176.2 GB sized, 59 unsized, 129.2 GB candidates (plan); **back the identity tables up to Ceph with SHA-256 before this batch**; `slurm/allspine_v9_bank.sh` line 21 `rm -rf` means never rerun a bank in place | B11 | not started on 2026-10-08 (after B10); 64/64, cut over and FINALIZED 2026-10-12 (issues #65, #68); on HOME, not reachable until migrated (read the Ceph targets); the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/lstv_flag /wsu/home/go/go24/go2432/scaling` |
| `/rs/rs_grp_oschome/go2432/data/multisource_banks/...` | Ceph | B11 target | B11 | not started; absent on 2026-10-08; FINALIZED 2026-10-12, the VinDr and BUU banks in it opened by visibility job 40599867 (issue #68) | `ls -ld /rs/rs_grp_oschome/go2432/data/multisource_banks` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` | HOME | nnU-Net raw; fifteen slurm scripts bind it into containers with no Ceph path (plan section 5) | B12 | dropped 2026-10-08: stays on HOME; not reachable by students | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` (348.6 GB), `/wsu/home/go/go24/go2432/ablate` (234.8 GB), `/wsu/home/go/go24/go2432/bench` (44 GB) | HOME | results, not imaging; Greg decides | B13 | not run on 2026-10-08; on 2026-10-12 3/3 verified, cut over and FINALIZED (`nnunet/results` 299 GB, `ablate` 202 GB; issues #65, #68); on HOME, not reachable until migrated (read the Ceph target); the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results /wsu/home/go/go24/go2432/{ablate,bench}` |
| `/rs/rs_grp_oschome/go2432/results/` | Ceph | B13 target | B13 | did not exist on 2026-10-08 (GRIDLS); FINALIZED 2026-10-12 (issue #68); readable by approved students since job 40602926 (issue #72) | `ls -ld /rs/rs_grp_oschome/go2432/results` |
| `/wsu/home/go/go24/go2432/qc.tar.gz`; `/wsu/home/go/go24/go2432/dis_renders`; `/wsu/home/go/go24/go2432/pitest`; `/wsu/home/go/go24/go2432/pdwtest`; `/wsu/home/go/go24/go2432/ostk_level_morphometry.csv`; `/wsu/home/go/go24/go2432/pdw_why.py`; `/wsu/home/go/go24/go2432/pi_ostk2.csv`; `/wsu/home/go/go24/go2432/s1v11`; `/wsu/home/go/go24/go2432/data/spondy_landmark` | HOME | nine loose items (bytes per item in `MANIFEST_GRID.md` section 2 row B14); `s1v11` is irreplaceable (restricted in the plan until 2026-10-12, issue #69); three entries stayed inspect-only (two 2022 download leftovers and `/wsu/home/go/go24/go2432/spinopelvic-seg/nnunet/raw`) | B14 | VERIFIED 9/9, cut over (nine symlinks in GRIDLS); on HOME, not reachable until migrated (read the Ceph targets); FINALIZED 2026-10-11; the Ceph path is the only copy | `ls -ld /wsu/home/go/go24/go2432/{qc.tar.gz,dis_renders,pitest,pdwtest,ostk_level_morphometry.csv,pdw_why.py,pi_ostk2.csv,s1v11} /wsu/home/go/go24/go2432/data/spondy_landmark` |
| into the folders of their sources (`ctspinopelvic1k_build_tree`, `xrspinopelvic1k/derived/dis_renders`, `mendeley_5jdfdgp762/raw`, ...) | Ceph | the nine verified B14 copies; `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` was owner-only (`drwx--S---`, read 2026-10-12) until visibility job 40602925 opened it the same day without the token check (section 1; issue #69); `dis_renders` opens with job 40599886 | B14 | VERIFIED | `ls -ld /rs/rs_grp_oschome/go2432/data/xrspinopelvic1k/derived/dis_renders /rs/rs_grp_oschome/go2432/data/mendeley_5jdfdgp762/raw` |

## 4. The platform's own records on the grid (`MANIFEST_GRID.md` section 3)

| path | volume | holds | batch | state on 2026-10-08 | check, from the Beethoven worker |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/{B00,B01,B02,B03,B04,B06,B07,B08,B09,B14,markers}` | HOME | STATUS and `<n>.verify.json` per item; `markers/` records which source wrote which destination | — | the per-batch truth; on HOME, not reachable by students (Greg supplies the lines, section 10) | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/{B00,B01,B02,B03,B04,B06,B07,B08,B09,B14,markers}` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/logs/*.out` (24) | HOME | the migration job logs | — | listed only; three still being written at 22:20 UTC | `ls -l /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/logs` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/dedup/hash_results/A01-A23.{json,tsv}`; `dedup/logs/dedup_hash_40581845.out`, `dedup_hash_40581924.out`; `dedup/applied/` (only `.gitkeep`: nothing linked) | HOME | the duplicate-census verdicts, 3.7 MB; also in `code/data_platform/dedup/` here | — | on HOME, not reachable by students; the laptop copy in this folder is the student's copy | `ls -l /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/dedup/hash_results` |
| `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/` | Ceph | the census: `census.json` 47,128 B, job scripts, outputs (per-file list in `MANIFEST_GRID.md` section 3) | — | Ceph-native; laptop copies of most files in `docs/grid_read_2026-10-08/census/` | `ls -l /rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07` |
| `/rs/rs_grp_oschome/go2432/data/_staging/B04` | Ceph | B04's transient hard-link landing, 2 entries; size not recorded | B04 | removed by the job when the group is in place | `ls -ld /rs/rs_grp_oschome/go2432/data/_staging/B04` |
| `/rs/rs_grp_oschome/go2432/data/_index` | Ceph | the holding index `holding.sqlite` | — | does not exist; never built (`TODO.md` step 3) | `ls -ld /rs/rs_grp_oschome/go2432/data/_index` (expect: no such file until step 3 runs) |
| `/rs/rs_grp_oschome/go2432/README` | Ceph | the Ceph root README of 2026-09-21 | — | listed only | `head -c 200 /rs/rs_grp_oschome/go2432/README` |
| `/rs/rs_grp_oschome/go2432/archive` | Ceph | empty; contradicts the README | — | listed only | `ls -la /rs/rs_grp_oschome/go2432/archive` |
| `/rs/rs_grp_oschome/go2432/data/morphdef` | Ceph | three empty folders (`logs`, `out`, `src`); removal candidate (plan section 8) | — | listed only | `ls -la /rs/rs_grp_oschome/go2432/data/morphdef` |
| `/rs/rs_grp_oschome/go2432/data/ctsp_april` | Ceph | an April CTSP tree; shares no CT bytes with the release (hash group A08/A10); size not recorded | — | **world-writable** (flag for Greg) | `ls -ld /rs/rs_grp_oschome/go2432/data/ctsp_april` |
| `/rs/rs_grp_oschome/go2432/tmp` | Ceph | Beethoven's `hpcworker` temp folders, 30.278 GB (census) | — | `11_students_grid_access`'s | `ls -ld /rs/rs_grp_oschome/go2432/tmp` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | HOME | the private repository checkout at 4e3fe9386... (GRIDLS); 363 GB du 2026-09-19 (code + `nnunet/`); cannot fetch the private remote | — | code stays on HOME; not reachable by students; the repository itself is private (root `CLAUDE.md` rule 8) | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` | HOME | the public repository checkout, 7.7 GB (census); contains a stray directory named `"\` and `.token` (38 B, a credential: section 9 below, never read) | — | on HOME, not reachable by students | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K` |
| `/wsu/home/go/go24/go2432/OpenSpineToolkit` | HOME | a copy with no `.git`; commit unknown; size not recorded | — | on HOME, not reachable by students; rsync again from cb43197 when needed | `ls -ld /wsu/home/go/go24/go2432/OpenSpineToolkit` |
| `/wsu/home/go/go24/go2432/remote_wait.sh` (beside it `sweep3.sh`, `g3_launch_train.sh`, `g3_launch_truth.sh`, `fig6_release_open_gate.sh`, `grid_ff_checkout*.sh`, `clip_sheets.{py,sbatch}`, `pick_demo_clips.py`, `export_envs.sbatch`, `env_spineps.yml`, `env_fluorogen.yml`) | HOME | the allowed `squeue` poller and HOME-root scripts (the `grid_ff_checkout*.sh` no longer work: the grid cannot fetch) | — | on HOME, not reachable by students | `head -c 200 /wsu/home/go/go24/go2432/remote_wait.sh` |

## 5. The model registry and MLflow (`MANIFEST_GRID.md` section 4)

This project owns `/wsu/home/go/go24/go2432/model_registry` and its ledger (settled in the final pass of 2026-10-08,
`../_plan/BUILD_RECORD.md`). Everything in this table sits on HOME and is not reachable by students.

| path | volume | holds | batch | state on 2026-10-08 | check, from the Beethoven worker |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/model_registry/<sha256[:16]>/<file>` | HOME | one read-only directory per weight file; at least 57 entries, dated 2026-09-15 to 2026-09-24; size not recorded | — | survived the migration (answers `docs/handoff/OPEN_QUESTIONS.md` B31 for this path) | `ls /wsu/home/go/go24/go2432/model_registry` |
| `/wsu/home/go/go24/go2432/model_registry/registry.jsonl` | HOME | the append-only ledger: 106 lines, of which 17 carry one `orientation_net_v2` sha (a sync loop; 106 lines is not 106 models) | — | repair is `TODO.md` step 5 | `head -c 200 /wsu/home/go/go24/go2432/model_registry/registry.jsonl` |
| `/wsu/home/go/go24/go2432/model_registry/aliases/<name>` | HOME | 79 symlinks to the newest registration of each name | — | listed | `ls /wsu/home/go/go24/go2432/model_registry/aliases` |
| `/wsu/home/go/go24/go2432/model_registry/mlflow_runs.jsonl` | HOME | sha to MLflow run id for after-the-fact registrations | — | listed | `head -c 200 /wsu/home/go/go24/go2432/model_registry/mlflow_runs.jsonl` |
| `/wsu/home/go/go24/go2432/mlflow/mlflow.db`; `mlflow/artifacts/` | HOME | the MLflow SQLite store (1,028,096 B) and artifacts | — | survived (B31) | `ls -ld /wsu/home/go/go24/go2432/mlflow/mlflow.db /wsu/home/go/go24/go2432/mlflow/artifacts` |
| `hf://gregoryschwingmdphd/level-id-weights/registry/<name>/<sha>.<ext>` | off-cluster (Hugging Face, private) | the off-cluster mirror; 1.1 GB for the sixteen backfilled models (`docs/MODEL_REGISTRY.md`) | — | not checked from the grid (no network in the pass) | no grid check; network goes through WSL (root `CLAUDE.md` rule 10), owner only |
| not in the registry: `/wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_*/weights/best.pt` and `runs/devcorpus/dc_*`; the shipped head `head_allspine_v9_mixed_kmax4_seed0` (`/wsu/home/go/go24/go2432/model_night/heads_mixed`, not reached in the pass); `anchor_det_c2_v1.pt` in `/wsu/home/go/go24/go2432/FluoroCap`; the nnU-Net checkpoints under `nnunet/results` (Dataset802/810/813); the Dataset803 checkpoints (HF only) | HOME / off-cluster | the registry gaps (`docs/handoff/INFRASTRUCTURE.md` section 5 "gaps") | — | whether `model_night/heads_mixed` exists is not recorded (listing truncated, `MANIFEST_GRID.md` section 9 unknown 3) | `ls -ld /wsu/home/go/go24/go2432/spine-detector/runs/realxray /wsu/home/go/go24/go2432/model_night/heads_mixed` |

## 6. Environments, toolchains, containers (`MANIFEST_GRID.md` section 5; reference only, nothing copied)

| path | volume | holds | batch | state on 2026-10-08 | check, from the Beethoven worker |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/mambaforge/envs/{spineps, fluorogen, spinedet, nextflow}` | HOME | the CPU env (`spineps`, Python 3.11, the working MLflow SQLite backend), the GPU env (`fluorogen`), the detector env (`spinedet`); 14 GB du; YAML exports in `code/env/` | — | on HOME, not reachable by students; a student's environment is `../11_students_grid_access/STUDENT_ENV.md` (issue #66) | `ls -ld /wsu/home/go/go24/go2432/mambaforge/envs/{spineps,fluorogen,spinedet,nextflow}` |
| `/rs/rs_grp_oschome/go2432/envs/{acq, fluoroclip, spineps212 (10.8 GB), spineps_cu128 (10.8), tsv3 (9.2), u251_drug, ytdl}` | Ceph | Ceph-side environments, 39.923 GB (census) | — | standing; `spineps212` readable by approved students since job 40602926 (2026-10-12, issue #72; `../11_students_grid_access/STUDENT_ENV.md`); whether students can read the others is not recorded | `ls -ld /rs/rs_grp_oschome/go2432/envs/{acq,fluoroclip,spineps212,spineps_cu128,tsv3,u251_drug,ytdl}` |
| `/rs/rs_grp_oschome/go2432/singularity_cache`; `/wsu/home/go/go24/go2432/singularity_cache` (2026-09-26) | Ceph; HOME | container caches; 17.040 GB on Ceph (census); the HOME one not recorded | — | standing; the HOME one not reachable by students | `ls -ld /rs/rs_grp_oschome/go2432/singularity_cache /wsu/home/go/go24/go2432/singularity_cache` |
| `/wsu/home/go/go24/go2432/.cache` | HOME | pip/torch/huggingface caches, 10.484 GB (census) | — | on HOME, not reachable by students | `ls -ld /wsu/home/go/go24/go2432/.cache` |
| `/wsu/home/go/go24/go2432/{totalseg_weights, spineps_models, NV-Segment-CTMR, rib-segmentation, Multi-View-Vertebra, gcc-14.2.0, gcc-9.1.0, cmake-4.0.2-linux-x86_64, intel, R, myvenv, condainstall, anaconda3}` | HOME | tool weights and toolchains; sizes not recorded | — | on HOME, not reachable by students | `ls -ld /wsu/home/go/go24/go2432/{totalseg_weights,spineps_models,NV-Segment-CTMR,rib-segmentation,Multi-View-Vertebra,gcc-14.2.0,gcc-9.1.0,cmake-4.0.2-linux-x86_64,intel,R,myvenv,condainstall,anaconda3}` |
| `/rs/rs_grp_oschome/go2432/containers/bioconductor-minfi_1.48.0.sif` | Ceph | a U251 container (another study), 555,257,856 B (census) | — | standing | `ls -l /rs/rs_grp_oschome/go2432/containers/bioconductor-minfi_1.48.0.sif` |

## 7. The identity tables and the real corpus (`MANIFEST_GRID.md` section 6; owned here, read by every model folder)

| path | volume | holds | batch | state on 2026-10-08 | check, from the Beethoven worker |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/patient_keys_final.json` (+ `patient_keys.json`, `patient_keys_v9.json`, two dated copies) | HOME | one key per person across every naming scheme (`code/tools/patient_keys.py`); 5,913,937 B; 803,531 B; 803,566 B | B11 | irreplaceable; on HOME, not reachable until migrated (B11 cut over and FINALIZED 2026-10-12, issue #68; read the Ceph target in `batch_items/B11`) | `ls -l /wsu/home/go/go24/go2432/{patient_keys_final.json,patient_keys.json,patient_keys_v9.json}` |
| `/wsu/home/go/go24/go2432/split_final.json` | HOME | the G3 person split (FROZEN 2026-09-23 20:18:48, job 40426793; never redraw: `docs/handoff/RECIPES.md` section 10); 8,065,646 B | B11 | on HOME, not reachable until migrated; B11 cut over and FINALIZED 2026-10-12 (issue #68; read the Ceph target in `batch_items/B11`) | `ls -l /wsu/home/go/go24/go2432/split_final.json` |
| `/wsu/home/go/go24/go2432/bank_splits.json` | HOME | split lists recovered after the 2026-09-20 deletions; 2,807,421 B | B11 | on HOME, not reachable until migrated; B11 cut over and FINALIZED 2026-10-12 (issue #68; read the Ceph target in `batch_items/B11`) | `ls -l /wsu/home/go/go24/go2432/bank_splits.json` |
| `/wsu/home/go/go24/go2432/{ctsp_patient_crosswalk.csv, ctsp_vid2patient.json, fluorocap_patient_keys.json}` | HOME | the CTSP token crosswalk and the FluoroCap keys; 115,094 B; 30,821 B; 112,088 B | B11 | on HOME, not reachable until migrated; B11 cut over and FINALIZED 2026-10-12 (issue #68; read the Ceph target in `batch_items/B11`) | `ls -l /wsu/home/go/go24/go2432/{ctsp_patient_crosswalk.csv,ctsp_vid2patient.json,fluorocap_patient_keys.json}` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/data_accounting/` | Ceph | the content-hash chain's output | — | does not exist; never run on the real corpus (`docs/handoff/LEAKAGE.md` section 7 item 1) | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/data_accounting` (expect: no such file) |
| `/rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/{touched.json, chk9/}` | Ceph | the evaluation gate's record of every file every job touched; CHK-9 reports; `touched.json` 55.3 MB on the laptop copy | — | standing | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate/{touched.json,chk9}` |
| `/rs/rs_grp_oschome/go2432/data/inventory/films/` (`nhanes_film_manifest.csv`, `FILM_CORPUS_INVENTORY.md`) | Ceph | per-image film manifests (job 40416535); size not recorded | — | standing | `ls -l /rs/rs_grp_oschome/go2432/data/inventory/films` |
| `/rs/rs_grp_oschome/go2432/tmp/realxray_lists_audit.json`; `tmp/film_corpora_audit.json` | Ceph | the real-frame list audit and the film-corpora audit; sizes not recorded | — | standing, in Ceph `tmp/` | `head -c 200 /rs/rs_grp_oschome/go2432/tmp/realxray_lists_audit.json` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` | Ceph | the RSNA 2022 header census (2,022 study directories); size not recorded | — | standing | `head -c 200 /rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` |

## 8. Terms, where the folder records them

- **VinDr-SpineXR**: under a DUA (`CLAUDE.md` rule 9 of this folder); the card spells it "PhysioNet Restricted Health
  Data License 1.5.0 (named-person DUA)" (`code/data_platform/sources.json`, card `vindr_spinexr`).
- **BUU-LSPINE**: under an EULA (`CLAUDE.md` rule 9); the card spells it "EULA (no licence; acknowledgement required;
  no re-identification); never redistribute" (`code/data_platform/sources.json`, card `buu_lspine_3600`; the 2000
  release and the v1 smoke copy carry the same terms, cards `buu_lspine_2000`, `buu_lspine_v1_smoke`).
- **CTSpinoPelvic1K**: CC BY-NC-SA 4.0; the card spells it "labels CC BY-NC-SA 4.0; CT images CC BY 3.0"
  (`code/data_platform/sources.json`, card `ctspinopelvic1k`).
- **TotalSegmentator**: CC BY 4.0 (`code/data_platform/sources.json`, card `totalsegmentator_v201`; for v3 the card
  reads "not separately recorded for v3; the RSNAI manifest root (v300 path) states CC BY 4.0").
- **COBRA2026**: CC BY-NC 4.0 (`code/data_platform/sources.json`, card `cobra2026`; also `code/tools/data_manifest.py`
  ROOTS).

For every other path above, this file repeats no terms: `code/data_platform/sources.json` carries a licence field per
source card, and where that card too is silent, the terms are not recorded in the folder. Banks holding VinDr or BUU
pixels were owner-only in their visibility pass until 2026-10-12 (`CLAUDE.md` rule 9); spinesurg-ct-nnunet d9b388d
stopped closing them, visibility jobs 40599886 and 40599867 opened them (section 1), and the copy of
`code/data_platform/plan/publish_visibility.sh` here, the file of 0ab783f since 2026-10-12 (issue #80), does not close
them either.

## 9. Credential files on HOME (`MANIFEST_GRID.md` section 7; by name only)

These appear by name only; they are never read, copied or echoed, and they get no check line. Tokens are read from
files by the jobs that need them, never echoed, never on a command line or in `sbatch --export` (root `CLAUDE.md` rule
10).

`/wsu/home/go/go24/go2432/github`, `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token`,
`/wsu/home/go/go24/go2432/XRSpinoPelvic1K/*.ica`, `/wsu/home/go/go24/go2432/.fluorocap/` (never moves),
`/wsu/home/go/go24/go2432/.hf_org_token`, `/wsu/home/go/go24/go2432/.hf_osc_token`,
`/wsu/home/go/go24/go2432/.zenodo_token`, `/wsu/home/go/go24/go2432/.kaggle/`, `/wsu/home/go/go24/go2432/.netrc`,
`/wsu/home/go/go24/go2432/.ssh/`, `/wsu/home/go/go24/go2432/.google_authenticator`,
`/wsu/home/go/go24/go2432/.gdrive_token`, `/wsu/home/go/go24/go2432/.geo_ftp_pass`,
`/wsu/home/go/go24/go2432/pass_file`, `/wsu/home/go/go24/go2432/private`, `/wsu/home/go/go24/go2432/.certs`,
`/wsu/home/go/go24/go2432/.huggingface`, `/wsu/home/go/go24/go2432/.copilot`, `/wsu/home/go/go24/go2432/.claude`.

## 10. First experiment (`TODO.md` step 1): read the migration's per-batch STATUS files

Jobs 40580669, 40580671 and 40580673 have ended: B04, B07 and B09 were copied, verified, cut over and finalized on
2026-10-11 (Greg's record, issue #49), and on 2026-10-12 B05 and B10 were finalized, and B11 and B13 when the chain
completed at 08:41 EDT (issues #65 and #68; `MANIFEST_GRID.md` section 2). The per-item lines behind those states are not in this
folder: read `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS` for B04, B05, B07, B09,
B10, B11 and B13.

First re-read `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/B02/STATUS` and confirm it still
reads: VERIFIED, 2,417 / 2,417 files, 196,195,055,488 B, 200 sampled (`STATUS.md` M.5).

Gate: 0 items RSYNC_FAILED, VERIFY_FAILED or DST_EXISTS (`TODO.md` step 1, the pre-stated number).

These STATUS files are on HOME, which no student can read (section 1): **Greg supplies the lines.** When they arrive,
record what they say beside this section with the date, and say plainly which batch each job carried only if a log
names it (on 2026-10-08 the batch-to-job assignment was by elimination, `MANIFEST_GRID.md` section 9 unknown 1).

## 11. Not recorded

The per-item STATUS lines of B04, B05, B07, B09, B10, B11 and B13 (none is in this folder; section 10 is how they
arrive); the outcome of visibility job 40599886; whether job 40602927 has run; which
`dp_migrate` job carried which batch (inferred by elimination only); the state of any path after 2026-10-08 beyond the
facts of issue #4 (2026-10-11) and issues #65, #68, #69 and #72 (2026-10-12); the sizes marked "not recorded" above; whether
`/wsu/home/go/go24/go2432/model_night/heads_mixed/` exists; the live state of the HF mirror and Zenodo v11.
