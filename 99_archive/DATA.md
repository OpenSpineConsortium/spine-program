# DATA.md: this folder's grid paths, reached through Beethoven

Written 2026-10-12. This folder is Greg-only (`CLAUDE.md` first lines); a student claims work here only after Greg
confirms a hand-out. Nothing in this folder is run, trained, scored or quoted: `TODO.md` step 1 says the folder gains
only dated records and list rows, and the copied records are never edited. So this file names no experiment. It lists
every grid path of `MANIFEST_GRID.md` sections 1 to 4, spelled as that manifest spells it, so a reader can find each
one and knows that no number from it is quoted.

**Columns.** Volume: HOME = `/wsu/home/go/go24/go2432` (Panasas), Ceph = `/rs/rs_grp_oschome/go2432`. What it holds,
its size and its migration state come from `MANIFEST_GRID.md`, whose one read-only grid pass is 2026-10-08 22:20 UTC
(`10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`, "GRIDLS"). Where a later record changes a
row, it is cited: Greg's data-platform record of 2026-10-11 (issue #49), restated in
`10_data_platform_grid/MANIFEST_GRID.md` section 2 ("folder 10, section 2" below), and the batch item lists
`10_data_platform_grid/code/data_platform/plan/batch_items/B*.tsv`. What no file records is written "not recorded".

