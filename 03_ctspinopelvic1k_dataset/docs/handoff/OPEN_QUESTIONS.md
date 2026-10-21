# Open questions

> **Copied whole into `03_ctspinopelvic1k_dataset` on 2026-10-08.** The path prefixes this file uses (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:` / `context/`, `Desktop/`, `np:`, `~`, `$RS`) and every laptop path it quotes resolve as `PREFIXES.md` says: to a repository at a named commit, to a file in this folder, or to the grid. Nothing in this folder depends on a laptop path (`../../MANIFEST_LOCAL.md` section 3.6).

Everything the six readers could not settle from files on 2026-10-08, deduplicated, with where to look and who can
answer. Source of every row: the "Unknowns" table and the flags of the reader note named in the last column
(`working_notes/topic1_...` = T1, `topic2_...` = T2, `topic3_...` = T3, `topic4_...` = T4, `topic5_...` = T5,
`topic6_...` = T6). Path prefixes and identifier namespaces: `README.md` §0 (row ids here are OQ-A1 and so on when
cited from another file). Rows A29-A30, F17-F23 and part G were added in the verification pass of 2026-10-08
(`README.md` §12); rows whose content is Greg's alone were moved to `GREG_ONLY/PRIVATE_STATE.md` and left here as
pointers.

"Who can answer": **Greg** = only Greg knows or decides; **grid** = anyone with grid access can read it off disk or the
scheduler (in a job or with `ls` / log reads, never Python on the login node); **run** = needs an analysis that has never
been done; **external** = dataset authors, a journal, TCIA, or a browser check.

---

## A. Questions only Greg can answer (ask in week one)

| # | question | why it matters | where to look first | from |
|---|---|---|---|---|
| A1 | Was SchwingNet paper 1 uploaded to Radiology: AI? (ERAS CV says "Submitted"; the repository says held; why: `GREG_ONLY/PRIVATE_STATE.md` §3) | if not, the ERAS CV is wrong; if so, the packet that went is stale | `Desktop/ERAS_2026/CV_2026-09-27.pdf`; `sn:packet_src/build/BUILD_REPORT.md`; `GREG_ONLY/PRIVATE_STATE.md` §3 | T4 |
| A2 | Was the Medical Physics MPDA packet of 2026-09-25 uploaded? Manuscript number? Editorial status? | the article may be under review with known defects (title page role, conflicts, reader wording, overlap sentence) | `ctsp:dist/submission/`; Greg's e-mail | T4, T6 |
| A3 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A4 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A5 | What is the VinDr-SpineXR HPR determination number and date? Answered 2026-10-20: HPR 2026-330 of 29 September 2026 (WSU IRB notice; spinesurg-ct-nnunet's data platform recorded it 2026-10-10) | the one placeholder in `sn:main.tex` (line 137); otherwise retrain the fold models without VinDr (fold models without VinDr or FluoroCap already exist as the 250 `name_fill` cells, REP truth and per protocol cell: `DATASET_USAGE.md` §3.2, §5) | `ctsp:IRB_VinDr_2026-09-25/` (gitignored); IRBQuestions@wayne.edu | T1, T3, T4 |
| A6 | NeurIPS 3474 camera-ready: what is the deadline; were the camera-ready, the Croissant file and the OpenReview note uploaded? | an accepted paper with 134 `[pending]` slots | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`; OpenReview | T4, T6 |
| A7 | Resubmit the cancelled appendix chains (SPINEPS, v11 summaries, total_v3) or cut Appendices I-J? | decides the camera-ready content | `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | T4 |
| A8 | Were BIBM 2026 (5 Jul) and the SPIE MI 2027 abstract (5 Aug) submitted? Was VerSeFusion submitted to NeurIPS D&B? | affects the cover-letter overlap list (decision 6) | `Desktop/NextPaper/bibm-spinopelvic/`; `NextPaper/VerSeFusion/README.md`; the CV | T4, T6 |
| A9 | Yes / no: supplement Table S5 (per level x view x field from `cv_v9.json`); the synthetic:real ratio sweep (`real_share` 0.1-0.9 at N = 25 and all, three seeds, ~45 cells); seeds 1-2 above N = 25 (18 cells x 2 arms) | the BUU-all reversal rests on one seed; no ratio was ever swept | `ssn:docs/RESUME_2026-09-22_PM.md` L35-37 "FOR GREG"; `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` | T1, T2 |
| A10 | Apply the "plateau is the truth denominator" text change? | the same-device detection plateau (~84 %) reads 95.6 % on repaired truth | `sn:REVISION_LOG3.md` §11 ("NOT yet applied") | T2 |
| A11 | Reword the Discussion's "7 of 9 cells" (only six verdict cells lie in "five to twenty-five persons"; the seventh is the reversal)? | [WORDING] | `sn:sections/discussion_motivation.tex` L53-56; `RESULTS_CATALOG.md` A10.9 | T2 |
| A12 | Reword the supplement's "FluoroCap panels are refused by the guard", given the current fold models train on 2,100 FluoroCap and 2,632 VinDr crops? | true at different times; reads as if they could not | `sn:supplement.tex` "Excluded sources"; `sn:main.tex` Ethics | T1, T3 |
| A13 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A14 | Affiliation: "Surgery" or "General Surgery" (never Neurosurgery) for each document | five documents say Surgery, two General Surgery, four Neurosurgery | `MANUSCRIPTS.md` C5 | T4 |
| A15 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A16 | Sign and freeze `ssn:docs/ruleclass/PREREG_rules.md`? | until then every rule number is calibration, not a result | its §9 freeze block | T2 |
| A17 | `greg_verdict` on the registry review queues (546 rendered cases; 0 filled) | transitional truth for paper 2 and the review tree | `sn:results/transitional_registry/REGISTRY.md`, `contact_sheets/` | T2 |
| A18 | Who is "Dr Tech" (full name, department, HF user)? | stage-2 reviewer of the transitional review | `ctsp:Student_Projects/BOARD.md`; RESUME L56, L69 | T2, T4, T5 |
| A19 | Keep or delete the RSNA 2022 cervical archive (237 GB of HOME, used by nothing)? Is it covered by HPR 2026-269? | quota; IRB scope | `DATASET_USAGE.md` §7 | T3 |
| A20 | Should the HF mirror be brought to v11 under one licence, or the mirror sentence deleted? | students on HF get v10 with id 29 | `context/hf-mirror-is-v10.md` (lists the lines to change) | T4, T6 |
| A21 | Drop the JEEHP med-ed manuscript (the study is published in Cureus) or turn it into a follow-up with new data? | duplicate publication | `MANUSCRIPTS.md` §12 | T4 |
| A22 | Post an arXiv replacement of the MPDA? | v1 predates the ten-page cut, the Castellvi five-of-six and the funding line | `ctsp:paper/mpda/ARXIV_SUBMISSION.md` | T4 |
| A23 | Were the CNS slides submitted to the meeting, and by what deadline? | talk on 2 Nov | `context/cns-deck-v2-2026-09-25.md` | T4 |
| A24 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A25 | Push `ctsp:Student_Projects` commit 3f1cf04 (a public repo)? | "pushing a public repo is Greg's call" | `context/lab-recipe-and-board.md` | T5 |
| A26 | Migration decisions reserved to Greg: deletions (1,590.3 GB candidates), B13 results move (627 GB), DUA / EULA folder permissions, the three B14 inspect-only entries, when `~/s1v11` opens to students | storage | `ssn:data_platform/MIGRATION_PLAN.md` §1 | T5 |
| A27 | Should the Castellvi grades that changed after NeurIPS review be reported to the area chair? What PGY year were the two readers? | camera-ready items 13 and 18 | `CAMERA_READY_CHANGES.md` | T4 |
| A28 | moved to `GREG_ONLY/PRIVATE_STATE.md` §3 (Greg only) | — | — | — |
| A29 | Confirm the reader split of this folder (`README.md` top; `GREG_ONLY/PRIVATE_STATE.md` §5); decide whether `HANDOFF/` is committed, and whether `GREG_ONLY/` goes into the same repository | the student-facing files must not state what `GREG_ONLY/` holds; until confirmed, nothing here goes to a student | `GREG_ONLY/PRIVATE_STATE.md` §5-6 | verification |
| A30 | Keep, redact or delete the personal and contact data withheld from the student copies (student usernames with counts; a WSU staff contact; three researchers' e-mail addresses) before any commit | personal data in a repository | `GREG_ONLY/PRIVATE_STATE.md` §4 | verification |

## B. Facts that are on the grid but not on the laptop

| # | question | where to look | from |
|---|---|---|---|
| B1 | What did the ruleclass arms (A, B, pelvis) finish after 2026-09-27? Current counts under `$RS/ruleclass/arms/*`; did `arms/pelvis/_timing/DECISION.json` get written? | `$RS/ruleclass/`; `sacct` | T2 |
| B2 | PANORAMA flags (call 40430888 / summary 40430889 pending on 2026-09-27) and its 1,495 masks | `$RS/data/anomaly_harvest/panorama/` | T2 |
| B3 | The 33-CT difference between `CORPUS.md` (21,655) and the tiers (21,622) | `$RS/ruleclass/CORPUS.md`, `tiers/` | T2 |
| B4 | Which of the 1,186 near-duplicate alias candidates are the same person | `$RS/ruleclass/.../alias_pairs_all.csv` | T2 |
| B5 | The cause of the census table's one-high counts | the grid query behind `ssn:docs/CENSUS_TABLE_2026-09-25.md` | T2 |
| B6 | Result of the re-implemented competitor ensemble (124 cells) | `~/model_night/ensemble/ensemble.json` | T1 |
| B7 | Corpus result of guided-acquisition job 40376577 | its log and output folder | T1 |
| B8 | Whether the runtime GPU / detector job (`slurm/runtime_cost.sh`) ran | logs | T1 |
| B9 | Whether the DeepFluoro device cards were refitted under `DF_CONVERSION=linear` | the grid copy of `docs/devices/`; `$RS/data/or_ready/devices/` | T1 |
| B10 | Box convention of the `scores.json` rows in `MODEL_CARD.md` §4.6; why `dc_B_held_cios_fusion_s1` has no row | `~/spine-detector/runs/devcorpus/*/scores.json` | T1 |
| B11 | Which held paper-2 job (40438005 or 40431765 / 66) carries the post-§15 detector | `JOBS_RECORD_2026-09-27_1544.md`; the job scripts | T1 |
| B12 | 7,045 vs 7,048 physics-styled renders (Table 1 footnote a) | a listing of `~/physics_drr` | T1 |
| B13 | Grid job id of the 2026-09-17 `~/scaling` sweep; whether `fig9_scaling` was drawn (`~/model_night/figures_feasibility/`) | logs; that folder | T2 |
| B14 | Whether `eval_scaling_curves.py cases` ever ran, and its result | `~/scaling_curves/` | T2 |
| B15 | Date, job id and full table of the LSTV flag learning curve | `~/lstv_flag/LEARNING_CURVE.md` | T2 |
| B16 | Whether the nnU-Net ablation array (`ssn:docs/ablations.md`) completed and what it found | `~/ablate/` | T2 |
| B17 | Which grid copies of `eval_gate.py`, `patient_keys.py` etc. ran the 2026-09-24 cells | the grid checkout's git log | T2 |
| B18 | Whether `slurm/data_accounting.sh` ever ran on the real corpus | `$RS/data/or_ready/data_accounting/` | T3 |
| B19 | Whether the grid `tools/realxray_banks.json` lists `cobra_elekta_v3` and `cobra_elekta_g3test`; which COBRA bank the current detector numbers read | the grid checkout | T3 |
| B20 | Whether `slurm/carmlspine_cv_v9.sh` itself was ever run (`carm_cvdaymix0_v9` exists). Partly answered 2026-10-08: its recipe was run cell by cell as the 250 `name_fill` cells (`ssn:tools/indomain_name_fill.py` L26-28, L869-873; `sn:slurm/name_fill.sh` L25, L42), which are v9-base fold models | `~/carm_cv*_v9*` | T3 |
| B21 | Whether `~/corpus_final/` (G4) or `sn:results/final/` (G5) exist | the grid | T3 |
| B22 | Per-source render counts inside `allspine_v9`; whether `physics_drr`'s 1,321 implant renders come from `implant_ct`, `implant_ts` or both | the bank's `meta.json` / case arrays | T3 |
| B23 | Per-source composition of the body detector's `yolo_v3` / `yolo_v4z` training sets (is AASCE in them?) | `~/spine-detector/data/yolo_v3`, `yolo_v4z` | T3 |
| B24 | Which bank MODEL_CARD's fold-0 crop counts describe (they sum to 31,396, not 31,446) | the fold bank's `meta.json` | T3 |
| B25 | RSNA census: 2,022 study directories vs 2,019 train studies; what besides the zip fills 236.8 GB | `$RS/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl`; `du` | T3 |
| B26 | Spinal-AI2024: 20,001 files on disk vs 20,000 released | the raw tree | T3 |
| B27 | Whether `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv` were recomputed on v11 anywhere | `~/CTSpinoPelvic1K/morphometrics/` on the grid | T6 |
| B28 | Whether `data/v5_final` and `data/zenodo_deposit` still exist in the grid CTSP checkout (the `ctsp:slurm/*.sh` defaults) | the grid | T6 |
| B29 | Whether the ostk canal-closing regression is fixed in the grid copy `~/OpenSpineToolkit` | its files | T5 |
| B30 | Migration batch state after 2026-10-08 (last recorded: B00, B01, B02, B03, B06, B08, B14 cut over; B04, B07, B09 copying); **B01 is contradictory in its own note**: cut over, yet the dedup census found the TCIA CT Colonography raw DICOM (721 GB) and `tcia_nifti` (336 GB) on neither HOME nor Ceph, with nothing recording what removed them (re-acquisition route `tcia_ctsp_download`); whether `$RS/data/_index/holding.sqlite` was built | `plan/runs/<B>/STATUS`; `$RS/data/_index/`; `context/data-platform-migration-2026-10.md` (13:34 rewrite) | T5 |
| B31 | Whether `~/remote_wait.sh`, `~/model_registry`, `~/mlflow` still sit at those paths after the migration | the grid | T5 |
| B32 | Why the grid can no longer fetch the private spinesurg repository | the grid checkout's remote config and credentials (do not print them) | T5 |
| B33 | Docker Hub tag or digest behind the current `spinesurg-ct.sif`; the GPU model behind gvohp | the `.sif` metadata; `sinfo` | T5 |
| B34 | The current approved Beethoven roster | the access service (not the vendor folder, which is never read) | T5 |

## C. Analyses never run (gaps in the evidence)

| # | gap | what would close it | from |
|---|---|---|---|
| C1 | No transitional (L6 / T13) accuracy on any real image with a human read | human reads of COBRA candidates through the review tree after the PREREG freeze | T1, T2 |
| C2 | No held-out plain-film naming in paper 1 | score the ImageNet-init G3 arm on G3 test films (f6eval was held / cancelled) | T1 |
| C3 | No per-angle naming | a human level read on the case134 spin, or a second labelled spin | T1, T2 |
| C4 | Per-level film naming on held-out persons | a committed aggregation tool on held-out persons (only the derived selection-split Table E exists) | T1, T2 |
| C5 | No synthetic:real ratio sweep; no power calculation for it | A9 | T2 |
| C6 | Film N-curve seeds 1-2 at N >= 50 | A9 | T2 |
| C7 | The selection effect of the v9 checkpoint on the alphabet-loss L6 recall (56.1-72.4 %) | an encoder whose epoch was not chosen on those spines | T1 |
| C8 | The anterior pelvic plane angle for the cohort (aSS = SS - APPA) | fit the APP from the hip labels | T6 |
| C9 | An LSTV-stratified PI sensitivity analysis | recompute PI with each candidate S1 end-plate | T6 |
| C10 | The person-level intraclass correlation for transitional endpoints; power under the `LEVELCHECK_MODEL.md` §15 detector | needed for two-proportion power and paper 2 | T2 |
| C11 | A whole-cohort Castellvi read of CTSP (33 graded against 71-142 expected) | a reader study | T2 |
| C12 | Calibration of the posterior (no reliability diagram, ECE or Brier anywhere) | a calibration analysis | T1 |
| C13 | A clean re-run of selective prediction (the 99 % at 35.7 % coverage is on a leaked bank and its own test half) | re-run on the v9 lineage with coverage chosen on a separate split | T1 |
| C14 | Primary C7 criterion (paired bootstrap of styled-corpus arms against the LODO baseline) | run it | T1 |
| C15 | E3: the leakage audit over every device-corpus training list; designs A and B lack the design-P refusal | run it; add the refusal | T3 |
| C16 | CHK-6 (near-duplicates) and CHK-7 (undeclared aliases) | the content chain on the real corpus | T3 |
| C17 | The exposure-clip A/B on real frames (typicality gate) | `ssn:slurm/device_spread_arm.sh` | T1 |
| C18 | PolyPose validation (`VALIDATION.{json,md}` does not exist); whether a bank was used in training | the validation chain `slurm/polypose_validate_submit.sh` | T6 |
| C19 | The Dataset813 numbered-rib folds: finished? scored? (the CNS 66629 title and the RPPR claim a single-shot model) | `~/spinesurg-ct-nnunet/nnunet/results/Dataset813*` | T4 |
| C20 | The v9-bank A5 film re-score (chain 40415667 -> 40415670) | its output | T4 |
| C21 | Self-tests and any run of `tools/transitional_review/` (untracked); the outcome of workflow wf_ded52e0e-cd1 | its journal; `--selftest`; commit the folder | T2 |
| C22 | Whether the CNS student abstract numbers predate the estimator and canal / end-plate fixes | recompute each against v11 and the fixed estimators | T4 |

## D. Unexplained observations (recorded, not guessed)

| # | observation | where | from |
|---|---|---|---|
| D1 | The reported held-out detector finds exactly half the boxes in 15 of 19 angle bins on the case134 spin (flat 49.5 %) | `sn:figures/figS4.record.json` (`real_lodo_flat_half`) | T1, T2 |
| D2 | ostk's 2026-09-10 shard run produced pedicle widths for about 2 of ~5,600 level-instances (`PDW` empty in all 4,744 committed rows) | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` "Pedicle width" | T6 |
| D3 | The splitter flagged record 0500 as L6 though its label has no id 25 | `ctsp:paper/mpda/main.tex` Data Format | T6 |
| D4 | Which two records besides the 44 plate-gate rejections lack PI (802 - 44 - 2 = 756) | `ctsp:morphometrics/surgical_morphometrics.csv` | T6 |
| D5 | 221 (CSV) vs 222 (CLAUDE.md, commit 2232bde) degenerate S1 carves | `ctsp:morphometrics/s1_carve_audit.csv` | T6 |
| D6 | Body word count 2,988 vs 2,998 | run `sn:tools/check_limits.py` | T1 |
| D7 | acqcov job id 40436995 (topic 1) vs 40437098 (`PENDING_JOBS.json`) for `coverage.json` | `sn:results/coverage/PENDING_JOBS.json` | T1, T2 |

## E. Facts that cannot be established from any file

| # | fact | why | from |
|---|---|---|---|
| E1 | Whether the 149 released C-ArmLSpine cases (148 scored; `LEAKAGE.md` §3 says what 149, 148 and 141 count) are that many people | no patient field; cases are acquisitions on five dates; only the dataset authors could say | T1, T2, T3 |
| E2 | Whether the 768 numeric-id and 34 `CTC-` CTSP records include the same human | settled only by a TCIA query | T6 |
| E3 | The PGY year of the two Castellvi readers | no record found | T4 |
| E4 | What the `cm_spine` Drive file is | the download never landed | T3 |
| E5 | Why 2,293 DeepFluoro vendor frames, the BUU AP films, the BUU (2000) labels and `synth_rare` are unused | no written criterion exists | T3 |
| E6 | Who rebuilt `ctsp:paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` at 2026-10-08 09:41 | file timestamp only | T4 |
| E7 | Live state of Zenodo v11 and the HF mirror today | no network was used; open https://doi.org/10.5281/zenodo.22797014; if the concept DOI resolves to v10, the merge step of `RECIPES.md` §9.1 applies to the Zenodo labels too | T4, T6 |
| E8 | Barr 2026's de novo value at n = 700 | flagged in the deep-research report for checking before quoting | T2 |
| E9 | Vialle 2005 sample size, 260 or 300 | two CTSP documents disagree; not checked against the paper | T6 |
| E10 | Location of `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_*.md` | named in the NeurIPS change log, found in no scratchpad | T4 |
| E11 | Where the MLHC decision letter and reviews are | outcome only in memory | T4 |
| E12 | Which Desktop `MDPA*.pdf` is the submitted version | `ctsp:dist/submission/` holds the packet | T6 |
| E13 | Final state of each of the 125 source-GT corrections | every row of `ctsp:docs/CORRECTIONS.md` still reads "pending (in review)" | T6 |
| E14 | Which script made the committed `fig_hardware.pdf`; the exact command behind `label_census_v11.csv` | two candidates each | T6 |
| E15 | The submitted text of the twelve CNS abstracts; the content of the LITT deck v6 | titles only on disk | T4 |
| E16 | Visibility and role of `lstv-detector`, `spinesurg-ct-annotator`, `CTSpinoPelvic1K-Syn`; which ostk `projects/` folders hold working code. (`NextPaper/spinopelvic-seg`: the NeurIPS camera-ready cites `OpenSpineConsortium/spinopelvic-seg` as the public code repository, `ctsp:` commit 70de829; only its live visibility is unverified) | not recorded | T5, T6 |
| E17 | Full ids of the Claude Docs "handoff c3c7acfd..." and "literature state 3b03e849..." | memory names prefixes only | T5 |
| E18 | Whether `git` is tolerated on warrior | not on the quoted ban list; never tested | T5 |
| E19 | The current state of the six unreviewed `pelvic_native` cases and the 16 zero-thoracic cases; how the 0787 lumbar-rib disagreement was resolved | `ctsp:docs/RELEASE_CHECKLIST.md`, `LAB_JOURNAL.md` | T6 |
| E20 | Whether the `ts12` and `v8` overlap corrections changed a printed number after 2026-09-24 | `MANUSCRIPT_CORRECTIONS.md` §2.3-2.4 (read in outline) | T1 |
| E21 | Whether the 81 SEEN quoted rows are all labelled "not held out" in `sn:main.tex` | the manuscript workflow owns it | T3 |

## F. Actions already known to be needed (no question, just not done)

| # | action | where | from |
|---|---|---|---|
| F1 | moved to `GREG_ONLY/PRIVATE_STATE.md` §2 (Greg only) | — | — |
| F2 | Copy the NeurIPS recomputation scripts out of the Temp scratchpad into the repository; commit the 2026-09-27 camera-ready edits | `MANUSCRIPTS.md` §7 | T4, T6 |
| F3 | Fix `sn:tools/fig6_score.py` (`T1/blinded/meta_ref/` -> `T1/open/meta_ref/`) and re-score the open gate | `sn:paper2_levelcheck/open_gate_40438004/README.md` | T1, T4 |
| F4 | Trim the SchwingNet supplement to 12 pages; regenerate the ATLAS cards, the stale `.md` twins, the Word packets; add `tabS4_ablation.md` and `.sources.md` | `MANUSCRIPTS.md` §2.6 | T1, T4 |
| F5 | Correct the wrong-bank attribution of the 98.7 / 99.1 / 99.4 recurrent head in `ssn:slurm/recurrent_head.sh` line 16 and `ssn:tools/recurrent_order.py` line 56 (films_ann, not films_all2) | `RESULTS_CATALOG.md` C1.2 | T1 |
| F6 | Correct Table 1's TotalSegmentator rows, and recompute the footnote-j total (4,093 renders) and the abstract from the v9 build roots (it counts `ts_drr` and `ts_drr_v3`, which v9 never reads, and omits `physics_drr` and `physics_rare`); correct `MODEL_CARD.md` / `DATASHEET.md` (device corpus is TS v3) | `DATASET_USAGE.md` §6; `RESULTS_CATALOG.md` A18.2, A18.5 | T3 |
| F7 | Fix `ssn:tools/xray_dataset_usage.py` (`buu_2000` mislabel; substring keys) | `DATASET_USAGE.md` §8 | T3 |
| F8 | Fix ostk: port the lowest-lumbar footprint isolation for S1 on v11 and flag the fallback; fix the 1b7005c canal regression (test: case 0097 within 1 mm); update `SPEC.md` / `README.md` / `CLAUDE.md` | `RESULTS_CATALOG.md` G.2-G.3 | T5, T6 |
| F9 | Recompute the sacrum-adjacent CSVs on v11 | `RESULTS_CATALOG.md` F.44 | T6 |
| F10 | Update stale entry documents a student reads first: `ctsp:README.md` (v5), `STATUS.md`, `docs/ROADMAP.md`, `paper/mpda/REPRODUCE.md` (§0, §2), `zenodo/README.md`, `zenodo/KNOWN_ISSUES.md` (v10; add mirrored CTs, 0533, COLONOG_299 L5), `ssn:README.md` (dataset link, "under audit"), `sn:README.md`, `sn:figures/FIGURES.md`, `ssn:docs/MODEL_REGISTRY.md` and `ssn:containers/build_container.sh` (login-node instructions); **`ssn:CLAUDE.md`**, which every Claude session in this repository loads: it runs `~/mambaforge/envs/spineps/bin/python .../pipeline_state.py` over ssh on the login node (python is killed there by name) and does not point at `HANDOFF/README.md`: give it the `sbatch` form and the pointer; check `ostk:CLAUDE.md` the same way (F8) | `working_notes/topic5`, `topic6` flags; verification 2026-10-08 | T5, T6 |
| F11 | Gitignore or move the personal and administrative files at the root of the public `CTSpinoPelvic1K-1` repository | `INFRASTRUCTURE.md` §1 | T6 |
| F12 | Commit `ssn:tools/transitional_review/` and `ssn:docs/REVIEW_TRANSITIONAL.md` (untracked) after their self-tests pass | `RECIPES.md` §3.3 | T2 |
| F13 | Fix the census table's off-by-one before anything else copies it (the CNS table already did) | `RESULTS_CATALOG.md` D.13 | T2 |
| F14 | Re-key the identity tables of `PATIENT_IDENTITY_SPEC.md` into `ssn:tools/identity/` (empty) | `LEAKAGE.md` §7 | T3 |
| F15 | Memory hygiene: index `fluorocap-pipeline-resume`, fix three broken wikilinks (a fresh project now loads `context/INDEX.md`; the original `MEMORY.md` is archived in `GREG_ONLY/context/`), remove the banned word from the originals and from 10 spinesurg and 29 CTSP tracked files | `CONTEXT_EXPORT.md` §5 | T5 |
| F16 | Correct the MPDA "This work received no funding" line (the title page names NIH F30GM147909) and the Figure 3 caption ("digitised from Figure 4A") | `MANUSCRIPTS.md` §6 | T6 |
| F17 | `ssn:tools/test_leak_check.py` fails (L312, "30 real names, 1 wrong": `phantom_p01_065kv -> geneva:phantom want geneva:phantom_p01`). The keyer changed on purpose (the Geneva resin phantom is one person, `sn:results/eval_gate/EVAL_LEAKS.md` item 3); the fixture still expects the old per-position key. Greg approves changing the fixture to `geneva:phantom`, or the test stays a known failure | `ssn:tools/test_leak_check.py` | verification |
| F18 | `python -m pytest` in `ostk:` gives 1 failed, 100 passed: `tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs` (`value` is None with flags `sagittal_ref_fallback`, `no_levels_available`; the test removes labels 11 and 12, the legacy femur ids). Cause not investigated | `ostk:tests/test_cobb.py` L91 | verification |
| F19 | `sn:sections/results.tex` L94-97 calls the seven real-frame candidates "a two-labeller count"; they are 4 two-labeller + 3 single-labeller (`RESULTS_CATALOG.md` A16.6). `sn:NUMBERS.md` L435 and `sn:CLAIMS_LEDGER.md` L271 still point at the retired key `figures/figure5.record.json#numbers_on_figure/counts_and_intervals`; repoint them to `sn:packet_src/persons_available_2026-09-24.json` [WORDING] | those files | verification |
| F20 | `ssn:tools/stats_compare.py --help` crashes (`TypeError: %c requires int or char`): the `certify` subcommand help at L1220 has an unescaped "99 % claim" (write `%%`) | that file | verification |
| F21 | `ssn:slurm/scaling_sweep.sh` writes to output paths that do not depend on `BASE` and skips existing outputs, so a v9 rerun can silently return the v2 curve; key its outputs on the base name before any rerun (`RECIPES.md` §1.8) | that file | verification |
| F22 | `ssn:tools/anomaly_manifest.py` defaults `--bank` to the deleted `~/allspine_v5_fov96_ctx/rung_1.npz`; change the default to v9 or make it required | L553 | verification |
| F23 | The NHANES twin count (48 of 54) was measured on v6 and v7 only; `ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` names v5 nowhere, so whether v5 carried the twins is not recorded | that file | verification |

## G. Where a verifier was wrong or partly wrong (2026-10-08)

Every finding of the three verifiers was checked against the files it cited before anything changed (`README.md` §12).
Most were right. These were not, or only partly:

| # | finding | what the files show | what was done |
|---|---|---|---|
| G1 | `DATASET_USAGE.md` §3.1: "`sources.json` records '7,048 ... ctsp 3,754, ts 1,831, verse 1,463' and has no implant split" | partly wrong: the `physics_drr` card in `ssn:data_platform/sources.json` holds both, `contents.items` = "7,045 anns: ctsp 2,430, totalseg 1,831, verse 1,463, implant 1,321" and, in its location notes, "7,048 physics-styled renders: ctsp 3,754, ts 1,831, verse 1,463 (corpus_census.md 3)" | both cited, with `ssn:docs/DATA_COMPLETENESS_AUDIT.md` L627; the gap stays `RESULTS_CATALOG.md` A18.4 |
| G2 | `MANUSCRIPTS.md` header: "the last commits touching main.tex, sections or supplement are 7e81dd7 and 05e05dc" | partly wrong: `git log -- SchwingNet/main.tex SchwingNet/sections SchwingNet/supplement.tex` lists 7e81dd7 (13:17) as the last; 05e05dc (13:30) rebuilt both copies and serialised the compile without touching those paths | the header names 7e81dd7 as the last manuscript commit and 05e05dc as the rebuild of record |
| G3 | `RECIPES.md` §1.2, §2.1: the prep jobs "`rm -rf` the shared inputs (base_cache, base_val, folds/drr$K, folds/ctx$K)" | partly right: `sn:slurm/name_fill_prep.sh` L27 removes `folds/drr$K`, `folds/ctx$K` and the fold views on every run; `sn:slurm/film_ncurve_prep.sh` removes `base_cache` and `base_val` only when `base_cache/base_train.npz` is missing (L26-33) and keeps `cells.json` when the prep outputs exist | §0 item 6 states each script's behaviour |
| G4 | `context/data-platform-migration-2026-10.md`: "contradicts README §3 and INFRASTRUCTURE §4, which list B01 as cut over" | partly: the live note itself records both B01 cut over and the CT Colonography trees on neither HOME nor Ceph, so the contradiction is inside the note | both readings given in `README.md` §3 and B30; unresolved |
| G5 | `OPEN_QUESTIONS.md` F10 "leaves out `ssn:CLAUDE.md`" | right, but `INFRASTRUCTURE.md` §3 and §13 row 5 did record the conflict | added to F10 |
| G6 | `RECIPES.md` §5: "name_fill.sh, the film N-curve and carmlspine_cv_v9init.sh all read that encoder as INIT" | partly wrong: `name_fill.sh` (L26) and `carmlspine_cv_v9init.sh` (L43) read `runs/model_rung_1_aug2.pt` as INIT; the film N-curve reads the v9 bank (`rung_1.npz`, `meta.json`, `ssn:tools/film_ncurve.py` L59-102) and trains its own render-only encoder. The blocker stands: `rm -rf "$CTX"` deletes both | the row names which job reads which |
