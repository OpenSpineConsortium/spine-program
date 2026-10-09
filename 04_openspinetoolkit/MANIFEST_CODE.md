# MANIFEST_CODE.md: the repositories this project works from

Nothing that lives in a repository is copied into this folder. Commits and remotes were read on
2026-10-08 with `git log -1`, `git remote -v` and `git status -sb` on the local clones (local refs only; no
network). Line numbers are at the commit named.

## OpenSpineToolkit (the code this project maintains)

| field | value |
|---|---|
| remotes | `origin` https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit.git ; `osc` https://github.com/OpenSpineConsortium/OpenSpineToolkit.git |
| branch, commit | `main`, cb43197 (2026-09-25 00:53 -0400, "A one-element array is indexed before it becomes a float"); in sync with `origin/main` on 2026-10-08; 85 commits since 2026-06-15 (handoff inventory) |
| visibility, licence | public; Apache-2.0 since commit 8bcaa78 (2026-06-23), relicensed from MIT |
| working tree | clean apart from untracked `build/` and `openspinetoolkit.egg-info/` (build artefacts); `_v.txt` is a tracked UTF-16 scratch readout of one case (not copied) |
| tests | 94 `def test_` functions in 14 files (cli 3, cobb 3, drr 5, geometry 5, io 3, labels 8, lordosis 24, masks 4, metrics 2, metrics2d 6, morphometry 10, project2d 11, spine 4, vertebral_body 6); `python -m pytest` 2026-10-08: 1 failed, 100 passed in 70.21 s |
| grid copy | `/wsu/home/go/go24/go2432/OpenSpineToolkit` (`ostk/` + `pyproject.toml`, no `.git`; `MANIFEST_GRID.md`) |

Files that matter, with lines at cb43197:

| file | what, and where |
|---|---|
| `ostk/labels.py` | `LABELS_V4` line 36 (legacy map, L1 = 1 ... femur_right = 12), `LABELS_V10` line 59, the `"S1": 29` entry line 64, `SchemeError` line 97, `detect_scheme` line 107 (pelvis voxel mass under each hypothesis; raises when ambiguous; returns the default for an empty volume), `labels_for` line 135, `lid` line 151 ("the thing to avoid in new code") |
| `ostk/spine.py` | `endplate_from_label` (docstring lines 458-467 calls the fallback "a last resort, not an equivalent ... drives pelvic incidence far too low"); the fallback itself lines 473-474 (`if level == "S1" and not m.any(): m = binary_mask(label, L["sacrum"])`), no QC flag |
| `ostk/vertebral_body.py` | `canal_mask(mask, affine, *, sup_axis, min_vox: int = 20)` line 98; the 2 mm ring closing before `binary_fill_holes` lines 113-132 (commit 1b7005c); `body_mask_by_canal`, `body_mask`, `endplate_corners_body` |
| `ostk/morphometry.py` | `CANAL_SLAB_FRAC` line 148, `canal_dimensions` line 151, `pedicle_widths` line 256 (returns `{"l", "r", "mean"}`, lines 346-378; its comment lines 284-304 record the 2026-09-10 shard-run puzzle, the 0010 figures at line 288), `level_morphometry` line 380 (merges `pedicle_widths` output unchanged at line 410; line 408 is the body-dimension prefix loop, 409 the canal merge) |
| `ostk/metrics.py` | PI/SS/PT, LL, PI-LL, Schwab modifiers, Roussouly, `spinopelvic_summary_from_label`; femoral head by acetabular-interface sphere fit; plausibility gates |
| `ostk/metrics2d.py`, `ostk/project2d.py`, `ostk/drr.py` | the 2-D port with identical definitions; the sagittal DRR along the bicoxofemoral axis; imported by XRSpinoPelvic1K |
| `ostk/genant.py` | six-point vertebral morphometry (commit ba82e1a) |
| `ostk/surgery.py` | post-operative synthesis prototype (`simulate_correction`, `bend_spine`, `warp_ct`, `synthesize_postop`, `place_interbody_cages`) |
| `ostk/cli.py` | `python -m ostk {pi,ll,cobb,all,morph} --labels <dir> --out <csv or jsonl> --workers N`; `_run_morph` line 61 and `_flatten` line 130 write the `morph` output wide, one row per case, keys prefixed by level |
| `tests/test_cobb.py` | line 83 `test_cobb_falls_back_gracefully_without_femurs`; removes legacy ids 11 and 12; assertion at line 91 fails with flags `sagittal_ref_fallback`, `no_levels_available` |
| `tests/test_labels.py` | 8 tests of scheme detection |
| `tools/export_demo_case.py` | the PACS demo exporter; `from ostk.labels import lid` line 39; `lid("S1")` lines 80 and 110; `lid(nm)` line 203; `--postop` flags |
| `SPEC.md` | the student contract; section 1 still "CTSpinoPelvic1K v3" with ids 1-50; line 130 "Out of scope (v3): SVA, TPA" |
| `README.md` | contributor guide; lines 27-48 name v3 and the SVA/TPA claim |
| `CLAUDE.md` | line 23 the SVA/TPA claim; line 59 "never hard-code an id, use lid("L1")"; no grid instructions (checked 2026-10-08 for handoff `OPEN_QUESTIONS.md` F10) |
| `ostk/README.md` | line 10 "27 analytic + phantom + CLI tests"; line 17 `LABELS`, `lid()`; line 42 SVA/TPA |
| `projects/README.md`, `projects/*/` | 13 miniproject folders (`git ls-files projects` at cb43197, 2026-10-08; the table in `projects/README.md` has 13 rows); `main.py` in `lordosis-trall-angle`, `sacral-slope-pelvic-incidence`, `scoliosis-cobb-angle` (answers handoff `OPEN_QUESTIONS.md` E16 for ostk: the other 10 are READMEs only). `projects/README.md`'s own status column is stale: it marks `scoliosis-cobb-angle` "open" although its `main.py` exists (`TODO.md` step 8) |
| `pyproject.toml`, `requirements.txt`, `pytest.ini` | installable since commit f9e23d3; `pytest.ini` sets `pythonpath = .` |

