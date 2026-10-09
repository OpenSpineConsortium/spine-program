# Topic 2: scaling plots, accuracy against number of samples, the anomaly scan, and the power calculations

Written 2026-10-08 from files on the laptop only. The grid was not contacted and no network was used. Every entry
names the file it was read from. A fact that no file records is written "not recorded". Where two files disagree,
both readings are given in Part E with the one trusted and why. The unknowns table is Part F.

## How to read this note

### Citation keys

| key | path |
|---|---|
| `ssn:` | `<spinesurg-ct-nnunet 097933a>/` (private repo, branch L6_Class; HEAD d5dee9a on 2026-10-08) |
| `sn:` | `ssn:SchwingNet/` |
| `ctsp:` | `<CTSpinoPelvic1K 7ddfe38>/` |
| `mem:` | `<the memory folder; copies in memory/ of this project, statuses in docs/handoff/context/INDEX.md>/` |
| `HO:` | `ssn:HANDOFF/literature_state/` (committed d5dee9a, 2026-10-08; its `power.md` is the full power inventory) |
| `~` | grid HOME `/wsu/home/go/go24/go2432` |
| `RS` | grid Ceph `/rs/rs_grp_oschome/go2432` |

### Tags on numbers

| tag | meaning |
|---|---|
| [M] | measured on persons held out from training and from checkpoint selection (the file says HELD OUT or `eval_gate` passed) |
| [M-sel] | measured on a selection split: the validation persons also chose a checkpoint, or the encoder's bank trained on them |
| [M-dev] | development number on a validation side, declared as such by its file |
| [D] | derived read-only from committed rows by an agent, not by a committed tool |
| [E] | expectation (a prevalence prior times a measured field-of-view probability), not an observation |
| [X] | extrapolation of a fitted curve beyond the largest N measured |
| [S] | superseded: do not quote |

### Which manuscript carries these results

The RSNA AI manuscript is `sn:main.tex` (sections in `sn:sections/`, numbers through `\RESULT{}` keys of
`sn:numbers_manifest.json`, build chain in `sn:RESULTS_BUILD.md`). Figure 5 there is the scaling figure
(`sn:main.tex` L199-213; last rebuilt 2026-09-25 13:47 per `git log -- SchwingNet/main.tex`). The file
`ssn:paper/rsnai/main_v2.tex` is an earlier k-devices draft (last commit 2026-09-22 22:37) whose scaling items are
still `\todo{[C7] ... [C8] scaling curve}` (`ssn:paper/rsnai/main_v2.tex` L40, L78). See Part E row 1.

---

## 0. The short version

1. **The current accuracy-against-samples evidence is Figure 5 of the SchwingNet manuscript** (`sn:figures/figure5.*`,
   built by `sn:tools/fig_power.py`, numbers in `sn:results/power/power.json`, generated 2026-09-25 13:41). Panels:
   (a) Wilson lower bound against transitional test persons; (b) naming against training persons on three film
   corpora and on one C-arm per view; (c) same-device detection against real frames, with one-view arms; (d)
   render-only detectors at matched N read along the lateral angle (`sn:figures/figure5.caption.txt`).
2. **Film naming rises with persons, from a render-only encoder** [M]: NHANES II 27.2 % (0 persons) -> 77.8 % (5) ->
   92.7 % (all 264); BUU-LSPINE 10.3 -> 65.0 -> 96.9 % (2,967); CSXA 3.2 -> 94.2 -> 99.8 % (4,114)
   (`sn:results/coverage/film_ncurve/FILM_NCURVE.md`).
3. **Renders help film naming only while film is scarce** [M]: render-only minus film-only = +21.9 / +11.1 / +18.7
   points at 5 persons and +12.2 / +6.0 / +6.2 at 25 (NHANES / BUU / CSXA), every seed separated; with every person
   the arms are level, and BUU is 1.6 points the other way, separated (`sn:results/coverage/film_ncurve/ablation/READ.md`).
4. **C-arm naming per view** [M]: lateral 93.7 % with no C-arm person -> 98.1 % with 50; AP 33.8 % -> 90.8 % with
   five -> 98.1 % with all (87.6 persons); a lateral-trained model names 54.7 % of AP bodies
   (`sn:results/indomain/name_fill.json#figure5b`, `sn:results/indomain/INDOMAIN.md` §5-6).
5. **Same-device detection plateaus from 24 frames (12 patients)** at about 84 % (body boxes, 0.74) [M]; the plateau is
   the truth boxes, not the detector: on complete, agreed, body-sourced boxes it is 95.6 % (642 boxes)
   (`sn:results/indomain/FIT_N.md`; `sn:results/indomain/denominator_repair.json`; `sn:REVISION_LOG3.md` §11).
6. **Accuracy follows where the frames sit in acquisition space, not how many there are** [M on renders]: AP+LAT-pose
   render arms find 82.1 % at the trained angles and 52.8 % over 16 other bins; doubling those frames gives 94.2 /
   64.8 %; the same count spread over the arc gives 80.7 / 77.1 % (`sn:results/power/power.json#panel_d_angle/summary`).
7. **Never measured:** a synthetic:real ratio sweep (the design fixed about 1:1 by rows), per-angle naming, per-level
   film naming on held-out persons, seeds above N = 25 on film, and any real-frame transitional test person
   (`sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md`, "What is not known").
8. **The older 2026-09-17 synthetic/real fraction sweep (`~/scaling`) is superseded**: it ran on the v2 bank, which
   leaked NHANES persons across the split and was deleted on 2026-09-20 [S] (`sn:results/indomain/INVENTORY.md` G8;
   `mem:grid-quota-and-deleted-banks.md`; `mem:nhanes-double-inclusion.md`).
9. **The anomaly scan** is a chain: anomaly manifest (2026-09-17) -> transitional subtypes and the G3 split
   (2026-09-23) -> five harvest streams and the one registry (2026-09-24: L6 146, T13 14 persons) -> acquisition
   screens over 18 public collections (2026-09-23/25) -> the ruleclass "SUPER DETECTOR RUN" census of 21,622 CTs and
   its tier lists (2026-09-27) -> a four-rule pre-registration (DRAFT v1, not frozen) -> a review tree whose code is on
   disk but untracked in git and, as far as any file records, not yet run.
10. **Power:** with no error, 35 transitional persons put the Wilson lower bound at 90 % and 22 carriers put variant
    sensitivity at 85 % (`sn:results/power/power.json#n_needed_zero_errors`; re-derived here). Today 7 unverified real
    at-risk persons with an exported frame exist (bound 64.6 %), and the 51 at-risk CT test persons are mostly in the
    encoder's training lineage (`sn:sections/results.tex` L91-98). Every power row of the programme is in
    `HO:power.md`.

---

# Part A. Scaling plots and accuracy against number of samples

## A.0 Every curve on disk, one row each

| # | curve | question | x axis | y axis | status | primary file |
|---|---|---|---|---|---|---|
| A1 | synthetic/real fraction sweep, 2026-09-17 | does adding renders help film naming; how much real film is needed | render fraction 0-1 at real 1.0; real fraction 0.25-1 at render 1.0 | interior-window exact level on real films | [S] leaky v2 bank | `sn:results/indomain/grid/scaling_curve_2026-09-17.json` (copy of `~/model_night/scaling/SCALING_CURVE.json`) |
| A2 | `eval_scaling_curves` (devices, cases, fewshot), 2026-09-22 | does a held-out device improve with more training devices / persons / few real frames | k devices; persons; shots | held-out recall | partial: devices at k = 1, 2 only and fit refused; fewshot never ran; cases not recorded | `ssn:slurm/eval_scaling_curves.sh` foot; `sn:results/indomain/INDOMAIN.md` L13 |
| A3 | real-frame detection learning curve (`lcurve`), 2026-09-23 | how many real frames of a device a render-pretrained detector needs | real frames N per device | vertebra recall, sacrum found | measured; superseded for Figure 5 by A4 | `sn:results/lcurve/lcurve.md`, `lcurve.json`, `fig_lcurve.png` |
| A4 | same-device detection fill (`det_fill`), 2026-09-24 | the same, finer N grid, one-view arms, out-of-domain arms at matched N | real C-ArmLSpine frames | recall @0.74 body / centre | measured; Figure 5c | `sn:results/indomain/det_fill.json` |
| A5 | C-arm naming fill (`name_fill`), 2026-09-24 | naming on real C-arm frames against in-domain persons, per view, against film and renders at matched persons | C-ArmLSpine persons per view | exact level | measured; Figure 5b (C-arm) | `sn:results/indomain/name_fill.json` |
| A6 | inverse-power-law fits of A4/A5, 2026-09-24 | asymptote and N to a target | N | fitted accuracy | fitted; 2,000-resample intervals | `sn:results/indomain/fit.json`, `INDOMAIN.md`, `FIT_N.md` |
| A7 | film N-curve, 2026-09-24 | film naming against training persons per corpus, from an encoder that never saw film | persons per corpus | exact level on v9 VAL films | measured; Figure 5b (film) | `sn:results/coverage/film_ncurve/film_ncurve.json`, `FILM_NCURVE.md` |
| A8 | film N-curve ablation, 2026-09-25/26 | do renders help ordinary-level film naming | same | same, three arms | measured; in the Discussion | `sn:results/coverage/film_ncurve/ablation/READ.md`, `ablation_read.json` |
| A9 | acquisition-space coverage census, 2026-09-24 | where every corpus and training set sits in angle / tilt / roll / magnification / field | per dimension bins | coverage C, entropy H* | measured (no model) | `sn:results/coverage/coverage.json`, `COVERAGE.md`, `fig_density*.png` |
| A10 | matched-N coverage arms, 2026-09-25 | at the same N, does pose coverage change what a render-only detector finds | lateral angle bin | body recall @0.25 | measured on renders; Figure 5d | `sn:results/coverage/experiment/EXPERIMENT.md`, `scores.json`, `runs/*/unseen/recall_vs_angle.json` |
| A11 | pooled nested fit N vs N + H*, 2026-09-25 | is the plateau N alone or N plus coverage | N and H*_lat | all points of A4, A5, A7, A10 | fitted; quoted in Results, not drawn | `sn:results/coverage/pooled_fit.json`, `POOLED_FIT.md`, `sensitivity/` |
| A12 | dimension exploration, 2026-09-25 | film against fluoroscopy, pooled against view-separated | persons / frames | naming / detection | measured, nothing retrained | `sn:results/coverage/dimension/film_vs_fluoro_dimension.{json,png}`; `mem:acquisition-space-saturation.md` |
| A13 | miss diagnostic and denominator repair, 2026-09-25 | why the same-device curve plateaus | arm | recall on repaired truth | measured | `sn:results/indomain/miss_diagnostic/`, `denominator_repair.json`; `sn:REVISION_LOG3.md` §11 |
| A14 | contribution matrix | which training source carries held-out detection | training set | held-out recall | measured; Figure S3 | `sn:results/contribution_matrix.{json,md}` |
| A15 | LSTV flag learning curve | does harvesting more transitional patients help a 2-D flag | positive training patients 10-120 | AUC within cohort | measured (grid file) | `~/lstv_flag/LEARNING_CURVE.md` (grid only), quoted in `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` L659 |
| A16 | D1 head data saturation (paper 2) | does the LevelCheck-comparison head saturate in data | fraction of 8,950 training persons | validation accuracy | [M-dev] | `sn:results/dual_loss/saturation.json`, `saturation_curve.csv`, `saturation_epochs.csv` |
| A17 | nnU-Net ablation array (CTSP segmentation) | six modelling choices of the segmentation model | ablation | Dice | results not on the laptop | `ssn:docs/ablations.md` (first commit 2026-04-18) |

## A.1 The 2026-09-17 synthetic/real fraction sweep (`~/scaling`) [S]

**What it says.** Six encoders on subsets of the v2 bank, scored on the same 455 held-out real lumbar films
(interior windows, film-clustered 95 % intervals) (`sn:results/indomain/grid/scaling_curve_2026-09-17.json`):

| point | render fraction | real fraction | ordinary lumbar | anomalous lumbar (12 films, 47 windows) | cervical (636 films) |
|---|---:|---:|---|---|---:|
| s000_r100 | 0 | 1.0 | 89.5 % [86.9, 92.0] | 34.0 % [8.9, 66.7] | 98.8 % |
| s025_r100 | 0.25 | 1.0 | 87.7 % [84.6, 90.5] | 44.7 % [18.0, 76.3] | 98.8 % |
| s050_r100 | 0.5 | 1.0 | 87.4 % [84.3, 90.2] | 53.2 % [24.6, 86.4] | 98.0 % |
| s100_r100 | 1.0 | 1.0 | 88.2 % [85.3, 91.1] | 36.2 % [14.3, 64.9] | 98.3 % |
| s100_r050 | 1.0 | 0.5 | 84.3 % [80.9, 87.4] | 53.2 % [25.6, 72.9] | 98.5 % |
| s100_r025 | 1.0 | 0.25 | 83.7 % [80.5, 86.8] | 38.3 % [16.4, 67.6] | 97.1 % |

The reading at the time was "renders buy variant anatomy, not the film domain" (render fraction 0 -> 0.5 moved
anomalous 34.0 -> 53.2 % while ordinary fell 2 points; cutting real film to a quarter cost about 5 points)
(`mem:remedies-refuted-2026-09-17.md`; `ssn:paper/rsnai/graveyard.tex` L65). Two cautions the files themselves
support: the anomalous column rests on 12 films and every interval overlaps every other; and the curve is not
monotone (s100_r100 anomalous 36.2 % sits below s050). **Why superseded:** the v2 bank split each source
separately, so 48 of 54 NHANES validation patients had their other copy in training
(`mem:nhanes-double-inclusion.md`; `ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`); `INVENTORY.md` marks every
row of this sweep "NOT ESTABLISHED" as held out (`sn:results/indomain/INVENTORY.md` L299-304) and says "that model
line is superseded and not quotable" (`sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md`, Table A note). The v2 bank was
deleted on 2026-09-20 (`mem:grid-quota-and-deleted-banks.md`).

