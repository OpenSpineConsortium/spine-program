# PLAN: the division of the spine programme into project folders

Written 2026-10-08 for `C:/Users/grego/OneDrive/Desktop/spine-program/` (one private GitHub repository; Greg pushes it).
This is the plan the builders execute. It decides the project list, the triage order, what each folder absorbs, and
the rules every folder obeys. The row-level disposition of every inventory row is `DISPOSITION.tsv` beside this file;
what stays out is `EXCLUDED.md`; what the three root files must say is `ROOT_FILES.md`.

**Sources.** The seven inventory notes and TSVs under
`C:/Users/grego/AppData/Local/Temp/claude/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/seed/notes/`
(1,385 rows: carm_hospital_path 111, ctsp_repo_root_and_sibling_folders 154, desktop_root_loose_files 207, grid_manifest 237,
inventory3_other_spine_folders 100, memory_and_handoff_map 367, spinesurg_ct_nnunet 209; counted 2026-10-08), the two proposals
under `.../scratchpad/seed/proposals/` (angle A "deployment first", angle B "salvage first"), and the handoff
`C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/` at commit 097933a (`README.md` section 5, `RESULTS_CATALOG.md`,
`OPEN_QUESTIONS.md`, `RESEARCH_DIRECTIONS.md` section 6, `MANUSCRIPTS.md` section 21, read directly on 2026-10-08).
Every number below names its file; "not recorded" means no file on the laptop or the grid records it.

**Prefixes.** `ssn:` = `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet` (private, branch `L6_Class`, commit 097933a);
`sn:` = `ssn:SchwingNet/`; `ctsp:` = `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1` (public, `master`, 7ddfe38, working tree
modified); `ostk:` = `C:/Users/grego/OneDrive/Desktop/OpenSpineToolkit` (public, `main`, cb43197); `xrsp:` =
`C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K` (private, `main`, 4f22935); `np:` = `C:/Users/grego/OneDrive/Desktop/NextPaper`;
`mem:` = `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/`; `HANDOFF/` = `ssn:HANDOFF/`;
`RC` = `HANDOFF/RESULTS_CATALOG.md`; `OQ` = `HANDOFF/OPEN_QUESTIONS.md`; `RD` = `HANDOFF/RESEARCH_DIRECTIONS.md`;
`HOME` = `/wsu/home/go/go24/go2432`; `$RS` = `/rs/rs_grp_oschome/go2432`. Hospital = Wayne State University School of
Medicine / Detroit Medical Center, Department of General Surgery.

---

## 1. The division in one table

Thirteen folders: twelve projects in triage order and one archive. Rank is by how likely the folder is to return a real
result from what is on disk and on the grid, with two exceptions stated in section 4: the C-arm path (01) is first by Greg's
instruction, and the transitional truth file (02) follows it because it is the pre-registered endpoint of the hospital
test rather than because it is likely to reach its bounds. The three support projects (10, 11, 12) are not hypotheses and
sit after the research projects; 10 is the dependency of nearly everything and its first steps run in week one regardless.

| rank | folder | title | reader | likelihood in one line | depends on |
|---|---|---|---|---|---|
| 01 | `01_carm_level_detection` | Intraoperative C-arm level detection: from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital | Greg-only | engineering steps S0-S2 likely within weeks; the hospital number gated by an unknown device and IRB lead time | 10, 02, 08 (only if a device card is chosen), 09 (the per-case form), 12 (the client) |
| 02 | `02_transitional_naming_truth` | Transitional-aware naming and the real-frame truth file (paper 2) | Greg-only | unlikely to reach its pre-stated bounds from the holding (0 verified persons against 22 or 35); likely to return a decisive screen number cheaply | 06, 10, 01, 08 |
| 03 | `03_ctspinopelvic1k_dataset` | CTSpinoPelvic1K: release v11, the dataset article and the NeurIPS camera-ready | student-safe after redaction | highest: one paper accepted, one submitted; editing, a rebuild and Greg's answers remain | 10, 05, 04, 06 |
| 04 | `04_openspinetoolkit` | OpenSpineToolkit: the v11 defects and their tests | student-safe | high and bounded: every defect has a one-hour test with a number; blocks 05 | 03 (v11 labels) |
| 05 | `05_ct_morphometry_parity` | CT morphometry, the spinopelvic estimator and 3-D to 2-D parity | student-safe | high for a number within days (PAR-1 is one laptop hour, RD section 6 rank 1) | 04, 03, 10, 02 (the 2-D side), 08 (exact-pose renders) |
| 06 | `06_transitional_ct_census` | The transitional census: harvest, registry, ruleclass arms and the review tree | student-safe after redaction | medium: the machine side is nearly done; the result needs readers (0 of 546 verdicts filled) | 10, 03, readers |
| 07 | `07_plain_film_level_id` | Plain-film level identification and the radiograph corner detector | Greg-only | medium: held-out corner numbers are real; the film naming numbers are leaked or wrong-bank; venue windows passed | 10 (B04, B05), 03, 01, 04 |
| 08 | `08_render_devices` | Image formation: DRR banks, device cards, PolyPose and synthetic-to-real | Greg-only | low as a claim (styled corpora failed the pre-stated 97 % on two of three devices), medium as support for 01 and 05 | 10, 03, 02 |
| 09 | `09_wrong_level_clinical_qi` | Wrong-level surgery: the iliac-crest paper, the scoping review and the QI protocol | Greg-only (QI text); the review and the clinical paper may be split out later | medium-low near term: the iliac-crest number is v5-era, the review needs human charting, the QI protocol waits on 01 S8 | 05, 01, Greg |
| 10 | `10_data_platform_grid` | The data platform: 211 sources, the Ceph migration, identity and leakage, grid operations | student-safe after Greg confirms OQ A29 | support; mechanical and high (three migration jobs were running at 22:20 UTC on 2026-10-08) | Greg's per-batch decisions |
| 11 | `11_students_grid_access` | Students on the grid: Beethoven, onboarding, the lab recipe and the med-ed record | Greg-only until the six Beethoven notes are redacted; the guides student-safe | support; operational (release 14.0.0 in field use) with two unfixed field failures | 10 |
| 12 | `12_website_pacs_demo` | The public site, the PACS demo and the level-service client | student-safe | support; operational (PACS demo 1,360 ms); the level service is not live | 01 (the service), 04 (the exporter), 05 (the atlas), 11 |
| 99 | `99_archive` | Archive: superseded, refuted and dormant work kept as a record | Greg-only | not a project to work; a record with the reason each item is here | none |

The inventory family tokens map to folders one to one: carm_detection -> 01, transitional_fluoro -> 02, ctsp_dataset -> 03,
toolkit -> 04, ct_morphometry_parity -> 05, anomaly_scan_census -> 06, plain_film_level_id -> 07, render_devices -> 08,
qi_wrong_level -> 09, data_platform -> 10, grid_access_students -> 11, website -> 12, archive -> 99, exclude -> `EXCLUDED.md`.

Row counts from `DISPOSITION.tsv` (1,369 rows after merging 16 exact duplicates of the 1,385 inventory rows; built by
`scratchpad/plan_build/build_disposition.py`, 83 row-level overrides): 01 288 (copy 197, reference 87, not copied 4);
02 43 (26 / 14 / 3); 03 169 (93 / 64 / 12); 04 17 (10 / 6 / 1); 05 33 (21 / 11 / 1); 06 91 (36 / 55 / 0); 07 67 (29 / 38 / 0);
08 71 (33 / 37 / 1); 09 9 (7 / 1 / 1); 10 157 (131 / 24 / 2); 11 44 (29 / 14 / 1); 12 12 (7 / 4 / 1); 99 57 (20 / 36 / 1);
excluded 311 (305 excluded outright, 6 referenced by path only).

---

## 2. The rules the builders follow

1. **One row, one place.** Every row of `DISPOSITION.tsv` names exactly one `project_folder` (or `EXCLUDE`) and one `action`.
   `copy` lands under `dest_relpath` in that folder; `reference` becomes a row in that folder's `MANIFEST_CODE.md` (a file in a
   repository), `MANIFEST_GRID.md` (a grid path) or `MANIFEST_LOCAL.md` (a laptop file kept by path); an `exclude` under a
   project folder becomes a "not copied, and why" row in that folder's `MANIFEST_LOCAL.md`; an `EXCLUDE` row lands only in
   `EXCLUDED.md`. A folder row stands for its files. The `reason` column carries the inventory row ids (`[carm r9; ...]`),
   the inventory's own token and action, and `|| decision:` where this plan overrode it.
2. **Deliberate duplicates, recorded.** Four kinds of duplication are allowed and every instance is written in the reason
   column: (a) the 22 standing-rule memory notes tagged `all` go into every folder's `memory/`; (b) a memory note may sit in
   several folders' `memory/` when the per-project cut lists of `memory_and_handoff_map.md` say so (its row home is its
   first family); (c) the HANDOFF rule below; (d) a handful of small documents copied into two folders because both must be
   self-contained (named in `DISPOSITION.tsv`: the four morphometry documents of `ctsp:docs/` into 03 and 05, the Castellvi
   csv files into 03 and 06, `pipeline.md` and `troubleshooting.md` into 01 and 10, `or_ready_audit_track_2026-09-22.json`
   into 01 and 08, `PHYSICS_LINKING.md` into 01 and 08, `XRAY_DATASET_USAGE` and `MANIFEST_DATA_MODELS_RESULTS` into 01 and 10).
   Nothing else is copied twice; everything else is cross-referenced by path inside the repository.
3. **The HANDOFF rule.** The eight student-readable HANDOFF files (`README.md`, `GLOSSARY.md`, `RECIPES.md`,
   `RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md` with its section 9 already
   moved out) are copied whole into every project folder's `docs/handoff/` (about 350 KB per folder), so a student with one
   folder has the catalog, the recipes and the open questions. The Greg-only HANDOFF files (`MANUSCRIPTS.md`,
   `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md` + `literature_state/`, `working_notes/`) are copied
   whole into the Greg-only folders 01, 02, 07, 08 and 09 only; the student-safe folders 03, 04, 05, 06, 10, 11, 12 receive
   the sections that bear on them as extracts with row ids in `STATUS.md` and `TODO.md` (the section-to-family map is the
   "HANDOFF sections by family" table of `memory_and_handoff_map.md` and the 201 `HANDOFF/` rows of `memory_and_handoff_map.tsv`).
   `HANDOFF/GREG_ONLY/` is never copied; it is referenced by path from 01 and from `EXCLUDED.md`.
4. **STATUS.md, TODO.md, MEMORY.md are extracts with ids.** `STATUS.md` = the RC rows named for the folder, each with its
   id, file and rigor mark (CURRENT / HELD OUT / [AUTO-TRUTH] / [THR] / SUPERSEDED / LEAKED / RECORD ONLY). `TODO.md` = the
   ordered steps of section 3 below, then the OQ rows, RD items, `MANUSCRIPTS.md` section 21 items and the repositories' own
   plans named for the folder, each with gate, pre-stated success number, dependency and who decides. `MEMORY.md` = the
   index of `memory/` with the `HANDOFF/context/INDEX.md` status of every note carried verbatim (CURRENT, DATED, PARTLY
   SUPERSEDED, SUPERSEDED, LEAKED, RECORD ONLY, DORMANT) and the replacement named where one exists.
5. **Memory notes.** Copy from `HANDOFF/context/` (the redacted copies with statuses), not from the live folder, after running
   `python HANDOFF/working_notes/builders/refresh_context.py` then `build_context_index.py` (the live
   `data-platform-migration-2026-10.md` changed at 16:43 after the 16:39 copy; `memory_and_handoff_map.md` "Rules"). Four live
   notes the copier did not redact (`grid-access-list-gate`, `rib-qc-gates-never-block-lstv`, `xray-corner-detector-status`,
   `beethoven-2026-10-02-field-failures`) and the six Beethoven notes (`ashley-bridge-project`, `ashley-compliance-boundary`,
   `ashley-extension-project`, `beethoven-2026-10-02-field-failures`, `beethoven-browser-ssh`, `beethoven-first-run-ux`, which
   exist only in `GREG_ONLY/context_beethoven/` and the live folder) are redacted by hand before copy: student usernames and
   first names, Greg's personal e-mail, a tester's e-mail, licence key ids, the Cloudflare account, token paths. The redacted
   copy of `learned-formation-refuted-calibrate-instead` still names a DMC clinician in its deliverables paragraph: strike it.
   The five Greg-only notes (`commercialization-stance`, `schwingnet-disclosure-scrub`, `hf-org-token-location`,
   `hf-osc-token-and-namespace`, `fluorocap-credentials-and-resolution`), the seven U251 / LITT notes, the six history-only
   resume notes and the live `MEMORY.md` are never copied.
6. **Copy rules (the task's list, applied).** Never: imaging data (nii, nii.gz, dcm, npz, npy, h5, mha, large png sets, zips
   of data), model weights, anything under `.git`, environments, caches, logs over 2 MB, any file over 25 MB (recorded in
   `MANIFEST_LOCAL.md` as reference-by-path with its size), credential or token files, anything under
   `C:/Users/grego/.beethoven-vendor`, personal and administrative material, U251 and LITT, `private_ip/` and the signed
   disclosure forms, student names and usernames, researcher and personal e-mail addresses. Files over 25 MB that the
   inventories found and the plan references by path: `sn:figures/*.tif` (3.5-39 MB), `sn:results/eval_gate/touched.json`
   55.3 MB, `sn:results/learning/*.npz` 31.8-32.8 MB, `sn:results/manifold/deep.npy` 124.1 MB, `sn:results/reader_e/features_j1.csv`
   40.3 MB (its `.gz` twin is copied), nine `ssn:spine_data_review/runs/*/records/hf.jsonl`, the two SchwingNet packets of 89 MB,
   `np:viz/*_lstv_3d.html` 26-40 MB each, `xrsp:dataset2024.zip` 4.0 GB, `CTSP1K_private/CTSpinoPelvic1K_prepurge_20260911.bundle`
   97.8 MB (`spinesurg_ct_nnunet.md` section 4; `inventory3_other_spine_folders.md`; `ctsp_repo_root_and_sibling_folders.md`).
7. **Redactions, by kind never by value.** Each folder's `MANIFEST_LOCAL.md` records every file copied with a redaction:
   the fluoroscopy data-request drafts (25 distinct addresses replaced by the institution; `spinesurg_ct_nnunet.md` section
   3.2), the VinDr cover note and the HPR 2026-144 tool (a phone number), the Protocol 1 draft (staff work e-mails cut, roles
   kept), `IRB_ADDENDUM.md` (an IRB office contact), the X-ray machine registration form (document metadata naming two
   staff), `ctsp:docs/castellvi_readers_2026-09-04.csv` and `ctsp:Lumbosac.csv` (reader initials replaced by A/B/C), the
   `email_*.md` and `COLLABORATOR_TASKS.md` of `ctsp:docs/`, `proposals/student_primer_email.md` and
   `cm_spine_request_email.md`, `np:action_items.txt` (two first names), `np:bibm-spinopelvic/main.tex` (a personal e-mail),
   the collaborator-named `.docx` in `nsurg/AACA` (renamed `collaborator_draft.docx`), the ten notes of rule 5. The banned
   word (the French-derived word for where data came from) is rewritten as origin, lineage, source or "where it came from"
   in the 10 tracked `ssn:` files, the 29 `ctsp:` files, `np:README.md`, `np:VerSeFusion/README.md` and
   `CTSpinoPelvic1K-Syn/README.md` that carry it; a repository-wide grep is the last step of every build. The affiliation
   reads Neurosurgery in `ssn:paper/rsnai/main_v2.tex`, `ssn:paper/qi_universal_protocol/main.tex`, the Balgrist draft and the
   TechFair deck: every copy's `MANIFEST_LOCAL.md` says so and every new sentence says General Surgery.
