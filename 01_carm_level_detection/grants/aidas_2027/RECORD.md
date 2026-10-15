# The AIDaS packet's record: where each number comes from, what the web settled, what is open

`latex/main.tex` is the packet; this file is what stands behind it and is not submitted. Until 2026-10-14 the packet
itself was this markdown (`AIDaS_SEED_2027_packet.md`, pull requests #91 and #93); the LaTeX source replaced it in
the pull request that closes issue #94, which applied `REVIEW_2026-10-14.md` and the three reviews of that day (a
numbers audit, a compliance read and a mock panel), with the changes made by design listed in section 4. Paths are
relative to spine-program; the record folders (`results/`, `figures/`, `manuscripts/`, `regulatory/`) live on the
grid and are read here from git history at main 5597197 (`ARCHIVE.md`). Row ids such as A2.1 are those of
`01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md`.

## 1. The file behind every number in the packet

| number in the packet | file |
|---|---|
| 0.12 % wrong-level surgery in a 27-hospital Japanese registry of 34,544 patients having degenerative spine surgery, 0.42 % thoracic [1] | `09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md` (Furuya 2026) |
| about half of responding US neurosurgeons report a wrong-level operation [2,3] | the same file (Mody 2008; Groff 2013); both surveyed neurosurgical societies, and Groff's "almost 50 %" is of lumbar surgery |
| 12.9 % of 550 surgical patients had a transitional vertebra; miscounted in clinic in 54 % [4] | `02_transitional_naming_truth/docs/LEVELCHECK_CLAIM.md` (Nakagawa 2017) |
| LevelCheck registers the preoperative CT to each image [5], 17 to 72 s in an operating room [6], against the 20 s to one minute surgeons said they would wait [7] | `01_carm_level_detection/docs/MODEL_CARD.md` section 6 (`levelcheck2012`, `manbachi2018`, `desilva2016`) |
| CTSpinoPelvic1K: 802 CTs, release 11, Zenodo 10.5281/zenodo.22797014 [8] | `03_ctspinopelvic1k_dataset/README.md` |
| one figure of the consortium's C-arm study took 250 fine-tunes | catalog section A9's header (250 / 250 cells behind Figure 5b) |
| the 2026 cohort [9]: 16 students, seven with no coding and eleven with no imaging experience, ten sub-projects active at the survey, all ten submitted as abstracts to a national meeting; Table 1's six domains, rated retrospectively before and after; the IRB's determination that the program was not human participant research; its success depending on mentors expert in Python, imaging software and Slurm; its limits, no control group and no objective measure | Cureus 2026;18(7):e112661, the PDF under `11_students_grid_access/manuscripts/` at 5597197 (Methods, Results, Limitations) |
| the grid's H200 partition, 4 nodes of 4 GPUs (gmsap) | `11_students_grid_access/docs/handoff/EXTRACTS_11.md` |
| 7,045 standard and 1,482 transitional annotated physics renders | `08_render_devices/README.md` (the 7,045 include 1,321 renders of synthetic-implant CTs) |
| a device-styled corpus of 142 TotalSegmentator spines | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` (devcorpus; design P; 12,730 styled entries) |
| C-ArmLSpine: 149 public lumbar cases, each a cone-beam CT with AP and lateral frames; automatic truth from two CT labelers agreeing | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` section 2.3 (149 is the released count; `MODEL_CARD.md` section 5.1 scores 148) and `MODEL_CARD.md` section 5.1 ([AUTO-TRUTH]) |
| YOLO11m detector; ResNet-18 encoder; two-layer bidirectional GRU over the run of 2 to 9 bodies; 27 levels | `01_carm_level_detection/docs/MODEL_CARD.md` (the model table); Figure 3a is `figures/schwingnet/fig1c_arch.pdf` at 5597197 |
| SID 1,140 mm and SOD 745 mm, so 1.53 times larger on the detector (Figure 3b) | `01_carm_level_detection/docs/MODEL_CARD.md` section 6.1 |
| the sixth lumbar vertebra in a labeled CT, its render and another person's radiograph; scale bars 20 mm, white on the CT and the render and black on the radiograph (Figure 1c) | `01_carm_level_detection/figures/schwingnet/figure1.png` and `figure1.record.json` ("bar, 20 mm") at 5597197 |
| 96.4 % of the 617 lateral bodies the film-trained detector finds, with no C-arm frame in training (595 / 617, [92.3, 98.4]) | row A2.1 (the naming boxes come from the film-trained keypoint body detector, `detector_v5z_final` at 0.35; the A2 rows' header) |
| 88.0 % of all 676 lateral bodies with agreed truth (595 / 676; the detector finds 617 of them) | rows A2.6, A2.7 |
| 43.7 % of 631 AP bodies (276 / 631, [34.9, 51.9]) | row A2.2 |
| AP fine-tuned on five cases' frames, 90.8 % [86.7, 94.3]; on all the other cases of each fold, 98.1 % [95.7, 99.8]; test cases held out | row A9.2 (on the catalog's REP truth, 633 AP bodies, where the same encoder's starting point is 33.8 %; Figure 4a sets it beside A2.2's zero-shot 43.7 % on 631 agreed bodies); the intervals are those of `results/schwingnet/indomain/name_fill.json` at 5597197, the file the A9 header names (figure5b, AP to AP, N = 5 and N = all; a case-clustered percentile bootstrap over 142 cases) |
| on the 233 frames where the sacrum is found, 81.5 % of the 286 that show one | row A6.6 |
| count and shape coupled, 98.2 % of 1,009 bodies (991 / 1,009, [96.5, 99.5]) | row A5.1 |
| the stack abstains on 9.9 % of those 233 frames (13 where count and shape disagree, 10 where the name is unsure) and catches 5 of the 6 that err | row A5.3 |
| the C-arm detector, trained on COBRA's and DeepFluoro's real frames, on the held-out C-ArmLSpine at 0.74: 80.5 % of vertebrae (231 / 287, [74.1, 86.8]), 76.8 % of sacra (43 / 56) | row A6.1 (`rx_lodo_carmlspine_1024`, a YOLO11m; 56 frames of 28 cases) |
| the same at 0.25: 90.6 % (260 / 287, [84.3, 94.5]), sacra 83.9 % (47 / 56) | row A6.2 |
| on rebuilt truth, 82.2 % of the 287 (236 / 287) and 93.9 % of the 214 vertebrae whose truth is complete and at least 80 % visible (201 / 214) | row A6.5, "both printed" (`results/schwingnet/indomain/DENOMINATOR_REPAIR.md` at 5597197); the repaired denominator's rule is in `docs/handoff/GLOSSARY.md`; A6.1's 80.5 % is on the truth before the rebuild |
| styled renders added to two devices' real frames: 63.1 % (181 / 287, [54.8, 71.0]) at 0.74, 87.8 % at 0.25 | rows A6.11, A7.8 |
| renders only: 0.3 % (1 / 287) at 0.74, 31.7 % (91 / 287) at 0.25 | row A6.12 |
| the 97 % set in advance, met by no held-out cell | row A6.13 (`ssn:docs/RSNAI_PLAN.md` C7) |
| styled renders 99 to 100 % separable from real frames | row A13.3 |
| for the R21: 99 patients give 80 % power for a Wilson lower bound of 90 % at a true 97 % (exactly 82 %; 98 give 66 %, so the number is exactly 99) | row E.4 (its planning values have no transitional measurement behind them) |
| the Co-PI's four high-performance computing papers with the clinical collaborator (2021 to 2024); the PI's Gaussian-splatting and implicit-surface papers (CVPR 2025 and 2026, NeurIPS 2024); the PI's PhD of November 2017 and appointment since January 2021 | the two biosketches (submitted with the packet, not committed) |

