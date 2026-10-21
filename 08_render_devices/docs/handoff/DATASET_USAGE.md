<!-- spine-program/08_render_devices: copy of spinesurg-ct-nnunet 097933a HANDOFF/DATASET_USAGE.md (copied 2026-10-08; redactions, if any, are listed in MANIFEST_LOCAL.md section 3). Laptop spellings of the path prefixes (`C:/` drive paths, the session scratchpad, the memory folder) are history, not dependencies: read them through this folder's CLAUDE.md "Prefixes in the copied documents". -->

# What data the SchwingNet model uses today, and what it does not

Greg asked (2026-10-08): "tell me the current usage of the datasets in my schwingnet model and what im not using". This
file answers from files on the laptop only. Nothing after 2026-09-27 changed the banks or models as far as any file
shows (`working_notes/topic3_dataset_usage_leakage_rsna.md` preamble). The data side as a whole (where each dataset came
from, licences, re-acquisition, the move to Ceph) is `ssn:data_platform/` (`README.md`, then `DATA_MANIFEST.md` §1); this
file does not redo it. Path prefixes as in `RESULTS_CATALOG.md`.

---

## 0. The short answer

1. **"The SchwingNet model" is five pieces** (§1): a film-trained keypoint body detector (`detector_v5z_final`), a
   real-frame vertebra and sacrum detector (`rx_lodo_carmlspine_1024`), the `allspine_v9` level encoder, its recurrent
   head, and, for the fine-tuned numbers only, five C-ArmLSpine fold models re-initialised from v9.
   `ssn:docs/MODEL_REGISTRY.md` does not name it; the identification is from `sn:atlas/model.json` and
   `ssn:docs/CINE_DEMO_RECON_2026-09-26.md` §1.
