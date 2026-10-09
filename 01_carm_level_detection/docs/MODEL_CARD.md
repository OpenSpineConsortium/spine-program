# Model card — naming the vertebral level from C-arm exposures

Written 2026-09-22 for the models the RSNA AI manuscript (`paper/rsnai/main_v2.tex`) reports. One card
covering four things that ship together, because none of them is useful alone: a **vertebra/sacrum
detector**, a **level encoder**, a **recurrent head**, and the **linker/chain/confirmation** that turns a
series of exposures into one named column.

**Every number in this card carries the file it was read from.** Where the honest entry is *not measured*,
it says so and names the job that would measure it. Nothing here is transcribed from memory, a log
message or an earlier document without the file being opened.

Companion documents: `docs/DATASHEET.md` (the data), `docs/RSNAI_CLAIMS.json` (the ledger that re-derives
every manuscript number), `docs/RSNAI_PLAN.md` (what is and is not verified).

---

## 1. Model details

### 1.1 What the four pieces are

| piece | architecture | input | output | where the weights are |
|---|---|---|---|---|
| **Detector** | YOLO11m, COCO init (`init: yolo11m.pt`) | one 8-bit exposure, 1024 px | boxes, classes `0 vertebra`, `1 sacrum` | `~/spine-detector/runs/devcorpus/dc_{A,B}_held_<device>/weights/best.pt` (grid) |
| **Level encoder** | ResNet-18, two-channel stem (image + target-marker), 27-class head | 2 × 320 × 320 fixed-scale context crop, target body at 96 px | 512-d embedding + 27-class posterior | `~/carm_cvmix{0..4}_fov96_ctx/runs/model_rung_1_ft_cv{k}_aug2.pt` (grid, 44,825,692 bytes each) |
| **Recurrent head** | `recurrent_order.RunLabeller`: Linear(512→256)+GELU, 2-layer BiGRU(256), Linear(512→27) | the run's embeddings, 2–9 vertebrae | 27-class posterior per position | `~/model_night/heads_carm/head_cv{0..4}.pt` (grid, 8,473,365 bytes each) |
| **Sweep logic** | no learned parameters | the frames, their boxes and embeddings | a chain of nodes, ordinals counted from the anchor, a confirmation offset | `tools/sweep_map.py`, `tools/needle_confirm.py` |

Class vocabulary is 27 levels — C1–C7, T1–T13, L1–L6, sacrum — read from
`tools/make_context_crops.LEVEL_ORDER`. **T13 and L6 are real classes, not post-hoc relabels**; that is the
point of the project and it is also where the model is weakest (§5).

### 1.2 Versions, seeds and code

| field | value | source |
|---|---|---|
| detector init | `yolo11m.pt` | `~/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/scores.json` `init` |
| detector epochs / imgsz / batch | 40 / 1024 / 8 | same `scores.json`; `args.yaml` |
| detector seed | `0`, `deterministic: true` | `~/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/args.yaml` |
| encoder init for the CV arms | registry alias `allspine_v2_r1` → `~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt` | `slurm/carmlspine_cv.sh`; `ls -l ~/model_registry/aliases/allspine_v2_r1` |
| encoder fine-tune | 15 epochs, lr 1e-4, `--augment 2` | `slurm/carmlspine_cv.sh` |
| head training | `tools/head_mixed_length.py --train-mode mixed` | `slurm/carmlspine_cv.sh` |
| code SHA in the result files | **absent from `devcorpus_train.py` and from `docs/carmlspine_cv5_mixed_2026-09-21.json`** | `docs/RSNAI_PLAN.md` box E4, status *partial* |

**This is a known defect, not an oversight being reported as a feature.** `tools/device_fit.py` writes
`code_sha` into every device card (see `docs/devices/cios_fusion.json` `fit.code_sha = 6e1cf8d`);
`tools/devcorpus_train.py` and the C-ArmLSpine CV scorer do not. Two of the three numbers in the
manuscript abstract therefore come from JSONs that cannot say which commit produced them. The seed is
recoverable for the finished detector runs from each run's `args.yaml` (`seed: 0`); it is not recorded in
`scores.json`.

### 1.3 Weight identity

**Not measured: no SHA-256 exists for any weight file reported here.** `grep devcorpus
~/model_registry/registry.jsonl` returns 0, as does `rx_pooled` and `r18_ce_v3` — the encoder
`tools/reproduce_physics.py` lists as a hard prerequisite *by path*. Every model in the k-devices half of
the paper is addressed by a mutable path under `~/spine-detector/runs`, which any rerun with
`exist_ok=True` overwrites. The registry exists (`docs/MODEL_REGISTRY.md`) precisely because a model
addressed by a mutable path was destroyed once.

To fix: `python tools/model_registry.py register` on each `dc_*/weights/best.pt`, each
`model_rung_1_ft_cv{k}_aug2.pt` and each `head_cv{k}.pt`, with `--metrics` pointing at that run's scores
file, then a ledger claim keyed to the sha. Not done as of 2026-09-22.

### 1.4 Licence and contact

Code: private repository `spinesurg-ct-nnunet`, branch `L6_Class` (private since 2026-09-14). Weights:
not released. Contact: Gregory Schwing, Department of General Surgery, Wayne State University / Detroit
Medical Center.

**Conflict of interest.** The author has a commercial interest in a level-confirmation product under
development, as stated on the manuscript title page.

---

## 2. Intended use

### 2.1 What it is for

