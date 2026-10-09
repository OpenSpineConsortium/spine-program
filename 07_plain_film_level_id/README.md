# 07_plain_film_level_id: plain-film level identification and the radiograph corner detector

Rank 7 of 12 projects in `spine-program` (`_plan/PLAN.md` section 1). Reader: Greg-only. Built
2026-10-08 from the laptop folders, the memory notes and one read-only pass over the grid; nothing on
the grid was written, and nothing here is imaging data or a model weight.

## What this is

The plain-radiograph line of the programme: a corner detector and a level-naming model for standing
and film radiographs, the synthetic-radiograph dataset that supplies exact end-plate corners
(XRSpinoPelvic1K), the student review Space that corrects pseudolabelled films, and the regulatory route
to hospital radiographs. The intraoperative C-arm work (`01_carm_level_detection`) grew out of this
line and now owns the encoder lineage and the body detector; this folder keeps what is specific to
plain film and the record of what the early film models claimed and why those claims were retired.

## Goal

A quotable, held-out account of corner localisation and level naming on plain radiographs, carried
onto the v11 label release, and one paper from it: XRSpinoPelvic1K corner detection and film
spinopelvic measurement against the published baseline (Bansal et al., PLoS One 2026, e0347290,
`docs/journal.pone.0347290.pdf`). Secondary: the amendment-47 route that lets students evaluate the
same methods on de-identified Detroit Medical Center trauma radiographs.

## State on 2026-10-08

**What is complete and quotable.**

- Corner localisation on 301 held-out BUU-LSPINE films (patient-grouped 1398 / 301 / 301 split,
  `buu_splits.json` in the XRSpinoPelvic1K repository): YOLOv8l-Pose at 1024 px puts 92.4 % of corners
  within 0.55 % of the image diagonal, 99.3 % within 1.10 %, 99.8 % within 1.66 %, against 75.6-76.8 %
  for the three published models at the strict threshold once their 640 px thresholds are converted
  to a fraction of the diagonal; median error 0.203 % of the diagonal
  (`docs/xrspinopelvic1k/docs/RESULTS.md` section 1.2). Sacral slope ICC(2,1) 0.952, MAE 2.01 degrees,
  94 % within 5 degrees; lumbar lordosis MAE 3.75 degrees; corner-identity macro-F1 0.999-1.000
  (sections 2-3). These numbers were produced by the repository's own evaluator on its own split; they
  did not pass through `eval_gate.py` and are not in `RESULTS_CATALOG.md` (`STATUS.md` section 1b).
- The detect_v1 field report (2026-09-02): AP50 0.957, PCK@0.1 0.768, PCK@0.2 0.917 on 558 held-out
  instances (NHANES 294, Mendeley 249, BUU 15); 111 epochs, final box mAP50 0.980, pose mAP50-95 0.901
  (`results/spine_detector_report/metrics.json`, `results.csv`). Superseded on the grid by detect_v2
  (AP50 0.970, PCK@0.1 0.812, PCK@0.2 0.942 on the same 558; `memory/xray-corner-detector-status.md`,
  DATED) and later by detector_v5z, the SchwingNet body detector owned by folder 01.
- The held-out film N-curve (`docs/handoff/RESULTS_CATALOG.md` A10): a render-only encoder fine-tuned
  on N persons per corpus and scored on the v9 validation persons of that corpus, which no cell ever
  trained or selected on. NHANES II 27.2 to 92.7 %, BUU 10.3 to 96.9 %, CSXA 3.2 to 99.8 % from N = 0
  to every person (A10.1-A10.3). Renders raise naming by +21.9 / +11.1 / +18.7 points at 5 persons and
  hurt BUU by 1.6 points at every person (A10.6, A10.8). Seeds 1-2 exist only at N <= 25.
- Render-trained against film-trained detection on 17 unseen NHANES II lumbar spines: 99.4 % against
  67.7 % at confidence 0.05, +31.7 points [21.0, 45.4] (A14.1).

**What is retired.** Every early film-naming headline: 96.7 / 98.8 / 99.1 % on the context ladder
(C1.1, cervical-dominated `films_ann`); 98.69 / 99.13 / 99.41 / 99.48 % for the recurrent head (C1.2,
`films_ann`, attributed to `films_all2` in two source files); 97.47 % and the "shortcut-free" 99.02 %
(C1.6, allspine v2, NHANES pooled twice); 99 % at 35.7 % coverage (C1.8, leaked bank, own test half);
the 2026-09-17 fraction sweep (C2.1, selection split on v2). `STATUS.md` lists each with its
replacement.

