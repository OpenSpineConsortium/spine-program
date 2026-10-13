# STATUS.md: the results in hand, with numbers, files and rigor marks

Status words and rigor marks are those of `docs/handoff/RESULTS_CATALOG.md` "How to read a row":
CURRENT; CURRENT-SEL (printed, but measured on the split that chose the checkpoint); HELD-OUT, NOT
QUOTED; SUPERSEDED; DISPUTED; REFUTED; RECORD ONLY (pre-SchwingNet exploration, not quotable); NOT
RECORDED; OPEN; and the marks [THR], [SEL-REP], [WRONG-BANK], [LEAK], [SEL-SPLIT], [ONE-SEED],
[AUTO-TRUTH], [DERIVED], [WORDING]. Rows with a catalog id are copied from the catalog with their id;
rows without one come from this folder's own files and say so. Grid paths are spelled in full in
`MANIFEST_GRID.md`; `sn:` below means `SchwingNet/` inside `spinesurg-ct-nnunet` 097933a.
`~` is `/wsu/home/go/go24/go2432`, the grid HOME, wherever a path below is abbreviated.

**2026-10-12, who reads what.** Greg answered OPEN_QUESTIONS A29 on issue #68, option (a): every Write holder may read all 13 folders; "Greg-only" and the label `greg-first` govern claiming and hand-outs, not reading. The `docs/handoff` copies keep their older wording.

## 1. The held-out numbers (quotable: through `eval_gate.py`, in the catalog)

### A10. Plain-film naming against training persons, and the render ablation (Figure 5b film, Table S4)

Design: a render-only encoder (the v9 bank minus every film row; 47,976 train / 9,036 val crops;
ImageNet start; own val exact 0.664) fine-tuned per cell on N persons of one corpus merged 1 : 1 with
the render bank's per-class-600 sample (15 epochs), then `head_mixed_length --train-mode mixed`; TEST =
the v9 VAL persons of that corpus, never trained or selected on by any cell or by this encoder;
scored by `tools/rigor_fixes.py a5-rows` with `tools/eval_gate.py` first. Seeds 0-2 at N <= 25,
seed 0 only above. Files: `sn:results/coverage/film_ncurve/film_ncurve.json`, `FILM_NCURVE.md`
(2026-09-24 23:25, 48 of 48 cells); jobs 40437808 -> 40437809 -> 40437810 -> 40437811.

| id | claim | status | feeds |
|---|---|---|---|
| A10.1 | NHANES II exact level at N = 0 / 5 / 10 / 25 / 50 / 100 / 200 / all: 27.2 / 77.8 / 82.3 / 87.8 / 89.2 / 89.6 / 92.5 / 92.7 % (264 persons) | CURRENT, HELD OUT | Figure 5b |
| A10.2 | BUU-LSPINE: 10.3 / 65.0 / 70.3 / 76.7 / 81.2 / 82.7 / 85.1 / 96.9 % (2,967) | CURRENT, HELD OUT | Figure 5b |
| A10.3 | CSXA: 3.2 / 94.2 / 93.0 / 96.4 / 97.3 / 97.3 / 98.0 / 99.8 % (4,114) | CURRENT, HELD OUT | Figure 5b |
| A10.4 | cross-corpus transfer peaks at 74.3 % (NHANES -> CSXA at N = 200, 749 films); NHANES-trained 73.2 % on BUU (all); BUU <-> CSXA <= 12.6 %; CSXA -> NHANES <= 43.7 % | CURRENT | Results |
| A10.5 | pooled-fit asymptotes: NHANES 95.9 % (the all point 3.2 below), BUU 100 % (3.1 below), CSXA 100 % (reached); `sn:results/coverage/pooled_fit.json#admissibility` | HELD-OUT, NOT QUOTED | — |
| A10.6 | render ablation at N = 5: render-only minus film-only NHANES +21.9, BUU +11.1, CSXA +18.7 points, every seed separated (`sn:results/coverage/film_ncurve/ablation/READ.md`; arrays 40451157 imagenet 48 / 48, 40451158 filmonly 39 / 48) | CURRENT, HELD OUT | Discussion, Table S4 |
| A10.7 | at N = 25: +12.2, +6.0, +6.2, every seed separated | CURRENT | Table S4 |
| A10.8 | at every person: NHANES +0.7 (level), CSXA -0.2 (level), **BUU -1.6, separated: renders hurt** (96.9 [96.0, 97.8] against 98.5 [98.0, 99.0]) | CURRENT [ONE-SEED] | Discussion |
| A10.9 | seven of nine verdict cells separated: six help, one hurts | **DISPUTED**: `memory/film-ncurve-ablation-result.md` and `sn:REVISION_LOG3.md` section 13 say "all help"; trust `READ.md`; the Discussion places "7 of 9" inside "five to twenty-five persons" where only six verdict cells lie [WORDING] | Discussion |
| A10.10 | ImageNet init on the same merged bank sits between (NHANES N = 5: 75.5 against 77.8 render-only against 55.9 film-only); at 50 persons NHANES and CSXA still separate (+7.7, +2.9); at 100 and 200 nothing separates | CURRENT | Table S4 |
| A10.11 | the synthetic:real ratio was about 1 : 1 by rows in every cell (`tools/merge_banks.py` line 60, `real_share` 0.5; 15,374 render rows per cell) while the distinct-image ratio ran 615 : 1 to 0.75 : 1; **never swept** | CURRENT fact | — |
| A10.12 | do not plot the N-curve endpoints (92.7 / 96.9 / 99.8) beside the A5 film numbers (99.1 / 97.3 / 99.8): different encoders on different splits | rule | — |

