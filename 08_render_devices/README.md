# 08_render_devices: image formation, DRR banks, device cards, PolyPose and synthetic-to-real

Rank 8 of 12 in the spine-program triage (`../_plan/PLAN.md` section 1). Reader: Greg-only until Greg confirms.
State written 2026-10-08.

## What this is

The rendering side that feeds every 2-D model in the programme. It holds the records, results and inventories of
five lines of work from spinesurg-ct-nnunet (commit 097933a):

1. **The DRR banks.** Physics renders (perspective, polychromatic, scatter, noise, 640 px) of CTSpinoPelvic1K,
   VerSe, TotalSegmentator and synthetic-implant CTs: `physics_drr` 7,045 annotations (ctsp 2,430, totalseg 1,831,
   verse 1,463, implant 1,321) and `physics_rare` 1,482 annotations of 81 transitional subjects (34 CTSP ids, 47
   VerSe series), the only labelled L6 and T13 at scale; plus the parallel-beam laterals `ctsp_drr` (801),
   `verse_drr` (387), the oblique arcs, the TotalSegmentator benches `ts_drr` (1,170) and `ts_drr_v3` (1,735), the
   anchor renders (7,842) and the styled device corpus (142 TotalSegmentator v3 whole spines, 4,551 files)
   (`docs/handoff/DATASET_USAGE.md` section 3.1 and 3.3; `docs/handoff/LITERATURE_STATE.md` section 1.6).
2. **The device cards.** Nine image-formation terms fitted leave-one-group-out on up to 40 real frames per device,
   with a Gaussian copula and an automatic-exposure regression: Cios Fusion, Elekta XVI, BV Pulsera and PIXIUM 4600
   in `results/devices/`; Surgio-B51 and Varian Halcyon only on the grid (`docs/DEVICE_PARAM_AUDIT.md`;
   `docs/handoff/RESULTS_CATALOG.md` A12.8).
3. **The DeepFluoro calibration.** The decision to calibrate formation rather than learn it: exact geometry
   (0.00 px landmark reprojection) plus attenuation explains 80.9 % of a real frame's attenuation variance over 366
   frames; nine device terms add +4.1 leave-one-specimen-out, +4.3 in the second fit; a learned refiner was better
   on 21 % of frames only (`docs/DEEPFLUORO_FORMATION.md`; `memory/learned-formation-refuted-calibrate-instead.md`).
4. **PolyPose.** The published polyrigid transform (NeurIPS 2025, MIT) reproduced on DeepFluoro (pelvis Dice
   0.992, femora 0.978 and 0.980) and turned into a generator that samples whole sagittal profiles within published
   ranges of motion; fused junctions get zero motion (`results/polypose/REPRODUCTION.md`, `SAMPLING_SPEC.md`;
   `memory/polypose-decision.md`). Its validation file does not exist.
5. **The refuted translation routes and the ratio question.** CycleGAN, ADDA, CUT and SDXL img2img returned no
   gain in any arm; the synthetic:real ratio was never swept here and never swept by any DRR paper
   (`memory/drr-to-fluoro-levers.md`; `memory/fluorogen-synthetic.md`; `docs/Synthetic real ratio X-ray detectors.md`).

## The goal

Keep the renders and cards honest and available, close the four open defects with a number each, and provide
the exact-pose renders that projects 05 and 01 ask for. The folder is not expected to carry a paper on its own.

## State on 2026-10-08

| line | state | the number | file |
|---|---|---|---|
| physics render banks | built; on HOME, in migration batches B10 and B11, whose state since is `../10_data_platform_grid/MANIFEST_GRID.md` section 2 | 7,045 + 1,482 annotations; a second count of 7,048 unexplained | `docs/handoff/DATASET_USAGE.md` 3.1; `docs/handoff/OPEN_QUESTIONS.md` B12 |
| device cards | four shipped, two grid-only; held-out gain positive but criterion C3 not met | R^2 card vs physics: Cios 0.905 vs 0.899, Pulsera 0.952 vs 0.917, Elekta 0.974 vs 0.964, PIXIUM 0.679 vs 0.650; 12-fold gain +0.019 [0.008, 0.033] | `docs/handoff/RESULTS_CATALOG.md` A12.1, A12.2, A12.4 |
| exposure clip | defect known, not repaired; the clip is the default | 1.7 to 5.1 % of the joint reached; 94.9 to 98.3 % of frames pinned | `docs/DEVICE_SPREAD_SWEEP.md`; A12.6 |
| styled-corpus detectors | pre-stated 97 % met on no held-out device; primary criterion never run; box convention of the rows not recorded | Cios 0.9157 to 0.9398; Elekta 0.3024 to 0.3270; Surgio 0.1429 to 0.1498 vertebra recall | `docs/handoff/RESULTS_CATALOG.md` A6.13, C4.6; `docs/handoff/OPEN_QUESTIONS.md` B10, C14 |
| calibration | decision stands; numbers are a record | 80.9 % explained; +4.3 held out; ceiling 99.5 % | `docs/DEEPFLUORO_FORMATION.md` 2, 5; C4.2 |
| corpus manifold | current; three feature spaces reported | styled vs real stays separable: Cios 100 %, Surgio 99.8 %, Elekta 99.0 % [98.1, 99.6] | `results/manifold/probes.json`; A13.3 |
| render ablation (support for 07) | current, held out | +21.9, +11.1, +18.7 points at 5 persons; +12.2, +6.0, +6.2 at 25; BUU -1.6 at every person | A10.6 to A10.8 |
| PolyPose | REPRODUCED; validation not written; generator commit on both checkouts | pelvis Dice 0.992(0.005); VALIDATION.{json,md} absent | `results/polypose/REPRODUCTION.md`; G.6 |
| translation routes | refuted; do not repeat | CycleGAN 6.62, ADDA 6.41 vs 6.44 mm with no adaptation (SyntheX); CUT v2 films-only 12.1 to 14.1 %, render-trained 33.5 to 23.7 % | `memory/drr-to-fluoro-levers.md`; `memory/fluorogen-synthetic.md` |
| synthetic:real ratio | never swept; literature plateau 4:1 to 10:1 | about 1:1 by rows in every trained cell | A10.11; `docs/Synthetic real ratio X-ray detectors.md` |