**What is open.** The XRSpinoPelvic1K `data/ct` and `data/labels` links dangle on a deleted export
built from 822 pre-release cases (DATA_MANIFEST defect 36); the repository tracks a Cerner `.ica` file
and a `.crdownload`; the BUU licence reading is undecided; the VinDr determination number is not
recorded (OPEN_QUESTIONS A5); the BIBM 2026 (5 July) and SPIE MI 2027 (5 August) windows passed with no
submission recorded (`docs/handoff/MANUSCRIPTS.md` section 10; OPEN_QUESTIONS A8); amendment 47 to
IRB-21-10-4123 is drafted, with its record count [N] unfilled, and not recorded as submitted
(`regulatory/`); no held-out per-level film table exists (OPEN_QUESTIONS C4); the competitor ensemble
result is in no repository document (C1.17).

## Success criteria

1. XRSpinoPelvic1K rebuilt from the v11 labels through `ostk.labels.labels_for(volume)`; five DRRs
   rendered with projected corners, overlaid and looked at; the S1 plate fitted in 3-D and projected
   within 0.6 degrees of the ostk sacral slope (the repository's own standard, `README.md` of
   XRSpinoPelvic1K); the tracked `.ica` and `.crdownload` purged from history and from the grid clone.
2. No document in this folder or in the repositories quotes 97.47, 99.02 or 98.7-99.4 % as held out;
   `slurm/recurrent_head.sh` line 16 and `tools/recurrent_order.py` line 56 of `spinesurg-ct-nnunet`
   say `films_ann`, not `films_all2`.
3. Greg's written BUU licence reading and the VinDr determination number (or a written VinDr
   exclusion) on file before any BUU-trained weight leaves the grid.
4. Amendment 47 approved, its scope sentence written into this README.
5. The paper: every number regenerated from a result file through a manifest key on the v11 rebuild;
   every held-out claim through `eval_gate.py`; the two-click femoral-head annotation protocol stated;
   the BUU-all reversal (A10.8) confirmed or refuted on three seeds; venue chosen by Greg (SPIE Medical
   Imaging 2027 or the Journal of Imaging Informatics in Medicine).

## How it relates to the other projects

- `01_carm_level_detection` owns the shared level-encoder lineage (allspine v9), the body detector
  (`detector_v5z_final`) and the local `spine-detector/src/` snapshot; the film N-curve is printed in
  its paper 1 (Figure 5b). This folder cites those and does not duplicate them.
- `03_ctspinopelvic1k_dataset` supplies the v11 labels the rebuild needs.
- `04_openspinetoolkit` supplies `ostk.project2d`, `ostk.drr`, `ostk.spine.endplate_corners` and
  `ostk.metrics2d`; XRSpinoPelvic1K pins `OSTK_REF` 09dd9c5 (`docs/xrspinopelvic1k/docs/HPC.md`).
- `05_ct_morphometry_parity` runs PAR-2 (projected morphometry at exact pose) on the v11 corners that
  this folder's rebuild produces (`docs/handoff/RESEARCH_DIRECTIONS.md` section 6, ranks 2 and 7).
- `08_render_devices` owns the DRR physics and device cards; the DRR-to-film gap measured here
  (RESULTS.md section 4) is one of its inputs.
- `10_data_platform_grid` runs batches B04 (the film corpora and the detector tree), B05
  (XRSpinoPelvic1K data), B10 and B11 (the banks); nothing here cuts over until it says so.
- `11_students_grid_access` holds the student roster and the review-Space repository ids; this folder
  holds the Space's code and the maintainer recipe.
- `99_archive` holds the superseded decks and plans; the RECORD ONLY material kept here
  (`results/track5_results/`, `results/lumbar_diag_2026-09-16/`) stays here because the retirement of
  the early numbers is part of this folder's record.

## Layout

```
CLAUDE.md  README.md  STATUS.md  TODO.md  MEMORY.md
MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md
memory/                       36 notes with status headers; COPIED_AT.txt (one note carries two <laptop:...> tokens)
docs/handoff/                 the 2026-10-08 handoff (12 documents, literature_state/, working_notes/)
docs/xrspinopelvic1k/         README, CITATION, LICENSE, docs/*.md, docs/figures (2 DRRs), annot/README
docs/journal.pone.0347290.pdf Bansal et al. 2026 (CC BY)
results/spine_detector_report/   detect_v1 report (BUU thumbnails removed); 3 renders kept, 37 by path
results/corner_detector_buu/     per-corner errors on 301 BUU test films, YOLO11n summary
results/lumbar_diag_2026-09-16/  mid-lumbar error diagnosis (RECORD ONLY)
results/track5_results/          band-transfer reports (RECORD ONLY, wrong bank)
figures/buu_vs_drr/              agreement, Bland-Altman, CED, corner-identity, Roussouly plots
code/review_space/               the student film-review Space (app, Dockerfile, READMEs)
code/context_ladder.py  code/eval_shortcut_controls.py   copies with their source commit
regulatory/                      amendment 47 to IRB-21-10-4123, redacted drafts and a README
```
