# What the abstracts changed in the screen

Two passes of the same criteria over the same 11980 records. The first had a title and a publication type; the second added the abstract wherever one could be fetched (`review/abstracts.jsonl`). Neither ledger overwrites the other: the first is `screening_titleonly.jsonl`, the second is `screening.jsonl`. Produced by `tools/review_compare.py`.

## Movement

| | n |
|---|---:|
| records screened in both passes | 11980 |
| of those, carrying an abstract in the second pass | 9291 |
| records that changed decision or reason | 5767 (48.14%) |
| included, title-only pass | 665 |
| included, title-and-abstract pass | 1933 |
| change in the included count | +1268 |

### Direction

| move | n |
|---|---:|
| same decision, reason changed | 4493 |
| exclude -> include | 1271 |
| include -> exclude | 3 |

### Reason to reason

| from | to | n |
|---|---|---:|
| `E_NO_FULLTEXT` | `E_NO_POPULATION` | 1670 |
| `E_NO_FULLTEXT` | `E_NO_CONCEPT` | 1316 |
| `E_NOT_SPINE` | `E_NO_POPULATION` | 1081 |
| `E_NO_FULLTEXT` | `INCLUDED` | 939 |
| `E_NOT_SPINE` | `E_NO_CONCEPT` | 188 |
| `E_NO_POPULATION` | `INCLUDED` | 171 |
| `E_NOT_SPINE` | `INCLUDED` | 122 |
| `E_NO_POPULATION` | `E_NO_CONCEPT` | 85 |
| `E_NOT_SPINE` | `E_ANIMAL_CADAVER` | 44 |
| `E_ANIMAL_CADAVER` | `E_NO_POPULATION` | 34 |
| `E_NO_FULLTEXT` | `E_ANIMAL_CADAVER` | 32 |
| `E_ANIMAL_CADAVER` | `INCLUDED` | 26 |
| `E_NO_POPULATION` | `E_ANIMAL_CADAVER` | 19 |
| `E_NO_CONCEPT` | `INCLUDED` | 10 |
| `E_NOT_SPINE` | `E_NON_SPINE_WRONG_SITE` | 8 |
| `E_NOT_SPINE` | `E_EDITORIAL_NO_DATA` | 7 |
| `E_EDITORIAL_NO_DATA` | `E_NO_POPULATION` | 4 |
| `E_NO_POPULATION` | `E_TECHNICAL_NO_LEVEL_CLAIM` | 2 |
| `INCLUDED` | `E_NON_SPINE_WRONG_SITE` | 2 |
| `E_EDITORIAL_NO_DATA` | `INCLUDED` | 2 |
| `E_NO_POPULATION` | `E_NON_SPINE_WRONG_SITE` | 1 |
| `INCLUDED` | `E_TECHNICAL_NO_LEVEL_CLAIM` | 1 |
| `E_NON_SPINE_WRONG_SITE` | `INCLUDED` | 1 |
| `E_NON_SPINE_WRONG_SITE` | `E_NO_POPULATION` | 1 |
| `E_EDITORIAL_NO_DATA` | `E_NO_CONCEPT` | 1 |

## What a changed decision looks like

Up to 4 records per kind of move, drawn with a fixed seed. Every one of the 5767 changed records is in `screen_changes.csv` with its evidence.

### `E_NO_FULLTEXT -> E_NO_POPULATION` (1670 records)

