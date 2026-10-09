# 05_ct_morphometry_parity

CT morphometry of CTSpinoPelvic1K, the spinopelvic estimator, and 3-D to 2-D parity. Project 5 of 12 in the spine programme
of the Open Spine Consortium (Wayne State University School of Medicine / Detroit Medical Center, Department of General
Surgery). Built 2026-10-08 from `../_plan/PLAN.md` section 3 (05) and the 33 rows of `../_plan/DISPOSITION.tsv` routed here.

## What this is

CTSpinoPelvic1K is a CT dataset of 802 abdominopelvic records with per-level vertebrae, ribs, sacrum, hips and femora in one
coordinate frame (release v11, Zenodo 10.5281/zenodo.22797014: `docs/handoff/INFRASTRUCTURE.md` line 45 and `docs/handoff/README.md` line 368;
the measurement rows are `docs/handoff/RESULTS_CATALOG.md` Part F). Its measurement
tables are the evidence behind the dataset article: per-level body heights, end-plate widths, canal width and depth, pedicle
width, disc height and trabecular attenuation (`results/morphometrics/level_gradients.csv`, `surgical_morphometrics.csv`,
`level_atlas.csv`), the spinopelvic angles (pelvic incidence, sacral slope, pelvic tilt, lumbar lordosis), the pelvic-shape and
transitional-anatomy columns, and the reference tables transcribed from the literature (`level_references.csv`,
`panjabi_reference.csv`, `pedicle_width_references.csv`). This folder owns the correctness of those numbers and the one
question they were built to ask: which features of a single vertebra name its level, and which of them survive projection
into the 2-D views a surgeon sees.

## Goal

1. Close the three open items of the spinopelvic estimator (`docs/SPINOPELVIC_ESTIMATOR.md` "Still open"): the eight
   prosthetic femoral heads, the 10 to 15 degree pelvic-incidence shift with the S1 choice on transitional spines, and the
   unmeasured anterior pelvic plane (`TODO.md` step 2).
2. Recompute the sacrum-adjacent tables on v11 with `labels_for` (`RESULTS_CATALOG.md` F.44; `TODO.md` step 3).
3. Revise the level atlas so the withheld L5 end-plate width and L5 pedicle width can be reported (F.34; `TODO.md` step 5).
4. Run the parity programme PAR-1 to PAR-6: a single-vertebra 3-D target first (PAR-1, one laptop hour), then projected
   morphometry at exact pose on all 802 v11 volumes (PAR-2), then the real paired sets with 01 (PAR-4, PAR-5), then any
   feature-engineering arm Greg decides on (PAR-6).

## State on 2026-10-08

- The v11 spinopelvic table stands on 756 of 802 records: PI 52.1 +/- 11.1, SS 36.6 +/- 10.6, PT 15.5 +/- 7.9 against
  Veilleux 2020's 52.1 / 36.5 / 15.6 (`results/morphometrics/surgical_morphometrics.csv`; F.21). Four estimator defects are
  fixed and documented (F.22, F.23); three items are open (F.25).
- The per-level atlas is current for T11 to L4 on every measure and withholds L5 for end-plate width and pedicle width
  (F.34, F.36). Canal depth was rewritten after the spread test (F.33). Body height sits about 6 mm above Panjabi 1992 and
  that is the cohort, not the method (F.35).
- T12 against L1 separate on shape alone at AUC 0.990 over 1,486 vertebrae, within patient (F.28; rerun 2026-10-08). The
  ratio-only single-vertebra number, which parity must be measured against, is not on disk.
- Reader E (ostk morphometry over five mask families, 3,524 CT-mask pairs, 38,432 instance rows) stopped at its J2 spread
  gate: the first pass failed on canal depth and lower end-plate width; after the features v3 rerun only lower end-plate width
  fails, for want of a published lower-plate yardstick (`results/reader_e/J3_NOT_SUBMITTED.md`, `j2/J2_GATE.md`,
  `j2v3/J2_GATE.md`). J3 was never submitted. Whether anything ran after 2026-09-25 is not recorded.
- Four CSVs written on v10 labels wait on v11 (F.44). The ostk canal-closing regression (G.2) and the silent S1 fallback
  (G.3) are open in OpenSpineToolkit cb43197 and belong to 04.
- The grid holds the 2026-09-10 scratch (VERIFIED on Ceph in batch B14), the HOME-root probe scripts (not in any
  repository), and reader E's J1 table (Ceph-native). See `MANIFEST_GRID.md`.

## Success criteria (pre-stated; each with its file)