8. **Each project folder holds** `CLAUDE.md`, `README.md`, `MEMORY.md` + `memory/`, `MANIFEST_GRID.md`, `MANIFEST_CODE.md`,
   `MANIFEST_LOCAL.md`, `TODO.md`, `STATUS.md`, and `docs/`, `results/`, `figures/`, `manuscripts/`, `code/` as the TSV routes
   them, `regulatory/` where IRB material lands (01, 07), `manuscripts/talks/` for decks, `docs/handoff/` for the HANDOFF
   copies. `code/` files carry a header with the source path and commit (097933a, 7ddfe38, cb43197, 4f22935) or "untracked
   2026-10-08" or "working tree, uncommitted edit" (the five edited `ssn:tools/*.py`: `level_prototype`, `carmlspine_eval`,
   `patient_keys`, `pipeline_state`, `test_patient_keys`). `MANIFEST_GRID.md` rows come from `grid_manifest.md` sections 2-6,
   `ssn:data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md`, `plan/batch_items/*.tsv`, `dedup/`, `HANDOFF/INFRASTRUCTURE.md`
   and the memory notes, each with what it holds, size where a file records one, migration state (batch, VERIFIED / ABSENT /
   copying / not started) and whether a job verified it; the one read-only grid pass of 2026-10-08 22:20 UTC
   (`scratchpad/seed/grid_ls_2026-10-08.out`) is copied into 10 so no folder re-runs it.
9. **Readers.** "Student-safe" means the folder may be handed out once Greg confirms the reader split (OQ A29, A30) and the
   redactions above are done; "Greg-only" means it holds SchwingNet or level-identification content, invention aspects,
   regulatory drafts with staff roles, or private draft text, and is never handed out. The whole repository is private; the
   label is about hand-outs.
10. **The standing rules every `CLAUDE.md` restates in its own words** (from `HANDOFF/README.md` section 5, `ctsp:CLAUDE.md`
    and the task): never the banned word; no fractional version numbers; figure captions at most 60 words; plain sentences;
    every number with its file and "not recorded" where none exists; check outside the computation, because the recurring
    failure is a number that is wrong but plausible (published values, an independent implementation, the spread not the
    median, a published prevalence; render the mask); two label schemes exist and mixing them does not raise, call
    `ostk.labels.labels_for(volume)`, identifier 29 is retired in v11 and code that gates on it goes, `zfill(4)` the case ids,
    canonicalise to RAS to analyse and never reorient when writing; held out means the person was never seen by the checkpoint
    or any ancestor, every quoted score goes through `ssn:tools/eval_gate.py`, never quote the leaked banks (allspine v2, v6,
    v7, v8 for VerSe, `anchor_drr`, `vindrps`); pre-register then score, numbers enter text through a manifest key; nothing
    runs on the login node, `sbatch -D`, `afterany`, `/dev/shm`, Ceph for large outputs, bash 4.2; SchwingNet and all
    level-identification code, text, figures and weights stay private; use all of a public dataset, fix or justify every
    truncation; network through WSL; tokens read from files only, never echoed; commit only when Greg asks; Ashley Schehr
    is a person, never a product name; the affiliation is General Surgery (Wayne State University School of Medicine /
    Detroit Medical Center), never Neurosurgery.

---

## 3. The projects

### 01 `01_carm_level_detection`: intraoperative C-arm level detection, from SchwingNet as it stands to a model tested on real fluoroscopy at the hospital

**Goal.** Take the reported SchwingNet stack (naming detector `detector_v5z_final`, sacrum and vertebra detector
`rx_lodo_carmlspine_1024`, level encoder `allspine_v9` rung 1, the BiGRU head, the count from the sacrum, alphabet coupling
and the stop signal; `HANDOFF/DATASET_USAGE.md` section 1; `carm_hospital_path.md` section 1.1) from four weight files on
the grid and a container that serves an older release, to a frozen, registered, latency-measured runtime whose output has
been read by humans against a pre-registered endpoint on exposures from the C-arm actually used at Wayne State / DMC,
under an approved protocol, with the device card or capture adapter, the reader protocol, the PREREG and the sample size
written before the first frame is scored.

**Reader.** Greg-only.

**Why it is likely or unlikely to work.** The model is real and held out on one unseen C-arm: 595 of 617 lateral vertebrae
exact (96.4 %, Wilson on effective n [92.3, 98.4]; RC A2.1; `sn:results/eval_gate/leaks/zeroshot_v9.json`); fine-tuned
five folds 601 / 617 = 97.4 % [93.2, 99.0] (A3.1); count from the sacrum 979 / 1,009 = 97.0 % (A4.7); coupled 98.2 %
(A5.1); the stop signal fires on 23 / 233 frames and catches 5 of 6 erring frames (A5.3). Against it: AP naming zero-shot
276 / 631 = 43.7 % (A2.2); detection on the held-out device 80.5 % at 0.74, short of the pre-stated 97 % (A6.1; 93.9 % on
the repaired denominator, A6.5); every C-ArmLSpine truth is automatic, no human has read a level on any real intraoperative
frame (`ssn:docs/MODEL_CARD.md` section 5.1; [AUTO-TRUTH] on every row); the hospital C-arm make and model are not recorded
in any file (`carm_hospital_path.md` section 2); no capture path from a C-arm exists in code; `ssn:service/` serves
`detect_v5z_epoch25` + M19 with no sacrum count, coupling or abstain flag (`HANDOFF/context/level-service-serving.md`);
the end-to-end latency of the reported stack on uncontended hardware was never measured (MODEL_CARD section 6.3, 6.6; no
`HOME/bench/runtime_cost.json`); three DMC protocol drafts exist and none is recorded as submitted; 0 verified real at-risk
persons against the 35 and 22 the pre-stated bounds need (`sn:results/power/power.json#n_needed_zero_errors`; A16.5).
S0 to S2 need only grid time and are likely within weeks; the hospital number comes only after IRB approval and a device
census.

**Families absorbed.** carm_detection (305 inventory rows across the seven TSVs; 288 after merging): `sn:` the manuscript,
results, figures, tables, packets; `ssn:docs/` model card, datasheet, deployment evidence, the physics and linking line,
sweep, count and guided documents (invention aspects: PRIVATE banner on the copies), prior art, the cine harness, the data
requests (redacted); `ssn:service/` and `tools/deploy_service.py`; `ssn:results/physics/`; `paper/rsnai/` and `paper/focused/`
as `manuscripts/superseded/`; the 19 pipeline scripts and the untracked cine tools into `code/`; the local
`Desktop/spine-detector/src/` snapshot into `code/spine_detector_src_snapshot/` (no `.git`, commit unknown;
`manifest.py::canonical_slots` is the slot order the runtime must respect); the whole `HANDOFF/` except `GREG_ONLY/`;
`ctsp:` the regulatory documents and the external reports (`C-Arm Validation Research Plan.pdf`, the five documents inside
`Untitled_Message.zip`, `Feasibility_FOV.docx`, `MULTI_XR.docx`, the two landscape PDFs with author addresses struck); the
private CNS deck v10; the 48 memory notes of the carm cut list with their statuses.

