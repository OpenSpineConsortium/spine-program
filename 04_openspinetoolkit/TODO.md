# TODO.md: what remains, in order

Each step names its gate, the number stated before the run, what it depends on and who decides.
"Engineering" means anyone with this folder, the repository and grid access may do it; "Greg" means only
Greg decides. Steps 1-5 are the plan's five (`../_plan/PLAN.md` section 3, folder 04); the rest come from
the handoff's `OPEN_QUESTIONS.md` (OQ), `RESEARCH_DIRECTIONS.md` (RD, Greg-only, extracted), `RECIPES.md`,
`MANUSCRIPTS.md` section 10, the memory notes and the repository's own plan (`projects/README.md`,
`SPEC.md` section 6). Every run is an `sbatch` job (`CLAUDE.md` rule 7); 0097 alone fits on a laptop.

## Not on the grid on 2026-10-09 (`MANIFEST_GRID.md` section 4), and the step that puts it there

- No `.git`, no `tests/`, no `SPEC.md` and no commit record beside the grid copy of ostk: step 5 writes `COMMIT.txt`
  and rsyncs the committed tree.
- No fixed ostk anywhere on the grid (the copy is the 1b7005c state of `vertebral_body.py` and carries the `"S1": 29`
  entry): steps 1 and 2, shipped by step 5.
- No run of `level_morphometry` on the v11 labels after the fix, so no post-fix `ostk_level_morphometry.csv` for 05:
  step 6.
- No populated pedicle-width column in any full run (every PDW cell of the 24 shards is empty): step 3, then step 6.
- No rendered body cuts of the fixed code, and the twelve `*_height.png` renders of job 40183679 are at no recorded
  path: step 1 renders ten cuts; the twelve old renders stay "not recorded" unless a listing finds them.

## The five steps

