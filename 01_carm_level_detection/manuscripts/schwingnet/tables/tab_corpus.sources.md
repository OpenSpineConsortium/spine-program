# Sources for every cell of Table 1 (`tab_corpus.tex` / `tab_corpus.md`)

Re-derived 2026-09-23 against the data-completeness audit. Files (repo-relative; `#` marks a JSON path):

- **INV** `docs/CT_INVENTORY.md` — table "Render banks" (bank / collection / renders / distinct subjects / truth).
- **PIS** `docs/PATIENT_IDENTITY_SPEC.md` — §2 table (identity unit, n cases, n persons after keying), §4 "What remains unknown".
- **MC** `docs/MODEL_CARD.md` — §3.1 detector training data, §3.2 the per-fold mixed bank (crop counts and the distinct films behind them, job 40416442), §4.1 test sets.
- **DS** `docs/DATASHEET.md` — §2.1 real device corpora, §2.3 labels, §2.6 plain-film corpora ("in the level bank (v8/v9)" column; the VinDr "one number per object" table), §2.7 synthetic device corpus, §3 Sampling.
- **AUD** `docs/DATA_COMPLETENESS_AUDIT.md` — the "Every gap" table (rows 34, 46, 77, 90), the release/on-disk/used ledgers (lines 444–447 COBRA, 525–532 NHANES, 704–719 C-ArmLSpine) and the Repairs section "C-ArmLSpine: case134 not built, case39's third frame dropped, case118's oblique called a lateral (2026-09-23)".
- **CC** `SchwingNet/CLAIM_CHECKLIST.md` row 20 (real-frame split sizes read from `/rs/.../or_ready/audit/AUDIT.md` (a)).
- **DEV** `docs/devices/{cios_fusion,elekta_xvi,bv_pulsera,pixium_4600}.json` — `fit.n_frames_fit`, `fit.n_frames_total`, `physics_terms.held_out_r2_median`, `physics_terms.baseline_r2_median`.
- **NUM** `SchwingNet/NUMBERS.md` "Counts in Methods" (COBRA Varian recount, C-ArmLSpine day groups).
- **PLAN** `docs/FLAGSHIP_PLAN.md` (the corpus table: what the released corpus takes; FluoroCap dropped; weights and corpus at G7).

Column "Released from it" is qualitative (corpus / parameters / weights) and is defined in footnote k; the only numbers in it are the device-card fit counts and medians (DEV).

## Row: CTSpinoPelvic1K

| cell | value | file → field |
|---|---|---|
| modality | abdominopelvic CT | INV `ctsp_drr` field of view "abdominopelvic FOV" |
| role | level bank | MC §3.2 fold bank `ctsp_drr 638`, `physics_drr`, `physics_rare`; a5.json per_source `ctsp_drr` |
| subjects | 801 patients of 802 records (TCIA patient identifier) | PIS §2 ctsp: n persons after keying **801**, identity unit "one TCIA PatientID" |
| frames/renders | 801 renders | INV `ctsp_drr` renders 801 |
| truth | release labels per level, ribs and pelvis | INV `ctsp_drr` truth |
| released | corpus; level weights | PLAN corpus table row "CTSpinoPelvic1K 802 … rendered CTs: level bank"; MC §3.2 (the fold models train on `ctsp_drr`) |
| footnote b | 0533 truncated, in no trained bank; rebuilt and replaced in the release (802 in the released corpus) | PIS §2 ctsp; DS §2.5; `results/repairs/ct0533_CHECK.md` (jobs 40416624 swapped=1 count=802; 40416626 ctsp_drr=802); `results/corpus_census.json#summary` ctsp persons 802, ctsp_drr items 802 (2026-09-24 fill pass) |

## Row: TotalSegmentator v2 and v3

| cell | value | file → field |
|---|---|---|
| modality | whole-body CT | INV `ts_drr` / `ts_drr_v3` "whole body" |
| role | level bank; styled corpus (142 subjects, 17 validation, i.e. checkpoint selection; EVALUATORS.md 1.4: the 17 are the selection subjects of every dc_* arm, not held out) | MC §3.2 `physics_drr`; MC §3.1 and DS §2.7 (142 clean subjects, the same 17 validation subjects) |
| subjects | 1,935 scans (CT scan) | PIS §2 ts: n persons after keying **1,935** distinct scans; "No patient identifier exists" |
| frames/renders | 1,170 (v2) and 1,735 (v3) renders | INV `ts_drr` 1170, `ts_drr_v3` 1735 |
| truth | labels mapped by name | INV `ts_drr` truth |
| released | corpus; level weights | PLAN corpus table; MC §3.2 |
| footnote c | 24 renumbered pairs, three duplicate groups | PIS §2 ts rule, PIS §4 |

