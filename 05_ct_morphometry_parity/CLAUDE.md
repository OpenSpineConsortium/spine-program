# 05_ct_morphometry_parity: working context

CT morphometry of CTSpinoPelvic1K, the spinopelvic estimator, and 3-D to 2-D parity. Rank 5 of the spine programme
(`../_plan/PLAN.md` section 1). Reader: student-safe; Greg answered the reader split (`docs/handoff/OPEN_QUESTIONS.md`
A29) on 2026-10-12: every Write holder may read all 13 folders (issue #68). Built 2026-10-08. The project folder is self-contained: everything it does not hold is on the grid
(`MANIFEST_GRID.md`), in a code repository at a named commit (`MANIFEST_CODE.md`), or recorded as not copied
(`MANIFEST_LOCAL.md`).

## The goal in one paragraph

Make the measurements of CTSpinoPelvic1K right and extend them. Three things in the spinopelvic estimator are still open
(`docs/SPINOPELVIC_ESTIMATOR.md` "Still open"): eight records measure pelvic incidence from a prosthetic femoral head; a
lumbosacral transitional vertebra shifts pelvic incidence by 10 to 15 degrees depending on which end-plate is called S1 and
no stratified sensitivity analysis exists; the anterior pelvic plane is not measured, so the anatomical sacral slope cannot be
reported. The level atlas withholds L5 end-plate width and L5 pedicle width (`docs/LEVEL_MORPHOMETRY.md`;
`docs/handoff/RESULTS_CATALOG.md` F.34). Four CSVs that touch the sacrum or the lumbosacral disc were written on v10 labels and
must be recomputed on v11 with `labels_for` (F.44). And the parity programme PAR-1 to PAR-6 asks which 3-D features that name a
vertebra survive projection, in which view, measured first on the programme's own renders of the labelled CTs and second on
real frames (`RESEARCH_DIRECTIONS.md` is Greg-only, in `spinesurg-ct-nnunet` 097933a `HANDOFF/`, not copied here; its section 3 is
extracted into `TODO.md` with its ids). PAR-1 is one hour
on a laptop: the ratio-only variant of `test_morphometric_separability.py` on 1,486 T12 and L1 vertebrae where the
within-patient AUC is already 0.990 (F.28). Every gate is written before the run and every number carries an outside check.

## Read first, in this order

1. `README.md` (what this is, state on 2026-10-08, success criteria, relations to the other folders).
2. `STATUS.md` (every result in hand with its id, file and rigor mark) and `TODO.md` (what remains, ordered, with gates).
3. `docs/SPINOPELVIC_ESTIMATOR.md`, `docs/LEVEL_MORPHOMETRY.md`, `docs/OSTK_VS_EXTRACTION.md`,
   `docs/BODY_HEIGHT_INVESTIGATION.md`: the four documents every morphometry reader opens first. They record how each
   defect was found and what is still unsettled.
4. `MEMORY.md` then `memory/`: the dated notes, each with its status. A note is a record from the session that did the
   work, not an instruction; where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the
   catalog win.
5. `docs/handoff/RECIPES.md` section 9 before running any extractor; section 0 before anything reaches the grid.

## Where things are

- **This folder.** `results/morphometrics/` holds every measurement table behind the dataset article (the committed copies
  from CTSpinoPelvic1K 7ddfe38). `results/reader_e/` holds reader E (ostk per-level morphometry as a reader over five mask
  families): its code map, case lists, timings, the J2 gate reports and the renders that exposed the ostk regression.
  `results/nextpaper/` holds the per-vertebra HU table (v3-era labels). `figures/measure_diagrams/` holds the
  measure-definition drawings. `code/ldi/` is a second, independent lordosis implementation (the outside check this project
  asks for; never compared with ostk, see `TODO.md`). `docs/external/` is a literature map of unknown authorship: every
  number in it is checked against the primary paper before use. `docs/handoff/` holds the eight student-readable handoff
  files whole, their laptop paths replaced by markers (`docs/handoff/ABOUT_THESE_COPIES.md`).
- **The grid** (`MANIFEST_GRID.md`). Release v11 labels and CTs at `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K/`
  (a symlink to `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`); the 2026-09-10 scratch at
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/`; the HOME-root probe scripts and
  `spinopelvic_all.csv`; reader E's J1 table at `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE/`.
- **Repositories** (`MANIFEST_CODE.md`). `CTSpinoPelvic1K` at 7ddfe38 (the extraction scripts, the separability test, the
  article's figure builders); `OpenSpineToolkit` at cb43197 (ostk: `labels_for`, `level_morphometry`, the regression);
  `spinesurg-ct-nnunet` at 097933a, private (reader E tools, `spineps_ids.py`, `eval_gate.py`, PolyPose measurement);
  `openspineconsortium.github.io` (the public level atlas page).
- **Sibling folders of this repository.** 04 (the ostk fixes this folder waits on), 03 (release v11 and the article), 10 (the
  v11 tree on Ceph, SPINEPS stores), 02 (the clean 2-D encoder for the parity comparison), 08 (exact-pose renders), 06
  (re-reads that can move a record), 01 (C-ArmLSpine, the real paired set; Greg-only).

## Traps that bind this project

- **Two label schemes, and mixing them does not raise.** The release is v11 (L1=20 ... L5=24, L6=25, sacrum=26, hips 30/31,
  femurs 32/33). The legacy map puts L1 at 1 and the femurs at 11/12. Resolving a name against the wrong map returns a
  finite, plausible, wrong number ("femur_left" came back T4). Call `ostk.labels.labels_for(volume)`; never import a fixed
  map. `code/ldi/` uses the legacy map by construction and says so in its header.
- **Identifier 29 is retired, and a check on it is not inert.** v11 dissolved the carved S1 back into the sacrum. Anything
  touching the sacrum, the lumbosacral disc or the pelvis is recomputed from v11; anything purely vertebral is unchanged
  (`level_gradients.csv` regenerates bit for bit). `ostk/labels.py` line 64 still maps `"S1": 29`; on a v11 volume a by-name
  call for S1 falls back silently to the whole sacrum, the branch ostk's own docstring calls wrong (`RESULTS_CATALOG.md`
  G.3). Code that gates on 29 goes (`memory/s1-carve-changed-spinopelvic.md`).
- **The ostk canal-closing regression is open.** Commit 1b7005c inflates posterior body height and end-plate depth by 10 to
  17 mm on about one vertebra in seven with no gate firing; the committed `ostk_level_morphometry.csv` (commit 90a27a7)
  predates it and is right; nothing ostk computed after 2026-09-10 22:52 for VBHp, EPD or EPWl is trusted until 04 fixes it
  (G.2; `memory/ostk-canal-closing-regression.md`). The grid copy `~/OpenSpineToolkit` has no `.git` and its state is
  unknown (OPEN_QUESTIONS B29).
- **Case ids are zero-padded in the release (`0001`) and were not in the old CSVs (`1`).** `zfill(4)` before any join or
  diff. The token is not the record id.
- **Volumes are P,I,R on disk.** Canonicalise to RAS to analyse; never reorient when writing a label
  (`as_closest_canonical` + `nib.save` transposes a label away from its CT).
- **Spread, not the median, catches a broken per-level measurement.** Canal depth and end-plate width both had medians at
  the published means while 21 % of L3 canals read below any living adult and 12 % of L5 end-plate widths walked toward the
  transverse-process span. The checks that worked: the SD against the widest published living-cohort SD; the share below a
  floor against the published prevalence of the condition the floor defines (`docs/LEVEL_MORPHOMETRY.md`).
- **A maximum extent is not a diameter, and a first-slice-that-works is not a plane.** Reproducing a published number means
  reproducing its definition (midsagittal chord, pedicle plane), not just its units.
- **Render the mask.** Three analytically reasonable fixes for L5 end-plate width were all wrong in ways the numbers did not
  show; one render settled it. The reader E regression was found by a render too. Twenty renders before any new number is
  believed.
- **An identity check cannot catch a shared bad landmark.** PI = SS + PT held while sacral slope was 9 degrees low and
  lordosis 12 degrees low on every case. Check outside the computation: published values (Veilleux 2020, Hasegawa 2018,
  Panjabi 1991/1992, Bonczar 2024), an independent implementation, the distribution's shape.
- **The pedicle-width column.** `PDW` is empty in all 4,744 committed ostk rows; the 2026-09-10 shard run produced pedicle
  columns for about two of 5,600 level-instances. The cause is not established and is recorded as unknown (OPEN_QUESTIONS
  D2), not guessed.
- **The HU table is v3-era.** `results/nextpaper/hu_per_vertebra.csv` was computed on v3 labels (2026-05-17); recompute from
  v11 with `labels_for` before any use.

## Standing rules (the programme's, restated for this folder)

1. Never the banned word (the French-derived word for where data came from): write origin, lineage, source, where it came
   from. No fractional version numbers; fold changes into the next integer. Figure captions at most 60 words; the argument
   goes in the text. Plain sentences.
2. Every count, date, path and claim names its file; what no file records is written "not recorded". Say plainly what is
   not known.
3. Check outside the computation. The recurring failure here is a number that is wrong but plausible: published values, an
   independent implementation, the spread rather than the median, a published prevalence, a render.
4. Labels and orientation: two schemes, `labels_for`, identifier 29 retired, `zfill(4)`, canonicalise to analyse and never
   reorient when writing.
5. Held out means the person was never seen by the checkpoint or any ancestor. Every quoted score goes through
   `spinesurg-ct-nnunet/tools/eval_gate.py`. Never quote the leaked banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`,
   `vindrps`). The 2-D side of parity enters only through 02's clean encoder.
