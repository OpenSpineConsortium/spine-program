# Recipes: regenerating each deliverable

Step-by-step regeneration, in the order Greg named them: the scaling plots; accuracy against the number of samples (the
film N-curve); the anomaly scan; the power calculations; then the DRR banks, the device calibration, the C-ArmLSpine
level experiment, the benchmark suite, the CTSpinoPelvic1K measurements and figures, and the data accounting and
leakage checks.

Every command below is copied from a script header, a result document or a reader note, each named beside it. None was
run on the grid for this handoff; the laptop tests named in §10 were run on 2026-10-08 (README "Verification record"). Path prefixes are those of `RESULTS_CATALOG.md` (`ssn:` spinesurg-ct-nnunet, `sn:` its
`SchwingNet/`, `ctsp:` CTSpinoPelvic1K-1, `ostk:` OpenSpineToolkit, `~` grid HOME, `$RS` = `/rs/rs_grp_oschome/go2432`).

---

## 0. Before any recipe: how work reaches the grid and comes back

1. **Never compute on the login node (warrior).** Every step below that runs Python, renders, trains or downloads is
   an `sbatch` job. Warrior kills python, python3, node, pip, md5sum, rsync, conda, gcc, make, R and others by name;
   no container command on warrior, ever (`context/no-jobs-on-login-node.md`; `context/grid-ssh-second-factor.md`;
   `ctsp:CLAUDE.md` "Grid"). Where a recipe below says `python ...` and names a grid path, wrap it in a job (template:
   `ssn:slurm/paired_sets_properties.sh`). Note: `ssn:CLAUDE.md` still tells you to run `tools/pipeline_state.py` over
   ssh on the login node; that predates the ban; run it in a job.
2. **Ship code by commit.** Commit locally (only when Greg asks); push through WSL (`wsl -e bash -lc 'cd ... && git push'`).
   **The grid can no longer fetch the private spinesurg repository** (2026-10-08; why is not recorded,
   `context/data-platform-migration-2026-10.md`), so `git pull --ff-only` on the grid no longer works. The route that
   did work on 2026-10-08 was `git archive | ssh tar` for `data_platform/` (same note; the exact command line was not
   recorded). Its form, for a committed tree:

   ```bash
   wsl -e bash -lc 'cd /mnt/c/<laptop Desktop>/spinesurg-ct-nnunet && C=$(git rev-parse HEAD) && \
     git archive --format=tar HEAD <paths> | ssh wsu-grid "cd ~/spinesurg-ct-nnunet && tar -xf - && echo $C >> SHIPPED_COMMITS.txt"'
   ```

   `git archive` ships only committed files, so a tool with uncommitted edits ships in its committed state and an
   untracked folder does not ship at all. On 2026-10-08 that applies to `tools/patient_keys.py`,
   `tools/test_patient_keys.py`, `tools/level_prototype.py`, `tools/carmlspine_eval.py` (modified) and
   `tools/transitional_review/` (untracked) (`git status`): commit them first. The grid checkout's own `git log` then
   no longer describes its files; the shipped commit is the last line of `SHIPPED_COMMITS.txt`. Tested only for a
   subfolder; whether `tar` on warrior is tolerated for the whole tree is not recorded. **`make physics`,
   `make physics-submit` and `make physics-fresh` run `git fetch -q origin && git reset -q --hard origin/L6_Class` on the
   grid checkout** (`ssn:tools/reproduce_physics.py` L113-114): today the fetch fails and the script still prints "grid
   is at <old commit>" and submits on the stale tree; if fetching ever works again, the reset discards whatever was
   shipped by archive. The default (polling) mode also runs `squeue` every 120 s from the laptop, against rule 6. Do not
   use them until fetching is restored; `make physics-tables` (no grid) is safe. Earlier record of the pull route: the
   history-only memory note `resume-2026-09-24` (not copied) and `working_notes/topic1_schwingnet_carm_results.md` §9.
3. **Submit with `sbatch -D <dir>`** (a relative `#SBATCH --output` resolves against the submit directory and the log
   folder must exist); chain with `--dependency=afterany:<id>` and let the child check a marker file (`afterok`
   strands chains); write each job id with a timestamp into the project's `JOBS.txt`; scratch under
   `/dev/shm/${USER}_<name>_${SLURM_JOB_ID}` with a cleanup trap (`ctsp:Student_Projects/RECIPE.md` §5 rules 3, 4, 13).
4. **Partitions.** CPU: `--partition=reqp --qos=requeue` (add `--no-requeue` unless the script is re-entrant). GPU:
   `--partition=gmsap,gvohp,galhp --qos=gpu --gres=gpu:1` (`INFRASTRUCTURE.md` §2.4).
5. **Python.** CPU tools: `~/mambaforge/envs/spineps/bin/python`; GPU tools: `~/mambaforge/envs/fluorogen/bin/python`;
   some detector jobs use `~/mambaforge/envs/spinedet/bin/python` (`ssn:slurm/allspine_v9_train.sh`); export
   `PYTHONNOUSERSITE=1` in every job (`ssn:env/README.md`).
6. **Resume is not reproduce.** Most array scripts skip a cell that already has a DONE marker and write to fixed
   directories, so re-submitting the same command **resumes**: only missing cells run, and the recorded cells come back
   unchanged (`sn:results/coverage/PENDING_JOBS.json#rule`). To **reproduce** a recorded run, first move the recorded
   output directory aside (or copy the scripts and change their output variable: `FN` in the film N-curve scripts, `ND`
   in the `name_fill` scripts, `OUT` elsewhere), because several prep jobs also `rm -rf` the shared inputs the recorded
   cells were built from (`sn:slurm/name_fill_prep.sh` L27 removes `folds/drr$K`, `folds/ctx$K` and the fold views on every
   run; `sn:slurm/film_ncurve_prep.sh` L26-33 rebuilds `base_cache`, `base_val` whenever `base_cache/base_train.npz` is
   missing). Submit, estimate, record, stop; do not poll `squeue` in a loop (`context/submit-and-sleep-orchestration.md`).
7. **Results come back** by copying the named files into the repository folder the manuscript reads (`scp` from the
   laptop through WSL; `rsync` would start rsync on warrior, which is killed by name: `INFRASTRUCTURE.md` §13).
8. **Into the manuscript.** A new number enters `sn:numbers_manifest.json` as a key pointing at `file#json-pointer`;
   the prose uses `\RESULT{key}`; `python SchwingNet/tools/results_macros.py --check` fails on a pending key, an unused
   key or a bare result numeral (`sn:RESULTS_BUILD.md`).