### A14. Render-trained against film-trained detector on plain films

| id | claim | file | status |
|---|---|---|---|
| A14.1 | 17 NHANES II lumbar spines neither detector saw, confidence 0.05: film-trained `detector_v5z_final` 99.4 % (160 / 161) against render-trained `anchor_det_v1` (6,650 renders, no real image) 67.7 % (109 / 161), +31.7 points [21.0, 45.4], 16 : 0 spines; at 0.25, 98.8 against 34.8 % | `sn:results/eval_gate/leaks/render_vs_film_unseen_rerun.json` (job 40429839) | CURRENT, HELD OUT |
| A14.2 | the 25-spine version: 99.14 against 71.67 %, +27.5 | older text | SUPERSEDED [LEAK] (24 of 25 spines in the film detector's own lists) |

## 1b. Held out by patient within BUU, repository-internal, not yet through `eval_gate.py` (TODO step 5)

Not quotable as gated: nothing in this section passed `tools/eval_gate.py` (CLAUDE.md rule 5).

### XRSpinoPelvic1K corner detection on BUU-LSPINE (this folder's own files; not in the catalog)

Every number: 301 test films of the patient-grouped, sex x age-band stratified 1398 / 301 / 301 split
(`buu_splits.json`), one metric implementation (`xrsp/evalmetrics.py`), repository main 4f22935.
These passed the repository's own evaluator, **not** `tools/eval_gate.py`; the BUU levels are
assigned by position, so "level" here is position. Mark: repository-internal, held out by patient
within BUU; not yet through the programme's gate; to be regenerated on the v11 rebuild (TODO step 5).

| claim | number | file |
|---|---|---|
| corner localisation, YOLOv8l-Pose at 1024 px, all annotated landmarks | 92.4 % within 0.55 % of the diagonal (Bansal's "5 px" on 640 px, converted), 99.3 % within 1.10 %, 99.8 % within 1.66 %; median 0.203 % of the diagonal (about 6.4 px on a median 3,167 px diagonal) | `docs/xrspinopelvic1k/docs/RESULTS.md` section 1.2 |
| the published models at the strict threshold | YOLOv8n-Pose 75.6 %, YOLOv11n-Pose 76.8 %, Detectron2-R50 75.8 % (their keypoints scored only inside IoU >= 0.5 matched boxes; 698 images against our 2,000) | same; `docs/journal.pone.0347290.pdf` |
| architecture and resolution sweep | v8l_640 median 6.89 px, 62 missed; v8l_1024 6.38 px, 160 missed; v11n at 640 / 1024 / 1280: 8.30 / 7.64 / 9.09 px; combined BUU + DRR 9.74 px (worst) | RESULTS.md section 1.3 |
| sacral slope from predicted corners (v8l_640) | ICC(2,1) 0.952, MAE 2.01 degrees, 94 % within 5 degrees, bias -0.36 degrees, limits of agreement -6.3 to +5.6 | RESULTS.md section 2 |
| lumbar lordosis (v11n_1024) | ICC 0.940, MAE 3.75 degrees | same |
| heatmap model, for comparison | SS ICC 0.887, MAE 2.95 degrees, 85 % within 5; LL ICC 0.865, MAE 4.85 degrees | same; `figures/buu_vs_drr/summary.json` (`buu.parameters`: SS ICC 0.8866, MAE 2.945; LL ICC 0.8654, MAE 4.848) |
| YOLO11n-pose, 282 films with SS | SS ICC 0.943, MAE 2.30 degrees, 91.8 % within 5; LL ICC 0.893, MAE 4.31 degrees | `results/corner_detector_buu/yolo/summary.json` |
| corner identity | macro-F1 0.999-1.000 (YOLO), 0.986 (heatmap); every off-diagonal entry is a superior / inferior slip on the same wall; anterior / posterior confusion is near zero | RESULTS.md section 3; `figures/buu_vs_drr/summary.json` |
| Theil-Sen fit across lumbar end-plates | rejected: LL MAE 6.68 against 4.85 degrees | RESULTS.md section 2 |
| per-level corner error (heatmap) | 1.14-1.21 px median at L3 / L4 (L3 1.141, L4 1.213; RESULTS.md prints 1.15-1.20, a rounding noted in the copy); 1.96 px at S1; 1.35 px at L1 | `results/corner_detector_buu/per_landmark_buu.csv` (medians recomputed 2026-10-08); RESULTS.md section 2 |
| confidence as a failure predictor | AUC 0.662 for a > 15 px error; 0 abstentions of 6,622 landmarks | RESULTS.md section 5 |
| image contrast against failure | correlation +0.072 (log max-error against intensity SD); the CLAHE run was cancelled | RESULTS.md section 5 |

Negative results (each closes a direction; RESULTS.md section 4): a pelvis class trained only on DRRs
fires on 40 / 40 DRRs at 0.94 confidence and 0 / 40 real films; femoral heads lie inside the image
bounds on 99.8 % of films (the earlier claim that they were outside is retracted in the file);
`xrsp/hipfit.py` "converged" on 301 / 301 films and is unusable; mixing DRRs into training was worst
or near-worst on every column (ED5 18.2 against 33.2 %); corner channels trained on BUU give 85 px
median error on DRRs (`figures/buu_vs_drr/summary.json` `drr.corner_error_px.median` 85.16).
Whole-spine framing (section 4b): a single pass finds 6.00 / 6 vertebrae at f = 1.00 and 0.00 / 6 at
f = 0.36; tiling holds 5.45 / 6 at f = 0.36 and 5.4-5.7 down to f = 0.20 with median corner error
0.28-0.33 % of the diagonal; at f = 1.00 tiling costs 6.00 -> 5.40 and SS MAE 2.79 -> 3.66 degrees.
Extrapolation above L1 (section 4c): 0.10 extra detections per film, 10 % of films, T12 only.
Methodological (section 5): anisotropic resize rendered a true 45-degree plate at 58.7 degrees;
checkpoint selection on validation loss kept the untrained heatmap network.

## 1c. Dated detector numbers (this folder's own files; superseded on the grid)

### The spine-detector detect_v1 field report (2026-09-02; this folder's own files)

| claim | number | file | status |
|---|---|---|---|
| held-out 558 instances, all | AP50 0.957, PCK@0.1 0.768, PCK@0.2 0.917 | `results/spine_detector_report/metrics.json` | DATED (superseded by detect_v2 on the grid) |
| by source: NHANES film (294) / Mendeley standing DR (249) / BUU (15) | AP50 0.970 / 0.956 / 0.861; PCK@0.1 0.815 / 0.715 / 0.731; PCK@0.2 0.924 / 0.910 / 0.904 | `metrics.json`, `report.txt` | DATED |
| training | 111 epochs; final box mAP50 0.980, mAP50-95 0.771; pose mAP50 0.922, mAP50-95 0.901 | `results.csv` last row | DATED |
| corpus at the time | 958 films, 6,073 instances, 727 patients (NHANES 3,217, Mendeley 2,666, BUU 190); `level_source` annotated 3,217 / unknown 2,666 / inferred_from_position 190 | `manifest.parquet` | DATED |
| detect_v2 (2026-09-08, 120 epochs) | AP50 0.970, PCK@0.1 0.812, PCK@0.2 0.942 on the same 558; film 0.960 / 0.852, standing DR 0.970 / 0.767; training-time val (535 films) box mAP50 0.991, pose mAP50 0.977; corpus 33,943 instances on 5,401 films (2026-09-07) | `memory/xray-corner-detector-status.md`; grid `~/spine-detector/runs/detect_v2/eval/` | DATED (C1.19); the later detectors (v3, v4, v5z, v6f) are folder 01's |

The report states its own gaps: no ignore-region ablation, no level head, no cross-site test; CSXA,
BUU-full, AASCE and VinDr not yet obtained at the time (`report.html`).

## 2. Printed on the selection split only (not held out)

### A15. Plain-film naming (selection split only)

File `sn:results/a5.json#per_protocol/random/*/patient_clustered` (v8 encoder, head
`head_allspine_v8_mixed_kmax4_seed0.pt`, seed 0). Every annotated patient of these corpora is in v8's
training or selection split, so **no held-out plain-film accuracy exists in paper 1** (EVAL_LEAKS L4).

| id | claim | status |
|---|---|---|
| A15.1 | CSXA cervical: 3,629 / 3,635 (99.8 %), 727 patients, Wilson [99.5, 99.9]; three bodies 99.6 % | CURRENT-SEL [SEL-SPLIT] |
| A15.2 | BUU-LSPINE lumbar: 2,671 / 2,744 (97.3 %), 549 cases [96.5, 98.0]; three bodies 95.0 % | CURRENT-SEL |
| A15.3 | NHANES II: 441 / 445 (99.1 %), 52 patients / 76 films, Wilson [97.8, 99.6]; three bodies 94.6 % | CURRENT-SEL |
| A15.4 | v9, three seeds: NHANES 96.9-97.6 % (`sn:results/v9_a5_seeds.json`) | CURRENT-SEL |
| A15.5 | per-level film naming: BUU L1-L5 96.4-98.4 %, NHANES 97.4-100 %, CSXA 99.7-100 %; renders floor at T7 (55-59 %), L6 20-42 %, T13 0 / 9 (`PER_LEVEL_DOMAIN_ANGLE.md` Table E) | [DERIVED] [SEL-SPLIT]; not quotable until a committed tool re-runs it on held-out persons (TODO 7) |
| A15.6 | the v9-bank re-score of A5 (chain 40415667 -> 40415670) "had not landed"; whether it did later | NOT RECORDED |

## 3. Retired: the C-arm and film programme before SchwingNet (2026-09-12 to 2026-09-22)

None of these is quotable. Each row names what replaced it.

### C1. Plain-film level identification and the early level models

| id | claim | file / bank | status | replaced by |
|---|---|---|---|---|
| C1.1 | context ladder on real films: single vertebra 96.7 %, 3 vertebrae 98.8 %, 5 vertebrae 99.1 %; lumbar n = 1 80.7 % (85.4 % at 96 px) | `/wsu/home/go/go24/go2432/tmp/ladder_summary.json` **not found on 2026-10-08** (a read-only `ls` at 01:25 UTC 2026-10-09; `memory/level-id-2d-results-2026-09-13.md` and RESULTS_CATALOG C1.1 are the only record); `films_ann` (cervical-dominated) | RECORD ONLY | A10 (held out) |
| C1.2 | recurrent head over single-crop embeddings: 98.69 / 99.13 / 99.41 / 99.48 % at 3 / 5 / 7 / 9 vertebrae, n 8,422; 14 of 27 classes live; weights never saved | `~/bench/xr_fov/recurrent.json`; **`films_ann_fov96_ctx`, not `films_all2`** (job 40215812 printed 28,032 crops); `slurm/recurrent_head.sh` line 16, `tools/recurrent_order.py` line 56 and `~/bench/model_registry.md` M96 still say `films_all2` | RECORD ONLY [WRONG-BANK] | A10; TODO step 2 |
| C1.3 | films_all2 head: 98.84 / 99.13 / 99.42 / 99.38 | `~/bench/xr_fov/recurrent_all2.json`; `results/track5_results/REPORT_all2.txt` (ten seeds: 98.81 / 99.23 / 99.33 / 99.36 % mean, sd 0.04-0.07 points) | RECORD ONLY | A10 |
| C1.4 | whole-spine 27-class single crop 78.74 % [78.11, 79.37], n 16,392; T13 0.0 % (n 14), L6 64.4 % | `~/model_night/runs/result_r18_ce.json`; allspine_v2 | RECORD ONLY [LEAK] | folder 01's v9 numbers |
| C1.5 | restored recurrent head on allspine_v2: 83.38 / 86.12 / 86.16 / 88.95 % at 3 / 5 / 7 / 9 (+10.2 at 9); T6-T8 floor 62-65 % | `~/model_night/recurrent_allspine_v2.json`; `memory/recurrent-head-restored-2026-09-16.md`; `results/track5_results/REPORT.txt` Part A (ten seeds: 83.42 / 86.23 / 86.13 / 88.70 % mean) | RECORD ONLY [LEAK] | — |
| C1.6 | mixed-length head 97.47 / 98.45 / 99.29 / 99.92 at 3 / 5 / 7 / 9; random window 99.02 % ("shortcut-free") | `memory/mixed-length-head-and-sota.md`; allspine v2, which pooled NHANES II twice | SUPERSEDED [LEAK] | A10.1-A10.3 |
| C1.7 | Star Temporal Classification loss loses to cross-entropy everywhere; transitional 22-24 % against 39.8 % | `~/model_night/stc/`; `memory/stc-does-not-transfer.md` | REFUTED | do not revisit |
| C1.8 | selective prediction: 99 % at 35.7 % coverage (exact), 55.7 % (region); AUGRC 0.0466 | `~/selective/SELECTIVE.md`; `memory/selective-prediction-the-honest-99.md`; leaked v2 bank, coverage chosen on the scored half | NOT QUOTABLE [LEAK] [SEL-REP] | TODO 8 (no clean re-run exists, OQ C13) |
| C1.9 | model-night arms: CORN 78.44, ordinal focal 75.05, frozen 30.12 %; four ViT arms produced no result | `docs/MANIFEST_DATA_MODELS_RESULTS.md` sections 5.2, 7.2; `results/lumbar_diag_2026-09-16/lumbar_combine_eval.json` (single crop: r18_ce 0.951, r18_corn 0.948, r18_ordfocal 0.925, dinov3_ft 0.798) | RECORD ONLY | — |
| C1.10 | corruption suite: films_all2 rung 1 clean 99.10 %, over-exposure severity 5 16.93 %; augmentation tier 2 79.18 % (motivates `--augment 2`) | `~/bench/robust/*.json` | RECORD ONLY | the `--augment 2` default stands |
| C1.11 | literature panels (FluoroCap): 19.7 % agreement with weak labels, n 7,065; resolution does not move naming (-0.33 points paired) | `~/model_night/panel_stats/`; `memory/fluoro-panel-gap-diagnosed.md` | not an accuracy; FluoroCap is figures of published articles (72.8 % of panels with zero pixel residual) | out of training (D1) |
| C1.12 | LSTV / TLTV 2-D flags: CTSP AUC 0.577 [0.480, 0.669]; VerSe 0.724; sex as positive control 0.951 on renders / 0.829 on real BUU | `~/lstv_flag/LSTV_FLAG_RESULTS.md` | REFUTED as a flag | folder 02 |
| C1.13 | LSTV flag learning curve, VerSe held out (67 patients, 31 positive): 10 positives AUC 0.652, 20 0.688, 40 0.704, 80 0.685, 120 0.713 | `docs/MANIFEST_DATA_MODELS_RESULTS.md` line 659; `~/lstv_flag/LEARNING_CURVE.md` (date and job not recorded) | RECORD ONLY | folder 02 |
| C1.14 | feasibility interior windows: v2 ordinary lumbar 91.8 % [89.4, 94.1]; anomalous 66.0 % (12 films); v6 anomalous interior 49.9 % [41.5, 58.9] (128 films) | `~/model_night/interior_windows/`; `memory/feasibility-claims-measured.md`; job 40321368 | RECORD ONLY [LEAK] | — |
| C1.15 | remedies (film-noise randomisation, pretrain on renders, renders mixed 8 epochs, anchored-only admission) all lose to the v2 baseline | `memory/remedies-refuted-2026-09-17.md` | REFUTED on a leaked bank | TODO 9 |
| C1.16 | Cina-style whole-film benchmark: v2 99.96 % = the sacrum-count rule 99.96 %; saturated | `memory/feasibility-claims-measured.md`; `tools/benchmark_cina.py`, job 40323179 | RECORD ONLY | only the limited field discriminates (folder 01) |
| C1.17 | re-implemented competitors (ours, Cina, Kim, VertX, Konya; 124 cells) and their ensemble | design `docs/COMPETITOR_BENCHMARK.md`; output `~/model_night/ensemble/ensemble.json` | **NOT RECORDED** in any repository document | TODO 6 |
| C1.18 | two-mechanisms table: L6 44.9 % in State C; one body 72.9 %, five bodies 97.0 %, whole 98.2 % | `memory`-adjacent note `two-mechanisms-thesis` (folder 01) | SUPERSEDED | 601 / 617 = 97.4 % whole lateral frame, 451 / 603 = 74.8 % one body (A3.1, A3.3; folder 01) |
| C1.19 | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | `memory/xray-corner-detector-status.md` | DATED | section 1 above |

### C2. The 2026-09-17 synthetic / real fraction sweep

| id | claim | status |
|---|---|---|
| C2.1 | six encoders on subsets of the v2 bank, scored on 455 held-out real lumbar films (interior windows): render fraction 0 / 0.25 / 0.5 / 1.0 at real 1.0 gave ordinary 89.5 / 87.7 / 87.4 / 88.2 % and anomalous (12 films, 47 windows) 34.0 / 44.7 / 53.2 / 36.2 %; real 0.5 and 0.25 at render 1.0 gave ordinary 84.3 / 83.7 %; cervical 97.1-98.8 % throughout (`sn:results/indomain/grid/scaling_curve_2026-09-17.json`) | SUPERSEDED [LEAK] [SEL-SPLIT]: v2 split each source separately (NHANES twins); each subset encoder kept its best epoch on the rows the evaluation then scored; every anomalous interval overlaps every other; v2 deleted 2026-09-20 |
| C2.2 | the reading "renders buy variant anatomy, not the film domain" | SUPERSEDED; the only render-ratio sweep ever run, on a superseded line |
| C2.3 | `eval_scaling_curves` devices axis at k = 1 for three held-out devices and k = 2 for Elekta only; `fewshot` never ran; `cases` needed a v8 encoder that did not exist then | PARTIAL; superseded by folder 01's lcurve / det_fill cells; whether `cases` ever ran NOT RECORDED |

### Track 5 band transfer (`results/track5_results/`; RECORD ONLY [WRONG-BANK])

Produced 2026-09-16 on allspine_v2 (`bank_audit_allspine_v2.txt`: 105,960 crops, 19,095 films) and
films_all2 (49,719 crops, 9,853 films), with a frozen script (`frozen_sha.txt`: `tools/recurrent_order.py`
sha256 `fc6e4ddc…`). What it showed and still means as a design fact: (1) the published protocol
(train at band 2k + 1, test at 2k + 1) is stable across ten seeds (sd 0.09-0.26 points, `REPORT.txt`
Part A) and the single-seed run would have picked the same k; (2) the train-band x eval-band matrix
shows training on short bands (k = 1, 2) transfers upward to long evaluation bands within about one
point while training on long bands loses 3-4 points on short ones (`REPORT.txt` Part B); (3) the
"seven vertebrae" cell of the published protocol has an **L5 dip** (66.81 % at train k = 3, eval k = 3,
against 87-89 % around it; BUU 41.30 % with every error called L4; `L5_DIP.txt`); (4) L6 and T13 had
**zero real training crops** (L6: 670 train, all renders; T13: 30 train, all renders;
`transitional_class_sources.txt`), which is why no film number for them exists; (5) GPU and CPU
re-runs of the same cell differ by a median 0.265 points, max 4.398 (`CROSSCHECK.txt`). The numbers
themselves are on a leaked bank and are not quoted anywhere.

### The mid-lumbar diagnosis (`results/lumbar_diag_2026-09-16/`; RECORD ONLY)

On the allspine_v2 r18_ce model (`lumbar_error_anatomy.json` names the bank and
`~/model_night/runs/result_r18_ce.json`): errors cluster by film (189 films with an error observed
against 257.6 expected if independent; permutation null [246, 268]; `lumbar_hypotheses.json`
`h1_clustering`), are monotone offsets rather than scrambles (439 monotone films, 179 non-monotone;
294 of the 316 wrong crops sit in the non-monotone films; `h1_monotone`), and a film-level decode
raised OVERALL exact from 0.9509 to 0.9880 (+3.71 points; L3 0.829 -> 0.973; chosen on half A,
+3.68; held on half B, +3.73; `per_level_before_after.csv`). The decode fixed 195 and broke 4 of the
"local" pattern films (`decode_by_film_pattern.json`). Crop statistics do not separate wrong from
right crops (`render/crop_stats_summary.json`). The design lesson (decode a whole film, not a crop)
survived into the recurrent and mixed-length heads; the numbers did not.

## 4. Superseded or wrong, in one list

| what was said | where | what is true | file |
|---|---|---|---|
| "98.7 / 99.1 / 99.4 % on films_all2" | `slurm/recurrent_head.sh` line 16; `tools/recurrent_order.py` line 56; `~/bench/model_registry.md` M96; `memory/xr-benchmark-and-robustness-2026-09-13.md` | measured on `films_ann`, a cervical-dominated 14-class bank; RECORD ONLY | C1.2; OQ F5 |
| "97.47 % at three vertebrae; quote the shortcut-free 99.02 %" | `memory/mixed-length-head-and-sota.md` | allspine v2 pooled NHANES twice; LEAKED | C1.6 |
| "99 % at 35.7 % coverage" | `memory/selective-prediction-the-honest-99.md` | leaked bank, coverage chosen on the scored half | C1.8 |
| "renders help at every N" (the ablation note) | `memory/film-ncurve-ablation-result.md`; `sn:REVISION_LOG3.md` section 13 | six help, one hurts (BUU at every person, 1.6 points, one seed) | A10.8, A10.9 |
| "99.14 against 71.67 % on 25 unseen spines" | older text | 24 of 25 spines were in the film detector's own lists; the 17-spine rerun is 99.4 against 67.7 % | A14.1, A14.2 |
| "renders buy variant anatomy" (the fraction sweep) | `memory/remedies-refuted-2026-09-17.md`; `ssn:paper/rsnai/graveyard.tex` line 65 | a selection-split number on a deleted leaked bank; never swept cleanly | C2.1, C2.2 |
| "femoral heads are outside the exposed anatomy on BUU" | an earlier draft of RESULTS.md section 4 | retracted in the file: heads inside the image bounds on 99.8 % of films; the skip rate of the annotation pilot is the measurement | RESULTS.md section 4 |
| "detect_v1 is the detector" | `results/spine_detector_report/` | detect_v2 (AP50 0.970) on the grid; detector_v5z is the SchwingNet body detector (folder 01) | `memory/xray-corner-detector-status.md` |
| "the Hugging Face mirror and Zenodo are v10" | `hf-mirror-is-v10` (folder 03) | Zenodo v11 published 2026-09-18 per four documents; the live state was not checked | OQ E7 |
