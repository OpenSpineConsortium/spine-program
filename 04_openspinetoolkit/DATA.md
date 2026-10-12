# DATA.md: this folder's data on the grid, reached through Beethoven

How a student reaches the grid material of 04_openspinetoolkit and runs the first measurement.
The paths are every row of `MANIFEST_GRID.md` sections 1 to 3, spelled as that manifest spells
them: HOME = `/wsu/home/go/go24/go2432` (Panasas), Ceph = `/rs/rs_grp_oschome/go2432`. Sizes,
dates and contents come from `MANIFEST_GRID.md`; what no file records is written "not recorded".

Every check line below is read-only (`ls -ld` for a directory or a link, `head -c 200` for a
file) and runs from the Beethoven worker — a session on a compute node — never python on the
login node (`CLAUDE.md` rule 7; read-only `ls`, `stat` and `cat` of small files are the one
thing the login node is for). Set once, then paste a check line:

```
H=/wsu/home/go/go24/go2432; C=/rs/rs_grp_oschome/go2432
```

A check line on a HOME path works only for Greg: nothing on HOME is readable by students (see
"Access", below). Each HOME row is marked **on HOME, not reachable until migrated**, with the
manifest's own migration state beside it where the manifest records one.

Line endings: three files of the grid toolkit copy are CRLF (`vertebral_body.py`,
`morphometry.py`, `surgery.py`) and three are LF (`labels.py`, `spine.py`, `genant.py`)
(`MANIFEST_GRID.md` section 1). Normalise line endings on every compared file before hashing,
or a comparison fails for the wrong reason (`TODO.md` step 5 gate).

## 1. The toolkit on the grid (`MANIFEST_GRID.md` section 1)