**Status word.** The status of the result each path holds, from `docs/handoff/RESULTS_CATALOG.md` (the row id is
given) and `STATUS.md`, as one of RECORD ONLY, SUPERSEDED, LEAKED (the catalog's [LEAK] mark), REFUTED or NOT
RECORDED. NOT RECORDED stands where the catalog marks the result NOT RECORDED, where it gives no status word, or where
no catalog row names the path; the catalog's own words follow in brackets where they say more. No path below has a
CURRENT row, so no number from any of them is quoted (`CLAUDE.md` trap 1; `TODO.md` step 15).

**Check lines.** Each is read-only: `ls -ld <path>` for a directory, a link or a file whose contents are not read;
`head -c 200 <file>` for a small file. Run them from the Beethoven worker, a session on a compute node, never python
or `du` on the login node (`CLAUDE.md`, "The standing rules"). A check line written with `{a,b}` expands in bash; a
check on a path expected to be absent answers "No such file or directory", and that answer is the check. A check line
on a HOME path works only for Greg: nothing on HOME is readable by students ("Access", below), so every HOME row is
marked **on HOME, not reachable until migrated**, with its migration state beside it.

## 1. Paths this archive owns (`MANIFEST_GRID.md` section 1)

| path | volume | what it holds | status word | migration state | check line |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw/rsna_cspine` | Ceph | the RSNA 2022 cervical-spine fracture CT archive: the Kaggle zip (2,019 train studies; per-level fracture labels C1-C7; 87 segmentations), one `.nii.zip`, `sample_submission.csv`, `fetch.log`; never unpacked; used by nothing; a header census refused every study (longest craniocaudal extent 334 mm, below the 350 mm a junction count needs). 4 files, 203,321,991,870 B (B08 STATUS row 001); zip 203,318,086,447 B | NOT RECORDED (no catalog row) | batch B08 VERIFIED: files 4/4, bytes 203,321,991,870 / 203,321,991,870, sampled 4 (GRIDLS line 2116); FINALIZED 2026-10-11 (folder 10, section 2). Readable by approved students. Keep or delete is Greg's (`docs/handoff/OPEN_QUESTIONS.md` A19; `TODO.md` step 2) | `ls -ld /rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw/rsna_cspine` |
| `/wsu/home/go/go24/go2432/data/rsna_cspine` | HOME | a link to the Ceph path above (GRIDLS line 2190, dated 2026-10-08 08:12) | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; B08 cut over; read the Ceph path | `ls -ld /wsu/home/go/go24/go2432/data/rsna_cspine` |
| `/wsu/home/go/go24/go2432/data/rsna_cspine.pre-ceph` | HOME | the HOME original, dated 2026-09-19 (GRIDLS line 2191); 236.8 GB of HOME before the move (`docs/handoff/DATASET_USAGE.md` section 7) | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; present on 2026-10-08; FINALIZE deletes the `.pre-ceph` copy and B08 was FINALIZED 2026-10-11 (folder 10, section 2), so it is expected absent | `ls -ld /wsu/home/go/go24/go2432/data/rsna_cspine.pre-ceph` (expected to fail) |
| `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` | HOME | a backup of the April 2026 `spinesurg-ct-annotator` repository (1083c4f), dated 2026-08-10; role beyond the name not recorded; directory entry 4,096 B (GRIDLS line 1134); contents size not recorded | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; in no batch, so no move is scheduled; its fate is Greg's (OQ A26; `TODO.md` step 11) | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` |
| `/wsu/home/go/go24/go2432/Multi-View-Vertebra` | HOME | a clone of the MICCAI 2023 Multi-View-Vertebra reference code (the multi-view sequence loss the parity ladder excludes); upstream URL not recorded; directory entry 4,096 B, dated 2026-09-13 (GRIDLS line 133) | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; B14 stay, kept on HOME (`../_plan/inventories/grid_manifest.tsv` row 199) | `ls -ld /wsu/home/go/go24/go2432/Multi-View-Vertebra` |
| `/wsu/home/go/go24/go2432/docs` | HOME | ten documents of 2026-02-12 from an earlier weak-label project (titles not recorded); size not recorded | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; B14 stay (`../_plan/inventories/grid_manifest.tsv` row 208) | `ls -ld /wsu/home/go/go24/go2432/docs` |
| `/wsu/home/go/go24/go2432/_adv_510.py` and about 300 loose audit scripts and outputs in the HOME root (`_adv_*.py`, `_v*_*.py`, `verify_*.py`, `ts_*.py`, `df_*.py`, `fc*.py`, `nh_*.py`, `mend_*.py`, `vprobe*.py`, `*.json`, `*.png`) | HOME | the identity-audit scratch of 2026-08-28, 2026-09-20 and 2026-09-22; `_adv_510.py` 1,610 B (GRIDLS line 145); `dicom_identity.json` 975,717 B; `df_ident2.json` 3,522,392 B; `_v_vindr_hdr.json` 1,606,544 B; the rest names only. Their conclusions are `docs/PATIENT_IDENTITY_SPEC.md` and `docs/DATA_COMPLETENESS_AUDIT.md` in spinesurg-ct-nnunet (owned by 10) | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; in no batch | `ls -ld /wsu/home/go/go24/go2432/_adv_510.py` |
| `/wsu/home/go/go24/go2432/logs` | HOME | HOME job logs (`slurm_logs`, `tmp`, `runs`, `track5`, `reg`, `selective`, `lstv_eval`, and the other subfolders `MANIFEST_GRID.md` lists); roles beyond name and date not recorded; directory entry 94,208 B | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; in no batch; deletion is Greg's call (OQ A26) | `ls -ld /wsu/home/go/go24/go2432/logs` |

## 2. FluoroCap on the grid (`MANIFEST_GRID.md` section 2; owned by `02_transitional_naming_truth` as test material)

| path | volume | what it holds | status word | migration state | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/FluoroCap` | HOME | the literature fluoroscopy harvest: the frozen release of 2026-09-13 (A 2,531 included panels, B 991 licence-clean), `articles/` and captions, `annotate/`, `archives/`, `PROTOCOL.md`, `CORPUS_MANIFEST.*`, `LEVEL_COUNTS.*`, and the weights registered from it on 2026-09-15; 367 entries; 316 GB by `du` on 2026-09-19 | NOT RECORDED (no catalog row names this path; the FluoroCap counts are descriptive, `STATUS.md` section 4) | on HOME, not reachable until migrated; B09 copying on 2026-10-08, FINALIZED 2026-10-11 (folder 10, section 2: "B09 (7; FluoroCap 316 GB)"); read the Ceph target below | `ls -ld /wsu/home/go/go24/go2432/FluoroCap` |
| `/rs/rs_grp_oschome/go2432/data/fluorocap/raw` | Ceph | the B09 landing folder; 1 entry at 22:20 UTC on 2026-10-08 | NOT RECORDED (no catalog row) | B09 FINALIZED 2026-10-11 (folder 10, section 2); readable by approved students | `ls -ld /rs/rs_grp_oschome/go2432/data/fluorocap/raw` |
| `/wsu/home/go/go24/go2432/REPORT.md` and `REPORT_interim.md` | HOME | the FluoroCap reports of 2026-09-13; 20,227 B and 16,115 B (GRIDLS lines 137-138); in no repository | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; in no batch; fetch with `scp` in a job when Greg allows (`TODO.md` step 13) | `ls -ld /wsu/home/go/go24/go2432/REPORT.md /wsu/home/go/go24/go2432/REPORT_interim.md` |
| `/wsu/home/go/go24/go2432/FluoroCap_lstv2` | HOME | the transitional harvest arm of FluoroCap (`memory/fluorocap-prototype-and-lstv-arm.md`); size not recorded | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; migration state not recorded; not re-verified on 2026-10-08 | `ls -ld /wsu/home/go/go24/go2432/FluoroCap_lstv2` |
| `/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` | HOME | the body detector of the reported SchwingNet stack (alias `detector_v5z_final`), the same file as `/wsu/home/go/go24/go2432/FluoroCap/detect_v5z_final_best.pt`; 42,233,939 B; owned by 01; private | NOT RECORDED (a weight, not a result file; numbers measured with it are 01's rows and are quoted only from 01) | on HOME, not reachable until migrated; the registry is in no batch | `ls -ld /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` |
| `/wsu/home/go/go24/go2432/FluoroCap/detect_v5z_final_best.pt` | HOME | the same detector file inside the FluoroCap tree | NOT RECORDED (as the row above) | on HOME, not reachable until migrated; inside the FluoroCap tree, which B09 moved (FINALIZED 2026-10-11, folder 10, section 2) | `ls -ld /wsu/home/go/go24/go2432/FluoroCap/detect_v5z_final_best.pt` |
| `/wsu/home/go/go24/go2432/model_registry/registry.jsonl` | HOME | the registry log that records the detector's sha on 2026-09-15 | NOT RECORDED (no catalog row) | on HOME, not reachable until migrated; in no batch | `head -c 200 /wsu/home/go/go24/go2432/model_registry/registry.jsonl` |

## 3. The roots of the superseded numbers (`MANIFEST_GRID.md` section 3; names only)

Every row is on HOME, not reachable until migrated. Only three are in a batch: `bench` and `ablate` are B13 and
`scaling` is B11 (`batch_items/B13.tsv`, `B11.tsv`; the state of both batches is folder 10, section 2). B13 lands under
`/rs/rs_grp_oschome/go2432/results/` (folder 10, section 2, row B13), not under `/rs/rs_grp_oschome/go2432/data/`;
job 40602926 opened that folder to approved students on 2026-10-12 (Greg, issue #72), and B13 was finalized the same
day (issue #68). Of `lstv_flag`, B11 moves only `renders`, `renders_verse`,
`renders_ctrl` and `smoke`, not the result files named below. The other rows are in no batch.

| path | volume | catalog row | what it was | status word | check line |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/tmp/ladder_summary.json` | HOME | C1.1 | the context ladder on the cervical-dominated `films_ann` bank; not found by a read-only `ls` at 01:25 UTC 2026-10-09 (`07_plain_film_level_id/MANIFEST_GRID.md`) | RECORD ONLY | `ls -ld /wsu/home/go/go24/go2432/tmp/ladder_summary.json` (expected to fail) |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json` | HOME | C1.2 | the recurrent head, job 40215812 (2026-09-13); the bank was `films_ann_fov96_ctx`, not `films_all2` | RECORD ONLY [WRONG-BANK]; attribution uncorrected (OQ F5) | `head -c 200 /wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json` |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent_all2.json` | HOME | C1.3 | the `films_all2` head | RECORD ONLY | `head -c 200 /wsu/home/go/go24/go2432/bench/xr_fov/recurrent_all2.json` |
| `/wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json` | HOME | C1.4 | whole-spine 27-class single crop on allspine_v2 | LEAKED (RECORD ONLY [LEAK]) | `head -c 200 /wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json` |
| `/wsu/home/go/go24/go2432/model_night/recurrent_allspine_v2.json` | HOME | C1.5 | the restored recurrent head on allspine_v2; job 40293790 | LEAKED (RECORD ONLY [LEAK]) | `head -c 200 /wsu/home/go/go24/go2432/model_night/recurrent_allspine_v2.json` |
| `/wsu/home/go/go24/go2432/model_night/stc/` | HOME | C1.7 | Star Temporal Classification against cross-entropy | REFUTED | `ls -ld /wsu/home/go/go24/go2432/model_night/stc` |
| `/wsu/home/go/go24/go2432/selective/SELECTIVE.md` | HOME | C1.8 | selective prediction; job 40291753 | LEAKED (NOT QUOTABLE [LEAK][SEL-REP]) | `head -c 200 /wsu/home/go/go24/go2432/selective/SELECTIVE.md` |
| `/wsu/home/go/go24/go2432/bench/robust/*.json` | HOME | C1.10 | the corruption suite on `films_all2` | RECORD ONLY | `ls -ld /wsu/home/go/go24/go2432/bench/robust` |
| `/wsu/home/go/go24/go2432/model_night/panel_stats/` | HOME | C1.11 | FluoroCap panel agreement with weak labels | NOT RECORDED (the catalog's status cell reads "not an accuracy") | `ls -ld /wsu/home/go/go24/go2432/model_night/panel_stats` |
| `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`, `LEARNING_CURVE.md`, `lstv_flag_labels_v2.csv` | HOME | C1.12, C1.13 | the 2-D LSTV / TLTV flags and their learning curve | REFUTED as a flag (C1.12); RECORD ONLY (C1.13) | `ls -ld /wsu/home/go/go24/go2432/lstv_flag/{LSTV_FLAG_RESULTS.md,LEARNING_CURVE.md,lstv_flag_labels_v2.csv}` |
| `/wsu/home/go/go24/go2432/model_night/interior_windows/` | HOME | C1.14 | the feasibility interior windows on v2 / v5 / v6; job 40321368 | LEAKED (RECORD ONLY [LEAK]) | `ls -ld /wsu/home/go/go24/go2432/model_night/interior_windows` |
| `/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` | HOME | C1.17 | the re-implemented competitor ensemble; whether the file exists is unknown (the 2026-10-08 listing of `/wsu/home/go/go24/go2432/model_night` was truncated) | NOT RECORDED (in any repository document) | `ls -ld /wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` |
| `/wsu/home/go/go24/go2432/model_night/scaling/SCALING_CURVE.json` and `/wsu/home/go/go24/go2432/scaling` | HOME | C2.1 | the 2026-09-17 synthetic / real fraction sweep on subsets of the v2 bank, and the subset banks | SUPERSEDED, LEAKED ([LEAK] [SEL-SPLIT]) | `ls -ld /wsu/home/go/go24/go2432/model_night/scaling/SCALING_CURVE.json /wsu/home/go/go24/go2432/scaling` |
| `/wsu/home/go/go24/go2432/allspine_v2` to `/wsu/home/go/go24/go2432/allspine_v5c` | HOME | C1.4, C1.5, C1.14, C2.1 | the leaked crop banks; deleted 2026-09-20 for quota (206.5 GB) | LEAKED | `ls -ld /wsu/home/go/go24/go2432/allspine_v2` (expected to fail) |
| `/wsu/home/go/go24/go2432/model_night/sweep_v3/` | HOME | C3.1 | the overlapping-exposure sweep on 120 held-out CTSP spines; job 40384843; owned by 01 as private history | RECORD ONLY (only sweep_v3 counts) | `ls -ld /wsu/home/go/go24/go2432/model_night/sweep_v3` |
| `/wsu/home/go/go24/go2432/ablate` | HOME | C5.1 | five arm directories of the CTSpinoPelvic1K nnU-Net ablations; which run wrote which directory is not recorded; owned by 03; 201.6 GB | NOT RECORDED (outcome never recorded, OQ B16) | `ls -ld /wsu/home/go/go24/go2432/ablate` |

## 4. Named only, never read, never copied (`MANIFEST_GRID.md` section 4)

These paths get no check line. They are never read, listed into a file, or copied.

| path | volume | what it holds | status word |
|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/private_ip` | Ceph | Greg's private records; 0.634 GB, 9 files | NOT RECORDED (no catalog row) |
| `/wsu/home/go/go24/go2432/.fluorocap/` | HOME | credentials, among them `/wsu/home/go/go24/go2432/.fluorocap/credentials.env`, from which the 2026-09-19 RSNA fetch took its Kaggle token; contents never read | NOT RECORDED (no catalog row) |
| `/wsu/home/go/go24/go2432/.hf_org_token`, `/wsu/home/go/go24/go2432/.hf_osc_token`, `/wsu/home/go/go24/go2432/.zenodo_token`, `/wsu/home/go/go24/go2432/.kaggle/`, `/wsu/home/go/go24/go2432/.netrc`, `/wsu/home/go/go24/go2432/github` | HOME | credential files; contents never read | NOT RECORDED (no catalog row) |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token`, `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/*.ica` | HOME | a token file and Cerner session files; contents never read | NOT RECORDED (no catalog row) |

`PLAN.md` section 6 (`../_plan/PLAN.md`) lists what Greg rotates.

## Terms

- **RSNA 2022 cervical archive.** Kaggle `rsna-2022-cervical-spine-fracture-detection`, held under the competition
  rules (login and acceptance of the rules; "non-commercial research and education only"), not under a data use
  agreement. Whether HPR 2026-269 covers it is not recorded (`docs/handoff/DATASET_USAGE.md` section 7, rows "terms"
  and "IRB"). The Kaggle token that fetched it is in a chat transcript and must be rotated (`DATASET_USAGE.md` section
  5; `TODO.md` step 2).
- **FluoroCap** is figures of published articles: 72.8 % of panels have zero pixel residual against the printed
  figure, so they are reproductions, not fluoroscopy. It is out of every training set by directive D1
  (`memory/data-directives-2026-09-23.md`; `CLAUDE.md` trap 3), a test set at most, and it stays private (root
  `CLAUDE.md` rule 8): readable on the grid does not mean it may be copied out or shown.
- **The names-only rows of section 4** (`/rs/rs_grp_oschome/go2432/private_ip` and the credential files) are never
  read or copied.
- For every other path above, the terms are not recorded in the folder.

## Access (Greg's facts of 2026-10-11)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students**: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- **On 2026-10-12 the VinDr and BUU items inside those folders opened too.** Until then the plan's `restricted` flag
  still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and
  BUU banks of B10 and B11, `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain folder including
  `multisource_banks`) open them (issue #65).
- **One path stays closed (owner-only):**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, whose one file is the
  annotator map, students' personal data rather than a dataset or a token (Greg, issue #69).
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` opened on 2026-10-12 without the token
  check (spinesurg-ct-nnunet 0ab783f; visibility job 40602925, issue #69).
- **Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students.** Items still there are moved
  to the Ceph volume by the data-platform plan, whose batch-by-batch state is folder 10, section 2. Every HOME row above
  is marked 'on HOME, not reachable until migrated'.

For this folder that means: the two Ceph paths under `/rs/rs_grp_oschome/go2432/data/` (the RSNA archive and the
FluoroCap landing folder) are readable by approved students; `/rs/rs_grp_oschome/go2432/private_ip` is not under
`data/`, is named only, and is never read; every HOME path is Greg's alone.

## Through Beethoven

The way in is Beethoven, the lab's Chrome extension. Install and use it per
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (the same pages are at
https://openspineconsortium.com/beethoven/). A reader needs a WSU AccessID with a grid account, the Google
Authenticator grid code, Claude Pro or Max, and Chrome on the invited Google account. Approved means a named ACL entry
`user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

The two access facts again, because every row above depends on them:

- every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (a named ACL entry on the
  volume root; other-read bits on folders and files), and since 2026-10-12 the VinDr and BUU items inside them and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`; one path stays closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (the annotator map,
  students' personal data);
- nothing on `/wsu/home/go/go24/go2432` is readable by students until the data-platform plan has moved it to Ceph.

Run the check lines above from the Beethoven worker. This folder submits no job (`CLAUDE.md`, "The standing rules").

## First experiment: none

This folder names no experiment. The first action is `TODO.md` step 15, a read: before any number from this folder is
written anywhere, find its row in `docs/handoff/RESULTS_CATALOG.md`; if its status is not CURRENT, do not write it.
`SUPERSEDED_NUMBERS.md` gives the replacement where one exists.

The one check with a number, run from the Beethoven worker:

```
ls -l /rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw/rsna_cspine
```

It shows 4 files whose sizes sum to 203,321,991,870 B (B08 STATUS row 001, as `MANIFEST_GRID.md` section 1 records it).
