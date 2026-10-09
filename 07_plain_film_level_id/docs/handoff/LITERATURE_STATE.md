# State of the literature: what data you hold, what is missing, and where size and power stand

Written 2026-10-08 for Greg, from files on this laptop only (no network, no grid). It cross-references the data
manifest (`data_platform/DATA_MANIFEST.md`, `sources.json`) and the acquisition census with every prior research
report, verified dataset sweep, prior-art note, dataset review and power analysis found on disk. Nothing a prior report
recorded was checked again on the web: a published study's n or result is **as recorded in** the file named beside it,
and section 6 says how each of those files was verified (voted, read from source, or unverified).


## Status of the numbers quoted here (added 2026-10-08, after `RESULTS_CATALOG.md` was written)

This file and `literature_state/` were written before `RESULTS_CATALOG.md` marked superseded and leaked numbers.
**Where they differ, `RESULTS_CATALOG.md` wins.** The check made on 2026-10-08 searched this file and every file in
`literature_state/` for the numbers the catalog marks SUPERSEDED, [LEAK], [SEL-SPLIT] or RECORD ONLY; a key-by-key audit
of every `NUM` / `TAB3` / `CLM` citation was not done. What it found:

| number as quoted | where | status in `RESULTS_CATALOG.md` | use instead |
|---|---|---|---|
| C-ArmLSpine lateral 98.2 % (606 of 617), Wilson 94.6-99.4; AP zero-shot 37.9 % (239/631); 96.3 % (594/617) zero-shot; one in field 72.8 % (440/604) | the verdict below (corrected), `literature_state/topic3_size_relative_to_studies.md` L67, `literature_state/dataset_landscape_by_task.md` L368 | A3.11, A2.9: SUPERSEDED (v2 lineage, UNRESOLVED U1); `sn:tables/tab3_naming.md` is a stale twin | 601 of 617 (97.4 %), Wilson on effective n [93.2, 99.0] (A3.1); zero-shot 595/617 (96.4 %) and AP 276/631 (43.7 %) (A2.1-A2.2); one in field 451/603 (74.8 %) (A3.3) |
| whole-film 99.96 % = the count-from-sacrum rule | the verdict below | C1.16: RECORD ONLY (measured on v2) | no current whole-film number |
| CSXA 99.87 % of 3,720; BUU 98.04 % of 2,698; BUU band3 94.89 % | `literature_state/topic3_size_relative_to_studies.md` L46, `dataset_landscape_by_task.md` L369 | C1.6: computed on allspine v2, in `sn:NUMBERS.md` "Numbers deliberately absent" | held-out film persons from the film N-curve: CSXA 99.8 %, BUU 96.9 %, NHANES 92.7 % at every person (A10.1-A10.3); the a5 numbers (CSXA 99.8, BUU 97.3, NHANES 99.1 %) are on the selection split (A15, CURRENT-SEL) |
| anomalous film interior 66.0 % (12 films), ordinary 91.8 %; anomalous 49.9 % (128 films), ordinary 89.9 % | power sentence below, `literature_state/power.md` row 6 and §6, `topic3_size_relative_to_studies.md` L46, L81 | C1.14: RECORD ONLY [LEAK] (v2 / v6) | none: no held-out transitional film number exists |
| L6 named 44.9 % (no anchor, "State C") | power sentence below, `power.md` row 6 and §6, `topic3_size_relative_to_studies.md` L81 | C1.18: SUPERSEDED (two-mechanisms table, v2 lineage) | none |
| render L6 recall 56.1-72.4 % on 10 held-out L6 spines | `power.md` row 6 and §6 | [SEL-SPLIT]: the v9 encoder kept its best epoch on the split these spines belong to (`sn:results/eval_gate/EVAL_LEAKS.md` item 6) | quote only with that mark |
| 9,108 films | the verdict below | A18.2: 9,108 counts the 542 NHANES films that carry landmarks; `~/films_drr` holds 9,109 annotation files (`ssn:docs/DATASHEET.md` L165) | either, with what it counts |

## Lead