To tell a surgeon **which vertebral level** an intraoperative C-arm exposure is showing, from the
exposures alone: no preoperative CT or MR, no registration to a 3-D scan, no tracked instrument, no
fiducial. The surgeon's existing remedy — count from the sacrum or from C2 across overlapping shots — is
what is automated, and the instrument's own confirming exposure is matched back onto that count.

The intended user is a surgeon or radiographer in an operating room that has a C-arm and does not have
navigation. `docs/CARM_DEPLOYMENT_EVIDENCE.md` §1–§7 establishes the two plausible deployment routes (a
Siemens Cios OpenApp; an external unit ingesting the C-arm's video, the LessRay/K180038 pattern).

### 2.2 What it outputs, and what it does when it does not know

Per vertebra: a level name, a probability, an entropy and an **abstain flag**. The flag is raised when the
whole-run decode and the single-crop reading disagree, or when the probability is below
`--abstain-below`, default **0.5** (`tools/level_prototype.py` line 132, rule at line 355). Abstention is
the safety mechanism, and §5.3 says plainly how far it can be trusted.

### 2.3 Out-of-scope use

- **Any clinical use.** Nothing here is cleared by any regulator, and no prospective study exists.
- **Autonomous level determination.** The system is evidence beside the surgeon's count, not a
  replacement for it. It has never been read by a clinician in theatre.
- **Regions it was not tested on.** The only intraoperative test set is **lumbar** (C-ArmLSpine: levels
  T11–sacrum, 265 of 296 frames carry L1 and only 3 carry T11 —
  `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine/summary.json` `boxes_per_level`). No cervical or
  thoracic intraoperative frame has been scored. **No C2 anchor has been demonstrated on a real
  intraoperative frame** (`docs/RSNAI_PLAN.md` C10).
- **A C-arm outside the tested families.** Held-out-device numbers exist for three device families; the
  other C-arms in the data are cadaver, phantom or non-spine.
- **Frames containing instrumentation.** Whether the test frames contain screws, rods or retractors, and
  how the system behaves when they do, is **not measured** — no subgroup analysis by instrumentation
  exists.
- **Paediatric, post-operative and severely deformed spines.** Untested.

---

## 3. Training data

The datasheet is `docs/DATASHEET.md`. In brief:

### 3.1 Detector (device corpus, leave-one-device-out)

`~/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/scores.json` `lists`:

| field | value |
|---|---|
| training devices (design A, Elekta held out) | `cios_fusion`, `surgio_b51_dr` |
| geometry the renders were cast under | `cios_fusion` |
| synthetic training entries | 5,408 |
| real-frame training entries | 896 (`real_rep: 2`) |
| validation entries | 794 |

Synthetic frames are whole-spine CTs from TotalSegmentator v2 ray-cast under a device's real poses and
styled through that device's nine fitted image-formation terms (`tools/device_style.py`, cards in
`docs/devices/*.json`). The **held-out device is absent from the training frames, from the training
renders' poses and from the calibration terms**, which is the definition the plan fixed
(`docs/RSNAI_PLAN.md`, rules of accountability).

### 3.2 Level encoder and head (C-ArmLSpine five-fold CV)

Per-fold mixed bank, from `/rs/rs_grp_oschome/go2432/data/or_ready/audit/AUDIT.md` (fold 0 shown; the
other folds differ only in the `carm_*` counts). **These are CROP counts of a capped bank, not films** —
the twelve sum to the bank's 31,446 crops:

```
buu_full 635, csxa 1758, nhanes 303, nhanes_drr 277, ctsp_drr 638, verse_drr 940,
physics_drr 5285, physics_rare 1132, FLUOROCAP 2100, VINDRPS 2632, carm_AP 7869, carm_LAT 7827
```

The distinct films behind the film sources, read from the bank's own case array (job 40416442): buu_full 589,
csxa 1,478, nhanes 236, nhanes_drr 208, **VINDRPS 2,071**, FLUOROCAP 950. The 2,632 was read as a VinDr film
count in three documents until 2026-09-23; it is 2,632 crops of 2,071 of the 10,466 released images, and the
level bank the reported model was trained on (`allspine_v8`/`v9`) holds no VinDr film at all.

Split by case, `md5(case) % 5 == k` is the test fold; the audit records **0 test cases in any fold's DRR
bank, crop bank or mixed bank**, and 0 split-rule violations.

### 3.3 A leak in the encoder's initialisation, stated rather than buried

The CV arms initialise from `allspine_v2_r1`, trained on the `allspine_v2` bank. Two split leaks are
documented in that bank family:

- **NHANES II entered twice**, as two sources split independently: 48 of 54 NHANES validation patients had
  their other copy in training (`docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`).
- **CTSpinoPelvic1K entered under two naming schemes**: 357 people on both sides of v6 and v7
  (`docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`).

`nhanes` and `nhanes_drr` both appear in the fold banks above, so the **initialisation of every C-ArmLSpine
CV encoder carries this leak**. What the leak does *not* touch: the C-ArmLSpine test cases themselves,
which are held out by case in every bank (§3.2), and every device-held-out detector result. The clean
rebuild is `slurm/allspine_v8_clean.sh` → `allspine_v8_bank.sh` → `allspine_v8_train.sh`; until it lands,
pooled real-film numbers from v2/v6/v7 are not quotable.

---

## 4. Evaluation data and metrics

### 4.1 Test sets

