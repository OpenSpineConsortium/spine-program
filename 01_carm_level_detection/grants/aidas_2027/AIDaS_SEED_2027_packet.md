<!-- AIDaS SEED 2026-2027 proposal packet. One markdown, exported to one PDF by build_pdf.sh. Every
[DATA NEEDED] tag is a value the investigators supply before submission; the appendix lists them. -->

# 2026-2027 AIDaS Seed Grant Program: proposal

**Project title.** Self-repairing agentic pipelines on the Wayne State grid: from labelled CT to real-time C-arm level localization, with medical trainees as the workforce

**Strategic areas addressed.** 1, Foundational AI (primary); 3, AI for Education and Workforce Training; 4, AI for Health

**Principal Investigator.** Zhizhong Han, PhD, [DATA NEEDED: rank], Department of Computer Science, College of Engineering, Wayne State University [DATA NEEDED: department code]. AIDaS affiliation: [DATA NEEDED: confirm membership, or request it before submission]. Contact: [DATA NEEDED: office, phone, e-mail].

**Co-Principal Investigator.** Loren Schwiebert, PhD, [DATA NEEDED: rank], Department of Computer Science, College of Engineering, Wayne State University [DATA NEEDED: department code]. Contact: [DATA NEEDED].

**Clinical collaborator (receives no award funds).** Gregory Schwing, MD, PhD, General Surgery (Wayne State University School of Medicine / Detroit Medical Center): the Open Spine Consortium record this proposal builds on (the spine-program repository, the CTSpinoPelvic1K dataset, the C-arm detector and the trainee program).

**External collaborators.** Detroit Medical Center imaging staff take part in the cadaver imaging session of Aim 3. No award funds reach an external organization.

**New Investigator status.** PI: [DATA NEEDED: tenure-track Assistant Professor, appointment start date]. Co-PI: [DATA NEEDED].

**Amount requested.** $18,057 over 12 months (January 1, 2027 to December 31, 2027).

**Abstract.** Wrong-level spine surgery persists because the intraoperative C-arm exposure is read by a person counting vertebrae from a landmark the field may not hold. The Open Spine Consortium at Wayne State has built, in the open, a dataset of 802 CTs with every vertebra labelled, a renderer that turns those CTs into device-faithful C-arm frames, and a detector that names the lumbar level on 97.4 % of 617 held-out lateral bodies. This seed project turns that record into three linked advances. Aim 1 builds an autonomous code-generating agent that reads the repository, writes and submits its own grid jobs, and repairs scheduler refusals and runtime exceptions without a person, under gates registered before any job runs. Aim 2 puts that agent in the hands of medical trainees on the WSU high-performance computing grid and measures what they can do with it against a published 2026 cohort. Aim 3 carries the CT-trained 3-D structure into 2-D fluoroscopy as low-latency bounding boxes and corner keypoints, measured per exposure on a held-out device and on a paired CT and X-ray cadaver set imaged at WSU/DMC. Deliverables within the year: the agent and its benchmark, a trainee cohort with measured outcomes, the cadaver set, an FDA Pre-Submission draft, and NSF CAREER and NIH R21 submissions.

**Keywords.** agentic systems; code generation; high-performance computing; medical education; fluoroscopy; keypoint detection; domain transfer; spine surgery

# Project narrative

## 1. Significance and innovation

Spine surgery takes its level from the intraoperative C-arm exposure, where a person counts vertebrae from a landmark. The count fails often enough to matter: wrong-level surgery occurs in 0.12 % of degenerative spine operations in a national registry (0.42 % in the thoracic spine), about half of US spine surgeons report at least one in their career, 17 % of events reach litigation, and the pooled median malpractice payment for a surgical never-event is $75,220. Transitional anatomy defeats the count: a lumbosacral transitional vertebra is present in 12.9 % of surgical patients and miscounted in 54 % of them. The existing aid, LevelCheck, registers the preoperative CT to the exposure in 4.7 s per image and 17 to 72 s in an operating room, longer than surgeons say they will wait.

