# TODO: what is not on the grid or not done, in order

Sources: `../_plan/PLAN.md` section 3 (01, the first five steps), the inventory's ordered plan behind it
(`docs/handoff/` and `docs/MODEL_CARD.md`), `docs/handoff/OPEN_QUESTIONS.md` (OQ), `docs/handoff/RESEARCH_DIRECTIONS.md`
(RD), `docs/handoff/RECIPES.md`, `docs/handoff/MANUSCRIPTS.md` sections 2.6, 2.8, 16, 21, and the repositories' own plans
(`docs/MODEL_CARD.md` "What this card asks for next", `manuscripts/schwingnet/README.md`, `docs/FLAGSHIP_PLAN.md`). Every
step names its gate, the pre-stated number where one exists, the dependency and who decides. "Greg decides" marks a
decision reserved to Greg (`../_plan/PLAN.md` section 5). Two constraints order the list: regulatory lead time is longer
than engineering time (start S4 early), and nothing is scored at the hospital before the stack, the runtime and the reading
protocol are frozen.

## A. The ordered plan

| step | what | gate / pre-stated number | depends on | who decides |
|---|---|---|---|---|
| **S0** | Freeze and register the reference stack: `python tools/model_registry.py register` for `rx_lodo_carmlspine_1024`, the five v9init fold encoders and heads and `dc_P_pooled`, with `--metrics`; add `seed` and `code_sha` to `devcorpus_train.py` and the CV scorer (`docs/MODEL_CARD.md` "What this card asks for next" items 1-2); commit the five edited tools (`level_prototype`, `carmlspine_eval`, `patient_keys`, `pipeline_state`, `test_patient_keys`) and the three untracked ones (`cine_eval.py`, `cine_latency.py`, `tools/fluoro_video/`), or keep the copies in `code/` as the record | every weight the paper quotes has a `HOME/model_registry/registry.jsonl` line with a sha256; `git status` clean for the C-arm tools | nothing | engineering; Greg commits when he asks |
| **S1** | Measure the uncontended latency of the reported stack: write the `docs/MODEL_CARD.md` section 6.6 job as a file (`slurm/runtime_cost.sh`, not `--wrap`), run `eval_runtime_cost.py --selftest`, then the GPU job `--frames /rs/rs_grp_oschome/go2432/data/realxray/carmlspine/images --bodies 6 --threads 1 4 16`; run `cine_latency.py` on the case134 spin (`CEPH/data/realxray/carmlspine_sweep`) once its prototype outputs exist | `HOME/bench/runtime_cost.json` with the detector stage present and `machine_load_*` empty; the per-exposure time written beside the 20 s to one minute the surgeons stated and the 4.7 s per image of the registration comparator (`docs/MODEL_CARD.md` section 6) | S0 | engineering |
| **S2** | Package the reported stack into `code/service/`: replace `detect_v5z_epoch25` + M19 with `detector_v5z_final` + the v9 encoder + the v9 head; add the sacrum detector, the count, the coupling, the abstain flag and the attenuation-and-window conversion of `docs/REAL_XRAY_DATASETS_SPEC.md` (percentiles 1/5/50/95/99 to 27/47/126/216/239, bone bright, head-up; respect `canonical_slots` of `code/spine_detector_src_snapshot/src/manifest.py`); `deploy_service.py` writes `registry.json`; weights stay in the private HF repository | parity with `level_prototype.py` on 50 evenly spaced C-ArmLSpine frames: boxes equal, decoded names and abstain flags identical, largest posterior difference below 1e-5 (the gate `code/cine_latency.py` defines) | S0 | engineering; the hosting choice (Modal, Fly.io, EC2, a tunnel; HF returned 402) is Greg's |
| **S3** | Discover the hospital device: which OR C-arms the co-investigating service uses; whether their exposures reach PACS as XA / RF / Secondary Capture or sit in the C-arm's own archive; a header census of ten archived exposures per device with `code/device_census.py` (format: `spinesurg-ct-nnunet:docs/devices/census/*_headers.md`: Manufacturer, ManufacturerModelName, SoftwareVersions, ImagerPixelSpacing, SID, Rows/Columns, BitsStored, PixelIntensityRelationship, PositionerType, Modality); ten exposures through `level_prototype.py` bone-bright and head-up, rendered and looked at, with the up/down flag recorded | the census files exist; make, model, software version, pixel spacing, bit depth and `PixelIntensityRelationship` written into `README.md` and `MANIFEST_GRID.md` ("not recorded" becomes a name); the ten renders pass by eye | S4 for PACS access, or a letter allowing a technical pilot on fully de-identified exports | Greg; Radiology informatics; the co-investigator (full name and spelling to confirm: `OPEN_QUESTIONS.md` A18 and the formation note) |
| **S4** | Regulatory: fill the Protocol 1 placeholders (faculty sponsor, co-investigators, one records number identical across the WSU form, the protocol and the DMC application: `regulatory/protocols_2026-09/PROTOCOL_1_eProtocol_draft_2026-09-15.md` item 164); submit Protocols 1 and 2 together as the summary states, and Protocol 3 (prospective passive capture of intraoperative C-arm images; "longest lead time, start it first", `IRB_ADDENDUM_2026-09-10.md` edit 3); the Radiology letter on the export path and the co-investigating service's letter; the DMC Research Compliance application with the same names (`regulatory/wsu_dmc_forms/dmc-research-review-process-*.pdf`); disclose the commercial interest in the eProtocol and COI (Greg-only, the addendum); obtain the VinDr-SpineXR determination number (`regulatory/vindr_2026-09-25/`) and print it in `manuscripts/schwingnet/main.tex` line 137, or retrain the fold models without VinDr (the 250 `name_fill` cells already exist: lateral 98.1 %, AP 97.0 %, `RESULTS_CATALOG.md` A9.4) | approval letters; the de-identification plan accepted (OCR screen of every frame: C-arm objects carry no burned-in-text flag, Protocol 1 item 174) | the drafts in `regulatory/`; a faculty sponsor (a resident PI needs one) | Greg; the sponsor; WSU IRB; DMC Research Compliance |
| **S5** | Freeze the DMC reading protocol and the PREREG before the first frame: reference standard = same-patient CT registration where a CT exists (labels agree with the operative note in at least 98 % of vertebrae, Protocol 1 H2), otherwise operative note plus postoperative imaging adjudicated blind; every transitional person read by a human on CT; endpoint per person, all reference-named bodies correct, lateral and AP separately, at detector confidence 0.74 with the 0.25 curve beside it; abstention and stop rates beside every accuracy; intervals clustered by person; the human-read naming convention of `docs/STUDENT_FLUORO_CORRECTION_GUIDE.md`; the per-case form of the QI protocol (`../09_wrong_level_clinical_qi/`) as the scaffold | `PREREG.md` signed by Greg and hashed; the two readers and the adjudicator named (in this private folder only); decide which frame the hospital study scores: naming (paper 1), the comparison (paper 2) or the process (QI) | S4 | Greg; the readers |
| **S6** | Retrospective in-domain test, zero-shot, no fine-tune: run the S2 runtime on every exported lateral and AP exposure of the hospital device that has a reference; stratify ordinary / transitional and instrumented / not (Protocol 1 H3 strata) | pre-stated: ordinary spines, naming per person with its interval, the 96.4 % zero-shot and 97.4 % fine-tuned C-ArmLSpine figures as context only; transitional: 35 error-free persons for the 90 % exact-level bound and 22 carriers for 85 % variant sensitivity (`results/schwingnet/power/power.json#n_needed_zero_errors`), or the sentence "not at parity" with the number (RD section 2.8); detection recall at 0.74 and 0.25 with the curve; the first 12 patients (24 frames) tell whether the device sits near the 81.7 / 85.3 % plateau (`results/schwingnet/indomain/INDOMAIN.md` section 8); at the 12.9 % transitional prevalence recorded in `../02_transitional_naming_truth/` (Nakagawa 2017, `LEVELCHECK_CLAIM.md` section 2) 35 transitional persons are expected among about 270 consecutive lumbar patients (a derivation, not a file) | S2, S4, S5 | Greg (PREREG) |
| **S7** | Fine-tune on the hospital device only if S6 detection or AP naming falls short: the recipe of `spinesurg-ct-nnunet:slurm/carmlspine_cv_v9init.sh` on a person-disjoint split (`code/patient_keys.py`, `code/eval_gate.py`); case-grouped and acquisition-day-grouped folds both reported; pooled never quoted without the device-held-out arm beside it (`memory/pooled-vs-lodo-device-designs.md`) | paired bootstrap of fine-tuned minus zero-shot with an interval excluding zero before any "improves" sentence (`BENCHMARK_PROTOCOL.md` rule 3, in project 03); about 68 persons for 97 % whole-frame AP naming (`INDOMAIN.md` section 8) | S6 | Greg |
| **S8** | Prospective silent evaluation (Protocols 2 and 3): the frozen runtime runs on incoming cases with no output to anyone treating the patient; disagreements with the CT-verified level and the operative note adjudicated afterwards; the QI process measures recorded per case (anchor used, exposures, minutes, dose, needles, disagreements) | the QI protocol's four-month baseline then eight-month assisted phase; primary outcome the surgeon-count versus fiducial disagreement rate with its interval and every case listed; "powered to estimate, not to detect a change in wrong-level events" (E.10) | S4 (Protocols 2-3), S6 | WSU IRB; Greg |
| **S9** | Phantom and cadaver bench for live capture, in parallel: register any X-ray machine used outside a clinical service with WSU OEHS (`regulatory/wsu_dmc_forms/x-ray_machine_registration_form.docx`; the Application for Use of Ionizing Radiation is a separate form); a frame grabber on the auxiliary video output; an anthropomorphic lumbar phantom; then a whole-body cadaver through the Anatomical Gift Program (`regulatory/carm_validation_plan_2026-09-21/`) and the Institutional Biosafety Committee; the guided loop's corpus arms (`HOME/model_night/guided/*`) read first, and only if the `frame` control lands near 85 % (`docs/GUIDED_ACQUISITION.md`) | the capture adapter produces frames that pass the S3 render check; the commanded-step error on a physical gantry measured (the external roadmap cites about 16 mm manual repositioning error against a 21 mm search half-width, `docs/external_reports/C-Arm_Validation_Research_Plan_2026-09-20.pdf`, reference only); geometry recovered on a physical phantom, replacing the synthetic-phantom 1.2 mm | S2; Radiation Safety approval | Greg; WSU OEHS; the Anatomical Gift Program |
| **S10** | Reader study and the comparison (paper 2, project 02; a fourth MRMC protocol later, addendum edit 5): the frozen LevelCheck comparator with human-read transitional persons; fix `SchwingNet/tools/fig6_score.py` (`T1/blinded/meta_ref/` to `T1/open/meta_ref/`) and re-score the open gate first (OQ F3); never release the blinded gate before `CEPH/data/fig6/unblinding/RELEASE_v2.json` is written by a person (`RESULTS_CATALOG.md` B.6) | at least 19 verified at-risk persons with a frame for H1; today 7 unverified (`manuscripts/schwingnet/packet/packet_src/persons_available_2026-09-24.json`) | S5, S6 | Greg; the technology-transfer office's answer on disclosure timing |