| step | what | gate (stated before the run) | depends on | decides |
|---|---|---|---|---|
| 1 | **CT-1, the canal-closing fix** (RD section 4 CT-1; RD section 6 rank 5, "depends on: nothing"). In `ostk/vertebral_body.py` `canal_mask` and `body_mask_by_canal`: require a per-section hole area of at least 18 mm2; take the wall only from sections whose hole reaches the canal's median area; raise `min_vox` from 20 (6.5 mm3 at the release spacing). Run on 0097 and twenty records; render ten body cuts and look at where the wall lands before reading a number. Keep the comparison in `ostk_extract.py`'s long format so the rows diff against the reference. | 0097 rows within 1 mm of `results/ostk_level_morphometry_0097_reference_90a27a7.csv` on VBHp (T12 28.88), EPDl (34.80) and SCD (18.72); over 802 records the L1-L5 share of SCD under 11.07 mm at or below 5.2 % (the baseline is 0.71 %, `STATUS.md`) and per-level SCD SD inside 2.45 at L3 and 3.76 at L5 (baseline 2.27 and 3.62); the ten renders show the wall on the body, not on the articular process. "The numbers moved toward the mean" is not a pass. | 03 (the v11 labels at `~/data/CTSpinoPelvic1K/labels`) | engineering |
| 2 | **The S1 fallback** (G.3; OQ F8). In `ostk/spine.py` `endplate_from_label`: when `level == "S1"` and no voxel carries the id, either raise `SchemeError`-style or set a QC flag (`s1_fallback_whole_sacrum`) that every caller propagates; port `_sacral_plate` from `CTSpinoPelvic1K/scripts/extract_surgical_morphometrics.py` line 137 (the plate isolated by the lowest lumbar body's footprint in x and y, then a generous height bound) as the v11 S1 plate; remove or mark retired the `"S1": 29` entry of `LABELS_V10` (`labels.py` line 64) so it matches `scripts/label_scheme.py`, which has no `"S1"` key; fix the same `lid("S1")` branch in `tools/export_demo_case.py` lines 80 and 110. | A test on a v11 volume (a real one, or a synthetic one with ids 20-26 and 30-33) shows `python -m ostk all` never runs the whole-sacrum branch silently; the flag or the raise appears; on 20 v11 records the PI median lands within the published supine band (47.1-52.1, `SPINOPELVIC_ESTIMATOR.md` "Which estimator") and no record returns PI below 22.4 without a flag (the gated floor of the release estimator, same file "Still open"); the bimodal split of F.26 (28.3 % near PI 18.6) is gone or flagged. | nothing | engineering |
| 3 | **Pedicle width** (G.4; OQ D2). (a) One hour: call `ostk.morphometry.pedicle_widths` on case 0010 L1 and L5 at cb43197 and print `l`, `r`, `mean`; this decides between the comment's 6.62 / 15.10 mm and the CLI shard's 1.06 / 3.54 mm (`STATUS.md` G.4 item 3). (b) Make the key names agree: `pedicle_widths` to return `PDW_l`, `PDW_r`, `PDW`, or `level_morphometry` to map them, so the extractor's `FIELDS` and the `morph` CLI write the same columns. (c) If (a) returns sub-millimetre values, compare with `code/grid_ostk_run_2026-09-10/pedicle_dev.py` `isthmus_width` (erosion neck; 118 pedicles per level validated 2026-09-10, `results/grid_run_2026-09-10/logs_pedbatch_40183964.out`) and adopt the one that tracks the published series. (d) Budget hours: 30-60 s per level at the 0.35 mm resample. | PDW present on at least 95 % of level instances in a full 802-record run; L5 median tracks the published 16.20 mm rather than 20.70 (F.36) and sits inside the published range 11.8-21.6; L1-L4 within 2 mm of the thirteen-series means (`CTSpinoPelvic1K/morphometrics/pedicle_width_references.csv`); the 0010 result written down with its command. | step 1 (the body mask) | engineering |
| 4 | **Documents and tests** (OQ F8, F10, F18). `SPEC.md` section 1, `README.md`, `CLAUDE.md`, `ostk/README.md` and `projects/README.md` to v11 (ids 20-25, 26, 30-33, 34-61, 62-68; 29 retired), 94 tests, `labels_for` instead of `lid`, the SVA/TPA blanket claim removed (Greg withdrew it: some scans include C7/T1), the `sbatch -D` form for grid runs added to ostk's `CLAUDE.md`. Fix `tests/test_cobb.py` line 91: first print what `labels_for` returns on the fixture after ids 11 and 12 are removed (cause not investigated, OQ F18). Add a test for step 2 on a synthetic v11 volume and for step 1 on the 0097 rows if a small 0097 fixture can be made without shipping imaging data. | `python -m pytest`: 101 passed, 0 failed; a grep of the four documents finds no "v3", "27 tests", `lid("L1")` or "out of scope (needs C7/T1)" as a blanket claim. | steps 1-3 | engineering writes; **Greg commits and pushes** (`main`, both remotes; `CLAUDE.md` rule 10) |
| 5 | **The grid copy** (OQ B29). After the commit: rsync the laptop checkout to `/wsu/home/go/go24/go2432/OpenSpineToolkit` through WSL (`CLAUDE.md` rule 10); write `COMMIT.txt` beside it with the commit hash and date; delete `~/ostk.tgz` only when Greg agrees. | `cat ~/OpenSpineToolkit/COMMIT.txt` names the commit; the sha256 of every `ostk/*.py` on the grid, after CRLF-to-LF normalisation of every compared file (today `vertebral_body.py`, `morphometry.py` and `surgery.py` are CRLF on the grid and `labels.py`, `spine.py`, `genant.py` are LF: `MANIFEST_GRID.md` section 1), equals the laptop's at that commit (today's `vertebral_body.py` equals 1b7005c: `STATUS.md`); OQ B29 closed in the handoff. | step 4 | engineering; Greg for the deletion |

## After the five steps

