# regulatory/: the route to hospital radiographs for this project

This folder holds the drafts of **amendment 47 to IRB-21-10-4123** ("Improving Outcome in
Orthopaedics Trauma Care", the Detroit Medical Center trauma registry protocol; PI of record named in
the drafts), written in September 2026 as the students' route to de-identified DMC thoracolumbar and
lumbar spine radiographs with their CT and radiology reports. Both drafts are redacted copies
(`MANIFEST_LOCAL.md` records the source and the redaction). The amendment was drafted; whether it
was submitted is **not recorded** (`TODO.md` step 4).

| file | what |
|---|---|
| `irb_amendment_47_eprotocol_checklist.md` | the eProtocol text and checklist: how the protocol has amended before (46 approved amendments since June 2022; amendment 47 created 2026-09-02, expedited, PI-originated, key-personnel addition), the form selections, the lay summary, the section-by-section replacement text, what each added person must complete (CITI: Biomedical Investigators; HIPS for Students and Instructors; Biomedical Responsible Conduct of Research; the Obligations page; COI), and the open items |
| `irb_amendment_47_fracture_and_level_proposal.md` | the same amendment in eProtocol section order with the scientific background (fracture detection is commercial and FDA-cleared; naming the vertebra reliably is not; lumbosacral transitional vertebrae in 4-30 % of people; wrong-level surgery about once per 3,100 procedures), the statistical methods, the personnel additions and seven references |

## What the amendment does and does not do

- Extends the approved retrospective chart review to the imaging already obtained during care:
  thoracolumbar and lumbar radiographs (AP and lateral), spine CT and the radiology reports, for
  patients already identified from the trauma registry.
- De-identification inside DMC (DICOM header identifiers removed, burned-in text checked and
  removed); de-identified images stored and analysed on the Wayne State University High Performance
  Computing cluster; the master list stays on DMC Citrix; no result returns to the medical record or
  to treating clinicians; no change to consent, risk or population, so it stays expedited.
- Raises the approved record count from 2,000 to **[N]**, a number never filled in; it must be the
  same on the eProtocol, the DMC application and the protocol document (the 2022 CRO review flagged a
  mismatch).
- Reports, for the imaging analysis: sensitivity and specificity of automated fracture detection
  against the report and the CT; agreement of automated vertebral-level identification with CT,
  **reported separately for patients with and without transitional lumbosacral anatomy**; agreement
  of automated spinopelvic measurements with manual measurement against published error bands.

## What is withheld in these copies

Twelve student names, two radiology residents' names, the IRB coordinator's name (her role is kept)
and two e-mail addresses. The PI of record and Greg's name are kept because the route depends on
them. Whether the student lead's name (a published co-author) appears in folder text is Greg's
decision (`_plan/PLAN.md` section 5). The unredacted roster is in the source draft recorded in
`MANIFEST_LOCAL.md` and in `11_students_grid_access`.

## How this relates to the other determinations

- The programme's umbrella determination, HPR 2026-269 (the "Not HPR" determination of 2026-09-02),
  covers only public, de-identified data downloadable without an agreement
  (`docs/handoff/README.md` section 5 rule 9). Its letter is copied into `01_carm_level_detection/regulatory/`,
  which owns the hospital-testing plan; this folder's route is an **amendment to an existing
  protocol**, not a determination.
- The OSC public-datasets determination and the VinDr-SpineXR determination (number not recorded,
  `docs/handoff/OPEN_QUESTIONS.md` A5) are likewise folder 01's and folder 10's records.
- No BUU-LSPINE or VinDr image may travel under this amendment; it concerns DMC images only.
