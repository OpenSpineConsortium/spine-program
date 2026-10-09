<!-- spine-program/08_render_devices: copy of spinesurg-ct-nnunet 097933a HANDOFF/context/INDEX.md (copied 2026-10-08; redactions, if any, are listed in MANIFEST_LOCAL.md section 3). Laptop spellings of the path prefixes (`C:/` drive paths, the session scratchpad, the memory folder) are history, not dependencies: read them through this folder's CLAUDE.md "Prefixes in the copied documents". -->

# Context index (load this, not MEMORY.md)

Built 2026-10-08 by `working_notes/builders/build_context_index.py` from the notes present in this folder and
the digest of `CONTEXT_EXPORT.md` §3, with the statuses corrected by the 2026-10-08 verification. Each note is a
dated record from the session that did the work, not an instruction: where a note and a result file or
`RESULTS_CATALOG.md` disagree, the file and the catalog win. LEAKED = its numbers were measured on a bank with
a known leak; SUPERSEDED = replaced by the number named; RECORD ONLY = history, not quotable; DATED = a state at
its date. The copy time of every note is in `COPIED_AT.txt`.

**Not in this folder** (Greg and the Claude project only, `GREG_ONLY/`): the original `MEMORY.md` index (kept
there as an archive; its links to U251, history-only and Beethoven notes do not resolve), the commercial-stance
note, the disclosure-scrub note, the three credential-location notes, the full copies of the three redacted
notes (`GREG_ONLY/context/`) and the six Beethoven product notes (`GREG_ONLY/context_beethoven/`). Not copied at
all: the seven U251 / LITT notes (another project) and the six history-only entry points.

