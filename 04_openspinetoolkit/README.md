# 04_openspinetoolkit: OpenSpineToolkit, the v11 defects and their tests

Rank 4 of the spine programme's twelve projects (`../_plan/PLAN.md` section 1). Reader: student-safe.
Built 2026-10-08 from the sources recorded in `MANIFEST_LOCAL.md`, `MANIFEST_CODE.md` and
`MANIFEST_GRID.md`. Start with `CLAUDE.md` (rules and traps), then `STATUS.md`, then `TODO.md`.

## What it is

OpenSpineToolkit (`ostk`) is a tested, public (Apache-2.0) Python package that measures spinopelvic
parameters (pelvic incidence, sacral slope, pelvic tilt, lumbar lordosis, PI-LL with the SRS-Schwab
modifiers, coronal Cobb) and per-level vertebral morphometry (body heights, end-plate widths and depths,
canal width and depth, pedicle width, six-point Genant morphometry) from CTSpinoPelvic1K label volumes,
with a sagittal DRR renderer, a 2-D projection of the same landmarks, a post-operative synthesis
prototype, a CLI (`python -m ostk {pi,ll,cobb,all,morph}`) and `projects/` for student miniprojects
contributed by fork and pull request. At commit cb43197 (`main`, 2026-09-25) it has 19 modules under
`ostk/`, 94 test functions in 14 test files and 13 miniproject folders (`git ls-files projects` at cb43197, 2026-10-08), 3 with a `main.py` and 10 README-only
(`MANIFEST_CODE.md`; counts verified 2026-10-08 with `git ls-files` and `grep -c "def test_"`).

## The goal

Keep ostk correct for release v11 and the student miniprojects by closing five defects, each with a
pre-stated test (`TODO.md` steps 1-5):

1. the 1b7005c canal-closing regression (VBHp and EPD inflated 10-17 mm on about one vertebra in
   seven; 0097 T12 VBHp 38.4 against 28.9 mm; `STATUS.md` G.2);
2. the `"S1": 29` entry that sends v11 volumes down the whole-sacrum branch silently (G.3);
3. the empty pedicle-width column (G.4);
4. the stale `SPEC.md`, `README.md`, `CLAUDE.md` and `ostk/README.md` (legacy v3 scheme, "27 tests",
   `lid()`, the blanket SVA/TPA claim) and the one failing test (`tests/test_cobb.py` line 91);
5. the grid copy, which carries the regression and has no commit recorded beside it.

## State on 2026-10-08

- Public repository in sync with `origin/main` at cb43197; only `build/` and `openspinetoolkit.egg-info/`
  untracked (`git status -sb`, 2026-10-08). Both remotes (`origin`, `osc`) point at the same commit per
  the 2026-10-08 inventory (`MANIFEST_CODE.md`).
- `python -m pytest` on the laptop, 2026-10-08: 1 failed, 100 passed in 70.21 s (reproduces handoff
  `OPEN_QUESTIONS.md` F18).
- No fix for G.2 or G.3 through cb43197 (read in the code on 2026-10-08: `canal_mask(..., min_vox=20)`
  with the 2 mm ring closing at `ostk/vertebral_body.py` lines 98-132; `"S1": 29` at `ostk/labels.py` line
  64; the fallback at `ostk/spine.py` lines 473-474).
- G.4 has a mechanical reading found on 2026-10-08 by reading code: `pedicle_widths` returns keys `l`,
  `r`, `mean` and the grid extractor keeps only `PDW_l`, `PDW_r`, `PDW`, so the committed columns are
  empty by construction; what the function returns on real volumes is contested between two files
  (`STATUS.md` G.4). Not run.
- The committed reference `ostk_level_morphometry.csv` (CTSpinoPelvic1K commit 90a27a7, 2026-09-10,
  4,744 rows, 802 cases) predates the regression and already meets the step-1 gate: 0.71 % of L1-L5
  canal depths under 11.07 mm (n 3,784) and per-level SD 2.03-3.62 mm (`STATUS.md` "Baseline").
- The grid copy `/wsu/home/go/go24/go2432/OpenSpineToolkit/ostk/vertebral_body.py` equals commit
  1b7005c line for line (CRLF endings; read 2026-10-09 00:12 UTC), so `OPEN_QUESTIONS.md` B29 is answered:
  the regression is on the grid (`MANIFEST_GRID.md`).

## Success criteria (the numbers the fixes must hit; from `TODO.md`)

- 0097 within 1 mm of the 90a27a7 rows on VBHp, EPDl and SCD; share of L1-L5 canal depths under
  11.07 mm at or below 5.2 % (twice the published 2.62 % congenital-stenosis prevalence); per-level SD
  inside the widest published living SD (2.45 at L3, 3.76 at L5); ten rendered body cuts show the wall
  on the body.
- A by-name S1 call on a v11 volume raises or sets a QC flag; `python -m ostk all` on v11 labels never
  runs the whole-sacrum branch silently; a test on a v11 volume proves it.
- Pedicle width present on at least 95 % of level instances; L5 tracks the published 16.20 mm rather
  than the release script's 20.70.
- `python -m pytest`: 101 passed; the four documents name v11, 94 tests, `labels_for` and the retired 29.
- `/wsu/home/go/go24/go2432/OpenSpineToolkit/COMMIT.txt` names the commit and the grid's
  `ostk/vertebral_body.py` hashes equal to the laptop's after line-ending normalisation.

## How it relates to the other projects

- **03_ctspinopelvic1k_dataset** supplies the v11 labels the tests run on and owns `scripts/label_scheme.py`
  (the source of truth that has no `"S1"` key) and `scripts/merge_s1_into_sacrum.py`. Depends on 03.
- **05_ct_morphometry_parity** consumes `level_morphometry` and the spinopelvic summary; its PAR and CT
  items wait on steps 1 and 2 here (handoff `RESEARCH_DIRECTIONS.md` CT-1 "depends on: nothing"; ranked
  5 in its section 6). This folder blocks 05.
- **07_plain_film_level_id** and **XRSpinoPelvic1K** import `ostk.project2d` and `ostk.drr` (the 2-D port).
- **08_render_devices** (PolyPose) measures through the release plate fits, not through ostk's primitives;
  the old ostk-primitive path read PI 3.6 on a (P, I, R) case whose truth is 53 (`STATUS.md` G.7).
- **12_website_pacs_demo** is fed by `tools/export_demo_case.py` (`metrics.json` for case 0003).
- **11_students_grid_access** hands students `SPEC.md` and `projects/`, which is why step 4 matters.

## What is deliberately not here

The repository itself (reference by commit; nothing of it is copied), the full 4,744-row CSV and the
morphometry documents (in 05 and 03), the reader E renders of the regression (3.2 MB, in 05's
`results/reader_e/diag/`), and the May 2026 survey CSV and abstract-portal PDF that carry names and
addresses (`MANIFEST_LOCAL.md`, "not copied").

## On the grid

Since 2026-10-13 (issue #87) `results/`, `figures/` and `manuscripts/` of this folder are symlinks to the same path under `/rs/rs_grp_oschome/shared/spine-program/archive/` on the grid, where the files are read through the link; everywhere else they are read from git history at main 5597197. `../ARCHIVE.md` says how, and how a task that must change one of them brings it back into its branch. The counts and sizes in `MANIFEST_LOCAL.md` describe the folder as it was built on 2026-10-08.