**Inputs and code.** Base bank `~/allspine_v2_fov96_ctx` (deleted). `ssn:tools/subset_bank.py` cuts a bank by FILM,
seeded, stratified by source; validation rows are copied unchanged so every point scores the same crops; "real"
means a source in `REAL_SOURCES` of `ssn:tools/eval_feasibility_claims.py` L79 (csxa, buu_full, nhanes, vindr,
aasce, mendeley, NHANESPS, VINDRPS, LAT236PS) or whose prefix before `_` is one of them. It has a
`--drop-val-twins` option written for exactly the NHANES defect. `ssn:slurm/scaling_sweep.sh` builds the six banks
under `~/scaling/<tag>`, trains each encoder with the short recipe (ResNet-18, CE, 8 epochs, via
`slurm/night_arm.sh`), fits a mixed-length head (`tools/head_mixed_length.py`, 15 epochs, kmax 4), scores with
`tools/eval_interior_windows.py --real-only 1`, and writes `~/model_night/scaling/SCALING_CURVE.json`.
`ssn:tools/make_feasibility_figures.py` L429-451 draws it as `fig9_scaling` under
`~/model_night/figures_feasibility/` (grid; no local copy found). The grid job id of the 2026-09-17 run is not
recorded in any file found. `~/scaling` (129.2 GB on 2026-09-20, `mem:grid-quota-and-deleted-banks.md`) is
planned to move to `RS/data/multisource_banks/derived/scaling` in migration batch B11
(`ssn:data_platform/plan/layout_map.csv` L298).

**Recipe, if a clean film fraction curve is ever wanted** (`sn:results/indomain/INVENTORY.md` G8):

```bash
# grid, from the login node; GPU job, 6 points, 40 h limit
sbatch -D ~/spinesurg-ct-nnunet --export=ALL,BASE=$HOME/allspine_v9_fov96_ctx slurm/scaling_sweep.sh
# writes ~/scaling/<tag>/ banks and ~/model_night/scaling/SCALING_CURVE.json; then
python tools/make_feasibility_figures.py --results ~/model_night --out ~/model_night/figures_feasibility
```

The proper replacement for this question is the ratio sweep that was proposed and never run (A.18).

## A.2 `eval_scaling_curves`: devices, cases, few-shot (2026-09-22) [partial]

`ssn:tools/eval_scaling_curves.py` (1,652 lines) was written to test the project's economic claim, that a new C-arm
costs a parameter fit rather than a labelled dataset, along three axes: held-out-device recall against the number of
training devices k (plan box C8), level accuracy against training persons, and held-out recall against a few real
frames of the held-out device (docstring). `ssn:slurm/eval_scaling_curves.sh` runs one mode per job and writes
`~/scaling_curves/` (deliberately not `~/scaling`). State recorded at the foot of that script (2026-09-22):
devices measured at k = 1 for all three held-out devices and k = 2 for Elekta XVI; with two distinct k the tool
refuses to fit a form, and three corpus devices cannot reach past k = 2; one cell is "derivable now" (Elekta held
out, Cios-only design-A model: 38.1 % [32.3, 44.5] at 0.25), which would move the drawn Elekta slope from +19.2 to
+6.3 points per device. `cases` needed the v8 encoder `model_r18_ce_v8.pt`, which did not exist yet. `fewshot`
needed only GPU time. `sn:results/indomain/INDOMAIN.md` L13 records the outcome: "devices curve measured at k = 1, 2
only and refused a fit; fewshot never ran ... Superseded by the lcurve/det_fill cells". Whether `cases` ever ran is
not recorded. `sn:results/eval_gate/EVALUATORS.md` L326 notes the tool is "not on the path of a quoted number".

## A.3 The real-frame detection learning curve (`lcurve`, 2026-09-23)

**Design** (`sn:results/lcurve/lcurve.md` "Design"; `ssn:tools/lcurve_train.py`). Stage 1 = the design-B
leave-one-device-out detector of the device (styled renders of the other two devices plus their real train frames
×2). Stage 2 = full-depth fine-tuning (SGD lr0 0.005, 20 epochs, no early stopping) on the stage-1 list plus the
device's own styled renders plus N real frames repeated to about 15 % of the epoch. Nested subsets of whole cases;
checkpoint by the device's real VAL split (fixed, not counted in N); test = the realxray test split, never in any
list; the three real L6 patients of C-ArmLSpine (case42, case121, case136) removed from every list and scored as
their own row.

**What it says** (`sn:results/lcurve/lcurve.md`) [M]:

| device | N = 0 | N ≈ 50 | N ≈ 100 | N ≈ 200 | N ≈ 400 | all real, pooled |
|---|---|---|---|---|---|---|
| C-ArmLSpine (Surgio-B51), vert recall @0.74, body truth, 287 bodies / 28 cases | 7.3 % | 81.5 % | 81.5 / 80.5 % | 80.1 / 82.2 % | unreachable (pool 208 frames) | 81.9 % (210 frames) |
| COBRA Elekta XVI @0.74, body truth, 893 bodies | 12.9 % | 24.6 % | 22.1 / 19.0 % | 31.2 % | 22.8 / 45.5 % | 93.2 % (2,640) |
| DeepFluoro (Cios Fusion) @0.74, 83 bodies, one specimen | 9.6 % | 33.7 % | 79.5 / 49.4 % | 55.4 % / 13.3 % (N 214 / 238) | - | 73.5 % (238) |

C-ArmLSpine transitional row: 74.3 % (26/35) from N = 50 on, three clusters, no usable interval. The COBRA body-truth
figures are a box-convention mismatch, not a learning effect (`sn:results/indomain/INVENTORY.md` "What the existing evidence already shows" item 5;
`sn:results/bodybox_rescore/`); DeepFluoro is one specimen and not monotone, so it "cannot carry Figure 5"
(`INVENTORY.md` item 6). Commit 180fb0f's message: "The real-frame learning curve lands, and it says the box convention
is the story".

**Jobs** (`sn:results/lcurve/JOBS.txt`): prep 40416377 (COMPLETED 01:37 EDT 2026-09-23; an earlier prep 40416368
failed because an unquoted remote `sed -i s/\r$//` deleted a trailing "r" from lines), array 40416378_0-18 (one task
per line of `sn:slurm/lcurve_manifest.txt`), report 40416379 (`sn:slurm/lcurve_report.sh`). Lists at
`RS/data/devcorpus/lists/lcurve_<device>_N<target>_s<seed>/`; runs `~/spine-detector/runs/lcurve/`; dumps
`RS/data/or_ready/lcurve/{dumps,results}/`.

**Recipe:** `sbatch -D ~/spinesurg-ct-nnunet SchwingNet/slurm/lcurve_prep.sh`, then the array
`SchwingNet/slurm/lcurve.sh` over the manifest, then `SchwingNet/slurm/lcurve_report.sh` (afterany), then rsync
`lcurve.{json,md}` and `fig_lcurve.png` back (`sn:results/lcurve/JOBS.txt`).

## A.4 Same-device detection fill (`det_fill`, Figure 5c) and A.13, the plateau explained

**Design** (`sn:results/power/power.json#panel_c_detection/design`): N real C-ArmLSpine frames = both views of N/2
training patients, nested subsets, added to a fixed background; one-view arms (25 or 50 frames of one protocol);
out-of-domain arms at matched N (COBRA Elekta frames; styled renders of this device posed on the same patients'
registered poses); a box-convention control (outline). Test = the released 28-patient test split, repaired truth
(LAT 27 patients / 138 vertebrae, AP 28 / 143 per seed). Body rule at the pre-stated 0.74 is the reported convention.

**What it says** [M] (`sn:results/indomain/FIT_N.md`; `power.json#panel_c_detection/curves`):
- Body @0.74, both views pooled: N = 0 7.7 % (66/861), 4 72.4 %, 10 76.0 %, 24 84.0 % (723/861), 50 82.5 %.
  Lateral asymptote 81.7 % [76.7, 86.6], AP 85.3 % [81.0, 90.7]; 95 % of the asymptote at 10.0 [5.1, 23.5] (LAT)
  and 11.9 [6.7, 33.5] (AP) frames; 90 % absolute recall "not reached" in 100 % (LAT) and 96 % (AP) of resamples.
- At 0.25 (centre rule) the asymptotes are 92.3 % (LAT) and 93.9 % (AP).
- Model-free plateau check: N = 24 against N = 200, LAT +2.2 points [-1.1, +6.0], AP +1.7 [+0.0, +3.8]
  (`INDOMAIN.md` §2).
- One-view arms: own view 83.0-86.4 %, other view 0.0-39.5 % (`power.json#panel_c_detection/summary`).
- Out-of-domain at matched N: no arm up to 50 reaches 24 in-domain frames; in-domain +28.5 points over COBRA and +15.7
  over styled renders on LAT, +20.7 and +27.0 on AP (`INDOMAIN.md` §3, model-free reading "the one to quote").
- The N = 0 body-rule floor is a box-convention artefact: arms without C-ArmLSpine frames draw whole-vertebra boxes,
  which the body rule scores as misses on the lateral view (`INDOMAIN.md` §2).

**Why it plateaus (A.13)** [M] (`sn:REVISION_LOG3.md` §11; job 40448862, `ssn:tools/carm_miss_diagnostic.py`;
`sn:results/indomain/miss_diagnostic/`; job 40448892, `ssn:tools/carm_denominator_repair.py`):
30 of 287 test vertebrae are missed by every plateau arm and 208 hit by every arm; vertebrae cut by the CBCT boundary
are missed 51.5 % of the time against 6.7 % for complete ones; on complete, agreed, SPINEPS-boxed bodies the plateau
arms read 96.9 %. On the repaired denominator N = 24 reads 95.6 % [92.9, 98.0] (614/642) against 84.0 % released,
and N = 200 reads 94.9 % (406/428) (`sn:results/indomain/denominator_repair.json#summary`). The text consequence was
left for Greg (`REVISION_LOG3.md` §11, "NOT yet applied").

**Jobs.** lcfill 40429442_0-5, collect lcfcoll 40436400, COMPLETED 08:07 on 2026-09-24
(`sn:results/coverage/PENDING_JOBS.json#done_before_this_pass`). Scripts `sn:slurm/lcurve_fill*.sh`
(`lcurve_fill_plan.sh`, `lcurve_fill.sh`, `lcurve_fill_boxstyle.sh`, `lcurve_fill_outline_prep.sh`,
`lcurve_fill_collect.sh`); tool `ssn:tools/lcurve_fill.py`. Per-frame hits `sn:results/indomain/detfill/grid/percase.json`
(`INDOMAIN.md` §10).

## A.5 C-arm naming fill (`name_fill`, Figure 5b C-arm)

**Design** (`ssn:tools/indomain_name_fill.py` docstring; `power.json#panel_b_carm/design`): the five case-grouped
folds of `tools/carmlspine_to_bank.py` (md5(case) % 5 == K test, (K+1) % 5 val); N = 0, 5, 10, 25, 50, all
C-ArmLSpine training cases of ONE view protocol (N = 100 cannot be drawn: no fold pool holds 100); recipe
`ssn:slurm/carmlspine_cv_v9.sh` (A12) verbatim with init `~/allspine_v9_fov96_ctx`; every cell scored on both
protocols; out-of-domain comparators at the same person counts (same-protocol plain films, same-protocol CT renders,
the other C-arm protocol). Scoring through `tools/level_prototype.py`, which runs `tools/eval_gate.py` on every
model chain against every test image's patient.

**What it says** [M] (`sn:results/indomain/INDOMAIN.md` §5-6; `name_fill.json#figure5b`):

| series | N = 0 | 5 | 10 | 25 | 50 | all (87-87.6 persons) |
|---|---:|---:|---:|---:|---:|---:|
| LAT trained, read on LAT, whole frame | 93.7 | 96.7 | 96.5 | 97.5 | 98.1 | 98.1 |
| AP trained, read on AP, whole frame | 33.8 | 90.8 | 94.7 | 95.4 | 95.4 | 98.1 |
| AP, 3 vertebrae in view | 28.5 | 69.4 | 75.1 | 81.4 | 83.7 | 87.6 |
| AP, 1 vertebra in view | 15.7 | 52.8 | 59.5 | 64.8 | 70.0 | 74.6 |
| LAT, 3 in view | 83.6 | 89.8 | 90.9 | 91.8 | 93.5 | 93.1 |
| LAT, 1 in view | 63.9 | 69.2 | 70.0 | 72.2 | 75.1 | 77.1 |
| LAT trained, read on AP | 32.2 | 33.1 | 36.0 | 39.9 | 51.0 | 54.7 |
| AP, same-protocol plain films (persons) | - | 80.6 | 83.6 | 94.5 | 97.9 | 96.4 |
| AP, same-protocol CT renders (persons) | - | 26.2 | 33.5 | 42.5 | 41.5 | 53.7 |
| both protocols trained (LAT / AP) | - | - | - | - | - | 98.1 / 97.0 |

Exchange rates (substitute persons per in-domain person): AP whole frame, film 3.6 at N_in = 5, 1.7 at 25, 1.2 at 50;
renders millions [X] (`INDOMAIN.md` §6). The whole-frame asymptotes are not identified (the curves sit at 97-98 %);
the narrow-field curves are still rising at 88 persons, so "no number of cases can be quoted for 97 % there"
(`INDOMAIN.md` §8). Zero-shot references: LAT whole 96.3 % (600/623), AP 43.9 % (278/633) (`INDOMAIN.md` §5).

**Jobs.** namefill arrays 40429416 and 40429901 (tasks 8 and 16 cancelled 07:36, re-run by namefillr 40436049_0-9,
COMPLETED 08:35 on 2026-09-24); 250/250 cells scored (`PENDING_JOBS.json#done_before_this_pass`). Scripts
`sn:slurm/name_fill*.sh` (prep, cpu, apfilm, keytest, retry, revise, survey, collect). Per-case rows
`sn:results/indomain/fit/name_percase.json` (job 40436856, `ssn:tools/indomain_fit_percase.py`).

## A.6 The fits: Figueroa inverse power law