Three obstacles stand between the laboratory's record and a device, and they are one obstacle: labelled 3-D anatomy must be carried into 2-D at interactive speed; the experiments that get it there need hundreds of grid jobs written, submitted and repaired, which is where a laboratory's time goes; and the trainees who hold the clinical question cannot write those jobs. The innovation is one loop (Figure 1): an agent that writes, submits and repairs grid jobs under gates registered before the job runs (Aim 1), driven by trainees (Aim 2), on the imaging pipeline (Aim 3). Aim 1 treats the scheduler as part of the runtime: a refused submission, a wrong quality-of-service string, an out-of-memory kill and a Python traceback are one kind of exception, read from the job's log and repaired in the job script, and nothing is quoted until its pre-registered gate passes. Agent benchmarks measure edits on one machine; none we know of measures an agent against a shared scheduler under a budget. Aim 3 names each vertebra from its own shape, uses the count only as a check and abstains where they disagree, trains on renders styled per device so that one held-out device is a true transfer test, and reaches low latency by one detection pass with no registration.

![Figure 1. The key idea. (a) An agent reads the repository, registers a gate, writes and submits a Slurm job, and repairs refusals and exceptions without a person. (b) A medical trainee drives that agent as a worker on the WSU grid. (c) The pipeline it extends names the level on a C-arm exposure under pre-stated gates.](figures/fig_key_idea.png){width=6.6in}

## 2. Specific aims

**Aim 1 (Foundational AI). An autonomous code-generation agent for the grid.** Build and benchmark an agent that parses the repository's files, generates script extensions, submits them as Slurm jobs on the WSU grid and corrects API and runtime exceptions without human intervention. Hypothesis H1: with the repair loop and pre-registered gates the agent passes at least 80 % of a 40-task benchmark with zero interventions, against at most 40 % for the same model in one shot.

**Aim 2 (Education and workforce). Medical trainees drive the agent on the HPC grid.** Enrol [DATA NEEDED: n] medical students and residents, each running the Aim 1 agent as a worker in their own grid account and owning one pre-registered sub-project that lands by pull request. Hypothesis H2: six-domain comfort gains at least as large as the 2026 cohort's, and a median time to first successful GPU job under seven days.

**Aim 3 (Health). CT-trained 3-D structure to 2-D C-arm fluoroscopy at low latency.** Carry the labelled 3-D structure of 802 CTs into fluoroscopy as a one-pass detector (a bounding box and four corner keypoints per vertebra and sacrum), a level encoder, and a projection model that ties each 2-D box to its 3-D body. Hypothesis H3: 97 % vertebra detection on a held-out device, under 1 s per exposure on one GPU, and at least 95 % exact level on the paired cadaver frames.

## 3. Approach and preliminary work

**Aim 1.** The agent is a Claude Code worker under the laboratory's claim protocol (one issue, one branch, one pull request, the plan stated before the first change). It runs the loop of Figure 1a: read the repository's instructions, task list and results catalog; register the rule, gate and input hashes; write the job script; submit; read the log; repair until the gate passes; open the pull request. The benchmark is 40 tasks from the repository's own task lists (figure rebuilds, render banks, detector fine-tunes, morphometric tables), each with a pre-stated gate, 10 for development and 30 sealed; three arms share one model and one budget: single shot, repair loop, repair loop with gates. Preliminary work: the laboratory's workers already run as Slurm jobs through the Beethoven extension, and the execution skeleton delivered with this proposal (autonomous_spine_agent.py) runs the loop against a simulated scheduler with the grid's real partitions and refusals: six of six mock tasks pass after eight repairs and two refusals with no intervention, a design check rather than a result.

**Aim 2.** Trainees come from the Open Spine Consortium's student program [DATA NEEDED: IRB number or exemption]. Each receives a grid account, the Beethoven extension, which starts Claude Code as a Slurm job in the trainee's own account, and one sub-project registered as an issue with its gate; the agent writes and repairs the jobs, and the trainee owns the question, the results and the pull request, which a mentor reviews. The six-domain instrument of the 2026 study is given before and after. Preliminary work (Cureus 2026;18(7):e112661): 16 students, seven with no coding and eleven with no imaging experience, completed ten sub-projects on the grid, whose GPU partition offers 4 nodes of 4 H200; all six domains improved (Wilcoxon, all p < 0.05; CT interpretation 1.81 to 3.31 and Python 1.31 to 2.56 on a five-point scale, each p < 0.001); all ten projects were submitted to a national meeting; 16 of 16 would recommend the program.

