# Manuscript corrections from the eval-gate closure (2026-09-24)

Written by the closure workflow. **No manuscript file was edited.** `main.tex`, `sections/`, `tables/`, `NUMBERS.md`
and `figures/figure*.*` / `figures/figS*.*` belong to the paper-six-figures workflow; `supplement.tex` is listed here
too and was not touched. Each item gives the file and line as of 2026-09-24 07:30, the text as it stands (copied
verbatim) and the text to put in its place, with the result file every new number is read from.

Three loose ends were closed. What each moves in the manuscript:

| item | what was done | manuscript change |
|---|---|---|
| 1. case134 real spin | the conflict resolved from the lists; score stage re-run against the unseen render curve (grid job 40431371) | **none** to any quoted number: all four arms are held out, and the real-spin numbers reproduce exactly. The stale non-manuscript files are named in §1.4 |
| 2. allspine_v8, 192 persons in train and val | cause traced from the bank's own case/split arrays (jobs 40431372, 40431408 for v9) | footnote c of Table 1 and "Numbers deliberately absent" widened; no quoted number moves (none of the 192 is a film patient) |
| 3a. render- vs film-trained detector | carried forward from `leaks/render_vs_film_unseen_rerun.json` (job 40429839) | Table S2 rows, footnotes a and f; Supplement "Which source carries the detector"; NUMBERS rows |
| 3b. device-card gain | carried forward from `leaks/card_gain_unseen.json` | Supplement "Image-formation terms"; Table S1; Table 1 Geneva and Ljubljana rows and footnote k; Figure S3 caption; NUMBERS rows |
| 3c. plain-film naming | stated | Table 3 footnote f gains one sentence: there is no unseen plain-film subset until the Figure 6 model is scored |
| Holm family | recomputed with the two replacements | sacrum comparison $P=.008$ becomes $P=.009$; the card gain enters at $P=.009$ |
| U1: C-ArmLSpine naming on the v9 lineage (section 7; `closure/cv_v9/CV_V9.md`) | the case- and day-grouped fold models re-trained from `allspine_v9` on the shipped banks (jobs 40431706, 40431707), scored on the pre-repair export (40436580) and today's, zero-shot v9 at every field size (40436982), coupling and the a4/a7/a9 twins (40436581, 40436862, 40436983, 40436901); every new input held out, overlap 0 | **every `\PENDING{G5}{C-ArmLSpine CV on the v9 lineage}` filled** (Key Point 2, Abstract, Results, Table 4 rows 58-60, 73, 75, 78 and note h, Figure 4 b/d, 40 NUMBERS rows, CLAIMS L211); 98.2 % becomes 97.4 % (601/617), day-grouped 92.1 % (568/617), coupled 98.2 % (991/1,009); fine-tuning adds +1.0 pp on lateral (not significant) and +52.6 on AP; the day-grouped result stays below zero-shot, so Limitations gains one sentence (section 7.2 item 8); section 8 gives the accuracy-saturation reading Greg asked for |
| Resume 10:50 (section 6) | checkpoint verified; item 1 requeued under eval_gate/2 (job 40436881, identical numbers, sha256-bound); the manuscript drive's uptake of every replacement checked line by line | **applied** in the tables and supplement; thirteen NUMBERS.md rows still unmarked; two figure-owner files; the review of 2026-09-24 touches none of items 1-3 |

---

## 1. case134: did the pooled detector see case134? No

### 1.1 The conflict, resolved from the lists

The in-domain inventory said case134 is in 0 entries of the pooled detector's lists. The arc workflow's report
(`results/arc/case134_sweep.md`, "Contamination") said "case134 is in the carmlspine TRAIN split (md5 bucket 3): the
pooled detector saw this patient's two SPOT frames (AP, LAT) in training". Read on the grid on 2026-09-24:

- `spine-detector/runs/devcorpus/dc_P_pooled/args.yaml` (written 2026-09-22 17:42): `model: yolo11m.pt`,
  `data: /rs/rs_grp_oschome/go2432/data/devcorpus/lists/P_pooled/data.yaml`.
- That `data.yaml` names `P_pooled/train.txt` and `P_pooled/val.txt`, both written 2026-09-22 17:42:33 and not
  touched since.
- `train.txt`: 18,906 lines, 420 C-ArmLSpine lines, which are 210 distinct frames of 105 cases (real frames repeated
  twice, `LIST_INFO.json` `real_rep: 2`). **0 lines contain case134.**
- `val.txt`: 1,998 lines, 30 C-ArmLSpine lines of 15 cases. **0 lines contain case134.**
- `dc_P_pooled/weights/best.pt` was written 2026-09-23 01:46. `realxray/carmlspine/images/train/case134_AP.png` and
  `case134_LAT.png` were written 2026-09-23 05:28:00, after training ended. The export's label cache of
  2026-09-22 05:58 (`labels/train.cache`) lists 105 train cases and no case134.

**The inventory is right.** The arc report's sentence is true of the export's split rule (`md5(case) % 10` sends
case134 to train) and of the export directory from 2026-09-23 05:28 on. It is false of every list any of the four
scored detectors trained or was selected on. The error was conservative: it withheld a held-out claim that holds.

The other "pooled" detector, `rx_pooled_1024` (real frames only), trained from 2026-09-21 22:00 to 23:42 on the
export directory itself, so case134 was not in it either. The lineage store still puts `carmlspine:case134` in its
train keys (`touched.json`: 220 train keys), because a rewritten directory is bounded by the split rule
(DATA_ACCOUNTING §5.2). That bound is conservative and is what VERIFY G10 exercised. `rx_pooled_1024` is not scored on
the spin.

### 1.2 The re-score (grid job 40431371, CPU)

`SchwingNet/results/eval_gate/closure/jobs/closure_case134.sh` ran the gate alone on each arm, then
`tools/case134_sweep.py score` with the same four weights as `slurm/case134_export_score.sh`. It was told to declare
any arm the gate found seen with `--not-held-out-role`, labelled beside the others. None was:

| arm | checkpoint (sha256) | gate on the 301-frame spin |
|---|---|---|
| pooled | `devcorpus/dc_P_pooled` (13f17d8c…) | HELD OUT, overlap 0, 1 checkpoint in the chain (COCO root) |
| lodoA | `devcorpus/dc_A_held_surgio_b51_dr` (bfa05c73…) | HELD OUT, overlap 0 |
| lodoB | `devcorpus/dc_B_held_surgio_b51_dr_s1` (9f7f2ff5…) | HELD OUT, overlap 0 |
| real_lodo | `realxray/rx_lodo_carmlspine_1024` (f6fe6b97…) | HELD OUT, overlap 0 over 2 (through `anchor_none_v2_17-1882`) |

- The render column now comes from `or_ready/eval_gate/arc_unseen/recall_vs_angle.json`. It has md5 05ff586c…, the
  same as the repo copy `results/arc/recall_vs_angle_unseen/recall_vs_angle.json`. It covers 40 subjects, and its
  eval_gate says held out, overlap 0, unresolved 0.
- The tool now refuses a render curve whose weights differ from the run's; these match arm for arm.
- **The real-spin numbers reproduce exactly**: `detectors` in the new `case134_sweep.json` equals the old one field
  for field. Body recall over the spin at 0.25 / 0.74 is:
  - pooled 93.6 / 78.1 %
  - lodoA 37.2 / 29.1 %
  - lodoB 29.6 / 23.5 %
  - real_lodo 49.5 / 49.4 %

  Each is over 1,204 boxes and is one cluster.
- Only the render column changed. Against the void 17-subject curve, it rose by 0.172 on average across the 16
  compared bins for lodoA, by 0.095 for lodoB and by 0.036 for pooled, and it did not move for real_lodo (−0.003).
- The shape comparison therefore changes most for lodoA. Its mean |real − render| gap fell from 0.176 to 0.124.
- Outputs are in `closure/case134_sweep/`: `case134_sweep.{json,md}`, `fig_case134_recall_vs_angle.png`,
  `gate_check_<arm>.json`, the job log and the frame overlays. On the grid they are in
  `or_ready/eval_gate/closure/case134_sweep/`. The old run in `or_ready/arc/case134_sweep/` was kept.

### 1.3 Manuscript

Nothing to change:

- Figure S5 (file `figures/figS4.*`) draws only the real-spin recall, which reproduces exactly.
- Its record already calls pooled HELD OUT.
- No sentence quotes the render comparison.

Optional, for the figure's owner: `figS4.record.json#not_shown_and_why` gives the render curve's reason as "its 17
held-out subjects were the validation (checkpoint-selection) subjects … not drawn". An unseen 40-subject curve now
exists and has been set beside the spin. The reason should become "not drawn (by choice); the unseen curve is
compared in `results/eval_gate/closure/case134_sweep/`", or the curve can be drawn.

### 1.4 Stale, not manuscript

- `results/arc/case134_sweep.{json,md}` and `fig_case134_recall_vs_angle.png` are superseded by
  `results/eval_gate/closure/case134_sweep/`. They draw the void curve and carry the false contamination sentence.
- `EVALUATORS.md` §1.4, the case134 row, already says the sentence is wrong; it can now point to the replacement.

---

## 2. allspine_v8: why 192 persons sit in both train and val

### 2.1 Cause (grid job 40431372, `closure/v8_overlap_cause.py`, `closure/v8_overlap/v8_overlap.json`)

The bank was keyed by `~/patient_keys.json` (2026-09-22 16:18, md5 fddc9842…; `tools/patient_keys.py` at c27b53f).
The gate keys every bank case by today's rules. Read from the bank's own `case` and `split` arrays (103,052 crops,
18,565 cases):

- No case sits on two sides: 0 cases.
- Under the build's keys, 0 persons sit on both sides. The build's own check ("people on both sides: 0") was true of
  the keys it was handed.
- Under today's keys, 192 persons sit on both sides: 187 CTSpinoPelvic1K and 5 VerSe. This is the same set, person
  for person, as the lineage store's v8 row (9,612 train keys ∩ 1,784 val keys).

So the build script is not at fault, and no per-case split overrode the person draw. **The key file filed one person
under two keys:**

| corpus | persons | how |
|---|---:|---|
| CTSpinoPelvic1K | 187 | Implant renders (`implant_<id>_v<k>_…`) were keyed as a person called `implant:<id>_v<k>`, apart from their source CT `ctsp:<id>`, and each hardware variant `_v0`, `_v1` separately. The person draw then sent them to different sides: implant renders in train, plain renders in val (66); plain in train, implant in val (53); or implant variants on both sides (68). Example: `ctsp:0004` is val through `CTSP_COLONOG_3` and `ctsp_0004_*_p*`, and train through `implant_0004_v0_ap_p0` and `implant_0004_v1_*`. |
| VerSe | 5 | Two series of one subject were keyed as two persons (series keyed as subjects), e.g. `verse201` in train and `verse253` in val, both subject `verse401`. |

Rule 1 is the implant alias gap that `patient_keys.key_any` now closes (it keys an implant render to its source CT,
or refuses it). Rule 2 was fixed for v9 (commit 7e88870, 2026-09-22 21:13).

**The same trace on v9 (job 40431408, `closure/v8_overlap/v9_overlap.json`):** all 164 v9 persons on both sides
are CTSpinoPelvic1K implant renders (61 / 45 / 58 in the same three patterns). No VerSe person is among them.
VERIFY.md 1b left "the rest was not traced". It is now traced: 164 of 164 are the implant alias.

### 2.2 What the overlap touches

The 192 persons' validation cases are:

| val source | cases | crops |
|---|---|---|
| `ctsp_drr` | 77 | 692 of 1,006 val crops |
| `physics_drr` | 459 | 2,396 of 6,174 |
| `physics_rare` | 105 | 514 of 1,545 |
| `verse_drr` | 5 | 90 of 832 |

**None are film sources** (BUU-LSPINE, CSXA or NHANES II). Every v8 accuracy on a CT-render validation source is
therefore scored partly on persons in training. That covers `results/a5.json#per_protocol/*/{ctsp_drr, physics_drr,
physics_rare, verse_drr}`: 93.9, 76.4, 45.1 and 83.3 %. None of these is quoted in the manuscript.

### 2.3 Quoted numbers that descend from v8, and whether the overlap moves them

| NUMBERS.md line | number | from v8 how | moved by the 192? |
|---|---|---|---|
| 109, 110, 111 | CSXA 99.8 %, BUU-LSPINE 97.3 %, NHANES II 99.1 % (Table 3 rows, `tab3_naming.tex:55-57`) | v8 encoder + head on the v8 val films | **No**: no film patient is among the 192. They remain selection-split numbers (EVAL_LEAKS L4), labelled so |
| 239 | CSXA / NHANES II Wilson on n_eff | same | No |
| 248 | films at three bodies 95.0 / 99.6 / 94.6 % (Table 3 footnote f) | same | No |
| 112 | "leak check: 0 validation patients in training for csxa, buu_full, nhanes (v8 bank)" | a5 leak check | **Stands** for the three film sources. For the four render sources the same check reported 0 with `unparsed_keys` equal to every key (`a5.json#leak_check_by_patient_key`): it never ran on them |
| 43, 227; Table 4 footnote d | "val+test persons in the v8 or v9 train split: 49 of 54 (L6), 4 of 4, 14 of 14, 15 of 15, 7 of 7, 3 of 3" | v8 and v9 train splits | **Stands.** Re-derived from the two banks' own `split == train` cases, keyed as the gate keys them and folded as the G3 split folds: 49 / 4 / 14 / 15 / 7 / 3, identical |
| 189, 291 | 0 VinDr films in the level bank; 9,108 level-bank films | counts | No |

