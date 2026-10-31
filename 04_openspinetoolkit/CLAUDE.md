# 04_openspinetoolkit: working context

OpenSpineToolkit (`ostk`) is the public Python package that measures spinopelvic parameters and
per-level vertebral geometry on CTSpinoPelvic1K label volumes. This folder is the seed of the
project that keeps it correct for release v11 and for the student miniprojects. It was built on
2026-10-08 from the laptop, the grid and the repositories; `MANIFEST_LOCAL.md` records where every
copy came from. Nothing in this folder depends on a laptop path. The only outside references are
the grid (`/wsu/home/go/go24/go2432`, `/rs/rs_grp_oschome/go2432`) and the repositories named in
`MANIFEST_CODE.md`.

## The goal in one paragraph

Fix the five known defects of ostk at commit cb43197 (`main`, 2026-09-25) and prove each fix with a
one-hour test that has a number: (1) the 1b7005c canal-closing regression that inflates posterior
body height and end-plate depth by 10-17 mm on about one vertebra in seven with no gate firing (case
0097 T12 VBHp 38.4 against 28.9 mm; `STATUS.md` G.2); (2) the `"S1": 29` entry of `LABELS_V10` that
makes a by-name call on a v11 volume fall back to the whole sacrum without a flag (G.3); (3) the
pedicle-width column that is empty in all 4,744 committed rows (G.4); (4) the documents that still
describe the legacy v3 scheme and "27 tests", and the one failing test (`tests/test_cobb.py` line
91); (5) the grid copy `/wsu/home/go/go24/go2432/OpenSpineToolkit`, which carries the regression and
has no commit beside it. Steps 1 and 2 block every morphometry number in `05_ct_morphometry_parity`.
The ordered steps, gates and deciders are in `TODO.md`; the results in hand are in `STATUS.md`.

## Where things are

- **This folder.** `STATUS.md` (results with numbers, files and rigor marks), `TODO.md` (ordered
  steps), `MEMORY.md` + `memory/` (28 notes with their statuses), `MANIFEST_GRID.md`,
  `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md`, `docs/handoff/` (the eight student-readable handoff files
  of 2026-10-08, whole, with their absolute laptop paths replaced by markers: `docs/handoff/ABOUT.md`), `results/` (the 0097 reference rows at commit 90a27a7 and the records of
  the 2026-09-10 grid run), `code/` (the pre-ostk scripts of 2026-05 and the grid-only drivers of the
  2026-09-10 run, each with a header saying where it came from), `figures/` (the May 2026 student
  panels), `manuscripts/bibm_spinopelvic/` (an unfinished 2026-06-28 draft with its honesty contract).
- **The code.** `OpenSpineToolkit`, branch `main`, commit cb43197, remotes `origin`
  (Gregory-Schwing-MD-PhD) and `osc` (OpenSpineConsortium): `ostk/labels.py` (`labels_for` at line
  135, `LABELS_V4` line 36, `LABELS_V10` line 59, the `"S1": 29` entry line 64), `ostk/vertebral_body.py`
  (`canal_mask` lines 98-132), `ostk/spine.py` (the sacrum fallback lines 473-474),
  `ostk/morphometry.py` (`canal_dimensions` line 151, `pedicle_widths` line 256 returning keys `l`,
  `r`, `mean`, `level_morphometry` line 380), `tests/` (94 test functions), `projects/` (13 student
  miniprojects by `git ls-files projects` at cb43197, 3 with a `main.py`, 10 README-only), `tools/export_demo_case.py` (the PACS demo exporter; imports
  `lid`). Everything else that matters is listed with lines in `MANIFEST_CODE.md`.
