# Protocol 1 — eProtocol draft (WSU IRB form order)

**Working title:** Automated identification of vertebral level and detection of injury on spine and pelvis imaging at the Detroit Medical Center: a retrospective imaging and records study

**Status:** draft for the PI, 15 September 2026. Written in the order of the WSU eProtocol IRB Form as exported for IRB-21-10-4123 (Vaidya, *Improving Outcome in Orthopaedics Trauma Care*), so each block below pastes into the matching eProtocol page. Bracketed items need the PI's decision. This file lives under `proposals/` (gitignored) and is not the public summary; the public summary is `IRB_two_protocols_summary.pdf`.

**Relationship to the two-protocol plan:** this is Protocol 1 (retrospective, Exempt Category 4, waiver of consent and of HIPAA authorization) from `IRB_two_protocols_summary.pdf`, with Aim 2 rewritten so that the intraoperative fluoroscopy–CT pairs are an explicit, named data source and the registration-based reference standard is described. Protocol 2 (prospective silent evaluation) is unchanged and is submitted alongside.

---

## Personnel Information

| Role | Name | Notes |
|---|---|---|
| Principal Investigator | [Gregory Schwing, MD, PhD — PGY-1 Surgery, DMC] | eProtocol requires a faculty sponsor/mentor for a resident PI: [Dr Montie / Dr Vaidya — confirm] |
| Faculty Sponsor/Mentor | [name, department] | signs the Obligations page |
| Co-Investigator (Neurosurgery) | [Dr To] | operating surgeon whose intraoperative fluoroscopy is uploaded to PACS; provides the surgeon-stated level from operative notes; adjudicates level disagreements |
| Co-Investigator (Radiology) | [name] | reference reads; adjudication of level and fracture; LSTV numbering convention |
| Co-Investigator (Orthopaedic Trauma) | [Dr Vaidya, if agreed] | trauma registry linkage (Aim 4) |
| Key personnel — study staff | [named residents/students who will touch identifiable data] | CITI Human Subjects + HIPAA Research current |
| Department Chair/Dean sign-off | [Chair, Department of Surgery] | |

Everyone listed as touching identifiable data must be on the DMC Research Compliance application with the same names.

## Study Location

