# Verification

What a verifier should confirm about the planning files, how to confirm each item, and what the checks run on
2026-10-08 (on this laptop, and under WSL Linux) found. Nothing here touched the grid or the network.

Sections 1-4 are the first pass. Section 5 is the second pass of the same day, after a review found one blocker, 17
major and 25 minor defects; where section 5 and the first pass differ, section 5 holds.

## 1. Results of the checks run here

| check | how | result |
|---|---|---|
| planning files agree with each other and with the disk | `python3 verify_planning.py` (Windows and WSL) | 14 of 14 pass; details in `verification_report.json` |
| re-acquisition driver | `python3 reacquire/test_reacquire.py` | 15 of 15 pass (Windows and WSL) |
| index builder | `python3 db/test_build_index.py` | 16 of 16 pass (Windows and WSL) |
| migration scripts | `bash plan/test_migration.sh` (WSL: rsync 3.2.7, python 3.12) | 13 of 13 functional checks pass |
| facts re-derived from the evidence files | the spot-check script (results in `spot_checks.json`) | 32 of 32 confirmed |
| Python 3.6 syntax | `ast.parse(feature_version=(3, 6))` on every `.py` here | all parse |

### The 14 consistency checks (`verify_planning.py`)

| # | what it confirms | result |
|---|---|---|
| V1 | `sources.yaml` holds exactly the data of `sources.json` (read with `lib/mini_yaml.py` and with PyYAML) | pass, 212 sources |
| V2 | one card in `DATA_MANIFEST.md` per source id, and one source per card | pass, 212 and 212 |
| V3 | every imaging row of `plan/disk_map.csv` (raw, derived or unknown; 308 rows) has a row in `plan/layout_map.csv` | pass, 308 of 308 |
| V4 | the batch files `plan/batch_items/*.tsv` hold exactly the `move` and `optional_move` rows | pass, 211 rows |
| V5 | every README.yaml template parses (mini_yaml and PyYAML agree), names a known index adapter and known source ids | pass, 68 templates |
| V6 | every repository script a re-acquisition command or a planning document names exists | pass, 146 names (one grid-only script named on purpose: `slurm/download_nhanes_full.sh`) |
| V7 | every re-acquisition command splits under shlex (`bash -n` on each is in the driver's tests) | pass, 124 commands |
| V8 | no file here contains the forbidden word | pass |
| V9 | the manifest's citations that name a file resolve on this machine | pass: 467 distinct cited paths, 457 resolve, 10 do not and each is explained (table below) |
| V10 | the generated blocks of LAYOUT.md and MIGRATION_PLAN.md are filled | pass |
| V11 | `bash -n` on every `.sh` and `.sbatch` here; no CRLF line endings | pass, 6 scripts |
| V12 | every Python file parses as Python 3.6 | pass |
| V13 | the five aliases are unique and none equals a source id | pass |
| V14 | the totals the manifest quotes equal `plan/plan_summary.json` | pass, 209 items / 3,189.0 GB |

The 10 cited paths that do not resolve here: three are false positives of the checker (a file name with spaces,
`Spondylolisthesis Vertebral Landmark.zip`; the prose range `01..14_*.eml`; a CTSpinoPelvic1K script cited without
its prefix); six are files the cards themselves say are absent from this laptop (`tools/identity/ts_alias.json`,
`slurm/download_nhanes_full.sh`, `tools/make_yolo_levels.py`, `tools/make_mv_bands.py`,
`SchwingNet/results/repairs/CARMLSPINE_CHECK.md`, `acquisition/alias_pairs.csv`); one is a finding (section 3).

V9's scope: it checks citations written as file paths (prefixed `ssn:`, `sscn:`, `nnunet:`, `ctsp:`, `xrsp:`,
`sdet:`, `sdr:`, `mem:`, `MEM/`, scratch prefixes, and bare `docs/`, `tools/`, `slurm/`, `SchwingNet/`,
`acquisition/` paths). It does not open the cited line or check the cited number; family A's short names (AUDIT L…,
MDMR L…) and line numbers were checked by family A's own scripts (dp:check_lines.py, dp:check_lines2.py), and the
spot checks below re-derive a sample of numbers from the files.

### The 32 spot checks (numbers re-derived from the evidence, not copied from the cards)

