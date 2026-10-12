# STATUS.md: the results in hand on 2026-10-08

Every number names its file. Status words and rigor marks follow `docs/handoff/RESULTS_CATALOG.md` "How to read a row":
CURRENT, HELD-OUT, SUPERSEDED, DISPUTED, RECORD ONLY, NOT RECORDED, OPEN; [AUTO-TRUTH], [DERIVED], [LEAK], [WRONG-BANK].
"RC" = `docs/handoff/RESULTS_CATALOG.md`; "GRIDLS" = `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`; "OQ" =
`docs/handoff/OPEN_QUESTIONS.md`; "MP" = `code/data_platform/MIGRATION_PLAN.md`; "DDP" = `code/data_platform/dedup/DEDUP_PLAN.md`.

## 1. The migration (RECORD; verified by the jobs named)

| id | result | file | status |
|---|---|---|---|
| M.1 | HOME 4,050.75 GB of a 4,294.97 GB soft limit (8,589.93 hard); 2,921,043 files of 10,000,000; unchanged from 2026-10-07 because no FINALIZE has run | GRIDLS "pan_quota"; `code/data_platform/DATA_MANIFEST.md` section 1 | SUPERSEDED by M.15 (HOME 1,334 GB on 2026-10-12) |
| M.2 | Ceph 7 TB of 20 TB (39.39 %); `/rs/rs_grp_oschome/go2432/data` 5,333.691 GB, 4,579,361 files | GRIDLS "df-ceph"; `docs/grid_read_2026-10-08/census/census_merged_partial.tsv` (job 40580051) | CURRENT |
| M.3 | B00 VERIFIED: 76/76 files, 5,272,150,583 B, 76 sampled; cut over | `plan/runs/B00/STATUS` (GRIDLS "STATUS files") | CURRENT; verified by `verify_transfer.py` |
| M.4 | B01: items 001 (raw DICOM, 721 GB) and 002 (NIfTI, 336 GB) ABSENT; 003-005 VERIFIED (`patient_db.json` 9,909,285 B, `patient_db.pkl` 2,409,446 B, `patient_db_summary.txt` 663 B); so "B01 cut over" means the three metadata files only; the raw trees are on neither volume and nothing records what removed them | `plan/runs/B01/STATUS`; GRIDLS "ls RS/data/tcia_ct_colonography" (`meta/` only); `memory/data-platform-migration-2026-10.md` | CURRENT; **answers OQ B30's first half**; the deletion itself NOT RECORDED |
| M.5 | B02 VERIFIED: the v11 working copy 2,417/2,417 files, 196,195,055,488 B, 200 sampled, hard-link group, irreplaceable; `0816_label_v4.nii.gz` 1,106,588 B; `build_archive` 13 files 6,236,530,062 B; `build_archive_private` 1 file 592 B; `build_archive_stage` 2,474 files 3,035,170,658 B; 25 build-tree items ABSENT (rows 002-024, 026, 030); cut over | `plan/runs/B02/STATUS` | CURRENT; the ABSENT rows settle `DATA_MANIFEST.md` section 10 family-A unknowns 3-4 and family-E unknown 3 (the reclaim phases ran) |
| M.6 | B03: both items ABSENT; CTSpine1K stands on Ceph (162.350 GB census; sha256 per file 2026-09-23); CTPelvic1K datasets 1-5 on neither volume (only `ctpelvic1k_clinic`, 14.832 GB) | `plan/runs/B03/STATUS`; GRIDLS "ls RS/data/ctspine1k ctpelvic1k rsna ribfrac"; census | CURRENT; CTPelvic1K re-download OPEN |
| M.7 | B06 VERIFIED 14/14 with measured sizes (VerSeFusion/data 6,951 files 194,191,642,435 B; implant_verse 2,254 files 159,368,901,079 B; vf_813 1,130 files 49,427,512,778 B; the eleven render banks and probes as listed in `MANIFEST_GRID.md` section 2); cut over; visibility pass finished 12:35 | `plan/runs/B06/STATUS`; `memory/data-platform-migration-2026-10.md` | CURRENT; the measured 194.2 GB supersedes the 138.1 GB du of 2026-09-01 |
| M.8 | B08 VERIFIED: `rsna_cspine` 4 files 203,321,991,870 B; `ribs` 89 files 78,699,138,633 B; cut over | `plan/runs/B08/STATUS` | CURRENT |
| M.9 | B14 VERIFIED 9/9: `qc.tar.gz` 196,147,947 B; `dis_renders` 5 files 10,869,856 B; `pitest` 10 files 13,899,387 B; `pdwtest` 2 files 2,710,749 B; `ostk_level_morphometry.csv` 302,994 B; `pdw_why.py` 1,761 B; `pi_ostk2.csv` 662 B; `s1v11` 835 files 1,189,924,200 B (restricted, irreplaceable); `spondy_landmark` 1,416 files 89,020,337 B; cut over | `plan/runs/B14/STATUS` | CURRENT |
| M.10 | B04, B07, B09 copying: jobs 40580669, 40580671, 40580673 RUNNING 12:28:51 of 4-00:00:00 on `reqp`; no STATUS yet; `_staging/B04` has 2 entries; `totalsegmentator_v300/raw` and `fluorocap/raw` exist with 1 entry each | GRIDLS "squeue", "ls RS/data B04 B05 B07 B09 B10 B11 targets" | SUPERSEDED by M.15 (B04, B07, B09 finalized 2026-10-11); the batch-to-job assignment is by elimination [DERIVED] |
| M.11 | B05, B10, B11 not started; B12 dropped (`nnunet/raw` stays on HOME); B13 not run (`/rs/rs_grp_oschome/go2432/results` absent); the holding index not built (`/rs/rs_grp_oschome/go2432/data/_index` absent); nothing finalized (`.pre-ceph` twins everywhere) | GRIDLS; MP section 5 | SUPERSEDED by M.15; B12 dropped and the index not built (as of 2026-10-08) still stand |
| M.12 | the plan's totals: 219 items to move, 3,256.6 GB sized, 157 unsized, 1,590.3 GB deletion candidates; B13 627.4 GB | MP section 5 (generated 2026-10-08) | CURRENT as a plan; the sizes are stale in both directions (MP section 0); the census decides |
| M.13 | the census: HOME `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` 7.7 GB (the 1.9 TB September tree reclaimed 2026-09-07); `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K` 196 GB the only HOME copy of the 802 CTs; `/wsu/home/go/go24/go2432/data` 624 GB; VerSeFusion 195 GB; `/wsu/home/go/go24/go2432/ablate` 202 GB; Ceph 7.7 TB apparent of which u251 2.2 TB is not imaging | `docs/grid_read_2026-10-08/census/census.json` (job 40578909), `ceph/census.tsv` (40580051, 1,590 rows), `home_after_F/census.tsv` (40580052, partial, 629 rows), `census_merged_partial.tsv` (2,427 rows) | CURRENT; the HOME census after `films_ap_drr` alphabetically was still running |
| M.14 | the 2026-10-08 first-pass figure "4,050 - 3,189 = 861 GB" for HOME after the move | MP section 10 | SUPERSEDED (wrong: part of the sized move total was no longer on HOME); rewrite from the census |
| M.15 | 2026-10-12: every batch with data was finalized on 2026-10-11 (B00, B01, B02, B04, B06, B07, B08, B09, B14); B05 3/3 VERIFY_OK, cut over, finalized; B10 64/64, cut over, finalized; B11 64/64, cut over, finalize running at 03:30 EDT; B13 two items verified (`nnunet/results` 299 GB, `ablate` 202 GB), cut over, finalize running; HOME 1,334 GB of the 4,295 GB soft limit; Ceph `oschome` 9 of 20 TB. The VinDr and BUU items inside the folders opened on 2026-10-11 were still owner-only (`drwx--S---`) through the plan's `restricted` flag; `publish_visibility.sh` was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs 40599886 (the B04, B05, B10, B14 folders) and 40599867 (after B13's finalize, every chain folder including `multisource_banks`) open them; two paths stay owner-only, `ctspinopelvic1k_build_tree/derived/build_archive_private` and `ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its Zenodo upload scripts for a token) | read on the grid 2026-10-12 (issue #65); Greg's record of 2026-10-11 (issue #49); `MANIFEST_GRID.md` section 2 | CURRENT (2026-10-12); no STATUS file of B04, B05, B07, B09, B10, B11 or B13 is in this folder; the outcome of the two visibility jobs and the state of `bench` (B13) are not recorded |

## 2. The duplicate census (hash jobs 40581845, 40581924)

| id | result | file | status |
|---|---|---|---|
| D.1 | 46 duplicate groups; at most 95.8 GB linkable byte-identical (37.3 GB on recorded hashes, 38.6 GB likely, 19.9 GB possible, plus 0 to 56.1 GB in A03); deletion candidates for Greg 353.7 GB now and 218.3 GB once a condition is met (VerSe `canonical/` 67.0, `labels_v10` 1.1, the scaling subset banks 129.2, `allspine_v8` 5.5, `C-ArmLSpine.zip` 15.6); 1,631 concrete alias rows over 830 subjects (`index_aliases.csv` holds 1,678 data rows: 1,631 `concrete`, 12 `rule`, 35 `pending_table` by its `status` column, counted 2026-10-08) | DDP "The totals" (the revised plan after its section 7 review); `code/data_platform/dedup/INDEX_ALIASES.md`; `index_aliases.csv` | CURRENT; the memory note's 97.7 / 482.9 / 1,659 are the first plan's figures (section 9) |
| D.2 | A01: VerSe'19 = VerSe'20 for 185 files, 8.42 GB (identical; linkable after FINALIZE) | `code/data_platform/dedup/HASH_RESULTS.md`; `hash_results/A01.json` | CURRENT |
| D.3 | A02: `canonical/` has 224 links and no byte copy; A03: the HF staging trees are not hard links (27 same inode; 2,753 files with no byte twin; 56 GB of distinct bytes: a deletion candidate, not a link) | same | CURRENT |
| D.4 | A07: the s1v11 build labels equal the release labels, 802 files, 1.19 GB (hold `greg_review`); A09: the 0533 repair equals the release; A08/A10: `ctsp_april` shares no CT bytes with the release | same | CURRENT |
| D.5 | A04 first came back "missing" because the grid's bash 4.2.46 keeps the quotes of a quoted replacement in `${var/pat/"$new"}`; rerun as job 40581924: 357 renders identical; the 13 `ann/glgl*.json` differ only by the embedded name (hold `removal_preferred`) | `dedup/HASH_RESULTS.md`; `memory/grid-bash-4-2-quoting.md` | CURRENT |
| D.6 | nothing linked yet: `dedup/applied/` holds only `.gitkeep` on both the laptop and the grid | GRIDLS "dedup on grid" | CURRENT |

## 3. Data integrity numbers printed in the SchwingNet supplement (RC A19; all CURRENT)

| id | claim | file |
|---|---|---|
| A19.1 | 99 data gaps = 31 criterion + 28 bug + 21 unfinished + 4 budget + 15 unknown | `docs/DATA_COMPLETENESS_AUDIT.md` "Every gap, worst first" |
| A19.2 | CHK-9 over 563 quoted numbers: 323 held out, 81 seen, 58 unreadable lineage, 101 no checkpoint (job 40429833); after the v9 closure 380 held out, 81 seen, 1 unresolved, 101 not applicable | `sn:results/eval_gate/EVAL_LEAKS.md`; `sn:results/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md` (in `01_carm_level_detection`) |
| A19.3 | 306 checkpoints in the lineage census, 133 with an unreadable link | `sn:results/eval_gate/LINEAGE.md` (01) |
| A19.4 | 57 quoted numbers traced to the deleted `allspine_v2_r1` bank, re-run on v9 | `MANUSCRIPT_CORRECTIONS.md` section 7.0 (01) |
| A19.5 | NHANES II in the banks twice; 48 of 54 validation patients twinned in training | `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `code/tools/leak_check.py` docstring |
| A19.6 | 2,437 harvested SPINEPS masks with raw ids 1..N; 3,490 relabelled [DERIVED: the sum of `actions.relabelled` over the six `results/spineps_ids/repair/relabel_summary_{bench,bench_ts,cobra_v1,deepfluoro,geneva,tsv3}.json`, 796 + 1,452 + 144 + 6 + 1 + 1,091; no file prints the total] | `results/spineps_ids/CENSUS.md` line 27 (the 2,437); the six `relabel_summary_*.json` (the 3,490); RC A19.6 cites `IMPACT.md` section 0 and `REPAIRS.md`, which do not print it |
| A19.7 | 69 quoted detector numbers re-scored in both box conventions | `sn:results/bodybox_rescore/RESCORE.md` (job 40419582; 01) |
| A19.8 | Mendeley: 500 of 584 films re-encode BUU-LSPINE | `code/tools/excluded_sources.py` REASONS |
| A19.9 | CTSpinoPelvic1K 0533 truncated download 17,301,504 B rebuilt to 250,067,995 B | `sn:results/repairs/ct0533_CHECK.md` (01); `memory/grid-ct-0533-truncated.md`; `code/tools/ctsp0533_*.py` |
| A19.10 | COBRA2026 frames counted up to four times in one arm: 5,013 duplicate entries | `sn:results/repairs/cobra-dup-leak_CHECK.md` (job 40416578; 01) |