## Row: VerSe 19/20

| cell | value | file → field |
|---|---|---|
| modality | spine CT | INV `verse_drr` "whole spine"; PIS §2 verse |
| role | level bank; no accuracy quoted | MC §3.2 `verse_drr 940`; NUMBERS.md "Numbers deliberately absent" (v8 keyed series as subjects) |
| subjects | 355 subjects, 374 series (subject) | PIS §2 verse "374 series belong to 355 subjects" |
| frames/renders | 387 renders; 374 soft-tissue renders | INV `verse_drr` 387, `verse_soft_drr` 374 |
| truth | VerSe masks C1–L6; published transitional table | INV `verse_drr` truth; `results/rare_class/transitional_subtypes.md` (Löffler 2021 supplementary table as the VerSe subtype source) |
| released | corpus; level weights | PLAN corpus table; MC §3.2 |

## Row: CSXA

| cell | value | file → field |
|---|---|---|
| modality | cervical lateral | DS §2.6 "CSXA cervical, lateral" |
| role | level bank; validation | MC §3.2 `csxa 1758`; a5.json per_protocol random csxa (validation) |
| subjects | 4,963 individuals (individual) | PIS §2 csxa n persons **4,963** |
| films | 4,963 films | DS §2.6 "in the level bank (v8/v9) 4,963" |
| truth | per-vertebra levels, released | DS §2.6 |
| released | corpus; level weights | PLAN corpus table ("CSXA … level bank + validation"); MC §3.2 |

## Row: BUU-LSPINE

| cell | value | file → field |
|---|---|---|
| modality | lumbar AP and lateral | DS §2.6 "AP + lateral" |
| role | level bank; validation | MC §3.2 `buu_full 635`; a5.json buu_full |
| subjects | 3,600 cases (case number) | PIS §2 buu n persons **3,600** by the released table |
| films | 3,603 lateral films; the 3,600 AP films are in no bank | DS §2.6 BUU row: on disk 7,204, in the level bank **3,603**; `results/JOBS_data_repairs.txt` "BUU AP films into the level bank (bank rebuild …) — not launched" |
| truth | end-plate lines L1–S1; levels by position | DS §2.6 |
| released | corpus; level weights | PLAN corpus table ("BUU 3,600×2"); MC §3.2 |
| footnote d | 3,598 by content; the built split merges the two pairs | PIS §2 buu; `results/corpus_census.json#summary` buu persons 3,598 (group_of buu:0629->0449, buu:0719->0140) (2026-09-24 fill pass) |

## Row: NHANES II

| cell | value | file → field |
|---|---|---|
| modality | lateral survey film | DS §2.6 "digitised national survey film corpus" |
| role | level bank; validation | MC §3.2 `nhanes 303, nhanes_drr 277`; a5.json nhanes |
| subjects | 364 persons among the annotated (sample person) | PIS §2 nhanes n persons **364**; DS §2.6 "364 persons" |
| films | 543 annotated films (542 on disk) of 17,075 release entries | DS §2.6 NHANES row: "17,073 of 17,075" on disk, in the level bank **542**, "543 films have landmarks … L00452 exists only inside the Zenodo pickle"; AUD line 525 (release 17,075 = 9,667 cervical + 7,408 lumbar) and 532; `results/JOBS_data_repairs.txt` job 40416535 marker `nhanes_rows=17075 nhanes_on_disk=17073 nhanes_annotated=543` |
| truth | landmarks, released | DS §2.6 |
| released | corpus; level weights | PLAN corpus table ("NHANES II ~17,000 films (543 annotated) … ALL"); MC §3.2 |
| footnote e | two entries served empty at source | DS §2.6 "NHANES II, the two entries that are not on disk" (L00452, L00456; HEAD+GET jobs 40416367, 40416535) |

## Row: VinDr-SpineXR