| test | n | split rule | source file |
|---|---|---|---|
| C-ArmLSpine five-fold CV | 148 cases, 296 frames | `md5(case) % 5` | `docs/carmlspine_cv5_mixed_2026-09-21.json` |
| C-ArmLSpine fixed test | 28 cases, 56 frames, 287 truth vertebrae | `md5(case) % 10` → 8–9 | `/rs/.../or_ready/audit/AUDIT.md`; `/rs/.../realxray/carmlspine/summary.json` |
| COBRA Elekta | 27 cases, 648 frames | same | `/rs/.../or_ready/audit/AUDIT.md` |
| DeepFluoro | **1 specimen**, 104 frames | fixed, by specimen | same |
| Geneva (BV Pulsera) | 1 phantom, 116 frames, all test | fixed | same |

### 4.2 Headline metrics, with their denominators

All from `docs/carmlspine_cv5_mixed_2026-09-21.json` unless stated.

| metric | value | denominator | key |
|---|---|---|---|
| lateral, whole frame, exact level | **98.22 %** | 617 vertebrae, 141 cases | `det/LAT/kfull.exact` |
| lateral, whole frame, detector recall of truth | **91.27 %** | of the truth vertebrae in those frames | `det/LAT/kfull.recall_named` |
| **lateral, whole frame, end to end** | **89.6 %** | = 0.9127 × 0.9822 | derived from the two above |
| lateral, **complete coverage** (truth boxes), exact | **93.64 %** | **676** agreed vertebrae, 143 cases | `oracle/LAT/kfull.exact` |
| lateral, complete coverage, within one level | **99.11 %** | same — **6 vertebrae are beyond one level** | `oracle/LAT/kfull.within1` |
| lateral, complete coverage, whole frame exact | 85.31 % | 148 frames | `oracle/LAT/kfull.frame_exact` |
| AP, complete coverage, exact / within one | 95.25 % / 100 % | 673 vertebrae | `oracle/AP/kfull` |
| AP, whole frame, exact | 96.67 % | 631 vertebrae, 142 cases | `det/AP/kfull.exact` |
| lateral, five in the field | 97.00 % | 667 vertebrae | `det/LAT/k5.exact` |
| lateral, three in the field | 92.86 % | — | `det/LAT/k3.exact` |
| lateral, one in the field | 72.85 % | — | `det/LAT/k1.exact` |
| device held out, vertebra recall (outline truth, conf 0.25) | 90.6 % | 287 truth vertebrae, 56 frames | `/rs/.../or_ready/lodo/rescore_outline.json` `lodo_carm__carm_test` |
| device held out, sacrum found (conf 0.25) | 83.9 % | same | same |

**The 98.22 % is conditional on detection.** It is computed over the vertebrae the detector found and
matched — 617 of the 676 agreed lateral vertebrae. Reporting it without the 91.27 % is a denominator
substitution, and it is named here for that reason.

**"No error exceeded one level" is false at complete coverage.** It holds on the detector-conditioned
subset (`det/LAT/kfull.within1 = 1.0`), and the oracle-box arm on the same cases, scoring all 676 agreed
vertebrae, gives `within1 = 0.9911` — **six vertebrae beyond one level**. A surgeon would act on that
sentence, so the complete-coverage figure is the one that belongs beside it. Both rows are in the same
file.

### 4.3 The operating point is not held out

The headline detector numbers are at **confidence 0.25**, which is one of 16 thresholds crossed with 3 box
conventions and 6 arms in `/rs/.../or_ready/lodo/rescore_outline.md`. The same arm at its own best-F1
threshold reads a different figure, and `tools/or_recall_curves.py` labels best-F1 thresholds as
test-tuned. `docs/PHYSICS_LINKING.md` already documents 0.25 as miscalibrated on both physics frames and
clean film. **A threshold chosen after seeing the held-out device's frames is not a held-out number.** The
transferred-threshold figure (`cross_device_threshold` in `curves.json`) should be the primary and the
curve the evidence; that reporting change has not been made.

### 4.4 Uncertainty

`docs/carmlspine_cv5_mixed_2026-09-21.json` carries a case-cluster bootstrap CI on the CV exact rates
(2,000 resamples, cluster = case, percentile method, `numpy.default_rng`;
`tools/carmlspine_pool_scores.py`). **53 of the 54 entries in `docs/RSNAI_CLAIMS.json` are bare point
estimates** — every device card R², every typicality, the leave-one-corpus-out figure, the L6 counts, both
per-source film-naming figures. No paired comparison with a CI of the *difference* exists for any of the
three comparative claims the manuscript makes.

### 4.5 Seed spread

All five seed-1 detector replicates now have a `scores.json` (re-checked on the grid 2026-09-22, late):
`dc_A_held_{cios_fusion,elekta_xvi,surgio_b51_dr}_s1` and `dc_B_held_{cios_fusion,surgio_b51_dr}_s1`.
**Only four of those five appear in the §4.6 table**: `dc_B_held_cios_fusion_s1` has no row, and no reason
is given. Either its `DEVICE-HELD-OUT` row is read and added or the sentence above is wrong; both cannot
stand. Nothing in this card turns on it, but a card that says "five exist" and shows four is the kind of
gap that is later read as a selection.
**No seed spread is reported anywhere in the manuscript**, but it is now computable; the held-out-device
rows read below (§4.6) are the first reading of them.

The *head* does have a measured spread, read from
`~/model_night/heads_mixed/mixed_allspine_v2_fov96_ctx_mixed_kmax4_seed{0,1,2}.json`
(`results.4.per_source.<source>.exact`, random 2–9 window):

