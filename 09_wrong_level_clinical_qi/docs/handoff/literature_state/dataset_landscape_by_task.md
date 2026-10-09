# Topic 2: the dataset landscape by task, cross-referenced with the manifest

Written 2026-10-08 from files on this laptop only. No network was used and nothing a prior report recorded was re-checked:
every n, licence and result for a dataset or study that is not held is **as recorded in** the report cited beside it,
and those reports did their own verification (or say plainly that they did not). Where a report marks a lead
"searcher pass only" or "unverified", this note carries that label.

## How to read this note

**File key.** Paths without a prefix are relative to `<spinesurg-ct-nnunet 097933a>/`.
`ctsp:` is `<CTSpinoPelvic1K 7ddfe38>/`. `mem:` is the memory folder
`<the memory folder; copies in memory/ of this project, statuses in docs/handoff/context/INDEX.md>/`.

| code | file |
|---|---|
| MAN#id | `data_platform/DATA_MANIFEST.md`, the card with that id; its status word is the `status` field of `data_platform/sources.json` |
| MAN§4.n | `data_platform/DATA_MANIFEST.md` section 4, defect row n |
| RANK | `SchwingNet/results/transitional_registry/acquisition/ranking.csv` (146 rows) |
| ACQ | `SchwingNet/results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| JOIN | `ranking_joined.csv` in this note's parent folder: RANK joined row by row to `sources.json` statuses by `join_ranking.py` (same folder); every RANK row matched a manifest id |
| MISSED | `docs/research_datasets_missed_verified_2026-09-21.json` |
| THIRD | `docs/research_datasets_third_pass_verified_2026-09-21.json` |
| FOURTH | `docs/research_datasets_fourth_pass_verified_2026-09-22.json`; "FOURTH-s" = a candidate in its `round1_verified` list or coverage note with no verifier verdict ("searcher pass only") |
| PAIRED | `docs/research_paired_ct_projection_verified_2026-09-21.json` |
| CARM | `docs/research_carm_datasets_verified_2026-09-22.json` |
| VIDEO | `docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` |
| REQ | `docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` (and the drafts in `docs/fluoro_requests_eml/`) |
| SXS | `docs/data_requests/SX-Stitch_request.md` |
| STRAT | `docs/FLUORO_DATASET_STRATEGY.md` |
| PATH | `docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` and `docs/pathology_source_sweep_2026-09-14.json` |
| HUM | `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` |
| REGF | `docs/research_registration_free_search_2026-09-22.md` |
| COMP | `docs/COMPETITOR_BENCHMARK.md` |
| MORPH | `docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` |
| RARE | `research_notes/spine synthesis prior art/rare-variant.md` |
| SYN | `reports/Synthetic real ratio X-ray detectors.md` |
| DSH | `docs/DATASHEET.md` |
| T1 | `docs/RSNAI_TABLE1_DATASETS.md` |
| TIERS | `docs/ruleclass/TIERS.md` |
| REG | `SchwingNet/results/transitional_registry/REGISTRY.md` (built 2026-09-24) |
| SUBT | `SchwingNet/results/rare_class/transitional_subtypes.md` (built 2026-09-23) |
| COBSCR | `SchwingNet/results/power/inputs/cobra_lstv_screen.grid.md` |
| PWT | `SchwingNet/results/power_table.json` |
| PWR | `SchwingNet/results/power/power.json` |
| CLAIMS | `docs/RSNAI_CLAIMS.json` |
| ROAD | `ctsp:docs/DATASETS_ROADMAP.md` |
| MPDA | `ctsp:paper/mpda/main.tex` (the dataset article) |
| MLHC | `ctsp:MLHC_2026_Research_Track_Paper.pdf`, Table 1 |
| NEUR | `ctsp:3474_Not_All_Spines_Are_Create.pdf`, Table 1 |
| GEM | `ctsp:Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf`: an AI-generated summary that no verification pass checked |

**Status words.** HELD: the manifest cards it as on disk, with the on-disk n from the card. PARTIAL: held in part, and
the cell says what is missing. MISSING: the field's literature names it and the manifest does not hold it, with the
reason (gated behind a form or DUA; excluded by the acquisition rule, quoted; not yet fetched; never released or never
located; request drafted but not sent). SYNTHETIC: rendered or generated, not imaged.

**The acquisition rule**, quoted once so the MISSING cells can point at it (ACQ section 1): "A CT enters the ranking
only if all five hold: 1. Coverage can hold a count ... 2. Slices ≤ 3 mm ... 3. The licence allows derived labels.
CC BY, BY-SA, BY-NC and BY-NC-SA qualify. ND does not ... and neither does a DUA that forbids derivative works ...
4. The source names a person ... 5. A catalogue lists what the source holds." Rows that pass are fetched in order of
expected transitional people per TB, none below 20 per TB (ACQ section 3).

**The expectation arithmetic** the ranking uses (ACQ section 2): E = Σ over new people [P(both lumbosacral references
| coverage) × p_LSTV + P(cage from T1 | coverage) × p_T13], with p_LSTV 0.09 (E_low) to 0.18 (E_high), p_T13 0.0064
to 0.020, and E_count = what a mask count can call with no reader (p_count 0.048). These are expected values from
cited prevalences and measured field-of-view rates, not calls (ACQ, opening paragraph).

---

## 0. Short answer

| task | what is held (on-disk n) | the largest gaps the literature names | why they are missing |
|---|---|---|---|
| vertebra-labelled CT | every open, labelled release the prior research names: CTSpine1K 1,005, CTPelvic1K, VerSe 374 scans, TotalSegmentator v2 1,228 and v3 1,939 folders, RibFrac 660 with RibSeg v2 and the Möller masks, RSNA 2022 cervical 2,019, CSI 2014 20, and CTSpinoPelvic1K 802 (MAN#ctspine1k, #verse19_20, #totalsegmentator_v201, #totalsegmentator_v300, #ribfrac, #rsna_2022_cspine, #csi2014, #ctspinopelvic1k) | 10 VerSe'20 series; the open tier-2 spine collections (Spine-Mets-CT-SEG 54 new people, Spinal-Multiple-Myeloma-SEG 67, LumVBCanSeg 185, LUMOS 280); VERIDAH's 1,536-scan cohort; NMDID 15,243; Glocker 125 | never downloaded (MAN§4.9); planned, not fetched (JOIN); never released (MPDA line 277); licence (ACQ section 7) |
| CT with transitional anatomy | about 195 distinct transitional persons in today's table (SUBT; REG); tier-1 acquisitions fetched, 15,233 new CTs plus 3,365 late, expected 460 + 91 count anomalies (ACQ opening table) but not yet read | 7 gated collections: 70,764 new people, E_low 1,791, E_high 3,848, E_count 1,066; Merlin alone E_low 1,260, more than all of tier 1 (831) | gated behind a DUA or registration, none signed (ACQ section 7; JOIN) |
| plain films with level labels | CSXA 4,963, BUU-LSPINE 3,600 patients, NHANES II 17,073 films (543 landmarked), VinDr-SpineXR 10,466, AASCE 609, Mendeley 714, IEEE 236 (MAN family D) | TVGH-SpineXR (T1–L5 levels); LUMOS 1,620 radiographs; Kwak 2025's 3,116 LSTV-labelled films | login not done (MAN#tvgh_spinexr); deferred (MAN#zenodo_lumos); unreleased (mem:lstv-data-landscape.md) |
| intraoperative frames with 3-D truth or pose | C-ArmLSpine 149 cases (the only open intraoperative spine set with a paired volume that the passes found; whether its subjects were living is not stated), DeepFluoro 6 cadavers, Geneva phantom, Ljubljana cadaver, SpineSAC phantoms (MAN family C; VIDEO; FOURTH carmlspine_unknowns) | every labelled intraoperative set found on patients: Huashan 140 patients, LevelCheck 178 CTs / 398 radiographs, Vanderbilt 336 frames, SX-Stitch 1,032 frames, RadGS-Reg 10 cases (subject type not stated) | request-only or unreleased; SX-Stitch, Balgrist and 14 cine letters drafted, none recorded as sent (MAN#sx_stitch_request, #balgrist_exvivo_request, #fluoro_cine_requests_2026_09_26) |
| CBCT projections with a planning CT | COBRA2026 692 public cases, 375,618 projections; C-ArmLSpine's 2 raw sweeps (MAN#cobra2026, #carmlspine) | COBRA validation and test (175 cases, embargoed to 2032-03-01); TROG SPARK 48 patients; Jaganathan 55 thoracolumbar CBCT; Charters 527 patients | embargo; not fetched; unreleased; request (CARM; FOURTH; PAIRED) |
| synthetic rendering sources | all of the project's own banks (MAN family A render cards, #devcorpus, #fluorogen_synthetic, #polypose_synthetic) and Spinal-AI2024 | PENGWIN Task 2 50,000 renders; FluoroSAM's ~3M synthetic images; Huang 2022's 10,368 simulated long films; Barr 2026's 20,063 synthetic cervical radiographs | not fetched; none of them synthesises a transitional vertebra, and no published work does (RARE section 0) |
| spondylolisthesis and pathology films | VinDr-SpineXR (lesion boxes), BUU-LSPINE (a spondylolisthesis dataset), Mendeley 5jdfdgp762 (90 spondylolisthesis films), AASCE (scoliosis), RSNA 2022 cervical fracture CT | commercial brokers; MrOS/SOF; Radiopaedia and Eurorad teaching files | paid licence; DUA; site terms (PATH; REQ item 8) |

**Where this leaves size and power** (section 9 has the detail). The pre-stated claim needs 35 transitional test
persons with zero errors for a 90 % Wilson lower bound on exact level, and 22 for an 85 % bound on variant sensitivity
(PWR `n_needed_zero_errors`). The inventory the power table was built on held 89 transitional subjects, which gives
37 test persons at a 40 % test share or 46 under the plan's 50 % rule (PWT `inventory_today`); at 45 persons one error
already drops the bound to 88.43 % (PWT). The registry of 2026-09-24 holds more (146 L6, 14 T13 persons; REG table A),
and the fetched tier-1 CTs are expected to add about 550 count anomalies once read (ACQ opening paragraph). The
binding shortage is not CT people. It is labelled real intraoperative frames from living patients, where every set the
literature names is request-only, and T13, where the registry holds 14 persons.

---

## 1. Vertebra-labelled CT

n is as the source records it; for held sources it is the card's on-disk n.

| dataset | n | labels | access, licence | manifest status | source |
|---|---|---|---|---|---|
| CTSpinoPelvic1K (this project) | 802 CT + 802 label volumes | vertebrae C1–L6 from CTSpine1K radiologists; sacrum and hips; ribs (TotalSegmentator plus the Möller network, student-corrected); Castellvi two-reader consensus on 33; hardware read on 11 | open; labels CC BY-NC-SA 4.0; Zenodo v11 | HELD 802 (HF mirror still carries v10 labels, MAN§4.2) | MAN#ctspinopelvic1k |
| CTSpine1K | 1,005 volumes: COLONOG 784, MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31 | expert VerSe-convention masks C1–L6 + sacrum, T13 = 28 | open; CC BY-NC-SA 4.0 | HELD 1,005 (Ceph copy listed 2026-09-23; the HOME copy is presumed deleted, MAN§4.39) | MAN#ctspine1k |
| CTPelvic1K | 1,184 scans in 7 sub-datasets (MPDA table) | radiologist-supervised pelvic masks; no vertebra numbering | open; CC BY 4.0 or NC, quoted both ways (MAN§4.8) | PARTIAL: masks of datasets 1–5 (their images are CTSpinoPelvic1K or AbdomenAtlas people) plus the clinical datasets 6–7, 178 listed, 173 on disk, 172 converted | MAN#ctpelvic1k; MPDA lines 362, 448 |
| VerSe'19/'20 | 374 scans / 355 patients, 4,505 vertebrae (VerSe'19 160 series / 141 subjects; VerSe'20 319 series / 300 subjects); MLHC Table 1 gives 460 | expert vertebra masks C1–L6, T13 = 28; no sacrum; Castellvi table for 325 TUM subjects | open; CC BY-SA 4.0 or CC BY 4.0, quoted both ways | PARTIAL: 10 VerSe'20 series were never downloaded and their VerSe'19 copies were substituted silently | MAN#verse19_20; MAN§4.9 |
| VerSeFusion (project) | 374 unified scans | release masks; VERIDAH renumbering of 14 scans; ribs from TotalSegmentator (pseudo) | project | HELD | MAN#versefusion |
| TotalSegmentator v2 | 1,228 subjects, 117 masks each (MPDA cites the 1,204 of the first release) | model output refined by hand; no L6 or T13 class | open; CC BY 4.0 | HELD 1,228 | MAN#totalsegmentator_v201 |
| TotalSegmentator v3 | 1,939 folders, 1,935 distinct scans; 286 aged under 18 | as above, refined bone labels | open | HELD 1,935 (24 subjects alias v2 ids, MAN§4.11) | MAN#totalsegmentator_v300 |
| RibFrac with RibSeg v2 | 660 chest CTs; 661 RibSeg v2 rib masks | fracture labels; expert-corrected ribs 1–24 | RibFrac CC BY-NC 4.0 | HELD 660 | MAN#ribfrac |
| Möller et al. 2025 stump-rib masks | VerSe 323 + RibFrac 420 subjects; 133 of 648 (20.5 %) carry a stump rib; manual masks on 31 CTs | rib masks, stump rule ≤ 38 mm | open; CC BY 4.0; Zenodo 14864106 (ROAD gives 14850928) | HELD (fetched with the RibFrac download); adds no new subjects, all are VerSe subjects (mem:lstv-data-landscape.md) | MAN#ribfrac lines 2012, 2140; ROAD |
| RSNA 2022 cervical spine fracture | 2,019 train studies; 961 with a fracture, 1,444 fractures (PATH) | per-level C1–C7 fracture labels; 87 segmentations | Kaggle rules, non-commercial | HELD 2,019 | MAN#rsna_2022_cspine; PATH |
| CSI 2014 spine CT | 20 | vertebra masks (release); two-labeller screen | open; ODC-By | HELD 20 | MAN#csi2014 |
| Pelvic-Reference-Data (IDC) | 58 | none for vertebrae | open; CC BY 3.0 | HELD 58 | MAN#idc_pelvic_reference_data |
| PENGWIN 2026 pelvic fracture CT | 340 (308 after folding onto CTPelvic1K); MLHC lists PENGWIN at 150 | fragment masks; two-labeller screen | open; CC BY-NC-SA 4.0 | HELD 340 | MAN#pengwin2026; MLHC |
| VertebralBodiesCT-Labels (HF fhofmann) | 1,460 (ROAD) | numbered bodies T1–T13, L1–L6, S1 | CC BY-SA 4.0 (ROAD) | PARTIAL: only its `data.csv` external L6/T13 reads are used, on the 70 TotalSegmentator CTs of `validation_ts`; the masks have no card | MAN#totalsegmentator_v201 lines 1645–1649; MAN#validation_ts |
| CADS aggregate (HF mrmrx/CADS-dataset) | about 22k volumes (ROAD); 753 not reachable elsewhere (CT-TRI 586, VISCERAL 167) | whole-body derived | per component | MISSING: gated (registration checkbox; CT-TRI terms unread); the rest is carried by sources already held (ACQ section 1) | MAN#hf_cads_unique; ACQ section 7 |
| Spine-Mets-CT-SEG (TCIA) | 55 (MLHC); 54 new people (RANK) | per-vertebra DICOM SEG named by level (PATH) | open; CC BY 4.0 | MISSING: planned, tier 2, not fetched (rule 4 of ACQ section 3 holds tier 2 while more than 5,000 fetched CTs are unscreened) | MAN#idc_spine_mets_ct_seg; JOIN |
| Spinal-Multiple-Myeloma-SEG (TCIA) | 67 | segmentation | open; CC BY 4.0 | MISSING: planned, tier 2 | MAN#idc_spinal_multiple_myeloma_seg |
| LumVBCanSeg lumbar CT | 185 | not recorded | open; CC BY 4.0 | MISSING: planned, tier 2 | MAN#zenodo_lumvbcanseg |
| LUMOS lumbar CT | 280 CT of 803 patients | DXA values and vertebral dimensions; no masks (MISSED) | open; CC BY-NC 4.0; Zenodo 18173664 (MISSED) or 18173663 (RANK) | MISSING: planned, deferred: "needs a zipped-DICOM convert route" | MAN#zenodo_lumos; MISSED finding 0 |
| MedPelvis3D | 99 | not recorded | open; CC BY 4.0 | MISSING: planned, tier 2 | MAN#zenodo_medpelvis3d |
| VSDFullBody post-mortem whole-body CT | 100 new of 109 | not recorded | CC BY-NC-SA per the record | MISSING: planned, tier 2 | MAN#zenodo_vsd_fullbody |
| Glocker spine CT (SpineWeb 3) | 125 patients | vertebra centroids | CC BY-NC-ND 4.0 | MISSING: excluded by rule 3, "ND does not" qualify | MAN#excluded_glocker_spine; ACQ section 7 |
| NMDID post-mortem whole-body CT | 15,243 decedents | none; levels by counting (PATH) | custom DUA forbidding derivative works | MISSING: excluded by rule 3 ("a DUA that forbids derivative works") | MAN#excluded_nmdid; ACQ section 1 |
| VERIDAH in-house CT cohort | 1,536 scans | anomaly-aware labels L6, T13 | not released | MISSING: never released ("what exists is a capability, not a dataset") | MPDA line 277 |
| Schinz 2026 whole-thoracolumbar CT | 1,242 CTs | shape-based junction labelling | not recorded | MISSING: release not recorded | MPDA lines 342–344 |
| SPIDER; TotalSpineSeg | MRI 447; MRI 1,404 | vertebra masks | not recorded | out of scope (MRI), not sought | MLHC |

## 2. CT with transitional anatomy (L6, T13, Castellvi)

What is held is counted in persons, from the registry and the subtype table. What is missing is ranked in section 8 by
the plan's own expectation.

| dataset or stream | n (transitional) | labels and truth tier | access, licence | manifest status | source |
|---|---|---|---|---|---|
| VerSe'20 variant table (Loeffler et al., Sci Data 2021, Suppl. Table 1) | L6 in 85 scans, T13 in 6, cervical ribs 18, stump ribs 90, Castellvi IIa 35, IIb 25, IIIa 14, IIIb 28, IV 7; Castellvi I shares a cell with grade 0 (181 subjects) | two neuroradiologists in consensus; enriched by PACS report search, not a prevalence sample | CC BY 4.0 | HELD (merged into `~/lstv_sources/TRANSITIONAL_LABELS.csv`, 4,245 rows) | mem:lstv-data-landscape.md |
| The project registry, all sources | persons: L6 146 (140 CT-only, 6 with real frames), T13 14, fused sacralised L5 27, Castellvi I/II 31, lumbar rib 26, unassigned 62, unresolved 129 | read 103 + two-labeller 27 + single 9 + morphology 1 for CT-only L6; T13: read 6, two-labeller 3, single 5 | mixed | HELD | REG table A |
| The subtype table (one day earlier) | 194 persons: L6 110, T13 7, Castellvi I/II 31, lumbar rib 14, fused L5 28 | radiologist-read or release-label | mixed | HELD | SUBT; ACQ opening paragraph |
| CTSpinoPelvic1K transitional records | L6 18 persons (SUBT) or 29 (REG, a day later); three transitional counts in circulation, 31/33/34 | two-reader Castellvi on 33 | as the release | HELD | SUBT; REG table B; MAN§4.5 |
| TotalSegmentator with VertebralBodiesCT external reads | 7 of 1,088 scans marked T13 (the plan's p_T13 prior); registry L6 22, T13 4 persons | external read (L6 and T13) on 70 CTs plus two pseudo-labellers | CC BY 4.0 / CC BY-SA 4.0 | HELD (masks of VertebralBodiesCT not carded, section 1) | ACQ section 2; REG table B; MAN#validation_ts |
| COBRA2026 planning CTs, LSTV screen | 91 pseudo-calls of 692: L6 38, T13 45, four-lumbar 8; 257 unreadable (field cuts the lumbar set) | SPINEPS+VERIDAH on the deformed planning CT; "not a radiologist read" | CC BY-NC 4.0 | HELD; the registry counts 3 L6 at a tiered truth | COBSCR; REG table B |
| RibFrac / other CT stream | T13 4 single-labeller, L6 1 morphology-only | pseudo | CC BY-NC 4.0 | HELD | MAN#ribfrac line 2140 |
| Acquisition tier 1 (45 routes + the NLST pilot) | 15,233 new CTs; E_low / E_high 831 / 1,703; E_count 460 | two-labeller screen, unread; TIERS lists 2,332 flagged person keys (flags, not calls) | open | HELD (fetched 2026-09-23); AbdomenAtlas 7,649 of 9,262 usable as predicted; AMOS only 723 of 2,364 CTs ≤ 3 mm (rule 2), about a third of its predicted people | ACQ opening table and section 9; TIERS section 0 |
| Acquisition tier 1, late (10 collections) | 3,365 new CTs; E_low / E_high 163 / 336; E_count 91 | as above | open | PARTIAL: PANORAMA 2,024 CTs on disk with 1,114 still pending the screen; CURVAS 70 of 90 (training_set.zip unresolved); DEEP-PSMA 53 of 100; the rest within a few CTs of their listed n | ACQ opening table; MAN family B summary; TIERS section 1 |
| NLST pilot T13 measurement | 34 of 367 countable CTs called T13 by one labeller (9.3 %); 5 carry a rib head on that body | outside check against rib heads | open | HELD; the 9.3 % was found wrong and not believed | ACQ section 11 |
| Gated: Merlin, RATIC, CT-RATE, INSPECT, CADS unique parts, RSPECT, MAGIC-CT | 70,764 new people; E_low 1,791, E_high 3,848, E_count 1,066 | none | DUA or registration; none signed | MISSING: gated | ACQ section 7; JOIN |
| Tier 2 and deferred (23 rows, below) | 33,362 new people; E_low 337, E_high 834, E_count 246 | none | open | MISSING: planned, held by stopping rule 4 | JOIN; ACQ section 3 |
| Excluded by licence: NMDID, Glocker, CancerVerse, LNDb | NMDID 15,243; Glocker 125; LNDb 294; CancerVerse not recorded | | ND or derivative-forbidding DUA | MISSING: excluded by rule 3; "No form would fix that" | ACQ section 7 |
| Literature cohorts the priors come from | Hanhivaara 2020: 3,855 abdominal CTs, LSTV 29 %, Castellvi II–IV 32 % of it; Nardo 2012: 4,636 films, 18.1 %; Nagata 2025: 551 whole-spine CTs, 16.3 %; Sun 2025: 500 UK Biobank controls, L6 3.2 %, four lumbar 1.6 %, L1 ribs 2.0 % | published reads | release not recorded | not datasets the project can hold (release not recorded) | ACQ section 2 |
| Hanhivaara 2024 reader study | 100 LSTV cases, four blinded readers; radiography sensitivity 32 %, CT 76 % | reader study | not recorded | not recorded | mem:lstv-data-landscape.md |

## 3. Plain films with per-vertebra level labels (AP and lateral, cervical and lumbar)

| dataset | n | views, region | labels | access, licence | manifest status | source |
|---|---|---|---|---|---|---|
| CSXA Cervical Spine X-ray Atlas | 4,963 films | lateral, cervical | corner keypoints whose labels name C2–C7 | registration; CC BY 4.0 | HELD 4,963; all in the level bank | MAN#csxa_cervical_xray_atlas; DSH section 2.6 |
| BUU-LSPINE (Klinwichit 2023) | 3,600 patients, 7,200 films | AP + lateral, lumbar | end-plate lines L1–L5 + S1; **levels assigned by position**; L4L6 sheet: 129 four-lumbar, 15 six-lumbar | request form + EULA, "No License Provided" | HELD 7,200 (3,603 in the level bank; the 3,600 AP films in no level bank, MAN§4.31); plus the 2,000 and 400 subsets | MAN#buu_lspine_3600; DSH section 2.6; mem:anomaly-manifest-sources.md |
| NHANES II (CDC) | 17,075 index entries (9,667 cervical + 7,408 lumbar); 17,073 TIFF (2 are empty at the source) | lateral, cervical and lumbar | none released; 543 films landmarked (next row); pseudo-labels on 16,234 | public domain | HELD 17,073; 16,531 unlabelled | MAN#nhanes2_cdc_films; DSH section 2.6 |
| NHANES II landmarks (Zenodo, VertXNet) | 543 films (275 cervical + 268 lumbar) of 364 persons | lateral | per-level masks named C2–C7, T1, T11–T12, L1–L5, S1 | CC BY 4.0 | HELD 543 | MAN#nhanes2_zenodo_landmarks |
| VinDr-SpineXR | 10,466 images / 5,000 studies | AP + lateral, lumbar | 13 lesion classes, **no levels**; pseudo levels on 7,625 | PhysioNet credentialed DUA | HELD 10,466; 0 films in the reported level bank; test split consumed for pseudo-labels (MAN§4.30) | MAN#vindr_spinexr; DSH section 2.6 |
| AASCE 2019 / BoostNet | 609 labelled films (481 + 128) + 98 challenge test | AP, whole spine | 4 corners × 17 vertebrae, T1–L5 naming assumed | SpineWeb form / open mirror | HELD (grid copy 579 jpg; 128 BoostNet test films never reached the render bank, MAN§4.32) | MAN#aasce2019_boostnet |
| Mendeley 5jdfdgp762 "Spondylolisthesis Vertebral Landmark" | 714 films, 698 annotated, 3,250 boxes | lateral, lumbar | 4 corners per body, class-agnostic | CC BY 4.0 | HELD 714; about 500 are BUU persons (MAN§4.33) | MAN#mendeley_5jdfdgp762 |
| IEEE DataPort lateral full-spine | 236 films | lateral, whole spine | none; machine pseudo-labels | subscription | HELD 236 | MAN#ieee_dataport_lateral_fullspine_236 |
| TVGH-SpineXR (IEEE DataPort 10.21227/x6bb-7r75) | not recorded | diagnostic full-spine films | T1–L5 per-vertebra level labels, masks, end-plates (per the record, never seen) | login required | MISSING: not acquired (probe only, 2026-09-22) | MAN#tvgh_spinexr; FOURTH refuted_or_useless list |
| LUMOS radiographs | 1,620 lumbar AP or lateral films of 803 living patients; 280 with a CT within 6 months | AP or lateral, lumbar | DXA values and vertebral height and width; no boxes, no levels | open; CC BY-NC 4.0 | MISSING: planned, deferred (the card covers the CTs; the radiographs have no card of their own) | MAN#zenodo_lumos; MISSED findings 0–1 |
| Kwak, Ro, Kang, J Clin Med 2025 | 3,116 standing lateral lumbar films; 313 test | lateral, lumbar | LSTV text-mined from MRI reports, one reader; 62.3 % positive | "may be shared upon reasonable request" | MISSING: never released | mem:lstv-data-landscape.md |
| Sabri 2025 (Neurosurg Focus) | 3,147 full-length radiographs, 8.8 % transitional | full length | not recorded | not recorded | MISSING: release not recorded | mem:lstv-data-landscape.md |
| Sina University Hospital, Tehran | 300 living trauma patients, AP pelvic film + abdominopelvic CT | AP pelvis | not recorded | "without undue reservation" (request) | MISSING: request, not drafted | THIRD finding 7 |
| Osaka/NAIST hip cohort | 475 patients (305 with QCT); 77 EOS biplanar films 2-D/3-D registered | hip and pelvis | registration | request | MISSING: request, not drafted (searcher pass only) | FOURTH updates_to_known |
| TCIA same-patient films with CT (TCGA-CW-6088, TCGA-D1-A2G5, CMB-LCA MSB-09794; VAREPOP-APOLLO, TCGA-BLCA, COVID-19-AR, COVID-19-NY-SBU) | 8 films over 3 patients in the IDC pass; 27 COVID-19-NY-SBU patients with an abdominal film and an abdomen/pelvis CT | AP pelvis, abdomen | none | open | MISSING: not fetched; the census keeps one CT series per patient, and CR/DX/RF series are not CT | FOURTH updates_to_known; MISSED finding 10; ACQ section 1 |
| AI Hub (Korea) datasets 610, 611 | not recorded | not recorded | not stated | restricted to Korean nationals, secure zone | MISSING: not obtainable as constituted | FOURTH refuted_or_useless |
| Methods compared by re-implementation: Cina 2021, VertXNet 2024, Kim 2024, Konya 2021 | not recorded in these files | whole films | — | no code or weights released | their datasets: not recorded (VertXNet's landmarks are the NHANES set held above) | COMP; mem:xr-benchmark-and-robustness-2026-09-13.md |

## 4. Intraoperative fluoroscopy or C-arm frames with 3-D truth or pose

| dataset | n | device, subject | 3-D truth or pose; labels | access, licence | manifest status | source |
|---|---|---|---|---|---|---|
| C-ArmLSpine (Zenodo 22768651) | 149 cases: 299 spot frames (AP 149, lateral 149 incl. one repeat, oblique 1), 602 raw sweep projections, 149 CBCTs | FIRST Surgio-B51; intraoperative; living or cadaver not stated | CBCT per case; no labels, no pose ship; the project projects two-labeller levels through registered poses | open; CC BY 4.0 | HELD (the published numbers used the 296-frame pre-repair bank, MAN§4.20) | MAN#carmlspine; FOURTH carmlspine_expectations |
| DeepFluoro (Grupp 2020) | 6 cadaveric pelves, 366 frames (vendor deposit 2,659 DICOMs) | Siemens Cios Fusion | CT + pose per frame; 14 landmarks; 2-D segmentation | CC BY-NC 4.0 (T1 says BY-NC-SA) | HELD in three copies (H5, vendor, xvr-data HF) | MAN#deepfluoro_h5, #deepfluoro_vendor, #deepfluoro_xvr_hf |
| Geneva hip gold standard (D'Isidoro 2021) | one resin phantom; 116 frames over 19 views (CARM records 19 frames) | Philips BV Pulsera, image intensifier | CT + gold-standard rigid transforms + projection matrix | CC BY-SA 4.0 (paper says BY-NC) | HELD | MAN#geneva_hip; CARM finding 0 |
| Ljubljana 2D-3D-GS (Tomažević 2002) | one cadaveric L1–L5; 18 turntable radiographs | Trixell PIXIUM 4600, not a C-arm | per-vertebra CT and MR crops, fiducial gold standard | CC BY-NC-ND or a signed agreement | HELD | MAN#ljubljana_2d3d_gs; CARM |
| SpineSAC (IIT Madras) | 3 sawbone phantoms; 59 scenarios; 286 raw DICOM + 118 processed frames | 5 or 6 C-arms (GE FluoroStar, Skanray, Ziehm, Siemens Cios Select and an unnamed Siemens) | phantom CT + projection matrices; no vertebra labels | no data licence stated | HELD | MAN#spinesac; FOURTH new_confirmed |
| Bournemouth cervical QF tracks (BORDaR 385) | 63 people, 252 sequences | Siemens Arcadis Avantic, lateral cine | per-frame level-named corner tracks C0–T1; **no pixels** | CC BY 4.0 | HELD (tracks only); the DICOM cine is MISSING, request drafted not sent | MAN#bournemouth_qf_cervical_tracks; VIDEO; REQ item 1 |
| Public fluoroscopy clips | 1,269 clips (776 live) | mixed, YouTube and journals | none | mixed | HELD, unlabelled | MAN#fluoro_video_public_clips |
| FluoroCap literature harvest | 29,500 panels, manifest 21,603 rows; 72.8 % reproductions with no pixel residual | republished figures | caption labels only; human QC pending on every row | per-article licence tiers | HELD; dropped from training by directive D1 (MAN§4.35) | MAN#fluorocap; mem:fluorocap-is-reproductions-not-fluoroscopy.md |
| Huashan Hospital, Fudan (Shao 2024) | 140 living patients, preoperative CT + intraoperative AP and lateral films | device unnamed | none on the real films; pose would come from registration | request ([e-mail withheld]) | MISSING: request, not drafted | MISSED findings 2, 12 |
| LevelCheck clinical data (De Silva 2016; Ketcha 2017) | 178 CTs / 398 radiographs; 24 patients / 61 radiographs | mobile radiography (Carestream DRX-1 for Ketcha) | registration to labelled CT | DUA (GEM: "strictly available via a formal Data Use Agreement") | MISSING: DUA, no request drafted | HUM finding 3; MISSED finding 5; GEM |
| Manbachi 2018 reader set | 62 hard intraoperative radiographs (from a 398-radiograph set), 5 surgeons | mixed C-arm | neuroradiologist truth on CT | not recorded | MISSING: release not recorded | HUM finding 1 |
| Huang 2022 (JHU MVMS) cadaver long films | 13 cadavers, 100 labelled images (50 AP + 50 lateral) | O-arm multi-slot long film | level labels | unreleased; the Zenodo record 7161385 holds simulations only | MISSING: never released; request to Siewerdsen suggested | MISSED finding 3; HUM finding 5 |
| Otake 2013 JHU cadaver | 1 cadaver, 36 projections (72 CT-projection pairs), 19 targets C6–L5 | prototype Siemens flat panel | registration-derived pose | no release | MISSING: never released | MISSED finding 4 |
| FluoroSAM Loop-X torso (JHU) and Spine-DART | one cadaver; 464 lower-torso images in arXiv v1; Spine-DART 35 images | Brainlab / medPhoton Loop-X | navigated pose, stitched CBCT, TotalSegmentator masks projected | FluoroSAM no route; Spine-DART "will be made available ... without undue reservation" | MISSING: request, not drafted (Spine-DART searcher pass only) | THIRD finding 4; FOURTH updates_to_known |
| RadGS-Reg (Nanjing) | 10 intraoperative spine cases, CT + AP and lateral | device unnamed | recorded pose | no route | MISSING: never released | THIRD finding 6 |
| Vanderbilt THA fluoroscopy (Chan 2025) | 146 living patients; 336 landmarked frames incl. midline L5/S1 and SI joints | AP only, device not reported | landmarks | no route | MISSING: never released | THIRD finding 5 |
| SX-Stitch (PUMCH / SUSTech) | 1,032 intraoperative C-arm images in overlapping series | scoliosis surgery | vertebra masks | request | MISSING: **request drafted, not sent** | SXS; MAN#sx_stitch_request |
| PUMCH stitching series (Liu 2026) | 43 scoliosis patients, 4–6 overlapping AP shots each | Philips Zenition 70 | displacement estimated, not recorded | "No datasets were generated or analysed" | MISSING: never released; asking judged unlikely | VIDEO; REQ "Not drafted" |
| Balgrist ex-vivo lumbar (Jecklin 2024/2025) | 6 specimens, ≥ 50 X-rays each (Sci Rep); 13 + 6 specimens per the letter | Siemens Cios Spin, Ziehm Vision, Vision FD | fiducial projection matrices | withheld for pending patents; request | MISSING: **request drafted, not sent** | MAN#balgrist_exvivo_request; FOURTH updates_to_known |
| CM Spine | 208 intraoperative lumbar G-arm images | G-arm | vertebra detection labels | email request (Chinese Academy of Sciences, per GEM) | MISSING: a Google Drive download returned an empty folder; whether that file was CM Spine is recorded only by its name | MAN#cm_spine_drive_file; STRAT "Not worth acquiring"; GEM |
| SheepSpineX | 9 sheep cervical spines, about 270 AP/LAT pairs | Siemens Arcadis Varic | CT + projected centroids | request | MISSING: request, not drafted | MISSED finding 8; FOURTH |
| NIT Warangal / NIMS lumbar | not recorded (9 patients or 2, the passes disagree) | Ziehm C-arm, intraoperative AP/LAT | preoperative CT with L1–L5 centroids | images on request | MISSING (searcher pass only) | FOURTH-s |
| VerSeg-Net | 50 patients | Philips UNIQ FD20, lumbar fluoroscopy | per-level L1–S1 masks; explicit sharing statement | not recorded | MISSING (searcher pass only) | FOURTH coverage_note |
| FAU Surgical-Device-Detection | 38 real spine CBCT-sweep projections | not recorded | implant masks, calibrated matrices | open | MISSING: not fetched (searcher pass only) | FOURTH-s |
| UC Davis cadaver screw study | 6 cadavers, CT + intraoperative X-rays, 151 screws | not recorded | not recorded | request | MISSING (searcher pass only) | FOURTH-s |
| BG Klinik Ludwigshafen (MINTOS) | cadaver lumbar series | three Siemens Cios detectors | not recorded | request | MISSING (searcher pass only) | FOURTH-s |
| DKFZ / Siemens (Kausch 2022) | "large human cadaver study" | mobile C-arm | pose updates, landmarks | not recorded | MISSING (searcher pass only) | FOURTH-s |
| Manipal thoracolumbar | 4 adolescent trauma patients | Ziehm 9-inch image intensifier | CT with T11–L3 levels | not recorded | MISSING (searcher pass only) | FOURTH-s |
| PLA General Hospital pelvic fracture | 8 living patients, AP + inlet + CT | not recorded | 3-D points of interest | request | MISSING (searcher pass only) | FOURTH-s |
| Southeast University / Bond-Star | 15 spine CTs + real PA X-rays | Perlove PLX118F | not recorded | not recorded | MISSING (searcher pass only) | FOURTH-s |
| SJTU / TAOiMAGE biplanar lumbar | 64 or 50 subjects (passes disagree) | calibrated standing biplanar radiographs | registered CT | request | MISSING (searcher pass only) | FOURTH-s |
| DVAP-Reg SimReg / HybReg | contents unverified | not recorded | not recorded | promised, not deposited | MISSING: never released | MISSED finding 7 |
| DAX corpus (Siemens / FAU) | 632,385 intraoperative X-rays, about 124k spine | Siemens | none | "clinical images cannot be shared" | MISSING: never released | FOURTH refuted_or_useless |
| Rao et al., EMBC 2024 | 578 C-arm images, three commercial C-arms | patients, cadavers, phantoms | detection only, recall 0.964 / 0.982 | not recorded | MISSING: release not recorded | REGF; mem:registration-free-prior-art.md |
| VDVM (Zhang 2023) | 382 C-arm + 203 full-length films to train; 31 C-arm test | not recorded | segment matching to the preoperative radiograph, 73.3 % | not recorded | MISSING: release not recorded | REGF section 5.1 |
| TCIA CMB-MML / CMB-AML interventional frames | not recorded | Siemens AXIOM-Artis "FL SPINE", DynaCT | same-patient CT | open | PARTIAL: the CMB-MML CTs are held (16 series); the XA frames were not fetched (searcher pass only) | MAN#idc_cmb_mml; FOURTH-s |
| MIDRC fluoroscopy | RF 71 + XA 15 of 202,222 studies; about 17 C-arm studies of unknown anatomy | mostly bronchoscopy and swallow | none | registration | MISSING: not fetched | THIRD finding 8 |
| Veriserum (ETH) | about 110,990 frames, knee-implant phantoms | custom biplanar image intensifiers | per-frame pose; no CT | non-commercial | MISSING: not fetched; planned only as a statistics target | CARM finding 3; STRAT tier 3 |
| CAMS-Knee | 6 subjects with instrumented knee replacements | modified BV Pulsera | CAD-registered pose | signed institutional licence | MISSING: not requested | CARM finding 4 |
| Pelphix | 257 cadaver frames (phase labels only) plus simulated sequences | not recorded | no cadaver masks or landmarks | not recorded | MISSING: not fetched; withdrawn as a check | STRAT tier 4 |
| SyntheX LoopX test set | 60 images | Brainlab LoopX | landmarks | not recorded | MISSING: not recorded | STRAT tier 1 |
| Coronary angiography: CADICA, ARCADE, XCAD, AngioCAD | CADICA 42 patients; ARCADE 3,000 images; XCAD 1,747 images; AngioCAD 413 patients | thoracic spine in the background | none for the spine | open (no DUA, per STRAT) | MISSING: not fetched (STRAT tier 2 plan) | STRAT tier 2 |
| Pediatric IRI | 95,308 images, 1,357 sequences | abdominal angiography, lumbar spine in field | none | not recorded | MISSING: not fetched | STRAT tier 2 |
| MIQR-CC ERCP | 19,018 frames | Ziehm / Philips | no CT, no spine labels | figshare | MISSING: not fetched | FOURTH refuted_or_useless |
| Maastricht dynamic cervical | 112 recordings, 1024², 15 fps | three systems | per-frame contours C0–C7 | request | MISSING: **request drafted, not sent** | VIDEO; REQ item 2 |
| Bournemouth lumbar QF | 127 analysed adults, L2–S1, 15 fps | Siemens Arcadis Avantic | per-frame angles public (OSF a27py) | request | MISSING: **request drafted, not sent** | VIDEO; REQ item 1 |
| Pittsburgh swallow corpus | about 1,500 lateral clips (1,518 / 265 patients) | Toshiba Ultimax, GE | C2 and C4 corners every frame | request | MISSING: **request drafted, not sent** | VIDEO; REQ item 4 |
| Bern dynamic myelography | 4 videos (62-patient cohort asked about) | pulsed 7.5 f/s | none | CC BY 4.0 MP4s | PARTIAL: the MP4s are held; native DICOM request drafted, not sent | REQ item 3 |
| Other cine sources (Seattle Science Foundation, Mayfield, DMX, Radiopaedia 7 cases, Procedure Guide, Konica DDR, Jefferson, MTFI, Faubel, DARADIA) | per letter | mixed | none | per source | MISSING: **requests drafted, not sent**; Seattle and Radiopaedia addresses unverified | REQ checklist; MAN#fluoro_cine_requests_2026_09_26 |

## 5. CBCT projection sets with a planning CT

| dataset | n | device, anatomy | geometry and CT | access, licence | manifest status | source |
|---|---|---|---|---|---|---|
| COBRA2026 | 867 pelvic RT patients (692 train / 52 val / 123 test); 375,618 projections held | Elekta Synergy/VersaHD (A–D), Varian Halcyon/TrueBeam/VitalBeam (F–G); pelvis | RTK geometry per projection; deformably registered planning CT | training CC BY-NC 4.0; validation and test embargoed to 2032-03-01 | PARTIAL: 692 of 867 held; only 145 of 692 in any frame bank; Varian 225 not exported ("geometry not solved"); the Elekta device card fitted on 40 frames of 3 cases | MAN#cobra2026; MAN§4.25; CARM finding 1; mem:data-audit-99-gaps.md |
| C-ArmLSpine raw sweeps | 2 cases × 301 projections | Surgio-B51; lumbar | CBCT of the same sweep; angle tag updates every ~5 frames | CC BY 4.0 | HELD | MAN#carmlspine; FOURTH carmlspine_expectations |
| TROG 15.01 SPARK | 48 prostate SBRT patients, 5 centres, about 1.1M frames (~620k kV); 960 GB compressed | Varian TrueBeam, Trilogy; Elekta XVI; pelvis | planning CT; per-frame gantry angle; only setup sweeps are full field; L5 absent in every rendered frame | open; CC BY 4.0 | MISSING: not fetched | FOURTH new_confirmed |
| SPARE (Sydney) | not established: every content claim refuted 0–3 in CARM; PAIRED reads it as real kV projections with a prior 4D-CT | Elekta, Varian; thorax | per-projection matrices | CC BY-NC 4.0; 291 GB | MISSING: not fetched | PAIRED findings 3–4; CARM caveats |
| RTK public patient data (CLB 1–2, POPI) | 3 subjects, 1,976 Elekta XVI projections | thorax | planning CT, per-projection matrix | no data licence stated | MISSING: not fetched | FOURTH new_confirmed |
| CHIRP | not recorded | Varian TrueBeam; head | planning CT + CBCT | open | MISSING: not fetched (searcher pass only) | FOURTH-s |
| TCIA 4D-Lung raw projections | 20 patients, about 2,500 projections per scan | Varian OBI; thorax | projections by request only | CC BY 3.0 (volumes) | MISSING: request, not drafted | PAIRED finding 5 |
| Jaganathan / Maier (Siemens, FAU) | 55 living thoracolumbar CBCT volumes with their real projections | device not named | ground-truth pose from reconstruction geometry | unreleased | MISSING: never released | PAIRED finding 6 |
| Charters 2024 (UCLA) | 527 patients, 4,213 images (2,486 paired kV) | gantry-mounted kV and MV; thoracolumbar spine | DICOM REG to planning CT | request | MISSING: request, not drafted | PAIRED finding 7 |
| Petragallo 2023 ExacTrac | 429 spine RT patients, 1,592 fractions | ExacTrac stereo kV | planning CT | data statement unread; no deposit found | MISSING: never located (searcher pass only) | FOURTH updates_to_known |
| CHR Metz-Thionville | 8,717 triggered kV images, 49 patients | not recorded | not recorded | "institutional and regulatory restrictions" | MISSING: collaboration request only | FOURTH refuted_or_useless |
| ADAPT trial 4D-CBCT | not recorded | not recorded | projections not released | — | MISSING: never released | FOURTH refuted_or_useless |
| Phantom projection sets: Zhao pelvis phantom (figshare 5663446), Madesta 4D-CBCT phantom, AAPM MATCH, RabbitCT re-release (496 projections), Yaniv fiducial phantoms | per set | CIRS 801-P pelvis on Elekta XVI; thorax phantoms; rabbit | phantom CT or CBCT | open | MISSING: not fetched (searcher pass only, except Yaniv judged useless) | FOURTH-s; FOURTH refuted_or_useless |

## 6. Synthetic rendering sources

| source | n | what it is | access, licence | manifest status | source file |
|---|---|---|---|---|---|
| Project render banks | ctsp_drr 802; physics_drr 7,045 annotations; physics_rare 1,482; verse_drr 387 (13 duplicates); ts_drr 1,170; ts_drr_v3 1,735; anchor_drr 7,842; anchor_drr_c2 6,129; lstv_flag_renders 9,612; spinalai_drr 8,358; aasce_drr 457; xrspinopelvic1k 6,416 lateral DRRs | DRR banks from held CTs | project | SYNTHETIC, HELD (row-spacing defect on ctsp_drr before 2026-09-19 and on 181 VerSe soft renders, MAN§4.16) | MAN family A render cards; MAN#xrspinopelvic1k |
| devcorpus | 4,551 files; 142 TotalSegmentator subjects | device-styled renders | project | SYNTHETIC, HELD | MAN#devcorpus; DSH section 2.7 |
| implant_ct_synthetic | implant_verse 1,119; implant_ts 1,629; implant_ct 1,518 deleted | CTs with simulated hardware | project | SYNTHETIC, PARTIAL (one bank deleted) | MAN#implant_ct_synthetic |
| fluorogen_synthetic | 12,929 renders (L6 1,763, T13 86) over 2,844 cases | SDXL + ControlNet + LoRA restyling | project | SYNTHETIC, HELD | MAN#fluorogen_synthetic |
| polypose_synthetic | not recorded | polyrigid-warped CTs | project | SYNTHETIC, HELD | MAN#polypose_synthetic |
| Spinal-AI2024 | 20,000 images; 8,358 usable renders of 44 synthetic identities | synthetic AP films | not recorded | SYNTHETIC, HELD | MAN#spinal_ai2024; MAN§4.34 |
| PENGWIN Task 2 (Zenodo 10913196) | 50,000 DeepDRR renders from 100 of 150 CTs | pelvic fragments, simulated K-wires | open; CC BY 4.0 | SYNTHETIC, MISSING: not fetched (the PENGWIN 2026 CTs are held and can be rendered) | THIRD finding 3 |
| FluoroSAM fluoroseg (HF benjamindkilleen/fluoroseg) | about 3M synthetic images | synthetic | open (HF) | SYNTHETIC, MISSING: not fetched | THIRD finding 4 |
| Huang 2022 long films (Zenodo 7161385) | 10,368 simulated long films from 162 CTs | simulated O-arm long film | CC BY 4.0 | SYNTHETIC, MISSING: not fetched | MISSED finding 3 |
| BiSpineX | DRRs from 337 VerSe CTs | simulated biplanar | regenerable | SYNTHETIC, MISSING as files; regenerable from the held VerSe | MISSED finding 8 |
| SyntheX data (JHU Dataverse 2PGJQU) | not recorded | renders and real hip frames | not recorded | **not recorded**: MISSED calls it one the project "already has", but the manifest has no card for it | MISSED finding 6 |
| 2D3D-RegQuality (HF) | dataset_real 11.7 GB + simulated 21.7 GB | DeepFluoro real frames paired with DRRs at perturbed poses | MIT | MISSING: not fetched (searcher pass only) | FOURTH updates_to_known |
| HKU MedIP cbct_projection | 4 records | Monte Carlo CBCT projections from TCIA CTs | MIT | SYNTHETIC, MISSING: judged synthetic | FOURTH refuted_or_useless |
| Barr 2026 synthetic cervical radiographs | 20,063 images released | DDPM radiographs from 4,963 real lateral films, no labels | released | SYNTHETIC, MISSING: not fetched | MORPH row 10; SYN |
| Thoracolumbar SSM (Sci Data 2024) | 16,807 models, 694 GB | meshes only | CC BY 4.0 | SYNTHETIC, MISSING: rejected (85.3 % outside their own 95 % ellipsoid) | MORPH row 15 |
| AnyCXR | 2,982 CTs → 126,410 renders | chest renders | not recorded | SYNTHETIC, MISSING: release not recorded | MORPH row 2 |
| VICTRE; XCAT | 2,986 synthetic subjects (breast); XCAT by request | computational phantoms | FDA open source; request | MISSING: rejected for now | MORPH row 13 |
| MAISI / NV-Generate-CT | generator | 3-D CT + mask | MONAI Apache-2.0; NVIDIA weights licence unread | MISSING: rejected, to run once as a disproof | MORPH row 11 |
| Synthetic transitional vertebrae | none exists | "No published work has synthesised a transitional vertebra, an L6, a T13, a sacralised L5, or any numerical vertebral variant, in any modality" | — | — | RARE section 0 |

## 7. Spondylolisthesis and pathology films

| dataset or source | n | labels | access, licence | manifest status | source |
|---|---|---|---|---|---|
| VinDr-SpineXR | 10,466 / 5,000 studies | 13 lesion classes (fracture, spondylolisthesis, osteophytes, implants ...), no levels | PhysioNet DUA | HELD (no WSU IRB determination covers VinDr, MAN§4.30) | MAN#vindr_spinexr; PATH |
| BUU-LSPINE (a spondylolisthesis detection dataset) | 3,600 patients | end-plate lines; L4L6 sheet | EULA | HELD | MAN#buu_lspine_3600 |
| Mendeley 5jdfdgp762 | 714 films; 90 spondylolisthesis films, 33 naming the slipped level in the file name | class-agnostic corners | CC BY 4.0 | HELD | MAN#mendeley_5jdfdgp762 |
| `~/data/spondy_landmark` on HOME | 0 NIfTI; one directory | named "spondylolisthesis landmarks" in the CT inventory | not recorded | HELD but unidentified | MAN#spondy_landmark |
| AASCE 2019 (scoliosis) | 609 labelled | 68 landmarks | form / mirror | HELD | MAN#aasce2019_boostnet |
| RSNA 2022 cervical fracture CT | 2,019 studies | per-level fracture labels | Kaggle rules | HELD | MAN#rsna_2022_cspine |
| Spine-Mets-CT-SEG; Spinal-Multiple-Myeloma-SEG | 54; 67 new people | per-level SEG | CC BY 4.0 | MISSING: planned, tier 2 | JOIN |
| MrOS / SOF archives | not recorded ("UNVERIFIED") | vertebral fracture grade by level, if images are released | account + DUA | MISSING: DUA, not applied for; SOF has no CT | PATH; FOURTH refuted_or_useless |
| Commercial brokers: Segmed, Gradient Health, Shaip, InfoBay AI (AWS), Datarade / FileMarket, TrainingDataPro | not recorded | per vendor | paid commercial licence | MISSING: paid, not pursued | PATH |
| Roboflow Universe sets | 100–1,500 images each, quality uncontrolled | sometimes per-level classes | per set | MISSING: not fetched | PATH |
| ROCOv2 (HF); MedPix mirrors | not recorded | captions | CC BY-NC-SA (ROCOv2); mixed | MISSING: not fetched | PATH |
| Figure and teaching-file corpora (PMC Open Access, Europe PMC, Open-i, Radiopaedia, Eurorad, Wikimedia, J-STAGE, KoreaMed and the rest of the 366 sources) | 366 sources, 534 queries | captions name the level | per article or site | PARTIAL: harvested into FluoroCap through Europe PMC, Open-i (289 matched), MultiCaRe (67), Open-PMC-18M, Wikimedia (33) and video; Radiopaedia not scraped (its terms bar it), application letter drafted, not sent | PATH; mem:fluorocap-dataset.md; REQ item 8 |

---

## 8. The missing ones, ranked by what they would add

### 8a. CT, by the plan's own expectation (E_low; E_count is what a mask screen can call without a reader)

Every row is computed from RANK and joined to the manifest status in JOIN. Totals reproduce the plan's own table
(ACQ opening table, gated row: 70,764 / 1,791 / 3,848 / 1,066).

| rank by E_low | collection | status (reason) | new people | coverage | E_low | E_high | E_count | E_T13 low |
|---:|---|---|---:|---|---:|---:|---:|---:|
| 1 | Merlin abdominal CT (Stanford AIMI) | gated: AIMI research-use DUA | 18,317 | abdomen-pelvis | 1,259.9 | 2,522.3 | 673.0 | 2.1 |
| 2 | RSNA RATIC abdominal trauma | gated: MIRA or Kaggle registration, non-commercial, no redistribution | 3,147 | chest-abdomen-pelvis | 240.7 | 499.3 | 135.8 | 15.9 |
| 3 | NLST (beyond the 500 pilot) | planned, tier 2 (stopping rule 4) | 24,713 | screening chest | 111.4 | 345.9 | 110.5 | 109.4 |
| 4 | ENHANCE.PET (`scidb_enhance_pet_1_6k`) | planned, deferred: Science Data Bank route not scripted | 1,683 | whole body | 108.3 | 225.3 | 61.3 | 7.6 |
| 5 | CT-RATE | gated: HF gate form | 21,304 | screening chest | 94.9 | 296.6 | 94.9 | 94.9 |
| 6 | INSPECT | gated: AIMI DUA | 19,402 | screening chest | 86.4 | 270.1 | 86.4 | 86.4 |
| 7 | TotalSegmentator task data, liver lesions | planned: unresolved overlap with TotalSegmentator v2/v3 | 842 | abdomen | 60.6 | 121.2 | 32.3 | 0.0 |
| 8 | CADS unique parts (CT-TRI, VISCERAL) | gated: HF checkbox; component terms | 753 | whole body | 48.5 | 100.8 | 27.4 | 3.4 |
| 9 | RSNA-STR PE (RSPECT) | gated: Kaggle rules | 7,279 | chest | 32.4 | 101.3 | 32.4 | 32.4 |
| 10 | MAGIC-CT | gated: DUA needing proof of human-subjects training; "Only Greg can make that application" | 562 | chest-abdomen | 27.9 | 57.7 | 15.7 | 1.7 |
| 11 | STOIC2021 | planned, tier 2 | 2,000 | screening chest | 8.9 | 27.8 | 8.9 | 8.9 |
| 12 | LUMOS | planned, deferred: zipped-DICOM route | 280 | spine | 7.9 | 16.4 | 4.5 | 0.5 |
| 13 | LIDC-IDRI | planned, tier 2 | 997 | screening chest | 7.5 | 20.0 | 6.1 | 4.4 |
| 14 | VSDFullBody | planned, tier 2 | 100 | whole body | 6.4 | 13.4 | 3.6 | 0.5 |
| 15 | TotalSegmentator task data, pleural effusion | planned: unresolved overlap | 600 | chest | 5.5 | 14.1 | 4.2 | 2.7 |
| 16 | TMTV benchmark | planned, deferred: zipped-DICOM route | 60 | whole body | 3.9 | 8.0 | 2.2 | 0.3 |
| 17 | UniToChest | planned, tier 2 | 623 | chest | 2.8 | 8.7 | 2.8 | 2.8 |
| 18–29 | NSCLC-Radiogenomics 2.1; Spinal-Multiple-Myeloma-SEG 1.9; NSCLC-Radiomics 1.8; Spine-Mets-CT-SEG 1.6; Prostate-Anatomical-Edge-Cases 1.4; MedPelvis3D 1.1; LDCT-and-Projection 0.9; TS hip implant 0.8; CPTAC-LSCC 0.7; LumVBCanSeg 0.7; CPTAC-LUAD 0.6; MIDRC-RICORD-1B 0.6 | planned, tier 2 or unresolved overlap | 54–415 each | mixed | each ≤ 2.1 | | | |
| — | 58 rows excluded for "no new countable people" or licence | excluded | 260 in all | | 4.1 in all | | | |
| — | AbdomenAtlas Mini 2 (`hf_abdomenatlas2_0_mini`) | planned: unresolved overlap with the held AbdomenAtlas | 0 counted | | 0.0 | | | |

Partial holdings that would add people if completed, from the same arithmetic where the plan gives it:

- **COBRA2026 validation and test, 175 cases**: embargoed until 2032-03-01 (MAN#cobra2026). The plan gives no E for
  them; they are the only rows that would add transitional people with real projections.
- **PANORAMA, 1,114 CTs pending the screen** (TIERS section 0). Already counted inside the late tier-1 E of 163.
- **CT Colonography remainder, about 21–23 people** held back until CTSpinoPelvic1K tokens are matched to IDC PatientIDs
  (ACQ section 5; MAN line 430): E_low 1.5 (RANK rank 50).
- **AMOS, 1,564 CTs refused as thicker than 3 mm** (ACQ section 9). Rule 2 excludes them; they cannot be recovered
  without changing the rule.

What the ranking says in words: one form (Merlin) is worth more expected transitional people than everything fetched in
tier 1 (E_low 1,260 against 831; ACQ section 7). The T13 bin, which is the sparse one (14 persons, REG table A),
gains almost only from chest CT: NLST 109, CT-RATE 95, INSPECT 86, RSPECT 32 expected T13 people at the low prior
(JOIN column E_t13_low). The plan's fifth stopping clause already orders those first at equal yield (ACQ section 10).
The NLST pilot showed that a T13 rate from one labeller on screening chest CT can be five to fifteen times its prior
and wrong (ACQ section 11), so those expected T13 numbers rest on a second labeller that is blind on that field.

### 8b. Films, fluoroscopy and projections (the plan's arithmetic does not cover them)

The plan's expectation formula is written for CT only, and no file computes an expected transitional yield for a film
or fluoroscopy set. The order below is by the number of new **living** subjects with a level label or a pose on
**real** projections, as recorded, because labelled real intraoperative frames are the input the project has least of
(STRAT section (a); DSH section 2.1: "Only C-ArmLSpine is intraoperative human data").

| order | source | new subjects with level or pose truth on real frames (as recorded) | what blocks it | source file |
|---:|---|---|---|---|
| 1 | LevelCheck clinical cohort | 178 CTs, 398 intraoperative radiographs (+ Ketcha 24 patients) | DUA with the JHU PI; nothing drafted | HUM finding 3; MISSED finding 5 |
| 2 | Vanderbilt THA fluoroscopy | 146 patients, 336 frames with L5/S1 and SI-joint landmarks (AP only) | no route | THIRD finding 5 |
| 3 | Huashan (Fudan) | 140 patients, CT + intraoperative AP and lateral; levels projectable after registration | request; nothing drafted | MISSED finding 2 |
| 4 | Bournemouth lumbar QF cine | 127 adults, L2–S1 (angles public, pixels not) | request drafted, not sent | VIDEO; REQ item 1 |
| 5 | Pittsburgh swallow corpus | 265 patients + 70 volunteers; C2 and C4 only | request drafted, not sent | VIDEO; REQ item 4 |
| 6 | Bournemouth cervical QF DICOM | 63 people, 252 sequences with public C0–T1 tracks | request drafted, not sent | VIDEO; REQ item 1 |
| 7 | VerSeg-Net lumbar fluoroscopy | 50 patients, per-level L1–S1 masks | searcher pass only; route not recorded | FOURTH coverage_note |
| 8 | Maastricht cervical cine | 39 healthy + 23 patients, 112 recordings, C0–C7 contours | request drafted, not sent | VIDEO; REQ item 2 |
| 9 | SX-Stitch | 1,032 overlapping intraoperative images (patient count not recorded) with vertebra masks | request drafted, not sent | SXS |
| 10 | Jaganathan / FAU thoracolumbar CBCT | 55 patients, real projections with pose | unreleased | PAIRED finding 6 |
| 11 | TROG SPARK | 48 living patients, pelvic kV with planning CT (L5 absent in rendered frames) | not fetched; open | FOURTH new_confirmed |
| 12 | Cadaver and phantom sets: Huang 2022 (13 cadavers), Balgrist (6 to 19 specimens, request drafted), UC Davis (6), FluoroSAM / Spine-DART (1), RadGS-Reg (10 cases, subject type not stated, no route) | per row | per row | sections 4 and 5 |
| — | Film sets with levels: TVGH-SpineXR (n not recorded, login), Kwak 2025 (3,116 films, unreleased), LUMOS radiographs (803 patients, no level labels) | per row | per row | section 3 |

---

## 9. Size and power against the published studies

Our n is from the files named; every published n is as recorded in the cited report.

| question | our n | published comparators (as recorded) | source |
|---|---|---|---|
| transitional test persons needed for the pre-stated bound | 35 persons with 0 errors for a 90 % Wilson lower bound on exact level; 22 for 85 % on variant sensitivity | — | PWR `n_needed_zero_errors` |
| transitional test persons available | inventory 89 (VerSe 56, CTSpinoPelvic1K 18, TotalSegmentator 12, C-ArmLSpine real 3) → 37 test persons at 40 %, 46 at the 50 % rule; lower bound 90.59 % at 0 errors, 86.18 % at 1, 82.30 % at 2 | to hold 90 % with 1 error needs about 60 persons (91.14 %), with 3 errors about 100 (91.55 %) | PWT |
| transitional persons in the registry | L6 146, T13 14, fused L5 27, Castellvi I/II 31, lumbar rib 26 (2026-09-24) | VerSe table: L6 85 scans, T13 6; VERIDAH trained with about 60–83 real anomaly CTs and a 1,536-scan cohort; VerSe organisers: L6 became learnable with 85 distinct scans, T13 with 6 never stabilised | REG; mem:lstv-data-landscape.md; mem:synthetic-real-ratio-evidence.md; MPDA line 277 |
| a published naming accuracy stratified by anomalous spine | the project scores anomalous spines separately (for example L6 confirmation on 18 CTSpinoPelvic1K spines × 3 seeds) | none: "No verified study excluded transitional or anomalous spines, but none stratified by them" | CLAIMS `lstv_runs`; HUM finding 8 |
| naming on real intraoperative frames | C-ArmLSpine five-fold CV, lateral: 141 cases, 617 vertebrae, 98.2 % exact | VDVM 31 C-arm test images, 73.3 %; Huang 2022, 13 cadavers / 100 long-film images, 88.3 %; Manbachi 2018, 62 images, surgeons about 69.6 % unassisted; Rao 2024, 578 C-arm images, detection recall 0.964–0.982 with no naming | CLAIMS; REGF; HUM findings 1, 5 |
| naming on real plain film | held-out CSXA 3,720 vertebrae (99.87 %); BUU-LSPINE 2,698 vertebrae (98.04 %; levels by position) | Kwak 2025: 3,116 films, 313 test, LSTV accuracy 76.4 % against a surgeon's 83.9 %; Cina 2021 "98.4 %" is a whole-film presence vector, not metric-comparable | CLAIMS; mem:mixed-length-head-and-sota.md; mem:lstv-data-landscape.md |
| real frames per device | C-ArmLSpine 296–299 frames on one device; DeepFluoro 366 cadaver frames; the Elekta card fitted on 40 frames | returns on real labelled frames flatten between 300 and 700; no DRR paper swept the synthetic-to-real ratio | MAN§4.20; SYN; mem:data-audit-99-gaps.md |
| CT cohort size at the lumbosacral junction | CTSpinoPelvic1K 802 under one protocol | CTSpine1K 1,005; CTPelvic1K 1,184; VerSe 374; RibSeg v2 660; TotalSegmentator 1,204 (MPDA table); TotalSegmentator on CTSpinoPelvic1K: Any-LSTV 33 cases, junction Dice 0.534 against 0.824 on 768 normal | MPDA lines 361–366; NEUR Table 1 |

---

## 10. Disagreements found while cross-referencing

| item | one file says | another says | files |
|---|---|---|---|
| LUMOS Zenodo record | 18173664 | 18173663 | MISSED; RANK / MAN#zenodo_lumos |
| Möller stump-rib masks record | Zenodo 14864106 | Zenodo 14850928 | mem:lstv-data-landscape.md and MAN#ribfrac; ROAD |
| Geneva hip frames | 116 frames over 19 views | 19 frames | MAN#geneva_hip and T1; CARM finding 0 |
| VerSe size | 374 scans | 460 | MAN#verse19_20 and MPDA; MLHC Table 1 |
| TotalSegmentator size | 1,204 | 1,228 (v2) / 1,935 (v3) | MPDA and MLHC; MAN |
| PENGWIN size | 150 CT | 340 CT held | MLHC; MAN#pengwin2026 |
| CTSpinoPelvic1K L6 persons | 18 (2026-09-23) | 29 (2026-09-24) | SUBT; REG table B |
| SyntheX data 2PGJQU | "already has" | no card | MISSED finding 6; MAN |
| DeepFluoro licence | CC BY-NC 4.0 | CC BY-NC-SA 4.0 | MAN#deepfluoro_h5; T1 |
| COBRA2026 shape | "145 pelvic RT patients, four centres", Elekta only | 867 patients, six centres, two vendors | CARM question text (the older entry); CARM summary |
| Ljubljana set in xvr / DiffDRR | Tomažević spine gold standard | Mitrović cerebral angiography | PAIRED finding 9 |

## 11. The Desktop PDFs named in the brief

All sit in `ctsp:` (the CTSpinoPelvic1K-1 folder), not on the Desktop itself. Read only where a dataset question needed it.

| file | what it is | read? |
|---|---|---|
| COBRA.pdf | COBRA2026 dataset paper (Thummerer et al.), 26 pages | title only; the manifest card already carries its counts |
| AITR-2002-001.pdf | Zöllei, MIT AI Technical Report 2002-001, 2D-3D rigid registration of fluoroscopy and CT | title only |
| PANJABI_1991_FULL.pdf | Panjabi 1991, thoracic vertebral morphometry (Spine 16:888) | title only; not a dataset |
| 3474_Not_All_Spines_Are_Create.pdf | the NeurIPS submission auditing TotalSegmentator on LSTV | Table 1 read (section 9) |
| 2D-3D-GS_UG.pdf | Ljubljana 2D-3D-GS user's guide | title only |
| MLHC_2026_Research_Track_Paper.pdf | the CTSpinoPelvic1K MLHC preprint | Table 1 read (sections 1, 10) |
| Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf | an AI-generated landscape summary (Veriserum, DeepFluoro, CAMS-Knee, CM Spine 208, LevelCheck DUA, CTSpine1K / X23D) | read in full (2 pages); used only where a verified file agrees |
| `spinesurg-ct-nnunet/buu.pdf` | a 410-byte "Access Denied" page, not the BUU paper | MAN#buu_lspine_3600 |

---

## 12. Unknowns

| unknown | where it was looked for | why it matters |
|---|---|---|
| Whether any of the 14 fluoroscopy cine letters, the SX-Stitch request or the Balgrist request was ever sent | MAN#fluoro_cine_requests_2026_09_26, #sx_stitch_request, #balgrist_exvivo_request ("Sent: not recorded") | they are the only drafted routes to labelled real fluoroscopy |
| Whether the CM Spine set (208 G-arm images) is the empty Google Drive file | MAN#cm_spine_drive_file; STRAT; GEM | the only named intraoperative lumbar set with detection labels that was attempted |
| The size and label content of TVGH-SpineXR | MAN#tvgh_spinexr ("not recorded"); FOURTH | the one film set the passes name with T1–L5 level labels that is not held |
| Whether SyntheX's Dataverse deposit (2PGJQU) is on disk | MISSED finding 6 says held; the manifest has no card | decides whether a real-versus-render matched set is in hand |
| Whether the CT Colonography localizers (up to 754 patients) survive on HOME | MAN#tcia_ct_colonography is `on_disk_state_unknown`; THIRD finding 7; the census refuses "localizer image type" series | a free, same-patient projection source for 754 people |
| Whether the xvr-data copy on disk holds the Balgrist femur and cerebral Ljubljana sets as well as DeepFluoro | MAN#deepfluoro_xvr_hf (six subjects listed; file count "not recorded locally") | small; extremity and cerebral anatomy |
| The patient counts behind SX-Stitch, VDVM, Rao 2024 and the NIT Warangal set | SXS; REGF; FOURTH-s | ranking 8b orders by subjects; these are counted in images |
| The release status of Sabri 2025, Schinz 2026, Hanhivaara, Nardo, Nagata and Sun cohorts | mem:lstv-data-landscape.md; MPDA; ACQ section 2 | they size the field; none is recorded as obtainable |
| Whether the gated collections' expected yields hold | ACQ section 9 ("Whether the priors hold"); AMOS and NLST already missed their priors | Merlin's 1,260 is a prior, not a count |
| SPARE's true contents | CARM (all claims refuted 0–3); PAIRED (2-1 on the log-domain claim) | it is the only open thoracic CBCT set with a prior 4D-CT besides RTK's three subjects |
| What C-ArmLSpine's subjects are (living or cadaver), how many distinct people, and how PRSCS-Net derived pose | FOURTH carmlspine_unknowns | the project's only intraoperative human data and its main real-frame test |
| Which CTPelvic1K or VerSe licence reading is right | MAN§4.8 ("need Greg's reading") | decides the redistribution column of every derived bank |
| The current on-disk state of HOME entries after 2026-09-01 and Ceph after 2026-09-25 | MAN section 1 (census job 40578909 had not reported) | every HELD count in this note is the dated count its card gives |
| Whether the 23 unverified FOURTH candidates (FORCAST-EST, US-X, Robarts, CHIRP and others) exist as described | FOURTH coverage_note: "only four carry a visible verifier verdict" | several are open downloads that would add devices or phantoms |
