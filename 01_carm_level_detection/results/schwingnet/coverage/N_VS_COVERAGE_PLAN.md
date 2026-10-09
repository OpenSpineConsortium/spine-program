# Is the plateau purely N, or N plus the acquisition variables of fluoroscopy? The analysis plan

Written 2026-09-24 before any of the new cells were scored. Greg's question (15:30): the fluoroscopy naming curve
plateaus near 90 % while plain-film naming reaches 98-99.9 %; the film corpora are far larger, and the C-arm frames
carry acquisition variables the films do not (positioner angles, tilt, magnification, field, patient position).
Is the gap explained by sample count alone, or by sample count plus those variables?

## What exists (do not recompute)

- `coverage.json`, `COVERAGE.md`, `fig_density.png`, `training_sets.csv`, `points_coverage.csv` (grid job acqcov
  40437098, 11:14-11:30): coverage C_d and normalised entropy H*_d over lat / tilt / roll / magnification / field /
  patient position, per corpus and per training set, bins stated, from DICOM tags where they exist and from pose
  pools for renders; every point of `results/indomain/points.csv` joined to its training set's coverage. Film corpora
  carry no positioner, SID or field tag on disk (section D of COVERAGE.md): their H* is 0 by construction (one view
  protocol each), which is exactly the contrast this plan needs.
- `results/indomain/name_fill.json` (250/250 cells scored, 08:36) and `det_fill.json` (45/45): the C-ArmLSpine
  naming curve, lateral and AP protocols, N in {0, 5, 10, 25, 50, all} C-arm cases, and the detection curves. No
  indomain fill cell is missing (the 07:36 cancellations were re-run by `namefillr` 40436049).
- `tools/indomain_fit_coverage.py`: the fit machinery (AICc on one Gaussian likelihood, partial correlations,
  `--experiment` for the matched-N arms).

## What is being measured now (submitted 2026-09-24, PENDING_JOBS.json beside this file)

**(i) The film N-curve** (`tools/film_ncurve.py`, `SchwingNet/slurm/film_ncurve_*.sh`; grid
`/rs/rs_grp_oschome/go2432/data/or_ready/film_ncurve/`, repo copy `results/coverage/film_ncurve/` after collection).
Naming accuracy on the fixed v9 VAL films of NHANES II, BUU-LSPINE and CSXA against N training PERSONS of that
corpus, N in {0, 5, 10, 25, 50, 100, 200, all}, seeds 0-2 at N <= 25. The recipe is the C-arm curve's, verbatim, with
one substitution forced by the leak rule: the C-arm curve fine-tunes the v9 encoder (which never saw a C-arm frame);
the v9 encoder HAS seen every film training person, so the film curve fine-tunes a new RENDER-ONLY encoder (v9 bank
minus every film row, from ImageNet, the v9 recipe), merged 1:1 with that bank's per-class-600 sample, 15 epochs at
lr 1e-4, then the mixed-length head. The Figure 6 G3-clean encoder is not usable either: its bank holds the film
roots. Test persons are outside every cell's training and selection set and outside the encoder's bank
(`cells.json#check`, per-cell `heldout.verdict`); `tools/rigor_fixes.py a5-rows` runs `tools/eval_gate.py` on the
encoder + head chain before scoring. Every cell scores all three corpora, so cross-corpus points come free.

**(ii) The matched-N low- vs high-coverage render arms** (`tools/coverage_arms.py`,
`SchwingNet/slurm/coverage_arms_*.sh`; grid `.../or_ready/coverage/experiment/`, lists under
`devcorpus/lists/cov_*`, runs under `~/spine-detector/runs/coverage/`). Per device card (Surgio-B51 first, Elekta XVI
second; Cios Fusion deferred: no card in the unseen sweep), three render-only detectors at the same N: `low` = the
existing styled corpus (poses from the real AP/LAT pool, H*_lat 0.20 for Surgio), `high` = N frames whose poses are
drawn from the arc pool only (lat uniform over -90..+90, H*_lat about 0.95), `low2n` = low plus N more real-pool
frames at a second render seed. Same subjects (the 142 clean subjects minus the 40 unseen-sweep subjects), same
card, same trainer, same selection frames, seeds 0 and 1. Scored on the unseen angle sweep (recall per 10 deg bin,
subject-clustered intervals), the real case134 spin (one patient, no interval) and every real test split (the
C-ArmLSpine body-convention re-score), each evaluator through the gate.

