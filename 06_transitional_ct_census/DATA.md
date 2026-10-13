# DATA.md: the grid paths of this folder, reached through Beethoven

This file lists every grid path of `MANIFEST_GRID.md` sections 1 to 4, spelled as the manifest spells it, with its
volume, what it holds, its state and one read-only check line per path. The access facts are Greg's, dated 2026-10-11
(issue #9). Every number below restates `MANIFEST_GRID.md`, which names the file each one comes from (the census of
job 40580051, a STATUS file, the 2026-10-08 read-only pass); where a size or a fact is in no file, this file writes
"not recorded". `MANIFEST_GRID.md` section 5 lists what is known missing or never there.

**How to run a check line.** Every check runs from the Beethoven worker (`../11_students_grid_access`), never python
or `du` on the login node (`CLAUDE.md` rule 9 of this folder). A directory gets `ls -ld <path>`; a file gets
`head -c 200 <file>`. A check line written with `{a,b}` expands in bash and covers each member; the braces carry no
spaces. A check on a path recorded as absent is expected to answer "No such file or directory" — that answer is the
check.

**Volumes.** HOME = `/wsu/home/go/go24/go2432` (Panasas). Ceph = `/rs/rs_grp_oschome/go2432` (CephFS, 20 TB, group
`oschome`). Every path below is spelled in full, so a copy never depends on this line (`MANIFEST_GRID.md` header).