## 4. Corpus totals and the disputed Table 1 (RC A18)

| id | claim | file | status |
|---|---|---|---|
| A18.2 | corpus totals 4,093 renders, 9,108 level-annotated films, 4,276 real exposures (778 C-arm) | `sn:tables/tab_corpus.sources.md` (01) | **DISPUTED**: the 4,093 counts `ts_drr` 1,170 and `ts_drr_v3` 1,735, which the v9 build never reads, and omits `physics_drr` 7,045 and `physics_rare` 1,482, which it does; recompute from `slurm/allspine_v9_bank.sh` (OQ F6) |
| A18.4 | 7,045 physics-styled renders in Table 1 footnote a vs 7,048 items in that root | `sn:supplement.tex` "Corpus census"; `code/data_platform/sources.json` card `physics_drr` holds both counts (OQ G1) | recorded unexplained |
| A18.5 | Table 1 says TotalSegmentator v2/v3 renders are in the level bank; the v9 build script has no `ts_drr` root (TS enters only as 1,831 `physics_drr` renders) | `docs/DATA_COMPLETENESS_AUDIT.md` lines 66, 511 | **DISPUTED**: trust the build script |

## 5. Identity and leakage findings (LEAKAGE sections 4-5; PATIENT_IDENTITY_SPEC; memory notes)