**(iii) Indomain fills**: nothing missing; see above.

## The model to fit when the points land

Pool every naming point that is a (training set, accuracy) pair with a known N and a known H*: the C-ArmLSpine
lateral and AP curves (name_fill.json; N = C-arm cases, H* of the C-arm training set from `training_sets.csv`,
which barely moves along that curve because the 13,078-entry base is fixed), the film curves (film_ncurve.json;
N = film persons, H* = 0 by protocol), the matched-N render arms (coverage/experiment/scores.json; N fixed, H*
varies: the one place N and H* are decoupled by construction). Units of N differ between corpora (a C-arm case is two
frames; a film person is one to two films), so N is entered as persons and the corpus as a factor where the model
allows it.

Nested comparison, fitted by `tools/indomain_fit_coverage.py` (extend it with `--film` and the pooled block):

    M0:  acc = A - B * N^(-C)                          (Figueroa inverse power law, the curve the paper already fits)
    M1:  acc = A - B * N^(-C) + g * H*_lat             (the same curve plus a coverage term)
    M1': acc = A - B * N^(-C) + g * H*_joint           (lat x tilt joint entropy, the review's density map)

on one Gaussian likelihood over the pooled points, weighted by each point's interval width; report AICc(M0) -
AICc(M1) and the likelihood-ratio test (1 df), g with its bootstrap interval, and the partial correlation of
accuracy with H* at fixed N. The answer is stated as one of:

- **purely N**: g's interval covers 0 and AICc prefers M0 (or dAICc < 2), AND the matched-N arms show no difference
  on the unseen sweep and the real spin beyond the seed spread;
- **N plus acquisition variables**: g's interval excludes 0 with dAICc >= 2, AND the high arm beats the low arm at
  matched N on the unseen sweep or the real spin by more than the seed spread (the low2n arm says whether more of
  the same bins would have done it).

Two checks that decide whether the pooled fit is even admissible: (a) the film curves must reach their plateau
inside the N grid (if NHANES at N = all is still rising, the film asymptote A is not identified and only the render
arms answer the question); (b) the C-arm curve's H* must not be collinear with N (it is nearly constant; if the
fit's design matrix is rank-deficient the coverage term is identified by the render arms and the film contrast only,
and the report says so).

What the plan cannot do: separate "acquisition variables" from "domain" beyond what the render arms isolate. The
arms vary ONE thing, pose coverage, with the card, the subjects and N held fixed; magnification and field are
card draws, not arm variables; patient position is not recorded in any corpus (COVERAGE.md, PatientPosition).

## Steps for the collect pass (when Greg says "check again")

1. `sacct -j <ids>`; collect only what is COMPLETED (PENDING_JOBS.json has the job ids, output paths and collectors).
2. Film: `scp` `or_ready/film_ncurve/{film_ncurve.json,FILM_NCURVE.md,cells.json}` -> `results/coverage/film_ncurve/`.
3. Arms: `scp` `or_ready/coverage/experiment/{arms.json,scores.json,EXPERIMENT.md,poses_*.json,lists_*.json}` ->
   `results/coverage/experiment/`; the per-arm `unseen/recall_vs_angle.json` and `case134/case134_sweep.json` from
   `~/spine-detector/runs/coverage/<arm>/`.
4. Re-run `tools/acq_coverage.py grid` after adding the `*_arc` and `*_low2` geometries to its render table (its
   `read_renders` iterates the three device names), so the new lists get canonical H* values; until then
   `LIST_INFO.json#lat` carries the same bins computed by `coverage_arms.py lists`.
5. Extend `tools/indomain_fit_coverage.py` with the pooled block above; write `results/coverage/N_VS_COVERAGE.md`
   with the verdict, the number, and the two admissibility checks.
6. Cells that failed: resubmit the array with the same manifest (every step is idempotent and skips DONE cells).