**Method** (`sn:results/indomain/INDOMAIN.md` §1; `FIT_N.md` "Method"): acc(N) = A − B·N^(−C), weighted nonlinear
least squares with rank weights j/m (Figueroa RL et al., BMC Med Inform Decis Mak 2012;12:8,
doi:10.1186/1472-6947-12-8, verified 2026-09-24 against PMC3307431), fitted on N > 0, multi-start, A in [0, 1].
Interval: case-clustered percentile bootstrap of the whole fit (resample test patients, recompute points, refit),
2,000 resamples, seed 0. An asymptote counts as identified when A is inside (0, 1) in the point fit and in at least
75 % of resamples with dof >= 2.

**Files and recipe.** `INDOMAIN.md` (generated 10:43 with 10 resamples, says "no interval" throughout); `fit.json`
rewritten 11:59 with `--boot 2000`; `FIT_N.md` (15:48, `ssn:tools/indomain_fit_N.py`) is the interval-bearing
extract to quote. Reproduce (`INDOMAIN.md` §10):

```bash
python tools/indomain_fit.py --boot 2000 && python tools/indomain_fit_docs.py
python tools/indomain_fit_N.py            # FIT_N.md from fit.json
```

What the fits support for collection (`INDOMAIN.md` §8): about 12 patients (24 frames, both views) of the device for
detection; for whole-frame AP naming, 68 persons for 97 % (inside the measured range) and 1,071 for 99 % [X]; for
collimated fields, keep collecting and refit. The fits say nothing about transitional training persons (three real
L6 patients, no curve).

## A.7 The film N-curve (Figure 5b, film)

**Design** (`ssn:tools/film_ncurve.py` docstring; `sn:results/coverage/N_VS_COVERAGE_PLAN.md` part i). The C-arm
curve fine-tunes the v9 encoder, which never saw a C-arm frame. The v9 encoder has seen every film person of its train
split, so a film curve on it would not mean N. The film curve therefore uses a new **render-only encoder**: the v9
bank minus every film row (physics_drr, physics_rare, ctsp_drr, verse_drr; 47,976 train / 9,036 val crops), from
ImageNet, the v9 recipe (40 epochs, lr 3e-4, `--augment 2`); its own val exact accuracy 0.664
(`film_ncurve.json#encoder`, `#check/render_bank`). Each cell fine-tunes it on N film persons merged 1:1 with the
render bank's per-class-600 sample (15 epochs, lr 1e-4, `--augment 2`), then `head_mixed_length --train-mode mixed`.
Persons by `tools/patient_keys.key_any` (one CSXA film = one person; one four-digit BUU case = one person; NHANES by
film number). TEST = the v9 VAL persons of each corpus (never trained or selected on by any cell or the encoder);
SELECTION = a fixed draw of min(100, ceil(0.15 × pool)) train persons; POOL = the rest, nested per seed.
N = 0, 5, 10, 25, 50, 100, 200, all; seeds 0-2 at N <= 25, seed 0 above. Scoring: `tools/rigor_fixes.py a5-rows`
on one test context holding the v9 val films of all three corpora (random windows of 2-9 vertebrae and maximal
bands), which runs `tools/eval_gate.py` first; patient-clustered intervals. Every cell is "HELD OUT"
(`film_ncurve.json#cells/<cell>/heldout`).

**What it says** [M] (`sn:results/coverage/film_ncurve/FILM_NCURVE.md`, generated 2026-09-24 23:25, 48/48 cells):

| corpus | N = 0 | 5 | 10 | 25 | 50 | 100 | 200 | all |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NHANES II | 27.2 | 77.8 | 82.3 | 87.8 | 89.2 | 89.6 | 92.5 | 92.7 (264) |
| BUU-LSPINE | 10.3 | 65.0 | 70.3 | 76.7 | 81.2 | 82.7 | 85.1 | 96.9 (2,967) |
| CSXA | 3.2 | 94.2 | 93.0 | 96.4 | 97.3 | 97.3 | 98.0 | 99.8 (4,114) |

Cross-corpus transfer is poor: NHANES-trained peaks at 74.3 % on CSXA (N = 200) and 73.2 % on BUU (all); BUU-trained
reads CSXA at <= 12.6 %; CSXA-trained reads BUU at <= 12.6 % and NHANES at <= 43.7 % (`FILM_NCURVE.md`;
`PER_LEVEL_DOMAIN_ANGLE.md` Table B note). Pooled-fit asymptotes: NHANES 95.9 % (not reached: the all point is 3.2
points below), BUU 100 % (3.1 below), CSXA 100 % (reached) (`pooled_fit.json#admissibility`).

These N-curve endpoints (92.7 / 96.9 / 99.8) and the a5 film numbers (99.1 / 97.3 / 99.8) come from different
encoders on different splits; quote them as what they are, never side by side as one curve
(`PER_LEVEL_DOMAIN_ANGLE.md` Table D note).

**Jobs** (`sn:results/coverage/PENDING_JOBS.json#chains/film_ncurve`): fnprep 40437808 (`sn:slurm/film_ncurve_prep.sh`,
CPU, 150 GB) -> fnenc 40437809 (`film_ncurve_encoder.sh`, afterany) -> fncell 40437810 (`film_ncurve.sh`, array 0-47%16)
-> fncoll 40437811 (`film_ncurve_collect.sh`). Grid outputs under `RS/data/or_ready/film_ncurve/`
(`cells.json`, `manifest.txt`, `render_bank/`, `test_ctx/`, `pool_*/`, `base_cache/`, `cells/<cell>/`,
`film_ncurve.json`, `FILM_NCURVE.md`). The bank-merge rule is `ssn:tools/merge_banks.py`.

**Recipe** (the scripts' own headers):

```bash
cd ~/spinesurg-ct-nnunet
P=$(sbatch --parsable -D ~/spinesurg-ct-nnunet SchwingNet/slurm/film_ncurve_prep.sh)
E=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --dependency=afterany:$P SchwingNet/slurm/film_ncurve_encoder.sh)
C=$(sbatch --parsable -D ~/spinesurg-ct-nnunet --array=0-47%16 --dependency=afterany:$E SchwingNet/slurm/film_ncurve.sh)
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:$C SchwingNet/slurm/film_ncurve_collect.sh
# then copy RS/data/or_ready/film_ncurve/{film_ncurve.json,FILM_NCURVE.md,cells.json} to SchwingNet/results/coverage/film_ncurve/
```

Every step skips cells with a DONE marker, so rerunning the same command resumes (`PENDING_JOBS.json#rule`).

## A.8 The film N-curve ablation: do renders help? (in the manuscript's Discussion)

**Question** (Greg, 2026-09-25): "if renders are my only source of rare classes they have to be included right? run
this test" (`sn:REVISION_LOG3.md` §13). Renders stay in training regardless (the only labelled L6 / T13); the test
is whether they also raise ordinary-level film naming.

**Design** (`sn:slurm/film_ncurve_ablation.sh` header; `REVISION_LOG3.md` §13): the same 48 cells, persons, seeds,
epochs, head and scoring. Arm `renderonly` = the reported curve (render-only init + merged bank). Arm `imagenet` =
ImageNet init on the same merged bank (isolates the render pretraining). Arm `filmonly` = ImageNet init with every
render row removed (film rows keep their oversampled count); N = 0 skipped. **Rule stated before the numbers:** at
N = 5 and 25 per corpus, renders help if renderonly exceeds filmonly outside the patient-clustered intervals on every
seed; the largest N is the third verdict cell per corpus, nine cells in all.

**What it says** [M] (`sn:results/coverage/film_ncurve/ablation/READ.md`; Table B of `PER_LEVEL_DOMAIN_ANGLE.md`):

| corpus | N | render-only | ImageNet, same bank | film only | render − film | verdict |
|---|---:|---:|---:|---:|---:|---|
| NHANES | 5 / 25 / all | 77.8 / 87.8 / 92.7 | 75.5 / 83.0 / 92.3 | 55.9 / 75.6 / 92.0 | +21.9 / +12.2 / +0.7 | help / help / level |
| BUU | 5 / 25 / all | 65.0 / 76.7 / 96.9 | 60.0 / 73.7 / 97.2 | 53.9 / 70.7 / 98.5 | +11.1 / +6.0 / −1.6 | help / help / **hurt (separated)** |
| CSXA | 5 / 25 / all | 94.2 / 96.4 / 99.8 | 91.2 / 91.9 / 99.8 | 75.4 / 90.2 / 99.9 | +18.7 / +6.2 / −0.2 | help / help / level |

Seven of the nine verdict cells separated: six for renders, one against (BUU, all persons). At 50 persons NHANES and
CSXA still separate (+7.7, +2.9); from 100 persons nothing separates. At N = 0 the render-only floor is 27.2 / 10.3 /
3.2 %. Most of the scarce-N gain is the render rows; 2-5 points is the render pretraining (ImageNet arm in between).
Seeds: 3 at N <= 25, **1 above**, so the "not separated" cells and the BUU reversal rest on one run each.

**In the manuscript.** `sn:sections/discussion_motivation.tex` L53-56: "at five to twenty-five persons per corpus the
render-pretrained encoder named ordinary levels `\RESULT{abl_gap_min_pts}` to `\RESULT{abl_gap_max_pts}` points above
film alone, separated on every seed in `\RESULT{abl_cells_separated}` of `\RESULT{abl_cells_total}` cells; with every
person the arms met, one corpus `\RESULT{abl_worst_delta_abs_pts}` points the other way" = 6 to 22, 7 of 9, 1.6
(`sn:results/coverage/film_ncurve/ablation/ablation_read.json`). See Part E row 3 on how "7 of 9" reads there.

**Jobs.** imagenet array 40451157 (48/48 scored), filmonly array 40451158 (39/48 = every cell but N = 0), collects
40451159 / 40451160 (`REVISION_LOG3.md` §13; `sn:numbers_manifest.json` key `abl_gap_min_pts`). Reader
`sn:tools/film_ncurve_ablation_read.py` (generated `ablation_read.json` 2026-09-27 13:07).

**Recipe:**

```bash
sbatch -D ~/spinesurg-ct-nnunet --array=0-47%12 --export=ALL,ARM=imagenet SchwingNet/slurm/film_ncurve_ablation.sh
sbatch -D ~/spinesurg-ct-nnunet --array=0-47%12 --export=ALL,ARM=filmonly SchwingNet/slurm/film_ncurve_ablation.sh
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<array> --export=ALL,ARM=imagenet SchwingNet/slurm/film_ncurve_ablation_collect.sh
sbatch -D ~/spinesurg-ct-nnunet --dependency=afterany:<array> --export=ALL,ARM=filmonly SchwingNet/slurm/film_ncurve_ablation_collect.sh
# copy RS/data/or_ready/film_ncurve/ablation/<arm>/{film_ncurve.json,FILM_NCURVE.md} to SchwingNet/results/coverage/film_ncurve/ablation/<arm>/
python SchwingNet/tools/film_ncurve_ablation_read.py     # READ.md + ablation_read.json
```

Each arm is about 15 GPU-hours (the reported cells averaged 18 min) (`REVISION_LOG3.md` §13).

## A.9 Acquisition-space coverage (the census of where the frames sit)

`ssn:tools/acq_coverage.py` computes, per dimension (lateral angle 18 bins of 10°, tilt 6 × 10°, roll 12 × 5°,
magnification 16 × 0.05, field 8 × 50 mm, joint lat × tilt K = 108, patient position), coverage C = occupied /
clinically relevant bins and normalised entropy H* = −Σp log p / log K, for every corpus and every training list a
scored checkpoint read; for a training set H* is over epoch entries (`sn:results/coverage/COVERAGE.md` "Definitions").
The definitions come from an AI-generated review Greg uploaded (`sn:lit/acquisition_space_review_2026-09-24`), which
is not cited (`COVERAGE.md`; `mem:acquisition-space-saturation.md`). Checks recorded in `COVERAGE.md`: the C-ArmLSpine
header sign fitted on 301 registered spin frames (median residual 4.2°); COBRA gantry map exact on 8,418 poses; no
PatientPosition recorded on any spot or spin header; film corpora carry no positioner, SID or field tag, so their H*
is 0 by construction. Grid job acqcov 40437098 (COMPLETED 11:30 on 2026-09-24; `PENDING_JOBS.json`). Figures
`sn:results/coverage/fig_density.png`, `fig_density_training.png`. Rerun: `python tools/acq_coverage.py grid --out
<dir>` on the grid, then `python tools/acq_coverage.py report --coverage coverage.json` (`ssn:tools/acq_coverage.py`
L1202-1209). Open item: the `*_arc` and `*_low2` render geometries are not in its table yet
(`PENDING_JOBS.json#not_done_by_this_pass`).

## A.10 Matched-N coverage arms (Figure 5d)

**Design** (`ssn:tools/coverage_arms.py` docstring; `N_VS_COVERAGE_PLAN.md` part ii). Per device card (Surgio-B51,
Elekta XVI; Cios Fusion deferred, no card in the unseen sweep), three render-only detectors at the same N: `low` =
poses from the device's real AP/LAT pool (H*_lat 0.24 for Surgio), `high` = poses drawn from the arc pool only
(H*_lat 0.99), `low2n` = low plus N more real-pool frames (2N). Same subjects (142 clean minus the 40 unseen-sweep
subjects; 125 train), same card, same trainer, seeds 0-1. Scored on the unseen angle sweep (40 TotalSegmentator
subjects, 19 lateral bins), the real case134 spin, and every real test split.

**What it says** (`power.json#panel_d_angle/summary`; `EXPERIMENT.md`) [M on renders]:

| arm (Surgio card) | N train | trained-angle bins | 16 untrained bins | all bins | real C-ArmLSpine test (vert recall) |
|---|---:|---:|---:|---:|---|
| low | 2,646 | 82.1 % | 52.8 % | 57.4 % | 4.9 / 9.1 % (s0 / s1) |
| low2n | 5,290 | 94.2 % | 64.8 % | 69.5 % | 1.4 / 2.4 % |
| high | 2,646 | 80.7 % | 77.1 % | 77.7 % | 0.7 / 1.0 % |

Elekta XVI arms score zero on every bin and on the real test. Caveat that travels with panel d: the Surgio card renders
thick laterals photon-starved, so the ±90° bins conflate geometry with synthetic underexposure
(`power.json#panel_d_angle/exposure_caveat`). The same render-only arms on the REAL device test read 0.7-9.1 %
whatever the coverage (`PER_LEVEL_DOMAIN_ANGLE.md` Table G).

**Jobs** (`PENDING_JOBS.json#chains/coverage_arms`): covrender 40437812 (array 0-3), covarm 40437813 (array 0-11,
`sn:slurm/coverage_arms_manifest.txt`), covcoll 40437814; then covscore 40443105 (score only) and covcoll2 40443106
(overwrites). Runs `~/spine-detector/runs/coverage/<arm>/`; collected `RS/data/or_ready/coverage/experiment/`;
local mirror `sn:results/coverage/experiment/runs/`.

**Recipe:** `sbatch SchwingNet/slurm/coverage_arms_render.sh` (array 0-3) -> `coverage_arms_train.sh` (array 0-11,
afterany) -> `coverage_arms_collect.sh`; rescoring without training is `coverage_arms_score.sh` + collect
(`PENDING_JOBS.json`). Exact sbatch lines with flags are not written in the PENDING file beyond script and array.

## A.11 The pooled nested fit: N alone, or N plus coverage

`ssn:tools/indomain_fit_coverage.py --film ...` (local, 2026-09-25 10:02) pools 105 points (film N-curve cells H* = 0;
C-arm naming cells, H* fixed per protocol; same-device detection cells; the matched-N arms) and compares
M0: acc = A_c − B_c N^−C (one exponent, per-corpus A, B) against M1: M0 + g·H*_lat
(`sn:results/coverage/POOLED_FIT.md`; `pooled_fit.json`).

**What it says** (`pooled_fit.json#comparison`): ΔAICc(M0 − M1) = +26.0; LR = 29.1, p = 6.7e-8; g = +20.0 points per
unit H*_lat [+12.2, +27.7]. Verdict: "N plus coverage", **but g is identified only by the two render-arm corpora**
(the only ones whose H* varies within corpus). Sensitivities: at confidence 0.74 the arms reverse it (ΔAICc −3.1,
p = 0.82, g −0.7 [−8.8, +7.4]); arms restricted to trained ones: ΔAICc +32.0, g +24.2
(`sn:results/coverage/sensitivity/`). The manuscript quotes it as "preferred count plus lateral-angle coverage at
confidence 0.25 ... not at 0.74" (`sn:sections/results.tex` L123-125). Not drawn since the 2026-09-25 afternoon build
(`power.json#pooled_fit/note`).

**Recipe** (inputs as recorded in `pooled_fit.json#inputs`):

```bash
python tools/indomain_fit_coverage.py --census SchwingNet/results/coverage/coverage.json \
  --experiment SchwingNet/results/coverage/experiment/scores.json \
  --film SchwingNet/results/coverage/film_ncurve/film_ncurve.json          # writes pooled_fit.json (+ fit/coverage_fit.json)
python tools/indomain_fit_coverage.py ... --arm-conf 0.74 --pooled-out SchwingNet/results/coverage/sensitivity/pooled_fit_conf074.json
```

The exact flag that produced `pooled_fit_trained_only.json` is not recorded.

## A.12 Film against fluoroscopy, pooled against view-separated (dimension exploration)

`sn:tools/fig_dimension_explore.py` (nothing retrained) -> `sn:results/coverage/dimension/film_vs_fluoro_dimension.
{json,png}`; then folded into Figure 5 by `fig_power.py` (`mem:acquisition-space-saturation.md`; `REVISION_LOG3.md`
§10). The claim the paper makes: accuracy follows where the frames sit in acquisition space, frames of one cell do
not transfer to another. **Not claimed:** that fluoroscopy is higher-dimensional than film, because no film corpus
records a projection angle, distance or magnification (`sn:results/coverage/DICOM_VARIABLES.md`, map not built) and
film has its own non-transferring dimension, corpus (NHANES -> CSXA 74 % at best) (`mem:acquisition-space-saturation.md`).

## A.13 See A.4 (the plateau is the denominator).

## A.14 The contribution matrix (which source carries held-out detection)

`sn:tools/contribution_matrix.py` recomputes every cell from per-frame raw predictions (`realxray_eval.py --dump-raw`)
at one operating point (conf 0.25, IoU 0.5), case-cluster bootstrap 2,000; C-ArmLSpine under the outline convention
with body beside it (docstring; `sn:results/contribution_matrix.md`, self-check 85 cells, max difference 0.0000).
Sections: held-out cells, in-training cells, marginal contribution of each source, named paired comparisons, design B
minus A, seed spread, single-source cells and covariates. Key readings in `PER_LEVEL_DOMAIN_ANGLE.md` Table G: renders
plus other devices' real frames (design B) HURT on the C-arm at 0.74 (63.1 [54.8, 71.0] against real-only 80.5
[74.1, 86.8]) and HELP on the Elekta kV imager (32.7 against 18.5 at 0.25). Figure S3 (`sn:figures/figS3.*`,
`sn:tools/fig5_contribution.py`). Rerun: `sn:slurm/contrib_matrix_cpu.sh` (CPU; "rerun this whenever a new arm lands").