| id | finding | file | status |
|---|---|---|---|
| L.1 | Historical leak 1: NHANES II entered the banks twice (`films_drr` and `nhanes_drr`), split independently; 48 of 54 validation patients twinned in training on v6 and v7; whether v5 carried them is not recorded (OQ F23) | `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `memory/nhanes-double-inclusion.md` | CURRENT (fixed by patient keys) |
| L.2 | Historical leak 2: CTSpinoPelvic1K under two names (the TCIA token and the release id); `anchor_drr`'s own split put 301 of 801 CTSP people on both sides | `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`; `memory/split-leak-cross-naming.md`; `docs/DATA_COMPLETENESS_AUDIT.md` | CURRENT (fixed by patient keys); every number on `anchor_drr` is [LEAK] |
| L.3 | `vindrps`: a 77.8 % validation leak | `docs/handoff/LEAKAGE.md` section 5; `extracts/RESEARCH_DIRECTIONS_sections.md` 5.1 | CURRENT; never quote `vindrps` |
| L.4 | Prone/supine double acquisition of one person in CTSP ruled out on disk; TotalSegmentator v2 to v3 is a 24-id renumber (1,118 v3 CTs byte-identical to v2; `s####` not stable across releases); a C-ArmLSpine case is an acquisition, not a person (149 cases, 148 scored, 141 keyed) | `docs/PATIENT_IDENTITY_SPEC.md`; `memory/identity-audit-findings.md`; `docs/handoff/LEAKAGE.md` section 3 | CURRENT; whether the 149 cases are that many people cannot be established (OQ E1) |
| L.5 | The G3 person split: FROZEN 2026-09-23 20:18:48 (job 40426793); CHK-1 to CHK-5 and CHK-8 run (CHK-4b WARN: 8,082 training renders under the poses of val/test/held real subjects; CHK-8 WARN: 17 unkeyed AASCE coronal films); CHK-6 and CHK-7 NOT RUN; leak audit PASS; 92 of 97 validation and test persons sit in v8 or v9 training | `docs/handoff/LEAKAGE.md` sections 2, 5 (the freeze and the checks); RC A16.4 and `docs/handoff/extracts/LITERATURE_STATE_sections.md` line 67 (the 92 of 97); `results/spineps_ids/g3_split/split_leak_report.json` | CURRENT; never resubmit `g3_split.sh` as a check (it rewrites `/wsu/home/go/go24/go2432/split_final.json` in place) |
| L.6 | The content-hash chain (`slurm/data_accounting.sh`) proved on a planted-leak corpus (`code/tools/diagnostics/make_fake_corpus.py`) and never run on the real corpus | `docs/handoff/LEAKAGE.md` section 7 item 1; `docs/DATA_ACCOUNTING.md` section 7 (empty by design) | OPEN |
| L.7 | The TotalSegmentator render bench is not held out from the v9 encoder: 483 of 523 sacrum-bearing spines seen; only 70 TS + 1 CTSP + 0 VerSe renders unseen | `memory/ts-bench-inside-v9-bank.md`; `docs/handoff/LEAKAGE.md` section 7 item 9 | CURRENT |
| L.8 | VerSeFusion `has_T13` says 18; the truth is 6; 39 of 85 L6 masks lack id 25 (that row cites the manifest card and two memory notes, MAN versefusion, VFT, VF8, none of which prints the 39: the file the count was read from is not recorded) | `memory/versefusion-t13-flag-wrong.md` (18 against 6); `docs/handoff/extracts/RESEARCH_DIRECTIONS_sections.md` section 5.2, table row "VerSe and VerSeFusion", line 46 (39 of 85) | CURRENT for 18 against 6; the 39 of 85 is RECORD ONLY until a file prints it |
| L.9 | `splits_5fold.json` at the repository root is an empty file (0 B, 2026-09-12); the release split has no held-out test set and never read the lumbar count | `docs/handoff/LEAKAGE.md` section 7 item 8; RC F.17 | CURRENT |

