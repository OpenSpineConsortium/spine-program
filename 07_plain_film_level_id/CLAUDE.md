# 07_plain_film_level_id: working context

Plain-film level identification and the radiograph corner detector, the line the intraoperative
C-arm work (folder `01_carm_level_detection`) grew out of. Reader: **Greg-only** (level-identification
code, a private repository, regulatory drafts that name roles), for claiming and hand-outs, not for reading: every
Write holder may read this folder, and a student takes an issue here only after Greg hands it out, with a comment
naming the student's login or by removing the label `greg-first` (Greg's answer of 2026-10-12, issue #68). This folder is one project of the
`spine-program` repository; `_plan/PLAN.md` section 3, project 07, is the division it was built from
on 2026-10-08.

## The goal in one paragraph

Name the vertebral level and locate the four end-plate corners on plain radiographs, with every quoted
number held out by person and traceable to a file. The assets are: the spine-detector corpus and its
detectors (the detect_v1 field report is in this folder: AP50 0.957 on 558 held-out instances,
`results/spine_detector_report/metrics.json`; detect_v2 is on the grid: AP50 0.970, PCK@0.1 0.812,
`memory/xray-corner-detector-status.md`); XRSpinoPelvic1K, DRRs of CTSpinoPelvic1K with four end-plate
corners fitted in 3-D and projected, and a YOLO-pose corner detector trained on BUU-LSPINE that puts
92.4 % of corners within 0.55 % of the image diagonal on 301 held-out BUU films with a sacral-slope
ICC(2,1) of 0.952 (`docs/xrspinopelvic1k/docs/RESULTS.md`); the held-out film N-curve, NHANES 92.7 %,
BUU 96.9 %, CSXA 99.8 % at every training person (`docs/handoff/RESULTS_CATALOG.md` A10.1-A10.3);
the student film-review Space (`code/review_space/`); and the amendment-47 route to Detroit Medical
Center trauma radiographs (`regulatory/`). The first job is to retire every leaked early film number
(97.47, 99.02 and 98.7-99.4 % are LEAKED or wrong-bank: `STATUS.md`). The paper this folder can write
is the corner-detection and film spinopelvic-measurement paper, from `RESULTS.md` recomputed on the
v11 rebuild (`TODO.md` step 5).

## Read first

1. `README.md`: what this is, the state on 2026-10-08, the success criteria.
2. `STATUS.md`: every result in hand with its id, its file and its rigor mark; what is superseded and
   by what.
3. `TODO.md`: the ordered steps, each with its gate, its pre-stated number, its dependency and who
   decides.
4. `MEMORY.md` and `memory/`: 36 notes with their statuses. A LEAKED or RECORD ONLY note is history,
   never the source of a quotable number.
5. `MANIFEST_GRID.md`, `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md`: where everything this folder does not
   hold lives.
6. `docs/handoff/README.md` section 5 (the ten rules) and `docs/handoff/RESULTS_CATALOG.md` "How to
   read a row" (the status words and rigor marks used in `STATUS.md`).

## Where things are

- **This folder.** `docs/handoff/` (the twelve handoff documents of `spinesurg-ct-nnunet` at 097933a
  plus `literature_state/` and `working_notes/`, with researcher e-mail addresses withheld; the 36
  context notes that bear on this folder are in `memory/`; `HANDOFF/context/`, `GREG_ONLY/` and
  `working_notes/builders/` are not here); `docs/xrspinopelvic1k/` (the XRSpinoPelvic1K documents at
  commit 4f22935); `docs/journal.pone.0347290.pdf` (Bansal et al. 2026, the published baseline);
  `results/spine_detector_report/` (detect_v1, 2026-09-02); `results/corner_detector_buu/` (per-corner
  errors on the 301 BUU test films); `results/lumbar_diag_2026-09-16/` (RECORD ONLY);
  `results/track5_results/` (RECORD ONLY, wrong bank); `figures/buu_vs_drr/`; `code/` (the review
  Space, the context ladder, the negative controls); `regulatory/`; `memory/`.
- **The grid.** HOME `/wsu/home/go/go24/go2432` and Ceph `/rs/rs_grp_oschome/go2432`. The film
  corpora and the detector tree: `/wsu/home/go/go24/go2432/spine-detector` (382 GB by the 2026-09-19
  du; migration batch B04 was copying to Ceph at 22:20 UTC on 2026-10-08). The XRSpinoPelvic1K
  checkout: `/wsu/home/go/go24/go2432/XRSpinoPelvic1K` (22.428 GB census; batch B05 not started; its
  `data/ct` and `data/labels` links dangle). The films in render format:
  `/wsu/home/go/go24/go2432/films_drr` (36 GB). The film N-curve outputs:
  `/rs/rs_grp_oschome/go2432/data/or_ready/film_ncurve`. Every path with what it holds, its size where
  a file records one, its migration state and whether a job verified it: `MANIFEST_GRID.md`.