## A.15 The LSTV flag learning curve (AUC against positive patients)

`ssn:tools/lstv_flag_learning_curve.py`: one fixed held-out split; the training positives subsampled to 10, 20, 40,
80 and all, five draws per point, negatives held constant; AUC within each cohort, never pooled (the two cohorts sit at
4 % and 46 % positive). Plot and table `ssn:tools/lstv_flag_curve_plot.py` -> `~/lstv_flag/LEARNING_CURVE.md` (grid).
Result as quoted in `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` L659 (assembled 2026-09-16) [M]: VerSe held-out
(67 patients, 31 positive): 10 positives 0.652, 20 0.688, 40 0.704, 80 0.685, 120 0.713; "tripling the positives
bought under 0.01 AUC". The run date and job id are not recorded locally.

## A.16 The D1 head data saturation (paper 2)

`sn:tools/d1_saturation.py` reads `tools/head_dual.py` outputs: accuracy against epochs (three seeds) and against
fraction of training persons (1/16 to 1 of 8,950), plus the bank's coverage census
(`sn:results/dual_loss/saturation.json#status`: "development numbers on the G3 bank's validation side ...; no test
person"). [M-dev] random-window overall: 0.687-0.692 at 563 persons, 0.700-0.722 at 1,121, 0.717-0.723 at 2,240,
0.729-0.739 at 4,477, 0.736-0.746 at 8,950; real film 0.981-0.988 throughout (`saturation_curve.csv`). Jobs:
d1lcurve array 40436887 (`sn:results/dual_loss/d1lcurve_40436887_*.out`), d1cover 40436997. This head belongs to the
paper-2 LevelCheck model (`sn:LEVELCHECK_MODEL.md` §12).

## A.17 The nnU-Net ablation array (`docs/ablations.md`)

Six ablations of the CTSpinoPelvic1K segmentation model (fused_only 803, no_partial 804, no_lstv_oversample, short
100 epochs, ResEnc L, fused-only test 805), submitted by `ssn:slurm/spine_ablation.sh` (`make ablate`), aggregated by
`ssn:tools/compare_ablations.py` (`make compare-ablations`) into `tables/ablations.tex`. No `tables/` directory exists
locally; the grid holds an `ablate` folder of 234.8 GB (`mem:grid-quota-and-deleted-banks.md`). Whether the array ran
to completion and what it found is not recorded on the laptop. It is not a scaling plot; it is listed because the
task named the file.

## A.18 The per-level, per-domain, per-angle manifest (grid commit 4e3fe938 = local 4e3fe93)

`sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` (commit 4e3fe93, 2026-09-27 17:12, present in this checkout) answers
Greg's question of 2026-09-27 ("How does it do at each level, in each domain and angle in fluoro, plain film, various
ratios of synthetic CT / real film, does it ever help ... Manifest"). Every number names its file and JSON pointer
and is marked held out, selection-split, or DERIVED. Its six-sentence answer, shortened:

1. **Per level, real C-arm** [M] (`sn:results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:cv5_det`, case-grouped
   five-fold, v9 lineage): L1-L5 name at 96.8-98.5 % on whole lateral frames, 95.5-97.7 % on whole AP; the one-body
   field separates them (L1 41.2 % LAT / 9.5 % AP; L4-L5 84-86 %). Zero-shot AP is a one-level cranial shift
   (L4→L3 ×51, L3→L2 ×51 ...), which fine-tuning removes. Not printed in any manuscript table (Table C).
2. **Per level, plain film** [D on M-sel]: from `sn:results/a5_rows.csv` (v8 encoder, selection split): lumbar
   96.4-98.4 % on BUU, 97.4-100 % on NHANES, cervical 99.7-100 % on CSXA; renders floor at T7 (55-59 %), L6 20-42 %,
   T13 0/9. Must be re-run on held-out persons by a committed tool before quoting (Table E).
3. **Per domain** (Table D): film 97.3-99.8 % [M-sel] / 92.7-99.8 % [M]; renders 45-94 % by source; real fluoroscopy
   zero-shot LAT 96.4 % (595/617) vs AP 43.7 % (276/631), fine-tuned 97.4 / 96.4 %, day-grouped 92.1 / 94.8 %.
   VinDr, FluoroCap, DeepFluoro, COBRA, Geneva, Ljubljana are not scored for naming.
4. **Per angle:** naming per angle does not exist. Detection per angle exists on three surfaces: one real 301-frame
   spin (case134; pooled 93.6 % @0.25; the reported held-out detector a flat 49.5 %, recorded as unexplained in
   `sn:figures/figS4.record.json`), the 40-subject render arc (A.10), COBRA gantry bands (Table F).
5. **Synthetic:real ratio: never swept.** `ssn:tools/merge_banks.py` L60 fixes `real_share = 0.5`,
   k = round(real_share/(1 − real_share) × 15,374 / n_crops), so every film cell is about 1:1 by rows (render rows
   15,374 in every cell) while the distinct-image ratio runs from 615:1 (BUU/CSXA N = 5) to 0.75:1 (CSXA all)
   (Table A). What was swept is N persons at fixed ratio.
6. **Do renders ever help?** Film naming: yes while scarce (A.8). C-arm naming: renders never substitute for
   in-domain persons (AP 26.2 -> 53.7 % vs in-domain 90.8 -> 98.1 %). Detection: hurt on the C-arm, help on the kV
   imager (A.14). Table G lists every measured instance, including the superseded 2026-09-17 level-model arms.

Its "What is not known" table, with what closes each: per-angle naming (a human level read on the case134 spin, or a
second labelled spin); per-level film on held-out persons (a committed aggregation tool); **the ratio sweep (one array:
real_share ∈ {0.1, 0.25, 0.5, 0.75, 0.9} at N = 25 and N = all, three seeds, about 45 cells × 15 epochs)**; seeds
1-2 at N = 50-all (18 cells × 2 arms); rare-class accuracy on anything real (the transitional review tree); naming
beyond one device. Two outputs for a doctor were proposed and neither is done: supplement Table S5 "Per level" from
`cv_v9.json` through `\RESULT` keys, and a one-page read of Tables C and G for Dr Tech. Both wait on Greg's decision
(`PER_LEVEL_DOMAIN_ANGLE.md` "Getting it in front of a doctor"; `ssn:docs/RESUME_2026-09-22_PM.md` L35-37 "FOR GREG":
per-level S5 yes/no, ratio sweep and seeds above N = 25 yes/no).

## A.19 What the literature says about the ratio (context for A.18 item 5)

`ssn:reports/Synthetic real ratio X-ray detectors.md` (deep research, 119 citations, 2026-09-23;
`mem:synthetic-real-ratio-evidence.md`): no DRR paper has swept the synthetic-to-real ratio or the real-frame count;
adjacent fields flatten at 4:1-10:1 (real 10-20 % of the mix); in pretrain-then-fine-tune the ratio stops mattering;
VerSe made L6 learnable at 85 distinct scans while T13 with 6 never stabilised; report rare recall with PR-AUC and
common-class precision. The experiment this project could be first to publish: a real-frame learning curve per device
(50/100/200/400) with the transitional class scored separately, and distinct CTs varied against renders per CT
(`mem:synthetic-real-ratio-evidence.md`). The in-house numbers that touch it: A1 [S], A3, A8. Barr 2026's de novo
n = 700 value is flagged in the report for checking before quoting (same note).

## A.20 Figure 5: how it is built, end to end

Inputs (each hashed into `power.json`): `film_ncurve.json` (sha256 5922dbdf...), `name_fill.json` (35b8ad7e...),
`det_fill.json` (af0357ae...), `pooled_fit.json` (a60c0a10...), the arms' `recall_vs_angle.json`
(`sn:results/power/power.json#panel_*/inputs`). Build chain (`sn:RESULTS_BUILD.md`):

```bash
python SchwingNet/tools/fig_power.py          # figures/figure5.{pdf,png,tif}, figure5.record.json, results/power/power.json
python SchwingNet/tools/results_macros.py --check   # exits 1 on any pending key, unused key, or bare result numeral
python SchwingNet/tools/check_limits.py
bash SchwingNet/slurm/compile.sh              # runs the generator, then latexmk -> main.pdf, supplement.pdf
```

Journal rules applied by `fig_power.py` (docstring): four components a-d, Arial >= 12 pt at 7.0 in, TIF at 1,200 dpi
LZW, Okabe-Ito palette validated 2026-09-25. Caption `sn:figures/figure5.caption.txt` (58 words, `sn:main.tex` L210).

---

# Part B. The anomaly scan (transitional anatomy harvest and the ruleclass SUPER DETECTOR RUN)

## B.0 Timeline

| date | event | file |
|---|---|---|
| 2026-07-04 | first entry in the CTSP LSTV re-read queue (volume 0172, five sacral foramina on a "normal") | `ctsp:docs/lstv_reread_queue.csv`; `mem:lstv-reread-queue.md` |
| 2026-08-02 | two findings: LCC post-processing deletes the loose lamina of spondylolytic vertebrae; thoracolumbar and lumbosacral anomalies co-occur | `mem:spondylolysis-and-border-anomaly-findings.md` |
| 2026-09-12 | L6 pseudo-Dice 0.000 for 27+ epochs under 12× duplication (Dataset813); counting decoder finds 6/6 L6 on 4-class truth; Dataset815 raises L6 cases 18 -> 62 | `mem:l6-sample-count-and-counting-decoder.md` |
| 2026-09-15 | VerSe variant table (Löffler 2021 Suppl. Table 1) verified against masks; VerSeFusion `has_T13` = 18 found wrong (truth 6); `TRANSITIONAL_LABELS.csv` 4,245 rows | `mem:lstv-data-landscape.md`; `mem:versefusion-t13-flag-wrong.md` |
| ≤ 2026-09-16 | LSTV flag learning curve (A.15) | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` L659 |
| 2026-09-17 | anomaly manifest: 749 anomalous spines in three trust tiers | `mem:anomaly-manifest-sources.md`; `ssn:tools/anomaly_manifest.py` |
| 2026-09-22 | R + C = 22 rule evaluated and removed from the manuscript | `ssn:docs/ANOMALY_RULE_EVALUATION.md`; `mem:anomaly-rule-rc22-evaluated.md` |
| 2026-09-23 | anomalous inventory (job 40416205); transitional subtypes table; G3 split; harvest directive "scrape the bottom of the barrel"; acquisition plan and tier-1 fetches start | `sn:results/anomalous_inventory.md`; `sn:results/rare_class/transitional_subtypes.md`, `split_plan.md`; `mem:anomaly-harvest-directive.md`; `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| 2026-09-24 | five harvest streams written; the one registry built 11:07; MAXIMIZE render pass 16:55; NLST T13 rule added | `sn:results/transitional_registry/REGISTRY.md`, `maximize/MAXIMIZE.md`; `ACQUISITION_PLAN.md` §11 |
| 2026-09-25 | census table of every collection with expected transitional people and storage | `ssn:docs/CENSUS_TABLE_2026-09-25.md` |
| 2026-09-26/27 | classifier catalogue R1-R37; ruleclass tier lists; arms A (TotalSegmentator), B (Möller ribs on SPINEPS+VERIDAH), pelvis (Dataset803) running; every other grid job recorded and cancelled | `ssn:docs/ruleclass/`; `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; `mem:ruleclass-super-detector-run.md` |
| 2026-09-27 16:47 | `PREREG_rules.md` DRAFT v1 committed (f15da62); review-tree code written 16:57-18:11, untracked | `ssn:docs/ruleclass/PREREG_rules.md`; `ssn:tools/transitional_review/` |

## B.1 Definitions that every number below depends on

- **A call needs a count; a count needs both junction references in the field.** L6 / four-lumbar / sacralised L5
  need the lowest rib-bearing vertebra and the sacrum; T13 needs the rib cage counted from T1. A CT that cannot count
  is `no_count`, never ordinary (`mem:anomaly-harvest-directive.md`; `ACQUISITION_PLAN.md` §1; `REGISTRY.md`
  "Denominators and refusals").
- **Truth tiers** (registry order): read > two-labeller > single-labeller > morphology-only > none. Only `read`
  (CTSP two-reader Castellvi consensus and read levels; the VerSe published table; three CTSpine1K list entries) is
  truth; `two-labeller` means two models that fail differently agreed (`REGISTRY.md` "What is not known";
  `ssn:docs/ruleclass/CLASSIFIERS.md` §0). Human reads exist only on CTSP (33 records) and VerSe (325 subjects), plus
  70 externally labelled TotalSegmentator CTs (L6/T13 only).
- **Labeller A** = SPINEPS + VERIDAH names bound to instances through the ctd centroid file (never by mask id);
  **labeller B** = TotalSegmentator geometry (rib-head contact, 38 mm stump rule); reader C = direct CT rib count
  (`CLASSIFIERS.md` R9-R11).
- **Real-frame persons are TEST only**: COBRA, C-ArmLSpine, DeepFluoro, Geneva, SpineSAC, Ljubljana people are never
  rendered for training (`REGISTRY.md`; `MAXIMIZE.md` "The rule applied").
- **Label maps**: VerSe raw masks L6 = 25, T13 = 28; CTSP v11 L6 = 25, sacrum 26, id 29 retired; legacy ostk map
  differs; resolve through `ostk.labels.labels_for` for CTSP / Dataset803 outputs only
  (`sn:results/rare_class/transitional_subtypes.md`; `ssn:docs/ruleclass/PREREG_rules.md` §0).

## B.2 Stage by stage

### B.2.1 The anomaly manifest (2026-09-17)

`ssn:tools/anomaly_manifest.py` -> `~/model_night/anomaly_manifest/{anomaly_manifest.csv, spine_classes.json,
summary.json}` (grid). 749 anomalous spines: tier A certain 355 (VerSe 163, BUU 144 real films, CTSP 48); tier B
pseudolabel 211 (VinDr 209, LAT236 2, all on frames without the junction); tier C FluoroCap captions 183. Four-class
over 1,113 CT spines: 902 ordinary / 98 LS-only / 47 TL-only / 66 both. Co-occurrence odds ratio VerSe 4.30 [2.59,
7.14], CTSP 4.00 [1.00, 16.03]; the pooled 12.8 is Simpson's paradox, never quote it. The count was once 34/16/2
because only the 802-record CTSP manifest was read; the master is `~/lstv_flag/lstv_flag_labels_v2.csv`
(`mem:anomaly-manifest-sources.md`). The adversarial audit later found the co-occurrence inflated by count-coupling;
VerSe 280 fully graded gives 3.61 [2.08, 6.27] (`mem:feasibility-claims-measured.md`). BUU anomaly labels live in
`KIOM2022_dataset_report.xlsx` sheet `L4L6` (129 L4, 15 L6), and 9 of the 15 "L6" are children
(`mem:anomaly-manifest-sources.md`; `mem:feasibility-claims-measured.md`). Rerun:
`python tools/anomaly_manifest.py --out ~/model_night/anomaly_manifest` (docstring). Consumers read `spine_classes.json`
via `--classes` (`ssn:slurm/count_*.sh`, `benchmark_cina.sh`); check the log line "per-case classes from:".

### B.2.2 The anomalous inventory and the subtype table (2026-09-23)

`ssn:tools/anomalous_inventory.py` (job 40416205) -> `sn:results/anomalous_inventory.{json,md}`: VerSe 56 (L6 50,
T13 6), CTSP 18 L6, TotalSegmentator 4 (3 L6, 1 T13; the verified subset of 12 once selected by "SPINEPS id 25
present" on raw-id masks, 8 of which are normal), C-ArmLSpine real 3 L6.
`ssn:tools/transitional_subtypes.py` -> `sn:results/rare_class/transitional_subtypes.{csv,json,md}`: 196 rows, 194
persons (L6 110, T13 7, Castellvi I-II 31, lumbar rib 14, sacralised L5 28, unassigned 4); both L6 and T13: zero in
every source. The fused-L5 representation matters: 9 CTSP cases merge the fused body into the sacrum label (the
detector can only see one body), 3 keep their own id 24.

### B.2.3 The G3 split of transitional people (2026-09-23)

`tools/make_split.py` -> `sn:results/rare_class/split_plan.md` (leak audit PASS). Transitional CT people 50/10/40 by
exact allocation within subtype (194 >= 150, so the small-inventory 50 % rule does not apply); real transitional
subjects all in test; everyone else by `sha256('g3|<seed>|<key>')`. Per side: L6 107 people (53/11/43), T13 7
(3/1/3), sacralised L5 28 (14/3/11), Castellvi I-II 31 (16/3/12), lumbar rib 14 (7/1/6). **49 of 54 L6 val+test
people are in the v8 or v9 training lineage**, so for a model descending from those banks they are not evidence. COBRA
screen calls (unverified): 91 (L6 38, T13 45, four-lumbar 8). Rerun:
`sbatch -D $HOME/spinesurg-ct-nnunet --export=ALL,STAGE=all SchwingNet/slurm/g3_split.sh`.

### B.2.4 The five harvest streams (2026-09-23/24)

Workflow anomaly-harvest wf_babed05b-84a writes `sn:results/transitional_registry/<stream>/` (one row per CT in a
shared schema) (`mem:anomaly-harvest-directive.md`):

| stream | tools | rows | what it found (registry table B) | outside check |
|---|---|---:|---|---|
| verse | `ssn:tools/harvest_verse_census.py` (voxel census, three labellings), `harvest_verse_registry.py` (joins the published table), `harvest_verse_render.py` (review MIPs); `ssn:slurm/harvest_verse_*.sh` | 374 series, 355 persons | L6 85, T13 6, sacralised 13, Castellvi I/II 27, lumbar rib 12, unassigned 23 | the published read itself; `verse/labeller_checks.json` |
| ctsp | `ssn:tools/ctsp_registry_census.py`, `ctsp_registry_ts.py`, `ctsp_registry_build.py` (three labellers on the release's student-reviewed ribs) | 64 positive rows (negatives on the grid) | L6 29 (17 read, 11 two-labeller, 1 single), sacralised 12, Castellvi I/II 4, lumbar rib 14, unassigned 5 | reader truth (`ctsp/SUMMARY.md`, `findings.md`) |
| totalsegmentator | `ssn:tools/ts_transitional_screen.py`, `ts_transitional_registry.py`, `transitional_ts_count.py` | 1,935 v300 keys | L6 22, T13 4, unassigned 26, unresolved 74 | `totalsegmentator/ctsp_validation.json` |
| cobra | `ssn:tools/harvest_cobra.py`, `harvest_cobra_validation.py`, `harvest_validate_a_ctsp.py`, `harvest_validate_b_score.py`; `ssn:tools/cobra_lstv_screen.py` (labeller A) | 692 | L6 3, unassigned 6, unresolved 11 (all TEST only) | `cobra/labeller_validation_ctsp.md` |
| other_ct | CTSpine1K, RibFrac, RSNA C-spine; `ssn:tools/other_ct_fetch.py` | 3,066 | CTSpine1K L6 3, sacralised 2; RibFrac T13 4, L6 1 | `other_ct/validation_summary.json` |

### B.2.5 The one registry (2026-09-24 11:07)

`ssn:tools/transitional_registry.py` -> `registry.csv` / `registry.json` / `REGISTRY.md`. 6,131 rows -> 6,108 persons
(5 phantoms kept as rows, not people); 782 alias edges (CTSpine1K COLONOG volume -> CTSP record), 56 written on a
registry person. Persons per subtype (table A): **L6 146** (read 103, two-labeller 29, single 10, morphology-only 4;
6 of them real-frame TEST), **T13 14** (read 6, two-labeller 3, single 5), sacralised L5 27, Castellvi I-II 31,
lumbar rib 26, unassigned 62, unresolved 129, none 1,686, no_count 3,987. Before/after against the subtype table: L6
110 -> 146 (106 kept, 3 dropped, 40 new), T13 7 -> 14. Review queues for Greg: verse 71, ctsp 72, totalsegmentator 137,
cobra 79, other_ct 87 (+103 labeller-validation), all rendered, **`greg_verdict` filled on 0**; contact sheets in
`sn:results/transitional_registry/contact_sheets/` (`REGISTRY.md` "Review queues"). The acquisition screens are not in
the registry ("no rows.csv: not a row stream"); they live in each collection's `rows.csv` on Ceph and enter the
ruleclass tiers as flag source R20 (`ssn:data_platform/DATA_MANIFEST.md` L3690-3695).

### B.2.6 MAXIMIZE: rendering every registry person the recipe allows (2026-09-24 16:55)

`ssn:tools/rare_class_maximize.py` -> `sn:results/transitional_registry/maximize/MAXIMIZE.md`. Rule: CT-only persons
at `read` or `two-labeller`, one CT per person, 70 distinct frames per CT (lateral ×3, AP ×3, arc obliques ×4, six
device cards plus raw bone DRR); an ID guard holds any case whose mask lacks the ids its call names. Totals: rendered
before 87; planned 165, rendered 109, held by the ID guard 54, stopped 2; waiting (adjudication first) 39; real-frame
TEST 13; unavailable 2. Rendered transitional CTs now: 196. Jobs `maximize/jobs.json`; scripts
`sn:slurm/rare_max_{stage,verse,verify}.sh`.

### B.2.7 The acquisition plan and the two-labeller screens of public CT (2026-09-23 to 09-25)

`sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` (623 lines) answers "any CT on the internet could be
segmented" with a rule: E = Σ over new people [P(both LS references | coverage) × p_LSTV + P(cage from T1) × p_T13]
[E], priors in `ssn:tools/acquisition_census.py` L17-26 (p_LSTV 0.09-0.18, Hanhivaara 2020 / Nardo 2012; p_count
0.048 = L6 3.2 % + four-lumbar 1.6 %, Sun 2025; p_T13 0.0064-0.020), P(countable) measured on TotalSegmentator
study types (job 40425064, `fov_calibration.json`). **Stopping rule stated before any fetch** (§3): no collection
below 20 expected transitional people per TB; no fetch with under 5 TB free; 8 TB cap; measure tier 1 before
committing tier 2; nothing beyond tier 1 while > 5,000 fetched CTs are unscreened. Tier 1: 45 routes + NLST pilot,
15,233 CTs, E_low / E_high 831 / 1,703, E_count 460 [E]. Chain per collection: `ssn:slurm/acquisition_submit.sh
<target>` -> fetch -> convert -> cases -> ts -> gate -> spineps -> call -> summary, `afterany`, resumable
(`ssn:data_platform/DATA_MANIFEST.md` L3654-3660). **The NLST pilot's 9.3 % T13 was wrong but plausible** (34 of 367,
all from labeller A alone, five to fifteen times the prior); checked outside the computation (jobs 40436876/77,
`tools/acquisition_t13_check.py`), it fell to 1.5 % once a rib on the named body was required, and that rule
(`acquisition_screen.confirm_t13_by_rib`) now runs at every `call` stage (§11).

### B.2.8 The census table (2026-09-25)

`ssn:docs/CENSUS_TABLE_2026-09-25.md` (generator `ssn:tools/census_table_2026-09-25.py`). Section 1, 18 collections
being screened: 18,873 listed, 16,898 on disk, 12,123 passing the field gate; expected L6 322, four-lumbar 161,
Castellvi II-IV 907-1,813, T13 38-119 [E]; called so far L6 two-labeller 21, single 18; T13 single 16; review 84;
843 GPU-hours spent. Section 2, tier 2 (chest-dominated, T13 only): 29,479 CTs, 2.9 TB; NLST alone 2.3 TB for about
110 T13 people, refused by the stopping rule. Section 3, gated (no form signed): Merlin (Stanford AIMI) alone expects
about 447 L6 and 224 four-lumbar [E], more than the whole open tier 1. Section 4, storage: 4,482 GB used of 20 TB on
2026-09-25; everything in the census would be about 15.5 TB. Caveats: on the 70 externally labelled validation CTs,
labeller A found 12 of 28 L6, B 17 of 28, both 9 ("halve it for what the current two-labeller rule will confirm
without a human"). See Part E row 6 on an off-by-one in its counts.

### B.2.9 The ruleclass SUPER DETECTOR RUN (2026-09-26/27)

**What it is** (`mem:ruleclass-super-detector-run.md`; `ssn:docs/ruleclass/README.md`, `TIERS.md`): the segmentation
base of the transitional review tree, at `RS/ruleclass/` (grid docs `CORPUS.md`, `tiers/TIERS.md`, `ARM_B.md`,
`arms/ts/ARM_A.md` + `STATUS.md`). Greg's determination (2026-09-26 23:50): two arms. **Arm A** = TotalSegmentator
2.18.0 `total` full resolution -> `arms/ts/<collection>/`. **Arm B** = SPINEPS + VERIDAH (existing) + Möller rib
nnU-Net (Zenodo 14864106, folds 0-2, through SPINEPS' wrapper; `arms/moller_fast/` for the corpus pass, `arms/moller/`
full config, 20-25× slower) + Greg's Dataset803 ensemble for the **pelvis only** (sacrum + hips) as the caudal
anchor -> `arms/pelvis/` (`ssn:docs/RESUME_2026-09-22_PM.md` L167, L197; "My model is essentially shit at everything
except the pelvis"). Environment `~/mambaforge/envs/spineps` (spineps 2.1.1, TPTBox 0.8.2, torch 2.6.0+cu124); the
Blackwell nodes ymh3/ymh4 cannot run it.

**Tier lists** (`ssn:docs/ruleclass/TIERS.md`, built 2026-09-27 00:20-00:40 by `tiers/build_tiers.py`, file listing
only): **21,622 CTs** (21,603 persons). Tier 1 5,094 CTs = CTSP 802 + TotalSegmentator-benchmark natives 1,602
(TS 1,228 + VerSe 374) + COBRA 692 + every other CT whose person carries a registry or screen flag (1,997) or another
classifier's positive (1). Tier 2 12,217 = every other CT with a SPINEPS mask. Untiered 4,311 (gate-refused, PANORAMA
pending 1,114, 210 TS scans where SPINEPS failed). Flags already in tier 1: L6 148 (registry R13) + 303 (acquisition
screens R20), T13 14 + 82, unresolved 129, review 1,168; 1,052 tier-1 CTs carry a positive-subtype flag, 1,285 only
review/unresolved (kept on purpose). Real frames: tier 1 696 (COBRA 692, C-ArmLSpine 4), tier 2 154. Children: 114 in
tier 1, 442 in tier 2. Both junctions in field: 2,951 tier 1, 8,050 tier 2. Raw-id SPINEPS masks: 108 tier 1, 422 tier
2 (read only through `tools/spineps_ids.relabel_by_ctd`). Estimated new output about 40 GB. Rebuild: `RS/ruleclass/code/
probe_t2.sh`, `probe_t3.sh` (listing) -> `build_tiers.py` -> `check_paths.sh` (0 missing) (`TIERS.md` §7).

**The classifier catalogue** (`ssn:docs/ruleclass/CLASSIFIERS.md`, 1,284 lines, built 2026-09-26 by
`build_classifiers_table.py`): every transitional classifier or label tried, R1-R37, joined per person in
`classifiers_by_person.csv` (22,173 rows × 226 columns, grid/scratch). Highlights from its §0: the consolidated truth
table is `labels_j3.csv` (R33, 321 read persons); rule 1's second step already ran on CTSP (R30: 18 six-lumbar spines
split A 11 / C 4 / B 1 / B-or-C 2); T13 against L6 on 25-presacral spines is a naming split between VERIDAH, the
VerSeFusion audit, TS v3's L6 class and the VerSe read, to be reported, not averaged; the Möller-mask stump flag is
65.7 % sensitive (R27) and the foramina counter fails on normals (R31); Dataset803 had no `results/` tree on the grid at
00:04 and had to be pulled from HF `OpenSpineConsortium/spinopelvic-seg-checkpoints` (R36). The other rescued design
documents: `STUMP_RULE.md` (stump / lowest-rib ratio rule, Wigh 1980, Möller 2026, Nagata 2025, calibration C0-C8),
`MORPH_API.md` (SPINEPS-subregion morphology, Schinz 2026 T-vs-L shape), `ARM_B_pelvis.md` (TTA decision rule; sacral
anchor fraction f < 0.10 free, 0.10-0.50 contact, >= 0.50 absorbed; iliac-crest cue).

**Grid jobs on 2026-09-27** (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`): armA_timing 40481415, armA_ts_t1
40481416 and collects; armb tier arrays 40481657/65 (tesla), 40481725 (t1f_gpu), 40481727/43-48 (MIG), 40481728 (H200),
measure arrays 40481749-69, sweeps 40481775/76; pelvis_timing 40481679, pelvis_arr 40481574, pelvis_agree 40481575,
pelvis_summary 40481573; `armb_t1pos_full` 40481738 (400-1,700 GPU-h fidelity pass) left held. Acceleration at 16:39:
arm-B predict arrays A30 40485812, A30-MIG 40485813, V100 40485814, arm A tier 2 CPU 40485815 + collects 40485887-89,
pelvis_timing copy 40485890 (cancel 40481679 only after `arms/pelvis/_timing/DECISION.json` exists)
(`ssn:docs/RESUME_2026-09-22_PM.md` L63-68). State at 17:00: 228 running, 315 pending; Möller fast 1,801 of 5,094 tier-1
CTs, pelvis 0, total_v3 0 (`RESUME_2026-09-22_PM.md` L29, L55). **What the arms finished after 2026-09-27 is not
recorded on the laptop.**