## 6. The SPINEPS instance-id census and repair (`results/spineps_ids/`)

| id | result | file | status |
|---|---|---|---|
| S.1 | 2,437 harvested SPINEPS masks carried raw instance ids 1..N (harvested before commit 147428d); 3,490 relabelled from the POI centroids [DERIVED: 796 + 1,452 + 144 + 6 + 1 + 1,091, the `actions.relabelled` fields of the six `repair/relabel_summary_*.json`]; consumers listed | `results/spineps_ids/CENSUS.md`, `CENSUS_reading.md`, `IMPACT.md`, `REPAIRS.md`, `CONSUMERS.md`, `impact_counts.json`, `files.tsv` | CURRENT |
| S.2 | The relabel verified per tree (`VERIFY.md`, `verify.json`, `verify_rows.jsonl`); the TS12 cases verified by render (`TS12_VERIFY.md`, `ts12/*_verify.json`; the 60 render PNGs are not copied here, see `MANIFEST_LOCAL.md`) | `results/spineps_ids/repair/`, `ts12/` | CURRENT |
| S.3 | Rescore after the repair: `repair/rescore/bench_ctd/` and `ctsp_postfix/` (`summary.json`, `per_case.csv`, `report.txt`); `rescore_report.json` | `results/spineps_ids/repair/rescore/` | CURRENT; the numbers belong to `01` and `06` and are quoted there |
| S.4 | VERIDAH output is not truth (`veridah_check.json`) | `results/spineps_ids/veridah_check.json`; `memory/spineps-ids-can-be-scrambled.md` | CURRENT |

