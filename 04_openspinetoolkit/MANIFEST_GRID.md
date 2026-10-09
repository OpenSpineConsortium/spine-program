# MANIFEST_GRID.md: every grid path this project uses or produced

HOME = `/wsu/home/go/go24/go2432` (Panasas; 4.3 TB soft quota, 4,050.75 GB used at 2026-10-08 22:20 UTC per
`pan_quota`). Ceph = `/rs/rs_grp_oschome/go2432` (20 TB volume, 7 TB used, 39.39 %, `df-ceph`). Sources:
the read-only listing of 2026-10-08 22:20 UTC (`../10_data_platform_grid`), a second read-only pass for
this folder on 2026-10-09 00:12 UTC (`ls`, `stat`, `cat` of small files through `wsl -e bash -lc 'ssh grid
...'`; the raw output is `results/grid_run_2026-09-10/grid_listing_2026-10-09T0012Z.txt`), the handoff
inventory of grid paths, and `spinesurg-ct-nnunet/data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md`,
`plan/batch_items/B14.tsv`, `dedup/HASH_RESULTS.md` at 097933a, and the batch run record
`/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/B14/STATUS` (grid HOME clone only: the laptop
clone at 097933a has no `plan/runs/`; read 2026-10-08 22:20 UTC in `../10_data_platform_grid`'s listing,
`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`). "Verified" means a listing or a read on the
date given; "not sized" means no census file records a size. Nothing was written on the grid.