**Aim 3.** Data: CTSpinoPelvic1K (802 CTs with every vertebra, the sacrum and the hips labelled; Zenodo 10.5281/zenodo.22797014), rendered per device card into 7,045 standard and 1,482 transitional annotated C-arm frames, and real frames from three devices (C-ArmLSpine, 141 cases with 617 lateral and 631 AP bodies; DeepFluoro; COBRA Elekta). Model: a YOLO11m-pose detector (a box and four corners per body), a ResNet-18 level encoder with a BiGRU over the column, a count from the detected sacrum, and the coupling that abstains when count and shape disagree. From 3-D to 2-D: the projection matrix at the device's geometry (source-to-image 1140 mm, source-to-object 745 mm, 0.1915 mm per pixel) ties each CT's labelled bodies to their boxes in the render, so the training label is the 3-D structure's own silhouette, and the cadaver's CT gives its X-ray's truth by the same projection. The cadaver set: [DATA NEEDED: n] specimens through WSU's Body Bequest Program, CT, then AP and lateral exposures at DMC at the protocol's three or four lumbar and six or seven thoracic positions, sealed by hash. Preliminary results, all held out (Figure 2; the results catalog): exact lateral level 601 of 617 bodies (97.4 %, Wilson [93.2, 99.0]) fine-tuned and 595 of 617 (96.4 %) zero-shot from renders alone; AP 608 of 631 (96.4 %); count and shape coupled 991 of 1,009 (98.2 %); the stop signal fires on 9.9 % of frames and catches five of six erring ones. Detection on a device never trained on is 231 of 287 bodies (80.5 % [74.1, 86.8]), short of the pre-stated 97 %, and device-styled renders stay 99 to 100 % separable from that device's real frames: that gap is what Aim 3 funds. The stack's end-to-end latency has not been measured; Aim 3 measures it first.

![Figure 2. Preliminary data. (a) The count is the problem: one extra thoracic body shifts every name counted from the anchor. (b) The corpus manifold of 11,638 frames from 18 sources: devices stay separable, so a held-out device is a real transfer test. (c) Held-out results with 95 % Wilson intervals; orange: the device never trained on.](figures/fig_preliminary_data.png){width=6.9in}

## 4. Evaluation: data, metrics and experiment design

| Aim | Data | Metrics | Design | Gate, stated before the run |
|----|-------------|------------------------|---------------|------------------|
| 1 | 40 repository tasks with gates: 10 development, 30 sealed | pass rate; repairs per task; human interventions; rule violations (login-node run, wrong QoS, credential in a file); GPU-hours and dollars per pass | three arms, one model, one budget, three seeds; paired bootstrap over tasks | 80 % pass, 0 interventions, 0 violations on the 30 sealed tasks; single shot as the control |
| 2 | 2027 cohort (n = [DATA NEEDED]); 2026 cohort (n = 16) | six-domain Likert before and after (one-tailed Wilcoxon); time to first successful GPU job; tasks passed without a mentor; projects reaching a pull request and an abstract | prospective cohort, same instrument, historical control; analysis plan registered before enrolment | gains at least the 2026 cohort's in all six domains; median first GPU job within 7 days |
| 3 | C-ArmLSpine (141 cases); DeepFluoro and COBRA Elekta frames; the render banks; the sealed cadaver set | per-frame exact level with a case-clustered Wilson interval; vertebra and sacrum recall at 0.74; corner error (mm); Dice and IoU of the projected silhouette; latency per exposure (median, p95); abstention rate | leave-one-device-out; the cadaver set opened once, after code and weights are hashed | 97 % detection on the held-out device; under 1 s per exposure on one H200; 95 % exact level on the cadaver frames |

Intervals are Wilson on the effective sample size, since frames cluster within cases. The cadaver set is the sanity test on real anatomy with CT truth; the powered tests are the held-out device and C-ArmLSpine, and the laboratory's power analysis (35 error-free persons for a 90 % bound) sets the R21's sample.

## 5. Expected outcomes, deliverables and timeline