| source | seed 0 | seed 1 | seed 2 | range |
|---|---|---|---|---|
| CSXA | 0.9987 | 0.9995 | 0.9981 | 0.14 pp |
| BUU-LSPINE | 0.9804 | 0.9800 | 0.9766 | 0.38 pp |
| ctsp_drr | 0.9645 | 0.9682 | 0.9617 | 0.65 pp |
| physics_rare | 0.6190 | 0.6198 | 0.6250 | 0.60 pp |

So a two-point difference between two detector designs is the same order as run-to-run variation on the
side of the system where variation HAS been measured, and cannot be claimed without the replicates.

### 4.6 The styled-corpus detector on its held-out device, read 2026-09-22

Read directly from `~/spine-detector/runs/devcorpus/<run>/scores.json`, the row whose `status` is
`DEVICE-HELD-OUT`. These are the C7 arms the manuscript leaves as a `\todo`; they are recorded here
because a model card that omits the number the models were built for is not a model card.

| run | design | held-out device | test set | frames | vertebra recall | sacrum found |
|---|---|---|---|---:|---:|---:|
| `dc_A_held_cios_fusion` | A | Cios Fusion | deepfluoro/test | 104 | **0.9157** | 1.0000 |
| `dc_A_held_cios_fusion_s1` | A (seed 1) | Cios Fusion | deepfluoro/test | 104 | **0.9157** | 1.0000 |
| `dc_B_held_cios_fusion` | B | Cios Fusion | deepfluoro/test | 104 | **0.9398** | 1.0000 |
| `dc_A_held_elekta_xvi` | A | Elekta XVI | cobra_elekta/test | 648 | **0.3024** | 0.3415 |
| `dc_A_held_elekta_xvi_s1` | A (seed 1) | Elekta XVI | cobra_elekta/test | 648 | **0.3135** | 0.2989 |
| `dc_B_held_elekta_xvi` | B | Elekta XVI | cobra_elekta/test | 648 | **0.3270** | 0.3645 |
| `dc_A_held_elekta_xvi_1dev_surgio_b51_dr` | A, **one** training device | Elekta XVI | cobra_elekta/test | 648 | **0.1221** | 0.0805 |
| `dc_A_held_surgio_b51_dr_s1` | A (seed 1) | Surgio-B51 | carmlspine/test | 56 | **0.1429** | 0.8214 |
| `dc_B_held_surgio_b51_dr_s1` | B (seed 1) | Surgio-B51 | carmlspine/test | 56 | **0.1498** | 0.8571 |

Four things follow, and none of them is flattering:

1. **The pre-stated pass criterion is not met on two of the three devices.** `docs/RSNAI_PLAN.md` C7 fixes
   "counting grade" at >= 97 % sacrum found and >= 97 % vertebra recall. Cios Fusion reaches 91.6-94.0 %
   vertebra recall and 100 % sacrum; Elekta reaches 30-33 %; Surgio-B51 reaches 14-15 % vertebra recall at
   82-86 % sacrum. The criterion was stated before the result was read, and it fails.

   **Two qualifications this row needs before it is used.** C7 states *two* pre-stated criteria and only
   the second is quoted above: the first is "design A or B >= baseline lodo on the held-out device with
   the paired-bootstrap CI of the difference excluding 0", and no paired bootstrap has been run, so the
   primary criterion is *undetermined*, not failed. And C7's 97 % is fixed **on the outline box
   convention**, which is also the convention of the 90.6 % / 83.9 % lodo baseline in §4.2; the
   `scores.json` rows above were read without recording which of the three box conventions in
   `rescore_outline.md` they use. Comparing them against the threshold, or against that baseline, is only
   valid if they are the same convention, and that has not been established here. Point 4 below rests on
   the same comparison.
2. **The seed spread is of the same order as the design difference.** On Elekta, design A gives 0.3024 and
   0.3135 across two seeds (1.1 pp) while A-versus-B is 0.3024 against 0.3270 (2.5 pp). No "design B beats
   design A" claim survives that without a paired interval, which does not exist.
3. **k = 1 to k = 2 training devices moves Elekta from 0.1221 to 0.3024** vertebra recall, which is the
   only scaling point on disk and is a real result for the C8 box — one point, one seed, no interval.
4. **The Surgio-B51 held-out row is far below the 90.6 % this card quotes in §4.2.** They are different
   experiments: §4.2 is a detector trained on the *real frames* of two other device families
   (`or_ready/lodo`), and this row is the *styled synthetic* corpus. The styled corpus does not yet reach
   what mixing two devices' real frames already achieves, and that comparison is the paper's central claim.
   It is stated here rather than left for a reader to assemble.

---

## 5. Caveats, limitations and known failure modes

### 5.1 The truth is two machines, not a human

Levels on the intraoperative cases come from a CBCT labelled by TotalSegmentator **and** SPINEPS+VERIDAH,
scored only where they agree. `/rs/rs_grp_oschome/go2432/data/carmlspine/levels.json` `summary`:

```
cases 148   vertebrae 910   agree 814 (89.5 %)   disagree 41   unmatched 55
spineps_missing 3   variant_cases 22
```

**The filter is not neutral.** From `/rs/.../realxray/carmlspine/summary.json`, boxes with an agreed name:
T11 **0 of 3**, T12 **6 of 63**, L1 **209 of 265**, against L3 and L4 at **286 of 296**. The agreement
filter removes the thoracolumbar junction — the exact place a wrong-level error happens. Both labellers are
deep networks trained on overlapping public CT corpora, so their agreement is correlated and is not an
independent check; and both name a level by counting from the sacrum, the same anchor the system under
test uses. **No level truth in this study was established by a human.**

### 5.2 Collimation is the binding constraint on detection