## 1. The toolkit on the grid

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| HOME`/OpenSpineToolkit` | an rsync copy of ostk with no `.git`: `ostk/` (19 `.py` files, `README.md`, `__pycache__/`) and `pyproject.toml` (1,945 B, 2026-08-06). `ostk/vertebral_body.py` 43,929 B, 2026-09-10 22:11, equals commit 1b7005c line for line after CRLF normalisation (sha256 of the LF text b6221243cd16e4a2...; it has the 2 mm ring closing at line 130 and `min_vox: int = 20` on the `def` line 98; cb43197 has the same numbering) and lacks only cb43197's 3-line fix (lines 453-454 and 830 replaced in place); `labels.py` 7,722 B, `spine.py` 26,904 B and `genant.py` 10,177 B (2026-09-11) are LF and equal cb43197's blobs byte for byte; `morphometry.py` 20,271 B is CRLF and equals cb43197's text after normalisation (blob 19,859 B; the difference is its 412 lines); `surgery.py` 37,631 B was not read, and its size is cb43197's 36,948 B blob plus 683 line endings, so it is CRLF too; of the six sized files three are CRLF (`vertebral_body.py`, `morphometry.py`, `surgery.py`) and three LF; `tests/`, `projects/`, `tools/`, `SPEC.md`, `README.md`, `CLAUDE.md` absent. No `COMMIT.txt`. | about 1.5 MB (`ls` block count); not in any census | HOME; not in a migration batch; stays on HOME (code, small) | 2026-10-09 00:12 UTC (listing + `cat` + local hash). **Answers handoff `OPEN_QUESTIONS.md` B29: the canal-closing regression is in the grid copy.** |
| HOME`/ostk.tgz` | an ostk tarball of 2026-09-10 04:10:58; contents not read | 186,470 B | HOME; deletion candidate once step 5 is done | `stat` 2026-10-09 |
| HOME`/ostk_run/` | the work directory of the 2026-09-10 shard run: `ostk_extract.py` (2,751 B, 03:41; the per-level extractor whose 24 shards became the committed CSV), `ostk_morph.py` (4,775 B, 03:01; the 60-case Panjabi check), `ped_batch.py` (2,228 B, 06:02), `pedicle_dev.py` (10,796 B, 05:59; `isthmus_width`, the erosion-neck development function), `edge_probe.py` (6,138 B, 03:28), `render_height.py` (6,825 B, 03:15), `__pycache__/`, and a nested `OpenSpineToolkit/` copy (dir 04:11; its `ostk/morphometry.py` is 15,044 B dated 07:28 = commit db4db40's text, sha256 e6623025958e3fa5...; `vertebral_body.py` 42,838 B dated 2026-08-05, matching no commit hash computed here; other files dated up to 12:25). The copies of the four scripts that matter are in `code/grid_ostk_run_2026-09-10/`. | small; not sized | HOME root; role now recorded (it was "unknown 10" of the grid inventory) | 2026-10-09 (listing; four scripts and `morphometry.py` read) |
| HOME`/ostk_shards/` | `in_0` ... `in_7`: eight folders of symlinks into HOME`/data/CTSpinoPelvic1K/labels/` (100-101 links each, made 2026-09-10 12:26; no data duplicated); `mout/morph_0..7.csv` (8 files, 40,724-42,498 B, 13:18-14:28; the `morph` CLI's wide format, 100 cases per file, pedicle keys landing as `<level>_l` and stray `L3_r`, `L3_mean`); `out/spinopelvic_0..7.csv` (8 files, 7,196-7,873 B, 12:52-13:25; PI/SS/PT/LL per case, 101 cases per file) | small | HOME root | 2026-10-09 (listing; `in_0` head, `morph_6.csv` and `spinopelvic_0.csv` read) |
| HOME`/ostk_morph_out/` | `shard_0..23.csv` (24 files, 12,307-13,242 B, 2026-09-10 04:52-05:10), long format `case, level, ...PDW_l, PDW_r, PDW, plate_rms_mm`; their sum is 304,811 B; the shards are CRLF (Python `csv.writer`'s default) with a 79-byte header line, and 304,811 minus 23 repeated headers of 79 B = 302,994 B, the Ceph `ostk_level_morphometry.csv` exactly; the blob committed as CTSpinoPelvic1K 90a27a7 is 298,249 B, the same 4,745 lines stored with LF (302,994 minus 4,745); PDW empty in every row read (`shard_0.csv`: 200 rows, 0 non-empty) | 302 KB | HOME root | 2026-10-09 (listing; `shard_0.csv` read) |
| HOME`/logs_ostkext_40183713_{0..23}.{out,err}` | the first shard attempt (03:42); every `.err` says job 40183715 was cancelled at 03:58:24; `.out` "shard 0/24: 34 case(s)" | 48 files of 23-81 B | HOME root; deletion candidates | 2026-10-09 (`_0` read) |
| HOME`/logs_ostkmorph_40183643.{out,err}` | the 60-case check of 03:06-03:17: every case failed with "matmul: ... size 3 is different from N" (the bug commit 9091e36 fixed at 03:18:37); its tables print n = 0 at every level; copied to `results/grid_run_2026-09-10/` | 11,438 B + 0 B | HOME root | 2026-10-09 (read) |
| HOME`/logs_ostkmorph_40183680.{out,err}` | the rerun of 03:34, cancelled at 03:44:42 after "10/60" | 32 B + 81 B | HOME root | 2026-10-09 (read) |
| HOME`/logs_rheight_40183679.out` | 03:20-03:25: twelve posterior-height renders written (`0001_L1_height.png` ... `0016_L5_height.png`, chords 29.6-32.8 mm); the PNGs' location is not recorded | 492 B | HOME root | 2026-10-09 (read) |
| HOME`/logs_peddev_{40183811,40183813,40183847,40183857,40183866,40183876,40183932,40183943,40183947,40183959}.{out,err}` | the pedicle development loop 04:29-06:02 (`pedicle_dev.py`); the last prints per-case widths, for example 0001 L1 mean 4.4 mm, 0004 L5 mean 17.3 mm against Panjabi 8.6 and 18.6; copied to `results/` | 0-696 B each | HOME root | 2026-10-09 (`40183959.out` read) |
| HOME`/logs_pedbatch_40183964.{out,err}` | 06:03-07:26, `ped_batch.py` over 60 cases: 114-118 pedicles per level, medians L1 7.1, L2 7.0, L3 9.1, L4 12.0, L5 14.4 mm beside Panjabi, Zindrick, Yu and Arockiaraj (the "118 pedicles per level" of commit db4db40); copied to `results/` | 601 B + 0 B | HOME root | 2026-10-09 (read) |
| Ceph`/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` | `ostk_level_morphometry.csv` 302,994 B (05:11; CRLF; the concatenation of the 24 shards, committed as CTSpinoPelvic1K 90a27a7, where the blob is 298,249 B with LF), `pdw_why.py` 1,761 B (16:00; probes where `pedicle_widths` bails on L1 and L5 of named cases; copied to `code/`), `pi_ostk2.csv` 662 B (11:46; ten cases, pelvic incidence by the pre-fix estimator; 5 rows flagged `identity_violation` with PI 2.3-20.1 (0024, 0182, 0375, 0401, 1084) and 5 `ok` with PI 36.7-62.0 (0569, 0624, 0760, 1043, 1129); for example 0024 PI 2.301; copied to `results/`), `pitest/` (10 label files, 13,899,387 B: 0024, 0182, 0375, 0401, 0569, 0624, 0760, 1043, 1084, 1129), `pdwtest/` (2 label files, 2,710,749 B: 0010, 0038) | 17.3 MB | batch B14, cut over 2026-10-08 11:02 (HOME names are now symlinks with `.pre-ceph` twins still beside them); `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/B14/STATUS` rows 003-007 VERIFIED (files and bytes equal, sampled; grid HOME clone, read 2026-10-08 22:20 UTC in `../10_data_platform_grid`'s listing; not in the laptop clone at 097933a); dedup `HASH_RESULTS.md` run 1 group A08: `pitest` and `pdwtest` are not v11 files (v10 copies, 12 unpaired), deletion candidates | 2026-10-09 (listing) |
| HOME`/{ostk_level_morphometry.csv, pdw_why.py, pdwtest, pi_ostk2.csv, pitest}` | symlinks (2026-10-08 11:02) to the Ceph paths above; `*.pre-ceph` originals still present (302,994 B, 1,761 B, dir, 662 B, dir) | 17.3 MB duplicated on HOME | B14 cut over; the `.pre-ceph` twins are for 10's deletion decision (Greg, handoff `OPEN_QUESTIONS.md` A26) | 2026-10-08 22:20 UTC listing |

## 2. Shared with 05_ct_morphometry_parity (the spinopelvic scratch of the same day)

| path | holds | size | state | verified |
|---|---|---|---|---|
| HOME`/spinopelvic_all.csv`, `~/agg_spinopelvic.py`, `~/show_pi.py`, `~/ss_probe.py`, `~/disc_probe*.py`, `~/height_probe.py`, `~/cmp_pdw.py`, `~/lm_probe.py` | spinopelvic estimator scratch of 2026-09-10 (`spinopelvic_all.csv` 63,562 B); in no repository as far as recorded | small | HOME root | 2026-10-08 22:20 UTC listing (grid inventory section 3.5); not re-read here |

## 3. Data and environments the tests need

| path | holds | size | state | verified |
|---|---|---|---|---|
| HOME`/data/CTSpinoPelvic1K/labels` | the v11 release labels (802 `NNNN_label.nii.gz`); `labels_v10/` beside it; CT at HOME`/data/CTSpinoPelvic1K/ct` (handoff `RECIPES.md` section 9, `D=~/data/CTSpinoPelvic1K`); the shard inputs of 2026-09-10 12:26 link into this folder (they were v10 at that date; v11 was defined 2026-09-16) | 1.19 GB for the labels (dedup A07: `s1v11/out/v11_labels` = the release labels, 802 identical) | HOME; whether and when it moves is 10's decision | the symlink targets seen 2026-10-09; the folder itself not listed in this pass |
| Ceph`/data/ctspinopelvic1k_build_tree/derived/s1v11/` | the v11 build workspace (835 files, 1,189,924,200 B; owner-only, "restricted, irreplaceable"; held for Greg's review) | 1.19 GB | B14 VERIFIED | `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/B14/STATUS` row 008 (grid HOME clone; read 2026-10-08 22:20 UTC in `../10_data_platform_grid`'s listing) |
| HOME`/mambaforge/envs/spineps/bin/python` | the CPU-tool interpreter (nibabel, scipy, numpy) ostk jobs run with; `fluorogen` (GPU), `spinedet`, `nextflow` beside it; export `PYTHONNOUSERSITE=1` in every job | `~/mambaforge` 14 GB (`MIGRATION_PLAN.md` section 8) | HOME, stays | handoff `RECIPES.md` section 0 item 5; not re-listed here |
| Ceph`/envs/` | conda environments `acq`, `fluoroclip`, `spineps212`, `spineps_cu128`, `tsv3`, `u251_drug`, `ytdl` | 39.923 GB (grid inventory r92) | Ceph | 2026-10-09 (listing) |

## 4. What is not on the grid

- No `.git`, no tests, no `SPEC.md` and no commit record of ostk: the repository lives only on GitHub and the
  laptop clone (`MANIFEST_CODE.md`). Step 5 of `TODO.md` writes `COMMIT.txt` beside the grid copy.
- No fixed ostk anywhere: the grid copy is the 1b7005c state for `vertebral_body.py`.
- No run of `level_morphometry` on v11 labels after the fix; no pedicle-width column populated by a full run
  (`STATUS.md` G.4); no rendered body cuts of the fixed code.
- The twelve `*_height.png` renders of job 40183679 and the reader E renders are not under any ostk path;
  the reader E renders are in the private repository (`MANIFEST_CODE.md`).
- The `OpenSpineToolbox` folder the pacs note calls stale was not seen in either grid listing.

## 5. How this folder's grid facts were taken

`wsl -e bash -lc 'ssh grid "ls -la ...; stat -c ... ; cat <small file>"'` on 2026-10-09 00:12 UTC; the
hashes were computed on the laptop from the `cat` output (md5sum and python are killed by name on the login
node). Jobs for the steps in `TODO.md` go through `sbatch -D <dir>` with the `spineps` interpreter; the
template is handoff `RECIPES.md` section 0.