Detroit Medical Center (Detroit Receiving Hospital, Harper University Hospital, Sinai-Grace, Hutzel, Children's Hospital of Michigan excluded for now) for record access and de-identification; Wayne State University High Performance Computing (the WSU research cluster, `grid.wayne.edu`) for analysis of de-identified data only. No VAMC, no international site, no internet-based recruitment.

## Funding

[Unfunded / departmental. If NIH or other support is added later, update.] No sponsor.

## Study Details

- IRB of record: WSU IRB
- Study type: Medical
- Review type: **Exempt** (Category 4, with limited IRB review for privacy and confidentiality because identifiable health information is accessed)

## Exempt Paragraph(s)

- Item A (more than minimal risk): **No**
- Item B (FDA-regulated drug/device clinical investigation): **No** — the software is used on existing images for research; no result returns to the record or to care
- Item C (prisoners): **No**
- Item D (risks): **Breach of confidentiality** (identifiers are used once for linkage and a coded key is retained during the study)
- Category 4: check **(2)** data recorded such that identity cannot be readily ascertained and no contact or re-identification, and **(3)** data includes identifiable health information protected under HIPAA
- 4a: **N** (HIPAA applies; see the HIPAA waiver page) · 4a(i) contact or re-identification: **N** · 4b data that is not pre-existing: **N** (records and images from 1 January 2006 to the IRB approval date; nothing collected prospectively) · 4c biospecimens: **N**

## Summary & Purpose

**1. Summary (lay language).** Surgeons and radiologists locate a vertebra by counting from a landmark. About one person in six has a spine with a different count, an extra or missing rib, or a vertebra fused to the pelvis, and counting goes wrong; operating on the wrong level is the result the field worries about most, and the thoracic spine and the lumbosacral junction are where it happens. Our group has built, from public CT scans, a program that outlines every bone of the spine and pelvis and names each vertebra from its own shape rather than by counting. This study uses images and records that already exist at DMC to (1) check that program on DMC patients, (2) build a reference standard for the intraoperative x-ray images surgeons use to confirm the level, by matching each intraoperative image to the same patient's CT with an image-registration algorithm, and use that reference to train and test a program that names the level from the intraoperative image alone, (3) train and test fracture detection on trauma spine and pelvis imaging, and (4) relate the imaging findings to treatment and outcome recorded in the trauma registry. No patient is contacted, treated differently, or has anything returned to the medical record.

**2a. Purpose and hypotheses.**

The purpose is to develop and evaluate computer methods that name vertebral levels and detect injury on the spine and pelvis images DMC patients already receive, with an explicit focus on the patients whose anatomy makes counting unreliable.

- H1. A vertebra-naming program trained on public CT identifies each lumbar and lower thoracic vertebra on DMC CT scans in agreement with the radiology report and with a radiologist's read, and does so in patients with transitional anatomy (sixth lumbar vertebra, sacralized L5, lumbarized S1, thirteenth thoracic vertebra, hypoplastic or absent twelfth rib) as well as in patients with usual anatomy.
- H2. Intraoperative fluoroscopic images can be labelled with vertebral levels by registering them to the same patient's pre- or post-operative CT (three-dimensional to two-dimensional registration), and those labels agree with the level recorded in the operative note and with the CT-verified numbering in at least 98% of vertebrae.
- H3. A program trained on those registration-derived labels identifies the vertebral level on an intraoperative fluoroscopic image **without** a CT, and its per-vertebra accuracy against the registration reference is measurable with a two-sided 95% confidence interval narrower than ±1 percentage point in each pre-specified stratum (usual anatomy, transitional anatomy, instrumented, non-instrumented).
- H4. Fracture detection on trauma spine and pelvis radiographs and CT reaches sensitivity and specificity against the CT-confirmed radiology read that can be compared with the initial clinical read.
- H5. Among trauma patients, imaging findings identified by the programs are associated with the treatment given and the recorded outcome.

**2b. What the investigators hope to learn.** Whether naming a vertebra from its shape survives contact with a real, largely underinsured urban trauma population and its imaging; how often an intraoperative image alone would have led to a wrong level, and in which patients; whether a registration-based reference standard is a practical way to label intraoperative images at scale; and whether fracture detection and level naming change enough management to justify the prospective silent evaluation in Protocol 2.

## Background, Rationale, Data Analysis and Procedures

### Section A

**a(i) Current knowledge.** Wrong-level spine surgery occurred in 0.12% of 34,544 consecutive cases in a recent single-system series, in 0.42% of thoracic cases, and every event was at L4–5 or L5–S1, with image misinterpretation named in 18.8%. Lumbosacral transitional vertebrae have a pooled prevalence of 15.3% across 83 studies; numerical variants (23 or 25 presacral segments) occur in 7.7% of whole-spine MRIs and cannot be seen on a limited field of view; outpatient level counts were wrong in 54% of patients with transitional anatomy in a surgical series; on radiographs, readers agree on the transitional type only at κ 0.16–0.32. The one validated method for labelling intraoperative radiographs, LevelCheck (Johns Hopkins), registers the patient's preoperative CT to the intraoperative image and placed labels correctly on 398 of 398 intraoperative radiographs from 178 patients; it requires a CT and is not publicly available, but the registration components it relies on are (xReg; DiffDRR/DiffPose). No public dataset of intraoperative spine fluoroscopy with vertebra-level labels exists. Our group has released a public CT dataset of 802 abdominopelvic scans with every vertebra, rib, sacrum and pelvis labelled, including 18 six-lumbar spines and 33 graded transitional cases (Zenodo 10.5281/zenodo.22642578; WSU determination 2026-269, Not Human Participant Research), and a vertebra-naming model trained on it. [Insert full citations; see the reference list at the end.]

**a(ii) Rationale.** Level naming from local shape has only been tested on public CT and on rendered images; whether it works on real intraoperative fluoroscopy, on instrumented spines, and in patients with transitional anatomy cannot be learned from public data because no such labelled data exist. Registration to the patient's own CT is the one route that produces exact labels for real intraoperative images without a human counting on the image. DMC archives intraoperative fluoroscopy to PACS for at least one neurosurgical service, and most spine-surgery patients have a pre- or post-operative CT, so the pairs exist.

**a(iii) Rationale for the participant population.** DMC's spine and trauma population is under-represented in public datasets and carries a heavy burden of high-energy injury and of prior surgery; it is the population in which the methods have to work. Adults only in this protocol.

**a(iv) Inclusion criteria.** Any patient aged 18 years or older with at least one of the following at a DMC facility between 1 January 2006 and the date of IRB approval: a CT that includes any part of the spine or pelvis; a radiograph of the spine or pelvis; an MRI of the spine; an intraoperative fluoroscopic image series of the spine or pelvis archived in PACS or in the C-arm or navigation archive; or an entry in the DMC trauma registry with a spine or pelvic injury.

**a(v) Exclusion criteria.** Age under 18 at the time of imaging; imaging that contains no spine or pelvis; studies whose images cannot be de-identified (burned-in identifiers that cannot be removed) are excluded from transfer but counted.

**b. Statistical methods.** Agreement of level names with the reference (radiology report and radiologist read for CT; registration-derived labels for intraoperative images; CT-verified count for radiographs) is reported as per-vertebra exact accuracy with Wilson 95% intervals, within-one-level rate, and the full confusion matrix, stratified by anatomy (usual; transitional with an unchanged count; transitional with a changed count), region (lumbosacral, thoracolumbar, thoracic, cervical), and instrumentation. Registration quality is reported as projected-centroid error and as the rate of level labels changed by adjudication. Fracture detection is reported as sensitivity, specificity and AUC against the CT-confirmed read, with the initial clinical read as comparator. Disagreements between the programs and the reference are adjudicated by a radiologist and a surgeon blinded to the program's output. Associations with treatment and outcome (Aim 4) use logistic regression adjusted for age, sex, injury severity and mechanism. Analyses are pre-specified in a statistical analysis plan filed before the first label is produced.

**c. Sample size justification.** To bound a per-vertebra accuracy of 99% with a 95% interval of ±0.5 percentage points requires about 1,500 verified vertebrae in each primary stratum; four primary strata (usual and transitional anatomy, each instrumented and not) give a target of 6,000 verified vertebrae on intraoperative images, i.e. roughly 1,500–2,500 intraoperative images from 800–1,500 patients, since about 12.9% of lumbar surgical patients have transitional anatomy and enrichment for those cases is deliberate. Trauma fracture detection at an expected sensitivity of 90% ± 3 points needs about 400 fractured studies. Because transitional anatomy and archived intraoperative imaging are both minorities, the records request is broad: [40,000 imaging studies from an estimated 25,000 patients — the same number must appear on the WSU form, this document and the DMC application; confirm with a PACS count before submission].

**d.** N/A (retrospective records study). **e.** No follow-up. **f.** N/A.

### Section B — Procedures

**a.** Interaction, intervention, or data collection from participants: **N**.

**b. Chronological description.**
1. DMC Radiology informatics and the neurosurgical service identify eligible studies by modality, body part and date (PACS query), and the trauma registry office identifies registry entries meeting the criteria.
2. Within the DMC secure environment (Citrix), the study team pulls the DICOM studies (CT, radiographs, MRI, and intraoperative fluoroscopy as XA, RF or Secondary Capture objects, including C-arm and navigation-system archives where they exist), the radiology reports, the operative notes, and the registry and EMR variables on the data collection sheet.
3. Medical record number, financial identification number and accession number are used once to link images to reports, notes and registry rows. Each patient receives a study code; each study a study code; the key linking codes to identifiers is kept on DMC Citrix, accessible only to the PI and one designated key holder, and nowhere else.
4. Images are de-identified inside DMC before transfer: DICOM headers are stripped to the DICOM PS3.15 basic de-identification profile with dates shifted per patient and ages retained in years (capped at 89); pixel data are screened for burned-in text with an optical-character-recognition detector on every frame, flagged frames are masked, and 100% of frames are inspected by a study team member before release; frames whose text cannot be masked without destroying the image are excluded and counted. Reports and notes are de-identified with a validated clinical text de-identification tool followed by manual review of a 10% sample.
5. De-identified images and text are transferred by encrypted transfer (SFTP over the WSU VPN, or an encrypted drive carried by the PI) to the WSU research cluster under a project directory readable only by the named study staff.
6. Intraoperative fluoroscopic images are registered to the same patient's pre- or post-operative CT with a three-dimensional to two-dimensional registration algorithm; the CT's vertebra labels are projected into the image to give the reference level of every visible vertebra; registrations that fail their quality gate are flagged for reader labelling. Operative notes supply the surgeon-stated level for comparison.
7. Programs for level naming on CT, level naming on radiographs and intraoperative images, and fracture detection are trained and tested on the de-identified data, with patient-level splits fixed before training.
8. A radiologist and a surgeon adjudicate a stratified sample of level labels and every disagreement between program and reference, blinded to the program's output.
9. Statistical analysis as in Section A(b). Aim 4 links imaging findings to registry treatment and outcome variables through the study codes only.

**c. Who, where, when.** Steps 1–4 by the PI and named DMC study staff inside DMC systems; step 5 by the PI; steps 6–9 by the PI and named WSU study staff on the WSU research cluster, over the [three]-year study period.

**d. Participant time commitment.** None.

**e. Non-research procedures.** None; all imaging and records were obtained for clinical care.

### Section C — Data collection methods

Data collection sheet (attached) lists every variable: demographics (age in years, sex, race/ethnicity as recorded, insurance class); imaging (modality, body part, date shifted, manufacturer and model, DICOM object type, matrix, bit depth, pixel spacing, view/projection, series description); radiology report text (de-identified); operative note fields (procedure, levels stated, approach, implants, intraoperative imaging used); trauma registry fields (mechanism, ISS, AIS by region, diagnoses, procedures, complications, length of stay, disposition, mortality, follow-up); derived labels (vertebra names, fracture flags, registration quality). Direct identifiers used only for linkage: MRN, FIN, accession number; never transferred.

## Participant Population

- Section A: adults **18–99**; no participants directly solicited, consented or completing study visits (records only); multi-site: **N** (single health system, several hospitals); records/charts used: **[40,000 imaging studies; ~25,000 patients — one number, everywhere]**.
- Section B: pregnant women are not excluded (records); no selection by race, ethnicity or sex; no vulnerable populations targeted; children excluded (rationale: pediatric spine anatomy and imaging differ; a separate protocol will follow if warranted); prisoners: records of incarcerated patients are not identified as such and are not targeted; if a record is discovered to belong to a prisoner it is handled under WSU policy [confirm wording with the IRB office].
- Sections C–E: no students, employees or non-English-speaking participants are recruited (records only; a DMC employee's clinical record could be among the records, which is handled by the confidentiality procedures).

## Recruitment Process, Participant Compensation and Costs

No recruitment, compensation or cost; records only.

## Benefits

No direct benefit to the individuals whose records are used. Potential benefit to future patients from level-confirmation and fracture-detection methods evaluated on this population, and educational benefit from de-identified teaching material.

## Procedures to Maintain Confidentiality

- Data type: **Coded** (the key held on DMC Citrix by the PI and one designated key holder; the coded dataset kept separately).
- a) Shared outside the research team: **Y** — de-identified images and derived labels may be shared with other academic institutions under a restricted data use agreement, and trained model weights may be released, in each case only after a separate WSU determination (as for 2026-269) and never with identifiers or the key. Coded data leave DMC only in de-identified form; nothing is shared through consumer cloud services.
- b) Data types: Protected Health Information (during linkage and de-identification inside DMC); Secondary data analysis (imaging, reports, notes, registry); Identifiable data: MRN, FIN, accession number, names on burned-in text, used only to link and to remove.
- c) Privacy: no contact with patients; the study team accesses records only through DMC's authorized research access path; the number of people who see identifiable data is limited to the named DMC study staff.
- d) Confidentiality: identifiers are replaced by study codes inside DMC; the key is stored on DMC Citrix with access logged; de-identified data are stored on the WSU research cluster in a project directory with permissions limited to named study staff, transferred only by encrypted means; laptops and portable drives used for transfer are full-disk encrypted; no identifiable data are ever placed on personal devices, email, or unencrypted storage; publications and releases contain no identifiers and no free text from records; small-cell counts (n < 10) are suppressed in tables.
- e) Retention and destruction: the key is destroyed [at study closure or 7 years after IRB approval, whichever is later, per WSU records policy — confirm]; de-identified data are retained for research reproducibility.
- f) Personnel with access: listed by name in Personnel Information; all with current CITI Human Subjects and HIPAA modules.

