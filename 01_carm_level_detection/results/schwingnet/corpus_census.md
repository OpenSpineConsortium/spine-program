# G4 corpus census: persons, images and transitional persons per source

Computed 2026-09-24 20:32 by `tools/corpus_census.py`. Every number is read from a file named here; the only typed numbers are the printed cells of Table 1 and Table 2, copied in to be compared against.

## Inputs

| input | file | stamp |
|---|---|---|
| SPLIT | `~/split_final.json (grid)` (sha256 65a57eb0c7a6) | generated 2026-09-23 20:18:48, seed 0, leak audit PASS; 29,514 person keys, 82 roots |
| REG | `results/transitional_registry/registry.csv` (sha256 f331c7897be6) | 2026-09-24 11:07 |
| SUB | `results/rare_class/transitional_subtypes.csv` (sha256 ec5fc0d2d601) | 2026-09-23 18:54 |
| FLAGS | `results/polypose/inputs/lstv_flag_labels_v2.csv` (sha256 e939da769bf8) | |
| KEYS | `spinesurg-ct-nnunet:tools\patient_keys.py` | fallback attribution of mixed-root items |

Persons: `side_of_person` of SPLIT by key prefix (the person key after the split's alias folds). Images: `item_side` of SPLIT per root; a source's **primary** roots count each object once (Table 1's unit); *all roots* also counts re-renders, re-windows, copies and subsets and is not additive. Sides: train / val / test; `hold` = COBRA cases the screen has not called; `excluded` = FluoroCap and Mendeley items.

## 0. The census in one table

Persons and primary images per source (train / val / test), transitional persons of the Table 2 subtype table (with its test-side count) and of the registry over every truth tier.

| source | persons (unit) | train / val / test | images, primary (kind: total, train / val / test) | transitional persons, subtype table (test) | registry, all tiers |
|---|---|---|---|---|---|
| ctsp | 802 (release record (TCIA patient)) | 636 / 73 / 93 | renders: 802 (636 / 73 / 93) | L6 18 (7), sacralised_L5_five_lumbar 3 (1), sacralised_L5_four_lumbar 9 (4), castellvi_I_II 4 (2), lumbar_rib 14 (6), unassigned 4 (2) | L6 29, sacralised_L5_five_lumbar 3, sacralised_L5_four_lumbar 9, castellvi_I_II 4, lumbar_rib 14, unassigned 5 |
| ts | 1,867 (folded scan group (no patient id)) | 1,469 / 193 / 205 | renders: 2,905 (2,248 / 318 / 339) | L6 3 (2), T13 1 (1) | L6 22, T13 4, unassigned 26 |
| verse | 355 (subject) | 252 / 35 / 68 | renders: 761 (547 / 76 / 138) | L6 86 (34), sacralised_L5_five_lumbar 13 (5), sacralised_L5_four_lumbar 3 (1), castellvi_I_II 27 (10), T13 6 (2) | L6 85, T13 6, sacralised_L5_five_lumbar 13, castellvi_I_II 27, lumbar_rib 12, unassigned 23 |
| csxa | 4,963 (individual) | 3,979 / 485 / 499 | radiographs: 4,963 (3,979 / 485 / 499) | - | - |
| buu | 3,598 (case (two byte-identical pairs merged)) | 2,926 / 331 / 341 | radiographs: 7,203 (5,859 / 662 / 682) | - | - |
| nhanes | 9,581 (sample person) | 7,673 / 969 / 939 | radiographs: 16,272 (13,010 / 1,672 / 1,590) | - | - |
| vindr | 4,981 (study) | 4,019 / 475 / 487 | radiographs: 10,274 (8,259 / 977 / 1,038) | - | - |
| fluorocap | 1,953 (source document (excluded)) | 0 / 0 / 0 (excluded 1,953) | literature panels: 2,385 (0 / 0 / 0 (excluded 2,385)) | - | - |
| carmlspine | 149 (case (acquisition session)) | 123 / 13 / 13 | real frames: 299 (247 / 26 / 26); cone-beam sweep projections: 301 (0 / 301 / 0) | L6 3 (3) | L6 3, unassigned 1 |
| deepfluoro | 6 (specimen) | 4 / 1 / 1 | real frames: 366 (231 / 111 / 24) | - | - |
| cobra | 692 (case (patient)) | 445 / 71 / 159 (hold 17) | real frames: 3,480 (2,232 / 240 / 840 (hold 168)) | - | L6 3, unassigned 6 |
| geneva | 19 (camera view of one phantom) | 0 / 0 / 19 | real frames: 116 (0 / 0 / 116) | - | - |
| ljubljana | 0 (not in the split) | 0 / 0 / 0 | none in the split | - | - |
| aasce | 217 (film index group) | 178 / 14 / 25 | radiographs: 440 (366 / 23 / 51) | - | - |
| spinalai | 44 (similarity group (no person)) | 44 / 0 / 0 | machine-generated films: 8,358 (8,358 / 0 / 0) | - | - |
| lat236 | 236 (film) | 193 / 22 / 21 | radiographs: 236 (193 / 22 / 21) | - | - |
| mendeley | 51 (excluded key) | 0 / 0 / 0 (excluded 51) | radiographs: 584 (0 / 0 / 0 (excluded 584)) | - | - |

## 1. Distinct persons per source, by split side

| source | Table 1 row | unit in the split | train / val / test | total | Table 1 |
|---|---|---|---|---|---|
| ctsp | CTSpinoPelvic1K | ctsp | 636 / 73 / 93 | 802 | 801 patients of 802 records |
| ts | TotalSegmentator v2 and v3 | ts | 1,469 / 193 / 205 | 1,867 | 1,935 scans |
| verse | VerSe 19/20 | verse | 252 / 35 / 68 | 355 | 355 subjects, 374 series |
| csxa | CSXA | csxa | 3,979 / 485 / 499 | 4,963 | 4,963 individuals |
| buu | BUU-LSPINE | buu | 2,926 / 331 / 341 | 3,598 | 3,600 cases |
| nhanes | NHANES II | nhanes | 7,673 / 969 / 939 | 9,581 | 364 persons among the annotated |
| vindr | VinDr-SpineXR | vindr | 4,019 / 475 / 487 | 4,981 | 5,000 studies |
| fluorocap | FluoroCap | fluorocap, fluorocap_video | 0 / 0 / 0 (excluded 1,953) | 1,953 | not established |
| carmlspine | C-ArmLSpine | carmlspine | 123 / 13 / 13 | 149 | not established; 149 released cases, 148 scored |
| deepfluoro | DeepFluoro | deepfluoro | 4 / 1 / 1 | 6 | 6 specimens (4 / 1 / 1) |
| cobra | COBRA2026, Elekta XVI | cobra | 445 / 71 / 159 (hold 17) | 692 | 145 patients of 467 public Elekta cases (110 / 8 / 27) |
| geneva | Geneva hip | geneva | 0 / 0 / 19 | 19 | 1 phantom |
| ljubljana | Ljubljana 2D-3D-GS | not in the split | - | 0 | 1 specimen (not split) |
| aasce | AASCE (not a Table 1 row) | aasce | 178 / 14 / 25 | 217 | no row |
| spinalai | Spinal-AI2024 (not a Table 1 row; machine-generated) | spinalai | 44 / 0 / 0 | 44 | no row |
| lat236 | lateral236 pseudo-labelled films (not a Table 1 row) | lat236 | 193 / 22 / 21 | 236 | no row |
| mendeley | Mendeley-716 (excluded: redistribution of BUU) | mendeley | 0 / 0 / 0 (excluded 51) | 51 | no row |

NHANES II persons behind the 543 annotated films: **364** ({'train': 294, 'test': 34, 'val': 36}). VinDr studies with an item: **4981** ({'train': 4019, 'val': 475, 'test': 487}). COBRA cases with a frame: **145** ({'test': 35, 'train': 93, 'val': 10, 'hold': 7}). C-ArmLSpine cases with a spot frame: **149** ({'train': 123, 'test': 13, 'val': 13}; views {'AP': 149, 'LAT': 149, 'OBL': 1}). ctsp:0533 side: test. Geneva keys: 19 views of one phantom.

## 2. Images per source: real frames, radiographs and renders, by split side

Primary roots only (one object once); every root is listed in section 3.

| source | kind | primary roots | train / val / test | total | Table 1 |
|---|---|---|---|---|---|
| ctsp | renders | `~/ctsp_drr` | 636 / 73 / 93 | 802 | 801 renders |
| ts | renders | `~/ts_drr`, `~/ts_drr_v3` | 2,248 / 318 / 339 | 2,905 | 1,170 (v2) and 1,735 (v3) renders |
| verse | renders | `~/verse_drr`, `~/verse_soft_drr` | 547 / 76 / 138 | 761 | 387 renders; 374 soft-tissue renders |
| csxa | radiographs | `~/films_drr` | 3,979 / 485 / 499 | 4,963 | 4,963 films |
| buu | radiographs | `~/films_ap_drr`, `~/films_drr` | 5,859 / 662 / 682 | 7,203 | 3,603 lateral films; the 3,600 AP films in no bank |
| nhanes | radiographs | `~/films_drr`, `~/nhanes_pseudo` (distinct by person and view: 543 annotated + 16234 pseudo-labelled, 505 in both) | 13,010 / 1,672 / 1,590 | 16,272 | 543 annotated films (542 on disk) of 17,075 |
| vindr | radiographs | `~/vindr_pseudo` | 8,259 / 977 / 1,038 | 10,274 | 2,071 films as 2,632 crops, of 10,466 released images |
| fluorocap | literature panels | `~/fluorocap_drr` | 0 / 0 / 0 (excluded 2,385) | 2,385 | 950 panels as 2,100 crops, of 29,484 harvested |
| carmlspine | real frames | `$RS/realxray/carmlspine` | 247 / 26 / 26 | 299 | 296 scored: 210 / 30 / 56 (105 / 15 / 28 cases); released 299 spot exposures, two cone-beam sweeps |
|  | renders | none primary (396 over 1 secondary roots) | 0 / 0 / 396 | 396 |  |
| deepfluoro | real frames | `$RS/realxray/deepfluoro` | 231 / 111 / 24 | 366 | 366 frames: 238 / 24 / 104 |
| cobra | real frames | `$RS/realxray/cobra_elekta` | 2,232 / 240 / 840 (hold 168) | 3,480 | 3,480 frames: 2,640 / 192 / 648 |
| geneva | real frames | `$RS/realxray/geneva_hip` | 0 / 0 / 116 | 116 | 116 frames, all test |
| ljubljana | - | none in the split | - | 0 | 18 frames |
| aasce | radiographs | `~/aasce_drr` | 366 / 23 / 51 | 440 | no row |
| spinalai | machine-generated films | `~/spinalai_drr` | 8,358 / 0 / 0 | 8,358 | no row |
| lat236 | radiographs | `~/lateral236_pseudo` | 193 / 22 / 21 | 236 | no row |
| mendeley | radiographs | `~/mendeley_drr` | 0 / 0 / 0 (excluded 584) | 584 | no row |

DeepFluoro frames per specimen and side: {'17-1882': {'val': 111}, '17-1905': {'test': 24}, '18-0725': {'train': 24}, '18-1109': {'train': 104}, '18-2799': {'train': 48}, '18-2800': {'train': 55}}. C-ArmLSpine sweep (301 projections of case134) side: val.

## 3. Every root of the split, with its items attributed to a source

| root | kind | primary | n | by side | by source |
|---|---|---|---|---|---|
| `$RS/realxray/pelvis_landmarks/cobra_elekta` | derived |  | 3,120 | 2,064 / 168 / 720 (hold 168) | cobra 3,120 |
| `$RS/realxray/pelvis_landmarks/deepfluoro` | derived |  | 342 | 231 / 111 / 0 | deepfluoro 342 |
| `$RS/realxray/pelvis_landmarks/geneva_hip` | derived |  | 116 | 0 / 0 / 116 | geneva 116 |
| `~/carm_cv0_drr` | derived |  | 226 | 180 / 20 / 26 | carmlspine 226 |
| `~/carm_cv1_drr` | derived |  | 246 | 206 / 18 / 22 | carmlspine 246 |
| `~/carm_cv2_drr` | derived |  | 240 | 200 / 24 / 16 | carmlspine 240 |
| `~/carm_cv3_drr` | derived |  | 224 | 192 / 14 / 18 | carmlspine 224 |
| `~/carm_cv4_drr` | derived |  | 248 | 206 / 20 / 22 | carmlspine 248 |
| `~/carm_cvday0_drr` | derived |  | 164 | 140 / 12 / 12 | carmlspine 164 |
| `~/carm_cvday1_drr` | derived |  | 210 | 170 / 18 / 22 | carmlspine 210 |
| `~/carm_cvday2_drr` | derived |  | 218 | 182 / 18 / 18 | carmlspine 218 |
| `~/carm_drr` | derived |  | 240 | 204 / 18 / 18 | carmlspine 240 |
| `~/fluorocap_drr` | panel | yes | 2,385 | 0 / 0 / 0 (excluded 2,385) | fluorocap 2,385 |
| `~/fluorocap_drr_smoke` | panel |  | 137 | 0 / 0 / 0 (excluded 137) | fluorocap 137 |
| `~/aasce_drr` | radiograph | yes | 440 | 366 / 23 / 51 | aasce 440 |
| `~/films_ap_drr` | radiograph | yes | 3,600 | 2,928 / 331 / 341 | buu 3,600 |
| `~/films_drr` | radiograph | yes | 9,109 | 7,352 / 868 / 889 | csxa 4,963; buu 3,603; nhanes 543 |
| `~/films_drr_buucorr` | radiograph |  | 9,109 | 7,352 / 868 / 889 | csxa 4,963; buu 3,603; nhanes 543 |
| `~/films_smoke` | radiograph |  | 3 | 3 / 0 / 0 | csxa 3 |
| `~/lateral236_pseudo` | radiograph | yes | 236 | 193 / 22 / 21 | lat236 236 |
| `~/mendeley_drr` | radiograph | yes | 584 | 0 / 0 / 0 (excluded 584) | mendeley 584 |
| `~/model_night/vindr_smoke` | radiograph |  | 12 | 9 / 3 / 0 | vindr 12 |
| `~/nhanes_drr` | radiograph |  | 543 | 442 / 52 / 49 | nhanes 543 |
| `~/nhanes_pseudo` | radiograph | yes | 16,234 | 12,982 / 1,667 / 1,585 | nhanes 16,234 |
| `~/pseudo_filtered/lateral236_pseudo_anchored` | radiograph |  | 203 | 164 / 20 / 19 | lat236 203 |
| `~/pseudo_filtered/nhanes_pseudo_anchored` | radiograph |  | 10,087 | 8,089 / 1,022 / 976 | nhanes 10,087 |
| `~/pseudo_filtered/vindr_pseudo_anchored` | radiograph |  | 5,131 | 4,137 / 476 / 518 | vindr 5,131 |
| `~/vindr_det_drr` | radiograph |  | 2,328 | 1,900 / 200 / 228 | vindr 2,328 |
| `~/vindr_pseudo` | radiograph | yes | 10,274 | 8,259 / 977 / 1,038 | vindr 10,274 |
| `~/vindr_pseudo_drr` | radiograph |  | 744 | 614 / 57 / 73 | vindr 744 |
| `$RS/realxray/carmlspine` | real | yes | 299 | 247 / 26 / 26 | carmlspine 299 |
| `$RS/realxray/carmlspine_pre_repair_2026-09-23` | real |  | 296 | 246 / 24 / 26 | carmlspine 296 |
| `$RS/realxray/carmlspine_sweep` | real |  | 301 | 0 / 301 / 0 | carmlspine 301 |
| `$RS/realxray/cobra_elekta` | real | yes | 3,480 | 2,232 / 240 / 840 (hold 168) | cobra 3,480 |
| `$RS/realxray/cobra_elekta_ap45` | real |  | 1,634 | 1,048 / 113 / 393 (hold 80) | cobra 1,634 |
| `$RS/realxray/cobra_elekta_smoke` | real |  | 24 | 24 / 0 / 0 | cobra 24 |
| `$RS/realxray/cobra_elekta_v2` | real |  | 3,480 | 2,232 / 240 / 840 (hold 168) | cobra 3,480 |
| `$RS/realxray/cobra_elekta_v2_ap45` | real |  | 1,634 | 1,048 / 113 / 393 (hold 80) | cobra 1,634 |
| `$RS/realxray/cobra_elekta_v3` | real |  | 3,480 | 2,232 / 240 / 840 (hold 168) | cobra 3,480 |
| `$RS/realxray/deepfluoro` | real | yes | 366 | 231 / 111 / 24 | deepfluoro 366 |
| `$RS/realxray/geneva_hip` | real | yes | 116 | 0 / 0 / 116 | geneva 116 |
| `$RS/devcorpus_arc/anglesweep/elekta_xvi` | render |  | 969 | 684 / 114 / 171 | ts 969 |
| `$RS/devcorpus_arc/anglesweep/surgio_b51_dr` | render |  | 969 | 684 / 114 / 171 | ts 969 |
| `$RS/rare_class/carmlspine_cbct_drr` | render |  | 396 | 0 / 0 / 396 | carmlspine 396 |
| `$RS/rare_class/ctsp_drr` | render |  | 2,834 | 1,243 / 354 / 1,237 | ctsp 2,834 |
| `$RS/rare_class/totalsegmentator_drr` | render |  | 933 | 484 / 0 / 449 | ts 933 |
| `$RS/rare_class/verse_drr` | render |  | 3,920 | 1,960 / 420 / 1,540 | verse 3,920 |
| `~/anchor_drr` | render |  | 7,844 | 6,108 / 770 / 966 | ctsp 4,640; ts 2,456; verse 748 |
| `~/anchor_drr_c2` | render |  | 6,131 | 4,773 / 614 / 744 | ts 3,779; ctsp 1,604; verse 748 |
| `~/ctsp_drr` | render | yes | 802 | 636 / 73 / 93 | ctsp 802 |
| `~/ctsp_drr_film` | render |  | 802 | 636 / 73 / 93 | ctsp 802 |
| `~/ctsp_drr_obl` | render |  | 1,256 | 872 / 124 / 260 | verse 1,256 |
| `~/ctsp_drr_obl2` | render |  | 2,511 | 1,743 / 248 / 520 | verse 2,511 |
| `~/cut_physics` | render |  | 3,000 | 2,387 / 255 / 358 | ctsp 3,000 |
| `~/cut_physics_v2` | render |  | 3,000 | 2,387 / 255 / 358 | ctsp 3,000 |
| `~/cut_rare` | render |  | 1,482 | 714 / 148 / 620 | verse 879; ctsp 603 |
| `~/cut_rare_v2` | render |  | 1,482 | 714 / 148 / 620 | verse 879; ctsp 603 |
| `~/exp3_fluoro` | render |  | 1,058 | 832 / 71 / 155 | ctsp 1,058 |
| `~/exp3_radiograph` | render |  | 1,058 | 832 / 71 / 155 | ctsp 1,058 |
| `~/fluorogen/synth_rare` | render |  | 12,929 | 9,282 / 1,270 / 2,377 | ctsp 6,916; verse 3,267; ts 2,746 |
| `~/fluorogen/synth_rare_lowstrength` | render |  | 566 | 264 / 56 / 246 | verse 340; ctsp 226 |
| `~/lstv_eval/renders60` | render |  | 60 | 20 / 5 / 35 | ctsp 60 |
| `~/lstv_flag/renders` | render |  | 9,624 | 7,632 / 876 / 1,116 | ctsp 9,624 |
| `~/lstv_flag/renders_ctrl` | render |  | 644 | 524 / 44 / 76 | ctsp 644 |
| `~/lstv_flag/renders_verse` | render |  | 3,456 | 2,388 / 324 / 744 | verse 3,456 |
| `~/lstv_flag/smoke` | render |  | 36 | 24 / 12 / 0 | ctsp 36 |
| `~/physics_drr` | render |  | 7,048 | 5,461 / 678 / 909 | ctsp 3,754; ts 1,831; verse 1,463 |
| `~/physics_drr_film` | render |  | 7,048 | 5,461 / 678 / 909 | ctsp 3,754; ts 1,831; verse 1,463 |
| `~/physics_rare` | render |  | 1,482 | 714 / 148 / 620 | verse 879; ctsp 603 |
| `~/physics_rare_film` | render |  | 1,482 | 714 / 148 / 620 | verse 879; ctsp 603 |
| `~/physics_smoke` | render |  | 14 | 8 / 3 / 3 | ctsp 14 |
| `~/postop_render` | render |  | 45 | 26 / 5 / 14 | ctsp 45 |
| `~/render_smoke/fluoro` | render |  | 9 | 7 / 2 / 0 | ctsp 9 |
| `~/render_smoke/radiograph` | render |  | 9 | 7 / 2 / 0 | ctsp 9 |
| `~/ts_drr` | render | yes | 1,170 | 896 / 130 / 144 | ts 1,170 |
| `~/ts_drr_v3` | render | yes | 1,735 | 1,352 / 188 / 195 | ts 1,735 |
| `~/verse_drr` | render | yes | 387 | 279 / 39 / 69 | verse 387 |
| `~/verse_drr_film` | render |  | 374 | 268 / 37 / 69 | verse 374 |
| `~/verse_drr_obl` | render |  | 1,494 | 1,070 / 148 / 276 | verse 1,494 |
| `~/verse_drr_obl2` | render |  | 2,989 | 2,141 / 296 / 552 | verse 2,989 |
| `~/verse_soft_drr` | render | yes | 374 | 268 / 37 / 69 | verse 374 |
| `~/spinalai_drr` | synthetic | yes | 8,358 | 8,358 / 0 / 0 | spinalai 8,358 |

## 4. Transitional persons by subtype, source, truth tier and split side

Two tables. **4a** is the subtype table Table 2 and Figure 5 were drawn from (read / consensus / release-label tiers; distinct persons), with each person's side read from the split file. **4b** is the one transitional registry (2026-09-24), which adds the automatic-labeller tiers and the CT streams outside the split; its read-tier subset should equal 4a.

### 4a. Subtype table (Table 2's basis), persons by source and side

| subtype | source | persons | train / val / test | Table 2 persons |
|---|---|---|---|---|
| L6 | ctsp | 18 | 9 / 2 / 7 | 18 |
| L6 | verse | 86 | 43 / 9 / 34 | 86 |
| L6 | ts | 3 | 1 / 0 / 2 | 3 |
| L6 | carmlspine | 3 | 0 / 0 / 3 | 3 |
| T13 | verse | 6 | 3 / 1 / 2 | 6 |
| T13 | ts | 1 | 0 / 0 / 1 | 1 |
| sacralised_L5_four_lumbar | ctsp | 9 | 4 / 1 / 4 | 9 |
| sacralised_L5_four_lumbar | verse | 3 | 1 / 1 / 1 | 3 |
| sacralised_L5_five_lumbar | ctsp | 3 | 2 / 0 / 1 | 3 |
| sacralised_L5_five_lumbar | verse | 13 | 7 / 1 / 5 | 13 |
| castellvi_I_II | ctsp | 4 | 2 / 0 / 2 | 4 |
| castellvi_I_II | verse | 27 | 14 / 3 / 10 | 27 |
| lumbar_rib | ctsp | 14 | 7 / 1 / 6 | 14 |
| unassigned | ctsp | 4 | 1 / 1 / 2 | 4 |

### 4b. Registry, all truth tiers (read > two-labeller > single-labeller > morphology-only), persons by source, tier and side

| subtype | source | persons | by tier | train / val / test (not in split) | real frames |
|---|---|---|---|---|---|
| L6 | verse | 85 | {'read': 85} | 43 / 9 / 33 | 0 |
| L6 | ctsp | 29 | {'read': 17, 'two-labeller': 11, 'single-labeller': 1} | 14 / 4 / 11 | 0 |
| L6 | ts | 22 | {'two-labeller': 14, 'single-labeller': 8} | 16 / 1 / 5 | 0 |
| L6 | ctspine1k | 3 | {'read': 1, 'two-labeller': 2} | 0 / 0 / 0 (3 not in split) | 0 |
| L6 | cobra | 3 | {'two-labeller': 2, 'single-labeller': 1} | 0 / 0 / 3 | 3 |
| L6 | carmlspine | 3 | {'morphology-only': 3} | 0 / 0 / 3 | 3 |
| L6 | ribfrac | 1 | {'morphology-only': 1} | 0 / 0 / 0 (1 not in split) | 0 |
| T13 | verse | 6 | {'read': 6} | 3 / 1 / 2 | 0 |
| T13 | ts | 4 | {'two-labeller': 3, 'single-labeller': 1} | 3 / 0 / 1 | 0 |
| T13 | ribfrac | 4 | {'single-labeller': 4} | 0 / 0 / 0 (4 not in split) | 0 |
| sacralised_L5_four_lumbar | ctsp | 9 | {'read': 9} | 4 / 1 / 4 | 0 |
| sacralised_L5_four_lumbar | ctspine1k | 2 | {'read': 2} | 0 / 0 / 0 (2 not in split) | 0 |
| sacralised_L5_five_lumbar | verse | 13 | {'read': 13} | 7 / 1 / 5 | 0 |
| sacralised_L5_five_lumbar | ctsp | 3 | {'read': 3} | 2 / 0 / 1 | 0 |
| castellvi_I_II | verse | 27 | {'read': 27} | 14 / 3 / 10 | 0 |
| castellvi_I_II | ctsp | 4 | {'read': 4} | 2 / 0 / 2 | 0 |
| lumbar_rib | ctsp | 14 | {'two-labeller': 9, 'single-labeller': 5} | 7 / 1 / 6 | 0 |
| lumbar_rib | verse | 12 | {'read': 12} | 11 / 1 / 0 | 0 |
| unassigned | ts | 26 | {'two-labeller': 8, 'single-labeller': 18} | 21 / 1 / 4 | 0 |
| unassigned | verse | 23 | {'read': 23} | 17 / 3 / 3 | 0 |
| unassigned | cobra | 6 | {'two-labeller': 4, 'single-labeller': 2} | 0 / 0 / 6 | 6 |
| unassigned | ctsp | 5 | {'two-labeller': 5} | 1 / 1 / 3 | 0 |
| unassigned | carmlspine | 1 | {'single-labeller': 1} | 1 / 0 / 0 | 1 |
| unassigned | ribfrac | 1 | {'single-labeller': 1} | 0 / 0 / 0 (1 not in split) | 0 |

Read-tier registry keys that differ from the subtype table:

- L6: in the subtype table, not read-tier in the registry: ['carmlspine:case121', 'carmlspine:case136', 'carmlspine:case42', 'ctsp:0068', 'ts:s1088', 'ts:s1089', 'ts:s1123', 'verse:gl279', 'verse:verse707']; read-tier in the registry, not in the subtype table: ['ctspine1k:MSD-T10:liver_106', 'verse:verse026']
- T13: in the subtype table, not read-tier in the registry: ['ts:s0616']; read-tier in the registry, not in the subtype table: []
- lumbar_rib: in the subtype table, not read-tier in the registry: ['ctsp:0172', 'ctsp:0231', 'ctsp:0315', 'ctsp:0389', 'ctsp:0428', 'ctsp:0431', 'ctsp:0473', 'ctsp:0516', 'ctsp:0568', 'ctsp:0660', 'ctsp:0680', 'ctsp:0720', 'ctsp:1004', 'ctsp:1090']; read-tier in the registry, not in the subtype table: ['verse:verse005', 'verse:verse031', 'verse:verse054', 'verse:verse073', 'verse:verse141', 'verse:verse149', 'verse:verse254', 'verse:verse260', 'verse:verse276', 'verse:verse415', 'verse:verse708', 'verse:verse807']
- sacralised_L5_four_lumbar: in the subtype table, not read-tier in the registry: ['verse:verse549', 'verse:verse552', 'verse:verse559']; read-tier in the registry, not in the subtype table: ['ctspine1k:MSD-T10:liver_83', 'ctspine1k:MSD-T10:liver_93']
- unassigned: in the subtype table, not read-tier in the registry: ['ctsp:0801', 'ctsp:0931', 'ctsp:1043', 'ctsp:1123']; read-tier in the registry, not in the subtype table: ['verse:verse008', 'verse:verse016', 'verse:verse022', 'verse:verse047', 'verse:verse056', 'verse:verse091', 'verse:verse108', 'verse:verse111', 'verse:verse139', 'verse:verse145', 'verse:verse410', 'verse:verse511', 'verse:verse531', 'verse:verse533', 'verse:verse549', 'verse:verse550', 'verse:verse552', 'verse:verse559', 'verse:verse640', 'verse:verse646', 'verse:verse756', 'verse:verse759', 'verse:verse824']

CTSpinoPelvic1K release-mask flags (`results/polypose/inputs/lstv_flag_labels_v2.csv columns has_L6, has_lumbar_rib, LSTV_flag, TLTV_flag, lstv_label, cohort`): 802 records; has_L6 18 (by side {'test': 7, 'val': 2, 'train': 9}); has_lumbar_rib 16; LSTV_flag 34; TLTV_flag 16; source lstv_label {'normal': 769, 'SACRALIZATION': 17, 'SEMI_SACRALIZATION': 2, 'LUMBARIZATION': 14}. VerSe rows 311, LSTV_flag 130.

## 5. Discrepancies against Table 1 (tables/tab_corpus.tex as printed)

| source | cell | Table 1 | census | likely cause |
|---|---|---|---|---|
| ctsp | subjects | 801 patients of 802 records | 802 persons in the split ((636, 73, 93) train/val/test); ctsp:0533 side = test | record 0533 was rebuilt (results/repairs/ct0533_CHECK.md: job 40416624 swapped=1 count=802; job 40416626 ctsp_drr=802) and is a person of the G3 split; Table 1 footnote b still says it is in no bank |
| ctsp | renders | 801 renders | 802 items in ~/ctsp_drr | the same 0533 rebuild: its render exists (job 40416626) |
| ts | subjects | 1,935 scans | 1867 persons after the split's alias folds ((1469, 193, 205)); 29 ts edges in group_of | the split folds TotalSegmentator scans by CT md5 and by shape+affine (split_plan.md CHK-2: 26 md5 groups + 27 shape+affine groups + the spec's declared pairs), more than the 24 renumbered pairs and three duplicate groups footnote c names; 1,935 is the scan count, the split's unit is the folded scan group |
| buu | subjects | 3,600 cases | 3598 persons ((2926, 331, 341)); group_of folds buu:0629->0449 and buu:0719->0140 | the split merges the two case pairs with byte-identical films that footnote d anticipates (at most 3,598 by content) |
| nhanes | subjects (whole release) | 364 persons among the annotated | 9581 sample persons in the split ((7673, 969, 939)): the 364 annotated plus the persons of the pseudo-labelled release films | the G4 corpus takes NHANES II whole (FLAGSHIP_PLAN corpus table; directive D2); Table 1 counts persons among the annotated films only; the NHANES double inclusion (films_drr + nhanes_drr) is closed by keying both copies to one sample person (patient_keys.py nhanes_drr/nhanes_film schemes) |
| nhanes | films | 543 annotated films (542 on disk) of 17,075 | 16272 distinct (person, view) films ({'train': 13010, 'test': 1590, 'val': 1672}): 543 annotated + 16234 pseudo-labelled, 505 in both; 543 annotated items in ~/nhanes_drr and again in ~/films_drr (one copy each, the same films) | Table 1 counts the annotated films; the corpus adds the release films that carry a pseudo-label ann (~/nhanes_pseudo); 17,073 are on disk, so 17,073 - 16,272 = 801 films have neither an annotation nor a pseudo-label ann and are in no root |
| nhanes | films (primary roots, additive count) | - | primary roots sum to 16777 but the distinct films are 16272 | the 543 annotated films sit in films_drr and 505 of them again in nhanes_pseudo; section 2 prints the root sum, this row the distinct count |
| footnote a | physics-styled re-renders | 7,045 over 3,029 subjects | 7048 items in ~/physics_drr ({'train': 5461, 'val': 678, 'test': 909}) | unexplained difference of a few items; footnote a may have been counted before the last render job or after a smoke exclusion |
| vindr | subjects | 5,000 studies | 4981 studies in the split ((4019, 475, 487)); 4981 studies have a pseudo-label or detector item | the split keys VinDr by study (identity export job 40416449) and places only studies with an item (CHK-8b); Table 1's 5,000 is the release count |
| vindr | films | 2,071 films as 2,632 crops, of 10,466 released images | 10274 release images with a pseudo-label ann in ~/vindr_pseudo ({'train': 8259, 'val': 977, 'test': 1038, 'hold': 0, 'excluded': 0}); 2,328 lesion-box films in ~/vindr_det_drr | Table 1 prints the fold-bank crop object (2,071 films as 2,632 crops); the corpus census counts release images with an ann; 10,466 - 10,274 = 192 images carry no pseudo-label ann and are in no root |
| fluorocap | subjects | not established | 1953 excluded person keys ({'fluorocap': 1616, 'fluorocap_video': 337}) | FluoroCap is excluded from the corpus (PI decision); its keys are source documents before the perceptual-hash merge (PATIENT_IDENTITY_SPEC: about 1,197 documents, uncertain), so the key count is not a subject count |
| fluorocap | panels | 950 panels as 2,100 crops, of 29,484 harvested | 2385 panels excluded in ~/fluorocap_drr (+137 smoke) | the 950 panels / 2,100 crops of Table 1 are the fold-bank object; the corpus drops FluoroCap |
| carmlspine | subjects | not established; 149 released cases, 148 scored | 149 cases in the split ((123, 13, 13)); 149 cases with a spot frame in $RS/realxray/carmlspine | the case134 repair (DATA_COMPLETENESS_AUDIT Repairs 2026-09-23; jobs 40416561-3): its two exposures under CBCT/ are now exported, so 149 cases are built, not 148; the G3 split is by person hash (80/10/10), not the detector's 7:1:2 case split |
| carmlspine | frames | 296 scored: 210 / 30 / 56 (105 / 15 / 28 cases); released 299 spot exposures, two cone-beam sweeps | {'train': 247, 'val': 26, 'test': 26, 'hold': 0, 'excluded': 0} over 299 items: 299 spot exposures (views {'AP': 149, 'LAT': 149, 'OBL': 1}) + 301 sweep projections of case134 (side val) | after the repair the bank holds 299 spot frames (case134's two added, case39's third kept as LAT2, case118's second frame typed OBL); the 210/30/56 of Table 1 is the pre-repair fixed case split; the sweep is one root of 301 projections, the second sweep is in no root |
| deepfluoro | frames by side | 366 frames: 238 / 24 / 104 | 366 frames: (231, 111, 24); per specimen {'17-1882': {'val': 111}, '17-1905': {'test': 24}, '18-0725': {'train': 24}, '18-1109': {'train': 104}, '18-2799': {'train': 48}, '18-2800': {'train': 55}} | the G3 split draws the exact 4/1/1 specimens by seed 0 (split_plan.md: DeepFluoro exact {'train': 4, 'val': 1, 'test': 1}); the detector's split (val 18-0725, test 18-1109) is a different draw; the frame total is unchanged |
| cobra | subjects | 145 patients of 467 public Elekta cases (110 / 8 / 27) | 692 cases in the split ({'train': 445, 'val': 71, 'test': 159, 'hold': 17, 'excluded': 0}); 145 cases with a frame in $RS/realxray/cobra_elekta ({'test': 35, 'train': 93, 'val': 10, 'hold': 7}) | the split places every catalogued case (692) so that later fetches land on a drawn side; Table 1 counts the 145 kept cases with frames; 'hold' = cases the screen has not called |
| cobra | frames by side | 3,480 frames: 2,640 / 192 / 648 | 3480 frames in cobra_elekta: {'train': 2232, 'val': 240, 'test': 840, 'hold': 168, 'excluded': 0} | the G3 person split re-draws the 145 cases (transitional screen calls to test, the rest by hash); the 2,640/192/648 is the detector's earlier 110/8/27 case split; cobra_elekta_v2, _v3 (3,480 each) and the two ap45 subsets are the same frames re-windowed or subset (results/repairs/cobra-dup-leak_CHECK.md: 5,013 duplicate list entries in one arm) and are not added |
| geneva | subjects | 1 phantom | 19 keys in the split, all test: ['geneva:phantom_p01', 'geneva:phantom_p02', 'geneva:phantom_p03']... | the split keys the phantom's camera views (p01..p25, 19 present) as separate keys; PATIENT_IDENTITY_SPEC says one object; the count is views, not subjects; every item is test, so no leak follows |
| ljubljana | subjects / frames | 1 specimen (not split); 18 frames | absent from the split (no root, no person key) | the 18 PIXIUM frames were used for device parameters only and were never exported to a bank; the census cannot count them from the split |
| aasce | row | no row | 217 keys ({'train': 178, 'val': 14, 'test': 25, 'hold': 0, 'excluded': 0}); primary items 440 | in the split but in no Table 1 row (footnote k names AASCE and SpinalAI as used by no trained component; Mendeley excluded; lat236 is not named anywhere in the tables) |
| spinalai | row | no row | 44 keys ({'train': 44, 'val': 0, 'test': 0, 'hold': 0, 'excluded': 0}); primary items 8358 | in the split but in no Table 1 row (footnote k names AASCE and SpinalAI as used by no trained component; Mendeley excluded; lat236 is not named anywhere in the tables) |
| lat236 | row | no row | 236 keys ({'train': 193, 'val': 22, 'test': 21, 'hold': 0, 'excluded': 0}); primary items 236 | in the split but in no Table 1 row (footnote k names AASCE and SpinalAI as used by no trained component; Mendeley excluded; lat236 is not named anywhere in the tables) |
| mendeley | row | no row | 51 keys ({'train': 0, 'val': 0, 'test': 0, 'hold': 0, 'excluded': 51}); primary items 584 | in the split but in no Table 1 row (footnote k names AASCE and SpinalAI as used by no trained component; Mendeley excluded; lat236 is not named anywhere in the tables) |

## 6. Comparison with Table 2 (tables/tab4_transitional.tex as printed)

| subtype | Table 2: total (CTSP / VerSe / TS / C-Arm); test CT + real | subtype table now | registry, all tiers | registry read tier | notes |
|---|---|---|---|---|---|
| L6 | 110 (18 / 86 / 3 / 3); 43 + 3 | 110 (18 / 86 / 3 / 3); 43 + 3 | {'total': 146, 'ctsp': 29, 'verse': 85, 'ctspine1k': 3, 'ts': 22, 'cobra': 3, 'carmlspine': 3, 'ribfrac': 1} | 103 | the registry (all truth tiers) counts 146 persons against the subtype table's 110; registry tiers {'read': 103, 'two-labeller': 29, 'single-labeller': 10, 'morphology-only': 4}; the registry re-tiers release-label and automatic-labeller rows (two-labeller / single-labeller / morphology-only) and adds the CTSpine1K, RibFrac and COBRA streams, which the subtype table never held registry's own statement per person (table_vs_registry): new to the registry (L6, two-labeller) [ts, two-labeller]: 13; new to the registry (L6, two-labeller) [ctsp, two-labeller]: 10; new to the registry (L6, single-labeller) [ts, single-labeller]: 8; new to the registry (L6, two-labeller) [cobra, two-labeller]: 2; new to the registry (L6, two-labeller) [ctspine1k, two-labeller]: 2; table T13 -> registry unresolved (none) [ts, none]: 2; table L6 -> registry none (none) [verse, none]: 2; new to the registry (L6, read) [verse, read]: 1; new to the registry (L6, read) [ctspine1k, read]: 1; new to the registry (L6, single-labeller) [ctsp, single-labeller]: 1; new to the registry (L6, single-labeller) [cobra, single-labeller]: 1; new to the registry (L6, morphology-only) [ribfrac, morphology-only]: 1 read-tier key differences: {'in_subtype_table_not_registry_read_tier': ['carmlspine:case121', 'carmlspine:case136', 'carmlspine:case42', 'ctsp:0068', 'ts:s1088', 'ts:s1089', 'ts:s1123', 'verse:gl279', 'verse:verse707'], 'in_registry_read_tier_not_subtype_table': ['ctspine1k:MSD-T10:liver_106', 'verse:verse026']} |
| T13 | 7 (0 / 6 / 1 / 0); 3 + 0 | 7 (0 / 6 / 1 / 0); 3 + 0 | {'total': 14, 'verse': 6, 'ts': 4, 'ribfrac': 4} | 6 | the registry (all truth tiers) counts 14 persons against the subtype table's 7; registry tiers {'read': 6, 'two-labeller': 3, 'single-labeller': 5}; the registry re-tiers release-label and automatic-labeller rows (two-labeller / single-labeller / morphology-only) and adds the CTSpine1K, RibFrac and COBRA streams, which the subtype table never held registry's own statement per person (table_vs_registry): new to the registry (T13, single-labeller) [ribfrac, single-labeller]: 4; new to the registry (T13, two-labeller) [ts, two-labeller]: 2; new to the registry (T13, single-labeller) [ts, single-labeller]: 1 read-tier key differences: {'in_subtype_table_not_registry_read_tier': ['ts:s0616'], 'in_registry_read_tier_not_subtype_table': []} |
| sacralised_L5_four_lumbar | 12 (9 / 3 / 0 / 0); 5 + 0 | 12 (9 / 3 / 0 / 0); 5 + 0 | {'total': 11, 'ctsp': 9, 'ctspine1k': 2} | 11 | the registry (all truth tiers) counts 11 persons against the subtype table's 12; registry tiers {'read': 11}; the registry re-tiers release-label and automatic-labeller rows (two-labeller / single-labeller / morphology-only) and adds the CTSpine1K, RibFrac and COBRA streams, which the subtype table never held registry's own statement per person (table_vs_registry): moved: table sacralised_L5_fused -> registry unassigned [verse, read]: 3; new to the registry (sacralised_L5_fused, read) [ctspine1k, read]: 2 read-tier key differences: {'in_subtype_table_not_registry_read_tier': ['verse:verse549', 'verse:verse552', 'verse:verse559'], 'in_registry_read_tier_not_subtype_table': ['ctspine1k:MSD-T10:liver_83', 'ctspine1k:MSD-T10:liver_93']} |
| sacralised_L5_five_lumbar | 16 (3 / 13 / 0 / 0); 6 + 0 | 16 (3 / 13 / 0 / 0); 6 + 0 | {'total': 16, 'ctsp': 3, 'verse': 13} | 16 | agrees |
| castellvi_I_II | 31 (4 / 27 / 0 / 0); 12 + 0 | 31 (4 / 27 / 0 / 0); 12 + 0 | {'total': 31, 'ctsp': 4, 'verse': 27} | 31 | agrees |
| lumbar_rib | 14 (14 / 0 / 0 / 0); 6 + 0 | 14 (14 / 0 / 0 / 0); 6 + 0 | {'total': 26, 'verse': 12, 'ctsp': 14} | 12 | the registry (all truth tiers) counts 26 persons against the subtype table's 14; registry tiers {'read': 12, 'two-labeller': 9, 'single-labeller': 5}; the registry re-tiers release-label and automatic-labeller rows (two-labeller / single-labeller / morphology-only) and adds the CTSpine1K, RibFrac and COBRA streams, which the subtype table never held registry's own statement per person (table_vs_registry): new to the registry (lumbar_rib, read) [verse, read]: 12 read-tier key differences: {'in_subtype_table_not_registry_read_tier': ['ctsp:0172', 'ctsp:0231', 'ctsp:0315', 'ctsp:0389', 'ctsp:0428', 'ctsp:0431', 'ctsp:0473', 'ctsp:0516', 'ctsp:0568', 'ctsp:0660', 'ctsp:0680', 'ctsp:0720', 'ctsp:1004', 'ctsp:1090'], 'in_registry_read_tier_not_subtype_table': ['verse:verse005', 'verse:verse031', 'verse:verse054', 'verse:verse073', 'verse:verse141', 'verse:verse149', 'verse:verse254', 'verse:verse260', 'verse:verse276', 'verse:verse415', 'verse:verse708', 'verse:verse807']} |
| unassigned | 4 (4 / 0 / 0 / 0); 2 + 0 | 4 (4 / 0 / 0 / 0); 2 + 0 | {'total': 62, 'verse': 23, 'ctsp': 5, 'ts': 26, 'cobra': 6, 'carmlspine': 1, 'ribfrac': 1} | 23 | the registry (all truth tiers) counts 62 persons against the subtype table's 4; registry tiers {'read': 23, 'two-labeller': 17, 'single-labeller': 22}; the registry re-tiers release-label and automatic-labeller rows (two-labeller / single-labeller / morphology-only) and adds the CTSpine1K, RibFrac and COBRA streams, which the subtype table never held registry's own statement per person (table_vs_registry): new to the registry (unassigned, read) [verse, read]: 20; new to the registry (unassigned, single-labeller) [ts, single-labeller]: 18; new to the registry (unassigned, two-labeller) [ts, two-labeller]: 8; new to the registry (unassigned, two-labeller) [cobra, two-labeller]: 4; moved: table sacralised_L5_fused -> registry unassigned [verse, read]: 3; new to the registry (unassigned, two-labeller) [ctsp, two-labeller]: 2; new to the registry (unassigned, single-labeller) [cobra, single-labeller]: 2; new to the registry (unassigned, single-labeller) [carmlspine, single-labeller]: 1; new to the registry (unassigned, single-labeller) [ribfrac, single-labeller]: 1; table unassigned -> registry none (none) [ctsp, none]: 1 read-tier key differences: {'in_subtype_table_not_registry_read_tier': ['ctsp:0801', 'ctsp:0931', 'ctsp:1043', 'ctsp:1123'], 'in_registry_read_tier_not_subtype_table': ['verse:verse008', 'verse:verse016', 'verse:verse022', 'verse:verse047', 'verse:verse056', 'verse:verse091', 'verse:verse108', 'verse:verse111', 'verse:verse139', 'verse:verse145', 'verse:verse410', 'verse:verse511', 'verse:verse531', 'verse:verse533', 'verse:verse549', 'verse:verse550', 'verse:verse552', 'verse:verse559', 'verse:verse640', 'verse:verse646', 'verse:verse756', 'verse:verse759', 'verse:verse824']} |
| any | {'total': 194, 'ctsp': 52, 'verse': 135, 'ts': 4, 'carmlspine': 3, 'test_ct': 77, 'test_real': 3} | {'ctsp': 52, 'verse': 135, 'ts': 4, 'carmlspine': 3, 'total': 194, 'test_ct': 77, 'test_real': 3} (194 distinct persons) | {'total_all_tiers': 306}; unresolved by source {'ts': 74, 'cobra': 11, 'ctspine1k': 15, 'ribfrac': 29} | | |

Earlier detector case split of the real-frame banks (results/realxray_lists_audit.json, for the comparison in section 5): {"carmlspine": {"images": {"train": 210, "val": 30, "test": 56}, "cases": {"train": 105, "val": 15, "test": 28}}, "cobra_elekta": {"images": {"train": 2640, "val": 192, "test": 648}, "cases": {"train": 110, "val": 8, "test": 27}}, "deepfluoro": {"images": {"train": 238, "val": 24, "test": 104}, "cases": {"train": 4, "val": 1, "test": 1}}, "geneva_hip": {"images": {"train": 0, "val": 0, "test": 116}, "cases": {"train": 0, "val": 0, "test": 1}}}

## 7. What is not known

- Ljubljana's 18 frames are in no split root; they are counted from Table 1 alone.
- The second C-ArmLSpine cone-beam sweep (two 301-projection sweeps are released) is in no split root; only case134's is.
- COBRA2026: 692 catalogued cases are placed but only 145 have frames in a split root; the full-release fetch (JOBS_cobra.txt) had not been exported to a bank when the split was drawn (cobra_elekta_g3test exists on the grid and is not in the split).
- TotalSegmentator persons: 1,935 scans fold to the split's person groups by content hash; whether the folded groups are persons is unknown (the release ships no patient identifier).
- C-ArmLSpine cases are acquisitions on five dates, not proven persons (PATIENT_IDENTITY_SPEC); the census counts cases.
- Geneva: the split carries 19 keys for one phantom; a per-key count is a view count.
- VinDr: 192 release images carry no pseudo-label ann and are in no root; the 19 studies without an item are on no side.
- The registry's two-labeller and single-labeller transitional calls (CTSP, TotalSegmentator, COBRA, CTSpine1K, RibFrac) are unread; which of them will be certified as transitional persons is open, so the census reports them by tier and does not add them to Table 2's counts.
- Renders per source over all roots double-count CTs (poses, styles, film copies, field-of-view cuts); only the primary roots give one image per CT.
