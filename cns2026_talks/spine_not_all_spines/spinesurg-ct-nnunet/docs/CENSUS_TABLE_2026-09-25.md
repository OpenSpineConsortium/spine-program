# The CT census: collections, spinal range, n, expected transitional people, what the screen has called, storage

Greg, 2026-09-25: "a table with all the datasets in the census, their presumed anatomical range along the spine, their n, the estimated number of each class of transitional anatomy ... and how much memory each will roughly require since I only have 20 TB". Read with the caveats at the end.

**How the expectations are computed** (ACQUISITION_PLAN.md section 2, constants in tools/acquisition_census.py). countable_LS = sum over CTs of P(both lumbosacral references in the field | coverage class); cage = sum of P(rib cage from T1 in the field). Then L6 = 3.2 % of countable_LS, four-lumbar (sacralised L5) = 1.6 % (Sun 2025, UK Biobank controls); Castellvi II-IV, which includes those two, = 9-18 % (Hanhivaara 2020; Nardo 2012); T13 = 0.64-2.0 % of cage (VertebralBodiesCT-Labels; L1 ribs in Sun 2025). P per coverage class was measured on TotalSegmentator v2's study types (WB 0.665/0.707, CAP 0.794/0.787, AP 0.763/0.018, abdomen 0.80/0, chest-abdomen 0.52/0.46, chest 0.053/0.70, chest screening 0/0.70, pelvis 0.118/0, spine 0.29/0.29). Collections found on 2026-09-24 (PANORAMA to CSI) have no ranking row; their class P is applied to the on-disk case count. The screen's own FOV gate (gate_pass) is the measured countable number where the chain has reached it.

## 1. Collections being screened now (22 chains; two labellers, SPINEPS+VERIDAH and TotalSegmentator geometry)

| collection | presumed spinal range | n listed | CTs on disk | FOV gate pass | expected L6 | expected 4-lumbar | expected Castellvi II-IV | expected T13 | called so far (registry rows) | raw GB | seg GB | status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---|
| AbdomenAtlas 3.0 Mini | abdomen; per-CT extent (a third reach T1) | 7,835 | 7,650 | 5,891 | 144 | 72 | 406-813 | 18.9-59.0 | - | 532 | 107 | SPINEPS running (12 GPUs) |
| IDC tier 1 (39 collections) | mixed: CAP, abdomen, chest, whole body | 3,600 | 3,500 | 3,044 | 62 | 31 | 173-346 | 11.4-35.5 | - | 658 | 55 | SPINEPS running (4 GPUs) |
| TCIA FDG-PET-CT-Lesions | whole body (skull to thigh) | 900 | 901 | 901 | 19 | 10 | 54-108 | 4.1-12.7 | - | 367 | 31 | SPINEPS running (6 GPUs) |
| AMOS22 CT (labelled + unlabelled) | abdomen | 2,200 | 724 | 723 | 19 | 9 | 52-104 | 0.0-0.0 | L6 two-labeller 9, single 11; T13 single 2; review 44; unassigned 24 | 96 | 13 | called |
| PANORAMA | abdomen (pancreas CE-CT) | 2,238 | 2,026 | pending | 52 | 26 | 146-292 | 0.0-0.0 | - | 182 | 16 | TotalSegmentator running (4 GPUs) |
| NLST pilot | chest, low-dose screening (adrenals caudal limit) | 500 | 501 | 499 | 0 | 0 | 0-0 | 2.2-7.0 | T13 single 5; lumbosacral count 0 | 69 | 7 | called |
| WAW-TACE | abdomen (liver, TACE) | 229 | 229 | 214 | 6 | 3 | 16-33 | 0.0-0.0 | - | 44 | 5 | SPINEPS running (1 GPU) |
| Kidney thorax-abdomen | chest + abdomen | 216 | 216 | 216 | 4 | 2 | 10-20 | 0.6-2.0 | - | 71 | 9 | SPINEPS running (1 GPU) |
| Barts CRL | abdomen (colorectal liver) | 213 | 213 | 212 | 5 | 3 | 15-31 | 0.0-0.0 | - | 19 | 6 | SPINEPS running (1 GPU) |
| PENGWIN 2026 | pelvis (fracture CT) | 341 | 341 | 12 | 1 | 1 | 4-7 | 0.0-0.0 | L6 single 1 | 78 | 5 | called |
| CTPelvic1K clinical 6-7 | pelvis | 178 | 173 | 7 | 1 | 0 | 2-4 | 0.0-0.0 | unassigned 1 | 14 | 5 | called |
| CURVAS-PDAC-VI | abdomen | 102 | 102 | 97 | 3 | 1 | 7-15 | 0.0-0.0 | T13 single 1; review 11 | 16 | 4 | called |
| CURVAS | abdomen | 71 | 71 | 57 | 2 | 1 | 5-10 | 0.0-0.0 | L6 single 4; unassigned 1 | 28 | 5 | called |
| TotalSegmentator v2 validation set | mixed (study types), 70 with external L6/T13 labels | 71 | 71 | 70 | 2 | 1 | 5-10 | 0.2-0.6 | L6 two-labeller 10, single 2; T13 single 7; review 14 | 1 | 2 | called + validated |
| AortaSeg60 | chest + abdomen + pelvis (CTA) | 56 | 56 | 56 | 1 | 1 | 4-8 | 0.3-0.9 | L6 two-labeller 1; review 4 | 15 | 5 | called |
| Deep-PSMA | whole body (PET/CT) | 54 | 54 | 54 | 1 | 1 | 3-6 | 0.2-0.8 | review 5; unassigned 1 | 23 | 3 | called |
| QUADRA-HC | whole body (long-axial PET/CT) | 49 | 49 | 49 | 1 | 1 | 3-6 | 0.2-0.7 | L6 two-labeller 1; T13 single 1; review 6; unassigned 1 | 20 | 3 | called |
| CSI 2014 spine | thoracolumbar spine | 20 | 21 | 21 | 0 | 0 | 1-1 | 0.0-0.1 | unassigned 2 | 7 | 3 | called |
| **sum** | | **18,873** | **16,898** | **12,123** | **322** | **161** | **907-1813** | **38-119** | L6 two-labeller 21, single 18; T13 single 16; review 84 | **2,240** | **284** | |