Found while re-deriving the 49 of 54, in the split workflow's file and not in the manuscript:

- `results/rare_class/split_plan.md` "Model exposure" says "v8: trained on 9893 people … v9: trained on 9878".
  `make_split.py` counts every `~/patient_keys*.json` case not in the bank's `val_cases` as trained. That includes
  the 1,713 `ts_drr` and `nhanes_drr` cases, whose roots neither bank read.
- The banks' own train splits hold **9,609** (v8) and **9,589** (v9) persons. The over-count is 232 TotalSegmentator +
  52 NHANES persons for v8, and 236 + 53 for v9. It is conservative, and it leaves the quoted per-subtype column
  unchanged (one L6 person, `ts:s1089`, is counted for v8 by that rule but is in v9's train split anyway).

### 2.4 Corrections

**Table 1, footnote c** (`tables/tab_corpus.tex:64`). Replace

```
VerSe series were keyed as subjects in the film bank, so no VerSe accuracy is quoted.
```

with

```
in the level banks, CTSpinoPelvic1K implant renders were keyed apart from their source CT and, in the first bank, VerSe series as subjects, which put CT-derived persons on both sides of each bank's split (192 in the first, 164 in the second; none from a film corpus), so no CT-render naming accuracy is quoted.
```

**NUMBERS.md:308** ("Numbers deliberately absent"). Replace

```
- Any VerSe accuracy from v8 (series keyed as subjects) and the pooled "overall" v8 figure.
```

with

```
- Any CT-render naming accuracy from v8 or v9 and the pooled "overall" v8 figure: the banks keyed CTSpinoPelvic1K implant renders apart from their source CT (v8: 187 persons on both sides of the split; v9: 164) and, in v8, VerSe series as subjects (5 persons) (`results/eval_gate/closure/v8_overlap/{v8,v9}_overlap.json`). No film patient is among them.
```

**NUMBERS.md:112**. Append to the number cell:

```
; for the four CT-render sources the same check did not run (every key unparsed); keyed as the gate keys them, 192 CT-derived persons (187 CTSpinoPelvic1K, 5 VerSe) are on both sides, none from a film corpus (`results/eval_gate/closure/v8_overlap/v8_overlap.json`)
```

**Optional, Methods** (`sections/methods.tex:52`). Replace

```
persons also in its training keys (Figure~\ref{fig:embedding});
```

with

```
persons also in its training keys, all CTSpinoPelvic1K persons whose implant renders the bank keyed apart from their source CT (Figure~\ref{fig:embedding});
```

**Not manuscript, for their owners:**

- `results/a5.json` labels: "v8 head (clean split)" and `v2_statement` "v8's known leak is VerSe (CT renders), which
  touches no film source". Should read: "v8's known leaks are VerSe series (5 persons) and CTSpinoPelvic1K implant
  renders (187 persons), both CT-derived; neither touches a film source".
- `results/RIGOR_FIXES.md` A5.
- `docs/MODEL_CARD.md:168` and `docs/DATASHEET.md:267` call v8 "the clean rebuild".
- `results/rare_class/split_plan.md` "Model exposure" totals (§2.3).
- EVAL_LEAKS.md L4 names the 192 but not their cause.

---

## 3a. Render- versus film-trained detector on plain radiographs

The as-quoted comparison used the first 25 annotated NHANES II spines. 24 of them are in the film detector's
(`detect_v5z_final`, parent `detect_v3`) own lists: 22 in train and 2 in val (EVAL_LEAKS L2).

The "196 of 233 bodies" was counted against `allspine_v7`, the level bank, which is the wrong list: the rerun file
still carries that field (`bodies_from_spines_in_holdout_train`), measured against v7.

The rerun scored every annotated NHANES II lumbar spine the gate passes for both detectors: 17 spines, 161 bodies,
held out True, overlap 0, unresolved 0 (`results/eval_gate/leaks/render_vs_film_unseen_rerun.json`; job 40429839).

| conf | film-trained | render-trained | film minus render [95 % percentile; BCa] | spines film > render : render > film | exact sign test p |
|---|---|---|---|---|---|
| 0.05 | 99.4 % (160/161) | 67.7 % (109/161) | +31.7 pp [21.0, 45.4]; [22.7, 48.2] | 16 : 0 | 3.1e-05 |
| 0.25 | 98.8 % (159/161) | 34.8 % (56/161) | +64.0 pp [55.3, 72.5]; [55.3, 72.6] | 17 : 0 | 1.5e-05 |

The file warns that intervals are unreliable below about 20 clusters (17 here).

**Table S2** (`tables/tab2_detection.tex:64-65`). Replace

```
Plain radiographs\fnm{f} & Render-trained detector, no real image & at 0.05: 71.7 (167/233) & -- & 43.3 (101/233) & -- & -- \\
 & Film-trained detector, in-sample (196 of 233 bodies from its training spines) & at 0.05: 99.1 (231/233) & -- & 98.7 (230/233) & -- & -- \\
```

with

```
Plain radiographs\fnm{f} & Render-trained detector, no real image & at 0.05: 67.7 (109/161) & -- & 34.8 (56/161) & -- & -- \\
 & Film-trained detector & at 0.05: 99.4 (160/161) & -- & 98.8 (159/161) & -- & -- \\
```

**Table S2 footnote a** (`tab2_detection.tex:71`). Replace

```
plain radiographs 25 NHANES II films (25 spines, 233 bodies).
```

with

```
plain radiographs 17 NHANES II lumbar films (17 spines, 161 bodies) whose patients neither detector trained or was selected on.
```

**Table S2 footnote f** (`tab2_detection.tex:76`). Replace

```
\fnm{f}Scored at 0.05 and 0.25 only; the film-trained recall is not a held-out number; paired difference at 0.05 +27.5 percentage points [20.5, 35.2], sign test 23 vs 0 spines, Holm-adjusted $P<.001$.
```

with

```
\fnm{f}Scored at 0.05 and 0.25 only, on every annotated NHANES~II lumbar spine that neither detector trained or was selected on; paired difference at 0.05 +31.7 percentage points [21.0, 45.4], sign test 16 vs 0 spines, Holm-adjusted $P<.001$; 17 clusters, so the intervals are approximate.
```

**Supplement, "Which source carries the detector"** (`supplement.tex:62-63`). Replace

```
on 233 vertebral bodies of 25 real films a film-trained detector, in-sample for 196 of
them, found 27.5 points more than a render-trained one at confidence 0.05 (20.5, 35.2; $P<.001$).
```

with

```
on 161 vertebral bodies of 17 real films whose patients neither detector trained or was selected on, a
film-trained detector found 31.7 points more than a render-trained one at confidence 0.05 (99.4\,\% against
67.7\,\%; 21.0, 45.4; 16 of 17 films favouring the film-trained detector, none the other; Holm-adjusted $P<.001$).
```

**NUMBERS.md**:

- **:113**. Replace the number cell with:

  ```
  render-trained vs film-trained detector on 161 bodies / 17 NHANES II lumbar spines neither detector trained or was selected on (gate held out, overlap 0), conf 0.05: 67.70 % vs 99.38 %; +31.7 pp [21.0, 45.4], BCa [22.7, 48.2]; sign test 16 vs 0 (p 3.1e-05). As first quoted (25 spines, 24 in the film detector's own train/val): 71.67 % vs 99.14 %, +27.5 pp, not held out
  ```

  Replace the file cell with `results/eval_gate/leaks/render_vs_film_unseen_rerun.json#conf_0.05`.
- **:244**. Replace with:

  ```
  | film- minus render-trained detector at 0.05: +31.7 pp [21.0, 45.4], $P<.001$ (16 vs 0 spines, p 3.1e-05, Holm 9.2e-5); 17 spines neither detector saw | Supplement, Table S2 footnote f | `results/eval_gate/leaks/render_vs_film_unseen_rerun.json#conf_0.05` |
  ```
- **:296**. Replace the number cell with:

  ```
  Table S2, plain radiographs (17 held-out spines, 161 bodies): render-trained 67.7 % (109/161) at 0.05 and 34.8 % (56/161) at 0.25; film-trained 99.4 % (160/161) and 98.8 % (159/161); paired difference at 0.25 +64.0 pp [55.3, 72.5], BCa [55.3, 72.6], sign test 17 vs 0
  ```

  Replace the file cell with `results/eval_gate/leaks/render_vs_film_unseen_rerun.json#conf_0.05`, `#conf_0.25`.

The render-trained detector alone is clean on all 25 as-quoted spines, 71.7 % (167/233). The replacement uses the
17-spine set for both detectors so that the pair stays paired.

---

## 3b. Device-card gain: patient-held-out folds only

The as-quoted +0.038 pools 24 folds from four devices. On two of them every fold fitted the one object it scores:

- BV Pulsera: the one Geneva resin phantom, 19 poses.
- PIXIUM 4600: the one Ljubljana cadaver, 18 radiographs.

Those folds are within-subject, not held out (EVAL_LEAKS L6; fold gates in `leaks/card_gain_unseen.json#gate_records`).
Re-read from `results/a6.json`, 10,000 fold resamples, seed 0, percentile (`results/eval_gate/leaks/card_gain_unseen.json`):

| folds | frames | mean gain [95 %] | frame-weighted [95 %] | negative folds | exact sign-flip p |
|---|---:|---|---|---:|---:|
| 12 patient-held-out (Cios Fusion, Elekta XVI) | 701 | +0.0193 [0.0076, 0.0326] | +0.0226 [0.0102, 0.0335] | 2 of 12 | 0.0044 |
| 12 within-subject (BV Pulsera, PIXIUM 4600) | 134 | +0.0560 [0.0248, 0.0881] | +0.0387 [0.0297, 0.0505] | 2 of 12 | 0.0034 |
| all 24, not held out (re-read here; `a3.json` quotes [0.0205, 0.0573] from its own resampling) | 835 | +0.0376 [0.0200, 0.0568] | +0.0252 [0.0151, 0.0346] | 4 of 24 | 0.00023 |

**Supplement, "Image-formation terms"** (`supplement.tex:42-45`). Replace

```
The fitted terms raised
held-out coefficient of determination ($R^2$) by 0.038 (95\,\% confidence interval: 0.021, 0.057; frame-weighted
0.025) over 24 folds nested in four devices, four negative (sign-flip over folds $P<.001$; all four device means
positive, $P=.13$).
```

with

```
On the two devices whose folds hold out patients (Cios Fusion and Elekta XVI; 12 folds, 701 frames), the fitted
terms raised held-out coefficient of determination ($R^2$) by 0.019 (95\,\% confidence interval: 0.008, 0.033;
frame-weighted 0.023; 0.010, 0.033), two folds negative (exact sign-flip over folds $P=.004$, Holm-adjusted
$P=.009$). On the other two a fold holds out views or frames of the one object every fold was fitted on (the
BV Pulsera phantom, the PIXIUM~4600 cadaver), so their gain, 0.056 (0.025, 0.088; 12 folds), is within-subject,
not held out.
```

Then **delete** the sentence at `supplement.tex:47-48`, which the replacement now says:

```
The folds of two devices are views or frames of one
object, not patients, so the pooled gain is not patient-held-out.
```

The criterion sentence between them ("The pre-stated criterion … was not met: … (Cios Fusion 0.015; $-0.003$,
0.034).") stays as it is. It is per device, and still not met.

**Table S1** (`tables/tabS1_device_terms.tex:24`). Replace

```
 & frames fitted; held-out $R^2$, card vs physics & & & 40 of 116; $R^2$ 0.952 vs 0.917 & 40 of 366; $R^2$ 0.905 vs 0.899 & 40 of 335; $R^2$ 0.974 vs 0.964 & 14 of 18; $R^2$ 0.679 vs 0.65 \\
```

with

```
 & frames fitted; fold-median $R^2$, card vs physics & & & 40 of 116; within-subject $R^2$ 0.952 vs 0.917 & 40 of 366; held-out $R^2$ 0.905 vs 0.899 & 40 of 335; held-out $R^2$ 0.974 vs 0.964 & 14 of 18; within-subject $R^2$ 0.679 vs 0.65 \\
```

**Table S1 note** (`tabS1_device_terms.tex:27`). Replace

```
Held-out $R^2$ is the median over folds, card against the uncalibrated physics default;
```

with

```
$R^2$ is the median over six folds of the frames each fold left out, card against the uncalibrated physics default; a Cios Fusion or Elekta XVI fold leaves out patients (held out), a BV Pulsera (one phantom) or PIXIUM 4600 (one cadaver) fold leaves out views or frames of the object the other folds were fitted on (within-subject);
```

**Table 1** (`tables/tab_corpus.tex:55-56`, last column). Replace

```
corpus; parameters (40 of 116, R² 0.952 vs 0.917)
```

and

```
parameters (14 of 18, R² 0.679 vs 0.650); no frame
```

with

```
corpus; parameters (40 of 116, within-subject R² 0.952 vs 0.917)
```

and

```
parameters (14 of 18, within-subject R² 0.679 vs 0.650); no frame
```

**Table 1 footnote k** (`tab_corpus.tex:72`). Replace

```
with the frames it was fitted on and its median held-out R² over six folds against uncalibrated physics.
```

with

```
with the frames it was fitted on and its median R² over six folds on the frames each fold left out, against uncalibrated physics (patients left out for Cios Fusion and Elekta XVI; views or frames of the one object for BV Pulsera and PIXIUM 4600).
```

**Figure S3 caption** (file `figures/figS2.caption.txt`, printed at `supplement.tex:99`). The whole caption becomes
(58 words, within the 60-word limit):

```
Image-formation parameters. (a) Real frame per device above its styled render; bar, 50 mm; R², body-region fit. (b) Fitted terms within their bounds: fold median, range. (c) Per-fold R² gain over uncalibrated physics (Pulsera, PIXIUM within one object); bar, six-fold t interval. (d) A refit with image noise in the loss failed its own gate; published parameters stand.
```

Panel (c) itself should separate the two kinds of fold, for example with hollow markers for BV Pulsera and PIXIUM.
That is the figure owner's decision. Panel (a)'s pair R² under the held-out fold fit is EVAL_LEAKS L7 and is not
part of this closure.

**NUMBERS.md**:

- **:134**. Replace the number cell with:

  ```
  mean gain over the 12 patient-held-out folds (Cios Fusion, Elekta XVI; 701 frames) +0.0193 [0.0076, 0.0326], frame-weighted +0.0226 [0.0102, 0.0335]; 2 of 12 negative; exact sign-flip p 0.0044 (Holm 0.0088). Within-subject folds (BV Pulsera, PIXIUM 4600; 134 frames) +0.0560 [0.0248, 0.0881]. All 24, not held out: +0.0376 [0.0205, 0.0573]
  ```

  Replace the file cell with `results/eval_gate/leaks/card_gain_unseen.json#patient_held_out_12`, `#within_subject_12`.
- **:140, :245** (device-level test "all four device means positive, $P=.13$"). Retire them from the printed set: two
  of the four means are within-subject, and with two held-out devices a device-level sign test cannot reach .05.
- **:141, :292**. Add "within-subject" before the Pulsera and PIXIUM medians.

The main text quotes no card-gain number. `methods.tex:59-60` says only that the terms "missed their pre-stated
criterion", which stays true. NUMBERS:245 names "abstract, Key Point 3, Results" as where the number appears; none
of them now carries it.

---

## 3c. Plain-film naming has NO unseen subset

Every annotated patient of CSXA (727 val / 4,963), BUU-LSPINE (549 val / 3,600) and NHANES II (52 val / 364) is in
the v8 encoder's training split or its validation split. The validation split chose the checkpoint (best of 40
epochs).

