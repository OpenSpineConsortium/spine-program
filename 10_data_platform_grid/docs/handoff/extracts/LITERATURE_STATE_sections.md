# Extract of HANDOFF/LITERATURE_STATE.md (spinesurg-ct-nnunet 097933a)

Sections Status, Lead, How to read, 2 (what is missing, A-E) and 7 (unknowns), per DISPOSITION rows 87-90. Its companion `literature_state/dataset_landscape_by_task.md` and `ranking_joined.csv` are copied whole beside this folder.

The whole file is Greg-only and sits in the Greg-only project folders (`01_carm_level_detection/docs/handoff/` and the others `../_plan/PLAN.md` rule 3 names); this extract carries the sections that bear on the data platform, with their section ids. Path prefixes (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:`) read as the repositories of `MANIFEST_CODE.md` at the stated commits, never as a laptop path. Two researcher addresses are withheld.

---

<!-- section: Status of the numbers quoted here -->

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


---

<!-- section: Lead -->

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


---

<!-- section: How to read this file -->

## How to read this file

**File key.** Roots: `ssn:` = `<repo spinesurg-ct-nnunet 097933a>/`; `ctsp:` =
`<repo CTSpinoPelvic1K 7ddfe38>/`; `mem:` =
`<memory notes; see MEMORY.md>/`; `LS:` =
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


---

<!-- section: 2 What is missing (A-E) -->

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
| A3 | Huashan Hospital, Fudan (Shao 2024) | 140 living patients, preoperative CT and intraoperative AP and lateral films of L1 to L5; levels projectable after registration | request, not drafted; no data statement | Email Jiang Jianyuan, <corresponding author of Shao 2024, address withheld>; ask for the device make and model, DICOM headers, frames per patient and DUA terms (two co-authors are from Shanghai Maestro Surgical Robotics) | as recorded in MISSED findings 2, 12 |
| A4 | VerSeg-Net lumbar fluoroscopy | 50 patients, Philips UNIQ FD20, per-level L1 to S1 masks; an "explicit sharing statement" | searcher pass only (named in the coverage note alone); route not recorded | not recorded | as recorded in FOURTH coverage note |
| A5 | PUMCH stitching series (Liu 2026, Eur Spine J) | 43 scoliosis patients, 4 to 6 overlapping prone AP shots each on a Philips Zenition 70; the shift between shots is estimated, not recorded; no labels stated | never released: "No datasets were generated or analysed during the current study" | asking is judged unlikely to succeed; not drafted | as recorded in VIDEO; REQ (not-drafted list) |
| A6 | TCIA CMB-MML and CMB-AML interventional frames | open, CC BY. 16 living patients with XA series: 35 unique 2-D frames (Siemens AXIOM-Artis last-image-hold captures) and 3 DynaCT volumes. Only MSB-04031 is a spine procedure (AP and lateral thoracolumbar vertebral augmentation, 6 unique frames, lumbar CT from about T10 to the sacrum); the other frames are iliac-crest biopsies with about L3/L4 to S1 in the field. No annotations; positioner angles and SID/SOD in the DICOM | not fetched. The CMB-MML and CMB-AML CTs are held (MAN#idc_cmb_mml, #idc_cmb_aml); the XA frames are not | anonymous NBIA REST `getSeries`, then `getImage` by SeriesInstanceUID (the verifier pulled about 550 MB this way on 2026-09-21); re-query Modality=XA on each release | as recorded in FOURTH r1 6 (partly confirmed twice) |
| A7 | Southeast University / Bond-Star Medical (Chen, Kong et al.) | 15 living patients: 15 spine CTs and 15 real PA C-arm X-rays (Perlove PLX118F); the group's Med Phys 2025 paper reports 52 real X-ray images | never released, no route: no data statement or offer | none recorded | as recorded in FOURTH r1 21 (partly confirmed twice) |
| A8 | Hohai University / Changzhou LineReg (Shen et al., Med Phys 2026) | 10 living patients, 90 real registration samples, 710 edge-annotated images (real X-rays and DRRs mixed); distinct real exposures not stated | never released: code only (github shenao1995/lineReg); no data statement found, full text paywalled. A sibling, FlowReg (A20), holds a README only | none recorded | as recorded in FOURTH r1 19 (partly confirmed twice) and updates_to_known 12 |
| A9 | RadGS-Reg (Nanjing / Changzhou; MICCAI 2025) | 10 intraoperative spine cases, each a preoperative CT with paired AP and lateral X-rays; 30 vertebra-level samples; poses "recorded during C-arm circular acquisitions"; living or cadaver not stated | never released, no route: no data statement or request route | write to the corresponding authors (Junfeng Jiang, <address withheld>; S. Kevin Zhou, <address withheld>); the paper does not invite requests | as recorded in THIRD findings 6, 10 |
| A10 | NIT Warangal / NIMS Hyderabad (2D-3D-sci-registration) | 9 living patients and 51 AP/LAT C-arm sets in the repository README (at most 49 unique frames); the manuscript's 2 patients are not among the nine; Ziehm C-arm; preoperative CT with level-named L1 to L5 centroids | CT and raw X-rays not released ("available upon reasonable request"); 60 centroid files and 54 overlay PNGs, each holding the real frame at 8 bits beside a DRR, are public | write to the authors; no request channel, DUA or form recorded | as recorded in FOURTH r1 18 (partly confirmed twice) |
| A11 | Fourth Medical Center of PLA General Hospital (Ju et al., Sci Rep 2025) | 8 living pelvic-fracture patients, intraoperative AP and inlet X-rays with CT; "8 real intraoperative X-ray images" stated, while the figures suggest 8 AP and inlet pairs | request, not drafted: "requests for data and materials should be addressed to Jingxin Zhao" | write to <address withheld> | as recorded in FOURTH r1 23 (partly confirmed twice) |
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
| A22 | Charters 2024 (UCLA) | 527 patients, 4,213 images: 2,486 paired kV (254 patients), 58 unpaired AP kV, 1,669 MV; thoraco-abdominal spine; DICOM REG to the planning CT | request, not drafted: "available upon reasonable request from the authors" | write to <address withheld> | as recorded in PAIRED finding 7 |
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
| A33 | Pittsburgh swallow corpus (Sejdic, Coyle) | 335 people: 265 patients (1,518 clips, Toshiba Ultimax) and 70 healthy volunteers (GE); C2 and C4 corners on every frame, so cervical only | request drafted, not sent | Send `04_pittsburgh.eml` to <address withheld>; Pitt data-use agreement | as recorded in REQ item 4; VIDEO |
| A34 | Bournemouth lumbar quantitative fluoroscopy (Breen 2021) | 127 analysed adults, lateral weight-bearing L2 to S1 cine at 15 fps; per-frame angles public on OSF a27py, pixels not | request drafted, not sent | Send `01_bournemouth.eml` to <address withheld> (cc Breen); a UK data-sharing agreement follows | as recorded in REQ item 1; VIDEO |
| A35 | Osaka/NAIST hip cohort and its EOS arm (Otake, Sato, Gu; Suehara, MICCAI 2025) | 77 real EOS biplanar pelvis and hip radiographs, each 2D-3D registered to the same patient's CT; parent cohort 475 patients, 305 with QCT | EOS set: dataset link "N/A", a collaboration lead; parent cohort on reasonable request; not drafted | write to the corresponding author | as recorded in FOURTH r2 18 (partly confirmed twice) and updates_to_known 11 |
| A36 | SJTU Med-X / Tongji / TAOiMAGE standing biplanar lumbar radiographs (Yu, Tsai; Med Phys 2026) | 64 living subjects with CT (48 young adults in six movements, 16 patients), 880 real calibrated biplanar pairs; the arXiv version gives 50 subjects | request, not drafted: "available from the corresponding author on reasonable request" | write to <address withheld>, <address withheld> or <address withheld> | as recorded in FOURTH r1 20 (partly confirmed twice) |
| A37 | Bournemouth cervical QF DICOM | the pixels behind the 252 held track sequences of 63 people | request drafted, not sent | the same letter as A34 | as recorded in REQ item 1 |
| A38 | Maastricht cervical and lumbar cine (van Santbrink, Bioengineering 2026) | 112 lateral cervical recordings, 89 from 39 healthy participants and 23 from pre-operative patients with cervical radicular syndrome, with per-frame C0 to C7 contours; lumbar L1 to S1 cine (11 men, 7.5 fps) | request drafted, not sent | Send `02_maastricht.eml` to <address withheld>; GDPR data-transfer agreement | as recorded in REQ item 2 |
| A39 | Utah Hive standing pelvic tilt and Cam-FAIS records (Anderson, Atkins) | 32 living adults with CT and per-frame pelvis and femur poses from biplane videoradiography; 0 X-ray images released | the released packages hold CT, meshes and transforms; the biplane frames and calibration are withheld | a request to Anderson or Atkins (Utah) | as recorded in FOURTH r2 10 (partly confirmed twice) and refuted_or_useless; CARM finding 7 |
| A40 | Bern dynamic myelography native DICOM | the DICOM behind the 4 held MP4s (section 1.4), and the 62-patient cohort the letter asks about | request drafted, not sent | Send `03_bern.eml` to <address withheld>; a Swiss data-transfer agreement | as recorded in REQ item 3 |
| A41 | MIDRC fluoroscopy | RF 71 and XA 15 of 202,222 studies; about 17 C-arm studies of unknown anatomy, mostly bronchoscopy and swallow; no labels; people not recorded | not fetched (registration) | MIDRC registration | as recorded in THIRD finding 8 |

**A42 to A64: cadaver, animal and phantom** (by specimens)

| rank | dataset | what it would add (as recorded) | why it is missing | the step that would get it | source |
|---:|---|---|---|---|---|
| A42 | Balgrist ex-vivo lumbar (Jecklin 2024, 2025) | 13 specimens plus 6 validation specimens per the request letter (the Sci Rep paper describes 6 specimens with at least 50 X-rays each), three C-arms, fiducial projection matrices | withheld for pending patents; request drafted, not sent | Send BALG to <corresponding author of Jecklin 2024, address withheld> | as recorded in BALG; MAN#balgrist_exvivo_request; FOURTH updates_to_known 4 |
| A43 | Huang 2022 JHU cadaver long films | 13 cadavers, 100 level-labelled O-arm long films (50 AP, 50 lateral) | never released (Zenodo 7161385 holds simulations only) | ask Siewerdsen (MD Anderson) with Uneri, Zbijewski or Stayman (JHU) copied | as recorded in MISSED findings 3, 12 |
| A44 | DKFZ / Siemens cadaver spine C-arm study (Kausch et al., MICCAI 2021, MedIA 2022) | 11 cadaver specimens, 16 datasets of 1,364 real projections each (21,824), k-wires or screws in 9 | never released ("Link to the dataset(s): N/A") | none recorded | as recorded in FOURTH r1 29 (partly confirmed twice) |
| A45 | SheepSpineX (X2P-Net, SJTU) | 9 ex-vivo sheep cervical spines, about 270 AP/LAT pairs with CT and projected centroids; Siemens Arcadis Varic | request, not drafted | write to <address withheld> and <address withheld> | as recorded in MISSED finding 8 |
| A46 | UC Davis / Augmedics cadaver screw study (Global Spine J 2025) | 6 cadavers, CT and about 11 to 12 real X-ray frames in all, 151 screws from the cervical spine to the SI joint | request only: "available from the corresponding author upon reasonable request", which most plausibly covers the screw tables, not the images | write to Richard L. Price, <address withheld> | as recorded in FOURTH r1 26 (partly confirmed twice) |
| A47 | Bern canine thoracolumbar Steinmann-pin fluoroscopy (Goffart 2022) | 5 canine cadaver columns, one end-on image per pin; OrthoScan FD-OR mini C-arm | request, not drafted | write to the authors | as recorded in FOURTH r2 11 (partly confirmed twice) |
| A48 | Giessen/Jena canine biplanar fluoroscopy (Front Vet Sci 2021) | 4 living dogs, biplanar fluoroscopy of pelvis, sacrum, L6 and L7 with per-frame poses against a same-dog CT; calibration films archived | request, not drafted: the archive files return HTTP 403 without login | enquiries to Prof. Martin S. Fischer, <address withheld> | as recorded in FOURTH new_confirmed and r2 0 (partly confirmed twice) |
| A49 | BG Klinik Ludwigshafen, MINTOS (Brunken 2026, J Imaging; Bullert, Eur Spine J) | 4 whole-body cadavers, 384 images evaluated, three Siemens Cios detectors (Fusion, Flow, Flow.neo) | request (J Imaging); the Eur Spine J paper says "No datasets were generated or analysed"; not drafted | write to <address withheld> | as recorded in FOURTH r1 28 (partly confirmed twice) |
| A50 | UMC Utrecht / Philips cadaver skin-marker registration (Bindels 2022) | 3 cadaver torsos, 780 vertebra registrations; Philips Zenition 70 and AlluraClarity FD20 | never released, no route | none | as recorded in FOURTH r2 15 (confirmed and partly confirmed) |
| A51 | Xinqiao Hospital live-minipig study (BMC Musculoskelet Disord 2025) | 3 live minipigs at L1 to L5, G-arm and C-arm, marker points; no CT and no level labels | images on request, not drafted | <address withheld>, <address withheld> | as recorded in MISSED finding 9 |
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
| C3 | Kwak, Ro, Kang 2025 (J Clin Med) | 3,116 standing lateral lumbar films, 1,941 LSTV (62.3 %, labels text-mined from MRI reports), 313 test | never released; "may be shared upon reasonable request" | write to <address withheld> (corresponding), copying <address withheld> (data curation) and <address withheld>; ask for the label table, or the weights and test-set ids, not the images | as recorded in mem:lstv-data-landscape.md and RF18 finding 12 |
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


---

<!-- section: 7 Unknowns (7.1-7.3) -->

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