Registry rows so far: 169 across the finished screens (amos22 90, TS v2 validation 33, CURVAS-PDAC-VI 12, QUADRA-HC 9, Deep-PSMA 6, NLST 5, CURVAS 5, AortaSeg60 5, CSI 2, PENGWIN 1, CTPelvic1K 1). 'review' = the two labellers disagree and a render awaits a human; 'unassigned' = one labeller could not count. GPU spent so far: 843 GPU-hours (TotalSegmentator 443, SPINEPS 400).

## 2. Planned, not started: tier 2 (chest-dominated; T13 is the only yield)

| collection | presumed spinal range (coverage mix) | n qualifying | expected L6 | expected 4-lumbar | expected Castellvi II-IV | expected T13 | fetch GB | seg GB (est.) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| idc:nlst | CHEST_SCREEN:24491;OTHER:222 | 24,713 | 0.7 | 0.3 | 2-4 | 109.4-342.0 | 2,305 | 346 |
| aws:stoic2021 | CHEST_SCREEN:2000 | 2,000 | 0.0 | 0.0 | 0-0 | 8.9-27.8 | 240 | 36 |
| idc:lidc_idri | CHEST_SCREEN:953;CAP:38;CA:4;ABD:1;AP:1 | 997 | 1.1 | 0.5 | 3-6 | 4.4-13.9 | 123 | 18 |
| zenodo:ribfrac | CHEST_SCREEN:660 | 660 | 0.0 | 0.0 | 0-0 | 2.9-9.2 | 78 | 12 |
| idc:nsclc_radiogenomics | CHEST_SCREEN:168;WB:10;CAP:8;ABD:1;CA:1 | 188 | 0.5 | 0.2 | 1-3 | 0.8-2.6 | 28 | 4 |
| idc:spinal_multiple_myeloma_seg | SPINE:67 | 67 | 0.6 | 0.3 | 2-4 | 0.1-0.4 | 34 | 5 |
| idc:nsclc_radiomics | CHEST_SCREEN:415 | 415 | 0.0 | 0.0 | 0-0 | 1.8-5.8 | 26 | 4 |
| idc:spine_mets_ct_seg | SPINE:51;ABD:2;PELVIS:1 | 54 | 0.5 | 0.3 | 2-3 | 0.1-0.3 | 17 | 3 |
| idc:prostate_anatomical_edge_cases | PELVIS:131 | 131 | 0.5 | 0.2 | 1-3 | 0.0-0.0 | 17 | 2 |
| idc:ldct_and_projection_data | CHEST:99 | 99 | 0.2 | 0.1 | 0-1 | 0.4-1.4 | 16 | 2 |
| idc:cptac_lscc | CHEST:20;OTHER:6;WB:4;CAP:2 | 32 | 0.2 | 0.1 | 1-1 | 0.1-0.4 | 8 | 1 |
| idc:cptac_luad | CHEST:22;OTHER:4;WB:4;ABD:2 | 32 | 0.2 | 0.1 | 1-1 | 0.1-0.4 | 7 | 1 |
| idc:midrc_ricord_1b | CHEST_SCREEN:61;OTHER:29;CAP:1 | 91 | 0.1 | 0.1 | 0-1 | 0.3-1.0 | 7 | 1 |
| **sum** | | **29,479** | **5** | **2** | **13-26** | **130-405** | **2,907** | **436** |