9. **Who can run what, and what `~` means.** In every command in this file `~` and `$HOME` mean **go2432's HOME,
   `/wsu/home/go/go24/go2432`**, as in `RESULTS_CATALOG.md`; `$RS` is `/rs/rs_grp_oschome/go2432`; `$RC` is
   `$RS/ruleclass`. In a student's shell `~` expands to the student's own HOME, so a student who copies a command must
   first set `GH=/wsu/home/go/go24/go2432` and write `$GH/...` for every `~/...`, or point it at their own copy. Two
   access rules decide what a student can run at all: `go2432/` below the Ceph gate "stays closed" to students
   (`INFRASTRUCTURE.md` §2.2), and `publish_visibility.sh` keeps VinDr, BUU and every bank holding their pixels
   owner-only (`INFRASTRUCTURE.md` §4). The v9 level bank holds BUU pixels, so the encoder, the film N-curve, the fold
   banks and everything downstream of them run only under Greg's account. Laptop-only sources (two personal folders that stay on the laptop and were never copied,
   the Temp scratchpads, the memory folder) are marked "laptop only" where cited; every laptop path
   starts at `<laptop Desktop>`, and the git remote to clone for each folder is in `README.md` "Getting
   access".

   | section | who can run it as written |
   |---|---|
   | §1.1 rebuild Figure 5 from committed files; §4 power; the laptop tests of §10 | anyone with the private repository (laptop) |
   | §9 CTSpinoPelvic1K | a student, on the public release (set `D` to their own copy or to the Ceph copy once its visibility allows) |
   | §1.2-1.8, §2, §3 (grid stages), §5, §6, §7, §8, the grid stages of §10 | Greg only (they read go2432's banks, `$RS/data/or_ready` or the pixel-restricted sources) |

---

## 1. The scaling plots (SchwingNet Figure 5 and the scaling analyses behind it)

**What "the scaling plots" are today.** The current accuracy-against-samples and coverage evidence is Figure 5 of the
SchwingNet manuscript (`sn:figures/figure5.*`, caption `figure5.caption.txt`, 58 words): (a) Wilson lower bound against
transitional test persons; (b) naming against training persons on three film corpora and on the C-arm per view; (c)
same-device detection against real frames; (d) render-only detectors at matched N along the lateral angle. Built by
`sn:tools/fig_power.py`, numbers in `sn:results/power/power.json` (2026-09-25 13:41). The older 2026-09-17 `~/scaling`
fraction sweep is superseded (leaky v2 bank) and `ssn:paper/rsnai/main_v2.tex` still has `\todo{[C8] scaling curve}`
(`working_notes/topic2_scaling_samples_anomaly_power.md` Part A, Part E row 1).

### 1.1 Rebuild Figure 5 from the result files already on disk (laptop or grid, minutes)

Inputs (each hashed into `power.json`): `sn:results/coverage/film_ncurve/film_ncurve.json` (sha256 5922dbdf...),
`sn:results/indomain/name_fill.json` (35b8ad7e...), `sn:results/indomain/det_fill.json` (af0357ae...),
`sn:results/coverage/pooled_fit.json` (a60c0a10...), `sn:results/coverage/experiment/runs/cov_surgio_b51_dr_*/unseen/recall_vs_angle.json`.

```bash
python SchwingNet/tools/fig_power.py                 # figures/figure5.{pdf,png,tif}, figure5.record.json, results/power/power.json
python SchwingNet/tools/results_macros.py --check    # exits 1 on a pending key, an unused key or a bare numeral
python SchwingNet/tools/check_limits.py              # words, abstract, figures, captions <= 60 words, references, banned word
sbatch -D ~/logs ~/spinesurg-ct-nnunet/SchwingNet/slurm/compile.sh     # grid only: there is no TeX on the laptop
```

Checks: `figure5.record.json` lists every drawn number with its `file#key`; the journal rules applied by `fig_power.py`
are four components a-d, Arial >= 12 pt at 7.0 in, TIF at 1,200 dpi LZW, Okabe-Ito palette (`fig_power.py`
docstring). Source: `sn:RESULTS_BUILD.md`; topic 2 A.20. Trap: `sn:figures/FIGURES.md` describes the retired 2026-09-22
four-figure set; ignore it.

### 1.2 Panel (b), C-arm: naming against training persons (`name_fill`)

Design: five case-grouped folds of `ssn:tools/carmlspine_to_bank.py` (test `md5(case) % 5 == K`, val `(K+1) % 5`);
N = 0, 5, 10, 25, 50, all training cases of one view protocol; recipe `ssn:slurm/carmlspine_cv_v9.sh` with init
`~/allspine_v9_fov96_ctx`; every cell scored on both protocols through `ssn:tools/level_prototype.py`, which runs
`ssn:tools/eval_gate.py` on every model chain (`ssn:tools/indomain_name_fill.py` docstring).

Commands, in the order of the script headers (`sn:slurm/name_fill*.sh`; resume vs reproduce: §0 item 6; outputs go to
the fixed `$RS/data/or_ready/indomain/name_fill`):

```bash
sbatch -D ~/spinesurg-ct-nnunet SchwingNet/slurm/name_fill_survey.sh                   # what the folds hold
P=$(sbatch --parsable -D ~/spinesurg-ct-nnunet SchwingNet/slurm/name_fill_prep.sh)     # CPU: fold banks, v9 base cache, manifest
n=$(wc -l < /rs/rs_grp_oschome/go2432/data/or_ready/indomain/name_fill/manifest.txt)    # after prep: cells = manifest lines
A=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --array=0-$((n-1))%16 --dependency=afterany:$P SchwingNet/slurm/name_fill.sh)
sbatch -D ~/spinesurg-ct-nnunet --array=0-4 SchwingNet/slurm/name_fill_cpu.sh          # optional: the zero-shot cells on CPU
sbatch -D ~/spinesurg-ct-nnunet SchwingNet/slurm/name_fill_apfilm.sh                   # optional: appends the AP film cells
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:$A SchwingNet/slurm/name_fill_collect.sh
```

`name_fill_retry.sh` (`--array=0-<n-1> --exclude=msa1 --export=ALL,MANIFEST=<retry manifest>`), `name_fill_revise.sh`
(`--export=ALL,DRY=1` first) and `name_fill_keytest.sh` (does a merged bank's crop key resolve for the gate) are the
repair jobs, each with its header's line. The collect step is the job, not a bare `python tools/indomain_name_fill.py
collect` (it reads `$RS` paths).  Recorded runs: arrays 40429416 and 40429901 (tasks 8 and 16 cancelled at
07:36, re-run by 40436049_0-9, COMPLETED 08:35 on 2026-09-24); 250 / 250 cells (`PENDING_JOBS.json#done_before_this_pass`).
Output `sn:results/indomain/name_fill.json`. Per-case rows `sn:results/indomain/fit/name_percase.json` (job 40436856,
`tools/indomain_fit_percase.py`).

Check: every cell's gate verdict is HELD OUT; 245 naming cells held out, overlap 0, unresolved 0 (`INDOMAIN.md` §1).

### 1.3 Panel (c): same-device detection against real frames (`det_fill`) and the plateau diagnosis

Design: N real C-ArmLSpine frames = both views of N/2 training patients, nested subsets, added to a fixed background;
one-view arms (25 or 50 frames of one protocol); out-of-domain arms at matched N (COBRA Elekta frames; styled renders of
this device on the same patients' poses); box-convention control (`power.json#panel_c_detection/design`).

Commands (headers of `sn:slurm/lcurve_fill*.sh`; tool `ssn:tools/lcurve_fill.py`; outputs under the fixed
`$RS/data/or_ready/indomain/detfill`, so move it aside to reproduce, §0 item 6): `sbatch -D ~/spinesurg-ct-nnunet
SchwingNet/slurm/lcurve_fill_plan.sh`; then, with `cells` = the lines of `SchwingNet/results/indomain/detfill/manifest.txt`,
`sbatch -D ~/spinesurg-ct-nnunet --array=0-$((cells-1)) SchwingNet/slurm/lcurve_fill.sh`; then `lcurve_fill_boxstyle.sh`,
`lcurve_fill_outline_prep.sh` and `lcurve_fill_collect.sh` with `-D ~/spinesurg-ct-nnunet` (collect `afterany` the array). Recorded: lcfill
40429442_0-5, collect lcfcoll 40436400, COMPLETED 08:07 on 2026-09-24. Output `sn:results/indomain/det_fill.json`;
per-frame hits `sn:results/indomain/detfill/grid/percase.json`.

The plateau diagnosis (re-score only, never retrain): `sn:slurm/carm_miss_diagnostic.sh` (job 40448862,
`ssn:tools/carm_miss_diagnostic.py` -> `sn:results/indomain/miss_diagnostic/`) and `sn:slurm/carm_denominator_repair.sh`
(job 40448892, `ssn:tools/carm_denominator_repair.py` -> `sn:results/indomain/denominator_repair.json`).

### 1.4 The fits (inverse power law) behind the "how many cases" statements

Method: acc(N) = A - B N^(-C), weighted nonlinear least squares with rank weights (Figueroa et al., BMC Med Inform
Decis Mak 2012;12:8), case-clustered percentile bootstrap of the whole fit, 2,000 resamples, seed 0; an asymptote counts
as identified when A is inside (0, 1) in the point fit and in at least 75 % of resamples (`sn:results/indomain/INDOMAIN.md` §1).

```bash
python tools/indomain_fit.py --boot 2000 && python tools/indomain_fit_docs.py
python tools/indomain_fit_N.py            # FIT_N.md: the interval-bearing extract to quote
```

Trap: `INDOMAIN.md` was generated at 10:43 with 10 resamples and says "no interval" everywhere; `fit.json` was rewritten
at 11:59 with `--boot 2000`; quote `FIT_N.md` (topic 2 Part E row 10).

### 1.5 Panel (d): matched-N coverage arms (render-only detectors at the same N, different poses)

Design: per device card (Surgio-B51, Elekta XVI), three render-only detectors at the same N: `low` (poses from the
device's real AP/LAT pool), `high` (arc pool), `low2n` (low plus N more real-pool frames); same 125 training subjects,
same card, trainer and seeds 0-1; scored on the unseen angle sweep (40 TotalSegmentator subjects, 19 lateral bins), the
real case134 spin and every real test split (`ssn:tools/coverage_arms.py` docstring; `sn:results/coverage/N_VS_COVERAGE_PLAN.md` part ii).

```bash
sbatch -D ~/spinesurg-ct-nnunet --array=0-3  SchwingNet/slurm/coverage_arms_render.sh
sbatch -D ~/spinesurg-ct-nnunet --array=0-11 --dependency=afterany:<render> SchwingNet/slurm/coverage_arms_train.sh   # one task per line of coverage_arms_manifest.txt
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<train> SchwingNet/slurm/coverage_arms_collect.sh
# re-score without training (one task per manifest line, then collect after the array):
S=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --array=0-11 SchwingNet/slurm/coverage_arms_score.sh)
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:$S SchwingNet/slurm/coverage_arms_collect.sh
```

Recorded: covrender 40437812 -> covarm 40437813 -> covcoll 40437814; covscore 40443105 and covcoll2 40443106. Runs
`~/spine-detector/runs/coverage/<arm>/`; collected `$RS/data/or_ready/coverage/experiment/`; local mirror
`sn:results/coverage/experiment/runs/`. The exact `sbatch` flags beyond script and array are not recorded
(`PENDING_JOBS.json`). Trap: the Surgio card renders thick laterals photon-starved, so +/-90 degree bins mix geometry
with underexposure (`power.json#panel_d_angle/exposure_caveat`).

### 1.6 The pooled nested fit (N alone vs N plus coverage) and the acquisition-space census

```bash
# acquisition-space census (grid, in a job), then the report
python tools/acq_coverage.py grid --out <dir>                    # sn:slurm/acq_coverage.sh
python tools/acq_coverage.py report --coverage coverage.json     # COVERAGE.md, fig_density*.png
# pooled fit (local, minutes)
python tools/indomain_fit_coverage.py --census SchwingNet/results/coverage/coverage.json \
  --experiment SchwingNet/results/coverage/experiment/scores.json \
  --film SchwingNet/results/coverage/film_ncurve/film_ncurve.json        # pooled_fit.json (+ fit/coverage_fit.json)
python tools/indomain_fit_coverage.py <same inputs> --arm-conf 0.74 \
  --pooled-out SchwingNet/results/coverage/sensitivity/pooled_fit_conf074.json
```

Sources: `ssn:tools/acq_coverage.py` L1202-1209; `sn:results/coverage/POOLED_FIT.md`; `pooled_fit.json#inputs`. The flag
that produced `sensitivity/pooled_fit_trained_only.json` is identifiable: only `--arm-min-val-map50 <value>`
fills `arms_excluded_untrained` (`ssn:tools/indomain_fit_coverage.py` L111, L506), and the file lists the six Elekta
arms; the threshold value used is not recorded. Check: the result reverses at confidence 0.74
(dAICc -3.1, p .82); quote it only as "at 0.25, not at 0.74" (`RESULTS_CATALOG.md` A11.5). Open: the `*_arc` and
`*_low2` render geometries are not yet in the census table.

### 1.7 The contribution matrix (which training source carries held-out detection)

`sbatch SchwingNet/slurm/contrib_matrix_cpu.sh` -> `sn:tools/contribution_matrix.py` (needs `tools/realxray_eval.py
--dump-raw` dumps of each arm). Rerun "whenever a new arm lands". Output `sn:results/contribution_matrix.{json,md}`;
self-check must report max |difference| 0.0000 over 85 cells. Figure: `sn:tools/fig5_contribution.py` /
`figS_supplement.py`. Trap: `sn:results/DATA_CONTRIBUTION.md` prose predates the rerun; the JSON is authoritative.

### 1.8 The superseded 2026-09-17 fraction sweep, if a clean film-fraction curve is ever wanted

Do not quote the old curve. `sn:results/indomain/INVENTORY.md` G8 suggests rebuilding it on a clean bank with the
command below. **Two traps make that command unsafe as written.** (1) `ssn:slurm/scaling_sweep.sh` writes to fixed
paths that do not depend on `BASE` (`~/scaling/<TAG>/`, `~/model_night/runs/model_scal_<TAG>.pt`,
`~/model_night/heads_mixed/head_scal_<TAG>_scal.pt`, `~/model_night/scaling/<TAG>/interior_windows.json`) and skips
every stage whose output exists (L38-53); `ssn:tools/subset_bank.py` returns at once on `READY` (L52). If the
2026-09-17 v2 outputs are still on HOME (`~/scaling` is listed there, 129 GB; whether the rest still exists is not
recorded), the run silently re-emits the leaky v2 curve. Move those four sets aside first, or copy the script with
output paths keyed on the `BASE` name, and check that the log's `SCALING_START ... base=` line names v9. (2) Even a
clean v9 run is a **selection-split** number: each subset encoder (`ssn:slurm/night_arm.sh` ->
`ssn:tools/train_level_backbone.py`) keeps its best epoch by accuracy on the subset bank's validation rows
(L516-520), and step 4 scores those same rows ("validation rows are identical in every subset bank"). A held-out
film-fraction curve needs the film N-curve design (§2.1: test persons outside the selection split), not this script.

```bash
sbatch -D ~/spinesurg-ct-nnunet --export=ALL,BASE=$HOME/allspine_v9_fov96_ctx slurm/scaling_sweep.sh   # GPU, 6 points, 40 h limit
python tools/make_feasibility_figures.py --results ~/model_night --out ~/model_night/figures_feasibility  # in a job
```

`ssn:tools/subset_bank.py` cuts a bank by film, seeded, stratified by source, copying validation rows unchanged; it has
`--drop-val-twins` for the NHANES defect. The proper replacement is the **ratio sweep proposed and never run**: one array,
`real_share` in {0.1, 0.25, 0.5, 0.75, 0.9} at N = 25 and N = all, three seeds, about 45 cells x 15 epochs, waiting on
Greg's yes/no (`sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` "What is not known"; `ssn:docs/RESUME_2026-09-22_PM.md`
L35-37). The bank-merge ratio it would vary is the command-line flag `--real-share` of `ssn:tools/merge_banks.py` (L31, default
0.5; L60 only uses it), so the sweep needs no code edit.

`ssn:tools/eval_scaling_curves.py` (devices / cases / fewshot, `ssn:slurm/eval_scaling_curves.sh`, output
`~/scaling_curves/`) is superseded by 1.2-1.3; read the foot of the slurm script before reviving it.

---

## 2. Accuracy against the number of samples: the film N-curve and the render ablation

### 2.1 The film N-curve (Figure 5b, film)

**Why a new encoder.** The v9 encoder has seen every film person of its training split, so a film curve on it would
not measure N; the curve uses a render-only encoder (the v9 bank minus every film row) and scores on the v9 VAL persons
of each corpus, which no cell and not this encoder ever trained or selected on (`ssn:tools/film_ncurve.py` docstring).

Inputs: `~/allspine_v9_fov96_ctx` (bank and split), `~/films_drr` (films), the render roots; person keys by
`tools/patient_keys.key_any` (one CSXA film = one person; one four-digit BUU case = one person; NHANES by film number).
Cells: N = 0, 5, 10, 25, 50, 100, 200, all per corpus (NHANES II, BUU-LSPINE, CSXA); seeds 0-2 at N <= 25, seed 0 above;
SELECTION = a fixed draw of min(100, ceil(0.15 x pool)) training persons; POOL = the rest, nested per seed.

The chain writes to the fixed `$RS/data/or_ready/film_ncurve` that holds the published run: re-submitting it resumes
(every recorded cell has a DONE marker and comes back unchanged); to reproduce, move that directory aside first or copy
the scripts with a new `FN` (§0 item 6).

```bash
cd ~/spinesurg-ct-nnunet
P=$(sbatch --parsable -D ~/spinesurg-ct-nnunet SchwingNet/slurm/film_ncurve_prep.sh)                       # CPU, 150 GB
E=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --dependency=afterany:$P SchwingNet/slurm/film_ncurve_encoder.sh)
C=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --array=0-47%16 --dependency=afterany:$E SchwingNet/slurm/film_ncurve.sh)
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:$C SchwingNet/slurm/film_ncurve_collect.sh
# then copy $RS/data/or_ready/film_ncurve/{film_ncurve.json,FILM_NCURVE.md,cells.json} to SchwingNet/results/coverage/film_ncurve/
```

Recorded run: fnprep 40437808 -> fnenc 40437809 -> fncell 40437810 -> fncoll 40437811 (`PENDING_JOBS.json#chains/film_ncurve`);
48 / 48 cells, `FILM_NCURVE.md` generated 2026-09-24 23:25. Grid outputs `$RS/data/or_ready/film_ncurve/` (`cells.json`,
`manifest.txt`, `render_bank/`, `test_ctx/`, `pool_*/`, `base_cache/`, `cells/<cell>/`). Runtime about 18 GPU-minutes per
cell (`sn:REVISION_LOG3.md` §13). Per cell: fine-tune 15 epochs, lr 1e-4, `--augment 2`, merged 1:1 with the render
bank's per-class-600 sample; then `head_mixed_length --train-mode mixed`; scoring `tools/rigor_fixes.py a5-rows` on one
test context, which runs `tools/eval_gate.py` first.

Checks: every `film_ncurve.json#cells/<cell>/heldout` reads "HELD OUT"; the render-only encoder's own val exact accuracy
is 0.664 (`#encoder`); NHANES all = 92.7 %, BUU all = 96.9 %, CSXA all = 99.8 % (`RESULTS_CATALOG.md` A10), read from
`film_ncurve.json#cells/<corpus>_Nall_s0/per_source_exact/random/<corpus>` (the `random` key; the `maximal_band*`
keys give other values, for example NHANES band3 92.9, band9 93.2).

### 2.2 The render ablation (Table S4, Discussion)

Arms: `renderonly` = the curve above; `imagenet` = ImageNet init on the same merged bank; `filmonly` = ImageNet init with
every render row removed (N = 0 skipped). Reading rule, stated before the numbers: at N = 5 and 25 per corpus, renders
help if render-only exceeds film-only outside the patient-clustered intervals on every seed; the largest N is the third
verdict cell; nine cells in all (`sn:REVISION_LOG3.md` §13).

Same caution as §2.1: the arms write under `$RS/data/or_ready/film_ncurve/ablation/<arm>/` and skip DONE cells.

```bash
sbatch -D ~/spinesurg-ct-nnunet --array=0-47%12 --export=ALL,ARM=imagenet SchwingNet/slurm/film_ncurve_ablation.sh
sbatch -D ~/spinesurg-ct-nnunet --array=0-47%12 --export=ALL,ARM=filmonly SchwingNet/slurm/film_ncurve_ablation.sh
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<array> --export=ALL,ARM=imagenet SchwingNet/slurm/film_ncurve_ablation_collect.sh
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<array> --export=ALL,ARM=filmonly SchwingNet/slurm/film_ncurve_ablation_collect.sh
# copy $RS/data/or_ready/film_ncurve/ablation/<arm>/{film_ncurve.json,FILM_NCURVE.md} to SchwingNet/results/coverage/film_ncurve/ablation/<arm>/
python SchwingNet/tools/film_ncurve_ablation_read.py          # READ.md + ablation_read.json
python SchwingNet/tools/make_supp_ablation_table.py           # tables/tabS4_ablation.tex
```

Recorded: imagenet 40451157 (48 / 48), filmonly 40451158 (39 / 48), collects 40451159 / 40451160; about 15 GPU-hours
per arm. Check: `READ.md` shows six "help" and one "hurt" (BUU, every person); the Discussion keys
`abl_gap_min_pts` 6, `abl_gap_max_pts` 22, `abl_cells_separated` 7, `abl_cells_total` 9, `abl_worst_delta_abs_pts` 1.6.
Traps: `tabS4_ablation.tex` has no `.md` twin and no `.sources.md` (every other table has both); the memory note
`context/film-ncurve-ablation-result.md` says "all help" and "not in the tex": both outdated.

### 2.3 Not yet run, waiting on Greg

Seeds 1-2 at N = 50 to all (18 cells x 2 arms): the BUU-all reversal rests on one seed. The ratio sweep (§1.8). A per-level
film table on held-out persons (needs a committed aggregation tool; today only the derived selection-split Table E of
`PER_LEVEL_DOMAIN_ANGLE.md` exists). Source: `PER_LEVEL_DOMAIN_ANGLE.md` "What is not known"; RESUME 2026-09-27 18:05
"FOR GREG".

### 2.4 The older sample curves (for completeness)

- Real-frame detection learning curve `lcurve` (2026-09-23): `sbatch -D ~/spinesurg-ct-nnunet SchwingNet/slurm/lcurve_prep.sh`;
  the array `SchwingNet/slurm/lcurve.sh` over `lcurve_manifest.txt`; `SchwingNet/slurm/lcurve_report.sh` (afterany);
  copy `lcurve.{json,md}` and `fig_lcurve.png` back. Recorded prep 40416377, array 40416378_0-18, report 40416379. Trap:
  an earlier prep (40416368) failed because an unquoted remote `sed -i s/\r$//` deleted a trailing "r" from lines
  (`sn:results/lcurve/JOBS.txt`).
- LSTV flag learning curve: `ssn:tools/lstv_flag_learning_curve.py` (one fixed held-out split; positives subsampled 10,
  20, 40, 80, all; five draws; AUC within each cohort, never pooled), plot `ssn:tools/lstv_flag_curve_plot.py` ->
  `~/lstv_flag/LEARNING_CURVE.md` (grid; date and job not recorded).
- The D1 head data saturation (paper 2): `sn:tools/d1_saturation.py` over `tools/head_dual.py` outputs (d1lcurve 40436887,
  d1cover 40436997) -> `sn:results/dual_loss/saturation.json`.

---

## 3. The anomaly scan: harvest, two labellers, registry, ruleclass and the review tree

**The definitions every number depends on** (`working_notes/topic2_scaling_samples_anomaly_power.md` B.1):
- A call needs a count; a count needs both junction references in the field (L6 / four-lumbar / sacralised L5 need the
  lowest rib-bearing vertebra and the sacrum; T13 needs the rib cage counted from T1). A CT that cannot count is
  `no_count`, never ordinary.
- Truth tiers, in registry order: read > two-labeller > single-labeller > morphology-only > none. Only `read` is truth
  (CTSP two-reader Castellvi consensus and read levels, 33 records; the published VerSe table, 325 subjects; three
  CTSpine1K list entries; plus 70 externally labelled TotalSegmentator CTs for L6 / T13).
- **The two labellers**: labeller A = SPINEPS + VERIDAH names bound to instances through the ctd centroid file (never by
  mask id); labeller B = TotalSegmentator geometry (rib-head contact, a 38 mm stump rule); reader C = a direct CT rib
  count (`ssn:docs/ruleclass/CLASSIFIERS.md` R9-R11). They fail differently, which is why agreement is a tier.
- Real-frame persons (COBRA, C-ArmLSpine, DeepFluoro, Geneva, SpineSAC, Ljubljana) are TEST only and never rendered
  for training.
- Label maps: VerSe raw masks L6 = 25, T13 = 28; CTSP v11 L6 = 25, sacrum 26, 29 retired; resolve CTSP / Dataset803
  outputs with `ostk.labels.labels_for`.

### 3.1 The chain, in dependency order

| step | command | output | recorded run | source |
|---|---|---|---|---|
| 1 anomaly manifest | `python tools/anomaly_manifest.py --out ~/model_night/anomaly_manifest --bank ~/allspine_v9_fov96_ctx/rung_1.npz` (in a job; the default `--bank` is `~/allspine_v5_fov96_ctx/rung_1.npz`, deleted 2026-09-20, and without it the run prints "no crop bank" and leaves the quality columns empty, unlike the 2026-09-17 manifest; `ssn:tools/anomaly_manifest.py` L553) | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (grid) | 2026-09-17 | `ssn:tools/anomaly_manifest.py` docstring; consumers read `spine_classes.json` via `--classes`; check the log line "per-case classes from:" |
| 2 inventory | `sbatch -D ~/spinesurg-ct-nnunet SchwingNet/slurm/anomalous_inventory.sh` (its `#SBATCH --output=anominv-%j.out` is relative, so `-D` decides where the log lands) -> `ssn:tools/anomalous_inventory.py` | `sn:results/anomalous_inventory.{json,md}` | job 40416205 | topic 2 B.2.2 |
| 3 subtypes | `python tools/transitional_subtypes.py --repo . --ctsp <CTSpinoPelvic1K-1> --aux <dir with manifest.csv, meta.json, patient_keys.json, patient_keys_v9.json> --out SchwingNet/results/rare_class --ts-override SchwingNet/results/rare_class/ts12_subtype_override.json` (`--ctsp`, `--aux` and `--out` are required and `--ts-override` takes a path: docstring L44-45, argparse L80-86) | `sn:results/rare_class/transitional_subtypes.{csv,json,md}` | 2026-09-23 18:54 | same |
| 4 person split (G3) | **frozen; do not rerun in place.** Recorded: `sbatch -D $HOME/spinesurg-ct-nnunet --export=ALL,STAGE=all SchwingNet/slurm/g3_split.sh` (`tools/make_split.py plan/apply`); a rerun re-globs every ann root on the grid today and rewrites `~/split_final.json` with no backup (§10) | `~/split_final.json`, `split_leak_report.json`, `sn:results/rare_class/split_plan.md` | apply 2026-09-23 20:18:48, seed 0, job 40426793 | `split_plan.md` header |
| 5 harvest streams | verse: `ssn:slurm/harvest_verse_{census,ts,ts_cpu,render}.sh` (tools `harvest_verse_census.py`, `harvest_verse_registry.py`, `harvest_verse_render.py`); ctsp: `ssn:slurm/ctsp_registry_census.sh` (`ctsp_registry_census.py`, `ctsp_registry_ts.py`, `ctsp_registry_build.py`); totalsegmentator: `ts_transitional_screen.py`, `ts_transitional_registry.py`, `transitional_ts_count.py`; cobra: `ssn:slurm/harvest_cobra_{cases,ts}.sh`, `harvest_validate_{a,b}_ctsp.sh` (`harvest_cobra.py`, `harvest_cobra_validation.py`, `harvest_validate_a_ctsp.py`, `harvest_validate_b_score.py`, `cobra_lstv_screen.py`); other_ct: `sbatch ... slurm/other_ct_fetch.sh <ctspine1k|ribfrac|rsna>` (`tools/other_ct_fetch.py`) | `sn:results/transitional_registry/<stream>/rows.csv`, `SUMMARY.md` (one row per CT in a shared schema) | workflow wf_babed05b-84a, 2026-09-23/24 | topic 2 B.2.4 |
| 6 registry | `python tools/transitional_registry.py` (reads every `<stream>/rows.csv`); test `ssn:tools/test_ts_transitional_registry.py` | `registry.csv`, `registry.json`, `REGISTRY.md`, review queues, `contact_sheets/` | 2026-09-24 11:07 | topic 2 B.2.5 |
| 7 renders (MAXIMIZE) | `python tools/rare_class_maximize.py`, then `sn:slurm/rare_max_stage.sh`, `rare_max_verse.sh`, `rare_max_verify.sh` | `maximize/MAXIMIZE.md`, `jobs.json` | 2026-09-24 16:55 | topic 2 B.2.6 |
| 8 acquisition screens | `bash slurm/acquisition_submit.sh <target>` (targets env, validation, tier1, tier1_late, tier2, dedupe); per collection fetch -> convert -> cases -> ts -> gate -> spineps -> call -> summary, `afterany`, resumable; ranking `python tools/acquisition_census.py --calibration <file> --aa3-meta <file> --nbia-fdg <file> --out <dir>` (all four required, L444-447; `--calibration` comes from `ssn:tools/acquisition_calibrate_fov.py`; the inputs used on 2026-09-23 are not recorded) | each collection's `rows.csv` under `$RS/data/anomaly_harvest/<collection>/` | 2026-09-23 to 09-25 | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` (a frozen copy also sits at `sn:results/fig6/frozen/v1/transitional_registry/acquisition/ACQUISITION_PLAN.md`); `ssn:data_platform/DATA_MANIFEST.md` L3654-3660 |
| 9 census table | `python tools/census_table_2026-09-25.py` | `ssn:docs/CENSUS_TABLE_2026-09-25.md` | 2026-09-25 | its counts are one high in every collection but PANORAMA; fix before reuse |
| 10 ruleclass arms | arm scripts on the grid only, under `$RS/ruleclass/code/`: `ts_arm_gpu.sh`, `ts_arm_collect.sh`, `armb/armb_tier.sh`, `armb_measure.sh`, `armb_remeasure.sh`, `armb_collect.sh`, `pelvis/pelvis_*.sh`; tier lists `probe_t2.sh`, `probe_t3.sh` -> `tiers/build_tiers.py` -> `check_paths.sh` (0 missing) | `$RS/ruleclass/arms/{ts,moller_fast,moller,pelvis}/<collection>/`, `tiers/` | jobs in `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; acceleration arrays 40485812-15, collects 40485887-89 | local copies are not in the repository; outcome after 2026-09-27 not recorded |
| 11 rules, tree, report (only after the PREREG freeze) | with `RC=/rs/rs_grp_oschome/go2432/ruleclass` (`ssn:tools/transitional_review/anomaly_rules_array.sh` L16): `sbatch -D $RC/rules --array=0-63 --export=ALL,LIST=$RC/tiers/tier1.tsv .../tools/transitional_review/anomaly_rules_array.sh`, then `python tools/transitional_review/anomaly_rules.py collect --out $RC/rules/tier1`; `build_review_tree.py --census <census.tsv>`; `rule_report.py --census ... --castellvi ... --lumbosac ... --verse-suppl ... --lstv-flags ... --registry ... --prereg docs/ruleclass/PREREG_rules.md` | per-CT JSON + TSV rows; `$RS/review_tree/<date>/<TYPE>/` case folders, `manifest.tsv`, `index.html`; `report.html` | **not recorded as run**; code untracked in git | `ssn:tools/transitional_review/` headers; topic 2 B.2.11 |

### 3.2 The ruleclass arms (the "SUPER DETECTOR RUN")

Greg's determination (2026-09-26 23:50): two arms. Arm A = TotalSegmentator 2.18.0 `total` at full resolution ->
`arms/ts/<collection>/`. Arm B = SPINEPS + VERIDAH (existing masks) + the Moller rib nnU-Net (Zenodo 14864106, folds
0-2, through SPINEPS' wrapper; `arms/moller_fast/` for the corpus pass, `arms/moller/` full configuration, 20-25x
slower) + Greg's Dataset803 ensemble for the **pelvis only** (sacrum + hips) as the caudal anchor -> `arms/pelvis/`
(Greg: "My model is essentially shit at everything except the pelvis"; `ssn:docs/RESUME_2026-09-22_PM.md` L167, L197).
Environment `~/mambaforge/envs/spineps` (spineps 2.1.1, TPTBox 0.8.2, torch 2.6.0+cu124); the Blackwell nodes ymh3 / ymh4
cannot run it. A pre-registered decision gate (`arms/pelvis/_timing/DECISION.json`) sits between a timing run and the
production array; cancel the old pelvis timing job only after that file exists (`ssn:docs/RESUME_2026-09-22_PM.md`
L63-68; `ctsp:Student_Projects/RECIPE.md` rule 14). Estimated new output about 40 GB (`ssn:docs/ruleclass/TIERS.md`).

Dataset803 has no `results/` tree on the grid; fetch it from Hugging Face
`OpenSpineConsortium/spinopelvic-seg-checkpoints` (`CLASSIFIERS.md` R36).

### 3.3 The pre-registration and the review

`ssn:docs/ruleclass/PREREG_rules.md` (DRAFT v1, f15da62): rule 1 rib-free lumbar count (free presacral bodies between the
lowest rib-bearing vertebra, a Moller rib > 38.0 mm on at least one side, and the cranial end of the Dataset803 sacrum;
`no_anchor` when the sacrum is absent, < 5 mL, at the caudal edge, or the two anchors differ by > 20 mm); rule 1b shape
of the sixth rib-free body (not yet built on SPINEPS masks); rule 2 pelvis and sacral morphology (gates nothing until a
reference half is frozen); rule 3 stump rib (lowest rib <= 38.0 mm and not cut by the border); rule 4 the MDPA (the CTSP
files' spelling of the Medical Physics dataset article, MPDA in this handoff) thoracolumbar shape score (T12 vs L1 AUC 0.990; its canal features must not come from ostk at or after 1b7005c). The
sweet spot is pre-stated: highest specificity subject to sensitivity >= 0.95 on read-tier positives, pooled and per
subtype. Review: stage 1 screen by Ashley Schehr (HF username withheld), blinded to the registry's call; stage 2 confirm by the
senior reviewer "Dr Tech" (full name recorded nowhere on disk), blinded to stage 1; reviewer instructions
`ssn:docs/REVIEW_TRANSITIONAL.md` (untracked). Freeze (§9): signer, date and sha256; after the freeze every output row
carries `prereg_sha256`; a later change is a new dated version, never an edit.

Before the freeze, resolve: the 33-CT difference between `CORPUS.md` (21,655; a grid-only file under `$RS/ruleclass`,
exact path not recorded, in no local repository) and the tiers (21,622); PANORAMA's 1,495
masks not yet in the tiers.

Next steps as written on 2026-09-27 18:05 (`ssn:docs/RESUME_2026-09-22_PM.md` L28-33): read the build workflow's journal
(wf_ded52e0e-cd1); run each self-test (`anomaly_rules.py --selftest` and the others); commit
`tools/transitional_review/`; then on the grid the rules array, the tree build, `rule_report`, the review app; deliver
`REVIEW_TRANSITIONAL.md`. "Nothing is scored as a result before PREREG_rules.md is frozen."

### 3.4 Checks that prove a stage worked (outside the computation)

- Labellers against external truth: `sn:results/transitional_registry/acquisition/validation/VALIDATION.md` (70 TS CTs);
  `cobra/labeller_validation_ctsp.md` (against CTSP readers).
- Prevalence windows: L6 2-5 %, 13 rib-bearing 0.37-0.88 %, lumbar rib 1.6 %, stump twelfth rib 12.6 %
  (`PREREG_rules.md`); priors in `ssn:tools/acquisition_census.py` L17-26 (p_LSTV 0.09-0.18; p_count 0.048; p_T13
  0.0064-0.020). A screen five to fifteen times its prior is wrong until shown otherwise: the NLST pilot's 9.3 % T13
  fell to 1.5 % once a rib on the named body was required (`sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` §11; jobs 40436876/77).

### 3.5 Traps (from the memory notes)

- Never read `has_T13` from the VerSeFusion manifest (18 claimed, 6 true) (`context/versefusion-t13-flag-wrong.md`).
- SPINEPS masks harvested before commit 147428d carry raw ids 1..N; never name by mask id; read them through
  `tools/spineps_ids.relabel_by_ctd`; in `tsv3_ctd` 431 and in `ctd_relabel/bench_ts_native` 31 "relabelled" masks are
  symlinks back to the raw mask (`TIERS.md` §3-4; `context/spineps-ids-can-be-scrambled.md`).
- TotalSegmentator `sacrum` and `vertebrae_S1` are disjoint; the whole sacrum is their union; TS rib masks often lack the
  rib head (`context/ts-sacrum-excludes-s1.md`).
- Dataset803 was trained on CTSpine1K + CTPelvic1K + COLONOG, and 440 of the 802 CTSP pelvis labels are its own
  out-of-fold pseudolabels, so on CTSP its agreement with "GT" is model against model (`PREREG_rules.md` §2).
- Children: an unfused S1 reads as a free body (`TIERS.md` §1).
- LCC post-processing deletes the loose lamina of a spondylolytic vertebra; a model counting from the rib anchor fails
  preferentially on LSTV cases because the anchor itself moves (`context/spondylolysis-and-border-anomaly-findings.md`).
- L6 Dice 0.000 under duplication is a distinct-case count signal, not a trainer bug
  (`context/l6-sample-count-and-counting-decoder.md`).
- `~/vf_813` maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work
  (`context/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md`).
- Append CTSP re-read discrepancies to `ctsp:docs/lstv_reread_queue.csv`, never a new file (`context/lstv-reread-queue.md`).

---

## 4. The power calculations

| calculation | how to regenerate | output | source |
|---|---|---|---|
| Figure 5a (Wilson lower bound vs persons; n needed at 0 / 1 / 2 / 5 errors) | `python SchwingNet/tools/fig_power.py` | `sn:results/power/power.json#panel_a`, `#n_needed_zero_errors` | `fig_power.py` |
| independent check, pure arithmetic | `python HANDOFF/working_notes/t2_wilson_check.py` (no repository import) | prints 35 / 22, 53 / 34, 69 / 45, 113 / 74; 64.57 % at 7, 90.59 at 37, 93.00 at 51, 95.86 at 89; 88.65 / 92.13 / 93.98 / 96.30 at 30 / 45 / 60 / 100 | verified 2026-10-08: all match `power.json`, `power_table.json`, `LEVELCHECK_CLAIM.md` §4 and `sn:sections/results.tex` L91-98 |
| Wilson table by errors and n | `sn:tools/fig_claim.py` | `sn:results/power_table.json` | topic 2 C.1 |
| statistical re-computations (power at planning accuracies; paper-2 power) | `python SchwingNet/tools/stats_review_recompute.py`; `python SchwingNet/tools/stats_review2_recompute.py` (2,000 resamples, seed 0) | `sn:results/stats_review/recompute.json` (R4_wilson), `stats_review2/recompute.json` (S1-S4, S9, S12) | topic 1 §9 |
| paper-2 n_min and power tables | the exact-binomial code in `sn:LEVELCHECK_MODEL.md` §11 (frozen; do not edit) | §5, §7, §13 of the same file | topic 2 C.1 row 4 |
| two-proportion power, n per arm, minimum detectable difference | `python tools/stats_compare.py power-diff --n1 <n> --p1 <p> [--n2 ...] [--p2 ...] [--deff ...]`, `stats_compare.py plan --arm <arm> ...`, `power-criterion`, `certify` (test `tools/test_stats_compare.py`). The top-level `python tools/stats_compare.py --help` crashes (`TypeError: %c requires int or char`: the `certify` help at L1220 has an unescaped "99 % claim"); the subcommand help works | none saved | `literature_state/power.md` row 9 |
| expected transitional people per collection and the stopping rule | `python tools/acquisition_census.py --calibration ... --aa3-meta ... --nbia-fdg ... --out ...` (§3.1 row 8; inputs used not recorded); `tools/census_table_2026-09-25.py` | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` §2-3; `CENSUS_TABLE_2026-09-25.md` | [E] |
| the full inventory of every power row in the programme | `python HANDOFF/literature_state/power_calc.py` (needs scipy; since 2026-10-08 it writes next to itself) | `literature_state/power_calc.json`, read in `power.md` | `literature_state/power.md` §1 (18 sources) |

The method to copy for any new pre-registered analysis (`working_notes/topic2_scaling_samples_anomaly_power.md` C.4):
write the rule and its success criterion, hash the document, stamp every output row with `prereg_sha256`, and treat any
number produced before the freeze as calibration. Four working examples: `PREREG_rules.md` §9 (the transitional rules),
`sn:LEVELCHECK_MODEL.md` §9 (freeze by git ancestry, UTC time and `git rev-parse HEAD` recorded at unblinding),
`sn:generated/numbers_audit.md` (per-key value and source SHA-256), and the U251 project's `PREREG.md` / `TARGETS.md`
hashes (another project).

---

## 5. The DRR banks (renders) and the crop banks that train the level encoder

**Rule first:** a render inherits its CT's person; every crop bank is built with one split over people across all roots
(`--patient-json`), and refuses unkeyed cases (`ssn:docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` "The fix"). Runnable forms
of the rebuilds whose id is a source in `ssn:data_platform/sources.json` (`ctsp_drr`, `verse_drr`, `physics_drr`,
`physics_rare`, `ts_drr`, `ts_drr_v3`, `devcorpus`; not `films_drr`, `nhanes_drr`, the `allspine_v9` bank or the
`carm_cvmix` fold banks) are printed by `python data_platform/reacquire/reacquire.py --grid <id>` (dry run by default;
`--run` only inside a job) (`ssn:data_platform/DATA_MANIFEST.md` cards). **Every row below is a record of how the
artefact was built, not an instruction to rebuild it in place** (several scripts delete their output first).

| render or bank | build | holds | used by | source |
|---|---|---|---|---|
| `~/films_drr` | `tools/manifest_to_drr_format.py` over the spine-detector manifest (renders stage of `ssn:slurm/reproduce_all.sh`) | 9,109 real films: CSXA 4,963 + BUU lateral 3,603 + NHANES 543 (36 GB) | every level bank | `DATA_MANIFEST.md` Appendix A1 |
| `~/nhanes_drr` | `tools/nhanes_to_drr_format.py` (`ssn:slurm/nhanes_build.sh`) | the same 543 NHANES films again | allspine v1/v2/v6/v7 and the fold banks: **the double inclusion**; v8/v9 drop it | A1; `ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` |
| `~/ctsp_drr` | `ssn:slurm/ctx_build_ctsp.sh`: `tools/make_drr_dataset.py --src nnunet/raw/Dataset813_SpineSurgLSTVFullRibs --dst ~/ctsp_drr --scheme ds813 --ct-root ~/data/CTSpinoPelvic1K/ct --prefix CTSP_ --resume` (CTs found by basename) | 801 CTSP lateral parallel-beam DRRs (0533 in no trained bank) | v9 | `DATA_MANIFEST.md` card `ctsp_drr`. A re-acquisition expects 802 anns (0533 repaired later; the card's `verify` step), so a rebuild is not the v9 input |
| `~/verse_drr` | `tools/make_drr_dataset.py --scheme verse` over `~/VerSeFusion/data/unified` | 387 (13 exact duplicates) | v9 | card `verse_drr`; `ANOMALY_RULE_EVALUATION.md` |
| `~/physics_drr` | `STAGE=physics PSCHEME=ctsp\|verse\|totalseg\|implant PSRC=<dir> sbatch --array=... ssn:slurm/fluorocap_v2.sh` -> `tools/render_physics_drr.py --per-case 2 --det-px 640` (perspective, polychromatic, scatter, noise) | 7,045 anns: ctsp 2,430, totalseg 1,831 (1,121 subjects), verse 1,463, implant 1,321 | v9 (the only route by which TotalSegmentator reaches the level bank) | card `physics_drr`; `data_platform/sources.json` |
| `~/physics_rare` | `ssn:tools/find_rare_cases.py` writes `~/FluoroCap/rare_cases_ctsp.txt` (34) and `rare_cases_verse.txt` (56), then `STAGE=physics ... PCASES=<file>` with the same script | 1,482 anns (34 CTSP ids 603 + 47 VerSe series 879) | v9 | card `physics_rare` |
| `~/ts_drr`, `~/ts_drr_v3` | `tools/ts_to_drr.py` (`ssn:slurm/ts_drr.sh`) | 1,170 / 1,735 renders | sweep bench only; **not in v9** (`ts_drr_v3` is read by nothing) despite Table 1 | `DATASET_USAGE.md` |
| `$RS/data/devcorpus` | `tools/devcorpus_build.py` (lists `--design A\|B\|P`) | 142 clean TotalSegmentator v3 whole spines ray-cast under each device's real poses and styled by its nine fitted terms; 17 validation subjects shared by all five styled corpora | the device-held-out detectors and the coverage arms | `ssn:docs/DATASHEET.md` §2.7; `DATA_MANIFEST.md` card `devcorpus` |
| `allspine_v9_fov96_ctx` (the level bank) | **record of how it was built; do not rerun in place.** `ssn:slurm/allspine_v9_bank.sh` L21 runs `rm -rf "$CTX"` on `~/allspine_v9_fov96_ctx`, which also holds `runs/model_rung_1_aug2.pt`, the v9 encoder that `sn:slurm/name_fill.sh` (L26) and `slurm/carmlspine_cv_v9init.sh` (L43) read as INIT, and `rung_1.npz` + `meta.json`, the bank that `name_fill.sh` (`merge_banks --base`) and the film N-curve (`ssn:tools/film_ncurve.py` L59-102) read; `allspine_v9_keys.sh` overwrites `~/patient_keys_v9.json` from whatever render roots exist today with the current `tools/patient_keys.py` (which has uncommitted local edits); neither script takes another output path. To reproduce, copy both scripts with `CTX=~/allspine_v9r_fov96_ctx` and `KEYS=~/patient_keys_v9r.json`, then compare `meta.json`, the per-source train / val counts (CSXA 4,214 / 749, BUU 3,070 / 533, NHANES 464 / 79) and the person-key counts with the shipped bank. The encoder can be restored from `~/model_registry` if its registration exists (`ssn:tools/train_level_classifier.py` registers alias `<bank>_rung_<tag>`, `ssn:docs/MODEL_REGISTRY.md`; whether the v9 encoder is registered is not recorded locally); the bank cannot. Recorded chain: keys `ssn:slurm/allspine_v9_keys.sh` (job 40415667) -> bank `ssn:slurm/allspine_v9_bank.sh` (40415668): `tools/make_context_crops.py --drr ~/films_drr --drr ~/ctsp_drr --drr ~/verse_drr --drr ~/physics_drr --drr ~/physics_rare --mode fov --size 320 --tgt-px 96 --val-frac 0.15 --patient-json ~/patient_keys_v9.json --group-strip-suffix --skip-clipped 1 --rungs 1` -> train `ssn:slurm/allspine_v9_train.sh` (40415669; `tools/train_level_classifier.py --rung 1 --epochs 40 --augment 2`, then `tools/head_mixed_length.py --train-mode mixed --kmax 4` at three seeds; GPU gvohp/galhp, 180 GB, 14 h) -> a5 score (40415670) | 18,565 case ids; films CSXA 4,214 / 749, BUU 3,070 / 533, NHANES 464 / 79; 9,592 train / 1,776 val person keys | the SchwingNet encoder and head | `ssn:slurm/allspine_v9_*.sh`; `DATASET_USAGE.md` §3.1 |
| C-ArmLSpine fold banks `carm_cvmix{0..4}` | `tools/merge_banks.py --base ~/allspine_v7_fov96_ctx/rung_1.npz --real ~/carm_cv{k}_fov96_ctx/rung_1.npz --out ~/carm_cvmix{k}_fov96_ctx --per-class 600 --real-share 0.5 --base-cache ~/carm_base_cache` (`ssn:slurm/carmlspine_cv.sh` line 28; `--out` is required) | fold 0: buu 635, csxa 1,758, nhanes 303, nhanes_drr 277, ctsp_drr 638, verse_drr 940, physics_drr 5,285, physics_rare 1,132, FluoroCap 2,100, VinDr 2,632, C-ArmLSpine AP 7,869 + LAT 7,827 | the fine-tuned naming numbers (v9init folds) | `ssn:docs/MODEL_CARD.md` §3.2 |

Checks: `meta.json` of every bank names its key file and roots; `tools/leak_check.py check` (`LEAKAGE.md`); the bank
builder fails if anyone is on both sides. Traps:
- The A-P voxel size was once written as the S-I row spacing, so every sweep before `sweep_v3` rendered the wrong field
  size (`context/drr-row-spacing-defect.md`).
- Physics-perturbed sweeps once rendered with no bone; use `make_drr_dataset --paths2-only`
  (`context/sweep-physics-no-bone.md`; `ssn:docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`).
- CT volumes are stored (P, I, R): decide directions from the affine (`context/ct-volumes-are-pir-not-ras.md`).
- `ctsp_drr` names a case `CTSP_COLONOG_<token>` while physics renders use `ctsp_<release id>`; key both through
  `tools/patient_keys.py`, never by name (357 people sat on both sides of the v6/v7 split)
  (`ssn:docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`).
- `Dataset813` image links are container paths; never repair them on the host; preprocess with
  `HF_EXPORT_DIR=$HOME/data/CTSpinoPelvic1K` (`context/dataset813-image-links-are-container-paths.md`).
- The exposure clip `device_style.SPREAD = 0.2` pins a term on 94.9-98.3 % of styled frames (§6).

---

## 6. The device calibration (image-formation cards)

| step | command | output | source |
|---|---|---|---|
| fit a card | `sbatch --export=ALL,CMD=fit,DEVICE=<cios_fusion\|bv_pulsera\|elekta_xvi\|pixium_4600\|surgio_b51_dr>,EXTRA="--variants" slurm/device_fit.sh` (`CMD=pairs\|fit\|display\|cobra-thickness`; reqp/requeue, 16 CPU, 96 GB, 12 h; env `fluorogen`) | `$RS/data/or_ready/devices/<device>/` (marker `FIT_DONE`) and `docs/devices/<device>.json` **in the grid repo copy** (copy it back). A refit overwrites the shipped card there: copy `docs/devices/<device>.json` aside first | `ssn:slurm/device_fit.sh` header |
| the supplement table | `python SchwingNet/tools/make_supp_device_table.py` | `sn:tables/tabS1_device_terms.tex` | topic 1 §3.2 |
| held-out gain on patient-held-out folds | recorded in `sn:results/eval_gate/leaks/card_gain_unseen.json` | +0.019 [0.008, 0.033] | `RESULTS_CATALOG.md` A12.2 |
| the exposure-spread sweep and the typicality gate | `ssn:slurm/device_spread_arm.sh` (A/B on real frames not yet run) | `ssn:docs/DEVICE_SPREAD_SWEEP.md` | `ssn:docs/DEVICE_PARAM_AUDIT.md` |

What a card is: nine terms fitted leave-one-group-out on up to 40 frames (PIXIUM 14 of 18) of a device's real exposures,
against exact geometry and attenuation; "calibrate, don't learn" (the learned refiner won on 21 % of frames only)
(`context/learned-formation-refuted-calibrate-instead.md`; `context/k-devices-one-network.md`). Devices and their frame
sources: Cios Fusion (DeepFluoro), Elekta XVI (COBRA, 40 frames of 3 cases), BV Pulsera (Geneva phantom), PIXIUM 4600
(Ljubljana), Surgio-B51 (C-ArmLSpine; its card exists only on the grid) (`DATASET_USAGE.md` §2).

Checks: held-out R^2 of the card above uncalibrated physics on every device (`docs/devices/*.json#physics_terms`); a
refit must pass its own acceptance gate (`sn:figures/figS2.record.json` panel d). Traps: DeepFluoro frames were once
converted as a log of a log (fix `DF_CONVERSION=linear`; whether the cards were refitted afterwards is not recorded);
160 of 366 DeepFluoro frames were stored upside down; the DeepFluoro focal length -5257.7 stays signed
(`context/deepfluoro-convention.md`). The full physics reproduction is `make physics` (exits non-zero if a number
moved), `make physics-tables`, `make physics-check` (`ssn:docs/HANDOFF_PHYSICS.md`); `make physics` hard-resets the
grid checkout and cannot fetch today (§0 item 2), so only `make physics-tables` is safe until fetching is restored.

---

## 7. The C-ArmLSpine level experiment

C-ArmLSpine: the only real intraoperative C-arm set with true laterals and a same-session CBCT (Zenodo 22768651, CC BY
4.0; PRSCS-Net, MedIA 97:103283): 149 cases (148 in most results), 299 spot frames (296 in the pre-repair bank behind
every published number), 149 CBCT, two 301-frame sweeps (`context/carmlspine-level-experiment.md`;
`ssn:docs/DATASHEET.md` §2.1). Entry document: `ssn:docs/HANDOFF_2026-09-21_PM.md` section "C-ArmLSpine is the project now".

### 7.1 Data preparation (scripts in `ssn:slurm/`, in order)

`carmlspine_fetch.sh` -> `carmlspine_dump_tags.sh` / `carmlspine_survey.sh` -> `carmlspine_nifti.sh` -> `carmlspine_seg.sh`
(+ `carmlspine_seg_s1.sh`; the two automatic labellers on the CBCT) -> `carmlspine_label_chain.sh` ->
`carmlspine_pose_chain.sh` / `carmlspine_pose.sh` (pose = header geometry SID 1140, SOD 745 + edge-only registration
`tools/drr_register.py`) -> `carmlspine_frames.sh` (frames with truth + crops) -> `carmlspine_prep.sh` / `carmlspine_preview.sh`.
The 2026-09-23 repairs: `carmlspine_repair_{census,seg,levels,pose,qc,bank,retry134}.sh` (PRE truth = before these,
REP = after). Zero-shot evaluation: `carmlspine_eval_chain.sh` submits `carmlspine_frames.sh` then `carmlspine_proto.sh`
per split with detector boxes and with truth boxes (`--export=ALL,BOXES=<b>,SPLIT=<s>,TAG=zeroshot`).

### 7.2 The cross-validation that the manuscript quotes

```bash
# five case-grouped folds, encoder re-initialised from v9 (the printed numbers)
# (from ~/spinesurg-ct-nnunet; the submit lines are the script headers' own)
sbatch -D ~/logs --array=0-4 slurm/carmlspine_cv_v9init.sh       # fold models ~/carm_cvmix{k}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt
sbatch -D ~/logs --array=0-2 slurm/carmlspine_cv_day_v9init.sh   # acquisition-day-grouped three folds
# closure: re-score every family on PRE truth with the gate (a Slurm job, reqp/requeue, 32 GB; never bash on warrior)
sbatch -D ~/logs SchwingNet/results/eval_gate/closure/cv_v9/closure_only.sh
```

Recorded: `carmcv9i` 40431706, closure 40436862 (after the `min_det_conf` fix), extras 40436901, zero-shot k-in-field
zs9kfield 40436982 with closure re-run 40437081 (`sn:results/eval_gate/closure/cv_v9/CV_V9.md`; `sn:REVISION_LOG2.md`).
Outputs `cv_v9.json`, `cv_v9_extras_pre.json`, `coupling_pre/coupling.json`. Then counting (`sbatch SchwingNet/slurm/counting.sh`
after `python tools/count_from_sacrum_eval.py --self-test`; report `python SchwingNet/tools/counting_report.py --in <dir> --out <dir>`,
both required, L175) and coupling (`sbatch --array=0-4 SchwingNet/slurm/coupling.sh`, its header's line, after
`python tools/alphabet_couple.py --self-test`; posteriors from
`tools/level_prototype.py --dump-posterior --sacrum-detector`). Figure 4: `python SchwingNet/tools/figure4_frame.py
--models v9init_pre --pull`.

Not in the printed results: `ssn:slurm/carmlspine_cv_v9.sh` ("A12" in its header) would rebuild the fold base sample
from `allspine_v9` (removing VinDr and FluoroCap); its own model paths "match nothing on disk"
(`sn:results/eval_gate/LINEAGE.md` lines 621-632). But its recipe was run, cell by cell: the 250 `name_fill` cells
(§1.2; `RESULTS_CATALOG.md` A9) are v9-base fold models with no VinDr or FluoroCap, N = all lateral 98.1 %, AP 97.0 %
(REP truth, per protocol cell). Running `carmlspine_cv_v9.sh` itself remains the way to replace the printed Table 3
cells for the VinDr / FluoroCap problem of `DATASET_USAGE.md` §5.

### 7.3 Traps (`context/carmlspine-level-experiment.md`)

Every CBCT slice has its own series UID (read with `tools/carmlspine_io.read_cbct`, never GDCM series grouping); no
FrameOfReferenceUID anywhere; DICOM PixelSpacing 1.0 is a placeholder (true pitch 0.150 mm: iRay Jupi1212X, 307.2 mm
panel; the poses were fitted at 0.1465 mm/px, so refit before reuse, `PREREG_rules.md`); case134's frames sit inside
CBCT/; case118 is AP + a -58 degree oblique; a third of cases name frames by UID (sort by PositionerPrimaryAngle);
lateral poses must be bounded around the header geometry (registration jumps half a vertebra on a periodic spine);
verify pose with detector boxes (`tools/carmlspine_pose_qc.py`), not the registration score; render calls with truth
(`tools/carmlspine_render_calls.py`) before believing a shift; a detector fine-tuned on a device's real frames and scored
on its held-out specimen is a same-device number; a case is an acquisition, not a proven person (report case-grouped and
day-grouped); case134/ori carries a real name: never print it (`ssn:docs/PATIENT_IDENTITY_SPEC.md` §2).

---

## 8. The benchmark suite

| benchmark | what it compares | how to run | state | source |
|---|---|---|---|---|
| head-to-head protocol | three axes, same cases / truth / metric, case-level bootstrap, frozen operating points, a comparator that cannot run reported as such: (1) detection and counting on real C-arm frames (pooled design P, LODO, same-device control, film-only, renders-only, retrained YOLOv8 / RT-DETR / Faster R-CNN, the LevelCheck registration ceiling); (2) naming on plain films (VertXNet, SpineCLUE unmodified); (3) every CT here by distinct subject | written 2026-09-22 before any comparator ran; arms listed with status | partial | `ssn:docs/BENCHMARK_PROTOCOL.md` |
| CT segmenters on CTSpinoPelvic1K (the one-shot space) | ours (Dataset810), TotalSegmentator v2, SPINEPS-CT + VERIDAH (+ Moller ribs), RibSeg v2, NV-Segment-CT (VISTA3D lineage), scored by `tools/eval_oneshot.py` and `tools/decode_sequence.py` | `python benchmark/make_case_table.py --raw nnunet/raw/Dataset810_SpineSurgLSTVOneShot --preprocessed nnunet/preprocessed/Dataset810_SpineSurgLSTVOneShot --hf_export ~/data/CTSpinoPelvic1K --out benchmark/cases.csv`; sanity `SYSTEM=gt PRED_DIR=.../labelsTr NAME_MAP=identity sbatch -D ~/spinesurg-ct-nnunet --partition=reqp --qos=requeue benchmark/score.sh` (must give Dice 1); `sbatch -D ~/spinesurg-ct-nnunet --partition=gmsap,gvohp,galhp benchmark/run_totalsegmentator.sh` then `SYSTEM=totalsegmentator sbatch -D ~/spinesurg-ct-nnunet --partition=reqp --qos=requeue benchmark/score.sh` (both scripts write `--output=logs/...` relative to the submit directory, so `logs/` must exist there, and they ask for `-q primary` / `-q gpu` with no partition: give the partition at submission); ours after `slurm/eval_fold_checkpoint.sh` | TotalSegmentator ready; SPINEPS container to pull; RibSeg has no released checkpoint; VISTA3D env built, smoke pending; `collect.py` "to write"; Dataset810 retired 2026-09-08 | `ssn:benchmark/README.md`; `context/competitor-benchmark.md` |
| re-implemented published 2-D methods and their ensemble | ours, cina, kim, vertx, konya rebuilt from their stated architectures, trained on one corpus, one held-out set; does a consensus beat the best one | `make competitors` (submits `slurm/competitor_ensemble.sh`), `make ensemble-report` | result NOT RECORDED (`~/model_night/ensemble/ensemble.json` on the grid) | `ssn:docs/COMPETITOR_BENCHMARK.md` |
| Cina-style whole-film benchmark | whole-film naming vs a sacrum-count rule | `ssn:slurm/benchmark_cina.sh` (`tools/benchmark_cina.py`, job 40323179) | saturated (99.96 % = 99.96 %); only the limited field discriminates | `context/feasibility-claims-measured.md` |
| X-ray level-ID bench and robustness | competitors, physics tiers, the recurrent head | `ssn:slurm/xr_bench.sh`; corruption suite `~/bench/robust/` | RECORD ONLY; note the wrong-bank attribution of the recurrent head (C1.2) | `context/xr-benchmark-and-robustness-2026-09-13.md` |
| the LSTV benchmark design | can one network name a rib by its vertebra (hypoplastic twelfth vs lumbar rib) and get the rib-free count right; L5 vs L6 is predicted to fail | design notes, written before the first run | design | `ssn:docs/LSTV_BENCHMARK.md` |
| TotalSegmentator render bench (sweep) | chains from the sacrum on 522 TS spines | `slurm/sweep_v3.sh` | only 71 cases are unseen by the v9 encoder: use `tools/unseen_cases.py` | `context/ts-bench-inside-v9-bank.md` |

Rules (`ssn:docs/BENCHMARK_PROTOCOL.md` "The rule that makes it fair"): same cases by patient key written before the runs;
one truth per axis made once; per-body recall and precision at a matched box convention with case-level bootstrap
(ignoring clustering: a naive 95 % interval covers 70.8 %, `tools/test_stats_compare.py`); same budget for retrained
arms; nothing tuned on the test split; the pooled number never quoted without the LODO number beside it.

---

## 9. CTSpinoPelvic1K: measurements, figures and the article

All heavy steps are batch jobs. Set `D=~/data/CTSpinoPelvic1K` (labels v11 at `$D/labels`, `labels_v10/` beside it, CT
at `$D/ct`). Sources: `working_notes/topic6_ctspinopelvic1k_and_toolkit.md` §15; `ctsp:paper/mpda/REPRODUCE.md` §1-5
(note: its §0 still says "The scheme is v10 ... S1=29" and §2 still describes the digitised Panjabi values; both stale).

1. **Get the release.** Labels from the Zenodo concept DOI 10.5281/zenodo.22139642 (v11 = 10.5281/zenodo.22797014;
   whether the concept DOI resolves to v11 or to v10 today is `OPEN_QUESTIONS.md` E7 and `MANUSCRIPTS.md` C1: if it
   resolves to v10, apply the merge step below to the Zenodo labels too); CTs
   rebuilt from TCIA with `ctsp:zenodo/fetch_from_tcia.py` and `ctsp:zenodo/reconstruct_ct.py` (SeriesInstanceUID in
   `manifest.json`), or downloaded from the Hugging Face mirror `OpenSpineConsortium/CTSpinoPelvic1K`, whose labels are
   still v10 (id 29 present) as of 2026-09-27: merge with
   `python scripts/merge_s1_into_sacrum.py --src <v10 labels> --dst <v11> --write`, check with `scripts/check_s1_merge.py`.
2. **Release gates (they stop the chain).**
   `python scripts/check_release_invariants.py --labels <v11> --ct <ct> --workers N --out qc_invariants.csv` (802 / 802 must
   pass); `python scripts/qc_rib_vertebra_incidence.py --labels <v11> --workers N --out <dir>`. Reason: on 2026-08-20 PI came
   back 154.6 degrees and SS 82.9 for all 802 records and the run exited zero (`ctsp:docs/RELEASE_CHECKLIST.md`).
3. **The seven extractors** (each takes `--labels`, `--manifest`, `--workers`, `--out`; the CT ones take `--ct`; each
   exits non-zero when a measure is outside its physiological envelope while still writing a good CSV: read the
   `*** N measure(s) outside the plausible range` line): `scripts/extract_level_gradients.py` -> `level_gradients.csv`;
   `extract_surgical_morphometrics.py` -> `surgical_morphometrics.csv` (Table III, Figure S2); `extract_pelvic_shape.py`;
   `extract_transition_morphometrics.py`; `extract_degenerative.py` (CT); `extract_opportunistic.py` (CT);
   `extract_proximal_femur.py` (CT; ~220 GB RAM at 8 workers, killed at 110 GB). Label-only extractors 15-30 min at 20
   workers; CT ones hours. **Recompute `pelvic_shape.csv`, `transition_morphometrics.csv` and `degenerative.csv` on v11**
   (they were written 2026-09-10 on v10 labels). Normalise case ids with `zfill(4)` before diffing. The batch wrappers in
   `ctsp:slurm/` (`level_gradients.sh`, `morphometrics.sh`, `pelvic_shape.sh`, `degenerative.sh`, `opportunistic.sh`,
   `proximal_femur.sh`, `finalize_release.sh`) still point at `data/v5_final` and use `-q primary`: edit before reuse.
4. **References.** `python morphometrics/make_reference_table.py` (writes `level_references.csv`, 365 rows; Panjabi 1991
   Table 3 values in since commit 83f7f95).
5. **Figures and tables of the article.**

| float | command | input |
|---|---|---|
| Table I prior art | hand-built in `main.tex` (black runs) | literature |
| Figure 1 pipeline | TikZ inline in `main.tex` (`fig_pipeline_standalone.tex`) | counts in text |
| Table II rib checks | `results/rib_qc_v4_vs_release/rib_qc_stages.py` (+ `rib_fragments_detail.py`) on the grid (job 40220664) | label trees |
| Figure 2 four phenotypes (0704, 0428, 0094, 0005) | `python scripts/make_fig_anchors.py --reselect` (calls `select_anchor_cases.py` -> `morphometrics/anchor_cases.json`, then `render_anchors.py`; flags `--scale_mode image --legend_cols 3 --panel_in 2.05 --height_in 2.35`); heavy | `transition_morphometrics.csv`, label volumes (default `data/zenodo_deposit/labels`). Trap: a check on retired id 29 inside `select_anchor_cases.py` once swapped a case silently |
| Table III spinopelvic | `scripts/extract_surgical_morphometrics.py`; numbers asserted by `paper/mpda/audit_ms.py` | `surgical_morphometrics.csv` |
| Figure 3 morphometry by level (L5 withheld for end-plate and pedicle width) | `python paper/mpda/make_levelatlas_fig.py` (also writes `morphometrics/level_atlas.csv`) | `level_gradients.csv`, `surgical_morphometrics.csv`, `level_references.csv`, `panjabi_reference.csv` |
| Figure S1 hardware | `python scripts/render_hardware.py --labels <v11>` (REPRODUCE) or `scripts/render_hardware_gallery.py` (audit_artifacts): which made the committed PDF is not recorded | labels, `metal.csv` |
| Figure S2 validation | `python paper/mpda/make_figures.py` (`fig_validation`); never pass a relative `--out` (it once wrote `paper/mpda/paper/mpda/figures/`) | `surgical_morphometrics.csv` |
| Figure S3 field of view | `python paper/mpda/make_fov_fig.py --census morphometrics/label_census_v11.csv` (the default is v7) | census CSV |
| Table S1 pseudolabeller Dice | `python scripts/extract_pseudolabel_dice.py` (fetches checkpoints from HF) | five Dataset803 checkpoints |
| Table S2 completeness | hand-written from `manifest.json` | `manifest.json` |
| Table S3 identifier census | `python scripts/make_census_table.py --census morphometrics/label_census_v11.csv --out paper/mpda/census_table.tex` | `label_census_v11.csv` (the command that produced it is not recorded; `scripts/label_census_v7.py --labels <v11>` is the likely one) |

6. **Audit.** `python paper/mpda/audit_artifacts.py --regen` (each artefact has a recorded generator; cheap ones re-run
   and pixel-compared); `python paper/mpda/audit_ms.py` (every number in the text against its CSV); `python
   paper/mpda/audit_pdfs.py` (the packet PDFs, including the v11 DOI).
7. **Build.** Prerequisite: TinyTeX in WSL with revtex4-2 and the packages listed in the header of
   `ctsp:paper/mpda/build.sh` (the grid's TeX carries revtex4-1 and cannot build this article). `bash paper/mpda/build.sh --reprint` -> `CTSpinoPelvic1K_reprint_check.pdf`: **the only page count that
   matters (at most 10 published pages)**; read the whole output, LaTeX prints a PDF and a page count on top of a broken
   table; `build.sh` without the flag gives the ~25-page submission form, meaningless for the limit; then
   `bash paper/mpda/make_arxiv.sh`, `python paper/mpda/make_overleaf.py`, and `python paper/mpda/make_submission.py`
   **from Windows** (it shells out to `wsl`) -> flat `dist/submission/`. The structured abstract goes in the submission
   form (`make_abstract_text.py`), not the PDF.
8. **ostk numbers.** `python -m ostk morph --labels <dir> --out morph.csv --workers 8`;
   `python -m ostk all --labels <dir> --out summary.csv --workers 8`; but on v11 labels ostk takes the whole-sacrum
   fallback for S1 silently (`RESULTS_CATALOG.md` G.3) and its canal mask carries the 1b7005c regression (G.2): do not
   trust its PI or its posterior body height until both are fixed.
9. **New Zenodo version** (`context/zenodo-deposit.md`): `scripts/renumber_labels.py --map vN` ->
   `zenodo/finalize_v9.py --new labels_vN --old labels_vM_old --max-id 68` ->
   `python3 zenodo/new_version.py --record <latest> --version vN --dir data/zenodo_deposit --replace <files>` ->
   `python3 zenodo/upload.py --publish <id>`; update `\datasetversion` and the DOI in `paper/mpda/main.tex`,
   `title_page.tex`, `cover_letter.md`; mirror with `hf/push_v9.py`; integer versions only. Network through WSL; token
   file `~/.zenodo_token` (never printed).
10. **Commit and push.** Directly to master; `git push origin master && git push osc master` through WSL; ostk on branch
    `main`, both remotes.

The full rebuild of the release from published sources is `ctsp:docs/BUILD_CHAIN.md` (13 steps for v10; model outputs
archived because they are not bit-reproducible; build archive 10.5281/zenodo.22647933; tag `v10-build-archive`;
`CHAIN_CHECK_v7_to_v10.txt` shows steps 12-13 regenerate all 802 volumes voxel for voxel); v11 is one more deterministic
step.

---

## 10. The data accounting and leakage checks

Full explanation in `LEAKAGE.md`; the commands (`ssn:docs/DATA_ACCOUNTING.md` §5.3, §6, §6.1; `ssn:slurm/data_accounting.sh`
header; `ssn:tools/leak_check.py` docstring):

```bash
# the content-hash chain on the grid (two submissions; the second refuses a partial ledger)
cd $HOME/spinesurg-ct-nnunet
A=$(sbatch --parsable -D $HOME/spinesurg-ct-nnunet --array=0-15 --export=ALL,STAGE=ledger slurm/data_accounting.sh)
sbatch -D $HOME/spinesurg-ct-nnunet --dependency=afterany:$A --export=ALL,STAGE=rest --cpus-per-task=8 --mem=64G \
  --time=04:00:00 --output=/wsu/home/go/go24/go2432/model_night/logs/data_accounting_rest_%j.out slurm/data_accounting.sh
# outcome: grep DATA_ACCOUNTING_LEAK_CHECK in the stage-2 log; outputs under $RS/data/or_ready/data_accounting

# self-test of the chain on the laptop: a planted leak must fail, a clean tree must pass
python tools/diagnostics/make_fake_corpus.py --out <scratch>/fake_leak
python tools/diagnostics/make_fake_corpus.py --out <scratch>/fake_clean --clean
# each only builds a tree; the test is the `ALLOW_LOCAL=1 STAGE=all ... PY=python bash slurm/data_accounting.sh` line it
# prints: run that line (the leaking tree must exit non-zero, the clean one zero)

# the bank and split audit alone (in a job)
python tools/leak_check.py check --out /rs/rs_grp_oschome/go2432/data/or_ready/leak
# CHK-9 over every quoted number, as the recorded job (writes chk9_report.json and CHK9_REPORT.md under $RS/.../eval_gate/chk9);
# a bare `python tools/leak_check.py chk9` lacks --quoted-results/--touched/--eval-sets, prints CHK9 COULD NOT RUN, exits 3
sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate -p reqp --qos=requeue \
  --export=ALL,STAGE=chk9 ~/spinesurg-ct-nnunet/slurm/eval_gate.sh
python SchwingNet/results/eval_gate/leaks/build_eval_leaks.py     # rebuild EVAL_LEAKS.md
# the G3 person split with its checks CHK-1..CHK-8: FROZEN (apply 2026-09-23 20:18:48, job 40426793). Do not submit
# g3_split.sh as a check: it re-globs today's ann roots and rewrites ~/split_final.json in place with os.replace and no
# backup (tools/make_split.py L978-981), although the file's own _about says "never redraw"; it also rewrites
# split_plan.md. To re-verify, copy the script with --split-out and --out-dir on a scratch Ceph path (or copy
# ~/split_final.json aside first), then diff side_of_person against the frozen file.
# the gate, on the laptop
python -m pytest tests/test_eval_gate.py -v
python tools/test_patient_keys.py ; python tools/test_leak_check.py
# 2026-10-08: test_leak_check.py FAILS on one stale fixture ("phantom_p01_065kv -> geneva:phantom want
# geneva:phantom_p01", AssertionError "30 real names, 1 wrong", L312). The keyer was changed on purpose: the Geneva
# resin phantom is one person, not 19 (SchwingNet/results/eval_gate/EVAL_LEAKS.md item 3); the fixture still expects
# the old per-position key. Changing the fixture to geneva:phantom waits on Greg (OPEN_QUESTIONS.md F17).
# real-frame banks (fail-closed admission list), in a job: it reads the grid path
python tools/realxray_train.py check --root /rs/rs_grp_oschome/go2432/data/realxray
# the list audit is its job (a bare audit_realxray_lists.py fails: --out is required)
sbatch slurm/audit_realxray_lists.sh       # -> $RS/tmp/realxray_lists_audit.json; copy to SchwingNet/results/
# the usage table (in a job; reads every ~/*/rung_1.npz)
python tools/xray_dataset_usage.py --out ~/model_night/XRAY_DATASET_USAGE.md
```

The doc's own `/tmp/...` paths for the fake corpus should be a scratch directory on the laptop. **The content-hash chain
has never been run on the real corpus as far as any file records** (`$RS/data/or_ready/data_accounting/` did not exist on
2026-09-22; CHK-6 and CHK-7 are NOT RUN in the G3 split). Before the next run of `xray_dataset_usage.py`: rename
`buu_2000` in its `RAW` list (it is the BUU-LSPINE 2000 release, not "AASCE test split"), key raw datasets with
`tools/patient_keys.py` rather than substrings, and update the HOME paths after the Ceph migration
(`ssn:data_platform/DATA_MANIFEST.md` Appendix B item 3).
