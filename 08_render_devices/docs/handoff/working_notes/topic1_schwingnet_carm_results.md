<!-- spine-program/08_render_devices: copy of spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic1_schwingnet_carm_results.md (copied 2026-10-08; redactions, if any, are listed in MANIFEST_LOCAL.md section 3). Laptop spellings of the path prefixes (`C:/` drive paths, the session scratchpad, the memory folder) are history, not dependencies: read them through this folder's CLAUDE.md "Prefixes in the copied documents". -->

# Topic 1 — SchwingNet and the C-arm program: every result, where it lives, how it was made, and whether it still stands

Written 2026-10-08 for the hand-off Greg asked for ("summarize how i arrived at all my results and where they are
located and recipes for regenerating them ... dont leave anything out"). Read-only: nothing was run, nothing on the
grid was touched. Every entry names the file that holds it.

**Path conventions.** Paths are relative to `<laptop:Desktop>/spinesurg-ct-nnunet` (private repository,
branch `L6_Class`) unless they begin with:
- `memory/` = `<laptop memory folder>/`
- `~` = grid HOME `/wsu/home/go/go24/go2432` (exists only on the grid)
- `/rs/` = grid Ceph `/rs/rs_grp_oschome/go2432/...` (exists only on the grid)
A `#` after a file is a JSON pointer, as `SchwingNet/NUMBERS.md` uses them.

**Status words used below.**
- **CURRENT** — printed in the manuscript as last built (grid builds 40483839 review / 40483840 camera-ready,
  2026-09-27; commit 05e05dc message).
- **CURRENT, SELECTION SPLIT** — printed, but measured on the split that chose the checkpoint, and labelled so.
- **HELD OUT, NOT QUOTED** — passes the evaluation gate, sits in a result file, not in the text.
- **SUPERSEDED** — replaced by a named later number; do not quote.
- **LEAKED / UNRESOLVED** — the evaluation gate's verdicts (`SchwingNet/results/eval_gate/EVAL_LEAKS.md` §"The verdicts").
- **REFUTED** — the hypothesis it supported was tested and failed.
- **PAPER 2** — belongs to the LevelCheck comparison moved out on 2026-09-24 (`SchwingNet/PAPER1_SCOPE.md`).
- **RECORD ONLY** — pre-SchwingNet exploration; kept for history, not quotable.

---

## 0. The five files to open first

| file | what it is |
|---|---|
| `SchwingNet/NUMBERS.md` | every number the manuscript has ever printed, row by row, with the file and JSON path it is read from; sections are dated and rows that left the text are marked SUPERSEDED. The section headings below its first section still carry OLD figure/table numbers (its own lines 33-36 say so). |
| `SchwingNet/numbers_manifest.json` + `SchwingNet/generated/numbers_audit.md` | the 74 keyed numbers and 5 figures the LaTeX build reads at compile time (`\RESULT{key}`), each with file, pointer, job and note; the audit file records the compiled value and the source file's SHA-256 (generated 2026-09-27T17:15:44Z). |
| `SchwingNet/results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` | the 2026-09-27 manifest answering "how does it do at each level, in each domain, at each angle, and do renders help" (commit 4e3fe93), with held-out vs selection-split marked on every row. |
| `SchwingNet/results/eval_gate/EVAL_LEAKS.md` + `SchwingNet/results/eval_gate/closure/MANUSCRIPT_CORRECTIONS.md` | the patient-keyed held-out audit of 563 quoted numbers and the re-runs that replaced the leaked or unresolved ones. |
| `SchwingNet/PAPER1_SCOPE.md` | what paper 1 may and may not report since the LevelCheck comparison became paper 2. |

Supporting: `SchwingNet/CLAIMS_LEDGER.md` (every "first"/superlative with its comparator and verdict; "The Discussion
is built from this file and nothing else", line 5), `SchwingNet/RESULTS_BUILD.md` (the results-to-PDF chain),
`SchwingNet/REVISION_LOG.md`, `REVISION_LOG2.md`, `REVISION_LOG3.md` (dated change logs, sections 1-13),
`docs/RESUME_2026-09-22_PM.md` (the resume file; newest block on top), `docs/MANIFEST_DATA_MODELS_RESULTS.md`
(the pre-SchwingNet 2026-09-16 inventory of every bank, model and result surface).

The memory note named in the task, `manifest-data-models-results`, does **not exist** in `memory/` (listed 2026-10-08:
165 files, none by that name). Its content is `docs/MANIFEST_DATA_MODELS_RESULTS.md` §1 and
`memory/recurrent-head-restored-2026-09-16.md` (section 5.1 below).

---

## 1. How the manuscripts relate (lineage of the result set)

| manuscript | file | title (from the file) | state | what it carried |
|---|---|---|---|---|
| chain paper | `paper/rsnai/main.tex` | "Naming Vertebrae Without an Anchor: Registration-Free Level Identification on Limited-Field Radiographs" (line 26) | superseded; last commit 6506470 2026-09-20 | feasibility / interior-window / v6 numbers (memory/feasibility-claims-measured.md "Deliverables") |
| focused paper | `paper/focused/main.tex` | "Making the Intraoperative Count Exact: Vertebral Level Confirmation from Overlapping ..." (line 37) | superseded; last commit f61cd72 2026-09-22 | sweep/counting/confirmation; the only "latency unmeasured" sentences (docs/MODEL_CARD.md §6) |
| QI paper | `paper/qi_universal_protocol/main.tex` | "The Universal Protocol with a level in it: site marking and time-out for spine ..." (line 21) | separate manuscript; last commit d4b895e 2026-09-22 | not a results paper (other topic) |
| k-devices concise draft | `paper/rsnai/main_v2.tex` (+ `claims.tex` from `docs/RSNAI_CLAIMS.json` via `tools/claims_fill.py`) | "Navigation from the C-arm alone: naming the vertebral level on any fluoroscope with a physics-parameterised synthetic corpus" | superseded by SchwingNet on 2026-09-22 (commit c508f5b); C7/C8 left as `\todo` | 54 claims in `docs/RSNAI_CLAIMS.json`; title page wrongly says "Department of Neurosurgery" (memory/user-affiliation-general-surgery.md says General Surgery) |
| **paper 1 = SchwingNet** | `SchwingNet/main.tex`, `SchwingNet/sections/*.tex`, `SchwingNet/supplement.tex` | "\netname{}: a convolutional-recurrent network for level naming in spine surgery" (main.tex line 61) | CURRENT; Radiology: AI Original Research | sections 2-4 below |
| **paper 2 = LevelCheck comparison** | `SchwingNet/paper2_levelcheck/` (`MOVED_FROM_PAPER1.md`, `numbers_manifest_moved.json`, `tables/tab_levelcheck.*`, `open_gate_40438004/`), `SchwingNet/LEVELCHECK_MODEL.md` (frozen), `SchwingNet/LEVELCHECK_CLAIM.md` | not titled in a file read | pending human reads | section 6 below |

Earlier "six-figure" plan (2026-09-23, memory/six-figure-paper-plan.md) became five figures + three tables on
2026-09-24 evening when Figure 6 / Table 3 moved to paper 2 (`SchwingNet/PAPER1_SCOPE.md`; memory/paper-split-2026-09-24.md).

---

## 2. Glossary needed to read any number

### 2.1 Models (the four shipped parts and their lineage)

| part | what was used for the CURRENT numbers | file that says so |
|---|---|---|
| naming (keypoint) detector | `detector_v5z_final` (`~/FluoroCap/detect_v5z_final_best.pt`, sha256 797de71a…), film-trained YOLO11m-pose, confidence 0.35 (the `tools/level_prototype.py` default); boxed 617 of 676 agreed lateral bodies | `SchwingNet/NUMBERS.md` statistical-revision row "the naming detector"; `docs/MANIFEST_DATA_MODELS_RESULTS.md` §5.3 (fine-tuned from detect_v3, 60 epochs, 2026-09-14) |
| sacrum / vertebra detector (anchor; Table S2 headline) | `rx_lodo_carmlspine_1024` = arm `lodo_carm`: YOLO11m on real COBRA2026 + DeepFluoro frames (3,094 = 2,832 + 262), C-ArmLSpine never seen; fine-tuned from the render-trained `pose/anchor_none_v2_17-1882` (itself from COCO yolo11m.pt); 80 epochs, seed 0, imgsz 1024 | `SchwingNet/NUMBERS.md` "Counts in Methods" rows on detector frames and detector; `SchwingNet/results/eval_gate/LINEAGE.md` rows `realxray/rx_*` |
| level encoder (zero-shot, Figure 2) | `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (ResNet-18, two-channel stem, 320 px crop, target 96 px, 27 classes C1-C7, T1-T13, L1-L6, sacrum) | `SchwingNet/results/learning/LEARNING.md` "What was run"; `SchwingNet/results/eval_gate/leaks/zeroshot_v9.json` |
| recurrent head | `head_allspine_v9_mixed_kmax4_seed0` (2-layer BiGRU over 2-9 bodies, trained by `tools/head_mixed_length.py --train-mode mixed`) | `SchwingNet/results/eval_gate/EVAL_LEAKS.md` U1 replacement table |
| fold models (fine-tuned CV) | `v9init_pre`: the same merged fold banks, directories, epochs, seeds and prototype defaults as the shipped folds, but the encoder fine-tuned from `allspine_v9` instead of `allspine_v2_r1` | `SchwingNet/results/eval_gate/closure/cv_v9/CV_V9.md` header |
| count and coupling | no learned parameters: `tools/count_from_sacrum_eval.py` (ordinal from the detected sacrum), `tools/alphabet_couple.py` (chooses ordinary / L6 / T13 / both alphabet from the classifier posteriors; disagreement = stop) | `SchwingNet/results/COUNTING.md`; `SchwingNet/results/COUPLING.md` |

Superseded encoder: `allspine_v2_r1` (`~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt`). Its training bank was
deleted, so every number from it is UNRESOLVED (EVAL_LEAKS U1: 57 of 58 unresolved quoted rows trace to it).

### 2.2 Banks (crop banks that train the level encoder)

| bank | what is in it | status | file |
|---|---|---|---|
| `films_ann_fov96_ctx` | CSXA cervical + NHANES II only; 14 of 27 classes live; val 8,422 crops, 93.8 % cervical | record only | `docs/MANIFEST_DATA_MODELS_RESULTS.md` §1.2 |
| `films_all2_fov96_ctx` | + BUU/VinDr; same 8,422-crop val as films_ann | record only | same, §1.1, §5.2 |
| `allspine_fov96_ctx` (v1), `allspine_v2/v3/v4/v5/v5c/v6/v7` | whole-spine 27-class banks mixing films and renders | v2, v6, v7 LEAKED (NHANES twice; CTSpinoPelvic1K under two names); banned from the manuscript | `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`; `SchwingNet/NUMBERS.md` line 11-12 |
| `allspine_v8` | patient-keyed rebuild (`slurm/allspine_v8_{clean,bank,train}.sh`); clean for film, but VerSe keyed by series | film numbers (a5) quotable as selection split; VerSe numbers banned | `SchwingNet/results/a5.json#leak_check_by_patient_key`; `SchwingNet/NUMBERS.md` line 12 |
| `allspine_v9` | v8 with VerSe re-keyed by subject; the CURRENT encoder lineage | its validation split is the checkpoint-selection split (Figure 2 is labelled so) | `SchwingNet/results/eval_gate/EVAL_LEAKS.md` L5 |
| G3 split banks (`results/fig6/bank_g3_v2`, `dual_loss/g3clean_v2`) | the person-disjoint subtype-stratified split built 2026-09-23 for the transitional test (paper 2 arm, ImageNet init) | development curve only in paper 1 | `SchwingNet/results/rare_class/split_plan.md`; `SchwingNet/results/dual_loss/saturation.json` |

### 2.3 Truth and conventions

- **C-ArmLSpine truth** is two automatic CBCT labellers (TotalSegmentator and SPINEPS+VERIDAH) scored only where they
  agree: 910 vertebrae, 814 agreed (89.5 %), T11 0/3, T12 6/63 agreed — the filter removes the thoracolumbar junction.
  No level truth in the study was set by a human (`docs/MODEL_CARD.md` §5.1; `docs/DATASHEET.md` §2.3).
- **PRE vs REP truth.** PRE = the export as it was when the old numbers were scored
  (`realxray/carmlspine_pre_repair_2026-09-23`); REP = after the 2026-09-23 repairs. Every C-ArmLSpine naming number in
  the text is on PRE truth; REP numbers sit in `cv_v9.json#families/rep:*` and are not quoted (`SchwingNet/NUMBERS.md`
  G5-fill "NOT used" row).
- **Box conventions.** WV/outline = whole vertebra projected from CT/CBCT labels; BODY = vertebral body (A28 convention,
  SPINEPS corpus instance, `tools/body_masks.py`). The two cross on every device: arms trained on body truth read ~90 %
  body / ~40 % outline on C-ArmLSpine; render/COBRA/DeepFluoro arms read the reverse (80.5 % outline / 5.2 % body for the
  reported held-out detector) (`SchwingNet/results/bodybox_rescore/RESCORE.md` "The finding, stated plainly").
- **Operating points.** 0.25 = YOLO default; 0.74 = "cross-device" (best pooled vertebra F1 of the `lodo_carm` arm over
  its sweeps on COBRA2026, DeepFluoro and the Geneva phantom; no C-ArmLSpine frame, but adopted as headline after the
  0.25 result was seen, so it must be written "cross-device", never "pre-stated" or "fixed beforehand") (`SchwingNet/results/a1.json#operating_points`; `SchwingNet/CLAIMS_LEDGER.md` §1 row 1, REVIEW_STATS F16);
  0.60 = own best F1, test-tuned, a bound only; 0.05 = film-detector comparisons; 0.35 = keypoint detector default.
- **Repaired detection denominator** (2026-09-25): keep a truth vertebra if complete (not cut by the CBCT), not a
  fallback box, ≥ 80 % visible and body area ≤ outline area: 287 → 214 (dropped 73: cut 66, fallback 6, visible < 0.8 7,
  body larger 11; reasons overlap) (`SchwingNet/results/indomain/DENOMINATOR_REPAIR.md`).

---

## 3. Paper 1 (SchwingNet) — what is printed now

### 3.1 Shape, limits and last build

- Five figures (1 phenotypes, 2 embedding, 3 network, 4 one exposure, 5 persons/views/angles), three tables
  (1 = `tables/tab_corpus.tex` image sources, 2 = `tables/tab4_transitional.tex` transitional persons, 3 =
  `tables/tab3_naming.tex` naming/counting/coupling) (`SchwingNet/main.tex` lines 125-227).
- Supplement: Figures S1-S5 = `fig2_flow`, `figS1`, `figS2`, `figS3`, `figS4` (the figS<n> file names are printed as
  S<n+1>; `SchwingNet/NUMBERS.md` lines 23-27); Tables S1 `tabS1_device_terms`, S2 `tab2_detection`, S3 `tabS3_corpus`,
  S4 `tabS4_ablation` (`SchwingNet/supplement.tex` lines 257, 320-322).
- Last build: grid jobs 40483839 (review) → 40483840 (camera-ready), 2026-09-27: main 23 pages, **supplement 13 pages**,
  0 LaTeX warnings, RESULT_PENDING 0 (commit 05e05dc message). The journal's supplement limit is ≤ 12 pages
  (`SchwingNet/RSNA_AI_REQUIREMENTS.md` line 21); the previous build 40449056/57 was 23 + 12 (`SchwingNet/REVISION_LOG3.md`
  §12). **The supplement is one page over after the ablation was added — open defect.**
- Body word count: commit 044ca9a (2026-09-25) says "body 3,000 / 2,988"; `PER_LEVEL_DOMAIN_ANGLE.md` (2026-09-27) says
  "2,998 / 3,000". Which is current after the 2026-09-27 Discussion sentence: not recorded (see unknowns).
- Packets: `SchwingNet/packet/` (review) and `SchwingNet/packet_cameraready/` (docx manuscript, figures, cover letter,
  title pages, CLAIM checklist, ATLAS cards); PDFs in `SchwingNet/packet_build/` (latest names dated 2026-09-27).
  Built by `SchwingNet/tools/make_packet.py`; one source, `\ifcameraready` flag (`REVISION_LOG3.md` §10).
- One placeholder remains in the manuscript sources: `\PENDING{G0}{VinDr determination number and date}`, which takes HPR 2026-330 and 29 September 2026 (Ethics
  paragraph, `main.tex` line 137); none in Results, the supplement or the printed tables (grep 2026-10-08), and
  `generated/pending.json` resolved every `\RESULT` key on 2026-09-27.

### 3.2 Figure / table → tool → data map

| printed item | tool | data it reads | record of drawn numbers |
|---|---|---|---|
| Figure 1 phenotypes | `SchwingNet/tools/figure1.py` (panels by `tools/figure1_panels.py` on the grid) | CT, renders, films of four persons | `SchwingNet/figures/figure1.record.json` |
| Figure 2 embedding | `SchwingNet/tools/figure2.py` + `figure2_analyse.py` (+ `figure2_transitional.py`; grid `tools/fig2_heldout_embed.py`, `fig2_occlusion_clean.py`) | `SchwingNet/results/figure2/figure2_metrics.json`, `figure2_transitional.json`, `zones_lateral_clean.json`; embeddings from grid jobs 40416675 (GPU) / 40416700 (CPU) (`results/learning/LEARNING.md`) | `SchwingNet/figures/figure2.record.json` |
| Figure 3 network | `SchwingNet/tools/figure3_network.py` | none (schematic) | `SchwingNet/figures/figure3.record.json` |
| Figure 4 one exposure | `SchwingNet/tools/figure4_frame.py --models v9init_pre [--pull]` | `results/eval_gate/closure/cv_v9/` (v9init_pre folds, PRE truth), `coupling_pre/coupling.json` | `SchwingNet/figures/figure4.record.json` |
| Figure 5 persons, views, angles | `SchwingNet/tools/fig_power.py` (local, 2026-09-25 13:41) | `results/power/power.json` (written by the tool), `results/coverage/film_ncurve/film_ncurve.json`, `results/indomain/name_fill.json`, `results/indomain/det_fill.json`, `results/coverage/experiment/runs/cov_surgio_b51_dr_*/unseen/recall_vs_angle.json`, `results/coverage/pooled_fit.json` | `SchwingNet/figures/figure5.record.json` |
| Figure S1 flow | `SchwingNet/tools/fig2_flow.py` | splits, datasheet | — |
| Figures S2-S5 | `SchwingNet/tools/figS_supplement.py s1|s2|s3|s4|all` | `results/manifold/probes.json`, `results/supplement_figs/`, `results/contribution_matrix.json`, `results/arc/` | `SchwingNet/figures/figS<n>.record.json` |
| Table 1 | hand-built; every cell traced | `SchwingNet/tables/tab_corpus.sources.md` | — |
| Table 2 | from the subtype table and split | `results/rare_class/transitional_subtypes.csv`, `results/rare_class/split_plan.md`, `figures/figure5.record.json` | `tables/tab4_transitional.sources.md` |
| Table 3 | from cv_v9 closure, counting, coupling | `results/eval_gate/closure/cv_v9/cv_v9.json`, `results/counting.json`, `results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` | `tables/tab3_naming.sources.md` |
| Table S1 | `SchwingNet/tools/make_supp_device_table.py` | `docs/devices/{bv_pulsera,cios_fusion,elekta_xvi,pixium_4600}.json` | — |
| Table S2 | hand-built | `results/a1.json`, `results/lcurve/lcurve.json`, `results/contribution_matrix.json`, `results/a3.json` | `tables/tab2_detection.sources.md` |
| Table S3 | `SchwingNet/tools/make_supp_census_tables.py --merged` | `results/age_sex_by_source.json`, `results/corpus_census.json` | — |
| Table S4 | `SchwingNet/tools/make_supp_ablation_table.py` | `results/coverage/film_ncurve/ablation/*` | — |

`fig_power.py` no longer contains the stop on `auto_reference.json` that `docs/RESUME_2026-09-22_PM.md` (09-24 15:47
block) and `PAPER1_SCOPE.md` item 4 describe (a grep of the tool for "auto_reference" finds nothing, 2026-10-08).

`SchwingNet/figures/FIGURES.md` still describes the 2026-09-22 four-figure set (Figure 3 naming, Figure 4 detection
"pending Greg's verdict") and is stale; `SchwingNet/README.md` says so in its own preamble.

---

## 4. Results catalog — every number in paper 1, by question

Each row: the claim with its number; the file; model/bank/truth; tool and job; status; where printed. Intervals are
2,000-resample case-cluster (or patient-cluster) bootstraps, percentile unless marked BCa or Wilson.

### 4.1 What the encoder learned (Figure 2) — CURRENT, SELECTION SPLIT

| claim | number | file | notes |
|---|---|---|---|
| nearest crop of another person is the same level | 9,740 of 13,009 (74.9 %) [72.2, 77.6], 1,612 persons; within one 93.8 % [92.7, 94.9] (cut from text) | `SchwingNet/results/figure2/figure2_metrics.json#nearest_other_person` | 2,889 crops of 164 persons in the training keys dropped first (`#cleaning`) |
| L6 separates from L5 more than L2-L5 from the level above | silhouette L6/L5 0.35 [0.31, 0.39], 98 crops, 10 persons; leave-person-out 0.34 [0.30, 0.38]; L5/L4 0.23 [0.21, 0.25]; L4/L3 0.17, L3/L2 0.16, L2/L1 0.19; L1/T12 0.32 [0.29, 0.35] | same `#silhouette/pairs/*`, `#heldout_l6/ladder_against_level_above/L6|L5/validation_leave_person_out` | abstract, Key Point 3, Results |
| classifier calls | 75 of 98 L6 crops named L6; 111 of 1,012 L5 crops named L6 | same `#validation_neighbours_and_calls/{L6,L5}` | Results |
| within one render source | VerSe renders 0.52 [0.45, 0.57] vs control 0.38 (10 persons); physics_rare 0.24 [0.20, 0.29] vs 0.16 (8); physics_drr **reversed** 0.14 [0.11, 0.20] vs 0.21 (5 persons, 11 crops) | same `#silhouette_within_source/sources` | supplement "Transitional crops" |
| never-seen L6 (C-ArmLSpine case42, case121, case136) | two-cluster silhouette 0.10 / 0.12 / 0.16 vs validation L6 0.34; their L3-L5 −0.09 to −0.01; 84 of 180 crops named L6; under the body box −0.07 and 13 of 180 | same `#heldout_l6`; `figures/figure2.record.json#never_seen` | HELD OUT (EVAL_LEAKS item 5: CLEAN for v9); one labeller's read only; supplement |
| fused L5 (four validation persons) | last free vertebra nearer L5 in 2 of 4 (−0.13, −0.18; both crops named L5); ordinary L4 0.24 (70 of 1,066 crops below zero); control L3 0.01 and −0.26 | `SchwingNet/results/figure2/figure2_transitional.json#fused_L5` | supplement |
| occlusion attribution | target enrichment 1.39-4.51 over six levels (T12 1.89, L3 2.26, L4 1.69, L5 1.39, L6 1.47, sacrum 4.51); for L4-L6 more attribution on the body below (36-43 %) than on the target (24-32 %) | `SchwingNet/results/figure2/zones_lateral_clean.json#sets/v9_val/<level>/maps/occlusion` | Results |
| no T13 crop in validation | 44 T13 crops in training, 0 in validation | `figure2_metrics.json#bank_transitional_census` | Results ("No T13 crop was outside training") |

Gate verdict: every Figure 2 number except the never-seen rows is LEAKED in the sense of "scored on the selection
split" (1,612 of 1,612 persons in v9's VAL set) — `EVAL_LEAKS.md` L5. The text labels it "checkpoint-selection split".

### 4.2 Zero-shot naming on the unseen C-arm (C-ArmLSpine, Surgio-B51) — CURRENT, HELD OUT

Model: v9 encoder + v9 head, no C-ArmLSpine frame in training; naming boxes from `detector_v5z_final` at 0.35; PRE truth.
File: `SchwingNet/results/eval_gate/leaks/zeroshot_v9.json` and `results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:zeroshot_v9_existing`, `#pre:zs_v9head`.

| claim | number | printed |
|---|---|---|
| lateral, whole frame | 595 / 617 (96.4 %), 141 cases (6 with an error); Wilson on n_eff [92.3, 98.4] (ceiling regime, design effect 3.84); percentile [93.3, 98.9]; BCa [92.5, 98.7]; answered 83.0 %, exact on answered 97.7 % | Key Point 1, abstract, Results, Table 3 |
| AP, whole frame | 276 / 631 (43.7 %), 142 cases (83 with an error) [34.9, 51.9]; answered 20.9 %, exact on answered 47.0 % | same |
| lateral minus AP | +54.3 points [45.6, 62.9] on 593 vertebrae of 140 cases; cases 79 : 1; exact sign test p 1.34e-22, Holm 5.4e-22 (`MANUSCRIPT_CORRECTIONS.md` §4) | abstract, Results |
| lateral, three / one in field | 970 / 1,159 (83.7 %) [79.6, 87.5]; 385 / 603 (63.8 %) [59.8, 67.9] | Results, Table 3 (job zs9kfield 40436982, closure re-run 40437081; `REVISION_LOG2.md` line 340) |
| AP three / one in field (not printed in text) | 391 / 1,176 (33.2 %); 112 / 591 (19.0 %) | `cv_v9.json#families/pre:zs_v9head` |
| counting the 59 undetected as wrong | 595 / 676 = 88.0 % | Table 3 note b |
| detector recall of agreed lateral bodies | 617 / 676 (91.3 %) | Results; `docs/carmlspine_cv5_mixed_2026-09-21.json#/oracle/LAT/kfull` |
| zero-shot AP errors are a one-level cranial shift | AP whole frame: L4→L3 ×51, L3→L2 ×51, L5→L4 ×48, L2→L1 ×46, L1→T12 ×21 | `PER_LEVEL_DOMAIN_ANGLE.md` Table C (from `cv_v9.json`); not printed |

Superseded predecessor: zeroshot2 on `allspine_v2_r1` (594/617 = 96.3 %, 239/631 = 37.9 %, +57.7 points) —
UNRESOLVED (U1) and disclosed only as "first zero-shot run, not used" in Table 3 note h (`SchwingNet/NUMBERS.md` Revision 2 row; `results/a7.json#cells/zeroshot2~1det~1{LAT,AP}~1kfull`).

### 4.3 Fine-tuned cross-validation naming — CURRENT, HELD OUT

Model: v9init_pre fold models; case-grouped five folds (`md5(case) % 5`) or acquisition-day-grouped three folds
(day groups 66 / 43 / 40 cases; `SchwingNet/results/carmlspine_day_groups.json`). File:
`SchwingNet/results/eval_gate/closure/cv_v9/cv_v9.json#families/pre:cv5_det/cells/...` and `#pre:cvday_det/...`;
paired contrasts `cv_v9_extras_pre.json#pairs`. Jobs: `carmcv9i` 40431706, closure 40436862 (after the `min_det_conf`
fix), extras 40436901 (`CV_V9.md` header; `REVISION_LOG2.md` lines 34, 295).

| claim | number | printed |
|---|---|---|
| lateral whole frame, case-grouped | 601 / 617 (97.4 %), 141 cases (4 with an error); Wilson [93.2, 99.0]; BCa [93.2, 99.4]; answered 503/617 (81.5 %), exact on answered 497/503 (98.8 %) | abstract, Results (`\RESULT{naming_lateral_cv_v9_*}`), Table 3 |
| AP whole frame, case-grouped | 608 / 631 (96.4 %), 142 (7); Wilson [92.5, 98.3] | Key Point 2, abstract, Results, Table 3 |
| lateral three / one in field | 1,079 / 1,159 (93.1 %) [89.2, 96.2]; 451 / 603 (74.8 %) [70.9, 78.7] | Key Point 2, Results, Table 3 |
| AP three / one in field | 1,005 / 1,176 (85.5 %); 399 / 591 (67.5 %) | Table 3 |
| day-grouped lateral / AP whole | 568 / 617 (92.1 %) [87.5, 96.0]; 598 / 631 (94.8 %) Wilson [90.1, 97.3] | Results, Table 3; limitations ("below zero-shot") |
| day-grouped lateral / AP three in field | 1,016 / 1,159 (87.7 %); 1,011 / 1,176 (86.0 %) | Table 3 |
| paired: case-grouped minus zero-shot, lateral | +1.0 point [−1.9, 4.0], cases 4 : 2, p .69 | Results |
| paired: case-grouped minus zero-shot, AP | +52.6 [44.1, 61.3], 78 : 2 | Results |
| paired: day-grouped minus zero-shot, lateral | −4.4 [−9.1, 0.2], 4 : 10, p .18 | Results |
| paired: case minus day, lateral | +5.3 [2.1, 9.1], 8 : 0, p .008 | not printed |
| per level, lateral whole (case-grouped) | L1 97.4 (76), L2 96.8 (123), L3 97.2 (141), L4 97.2 (141), L5 98.5 (136) | `PER_LEVEL_DOMAIN_ANGLE.md` Table C; NOT printed (supplement Table S5 proposed, waits on Greg) |
| per level, one in field | L1 41.2 % LAT / 9.5 % AP is the weakest cell; L4-L5 84-86 % | same Table C |

Reading recorded in `MANUSCRIPT_CORRECTIONS.md` §8: lateral naming is saturated before any same-device frame is seen;
the AP view is a coverage hole the device's own frames fill; a held-out acquisition day is worse than never having seen
the device; same-device data helps most at one body in field (+10.9 [+6.4, +15.5]).

### 4.4 Counting from the detected sacrum (no classifier) — CURRENT, HELD OUT

Tool `tools/count_from_sacrum_eval.py` (self-test with synthetic frames), runner `SchwingNet/slurm/counting.sh`, report
`SchwingNet/tools/counting_report.py`; final job 40416281 (2026-09-23 01:01, 21 cells, outside check against a1.json PASS)
(`SchwingNet/results/JOBS.txt`). File `SchwingNet/results/counting.json`, per-frame `results/counting/*.json`.

| claim | number | printed |
|---|---|---|
| C-ArmLSpine test (28 cases, 56 frames), held-out detector, 0.74, outline | counting defined 46/56 (82.1 %) [69.6, 92.9]; detected sacrum is true 43/46; ordinal correct 188/197 matched (95.4 %) [89.4, 99.5]; within one 197/197; truth bodies right over defined frames 188/232 (81.0 %) [73.8, 87.6] | abstract, Discussion, Table 3 |
| same at 0.25 | defined 51/56; ordinal correct 199/235 (84.7 %) [77.4, 90.7]; within one 225/235 | Table 3 |
| misses by ordinal | 25 of 35 missed bodies at ordinals 5-6 (18 + 7); 16 within 6 px of the frame border (`SchwingNet/results/fig5_naming_data.json#b`) | printed in an earlier revision; not in the current Results |
| COBRA2026 test, held-out detector, 0.25 | defined 111/609 (18.2 %); ordinal correct 54/76 (71.1 %) [56.6, 80.3] | Table 3 |
| DeepFluoro test specimen, 0.25 | 53/67 (79.1 %), one cluster, no interval | twin only |
| pooled over three held-out devices, 0.25 | defined 252/755 (33.4 %); ordinal correct 306/378 (81.0 %) [75.7, 85.8]; within one 366/378 | Table 3 |
| count alone on anchored frames (fold frames, 0.74) | 979 / 1,009 (97.0 %) [94.2, 99.2], 130 cases — uses no encoder, so unchanged by the v9 re-run | Key Point 2, abstract, Results |

### 4.5 Coupling and the stop signal — CURRENT, HELD OUT

File `SchwingNet/results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` (v9init_pre folds; gate block HELD OUT,
420 checks). Coupler `tools/alphabet_couple.py` (runner `SchwingNet/slurm/coupling.sh`; collector job 40436581,
`REVISION_LOG2.md` line 214). 290 frames / 145 cases with agreed truth; 233 anchored at 0.74.

| claim | number | printed |
|---|---|---|
| classifier / count / coupled on 1,009 counted bodies (0.74) | 986 (97.7 %) [95.9, 99.2]; 979 (97.0 %) [94.2, 99.2]; 991 (98.2 %) [96.5, 99.5] | Key Point 2, abstract, Results, Table 3 |
| coupled minus count / minus classifier | +1.2 points [0.0, 3.2]; +0.5 [−1.5, 2.4] | Results, Table 3 |
| disagreement and stop | disagreement frames 13/233 (5.6 %) [2.6, 9.2]; stop on 23/233 (9.9 %) [5.7, 14.5] (13 disagreement + 10 low margin); catches 5 of 6 erring frames | Results, Table 3 |
| L6 calls | 3 of 233 anchored frames (case139 AP+LAT, case44 LAT), all stopped; coupled exact on their 12 bodies 12/12, count 0/12 | Results ("all four L6 calls", with the next row), Table 3 |
| the three one-labeller L6 patients | 6 frames, 4 anchored at 0.74, one L6 call (case42 LAT, flagged); classifier 0/5, coupled 1/5 on the five bodies one labeller reads L6 (agreement, not correctness) | Results, Table 3, Figure 4d |
| at 0.25 (266 anchored, 1,149 bodies) | classifier 1,122 (97.7 %); count 1,104 (96.1 %); coupled 1,116 (97.1 %); disagreement frames 19/266 | Table 3 |

Superseded: the v2-lineage coupling (993 / 995 of 1,009, 12/233 disagreement, 4 of 5 flagged, 921/922 unflagged) in
`SchwingNet/results/coupling.json` — UNRESOLVED (U1); the oracle-box rows (94.7 / 97.7 / 95.9 % of 1,329) are twin only.

### 4.6 Detection on the held-out device (Table S2, Results) — CURRENT, HELD OUT

Arm `lodo_carm` (`rx_lodo_carmlspine_1024`): COBRA Elekta + DeepFluoro real frames; C-ArmLSpine test 56 frames / 28 cases /
287 vertebrae / 56 sacra; outline truth; IoU 0.5. File `SchwingNet/results/a1.json` (`tools/rigor_fixes.py`, code
6e1cf8d, RIGOR_CHAIN jobs gpu 40415602, cpu 40415603/04/14/26/32, cvday 40415610, pool 40415625 —
`SchwingNet/results/JOBS.txt`; report `SchwingNet/results/RIGOR_FIXES.md`).

| claim | number | printed |
|---|---|---|
| vertebra / sacrum at 0.74 | 231/287 (80.5 %) [74.1, 86.8]; 43/56 (76.8 %) [64.3, 89.3] | Results ("short of the pre-stated 97 %"), Table S2 |
| at 0.25 | 260/287 (90.6 %), Wilson on n_eff [84.3, 94.5]; sacrum 47/56 (83.9 %) [73.2, 92.9] | Table S2 |
| at 0.60 (own best F1, optimistic) | 250/287 (87.1 %); sacrum 45/56 (80.4 %) | `a1.json`, not printed as a headline |
| full recall-against-confidence curve, 17 thresholds | 0.01 → 92.7 %, 0.74 → 80.5 %, 0.80 → 67.9 %, 0.90 → 0.0 % | `RIGOR_FIXES.md` A1 table |
| on the repaired denominator | 201/214 (93.9 %) [90.4, 97.1]; re-scored on the rebuilt truth the released denominator reads 236/287 (the text's 231/287 was scored before the 05:22 rebuild) | Results, supplement (`\RESULT{det_heldout_repaired_*}`; `results/indomain/denominator_repair.json`; job 40448892) |
| sacrum anchor on fold frames (0.74) | a sacrum box on 233 of the 286 frames showing a sacrum (81.5 %); no frame without a truth sacrum anchored | Results (REVIEW2_STATS N15) |
| same-device control minus held-out, sacrum at 0.25 | 98.2 % vs 83.9 %, +14.3 points [5.4, 23.2]; sign test 8 : 0; Holm-adjusted P = .009 (replaced .008 when the Holm family was re-formed) | supplement (`results/a3.json#comparisons/pooled_vs_heldout_detector`) |
| same-device controls on C-ArmLSpine (outline) | real-only 40.4 / 41.5 %; pooled real 40.1 / 40.8 % at 0.74 / 0.25 (box-convention artefact); body readings 89.9 % (258/287) and 90.6 % (260/287) | Table S2 (`results/lcurve/lcurve.json#devices/surgio_b51_dr/all_real[]`) |
| COBRA2026 held out (Elekta never seen) | 6.2 % (55/893) at 0.74, 18.5 % (165/893) at 0.25; sacrum 21/609 at 0.74 | Table S2 |
| DeepFluoro test specimen held out | 74.7 % (62/83) at 0.74, 95.2 % at 0.25, sacrum 90/90 (one cluster) | Table S2 |
| design B (styled renders of the other two devices + their real frames) | C-ArmLSpine 63.1 % (181/287) at 0.74, 87.8 % at 0.25; COBRA 10.1 % / 32.7 %; DeepFluoro specimen 69.9 % / 94.0 % | Table S2 |
| renders only | C-ArmLSpine 0.3 % (1/287) at 0.74, 31.7 % (91/287) at 0.25 | supplement, Table S2 |

Pre-stated "counting grade" target (≥ 97 % vertebra and sacrum, `docs/RSNAI_PLAN.md` C7) is **not met** by the
reported detector on C-ArmLSpine (Results: "short of the pre-stated 97 %"), nor by any held-out cell of Table S2. For the
styled-corpus arms `docs/MODEL_CARD.md` §4.6 point 1 writes "not met on two of the three devices", although its own Cios
Fusion row (91.6-94.0 % vertebra recall) is also below 97 %; and it notes the primary C7 criterion (paired bootstrap
against the LODO baseline) was never run, so that one is undetermined, not failed.

### 4.7 Which training source carries the detector (Figure S4, supplement) — CURRENT, HELD OUT

File `SchwingNet/results/contribution_matrix.json` (`SchwingNet/tools/contribution_matrix.py`, grid jobs 40415588 and
rerun 40415691; 24 arms, 85 held-out cells, self-check max |difference| 0.0000; conf 0.25, outline). Narrative
`SchwingNet/results/DATA_CONTRIBUTION.md` — **its prose predates the rerun; the JSON is authoritative** (its own preamble
lists nine corrections).

| claim | number | printed |
|---|---|---|
| radiotherapy imager (Elekta, E) frames alone → C-ArmLSpine | 86.8 % (249/287) [81.1, 91.8] (body convention 11.1 %) | Results (`\RESULT{a3_e_only_carm_pct}`), Figure S4 |
| cadaver C-arm (Cios/DeepFluoro, D) alone → C-ArmLSpine | 12.9 % (37/287) [8.3, 18.1] (body 3.8 %) | Results, Figure S4 |
| adding E to D | +71.8 points [63.4, 79.6] (seed 1: +67.6 [57.6, 76.8]) | Results |
| adding D to E | −2.1 [−6.0, +1.4]; seed 1 −6.3 [−9.8, −2.9] | supplement |
| cutting E's real frames 2,640 → 240 | −47.7 points [−53.7, −41.8] (body −8.0, no paired interval) | supplement |
| COBRA held out: add D to S | +18.0 … +23.9; add S to D −7.8 [−12.5, −3.9] | supplement / older text |
| seed spread on multi-cluster held-out cells | 1.1-5.6 points (7.3 under body) | supplement |
| "no arm isolates angle" | E differs from D in device, anatomy (110 patients vs 4 specimens), frame count and angle together | `CLAIMS_LEDGER.md` §1 (REWRITE verdict F13) |

### 4.8 Same-device detection learning curve and the plateau (Figure 5c, supplement) — CURRENT, HELD OUT

Files: `SchwingNet/results/indomain/det_fill.json` (jobs 40425531/32, 40427581, 40429284, 40449438 named in the file),
`results/lcurve/lcurve.json` (`SchwingNet/slurm/lcurve*.sh`: prep 40416377, array 40416378_0-18, report 40416379 —
`results/lcurve/JOBS.txt`), `results/indomain/INVENTORY.md`, `results/indomain/INDOMAIN.md`, `results/indomain/fit.json`.
Tools `tools/lcurve_fill.py`, `tools/lcurve_train.py`, `tools/lcurve_score.py`, fit `tools/indomain_fit.py` +
`tools/indomain_fit_docs.py`.

| claim | number | printed |
|---|---|---|
| no frame of the device (stage 2: own-geometry styled renders + other C-arms) | 7.0 % (20/287) [4.2, 10.1] body @0.74; stage 1 alone 12.5 % (36/287) | Results (`\RESULT{det_carm_body_recall_074_*}`), supplement |
| plateau from 24 frames | both views at N = 24: lateral 84.1 %, AP 84.6 %; 95.6 % [92.9, 98.0] on the repaired denominator; N = 200 94.9 % [91.3, 97.9] repaired | Results, supplement |
| 50-210 frames | 81.5-86.8 % (234-249/287); every interval from 50 frames up overlaps | supplement |
| one-view arms (25 or 50 frames, two seeds) | own view 83.0-86.4 %; the other view 0.0-39.5 % | Results, supplement (`results/power/power.json#panel_c_detection/summary`) |
| paired plateau check (body @0.74) | N24 vs N200 LAT +2.2 [−1.1, +6.0], AP +1.7 [0.0, 3.8] | `INDOMAIN.md` §2 |
| in-domain frames vs substitutes at N = 24 (centre @0.74) | LAT +28.5 points over COBRA frames, +15.7 over styled renders; AP +20.7 / +27.0 | `INDOMAIN.md` §3 |
| the plateau is the truth denominator | 30 of 287 missed by all ten plateau arms, 208 hit by all; CBCT-cut vertebrae carry 340 of 489 misses; clean subset (204 of 287, complete, agreed, SPINEPS-boxed) 96.9 % (AP 98.7, LAT 95.8) | `results/indomain/miss_diagnostic/MISS_DIAGNOSTIC.md` (job 40448862); memory/carm-plateau-is-the-denominator.md |
| asymptote fits | same-device naming asymptotes NOT identified at 87 persons; detection lateral centre @0.74 asymptote 0.825 [0.781, 0.871] identified | `SchwingNet/NUMBERS.md` Revision 3 last row (`results/indomain/fit.json` 11:59, n_boot 2,000) — NOT quoted |

Caveat carried in the supplement: the device's styled renders were posed on the registered geometry of all 148 cases,
test cases included (`results/indomain/INVENTORY.md` "Pose donors").

### 4.9 C-arm naming against training persons, by view (Figure 5b) — CURRENT, HELD OUT

File `SchwingNet/results/indomain/name_fill.json#figure5b` (`tools/indomain_name_fill.py collect`, generated
2026-09-24T08:36:19; jobs 40425531/32, 40427901, 40429295, 40429398, 40429416, 40429708, 40429901, 40432733, 40434497,
40436049/50 named in the file; runner `SchwingNet/slurm/name_fill*.sh`). REP truth (623 LAT / 633 AP vertebrae), three seeds at small N.

| claim | number |
|---|---|
| lateral protocol: N = 0 → 50 persons | 93.7 % → 98.1 % |
| AP protocol: N = 0 → 5 → all (84-96 per fold) | 33.8 % → 90.8 % → 98.1 % |
| lateral-trained, read on AP, all persons | 54.7 % |
| both protocols trained, all persons | lateral 98.1 %, AP 97.0 % |
| one in field (not printed) | LAT 63.9 % (N0) → 77.1 % (all); AP 15.7 % → 74.6 %; asymptotes not identified (`INDOMAIN.md` §5) |
| renders as substitute for C-arm persons (not printed) | AP whole frame 26.2 → 53.7 % vs in-domain 90.8 → 98.1 % (`INDOMAIN.md` §6) |

All printed via `\RESULT{name_carm_*}` keys.

### 4.10 Plain-film naming against training persons, and the render ablation (Figure 5b, Table S4, Discussion) — CURRENT, HELD OUT PERSONS

Film N-curve: `SchwingNet/results/coverage/film_ncurve/film_ncurve.json` + `FILM_NCURVE.md` (generated
2026-09-24T23:25:30, 48 of 48 cells; `tools/film_ncurve.py`; chain 40437809 → 40437810 → collect 40437811,
`docs/RESUME_2026-09-22_PM.md` / memory/resume-2026-09-24.md). Encoder: render-only (film-free) encoder fine-tuned per
cell on N persons of one corpus; scored on fixed v9 VAL films of that corpus; random 2-9 windows; three seeds at
N ≤ 25, **one seed above** (`PER_LEVEL_DOMAIN_ANGLE.md` Table B header).

| corpus | N = 0 | 5 | 10 | 25 | 50 | 100 | 200 | all (persons) |
|---|---|---|---|---|---|---|---|---|
| NHANES II | 27.2 | 77.8 | 82.3 | 87.8 | 89.2 | 89.6 | 92.5 | 92.7 (264) |
| BUU-LSPINE | 10.3 | 65.0 | 70.3 | 76.7 | 81.2 | 82.7 | 85.1 | 96.9 (2,967) |
| CSXA | 3.2 | 94.2 | 93.0 | 96.4 | 97.3 | 97.3 | 98.0 | 99.8 (4,114) |

Cross-corpus transfer peaks at 74.3 % (NHANES → CSXA at N = 200, 749 films); BUU ↔ CSXA ≤ 12.6 % (`FILM_NCURVE.md`;
`\RESULT{film_transfer_*}`).

Ablation (Greg 2026-09-25 "if renders are my only source of rare classes they have to be included right? run this
test"): `SchwingNet/results/coverage/film_ncurve/ablation/READ.md` (+ `imagenet/`, `filmonly/`, `ablation_read.json`;
arrays 40451157 imagenet, 40451158 filmonly, collects 40451159/60; reader `SchwingNet/tools/film_ncurve_ablation_read.py`;
rule pre-stated in `REVISION_LOG3.md` §13).

| finding | number |
|---|---|
| render-only minus film-only at N = 5 | NHANES +21.9, BUU +11.1, CSXA +18.7 points, every seed separated |
| at N = 25 | +12.2, +6.0, +6.2, every seed separated |
| at every person | NHANES +0.7 (level), CSXA −0.2 (level), **BUU −1.6, separated: renders hurt** |
| verdict cells | 7 of 9 separated: 6 "help", 1 "hurt" (BUU, all persons) |
| ImageNet init on the same merged bank | sits between at small N (NHANES N = 5: 75.5 vs 77.8 render-only vs 55.9 film-only); most of the scarce-N gain is the render rows, 2-5 points is the pretraining |
| ratio actually trained | ~1 : 1 render : film rows by design (`tools/merge_banks.py` line 60, `real_share` 0.5); **never swept** |

Printed: Discussion (`\RESULT{abl_gap_min_pts}` 6 to `abl_gap_max_pts` 22, `abl_cells_separated` 7 of `abl_cells_total` 9,
`abl_worst_delta_abs_pts` 1.6 "the other way"), Table S4, Results ("Persons, views and angles").

### 4.11 Angle, coverage and the pooled fit (Figure 5d, Figure S5, Results) — CURRENT

| claim | number | file / job | printed |
|---|---|---|---|
| matched-N render arms (Surgio card, 2,646 renders, 125 subjects, conf 0.25), 40 unseen TotalSegmentator subjects | AP+LAT-pose arm: 82.1 % at trained angles, 52.8 % over the 16 untrained bins; twice the frames at the same poses 94.2 / 64.8 %; the arc arm 80.7 / 77.1 % | `results/power/power.json#panel_d_angle/summary`; arms `results/coverage/experiment/` (chain 40437812 → 40437813 → 40437814; `tools/coverage_arms.py`) | Results, Figure 5d |
| Elekta XVI coverage arms | printed as "scored zero"; `EXPERIMENT.md` shows real-test vertebra recall 0.0 for four arms and 1.6 % / 0.4 % for the two low2n seeds; the pooled fit treats all six as 0.0, untrained (`generated/numbers_audit.md` key `cov_pooled_n_points`) | `results/coverage/experiment/EXPERIMENT.md` | Results ("the Elekta XVI arms scored zero") |
| the same render-only arms on the REAL Surgio test | 0.7-9.1 % | `EXPERIMENT.md` | `PER_LEVEL_DOMAIN_ANGLE.md` Table G (not printed) |
| one real 301-frame rotational acquisition (case134) | pooled detector 93.6 % of bodies at 0.25 (78.1 % at 0.74); reported held-out detector 49.5 % ("exactly half of the boxes in 15 of 19 bins", recorded UNEXPLAINED) | `figures/figS4.record.json`; `results/arc/case134_sweep.md` (`tools/case134_sweep.py`; job 40431371, requeued under eval_gate/2 as 40436881) | Results (`\RESULT{s5_*}`), Figure S5 |
| nested fit over 105 points | AICc lower by 26.0 for N + lateral-angle coverage (g = +19.96 points per unit H*_lat [12.24, 27.69]); LR p 6.7e-08 at conf 0.25; at conf 0.74 p .82 (coverage adds nothing) | `results/coverage/pooled_fit.json`, `results/coverage/POOLED_FIT.md` (2026-09-25 10:02, `tools/indomain_fit_coverage.py --film`); `results/coverage/sensitivity/pooled_fit_conf074.json` | Results; g identified only by the two render-arm corpora |
| real Surgio pose pool | 148 AP (within 10°) + 148 lateral, none between 10 and 60°; occupies 3 of 18 lateral bins (normalised entropy 0.19), 6 % of joint bins; case134 spin 83 % of lateral bins | `results/coverage/coverage.json` (job acqcov 40436995, `tools/acq_coverage.py`); `results/arc/audit/pose_pools.json` | supplement |
| unseen render angle sweep, pooled detector | below 90 % of its AP recall by ±30° on both cards; Surgio card 0.69 at −50°, 0.99 at −90°; another subject's truth boxes already score 0.64-0.68 (anchor floor ~0.67) | `results/arc/recall_vs_angle_unseen/recall_vs_angle.json` (job 40428072) | supplement |

### 4.12 Image-formation device cards (Figure S3, Table S1) — CURRENT, SUPPLEMENT

Tool `tools/device_fit.py` (+ `tools/device_physics.py`, `slurm/device_fit.sh`); cards `docs/devices/<device>.json`
(code_sha 6e1cf8d recorded). Nine terms fitted leave-one-group-out on up to 40 frames (PIXIUM 14 of 18).

| claim | number | file |
|---|---|---|
| held-out R² card vs uncalibrated physics | Cios Fusion 0.905 vs 0.899 (40/366 frames); BV Pulsera 0.952 vs 0.917 (40/116); Elekta XVI 0.974 vs 0.964 (40/335); PIXIUM 4600 0.679 vs 0.650 (14/18) | `docs/devices/*.json#physics_terms` |
| gain on the 12 patient-held-out folds (Cios, Elekta; 701 frames) | +0.019 [0.008, 0.033]; frame-weighted 0.023 [0.010, 0.033]; 2 of 12 negative; exact sign-flip P = .004, Holm .009 | `results/eval_gate/leaks/card_gain_unseen.json` (CURRENT, supplement) |
| within-subject folds (Pulsera phantom, PIXIUM cadaver) | 0.056 [0.025, 0.088] — not held out (one object) | same |
| criterion C3 (every device's gain > 0 with interval excluding 0) | **not met**: holds only on six-fold percentile; on six-fold t intervals only BV Pulsera excludes 0 | `results/a6.json#verdict`; `results/stats_review/recompute.json#R2_card` |
| refit with image noise in the loss | failed its own acceptance gate on every device; published parameters stand | `figures/figS2.record.json` panel d; `results/supplement_figs/card_refit/` |
| exposure clip defect | `device_style.SPREAD = 0.2` reaches 1.7-5.1 % of each device's joint distribution; 94.9-98.3 % of styled frames carry a pinned term; typicality gate (99 % joint) written, clip still default | `docs/DEVICE_SPREAD_SWEEP.md`; `docs/DEVICE_PARAM_AUDIT.md`; memory/device-sampling-audit.md; supplement says "a defect not repaired" |

Superseded: the 24-fold gain +0.0376 [0.0205, 0.0573] (LEAKED L6: two devices have one subject).

### 4.13 Corpus manifold and the film/fluoroscopy question (Figure S2) — CURRENT, SUPPLEMENT

| claim | number | file |
|---|---|---|
| film vs fluoroscopy, one corpus held out (19 corpora, 7,311 frames) | −0.7 to +9.2 points over the 71.8 % majority share across six pooled cells; no percentile interval excludes zero; two knn15 BCa intervals do | `results/a2.json#corpus_manifold/excess_over_chance`; embedding `results/corpus_manifold/` (job 40414107 features; 40414544/45) |
| films vs C-arm + kV frames, one source held out (5,797 frames) | image statistics 63.4 % [57.6, 69.2] vs majority 64.4 %; deep features 85.0 % [79.4, 90.0] | `figures/figS1.record.json`; `results/manifold/probes.json` (jobs 40416696-98, `tools/corpus_manifold.py`) |
| styled renders vs the device's real frames | Cios 100 % (n 736), Surgio 99.8 % (666), Elekta 99.0 % [98.1, 99.6] (771) — renders stay separable | same |
| per-device overlaps (not printed) | Bhattacharyya 0.005 (DeepFluoro-Geneva) to 0.675 (Elekta-Geneva) | `docs/RSNAI_CLAIMS.json` manifold_carm_pair_min/max; memory/film-fluoro-boundary-not-transferable.md |

### 4.14 Render-trained vs film-trained detector on plain films — CURRENT, SUPPLEMENT (rerun on unseen spines)

| claim | number | file |
|---|---|---|
| 17 NHANES II lumbar spines neither detector saw, conf 0.05 | film-trained 99.4 % (160/161) vs render-trained 67.7 % (109/161), +31.7 points [21.0, 45.4], 16 : 0 spines; at 0.25 98.8 % vs 34.8 % | `results/eval_gate/leaks/render_vs_film_unseen_rerun.json` (job 40429839) |

Superseded: the 25-spine version (99.14 vs 71.67 %, +27.5 points) — 24 of 25 spines were in the film detector's own
lists (LEAKED L2). Detector: `anchor_det_v1` (6,650 renders, zero real images) vs `detect_v5z_final`
(memory/detection-is-the-binding-constraint.md).

### 4.15 Plain-film naming on the selection split (supplement) — CURRENT, SELECTION SPLIT

File `SchwingNet/results/a5.json#per_protocol/random/*/patient_clustered` (v8 encoder `allspine_v8 model_rung_1_aug2.pt`,
head `head_allspine_v8_mixed_kmax4_seed0.pt`, seed 0; `results/a5_rows_meta.json`).

| corpus | exact, random 2-9 window | three bodies |
|---|---|---|
| CSXA cervical | 3,629 / 3,635 (99.8 %), 727 patients, Wilson [99.5, 99.9] | 99.6 % |
| BUU-LSPINE lumbar | 2,671 / 2,744 (97.3 %), 549 cases [96.5, 98.0] | 95.0 % |
| NHANES II | 441 / 445 (99.1 %), 52 patients / 76 films, Wilson [97.8, 99.6] | 94.6 % |

Every annotated patient of the three corpora is in v8's training or selection split, so **no held-out plain-film
accuracy exists in paper 1** (EVAL_LEAKS L4; supplement "Plain-film naming on the selection split"). v9 three seeds give
NHANES 96.9-97.6 % (`results/v9_a5_seeds.json`; Table 3 twin note f). Per-level film naming was DERIVED read-only in
`PER_LEVEL_DOMAIN_ANGLE.md` Table E (BUU L1-L5 96.4-98.4 %, NHANES 97.4-100 %, renders: L6 20-42 %, T13 0/9) and is
not quotable until a committed tool re-runs it on held-out persons.

### 4.16 Transitional persons, the split and the sample-size argument (Table 2, Figure 5a) — CURRENT

| claim | number | file |
|---|---|---|
| transitional persons in the sources | 194: L6 110 (CTSP 18 / VerSe 86 / TS 3 / C-ArmLSpine 3), T13 7 (VerSe 6 / TS 1), sacralised L5 28 (12 four-lumbar), Castellvi I/II 31, lumbar rib 14, unassigned 4; per source 52 / 135 / 4 / 3 | `results/rare_class/transitional_subtypes.csv` (2026-09-23 18:54, `tools/transitional_subtypes.py --ts-override`) |
| no spine carries both L6 and T13 | 0 in every source | `results/rare_class/transitional_subtypes.md` |
| eight of twelve TS "L6" spines are normal | independent rib count; four transitional | `results/spineps_ids/TS12_VERIFY.md` |
| built split (test side) | L6 43 + 3 real, T13 3, sacralised 11 (5 four-lumbar + 6 five-lumbar), Castellvi 12, lumbar rib 6, unassigned 2 = 77 CT + 3 real; 92 of 97 val+test persons sit in v8/v9 training | `results/rare_class/split_plan.md` (`tools/make_split.py` apply 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS) |
| pre-stated targets | exact-level Wilson lower bound ≥ 90 % needs 35 error-free at-risk persons; variant sensitivity ≥ 85 % needs 22 carriers | `results/power/power.json#n_needed_zero_errors`; independent check `results/stats_review/recompute.json#R4_wilson` (PASS) |
| COBRA2026 screen | 91 unread test-side calls (L6 38, T13 45, four-lumbar 8); a two-labeller count with both junctions in field and an exported frame finds 7 at-risk persons (L6 3, four-lumbar 4, T13 0) → error-free Wilson bound 64.6 % | `figures/figure5.record.json#numbers_on_figure/counts_and_intervals`; `results/transitional_registry/cobra/rows.csv` |
| at-risk CT test persons | 51 (L6 43, four-lumbar 5, T13 3), 36 rendered → 93.0 % error-free | same |
| labeller calibration | VERIDAH L6 call matched CTSP readers in 10 of 24; T13 in 0 of 52 | `results/spineps_ids/IMPACT.md` (line 230); `results/stats_review2/recompute.json#S4_cobra_call_yield` |
| no released radiograph or C-arm frame carries a human-read T13 or Castellvi grade | statement about the sources | `figures/figure1.record.json#not_shown_and_why` |

Superseded: the 57 "field-supported" COBRA calls / 93.7 % best case; the 89 / 37 / 90.6 % inventory projection (built
on 12 TS spines read from raw SPINEPS ids); the 98.2 %-planning-accuracy power curve (69 / 4,276); the frozen exact test
numbers (PAPER 2). The `tables/tab4_transitional.md` twin still prints the superseded "91 (57) … 93.7" row; the printed
`.tex` reads "91 (7) … 93.0 (51 CT); 64.6 (7 real)".

### 4.17 Development learning curve of the split-trained arm (supplement) — CURRENT, VALIDATION SIDE ONLY

File `SchwingNet/results/dual_loss/saturation.json` (`SchwingNet/tools/d1_saturation.py`; d1lcurve array 40436887,
logs in `results/dual_loss/`). ImageNet-init encoder + head on G3 training persons, nested fractions, three seeds, read on
the validation side that chose the epoch.

| claim | number |
|---|---|
| training persons | 563 / 1,121 / 2,240 / 4,477 / 8,950 |
| random windows overall | 68.9 % → 74.0 %; last doubling +0.6; seed spread 1.0 at full size |
| real films | 98.2 % (563) → 98.7 % (8,950); last doubling +0.1; three bodies 97.2-97.5 % at every size |
| CT renders | 59.6 → 66.2 % (+0.8 last doubling) |
| rendered L6 bodies | 51.8 → 64.2 % (+1.7; seed spread 3.4) |
| rendered T13 | named in none of three full-size runs |
| epochs | within 0.5 points of final by epoch 8-12 |

### 4.18 Study population (abstract, Results, Table S3) — CURRENT

`results/age_sex_by_source.json` (`SchwingNet/tools/age_sex_by_source.py`; VinDr headers job 40438307): median age 36 y
(CSXA) to 66 y (COBRA2026, age on 115 of 145); female 42.5 % (TotalSegmentator) to 64.5 % (CSXA); none released for the
intraoperative, cadaveric or phantom sets. Corpus totals 4,093 renders, 9,108 level-annotated films, 4,276 real exposures
(778 C-arm) — `tables/tab_corpus.sources.md` "Totals row (footnote j)". Figure 1 persons 24-89 y
(`figures/figure1.record.json#components[].demographics`).

### 4.19 Data-integrity numbers printed in the supplement — CURRENT

| number | file |
|---|---|
| 99 data gaps = 31 criterion + 28 bug + 21 unfinished + 4 budget + 15 unknown | `docs/DATA_COMPLETENESS_AUDIT.md` "Every gap, worst first" |
| CHK-9 over 563 quoted numbers: 323 held out, 81 seen, 58 unreadable lineage, 101 no checkpoint | `results/eval_gate/EVAL_LEAKS.md` GENERATED counts (job 40429833) |
| 306 checkpoints in the lineage census, 133 with an unreadable link | `results/eval_gate/LINEAGE.md` |
| 57 quoted numbers traced to the deleted `allspine_v2_r1` bank, re-run on v9 | `MANUSCRIPT_CORRECTIONS.md` §7.0 |
| NHANES II in the banks twice; 48 of 54 validation patients twinned in training | `docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `tools/leak_check.py` docstring |
| 2,437 harvested masks with raw ids 1..N; 3,490 relabelled | `results/spineps_ids/CENSUS.md`, `IMPACT.md` §0, `REPAIRS.md` |
| 69 quoted detector numbers re-scored in both box conventions | `results/bodybox_rescore/RESCORE.md` (job 40419582) |
| Mendeley: 500 of 584 films re-encode BUU-LSPINE | `tools/excluded_sources.py` REASONS |
| CTSpinoPelvic1K 0533 truncated download 17,301,504 → rebuilt 250,067,995 bytes | `results/repairs/ct0533_CHECK.md` |
| COBRA2026 frames counted up to four times in one arm: 5,013 duplicate entries | `results/repairs/cobra-dup-leak_CHECK.md` (job 40416578) |

---

## 5. Results from before SchwingNet (2026-09-12 to 2026-09-22): what they were and whether they still stand

These built the program; almost none is quotable now. Order roughly chronological.

### 5.1 Plain-film level identification (FluoroCap era)

| result | number | where | status |
|---|---|---|---|
| context ladder on real films, single vertebra | n = 1 96.7 %, 3 vert 98.8 %, 5 vert 99.1 %; lumbar n = 1 80.7 % (85.4 % at 96 px) | `~/tmp/ladder_summary.json` (grid); memory/level-id-2d-results-2026-09-13.md | RECORD ONLY (films_ann bank, cervical-dominated) |
| recurrent head over single-crop embeddings | 98.69 / 99.13 / 99.41 / 99.48 % at 3/5/7/9 vertebrae, n 8,422 | `~/bench/xr_fov/recurrent.json` (job 40215812, 2026-09-13 13:28) | RECORD ONLY. **Measured on `films_ann_fov96_ctx`, not `films_all2` as `slurm/recurrent_head.sh` line 16, `tools/recurrent_order.py` line 56 and `~/bench/model_registry.md` M96 still say** (three lines of evidence in `docs/MANIFEST_DATA_MODELS_RESULTS.md` §1.1; the two local files were still uncorrected on 2026-10-08). 14 of 27 classes live; head worth ~+0.4 over single-crop 96.95-98.98 %; weights never saved |
| films_all2 head | 98.84 / 99.13 / 99.42 / 99.38 | `~/bench/xr_fov/recurrent_all2.json` | RECORD ONLY |
| whole-spine (allspine_v2, 27 classes) single-crop | 78.74 % [78.11, 79.37], n 16,392; T13 0.0 % (n 14), L6 64.4 % | `~/model_night/runs/result_r18_ce.json` | LEAKED bank (v2) |
| restored recurrent head on allspine_v2 | 83.38 / 86.12 / 86.16 / 88.95 % at 3/5/7/9 (+10.2 at 9); T6-T8 the floor 62-65 % | `~/model_night/recurrent_allspine_v2.json` (job 40293790); memory/recurrent-head-restored-2026-09-16.md | LEAKED bank |
| mixed-length head | 97.47 / 98.45 / 99.29 / 99.92 at 3/5/7/9; random window 99.02 % ("shortcut-free") | memory/mixed-length-head-and-sota.md | SUPERSEDED: pools NHANES twice (memory note's own 2026-09-22 correction); clean per-source v2: CSXA 99.87 %, BUU 98.04 % — both now in "Numbers deliberately absent" (`SchwingNet/NUMBERS.md`) |
| STC (star) loss | loses to cross-entropy everywhere; transitional 22-24 % vs 39.8 % | `~/model_night/stc/`; memory/stc-does-not-transfer.md | REFUTED |
| selective prediction | 99 % accuracy at 35.7 % coverage (exact level), 55.7 % (region); AUGRC 0.0466 | `~/selective/SELECTIVE.md` (job 40291753, `tools/level_selective.py`); memory/selective-prediction-the-honest-99.md | not quotable: leaked v2 bank; computed on the test half (~8,280 vertebrae, not 16,392); coverage chosen on the same half (`docs/MODEL_CARD.md` §5.3). In "Numbers deliberately absent" |
| model-night arms (CORN, ordinal focal, frozen, ViT) | 78.44 / 75.05 / 30.12 %; four ViT arms produced no result | `docs/MANIFEST_DATA_MODELS_RESULTS.md` §5.2, §7.2 | RECORD ONLY |
| corruption suite | films_all2 rung 1: clean 99.10 %, over-exposure sev 5 16.93 %; aug tier 2 79.18 % | `~/bench/robust/*.json`; MANIFEST Surface I | RECORD ONLY (motivates `--augment 2`) |
| literature panels (FluoroCap) | 19.7 % agreement with weak labels, n 7,065; resolution does not move naming (−0.33 points paired) | `~/model_night/panel_stats/`; memory/fluoro-panel-gap-diagnosed.md | not an accuracy; FluoroCap is figures of published articles (memory/fluorocap-is-reproductions-not-fluoroscopy.md) |
| LSTV / TLTV flags | CTSP AUC 0.577 [0.480, 0.669] (contains 0.5); VerSe 0.724; sex positive control 0.951 renders / 0.829 real BUU | `~/lstv_flag/LSTV_FLAG_RESULTS.md`; MANIFEST Surface K-L | REFUTED as a flag |
| feasibility claims (interior windows) | v2 ordinary lumbar interior 91.8 % [89.4, 94.1]; anomalous 66.0 % (12 films); v6 interior anomalous 49.9 % [41.5, 58.9] (128 films) | `~/model_night/interior_windows/` (job 40321368); memory/feasibility-claims-measured.md | RECORD ONLY (v2/v5/v6 banks leaked or superseded) |
| remedies | film-noise randomisation, pretrain-on-renders, renders mixed 8 ep, anchored-only admission all lose to v2 baseline (91.8 / 66.0); render fraction 0 → 0.5 raised anomalous 34.0 → 53.2 | memory/remedies-refuted-2026-09-17.md | REFUTED (remedies); the fraction sweep is the only render-ratio sweep ever run and is on a superseded line (`PER_LEVEL_DOMAIN_ANGLE.md` Table A note) |
| Cina-style whole-film benchmark | v2 99.96 % = sacrum-count rule 99.96 % — saturated; only the limited field discriminates | memory/feasibility-claims-measured.md (`tools/benchmark_cina.py`, job 40323179) | RECORD ONLY |
| re-implemented competitors + ensemble (ours, cina, kim, vertx, konya; 124 cells, dev/test halves) | design in `docs/COMPETITOR_BENCHMARK.md`; output `~/model_night/ensemble/ensemble.json` | **result not recorded in any repository document read** |
| 2-mechanisms table numbers | L6 44.9 % in State C; 1 body 72.9 %, 5 bodies 97.0 %, whole 98.2 % | memory/two-mechanisms-thesis.md | SUPERSEDED (v2-lineage CV; framing still governs the paper) |

### 5.2 The sweep / chain / confirmation line (counting across exposures)

| result | number | where | status |
|---|---|---|---|
| sweep_v3 (respaced renders) held-out 120 CTSP, 2-body, 9-inch | naming 72.1 → 95.2 %; chain 97.5 %; with the end rule 120/120 | `~/model_night/sweep_v3/` (job 40384843; `slurm/sweep_v3.sh`; `tools/make_results_table.py`); memory/sweep-map-replaces-registration.md | RECORD ONLY; only sweep_v3 counts — `sweep2`, `sweep_holdout_v2`, `sweep_protocol`, `sweep_improve`, `sweep_fix` superseded by the row-spacing defect (memory/drr-row-spacing-defect.md) |
| TS bench, 522 spines from the sacrum | 98.5 % chains; 203 from C2 95.1 % | same | held out for the v7-lineage encoder only; for v9 only 71 cases are unseen (`~/model_night/sweep_v3/cns/unseen_v9.txt`; memory/ts-bench-inside-v9-bank.md) |
| 25 real lumbar films | chain 100 % with true boxes; 21/25 chains with the detector | same | RECORD ONLY |
| overlap ladder | 2 bodies of overlap optimal (97.5 % chains) | same; `docs/SWEEP_PROTOCOL.md` | protocol recommendation |
| counting with boxes given | 99.66 % of 6,255 walks (801 CTSP); C2 down on 262 real films 1,204/1,209 (99.67 %) | `docs/COUNTING_EVIDENCE.md` (generated by `tools/counting_brief.py`) | RECORD ONLY |
| counting with detector boxes | render detector 30.06 % (anchor by class 44.07 %, 507 of 625 refused) | same | REFUTED as deployable |
| needle confirmation | 99.31 % of 5,385 vs 99.48 % needle-free (801 CTSP); on TS cervical 84.58 % vs 93.09 % (the metal is not free) | same | RECORD ONLY |
| search-window ablation | widening 0.6 → 2.1 bodies leaves counting at 98.9-99.6 %; window not the mechanism | same | RECORD ONLY |
| transitional confirmation (18 CTSP L6 spines × 3 seeds) | clean: 45/54 exact chains, 36 named L6; film-noise: 45 and 35 | `/rs/.../or_ready/story_rows_f3/summary.json`, `story_rows_f6/summary.json`; `docs/RSNAI_CLAIMS.json` lstv_* | RECORD ONLY (was Figure 2 of the 2026-09-22 set; not in the current paper) |
| linking under physics | boxes given 99.74 % clean / 71.73 % physics; detector boxes 39.52 % / 21.50 % at conf 0.05 (0.25 miscalibrated) | `docs/PHYSICS_LINKING.md`; `docs/HANDOFF_PHYSICS.md`; `results/physics/` | RECORD ONLY; anything measured under `--perturb physics` before the bone path fix is not quotable (`docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`) |
| three physics defects | only the AEC extrapolation changed an image (PIXIUM 4,607 → 103,084 photons/mm² once capped) | `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`; memory/physics-three-defects-measured.md | RECORD ONLY |
| guided acquisition | engine built; phantom only (geometry to 1.2 mm); job 40376577's corpus result | `docs/GUIDED_ACQUISITION.md` STATUS (2026-09-18) | **corpus result not recorded**; nothing quotable |
| runtime | full-resolution link 422.6 s per pair vs 575 ms reduced; 3-exposure sweep 12.6 s, 7 → 27.2 s excluding the detector, contended CPU, synthetic exposures; "same answer" claim withdrawn | `docs/MODEL_CARD.md` §6.3; `~/bench/runtime_cost_workstation.json` | not in any manuscript; GPU/detector job (§6.6) run status not recorded |

### 5.3 DeepFluoro, image formation, devices (2026-09-20 to 09-22)

| result | number | where | status |
|---|---|---|---|
| render-only detector on DeepFluoro real frames (sacrum recall, 6 specimens, 365 frames, conf 0.05) | 76.9 % (by specimen 47.8-96.2; seed alone moves 26 points); before fixing 160/366 stored upside-down frames ~40 % | memory/learned-formation-refuted-calibrate-instead.md; `docs/DEEPFLUORO_FORMATION.md` | RECORD ONLY |
| calibrate, don't learn | exact geometry + attenuation 80.9 % explained; nine terms LOSO +4.1, v2 +4.3 (`calibration_best.json`); ceiling 99.5 %; learned refiner better on 21 % of frames only | same | the decision stands; numbers RECORD ONLY |
| DeepFluoro frames were converted wrongly (log of a log) | fix `DF_CONVERSION=linear` | same | open: refit under linear not confirmed in a file read |
| learned arms vs none on TS renders | none_v2 64.0 %; rffull 71.7, rfhp 72.2, fda 74.2; pairs 90.0-95.0 % | `tools/deepfluoro_anchor_report.py`; same memory | RECORD ONLY |
| real-frame LODO detector (first table) | C-ArmLSpine held out 90.6 % vertebrae / 83.9 % sacrum at 0.25, outline (5.2 % under body = convention) | `/rs/.../or_ready/lodo/rescore_outline.json`; `docs/RSNAI_CLAIMS.json` | became a1.json (section 4.6) |
| styled-corpus LODO (dc arms) | Cios held out 0.9157-0.9398 vertebra recall (test specimen); Elekta 0.3024-0.3270; Surgio 0.1429-0.1498; 1 → 2 training devices Elekta 0.1221 → 0.3024 | `~/spine-detector/runs/devcorpus/*/scores.json`; `docs/MODEL_CARD.md` §4.6 | SUPERSEDED by the contribution matrix scoring; box convention of those rows not recorded (§4.6 qualification) |
| level naming CV on C-ArmLSpine, v2 lineage | lateral 98.2 % (606/617), AP 96.7 %, k5 97.0, k3 92.9, k1 72.8; zero-shot 96.3 / 37.9 % | `docs/carmlspine_cv5_mixed_2026-09-21.json`, `docs/carmlspine_zeroshot2_pooled_all_2026-09-21.json` | SUPERSEDED (UNRESOLVED U1) by cv_v9 |
| fixed-split fine-tunes (28 test cases) | mixed fine-tune LAT/AP 94.6 / 95.2 % whole, 87.4 / 86.4 % at 3; real-only fine-tune 89.2 / 95.2 % (lost laterals); detector fine-tunes multi 97.4 / 95.9, pooled 93.1 / 100 % | `docs/carmlspine_ft_mix_test_2026-09-21.json`, `_ft_realonly_`, `_ftdet_multi_test_2026-09-22.json`, `_ftdet_pooled_` | RECORD ONLY |
| first manifold (37 corpora) | every held-out C-arm corpus labelled FILM; LOFO pooled 71.1 % vs chance 71.8 % | `/rs/.../or_ready/corpus_manifold/overlap.json`; memory/film-fluoro-boundary-not-transferable.md | SUPERSEDED by the a2 six-cell range (section 4.13) |
| device deployment | one vendor route (Siemens Cios OpenApps, K181560 / K203504); no published compute figure for any C-arm | `docs/CARM_DEPLOYMENT_EVIDENCE.md` | evidence document, no number in the paper |
| sweep timing literature | a 3-5 exposure sweep ≈ 2-5 min, dominated by C-arm moves (36-49 s each) — a synthesis, not a measurement | `docs/SWEEP_TIME_EVIDENCE.md` | evidence document |

### 5.4 The 2026-09-22 rigor audit that created SchwingNet's rules

17 adversarial agents (memory/rigor-audit-findings.md; `docs/RESUME_2026-09-22_PM.md`): selective reporting in two
places (rescore_outline 1,440 cells; manifold three feature spaces), threshold-dependent detector number, one CI in 54
claims, film CIs clustered by vertebra, no paired tests, criterion C3 never evaluated, selective prediction invisible,
abstention unreported. Fixes A1-A7 and A9 are `SchwingNet/results/RIGOR_FIXES.md` / `rigor_fixes.json` (code 6e1cf8d),
A8 is the verse_drr-millimetre prohibition. The statistical reviews F1-F22 and the revision are
`SchwingNet/REVIEW_STATS.md`, `REVIEW2_STATS.md`, `REVISION_LOG.md`; recomputations
`SchwingNet/results/stats_review/recompute.json` and `stats_review2/recompute.json`
(`SchwingNet/tools/stats_review_recompute.py`, `stats_review2_recompute.py`).

---

## 6. Paper 2 — the LevelCheck / surgeon comparison (PAPER 2; nothing here is printed in paper 1)

| item | state | file |
|---|---|---|
| what LevelCheck's published numbers are | registration accuracy; the level name is imported from the preoperative CT annotation (Otake 2012 99.998 % simulated; Lo 2015 100 % at 200 multistarts; Manbachi 2018 median error 30.4 % → 2.4 %) | `SchwingNet/LEVELCHECK_CLAIM.md` §1 |
| what may and may not be said | two-column table; "LevelCheck fails on transitional anatomy" is not citable | same §3 |
| frozen comparator | H1 at-risk 82.2 % (Peh 1999) n_min 19; H2 97.6 % (Manbachi 2018) n_min 152; H6 ordinary non-inferiority 92.6 % (margin 5) n 48; commits ecae75f (2026-09-23 19:50:36), 1897772, 2993f40, b511985 (s14), d0403de (s15); never edit | `SchwingNet/LEVELCHECK_MODEL.md`; `SchwingNet/NUMBERS.md` LevelCheck row and Revision 3 pre-registration row |
| automated reference | only ordinary spines qualify: Dawid-Skene PPV 0.971 [0.957, 0.981], coverage 0.886; no rule reaches PPV lower bound 0.90 for L6, T13 or four-lumbar; every transitional test person needs a human read | `SchwingNet/results/auto_reference/CALIBRATION.md`; frozen `results/fig6/frozen/auto_reference.json` (57782cad…) |
| ordinary COBRA test persons on automated truth | 56 assigned ordinary (44 with frames) — H6 short of n_min 48 by 4 | `docs/RESUME_2026-09-22_PM.md` 2026-09-24 15:47 block |
| open gate 40438004 (ordinary strata only) | ran 2026-09-25; harvest-name scores only; **reference-standard score not written** because `SchwingNet/tools/fig6_score.py` read `T1/blinded/meta_ref/` instead of `T1/open/meta_ref/` — fix before scoring | `SchwingNet/paper2_levelcheck/open_gate_40438004/README.md` |
| blinded gate | held; must not be released before `/rs/.../data/fig6/unblinding/RELEASE_v2.json` exists (written by a person after a frozen human truth) | memory/resume-2026-09-24.md names job 40438005; `REVISION_LOG3.md` line 7 names f6eval 40431765/40431766 held — both recorded, see contradictions |
| why it left paper 1 | ordinary-only superiority over 97.6 % needs 152 zero-error persons; transitional strata need human reads that do not exist | memory/paper-split-2026-09-24.md |
| prior-art numbers used | wrong-level 1 in 3,110 (Mody 2008), 12.8/10,000 (Jhawar 2007), 0.12 % of 34,544 (Furuya 2026); LSTV 12.9 % with 54 % miscounted at clinic (Nakagawa 2017); Castellvi II-IV ~9 % of CT (Hanhivaara 2020) | `SchwingNet/LEVELCHECK_CLAIM.md` §2 |
| old Figure 6d Wilson table | all 30 cells equal `scipy` Wilson lower bounds | `SchwingNet/results/power_table.json` (`SchwingNet/tools/fig_claim.py`) — RECORD |

---

## 7. How leakage was checked, as it bears on each result

- **The rule** (Greg, 2026-09-23): an item is held out for a checkpoint only if its patient key is in neither the train
  nor the val/selection set of that checkpoint or any ancestor; a render inherits its CT subject; only public
  ImageNet/COCO weights are exempt; unknown is not clean (`EVAL_LEAKS.md` opening).
- **The machinery**: `tools/eval_gate.py` (runs before every quoted score, stamps the verdict and `weights_sha256`;
  eval_gate/2 refuses a block whose sha set differs), `tools/holdout.py` (validation counts as seen),
  `tools/checkpoint_lineage.py` (306 checkpoints), `tools/leak_check.py chk9` (563 quoted numbers),
  `tools/make_split.py` CHK-1…CHK-8 (exit non-zero on failure), `tools/patient_keys.py` +
  `make_context_crops --patient-json`, `tools/spineps_ids.py` (instance-id guard), `tools/excluded_sources.py`,
  `tools/unseen_cases.py` (what a checkpoint's chain never saw) (`SchwingNet/supplement.tex` "Data integrity and quality
  controls"; `MANUSCRIPT_CORRECTIONS.md` §5).
- **Verdict by family** (`EVAL_LEAKS.md` §1-3): L1 old recall-vs-angle curve (void, re-scored on 40 unseen subjects;
  the leak did not inflate it); L2 render vs film (re-run on 17 unseen spines; gap holds); L3 COBRA learning-curve
  control (not in manuscript); L4 plain-film naming (no unseen subset exists); L5 Figure 2 and alphabet-loss L6 recall
  (selection split); L6 card gain (two devices have one subject; 12-fold re-read); L7 Figure S2a pair R² (re-run under
  the held-out fold); U1 every v2-lineage C-ArmLSpine number (re-run on v9 = section 4.2-4.5).
- **Known leaks in earlier banks**: NHANES twice (v2/v5/v6/v7), CTSpinoPelvic1K under two names (357 people in v6/v7),
  VerSe by series in v8, `anchor_drr` split leak (render detector's own-domain 93.48 %), `vindrps` keyed per image,
  `allspine_v8` 192 persons in both train and val (187 CTSpinoPelvic1K, 5 VerSe; no film patient)
  (`SchwingNet/NUMBERS.md` "Numbers deliberately absent"; `MANUSCRIPT_CORRECTIONS.md` §2).
- **Selection effect not measured**: the v9 encoder kept its best epoch on the split the alphabet-loss "10 held-out L6
  spines" belong to; its size is unmeasured (`EVAL_LEAKS.md` item 6).
- **Pose dependency reported, not scored**: every `lc_*` list carries all 7,322 styled renders, including 598 under
  C-ArmLSpine test-case poses (`EVAL_LEAKS.md` item 3; `results/eval_gate/EVALUATORS.md` §1.3).

---

## 8. Where documents disagree, and which reading is trusted

| question | reading A (file) | reading B (file) | trusted, and why |
|---|---|---|---|
| Naming numbers in Table 3 | `SchwingNet/tables/tab3_naming.md` (twin): 606/617, 610/631, zero-shot 594/617 and 239/631 | `SchwingNet/tables/tab3_naming.tex` (printed): 601/617, 608/631, 595/617, 276/631 | **B**: the twin was not regenerated after the v9 re-run; A is the UNRESOLVED v2 lineage (EVAL_LEAKS U1) |
| Table 2 totals | `tables/tab4_transitional.md`: "91 (57) … 93.7 (57 CT)" | `tables/tab4_transitional.tex`: "91 (7) … 93.0 (51 CT); 64.6 (7 real)" | **B** (NUMBERS.md Revision 2 says the 57 / 93.7 left the text) |
| ATLAS model card | `SchwingNet/atlas/model.json`, `packet/atlas/model.json`, `packet_cameraready/atlas/model.json`: 594 of 617 (96.3 %), 239 of 631, 606 of 617 | `SchwingNet/main.tex`: 595 of 617 (96.4 %), 276 of 631, 601 of 617 | **B**; the cards in both packets carry superseded numbers — fix before submission |
| Render ablation verdict | `REVISION_LOG3.md` §13 and memory/film-ncurve-ablation-result.md: "7 of 9 … all in the direction 'renders help'" | `results/coverage/film_ncurve/ablation/READ.md`, `tables/tabS4_ablation.tex`, `PER_LEVEL_DOMAIN_ANGLE.md`: 6 help, 1 hurt (BUU, every person, separated) | **B**: READ.md is generated by the reader tool from the result files; the Discussion now states both directions (commit 05e05dc) |
| Is the ablation in the manuscript | memory/film-ncurve-ablation-result.md: "NOT in the tex" | commits 7e81dd7 / 05e05dc; `sections/discussion_motivation.tex`; Table S4 | **B** (later; verified in the tex 2026-10-08) |
| Which bank gave 98.7/99.1/99.4 | `slurm/recurrent_head.sh` line 16, `tools/recurrent_order.py` line 56, `~/bench/model_registry.md` M96: films_all2 | `docs/MANIFEST_DATA_MODELS_RESULTS.md` §1.1: films_ann | **B**: job log prints 28,032 crops = films_ann exactly; films_all2 inputs were created after the result; the script's own usage line names films_ann |
| Device-card gain | supplement older text / NUMBERS row: 24 folds +0.0376 | supplement now: 12 patient-held-out folds +0.019 | **B** (EVAL_LEAKS L6) |
| Held-out detector, released denominator | `results/a1.json`: 231/287 | `results/indomain/denominator_repair.json`: 236/287 re-scored on the rebuilt truth | both printed; the text keeps 231 (scored 2026-09-22) and the supplement states the 236 beside it |
| Zero-shot lateral | 594/617 (zeroshot2, v2) | 595/617 (v9, PRE truth); `INDOMAIN.md` §5 600/623 (REP truth) | 595/617 is quoted; 600/623 is the same model on REP truth (not quoted) |
| Sacrum anchoring denominator | `NUMBERS.md` old row: 233 of 290 frames (80.3 %) | current Results: 233 of the 286 frames showing a sacrum (81.5 %) | **B** (REVIEW2_STATS N15: four frames have no truth sacrum) |
| "No error exceeded one level" | `paper/rsnai/main_v2.tex` Results | `docs/MODEL_CARD.md` §4.2: false at complete coverage (6 vertebrae beyond one level of 676) | **B** |
| Excluded literature panels | supplement "Excluded sources": FluoroCap refused by `assert_clean` | `docs/MODEL_CARD.md` §3.2 and `SchwingNet/NUMBERS.md` Table 1 row: FluoroCap 950 panels as 2,100 crops in the C-ArmLSpine fold banks; `CV_V9.md`: v9 folds use "the same merged fold banks"; `main.tex` Ethics: panels "used for training only" | both true at different times: the guard post-dates the fold banks. The current fold models do train on FluoroCap panels and VinDr crops; the supplement sentence reads as if they could not. Unresolved wording; Greg should decide |
| Clean C-arm detection subset | memory/carm-plateau-is-the-denominator.md: 204 of 287, 96.9 % | `DENOMINATOR_REPAIR.md`: 214 of 287 | different rules (the diagnostic also required label agreement; the repair does not); the repair (214) is printed |
| Same-device naming fit | `results/indomain/INDOMAIN.md` (10:43): 10 resamples, "no interval" | `SchwingNet/NUMBERS.md` Revision 3: `fit.json` 11:59, n_boot 2,000 | **B** is newer; INDOMAIN.md text may be stale against fit.json; neither is quoted |
| Contribution narrative | `results/DATA_CONTRIBUTION.md` prose | `results/contribution_matrix.json` | **JSON** (the prose preamble lists nine corrections) |
| Selective-prediction denominator | 16,392 vertebrae (file header) | ~8,280 test-half vertebrae (`docs/MODEL_CARD.md` §5.3 arithmetic) | **B** |
| Paper-1 title | memory/paper-split-2026-09-24.md: "… robust to transitional anatomy" | `SchwingNet/main.tex` line 61: no clause | **B** (the file as built) |
| Blinded paper-2 gate job | memory/resume-2026-09-24.md: 40438005 | `REVISION_LOG3.md` line 7: f6eval 40431765/40431766 held | both are recorded as held; which one carries the post-section-15 detector is not stated in a file read |
| Word count | commit 044ca9a: 2,988 | `PER_LEVEL_DOMAIN_ANGLE.md`: 2,998 | not resolvable without running `tools/check_limits.py` |
| Affiliation | `paper/rsnai/main_v2.tex`: Department of Neurosurgery | memory/user-affiliation-general-surgery.md: General Surgery | **B** (Greg's own correction) |
| COBRA Varian cases | 24 (manifest 06:49 2026-09-22, mid-fetch) | 26 (grid recount 2026-09-23) | **26** (`SchwingNet/NUMBERS.md` COBRA Varian row) |

---

## 9. Recipes: how to regenerate each layer

All grid work goes through `sbatch` (never the login node; memory/no-jobs-on-login-node.md); ship code by commit, push,
and `git pull --ff-only` on the grid clone (memory/resume-2026-09-24.md); use `sbatch -D <dir>` because `--output`
resolves against the submit directory; network via WSL (CLAUDE.md).

| layer | command or script | notes |
|---|---|---|
| manuscript PDFs | `sbatch -D ~/logs ~/spinesurg-ct-nnunet/SchwingNet/slurm/compile.sh` (review); same with `--export=ALL,CAMERAREADY=1` for the camera-ready, chained `--dependency=afterany` | texlive/2020 module, TeX Gyre Termes; compile.sh now takes an flock — never run the two copies at once (commit 05e05dc); PDFs to `SchwingNet/build/{review,cameraready}/` |
| numbers into the tex | `python SchwingNet/tools/results_macros.py --check` | fails on a pending key, an unused key, or a bare result numeral in `sections/results.tex`/`main.tex` (`RESULTS_BUILD.md`); tables are not scanned |
| journal limits | `python SchwingNet/tools/check_limits.py` | words, abstract, figures, captions ≤ 60 words, refs, banned word, retired rule |
| packets | `python SchwingNet/tools/make_packet.py` (inputs `SchwingNet/packet_src/`, `build_packet_src.py`) | regenerate the ATLAS cards first (`SchwingNet/atlas/update_cards.py`, `validate_cards.py`) — they are stale |
| CLAIM checklist | `SchwingNet/tools/gen_claim_checklist.py`; `check_claim_checklist.py` | CLAIM 2024 map in `packet_src/claim2024/map.json` |
| Figures 1-5 | `SchwingNet/tools/figure1.py --panels …`; `figure2.py` (+ `figure2_analyse.py`); `figure3_network.py`; `figure4_frame.py --models v9init_pre --pull`; `fig_power.py` | each writes `figures/<name>.record.json` |
| Figures S1-S5 | `SchwingNet/tools/fig2_flow.py`; `python SchwingNet/tools/figS_supplement.py all` | builder refuses text < 12 pt or non-Arial |
| supplement tables | `make_supp_device_table.py`, `make_supp_census_tables.py --merged`, `make_supp_ablation_table.py` (all in `SchwingNet/tools/`) | — |
| rigor fixes a1-a9 | `tools/rigor_fixes.py report` (and subcommands such as `a3a-rows --only-unseen`) | RIGOR_CHAIN jobs in `SchwingNet/results/JOBS.txt` |
| statistical recomputation | `SchwingNet/tools/stats_review_recompute.py`, `stats_review2_recompute.py` | 2,000 resamples, seed 0 |
| v9 C-ArmLSpine CV and zero-shot | `SchwingNet/results/eval_gate/closure/cv_v9/closure_cv_v9.py`, `closure_only.sh` | fold training `carmcv9i`; k-in-field `zs9kfield`; the old fold dirs are `~/carm_cvmix{0..4}_fov96_ctx` |
| counting | `sbatch SchwingNet/slurm/counting.sh` (`tools/count_from_sacrum_eval.py --self-test` first) | report `SchwingNet/tools/counting_report.py` |
| coupling | `sbatch SchwingNet/slurm/coupling.sh` (`tools/alphabet_couple.py --self-test`) | posteriors from `tools/level_prototype.py --dump-posterior --sacrum-detector` |
| contribution matrix | `sbatch SchwingNet/slurm/contrib_matrix_cpu.sh` → `SchwingNet/tools/contribution_matrix.py` | needs `realxray_eval.py --dump-raw` dumps of each arm |
| real-frame learning curve | `SchwingNet/slurm/lcurve_prep.sh`, `lcurve.sh` (array per `lcurve_manifest.txt`), `lcurve_report.sh` | stage-1 = `dc_B_held_<device>(_s1)` |
| in-domain fills | `SchwingNet/slurm/lcurve_fill*.sh` (`tools/lcurve_fill.py`), `name_fill*.sh` (`tools/indomain_name_fill.py`); fit `tools/indomain_fit.py`, `indomain_fit_docs.py` | — |
| film N-curve | `SchwingNet/slurm/film_ncurve_prep.sh`, `film_ncurve.sh`, `film_ncurve_collect.sh` (`tools/film_ncurve.py`) | about 18 GPU-min per cell (`REVISION_LOG3.md` §13) |
| render ablation | `SchwingNet/slurm/film_ncurve_ablation.sh` (ARM imagenet / filmonly) + `film_ncurve_ablation_collect.sh`; read `SchwingNet/tools/film_ncurve_ablation_read.py` | ~15 GPU-hours per arm |
| coverage arms and pooled fit | `SchwingNet/slurm/coverage_arms_{render,train,score,collect}.sh` (`tools/coverage_arms.py`); `tools/indomain_fit_coverage.py --film` | conf 0.74 sensitivity in `results/coverage/sensitivity/` |
| acquisition-space coverage | `sbatch SchwingNet/slurm/acq_coverage.sh` (`tools/acq_coverage.py`) | — |
| denominator repair / miss diagnostic | `SchwingNet/slurm/carm_denominator_repair.sh`, `carm_miss_diagnostic.sh` | re-score, never retrain |
| case134 spin | `tools/case134_sweep.py` | detection only; no level truth |
| manifold | `sbatch SchwingNet/slurm/manifold.sh` (`tools/corpus_manifold.py`) | features, deep, probes |
| eval gate audit | `tools/leak_check.py chk9`; `SchwingNet/results/eval_gate/leaks/build_eval_leaks.py` | inputs `results/eval_gate/quoted_results.json`, `/rs/.../or_ready/eval_gate/touched.json`, `eval_sets.json` |
| device cards | `slurm/device_fit.sh` (CMD/DEVICE/EXTRA) → `tools/device_fit.py`; cards written in the grid repo copy, rsync back | `docs/devices/surgio_b51_dr.json` exists only on the grid (`DATA_CONTRIBUTION.md` correction ix) |
| physics / linking | `make physics`, `make physics-tables`, `make physics-check` | `docs/HANDOFF_PHYSICS.md` |
| sweep | `slurm/sweep_v3.sh`; table `tools/make_results_table.py` | `--end-rule skip` |
| feasibility ledger | `slurm/reproduce_feasibility.sh` → `LEDGER.tsv`; `slurm/reproduce_all.sh` (19 stages) | RECORD ONLY |
| runtime | `python tools/eval_runtime_cost.py --selftest`, then the §8 command in `docs/MODEL_CARD.md` | detector stage needs ultralytics |
| older claims ledger | `python tools/claims_check.py` | covers only `docs/RSNAI_CLAIMS.json` (54 claims of main_v2) |

---

## 10. Which data each SchwingNet component uses, and what is not used (results view)

The data side proper is `data_platform/README.md` and `data_platform/DATA_MANIFEST.md` §1 (not redone here).

| component | trained on | file |
|---|---|---|
| keypoint (naming) detector `detector_v5z_final` | film keypoint corpus `data/yolo_v4z` (spine-detector), fine-tuned from detect_v3 | `docs/MANIFEST_DATA_MODELS_RESULTS.md` §5.3; memory/xray-corner-detector-status.md |
| sacrum detector `rx_lodo_carmlspine_1024` | COBRA2026 Elekta train+val 2,832 + DeepFluoro train+val 262 real frames; parent trained on TotalSegmentator renders | `SchwingNet/NUMBERS.md` "detector training frames"; `results/eval_gate/LINEAGE.md` |
| v9 level encoder + head | `allspine_v9`: CSXA 4,963, BUU-LSPINE 3,603, NHANES II 543 films (no VinDr, no AASCE, no Mendeley); renders ctsp_drr, verse_drr, physics_drr (TotalSegmentator), physics_rare | `docs/XRAY_DATASET_USAGE.md` table; `PER_LEVEL_DOMAIN_ANGLE.md` Table D |
| C-ArmLSpine fold models | per-fold mixed bank (fold 0 crops): buu 635, csxa 1,758, nhanes 303, nhanes_drr 277, ctsp_drr 638, verse_drr 940, physics_drr 5,285, physics_rare 1,132, FluoroCap 2,100, VinDr pseudo-labels 2,632, C-ArmLSpine AP 7,869, LAT 7,827 | `docs/MODEL_CARD.md` §3.2 (v2 lineage; `CV_V9.md` says v9 folds use the same banks) |
| device cards / styled renders | Cios Fusion (DeepFluoro), Elekta XVI (COBRA, 40 frames of 3 cases), BV Pulsera (Geneva phantom), PIXIUM 4600 (Ljubljana), Surgio-B51 (C-ArmLSpine); 142 clean TotalSegmentator whole spines rendered | `docs/devices/*.json`; memory/k-devices-one-network.md; `SchwingNet/NUMBERS.md` CT counts row |

Not used by any reported model (from the files): COBRA2026 Varian (26 cases fetched), the rest of the 692-case COBRA
release beyond 145 Elekta cases, SpineSAC (no bone truth), AASCE (457 films in its own bank only), Mendeley 5jdfdgp762
(excluded, BUU re-encodings), IEEE lateral 236, Spinal-AI2024 (machine generated), the 16,530 unannotated NHANES II
films (except as pseudo-labels in banks now banned), VinDr in the level bank (fold banks only), Geneva (test-only),
case134 spin (detection test only) (`docs/XRAY_DATASET_USAGE.md`; `docs/RSNAI_TABLE1_DATASETS.md`; `SchwingNet/NUMBERS.md`
Counts rows; `docs/MANIFEST_DATA_MODELS_RESULTS.md` §7.4).

---

## 11. Open items that change results (as recorded on 2026-09-27)

| item | owner / blocker | file |
|---|---|---|
| supplement 13 pages against the 12-page cap | text cut needed | commit 05e05dc; `RSNA_AI_REQUIREMENTS.md` line 21 |
| ATLAS cards and twins carry superseded numbers | regenerate | section 8 |
| VinDr determination number and date | known: HPR 2026-330, 29 September 2026; print it | `main.tex` `\PENDING{G0}` |
| per-level supplement table S5 (L1-L5 × view × field) | Greg's yes/no | `PER_LEVEL_DOMAIN_ANGLE.md` "Getting it in front of a doctor"; RESUME 2026-09-27 18:05 "FOR GREG" |
| ratio sweep (`real_share` 0.1-0.9 at N = 25 and all, 3 seeds, ~45 cells) | Greg's yes/no | same |
| seeds 1-2 above N = 25 (18 cells × 2 arms) — the BUU-all reversal rests on one seed | Greg's yes/no | same |
| held-out plain-film naming | needs the ImageNet-init arm scored on G3 test films (f6eval held) | `EVAL_LEAKS.md` L4 |
| any transitional accuracy on real exposures | human reads of COBRA candidates (transitional review tree, `docs/REVIEW_TRANSITIONAL.md`, `docs/ruleclass/PREREG_rules.md` draft) | memory/paper-split-2026-09-24.md; RESUME 2026-09-27 16:45 |
| flagship detector on body boxes (G4/G5) | never built; `SchwingNet/results/final/` does not exist | `docs/FLAGSHIP_PLAN.md` gates; the `tables/tab2_detection.md` twin still lists "PENDING G5" flagship rows, the printed `tab2_detection.tex` no longer carries them |
| paper 2 reference scoring | fix `SchwingNet/tools/fig6_score.py` gate path | `paper2_levelcheck/open_gate_40438004/README.md` |
| unexplained half-recall of the held-out detector on the case134 spin | not investigated further | `figures/figS4.record.json` (record real_lodo_flat_half) |
| exposure clip still default (typicality gate not A/B-tested on real frames) | `slurm/device_spread_arm.sh` | `docs/DEVICE_SPREAD_SWEEP.md` |
| calibration of the posterior (no reliability diagram, ECE or Brier anywhere) | not started | `docs/MODEL_CARD.md` §5.3, §8 item 5 |
| weight registration and code SHA in `devcorpus_train.py` scores | not done as of the card | `docs/MODEL_CARD.md` §1.2-1.3 |

---

## 12. Unknowns

| fact | where looked |
|---|---|
| Exact body word count after the 2026-09-27 Discussion sentence (2,988 vs 2,998) | commit messages 044ca9a, 05e05dc; `PER_LEVEL_DOMAIN_ANGLE.md`; `check_limits.py` not run (read-only) |
| Result of the re-implemented competitor ensemble (124 cells, dev→test drop) | `docs/COMPETITOR_BENCHMARK.md`, `docs/MANIFEST_DATA_MODELS_RESULTS.md`, `docs/PIPELINE_RESUME.md`, `docs/RESUME_2026-09-22_PM.md` — only the path `~/model_night/ensemble/ensemble.json` (grid) is recorded |
| Outcome of guided-acquisition job 40376577 | `docs/GUIDED_ACQUISITION.md` STATUS block (2026-09-18), `docs/INVENTION_DISCLOSURE.md` §8, RESUME — not recorded |
| Whether the runtime GPU job (`slurm/runtime_cost.sh`, MODEL_CARD §6.6) ran, and the detector-stage latency | `docs/MODEL_CARD.md` §6; RESUME — not recorded |
| Whether the DeepFluoro cards were refitted under `DF_CONVERSION=linear` | memory/learned-formation-refuted-calibrate-instead.md; `docs/DEEPFLUORO_FORMATION.md` not read in full — not established |
| Box convention of the `scores.json` rows in MODEL_CARD §4.6 and why `dc_B_held_cios_fusion_s1` has no row | `docs/MODEL_CARD.md` §4.5-4.6 — the card itself says not recorded |
| Which held paper-2 job (40438005 vs 40431765/66) carries the post-section-15 detector | memory/resume-2026-09-24.md; `REVISION_LOG3.md` lines 7, 96-97 |
| Why the reported held-out detector finds exactly half the boxes in 15 of 19 angle bins on case134 | `figures/figS4.record.json`; `results/arc/case134_sweep.md` — recorded UNEXPLAINED |
| 7,045 physics-styled renders in Table 1 footnote a vs 7,048 items in that root | `SchwingNet/supplement.tex` "Corpus census" — recorded unexplained |
| Per-angle level naming | `PER_LEVEL_DOMAIN_ANGLE.md` §"What is not known" — does not exist |
| Held-out per-level film naming | same — only the DERIVED selection-split Table E exists |
| Any synthetic:real ratio sweep on the current line | `PER_LEVEL_DOMAIN_ANGLE.md` Table A; `memory/synthetic-real-ratio-evidence.md` — never run |
| Rare-class (L6/T13) accuracy on any real image with a human read | `SchwingNet/main.tex` Results; `PER_LEVEL_DOMAIN_ANGLE.md` "What is not known" — none exists |
| Whether the 148 C-ArmLSpine cases are 148 people | `sections/discussion_limits.tex`; `docs/PATIENT_IDENTITY_SPEC.md` (cited, not read in full) — "cannot be established" |
| The memory note `manifest-data-models-results` | `memory/` listing (165 files) — absent |
| Selection effect of the v9 checkpoint on the alphabet-loss L6 recall (56.1-72.4 %) | `EVAL_LEAKS.md` item 6 — "has not been measured" |
| Current seed spread of detector designs beyond the four rows read | `docs/MODEL_CARD.md` §4.5 — partial |
| Whether the `ts12` and `v8` overlap corrections changed any printed number after 2026-09-24 | `MANUSCRIPT_CORRECTIONS.md` §2.3-2.4 (read in outline only) |
| `/rs/` and `~` files named above (grid only) — contents not re-verified | grid not contacted by instruction |