| path | volume | what it holds | access today | check line |
|---|---|---|---|---|
| HOME`/OpenSpineToolkit` | HOME (Panasas) | an rsync copy of ostk with no `.git`: `ostk/` (19 `.py` files, `README.md`, `__pycache__/`) and `pyproject.toml`; `vertebral_body.py` is the 1b7005c state — it carries the canal-closing regression and lacks cb43197's 3-line fix; no `COMMIT.txt`; about 1.5 MB | on HOME, not reachable until migrated; the manifest records it in no migration batch, staying on HOME (code, small) | `ls -ld $H/OpenSpineToolkit` |
| HOME`/ostk.tgz` | HOME (Panasas) | an ostk tarball of 2026-09-10 04:10:58; contents not read; 186,470 B; deletion candidate once `TODO.md` step 5 is done | on HOME, not reachable until migrated; deletion is Greg's | `head -c 200 $H/ostk.tgz` (a gzip file; expect binary) |
| HOME`/ostk_run/` | HOME (Panasas) | the work directory of the 2026-09-10 shard run: `ostk_extract.py`, `ostk_morph.py`, `ped_batch.py`, `pedicle_dev.py`, `edge_probe.py`, `render_height.py` and a nested `OpenSpineToolkit/` copy; the four scripts that matter are copied into this folder's `code/grid_ostk_run_2026-09-10/`; small, not sized | on HOME, not reachable until migrated | `ls -ld $H/ostk_run` |
| HOME`/ostk_shards/` | HOME (Panasas) | `in_0` … `in_7`, eight folders of symlinks into HOME`/data/CTSpinoPelvic1K/labels/` (100-101 links each, 2026-09-10 12:26; no data duplicated); `mout/morph_0..7.csv` (wide format, pedicle keys misnamed); `out/spinopelvic_0..7.csv`; small | on HOME, not reachable until migrated | `ls -ld $H/ostk_shards` |
| HOME`/ostk_morph_out/` | HOME (Panasas) | `shard_0..23.csv`, 24 long-format files summing 304,811 B, CRLF; their concatenation is the committed `ostk_level_morphometry.csv` (90a27a7); PDW empty in every row read; 302 KB | on HOME, not reachable until migrated | `ls -ld $H/ostk_morph_out` |
| HOME`/logs_ostkext_40183713_{0..23}.{out,err}` | HOME (Panasas) | the first shard attempt (2026-09-10 03:42), cancelled; 48 files of 23-81 B | on HOME, not reachable until migrated; deletion candidates | `head -c 200 $H/logs_ostkext_40183713_0.out` |
| HOME`/logs_ostkmorph_40183643.{out,err}` | HOME (Panasas) | the 60-case check of 03:06-03:17, every case failed on the matmul bug fixed at 03:18:37; 11,438 B + 0 B; a copy is in this folder's `results/grid_run_2026-09-10/` | on HOME, not reachable until migrated | `head -c 200 $H/logs_ostkmorph_40183643.out` |
| HOME`/logs_ostkmorph_40183680.{out,err}` | HOME (Panasas) | the rerun of 03:34, cancelled at 03:44:42 after "10/60"; 32 B + 81 B | on HOME, not reachable until migrated | `head -c 200 $H/logs_ostkmorph_40183680.err` |
| HOME`/logs_rheight_40183679.out` | HOME (Panasas) | twelve posterior-height renders written 03:20-03:25 (chords 29.6-32.8 mm); the PNGs' location is not recorded; 492 B | on HOME, not reachable until migrated | `head -c 200 $H/logs_rheight_40183679.out` |
| HOME`/logs_peddev_{40183811,40183813,40183847,40183857,40183866,40183876,40183932,40183943,40183947,40183959}.{out,err}` | HOME (Panasas) | the pedicle development loop 04:29-06:02; the last prints per-case widths; 0-696 B each; a copy of `40183959.out` is in `results/grid_run_2026-09-10/` | on HOME, not reachable until migrated | `head -c 200 $H/logs_peddev_40183959.out` |
| HOME`/logs_pedbatch_40183964.{out,err}` | HOME (Panasas) | `ped_batch.py` over 60 cases, 06:03-07:26: 114-118 pedicles per level with medians beside the published series; 601 B + 0 B; a copy is in `results/grid_run_2026-09-10/` | on HOME, not reachable until migrated | `head -c 200 $H/logs_pedbatch_40183964.out` |
| Ceph`/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` | Ceph | `ostk_level_morphometry.csv` 302,994 B (CRLF; the 24 shards concatenated, committed as CTSpinoPelvic1K 90a27a7, blob 298,249 B with LF), `pdw_why.py`, `pi_ostk2.csv` (ten cases, five flagged `identity_violation`), `pitest/` (10 v10 label files), `pdwtest/` (2); 17.3 MB; batch B14 cut over 2026-10-08 | readable by approved students (under Ceph `/data/`) | `ls -ld $C/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10` |
| HOME`/{ostk_level_morphometry.csv, pdw_why.py, pdwtest, pi_ostk2.csv, pitest}` | HOME (Panasas) | symlinks (2026-10-08 11:02) to the Ceph scratch above; the `*.pre-ceph` originals (17.3 MB) went with B14's FINALIZE of 2026-10-11 (`../10_data_platform_grid/MANIFEST_GRID.md` section 2) | on HOME, not reachable until migrated; students use the Ceph path above instead | `ls -ld $H/ostk_level_morphometry.csv` |

## 2. Shared with 05_ct_morphometry_parity (`MANIFEST_GRID.md` section 2)

| path | volume | what it holds | access today | check line |
|---|---|---|---|---|
| HOME`/spinopelvic_all.csv`, `~/agg_spinopelvic.py`, `~/show_pi.py`, `~/ss_probe.py`, `~/disc_probe*.py`, `~/height_probe.py`, `~/cmp_pdw.py`, `~/lm_probe.py` | HOME (Panasas) | the spinopelvic estimator scratch of 2026-09-10 (`spinopelvic_all.csv` 63,562 B); in no repository as far as recorded | on HOME, not reachable until migrated; whether these are in a migration batch is not recorded in this folder | `head -c 200 $H/spinopelvic_all.csv` |

