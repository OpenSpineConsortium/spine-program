# DATA — reaching this project's grid data through Beethoven, and the first experiment

Written 2026-10-11 for issue #8. The paths below are `MANIFEST_GRID.md` sections 1 to 5, spelled as the manifest spells
them (its sources are the one read-only grid pass of 2026-10-08 22:20 UTC and the migration STATUS files; every size and
count below comes from that manifest). The access facts are Greg's, dated 2026-10-11, given in issue #8; where they and an
older recorded statement disagree, both are shown with their dates. What no file records is written "not recorded".

Reader: this folder is student-safe; Greg answered the reader split (`CLAUDE.md` first paragraph;
`docs/handoff/OPEN_QUESTIONS.md` A29) on 2026-10-12: every Write holder may read all 13 folders (issue #68).

Conventions. `HOME` = `/wsu/home/go/go24/go2432` (Greg's home directory, the Panasas volume, 4.3 TB soft quota);
`RS` = `/rs/rs_grp_oschome/go2432` (the Ceph volume, CephFS, 20 TB, group `oschome`) (`MANIFEST_GRID.md` header). In a
student's shell `~` expands to the student's own HOME, so every check line writes the full path
(`docs/handoff/RECIPES.md` section 0 item 9). Every check line is read-only (`ls -ld` for a directory,
`head -c 200` for a file) and runs **from the Beethoven worker**, which is a batch job on a compute node
(`../11_students_grid_access/docs/beethoven/extension_README.md`) — never python, and never anything on the login node
warrior, which kills python, node, pip, md5sum, rsync, conda and others by name (`CLAUDE.md` rule 7;
`docs/handoff/RECIPES.md` section 0 item 1). A check marked **(Greg only)** names a HOME
path, which the 2026-10-11 access facts leave unreadable to students: the expected result of a student's check there is a
refusal, and the item is marked **on HOME, not reachable until migrated**.

## 1. The release this project measures — `MANIFEST_GRID.md` section 1

- `HOME/data/CTSpinoPelvic1K` -> `RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` — Ceph (the HOME spelling became a
  symlink to the Ceph copy on 2026-10-08 08:11; its twin `HOME/data/CTSpinoPelvic1K.pre-ceph`, 2026-09-16, went with
  B02's FINALIZE of 2026-10-11, `../10_data_platform_grid/MANIFEST_GRID.md` section 2). Release v11: `labels/` 802 files (2026-09-16 09:21), `labels_v10/` 802 (2026-09-07), `ct/` 802 (2026-09-23
  03:03, after the 0533 repair), `labels.zip` 883,912,953 B, `manifest.json` 1,100,037 B, `splits_5fold.json` 247,222 B,
  `dataset_labels.json` (v11, 2026-09-11), `dataset_labels_v10.json`, `SHA256SUMS.txt` 73,633 B, `KNOWN_ISSUES.md`,
  `README.md`, `fetch_from_tcia.py`, `reconstruct_ct.py`. VERIFIED: B02 item 001, `VERIFY_OK`, 2,417 / 2,417 files,
  196,195,055,488 / 196,195,055,488 B. A student reads the Ceph spelling; the HOME symlink is on HOME.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` — a readable directory.
- `HOME/CTSpinoPelvic1K` — HOME (Panasas). The git clone of CTSpinoPelvic1K, `master` at a0c5139 (2026-09-07) with 133
  dirty status lines; `scripts/` line-identical to the laptop for `extract_transition_morphometrics.py`,
  `measure_sacral_ala.py`, `measure_tp_height.py`; `extract_level_gradients.py` differs (430 vs 423 lines) and must not
  be imported from there. 1,945.6 GB for the whole tree including `data/`; its `data/` subtree moves in batch B02, whose
  items 002-024, 026 and 030 read ABSENT at the 2026-10-08 pass (items 025 and 027-029 VERIFIED).
  **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K` — a directory; a student's `ls` is refused.
- `HOME/CTSpinoPelvic1K/morphometrics` — HOME (Panasas). The committed tables plus files not in the laptop copy
  (`fig_anatomical_report.png`, `fig_foramina_sweep.png`, `fig_transition_landscape.png`, `foramina_param_sweep.csv`; no
  `label_census_v11.csv` there); not sized. Whether `pelvic_shape.csv`, `transition_morphometrics.csv`,
  `degenerative.csv` were recomputed on v11 here is not shown (`docs/handoff/OPEN_QUESTIONS.md` B27): read the mtimes
  with `ls -l` first. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/morphometrics` — a directory.

## 2. What this project produced on the grid — `MANIFEST_GRID.md` section 2

- `RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` — Ceph. The 2026-09-10 spinopelvic and pedicle-width
  scratch: `ostk_level_morphometry.csv` (302,994 B; the ostk per-level run at commit 90a27a7, before the regression),
  `pi_ostk2.csv` (662 B), `pdw_why.py` (1,761 B), `pitest/` (13,899,387 B; 10 release label copies), `pdwtest/`
  (2,710,749 B; 2); what `pitest` and `pdwtest` stand for is not recorded. VERIFIED: B14 items 003-007, `VERIFY_OK`,
  bytes matched, every file sampled; cut over 2026-10-08 11:02, with the HOME-root symlinks
  `~/ostk_level_morphometry.csv`, `~/pi_ostk2.csv`, `~/pdw_why.py`, `~/pitest`, `~/pdwtest` pointing here.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10` — a readable
  directory holding those five entries.
- `HOME/spinopelvic_all.csv` — HOME (Panasas). The spinopelvic table of 2026-09-10 13:27; 63,562 B; a family-E entry of
  `DATA_MANIFEST.md` line 628, in no batch item file. **On HOME, not reachable until migrated** (no batch is recorded
  for it in this folder).
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/spinopelvic_all.csv` — the CSV header.
- `HOME/agg_spinopelvic.py` 4,259 B, `show_pi.py` 276 B, `ss_probe.py` 2,671 B, `disc_probe.py` 1,873 B,
  `disc_probe2.py` 2,955 B, `height_probe.py` 5,198 B, `cmp_pdw.py` 1,480 B, `lm_probe.py` 762 B (all 2026-09-10) —
  HOME (Panasas), at the HOME root. The spinopelvic estimator probe scripts; in no repository as far as recorded;
  not scheduled in any batch. Whether `~/height_probe.py` equals the tracked `scripts/height_probe.py` is not recorded.
  **On HOME, not reachable until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/agg_spinopelvic.py` — python source; the same line, with its
  name, checks each of the other seven.
- `HOME/ostk.tgz` (2026-09-10 04:10; 186,470 B), `HOME/ostk_run/` (06:03; a second scratch copy of OpenSpineToolkit),
  `HOME/ostk_shards/` (12:26; 12 entries), `HOME/ostk_morph_out/` (04:11) — HOME (Panasas). The 2026-09-10 shard run of
  per-level morphometry and pedicle width: the run whose `PDW` column came back empty
  (`docs/handoff/OPEN_QUESTIONS.md` D2); folders not sized; family-E entries, no batch; role beyond the names not
  recorded. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/ostk_run /wsu/home/go/go24/go2432/ostk_shards
  /wsu/home/go/go24/go2432/ostk_morph_out` — directories; `head -c 200 /wsu/home/go/go24/go2432/ostk.tgz` — gzip bytes
  (a read check only).
- `HOME/logs_ostkmorph_40183643.{out,err}` (11,438 B / 0 B), `logs_ostkmorph_40183680.{out,err}` (32 B / 81 B);
  `logs_ostkext_40183713_*` (96 files), `logs_peddev_*` (20), `logs_pedbatch_*` (2), `logs_rheight_*` (2) — HOME
  (Panasas), at the HOME root. The job logs of that day; small. **On HOME, not reachable until migrated.**
  Check (Greg only): `head -c 200 /wsu/home/go/go24/go2432/logs_ostkmorph_40183643.out` — log text.
- `HOME/height_renders/` (2026-09-10 03:25), `HOME/ped_renders/` (04:42) — HOME (Panasas). The body-height renders
  behind `docs/BODY_HEIGHT_INVESTIGATION.md` and the pedicle renders; not sized. Batch B10 moves them to
  `RS/data/ctspinopelvic1k/derived/height_renders` and `.../ped_renders`; at the 2026-10-08 pass
  `RS/data/ctspinopelvic1k/derived` did not exist (B10 not run); B10's state since is
  `../10_data_platform_grid/MANIFEST_GRID.md` section 2 (finalized 2026-10-12). **On HOME, not reachable until
  migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/height_renders /wsu/home/go/go24/go2432/ped_renders`; with B10
  finalized, a student's check is `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/derived/height_renders`.
- `RS/data/ctspinopelvic1k_build_tree/derived/s1v11/` — Ceph. The v11 build workspace (2026-09-11 to 18): the build and
  audit script copies, the logs of jobs 40198228 (s1_v11), 40198880 (v11_morph), 40309073 (verify_v11), 40309160
  (package_v11), `out/v11_labels`, `out/s1_carve_audit.csv`, `morphometrics/surgical_morphometrics.csv`,
  `out/dataset_labels_v11.json`, and the Zenodo v11 upload scripts and state. 835 files, 1,189,924,200 B. VERIFIED: B14
  item 008, sampled 200; irreplaceable. Owner-only (`drwx--S---`) when read on 2026-10-12 (issue #65); **readable by
  approved students since visibility job 40602925 of 2026-10-12**, opened without the token check (Greg, issue #69;
  see Terms).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` — a readable directory.
- `RS/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` — Ceph. Pelvis-propagation QC renders (03's; listed
  because it sits beside the scratch); 196,147,947 B. VERIFIED: B14 item 001.
  Check: `head -c 200 /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` — gzip
  bytes (a read check only).

## 3. Reader E — `MANIFEST_GRID.md` section 3

- `RS/data/or_ready/auto_reference/readerE/` — Ceph (Ceph-native, made under `RS`; no migration). J0 (60 CT-segmenter
  pairs), J0bis, J1 (`j1/_collect/features_j1.csv` 38,432 instance rows, `features_index.csv` 3,524 pairs),
  `j1v3/_collect/` (the features v3 rerun), `j2/mask_bits_j1.csv.gz`; made by jobs 40438613, 40438806, 40438897,
  40443093, 40443305-08, 40443310, 40448877. `features_j1.csv` is 40,334,008 B on the laptop copy; the rest not sized.
  Fetch `features_j1.csv` only after its J2 gate passes (`TODO.md` step 4).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE` — a readable directory.
- `RS/data/or_ready/auto_reference/lists/{ctsp,verse,ts12,cobra_ct,cobra_cbct,carmlspine}.csv`; `readerC/<corpus>/json/`;
  `readersAB/{a,b}/<corpus>/<case>.json` — Ceph (Ceph-native). Reader E's inputs: the CT and mask lists, reader C's
  calls, readers A/B's guard records; not sized.
  Check: `head -c 200 /rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/lists/ctsp.csv` — the list's CSV header.
- `RS/data/spineps/ctsp/CTSP_<case>_{seg-vert_msk,seg-spine_msk}.nii.gz` + `_ctd.json` (801 masks);
  `RS/data/spineps/ctd_relabel/bench_ts_native/VERSE_<cid>_*`; `HOME/bench/spineps/native_ctd/COLONOG_<n>_*` (796) —
  the first two Ceph, the third HOME (Panasas). The SPINEPS post-fix stores: the corpus (subregion) label CT-5 needs;
  **every id passes `tools/spineps_ids.py assert_verse_monotonic` before any read** (see Terms); not sized; owned by 10
  and 06. The COLONOG part is **on HOME, not reachable until migrated** (which batch moves it is not recorded in this
  folder).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/spineps/ctsp` — a readable directory; (Greg only)
  `ls -ld /wsu/home/go/go24/go2432/bench/spineps/native_ctd`.
- `HOME/bench/totalsegmentator/native/COLONOG_<n>.nii.gz` (804) + `class_map.json`;
  `RS/data/anomaly_harvest/verse/ts/<cid>.nii.gz` + `class_map.json` — the first HOME (Panasas), the second Ceph.
  TotalSegmentator v2 `total` outputs; the COLONOG number is not the case id (map in `tools/rib_count_ts_prep.py`); TS
  `sacrum` and `vertebrae_S1` are disjoint; not sized; owned by 10. The HOME part is **on HOME, not reachable until
  migrated** (no batch recorded in this folder).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/anomaly_harvest/verse/ts` — a readable directory; (Greg only)
  `ls -ld /wsu/home/go/go24/go2432/bench/totalsegmentator/native`.
- `HOME/VerSeFusion/data/unified/scan-<cid>/scan-<cid>_{ct,msk}.nii.gz` — HOME (Panasas). VerSeFusion expert masks
  (VerSe alphabet, no sacrum id); 139.0 GB raw (listing 2026-05-13). Batch B06: `RS/data/versefusion/raw/VerSeFusion_data`
  exists (2026-10-08 07:18), and B06 was finalized on 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md`
  section 2). **On HOME, not reachable until migrated** (the raw Ceph copy is the readable one).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` — a readable directory; (Greg only)
  `ls -ld /wsu/home/go/go24/go2432/VerSeFusion/data/unified`.

## 4. VerSeFusion measurement derivatives — `MANIFEST_GRID.md` section 4

- `RS/data/versefusion/derived/vf_v10/` — Ceph. `vf_813` relabelled to the CTSP v10 ids for measurement; regenerable;
  v10 ids include 29, so any sacral column from it needs the v11 semantics; 374 files, 319,212,368 B. VERIFIED: B06 item
  014, 374 / 374 files, bytes matched. `HOME/vf_v10` is a symlink here since 2026-10-08 12:35; `HOME/vf_v10.pre-ceph`
  went with B06's FINALIZE of 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md` section 2).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_v10` — a readable directory.
- `HOME/vf_morphometrics/` — HOME (Panasas). VerSeFusion morphometrics output (mtime 2026-09-12); not sized; batch not
  recorded in what the 2026-10-08 pass read. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/vf_morphometrics` — a directory.

## 5. Code on the grid that this project calls — `MANIFEST_GRID.md` section 5

- `HOME/OpenSpineToolkit/` — HOME (Panasas). An rsync copy of ostk with no `.git` (commit unknown; whether the 1b7005c
  regression is in it is `docs/handoff/OPEN_QUESTIONS.md` B29); not installed in the spineps env — the pattern is
  `export PYTHONPATH=$HOME/OpenSpineToolkit:$HOME/spinesurg-ct-nnunet/tools${PYTHONPATH:+:$PYTHONPATH}`. Refresh from
  OpenSpineToolkit `main` after 04's fix; never trust its VBHp / EPD until then. **On HOME, not reachable until
  migrated** (no batch recorded in this folder).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/OpenSpineToolkit` — a directory.
- `HOME/spinesurg-ct-nnunet/` — HOME (Panasas). The private repository's grid checkout: git, branch `L6_Class`, at
  `c0b752a4` on 2026-09-24 (three commits behind the laptop then); ship by commit, push and `git pull --ff-only`, never
  scp. The reader E tools and `tools/spineps_ids.py` run from here. **On HOME, not reachable until migrated** (and the
  repository itself stays private, `CLAUDE.md` rule 8).
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet` — a directory.

## Terms

- The release is **CTSpinoPelvic1K v11, CC BY-NC-SA 4.0** (issue #8; `docs/handoff/INFRASTRUCTURE.md` line 54:
  CTSpine1K and everything derived from it, CTSpinoPelvic1K included, is CC BY-NC-SA; Zenodo 10.5281/zenodo.22797014,
  `README.md` "What this is").
- **`s1v11` is open**: owner-only `drwx--S---` when read on 2026-10-12 (issue #65), it was opened to approved students
  the same day without the token check, by Greg's decision (visibility job 40602925, issue #69).
- **The Ljubljana specimen of `TODO.md` step 4 is read-only under its ND licence** (issue #8; `TODO.md` step 4 names it
  as an n-1 check at gold pose, read-only under its ND licence; the specimen is the PIXIUM 4600 cadaver, 18 frames, one
  cadaver L1-L5, parameters only, `docs/handoff/DATASET_USAGE.md` section 2.3 and `docs/handoff/GLOSSARY.md`).
- Any other terms question is **not recorded in the folder**.
- **SPINEPS ids pass `tools/spineps_ids.py assert_verse_monotonic` before any read** (`MANIFEST_GRID.md` section 3; the
  guard is `spinesurg-ct-nnunet` 097933a `tools/spineps_ids.py`, `assert_verse_monotonic` at line 394,
  `MANIFEST_CODE.md`).

## Access — Greg's facts of 2026-10-11 (issue #8)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** (a named ACL entry on the
  volume root; other-read bits on folders and files), **including** `vindr_spinexr`, `buu_lspine_3600`,
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
  **Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students**; items still there are moved
  to the Ceph volume by the data-platform plan, whose batch-by-batch state is `../10_data_platform_grid/MANIFEST_GRID.md`
  section 2, and every such item above is marked "on HOME, not reachable until migrated".

These facts are newer than this folder's records and supersede `docs/handoff/RECIPES.md` section 0 item 9 where they
disagree (it says, as of 2026-10-08, that `go2432/` below the Ceph gate "stays closed" to students and that
`publish_visibility.sh` keeps VinDr, BUU and every bank holding their pixels owner-only).

## Through Beethoven

A student reaches the readable paths above from the Beethoven worker. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md`; the published pages are at
https://openspineconsortium.com/beethoven/ (issue #8).

A student needs: a WSU AccessID with a grid account, the Google Authenticator grid code, a Claude Pro or Max
subscription, and Chrome on the invited Google account (`../11_students_grid_access/README.md`; issue #8). **Approved**
means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome` (issue #8;
`../11_students_grid_access/README.md` "approval = `user:<AccessID>:rwx` on the root").

The two access facts, repeated: every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by an approved student
(the named ACL entry on the volume root; other-read bits on folders and files), including the VinDr and BUU folders,
because every approved student holds the PhysioNet credential and the VinDr and BUU agreements, and since 2026-10-12
the VinDr and BUU items inside them and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`;
one path stays closed, `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (the
annotator map, students' personal data); and nothing on `/wsu/home/go/go24/go2432` is readable by students until the data-platform
batches move it to Ceph.

## First experiment: PAR-1, the ratio-only single-vertebra separability test

The first experiment is `TODO.md` step 1, PAR-1: **laptop only, about one hour** (`CLAUDE.md` "The goal in one
paragraph"). Nothing in it touches the grid: the input CSV is already in this folder and the script is in the public
repository.

**Input.** `results/morphometrics/level_gradients.csv` — the committed copy from CTSpinoPelvic1K 7ddfe38; per-level
heights, widths and process span; bit-for-bit identical across v10 and v11 (`MANIFEST_CODE.md`).

**Code.** `scripts/test_morphometric_separability.py` in the `CTSpinoPelvic1K` repository at master **7ddfe38**
(`MANIFEST_CODE.md`: `osc` = github.com/OpenSpineConsortium/CTSpinoPelvic1K, the remote the paper cites; `origin` =
github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K; public). A student clones the public repository to their laptop.

**Step 1 — reproduce F.28.** Run the script **unchanged** on `results/morphometrics/level_gradients.csv`. The number to
reproduce is the 2026-10-08 laptop rerun of F.28: **T12 against L1, AUC 0.990, accuracy 0.972, on 1,486 vertebrae from
798 cases** (issue #8; `STATUS.md` F.28). The catalog row reads AUC 0.990, accuracy 97.3 % over 1,485 vertebrae
(`docs/handoff/RESULTS_CATALOG.md` F.28); the one-row difference between 1,485 and 1,486 is explained by no file
(`STATUS.md` F.28). The largest standardised weights of the rerun, for comparison: `tp_span/case_median` -1.851,
`tp_span/body_height` -1.184, `body_height/case_median` -1.012 (`STATUS.md` F.28); the dominant feature is the
transverse-process span.

**Step 2 — the ratio-only variant.** Copy the script to a variant that **drops the five case-median features and keeps
the six between-measure ratios**; T12 against L1 on the same CSV, grouped five-fold by case, seed 0, as the original
(`TODO.md` step 1a; `MANIFEST_CODE.md`). The variant's result is on disk nowhere — no ratio-only single-vertebra
separability result exists anywhere (`STATUS.md` "PAR-1" row; `MANIFEST_GRID.md` section 6) — so whoever runs this
writes the first number.

**The pre-stated gate** (`TODO.md` step 1, written before the run):

- **AUC at or above 0.95**: a single-vertebra 3-D target exists and PAR-2 inherits the feature list.
- 0.90 to 0.95: the target is one body plus one neighbour.
- Below 0.90: the parity target is a window of three or more bodies, and the 2-D one-body number (74.8 %, A3.3) is
  compared to a window number, never to 0.990.
- The bootstrap interval at n 1,486 is about +/- 0.006 (`TODO.md` step 1).

**Outside check** (never skipped, `CLAUDE.md` rule 3): the sign of every ratio's weight against the Panjabi 1991 Table 3
per-level means (`results/morphometrics/panjabi_reference.csv`, `results/morphometrics/level_references.csv`), and the
dominant weight must stay on the transverse-process span or the variant has changed the question (`TODO.md` step 1).

Parts (b) and (c) of the same step — the seven-level shape model on the 643 ordinary records, and L6 against ordinary L5
on the ostk rows with its leave-one-case-out design and renders — are specified in `TODO.md` step 1 and follow after the
two runs above.