- **The reference.** The extraction script the fix must agree with is
  `CTSpinoPelvic1K/scripts/extract_surgical_morphometrics.py` (`_sacral_plate` at line 137 isolates
  the S1 plate by the lowest lumbar body's footprint); the pre-regression numbers are
  `CTSpinoPelvic1K/morphometrics/ostk_level_morphometry.csv` at commit 90a27a7 (4,744 rows; the six
  case-0097 rows are in `results/`).
- **The grid.** `/wsu/home/go/go24/go2432/OpenSpineToolkit` (rsync copy, `ostk/` + `pyproject.toml`,
  no `.git`, carries 1b7005c's closing; verified 2026-10-09 00:12 UTC), `~/ostk.tgz`, `~/ostk_run`,
  `~/ostk_shards`, `~/ostk_morph_out` and the `logs_ostk*`, `logs_ped*`, `logs_rheight_*` of the
  2026-09-10 run; the v11 labels under `~/data/CTSpinoPelvic1K/labels`; Greg's Python for CPU jobs is
  `~/mambaforge/envs/spineps/bin/python`, in his HOME, which students cannot read; a student's environment is
  `11_students_grid_access/STUDENT_ENV.md` (written by issue #66). Every path with what it holds: `MANIFEST_GRID.md`.

## Rules that bind this project (the standing rules, restated)

1. **Words.** Never the French-derived word for where data came from: write source, origin, lineage,
   where it came from, label history. No fractional version numbers; fold changes into the next integer
   version. Figure captions at most 60 words; the argument goes in the text. Plain sentences.
2. **Every number carries its file.** A count, date, path or claim names the file it comes from; what no
   file records is written "not recorded"; an unexplained failure is recorded as unexplained, not guessed.
3. **Check outside the computation.** The recurring failure in this programme is a number that is wrong
   but plausible: three estimators returned finite values from the wrong bone, the wrong surface or the
   wrong label map and nothing raised, and the identity PI = SS + PT held through a 9-degree error in
   sacral slope. Compare with published values, an independent implementation, the distribution's spread
   (not its median), a published prevalence; render the mask. "The numbers moved toward the mean" is not
   a pass.
4. **Labels and orientation.** Two label schemes are live and mixing them does not raise: the release
   (v11, VerSe-native: L1-L5 = 20-24, L6 = 25, sacrum 26, hips 30/31, femora 32/33) and the legacy ostk
   map (L1 = 1, S1 = 7, sacrum 8, hips 9/10, femora 11/12). Resolved against the wrong map,
   "femur_left" comes back T4. Call `ostk.labels.labels_for(volume)`; never import a fixed map. In v11
   identifier 29 (the carved S1 of v10) is retired and dissolved into 26; code that gates on 29 must go
   with it, and ostk's own `LABELS_V10` still carries it. Case ids are zero-padded in the release
   (`0001`) and were not in old CSVs: `zfill(4)` before diffing. Volumes are stored (P, I, R):
   canonicalise to RAS to analyse (`nib.as_closest_canonical`), never reorient when writing a label.
5. **Held out means never seen.** Every quoted model score goes through the evaluation gate of the
   private repository and the leaked banks are never quoted (allspine v2, v6, v7, v8 for VerSe,
   `anchor_drr`, `vindrps`). This folder holds no model and quotes no model score; the rule binds any
   measurement that feeds one.
6. **Pre-register, then score.** Write the rule and its success number before the run (the gates in
   `TODO.md` are written before any fix is tested); numbers enter text from files, never typed.
7. **The grid's login node runs nothing.** Every computation, render and download is an `sbatch` job;
   warrior kills python, rsync, md5sum and others by name. `sbatch -D <dir>` (a relative `--output`
   resolves against the submit directory), `afterany` not `afterok`, IPC under `/dev/shm` (node `/tmp` is
   swept), large outputs on Ceph, grid bash is bash 4.2. Read-only looking with `ls`, `stat`, `cat` of
   small files and `squeue` is fine, which is how this folder's grid facts were taken.
8. **Private things stay private.** SchwingNet and all level-identification code, text, figures and
   weights stay private; never add such code to ostk without asking. ostk itself is public (Apache-2.0):
   what goes into it is research and education material only.
9. **Data.** Use all of a public dataset; every truncation is fixed or justified in writing before a
   rerun; identity comes from metadata first and the file name last.
10. **Git, network, credentials.** In OpenSpineToolkit, ostk commits go to `main` and are pushed to both
    remotes; commit only when Greg asks. In spine-program itself the account doing the work pushes only its
    claim branch `claude/<issue>` and the pull request merges as root `CLAUDE.md` rule 10 says. On Greg's laptop, network
    (push, ssh, rsync) goes through `wsl -e bash -lc '...'`. Tokens are
    read from files only, never echoed, never on a command line. Write scripts as files and run them
    by path (heredocs collapse backslashes). Ashley Schehr is a person, never a product name. The
    affiliation is General Surgery (Wayne State University School of Medicine / Detroit Medical
    Center), never Neurosurgery.

## Traps that cost time here

- **The regression's own docstring says the closing is "used only to find the hole". It is not.**
  The extra hole sections change which sections carry a wall; VBHa, SA, SP, IA and `plate_rms` stay
  unchanged, so nothing raised. It was found by rendering (`memory/ostk-canal-closing-regression.md`).
- **The sacrum fallback is documented as wrong inside the function that performs it** (`spine.py`
  lines 461-467: "drives pelvic incidence far too low") and attaches no flag. Grep finds no fallback
  flag in `metrics.py` or `spine.py` (handoff working note topic 6 section 9.5).
- **Pedicle width has two column vocabularies.** `pedicle_widths` returns `l`, `r`, `mean`; the grid
  extractor `code/grid_ostk_run_2026-09-10/ostk_extract.py` writes `PDW_l`, `PDW_r`, `PDW` and keeps
  only those keys, so its columns are empty by construction; the `morph` CLI writes `<level>_l`. See
  `STATUS.md` G.4 before touching it, and budget hours not minutes (30-60 s per level).
- **The 2026-09-10 run's own package copy was overwritten the same day** (`~/ostk_run/OpenSpineToolkit/
  ostk/morphometry.py` is dated 07:28, after the 04:11-05:11 shards), so the package state that produced
  the committed CSV is inferred from commit times, not preserved.
- **The test fixture uses legacy ids.** `tests/test_cobb.py` removes labels 11 and 12 (the legacy
  femora); the failing assertion at line 91 sees `no_levels_available`. Cause not investigated.
- **The exporter defaults to the legacy map.** `tools/export_demo_case.py` imports `lid` (line 39) and
  calls `lid("S1")` (lines 80, 110); demo case 0003 is a v3-scheme case. Running it on a v11 case needs
  `labels_for`.
- **Three files of the grid copy have CRLF line endings**: `vertebral_body.py` (43,929 B against 43,092 B for the
  same 1b7005c text with LF), `morphometry.py` (20,271 against the 19,859 B blob) and `surgery.py` (37,631 against
  36,948); `labels.py`, `spine.py` and `genant.py` are LF and equal byte for byte. Normalise line endings on every
  compared file before hashing, or the comparison in `TODO.md` step 5 fails for the wrong reason.
- **Do not re-measure a synthesised post-operative image** (`ostk.surgery`): voxel roughness collapses
  the plate fit (LL 45.7 read as about 24 when it should rise to 55); post-op numbers are carried
  analytically and the image is display only (`memory/postop-spine-synthesis.md`).
- **The blanket "SVA/TPA out of scope (no C7/T1)" claim was removed by Greg** because some scans do
  include C7/T1 (`memory/pacs-demo-and-ostk-params.md`); `SPEC.md` line 130, `README.md` lines 44 and 48,
  `CLAUDE.md` line 23 and `ostk/README.md` line 42 still carry it.
- **`SPEC.md` is the student contract and it is stale** (v3 ids 1-50 in section 1, "27 tests" in
  `ostk/README.md` line 10, `lid("L1")` in `CLAUDE.md` line 59). Students read it first (handoff
  `OPEN_QUESTIONS.md` F10).

## How to work here

Read `README.md`, then `STATUS.md`, then `TODO.md`. Before a fix, write its gate and number into
`TODO.md` if it is not already there. Test on case 0097 first (the six reference rows are in
`results/ostk_level_morphometry_0097_reference_90a27a7.csv`), then on twenty records, and render ten
body cuts before believing a number. Keep the comparison against the published floors and SDs named in
`TODO.md` step 1. When a note in `memory/` and a result file disagree, the file wins.