CTSpinoPelvic1K manifest: positions supine 422 / prone 377 / decubitus 2 + 1; 802 records and 802 tokens; 1,153
distinct series UIDs; match_type separate 351; prov_pelvis manual 362 / pseudo 440; lstv_label normal 769 /
sacralization 17 / lumbarization 14 / semi-sacralization 2 (the file spells the last `SEMI_SACRALIZATION`); the
deposit README's "imaged supine" near line 223. RSNAI manifest roots: C-ArmLSpine 59,609 files / 23,347,039,978 B;
DeepFluoro vendor 94,626 / 72,708,547,975 B and its source string naming IFSXNV (the swapped DOI); TotalSegmentator
v3 228,803 / 52,343,746,738 B; SpineSAC 4,147,554,733 B. Acquisition: ranking.csv 146 rows; idc_tier1.csv 3,600
series, 892,817 instances, 39 collections. Audit: C-ArmLSpine zip 15,581,614,253 B; TS zips 23,581,218,285 and
37,415,622,057 B; Zenodo v11 22797014 and 2026-09-18; 810 OK; 0533 sha256 478a74e9…; NHANES 17,075; VinDr 10,466; RSNA
203,318,086,447 B; Geneva 412,867,633 B. COBRA 692/692, 771.1 GB (RESUME_2026-09-22_PM). Licence lines: CTPelvic1K
CC BY at ctsp:README.md L515 and NC at ctsp:docs/DATASETS_ROADMAP.md L95. Ljubljana local zip: 79,049,365 B and
sha256 31cb4838…fdea9 (hashed here). Census table: 4,482 GB used, 754, 682. tools/patient_keys.py path hints at lines
209-212. du of 2026-09-01: tcia 721G, tcia_nifti 336G, hf_export 328G. Listing: no HOME data folder symlinked to Ceph.

## 2. Checklist for the verifier

### 2.1 Every claim traceable

- [ ] Pick ten facts at random from `DATA_MANIFEST.md` cards; open the cited file at the cited line (legends in
      sections 5-9 of the manifest) and confirm the number. The tag before a merged card's text (`[A]` ... `[E]`)
      says which family's legend applies.
- [ ] Confirm that every structured value in `sources.yaml` matches its card: each block carries a `cite` list taken
      from the card field it came from (`acquired.cite`, `contents.cite`, `annotation.cite`, `reacquire.cite`).
- [ ] Confirm "not recorded" is written wherever a card had no file behind a fact (search the manifest for it), and
      that no date in the timeline (manifest section 3) lacks a "how known" column.

### 2.2 Every imaging entry of the listing mapped

- [ ] `python3 plan/build_plan.py --check` prints "every imaging row has a rule".
- [ ] When the census lands: `python3 plan/build_plan.py --census <census.tsv>`; confirm the batch totals move the way
      the census says, that no folder in `census/depth2.tsv` holding imaging is missing from `plan/layout_map.csv`, and
      that the three `inspect` rows left in B14 were looked at (two download leftovers and
      `~/spinopelvic-seg/nnunet/raw`; section 6 identified the other unnamed entries).
- [ ] On the grid, `sbatch --export=ALL,BATCH=ALL plan/preflight.sbatch`; every `ABSENT` item is one the cards said
      might be deleted (reclaim lists), and nothing else.

### 2.3 Every tool referenced exists