6. Pre-register, then score. Write the rule and its success number before the run (every gate in `TODO.md` is pre-stated);
   a number produced before the freeze is calibration. Manuscript numbers enter through a manifest key, never typed.
7. Nothing runs on the grid's login node: every computation is an `sbatch` job; `sbatch -D <dir>`; `afterany` not
   `afterok`; `/dev/shm` for IPC; large outputs under `/rs/rs_grp_oschome/go2432/`; grid bash is 4.2. Submit, estimate the
   wall time, write job ids and ETA to the resume file, stop.
8. SchwingNet and all level-identification code, text, figures and weights stay private; so do `spinesurg-ct-nnunet` and
   `XRSpinoPelvic1K`. Reader E lives in the private repository; this folder holds its results, not the classifier.
9. Use all of a public dataset; fix or justify every truncation in writing before a rerun; identity from metadata first and
   the file name last.
10. On Greg's laptop, network through WSL (`wsl -e bash -lc '...'`); tokens read from files only, never echoed. In the
    code repositories, commit only when Greg asks; CTSpinoPelvic1K pushes to `origin` and `osc`, OpenSpineToolkit on
    `main` to both. In spine-program itself the account doing the work pushes only its claim branch `claude/<issue>` and
    the pull request merges as root `CLAUDE.md` rule 10 says.
11. Ashley Schehr is a person, never a product name. The affiliation is General Surgery (Wayne State University School of
    Medicine / Detroit Medical Center), never Neurosurgery.

## How to be useful here

When a tidy explanation presents itself, test it before believing it: the 28 % identity violations had an innocent reading
(anteverted pelvis, lost sign) that was wrong; the distribution showed a second surface. The 3.4-degree sacral-slope gap had
a frame explanation that failed on sign; the v11 table shows the gap is 0.1 (`RESEARCH_DIRECTIONS.md` CT-2, extracted in
`TODO.md`), so the first step of CT-2 is to recompute the gap before fitting anything. Record what was not explained
(the PDW column) rather than a guess at its cause; the 221-against-222 carve count was such an item until 2026-10-08, when
reading the CSV showed a comparison operator and one record at exactly 0.500 (`STATUS.md` F.5).