No number in the packet comes from a row marked LEAKED, SUPERSEDED or RECORD ONLY (root CLAUDE.md rule 5). The
numbers drawn in Figures 2c and 4 are typed once in `make_figures.py` beside their rows; `figures/sources/SOURCES.md`
says where each image comes from. The narrative quotes no number from the execution skeleton's mock run.

## 2. Values found on the public web, 2026-10-14

The session's page fetcher could not reach any site, so most of these rest on search-engine excerpts of the pages
named; only the PI's homepage (through its GitHub source) and Anthropic's pages were read directly. Check each on its
page before submitting.

| value in the packet | source |
|---|---|
| the call: due October 16, 2026, 11:59 p.m. ET, one PDF to the AIDaS office; four awards of $10,000 to $20,000; the PI an AIDaS affiliated member on a tenure-track or tenured appointment; no award funds to external collaborators; a final report, an AIDaS event, acknowledgment and a federal proposal within 12 months of the end | https://aidas.wayne.edu/seed-grant, and the call itself, `01_carm_level_detection/regulatory/carm_validation_plan_2026-09-21/AIDaS_Seed_Grant_Program.pdf` at 5597197 |
| both investigators are AIDaS affiliated members | the owner, 2026-10-14 (no public member list was found) |
| the PI: Assistant Professor of Computer Science; at Wayne State since January 2021; founding director of the Machine Perception Lab | the PI's College of Engineering profile page and personal homepage (addresses left out, since each carries the PI's university ID) |
| the Co-PI: Professor since 2021, chair 2014 to 2022; GPU acceleration of scientific codes | the Co-PI's College of Engineering profile page (address left out, as above) |
| the cover's contact lines (in `latex/contacts.tex`, never committed) | the Computer Science department directory, https://engineering.wayne.edu/about/directory.php?group=1117, and the WSU people directory |
| NIH Early Stage Investigator status ends ten years after the terminal degree, so November 2027 | https://grants.nih.gov/policy-and-compliance/policy-topics/early-stage-investigators/determining-status |
| NSF CAREER: NSF 22-586, the fourth Wednesday of July (July 28, 2027; July 26, 2028); eligibility judged at the deadline | https://www.nsf.gov/funding/opportunities/career-faculty-early-career-development-program |
| IIS core programs under Future CoRe, NSF 25-543 | https://www.nsf.gov/ (NSF 25-543, posted July 25, 2025) |
| NIBIB Trailblazer: PA-25-169 expired May 8, 2026; successor forecast FOR-EB-26-001 | https://grants.nih.gov/grants/guide/pa-files/PA-25-169.html and https://simpler.grants.gov/opportunity/9f06c317-b398-4482-89b1-57bcf35363f3 |
| parent R21 PA-25-304, expires January 8, 2028, last date October 16, 2027; NIBIB's EBRG PAR-25-321 through October 16, 2027 | https://grants.nih.gov/grants/guide/pa-files/PA-25-304.html |
| October 16, 2027 is a Saturday, so the R21 goes in Monday, October 18 | https://grants.nih.gov/grants-process/submit/submission-policies/standard-due-dates and the calendar |
| NSF CyberTraining, NSF 23-520: Pilot up to $300,000 over two years; the third Thursday of January (January 20, 2028) | https://www.nsf.gov/funding/opportunities/training-based-workforce-development-advanced |
| NSF Smart Health, NSF 25-542, awaiting a new solicitation | https://www.nsf.gov/funding/opportunities/sch-smart-health-biomedical-research-era-artificial-intelligence/nsf25-542/solicitation |
| America's AI Action Plan (July 2025): AI-enabled science; a worker-first agenda | https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf |
| EO 14363, the Genesis Mission; NSF DCL 26-023; NIH's Bio Genesis Mission | https://www.federalregister.gov/documents/2025/11/28/2025-21665/launching-the-genesis-mission and https://www.nih.gov/bio-genesismission |
| EO 14303, Gold Standard Science; OSTP's guidance of June 2025 on pre-registration and null results | https://www.federalregister.gov/documents/2025/05/29/2025-09802/restoring-gold-standard-science and https://www.whitehouse.gov/wp-content/uploads/2025/03/OSTP-Guidance-for-GSS-June-2025.pdf |
| the NIH Strategic Plan for Data Science 2025-2030 | https://datascience.nih.gov/nih-strategic-plan-data-science (the plan's title and years only; the sentence that it and NIH's data sharing policy ask for reusable data is inferred, not quoted) |
| FDA Q-Submission: written feedback within 70 days; no fee today; a $2,000 fee proposed from fiscal year 2028 | https://www.fda.gov/media/114034/download and https://www.fda.gov/media/193532/download |
| Michigan minimum wage $15.00 from January 1, 2027 | MCL 408.934, https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-408-934 |
| temporary employees and students are not benefit-eligible | https://hr.wayne.edu/tcw/benefits |
| a student assistant's composite fringe rate, 1.7 % (FICA only), fiscal year 2025 | https://fisops.wayne.edu/accounting/files/composite-2025-fringe-benefit-detail.pdf (from https://fisops.wayne.edu/accounting/cost/fringe-benefits) |
| capital equipment threshold $5,000 | https://policies.wayne.edu/appm/6-property-and-capital-equipment |
| C&IT hosted storage $40 per 100 GB a year, so $400 per TB | https://services.wayne.edu/TDClient/277/Portal/KB/Article/20343 |
| the grid's compute is free to WSU researchers | https://services.wayne.edu/TDClient/277/Portal/KB/Article/20229/Grid-FAQs |
| the Body Bequest donor authorization permits de-identified images | https://bodybequest.med.wayne.edu/docs/bbp_brochure.pdf |
| the C-arm in Room 0312 Elliman; dosimetry badges at DLAR's director 15 business days ahead | https://research.wayne.edu/oehs/rad-safety/xray-imaging |
| Magewell USB Capture AIO, $619 retail | https://www.fullcompass.com/prod/600750-magewell-usb-capture-aio-usb-capture-aio |
| an OEC 9900's live output is BNC; its DVI output carries review images | https://www.blockimaging.com/oec-9900-how-to-add-an-extra-real-time-image-monitor |
| a mid-level regulatory consultant, about $200 to $400 an hour (the packet uses $300) | https://seed.nih.gov/sites/default/files/2024-12/Regulatory-and-Manufacturing-Consulting-for-Life-Sciences.pdf |
| the Claude Team plan for scientists: Premium seats at $15 a month for a verified PI's group, "Annual billing available ($0 / $180 per seat)", the price held for 12 months from sign-up; card payment only | https://claude.com/programs/team-plan-for-scientists and https://support.claude.com/en/articles/16634237-claude-team-plan-for-scientists (the 12 months); https://support.claude.com/en/articles/12997503 (cards only) |
| Claude Pro at $20 a month | https://claude.com/pricing (read directly) |
| Anthropic's AI for Science program: up to $50,000 in API credits per project, any researcher eligible (the help article's older "up to $20,000 ... for a 6-month period" predates it; no duration is given for the new ceiling); the program's terms ask the institution to let Anthropic use data made with the credits, model training included | https://www.anthropic.com/news/expanding-support-for-scientists (August 27, 2026) and https://support.claude.com/en/articles/11199177-anthropics-ai-for-science-program |
| poster at $6 a square foot, School of Medicine Medical Communications | https://medcom.med.wayne.edu/large-format-substrates |