| cell | value | file → field |
|---|---|---|
| modality | AP and lateral | DS §2.6 |
| role | intraoperative fold banks only, training, pseudo-labelled | MC §3.2 fold bank `VINDRPS 2632` crops = **2,071** distinct films (job 40416442); DS §2.6 VinDr table "carm_mix and the C-ArmLSpine fold banks: 2,071 films (2,632 crops)" and "allspine_v8, allspine_v9 — the level bank the model was trained on: 0" |
| subjects | 5,000 studies (study) | PIS §2 vindr "10,466 images → 5,000 studies"; DS §2.6 "10,466 images / 5,000 studies" |
| films | 2,071 films as 2,632 crops, of 10,466 released images | DS §2.6 VinDr table (same rows) |
| truth | lesion boxes released; levels pseudo-labelled | DS §2.6 |
| released | corpus (all 10,466 images) | PLAN corpus table ("VinDr 10,466 … ALL"); AUD directive D3 (use all 10,466) |
| footnote f | fold banks vs the film bank; 31,400 crops per fold | MC §3.2 ("the twelve sum to the bank's 31,446 crops"); DS §2.6 |

## Row: FluoroCap

| cell | value | file → field |
|---|---|---|
| modality | literature fluoroscopy panels | INV `fluorocap_drr`; DS §2.5 |
| role | intraoperative fold banks only, training; dropped from the release | MC §3.2 `FLUOROCAP 2100` crops = **950** distinct panels (job 40416442); DS §2.6 "FluoroCap is train-only"; PLAN corpus table "FluoroCap dropped from training (PI decision)" |
| subjects | not established (source article or video) | PIS §2 / §4 fluorocap |
| panels | 950 panels as 2,100 crops, of 29,484 harvested | MC §3.2 (950 / 2,100); DS §2.5 "29,484 panels (audit count)" |
| truth | none released | INV `fluorocap_drr` truth "none" |
| released | none | PLAN corpus table ("0 in training"; reproductions, never redistributed — atlas/dataset.json License) |
| footnote g | document key over-merges | PIS §4 fluorocap |

## Row: C-ArmLSpine

| cell | value | file → field |
|---|---|---|
| modality | mobile C-arm, Surgio-B51; per-case CBCT | DS §2.1 C-ArmLSpine |
| role | naming cross-validation; held-out detector test | MC §4.1 "C-ArmLSpine five-fold CV", "C-ArmLSpine fixed test"; a1.json arm `lodo_carm` (C-ArmLSpine never seen) |
| subjects | not established: 149 released cases, 148 scored (case, one acquisition session) | PIS §2 carmlspine "persons ≤149, unknown"; AUD Repairs "The release is 149 complete cases"; CC "149 cases released → 148 built" |
| frames | 296 frames scored: 210 / 30 / 56 (105 / 15 / 28 cases) | CC row 20; `results/realxray_lists_audit.json#banks/carmlspine/images` (210 / 30 / 56) and `#cases` (105 / 15 / 28) |
| frames, released | 299 spot exposures and two 301-projection cone-beam sweeps | AUD line 704 (`catalogue.json`: folders C-arm 297, ori 302; frame_headers 147×2, case39×3, case134 in CBCT/) and Repairs "Expected: 299 spot frames over 149 cases (297 in C-arm/ + case134's 2 in CBCT/) = 149 AP + 149 LAT + 1 OBL"; AUD line 729 (two sweeps are 2 × 301) |
| truth | CBCT, two automatic labellers, agreed levels; pose by registration | DS §2.3, §3 |
| released | corpus; level weights (fold models); no detector weight | PLAN corpus table ("C-ArmLSpine 149 … ALL"); MC §3.2 (`carm_AP 7869, carm_LAT 7827` crops in every fold bank); MC §3.1 / a1.json (the reported detector never saw it) |
| footnote h | case134 missed by the walker; case39 repeat lateral; case118 oblique scored as lateral; five dates | AUD Repairs section (quoted above); AUD row 77 (case39); `results/carmlspine_day_groups.json` study_dates (five dates) |

## Row: DeepFluoro

| cell | value | file → field |
|---|---|---|
| modality | mobile C-arm, Cios Fusion; cadaver CT | DS §2.1 |
| role | detector training; device parameters | MC §3.1; a1.json arm (COBRA Elekta + DeepFluoro real frames) |
| subjects | 6 specimens (specimen; 4 / 1 / 1) | PIS §2 deepfluoro; CC row 20 |
| frames | 366 frames: 238 / 24 / 104 | CC row 20; `results/realxray_lists_audit.json#banks/deepfluoro/images` |
| truth | CT and C-arm pose per frame | DS §2.1 |
| released | corpus; parameters (40 of 366 frames; R² 0.905 vs 0.899); detector weights | DEV `cios_fusion.json` fit.n_frames_fit 40 / n_frames_total 366, held_out_r2_median 0.9049, baseline 0.8994; a1.json arm |