So every plain-film naming number is a selection-split number, and **no held-out plain-film naming number can be
computed from any existing level model**. One will exist only when the Figure 6 model is scored on the test side of
the person-disjoint G3 split. That model is ImageNet-initialised and trained on the G3 training side (the f6train
and f6eval chain, owned by another workflow). The G3 test side holds film patients: BUU 341, CSXA 499, NHANES 939
persons (`results/rare_class/split_plan.md`; the annotated subset is what a film naming number would be scored on).

Table 3 already labels the rows "selection split" and the text quotes none of them, so no number changes.

**Table 3 footnote f** (`tables/tab3_naming.tex:89`). Replace

```
\fnm{f}Patient-keyed validation split, which also chose the encoder checkpoint (one seed); random windows of two to nine bodies (at three: BUU-LSPINE 95.0\,\%, CSXA 99.6\,\%, NHANES II 94.6\,\%); NHANES II 76 films of 52 patients.
```

with

```
\fnm{f}Patient-keyed validation split, which also chose the encoder checkpoint (one seed); random windows of two to nine bodies (at three: BUU-LSPINE 95.0\,\%, CSXA 99.6\,\%, NHANES II 94.6\,\%); NHANES II 76 films of 52 patients. Every annotated patient of the three corpora is in this encoder's training or selection split, so no held-out plain-film accuracy exists until the ImageNet-initialised model of Figure~\ref{fig:levelcheck} is scored on the test films of the person-disjoint split.
```

**Optional, Table 1** (`tab_corpus.tex:46-48`, "Role in this work"). `level bank; validation` would read more
exactly as `level bank; checkpoint-selection split` on the CSXA, BUU-LSPINE and NHANES II rows.

---

## 4. The Holm family after the replacements

The four comparisons stay the same; two members change their data. Raw p values:

- zero-shot lateral minus AP: 2.5e-23 (unchanged; UNRESOLVED U1, not this closure's item)
- film minus render: 2.4e-7 becomes **3.1e-5** (16 vs 0 held-out spines)
- sacrum, same-device minus held-out: 0.0078 (unchanged)
- card gain: 2.3e-4 (24 folds) becomes **0.0044** (12 patient-held-out folds)

Holm-adjusted: **1.0e-22, 9.2e-5, 0.0088, 0.0088** (was 1.0e-22, 7.2e-7, 0.0078, 4.6e-4). If the zero-shot row moves
to the certified v9 model (79 vs 1 cases, p 1.3e-22), the first becomes 5.4e-22 and the other three are unchanged.

| where | as it stands | replace with |
|---|---|---|
| `supplement.tex:59` | `(5.4, 23.2; Holm-adjusted exact sign test $P=.008$)` | `(5.4, 23.2; Holm-adjusted exact sign test $P=.009$)` |
| NUMBERS.md:125 | `sign test 8 vs 0; Holm 0.0078` | `sign test 8 vs 0; Holm 0.0088` |
| NUMBERS.md:243 | `$P=.008$ (sign test 8 vs 0, p 0.0078, Holm 0.0078)` | `$P=.009$ (sign test 8 vs 0, p 0.0078, Holm 0.0088)` |

**NUMBERS.md:128.** Replace

```
exact/cluster p 2.5e-23, 2.4e-7, 0.0078, 2.3e-4 (exact sign-flip over 24 folds); Holm-adjusted 1.0e-22, 7.2e-7, 0.0078, 4.6e-4. Printed as $P<.001$, $P<.001$, $P=.008$, $P<.001$
```

with

```
exact/cluster p 2.5e-23, 3.1e-5 (16 vs 0 held-out spines), 0.0078, 0.0044 (exact sign-flip over the 12 patient-held-out folds); Holm-adjusted 1.0e-22, 9.2e-5, 0.0088, 0.0088. Printed as $P<.001$, $P<.001$, $P=.009$, $P=.009$
```

The Methods sentence (`methods.tex:110-111`, "Holm-adjusted over four comparisons named before adjustment (lateral
versus anteroposterior naming; three in the supplement)") needs no change.

---

## Where every number here is read from

| number | file |
|---|---|
| P_pooled list census, timestamps | grid `devcorpus/lists/P_pooled/{args,data}.yaml`, `train.txt`, `val.txt`, `LIST_INFO.json`; `realxray/carmlspine/images/train/case134_*.png`; `labels/train.cache` (read 2026-09-24) |
| case134 gate verdicts, re-score | `closure/case134_sweep/gate_check_<arm>.json`, `case134_sweep.json#eval_gate`, `#detectors`, `#render_curve_*` |
| v8 / v9 overlap, causes, exposure | `closure/v8_overlap/v8_overlap.json`, `v9_overlap.json` (`persons_on_both_sides_*`, `store`, `causes`, `val_*_by_source`, `exposure`) |
| render vs film | `leaks/render_vs_film_unseen_rerun.json#conf_0.05`, `#conf_0.25`, `#eval_gate` |
| card gain | `leaks/card_gain_unseen.json#patient_held_out_12`, `#within_subject_12`, `#all_24`, `#gate_records` |
| Holm | recomputed from the raw p values above (exact two-sided sign test 2·0.5^16 = 3.05e-5; sign-flip 0.00439 from the file) |


---

## 5. The gate closed (VERIFY.md 1b and 1c): no quoted number or printed sentence moves

Written by the gate-closure item (2026-09-24 08:10). Its files are under `closure/bypass/`: the grid job scripts,
their outputs (`grid_jobs/*.out`), one log per call (`logs/`) and the result files (`out/`). The code is
`tools/eval_gate.py` "eval_gate/2" and the evaluators listed in `docs/DATA_ACCOUNTING.md` §5.3. **No manuscript file
was edited, and nothing in this section asks for a manuscript edit.** Every sentence and cell stays as it stands. The
evidence for each route is below.

| route VERIFY found | what eval_gate/2 does now | quoted numbers that came through it | manuscript |
|---|---|---|---|
| 1b-i `arc_recall_eval.py --matches` checked `--weights`, not the weights that made the predictions | every matches file records `weights_sha256`; a file that records none, or another checkpoint's, is refused before anything is written | none: the one `--matches` run was VERIFY's demonstration, and its output was not kept | none |
| 1b-ii `carry()` trusted any block | a held-out block is carried only if its checks are non-empty and complete, the dump's recorded sha256 set equals the checked one, and the patients it scored equal the tested set (digest) | none found (audit below) | none |
| 1b-iii keys used as given (`implant:<case>_v<k>`, `{key, case}`) | every key is canonicalised and resolved to a person; an implant key maps to its source CT; one that names no person raises; a dict's `key` never hides its `case` | none: the one route (`learning_embed.py`) scored only the v9 selection split, which is refused anyway | none |
| 1c: 29 weight-loading evaluators made no gate call | all 29 gate before scoring and stamp their outputs | Figure 2 (`fig2_occlusion_clean`, `fig2_heldout_embed`); verdicts unchanged | none |

### 5.1 Grid reproduction (job 40436261; staged code eval_gate.py md5 2b0c9e05…, the same as this checkout)

Each call ran through its own command line against the grid lineage store and the real files. The pass/raise column
is the job's `RESULT` line; the numbers are from `out/`.

| call | input | result |
|---|---|---|
| R1a | void curve's `matches.json` (dc_P_pooled's predictions) under `--weights pooled=detect_v5z` (VERIFY's demonstration) | UnverifiedDump; no output. It was 456 leaked cells labelled held out |
| R1b | the unseen run's own `matches.json`, its own four weights | UnverifiedDump: written before eval_gate/2, it records no sha256 |
| R1c | the same, `--not-held-out` | passes; the curve's `eval_gate.held_out` is false and carries the reason |
| R1d | a copy of that file bound the eval_gate/2 way (sha256 from the four weight files), then (i) its own weights, (ii) `--weights pooled=detect_v5z` | (i) passes, and **1,824 of 1,824 curve cells equal the published unseen curve** (`out/R1d_i_cells.json`); (ii) UnverifiedDump: `pooled` was made by 13f17d8c…, and `--weights` is 797de71a… |
| T1 | a hand-written block `{held_out: true, checks: []}` on dc_P_pooled × the 17 arc subjects | UnverifiedDump |
| T2 | a genuine eval_gate/2 block of detect_v5z (held out for the 17) pasted onto dc_P_pooled's dump | UnverifiedDump, "another checkpoint"; control: the same block on detect_v5z's own dump is carried |
| T2b | dc_P_pooled's genuine block on the 40 unseen, pasted onto its dump of the 17 | UnverifiedDump, "another evaluation set" (17 vs 40 patients, digests differ) |
| T3, T3b | the real pre-gate dump `or_ready/lodo/sweeps/lodo_carm__cobra_test.json`; then with today's sha256 written in | UnverifiedDump (records no sha256); with the sha: gated at scoring, SeenInEvaluation (27 of 27 in rx_lodo's VAL) |
| scorers | `lcurve_score.py`, `count_from_sacrum_eval.py` on that dump | UnverifiedDump; no output |
| C | control: `realxray_eval.py` (eval_gate/2) rx_lodo_carmlspine_1024 on C-ArmLSpine test, then `lcurve_score.py` on it | held out (28 patients); `lcurve_score` carries it. Its block moved onto dc_P_pooled's weights, onto the 17 arc subjects, with one key deleted, or with `weights_sha256` removed: UnverifiedDump each time |
| K1 | `learning_embed`'s route over the real v9 val split (2,811 cases) with `~/patient_keys_v9.json` | 164 of the encoder's TRAIN persons seen, as with every case keyed by name. The old route saw 73. 194 map entries are `implant:` keys; 0 map entries name no person; 0 unkeyed |
| K2–K6 | `implant:0001_v0` vs model_scal_pt_render; `{key: ts:s9999, case: TS_s0585}` vs dc_P_pooled; `implant:zzz9_v0`; `ts:bogus`; control `carmlspine:case100` vs rx_lodo | SeenInEvaluation (ctsp:0001); SeenInEvaluation (ts:s0585); UnkeyedEvalItem; UnkeyedEvalItem; held out |
| learning_embed | the real v9 bank, map and encoder | SeenInEvaluation: 1,776 of 1,776 val persons in its VAL set, 164 in its TRAIN set (VERIFY G17b saw 1,685 of 1,804 and 73) |
| Figure 2 | `fig2_occlusion_clean.py` on the v9 val draw; `fig2_heldout_embed.py` on case42, case121, case136 | SeenInEvaluation before a crop is streamed; the three L6 patients held out for the v9 encoder (overlap 0), and the embedding is written |