References [1] to [16] and the claims tied to them were checked on 2026-10-14 against search excerpts and the
repository's earlier full-text readings (`01_carm_level_detection/docs/research/BIB_RESOLVE_2026-09-22.json`): [12]
now cites ICML 2025; DeepDRR [15] is credited with the physics and SyntheX [16] with the strong domain randomization,
whose hip-landmark parity rests on 366 cadaver images from six specimens; [1] counts patients, not operations; [2]
and [3] surveyed neurosurgical societies; the cohort's ten abstracts were submitted, not reported accepted. Still to
check by hand: the first author's initial in [4] and the Zenodo page of [8]. The FICA rate of line A2 is the
employer's statutory share, Social Security 6.2 % and Medicare 1.45 % (IRS Publication 15,
https://www.irs.gov/publications/p15).

## 3. What only the team can supply (the red [DATA NEEDED] marks)

1. The PI's office and phone (the filled `contacts.tex` gives the department office until then).
2. That the PI's appointment is tenure-track (the call requires it) and the ESI end date in eRA Commons.
3. That the PI leads no other AIDaS proposal this cycle.
4. The 2027 cohort: eight trainees in two waves of four (Aim 2 and the evaluation table).
5. The PI's tenure timing and earlier CAREER competitions, for the CAREER plan.
6. The PI's part in the consortium's work so far, and since when (the team paragraph).
7. Effort: the PI's and the Co-PI's percentages, in kind.
8. Budget: the Body Bequest fee (B1) and its terms for public release of the images; the CT facility and rate (B2);
   DLAR's rate and that Room 0312 Elliman takes human specimens (B3); the OEHS fee (B4); the C-arm's model and video
   output (B5); WSU's job category and scale for line A; the P-card route and the PI's verification for the Team
   plan (C1); that AIDaS applies no F&A; and the AIDaS office's answer on lines B, D and F.