Within the award period: (1) the agent, its 40-task benchmark and the three-arm report, under the MIT license; (2) the cohort's outcome report, the trainees' merged pull requests and abstracts; (3) the paired CT and X-ray cadaver set, deposited beside CTSpinoPelvic1K, with the leave-one-device-out and latency results in a manuscript; (4) the FDA Pre-Submission draft; (5) the CAREER and R21 submissions. Quarter 1: agent version 1, benchmark sealed, recruitment, IRB and imaging approvals. Quarter 2: benchmark run, cohort start, cadaver imaging, latency measured. Quarter 3: CAREER submitted, leave-one-device-out results, Pre-Submission drafted. Quarter 4: R21 submitted, cohort post-survey, cadaver set opened, final report and symposium. Risks: the agent's cost is bounded per task; a delayed specimen falls back to the phantom and the existing device frames; a held-out-device result under 97 % becomes the R21's first aim.

# AIDaS funding priority alignment

**National priorities.** The White House Office of Science and Technology Policy's national AI strategy [DATA NEEDED: cite the current OSTP document and date at submission] names agentic and trustworthy AI, AI-enabled science on national computing, and an AI-ready workforce. NSF's AI portfolio funds foundational agentic systems through its CISE core programs and the National AI Research Institutes; NIH's Strategic Plan for Data Science 2023-2028 and its Bridge2AI program fund AI-ready data and trustworthy clinical AI. The three aims map onto those priorities: Aim 1 is an agentic system held to verifiable gates, Aim 2 trains Michigan's medical workforce on a national-class grid, and Aim 3 is medical imaging AI with a regulatory pathway opened during the award.

**Target agencies, programs and solicitations.**

1. NSF Faculty Early Career Development Program (CAREER), CISE/IIS Robust Intelligence, PI Zhizhong Han [DATA NEEDED: current solicitation number]. Research plan: Aim 1 and the 3-D-to-2-D learning of Aim 3; education plan: Aim 2 as a sustained trainee program. Submission: the July 2027 deadline [DATA NEEDED: confirm the date and the PI's eligibility: untenured Assistant Professor at the deadline, no prior CAREER award].
2. NIH R21 through NIBIB: the Trailblazer Award for New and Early Stage Investigators [DATA NEEDED: current PAR number] or the parent R21, with the clinical collaborator's institution as the imaging site. Preliminary data: the cadaver set and the held-out-device result; the FDA Pre-Submission feedback shapes its validation aim. Submission: the standard due date of October 16, 2027 [DATA NEEDED: confirm against the PAR's own dates].
3. NSF Smart Health and Biomedical Research in the Era of Artificial Intelligence and Advanced Data Science (SCH, joint with NIH; NSF 23-614 or its successor [DATA NEEDED: current number and deadline]). The whole loop (agent, trainees, device) as a four-year project, submitted in the 2028 cycle once the CAREER and R21 reviews are in hand.

**New Investigator criteria.** The PI [DATA NEEDED: confirm] is a tenure-track Assistant Professor, which AIDaS gives priority and the CAREER requires. NIH's Early Stage Investigator status (within ten years of the terminal degree, no substantial independent NIH award) [DATA NEEDED: PI's degree year] qualifies the R21 for the Trailblazer mechanism. The Co-PI brings HPC systems and the grid relationship; the clinical collaborator brings the data record, the trainee program and the DMC imaging access, and receives no funds.

**Timeline for external submission.**

| When | Milestone |
|------------|------------------------------|
| January to March 2027 (months 1 to 3) | Program-officer contact at NSF IIS and NIBIB with a one-page concept; benchmark and gates sealed |
| July 2027 (month 7) | NSF CAREER submitted with the Aim 1 benchmark and the Aim 3 transfer results |
| October 16, 2027 (month 10) | NIH R21 submitted with the cadaver set, the latency measurement and the Pre-Submission feedback |
| December 2027 (month 12) | Project ends; AIDaS final report and symposium presentation |
| February to June 2028 (post-award months 2 to 6) | R21 summary statement; resubmission at the June 16, 2028 due date if needed |
| July 2028 (post-award month 7) | CAREER resubmission if not funded |
| By December 2028 (post-award month 12) | NSF SCH full proposal [DATA NEEDED: 2028 deadline], within 12 months of the project end as AIDaS requires |