## 7. Inventories and usage tables

| id | result | file | status |
|---|---|---|---|
| I.1 | The CT axis of any benchmark is every collection: 5,700+ subjects across the render roots | `docs/CT_INVENTORY.md`; `memory/ct-benchmark-covers-all-collections.md` | CURRENT as a count; its bank labels are wrong (`physics_drr` is not CTSP-only; `carm_drr` holds real frames: `docs/handoff/DATASET_USAGE.md` section 6) |
| I.2 | The X-ray usage table per bank | `docs/XRAY_DATASET_USAGE.md` | CURRENT with one mislabel: `buu_2000` "AASCE test split, 4,000" is the BUU-LSPINE 2000 release (OQ F7) |
| I.3 | The 2026-09-16 manifest of data, models and results | `docs/MANIFEST_DATA_MODELS_RESULTS.md` | DATED (pre-migration paths) |
| I.4 | The bank profile of allspine v3 | `docs/bank_profile_v3.json` | RECORD ONLY (v3 bank deleted 2026-09-20) |
| I.5 | Every job cancelled on 2026-09-27 with how to resume it (NeurIPS appendix chains, ruleclass arms) | `docs/grid_records/JOBS_RECORD_2026-09-27_1544.{md,tsv}` | RECORD |
| I.6 | The scoping review of public spine datasets: protocol, pipeline, 21 `sdr/` modules, pilot run 2026-09-19; the review runs themselves (7,567 files) stay in the repository folder | `code/spine_data_review/`; `memory/spine-data-review-and-ts-bench.md` | DATED; no result number is quoted from it in any manuscript |
| I.7 | The dataset landscape by task and the joined ranking of 70+ collections | `../09_wrong_level_clinical_qi/docs/handoff/literature_state/dataset_landscape_by_task.md`, `ranking_joined.csv` (Greg-only; removed from this folder in the final pass; extract in `docs/handoff/extracts/LITERATURE_STATE_sections.md`) | CURRENT (2026-10-08) |