### B.2.10 The four-rule pre-registration (`PREREG_rules.md`, DRAFT v1, not frozen)

`ssn:docs/ruleclass/PREREG_rules.md` (commit f15da62, 2026-09-27 16:47). Status line: "awaiting Greg's sign-off. Not
frozen. Until the freeze line at the end is filled, every number this document produces is calibration, not a result."
- **Rule 1, rib-free lumbar count**: free presacral bodies between the lowest rib-bearing vertebra (a Möller rib
  > 38.0 mm on at least one side) and the cranial end of the Dataset803 sacrum (TS sacrum ∪ S1 until Dataset803
  exists); per-body sacral fraction f; `no_anchor` when the sacrum is absent, < 5 mL, at the caudal edge, or the two
  anchors differ by > 20 mm. Output count ∈ {4, 5, 6, no_count}.
- **Rule 1b**: shape of the sixth rib-free body (facet angle, costal-process offset, process shape; logistic model on
  named T12/L1, P(thoracic) >= 0.80 thoracic, <= 0.20 lumbar, between = TLTV). Not yet built on SPINEPS masks.
- **Rule 2, pelvis and sacral morphology**: features against the central 95 % of a reference half of adults with an
  agreed count of five; **no validated threshold yet; gates nothing until the reference-half freeze**. Every earlier
  pelvic cue on CTSP was falsified or weak (ala rise AUC 0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599;
  `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md`).
