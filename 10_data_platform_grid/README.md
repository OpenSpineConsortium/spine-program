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

## State on 2026-10-08 (every number from the file named)

| measure | value | file |
|---|---|---|
| HOME used | 4,050.75 GB of a 4,294.97 GB soft limit (8,589.93 hard); 2,921,043 files of 10,000,000 | `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "pan_quota" |
| Ceph used | 7 TB of 20 TB (39.39 %); `/rs/rs_grp_oschome/go2432/data` alone 5,333.691 GB, 4,579,361 files | same file "df-ceph"; `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` (job 40580051) |
| batches VERIFIED and cut over | B00 (76/76 files), B02 (2,417/2,417 files, 196,195,055,488 B, 200 sampled; 25 build-tree items ABSENT), B06 (14/14), B08 (2/2), B14 (9/9); B01 three metadata files VERIFIED, the two raw trees ABSENT; B03 both items ABSENT | `plan/runs/<B>/STATUS` on the grid, captured in `grid_ls_2026-10-08.out` "STATUS files" |
| batches copying at 22:20 UTC | B04, B07, B09: jobs 40580669, 40580671, 40580673 RUNNING 12:28:51 of 4-00:00:00 on `reqp` (batch assignment inferred by elimination, not read from the logs) | same file "squeue" |
| not started | B05 (after B04), B10 (64 items), B11 (64 items incl. the identity tables); B12 dropped; B13 (627.4 GB of results) awaits Greg | `code/data_platform/MIGRATION_PLAN.md` section 5 |
| finalized | none: every cut-over path keeps its `.pre-ceph` twin; `pan_quota` unchanged from 2026-10-07 | `grid_ls_2026-10-08.out` "ls HOME", "ls ~/data" |
| holding index | not built: `/rs/rs_grp_oschome/go2432/data/_index` does not exist | same file "ls RS/data/_index" |
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