## 4. Open items and caveats for the owner

- **Allowability.** The call lists graduate student support, computing, invited collaborator travel and data
  management. Lines A, A2, C1 and C2 fit and total $10,277; lines B, D and F do not obviously fit and are for the
  AIDaS office to confirm. Without B the request is $13,349; without B and D, $10,349; without B, D and F, $10,277,
  still above the $10,000 floor. Line A2 budgets FICA at 7.65 % for a hire who is not an enrolled student; a
  student assistant's composite rate is 1.7 %, and the difference, about $464, buys about 30 more hours. The
  sensitivity: at $18 an hour line A makes the total $20,247, over the cap unless the hours fall to 507; at $20,
  $21,367, and 456 hours at most.
- **The data behind the fold models.** Rows A5.1 and A5.3 (Figure 4a's coupled point and the stop signal) come from
  the C-ArmLSpine fold models, whose training banks hold 2,632 VinDr crops and 2,100 FluoroCap crops; the catalog's
  A3 header called that a breach of data directive D1 and of the IRB's scope. The owner settled it on 2026-10-14:
  "I don't understand why I would exclude vindr amd fluorocap. Just do whatever gets better results", and "I've
  gotten permission to use any and all data and filled out all data use agreeement forms". The packet therefore
  quotes the stronger result for each question, and the catalog and `DATASET_USAGE.md` say the matter is settled.
  Asked whether rule 9 should change, the owner answered "No I don't think fluorocap will help": FluoroCap stays out
  of new training. Rows A2.1, A2.2 and A9.2 come from the v9 encoder, whose training sample holds neither set
  (`DATASET_USAGE.md` section 1, item 4), and the catalog raises no such note on the A6 detector rows.
- **Disclosure** (root CLAUDE.md rule 8). The packet describes SchwingNet: Figure 3a is its architecture and the
  narrative quotes its held-out results; paper 1 is held pending the technology-transfer office. Run
  `ssn:tools/disclosure_audit.py` before sending, and decide what the AIDaS reviewers may see.
- **The MIT release** of the agent and its benchmark is the owner's call, with only the tasks a disclosure review
  clears.
- **Changes made by design**, against the letter of a review finding: H2 is a within-trainee crossover on two
  matched starter tasks, estimated with 95 % intervals, in place of `REVIEW_2026-10-14.md` item 26's six one-tailed
  tests, which eight trainees would pass together with a probability of about a third; Figure 1 drops the
  `fig1a_problem` cartoon that item 23 kept, for the trainee's route, the repair loop and the sixth lumbar vertebra;
  Foundational AI stays the primary area, framed as the reliability of agentic systems, where the compliance
  review of 2026-10-14 suggested leading with AI for Health; and line E is written by the PI in kind, where item 35
  gave it 8 of Aim 1's hours.
- **The writing review's edits** (`review/r6_panel_writing.md`), applied 2026-10-15, with three taken another way:
  N6n keeps the catalog's word, "on truth rebuilt after that scoring", since no file records that the rebuild of
  the C-ArmLSpine truth corrected labels (row A6.5 says only "re-scored on the rebuilt truth"); H3x is applied,
  so H3 promises 97 % "on each held-out C-arm", which still covers DeepFluoro (74.7 % at 0.74 today, row A6.10)
  and leaves out COBRA's Elekta imaging (6.2 %, row A6.9), a hypothesis for after Aim 3's work, not a result; and
  the note under the evaluation table was cut to one line ("None is a powered test; each sizes the CAREER,
  CyberTraining or R21 proposal") to give page 4 a line of room, which drops the clause that the cadaver set tests
  real anatomy against CT truth, said in Aim 3 already. A8 is added to the CAREER item. The adversarial review of
  those edits (2026-10-15) found every number matching this record and changed wording only: the hidden check is
  "unseen by the agent" (arm was used before its definition); the C-arm detector "will learn" corners (the
  existing one boxes bodies); A8 says Aim 1's tasks "include" Aim 3's experiments (the benchmark also draws on the
  consortium's lists); the note under the table no longer says H3 sizes the R21 (its 99 patients come from planning
  values, row E.4); "DLAR, which books the room" is dropped, since no file records who books it; Figure 3b's
  magnification label moved off the panel's line; Figure 1c says "scale bars" (the radiograph's is black); Figure 4b's
  title says "a new C-arm", as its caption does.
- **The Gaussian renderer** is framed as built on the PI's Gaussian-splatting work; the PI should confirm that
  framing and references [13] and [14].
- **Line E** asks Anthropic's AI for Science program for API credits; the laboratory works without API keys, so the
  credits would run only the benchmark's extra repeats, on the program's terms. Those terms ask the institution to
  let Anthropic use data made with the credits, model training included, so the repeats would run only tasks whose
  data agreements allow it (the packet says "on tasks its data terms allow").
- **The R21's mechanism.** The parent R21 (PA-25-304) allows no clinical trial and NIBIB's EBRG (PAR-25-321) makes one
  optional, so a validation that reaches patients' care fits PAR-25-321; earlier Trailblazer calls discouraged
  preliminary data, which the alignment page plans to bring.
- **Reference [9]** is cited without its author list, since rule 12 keeps student names out of this repository; add
  the authors in Overleaf if wanted.
- **Federal wording.** EO 14434 (September 29, 2026), "Inaugurating the Era of Super Intelligence", has agencies
  write "Super Intelligence" and "SI" in place of "AI" in their own documents. It binds agencies, not applicants, so
  the AIDaS packet keeps "AI" and the CAREER and R21 drafts may echo a solicitation's own words without having to.
- **The literature grounding and the pending protocol** (added 2026-10-15, section 6). The packet says Scopus is
  confirmed and ScienceDirect waits on an amendment: ask the library to add the text and data mining amendment to
  WSU's ScienceDirect agreement with Elsevier's account manager, and confirm before sending that Elsevier has enabled
  the Scopus APIs on the key. The key is one person's; the agent queries the index on the grid, never the API, and
  the index stays outside the MIT release. The protocol IRB-26-03-8648 is in draft on the IRB's side (pre-reviewed
  2026-09-28, expedited review requested): the packet calls it pending and promises nothing from it within the award;
  if it is approved or submitted before the deadline, say so on the cover and the alignment page. The protocol's own
  text calls the consortium's benchmark neurosurgical in two places; the packet does not (root CLAUDE.md rule 1).