## 8. The model registry

| id | result | file | status |
|---|---|---|---|
| R.1 | Store with at least 57 entries; ledger 106 lines of which 17 carry one `orientation_net_v2` sha (the first registration at 15:39:56 plus 16 repeats to 20:57:21 on 2026-09-15); 79 aliases; MLflow SQLite 1,028,096 B; sixteen pre-registry models backfilled 2026-09-15 (1.1 GB mirrored) | GRIDLS "ls ~/model_registry", "registry.jsonl", "mlflow"; `docs/MODEL_REGISTRY.md` | CURRENT; answers OQ B31 |
| R.2 | The v9 level encoder is registered as `allspine_v9_fov96_ctx_rung_1_aug2` (store `188f9fcbfa3c6de1`, 2026-09-23); the real-frame detectors `rx_*` and the device-corpus detectors `dc_*` are not registered | GRIDLS "aliases"; `MANIFEST_GRID.md` section 4 | CURRENT; the gap is `01`'s to close |
| R.3 | `docs/MODEL_REGISTRY.md` tells the reader to run `sync` and `mlflow ui` on the login node and says compute nodes have no route out | `docs/MODEL_REGISTRY.md`; `docs/handoff/INFRASTRUCTURE.md` section 13 rows 5-6 | SUPERSEDED on those two points by `docs/MODEL_REGISTRY_CORRECTION.md` (compute nodes have internet, job 40409460; nothing runs on warrior) |

## 9. What is superseded, and by what

| superseded | by |
|---|---|
| The plan's sizes of 2026-09-01 (du) and the "861 GB" end state | the STATUS measurements and the census (M.7, M.13, M.14) |
| `memory/grid-access.md` (project root `/wsu/home/go/go24/go2432/CTSpinoPelvic1K`, labels `data/v5_final`, CT `data/hf_export/ct`; "the `grid` alias does not resolve") | labels and CTs under `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (B02); the alias resolves (`memory/windows-ssh-to-grid.md`) |
| allspine v2, v3, v4, v5, v5c crop banks and every number scored on them | deleted 2026-09-20 (`memory/grid-quota-and-deleted-banks.md`); holdouts repointed to v7; the v9 lineage |
| `CT_INVENTORY.md` bank labels; `XRAY_DATASET_USAGE.md` `buu_2000` row | `docs/handoff/DATASET_USAGE.md` section 6; OQ F7 |
| `MODEL_REGISTRY.md` login-node lines | `docs/MODEL_REGISTRY_CORRECTION.md` |
| "212 sources" (memory) | 211 + one merged alias (`DATA_MANIFEST.md`; `docs/handoff/INFRASTRUCTURE.md` section 13 row 17) |
| "B01 cut over" read as "the TCIA trees are safe" | M.4: the raw trees are ABSENT; re-acquisition route `tcia_ctsp_download` |
| the memory note's claim that compute nodes have no route out | job 40409460: they do (`INFRASTRUCTURE.md` section 13 row 6) |
| `memory/data-platform-migration-2026-10.md` lines 70-71: the dedup plan as first written (at most 97.7 GB linkable; 482.9 GB deletion candidates; 1,659 alias rows) | the revised `DEDUP_PLAN.md` "The totals" after its section 7 review: at most 95.8 GB; 353.7 GB now + 218.3 GB conditional (482.9 = 353.7 + the 129.2 GB scaling banks, now conditional); 1,631 concrete alias rows (D.1) |

## 10. Not recorded (said plainly)

What removed the TCIA CT Colonography raw and NIfTI trees, and when; why the grid can no longer fetch the private
repository; which `dp_migrate` job carries which batch (inferred only); whether `/wsu/home/go/go24/go2432/model_night/heads_mixed/` exists;
the throughput of this cluster's rsync (the pilot's `runs/B00/001.rsync.log` would give it; not read); whether v5
carried the NHANES twins; the HOME sizes after `films_ap_drr` alphabetically on 2026-10-08; the live state of the HF
mirror and Zenodo v11.