You hold the large open, vertebra-labelled spine CT releases the prior research names: CTSpine1K 1,005 volumes, VerSe
374 scans, TotalSegmentator 1,228 and 1,935 scans, RibFrac 660, RSNA 2022 cervical 2,019, and your own CTSpinoPelvic1K
802 (MAN section 1). The exceptions are small or blocked. Ten VerSe'20 series were never downloaded (MAN§4.9).
Spine-Mets-CT-SEG (54 new people), Spinal-Multiple-Myeloma-SEG (67), LumVBCanSeg (185 lumbar CTs) and MedPelvis3D (99)
are planned for tier 2 and held back by stopping rule 4. The LUMOS CTs (280) are deferred until a zipped-DICOM route is
written. The Glocker spine CT (125 patients, 242 scans) is excluded by its ND licence under rule 3. The
VertebralBodiesCT-Labels masks (1,460) are held only as reads on 70 CTs and have no card (JOIN ranks 54, 75, 82, 84, 86,
128; MAN#totalsegmentator_v201; section 2, B11 to B13).

Beyond those you hold the CTs that tier 1 of the acquisition plan fetched for the transitional screen (15,233 and 3,365
late additions, people at most), which no one has read; 9,108 level-labelled real plain films; and exactly one real
intraoperative human set with a volume, C-ArmLSpine (149 cases, one C-arm model) (ACQ opening table; CORP note j; DSH
section 2.1).

What is missing that matters most is labelled real intraoperative frames from living patients. Every verified set of
that kind the literature names is request-only or unreleased: LevelCheck's 178 CTs and 398 radiographs, Vanderbilt's 146
patients, Huashan's 140, PUMCH's 43 and SX-Stitch's 1,032 frames among them (section 2, A1 to A21). The one partial
exception is NIT Warangal (9 patients, A10), whose level-named centroid files are public and whose real frames are
public only as 8-bit copies inside overlay images. No drafted request is recorded as sent. One open interventional set
with same-patient CT has not been fetched: the TCIA CMB-MML and CMB-AML XA frames, which the fourth sweep partly
confirmed, but only one patient's frames show a spine procedure and none carry labels (FOURTH r1 6; section 2, A6). The
other gap is seven gated CT collections nobody has signed for, of which Merlin alone is expected to add more
transitional people (E_low 1,260) than all of tier 1 (831) (N2 section 8b; MAN#sx_stitch_request; ACQ section 7).

In size, you are larger than every published radiograph naming study and every C-arm naming study whose n is recorded
(9,108 films against VertXNet's 1,183 images; 296 C-arm frames against VDVM's 31). You are smaller than LevelCheck's
registration cohort (296 frames from 148 cases against 398 radiographs from 178 patients). You are comparable on CT (802
patients against VERIDAH's 1,536), and smaller on 2-D LSTV (147 real 2-D transitional positives against Kwak's 1,941)
and on human readers (no reader study against Manbachi's 5 surgeons) (N3; section 3).

In power, the pre-stated transitional claim needs 35 test persons named without error (PJ). You have 0 verified
real-frame transitional test persons and 7 unverified ones (RES; NUM:435). The CT side has 51 at-risk test persons, but
92 of the 97 transitional persons on the validation and test sides sit in the training data of the current encoder
(NUM:436; TAB2 note d). Every power figure so far assumes a true accuracy of 95 to 99 %, and no transitional
measurement supports it: render L6 recall is 56.1 to 72.4 % (RS2 N1; LCM section 8).

## How to read this file

**File key.** Roots: `ssn:` = `<repo:spinesurg-ct-nnunet 097933a>/`; `ctsp:` =
`<repo:CTSpinoPelvic1K 7ddfe38>/`; `mem:` =
`<live memory folder; HANDOFF/context/ holds the copies>/`; `LS:` =
`ssn:HANDOFF/literature_state/`, which holds the four working notes this file summarises and the scripts behind every
number marked **calc** or **calc_review** (copied there from the session scratchpad so the citations survive it).

| code | file |
|---|---|
| MAN#id, MAN section n, MAN§4.n | `ssn:data_platform/DATA_MANIFEST.md`: the card with that id; section n; section 4 defect row n |
| SRC | `ssn:data_platform/sources.json` (status field per source) |
| RANK | `ssn:SchwingNet/results/transitional_registry/acquisition/ranking.csv` (146 rows) |
| ACQ | `ssn:SchwingNet/results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| FOV | `ssn:SchwingNet/results/transitional_registry/acquisition/fov_calibration.json` |
| JOIN | `LS:ranking_joined.csv`, RANK joined to SRC statuses by `LS:join_ranking.py` |
| CEN | `ssn:docs/CENSUS_TABLE_2026-09-25.md` |
| TIERS | `ssn:docs/ruleclass/TIERS.md` |
| REG | `ssn:SchwingNet/results/transitional_registry/REGISTRY.md` (built 2026-09-24) |
| SUBT | `ssn:SchwingNet/results/rare_class/transitional_subtypes.md` (built 2026-09-23) |
| POS | `ssn:SchwingNet/lit/ct_lstv_classifier/positives_census.md` |
| COBS | `ssn:SchwingNet/results/power/inputs/cobra_lstv_screen.grid.md` |
| MISSED | `ssn:docs/research_datasets_missed_verified_2026-09-21.json` |
| THIRD | `ssn:docs/research_datasets_third_pass_verified_2026-09-21.json` |
| FOURTH; FOURTH r1 n, r2 n | `ssn:docs/research_datasets_fourth_pass_verified_2026-09-22.json`. "r1 n" is item n of its `round1_verified` list (30 candidates) and "r2 n" item n of `round2.verified` (28); each carries two verifier verdicts, quoted as, for example, "partly confirmed twice". "Searcher pass only" is kept for a candidate the file names with no verdict at all (VerSeg-Net, in the coverage note) |
| PAIRED | `ssn:docs/research_paired_ct_projection_verified_2026-09-21.json` |
| CARM | `ssn:docs/research_carm_datasets_verified_2026-09-22.json` |
| RF18 | `ssn:docs/research_registration_free_2026-09-18.json` |
| RF22 | `ssn:docs/research_registration_free_search_2026-09-22.md` |
| VIDEO | `ssn:docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` |
| REQ | `ssn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`; the ready drafts are `ssn:docs/fluoro_requests_eml/NN_source.eml` |
| SXS | `ssn:docs/data_requests/SX-Stitch_request.md` |
| BALG | `ssn:docs/outreach/balgrist_data_request_2026-09-21.md` |
| STRAT | `ssn:docs/FLUORO_DATASET_STRATEGY.md` |
| PATH | `ssn:docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` and `ssn:docs/pathology_source_sweep_2026-09-14.json` |
| HAI | `ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` |
| XR | `ssn:docs/PRIOR_ART_LEVEL_ID_XRAY.md` |
| COMP | `ssn:docs/COMPETITOR_BENCHMARK.md` |
| MORPH | `ssn:docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` |
| RARE | `ssn:research_notes/spine synthesis prior art/rare-variant.md` |
| SYN | `ssn:reports/Synthetic real ratio X-ray detectors.md` (deep research "Synthetic", 2026-09-23) |
| DSH | `ssn:docs/DATASHEET.md` |
| T1 | `ssn:docs/RSNAI_TABLE1_DATASETS.md` |
| CLM | `ssn:docs/RSNAI_CLAIMS.json` (claim id given) |
| LED | `ssn:SchwingNet/CLAIMS_LEDGER.md` |
| CORP | `ssn:SchwingNet/tables/tab_corpus.md` (manuscript Table 1) |
| TAB2 | `ssn:SchwingNet/tables/tab4_transitional.md` (manuscript Table 2, transitional persons) |
| TAB3 | `ssn:SchwingNet/tables/tab3_naming.md` (manuscript Table 3) |
| RES | `ssn:SchwingNet/sections/results.tex` |
| AUTO, PREV, TLJ, CORR | `ssn:SchwingNet/lit/ct_lstv_classifier/` `lit_ct_lstv_automation.md`, `lit_prevalence_and_definitions.md`, `lit_tl_junction_and_enumeration.md`, `CORRECTIONS.md` (the corrections apply to the other three) |
| PJ | `ssn:SchwingNet/results/power/power.json` (Figure 5) |
| PT | `ssn:SchwingNet/results/power_table.json` |
| SR1, SR2 | `ssn:SchwingNet/results/stats_review/recompute.json`, `ssn:SchwingNet/results/stats_review2/recompute.json` |
| RS1, RS2 | `ssn:SchwingNet/REVIEW_STATS.md`, `ssn:SchwingNet/REVIEW2_STATS.md` |
| LCM | `ssn:SchwingNet/LEVELCHECK_MODEL.md` (the frozen paper-2 comparator) |
| NUM:n | `ssn:SchwingNet/NUMBERS.md`, line n |
| FITN | `ssn:SchwingNet/results/indomain/FIT_N.md` |
| ABL | `ssn:SchwingNet/results/coverage/film_ncurve/ablation/READ.md` |
| FP | `ssn:docs/FLAGSHIP_PLAN.md` |
| GATE | `ssn:SchwingNet/paper2_levelcheck/open_gate_40438004/README.md` |
| RES22 | `ssn:docs/RESUME_2026-09-22_PM.md` |
| RSN2 | `ssn:paper/rsnai/main_v2.tex`, the concise RSNA AI draft of 2026-09-22, with its numbers as macros in `ssn:paper/rsnai/claims.tex` (it is not under `SchwingNet/paper/`). The current manuscript is `ssn:SchwingNet/sections/*.tex` (`results.tex` last committed 2026-09-25), and a grep finds neither RSN2 count used here in it: the counts were dropped from the manuscript, not replaced by other values |
| MPDA | `ctsp:paper/mpda/main.tex` (the dataset article) |
| NIPS | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.tex` |
| MLHC | `ctsp:MLHC_2026_Research_Track_Paper.pdf`, Table 1 |
| ROAD | `ctsp:docs/DATASETS_ROADMAP.md` |
| GEM | `ctsp:Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf` (AI-generated, never verified; used only where a verified file agrees) |
| N1 | `LS:topic1_bibliography.md` (every research file on disk, 114 rows; section letters and row numbers given) |
| N2 | `LS:dataset_landscape_by_task.md` (the landscape by task, cross-referenced with the manifest). Its "FOURTH-s" (no verdict) label is wrong for every item it is applied to, since each sits in FOURTH's verdict lists with two verdicts; section 2 gives those verdicts and carries every one of its MISSING rows |
| N3 | `LS:topic3_size_relative_to_studies.md` (size against published studies) |
| N4 | `LS:power.md` (the power calculations its grep found, and the arithmetic applied to today's n; section 4 names the directories it searched and adds what a wider grep found) |
| calc | `LS:power_calc.py` (output `LS:power_calc.json`), `LS:calc_addendum.py` (output `LS:calc_addendum.json`), `LS:t3_ratios.py`: the repository's own formulas (LCM section 11 exact binomial; `ssn:tools/stats_compare.py` two-proportion) applied to today's n |
| calc_review | `LS:calc_review.py` (output `LS:calc_review.json`): arithmetic added on review: the VERIDAH test-set inferences, ratios on 51 and 57 test persons, the CTSpinoPelvic1K read-tier L6 interval, the countable-people sums and the tier-2 reconciliation |
| mem:name | the memory note of that name |

**Status words.** HELD: the manifest cards it as on disk, with the card's on-disk n. PARTIAL: held in part; the cell says
what is missing. MISSING: the field's literature names it and the manifest does not hold it. SYNTHETIC: rendered or
generated, not imaged.

**Other conventions.** Every held count is the dated count its card gives; the storage census of 2026-10-07 (Slurm job
40578909) had not reported when the manifest was written (MAN section 1). Licences are written without their version
number; each card gives the full name. Ratios are your n divided by the study's n, and compare size only: no two systems
in this space report the same quantity (COMP; RF18 finding 15), so headline results sit side by side and are not a
ranking.

---

## 1. What I have

The manifest lists 211 sources (a 212th card, `spondy_landmark`, turned out to be a second copy of Mendeley 5jdfdgp762
and was merged into it): 115 on disk, 23 planned, 7 gated, 58 excluded, and 8 other (Hugging Face only 1, laptop only 1,
deleted 1, empty 1, not acquired 1, requests drafted and not sent 3) (MAN section 1). By family: A, the CT releases and
their banks, 30 (29 on disk); B, the anomaly-harvest CT acquisitions, 144 (56 on disk); C, real X-ray and fluoroscopy with
3-D truth or pose, 12 (12); D, plain film and harvested 2-D, 24 (17); E, the disk map, 1 (MAN section 1).

### 1.1 Vertebra-labelled CT

| dataset | held n | labels | licence, access | card |
|---|---|---|---|---|
| CTSpinoPelvic1K (yours) | 802 records, one per patient, and 802 label volumes (MAN; MPDA lines 226, 435, 801); 1,153 distinct spine and pelvic series UIDs across those records (MAN#ctspinopelvic1k, citing MANSUM). The NeurIPS paper used the April release of 1,153 records over 802 patients (NIPS lines 90 to 91, 194) and scored 1,152 records of 801 patients (NIPS lines 299 to 301) | vertebrae C1 to L6 from CTSpine1K radiologists; sacrum, hips, femora; ribs (TotalSegmentator plus the Möller network, student-corrected); Castellvi two-reader consensus on 33 | open; labels CC BY-NC-SA; Zenodo v11. HELD; the Hugging Face mirror still carries v10 labels (MAN§4.2) | MAN#ctspinopelvic1k |
| TCIA CT COLONOGRAPHY | 825 patients, 3,451 series | none (the CT behind CTSpinoPelvic1K) | open | MAN#tcia_ct_colonography (HOME state unknown) |
| CTSpine1K | 1,005 volumes (COLONOG 784, MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31) | expert VerSe-convention masks C1 to L6 and sacrum | open; CC BY-NC-SA. HELD on Ceph; HOME copy presumed deleted (MAN§4.39) | MAN#ctspine1k |
| CTPelvic1K | 1,184 scans in 7 sub-datasets (MPDA) | radiologist-supervised pelvic masks; no vertebra numbering | open; CC BY or BY-NC, quoted both ways (MAN§4.8). PARTIAL: masks of datasets 1 to 5 plus clinical datasets 6 and 7 (178 listed, 173 on disk, 172 converted) | MAN#ctpelvic1k |
| VerSe'19 and '20 | 374 scans of 355 patients, 4,505 vertebrae | expert masks C1 to L6, T13 = 28; no sacrum | open; CC BY-SA or CC BY, quoted both ways. PARTIAL: 10 VerSe'20 series never downloaded, VerSe'19 copies substituted silently (MAN§4.9) | MAN#verse19_20 |
| VerSeFusion (project) | 374 unified scans | release masks; VERIDAH renumbering of 14 scans; pseudo ribs | project. HELD | MAN#versefusion |
| TotalSegmentator v2 | 1,228 subjects | 117 masks each; no L6 or T13 class | open; CC BY. HELD | MAN#totalsegmentator_v201 |
| TotalSegmentator v3 | 1,939 folders, 1,935 distinct scans (286 under 18) | refined bone labels | open. HELD; 24 subjects alias v2 ids (MAN§4.11) | MAN#totalsegmentator_v300 |
| RibFrac with RibSeg v2 | 660 chest CTs; 661 rib masks | fracture labels; ribs 1 to 24 | CC BY-NC. HELD | MAN#ribfrac |
| Möller 2025 stump-rib masks | VerSe 323 + RibFrac 420 public subjects (743); final analysis set 648, of whom 133 carry a stump rib (AUTO C3; why 95 were left out is not recorded, section 7.2) | rib masks | CC BY; one Zenodo record, concept DOI 14850928 with its single version 14864106 (CORR). HELD; adds no new subjects | MAN#ribfrac; mem:lstv-data-landscape.md; CORR |
| RSNA 2022 cervical fracture | 2,019 studies; 961 with a fracture | per-level C1 to C7 fracture labels; 87 segmentations | Kaggle rules, non-commercial. HELD | MAN#rsna_2022_cspine; PATH |
| CSI 2014 spine CT | 20 | vertebra masks | ODC-By. HELD | MAN#csi2014 |
| PENGWIN 2026 pelvic fracture CT | 340 (308 after folding onto CTPelvic1K) | fragment masks | CC BY-NC-SA. HELD | MAN#pengwin2026 |
| Pelvic-Reference-Data (IDC) | 58 | none for vertebrae | CC BY. HELD | MAN#idc_pelvic_reference_data |
| VertebralBodiesCT-Labels (HF) | 1,460 (ROAD) | numbered bodies T1 to T13, L1 to L6, S1 | CC BY-SA. PARTIAL: only its external L6 and T13 reads on 70 TotalSegmentator CTs are used; the masks have no card | MAN#totalsegmentator_v201; MAN#validation_ts |

### 1.2 CT with transitional anatomy (persons), and the CT fetched to find more

| dataset or stream | held n | labels and truth tier | licence | card or file |
|---|---|---|---|---|
| VerSe'20 variant table (Loeffler 2021, Suppl. Table 1) | L6 in 85 scans, T13 in 6, cervical ribs 18, stump ribs 90; Castellvi IIa 35, IIb 25, IIIa 14, IIIb 28, IV 7 (II to IV = 109) | two neuroradiologists in consensus; enriched by report search, not a prevalence sample | CC BY | mem:lstv-data-landscape.md; CORR |
| The transitional registry, all streams (2026-09-24) | 306 positive persons of 6,108: L6 146 (140 CT-only, 6 with real frames), T13 14, sacralised L5 fused 27, Castellvi I/II 31, lumbar rib 26, unassigned 62; a further 129 unresolved | CT-only L6: read 103, two-labeller 27, single 9, morphology 1; T13: read 6, two-labeller 3, single 5 | mixed | REG table A; POS |
| Manuscript Table 2 (2026-09-23) | 194 persons (CTSpinoPelvic1K 52, VerSe 135, TotalSegmentator 4, C-ArmLSpine 3): L6 110, T13 7, sacralised L5 28, Castellvi I/II 31, lumbar rib 14, unassigned 4 | CTSpinoPelvic1K two-reader or release label; VerSe published read; TotalSegmentator rib count; C-ArmLSpine one automatic labeller | mixed | TAB2 |
| Read-tier persons only | 202 (CTSpinoPelvic1K 33, VerSe 166, CTSpine1K MSD-T10 3) | a radiologist's read | mixed | POS |
| CTSpinoPelvic1K transitional records | L6 in 18 records by release label (MPDA; SUBT), 16 by the readers' own count (CORR: seven records disagree and stay out of every lumbosacral truth pool until re-read; read-tier pools LS-L6 16, LS-SAC 9, LS-II 1), or 29 persons (REG table B, one day later); Castellvi-graded 33, 34 or 39 depending on the file | two-reader Castellvi consensus | as the release | N1 section I; REG; CORR |
| TotalSegmentator with outside reads | registry L6 22, T13 4 persons; 7 T13 of 1,088 scans (the plan's T13 prior) | outside read on 70 CTs plus two pseudo-labellers | CC BY / CC BY-SA | REG table B; ACQ section 2 |
| COBRA2026 planning-CT screen | 91 calls of 692 (L6 38, T13 45, four-lumbar 8); 257 unreadable; registry keeps L6 3 | one automatic labeller, "not a radiologist read" | CC BY-NC | COBS; REG table B |
| RibFrac stream | T13 4 (single labeller), L6 1 (morphology only) | pseudo | CC BY-NC | REG tables B, C |
| Tier-1 acquisitions (fetched from 2026-09-23) | 15,233 new CTs in the plan's count (people, at most); expected 831 to 1,703 transitional people, 460 callable by a mask count. On disk per the family-B cards: 39 IDC collections (3,499 usable CTs), FDG-PET-CT-Lesions 900, AbdomenAtlas 3 Mini 7,649 usable, AMOS 723 (of 2,364: rule 2 refused 1,564 as thicker than 3 mm, and 67 are duplicates inside AMOS, ACQ section 9), NLST pilot 500, CTPelvic1K clinical 172, CSI 2014 20, a 70-CT validation set | two-labeller screen, unread; 2,332 flagged person keys (flags, not calls) | open | ACQ opening table and section 9; MAN section 1; TIERS section 0 |
| Tier-1 late (2026-09-24) | 3,365 new CTs, ten Zenodo collections; expected 163 to 336, 91 callable. PARTIAL: PANORAMA 1,114 CTs still pending the screen; CURVAS 70 of 90; DEEP-PSMA 53 of 100 | as above | open | ACQ opening table; TIERS section 1 |
| NLST pilot T13 measurement | 34 of 367 countable CTs called T13 by one labeller (9.3 %), shown wrong; 1.5 % once a rib on the named body was required | outside check against rib heads | open | ACQ section 11 |

### 1.3 Plain films with level labels

| dataset | held n | labels | licence, access | card |
|---|---|---|---|---|
| CSXA cervical atlas | 4,963 lateral films, all in the level bank | corner keypoints naming C2 to C7 | registration; CC BY | MAN#csxa_cervical_xray_atlas |
| BUU-LSPINE (Klinwichit 2023) | 3,600 patients, 7,200 films; 3,603 lateral in the level bank, the 3,600 AP in none (MAN§4.31); plus 2,000 and 400 subsets | end-plate lines L1 to L5 and S1, levels assigned by position; L4L6 sheet: 129 four-lumbar, 15 six-lumbar | request form and EULA, "No License Provided"; keep out of flag training (mem:lstv-data-landscape.md) | MAN#buu_lspine_3600; mem:anomaly-manifest-sources.md |
| NHANES II (CDC) | 17,073 films (2 of 17,075 empty at the source) | none released; pseudo-labels on 16,234 | public domain | MAN#nhanes2_cdc_films |
| NHANES II landmarks (VertXNet) | 543 films of 364 persons | per-level masks C2 to C7, T1, T11 to T12, L1 to L5, S1 | CC BY | MAN#nhanes2_zenodo_landmarks |
| VinDr-SpineXR | 10,466 images, 5,000 studies | lesion classes, no levels (13 in the audit release row, 8 in MANIFEST section 2.1, unreconciled: MAN section 10, family D unknowns row 12); pseudo levels on 7,625; 0 films in the reported level bank | PhysioNet DUA; no WSU IRB determination covers it (MAN§4.30) | MAN#vindr_spinexr |
| AASCE 2019 / BoostNet | 609 labelled films (grid copy 579); 128 BoostNet test films never reached the render bank (MAN§4.32) | 4 corners on 17 vertebrae, T1 to L5 naming assumed | SpineWeb form / mirror | MAN#aasce2019_boostnet |
| Mendeley 5jdfdgp762 | 714 films, 698 annotated; about 500 are BUU persons (MAN§4.33) | class-agnostic corners | CC BY | MAN#mendeley_5jdfdgp762 |
| IEEE DataPort lateral full spine | 236 films | machine pseudo-labels only | subscription | MAN#ieee_dataport_lateral_fullspine_236 |
| spine-detector corner corpus (project) | 33,943 vertebra instances on 5,401 films on 2026-09-07 (AP 18,061, lateral 15,882), drawn from the BUU 2,000-pair subset, AASCE, NHANES II and Mendeley; held-out set 558 instances | 4 corners per vertebra; level annotated, inferred from position or unknown by source | private repository; inherits each source's terms | MAN#spine_detector_corpus |
| **Level bank in use** | 9,108 films: CSXA 4,963 + BUU-LSPINE 3,603 + NHANES II 542 | | | CORP note j |

### 1.4 Intraoperative and other real frames with 3-D truth or pose

| dataset | held n | device, subject | truth | licence | card |
|---|---|---|---|---|---|
| C-ArmLSpine (Zenodo 22768651) | 149 cases: 299 spot frames, 602 raw sweep projections, 149 CBCTs (137 include the sacrum); published numbers used the 296-frame pre-repair bank (MAN§4.20); distinct persons not established; living or cadaver not stated | FIRST Surgio-B51, intraoperative | CBCT per case; no labels or poses ship; levels projected from two automatic labellers | CC BY | MAN#carmlspine; FOURTH |
| DeepFluoro (Grupp 2020) | 6 cadaveric pelves, 366 frames | Siemens Cios Fusion | CT and pose per frame; 14 landmarks | CC BY-NC (T1 says BY-NC-SA) | MAN#deepfluoro_h5 and two other copies |
| Geneva hip gold standard | 1 resin phantom; 116 frames over 19 views (CARM says 19 frames) | Philips BV Pulsera | CT, rigid transforms, projection matrix | CC BY-SA (paper says BY-NC) | MAN#geneva_hip |
| Ljubljana 2D-3D-GS | 1 cadaveric L1 to L5; 18 turntable radiographs | Trixell PIXIUM 4600, not a C-arm | fiducial gold standard | CC BY-NC-ND or signed agreement | MAN#ljubljana_2d3d_gs |
| SpineSAC | 3 sawbone phantoms, 286 raw and 118 processed frames | 5 or 6 C-arms | phantom CT, projection matrices; no bone truth yet | none stated | MAN#spinesac |
| Bournemouth cervical QF tracks | 63 people, 252 sequences, tracks only (no pixels) | Siemens Arcadis Avantic, lateral cine | level-named corners C0 to T1 per frame | CC BY | MAN#bournemouth_qf_cervical_tracks |
| Public fluoroscopy clips | 1,269 clips (776 live) | mixed | none | mixed | MAN#fluoro_video_public_clips |
| FluoroCap literature harvest | 29,500 panels, 21,603 manifest rows; 72.8 % are reproductions with no pixel residual | republished figures | caption labels only | per article | MAN#fluorocap; dropped from training (MAN§4.35) |
| Bern dynamic myelography videos | 4 MP4s (5 to 21 s each), held among the public clips; the native DICOM and the 62-patient cohort are not held (section 2, A40) | pulsed 7.5 f/s | none | CC BY | PARTIAL: MAN#fluoro_video_public_clips; REQ item 3 |
| carm_drr and its fold copies (project banks) | C-ArmLSpine real spot frames in the render-bank layout: 240 annotations over 120 cases (105 train, 15 validation) in `~/carm_drr`; cross-validation copies of 224 to 248 entries; plus `rare_class/carmlspine_cbct_drr`, 396 held-out renders of 3 real L6 CBCTs | real frames (the name "drr" is only the layout); the CBCT bank is synthetic | levels from two automatic labellers | derived from CC BY, not distributed | MAN#carm_drr |
| **Real frames scored** | 4,276 (296 + 366 + 3,480 + 116 + 18), of which 778 from mobile C-arms; only the Surgio-B51 carries naming truth | | | | CORP note j; N3 section 2 |

"Only C-ArmLSpine is intraoperative human data" (DSH section 2.1).

### 1.5 CBCT projections with a planning CT

| dataset | held n | device | truth | licence | card |
|---|---|---|---|---|---|
| COBRA2026 | 692 of 867 cases, 375,618 projections; only 145 of the 692 in any frame bank; Varian 225 not exported ("geometry not solved"); the Elekta device card fitted on 40 frames of 3 cases | Elekta Synergy and VersaHD; Varian Halcyon, TrueBeam, VitalBeam; pelvis | RTK geometry per projection; deformably registered planning CT | training CC BY-NC; validation and test (175) embargoed to 2032-03-01. PARTIAL | MAN#cobra2026; MAN§4.25; mem:data-audit-99-gaps.md |
| C-ArmLSpine raw sweeps | 2 cases, 301 projections each | Surgio-B51, lumbar | CBCT of the same sweep | CC BY | MAN#carmlspine |

### 1.6 Synthetic rendering sources (all SYNTHETIC, HELD)

| source | n | card |
|---|---|---|
| Project render banks | ctsp_drr 801 (banks rebuilt after 2026-09-23 hold 802, MAN#ctsp_drr); physics_drr 7,045 annotations; physics_rare 1,482; verse_drr 387; ts_drr 1,170; ts_drr_v3 1,735; anchor_drr 7,842; anchor_drr_c2 6,129; lstv_flag_renders 9,612; spinalai_drr 8,358; aasce_drr 457; xrspinopelvic1k 6,416 lateral DRRs (row-spacing defect on ctsp_drr before 2026-09-19 and on 181 VerSe soft renders, MAN§4.16) | MAN family A render cards; MAN#xrspinopelvic1k |
| devcorpus | 4,551 files from 142 TotalSegmentator subjects | MAN#devcorpus |
| implant_ct_synthetic | implant_verse 1,119; implant_ts 1,629; implant_ct 1,518 deleted (PARTIAL) | MAN#implant_ct_synthetic |
| fluorogen_synthetic | 12,929 restyled renders (L6 1,763, T13 86) over 2,844 cases | MAN#fluorogen_synthetic |
| polypose_synthetic | not recorded | MAN#polypose_synthetic |
| Spinal-AI2024 | 20,000 images; 8,358 usable renders of 44 synthetic identities | MAN#spinal_ai2024; MAN§4.34 |

### 1.7 Spondylolisthesis and pathology

| dataset | held n | labels | card |
|---|---|---|---|
| VinDr-SpineXR | 10,466 | lesion classes (fracture, spondylolisthesis, osteophytes, implants; 13 or 8, unreconciled, MAN section 10 family D row 12), no levels | MAN#vindr_spinexr |
| BUU-LSPINE | 3,600 patients | end-plate lines; a spondylolisthesis detection dataset | MAN#buu_lspine_3600 |
| Mendeley 5jdfdgp762 | 714 films; 90 spondylolisthesis films, 33 naming the slipped level in the file name | corners | MAN#mendeley_5jdfdgp762 |
| AASCE 2019 | 609 labelled | scoliosis landmarks | MAN#aasce2019_boostnet |
| RSNA 2022 cervical fracture CT | 2,019 studies | per-level fracture labels | MAN#rsna_2022_cspine |

---

## 2. What is missing

A missing dataset is one the field's literature names and the manifest does not hold. This section lists every such
set named in the verified sweeps (MISSED, THIRD, FOURTH, PAIRED, CARM), the prior-art and strategy notes, and the
working note N2, in five groups. Within a group, rows are ranked by subjects as recorded, largest first, because new
people are what the claims lack; a set whose subject count is not recorded comes last in its group, ordered by the
images it records. A count in another unit (frames, recordings) is used only where the file gives no subjects, and the
cell says so.

- **A. Real projections with level or pose truth, spine or pelvis in the field.** This is the input every transitional
  power row in section 4 needs and the one you have least of (DSH section 2.1; N2 section 8b). Five subgroups:
  intraoperative and interventional sets from living patients, or intraoperative with the subject type not stated (A1
  to A21); radiotherapy kV and CBCT sets from living patients with a planning CT (A22 to A31); interventional CBCT
  sweeps with no planning CT (A32); diagnostic cine, dynamic and biplanar radiography of living people (A33 to A41);
  cadaver, animal and phantom sets (A42 to A64).
- **B. CT that would add transitional people.** Ordered by the acquisition plan's own E_low; the E_T13 column matters
  because T13 is the scarce class (section 5) and gains almost only from chest CT (JOIN; ACQ section 10).
- **C. Films with level or LSTV labels**, ordered by n as recorded (people where the file gives people, otherwise
  films), n not recorded last.
- **D. Synthetic sets**, ordered by the number of images or subjects as recorded, n not recorded last. Last as a group
  of new data, because none synthesises a transitional vertebra: "No published work has synthesised a transitional
  vertebra ... in any modality" (RARE section 0).
- **E. Other named sets not held**: off-target anatomy, sets the sweeps refuted or judged useless, CT scouts, MRI,
  brokers and web sources, and the literature cohorts behind the priors. They are listed so that "missing" is complete;
  as recorded, none would add a transitional person or level truth on real spine or pelvis projections.

Reason words: *gated*; *not fetched*; *excluded by rule n* (ACQ section 1); *never released* (with or without a
route); *release not recorded*; *request, not drafted*; *request drafted, not sent*; *refuted* (the sweep's verifiers
found the description false); *judged useless* (the sweep's synthesis says it serves neither need); *searcher pass
only* (named with no verifier verdict). For FOURTH items the verdicts are given as recorded in its `round1_verified`
(r1) and `round2.verified` (r2) lists, two per candidate.

### A. Real projections with level or pose truth

**A1 to A21: intraoperative and interventional, living patients or subject type not stated** (by subjects)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A1 | LevelCheck clinical cohort (De Silva 2016; Ketcha 2017) | 178 patients: 178 preoperative CTs and 398 intraoperative radiographs; plus Ketcha's 24 thoracolumbar patients with 61 Carestream DRX-1 radiographs | DUA; no request drafted; neither paper has a data statement | Contact and route are not recorded for this cohort. MISSED finding 12 names Siewerdsen (at MD Anderson since 2022) with Uneri, Zbijewski or Stayman (JHU) copied, but for the Huang 2022 and Zhang 2021 cadaver long films (A43, A64), not for this cohort; the route is borrowed here. GEM (unverified) says "a formal Data Use Agreement" with the PI | as recorded in HAI finding 3 and MISSED findings 5, 12; GEM |
| A2 | Vanderbilt THA fluoroscopy (Chan 2025) | 146 living patients (161 hips), 336 frames with midline L5/S1 and SI-joint landmarks, AP only | never released, no route: no data-availability or on-request statement; the repository holds code only | none recorded; contact not recorded | as recorded in THIRD finding 5 |
| A3 | Huashan Hospital, Fudan (Shao 2024) | 140 living patients, preoperative CT and intraoperative AP and lateral films of L1 to L5; levels projectable after registration | request, not drafted; no data statement | Email Jiang Jianyuan, [e-mail withheld]; ask for the device make and model, DICOM headers, frames per patient and DUA terms (two co-authors are from Shanghai Maestro Surgical Robotics) | as recorded in MISSED findings 2, 12 |
| A4 | VerSeg-Net lumbar fluoroscopy | 50 patients, Philips UNIQ FD20, per-level L1 to S1 masks; an "explicit sharing statement" | searcher pass only (named in the coverage note alone); route not recorded | not recorded | as recorded in FOURTH coverage note |
| A5 | PUMCH stitching series (Liu 2026, Eur Spine J) | 43 scoliosis patients, 4 to 6 overlapping prone AP shots each on a Philips Zenition 70; the shift between shots is estimated, not recorded; no labels stated | never released: "No datasets were generated or analysed during the current study" | asking is judged unlikely to succeed; not drafted | as recorded in VIDEO; REQ (not-drafted list) |
| A6 | TCIA CMB-MML and CMB-AML interventional frames | open, CC BY. 16 living patients with XA series: 35 unique 2-D frames (Siemens AXIOM-Artis last-image-hold captures) and 3 DynaCT volumes. Only MSB-04031 is a spine procedure (AP and lateral thoracolumbar vertebral augmentation, 6 unique frames, lumbar CT from about T10 to the sacrum); the other frames are iliac-crest biopsies with about L3/L4 to S1 in the field. No annotations; positioner angles and SID/SOD in the DICOM | not fetched. The CMB-MML and CMB-AML CTs are held (MAN#idc_cmb_mml, #idc_cmb_aml); the XA frames are not | anonymous NBIA REST `getSeries`, then `getImage` by SeriesInstanceUID (the verifier pulled about 550 MB this way on 2026-09-21); re-query Modality=XA on each release | as recorded in FOURTH r1 6 (partly confirmed twice) |
| A7 | Southeast University / Bond-Star Medical (Chen, Kong et al.) | 15 living patients: 15 spine CTs and 15 real PA C-arm X-rays (Perlove PLX118F); the group's Med Phys 2025 paper reports 52 real X-ray images | never released, no route: no data statement or offer | none recorded | as recorded in FOURTH r1 21 (partly confirmed twice) |
| A8 | Hohai University / Changzhou LineReg (Shen et al., Med Phys 2026) | 10 living patients, 90 real registration samples, 710 edge-annotated images (real X-rays and DRRs mixed); distinct real exposures not stated | never released: code only (github shenao1995/lineReg); no data statement found, full text paywalled. A sibling, FlowReg (A20), holds a README only | none recorded | as recorded in FOURTH r1 19 (partly confirmed twice) and updates_to_known 12 |
| A9 | RadGS-Reg (Nanjing / Changzhou; MICCAI 2025) | 10 intraoperative spine cases, each a preoperative CT with paired AP and lateral X-rays; 30 vertebra-level samples; poses "recorded during C-arm circular acquisitions"; living or cadaver not stated | never released, no route: no data statement or request route | write to the corresponding authors (Junfeng Jiang, [e-mail withheld]; S. Kevin Zhou, [e-mail withheld]); the paper does not invite requests | as recorded in THIRD findings 6, 10 |
| A10 | NIT Warangal / NIMS Hyderabad (2D-3D-sci-registration) | 9 living patients and 51 AP/LAT C-arm sets in the repository README (at most 49 unique frames); the manuscript's 2 patients are not among the nine; Ziehm C-arm; preoperative CT with level-named L1 to L5 centroids | CT and raw X-rays not released ("available upon reasonable request"); 60 centroid files and 54 overlay PNGs, each holding the real frame at 8 bits beside a DRR, are public | write to the authors; no request channel, DUA or form recorded | as recorded in FOURTH r1 18 (partly confirmed twice) |
| A11 | Fourth Medical Center of PLA General Hospital (Ju et al., Sci Rep 2025) | 8 living pelvic-fracture patients, intraoperative AP and inlet X-rays with CT; "8 real intraoperative X-ray images" stated, while the figures suggest 8 AP and inlet pairs | request, not drafted: "requests for data and materials should be addressed to Jingxin Zhao" | write to [e-mail withheld] | as recorded in FOURTH r1 23 (partly confirmed twice) |
| A12 | Manipal (MIT / Kasturba Medical College) | 4 living adolescent thoracolumbar trauma patients, preoperative CT with T11 to L3 levels, Ziehm 9-inch image intensifier; in effect four AP images | never released, no route: no data-availability section | none recorded | as recorded in FOURTH r1 22 (partly confirmed twice) |
| A13 | DAX pre-training corpus (Siemens Healthineers / FAU) | 632,385 intraoperative X-rays, about 124,000 of the spine; no labels; patient count not recorded | never released, no route: "the clinical images cannot be shared"; only the DINO backbone checkpoints are public | none; the checkpoints could serve as an initialisation | as recorded in FOURTH refuted_or_useless (judged useless) |
| A14 | SX-Stitch (PUMCH / SUSTech) | 1,032 intraoperative C-arm frames in overlapping series with vertebra masks; patient count not recorded | request drafted, not sent | Send SXS to Wei Liu (SUSTech) and Jinqian Liang (PUMCH); no email is printed in the arXiv version, so use the SUSTech and PUMCH directory addresses | as recorded in SXS; MAN#sx_stitch_request |
| A15 | Rao 2024, EMBC (Spine Vision) | 578 C-arm images from three commercial C-arms; patients, cadavers and phantoms, counts not recorded; per-vertebra detection labels, no naming | release not recorded | not recorded | as recorded in RF22 section 5.1; mem:registration-free-prior-art.md |
| A16 | VDVM (Zhang 2023) | 382 C-arm images and 203 full-length films to train, 31 C-arm test images; patient count not recorded | release not recorded | not recorded | as recorded in RF22 section 5.1 |
| A17 | CM Spine | 208 intraoperative lumbar G-arm images with vertebra detection labels; patient count not recorded | a Google Drive download returned an empty folder, and whether that file was CM Spine is recorded only by its name; otherwise request only | email request (Chinese Academy of Sciences, per GEM, unverified); STRAT: "genuinely relevant but email-request only; send the email, do not wait on it" | as recorded in MAN#cm_spine_drive_file; STRAT; GEM |
| A18 | Manbachi 2018 reader set | 62 hard intraoperative radiographs drawn from LevelCheck's 398 (A1), read by 5 surgeons | release not recorded | as A1 | as recorded in HAI finding 1 |
| A19 | MetaPose private pelvic-fracture X-ray and CT set (Wang 2026); CT2X-IRA private clinical CT and X-ray set (Geng, PMB 2023) | subjects, images and device not retrieved | private; access unknown | not recorded | as recorded in FOURTH r1 24, 25 (partly confirmed twice each) |
| A20 | FlowReg (Shen, Nong, Zhou; MICCAI 2026), the LineReg lineage | clinical patients, count unknown; real X-ray use is inferred from the lineage, not seen | never released, no route; the repository holds a README only | none | as recorded in FOURTH r2 20 (confirmed and partly confirmed) and updates_to_known 12 |
| A21 | DVAP-Reg SimReg and HybReg (TMMU, MedIA 2026) | contents not verified; whether HybReg holds real intraoperative X-rays is unverified | promised, not deposited; an open issue asking for a timeline has no answer | watch the National Basic Science Data Center deposit | as recorded in MISSED finding 7 |

**A22 to A31: radiotherapy kV and CBCT, living patients, planning CT** (by subjects)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A22 | Charters 2024 (UCLA) | 527 patients, 4,213 images: 2,486 paired kV (254 patients), 58 unpaired AP kV, 1,669 MV; thoraco-abdominal spine; DICOM REG to the planning CT | request, not drafted: "available upon reasonable request from the authors" | write to [e-mail withheld] | as recorded in PAIRED finding 7 |
| A23 | Petragallo, Lamb et al. 2023 (UCLA and Brainlab ExacTrac, six or more institutions) | 429 spine radiotherapy patients, 1,592 fractions, 3,184 real stereoscopic kV images, with planning-CT DRRs including simulated off-by-one-vertebra shifts | request only, conditioned on IRB approval and six institutional data-sharing agreements; no deposit found; not drafted | write to the corresponding author, Rachel Petragallo (UCLA Radiation Oncology; her PhD finished in 2024, so the contact is likely stale) | as recorded in FOURTH r2 17 (partly confirmed twice) and updates_to_known 10 |
| A24 | COBRA2026 validation and test | 175 cases; the only rows that would add transitional people with real projections of the held kind | embargoed to 2032-03-01 | none before 2032 | MAN#cobra2026 |
| A25 | CHR Metz-Thionville triggered-kV SBRT cohort (Techer et al.) | 49 bone-metastasis patients, 8,717 triggered kV images | never released: "subject to institutional and regulatory restrictions"; code only (Zenodo 21516903) | a collaboration request to P. Retif | as recorded in FOURTH refuted_or_useless |
| A26 | TROG 15.01 SPARK | 48 living prostate SBRT patients, 5 centres, about 1.1 M frames, planning CT; L5 absent in every rendered frame | not fetched (open, CC BY, 960 GB compressed) | fetch as a Slurm job onto Ceph | as recorded in FOURTH new_confirmed and r1 1 (partly confirmed twice) |
| A27 | TCIA 4D-Lung raw projections | 20 patients, about 2,500 Varian OBI kV projections per scan, thorax | the release holds volumes only; projections by request; not drafted | request from the authors (Hugo et al., Med Phys 2017) | as recorded in PAIRED finding 5 |
| A28 | Stanford CyberKnife clinical spine 2D-3D data (Russakoff, Rohlfing, Maurer, 2003 to 2005) | 4 to 5 living patients, stereo kV pairs | never released, no route | none | as recorded in FOURTH r2 16 (partly confirmed twice) |
| A29 | RTK public patient data (Centre Léon Bérard patients 1 and 2, POPI) | 3 living lung patients, Elekta XVI 4D-CBCT projections with planning CT and per-projection matrices | not fetched (open; no data licence stated) | download from data.kitware.com | as recorded in FOURTH new_confirmed and r1 2 (partly confirmed twice) |
| A30 | SPARE (Sydney) | contents not established: every content claim was refuted 0 to 3 in CARM; PAIRED reads it as real Elekta and Varian kV projections with a prior 4D-CT | not fetched (CC BY-NC, 291 GB) | read `Instructions_Datasets` inside the archive before any fetch | as recorded in PAIRED findings 3, 4; CARM caveats |
| A31 | ADAPT trial 4D-CBCT raw projections (Image X Institute) | not recorded | never released; only GIFs and code are public | a direct request is plausible; there is no route today | as recorded in FOURTH refuted_or_useless |

**A32: interventional CBCT sweeps with no planning CT**

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A32 | Jaganathan / Maier (Siemens Healthineers, FAU; WACV 2023, MICCAI 2021) | 55 living patients, thoracic and lumbar CBCT volumes, each with the real projections of its sweep (190 to 390 per volume) and pose from the reconstruction geometry; device not named | never released; no data statement | ask FAU or Siemens under a DUA (the file's open question) | as recorded in PAIRED finding 6 |

**A33 to A41: diagnostic cine, dynamic and biplanar radiography, living people** (by people)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A33 | Pittsburgh swallow corpus (Sejdic, Coyle) | 335 people: 265 patients (1,518 clips, Toshiba Ultimax) and 70 healthy volunteers (GE); C2 and C4 corners on every frame, so cervical only | request drafted, not sent | Send `04_pittsburgh.eml` to [e-mail withheld]; Pitt data-use agreement | as recorded in REQ item 4; VIDEO |
| A34 | Bournemouth lumbar quantitative fluoroscopy (Breen 2021) | 127 analysed adults, lateral weight-bearing L2 to S1 cine at 15 fps; per-frame angles public on OSF a27py, pixels not | request drafted, not sent | Send `01_bournemouth.eml` to [e-mail withheld] (cc Breen); a UK data-sharing agreement follows | as recorded in REQ item 1; VIDEO |
| A35 | Osaka/NAIST hip cohort and its EOS arm (Otake, Sato, Gu; Suehara, MICCAI 2025) | 77 real EOS biplanar pelvis and hip radiographs, each 2D-3D registered to the same patient's CT; parent cohort 475 patients, 305 with QCT | EOS set: dataset link "N/A", a collaboration lead; parent cohort on reasonable request; not drafted | write to the corresponding author | as recorded in FOURTH r2 18 (partly confirmed twice) and updates_to_known 11 |
| A36 | SJTU Med-X / Tongji / TAOiMAGE standing biplanar lumbar radiographs (Yu, Tsai; Med Phys 2026) | 64 living subjects with CT (48 young adults in six movements, 16 patients), 880 real calibrated biplanar pairs; the arXiv version gives 50 subjects | request, not drafted: "available from the corresponding author on reasonable request" | write to [e-mail withheld], [e-mail withheld] or [e-mail withheld] | as recorded in FOURTH r1 20 (partly confirmed twice) |
| A37 | Bournemouth cervical QF DICOM | the pixels behind the 252 held track sequences of 63 people | request drafted, not sent | the same letter as A34 | as recorded in REQ item 1 |
| A38 | Maastricht cervical and lumbar cine (van Santbrink, Bioengineering 2026) | 112 lateral cervical recordings, 89 from 39 healthy participants and 23 from pre-operative patients with cervical radicular syndrome, with per-frame C0 to C7 contours; lumbar L1 to S1 cine (11 men, 7.5 fps) | request drafted, not sent | Send `02_maastricht.eml` to [e-mail withheld]; GDPR data-transfer agreement | as recorded in REQ item 2 |
| A39 | Utah Hive standing pelvic tilt and Cam-FAIS records (Anderson, Atkins) | 32 living adults with CT and per-frame pelvis and femur poses from biplane videoradiography; 0 X-ray images released | the released packages hold CT, meshes and transforms; the biplane frames and calibration are withheld | a request to Anderson or Atkins (Utah) | as recorded in FOURTH r2 10 (partly confirmed twice) and refuted_or_useless; CARM finding 7 |
| A40 | Bern dynamic myelography native DICOM | the DICOM behind the 4 held MP4s (section 1.4), and the 62-patient cohort the letter asks about | request drafted, not sent | Send `03_bern.eml` to [e-mail withheld]; a Swiss data-transfer agreement | as recorded in REQ item 3 |
| A41 | MIDRC fluoroscopy | RF 71 and XA 15 of 202,222 studies; about 17 C-arm studies of unknown anatomy, mostly bronchoscopy and swallow; no labels; people not recorded | not fetched (registration) | MIDRC registration | as recorded in THIRD finding 8 |

**A42 to A64: cadaver, animal and phantom** (by specimens)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A42 | Balgrist ex-vivo lumbar (Jecklin 2024, 2025) | 13 specimens plus 6 validation specimens per the request letter (the Sci Rep paper describes 6 specimens with at least 50 X-rays each), three C-arms, fiducial projection matrices | withheld for pending patents; request drafted, not sent | Send BALG to [e-mail withheld] | as recorded in BALG; MAN#balgrist_exvivo_request; FOURTH updates_to_known 4 |
| A43 | Huang 2022 JHU cadaver long films | 13 cadavers, 100 level-labelled O-arm long films (50 AP, 50 lateral) | never released (Zenodo 7161385 holds simulations only) | ask Siewerdsen (MD Anderson) with Uneri, Zbijewski or Stayman (JHU) copied | as recorded in MISSED findings 3, 12 |
| A44 | DKFZ / Siemens cadaver spine C-arm study (Kausch et al., MICCAI 2021, MedIA 2022) | 11 cadaver specimens, 16 datasets of 1,364 real projections each (21,824), k-wires or screws in 9 | never released ("Link to the dataset(s): N/A") | none recorded | as recorded in FOURTH r1 29 (partly confirmed twice) |
| A45 | SheepSpineX (X2P-Net, SJTU) | 9 ex-vivo sheep cervical spines, about 270 AP/LAT pairs with CT and projected centroids; Siemens Arcadis Varic | request, not drafted | write to [e-mail withheld] and [e-mail withheld] | as recorded in MISSED finding 8 |
| A46 | UC Davis / Augmedics cadaver screw study (Global Spine J 2025) | 6 cadavers, CT and about 11 to 12 real X-ray frames in all, 151 screws from the cervical spine to the SI joint | request only: "available from the corresponding author upon reasonable request", which most plausibly covers the screw tables, not the images | write to Richard L. Price, [e-mail withheld] | as recorded in FOURTH r1 26 (partly confirmed twice) |
| A47 | Bern canine thoracolumbar Steinmann-pin fluoroscopy (Goffart 2022) | 5 canine cadaver columns, one end-on image per pin; OrthoScan FD-OR mini C-arm | request, not drafted | write to the authors | as recorded in FOURTH r2 11 (partly confirmed twice) |
| A48 | Giessen/Jena canine biplanar fluoroscopy (Front Vet Sci 2021) | 4 living dogs, biplanar fluoroscopy of pelvis, sacrum, L6 and L7 with per-frame poses against a same-dog CT; calibration films archived | request, not drafted: the archive files return HTTP 403 without login | enquiries to Prof. Martin S. Fischer, [e-mail withheld] | as recorded in FOURTH new_confirmed and r2 0 (partly confirmed twice) |
| A49 | BG Klinik Ludwigshafen, MINTOS (Brunken 2026, J Imaging; Bullert, Eur Spine J) | 4 whole-body cadavers, 384 images evaluated, three Siemens Cios detectors (Fusion, Flow, Flow.neo) | request (J Imaging); the Eur Spine J paper says "No datasets were generated or analysed"; not drafted | write to [e-mail withheld] | as recorded in FOURTH r1 28 (partly confirmed twice) |
| A50 | UMC Utrecht / Philips cadaver skin-marker registration (Bindels 2022) | 3 cadaver torsos, 780 vertebra registrations; Philips Zenition 70 and AlluraClarity FD20 | never released, no route | none | as recorded in FOURTH r2 15 (confirmed and partly confirmed) |
| A51 | Xinqiao Hospital live-minipig study (BMC Musculoskelet Disord 2025) | 3 live minipigs at L1 to L5, G-arm and C-arm, marker points; no CT and no level labels | images on request, not drafted | [e-mail withheld], [e-mail withheld] | as recorded in MISSED finding 9 |
| A52 | Utrecht ISI 2D-3D gold standard (van de Kraats 2005) | 2 cadaveric lumbar segments, 4 fluoroscopy images each with 3DRX, CT and MR; masks for 8 vertebrae | lost: "This database is no longer available" since 2013, never archived | a private copy from van Walsum or Niessen (Erasmus MC), Penney (KCL), Tomazevic (Ljubljana) or the Vienna licensees | as recorded in FOURTH r2 12 (partly confirmed twice) and updates_to_known 3 |
| A53 | US-X Complete (TUM CAMP) | 2 lumbar phantoms, Loop-X lateral X-ray with co-registered CBCT | not fetched (open) | download | as recorded in FOURTH r1 9 (partly confirmed twice) |
| A54 | Otake 2013 JHU cadaver (prototype Siemens flat-panel C-arm) | 1 cadaver, 36 projections (72 CT-projection pairs), 19 targets from C6 to L5 | never released; no release statement | write to Siewerdsen (MD Anderson) and Zbijewski or Stayman (JHU) | as recorded in MISSED findings 4, 11 |
| A55 | FluoroSAM Loop-X torso cadaver (JHU ARCADE) | 1 full-torso cadaver (T2 to mid-femur), navigated pose, 464 lower-torso images in arXiv v1, projected TotalSegmentator masks | no route; request not drafted | write to Killeen and Unberath (JHU ARCADE; addresses not verified) | as recorded in THIRD findings 4, 11 |
| A56 | Spine-DART (JHU; Front Robot AI 2026) | 1 cadaver, Loop-X CT, 35 fluoroscopic images, 16 vertebrae | request, not drafted ("without undue reservation") | write to the authors | as recorded in FOURTH r1 27 (partly confirmed twice) |
| A57 | Goswami IOERT pig lower limb (IEEE DataPort 10.21227/gxpd-d998) | 1 pig limb specimen, 7 calibrated C-arm projections and CT; limb anatomy, so device calibration only | not fetched (open, CC BY) | download | as recorded in FOURTH r1 16 (partly confirmed twice) and updates_to_known 6 |
| A58 | LevelCheck Rando phantom (Otake 2012; the prototype flat-panel C-arm of A54) | 1 thoracic phantom, 35 frames over a 70-degree arc | never released; no data statement | as A54 | as recorded in MISSED findings 5, 11 |
| A59 | FORCAST-EST (heidata 10.11588/data/GIWRQA) | 1 lumbar spine phantom: Siemens AXIOM-Artis DynaCT sinograms (2 x 496 frames), arbitrary-trajectory projections and CBCT volumes, with and without metal; about 4.6 GB | not fetched (open, CC BY) | download | as recorded in FOURTH r2 14 (confirmed and partly confirmed) |
| A60 | Zhao pelvis phantom (figshare 5663446); Madesta 4D-CBCT phantom; AAPM MATCH phantom; RabbitCT re-release (496 projections of a post-mortem rabbit) | 1 phantom or specimen each | not fetched (open) | download | as recorded in FOURTH r1 4, 12, 11, 5 (each confirmed or partly confirmed by both verifiers) |
| A61 | Robarts endoleak phantom (Xing; Canon Alphenix) | 1 phantom, 156 fluoro-CT pairs | access unknown (one verifier found no release) | write to the authors | as recorded in FOURTH r1 14 (partly confirmed twice) |
| A62 | Marques and Pina 2026 (four C-arms); Jensen 2024 (three flat-panel C-arms) | a low-contrast phantom on 4 units; one cadaver flank on 3 units | DICOM not shared (Marques and Pina release only the phantom's STL files, Zenodo 18827666); Jensen: no release | print the Marques and Pina phantom and image it on your own C-arms | as recorded in THIRD findings 9, 12 |
| A63 | SyntheX LoopX test set | 60 images with landmarks; subjects not recorded | not recorded | not recorded | as recorded in STRAT tier 1 |
| A64 | Zhang 2021, 2022 JHU multi-slot O-arm | real long-length images of phantoms and cadavers; n not recorded | never released | as A43 | as recorded in MISSED findings 3, 12 |

### B. CT that would add transitional people

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| B1 | Merlin abdominal CT (Stanford AIMI) | 18,317 new people; E_low 1,259.9, E_high 2,522.3, E_count 673.0, E_T13 low 2.1 | gated | Sign in to the Stanford AIMI portal (stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40) and accept the AIMI non-commercial research-use DUA; a time-limited Azure URL follows | ACQ section 7; JOIN |
| B2 | RSNA RATIC abdominal trauma | 3,147; E_low 240.7, E_high 499.3, E_count 135.8, E_T13 15.9 | gated | A MIRA (mira.rsna.org/dataset/5) or Kaggle account and RSNA's terms: non-commercial, no redistribution; derived labels internal only | ACQ section 7; JOIN |
| B3 | NLST beyond the 500-CT pilot | 24,713; E_low 111.4, E_high 345.9, E_count 110.5, E_T13 109.4 | planned, tier 2, held by stopping rule 4 (tier 2 waits while more than 5,000 fetched CTs are unscreened) | finish the tier-1 screen, then release tier 2 | JOIN; ACQ section 3 |
| B4 | ENHANCE.PET 1.6k | 1,683; E_low 108.3, E_count 61.3, E_T13 7.6 | deferred: the Science Data Bank route is not written (a login may be needed, unconfirmed) | write the route | JOIN; ACQ section 7 |
| B5 | CT-RATE | 21,304; E_low 94.9, E_count 94.9 (T13 only), E_T13 94.9 | gated | Hugging Face gate form (name, institution, email, terms checkbox) at huggingface.co/datasets/ibrahimhamamci/CT-RATE; CC BY-NC-SA. Ungated re-uploads exist and were deliberately not used | ACQ section 7 |
| B6 | INSPECT | 19,402; E_low 86.4, E_T13 86.4 | gated | the same AIMI research-use DUA as Merlin | ACQ section 7 |
| B7 | TotalSegmentator task data (liver lesions) | 842; E_low 60.6 | unresolved overlap with TotalSegmentator v2 and v3 | an id map, or an answer from the authors | JOIN; ACQ section 9 |
| B8 | CADS unique parts (CT-TRI 586, VISCERAL 167) | 753; E_low 48.5 | gated | Hugging Face checkbox at huggingface.co/datasets/mrmrx/CADS-dataset; CT-TRI's own terms must be read for derived labels; VISCERAL carries its access agreement | ACQ section 7 |
| B9 | RSNA-STR PE (RSPECT) | 7,279; E_low 32.4, E_T13 32.4 | gated | Kaggle account and the competition rules (kaggle.com/c/rsna-str-pulmonary-embolism-detection) | ACQ section 7 |
| B10 | MAGIC-CT | 562; E_low 27.9 | gated: the record's DUA requires proof of completed human-subjects or HIPAA training; "Only Greg can make that application" | apply at zenodo.org/records/18389015 | ACQ section 7 |
| B11 | Tier 2, deferred and unresolved-overlap remainder, in E_low order | STOIC2021 8.9; LUMOS 7.9; LIDC-IDRI 7.5; VSDFullBody 6.4; TotalSegmentator task data, pleural effusion 5.5 (E_T13 2.7); TMTV 3.9; UniToChest 2.8; NSCLC-Radiogenomics 2.1; Spinal-Multiple-Myeloma-SEG 1.9; NSCLC-Radiomics 1.8; Spine-Mets-CT-SEG 1.6; Prostate-Anatomical-Edge-Cases 1.4; MedPelvis3D 1.1; LDCT-and-Projection 0.9; TotalSegmentator task data, hip implant 0.8; CPTAC-LSCC 0.7; LumVBCanSeg 0.7; CPTAC-LUAD 0.6; MIDRC-RICORD-1B 0.6. The spine-labelled or spine-only sets among them are Spine-Mets-CT-SEG (54 new people of 55, per-vertebra DICOM SEG named by level, CC BY), Spinal-Multiple-Myeloma-SEG (67), LumVBCanSeg (185 lumbar CTs), MedPelvis3D (99 pelvic CTs) and LUMOS (280 lumbar CTs) | tier 2, held by stopping rule 4; LUMOS and TMTV deferred until a zipped-DICOM route is written; the two TotalSegmentator task sets are unresolved overlap | as B3; write the routes; an id map | JOIN ranks 13, 18, 54, 75 to 88, 91, 92; N2 section 8a rows 11 to 29 |
| B12 | Partial holdings | PANORAMA 1,114 CTs pending the screen; CT Colonography remainder, about 21 to 23 people (E_low 1.5); AMOS 1,564 CTs thicker than 3 mm; the 10 VerSe'20 series never downloaded (their VerSe'19 copies were substituted silently); the VertebralBodiesCT-Labels masks (1,460 in ROAD), of which only the external L6 and T13 reads on 70 TotalSegmentator CTs are used and which have no card | screen not finished; token match pending; rule 2; never downloaded; not carded | run the screen; match CTSpinoPelvic1K tokens to IDC PatientIDs; AMOS cannot be recovered without changing rule 2; re-download the 10 series; fetch and card the masks | TIERS section 0; ACQ sections 5, 9; MAN§4.9; MAN#totalsegmentator_v201; ROAD |
| B13 | Excluded by licence: NMDID (15,243 decedents); Glocker spine CT (SpineWeb 3; 125 patients, 242 scans, vertebra centroids, CC BY-NC-ND); LNDb (294); CancerVerse | | rule 3: an ND licence or a DUA forbidding derivative works | "No form would fix that" | ACQ section 7; JOIN rank 128 |
| B14 | Never released: VERIDAH in-house CT (1,536 scans); Schinz 2026 (1,242 whole-thoracolumbar CTs, release not recorded) | anomaly-aware labels (VERIDAH) | "what exists is a capability, not a dataset" (VERIDAH) | none | MPDA lines 277, 342 to 344 |

### C. Films with level or LSTV labels (by n as recorded)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| C1 | MrOS (Osteoporotic Fractures in Men, US) | about 3,600 to 3,786 men with baseline lateral thoracic and lumbar films and same-visit QCT slabs; 10,351 annotated lateral spine films (67,215 vertebral bodies) were released to one outside group; the CT slabs miss the sacrum and L5-S1 | DUA, not applied for: images only through a Publications Committee analysis plan and a DUA; MrOS Online accounts disabled pending re-registration (2026-09-21); not for commercial use | an analysis plan and DUA through the Coordinating Center | as recorded in FOURTH r2 23 (partly confirmed twice) and updates_to_known 13; PATH |
| C2 | Sabri 2025 (Neurosurg Focus) | 3,147 full-length radiographs, 8.8 % transitional | release not recorded | not recorded | as recorded in mem:lstv-data-landscape.md |
| C3 | Kwak, Ro, Kang 2025 (J Clin Med) | 3,116 standing lateral lumbar films, 1,941 LSTV (62.3 %, labels text-mined from MRI reports), 313 test | never released; "may be shared upon reasonable request" | write to [e-mail withheld] (corresponding), copying [e-mail withheld] (data curation) and [e-mail withheld]; ask for the label table, or the weights and test-set ids, not the images | as recorded in mem:lstv-data-landscape.md and RF18 finding 12 |
| C4 | LUMOS radiographs | 1,620 lumbar films of 803 living patients; 280 with a CT within six months; DXA and vertebral dimensions, no levels | planned, deferred | write the zipped-DICOM route; confirm that CT id n and X-ray id n are one patient before trusting a pair | as recorded in MAN#zenodo_lumos; MISSED findings 0, 1, 12 |
| C5 | Sina University Hospital, Tehran | 300 living trauma patients, AP pelvic film and abdominopelvic CT | request, not drafted ("without undue reservation") | write to the authors | as recorded in THIRD finding 7 |
| C6 | TCIA same-patient films with CT: COVID-19-NY-SBU; TCGA-KIRC, TCGA-UCEC, TCGA-BLCA, VAREPOP-APOLLO, COVID-19-AR, CMB-LCA | COVID-19-NY-SBU: 27 patients with an abdominal film and an abdomen/pelvis CT; the other overlaps: 3 to 15 patients, 8 to tens of films; no labels | not fetched: the census keeps one CT series per patient, and CR, DX and RF series are not CT (the COVID-19-NY-SBU CTs are held, JOIN rank 53) | an NBIA query by modality per collection | as recorded in MISSED finding 10; FOURTH r1 8, r2 27 (partly confirmed twice each); ACQ section 1 |
| C7 | TVGH-SpineXR (IEEE DataPort 10.21227/x6bb-7r75) | n not recorded; T1 to L5 per-vertebra level labels, masks and end-plates per the record | not acquired (probe only, 2026-09-22) | log in to IEEE DataPort | as recorded in MAN#tvgh_spinexr; FOURTH refuted_or_useless |
| C8 | AI Hub (Korea) datasets 610 and 611 | n not recorded; whether levels are labelled is not stated | not obtainable as constituted: restricted to Korean nationals, analysis in a secure zone with no download | a Korean collaborator | as recorded in FOURTH refuted_or_useless |

### D. Synthetic sets (by images or subjects as recorded)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| D1 | FluoroSAM fluoroseg (Hugging Face benjamindkilleen/fluoroseg) | about 3 M synthetic images | not fetched | download if a use appears | as recorded in THIRD finding 4 |
| D2 | AnyCXR | 126,410 chest renders from 2,982 CTs | release not recorded | none | as recorded in MORPH row 2 |
| D3 | PENGWIN Task 2 (Zenodo 10913196) | 50,000 DeepDRR renders from 100 of 150 CTs; pelvic fragments, simulated K-wires | not fetched (the PENGWIN 2026 CTs are held and can be rendered) | download if a use appears | as recorded in THIRD finding 3 |
| D4 | Barr 2026 synthetic cervical radiographs | 20,063 DDPM radiographs from 4,963 real lateral films, no labels | not fetched | download if a use appears | as recorded in MORPH row 10; SYN |
| D5 | Thoracolumbar SSM (Sci Data 2024) | 16,807 shape models, meshes only (694 GB) | rejected: 85.3 % fall outside their own 95 % ellipsoid | none | as recorded in MORPH row 15 |
| D6 | Huang 2022 long films (Zenodo 7161385) | 10,368 simulated long films from 162 CTs | not fetched | download if a use appears | as recorded in MISSED finding 3 |
| D7 | VICTRE; XCAT | 2,986 synthetic breast subjects; XCAT by request | rejected for now | none | as recorded in MORPH row 13 |
| D8 | BiSpineX | DRRs from 337 VerSe CTs | not held as files; regenerable from the held VerSe | regenerate if needed | as recorded in MISSED finding 8 |
| D9 | HKU MedIP cbct_projection | 4 records of Monte Carlo CBCT projections rendered from TCIA CTs (MIT) | judged useless: synthetic, not acquired | none; a possible scatter-model prior | as recorded in FOURTH refuted_or_useless |
| D10 | 2D3D-RegQuality (Hugging Face suemincho/2D3D-RegQuality) | DeepFluoro real frames paired with DRRs at perturbed poses, 11.7 GB real and 21.7 GB simulated; n not recorded | not fetched | download if a use appears | as recorded in FOURTH updates_to_known (DeepFluoro entry) |
| D11 | MAISI / NV-Generate-CT | a 3-D CT and mask generator (no n) | rejected, to run once as a disproof; the NVIDIA weights licence is unread | none | as recorded in MORPH row 11 |
| D12 | SyntheX deposit (JHU Dataverse 2PGJQU) | renders and real hip frames; n not recorded | not recorded: MISSED calls it one the project "already has", but the manifest has no card | look for it on the grid and card it | as recorded in MISSED finding 6 |

### E. Other named sets not held

| rank | dataset or source | n (as recorded) | why it is missing, and why it would not add level truth on spine or pelvis projections | source |
|---:|---|---|---|---|
| E1 | CHIRP (Varian TrueBeam kV projections, planning CT and CBCT) | 30 living head-and-neck patients | not fetched (open); head and neck, cervical spine coverage not stated | FOURTH r1 3 (partly confirmed twice) |
| E2 | Ljubljana 3D-2D-GS-CA (Mitrovic 2013) | 10 cerebrovascular patients, 3D-DSA with AP and lateral DSA frames and detector poses | not held: the xvr-data copy on disk is its `deepfluoro/` subfolder only; open, CC BY-NC-ND; head | CARM finding 5; PAIRED finding 9; MAN#deepfluoro_xvr_hf |
| E3 | Balgrist femur (Flepp 2025) | 5 cadaveric femora, 50 X-rays with photon-counting CT | not fetched (open); femur only | FOURTH r1 15 (partly confirmed twice) |
| E4 | Science Data Bank head phantom 2D-3D set | 10 phantom cases | not fetched (open); head | FOURTH r1 17 (partly confirmed twice) |
| E5 | Lungman chest phantom | 1 phantom, 1 real radiograph, 2 CTs | not fetched (open); one frame | FOURTH r1 13 (partly confirmed twice) |
| E6 | Veriserum (ETH) | about 110,990 knee-implant phantom frames with poses, no CT | not fetched; non-commercial; planned only as a statistics target | CARM finding 3; STRAT tier 3 |
| E7 | CAMS-Knee | 6 subjects with instrumented knee replacements | signed institutional licence, not requested; knee | CARM finding 4 |
| E8 | Coronary angiography: CADICA, ARCADE, XCAD, AngioCAD | CADICA 42 patients; ARCADE 3,000 images; XCAD 1,747 images; AngioCAD 413 patients | not fetched (STRAT tier 2 plan); thoracic spine in the background, no spine labels | STRAT tier 2 |
| E9 | Pediatric IRI | 95,308 images, 1,357 sequences | not fetched; abdominal angiography with the lumbar spine in the field, no spine labels | STRAT tier 2 |
| E10 | MIQR-CC ERCP | 19,018 frames (Ziehm, Philips) | judged useless: no CT, no spine labels; at most an unlabelled real-domain source | FOURTH refuted_or_useless |
| E11 | Pelphix | 257 cadaver frames with phase labels only, plus simulated sequences | not fetched; no cadaver masks or landmarks; withdrawn as a check | STRAT tier 4 |
| E12 | Penn Vet equine C6 to T1 (lateral radiographs against standing CBCT) | 94 living horses | never released, no route; no images released | FOURTH r2 22 (partly confirmed twice) |
| E13 | XMAPortal biplanar XROMM collections: iguana, turtles, ball pythons, alligators and guineafowl, turkeys, quail, boas, trout and frogfish; non-public trunk studies; UNLV10 canine hip | 3 to 85 animals per collection | open but animal and off-target (the trunk studies on request; UNLV10 gated, judged useless) | FOURTH r2 1 to 9 (partly confirmed twice each); refuted_or_useless |
| E14 | Sets with zero frames: ETH tracking dual-plane fluoroscope (X-ray never switched on); Calgary biplanar knee ("The data are unavailable due to privacy restrictions") | 0 frames | excluded from the census by CARM | CARM finding 7 |
| E15 | CT localizers and scouts with same-patient CT: TCIA beyond CT Colonography; CT Colonography's own; Framingham MDCT (T4 to S1); AGES-Reykjavik (T6 to L4) | about 1,148 to 2,697 TCIA patients; up to 754 CT Colonography patients; 3,529; 5,764 | TCIA not fetched (open); the CT Colonography localizers' state on HOME is unknown; Framingham and AGES on request, not drafted. Fan-beam scouts, not C-arm frames, and no labels | FOURTH r1 7 (confirmed and partly confirmed), r2 25, 26 (partly confirmed twice each); THIRD finding 7; MAN#tcia_ct_colonography |
| E16 | FAU Surgical-Device-Detection | 4 shipped cases, 38 spine projections | refuted twice: the shipped projections are simulated, and the real clinical images "cannot be shared publicly" (N2 lists it as not fetched) | FOURTH r1 10 |
| E17 | Bournemouth/AECC quantitative fluoroscopy frames (OSF z2jby) | sizes disagree: 45,968 frames in 139 folders, about 58 or 89 subjects, or 28,894 frames | judged useless: diagnostic weight-bearing lumbar fluoroscopy at 224 px with no CT and no label files; at most an unlabelled real-domain source | FOURTH refuted_or_useless |
| E18 | Other spine or pelvis items refuted or judged useless: BMTVG / SpineAlign (no X-ray frames); UMN biplane spine osteokinematics (cadaver images withheld, results CC0); ovine cadaveric lumbar DXRS (ex vivo, no CT); orthopaedic screw images (post-operative films, no CT); MFHI femoral head (cropped patches); Vienna porcine head (head only); ferret biplanar videos; Xiamen skeleton-attention registration (does not exist as described); Alphatec dual C-arm pairing (industry, unreleased); HKU sparsity-to-geometry and BIT Geng tumour tracking (title-only leads); CBCT-IQ (no projections); Xia 2018 (pig lung only); Yaniv fiducial phantoms (non-anatomical) | per item | refuted or judged useless as given | FOURTH refuted_or_useless; FOURTH r2 19, 21 |
| E19 | Cohorts judged useless: MrOS Hong Kong (about 2,000 men, 328 with spine QCT; refuted by one verifier), SOF (no CT), Health ABC (one 10 mm CT slice), FORMEN (DXA only) | per item | no volume CT paired with films, or not public | FOURTH r2 24; refuted_or_useless |
| E20 | SPIDER; TotalSpineSeg | MRI 447; MRI 1,404 | out of scope (MRI), not sought | MLHC |
| E21 | Commercial brokers: Segmed, Gradient Health, Shaip, InfoBay AI (AWS), Datarade / FileMarket, TrainingDataPro | not recorded | paid licence, not pursued | PATH |
| E22 | Roboflow Universe sets; ROCOv2 (Hugging Face) and MedPix mirrors | 100 to 1,500 images per Roboflow set, quality uncontrolled; ROCOv2 and MedPix not recorded | not fetched | PATH |
| E23 | Radiopaedia, Eurorad and other figure and teaching-file corpora (366 sources, 534 queries) | not recorded | PARTIAL: harvested into FluoroCap through Europe PMC, Open-i, MultiCaRe, Open-PMC-18M, Wikimedia and video; Radiopaedia not scraped (its terms bar it), application letter drafted, not sent | PATH; mem:fluorocap-dataset.md; REQ item 8 |
| E24 | Other cine sources: Seattle Science Foundation, Mayfield, DMX, Radiopaedia (7 cases), Procedure Guide, Konica DDR, Jefferson, MTFI, Faubel, DARADIA | per letter | requests drafted, not sent; the Seattle and Radiopaedia addresses are unverified | REQ checklist; MAN#fluoro_cine_requests_2026_09_26 |
| E25 | Datasets behind re-implemented radiograph methods: Cina 2021, VertXNet 2024 (its landmarks are the held NHANES set), Kim 2024, Kónya 2021 | not recorded | no code or weights released; datasets not recorded | COMP; mem:xr-benchmark-and-robustness-2026-09-13.md |
| E26 | Literature cohorts behind the priors: Hanhivaara 2020 (3,855 abdominal CTs), Nardo 2012 (4,636 films), Nagata 2025 (551 whole-spine CTs), Sun 2025 (500 UK Biobank controls), Hanhivaara 2024 reader study (100 LSTV cases) | as given | release not recorded | ACQ section 2; mem:lstv-data-landscape.md |

Two things in these tables are not data. First, no drafted request is recorded as sent: SX-Stitch, Balgrist and the
fourteen cine letters all read "Sent: not recorded" (MAN#sx_stitch_request, #balgrist_exvivo_request,
#fluoro_cine_requests_2026_09_26). Second, the negative findings are incomplete: the sweeps record several search
angles that never ran (TUM CAMP, Bern, FAU/CONRAD, raw O-arm and Airo projections, grand-challenge, Gitee and Baidu,
Google Dataset Search, OpenReview, forensic post-mortem CT, interventional torso procedures), so "missing" there means
never looked (N1 section J row 19; MISSED summary; FOURTH coverage note). The PRISMA-ScR scoping review that was meant
to list the field's datasets ran its search but screened nothing and charted nothing, and matched 11 of its 30 known
datasets (N1 row 94).

---

## 3. Size against the comparable studies

Every study cell is as recorded in the file in its source column. Ratio = your n / study n (calc, `LS:t3_ratios.py`).

| task | study | study n | headline result | source | your counterpart | ratio |
|---|---|---|---|---|---|---|
| Radiograph level ID | Chen, VertXNet 2024 | 1,183 images (split not recorded) | no naming accuracy; panoptic quality 0.89 to 0.90 | as recorded in RF18 finding 9 | 9,108 level-bank films (CORP) | 7.70 |
| Radiograph level ID | Kim JK 2024 | 150 radiographs | L5 precision 95.7 %, recall 97.8 % | n as recorded in AUTO (the Kim 2024 entry, which also gives mAP0.5 99.2 %); result as recorded in RF22 section 5.6 | 9,108 films | 60.7 |
| Radiograph level ID | Klinwichit, BUU-LSPINE 2023 | 3,600 patients, 7,200 films | detection mAP 81.93 AP, 83.45 lateral; names no level | as recorded in mem:mixed-length-head-and-sota.md | 9,108 films; 3,603 BUU films used | 1.26; 0.50 |
| Radiograph level ID | Barr 2026 (adjacent: landmarks) | 100 to 700 real films | synthetic prior worth 2.6 to 4.3 times lower error at 100 to 400 real, gone at 600 to 700 | as recorded in SYN | CSXA 4,963 | 7.09 |
| Radiograph level ID | Cina 2021 | not recorded | 98.4 %, a whole-film presence vector | as recorded in mem:mixed-length-head-and-sota.md | 520 whole lumbar films | not computable |
| C-arm naming | Zhang, VDVM 2023 | 31 C-arm test images (382 C-arm + 203 radiographs to train); patients not stated | naming 73.3 % | as recorded in RF22 section 5.1 | 296 frames, 148 cases (TAB3) | 9.55 |
| C-arm naming | Huang, MVMS 2022 | 100 O-arm long films, 13 cadavers | labelling 88.3 % | as recorded in HAI section 5; RF18 | 296 frames; 148 cases | 2.96; 11.4 |
| C-arm naming | Huang, MVMS SPIE 2022 | 50 long films, 14 cadavers | 91.7 % | as recorded in RF22 section 5.3 | 296; 148 | 5.92; 10.6 |
| C-arm naming | Killeen 2025 | 80 images, 1 cadaver | Dice 0.04 per level | as recorded in RF22 section 5.3 | 296; 148 | 3.70; 148 |
| C-arm naming | Desai 2026 (ChatGPT abstract) | 75 cases | 28 % agreement with a neurosurgeon | as recorded in RF22 section 5.1 | 148 cases | 1.97 |
| C-arm detection | Rao 2024, Spine Vision | 578 images, 3 C-arms; test 20 images | recall 0.964 (their model), 0.982 (YOLOv5); no naming | as recorded in RF22 section 5.1 | 778 mobile C-arm frames, 3 mobile C-arms; device-held-out test 56 frames (CORP; TAB3) | 1.35; test 2.80; devices 1.00 |
| Registration | De Silva 2016, LevelCheck | 398 radiographs, 178 CTs | 100 % of labels within the correct level, given a labelled CT | as recorded in HAI sections 3, 4 | 296 frames; 148 cases | 0.74; 0.83 |
| Human readers | Manbachi 2018 | 62 radiographs, 5 surgeons | median error 30.4 % unaided, 2.4 % with LevelCheck | as recorded in HAI sections 1, 2 | no reader study (TAB3) | none against 5 |
| Pose regression | Zheng 2018 | 420 real test X-rays, 42 C-arm CT volumes | failure rate 16.07 % to 11.20 % | as recorded in LED section 2 | 4,276 real frames with 3-D truth | 10.2 |
| C-arm naming | Li 2016; Li 2017; ABLSpineLevelCheck 2024 | not recorded (full texts unread) | not recorded | RF22 section 5.2 | | not computable |
| 2-D LSTV | Kwak 2025 | 3,116 films, 1,941 LSTV; test 195 LSTV of 313 | accuracy 76.4 %, AUC 0.84; one surgeon 83.9 % | as recorded in RF18 finding 12; AUTO C1 | 147 real 2-D positives (144 BUU anomalous + 3 C-ArmLSpine L6); 128 anomalous test films (mem:anomaly-manifest-sources.md; TAB2; mem:feasibility-claims-measured.md) | 0.076; test 0.66 |
| 2-D LSTV | Hanhivaara 2024 (readers) | 100 LSTV patients, 4 readers | radiograph sensitivity 32 %, CT 76 % | as recorded in AUTO; TLJ row 6 | no counterpart | not computable |
| 2-D TLTV | none published | | no detector for T13 or a lumbar rib in 2-D | as recorded in mem:lstv-data-landscape.md | 0 real in 2-D (TAB2) | zero on both sides |
| CT labelling | Sekuboyina, VerSe 2021 | 374 scans, 355 patients; L6 47 cases | top identification 94.25 % and 96.58 % | as recorded in AUTO C4; TLJ row 2 | 802 patients | 2.26 |
| CT labelling | Liebl, VerSe'20 descriptor 2021 | 300 subjects, 319 series; L6 in 85 series | data descriptor | as recorded in AUTO C5; TLJ row 1 | L6 persons 110, of whom 86 are VerSe's own (TAB2) | 1.29; beyond VerSe 24 (0.28) |
| CT labelling | Möller, VERIDAH 2026 (arXiv) | 1,536 CTs (1,171 train, 365 test); anomaly scans about 197 in all, inferred from the cohort rates (the paper prints rates and percentages, not counts); test-side anomaly scans 54 by the rates or 63 by the recall percentages (section 7.2) | all-correct 99.18 %; lumbar-anomaly recall 97.22 % | as recorded in AUTO C2; TLJ row 3; CORR | 802 patients; 129 count-changing transitional persons (TAB2) | 0.52; 0.66 |
| CT labelling | Hanaoka 2017 | 300 CTs, 73 transitional | 211 of 217 normal; 71 of 73 transitional only "partially" | as recorded in AUTO C6 | 802; 194 transitional | 2.67; 2.66 |
| CT labelling | Netherton 2020 | 803 training CTs | identification 94.2 % | as recorded in AUTO | 802 | 1.00 |
| CT labelling | Schinz 2026 | 1,242 CTs | shape-based labelling 100 % | as recorded in TLJ row 7 | 802; T12 against L1 AUC 0.990 (MPDA) | 0.65 |
| CT labelling | NanoxAI HealthOST (FDA K213944) | 150 CTs | 91.49 % agreement; no transitional handling documented | as recorded in AUTO C7 | 802 | 5.35 |
| CT labelling | Elton 2020 | 289 CTs | L1 98 % | as recorded in AUTO | 802 | 2.78 |
| CT labelling | Wasserthal, TotalSegmentator 2023 | 1,204 CTs | no L6, T13 or lumbar-rib class; no Dice figure is recorded in any file on disk (the 0.943 in N3 has no on-disk source) | n as recorded in MPDA line 365 (Table 1); classes as recorded in TLJ and AUTO | 802; your audit: L6 predicted on 0 of 1,152 records (NIPS) | 0.67 |
| CT labelling | CTSpine1K; CTPelvic1K; RibSeg v2; Möller stump ribs | 1,005; 1,184; 660; 648 | datasets | as recorded in MPDA; AUTO C3 | 802 | 0.80; 0.68; 1.22; 1.24 |
| Prevalence | Paik 2013 | 8,280 | six lumbar 8.2 %; type II to IV 10.6 % | as recorded in PREV | 1,113 CT spines with both junction flags (mem:anomaly-manifest-sources.md) | 0.13 |
| Prevalence | Tang 2014; Nardo 2012; Liebrand 2025 | 5,860; 4,636; 4,184 | 15.8 %; 18.1 %; LSTV 5.1 %, wrong level 36 of 214 | as recorded in PREV | 1,113 | 0.19; 0.24; 0.27 |
| Prevalence | Hanhivaara 2020 | 3,855 abdominal CTs | any LSTV 28.6 %; type II to IV 9.0 % | as recorded in PREV; AUTO | 1,113 | 0.29 |
| Prevalence | Sabri 2025 | 3,147 | 8.8 % lack 24 presacral segments | as recorded in PREV; TLJ | 1,113 | 0.35 |
| Prevalence | Doo 2020; Sugiura 2021 | 1,340 CTs; 1,179 CTs | TLTV 11.2 %; LSTV 7.1 to 9.0 % | as recorded in PREV with CORR | 1,113 | 0.83; 0.94 |
| Prevalence | Hanson 2010; Nagata 2025; Yoon 2023; Tins 2016; Apazidis 2011; Carrino 2011 | 750; 551; 450; 418; 211; 147 | six lumbar-type 14.5 %; LSTV 16.3 %; LSTV 26.4 %; transitional 3.3 %; 35.6 %; LSTV 15.0 % | as recorded in PREV | 1,113 | 1.48; 2.02; 2.47; 2.66; 5.27; 7.57 |
| Fiducial localisation (the cost of avoiding the count) | Siminski 2023 (Mayo Clinic) | 179 preoperative gold fiducials over 38 months, 176 thoracic | 51.9 min and 183 mGy each | as recorded in RSN2 line 58 | no fiducial series | not computable |
| Surgical miscount | Nakagawa 2017; Albano 2024 | 71 LSTV of 550 operations; 885 patients over 39 studies | count wrong in 38 of 71; wrong level 12 of 885 | as recorded in LED section 6; PREV with CORR | no surgical series | not computable |

**One verdict per task** (N3 section 6):

- **Radiograph level identification: larger.** 9,108 films against VertXNet's 1,183 images (7.7 times) and Kim's 150
  (61 times); accuracy cannot be ranked, because no published plain-film naming accuracy is metric-comparable and the
  whole-film task is saturated (your model and the count-from-sacrum rule both scored 99.96 % on 520 films, a v2-bank
  measurement now RECORD ONLY, `RESULTS_CATALOG.md` C1.16) (mem:mixed-length-head-and-sota.md, whose own numbers are
  from the leaked allspine v2 bank; mem:feasibility-claims-measured.md). The 9,108 counts the NHANES films that carry
  landmarks; `~/films_drr` holds 9,109 annotation files (`ssn:docs/DATASHEET.md` L165).
- **C-arm naming: larger test, one device, no readers.** 296 frames against VDVM's 31 (9.6 times) and Huang's 100 (3.0
  times); your best number, 97.4 % (601 of 617 lateral vertebrae, 141 cases, Wilson on effective n 93.2 to 99.0), is on
  one device with automatic truth (`RESULTS_CATALOG.md` A3.1, from
  `sn:results/eval_gate/closure/cv_v9/cv_v9.json`; the 98.2 % of 606 of 617 that TAB3 and CLM carm_cv5_lat_whole_exact
  still carry is the superseded v2-lineage run, A3.11).
- **C-arm detection: comparable size, lower recall with the device held out.** 778 frames against Rao's 578 (1.35
  times), 3 mobile C-arms against 3; your held-out-device recall is 80.5 % (231 of 287) against Rao's in-domain 0.964 on
  20 images (RES; LED section 1 forbids "best recall").
- **Registration and human-reader studies: smaller.** 296 frames against De Silva's 398 (0.74 times); no reader study
  against Manbachi's 5 surgeons.
- **2-D LSTV: smaller.** 147 real positives against Kwak's 1,941 (0.08 times), 128 anomalous test films against 195
  (0.66 times); your anchor-free anomalous-film accuracy is 49.9 % [41.5, 58.9] over 128 films against 89.9 % on 453
  ordinary films (mem:feasibility-claims-measured.md). 2-D TLTV is zero on both sides.
- **CT labelling with anomalies: comparable.** 802 patients against VerSe's 355 (2.3 times), VERIDAH's 1,536 (0.52
  times) and TotalSegmentator's 1,204 (0.67 times); 129 count-changing transitional persons against about 197 for
  VERIDAH (inferred from its rates); 86 of your 110 L6 persons are VerSe's own, so beyond VerSe you add 24. No CT L6
  identification rate from your own model is recorded (N3 section 4).
- **Prevalence: smaller than the large series, and not a prevalence sample.** 1,113 flagged CT spines against 3,855 to
  8,280 (0.13 to 0.29 times), comparable to Doo 2020 (0.83 times); VerSe is enriched by design and CTSpinoPelvic1K is a
  colonography cohort aged 50 and over (TLJ row 1; MPDA).

**Transitional test size against the precision it buys** (N3 section 7):

| quantity | yours | comparator, as recorded | ratio | source |
|---|---|---|---|---|
| Test persons with no error needed for a Wilson lower bound of 90 % on exact level | 35 | pre-stated target | | PJ n_needed_zero_errors |
| Carriers with no miss needed for 85 % variant sensitivity | 22 | pre-stated target | | PJ |
| At-risk CT test persons: L6 43, sacralised L5 or four lumbar 5, T13 3 (the definition behind the 129 above) | 51 (bound 93.0 % if all correct) | VERIDAH's CT test anomaly scans, never printed: 54 inferred from the test-set rates (about 29 lumbar and 25 thoracic, AUTO C2) or 63 inferred from the recall percentages (35 of 36 and 26 of 27, CORR) | 0.81 to 0.94 | NUM:436; TAB2; calc_review |
| the same | 51 | VerSe'20 hidden phase: 17 L6 + 2 T13 | 2.68 | NUM:436; AUTO C4; calc_review |
| TAB2's L6, T13 and both sacralised rows (adds 6 sacralised five-lumbar persons, whose count does not change) | 57 (bound 93.7 %) | VERIDAH's 54 or 63, as above; VerSe's 19 | 0.90 to 1.06; 3.00 | TAB2; calc_review |
| Validation and test transitional persons inside the current encoder's training | 92 of 97 | | | TAB2 note d |
| Verified real-frame transitional test persons | 0 (the three C-ArmLSpine L6 are scored only in cross-validation, as agreement with one labeller) | Kwak test: 195 LSTV films | 0 | RES; TAB2 |
| COBRA2026 at-risk persons with an exported frame, two-labeller count | 7 (best-case bound 64.6 %) | | | RES; NUM:435 |

On paper the CT at-risk test (51 persons) is 0.81 to 0.94 times VERIDAH's anomaly test set, depending on which
inference about that set is used, and 2.7 times VerSe's hidden phase. It cannot be scored with the current encoder,
and on real frames there is no verified transitional test person.

---

## 4. Power

N4 section 1 lists 18 power or sample-size calculations, found by grep across `ssn:SchwingNet/results`, `ssn:docs`, `ssn:tools`,
`ssn:SchwingNet/tools`, `ssn:paper`, `ssn:reports`, `ssn:research_notes`, `ctsp:docs` and `ctsp:paper/mpda`. On review the grep was
extended to `ctsp:proposals`, `ctsp:mlhc`, `ctsp:BIBM` and `NextPaper`, and to the whole of `ssn:` for "underpowered",
"80 % power", "n_min" and "powered to"; N4's items not carried into the table below, and what the wider grep found, are
in "Other power statements" after it. The table takes each comparison you make or plan. "First n" is the smallest n at
which power reaches the level; exact-test power is sawtoothed, so "always from" gives the n from which it holds. Where
no file holds a calculation, the row says so and lists the inputs a calculation would need.

| # | comparison | effect size or true accuracy assumed, and source | n today, and source | power today | n for 80 % power | n for 90 % power |
|---:|---|---|---|---|---|---|
| 1 | Accuracy difference between devices, at device level (fitted card against uncalibrated physics) | none assumed. Observed: card gain 0.025 frame-weighted over 835 frames; all four device means positive (NUM:146; SR1 R2_card) | 4 devices, 24 folds (NUM:146) | No file computes it. With 4 devices the smallest two-sided sign-flip P is 0.125 (printed P = .13), so power at alpha 0.05 is 0 whatever the effect (calc). Fold level: P 0.00023 (NUM:146) | No calculation exists. calc: at least 6 devices before any two-sided P of 0.05 or less is attainable. Inputs needed: per-device effect and its spread | no calculation exists |
| 2 | Same-device frames needed for detection (C-ArmLSpine) | none; fitted asymptote 81.7 % lateral, 85.3 % AP (FITN) | up to 200 real frames per arm, 28 test patients (FITN) | not a power calculation: 95 % of the asymptote at 10.0 lateral and 11.9 AP frames; 90 % absolute recall not reached (FITN) | not applicable (learning curve) | not applicable |
| 3 | Same-device persons needed for naming (C-ArmLSpine) | none; fitted (FITN) | 87 training persons per view (PJ panel_b_carm) | not a power calculation: AP 67.6 persons to 97 %, 1,071 to 99 %; lateral 12.1 to 97 %, 1,064 to 99 %; asymptote not identified (FITN) | not applicable | not applicable |
| 4 | Held-out-device (LODO) against same-device (pooled) detection | none assumed. Observed: 98.2 % against 83.9 %, +14.3 points [5.4, 23.2] (NUM:131) | 28 C-ArmLSpine test cases, 8 better and 0 worse (NUM:131) | Decided at this n on one device: Holm P 0.0078 printed, 0.016 counting the card test (RS2 N9; SR2 S8). No a priori calculation. calc: an exact sign test needs 6 discordant cases all one way for P of 0.05 or less, 8 for 0.0125 | Across devices: no calculation exists. Inputs: per-device discordant-case rate, cases per device | no calculation exists |
| 5 | Synthetic-to-real ratio | none. No DRR or fluoroscopy paper has swept the ratio; other modalities flatten at 4:1 to 10:1 (as recorded in SYN section 1); the flagship fixes real at 10 to 20 % (FP) | no ratio sweep run. Render rows against film only: +21.9 / +11.1 / +18.7 points at 5 persons and +12.2 / +6.0 / +6.2 at 25 (NHANES II / BUU-LSPINE / CSXA) (ABL) | no calculation; 7 of 9 pre-stated cells separated (ABL) | No calculation exists. Inputs: the ratio grid, real-frame n per arm, between-seed SD per cell (in ABL), test persons per corpus, intraclass correlation of frames within a person | no calculation exists |
| 6 | Naming accuracy on transitional against ordinary spines | none assumed. Observed: anomalous films 49.9 % [41.5, 58.9] (128 films) against ordinary 89.9 % [87.1, 92.7] (453 films), anchor-free interior windows (mem:feasibility-claims-measured.md); L6 named 44.9 % with no anchor on anomalous BUU films (same note); render L6 recall 56.1 to 72.4 % on 10 held-out L6 spines (LCM section 8) | 10 L6 evidence persons on renders, 0 T13; 3 real L6 excluded from the primary analysis (LCM section 4) | no file computes it | calc (two-sided alpha 0.05, Cohen's h): 19 per arm at design effect 1, 74 at design effect 4 (`LS:calc_addendum.json`); design effects of 3.84 to 4.47 were measured for lateral naming (NUM:419, NUM:463) | calc: 25 per arm at design effect 1, 99 at 4 |
| 7 | Count against count plus morphology on transitional persons (paper 2, M1) | none assumed. Development: coupled better on 3 cases, worse on 0, ties 127, sign P 0.25 (SR2 S6; RS2 N3) | none scored (GATE) | not computed; the test runs only with at least 6 discordant persons (LCM section 12); calc: 6 all one way is the fewest for one-sided P of 0.025 or less | No calculation exists. Input: the discordance rate among transitional persons | no calculation exists |
| 8 | L6 detection (Wilson lower bound of variant sensitivity at least 85 %) | true 95 to 99 % in the planning tables, with no measurement behind it (SR1 R4); development L6 recall 56.1 to 72.4 % (LCM section 8) | 43 CT test persons, but 49 of 54 validation and test L6 persons are in the encoder's training lineage (TAB2); real: 3 C-ArmLSpine L6 excluded, 3 COBRA2026 two-labeller L6 (NUM:435) | at 43 carriers with one miss allowed: 0.36 / 0.63 / 0.79 / 0.93 at a true 95 / 97 / 98 / 99 % (calc); at a recall of 72.4 %, P(22 of 22 found) = 0.0008, and the probability of meeting the bound reaches 80 % at no n (calc) | floor 22 carriers with no miss (PJ); calc first n 74 / 45 / 34 / 22 at 95 / 97 / 98 / 99 %; 347 at 90 %; never at 72.4 % | calc: 92 / 55 / 45 / 34; 461 at 90 % |
| 9 | T13 detection (same 85 % target) | as row 8; no T13 recall can be measured: "no validation film carries one" (`ssn:SchwingNet/results/ALPHABET_LOSS.md`) | 3 CT test persons, 0 real (TAB2); 7 T13 persons in all sources (TAB2), 14 in the registry (REG table A) | 0, below the 22-carrier floor (PJ; RS1 F17) | at least 22 carriers with no miss (PJ); about 55 T13 people in total under the 50/10/40 split (calc, N4 section 4) | as row 8 |
| 10 | Paper 1 exact level (Wilson lower bound at least 90 % on transitional test persons; FP gate G6) | true 95 to 99 % planning values (SR1 R4), unsupported by any transitional measurement (RS2 N1) | 51 at-risk CT test persons, most in the encoder's training data (NUM:436; TAB2); 7 real at-risk persons by a two-labeller count (NUM:435); 0 verified real (RES) | at 51 with no error allowed: 0.07 / 0.21 / 0.36 / 0.60 at 95 / 97 / 98 / 99 % (calc); at 7: 0, best-case bound 64.6 % (NUM:435) | 99 at a true 97 %, 69 at 98 % (SR1 R4); calc 217 at 95 %, 53 at 99 % | calc: 291 / 127 / 84 / 53 at 95 / 97 / 98 / 99 % |
| 11 | LevelCheck H1 (paper 2: at-risk persons, superiority over 82.2 %, the Peh 1999 coronal localiser) | true 90 / 95 / 97 % planning values (LCM section 7) | primary is real frames: 7 two-labeller at-risk persons (NUM:435), below n_min 19 (LCM section 5); 57 COBRA2026 screen calls supported by their field, unverified (TAB2 note e); 51 CT persons as a secondary analysis | at 7: 0 (ineligible). P(at least 19 of the 57 calls confirmed) = 0.00007 at the labeller's CTSpinoPelvic1K PPV, 0.30 at its upper limits (SR2 S4). At 51 CT persons: 0.24 / 0.75 / 0.93 / 0.998 at 90 / 95 / 97 / 99 % (calc). If the true accuracy equals the COBRA2026 anchor rate of the frozen sacrum detector, 3.4 % (21 of 609 frames), power is 0 (SR2 S12, `H1_power_if_true_equals_cobra_anchor_rate`) | 162 (always from 175) at 90 %; 55 at 95 %; 71 at 95 % under Holm alpha/3 (SR2 S1); calc 38 at 97 % | calc: 208 (always from 228) at 90 %; 63 (always from 70) at 95 %; 47 at 97 % |
| 12 | LevelCheck H2 (superiority over 97.6 %, the median of Manbachi's five surgeons) | true 95 / 99 % (SR2 S1) | as row 11 | 0 below 152 persons at any true accuracy (LCM section 13); at most 0.00041 at a true 95 % for n up to 2,000 (SR2 S1) | 708 (always from 763) at a true 99 % (SR2 S1); never at 98 % within 1,300 (calc) | 922 (always from 974) at 99 % (calc; LCM section 13 gives the same for accepted persons) |
| 13 | LevelCheck H3 to H5 (per subtype against 82.2 %) | as row 11 | CT test: L6 43, sacralised L5 5, T13 3 (TAB2); real: L6 3, four-lumbar 4, T13 0 (NUM:435) | H4 and H5 ineligible on every count (n below 19); H3 ineligible on real frames (LCM section 5) | n_min 19 (23, 25, 28 at the Holm steps) (LCM section 5) | as row 11 |
| 14 | LevelCheck H6 (ordinary spines, non-inferiority against 92.6 %, a margin chosen knowing the development results) | true 95 / 97 / 98 / 99 % (SR2 S3) | at most 51 ordinary real-frame persons (COBRA2026 41, C-ArmLSpine 10) (SR2 S3); only 13 reference-ordinary COBRA persons are in the open gate and the 10 C-ArmLSpine persons have no reference (RES22 lines 679 to 688); 103 COBRA test persons have no automated reference (GATE) | at 51: 0.07 / 0.21 / 0.36 / 0.60 (SR2 S3); at 13: 0, below n_min 48 (calc). With the frozen detectors the illustrative expected H6 accuracy is about 0.14, power 0 against 92.6 % (SR2 S12, `H6_illustrative_expected_accuracy`) | calc: 210 (always from 245) at 97 %; 136 at 98 %; 73 (always from 95) at 99 % | calc: 262 (296) / 155 (173) / 95 (116) |
| 15 | LevelCheck S1 (accepted-person accuracy against 97.6 %, selective) | true accuracy of accepted persons 99.9 / 99.5 / 99.0 % (LCM section 13) | none scored | 0 below 152 accepted persons (LCM section 13) | 152 (always from 230) / 299 (363) / 708 (763); against 0.97: 122, 239, 386 (LCM section 13) | 230 / 424 / 922 (always from 974) (LCM section 13) |
| 16 | A 99 % selective-accuracy claim for level naming | zero errors, one-sided 95 % confidence | 2,956 answered held-out renders at 99 % (mem:selective-prediction-the-honest-99.md) | not a power calculation | about 298 answered cases; class-conditional 99 % needs at least 99 real calibration cases per class, 2,673 at 27 classes (as recorded in mem:selective-prediction-the-honest-99.md) | not recorded |
| 17 | Wrong-level events under the QI localisation protocol | wrong-level rate 0.12 % | not applicable | "powered to estimate, not to detect a change in wrong-level events" | "tens of thousands of cases" (`ssn:paper/qi_universal_protocol/main.tex` lines 229 to 231) | not recorded |

**What the frozen endpoint does to rows 10 to 15.** The paper-2 endpoint scores a person wrong for a missed body, an
unanchored frame or an abstention, not only for a wrong name (LCM section 4). On ordinary C-ArmLSpine development frames
that endpoint held on 162 of 284 frames (57.0 %), and naming failed on 1 (SR2 S11). The COBRA2026 sacrum detector fixed
for the primary analysis found the sacrum on 21 of 609 frames (3.4 %) (SR2 S12). LCM section 15 replaced those detectors
before unblinding, and no file recomputes the power under the replacement.

**The comparators' own n** (each as recorded in the file named):

| comparison | published study | its n | your n today |
|---|---|---|---|
| LevelCheck comparator | Manbachi 2018, study 1 | 5 surgeons, 62 radiographs; no denominator or interval for 97.6 % (LCM section 2) | 7 unverified at-risk real-frame persons (NUM:435) |
| LevelCheck comparator | Manbachi 2018, study 2 | 20 operating-room patients, 20 of 20 correct (LCM section 2) | at most 51 ordinary real-frame persons, 13 with a reference (row 14) |
| Planning-read miscount | Nakagawa 2017; Peh 1999; Yun 2018; Albano 2024 | 71 LSTV of 550 operations; 129 patients with 17 LSTV; 100 variant patients of 1,446 CTs; 885 LSTV surgical patients over 39 studies (LCM section 2) | 194 transitional persons in all sources (TAB2) |
| CT transitional labelling | VERIDAH | 1,171 training CTs with 60 thoracic and 83 lumbar enumeration anomalies (SYN); test-side anomaly scans never printed: SYN states 25 and 29 as counts, but they are inferred, 54 from the rates (AUTO C2) or 63 from the recall percentages (CORR) | L6 110, T13 7 (TAB2); registry L6 146, T13 14 (REG) |
| When L6 becomes learnable | VerSe'20 | L6 in 85 scans of the release, 28 of them in training, which sufficed; T13 in 6 "never stabilised" (SYN; mem:lstv-data-landscape.md) | 18 distinct CTSpinoPelvic1K L6 cases gave L6 Dice 0.000 under 12-fold duplication (mem:l6-sample-count-and-counting-decoder.md) |
| Confirmation at a transitional vertebra | none published: no study stratifies naming by anomalous spine (HAI finding 8) | none | 18 CTSpinoPelvic1K L6 spines with 3 seeds, 54 runs per arm: 45 chains with one node per body and 36 runs naming L6 on clean renders, 45 and 35 under the film noise model (RSN2 line 75; `ssn:paper/rsnai/claims.tex` lines 46 to 50); not in the current manuscript |
| Synthetic and real mixing | Barr 2026; Gherardini 2020; SyntheX; DeepDRR | 100 to 700 real films; 240 real frames; 366 real frames from 6 cadavers; 78 real cadaver images (SYN sections 1, 2) | film curves to 264 (NHANES II), 2,967 (BUU-LSPINE), 4,114 (CSXA) persons; C-arm naming to 87 persons per view (PJ) |

**Where power stands, in four sentences** (N4 section 6). Every powered statement so far rests on planning accuracies of
95 to 99 % that no transitional measurement supports, and the transitional figures on disk (render L6 recall 56.1 to
72.4 % [SEL-SPLIT]; L6 named 44.9 % with no anchor on anomalous films, SUPERSEDED; 49.9 % on anomalous film windows,
RECORD ONLY [LEAK]; see the status table at the top) would put every transitional test at or near zero power; no
held-out transitional measurement exists, so this is a planning statement (RS2 N1; SR2 S2; rows 6, 8, 10). The one comparison already decided at its n is held-out-device
against same-device detection on one device (28 cases, 8 to 0), and device-level claims cannot be tested with 4
devices (rows 1, 4). Paper 1's 90 % target needs 35 error-free at-risk persons and paper 2's primary H1 needs 19, while
7 unverified real at-risk persons exist and the 51 CT test persons are mostly in the encoder's training lineage (PJ; LCM
section 5; NUM:435 to 436; TAB2). The 97.6 % LevelCheck figure cannot be exceeded at any reachable n (152 error-free
persons give 0.22 power at a true 99 %) (LCM section 7).

**Other power statements on disk.** N4's items not carried into the table above, and what the wider grep found. None of
them is a power calculation for a claim of paper 1 or paper 2 except where the row says so.

| file and line | statement, as the file gives it | what it rests on |
|---|---|---|
| PT (`lower_bound_pct_by_k_then_n`; N4 item 1) | Wilson lower bound with 0 errors: 88.65 % at 30 persons, 92.13 % at 45, 93.98 % at 60, 96.3 % at 100; its inventory (89 persons, 37 test persons, bound 90.59 %) is superseded | a bounds table, not power (section 7.2) |
| NUM:52, marked SUPERSEDED 2026-09-24 (N4 item 14) | at the planning accuracy 98.2 % (606 of 617), 80 % power for the 90 % bound at n = 69; exceeding 97.6 % first at n = 4,276; 99.3 % never; "No longer in the manuscript" | a C-arm per-vertebra accuracy used as a person-level planning value; Figure 5 was rebuilt on the frozen exact test |
| `ssn:tools/anomaly_cooccurrence_from_labels.py` lines 3 to 6 (N4 item 15) | thoracolumbar and lumbosacral anomaly co-occurrence in CTSpinoPelvic1K: odds ratio 4.00 (1.00 to 16.03), "underpowered on its own" | a both-anomaly cell of two cases |
| `ssn:docs/MORNING_BRIEF_2026-09-16.md` lines 79, 123 (N4 item 16) | BUU label noise: "n=80, no power"; 33 shifted films: "no power" | no calculation |
| `ssn:docs/FLUORO_DATASET_STRATEGY.md` line 177 (N4 item 17) | the SyntheX parity reading: a landmark difference at P = 0.14 is "an underpowered null" (as recorded there) | SyntheX's own test, not re-computed |
| MPDA lines 919 to 921 (N4 item 18) | no power calculation; a whole-cohort Castellvi read "would test the co-occurrence ... at full power" | no calculation |
| `ctsp:proposals/review/MANUSCRIPT_wrong_level_scoping_review.md` lines 182 to 185, 356 | "the test is underpowered": among 45 sources that name a countermeasure, 72.2 % (49.1 to 87.5) against 70.4 % (51.5 to 84.1), Fisher P = 1.000, odds ratio 1.07 (0.30 to 3.84); sensitivity analysis on 603 sources, odds ratio 0.95 (0.36 to 2.50) | a scoping-review Fisher test, not this programme's claims |
| `ctsp:mlhc/full-paper-template.tex` lines 1141 to 1144; the same sentence in `ctsp:BIBM/IEEE_Conference_Template__3_/full-paper-template_MLHC.tex` lines 1142 to 1143 and `NextPaper/AR/full-paper-template.tex` lines 954 to 955 | running zero-shot TotalSegmentator on the full matched cohort rather than the 52-case test split "materially increases the statistical power of the LSTV-subgroup analysis" | no calculation behind it |
| RES22 lines 255 to 257 | real-frame test persons on 2026-09-22: 56 COBRA2026 persons assigned ordinary (44 with frames); "H6 n_min is 48, so H6 is 4 persons short on automated truth alone" | the LCM section 5 n_min; superseded by the 51 and 13 of row 14 |
| RES22 lines 674 to 677 | one-sided exact binomial at alpha 0.05: with 44 to 56 ordinary test persons, superiority over 0.976 is impossible even at 44 of 44 (P = 0.34) or 56 of 56 (P = 0.26); H2 n_min is 152 with zero errors, "~300 for 80 % power at a true 0.995" | alpha 0.05, not the frozen 0.025 of row 12 |
| ACQ sections 2 and 3; `ssn:tools/acquisition_census.py` (N4 item 10) | the acquisition stopping rule: fetch in order of expected transitional people per TB, none below 20 per TB; CEN section 2 adds a CephFS floor of 5 TB and an acquisition cap of 8 TB, and says the rule refuses NLST as it stands | an expectation rule from prevalence priors, not a power calculation |

The rest of the wider grep repeats n_min values already in rows 11 to 15 (for example
`ssn:SchwingNet/results/auto_reference/CALIBRATION.md` line 112 and `ssn:SchwingNet/CLAIMS_LEDGER.md` lines 271, 282) or sits in code and
figure captions.

---

## 5. The transitional-anatomy count: expected against called

The expectation is the acquisition plan's formula: for each new person, P(both lumbosacral references in the field) times
the LSTV prior (9 % low, from Hanhivaara 2020; 18 % high, from Nardo 2012), plus P(rib cage from T1) times the T13 prior
(0.64 % from VertebralBodiesCT-Labels, to 2.0 % from Sun 2025); E_count is what a mask count can call with no reader
(4.8 % = L6 3.2 % + four-lumbar 1.6 %, Sun 2025) (ACQ section 2; priors as recorded in `ssn:tools/acquisition_census.py`
lines 17 to 26). These are expected values, not calls.

### 5.1 The acquisition blocks (ACQ opening table)

| block | collections | new CTs (people, at most) | expected transitional people, E_low / E_high | callable by a mask count (E_count) | status |
|---|---:|---:|---:|---:|---|
| tier 1, fetching since 2026-09-23 | 45 routes + NLST pilot | 15,233 | 831 / 1,703 | 460 | fetched; flagged by the screen (TIERS), read by no one |
| tier 1, late (2026-09-24) | 10 | 3,365 | 163 / 336 | 91 | mostly fetched; PANORAMA 1,114 CTs pending the screen (TIERS section 0) |
| tier 2 | 17 | 30,486 | 153 / 456 | 144 | planned, held by stopping rule 4 |
| deferred or unresolved overlap | 7 | 3,536 | 187 / 387 (if every person were new) | 105 | route not written |
| gated | 7 | 70,764 | 1,791 / 3,848 | 1,066 | no form signed |
| excluded or no new countable people | 59 | | 4 | | |

Two expectations already missed: AMOS kept 723 of its 2,364 CTs at 3 mm or thinner, about a third of its predicted
people, and the NLST pilot's 9.3 % T13 rate was five to fifteen times its prior and wrong (ACQ sections 9, 11).
AbdomenAtlas matched its prediction (7,649 of 9,262 usable against 7,835 predicted) (ACQ section 9).

### 5.2 What the holdings should contain, against what has been called (N4 section 4)

| block | CTs on disk, and lumbosacral-countable people | expected L6 | expected four-lumbar | expected Castellvi II to IV | expected T13 | called so far |
|---|---|---:|---:|---:|---:|---|
| CTSpinoPelvic1K, 802 | 802 on disk; 789 countable (FOV ctsp_all 0.984) | 25.3 (calc) | 12.6 (calc) | 71 to 142 (calc) | 0; no rib cage in the colonography field (FOV) | read: L6 18 by release label and 16 by the readers' own count (CORR), four lumbar 9, Castellvi-graded 33 (MPDA lines 622, 773 to 779, 239); registry: L6 29, sacralised L5 fused 12, Castellvi I/II 4, lumbar rib 14, unassigned 5 (REG tables B, C) |
| TotalSegmentator v2, 1,228 | 1,228 on disk; 483 lumbosacral, 471 cage (calc over FOV) | 15.5 | 7.7 | 43 to 87 | 3.0 to 9.4 | registry over 1,935 TotalSegmentator keys: L6 22, T13 4, unassigned 26, unresolved 74 (REG table B) |
| COBRA2026, 692 planning CTs | 692 on disk; 435 readable by the screen (COBS) | 13.9 | 7.0 | 39 to 78 | not computable (cage coverage not recorded) | one-labeller screen: L6 38, T13 45, four-lumbar 8 (COBS); registry keeps L6 3 (REG table B) |
| 18 screened acquisition collections | 16,898 on disk, 12,123 passing the field gate (CEN section 1; both run one too high in every collection checked but PANORAMA, MAN§4.37); about 10,060 lumbosacral-countable, the sum of CEN's per-person probabilities behind its 322 expected L6 (322 / 0.032, calc_review) | 322 | 161 | 907 to 1,813 | 38 to 119 | 2026-09-25: L6 two-labeller 21, single 18; T13 single 16; review 84 (CEN section 1). 2026-09-27 flags on tier-1 CTs: L6 303, T13 82, both 1, unassigned 368, review 1,168 (TIERS section 1) |
| RibFrac, 660 | 660 on disk; 459 cage, 0 lumbosacral (RANK) | 0 | 0 | 0 | 2.9 to 9.2 | registry: T13 4 single-labeller, L6 1 morphology-only (REG) |
| VerSe, 355 persons | enriched by report search, not a prevalence sample | | | | | registry: L6 85, T13 6, sacralised L5 13, Castellvi I/II 27, lumbar rib 12 (REG table B) |
| C-ArmLSpine, 149 CBCTs | 0: lumbar-only CBCT, "neither could count" (LCM section 4) | | | | | registry: L6 3 morphology-only (REG table C) |
| **total, excluding VerSe, C-ArmLSpine and phantoms** | about 20,280 CTs on disk (802 + 1,228 + 692 + 16,898 + 660) of the 21,622 census CTs (TIERS section 1); about 11,770 lumbosacral-countable people (789 + 483 + 435 + about 10,060; 377 / 0.032 = 11,780) (calc_review) | **377** | **188** | **1,061 to 2,120** | **44 to 138** | registry over every stream but the acquisitions: L6 146, T13 14, sacralised L5 fused 27, Castellvi I/II 31, lumbar rib 26, unassigned 62, unresolved 129 (REG table A) |

The total double-counts the 71 TotalSegmentator validation CTs (about 2 expected L6), and other cross-collection
duplicates are not removed (TIERS section 8).

What the comparison says:

- **CTSpinoPelvic1K sits at or a little below the priors where it was read.** The readers' own count gives L6 in 16
  of 789, 2.0 % (Wilson 1.3 to 3.3 %), against a 3.2 % prior; the release label gives 18 (2.3 %, Wilson 1.4 to
  3.6 %), and the seven records where the two disagree are out of every lumbosacral truth pool until re-read (CORR;
  calc_review). Four-lumbar 9 of 789 is 1.1 % against 1.6 % (calc). Only 33 records carry a Castellvi grade against
  71 to 142 expected, and the article names a whole-cohort Castellvi read as work still to do (MPDA lines 919 to 921);
  that gap is an unread cohort, not a measured shortfall.
- **The COBRA2026 one-labeller screen runs far above the prior and is not trusted.** 38 L6 of 435 is 8.7 % (calc)
  against 3.2 %, with 45 T13 calls on abdominopelvic CTs; the same labeller matched reader truth on CTSpinoPelvic1K in
  10 of 24 L6 and 0 of 52 T13 (SR2 S4). The registry keeps 3.
- **The acquisition screens match the expected total at face value, which is not evidence.** 303 L6 flags sit near
  322 expected, but on 70 outside-labelled CTs the screen found 12 of 28 L6 (labeller A), 17 of 28 (B) and 9 of 28 (both)
  (CEN caveats). A screen that finds a third to two-thirds of the true cases and still flags about as many as expected is
  carrying false positives.
- **T13 is the scarce class everywhere.** 44 to 138 T13 people are expected in the whole holding, almost all from
  chest-containing fields; the 85 % sensitivity bound needs 22 test carriers, about 55 T13 people in total under the
  50/10/40 split, and the low end (44) falls short before any call fails verification (PJ; calc).
- **L6 is not short in number; verification is.** 377 L6 and 188 four-lumbar people are expected, against the 85 L6
  scans in the VerSe'20 release, of which the 28 in training sufficed to make L6 learnable there (as recorded in SYN).
  No acquired CT has a radiologist read (ACQ section 9).

---

## 6. The research this rests on

Every prior research report, verified sweep, prior-art note, dataset review, memory note and dataset or review PDF on
disk, newest first: 114 files (N1 sections A to G). The date is the latest date the file carries, with how it is known
(stated in the file, mtime, git, or a memory note's modified field). Path roots: `S/` = `ssn:`, `C/` = `ctsp:`, `M/` =
`mem:`. "Voted" means a deep-research harness put each claim to three adversarial verifiers, with counts of claims
extracted / verified / confirmed / refuted; "read from source" means numbers were read from the primary text with no vote;
"identifiers checked" means DOIs and PMIDs were resolved. The full row for each file, with every dataset and study it
names and the n it records, is in N1 (row number in the last column); "row n" inside a cell means N1 row n. N1 section H
lists the files considered and left out.

| date | file | question it answered | conclusion, as recorded in the file | verification | N1 row |
|---|---|---|---|---|---:|
| 2026-10-08 (modified) | `M/data-platform-migration-2026-10.md` | Where the data manifest and the migration plan live | The manifest that the later topics cross-reference against is in `S/data_platform/`. | Not a review (pointer to the manifest). | 114 |
| 2026-09-27 (modified) | `M/ruleclass-super-detector-run.md` | The transitional screen over the whole CT census | The census screen is the segmentation source for the transitional review tree, and C-ArmLSpine is the only CT-and-radiograph pairing in it. | Not a review (own run). | 113 |
| 2026-09-26 (stated) | `S/docs/FLUORO_VIDEO_SOURCES_2026-09-26.md` | Every public source of spine fluoroscopy video, for a temporal test set | No open download of spine fluoroscopy video with vertebra labels exists, and the next step is to ask Bournemouth for the cine. | Voted (workflow wf_0a5da043-1a5): 106 / 25 / 21 / 4. | 46 |
| 2026-09-26 (mtime) | `C/panjabi_1976.pdf` | Panjabi 1976, three-dimensional flexibility and stiffness of the thoracic spine | Thoracic segmental flexibility data; `M/polypose-decision.md` bounds PolyPose by Panjabi's segmental range of motion, but which Panjabi source that bound uses was not checked here. | Saved primary source. | 90 |
| 2026-09-25 (git) | `C/paper/mpda/main.tex` (Introduction, the prior-art table `tab:priorart`, Discussion) | How CTSpinoPelvic1K compares with the public CT collections at the lumbosacral junction | No prior public collection can record a six-lumbar spine together with both of its borders, and CTSpinoPelvic1K is, to the authors' knowledge, the largest spine-and-pelvis annotated CT cohort acquired under one protocol. | Not a sweep. A citation check file exists (`C/paper/mpda/CITATION_CHECK.md`), not read for this note. | 55 |
| 2026-09-25 (modified) | `M/acquisition-space-saturation.md` | Why the fluoroscopy plateau sits where it does | Accuracy follows where frames sit in acquisition space, not how many there are. | Not a review (own result); the AI review it mentions is row 103. | 73 |
| 2026-09-25 (modified) | `M/carm-plateau-is-the-denominator.md` | Why same-device C-arm detection plateaus at 82 % to 85 % | The plateau is the truth denominator (cut slivers, disagreed levels, poor registrations), and recall on the clean subset is 96.9 %. | Not a review (own diagnostic). | 74 |
| 2026-09-24 (stated) | `S/docs/DATASHEET.md` | A Gebru-style datasheet for every corpus behind the RSNA AI manuscript | Every corpus is a public release or synthesised from one, no new patient images were acquired, and two split defects shipped and were not yet repaired. | Not a review; every count carries the file it was read from, and missing counts are marked "not recorded". | 42 |
| 2026-09-24 (stated) | `S/spine_data_review/` (README.md, PROTOCOL.md, `runs/2026-09-23/prisma_counts.json`, `screen/known_items.csv`, `data/screening/decisions.csv`, `charting/validation_report.json`) | A PRISMA-ScR scoping review of every publicly described spine CT and projection-radiography dataset: annotation origin, variant labels, licence, and availability tested by code | The search ran, but no screening decision has been recorded (`decisions.csv` holds only its header) and no dataset has been charted (0 records), so the review has no results yet. | Not voted. The protocol was frozen before the search. Screening and charting were never done. | 94 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/CITABLE_CLAIMS.md` | Which claims of an AI-generated review (row 103) can be cited, and with which primary source? | The review's "90 % fluoroscopy plateau against 99 % radiograph parity" is the project's own result, not literature, and several of its other claims are partly true or contradicted. | Identifiers checked: each claim was checked against PubMed, Europe PMC, Crossref, arXiv or PMC and graded VERIFIED, PARTLY, NOT FOUND or CONTRADICTED. | 96 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/lit_ct_lstv_automation.md` | Is there a published automated LSTV or enumeration-anomaly detector on CT? | No published CT LSTV classifier has been validated against radiologist Castellvi reads; what exists on CT is enumeration-anomaly labelling, and no FDA-cleared naming tool documents LSTV handling. | Read from source (every number read on the named page or PDF). Errors found later are listed in row 99. | 97 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/lit_prevalence_and_definitions.md` | What prevalence and agreement figures should a CT transitional census land inside? | Prevalence depends on modality and definition: about 29 % any-type LSTV on CT but about 9 % to 11 % type II to IV, and 25 presacral segments in about 5 % to 8 %, 23 in about 3 % to 5 %. | Read from source (PubMed, Europe PMC, PMC); abstract-only rows marked. Corrections in row 99. | 98 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/CORRECTIONS.md` | Which statements in rows 97, 98 and 100 were wrong? | The notes are left as written, and these corrections apply to them. | Identifiers checked (verifier pass, 2026-09-24). | 99 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/lit_tl_junction_and_enumeration.md` | What does the literature say about the thoracolumbar junction and enumeration on CT? | A shape-based reading of the thoracolumbar junction beats counting, and no public CT segmenter has T13, L6 or lumbar-rib classes except VERIDAH. | Read from source; numbers read by the fetch tool's extractor are flagged as second-hand. Corrections in row 99. | 100 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/positives_census.md` | How many reader-labelled transitional persons are available for a CT phenotype classifier? | Reader-labelled positives are small and fixed, and segmenter calls are candidates, not labels. | Not a review (inventory; every number copied or computed from a named file). | 101 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md` | What already exists to build and validate a CT transitional-phenotype classifier without new human reads? | The features and calibration harness exist, and the binding limit is the small number of human-read positives. | Not a review (inventory of own files). | 102 |
| 2026-09-24 (stated) | `S/SchwingNet/lit/acquisition_space_review_2026-09-24.pdf` and `.txt` | "Advanced Computational Frameworks for Vertebral Body Detection and 2D/3D Registration in Intraoperative Fluoroscopy" | Detectors plateau on fluoroscopy because routine data over-represent AP and lateral views. | AI-generated (the file's own note says so). Its claims are graded one by one in row 96, and `M/acquisition-space-saturation.md` says to cite nothing from it. | 103 |
| 2026-09-23 (mtime) | `S/reports/Synthetic real ratio X-ray detectors.md` | For a DRR-trained C-arm detector with few real frames, which synthetic-to-real ratio, real-frame count, rare-class oversampling and render budget does the literature support? | No DRR study has swept the synthetic-to-real ratio; adjacent sweeps flatten at 4:1 to 10:1, real-frame gains flatten at 300 to 700 frames, and the only rare-class levers with numbers are distinct real cases (85 L6 scans in VerSe'20) and VERIDAH's 4x oversampling. | Read from source (its four notes, rows 2 to 5, say numbers were read from full text unless marked abstract-only). Not voted. The report flags one value for re-check itself: Barr's de novo error of 7.42 at both n = 600 and n = 700. | 1 |
| 2026-09-23 (mtime) | `S/research_notes/Synthetic real ratio X-ray detectors/fidelity_vs_ratio.md` | Does the physics or style fidelity of synthetic X-rays change how much real data is needed, or the best ratio? | Physics fidelity has been measured only with zero real training data, and no paper adds real images to physics renders and sweeps the ratio. | Read from source; "abstract only" marked where so. Three numbers from a faulty SyntheX summary were discarded and listed so they are not reused. | 2 |
| 2026-09-23 (mtime) | `S/research_notes/Synthetic real ratio X-ray detectors/mixing_ratios.md` | Which sim-to-real X-ray papers swept the ratio or the real-image count, or fine-tuned on N real images? | None of the physics-simulation flagships sweeps the ratio or the real count; the only sweeps are in guidewire, cervical-radiograph and chest-radiograph generative work. | Read from source: 20 papers in full text, 9 abstract-only (Bier 2019, FluoroSAM, XraySyn, DiffPose, Esfandiari 2018, Grupp 2020, Arrabi 2025, Jung 2026, Viviers 2024). | 3 |
| 2026-09-23 (mtime) | `S/research_notes/Synthetic real ratio X-ray detectors/rare_class_oversampling.md` | What is the measured effect of oversampling a rare class, especially a transitional vertebra, on rare-class recall and common-class accuracy? | No spine paper synthesises L6, T13 or Castellvi cases; the two levers are more real cases and VERIDAH's 4x oversampling, and neither has an ablation. | Read from source; claims taken only from a search summary are marked "(unverified)" or moved to the gaps. | 4 |
| 2026-09-23 (mtime) | `S/research_notes/Synthetic real ratio X-ray detectors/scaling_and_curricula.md` | Where do YOLO detectors and ResNet classifiers on radiographs show diminishing returns, and which synthetic and real curricula were measured? | No YOLO learning curve on radiographs near 1024 px exists; the chest-radiograph classifier knee is near 20,000 images, and the carpal detector passed 0.95 at 96 to 100 radiographs. | Read from source; abstract-only items marked. | 5 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/biomech.md` | Can biomechanical or articulated models generate new labelled spine CTs at a commanded lordosis or phenotype? | The polyaffine warp is citable prior art, finite elements are the wrong tool, and nobody has bounded per-level perturbation by Panjabi's range of motion. | Read from source (evidence file; entries added on resume are marked). | 6 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/diffusion.md` | Can a mask-conditioned 3-D CT generator paint a CT that obeys an edited label map (an inserted L6, a sacralised L5)? | No spine-specific anatomically conditioned 3-D CT generator exists, and the edited-mask case was tested by seg2med and failed. | Read from source (two passes; numbers are the authors' own). | 7 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/downstream.md` | Did anyone train a detector or segmenter on generated or deformed anatomy and measure a gain on real held-out data? | The state of the art is affine plus intensity augmentation, anatomy synthesis buys 1 to 2 Dice points where measured, and the one measured lever for rare anatomy is real rare cases. | Read from source (two passes; the second corrects the first). | 8 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/rare-variant.md` | Has anyone synthesised a transitional or numerical vertebral variant in any modality? | No published work has synthesised an L6, T13, sacralised L5 or other numerical variant; every anomaly paper uses naturally occurring cases. | Read from source. | 9 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/registration.md` | Can registration, atlas or interpolation augmentation generate labelled anatomical variation? | A diffeomorphism cannot create a vertebra, and the measured gains of this family appear only up to about 60 training subjects. | Read from source. | 10 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/ssm.md` | Does any spine statistical shape or shape-intensity model produce CT intensities, and on how many subjects? | No spine SSM generates a CT, and the project's roughly 2,900 labelled CTs exceed any spine SSM training set by an order of magnitude. | Read from source; four candidates went through the adversarial checks in rows 12 to 15. | 11 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/ssm-verify-meng2020.md` | Adversarial check of the Meng 2020 full-spine statistical model | Surfaces only, no sacrum or pelvis, and no learned prior on inter-vertebral rotation. | Read from source (paper PDF and repository). | 12 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/ssm-verify-schmid2023.md` | Adversarial check of Schmid 2023 shape-and-intensity augmentation | Confirmed as summarised, except that the shape-and-intensity model alone was not significant, and no code was released. | Read from source (PMC10406777). | 13 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/verify-SIM-castro-mateos-2015.md` | Adversarial check of Statistical Interspace Models | Rejected for the project's requirement; one idea kept. | Read from source (the thesis, not the journal PDF; the file says the two could differ). | 14 |
| 2026-09-23 (stated) | `S/research_notes/spine synthesis prior art/verify-gpmm.md` | Adversarial check of Gaussian Process Morphable Models | Rejected: it deforms a fixed topology, so it cannot add or remove a vertebra, and no downstream gain has been measured with it. | Read from source (arXiv full text, Crossref, GitHub). | 15 |
| 2026-09-23 (stated) | `S/docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` | Which published morphology-synthesis method should the project adopt? | No published method meets the requirement, nobody has manufactured a transitional vertebra, and PolyPose is adopted as the mechanism with its result to be reported even if negative. | Read from source; compiled from the six angle notes and five adversarial verification files in rows 6 to 15. | 44 |
| 2026-09-23 (mtime) | `S/docs/data_requests/SX-Stitch_request.md` | A data request to the SX-Stitch authors | It is the only published collection of overlapping intraoperative C-arm frames of the spine, and a request was drafted for Greg to send. Whether it was sent is not recorded. | Not a review (request draft). | 45 |
| 2026-09-23 (modified) | `M/synthetic-real-ratio-evidence.md` | Summary of row 1 | As row 1. | As row 1. | 68 |
| 2026-09-23 (modified) | `M/data-audit-99-gaps.md` | Which datasets are incomplete or defective on disk? | 99 gaps were recorded in `S/docs/DATA_COMPLETENESS_AUDIT.md`, and several change the science. | Not a review (own audit; twelve verify agents never ran, as the audit document says). | 69 |
| 2026-09-23 (modified) | `M/lstv-tltv-detection-goal.md` | The standing goal: name the level correctly on a transitional spine from C-arm exposures | Every experiment serves naming the transitional level at parity with an ordinary one. | Not a review (directive). | 70 |
| 2026-09-23 (modified) | `M/two-mechanisms-thesis.md` | The paper's thesis: morphology classifier plus count from the anchor | The classifier answers first, the sweep verifies, and disagreement is the stop signal. | Not a review (thesis). | 71 |
| 2026-09-23 (modified) | `M/flagship-program.md` | The order of work, gates G0 to G7 | Nothing trains before the data gates close, and the claim's power is designed in rather than hoped for. | Not a review (plan). | 72 |
| 2026-09-22 (stated) | `S/docs/research_datasets_fourth_pass_verified_2026-09-22.json` | Fourth dataset sweep across repositories, imaging archives, cohorts and conference programmes, with C-ArmLSpine read in full | Four new sets were confirmed, none of them labelled real intraoperative spine fluoroscopy from living patients, and C-ArmLSpine ships pixels only. | Voted per item: 344 queries; 30 candidates verified in round 1 and 28 in round 2; every final item carries a confidence. | 23 |
| 2026-09-22 (stated) | `S/docs/research_carm_datasets_verified_2026-09-22.json` | Census of downloadable real C-arm, fluoroscopy and CBCT-projection datasets, to fit an image-formation model per C-arm | Three sets deliver real frames with a volume and a pose without a request (Geneva, COBRA2026, the Ljubljana pair), none adds a new mobile C-arm model, and the "already known" COBRA2026 entry (145 patients, four centres) was wrong on every count. | Voted: 94 / 25 / 19 / 6. | 24 |
| 2026-09-22 (stated) | `S/docs/research_rsnai_intro_verified_2026-09-22.json` | Citations for the RSNA AI introduction: the counting workflow, wrong-level incidence, LevelCheck's requirements, fiducial cost, and the navigation gap | The counting workflow, wrong-level rates and fiducial costs are verified, and Upadhyaya 2012 carries no cost figure. | Voted: 125 / 25 / 13 / 2, plus 10 unverified. Synthesis failed. | 25 |
| 2026-09-22 (stated) | `S/docs/research_rsnai_intro2_partial_2026-09-22.json` | Continuation of row 25 (navigation access and cost) | The Upadhyaya identifiers are corrected, and the navigation-access numbers stayed unverified in this partial run. | Voted, partial: 108 / 25 / 10 / 1, plus 14 unverified. | 26 |
| 2026-09-22 (stated) | `S/docs/research_rsnai_intro_nav_verified_2026-09-22.json` | Completion of rows 25 and 26 | The navigation-access argument is supported, and nothing was verified for registration-free naming on real fluoroscopy, the author instructions, or shots and dose per manual localisation. | Voted: 109 / 25 / 21 / 4. | 27 |
| 2026-09-22 (stated) | `S/docs/research_localisation_cost_2026-09-22.json` | What do intraoperative fluoroscopic level localisation and its errors cost in exposures, time and dose? | A localisation costs a few shots and a few minutes, initial wrong-level exposure runs from 0.12 % to 15 % depending on protocol, and no dedicated time-motion study of level localisation was found. | Identifiers checked: every DOI against Crossref and every PMID against PubMed; a per-claim flag says whether the full text was read. | 28 |
| 2026-09-22 (stated) | `S/docs/research_registration_free_search_2026-09-22.md` | Are three manuscript sentences about registration-free level identification on fluoroscopy true? | The "no naming system" sentence holds only in a narrower form, the "no per-vertebra recall" sentence is contradicted by Rao 2024, and the "everything imports identity from CT or MR" sentence is refuted; the file gives the wording the evidence allows. | Identifiers checked (DOIs and PMIDs). Three records (Li 2016, Li 2017, ABLSpineLevelCheck) could not be read and could still change the naming claim. | 29 |
| 2026-09-22 (stated) | `S/docs/research_rsnai_author_instructions_2026-09-22.md` | What are the Radiology: Artificial Intelligence limits for Original Research? | 3,000 words from Introduction to Discussion and a structured abstract of at most 250 words, per the 2025-06-10 Wayback capture. | Not a review. Read from a Wayback capture only; the live page was blocked. | 30 |
| 2026-09-22 (stated) | `S/docs/BENCHMARK_PROTOCOL.md` | How every comparator is scored on the same cases, truth and metric | A comparator that cannot run is reported with the reason, and pseudolabelled collections are reported as coverage only. | Not a review (protocol written before any comparator ran). | 41 |
| 2026-09-22 (stated) | `S/docs/RSNAI_TABLE1_DATASETS.md` | Machine-generated Table 1 of the X-ray datasets | It lists each dataset's device, pitch, storage and pairing, and names the cells the files cannot fill. | Not a review (generated by `tools/rsnai_table1.py` from the manifest). | 43 |
| 2026-09-22 (stated) | `M/mixed-length-head-and-sota.md` | What is the published state of the art for naming on plain radiographs? | No published plain-radiograph naming accuracy is metric-comparable with the project's. | Stated "Verified 2026-09-16"; method not recorded in the note. | 63 |
| 2026-09-22 (stated) | `M/registration-free-prior-art.md` | What is published on naming vertebrae from intraoperative fluoroscopy? | Restrict the novelty claim to naming, because per-vertebra detection recall on C-arm images is published. | Pointer to row 29 (identifiers checked; three records unread). | 67 |
| 2026-09-22 (modified) | `M/anomaly-rule-rc22-evaluated.md` | Does the "R + C = 22" transitional-spine rule work? (The rule's origin is not stated in the note.) | The rule is one count, rarely applies, rests on a C1 premise that is false for VerSe, and localises nothing. | Not a review (own evaluation). | 110 |
| 2026-09-22 (modified) | `M/ct-benchmark-covers-all-collections.md` | How many distinct subjects each CT render bank holds | The benchmark's CT axis is every collection (5,700 or more subjects), and counts are not additive across banks. | Not a review (own inventory). | 111 |
| 2026-09-22 (stated) | `M/film-fluoro-boundary-not-transferable.md` | Are film and fluoroscopy separable image domains? | Each C-arm keeps its own region of image-statistics space, but the film-against-fluoroscopy boundary does not transfer to an unseen corpus. | Not a review (own measurement). | 112 |
| 2026-09-21 (stated) | `S/docs/research_paired_ct_projection_unverified_2026-09-21.md` | The same question as row 19, before verification | COBRA2026 is the candidate, and its spine coverage is not stated. | Unverified (the filename says so). | 18 |
| 2026-09-21 (stated) | `S/docs/research_paired_ct_projection_verified_2026-09-21.json` | Which datasets pair a CT or CBCT with real 2-D projections of the spine, pelvis or torso with a known or recoverable pose? | Only COBRA2026 is downloadable and fills most of the gap, but it is not a C-arm and its spine coverage is unconfirmed; no public set pairs a living patient's CT with intraoperative lumbar C-arm fluoroscopy and a known pose. | Voted: 99 / 25 / 15 / 10. | 19 |
| 2026-09-21 (stated) | `S/docs/research_datasets_missed_verified_2026-09-21.json` | Which datasets had the project missed: (A) CT paired with real torso 2-D from a device other than a Siemens Cios Fusion, and (B) labelled real intraoperative spine fluoroscopy? | No public set of intraoperative lumbar fluoroscopy from living patients with vertebra labels was found, and LUMOS is the only new open set. | Voted: 82 / 25 / 25 / 0. The file says angles 2, 3, 7 and 8 produced nothing and are unsearched ground, not negatives. | 20 |
| 2026-09-21 (stated) | `S/docs/research_datasets_third_pass_verified_2026-09-21.json` | Third pass over the angles the first two left unverified | C-ArmLSpine is the best new open set, and no public, labelled, multi-device intraoperative pelvis or spine fluoroscopy set was found in any of the three passes. | Voted: 78 / 25 / 21 / 4. | 21 |
| 2026-09-21 (stated) | `S/docs/research_sim_real_mixing_verified_2026-09-21.json` | With abundant DRRs and a small real set, is sequential, mixed or replay training best? | Keep mixed training as the default, because the real C-arm frames cover only T11 to S1, and no matched X-ray comparison of the three strategies exists. | Voted: 85 / 25 / 22 / 3. | 22 |
| 2026-09-21 (stated) | `S/docs/REAL_XRAY_DATASETS_SPEC.md` | What single format every real X-ray dataset with projected labels should be written in | Labels are projected from a registered CT or CBCT, every volume is labelled by both TotalSegmentator and SPINEPS with VERIDAH, and a level is used only where the two agree. | Not a review (specification). | 40 |
| 2026-09-21 (mtime) | `C/2D-3D-GS_UG.pdf` | The user's guide to the Ljubljana 2D-3D registration gold standard (Tomazevic, Likar, Pernus) | The data may be used only after signing the laboratory's agreement; the guide forbids unauthorised distribution. | Saved primary source. | 85 |
| 2026-09-21 (mtime) | `C/AITR-2002-001.pdf` | Zollei 2001, MIT AI Technical Report 2002-001, "2D-3D Rigid-Body Registration of X-Ray Fluoroscopy and CT Images" | A registration method thesis, background for the 2D-3D lineage. | Saved primary source. | 86 |
| 2026-09-21 (mtime) | `C/Spine Fluoroscopy Image Datasets.pdf` | "Comprehensive Analysis of Spine-Focused Fluoroscopic and Radiographic Datasets for Image-Guided Robotic Interventions" | A survey of spine-relevant fluoroscopy and radiograph datasets; continuous spine fluoroscopy video is described as exceptionally rare. | Unverified (author not stated; no verification recorded; references include ResearchGate and Kaggle pages). | 87 |
| 2026-09-21 (mtime) | `C/COBRA.pdf` | The COBRA2026 dataset paper (Thummerer, Rit, Kamp, Maspero and others), "a large-scale multicenter pelvic cone-beam computed tomography projection dataset" | The paired CBCT-projection set the device calibration uses. | Saved primary source. | 88 |
| 2026-09-21 (mtime) | `C/Sun_2021_Phys._Med._Biol._66_175002.pdf` | CrossModalNet (Sun et al., Phys Med Biol 2021) | Excluded as kV or C-arm paired data in row 19. | Saved primary source. | 89 |
| 2026-09-21 (stated) | `M/drr-to-fluoro-levers.md` | Which levers move DRR-to-real-fluoroscopy transfer? | Fidelity, strong domain randomisation and scale are the measured levers, and generative translation buys nothing. | Voted ("Deep-research pass, 107 agents, adversarially verified"). | 109 |
| 2026-09-20 (stated) | `S/docs/FLUORO_DATASET_STRATEGY.md` | Which external fluoroscopy datasets to acquire, in what order, and what each is for | DeepFluoro comes first because its labels are free and exact, no published per-vertebra recall on real fluoroscopy exists, and no dataset supplies a commanded sweep on a live patient. | Not a voted sweep. The file withdraws its own earlier Pelphix comparison after checking it, and cites PMIDs and DOIs inline. | 39 |
| 2026-09-20 (modified) | `M/fluorocap-is-reproductions-not-fluoroscopy.md` | Is FluoroCap fluoroscopy fit for training? | FluoroCap is mostly press reproductions, so about 200 panels should be annotated as a test set, not used for training. | Not a review (own measurement). | 66 |
| 2026-09-20 (mtime) | `C/Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf` | A two-page summary of public fluoroscopy datasets and noise-simulation frameworks | There are "virtually zero" open spine fluoroscopy datasets, so the field renders from CT. | AI-generated (Google Gemini export; no verification). The LevelCheck "vast repository" claim has no n and is contradicted in part by row 20, which found the original LevelCheck real paired data was one phantom (35 frames). | 83 |
| 2026-09-20 (mtime) | `C/C-Arm Validation Research Plan.pdf` | "Translational Roadmap for Exact Intraoperative Vertebral Counting via Overlapping C-Arm Fluoroscopy" | A roadmap for validating overlapping-frame counting. | Unverified (author not stated; no verification recorded). | 84 |
| 2026-09-20 (stated) | `S/docs/CARM_DEPLOYMENT_EVIDENCE.md` | Can a level-confirmation algorithm ship as a software update to a fielded C-arm? | One vendor-sanctioned on-device route exists (Siemens Cios), and nobody publishes the compute available on it. | Voted (three verifiers per claim; refuted claims listed at the end). | 95 |
| 2026-09-19 (mtime) | `C/MDPA.pdf` and `C/arxiv_final_draft_9_19_2026.pdf` | Earlier versions of the dataset article (row 55) | As row 55. | Not a review (own manuscript). | 82 |
| 2026-09-19 (stated) | `S/docs/SWEEP_TIME_EVIDENCE.md` | How long would a fluoroscopic sweep take, and what does current localisation cost? | A four-exposure sweep plus one query image is about 3 to 4 min of C-arm positioning and under 30 s of compute, against 15 min published for standard thoracic counting. | Voted (workflow wf_42f017f0-4cf; three verifiers per claim; counts not given in the summary). | 91 |
| 2026-09-19 (stated) | `S/docs/WRONG_LEVEL_COST_EVIDENCE.md` | What do wrong-level surgery and level localisation cost, for the introduction? | Wrong-level surgery is common across a career and rare per procedure, the thoracic spine has its own published rate (0.42 %), and the 0.09 to 4.5 per 10,000 band must not be quoted as a spine figure. | Voted (workflow wf_7c2848b4-012; 15 sources; two of three refutations kill a claim). | 92 |
| 2026-09-19 (stated) | `S/docs/WRONG_SITE_BURDEN_EVIDENCE.md` | What is the annual burden of wrong-site and wrong-level spine surgery? | US indemnity for wrong-level spine surgery is on the order of 8 to 36 million dollars a year, and no evidence-based worldwide figure exists. | Voted (workflow wf_203d096e-7c0; three verifiers per claim). | 93 |
| 2026-09-19 (modified) | `M/spine-data-review-and-ts-bench.md` | The TotalSegmentator render bench and the scoping review workstream | TotalSegmentator is ordinary-anatomy truth only, and VERIDAH is the one CT labeller that can name L6 and T13. | Not a review (workstream note). | 108 |
| 2026-09-18 (stated) | `S/docs/research_patent_2026-09-18.json` | What must a US academic inventor do to patent a registration-free intraoperative level-identification method, and what prior art stands in the way? | The CT- and MRI-requiring patents do not read on a method with no preoperative volume, and US 8,718,346 discloses manual labelling on stitched C-arm images, which is prior art rather than a blocking claim. | Voted: 125 / 25 / 17 / 7, plus 1 unverified. The synthesis step failed, so the 17 confirmed claims are unmerged. | 16 |
| 2026-09-18 (stated) | `S/docs/research_registration_free_2026-09-18.json` | Which published methods name a vertebral level on radiographs or fluoroscopy without registering to a preoperative CT or MRI? | Exactly one system names levels on intraoperative X-ray without registration (MVMS, on cadaver long films), transitional spines are unaddressed, and no method releases code or weights. | Voted: 105 / 25 / 22 / 3. Most checks were against abstracts because five of six primary papers were paywalled. | 17 |
| 2026-09-18 (mtime) | `S/docs/COMPETITOR_BENCHMARK.md` | How to rebuild the published registration-free methods on one corpus, and whether a consensus beats any one | Published figures cannot be read as a ranking, so each paradigm is rebuilt and any ensemble is chosen on one half of the films and reported on the other. | Not a review (design note). | 38 |
| 2026-09-17 (stated) | `S/docs/PRIOR_ART_SYNTHETIC_AND_SELF_TRAINING.md` | What closes the DRR-to-radiograph gap, how synthetic data scales, and how to self-train on rare classes | Physics DRRs with strong photometric randomisation matched both generative translation and matched-size real training, synthetic pretraining then real fine-tuning beat naive mixing in the one comparison, and nothing was measured for diffusion img2img, ControlNet or LoRA on radiographs. | Voted (workflow wf_78f61c94-3fe, 105 agents, three votes per claim). The claim "DeepDRR physics beats naive DRR" was refuted 0-3. | 36 |
| 2026-09-17 (stated) | `S/docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` | How accurately do humans and software name the vertebral level, and on what? | There is one measured human exact-level naming number (Manbachi), LevelCheck's figures are registration success rather than naming, there is one registration-free AI number (88.3 %), and no anomaly-stratified naming accuracy exists anywhere. | Voted (workflow wf_93111768-3ea, 106 agents; 24 verified claims). The Liebrand 2026 row was not voted (low confidence). | 37 |
| 2026-09-17 (modified) | `M/anomaly-manifest-sources.md` | Where every anomalous spine in the holdings lives | The master flag table is `~/lstv_flag/lstv_flag_labels_v2.csv`, and the pooled co-occurrence odds ratio of 12.8 is Simpson's paradox and must not be quoted. | Not a review (own inventory). | 64 |
| 2026-09-17 (modified) | `M/feasibility-claims-measured.md` | Which claims of the limited-field feasibility report hold? | Three of five disproofs were overturned by an adversarial audit, and the definitive anchor-free accuracy on anomalous real films is 49.9 % (41.5 to 58.9) over 128 films. | An adversarial audit (20 agents) is recorded for the own-result claims; the literature numbers are cited to two deep-research runs. | 65 |
| 2026-09-16 (mtime) | `S/buu.pdf` | Meant to be the BUU-LSPINE paper (MDPI Applied Sciences 13(15):8646) | The BUU-LSPINE paper is not on disk in this file. | Not a source (failed download). | 81 |
| 2026-09-15 (mtime) | `C/docs/ukb.html` | A saved copy of a primary article, not a review: "Identification of novel vertebral development factors through UK Biobank candidate gene search and body imaging analysis", Communications Biology 2025, PMC12630705 | Three genes (GPC3, NR6A1, VRTN) are associated with lumbar and rib numerical variants. | Not a review; saved primary source, only the abstract read for this note. | 54 |
| 2026-09-15 (stated) | `M/lstv-data-landscape.md` | Where transitional-vertebra labels exist for training a 2-D flag | The published 2-D LSTV literature is one paper, and the positives available beyond CTSpinoPelvic1K's 33 are 274 distinct LSTV and 102 TLTV cases. | Read from source: the VerSe table was checked against the paper's Table 2 on 2026-09-15. | 61 |
| 2026-09-15 (stated) | `M/selective-prediction-the-honest-99.md` | Can 99 % be claimed for level identification, and in what form? | 99 % is reachable as a coverage claim (35.7 % of vertebrae named exactly, 55.7 % by region), not as an accuracy claim. | Not a review (own result). | 62 |
| 2026-09-15 (stated) | `M/versefusion-t13-flag-wrong.md` | Is the VerSeFusion manifest's T13 flag right? | Never read has_T13 from the VerSeFusion manifest; take variants from Loeffler 2021, Supplemental Table 1. | Read from source (masks against the published table). | 107 |
| 2026-09-14 (mtime) | `S/docs/PRIOR_ART_LEVEL_ID_XRAY.md` | Not stated; the file is an 11-row table of PubMed hits with the numbers each abstract reports | Not stated. | Unverified (no method or verification recorded; numbers truncated mid-sentence). | 32 |
| 2026-09-14 (stated) | `S/docs/PRIOR_ART_WEAK_SUPERVISION.md` | How does the field get per-vertebra labels onto unannotated radiographs, and what is that problem called? | No paper uses hardware named in a caption as a per-vertebra constraint, and pseudo-labelling is the standard route for training data. | Unverified (OpenAlex scan, ten queries, top-cited per query). | 33 |
| 2026-09-14 (mtime) | `S/docs/PRIOR_ART_WRONG_LEVEL_SCAN.md` | Not stated; four raw OpenAlex tables (wrong-level surgery, transitional anatomy, AI detection of transitional anatomy, rare classes) | Not stated. | Unverified (no header, method or verification recorded). | 34 |
| 2026-09-14 (stated) | `S/docs/PATHOLOGY_SOURCE_SWEEP_2026-09-14.md` (raw companion `S/docs/pathology_source_sweep_2026-09-14.json`: 366 sources, 534 queries, 7 clinical families, a critics block) | Where to get pathology, variant and wrong-site images whose level is stated, and how to scrape each source | A per-source access table for scrapers, plus a clinical knowledge base for seven pathology families. | Unverified for the clinical part (machine-authored; the skeptic pass did not run). The source table comes from a parallel sweep with no vote recorded. | 35 |
| 2026-09-14 (stated) | `M/fluorocap-dataset.md` | How FluoroCap, the literature-mined fluoroscopy collection, was built | A large caption-labelled panel set was assembled, and the film-trained detector did not transfer to C-arm panels. | Not a review (build log). | 60 |
| 2026-09-13 (git) | `C/docs/dataset_card.md` | The Hugging Face card for CTSpinoPelvic1K | 33 transitional cases carry an expert Castellvi grade (25 from the vertebral count, 8 from the pelvic annotation). | Not a review. It describes release v3 with S1 carved as id 29; `C/CLAUDE.md` says the current release is v11 and id 29 is retired, so the card is out of date on the label scheme. | 47 |
| 2026-09-13 (modified) | `M/level-id-2d-results-2026-09-13.md` | How well a single crop names a vertebra on real films | Overall single-vertebra accuracy was 96.7 % and lumbar 80.7 %, and more lumbar data is the only lever. | Not a review (own result). | 58 |
| 2026-09-13 (modified) | `M/xr-benchmark-and-robustness-2026-09-13.md` | Which published radiograph level labellers can be benchmarked, and how robust the model is | No public radiograph level labeller ships weights, so competitors are re-implemented mechanisms, and the recurrent head over single-crop embeddings scored best (98.7 % at three vertebrae). | Not a review (own result). | 59 |
| 2026-09-13 (mtime) | `C/PANJABI_1991_FULL.pdf` and `C/PANJABI_1991_FULL_fixed.pdf` | Panjabi 1991, "Thoracic human vertebrae: quantitative three-dimensional anatomy", Spine 16(8):888-901, obtained by interlibrary loan | The reference series drawn on Figure 6 of the dataset article. | Saved primary source. | 80 |
| 2026-09-13 (stated) | `M/panjabi-1991-page-892.md` | Where page 892 of Panjabi 1991 (Table 3) could be obtained | Every scan of the paper skipped page 892, and the interlibrary-loan copy in `C/` supplied it. | Read from source (the page was read by eye). | 105 |
| 2026-09-12 (modified) | `M/ctspine1k-selection-code-deleted.md` | Did CTSpine1K's code really choose one of two positions at random? | The selection code was deleted and never selected anything, so the annotation-to-series mapping never existed and the crosswalk is the only way to establish it. | Read from source (the deleted file at commit 7f44959). | 106 |
| 2026-09-11 (git) | `C/docs/LEVEL_MORPHOMETRY.md` | Why canal depth and end-plate width were wrong, and what the published methods define | Both defects were caught by comparing spread and prevalence against published living cohorts, not by any internal check. | Unverified as a sweep; numbers are cited inline to their papers. | 53 |
| 2026-09-10 (git) | `C/docs/NEXT_PAPER_REFERENCES.md` | Which multi-series morphometric references were built and held back for a later paper | Published series disagree with each other by 21 % to 69 % of their own median, which is a finding about the literature and belongs in its own paper. | Unverified (no verification recorded). | 52 |
| 2026-09-08 (modified) | `M/competitor-benchmark.md` | How the public CT segmenters are scored against CTSpinoPelvic1K in one label space | Runs were pending at that date, and competitors without an L6 class still get their count scored. | Not a review (run log). | 57 |
| 2026-09-08 (modified) | `M/xray-corner-detector-status.md` | What the radiograph corner-detector corpus holds | The detector reached AP50 0.970 on held-out films. | Not a review (own corpus). | 104 |
| 2026-08-23 (mtime) | `3474_Not_All_Spines_Are_Create.pdf` | The NeurIPS submission "Not All Spines Are Created Equal: How TotalSegmentator Fails on Lumbosacral Transitional Vertebrae" | On lumbarisation cases TotalSegmentator shifts lumbar labels one level caudally, and junction Dice drops by 29 points (abstract). | Not a review (own manuscript). | 79 |
| 2026-08-22 (mtime) | `S/docs/LSTV_BENCHMARK.md` | How to run the single-pass transitional-anatomy experiment, and what would make it fail | The sampler, not the backbone, is the main risk, and count accuracy must be reported separately for typical and transitional anatomy. | Not a review (design notes written before the first run). | 31 |
| 2026-08-22 (git) | `C/docs/COUNTING_PRIOR_ART.md` | How a convolutional network can enumerate a variable number of vertebrae | Four families of answers exist, and a one-shot model should learn the thoracolumbar junction from local morphology but cannot settle L5 against L6. | Unverified (sources listed, no verification recorded). | 50 |
| 2026-08-22 (git) | `C/docs/METHODS_REFERENCES.md` | What each released measurement is checked against | A measure that disagrees with its published value is withheld, and at that date the file says the dataset carried no Castellvi grades, only LSTV labels for 33 cases. | Unverified (no verification recorded). Its "no Castellvi grades" statement conflicts with row 47 and with `C/docs/CASTELLVI_SCREEN_BLIND_SPOT.md` (2026-08-23 git), which says all 33 carry a radiologist grade. | 51 |
| 2026-08-02 (mtime) | `C/CaseReports_T12_hypoplastic_rib.pdf` | A case report on naming lumbar segments under fluoroscopy when a T12 rib is hypoplastic | Lumbarisation and sacralisation confuse fluoroscopic segment identification before pain interventions. | Saved primary source. | 78 |
| 2026-07-24 (modified) | `M/publication-roadmap.md` | How the spinopelvic work splits into papers, and where each goes | The dataset descriptor moved to Medical Physics after MLHC rejected it, and the level-identification work moved to Radiology: Artificial Intelligence. | Not a review (plan). | 56 |
| 2026-06-25 (git) | `C/docs/DATASETS_ROADMAP.md` | Which external CT datasets to unify into one VerSe-native corpus, and how | A phased plan to fold each source in, with the Moller rib and stump-rib masks as the highest-leverage first pull. | Unverified (a "Verified links" table header, no verification method recorded). | 49 |
| 2026-06-25 (mtime) | `C/TS_DS.pdf` | The TotalSegmentator paper (Radiology: Artificial Intelligence) | The whole-body CT segmenter and dataset the article compares against. | Saved primary source. | 77 |
| 2026-06-24 (mtime) | `C/RIBSEG.pdf` | The RibSeg v2 paper (Jin et al., IEEE TMI) | The public rib-labelling benchmark the dataset article compares against. | Saved primary source. | 76 |
| 2026-06-12 (git) | `C/docs/DATASET_PRINCIPLES.md` | The governing rules for the dataset | The dataset is append-only, and radiologist ground truth is never overwritten. | Not a review. | 48 |
| 2026-06-08 (mtime) | `MLHC_2026_Research_Track_Paper.pdf` (Desktop root and `C/`) | The MLHC 2026 submission of CTSpinoPelvic1K, "A Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation" | The own dataset paper as first submitted; `M/publication-roadmap.md` records that MLHC rejected it. | Not a review (own manuscript). | 75 |

---

## 7. Unknowns

### 7.1 What is not known

| # | unknown | where it was looked for | why it matters |
|---:|---|---|---|
| 1 | The true person-level transitional naming accuracy of any arm on real frames | PJ; SR2 S2; LCM section 8; TAB2 | Every power row needs it as the effect size; every powered statement so far assumes 95 to 99 % |
| 2 | How many of the 57 field-supported COBRA2026 screen calls are transitional | TAB2 note e; SR2 S4; RS2 N7 | No human read exists; the labeller's CTSpinoPelvic1K PPV is L6 10 of 24, T13 0 of 52 |
| 3 | Whether the 13 reference-ordinary COBRA persons and 10 C-ArmLSpine persons can carry H6 | GATE; RES22 lines 679 to 688 | The open gate's reference-standard score was never written |
| 4 | The person-level intraclass correlation for transitional endpoints | NUM (design effects 3.84 to 4.47 are for vertebrae within cases, ordinary spines) | Needed by every two-proportion power row |
| 5 | Any power calculation for device-level differences, LODO against pooled across devices, or the synthetic-to-real ratio | grep of the directories named in section 4 (N4 section 1, extended on review) | With 4 devices the smallest attainable device-level P is 0.125 |
| 6 | Power under the replacement detector of LCM section 15 | LCM section 15; SR2 | The power-0 reading of SR2 S12 applies to the detectors that were replaced |
| 7 | Whether C-ArmLSpine's 148 or 149 cases are 148 or 149 people, whether they were living, the ethics approval, and how its pose was obtained | FOURTH unknowns; CORP note h; `ssn:SchwingNet/sections/discussion_limits.tex` | It is the only intraoperative human data; files record 149 cases, 148 cases and 120 subjects |
| 8 | Whether any drafted request (SX-Stitch, Balgrist, the 14 cine letters) was sent or answered | MAN#sx_stitch_request, #balgrist_exvivo_request, #fluoro_cine_requests_2026_09_26 ("Sent: not recorded") | They are the only drafted routes to labelled real fluoroscopy |
| 9 | Whether the gated collections' expected yields hold | ACQ section 9 | Merlin's 1,260 is a prior; AMOS and the NLST pilot already missed theirs |
| 10 | Whether the tier-1 acquisition yields its expected 831 to 1,703 transitional people | ACQ section 9; TIERS | The only route by which the CT transitional count grows past VERIDAH's |
| 11 | Person counts across acquisition collections after deduplication | TIERS section 8; ACQ section 9 (`alias_pairs_all.csv` is on the grid) | Near-duplicates are listed, not merged |
| 12 | Ruleclass flag counts after the Möller rib and Dataset803 pelvis arms ran (after 2026-09-27) | TIERS; mem:ruleclass-super-detector-run.md (CORPUS.md is on the grid) | The latest flag counts are not on this laptop |
| 13 | How many LSTVs a whole-cohort Castellvi read of CTSpinoPelvic1K would add | MPDA lines 919 to 921 | 33 graded against 71 to 142 expected |
| 14 | Cage-from-T1 coverage of the COBRA2026 planning CTs; P(both references) for TotalSegmentator v3 keys beyond the 1,228 calibrated v2 scans | COBS; FOV; CEN | Expected T13 in COBRA and expected counts for v3 cannot be computed |
| 15 | Whether COBRA2026 projections cover the sacral ala and L5 | PAIRED (marked unverified) | Decides whether COBRA2026 counts as spine data |
| 16 | What Li 2016, Li 2017 and ABLSpineLevelCheck 2024 report | RF22 sections 5.2, 6 (IEEE Xplore blocked) | Any of them could hold a C-arm naming result that overturns the naming-novelty claim |
| 17 | Cina 2021's train and test n; VertXNet's split; Kónya 2021, Kim KC 2021, Mushtaq 2022 cohorts; the BUU-LSPINE baseline's test split | mem:mixed-length-head-and-sota.md; RF18; RF22 section 5.6 | Radiograph ratios rest on total images, not test sets; the BUU paper is not on disk (`ssn:buu.pdf` is an access-denied page) |
| 18 | VDVM's patient count and whether its 31 test images are intraoperative; Rao 2024's subject count and whether any are living patients; Huang 2022's anomaly content | RF22 sections 5.1, 6; RF18 | The C-arm ratios are in images, not people; Rao's 0.964 may be cadaver and phantom only |
| 19 | The patient counts behind SX-Stitch, Rao 2024, VDVM, CM Spine and DAX | SXS; RF22; MAN#cm_spine_drive_file; FOURTH refuted_or_useless | Section 2 orders group A by subjects; these are counted in images and sit last in their subgroup |
| 20 | Size and label content of TVGH-SpineXR | MAN#tvgh_spinexr; FOURTH | The one film set named with T1 to L5 level labels that is not held |
| 21 | Whether SyntheX's Dataverse deposit 2PGJQU is on disk | MISSED finding 6 says held; the manifest has no card | Decides whether a matched real-and-render set is in hand |
| 22 | Whether the CT Colonography localizers (up to 754 patients) survive on HOME | MAN#tcia_ct_colonography (state unknown); THIRD finding 7 | A free same-patient projection source |
| 23 | Whether the empty Google Drive download is the CM Spine 208-image G-arm set | MAN#cm_spine_drive_file; STRAT; GEM | The only named intraoperative lumbar set with detection labels that was attempted |
| 24 | SPARE's true contents | CARM (every claim refuted 0 to 3); PAIRED | The only open thoracic CBCT set with a prior 4D-CT besides RTK's three subjects |
| 25 | Whether VerSeg-Net exists as described, and whether the fourth-pass items its verifiers only partly confirmed hold in the parts not confirmed | FOURTH: `round1_verified` (30 candidates) and `round2.verified` (28) carry two verifier verdicts each (FAU Surgical-Device-Detection refuted twice); the coverage note's "only four carry a visible verifier verdict" describes the truncated transcript its synthesis step received, of about 83 deduplicated candidates. Only items named in the coverage note alone, such as VerSeg-Net, have no verdict | VerSeg-Net (A4) is the only labelled lumbar intraoperative fluoroscopy set from 50 patients named anywhere |
| 26 | Which licence reading is right for CTPelvic1K, VerSe, DeepFluoro, Geneva and Ljubljana | MAN§4.8 ("need Greg's reading") | Decides the redistribution column of every derived bank |
| 27 | The current on-disk state of HOME after 2026-09-01 and Ceph after 2026-09-25 | MAN section 1 (census job 40578909 had not reported) | Every HELD count here is the card's dated count |
| 28 | The sampling error of the frozen comparators: 97.6 % has no published denominator, and Peh 1999's numerator is assumed (106 of 129) | LCM section 2; SR2 S9; RS2 N10 | The comparator's own interval is unknown |
| 29 | Barr 2026's de novo error at n = 700 (7.42 at both 600 and 700) | SYN section 2 (flagged there) | The real-frame crossover number depends on it |
| 30 | The release status of the Sabri 2025, Schinz 2026, Hanhivaara, Nardo, Nagata and Sun cohorts | mem:lstv-data-landscape.md; MPDA; ACQ section 2 | They size the field; none is recorded as obtainable |
| 31 | Venues of Barr 2026, Hu 2016, Liebrand 2025, Albano 2024, Osiowski 2024; Hanhivaara 2022's n; the full text of the Liebrand 2026 systematic review | SYN; PREV; MPDA; HAI section 9; RF22 section 5.7 | Liebrand 2026 is the review a reviewer will reach for |
| 32 | Which study gives "best whole-spine identification 96.5 % on MRI", and where the "R + C = 22" rule comes from | mem:selective-prediction-the-honest-99.md; mem:anomaly-rule-rc22-evaluated.md | Neither note names its source |
| 33 | Whether the pathology sweep's clinical knowledge base is right | PATH (the skeptic pass did not run) | Its recommendations cannot be cited |
| 34 | The confirmed claims of the patent sweep and two RSNA AI sweeps | `ssn:docs/research_patent_2026-09-18.json`, `research_rsnai_intro_verified_2026-09-22.json`, `research_rsnai_intro2_partial_2026-09-22.json` | The synthesis step failed, so the claims are unmerged |
| 35 | Whether the research notes' numbers were ever put to a vote; how `PRIOR_ART_LEVEL_ID_XRAY.md` and `PRIOR_ART_WRONG_LEVEL_SCAN.md` were produced; who wrote the Gemini summary, `Spine Fluoroscopy Image Datasets.pdf` and `C-Arm Validation Research Plan.pdf` | N1 rows 2 to 15, 32, 34, 83, 84, 87 | Their numbers are read from source or unverified, not voted |
| 36 | Which LUMOS CT belongs to which radiograph | MISSED finding 0 | The 280 "paired" cases are paired only by an undocumented folder id |
| 37 | Whether the "3 against 15 minutes" localisation figure exists in Upadhyaya 2012 | `ssn:docs/research_localisation_cost_2026-09-22.json`; `research_rsnai_intro_verified_2026-09-22.json` | It appears only in a press release and a later review |
| 38 | The current Hugging Face card for the v11 release | `ctsp:docs/dataset_card.md` describes release v3 with the retired id 29 | The card on disk is out of date on the label scheme |
| 39 | No CT L6 identification rate from your own model | NIPS (voxel-level results only); TAB2; RES | No CT naming number can be set beside VERIDAH's recall |
| 40 | No human reader study, and no device or site counts for the film corpora | TAB3; RES; T1 (cells marked unfillable) | Manbachi's design has no counterpart; no device-level statement can be made for radiographs |
| 41 | Whether RadGS-Reg (A9) and LineReg (A8) share patients | THIRD finding 6 (Changzhou affiliation; code at github shenao1995); FOURTH r1 19 (the same code author) | Group A could count 10 people twice |
| 42 | How many lumbar- and thoracic-anomaly scans VERIDAH's CT test set holds | AUTO C2 (rates: about 54); CORR (recall percentages: 63) | The CT size ratio is 0.81 to 0.94 on 51 persons depending on the answer |
| 43 | Whether Petragallo's 429-patient ExacTrac set can be requested at all | FOURTH r2 17 (six institutional agreements; the corresponding author finished her PhD in 2024) | It is the second-largest living-patient spine projection set with a planning CT |
| 44 | Whether the CMB-MML and CMB-AML frames other than MSB-04031 can carry a level: they are iliac-crest biopsies with about L3/L4 to S1 in the field | FOURTH r1 6 | Decides whether A6 is one usable patient or about 15 |
| 45 | Whether the Mayo fiducial series and the L6 confirmation experiment of RSN2 return to the manuscript | RSN2 lines 58, 75; grep of `ssn:SchwingNet/sections/` | Section 3 and 4 cite them from the superseded draft |

### 7.2 Places where two files disagree

| item | one file says | another says | files |
|---|---|---|---|
| VerSe scans with L6 | 85 scans (Liebl 2021) | 47 cases (Sekuboyina 2021, split 15/15/17); 50 with id 25; 87 read series | mem:lstv-data-landscape.md; AUTO C4, C5; TLJ; mem:ruleclass-super-detector-run.md; `ssn:SchwingNet/lit/ct_lstv_classifier/reusable_inventory.md`. AUTO says to count from the masks; no file has |
| CTSpinoPelvic1K L6 | 18 records by release label (2026-09-23) | 16 by the readers' own count, seven records disagreeing (CORR); 29 persons (2026-09-24) | SUBT and MPDA; CORR; REG table B |
| CTSpinoPelvic1K Castellvi-graded records | 33 | 34; 39 | `ctsp:docs/dataset_card.md` and MPDA; reusable_inventory.md; mem:publication-roadmap.md (`Lumbosac.csv`) |
| C-ArmLSpine size | 149 cases | 148 cases, 296 frames; 120 distinct subjects | FOURTH; DSH and T1; `ssn:docs/BENCHMARK_PROTOCOL.md` and mem:ct-benchmark-covers-all-collections.md |
| Zero-shot lateral naming on C-ArmLSpine | 595 of 617 (96.4 %) | 594 of 617 (96.3 %) | RES; TAB3 and CLM carm_zeroshot_lat_whole_exact |
| The four stopped L6 calls on C-ArmLSpine | three on five-lumbar frames, one on a six-lumbar patient's frame | 4 of 233 on five-lumbar frames | RES; TAB3 |
| LCM section 7, H6 power at 145 persons | "0.44 at 98 % and 0.82 at 99 % (unadjusted)" | the frozen code gives 0.83 and 0.98 unadjusted; the stated values reproduce only at alpha 0.025/6 | LCM section 7; calc (N4 section 7 row 3) |
| Anomalous-film interior accuracy | 66.0 % over 12 films | 49.9 % over 128 films, "the definitive" figure; the 12-film number "was noise" | N4 row 6 used the first; mem:feasibility-claims-measured.md says the second. This file uses 49.9 % |
| "L6 by the classifier 44.9 %" | on real C-ArmLSpine laterals | on anomalous BUU films with no anchor ("State C") | N4 row 6 (citing mem:two-mechanisms-thesis.md); mem:feasibility-claims-measured.md, which mem:two-mechanisms-thesis.md cites. This file uses the second |
| Power-table inventory | 89 transitional subjects, 37 test persons, bound 90.59 % | superseded: 4 of the 12 TotalSegmentator spines are transitional on an independent rib count | PT; `ssn:tools/anomalous_inventory.py` docstring |
| Transitional persons in all sources | 194 (Table 2) | about 190 (ACQ); 202 read-tier (POS); 306 positive in the registry (REG, POS) | different dates and definitions |
| TotalSegmentator size | 1,204 | 1,228 (v2); 1,278, which is not a release size but the tier-1 TotalSegmentator CTs of the ruleclass census ("TS-dataset 1,278" in the memory note); 1,935 or 1,939 (v3) | MPDA; MAN; mem:ruleclass-super-detector-run.md; TIERS section 1 row ts |
| CTPelvic1K size | about 1.1k | 1,184 | ROAD; MPDA |
| BUU-LSPINE | 3,600 patients, 7,200 films | 3,600 films from 1,200 patients (PATH); 7,204 films on disk, of which 3,603 lateral films are in the level bank (DSH; 3,603 counts films, not patients) | MAN and mem:lstv-data-landscape.md; PATH; DSH section 2.6 |
| AASCE 2019 | 609 | 579; 457 | PATH and MAN; DSH; T1 |
| NHANES II region split | 7,408 lumbar and 9,667 cervical | 8,840 cervical and 7,394 lumbar | mem:lstv-data-landscape.md; mem:anomaly-manifest-sources.md |
| VerSe size | 374 scans | 460 | MAN and MPDA; MLHC Table 1 |
| PENGWIN size | 150 CTs | 340 CTs held | MLHC; MAN#pengwin2026 |
| Geneva hip frames | 116 frames over 19 views | 19 frames | MAN#geneva_hip and T1; CARM finding 0 |
| LUMOS Zenodo record | 18173664 | 18173663 | MISSED; RANK and MAN#zenodo_lumos |
| Möller stump-rib masks record (resolved) | Zenodo 14864106 | Zenodo 14850928 | not a disagreement: 14850928 is the concept DOI and 14864106 its single version, one record; cite the concept DOI (CORR). Quoted by mem:lstv-data-landscape.md and MAN#ribfrac; ROAD and TLJ |
| Möller stump-rib cohort | VerSe 323 + RibFrac 420 subjects (743) | 133 of 648 subjects carry a stump rib | mem:lstv-data-landscape.md gives both without reconciling them; AUTO C3 gives 648 as the final analysis set of the 743 public subjects, and the files read do not say why 95 were left out |
| DeepFluoro licence | CC BY-NC | CC BY-NC-SA | MAN#deepfluoro_h5; T1 |
| SyntheX deposit 2PGJQU | "already has" | no card | MISSED finding 6; MAN |
| COBRA2026 shape | 145 patients, four centres, Elekta only | 867 patients, six centres, two vendors | the older entry quoted in CARM's question; CARM summary (the older entry was wrong on every count) |
| Tier 2 and deferred totals (reconciled) | 30,486 + 3,536 = 34,022 new CTs; E_low 153 + 187 = 340 | 33,362 new people; E_low 337 | ACQ opening table; JOIN totals (N2 section 2). The gap, 660 people and E_low 3, is RibFrac: tier 2 in RANK (rank 90: 660 new people, E_low 2.9) but held, so JOIN leaves it out (calc_review) |
| VERIDAH CT test-set anomaly scans | 25 thoracic and 29 lumbar, written as counts (SYN) | 54 inferred from the test rates (6.8 % and 7.9 % of 365, AUTO C2); 63 inferred from the recall percentages, which 29 and 25 cannot produce (28 of 29 is 96.6 %, 24 of 25 is 96.0 %) but 35 of 36 and 26 of 27 do (97.22 %, 96.30 %) (CORR) | SYN; AUTO C2; CORR; calc_review. The paper prints rates and percentages only |
| CT transitional test persons | 57 (TAB2: L6, T13 and both sacralised rows) | 51 at risk (NUM:436: the sacralised five-lumbar row, whose count does not change, is left out) | TAB2; NUM:436; RS2 N12 asks the manuscript for "at-risk" in place of "count-changing". This file uses 51 |
| VinDr-SpineXR lesion classes | 13 | 8 | the audit release row; MANIFEST section 2.1 (MAN section 10, family D unknowns row 12) |

### 7.3 Where this file departs from the review of 2026-10-08

A review of this file raised 24 points; all were applied. In four places the review's own wording did not match the
files, and this file follows the files.

| review point | what the review said | what the file says | evidence |
|---|---|---|---|
| CMB-MML / CMB-AML interventional frames | add as "searcher pass only", patient count "not recorded" (N2 likewise labels it "FOURTH-s") | both verifiers returned "partly confirmed", and they counted 16 XA patients, 35 unique 2-D frames and 3 DynaCT volumes, with one spine procedure (MSB-04031) | FOURTH r1 6 (`round1_verified` item 6, two verdicts with counts); section 2, A6 |
| Section 5.2, the countable total | "give the countable sum (about 14,290 by the rows above)" | 14,289 is 789 + 483 + 435 + 12,123 + 459: it adds CEN's field-gate passes (not its lumbosacral-countable sum) and RibFrac's rib-cage count (not lumbosacral). The lumbosacral-countable sum is about 11,770 | calc_review (`countable_LS_sum` 11,769; `reviewer_14290_is_789_483_435_12123_459`); CEN section 1 |
| The 4,276 statement | "also CLAIMS_LEDGER L246" | the current `ssn:SchwingNet/CLAIMS_LEDGER.md` line 246 is about per-device image formation; the quoted sentence ("exceeding 97.6 % with 80 % power first at 4,276") survives only in older ledger states quoted by the evaluation-gate reports; NUM:52 carries it, marked superseded | `ssn:SchwingNet/CLAIMS_LEDGER.md` line 246 (read); `ssn:SchwingNet/results/eval_gate/chk9/chk9_report.json` (the quoted "CLAIMS:L246" text); NUM:52 |
| The JHU prototype-Siemens cadaver and phantom | listed beside the LevelCheck Rando phantom as further missing items | MISSED's summary pair ("one JHU cadaver and one JHU phantom, imaged on a prototype Siemens flat-panel C-arm") is the same as findings 4 (Otake 2013 cadaver) and 5 (Otake 2012 Rando phantom); each is listed once | MISSED summary and findings 4, 5, 11; section 2, A54 and A58 |
