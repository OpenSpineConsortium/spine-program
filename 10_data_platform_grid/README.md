# 10_data_platform_grid

The data platform: 211 imaging sources, the HOME-to-Ceph migration, identity and leakage, the model registry, the
environments and the grid operating rules. Rank 10 of 12 in the triage of `../_plan/PLAN.md`: a support project, not
a hypothesis, on which every other project folder depends.

**Reader.** Student-safe once Greg confirms the reader split (`docs/handoff/OPEN_QUESTIONS.md` A29) and the
withheld contact data (A30); until then Greg-only. Credential names only, never values.

## What it is

Three things live here, each with its record of origin:

1. **The manifest and the migration** (`code/data_platform/`). One card per source (211: 176 upstream releases,
   7 project releases, 23 derived banks, 2 output roots, 3 unsent requests; `docs/handoff/INFRASTRUCTURE.md` section 4),
   the target layout on Ceph (`LAYOUT.md`), the batch procedure (`MIGRATION_PLAN.md`: preflight, rsync and verify,
   cut over with a symlink, smoke checks, README.yaml and index, FINALIZE after Greg looks), the re-acquisition driver
   (`reacquire/`), the holding index (`db/`), the duplicate census (`dedup/`) and the planning checks (`VERIFICATION.md`).
2. **Identity and leakage** (`docs/`, `code/tools/`). The person-level identity specification
   (`docs/PATIENT_IDENTITY_SPEC.md`), the data contract (`docs/DATA_ACCOUNTING.md`), the 99-gap completeness audit
   (`docs/DATA_COMPLETENESS_AUDIT.md`), the two historical split leaks (`docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`,
   `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`), the rule and the checks CHK-1 to CHK-9 (`docs/handoff/LEAKAGE.md`),
   the tools that implement them (`code/tools/patient_keys.py`, `leak_check.py`, `data_ledger.py`, `data_alias.py`,
   `data_lineage.py`, `data_manifest.py`) and their laptop tests, and the SPINEPS instance-id census and repair
   (`results/spineps_ids/`, `code/tools/spineps_ids*.py`).
3. **Grid operations** (`docs/`, `memory/`). The model registry (`docs/MODEL_REGISTRY.md` with its correction), the
   environments (`code/env/`), the record of every job cancelled on 2026-09-27 (`docs/grid_records/`), the one
   read-only pass over both volumes on 2026-10-08 22:20 UTC with the laptop copies of the storage census
   (`docs/grid_read_2026-10-08/`), and the grid notes in `memory/`.

## State on 2026-10-12 (every number from the file named; 2026-10-08 where nothing later is recorded)