## Consent Information

Waiver of consent is requested under 45 CFR 46.116(f): the research is minimal risk (records and images only); it could not practicably be carried out without the waiver (tens of thousands of records over twenty years; many patients are deceased, transient or unreachable, and contacting trauma patients about old records would itself be a burden); it could not practicably be carried out without identifiable information because linkage of images to reports, notes and registry requires the identifiers once; the waiver will not adversely affect rights and welfare (no contact, no change to care, coded data, no return of results); and, where appropriate, no additional pertinent information will be provided after participation because there is none.

## HIPAA — Waiver of Authorization

1. Waiver requested: **Y** — to obtain data for a retrospective records and imaging study (and to screen records for eligibility).
2. Minimal risk to privacy: identifiers are used once, inside DMC, for linkage; a coded key is kept on DMC Citrix with logged access by the PI and one key holder; images are de-identified in header and pixel data with 100% inspection before leaving DMC; reports and notes are de-identified by tool plus manual sampling; de-identified data are stored on an access-controlled WSU research system.
3. Impracticable without the waiver: retrospective study of [40,000] studies from 2006 onward; authorization from each patient is not feasible.
4. Impracticable without PHI: images, reports, operative notes and registry rows must be linked per patient to build the reference standard (a fluoroscopic image is only labelled by the same patient's CT), and dates are needed to order studies within an episode of care.
5. Protection from improper use: as in Confidentiality (c)–(f); minimum necessary data elements on the data collection sheet; PHI never leaves DMC.
6. Destruction of identifiers: the key is destroyed [at study closure / 7 years — confirm]; identifiers are removed from all data at step 4 of the procedures; audit logs are retained as required.
7. PHI obtained under the waiver will not be reused or disclosed outside the research team except as required by law, for authorized oversight, or for other research for which use or disclosure is permitted under the Privacy Rule: **Y**.

## Attachments (to prepare)

1. Data collection sheet (variables, sources, minimum-necessary justification).
2. De-identification standard operating procedure (DICOM header profile, pixel OCR screening, 100% visual inspection, text de-identification and 10% audit).
3. DMC Research Compliance / Office of Research application and DMC IT data-transfer approval.
4. Letter of support from the Neurosurgery service (Dr To) confirming intraoperative fluoroscopy is archived to PACS and agreeing to co-investigator role; letter from Radiology (PACS export path; whether OR C-arm and navigation archives are separate from PACS).
5. WSU determination 2026-269 (Not Human Participant Research, public data) for context.
6. Statistical analysis plan (pre-specified strata, endpoints, sample sizes).
7. CITI certificates; COI disclosures for every investigator.
8. Reference list.

---

## Notes to the PI (not part of the eProtocol)

**The design question you asked — CTs and fluoroscopy together?** Yes, and it is the point of the protocol. Request, per patient: every intraoperative fluoroscopic image (XA, RF and Secondary Capture objects; ask Radiology whether OR C-arm saves and navigation screenshots land in PACS or in a separate archive — at one university centre 90 of 190 consecutive cases had intraoperative images only on film or outside PACS), the pre-operative and any post-operative CT, the radiology reports, the operative note (the surgeon's stated level is the clinical comparator), and whole-spine MRI reports when present (they carry the numbering convention). The registration-labelled pairs are the reference standard; the registration-free model is the index test; the surgeon's intraoperative level call is the clinical baseline. Also request fluoroscopy from patients **without** a CT: they cannot enter the reference set, but they are the honest test of the registration-free model on cases nobody could register. Ask for post-instrumentation captures explicitly (every fusion case has them) so hardware arrives labelled; ask for corpectomy cases by CPT code so that stratum is countable.

**Numbers.** Write one number for records on the WSU form, this document and the DMC application. Before you pick it, get a PACS count for: CT with spine/pelvis 2006–present; spine radiographs; intraoperative fluoroscopy series (XA/RF/SC) by service and by year; and how many of those patients have a CT within 6 months. The count for Dr To's cases alone tells you the Tier 0 yield per year.

**Faculty sponsor and roles.** eProtocol needs a faculty PI or a faculty sponsor for a resident. Dr To as co-I for neurosurgery; a radiologist co-I for adjudication; Dr Vaidya as co-I if the trauma registry (Aim 4) stays in this protocol. Everyone on the DMC application by the same names.

**Disclosure that belongs in the eProtocol and nowhere public.** Per `IRB_ADDENDUM.md` (Edit 1), add to the Purpose and Confidentiality sections of the eProtocol only:

> Data collected under this protocol may be used for the development, training, testing and validation of computational methods and software, including software that may subsequently be commercialised or submitted for regulatory clearance. De-identified images and derived labels may be shared under a restricted data use agreement, and model weights may be released, each after a Wayne State University determination. Any transfer of data or derived artifacts to a commercial entity will be governed by a separate data use agreement executed with the covered entity, and is not authorised by this protocol alone.

and make the COI disclosure accurate on the date it is signed. The DUA with DMC/Tenet legal is a parallel track (Edit 2), not an IRB item.

**De-identification is the part reviewers will probe.** The header flag for burned-in text is optional in DICOM and absent on many C-arm objects, and the shipped CTP pixel scripts have no C-arm signatures; say plainly that every frame is OCR-screened and every frame is looked at. Budget the time: at 1–2 s per frame for the OCR pass plus a human look, 5,000 frames is a few days.

**What to cut if the IRB pushes back on breadth.** Aim 4 (registry linkage) is separable; Aims 1–3 are imaging and reports only and are the core.

## References (to be completed)

- LevelCheck utility study, Spine 2016; clinical translation, Ann Biomed Eng 2018.
- Wrong-level surgery incidence in 34,544 cases (2025/2026 series); thoracic rate.
- LSTV prevalence meta-analysis (83 studies, 15.3%); numerical variants on whole-spine MRI (7.7%); outpatient count errors in LSTV surgical patients (54%); radiographic Castellvi typing κ 0.16–0.32.
- CTSpinoPelvic1K dataset descriptor (Zenodo 10.5281/zenodo.22642578) and WSU determination 2026-269.
- DICOM PS3.15 de-identification profiles; JIIM 2024 OCR-based burned-in text detection covering XA/RF.
- xReg (Grupp 2020); DiffDRR/DiffPose (Gopalakrishnan 2024).
