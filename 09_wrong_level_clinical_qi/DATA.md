# DATA.md: the grid paths of this folder, reached through Beethoven

This file lists every path and item of `MANIFEST_GRID.md` sections 1 to 3, spelled as the manifest spells it, with its
volume, what it holds, its size and migration state as recorded, and one read-only check line per path. The access
facts are Greg's, dated 2026-10-11 (issue #15). Every number below restates `MANIFEST_GRID.md`, which names the file
each one comes from (the read-only grid pass of 2026-10-08 22:20 UTC, cited there as GRIDLS; the migration STATUS
files read in that pass; the data platform's `DATA_MANIFEST.md`, `MIGRATION_PLAN.md`, `plan/batch_items/B02.tsv` and
`B09.tsv` at `spinesurg-ct-nnunet` 097933a). Nothing was re-read on the grid for this file. Where a size or a fact is
in no file, this file writes "not recorded".

**Who reads this folder.** Greg only (`CLAUDE.md` "Reader": the QI manuscript describes invention aspects and stays
private until Greg confirms the provisional is filed). The review and the clinical paper may move to a student-safe
folder once Greg names the first author (`TODO.md` step 6). The access facts are recorded anyway, because they decide
which check lines an approved student could run if Greg hands any of this out, and which only Greg can.

**This folder owns no grid path.** The one computation it commissions, the v11 recompute of the iliac-crest
statistic, runs under `05_ct_morphometry_parity` (`MANIFEST_GRID.md` header; `_plan/PLAN.md` section 3, folder 09).

**How to run a check line.** Every check runs from the Beethoven worker (`../11_students_grid_access`), which runs
on a compute node (`../11_students_grid_access/docs/beethoven/extension_README.md`), never python or `du` on the
login node (`CLAUDE.md` rule 7). A directory gets
`ls -ld <path>`; a file gets `head -c 200 <file>`; an executable gets `ls -ld`, because `head` would print binary. A
check line written with `{a,b}` expands in bash and covers each member; the braces carry no spaces. A check on a path
recorded as absent is expected to answer "No such file or directory"; that answer is the check. In a student's shell
`~` is the student's own home (`docs/handoff/RECIPES.md` section 0 item 9), so every check line spells the path in
full. One exception to the read rule:
`/wsu/home/go/go24/go2432/.fluorocap/` holds credentials and gets `ls -ld` only, never `ls` of its contents, never
`head`.

**Volumes.** HOME = `/wsu/home/go/go24/go2432` (Panasas, 4,050.75 GB of a 4,294.97 GB soft limit on 2026-10-08).
Ceph = `/rs/rs_grp_oschome/go2432` (20 TB volume, `df-ceph oschome`). The review corpora of section 5 sit in neither:
they are in the laptop's WSL home (`MANIFEST_GRID.md` header and section 3).

## 1. Access on 2026-10-11 (Greg, issue #15)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- The one closed path is `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`.
  This folder uses nothing under it.
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students. Items still there are being
  moved to the Ceph volume by the data-platform plan (batches B05, B10, B11, B13 running on 2026-10-12). Every such
  item below is marked **on HOME, not reachable until migrated**; where no batch is recorded for an item, the mark
  says so. Greg runs those check lines until the batches land.
- Two Ceph paths of this folder sit outside `data/`: `/rs/rs_grp_oschome/go2432/model_night` and
  `/rs/rs_grp_oschome/go2432/tmp/fluorocap_audit/AUDIT.json`. The facts above speak of `data/` only, so whether a
  student can read these two is not recorded; the mode their check line prints settles it.

These facts are newer than this folder's handoff and supersede it where they disagree: `docs/handoff/RECIPES.md`
section 0 item 9, as of 2026-10-08, says `go2432/` below the Ceph gate "stays closed" to students and that
`publish_visibility.sh` keeps VinDr, BUU and every bank holding their pixels owner-only.

## 2. Through Beethoven