From `/rs/.../or_ready/lodo/rescore_outline.md`, arm `lodo_carm` (the held-out-device detector), outline
recall at conf 0.25:

| field | frames | truth | vertebra recall | sacrum found |
|---|---|---|---|---|
| whole frame | 56 | 287 | **90.6 %** | **83.9 %** |
| three vertebrae in the field | 175 | 566 | **18.7 %** | **0.0 %** |
| one vertebra in the field | 287 | 345 | **11.3 %** | 7.7 % |

The clinical exposure is collimated. The manuscript reports k5/k3/k1 for *naming* and not for *detection*,
which reads as selective reporting of the condition where the method survives.

### 5.3 The posterior is not calibrated, and the abstain rule rests on it

From `~/selective/SELECTIVE.md`. **The denominator below is not 16,392.** That file's header reports
16,392 held-out vertebrae over 2,927 cases, but `tools/level_selective.py` splits those cases in half by
`--cal-frac 0.5` and computes the full-coverage accuracies, the risk-coverage curve and this per-class
table over the **test half only** (`for r in test`, lines 141–214) — roughly 8,300 vertebrae from about
1,460 cases. Quoting the 16,392 beside these rows is the same denominator substitution §4.2 names for the
98.22 %. The exact test-half `n` has to be read off the file's own "calibration … ; test …" line; it is not
reproduced here because it was not re-read. Per class, over that test half:

| level | n | accuracy | mean top posterior |
|---|---|---|---|
| T13 | 11 | **0.0 %** | 0.804 |
| T9 | 143 | 46.2 % | 0.625 |
| L6 | 57 | 63.2 % | 0.806 |
| sacrum | 70 | 98.6 % | 0.988 |

T13 is confidently wrong: 0 % right at a mean top posterior of 0.804. **No reliability diagram, expected
calibration error or Brier score exists anywhere in `tools/`.** A 0.5 abstain threshold on a posterior of
that quality is a threshold on an uncalibrated number.

What the same file *does* support, honestly — all of it over that test half, not over 16,392: at full
coverage the leaf accuracy is 78.8 % and the region accuracy 93.4 %; 99 % accuracy among answered vertebrae
is reachable at **35.7 % coverage** (n answered 2,956, 95 % lower bound 98.7 %), and split conformal gives
one region on **70.3 %** of vertebrae at 99.7 %. The internal arithmetic is consistent with the test half
and not with 16,392: 2,956 / 0.357 = 8,280 vertebrae, and 35.7 % of 16,392 would be 5,852. Certifying 99 %
one-sided at 95 % confidence with no observed error needs about **298 answered cases** (rule of three;
ln 0.05 / ln 0.99 = 298.1 — checked). The coverage figure is also **not held out**: `coverage_at` picks the
largest coverage meeting the target *on the same test half it is reported on*, so it is a threshold chosen
after seeing the outcome, the same objection §4.3 raises against confidence 0.25.

### 5.4 The anchor may be a framing convention

`/rs/.../or_ready/robust/position_prior.json`: a fixed prior box, with no model at all, finds

| device | sacra found by the prior | median IoU |
|---|---|---|
| C-ArmLSpine | **85.7 %** | 0.69 |
| COBRA Elekta | 58.5 % | 0.54 |
| DeepFluoro | 13.5 % | 0.17 |

Counting starts at the sacrum, so the 83.9 % held-out sacrum recall must be read against its device's
prior of 85.7 %.

### 5.5 The sweep numbers use the annotation's boxes

Every sweep/chain figure in the manuscript uses truth boxes, which measures the linker and not a
deployable system; and the executed move is the commanded move by construction, so the exactness figures
are an upper bound on what the search window achieves when a radiographer's move is not the commanded one.

### 5.6 What is not measured at all

- Per-class intervals, macro-averaged (balanced) accuracy beside the micro-averaged headline.
- Calibration (§5.3), paired comparisons with a CI of the difference (§4.4), seed spread for detectors
  (§4.5), weight hashes (§1.3), code SHA in the result files (§1.2).
- Behaviour with instrumentation in the frame; patient age, sex and habitus (the C-ArmLSpine DICOMs carry
  **no** `PatientAge`, `PatientSex` or `PatientID` tag — checked in
  `/rs/.../carmlspine/tags_case1.txt`, which carries `Manufacturer`, `Manufacturer's Model Name
  Surgio-B51`, `KVP` and `Exposure Time` and nothing identifying).
- An external architecture baseline on the detection task (every detector number is YOLO11m).

---

## 6. Runtime cost

Measured by `tools/eval_runtime_cost.py`; result JSON named in the run's `--out`. The tool times each
stage by calling the same function the pipeline calls, on named hardware, with the spread over repeats,
and it refuses to estimate a stage it could not run.

**Where that sentence actually is.** The line *"No speed claim is made here: end-to-end latency on the
hardware this would run on was not measured"* is `paper/focused/main.tex` line 632, with a companion at
line 382 (*"End-to-end latency on embedded hardware is unmeasured"*). It is **not** in the RSNA AI draft:
`grep -i "speed\|latenc\|runtime\|real.time" paper/rsnai/main_v2.tex paper/rsnai/main.tex` returns
nothing, so `main_v2.tex` does not disclaim a cost — it states no cost at all, which is the weaker
position of the two. This section is what either draft would cite.

