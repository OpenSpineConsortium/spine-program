# results/grid_run_2026-09-10: records of the day ostk measured all 802 records

Small files read from the grid on 2026-10-09 00:12 UTC with `cat` (read-only; `../../MANIFEST_GRID.md`
section 5). They are the evidence behind `../../STATUS.md` G.4 and the timeline below. Times are the
grid's local clock (-0400) from `ls`; commit times are from `git log` of OpenSpineToolkit.

| file | what it is |
|---|---|
| `grid_listing_2026-10-09T0012Z.txt` | the `ls`/`stat` output of both passes (paths, sizes, dates; nothing else) |
| `logs_ostkmorph_40183643.out` | 03:06-03:17, `ostk_morph.py` over 60 cases: every case failed with the matmul shape error; the Panjabi tables print n = 0 |
| `logs_ostkmorph_40183680.err` | the 03:34 rerun, cancelled at 03:44:42 |
| `logs_ostkext_40183713_0.{out,err}` | the first shard attempt (03:42, "shard 0/24: 34 case(s)"), cancelled at 03:58:24 |
| `ostk_morph_out_shard_0.csv` | one of the 24 shards of 04:52-05:10 that became the committed `ostk_level_morphometry.csv` (200 rows; `PDW_l`, `PDW_r`, `PDW` empty in every row; CRLF on the grid, 12,764 B, written here LF, 12,563 B) |
| `logs_peddev_40183959.out` | the last pedicle development job (05:59-06:02): per-case widths by `pedicle_dev.isthmus_width`, for example 0001 L1 mean 4.4 mm, 0004 L5 mean 17.3 mm, beside Panjabi |
| `logs_pedbatch_40183964.out` | 06:03-07:26, `ped_batch.py` over 60 cases: 114-118 pedicles per level; medians L1 7.1, L2 7.0, L3 9.1, L4 12.0, L5 14.4 mm beside Panjabi 8.6/8.2/10.2/14.1/18.6, Zindrick, Yu and Arockiaraj (the table commit db4db40 calls "validated on 118 pedicles per level") |
| `pi_ostk2.csv` | 11:46, ten cases through the pre-fix pelvic-incidence path; 5 rows flagged `identity_violation` with PI 2.3-20.1 (0024, 0182, 0375, 0401, 1084) and 5 `ok` with PI 36.7-62.0 (0569, 0624, 0760, 1043, 1129); for example 0024 PI 2.301 |
| `ostk_shards_out_spinopelvic_0.csv` | 12:52-13:25, `python -m ostk all` shard: PI/SS/PT/LL for 101 cases on v10 labels; the run copy's `labels.py` (7,722 B, dated 11:29) is the detected-scheme version committed as 2e8b2c2 at 11:52 |
| `ostk_shards_mout_morph_6.csv` | 13:18-14:28, `python -m ostk morph` shard: wide format, 100 cases; the pedicle keys land as `T11_l` ... `L5_l` (medians 0.71-1.42 mm) with `L3_r`, `L3_mean` on one case |

## The day in order (from the files above, the commit log and `ls` dates)

| time (-0400) | event | evidence |
|---|---|---|
| 03:02 | commit 204ce14, `ostk.morphometry` in the vertebra's own frame | `git log` |
| 03:06-03:17 | job 40183643 `ostk_morph.py`: every case crashes (axis matrix used as an axis) | `logs_ostkmorph_40183643.out` |
| 03:18 | commit 9091e36 fixes it | `git log` |
| 03:20-03:25 | job 40183679: twelve posterior-height renders (`*_height.png`, chords 29.6-32.8 mm); their location not recorded | `logs_rheight_40183679.out` (listing only) |
| 03:34-03:44 | job 40183680, cancelled | `logs_ostkmorph_40183680.err` |
| 03:41 | `ostk_extract.py` written (the 24-shard extractor) | `ls` date |
| 03:42-03:58 | first shard array (job 40183713/15), cancelled | `logs_ostkext_40183713_0.*` |
| 03:50 | commit 8790353, the `morph` command | `git log` |
| 04:10 | commit da2550a, pedicle width opt-in (`pedicle: bool = False`) | `git log` |
| 04:11 | `~/ostk_run/OpenSpineToolkit` copy made; `~/ostk.tgz` at 04:10:58 | `ls`, `stat` |
| 04:11-05:11 | the 24 shards run; `shard_*.csv` 04:52-05:10; the concatenation is dated 05:11 and became CTSpinoPelvic1K commit 90a27a7 the same day | `ls`; `../../MANIFEST_GRID.md` |
| 04:29-06:02 | ten `pedicle_dev` jobs | `logs_peddev_*` |
| 06:03-07:26 | job 40183964 `ped_batch.py`, the 118-pedicle table | `logs_pedbatch_40183964.out` |
| 07:28-07:29 | `~/ostk_run/OpenSpineToolkit/ostk/morphometry.py` overwritten (db4db40's text); commit db4db40 at 07:29:58 | `ls`, hash, `git log` |
| 11:29-12:25 | the run copy's other modules refreshed (`labels.py` 11:29, `metrics.py`/`spine.py` 12:23); commits 2e8b2c2 (11:52), 477dd0d, 6cacd3e, e57408b | `ls`, `git log` |
| 11:38, 16:09 | `~/pitest` (10 labels), `~/pdwtest` (2 labels) made (v10 copies, dedup A08) | `ls`; `dedup/HASH_RESULTS.md` |
| 12:26 | `~/ostk_shards/in_*` symlinks into `~/data/CTSpinoPelvic1K/labels` | `ls` |
| 12:52-13:25 | `out/spinopelvic_0..7.csv` | `ls` |
| 13:18-14:28 | `mout/morph_0..7.csv` | `ls` |
| 16:00 | `pdw_why.py` written | `ls` |
| 16:04, 16:16 | commits d1189c8, 6a5992f (the pedicle note rewritten twice) | `git log` |
| 22:11 | `vertebral_body.py` with the ring closing saved; rsynced to `~/OpenSpineToolkit` on 2026-09-23 | `ls` (grid copy dated 22:11) |
| 22:52 | commit 1b7005c, the regression | `git log` |

The scripts that ran are in `../../code/grid_ostk_run_2026-09-10/`. The reference CSV's six 0097 rows are
`../ostk_level_morphometry_0097_reference_90a27a7.csv`.