Beethoven is the way a student reaches these paths. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (pages at https://openspineconsortium.com/beethoven/).

A reader needs: a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and Chrome
on the invited Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`
(issue #15; `../11_students_grid_access/README.md`).

The two access facts again, because they decide what a check line can answer:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the
  volume root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements; the one closed path is
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`.
- Nothing on `/wsu/home/go/go24/go2432` is readable by students; items still there are marked **on HOME, not
  reachable until migrated** below, and Greg runs the HOME check lines until batches B05, B10, B11 and B13 land.

## 3. Grid paths this project uses (`MANIFEST_GRID.md` section 1)

| path (as the manifest spells it) | volume | holds | size and state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | Ceph, under `data/`: readable by approved students | the release v11 working copy: `ct/` (802), `labels/` (802, dated 2026-09-16), `labels_v10/` (802), `labels.zip` 883,912,953 B, `manifest.json` 1,100,037 B, `splits_5fold.json`, `dataset_labels.json`, `KNOWN_ISSUES.md`, `README.md`, `SHA256SUMS.txt`, `fetch_from_tcia.py`, `reconstruct_ct.py` | 196,195,055,488 B, 2,417 files (B02 STATUS); B02 cut over; VERIFIED 2,417 / 2,417 files, 200 sampled (B02 STATUS item 001) | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` |
| `labels/` of the row above, in full `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` (`CLAUDE.md` "Where things are") | Ceph, under `data/`: readable by approved students | the 802 v11 label volumes, dated 2026-09-16: the input of the first experiment (section 7) | inside the VERIFIED B02 copy; not sized on its own | `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` |
| `~/data/CTSpinoPelvic1K` (`docs/handoff/RECIPES.md` section 9 sets `D=~/data/CTSpinoPelvic1K`) | HOME | a symlink to the Ceph copy above (`MIGRATION_PLAN.md` B02; B02 STATUS "hard-link rsync rc=0") | already migrated; the symlink itself is on HOME and not reachable by students, its target (the Ceph row above) is, so a student sets `D` to the Ceph spelling instead | (Greg) `ls -ld /wsu/home/go/go24/go2432/data/CTSpinoPelvic1K`; it should print the arrow to the Ceph path |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` | HOME | the public repository's grid checkout: `master` at a0c5139 (GRIDLS `.git/refs/heads/master`; the laptop is at 7ddfe38); `morphometrics/` with 26 CSV / PNG files including `surgical_morphometrics.csv`, `transition_morphometrics.csv`, `pelvic_shape.csv`, `degenerative.csv`, `level_gradients.csv`, `castellvi_grades.csv`; `data/` remnants (`l6_audit.json`, `l6_truth.json`, `hip_crossover_*.json`); a `.token` file (38 B; never read; rotation list `_plan/PLAN.md` section 6) | not sized; listed only; not a migration item; **on HOME, not reachable until migrated** (no batch recorded); pull to 7ddfe38 before running anything | (Greg) `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K`; never `head` the `.token` |
| `morphometrics/` of the row above, in full `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/morphometrics` | HOME | the per-case CSVs the clinical paper's tables come from; `surgical_morphometrics.csv` carries `crest_above_l45_mm`, `crest_blocks_l45`, `crest_z_mm` and `rib12_to_crest_mm` (columns 12 to 14 and 57, `MANIFEST_CODE.md`) | not sized; **on HOME, not reachable until migrated** (no batch recorded); whether its CSVs were recomputed on v11 is not recorded (section 5) | (Greg) `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/morphometrics` |
| `/wsu/home/go/go24/go2432/model_night` and `/wsu/home/go/go24/go2432/model_night/count_walk` | HOME | SchwingNet experiment roots (directory dated 2026-09-22 17:29, GRIDLS line 922); `count_walk` is in the head of the `~/model_night` listing (GRIDLS line 2813); `tools/fiducial_walk.py` / `slurm/fiducial_walk.sh` wrote the fiducial-walk results to `~/model_night/fiducial/` and `count_walk/*/fiducial.json` (`spinesurg-ct-nnunet` `docs/CONTINUANCE_2026-09-19.md` lines 89 to 99) | not sized; batch not recorded (`~/model_night` was to stay on HOME while jobs ran, `memory/grid-ceph-volume-oschome.md`); **on HOME, not reachable until migrated** (no batch recorded); owned by `01_carm_level_detection`, read-only here | (Greg) `ls -ld /wsu/home/go/go24/go2432/model_night /wsu/home/go/go24/go2432/model_night/count_walk` |
| `~/model_night/fiducial/` | HOME | the source of "94.5 % of 950 walks" and "92.2 % of 7,405 walks" in `manuscripts/qi_universal_protocol/main.tex`; quoted only after 01's evaluation gate passes them (`CLAUDE.md` rule 5) | not seen: the `~/model_night` listing was truncated (`10_data_platform_grid`, grid manifest section 7), so whether it exists is not known; **on HOME, not reachable until migrated** (no batch recorded) | (Greg) `ls -ld /wsu/home/go/go24/go2432/model_night/fiducial` (either answer is news; record it) |
| `/rs/rs_grp_oschome/go2432/model_night` | Ceph, outside `data/` | the Ceph root for new SchwingNet experiment roots (GRIDLS line 1369) | not sized; exists; whether students can read it is not recorded (section 1) | `ls -ld /rs/rs_grp_oschome/go2432/model_night` (the mode shown settles it) |
| `/wsu/home/go/go24/go2432/FluoroCap` | HOME | the literature harvest FluoroCap: `releases/` (two releases, 2026-09-13), `articles.jsonl`, `captions_*.jsonl`, `annotate/`, `archives/`, `commons/`, `PROTOCOL.md`, `README.md`, the weights `anchor_det_v1.pt`, `anchor_det_c2_v1.pt`; `youtube/` 181.0 GB, `pdf/` 19.8 GB, `panels/` 4.7 GB, `raw/` 2.3 GB (`DATA_MANIFEST.md` FluoroCap card; GRIDLS); the parent harvest of the review's fluoroscopy arm and of the `fluorocap.py` search (`QUERY_EXTRA`, line 58) | 316.0 GB (`plan/batch_items/B09.tsv`); B09, flagged irreplaceable, candidate; copying at 22:20 UTC 2026-10-08 (job 40580673 per `_plan/PLAN.md` folder 10; no STATUS yet); B09's state on 2026-10-11 is not recorded (B09 is not among the four batches of section 1); **on HOME, not reachable until migrated** | (Greg) `ls -ld /wsu/home/go/go24/go2432/FluoroCap` |
| `/rs/rs_grp_oschome/go2432/data/fluorocap/raw/FluoroCap` (inside `$RS/data/fluorocap/raw`) | Ceph, under `data/`: readable by approved students once the copy is there | the B09 target of the row above | `$RS/data/fluorocap/raw` existed with one entry on 2026-10-08; whether the copy is complete is not recorded (no B09 STATUS) | `ls -ld /rs/rs_grp_oschome/go2432/data/fluorocap/raw /rs/rs_grp_oschome/go2432/data/fluorocap/raw/FluoroCap` (an absent or partial answer while B09 has not finished is admissible) |
| `/rs/rs_grp_oschome/go2432/tmp/fluorocap_audit/AUDIT.json` | Ceph `tmp/`, outside `data/` | the FluoroCap completeness audit written by job 40416374 (`DATA_MANIFEST.md` FluoroCap card, citing `docs/DATA_COMPLETENESS_AUDIT.md`); background for the review's "fluoroscopy corpus of 158,955 records" sentence (`PROTOCOL_...md` section 4) | not sized; whether students can read it is not recorded (section 1) | `head -c 200 /rs/rs_grp_oschome/go2432/tmp/fluorocap_audit/AUDIT.json` |
| `/wsu/home/go/go24/go2432/.fluorocap/` | HOME | the credentials file `credentials.env` that `review_abstracts.py` reads for the Semantic Scholar key (its docstring) | 1 directory, contents never read; `MIGRATION_PLAN.md` B09 says the credentials are not migrated; never reachable by students; rotation is Greg's (`_plan/PLAN.md` section 6) | (Greg) `ls -ld /wsu/home/go/go24/go2432/.fluorocap` only; never `ls` its contents, never `head`, never copy |
| `/wsu/home/go/go24/go2432/mambaforge/envs/spineps/bin/python` | HOME | the Python environment with nibabel and scipy used in jobs (`memory/no-jobs-on-login-node.md`) | not sized; **on HOME, not reachable until migrated** (no batch recorded); what python a student uses instead is not recorded | (Greg) `ls -ld /wsu/home/go/go24/go2432/mambaforge/envs/spineps/bin/python` (an executable: `ls -ld`, not `head`; never run it on the login node) |

Partition `reqp` with `--qos=requeue` for CPU work; `sbatch -D <dir>`; `afterany`; outputs to Ceph
(`MANIFEST_GRID.md` section 1; `docs/handoff/README.md` section 5 rule 7).

## 4. Grid paths with the same words that are NOT this project's (`MANIFEST_GRID.md` section 2)

Listed so that nobody reads them for this folder's review. Each belongs to the folder named.

| path (as the manifest spells it) | volume | what it is | belongs to | check, from the Beethoven worker |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/review_pack`, `review_pack_smoke`, `review_pack_v2` | HOME | 1,500 pseudo-labelled films for the level-review Space (`DATA_MANIFEST.md` line 18696); the level-review pack of the film programme, not this review | `07_plain_film_level_id` | **on HOME, not reachable until migrated** (no batch recorded in this folder); (Greg) `ls -ld /wsu/home/go/go24/go2432/{review_pack,review_pack_smoke,review_pack_v2}` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/panorama/review` | Ceph, under `data/`: readable by approved students | a screen-review folder of the PANORAMA collection (GRIDLS line 3155) | `06_transitional_ct_census` | `ls -ld /rs/rs_grp_oschome/go2432/data/anomaly_harvest/panorama/review` |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review`, `ctspinopelvic1k-review-triaged`, `spinesurg-ct-annotator.backup` | HOME | review Space material; may hold reviewer usernames: never copy (`10_data_platform_grid` grid manifest line 161) | `03_ctspinopelvic1k_dataset` | **on HOME, not reachable until migrated** (no batch recorded in this folder); (Greg) `ls -ld /wsu/home/go/go24/go2432/{CTSpinoPelvic1K-review,ctspinopelvic1k-review-triaged,spinesurg-ct-annotator.backup}`; never list or copy the contents |
| `spinesurg-ct-nnunet/spine_data_review/` (repository, not a grid path) | a folder of the private repository, not a volume | the PRISMA-ScR scoping review of public spine datasets: a different review | `10_data_platform_grid` | the grid checkout of that repository is `~/spinesurg-ct-nnunet` (`MANIFEST_CODE.md`), on HOME and not reachable by students (no batch recorded; the repository itself is private, root `../CLAUDE.md` rule 8); (Greg) `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/spine_data_review` (whether the grid checkout holds it at its commit is not recorded) |

## 5. Not on the grid, and remains to be put there (`MANIFEST_GRID.md` section 3)

The review's corpus and ledgers are in the laptop's WSL home, not on the grid (`CLAUDE.md` trap "The review's corpus
and ledgers are on the laptop"). `TODO.md` step 0 puts them on Ceph at a path `10_data_platform_grid` assigns under
`/rs/rs_grp_oschome/go2432/data/fluorocap/derived/`; its proposal is `review_wrong_level/`, which Greg has not
approved. From the Beethoven worker the only check is on that proposed target, and "No such file or directory" is the
expected answer until step 0 lands. Greg checks the laptop side in his WSL shell. Sizes are the laptop stat of
2026-10-08; the absolute laptop paths are in `MANIFEST_LOCAL.md`.

| item (as the manifest spells it) | volume | holds | size | check |
|---|---|---|---|---|
| the review's working folder `~/review/` | the laptop's WSL home | the review's working folder (directory mtime 2026-09-15 21:46, newest files 21:49: `REVIEW_STATS.json`, `REVIEW_STATS.md`); `screening.jsonl`, `abstracts.jsonl`, `extraction.jsonl`, `screening_titleonly.jsonl`, `screen_changes.csv`, `corpus_snapshot/` (the checksummed corpus copy, `MANIFEST.sha256`), `titleonly/`; `review_*.py` default to it (their docstrings); copied in part into `results/scoping_review/` (`MANIFEST_LOCAL.md`) | 93 MB (`du -sh`); `screening.jsonl` 15,979,944 B; `abstracts.jsonl` 17,913,689 B; `extraction.jsonl` 5,657,062 B; `screening_titleonly.jsonl` 12,280,009 B; `screen_changes.csv` 3,525,612 B; `corpus_snapshot/` 25 MB; `titleonly/` 15 MB | Beethoven worker: `ls -ld /rs/rs_grp_oschome/go2432/data/fluorocap/derived/review_wrong_level` (expect: no such file); laptop (Greg, WSL): `ls -ld ~/review` |
| the review's Europe PMC arm `~/FluoroCap_lstv/` | the laptop's WSL home | `articles.jsonl` (6,007 records), `passages.jsonl` (11,761 passages), `captions_matched.jsonl`, `raw/` (822 entries of panels: images), `raw_hires/` (540), `pdf_cache/`, `WRONG_LEVEL.md` and `.json` (copied here as `results/wrong_level_passages/`); dated 2026-09-15 22:13; `DATA_MANIFEST.md` line 18038: "the LSTV arm; it does not exist on the grid"; the images stay out of this repository | 1.6 GB; `articles.jsonl` 1,889,024 B; `passages.jsonl` 15,955,486 B | Beethoven worker: as `~/review/` above; laptop (Greg, WSL): `ls -ld ~/FluoroCap_lstv` |
| the review's Semantic Scholar arm `~/FluoroCap_s2/` | the laptop's WSL home | `s2_works.jsonl` (6,287 records), `passages.jsonl`, `pdf/`, `pdffig/` (452 entries: images), `pdffig_matched*.jsonl`; dated 2026-09-15 17:33; `DATA_MANIFEST.md` line 18878 | 3.6 GB; `s2_works.jsonl` 3,949,017 B; `passages.jsonl` 2,093,752 B | Beethoven worker: as `~/review/` above; laptop (Greg, WSL): `ls -ld ~/FluoroCap_s2` |
| `~/FluoroCap_lstv2/` | the laptop's WSL home | a second harvest round (`HARVEST_SUMMARY.md`, `openalex_works.jsonl`, `commons/`, `medpix/`, `openi/`, `pdffig/`); dated 2026-09-15 17:00; whether it feeds the review is not recorded | not sized | Beethoven worker: as `~/review/` above; laptop (Greg, WSL): `ls -ld ~/FluoroCap_lstv2` |
| human screening decisions and charting | nowhere | `validation_sample.csv` has 200 rows and an empty `human_decision` column; no charting table exists (`results/scoping_review/validation_sample.csv`; `REVIEW_STATS.md` first paragraph); `TODO.md` step 3 | 0 of 200; 0 of 1,933 | no grid path: nothing to check from the worker; the record is `results/scoping_review/validation_sample.csv` in this folder |
| the v11 iliac-crest recompute | not run | `transition_morphometrics.csv` and `pelvic_shape.csv` were written 2026-09-10 on v10 labels (`docs/handoff/RECIPES.md` section 9 item 3); `surgical_morphometrics.csv` was last committed at 2232bde 2026-09-11 "Withdraw the carved S1", and whether it was computed on the v11 tree is not recorded (`RESULTS_CATALOG.md` F.41, F.44); `TODO.md` step 1, under 05 (section 7) | 802 records | **on HOME, not reachable until migrated** (no batch recorded); (Greg) `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K/morphometrics/{surgical_morphometrics.csv,transition_morphometrics.csv,pelvic_shape.csv}` (an mtime after 2026-09-16, the date of the v11 `labels/`, is the first sign of a recompute, not proof of one) |
| the QI study's data | none exists | the protocol has not run; no IRB submission is recorded (`docs/handoff/MANUSCRIPTS.md` section 5; the determinations on file are in `01_carm_level_detection/regulatory/`); `TODO.md` steps 4 and 5, after 01 reaches S8 | 0 cases | no grid path: nothing to check |

## 6. Terms, where the folder records them

- **CTSpinoPelvic1K v11** (`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`): CC BY-NC-SA
  4.0 (issue #15; `docs/handoff/MANUSCRIPTS.md` section 6, the "data" row: v11 = 10.5281/zenodo.22797014, CC BY-NC-SA
  4.0; `docs/handoff/INFRASTRUCTURE.md` line 54: CTSpine1K and everything derived from it, CTSpinoPelvic1K included,
  is CC BY-NC-SA).
- **FluoroCap** (`/wsu/home/go/go24/go2432/FluoroCap` and its Ceph target): panels harvested from figures of
  published articles, 72.8 % of them reproductions (`docs/handoff/GLOSSARY.md` "FluoroCap"); out of training by
  directive D1 (`memory/data-directives-2026-09-23.md`; `docs/handoff/README.md` "DIR-D1"); a test set at most.
- **The Semantic Scholar key** in `/wsu/home/go/go24/go2432/.fluorocap/` is named only, never read, never copied,
  never echoed (`MANIFEST_GRID.md` section 1; `CLAUDE.md` rule 10).
- For every other path above, the terms are **not recorded in the folder**.

## 7. First experiment: the v11 recompute of the iliac-crest statistic (`TODO.md` step 1)

`TODO.md` step 1, run after `05_ct_morphometry_parity` step 3 (its v11 recompute of the pelvis-adjacent CSVs,
`RESULTS_CATALOG.md` F.44; 05's `TODO.md` row 15 names this crest recompute). It runs under 05, and like every piece
of this folder it starts only with Greg's go-ahead (`TODO.md` header; `docs/handoff/MANUSCRIPTS.md` section 21
item 8).

**What it replaces.** The v5-era 24.7 % (195 / 789) with the crest 12 mm or more above the L4-5 disc (catalog F.41,
SUPERSEDED-PENDING), and Table 1's crest at L4 in 87.1 % (Wilson 95 % 84.4 to 89.4) of the five-rib-free group,
n = 706, with the rest of Tables 1 and 2 (`STATUS.md` section 1). Both were computed before the v6 hip-laterality
corrections and before v11, and the crest is read from the hip labels, so nothing from them is quoted until this run
replaces them (`CLAUDE.md` trap "The iliac-crest number is v5-era").

**Input.** The v11 labels at `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels`
(802 volumes, Ceph, readable by approved students), with the release's `manifest.json` beside them. Set
`D=/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`, not the HOME symlink. Never the Hugging
Face mirror, whose labels are still v10 with identifier 29 (`docs/handoff/RECIPES.md` section 9 item 1).

**Code.** `CTSpinoPelvic1K` at 7ddfe38 (`MANIFEST_CODE.md`): `scripts/extract_surgical_morphometrics.py` (2232bde)
writes `crest_above_l45_mm` and `crest_blocks_l45`; the crest is the highest z of either hip label, the disc the
midpoint between the inferior extent of the L4 body and the superior extent of the L5 body, and positive means the
crest rises above the disc (`STATUS.md` section 1 "definition"). `scripts/extract_transition_morphometrics.py` writes
the rib-free count and the level the crest reaches, behind Tables 1 and 2. The grid checkout is at a0c5139 and is
pulled to 7ddfe38 first (`MANIFEST_GRID.md` section 1). The batch wrappers in `slurm/` still point at `data/v5_final`
and `-q primary` and are edited off both before reuse (`docs/handoff/RECIPES.md` section 9 item 3). Each extractor
takes `--labels`, `--manifest`, `--workers` and `--out` (same item); that `$D/manifest.json` is the file `--manifest`
expects is not recorded in this folder.

**The rules on the run** (`CLAUDE.md` rule 4):

- Names through `ostk.labels.labels_for(volume)`, never a fixed map. Whether the two extractors at 7ddfe38 already
  call `labels_for` is not recorded in this folder: read them before the run, and replace any fixed map first. An
  outside check on the result: on a v11 volume L4 resolves to 23, L5 to 24 and the hips to 30 and 31 (root
  `../CLAUDE.md` rule 4); any other answer means the legacy map, under which "femur_left" comes back T4.
- No code path gates on identifier 29, the carved S1, retired in v11 and dissolved into 26.
- Canonicalise to RAS to analyse (the CT volumes are stored P, I, R); never reorient when writing a label.
- Case ids go through `zfill(4)` before the per-case diff against the 2026-09-11 CSV (2232bde); the old CSVs were not
  zero-padded.

**The job** (`CLAUDE.md` rule 7). One `sbatch -D <dir>` job on `--partition=reqp --qos=requeue`, chained after 05's
step 3 with `--dependency=afterany:<id>`, never `afterok`; IPC under `/dev/shm`; outputs on Ceph under
`/rs/rs_grp_oschome/go2432/`, never HOME (which Ceph directory is not recorded in this folder). The recorded python is
`/wsu/home/go/go24/go2432/mambaforge/envs/spineps/bin/python`, on HOME, which a student cannot read; what python a
student uses instead is not recorded. The label-only extractors take 15 to 30 minutes at 20 workers
(`docs/handoff/RECIPES.md` section 9 item 3). Each extractor exits non-zero when a median leaves its published range
while still writing a good CSV, so the log's `*** N measure(s) outside the plausible range` line is read, not the exit
code (same item). Submit, estimate the wall time, write the job ids and the ETA down, stop.

**The tests, stated before the run** (`TODO.md` step 1; `CLAUDE.md` rule 6; the paper's "Analysis",
`manuscripts/iliac_crest/main.tex`). They are written down and hashed before the submit, and every output row carries
the hash (root `../CLAUDE.md` rule 6); a number produced before that is calibration.

1. The share of records with `crest_above_l45_mm` at or above +12 mm (`crest_blocks_l45`), with its Wilson 95 %
   interval, against the 24.7 % (195 / 789).
2. The level the crest reaches (L3, L4, L5) per rib-free group (four, five, six), each with a Wilson 95 % interval,
   as Table 1; the five-rib-free crest at L4 against 87.1 % (84.4 to 89.4).
3. Fisher's exact test on the direction of crest misplacement between the two routes to a count of four (lumbar rib
   present, no lumbar rib), as Table 2, labelled post hoc as the paper labels it.
4. The outside check: the spread of `crest_above_l45_mm` (its SD and range, not its median) against the widest
   published living-cohort spread. Which published series that is, is not recorded in this folder (`STATUS.md`
   section 1, last paragraph: the iliac-crest tangent sign on MRI is the one entry); it is chosen from the literature
   and written down before the run, never tuned to the result.
5. The denominator: the v5 figure counts 789 of 802 records, and why 13 fall out is not recorded in this folder. The
   v11 run states its denominator and writes a reason for every record it leaves out
   (`memory/no-unexplained-subsets-fix-not-disclose.md`).

**The gate** (`TODO.md` step 1). The 24.7 % and Tables 1 and 2 are replaced by v11 numbers with their CSV and job id,
or the paper is withdrawn from the queue; a before-and-after diff per case is written; no case moves group without a
rendered mask. Engineering runs it; Greg reads the diff. It depends on 05's step 3, on `04_openspinetoolkit` CT-1 (the
S1 fallback and the canal regression, `RESULTS_CATALOG.md` G.2, G.3) if any ostk column is used, and on the wrappers
edited off `data/v5_final`.

## 8. Not recorded

The state of any grid path after 2026-10-08 beyond the access facts of 2026-10-11 (section 1); the outcome of batches
B05, B10, B11 and B13 said to run on 2026-10-12, and B09's state on 2026-10-11 (no STATUS for any of them is in this
folder); whether students can read the two Ceph paths outside `data/` (`/rs/rs_grp_oschome/go2432/model_night`,
`/rs/rs_grp_oschome/go2432/tmp/fluorocap_audit/AUDIT.json`); whether `/wsu/home/go/go24/go2432/model_night/fiducial`
exists; the sizes marked "not sized" above; whether `surgical_morphometrics.csv` at 2232bde was computed on v11 labels
(05's `MANIFEST_GRID.md` section 2 records a `surgical_morphometrics.csv` in the v11 build workspace, written under job
40198880 "v11_morph"; whether it is the committed file is not recorded here); whether the extractors at 7ddfe38 call
`labels_for`; the Ceph output directory of the recompute; what python a student uses; how a student puts a checkout of
`CTSpinoPelvic1K` at 7ddfe38 on the grid; which published series sets the spread check; why the v5 figure counts 789
of 802 records; the Ceph path of the review corpora (Greg approves it, `TODO.md` step 0); whether `~/FluoroCap_lstv2`
feeds the review; the terms of every path section 6 does not name.