Commits that matter (`git log`, dates in -0400):

| commit | date | what |
|---|---|---|
| 204ce14 | 2026-09-10 03:02 | `ostk.morphometry`: level dimensions in the vertebra's own frame |
| 9091e36 | 2026-09-10 03:18 | pedicle width used the axis matrix as an axis (the matmul crash in `results/grid_run_2026-09-10/logs_ostkmorph_40183643.out`) |
| 8790353 | 2026-09-10 03:50 | `morph` command, and a CSV header bug it would have shipped |
| da2550a | 2026-09-10 04:10 | pedicle width not validated, so it no longer arrives by default (`level_morphometry(..., pedicle: bool = False)`) |
| db4db40 | 2026-09-10 07:29 | pedicle width validated on 118 pedicles per level, no longer opt-in (the `pedicle` argument removed) |
| 2e8b2c2 | 2026-09-10 11:52 | the label scheme is detected, not assumed (`labels_for`) |
| 477dd0d | 2026-09-10 12:11 | QC flags were dropped for exactly the cases that needed them |
| 6cacd3e | 2026-09-10 12:26 | the sacral base does not have the corners the corner method assumes |
| 4d50296 | 2026-09-10 13:29 | pelvic tilt is signed |
| d1189c8, 6a5992f | 2026-09-10 16:04, 16:16 | the pedicle note: "returns nothing through level_morphometry", then "slow and absent from one run, not broken" |
| 1b7005c | 2026-09-10 22:52 | canal depth as a midsagittal chord at the pedicle; adds the 2 mm ring closing (the regression) |
| ba82e1a | 2026-09-11 20:09 | six-point vertebral morphometry (`genant.py`) |
| cb43197 | 2026-09-25 00:53 | a one-element array is indexed before it becomes a float (3 lines of `vertebral_body.py` replaced in place, at lines 453-454 and 830: `git diff --numstat 1b7005c cb43197` gives 3 insertions, 3 deletions there; the other 241 insertions between the two commits are `genant.py`) |

## CTSpinoPelvic1K (the dataset repository; the reference the fixes are tested against)

| field | value |
|---|---|
| remotes | `origin` Gregory-Schwing-MD-PhD/CTSpinoPelvic1K ; `osc` OpenSpineConsortium/CTSpinoPelvic1K |
| branch, commit | `master`, 7ddfe38 (2026-10-08); working tree modified on 2026-10-08 |
| visibility | public; its root holds untracked personal files, so never `git add -A` there |