**`regulatory/`.** HPR 2026-144 letter (`ctsp:IRB Not HPR Determination 4.21.26.pdf`, 2,088,991 B; phone redacted; one copy for
three byte-identical paths), HPR 2026-269 memo (`ctsp:2026 269 Schwing IRB Not HPR Determination 9.2.26.pdf`, 670,187 B; one
of two identical twins), the filled tool (`ctsp:OSC_HPR_Determination_public_datasets.pdf`, 556,822 B;
`Desktop/hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf`), `ctsp:IRB_VinDr_2026-09-25/` (three PDFs; cover note
with the phone number cut; zip dropped), `ctsp:proposals/irb/PROTOCOL_1_eProtocol_draft_2026-09-15.md` (roles kept, staff
e-mails cut) and `IRB_two_protocols_summary.{pdf,docx}`, `ctsp:IRB_ADDENDUM.md` (edits 1-5; IRB office contact cut;
Greg-only), `ctsp:DUA.pdf` (header: generated advice, not an executed agreement), `ctsp:proposals/FluoroCap_HPR_attachment.md`,
`ssn:docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` (phone redacted), `CTSP1K_private/proposals_backup_20260911/irb/`
(IRB_PLAN.md, PROPOSAL_SHORT.md, the summary; EMAIL.md excluded), `Desktop/IRB/spine_study_protocol.{docx,pdf}` and
`Data_Collection_Tool.*` (March 2026), the DMC research-review process PDFs and the WSU IRB pages of `Desktop/IRB/`,
`Desktop/CTSpinoPelvic1K/IRB_IRB-26-03-8648_SubmitPreApproval.pdf` (outcome not recorded), the blank WSU HPR forms,
`Desktop/x-ray_machine_registration_form.doc` (metadata stripped), `Desktop/wsu_patent_policy.pdf`. By path only:
`ctsp:VAIDYAS_IRB.pdf` and `Desktop/IRB/Retrospective IRB PROTOCOL.pdf` (other investigators' protocols),
`ctsp:COMMERCIALIZATION.md` (never in a project folder), `ssn:docs/INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`,
`provisional/`, `disclosure_*`, `PATENT_PACKAGE.md` (Greg's private filing material).

**Grid paths it owns** (`grid_manifest.md` section 3.1; `carm_hospital_path.md` sections 1.1, 4.9). Weights:
`HOME/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` (42,233,939 B, registered);
`HOME/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt` (40,601,637 B, no sha256 in the registry);
`HOME/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (44,824,746 B, alias 188f9fcbfa3c6de1);
`HOME/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` (8,473,727 B; the folder was not reached by the
listing, not verified); the fold models `HOME/carm_cvmix{0..4}_fov96_ctx` (3.37-3.41 GB each; VinDr and FluoroCap crops
inside) and `HOME/model_night/heads_carm/`; `dc_P_pooled`. Data: `$RS/data/carmlspine` 86.834 GB (case134 headers carry a
real PatientID: never print); `$RS/data/realxray` 3.408 GB (23 banks; no `cobra_varian`); `$RS/data/cobra2026` 808.615 GB;
`$RS/data/deepfluoro_h5` 5,272,150,583 B B00 VERIFIED; `deepfluoro_vendor` 110.987 GB; `geneva_hip_src`, `ljubljana`,
`spinesac`; `$RS/data/external/fluoro_video` 262.801 GB. Results: `$RS/data/or_ready` 867.951 GB (paper 1's result root);
`HOME/model_night` (`PIPELINE_STATE.md`, `heads_carm/`, `guided/`, `fiducial/`); `HOME/bench` (`latency.json` 2026-09-13 on the
older stack, `runtime_cost_workstation.json`; no `runtime_cost.json`); `HOME/level_id_service`; `HOME/scaling` 129.2 GB; the
identity tables (`HOME/split_final.json` 8,065,646 B, `patient_keys*.json`); `HOME/model_registry` (ledger 106 lines, 79
aliases). `HOME/corpus_final` does not exist (G4 never built). Migration: the carm banks are B10 and the identity tables B11,
neither started.

**Repositories referenced** (`MANIFEST_CODE.md`): `spinesurg-ct-nnunet` `L6_Class` 097933a (the grid checkout is at 4e3fe93 and
cannot fetch the private remote; ship by `git archive | ssh tar`, `HANDOFF/RECIPES.md` section 0); `OpenSpineConsortium/spine-detector`
(private; the grid `HOME/spine-detector` has `.git`); `openspineconsortium.github.io` `pacs/remote.js` (the service client);
HF private `gregoryschwingmdphd/level-id-weights` (serves the older release).

**First five steps** (`carm_hospital_path.md` section 3; S5-S10 go into `TODO.md` after them):

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| S0 | freeze and register the reference stack: `python tools/model_registry.py register` for `rx_lodo_carmlspine_1024`, the five v9init fold encoders and heads, `dc_P_pooled`, with `--metrics`; add `seed` and `code_sha` to `devcorpus_train.py` and the CV scorer; commit or copy the five edited and three untracked C-arm tools | every weight the paper quotes has a `registry.jsonl` line with a sha256; `git status` clean for the C-arm tools | nothing | engineering; Greg commits |
| S1 | measure the uncontended latency: the `MODEL_CARD.md` section 6.6 job written as a file, `eval_runtime_cost.py --selftest`, then the GPU job `--frames $RS/data/realxray/carmlspine/images --bodies 6 --threads 1 4 16`; `cine_latency.py` on the case134 spin | `HOME/bench/runtime_cost.json` with the detector stage present and `machine_load_*` empty; the per-exposure time written beside the 20 s to one minute the surgeons stated (MODEL_CARD section 6) | S0 | engineering |
| S2 | package the reported stack into `service/`: `detector_v5z_final` + v9 encoder + v9 head + sacrum detector + count + coupling + abstain + the attenuation and window conversion of `REAL_XRAY_DATASETS_SPEC.md`; `deploy_service.py` writes `registry.json`; weights stay in the private HF repo | parity with `level_prototype.py` on 50 evenly spaced C-ArmLSpine frames: boxes equal, names and abstain flags identical, largest posterior difference below 1e-5 (the gate `cine_latency.py` defines) | S0 | engineering; hosting is Greg's |
| S3 | discover the hospital device: which OR C-arms the co-investigating service uses; whether exposures reach PACS as XA / RF / SC; a header census of ten archived exposures per device with `tools/device_census.py`; ten exposures through `level_prototype.py` bone-bright and head-up, rendered and looked at | the census files exist; make, model, software, pixel spacing, bit depth and `PixelIntensityRelationship` written into `README.md` ("not recorded" becomes a name); the ten renders pass by eye | S4 for PACS access, or a letter allowing a technical pilot on de-identified exports | Greg; Radiology informatics; the co-investigator |
| S4 | regulatory: fill the Protocol 1 placeholders (faculty sponsor, co-investigators, one records number across the WSU form, the protocol and the DMC application), submit Protocols 1 and 2 together and Protocol 3 (prospective passive capture, "longest lead time, start it first", `IRB_ADDENDUM.md` edit 3); Radiology and co-investigating-service letters; DMC Research Compliance; the VinDr determination number obtained or the fold models retrained without VinDr (OQ A5; the 250 `name_fill` cells exist, A9.4) | approval letters; the de-identification plan accepted (OCR screen of every frame) | the drafts above; a faculty sponsor | Greg (a resident PI needs a sponsor); WSU IRB; DMC |

Then S5 freeze the DMC reading protocol and PREREG (signed and hashed; 35 error-free persons for the 90 % bound, 22 carriers
for 85 %; two readers and an adjudicator named in the private seed only), S6 the retrospective zero-shot test stratified
ordinary / transitional, S7 fine-tune only if S6 falls short (person-disjoint split, both fold groupings, paired bootstrap
before any "improves"), S8 the prospective silent evaluation under the QI frame, S9 the phantom and cadaver bench for live
capture (OEHS machine registration first), S10 the reader study and paper 2 (fix `sn:tools/fig6_score.py` first, OQ F3).
Not carried forward: the 98.22 % v2-lineage CV, the 99 % at 35.7 % coverage, the "100 % sacrum on DeepFluoro", any
styled-corpus "B beats A", the R + C = 22 rule, any guided-loop corpus number, the 734x linker speed-up as a timing,
CycleGAN / CUT / ADDA / SDXL translation (`carm_hospital_path.md` section 3 "What not to carry forward").

**Dependencies.** 10 (B10, B11; the identity tables; the grid checkout behind the laptop), 02 (any transitional claim at the
hospital and the paper 2 "H1 seen" ledger), 08 (a device card only if the styled route is chosen after S3), 09 (the per-case
QI form as the S5 / S8 scaffold), 12 (the service client).

### 02 `02_transitional_naming_truth`: transitional-aware naming and the real-frame truth file (paper 2)

**Goal.** Name the level correctly on a transitional spine (L6, T13, sacralised L5, four-lumbar) from C-arm exposures at
parity with an ordinary spine, or write "not at parity" with its number (Greg's standing determination of 2026-09-23,
`HANDOFF/context/lstv-tltv-detection-goal.md`; RD section 2.1). The folder owns the real-frame transitional truth file
(FLU-1), the clean-lineage encoder on the G3 split (FLU-2), paper 2's frozen comparator and reader protocol
(`sn:LEVELCHECK_MODEL.md`, frozen 2026-09-23 by commits ecae75f to d0403de, never edited), the automated-reference
calibration, the dual-loss and alphabet-loss arms, and the power inventory.

**Reader.** Greg-only; the reader-protocol documents may go to the readers.

**Why it is unlikely to reach its bounds and still worth second place.** The pre-stated bounds cannot be reached from the
holding: 0 verified real at-risk persons against 35 for the 90 % exact-level bound and 22 carriers for 85 % sensitivity
(`sn:results/power/power.json#n_needed_zero_errors`; RC A16.5); 7 unverified with a frame, 4 two-labeller and 3
single-labeller (`sn:packet_src/persons_available_2026-09-24.json`; A16.6); the expected COBRA yield at the labeller's PPV of
10 of 24 is about 5 to 13 verifiable on CT, at most 19, and "22 cannot be reached from COBRA alone" (RD section 6 rank 3);
49 of 54 G3 L6 validation and test people sit in the v8 / v9 training lineage (D.6), so FLU-2 starts from ImageNet; the
three real L6 patients read classifier 0 of 5, coupled 1 of 5 (A5.5); the 97.6 % comparator "cannot be exceeded at any
reachable n" (E.6). What it returns soon and decisively: the FLU-2 validation screen (zero or one miss of 7 render-scoreable
L6 persons proceeds, two or more stops; RD section 2.8), the one-hour COBRA coverage render, and the 11 field-supported
COBRA L6 calls that RD section 6 calls "the single most decisive afternoon in the holding". It is second because the hospital
test's pre-registered endpoint (01 S5, S6) is transitional, and 01 cannot write that PREREG without this folder's truth
file, reader protocol and power table.

**Families absorbed.** transitional_fluoro (42 rows; 43 after the row moves): `sn:paper2_levelcheck/`, `LEVELCHECK_MODEL.md`,
`LEVELCHECK_CLAIM.md`, `results/fig6/` top-level md and json (the `frozen/` 62 MB and `verification/` 69 MB trees by path;
`.gitattributes -text` travels with any copy), `results/auto_reference/` (Dawid-Skene PPV 0.971; no rule reaches 0.90 for L6
or T13), `results/rare_class/` (`split_plan.md`; `transitional_subtypes.*` 194 persons), `results/dual_loss/`,
`results/learning/` md and json (five `.npz` by path), `ssn:reader_space/` app (not `_original_space/`),
`HANDOFF/LITERATURE_STATE.md` + `literature_state/` (`power.md`, `power_calc.py`), `working_notes/t2_wilson_check.py`; `code/`:
`film_ncurve.py`, `auto_reference_calibrate.py`, `verification_pages.py`, `transitional_detectors.py`, `rare_class_*.py`,
`score_m1_f1.py`, `pool_variant_cv.py`; the 9 memory notes of the transitional cut list. Not copied, listed:
`Desktop/FluoroCap_reading`, `FluoroCap_screening` (3 of 64 and 2 of 104 pages; dormant; licence-bearing images).

**Grid paths it owns** (`grid_manifest.md` section 3.3): `$RS/data/fig6` 13.920 GB with `HOLD_README.txt` and `unblinding/`
(`RELEASE_v2.json` must be written by a person before the blinded gate opens; RC B.6); `$RS/data/or_ready/{auto_reference,
dual_loss, alphabet_loss, v9}`; registry aliases `head_fig6_g3clean_*` (21), `bank_g3_v2_rung_1_g3clean_aug2`, `det_g3_primary_s0`;
`HOME/split_final.json` (the frozen G3 split; a rerun of `g3_split.sh` overwrites it with no backup, `RECIPES.md` section 3.1);
`$RS/data/cobra2026` (shared with 01; validation and test 175 cases embargoed to 2032-03-01); `$RS/data/rare_class` 5.797 GB;
`HOME/physics_rare`; `$RS/data/realxray/carmlspine` (the three one-labeller L6: case42, case121, case136); `HOME/lstv_flag`
(flag models registered; `LEARNING_CURVE.md`); `HOME/FluoroCap` 316 GB (test set only; B09 copying).

**Repositories referenced.** `spinesurg-ct-nnunet` 097933a (`rare_class_*.py`, `transitional_detectors.py`,
`eval_transitional*`, `lstv_flag_*.py` (the refuted 2-D flag line), `sn:tools/fig6_*`, the slurm of
`spinesurg_ct_nnunet.tsv` row 155); the FluoroCap documents live in 99.

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | the one-hour COBRA coverage render: project the Dataset803 sacrum and L5 labels of ten planning CTs through their RTK geometry onto their own Elekta projections and render (RD section 2.7) | by eye: sacrum and L5 inside the field on the exported frames, or COBRA is not spine data for the sacrum anchor | 10 (the collections on Ceph) | engineering |
| 2 | freeze the reading protocol: `ssn:docs/REVIEW_TRANSITIONAL.md` and `docs/ruleclass/PREREG_rules.md` section 9 freeze block signed and hashed (OQ A16) | sha256 in the freeze block; until then every number is calibration | 06 (the review tree) | Greg |
| 3 | the 63-volume reader queue (57 field-supported COBRA calls, 3 re-reads, 3 C-ArmLSpine CBCTs) through the two-stage review tree, read on the CT, truth tier per person; yield in two columns (confirmed on CT; scorable on an exported frame); the 11 field-supported COBRA L6 calls first | 22 carriers with a frame, or the written sentence that no fluoroscopy transitional sensitivity can be claimed and DAT-1 is the only route | step 2; readers | Greg adjudicates |
| 4 | fix `sn:tools/fig6_score.py` (`T1/blinded/meta_ref/` -> `T1/open/meta_ref/`) and re-score the open gate's dumps (OQ F3; RC B.5) | the reference-standard score of gate 40438004 written beside the harvest-name score | nothing | engineering |
| 5 | FLU-2: train the ResNet-18 two-channel encoder from ImageNet on G3 training persons only, renders and films mixed per batch, one seed at lambda 0; score the 7 render-scoreable of the 11 validation L6 persons; submit, estimate wall time, write job ids and ETA to the resume file, stop | zero or one miss proceeds to three seeds, two heads and `alphabet_couple.py` on the same frames; two or more misses stops the arm; no test person is scored before the paper 2 ledger carries "H1 seen" (`sn:PAPER1_SCOPE.md`); the BUU licence read before any weight leaves the grid | step 2; 10 (B10 / B11) | Greg (licence, ledger) |

**Dependencies.** 06 (candidates, registry, the review-tree code), 10 (G3 split and identity tables), 01 (the shared stack and
`alphabet_couple.py`), 08 (`physics_rare` renders), readers (stage 1 Ashley Schehr, stage 2 "Dr Tech", whose full name is not
on disk, OQ A18), Greg's BUU licence decision.

### 03 `03_ctspinopelvic1k_dataset`: CTSpinoPelvic1K, release v11, the dataset article and the NeurIPS camera-ready

**Goal.** Close out the public dataset: the Medical Physics Dataset and Software Article (third packet built 2026-09-25,
upload not recorded; `HANDOFF/MANUSCRIPTS.md` section 6), the accepted NeurIPS 2026 Evaluations and Datasets paper 3474
(poster, OpenReview D8yRWDAGQF; camera-ready working copy with 134 `[pending]` slots; section 7), the Zenodo v11 deposit
(10.5281/zenodo.22797014, published 2026-09-18; `MANUSCRIPTS.md` section 20 C1) against a Hugging Face mirror still at v10
with id 29 (`context/hf-mirror-is-v10.md`), `KNOWN_ISSUES.md` and the release documents, and a reproducible build chain
(`ctsp:paper/mpda/REPRODUCE.md`).

**Reader.** Student-safe after redaction (the coauthor Word dumps and reviewer names stay out; `COMMERCIALIZATION.md` and
`IRB_ADDENDUM.md` are not here).

**Why it is likely to work.** Highest in the set: one paper accepted, one submitted, and what remains is editing, a rebuild
and Greg's answers (OQ A2, A6, A7, A20, A22, A27). Numbers in hand: 802 records (RC F.1); v11 spinopelvic over 756 records
PI 52.1 +/- 11.1, SS 36.6 +/- 10.6, PT 15.5 +/- 7.9 against Veilleux 52.1 / 36.5 / 15.6 (F.21;
`ctsp:morphometrics/surgical_morphometrics.csv`); 5,751 of 5,753 evaluable ribs match (F.9); Castellvi consensus on 34
records, kappa 0.737 (F.14); `build.sh --reprint` gives 10 published pages (rebuilt 2026-10-08 09:41, by whom not recorded, OQ
E6). Open defects that must be fixed, not disclosed: NeurIPS headline defects A (TotalSegmentator sacrum 0.817 counts its S1
class as a miss) and B (two window definitions subtracted) still in the main text (F.47); the MPDA acknowledgements say
"no funding" while the title page names F30GM147909 (OQ F16).

**Families absorbed.** ctsp_dataset (163 rows; 169 after moves): `ctsp:paper/mpda/` (tex, bib, `REPRODUCE.md`, `PLAN.md`,
`build.sh`, `make_submission.py`, `make_arxiv.sh`, the figure makers, `tools/`, `figures/`, the compiled article, reprint and
reprint-check PDFs; the three `_*` coauthor folders by reference; `_schehr/crossref/*.bib` copied); `CAMERA_READY_NEURIPS/`
from the working tree (the untracked `src/appendix/` 11 tex and `fig_app_construction.pdf`; the tex modified after 7ddfe38);
`ctsp:docs/` (61 tracked + 5 untracked; redactions per section 2 rule 7); the root md, `CITATION.cff`, `LICENSE`, `NOTICE`;
`results/`, `hardware_review/` csv, json, README (renders by path; `verify/` nii excluded), `qc_final/`, `qc_hardware/`;
`zenodo/README.md`, `zenodo/KNOWN_ISSUES.md`, `data/zenodo_deposit/{manifest.json, splits_5fold.json, dataset_labels.json,
SHA256SUMS.txt, KNOWN_ISSUES.md}`, the ITK-SNAP descriptors; the root QC tables (`Lumbosac.csv` with reader initials renamed;
`spine_tampering.csv` not copied); the case-0816 and 0068 scripts and json (volumes excluded); the four `scratchpad/` review
reports; the manuscripts `arxiv_final_draft_9_19_2026.pdf` (arXiv 2609.22760), `3474_Not_All_Spines_Are_Create.pdf`,
`MLHC_2026_Research_Track_Paper.pdf` + text + three rebuttals (rejected; never "under review"), `Desktop/MDPA_FINAL.pdf` (the
submitted 21 September build, only copy), `Desktop/MDPA_AI.pdf` and the GPTZero scan (AI-text records),
`Desktop/CTSpinoPelvic1K_submission/` (the 2026-09-07 as-submitted package), `LAB_JOURNAL_2026-08-19.pdf`,
`spinopelvic_rotation.mp4`; `manuscripts/talks/cns2026/`: `CNS2026_Schwing_NotAllSpines_public_v12.pptx` (the only deck for
2 November), `CNS2026_Schwing_LSTV.pptx` (draft, not presented), `ctsp:paper/cns2026/` generators (minus `abs418_tables.json`);
`Desktop/NeurIPS/` `bm/`, `audit/`, `ens/`, `pred/` (per-case evidence behind the camera-ready; which checkpoint made `ens/` and
`pred/` is not recorded), the `lstv_review/` tool packet; `Desktop/SpineSurg-CT/` the March 2026 arXiv draft, `labnotebook/`
memos, `metadata_colonog.csv`, `data_split.txt`; `np:AR/` (NeurIPS draft frozen 2026-09-08, superseded record), `np:RadAI/`
(`main.tex` with `\todo` results, the CLAIM 2024 map of 42 items), `np:manifest.csv` (1,153 rows, ids unpadded, superseded),
`np:flip18_review/` forms and QC png, `np:viz/index.html`, `ACRIN-6664_protocol.pdf`, `TCIA-CTC-large-10-mm-polyps.xls`;
`Desktop/itksnap_review/README.md` + `labels_review.txt` (the 0008 reasoning and the house rule "anchor at S1, count up; a rib
never renames a vertebra"); from `ssn:`: `benchmark/`, `scripts/`, `containers/`, `docker/`, `data/README.md` (its label table
is the OLD ten-class scheme, L1 = 1: the copy says so in its first line), `docs/BENCHMARK_PROTOCOL.md`,
`COMPETITOR_BENCHMARK.md`, `ablations.md`; the 36 memory notes of the ctsp cut list (`annotator-roster` from the redacted copy;
`cns-deck-v2-2026-09-25` moved here from archive because the talk is live until 2026-11-02).

**Grid paths it owns** (`grid_manifest.md` section 3.4): `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` 196,195,055,488 B,
2,417 files, B02 VERIFIED (the only grid copy of the 802 CTs and the v11 labels); `ctspinopelvic1k_build_tree/derived`
(`build_archive` 6,236,530,062 B = Zenodo 22647933 staging; `s1v11` 1,189,924,200 B restricted, byte-identical to the release
labels; `qc_2026-06-12.tar.gz` 196,147,947 B); `$RS/data/ctsp0533_repair` 0.604 GB; `tcia_ct_colonography/meta` (the only TCIA
material left; raw 721 GB and NIfTI 336 GB ABSENT, B01); `HOME/CTSpinoPelvic1K` checkout at a0c5139 (behind 7ddfe38; holds
`.token`, a credential, and a stray directory named `"\`); `HOME/spinesurg-ct-nnunet/nnunet/raw` Dataset802/803/804/810/813/815
(imagesTr links resolve only in the container); `nnunet/results` 348.6 GB (802/810/813; no 815; whether 813 finished is not
recorded, OQ C19); `$RS/neurips_v11` 10.174 GB, `neurips_tsv3` 2.250 GB, `neurips_spineps`, `$RS/data/ctsp_april` 86.883 GB
(world-writable); `HOME/ablate` 201.6 GB (five arms; outcome unread, OQ B16); `HOME/bench` 35.845 GB (its C-arm files are also
listed in 01); `HOME/spinopelvic-seg` 27 GB; `$RS/cns2026_posterior`; the review Space trees (usernames; never copy).

**Repositories referenced.** `CTSpinoPelvic1K` `master` 7ddfe38 (remotes `origin` and `osc`; `scripts/` 267 incl.
`label_scheme.py`, the `extract_*.py` chain of `REPRODUCE.md`, `build_*.py`, `benchmark_*.py`, `select_anchor_cases.py`;
`slurm/`, `tests/`, `zenodo/`, `hf/`, `review_service/`, `reviewtool/`); `spinesurg-ct-nnunet` 097933a (the nnU-Net tools and
slurm arrays); `OpenSpineConsortium/spinopelvic-seg` `main` c105981 (the Dataset803 pseudolabeller the camera-ready cites; live
visibility unverified, OQ E16); `Gregory-Schwing-MD-PhD/VerSeFusion` 2b21cc4; `Gregory-Schwing-MD-PhD/SpineSurg-CT` 0051074;
`Desktop/CTSpinoPelvic1K` (older clone 4fb4a62, an ancestor).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | ask Greg OQ A2 (MPDA uploaded? number?), A6 (NeurIPS deadline; camera-ready, Croissant, OpenReview note uploaded?), A7 (resubmit the cancelled appendix chains, jobs in `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`, or cut Appendices I-J), A22 (arXiv replacement) | answers written into `STATUS.md` with dates | nothing | Greg |
| 2 | NeurIPS camera-ready: commit the 2026-09-27 working tree; rescue the recomputation scripts from the Temp scratchpad into the repository (OQ F2; RC F.48); fix defects A (TS whole sacrum = union of `sacrum` and `vertebrae_S1`) and B (one window definition); settle items 16-24 of `CAMERA_READY_CHANGES.md` | zero `[pending]` slots; content inside the venue limit; captions at most 60 words by the project counter; every number from a file in the repo; uploaded only on Greg's word | step 1 | Greg |
| 3 | MPDA: the corrections of `MANUSCRIPTS.md` section 6 (role, conflicts versus the disclosure, reader wording, the overlap sentence, the mirrored CTs, the Figure 3 caption "digitised from Figure 4A" -> Panjabi Table 3, the funding line, OQ F16); rebuild | `build.sh --reprint` = 10 published pages with the whole build output read; `audit_ms.py`, `audit_artifacts.py`, `audit_pdfs.py` pass; packet regenerated from Windows; a changed deposit is a new integer Zenodo version | step 1 | Greg |
| 4 | the release documents to v11 and the mirror: `KNOWN_ISSUES.md` (add 0533, the mirrored CTs tokens 75 and 480, COLONOG_299's misplaced L5; F.19), `REPRODUCE.md` section 0 (still "v10 ... S1 = 29"), `README.md` (v5), `STATUS.md`, `ROADMAP.md` (MLHC "in review" is stale), `zenodo/README.md`; HF `OpenSpineConsortium/CTSpinoPelvic1K` to v11 under one licence or the mirror sentence deleted (OQ A20); check Zenodo v11 resolves (OQ E7) | no document names v10, id 29 or MLHC-in-review as current; HF `main` = v11 labels byte for byte against `SHA256SUMS.txt`, or the sentence gone | nothing | Greg (A20) |
| 5 | repository hygiene: gitignore or move the personal and administrative files at the `ctsp:` root (OQ F11); Greg decides on `morphometrics/annotator_names.csv` (student names, tracked, public) and `spine_tampering.csv`; the banned word out of the 29 tracked files (F15); recompute the sacrum-adjacent CSVs on v11 with 05 before any new number (F.44) | `git status` shows no personal file; a grep for the word returns nothing; nothing pushed without Greg; every CSV touching the sacrum carries a v11 commit | 05 step 3 | Greg |

**Dependencies.** 10 (the v11 tree and the cancelled appendix chains run on the grid), 05 (v11 recomputes), 04 (the ostk S1
fallback before any ostk-derived number), 06 (the Castellvi reads and the seven disputed records).

### 04 `04_openspinetoolkit`: OpenSpineToolkit, the v11 defects and their tests

**Goal.** Keep ostk (public, `main` cb43197, 19 modules, 94 test functions; `inventory3_other_spine_folders.md` section 2.1)
correct for release v11 and the student miniprojects: fix the 1b7005c canal-closing regression (VBHp and EPD inflated 10-17 mm
on about one vertebra in seven with no gate; case 0097 T12 VBHp 38.4 vs 28.9 mm; RC G.2), guard or remove `"S1": 29` in
`LABELS_V10` so a by-name call on a v11 volume raises instead of falling back to the whole sacrum (G.3), make PDW survive a
full run (empty in all 4,744 committed rows; G.4; OQ D2), bring `SPEC.md`, `README.md` and `CLAUDE.md` from the legacy v3
scheme and "27 tests" to v11 and 94, fix the one failing test (`tests/test_cobb.py` removes the legacy femur ids 11 and 12;
OQ F18), and re-sync the grid copy with its commit recorded (OQ B29).

**Reader.** Student-safe.

**Why it is high.** Every item has a test with a number: 0097 within 1 mm on VBHp, EPDl and SCD; the share of canal chords
under 11.07 mm at or below 5.2 % (twice the published 2.62 %; the number the fix must move is 15.8 % of reader E's J1
instances); per-level SD inside the widest published living SD (RD CT-1); `pytest` 101 passed. It is ranked fourth because
its first two steps block 05 and RD section 6 lists CT-1 among the week-one items with "depends on: nothing".

**Families absorbed.** toolkit (17 rows): the repository by reference; copied: the defect list (RC Part G,
`HANDOFF/INFRASTRUCTURE.md` section 7, `context/ostk-canal-closing-regression.md` with its fix plan), `np:bibm-spinopelvic/`
(`main.tex` with its honesty contract, `tools/cohort_stats.py`, README; personal e-mail struck; never finished), `np:old/`
(the May 2026 student figure panels; the survey CSV inside excluded), the pre-ostk scripts of 2026-05-17 (`spine_analysis_v316.py`,
`v317.py`, `test*.py`, `vertebral_corners.py`; dated lineage), `ostk:SPEC.md` as the contract; the 9 memory notes of the
toolkit cut list. `ostk:_v.txt` not copied.

**Grid paths it owns.** `HOME/OpenSpineToolkit` (rsync copy, `ostk/` + `pyproject.toml`, 2026-09-23, no `.git`, commit unknown,
carries the regression); `HOME/ostk.tgz` 186,470 B (2026-09-10); the shard outputs shared with 05 (`HOME/ostk_run`,
`ostk_shards`, `ostk_morph_out`, the `logs_ostk*` of the 2026-09-10 run).

**Repositories referenced.** `OpenSpineToolkit` `main` cb43197 (remotes `origin` and `osc`): `ostk/labels.py` (L135 `labels_for`,
L36 `LABELS_V4`, L59 `LABELS_V10`, L64 the `"S1": 29` line), `ostk/vertebral_body.py` L98-132, `ostk/spine.py` L473-474,
`ostk/morphometry.py` (`canal_dimensions` L151, `level_morphometry` L380), `ostk/project2d.py`, `ostk/drr.py`, `ostk/surgery.py`,
`tests/`, `projects/` (14 student READMEs), `tools/export_demo_case.py`.

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | CT-1: per-section hole area at least 18 mm², wall taken only from sections whose hole reaches the canal's median area, raised `min_vox`; run on 0097 and twenty records; render ten body cuts | 0097 within 1 mm of `ostk_level_morphometry.csv` at commit 90a27a7 on VBHp, EPDl, SCD; under-11.07 mm share at or below 5.2 %; per-level SD inside the published band; "the numbers moved toward the mean" is not a pass | 03 (v11 labels) | engineering |
| 2 | the S1 fallback: `endplate_from_label(..., "S1", ...)` on a v11 volume raises or sets a QC flag; port the extraction script's lowest-lumbar footprint isolation (G.3; OQ F8) | `python -m ostk all` on v11 labels never silently runs the whole-sacrum branch; a test on a v11 volume | nothing | engineering |
| 3 | PDW: find why the column is empty (G.4; OQ D2) and fix | PDW present on at least 95 % of level instances; L5 tracks the published 16.20 mm rather than 20.70 | step 1 | engineering |
| 4 | documents and tests: SPEC / README / CLAUDE to v11 and 94 tests, `labels_for` and the retired 29 named; `test_cobb` fixed; the login-node lines checked (OQ F10) | `pytest` 101 passed | steps 1-3 | engineering; Greg commits |
| 5 | rsync to the grid and write the commit beside it | `HOME/OpenSpineToolkit/COMMIT.txt` names the commit; a hash of `ostk/vertebral_body.py` on the grid equals the laptop's; OQ B29 closed | step 4 | engineering |

**Dependencies.** 03 (v11 labels for the tests). Blocks 05; feeds 07 (`ostk.project2d`, `ostk.drr`) and 12 (the demo exporter).

### 05 `05_ct_morphometry_parity`: CT morphometry, the spinopelvic estimator and 3-D to 2-D parity

**Goal.** Make the measurements of CTSpinoPelvic1K right and extend them: the spinopelvic estimator's three open items (eight
prosthetic femoral heads, the 10-15 degree PI shift with the S1 choice on LSTV, the unmeasured anterior pelvic plane;
`ctsp:docs/SPINOPELVIC_ESTIMATOR.md` "Still open"), the level atlas with L5 end-plate width and L5 pedicle width withheld
(`LEVEL_MORPHOMETRY.md`; RC F.34), the sacrum-adjacent CSVs recomputed on v11 (F.44), and the parity programme PAR-1 to PAR-6
(RD section 3): which 3-D features that name a vertebra survive projection, in which view, measured on the programme's own
renders first and on real frames second.

**Reader.** Student-safe.

**Why it is likely to work.** A number comes back within days with no reads, no network and no decision: PAR-1 is the
ratio-only variant of `ctsp:scripts/test_morphometric_separability.py`, one hour on the laptop, on 1,486 T12 and L1 vertebrae
where the within-patient AUC is already 0.990 (F.28) and the bootstrap interval at that n is about +/- 0.006 (RD section
3.8), with a pre-stated three-tier gate; RD section 6 ranks PAR-1 and PAR-2 first and second. Limits: the parity comparison
proper has a minimum detectable deficit of about 8 points on the 73 CTSP persons in G3 validation and waits on 02's clean
encoder; the L6 question has 13 ostk positives and separates "no signal" from "some signal" only; the lumbosacral 3-D target
is undefined without the count (RD section 3.1).

**Families absorbed.** ct_morphometry_parity (33 rows): `ctsp:docs/SPINOPELVIC_ESTIMATOR.md`, `LEVEL_MORPHOMETRY.md`,
`OSTK_VS_EXTRACTION.md`, `BODY_HEIGHT_INVESTIGATION.md` (also in 03), `ctsp:morphometrics/` every tracked csv, json, py and
the `tp_height_renders/` (minus `annotator_names.csv`; the `.bak`, `.pre0631` and `.v10.csv.bak` generations by reference),
the measure-definition diagrams of `ctsp:scratchpad/m4..m9/` and `measures*/`, `sn:results/reader_e/` (code map, cases,
timings, `diag/` renders; `features_j1.csv.gz` copied, the 40 MB csv by path), `np:hu_per_vertebra.csv` (3,913 rows, v3-era
labels, said so) and its xlsx, `Desktop/LDI/` (`automated_lordosis.py`, `dataset_interface.py`, `run_hf_sample.py`, README; a
second, independent lordosis implementation, the outside check `ctsp:CLAUDE.md` asks for; the only copy),
`Desktop/Spine Morphometrics_ Beyond Basic Measurements.pdf` (a literature map with no author; every number to be checked
against the primary paper); the 4 memory notes of the cut list (`panjabi-1991-page-892` notes that the PDF scan is referenced
by path, never copied). By reference: `Desktop/morphometrics/transition_morphometrics.csv` (2026-08-17; md5 matches no repo
copy), `openspineconsortium.github.io/atlas/level_atlas.csv` (48 rows), `ssn:tools/pelvis_landmarks.py`, `plan_postop.py`.

**Grid paths it owns** (`grid_manifest.md` section 3.5): `$RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/
{ostk_level_morphometry.csv 302,994 B, pi_ostk2.csv, pdw_why.py, pitest, pdwtest}` B14 VERIFIED; `HOME/spinopelvic_all.csv`
63,562 B and the probe scripts at the HOME root (`agg_spinopelvic.py`, `show_pi.py`, `ss_probe.py`, `disc_probe*.py`,
`height_probe.py`, `cmp_pdw.py`, `lm_probe.py`; in no repository as far as recorded); `HOME/height_renders`;
`HOME/CTSpinoPelvic1K/morphometrics` (recomputed on v11? OQ B27); `$RS/data/versefusion/derived/vf_v10`.

**Repositories referenced.** `CTSpinoPelvic1K` 7ddfe38 (`scripts/test_morphometric_separability.py`, `six_lumbar_readings.py`,
`shift_hypothesis_test.py`, `extract_surgical_morphometrics.py` (its report prints 643 ordinary records while the docstring
says 644), `extract_*.py`, `height_probe.py`, `render_height.py`, `compare_v10_v11_spinopelvic.py`, `audit_s1_carve.py`);
`OpenSpineToolkit` cb43197; `spinesurg-ct-nnunet` 097933a.

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | PAR-1 on the laptop: drop the five case-median features, keep the six ratios; T12 against L1 on `level_gradients.csv`, grouped five-fold, seed 0; the seven-level model on the 643 ordinary records applied to the 18 six-lumbar spines; L6 against L5 on the 13 ostk rows (0033 removed) leave-one-case-out with a 1,000-permutation p | AUC at or above 0.95: a single-vertebra target exists; 0.90-0.95: one body plus a neighbour; below 0.90: a window of three or more; outside check: every ratio's weight sign against Panjabi 1991 Table 3 and the dominant weight on the transverse-process span | nothing | engineering |
| 2 | CT-2 after 04 step 1: recompute SS, PI, PT means from the v11 columns beside Veilleux (gap 0.1, not the stale 3.4 of SPE section 5); fit ASIS and pubic tubercles from the hip labels, APP, APPA, aSS, aPT; render ten fits first; report the 8 prosthetic records | APPA median inside the published supine band +5.1 to +12.2 degrees, or the extraction is wrong; then a two-reader manual read of PI, SS, PT on 50 records (MAE, ICC, Bland-Altman) | 04 step 1 | engineering |
| 3 | recompute `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv` (and `opportunistic.csv`, `proximal_femur.csv`) on v11 with `labels_for` (F.44), zero-padded ids, PIR axes checked, never reoriented on write; `n_voxels_fg` (0 in 340 of 802, F.16) fixed or dropped | no column reads identifier 29; the spread test: per-level SD inside the widest published living-cohort SD; share below a floor against published prevalence; twenty retained masks rendered before any number is believed | 04 step 2 | engineering |
| 4 | PAR-2 smoke: fifty records, lateral and AP, T12 to L4, two hours on `reqp --qos=requeue`, outputs under `$RS`; submit, estimate wall time, write job ids and ETA to the resume file; then all 802 and the arc | per-feature ICC tiers 0.75 / 0.50 with case-clustered lower bound above 0.60; junction AUC tiers 0.970 / 0.90 per view; twenty records per view rendered with every chord drawn | step 1; 10 (the v11 tree on Ceph) | engineering |
| 5 | CT-5 and the withheld L5 columns: end-plate width at L1, L4, L5 from the SPINEPS corpus label on the same 741 / 773 / 764 records, scored with the three columns `LEVEL_MORPHOMETRY.md` uses | no rule ships unless it beats the shipped rule on all three columns; if the corpus label's L5 SD stays above 5.54 the shoulders were not the whole story | 04 step 1; 10 (`spineps_ids.py`) | engineering |

Then PAR-3 (Farshad 2013 on lateral renders of the 21 graded III / IV records), PAR-4 (pose quality against naming on
C-ArmLSpine, with 01), PAR-5, PAR-6 (each after Greg's decision), CT-4, CT-7; the PDW cause recorded, not guessed.

**Dependencies.** 04 (CT-1 fix and the S1 fallback), 03 (v11 labels), 10 (the v11 tree on Ceph; the SPINEPS stores through
`spineps_ids.py`), 02 (FLU-2's encoder for the 2-D side of parity), 08 (exact-pose renders for PAR-2), 06 (CT-3 re-reads can
move a record).

### 06 `06_transitional_ct_census`: the transitional census, harvest, registry, ruleclass arms and the review tree

**Goal.** Find enough transitional people across every public CT to test naming (`context/anomaly-harvest-directive.md`, Greg
2026-09-23: screen every CT, two labellers, both junctions in field): the acquisition over 18 collections (18,873 listed,
16,898 on disk, 12,123 passing the field gate; `ssn:docs/CENSUS_TABLE_2026-09-25.md`, off by one in every collection but
PANORAMA, RC D.13), the one registry (6,131 rows -> 6,108 persons; L6 146, T13 14; `sn:results/transitional_registry/REGISTRY.md`;
D.8), the ruleclass run over 21,622 CTs (two arms plus the pelvis arm; `ssn:docs/ruleclass/TIERS.md`), the four pre-registered
rules (DRAFT v1, unsigned; D.23), the two-stage review tree (`ssn:tools/transitional_review/`, untracked, never run), and the
human verdicts that turn a call into truth; plus the VerSeFusion, CTSpine1K, CTSpinoPelvic1K-Syn and MRI (lstv-detector)
lines that feed it.

**Reader.** Student-safe after redaction (usernames in review material and some notes; case134's real PatientID is in 01's
domain and never printed).

**Why it is medium.** The machine side is nearly done: arm A tier 1 5,094 CTs complete but one, tier 2 848 of 12,217 pending at
about 19.7 GPU-hours (`$RS/ruleclass/arms/ts/STATUS.md`, 2026-09-29, read in the grid pass); the pelvis arm's `DECISION.json`
was written from zero timing CTs and the production array never ran (`arms/pelvis/_timing/DECISION.json`, `tier2_go false`,
`n_timing 0`). The result that matters needs readers: `greg_verdict` filled on 0 of 546 rendered review cases (D.9); the
whole-cohort Castellvi read is 40 to 67 reader-hours per stage (RD CT-3); labeller PPV for L6 is 10 of 24 and for T13 0 of 52
(A16.8); the NLST T13 9.3 % was wrong but plausible and fell to 1.5 % once a rib on the body was required (D.12). The gated
collections that would change the count (Stanford Merlin, about 447 L6 people expected, D.13) have no agreement.

**Families absorbed.** anomaly_scan_census (99 rows; 91 after merges and moves): `sn:results/transitional_registry/` md, csv,
json (contact sheets by path), `ssn:docs/ruleclass/` (`CLASSIFIERS.md` 282 KB R1-R33, `STUMP_RULE.md`, `MORPH_API.md`,
`ARM_B_pelvis.md`, `TIERS.md`, `PREREG_rules.md`), `CT_LSTV_CLASSIFIER_PLAN.md` (74 KB, design only),
`CENSUS_TABLE_2026-09-25.md` (flagged), `REVIEW_TRANSITIONAL.md`, `ANOMALY_RULE_EVALUATION.*` (R + C = 22 refuted),
`ssn:tools/CT_MINE_REPORT.md`, `sn:lit/ct_lstv_classifier/`, `ssn:disputed_renders/` (7 PNG), `ctsp:docker/Dockerfile.spineps` +
`fetch_spineps_weights.py`; `code/`: `tools/transitional_review/` (10 files, after the banned word is removed from
`anomaly_rules.py` and `build_review_tree.py`); the VerSeFusion line: `np:README.md` (2026-05-14 dataset card, banned word
rewritten) and `np:Makefile`, `np:VerSeFusion_grid_derived/` tables, cards and corrected renders (about 12 MB; `manifest.csv`
374 rows with `has_T13 = 18` WRONG, truth 6, written beside every copy; the 374 QC PNGs by path), `np:renders/`,
`np:VerSeFusion/verse_datasets_age_sex_19.xlsx`, `Desktop/NeurIPS/Lumbosac_Castelvii_Class.csv` (stale IIIb 19, said so) and
`verse_veridah_labelcorrection.csv/.xlsx`; `Desktop/CTSpinoPelvic1K-Syn/` whole (local git 7098eb1, no remote; the only copy;
README banned word rewritten); the AACA 2026 MRI line from `nsurg/AACA/`: `citations/3d/lstv_cohort_summary.csv` (n 282),
`lstv_per_study.csv`, `lstv_alignment.csv`, `lstv_l6_subgroup.csv`, `raj/results/*.json`, `docs/` (README, three docx guides),
`LSTV Vertebrae Labeling Manual.pdf`, `Submission Summary.pdf`, the collaborator draft renamed; the 12 memory notes of the cut
list (`lstv-data-landscape` from the redacted copy). By path: `Desktop/STUMP_RIBS.pdf`, `np:viz/*_lstv_3d.html`, the DICOM,
images, `.pth` and the Firebase key under `nsurg/AACA` (the key is excluded and must be revoked).

**Grid paths it owns** (`grid_manifest.md` section 3.3): `$RS/ruleclass` 48.579 GB (163,587 files; `CORPUS.md` says 21,655 CTs
against the tiers' 21,622, unexplained, OQ B3); `$RS/data/anomaly_harvest` 325.817 GB (PANORAMA `calls/`, `rows.csv`,
`registry_rows.csv` on disk, counts unread, OQ B2); the 19 family-B collections `$RS/data/{idc 706.083, abdomenatlas3_mini 570.557,
tcia_fdg_pet_ct_lesions 393.872, panorama 194.439, ctspine1k 162.350, amos22 102.615, pengwin2026 83.499, ribfrac 78.200,
kidney_thoraxabdomen 75.938, nlst_pilot 73.544, waw_tace 47.151, curvas 29.994, deep_psma 24.253, quadra_hc 20.413, barts_crl
20.313, curvas_pdacvi 16.879, aortaseg60 15.929, ctpelvic1k_clinic 14.832, csi2014 6.641}` GB; `$RS/data/spineps` 8.834 GB;
`validation_ts`; `HOME/bench_ts` 1.511 GB; `HOME/model_night/anomaly_manifest`; `$RS/data/versefusion` raw 194,191,642,435 B and
derived, B06 VERIFIED; `HOME/VerSeFusion` (`data` symlinked to Ceph 2026-10-08); `HOME/lstv-detector` ABSENT; `$RS/review_tree`
does not exist.

**Repositories referenced.** `spinesurg-ct-nnunet` 097933a (`acquisition_*.py`, `harvest_*.py`, `transitional_*`, `ts_*`,
`other_ct_*`, `ctsp_registry_*`, `versefusion_*`, `anomaly_*` (`anomaly_manifest.py` defaults to a deleted bank, OQ F22),
`census_table_2026-09-25.py`, the slurm of row 151); `Gregory-Schwing-MD-PhD/VerSeFusion` 2b21cc4 (`configs/veridah_corrections.csv`
25 rows); `Gregory-Schwing-MD-PhD/lstv-detector` `no_angles` 84636d6 (no ground truth; estimated accuracies 65-90 % by its own
README); `Gregory-Schwing-MD-PhD/spine-level-ai` 5043793; `lstv-annotation-tool`.

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | a read-only job answers OQ B1-B5: `arms/moller_fast/JOBS_ACCEL.txt`, `_claims_*`, `arms/pelvis/<collection>`, PANORAMA's `rows.csv` and `registry_rows.csv` counts, the 33-CT discrepancy, the one-high census counts | the counts written into `STATUS.md` with the job id; the census table corrected before anything copies it again (OQ F13) | nothing | engineering |
| 2 | commit `tools/transitional_review/` after its self-tests, banned word removed (OQ F12, C21); Greg signs `PREREG_rules.md` section 9 (A16) | sha256 in the freeze block; before it, every rule number is calibration | nothing | Greg |
| 3 | finish arm A tier 2 (848 CTs, `ts_arm_gpu.sh`) and the Moller full configuration; run the pelvis arm's 20-CT timing task, then decide tier 2 | `arms/ts/STATUS.md` remaining 0; `DECISION.json` rewritten from at least 20 timing CTs with a Dice | 10 (B07 for the TS trees) | engineering |
| 4 | open the review queues (verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87) in the two-stage tree, paired-radiograph cases first; the 63 field-supported volumes of 02 first of all; truth tier recorded per person | `greg_verdict` filled; a segmenter call is never promoted without a read; yield in two columns (confirmed on CT; with a frame); per-collection call rate against the prevalence windows (L6 prior 3.2 %, T13 0.6-2.0 %, Castellvi II-IV 9-18 %) | step 2; readers | Greg adjudicates |
| 5 | CT-3: one script counts ids 25 and 28 per raw VerSe mask against the Loeffler table (under an hour; never `vf_813`); a third reader blind to the first two on 0008, 0021, 0033, 0049, 0176, 0179, 0196, 0172, 0068; then two readers grade all 802 with a senior adjudicator | II-IV rate inside 9-18 % and type I near 68 % of calls; second-reader kappa at or above 0.63; if a record moves, the G3 split is re-split and the leak audit re-run before 02 scores anyone | readers | Greg |

**Dependencies.** 10 (the collections on Ceph; `spineps_ids.py`; B06, B07), 03 (the seven disputed CTSP records), readers
(Ashley Schehr stage 1; "Dr Tech" stage 2; Greg adjudicates); 02 consumes its output.

### 07 `07_plain_film_level_id`: plain-film level identification and the radiograph corner detector

**Goal.** Level identification and corner detection on plain radiographs, the line the C-arm work grew out of: the
spine-detector corpus and detectors (detect_v1 report on the laptop: AP50 0.957 on 558 instances; detect_v2 on the grid AP50
0.970, PCK@0.1 0.812; `Desktop/spine-detector/report/metrics.json`; `context/xray-corner-detector-status.md`), XRSpinoPelvic1K
(DRRs of CTSpinoPelvic1K with four end-plate corners fitted in 3-D and projected; a YOLO-pose corner detector trained on
BUU-LSPINE), the held-out film N-curve (RC A10), the student film-review Space, the amendment-47 route to DMC trauma
radiographs, and the retirement of every leaked early film number.

**Reader.** Greg-only (level-identification code; the private repository; the amendment drafts).

**Why it is medium.** The quotable numbers are held out and complete: corner localisation 92.4 % within 0.55 % of the diagonal
on 301 held-out BUU films against 75.6-76.8 % for the published models; SS ICC(2,1) 0.952, MAE 2.01 degrees; LL MAE 3.75
degrees; corner-identity macro-F1 0.999-1.000 (`xrsp:docs/RESULTS.md`); film naming against persons NHANES 27.2 -> 92.7 %,
BUU 10.3 -> 96.9 %, CSXA 3.2 -> 99.8 % at N = 0 to all (A10.1-A10.3, HELD OUT); the render ablation at N = 5 +21.9 / +11.1 /
+18.7 points (A10.6). Against it: the BIBM window (5 July) and the SPIE MI abstract (5 August) passed with no submission
recorded (`MANUSCRIPTS.md` section 10; OQ A8); `xrsp:data/ct` and `data/labels` dangle on a deleted export built from 822
pre-release cases (`DATA_MANIFEST.md` defect 36); the BUU licence is undecided; the 97.47 / 99.02 / 98.7-99.4 % film numbers
are LEAKED or wrong-bank (RC C1.2; OQ F5); the route to hospital films is an IRB amendment, not a determination.

**Families absorbed.** plain_film_level_id (69 rows; 67 after merges and moves): `Desktop/spine-detector/report/` into
`results/spine_detector_report/` (text files and the 50 renders; the local `src/` snapshot lands in 01 for the runtime);
`ctsp:scratchpad/results_unified/` (33 BUU-vs-DRR agreement, Bland-Altman and CED figures), `scratchpad/yolo/`, `failures/`,
`per_landmark_buu.csv`, `pl_v8l640.csv`, `pl_v8l1024.csv`; `ssn:track5_results/` (RECORD ONLY [WRONG-BANK]),
`lumbar_diag_2026-09-16/` (RECORD ONLY), `review_space/`; `xrsp:journal.pone.0347290.pdf` (CC-BY baseline); `regulatory/`: the
amendment-47 drafts from `CTSP1K_private/proposals_backup_20260911/` (`IRB-21-10-4123_Amendment_Draft.docx`,
`irb_amendment_draft.md`, `XR_Fracture_Detector_Proposal.docx`, `xr_fracture_detector.md`); `code/`: `eval_shortcut_controls.py`
(the negative controls), `context_ladder.py`; the 14 memory notes of the cut list with LEAKED and RECORD ONLY marked
(`xray-corner-detector-status` redacted by hand). By path: `ctsp:BUU-LSPINE_400/`, `BUULSPINE_3600/` (9.96 GB),
`AASCE19/Archive.zip`, `CSPINE_ARCHIVE/`, `LATERAL_ATLAS/` (its `key.txt` is an AWS credential: exclude and rotate),
`xrsp:dataset2024.zip` (4.0 GB, identity not recorded), `Desktop/TEST_XR.png` (origin unknown).

**Grid paths it owns** (`grid_manifest.md` section 3.6): `HOME/spine-detector` 382 GB (B04 copying; `data/raw/{aasce, buu_full,
buu_v1, cm_spine, csxa, lateral_236, mendeley_716, nhanes_annotated, nhanes_full, spinal_ai2024, vindr}`; `runs/`; `yolo11m-pose.pt`);
`HOME/XRSpinoPelvic1K` 22.428 GB (B05 after B04; the Cerner `.ica` and `.crdownload` in the checkout root); `HOME/films_drr` 36 GB,
`films_all2_fov96_ctx` 26.278 GB, `films_ann_fov96_ctx` 13.861 GB, `allspine_v6/v7/v7nofluoro/v8_fov96_ctx`, `buu_fov96_ctx` 9.981 GB,
`buu_yolo`, `nhanes_*`, `vindr_*`, `mendeley_fov96_ctx`, `aasce_fov96_ctx`, the packs (`quiz_pack`, `reader_study`, `review_pack*`,
`verify_bench`) (B10 / B11 not started; most superseded by v9); `$RS/data/inventory/films` (`nhanes_film_manifest.csv` 2,109,890 B,
`vindr_film_manifest.csv`); `$RS/data/thoracic_xr` 0.859 GB; registry aliases `films_all2_rung*`, `recurrent_head_films_all2_r1`
(wrong-bank), `detector_v5z_*`, `detector_v6f`; `allspine_v2..v5c` deleted 2026-09-20.

**Repositories referenced.** `XRSpinoPelvic1K` `main` 4f22935 (copy `docs/RESULTS.md`, `ROADMAP.md`, `PIPELINE.md`, `HPC.md`
with `OSTK_REF` 09dd9c5, `reader_study_protocol.md`, `dataset_card.md`, `annot/README.md`; the tracked `.ica` and `.crdownload`
flagged for a history purge); `OpenSpineConsortium/spine-detector` (private; `train.py` with `fliplr=0.0` explained;
`manifest.py::canonical_slots`); `spinesurg-ct-nnunet` 097933a (the tools of rows 141-142 and slurm of row 154 of
`spinesurg_ct_nnunet.tsv`; `logs/xray_gate/`); `OpenSpineToolkit` cb43197 (`ostk.project2d`, `ostk.drr`).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | purge the tracked `.ica` and `.crdownload` from XRSpinoPelvic1K history and the grid clone; after B04 and B05 land, rebuild `data/ct` and `data/labels` from the v11 tree with `labels_for` | `git ls-files` clean; five DRRs rendered with projected corners overlaid and looked at; the S1 plate fitted in 3-D and projected (within 0.6 degrees), never from the 2-D silhouette | 10 (B04, B05); 03 | Greg (history rewrite) |
| 2 | correct the wrong-bank attribution (`ssn:slurm/recurrent_head.sh` L16, `tools/recurrent_order.py` L56: films_ann, not films_all2; OQ F5) and mark every leaked number in the folder's documents | no document quotes 97.47, 99.02 or 98.7-99.4 % as held out; the held-out film number is the N-curve | nothing | engineering |
| 3 | Greg's BUU licence reading (3,603 BUU laterals sit in v9) and the VinDr determination number (OQ A5) or a written exclusion; `vindrps` (77.8 % validation leak) never re-enters a bank | written decisions before any weight trained with BUU leaves the grid; the number recorded or VinDr out | nothing | Greg |
| 4 | regulatory: amendment 47 on IRB-21-10-4123 with that protocol's PI as the students' route to DMC trauma radiographs | the amendment approved and its scope sentence written into `README.md` | Greg with the PI | Greg |
| 5 | choose the paper (XRSpinoPelvic1K corner detection and film spinopelvic measurement, SPIE MI 2027 or J Imaging Informatics in Medicine) from `RESULTS.md` recomputed on the v11 rebuild; close OQ C2 (score the ImageNet-init G3 arm on G3 test films) and decide A9 (seeds 1-2 above N = 25; the ratio sweep) | every number regenerated from a result file through a manifest key; every held-out claim through `eval_gate.py`; the two-click femoral-head annotation protocol stated; the BUU-all reversal confirmed or refuted on three seeds | steps 1-3 | Greg (venue, A9) |

**Dependencies.** 10 (B04, B05), 03 (v11), 01 (the shared encoder lineage and the body detector), 04 (`ostk.project2d`, `ostk.drr`).

### 08 `08_render_devices`: image formation, DRR banks, device cards, PolyPose and synthetic-to-real

**Goal.** The rendering side that feeds every 2-D model: the DRR banks from CTSpinoPelvic1K, VerSe and TotalSegmentator
(`physics_drr` 7,045 renders; `physics_rare` 1,482 renders of 81 transitional subjects, the only labelled L6 and T13 at scale;
`DATASET_USAGE.md` section 3.1), the nine-term device cards (Cios Fusion, Elekta XVI, BV Pulsera, PIXIUM 4600 on disk;
Surgio-B51 and Varian Halcyon on the grid), the DeepFluoro calibration (physics 80.9 %, nine device terms +4.3 held out;
`context/learned-formation-refuted-calibrate-instead.md`), the styled device corpus with its pooled and LODO designs,
PolyPose morphology augmentation within published ranges of motion, and the record of the refuted translation routes.

**Reader.** Greg-only until Greg confirms (the sweep and physics documents describe invention aspects; the banks derive from
NC-licensed data; the redacted formation note names a DMC clinician: keep it struck).

**Why it is low as a claim and medium as support.** The styled corpus met its pre-stated 97 % detection criterion on none of
three held-out devices (Cios 91.6-94.0 %, Elekta 30-33 %, Surgio 14-15 %; `ssn:docs/MODEL_CARD.md` section 4.6; RC A6.13);
device-level claims cannot be tested with four devices (smallest two-sided P 0.125; E.11); the card clip saturates
(`context/device-sampling-audit.md`; A12.6) and is still the default; the synthetic:real ratio was never swept (A10.11; OQ A9,
C5); CycleGAN, CUT, ADDA and SDXL gave no gain in any arm (RD section 2.2). As support it is indispensable: renders raise
scarce-N film naming by 6 to 22 points (A10.6-A10.10), they are the only route by which TotalSegmentator reaches the level
bank, the arc of oblique poses is the only route to angles no real set covers, and PolyPose's DeepFluoro reproduction is
REPRODUCED (Dice pelvis 0.992; `sn:results/polypose/REPRODUCTION.md`) though its `VALIDATION.{json,md}` does not exist (G.6).

**Families absorbed.** render_devices (71 rows): `ssn:docs/devices/` (the four fitted cards, `.frames.csv`, the header-census
format), `DEVICE_PARAM_AUDIT.md`, `DEVICE_SPREAD_SWEEP.md`, `DEEPFLUORO_FORMATION.md`, `MORPHOLOGY_SYNTHESIS_PRIOR_ART.md`,
`SIMULATION_FIDELITY.md`, `fig_device_params.png`, `fig_device_spread.png`, `path_census.json`,
`polypose_reference_envelope.json`, `polypose_segmental_rom.csv`; `sn:results/manifold/` md, csv, json (`deep.npy` 124 MB by
path), `sn:results/polypose/` (REPRODUCTION, SAMPLING_SPEC, cohort files, `rom_cine.json` untracked), `results/corpus_manifold/`;
`ssn:research_notes/` (14 verified literature notes), `ssn:reports/Synthetic real ratio X-ray detectors.md`; `code/`:
`device_fit.py`, `device_style.py`, `device_spread_sweep.py`, `deepfluoro_calibrate.py`, `make_drr_dataset.py` (`--paths2-only`),
`render_physics_drr.py`, `polypose/polypose_sample.py`, `polypose_warp.py`, `spine_project.py`; the 19 memory notes of the cut
list. By path: `ctsp:infobot/` (288 MB of 2019 DR + bone-DRR pairs; origin not recorded), `ctsp:2D-3D-GS.zip`, `PIG/*.zip`,
`ssn:recept_out.json` (purpose not recorded), `Desktop/Panjabi_1976_JBJS_thoracic.pdf`.

**Grid paths it owns** (`grid_manifest.md` section 3.2): `HOME/physics_drr`, `physics_rare`, `physics_drr_film`,
`physics_rare_film`, `physics_smoke` (B10 / B11; 7,045 vs 7,048 renders, OQ B12); `HOME/ctsp_drr` 0.686 GB, `anchor_drr` 0.713 GB
(its own split leaks 301 of 801 people), `ts_drr` (not held out from v9), `ts_drr_v3` (read by nothing), `implant_ts`
(unfinished, 355 subjects), `cut_*`, `fluorogen`, the pseudo-label banks; `$RS/data/versefusion/derived/{implant_verse 159.4 GB,
verse_drr, verse_drr_film, verse_drr_obl(2), verse_soft_drr (row-spacing defect on 181 of 374), ctsp_drr_obl(2), obl2_fov96_ctx
13.3 GB, vf_813 49.4 GB, vf_v10}` B06 VERIFIED; `$RS/data/polypose` 87.713 GB; `$RS/data/or_ready/devices`, `devices_refit`,
`devices_refit_constrained`, `devices_refit_v2` (whether the DeepFluoro cards were refitted under `DF_CONVERSION=linear`, OQ B9,
can now be read there); `$RS/data/devcorpus` 18.280 GB + `devcorpus_arc`; `HOME/spine-detector/runs/devcorpus` (21 arms, no
registry alias); `HOME/data/TotalSegmentator` (the 2.0.1 release, 82.0 GB) and `_v3` (89.8 GB), B07 copying; `$RS/model_night`
anchor rounds 0.831 GB; `deepfluoro_h5`, `deepfluoro_vendor`, `geneva_hip_src`, `ljubljana`, `spinesac` (shared with 01).

**Repositories referenced.** `spinesurg-ct-nnunet` 097933a (`device_*.py` (8), `deepfluoro_*.py` (23), `devcorpus_*.py`,
`ts_to_drr.py`, `drr_register.py`, `reg_*`, `strong_dr.py`, `film_style_dataset.py`, `fluorogen_*`, `drr2fluoro_cut.py`,
`spinesac_*` (9), `cobra_*` (6), `corpus_manifold.py`, `tools/polypose/` (16; generator commit 1f4418f never pushed) and
`polypose_*.py` (12); the slurm of row 150).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | read `or_ready/devices_refit*` and `~/spine-detector/runs/devcorpus/*/scores.json` in a job to answer OQ B9 and B10 (the box convention; the missing `dc_B_held_cios_fusion_s1` row) | MODEL_CARD section 4.6 reconciled with `scores.json`; the convention named; both written into `STATUS.md` | nothing | engineering |
| 2 | write PolyPose `VALIDATION.{json,md}` through `slurm/polypose_validate_submit.sh`; record whether any training bank used PolyPose; push generator commit 1f4418f (OQ C18) | the file exists with the Dice and range-of-motion checks; fused junctions zero motion confirmed | nothing | engineering; Greg pushes |
| 3 | the primary C7 criterion: paired bootstrap of the styled-corpus arms against the LODO baseline (OQ C14) and the exposure-clip A/B on real frames (C17, `slurm/device_spread_arm.sh`) | a CI excluding zero before any "improves"; otherwise the sentence "not met" with the number; the default clip changes only if the CI excludes zero | 10 (B10 / B11 for the banks) | engineering |
| 4 | correct Table 1's TotalSegmentator rows and the 4,093-render footnote from the v9 build roots; the DATASHEET and MODEL_CARD device-corpus lines (OQ F6) | `ts_drr` and `ts_drr_v3` counted out; `physics_drr` and `physics_rare` counted in | step 1 | engineering |
| 5 | the 45-cell synthetic:real ratio array (real share 0.1-0.9, N 25 and all, three seeds, L6 scored separately) only after 02's clean encoder exists and Greg says yes (OQ A9) | a cell that raises held-out L6 recall without lowering ordinary film by more than the seed spread (1.0 point at full size); the plateau reported as a curve, never one ratio | 02 step 5 | Greg |

**Dependencies.** 10 (B06, B07, B10, B11), 03 (v11 labels for exact-pose renders), 02 (the clean encoder), 01 (the consumer).

### 09 `09_wrong_level_clinical_qi`: wrong-level surgery, the iliac-crest paper, the scoping review and the QI protocol

**Goal.** The clinical argument and its three instruments: the iliac-crest clinical paper (`ctsp:paper/clinical/main.tex`,
Spine Surgery and Related Research, "complete draft with real numbers", first author unassigned), the wrong-level-surgery
scoping review (`ctsp:proposals/review/`: protocol v1.0, manuscript v0.4 of 2026-09-15, PRISMA-ScR checklist; "no number has yet
passed human charting"), the four verified evidence briefs, and the quality-improvement protocol manuscript "The Universal
Protocol with a level in it" (The Joint Commission Journal on Quality and Patient Safety, SQUIRE 2.0, 9 pages, built
2026-09-22, never submitted) whose per-case form is the process measure the hospital test needs.

**Reader.** Greg-only for the QI manuscript (it describes invention aspects: the sweep and the persistent digital fiducial;
private until the provisional is filed, `MANUSCRIPTS.md` section 5); the review and the clinical paper may be split into a
student-safe folder once Greg names the first author.

**Why it is medium-low near term.** The iliac-crest number (24.7 %, 195 of 789; RC F.41) is v5-era and touches the pelvis, so it
is SUPERSEDED-PENDING until recomputed on v11; the review needs human charting by two readers; the QI protocol cannot run
before 01 reaches S8, its affiliation line reads Neurosurgery, two sentences ("17 ms per frame", "about fifteen minutes")
have no file, and its primary outcome is powered to estimate only (E.10). It pays off through 01: the per-case form (anchor,
exposures, minutes, dose, needles, disagreement, confidence, level reached, transitional anatomy) is the S5 / S8 scaffold.
`MANUSCRIPTS.md` section 21 item 8 says each of these starts only with Greg's go-ahead.

**Families absorbed.** qi_wrong_level (9 rows): `ssn:paper/qi_universal_protocol/{main.tex, main.pdf, build.sh}` with a copy of
its bibliography `ssn:paper/rsnai/refs.bib` beside it (both paths recorded); `ssn:docs/WRONG_LEVEL_COST_EVIDENCE.md`,
`WRONG_SITE_BURDEN_EVIDENCE.md` (three refutation votes per claim); `ctsp:proposals/review/`; `ctsp:paper/clinical/main.tex` +
`iliac_crest_landmark.pdf`; `code/`: `review_prisma.py`, `review_stats.py`, `prior_art_wrong_level.py`; `MANUSCRIPTS.md`
sections 5 and 11, `LITERATURE_STATE.md` section 6, `literature_state/topic1_bibliography.md` as extracts;
`ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` (human naming 69.6 % unassisted, 97.6 % with LevelCheck) cross-referenced from
01; the memory note `registration-free-prior-art` plus the 22 `all`. `main - Copy.pdf` not copied.

**Grid paths it owns.** None of its own; the iliac-crest recompute runs under 05.

**Repositories referenced.** `spinesurg-ct-nnunet` 097933a (`review_*.py` (9), `prior_art_weak.py`, `prior_art_wrong_level.py`,
`fluorocap_wrong_level_report.py`); `CTSpinoPelvic1K` 7ddfe38 (the iliac-crest extraction scripts).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | recompute the iliac-crest statistic (crest height against L4-5) on v11 with `labels_for` (F.41); compare its spread, not its median, against the published iliac-crest level distributions | the 24.7 % replaced by a v11 number with its file, or the paper withdrawn from the queue; hypothesis tests stated before the run | 05 step 3 | engineering |
| 2 | Greg decides venue and authorship (SSRR as drafted), the first author, and whether the paper waits for CT-3's whole-cohort Castellvi read (33 graded against 71-142 expected, D.18) | a written decision in `STATUS.md` | step 1 | Greg |
| 3 | the scoping review: run `review_prisma.py` on the frozen search; two readers chart the included set; `review_stats.py` regenerates the counts | PRISMA flow numbers printed by the tool; charting kappa reported; no number in the manuscript that did not pass human charting | readers | Greg |
| 4 | the QI manuscript: affiliation to General Surgery; the two unverified sentences struck until a file exists for each (the latency file is 01 S1's output); `ssn:tools/disclosure_audit.py` run; held until Greg confirms the provisional is filed | the audit passes; no sentence without a file; Greg's written go before any submission | 01 S1 | Greg |
| 5 | register the per-case QI form as the reader-protocol scaffold in 01's PREREG draft; the protocol activates only after 01 S8 | the form appears in `01_carm_level_detection/regulatory/PREREG_draft.md` and 01's PREREG cites it | 01 S5 | Greg |

**Dependencies.** 05 (v11 recompute), 01 (deployment and the QI arm), Greg (the provisional, the first author).

### 10 `10_data_platform_grid`: the data platform, 211 sources, the Ceph migration, identity and leakage, grid operations

**Goal.** One record of where every imaging source came from (211 cards, `ssn:data_platform/DATA_MANIFEST.md`), where it sits
(HOME versus `$RS`), its migration and verification state batch by batch, the identity and leakage rules every bank must pass
(`HANDOFF/LEAKAGE.md`, `ssn:docs/PATIENT_IDENTITY_SPEC.md`), the model registry, the environments and the grid operating rules;
finish batches B04 to B11, build the holding index, FINALIZE on Greg's word, and repair the records that contradict each other.

**Reader.** Student-safe after Greg confirms the reader split (OQ A29); credential names only, never values;
`INFRASTRUCTURE.md` section 9 stays out.

**Why it is likely to work.** Mechanical and under way: at 22:20 UTC on 2026-10-08 three `dp_migrate` jobs (40580669, 40580671,
40580673) were running for B04, B07, B09 and a census job 40580052 (`scratchpad/seed/grid_ls_2026-10-08.out`); B00 76 / 76 files
VERIFIED, B02 2,417 / 2,417 files 196.2 GB VERIFIED with 200 sampled, B06 14 / 14 VERIFIED, B08 and B14 VERIFIED
(`plan/runs/<B>/STATUS`). Risks are decisions, not engineering: HOME 4,050.75 GB of a 4,294.97 GB soft limit with no batch
finalized (`pan_quota`); the TCIA CT Colonography raw DICOM (721 GB) and NIfTI (336 GB) are on neither volume with nothing
recording the deletion (B01 rows ABSENT; OQ B30); CTPelvic1K datasets 1-5 absent; 1,590.3 GB of deletion candidates and B13
(627 GB) reserved to Greg (`MIGRATION_PLAN.md` sections 1, 8; OQ A26).

**Families absorbed.** data_platform (158 rows; 157 after merges): `ssn:data_platform/` whole into `code/data_platform/` with
its relative paths intact (DATA_MANIFEST 939 KB, MIGRATION_PLAN, LAYOUT, VERIFICATION, `sources.json/.yaml`, `plan/` incl.
`batch_items/B00-B14.tsv` (no B12; dropped), `dedup/` (DEDUP_PLAN 126 KB, `hash_results/A01-A23`), `db/`, `reacquire/`, `lib/`);
`HANDOFF/LEAKAGE.md`, `INFRASTRUCTURE.md`; `ssn:docs/DATA_ACCOUNTING.md`, `DATA_COMPLETENESS_AUDIT.md` (361 KB, 99 gaps),
`PATIENT_IDENTITY_SPEC.md`, `NHANES_DOUBLE_INCLUSION_2026-09-22.md`, `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`, `CT_INVENTORY.md`,
`XRAY_DATASET_USAGE.md`, `MANIFEST_DATA_MODELS_RESULTS.md`, `MODEL_REGISTRY.md` (the login-node `mlflow ui` instruction corrected
beside it), `grid_records/JOBS_RECORD_2026-09-27_1544.{md,tsv}`, `pipeline.md`, `troubleshooting.md`; `sn:results/spineps_ids/` md
and json; `ssn:spine_data_review/` tracked part (the PRISMA-ScR scoping review of every public spine dataset; `runs/` by path);
`ssn:env/`; `code/`: `spineps_ids*.py` + tests, `data_ledger.py`, `data_alias.py`, `data_lineage.py`, `data_manifest.py`,
`leak_check.py` + `test_leak_check.py` (fails on one stale Geneva fixture, OQ F17), `patient_keys.py` + test, `ct_inventory.py`,
`xray_dataset_usage.py` (`buu_2000` mislabel, OQ F7), `pipeline_state.py`, `diagnostics/make_fake_corpus.py`,
`inspect_dicom_tree.py`, `ctsp0533_*.py`; the read-only grid pass of 2026-10-08 (`grid_ls_2026-10-08.out` 220 KB,
`grid_ls_condensed.txt`, `grid_remote_ls.sh`) and the laptop census copies (`scratchpad/census/*`) into
`docs/grid_read_2026-10-08/`; the 28 memory notes of the cut list plus the grid notes; the home copies of most `all`-tagged
HANDOFF sections.

**Grid paths it owns** (`grid_manifest.md` sections 2, 3.7, 3.9, 4-6): the whole batch table (B00-B14); `$RS/data/inventory/
census_2026-10-07`; `HOME/spinesurg-ct-nnunet/data_platform/plan/runs/*`, `plan/logs/*.out` (24), `dedup/hash_results`;
`HOME/spinesurg-ct-nnunet` at 4e3fe93; `HOME/model_registry` (ledger 106 lines; `orientation_net_v2` re-registered 16 times),
`HOME/mlflow/mlflow.db` 1,028,096 B; environments `HOME/mambaforge/envs/{spineps, fluorogen, spinedet}`, `$RS/envs` 39.923 GB,
`$RS/singularity_cache` 17.040 GB; the identity tables (`HOME/patient_keys_final.json` 5,913,937 B, `split_final.json`,
`bank_splits.json`); the credential files on HOME by name only (`~/github` token, mode 600: Greg rotates and deletes;
`~/CTSpinoPelvic1K/.token`); `$RS/data/_index` absent; `$RS/results` absent; `$RS/archive` empty; `$RS/data/morphdef` three
empty folders; `$RS/data/ctsp_april` world-writable.

**Repositories referenced.** `spinesurg-ct-nnunet` 097933a (`data_platform/`, the slurm of row 152: `data_accounting`,
`data_ledger`, `audit_*`, `ctsp0533_*`, `grid_ff_checkout*` which no longer work).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | when the three `dp_migrate` jobs end, read `plan/runs/{B04,B07,B09}/STATUS`; cut over per `MIGRATION_PLAN.md` section 3 e-f; smoke checks section 4 | every item VERIFIED or ABSENT with a written reason; symlinks in place with `.pre-ceph` twins; the grid `tools/realxray_banks.json` lists `cobra_elekta_v3` and `_g3test` (OQ B19) | the jobs | engineering |
| 2 | B10 (64 single-source banks) and B11 (64 multi-source banks and identity tables) after B04 / B06 / B07 land; back up `~/split_final.json`, `~/patient_keys*.json`, `~/bank_splits.json` to Ceph first | STATUS VERIFIED with measured sizes; the backups' sha256 recorded; `~/allspine_v9_fov96_ctx` never rerun in place (`slurm/allspine_v9_bank.sh` L21 `rm -rf`) | step 1 | engineering |
| 3 | build the holding index: `sbatch -D "$PWD" data_platform/db/build_index.sbatch` | `$RS/data/_index/holding.sqlite` exists; its file count equals the census count per collection | steps 1-2 | engineering |
| 4 | Greg's decisions (`MIGRATION_PLAN.md` sections 1, 8; OQ A26): deletions (1,590.3 GB candidates), B13 (627 GB), DUA / EULA folder permissions, the three B14 inspect-only entries, when `~/s1v11` opens; then FINALIZE batch by batch | `pan_quota` below 90 % after B02 and B06 are finalized; each FINALIZE recorded with its job id | Greg | Greg |
| 5 | repair the records: B01 (re-acquire with `reacquire.py tcia_ct_colonography`, route `tcia_ctsp_download`, 1,057 GB, or write the deletion record naming `~/cleanup_v1v3_tcia.sh`); CTPelvic1K 1-5 re-download (Zenodo 4588403) in a job; the grid checkout brought to 097933a by archive; the login-node instructions in `ssn:CLAUDE.md`, `PIPELINE_RESUME.md`, `MODEL_REGISTRY.md`, `containers/build_container.sh` replaced by `sbatch` forms (OQ F10); `~/github` and `~/CTSpinoPelvic1K/.token` rotated and deleted; `$RS/data/ctsp_april` permissions; the `"\` directory removed; the content-hash chain on the real corpus (OQ C16); the identity tables re-keyed into `tools/identity/` (OQ F14) | OQ B30, B31, B32 answered in `STATUS.md` with the file or job that answers them | Greg (re-acquisition) | Greg, engineering |

**Dependencies.** Greg's per-batch decisions. Every other project depends on it; its first three steps run in week one.

### 11 `11_students_grid_access`: students on the grid, Beethoven, onboarding, the lab recipe and the med-ed record

**Goal.** Keep the path by which students reach the grid and do a project working: Beethoven (browser extension + `hpcworker`,
release 14.0.0, `OpenSpineConsortium/beethoven` 2f90319; Beethoven for VS Code and the access service,
`OpenSpineConsortium/beethoven-vscode` 8d7fc65), the onboarding one-liner and `Student_Projects` (`RECIPE.md`, the board,
templates; local commit 3f1cf04 not pushed, OQ A25), the review Spaces and annotator tooling, the access-list gate on
`/rs/rs_grp_oschome` (named-user ACL entries), and the medical-education study (published in Cureus 14 July 2026, DOI
10.7759/cureus.112661; the JEEHP version would duplicate it, OQ A21).

**Reader.** Greg-only until the six Beethoven notes and the access-gate note are redacted; student-safe afterwards for the
guides, the recipe and the tutorials, never for the compliance and licensing notes or the roster.

**Why it is high for operation.** It worked in the field on 2026-10-02 and the dead-run-record failure was fixed in 13.0.0;
two failures stand (VPN sittings die about five minutes after the last keystroke; `reqp`/requeue preempts workers;
`context/beethoven-2026-10-02-field-failures.md`); the approved roster lives only in the access service (OQ B34). No finding
is expected; its product is students producing work under the recipe.

**Families absorbed.** grid_access_students (44 rows): the repositories by reference; copied: Beethoven `docs/`
(RESEARCH_REPORT, ARCHITECTURE, DIAGNOSTICS, OPEN_QUESTIONS, WAYNE_STATE_PILOT, the V11 / V12 CONTRACT and STATUS, TESTERS, the
guides, `CLAUDE.md`, SECURITY, PRIVACY), `ashley/docs/CHECKPOINT_2026-09-28.md`, LICENSING, ENGINEERING, `docs/research/`;
`Desktop/cureus.pdf`; `ctsp:OSC MedEd Manuscript - JEEHP.docx`, `Med_Ed_CNS.pptx`, `Med_Ed_CNS_visual_abstract.pptx`,
`ctsp:docs/survey_protocol.md` (the raw survey CSV never); `ctsp:proposals/student_primer_email.md` and
`cm_spine_request_email.md` redacted; `ctsp:Browser Extension HPC Orchestration Protocols.pdf`, `University-Agnostic HPC AI
Architecture.pdf`, `ctsp:openresearch/*.txt`; `HANDOFF/README.md` sections 4, 8-10 (roles only), `INFRASTRUCTURE.md` sections
2, 8, 11, `GLOSSARY.md` grid section as extracts; the 18 memory notes of the cut list (six Beethoven notes and
`grid-access-list-gate` redacted by hand). By reference: `Student_Projects` (`board.json` names students),
`ctsp:review_service/`, `reviewtool/`, `spinesurg-ct-annotator` (`assignments.json` may name students),
`openspineconsortium.github.io/tutorials/`, `onboard.sh`, `onboard.ps1`; excluded: `Desktop/Ashley Bridge for testers` and the
6.0.0 tester zip (superseded by release 14.0.0), `C:/Users/grego/.beethoven-vendor` (never read).

**Grid paths it owns** (`grid_manifest.md` section 3.8): `$RS/hpcworker` 1.076 GB, `hpcworker-ci`, `$RS/ashley` 2.136 GB,
`/rs/rs_grp_oschome/shared/{beethoven, access, ashley -> beethoven}` (other-readable; the volume root `drwxrws--T` with
named-user ACLs), `HOME/.beethoven` (`.ashley` -> `.beethoven`), `HOME/.hpcworker`, `HOME/hpcworker_src`, `$RS/tmp` 30.278 GB
of `hpcworker` temp; the review Space trees `HOME/CTSpinoPelvic1K-review`, `ctspinopelvic1k-review-triaged`,
`spinesurg-ct-annotator.backup` (usernames; never copy).

**Repositories referenced.** `OpenSpineConsortium/beethoven` `main` 2f90319 (`framework/`, `extension/`, `release/4.0.0-14.0.0`,
`docs/`; `extension/src/licensing/keys.json` holds a verification key only), `OpenSpineConsortium/beethoven-vscode` `main`
8d7fc65 (`grid/`, `cli/`, `tools/intake`); both pushed with `tools/push_org.sh` (whether these commits are pushed is not
recorded); `OpenSpineConsortium/Student_Projects` 3f1cf04; `Gregory-Schwing-MD-PhD/spinesurg-ct-annotator` 1083c4f;
`openspineconsortium.github.io`.

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | redact and copy the six Beethoven notes and the access-gate note; confirm with Greg which `GREG_ONLY/context_beethoven/` facts the INFRASTRUCTURE and README sections cite | a grep for `@`, key ids, account names and usernames over `memory/` returns nothing personal | nothing | Greg (whether the notes travel at all) |
| 2 | the two field failures: the OOD idle sweep (keep-alive or a documented sitting rule) and the partition profile (`secp`/secondary, pending Greg) | a worker survives 30 minutes idle in a test; a two-hour test job is not preempted; a student completes the first-week recipe (`HANDOFF/README.md` section 8) end to end | nothing | Greg (profile) |
| 3 | OQ A25: push `Student_Projects` 3f1cf04 (a public repo) or record why not; the board's draft leads | pushed or recorded as held; the remote's HEAD in `MANIFEST_CODE.md` | nothing | Greg |
| 4 | OQ A21: drop the JEEHP med-ed submission or redesign it as a follow-up with new data (Ashley Schehr leads) | the decision written in `STATUS.md` | nothing | Greg |
| 5 | the stale entry documents students read first (OQ F10): `ctsp:README.md` (v5), `STATUS.md`, `ROADMAP.md`, `ssn:CLAUDE.md` login-node line, `templates/CLAUDE.md`, `onboard.md`, the primer, updated together; OQ B34 the roster read from the access service and the gate documented as a mechanism, not people | no student-facing document instructs python on the login node; every one names v11; README names named ACL entries, not names | 03 step 4 | engineering |

**Dependencies.** 10 (the Ceph access gate), 03 (dataset documents).

### 12 `12_website_pacs_demo`: the public site, the PACS demo and the level-service client

**Goal.** Maintain `openspineconsortium.github.io` (211 commits; the local clone c1800f8 is behind origin a17ea39 by ten commits
of 2026-10-07; `inventory3_other_spine_folders.md` section 2.7): every page a body fragment under `tools/pages/**` built by
`tools/build_site.py`; the NiiVue PACS demo on case 0003 consuming `metrics.json` from `ostk tools/export_demo_case.py`; the
X-ray tab calling the level service at `SERVICE_DEFAULT` (`https://level-id.openspineconsortium.org`, not live on 2026-09-14,
not re-checked); the level atlas table (48 rows); tutorials, onboarding and the Beethoven pages; the people page from
`contributions/manifest.json`. Never serve weights; never add `pacs/testimgs/` (BUU films, not redistributable).

**Reader.** Student-safe (the site is public; its names are there by design and are not copied into the seed).

**Why it is high as maintenance.** Nothing to discover; the one decision (hosting the service) belongs to 01 S2. Latency record:
PACS X-ray demo 40,018 ms -> 1,360 ms (RC G.8).

**Families absorbed.** website (13 rows; 12 after merges): the repository by reference; copied: `ctsp:assets/` (OSC logo svg,
png, `osc_logo.py`), `Desktop/OpenSpineConsortium-logo/` (10 renders), `ctsp:poster/` (the OSC visual abstract and its build
scripts); `INFRASTRUCTURE.md` section 6, `MANUSCRIPTS.md` section 12 as extracts; the 5 memory notes of the cut list
(`engine-swap-architecture`, `level-service-serving`, `pacs-demo-and-ostk-params`, `pacs-website-latency-root-cause`,
`hf-identity`). By reference: `openspineconsortium.github.io/pacs/` (`remote.js`, `xr.js`, `infer.js`, `pacs.js`),
`atlas/level_atlas.csv` + `build_table.py`, `AI_Imaging_Workshop.pdf` (two sizes exist). Not copied: `googlec3911e7fb095977e.html`
(a site-verification token; the tracked copy is the record).

**Grid paths it owns.** None; `HOME/level_id_service` (`app.py`, `weights/`, 2026-09-14; serves `detect_v5z_epoch25`) is listed
because the service ran on the login node on 2026-09-14 and must not again; `$RS/data/gallery`.

**Repositories referenced.** `OpenSpineConsortium/openspineconsortium.github.io` `master` (pull first); `OpenSpineToolkit`
cb43197 (`tools/export_demo_case.py`); the two Beethoven repositories (their texts are rendered into `/beethoven/`).

**First five steps.**

| step | what | gate | depends on | who decides |
|---|---|---|---|---|
| 1 | `git pull` origin master (ten commits behind) before any edit | a clean fast-forward; the lab-storage request and admin pages present; `git status -sb` shows no divergence | nothing | engineering |
| 2 | ignore or delete the untracked `pacs/testimgs/`, `pacs/webtest/`, `pacs/sllp/`, `headshots/*.orig`; a pre-commit check that refuses `.pt`, `.onnx`, films and `testimgs/` | `git status` shows no film; the hook exists and is documented | nothing | engineering |
| 3 | the X-ray tab: when 01 S2 ships, point `pacs/remote.js` at the chosen host; otherwise remove the `SERVICE_DEFAULT` call | `GET /health` returns the registry entry of the reported stack, or no page calls a dead endpoint | 01 S2 | Greg (hosting) |
| 4 | regenerate `atlas/level_atlas.csv` from the v11 columns after 05 step 3 | the CSV carries its commit and equals `ctsp:morphometrics/level_atlas.csv` at a named commit; L5 end-plate width and pedicle width stay withheld until 05 step 5 passes | 05 | engineering |
| 5 | re-check the data page's mirror sentence (OQ A20), the tutorials and the onboarding pages against OQ F10 and the v11 scheme | no public page says v10 after the push; no page instructs python on the login node or names id 29 as current | 03 step 4; 11 step 5 | engineering |

**Dependencies.** 01 (the service), 04 (the demo exporter), 05 (the atlas), 11 (onboarding text).

### 99 `99_archive`: superseded, refuted and dormant work kept as a record

**Goal.** Keep, dated and never as a source of a quotable number, with the reason each item is here and what replaced it, so
nobody repeats it: FluoroCap (the literature harvest; 4,979 figures, 10,281 panels, 72.8 % of panels with zero pixel residual;
test set only by directive D1; the four FluoroCap documents and `PATHOLOGY_SOURCE_SWEEP_2026-09-14.*` copied; the 80
`fluorocap_*` tools, 14 slurm chains, `benchmark/data/fluorocap_v0.1/`, `HOME/REPORT.md` and `REPORT_interim.md` by path); the
generative translation routes (`fluorogen-synthetic`, `drr-to-fluoro-levers`: SDXL img2img dead at every strength, CUT not a
lever, CycleGAN and ADDA refuted); the refuted losses and rules (STC loses to cross-entropy, C1.7; R + C = 22, D.24; the pelvic
Castellvi cues, D.21; foramina counting, F.39); one page `SUPERSEDED_NUMBERS.md` listing every v2-lineage, leaked or wrong-bank
number with its replacement (98.22 % -> 97.4 % A3.1; 96.3 / 37.9 -> 96.4 / 43.7 A2.1-A2.2; 72.9 / 97.0 / 44.9 -> 74.8 A3.3; 99 %
at 35.7 % coverage, leaked, no clean re-run OQ C13; 97.47 / 99.02 LEAKED; 98.7 / 99.1 / 99.4 wrong bank C1.2; 96.7 % on the
cervical-dominated bank C1.1; the 2026-09-17 scaling sweep C2.1; "100 % sacrum on DeepFluoro"; the 734x linker speed-up; any
guided-loop corpus number), noting that `sn:tables/tab3_naming.md` and the three `atlas/model.json` copies still print the
stale rows (A2.9, A3.11; fixed in 01); the dated checkpoints (`ssn:docs/RESUME_2026-09-22_PM.md` 367 KB with the banned word
removed, `RESUME_2026-09-22.md`, `DAILY_REPORT_2026-09-22.md`, `MORNING_BRIEF_2026-09-16.md`, the two `HANDOFF_2026-09-21_PM.md`,
one copy if identical; the five history-only resume memory notes by reference, `resume-2026-09-21-pm` names a researcher and an
e-mail); the superseded plans (`RSNAI_PLAN.md`, `RSNAI_CLAIMS.json`, `FEASIBILITY_REPRODUCE.md` stay in 01 as history flagged
superseded; `PATENT_PACKAGE.md` is excluded); the superseded manuscripts and builds by path (`Desktop/MDPA.pdf`, `ctsp:MDPA.pdf`,
`MDPA_OL.zip`, the two overleaf folders, the root source zips, `ctsp:dist/`, `sn:packet/`, `packet_cameraready/`, the 16 earlier
packet PDFs, `Desktop/new_repo`, the pre-purge bundle 97.8 MB: reference only, never push); the talks presented or superseded
(`TechFair_LSTV_Schwing.pptx` one copy; the CNS decks v2, v3, v9, v11 and the v10 twin by path; `Desktop/MANS_Talk/` md and html
outlines; `GREG_PRES.pptx`, `SPINAL_AVM.pptx` by path); early scratch (`np:action_items.txt` redacted, `meeting_agenda.docx`, the
Castellvi IV example image, `Desktop/FUC/`); one list `LITERATURE_BY_PATH.md` of every third-party PDF kept by path with its
identifier (`COBRA.pdf`, `RIBSEG.pdf`, `TS_DS.pdf`, `PANJABI_1991_FULL*.pdf`, `panjabi_1976.pdf`, `STUMP_RIBS.pdf`, `MANUAL_REFS/`,
the SpineSurg-CT and nsurg/AACA literature, the saved HTML pages; library access was cut 2026-06-30, so the paths matter);
`ssn:LICENSE`, `NOTICE`, `.gitignore`, `.github/workflows/ci.yml` by path; `$RS/data/rsna_2022_cspine/raw` (237 GB used by
nothing; keep or delete is OQ A19). Its `README.md` carries the "superseded by what" chains of
`ctsp_repo_root_and_sibling_folders.md` section 4, `desktop_root_loose_files.md` "Superseded chains" and
`memory_and_handoff_map.md` "What is superseded by what".

**Reader.** Greg-only (it holds SchwingNet decks and private draft history). **Steps.** None beyond the listing; nothing in it
is run.

---

## 4. Where the two proposals disagreed and what was decided

Both proposals arrived at the same twelve projects and one archive, the same token-to-folder mapping and the same regulatory,
redaction and copy rules; they differed on order, on where the HANDOFF lives, on the archive's number and on a dozen rows.
**Order.** Angle A ranked the transitional truth file second and the data platform fourth (support that blocks 01); angle B
ranked the dataset second, the toolkit third, the transitional work ninth (low likelihood) and the data platform tenth (a
support project, not a hypothesis). This plan takes B's principle (rank research projects by likelihood, support projects
after them) with A's one exception: 02 stays second, not because it is likely to reach its bounds (it is not: 0 verified
persons against 22 or 35) but because the hospital test's pre-registered endpoint is transitional and 01's S5 cannot be
written without 02's truth file, reader protocol and power table; the folder says so in its own README. The toolkit moves
to fourth (B) because its two one-hour fixes block every morphometry number (RD CT-1 "depends on: nothing"); plain film (07)
sits above the QI / clinical folder (09) because its held-out corner numbers are complete while the clinical folder's one
number is v5-era; render devices (08) stays between them as support 01 may need after S3. **The HANDOFF.** A cut it per folder
into extracts; B kept whole copies in 01 (and LEAKAGE / INFRASTRUCTURE in 10, LITERATURE_STATE in 09) with extracts elsewhere.
This plan copies the eight student-readable files whole into every folder (about 350 KB each, so a student with one folder
has the catalog) and the Greg-only files whole into the five Greg-only folders, extracts elsewhere (section 2 rule 3). **The
archive** is `99_archive` (B), so its number says it is not a project. **Rows.** Where the two inventories or the two proposals
put a file in different homes, the decision is in `DISPOSITION.tsv` under `|| decision:`; the ones that matter: `IRB_ADDENDUM.md`
copied into 01 with the IRB contact cut (B) rather than referenced (A); `COMMERCIALIZATION.md` excluded (both); the CNS
generator and the public v12 and LSTV decks into 03 (B) rather than archive (A); the two `HANDOFF_2026-09-21_PM.md` and
`RESUME_2026-09-22_PM.md` into 99 as dated checkpoints (B) rather than 01 (A); the `spine-detector/src/` snapshot copied into
01 (B) rather than referenced (A), because the local folder has no `.git` and the runtime needs `canonical_slots`;
`LEVELCHECK_MODEL.md` into 02 (both); `STUDENT_FLUORO_CORRECTION_GUIDE.md` into 01 (both); the memory note
`cns-deck-v2-2026-09-25` into 03 (B); the six Beethoven notes into 11 redacted (both, with Greg's veto recorded in section 5).

---

## 5. Decisions reserved to Greg (written into each folder's TODO.md as "Greg decides")

OQ A1 (SchwingNet uploaded?), A2 (MPDA packet, number), A5 (VinDr determination), A6 (NeurIPS deadline and uploads), A7
(appendix chains or cut I-J), A8 (BIBM, SPIE, VerSeFusion submissions), A9 (the three optional arms), A14 (affiliation word),
A16 (sign PREREG), A17 (the 546 verdicts), A18 (who is "Dr Tech"), A19 (the RSNA 2022 archive), A20 (HF mirror), A21 (JEEHP),
A22 (arXiv replacement), A23 (CNS slides submitted?), A25 (push Student_Projects), A26 (migration deletions, B13, permissions,
`~/s1v11`), A27 (area chair), A29 and A30 (the reader split and the withheld personal data); the hospital's C-arm and the
faculty sponsor (01 S3-S4); the BUU licence; whether `HANDOFF/GREG_ONLY/` content enters `spine-program` at all (this plan
keeps it out and references it by path); whether the QI manuscript, `GUIDED_ACQUISITION.md`, `SWEEP_PROTOCOL.md` and the
sweep / count / confirm documents may sit in the private repository before the provisional is filed (this plan copies them
into 01 and 09 as research documents with a PRIVATE banner and references `INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`,
`provisional/` and `disclosure_*` by path); whether the six Beethoven notes travel into 11 (this plan copies them redacted; Greg
may delete them); whether Ashley Schehr's name appears in folder text (a published co-author and a person never renamed;
usernames never); whether `CASE_HIEBER` holds a cervical case report Greg wants kept (excluded: it holds patient documents);
whether `morphometrics/annotator_names.csv` and `spine_tampering.csv` leave the public repository; the credentials of section 6.

**Answered by Greg on 2026-10-12** (his comments on issues #68 to #72; recorded by the pull request of #68). A29: option
(a), every Write holder may read all 13 folders; "Greg-only" and the label `greg-first` govern claiming and hand-outs,
not reading, and a hand-out is Greg's comment on an issue naming the student's login, or the label `greg-first` removed.
A30 has no separate answer; the withheld personal data stays out of the repository (root `CLAUDE.md` rule 12). A26,
`~/s1v11`: opened to approved students without the token check (spinesurg-ct-nnunet 0ab783f drops it from
`FIXED_RESTRICTED_PATHS`; visibility job 40602925, issue #69); the one path still owner-only is
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, because its one file is the
annotator map, students' personal data rather than a dataset or a token. A26, B13: finalized; the migration chain
completed at 08:41 EDT on 2026-10-12 (`10_data_platform_grid/MANIFEST_GRID.md` section 2). The credentials of section 6:
no rotation planned (section 6, issue #70). The history of main with the redacted values: kept as it is (issue #71;
`MANIFEST_LOCAL.md` of 01, 08 and 10).

## 6. Credentials to rotate (paths only, never contents; from the four laptop inventories and `grid_manifest.md` section 3.10)

`ctsp:LATERAL_ATLAS/key.txt` (an AWS key pair; its first two lines were printed into a tool output on 2026-10-08: treat as
exposed), `Desktop/NeurIPS/client_secret_*.apps.googleusercontent.com.json` and `Desktop/client_secret_*.json` (Google OAuth),
`Desktop/openapi_key.txt`, `np:spinopelvic-seg-mlhc/.git/config` (a GitHub token in the origin URL; the folder is excluded whole),
`nsurg/AACA/firebase/*-adminsdk-*.json` (a Firebase service account), `onboarding/personal_key.txt` (Login.gov), `ctsp:.env`,
`ctsp:cookies.txt`, the Cerner `.ica` session files (eleven in `ctsp:`, two at the Desktop root, five untracked and one tracked in
`xrsp:` at 4f22935 and on the grid clone), `Desktop/FJP.docx` (an ssh login line), `ctsp:go2432@warrior__.pdf` (a printed login
banner); on the grid `~/github` (41 B, mode 600), `~/CTSpinoPelvic1K/.token` (38 B), and by name only `~/.hf_org_token`,
`~/.hf_osc_token`, `~/.zenodo_token`, `~/.fluorocap/`, `~/.kaggle/`, `~/.netrc`, `~/.gdrive_token`, `~/.geo_ftp_pass`, `~/pass_file`,
`~/private`, `~/.certs`; `C:/Users/grego/.beethoven-vendor` (never read). Whether the GitHub token and the Firebase key are
still live is not recorded.

**Greg's answer, 2026-10-12** (issue #70: "dont worry about tokens"): no rotation is planned; the credentials stay where
the list above puts them, and no rotation date is recorded for any of them. The readiness review's scan of 2026-10-12
found no secret value committed (issue #70).

## 7. Unknowns this division leaves (from the inventories, not re-derived)

The hospital's C-arm make, model and software; whether any DMC protocol was submitted; the VinDr determination number; the
identity of "Dr Tech" and the spelling of the Neurosurgery co-investigator's name; whether the 148 C-ArmLSpine cases are 148
people (OQ E1); whether `~/model_night/heads_mixed/` and `ensemble/ensemble.json` exist (the listing was truncated); whether
B10 has run; the commit of the local `spine-detector` snapshot; the identity of `xrsp:dataset2024.zip`; the origin of the root
`Archive.zip` (2,682 PNGs `JW_T1_J1_L_*`); which build produced `Desktop/morphometrics/transition_morphometrics.csv`; which
checkpoint made `NeurIPS/ens/` and `pred/`; the outcome of IRB-26-03-8648; whether `Student_Projects` 3f1cf04,
`CTSpinoPelvic1K-Syn` and the two Beethoven commits were pushed; whether the eleven `np:viz/*_lstv_3d.html` equal those under
`nsurg/AACA/citations/3d`; the live state of Zenodo v11, the HF mirror, the private weights repo and `level-id.openspineconsortium.org`
(no network was used); whether the GitHub token in the mlhc git config and the Firebase key are live.

## 8. Size and shape

Everything copied is text, small result files, PDFs, decks and figures under 25 MB each. The largest folders are 01
(SchwingNet PNG / PDF figures about 170 MB without the TIFFs, the two 2026-09-27 packet PDFs 12.6 MB each, the results md / json)
and 03 (the MPDA and NeurIPS figure PDFs, the NeurIPS per-case CSVs, the decks 2.3 to 13.6 MB); the whole repository should
stay under 1 GB with every file under GitHub's 100 MB limit. Where a folder would exceed that, the figure PNGs go by path
first (they regenerate from the `.record.json` sidecars).


---

## 9. Corrections of the final pass (2026-10-08, after the critic's check; details in `BUILD_RECORD.md`)

1. **Owners settled.** `/wsu/home/go/go24/go2432/model_registry` and its ledger `registry.jsonl` belong to 10 (section 3 listed the path under 01 and 10); 01 appends rows (S0), 12 names weights by id, neither edits the ledger. `split_final.json` and `patient_keys*.json` belong to 10 (01 reads them). `bench` is one directory listed by 01 (latency files) and 03 (the harness); both say so. `physics_rare` belongs to 08; 02 reads it.
2. **Rule 2d applied.** 01 no longer holds `HANDOFF_PHYSICS.md`, `PHYSICS_SWEEP_NO_BONE_2026-09-22.md`, `PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md`, `SIMULATION_FIDELITY.md` (08 owns), `WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md` (09 owns) or `JOBS_RECORD_2026-09-27_1544.*` (10 owns); the remaining shared copies are recorded as shared on both sides.
3. **Rule 3 applied.** The Greg-only working notes topic 2 and topic 6 and the `literature_state/` scripts were removed from 06, 03 and 10; they stay whole in 01, 02, 07, 08, 09.
4. **08 `code/`.** The nine scripts section 3 promised are copied (the disposition rows ssn r132, r133, r150 had said reference; the plan wins), with the two untracked cine files and the SpineSurg-CT synthesis line (0051074).
5. **Six left-behind items added.** lstv-fusion (3c8f5c1) into 06; the SpineSurg-CT augmentation line into 08; `slurm/polypose_cine.sh` into 08; the May 2026 NeurIPS submission source into 03; the co-author review files into 03; the presentations record (redacted) into 99 with a STATUS row in 11.
6. **Redactions made uniform.** The one Hugging Face handle withheld in every folder; the ten student co-author names withheld in the 07 and 08 handoff copies and the 03 deck generators as 01 and 02 already had them; the library address withheld in every memory copy; 06's review-case count 546 is 446 + 103 = 549 (fixed by 06's verifier).
7. **Numbers.** `DISPOSITION.tsv` is unchanged; the copy counts of section 1 are the first build's and are superseded by each folder's `MANIFEST_LOCAL.md` final-pass section.