- **Repositories.** `spinesurg-ct-nnunet` (private, branch `L6_Class`, 097933a); `XRSpinoPelvic1K`
  (private, `main`, 4f22935); `OpenSpineConsortium/spine-detector` (private; commit not recorded);
  `CTSpinoPelvic1K` (public, `master`, 7ddfe38); `OpenSpineToolkit` (public, `main`, cb43197). URLs,
  branches and the files that matter: `MANIFEST_CODE.md`.
- **Sibling folders.** `01_carm_level_detection` (the encoder lineage, the body detector and the
  `spine-detector/src/` snapshot), `03_ctspinopelvic1k_dataset` (the v11 labels), `04_openspinetoolkit`
  (`ostk.project2d`, `ostk.drr`, the end-plate fit), `10_data_platform_grid` (batches B04, B05, B10,
  B11 and the one read-only grid pass of 2026-10-08).

## Prefixes in the copied documents

The handoff files under `docs/handoff/` were written inside the `spinesurg-ct-nnunet` repository and
use its path prefixes. In this folder they resolve to repositories, never to a laptop:

| prefix | resolves to |
|---|---|
| `ssn:` (also `sscn/`, `[SSN]`, `S/`) | `spinesurg-ct-nnunet`, private, branch `L6_Class`, commit 097933a (`MANIFEST_CODE.md` section 1) |
| `sn:` | `ssn:SchwingNet/` |
| `ctsp:` (also `ctsp/`, `[CTSP]`, `C/`) | `CTSpinoPelvic1K`, public, `master`, 7ddfe38 (section 4) |
| `ostk:` (also `[OSTK]`) | `OpenSpineToolkit`, public, `main`, cb43197 (section 5) |
| `xrsp:` | `XRSpinoPelvic1K`, private, `main`, 4f22935 (section 2) |
| `sdet:` | `OpenSpineConsortium/spine-detector`, private (section 3) |
| `students:` | `ctsp:Student_Projects/` |
| `np:`, `bth:` | laptop folders owned by folders 03 / 99 and 11; nothing here reads them |
| `context/`, `mem:` | the redacted memory copies in `HANDOFF/context/` of `spinesurg-ct-nnunet`; the 36 that bear on this folder are in `memory/` |
| `~`, `$HOME` | the grid HOME `/wsu/home/go/go24/go2432` |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `<repo:...>`, `<laptop:...>` | bracketed tokens the builder substituted for literal laptop spellings in the handoff copies (`MANIFEST_LOCAL.md` section 1); a `<laptop:...>` token names something this folder does not depend on |

## The standing rules, in this folder's words

1. **Words.** Never the word Greg bans for where data came from (the French-derived one): write
   origin, lineage, source, or where it came from. No fractional version numbers; fold a change into
   the next integer version. Figure captions at most 60 words; the argument goes in the text. Plain
   sentences. The affiliation is the Department of General Surgery, Wayne State University School of
   Medicine / Detroit Medical Center, never Neurosurgery. Ashley Schehr is a person, never a product
   name.
2. **Every number carries its file.** A count, a date, a path or a claim names the file it comes from.
   What no file records is written "not recorded". Say plainly what is not known.
3. **Check outside the computation.** The recurring failure in this programme is a number that is
   wrong but plausible: three estimators produced finite, reasonable values from the wrong bone, the
   wrong surface or the wrong label map, and none raised. Compare with a published value, an
   independent implementation, the spread of the distribution (not its median), a published
   prevalence; render the mask and look. In this folder the same failure wore a different coat: the
   98.7 / 99.1 / 99.4 % recurrent head was a 14-class number on a cervical-dominated bank, attributed
   to the wrong bank in two source files (`STATUS.md` C1.2).
4. **Labels and orientation.** Two label schemes exist and mixing them does not raise: "femur_left"
   resolved against the wrong map comes back T4. Call `ostk.labels.labels_for(volume)`; never import
   a fixed map. In release v11 identifier 29 is retired; anything that gates on 29 goes. Zero-pad case
   ids with `zfill(4)`. Canonicalise to RAS to analyse; never reorient when writing a label. The
   XRSpinoPelvic1K rebuild (TODO step 1) is where this folder meets all four.
5. **Held out means the person was never seen** by the checkpoint or any ancestor; a render inherits
   its CT's person; unknown is not clean. Every quoted score goes through `tools/eval_gate.py` of
   `spinesurg-ct-nnunet`. Never quote from the leaked banks: allspine v2, v6, v7, v8 for VerSe,
   `anchor_drr`, `vindrps`. The BUU levels are counting-inferred, so a BUU "level" number measures
   position, not identity (`memory/context-ladder-2d-level-experiment.md`).
6. **Pre-register, then score.** Write the rule and its success number before the run; a number
   produced before the freeze is calibration. Numbers enter a manuscript through a manifest key, never
   typed.
