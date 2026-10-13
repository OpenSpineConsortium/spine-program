# STATUS for 99_archive (2026-10-08)

The results this folder holds are RECORD ONLY, SUPERSEDED, LEAKED or REFUTED. Each row carries its id in
`docs/handoff/RESULTS_CATALOG.md` ("RC"), the file that holds the number (grid paths spelled in full; repository paths
against spinesurg-ct-nnunet 097933a unless stated) and its status with the rigor marks of the catalog's "How to read a
row" ([THR], [SEL-REP], [WRONG-BANK], [LEAK], [SEL-SPLIT], [ONE-SEED], [AUTO-TRUTH], [DERIVED], [WORDING]). Nothing
below is quotable; the replacement, where one exists, is in `SUPERSEDED_NUMBERS.md`.

**2026-10-12, who reads what.** Greg answered OPEN_QUESTIONS A29 on issue #68, option (a): every Write holder may read all 13 folders; "Greg-only" and the label `greg-first` govern claiming and hand-outs, not reading. The `docs/handoff` copies keep their older wording.

## 1. The C-arm and film programme before SchwingNet (RC Part C, 2026-09-12 to 2026-09-22; the archive's own header)

### 1.1 Plain-film level identification and the early level models (RC C1)

| id | claim | file | status |
|---|---|---|---|
| C1.1 | context ladder on real films: one vertebra 96.7 %, three 98.8 %, five 99.1 %; lumbar one vertebra 80.7 % (85.4 % at 96 px) | `/wsu/home/go/go24/go2432/tmp/ladder_summary.json`; `mem:level-id-2d-results-2026-09-13.md` (in 01, 07) | RECORD ONLY; the `films_ann` bank is cervical-dominated |
| C1.2 | recurrent head over single-crop embeddings: 98.69 / 99.13 / 99.41 / 99.48 % at 3 / 5 / 7 / 9 vertebrae, n 8,422; 14 of 27 classes live; weights never saved; job 40215812 (2026-09-13) | `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json` | RECORD ONLY [WRONG-BANK]: ran on `films_ann_fov96_ctx`, not `films_all2`; three files still say `films_all2` (OQ F5; `TODO.md` step 5) |
| C1.3 | the `films_all2` head: 98.84 / 99.13 / 99.42 / 99.38 | `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent_all2.json` | RECORD ONLY |
| C1.4 | whole-spine 27-class single crop 78.74 % [78.11, 79.37], n 16,392; T13 0.0 % (n 14); L6 64.4 % | `/wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json` | RECORD ONLY [LEAK] (allspine_v2) |
| C1.5 | restored recurrent head on allspine_v2: 83.38 / 86.12 / 86.16 / 88.95 % at 3 / 5 / 7 / 9; T6-T8 floor 62-65 %; job 40293790 | `/wsu/home/go/go24/go2432/model_night/recurrent_allspine_v2.json` | RECORD ONLY [LEAK] |
| C1.6 | mixed-length head 97.47 / 98.45 / 99.29 / 99.92 at 3 / 5 / 7 / 9; random window 99.02 % | `mem:mixed-length-head-and-sota.md` (in 01, 07); `tools/head_mixed_length.py` | SUPERSEDED [LEAK]: the bank pooled NHANES II twice; the per-source clean v2 numbers (CSXA 99.87 %, BUU 98.04 %) are in "Numbers deliberately absent" |
| C1.7 | Star Temporal Classification loses to cross-entropy everywhere; transitional 22-24 % against 39.8 % | `/wsu/home/go/go24/go2432/model_night/stc/`; `mem:stc-does-not-transfer.md` (in 01, 07) | REFUTED |
| C1.8 | selective prediction: 99 % accuracy at 35.7 % coverage (exact level), 55.7 % (region); AUGRC 0.0466; job 40291753 | `/wsu/home/go/go24/go2432/selective/SELECTIVE.md`; `tools/level_selective.py` | NOT QUOTABLE [LEAK][SEL-REP]: computed on the leaked v2 bank's own test half with coverage chosen there (`docs/MODEL_CARD.md` section 5.3); no clean re-run (OQ C13) |
| C1.9 | model-night arms: CORN 78.44, ordinal focal 75.05, frozen 30.12 %; four ViT arms produced no result | `docs/MANIFEST_DATA_MODELS_RESULTS.md` sections 5.2, 7.2 | RECORD ONLY |
| C1.10 | corruption suite: `films_all2` rung 1 clean 99.10 %, over-exposure severity 5 16.93 %; augmentation tier 2 79.18 % | `/wsu/home/go/go24/go2432/bench/robust/*.json` | RECORD ONLY |
| C1.11 | FluoroCap literature panels: 19.7 % agreement with weak labels, n 7,065; resolution does not move naming (-0.33 points paired) | `/wsu/home/go/go24/go2432/model_night/panel_stats/`; `memory/fluoro-panel-gap-diagnosed.md`; `docs/checkpoints/MORNING_BRIEF_2026-09-16.md` | not an accuracy: FluoroCap is figures of published articles, 72.8 % of panels with zero pixel residual |
| C1.12 | LSTV / TLTV 2-D flags: CTSP AUC 0.577 [0.480, 0.669] (contains 0.5); VerSe 0.724; sex as positive control 0.951 on renders / 0.829 on real BUU | `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md` | REFUTED as a flag |
| C1.13 | LSTV flag learning curve, VerSe held out (67 patients, 31 positive): 10 positives AUC 0.652, 20 0.688, 40 0.704, 80 0.685, 120 0.713 | `docs/MANIFEST_DATA_MODELS_RESULTS.md` L659; `/wsu/home/go/go24/go2432/lstv_flag/LEARNING_CURVE.md` | RECORD ONLY; date and job not recorded |
| C1.14 | feasibility interior windows: v2 ordinary lumbar 91.8 % [89.4, 94.1]; anomalous 66.0 % (12 films); v6 anomalous interior 49.9 % [41.5, 58.9] (128 films); job 40321368 | `/wsu/home/go/go24/go2432/model_night/interior_windows/`; `mem:feasibility-claims-measured.md` (in 01, 07) | RECORD ONLY [LEAK] |
| C1.15 | remedies (film-noise randomisation, pretrain on renders, renders mixed 8 epochs, anchored-only admission) all lose to the v2 baseline | `mem:remedies-refuted-2026-09-17.md` (in 01, 07) | REFUTED on a leaked bank; not re-run on v9 (`TODO.md` step 7) |
| C1.16 | whole-film benchmark: v2 99.96 % = the sacrum-count rule 99.96 %; saturated; job 40323179 | `tools/benchmark_cina.py`; the same note | RECORD ONLY |
| C1.17 | re-implemented published competitors (ours, cina, kim, vertx, konya; 124 cells) and their ensemble | design `docs/COMPETITOR_BENCHMARK.md`; output `/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` | NOT RECORDED in any repository document; whether the output file exists is unknown |
| C1.18 | two-mechanisms table: L6 44.9 % in State C; one body 72.9 %, five bodies 97.0 %, whole 98.2 % | `mem:two-mechanisms-thesis.md` (in 01) | SUPERSEDED (the framing still governs paper 1) |
| C1.19 | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | `mem:xray-corner-detector-status.md` (in 07) | DATED |