| measure | value | file |
|---|---|---|
| HOME used | 520 GB of the 4,295 GB soft limit at the chain's end on 2026-10-12 (1,334 GB earlier that day); 4,050.75 GB of a 4,294.97 GB soft limit (8,589.93 hard), 2,921,043 files of 10,000,000, on 2026-10-08 | Greg, issue #68; read on the grid 2026-10-12 (issue #65); `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "pan_quota" |
| Ceph used | `oschome` 9 of 20 TB on 2026-10-12; 7 TB of 20 TB (39.39 %) on 2026-10-08, `/rs/rs_grp_oschome/go2432/data` alone 5,333.691 GB, 4,579,361 files | issue #65; `grid_ls_2026-10-08.out` "df-ceph"; `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` (job 40580051) |
| finalized | every batch with data on 2026-10-11: B00, B01, B02, B04, B06, B07, B08, B09, B14 (B03 had nothing to move; B12 dropped); on 2026-10-12 B05 (3/3 VERIFY_OK) and B10 (64/64), each cut over and finalized | `MANIFEST_GRID.md` section 2 (Greg's record of 2026-10-11, issue #49; issue #65) |
| the chain's end, 2026-10-12 | complete at 08:41 EDT: every batch with data copied, verified, cut over and finalized, B11 (64/64) and B13 (3/3) included; no refusal; visibility job 40599867 opened the VinDr and BUU banks in `multisource_banks`; job 40599718 deleted the TotalSegmentator v3.0.0 zip (37.4 GB) and the NHANES extracted pickles (159 GB), job 40602927 deletes the v2.0.1 zip (23.58 GB); dedup A14 linked 1,413 files | Greg, issue #68; `MANIFEST_GRID.md` section 2 |
| what the 2026-10-08 STATUS files measured | B00 76/76 files; B02 2,417/2,417 files, 196,195,055,488 B, 200 sampled, 25 build-tree items ABSENT; B06 14/14; B08 2/2; B14 9/9; B01 three metadata files VERIFIED, the two raw trees ABSENT; B03 both items ABSENT | `plan/runs/<B>/STATUS` on the grid, captured in `grid_ls_2026-10-08.out` "STATUS files" |
| student access | every folder under `/rs/rs_grp_oschome/go2432/data/` readable by approved students (2026-10-11); the VinDr and BUU items inside them, owner-only until 2026-10-12, opened by visibility jobs 40599886 and 40599867 after `publish_visibility.sh` was fixed (spinesurg-ct-nnunet d9b388d); `.../ctspinopelvic1k_build_tree/derived/s1v11` opened on 2026-10-12 without the token check (spinesurg-ct-nnunet 0ab783f, visibility job 40602925); one path stays owner-only, `.../ctspinopelvic1k_build_tree/derived/build_archive_private` (its one file is the annotator map, students' personal data); job 40602926 opened `/rs/rs_grp_oschome/go2432/envs/spineps212` and `/rs/rs_grp_oschome/go2432/results` | `DATA.md` section 1; issues #65, #69 and #72 |
| holding index | not built: `/rs/rs_grp_oschome/go2432/data/_index` does not exist (2026-10-08; nothing later recorded) | `grid_ls_2026-10-08.out` "ls RS/data/_index" |
| deletion candidates | 1,590.3 GB (plan) plus, from the duplicate census, 353.7 GB now and 218.3 GB once a condition is met; decisions reserved to Greg | `MIGRATION_PLAN.md` section 8; `code/data_platform/dedup/DEDUP_PLAN.md` "The totals" |
| the contradiction | B01 "cut over" against the TCIA CT Colonography raw DICOM (721 GB) and NIfTI (336 GB) on neither volume, nothing recording their deletion | `docs/handoff/OPEN_QUESTIONS.md` B30; `STATUS.md` here |

## Goal and success criteria

- Every imaging holding of `code/data_platform/plan/layout_map.csv` sits under `/rs/rs_grp_oschome/go2432/data/<source>/`
  with a README.yaml, is VERIFIED by `plan/verify_transfer.py` (counts, sizes, links, hard-link groups, a 200-file
  SHA-256 sample), and is indexed in `/rs/rs_grp_oschome/go2432/data/_index/holding.sqlite` whose per-collection file
  counts equal the census (`MIGRATION_PLAN.md` section 10).
- Every old HOME path is a symlink; every FINALIZE is recorded with its job id; `pan_quota` falls below 90 % of the
  soft limit after B02 and B06 are finalized (`TODO.md` step 4).
- B01 and B03 are resolved: either re-acquired by `reacquire.py` in a job, or a written deletion record names the
  script and date (`TODO.md` step 5).
- The identity tables are backed up to Ceph with recorded SHA-256 before B11 moves them; the content-hash chain
  (`slurm/data_accounting.sh`) has run once on the real corpus (`docs/handoff/LEAKAGE.md` section 7 item 1).
- The two known tool defects are fixed: `tools/xray_dataset_usage.py` (`buu_2000` mislabel, substring keys;
  `OPEN_QUESTIONS.md` F7) and the stale Geneva fixture in `tools/test_leak_check.py` (F17, Greg decides).

## How it relates to the other projects

- `01_carm_level_detection` reads the registry entries, the real-frame banks under `/rs/rs_grp_oschome/go2432/data/realxray`
  and the identity tables; its held-out claims rest on the leakage rules kept here.
- `02_transitional_naming_truth`, `06_transitional_ct_census` and `07_plain_film_level_id` read banks that B10 and B11
  move; `03_ctspinopelvic1k_dataset` reads the v11 working copy that B02 moved (`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`).
- `05_ct_morphometry_parity` and `04_openspinetoolkit` need the v11 labels and the B14 items (`s1v11`, `pitest`, `pdwtest`).
- `11_students_grid_access` owns the access-list gate on `/rs/rs_grp_oschome`; this folder owns which folders are
  world-readable (`plan/publish_visibility.sh`).
- `12_website_pacs_demo` depends on nothing here except the model registry's naming.

## How to read the handoff copies

`docs/handoff/` holds the eight student-readable handoff files whole. Their path prefixes (`ssn:`, `sn:`, `ctsp:`,
`ostk:`, `mem:`, `~`, `$RS`) are defined in `docs/handoff/README.md` section 0 by laptop folder; in this folder read
them as the repositories of `MANIFEST_CODE.md` at the stated commits and as `memory/` here, never as a laptop path.
The Greg-only handoff files (`MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md`,
`working_notes/`) are not copied whole; the sections that bear on this project are extracted with their section ids
under `docs/handoff/extracts/` and folded into `STATUS.md` and `TODO.md`.