| file | why this project needs it |
|---|---|
| `scripts/label_scheme.py` | the single source of truth for v11: ids `range(0, 69)` minus 29, `verify()`, `label_dict()` with no `"S1"` key |
| `scripts/extract_surgical_morphometrics.py` | `_sacral_plate` line 137: the S1 end-plate of the whole sacrum isolated by the lowest lumbar body's footprint in both x and y, the method `TODO.md` step 2 ports; `_canal_column` line 240, `_canal_ap` line 337 (the release canal recipe); `_body_mask` line 397; `_femoral_head` line 479 |
| `scripts/merge_s1_into_sacrum.py`, `scripts/check_s1_merge.py` | v10 to v11 (29 into 26) and its check |
| `morphometrics/ostk_level_morphometry.csv` | commit 90a27a7 (2026-09-10, "ostk over all 802 records, and why the figure keeps the scripts' numbers"); 4,744 rows, 802 cases, columns `case, level, VBHa, VBHp, EPWu, EPWl, EPDu, EPDl, SCW, SCD, PDW_l, PDW_r, PDW, plate_rms_mm`; the pre-regression reference; six 0097 rows copied to `results/` |
| `morphometrics/level_references.csv` | 365 rows of published per-level values including Panjabi 1991 Table 3 |
| `morphometrics/pedicle_width_references.csv` | thirteen published pedicle-width series |
| `docs/SPINOPELVIC_ESTIMATOR.md` | the four defects of the estimator, "Which estimator the release actually reports" (ostk's bimodal S1 fit: 28.3 % of 802 land on a steeper surface with PI near 18.6), "Pedicle width", "Still open" |
| `docs/OSTK_VS_EXTRACTION.md` | ostk against the scripts over 802 records against Panjabi 1992 |
| `docs/LEVEL_MORPHOMETRY.md` | the canal floors (11.70 mm, 11.07 mm), the 2.62 % prevalence, the widest published living SDs (2.45 at L3, 3.76 at L5) |
| `CLAUDE.md` | the project's standing context (the two schemes, 29, zfill, orientation, "render the mask") |
| `paper/mpda/REPRODUCE.md` | the release pipeline; its section 0 still says v10 with S1 = 29 (stale per handoff `RECIPES.md` section 9) |

## spinesurg-ct-nnunet (private; the handoff and the consumers of ostk)

| field | value |
|---|---|
| remote | `origin` Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet (private since 2026-09-14) |
| branch, commit | `L6_Class`, 097933a (2026-10-08) |

| file | why |
|---|---|
| `HANDOFF/README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md` | copied whole into `docs/handoff/` |
| `HANDOFF/RESEARCH_DIRECTIONS.md` | Greg-only; its CT-1 row (section 4) and rank 5 (section 6) are extracted into `TODO.md` |
| `HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | sections 4.6-4.7 and 9-11 (the toolkit), 14 row C10; extracted into `STATUS.md` |
| `HANDOFF/context/*.md`, `context/INDEX.md` | the redacted note copies and their statuses (`MEMORY.md`) |
| `SchwingNet/tools/reader_e_features.py` (65609fd) | reader E builds its own closed-ring canal column and uses ostk's `body_mask` only as a recorded fallback |
| `SchwingNet/tools/reader_e_diag_corners.py`; `SchwingNet/results/reader_e/diag/` | the renders that found the regression: `0097_v11_diag.json` and the `0097_v11_k*_corners.png` (7 files, 3.2 MB; copied into 05) |
| `SchwingNet/results/reader_e/J3_NOT_SUBMITTED.md` | line 14: 15.8 % of J1 instances under the 11.07 mm floor against 2.62 % published; line 34: the window rule, share at or below 2 x 2.62 % |
| `tools/polypose/measure_sagittal.py`, `tools/polypose_sample.py`, `tools/polypose_warp.py`, `tools/polypose_invariants.py`, `tools/polypose_manifest.py`, `tools/polypose/cine_render.py`, `tools/polypose/validation_render.py` | ostk importers; PolyPose measures through the release plate fits (`measure_image`) |
| `tools/transitional_review/anomaly_rules.py`, `tools/transitional_review/build_review_tree.py`, `tools/eval_xrsp1k_seg.py` | ostk importers (`grep -rl "from ostk\|import ostk"`, 2026-10-08) |
| `data_platform/DATA_MANIFEST.md`, `MIGRATION_PLAN.md`, `LAYOUT.md`, `plan/batch_items/B14.tsv`, `dedup/HASH_RESULTS.md` | the migration state of the 2026-09-10 scratch (`MANIFEST_GRID.md`) |

## XRSpinoPelvic1K (private; the 2-D consumer)

| field | value |
|---|---|
| remote, branch, commit | `origin` Gregory-Schwing-MD-PhD/XRSpinoPelvic1K, `main`, 4f22935; private since 2026-09-26 |
| ostk importers | `annot/make_reference.py`, `scripts/evaluate_unified.py`, `scripts/evaluate_yolo.py`, `xrsp/build_dataset.py`, `xrsp/femhead.py`, `xrsp/oblique.py` (grep 2026-10-08); `xrsp/labels.py` has its own `labels_for` |
| caveat | built from 822 cases of a pre-release export; a rebuild from v11 must resolve names through `labels_for` and wait for `TODO.md` step 2 (handoff `DATA_MANIFEST.md` defect 36) |

## openspineconsortium.github.io (the demo the exporter feeds)

| field | value |
|---|---|
| remote, branch | `origin` OpenSpineConsortium/openspineconsortium.github.io, `master`; pushing publishes |
| local commit | c1800f8 (2026-10-02); the local clone was 10 commits behind `origin/master` on 2026-10-08 |
| files | `pacs/data/0003/metrics.json` (+ `ct.nii.gz`, `seg.nii.gz`, `postop_*`) written by `tools/export_demo_case.py`; commit ea0086c moved the X-ray model behind the level service (2026-09-14) |

## Student_Projects (nested in CTSpinoPelvic1K; the student entry)

`origin` OpenSpineConsortium/Student_Projects, `main`, local commit 3f1cf04 "ahead 1", deliberately not
pushed. `RECIPE.md` section 3 and 5 restate the private-forever list and the grid rules students follow.
Reference only.