The full table with rigor marks is `STATUS.md`; what remains is `TODO.md`.

## Success criteria (pre-stated here, from the plan and the open questions)

- **S1.** `MODEL_CARD.md` section 4.6 reconciled with `~/spine-detector/runs/devcorpus/*/scores.json`, with the box
  convention named and the missing `dc_B_held_cios_fusion_s1` row explained or added (OQ B10).
- **S2.** Whether the cards were refitted under `DF_CONVERSION=linear`, read from `$RS/data/or_ready/devices_refit*`
  and written into `STATUS.md` (OQ B9).
- **S3.** The primary C7 criterion: a paired bootstrap of each styled-corpus arm against the LODO baseline on the
  same held-out device; "improves" only if the interval excludes zero, otherwise the sentence "not met" with the
  number (OQ C14).
- **S4.** The exposure-clip A/B on real frames; the default sampler changes only if the interval excludes zero (OQ C17).
- **S5.** `results/polypose/VALIDATION.{json,md}` exists, with the Dice and range-of-motion checks and the
  fused-junction zero-motion check passing (OQ C18).
- **S6.** The synthetic:real ratio array (real share 0.1 to 0.9, N 25 and all, three seeds, L6 scored separately)
  reported as a curve, never one ratio; a cell counts only if it raises held-out L6 recall without lowering
  ordinary film naming by more than the seed spread (1.0 point at full size) (OQ A9, C5; Greg decides).

## How it relates to the other projects

- **01 (C-arm detection to hospital testing)** consumes the cards, the styled corpus and the physics renders; the
  styled-corpus detectors and the pooled detector live under `~/spine-detector/runs/devcorpus`. 01 chooses a
  device card for the hospital's C-arm only if a card is fitted for it; the header-census format in
  `results/devices/census/` is what a hospital device census would reuse.
- **02 (transitional naming)** needs `physics_rare` (the only rare-class renders) and PolyPose variants, and owns
  the clean encoder that step 5 of `TODO.md` waits on.
- **05 (CT morphometry and 3-D to 2-D parity)** needs exact-pose renders of the 802 v11 volumes (PAR-2); the
  renderer is `tools/render_physics_drr.py` and `tools/make_drr_dataset.py` of spinesurg-ct-nnunet.
- **07 (plain-film level identification)** quotes the render ablation (A10.6 to A10.10) and the render-trained
  versus film-trained detector (A14.1).
- **10 (data platform)** owns the migration of every bank named in `MANIFEST_GRID.md` (B06 verified; B07 copying;
  B10 and B11 not started on 2026-10-08).
- **03 (CTSpinoPelvic1K)** supplies the v11 labels; identifier 29 is retired there and any render keyed on it is wrong.

## Folder map

```
CLAUDE.md  README.md  STATUS.md  TODO.md  MEMORY.md
MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md
docs/            physics, device, formation and prior-art records; the ratio report; research_notes/; handoff/
results/devices/ four fitted cards (.json, .3free.json, .frames.csv), eval_gate/, census/
results/manifold/  MANIFOLD.md, pairwise separability tables, overlap.json, probes.json, formation_gap/, examples/
results/polypose/  REPRODUCTION, REPRODUCIBILITY, POLYPOSE_API, SAMPLING_SPEC, cohort files, rom_cine.json, report/,
                 validation/ (the 22-case inspection and one smoke variant of 2026-09-23; no VALIDATION report)
figures/         fig_device_params.png, fig_device_spread.png (and the second params figure the audit cites)
memory/          40 notes with their status headers
code/            nothing copied; README.md points at MANIFEST_CODE.md
```

## On the grid

Since 2026-10-13 (issue #87) `results/` and `figures/` of this folder are symlinks to the same path under `/rs/rs_grp_oschome/shared/spine-program/archive/` on the grid, where the files are read through the link; everywhere else they are read from git history at main 5597197. `../ARCHIVE.md` says how, and how a task that must change one of them brings it back into its branch. The counts and sizes in `MANIFEST_LOCAL.md` describe the folder as it was built on 2026-10-08.