| item | number that counts as success | where it is checked |
|---|---|---|
| PAR-1 | ratio-only T12 vs L1 AUC at or above 0.95 means a single-vertebra target exists; 0.90 to 0.95 one body plus a neighbour; below 0.90 a window of three or more; the dominant weight stays on the transverse-process span and every weight sign agrees with Panjabi 1991 Table 3 | `TODO.md` step 1; `results/morphometrics/panjabi_reference.csv` |
| CT-2 | the v11 gap to Veilleux is confirmed at 0.1 degrees, not 3.4, before any fit; the APP angle's median lies inside the published supine band +5.1 to +12.2 degrees, or the extraction is wrong | `TODO.md` step 2 |
| F.44 recompute | no column reads identifier 29; per-level SD inside the widest published living-cohort SD; share below a floor against published prevalence; twenty masks rendered | `TODO.md` step 3 |
| PAR-2 | per-feature ICC tiers 0.75 / 0.50 with the case-clustered lower bound above 0.60; junction AUC per view 0.970 / 0.90 | `TODO.md` step 4 |
| CT-5 | a corpus-label rule ships only if it beats the shipped rule on all three columns `LEVEL_MORPHOMETRY.md` uses | `TODO.md` step 5 |
| reader E J3 | the J2 gate passes on both the number rule and the render rule; the G3 test transitional persons are asserted out of training | `results/reader_e/J3_NOT_SUBMITTED.md` |

## How it relates to the other projects

- **04_openspinetoolkit** blocks the ostk-based numbers: CT-1 (the canal-closing fix, tested on record 0097 within 1 mm)
  and the S1 fallback flag. Reader E's SCD/SCW were re-read on the release recipe for this reason.
- **03_ctspinopelvic1k_dataset** owns release v11, the dataset article and its Figure 3; the four morphometry documents are
  copied into both folders. The article's caption still says Panjabi values were "digitised from Figure 4A" while Table 3 was
  obtained (F.38): 03's resubmission item, this folder's fact.
- **10_data_platform_grid** owns the v11 tree on Ceph, the SPINEPS and TotalSegmentator stores reader E reads, and
  `tools/spineps_ids.py`.
- **02_transitional_naming_truth** supplies the clean 2-D encoder the parity comparison needs; one CTSP render is unseen by
  the v9 chain (`docs/handoff/LEAKAGE.md` line 64, `tools/unseen_cases.py`), so no CTSP person can be treated as held out for a
  v9-lineage model and no 2-D number is quoted here until then.
- **08_render_devices** supplies exact-pose renders for PAR-2; **01_carm_level_detection** holds C-ArmLSpine for PAR-4 and
  PAR-5 (Greg-only); **06_transitional_ct_census** re-reads can move a record and change the G3 split; **09** needs the
  iliac-crest number recomputed on v11 (F.41).

## Layout

```
CLAUDE.md  README.md  STATUS.md  TODO.md  MEMORY.md  MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md
memory/              25 notes with their HANDOFF/context/INDEX.md status on line 1
docs/                the four morphometry documents; external/ (a literature map, unverified); handoff/ (eight files + `ABOUT_THESE_COPIES.md`)
results/morphometrics/   every measurement table of CTSpinoPelvic1K 7ddfe38 (annotator names excluded) + tp_height_renders/
results/reader_e/        reader E: code map, cases, timings, J0/J1 JSON, J2 gates, diag/, smoke/, verify_corners/, j2/, j2v3/
results/nextpaper/       hu_per_vertebra.csv (+ xlsx), v3-era labels
figures/measure_diagrams/ measure-definition drawings (m4..m9, measures, measures2, measures3)
code/ldi/                the independent lordosis / LDI implementation (no git; legacy label map)
```

## Prefix keys used inside the copied documents

The handoff files and the memory notes were written with path prefixes. In this repository they resolve to
`MANIFEST_CODE.md` entries, not to any laptop: `ctsp:` = CTSpinoPelvic1K at 7ddfe38; `ostk:` = OpenSpineToolkit at cb43197;
`ssn:` = spinesurg-ct-nnunet at 097933a (private); `sn:` = `ssn:SchwingNet/`; `mem:` and `context/` = `memory/` here (or the
owning folder's `memory/`); `HOME` or `~` = `/wsu/home/go/go24/go2432`; `$RS` = `/rs/rs_grp_oschome/go2432`. Where an original spelled an absolute laptop
path, the copy here carries a marker instead (`<laptop Desktop>/`, `<laptop home>/`, `<laptop memory folder>/`,
`<laptop vendor folder, never read>`, `<laptop Temp scratchpad, swept>/`); `docs/handoff/ABOUT_THESE_COPIES.md` and
`MANIFEST_LOCAL.md` section 2 list every substitution. No laptop path remains in this folder outside `MANIFEST_LOCAL.md`.