- **The figures.** Figure 2a is redrawn as vector boxes from the labels of the extension's own store diagram, and
  Figure 2b crops the popup's top half, which shows no grid login; the VS Code edition's diagrams have labels that
  overlap at print size and are not used.

## 5. The execution skeleton

`autonomous_spine_agent.py` beside this file is the mock of Aim 1, standard library only: a grid simulator with the
WSU grid's partitions and quality-of-service rules that refuses what the real scheduler refuses; a mock language
model that drafts a job with a planted mistake and repairs it from the scheduler's message or the traceback; the
agent loop with gates registered by hash; and a placeholder evaluation with the C-arm projection matrix. Run
`python3 autonomous_spine_agent.py --selftest`, then `--tasks 6 --seed 0 --root <repository> --out run.json`, on a
laptop or as an sbatch job, never on the login node. Its numbers are simulated and appear nowhere in the packet as
results.

## 6. The two sources of 2026-10-15, kept out of git

Both were given to the grant thread on 2026-10-15 and neither enters the repository (root CLAUDE.md rule 12: the
correspondence carries addresses, the form a CV); the facts the packet takes from them are these.

- **Elsevier's answer on text and data mining** (correspondence of 2026-10-15). What was asked: non-commercial
  academic research on spinal disease; a retrieval-augmented system in which spine-related articles are split into
  passages and indexed, a question retrieves the most relevant passages, shown as short verbatim quotations with the
  full citation and a DOI link to the version of record, and a language model uses them as context beside the output
  of the consortium's own X-ray models; no Elsevier content trains, fine-tunes or improves any model; everything hosted
  on WSU's grid in access-controlled storage, nothing shared outside WSU, only brief quotations with citation and DOI
  in anything published; the index and the full text deleted when the project ends or the key lapses. The answer:
  Scopus approved, WSU's Scopus agreement including text and data mining and AI usage rights, the Scopus Search,
  Abstract Retrieval and Citation Overview APIs being enabled on the institutional key; ScienceDirect not yet, since
  WSU's ScienceDirect agreement has no text and data mining amendment, which the library or procurement adds with
  Elsevier's account manager. In the packet: the cover's strategic-areas line and abstract, Aim 2's grounding
  sentence, and the clinical collaborator's roles.