### 1.2 The 2026-09-17 synthetic / real fraction sweep (RC C2)

| id | claim | file | status |
|---|---|---|---|
| C2.1 | six encoders on subsets of the v2 bank, scored on 455 held-out real lumbar films: render fraction 0 / 0.25 / 0.5 / 1.0 at real 1.0 gave ordinary 89.5 / 87.7 / 87.4 / 88.2 % and anomalous (12 films, 47 windows) 34.0 / 44.7 / 53.2 / 36.2 %; real 0.5 and 0.25 at render 1.0 gave ordinary 84.3 / 83.7 %, anomalous 53.2 / 38.3 %; cervical 97.1-98.8 % | `SchwingNet/results/indomain/grid/scaling_curve_2026-09-17.json` (copy of `/wsu/home/go/go24/go2432/model_night/scaling/SCALING_CURVE.json`); `paper/rsnai/graveyard.tex` L65 | SUPERSEDED [LEAK] [SEL-SPLIT]: v2 split each source separately (NHANES twins across the split); each subset encoder kept its best epoch on the rows the interior evaluation then scored; every anomalous interval overlaps every other; `SchwingNet/results/indomain/INVENTORY.md` L299-304 marks every row NOT ESTABLISHED; job id not recorded; whether `fig9_scaling` was drawn not recorded |
| C2.2 | the reading at the time: "renders buy variant anatomy, not the film domain" | same | SUPERSEDED; the only render-ratio sweep ever run, on a superseded line |
| C2.3 | `eval_scaling_curves` devices axis at k = 1 for three held-out devices and k = 2 for Elekta only; one derivable cell: Elekta held out, Cios-only design-A model 38.1 % [32.3, 44.5] at 0.25 | foot of `slurm/eval_scaling_curves.sh`; `SchwingNet/results/indomain/INDOMAIN.md` L13 | PARTIAL; superseded by the lcurve / det_fill cells; whether `cases` ever ran NOT RECORDED |

