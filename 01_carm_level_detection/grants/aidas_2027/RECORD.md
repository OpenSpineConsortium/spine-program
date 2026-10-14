# The AIDaS packet's record: where each number comes from, what the web settled, what is open

`latex/main.tex` is the packet; this file is what stands behind it and is not submitted. Until 2026-10-14 the packet
itself was this markdown (`AIDaS_SEED_2027_packet.md`, pull requests #91 and #93); the LaTeX source replaced it in
the pull request that closes issue #94, which also applied every finding of `REVIEW_2026-10-14.md`. Paths are
relative to spine-program; the record folders (`results/`, `figures/`, `manuscripts/`, `regulatory/`) live on the
grid and are read here from git history at main 5597197 (`ARCHIVE.md`).

## 1. The file behind every number in the packet

| number in the packet | file |
|---|---|
| 0.12 % wrong-level surgery in a 27-hospital registry of 34,544 degenerative operations, 0.42 % thoracic [1] | `09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md` (Furuya 2026) |
| about half of responding US spine surgeons report a wrong-level operation [2,3]; 17 % of reported events led to legal action or settlement [2] | the same file (Mody 2008, 73 of 418 events; Groff 2013) |
| median payment for a surgical never event, $75,220 [4] | the same file (Bettis 2026, NPDB, 2025 dollars) |
| 12.9 % of 550 surgical patients had a transitional vertebra; miscounted in clinic in 54 % [5] | `02_transitional_naming_truth/docs/LEVELCHECK_CLAIM.md` (Nakagawa 2017) |
| LevelCheck: 4.7 s per image on a 2012 graphics card, 17 to 72 s in an operating room, against 20 s to one minute [6-8] | `01_carm_level_detection/docs/MODEL_CARD.md` section 6 (`levelcheck2012`, `manbachi2018`, `desilva2016`) |
| CTSpinoPelvic1K: 802 CTs, release 11, Zenodo 10.5281/zenodo.22797014 [9] | `03_ctspinopelvic1k_dataset/README.md` |
| 7,045 and 1,482 annotated physics renders | `08_render_devices/README.md` (the 7,045 include 1,321 renders of synthetic-implant CTs) |
| 142 TotalSegmentator spines styled per device; 12,730 styled training entries | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` (devcorpus; design P) |
| C-ArmLSpine: 149 cases; 617 lateral and 631 AP bodies; automatic truth from two CBCT labelers agreeing | `01_carm_level_detection/docs/MODEL_CARD.md` section 5.1; `docs/handoff/RESULTS_CATALOG.md` rows A2.1, A2.2 |
| YOLO11m detector; ResNet-18 encoder; two-layer bidirectional GRU; 27 levels | `01_carm_level_detection/docs/MODEL_CARD.md` (the model table); Figure 3a is `figures/schwingnet/fig1c_arch.pdf` at 5597197 |
| 0.1915 mm per pixel at SID 1,140 mm and SOD 745 mm, so 1.53 times larger on the detector | `01_carm_level_detection/docs/MODEL_CARD.md` section 6.1 |
| 96.4 % of 617 lateral bodies with no C-arm frame in training (595 / 617, Wilson [92.3, 98.4]) | `RESULTS_CATALOG.md` row A2.1 |
| 43.7 % of 631 AP bodies (276 / 631, [34.9, 51.9]) | row A2.2 |
| AP with the device's own frames, 96.4 % (608 / 631, [92.5, 98.3]) | row A3.2 |
| count and shape coupled, 98.2 % of 1,009 bodies on frames holding the sacrum ([96.5, 99.5]) | row A5.1 |
| stop signal on 9.9 % of 233 anchored frames, catching 5 of the 6 that err | row A5.3 |
| detector on the held-out C-ArmLSpine at 0.74: 80.5 % (231 / 287, [74.1, 86.8]) | row A6.1 |
| the same at 0.25: 90.6 % (260 / 287) | row A6.2 |
| styled renders and two devices' real frames, 63.1 % (181 / 287) | row A6.11 |
| renders only, 0.3 % (1 / 287) | row A6.12 |
| the pre-stated 97 %, met by no held-out cell | row A6.13 (`ssn:docs/RSNAI_PLAN.md` C7) |
| styled renders 99 to 100 % separable from real frames | row A13.3 |
| 35 persons with no error for a 90 % lower bound | row E.2 |
| the 2026 cohort: 16 students, seven with no coding, eleven with no imaging experience, ten sub-projects active at the survey, all ten submitted as abstracts, all 16 would recommend; Table 1's six domains before and after, one-tailed Wilcoxon | Cureus 2026;18(7):e112661 [13], the PDF under `11_students_grid_access/manuscripts/` at 5597197 |
| the grid's H200 partition, 4 nodes of 4 GPUs | `11_students_grid_access/docs/handoff/EXTRACTS_11.md` (gmsap) |
| the co-investigators' four joint papers (2021 to 2024) with the clinical collaborator; the PI's Gaussian-splatting and implicit-surface papers; the PI's PhD of November 2017 and appointment since 2021 | the two biosketches (submitted with the packet, not committed) |

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
| the PI: Assistant Professor of Computer Science; at Wayne State since January 2021; founding director of the Machine Perception Lab | https://engineering.wayne.edu/profile/hg0137 and https://h312h.github.io/ |
| the Co-PI: Professor since 2021, chair 2014 to 2022; GPU acceleration of scientific codes | https://engineering.wayne.edu/profile/aa4760 |
| the cover's contact lines (in `latex/contacts.tex`, never committed) | the department directory, https://engineering.wayne.edu/about/directory.php?group=1117, and https://wayne.edu/people/aa4760 |
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
| capital equipment threshold $5,000 | https://policies.wayne.edu/appm/6-property-and-capital-equipment |
| C&IT hosted storage $40 per 100 GB a year, so $400 per TB | https://services.wayne.edu/TDClient/277/Portal/KB/Article/20343 |
| the grid's compute is free to WSU researchers | https://services.wayne.edu/TDClient/277/Portal/KB/Article/20229/Grid-FAQs |
| the Body Bequest donor authorization permits de-identified images | https://bodybequest.med.wayne.edu/docs/bbp_brochure.pdf |
| the C-arm in Room 0312 Elliman; dosimetry badges at DLAR's director 15 business days ahead | https://research.wayne.edu/oehs/rad-safety/xray-imaging |
| Magewell USB Capture AIO, $619 list | https://www.fullcompass.com/prod/600750-magewell-usb-capture-aio-usb-capture-aio |
| an OEC 9900's live output is BNC; its DVI output carries review images | https://www.blockimaging.com/oec-9900-how-to-add-an-extra-real-time-image-monitor |
| a mid-level regulatory consultant, about $200 to $400 an hour (the packet uses $300) | https://seed.nih.gov/sites/default/files/2024-12/Regulatory-and-Manufacturing-Consulting-for-Life-Sciences.pdf |
| the Claude Team plan for scientists: Premium seats at $15 a month for a verified PI's group; card payment only | https://claude.com/programs/team-plan-for-scientists and https://support.claude.com/en/articles/12997503 (both read directly) |
| Claude Pro at $20 a month | https://claude.com/pricing (read directly) |
| Anthropic's AI for Science program: up to $20,000 in API credits for six months | https://support.claude.com/en/articles/11199177-anthropics-ai-for-science-program (read directly) |
| poster at $6 a square foot, School of Medicine Medical Communications | https://medcom.med.wayne.edu/large-format-substrates |

## 3. What only the team can supply (the red [DATA NEEDED] marks)

1. The PI's office and phone (the cover gives the department office until then).
2. That the PI's appointment is tenure-track (the call requires it) and the ESI end date in eRA Commons.
3. That the PI leads no other AIDaS proposal this cycle.
4. The 2027 cohort: eight trainees in two waves of four, and the IRB determination's HPR number.
5. Effort: the PI's and the Co-PI's percentages, in kind.
6. The PI's tenure timing and earlier CAREER competitions, for the CAREER plan.
7. The reissued parent R21 notice, once NIH publishes it.
8. Budget: the Body Bequest fee and its terms for public release of the images (B1), the CT facility and rate (B2),
   DLAR's rate and the C-arm's model and live output (B3, B5), the OEHS fee (B4), WSU's job category and scale for
   line A, the P-card route and the PI's verification for the Team plan (C1), and whether AIDaS applies F&A.

## 4. Open items and caveats for the owner

- **Allowability.** The call lists graduate student support, computing, invited collaborator travel and data
  management. Lines A, C1 and C2 fit; lines B, D and F do not obviously fit and are for the AIDaS office to confirm.
  Without B the request is $13,349; without B and D, $10,349; without B, D and F, $10,277, still above the $10,000
  floor. The sensitivity: at $18 an hour line A makes the total $20,247, over the cap unless the hours fall to 507;
  at $20, $21,367 and 457 hours.
- **Disclosure** (root CLAUDE.md rule 8). The packet describes SchwingNet: Figure 3a is its architecture and the
  narrative quotes its held-out results; paper 1 is held pending the technology-transfer office. Run
  `ssn:tools/disclosure_audit.py` before sending, and decide what the AIDaS reviewers may see.
- **The MIT release** of the agent and its benchmark is the owner's call, with only the tasks a disclosure review
  clears.
- **The fold models** behind rows A3.2, A5.1 and A5.3 (Figure 4a's last two points and the stop signal) were
  fine-tuned on banks built from `allspine_v7` that hold 2,632 VinDr crops and 2,100 FluoroCap crops; the catalog's
  A3 header says "the composition breaks directive D1 and the IRB scope", though it marks the rows CURRENT and HELD
  OUT. Rows A2.1 and A2.2 come from the v9 encoder and head and the A6 rows from the detector arms, and the catalog
  raises no such note on them. Whether the packet quotes the three is the owner's call; without them it keeps the
  zero-shot and held-out-device results.
- **The Gaussian renderer** is framed as built with the PI's Gaussian-splatting methods; the PI should confirm that
  framing and the references [11] and [12], which were written from memory and not checked against the papers.
  SWE-bench [10] likewise.
- **Line E** asks Anthropic's AI for Science program for API credits; the laboratory works without API keys, so the
  credits would run only the benchmark's extra seeds, on the program's terms.
- **Reference [13]** is cited without its author list, since rule 12 keeps student names out of this repository; add
  the authors in Overleaf if wanted.
- **Federal wording.** EO 14434 (September 29, 2026) has agencies write "Super Intelligence" and "SI" in place of
  "AI" in official documents; the AIDaS packet is internal and keeps "AI", but the CAREER and R21 drafts may need it.
- **The VS Code edition's diagrams** (the setup wizard, the job topology) have labels that overlap at print size, so
  the figures use the browser extension's own store artwork.

## 5. The execution skeleton

`autonomous_spine_agent.py` beside this file is the mock of Aim 1, standard library only: a grid simulator with the
WSU grid's partitions and quality-of-service rules that refuses what the real scheduler refuses; a mock language
model that drafts a job with a planted mistake and repairs it from the scheduler's message or the traceback; the
agent loop with gates registered by hash; and a placeholder evaluation with the C-arm projection matrix. Run
`python3 autonomous_spine_agent.py --selftest`, then `--tasks 6 --seed 0 --root <repository> --out run.json`, on a
laptop or as an sbatch job, never on the login node. Its numbers are simulated and appear nowhere in the packet as
results.
