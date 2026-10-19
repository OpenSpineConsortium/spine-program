# The AIDaS program: goal, epics and tasks

Written by render_plan.py from plan.json; edit plan.json, then run render_plan.py and make_issues.py.

**Goal** ([#121](https://github.com/OpenSpineConsortium/spine-program/issues/121)): AIDaS 2027: a customizable spine RAG-LLM in one year, built by agents under REFORMS.

The program the AIDaS Seed Grant proposal of 2026-10-16 describes (01_carm_level_detection/grants/aidas_2027/latex/main.tex at 88871de): Aim 1, Claude Code iterating the scientific method on the WSU grid inside Beethoven, beethoven-qa, beethoven-research and Symphony; Aim 2, eight medical trainees driving that agent; Aim 3, CT-labeled structure carried into C-arm images and on to a spine RAG-LLM. Award period January 1 to December 31, 2027, pending the award. Each epic below is a sub-issue of this one, and each task a sub-issue of its epic; 13_aidas_program/PLAN.md is the same tree as prose.

## E1: Workflow: the folder's way of working, REFORMS records and the two gates ([#122](https://github.com/OpenSpineConsortium/spine-program/issues/122))

How every task in this program is done: a question and a pass/fail gate sealed by hash before the first job, the REFORMS record kept as the work goes, code passing beethoven-qa, every evaluation passing beethoven-research's split check, one pull request per task. 13_aidas_program/REFORMS.md maps the checklist to the tasks.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E1.1 Onboard to the program: grid account, Beethoven, CITI, the folder's rules | [#123](https://github.com/OpenSpineConsortium/spine-program/issues/123) | Ashley | a grid job of Ashley's own runs through Beethoven and its log returns to a claim branch; CITI Biomedical and HIPS courses current |  |  |
| E1.2 Write the REFORMS record template and the sealed-gate template | [#124](https://github.com/OpenSpineConsortium/spine-program/issues/124) | Ashley | templates/REFORMS_RECORD.md and templates/GATE.md exist, each REFORMS item has a field, and sealing a gate prints its sha256 | all modules |  |
| E1.3 Wire beethoven-qa's gate into the program's code | [#125](https://github.com/OpenSpineConsortium/spine-program/issues/125) | Ashley | a pull request that adds a public function without a contract fails the gate; one with a contract passes | 2 computational reproducibility, 5 modeling |  |
| E1.4 Run beethoven-research's split check on every evaluation | [#126](https://github.com/OpenSpineConsortium/spine-program/issues/126) | Ashley | every evaluation in the program has a split check result on file; a planted shared patient is refused | 6 data leakage |  |
| E1.5 Write the CLAIM checklist for imaging AI into beethoven-research | [#127](https://github.com/OpenSpineConsortium/spine-program/issues/127) | Ashley | every CLAIM 2024 item has a field and a check or a reason it is checked by hand | 8 generalizability and limitations |  |
| E1.6 Monthly status to the PI and Co-PI, and the final report's skeleton | [#128](https://github.com/OpenSpineConsortium/spine-program/issues/128) | Ashley | one status note a month in 13_aidas_program/reports/, each epic's state in a line |  |  |

## E2: IRB and regulatory: the protocol, the trainee study, DMC access, the FDA Pre-Submission ([#129](https://github.com/OpenSpineConsortium/spine-program/issues/129))

What must be approved before the data work starts. The change list for IRB-26-03-8648 is outside git (the project's files, grant-irb/), since it is drawn from the IRB form (root CLAUDE.md rule 12).

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E2.1 Apply the change list to IRB-26-03-8648 and submit it | [#130](https://github.com/OpenSpineConsortium/spine-program/issues/130) | Greg | the protocol's status in eProtocol is Submitted, then Approved | 1 study goals |  |
| E2.2 Add the PI, the Co-PI and the research assistant to the protocol | [#131](https://github.com/OpenSpineConsortium/spine-program/issues/131) | Greg | each is listed in eProtocol with current CITI courses |  | E1.1 [#123](https://github.com/OpenSpineConsortium/spine-program/issues/123) |
| E2.3 Draft the exempt application for the trainee study (Aim 2) | [#132](https://github.com/OpenSpineConsortium/spine-program/issues/132) | Ashley | the application is filed in eProtocol and a determination number is recorded | 1 study goals |  |
| E2.4 DMC data access: the EMR and PACS request for the cohort | [#133](https://github.com/OpenSpineConsortium/spine-program/issues/133) | Greg | the DMC approval and the access route are recorded | 3 data quality | E2.1 [#130](https://github.com/OpenSpineConsortium/spine-program/issues/130) |
| E2.5 FDA Pre-Submission package for the advisory level label | [#134](https://github.com/OpenSpineConsortium/spine-program/issues/134) | Dr. Han | the package is filed by April 2027, before FDA's proposed fee from October 1, 2027 | 8 generalizability and limitations |  |
| E2.6 Cadaver set paperwork: Body Bequest Program, DLAR session, dosimetry and OEHS | [#135](https://github.com/OpenSpineConsortium/spine-program/issues/135) | Ashley | two specimens requested, the C-arm session booked, the dosimetry enrolment and OEHS form filed 15 business days before it | 3 data quality |  |

## E3: Clinical data mining: the DMC spine surgery cohort under the IRB ([#136](https://github.com/OpenSpineConsortium/spine-program/issues/136))

About 4,000 adult DMC spine surgery patients, imaging with operative notes and radiology reports, coded with the key in REDCap, de-identified to NIfTI on the grid. Nothing here starts before E2.1 and E2.4 are approved, and no patient data reaches any cloud AI service, the Claude agent included.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E3.1 Build the data dictionary in REDCap | [#137](https://github.com/OpenSpineConsortium/spine-program/issues/137) | Ashley | every variable has a type, a source field and a coding rule; a test record round-trips | 3 data quality | E2.1 [#130](https://github.com/OpenSpineConsortium/spine-program/issues/130) |
| E3.2 Write the cohort query: codes, surgical logs, inclusion and exclusion | [#138](https://github.com/OpenSpineConsortium/spine-program/issues/138) | Ashley | the query and its counts at each step are written before the first extraction, and the final count is recorded | 3 data quality, 4 preprocessing | E2.4 [#133](https://github.com/OpenSpineConsortium/spine-program/issues/133) |
| E3.3 De-identification pipeline: DICOM to NIfTI, text scrubbing, the coded key | [#139](https://github.com/OpenSpineConsortium/spine-program/issues/139) | Ashley | a header check finds no identifier in any output, and a sample of scrubbed notes is read by a person | 4 preprocessing | E3.2 [#138](https://github.com/OpenSpineConsortium/spine-program/issues/138) |
| E3.4 Double-code 15 percent and report agreement | [#140](https://github.com/OpenSpineConsortium/spine-program/issues/140) | Ashley | Cohen's kappa and ICC with intervals for every variable, about 600 charts | 3 data quality, 7 metrics and uncertainty | E3.3 [#139](https://github.com/OpenSpineConsortium/spine-program/issues/139) |
| E3.5 Pre-register the case-control analyses | [#141](https://github.com/OpenSpineConsortium/spine-program/issues/141) | Ashley | the analysis plan is sealed by hash before any outcome is looked at | 1 study goals, 7 metrics and uncertainty | E3.1 [#137](https://github.com/OpenSpineConsortium/spine-program/issues/137) |

## E4: C-arm training: close the detection gap (Aim 3) ([#142](https://github.com/OpenSpineConsortium/spine-program/issues/142))

The level model names 96.4 percent of the lateral vertebrae a film-trained detector finds on a public C-arm, while detection there stays at 80.5 percent (90.6 at 0.25) against the 97 percent set in advance (the proposal's Figure 1f; RECORD.md section 1). These tasks close that gap with COBRA's unseen projections, corner labels, learned simulation and the cadaver set. The level-identification code and weights stay private (root CLAUDE.md rule 8).

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E4.1 Export COBRA's 372,000 unseen projections and look at the Varian bank | [#143](https://github.com/OpenSpineConsortium/spine-program/issues/143) | Ashley | every exported case has its geometry and registered CT; a rendered sample of the Varian bank is looked at and recorded | 3 data quality, 4 preprocessing |  |
| E4.2 Corner labels by projecting each CT's corners at the device geometry | [#144](https://github.com/OpenSpineConsortium/spine-program/issues/144) | Ashley | projected corners rendered on 50 random frames and looked at; exact on renders | 4 preprocessing | E4.1 [#143](https://github.com/OpenSpineConsortium/spine-program/issues/143) |
| E4.3 Train the corner-learning C-arm detector, leave one device out | [#145](https://github.com/OpenSpineConsortium/spine-program/issues/145) | Ashley | sealed before training: 97 percent of vertebrae and sacra on each held-out C-arm at 0.74, with no more false detections than today | 5 modeling, 6 data leakage, 7 metrics and uncertainty | E4.2 [#144](https://github.com/OpenSpineConsortium/spine-program/issues/144), E1.4 [#126](https://github.com/OpenSpineConsortium/spine-program/issues/126) |
| E4.4 Learned X-ray simulation until a classifier cannot tell renders from real frames | [#146](https://github.com/OpenSpineConsortium/spine-program/issues/146) | Ashley | the render-versus-real classifier at chance on held-out frames, the anatomy and labels unchanged | 5 modeling | E4.1 [#143](https://github.com/OpenSpineConsortium/spine-program/issues/143) |
| E4.5 Image and seal the cadaver set | [#147](https://github.com/OpenSpineConsortium/spine-program/issues/147) | Ashley | two specimens CT-scanned and imaged AP and lateral at lumbar and thoracic positions, the set sealed by hash before any model sees it | 3 data quality, 6 data leakage | E2.6 [#135](https://github.com/OpenSpineConsortium/spine-program/issues/135) |
| E4.6 Measure the stack's latency on one GPU | [#148](https://github.com/OpenSpineConsortium/spine-program/issues/148) | Ashley | median and 95th percentile per frame on one GPU, recorded with the job id | 7 metrics and uncertainty |  |

## E5: Literature data mining: the Scopus and ScienceDirect spine corpus on the grid ([#149](https://github.com/OpenSpineConsortium/spine-program/issues/149))

Elsevier granted WSU text and data mining on Scopus and ScienceDirect, text, images and multimedia. Its content is never made public: the WSU library and Elsevier confirmed on 2026-10-19 that Claude may read it on that condition; it never trains a model, as WSU told Elsevier, and only short quotations with citation and DOI appear in anything published. The API key and the institutional token stay server-side on the grid, sent only in request headers over HTTPS.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E5.1 Store the Elsevier key and institutional token on the grid | [#150](https://github.com/OpenSpineConsortium/spine-program/issues/150) | Greg | both are files readable by their owner alone, outside every repository; the harvester reads them by path | 2 computational reproducibility |  |
| E5.2 Harvest the spine corpus as sbatch jobs | [#151](https://github.com/OpenSpineConsortium/spine-program/issues/151) | Ashley | the query, the counts and a checksum of every file recorded; no token in any log | 3 data quality | E5.1 [#150](https://github.com/OpenSpineConsortium/spine-program/issues/150) |
| E5.3 Build the passage index with citations and DOIs | [#152](https://github.com/OpenSpineConsortium/spine-program/issues/152) | Ashley | every passage traces to its article, page and DOI; the index deletes itself when the project or key ends | 4 preprocessing | E5.2 [#151](https://github.com/OpenSpineConsortium/spine-program/issues/151) |
| E5.4 Host the grid text model that answers with verbatim quotations | [#153](https://github.com/OpenSpineConsortium/spine-program/issues/153) | Ashley | a misquoted passage fails the gate; quotation support graded on a held-out question set | 5 modeling, 7 metrics and uncertainty | E5.3 [#152](https://github.com/OpenSpineConsortium/spine-program/issues/152) |

## E6: The spine RAG-LLM (Aim 3): detectors as tools, two releases, graded against OpenEvidence ([#154](https://github.com/OpenSpineConsortium/spine-program/issues/154))

A multimodal model hosted on the grid that takes the image, the detectors' boxes and names and the retrieved passages, and answers with the level, the finding and verbatim quotations; customizable in that a lab swaps in its own corpus, detectors and records.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E6.1 Choose and host the multimodal base model on the grid's GPUs | [#155](https://github.com/OpenSpineConsortium/spine-program/issues/155) | Dr. Han | the model's licence, version and weights hash recorded; it serves one request on a grid GPU | 5 modeling |  |
| E6.2 Give the model the detector and the level model as tools | [#156](https://github.com/OpenSpineConsortium/spine-program/issues/156) | Ashley | on 20 public images the model's answer names the level the tools returned | 5 modeling | E6.1 [#155](https://github.com/OpenSpineConsortium/spine-program/issues/155) |
| E6.3 First release: fine-tune on the public corpus | [#157](https://github.com/OpenSpineConsortium/spine-program/issues/157) | Dr. Han | trained only on public data, its split checked, its weights hashed | 5 modeling, 6 data leakage | E6.2 [#156](https://github.com/OpenSpineConsortium/spine-program/issues/156), E5.4 [#153](https://github.com/OpenSpineConsortium/spine-program/issues/153) |
| E6.4 Write the held-out question set on public images and its grading rubric | [#158](https://github.com/OpenSpineConsortium/spine-program/issues/158) | Ashley | the questions and rubric sealed by hash before any model answers them | 7 metrics and uncertainty |  |
| E6.5 Grade the RAG-LLM against OpenEvidence | [#159](https://github.com/OpenSpineConsortium/spine-program/issues/159) | Ashley | H3's comparison reported, a loss reported as one | 7 metrics and uncertainty, 8 generalizability | E6.3 [#157](https://github.com/OpenSpineConsortium/spine-program/issues/157), E6.4 [#158](https://github.com/OpenSpineConsortium/spine-program/issues/158) |
| E6.6 Second release: fine-tune on images paired with charts under the IRB | [#160](https://github.com/OpenSpineConsortium/spine-program/issues/160) | Dr. Han | trained on the grid only; its weights stay on the grid; split checked by patient | 5 modeling, 6 data leakage | E2.1 [#130](https://github.com/OpenSpineConsortium/spine-program/issues/130), E3.4 [#140](https://github.com/OpenSpineConsortium/spine-program/issues/140) |

## E7: Aim 1: the agent doing research under the frameworks, and its cost ([#161](https://github.com/OpenSpineConsortium/spine-program/issues/161))

Claude Code at a pinned model version iterates hypotheses on the grid; a result counts only when a test sealed before the run passes and a person merges it. The agent never reads patient data; it may read Elsevier content, which is never made public.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E7.1 Write the 30 tasks: 10 for development, 20 sealed with hidden checks | [#162](https://github.com/OpenSpineConsortium/spine-program/issues/162) | Ashley | each sealed task has a hidden check, a clean copy and a faulted copy, all hashed | 1 study goals, 6 data leakage | E1.2 [#124](https://github.com/OpenSpineConsortium/spine-program/issues/124) |
| E7.2 Plant the faults | [#163](https://github.com/OpenSpineConsortium/spine-program/issues/163) | Dr. Schwiebert | someone who did not write the checks plants one fault per faulted copy: a shared patient, a wrong label scheme, a threshold tuned on the test set, a typed number, a run that does not reproduce | 6 data leakage | E7.1 [#162](https://github.com/OpenSpineConsortium/spine-program/issues/162) |
| E7.3 Run the 80 runs, with and without the checks | [#164](https://github.com/OpenSpineConsortium/spine-program/issues/164) | Ashley | H1 reported: wrong results on faulted copies, passes on clean copies, reruns within a sealed tolerance | 2 computational reproducibility, 7 metrics | E7.2 [#163](https://github.com/OpenSpineConsortium/spine-program/issues/163), E1.3 [#125](https://github.com/OpenSpineConsortium/spine-program/issues/125), E1.4 [#126](https://github.com/OpenSpineConsortium/spine-program/issues/126) |
| E7.4 The profiler and the four economies (1b) | [#165](https://github.com/OpenSpineConsortium/spine-program/issues/165) | Ashley | H1b reported: tokens per passing gate with and without the economies | 2 computational reproducibility | E7.1 [#162](https://github.com/OpenSpineConsortium/spine-program/issues/162) |
| E7.5 The protocol against its competitors (1c) | [#166](https://github.com/OpenSpineConsortium/spine-program/issues/166) | Greg | waits for Greg's word before any run | 7 metrics and uncertainty |  |

## E8: Recruitment and Aim 2: eight trainees drive the agent ([#167](https://github.com/OpenSpineConsortium/spine-program/issues/167))

Two waves of four medical students and residents, each with a grid account, Beethoven and a gated sub-project; a preregistered within-trainee crossover against the 2026 setup. Waits on E2.3's exempt determination.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E8.1 Recruit eight trainees in two waves | [#168](https://github.com/OpenSpineConsortium/spine-program/issues/168) | Ashley | eight enrolled under the determination, by someone who neither teaches nor supervises them | 1 study goals | E2.3 [#132](https://github.com/OpenSpineConsortium/spine-program/issues/132) |
| E8.2 Accounts and seats: grid, Beethoven, Claude Team seats | [#169](https://github.com/OpenSpineConsortium/spine-program/issues/169) | Ashley | each trainee runs one grid job through Beethoven |  | E8.1 [#168](https://github.com/OpenSpineConsortium/spine-program/issues/168) |
| E8.3 Write and pre-register the matched starter tasks | [#170](https://github.com/OpenSpineConsortium/spine-program/issues/170) | Ashley | task pairs, order counterbalancing and H2's measures sealed by hash before wave 1 | 1 study goals, 7 metrics |  |
| E8.4 Run the comfort survey before and after each wave | [#171](https://github.com/OpenSpineConsortium/spine-program/issues/171) | Ashley | both surveys collected and coded with no names | 7 metrics and uncertainty | E8.1 [#168](https://github.com/OpenSpineConsortium/spine-program/issues/168) |
| E8.5 Run the waves and report H2 | [#172](https://github.com/OpenSpineConsortium/spine-program/issues/172) | Ashley | H2's two measures with 95 percent intervals | 7 metrics and uncertainty | E8.2 [#169](https://github.com/OpenSpineConsortium/spine-program/issues/169), E8.3 [#170](https://github.com/OpenSpineConsortium/spine-program/issues/170) |

## E9: Award administration: allowability, hiring, purchases ([#173](https://github.com/OpenSpineConsortium/spine-program/issues/173))

The budget of $19,987 (the proposal's budget page) once awarded.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E9.1 Get the AIDaS office's answer on lines A, B, C3, D and F | [#174](https://github.com/OpenSpineConsortium/spine-program/issues/174) | Greg | the answer recorded with its date |  |  |
| E9.2 Hire the part-time researcher (line A) | [#175](https://github.com/OpenSpineConsortium/spine-program/issues/175) | Dr. Han | a hire in place by month 3 |  | E9.1 [#174](https://github.com/OpenSpineConsortium/spine-program/issues/174) |
| E9.3 Buy the Claude seats, the storage and the frame grabber | [#176](https://github.com/OpenSpineConsortium/spine-program/issues/176) | Dr. Han | six seats in January 2027, 2 TB of C&IT storage, the Magewell capture unit |  | E9.1 [#174](https://github.com/OpenSpineConsortium/spine-program/issues/174) |

## E10: Proposals and dissemination: CAREER, R21, CyberTraining, the symposium ([#177](https://github.com/OpenSpineConsortium/spine-program/issues/177))

The federal proposals the award must lead to within 12 months, and the record they need.

| task | issue | owner | gate | REFORMS | waits on |
|---|---|---|---|---|---|
| E10.1 NSF CAREER, due July 28, 2027 | [#178](https://github.com/OpenSpineConsortium/spine-program/issues/178) | Dr. Han | submitted with Aim 1's early results and Aim 2's first wave |  | E7.3 [#164](https://github.com/OpenSpineConsortium/spine-program/issues/164) |
| E10.2 NIH R21 at NIBIB, due October 18, 2027 | [#179](https://github.com/OpenSpineConsortium/spine-program/issues/179) | Dr. Han | submitted with the cadaver set, the latency and FDA's feedback |  | E4.5 [#147](https://github.com/OpenSpineConsortium/spine-program/issues/147), E4.6 [#148](https://github.com/OpenSpineConsortium/spine-program/issues/148), E2.5 [#134](https://github.com/OpenSpineConsortium/spine-program/issues/134) |
| E10.3 NSF CyberTraining Pilot, due January 20, 2028 | [#180](https://github.com/OpenSpineConsortium/spine-program/issues/180) | Dr. Schwiebert | submitted, sized by H2 |  | E8.5 [#172](https://github.com/OpenSpineConsortium/spine-program/issues/172) |
| E10.4 The AIDaS symposium poster and the final report | [#181](https://github.com/OpenSpineConsortium/spine-program/issues/181) | Ashley | the poster printed and the report sent in December 2027 | 8 generalizability and limitations | E1.6 [#128](https://github.com/OpenSpineConsortium/spine-program/issues/128) |
| E10.5 Submit the proposal to Anthropic's AI for Science program and the other fits | [#182](https://github.com/OpenSpineConsortium/spine-program/issues/182) | Greg | each submission recorded with its date |  |  |