# Budget and justification

| Line | Item | Basis | Amount |
|-----|----------------------|------------------------------|-------|
| A | Part-time post-baccalaureate researcher | 520 h at $15.00 per hour: Aim 1, 180 h; Aim 2, 160 h; Aim 3, 180 h | $7,800 |
| A2 | Fringe on line A | 7.65 % statutory [DATA NEEDED: WSU FY2027 part-time temporary rate] | $597 |
| B1 | Two cadaver specimens, WSU Body Bequest Program | [DATA NEEDED: program fee]; placeholder $1,250 each | $2,500 |
| B2 | Specimen CT, two scans | research rate [DATA NEEDED]; placeholder $300 each | $600 |
| B3 | C-arm suite and technologist, one session at DMC | 4 h at $300 [DATA NEEDED: DMC research rate] | $1,200 |
| B4 | Radiation safety: dosimetry and OEHS review | [DATA NEEDED: OEHS fee] | $300 |
| B5 | Frame grabber for the C-arm's video output | one unit, under the capital threshold | $450 |
| C1 | Claude subscription seats for the trainees' workers | 4 seats at $20 a month, 12 months [DATA NEEDED: count and plan] | $960 |
| C2 | Data management and storage: grid allocation and Zenodo deposit | [DATA NEEDED: WSU research storage rate] | $500 |
| D | FDA Pre-Submission preparation: regulatory consultant | 12 h at $250 [DATA NEEDED: rate]; FDA charges no Pre-Submission fee | $3,000 |
| E | Anthropic research-access (AI for Science) application | no application fee [DATA NEEDED: confirm]; hours in line A | $0 |
| F | Dissemination: AIDaS symposium poster | one poster | $150 |
| | **Total requested** | | **$18,057** |

- **Line A.** A part-time post-baccalaureate researcher, not a graduate research assistant: a GRA with tuition and benefits exceeds the whole award, and the work (running the benchmark, logging the cohort's measures, curating and de-identifying the cadaver set) is technician work at ten hours a week for 52 weeks. The rate is $15.00 per hour [DATA NEEDED: confirm against WSU's temporary research-staff scale]; hours are logged by aim; no tuition and no full-time GRA are requested.
- **Line A2.** Statutory fringe only; WSU's negotiated rate for this category replaces the placeholder [DATA NEEDED].
- **Lines B1 to B5.** A paired CT and X-ray set of the same anatomy exists in no public dataset, and it is the only test in which the X-ray's truth comes from a CT rather than a reader. Two specimens give AP and lateral exposures at every protocol position; the CT is the label, the C-arm at DMC is the deployment device, and the frame grabber captures the exposure as the device shows it, which is the deployment input. OEHS review and dosimetry are required for the session; each fee is a placeholder until quoted [DATA NEEDED].
- **Lines C1 and C2.** The trainees' workers run on Claude subscription seats, one per trainee, never on an API key, by the laboratory's rule; the WSU grid's compute is in kind. Storage covers the render banks and the cadaver set during the award and the Zenodo deposit at its end.
- **Line D.** FDA's Pre-Submission program charges no fee; the cost is a consultant's hours to prepare the package (device description, intended use, proposed testing) so that FDA's written feedback reaches the R21 before October 2027.
- **Line E.** Anthropic's research-access programs award compute credits with no application fee; the application is prepared on line A hours, and the $0 line keeps the request in the audit trail.
- **Line F.** Presenting at an AIDaS symposium is an award expectation.
- **Not requested.** PI and Co-PI salary, travel, tuition, capital equipment and indirect costs [DATA NEEDED: confirm AIDaS applies no F&A]. In kind: WSU grid compute, the collaborator's time and the existing datasets.
- **Allowability.** The call lists graduate student support, computing, invited collaborator travel and data management as allowable. Lines A, C1 and C2 fall under those headings; lines B and D are research costs the AIDaS office is asked to confirm before submission [DATA NEEDED]; a disallowed line is removed and the total falls, since no other line depends on it.

# Biosketches

Two pages per investigator in NSF or NIH format, appended as separate PDFs at submission [DATA NEEDED for each of the PI and the Co-PI: current position; education and training; five products most closely related to this proposal; five other significant products; synergistic activities; current and pending support; for NIH format, the personal statement and the contributions to science].