- [ ] V6 passes on the grid checkout too, run in a job, never on warrior (from `data_platform/`:
      `mkdir -p logs && sbatch -p reqp --qos=requeue -o logs/vp_%j.out --wrap "python3 verify_planning.py"`; the
      citation check V9 needs this laptop's paths and will report them unresolved on the grid, which is expected).
- [ ] The tools named only on the grid exist there: `slurm/download_nhanes_full.sh`,
      `~/spine-detector/scripts/download_sources.py`, `~/data/ribs/dl.sh`, the VerSeFusion download in `~/VerSeFusion`.

### 2.4 Every command parses, and the routes work

- [ ] `python3 reacquire/test_reacquire.py` (runs `bash -n` on every command).
- [ ] `python3 reacquire/reacquire.py --all` prints a block per source and one line per command.
- [ ] On the grid, one small `run` source end to end in a job, for example
      `cd reacquire && mkdir -p logs && sbatch -D "$PWD" --export=ALL,IDS="ljubljana_2d3d_gs",MODE=--run reacquire.sbatch`
      (79 MB, sha256 known), then `--verify`.

### 2.5 The migration on the grid

- [ ] B00 pilot: copy, verify, `tools/data_manifest.py check` on the remapped manifest, cut over, smoke checks,
      finalize; `pan_quota` drops by about 6 GB.
- [ ] B02: every item is in the hard-link group (`batch_items/B02.tsv`); the verify JSONs report
      `hardlink_groups_equal: true` and `n_nlink_differs: 0`, and one CT has the same inode under both Ceph paths.
- [ ] After each cut-over, one container job that binds the moved HOME tree and `/rs/rs_grp_oschome/go2432` reads
      through the symlink.

### 2.6 The index

- [ ] `python3 db/test_build_index.py`; then on the grid, after B00 and B02, `sbatch db/build_index.sbatch` with
      `FOLDERS="deepfluoro_h5 ctspinopelvic1k"`; `SELECT * FROM v_annotated_ct_by_modality_position` shows 802 CTSP CT
      items split prone / supine / decubitus as 377 / 422 / 3.

## 3. Findings made during verification

1. `tools/realxray_banks.json` names `tools/carmlspine_multi_build.py` as the builder of the `carmlspine_multi` bank;
   the tool is not in this repository and has no git history here.
2. The sized move total (3,256.3 GB after the second pass; 3,189 GB in the first) uses the 2026-09-01 du for the
   largest trees; 290 GB of it (the reclaim-listed B02 folders, 64.1 GB once the shared CT inodes are counted once,
   and B03, 226 GB) is presumed deleted (a memory note says reclaim phases A and B ran on 2026-09-07), the TCIA trees
   of B01 (1,057 GB) are on no delete list but their state after 2026-09-01 is not recorded, and 152 items have no
   recorded size. The census decides the real total (MIGRATION_PLAN.md section 10).
3. Five sources were carded twice under different ids and are merged (manifest section 2); the old ids remain
   aliases. Family B's card for `idc_ct_colonography` now sits inside `tcia_ct_colonography` (family A section).
4. `buu_lspine_drive_mirror` is deleted (disk_cleanup.sh); it keeps a card and no README.yaml.
5. Patient position is recorded in a release file for CTSpinoPelvic1K (manifest), and in DICOM headers for C-ArmLSpine
   frames and for the NBIA and IDC collections of family B, which keep their DICOM: the acquisition adapter now reads
   (0018,5100) from each case's series (second pass). Sources that ship only NIfTI or MHA stay `unknown`.

## 4. Where the generators are

`DATA_MANIFEST.md` and `sources.json` were generated from the five family card files by scripts in the session
scratchpad (`.../scratchpad/dataplan/platform/`: parse_cards.py, curated_a.py, curated_cd.py, build_sources.py,
make_manifest.py, spot_check.py; session scratch folder; scripts not preserved: not recorded). The second pass edited both files in place (scripts in `.../scratchpad/dataplan/fix2/`:
patch_facts.py, patch_reacquire.py, patch_recipes_md.py; session scratch folder; scripts not preserved: not recorded), so rerunning the first-pass generators would undo it; do not.
From now on `sources.json` and `DATA_MANIFEST.md` are the files to edit; `sync_sources_yaml.py` rewrites
`sources.yaml` from `sources.json`. The plan tables regenerate from `plan/build_plan.py`, which lives here.

## 5. Second pass, 2026-10-08: the review's findings, what changed, what was checked

A review of the first pass reported 43 findings (1 blocker, 17 major, 25 minor) against the manifest, the
re-acquisition driver, the migration scripts and the index. Every one was checked against the files it cites before
anything changed; all were applied, three with a correction to the finding itself (section 5.3). Nothing touched the
grid or the network.

### 5.1 Results of the checks run after the changes

| check | how | result |
|---|---|---|
| planning files agree with each other and the disk | `python3 verify_planning.py` (Windows and WSL) | 14 of 14 pass: 212 sources, 308 imaging rows mapped, 213 batch rows, 68 README templates, 146 tool names, 87 commands, 469 cited paths (459 resolve, the same 10 explained ones do not), 211 items / 3,256.3 GB quoted and planned |
| re-acquisition driver | `python3 reacquire/test_reacquire.py` | 28 of 28 pass (Windows and WSL); 13 tests are new |
| index builder | `python3 db/test_build_index.py` | 24 of 24 pass (Windows and WSL); 8 tests are new |
| migration scripts | `bash plan/test_migration.sh` (WSL: rsync 3.2.7, bash 5.2) | 26 of 26 checks pass; 13 are new |
| the review's own probes, rerun | `scratchpad/dataplan/review_mig/probe_migration.sh`, `probe_index.py` (session scratch folder; scripts not preserved: not recorded) | P2 and P5 fixed; P1, P3, P4 now caught (their printed last lines are explained in 5.3); the index probe gives masks attached, VerSe roles from the path, per-release status |
| the four changed repository scripts | `bash -n` | parse; not run |

### 5.2 What changed, finding by finding

**Manifest and `sources.json` (13 findings).**

| finding | change | evidence checked |
|---|---|---|
| acquisition dates of five film sources said "not recorded" (major) | CSXA 2026-09-01..09 (LICENSE 22:50, images 2026-09-09 23:00); BUU-LSPINE 3600 2026-09-09 22:50; BUU v1 smoke and NHANES annotated zip 2026-09-01 23:28; NHANES II films 2026-09-09 13:03 to 2026-09-23 03:00, with the 2026-09-11 cancellation kept as an event; VinDr 2026-09-07 17:49 to 2026-09-10 17:25. Timeline rows, cards and `acquired.date`/`date_basis` | `SchwingNet/results/g0_facts.md` §2 lines 65-68 |
| CTSpine1K and CTPelvic1K HOME copies dated 2026-05 and 2026-09-01 (major) | both "by 2026-04-25", exact day not recorded; the 2026-05-16 "use token" commit noted as a possible re-run; "gated in May" now "gated in April" | `git show 550cfff` (2026-04-18) holds `slurm/download_raw.sh` with both stages and the "gated" header (line 34) and `scripts/place_fused_masks.py`; CRC lines 51, 247, 329-331 |
| April release recipe cloned the wrong repository and checked 1,000 files (major) | source of record `anonymous-neurips-ED/CTSpinoPelvic1K`, revision not pinned down; check 1,153 records (342 + 351 x 2 + 89 + 20); the gregoryschwingmdphd repository described as not this release; build chain kept as the fallback | CRC lines 51, 348-351; AUDIT line 618; CTSpinoPelvic1K-1 README lines 400, 424, 453 |
| "107 more collections" | "88 more family-B sources are not fetched (23 planned, 7 gated, 58 excluded)", from `sources.json`; three unfetched ranking rows are family-A cards | `sources.json` statuses; `ranking.csv` (146 rows) |
| "40 IDC tier-1 collections" | 39 plus the `idc_tier1` route card | `manifests/idc_tier1.csv`: 39 collections, 3,600 series |
| "117 on disk" did not reproduce | 116 on disk on the grid (on_disk, partial, state_unknown, unidentified); family D 17 on disk, 7 other; modality tally recomputed (unknown 1) and the definition stated | `sources.json` |
| reclaim "not recorded" | the memory note's statement (phases A and B ran on 2026-09-07; no job log here; phase-A/B folders presumed deleted pending the census) in section 1, defect 39, the unknowns tables and the four `sources.json` location notes | memory note zenodo-deposit.md line 30 |
| `ctsp_april` contents "not recorded" | fetch job 40480758 fetched and sha-verified 2,306 of 2,306 inputs of the 1,153 records; only the subpath stays unknown | `docs/RESUME_2026-09-22_PM.md` line 139 |
| 2026-09-19 du not used | `~/spinesurg-ct-nnunet` 363G (the 1,433.6 GB of 2026-09-01 marked superseded), `~/spine-detector` 382G, `~/nhanes_pseudo` 74G in `plan/disk_map.csv`, the cards and the unknowns row | `docs/CONTINUANCE_2026-09-19.md` line 27; `du_home_top.txt` dated 2026-09-19 in the listing |
| row spacing "172 of 801" | wrong on all 801 (median 7.5 %), more than 1.2x off on 172 | memory note drr-row-spacing-defect.md |
| timeline cites for DeepFluoro vendor and SpineSAC | vendor: g0_facts §2, 01:23 (the "01:35" had no source and is gone); SpineSAC: listing and git c7013ca/9fcc9cf (2026-09-22), AUDIT line 716 for the count only | g0_facts line 72; `git log` |
| PolyPose "82 GB" | the folder total, which holds the venv, the sif and the `deepfluoro_xvr_hf` copy; cohort size not recorded | `slurm/env/polypose.setup_status.json`; `slurm/polypose_env.sh` (`HF_HOME=$PP_ROOT/hf`) |
| VerSeFusion `has_T13` "wrong" | describes the VERIDAH-renumbered tree; the masks give 6; the memory note cited only for the instruction | AUDIT line 948 |

Every card whose re-acquisition entry changed (80) now opens its recipe field with an italic line naming the change
and pointing at `sources.json`; section 2 of the manifest says the `sources.json` block is the runnable form.

**Re-acquisition (15 findings).**

| finding | change |
|---|---|
| sbatch log folder missing (major) | `logs/.gitkeep` committed beside each sbatch file (reacquire, plan, db); the printed sbatch line and every usage comment run `mkdir -p logs` first; `reacquire.sbatch` stops with a message when the driver is not on the grid yet. The same defect was in `migrate_batch.sbatch`, `cutover.sh`, `preflight.sbatch` and `db/build_index.sbatch`; all fixed |
| CTSpinoPelvic1K rebuild (major) | writes a fresh tree `raw/CTSpinoPelvic1K_v11` (never the migrated working copy, so "already built" cannot pass on old files); builds `dcm2niix` from conda-forge under `$RS/envs/dcm2niix` and tests that it runs, as `slurm/ctsp0533_repair.sh` lines 84-118 do; checks the `tcia_utils` import first; new helper `reacquire.py nifti-check` reads every CT's gzip stream and compares shape and affine with the label; `tools/ctsp0533_verify.py` judges 0533; the cast file's sha256 is a note, no longer a check |
| recipes writing to HOME (major) | TCIA: `DATA_DIR=${DEST}` (bound into the container through a real path), the conda singularity on PATH, the SIF checked first; VerSe: `slurm/download_raw.sh` submitted directly with `DATA_DIR`/`RAW_DIR` on Ceph (the Makefile's own `DATA_DIR` would override the environment); `verse_drr`, `spinalai_drr`, `aasce_drr`, `ts_drr_v3`, `ctsp_drr` source and destination on the layout; also `ts_drr`, which the review did not list; a test fails any recipe that names `${HOME}/` outside the environments |
| 40 IDC entries sharing one state folder (major) | `idc_tier1` is the only runnable IDC entry; the 39 per-collection entries are `manual` with `covered_by: idc_tier1`, their single-collection command in the steps, and a check that counts that collection's series in `verified.jsonl` (they sum to 3,600); `reacquire.py` refuses any selection in which two runnable sources share an acquisition state folder |
| manifests read from the Ceph tree (major) | read from `SchwingNet/results/transitional_registry/acquisition/manifests/` in the repository; `$D/logs` created before every family-B sbatch |
| AASCE recipe was a discovery sweep (major) | new helper `reacquire.py github-zip` (the codeload zip of the default branch, as `tools/thoracic_xr_fetch.py` built its URL) with md5 fe9430ab... and 354,809,072 B, unzip, a 903-jpg count that ignores files under 1 KB; the sweep kept as an optional discovery step |
| GPU rebuilds forced onto reqp (major) | `lstv_flag_renders`, `physics_drr`, `implant_ct_synthetic`, `nnunet_dataset815` are `manual` with their own submit lines; `carm_drr` runs only `tools/carmlspine_to_bank.py` into the layout (the fine-tune and its `rm -rf $HOME/carm_drr` are gone) |
| helpers ran before the login-node check | they refuse on warrior and outside a job (`--outside-slurm` for tests) |
| reruns and requeues | a requeue keeps its job id, and submit-mode commands that already ran in that job are skipped (`--resume` across jobs); every download goes to `.part`, is checked, and only then replaces the destination (a complete file that fails its hash becomes `.bad`); an existing copy that verifies is kept; a complete `.part` is finished without a request; HTTP 416 on a complete `.part` is taken as done; C-ArmLSpine passes `--bytes 15581614253` |
| VerSe check read `failed` | reads `n_failed`; unify and qc chained with `afterany` |
| DeepFluoro vendor unpack submitted from a `run` source | the unpack runs inline in the same job |
| bare `kaggle` | the spineps env's `kaggle` by path, with `-p` |
| `git lfs pull || true` | `git lfs pull` is required when `.gitattributes` declares LFS; the jpg count ignores pointer stubs |
| CTPelvic1K regex and cite; Geneva nested zips; Dataset802/803 | regex `dataset([1-5]_mask_mappingback|[67]_data)`; new check `archive_ok` reads every tar member; Geneva unpacks the nested zips and checks 482 files (AUDIT line 733); 802/803 is a manual rebuild and the checkpoint repository is described as a model source whose privacy is not recorded |
| dry run hid check keys | every key a check uses is printed; `--all` prints `IDS="--all --modes ..."`; `--grid` resolves the grid's HOME |

Also fixed: `source_env` gave a derived bank the source's `raw/` folder as `DEST`; it is now the layout subpath.

**Migration (13 findings).**

| finding | change |
|---|---|
| FINALIZE deleted without comparing (blocker) | FINALIZE requires the symlink to point at an existing Ceph copy, reruns `verify_transfer.py` on `.pre-ceph` against Ceph (every file hashed when the item is `irreplaceable` or under 50 GB), and refuses when a size-and-mtime rsync dry run itemizes anything; results in `runs/<B>/<n>.finalize.json`. The running-job check also reads batch scripts and the usual path spellings, and MIGRATION_PLAN.md section 2.3 says it is advisory |
| only one B02 item in the hard-link group (major) | every B02 item and the spine-detector `yolo*` banks are groups; `verify_transfer.py` fails a file whose hard-link count differs between HOME and Ceph; `test_migration.sh` checks the generated `B02.tsv` and `B04.tsv` |
| group reruns did not resume (major) | copies already placed are renamed back into staging, refreshed by the one group rsync (`--delete` inside staging) and moved into place again; staging is removed at the end; a rerun refuses leftovers its `.group_items` record does not name |
| B12 would dangle inside fifteen nnU-Net containers (major) | B12 dropped: `nnunet/raw` stays on HOME; the fifteen scripts listed in MIGRATION_PLAN.md section 6; `slurm/versefusion_totalseg.sh` binds the group path for B06; the `Path.resolve()` hazard written down |
| Python on the login node (major) | every step is a job (`sbatch --wrap`) or runs on this laptop; "anywhere" removed from db/README.md |
| generic adapter (major) | mask-named volumes attach to the image with the same case stem and are never items; with no file-level label the release's `annotation.status` applies, marked per-release; hard-link copies get `duplicate_of` and `counted = 0`; conversions and outputs beside a DICOM release are kept with `counted = 0`; README `index_skip` leaves out the CTSpine1K HOME copy; the source table carries annotation status and position; the views count `counted = 1` and treat `unknown` as not annotated |
| VerSe adapter (major) | source and role from the first folder below `VerSeFusion_data`; `unified/` and `qc/` not indexed; masks matched within their own tree |
| family-B position (major) | the acquisition adapter maps each case to its series UID (`convert/shard*.jsonl`) and its DICOM folder (`fetch/verified.jsonl`) and reads one header: position, StudyDate, manufacturer, series UID; the harvest calls attach to the CTSP, VerSe and TotalSegmentator items by subject key |
| batch sizes did not add up; section 10 impossible | an unsized parent takes the sum of its sized children (VerSeFusion/data 138.1 GB, VinDr 48 GB); the 192.8 GB of shared CT inodes counted once (B02 291.1 GB, its candidates 64.1 GB); the nnunet note no longer lists `preprocessed`; section 10 rewritten: what stays on HOME with a recorded size (about 1,018 GB) plus the sized move total exceeds the 4,050 GB HOME holds, so the end state waits for the census |
| restricted pixels group-readable | every layout row whose sources name VinDr-SpineXR or BUU-LSPINE, and the spine-detector `interim` and `yolo*`, is flagged `restricted`, copied with `--chmod=go-rwx` and closed again after the copy; mixed folders list `restricted_subfolders`; closing the existing `$RS/data/vindr` is a one-line job left to Greg |
| relative links leaving an item verified | a link that resolved at the source and does not resolve at the copy fails verification; preflight counts relative links that leave each item |
| rebuild scripts deleted the symlink | `slurm/nhanes_build.sh`, `slurm/vindr_pseudolabel.sh`, `slurm/launch_dual.sh` clear the bank's contents through the link (`find -H <bank> -mindepth 1 -delete`; their writers use `exist_ok`); listed in section 6 |
| existing destinations overwritten | a destination that exists and was not written by an earlier run of the same item is refused (`DST_EXISTS`; `runs/markers/`) |
| setgid lost | `--chmod=Dg+s` |
| layout entries | `~/spinopelvic-seg/nnunet/raw` inspected first (B14); `~/lstv_flag` split, only its render folders move; the B13 target is `$RS/results/nnunet_results`; the CTSpine1K HOME copy lands at `raw/home_copy` (no wrong date in a path) |

### 5.3 Where the review was wrong, or partly

1. ".gitignore:49 ignores logs/*" does not apply here: the pattern `logs/*` contains a slash, so git anchors it at the
   repository root, and `git check-ignore -v data_platform/plan/logs/.gitkeep` (and the reacquire and db ones)
   returns nothing (exit 1). The defect itself, no `logs/` folder when Slurm opens `--output`, was real and is fixed.
2. The C-ArmLSpine zip size (15,581,614,253 B) is at `docs/DATA_COMPLETENESS_AUDIT.md` line 710, not 703; the value is
   right and the cite in `sources.json` says line 710.
3. AUDIT line 618 calls `gregoryschwingmdphd/CTSpinoPelvic1K` the "Older HF repo ... (1153-record era, not the
   release)"; the review called it "a later 1,000-file state". Its lastModified (2026-08-28) is after the April export,
   but the audit calls it older, relative to the current release. The card quotes the audit and says only that it is
   not the 1,153-record April state.
4. The review's "90 not-fetched ranking.csv rows" was not re-derived: ranking rows and family-B sources do not map one
   to one (AMOS22 has two rows; the `idc_tier1` route card, `validation_ts` and `nlst_pilot` have none; three unfetched
   rows are carded under family-A ids). The manifest now uses only `sources.json` statuses (88 = 23 + 7 + 58).
5. For NHANES II the 2026-09-23 03:00 `.download_complete` was written by `slurm/film_corpus_inventory.sh`, an
   inventory marker, not by the download (the structured entry already said so); the timeline keeps both dates and
   says which is which.
6. The probes' printed last lines after the fixes: P1 still prints "hard link BROKEN" because the probe writes its own
   batch file in which only one item is flagged; with that file both items now fail verification (hard-link counts
   differ), and the generated `B02.tsv` flags every item. P3 prints "link DANGLES although verify said VERIFIED"
   because it checks the link, not the status: the bank holding the link is VERIFY_FAILED and only the item it points
   into verified. P4 prints "late file LOST" because it looks only on the Ceph side: FINALIZE refused
   (REFUSED_PRE_DIFFERS) and the file is still in `.pre-ceph`. `test_migration.sh` asserts all three.
7. The `--impersonate` streaming path is, as the review said, safe at Geneva's 413 MB; unchanged, except that the
   `.part` is now checked before it replaces anything.

### 5.4 Defects the second pass found that the review did not list

- **Empty fields shifted the flags column.** `IFS=$'\t' read` treats consecutive tabs as one separator, so every
  batch row with an empty size (152 unsized items) put its flags into the size field: `hardlink_group`, `restricted`
  and `glob` were lost for those rows (the `yolo*` row would not have expanded; the `build_archive*` rows would have
  left the group). `migrate_batch.sbatch`, `cutover.sh` and `preflight.sbatch` now read rows with a `\037` separator.
  `test_migration.sh` caught it.
- **Empty arrays under `set -u` on bash 4.2.** The nodes run CentOS 7 (`slurm/env/polypose.setup_status.json`:
  host_os CentOS Linux 7, glibc 2.17). CentOS 7 ships bash 4.2, which raises "unbound variable" on `"${arr[@]}"` of
  an empty array under `set -u`; the bash version on the nodes is not recorded. The optional-argument arrays use
  `${arr[@]+"${arr[@]}"}`. WSL has bash 5.2, so this is reasoned, not tested.
- **A stale batch file.** `build_plan.py` left `batch_items/B12.tsv` behind when B12 lost its item (V4 caught it); it
  now removes the files of empty batches.
- **`ts_drr` wrote to HOME** through the script's defaults; fixed with the other recipes.

### 5.5 Files changed outside `data_platform/`

`slurm/versefusion_totalseg.sh` (binds `/rs/rs_grp_oschome/go2432` when it exists), `slurm/nhanes_build.sh`,
`slurm/vindr_pseudolabel.sh`, `slurm/launch_dual.sh` (clear a bank's contents instead of removing its path). Each
parses (`bash -n`); none was run. `data_platform/` itself is still untracked in git.

### 5.6 Open for Greg

- Commit and push `data_platform/` and the four slurm scripts (both remotes, through WSL) before any grid run; the
  sbatch scripts stop when the driver is not on the grid.
- The census (job 40578909): regenerate the plan from it, then rewrite MIGRATION_PLAN.md section 10 and the dated
  sizes; inspect `~/spinopelvic-seg/nnunet/raw` and the two download leftovers (section 6 identified the other
  unnamed entries).
- Group read of DUA/EULA pixels: the allspine and other banks that hold BUU or VinDr pixels are now owner-only by
  default, which affects any student who reads them; and whether to close the existing `$RS/data/vindr`.
- Items that will fail verification by design until decided: a bank whose relative links point into another item, and
  any file whose hard-link partner is not in the plan (`ALLOW_NLINK_LOSS=1` after review).
- `tcia_utils` in the spineps env (the CTSpinoPelvic1K rebuild checks and stops); the SIFs that the TCIA and VerSe
  recipes check for (`CTSpinoPelvic1K/containers/ctspinopelvic1k.sif`, `VerSeFusion/containers/versefusion.sif`).
- GPU rebuilds left manual: the `PSRC` values of `physics_drr`, `TS_SRC` and an array size for `implant_ts`, a resume
  guard for the implant stage, and the HOME paths hard-coded in `slurm/lstv_flag_render.sh`.
- Whether `OpenSpineConsortium/spinopelvic-seg-checkpoints` is private is not recorded.

## 6. Third pass, 2026-10-08: the HOME entries nobody had named

Greg: "Please don't give up on these, identify them based on any metadata or url source data affiliated with them."
A read-only job on the grid (scratchpad `inspect_unknown.sh`, output `inspect_unknown.out`: session scratch folder, neither preserved: not recorded; a token that appeared in
it is copied nowhere) listed the files, dates, git remotes, README and log heads of the fifteen HOME entries no file
named (the fourteen disk-map rows of role `unknown` and `~/data/spondy_landmark`) and of `$RS/data/morphdef`. Thirteen
of the fifteen and `morphdef` are identified; MIGRATION_PLAN.md section 5 ("B14") has the table. Nothing touched the
grid or the network from this laptop, and nothing was committed.

### 6.1 What changed

- `plan/build_plan.py`: one rule per identified path. Six imaging-derived items move in B14 into the folders of their
  sources (`~/data/spondy_landmark` to `mendeley_5jdfdgp762/raw/`; `~/s1v11`, `~/pitest`, `~/pdwtest` and
  `~/qc.tar.gz` to `ctspinopelvic1k_build_tree/derived/`; `~/dis_renders` to `xrspinopelvic1k/derived/`); nine
  entries stay (action `stay`, batch B14); three stay inspect-only. B14 is renamed "identified 2026-10-08: moved or
  left" and depends on B02, B04, B05. Because jobs on the grid read the item files of B00-B09, no batch B00-B11 gained
  or lost an item: `~/data/spondy_landmark`, an inspect-only row of B08 that was never in `B08.tsv`, moved to B14.
  The totals now cover B00-B11 and B14 and leave inspect-only rows out; the 211 quoted before counted
  `spondy_landmark`'s inspect row as an item. Stale README.yaml templates are removed (`spondy_landmark.yaml`), and a
  sub-folder closed for a reason other than DUA/EULA pixels (`derived/s1v11`) says so in its README.yaml.
- `plan/disk_map.csv`: 18 rows (role, source id, notes; the sizes of `~/pitest` and `~/pdwtest` from the listing).
- `sources.json` / `sources.yaml`: `spondy_landmark` merged into `mendeley_5jdfdgp762` (the id stays as an alias;
  `reacquire.py spondy_landmark` prints the Mendeley recipe), 212 to 211 sources; `~/s1v11` and `~/qc.tar.gz` moved
  from the `ctspinopelvic1k` locations to `ctspinopelvic1k_build_tree`, with `~/pitest` and `~/pdwtest`;
  `~/dis_renders` added to `xrspinopelvic1k`; timelines and defects.
- `DATA_MANIFEST.md`: section 1 counts and totals, five timeline rows and one history row (`~/docs`), the three cards,
  the former `spondy_landmark` card kept verbatim in a collapsed block inside the Mendeley card, unknowns rows A14, D16,
  E4 and E18 removed, E5 rewritten to the two leftovers, A22 annotated.
- `LAYOUT.md` rules 3 and 8, section 3 and the action legend; `MIGRATION_PLAN.md` sections 0, 1, 5 (the B08 note and
  the B14 section), 7, 8 and 10; `README.md`.
- `plan/test_migration.sh`: seven checks (listed in its header).

### 6.2 Results of the checks run after the changes

| check | how | result |
|---|---|---|
| the item files the grid jobs read are unchanged | `cmp` of `plan/batch_items/B*.tsv` against a copy taken before this pass | B00-B13: 13 of 13 byte-identical; `B14.tsv` is new (6 items) |
| planning files agree with each other and the disk | `python3 verify_planning.py` (Windows and WSL) | 14 of 14 pass: 211 sources, 300 imaging rows mapped, 219 batch rows, 67 README templates, 147 tool names, 87 commands, 473 cited paths (463 resolve, the same 10 explained ones do not), 219 items / 3,256.6 GB quoted and planned |
| every imaging row has a rule | `python3 plan/build_plan.py --check` | 324 rows |
| re-acquisition driver | `python3 reacquire/test_reacquire.py` | 28 of 28 pass (Windows and WSL) |
| index builder | `python3 db/test_build_index.py` | 24 of 24 pass (Windows and WSL) |
| migration scripts | `bash plan/test_migration.sh` (WSL) | 33 of 33 checks pass; 7 are new |

### 6.3 What the inspection does not show

- Some facts came from the same day's grid reading and are not in `inspect_unknown.out`: what `url.txt` and
  `files.json` hold, the `Train/` (`Keypointrcnn_data`) and `Test/` (16 entries) layout of `spondy_landmark`, the member
  names of `qc.tar.gz`, what `~/v` and `VerSeFusion.tar.gz` contain. The cards and the plan say so where they use them.
  The `qc.tar.gz` member pattern agrees with what `ctsp:scripts/viz_propagation.py` L122 writes, committed the day the
  archive is dated.
- The inspection's URL search printed nothing for any entry: its pattern `[^"' <>)\]]+` ends the bracket expression
  at the first `]`, so it demands a literal `]` after one character and matches no URL (tested here with GNU grep in
  Git Bash and WSL). A rerun with `]` first in the class (`[^]"' <>)]+`) would print the URLs.
- Not checked: whether `~/s1v11/out/v11_labels`, `~/pitest` and `~/pdwtest` share inodes with the release labels (the
  preflight shows it); whether `~/s1v11`'s upload scripts or state files hold a token; whether the `spondy_landmark`
  zip's sha256 equals `mendeley_716`'s; what the `~/dis_renders` PNGs show; the two download leftovers.
- Security: `~/github` holds a GitHub personal access token in plain text (mode set to 600 on 2026-10-08). Greg
  rotates the token and deletes the file.