## Row: COBRA2026, Elekta XVI

| cell | value | file → field |
|---|---|---|
| modality | radiotherapy kV imager; planning CT | DS §2.1 |
| role | detector training; device parameters | MC §3.1; a1.json arm |
| subjects | 145 patients of 467 public Elekta cases (case, one per patient; 110 / 8 / 27) | PIS §2 cobra (145; one case = one patient); DS §3 Sampling ("A 120, B 107, C 120, D 120, F 92, G 133 = 692"; 467 = A–D); CC row 20 (110/8/27) |
| frames | 3,480 frames: 2,640 / 192 / 648 | CC row 20; `results/realxray_lists_audit.json#banks/cobra_elekta/images` |
| truth | planning CT, deformably registered; RTK geometry | DS §2.1 |
| released | corpus (all 692 cases, fetching); parameters (40 of 335; R² 0.974 vs 0.964); detector weights | PLAN corpus table ("COBRA2026 692 cases … ALL"); `results/JOBS_cobra.txt` (full fetch); DEV `elekta_xvi.json` fit 40 / 335, r2 0.9744 / 0.9637; a1.json arm |
| footnote i | 692 = 467 + 225; 152 fetched, 145 kept, B000; 26 Varian | DS §3 Sampling; NUM "COBRA2026 692 public → 152 downloaded → 145 kept (B000 dropped)" and the Varian recount (26: F 14, G 12); DS §3 reading traps (B000: 41 frames the CT never covers) |

## Row: Geneva hip

| cell | value | file → field |
|---|---|---|
| modality | mobile C-arm, BV Pulsera; phantom CT | DS §2.1 |
| role | unseen device, test only; device parameters | MC §4.1; `results/repairs/cobra-dup-leak_CHECK.md` defect A (116 test frames, in no arm's train list) |
| subjects | 1 phantom (none: one object) | PIS §2 geneva_hip |
| frames | 116 frames, all test | CC row 20; MC §4.1 |
| truth | CT and gold-standard pose | DS §2.1 |
| released | corpus; parameters (40 of 116; R² 0.952 vs 0.917) | DEV `bv_pulsera.json` fit 40 / 116, r2 0.9524 / 0.9172; PLAN corpus table ("Geneva 116 … ALL") |

## Row: Ljubljana 2D-3D-GS

| cell | value | file → field |
|---|---|---|
| modality | turntable flat panel, PIXIUM 4600; cadaver CT | DS §2.1 |
| role | device parameters only | DS §2.7; absent from every training list in MC §3 |
| subjects | 1 specimen (not split) | PIS §2 ljubljana |
| frames | 18 frames | DS §2.1 |
| truth | CT and gold-standard pose | DS §2.1 |
| released | parameters (14 of 18; R² 0.679 vs 0.650); no frame | DEV `pixium_4600.json` fit 14 / 18, r2 0.6785 / 0.6496; licence CC BY-NC-ND (atlas/dataset.json License) so no frame is redistributed |

## Totals row (footnote j)

| total | arithmetic | file |
|---|---|---|
| 4,093 renders | 801 + 1,170 + 1,735 + 387 | INV render banks |
| 9,108 films in the level bank | 4,963 + 3,603 + 542 | DS §2.6 "in the level bank (v8/v9)" column (CSXA 4,963; BUU 3,603; NHANES 542) |
| fold banks alone | 2,071 VinDr films; 950 FluoroCap panels | MC §3.2 (job 40416442 distinct films) |
| 4,276 real frames scored | 296 + 366 + 3,480 + 116 + 18 | CC row 20; DS §2.1; `results/realxray_lists_audit.json` |
| of which C-arm 778 | 296 + 366 + 116 | the rows whose modality reads "mobile C-arm" |

## Footnote k (used by no trained component)

| collection | value | file |
|---|---|---|
| SpinalAI | 8,358 machine-generated renders | INV `spinalai_drr`; DS §2.6 |
| AASCE | 457 renders | INV `aasce_drr` |
| anchor-crop | 7,842 renders | INV `anchor_drr` |
| SpineSAC | sawbone-phantom frames | DS §2.1 |
| Mendeley-716 | redistribution of BUU-LSPINE | PIS §2 mendeley; DS §2.6 |
| corpus and weights at G7 | — | PLAN "The deliverables (G7)" |