- **The pending IRB protocol** (the IRB form's print view of 2026-10-15, protocol IRB-26-03-8648, Wayne State IRB):
  "Creation of a Secure Multimodal Clinical and Radiographic Spine Surgery Dataset for Case-Control Research and
  Locally Hosted AI Development"; study type medical, expedited review requested; "Date Submitted: Draft", created
  2026-03-23, department certification 2026-03-30, pre-reviewed 2026-09-28; the clinical collaborator as Principal
  Investigator with a faculty sponsor, co-investigators the consortium's members; no funding; proposed 2026-05-01 to
  2029-05-01; retrospective, a waiver of consent and of HIPAA authorization requested; about 4,000 adult patients who
  had spine surgery at a Detroit Medical Center facility in the last ten years, with imaging (primarily CT) in PACS and
  operative notes, clinical notes and radiology reports in the EMR; coded data with the key in REDCap, NIfTI
  conversion, all 18 identifiers removed from the final dataset, storage on the WSU grid, kept seven years; 15 percent
  (about 600) double-coded; pseudolabels verified by supervised medical students; a locally hosted multimodal model
  trained only on the grid; a de-identified restricted-access release under a data use agreement. In the packet: the
  abstract, section 4's sentence on the R21's clinical data, and the alignment page's R21 item and team paragraph,
  each saying "about 4,000", "ten years", "de-identified CT paired with operative notes and radiology reports" and
  "pending", nothing more.