**What the number has to be compared against**, from the same paragraph of `paper/focused/main.tex`
(primary sources cited there): LevelCheck registration was reported at **4.7 s** per image on a 2012
graphics card and **17–72 s** per registration in an operating room on a single-GPU workstation
(`levelcheck2012`, `manbachi2018`), against three surgeons' stated willingness to wait **20 s to one
minute** in all cases and more than a minute in **60.6 % (305/503)** of the ratings where they had judged
LevelCheck helpful (`desilva2016`). The protocol here is three or four exposures for a lumbar target and
six or seven for a mid-thoracic one — which is why the sweeps timed are 3 and 7.

### 6.1 The geometry every timing is at

Read from disk, not assumed: all 296 `/rs/.../realxray/carmlspine/meta/*.json` record `size` 1024 and
`px_mm` **0.1915** — the object-plane pixel size (`px_mm_detector` 0.2930 at SID 1140 / SOD 745 mm, so a
magnification of 1.53). The median spacing of their truth box centres is **177.9 px**. The tool derives
its pitch independently, from `sweep_map.PITCH_MM["lumbar"]` = 34.0 mm at that pixel size, giving
**177.5 px** — 0.2 % apart, which is the check that the linker is being timed on the right search window.
Bodies per exposure default to `det/LAT/kfull.vertebrae / frames` = 617/148 = **4.17**; the truth carries
6.10 boxes per frame, so `--bodies 6` is the detector's own load.

**Two defects in that paragraph were found by adversarial review on 2026-09-22 and are fixed in the tool;
the §6.3 run predates the fix.**

1. `bodies_per_frame()` walked `docs/carmlspine_cv5_mixed_2026-09-21.json` as a nested
   `det` → `LAT` → `kfull`, but that file is keyed `"det/LAT/kfull"` as **one flat string**. The read
   always failed and the tool fell back to a hard-coded `4`. Because 617/148 = 4.17 rounds to exactly that
   4, nothing in the output differed — the number was right and its stated source was not. The §6.3 timings
   are therefore at 4 bodies from a constant, not from the file. The tool now tries both spellings, records
   which one answered, and emits a caveat naming the hard-coded default when neither does.
2. The pitch cross-check was decided from the **default** frame size before `--frames` had loaded the real
   exposures, so a run on frames of any other size still recorded `applies: true` and "0.2 % apart".
   Verified by running the tool on a 512 px fixture: it certified a 177.55 px pitch against C-ArmLSpine's
   177.9 px on frames whose real pitch was 100 px. The check is now made after the exposures exist, carries
   `frame_px_actually_used`, and caveats when it does not apply.

### 6.2 The finding