| note | one line | project | status | what replaces it, or why |
|---|---|---|---|---|
| [`acquisition-space-saturation`](acquisition-space-saturation.md) | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); claim wording | SN | CURRENT |  |
| [`annotator-roster`](annotator-roster.md) | who annotated what, from `slots[].reviewer` in private ledgers; 13 students by 2026-08-23 | LAB | DATED; redacted copy | per-person usernames and counts withheld here (full note in `GREG_ONLY/context/`) |
| [`anomaly-harvest-directive`](anomaly-harvest-directive.md) | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in FOV | ANOM | CURRENT |  |
| [`anomaly-manifest-sources`](anomaly-manifest-sources.md) | 749 anomalous spines in 3 tiers; master table `lstv_flag_labels_v2.csv`; why the count was once 34/16/2 | ANOM | DATED |  |
| [`anomaly-rule-rc22-evaluated`](anomaly-rule-rc22-evaluated.md) | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | ANOM | CURRENT |  |
| [`bash-heredoc-backslashes`](bash-heredoc-backslashes.md) | heredocs collapse backslashes; write scripts with Write, run by path | PREF | CURRENT |  |
| [`canonical-rib-triage`](canonical-rib-triage.md) | rib review set defined by `qc_v4_ribs_and_verts.py`; worklist regenerated from it | CTSP | DATED |  |
| [`carm-plateau-is-the-denominator`](carm-plateau-is-the-denominator.md) | same-device 82-85 % plateau is the truth denominator; clean subset 96.9 % | SN | CURRENT |  |
| [`carmlspine-level-experiment`](carmlspine-level-experiment.md) | C-ArmLSpine (148 cases, AP+LAT+CBCT): reading traps, pose convention, pipeline | SN | CURRENT |  |
| [`chart-preferences`](chart-preferences.md) | slides: no sideways bars, donuts/lines, published background figures, big type | PREF | CURRENT |  |
| [`cloudflare-tls-fingerprint`](cloudflare-tls-fingerprint.md) | 403 everywhere = TLS fingerprint block; `curl_cffi impersonate="chrome"` | REF | CURRENT |  |
| [`cns-deck-v2-2026-09-25`](cns-deck-v2-2026-09-25.md) | CNS spine deck: v10 discloses Part B; public CT-side cut on the Desktop; generators and template traps | DECK / SN | DATED |  |
| [`commit-directly-to-master`](commit-directly-to-master.md) | CTSP repo: commit to master, no branches | PREF | CURRENT |  |
| [`competitor-benchmark`](competitor-benchmark.md) | TS, SPINEPS/VERIDAH + Möller ribs, VISTA3D, RibSeg in the one-shot space; grid layout | SN / CTSP | DATED |  |
| [`context-ladder-2d-level-experiment`](context-ladder-2d-level-experiment.md) | how much spine must be visible to name a vertebra; BUU levels are counting-inferred | SN | DATED |  |
| [`ct-benchmark-covers-all-collections`](ct-benchmark-covers-all-collections.md) | the CT axis is every collection (5,700+ subjects); `tools/ct_inventory.py` | DATA | CURRENT |  |
| [`ct-volumes-are-pir-not-ras`](ct-volumes-are-pir-not-ras.md) | volumes are (P,I,R) on disk; decide by reading the affine | CTSP | CURRENT |  |
| [`ctspine1k-selection-code-deleted`](ctspine1k-selection-code-deleted.md) | CTSpine1K's supine/prone selector does not select; recover at 7f44959 | REF | CURRENT |  |
| [`data-audit-99-gaps`](data-audit-99-gaps.md) | 99 gaps in `docs/DATA_COMPLETENESS_AUDIT.md`; the ones that change the science | DATA | DATED |  |
| [`data-directives-2026-09-23`](data-directives-2026-09-23.md) | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | PREF / DATA | CURRENT |  |
| [`data-platform-migration-2026-10`](data-platform-migration-2026-10.md) | data_platform: manifest, layout, batches B00-B14, census, state 2026-10-08, visibility | DATA / GRID | CURRENT (copied 16:33, after its 13:34 and 16:20 rewrites) | batch state, dedup hash verdicts, and the TCIA CT Colonography raw trees found on neither HOME nor Ceph (`OPEN_QUESTIONS.md` B30) |
| [`dataset813-image-links-are-container-paths`](dataset813-image-links-are-container-paths.md) | Dataset813 imagesTr links resolve only in the container; never repair; `HF_EXPORT_DIR` | GRID | CURRENT |  |
| [`deepfluoro-convention`](deepfluoro-convention.md) | DeepFluoro file layout and projection convention (0.00 px reprojection) | REF / SN | CURRENT |  |
| [`detection-is-the-binding-constraint`](detection-is-the-binding-constraint.md) | counting fails on detection (60 points) not linking (11-28) | SN | CURRENT |  |
| [`device-sampling-audit`](device-sampling-audit.md) | card clip saturates (95-98 % of the joint lost); typicality gate | SN | CURRENT |  |
| [`diagnostics-graph-required`](diagnostics-graph-required.md) | every Beethoven feature needs diagnostics-graph nodes first | PREF / BTH | CURRENT |  |
| [`drr-row-spacing-defect`](drr-row-spacing-defect.md) | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | SN | CURRENT |  |
| [`drr-to-fluoro-levers`](drr-to-fluoro-levers.md) | three measured levers for DRR→fluoro; CycleGAN/ADDA refuted; honest ceiling | REF / SN | CURRENT |  |
| [`engine-swap-architecture`](engine-swap-architecture.md) | demo consumes a `metrics.json` contract so the engine can be swapped | WEB | DATED |  |
| [`feasibility-claims-measured`](feasibility-claims-measured.md) | the FOV feasibility report tested claim by claim; head/encoder pairing trap | SN | RECORD ONLY [LEAK] | its accuracies are on v2 / v5 / v6 (C1.14, C1.16); its claim-by-claim reading of the external report still stands |
| [`figure-captions-terse`](figure-captions-terse.md) | captions short, argument in text; float spacing | PREF | CURRENT |  |
| [`figure-preferences-schwingnet`](figure-preferences-schwingnet.md) | Greg's figure verdicts for the SchwingNet manuscript (2026-09-22) | PREF / SN | PARTLY SUPERSEDED (five-figure paper 1, mem:paper-split-2026-09-24.md) |  |
| [`film-fluoro-boundary-not-transferable`](film-fluoro-boundary-not-transferable.md) | devices separate pairwise; film vs fluoro does not transfer to an unseen corpus | SN | CURRENT |  |
| [`film-ncurve-ablation-result`](film-ncurve-ablation-result.md) | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | SN | SUPERSEDED reading | "all help" is outdated: the tool's `sn:results/coverage/film_ncurve/ablation/READ.md` shows 7 of 9 cells separated, six help and one hurts (BUU at every person) (A10.6-A10.9); its "from 100 persons the arms overlap" holds at 100 and 200 persons, not at every person (A10.10) |
| [`flagship-paper-frame`](flagship-paper-frame.md) | "ships a network"; claims ledger; `\PENDING` macros | SN | PARTLY SUPERSEDED (LevelCheck comparison moved to paper 2) |  |
| [`flagship-program`](flagship-program.md) | gates G0-G7 in `docs/FLAGSHIP_PLAN.md` | SN | DATED |  |
| [`fluoro-panel-gap-diagnosed`](fluoro-panel-gap-diagnosed.md) | literature panels 19.7 % vs 95.1 % on radiographs: domain plus contamination | FC / SN | DORMANT |  |
| [`fluorocap-dataset`](fluorocap-dataset.md) | FluoroCap test set on grid `~/FluoroCap`: stages, routes, manifest | FC | DORMANT |  |
| [`fluorocap-is-reproductions-not-fluoroscopy`](fluorocap-is-reproductions-not-fluoroscopy.md) | 72.8 % of panels have zero pixel residual; test set only | FC | CURRENT (the reason FC is out of training) |  |
| [`fluorocap-pipeline-resume`](fluorocap-pipeline-resume.md) | start at `docs/PIPELINE_RESUME.md` and `tools/pipeline_state.py`; add every stage there (not in MEMORY.md index) | SN | CURRENT |  |
| [`fluorocap-prototype-and-lstv-arm`](fluorocap-prototype-and-lstv-arm.md) | single-image prototype, transitional harvest arm, Semantic Scholar route | FC | DORMANT |  |
| [`fluorocap-repo-private`](fluorocap-repo-private.md) | spinesurg private since 2026-09-14; never push level-ID code public | PREF | CURRENT |  |
| [`fluorogen-synthetic`](fluorogen-synthetic.md) | SDXL + ControlNet + LoRA synthetic C-arm frames; gmsap = 4 x 4 H200 | SN | DATED |  |
| [`grid-access`](grid-access.md) | login, project root, where CTs and labels lived, ITK-SNAP launch | GRID | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) |  |
| [`grid-access-list-gate`](grid-access-list-gate.md) | approved students = named ACL entries on `/rs/rs_grp_oschome` | GRID / BTH | CURRENT |  |
| [`grid-apptainer-module-works`](grid-apptainer-module-works.md) | `module load apptainer/1.2.2` sandbox builds; secp starts at once | GRID | CURRENT |  |
| [`grid-ashley-deletion-2026-09-28`](grid-ashley-deletion-2026-09-28.md) | `~/.ashley` wiped during a phone session; destructive commands refuse under CLAUDECODE | GRID / BTH | CURRENT |  |
| [`grid-bash-4-2-quoting`](grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail | GRID | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; write grid jobs for bash 4.2 |
| [`grid-ceph-volume-oschome`](grid-ceph-volume-oschome.md) | 20 TB Ceph volume, working tree, `df-ceph oschome` | GRID | CURRENT |  |
| [`grid-ct-0533-truncated`](grid-ct-0533-truncated.md) | CT 0533 truncation repaired on the grid and HF | CTSP | CURRENT (done) |  |
| [`grid-local-singularity-is-broken`](grid-local-singularity-is-broken.md) | use conda singularity + pre-unpacked sandbox + specific bind | GRID | CURRENT |  |
| [`grid-quota-and-deleted-banks`](grid-quota-and-deleted-banks.md) | `pan_quota`; banks deleted 2026-09-20; `holdout.py` raises; refs → v7 | GRID | CURRENT |  |
| [`grid-slurm-inside-apptainer`](grid-slurm-inside-apptainer.md) | binds that make sbatch work inside a container | GRID | CURRENT |  |
| [`grid-ssh-second-factor`](grid-ssh-second-factor.md) | ssh off-VPN with password + TOTP; warrior bans python, rsync and others | GRID | CURRENT |  |
| [`guided-acquisition-loop`](guided-acquisition-loop.md) | commanded displacement + digital fiducial; what must not be quoted | SN | DATED |  |
| [`hf-identity`](hf-identity.md) | HF username `gregoryschwingmdphd` | CRED | CURRENT |  |
| [`hf-mirror-is-v10`](hf-mirror-is-v10.md) | public HF/Zenodo is v10 with id 29; v11 local only; lines to change when it ships | CTSP | PARTLY SUPERSEDED | the Hugging Face mirror was still v10 on 2026-09-27 (checked by API), but the note's statement that Zenodo is v10 is contradicted by four documents giving v11 on Zenodo (`MANUSCRIPTS.md` §20 C1) |
| [`identity-audit-findings`](identity-audit-findings.md) | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case ≠ person | DATA | CURRENT |  |
| [`journal-figure-and-style-rules`](journal-figure-and-style-rules.md) | Medical Physics figure and text rules; page estimate | PREF / CTSP | CURRENT |  |
| [`k-devices-one-network`](k-devices-one-network.md) | per-device parameter sets, styled renders, LODO; where the pipeline lives | SN | CURRENT |  |
| [`key-patients-from-metadata-not-filenames`](key-patients-from-metadata-not-filenames.md) | identity order: DICOM → manifest → ann fields → filename last | PREF / DATA | CURRENT |  |
| [`l6-sample-count-and-counting-decoder`](l6-sample-count-and-counting-decoder.md) | L6 dice 0.000 = too few cases; counting decoder; Dataset815 | SN / CTSP | DATED |  |
| [`lab-recipe-and-board`](lab-recipe-and-board.md) | RECIPE.md, board.json → BOARD.md, Claude Doc; local commit not pushed | LAB | CURRENT (location and count errors, section 13 rows 1-2) |  |
| [`label-scheme-v4-vs-ostk`](label-scheme-v4-vs-ostk.md) | two live maps; `labels_for(volume)`; what the mix-up cost | CTSP / OSTK | CURRENT |  |
| [`learned-formation-refuted-calibrate-instead`](learned-formation-refuted-calibrate-instead.md) | CT→fluoro formation calibrated on DeepFluoro; first real-fluoro recall | SN | CURRENT; redacted copy | one staff contact withheld here (full note in `GREG_ONLY/context/`) |
| [`level-id-2d-results-2026-09-13`](level-id-2d-results-2026-09-13.md) | 2-D level ID on real films, 13 Sep results | SN | RECORD ONLY | the 96.7 % single-crop number is on the cervical-dominated `films_ann` bank (C1.1) |
| [`level-model-bank-coverage`](level-model-bank-coverage.md) | the deployed bank held only cervical and lumbar films | SN | DATED |  |
| [`level-service-serving`](level-service-serving.md) | website never serves weights; service + private HF weights | PREF / WEB | CURRENT |  |
| [`local-level-identity-thesis`](local-level-identity-thesis.md) | name a vertebra by local morphology instead of counting from C2 | SN / CTSP | CURRENT |  |
| [`lstv-data-landscape`](lstv-data-landscape.md) | where LSTV/TLTV labels exist; the one published 2-D LSTV model | REF | DATED; redacted copy | three researcher e-mail addresses withheld here (full note in `GREG_ONLY/context/`) |
| [`lstv-oneshot-training-run`](lstv-oneshot-training-run.md) | Dataset810 one-shot LSTV run for the CNS slides | ANOM / CTSP | DATED |  |
| [`lstv-reread-queue`](lstv-reread-queue.md) | log doubtful source LSTV labels in `docs/lstv_reread_queue.csv` | CTSP | CURRENT |  |
| [`lstv-tltv-detection-goal`](lstv-tltv-detection-goal.md) | standing determination: detect LSTV/TLTV from C-arm exposures | SN | CURRENT |  |
| [`mixed-length-head-and-sota`](mixed-length-head-and-sota.md) | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | SN | LEAKED | its numbers (97.47 % at 3 vertebrae, the "shortcut-free" 99.02 %) are on allspine v2, which pooled NHANES II twice (`RESULTS_CATALOG.md` C1.6); do not follow its "quote 99.02 %". Held-out film naming today: the film N-curve at every person, CSXA 99.8 %, BUU 96.9 %, NHANES 92.7 % (A10.1-A10.3) |
| [`model-registry`](model-registry.md) | content-addressed weights store, ledger, MLflow, HF mirror | GRID / SN | CURRENT |  |
| [`morphology-deformation-feasibility`](morphology-deformation-feasibility.md) | literature first; no bespoke CT warp | PREF | CURRENT |  |
| [`never-reorient-when-writing-labels`](never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label | CTSP | CURRENT |  |
| [`nhanes-double-inclusion`](nhanes-double-inclusion.md) | NHANES in the banks twice, split independently | DATA | CURRENT (fixed by patient keys) |  |
| [`nninteractive-colab-versions`](nninteractive-colab-versions.md) | ITK-SNAP DLS (nnInteractive) Colab pins | REF | DATED |  |
| [`no-jobs-on-login-node`](no-jobs-on-login-node.md) | every computation via sbatch; compute nodes have internet; C&IT addendum | GRID / PREF | CURRENT |  |
| [`no-unexplained-subsets-fix-not-disclose`](no-unexplained-subsets-fix-not-disclose.md) | use all of a dataset; describe each in prose; fix leaks, don't disclose | PREF | CURRENT |  |
| [`oblique-angles-and-sweep-vision`](oblique-angles-and-sweep-vision.md) | detector must work at any angle; synthetic AP→lateral arcs; AR vision is preview only | SN | CURRENT |  |
| [`ostk-canal-closing-regression`](ostk-canal-closing-regression.md) | ostk 1b7005c inflates VBHp/EPD 10-17 mm on ~1 in 7 vertebrae | OSTK | CURRENT (open) |  |
| [`pacs-demo-and-ostk-params`](pacs-demo-and-ostk-params.md) | ostk parameters and CLI; NiiVue PACS demo; no blanket SVA/TPA claim | OSTK / WEB | CURRENT |  |
| [`pacs-website-latency-root-cause`](pacs-website-latency-root-cause.md) | PACS demo 40 s → 1.36 s (redirect, COEP vs CDN, input size) | WEB | DATED |  |
| [`panjabi-1991-page-892`](panjabi-1991-page-892.md) | full Panjabi 1991 obtained; Table 3 in `level_references.csv` | REF | CURRENT |  |
| [`paper-split-2026-09-24`](paper-split-2026-09-24.md) | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | SN | CURRENT |  |
| [`physics-three-defects-measured`](physics-three-defects-measured.md) | only the AEC defect changed an image; the display window hides the lateral spine | SN | CURRENT |  |
| [`polypose-decision`](polypose-decision.md) | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | SN | CURRENT |  |
| [`polypose-generator-build`](polypose-generator-build.md) | where the PolyPose generator lives; six traps | SN | CURRENT |  |
| [`pooled-vs-lodo-device-designs`](pooled-vs-lodo-device-designs.md) | pooled and LODO both reported; list builder refuses split subjects | SN | CURRENT |  |
| [`postop-jaggedness-future`](postop-jaggedness-future.md) | future: fix post-op synthesis voxel roughness | OSTK | DATED |  |
| [`postop-spine-synthesis`](postop-spine-synthesis.md) | `ostk.surgery` synthetic post-op spines (labels only) | OSTK | DATED |  |
| [`prone-supine-flexibility-future`](prone-supine-flexibility-future.md) | 351 separate-mode pelvic acquisitions held out; flexibility idea | CTSP | DATED |  |
| [`publication-roadmap`](publication-roadmap.md) | paper split plan and venues, with 2026-06/07/09 updates | PREF / strategy | PARTLY SUPERSEDED (later frames in flagship, rsnai, paper-split notes) |  |
| [`push-both-github-remotes`](push-both-github-remotes.md) | CTSP: push origin and osc every time | PREF | CURRENT |  |
| [`recurrent-head-restored-2026-09-16`](recurrent-head-restored-2026-09-16.md) | BiGRU head was unreachable; restored, +10 points on the 27-class bank | SN | DATED | the head's 99 % was on a cervical-dominated bank (`CONTEXT_EXPORT.md` §3) |
| [`registration-free-prior-art`](registration-free-prior-art.md) | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | REF | CURRENT |  |
| [`remedies-refuted-2026-09-17`](remedies-refuted-2026-09-17.md) | pretrain-on-DRR, film-noise, anchored-only, CReST admission all lose | SN | LEAKED numbers | the scaling curve it quotes is the v2 sweep (C2.1, SUPERSEDED [LEAK] [SEL-SPLIT]); the refutations were not re-run on v9 |
| [`review-space-repos`](review-space-repos.md) | exact HF repo ids for the review Spaces; the decoy repo | LAB | CURRENT |  |
| [`rib-approach-ts-trust`](rib-approach-ts-trust.md) | future rib labelling: trust TS numbering, add Möller's bridge | CTSP | DATED |  |
| [`rib-auto-engulf-post-correction-only`](rib-auto-engulf-post-correction-only.md) | rib cleanup only after student correction | CTSP | CURRENT |  |
| [`rib-qc-gates-never-block-lstv`](rib-qc-gates-never-block-lstv.md) | only rib-purity checks gate rib reviews | CTSP | CURRENT |  |
| [`rigor-audit-findings`](rigor-audit-findings.md) | selective reporting in two places, uninterval'd detector figure, one CI in 54 claims | SN | DATED |  |
| [`rsnai-author-instructions`](rsnai-author-instructions.md) | Radiology AI limits | REF / SN | CURRENT |  |
| [`rsnai-paper-endpoint`](rsnai-paper-endpoint.md) | one concise RSNA AI manuscript `paper/rsnai/main_v2.tex`; checklist `docs/RSNAI_PLAN.md` | SN | DATED (see schwingnet-manuscript, paper-split) |  |
| [`ruleclass-super-detector-run`](ruleclass-super-detector-run.md) | `/rs/.../ruleclass` census over 21,622 CTs; two arms; review tree | ANOM | CURRENT |  |
| [`s1-carve-changed-spinopelvic`](s1-carve-changed-spinopelvic.md) | carved S1 (29) unreliable; gone in v11; retire checks on 29 | CTSP | CURRENT |  |
| [`scheme-bone-hardware-only`](scheme-bone-hardware-only.md) | scheme 0-68 with one hole at 29 from v11; 13 ribs per side | CTSP | CURRENT |  |
| [`schwingnet-manuscript`](schwingnet-manuscript.md) | `SchwingNet/` manuscript built only from rigor-passing numbers; CLAIM map, ATLAS cards | SN | CURRENT |  |
| [`scratchpad-shadows-stdlib`](scratchpad-shadows-stdlib.md) | stdlib-named scratch scripts hijack Python | PREF | CURRENT |  |
| [`selective-prediction-the-honest-99`](selective-prediction-the-honest-99.md) | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | SN | LEAKED | the 99 % at 35.7 % / 55.7 % coverage is on the leaked v2 bank, computed on its own test half (C1.8; `LEAKAGE.md` §5.1); no clean re-run exists (`OPEN_QUESTIONS.md` C13). Its arithmetic (about 298 answered cases to certify 99 %) still holds (E.9) |
| [`six-figure-paper-plan`](six-figure-paper-plan.md) | six figures; LevelCheck pre-specified, never tuned | SN | PARTLY SUPERSEDED (Figure 6 moved to paper 2) |  |
| [`spine-data-review-and-ts-bench`](spine-data-review-and-ts-bench.md) | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the scoping review | SN / DATA | DATED |  |
| [`spineps-ids-can-be-scrambled`](spineps-ids-can-be-scrambled.md) | pre-147428d SPINEPS masks carry raw ids; guard `tools/spineps_ids.py`; VERIDAH not truth | DATA | CURRENT |  |
| [`split-leak-cross-naming`](split-leak-cross-naming.md) | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | DATA | CURRENT |  |
| [`splits-origin-and-v3-resplit`](splits-origin-and-v3-resplit.md) | 5-fold splitter is patient-grouped + LSTV-stratified; v3 needs a resplit | DATA | DATED |  |
| [`spondylolysis-and-border-anomaly-findings`](spondylolysis-and-border-anomaly-findings.md) | LCC deletes the loose lamina; T-L and L-S variants co-occur | CTSP / ANOM | CURRENT |  |
| [`stc-does-not-transfer`](stc-does-not-transfer.md) | Star Temporal Classification loses to cross-entropy on naming | SN | CURRENT |  |
| [`student-onboarding-structure`](student-onboarding-structure.md) | onboarding one-liner, Student_Projects layout, grid account and 2FA facts | LAB | CURRENT (local path wrong, section 13 row 1) |  |
| [`students-see-no-internals`](students-see-no-internals.md) | student tools offer one path | PREF / BTH | CURRENT |  |
| [`submit-and-sleep-orchestration`](submit-and-sleep-orchestration.md) | submit, estimate, record, stop | PREF | CURRENT |  |
| [`sweep-map-replaces-registration`](sweep-map-replaces-registration.md) | overlapping frames build a radiograph-only registration; sweep_v3 numbers | SN | CURRENT |  |
| [`sweep-physics-no-bone`](sweep-physics-no-bone.md) | physics-perturbed sweeps rendered with no bone; fix `--paths2-only` | SN | CURRENT |  |
| [`synthetic-real-ratio-evidence`](synthetic-real-ratio-evidence.md) | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | REF | CURRENT |  |
| [`tables-black-not-colour`](tables-black-not-colour.md) | matrix tables black + one outlined mark | PREF | CURRENT |  |
| [`thoracic-gt-fov-limited`](thoracic-gt-fov-limited.md) | v3 thoracic GT covers ~T8 down | CTSP | CURRENT |  |
| [`ts-bench-inside-v9-bank`](ts-bench-inside-v9-bank.md) | TS render bench is not held out from the v9 encoder | DATA / SN | CURRENT |  |
| [`ts-sacrum-excludes-s1`](ts-sacrum-excludes-s1.md) | TS `sacrum` excludes S1; whole sacrum = union | DATA | CURRENT |  |
| [`two-mechanisms-thesis`](two-mechanisms-thesis.md) | morphology for quick limited-FOV localisation; sweep/count as the safety net | SN | SUPERSEDED numbers | 98.2 % whole frame, 72.9 % one body and 44.9 % L6 are the v2-lineage run (C1.18, A3.11). Current: 601 / 617 = 97.4 % whole lateral frame (A3.1), 451 / 603 = 74.8 % one body in field (A3.3). The framing (morphology for limited fields, counting as the safety net) still governs paper 1 |
| [`user-affiliation-general-surgery`](user-affiliation-general-surgery.md) | General Surgery, not Neurosurgery | PREF | CURRENT |  |
| [`versefusion-t13-flag-wrong`](versefusion-t13-flag-wrong.md) | VerSeFusion `has_T13` says 18; truth 6 | DATA | CURRENT |  |
| [`vf813-drops-c1-t9-use-raw-verse-for-whole-spine`](vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md) | `~/vf_813` maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | DATA | CURRENT |  |
| [`windows-junction-worktree-trap`](windows-junction-worktree-trap.md) | worktree remove deletes junction targets | PREF | CURRENT |  |
| [`windows-ssh-to-grid`](windows-ssh-to-grid.md) | Windows ssh needs hmac-sha1 and IPv4; `wsu-grid` alias | GRID | CURRENT |  |
| [`writing-preferences`](writing-preferences.md) | the banned word; no fractional versions | PREF | CURRENT |  |
| [`wsl-for-network`](wsl-for-network.md) | network commands via WSL | GRID / PREF | CURRENT |  |
| [`wsu-library-access-cutoff`](wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30 | REF | CURRENT |  |
| [`xr-benchmark-and-robustness-2026-09-13`](xr-benchmark-and-robustness-2026-09-13.md) | X-ray level-ID competitor benchmark, physics tiers, recurrent head | SN | RECORD ONLY [WRONG-BANK] | the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; `OPEN_QUESTIONS.md` F5) |
| [`xray-corner-detector-status`](xray-corner-detector-status.md) | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | SN | DATED |  |
| [`zenodo-deposit`](zenodo-deposit.md) | Zenodo token, DOIs, version recipe, build archive | CTSP / CRED | PARTLY SUPERSEDED | says v10 is current on Zenodo; four documents give v11 = 10.5281/zenodo.22797014, published 18 Sep 2026 (`MANUSCRIPTS.md` §20 C1). Live state not re-checked (`OPEN_QUESTIONS.md` E7) |

141 notes.
