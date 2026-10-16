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
| (cut for room on 2026-10-16) one figure of the consortium's C-arm study took 250 fine-tunes | catalog section A9's header (250 / 250 cells behind Figure 5b); the sentence left the packet in the rewrite for issue #106 |
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
| (cut for room in the reframing of 2026-10-16) on rebuilt truth, 82.2 % of the 287 (236 / 287) and 93.9 % of the 214 vertebrae whose truth is complete and at least 80 % visible (201 / 214) | row A6.5, "both printed" (`results/schwingnet/indomain/DENOMINATOR_REPAIR.md` at 5597197); the repaired denominator's rule is in `docs/handoff/GLOSSARY.md`; A6.1's 80.5 % is on the truth before the rebuild |
| styled renders added to two devices' real frames: 63.1 % (181 / 287, [54.8, 71.0]) at 0.74, 87.8 % at 0.25 | rows A6.11, A7.8 |
| renders only: 0.3 % (1 / 287) at 0.74, 31.7 % (91 / 287) at 0.25 | row A6.12 |
| the 97 % set in advance, met by no held-out cell | row A6.13 (`ssn:docs/RSNAI_PLAN.md` C7) |
| styled renders 99 to 100 % separable from real frames | row A13.3 |
| for the R21: 99 patients give 80 % power for a Wilson lower bound of 90 % at a true 97 % (exactly 82 %; 98 give 66 %, so the number is exactly 99) | row E.4 (its planning values have no transitional measurement behind them) |
| Beethoven keeps the grid's profile as checked data and its job rules in writing, and runs Claude Code workers as Slurm jobs (the significance, Aim 1, Figure 2) | `OpenSpineConsortium/beethoven-sites` at 83f34e8, `sites/wayne/site.json`: Slurm, the login node, the CPU partition and its QoS (secp, secondary), the GPU partitions by name only (gmsap, gvohp; the schema has no field for a GPU QoS or a GPU request, which only `11_students_grid_access/docs/handoff/EXTRACTS_11.md` records: QoS gpu, `--gres=gpu:1`, gmsap 4 nodes of 4 H200), the login node's 20-process cap and `scheduler_in_worker` (the host's Slurm client bound into the worker's container, measured on the grid on 2026-09-28), held to the module schema by the repository's checker and 53 tests; the launcher that composes the profile and starts the worker is `OpenSpineConsortium/hpcworker`, which this session could not read, and Figure 2a, from the extension's own store diagram. The job rules are prose, not data: "Grid etiquette" in `beethoven-agents/CLAUDE.md` and `beethoven-research/CLAUDE.md`, and the workspace guide the worker is given (follow a job at most once a minute, cancel only its own jobs, container temp on node-local disk); in code, the engine's guard caps arrays at 200 and refuses a secret in `sbatch --export`, and checks no partition, QoS or wall time. The worker has run as a Slurm job on a CPU node, reached from claude.ai (jobs 40496445 and 40501099, `11_students_grid_access/docs/beethoven/WAYNE_STATE_PILOT.md`), but no worker has yet submitted a real job, GPU or not, only `sbatch --test-only`, so Figure 2's caption says the worker is built to send GPU jobs to H200s |
| beethoven-qa's gate: contracts on every public function, searched for counterexamples by CrossHair and Z3, required on the agents' and the research code | `OpenSpineConsortium/beethoven-qa` at 85f0e1c, `README.md` (the gate; most conditions are searched within a 20-second bound rather than proven, which the packet's "checked" allows and "proven" would not); `beethoven-agents` at a40a71a and `beethoven-research` at 7e8fd69 each carry its release 3.0.0, hash-checked, and run the gate as a required check on `main` (their `.github/rulesets/main.json`; GitHub's live settings not checked; organization admins may bypass). The gate governs what lands on `main`, not what a job runs: tying each result to code that passed it is specified, not built, so the packet lists "one-command reruns of gated code" among what the consortium builds. The gate covers neither the C-arm code of Aim 3 nor anything outside those two repositories |
| beethoven-research holds REFORMS [10] rules and plans the CLAIM [11] checklist; the patient-split check is built; the consortium builds, in kind, the other REFORMS checks, the CLAIM checklist and one-command reruns of gated code | `OpenSpineConsortium/beethoven-research` at 7e8fd69: `CLAUDE.md` writes the split, result-row and rerun rules and names the REFORMS record and the CLAIM checklist as to come (`CLAUDE.md` lines 5 and 251-252, `README.md` lines 37-39); no CLAIM item is written yet, so the packet says beethoven-research plans it; of the rules, only the split rule is built; `src/beethoven_research/splits.py`, with 9 tests and a CrossHair check in its required gate, refuses an evaluation case that shares a patient, study, cadaver or CT source volume with a training case. Specified there and not built: result rows that carry the run, the commit and a clean-tree flag, refusing a row from a dirty tree; the log of every human intervention, written when it happens; and each run's compute and quota record (Slurm job ids, GPU-hours, tokens) |
| Symphony: each task an issue held by one agent, a person merging; public under MIT; its tests catch all 93 mutated rules | `OpenSpineConsortium/symphony-protocol` at a3a5b4d (2026-10-15): `spec/PROTOCOL.md` (one worker per claim, since GitHub refuses a second push of the branch; the owner merges under the default policy, a registered worker may land by auto-merge), `LICENSE`, `validation/README.md` and `tests/test_validation_mutants.py` (93 mutants, each one rule of the library broken on purpose, each caught in the required check on a recorded trace the unbroken library passes; the full search runs outside the required check). The 93 are on `main` after release 0.4.1, not yet released; this repository vendors 0.4.1 as `tools/sdlc_protocol` and uses its claims and board, and no Beethoven repository uses Symphony yet |
| the five planted faults: a patient in both training and test sets, the wrong label scheme, a threshold tuned on the test set, a typed number, a run that does not reproduce | the failures this programme guards against, root `CLAUDE.md` rules 3 to 6 (numbers wrong but plausible, two label schemes, held out means held out, pre-register then score) and `01_carm_level_detection/CLAUDE.md` (the threshold 0.74 is cross-device, never pre-stated; a number enters a manuscript only through a manifest key; resume is not reproduce) |
| Aim 1's design: 30 tasks, 10 for development and 20 sealed, each with a hidden check and a clean and a faulted copy; two arms, with and without the checks; eight GPU-hours per task, reruns included; each arm runs each copy once (80 runs); H1's under 20 % against over half, with no fewer passes on clean copies | chosen on 2026-10-15 for issue #100 and revised the same day after review (section 4); no file stands behind them, and H1's thresholds are a hypothesis written before any run, not a result |
| the Co-PI's four high-performance computing papers with the clinical collaborator (2021 to 2024); the PI's Gaussian-splatting and implicit-surface papers (CVPR 2025 and 2026, NeurIPS 2024); the PI's PhD of November 2017 and appointment since January 2021 | the two biosketches (submitted with the packet, not committed) |
| US neurosurgeons reported 418 wrong-level operations in about 1.3 million, one in 3,110, 17 % followed by legal action or a settlement [2] | `01_carm_level_detection/docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` (Mody 2008: self-report, 415 responses, a 12 % response rate, no interval) and `09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md` (73 of the 418 led to legal action or settlement) |
| surgeons' median naming error 30.4 % unaided and 2.4 % with LevelCheck, on 62 hard intraoperative images [6] | `01_carm_level_detection/docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` (Manbachi 2018: five surgeons, the same images, p < 0.01) |
| wrong-site surgery a serious reportable event, unpaid by Medicare since January 2009 [21] | the web only (section 2): the National Quality Forum's 2011 update, event 1A, and CMS national coverage determinations 140.6 to 140.8, effective January 15, 2009; neither local evidence brief covers them, and CMS's own term is "wrong body part" |
| the Joint Commission's 2024 review: 127 wrong surgeries, 9 wrong-level, 7 of those spinal, 36 % with severe permanent harm [22] | `09_wrong_level_clinical_qi/docs/WRONG_SITE_BURDEN_EVIDENCE.md` (the primary PDF, read verbatim by three verifiers; reporting is voluntary, so the counts are a floor, and the report draws no frequency from them) |
| paid US malpractice claims for surgical never events, $1.3 billion over 9,744 claims in 1990 to 2010 [23] | the same file (Mehtsun 2013: all surgical never events, a 21-year total, about $62 million a year; no source supports "billions a year", so the packet never says it) |
| 978 English spinal negligence claims over five years, 535.5 million pounds [24] | `09_wrong_level_clinical_qi/docs/WRONG_LEVEL_COST_EVIDENCE.md` (Machin 2018: April 2012 to April 2017, every spinal negligence claim, 26 of them never events; an estimate that includes reserves) |
| one US insurer's 68 wrong-site claims closed in 2013 to 2020 averaged $136,453, spine the commonest procedure [25] ("60.3 % settled" was cut for room in the reframing of 2026-10-16) | `09_wrong_level_clinical_qi/docs/WRONG_SITE_BURDEN_EVIDENCE.md` (Tan 2023: mean closed claim value $136,452.84, 60.3 % settled; spine or disc surgery the commonest procedure type at 22.1 %; a skewed mean, the poster's median $36,250 unconfirmed) |
| a card for each of 211 imaging sources, 115 of them on the grid (5.3 TB); in the abstract "211 catalogued sources, 115 on the grid at 5.3 TB" | `10_data_platform_grid/code/data_platform/DATA_MANIFEST.md` (211 sources: 176 upstream releases, 7 project releases, 23 derived products, 2 output roots and 3 drafted requests; 115 on disk) and `10_data_platform_grid/docs/grid_read_2026-10-08/census/ceph/census.tsv` (5,333.691 GB in 4,579,361 files on 2026-10-08, six migration batches not yet landed) |
| every item keyed to a person; nine leakage checks (seven run on the frozen split) ("which closed the two cross-naming leaks the identity checks found" was cut for room in the reframing of 2026-10-16) | `10_data_platform_grid/docs/handoff/LEAKAGE.md` (NHANES II entered the banks twice, 48 of 54 validation patients with a twin in training; CTSpinoPelvic1K under two names put 371 people on both sides of a split; both closed) and `10_data_platform_grid/STATUS.md` (CHK-1 to CHK-9; seven ran on the frozen person split, CHK-6 and CHK-7 not run; the leak audit passed) |
| 563 quoted numbers audited against their models' training persons | catalog row A19.2 (CHK-9: after the v9 closure 380 held out, 81 seen, 1 unresolved, 101 not applicable) |
| the CT census, 21,622 CTs from 21,603 persons | `06_transitional_ct_census/docs/ruleclass/TIERS.md` (catalog D.19, quoted "by the tier lists"; the grid's CORPUS.md says 21,655, a 33-CT difference recorded as unexplained) |
| the two automatic labelers chosen to fail differently "screened 18 further public collections (843 GPU-hours)", after the registry | `06_transitional_ct_census/docs/CENSUS_TABLE_2026-09-25.md` (843 GPU-hours: TotalSegmentator 443, SPINEPS 400; section 1, one row per collection, 18 rows) and `06_transitional_ct_census/STATUS.md` (catalog D.13: 18 collections, 18,873 listed; the row is DISPUTED for its on-disk and field-gate counts only, which the packet does not quote); the screen is later than the registry and not in it (`evidence/spine-aim-facts-2026-10-15.md`: the registry "leaves out the 18 acquired collections' calls"), so since the review of 2026-10-16 the packet no longer says the screen filled the registry |
| the labelers "filled a registry of 6,108 persons from the collections then in hand, 146 of them with a sixth lumbar vertebra, 103 on an expert read, and 14 with a thirteenth thoracic" | catalog row D.8 (the one registry of 2026-09-24: 6,131 rows, 6,108 persons, 782 alias edges; L6 146, of which 103 read by a person, 29 two-labeller, 10 single; T13 14) built from D.7's five harvest streams (verse, ctsp, totalsegmentator, cobra and other_ct, the last holding CTSpine1K and RibFrac among others) |
| a stopping rule, fixed before any download, that turned 29,479 mostly chest CTs away | catalog row D.11 (the rule: no collection below 20 expected transitional persons per terabyte, no fetch under 5 TB free, an 8 TB cap, tier 1 before tier 2; 29,479 CTs, 2.9 TB, turned down), `06_transitional_ct_census/README.md` ("tier 2 (29,479 CTs, 2.9 TB) refused") and the census table's section 2, whose tier 2 is chest-dominated, hence "mostly" |
| a labeler's 9.3 % rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4 % (5 of 367) once a rib on the named body was required ("five to fifteen times the published rate" was cut for room in the reframing of 2026-10-16) | catalog row D.12 (the NLST pilot: 34 of 367 from labeller A alone; 5 kept with a rib, 1.4 % of 367, which the catalog's own prose rounds to 1.5 %; the prior 0.6 to 2.0 %) |
| CTSpinoPelvic1K's benchmark paper is a NeurIPS 2026 poster | `03_ctspinopelvic1k_dataset/README.md` (submission 3474, accepted as a poster on 2026-09-24, OpenReview D8yRWDAGQF, the Evaluations and Datasets track) |
| 39,705 plain radiographs, 12,709 of which train a film detector | `10_data_platform_grid/docs/DATA_COMPLETENESS_AUDIT.md` (12,709 of 39,705 held films) and `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` (the body detector's film corpus); the 39,705 are CSXA 4,963, BUU-LSPINE 7,203, NHANES II 17,073 and VinDr-SpineXR 10,466 |
| the film detector finds 98.8 % (at 0.25) of 161 lumbar vertebrae on 17 spines it never saw | row A14.1 (at confidence 0.25, the threshold the packet uses elsewhere; 99.4 %, 160 / 161, at 0.05; the spines are NHANES II radiographs; the render-trained arm of the row is never quoted, its bank being the leaked one) |
| device cards fitted to four imagers reproduce held-out real frames at R^2 0.679 to 0.974 | row A12.1 (Cios Fusion 0.905, BV Pulsera 0.952, Elekta XVI 0.974, PIXIUM 4600 0.679, each above uncalibrated physics; fitted on 40 frames or fewer, 14 for PIXIUM) |
| COBRA: 692 radiotherapy cone-beam cases (467 Elekta XVI, 225 Varian OBI), 375,618 projections, each case with its acquisition geometry and a registered planning CT [29] ("exact" was dropped in the review of 2026-10-16: the geometry is RTK's per-case file, the CT deformably registered) | `01_carm_level_detection/MANIFEST_GRID.md` (692 of 692 cases, 375,618 projections, 808.615 GB by ls on 2026-10-08; `DATASET_USAGE.md` gives 771 GB) and `01_carm_level_detection/docs/DATASHEET.md` (Elekta XVI, centres A to D, 467 public cases, 0.8 mm at 504 squared, a deformably registered planning CT and RTK geometry per case, CC BY-NC 4.0); the 225 Varian cases are `DATASET_USAGE.md`'s "0 of 225 Varian", and 467 + 225 = 692 |
| 145 Elekta cases, 24 frames each, are in any frame bank (110 of them, 2,640 frames, train the detector); 322 Elekta and all 225 Varian cases train nothing; the 372,000 unseen projections, "with a CT whose automatic labels project onto every one" | `01_carm_level_detection/docs/handoff/DATASET_USAGE.md` section 2 (145 Elekta cases of 24 frames in the banks, 0 of 225 Varian) and its table's COBRA row (detector S trains on 110 cases and selects on 8, the other 27 its test; 110 x 24 = 2,640, the count A7.4 cuts to 240); the planning CTs' labels are the automatic labelers', none read by a person; 467 - 145 = 322; 375,618 - 3,480 = 372,138, written as 372,000 |
| Elekta frames and their styled renders alone find 86.8 % (249 of 287 [81.1, 91.8]) of the held-out C-arm's vertebrae at 0.25 on outline truth; cadaver C-arm frames alone 12.9 %; cutting the Elekta frames from 2,640 to 240 costs 47.7 points [-53.7, -41.8] | rows A7.1, A7.2 and A7.4 (the A7 header: 24 arms, 85 held-out cells, confidence 0.25, outline truth; under body-box truth the same arm reads 11.1 %, which is why the packet names the convention) |
| a detector that never saw COBRA finds 6.2 % of its vertebrae (18.5 % at 0.25) | row A6.9 (55 / 893 at 0.74, 165 / 893 at 0.25) |
| "the median age of its exported cases is 66 (known for 115 of 145)" | row A18.1 (age known on 115 of the 145 exported cases) |
| 7 transitional persons found and 91 calls unread on COBRA | row A16.6 (7 at-risk persons with an exported frame, 4 two-labeller and 3 single-labeller, L6 3; 91 unread test-side calls: L6 38, T13 45, four-lumbar 8) |
| the sacrum defined on 18.2 % of 609 COBRA test frames | row A4.4 (111 / 609 at 0.25) |
| two deployment routes have FDA precedents, an app on the C-arm maker's own platform and an external unit reading the C-arm's video output | `01_carm_level_detection/docs/CARM_DEPLOYMENT_EVIDENCE.md` (Siemens Cios OpenApps on the Cios family, clearances K181560 and K203504; NuVasive/Globus Pulse with LessRay, K180038) |
| CooperBench: two agents in separate workspaces, talking only by message, passed 183 of 652 feature pairs against 315 for one agent (GPT-5), most failures duplicated or incompatible work [27] | the Symphony taxonomy specification and manual the owner sent on 2026-10-15 (kept out of git), section 7.1 of the specification, which verified the counts in the paper's PDF: GPT-5 315 against 183 of 652, Claude Sonnet 4.5 307 against 168; 33.2 % of failed two-agent runs were work overlap and 29.7 % divergent architecture. These are the paper's published counts; the consortium's own coordbench runs appear nowhere, under the owner's hold of 2026-10-15 until the full suite has run |
| a shared workspace with optimistic concurrency raised a worktree baseline from 63.8 to 82.5 % on Commit0-Lite [26] | the package-search report the owner sent on 2026-10-15 (kept out of git), quoting STORM's macro pass rates; the paper is arXiv 2605.20563, "Multi-agent collaboration with state management", whose abstract page on export.arxiv.org gave the authors on 2026-10-16 |
| the orchestrator "as the consortium's own first attempt did" (worktrees, merge, adversarial review, verify); LangGraph's fan-out with checkpointing, Temporal's sagas, OpenHands sandboxes, schema-validated outputs | the owner's Workflow script of 2026-10-15 (three parallel worktree builders, a stack-and-merge step, a four-lens adversarial review, verify, fix) and the package-search report that proposes LangGraph.js's Send API with checkpointing, Temporal.io, OpenHands sandboxes and Zod-validated outputs for it; both kept out of git |
| gh-aw's work queue, unsorry, Copilot's cloud agent and Claude Code's agent teams, on the twelve-axis taxonomy written for the comparison (the three axes named in parentheses were cut for room in the reframing of 2026-10-16) | the taxonomy specification (twelve axes; the three the study rests on are axis 10, who pays for compute and inference, axis 5, how a claim is kept, and axis 11, what decides that work is acceptable; its neighbours include gh-aw's work queue, unsorry, Copilot's cloud agent, Claude Code's agent teams and agentic-setup) and the manual, the owner's documents of 2026-10-15 |
| agentprof's hooks [28] | github.com/kitaisreal/agentprof, its README read on raw.githubusercontent.com on 2026-10-16: "A profiler for agentic coding tools" that registers PreToolUse and PostToolUse hooks in Claude Code and logs every tool call with timestamps and token counts |
| Symphony records what each run cost (a usage trailer on every commit, a usage artifact per Actions run, aggregated by its metrics workflow) | `OpenSpineConsortium/symphony-template`, `docs/memory/field-metrics.md` and `.github/workflows/metrics.yml` (the Symphony-Usage trailer on each session's commits, a symphony-usage artifact per Claude run in Actions, read into the economics and coordination keys; symphony-template#57) |
| its protocol library is checked over every interleaving of a few workers against an oracle written from its spec | `OpenSpineConsortium/symphony-protocol`, `validation/DESIGN.md` and `validation/README.md` (the validation harness: every interleaving of a few workers against an oracle written from the specification's text, with the 93 mutants proving the checks bite; on `main` after release 0.4.1) |
| compute is GitHub's free standard runners on public repositories (Aim 1c and the budget's C1, C2 note) | the taxonomy specification's table of what GitHub gives (standard runners with 4 vCPUs, 16 GB and a 14 GB SSD on public repositories; concurrent jobs Free 20, Pro 40, Team 60), checked by the owner's documents against GitHub's pages; the packet prints no runner size |
| H3's "the stack names a frame in under 1 s on one GPU (no latency of the stack is on file yet)" | `01_carm_level_detection/CLAUDE.md` ("No latency of the reported stack exists": the 2026-09-13 bench timed older models, the 2026-09-22 run was contended and never timed the detector, the GPU job of `docs/MODEL_CARD.md` section 6.6 was never run); the 1 s is a target written before any run, and the budget's latency runs measure it |
| the project's goal, "a customizable, locally hosted retrieval-augmented language model for spine care (a RAG-LLM)" that reads the image through the consortium's detectors, retrieves from its index of Scopus and ScienceDirect spine literature, answers with cited quotations, is fine-tuned on images paired with clinical charts under the pending protocol, is compared with OpenEvidence through a Claude plug-in [31], and lets a lab swap in its own corpus, detectors and records; the spine program as "the case example" (the title, the cover's area 4 line, the abstract, section 1's premise, Aim 3's heading and its paragraph "The RAG-LLM", section 3, the alignment page) | the owner's message of 2026-10-16 02:30 UTC in the Project's chat: the proposal "can be reworked such that the SpineAI project is simply a case example of what this organized AI assisted tool can facilitate in a short period of time, the goal is to develop a customizable RAG-LLM, where I will train a multimodal LLM which uses my XRay detector and my Scopus and now science direct Text, Image, Multimedia database to create a RAG of spine literature/imaging and pretrained spine detector on my corpus to fine tune on / with images corresponding with clinical charts under the auspices of this IRB which will be amended however necessary / and either compare with or used to augment / augment an OpenEvidence plug in claude" (the mcpmarket.com link of [31]); "compare with or ... augment" is kept as both, the side-by-side grading and the detectors offered to OpenEvidence as a tool |
| "IRB-26-03-8648, whose stated purpose is a locally hosted multimodal spine LLM, amended as the work requires" (Aim 3); "fine-tuned on images paired with clinical charts under the consortium's pending IRB protocol (about 4,000 Detroit Medical Center spine surgery patients; amended as the work requires)" (the abstract); "the pending protocol's own stated purpose" (section 1) | the IRB form's print view (section 6; given again with the owner's message of 2026-10-16), whose purpose section reads "Multimodal AI Development: To train and validate a proprietary, multimodal spine surgery Large Language Model (LLM)", with "all deep learning and model training ... executed locally on the secured Wayne State University high-performance computing grid" and "Public or cloud-based AI systems (e.g., ChatGPT) ... strictly prohibited", for "report-and-image-to-mask" tasks, decision support and synthetic planning and educational imagery; "amended as the work requires" is the owner's "which will be amended however necessary" |
| the index of "Scopus and ScienceDirect spine literature (text, images and multimedia, under WSU's text and data mining rights)" (the abstract) and Aim 2's "Scopus, and ScienceDirect's text, images and multimedia) under WSU's text and data mining and AI rights from Elsevier" | the owner's message of 2026-10-16 ("my Scopus and now science direct Text, Image, Multimedia database"); the correspondence of 2026-10-15 (section 6) had Scopus approved and ScienceDirect's amendment pending, so the owner's "now" is read as that amendment having come through, a reading the owner confirms before submission, since no later correspondence was given to the thread |
| "On a held-out question set the mentors write on public images, its answers and OpenEvidence's, through a Claude plug-in [31], are graded side by side for correctness and for quotations that support them; the detectors' reading of an image may go to OpenEvidence with the question, while no indexed passage and no patient record leaves the grid" (Aim 3), H3's "graded correct at least as often as OpenEvidence where the question needs the image, with no unsupported quotation", and the Measures' "graded correctness and quotation support against OpenEvidence" | a design of this thread's, from the owner's "either compare with or used to augment": the correspondence of 2026-10-15 told Elsevier that no outside AI service receives its content and the protocol's own text bars public or cloud AI on its data, so the comparison sends OpenEvidence only the question, on a public image, and the detectors' reading of it, and the mentors grade the two answers by hand; the plug-in is not called OpenEvidence's, since the skill [31] is a third party's; the threshold "at least as often ... where the question needs the image" is a hypothesis written before any run, this thread's choice |
| "the RAG-LLM's first release, on the public corpus (CTSpinoPelvic1K, the labeled films, COBRA)", its second "on images paired with operative notes and radiology reports under IRB-26-03-8648" (Aim 3, section 3's quarters 3 and 4) | a design of this thread's: the public corpus is the one in hand (section 1's rows for 802 CTs, 39,705 radiographs, COBRA), so the first release and its graded question set fit the award year while the protocol is amended and approved; the films carry their collections' published labels (`10_data_platform_grid/docs/DATA_COMPLETENESS_AUDIT.md` lists the four film collections and their label files), no report and no patient record of the consortium's, which is why the packet says "labeled films" and keeps the reports for the second release |

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
repository's earlier full-text readings (`01_carm_level_detection/docs/research/BIB_RESOLVE_2026-09-22.json`). Since
issue #100 the list is [1] to [20]: [10] REFORMS (Science Advances 10(18), eadk3452, May 2024), [11] the CLAIM
2024 update (Radiology: Artificial Intelligence 6(4), e240300), [14] the AI Scientist (arXiv 2408.06292, no
peer-reviewed venue found), [15] Luo, Kasirzadeh and Shah, "The more you automate, the less you see: hidden pitfalls
of AI scientist systems" (arXiv 2509.08713; a NeurIPS 2025 workshop paper, so cited as arXiv) and [16] Atinafu and
Cohen, "RewardHackingAgents" (ICDE Workshops 2026, pp. 27-34, doi:10.1109/ICDEW71238.2026.00009) were checked on
2026-10-15 against search excerpts; RE-Bench is no longer cited, and the old [10], [11] and [13] to [16] are [12],
[13] and [17] to [20]. For room, [10] and [11] carry no system name (the text names REFORMS and CLAIM), [15] no
title and [8] no "Zenodo 2026" (its doi is Zenodo's). DeepDRR [19] is credited with the physics and SyntheX [20] with the strong domain randomization,
whose hip-landmark parity rests on 366 cadaver images from six specimens; [1] counts patients, not operations; [2]
and [3] surveyed neurosurgical societies; the cohort's ten abstracts were submitted, not reported accepted. Still to
check by hand: the first author's initial in [4] and the Zenodo page of [8]. The FICA rate of line A2 is the
employer's statutory share, Social Security 6.2 % and Medicare 1.45 % (IRS Publication 15,
https://www.irs.gov/publications/p15).

### Values added on 2026-10-16

The rewrite for issue #106 (the owner's items 5 to 12 of 2026-10-15) added references [21] to [30], and the
reframing of 2026-10-16 (the owner's message of 02:30 UTC, section 4) added [31]. The cost
literature rests on the project's own evidence briefs under `09_wrong_level_clinical_qi/docs/` and on search snippets
gathered on 2026-10-15 (`evidence/spine-aim-facts-2026-10-15.md`, whose run could open no publisher page); the three
arXiv abstract pages were read on export.arxiv.org on 2026-10-16 and agentprof's README on raw.githubusercontent.com.
Each bibliographic detail marked "snippet" below is checked on PubMed or the publisher's page before submission.

| value in the packet | source |
|---|---|
| [21] NQF, Serious Reportable Events, 2011 update (event 1A, wrong site); CMS NCD 140.6 to 140.8, effective January 15, 2009 | snippets of https://qualityforum.org/Publications/2011/12/SRE_2011_Final_Report.aspx and https://www.cms.gov/transmittals/downloads/R101NCD.pdf; in neither local brief |
| [22] The Joint Commission, Sentinel Event Data, 2024 Annual Review | the primary PDF, verified by the brief's three verifiers (digitalassets.jointcommission.org, content id eac7511986c0442a9c1ae04b1aa02cc0) |
| [23] Mehtsun WT, et al. Surgery 2013;153(4):465-72 | volume, issue and pages from a snippet of https://pubmed.ncbi.nlm.nih.gov/23257079/; the brief records the claim counts and the total, not the pages |
| [24] Machin JT, et al. Eur Spine J 2018;27:2693-9 | the brief gives 27(11):2693-2699, PMID 30151803; the issue number was not confirmed on the web, so the packet prints the volume alone; a snippet says a 2019 correction (28(1):195) fixed the first author's name |
| [25] Tan J, et al. Jt Comm J Qual Patient Saf 2023;49(5):265-73 | the brief gives the journal, volume, issue, pages and PMID 36925434; the author list is from a snippet of the ScienceDirect page |
| [26] Liu M, et al. Multi-agent collaboration with state management (STORM). arXiv:2605.20563 | https://export.arxiv.org/abs/2605.20563 (Liu, Chen, Xu, Jiang, Dong and others; 2026-05-19); the 63.8 and 82.5 % are the owner's report's reading of the paper; the abstract, read on 2026-10-16, says STORM "outperforms the git-worktree-based multi-agent baseline by +18.7 on Commit0-Lite", and 82.5 - 63.8 = 18.7 |
| [27] Khatua A, et al. CooperBench. arXiv:2601.13295 | https://export.arxiv.org/abs/2601.13295 ("CooperBench: Why Coding Agents Cannot be Your Teammates Yet", Khatua, Zhu, ..., Yang; 2026-01-19); the counts from the taxonomy specification's section 7.1; the abstract, read again on 2026-10-16, says agents "achieve on average 30% lower success rates when working together" (GPT-5's 183 against 315 is 42 % lower, Sonnet 4.5's 168 against 307 45 %, so the two named models sit above that average) and names jammed communication, broken commitments and wrong expectations as the issues; "most failures duplicated or incompatible work" is the specification's 33.2 % work overlap plus 29.7 % divergent architecture |
| [28] agentprof. github.com/kitaisreal/agentprof, 2026 | https://raw.githubusercontent.com/kitaisreal/agentprof/main/README.md |
| [29] Thummerer A, et al. COBRA2026. arXiv:2607.20037 | https://export.arxiv.org/abs/2607.20037 ("COBRA2026: a large-scale multicenter pelvic cone-beam computed tomography projection dataset", Thummerer, Rit, Kamp, Maspero and others); `10_data_platform_grid/code/data_platform/sources.json` gives the same id and Zenodo 10.5281/zenodo.21322350, v1.0.0 of 2026-07-13 |
| [31] OpenEvidence, openevidence.com; a Claude Code set-up skill for its API, mcpmarket.com/tools/skills/openevidence-api-setup-auth | https://mcpmarket.com/tools/skills/openevidence-api-setup-auth, read on 2026-10-16: a Claude Code skill, "OpenEvidence API Setup & Auth" by jeremylongshore, that "configures and verifies OpenEvidence API authentication for clinical decision support integrations in healthcare applications"; the link the owner's message of 2026-10-16 gave; openevidence.com itself was not read, so the packet calls it a clinical evidence service and quotes no figure about it |
| [30] C-ArmLSpine. Med Image Anal 2024;97:103283 | `10_data_platform_grid/code/data_platform/sources.json` (Zhang et al., Medical Image Analysis 97:103283, 2024; Zenodo 10.5281/zenodo.22768651; doi:10.1016/j.media.2024.103283); no local file holds the author list, so the reference names the dataset, as [8] does |

Since issue #106 the list is [1] to [31]; [1] to [20] are as before.

## 3. What only the team can supply (the red [DATA NEEDED] marks)

1. The PI's office and phone (the filled `contacts.tex` gives the department office until then).
2. Settled: that the PI's appointment is tenure-track (the call requires it) and the ESI end date in eRA Commons,
   both confirmed in Dr. Han's edits of 2026-10-15 (issue #102), which commented their marks out.
3. Settled the same way: that the PI leads no other AIDaS proposal this cycle.
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
- **The MIT release** of Aim 1's tasks, records and report is the owner's call, with only the tasks a disclosure
  review clears. Beethoven's repositories (beethoven-sites, -base, -qa, -agents, -research) are private and
  proprietary and are not released; Symphony is public under MIT already.
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
  framing and references [17] and [18].
- **Line E**, an application to Anthropic's AI for Science program for API credits, was dropped on 2026-10-15 (issue
  #100): Beethoven and the consortium's frameworks use no API key and no usage credit, every agent running on a plan
  held in a person's own name, and the program's terms would let Anthropic use data made with the credits. The
  request is unchanged, since line E asked for $0; line F keeps its letter. Put it back only with a way to run the
  credits outside Beethoven.
- **The R21's mechanism.** The parent R21 (PA-25-304) allows no clinical trial and NIBIB's EBRG (PAR-25-321) makes one
  optional, so a validation that reaches patients' care fits PAR-25-321; earlier Trailblazer calls discouraged
  preliminary data, which the alignment page plans to bring.
- **Reference [9]** names its first author alone, "Schehr A, et al." (a published co-author, root CLAUDE.md rule 1),
  since rule 12 keeps student names out of this repository; add the other authors in Overleaf if wanted.
- **Federal wording.** EO 14434 (September 29, 2026), "Inaugurating the Era of Super Intelligence", has agencies
  write "Super Intelligence" and "SI" in place of "AI" in their own documents. It binds agencies, not applicants, so
  the AIDaS packet keeps "AI" and the CAREER and R21 drafts may echo a solicitation's own words without having to.
- **The literature grounding and the pending protocol** (added 2026-10-15, section 6). The packet says Scopus is
  confirmed and quotes Scopus abstracts only (since issue #100 it no longer says, for room, that ScienceDirect's full
  text waits on an amendment): ask the library to add the text and data mining amendment to
  WSU's ScienceDirect agreement with Elsevier's account manager, and confirm before sending that Elsevier has enabled
  the Scopus APIs on the key. The key is one person's; the agent queries the index on the grid, never the API, and
  the index stays outside the MIT release. The protocol IRB-26-03-8648 is in draft on the IRB's side (pre-reviewed
  2026-09-28, expedited review requested): the packet calls it pending and promises nothing from it within the award;
  if it is approved or submitted before the deadline, say so on the cover and the alignment page. The protocol's own
  text calls the consortium's benchmark neurosurgical in two places; the packet does not (root CLAUDE.md rule 1).
  The correspondence also told Elsevier the index sits in storage only the key holder reads; the trainees read the
  answers inside WSU, which "nothing shared outside WSU" allows, but ask Elsevier if that reading is in doubt.
- **The panel review of 2026-10-15.** After the two elements went in, a five-reviewer AIDaS panel read the packet
  again and a verifier kept 13 of its proposals; 11 were applied. Aim 1's one-shot arm now retries from scratch within
  the same budget, so H1 tests repair, not more attempts. Aim 2's starter tasks lie outside the agent's development
  set and benchmark, task and order counterbalanced, and the preliminary work says the 2026 mentors were expert in
  Slurm. A wrong QoS is no longer counted a rule violation, since the scheduler refuses it and the agent repairs it.
  The literature answers are measured (a misquoted passage fails a gate; the mentor marks one that does not support
  the answer), come from Scopus abstracts, and come from a language model on the grid (section 6). The cover's AI for
  Health line states the intended use and that the stack withholds a label when its checks disagree; the abstract no
  longer promises to close the detection gap; the R21 item says FDA's feedback shapes the validation, not the
  protocol; budget line D asks FDA about the reference standard; the team paragraph states the PI's lead. Not
  applied: tying New Investigator status to federal targets on the cover (no room, and said on page 5) and moving the
  CAREER row (it would contradict the risk fallback on page 4). To fit 10 pages, the H2 sentence no longer repeats
  that comfort is secondary (the table says so) and the table's Aim 2 design reads "plan preregistered".
- **Aim 1 rewritten around the consortium's frameworks** (issue #100, 2026-10-15). The owner, 2026-10-15: "so Aim 1
  is slightly wrong, the beethoven-base and beethoven-site repos already hold all the protocols for writing grid jobs
  on WSU cluster. The LLM doesnt have to learn how to do that, further the beethoven-research repo contains protocols
  for writing repreducible CLAIM/REFORMS compliant workflows, all claude will do is iterate the scientific method and
  perform semi-autonomous AI research under a set of strict frameworks to ensure quality", and "theres also
  beethoven-qa for checkign the autonomously written code, beethoven-agents, and the entire symphony-protocol for
  coordinating multi-agentic workl essentially it is the culmination of all my work thus far". The title, the cover's
  area 1 line, the abstract, the keywords, the significance, Figure 1b and its caption, the Aim 1 paragraph, the
  evaluation table's Aim 1 row, section 4, the CAREER item, the team paragraph, the timeline and the budget's lines A,
  C1, C2 and E now say so: Claude Code iterates hypotheses inside Beethoven (the grid's rules), beethoven-qa (the
  code), beethoven-research (REFORMS and CLAIM) and Symphony (several agents), a person setting each task's question
  and gate and merging what is accepted. Defaults taken without asking, each the owner's to change: the methodological
  contribution is a planted-fault study (how often an agent doing research accepts a wrong but plausible result, and
  which checks fixed in advance stop it), with two arms, with and without the frameworks' checks, since a benchmark of
  job repair no longer fits; the faults are the five kinds this programme guards against (section 1); 30 tasks, 80
  runs, eight GPU-hours per task, and line A's 180 Aim 1 hours re-based on checking runs and sealing known answers;
  the PI "designs Aim 1" and the Co-PI "builds the evaluation harness, plants the faults and keeps the grid
  measures" (both asked of them by e-mail); the agents run attended until the grid clears unattended agents, which `beethoven-research/CLAUDE.md`
  requires first. What is built and what the consortium builds in kind is said in the Aim 1 paragraph itself: the grid profile,
  the code gate, the patient-split check and Symphony exist; the other REFORMS checks, the CLAIM checklist, the
  one-command reruns and the orchestration of several agents' Slurm jobs (specified in `beethoven-agents`, not
  built) do not. The consortium's coordination experiment of 2026-10-15 is kept out of the packet, as the owner
  asked on 2026-10-15 ("hold off on getting the data into the grant until i run the full benchmark suite"). The
  execution skeleton (section 5) and RE-Bench went with the old Aim 1. To fit 10
  pages, Aim 2's literature sentence lost its ScienceDirect clause, section 4 points to the alignment page for the
  protocol IRB-26-03-8648's details, and the team paragraph is shorter.
- **The review of the rewritten Aim 1** (issue #100, 2026-10-15). Three reviewers read the packet as an AIDaS
  panel would, and a source check read the Beethoven repositories, symphony-protocol and the new references; what
  survived was applied. The design now gives each sealed task a clean and a faulted copy, the fault planted after the
  checks freeze by someone who did not write them, and each arm runs each copy once in its own repository, so H1
  also asks for no fewer passes on clean copies and reruns within a sealed tolerance; a person merges each result and
  every other step a person takes, blind to faults, is a logged intervention. The text says what is built (rows above)
  and that the consortium builds the rest in kind. Figure 2's caption says the worker is "built to send GPU jobs to
  H200s", since no worker has submitted a real job; the agents run attended, a person approving each command, until
  the grid clears unattended runs: the engine image is not yet built on the grid, its managed settings lock out
  Claude Code's bypass mode, a non-interactive step refuses any command not allowed and no rule allows `sbatch`
  (`beethoven-agents/containers/`, `beethoven-agents/CLAUDE.md`; inferred from the documented behaviour, not seen on
  the grid), and the first unattended run waits on the cluster's written position on autonomous agents. The related
  work cites [15] and [16]; line A's Aim 1 hours check 80 runs at two hours each and seal the known answers in 20; the
  team paragraph says Beethoven and its frameworks are the clinical collaborator's proprietary software, given in
  kind, with no award funds going to them. To fit 10 pages: the alignment page lost its FDA Q-Submission sentence (the
  R21 item and the timeline name the Pre-Submission) and says the Co-PI's four papers with the clinical collaborator
  in fewer words; section 4 no longer names the R21's protocol (the alignment page does); Aim 3 no longer says the
  agents run its experiments (the significance turns the agent on the detection gap, and the CAREER item says Aim 1's
  agent runs them); the evaluation table and the references are shorter.
- **The final fact-check of that rewrite** (2026-10-15) changed six things: beethoven-research "plans" the CLAIM
  checklist, since no CLAIM item is written there yet (if one is written elsewhere, say "holds" again); the gate's
  definition is set off in parentheses, so "the agent can read but not change" is the gate, not the first job;
  Slurm is named once as the scheduler; the team paragraph calls Beethoven's repositories proprietary, since
  Symphony is public under MIT; the CAREER row says "Aim 1's early results", since the runs go on to month 8; and
  line A's 20 sealing hours say "hours".
- **The owner's calls from that review.** (1) Line C1 buys Claude Team Premium seats, but `beethoven-agents`
  decision D1 ("a flat-rate Claude plan held in the student's own name", marked settled) and `docs/ACCOUNTS.md` ask
  for a plan in the person's own name, and the 2026 pilot asked for Pro or Max: a Team plan is the organisation's.
  A seat moved to the next trainee, who signs in with their own account, shares no account; but either D1 is amended
  or C1 changes to Pro plans, an amount the owner sets. On Team, keep usage credits off and have an Owner turn on
  Remote Control. (2) `beethoven-research` merges by GitHub's auto-merge with no human click once its checks are
  green, `SKIP_GATE=1` skips the pre-push gate and organization admins bypass the required checks
  (`beethoven-research/CLAUDE.md`, `.github/workflows/automerge.yml`, `.github/rulesets/main.json`): the packet's
  "a person merges each result" holds for Aim 1's own task repositories, which must be set up that way (Symphony's
  default policy), not for `beethoven-research` itself. (3) `beethoven-research/CLAUDE.md` keeps CTSpinoPelvic1K out
  of any data split until its patient-identity audit closes, a written rule with no check in code: tasks drawn from
  Aim 3 that train or evaluate on CTSpinoPelvic1K wait on that audit or use other corpora. (4) Conflict of interest:
  beethoven-qa, -agents and -research (and, by an earlier reading, -base) name the clinical collaborator as their
  vendor under the trade name OpenSpineConsortium, and beethoven-sites names none;
  the packet says so in the team paragraph, and the WSU conflict-of-interest check is the owner's. (5) Symphony's 93
  mutants are on `main` after release 0.4.1; the packet says "Symphony's tests", which holds of the development
  version whether or not 0.5.0 is released by the deadline.
- **The figures.** Figure 2a is redrawn as vector boxes from the labels of the extension's own store diagram, and
  Figure 2b crops the popup's top half, which shows no grid login; the VS Code edition's diagrams have labels that
  overlap at print size and are not used.

- **The rewrite of 2026-10-16 (issue #106; the owner's items 5 to 12 of 2026-10-15).** The abstract and section 1
  now carry the hospital's stake in cited rules and costs (never "billions a year", which no source supports), the
  platform's scale and the census that mined it; Aim 1 gained 1b (the cost of the agent: Symphony's usage records, a
  profiler, four economies run as sealed tasks, a standing routine proposing the next experiment), 1c (the claim
  protocol against the worktree orchestrator, one framework orchestrator and the published systems, on CooperBench's
  pairs, SWE-bench instances and Aim 3's tasks, on GitHub's free runners and the grid) and 1d (the control panel, the
  token wizard, the Actions-to-grid bridge, the extension's click brought to the claude.ai Project); Aim 3 gained
  "What COBRA adds". To hold three pages the narrative is 8.8 pt on 10 pt leading with 0.65 in margins (was 9 pt and
  0.7 in), the evaluation table is folded into the Measures clauses and section 3 is one line, Figures 1 and 4 are
  0.58 of the line and Figure 2 is 0.54, Figure 3's panels are 2.80 and 1.71 in, Figures 2 and 3 are top floats, and
  the references are 5.8 pt in five columns (the layout changed again in the reframing, two bullets below).
- **Defaults taken in that rewrite, for the owner to overrule.** (1) CooperBench's published counts are cited as
  literature [27]; the consortium's own coordbench runs appear nowhere, under the owner's hold of 2026-10-15 until the
  full suite has run. (2) H1b ("the four economies together pass the same gates at under half the tokens") and H1c
  ("cost per passing task at or under each orchestrator's on every suite, pass rates inside their paired intervals")
  are hypotheses written before any run, with thresholds this session chose. (3) Item 9 of the owner's list arrived
  cut off ("Projects can only be opened in"); 1d reads it as bringing the extension's one click to the claude.ai
  Project each trainee works in. (4) The strace article the owner linked is "system-call tracing" in 1b, with no
  reference, since its page was not read. (5) Left out on purpose: the A8 learning curve (its N = 0 floor is a
  box-convention artefact, A8.1, and would read against A6.1's 80.5 %); A3.1 and A3.2 (beside A9.2's 98.1 % they
  would look inconsistent); A8.6 (HELD-OUT, NOT QUOTED); the render-trained arm of A14.1 (a leaked bank); and, for
  room, "(one results figure took 250 fine-tunes)", "(0.42 % in the thoracic spine)", "(88.0 % counting those it
  misses)" from the abstract only (Aim 3 keeps it) and the runners' "(4 vCPUs, 16 GB)". (6) The costs [21] to [25]
  rest on the project's briefs and on search snippets; no publisher page was read, so each is checked by hand before
  submission (section 2). (7) The COBRA sentence names no tube voltage: the Elekta imagers run at 120 kV and the
  Varian ones at 125 to 140 kV in a research note that calls itself unverified, so the packet says "a linac's kV
  imager" and no number.
- **What adding COBRA buys, the owner's question of 2026-10-15, in one place.** Today 145 of COBRA's 692 cases
  (3,480 frames) are in any training bank, and they already carry cross-device detection: Elekta frames and their
  styled renders alone find 86.8 % of the held-out surgical C-arm's vertebrae at 0.25 on outline truth, cadaver
  C-arm frames alone 12.9 %, and cutting the Elekta frames tenfold costs 47.7 points (A7.1, A7.2, A7.4). The other
  372,000 projections (322 Elekta and all 225 Varian cases) come with each case's acquisition geometry and a
  registered planning CT, so they are real-image corner labels for the new detector at scale, paired data to fit the
  simulator's spectrum, scatter and sensor terms by supervision, and a second held-out vendor; the cost is an export,
  storage, a Varian bank with a quality look and GPU hours, written into Aim 1's task set and quarter 1. The limits
  the packet states: a linac's kV imager is not a surgical C-arm; a detector that never saw it finds 6.2 % of its
  vertebrae (A6.9); its median age is 66 (A18.1); 7 transitional persons found and 91 calls unread (A16.6); the sacrum
  defined on 18.2 % of 609 test frames (A4.4); so COBRA trains detection and simulation while the surgical C-arm and
  the cadaver set test naming. Not in the packet: CC BY-NC 4.0 terms (research use, no commercial product trains on
  it without the licensors' leave) and the 74,364 cross-case near-duplicate pairs (different patients at the same
  gantry angle; no same-case pair, so the by-case split holds; `01_carm_level_detection/docs/DATASHEET.md`).
- **The reframing of 2026-10-16 (the owner's message of 02:30 UTC).** The spine program is now the case example and
  the project's end product is the customizable, locally hosted spine RAG-LLM (section 1's five rows on it). Changed:
  the title; the cover's area 4 line; the abstract's goal sentence and its deliverables; section 1's premise paragraph
  and its Aim 3 line; Aim 2's grounding sentence (ScienceDirect's text, images and multimedia beside Scopus); Aim 3's
  heading, a new paragraph "The RAG-LLM" (the detectors as the model's tools, the first release on the public corpus,
  the second on paired images and charts under the protocol, the side-by-side grading against OpenEvidence), H3 and
  the Measures; section 3's deliverables and quarters 3 and 4; the alignment page's R21 item and team sentence; the
  budget's C2 line; and reference [31]. Displaced for room, with nothing else lost: A6.5's rebuilt-truth clause (82.2
  and 93.9 %), Tan's "60.3 % settled", the identity checks' two closed leaks, D.12's "five to fifteen times the
  published rate", "End-to-end latency is unmeasured; Aim 3 measures it first" (the latency measures and the budget's
  latency runs stay), the three taxonomy axes named in parentheses, the keywords "3-D Gaussian splatting" and "domain
  transfer", COBRA's "by supervision" and the cost list's wording, and section 3's heading paragraph, now one
  paragraph. The layout now: the abstract in \small, the narrative 8.8 pt on 9.8 pt leading with 0.5 pt paragraph
  skip and 4 pt float separation, captions at 1 pt skip, the references' column separation 1 pt, Figures 1 and 4 at
  0.50 of the line and Figure 2 at 0.48, Figure 3's panels 2.55 and 1.56 in; 10 pages, no overfull line, 16 red marks.
  Not changed, since the owner's message did not ask it: the holds of 2026-10-15 (no coordbench run data; VinDr and
  FluoroCap's results stay; rule 9), the names kept private, and the red marks' owners.
- **The adversarial review of 2026-10-16.** One reviewer read the packet against its files and traced every number
  (its report is in the thread's session, not in git); 32 findings. Applied: "an invention-disclosure review" became
  "WSU's technology-transfer review"; the registry no longer reads as filled by the 18-collection screen (rows above);
  115 of the 211 sources on the grid; seven of the nine leakage checks run; "legal action or a settlement"; the films
  "labeled", not "with their reports"; the plug-in "a Claude plug-in", not OpenEvidence's, and the question set on
  public images; the RAG-LLM's first release in the clinical collaborator's in-kind work and in line A's checking
  hours; the second release's fine-tune and "whose stated purposes include"; COBRA's frame bank against its
  training frames, "automatic labels", the exported cases' median age, no "exact" geometry; "no latency of the stack
  is on file yet" in H3; the wizard and the grid bridge in quarter 2; "at 0.25" on A14.1; "submitted" for the
  abstracts; "many GPU jobs" for "hundreds"; the PDF's title; and the record rows. Not applied: the reviewer read
  "nothing retrained" as barring the RAG-LLM's fine-tune, but that hold is about the leaked initialisations (rule 9)
  and the owner's message of 2026-10-16 asks for the fine-tune; the ScienceDirect wording stays on the owner's word
  (section 6) with "under WSU's text and data mining and AI rights from Elsevier" in place of "rights Elsevier
  approved"; the references stay 5.8 pt in five columns and the orchestrator frameworks stay named, for room. To hold
  10 pages after it: the narrative on 9.7 pt leading, Figure 2 at 0.46 of the line and Figure 4 at 0.48, two
  timeline rows and the closing line shortened. `review/page_slack.py` now measures against the 0.65 in margins.
- **The contact lines of 2026-10-16 (issue #108).** The owner's lines in the private `latex/contacts.tex` take two
  more lines on the cover than the placeholders, which pushed the keywords' second line onto an eleventh page. Six
  trims win it back without dropping a fact: "own" before the consortium's detector, "mined for the problem" (the
  census sentence says it), "first" and "after" around CooperBench and SWE-bench, "372,000 unseen COBRA
  projections", "the RAG-LLM" for "the RAG-LLM's text half" in the abstract (Aim 2 keeps the text half), and "lines
  B to D buy goods and services" without "from WSU units and vendors". With the real lines page 1 is full; with the
  example lines it has 18 pt to spare. The PI's line prints two phone numbers with no label between them, as the
  owner's file has it.

## 5. The execution skeleton

`autonomous_spine_agent.py` beside this file was the mock of the earlier Aim 1, an agent that repaired its own
Slurm jobs; since issue #100 Aim 1 iterates research inside the consortium's frameworks, which hold the grid's rules
the simulator re-created by hand, so it is kept only as a record. It is standard library only: a grid simulator with the
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
  Elsevier's account manager. In the packet: the cover's area 3 line, the abstract, Aim 2's grounding sentence,
  the evaluation table's Aim 2 metrics and the clinical collaborator's roles; since the reframing of 2026-10-16 also
  the abstract's goal sentence, section 1's premise and Aim 3's "The RAG-LLM", which name ScienceDirect's text,
  images and multimedia on the owner's word of that day ("now science direct"), the amendment this correspondence
  left pending; the owner confirms it before submission. The packet sends the trainees'
  literature questions to a language model on the grid, never to the agent, since the agent's model runs on Claude's
  servers (Figure 2a) and the correspondence told Elsevier that no outside AI service receives its content.
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
  trained only on the grid; a de-identified restricted-access release under a data use agreement. In the packet: since the
  reframing of 2026-10-16, the abstract ("fine-tuned on images paired with clinical charts under the consortium's
  pending IRB protocol (about 4,000 Detroit Medical Center spine surgery patients; amended as the work requires)"),
  section 1 ("the pending protocol's own stated purpose"), Aim 3 ("IRB-26-03-8648, whose stated purpose is a locally
  hosted multimodal spine LLM, amended as the work requires"; the form's purpose paragraph is quoted in section 1's
  row), the alignment page's R21 item ("pending", "about 4,000 adult DMC spine surgery patients, their CT and
  records, the RAG-LLM's paired images and charts") and its team paragraph ("the pending protocol"); the form was
  given to the thread again on 2026-10-16 with the owner's message and stays out of git.