- **Rule 3, stump rib**: STUMP if the lowest rib <= 38.0 mm and not cut by the border; the ratio S3 cut only at the
  valley of a calibrated bimodal distribution, else dropped.
- **Rule 4, MDPA thoraco-lumbar shape score** (`ctsp:paper/mpda/main.tex` L335-341: T12 against L1 AUC 0.990, 97.3 %
  over 1,485 vertebrae): a second opinion, never applied to an unnamed body before; its canal features must not come
  from OpenSpineToolkit at or after 1b7005c.
- **Combination and sweet spot**: flag = union of rule outputs; truth = read tiers only; **sweet spot pre-stated** as the
  configuration with the highest specificity subject to sensitivity >= 0.95 on read-tier positives, pooled and per
  subtype; prevalence windows as an outside check (13 rib-bearing 0.37-0.88 %, lumbar rib 1.6 %, stump twelfth rib
  12.6 %, L6 2-5 %).
- **Paired corpora**: only 850 CTs have a radiograph of the same person (COBRA 692 on the deformed `ct_def`, C-ArmLSpine
  149, 9 cadaver/phantom); on C-ArmLSpine rules 1, 3 and 4 are computable on at most about 19 of 149 cases; C-ArmLSpine
  poses were fit at 0.1465 mm/px while the code now says 0.150, so poses are refit first.
- **Review**: stage 1 screen by Ashley Schehr (HF handle [handle withheld]), blinded to the registry's call; stage 2 confirm by the
  senior reviewer ("Dr Tech", whose full name is recorded nowhere on disk; `RESUME_2026-09-22_PM.md` L56, L69), blinded to
  stage 1. Reviewer instructions: `ssn:docs/REVIEW_TRANSITIONAL.md` (untracked).
- **Freeze** (§9): signer, date and sha256 blank. After the freeze every output row carries `prereg_sha256`.
- Open before the freeze: the 33-CT difference between `CORPUS.md` (21,655) and the tiers (21,622); PANORAMA's 1,495
  masks not yet in the tiers.

### B.2.11 The review-tree code (written 2026-09-27, untracked, not run as far as recorded)

`ssn:tools/transitional_review/` (`git status`: untracked `??`; files dated 2026-09-27 16:57-18:11):
- `anomaly_rules.py` (2,229 lines): one JSON + one TSV row per CT with rules 1 and 3, rule 2 / 1b / 4 features (no
  decision: nothing frozen), comparators, the sha256 of the pre-registration as read, `prereg_status: draft`, git SHA,
  input sha256s. Modes `case`, `run --claim`, `collect`, `--selftest`.
- `anomaly_rules_array.sh`: CPU Slurm array (reqp, requeue, 2 cores, 8 G, `/dev/shm` scratch, afterany):
  `sbatch -D $RC/rules --array=0-63 --export=ALL,LIST=$RC/tiers/tier1.tsv .../anomaly_rules_array.sh`, then
  `anomaly_rules.py collect --out $RC/rules/tier1` (header).
- `build_review_tree.py` (2,261 lines): one case directory per flagged CT under `RS/review_tree/<date>/<TYPE>/`
  (symlinked CT, masks, ITK-SNAP / Slicer label descriptors, radiographs with camera geometry, `evidence.json` with a
  hidden block for audit, README, `make_slicer_scene.py`), plus `manifest.tsv`, `index.html`.
- `rule_report.py` (1,588 lines): per-rule contribution, the configuration sweep with Wilson intervals and the
  pre-stated sweet spot, ROC per rule, prevalence windows, `report.html`; truth from `ctsp:docs/castellvi_consensus.csv`,
  `ctsp:Lumbosac.csv`, the VerSe Suppl. Table 1 and the registry's read tier only.
- `review_app/` (HF Space app: claim -> submit -> blind stage 2), `pose_to_viewer.py`, `cobra_geometry_to_P.py`,
  `refit_carmlspine_poses.sh`.

The 2026-09-27 18:05 checkpoint lists, still to do: read the build workflow's journal (wf_ded52e0e-cd1), run each
self-test, commit `tools/transitional_review/`, then on the grid the rules array, tree build, `rule_report`, review
app, and deliver `REVIEW_TRANSITIONAL.md`; "Nothing is scored as a result before PREREG_rules.md is frozen"
(`ssn:docs/RESUME_2026-09-22_PM.md` L28-33). No later file records any of these steps.

### B.2.12 The R + C = 22 rule (evaluated 2026-09-22, removed)

`ssn:docs/ANOMALY_RULE_EVALUATION.md`, `ssn:docs/anomaly_rule_evaluation.json`, grid job 40414996,
`ssn:tools/eval_anomaly_rule.py`. R + C = N − 1 for every target, so the rule is "N ≠ 23"; computable on 14 of 1,175
spines (1.2 %; VerSe 14/374, CTSP 0/801); C1 is labelled on every VerSe case carrying C2, so a detector that boxes C1
flags every normal spine (specificity 0.000); the 1.00/1.00 is circular; holding false alarm at 5 % needs per-body miss
rate <= 0.223 %. Method worth keeping: centre-to-centre spacing, not box gaps, finds a missing body (p99 ratio 1.17,
threshold 1.6). Incidental: `~/verse_drr` holds 13 exact duplicate renders (`glgl003`... repeating `gl003`...).
Rerun: `sbatch -D ~/spinesurg-ct-nnunet slurm/eval_anomaly_rule.sh` (`ANOMALY_RULE_EVALUATION.md` "Reproduce").
Removed from the SchwingNet manuscript on Greg's order (`mem:schwingnet-manuscript.md`).

### B.2.13 Re-read queues in the CTSpinoPelvic1K repo

`ctsp:docs/lstv_reread_queue.csv` (1 entry: 0172), `castellvi_reread_queue.csv` (25 rows, the learned Castellvi screen's
top 25, R5), `castellvi_type1_queue.csv` (214 rows), `castellvi_consensus.csv` (34 rows, the two-reader consensus),
`castellvi_readers_2026-09-04.csv` (45 rows) (row counts by `wc -l` minus header). Append new discrepancies to the
existing LSTV queue, never a new file (`mem:lstv-reread-queue.md`).

