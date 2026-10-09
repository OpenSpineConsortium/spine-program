# Sources for every number in `sections/methods.tex` (data passage and mechanism sentences), 2026-09-23

> **2026-09-23, six-figure wrap.** `methods.tex` was rewritten around the six figures. Rows below still trace
> every data-passage number that survived (sources, reference standard, detector, level model, folds, statistics).
> New in the rewrite and traced in `SchwingNet/NUMBERS.md` section "The six-figure wrap": the encoder-embedding
> paragraph (2,889 crops of 164 persons dropped; `results/figure2/figure2_metrics.json#cleaning`), the transitional
> typing (`results/rare_class/transitional_subtypes.csv`) and the LevelCheck comparator paragraph (82.2 %, 97.6 %,
> 92.6 %, the draw, the test, Holm at 0.025: `SchwingNet/LEVELCHECK_MODEL.md` §3-§5, commit ecae75f). Cut from
> Methods: the per-device image-formation paragraph (now supplement text), the pending flagship-arm sentence and the
> partition details of the film bank.


> **2026-09-24, re-wrap against the morning's figure builds.** New in `methods.tex`, each traced in `NUMBERS.md`
> rows marked "(2026-09-24)": the automated reference for unread transitional test persons (`LEVELCHECK_MODEL.md`
> §14, commit b511985); the fused-L5 analysis of the encoder paragraph (`results/figure2/figure2_transitional.json`);
> the keypoint detector named YOLO11m-pose (`atlas/model.json`) and the sacrum detector fine-tuned from the
> render-trained detector (`results/eval_gate/LINEAGE.md`); the scored arm's encoder from ImageNet weights
> (`results/fig6/RUN_v2.json`); the three secondary analyses fixed before unblinding (`LEVELCHECK_MODEL.md` §12-§13,
> commits 1897772 and 2993f40); the power statement of the statistics paragraph (at a true 95 %: 55, 71 at Holm
> alpha/3, below 0.1 % against 97.6 %, 708 at a true 99 %; `results/power/power.json#panel_b/drawn`). Cut for length:
> the detector's 1,024-pixel input and class names (in Figure 3), the list of the three supplement Holm comparisons
> (named in the supplement), "five bodies in view" among the secondary outcomes (Table 4's twin keeps the row). The
> analysis end date is now 24 September 2026. Supplement figure numbers follow `supplement.tex` (S1 flow, S2
> manifold, S3 formation, S4 detector source, S5 angle).

Paths are repo-relative. Where a number is already in `SchwingNet/NUMBERS.md` the row is named; otherwise the
file and field are given.

## Study design and data

| sentence | number | file |
|---|---|---|
| ethics | HPR 2026-269 | `main.tex` line 63 (Ethics); `CLAIM_CHECKLIST.md` row 137 |
| CTSpinoPelvic1K | 802 records, 801 rendered, 0533 truncated | NUMBERS.md "Counts in Methods" (CTSpinoPelvic1K 802 → 801); `docs/CT_INVENTORY.md` `ctsp_drr` 801; `docs/PATIENT_IDENTITY_SPEC.md` §2 ctsp |
| TotalSegmentator | 1,170 (v2) and 1,735 (v3) renders; 1,935 distinct scans; no patient identifier | `docs/CT_INVENTORY.md` `ts_drr`, `ts_drr_v3`; `docs/PATIENT_IDENTITY_SPEC.md` §2 ts ("No patient identifier exists", 1,935) |
| TotalSegmentator clean list | 142 subjects, 17 validation; criterion: every level C2–L5 and the sacrum with ≥ 200 voxels each, and fewer than 20 voxels above 2,500 HU inside the vertebral union | `tools/ts_clean_subjects.py` (`NEED`, `MIN_VOX = 200`, `METAL_HU = 2500`, `METAL_VOX = 20`); count 142 in `docs/PATIENT_IDENTITY_SPEC.md` §2 devcorpus and NUMBERS.md (1,228 → 1,170 → 142 → 17); 17 validation in `docs/DATASHEET.md` §2.7. The 200-voxel floor is in the script and not in the prose (word budget); the prose says "labelled". CLAIM_CHECKLIST row 8 records that this criterion was not written in any document; it now is, here. |
| VerSe | 374 series, 355 subjects, masks C1–L6, 387 renders; no accuracy quoted (series keyed as subjects) | `docs/PATIENT_IDENTITY_SPEC.md` §2 verse; `docs/CT_INVENTORY.md` `verse_drr` 387; NUMBERS.md "Numbers deliberately absent" (v8 VerSe) |
| CSXA | 4,963 films, 4,963 individuals, released per-vertebra levels | `docs/DATASHEET.md` §2.6; `docs/PATIENT_IDENTITY_SPEC.md` §2 csxa |
| BUU-LSPINE | 3,600 cases; 3,603 lateral, 3,600 AP films; levels by position from end-plate lines L1–S1 | `docs/PATIENT_IDENTITY_SPEC.md` §2 buu (`films_drr 3,603`, `films_ap_drr 3,600`, 3,600 by the released table); `docs/DATASHEET.md` §2.6 |
| NHANES II | 543 films with landmarks, 364 persons, digitised national survey | `docs/DATASHEET.md` §2.6; `docs/PATIENT_IDENTITY_SPEC.md` §2 nhanes (364) |
| CSXA/BUU/NHANES role | level bank training and film validation split, zero validation patients in training | `docs/MODEL_CARD.md` §3.2 fold bank; NUMBERS.md "Plain film" leak check (`results/a5.json#leak_check_by_patient_key`) |
| VinDr-SpineXR | 10,466 images, 5,000 studies, lesion boxes, pseudo-labelled, training only, nothing quoted | `docs/PATIENT_IDENTITY_SPEC.md` §2 vindr; `docs/DATASHEET.md` §2.6; NUMBERS.md "Numbers deliberately absent" (any VinDr number) |
| FluoroCap | 2,385 panels in the bank, 29,484 harvested; training only; no patient identifier, no patient count | `docs/CT_INVENTORY.md` `fluorocap_drr` 2385; `docs/DATASHEET.md` §2.5 (29,484), §2.6 (train-only, republished figure = same patient); `docs/PATIENT_IDENTITY_SPEC.md` §2 and §4 fluorocap ("never report a patient count") |
| C-ArmLSpine | Surgio-B51; one AP + one lateral + CBCT per case; 149 released, 148 built, 296 frames; roles | `docs/DATASHEET.md` §2.1 and §3; NUMBERS.md "Counts in Methods" (149 → 148, 296); `docs/MODEL_CARD.md` §4.1 (five-fold CV; fixed test) |
| C-ArmLSpine exclusion | case134: no AP or lateral, a raw 302-frame sweep, residual patient identifier; entered no bank; reported to the authors | `docs/DATASHEET.md` §3 Sampling; `docs/PATIENT_IDENTITY_SPEC.md` §3 row 16 (302 XA frames, real PatientID and PatientName under `case134/ori/`); NUMBERS.md "Counts in Methods" row "302 XA frames in case134/ori"; "reported to the dataset authors" is the standing Ethics sentence in `main.tex` line 63. The old prose said "one failed conversion"; the reason now given is the one the datasheet records. |
| DeepFluoro | six cadaveric specimens, Siemens Cios Fusion, 366 frames, CT and pose per frame; 4/1/1 specimens, 238 training frames; device card | `docs/DATASHEET.md` §2.1; NUMBERS.md "Counts in Methods" (DeepFluoro six specimens, 366, 4/1/1, 238/24/104); `docs/devices/cios_fusion.json` (card) |
| COBRA2026 release | 692 public cases; six centres (A–D Elekta XVI, F–G Varian); planning CT deformably registered | `docs/DATASHEET.md` §2.1 and §3; `docs/HANDOFF_2026-09-21_PM.md` line 607 ("six centres, 867 patients, 692 public"). The task text said seven centres; no file on disk says seven, so the prose says six. |
| COBRA2026 fetch | 152 Elekta and 26 Varian fetched; cut by download volume, no criterion | `docs/RESUME_2026-09-22_PM.md` lines 981–985 (42 GB per 152 cases, "not by any criterion"; 26 Varian = F 14 + G 12). **Discrepancy**: `docs/DATASHEET.md` §2.1/§3, `docs/RSNAI_TABLE1_DATASETS.md` and Table 1 footnote i all say **24** Varian cases. **Recounted on the grid 2026-09-23** (`find /rs/rs_grp_oschome/go2432/data/cobra2026/cases -maxdepth 1 -type d -name 'F*'/'G*' ! -newermt '2026-09-22 23:45'`): 14 F and 12 G case folders, each with `projections.mha`, all older than the full-release fetch that began 23:53 on 2026-09-22 (`centre_F_cases.txt` 23:51:30; F028/G016 landed 23:53). Three F cases arrived 2026-09-21 15:26–15:29 and the other 23 between 06:40 and 07:05 on 2026-09-22; the datasheet's manifest was built at 06:49 that morning, mid-fetch, which is where 24 came from. **26 is right.** Resolved 2026-09-23: Table 1 footnote i, `tables/tab_corpus.md` note i, `tables/tab_corpus.sources.md`, `docs/DATASHEET.md` §2.1, §3 and the census block, `docs/RSNAI_TABLE1_DATASETS.md` row Varian (and its generator `tools/rsnai_table1.py`), `atlas/dataset.json`, `CLAIM_CHECKLIST.md` rows 8 and the census, `claim_checklist.json` and `NUMBERS.md` all now say 26 (F 14, G 12), each with all five files. |
| COBRA2026 used | 145 Elekta cases with usable geometry; 3,480 frames; 110 / 8 / 27 patients; trained the detector and the Elekta card; Varian used by no reported model | NUMBERS.md "Counts in Methods" (692 → 152 → 145; 110/8/27; 2,640/192/648 = 3,480); `docs/MODEL_CARD.md` §3.1; `docs/devices/elekta_xvi.json`; Table 1 footnote i and `tables/tab_corpus.sources.md` "Footnote i" (Varian absent from every training list in MODEL_CARD §3). "Usable geometry" covers B000 (41 frames the CT never covers, `docs/DATASHEET.md` §3 reading traps); the other six of the seven dropped cases are not itemised in any document read. |
| Geneva hip | Philips BV Pulsera image intensifier; one resin phantom; 116 frames; gold-standard pose; test only, unseen device | `docs/DATASHEET.md` §2.1; NUMBERS.md "Counts in Methods" (Geneva one phantom, 116 frames); `docs/MODEL_CARD.md` §4.1 |
| Ljubljana | one cadaveric L1–L5 specimen; turntable flat panel (Trixell PIXIUM 4600); 18 radiographs; device card only, no anatomy learned | `docs/DATASHEET.md` §2.1; `docs/PATIENT_IDENTITY_SPEC.md` §2 ljubljana; `tables/tab_corpus.sources.md` row Ljubljana ("absent from every training list in MC §3") |

Not written in the manuscript, recorded here as instructed: the full COBRA2026 release is being fetched
(`slurm/cobra_fetch_all.sh`, `docs/RESUME_2026-09-22_PM.md` A10) and the final version of this manuscript uses
all of it; every "of 692" clause then goes away, and any exclusion is by a stated criterion.

## Level model, the two mechanisms

| claim | file |
|---|---|
| counting from the anchor: sweep links overlapping exposures, sacrum is ordinal 0, each body an ordinal from it, no morphology read, accuracy bounded by detection | `docs/MODEL_CARD.md` §5.2 ("Collimation is the binding constraint on detection"), §5.5 (sweep numbers use the annotation's boxes); memory `sweep-map-replaces-registration`, `detection-is-the-binding-constraint` |
| naming from morphology: context crop per detected body, recurrent head over the run; counts when the anchor is in the run, names from crop and neighbours when it is not | `docs/MODEL_CARD.md` §1.1 (the four pieces), §3.2; `tools/level_prototype.py`; `docs/carmlspine_cv5_mixed_2026-09-21.json` (k1/k3/k5/kfull cells = runs with and without the anchor) |
| "every level accuracy in Results measures this second mechanism on single exposures; no counting-chain accuracy is quoted" (checker's rewording, 2026-09-23: the earlier "every number in Results is labelled by the one it measures" was false as the manuscript stands, since `sections/results.tex` labels no row by mechanism) | every level accuracy in `sections/results.tex` is a `det/*`, `oracle/*`, zero-shot or plain-film naming cell (`results/a4.json`, `a5.json`, `a7.json`, `a9.json`); `grep -i 'sweep\|chain\|linker'` over `main.tex`, `supplement.tex` and `sections/*.tex` finds no counting-chain accuracy, only the Figure 1–2 captions (a demonstration margin of 0.37, not an accuracy) and `discussion_limits.tex` ("measured on annotation boxes and commanded moves, bounding the linker"). "The head may count along it" replaces "it can count": the head takes the run's embeddings (`docs/MODEL_CARD.md` §1.1), and whether it counts when the sacrum is in the run is a mechanism reading, not a measured claim. |

## Word budget, and what was cut

`python SchwingNet/tools/check_limits.py` after this pass: Introduction to Discussion **3,267 words (limit
3,000)**; Materials and Methods 1,219 (was 929), of which the data passage is 509. The other sections are
unchanged (Introduction 502, Results 865, Discussion 681 after a 15-word trim in `discussion_limits.tex`).
The checker also fails on `FINAL_CHECK.md: retired rule named`, which predates this pass.

The data passage cannot carry thirteen datasets with counts, roles and exclusion reasons in fewer than
~500 words, and the rest of Methods is now 710 words; reaching 3,000 inside Methods alone would delete
the model, detector or statistics description. **267 words must come from Introduction, Results or
`discussion_motivation.tex`, which other passes own.** Candidate: the Results paragraphs that restate the
counting-versus-naming distinction now made in Methods.

Text removed from Methods that belongs in the supplement (`supplement.tex`, owned by another pass):

- Device cards: the list of the nine image-formation terms (polyenergetic transmission, scatter, collimator
  penumbra, quantum draw, receptor blur, edge enhancement, vignetting, heel effect, display match); that the
  per-frame exposure terms were stored as a copula and the draws used here clipped to the central 60 % of
  each marginal.
- Statistics: that the 1,440 rescoring cells are six arms × three sets × 16 thresholds × three box
  conventions, with arm and set fixed by the question; that the six film-versus-fluoroscopy cells are the
  pooled cells; that the ledger re-derives each number from its result file.
- Detection: that the 85 held-out cells are recomputed from per-frame predictions; that the equal-count arm
  cut COBRA by patient (the prose now says "cut to DeepFluoro's count").
- Partitions: that the fine-tuning base of each fold, not only the initialisation, comes from the leaking bank
  family (`docs/MODEL_CARD.md` §3.3).
- Level model: that the sweep logic is parameter-free.

Words that still count and were kept on purpose: "TotalSegmentator" and "VERIDAH" citations in the
reference standard (the tools are named there, so the data passage does not repeat the citation).