2. **The level encoder learns from three radiograph corpora and three CT collections only**: CSXA (4,963 films),
   BUU-LSPINE laterals (3,603 files, 3,600 people), the 543 annotated NHANES II films, and renders of CTSpinoPelvic1K,
   VerSe 19/20 and TotalSegmentator v2 (`ssn:slurm/allspine_v9_bank.sh`; `ssn:docs/XRAY_DATASET_USAGE.md`;
   `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 536). Its bank is `allspine_v9_fov96_ctx`.
3. **Not in the level bank at all**: VinDr-SpineXR (0 of 10,466), the 16,531 unannotated NHANES films, the 3,600 BUU AP
   films, AASCE, Mendeley, IEEE lateral-236, Spinal-AI2024, FluoroCap, TotalSegmentator v3 renders (`ts_drr_v3`), RSNA
   2022 cervical CT, RibFrac, CTSpine1K, and every real C-arm frame (§2, §4).
4. **But the C-ArmLSpine fold models (the fine-tuned naming numbers in the paper) still train on VinDr and FluoroCap
   crops**: 2,632 VinDr crops of 2,071 films and 2,100 FluoroCap crops of 950 panels per fold bank, plus both NHANES
   copies, because the v9-initialised fold models reuse the fold banks built from `allspine_v7`
   (`ssn:docs/MODEL_CARD.md` §3.2; `sn:results/eval_gate/closure/cv_v9/CV_V9.md` preamble; `ssn:slurm/carmlspine_cv_v9init.sh`
   lines 11, 67). This contradicts directive D1 (FluoroCap out of every training set) and uses VinDr (a PhysioNet data
   use agreement) covered by WSU IRB HPR 2026-330 of 29 September 2026, the supplement to determination 2026-269 (`sn:packet_src/statements.md` item 5). See §5. **Fold models
   without VinDr or FluoroCap already exist**: the 250 Figure 5b `name_fill` cells were fine-tuned from the v9 encoder
   on the v9 per-class-600 base sample (no VinDr, no FluoroCap, one NHANES copy), including N = all and both-protocol
   models (§3.2; `RESULTS_CATALOG.md` A9).
5. **The detectors**: the body detector's film corpus is 12,709 films (CSXA, BUU AP + lateral, the 543 NHANES), "with no
   written reason for the other 26,996" held films, and it has never seen a VinDr vertebra
   (`ssn:docs/DATA_COMPLETENESS_AUDIT.md` re-count, "Gaps the auditor missed"). The sacrum detector trains on real COBRA2026
   Elekta (118 cases: 110 train + 8 val) and DeepFluoro (5 specimens: 4 train + 1 val) frames only, 3,094 frames
   (`sn:NUMBERS.md` "Counts in Methods" L183, L184, L187; the split names, without counts, are in
   `sn:results/eval_gate/EVALUATORS.md` line 524).
6. **Real C-arm data is barely used**: of COBRA2026's 692 fetched public cases only 145 Elekta cases (24 frames each)
   are in any frame bank and 0 of 225 Varian; 2,293 DeepFluoro vendor frames, the second C-ArmLSpine CBCT sweep, the
   Ljubljana frames and all SpineSAC frames train or score nothing (§2).

---

## 1. Which model is "the SchwingNet model" today

| piece | weights (grid) | trained on | used for | source |
|---|---|---|---|---|
| body (corner) detector | `~/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (alias `detector_v5z_final`; same file as `~/FluoroCap/detect_v5z_final_best.pt`), YOLO11m-pose, confidence 0.35 | `data/yolo_v4z` (zoomed windows), fine-tuned 60 epochs from `detect_v3` (`data/yolo_v3`), from COCO yolo11m-pose; per-source composition of `yolo_v3` / `yolo_v4z` not recorded | the naming boxes (boxed 617 of 676 agreed lateral bodies) | `ssn:docs/CINE_DEMO_RECON_2026-09-26.md` §1; `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` lines 434-437; `sn:results/eval_gate/LINEAGE.md` line 42 |
| vertebra / sacrum detector | `~/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt`, YOLO11m, confidence 0.74 ("cross-device") or 0.25 | COBRA Elekta train+val (110 + 8 cases) and DeepFluoro train+val (238 + 24 frames, 5 specimens) real frames = 3,094 frames (2,832 + 262); initialised from `pose/anchor_none_v2_17-1882` (TotalSegmentator renders) from COCO yolo11m; 80 epochs, seed 0, imgsz 1024; `best.pt` selected on COBRA test + DeepFluoro test | the sacrum anchor for counting; held-out detection on C-ArmLSpine | `sn:results/eval_gate/EVALUATORS.md` lines 53, 129, 523-524; `sn:NUMBERS.md` "Counts in Methods" |
| level encoder | `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (sha256 prefix 188f9fcbfa3c6de1), ResNet-18, two-channel stem, 320 px crop, target 96 px, 27 classes (C1-C7, T1-T13, L1-L6, sacrum) | `allspine_v9_fov96_ctx` (§3.1); 9,592 train / 1,776 val person keys; 40 epochs, `--augment 2`; best epoch chosen on the val split | zero-shot naming; Figure 2 | `ssn:docs/CINE_DEMO_RECON_2026-09-26.md` §1; `LINEAGE.md` row `allspine_v9`; `ssn:slurm/allspine_v9_train.sh` |
| recurrent head | `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (two-layer BiGRU over 2-9 bodies) | the same v9 bank, mixed runs of 2-9 bodies (`tools/head_mixed_length.py --train-mode mixed --kmax 4`) | sequence naming | same; `sn:results/eval_gate/EVAL_LEAKS.md` U1 table |
| C-ArmLSpine fold models (fine-tuned numbers only) | `~/carm_cvmix{k}_fov96_ctx/runs/model_rung_1_ft_cv{k}_v9init_aug2.pt` + `~/model_night/heads_carm/head_cv{k}_v9init.pt`, k = 0-4 | the shipped fold banks `carm_cvmix{k}` (§3.2), fine-tuned from the v9 encoder | the case-grouped and day-grouped cross-validation (Table 3) | `ssn:slurm/carmlspine_cv_v9init.sh` lines 11-23, 43-75; `CV_V9.md` |
| count and coupling | no learned parameters: `tools/count_from_sacrum_eval.py`, `tools/alphabet_couple.py` | — | the ordinal from the detected sacrum; the stop signal | `sn:results/COUNTING.md`; `sn:results/COUPLING.md` |

Not part of it: the un-suffixed `ft_cv{k}_aug2.pt` fold models (initialised from `allspine_v2_r1`, whose training bank was
deleted; the gate refuses them); `detect_v5z_epoch25`, the checkpoint shipped in `~/level_id_service` (a different
product with a different detector, `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` line 437); the device-corpus detectors
`dc_A/B/P_*`, which appear only in the supplement's detection analysis (`sn:results/DATA_CONTRIBUTION.md`).

Headline numbers this stack carries: zero-shot lateral 595 / 617 = 96.4 % on C-ArmLSpine; case-grouped five-fold
601 / 617 = 97.4 %; day-grouped 568 / 617 = 92.1 % (`RESULTS_CATALOG.md` A2-A3).

### Bank lineage of the level encoder

| bank | date | what changed | status | source |
|---|---|---|---|---|
| `films_ann_fov96_ctx` | 2026-09-13 | CSXA + NHANES only; 14 of 27 classes live | record only | `ssn:docs/MANIFEST_DATA_MODELS_RESULTS.md` §1.2 |
| `films_all2_fov96_ctx` | 2026-09-13 | CSXA + BUU + VinDr 744 + NHANES 543; no T2-T11, T13 or L6 crops | superseded | `context/level-model-bank-coverage.md`; `DATA_MANIFEST.md` Appendix A2 |
| `allspine_fov96_ctx` | 2026-09-14 | films_drr + nhanes_drr + ctsp_drr + verse_drr + physics_drr | superseded | `ssn:slurm/allspine_bank.sh` |
| `allspine_v2` ... `v5c` | 09-15 to 09-18 | v3/v4 added VinDr 744 and AASCE; v5 added NHANES pseudo, lat236, Mendeley | deleted 2026-09-20 (quota) | `context/grid-quota-and-deleted-banks.md` |
| `allspine_v6`, `v7`, `v7nofluoro` | 09-17/18 | v7 = v2 + FluoroCap + VinDr pseudo (164,161 crops) | leaked (NHANES twice; CTSP under two names); v7 is the base of the fold banks | `DATA_MANIFEST.md` A2; `ssn:slurm/overnight_v7.sh` |
| `allspine_v8` | 2026-09-22 | v2 sources minus `~/nhanes_drr`, one split over people | VerSe series keyed as subjects (5 people on both sides) | `ssn:slurm/allspine_v8_bank.sh`; `context/identity-audit-findings.md` |
| **`allspine_v9`** | 2026-09-23 | v8 with VerSe keyed by subject (`patient_keys_v9.json`) | **current**; jobs keys 40415667, bank 40415668, train 40415669, a5 40415670 | `ssn:slurm/allspine_v9_bank.sh` |

---

## 2. Dataset by dataset

Columns: **on disk** = the raw tree; **level bank (v9)** = distinct films or renders in `allspine_v9_fov96_ctx`;
**other banks** = the largest count in any other crop bank on the grid (most superseded); **detectors**: B = body
detector `detector_v5z_final`, S = sacrum detector `rx_lodo_carmlspine_1024`; **device corpus** = `$RS/data/devcorpus` and
the `dc_*` arms; **fold models** = the `carm_cvmix{k}` fold banks behind the v9init fold models (crops, films in
brackets). **source** = the primary files behind the row, carried from the source column of
`working_notes/topic3_dataset_usage_leakage_rsna.md` §2 (that note keeps the cell-by-cell trail).

### 2.1 Radiographs

| dataset | on disk | level bank (v9) | other banks | detectors | fold models | used? and why not | source (per row; carried from the reader note) |
|---|---|---|---|---|---|---|---|
| CSXA cervical lateral | 4,963 PNG + JSON | 4,963 (4,214 train / 749 val) | 4,963 | B: yes | 1,758 crops (1,478 films) | **used fully**; only `datasets.xlsx` metadata unused; "one image = one person" is the release's claim, untested | `ssn:docs/XRAY_DATASET_USAGE.md`; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 106, 536; `ssn:docs/DATA_ACCOUNTING.md` §3; `ssn:docs/MODEL_CARD.md` §3.2 |
| BUU-LSPINE lateral (3600 release) | 3,604 jpg (3,600 ids; 3 byte-identical "(1)" copies) | 3,603 files = 3,600 people (3,070 / 533) | 3,603 | B: yes | 635 crops (589 films) | **used**; "3,603" is a file count printed as a film count | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 536, 839-851 |
| BUU-LSPINE AP (3600 release) | 3,600 | 0 | `buu_pair_fov48_ctx` (deleted) | B: yes | — | **not used, no valid written criterion**: the AP csv files carry the same end-plate lines; the ATLAS card's "availability of labels" reason is false | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 75, 425, 851 |
| BUU-LSPINE (2000) relabel | 4,000 jpg + csv (pixels a subset of buu_full) | 0 | — | — | — | second label vintage unused; **mislabelled "AASCE test split" in `ssn:tools/xray_dataset_usage.py`** | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 76, 426, 548; `ssn:data_platform/DATA_MANIFEST.md` §4 #31 |
| BUU-LSPINE 400 sample | 800 images, laptop only (`ctsp:BUU-LSPINE_400`) | 0 | — | — | — | orphan download, referenced by no code | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 426 |
| NHANES II annotated | 543 films (364 persons) | 543 (464 / 79 cases) | 543 | B: yes (`yolo_v2` 443 / 50 / 50) | `nhanes` 303 crops (236 films) **and** `nhanes_drr` 277 (208): both copies | used; **the double inclusion persists in the fold banks** | `ssn:docs/DATASHEET.md` §2.6; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 536, 542; `ssn:docs/MODEL_CARD.md` §3.2 |
| NHANES II unannotated | 16,531 of 17,073 TIFF | 0 | `nhanesps_fov96_ctx` 15,746 pseudo-labelled (fed deleted v5) | never offered | — | level bank: written criterion (raw decoder pseudo-labels cut anomalous accuracy by 20 points); detector: no criterion; directive D2 open | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 105, 406, Repairs 2026-09-23 |
| VinDr-SpineXR | 10,466 DICOM / 5,000 studies (SHA-256 verified) | **0** | `vindrps_fov96_ctx` / `allspine_v7` 7,625 films (43,244 crops); `vindr_fov96_ctx` 744 | B: no (0 vertebrae in `yolo_v2`-`v5f`); only `yolo_hw` (implant boxes) | **2,632 crops (2,071 films, 1,784 studies)** | lesion boxes, not levels; v8 dropped it "for comparability" (no scientific criterion); PhysioNet DUA source covered by HPR 2026-330 (29 September 2026), the supplement to determination 2026-269; release test split consumed by pseudo-labelling; directive D3 ("use all 10,466") open | `ssn:docs/DATASHEET.md` §2.6; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 63, Repairs; `sn:packet_src/statements.md` lines 25, 75 |
| AASCE / BoostNet | 579 jpg on HOME (481 labelled + 98 challenge test); full mirror 609 labelled on Ceph | 0 | `aasce_fov96_ctx` 457 (fed deleted v4/v5/v5c) | B: in the 2026-09-07 detector corpus; whether in `yolo_v3` not recorded | — | thoracic **test** set only (608 films, `ssn:slurm/thoracic_xr_eval.sh`); request-form source; D6 says use | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 98-99, 587-588; `context/xray-corner-detector-status.md` |
| Mendeley 5jdfdgp762 | 714 jpg (698 annotated) | 0 | `mendeley_fov96_ctx` 584 (fed deleted v5/v5c) | B: `yolo_v3/images/*/mendeley_*` | — | **excluded by directive**: about 500 BUU people and 13 VinDr images redistributed; 71 non-duplicate films left out with no written reason | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 101; `ssn:docs/PATIENT_IDENTITY_SPEC.md` §2-3; `context/data-directives-2026-09-23.md` |
| IEEE DataPort lateral 236 | 236 | 0 | `lat236ps_fov96_ctx` 212 (fed deleted v5) | — | — | no release labels; pseudo-label arm refuted (19 points of anomalous accuracy) | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 104 |
| Spinal-AI2024 | 20,000 (the usage tool counts 20,001) | 0 | `spinalai_drr` 8,358 renders in no bank | — | — | written criterion: machine-generated, 44 synthetic identities, levels assumed; D6 says use; the G3 split puts all on train | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 100; `ssn:docs/XRAY_DATASET_USAGE.md` |
| FluoroCap literature panels | 29,500 panels (21,603 manifest rows) | 0 | `fluorocap_fov96_ctx` 2,385 -> `allspine_v7` | detect_v6f self-training (not SchwingNet) | **2,100 crops (950 panels)** | **dropped by directive D1** (72.8 % have zero pixel residual: reproductions of published figures; no patient key); still inside the fold banks | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 23, 97; `context/fluorocap-is-reproductions-not-fluoroscopy.md` |
| cm_spine Drive file | empty directory | 0 | — | — | — | the download never landed; what it is is not recorded | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 74 |
| TVGH-SpineXR | not acquired (403 login) | — | — | — | — | access never requested | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 102 |

### 2.2 CT collections and their render banks

| dataset | on disk | level bank (v9) | other banks | detectors / device corpus | fold models | used? and why not | source (per row; carried from the reader note) |
|---|---|---|---|---|---|---|---|
| CTSpinoPelvic1K | 802 CT (0533 rebuilt 2026-09-23) | `ctsp_drr` 801 + `physics_drr` ctsp 2,430 (798 cases) + implant variants + `physics_rare` 603 (34 cases); 0533 in no trained bank | `anchor_drr` CTSP 1,602 + implant 3,036; `anchor_drr_c2`; LSTV-flag renders 9,612 | render detector `anchor_det_v1` (not SchwingNet) | `ctsp_drr` 638 crops | **used**; the release's own `splits_5fold.json` is used by nothing; `Dataset815` built, never trained | `ssn:data_platform/DATA_MANIFEST.md` sources table; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 20-22, 30, 91-93; `sn:tables/tab_corpus.md` footnote b |
| TotalSegmentator v2.0.1 | 1,228 subjects | `physics_drr` totalseg 1,831 renders over 1,121 subjects | `ts_drr` 1,170 (sweep bench, not in v9); `anchor_drr` TS 2,456 | parent of S (`anchor_none_v2_*`, TS renders) | inside `physics_drr` 5,285 crops | used through `physics_drr` only; 355 subjects never processed into `implant_ts`; 107 subjects not in physics_drr | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 67, 83, 511 |
| TotalSegmentator v3.0.0 | 1,939 dirs (1,935 distinct scans) | 0 | `ts_drr_v3` 1,735 read by nothing; `anchor_drr_c2` 3,779; rare_class TS 933 | **device corpus: 142 clean whole-spine subjects (17 val)** rendered under device poses, styled per card | — | device corpus only; Table 1 wrongly says "level bank" (§6) | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 66, 113, 511; `ssn:docs/PATIENT_IDENTITY_SPEC.md` §2 devcorpus row |
| VerSe 19/20 | 374 series / 355 subjects (10 VerSe'20 series never downloaded) | `verse_drr` 387 (13 duplicates) + `physics_drr` verse 1,463 (282 series) + `physics_rare` 879 (47 series) | `verse_soft_drr` 374 (spacing defect); `verse_drr_obl/obl2` | `anchor_drr` VerSe 748 | `verse_drr` 940 crops | **used**; no VerSe accuracy is quoted | `ssn:data_platform/DATA_MANIFEST.md` sources; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 41-45, 69-70; `sn:tables/tab_corpus.md` footnote c |
| RSNA 2022 cervical CT | 2,019 train studies in a 203 GB zip (census: 2,022 study directories) | 0 | — | — | — | **used by nothing**: never unpacked; a header census refused every study (longest 334 mm < the 350 mm a junction count needs) (§7) | §7 below; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 62, 568, 584 |
| RibFrac | 660 chest CT | 0 | — | — | — | transitional registry only (other_ct stream) | `sn:results/transitional_registry/other_ct/SUMMARY.md` |
| CTSpine1K | 1,005 volumes (782 are CTSpinoPelvic1K people) | 0 | — | — | — | transitional registry only (223 screened) | `sn:results/transitional_registry/other_ct/SUMMARY.md` |
| FluoroGen `synth_rare` | 12,929 renders (T13 86, L6 1,763) | 0 | `sd_fov96_ctx` (other FluoroGen output) | — | — | no bank and **no written reason** | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 104 |

### 2.3 Real C-arm and projection sets

| dataset | on disk | level bank (v9) | other banks | detectors / device corpus | fold models | used? and why not | source (per row; carried from the reader note) |
|---|---|---|---|---|---|---|---|
| C-ArmLSpine (Surgio-B51) | 149 cases; 299 spot frames (296 in the pre-repair bank behind every published number); 149 CBCT; 2 sweeps x 301 | 0 | `carm_fov96_ctx`, `carm_cv{k}`, `carm_drr` 240 (real frames, despite the name) | S: **held out** (test 56 frames, 28 cases); Surgio card | `carm_AP` + `carm_LAT` (fold 0: 7,869 + 7,827 by MODEL_CARD; 7,891 + 7,855 by the audit) | **the test set**: zero-shot (617 lateral vertebrae, 141 cases), cross-validation, case134 sweep (Figure S5); case39's sweep is in no root | `ssn:docs/DATASHEET.md` §2.1; `ssn:data_platform/DATA_MANIFEST.md` §4 #20, #22; `sn:results/corpus_census.md` §5, §7 |
| DeepFluoro (Cios Fusion) | 6 cadaver specimens, 366 frames (H5); vendor deposit 2,659 frames + 19 CT; HF re-host | 0 | `realxray/deepfluoro` 366 | S: train+val (238 + 24 frames, 5 specimens); test specimen 18-1109 is S's selection set; Cios card (40 of 366 frames); design-A renders under its poses, 18-1109 included | — | 2,293 vendor frames unused, no criterion written; frames entered at x4 downsample, no reason written | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 78-80; `sn:results/DATA_CONTRIBUTION.md` §6 |
| COBRA2026 Elekta XVI | 467 public Elekta cases, all fetched (692 / 692 COBRA cases, 771 GB, 2026-09-23) | 0 | `realxray/cobra_elekta` 145 cases, 3,480 frames (24 per case); derived `_v2`, `_v3`, `_ap45` | S: train+val (110 + 8 cases); test 27 cases is S's selection set; Elekta card (40 frames of 3 cases) | — | 322 Elekta cases never exported (download budget, then no rebuild); 74,142 of 77,622 projections of the attempted cases unused (24 per case, no reason); the LSTV screen of all 692 planning CTs left 91 calls unread; D4 open | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 46-48, 71; `ssn:data_platform/DATA_MANIFEST.md` cobra2026 card |
| COBRA2026 Varian OBI | 225 cases fetched | 0 | none (`cobra_varian` "NOT BUILT YET") | `varian_halcyon` card (grid only) | — | geometry map solved 2026-09-23; no frame enters a bank until an acceptance render is looked at | `ssn:tools/realxray_banks.json`; `ssn:docs/DATA_COMPLETENESS_AUDIT.md` Repairs 2026-09-23 Varian |
| Geneva hip (BV Pulsera) | 116 frames, one phantom | 0 | `realxray/geneva_hip` 116 | test only; card `bv_pulsera` (40 of 116); the unseen-device test | — | fully used, as test | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 107 |
| Ljubljana 2D-3D-GS (PIXIUM 4600) | 18 frames, one cadaver L1-L5 | 0 | none | card `pixium_4600` (14 of 18) | — | parameters only; no truth bank built (up to 90 level boxes possible) | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` line 65; `sn:results/corpus_census.md` §5 |
| SpineSAC (six C-arms, sawbones) | 5,490 of 5,492 files, 59 scenarios | 0 | none | predictions only | — | no bone truth (TotalSegmentator masks empty on the sawbone CTs; the fallback crashed); 0 frames scored; no data licence | `ssn:docs/DATA_COMPLETENESS_AUDIT.md` lines 29, 37, 594 |

Two traps in the usage table itself (`ssn:docs/XRAY_DATASET_USAGE.md`): its raw-dataset rows read "films in any bank 0"
for Mendeley and lateral-236 while its render-directory rows read 584 and 212, because the raw rows match a substring
(`mendeley`, `lateral236`) against case ids spelled `MEND_*` and `LAT236PS_*` (`ssn:tools/xray_dataset_usage.py`); trust
the render rows and `DATA_MANIFEST.md` Appendix A2. The body detector's per-version composition (`yolo_v3`, `yolo_v4z`) is
not recorded locally (`DATA_MANIFEST.md` unknown #21); the 12,709-film figure is the audit verifier's.

---

## 3. Bank composition in detail

### 3.1 `allspine_v9_fov96_ctx` (the level bank)

- Build: `ssn:slurm/allspine_v9_bank.sh` runs `tools/make_context_crops.py --drr ~/films_drr --drr ~/ctsp_drr --drr ~/verse_drr
  --drr ~/physics_drr --drr ~/physics_rare --mode fov --size 320 --tgt-px 96 --val-frac 0.15 --patient-json
  ~/patient_keys_v9.json --group-strip-suffix --skip-clipped 1 --rungs 1`. The only change from v8 is the key file
  (VerSe by subject).
- 18,565 distinct case ids (films plus renders) (`ssn:docs/XRAY_DATASET_USAGE.md`).
- Films: CSXA 4,214 / 749; BUU 3,070 / 533 (3,600 people); NHANES 464 / 79 (364 people) (`~/model_night/logs/v9bank_40415668.out`
  lines 3-11, grid only, quoted in `DATA_COMPLETENESS_AUDIT.md` line 536).
- Renders: `ctsp_drr` 801, `verse_drr` 387, `physics_drr` 7,045 anns (ctsp 2,430, totalseg 1,831, verse 1,463, implant
  1,321) (`ssn:data_platform/sources.json` card `physics_drr`, field `contents.items`; the same split is in
  `ssn:docs/DATA_COMPLETENESS_AUDIT.md` L627), `physics_rare` 1,482 anns (34 CTSP ids 603 + 47 VerSe series 879)
  (`DATA_COMPLETENESS_AUDIT.md` L628). The same `sources.json` card's location notes say 7,048 renders (ctsp 3,754,
  ts 1,831, verse 1,463, after `sn:results/corpus_census.md` §3): the 7,045-vs-7,048 gap of `RESULTS_CATALOG.md` A18.4,
  unexplained. Per-source render counts inside the v9 bank itself are not recorded locally.
- The v9 validation split is the encoder's selection split (best of 40 epochs by exact accuracy), so numbers scored on
  it are not held out (`sn:results/eval_gate/EVALUATORS.md` item 1; `EVAL_LEAKS.md` §1 item 6).

### 3.2 The C-ArmLSpine fold banks `carm_cvmix{0..4}`

- Built by `tools/merge_banks.py --base ~/allspine_v7_fov96_ctx/rung_1.npz --real ~/carm_cv{k}_fov96_ctx/rung_1.npz
  --per-class 600 --real-share 0.5` (`ssn:slurm/carmlspine_cv.sh` line 28).
- Test fold `md5(case) % 5 == k`; the audit recorded 0 test cases in any fold's DRR, crop or mixed bank
  (`ssn:docs/MODEL_CARD.md` §3.2, from `$RS/data/or_ready/audit/AUDIT.md`, grid only).
- Crops per source, fold 0 (MODEL_CARD §3.2): buu_full 635, csxa 1,758, nhanes 303, nhanes_drr 277, ctsp_drr 638,
  verse_drr 940, physics_drr 5,285, physics_rare 1,132, FLUOROCAP 2,100, VINDRPS 2,632, carm_AP 7,869, carm_LAT 7,827.
  Distinct films: buu 589, csxa 1,478, nhanes 236, nhanes_drr 208, VinDr 2,071, FluoroCap 950 (job 40416442). These
  twelve numbers sum to 31,396, not the stated 31,446; the audit's `carm_mix` numbers (AP 7,891, LAT 7,855) sum to 31,446;
  which bank each set describes is not recorded.
- The fold models quoted since 2026-09-24 (`v9init`) were "fine-tuned from allspine_v9 (the only change)" on these same
  banks (`ssn:slurm/carmlspine_cv_v9init.sh` line 67).
- `ssn:slurm/carmlspine_cv_v9.sh` (its own header calls it "A12"; the list that numbering belongs to is not recorded)
  would rebuild the base sample from `allspine_v9`; its own model paths "match nothing on disk" (`LINEAGE.md` lines
  621-632); `DATA_MANIFEST.md` A2 lists one bank `carm_cvdaymix0_v9`. **v9-base fold models do exist, as the Figure 5b
  `name_fill` cells**: `ssn:tools/indomain_name_fill.py` (docstring L26-28, record L869-873) runs "slurm/carmlspine_cv_v9.sh
  (A12) verbatim except training cases and seed", and `sn:slurm/name_fill.sh` (L25, L42) merges each cell's C-ArmLSpine
  crops onto `merge_banks --base $V9/rung_1.npz --per-class 600 --real-share 0.5`. Those banks carry no VinDr, no
  FluoroCap and one NHANES copy. 250 cells were trained (arrays 40429416, 40429901, retry 40436049), including N = all
  and both-protocol models: lateral 98.1 %, AP 97.0 % (`RESULTS_CATALOG.md` A9.4). They are scored on REP truth and per
  protocol cell, so they are not identical to the printed Table 3 (PRE truth, `v9init` fold models).

### 3.3 The device corpus and the device-held-out detectors

- `$RS/data/devcorpus`: 142 clean TotalSegmentator v3 whole spines (`~/model_night/ts_clean_subjects.txt`; 17 validation
  subjects shared by all five styled corpora) ray-cast under each device's real poses and styled by its nine fitted terms
  (`ssn:docs/DATASHEET.md` §2.7).
- Styled corpora `cios_fusion__cios_fusion`, `cios_fusion__elekta_xvi`, `cios_fusion__surgio_b51_dr`,
  `elekta_xvi__elekta_xvi`, `surgio_b51_dr__surgio_b51_dr`, each with a `__typicality` twin.
- Design A with Elekta held out: 5,408 synthetic + 896 real (`real_rep: 2`) training entries, 794 validation; design P
  (pooled): 18,906 training entries (12,730 styled + 6,176 real), 1,998 validation, 56 test specimens
  (`MODEL_CARD.md` §3.1; `context/pooled-vs-lodo-device-designs.md`).
- Real-frame banks enter only through `ssn:tools/realxray_banks.json` (roles device / derived / smoke).

---

## 4. What is not used, grouped by reason (`DATA_COMPLETENESS_AUDIT.md` legend)

| reason | items |
|---|---|
| no labels in the release | VinDr levels (lesion boxes only), NHANES unannotated films, IEEE lateral-236, AASCE challenge test 98, RSNA 2022 (fracture labels and 87 segmentations, never read) |
| excluded by Greg's directive (2026-09-23) | FluoroCap (D1), Mendeley-716 (D6, BUU redistribution) |
| data-use agreement or ethics | VinDr (PhysioNet DUA; covered by HPR 2026-330 of 29 September 2026, the supplement to 2026-269; the manuscript's `[[PENDING G0]]` token takes that number); AASCE (request form); RSNA 2022 (competition rules, non-commercial) |
| converted, never banked | `spinalai_drr` 8,358; `ts_drr_v3` 1,735; `synth_rare` 12,929; `films_ap_drr` 3,600; `nhanes_pseudo`, `lateral236_pseudo` (v5 only) |
| superseded or deleted with their bank | AASCE, Mendeley, lat236, NHANES pseudo (reached only `allspine_v4/v5/v5c`, deleted 2026-09-20); the VinDr 744 route (v3/v4) |
| budget or unfinished | COBRA Elekta 322 cases not exported and 24 frames per case; COBRA Varian 225; implant_ts 355 subjects; physics_drr VerSe 92 series; physics_rare 9 series; Ljubljana truth bank; SpineSAC truth; the second C-ArmLSpine sweep |
| no written reason | BUU AP 3,600; BUU (2000) labels; DeepFluoro vendor frames 2,293; DeepFluoro x4 downsample; `synth_rare`; NHANES films for detection |

**Greg's data directives D1-D9** (`ssn:docs/RESUME_2026-09-22_PM.md` lines 2130-2164; summary in
`context/data-directives-2026-09-23.md`) are all unticked except D7 (`[~]`). Since then: D3's count was established (0
VinDr in v8/v9) but VinDr was not added; D7's case134 and case39 frames were exported; D8 (CT 0533) was repaired; no bank
was rebuilt for D2, D4, D5 or D6 ("both are rebuilds of a bank or a training set, which G0 does not authorise",
`DATA_COMPLETENESS_AUDIT.md` Repairs). The planned flagship corpus that would use everything is `ssn:docs/FLAGSHIP_PLAN.md`
"The corpus (G4)"; `~/corpus_final/` and `sn:results/final/` appear in no file on this laptop.

---

## 5. Decisions this table puts in front of Greg

| decision | why | the options recorded | source |
|---|---|---|---|
| VinDr and FluoroCap inside the fold banks of the fine-tuned numbers | breaks D1; VinDr is covered by HPR 2026-330 (29 September 2026) | (a) print the VinDr determination, HPR 2026-330 of 29 September 2026 (the HPR tool was filled 2026-09-25; the notice came 2026-09-29); or (b) retrain the fold models without VinDr and FluoroCap, which `ssn:slurm/carmlspine_cv_v9.sh` (base sample from `allspine_v9`) would do. Option (b) has in effect been measured already: the `name_fill` cells (§3.2; `RESULTS_CATALOG.md` A9) are v9-base fold models with no VinDr or FluoroCap, N = all lateral 98.1 % and AP 97.0 % (A9.4), with the caveat that they are scored on REP truth per protocol cell, not as the printed Table 3. Greg's instruction of 2026-09-25 was to assume (a) granted and leave only the number token; settled by Greg on 2026-10-14: every dataset is permitted, its data use agreement filed, and the stronger results are quoted, while FluoroCap stays out of new training (root CLAUDE.md rule 9) | `sn:packet_src/build/BUILD_REPORT.md` decision 1; `MANUSCRIPTS.md` §2.6 |
| the supplement sentence that FluoroCap panels are "refused by the guard" | the current fold models do train on 2,100 FluoroCap crops; `main.tex` Ethics says the panels were "used for training only" | reword; both statements were true at different times (the guard post-dates the fold banks) | `working_notes/topic1_schwingnet_carm_results.md` §8 |
| "use all" directives D2-D6 | NHANES 16,531 unannotated, VinDr, all COBRA, the rest of TS v2, SpineSAC / Spinal-AI / AASCE / anchor never reached a trained bank | a rebuild authorised beyond G0 | `context/data-directives-2026-09-23.md`; `DATA_COMPLETENESS_AUDIT.md` |
| BUU AP films | 3,600 labelled AP films with no valid criterion for leaving them out | add to a bank, or write the criterion | `DATA_COMPLETENESS_AUDIT.md` lines 75, 425, 851 |
| RSNA 2022 cervical archive | 237 GB of HOME used by nothing | unpack to `$RS/data` and add a `ct_inventory.py` root for cervical / C2-anchor work, or delete; re-acquire via sbatch, never the login node; rotate the Kaggle token ("it is in the chat transcript", `ssn:docs/CONTINUANCE_2026-09-19.md` L24; also `ssn:data_platform/DATA_MANIFEST.md` L1989) | §7 |

---

## 6. Where documents disagree about data use

| claim A | claim B | trusted | why |
|---|---|---|---|
| Table 1: TotalSegmentator v2 and v3 contribute 1,170 and 1,735 renders to the "level bank" (`sn:tables/tab_corpus.md`) | the v9 bank roots exclude `ts_drr` and `ts_drr_v3`; TS reaches the bank only as 1,831 `physics_drr` renders; `ts_drr_v3` is read by nothing | B | the build script is what ran |
| the device corpus is "TotalSegmentator v2" (`MODEL_CARD.md` §3.1; `DATASHEET.md` §2.7) | v3: the manifest root is `TotalSegmentator_v3/...v300` (`ssn:docs/RSNAI_DATA_MANIFEST.json`); `PATIENT_IDENTITY_SPEC.md` §2; audit line 113 | B | path and two independent documents |
| "the clean rebuild has not landed" (`MODEL_CARD.md` §3.3; `DATASHEET.md` §4) | v8 and v9 exist and are trained | B | A was written 2026-09-22, before the rebuild |
| the C-ArmLSpine encoder was "initialised from the v7 bank" (`context/no-unexplained-subsets-fix-not-disclose.md`) | initialised from `allspine_v2_r1` (`MODEL_CARD.md` §1.2; `ssn:slurm/carmlspine_cv.sh` line 21) | both, read correctly | init = `allspine_v2_r1` (v9 for the v9init folds); the base crops of the fold bank come from `allspine_v7` |
| `XRAY_DATASET_USAGE.md` "AASCE test split, 4,000, report spreadsheet only" | it is the BUU-LSPINE (2000) release (pixel identity with buu_full) | B | `DATA_COMPLETENESS_AUDIT.md` lines 76, 548 |
| `CT_INVENTORY.md`: `physics_drr` = CTSP, 3,029 subjects; `physics_rare` = CTSP, 81; `carm_drr` = CBCT renders | `physics_drr` mixes ctsp / totalseg / verse / implant; `physics_rare` = 34 CTSP + 47 VerSe; `carm_drr` holds real frames | B | the inventory labels banks by name, not contents |
| `tools/realxray_banks.json`: Varian "geometry not solved" | map solved 2026-09-23, acceptance render pending | B | the JSON note predates the repair |
| `DATA_MANIFEST.md` line 14766: `cobra_elekta_v3` and `cobra_elekta_g3test` are in `tools/realxray_banks.json` | the local `tools/realxray_banks.json` (commit 180fb0f) has neither | unresolved | the grid copy may be newer |
| body detector in use: `detector_v5z_final` (atlas, manuscript) | `detect_v5z_epoch25` shipped in `~/level_id_service` | both true | different products carry different checkpoints |

---

## 7. The RSNA 2022 cervical-spine fracture CT archive

| item | fact | source |
|---|---|---|
| what | Kaggle `rsna-2022-cervical-spine-fracture-detection`; dataset paper doi 10.1148/ryai.230034; 3,112 CT scans collected, 2,019 in the Kaggle train split; per-level fracture labels C1-C7 in `train.csv`; 87 segmentations | `DATA_COMPLETENESS_AUDIT.md` line 568; `ssn:docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 15 |
| terms | login and acceptance of competition rules; "non-commercial research and education only" | same line 15 |
| why fetched | planned unzip, DICOM -> NIfTI, SPINEPS, renders for C2 sweeps; "the only large source where a C1 vs C2 vs C7 label is voxel-anchored" | `ssn:docs/CONTINUANCE_2026-09-19.md`; `PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` line 397 |
| how fetched | `MODE=download nohup bash slurm/rsna_cspine_fetch.sh > ~/data/rsna_cspine/fetch.log` (Kaggle CLI, token from `~/.fluorocap/credentials.env`, not read), **on the login node** (now forbidden), 2026-09-19, rc 0 | `ssn:slurm/rsna_cspine_fetch.sh`; `DATA_MANIFEST.md` card `rsna_2022_cspine` |
| on disk | `~/data/rsna_cspine/`: zip 203,318,086,447 B (189 GiB), one `.nii.zip`, `sample_submission.csv`, `fetch.log`; never unpacked; 236.8 GB of HOME (what besides the zip makes up the difference is not recorded) | `DATA_COMPLETENESS_AUDIT.md` lines 62, 584 |
| header census | `sbatch ... slurm/other_ct_fetch.sh rsna` -> `tools/other_ct_fetch.py rsna --zip ... --out $RS/data/anomaly_harvest/other_ct/rsna`: slice count and image positions read from the zip; `rsna_headers.jsonl` (grid); prints `RSNA_CENSUS_DONE` | `ssn:tools/other_ct_fetch.py` lines 13-21, 200-241 |
| census result | 2,022 study directories (likely including test-image studies; not recorded); longest craniocaudal extent 334 mm, below the 350 mm a scan from the skull base needs to reach the thoracolumbar junction; all refused; `no_count` in the registry | `sn:results/transitional_registry/other_ct/SUMMARY.md` lines 30, 36, 112 |
| code vs docstring | the docstring promises that a long-enough study "is extracted and converted"; `cmd_rsna` only writes headers (no study qualified, so nothing was lost) | `tools/other_ct_fetch.py` lines 13-16 vs 200-241 |
| used by | nothing | `DATA_COMPLETENESS_AUDIT.md` lines 62, 597 |
| what was never tried | a cervical use (C1-C7 level renders, a C2 anchor); the 350 mm rule refuses the archive only for junction counting | topic 3 §14 |
| IRB | whether HPR 2026-269 covers it (competition rules, not a DUA) is not recorded | `sn:packet_src/statements.md` lines 25, 57 |

Other RSNA items: the Radiology: Artificial Intelligence manuscripts (`MANUSCRIPTS.md`); RSNA 2024 Lumbar Spine
Degenerative Classification (MRI) downloaded by `Desktop/lstv-detector/slurm_scripts/00_download_data.sh` for an earlier
MRI project (last commit 2026-06-13), kept out of the CT table (`ssn:docs/ruleclass/CLASSIFIERS.md` R37); no SchwingNet
bank uses it.

---

## 8. How to regenerate the usage numbers

| what | command | output |
|---|---|---|
| X-ray usage table | `python tools/xray_dataset_usage.py --out ~/model_night/XRAY_DATASET_USAGE.md` (in a job; reads every `~/*/rung_1.npz`) | `.md` + `.json`, copied to `ssn:docs/` |
| NHANES and VinDr per-image manifests | `ssn:slurm/film_corpus_inventory.sh` (job 40416535) -> `tools/film_corpus_inventory.py` | `$RS/data/inventory/films/` incl. `nhanes_film_manifest.csv`, `FILM_CORPUS_INVENTORY.md` |
| per-bank film counts from case arrays | `tools/audit_film_corpora.py` (job 40416442) | `$RS/tmp/film_corpora_audit.json` (grid) |
| CT render subjects | `python tools/ct_inventory.py --out docs/CT_INVENTORY.md --json docs/CT_INVENTORY.json` | `ssn:docs/CT_INVENTORY.md` |
| persons and images per source on the G3 split | `python SchwingNet/tools/corpus_census.py` | `sn:results/corpus_census.md` |
| real-frame training lists, derived-bank duplicates | `sbatch ssn:slurm/audit_realxray_lists.sh` (the job runs `tools/test_realxray_banks.py` and `tools/audit_realxray_lists.py --out $RS/tmp/realxray_lists_audit.json`; a bare `python tools/audit_realxray_lists.py` fails because `--out` is required) | `$RS/tmp/realxray_lists_audit.json`, copied to `sn:results/realxray_lists_audit.json` |
| the data side as a whole | `ssn:data_platform/` (`DATA_MANIFEST.md` §1; `MIGRATION_PLAN.md` §0) | `sources.json`, `db/` index |

Fix before the next run: rename `buu_2000` in `tools/xray_dataset_usage.py` `RAW`; key raw datasets by
`tools/patient_keys.py` rather than substrings; update the HOME paths after the Ceph migration (`DATA_MANIFEST.md`
Appendix B item 3; person keys depend on the path fragments `"/vindr"`, `"lateral236"`, `"/raw/lateral_236/"` in
`tools/patient_keys.py` lines 210-212).
