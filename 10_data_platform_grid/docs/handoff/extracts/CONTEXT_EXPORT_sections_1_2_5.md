# Extract of HANDOFF/CONTEXT_EXPORT.md (spinesurg-ct-nnunet 097933a)

Sections 1-5, per DISPOSITION rows 94-98. Section 3's one-line digests are dated and several carry leaked or superseded numbers; `memory/CONTEXT_INDEX_2026-10-08.md` gives the status of each.

The whole file is Greg-only and sits in the Greg-only project folders (`01_carm_level_detection/docs/handoff/` and the others `../_plan/PLAN.md` rule 3 names); this extract carries the sections that bear on the data platform, with their section ids. Path prefixes (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:`) read as the repositories of `MANIFEST_CODE.md` at the stated commits, never as a laptop path. Two researcher addresses are withheld.

---

<!-- section: 1 What context/ holds -->

## 1. What `context/` holds

- **After the refresh of 2026-10-08 (see `context/COPIED_AT.txt` for the time): 141 notes in `context/` plus
  `context/INDEX.md`**; `GREG_ONLY/context/` holds `MEMORY.md` (the original index, kept as an archive: its links to
  U251, history-only and Beethoven notes do not resolve), the five moved notes (`commercialization-stance`,
  `schwingnet-disclosure-scrub`, `hf-org-token-location`, `hf-osc-token-and-namespace`,
  `fluorocap-credentials-and-resolution`) and the full copies of the three redacted notes (`annotator-roster`,
  `learned-formation-refuted-calibrate-instead`, `lstv-data-landscape`); `GREG_ONLY/context_beethoven/` holds the six
  Beethoven product notes. The first copy (12:28) held 145 notes plus `MEMORY.md`. Every live note on spine imaging, CTSpinoPelvic1K, SchwingNet, the anomaly scan, data, splits, the
  grid, the toolkit, the website, students, manuscripts, figures and standing preferences is there, including the four
  dormant FluoroCap notes (FluoroCap is out of training by directive D1 but still sits inside the C-arm fold banks, so the
  notes still bear on open work) and the credential-location notes (they name files, never values; a scan for token-shaped
  strings found none).
- **Left out (13)**: the seven U251 / LITT notes (another project: `u251-*`,
  `litt-contralateral-two-readings`, `cns-abstract-418-deck`) and the six history-only entry points (`resume-*`,
  `overnight-2026-09-15-chains`). The six Beethoven product notes were at first left out as "living with the Beethoven
  repository"; a search of `Desktop/ashley-bridge/docs` found the compliance boundary only in store texts and nothing of
  `beethoven-first-run-ux`, so they are now copied to `GREG_ONLY/context_beethoven/`.
- **One substitution, made on purpose.** Greg bans one word (named in `CTSpinoPelvic1K-1/CLAUDE.md` "Standing
  preferences"). Since the refresh the copies are byte-for-byte identical to the originals, line endings included, except (the
first copy had normalised about twenty notes' CRLF line endings to LF): where a note states the rule, the quoted
  word is replaced by `[the word named in CTSpinoPelvic1K-1/CLAUDE.md "Standing preferences"]` (in `writing-preferences.md`,
  `schwingnet-manuscript.md` and `GREG_ONLY/context/MEMORY.md`); everywhere else the word became "origin"; and the note whose file name
  carried it is copied as `splits-origin-and-v3-resplit.md`, with every link to it renamed (`MEMORY.md`,
  `ct-benchmark-covers-all-collections.md`, `label-scheme-v4-vs-ostk.md`, `lstv-reread-queue.md`,
  `prone-supine-flexibility-future.md`, `rib-auto-engulf-post-correction-only.md`, `thoracic-gt-fov-limited.md`). The
  copying script was `scratchpad/handoff/copy_context.py` and is now
  `working_notes/builders/refresh_context.py` (its context half, with the moves and redactions); both refuse if the word
  survives. The three redactions replace e-mail addresses, one telephone number and the per-student tally with a pointer
  to the full copy.


---

<!-- section: 2 How a fresh Claude project should load this -->

## 2. How a fresh Claude project should load this

1. Put `HANDOFF/README.md`, `HANDOFF/INFRASTRUCTURE.md` and `HANDOFF/context/INDEX.md` (not `MEMORY.md`: its one-line
   summaries carry leaked numbers and point at notes that were not copied) in the project's standing instructions or
   knowledge; add the two repository `CLAUDE.md` files and, for Greg's own project, `GREG_ONLY/PRIVATE_STATE.md`.
2. Load the `context/` notes as reference documents, not as instructions to obey blindly: the "status" column below (and
   `context/INDEX.md`, which names the replacing file and number) says which are leaked, superseded, dated or partly
   superseded, and `README.md` §5 lists the ten rules that bind.
3. Treat every number in a memory note as dated: the result files and `RESULTS_CATALOG.md` win where they disagree
   (examples: `film-ncurve-ablation-result` says all seven separated cells favour renders; the tool's own `READ.md` says six
   help and one hurts; `rsnai-paper-endpoint` calls `main_v2.tex` the culmination; `SchwingNet/main.tex` superseded it).


---

<!-- section: 3 Digest of every memory note (one line each; several digests carry LEAKED or SUPERSEDED numbers: read the status column) -->

## 3. Digest of every memory note

Status codes (from the reader digest, corrected by the 2026-10-08 verification): LEAKED = the note's numbers were
measured on a bank with a known leak; SUPERSEDED = replaced by a later number (named in `context/INDEX.md`); RECORD
ONLY = history, not quotable; CURRENT = a standing rule or a still-valid fact; DATED = a state or result at its
date, check newer files; PARTLY SUPERSEDED = a later file replaces part of it; HISTORY = a superseded entry point; DORMANT
= about FluoroCap, dropped from training 2026-09-23. Project codes: SN = SchwingNet / level identification / fluoroscopy and
films; CTSP = the dataset; ANOM = transitional census and anomaly harvest; DATA = identity, splits, audits, platform; GRID
= cluster; BTH = Beethoven / Ashley (the extension; Ashley Schehr is a person); FC = FluoroCap; OSTK; WEB = website / PACS
demo; LAB = students and annotation; PREF = working rules; CRED = credential locations; REF = literature or external
reference; DECK = talks; U251 = the separate RNA-seq / LITT project.

Counts: 165 notes (164 at the first build plus `grid-bash-4-2-quoting`); 159 live, 6 history-only; 141 in `context/`
(three of them redacted), 5 moved to `GREG_ONLY/context/`, 6 in `GREG_ONLY/context_beethoven/`.

| note | one line | project | status | live / history-only | copied to `context/` |
|---|---|---|---|---|---|
| `acquisition-space-saturation` | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); claim wording | SN | CURRENT | live | yes |
| `annotator-roster` | who annotated what, from `slots[].reviewer` in private ledgers; 13 students by 2026-08-23 | LAB | DATED | live | yes, redacted (full copy in GREG_ONLY/context/) |
| `anomaly-harvest-directive` | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in FOV | ANOM | CURRENT | live | yes |
| `anomaly-manifest-sources` | 749 anomalous spines in 3 tiers; master table `lstv_flag_labels_v2.csv`; why the count was once 34/16/2 | ANOM | DATED | live | yes |
| `anomaly-rule-rc22-evaluated` | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | ANOM | CURRENT | live | yes |
| `ashley-bridge-project` | Beethoven: framework + extension, versions 2.0.0-12.0.0, repos, shared copy, access model, rename | BTH | CURRENT (to 2026-10-02; 13/14.0.0 in repo log) | live | GREG_ONLY/context_beethoven/ |
| `ashley-compliance-boundary` | never handle a Claude credential; student signs in via Claude Code; legal findings and open written answers | BTH | CURRENT | live | GREG_ONLY/context_beethoven/ |
| `ashley-extension-project` | the VS Code extension (Ashley 3.0.0, Marketplace), keys, access service, still-needs-Greg list | BTH | PARTLY SUPERSEDED (renamed Beethoven for VS Code 2026-09-30) | live | GREG_ONLY/context_beethoven/ |
| `bash-heredoc-backslashes` | heredocs collapse backslashes; write scripts with Write, run by path | PREF | CURRENT | live | yes |
| `beethoven-2026-10-02-field-failures` | first real use: dead run records, VPN sign-in sweep, reqp preemption, group vs list; read the grid first | BTH | CURRENT | live | GREG_ONLY/context_beethoven/ |
| `beethoven-browser-ssh` | WebCrypto ssh prototype, IWA + Direct Sockets spike, policy limits, decisions waiting on Greg | BTH | DATED | live | GREG_ONLY/context_beethoven/ |
| `beethoven-first-run-ux` | Greg's eight-message brief for the first run: prerequisites, VPN, nothing silent, no window hunting | BTH | CURRENT | live | GREG_ONLY/context_beethoven/ |
| `canonical-rib-triage` | rib review set defined by `qc_v4_ribs_and_verts.py`; worklist regenerated from it | CTSP | DATED | live | yes |
| `carm-plateau-is-the-denominator` | same-device 82-85 % plateau is the truth denominator; clean subset 96.9 % | SN | CURRENT | live | yes |
| `carmlspine-level-experiment` | C-ArmLSpine (148 cases, AP+LAT+CBCT): reading traps, pose convention, pipeline | SN | CURRENT | live | yes |
| `chart-preferences` | slides: no sideways bars, donuts/lines, published background figures, big type | PREF | CURRENT | live | yes |
| `cloudflare-tls-fingerprint` | 403 everywhere = TLS fingerprint block; `curl_cffi impersonate="chrome"` | REF | CURRENT | live | yes |
| `cns-abstract-418-deck` | CNS Abstract 418 LITT talk, v5 46 slides, builder path | DECK / U251 | DATED | live | no (U251, another project) |
| `cns-deck-v2-2026-09-25` | CNS spine deck: v10 discloses Part B; public CT-side cut on the Desktop; generators and template traps | DECK / SN | DATED | live | yes |
| `commercialization-stance` | Greg's standing stance on what the work is for; never stated outward (GREG_ONLY/PRIVATE_STATE.md §1) | PREF | CURRENT | live | GREG_ONLY/context/ (moved 2026-10-08) |
| `commit-directly-to-master` | CTSP repo: commit to master, no branches | PREF | CURRENT | live | yes |
| `competitor-benchmark` | TS, SPINEPS/VERIDAH + Möller ribs, VISTA3D, RibSeg in the one-shot space; grid layout | SN / CTSP | DATED | live | yes |
| `context-ladder-2d-level-experiment` | how much spine must be visible to name a vertebra; BUU levels are counting-inferred | SN | DATED | live | yes |
| `ct-benchmark-covers-all-collections` | the CT axis is every collection (5,700+ subjects); `tools/ct_inventory.py` | DATA | CURRENT | live | yes |
| `ct-volumes-are-pir-not-ras` | volumes are (P,I,R) on disk; decide by reading the affine | CTSP | CURRENT | live | yes |
| `ctspine1k-selection-code-deleted` | CTSpine1K's supine/prone selector does not select; recover at 7f44959 | REF | CURRENT | live | yes |
| `data-audit-99-gaps` | 99 gaps in `docs/DATA_COMPLETENESS_AUDIT.md`; the ones that change the science | DATA | DATED | live | yes |
| `data-directives-2026-09-23` | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | PREF / DATA | CURRENT | live | yes |
| `data-platform-migration-2026-10` | data_platform: manifest, layout, batches B00-B14, census, state 2026-10-08, visibility | DATA / GRID | CURRENT | live | yes |
| `dataset813-image-links-are-container-paths` | Dataset813 imagesTr links resolve only in the container; never repair; `HF_EXPORT_DIR` | GRID | CURRENT | live | yes |
| `deepfluoro-convention` | DeepFluoro file layout and projection convention (0.00 px reprojection) | REF / SN | CURRENT | live | yes |
| `detection-is-the-binding-constraint` | counting fails on detection (60 points) not linking (11-28) | SN | CURRENT | live | yes |
| `device-sampling-audit` | card clip saturates (95-98 % of the joint lost); typicality gate | SN | CURRENT | live | yes |
| `diagnostics-graph-required` | every Beethoven feature needs diagnostics-graph nodes first | PREF / BTH | CURRENT | live | yes |
| `drr-row-spacing-defect` | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | SN | CURRENT | live | yes |
| `drr-to-fluoro-levers` | three measured levers for DRR→fluoro; CycleGAN/ADDA refuted; honest ceiling | REF / SN | CURRENT | live | yes |
| `engine-swap-architecture` | demo consumes a `metrics.json` contract so the engine can be swapped | WEB | DATED | live | yes |
| `feasibility-claims-measured` | the FOV feasibility report tested claim by claim; head/encoder pairing trap | SN | RECORD ONLY [LEAK] numbers (C1.14, C1.16) | live | yes |
| `figure-captions-terse` | captions short, argument in text; float spacing | PREF | CURRENT | live | yes |
| `figure-preferences-schwingnet` | Greg's figure verdicts for the SchwingNet manuscript (2026-09-22) | PREF / SN | PARTLY SUPERSEDED (five-figure paper 1, mem:paper-split-2026-09-24.md) | live | yes |
| `film-fluoro-boundary-not-transferable` | devices separate pairwise; film vs fluoro does not transfer to an unseen corpus | SN | CURRENT | live | yes |
| `film-ncurve-ablation-result` | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | SN | SUPERSEDED reading ("all help"; READ.md: six help, one hurts; A10.9) | live | yes |
| `flagship-paper-frame` | "ships a network"; claims ledger; `\PENDING` macros | SN | PARTLY SUPERSEDED (LevelCheck comparison moved to paper 2) | live | yes |
| `flagship-program` | gates G0-G7 in `docs/FLAGSHIP_PLAN.md` | SN | DATED | live | yes |
| `fluoro-panel-gap-diagnosed` | literature panels 19.7 % vs 95.1 % on radiographs: domain plus contamination | FC / SN | DORMANT | live | yes |
| `fluorocap-credentials-and-resolution` | `~/.fluorocap` credential store; publisher-original refetch | FC / CRED | DORMANT | live | GREG_ONLY/context/ (moved 2026-10-08) |
| `fluorocap-dataset` | FluoroCap test set on grid `~/FluoroCap`: stages, routes, manifest | FC | DORMANT | live | yes |
| `fluorocap-is-reproductions-not-fluoroscopy` | 72.8 % of panels have zero pixel residual; test set only | FC | CURRENT (the reason FC is out of training) | live | yes |
| `fluorocap-pipeline-resume` | start at `docs/PIPELINE_RESUME.md` and `tools/pipeline_state.py`; add every stage there (not in MEMORY.md index) | SN | CURRENT | live | yes |
| `fluorocap-prototype-and-lstv-arm` | single-image prototype, transitional harvest arm, Semantic Scholar route | FC | DORMANT | live | yes |
| `fluorocap-repo-private` | spinesurg private since 2026-09-14; never push level-ID code public | PREF | CURRENT | live | yes |
| `fluorogen-synthetic` | SDXL + ControlNet + LoRA synthetic C-arm frames; gmsap = 4 x 4 H200 | SN | DATED | live | yes |
| `grid-access-list-gate` | approved students = named ACL entries on `/rs/rs_grp_oschome` | GRID / BTH | CURRENT | live | yes |
| `grid-access` | login, project root, where CTs and labels lived, ITK-SNAP launch | GRID | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) | live | yes |
| `grid-apptainer-module-works` | `module load apptainer/1.2.2` sandbox builds; secp starts at once | GRID | CURRENT | live | yes |
| `grid-ashley-deletion-2026-09-28` | `~/.ashley` wiped during a phone session; destructive commands refuse under CLAUDECODE | GRID / BTH | CURRENT | live | yes |
| `grid-bash-4-2-quoting` | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail | GRID | CURRENT (new 2026-10-08 13:35) | live | yes |
| `grid-ceph-volume-oschome` | 20 TB Ceph volume, working tree, `df-ceph oschome` | GRID | CURRENT | live | yes |
| `grid-ct-0533-truncated` | CT 0533 truncation repaired on the grid and HF | CTSP | CURRENT (done) | live | yes |
| `grid-local-singularity-is-broken` | use conda singularity + pre-unpacked sandbox + specific bind | GRID | CURRENT | live | yes |
| `grid-quota-and-deleted-banks` | `pan_quota`; banks deleted 2026-09-20; `holdout.py` raises; refs → v7 | GRID | CURRENT | live | yes |
| `grid-slurm-inside-apptainer` | binds that make sbatch work inside a container | GRID | CURRENT | live | yes |
| `grid-ssh-second-factor` | ssh off-VPN with password + TOTP; warrior bans python, rsync and others | GRID | CURRENT | live | yes |
| `guided-acquisition-loop` | commanded displacement + digital fiducial; what must not be quoted | SN | DATED | live | yes |
| `hf-identity` | HF username `gregoryschwingmdphd` | CRED | CURRENT | live | yes |
| `hf-mirror-is-v10` | public HF/Zenodo is v10 with id 29; v11 local only; lines to change when it ships | CTSP | PARTLY SUPERSEDED (HF v10 as of 2026-09-27 stands; "Zenodo is v10" contradicted, MANUSCRIPTS C1) | live | yes |
| `hf-org-token-location` | `anonymous-mlhc` token location; personal token separate | CRED | CURRENT | live | GREG_ONLY/context/ (moved 2026-10-08) |
| `hf-osc-token-and-namespace` | OSC org token in four places; three tokens table | CRED | PARTLY SUPERSEDED ("v6 on main") | live | GREG_ONLY/context/ (moved 2026-10-08) |
| `identity-audit-findings` | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case ≠ person | DATA | CURRENT | live | yes |
| `journal-figure-and-style-rules` | Medical Physics figure and text rules; page estimate | PREF / CTSP | CURRENT | live | yes |
| `k-devices-one-network` | per-device parameter sets, styled renders, LODO; where the pipeline lives | SN | CURRENT | live | yes |
| `key-patients-from-metadata-not-filenames` | identity order: DICOM → manifest → ann fields → filename last | PREF / DATA | CURRENT | live | yes |
| `l6-sample-count-and-counting-decoder` | L6 dice 0.000 = too few cases; counting decoder; Dataset815 | SN / CTSP | DATED | live | yes |
| `lab-recipe-and-board` | RECIPE.md, board.json → BOARD.md, Claude Doc; local commit not pushed | LAB | CURRENT (location and count errors, section 13 rows 1-2) | live | yes |
| `label-scheme-v4-vs-ostk` | two live maps; `labels_for(volume)`; what the mix-up cost | CTSP / OSTK | CURRENT | live | yes |
| `learned-formation-refuted-calibrate-instead` | CT→fluoro formation calibrated on DeepFluoro; first real-fluoro recall | SN | CURRENT | live | yes, redacted (full copy in GREG_ONLY/context/) |
| `level-id-2d-results-2026-09-13` | 2-D level ID on real films, 13 Sep results | SN | RECORD ONLY (films_ann bank, C1.1) | live | yes |
| `level-model-bank-coverage` | the deployed bank held only cervical and lumbar films | SN | DATED | live | yes |
| `level-service-serving` | website never serves weights; service + private HF weights | PREF / WEB | CURRENT | live | yes |
| `litt-contralateral-two-readings` | contralateral U251N signal: say the measurement, instrument statements conditional | U251 | CURRENT (other project) | live | no (U251, another project) |
| `local-level-identity-thesis` | name a vertebra by local morphology instead of counting from C2 | SN / CTSP | CURRENT | live | yes |
| `lstv-data-landscape` | where LSTV/TLTV labels exist; the one published 2-D LSTV model | REF | DATED | live | yes, redacted (full copy in GREG_ONLY/context/) |
| `lstv-oneshot-training-run` | Dataset810 one-shot LSTV run for the CNS slides | ANOM / CTSP | DATED | live | yes |
| `lstv-reread-queue` | log doubtful source LSTV labels in `docs/lstv_reread_queue.csv` | CTSP | CURRENT | live | yes |
| `lstv-tltv-detection-goal` | standing determination: detect LSTV/TLTV from C-arm exposures | SN | CURRENT | live | yes |
| `mixed-length-head-and-sota` | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | SN | LEAKED (numbers on allspine v2; RESULTS_CATALOG C1.6; see context/INDEX.md) | live | yes |
| `model-registry` | content-addressed weights store, ledger, MLflow, HF mirror | GRID / SN | CURRENT | live | yes |
| `morphology-deformation-feasibility` | literature first; no bespoke CT warp | PREF | CURRENT | live | yes |
| `never-reorient-when-writing-labels` | `as_closest_canonical` + `nib.save` transposes a label | CTSP | CURRENT | live | yes |
| `nhanes-double-inclusion` | NHANES in the banks twice, split independently | DATA | CURRENT (fixed by patient keys) | live | yes |
| `nninteractive-colab-versions` | ITK-SNAP DLS (nnInteractive) Colab pins | REF | DATED | live | yes |
| `no-jobs-on-login-node` | every computation via sbatch; compute nodes have internet; C&IT addendum | GRID / PREF | CURRENT | live | yes |
| `no-unexplained-subsets-fix-not-disclose` | use all of a dataset; describe each in prose; fix leaks, don't disclose | PREF | CURRENT | live | yes |
| `oblique-angles-and-sweep-vision` | detector must work at any angle; synthetic AP→lateral arcs; AR vision is preview only | SN | CURRENT | live | yes |
| `ostk-canal-closing-regression` | ostk 1b7005c inflates VBHp/EPD 10-17 mm on ~1 in 7 vertebrae | OSTK | CURRENT (open) | live | yes |
| `overnight-2026-09-15-chains` | where the 2026-09-15 FluoroCap overnight runs wrote | FC | HISTORY | history-only | no (history-only entry point) |
| `pacs-demo-and-ostk-params` | ostk parameters and CLI; NiiVue PACS demo; no blanket SVA/TPA claim | OSTK / WEB | CURRENT | live | yes |
| `pacs-website-latency-root-cause` | PACS demo 40 s → 1.36 s (redirect, COEP vs CDN, input size) | WEB | DATED | live | yes |
| `panjabi-1991-page-892` | full Panjabi 1991 obtained; Table 3 in `level_references.csv` | REF | CURRENT | live | yes |
| `paper-split-2026-09-24` | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | SN | CURRENT | live | yes |
| `physics-three-defects-measured` | only the AEC defect changed an image; the display window hides the lateral spine | SN | CURRENT | live | yes |
| `polypose-decision` | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | SN | CURRENT | live | yes |
| `polypose-generator-build` | where the PolyPose generator lives; six traps | SN | CURRENT | live | yes |
| `pooled-vs-lodo-device-designs` | pooled and LODO both reported; list builder refuses split subjects | SN | CURRENT | live | yes |
| `postop-jaggedness-future` | future: fix post-op synthesis voxel roughness | OSTK | DATED | live | yes |
| `postop-spine-synthesis` | `ostk.surgery` synthetic post-op spines (labels only) | OSTK | DATED | live | yes |
| `prone-supine-flexibility-future` | 351 separate-mode pelvic acquisitions held out; flexibility idea | CTSP | DATED | live | yes |
| `publication-roadmap` | paper split plan and venues, with 2026-06/07/09 updates | PREF / strategy | PARTLY SUPERSEDED (later frames in flagship, rsnai, paper-split notes) | live | yes |
| `push-both-github-remotes` | CTSP: push origin and osc every time | PREF | CURRENT | live | yes |
| `recurrent-head-restored-2026-09-16` | BiGRU head was unreachable; restored, +10 points on the 27-class bank | SN | DATED | live | yes |
| `registration-free-prior-art` | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | REF | CURRENT | live | yes |
| `remedies-refuted-2026-09-17` | pretrain-on-DRR, film-noise, anchored-only, CReST admission all lose | SN | LEAKED numbers (the v2 scaling sweep, C2.1); refutations not re-run on v9 | live | yes |
| `resume-2026-09-21-pm` | entry point after 2026-09-21 for CT→fluoro formation | SN | HISTORY | history-only | no (history-only entry point) |
| `resume-2026-09-22-pm` | entry point 2026-09-23 02:15 | SN | HISTORY | history-only | no (history-only entry point) |
| `resume-2026-09-22` | entry point 2026-09-22 (k-devices chain, RSNAI plan) | SN | HISTORY | history-only | no (history-only entry point) |
| `resume-2026-09-24` | entry point 2026-09-24 (Figure 6 gate) | SN | HISTORY | history-only | no (history-only entry point) |
| `resume-2026-09-26-handoff` | handoff 2026-09-26: two top blocks (u251 RESUME.md; spinesurg RESUME_2026-09-22_PM.md) | SN / U251 | DATED (the spinesurg RESUME top block of 2026-09-27 is newer) | history-only | no (history-only entry point) |
| `review-space-repos` | exact HF repo ids for the review Spaces; the decoy repo | LAB | CURRENT | live | yes |
| `rib-approach-ts-trust` | future rib labelling: trust TS numbering, add Möller's bridge | CTSP | DATED | live | yes |
| `rib-auto-engulf-post-correction-only` | rib cleanup only after student correction | CTSP | CURRENT | live | yes |
| `rib-qc-gates-never-block-lstv` | only rib-purity checks gate rib reviews | CTSP | CURRENT | live | yes |
| `rigor-audit-findings` | selective reporting in two places, uninterval'd detector figure, one CI in 54 claims | SN | DATED | live | yes |
| `rsnai-author-instructions` | Radiology AI limits | REF / SN | CURRENT | live | yes |
| `rsnai-paper-endpoint` | one concise RSNA AI manuscript `paper/rsnai/main_v2.tex`; checklist `docs/RSNAI_PLAN.md` | SN | DATED (see schwingnet-manuscript, paper-split) | live | yes |
| `ruleclass-super-detector-run` | `/rs/.../ruleclass` census over 21,622 CTs; two arms; review tree | ANOM | CURRENT | live | yes |
| `s1-carve-changed-spinopelvic` | carved S1 (29) unreliable; gone in v11; retire checks on 29 | CTSP | CURRENT | live | yes |
| `scheme-bone-hardware-only` | scheme 0-68 with one hole at 29 from v11; 13 ribs per side | CTSP | CURRENT | live | yes |
| `schwingnet-disclosure-scrub` | SchwingNet private, CT side public; the clean-up state is Greg-only | PREF | CURRENT | live | GREG_ONLY/context/ (moved 2026-10-08) |
| `schwingnet-manuscript` | `SchwingNet/` manuscript built only from rigor-passing numbers; CLAIM map, ATLAS cards | SN | CURRENT | live | yes |
| `scratchpad-shadows-stdlib` | stdlib-named scratch scripts hijack Python | PREF | CURRENT | live | yes |
| `selective-prediction-the-honest-99` | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | SN | LEAKED (99 % at 35.7 % coverage on the leaked v2 bank; C1.8) | live | yes |
| `six-figure-paper-plan` | six figures; LevelCheck pre-specified, never tuned | SN | PARTLY SUPERSEDED (Figure 6 moved to paper 2) | live | yes |
| `spine-data-review-and-ts-bench` | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the scoping review | SN / DATA | DATED | live | yes |
| `spineps-ids-can-be-scrambled` | pre-147428d SPINEPS masks carry raw ids; guard `tools/spineps_ids.py`; VERIDAH not truth | DATA | CURRENT | live | yes |
| `split-leak-cross-naming` | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | DATA | CURRENT | live | yes |
| `splits-origin-and-v3-resplit (original file name carries the banned word)` | 5-fold splitter is patient-grouped + LSTV-stratified; v3 needs a resplit | DATA | DATED | live | yes |
| `spondylolysis-and-border-anomaly-findings` | LCC deletes the loose lamina; T-L and L-S variants co-occur | CTSP / ANOM | CURRENT | live | yes |
| `stc-does-not-transfer` | Star Temporal Classification loses to cross-entropy on naming | SN | CURRENT | live | yes |
| `student-onboarding-structure` | onboarding one-liner, Student_Projects layout, grid account and 2FA facts | LAB | CURRENT (local path wrong, section 13 row 1) | live | yes |
| `students-see-no-internals` | student tools offer one path | PREF / BTH | CURRENT | live | yes |
| `submit-and-sleep-orchestration` | submit, estimate, record, stop | PREF | CURRENT | live | yes |
| `sweep-map-replaces-registration` | overlapping frames build a radiograph-only registration; sweep_v3 numbers | SN | CURRENT | live | yes |
| `sweep-physics-no-bone` | physics-perturbed sweeps rendered with no bone; fix `--paths2-only` | SN | CURRENT | live | yes |
| `synthetic-real-ratio-evidence` | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | REF | CURRENT | live | yes |
| `tables-black-not-colour` | matrix tables black + one outlined mark | PREF | CURRENT | live | yes |
| `thoracic-gt-fov-limited` | v3 thoracic GT covers ~T8 down | CTSP | CURRENT | live | yes |
| `ts-bench-inside-v9-bank` | TS render bench is not held out from the v9 encoder | DATA / SN | CURRENT | live | yes |
| `ts-sacrum-excludes-s1` | TS `sacrum` excludes S1; whole sacrum = union | DATA | CURRENT | live | yes |
| `two-mechanisms-thesis` | morphology for quick limited-FOV localisation; sweep/count as the safety net | SN | SUPERSEDED numbers (98.2 % / 72.9 % / 44.9 % are v2-lineage; C1.18; current 97.4 %, A3.1); framing CURRENT | live | yes |
| `u251-cibersort-deconvolution` | CIBERSORT not installed; re-implementation fit weak | U251 | other project | live | no (U251, another project) |
| `u251-multiomics-sample-pairing` | GEO pairing lives in metadata; three pieces carry two names | U251 | other project | live | no (U251, another project) |
| `u251-name-sweep-traps` | N1/N2 are null hypotheses; result files SHA-256 anchored | U251 | other project | live | no (U251, another project) |
| `u251-project-containment` | U251 lives only in its own public repo and RESUME.md | U251 / PREF | CURRENT | live | no (U251, another project) |
| `u251-translation-fall-il68b` | "translation" fall = ribosomal-protein block leaning on IL68B | U251 | other project | live | no (U251, another project) |
| `user-affiliation-general-surgery` | General Surgery, not Neurosurgery | PREF | CURRENT | live | yes |
| `versefusion-t13-flag-wrong` | VerSeFusion `has_T13` says 18; truth 6 | DATA | CURRENT | live | yes |
| `vf813-drops-c1-t9-use-raw-verse-for-whole-spine` | `~/vf_813` maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | DATA | CURRENT | live | yes |
| `windows-junction-worktree-trap` | worktree remove deletes junction targets | PREF | CURRENT | live | yes |
| `windows-ssh-to-grid` | Windows ssh needs hmac-sha1 and IPv4; `wsu-grid` alias | GRID | CURRENT | live | yes |
| `writing-preferences` | the banned word; no fractional versions | PREF | CURRENT | live | yes |
| `wsl-for-network` | network commands via WSL | GRID / PREF | CURRENT | live | yes |
| `wsu-library-access-cutoff` | WSU Libraries dropped DMC residents 2026-06-30 | REF | CURRENT | live | yes |
| `xr-benchmark-and-robustness-2026-09-13` | X-ray level-ID competitor benchmark, physics tiers, recurrent head | SN | RECORD ONLY [WRONG-BANK] (C1.2) | live | yes |
| `xray-corner-detector-status` | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | SN | DATED | live | yes |
| `zenodo-deposit` | Zenodo token, DOIs, version recipe, build archive | CTSP / CRED | PARTLY SUPERSEDED (v11 = 10.5281/zenodo.22797014 on Zenodo per MANUSCRIPTS C1) | live | yes |


---

<!-- section: 4 Other context that lives only in the session -->

## 4. Other context that lives only in the session or outside the repositories

| item | where it lives now | why it matters | source |
|---|---|---|---|
| the memory notes themselves | the memory folder named above | copied here (§1) | — |
| Claude Docs | data report https://claude.ai/code/artifact/74a2ec52-90e4-4f20-82a5-5c8648668676; the Lab Recipe https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587; "handoff c3c7acfd..." and "literature state 3b03e849..." (full ids not recorded) | living documents | `context/data-platform-migration-2026-10.md`; `context/lab-recipe-and-board.md` |
| a web copy of the superseded feasibility manuscript | https://claude.ai/artifact/3DFZMHt4oAnrDVHwxdZnyf | history | `context/feasibility-claims-measured.md` |
| the NeurIPS camera-ready recomputation scripts | `<session scratchpad; not a dependency>/neurips_fixes/cr_apply/` (`crverify*.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py`) | Temp scratchpads can be swept; **copy them into `CTSpinoPelvic1K-1/CAMERA_READY_NEURIPS/`** | `MANUSCRIPTS.md` §7 |
| `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` | named in `CAMERA_READY_CHANGES.md`; found in no scratchpad | the exact wording for cutting Appendices I-J is lost | `working_notes/topic4_manuscripts.md` §7 |
| Beethoven design specs and spikes | session scratchpads (`v11/SPEC.md`, `v11/ssh/design/SSH_DESIGN.md`, `v12/iwa/REPORT.md`, `v12/iwa/STUDENT_STEPS.md`, `v12/iwa/app/dist/beethoven-iwa-0.2.0.swbn`, `rename-beethoven-global.js`) | `V11_CONTRACT.md` / `V12_STATUS.md` in the Beethoven repo carry part of it | `GREG_ONLY/context_beethoven/` notes |
| the annotator tally script | "`scratchpad/roster.py` pattern" | the only way to count who annotated | `GREG_ONLY/context/annotator-roster.md` (redacted copy in `context/`) |
| workflow journals | `...\subagents\workflows\wf_<id>\journal.jsonl` (for example wf_ded52e0e-cd1, the transitional review-tree build; wf_babed05b-84a, the anomaly harvest) | resume state of background workflows; a new session can read them, not resume them | `spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` |
| the resume file | `spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` (newest block on top, 2026-09-27 18:05; "FOR GREG" decisions at L35-37) | the last session checkpoint of the spine work | — |
| the grid jobs record | `spinesurg-ct-nnunet/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | every job cancelled on 2026-09-27 with how to resume it | — |
| GitHub purge drafts and the TTO package | `Desktop/private_ip/github_purge_requests/`, `Desktop/private_ip/TTO_package_2026-09-25/` (laptop only) | pending filings (Greg) | `GREG_ONLY/context/schwingnet-disclosure-scrub.md` |
| this handoff's working notes | `HANDOFF/working_notes/` (copied from the session scratchpad on 2026-10-08) | the full tables behind every file here | — |
| this handoff's builder scripts | `HANDOFF/working_notes/builders/` (`copy_context.py`, `build_context_export.py`, `check_paths.py`, `check_refs.py` copied from the scratchpad on 2026-10-08; `refresh_context.py`, `build_context_index.py`, `patch_helper.py` written in the verification pass) | the scratchpad copies can be swept | — |


---

<!-- section: 5 Memory hygiene a fresh project inherits -->

## 5. Memory hygiene a fresh project inherits

`fluorocap-pipeline-resume.md` is not in the `MEMORY.md` index; `ashley-extension-project` and `ashley-bridge-project` are
each linked twice in the index; broken wikilinks: `grid-access` -> `no-login-node-jobs` (the file is
`no-jobs-on-login-node`), `never-reorient-when-writing-labels` -> `ct-spinopelvic-release-gates` (no such note),
`postop-jaggedness-future` -> `postop-spine-synthesis.md` (an extra `.md`); the two "START HERE" bullets at the top of
`MEMORY.md` point at states of 2026-09-28 and 2026-09-26, while newer state lives in
`spinesurg-ct-nnunet/docs/RESUME_2026-09-22_PM.md` (2026-09-27), `context/data-platform-migration-2026-10.md` (2026-10-08)
and the Beethoven repo log (2026-10-03); `lab-recipe-and-board.md` and `student-onboarding-structure.md` put Student_Projects
at `Desktop/Student_Projects` (it is `CTSpinoPelvic1K-1/Student_Projects`) and count 11 unstaffed cards (10)
(`working_notes/topic5_operating_here.md` §13-14).