NLST alone is 2.3 TB for about 110 T13 people and no lumbosacral count (the caudal limit is the adrenals). The stopping rule in the plan (E_low per TB >= 20, CephFS floor 5 TB, acquisition cap 8 TB) refuses it as it stands.

## 3. Gated (a form each; none signed): the largest yields in the census

| collection | presumed spinal range | n | expected L6 | expected 4-lumbar | expected Castellvi II-IV | expected T13 | raw GB (est.) | seg GB (est.) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| stanford_aimi:merlin | AP:18317 | 18,317 | 447 | 224 | 1258-2516 | 2-7 | 1,530 | 229 |
| rsna:ratic_abdominal_trauma | CAP:3147 | 3,147 | 80 | 40 | 225-450 | 16-50 | 942 | 141 |
| hf:ct_rate | CHEST_SCREEN:21304 | 21,304 | 0 | 0 | 0-0 | 95-297 | 2,130 | 320 |
| stanford_aimi:inspect | CHEST_SCREEN:19402 | 19,402 | 0 | 0 | 0-0 | 86-270 | 1,940 | 291 |
| hf:cads_unique | WB:753 | 753 | 16 | 8 | 45-90 | 3-11 | 123 | 19 |
| **sum** | | | **543** | **272** | **1528-3056** | **203-633** | **6,666** | **1,000** |

Merlin (Stanford AIMI, one research-use agreement) is worth more than the whole open tier 1 by itself: about 447 L6 and 224 four-lumbar people expected against 322 and 161 for everything being screened now. Its size is an estimate (25,494 CTs at about 60 MB each as compressed NIfTI; the plan lists no size).

## 4. Storage against the 20 TB volume

| block | raw GB | segmentation GB | total GB |
|---|---:|---:|---:|
| screened collections on disk now (section 1) | 2,240 | 284 | 2,524 |
| the rest of the volume today (COBRA2026 754, or_ready models and dumps 682, CTSpine1K 152, DeepFluoro 104, PolyPose 82, C-ArmLSpine 81, RibFrac 73, others ~60) | 1,988 | - | 1,988 |
| **used today (df-ceph, 2026-09-25 14:50)** | | | **4,482 (22 % of 20 TB)** |
| tier 2 if fetched in full (section 2) | 2,907 | 436 | 3,343 |
| gated collections if every form succeeds (section 3, estimates) | 6,666 | 1,000 | 7,666 |
| **everything in the census, volumes and segmentations** | | | **15,490** |

Segmentation output runs 8-20 % of the CT it came from (AbdomenAtlas 107 of 532 GB, IDC 55 of 658, TCIA 31 of 367, AMOS 13 of 96); 15 % is used for the estimates. The segmentations are the durable asset: with them on disk any better screen (reader E, a repaired counting rule) re-runs on CPU with no GPU cost, so the raw DICOM of a collection can be deleted once its NIfTI conversions and masks exist (IDC's raw DICOM is 658 GB for 3,500 series). The whole census fits the 20 TB volume only if the two chest-only gated sets (CT-RATE, INSPECT: T13 only, about 4 TB) are left out or fetched and deleted in batches, and NLST is refused as the plan says.

## Caveats

- Expected counts are priors times coverage probabilities, not observations; the screen's measured FOV gate already disagrees with the class prior where the collection is unusual (PENGWIN pelvic CT: 12 of 341 pass, the pelvis prior would give 40; NLST: 0 lumbosacral counts, as the plan stated).
- The screen finds fewer than the priors promise: on the 70 validation CTs with external labels, labeller A found 12 of 28 L6, labeller B 17 of 28, both together 9 (VALIDATION.md). Expected L6 in the tables is what is there, not what this screen will call; halve it for what the current two-labeller rule will confirm without a human.
- AbdomenAtlas overlaps FLARE and KiTS (repeats of one person); AMOS's unlabelled set has no patient ids; the dedupe job (alias_pairs_all.csv) is what counts people once.
- Sizes are du -sBG on the volume (raw = data/<collection>, seg = anomaly_harvest/<collection>/{seg,spineps}); the IDC and TCIA raw figures are DICOM, three to four times their NIfTI equivalents.