### 1.3 Pointers to the rest of Part C (owned elsewhere; all RECORD ONLY or superseded)

RC C3.1-C3.13, the sweep / chain / confirmation line (private; owned by 01): sweep_v3 naming 72.1 to 95.2 % on 120
held-out CTSP spines, chain 97.5 %, job 40384843; counting with boxes given 99.66 % of 6,255 walks; counting with detector
boxes 30.06 % (REFUTED as deployable); guided acquisition NOT RECORDED; runtime 422.6 s per pair full resolution against
575 ms reduced, the "same answer" claim withdrawn. RC C4.1-C4.11, DeepFluoro and devices (owned by 08): render-only
detector sacrum recall 76.9 % by specimen 47.8-96.2 %; "calibrate, don't learn" stands with its numbers RECORD ONLY;
styled-corpus LODO rows SUPERSEDED by the contribution-matrix scoring; C4.11 the translation levers (CycleGAN and ADDA
refuted) is a CURRENT finding. RC C5.1-C5.3, the CT ablations (owned by 03): six nnU-Net ablation runs (catalog C5.1) NOT RECORDED; the grid holds five arm
directories under `/wsu/home/go/go24/go2432/ablate`, 201.6 GB (`MANIFEST_GRID.md` section 3; runs and directories are different counts); L6 pseudo-Dice 0.000 under 12x duplication (DATED); the Dataset810 one-shot run retired for
Dataset813, folds NOT RECORDED, so no evaluated single-shot model exists on disk (contradiction C17 with the RPPR and the
CNS 66629 title).

## 2. Superseded C-ArmLSpine rows still printed somewhere (RC Part A; owned by 01)