7. **Nothing runs on the login node.** Every computation, render, plot and download is an `sbatch`
   job; `sbatch -D <dir>`; `afterany`, not `afterok`; IPC under `/dev/shm`; large outputs on Ceph; grid
   bash is bash 4.2; no container command on the login node and nothing of ours under its `/tmp`.
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights,
   this folder included, stay private. The XRSpinoPelvic1K repository stays private until its history
   is purged (TODO step 1). No weight trained with BUU laterals leaves the grid until Greg has read the
   BUU licence (TODO step 3).
9. **Data.** Use all of a public dataset; fix or justify in writing every truncation before a rerun;
   identity comes from metadata first and the file name last; FluoroCap is out of training. BUU-LSPINE
   images and crops are never redistributed (DATA_MANIFEST card `buu_lspine_3600`, quoted in
   `MANIFEST_LOCAL.md`); VinDr-SpineXR stays on the grid under its DUA.
10. **Git, network, credentials.** On Greg's laptop, network through `wsl -e bash -lc '...'`. Tokens
    are read from files, never echoed, never on a command line. In the code repositories this folder
    names, commit only when Greg asks; in spine-program itself the account doing the work pushes only its
    claim branch `claude/<issue>` and the pull request merges as root `CLAUDE.md` rule 10 says. Write scripts as files
    and run them by path (heredocs collapse backslashes).

## Traps that bind this project

- **The leaked numbers look best.** 97.47 % at three vertebrae and the "shortcut-free" 99.02 % are on
  allspine v2, which pooled NHANES II twice (`STATUS.md` C1.6). 98.69 / 99.13 / 99.41 / 99.48 % at
  3 / 5 / 7 / 9 vertebrae are on `films_ann_fov96_ctx`, a cervical-dominated bank with 14 of 27
  classes live, and two source files still say `films_all2` (`STATUS.md` C1.2; TODO step 2). 99 % at
  35.7 % coverage was computed on the leaked v2 bank and its own test half (C1.8). The held-out film
  number is the film N-curve (A10.1-A10.3), and its endpoints may not be plotted beside the
  selection-split A5 numbers (A10.12).
- **No held-out plain-film naming exists in paper 1** (A15; EVAL_LEAKS L4): every annotated patient of
  CSXA, BUU and NHANES is in the v8 encoder's training or selection split. The N-curve's render-only
  encoder is the clean one.
- **The S1 end-plate cannot be fitted from a 2-D silhouette.** The ala superimposes on the body and
  the fit is 26-32 degrees wrong at every slab fraction; fitted in 3-D and projected it is within 0.6
  degrees (`docs/xrspinopelvic1k/README.md`). That is why XRSpinoPelvic1K is generated from CT and
  why its rebuild must come from the v11 labels through `labels_for`.
- **A horizontal flip destroys the corner head.** It swaps the anterior and posterior corner slots and
  the head silently fails to converge; `fliplr=0.0` and `mosaic=0.0` are deliberate
  (`MANIFEST_CODE.md`, spine-detector `src/train.py`; Bansal's Table 11 measured the same).
- **Anisotropic resize distorts every angle.** A true 45-degree plate rendered at 58.7 degrees until
  the loaders letterboxed (`docs/xrspinopelvic1k/docs/RESULTS.md` section 5). Checkpoint selection on
  validation loss kept the untrained heatmap network; select on landmark error.
- **The detector does not extrapolate above L1** (0.10 extra detections per film) because BUU labels
  L1-S1 only, so every thoracic vertebra was a positive example of background (RESULTS.md 4c). A
  single pass finds 0 of 6 vertebrae at standing framing f = 0.36; tiling holds 5.45 of 6 (4b).
- **Mixing DRRs into film training made real-film accuracy worse on every column**, and a pelvis class
  trained only on DRRs fires on 40 of 40 DRRs and 0 of 40 films (RESULTS.md section 4). The DRR
  pseudo-label route to thoracic corners is open only once the synthetic-to-real gap is measured and
  closed.
- **The 2026-09-17 fraction sweep is unsafe to rerun as written**: `slurm/scaling_sweep.sh` writes to
  paths that do not depend on `BASE` and skips existing outputs, so a v9 rerun can silently re-emit
  the v2 curve; even a clean rerun is a selection-split number (`docs/handoff/RECIPES.md` section 1.8;
  OPEN_QUESTIONS F21).
- **The XRSpinoPelvic1K checkout tracks a Cerner `.ica` session file and a `.crdownload`** at 4f22935
  and on the grid clone; purge the history before any visibility change (TODO step 1). Six more `.ica`
  files sit untracked beside it; none is copied anywhere.
- **The film N-curve chain resumes, it does not reproduce.** Its outputs sit at a fixed Ceph path with
  DONE markers; to reproduce, move the directory aside or copy the scripts with a new `FN`
  (`docs/handoff/RECIPES.md` section 2.1).
- **`render/` montages and best/worst overlays are BUU film pixels** and were left on their source
  paths (`MANIFEST_LOCAL.md`); the numbers behind them are in this folder.