## 3. Data and environments the tests need (`MANIFEST_GRID.md` section 3)

| path | volume | what it holds | access today | check line |
|---|---|---|---|---|
| HOME`/data/CTSpinoPelvic1K/labels` | spelled on HOME; resolves to Ceph | the v11 release labels (802 `NNNN_label.nii.gz`, ids zero-padded), `labels_v10/` beside them, CT at HOME`/data/CTSpinoPelvic1K/ct`; 1.19 GB. `~/data/CTSpinoPelvic1K` is a HOME symlink; its Ceph target, from `03_ctspinopelvic1k_dataset/MANIFEST_GRID.md` section 1, is `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (batch B02 cut over 2026-10-08) | the Ceph target is readable by approved students; the HOME spelling resolves only for Greg | `ls -ld $C/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` |
| Ceph`/data/ctspinopelvic1k_build_tree/derived/s1v11/` | Ceph | the v11 build workspace (835 files, 1,189,924,200 B); batch B14 VERIFIED | owner-only (`drwx--S---`, read 2026-10-12, issue #65) until Greg reads its Zenodo upload scripts for a token; see "Terms" below | `ls -ld $C/data/ctspinopelvic1k_build_tree/derived/s1v11` (expect owner-only bits) |
| HOME`/mambaforge/envs/spineps/bin/python` | HOME (Panasas) | the CPU-tool interpreter (nibabel, scipy, numpy) ostk jobs run with; `~/mambaforge` is 14 GB; export `PYTHONNOUSERSITE=1` in every job | on HOME, not reachable until migrated; the manifest records it staying on HOME. A student's environment is `../11_students_grid_access/STUDENT_ENV.md` (issue #66) | `head -c 200 $H/mambaforge/envs/spineps/bin/python` (a binary; expect ELF bytes) |
| Ceph`/envs/` | Ceph | conda environments `acq`, `fluoroclip`, `spineps212`, `spineps_cu128`, `tsv3`, `u251_drug`, `ytdl`; 39.923 GB | beside Ceph `/data/`, not under it, so the student-access fact below does not cover it; whether students can read it is not recorded | `ls -ld $C/envs` |

## Terms

- The labels are **CTSpinoPelvic1K v11, CC BY-NC-SA 4.0 on Zenodo**
  (`03_ctspinopelvic1k_dataset/docs/release/README.md` "Sources and licence"; the v11 record is
  10.5281/zenodo.22797014, `03_ctspinopelvic1k_dataset/docs/handoff/EXTRACTS.md`).
- `s1v11`: 03 records it as restricted — "stays owner-only until its upload scripts are read
  for a token"; owner-only (`drwx--S---`) when read on 2026-10-12 (issue #65); when it opens to
  students is Greg's decision (`03_ctspinopelvic1k_dataset/MANIFEST_GRID.md` section 1).
- The ostk code itself is public, Apache-2.0 (this folder's `CLAUDE.md` rule 8).
- For everything else in sections 1 to 3 (the run scratch, the logs, the probe scripts, the
  environments): not recorded in the folder.

## Access (Greg's facts of 2026-10-11, issue #7)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** — a
  named ACL entry on the volume root, other-read bits on folders and files — including
  `vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and
  `spine_detector_corpus`, because every approved student holds the PhysioNet credential and
  the VinDr and BUU agreements.