## B.3 Outside checks on the labellers (what the automatic calls are worth)

| check | result | file |
|---|---|---|
| A and B on 70 TotalSegmentator CTs with external L6/T13 labels | A found 12 of 28 L6 (6 no count), B 17 of 28 (9 no count), both 9; A found 5 of 7 T13, B 0 of 7 (7 no count); false L6 A 2, B 1 | `sn:results/transitional_registry/acquisition/validation/VALIDATION.md` |
| A and B (COBRA code) on CTSP against reader truth, before / after the 2026-09-24 rules | two-labeller L6 12 calls, 6 right [25.4, 74.6] -> 7 calls, 5 right [35.9, 91.8]; L6 reaching two-labeller tier 6 of 18 -> 5 of 18 | `sn:results/transitional_registry/cobra/labeller_validation_ctsp.md` |
| TotalSegmentator-stream two-labeller L6 on CTSP | right 6 of 10 | `REGISTRY.md` "What is not known" |
| COBRA one-labeller screen against CTSP reader truth | 10 of 24 L6, 0 of 52 T13 | `HO:power.md` §4 (citing `sn:results/stats_review2/recompute.json` S4) |
| NLST T13 before / after the rib-on-named-body rule | 9.3 % -> 1.5 % (prior 0.6-2.0 %) | `ACQUISITION_PLAN.md` §11 |
| Möller-mask stump flag against the VerSe read | 65.7 % sensitive | `mem:lstv-data-landscape.md`; `CLASSIFIERS.md` R27 |
| CTSP read prevalence against priors | L6 18/789 = 2.3 % (prior 3.2 %); four-lumbar 9/789 = 1.1 % (prior 1.6 %); only 33 Castellvi-graded against 71-142 expected | `HO:power.md` §4 |

## B.4 Distinct transitional people, by date (do not mix these counts)

| date | count | source |
|---|---|---|
| 2026-09-17 | 749 anomalous spines in 3 tiers (tier A 355) | `mem:anomaly-manifest-sources.md` |
| 2026-09-23 | 81 transitional spines (VerSe 56, CTSP 18, TS 4, C-ArmLSpine 3) | `sn:results/anomalous_inventory.md` |
| 2026-09-23 | 89 (VerSe 56, CTSP 18, TS 12, C-ArmLSpine 3), superseded: the 12 TS were raw-id selections, 4 transitional | `sn:results/power_table.json#inventory_today`; `HO:power.md` §7 row 2 |
| 2026-09-23 | 194 persons (L6 110, T13 7, Castellvi I-II 31, lumbar rib 14, sacralised 28, unassigned 4) | `sn:results/rare_class/transitional_subtypes.md` |
| 2026-09-23 | G3 split: L6 107, T13 7, sacralised 28, Castellvi 31, lumbar rib 14, unassigned 4 | `sn:results/rare_class/split_plan.md` |
| 2026-09-24 | registry: L6 146, T13 14, sacralised 27, Castellvi I-II 31, lumbar rib 26, unassigned 62 | `REGISTRY.md` table A |
| 2026-09-24 | rendered transitional CTs 196 | `MAXIMIZE.md` totals |
| 2026-09-27 | tier-1 flags L6 148 (registry) + 303 (screens), T13 14 + 82 | `ssn:docs/ruleclass/TIERS.md` §1 |

## B.5 Recipes for the anomaly chain (in dependency order)

1. Anomaly manifest: `python tools/anomaly_manifest.py --out ~/model_night/anomaly_manifest` (grid, via sbatch).
2. Inventory and subtypes: `tools/anomalous_inventory.py` (`sn:slurm/anomalous_inventory.sh`), then
   `tools/transitional_subtypes.py`.
3. Split: `sbatch -D $HOME/spinesurg-ct-nnunet --export=ALL,STAGE=all SchwingNet/slurm/g3_split.sh`.
4. Streams: `ssn:slurm/harvest_verse_{census,ts,ts_cpu,render}.sh`, `harvest_cobra_{cases,ts}.sh`,
   `harvest_validate_{a,b}_ctsp.sh`, `ctsp_registry_census.sh`; the tools named in B.2.4.
5. Registry: `python tools/transitional_registry.py` (reads every `<stream>/rows.csv`, writes `registry.*`,
   `REGISTRY.md`); a test exists, `ssn:tools/test_ts_transitional_registry.py`.
6. Renders: `python tools/rare_class_maximize.py` then `sn:slurm/rare_max_stage.sh`, `rare_max_verse.sh`,
   `rare_max_verify.sh`.
7. Acquisition: `bash slurm/acquisition_submit.sh tier1` (targets env, validation, tier1, tier1_late, tier2, dedupe);
   `python tools/acquisition_census.py` for the ranking; `tools/census_table_2026-09-25.py` for the census table.
8. Ruleclass: the arm scripts live on the grid under `RS/ruleclass/code/` (`ts_arm_gpu.sh`, `ts_arm_collect.sh`,
   `armb/armb_tier.sh`, `armb_measure.sh`, `armb_remeasure.sh`, `armb_collect.sh`, `pelvis/pelvis_*.sh`)
   (`JOBS_RECORD_2026-09-27_1544.md`); local copies are not in the repository.
9. Rules, tree, report (after the PREREG freeze): `anomaly_rules_array.sh` per tier list -> `anomaly_rules.py
   collect` -> `build_review_tree.py --census <census.tsv>` -> `rule_report.py --census ... --castellvi ...
   --lumbosac ... --verse-suppl ... --lstv-flags ... --registry ... --prereg docs/ruleclass/PREREG_rules.md`.

## B.6 Traps specific to the anomaly work

- Never read `has_T13` from the VerSeFusion manifest (18 claimed, 6 true; six of the eighteen carry an L6 instead,
  the signature of a wrong label map); `verse707` is a genuine table-versus-mask conflict (`mem:versefusion-t13-flag-wrong.md`).
- SPINEPS masks harvested before 147428d carry raw ids 1..N; never name by mask id (`TIERS.md` §3-4;
  `mem:spineps-ids-can-be-scrambled.md`). In `tsv3_ctd` 431 and in `ctd_relabel/bench_ts_native` 31 "relabelled" masks
  are symlinks back to the raw mask (`TIERS.md` §4).
- TotalSegmentator `sacrum` and `vertebrae_S1` are disjoint; the whole sacrum is their union; TS rib masks often lack
  the rib head, so a rib-free count on TS ribs alone disagrees with SPINEPS (`PREREG_rules.md` §0;
  `mem:ruleclass-super-detector-run.md`).
- Dataset803 was trained on CTSpine1K + CTPelvic1K + COLONOG, and 440 of the 802 CTSP pelvis labels are its own
  out-of-fold pseudo-labels, so on CTSP its agreement with "GT" is model-versus-model (`PREREG_rules.md` §2).
- Children: an unfused S1 reads as a free body (`TIERS.md` §1).
- LCC post-processing deletes the loose lamina of a spondylolytic vertebra; "one bone = one component" is the wrong
  invariant (`mem:spondylolysis-and-border-anomaly-findings.md`).
- A model that counts from the rib anchor fails preferentially on LSTV cases, because the anchor itself moves
  (`mem:spondylolysis-and-border-anomaly-findings.md`).
- L6 = 0.000 Dice under duplication is a distinct-case count signal, not a trainer bug (`mem:l6-sample-count-and-counting-decoder.md`).
- Two strata of the CTSP folds hold 2 cases and cannot appear in every fold (`HO:power.md` §5).

---

# Part C. The power calculations

## C.1 Every power or sample-size calculation on disk

The complete inventory, with reproduced checks and its own arithmetic, is `HO:power.md` (written 2026-10-08,
`HO:power_calc.py` -> `HO:power_calc.json`, using the repository's exact-binomial code from `sn:LEVELCHECK_MODEL.md`
§11 and `ssn:tools/stats_compare.py`). Its section 1 lists 18 sources; the ones that bear on this topic:

| # | calculation | file | what it says |
|---|---|---|---|
| 1 | Wilson lower bound by errors k and test persons n | `sn:results/power_table.json` (tool `sn:tools/fig_claim.py`) | 0 errors: 88.65 % at 30, 92.13 at 45, 93.98 at 60, 96.3 at 100; inventory block (89 persons) superseded |
| 2 | smallest n meeting the pre-stated targets (Figure 5a) | `sn:results/power/power.json#panel_a`, `#n_needed_zero_errors` | 90 % exact-level bound: 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; 85 % variant-sensitivity bound: 22 / 34 / 45 / 74 carriers |
| 3 | probability the Wilson target is met; n for 80 % power | `sn:results/stats_review/recompute.json` R4_wilson | 99 persons at a true 97 %, 69 at 98 % (planning values with no transitional measurement behind them) |
| 4 | LevelCheck comparison (paper 2): n_min, power tables, Holm | `sn:LEVELCHECK_MODEL.md` §5, §7, §13 (frozen §9) | n_min 19 / 48 / 152 for p0 0.822 / 0.926 / 0.976; the 97.6 % comparator cannot be exceeded at any reachable n |
| 5 | independent recomputation of paper-2 power | `sn:results/stats_review2/recompute.json` S1-S4, S9, S12; `sn:REVIEW2_STATS.md` | reproduced; power is 0 at any true accuracy <= 0.822 |
| 6 | LevelCheck claim power table (earlier) | `sn:LEVELCHECK_CLAIM.md` §4 | the same Wilson table; 89-person inventory: test n ≈ 36, target met only with zero errors; 3 real transitional subjects give 43.9 % |
| 7 | learning-curve "N to target" | `sn:results/indomain/FIT_N.md` | A.6; not a power calculation |
| 8 | two-proportion power, n per arm, minimum detectable difference | `ssn:tools/stats_compare.py` | tool only; no saved output found (`HO:power.md` row 9) |
| 9 | expected transitional people per collection; stopping rule | `ACQUISITION_PLAN.md` §2-3; `ssn:tools/acquisition_census.py`; `ssn:docs/CENSUS_TABLE_2026-09-25.md` | [E]; B.2.7-B.2.8 |
| 10 | QI protocol | `ssn:paper/qi_universal_protocol/main.tex` L229-231 | "powered to estimate, not to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" |
| 11 | selective prediction | `mem:selective-prediction-the-honest-99.md` | certifying 99 % selective accuracy with zero errors takes about 298 answered cases; class-conditional 99 % needs >= 99 real calibration cases per class |
| 12 | older Figure 5 panel b (exact binomial) | `sn:NUMBERS.md` L52 (marked SUPERSEDED 2026-09-24) | 80 % power for the 90 % bound at 69; exceeding 97.6 % first at 4,276 (as recorded in `HO:power.md` row 14) |
| 13 | co-occurrence | `ssn:tools/anomaly_cooccurrence_from_labels.py` L3-6 | CTSP odds ratio 4.00 (1.00-16.03) on a both-cell of two, "underpowered on its own" |
| 14 | CTSpinoPelvic1K article | `ctsp:paper/mpda/main.tex` | no power calculation; L919-921 "would test the co-occurrence ... at full power" |

Rows 15-18 of `HO:power.md` §1 (BUU label noise "n = 80, no power" in `ssn:docs/MORNING_BRIEF_2026-09-16.md`; the
SyntheX parity reading in `ssn:docs/FLUORO_DATASET_STRATEGY.md` L177; the paper-2 reviews `sn:REVIEW_STATS.md` F17 and
`sn:REVIEW2_STATS.md` N1, N8, N10, N11) are reviews of the above, not new calculations.

## C.2 Figure 5a, re-derived for this note

