# Extract of HANDOFF/RESEARCH_DIRECTIONS.md (spinesurg-ct-nnunet 097933a)

Sections Lead, 5 (5.1-5.5), 6 (the ranked list; DAT-1 is rank 6), 7, 8 and the file key, per DISPOSITION rows 80-86.

The whole file is Greg-only and sits in the Greg-only project folders (`01_carm_level_detection/docs/handoff/` and the others `../_plan/PLAN.md` rule 3 names); this extract carries the sections that bear on the data platform, with their section ids. Path prefixes (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:`) read as the repositories of `MANIFEST_CODE.md` at the stated commits, never as a laptop path. Two researcher addresses are withheld.

---

<!-- section: Lead -->

## Lead

The evidence supports one order of work: measurement first, human reads second, models third. On ordinary spines the 2-D system is at ceiling on plain film and near ceiling on the one real C-arm. It names 97.4 % of bodies on a whole lateral frame and 74.8 % with one body in view, NUM:463. On transitional spines no number exists on a real frame with a human read. The one fact that constrains every project is that the verified real-frame transitional test count is zero today, NUM:435; LS Lead. The best rendered L6 recall is 56.1 to 72.4 % on ten held-out persons, ALPHA Verdict. Human readers reach 32 % sensitivity for Castellvi type on radiographs against 76 % on CT, HANH lines 130 to 131 and 27 to 28. Greg's parity idea is sound, but its 3-D target is not yet in the form the goal needs. The published 0.990 for T12 against L1 divides five of its eleven features by the patient's median over three or more levels and leaves the six between-measure ratios undivided, SEP lines 55 to 80. Its dominant feature is the transverse-process span, which is coronal, SEP rerun 2026-10-08. No lumbosacral 3-D classifier exists at all, MPDA lines 335 to 342 and 905 to 907. So the first two projects are an hour on the laptop and a day on the grid. They define the single-vertebra 3-D target, then measure which 3-D features survive projection, per view, on exact-pose renders of the 802 labelled CTs. In the same week the reader work that creates power starts. That work is a one-hour coverage render on COBRA, a reader queue of 63 volumes, the seven CTSP re-reads, the VerSe mask count and the whole-cohort Castellvi read. Models wait for a frozen truth file and a clean encoder. The first clean model is expected to fail its validation screen, and that failure is itself the result the standing determination asks to be stated plainly, LTDG.

---


---

<!-- section: 5 Datasets by project (5.1-5.5) -->

## 5. Datasets by project

"After migration" is a target path, not a state. No HOME imaging folder had moved on 2026-10-07, B06 was copied on 2026-10-08 with finalization unrecorded, and a direction that reads from `$RS` must first check `runs/<B>/STATUS` on the grid, MAN section 4 row 40; DDP; MP section 5.

### 5.1 The fluoroscopy classifier

| source | holds | labels, who made them | transitional content | restrictions | bank or split today | leakage into the current encoder | file |
|---|---|---|---|---|---|---|---|
| C-ArmLSpine | 149 sessions, 299 spot frames, 149 CBCTs | none released; two automatic labellers on the CBCT; poses by edge registration | 3 L6, one labeller, test only | CC BY 4.0; a real name in case134 headers | `realxray/carmlspine` 148 cases split 105/15/28, the pre-repair count, MAN lines 13833 and 13905, against 149 live; `carm_cv0..4`, `carm_cvday0..2` | the older `carm_cv*_drr` fine-tunes descend from v7; the zero-shot v9 numbers are clean, and the 97.4 % in 1.1 is the gated v9-lineage rerun, NUM:463 | MAN carmlspine |
| COBRA2026 | 692 cases, 375,618 projections | automatic; two-labeller boxes on 150 Elekta exports | 91 screen calls, 57 field-supported, 7 with a frame | CC BY-NC; 175 cases embargoed to 2032 | 145 cases in `realxray/cobra_elekta*`, 3,480 frames; Varian 0 | not in the level bank | MAN cobra2026 |
| DeepFluoro | 6 pelves, 366 frames with exact pose | one merged vertebra class; 14 pelvic landmarks | none | NC either way | `realxray/deepfluoro` 238/24/104 by specimen | detector and card only | MAN deepfluoro_h5 |
| BUU-LSPINE | 3,600 cases, 7,200 films | end-plate lines; levels counting-inferred; L4L6 sheet | 129 four-lumbar, 15 six-lumbar; 9 of 15 children | EULA; "No License Provided"; owner-only | 3,603 laterals in v9; AP films in no bank | all laterals in v9 lineage | MAN buu_lspine_3600 |
| CSXA | 4,963 lateral cervical | expert corners C2 to C7 | none | CC BY 4.0 | all in v9, 4,214 train, 749 val | all in v9 | MAN csxa |
| NHANES II | 17,073 films; 543 landmarked | expert landmarks on 543; pseudo on the rest | none read | public domain | 543 in v9; 16,531 in no trained bank | 543 in v9; v2, v6, v7 twice | MAN nhanes2 |
| VinDr-SpineXR | 10,466 images, 5,000 studies | lesion boxes; pseudo levels on 7,625 | a tier-B pseudo-flag count off the junction was quoted as 209 in the notes; 209 is not on disk | PhysioNet DUA; no WSU determination | 0 in v9; 7,625 in `vindrps` and v7 | `vindrps` 77.8 % validation leak | MAN vindr |
| render banks | ctsp_drr 802; physics_drr 7,045; physics_rare 1,482; verse_drr 387; ts_drr 2,905; xrsp1k 6,416 | CT labels projected | physics_rare: 34 CTSP plus 47 VerSe transitional series | inherit CT terms | v9 = films_drr + ctsp_drr + verse_drr + physics_drr + physics_rare | all inside v9; TS bench inside v9 except 70 | MAN render cards; TSB |
| the G3 split | 50/10/40 per subtype; every real transitional subject in test | | test L6 43 plus 3 real, of whom about 29 carry an L6 mask a render can score and 14 are audit-only; T13 3, sacralised 11, Castellvi 12, lumbar rib 6; validation L6 11, 7 render-scoreable and 4 audit-only; T13 1, SPLT lines 26 and 35 | | leak audit PASS 2026-09-23 | 92 of 97 validation and test persons sit in v8 or v9 training | SPLT; TAB2 note d |

### 5.2 CT projects

| source | holds | labels | transitional content | restrictions | state | leakage and traps | file |
|---|---|---|---|---|---|---|---|
| CTSpinoPelvic1K v11 | 802 records, one per patient; 422 supine, 377 prone, 3 decubitus | radiologist-sourced vertebrae; sacrum and hips expert where fused, pseudolabel otherwise; ribs student-corrected; Castellvi two-reader consensus on 33 | L6 18 by label, 16 by the readers; graded 33; sacralised fused 12 by label, 9 as truth; four-lumbar 9 two-labeller; no FOV reaches T1 | CT CC BY 3.0; labels CC BY-NC-SA 4.0; the HF mirror is v10 with id 29 | Zenodo v11; grid `~/data/CTSpinoPelvic1K/labels` | shipped folds never read the lumbar count; token is not the record id; 801 of 802 in v9 lineage via renders | MAN ctspinopelvic1k; HFM; CSB |
| CTSpine1K | 1,005 volumes | expert VerSe-convention masks | README lists 24 lumbarisation and 13 sacralisation, an authors' list; 3 new read-tier persons in MSD-T10 | CC BY-NC-SA 4.0 | Ceph-native | 782 COLONOG volumes are CTSP persons | MAN ctspine1k; DDP C02 |
| VerSe and VerSeFusion | 374 scans of 355 subjects | expert masks C1 to L6, T13 = 28; Loeffler 2021 table, two neuroradiologists | read tier L6 85, T13 6, sacralised 13, Castellvi II 27, lumbar rib 12, stump 18 | CC BY or BY-SA, quoted both ways | B06 copied 2026-10-08, finalization unrecorded | `has_T13` is wrong, 18 against 6; 39 of 85 L6 masks lack id 25; never `vf_813` for whole-spine work; verse707 conflict | MAN versefusion; VFT; VF8 |
| TotalSegmentator v2 and v3 | 1,228 and 1,935 scans | 117 structures, model output refined; no L6, T13 or lumbar-rib class; `sacrum` excludes S1 | two-labeller L6 14; outside reads on 70 CTs, 28 L6, found 12, 17 and 9 | CC BY 4.0 | B07 plan | 1,118 v3 CTs byte-identical to v2; `s####` not stable across releases | MAN totalsegmentator; TSS; DDP A05 |
| the acquisition tiers | 21,622 CTs; tier 1 5,094; tier 2 12,217 | two pseudo-labellers; no radiologist read on any acquired CT | flags L6 303, T13 82, review 1,168; expected over the 18 screened collections L6 322, T13 38 to 119, N4 line 137; over the whole holding T13 44 to 138, LS line 676 | open routes | Ceph-native | 127 exact folds merged; 1,186 near-duplicates unmerged | TIERS; LS section 5 |
| Dataset813 and Dataset815 | 802; 1,176 cases | nnU-Net raw | 18 L6; 62 L6 and 4 T13 by manifest | NC-SA | 815 never preprocessed | 813 flags stale; image links resolve only inside the container | MAN nnunet cards; D813 |
| RibFrac, RibSeg v2, Möller masks | 660 chest CTs | expert ribs 1 to 24; stump masks | T13 4 single-labeller | RibFrac CC BY-NC; Möller CC BY | Ceph-native | 648 of 743 analysed, 95 unexplained | MAN ribfrac; STUMP |
| RSNA 2022 cervical | 2,019 studies | per-level fracture labels | none | Kaggle, non-commercial | zip never unpacked | used by nothing | MAN rsna_2022 |

### 5.3 Paired sets for parity

| set | 3-D side | 2-D side | pose | per-vertebra 2-D truth | what it can test | file |
|---|---|---|---|---|---|---|
| C-ArmLSpine | 149 lumbar CBCTs | 299 spot frames, 2 sweeps | registration, verify by boxes | automatic, agreed levels | the only living-spine real pair; 3 L6 | MAN carmlspine |
| DeepFluoro | 6 pelvis CTs | 366 frames | exact | none per vertebra | the projection operator, not identity | DFC |
| COBRA2026 | 692 planning CTs on `ct_def` | 375,618 projections | exact by RTK | none; coverage unverified | second device for sacral features once verified | MAN cobra2026 |
| Ljubljana | 1 cadaver L1 to L5 | 18 radiographs | gold per vertebra | gold, five bodies | n 1 check of the projected-landmark step | MAN ljubljana |
| the programme's renders | 802 CTSP, 374 VerSe, TS, 81 transitional series | ctsp_drr, physics_drr, physics_rare, xrsp1k, devcorpus arc | exact by construction | full level truth; boxes and end-plate corners only | the visibility experiment | MAN render cards |

### 5.4 Holdings no model uses

| item | n | why unused, as recorded | what would change it | file |
|---|---|---|---|---|
| NHANES II unannotated films | 16,531 | never offered to the detector | directive D2, detector self-training | MAN nhanes2; XDU |
| BUU-LSPINE AP films | 3,600 | in no bank; no written criterion | a bank or a one-sentence written exclusion | MAN section 4 row 31 |
| VinDr in the shipped bank | 0 of 10,466 | pseudo levels; test split consumed; DUA | a determination and study-keyed splits | MAN vindr |
| AASCE 457, Spinal-AI 8,358, anchor_drr 7,842, Mendeley 584, lateral_236 212 | per row; the labelled-film counts are XDU lines 17 to 37, anchor_drr 7,842 is CORP note k | fed only deleted banks; anchor_drr's own split puts 301 of 801 CTSP people on both sides, MAN section 4 row 18; DDP C10; Spinal-AI has no person; Mendeley is a BUU redistribution | AASCE and Spinal-AI by directive D6, each wholly on one side; Mendeley stays out | XDU lines 17 to 37; CORP note k; MAN section 4 row 18; DDP B09 and C10 |
| RSNA 2022 cervical fracture CT | 2,019 studies | used by nothing | a cervical arm, none planned | MAN rsna_2022 |
| COBRA cases not exported; Varian | 547 of 692; 225 | exporter refuses Varian; the axis map was solved 2026-09-23 | write the Varian export; directive D4 | MAN cobra2026 |
| DeepFluoro vendor frames without a pose | 2,293 of 2,659 | no released pose | pose recovery, unrecorded | MAN deepfluoro_vendor |
| C-ArmLSpine sweep projections and the case134 spin | 602; 302 frames | only one script reads a sweep | export into the real-frame layout | MAN carmlspine; FP G4 |
| ts_drr_v3 | 1,735 renders | never benched | a held-out TS test by CT hash | DDP B04 |
| Dataset815 | 1,176 cases, 62 L6 | never preprocessed | `sbatch slurm/prep815.sh` where singularity resolves | MAN nnunet_dataset815 |
| tier-1 acquisition CTs | 20,280 screened | read by no one; in no bank by design | the reader queue | LS section 5.2 |
| FluoroCap | 29,500 panels | dropped by directive D1; the 200-panel test set does not exist | annotate about 200 or write it off | MAN fluorocap; DD23 |

### 5.5 Missing sets and the step to get each

| set | adds | state | the step | file |
|---|---|---|---|---|
| LevelCheck clinical cohort | 178 patients, 178 CTs, 398 intraoperative radiographs; about 16 at-risk persons at 9 % | no request drafted | Greg drafts a letter to the I-STAR group | LS A1 |
| Huashan | 140 patients, CT with intraoperative AP and lateral; about 13 at-risk | no request drafted | email <corresponding author of Shao 2024, address withheld> for device, headers, frames per patient, DUA terms | LS A3 |
| SX-Stitch | 1,032 overlapping intraoperative frames with masks | drafted 2026-09-23, not sent | send | SXS |
| Balgrist ex-vivo | 13 plus 6 specimens, three C-arms | drafted, not sent | send | MAN balgrist card |
| fourteen cine letters, Bournemouth among them | real cine with level-named tracks | drafted, not sent | send | MAN cine requests card |
| Charters 2024, UCLA | 527 patients, 2,486 paired kV with DICOM REG | not drafted | write | LS A22 |
| Jaganathan and Maier | 55 thoracolumbar CBCT sweeps | never released | ask FAU or Siemens under a DUA | LS A32 |
| TCIA CMB-MML and CMB-AML XA | 16 patients, one spine procedure | open, not fetched | anonymous NBIA fetch as a Slurm job | LS A6 |
| NIT Warangal | 9 level-named patients | public | download | LS A10 |
| Merlin, Stanford AIMI | E_low 1,260 transitional people, more than all of tier 1 at 831 | gated, no form signed | Greg accepts the AIMI DUA | LS B1; ACQ section 7 |
| CT-RATE, INSPECT, NLST beyond the pilot | T13 95, 86 and 109 expected at the low prior | gated or held by the stopping rule | the HF gate form; the AIMI DUA; finish the tier-1 screen | LS B3, B5, B6 |
| Griffith 2022 per-level SDs | the closest matched comparator for the atlas | paywalled | interlibrary request | LM "Still open" |
| Li 2016, Li 2017, ABLSpineLevelCheck 2024 | the naming-novelty risk; the one title near the parity question | IEEE Xplore blocked | a library request before any submission | RFP |

---


---

<!-- section: 6 The ranked project list (DAT-1 is rank 6) and the time order -->

## 6. The ranked project list

| rank | project | first step | gate | n today against n needed | the decision it returns | depends on |
|---|---|---|---|---|---|---|
| 1 | PAR-1, the single-vertebra 3-D target | the ratio-only variant of `test_morphometric_separability.py`, T12 against L1, one hour on the laptop | AUC at or above 0.95, 0.90 to 0.95, or below 0.90 | 1,486 against 1,486; L6 13 positives against 757, nothing finer than "some signal" | what parity is measured against: one body, one body plus a neighbour, or a window | nothing |
| 2 | PAR-2, projected morphometry at exact pose on 802 v11 volumes | fifty records, lateral and AP, T12 to L4, a two-hour smoke test on `reqp`, with the job ids and ETA written to the resume file; then all 802 and the arc, where the gates are scored | per-feature ICC tiers 0.75 and 0.50; junction AUC tiers 0.97 and 0.90 | 1,486 against 1,486 | the per-feature, per-view visibility table and the view each confusion pair needs | PAR-1's feature list; the v11 tree on the grid |
| 3 | FLU-1, the real-frame transitional truth file | the one-hour COBRA coverage render; then the 63-volume reader queue under a frozen protocol; then the Elekta export of every confirmed case | 22 carriers for 85 %; 35 at-risk persons for 90 %; 19 for paper 2 H1 | 0 verified against 22 or 35; expected about 5 to 13 verifiable on CT, at most 19 if every supported call confirms, calc at the labeller's PPV of 10 of 24; 22 cannot be reached from COBRA alone; scorable on a real frame only where a frame is exported, 7 of 91 calls today, NUM:435 | whether any anomaly-aware claim on real frames can ever be powered from the holding; DAT-1 is the only route to 22 | a reader; the protocol freeze; the Varian exporter or a written Varian exclusion |
| 4 | CT-3, the re-reads, the VerSe mask count and the whole-cohort Castellvi read | the VerSe raw-mask count script, under an hour; the nine CTSP re-reads with a third reader | II to IV rate inside 9 to 18 %; second-reader kappa at or above 0.63 | 33 graded against 71 to 142 expected | the lumbosacral truth pools and the rib co-occurrence test at power 0.98 | two readers and an adjudicator |
| 5 | CT-1 and CT-2, the ostk fix and the anterior pelvic plane | 0097 alone, under an hour; fifty records with ten renders, two hours | 0097 within 1 mm; APPA inside the supine band; the v11 gap to Veilleux confirmed at 0.1 before the fit | 802 | safe 3-D columns for every twin; the APP-referenced sacral slope beside the scanner-axis one | nothing |
| 6 | DAT-1, send the drafted requests, draft two, fetch two | the letters out this week; record "sent" in the manifest card | a reply naming a DUA route for at least one set of 100 or more living patients | 0 sets against 19, 35 or 60 persons | whether real transitional n can come from outside the holding | Greg's signature |
| 7 | PAR-3, Farshad 2013 on lateral renders | the 21 graded III and IV records and 100 ordinary renders, half a day | sensitivity at or above 0.75 transfers; below 0.60 the lateral is empty for the fused class | 21 positives, 643 negatives | the one literature-grounded lateral feature, or its absence | the v11 end-plate corners from PAR-2 step 1 |
| 8 | PAR-4, pose quality against naming on C-ArmLSpine, and the sacra called L6 | the exactness-by-NCC-quartile table, two hours; render the 24 sacrum crops and the four off-bone laterals | odds of an error per 0.25 body of disagreement with an interval excluding 1 | 617 lateral and 631 AP bodies; 24 sacra | go or no-go for the real paired probe; a crop rule or a class problem for the sacrum | the per-frame registration scores on the grid |
| 9 | FLU-2, the clean-lineage encoder on G3, validation side, with the count-against-morphology agreement | one seed, lambda 0, job ids and ETA written to the resume file; scored on the 7 render-scoreable of the 11 validation L6 persons; then three seeds, two heads, and `alphabet_couple.py` on the same frames | the screen of section 2.8: zero or one miss of 7 proceeds, two or more stops, before any test or real arm; the count catches at least 80 % of run-shifted films | 7 render-scoreable of 11 validation persons; about 29 of 43 test persons after "H1 seen", zero misses of 29 for the 85 % bound; at a true 72.4 % the screen passes 38 % of the time and at 85 % 72 %, calc | the first quotable held-out render number, or the "not at parity" sentence; whether the two mechanisms are a measured property | FLU-1's protocol; PLAN decision 3 for the audit-only persons; the paper 2 ledger entry before any test person; the BUU licence decision before any weight leaves |
| 10 | CT-4, the 3-D single-body classifier and the LS-L6 certification | J0 timing on 20 CTs; the facet-angle model on unambiguous bodies | PPV lower bound 0.90 on LS-L6, at most 3 errors on 88 | 88 against 88; every other phenotype short by 7 to 33 reads | the 3-D side of parity at both junctions; reader E for the fusion | CT-1; CT-3's re-reads; Greg's fourteen decisions |
| 11 | PAR-5, the real paired probe on C-ArmLSpine | `level_morphometry` on the CBCTs; the pose re-fit at 0.150 mm; the embedding regression per feature per view | Q² above 0.5 on the lateral for any feature beyond height and wedge, or the parity work moves to AP | L1 in 76 lateral frames; L2 to L5 in 123 to 142 | which 3-D features a real frame carries, per view, on living spines | PAR-2's definitions; PAR-4's verdict; CT-1 |
| 12 | PAR-6, the measured 2-D feature arm and the V1 to V4 variants | V0 under the ALPHABET_LOSS protocol; each variant only after Greg's decision | HELPS, TRADE-OFF, HURTS or NOT SHOWN by the pre-stated rule | evidence persons 10 held-out L6 and 0 T13 | whether explicit 2-D morphometry moves the junction pairs, with a number | PAR-2, PAR-3, PAR-5, FLU-2 |
| 13 | CT-6, the L6 learnability curve on Dataset815 | preprocess 815 where singularity resolves; repair the flags | Dice leaves zero at 36 or stays zero at 62 | 62 distinct L6 with a read | whether L6 is learnable as a voxel class from this corpus | GPU time; CT-3's flags |
| 14 | CT-5, CT-7, CT-8, CT-9, CT-10 | as in section 4 | as in section 4 | as in section 4 | atlas revision; the anchor-ordinal premise; the rib phenotype; the census adjudication; the benchmark | CT-1; the PREREG freeze; readers |
| 15 | PUB-1, the dataset article resubmission and paper 1's rigor fixes | the seven items to Greg as a list; `build.sh --reprint`; the eight fixes on existing outputs | ten published pages; `eval_gate` held out on every quoted row | none by policy | a citable dataset article; a submittable paper 1 held for the TTO | Greg; the TTO answer |
| 16 | CT-11, prone and supine mobility | twenty pairs pseudolabelled out of fold | PI invariance | 351 pairs | a later paper | recorded as not a now-thing |

### The time order and the dependencies

Week one has no model in it. PAR-1 runs on the laptop in an hour and tells everyone what parity is measured against. The COBRA coverage render and the VerSe mask count run as single one-hour jobs on `reqp`. PAR-2's fifty-record pilot and CT-1's 0097 test run the same day. The drafted letters go out and the two new drafts are written, because they cost nothing and set the clock on the only route to real transitional persons outside the holding. The reader queues open: the seven CTSP re-reads plus 0172 and 0068 first, then the 63 field-supported volumes, then the 802 for Castellvi grade. If a reader is free on Monday, the 11 field-supported COBRA L6 calls are the single most decisive afternoon in the holding, because they can retire the real-frame transitional claim before any model is built.

Weeks two to six. PAR-2 runs on all 802 and the arc. CT-2 closes the anterior pelvic plane and REPRODUCE.md item 1. PAR-3 reproduces the one lateral rule. PAR-4 decides whether the registered poses are good enough for a real paired probe. FLU-2 trains the clean encoder from ImageNet and is read on the validation side only. CT-3's Castellvi read proceeds at 3 to 5 minutes a case.

After CT-1 and CT-3's re-reads. CT-4 runs J0 and then the facet-angle model and the LS-L6 pool. CT-6 preprocesses Dataset815 when a singularity partition is free. PAR-5 runs when PAR-2 has frozen its definitions and PAR-4 has passed.

After FLU-1's read. If 19 or more at-risk persons are verified with an exported frame, paper 2's power is recomputed under the replacement detector and the gate is unblinded under the frozen protocol. If fewer, paper 2 is restated as awaiting verified cases and DAT-1's replies decide its future. Only then is any G3 test transitional person scored, and only after the "H1 seen" entry.

Last and conditional. PAR-6 and the V1 to V4 variants, each as an arm Greg has decided on, each under the ALPHABET_LOSS protocol, each reported with its false-variant cost beside its recall.

Three things run through the whole order. If CT-3's re-reads move a record, the G3 split changes and the leak audit is re-run before FLU-2 scores anyone, SPLT header. No weight trained with BUU laterals leaves until Greg has read the licence. Nothing trains on the flagship recipe before gates G0 to G3 close, and which gates are formally closed is not written in one place on this laptop; `tools/pipeline_state.py` on the grid is the authority, FP "Gates"; note 6 Unknowns.

---


---

<!-- section: 7 Where the proposals disagreed -->

## 7. Where the proposals disagreed and what was decided

The three proposals agreed on the facts and disagreed on the axis of ranking.

Proposal A ranked by how soon a number comes back that changes a decision, using only data in the holding. It put the hour-long ratio-only 3-D run first and the clean encoder ninth.

Proposal B made Greg's parity idea the spine. It put the full projected-morphometry study first, wrote the richest feature inventory and the model variants with their published analogues, and placed the human reads second.

Proposal C ranked by whether a pre-stated claim can be decided at the n on disk in a paper that already has a home. It put paper 1's close-out and the whole-cohort Castellvi read first, placed the parity study seventh, and named the claims unreachable at any n.

This document takes B as the programme. Greg's three asks are its structure, and its feature-level specification is what a student can act on. Every proposal agreed that the geometry experiment needs no reads, no decisions and no network. It grafts from A the "smallest experiment that changes a decision" for every project. It also takes A's ordering of the ratio-only 3-D run before the full projection study, since the full study inherits its feature list from the hour-long one. It grafts from C the venue and power discipline and the list of claims unreachable at any n. It takes from C the whole-cohort Castellvi read, the single largest increase in read positives on data already held, and the week-one sending of the drafted letters, which A excluded by its own rule. Where B put the geometry experiment ahead of the reads, this document runs them in the same week. The reads are the binding constraint for the fluoroscopy classifier and the geometry experiment is the binding constraint for the parity claim, and neither waits on the other.

| item | proposal A | proposal B | proposal C | decided here |
|---|---|---|---|---|
| rank 1 | the ratio-only 3-D target, laptop, one hour | projected morphometry at exact pose, grid, one day | paper 1 close-out | the ratio-only run first, the projection study second; paper 1's fixes are housekeeping, not research |
| the reads | ranks 3 and 4 | rank 2 | ranks 2 and 4 | the same week as the geometry work |
| sending the drafted requests | excluded by rule | rank 10, "this week, zero cost", B line 357 | rank 5, "this week" | week one, zero cost |
| the junction AUC gate for the projection study | not stated as a single number | three tiers, 0.97 and 0.90 | within 0.02 of 0.990, or below 0.95 stops | the three tiers, so both earlier thresholds are visible |
| the 85 % bound on 43 test L6 persons | at most 2 misses, from the n 45 row | at most 1 miss, by calculation | at most 2 misses | at most 1 miss; 42 of 43 gives 87.9 %, 41 of 43 gives 84.5 % (calc); on the about 29 render-scoreable test persons zero misses, 29 of 29 gives 88.3 % (calc) |
| the lumbosacral parity target | scope parity to the thoracolumbar junction and the fused L5 unless the 14-row run surprises | no claim until a 3-D single-body number exists on the same persons | excluded from the projection study as undefined in 3-D | B's rule, with A's 14-row run as the first test and C's exclusion from any AUC |
| the clean encoder | rank 9, expected to fail its gate, which is the decision | rank 6, after the protocol freeze | rank 6, validation side only | rank 9, validation side first, one seed at lambda 0 as the smallest step |
| the model variants V1 to V4 | deferred until the projection study and the lateral rule return | each an arm, each needing Greg's decision | not ranked | B's table, placed last, each after Greg's decision |
| paper close-outs | not ranked | not ranked | ranks 1, 9 and 11 | listed as housekeeping beside the research list |

---


---

<!-- section: 8 Unknowns (1-30) -->

## 8. Unknowns

What is not on disk, where it was looked for, and why it matters.

| # | unknown | where it was looked for | why it matters |
|---|---|---|---|
| 1 | the ratio-only single-vertebra T12 against L1 AUC, with no case median | SEP; AOD; `ctsp:docs`; `paper/mpda` | the 3-D side of parity; PAR-1 answers it in an hour |
| 2 | any per-feature, per-level, per-view measurement of what survives projection, anywhere | the research JSONs, `SchwingNet/lit`, `research_notes`, `reports`, `ctsp:docs`; grep for "visib", "shape model", "reconstruct" | none exists; PAR-2 is the first |
| 3 | any CT L6 or lumbosacral naming rate from the programme's own model | NIPS, voxel-level only; TAB2; LS 7.1 row 39 | parity cannot be claimed against an unmeasured number |
| 4 | a human level read on any real fluoroscopic frame | RES; MAN carmlspine; LS 7.1 row 1 | every real 2-D number is against automatic truth |
| 5 | whether COBRA2026 projections cover L5 and the sacral ala | PAIRED, marked unverified; LS 7.1 row 15 | decides whether COBRA is spine data for the sacrum anchor and whether its 91 calls can be scored |
| 6 | how many of the 57 field-supported COBRA calls and the 303 L6 and 82 T13 acquisition flags are transitional | TAB2 note e; TIERS; no read exists | the whole yield of FLU-1 and CT-9 |
| 7 | whether C-ArmLSpine's 149 cases are 149 living people, under what ethics approval, and how its pose was obtained | FOURTH unknowns; LS 7.1 row 7 | the person unit of every real-frame interval |
| 8 | whether naming accuracy on C-ArmLSpine tracks registered pose quality | MAN carmlspine, "not measured" | PAR-4 and PAR-5 depend on it |
| 9 | the 3-D morphometrics of the C-ArmLSpine CBCTs | nowhere on disk | the input to PAR-5 |
| 10 | whether any drafted data request was sent or answered | the three manifest request cards, "Sent: not recorded"; LS 7.1 row 8 | DAT-1's whole premise |
| 11 | what Li 2016, Li 2017 and ABLSpineLevelCheck 2024 report | RF22 sections 5.2 and 6; IEEE Xplore blocked | could overturn paper 1's naming-novelty sentence; Li 2017 is the one title near the parity question |
| 12 | the true person-level transitional naming accuracy of any arm on real frames | PJ; RS2 S2; LCM section 8 | every power row needs it; every planning value assumed 95 to 99 % |
| 13 | which gates G0 to G7 are formally closed | FP; the top of the resume log; NUM | the time order assumes G3 is built and G4 is not; `tools/pipeline_state.py` on the grid is the authority |
| 14 | the state of the data migration and whether any batch is finalized | MP, no `runs/<B>/STATUS` on this laptop; DDP | every "run this on the grid" step |
| 15 | the TTO's answer on Part B | CNS | paper 1 and the QI protocol cannot leave without it |
| 16 | which licence reading holds for CTPelvic1K, VerSe, DeepFluoro, Geneva and Ljubljana, and the BUU EULA terms for derived labels | MAN section 4 row 8; LS 7.1 row 26 | which banks may back released weights |
| 17 | the VerSe L6 count, 85, 47, 50 or 87 | CORR; POS; LS 7.2 | a count from the raw masks has not been done; CT-3 does it |
| 18 | how many LSTV a whole-cohort Castellvi read adds | MPDA lines 919 to 921; N4 section 4 | 71 to 142 is a prior |
| 19 | whether the 1.6 % four-lumbar and 0.64 to 2.0 % T13 priors trace to a verified primary | PLAN Appendix A | every expected transitional yield inherits them |
| 20 | the source of "about 0.7 AUC from 2-D angles alone" and of "best whole-spine identification 96.5 % on MRI" | PPD; SPH; LS 7.1 row 32 | not used as checks here |
| 21 | whether the SyntheX deposit 2PGJQU and the CT Colonography localizers are on disk | LS D12 and E15 | a matched real-and-render hip set; same-patient scouts for up to 754 CTSP people |
| 22 | a manual spinopelvic read on any CTSP record | SPE; `ostk:projects/README.md`; BIBM | the only outside check on PI, SS and PT; CT-2 adds it |
| 23 | the denominator of "L6 44.9 %" and the v6 interior result files | FCM line 141; the grid-only `~/model_night/interior_windows` | the quotable anomalous film numbers come from a memory note |
| 24 | whether the 2026-09-17 refutation of pretrain-then-fine-tune was ever re-run on a clean bank | RR17 | the training-schedule default rests on a leaked-bank arm |
| 25 | who wrote the XRSpinoPelvic1K corner projection and whether its corners were validated against a reader | MAN xrspinopelvic1k, "status not recorded" | PAR-2's starting bank |
| 26 | the Ferguson view as a verified definition | the pathology sweep, whose skeptic pass never ran | the AP projection the Castellvi literature uses |
| 27 | the person counts behind AASCE's 217 index groups, CSXA's one-image-one-patient assumption and VinDr studies per patient | PIS section 4 | every leak check is only as good as these keys |
| 28 | a validated reject rule or variance decomposition for any 3-D measure | LM "Still open" | the yardstick for how much 2-D error is method |
| 29 | the spinopelvic numbers SPE section 5 argues from, PI 52.6, SS 33.1, PT 19.6, against the v11 release table's 52.1, 36.6, 15.5 | SPE lines 153 and 180; MPDA lines 723 to 727; note 6 row 84 | SPE section 5 predates the 2026-09-11 plate fix and is stale; its 3.4 degree gap is 0.1 on v11; the section needs a rewrite, and CT-2 checks the gap before fitting anything |
| 30 | the source of the VinDr tier-B pseudo-flag count of 209 | MAN vindr; XDU; TIERS; LS | quoted in the direction notes; not on disk |

Two numbers quoted in the direction notes have no on-disk source and are not used as checks: the "about 0.7 AUC from 2-D angles" paper and a TotalSegmentator Dice of 0.943, note 4 flag 8.

---


---

<!-- section: File key -->

## File key

Roots.

| key | path |
|---|---|
| `ssn:` | `<repo spinesurg-ct-nnunet 097933a>/` |
| `sn:` | `ssn:SchwingNet/` |
| `ctsp:` | `<repo CTSpinoPelvic1K 7ddfe38>/` |
| `ostk:` | `<repo OpenSpineToolkit cb43197>/` |
| `np:` | `<laptop folder Desktop/NextPaper; not a dependency>/` |
| `mem:` | `<memory notes; see MEMORY.md>/` |
| notes, proposals | `<session scratchpad; not a dependency>/directions/{notes,proposals}/`; note 1 to note 6 are `topic1_*.md` to `topic6_*.md`; proposals A, B, C are `A_fastest_to_decisive_evidence.md`, `angle_B_parity_spine.md`, `angle_C_powered_claims.md` |
| `$RS` | `/rs/rs_grp_oschome/go2432` on the grid |

Abbreviations, alphabetical.

| key | file |
|---|---|
| A5 | `sn:results/a5_rows.csv` with `a5_rows_meta.json` |
| ACC | `ssn:docs/DATA_ACCOUNTING.md` |
| ACP | `ssn:tools/alphabet_couple.py` |
| ACQ | `sn:results/transitional_registry/acquisition/ACQUISITION_PLAN.md` |
| ALPHA | `sn:results/ALPHABET_LOSS.md` |
| AMS | `mem:anomaly-manifest-sources.md` |
| AOD | `ctsp:docs/ANCHOR_ORDINAL_DESIGN.md` |
| ASS | `mem:acquisition-space-saturation.md` |
| AUTO | `sn:lit/ct_lstv_classifier/lit_ct_lstv_automation.md` |
| BHI | `ctsp:docs/BODY_HEIGHT_INVESTIGATION.md` |
| BIBM | `np:bibm-spinopelvic/main.tex` |
| BP | `ssn:docs/BENCHMARK_PROTOCOL.md` |
| CBM | `mem:competitor-benchmark.md` |
| CIT | `sn:lit/CITABLE_CLAIMS.md` |
| CL | `sn:CLAIMS_LEDGER.md` |
| CLAUDE | `ctsp:CLAUDE.md` |
| CLD | `mem:context-ladder-2d-level-experiment.md` |
| CLE | `mem:carmlspine-level-experiment.md` |
| CNS | `mem:cns-deck-v2-2026-09-25.md` |
| CORP | `sn:tables/tab_corpus.md` |
| CORR | `sn:lit/ct_lstv_classifier/CORRECTIONS.md` |
| COUNT | `sn:results/COUNTING.md` |
| CPA | `ctsp:docs/COUNTING_PRIOR_ART.md` |
| CPD | `mem:carm-plateau-is-the-denominator.md` |
| CSB | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` |
| CV9 | `sn:results/eval_gate/closure/cv_v9/cv_v9.json` |
| D813 | `mem:dataset813-image-links-are-container-paths.md` |
| DBC | `mem:detection-is-the-binding-constraint.md` |
| DD23 | `mem:data-directives-2026-09-23.md` |
| DDP | `ssn:data_platform/dedup/DEDUP_PLAN.md` |
| DFC | `mem:deepfluoro-convention.md` |
| DFF | `ssn:docs/DEEPFLUORO_FORMATION.md` |
| DFL | `mem:drr-to-fluoro-levers.md` |
| DRS | `mem:drr-row-spacing-defect.md` |
| FCM | `mem:feasibility-claims-measured.md` |
| FCX | `ssn:HANDOFF/context/feasibility-claims-measured.md` |
| FFB | `mem:film-fluoro-boundary-not-transferable.md` |
| FGS | `mem:fluorogen-synthetic.md` |
| FNC | `sn:results/coverage/film_ncurve/ablation/READ.md`; `mem:film-ncurve-ablation-result.md` |
| FOURTH | `ssn:docs/research_datasets_fourth_pass_verified_2026-09-22.json` |
| FP | `ssn:docs/FLAGSHIP_PLAN.md` |
| FPL | `mem:fluorocap-prototype-and-lstv-arm.md` |
| GRAD | `sn:results/learning/gradient_regression.json` |
| HAI | `ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` |
| HANH | `sn:lit/ct_lstv_classifier/sources/hanhivaara2024_castellvi_CR_CT_MRI_accepted_manuscript.txt` |
| HFM | `mem:hf-mirror-is-v10.md` |
| HPH | `ssn:docs/HANDOFF_PHYSICS.md` |
| IAF | `mem:identity-audit-findings.md` |
| J3NS | `sn:results/reader_e/J3_NOT_SUBMITTED.md` |
| KDN | `mem:k-devices-one-network.md` |
| L6C | `sn:results/learning/l6_confound.json` |
| L6SC | `mem:l6-sample-count-and-counting-decoder.md` |
| LCC | `sn:LEVELCHECK_CLAIM.md` |
| LCM | `sn:LEVELCHECK_MODEL.md` |
| LDL | `mem:lstv-data-landscape.md` |
| LEARN | `sn:results/learning/LEARNING.md` |
| LFR | `mem:learned-formation-refuted-calibrate-instead.md` |
| LG | `ctsp:morphometrics/level_gradients.csv` |
| LID13 | `mem:level-id-2d-results-2026-09-13.md` |
| LJ | `ctsp:docs/LAB_JOURNAL.md` |
| LM | `ctsp:docs/LEVEL_MORPHOMETRY.md` |
| LMBC | `mem:level-model-bank-coverage.md` |
| LS | `ssn:HANDOFF/LITERATURE_STATE.md`, section given |
| LSB | `ssn:docs/LSTV_BENCHMARK.md` |
| LTDG | `mem:lstv-tltv-detection-goal.md` |
| MAN | `ssn:data_platform/DATA_MANIFEST.md`, the card named |
| MAPI | `ssn:docs/ruleclass/MORPH_API.md` |
| MDD | `ssn:tools/make_drr_dataset.py` |
| MDF | `mem:morphology-deformation-feasibility.md` |
| MLS | `mem:mixed-length-head-and-sota.md` |
| MORPH | `ssn:docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` |
| MP | `ssn:data_platform/MIGRATION_PLAN.md` |
| MPDA | `ctsp:paper/mpda/main.tex` |
| N2 | `ssn:HANDOFF/literature_state/dataset_landscape_by_task.md` |
| N4 | `ssn:HANDOFF/literature_state/power.md` |
| NDI | `mem:nhanes-double-inclusion.md` |
| NIPS | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.tex` |
| NPR | `ctsp:docs/NEXT_PAPER_REFERENCES.md` |
| NUM:n | `sn:NUMBERS.md`, line n |
| OCR | `mem:ostk-canal-closing-regression.md` |
| OM2 | `ostk:ostk/metrics2d.py` |
| OVE | `ctsp:docs/OSTK_VS_EXTRACTION.md` |
| P1S | `sn:PAPER1_SCOPE.md` |
| PAIRED | `ssn:docs/research_paired_ct_projection_verified_2026-09-21.json` |
| PAN | `mem:panjabi-1991-page-892.md`; `<laptop folder Desktop/PANJABI_1991_FULL.pdf; not a dependency>` |
| PAS | `ssn:docs/PRIOR_ART_SYNTHETIC_AND_SELF_TRAINING.md` |
| PIR | `mem:ct-volumes-are-pir-not-ras.md` |
| PIS | `ssn:docs/PATIENT_IDENTITY_SPEC.md` |
| PJ | `sn:results/power/power.json` |
| PLAN | `ssn:docs/CT_LSTV_CLASSIFIER_PLAN.md` |
| PLDA | `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` |
| POS | `sn:lit/ct_lstv_classifier/positives_census.md` |
| PPD | `mem:polypose-decision.md` |
| PRER | `ssn:docs/ruleclass/PREREG_rules.md` |
| PREV | `sn:lit/ct_lstv_classifier/lit_prevalence_and_definitions.md` |
| PS24 | `mem:paper-split-2026-09-24.md` |
| PSF | `mem:prone-supine-flexibility-future.md` |
| RAF | `mem:rigor-audit-findings.md` |
| RC22 | `mem:anomaly-rule-rc22-evaluated.md` |
| RDO | `ssn:tools/render_drr_overlay.py` |
| REPRO | `ctsp:paper/mpda/REPRODUCE.md` |
| RES | `sn:sections/results.tex` |
| REVT | `ssn:docs/REVIEW_TRANSITIONAL.md` |
| RF18 | `ssn:docs/research_registration_free_2026-09-18.json` |
| RF22 | `ssn:docs/research_registration_free_search_2026-09-22.md` |
| RFP | `mem:registration-free-prior-art.md` |
| RHR | `mem:recurrent-head-restored-2026-09-16.md` |
| RLC | `ctsp:docs/RELEASE_CHECKLIST.md` |
| RPD | `ssn:tools/render_physics_drr.py` |
| RR17 | `mem:remedies-refuted-2026-09-17.md` |
| RS2 | `sn:REVIEW2_STATS.md` |
| RSP | `ssn:research_notes/spine synthesis prior art/registration.md` |
| SBM | `ctsp:docs/SPINEPS_BENCHMARK.md` |
| SEP | `ctsp:scripts/test_morphometric_separability.py` |
| SM | `ctsp:morphometrics/surgical_morphometrics.csv` |
| SPE | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` |
| SPH | `mem:selective-prediction-the-honest-99.md` |
| SPID | `mem:spineps-ids-can-be-scrambled.md` |
| SPLT | `sn:results/rare_class/split_plan.md` |
| SRE | `mem:synthetic-real-ratio-evidence.md` |
| SRM | `ssn:docs/research_sim_real_mixing_verified_2026-09-21.json` |
| STC | `mem:stc-does-not-transfer.md` |
| STUMP | `ssn:docs/ruleclass/STUMP_RULE.md` |
| SWP | `mem:sweep-map-replaces-registration.md` |
| SXS | `ssn:docs/data_requests/SX-Stitch_request.md` |
| SYN | `ssn:reports/Synthetic real ratio X-ray detectors.md` |
| T3 | `sn:tables/tab3_naming.md` |
| TAB3 | `sn:tables/tab3_naming.md`, the same file as T3 |
| TAB2 | `sn:tables/tab4_transitional.md` |
| TIERS | `ssn:docs/ruleclass/TIERS.md` |
| TLJ | `sn:lit/ct_lstv_classifier/lit_tl_junction_and_enumeration.md` |
| TM | `ctsp:morphometrics/transition_morphometrics.csv` |
| TMT | `mem:two-mechanisms-thesis.md` |
| TSB | `mem:ts-bench-inside-v9-bank.md` |
| TSS | `mem:ts-sacrum-excludes-s1.md` |
| VF8 | `mem:vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` |
| VFT | `mem:versefusion-t13-flag-wrong.md` |
| XDU | `ssn:docs/XRAY_DATASET_USAGE.md` |


Glossary, twelve lines for a first-week reader. Fuller definitions are in `GLOSSARY.md`.

| term | meaning and where it is defined |
|---|---|
| G3 split | the person-disjoint split of 2026-09-23, ordinary 80/10/10 and transitional 50/10/40; `GLOSSARY.md` "G3 split"; SPLT |
| G0 to G7 | the gates of the flagship programme, from data complete to manuscript; `GLOSSARY.md` "G0-G7"; FP lines 57 to 64 |
| paper 1 and paper 2 | paper 1 is SchwingNet's five-figure manuscript and scores no G3 test transitional person; paper 2 is the LevelCheck and surgeon comparison; PS24; P1S |
| "H1 seen" | the entry paper 2's ledger must carry before any G3 test transitional person is scored; PS24 lines 24 to 26 state the rule for H6 as "H6 seen", and the H1 wording is this document's counterpart, not on disk |
| the ledger | `sn:CLAIMS_LEDGER.md`, where every quoted claim carries its file and its gate verdict; CL |
| eval_gate | `ssn:tools/eval_gate.py`, which refuses to score a seen or unresolved item and stamps every result; ACC section 5.3; `GLOSSARY.md` "the gate" |
| alphabet | the set of level names a frame may use, ordinary, L6, T13 or both, chosen from the classifier posteriors and the count; ACP; `GLOSSARY.md` "coupling, alphabet, stop signal" |
| State C | the label-defined unanchored condition: no labelled anchor such as the sacrum in the window, so no count is possible; FCM line 18 |
| physics_rare | the render bank of 1,482 physics-based cone-beam renders of 34 CTSP ids and 47 VerSe series; MAN physics_rare line 2643; `GLOSSARY.md` "*_drr render banks" |
| Dataset803 | the nnU-Net pelvic pseudolabeller, sacrum and hips, used to put a sacrum label on CTs that have none; `GLOSSARY.md` "Dataset803 / 810 / 813 / 815" |
| the review tree | per-flagged-CT case folders for the two-stage human read; REVT; `GLOSSARY.md` "review tree" |
| reqp, RTK | `reqp` is the preemptible CPU partition on the grid, used with `--qos=requeue`, CLAUDE "Grid"; RTK is the cone-beam projection geometry COBRA2026 ships with every projection, PRER line 20 |