- **On 2026-10-12 the VinDr and BUU items inside those folders opened too.** Until then the
  plan's `restricted` flag still closed them item by item, mode `drwx--S---` (`vindr/raw`,
  `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and BUU banks of B10 and B11,
  `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain
  folder including `multisource_banks`) open them (issue #65).
- **Two paths stay closed (owner-only):**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`,
  private build material and not a dataset, and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, until Greg reads its
  Zenodo upload scripts for a token (issue #65;
  `../10_data_platform_grid/code/data_platform/plan/publish_visibility.sh`, from
  spinesurg-ct-nnunet d9b388d).
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students; items
  still there are moved to the Ceph volume by the data-platform plan, whose batch-by-batch state
  is `../10_data_platform_grid/MANIFEST_GRID.md` section 2. Every HOME row above is marked
  'on HOME, not reachable until migrated'.
- Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

## Through Beethoven

The way in is Beethoven, the lab's Chrome extension: install and use it per
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (the same pages are at
https://openspineconsortium.com/beethoven/). A student needs: a WSU AccessID with a grid
account, the Google Authenticator grid code, Claude Pro or Max, and Chrome on the invited
Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`.

The two access facts, again, because everything below depends on them:

- every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named
  ACL entry on the volume root; other-read bits on folders and files), and since 2026-10-12 the
  VinDr and BUU items inside them; two paths stay closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`
  (private build material, not a dataset) and
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its
  Zenodo upload scripts for a token);
- nothing on `/wsu/home/go/go24/go2432` is readable by students until the data-platform plan
  has moved it to Ceph.

Run the check lines of sections 1 to 3 from the Beethoven worker. Computation is an `sbatch`
job, never a command on the login node (`CLAUDE.md` rule 7).

## First experiment: re-measure case 0097 at cb43197

This is the measurement `TODO.md` step 1 asks for **before any fix**: run ostk as it stands on
case 0097's v11 label alone and put its numbers beside the pre-regression reference rows.

1. **The label.** The folder spells the labels HOME`/data/CTSpinoPelvic1K/labels` — a HOME
   symlink; a student uses its Ceph target from `03_ctspinopelvic1k_dataset/MANIFEST_GRID.md`
   section 1: `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels`.
   Make a work folder holding one symlink to `0097_label.nii.gz` and point the run at it — the
   pattern of the 2026-09-10 shard folders, which linked into the labels folder and duplicated
   no data (`MANIFEST_GRID.md` section 1, `ostk_shards`).
2. **The code.** ostk at commit cb43197, branch `main`, cloned from the repository named in
   `MANIFEST_CODE.md`. Not the grid copy HOME`/OpenSpineToolkit`: it has no `.git`, its
   `vertebral_body.py` is the 1b7005c state, and students cannot read it.
3. **The run.** `python -m ostk morph --labels <dir>` as an `sbatch` job (`sbatch -D <dir>`;
   CPU partition `reqp --qos=requeue`; the job template is handoff `RECIPES.md` section 0).
   The interpreter the folder records is Greg's HOME`/mambaforge/envs/spineps/bin/python`,
   which students cannot read; a student's environment is
   `../11_students_grid_access/STUDENT_ENV.md` (issue #66).
   Case 0097 alone also fits on a laptop (`TODO.md`).
4. **The comparison.** The reference is
   `results/ostk_level_morphometry_0097_reference_90a27a7.csv` — the six case-0097 rows of the
   committed CSV at 90a27a7, before the regression: **T12 VBHp 28.88, EPDl 34.80, SCD 18.72**.
   The regression note expects cb43197 to read about **VBHp 38.4 and EPDl 52.0** at T12; those
   two numbers exist in no file but the note (`STATUS.md` G.2), and this run is their first
   re-measurement. Mind the format: the `morph` CLI writes one wide row per case, the reference
   is long format, one row per level (`TODO.md` item 7); map columns before diffing.
5. **Render the T12 cut** and look at where the posterior wall lands before reading a number
   (`TODO.md` step 1; `CLAUDE.md` "render the mask"). The regression was found by rendering,
   not by the numbers.

If any compared file is hashed along the way, normalise line endings first: three grid-copy
files are CRLF (`vertebral_body.py`, `morphometry.py`, `surgery.py`;
`MANIFEST_GRID.md` section 1).

The folder is student-safe once Greg confirms the reader split
(`TODO.md` "Decisions reserved to Greg").