**The linker, not the networks, is the cost.** `sweep_map.ncc_shift` searches a (dy × dx) grid of
normalised correlations at full frame resolution. `map_query_panorama` already reduces its images to
`sweep_map.WORK_PITCH` = 40 px per body before matching, and its docstring says why ("the difference
between seconds and a day per collection"); `ncc_shift` does not. The tool therefore times the link both
ways and reports them side by side, **with the answer beside the cost**: `geometry.reduced.same_answer_check`
records the translation each resolution returned and whether they agree once the reduced `dy` is divided by
the scale. A reduction that changed the answer would not be a remedy, and asserting that it does not is
exactly the kind of tidy explanation this project has been wrong about before.

### 6.3 What it measures, on the workstation, 2026-09-22

Run: `tools/eval_runtime_cost.py --repeats 12 --geo-repeats 5 --full-linker-repeats 2 --e2e-repeats 2
--threads 16 --sweep 3 7`, code SHA `edf0801`, seed 0, at the C-ArmLSpine geometry of §6.1 (1024², pitch
177.55 px derived, 177.9 px measured — 0.2 % apart), four bodies per exposure, flip TTA on.

**The exposures were SYNTHETIC**, not C-ArmLSpine frames: no `--frames` was given, so the run used the
tool's generated exposures — noise with a periodic column of bright blocks at the real pitch, on a real
1024² canvas. The JSON carries that as a caveat; this section did not, and that is a material omission,
because §6.1 reads as though the frames as well as the geometry came from disk. What follows from it: the
**timings stand** (the correlation grid, the crop canvas and the template are set by frame size, pitch and
box count, not by bone), but the *same-answer* result below does **not** — see the correction after the
tables.

Hardware: Intel64 Family 6 Model 165 (8 physical / 16 logical cores), 68.4 GB, torch 2.13.0+cpu, OpenCV
5.0.0, **no GPU, no ultralytics**. **The machine was shared** — the tool recorded four other Python
processes near 100 % and Defender above 100 % at both samples — so every figure below is a *contended*
latency and an upper bound. The §6.6 grid job is the uncontended version.

| stage | as implemented | reduced to WORK_PITCH | n | notes |
|---|---:|---:|---|---|
| detect | **not measured** | — | — | no ultralytics on this machine |
| crop (window + context crops) | 211.2 ms | — | 12 | rel SD 0.04 |
| encode (ResNet-18 over 4 crops × 2 TTA) | 3,350.7 ms | — | 12 | rel SD 0.40 |
| head (fc + BiGRU) | 123.8 ms | — | 12 | rel SD 5.2 — contention, not the model |
| **link** (`ncc_shift`, one pair) | **422,633 ms** | **575.4 ms** | 2 / 5 | **734×**; full range 414.3–431.0 s and 504–588 ms |
| chain (bookkeeping) | below the noise | below the noise | 2 | reported as 0 with its raw negative difference |
| confirm (panorama + template match) | 142.5 ms | 34.8 ms | 5 | `map_query_panorama` reduces internally |

| sweep | measured, reduced linker | additive budget | budget / measured | **budget, as implemented** |
|---|---:|---:|---:|---:|
| 3 exposures | **12.60 s** (SD 5.78) | 12.24 s | 0.971 | **856 s = 14.3 min** |
| 7 exposures | **27.20 s** (SD 13.72) | 29.29 s | 1.077 | **2,562 s = 42.7 min** |

Peak process resident set 368 MB. Encoder 11,173,376 parameters and 3.62 GMAC per crop; head 2,117,403
parameters. Both end-to-end figures are named `end_to_end_excluding_detector`: **the detector is not in
them and they are lower bounds.**

Result file: `~/bench/runtime_cost_workstation.json` on the grid, with
`~/bench/fig_runtime_workstation.{png,pdf}`. Redraw with
`python tools/eval_runtime_cost.py --redraw <json> --fig <stem>`.

**The finding, stated plainly.** As the code stands, one linked pair of full-resolution exposures costs
seven minutes on this CPU, so a seven-exposure sweep would take about three quarters of an hour — against
surgeons who said they would wait 20 s to a minute. Applying the reduction `map_query_panorama` already
applies takes the same sweep to 27 s. **That part stands.** The two sentences that followed it did not, and
are withdrawn:

*"the two resolutions return the same translation."* The `same_answer_check` that supported it ran on the
synthetic exposures, whose block column sits at **identical positions in every frame**. Any correlation
peak on that field lands on a multiple of the pitch by construction, which is exactly what both readings
are: −177 px is one pitch, −40 px is one `WORK_PITCH`. The agreement is forced by the periodicity and is
not evidence about the reduction. Run on real frames (a 512 px fixture, adversarial review 2026-09-22) the
two resolutions **disagreed** — full `dy` −423 against −408.4 rescaled, 14.6 px apart against a 4.4 px
tolerance — and the tool recorded `agrees_within_one_reduced_pixel: false` while still printing "same
answer" and a 244× speed-up, with no caveat. That is now a shouted caveat and the print is honest. **The
734× reduction has no measured accuracy result behind it on real frames and must not be shipped on the
timing.**

*"the additive budget and the composed wall clock agree to 3 % and 8 %, so the stage decomposition is not
hiding a stage."* That ratio is not reproducible at the repeat counts used. Three back-to-back runs of the
same configuration on the same machine (`--size 320 --sweep 3 --repeats 4 --e2e-repeats 5`) gave
**0.736, 1.206 and 0.803** — a 64 % span — while the wall clock itself barely moved (5.43 / 5.26 / 5.25 s).
The scatter is in the *budget*: the encoder's stage median read 835, 1,433 and 904 ms across the three.
The 0.971 and 1.077 above are one draw of that, at `--e2e-repeats 2` with a wall-clock relative SD of
0.46 and 0.50. A stage costing up to about 30 % of the sweep would be invisible to this comparison as run.
Two further reasons it is not the check it was described as: the budget's `crop` term is timed on
full-resolution exposures while the wall clock composes it at scale 0.2253, which over-counts it 1.8× (188.6
against 106.6 ms per exposure, measured); and when no reduction applies at all the budget silently dropped
`link`, `chain` and `confirm` and still printed a ratio. Both are recorded in the JSON now
(`additive_budget_reduced_missing_stages`, `budget_stage_resolution_note`) and the ratio is only a check
when the missing-stage list is empty and `--e2e-repeats` is large enough to resolve the disagreement.

`chain` is genuinely negligible; `crop` and `confirm` are tens to hundreds of milliseconds; the two costs
that will decide deployability are the **detector** (not measured here) and the **encoder**, and the
encoder's 3.35 s is eight passes of a ResNet-18 at 320 px on a contended CPU with no batching and no GPU.

**The detector stage is `not_measured` on any machine without ultralytics**, and every end-to-end figure
from such a run is renamed `end_to_end_excluding_detector` and is a lower bound.

### 6.4 Why an unmeasured latency was not acceptable

`docs/CARM_DEPLOYMENT_EVIDENCE.md` §6: **no CPU, GPU or RAM figure surfaced for any C-arm examined, from
any manufacturer**, and whether a Cios OpenApp is given an accelerator or only a general-purpose core is
unknown. The authors' own measured range on named hardware is therefore the only available anchor, which
is why a CPU-only measurement is part of the tool and not an afterthought.

### 6.5 What the JSON carries, so a millisecond can be judged

`hardware` (CPU model, physical and logical cores, RAM, torch/cv2/ultralytics versions, GPU name and
memory, any SLURM ids); `config` (frame size, pixel size, pitch and its cross-check, bodies per exposure
and the file that number came from, crop canvas, detector `imgsz`, TTA, repeat counts, and whether the
exposures were real or synthetic); per stage `n`, median, mean, SD, min, max, p5, p95, IQR and relative
SD; `peak_process_rss_mb` (a high-water mark, stated as such) and, on a GPU, `gpu_peak_allocated_mb` /
`gpu_peak_reserved_mb`; `not_measured` with a reason per stage; and `caveats`.

It also records **`machine_load_at_start` and `machine_load_at_end`**: system CPU utilisation and any
other process above 20 %. A latency measured while other jobs saturate the cores is a contended latency,
and nothing else in the output would say so; when the field is non-empty the tool emits a caveat naming
the processes and calling the figures an upper bound. **A reference measurement belongs on an otherwise
idle machine, which on this project means a SLURM job, not the workstation.**

### 6.6 Not measured

GPU-hours to fit a card, render a corpus, style it, or train one leave-one-device-out arm. `sacct -S
2026-08-01 -X --format=JobID,AllocTRES,ElapsedRaw` returns the rows this needs (checked on the grid
2026-09-22); the per-stage totals have **not** been derived here, and an earlier pooled figure is not
repeated in this card because it was not re-derived from that query.

Also not measured until this job runs: the **detector stage** and every **GPU** figure, because
ultralytics and CUDA are not on the workstation. The job that fills them:

The `--wrap` body is **one line**. An earlier version of this block broke it across lines inside the single
quotes with no backslashes; `sbatch` puts that string into `#!/bin/sh` verbatim, so every newline ends a
command, the python runs with **no arguments** and exits on `--out is required`, and the remaining lines
come back as `--out: command not found`. The job occupies a GPU, writes nothing, and its only symptom is a
log of "command not found". Written as a script instead of `--wrap` it is easier to read and cannot fail
that way:

```bash
cat > ~/spinesurg-ct-nnunet/slurm/runtime_cost.sh <<'EOF'
#!/bin/bash
#SBATCH --job-name=runtimecost
#SBATCH --partition=gvohp,galhp
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=/wsu/home/go/go24/go2432/model_night/logs/runtimecost_%j.out
export PYTHONNOUSERSITE=1 TMPDIR=$HOME/tmp
mkdir -p "$HOME/bench" "$HOME/tmp" /wsu/home/go/go24/go2432/model_night/logs
cd "$HOME/spinesurg-ct-nnunet" || exit 1
"$HOME/mambaforge/envs/spinedet/bin/python" -u tools/eval_runtime_cost.py --selftest || exit 1
"$HOME/mambaforge/envs/spinedet/bin/python" -u tools/eval_runtime_cost.py \
  --out "$HOME/bench/runtime_cost.json" --fig "$HOME/bench/fig_runtime" \
  --detector "$HOME/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/weights/best.pt" --imgsz 1024 \
  --model "$HOME/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt" \
  --head "$HOME/model_night/heads_carm/head_cv0.pt" --bodies 6 \
  --frames /rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images \
  --repeats 30 --geo-repeats 5 --full-linker-repeats 3 --e2e-repeats 15 --threads 1 4 16
EOF
sbatch -D ~/spinesurg-ct-nnunet ~/spinesurg-ct-nnunet/slurm/runtime_cost.sh
```

`--time` is 8 h, not 4: one full-resolution link is about seven minutes, `--full-linker-repeats 3` pays for
three of them, and the single-thread arm pays for the encoder about a hundred times over the stage and
end-to-end repeats. `--e2e-repeats` is 15, not 5, for the reason in §6.3: at the repeat counts used so far
the budget/wall-clock ratio is not resolvable. `--selftest` runs first so a job that would time a wrong
architecture stops before it spends the GPU.

A GPU job is used even for the CPU-only figures, because it is the way to get an **uncontended** machine;
a workstation running other jobs measures contention, and the tool's `machine_load_*` fields say so.

---

## 7. Ethical considerations

The failure mode that matters is a **confidently wrong level**: a name the surgeon acts on. §5.3 shows the
system has exactly that failure at T13 (0 % right, 0.804 mean posterior), and §5.1 shows the evaluation
withholds the thoracolumbar junction where such errors live. Any deployment must therefore present the
count as evidence beside the surgeon's own, abstain visibly, and never suppress the surgeon's check film.

All data are public and de-identified at source; the C-ArmLSpine DICOMs carry no patient identifiers at
all (§5.6). No patient consent was sought by this project because no new data were acquired.

---

## 8. How to reproduce

```bash
# check the encoder implementation against the published ResNet-18 arithmetic before believing a timing
python tools/eval_runtime_cost.py --selftest

# runtime, on the grid (the §6.6 sbatch line is the uncontended version of this)
python tools/eval_runtime_cost.py --out <dir>/runtime_cost.json --fig <dir>/fig_runtime \
    --detector ~/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt --imgsz 1024 \
    --model ~/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt \
    --head ~/model_night/heads_carm/head_cv0.pt --bodies 6 \
    --frames /rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images

# redraw the figure from a result, measuring nothing
python tools/eval_runtime_cost.py --redraw <dir>/runtime_cost.json --fig <dir>/fig_runtime

# every number THE MANUSCRIPT quotes, re-derived from its result file (non-zero exit on drift).
# NOTE: this covers docs/RSNAI_CLAIMS.json only -- 54 claims, none of them from this card or from
# docs/DATASHEET.md. No number in either document is under drift control. Adding them is a ledger
# entry per row, keyed {file, path, expect, tol}; until then "every number carries its file" means a
# human opened it once, not that a check re-opens it.
python tools/claims_check.py

# the leakage audit over the split files
python tools/or_audit_splits.py && python tools/or_audit_dupes.py
```

### What this card asks for next, in order

1. Run the §6.6 job so the detector stage and the GPU figures exist and the manuscript's "latency was not
   measured" sentence can go.
2. Register every reported weight (§1.3) and add `seed` + `code_sha` to `devcorpus_train.py`'s
   `scores.json` (§1.2) — a two-line change; `device_fit.py` already does it.
3. Read the five `_s1` detector replicates and report a seed spread beside every "beats" claim (§4.5).
4. Report the transferred-threshold detector figure as primary and the confidence curve as the evidence
   (§4.3), and the k3/k1 detector rows beside the naming ones (§5.2).
5. A reliability diagram, ECE and Brier score per region and per class, with and without temperature
   scaling, on `~/selective/post_val.jsonl` — the abstain rule has no calibration behind it (§5.3).
6. A human read of the 22 variant-flagged cases plus a random 30 against the CBCT, so the truth has one
   measurement from outside the two networks that produced it (§5.1).