Nothing was written under `or_ready/arc`, `or_ready/lodo`, `or_ready/eval_gate/arc_unseen` or `results/fig6` (the
job's final `find`).

### 5.2 Why no quoted number moves

- **--matches.** No quoted number was produced by `--matches`. The unseen curve, re-aggregated from its own
  predictions under the binding, reproduces every cell. No manuscript sentence quotes the curve (§1.3; EVAL_LEAKS item 1).
- **Blocks already written.** Six result files under `results/` carry a gate block at the top level
  (`out/existing_blocks_audit.json`): the three unseen-arc files, `leaks/render_vs_film_unseen_rerun.json`,
  `leaks/a3a_unseen/a3a_rows_meta.json` and `smoke_gate/rx_lodo__carm_test.json`. None is hand-written or
  transplanted:
  - every one has non-empty checks, each with a checkpoint sha256;
  - where the file names its weights, the checked paths equal them;
  - where it records what it scored, the patient count equals the count checked (40, 40, 40, 28).
  - The quoted pre-gate dumps carry no block, and CHK-9 decided their rows from lists, not from a block.
- **The headline detector's dump.** The 21 `lodo_detector_on_carm` rows (a1: 80.5, 90.6, 76.8, 83.9 %) come from the
  pre-gate dump `sweeps/lodo_carm__carm_test.json`. It records no sha256, so the question is whether it was made by the
  file now at its path. The control C re-scored the same frames with that file (sha256 f6fe6b97…)
  (`out/samefile_lodo_carm.json`):
  - raw predictions are identical to four decimals on 55 of 56 frames, case118 included. case118's oblique was renamed
    from LAT to OBL in the 2026-09-23 export, and its predictions are unchanged.
  - The one exception, case100_LAT, differs by 1e-4 in one score (0.1827 against 0.1826) and 0.1 px in one box, both
    below 0.25. That is floating-point nondeterminism across nodes.
  - So the numbers stand, and there is now evidence from outside the gate that the path-keyed verdict described the
    right weights. The C dump's own pooled numbers are identical to the gated smoke run of 2026-09-23.
- **Keys.** Figure 2 was analysed with implant renders re-keyed to their source CT by `figure2_analyse.py`. The
  gate's own resolution now agrees with it set for set: `eval_sets.json` rebuilt under eval_gate/2 gives v9_val 1,776
  persons and v9_val_clean 1,612, the same keys as before. The undercount (73 against 164) was in the gate's report on a
  split that was refused in either case.
- **The Figure 2 evaluators.** The caption already calls the space the "checkpoint-selection split". The occlusion
  panel's draw is refused unless declared, as EVAL_LEAKS already records it (LEAKED, NUMBERS:L45). The "never-seen" L6
  patients pass the gate on their own, without the renderer's `held_out: true` flag.

### 5.3 `eval_sets.json` regenerated (jobs 40436056, 40436260)

- It was rebuilt with eval_gate/2 from the rendered `anglesweep_unseen/SET_INFO.json`: 17 sets, **0 keys added or
  removed in any set, 0 unkeyed, 0 failed** (`out/eval_sets_diff.json`).
- It is installed where CHK-9 reads it (`or_ready/eval_gate/eval_sets.json`), with the eval_gate/1 file kept as
  `eval_sets.eval_gate1.json`. The repo copy `results/eval_gate/eval_sets.json` is replaced with it.
- Its `source` strings name the staged code directory, whose `SchwingNet/` is a link to the grid clone's.
- CHK-9 verdicts cannot change, because the keys are identical.

### 5.4 Not manuscript: what eval_gate/2 now requires of the files the manuscript quotes

- **A dump that records no `weights_sha256` is refused by every scorer unless declared.** No `realxray_eval` or arc
  dump written before 2026-09-24 records one. A `level_prototype` output records every model's sha256 except the
  head's, so a prototype run that used a head is refused too, and one without a head is gated by the recorded
  sha256s. The numbers and their CHK-9 verdicts stand. What changes is that re-running any scorer
  over these dumps first needs the evaluator re-run, which now records the sha256, or a declaration.
  - The dump-derived families in `quoted_results.json`, with their row counts: lcurve 112, contribution 101,
    count_only 86, fig3_scored 58, coupling 27, carm_cv_naming 23, lodo_detector_on_carm 21, counting 11,
    carm_zeroshot 9, carm_cvday_naming 5, pooled_vs_lodo_carm 4, carm_cv_oracle 1.
  - Only lodo_detector_on_carm was re-checked against today's weight file (§5.2).
- **The files §3a and the arc work quote were written under eval_gate/1.** Their blocks pass the audit in §5.2, but
  eval_gate/2 carries them only after a re-run. They are `leaks/render_vs_film_unseen_rerun.json`,
  `leaks/a3a_unseen/a3a_rows_meta.json`, `results/arc/recall_vs_angle_unseen/{recall_vs_angle,prior_check,subjects}.json`
  and the device-card sidecars `docs/devices/eval_gate/*.json` (`tools/device_fit.py gate`, CPU).
- **`tools/head_mixed_length.py` and `tools/head_dual.py` were not changed.** They write
  `json.dump({"eval_gate": gate, ...})`, which records no sha256. They were left alone because the held Figure 6
  chain runs them (`fig6_train.sh`, `d1_train.sh`). A scorer that carries their output will refuse it until each
  writer calls `EG.stamp(result, gate)`.
- **The grid clone's `tools/eval_gate.py` is still eval_gate/1** (md5 0b00cccc…), for the same reason. eval_gate/2
  runs from `or_ready/eval_gate/closure/bypass/code/`.
- **Residual.** A check with no checkpoint (a model fitted inside the evaluator: device-card folds, a head fitted in
  the run) has no sha256 to bind. It is bound by its key digest alone.
- **Residual.** A person-id shape check says a key could name a person of its corpus, not that the person exists:
  `ts:s9999` fits the TotalSegmentator shape. No release here ships a registry of every subject.


---

## 6. Resume of 2026-09-24 10:50: the checkpoint verified, item 1 requeued under eval_gate/2, and what the manuscript drive has already taken

Written on the resume after Greg's request of 2026-09-24 (the acquisition-space review, `lit/acquisition_space_review_2026-09-24.{pdf,txt}`, commit 5d4b887). **Nothing in items 1-3 depends on a training hyperparameter or on how the training corpus samples the acquisition space**: item 1 is a re-score of fixed detectors on a fixed real acquisition, item 2 is a key-alias trace on two fixed banks, item 3 is a carry-forward of two held-out re-derivations. So no job here was requeued because of the review; the review's integration is the `review-integration` workflow's. The one thing it can take from here: the held-out angle data its section 2 argument (oblique views under-sampled; the plateau as sampling-density saturation) would cite are `closure/case134_sweep_eg2/` (one real rotational acquisition, four detectors) and the 40-subject unseen render curve (`results/arc/recall_vs_angle_unseen/`; eval_gate/2 copy `closure/bypass/out/R1d_i/`), not the void 17-subject curve.

### 6.1 The checkpoint, re-read

| item | grid job | state on the grid | local copy |
|---|---|---|---|
| 1 case134 re-score | 40431371 | COMPLETED 0:0, 13 min | `closure/case134_sweep/`, md5 equal file for file (`case134_sweep.json` d9d8cb91…, the four `gate_check_*.json`) |
| 2 v8 / v9 overlap | 40431372, 40431408 | COMPLETED 0:0 | `closure/v8_overlap/{v8,v9}_overlap.json`, md5 equal (6e684b40…, 6d2eddac…) |
| 3a, 3b carry-forward | 40429839 (3a) | files as quoted | `leaks/render_vs_film_unseen_rerun.json#conf_0.05` (+31.68 pp [20.99, 45.40]; 16 : 0; p 3.05e-5); `leaks/card_gain_unseen.json#patient_held_out_12` (+0.01928 [0.00764, 0.03256]; p 0.00439) |

Every number in sections 1-4 re-reads from those files unchanged.

### 6.2 Item 1 requeued under eval_gate/2 (grid job 40436881, CPU, 10 min 55 s, COMPLETED 0:0)

Why: the 07:18 re-score ran the grid clone's tools, which are still eval_gate/1 (section 5.4), so its dump records no `weights_sha256`, and the render curve it compared against (`or_ready/eval_gate/arc_unseen/recall_vs_angle.json`, eval_gate/1) is refused by `carry()` under eval_gate/2. The gate changed under the item, so its score stage was run again, not re-labelled.

What ran: `closure/jobs/closure_case134_eg2.sh` (on the grid at `or_ready/eval_gate/closure/closure_case134_eg2.sh`), the same two steps as `closure_case134.sh`, from the STAGED eval_gate/2 code (`closure/bypass/code`; `tools/eval_gate.py` md5 2b0c9e05…, `tools/case134_sweep.py` e229200a…, both the same as this checkout; the grid clone left alone for the held Figure 6 chain), with `--render-curve` = `closure/bypass/out/R1d_i/recall_vs_angle.json`, the eval_gate/2 re-aggregation of the unseen run's own predictions (section 5.1: 1,824 of 1,824 cells equal to the published unseen curve). Outputs in a NEW directory, `closure/case134_sweep_eg2/` (grid and local), with the job log `c134_eg2_40436881.out`; `closure/case134_sweep/` and `or_ready/arc/case134_sweep/` kept.

Result:

- Gate alone (eval_gate/2 `check`), per arm: pooled, lodoA, lodoB, real_lodo all rc 0, HELD OUT; `SEEN_ARMS=none`, so no arm was declared.
- The dump: `eval_gate` gate_version eval_gate/2, held_out true, overlap 0, unresolved 0, 4 checks, each with its `checkpoint_sha256` (13f17d8c…, bfa05c73…, 9f7f2ff5…, f6fe6b97…), its `eval_keys` (one: case134) and `eval_digest`; `weights_sha256` recorded for the four arms; `held_out_by_arm` all true.
- The render curve was CARRIED, not refused: `render_curve_eval_gate` eval_gate/2, held out, overlap 0, unresolved 0, 40 subjects; `render_curve_md5` da33baef… (the R1d_i copy; the 07:18 run read 05ff586c…, the eval_gate/1 file).
- **Every number is identical to the 07:18 run**: `detectors` equal field for field (`DETECTORS_IDENTICAL_TO_0718_RUN True` in the log); all 76 per-bin rows of the render comparison in `case134_sweep.md` equal; no other top-level field differs. Body recall over the spin at 0.25 / 0.74 stays pooled 93.6 / 78.1 %, lodoA 37.2 / 29.1 %, lodoB 29.6 / 23.5 %, real_lodo 49.5 / 49.4 %.
- Manuscript: still nothing to change (section 1.3). The section 5.4 residual "the arc work's files were written under eval_gate/1" is closed for item 1; it stays open for `leaks/render_vs_film_unseen_rerun.json` (3a) and for `results/arc/recall_vs_angle_unseen/` itself, whose eval_gate/2 twin is `closure/bypass/out/R1d_i/` (not copied over the published file: that directory is the arc workflow's).

### 6.3 What the manuscript drive (REVISION_LOG2.md, 08:39; working tree, uncommitted) has taken from sections 1-4, against the files as they stand now

Read on the resume with the quoted "as it stands" text searched verbatim in every file. Line numbers are of the working tree at 10:50.

| section | replacement | status | where it now stands |
|---|---|---|---|
| 2.4 Table 1 note c | as written | **applied** verbatim | `tables/tab_corpus.tex:69` |
| 2.4 NUMBERS.md:308 ("Numbers deliberately absent") | rewrite | **not applied**; the old line stands at `NUMBERS.md:308` | the drive's convention (NUMBERS.md "Revision 2", line 398 on) is to add rows and mark old rows SUPERSEDED, not to rewrite; do that here |
| 2.4 NUMBERS.md:112 append | append | **not applied**; `NUMBERS.md:112` unchanged | same |
| 2.4 Methods optional clause | optional | **declined** (REVISION_LOG2: "+14 words, not taken for length"); `sections/methods.tex:58` unchanged | none needed |
| 3a Table S2 rows | as written | **applied** verbatim | `tables/tab2_detection.tex:68-69` |
| 3a Table S2 notes a and f | as written | **applied** verbatim | `tab2_detection.tex:75`, `:80` |
| 3a Supplement "Which source carries the detector" | as written | **applied** verbatim (the section also gained body-convention brackets from REVIEW2_RSNA) | `supplement.tex:74-77` |
| 3a NUMBERS.md:113, :244, :296 | rewrite | **superseded by the drive's own row** `NUMBERS.md:434` (99.4 vs 67.7, +31.7 [21.0, 45.4], 16 vs 0; 0.25 row); the old rows :113, :244, :296 still print 27.5 / 233 / 25 spines and are not marked SUPERSEDED | mark them SUPERSEDED 2026-09-24 pointing at :434 |
| 3b Supplement "Image-formation terms" + deleted sentence | as written | **applied** verbatim; the deleted sentence is gone | `supplement.tex:50-55` |
| 3b Table S1 row and note | as written | **applied** verbatim (generator `tools/make_supp_device_table.py` updated) | `tables/tabS1_device_terms.tex:24`, `:27` |
| 3b Table 1 Geneva and Ljubljana cells, note k | as written | **applied** verbatim | `tab_corpus.tex:60-61`, `:77` |
| 3b Figure S3 legend | 58-word caption | **applied** in the supplement's printed legend | `supplement.tex:130`; `figures/figS2.caption.txt` (figure owner's file) still reads "(c) Held-out R² gain over uncalibrated physics per fold" and lacks "of the same projection" being removed: the print and the caption file differ, and unlike Figures 1 and 4 (`main.tex:127`, `:154`) no comment says so |
| 3b NUMBERS.md:134, :140, :141, :245, :292 | rewrite / retire | **superseded by** `NUMBERS.md:435` (12 folds +0.019 [0.008, 0.033]; within-subject 0.056); the old rows stand unmarked, :140 and :245 still carry the retired device-level $P=.13$ | mark SUPERSEDED; the retired device-level test needs the mark most |
| 3c Table 3 (printed Table 4) note f | as written | **applied** verbatim | `tables/tab3_naming.tex:89` |
| 3c Table 1 role cells (optional) | "checkpoint-selection split" | **applied** as "level bank; checkpoint selection" | `tab_corpus.tex:51-53` |
| 4 Holm: supplement $P=.009$ | as written | **applied** | `supplement.tex:71`; the family's first member is now the v9 zero-shot run (Holm 5.4e-22), as section 4 anticipated |
| 4 NUMBERS.md:125, :128, :243 | rewrite | **superseded by** `NUMBERS.md:436` (raw 1.3e-22, 3.1e-5, 0.0078, 0.0044; adjusted 5.4e-22, 9.2e-5, 0.0088, 0.0088); old rows :125, :128, :243 still print Holm 0.0078 / .008 and are unmarked | mark SUPERSEDED |
| 1.3 optional: `figS4.record.json#not_shown_and_why` | reword | **not applied** (figure owner's file, line 1387 unchanged) | the reason should now name `closure/case134_sweep_eg2/` |

Not manuscript, still as section 2.4 listed them: `results/a5.json#v2_statement` ("v8's known leak is VerSe"), `results/RIGOR_FIXES.md` A5, `docs/MODEL_CARD.md:168`, `docs/DATASHEET.md:267`, `results/rare_class/split_plan.md` "Model exposure", EVAL_LEAKS.md L4.

### 6.4 Still open after this resume, and whose

- The unmarked NUMBERS.md rows above (paper-six-figures / manuscript-drive): thirteen lines, all listed.
- `figures/figS2.caption.txt` and `figures/figS4.record.json` (figure owners).
- eval_gate/2 re-runs of `leaks/render_vs_film_unseen_rerun.json` (`rigor_fixes.py a3a-rows`, CPU) and of the published unseen arc curve, so that scorers can carry them without a declaration (section 5.4); their numbers are not in question (sections 3a, 5.1).
- Plain-film naming has no held-out number until the Figure 6 model is scored on the G3 test films (section 3c); unchanged, and outside this closure.
- `closure/cv_v9/` (EVAL_LEAKS U1, the C-ArmLSpine fold models) is another item's: `carmcv9i` 40431706 and `carmcv9pre` 40436580 arrays COMPLETED, `cv9icollect` 40436581 COMPLETED, `cv9iprerep` 40436575 FAILED rc 3; no result file has reached `closure/cv_v9/` locally. Not touched here.

---

## 7. C-ArmLSpine naming re-established on the v9 lineage (EVAL_LEAKS U1): every quoted row, old beside new

Written 2026-09-24 11:00 by the U1-closure item. **No manuscript file was edited.** Every number below is read from
`results/eval_gate/closure/cv_v9/` (`CV_V9.md` is the machine-written row-by-row table; `cv_v9.json` its source), and
the text as it stands is copied verbatim from the files at 10:30 today. Where the manuscript carries a
`\PENDING{G5}{C-ArmLSpine CV on the v9 lineage...}` macro, the replacement is the sentence or cells to put in its place.

### 7.0 What ran, and what the gate says

57 of the 58 UNRESOLVED quoted rows traced to `allspine_v2_r1`, whose training bank was deleted (U1). The fold models
were re-trained with **one change, the initialisation**: `slurm/carmlspine_cv_v9init.sh` (job 40431706, folds 0-4) and
`slurm/carmlspine_cv_day_v9init.sh` (40431707, day folds 0-2) fine-tune from the lineage-complete `allspine_v9` encoder
on the shipped folds' own merged banks (`~/carm_cvmix<K>_fov96_ctx`, `~/carm_cvdaymix<K>_fov96_ctx`, written before the
shipped models), with the shipped epochs (15), learning rate (1e-4), augmentation (2), seeds, mixed-length head and
prototype defaults, then score the shipped fold directories; per case fold they also run the coupling prototype
(`--dump-posterior`, the held-out sacrum detector) and zero-shot `allspine_v9` on the fold's whole frames.

**Two truths.** The shipped fold directories are symlinks into the C-ArmLSpine export, which was rewritten on
2026-09-23 (case118's oblique frame renamed, case134 added) after every quoted number was scored. So
`closure/cv_v9/prerepair_fold_dirs.py` (job 40436575) mirrored every fold directory link for link onto the kept
pre-repair export, and `slurm/carmlspine_cv_v9init_prerepair.sh` (40436580, tasks 0-7) scored the same new models on
it, with the shipped models re-run beside them as declared controls. **"pre"** (the export as it was) is the
like-for-like replacement: old and new differ by the initialisation alone. **"rep"** (the export as it stands) is
reported beside every pre number in `CV_V9.md`. The k-vertebra crops had to be regenerated for the mirror; they
match the shipped crops except that case13_LAT is one crop short at every k (case fold 0, day fold 2), so the
k = 1..5 denominators are a few items smaller than the old ones (662 against 667 at five in field, and so on).

**Collect.** `closure/cv_v9/collect_cv_v9.sh` (40436581) ran the four coupler passes and `coupling_report.py` over
both truths and the `rigor_fixes.py a4 / a7 / a9` twins, then died in `closure_cv_v9.py` on a list-valued JSON;
`closure_only.sh` re-ran that one step (40436862, and 40436983 after the zero-shot ladder), `zs_v9_kfield.sh`
(40436982) scored zero-shot `allspine_v9` at k = 1..5 on every fold, and `cv_v9_extras.sh` (40436901) computed the
count-versus-classifier matrix and the paired zero-shot-versus-fine-tuned reading.

**The gate.** Every new score file was written behind `tools/eval_gate.py` inside `level_prototype.py` with no
declaration; every family in `cv_v9.json` reads **held out, overlap 0, unresolved 0** (150 checks for the case folds,
90 for the day folds, 25 for zero-shot). The old families are refused by the strict gate (`UnresolvedLineage`, 60
and 36 unresolved links) and were read for the "old" column only under a declared reason. One caveat, not a leak:
the grid clone's `tools/eval_gate.py` is still eval_gate/1 (md5 0b00cccc; it is held there for the Figure 6 chain,
§5.4), so the new dumps carry eval_gate/1 blocks without `weights_sha256`; a scorer under eval_gate/2 will refuse them
until the evaluators are re-run under it or the read is declared. The verdicts themselves are the same under both.

**Controls (`CV_V9.md` §7).** The shipped fold models re-run with today's code on the pre-repair mirror reproduce the
shipped whole-frame score files item for item in 7 of 8 folds (day fold 0: 587 of 588 items, one call flipped,
floating-point nondeterminism across nodes); at k = 1..5 they differ by case13_LAT's missing crop and a handful of
regenerated-crop items. On the repaired export the shipped models move by 3-4 items per fold: the truth moved, the
models did not.

**Code.** `closure_cv_v9.py` imports the shipped estimators (`rigor_fixes.prop_ci`, `paired_ci`,
`cluster_level_wilson`, `carmlspine_pool_scores.boot`): case-clustered bootstrap, 2,000 resamples, seed 0. The
interval to print follows Table 4 note g: Wilson on the design-effect-adjusted n where the cell is flagged
`ceiling_regime`, the percentile interval otherwise; both are given below.

### 7.1 What moves, and which claim changes

| quantity (pre-repair truth) | old (allspine_v2_r1, UNRESOLVED) | new (allspine_v9, HELD OUT) | moves? |
|---|---|---|---|
| lateral, whole frame, case-grouped | 98.2 % (606/617); 3 of 141 cases erring; Wilson on n_eff [94.6, 99.4] | **97.4 % (601/617)**; 4 cases; Wilson on n_eff [93.2, 99.0]; percentile [94.5, 99.5]; BCa [93.2, 99.4] | inside the old interval; 5 more errors, 3 of them to thoracic names (L4→T3, L5→T4, L3→T2) |
| AP, whole frame, case-grouped | 96.7 % (610/631); Wilson [92.7, 98.5] | **96.4 % (608/631)**; 7 of 142 cases; Wilson [92.5, 98.3]; percentile [93.3, 98.6]; BCa [92.8, 98.4] | no |
| lateral, five / four / three / two / one in field | 97.0 / 95.7 / 92.9 / 89.5 / 72.8 % | **95.8 (634/662) / 94.8 (999/1,054) / 93.1 (1,079/1,159) / 89.9 (870/968) / 74.8 % (451/603)** | five-in-field −1.2, one-in-field +2.0; all inside the old intervals |
| lateral, day-grouped, whole frame | 92.5 % (571/617); [87.7, 96.4] | **92.1 % (568/617)**; 12 of 141 cases; percentile [87.5, 96.0]; BCa [86.7, 95.6] | no; **still below zero-shot 96.4 %** (paired −4.4 pp [−9.1, +0.2]; 4 cases better, 10 worse) |
| AP, day-grouped, whole frame | 96.7 % (610/631) | **94.8 % (598/631)**; 9 cases; Wilson [90.1, 97.3]; percentile [91.0, 98.0] | −1.9 pp, inside the old interval |
| lateral, day-grouped, three / one in field | 87.6 / 66.6 % | **87.7 (1,016/1,159) / 71.8 % (433/603)** | one-in-field +5.2 |
| zero-shot, lateral, three / one in field (Table 4's pending zero-shot row) | first run (zeroshot2): 86.9 (1,010/1,162) / 63.1 % (381/604) | **v9: 83.7 % (970/1,159)** [79.6, 87.5], 59 of 142 cases erring; **63.8 % (385/603)** [59.8, 67.9], 118 cases; the whole-frame 96.4 % (595/617) is reproduced | new cells (the manuscript quoted none); the v9 zero-shot is 3.2 points weaker than the first run with three bodies in view |
| fine-tuned minus zero-shot, lateral, same 617 vertebrae | not computed on a clean lineage | **+1.0 pp [−1.9, +4.0]**; 4 cases better, 2 worse; exact sign p 0.69 | **the claim that fine-tuning improves lateral naming is not supported**; what fine-tuning adds is the AP view: **+52.6 pp [+44.1, +61.3]**, 78 : 2 cases, p 5e-21 |
| abstention, lateral whole frame | answered 83.1 %, exact on answered 98.4 % (505/513) | **answered 81.5 % (503/617), exact on answered 98.8 % (497/503) [97.1, 100.0]**; at 0.9 answers 57.5 % at 99.7 %, at 0.95 answers 47.2 % at 100.0 % (291/291) | no |
| truth boxes, lateral whole frame (complete coverage) | 93.6 % (633/676) [90.0, 96.8] | **94.2 % (637/676)** [90.9, 97.0]; within one 99.1 % | no |
| coupling at 0.74, 1,009 counted bodies, 130 cases | classifier 98.4 % (993), count 97.0 % (979), coupled 98.6 % (995); coupled − count +1.6 [0.0, 3.8]; coupled − classifier +0.2 [−1.7, 2.1] | **classifier 97.7 % (986) [95.9, 99.2], count 97.0 % (979) [94.2, 99.2] (identical: the count uses no level model), coupled 98.2 % (991) [96.5, 99.5]; coupled − count +1.2 [0.0, 3.2]; coupled − classifier +0.5 [−1.5, 2.4]** | no: the count is unchanged, the coupled call still sits above the classifier and the count without a significant margin |
| disagreement and the stop signal at 0.74 | 12/233 frames (5.2 %), 34/1,066 bodies; agree 982/983; disagree coupled 13/26, classifier 11/26; flag on 4 of 5 error frames, 17 of 225 correct; unflagged 921/922 | **13/233 (5.6 % [2.6, 9.2]), 42/1,066 (3.9 % [1.8, 6.5]); agree 975/980; disagree coupled 16/29, classifier 11/29, neither 2; flag on 5 of 6 error frames, 16 of 224 correct (7.1 %); unflagged 921/922; flagged anchored 23/233 (9.9 %)** | no |
| L6 calls at 0.74 on anchored agreed five-lumbar frames | 4 of 233 (case106_AP, case139_AP, case139_LAT, case44_LAT), all with a stop | **3 of 233 (case139_AP, case139_LAT, case44_LAT), 2 cases, all with a stop**; case106_AP is now ordinary | one fewer false L6 |
| the three one-labeller L6 patients | coupled agrees with the L6 read on 1 of 5 L6 bodies, classifier 0 of 5; at 0.74 one L6 call on 4 anchored frames (case42 LAT), 2 of 6 frames unanchored | **identical: 1 of 5, 0 of 5; 1 of 4 anchored (case42 LAT, flag "disagreement")** | no |
| Figure 4d (case42 lateral, fold 2, det74) | classifier L2 0.89, L3 1.00, L4 0.96, L5 0.92, sacrum 0.02; ordinary −2.7851, L6 −0.7550; margin 2.0301 vs tau 1.6524; call L6 | **L2 0.93, L3 0.99, L4 1.00, L5 0.66, sacrum 0.01; ordinary −3.0579, L6 −1.1065; margin 1.9514 vs tau 1.583; call L6; 4 of 4 named bodies differ from the count** | the drawn rows do not move; the posteriors and margin do |
| Figure 4b (case11 lateral, fold 3, three in field) | L2 0.99, L3 0.99, L4 0.99, none | **L2 0.99, L3 0.96, L4 0.98, none**; panel count 1,079 of 1,159 (93.1 %) | two drawn posteriors and the denominator |
| Figure 5 "planning accuracy 98.22" (`FIGREC:figure5/03`) | 98.2 % (606/617) | — | already retired: Figure 5 was rebuilt on the frozen exact test (NUMBERS.md:46, SUPERSEDED) |

**Claims that change.** (1) Every fine-tuned number moves by 0-2 points and stays inside the old interval; the
headline "98.2 %" becomes 97.4 %, "606 of 617" becomes 601 of 617. (2) On the lateral view the fine-tuned model is
now one point above the zero-shot one, not significantly (4 : 2 cases); the manuscript must not credit fine-tuning
with better lateral naming. What it adds is the anteroposterior view, 52.6 points. (3) Day-grouped fine-tuning
remains below zero-shot (92.1 against 96.4 %), so REVIEW2_RSNA B4 applies: the limitation belongs in
`discussion_limits.tex` (§7.2, item 8). (4) The zero-shot cells the manuscript already quotes (595/617, 276/631,
+54.3) are reproduced exactly by the closure's own re-score of the same encoder on the pre-repair frames
(`pre:zs_v9head`).

### 7.2 The manuscript: text and cells to replace

Intervals in the sentences below are Wilson on n_eff where Table 4 note g applies (lateral and AP whole frame,
case-grouped; AP whole frame, day-grouped) and percentile otherwise; the BCa twins are in `CV_V9.md`.

**1. `main.tex:69` (Key Point 2).** As it stands:

```
\item Counting up from the detected sacrum named 979 of 1,009 bodies on anchored lateral and anteroposterior frames (97.0\,\%); fine-tuned naming, with three vertebrae in view and coupled with the count, is \PENDING{G5}{C-ArmLSpine cross-validation on the v9 lineage}.
```

Replace with:

```
\item Counting up from the detected sacrum named 979 of 1,009 bodies on anchored lateral and anteroposterior frames (97.0\,\%); fine-tuned on the other cases, SchwingNet named 601 of 617 lateral vertebrae (97.4\,\%), 1,079 of 1,159 with three in view (93.1\,\%), and, coupled with the count, 991 of the 1,009 (98.2\,\%).
```

**2. `main.tex:82` (Abstract, Results).** As it stands (fragment):

```
fine-tuned, \PENDING{G5}{C-ArmLSpine CV on the v9 lineage}. On anchored frames the count from the detected sacrum named 979 of 1,009 bodies (97.0\,\%).
```

Replace with:

```
fine-tuned on the other cases, 601 of 617 lateral (97.4\,\%; 93.2, 99.0) and 608 of 631 anteroposterior (96.4\,\%), and 568 of 617 lateral with whole acquisition days held out (92.1\,\%). On anchored frames the count from the detected sacrum named 979 of 1,009 bodies (97.0\,\%) and the coupled call 991 (98.2\,\%).
```

**3. `sections/results.tex:55-56`.** As it stands:

```
\PENDING{G5}{C-ArmLSpine CV on the v9 lineage: fine-tuned lateral and anteroposterior, case- and day-grouped; three
and one lateral bodies in view, zero-shot and fine-tuned (Figure 4b)}
```

Replace with:

```
Fine-tuned on the other cases (five case-grouped folds), it named 601 of 617 detected lateral vertebrae (97.4\,\%;
93.2, 99.0; four of 141 cases erring) and 608 of 631 anteroposterior (96.4\,\%; 92.5, 98.3): a paired gain over
zero-shot of 1.0 point on the lateral view (\(-1.9\), 4.0; four cases better, two worse) and 52.6 points on the
anteroposterior (44.1, 61.3; 78 better, two worse). With three lateral bodies in view it named 1,079 of 1,159
(93.1\,\%; 89.2, 96.2) against 970 of 1,159 zero-shot (83.7\,\%; 79.6, 87.5), and with one body 451 of 603
(74.8\,\%; 70.9, 78.7) against 385 of 603 (63.8\,\%; 59.8, 67.9) (Figure~\ref{fig:exposure}b). With acquisition days held out instead of cases, fine-tuning named 568 of
617 lateral vertebrae (92.1\,\%; 87.5, 96.0), 4.4 points below zero-shot (\(-9.1\), 0.2; four cases better, ten
worse), and 598 of 631 anteroposterior (94.8\,\%; 90.1, 97.3).
```

**4. `sections/results.tex:58-59`.** As it stands:

```
(Figure~\ref{fig:exposure}c); \PENDING{G5}{C-ArmLSpine CV on the v9 lineage: classifier and coupled call on those
bodies, against the count and the classifier; stop signal; L6 calls (Figure 4d)}.
```

Replace with:

```
(Figure~\ref{fig:exposure}c); the classifier alone named 986 of them (97.7\,\%; 95.9, 99.2) and the coupled call
991 (98.2\,\%; 96.5, 99.5), 1.2 points above the count (0.0, 3.2) and 0.5 above the classifier (\(-1.5\), 2.4).
Classifier and count disagreed on 13 of 233 anchored frames (5.6\,\%; 2.6, 9.2); where they agreed the call was
right on 975 of 980 bodies, where they disagreed the coupled call was right on 16 of 29 and the classifier on 11.
The stop signal fired on five of the six anchored frames with a coupled error and on 16 of 224 fully correct
frames (7.1\,\%); unflagged coupled calls were exact on 921 of 922 bodies. Three of 233 anchored five-lumbar frames
were called L6 (two cases), each with a stop, and on the three patients one CT reading calls six-lumbar the coupled
call agreed with that reading on one of four anchored frames (Figure~\ref{fig:exposure}d).
```

**5. `tables/tab3_naming.tex`.** Each `\PENDING{G5}` cell spans several numbers; the rows below are one table row
per number, in the table's column order (measure; % (k/n); clusters (with an error); 95 % percentile; BCa).

Line 58, as it stands:
```
 & & lateral; three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with (zero-shot, `pre:zs_v9head`):
```
 & & lateral; three in field & exact level & 83.7 (970/1,159) & 142 (59) & [79.6, 87.5] & [79.4, 87.4] \\
 & & lateral; one in field & exact level & 63.8 (385/603) & 142 (118) & [59.8, 67.9] & [59.8, 67.7] \\
```

Line 59, as it stands:
```
 & the same; case-grouped folds\fnm{h} & lateral and AP; whole frame, three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & the same; case-grouped folds\fnm{h} & lateral; whole frame & exact level & 97.4 (601/617) & 141 (4) & Wilson [93.2, 99.0]\fnm{g} & [93.2, 99.4] \\
 & & AP; whole frame & exact level & 96.4 (608/631) & 142 (7) & Wilson [92.5, 98.3]\fnm{g} & [92.8, 98.4] \\
 & & lateral; three in field & exact level & 93.1 (1,079/1,159) & 142 (23) & [89.2, 96.2] & [88.5, 95.9] \\
 & & lateral; one in field & exact level & 74.8 (451/603) & 142 (94) & [70.9, 78.7] & [70.7, 78.5] \\
```

Line 60, as it stands:
```
 & the same; day-grouped folds\fnm{h} & lateral and AP; whole frame, three and one in field & exact level & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & the same; day-grouped folds\fnm{h} & lateral; whole frame & exact level & 92.1 (568/617) & 141 (12) & [87.5, 96.0] & [86.7, 95.6] \\
 & & AP; whole frame & exact level & 94.8 (598/631) & 142 (9) & Wilson [90.1, 97.3]\fnm{g} & [90.2, 97.5] \\
 & & lateral; three in field & exact level & 87.7 (1,016/1,159) & 142 (38) & [83.5, 91.6] & [82.5, 91.1] \\
 & & lateral; one in field & exact level & 71.8 (433/603) & 142 (99) & [67.6, 75.9] & [67.3, 75.7] \\
```

Line 73 (coupled, conf 0.74), as it stands:
```
 & & & classifier alone; coupled; each minus the other and minus the count; disagreement and stop-signal frames; L6 calls on five-lumbar frames & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & & & classifier alone, counted bodies & 97.7 (986/1,009) & 130 & [95.9, 99.2] & -- \\
 & & & coupled, counted bodies & 98.2 (991/1,009) & 130 & [96.5, 99.5] & -- \\
 & & & coupled minus count, percentage points & +1.2 & 130 & [0.0, 3.2] & -- \\
 & & & coupled minus classifier, percentage points & +0.5 & 130 & [$-$1.5, 2.4] & -- \\
 & & & frames where classifier and count disagree & 5.6 (13/233) & 132 & [2.6, 9.2] & -- \\
 & & & anchored frames with a stop signal & 9.9 (23/233) & 132 & [5.7, 14.5] & -- \\
 & & & five-lumbar frames called L6 (each with a stop) & 3 of 233 & 2 & no interval & -- \\
```

Line 75 (coupled, conf 0.25), as it stands:
```
 & & & classifier alone; coupled; disagreement frames & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & -- & -- & -- \\
```
Replace with:
```
 & & & classifier alone, counted bodies & 97.7 (1,122/1,149) & 139 & [95.8, 99.2] & -- \\
 & & & coupled, counted bodies & 97.1 (1,116/1,149) & 139 & [95.3, 98.8] & -- \\
 & & & frames where classifier and count disagree & 7.1 (19/266) & 142 & [3.8, 10.8] & -- \\
```

Line 78 (the three one-labeller L6 cases), as it stands:
```
 & three C-ArmLSpine cases read as L6 by one labeller\fnm{e} & whole frame; conf 0.25 and 0.74 & agreement with that read on the L6 body (coupled; classifier); anchored frames called L6 & \PENDING{G5}{C-ArmLSpine CV on the v9 lineage} & 3 & no interval & -- \\
```
Replace with:
```
 & three C-ArmLSpine cases read as L6 by one labeller\fnm{e} & whole frame; conf 0.25 and 0.74 & agreement with that read on the L6 body: coupled 1 of 5, classifier 0 of 5 (both operating points); anchored frames called L6 at 0.74 & 1 of 4 & 3 & no interval & -- \\
```

Footnote h, last sentence, as it stands:
```
The case- and day-grouped fold models, first fine-tuned from that earlier encoder, are being re-run from the latest one.
```
Replace with:
```
The case- and day-grouped fold models are fine-tuned from the latest encoder on the other folds' cases; a first run from the earlier encoder gave 606/617 lateral case-grouped and 571/617 day-grouped and is not used.
```

Footnote d already describes the coupling; no change. The count-from-the-sacrum rows (lines 65-70) and the
"count alone, counted bodies" rows (72, 74: 979/1,009 and 1,104/1,149) are CLEAN and identical in the re-run.

**6. `tables/tab3_naming.md` (twin) and `tab3_naming.sources.md`.** Row 7 `98.2 (606/617) | 141 (3) | Wilson (g)
[94.6, 99.4]; percentile [95.7, 100.0] | [95.0, 99.5]` becomes `97.4 (601/617) | 141 (4) | Wilson (g) [93.2, 99.0];
percentile [94.5, 99.5] | [93.2, 99.4]`; row 21 `92.5 (571/617) | 141 | [87.7, 96.4] | [87.0, 96.1]` becomes
`92.1 (568/617) | 141 (12) | [87.5, 96.0] | [86.7, 95.6]`; row 46 `98.3 (1,129/1,149)` becomes `97.7 (1,122/1,149) |
139 | [95.8, 99.2]`; row 50 `−0.7 | 143 | [−2.4, 1.0]` becomes `−0.5 | 139 | [−2.5, 1.5]`; row 55 `98.4 (993/1,009)`
becomes `97.7 (986/1,009) | 130 | [95.9, 99.2]`; row 61 `+0.2 | 130 | [−1.7, 2.1]` becomes `+0.5 | 130 | [−1.5,
2.4]`; row 65 `98.6 (654/663)` becomes `96.8 (642/663)`; rows 68 (`94.7 (1,259/1,329)`) and 72 (`1 of 5; 0 of 5`)
are unchanged. The remaining twin rows are in `CV_V9.md` §4 cell for cell. In `tab3_naming.sources.md`, A4 → 
`results/eval_gate/closure/cv_v9/rigor_pre/a4.json`, A7 → `.../rigor_pre/a7.json` (cv5 cells; the zero-shot arm is
now `cv_v9.json#families/pre:zs_v9head`), A9 → `.../rigor_pre/a9.json`, CPL → `.../coupling_pre/coupling.json`.

**7. `figures/figure4.record.json` and the drawn figure.** Panel b footer "Three in view: 1,079 of 1,162 bodies
exact (92.9\,%)" becomes "1,079 of 1,159 bodies exact (93.1\,%)"; the drawn names "L2 0.99, L3 0.99, L4 0.99, none"
become "L2 0.99, L3 0.96, L4 0.98, none"; panel d keeps its five rows and "4 of 4", with `p_classifier` 0.925 /
0.9928 / 0.9983 / 0.6561 / 0.0066, candidates ordinary −3.0579 / L6 −1.1065, margin 1.9514 against
`tau_fold2_det74` 1.583, and "4 of 233" becomes "3 of 233 (case139_AP, case139_LAT, case44_LAT)". Panels a and c do
not move (617 of 676; 233 of 290; 979 of 1,009; the ranks are classifier-free). Inputs to re-point: `crop_b_pred` →
`closure/cv_v9/fig4_inputs_pre/proto_v9init_prerepair/cv_fold3/det/k3/case11_LAT_k3_1.json`, `score_b` →
`.../cv_fold3/det_score_k3.json`, `proto_a` → `.../proto_post_v9init_prerepair/cv_fold3/det/kfull/case11_LAT.json`,
`proto_d` → `.../cv_fold2/det/kfull/case42_LAT.json`, `couple_f0..f4` / `couple_a` / `couple_d` →
`.../proto_post_v9init_prerepair/cv_fold<K>/det/kfull/couple_c74/couple_all.json`, `coupling` →
`closure/cv_v9/coupling_pre/coupling.json`, `a4` → `closure/cv_v9/rigor_pre/a4.json`, `cv5` →
`closure/cv_v9/carmlspine_cv5_v9init_pre.json` (the drop-in twin of `docs/carmlspine_cv5_mixed_2026-09-21.json`).
The caption carries no number. The `leak_gate` block's "HELD OUT" labels on the b and d rows become true under
CHK-9 once `quoted_results.json` points at these files.

**8. `sections/discussion_limits.tex`, after "only runs from a lineage-complete encoder are reported."** Add
(REVIEW2_RSNA B4, which the file's own comment says to add if the day-grouped result again falls below zero-shot;
it does, 92.1 against 96.4 %):

```
Fine-tuning on the device's own frames added one point to lateral naming and, with acquisition days held out, fell
four points below the model that had never seen the device, so frames from other days did not carry to a new day.
```

**9. `sections/discussion_motivation.tex`.** No fine-tuned number is quoted there by design (its comment); the
zero-shot 96.4 % and the count's 97.0 % stand. If the paper wants one sentence on what fine-tuning bought, it is
the anteroposterior view (43.7 → 96.4 %), not the lateral (96.4 → 97.4 %).

**10. `SchwingNet/NUMBERS.md`** (line numbers as of 10:30 today; the old EVAL_LEAKS ids are in brackets).

| line | as it stands (number) | replace with |
|---|---|---|
| 55 [L46] | 617 of 676 boxed; sacrum on 233 of 290 at 0.74 | unchanged (detector-only); file pointers → `closure/cv_v9/carmlspine_cv5_v9init_pre.json`, `coupling_pre/coupling.json` |
| 56 [L47] | 1 of 5 anchored L6 bodies at 0.25 | unchanged; file → `coupling_pre/coupling.json#cells_with_veridah_l6/det~1kfull/per_level/L6` |
| 84 [L64] | 98.2 % = 606/617, 3 cases with an error; [95.7, 100.0]; BCa [95.0, 99.5]; Wilson on n_eff 147.6 [94.6, 99.4]; within one 100 % | 97.4 % = 601/617, 141 cases, 4 with an error; percentile [94.5, 99.5]; BCa [93.2, 99.4]; Wilson on n_eff [93.2, 99.0] (design effect 4.47); within one 99.2 % — `closure/cv_v9/rigor_pre/a4.json#cells/det~1LAT~1kfull` |
| 85 [L65] | 97.9 % = 138/141, Wilson [93.9, 99.3] | 97.2 % = 137/141, Wilson [92.9, 98.9] |
| 86 [L66] | AP 96.7 % = 610/631 (6 with an error); [93.6, 99.1]; BCa [92.9, 98.7] | 96.4 % = 608/631, 142 cases (7); [93.3, 98.6]; BCa [92.8, 98.4] |
| 87 [L67] | five in field 97.0 % = 647/667, 131 cases; [93.3, 99.8]; BCa [91.7, 99.2] | 95.8 % = 634/662, 131 cases (5); [91.4, 98.8]; BCa [89.9, 98.5] |
| 88 [L68] | three in field 92.9 % = 1,079/1,162; [89.6, 95.6]; BCa [89.1, 95.4] | 93.1 % = 1,079/1,159, 142 cases (23); [89.2, 96.2]; BCa [88.5, 95.9] |
| 89 [L69] | one in field 72.8 % = 440/604; [69.0, 76.2]; BCa [69.0, 76.2] | 74.8 % = 451/603, 142 cases (94); [70.9, 78.7]; BCa [70.7, 78.5] |
| 90 [L70] | day-grouped lateral 92.5 % = 571/617; [87.7, 96.4]; BCa [87.0, 96.1]; within one 95.1 %; answered 74.9 % | 92.1 % = 568/617, 141 cases (12); [87.5, 96.0]; BCa [86.7, 95.6]; within one 93.8 %; answered 72.9 % — `closure/cv_v9/rigor_pre/a9.json#cv/cvday_acquisition_day_folds/cells/det~1LAT~1kfull` |
| 91 [L71] | day-grouped AP 96.7 % = 610/631; [93.7, 99.1]; BCa [92.7, 98.7]; answered 74.2 % | 94.8 % = 598/631 (9); [91.0, 98.0]; BCa [90.2, 97.5]; Wilson on n_eff [90.1, 97.3]; answered 73.5 % |
| 92 [L72] | day-grouped three in field 87.6 % = 1,018/1,162; [83.3, 91.6]; BCa [82.3, 91.2]; answered 73.1 % | 87.7 % = 1,016/1,159 (38); [83.5, 91.6]; BCa [82.5, 91.1]; answered 72.6 % |
| 93 [L73] | day-grouped one in field 66.6 % = 402/604; [62.6, 70.6]; BCa [62.4, 70.4]; answered 69.9 % | 71.8 % = 433/603 (99); [67.6, 75.9]; BCa [67.3, 75.7]; answered 74.3 % |
| 95 [L75] | answered 83.1 % = 513/617 [79.7, 86.3]; exact on answered 98.4 % = 505/513 [96.2, 100.0], BCa [95.0, 99.6]; 3 of 11 errors among the abstained | answered 81.5 % = 503/617 [77.7, 85.0]; exact on answered 98.8 % = 497/503 [97.1, 100.0], BCa [96.2, 99.8]; 10 of 16 errors among the abstained — `rigor_pre/a7.json#cells/cv5~1det~1LAT~1kfull/default_rule` |
| 96 [L76] | 0.9 answers 53.6 % at 99.4 % [98.1, 100.0]; 0.95 answers 42.9 % at 99.6 % | 0.9 answers 57.5 % (355/617) at 99.7 % (354/355) [99.1, 100.0]; 0.95 answers 47.2 % (291/617) at 100.0 % (291/291) |
| 97 [L77] | AP answered 77.3 % [74.2, 80.5]; exact on answered 97.5 % [95.3, 99.4] | answered 73.1 % (461/631) [69.7, 76.6]; exact on answered 97.8 % (451/461) [95.7, 99.4] |
| 98 [L78] | five in field 83.4 % answered = 556/667 [79.6, 86.8]; exact on answered 97.7 % = 543/556 [94.4, 100.0], BCa [92.8, 99.5] | 82.0 % = 543/662 [78.0, 85.7]; exact on answered 97.6 % = 530/543 [94.5, 99.6], BCa [93.0, 99.3] |
| 99 [L79] | three / one in field: 80.0 % answered, 95.6 % [93.0, 97.7]; 74.3 %, 82.9 % [78.9, 86.4] | 79.2 % (918/1,159) answered, 96.4 % (885/918) [93.8, 98.4]; 79.4 % (479/603), 84.8 % (406/479) [81.7, 87.8] |
| 100 [L80] | complete coverage with truth boxes 93.6 % [90.0, 96.8], within one 99.1 % | 94.2 % (637/676) [90.9, 97.0], BCa [89.9, 96.7], within one 99.1 % — `closure/cv_v9/carmlspine_cv5_v9init_pre.json#oracle/LAT/kfull` |
| 101-103 [L81-L83] | the first zero-shot run (594/617, 239/631, +57.7) | superseded by lines 413-415 (v9); the closure's own re-score of that encoder on the pre-repair fold frames gives 595/617, 276/631, +54.3 pp [45.7, 62.4], 79 : 1 cases, identical to `leaks/zeroshot_v9.json` |
| 205 [L185] | ladder 72.8 / 89.5 / 92.9 / 95.7 / 97.0 / 98.2 % | 74.8 (451/603, 142) / 89.9 (870/968, 143) / 93.1 (1,079/1,159, 142) / 94.8 (999/1,054, 142) / 95.8 (634/662, 131) / 97.4 % (601/617, 141); percentile [70.9, 78.7] / [86.9, 92.7] / [89.2, 96.2] / [91.1, 97.7] / [91.4, 98.8] / [94.5, 99.5]; BCa [70.7, 78.5] / [86.6, 92.5] / [88.5, 95.9] / [90.3, 97.3] / [89.9, 98.5] / [93.2, 99.4] |
| 206 [L186] | day-grouped ladder 66.6 / 81.4 / 87.6 / 90.3 / 92.8 / 92.5 % | 71.8 / 84.9 / 87.7 / 90.7 / 92.0 / 92.1 % (433/603; 822/968; 1,016/1,159; 956/1,054; 609/662; 568/617); percentile [67.6, 75.9] / [81.2, 88.4] / [83.5, 91.6] / [86.0, 94.8] / [87.0, 96.6] / [87.5, 96.0] |
| 207 [L187] | zero-shot (zeroshot2) lateral whole frame 96.3 % [93.1, 98.7] (fig5_naming, retired) | the v9 zero-shot ladder: 63.8 / 80.4 / 83.7 / 88.6 / 89.3 / 96.4 % (385/603; 778/968; 970/1,159; 934/1,054; 591/662; 595/617; 142 / 143 / 142 / 142 / 131 / 141 cases); percentile [59.8, 67.9] / [76.4, 84.0] / [79.6, 87.5] / [84.4, 92.4] / [83.7, 93.9] / [93.4, 98.9]; BCa [59.8, 67.7] / [76.4, 83.9] / [79.4, 87.4] / [84.1, 92.2] / [83.3, 93.6] / [92.5, 98.7]; the first run's ladder (zeroshot2, not used) was 63.1 / 82.6 / 86.9 / 88.5 / 90.3 / 96.3 % — `cv_v9.json#families/pre:zs_v9head/cells/LAT/k{1..5,full}` |
| 211 [L191] | case42 lateral, fold 2, det74: classifier L2 (0.89), L3 (1.00), L4 (0.96), L5 (0.92), sacrum (0.02); ordinary −2.7851, L6 −0.7550; margin 2.0301 above the fold's threshold 1.6524; call L6 | classifier L2 (0.93), L3 (0.99), L4 (1.00), L5 (0.66), sacrum (0.01); ordinary −3.0579, L6 −1.1065; margin 1.9514 above the fold's threshold 1.583; call L6; coupled L2..L6; one disagreement, flag `disagreement` — `closure/cv_v9/fig4_inputs_pre/.../cv_fold2/det/kfull/couple_c74/couple_all.json#frames[stem=case42_LAT]` |
| 213 [L193] | 233 anchored; 1,066 counted, 34 disagree = 3.2 % [1.4, 5.4]; 12 of 233 = 5.2 % [2.5, 8.7]; agree 982/983; disagree coupled 13/26, classifier 11/26, neither 2 | 233 anchored; 1,066 counted, 42 disagree = 3.9 % [1.8, 6.5]; 13 of 233 = 5.6 % [2.6, 9.2]; agree 975/980; disagree coupled 16/29, classifier 11/29, neither 2 |
| 214 [L194] | matrix diagonal 1 / 136 / 215 / 221 / 221 / 221; off-diagonal ... (total 1,066; 1,032 on the diagonal) | diagonal T12 1 / L1 136 / L2 214 / L3 220 / L4 220 / L5 220 (total 1,066; 1,011 on the diagonal); off-diagonal L2→L3 6, L3→L4 6, L4→L5 6, L2→L1 6, L3→L2 6, L4→L3 6, L5→L4 6, sacrum→L5 5, L1→L2 4, L6→L5 1, L2→L4 1, L3→L5 1, L1→T12 1 — `closure/cv_v9/cv_v9_extras_pre.json#matrix_det74_kfull`. (The old row quoted "1,032 on the diagonal" = 1,066 − 34 disagreeing bodies while its own diagonal cells summed to 1,015; the new diagonal sums to 1,011 against 1,024 = 1,066 − 42: the coupler's disagreement count does not treat every off-diagonal cell as a disagreement, a body the classifier names "sacrum" abstaining, so the two readings differ by construction, as before) |
| 215 [L195] | flag fires on 4 of 5 error frames and 17 of 225 correct (7.6 %); unflagged 921/922 | on 5 of 6 error frames and 16 of 224 correct (7.1 %); unflagged 921/922; flagged 70 of 87 (80.5 %) |
| 237 [L217] | case-grouped lateral 98.2 % (606/617) Wilson on n_eff [94.6, 99.4] (percentile upper limit 100.0 with 11 errors) | 97.4 % (601/617) Wilson on n_eff [93.2, 99.0] (design effect 4.47; 16 errors) |
| 238 [L218] | case-grouped AP 96.7 % (610/631) Wilson on n_eff [92.7, 98.5] | 96.4 % (608/631) Wilson on n_eff [92.5, 98.3] |
| 240 [L220] | case-grouped 606/676 = 89.6 % | 601/676 = 88.9 % |
| 241 [L221] | cv fold 0 lowest det_conf 0.381 | new cv (all folds) 0.364, zero-shot v9 0.364 (pre) — `cv_v9.json#detector_min_det_conf_pre` |
| 251 [L231] | classifier 993 (98.4 %) [96.8, 99.7], count 979 (97.0 %) [94.2, 99.2], coupled 995 (98.6 %) [97.2, 99.7]; coupled − count +1.6 [0.0, 3.8]; coupled − classifier +0.2 [−1.7, 2.1]; disagreement 12/233 = 5.2 % [2.5, 8.7]; flag 4 of 5 / 17 of 225; unflagged 921/922 | classifier 986 (97.7 %) [95.9, 99.2], count 979 (97.0 %) [94.2, 99.2], coupled 991 (98.2 %) [96.5, 99.5]; coupled − count +1.2 [0.0, 3.2]; coupled − classifier +0.5 [−1.5, 2.4]; disagreement 13/233 = 5.6 % [2.6, 9.2] (132 cases); flag 5 of 6 / 16 of 224; unflagged 921/922 — `coupling_pre/coupling.json#cells/det74~1kfull` |
| 298 [L278] | at 0.25: classifier 98.3 % (1,129/1,149) [96.5, 99.6], count 96.1 %, coupled 97.5 % (1,120/1,149) [95.7, 99.0], +1.4 [0.0, 3.4], −0.7 [−2.4, 1.0], disagreement 6.8 % (18/266) [3.5, 10.2], flag sensitivity 9/10, false alarm 18/252 = 7.1 %, unflagged 1,040/1,041; at 0.74 98.4 / 97.0 / 98.6; five in field at 0.25 98.6 (654/663), 88.5, 89.9 (596/663) [85.8, 93.5]; oracle 94.7 / 97.7 / 95.9 of 1,329 | at 0.25: classifier 97.7 % (1,122/1,149) [95.8, 99.2], count 96.1 % (1,104/1,149), coupled 97.1 % (1,116/1,149) [95.3, 98.8], +1.0 [−0.1, 2.9], −0.5 [−2.5, 1.5], disagreement 7.1 % (19/266) [3.8, 10.8], flag sensitivity 10/11 (90.9 %), false alarm 19/251 (7.6 %), unflagged 1,032/1,033; at 0.74 97.7 / 97.0 / 98.2; five in field at 0.25 96.8 (642/663), 88.5 (587/663), 90.3 (599/663) [86.3, 93.8]; oracle boxes 94.7 (1,259/1,329) / 97.7 (1,298) / 97.0 (1,289) — `coupling_pre/COUPLING.md` §"five test folds pooled" |
| 299 [L279] | 1 of 5 coupled, 0 of 5 classifier | unchanged |
| 301 [L281] | ordinary spines today: 260 of 266 anchored frames ordinary, 6 called L6 in five cases | 261 of 266 ordinary, 5 called L6 in four cases (case139, case19, case44, case9) at 0.25; at 0.74, 230 of 233 ordinary, 3 L6 in two cases |
| 402-403 | "every case- and day-grouped fold cell (606/617, 610/631, 571/617, ...)" UNRESOLVED | resolved by this section: each replaced above |
| 417 | first zero-shot run, not used: 594/617, 239/631 | add: first fold-model runs, not used: 606/617 case-grouped, 571/617 day-grouped lateral (Table 4 note h) |

**11. `CLAIMS_LEDGER.md:211`** ("classifier unchanged in 20 of 20 cells; coupled 90.3 % [79.8, 98.4] vs classifier
86.0 % [75.1, 95.4] on anchored bodies; DEFENSIBLE AFTER a verifier re-runs"): the re-run's report again shows the
classifier unchanged in 20 of 20 cells (`coupling_pre/COUPLING.md` "The classifier did not move"); the oracle
five-in-field cell it quotes (`oracle_ext/k5`) is now coupled 93.0 % (239/257) [84.9, 99.2] against classifier
90.3 % (232/257) [80.7, 98.0]; the verifier's re-run is this closure, with the gate on every input.

**12. Rows that do not move, and rows this closure does not own.** The count from the sacrum (Table 4 lines 65-70,
72, 74; Key Point 2's 979 of 1,009; `FIGREC:figure4/07-12`) uses no level encoder and is identical in the re-run.
The zero-shot whole-frame cells already in the text (595/617, 276/631, +54.3) are reproduced. `RESCORE:G1`, `H1`,
`H2` take the det74/kfull, case-grouped lateral and zero-shot cells above. `FIGREC:figure5/03` is retired. Not this
closure's: `results.tex:72` and Figure 5's in-domain data-case panels (`results/indomain/fit.json`, the
`indomain_name_fill` workflow) and the Flagship cells of `tab2_detection.tex:54-66` (FLAGSHIP_PLAN G5).

### 7.3 Where every number here is read from

| number | file (all under `SchwingNet/results/eval_gate/closure/cv_v9/`) |
|---|---|
| every cell, old and new, both truths | `cv_v9.json#families/<old|pre|rep>:<cv5_det|cv5_oracle|cvday_det|zs_v9head|zs_v9nohead|zeroshot2>/cells/<VIEW>/k<K>` (k, n, clusters, clusters_with_error, percentile, bca, wilson_effective_n, ceiling_regime, answered, exact_on_answered, abstain_sweep, within1, per_level, confusions); tabulated in `CV_V9.md` |
| the pooled twins of `docs/carmlspine_cv5_mixed_2026-09-21.json` | `carmlspine_cv5_v9init_pre.json`, `carmlspine_cvday_v9init_pre.json` (and `_rep`) |
| a4 / a7 / a9 twins of `results/a4.json`, `a7.json`, `a9.json` | `rigor_pre/a4.json`, `a7.json`, `a9.json` (and `rigor_rep/`) |
| coupling | `coupling_pre/coupling.json` (`#cells/det74~1kfull`, `det~1kfull`, `det~1k5`, `oracle~1kfull`, `oracle_ext~1k5`, `#cells_with_veridah_l6`, `#l6_patients`, `#tau`), `coupling_pre/COUPLING.md`; the five det74 coupler records `fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold<K>/det/kfull/couple_c74/couple_all.json` |
| paired zero-shot vs fine-tuned; the matrix | `cv_v9_extras_pre.json#pairs/<LAT|AP>/<comparison>`, `#matrix_det74_kfull` |
| Figure 4 b and d records | `cv_v9.json#figure4/b_pre`, `d_pre`; the input files under `fig4_inputs_pre/` |
| controls | `cv_v9.json#controls`, `prerepair_fold_dirs.json` |
| gate verdicts | `cv_v9.json#families/*/gate`, `#strict_gate_on_old`; each score file's own `eval_gate` block on the grid (`/rs/rs_grp_oschome/go2432/data/carmlspine/proto_v9init_prerepair/`, `proto_post_v9init_prerepair/`) |
| job logs | `grid_pull/` (carmcv9i, carmcvday9i, carmcv9pre, cv9iprerep, cv9icollect, cv9iclosure, cv9iextras, zs9kfield) |

---

## 8. The accuracy-saturation reading (Greg's request of 2026-09-24): what these numbers support

Greg asked that the ideas of the uploaded overview ("Advanced Computational Frameworks for Vertebral Body Detection
and 2D/3D Registration in Intraoperative Fluoroscopy", `3e8e7309-AA_.pdf`) be integrated, "especially the learning
rate accuracy saturation part". The part in question is its §2: a fluoroscopy model that plateaus near 90 % while
standardised radiographs reach 99 % is rarely capacity-limited; the plateau is sampling-density saturation in a
high-dimensional acquisition space (positioner angles, SID, magnification, patient position), so adding randomly
sampled same-device data yields diminishing returns, and the remedy is coverage-driven sampling of the sparse
acquisition bins (a coverage ratio per dimension and a normalised entropy over DICOM tags). This section states what
the closure's held-out numbers say about that reading; the paper workflow owns the text. **The overview is an
unsourced synthesis; the paper cites its primary sources** (its works-cited list: DeepDRR, Unberath 2018; DiffDRR,
Gopalakrishnan 2022; the pairwise domain-adaptation module, Zheng 2018, PMC5767648; LevelCheck, De Silva 2016;
X23D, Jecklin 2022), never the overview.

**What the C-ArmLSpine numbers show (pre-repair truth, all held out; `cv_v9_extras_pre.json`, `CV_V9.md` §6).**

1. *Lateral naming is saturated before any same-device frame is seen.* Zero-shot, trained on renders and
   radiographs only, names 595 of 617 detected lateral vertebrae (96.4 %). Fine-tuning on the other ~118 cases of
   the same device changes 22 calls (14 gained, 8 lost) for 601 of 617 (97.4 %): +1.0 point [−1.9, +4.0], four
   cases better and two worse, exact sign p 0.69. The recurrent head adds +0.8 [−2.4, +4.2] over the encoder alone.
   Same-device data does not move the lateral plateau.
2. *The anteroposterior view is a coverage hole, and same-device data fills it.* Zero-shot names 276 of 631 AP
   vertebrae (43.7 %); fine-tuned, 608 of 631 (96.4 %): +52.6 points [+44.1, +61.3], 78 cases better and 2 worse.
   The AP geometry of this C-arm is not in the render/radiograph training distribution; ~118 cases of it are enough
   to bring AP to the lateral ceiling.
3. *Within one device, acquisition day is a coverage dimension.* With whole acquisition days held out, the
   fine-tuned model names 568 of 617 lateral vertebrae (92.1 %): 4.4 points below zero-shot [−9.1, +0.2], four
   cases better and ten worse, and 5.3 points below the case-grouped fine-tune [+2.1, +9.1], eight cases better and
   none worse (p 0.008). Same-device frames from other days do not transfer to a new day; they move the model off
   the broad prior towards the seen days. On the AP view the day-grouped fine-tune still gains 51.0 points over
   zero-shot, so the hole the AP frames fill is a view, not a day.
4. *Same-device data buys most where the field is smallest, and nothing on the whole frame.* Fine-tuned:
   74.8 / 89.9 / 93.1 / 94.8 / 95.8 / 97.4 % at one to five lateral bodies and the whole frame; zero-shot:
   63.8 / 80.4 / 83.7 / 88.6 / 89.3 / 96.4 %. Paired on the same crops (`cv_v9_extras_pre.json#pairs_by_k`), the
   fine-tuned gain over zero-shot is +10.9 [+6.4, +15.5] at one body (65 : 24 cases), +9.5, +9.4 [+4.5, +14.5],
   +6.2, +6.5 at two to five, and +1.0 [−1.9, +4.0] on the whole frame. The day-grouped fine-tune shows the same
   shape at a lower level: +8.0 [+3.3, +12.5] at one body, +4.0 at three, and −4.4 on the whole frame. So the
   whole-frame lateral plateau is the render-and-radiograph prior's own ceiling; the limited field, where a body
   must be named from its shape with little context, is where the device's own frames add coverage.
5. *What the manuscript cannot yet claim.* The overview's "99 % on standardised radiographs" has no held-out
   counterpart of our own: the plain-film accuracies (97.3-99.8 %) are the encoder's selection split (EVAL_LEAKS
   L4) and no held-out film number exists until the Figure 6 model is scored. The comparison in the paper must be
   lateral (96.4 %, held out, unseen device) against AP (43.7 %), not film against fluoroscopy.

**Proposed use in the paper (for the paper-six-figures workflow).** One sentence in the Results after the
fine-tuned numbers (item 3 of §7.2 already carries the paired gains) and one paragraph in the Discussion, in place of
a second same-device-data claim: the lateral plateau did not respond to same-device data, the anteroposterior view
did, and a held-out day was worse than never having seen the device; so the next data should be chosen by where the
acquisition space is empty (view, day, and, by the DICOM positioner and distance tags, angle and magnification), not
by volume. The Limitations sentence of §7.2 item 8 carries the day-grouped fact.

**A concrete follow-up this closure did not run** (a new analysis, not a re-score): the coverage and normalised
entropy the overview defines can be computed for C-ArmLSpine from the DICOM tags already on the grid
(`/rs/rs_grp_oschome/go2432/data/carmlspine/headers_dossier.json`, `tags_case*.txt`: positioner primary and
secondary angle 0018,1510 / 0018,1511, SID 0018,1110, patient position 0018,5100) over the 148 cases and their
acquisition days, and per fold. It would say whether the held-out days occupy acquisition bins the other days do
not, which is the overview's mechanism stated as a measurement rather than an interpretation; and it would give
Figure 2 of the flagship plan (the sampling chart) a real-device column. It needs a CPU job and a reading of the
per-frame tags; no checkpoint is involved.