<!-- end of the submitted packet: build_pdf.sh stops here -->

# Appendix (not submitted): the execution skeleton, the sources and the open items

## The execution skeleton

`autonomous_spine_agent.py` beside this file is the mock of Aim 1, standard library only. It holds (1) a grid simulator with the WSU grid's partitions and quality-of-service rules that refuses what the real scheduler refuses (a login-node run, a GPU on the CPU partition, an invalid QoS, a working directory off the research volumes) and tracks memory, threads and the GPU queue; (2) a mock language model that drafts a job with a planted mistake and repairs it from the scheduler's message or the traceback; (3) the agent loop that reads the repository's TODO files, registers a gate by hash, submits, reads the log and repairs until the gate passes; and (4) a placeholder evaluation loop with the C-arm projection matrix at the device's geometry that computes Dice and IoU of projected silhouettes, corner error in mm and exact-level rate with a Wilson interval. Run `python3 autonomous_spine_agent.py --selftest`, then `python3 autonomous_spine_agent.py --tasks 6 --seed 0 --root <repository> --out run.json`. The numbers it prints are simulated and are quoted nowhere above as results.

## Sources of the numbers above

Every number in the packet names its file here; the repository paths are relative to spine-program at the commit this packet was written on, and the record material lives on the grid (ARCHIVE.md) with its copies in git history at main 5597197.

- Wrong-level incidence (0.12 %, thoracic 0.42 %), the surgeons' career rate, the litigation share and the NPDB median: 09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md and WRONG_SITE_BURDEN_EVIDENCE.md (Furuya 2026; Mody 2008; Groff; Bettis).
- LSTV prevalence and miscount: 02_transitional_naming_truth/docs/LEVELCHECK_CLAIM.md.
- LevelCheck timings and surgeons' waiting time: 01_carm_level_detection/docs/MODEL_CARD.md section 6 (levelcheck2012, manbachi2018, desilva2016); the unmeasured latency of the reported stack: the same section.
- Exact level, AP, zero-shot, coupling, stop signal, held-out device at 0.74 and 0.25, styled-render separability: 01_carm_level_detection/docs/handoff/RESULTS_CATALOG.md rows A3.1, A3.2, A2.1, A5.1, A5.3, A6.1, A6.2, A13.3; power: row E.2. Figure 2c draws rows A2.1, A3.1, A3.2, A5.1, A6.1 and A6.2 with their intervals.
- Geometry: MODEL_CARD.md section 6.1 (px_mm 0.1915, SID 1140, SOD 745, lumbar pitch 34 mm).
- CTSpinoPelvic1K: 03_ctspinopelvic1k_dataset/README.md (802 records, Zenodo 10.5281/zenodo.22797014, v11). Render banks: 08_render_devices/README.md (7,045 and 1,482 annotations). Corpus manifold: figures/schwingnet/figS1.caption.txt at 5597197 (11,638 frames, 18 sources). Real-frame banks: 01_carm_level_detection/docs/handoff/DATASET_USAGE.md (C-ArmLSpine, DeepFluoro, COBRA Elekta).
- The 2026 cohort: 11_students_grid_access/manuscripts/cureus_2026_e112661_Schehr_Kim_Schwing.pdf at 5597197 (Table 1 and the Results). The grid's GPU partition: 11_students_grid_access/docs/handoff/EXTRACTS_11.md.
- The mock run: autonomous_spine_agent.py with --tasks 6 --seed 0 on this repository.

## Open items before submission

1. Every [DATA NEEDED] tag above: ranks, department codes, contacts, AIDaS membership, New Investigator and ESI status, the IRB number, the cohort size, the specimen count and site, every placeholder fee, the fringe rate, the seat count, the solicitation numbers and dates, the OSTP citation, the F&A rule.
2. The AIDaS office's answer on lines B and D.
3. Biosketches, two pages each.
4. The disclosure audit the repository requires before any submission (CLAUDE.md rule 8), since the narrative quotes level-identification results.
5. The deadline: October 16, 2026, 11:59 p.m. ET, as a single PDF to the AIDaS office.