- **s2:5166d6ec35e18d63babd0bbdde080ccf0eba7b36** - Retrospective Analysis of the Efficacy and Safety of Endoscopic Spinal Tuberculosis and Brucellosis Lesion Removal and Posterior Pedicle Lesion Remova
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"
- **s2:11985e8b1c67d94cf0d2613232d3f9d5cb623fe2** - Postfusion effect on pullout strength of pedicle screws with expandablepeek shell and conventional screws.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "pedicle"; `P_SPINE_PROCEDURE` = "pedicle screw"
- **s2:8fb993dd8ceb9283d914c274b630a9cb458577cf** - Supraneural transforaminal epidural injection in the treatment of radiculopathy in the lumbar spine – a brief descriptive overview and technique of ma
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_SPINE_PROCEDURE` = "epidural injection"; `C_IMAGING_LEVEL_STEP` = "Fluorosco"
- **epmc:PMC1520344** - Ruptured cervical intervertebral discs.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "cervical"

### `E_NO_FULLTEXT -> E_NO_CONCEPT` (1316 records)

- **s2:03b11435a48bfed20be5de19c87ca4e65d6e18d2** - The short-term efficacy and safety of artificial total disc replacement for selected patients with lumbar degenerative disc disease compared with ante
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "interbody fusion"
- **epmc:PMC6626756** - Complication avoidance in minimally invasive spinal surgery.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "surgeon"; `P_SPINE_PROCEDURE` = "spinal surgery"
- **s2:340915ee06b3a043bc0e8470dfe037c2abf4ae94** - Prone Lateral Corpectomy with Short-Segment Posterior Spinal Fusion for Lumbar Burst Fracture: Report of Two Cases and Technical Outline
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "Patient"; `P_SPINE_PROCEDURE` = "interbody fusion"
- **epmc:PMC11959104** - Cervical Intradural Extramedullary Endodermal Cyst Rapidly Manifesting Tetraparesis in a Pediatric Patient. A Case Report.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "cervical"; `P_HUMAN_CLINICAL` = "hospital"; `P_SPINE_PROCEDURE` = "laminotomy"

### `E_NOT_SPINE -> E_NO_POPULATION` (1081 records)

- **s2:0e2b772c103304d1b7b50dd0a619ea52c0c2ceba** - Efficacy of the Stellate Ganglion Block Through the Lateral Approach Using Ultrasonogram and Fluoroscopy.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "cervical"; `P_HUMAN_CLINICAL` = "patient"; `P_HUMAN_CLINICAL` = "patient"
- **s2:040c5c58fb833af05fb12353615de376a472e98e** - Respiratory and Internal Unit Muscle Training in Diaphragmatic Thickness and Mobility and Lombar Stability of Pregnant Women: Case Study
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "spine"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"
- **epmc:PMC7604928** - Müllerian duct anomalies with term pregnancy: a case report.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "thoracic"; `P_HUMAN_CLINICAL` = "patient"; `P_HUMAN_CLINICAL` = "patient"
- **s2:560a5dffcc40a7503bfa9167cb3aa4882f7f44c7** - 2D-fluoroscopic navigated percutaneous screw fixation of pelvic ring injuries - a case series
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "sacral"; `P_HUMAN_CLINICAL` = "case series"; `P_HUMAN_CLINICAL` = "case series"

### `E_NO_FULLTEXT -> INCLUDED` (939 records)

- **s2:c6841b2162a16f15503fc174d5daddff0cdb4eb0** - Comparison of percutaneous endoscopic interlaminar discectomy and conventional open lumbar discectomy for L4/5 and L5/S1 double-segmental lumbar disk 
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "discectomy"
- **s2:216bb097ea2248ea80344f65f3033e3ec70f4233** - Intra-Operative Complic atio n of Lumbar Kyphoplasty Instrumentatio n
in Non-Osteoporotic Patients with Compression Fractures
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "Vertebr"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "kyphoplasty"
- **epmc:PMC6046340** - A review of 571 radiographs on Tuffier's inter-cristal line and its' application in lumbar spinal surgery.
  - now: INCLUDED (Population and concept both matched: C_WRONG_LEVEL_EVENT)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `C_WRONG_LEVEL_EVENT` = "wrong level"; `P_HUMAN_CLINICAL` = "surgeon"
- **s2:02dc501510d18dfb70bca7136bee7c0f14603260** - Minimally invasive unilateral pedicle screws and a translaminar facet screw fixation and interbody fusion for treatment of single-segment lower lumbar
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "foramin"; `P_HUMAN_CLINICAL` = "hospital"; `P_SPINE_PROCEDURE` = "interbody fusion"

### `E_NOT_SPINE -> E_NO_CONCEPT` (188 records)

- **s2:00315815700e7df05382b138dfedcead172c3c9d** - Relación entre las características de los recién nacidos sometidos a procedimientos dolorosos no-quirúrgicos y el manejo del dolor en una unidad de cu
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "Retrospective"; `P_SPINE_PROCEDURE` = "lumbar puncture"
- **s2:00c8bbda621691c1b8b78066c46056efb01be7c5** - Time dependency of CSF cell count, lactate and blood-CSF barrier dysfunction after epileptic seizures and status epilepticus.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "retrospective"; `P_SPINE_PROCEDURE` = "lumbar puncture"
- **s2:010c93f7c16c55b8185bc4171412c9f55e9835d2** - Use of Clinical Criteria and Molecular Diagnosis to More Effectively Monitor Patients Recovering after Severe Acute Respiratory Syndrome Coronavirus I
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "lumbar puncture"
- **s2:025b765d2ebe9359ede72386fb2bb08c626ce594** - Meningitis due to carbapenemase-producing Aeromonas hydrophila: a case report.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "Lumbar"; `P_HUMAN_CLINICAL` = "clinical"; `P_SPINE_PROCEDURE` = "Lumbar puncture"

### `E_NO_POPULATION -> INCLUDED` (171 records)

- **s2:d2d99b0d7ed913a35079d7382a052c3b4603773a** - Adolescent Idiopathic Scoliosis Treatment by a Korean Neurosurgeon: The Changing Role for Neurosurgeons
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "scolio"; `P_HUMAN_CLINICAL` = "clinical"; `P_SPINE_PROCEDURE` = "pedicle screw"
- **epmc:PMC10257956** - Nationwide Survey of the Surgical Complications Associated with Lateral Lumbar Interbody Fusion in 2015-2020.
  - now: INCLUDED (Population and concept both matched: C_WRONG_LEVEL_EVENT)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "interbody fusion"
- **epmc:PMC3733236** - Retrolisthesis and lumbar disc herniation: a postoperative assessment of patient function.
  - now: INCLUDED (Population and concept both matched: C_WRONG_LEVEL_EVENT)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "discectomy"
- **epmc:PMC8346390** - Management of spinal deformities and tibial pseudarthrosis in children with neurofibromatosis type 1 (NF-1).
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "spinal fusion"

### `E_NOT_SPINE -> INCLUDED` (122 records)

- **s2:798082b3494807000ccf67b90cbe282a01bd9710** - Protocol of the randomised placebo controlled pilot trial of the management of acute sciatica (SCIATICA): a feasibility study
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "foramin"; `P_HUMAN_CLINICAL` = "hospital"; `P_SPINE_PROCEDURE` = "epidural steroid injection"
- **s2:a93cb22979ab1b57aa00a263a62d5195286ea5e1** - Comparison of the efficacies of TINAVI robot-assisted surgery and conventional open surgery for Levine–Edward type IIA (postreduction) hangman fractur
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "pedicle"; `P_HUMAN_CLINICAL` = "clinical"; `P_SPINE_PROCEDURE` = "pedicle screw"
- **s2:c3641684982615e3ad4f8884053004855cb33091** - 51 Carbapenem-resistant organism and Candida auris cases among non-nursing home congregate facility residents in New York City, 2019–2024
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "spinal fusion"
- **s2:1ce9dbe2788547a80c47904bff8ec25caa77c6b0** - Unsupervised Training of a Dynamic Context-Aware Deep Denoising Framework for Low-Dose Fluoroscopic Imaging
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "spinal surgery"

### `E_NO_POPULATION -> E_NO_CONCEPT` (85 records)

- **epmc:PMC9670565** - Application of C2 subfacetal screws for the management of atlantoaxial dislocation in patients with Klippel-Feil syndrome characterized by a narrow C2
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "Klippel-Feil"; `P_HUMAN_CLINICAL` = "clinical"; `P_SPINE_PROCEDURE` = "pedicle screw"
- **epmc:PMC11763388** - Patient-Reported Outcomes in Children Undergoing the Modified Green Procedure for Treating Sprengel's Deformity: Results from a Multicentric Study.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "osteotomy"; `P_HUMAN_CLINICAL` = "patient"
- **epmc:PMC8099396** - Symptomatic Atlas Hypoplasia in a Latin-American Patient: Case Report and Literature Review.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "cervical"; `P_HUMAN_CLINICAL` = "patient"; `P_SPINE_PROCEDURE` = "laminectomy"
- **epmc:PMC4843064** - Vertebral and Intraspinal Anomalies in Indian Population with Congenital Scoliosis: A Study of 119 Consecutive Patients.
  - now: E_NO_CONCEPT (Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim.)
  - from the abstract: `P_SPINE_ANY` = "vertebr"; `P_HUMAN_CLINICAL` = "Retrospective"; `P_SPINE_PROCEDURE` = "underwent surgery"

### `E_NOT_SPINE -> E_ANIMAL_CADAVER` (44 records)

- **epmc:PMC5073852** - Relationships between body condition score and ultrasound skin-associated subcutaneous fat depth in equids.
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_ANIMAL` = "horses"
- **s2:03152d8fc09eeedc661ff05e5757ec935711a674** - Effect of nerve injury on the number of dorsal root ganglion neurons and autotomy behavior in adult Bax-deficient mice
  - now: E_ANIMAL_CADAVER (Animal or cadaver term with no clinical or patient term anywhere held.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"
- **s2:5c20757eea72ccfce6a9ad964c48208096fc1fb9** - Respiratory Motion Compensation Using Diaphragm Tracking for Cone-Beam C-Arm CT: A Simulation and a Phantom Study
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "thoracic"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"
- **s2:013da35f0e62ebf42af34276374084a99d41fe9f** - Phosphorus deficiency in buffaloes in the state of Pará, Northern Brazil
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"

### `E_ANIMAL_CADAVER -> E_NO_POPULATION` (34 records)

- **epmc:PMC3276343** - Transient overexpression of sonic hedgehog alters the architecture and mechanical properties of trabecular bone.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "vertebr"; `P_ANIMAL` = "mice"; `P_HUMAN_EXPLICIT` = "adult"
- **epmc:PMC5923383** - Targeting of NAT10 enhances healthspan in a mouse model of human accelerated aging syndrome.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_HUMAN_CLINICAL` = "patient"; `P_HUMAN_CLINICAL` = "patient"; `P_ANIMAL` = "mouse"
- **epmc:PMC3229977** - Lathyrism-induced alterations in collagen cross-links influence the mechanical properties of bone material without affecting the mineral.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_SPINE_ANY` = "vertebr"; `P_HUMAN_CLINICAL` = "patient"; `P_HUMAN_CLINICAL` = "patient"
- **epmc:PMC9668918** - Comprehensive dynamic and kinematic analysis of the rodent hindlimb during over ground walking.
  - now: E_NO_POPULATION (No spine procedure or vertebral-enumeration population with a human or clinical term.)
  - from the abstract: `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"; `P_ANIMAL` = "rat"

### `E_NO_FULLTEXT -> E_ANIMAL_CADAVER` (32 records)

- **epmc:PMC9913153** - The Thoracic Inlet Heart Size, a New Approach to Radiographic Cardiac Measurement.
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "Vertebr"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"
- **s2:05ec2ea957a432cc0d926ce28e031d97127faf05** - Anti-inflammatory effects of sacral nerve stimulation: a novel spinal afferent and vagal efferent pathway.
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "Sacral"; `P_ANIMAL` = "rats"
- **s2:0004d3f98e3d6e8c2c54fe5b2c4bcdd2b41ee382** - Intrathecal infusion of hypertonic fluid enables CSF Flow Enhancement (CFE) to facilitate nanoparticle delivery to the brain and spinal cord
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_ANIMAL` = "mice"
- **epmc:PMC1007398** - Radiological cervical arthritis in populations.
  - now: E_ANIMAL_CADAVER (Animal or cadaver work in the retrieved text with no explicit human population term.)
  - from the abstract: `P_SPINE_ANY` = "cervical"; `P_ANIMAL` = "sheep"

### `E_ANIMAL_CADAVER -> INCLUDED` (26 records)

- **s2:f6b28d97491202f7f1df816a02e9d9830bebd958** - A novel minimally invasive, dorsolateral, tubular partial odontoidectomy and autologous bone augmentation to treat dens pseudarthrosis: cadaveric, 3D 
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "odontoid"; `P_HUMAN_CLINICAL` = "clinical"; `P_SPINE_PROCEDURE` = "pedicle screw"
- **s2:2683a5bbd3430b3f0c392bbf89146707833b2f7e** - Puncture and localization for percutaneous endoscopic lumbar discectomy with C-arm navigation: a randomized controlled cadaver trial
  - now: INCLUDED (Population and concept both matched: C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "lumbar"; `P_HUMAN_CLINICAL` = "surgeon"; `P_SPINE_PROCEDURE` = "discectomy"
- **epmc:PMC6102422** - Usefulness of spinal unenhanced computed tomography and CT-myelography in the age of multidetector CT technology and magnetic resonance imaging - Prel
  - now: INCLUDED (Population and concept both matched: C_TRANSITIONAL)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "clinical"; `P_HUMAN_CLINICAL` = "clinical"
- **epmc:PMC6857820** - Using Porcine Cadavers as an Alternative to Human Cadavers for Teaching Minimally Invasive Spinal Fusion: Proof of Concept and Anatomical Comparison.
  - now: INCLUDED (Population and concept both matched: C_NUMBERING, C_IMAGING_LEVEL_STEP)
  - from the abstract: `P_SPINE_ANY` = "spinal"; `P_HUMAN_CLINICAL` = "surgeon"; `P_SPINE_PROCEDURE` = "pedicle screw"