The pre-stated targets come from `ssn:docs/FLAGSHIP_PLAN.md` "The claim (G6)" item 4 (exact level on transitional real
frames with Wilson lower bound >= 90 %; variant sensitivity lower bound >= 85 %; "If the bound is not met, the
manuscript says so"). Wilson 95 % score interval, z = 1.959964. Re-derived independently by
`<laptop scratchpad; see MANIFEST_LOCAL.md>/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/handoff/t2_wilson_check.py` (pure arithmetic, no repository import): 0 errors 35 / 22, 1 error 53 / 34,
2 errors 69 / 45, 5 errors 113 / 74; error-free bounds 64.57 % at n = 7, 90.59 % at 37, 93.00 % at 51, 95.86 % at 89;
88.65 / 92.13 / 93.98 / 96.30 % at 30 / 45 / 60 / 100. **All match** `power.json`, `power_table.json`,
`LEVELCHECK_CLAIM.md` §4 and `sn:sections/results.tex` L91-98.

What the manuscript says (`sn:sections/results.tex` L91-98): no real-frame transitional test person was verified; the
three C-ArmLSpine L6 patients are scored only in cross-validation; against 91 unread COBRA2026 screen calls, a
two-labeller count found seven at-risk persons with an exported frame (error-free bound 64.6 %); the split's 51 at-risk
CT test persons, most in the encoder's training data, would give 93.0 %. The bound is a bound, not a power: it assumes
zero to five errors, and `HO:power.md` §2 rows 8-10 compute the power at planning accuracies (for example at 51 persons
with no error allowed, 0.07 / 0.21 / 0.36 / 0.60 at a true 95 / 97 / 98 / 99 %).

## C.3 The plain answer the power files give (from `HO:power.md` §6, restated)

- Every powered statement rests on planning accuracies of 95-99 % that no transitional measurement supports; the
  measured transitional figures (render L6 recall 56.1-72.4 %, real C-arm L6 classifier 44.9 %, film interior
  anomalous 66.0 %) put every transitional test at or near zero power.
- The one comparison already decided at its n is LODO against pooled detection on one device (28 cases, 8 to 0).
  Device-level claims cannot be tested with 4 devices (the smallest two-sided sign-flip P is 0.125).
- Paper 1's 90 % target needs 35 error-free at-risk persons; paper 2's primary H1 needs 19; today 7 unverified real
  at-risk persons exist.
- No power calculation exists for the synthetic-to-real ratio, for device-level differences, or for LODO across
  devices (`HO:power.md` §8 row 5).
- T13 is the scarce class everywhere: 44-138 T13 people expected in the whole holding [E], against about 55 needed in
  total for 22 test carriers under the 50/10/40 split (`HO:power.md` §4).

## C.4 Method: pre-registration and SHA-256 anchoring, as practised across these projects

The practice that keeps a result tied to the rule it was judged by has four working forms on disk. (1) **U251** (the
RNA-seq project, otherwise outside this topic): `PREREG*.md` and `TARGETS.md` are hash anchors whose SHA-256 is
written into every result file as `prereg_sha256` and quoted in the manuscript; result JSONs carry `_sha256` stamps and
can only be regenerated by rerunning the pipeline, never edited; editing a pre-registration's text breaks the tie
(`mem:u251-name-sweep-traps.md`). (2) **The transitional rules**: `PREREG_rules.md` §9 has a freeze block (signer, date,
sha256) and `anomaly_rules.py`, `build_review_tree.py` and `rule_report.py` already hash the document as read into
every row with `prereg_status draft|frozen`; a change after the freeze is a new dated version, never an edit
(`PREREG_rules.md` header and §9). (3) **The paper-2 comparison**: `sn:LEVELCHECK_MODEL.md` §9 freezes by git
ancestry; the G6 evaluator records UTC time and `git rev-parse HEAD` at unblinding, the commit adding the file must be
an ancestor, and any later value change lists old, new and reason. (4) **The manuscript build**:
`sn:generated/numbers_audit.md` records, per `\RESULT` key, the compiled value, file, pointer and the file's SHA-256;
`power.json` hashes each input file (`sn:RESULTS_BUILD.md`). The film N-curve ablation used the weaker form of a
reading rule written in the revision log before the numbers came back (`REVISION_LOG3.md` §13: "Reading rule, stated
before the numbers"), with no hash. A new student should copy form (2): write the rule, hash it, stamp every output
row, and treat any number produced before the freeze as calibration.

---

# Part D. Leakage controls on these curves

| curve | control | file |
|---|---|---|
| A1 2026-09-17 sweep | none adequate: v2 split per source, NHANES twins across the split; `subset_bank.py --drop-val-twins` written afterwards | `mem:nhanes-double-inclusion.md`; `ssn:tools/subset_bank.py` |
| A3 lcurve | test split never in any list; the three real L6 patients removed from every list of every device; checkpoint on a fixed val split | `sn:results/lcurve/lcurve.md` "Design" |
| A4/A5 det_fill / name_fill | `tools/eval_gate.py` on every model chain against every test image's patient; list intersections recorded; detection 45 cells and naming 245 cells held out, overlap 0, unresolved 0 | `INDOMAIN.md` §1; `FIT_N.md` "Method" |
| A7/A8 film N-curve and ablation | new render-only encoder because v9 and the Figure 6 G3 encoder both trained on the film persons; test persons outside every cell and outside the encoder's bank; `eval_gate` inside `a5-rows`; each cell `heldout: HELD OUT` | `ssn:tools/film_ncurve.py` docstring; `film_ncurve.json#cells/*/heldout` |
| A10 coverage arms | 40 unseen-sweep subjects excluded from training; real tests never trained on | `N_VS_COVERAGE_PLAN.md` part ii |
| a5 per-source film numbers | selection split, leak check by patient key: 0 of 549 BUU, 727 CSXA, 52 NHANES val patients in train | `sn:results/a5_rows_meta.json` |
| cv_v9 C-arm per level | v9 lineage re-run; the old lineage is `held out: False`, 60 unresolved | `sn:results/eval_gate/closure/cv_v9/CV_V9.md` |
| G3 transitional split | leak audit PASS, but 49 of 54 L6 val+test people are in v8/v9 training lineage | `sn:results/rare_class/split_plan.md` |
| deleted-bank trap | an unreadable `--holdout-bank` left the trained-on set empty; `tools/holdout.py` now raises; references repointed to `allspine_v7_fov96_ctx` | `mem:grid-quota-and-deleted-banks.md` |

---

# Part E. Where documents disagree

| # | the two readings | trusted | why |
|---|---|---|---|
| 1 | The task brief calls `paper/rsnai/main_v2.tex` the RSNA AI manuscript; `sn:main.tex` is the manuscript with Figure 5 and the `\RESULT` build | `sn:main.tex` | `main_v2.tex` last changed 2026-09-22 and still holds `\todo{[C8] scaling curve}`; `sn:main.tex` was rebuilt 2026-09-25 with every Figure 5 number keyed (`git log`; `sn:RESULTS_BUILD.md`; `mem:schwingnet-manuscript.md`) |
| 2 | `mem:film-ncurve-ablation-result.md` and `sn:REVISION_LOG3.md` §13: "7 of 9 pre-stated cells separated, all 'help'"; `READ.md` and `PER_LEVEL_DOMAIN_ANGLE.md`: seven separated, six for and one against (BUU all persons, renders HURT, separated) | `READ.md` | it is the tool's own output (`film_ncurve_ablation_read.py`), and BUU all reads 96.9 [96.0, 97.8] against 98.5 [98.0, 99.0], intervals apart; `PER_LEVEL_DOMAIN_ANGLE.md` (later, 2026-09-27) corrects the earlier wording |
| 3 | The Discussion sentence (`sn:sections/discussion_motivation.tex` L53-56) puts "separated on every seed in 7 of 9 cells" inside "at five to twenty-five persons per corpus"; only six of the nine verdict cells are in that range, and the seventh separated cell is the reversal | the numbers are right; the sentence's scope is loose | the gap range 6-22 and "one corpus 1.6 points the other way" are both correct; a reader could take 7 of 9 as all in the scarce range. Greg to decide whether to reword (not recorded as decided) |
| 4 | `mem:film-ncurve-ablation-result.md`: the Discussion sentence is "NOT in the tex"; `ssn:docs/RESUME_2026-09-22_PM.md` L73-79 and the tex itself: it is in, since 2026-09-27 13:20 | the tex | `discussion_motivation.tex` L53-56 carries it with five `\RESULT` keys |
| 5 | `ssn:docs/ruleclass/TIERS.md` §0: tier 1 5,094 / tier 2 12,217 / untiered 4,311; `ssn:docs/RESUME_2026-09-22_PM.md` L134: 5,095 / 12,218 / 4,312 | `TIERS.md` | it is the builder's own document and its per-collection table sums to 5,094; the RESUME line is a progress note. An off-by-one per list suggests a counted header line; not confirmed |
| 6 | `ssn:docs/CENSUS_TABLE_2026-09-25.md` "CTs on disk" and "FOV gate pass" against the collection `SUMMARY.md` files and `TIERS.md`: one higher in every collection checked except PANORAMA (AMOS 724 vs 723, NLST 501/499 vs 500/498, AbdomenAtlas 7,650 vs 7,649 ...) | `SUMMARY.md` / `TIERS.md` | `ssn:data_platform/DATA_MANIFEST.md` L175, L3698-3703; the grid query behind the census table is not on disk; the CNS 2026 table copies the high figures (`ctsp:paper/cns2026/prep_v8_table.py`) |
| 7 | `PREREG_rules.md` §0 / `CORPUS.md` (grid): census 21,655 CTs; `TIERS.md`: 21,622 | `TIERS.md` for the lists in use | the 33-CT difference is called "unexplained" and must be resolved before the census table is final (`PREREG_rules.md` §0) |
| 8 | Transitional person counts differ by file and date (81, 89, 194, 146 L6 ...) | the registry (`REGISTRY.md`, 2026-09-24) for persons; the G3 split for sides | B.4 lists each with its date; `power_table.json`'s 89 is superseded because 8 of its 12 TotalSegmentator spines are normal (`sn:results/anomalous_inventory.md`) |
| 9 | `mem:anomaly-manifest-sources.md` (2026-09-17): co-occurrence OR VerSe 4.30 [2.59, 7.14]; `mem:feasibility-claims-measured.md` (audit, same day): VerSe 280 fully graded 3.61 [2.08, 6.27], inflated by count-coupling | 3.61 | the audit removed count-coupled and unknown-scored-negative rows; quote it with the morphology-only 3.2 [1.8, 5.8] beside it |
| 10 | `INDOMAIN.md` (10:43, 10 resamples) prints "no interval" for every asymptote; `FIT_N.md` (15:48, 2,000 resamples) gives intervals | `FIT_N.md` | it is the interval-bearing extract from the 2,000-resample `fit.json` |
| 11 | `INDOMAIN.md` §7 says the coverage comparison is PENDING; `POOLED_FIT.md` (2026-09-25) and Figure 5d answer it | `POOLED_FIT.md`, `power.json` | `INDOMAIN.md` was generated before the arms landed and was not regenerated |
| 12 | `slurm/scaling_sweep.sh` says the curve is drawn by `make_feasibility_figures.py` as the scaling figure; `INVENTORY.md` G8 says the film N sweep "exists only on the leaky v2 bank" | both true at their dates | the film N-curve (A7, 2026-09-24) now replaces it for Figure 5; G8 predates A7 |

---

# Part F. Unknowns

| # | fact | where looked |
|---|---|---|
| 1 | grid job id of the 2026-09-17 scaling sweep | `ssn:slurm/scaling_sweep.sh`, `ssn:docs/FEASIBILITY_REPRODUCE.md`, `sn:results/indomain/INVENTORY.md`, `mem:remedies-refuted-2026-09-17.md`, repo grep for `scaling_` job ids |
| 2 | whether `fig9_scaling` was ever drawn, and where | `ssn:tools/make_feasibility_figures.py`; local file search (no copy) |
| 3 | whether `eval_scaling_curves.py cases` ever ran, and its result | `ssn:slurm/eval_scaling_curves.sh` foot; `INDOMAIN.md` L13; repo grep for `scaling_cases` |
| 4 | the exact flag that produced `sensitivity/pooled_fit_trained_only.json` | `sn:results/coverage/sensitivity/POOLED_FIT.md`; `pooled_fit.json` |
| 5 | exact sbatch flags for the coverage-arm chain beyond script and array | `sn:results/coverage/PENDING_JOBS.json` |
| 6 | date and job id of the LSTV flag learning curve; its full table | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` L659 (only the five points); `~/lstv_flag/LEARNING_CURVE.md` is grid-only |
| 7 | whether the nnU-Net ablation array (`docs/ablations.md`) completed and what it found | local `tables/` (absent); `mem:grid-quota-and-deleted-banks.md` (only the `ablate` folder size) |
| 8 | seeds 1-2 for film N-curve cells at N >= 50 | `PER_LEVEL_DOMAIN_ANGLE.md` "What is not known" (not run) |
| 9 | any synthetic:real ratio sweep result | `PER_LEVEL_DOMAIN_ANGLE.md` Table A; `HO:power.md` row 5 (never run) |
| 10 | per-angle naming accuracy | `PER_LEVEL_DOMAIN_ANGLE.md` Table F (does not exist) |
| 11 | per-level film naming on held-out persons | `PER_LEVEL_DOMAIN_ANGLE.md` Table E (only selection split, derived) |
| 12 | why the reported held-out detector reads a flat 49.5 % across the case134 spin | `sn:figures/figS4.record.json` (recorded as unexplained) |
| 13 | Greg's decisions on supplement Table S5, the ratio sweep, seeds above N = 25, the denominator-repair wording | `ssn:docs/RESUME_2026-09-22_PM.md` L35-37; `REVISION_LOG3.md` §11 |
| 14 | what the ruleclass arms (A, B, pelvis) finished after 2026-09-27, and current counts in `RS/ruleclass/arms/*` | `ssn:docs/RESUME_2026-09-22_PM.md`; `ssn:data_platform/`; memory (nothing after 2026-09-27) |
| 15 | whether `PREREG_rules.md` was signed and frozen | `ssn:docs/ruleclass/PREREG_rules.md` §9 (blank on 2026-10-08) |
| 16 | whether `anomaly_rules.py`, `build_review_tree.py`, `rule_report.py` or the review app ever ran on the grid, and whether their self-tests pass | `ssn:tools/transitional_review/` (untracked); `RESUME_2026-09-22_PM.md` L28-33 |
| 17 | the outcome of build workflow wf_ded52e0e-cd1 (its journal) | its journal path is in `RESUME_2026-09-22_PM.md` L28; not read here (session folder) |
| 18 | the 33-CT difference between `CORPUS.md` (21,655) and the tiers (21,622) | `PREREG_rules.md` §0; `TIERS.md`; `CORPUS.md` is grid-only |
| 19 | PANORAMA's flags (its call step 40430888 and summary 40430889 were pending on 2026-09-27) | `TIERS.md` §5 |
| 20 | which of the 1,186 near-duplicate alias candidates are the same person; person counts after dedupe | `TIERS.md` §8; `alias_pairs_all.csv` is grid-only |
| 21 | Dr Tech's full name, department and HF user | `RESUME_2026-09-22_PM.md` L56, L69 ("has no name anywhere on disk") |
| 22 | `greg_verdict` on any registry review-queue case | `REGISTRY.md` "Review queues" (0 filled on 2026-09-24); no later file |
| 23 | how many CTSP LSTVs a whole-cohort Castellvi read would add (33 graded against 71-142 expected) | `HO:power.md` §8 row 10; `ctsp:paper/mpda/main.tex` L919-921 |
| 24 | the cause of the census table's one-high counts | `ssn:data_platform/DATA_MANIFEST.md` L3698-3703 (grid query not on disk) |
| 25 | whether the 148 C-ArmLSpine cases are 148 people | `HO:power.md` §8 row 13; `sn:sections/discussion_limits.tex` |
| 26 | the person-level intraclass correlation for transitional endpoints (needed for two-proportion power) | `HO:power.md` §8 row 4 |
| 27 | power under the `LEVELCHECK_MODEL.md` §15 replacement detector | `HO:power.md` §8 row 6 |
| 28 | Barr 2026's de novo value at n = 700 | `mem:synthetic-real-ratio-evidence.md` (flagged for checking) |
| 29 | which grid copies of `tools/eval_gate.py`, `patient_keys.py` and related tools ran the 2026-09-24 cells (local copies were a later revision) | `PENDING_JOBS.json#not_done_by_this_pass/grid_tool_versions` |