## B. Decisions and questions only Greg can answer (OQ part A, the rows that bear here)

| OQ | question | why it matters here |
|---|---|---|
| A1 | Was paper 1 uploaded to Radiology: AI? (the CV says "Submitted"; the repository says held) | if uploaded, the packet that went is stale (13-page supplement, stale ATLAS cards) |
| A5 | The VinDr-SpineXR HPR determination number and date | the one placeholder in `main.tex` line 137; S4 |
| A9 | Yes / no on supplement Table S5 (per level x view x field), the synthetic:real ratio sweep (about 45 cells), seeds 1-2 above N = 25 | no ratio was ever swept (C5); the BUU-all reversal rests on one seed |
| A10 | Apply the "plateau is the truth denominator" text change (`manuscripts/schwingnet/REVISION_LOG3.md` section 11, "NOT yet applied") | the same-device plateau (about 84 %) reads 95.6 % on repaired truth (A8.7) |
| A11, A12 | Reword "7 of 9 cells"; reword "FluoroCap panels are refused by the guard" (the fold models train on 2,100 FluoroCap and 2,632 VinDr crops) | [WORDING] items before any submission |
| A14 | "Surgery" or "General Surgery" for each document (never Neurosurgery) | four superseded manuscript drafts and one data-request placeholder say Neurosurgery (`MANIFEST_LOCAL.md` section 3) |
| A18 | Who is the stage-2 reader "Dr Tech"; the co-investigator's full name and spelling | S3, S5 need named people; the Protocol 1 draft writes "[Dr To]" |
| A19 | Keep or delete the RSNA 2022 cervical archive (237 GB of HOME); is it covered by HPR 2026-269? | quota and IRB scope |
| A26 | Migration decisions: deletions (1,590.3 GB candidates), the B13 results move (627 GB), DUA / EULA folder permissions | `CEPH/data/or_ready` (868 GB) and `HOME/scaling` (129 GB) are this project's |
| A29, A30 | Answered by Greg on 2026-10-12 (issue #68): every Write holder may read all 13 folders, this one included; the withheld personal data stays out (root `CLAUDE.md` rule 12) | this folder stays Greg-only for claiming and hand-outs: a student takes an issue here only after Greg hands it out, with a comment naming the student's login or by removing the label `greg-first` |
| (RD) | The BUU licence: may weights trained with BUU laterals leave the grid? | the v9 bank holds 3,603 BUU laterals; S2 ships weights off the grid to the private HF repository: Greg decides first |
| (PLAN) | Which track the hospital test is on: a research study on the research track is consistent with the two-track rule | the commercial goal appears in no student-facing document |

## C. Facts on the grid, not on the laptop (OQ part B)

B6 result of the re-implemented competitor ensemble (`HOME/model_night/ensemble/ensemble.json`); B7 corpus result of guided
job 40376577 (`HOME/model_night/guided/*`); B8 whether `slurm/runtime_cost.sh` ever ran (no: the file does not exist in
the repository; S1); B9 whether the DeepFluoro cards were refitted under `DF_CONVERSION=linear`; B10 the box convention of
the `scores.json` rows in `MODEL_CARD.md` section 4.6 and why `dc_B_held_cios_fusion_s1` has no row; B11 which held paper-2
job carries the post-section-15 detector; B12 7,045 vs 7,048 physics-styled renders; B13, B14 the 2026-09-17 scaling
sweep's job id and whether `eval_scaling_curves.py cases` ran; B17 which grid copies of `eval_gate.py` and `patient_keys.py`
ran the 2026-09-24 cells; B18 whether `slurm/data_accounting.sh` ran on the real corpus; B19 which COBRA bank the current
detector numbers read; B20 `carmlspine_cv_v9.sh` was run cell by cell as the 250 `name_fill` cells; B21 `~/corpus_final`
(G4) and `sn:results/final/` (G5) do not exist; B22 per-source render counts inside `allspine_v9`; B23 per-source
composition of the body detector's `yolo_v3` / `yolo_v4z` training sets (is AASCE in them?); B24 which bank the fold-0 crop
counts describe (they sum to 31,396, not 31,446); B30 the migration state (B10, B11 for this project); B31 whether
`~/model_registry`, `~/mlflow`, `~/remote_wait.sh` still sit at those paths; B32 why the grid can no longer fetch the
private repository. Each is read with `ls` and log reads in a job or from the scheduler, never Python on the login node.

## D. Analyses never run (OQ part C)

| OQ | gap | what closes it | pre-stated number |
|---|---|---|---|
| C1 | no transitional accuracy on any real image with a human read | human reads of the COBRA candidates through the review tree after the PREREG freeze (project 02, 06) | 22 carriers / 35 at-risk persons |
| C2 | no held-out plain-film naming in paper 1 | score the ImageNet-init G3 arm on G3 test films (f6eval was held) | per project 07 |
| C3 | no per-angle naming | a human level read on the case134 spin, or a second labelled spin | — |
| C4 | per-level film naming on held-out persons | a committed aggregation tool | — |
| C5, C6 | no synthetic:real ratio sweep (no power calculation for it); film N-curve seeds 1-2 at N at least 50 | Greg's A9 | — |
| C7 | the selection effect of the v9 checkpoint on the alphabet-loss L6 recall (56.1 to 72.4 %) | an encoder whose epoch was not chosen on those spines | — |
| C12 | posterior calibration: no reliability diagram, ECE or Brier anywhere (T13: 0 % right at mean top posterior 0.804) | `code/eval_calibration.py` as a job | — |
| C13 | a clean re-run of selective prediction (the 99 % at 35.7 % coverage is on a leaked bank and its own test half) | re-run on the v9 lineage with coverage chosen on a separate split (`code/level_selective.py`); certifying 99 % with zero errors takes about 298 answered cases (E.9) | 99 % selective accuracy |
| C14 | the primary C7 criterion (paired bootstrap of styled-corpus arms against the LODO baseline) was never run | run it | 97 % vertebra and sacrum |
| C15, C16 | the leakage audit over every device-corpus training list; CHK-6 near-duplicates and CHK-7 undeclared aliases | run them (project 10's chain) | 0 cross-split overlaps |
| C17 | the exposure-clip A/B on real frames (typicality gate) | `slurm/device_spread_arm.sh` | — |
| C20 | the v9-bank A5 film re-score (chain 40415667 to 40415670) | read its output | — |
| C10 | the person-level intraclass correlation for transitional endpoints (any two-proportion power) | compute it from the first hospital reads | — |

## E. Unexplained observations and unestablishable facts (OQ parts D, E)

D1 the reported held-out detector finds exactly half the boxes in 15 of 19 angle bins on the case134 spin (flat 49.5 %,
`figures/schwingnet/figS4.record.json`); D6 body word count 2,988 vs 2,998 (run `check_limits.py`); D7 acqcov job id
40436995 vs 40437098 for `coverage.json`. E1 whether the 149 released C-ArmLSpine cases are that many people (only the
dataset authors could say); E20 whether the `ts12` and `v8` overlap corrections changed a printed number after
2026-09-24; E21 whether the 81 SEEN quoted rows are all labelled "not held out" in `main.tex`.

## F. Actions already known to be needed (OQ part F)

F4 trim the supplement to 12 pages, regenerate the ATLAS cards (`atlas/update_cards.py`, `validate_cards.py`), the stale
`.md` twins (`tab3_naming.md`, `tab4_transitional.md`) and the Word packets, add `tabS4_ablation.md` and `.sources.md`,
and trim the panel sidecar `SchwingNet/figures/fig2_pipeline.caption.txt` at the source (61 words by `wc -w` at 097933a;
the copy `figures/schwingnet/fig2_pipeline.caption.txt` here drops "(NCC)" to make 60; `check_limits.py` counts only the
`\caption{}` of `main.tex`, so the limit check never saw the sidecar);
F5 correct the wrong-bank attribution in `slurm/recurrent_head.sh` line 16 and `tools/recurrent_order.py` line 56
(`films_ann`, not `films_all2`); F6 correct Table 1's TotalSegmentator rows and recompute the footnote-j total (4,093
renders) and the abstract from the v9 build roots; F7 fix `tools/xray_dataset_usage.py` (`buu_2000` mislabel); F17 the
`test_leak_check.py` fixture (`geneva:phantom`); F19 `sections/results.tex` L94-97 "a two-labeller count" (4 two-labeller +
3 single-labeller) and the retired key in `NUMBERS.md` L435 and `CLAIMS_LEDGER.md` L271; F20 the `%c` crash in
`stats_compare.py --help`; F21 key `slurm/scaling_sweep.sh` outputs on the base name before any v9 rerun; F10 the login-node
line in `spinesurg-ct-nnunet:CLAUDE.md` and `docs/MODEL_REGISTRY.md`.

## G. Research directions that bear on this project (RD section 6)

| rank | project | first step | gate | n today vs needed | depends on |
|---|---|---|---|---|---|
| 6 | DAT-1: send the drafted requests (`docs/data_requests/`: fourteen cine sources, SX-Stitch, Balgrist; none sent; `MANUSCRIPTS.md` section 16), draft two more (LevelCheck's 178 patients with 398 intraoperative radiographs; Huashan's 140 with CT and intraoperative films), fetch two free items (TCIA CMB XA frames, the NIT Warangal centroid files) | the letters out; "sent" recorded in the manifest card; the "Read once before sending" list binds (commercial-scope sentence, IRB question first, co-authorship offers, Radiopaedia only by application); the Balgrist draft still says neurosurgery resident: fix | a reply naming a DUA route for at least one set of 100 or more living patients | 0 sets vs 19, 35 or 60 persons | Greg's signature |
| 8 | PAR-4: pose quality against naming on C-ArmLSpine, and the 24 sacra called L6 | the exactness-by-NCC-quartile table (two hours); render the 24 sacrum crops and the four off-bone laterals | odds of an error per 0.25 body of disagreement with an interval excluding 1 | 617 lateral and 631 AP bodies; 24 sacra | the per-frame registration scores on the grid |
| 9 | FLU-2: the clean-lineage encoder on G3, validation side, with the count-against-morphology agreement (project 02) | one seed, lambda 0; scored on the 7 render-scoreable of the 11 validation L6 persons | zero or one miss of 7 proceeds; two or more stops (RD 2.8); the count catches at least 80 % of run-shifted films | 7 of 11; about 29 of 43 test persons after "H1 seen" | FLU-1's protocol; the paper 2 ledger; the BUU licence decision before any weight leaves |
| 11 | PAR-5: the real paired probe on C-ArmLSpine (`level_morphometry` on the CBCTs; pose re-fit at 0.150 mm; embedding regression per feature per view) | Q squared above 0.5 on the lateral for any feature beyond height and wedge, or the parity work moves to AP | L1 in 76 lateral frames; L2 to L5 in 123 to 142 | PAR-2's definitions; PAR-4's verdict; CT-1 (project 05) |
| 15 | PUB-1: paper 1's rigor fixes (section H below) and the dataset article resubmission (project 03) | `eval_gate` held out on every quoted row; the seven items to Greg as a list | none by policy | Greg; the TTO answer |

RD section 1 (what is known) is the reading behind `STATUS.md`; RD section 2.2 lists what was tried and failed
(CycleGAN / CUT / ADDA / SDXL, no gain in any arm) and must not be retried without a new reason.

## H. Paper 1: what blocks submission and the redo plan (`MANUSCRIPTS.md` sections 2.6, 2.8, 21)

Seven author decisions fail `packet_src/build_packet_src.py --strict` while open (`manuscripts/schwingnet/packet/packet_src/build/BUILD_REPORT.md`,
2026-09-27): (1) `vindr_irb` (S4); (2) `hf_mirror_v11` (project 03: bring the mirror to v11 under one licence or delete
the sentence); (3) `release_code_weights` (pick WEIGHTS_OPTION_DEPOSIT or WEIGHTS_OPTION_AGREEMENT in `statements.md`;
`MODEL_CARD.md` 1.4 says weights not released, `INVENTION_DISCLOSURE.md` section 9 advises trade secret); (4)
`filing_before_submission` (the provisional first; counsel sees the COI statement); (5) `title_clauses` (`front_matter.json`
still says "robust to transitional anatomy"); (6) `subject_overlap_list` (which of NeurIPS 3474, MLHC 2026, BIBM 2026, the
CNS abstracts to name); (7) `claim_form` (upload `claim_checklist_2024.docx`). Then, in order: ask Greg A1; get the TTO
answer and do nothing public before it; close the seven decisions; correct Table 1 (F6) and the FluoroCap wording (A12);
trim the supplement to 12 pages and regenerate cards and twins (F4); rebuild both copies on the grid one after the other
(`compile.sh` holds a flock), fetch to `packet_build/`, run `check_limits.py` (and with `CAMERAREADY=1`),
`results_macros.py --check`, `build_packet_src.py --strict`, `make_packet.py`, render and look at every page; convert the
remaining hand-typed table cells to `\RESULT{}` keys; settle A9, A10, A11 before any new number enters; verify the journal
limits in a browser. Disclosure first throughout: no SchwingNet, QI, focused or main_v2 text, figure or deck anywhere
public; run `tools/disclosure_audit.py` before any talk or upload.

## I. Not to be carried forward

The 98.22 % v2-lineage cross-validation (`results/carmlspine_v2_lineage_2026-09-21/`, still printed in `tab3_naming.md` and
`atlas/model.json`: A2.9, A3.11); the 99 % at 35.7 % coverage (LEAKED); the "100 % sacrum on DeepFluoro" (a same-device
number, `docs/or_ready_audit_track_2026-09-22.json`); any styled-corpus "design B beats A" (seed spread of the same order,
`MODEL_CARD.md` 4.6); the R + C = 22 rule (`memory/anomaly-rule-rc22-evaluated.md`); any guided-loop corpus number (C3.12
NOT RECORDED); the 734x linker speed-up as a shipped timing (C3.13); CycleGAN / CUT / ADDA / SDXL translation (RD 2.2);
the QI draft's "17 ms per frame" and "about fifteen minutes of fluoroscopic counting" (no file).