## 1. Access on 2026-10-11 (Greg, issue #9)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- On 2026-10-12 the VinDr and BUU items inside those folders opened too. Until then the plan's `restricted` flag
  still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and
  BUU banks of B10 and B11, `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain folder including
  `multisource_banks`) open them (issue #65).
- One path stays closed (owner-only):
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, whose one file is the
  annotator map, students' personal data rather than a dataset or a token (Greg, issue #69).
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` opened on 2026-10-12 without the token
  check (spinesurg-ct-nnunet 0ab783f; visibility job 40602925, issue #69).
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students. Items still there are moved to
  the Ceph volume by the data-platform plan, whose batch-by-batch state is `../10_data_platform_grid/MANIFEST_GRID.md`
  section 2. Every such item in the tables below is marked **on HOME, not reachable until migrated**; Greg runs those
  check lines until the batches land.
- `/rs/rs_grp_oschome/go2432/ruleclass` and `/rs/rs_grp_oschome/go2432/cns2026_posterior` sit at the Ceph root, not
  under `data/`, and the access facts above do not speak for them: whether a student can read them is not recorded.
  If a check there is refused, Greg runs it (issue #9).

## 2. Through Beethoven

Beethoven is the way a student reaches these paths. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (pages at https://openspineconsortium.com/beethoven/).

A student needs: a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and
Chrome on the invited Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on
`/rs/rs_grp_oschome` (issue #9).

The two access facts again, because they decide what a check line can answer:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the
  volume root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus` and, since 2026-10-12, the VinDr and BUU
  items inside them and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`; one path stays
  closed, `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (the annotator
  map, students' personal data).
- Nothing on `/wsu/home/go/go24/go2432` is readable by students; items still there are marked **on HOME, not
  reachable until migrated** below, and Greg runs the HOME check lines until the data-platform batches move them
  (`../10_data_platform_grid/MANIFEST_GRID.md` section 2).

## 3. The ruleclass census (`MANIFEST_GRID.md` section 1; Ceph, at the volume root, not under `data/`)

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/ruleclass` | Ceph | `CORPUS.md` 30,381 B, `ARM_B.md` 19,613 B, `corpus_counts.json` 20,963 B, `arms/{ts, moller_fast, moller, pelvis}`, `tiers/` (8 entries), `code/` (21 entries, the arm scripts: grid only, in no repository), `logs/` (802), `moller_masks/` (7), `containers/` 7.719 GB; 48.579 GB census, 163,587 files | Ceph-native; grows; `CORPUS.md` says 21,655 CTs against the tiers' 21,622 (OQ B3, unexplained) | `ls -ld /rs/rs_grp_oschome/go2432/ruleclass` |
| `/rs/rs_grp_oschome/go2432/ruleclass/tiers/` | Ceph | `tier1.txt` + `tier1.tsv` (5,094 CTs, 5,075 persons), `tier2.txt` + `tier2.tsv` (12,217), `untiered.tsv` (4,311), `TIERS.md`, `build_tiers.py`; the local copy of `TIERS.md` is `docs/ruleclass/TIERS.md` | `check_paths.sh` stat-tested every path: 0 missing (`docs/ruleclass/TIERS.md` section 0) | `ls -ld /rs/rs_grp_oschome/go2432/ruleclass/tiers/` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md` | Ceph | arm A (TotalSegmentator 2.18.0 `total`) at 2026-09-29 04:23:52: tier 1 done 3,166 + exists 1,927 + failed 1 of 5,094; tier 2 done 10,398 + exists 968 + failed 3 + pending 848 of 12,217 | read in the 2026-10-08 pass; the first experiment (section 8) re-reads it | `head -c 200 /rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/_timing/DECISION.json` | Ceph | 621 B, 2026-09-29 08:21: `mode tta`, `n_timing 0`, `tier2_go false`, "tier 2 ready, NOT submitted: no projection"; beside it `SUMMARY.md` 429 B, `agree_timing20.tsv` 3,569 B, `census.tsv` 2,989,732 B, `renders/` (20) | the gate file was written from zero timing CTs; the production array never ran (`TODO.md` step 3) | `head -c 200 /rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/_timing/DECISION.json` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/<collection>` | Ceph | per-collection folders (abdomenatlas3_mini, amos22, aortaseg60, barts_crl, cobra, ctsp, ctspine1k, idc, kidney_thoraxabdomen, ribfrac, tcia_fdg_pet_ct_lesions, ts, verse, waw_tace) plus `_agree`, `_model`, `_work` | contents not recorded (`TODO.md` step 1) | `ls -ld /rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/{abdomenatlas3_mini,amos22,aortaseg60,barts_crl,cobra,ctsp,ctspine1k,idc,kidney_thoraxabdomen,ribfrac,tcia_fdg_pet_ct_lesions,ts,verse,waw_tace,_agree,_model,_work}` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/moller_fast` | Ceph | arm B Moller rib masks, fast pass, 23 collection folders + `JOBS_ACCEL.txt`, `_claims_measure`, `_claims_predict` | fast pass was 1,801 of 5,094 tier-1 CTs at 17:00 on 2026-09-27 (`STATUS.md` D.20); later counts not recorded | `ls -ld /rs/rs_grp_oschome/go2432/ruleclass/arms/moller_fast` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/moller` | Ceph | arm B full configuration (20-25x slower than the fast pass), 15 entries | not recorded as finished | `ls -ld /rs/rs_grp_oschome/go2432/ruleclass/arms/moller` |
| `/rs/rs_grp_oschome/go2432/review_tree` | Ceph | the two-stage review tree the code writes to | **does not exist**; never built; `code/transitional_review/` untracked; PREREG unsigned | `ls -ld /rs/rs_grp_oschome/go2432/review_tree` (expect: no such file — that answer is the check) |
| `/rs/rs_grp_oschome/go2432/cns2026_posterior` | Ceph | three sbatch and two python files of 2026-09-26, the CNS 2026 posterior-element scripts; not in a repository as far as recorded | Ceph-native; 5 files | `ls -ld /rs/rs_grp_oschome/go2432/cns2026_posterior` |

## 4. The harvest and the acquisitions (`MANIFEST_GRID.md` section 2; Ceph, under `data/`, readable by approved students)

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest` | Ceph | 24 entries: `acquisition/`, `other_ct/`, `verse/`, `ctsp/`, `totalsegmentator/`, `validation_ts/`, `cobra/`, and one screen folder per fetched collection (`panorama/` holds `calls/`, `rows.csv`, `registry_rows.csv`, `gate*.csv`, `SUMMARY.md`, `review/`); 325.817 GB census, 1,063,032 files | Ceph-native; the two-labeller screens per collection; PANORAMA's row counts not read (OQ B2) | `ls -ld /rs/rs_grp_oschome/go2432/data/anomaly_harvest` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition` | Ceph | `jobs.txt`, logs, manifests, `alias_pairs.csv`, `alias_pairs_all.csv` (1,186 near-duplicate candidates) | Ceph-native; the laptop copies of the plan, census, ranking and manifests are `results/transitional_registry/acquisition/` | `ls -ld /rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` | Ceph | the RSNA 2022 cervical census headers; 2,022 study directories against 2,019 train studies (OQ B25) | Ceph-native | `head -c 200 /rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` |
| `/rs/rs_grp_oschome/go2432/data/idc` | Ceph | 39 IDC tier-1 collections, 3,600 series, 3,499 usable CTs; 706.083 GB census | Ceph-native; `fetch/verified.jsonl` per collection (not read); archives deleted after unpack | `ls -ld /rs/rs_grp_oschome/go2432/data/idc` |
| `/rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini` | Ceph | AbdomenAtlas 3.0 Mini, 7,649 usable CTs of 9,262; 570.557 GB | Ceph-native; matched its prediction (7,835 predicted) | `ls -ld /rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini` |
| `/rs/rs_grp_oschome/go2432/data/tcia_fdg_pet_ct_lesions` | Ceph | FDG-PET-CT-Lesions, 900 CTs; 393.872 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/tcia_fdg_pet_ct_lesions` |
| `/rs/rs_grp_oschome/go2432/data/panorama` | Ceph | PANORAMA, 2,024 CTs; 194.439 GB | Ceph-native; screen incomplete (1,114 pending in the tiers); the only collection whose census counts were not one high | `ls -ld /rs/rs_grp_oschome/go2432/data/panorama` |
| `/rs/rs_grp_oschome/go2432/data/ctspine1k` | Ceph | the Ceph copy of CTSpine1K (`raw_data/`, `metadata/`, `hf_listing.json` 618,236 B, `fetch_status.json`); 782 COLONOG volumes are CTSpinoPelvic1K people and were folded in the tiers; 162.350 GB | Ceph-native; sha-verified 2026-09-23; HOME copy ABSENT (B03) | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspine1k` |
| `/rs/rs_grp_oschome/go2432/data/amos22` | Ceph | AMOS22, 723 CTs kept of 2,364 (1,564 refused as thicker than 3 mm; 67 duplicates); 102.615 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/amos22` |
| `/rs/rs_grp_oschome/go2432/data/pengwin2026` | Ceph | PENGWIN 2026, 340 CTs (308 after folding; 32 folded onto CTPelvic1K clinic); 83.499 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/pengwin2026` |
| `/rs/rs_grp_oschome/go2432/data/ribfrac` | Ceph | RibFrac 660 chest CTs (`images/`) plus `raw/ribs` from HOME (B08, VERIFIED 89 files 78,699,138,633 B); 78.200 GB | B08 cut over, VERIFIED; registry T13 4 single-labeller, L6 1 morphology-only | `ls -ld /rs/rs_grp_oschome/go2432/data/ribfrac` |
| `/rs/rs_grp_oschome/go2432/data/kidney_thoraxabdomen` | Ceph | 215 CTs; 75.938 GB | Ceph-native; 176 tier-2 arm A CTs pending | `ls -ld /rs/rs_grp_oschome/go2432/data/kidney_thoraxabdomen` |
| `/rs/rs_grp_oschome/go2432/data/nlst_pilot` | Ceph | NLST pilot 500 CTs; 73.544 GB | Ceph-native; the T13 9.3 % that fell to 1.4 % (`STATUS.md` D.12); 484 tier-2 arm A CTs pending | `ls -ld /rs/rs_grp_oschome/go2432/data/nlst_pilot` |
| `/rs/rs_grp_oschome/go2432/data/waw_tace` | Ceph | 228 CTs; 47.151 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/waw_tace` |
| `/rs/rs_grp_oschome/go2432/data/curvas` | Ceph | 70 of 90 CTs (`training_set.zip` unresolved); 29.994 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/curvas` |
| `/rs/rs_grp_oschome/go2432/data/deep_psma` | Ceph | 53 CTs; 24.253 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/deep_psma` |
| `/rs/rs_grp_oschome/go2432/data/quadra_hc` | Ceph | 48 CTs; 20.413 GB | Ceph-native; 4 tier-2 arm A CTs pending | `ls -ld /rs/rs_grp_oschome/go2432/data/quadra_hc` |
| `/rs/rs_grp_oschome/go2432/data/barts_crl` | Ceph | 212 CTs; 20.313 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/barts_crl` |
| `/rs/rs_grp_oschome/go2432/data/curvas_pdacvi` | Ceph | 101 CTs; 16.879 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/curvas_pdacvi` |
| `/rs/rs_grp_oschome/go2432/data/aortaseg60` | Ceph | 55 CTs; 15.929 GB | Ceph-native; 2 tier-2 arm A CTs pending | `ls -ld /rs/rs_grp_oschome/go2432/data/aortaseg60` |
| `/rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` | Ceph | CTPelvic1K datasets 6-7 (172 CTs); 14.832 GB | Ceph-native; CTPelvic1K datasets 1-5 are on neither volume (B03 row 002 ABSENT): re-download in a job if needed | `ls -ld /rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` |
| `/rs/rs_grp_oschome/go2432/data/csi2014` | Ceph | CSI 2014, 20 CTs; 6.641 GB | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/csi2014` |
| `/rs/rs_grp_oschome/go2432/data/spineps` | Ceph | SPINEPS harvest masks; 8.834 GB census | Ceph-native; masks before commit 147428d carry raw ids (section 7 below; `memory/spineps-ids-can-be-scrambled.md`) | `ls -ld /rs/rs_grp_oschome/go2432/data/spineps` |
| `/rs/rs_grp_oschome/go2432/data/validation_ts` | Ceph | the 70 externally labelled TotalSegmentator CTs as links into `~/data/TotalSegmentator`; 0 (links) | Ceph-native, but the links point into `~/data/TotalSegmentator` on HOME (`MANIFEST_GRID.md` section 4); B07 cut that tree over to Ceph and was finalized on 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md` section 2); whether the links now resolve for a student is not recorded | `ls -ld /rs/rs_grp_oschome/go2432/data/validation_ts` |
| `/rs/rs_grp_oschome/go2432/data/rare_class` | Ceph | rare-class renders (MAXIMIZE); 5.797 GB census | Ceph-native (`STATUS.md` D.10) | `ls -ld /rs/rs_grp_oschome/go2432/data/rare_class` |
| `/rs/rs_grp_oschome/go2432/data/d815_repair` | Ceph | the Dataset815 flag repair of 2026-09-23; 0.001 GB | Ceph-native (`TODO.md` step 11) | `ls -ld /rs/rs_grp_oschome/go2432/data/d815_repair` |

## 5. The VerSeFusion line (`MANIFEST_GRID.md` section 3)

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` | Ceph | VerSe 19/20 raw, unified, canonical, corrected, tables, HF staging; the raw masks under `unified/scan-*/` (id 25 = L6, id 28 = T13); 194,191,642,435 B STATUS (6,951 files) | B06 cut over, VERIFIED (14/14); `TODO.md` step 5 counts ids here, never in `vf_813` | `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813` | Ceph | the Dataset815 input conversion (C1-T9 sent to ignore); 49,427,512,778 B STATUS (1,130 files) | B06 cut over, VERIFIED; never for whole-spine work (`MEMORY.md`) | `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813_probe` | Ceph | unknown probe output of 2026-09-12; 139,428,370 B STATUS (4 files) | B06 cut over, VERIFIED; role not recorded | `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813_probe` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/verse_drr` | Ceph | VerSe renders; holds 13 `glgl*` byte twins; 477,053,118 B (1,492 files) | B06 cut over, VERIFIED; `STATUS.md` D.25; dedup A04 removal_preferred | `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/derived/verse_drr` |
| `/wsu/home/go/go24/go2432/VerSeFusion` | HOME | the VerSeFusion pipeline checkout (`.git`); `data` is a symlink to `/rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` since 2026-10-08 10:39; `data.pre-ceph` (139 GB) was present on 2026-10-08 and went with B06's FINALIZE of 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md` section 2); checkout small | B06 cut over and finalized; **on HOME, not reachable until migrated** (the data itself is readable at the Ceph target above) | `ls -ld /wsu/home/go/go24/go2432/VerSeFusion` (Greg runs it) |
| `/wsu/home/go/go24/go2432/VerseFusion` (file, 24,769 B) and `/wsu/home/go/go24/go2432/VerSeFusion.tar.gz` | HOME | unknown; contents not recorded | **on HOME, not reachable until migrated** | `head -c 200 /wsu/home/go/go24/go2432/VerseFusion; head -c 200 /wsu/home/go/go24/go2432/VerSeFusion.tar.gz` (Greg runs it) |

## 6. Labellers, weights and benches (`MANIFEST_GRID.md` section 4; all on HOME)

Everything in this table sits on HOME, which no student can read (section 1); each item a batch is moving is marked
**on HOME, not reachable until migrated**. Greg runs these check lines until the batches land. Where no batch is
named, none is recorded.

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/bench_ts` | HOME | SPINEPS+VERIDAH over 1,228 TS v2 + 374 VerSe CTs (`cases.csv`, `spineps/native/`); 1.511 GB census; 31 "relabelled" masks are links back to raw masks (`docs/handoff/RECIPES.md` section 3.5) | B11 not started on 2026-10-08; B11's state since is `../10_data_platform_grid/MANIFEST_GRID.md` section 2; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/bench_ts` |
| `/wsu/home/go/go24/go2432/totalseg_weights` | HOME | TotalSegmentator weights (labeller B); not sized | on HOME, not reachable until migrated; batch not recorded | `ls -ld /wsu/home/go/go24/go2432/totalseg_weights` |
| `/wsu/home/go/go24/go2432/spineps_models` | HOME | SPINEPS model weights (labeller A); not sized | on HOME, not reachable until migrated; batch not recorded | `ls -ld /wsu/home/go/go24/go2432/spineps_models` |
| `/wsu/home/go/go24/go2432/rib-segmentation` | HOME | the Moller rib nnU-Net checkout (Zenodo 14864106, folds 0-2; arm B); not sized | on HOME, not reachable until migrated; batch not recorded | `ls -ld /wsu/home/go/go24/go2432/rib-segmentation` |
| `/wsu/home/go/go24/go2432/model_night/anomaly_manifest` | HOME | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (2026-09-17; `STATUS.md` D.1); not sized | on HOME, not reachable until migrated; batch not recorded | `ls -ld /wsu/home/go/go24/go2432/model_night/anomaly_manifest` |
| `/wsu/home/go/go24/go2432/lstv_flag` | HOME | `LEARNING_CURVE.md`, `LSTV_FLAG_RESULTS.md`, `ANOMALY_INVENTORY.md`, `_lstv_phenotypes.csv`, `models/` (registered flag models), the master flag table `lstv_flag_labels_v2.csv` (not seen in the `head -30` of the pass); not sized | B11, whose state is `../10_data_platform_grid/MANIFEST_GRID.md` section 2; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/lstv_flag` |
| `/wsu/home/go/go24/go2432/data/TotalSegmentator` (the v2 release, 1,228 CTs), `/wsu/home/go/go24/go2432/data/TotalSegmentator_v3` (1,939) | HOME | the two TS releases; 82.0 / 89.8 GB du (B07.tsv); `/rs/rs_grp_oschome/go2432/data/validation_ts/raw/*` links point into the v2 tree | B07 copying on 2026-10-08 (no STATUS yet); on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/data/{TotalSegmentator,TotalSegmentator_v3}` |
| `/wsu/home/go/go24/go2432/lstv-detector` | HOME | the MRI lstv-detector tree; its results survive only in `results/aaca_lstv_mri/` | **ABSENT** on 2026-10-08 | `ls -ld /wsu/home/go/go24/go2432/lstv-detector` (expect: no such file — that answer is the check; Greg runs it) |
| `/wsu/home/go/go24/go2432/split_final.json`, `split_leak_report.json` | HOME | the frozen G3 person split (apply 2026-09-23 20:18:48, seed 0, job 40426793); leak audit PASS; never rerun in place (`docs/handoff/RECIPES.md` section 3.1 step 4); small | B11, whose state is `../10_data_platform_grid/MANIFEST_GRID.md` section 2; on HOME, not reachable until migrated | `head -c 200 /wsu/home/go/go24/go2432/{split_final.json,split_leak_report.json}` (Greg runs it) |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | HOME | the grid checkout, behind the laptop (4e3fe93 against 097933a) and unable to fetch; ship by `git archive \| ssh tar` (`docs/handoff/RECIPES.md` section 0) | on HOME, not reachable by students; the repository itself is private (root `CLAUDE.md` rule 8) | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet` |

## 7. Terms, where the folder records them

- **TotalSegmentator**: CC BY 4.0 (issue #9; `../10_data_platform_grid/DATA.md` section 8, card
  `totalsegmentator_v201` in that folder's `code/data_platform/sources.json`).
- **COBRA2026** (the `cobra` stream of the registry and of `anomaly_harvest/cobra`): CC BY-NC 4.0, and its 175
  validation and test cases (validation 52 and test 123) are embargoed to 2032-03-01, so "COBRA2026" here means the
  692-case public training split (issue #9; `../_plan/PLAN.md` section 3;
  `../10_data_platform_grid/docs/DATA_COMPLETENESS_AUDIT.md`).
- **The seven gated collections** of `TODO.md` step 13 (Stanford Merlin, RSNA RATIC, CT-RATE, INSPECT, CADS, RSPECT,
  MAGIC-CT): no agreement is signed and they are not on the grid; until one is, no expected number from them enters
  any table.
- For every other path above, the terms are **not recorded in the folder**.
- **SPINEPS masks harvested before commit 147428d carry raw ids 1..N**, not vertebra names: never name by mask id;
  name through the centroid file (`tools/spineps_ids.relabel_by_ctd`; `memory/spineps-ids-can-be-scrambled.md`,
  `docs/ruleclass/TIERS.md` sections 3-4).

## 8. First experiment (`TODO.md` step 1): one read-only job re-reads the ruleclass state

One read-only `sbatch -D <dir>` job on `reqp --qos=requeue` (nothing on the login node; `CLAUDE.md` rule 9), which
answers open questions B1 to B5:

- Re-read `/rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md`. Expected, as of 2026-09-29 04:23:52 (`STATUS.md`
  G.1): tier 1 5,094 = 3,166 done + 1,927 exists + 1 failed; tier 2 12,217 = 10,398 done + 968 exists + 3 failed +
  848 pending. A different answer is news: record it with the job id, never silently.
- Then the 33-CT gap: `CORPUS.md` says 21,655 CTs against the `tiers/` 21,622 (tier 1 5,094 + tier 2 12,217 +
  untiered 4,311). Explain the difference (OQ B3).
- The rest of `TODO.md` step 1: read `arms/moller_fast/JOBS_ACCEL.txt` and `_claims_measure` / `_claims_predict`
  (OQ B1 for arm B), list `arms/pelvis/<collection>`, and count the rows of PANORAMA's `rows.csv` and
  `registry_rows.csv` (OQ B2), toward the cause of the census table's one-high counts (OQ B5).
- Gate (`TODO.md` step 1): the counts written into `STATUS.md` section 3 with the job id;
  `docs/CENSUS_TABLE_2026-09-25.md` corrected before anything copies it again (OQ F13).
- `ruleclass` is not under `data/` (section 1): if it is unreadable to the student, Greg runs the job.

## 9. Not recorded

Whether a student can read `/rs/rs_grp_oschome/go2432/ruleclass` and `/rs/rs_grp_oschome/go2432/cns2026_posterior`
(the access facts of 2026-10-11 cover `data/` only; section 1); the state of any grid path after the dates the
manifest records (the read-only pass of 2026-10-08, the arm A STATUS of 2026-09-29) beyond the access facts of
2026-10-11 and 2026-10-12; what arm B finished after 2026-09-27 and whether the Moller full configuration finished;
the contents of `arms/pelvis/<collection>` and PANORAMA's row counts (the first experiment reads them); the cause of
the 33-CT gap and of the census table's one-high counts (OQ B3, B5); the sizes marked "not sized" in section 6; the
STATUS lines of the batches finalized since 2026-10-08 (their state is `../10_data_platform_grid/MANIFEST_GRID.md`
section 2; no STATUS for them is in this folder); the outcome of visibility jobs 40599886 and 40599867; the terms of
every path section 7 does not name.