| id | claim | file | status |
|---|---|---|---|
| A2.9 | first zero-shot run on `allspine_v2_r1`: 594 / 617 (96.3 %) lateral, 239 / 631 (37.9 %) AP | `SchwingNet/results/a7.json#cells/zeroshot2~1det~1{LAT,AP}~1kfull`; `docs/carmlspine_zeroshot2_pooled_all_2026-09-21.json` | SUPERSEDED (the encoder's bank was deleted; UNRESOLVED U1); still printed in `SchwingNet/tables/tab3_naming.md` and the three `atlas/model.json` copies (`TODO.md` step 4) |
| A3.11 | v2-lineage cross-validation: lateral 606 / 617 (98.2 %), AP 96.7 %, k5 97.0, k3 92.9, k1 72.8 | `docs/carmlspine_cv5_mixed_2026-09-21.json`; printed in `docs/checkpoints/DAILY_REPORT_2026-09-22.md` | SUPERSEDED by A3.1 (601 / 617 = 97.4 %); still in the stale twins |

## 3. The refuted routes and rules

| what | number | file | status |
|---|---|---|---|
| SDXL img2img render-to-fluoroscopy translation | dead at every strength | `memory/fluorogen-synthetic.md`; `RESEARCH_DIRECTIONS.md` section 2 table (FGS) | REFUTED |
| CUT (contrastive unpaired translation) | moved the films-only model 12.1 to 14.1 % and dropped the render-trained one | same | REFUTED (not a lever) |
| CycleGAN and ADDA | indistinguishable from none; the published SyntheX line gives 6.62 and 6.41 mm against 6.44 with no translation | `mem:drr-to-fluoro-levers.md` (in 01, 08); RC C4.11; `RESEARCH_DIRECTIONS.md` section 1 row SyntheX | REFUTED |
| Star Temporal Classification loss | loses to cross-entropy everywhere (C1.7) | `/wsu/home/go/go24/go2432/model_night/stc/` | REFUTED |
| the R + C = 22 rule | one count; computable on 14 of 1,175 spines (1.2 %; VerSe 14 / 374, CTSP 0 / 801); C1 is labelled on every VerSe case carrying C2, so a detector that boxes C1 flags every normal spine (specificity 0.000); job 40414996 | `docs/ANOMALY_RULE_EVALUATION.md`, `anomaly_rule_evaluation.json`; `tools/eval_anomaly_rule.py`; RC D.24 | REFUTED; removed from the manuscript on Greg's order |
| the pelvic Castellvi cues on CTSP | ala rise AUC 0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599 | `docs/CASTELLVI_SCREEN_BLIND_SPOT.md` in CTSpinoPelvic1K 7ddfe38; RC D.21 | REFUTED cues |
| sacral foramina counting | 93 cases x 81 settings; best 31-39 % per case | `docs/LAB_JOURNAL.md` "Negative results" and `scripts/sweep_foramina_params.py` in CTSpinoPelvic1K 7ddfe38; RC F.39 | REFUTED |
| the 2-D LSTV / TLTV flags | CTSP AUC 0.577, interval containing 0.5 (C1.12) | `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md` | REFUTED as a flag |
| a learned refiner as the 2-D reference | 68.1 % explained against 69.3 % calibrated; better on 21 % of frames only (C4.2) | `mem:learned-formation-refuted-calibrate-instead.md` (in 01, 08) | REFUTED; "calibrate, don't learn" stands |
| decoder-named pseudolabels; size in millimetres as a scalar | no number on disk | `RESEARCH_DIRECTIONS.md` section 3.5 ("Excluded by the record") | excluded by the record |
| the 734x linker speed-up as a shipped timing; any guided-loop corpus number | RECORD ONLY (C3.13; C3.12 NOT RECORDED) | `docs/MODEL_CARD.md` section 6.3; `docs/GUIDED_ACQUISITION.md` STATUS | not to be carried forward (`README.md` section 4 list 1) |

## 4. FluoroCap: the numbers that describe the dormant line (descriptive, not accuracies)

| what | number | file |
|---|---|---|
| the frozen release of 2026-09-13 / 14 (named on disk `FluoroCap_v0.1_A` and `_B`) | 4,979 figures, 2,205 articles, 10,281 panels; A 2,531 included, B 991 licence-clean | `memory/fluorocap-dataset.md`; `benchmark/data/fluorocap_v0.1/stats.json`, `LOCK_A.json`, `LOCK_B.json` |
| panel images on disk at QC | 11,349 | `docs/fluorocap/FLUOROCAP_QC_2026-09-14.md` section 1 |
| reproductions | 72.8 % of panels have zero pixel residual against the printed figure | `mem:fluorocap-is-reproductions-not-fluoroscopy.md` (in 01); `docs/handoff/DATASET_USAGE.md` section 2.1 |
| manifest rows and panels counted by the usage table | 29,500 panels (21,603 manifest rows); `fluorocap_fov96_ctx` 2,385 crops went into allspine_v7 | `docs/handoff/DATASET_USAGE.md` section 2.1 |
| still inside the C-ArmLSpine fold banks | 2,100 crops of 950 panels per fold bank (job 40416442) | `docs/handoff/DATASET_USAGE.md` sections 0.4, 3.2 |
| human-verified level reads | 0 | `docs/fluorocap/FLUOROCAP_QC_2026-09-14.md` section 8 ("What is not known"), line 166: "No panel has been read by a human" |
| the pathology-source sweep | 366 sources, 534 literal queries, eleven search angles; the skeptic pass of the clinical entries never ran | `docs/fluorocap/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` |
| the resolution ladder of 2026-09-16 | 1,467 paired panels / 6,652 vertebrae, 36 to 88 px: -0.33 points (CI95 -0.88, +0.22); the detector returned nothing on 60 then 39 of 397 paired panels (McNemar z 3.38) | `docs/checkpoints/MORNING_BRIEF_2026-09-16.md` (RECORD ONLY) |
| the TTA + monotone decode of 2026-09-16 | 95.09 % to 98.80 % (n 7,339), "largely BUU" | same (RECORD ONLY [LEAK]: the v2-era banks) |

## 5. The talks, manuscripts and submissions recorded here

| item | state | file |
|---|---|---|
| AACA 2026 Tech Fair deck, "Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection", 15 slides | presented (43rd AACA meeting, Mayo Clinic, 13 June 2026; file dated 2026-07-24); built on third-party segmenters; discloses neither Part A nor Part B; title slide says Neurosurgery (C5); nothing to redo | `manuscripts/talks/TechFair_LSTV_Schwing.pptx`; `docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md` section 14 |
| MLHC 2026 research-track submission, "CTSpinoPelvic1K: A Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation", 1,137 volumes, 804 patients, 10-class labelmap | rejected (`memory/publication-roadmap.md`, 2026-07-24); `docs/ROADMAP.md` in CTSpinoPelvic1K still says "in review, score 2.75/4" (stale, C8); the decision letter's location not recorded; never cite it as under review | extract section 8; the PDF and source are owned by 03 |
| CNS 2026 decks v2, v3, v9, v10, v11 | superseded; v3 / v9 / v10 disclose Part B (private); v12 public is the current deck (03); whether the slides were submitted and by what deadline is not recorded (OQ A23) | `manuscripts/talks/README.md`; extract section 13.2 |
| the older C-arm drafts (`paper/rsnai/main.tex` 6506470; `main_v2.tex` c508f5b, 54 / 54 claims verified by job 40414708; `paper/focused/main.tex` f61cd72) | superseded by SchwingNet (`SchwingNet/main.tex`); copies in 01 | extract section 4 |
| the NIH F30 year-4 report (RPPR, 24 July 2026) | sent; says a single-shot CT model was "developed and validated" while no evaluated single-shot model is recorded on disk (C17); nothing to redo | extract section 18 (files owned by 03) |
| the May 2026 action items and agenda | superseded by the v10 / v11 build; the 45 VerSe L6 cases and the NeurIPS merge they planned are history (the VerSe L6 count itself is unsettled: 85, 47, 50 or 87; `RESEARCH_DIRECTIONS.md` section 8 unknown 17) | `docs/early_scratch_2026-05/` |
| the 2026-02-14 DICOM dual-view crosshair bug | fixed in the viewer JS kept here; superseded by the NiiVue PACS demo (12) | `code/fuc/` |

## 6. Superseded by what, in one line each

The v2-lineage C-ArmLSpine numbers by the v9 lineage (A2.1, A2.2, A3.1, A3.3); the film heads of September by the film
N-curve on held-out persons (A10.1 to A10.3); the leaked-bank remedies by nothing yet (`TODO.md` step 7); the FluoroCap
training use by directive D1 (test set at most); the translation routes by the measured levers (fidelity, strong domain
randomisation, scale; `mem:drr-to-fluoro-levers.md`); the R + C = 22 rule and the pelvic cues by the ruleclass
pre-registration draft (06); the September decks by `CNS2026_Schwing_NotAllSpines_public_v12.pptx` (03); the MLHC
submission by the Medical Physics article (03); the March arXiv draft and the April repositories by CTSpinoPelvic1K at
7ddfe38; the annotator of April by `review_service/` (03 / 11); the FUC viewer by the NiiVue PACS demo (12).
