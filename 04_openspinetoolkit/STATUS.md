# STATUS.md: the results in hand on 2026-10-08

Rows G.1-G.8 are `docs/handoff/RESULTS_CATALOG.md` Part G verbatim in substance, with their status words
and the files that hold them; the "checked 2026-10-08" column says what this build verified outside the
catalog by reading code, files and the grid. Rows marked [DERIVED] were computed read-only by the builder
from committed rows or captured files, not by a committed tool (the catalog's definition). Status words:
CURRENT, OPEN (a known defect), DATED (a state at its date), prototype, unexplained, SUPERSEDED (do not
quote), RECORD ONLY (history).

## Part G of the catalog, as it stands

| id | claim | file | status | checked 2026-10-08 |
|---|---|---|---|---|
| G.1 | 94 test functions across `tests/`; `tests/test_labels.py` covers scheme detection | `OpenSpineToolkit` cb43197 `tests/` | CURRENT | 94 by `grep -c "def test_"` over 14 files; `python -m pytest -q` on the laptop: **1 failed, 100 passed in 70.21 s** (handoff `OPEN_QUESTIONS.md` F18 reproduced); the failure is `tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs` line 91, flags `sagittal_ref_fallback`, `no_levels_available` |
| G.2 | **regression**: commit 1b7005c (2026-09-10 22:52) added a 2 mm ring closing in `canal_mask`; in the two or three sections below the pedicles it bridges the laminae, `body_mask_by_canal` takes that section's anterior canal edge as the wall (14-15 mm posterior of the true wall) and every lower section inherits it: case 0097 T12 VBHp 38.4 against 28.9 mm, EPDl 52.0 against 34.8; about one vertebra in seven inflated by 10-17 mm with no gate firing; `min_vox = 20` admits 3 mm "canals" (16 % of chords below the 11.07 mm living floor against 2.6 % published). Do not trust ostk VBHp / EPD / EPWl computed after that commit | `memory/ostk-canal-closing-regression.md`; `ostk/vertebral_body.py` lines 98-132; renders `SchwingNet/results/reader_e/diag/*.png` (private repository, 7 files 3.2 MB, copied into 05) | **OPEN**: no fix through cb43197; found by rendering | `canal_mask(..., min_vox: int = 20)` at line 98 and `ndimage.binary_closing(mvc[k], se)` inside it are in cb43197; the `pedicle_widths` and `level_morphometry` code paths unchanged in function since db4db40 apart from comments. The reference rows: 0097 T12 VBHp **28.88**, EPDl **34.80**, SCD 18.72 (`results/ostk_level_morphometry_0097_reference_90a27a7.csv`). The inflated values 38.4 and 52.0 exist in no file but the note; they are re-measured by `TODO.md` step 1 |
| G.3 | **finding of 2026-10-08 (by reading code, not run)**: `LABELS_V10` still maps `"S1": 29`; on a v11 volume no voxel is 29, so `endplate_from_label(..., "S1", ...)` falls back to the whole sacrum, which the function's own docstring calls "a last resort ... drives pelvic incidence far too low", and no QC flag marks the fallback; `python -m ostk all` on v11 labels runs the branch documented as wrong | `ostk/labels.py` line 64; `ostk/spine.py` lines 473-474; handoff working note topic 6 section 9.5 | **OPEN**; fix = port the extraction script's lowest-lumbar footprint isolation into ostk and flag the fallback | both lines confirmed in cb43197; the extraction script's method is `_sacral_plate` at `CTSpinoPelvic1K/scripts/extract_surgical_morphometrics.py` line 137; `scripts/label_scheme.py` has no `"S1"` key (handoff `scheme-bone-hardware-only` note); the exporter `tools/export_demo_case.py` calls `lid("S1")` at lines 80 and 110 with the same fallback |
| G.4 | `PDW` (pedicle width) is empty in all 4,744 rows of `ostk_level_morphometry.csv`; the 2026-09-10 shard run produced pedicle columns for about two of about 5,600 level-instances | `CTSpinoPelvic1K/morphometrics/ostk_level_morphometry.csv`; `docs/SPINOPELVIC_ESTIMATOR.md` "Pedicle width" | unexplained in the catalog | [DERIVED] a mechanical reading, below under "G.4 read on 2026-10-08"; PDW, PDW_l and PDW_r are empty in all 4,744 rows (counted) |
| G.5 | post-operative synthesis (`ostk.surgery`): demo case 0003, ALIF L1-S1, age 50, LL 45.7 to 55.0, PI-LL 9.8 to 0.5, five cages; re-measuring the synthesised image collapses LL 45.7 to about 24 (voxel roughness), so post-op numbers are carried analytically and the image is display only | `memory/postop-spine-synthesis.md`; `memory/postop-jaggedness-future.md` | prototype | not re-run; `ostk/surgery.py` is 36,948 B at cb43197 (`git cat-file -s`); the grid copy is 37,631 B, CRLF (683 lines) |
| G.6 | PolyPose (private repository): DeepFluoro reproduction "REPRODUCED" (Dice pelvis 0.992, femora 0.978 / 0.980); generator commit 1f4418f never pushed; `VALIDATION.{json,md}` does not exist | `SchwingNet/results/polypose/REPRODUCTION.md`, `REPRODUCIBILITY.md`; `polypose-generator-build` note (in 08) | OPEN (validation not written) | belongs to 08_render_devices; listed because PolyPose imports ostk (`MANIFEST_CODE.md`) |
| G.7 | the old ostk-primitive path read PI 3.6 / LL -8.9 on (P, I, R) case 0874 (truth 53 / 54); PolyPose now measures through the release plate fits (`tools/polypose/measure_sagittal.measure_image`) | `polypose-generator-build` note (in 08) | CURRENT trap | the trap is restated in `CLAUDE.md` ("canonicalise to analyse") |
| G.8 | PACS X-ray demo latency 40,018 ms to 1,360 ms; since 2026-09-14 the X-ray model runs behind the level service | `pacs-website-latency-root-cause` note (in 12); website commit ea0086c | DATED | belongs to 12_website_pacs_demo |

## Catalog rows from Part F that judge ostk against the release scripts (owned by 05, quoted here)

| id | claim | file | status |
|---|---|---|---|
| F.26 | extraction script against ostk on the same 300 records: PI median 49.2 against 45.8; outside the plausible range 6.3 % against 16.0 %; ostk's S1 surface fit is bimodal (28.3 % of 802 land on a steeper surface, PI near 18.6 with SS near 42, arriving as `identity_violation` with PI = |SS - PT|) | `CTSpinoPelvic1K/docs/SPINOPELVIC_ESTIMATOR.md` "Which estimator" | CURRENT (the release reports the extraction script) |
| F.36 | pedicle width tracks 13 published series except L5 (20.70 against 16.20; withheld from the figure); ostk reads L5 15.10 mm on individual cases | `SPINOPELVIC_ESTIMATOR.md` "Pedicle width" | CURRENT |
| F.37 | ostk against the scripts over 802 records against Panjabi 1992: ostk closer on posterior body height at every level (L5 error +7.5 to +2.3 mm), worse on every width (no transverse-process removal): EPW L5 ostk 55.6 against scripts 51.0 against Panjabi 47.3; SCW L5 35.2 against 30.0 against 27.1 | `CTSpinoPelvic1K/docs/OSTK_VS_EXTRACTION.md`; the CSV at 90a27a7 | CURRENT (the figure keeps the scripts' values) |

## G.4 read on 2026-10-08 (not run; code, timestamps and captured files) [DERIVED]

1. **The columns are empty by construction at cb43197.** `ostk/morphometry.py` `pedicle_widths` (lines 256-378)
   returns a dict with keys `l`, `r` and `mean`; `level_morphometry` merges it unchanged (line 410,
   `out.update(pedicle_widths(...))`). The grid extractor that produced the committed CSV,
   `code/grid_ostk_run_2026-09-10/ostk_extract.py` (grid HOME `~/ostk_run/ostk_extract.py`, 2026-09-10
   03:41), declares `FIELDS = [... "PDW_l", "PDW_r", "PDW", ...]` and writes `row[k] = v` only `if k in row`.
   The names do not match, so `l`, `r` and `mean` are dropped whatever they held. The 24 shard files it wrote
   (`~/ostk_morph_out/shard_0..23.csv`, 04:52-05:10) sum to 304,811 B, the Ceph concatenation's 302,994 B plus 23 repeated 79-byte CRLF headers exactly
   (`MANIFEST_GRID.md` section 1) and `shard_0.csv` has 0 non-empty PDW values in 200 rows
   (`results/grid_run_2026-09-10/ostk_morph_out_shard_0.csv`).
2. **At the run's hour the function was also opt-in.** Commit da2550a (04:10:37 -0400) gave
   `level_morphometry` a `pedicle: bool = False` argument; the extractor never passes it; the shards ran
   04:11-05:11; db4db40 (07:29:58) removed the argument again. The run's own package copy
   (`~/ostk_run/OpenSpineToolkit/ostk/morphometry.py`) was overwritten at 07:28 with db4db40's text (hash
   e6623025958e3fa5..., 15,044 B), so the state at 04:11 is inferred from these times, not preserved. Either
   reason alone empties the columns; the key mismatch is the one that is still true today.
3. **What the function returns on real volumes is contested between two files.** The comment inside
   `pedicle_widths` (cb43197 lines 284-304) says a direct call on case 0010 returns L1 6.62 mm and L5 15.10 mm
   and that `level_morphometry` returns the same. The grid's second run through the `morph` CLI
   (`~/ostk_shards/mout/morph_6.csv`, 2026-09-10 13:18, package at the db4db40 state, which has the same
   function body) records for case 0010 `L1_l` 1.06 and `L5_l` 3.54 mm, and across its 100 cases the `_l`
   medians are 0.71-1.42 mm with `r` present on 1 case of 100 (`results/grid_run_2026-09-10/
   ostk_shards_mout_morph_6.csv`, counted). No pedicle is 0.7 mm wide (published means 5.8-18.6 mm,
   `code/grid_ostk_run_2026-09-10/ped_batch.py` table). Which reading is right is `TODO.md` step 3's first
   hour. The numbers that were validated on 2026-09-10 (118 pedicles per level, medians L1 7.1, L2 7.0,
   L3 9.1, L4 12.0, L5 14.4 mm; `results/grid_run_2026-09-10/logs_pedbatch_40183964.out`) came from
   `pedicle_dev.isthmus_width` (an erosion-neck method, `code/grid_ostk_run_2026-09-10/pedicle_dev.py`),
   not from `ostk.morphometry.pedicle_widths` (a least-area section method).
4. **Cause of the catalog's "about two of about 5,600"**: not established; the one `L3_r`/`L3_mean` pair in
   `morph_6.csv` is the kind of stray cell the catalog counted.

## Baseline for the step-1 gate, from the pre-regression CSV (commit 90a27a7) [DERIVED]

Computed 2026-10-08 from `CTSpinoPelvic1K/morphometrics/ostk_level_morphometry.csv` (4,744 rows, 802 cases;
population SD):

| level | n | SCD median | SCD SD | share under 11.07 mm | VBHp median | VBHp SD | EPDl median | EPDl SD | EPWl median | EPWl SD |
|---|---|---|---|---|---|---|---|---|---|---|
| T12 | 797 | 17.93 | 1.77 | 0.4 % | 27.63 | 3.39 | 33.80 | 5.68 | 44.53 | 5.51 |
| L1 | 796 | 18.24 | 2.20 | 1.1 % | 29.02 | 3.71 | 35.03 | 6.36 | 45.91 | 5.65 |
| L2 | 791 | 18.02 | 2.03 | 0.5 % | 28.88 | 3.32 | 36.28 | 6.28 | 47.80 | 6.04 |
| L3 | 795 | 18.16 | 2.27 | 0.5 % | 28.50 | 2.84 | 35.47 | 5.50 | 49.82 | 5.76 |
| L4 | 794 | 19.85 | 2.79 | 0.5 % | 27.48 | 2.94 | 33.30 | 4.86 | 51.77 | 5.79 |
| L5 | 757 | 22.07 | 3.62 | 0.9 % | 25.24 | 3.03 | 29.69 | 5.27 | 53.61 | 7.63 |
| L6 | 14 | 20.32 | 3.94 | 0.0 % | 24.13 | 2.10 | 26.38 | 4.29 | 56.52 | 15.53 |

L1-L5 pooled: 3,784 instances, **0.71 %** under 11.07 mm. Against the outside references: the published
congenital-stenosis prevalence is 2.62 % (`CTSpinoPelvic1K/docs/LEVEL_MORPHOMETRY.md` line 28), the window
rule allows at most twice that (`J3_NOT_SUBMITTED.md` line 34), and the widest published living SD for canal
depth is 2.45 at L3 and 3.76 at L5 (Griffith; `LEVEL_MORPHOMETRY.md` lines 22-23). The pre-regression ostk
output passes all three; the post-regression table did not (15.8 % of reader E's J1 instances under the
floor, `J3_NOT_SUBMITTED.md` line 14). So the step-1 gate is "reproduce 90a27a7 on 0097 within 1 mm and keep
these shares and SDs", not "improve on them". EPWl at L5 (53.61, SD 7.63) is the transverse-process merge the
catalog's F.37 describes and is 05's atlas question (CT-5), not this project's.

## The grid copy (answers handoff `OPEN_QUESTIONS.md` B29) [DERIVED]

`/wsu/home/go/go24/go2432/OpenSpineToolkit/ostk/vertebral_body.py` (43,929 B, 2026-09-10 22:11) equals
commit 1b7005c's text after CRLF normalisation and differs from cb43197 by the 3 lines of the numpy fix (3 replaced in place at lines 453-454 and 830; `git diff --numstat 1b7005c cb43197 -- ostk/vertebral_body.py`);
`labels.py` and `spine.py` equal cb43197's byte for byte (LF); `morphometry.py` equals it after CRLF normalisation (20,271 B on the grid, 19,859 B blob, 412 lines); `surgery.py` was not read (37,631 B = the 36,948 B blob + 683 line endings). The grid copy therefore carries the regression and
the `"S1": 29` entry. Read 2026-10-09 00:12 UTC (`MANIFEST_GRID.md` section 1).

## The documents and the exporter (stale text located) [DERIVED]

`SPEC.md` section 1 ("CTSpinoPelvic1K v3", ids 1-50, ignore 50) and line 130; `README.md` lines 27-48;
`CLAUDE.md` line 23 ("SVA/TPA need C7/T1, which v3 doesn't have") and line 59 (`lid("L1")`); `ostk/README.md`
line 10 ("27 analytic + phantom + CLI tests"), line 17, line 42; `projects/README.md` rows for
`sagittal-vertical-axis` and `t1-pelvic-angle` ("out of scope"). Handoff contradiction C10 (topic 6 section
14) trusts the code and the pacs note over these documents. `tools/export_demo_case.py` imports `lid` at line 39
and calls it at lines 80, 82, 110, 112 and 203. `CLAUDE.md` of ostk has no grid command (F10 check: nothing to
remove; the `sbatch` form is to be added).

## What is superseded, and by what

- The "27 tests" of `ostk/README.md` line 10: superseded by 94 test functions (G.1).
- `SPEC.md` section 1's v3 scheme and `lid()`: superseded by `labels_for` (commit 2e8b2c2) and the v11 scheme
  (`CLAUDE.md` rule 4); the documents were never updated.
- The blanket "SVA/TPA out of scope" claim: withdrawn by Greg in June 2026 (`memory/pacs-demo-and-ostk-params.md`);
  the documents still carry it.
- The `S1 = 29` line of the v10 scheme in `memory/label-scheme-v4-vs-ostk.md`: true for v10, retired in v11
  (2026-09-16; `scheme-bone-hardware-only` note in 03).
- The catalog's G.4 "unexplained": narrowed by the reading above; the contested return value is not resolved.
- The grid inventory's "commit unknown; regression state unknown (B29)" for the grid copy: answered above.
- The 2026-09-10 shard-run CSV is right for every column but PDW and remains the reference (G.2); the
  `morph` CLI's wide-format shards of 13:18-14:28 are not a reference for anything (pedicle keys misnamed,
  run on v10 labels).
- The "23-byte gap" between the 24 shard files and the committed CSV, written in an earlier pass of this build: the
  shards and the Ceph concatenation are CRLF with a 79-byte header line, 304,811 - 23 x 79 = 302,994 B is the Ceph
  file exactly, and the committed blob is 298,249 B because git stored the same 4,745 lines with LF
  (`MANIFEST_GRID.md` section 1). Arithmetic, not an unknown.

## What is not known (recorded, not guessed)

- Why `pedicle_widths` returns 0.7-1.4 mm medians through the CLI run while its own comment reports 6.62 and
  15.10 mm by direct call (item 3 above).
- The commit the grid copy was rsynced from (no `.git`; by content it is the ba82e1a-to-cb43197 state).
- The cause of the `test_cobb` failure (`OPEN_QUESTIONS.md` F18: "not investigated").
- Whether the twelve `*_height.png` renders of job 40183679 still exist and where.
