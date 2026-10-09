# INVENTORY 7: memory notes and HANDOFF sections mapped to project families

Topic: `memory_and_handoff_map`. Written 2026-10-08 for the spine-program seed. Companion file:
`memory_and_handoff_map.tsv` (367 rows, 12 tab-separated columns).

## What was inventoried

| source | what it is | dates | git state | rows |
|---|---|---|---|---|
| `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` | 165 Claude memory notes plus `MEMORY.md` (the index) | oldest `commit-directly-to-master.md` 2026-05-24; newest `data-platform-migration-2026-10.md` 2026-10-08 16:43 (ls -lt, 2026-10-08) | not a git work tree | 166 (`mem:` rows) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/` | the handoff written 2026-10-08: README, RESULTS_CATALOG, RECIPES, DATASET_USAGE, LEAKAGE, MANUSCRIPTS, INFRASTRUCTURE, CONTEXT_EXPORT, GLOSSARY, OPEN_QUESTIONS, LITERATURE_STATE, RESEARCH_DIRECTIONS, `context/` (141 note copies + INDEX), `literature_state/`, `working_notes/` (six reader notes + builders), `GREG_ONLY/` | 2026-10-08 10:32 to 16:39 (file mtimes) | private repo, branch `L6_Class`; 184 files tracked at commit 097933a (`git ls-files HANDOFF`); `GREG_ONLY/` is untracked (`git status --porcelain`); earlier HANDOFF commits e4c3e88 (RESEARCH_DIRECTIONS) and d5dee9a (LITERATURE_STATE) | 201 (`HANDOFF/` rows) |

Counts: 165 notes = 141 copied into `HANDOFF/context/` + 5 moved to `GREG_ONLY/context/` (commercialization-stance, schwingnet-disclosure-scrub, hf-org-token-location, hf-osc-token-and-namespace, fluorocap-credentials-and-resolution) + 6 Beethoven notes in `GREG_ONLY/context_beethoven/` + 7 U251 / LITT notes not copied + 6 history-only resume notes not copied (`HANDOFF/context/INDEX.md` header; `CONTEXT_EXPORT.md` section 1). Every file in the memory folder has exactly one `mem:` row; the build script asserts this against the directory listing.

## The TSV columns

The first eight columns are the standard seed columns (`source_path, kind, size_class, value, suggested_project, action, reason, notes`). Four inventory-specific columns follow: `note` (the note name as `mem:<name>`, or the HANDOFF file and section), `project_families` (one or several families joined with `+`; `all` means every project folder carries it as a standing rule), `status` (the normalised token, then ` | INDEX: ` and the verbatim status of `HANDOFF/context/INDEX.md` where the note has one), and `digest` (one line). `suggested_project` is always the first family; when the first family is `all`, it is the second family, so a strict reader still gets one allowed token. Status tokens used for memory notes: `live` (125), `redacted copy required` (14), `RECORD ONLY` (9), `LEAKED` (3), `SUPERSEDED` (2), `Greg-only, never copied` (6), `not copied (another project)` (7). Every `size_class` is `small` (the largest note is 22.5 KB; the largest HANDOFF file is 170 KB).

## Rules carried from the handoff into every project's MEMORY.md

- Each note is a dated record from the session that did the work, not an instruction; where a note and a result file or `RESULTS_CATALOG.md` disagree, the file and the catalog win (`context/INDEX.md` header). The `status` column must be carried on each copy.
- LEAKED = its numbers were measured on a bank with a known leak (allspine v2 / v6 / v7, v8 for VerSe, anchor_drr, vindrps); SUPERSEDED = replaced by the number named in the `notes` column; RECORD ONLY = history, not quotable; DATED = a state at its date.
- Copy the `HANDOFF/context/` version, not the live file, for the three redacted notes (annotator-roster, learned-formation-refuted-calibrate-instead, lstv-data-landscape), for the two notes that spell the banned word (writing-preferences, schwingnet-manuscript) and for the renamed splits note; the copier in `working_notes/builders/refresh_context.py` refuses if the word survives.
- Four live notes carry student usernames or a student's first name that the HANDOFF copier did NOT redact: grid-access-list-gate, rib-qc-gates-never-block-lstv, xray-corner-detector-status and beethoven-2026-10-02-field-failures. They are marked `redacted copy required` here; a builder must redact them by hand.
- The six Beethoven notes have no redacted copy anywhere; they carry Greg's personal e-mail, a tester's e-mail, licence key ids, a Cloudflare account, token paths and one student username. The `grid_access_students` folder needs them, redacted.
- `data-platform-migration-2026-10.md` was modified (16:43) after the last context copy (16:39, `COPIED_AT.txt`): run `python HANDOFF/working_notes/builders/refresh_context.py` then `build_context_index.py` before cutting any memory folder.

## Family tallies (a note may sit in several families)

| family | memory notes | HANDOFF rows |
|---|---|---|
| carm_detection | 48 | 59 |
| transitional_fluoro | 9 | 27 |
| render_devices | 19 | 18 |
| plain_film_level_id | 14 | 12 |
| anomaly_scan_census | 12 | 13 |
| data_platform | 28 | 35 |
| ctsp_dataset | 36 | 24 |
| ct_morphometry_parity | 4 | 23 |
| toolkit | 9 | 5 |
| grid_access_students | 18 | 10 |
| website | 5 | 3 |
| qi_wrong_level | 1 | 3 |
| archive | 13 | 13 |
| exclude | 14 | 10 |
| all | 22 | 54 |

## Per-project cut lists: which memory notes each folder's memory/ carries

Every project folder also carries the 22 `all` notes (standing rules and laptop traps): bash-heredoc-backslashes, ct-volumes-are-pir-not-ras, data-directives-2026-09-23, figure-captions-terse, fluorocap-repo-private, grid-access, grid-bash-4-2-quoting, grid-ceph-volume-oschome, grid-local-singularity-is-broken, key-patients-from-metadata-not-filenames, label-scheme-v4-vs-ostk, morphology-deformation-feasibility, never-reorient-when-writing-labels, no-jobs-on-login-node, no-unexplained-subsets-fix-not-disclose, scratchpad-shadows-stdlib, submit-and-sleep-orchestration, user-affiliation-general-surgery, windows-junction-worktree-trap, writing-preferences, wsl-for-network, wsu-library-access-cutoff.

### 01 carm_detection (intraoperative C-arm level detection to hospital testing)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| acquisition-space-saturation | live | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); the claim wording | current finding behind Figure 5 |
| anomaly-rule-rc22-evaluated | live | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | removed from the manuscript on Greg's order (D.24) |
| carm-plateau-is-the-denominator | live | same-device 82-85 % plateau is the truth denominator; clean subset 96.9 % | RESULTS_CATALOG A8.7 uses 214 / 95.6 % from the repair tool; the note's 204 / 96.9 % is a different rule |
| carmlspine-level-experiment | live | C-ArmLSpine (148 cases, AP+LAT+CBCT): reading traps, pose convention, pipeline | its 2026-09-21 numbers (96.3 / 37.9 / 98.2) are the v2-lineage run; current numbers are A2 and A3 |
| chart-preferences | live | slides: no sideways bars, donuts/lines, published background figures, big type | slide preference for any talk |
| data-audit-99-gaps | live | 99 gaps in docs/DATA_COMPLETENESS_AUDIT.md; the ones that change the science | the audit list that gates final training (the D-rows) |
| detection-is-the-binding-constraint | live | counting fails on detection (60 points) not linking (11-28) | the finding that orders the C-arm work |
| drr-row-spacing-defect | live | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | why only sweep_v3 counts |
| figure-preferences-schwingnet | live | Greg's figure verdicts for the SchwingNet manuscript (2026-09-22) | taste record for any new figure |
| film-fluoro-boundary-not-transferable | live | devices separate pairwise; film vs fluoroscopy does not transfer to an unseen corpus | the manifold finding (A13) |
| film-ncurve-ablation-result | SUPERSEDED | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | trust sn:results/coverage/film_ncurve/ablation/READ.md: 7 of 9 cells separated, six help and one hurts (A10.6-A10.10) |
| flagship-paper-frame | live | ships a network; claims ledger; PENDING macros | the five contributions and the ledger rule |
| flagship-program | live | gates G0-G7 in docs/FLAGSHIP_PLAN.md | which gates are formally closed is not written in one place (RESEARCH_DIRECTIONS unknown 13); pipeline_state.py on the grid is the authority |
| fluorocap-dataset | live | FluoroCap test set on grid ~/FluoroCap: stages, routes, manifest schema, v0.1 freeze | 16.5 KB; copy into archive; reference from carm_detection |
| fluorocap-is-reproductions-not-fluoroscopy | live | 72.8 % of panels have zero pixel residual; test set only | why FluoroCap is excluded |
| fluorocap-pipeline-resume | live | start at docs/PIPELINE_RESUME.md and tools/pipeline_state.py; add every stage there | its ssh line runs python on the login node, which the login-node rule forbids (OPEN_QUESTIONS F10): run it as a job |
| grid-quota-and-deleted-banks | live | pan_quota; banks deleted 2026-09-20; holdout.py raises; refs repointed to v7 | why v2-v5c banks are gone and what that broke |
| guided-acquisition-loop | live | commanded displacement + digital fiducial; what must not be quoted | references docs/provisional and INVENTION_DISCLOSURE in the private repo; corpus result of job 40376577 NOT RECORDED (C3.12) |
| identity-audit-findings | live | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case is not a person | the patient-identity spec summary |
| k-devices-one-network | live | per-device parameter sets, styled renders, LODO; where the pipeline lives | the device pipeline map |
| learned-formation-refuted-calibrate-instead | redacted copy required | CT to fluoro formation calibrated on DeepFluoro; first real-fluoro recall; the 2026-09-21 deliverables (IRB protocol draft, seed-grant draft, phantom plan, TL;DR) | copy the HANDOFF/context version (one staff contact withheld); 18.9 KB; names a DMC neurosurgeon: keep that redacted too; the IRB and grant drafts exist only in a scratchpad and as claude.ai artifacts |
| level-service-serving | live | website never serves weights; service + private HF weights | standing serving rule |
| local-level-identity-thesis | live | name a vertebra by local morphology instead of counting from C2 | the thesis sentence of the programme |
| lstv-tltv-detection-goal | live | standing determination: detect LSTV/TLTV from C-arm exposures | its numbers (72.9 / 97.0 / 44.9) are the v2-lineage table (C1.18) |
| mixed-length-head-and-sota | LEAKED | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | do not quote 97.47 or 99.02; held-out film naming today is the film N-curve (A10.1-A10.3) |
| model-registry | live | content-addressed weights store, ledger, MLflow, HF mirror | whether ~/model_registry survived the migration is OPEN_QUESTIONS B31 |
| oblique-angles-and-sweep-vision | live | detector must work at any angle; synthetic AP to lateral arcs; AR vision is preview only | pose-pool rule and the case134 spin |
| paper-split-2026-09-24 | live | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | the scope rule of paper 1 and paper 2 |
| pooled-vs-lodo-device-designs | live | pooled and LODO both reported; list builder refuses split subjects | design rule for device arms |
| recurrent-head-restored-2026-09-16 | live | BiGRU head was unreachable; restored, +10 points on the 27-class bank | the head's 99 % was on a cervical-dominated bank (CONTEXT_EXPORT section 3) |
| registration-free-prior-art | live | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | three unread IEEE papers could overturn the naming claim (RESEARCH_DIRECTIONS unknown 11) |
| rigor-audit-findings | live | selective reporting in two places, interval-free detector figure, one CI in 54 claims | the fix list answered item by item in sn:results/RIGOR_FIXES.md |
| rsnai-author-instructions | live | Radiology AI limits | submission limits |
| rsnai-paper-endpoint | live | one concise RSNA AI manuscript paper/rsnai/main_v2.tex; checklist docs/RSNAI_PLAN.md; citation traps | main_v2.tex is superseded by SchwingNet/main.tex; the citation traps stand |
| schwingnet-manuscript | live | SchwingNet/ manuscript built only from rigor-passing numbers; CLAIM map, ATLAS cards | copy the HANDOFF/context version: it substitutes the banned word where the note states the rule |
| selective-prediction-the-honest-99 | LEAKED | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | the arithmetic (about 298 answered cases to certify 99 %) stands (E.9); the numbers are on the leaked v2 bank and its own test half (C1.8); no clean re-run exists (OPEN_QUESTIONS C13) |
| six-figure-paper-plan | live | six figures; LevelCheck pre-specified, never tuned | the finish-line rule |
| spine-data-review-and-ts-bench | live | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the PRISMA-ScR scoping review | the SPINEPS stores it built carry raw ids; the TS bench is inside the v9 bank |
| split-leak-cross-naming | live | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | leak record and the bank-building rule |
| stc-does-not-transfer | live | Star Temporal Classification loses to cross-entropy on naming | refuted loss; do not revisit (C1.7) |
| sweep-map-replaces-registration | live | overlapping frames build a radiograph-only registration; sweep_v3 numbers | the TS-bench numbers are held out only for the v7-lineage encoder (ts-bench-inside-v9-bank) |
| sweep-physics-no-bone | live | physics-perturbed sweeps rendered with no bone; fix --paths2-only | its causal claim is superseded by physics-three-defects-measured |
| synthetic-real-ratio-evidence | live | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | the project's own ratio was never swept (A10.11; OPEN_QUESTIONS A9) |
| tables-black-not-colour | live | matrix tables black + one outlined mark | table style rule |
| ts-bench-inside-v9-bank | live | TS render bench is not held out from the v9 encoder (70 TS + 1 CTSP + 0 VerSe renders unseen) | held-out rule for v9-lineage models |
| two-mechanisms-thesis | SUPERSEDED | morphology for quick limited-FOV localisation; sweep/count as the safety net | the framing governs paper 1; its numbers are the v2-lineage run (C1.18, A3.11): current 601/617 = 97.4 % whole lateral (A3.1), 451/603 = 74.8 % one body (A3.3) |
| xray-corner-detector-status | redacted copy required | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | names a student by first name; the HANDOFF copy is unredacted: redact before copying |

### 02 transitional_fluoro (the anomaly-aware classifier, paper 2, power)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| anomaly-harvest-directive | live | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in FOV | the binding directive behind the anomaly scan |
| feasibility-claims-measured | RECORD ONLY | the FOV feasibility report tested claim by claim; head/encoder pairing trap; the Cina benchmark mandate | never quote its numbers; 14.7 KB |
| fluorocap-prototype-and-lstv-arm | live | single-image prototype, transitional harvest arm, Semantic Scholar route; LSTV flag results; scoping-review statistics; the two verification benches | 13.6 KB |
| lstv-data-landscape | redacted copy required | where LSTV/TLTV labels exist; the one published 2-D LSTV model (Kwak 2025) | copy the HANDOFF/context version (three researcher e-mail addresses withheld) |
| lstv-tltv-detection-goal | live | standing determination: detect LSTV/TLTV from C-arm exposures | its numbers (72.9 / 97.0 / 44.9) are the v2-lineage table (C1.18) |
| paper-split-2026-09-24 | live | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | the scope rule of paper 1 and paper 2 |
| polypose-decision | live | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | Greg's decision on synthesis |
| spineps-ids-can-be-scrambled | live | pre-147428d SPINEPS masks carry raw ids; guard tools/spineps_ids.py; VERIDAH not truth; v8/v9 saw most G3 test people | standing trap for every SPINEPS consumer |
| two-mechanisms-thesis | SUPERSEDED | morphology for quick limited-FOV localisation; sweep/count as the safety net | the framing governs paper 1; its numbers are the v2-lineage run (C1.18, A3.11): current 601/617 = 97.4 % whole lateral (A3.1), 451/603 = 74.8 % one body (A3.3) |

### 03 render_devices (DRR banks, device cards, formation, PolyPose)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| acquisition-space-saturation | live | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); the claim wording | current finding behind Figure 5 |
| deepfluoro-convention | live | DeepFluoro file layout and projection convention (0.00 px reprojection) | the settled convention |
| device-sampling-audit | live | card clip saturates (95-98 % of the joint lost); typicality gate | open defect A12.6; the clip is still the default |
| drr-row-spacing-defect | live | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | why only sweep_v3 counts |
| drr-to-fluoro-levers | live | three measured levers for DRR to fluoro; CycleGAN and ADDA refuted; honest ceiling | what to build and what not to build for sim-to-real |
| film-fluoro-boundary-not-transferable | live | devices separate pairwise; film vs fluoroscopy does not transfer to an unseen corpus | the manifold finding (A13) |
| fluorogen-synthetic | live | SDXL + ControlNet + LoRA synthetic C-arm frames; img2img dead at every strength; CUT v2 is not a lever | refuted generative route; stops a repeat |
| k-devices-one-network | live | per-device parameter sets, styled renders, LODO; where the pipeline lives | the device pipeline map |
| learned-formation-refuted-calibrate-instead | redacted copy required | CT to fluoro formation calibrated on DeepFluoro; first real-fluoro recall; the 2026-09-21 deliverables (IRB protocol draft, seed-grant draft, phantom plan, TL;DR) | copy the HANDOFF/context version (one staff contact withheld); 18.9 KB; names a DMC neurosurgeon: keep that redacted too; the IRB and grant drafts exist only in a scratchpad and as claude.ai artifacts |
| oblique-angles-and-sweep-vision | live | detector must work at any angle; synthetic AP to lateral arcs; AR vision is preview only | pose-pool rule and the case134 spin |
| physics-three-defects-measured | live | only the AEC defect changed an image; the display window hides the lateral spine | physics diagnosis record |
| polypose-decision | live | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | Greg's decision on synthesis |
| polypose-generator-build | live | where the PolyPose generator lives; six traps | commit 1f4418f never pushed; VALIDATION.{json,md} not written (G.6) |
| pooled-vs-lodo-device-designs | live | pooled and LODO both reported; list builder refuses split subjects | design rule for device arms |
| sweep-physics-no-bone | live | physics-perturbed sweeps rendered with no bone; fix --paths2-only | its causal claim is superseded by physics-three-defects-measured |
| synthetic-real-ratio-evidence | live | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | the project's own ratio was never swept (A10.11; OPEN_QUESTIONS A9) |
| ts-sacrum-excludes-s1 | live | TS sacrum excludes S1; whole sacrum = union | the trap behind NeurIPS defect A (F.47) |
| vf813-drops-c1-t9-use-raw-verse-for-whole-spine | live | ~/vf_813 maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | render-source rule |

### 04 plain_film_level_id (the plain-film line, early level models)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| context-ladder-2d-level-experiment | live | how much spine must be visible to name a vertebra; BUU levels are counting-inferred | design rules of the context ladder (masking, not cropping) |
| feasibility-claims-measured | RECORD ONLY | the FOV feasibility report tested claim by claim; head/encoder pairing trap; the Cina benchmark mandate | never quote its numbers; 14.7 KB |
| film-ncurve-ablation-result | SUPERSEDED | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | trust sn:results/coverage/film_ncurve/ablation/READ.md: 7 of 9 cells separated, six help and one hurts (A10.6-A10.10) |
| fluoro-panel-gap-diagnosed | live | literature panels 19.7 % vs 95.1 % on radiographs: domain plus contamination | FluoroCap diagnosis; never quote 19.7 % as accuracy |
| level-id-2d-results-2026-09-13 | RECORD ONLY | 2-D level ID on real films, 13 Sep results | history; the 96.7 % is on the cervical-dominated films_ann bank (C1.1) |
| level-model-bank-coverage | live | the deployed bank held only cervical and lumbar films | why the 99 % was a 14-class number |
| mixed-length-head-and-sota | LEAKED | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | do not quote 97.47 or 99.02; held-out film naming today is the film N-curve (A10.1-A10.3) |
| nhanes-double-inclusion | live | NHANES in the banks twice, split independently | leak record |
| recurrent-head-restored-2026-09-16 | live | BiGRU head was unreachable; restored, +10 points on the 27-class bank | the head's 99 % was on a cervical-dominated bank (CONTEXT_EXPORT section 3) |
| remedies-refuted-2026-09-17 | LEAKED | pretrain-on-DRR, film-noise, anchored-only, CReST admission all lose | the refutations were not re-run on v9 (RESEARCH_DIRECTIONS unknown 24); the scaling curve it quotes is C2.1 |
| selective-prediction-the-honest-99 | LEAKED | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | the arithmetic (about 298 answered cases to certify 99 %) stands (E.9); the numbers are on the leaked v2 bank and its own test half (C1.8); no clean re-run exists (OPEN_QUESTIONS C13) |
| stc-does-not-transfer | live | Star Temporal Classification loses to cross-entropy on naming | refuted loss; do not revisit (C1.7) |
| xr-benchmark-and-robustness-2026-09-13 | RECORD ONLY | X-ray level-ID competitor benchmark, physics tiers, recurrent head | the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; OPEN_QUESTIONS F5) |
| xray-corner-detector-status | redacted copy required | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | names a student by first name; the HANDOFF copy is unredacted: redact before copying |

### 05 anomaly_scan_census (harvest, registry, ruleclass, review tree)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| anomaly-harvest-directive | live | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in FOV | the binding directive behind the anomaly scan |
| anomaly-manifest-sources | live | 749 anomalous spines in 3 tiers; master table lstv_flag_labels_v2.csv; why the count was once 34/16/2 | the dated series of transitional counts is RESULTS_CATALOG D.27; never mix dates |
| anomaly-rule-rc22-evaluated | live | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | removed from the manuscript on Greg's order (D.24) |
| competitor-benchmark | live | TotalSegmentator, SPINEPS/VERIDAH + Moller ribs, VISTA3D, RibSeg in the one-shot space; grid layout; decoder rules | the SPINEPS stores it harvested carry raw ids (spineps-ids-can-be-scrambled) |
| l6-sample-count-and-counting-decoder | live | L6 dice 0.000 = too few distinct cases; counting decoder; Dataset815 | CT-6 premise |
| lstv-data-landscape | redacted copy required | where LSTV/TLTV labels exist; the one published 2-D LSTV model (Kwak 2025) | copy the HANDOFF/context version (three researcher e-mail addresses withheld) |
| lstv-oneshot-training-run | live | Dataset810 one-shot LSTV run for the CNS slides; retired for Dataset813 (numbered ribs) | whether the Dataset813 folds finished or were scored is NOT RECORDED (C5.3) |
| ruleclass-super-detector-run | live | /rs/.../ruleclass census over 21,622 CTs; two arms; review tree | what the arms finished after 2026-09-27 is NOT RECORDED (OPEN_QUESTIONS B1) |
| spine-data-review-and-ts-bench | live | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the PRISMA-ScR scoping review | the SPINEPS stores it built carry raw ids; the TS bench is inside the v9 bank |
| spineps-ids-can-be-scrambled | live | pre-147428d SPINEPS masks carry raw ids; guard tools/spineps_ids.py; VERIDAH not truth; v8/v9 saw most G3 test people | standing trap for every SPINEPS consumer |
| spondylolysis-and-border-anomaly-findings | live | LCC deletes the loose lamina; T-L and L-S variants co-occur | two paper-worthy findings not in code |
| versefusion-t13-flag-wrong | live | VerSeFusion has_T13 says 18; truth 6 | label-map trap, third instance |

### 06 data_platform (manifest, migration, identity, leakage, grid operations)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| cloudflare-tls-fingerprint | live | 403 everywhere = TLS fingerprint block; curl_cffi impersonate chrome | fetch recipe for the JHU archive and similar hosts |
| ct-benchmark-covers-all-collections | live | the CT axis is every collection (5,700+ subjects); tools/ct_inventory.py | subject-count rule for any benchmark |
| data-audit-99-gaps | live | 99 gaps in docs/DATA_COMPLETENESS_AUDIT.md; the ones that change the science | the audit list that gates final training (the D-rows) |
| data-platform-migration-2026-10 | live | data_platform: manifest, layout, batches B00-B14, census, state 2026-10-08, visibility | the live note (mtime 2026-10-08 16:43) is newer than the HANDOFF copy (16:39): re-run refresh_context.py before copying; the B01 contradiction is OPEN_QUESTIONS B30 |
| dataset813-image-links-are-container-paths | live | Dataset813 imagesTr links resolve only in the container; never repair; HF_EXPORT_DIR | nnU-Net raw-tree trap |
| flagship-program | live | gates G0-G7 in docs/FLAGSHIP_PLAN.md | which gates are formally closed is not written in one place (RESEARCH_DIRECTIONS unknown 13); pipeline_state.py on the grid is the authority |
| fluorocap-is-reproductions-not-fluoroscopy | live | 72.8 % of panels have zero pixel residual; test set only | why FluoroCap is excluded |
| grid-apptainer-module-works | live | module load apptainer/1.2.2 sandbox builds; secp starts at once | container route on the grid |
| grid-ct-0533-truncated | live | CT 0533 truncation repaired on the grid and HF 2026-09-23 | release defect record; KNOWN_ISSUES.md still lacks it (F.19) |
| grid-quota-and-deleted-banks | live | pan_quota; banks deleted 2026-09-20; holdout.py raises; refs repointed to v7 | why v2-v5c banks are gone and what that broke |
| identity-audit-findings | live | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case is not a person | the patient-identity spec summary |
| model-registry | live | content-addressed weights store, ledger, MLflow, HF mirror | whether ~/model_registry survived the migration is OPEN_QUESTIONS B31 |
| nhanes-double-inclusion | live | NHANES in the banks twice, split independently | leak record |
| spine-data-review-and-ts-bench | live | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the PRISMA-ScR scoping review | the SPINEPS stores it built carry raw ids; the TS bench is inside the v9 bank |
| spineps-ids-can-be-scrambled | live | pre-147428d SPINEPS masks carry raw ids; guard tools/spineps_ids.py; VERIDAH not truth; v8/v9 saw most G3 test people | standing trap for every SPINEPS consumer |
| split-leak-cross-naming | live | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | leak record and the bank-building rule |
| splits-origin-and-v3-resplit | redacted copy required | 5-fold splitter is patient-grouped + LSTV-stratified; v3 needs a resplit; the shipped v11 splits never read the lumbar count | source_path points at the HANDOFF copy on purpose; the live original is the one note in the memory folder whose name the copier renamed |
| ts-bench-inside-v9-bank | live | TS render bench is not held out from the v9 encoder (70 TS + 1 CTSP + 0 VerSe renders unseen) | held-out rule for v9-lineage models |
| ts-sacrum-excludes-s1 | live | TS sacrum excludes S1; whole sacrum = union | the trap behind NeurIPS defect A (F.47) |
| versefusion-t13-flag-wrong | live | VerSeFusion has_T13 says 18; truth 6 | label-map trap, third instance |
| vf813-drops-c1-t9-use-raw-verse-for-whole-spine | live | ~/vf_813 maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | render-source rule |
| windows-ssh-to-grid | live | Windows ssh needs hmac-sha1 and IPv4; wsu-grid alias | ssh config facts |

### 07 ctsp_dataset (CTSpinoPelvic1K release, article, NeurIPS)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| annotator-roster | redacted copy required | who annotated what, from slots[].reviewer in the private ledgers; 13 students by 2026-08-23 | copy HANDOFF/context/annotator-roster.md (usernames and per-person counts withheld); the full copy stays in GREG_ONLY/context |
| canonical-rib-triage | live | rib review set defined by qc_v4_ribs_and_verts.py (152 cases); worklist regenerated from it | rib-review history of the release |
| chart-preferences | live | slides: no sideways bars, donuts/lines, published background figures, big type | slide preference for any talk |
| cns-deck-v2-2026-09-25 | live | CNS spine deck: v10 discloses Part B; v12_public (17 slides, CT side only) is the disclosure-safe cut; generators and template traps | the generator paper/cns2026 is excluded from the public repo (git info/exclude); 13.3 KB |
| commit-directly-to-master | live | CTSP repo: commit to master, no branches | repo workflow rule |
| competitor-benchmark | live | TotalSegmentator, SPINEPS/VERIDAH + Moller ribs, VISTA3D, RibSeg in the one-shot space; grid layout; decoder rules | the SPINEPS stores it harvested carry raw ids (spineps-ids-can-be-scrambled) |
| ctspine1k-selection-code-deleted | live | CTSpine1K's supine/prone selector does not select; recover at 7f44959 | source-lineage fact in the dataset article (F.2) |
| dataset813-image-links-are-container-paths | live | Dataset813 imagesTr links resolve only in the container; never repair; HF_EXPORT_DIR | nnU-Net raw-tree trap |
| grid-ct-0533-truncated | live | CT 0533 truncation repaired on the grid and HF 2026-09-23 | release defect record; KNOWN_ISSUES.md still lacks it (F.19) |
| hf-identity | live | HF username gregoryschwingmdphd | Greg's own public handle; no secret |
| hf-mirror-is-v10 | live | public HF is v10 with id 29 on 2026-09-27; v11 local only; lines to change when it ships | its Zenodo-is-v10 statement is contradicted by four documents giving v11 (MANUSCRIPTS section 20 C1); live state unverified (OPEN_QUESTIONS E7) |
| journal-figure-and-style-rules | live | Medical Physics figure and text rules; no abstract in the main document; page estimate | dataset-article style gate |
| l6-sample-count-and-counting-decoder | live | L6 dice 0.000 = too few distinct cases; counting decoder; Dataset815 | CT-6 premise |
| local-level-identity-thesis | live | name a vertebra by local morphology instead of counting from C2 | the thesis sentence of the programme |
| lstv-oneshot-training-run | live | Dataset810 one-shot LSTV run for the CNS slides; retired for Dataset813 (numbered ribs) | whether the Dataset813 folds finished or were scored is NOT RECORDED (C5.3) |
| lstv-reread-queue | live | log doubtful source LSTV labels in docs/lstv_reread_queue.csv | re-read protocol |
| nninteractive-colab-versions | live | ITK-SNAP DLS (nnInteractive) Colab pins | annotation tooling for student rib review |
| panjabi-1991-page-892 | live | full Panjabi 1991 obtained; Table 3 in level_references.csv | the PDF CTSpinoPelvic1K-1/PANJABI_1991_FULL_fixed.pdf is a copyrighted article scan: reference by path, do not copy into a repository |
| prone-supine-flexibility-future | live | 351 separate-mode pelvic acquisitions held out; flexibility idea | CT-11 premise |
| publication-roadmap | live | paper split plan and venues, with 2026-06/07/09 updates | history of the venue plan |
| push-both-github-remotes | live | CTSP: push origin and osc every time | repo rule |
| review-space-repos | live | exact HF repo ids for the review Spaces; the decoy repo | annotation infrastructure |
| rib-approach-ts-trust | live | rib labelling: trust TS numbering, add Moller's bridge (implemented 2026-06-29) | how the release ribs were built |
| rib-auto-engulf-post-correction-only | live | rib cleanup only after student correction | release pipeline rule |
| rib-qc-gates-never-block-lstv | redacted copy required | only rib-purity checks gate rib reviews | names two annotator usernames in its why-paragraph; the HANDOFF copy is unredacted: redact before copying |
| s1-carve-changed-spinopelvic | live | carved S1 (29) unreliable; gone in v11; retire checks on 29 | standing rule: identifier 29 retired |
| scheme-bone-hardware-only | live | scheme 0-68 with one hole at 29 from v11; 13 ribs per side | the label scheme |
| splits-origin-and-v3-resplit | redacted copy required | 5-fold splitter is patient-grouped + LSTV-stratified; v3 needs a resplit; the shipped v11 splits never read the lumbar count | source_path points at the HANDOFF copy on purpose; the live original is the one note in the memory folder whose name the copier renamed |
| spondylolysis-and-border-anomaly-findings | live | LCC deletes the loose lamina; T-L and L-S variants co-occur | two paper-worthy findings not in code |
| tables-black-not-colour | live | matrix tables black + one outlined mark | table style rule |
| thoracic-gt-fov-limited | live | v3 thoracic GT covers about T8 down | dataset scope fact |
| ts-sacrum-excludes-s1 | live | TS sacrum excludes S1; whole sacrum = union | the trap behind NeurIPS defect A (F.47) |
| zenodo-deposit | live | Zenodo DOIs, version recipe, build archive; token file name only | says v10 is current; four documents give v11 = 10.5281/zenodo.22797014 published 2026-09-18 (MANUSCRIPTS section 20 C1); names ~/.zenodo_token (a file name, no value) |

### 08 ct_morphometry_parity (measurements, 3-D to 2-D parity, PAR-n, CT-n)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| ostk-canal-closing-regression | live | ostk 1b7005c inflates VBHp/EPD 10-17 mm on about 1 in 7 vertebrae | open defect CT-1; the fix plan is in the note |
| panjabi-1991-page-892 | live | full Panjabi 1991 obtained; Table 3 in level_references.csv | the PDF CTSpinoPelvic1K-1/PANJABI_1991_FULL_fixed.pdf is a copyrighted article scan: reference by path, do not copy into a repository |
| s1-carve-changed-spinopelvic | live | carved S1 (29) unreliable; gone in v11; retire checks on 29 | standing rule: identifier 29 retired |

### 09 toolkit (OpenSpineToolkit)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| commit-directly-to-master | live | CTSP repo: commit to master, no branches | repo workflow rule |
| engine-swap-architecture | live | demo consumes a metrics.json contract so the engine can be swapped | PACS demo interface contract |
| ostk-canal-closing-regression | live | ostk 1b7005c inflates VBHp/EPD 10-17 mm on about 1 in 7 vertebrae | open defect CT-1; the fix plan is in the note |
| pacs-demo-and-ostk-params | live | ostk parameters and CLI; NiiVue PACS demo; no blanket SVA/TPA claim | toolkit scope and the demo contract |
| postop-jaggedness-future | live | future: fix post-op synthesis voxel roughness | toolkit future item |
| postop-spine-synthesis | live | ostk.surgery synthetic post-op spines (labels only) | toolkit prototype record (G.5) |

### 10 grid_access_students (Beethoven, onboarding, lab recipe)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| ashley-bridge-project | redacted copy required | Beethoven (was Ashley Bridge): hpcworker framework + browser extension over Open OnDemand; versions 2.0.0 to 14.0.0, access service, the no-keys rule | 22.5 KB; in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| ashley-compliance-boundary | redacted copy required | Ashley never handles a Claude credential; terms research; dispute clauses; terms version 3 | in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| ashley-extension-project | redacted copy required | Ashley VS Code extension v3.0.0 (2026-09-28): agreements, access service, Marketplace publication, what still needs Greg | in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| beethoven-2026-10-02-field-failures | redacted copy required | first real use 2026-10-02: dead run records never age out, VPN sitting dies after 5 min, reqp preempts workers, group oschome is not the access list | in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| beethoven-browser-ssh | redacted copy required | browser-ssh prototype works; IWA + Direct Sockets spike; policy facts; decisions waiting on Greg | in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| beethoven-first-run-ux | redacted copy required | Greg's 2026-10-01 brief for the first run; seven messages; prerequisites, VPN, portal, nothing silent | in HANDOFF these sit in GREG_ONLY/context_beethoven; no redacted copy exists yet; redact personal e-mails, student usernames, licence key ids, account names and token paths before copying |
| diagnostics-graph-required | live | every Beethoven feature needs diagnostics-graph nodes first | Beethoven integration rule |
| grid-access-list-gate | redacted copy required | approved students = named ACL entries on /rs/rs_grp_oschome | names one student username; the HANDOFF copy is unredacted: redact before copying |
| grid-apptainer-module-works | live | module load apptainer/1.2.2 sandbox builds; secp starts at once | container route on the grid |
| grid-ashley-deletion-2026-09-28 | live | ~/.ashley wiped during a phone session; destructive commands refuse under CLAUDECODE | safety rule for agents on the grid |
| grid-slurm-inside-apptainer | live | binds that make sbatch work inside a container | Beethoven worker fact |
| grid-ssh-second-factor | live | ssh off-VPN with password + TOTP; warrior bans python, rsync and others | student sign-in facts |
| hf-mirror-is-v10 | live | public HF is v10 with id 29 on 2026-09-27; v11 local only; lines to change when it ships | its Zenodo-is-v10 statement is contradicted by four documents giving v11 (MANUSCRIPTS section 20 C1); live state unverified (OPEN_QUESTIONS E7) |
| lab-recipe-and-board | live | RECIPE.md, board.json to BOARD.md, Claude Doc; local commit not pushed | Student_Projects is at CTSpinoPelvic1K-1/Student_Projects, not Desktop; 10 unstaffed cards, not 11; names Ashley Schehr (a person, a published co-author) and Dr Tech; no e-mails |
| student-onboarding-structure | live | onboarding one-liner, Student_Projects layout, grid account and 2FA facts | the local clone is CTSpinoPelvic1K-1/Student_Projects |
| students-see-no-internals | live | student tools offer one path | Beethoven UX rule |
| windows-ssh-to-grid | live | Windows ssh needs hmac-sha1 and IPv4; wsu-grid alias | ssh config facts |

### 11 website (openspineconsortium.github.io, PACS demo, level service)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| engine-swap-architecture | live | demo consumes a metrics.json contract so the engine can be swapped | PACS demo interface contract |
| hf-identity | live | HF username gregoryschwingmdphd | Greg's own public handle; no secret |
| level-service-serving | live | website never serves weights; service + private HF weights | standing serving rule |
| pacs-demo-and-ostk-params | live | ostk parameters and CLI; NiiVue PACS demo; no blanket SVA/TPA claim | toolkit scope and the demo contract |
| pacs-website-latency-root-cause | live | PACS demo 40 s to 1.36 s (redirect, COEP vs CDN, input size) | website performance record (G.8) |

### 12 qi_wrong_level (the QI manuscript and the wrong-level literature)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| registration-free-prior-art | live | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | three unread IEEE papers could overturn the naming claim (RESEARCH_DIRECTIONS unknown 11) |

### archive (history, superseded decks and plans)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| MEMORY | Greg-only, never copied | the live memory index (14.8 KB); its one-liners carry leaked numbers and link notes that were not copied | two START HERE bullets point at 2026-09-28 and 2026-09-26 states; broken wikilinks listed in CONTEXT_EXPORT section 5 |
| cns-deck-v2-2026-09-25 | live | CNS spine deck: v10 discloses Part B; v12_public (17 slides, CT side only) is the disclosure-safe cut; generators and template traps | the generator paper/cns2026 is excluded from the public repo (git info/exclude); 13.3 KB |
| fluoro-panel-gap-diagnosed | live | literature panels 19.7 % vs 95.1 % on radiographs: domain plus contamination | FluoroCap diagnosis; never quote 19.7 % as accuracy |
| fluorocap-dataset | live | FluoroCap test set on grid ~/FluoroCap: stages, routes, manifest schema, v0.1 freeze | 16.5 KB; copy into archive; reference from carm_detection |
| fluorocap-prototype-and-lstv-arm | live | single-image prototype, transitional harvest arm, Semantic Scholar route; LSTV flag results; scoping-review statistics; the two verification benches | 13.6 KB |
| fluorogen-synthetic | live | SDXL + ControlNet + LoRA synthetic C-arm frames; img2img dead at every strength; CUT v2 is not a lever | refuted generative route; stops a repeat |
| overnight-2026-09-15-chains | RECORD ONLY | where the 2026-09-15 overnight FluoroCap runs wrote their results | history; the markers it names are on the grid under ~/FluoroCap |
| publication-roadmap | live | paper split plan and venues, with 2026-06/07/09 updates | history of the venue plan |
| resume-2026-09-21-pm | RECORD ONLY | 2026-09-21 formation checkpoint; points at docs/HANDOFF_2026-09-21_PM.md | history; names a researcher and an e-mail (Balgrist): never copy unredacted; the repo doc it points at is the record |
| resume-2026-09-22 | RECORD ONLY | 2026-09-22 checkpoint: RSNAI_PLAN, the k-devices queue | history; the repo docs hold the record |
| resume-2026-09-22-pm | RECORD ONLY | 2026-09-23 checkpoint at the top of docs/RESUME_2026-09-22_PM.md; FLAGSHIP_PLAN gates | the resume file it names is in the private repo |
| resume-2026-09-24 | RECORD ONLY | 2026-09-24 checkpoint: Figure 6 open gate released, blinded gate held | history |
| resume-2026-09-26-handoff | RECORD ONLY | 2026-09-26 handoff: U251 and spine blocks | half U251; the spine half points at RESUME_2026-09-22_PM.md |

### exclude (Greg-only, credentials, another study)

| note | status | digest | copy from / caveat |
|---|---|---|---|
| MEMORY | Greg-only, never copied | the live memory index (14.8 KB); its one-liners carry leaked numbers and link notes that were not copied | two START HERE bullets point at 2026-09-28 and 2026-09-26 states; broken wikilinks listed in CONTEXT_EXPORT section 5 |
| cns-abstract-418-deck | not copied (another project) | CNS 2026 Abstract 418 LITT deck v5 (46 slides) | another study (U251 glioblastoma / LITT); not spine work |
| commercialization-stance | Greg-only, never copied | standing commercial objective and the two-track rule (research grid vs commercial accounts) | Greg's private position (GREG_ONLY/PRIVATE_STATE.md section 1); never in a project folder or public text |
| fluorocap-credentials-and-resolution | Greg-only, never copied | credential-store location for the FluoroCap harvesters and the publisher refetch rules | credential-location note (PRIVATE_STATE section 2); FluoroCap is dropped by directive D1 |
| hf-org-token-location | Greg-only, never copied | anonymous-mlhc org token location | credential-location note (PRIVATE_STATE section 2) |
| hf-osc-token-and-namespace | Greg-only, never copied | OpenSpineConsortium is a real HF org; its token location | credential-location note (PRIVATE_STATE section 2); the org fact itself is in INFRASTRUCTURE section 1 |
| litt-contralateral-two-readings | not copied (another project) | LITT contralateral signal: migration vs carry-over cannot be separated | another study (U251 glioblastoma / LITT); not spine work |
| resume-2026-09-26-handoff | RECORD ONLY | 2026-09-26 handoff: U251 and spine blocks | half U251; the spine half points at RESUME_2026-09-22_PM.md |
| schwingnet-disclosure-scrub | Greg-only, never copied | 2026-09-26 scrub of public SchwingNet disclosures; pending GitHub Support purges | Greg's private filing state (PRIVATE_STATE section 3) |
| u251-cibersort-deconvolution | not copied (another project) | U251 Neftel-state deconvolution; CIBERSORT not installed anywhere | another study (U251 glioblastoma / LITT); not spine work |
| u251-multiomics-sample-pairing | not copied (another project) | U251 RNA/methylation pairing lives only in metadata | another study (U251 glioblastoma / LITT); not spine work |
| u251-name-sweep-traps | not copied (another project) | U251 repo: N1/N2 are null-hypothesis labels; SHA-anchored files | another study (U251 glioblastoma / LITT); not spine work |
| u251-project-containment | not copied (another project) | Greg 2026-09-26: U251 work only in the u251 dir and its public repo | another study (U251 glioblastoma / LITT); not spine work |
| u251-translation-fall-il68b | not copied (another project) | U251 LITT RNA-seq: the translation fall is a ribosomal-protein block | another study (U251 glioblastoma / LITT); not spine work |

## HANDOFF sections by family: what STATUS.md and TODO.md are cut from

The `HANDOFF/` rows give every file section with its families; the compact map a builder needs:

| family | STATUS.md (results in hand) | TODO.md (what remains) | memory and rules |
|---|---|---|---|
| carm_detection | RESULTS_CATALOG A1-A9, A11-A14, A18-A19, C3, C4; DATASET_USAGE 0-3, 6; LEAKAGE 1-7; MANUSCRIPTS 2, 4, 17 | OPEN_QUESTIONS A1 A5 A9-A12 A16-A17, B6-B14 B17-B24, C1-C7 C12-C17 C20, D1 D6 D7, E1 E20 E21, F4-F7 F19-F21; RESEARCH_DIRECTIONS 1.1-1.7, FLU-2, PAR-4, PAR-5, PUB-1; RECIPES 0, 1, 2, 5, 7, 10; LITERATURE_STATE 1.4, 1.5, 2A, 3 | README 5, INFRASTRUCTURE 1.1, 3, 10 |
| transitional_fluoro | RESULTS_CATALOG A1, A5, A16, A17, B, E; literature_state/power.md; working_notes/t2_wilson_check.py | OPEN_QUESTIONS A16-A17, B15, C1-C7 C10-C11, E8, F3; RESEARCH_DIRECTIONS 2.1-2.9, FLU-1, FLU-2, PAR-6, DAT-1; RECIPES 3, 4; LITERATURE_STATE 1.2, 2A, 3, 4; MANUSCRIPTS 3, 16 | the lstv-tltv-detection-goal and paper-split notes |
| render_devices | RESULTS_CATALOG A6, A7, A11-A14, C2, C4, G.6-G.7 | OPEN_QUESTIONS B9-B10, C18; RESEARCH_DIRECTIONS 1.4, PAR-2; RECIPES 5, 6; LITERATURE_STATE 1.5, 1.6, 2D; LEAKAGE 3 (device designs) | k-devices, device-sampling, deepfluoro notes |
| plain_film_level_id | RESULTS_CATALOG A10, A14, A15, C1, C2 | OPEN_QUESTIONS C2, C4, F5; RESEARCH_DIRECTIONS 1.1; RECIPES 1.8, 2; LITERATURE_STATE 1.3, 2C; MANUSCRIPTS 10 | the LEAKED and RECORD ONLY notes with their replacements |
| anomaly_scan_census | RESULTS_CATALOG D (D.1-D.27), A16.6-A16.8 | OPEN_QUESTIONS B1-B5, C21, F12 F13 F22; RESEARCH_DIRECTIONS CT-3, CT-4, CT-8, CT-9, FLU-1; RECIPES 3.1-3.5; LITERATURE_STATE 1.2, 2B, 5 | ruleclass, harvest directive, spineps-ids, versefusion notes |
| data_platform | RESULTS_CATALOG A18, A19; DATASET_USAGE 2, 4, 7, 8; LEAKAGE 2-7; README 3 | OPEN_QUESTIONS A19 A26, B16-B33, E4 E5 E16, F14 F17 F23; RESEARCH_DIRECTIONS 5.1-5.5, DAT-1; RECIPES 0, 10; LITERATURE_STATE 1.1, 2; MANUSCRIPTS 16, 19; INFRASTRUCTURE 2, 4, 5 | the grid operating notes and the identity / leak notes |
| ctsp_dataset | RESULTS_CATALOG F1, F3, C5; MANUSCRIPTS 6, 7, 8, 9, 13 | OPEN_QUESTIONS A2 A6-A8 A20-A22 A27, B16 B27 B28, C19 C22, D3-D5, E2 E3 E6 E7 E10-E14 E19, F2 F10 F11 F16; RESEARCH_DIRECTIONS CT-3, CT-6, CT-7, CT-10, CT-11, PUB-1; RECIPES 8, 9; LITERATURE_STATE 1.1 | label scheme, S1 carve, rib and review notes |
| ct_morphometry_parity | RESULTS_CATALOG F2 (F.21-F.45), F.37-F.38, G.2-G.4 | OPEN_QUESTIONS C8 C9, D2, E9, F9; RESEARCH_DIRECTIONS 1.3, 3.1-3.9, PAR-1 to PAR-6, CT-1, CT-2, CT-4, CT-5, CT-7; RECIPES 9; MANUSCRIPTS 6, 11 | ostk regression, panjabi, s1-carve notes |
| toolkit | RESULTS_CATALOG G (G.1-G.8) | OPEN_QUESTIONS B29, F8, F18; RESEARCH_DIRECTIONS CT-1; INFRASTRUCTURE 7 | label-scheme, ostk-canal-closing, pacs-demo, postop notes |
| grid_access_students | INFRASTRUCTURE 2.1-2.3, 8, 11; README 4, 8, 9, 10 | OPEN_QUESTIONS A18 A25, B34, E18; GLOSSARY grid section | the six Beethoven notes (redacted), onboarding, lab recipe, access gate, ssh notes |
| website | RESULTS_CATALOG G.8; INFRASTRUCTURE 6 (the service) | MANUSCRIPTS 12 (med-ed), OPEN_QUESTIONS A21 | level-service-serving, pacs notes, engine-swap |
| qi_wrong_level | MANUSCRIPTS 5; RESULTS_CATALOG E.10, B.8; LITERATURE_STATE 6; literature_state/topic1_bibliography.md | none recorded beyond keeping the draft private | registration-free-prior-art |
| archive | RESULTS_CATALOG Part C header; MANUSCRIPTS 4, 8, 13, 14, 18, 19 | none | cns-deck, publication-roadmap, fluorocap, the resume notes (reference only) |

Greg-only, never into any project folder: `GREG_ONLY/PRIVATE_STATE.md` sections 1-6, `GREG_ONLY/README.md`, `GREG_ONLY/context/` (MEMORY.md archive, the five moved notes, the three full copies), INFRASTRUCTURE section 9 (credentials, moved) and MANUSCRIPTS section 15 (invention disclosure). OPEN_QUESTIONS rows A3, A4, A13, A15, A24, A28 and F1 were moved there as well.

## What is superseded by what (the notes a builder must not quote as current)

| note | superseded or leaked part | what replaces it |
|---|---|---|
| feasibility-claims-measured | RECORD ONLY (RECORD ONLY [LEAK]) | never quote its numbers; 14.7 KB |
| figure-preferences-schwingnet | live (PARTLY SUPERSEDED (five-figure paper 1, mem:paper-split-2026-09-24.md)) | taste record for any new figure |
| film-ncurve-ablation-result | SUPERSEDED (SUPERSEDED reading) | trust sn:results/coverage/film_ncurve/ablation/READ.md: 7 of 9 cells separated, six help and one hurts (A10.6-A10.10) |
| flagship-paper-frame | live (PARTLY SUPERSEDED (LevelCheck comparison moved to paper 2)) | the five contributions and the ledger rule |
| grid-access | live (PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE section 13 rows 3-4)) | aliases now resolve (windows-ssh-to-grid); data moved to Ceph (grid-ceph-volume-oschome) |
| hf-mirror-is-v10 | live (PARTLY SUPERSEDED) | its Zenodo-is-v10 statement is contradicted by four documents giving v11 (MANUSCRIPTS section 20 C1); live state unverified (OPEN_QUESTIONS E7) |
| level-id-2d-results-2026-09-13 | RECORD ONLY (RECORD ONLY) | history; the 96.7 % is on the cervical-dominated films_ann bank (C1.1) |
| mixed-length-head-and-sota | LEAKED (LEAKED) | do not quote 97.47 or 99.02; held-out film naming today is the film N-curve (A10.1-A10.3) |
| overnight-2026-09-15-chains | RECORD ONLY (not copied (history-only entry point)) | history; the markers it names are on the grid under ~/FluoroCap |
| publication-roadmap | live (PARTLY SUPERSEDED (later frames in flagship, rsnai, paper-split notes)) | history of the venue plan |
| remedies-refuted-2026-09-17 | LEAKED (LEAKED numbers) | the refutations were not re-run on v9 (RESEARCH_DIRECTIONS unknown 24); the scaling curve it quotes is C2.1 |
| resume-2026-09-21-pm | RECORD ONLY (not copied (history-only entry point)) | history; names a researcher and an e-mail (Balgrist): never copy unredacted; the repo doc it points at is the record |
| resume-2026-09-22 | RECORD ONLY (not copied (history-only entry point)) | history; the repo docs hold the record |
| resume-2026-09-22-pm | RECORD ONLY (not copied (history-only entry point)) | the resume file it names is in the private repo |
| resume-2026-09-24 | RECORD ONLY (not copied (history-only entry point)) | history |
| resume-2026-09-26-handoff | RECORD ONLY (not copied (history-only entry point)) | half U251; the spine half points at RESUME_2026-09-22_PM.md |
| selective-prediction-the-honest-99 | LEAKED (LEAKED) | the arithmetic (about 298 answered cases to certify 99 %) stands (E.9); the numbers are on the leaked v2 bank and its own test half (C1.8); no clean re-run exists (OPEN_QUESTIONS C13) |
| six-figure-paper-plan | live (PARTLY SUPERSEDED (Figure 6 moved to paper 2)) | the finish-line rule |
| two-mechanisms-thesis | SUPERSEDED (SUPERSEDED numbers) | the framing governs paper 1; its numbers are the v2-lineage run (C1.18, A3.11): current 601/617 = 97.4 % whole lateral (A3.1), 451/603 = 74.8 % one body (A3.3) |
| xr-benchmark-and-robustness-2026-09-13 | RECORD ONLY (RECORD ONLY [WRONG-BANK]) | the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; OPEN_QUESTIONS F5) |
| zenodo-deposit | live (PARTLY SUPERSEDED) | says v10 is current; four documents give v11 = 10.5281/zenodo.22797014 published 2026-09-18 (MANUSCRIPTS section 20 C1); names ~/.zenodo_token (a file name, no value) |

## Best files, in the order a builder should open them

1. `HANDOFF/context/INDEX.md` (25.9 KB): the 141 notes with status and replacement; cut every project MEMORY.md from it.
2. `HANDOFF/RESULTS_CATALOG.md` (110 KB): every result with id, file, status and rigor mark; STATUS.md of every project is a filtered copy of its parts.
3. `HANDOFF/OPEN_QUESTIONS.md` (28.5 KB) and `HANDOFF/RESEARCH_DIRECTIONS.md` (134 KB): TODO.md of every project comes from parts A-G and from PAR-1..6, FLU-1..2, CT-1..11, DAT-1, PUB-1 with their gates and n.
4. `HANDOFF/RECIPES.md` (73.6 KB): how each deliverable is regenerated; section 0 before any recipe.
5. `HANDOFF/README.md` section 5 and `INFRASTRUCTURE.md` section 10: the standing rules each CLAUDE.md must restate.
6. `HANDOFF/MANUSCRIPTS.md` section 19 (Desktop classification): the disposition source for `_plan/`.
7. `HANDOFF/working_notes/topic1..6` (59-97 KB each): the full tables behind the catalog, with every contradiction; keep in the project that owns the topic.

## What a reader would lose if the memory folder were dropped

Nothing numeric that is quotable: every current number is in a result file and in `RESULTS_CATALOG.md`. What would be lost is the reasoning record: why each defect was found (rendering, an outside reference), the traps that cost days (two label maps, id 29, P-I-R volumes, raw SPINEPS ids, the row-spacing defect, the login-node bans, bash 4.2), Greg's verbatim directives with their dates (D1-D9, the LSTV/TLTV determination, the two-mechanisms framing, submit-and-sleep, the no-keys rule for Beethoven), and the dormant lines that must not be repeated (FluoroCap as training data, FluoroGen img2img, STC loss, CycleGAN translation, bespoke CT warps). The six history-only resume notes point at repo documents (`ssn:docs/RESUME_2026-09-22_PM.md`, `docs/HANDOFF_2026-09-21_PM.md`, `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`) that hold the actual checkpoints; the notes themselves can be referenced, not copied.

## Unknowns

- Whether Greg wants the `grid_access_students` folder to carry the six Beethoven notes at all: in the handoff they are Greg-only, and the task lists Beethoven as a project family. This inventory marks them `redacted copy required` and leaves the decision to the builder of `_plan/`.
- Which notes INFRASTRUCTURE.md and README.md cite from `GREG_ONLY/context_beethoven/` by fact, so that a redacted copy keeps those facts: not checked line by line.
- The live `data-platform-migration-2026-10.md` content after 16:39 was not diffed against the HANDOFF copy; only the mtime shows it changed.
- `lab-recipe-and-board.md` and `README.md` section 10 name Ashley Schehr and Dr Tech; Ashley Schehr is a published co-author and, per the standing rule, a person never renamed; whether a project folder may name her is Greg's call (OPEN_QUESTIONS A30 covers only usernames, a staff contact and three e-mails).
- The `all` tag puts 22 standing-rule notes in every project folder; whether the builders prefer one shared `common/memory/` folder with links is a layout decision this inventory does not make.

## Flags

- The TSV has 12 columns, not 8: the four inventory-specific columns are appended after the standard eight.
- One `source_path` points at a HANDOFF copy instead of the live file on purpose (the splits note): the live file's name carries the banned word.
- Four live notes with student identifiers were not redacted by the HANDOFF copier (listed above); the HANDOFF `context/` copies of those four are unsafe to copy as they stand.
- The `learned-formation-refuted-calibrate-instead` note (redacted copy) still names a DMC neurosurgeon by name in its deliverables paragraph; the builder of `01_carm_detection/regulatory/` should decide whether that name travels.
- `panjabi-1991-page-892` names a copyrighted article scan on the repo root; reference by path, never copy into a repository.
- `fluorocap-pipeline-resume` and `ssn:CLAUDE.md` both run python on the login node, against the standing rule; carry the note with the correction.