| # | what | gate | depends on | decides | from |
|---|---|---|---|---|---|
| 6 | Re-run `python -m ostk morph` and `python -m ostk all` on the 802 v11 labels as a 24-shard `sbatch` array (the 2026-09-10 shard plan: `sbatch -D`, `afterany`, outputs on Ceph under `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/`), and hand the long-format CSV to 05 as the post-fix `ostk_level_morphometry.csv`. | all 802 cases present; the `qc_flags` column non-empty where a fallback fired; the baseline table of `STATUS.md` reproduced within its SDs; the run's job ids and ETA written here before sleeping | steps 1-3 | engineering | handoff `RECIPES.md` section 9 item 8; `submit-and-sleep-orchestration` note |
| 7 | Unify the two output formats: the `morph` CLI writes one wide row per case, the extractor one long row per level; pick the long format (it diffs against the reference) and have the CLI emit it, or document both. | one `python -m ostk morph` run reproduces the 90a27a7 column set exactly | step 3 | engineering | `STATUS.md` G.4 |
| 8 | Answer OQ E16 for ostk in `projects/README.md`: only `lordosis-trall-angle`, `sacral-slope-pelvic-incidence` and `scoliosis-cobb-angle` have a `main.py`; the other ten of the 13 folders are READMEs (`git ls-files projects` at cb43197); the table's status column marks `scoliosis-cobb-angle` "open" although its `main.py` exists; say which are open for students after v11. | the table in `projects/README.md` matches `git ls-files` | step 4 | engineering | OQ E16; `MANIFEST_CODE.md` |
| 9 | The BIBM draft (`manuscripts/bibm_spinopelvic/`): treat as unwritten (handoff `MANUSCRIPTS.md` section 10, "Redo"). If Greg wants it, Table 1 is `python -m ostk all` on v11 after steps 1-2 with `labels_for`, then `tools/cohort_stats.py`; the honesty contract in the header stays; the X-ray level-localisation parts are SchwingNet-adjacent and stay private. | Greg's yes or no recorded here | steps 1-2, 6 | **Greg** (OQ A8) | `MANUSCRIPTS.md` section 10 |
| 10 | The PACS exporter on a v11 case: `tools/export_demo_case.py` with `labels_for`, regenerate `pacs/data/<case>/metrics.json`, bump the cache-bust; pushing the website publishes. | the exported PI/SS/PT/LL equal `python -m ostk all` for the same case; demo case 0003 (v3 scheme) still renders | steps 2, 4 | engineering; **Greg** before any push to the website (publishes publicly) | `memory/pacs-demo-and-ostk-params.md`; 12_website_pacs_demo |
| 11 | Post-op synthesis: fix the voxel roughness so a synthesised image can be re-measured (anti-aliased label resampling, end-plate smoothing before the fit, or per-vertebra rigid placement). | re-measured LL after a +9.3 degree L1 rotation on case 0003 reads 55.0 within 1 degree instead of about 24 | nothing; dormant | **Greg** (whether to spend time on it) | `memory/postop-jaggedness-future.md` |
| 12 | The engine-swap interface (`predict(ct, label)`, `synthesize(ct, label, plan)` with the geometric code as the default backend). | contract only until a network backend exists | nothing; dormant | **Greg** | `memory/engine-swap-architecture.md` |
| 13 | Record, in 10's deletion list, the HOME duplicates this project left: `~/ostk.tgz`, `~/ostk_run`, `~/ostk_shards` (symlinks and 16 small CSVs), `~/ostk_morph_out`, the 48 `logs_ostkext_*`, the `*.pre-ceph` twins of the 2026-09-10 scratch, and the `pitest`/`pdwtest` v10 label copies on Ceph (dedup A08, deletion candidates). | each entry appears in `10_data_platform_grid`'s list with this folder named as owner | nothing | **Greg** (OQ A26: migration deletions) | `MANIFEST_GRID.md` |

## Decisions reserved to Greg

- Commit and push after step 4 (`main`, `origin` and `osc`); whether the fixed state is tagged as the next
  integer version.
- Whether the BIBM wrap-up is pursued (OQ A8) and whether the PACS demo is regenerated and published (step 10).
- Deletions on the grid (step 13; OQ A26) and of `~/ostk.tgz`.
- Whether level-identification code of any kind may enter ostk (the standing answer is no; handoff
  `INFRASTRUCTURE.md` section 1.1).
- Whether this folder may be handed to students: answered by Greg on 2026-10-12 (OQ A29; issue #68), every Write
  holder may read all 13 folders, and this folder is student-safe.

## Closed by this build (2026-10-08), for the handoff's record

- OQ B29: the grid copy carries the regression (`STATUS.md`, `MANIFEST_GRID.md`).
- OQ E16 for ostk: three of thirteen `projects/` folders have code (`git ls-files projects` at cb43197; the fourteenth entry under `projects/` is its `README.md`).
- OQ F10 for `ostk:CLAUDE.md`: no login-node command present; the `sbatch` form is still to be added (step 4).
- The grid inventory's unknown 10 for `~/ostk_run`, `~/ostk_shards`, `~/ostk_morph_out`: roles recorded.
