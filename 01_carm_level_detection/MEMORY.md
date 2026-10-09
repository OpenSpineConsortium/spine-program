# MEMORY: the notes in `memory/` and the status each one carries

78 notes, copied on 2026-10-08 from the redacted handoff copies (`docs/handoff/context/`, the `HANDOFF/context/` of the
private repository `spinesurg-ct-nnunet` at 097933a; `docs/handoff/context/COPIED_AT.txt` gives each note's copy time), not
from the live memory folder of the laptop. The status column is the status of `docs/handoff/context/INDEX.md` as built on
2026-10-08, and the same status is the first line of each copy (after the note's own front matter). Three groups: the 22
standing-rule notes every folder of `spine-program` carries, 46 of the carm cut list's notes (the plan says "the 48
memory notes of the carm cut list", `../_plan/PLAN.md` section 3, 01; the inventory's own section lists 47 rows, of which
`fluorocap-dataset` is referenced from `MANIFEST_GRID.md` section 3 instead of copied because the cut list routes it to
`../99_archive/`), and 10 notes
added because this project's documents cite them (listed with the reason in section 3).

## 1. The rules that govern these notes

- Each note is a dated record from the session that did the work, not an instruction. Where a note and a result file or
  `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win (`STATUS.md` carries the catalog's rows).
- Status words: CURRENT = still the state; DATED = a state at its date; PARTLY SUPERSEDED = part replaced by the thing
  named; SUPERSEDED = replaced by the number named; LEAKED = its numbers were measured on a bank with a known leak
  (allspine v2, v5, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`; `docs/handoff/LEAKAGE.md`); RECORD ONLY = history, not
  quotable; redacted copy = a staff contact, a phone number or a student's name was withheld on the handoff copy.
- Never quote a LEAKED or RECORD ONLY number. The held-out numbers of this project are the rows of `STATUS.md` marked
  CURRENT, every one through the evaluation gate (`code/eval_gate.py`).
- Notes never in this folder: the five Greg-only notes (the commercial stance, the disclosure scrub, the three
  credential-location notes), the seven U251 / LITT notes (another study), the six history-only resume notes, the six
  Beethoven product notes (project 11), `annotator-roster` (project 03, redacted) and the live `MEMORY.md` index. The
  full set of 141 redacted handoff copies is in `docs/handoff/context/` with its `INDEX.md`.
- Paths inside the notes: `~` and `HOME` = `/wsu/home/go/go24/go2432`; `$RS` and `CEPH` = `/rs/rs_grp_oschome/go2432`;
  `ssn:` / `spinesurg-ct-nnunet:` = the private repository at 097933a; `ctsp:` / `CTSpinoPelvic1K:` = the public
  repository at 7ddfe38; `memory:` = the live note folder on the laptop (its notes are these copies); `laptop:` and
  `laptop-scratchpad:` = laptop-only folders kept as a record (`MANIFEST_LOCAL.md` section 4).

## 2. The 46 notes of the carm cut list, and what each is for

Digest and caveat are the cut list's (`../_plan/` inventory `memory_and_handoff_map.md`, section "01 carm_detection");
the status is `INDEX.md`'s.

| note | status (INDEX.md) | digest | caveat |
|---|---|---|---|
| `acquisition-space-saturation` | CURRENT | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); the claim wording | current finding behind Figure 5 |
| `anomaly-rule-rc22-evaluated` | CURRENT | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | removed from the manuscript on Greg's order (D.24) |
| `carm-plateau-is-the-denominator` | CURRENT | same-device 82-85 % plateau is the truth denominator; clean subset 96.9 % | RESULTS_CATALOG A8.7 uses 214 / 95.6 % from the repair tool; the note's 204 / 96.9 % is a different rule |
| `carmlspine-level-experiment` | CURRENT | C-ArmLSpine (148 cases, AP+LAT+CBCT): reading traps, pose convention, pipeline | its 2026-09-21 numbers (96.3 / 37.9 / 98.2) are the v2-lineage run; current numbers are A2 and A3 |
| `chart-preferences` | CURRENT | slides: no sideways bars, donuts/lines, published background figures, big type | slide preference for any talk |
| `data-audit-99-gaps` | DATED | 99 gaps in docs/DATA_COMPLETENESS_AUDIT.md; the ones that change the science | the audit list that gates final training (the D-rows) |
| `detection-is-the-binding-constraint` | CURRENT | counting fails on detection (60 points) not linking (11-28) | the finding that orders the C-arm work |
| `drr-row-spacing-defect` | CURRENT | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | why only sweep_v3 counts |
| `figure-preferences-schwingnet` | PARTLY SUPERSEDED (five-figure paper 1, mem:paper-split-2026-09-24.md) | Greg's figure verdicts for the SchwingNet manuscript (2026-09-22) | taste record for any new figure |
| `film-fluoro-boundary-not-transferable` | CURRENT | devices separate pairwise; film vs fluoroscopy does not transfer to an unseen corpus | the manifold finding (A13) |
| `film-ncurve-ablation-result` | SUPERSEDED reading | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | trust sn:results/coverage/film_ncurve/ablation/READ.md: 7 of 9 cells separated, six help and one hurts (A10.6-A10.10) |
| `flagship-paper-frame` | PARTLY SUPERSEDED (LevelCheck comparison moved to paper 2) | ships a network; claims ledger; PENDING macros | the five contributions and the ledger rule |
| `flagship-program` | DATED | gates G0-G7 in docs/FLAGSHIP_PLAN.md | which gates are formally closed is not written in one place (RESEARCH_DIRECTIONS unknown 13); pipeline_state.py on the grid is the authority |
| `fluorocap-is-reproductions-not-fluoroscopy` | CURRENT (the reason FC is out of training) | 72.8 % of panels have zero pixel residual; test set only | why FluoroCap is excluded |
| `fluorocap-pipeline-resume` | CURRENT | start at docs/PIPELINE_RESUME.md and tools/pipeline_state.py; add every stage there | its ssh line runs python on the login node, which the login-node rule forbids (OPEN_QUESTIONS F10): run it as a job |
| `grid-quota-and-deleted-banks` | CURRENT | pan_quota; banks deleted 2026-09-20; holdout.py raises; refs repointed to v7 | why v2-v5c banks are gone and what that broke |
| `guided-acquisition-loop` | DATED | commanded displacement + digital fiducial; what must not be quoted | references docs/provisional and INVENTION_DISCLOSURE in the private repo; corpus result of job 40376577 NOT RECORDED (C3.12) |
| `identity-audit-findings` | CURRENT | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case is not a person | the patient-identity spec summary |
| `k-devices-one-network` | CURRENT | per-device parameter sets, styled renders, LODO; where the pipeline lives | the device pipeline map |
| `learned-formation-refuted-calibrate-instead` | CURRENT; redacted copy | CT to fluoro formation calibrated on DeepFluoro; first real-fluoro recall; the 2026-09-21 deliverables (IRB protocol draft, seed-grant draft, phantom plan, TL;DR) | copy the HANDOFF/context version (one staff contact withheld); 18.9 KB; names a DMC neurosurgeon: keep that redacted too; the IRB and grant drafts exist only in a scratchpad and as claude.ai artifacts |
| `level-service-serving` | CURRENT | website never serves weights; service + private HF weights | standing serving rule |
| `local-level-identity-thesis` | CURRENT | name a vertebra by local morphology instead of counting from C2 | the thesis sentence of the programme |
| `lstv-tltv-detection-goal` | CURRENT | standing determination: detect LSTV/TLTV from C-arm exposures | its numbers (72.9 / 97.0 / 44.9) are the v2-lineage table (C1.18) |
| `mixed-length-head-and-sota` | LEAKED | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | do not quote 97.47 or 99.02; held-out film naming today is the film N-curve (A10.1-A10.3) |
| `model-registry` | CURRENT | content-addressed weights store, ledger, MLflow, HF mirror | whether ~/model_registry survived the migration is OPEN_QUESTIONS B31 |
| `oblique-angles-and-sweep-vision` | CURRENT | detector must work at any angle; synthetic AP to lateral arcs; AR vision is preview only | pose-pool rule and the case134 spin |
| `paper-split-2026-09-24` | CURRENT | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | the scope rule of paper 1 and paper 2 |
| `pooled-vs-lodo-device-designs` | CURRENT | pooled and LODO both reported; list builder refuses split subjects | design rule for device arms |
| `recurrent-head-restored-2026-09-16` | DATED | BiGRU head was unreachable; restored, +10 points on the 27-class bank | the head's 99 % was on a cervical-dominated bank (CONTEXT_EXPORT section 3) |
| `registration-free-prior-art` | CURRENT | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | three unread IEEE papers could overturn the naming claim (RESEARCH_DIRECTIONS unknown 11) |
| `rigor-audit-findings` | DATED | selective reporting in two places, interval-free detector figure, one CI in 54 claims | the fix list answered item by item in sn:results/RIGOR_FIXES.md |
| `rsnai-author-instructions` | CURRENT | Radiology AI limits | submission limits |
| `rsnai-paper-endpoint` | DATED (see schwingnet-manuscript, paper-split) | one concise RSNA AI manuscript paper/rsnai/main_v2.tex; checklist docs/RSNAI_PLAN.md; citation traps | main_v2.tex is superseded by SchwingNet/main.tex; the citation traps stand |
| `schwingnet-manuscript` | CURRENT | SchwingNet/ manuscript built only from rigor-passing numbers; CLAIM map, ATLAS cards | copy the HANDOFF/context version: it substitutes the banned word where the note states the rule |
| `selective-prediction-the-honest-99` | LEAKED | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | the arithmetic (about 298 answered cases to certify 99 %) stands (E.9); the numbers are on the leaked v2 bank and its own test half (C1.8); no clean re-run exists (OPEN_QUESTIONS C13) |
| `six-figure-paper-plan` | PARTLY SUPERSEDED (Figure 6 moved to paper 2) | six figures; LevelCheck pre-specified, never tuned | the finish-line rule |
| `spine-data-review-and-ts-bench` | DATED | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the PRISMA-ScR scoping review | the SPINEPS stores it built carry raw ids; the TS bench is inside the v9 bank |
| `split-leak-cross-naming` | CURRENT | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | leak record and the bank-building rule |
| `stc-does-not-transfer` | CURRENT | Star Temporal Classification loses to cross-entropy on naming | refuted loss; do not revisit (C1.7) |
| `sweep-map-replaces-registration` | CURRENT | overlapping frames build a radiograph-only registration; sweep_v3 numbers | the TS-bench numbers are held out only for the v7-lineage encoder (ts-bench-inside-v9-bank) |
| `sweep-physics-no-bone` | CURRENT | physics-perturbed sweeps rendered with no bone; fix --paths2-only | its causal claim is superseded by physics-three-defects-measured |
| `synthetic-real-ratio-evidence` | CURRENT | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | the project's own ratio was never swept (A10.11; OPEN_QUESTIONS A9) |
| `tables-black-not-colour` | CURRENT | matrix tables black + one outlined mark | table style rule |
| `ts-bench-inside-v9-bank` | CURRENT | TS render bench is not held out from the v9 encoder (70 TS + 1 CTSP + 0 VerSe renders unseen) | held-out rule for v9-lineage models |
| `two-mechanisms-thesis` | SUPERSEDED numbers | morphology for quick limited-FOV localisation; sweep/count as the safety net | the framing governs paper 1; its numbers are the v2-lineage run (C1.18, A3.11): current 601/617 = 97.4 % whole lateral (A3.1), 451/603 = 74.8 % one body (A3.3) |
| `xray-corner-detector-status` | DATED | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | names a student by first name; the HANDOFF copy is unredacted: redact before copying |

Not copied from the cut list: `fluorocap-dataset` (DORMANT; the FluoroCap test set on the grid, `~/FluoroCap`: stages,
routes, manifest). The cut list routes it to `../99_archive/memory/` and has this project reference it; its grid rows are
in `MANIFEST_GRID.md` section 3 and the reason FluoroCap is out of training is `fluorocap-is-reproductions-not-fluoroscopy`.

## 3. The 10 notes added for this project

| note | status (INDEX.md) | why it is here |
|---|---|---|
| `deepfluoro-convention` | CURRENT | the (z,y,x) HU volume and signed-focal convention every DeepFluoro number of this project depends on (`STATUS.md` section 6); without it a re-projection is silently mirrored |
| `device-sampling-audit` | CURRENT | the card clip saturates (A12.6): the open defect behind any styled-render arm S3 might choose after the device census |
| `drr-to-fluoro-levers` | CURRENT | the three measured levers for render-to-fluoroscopy transfer and the refuted CycleGAN / ADDA route (RD 2.2): what not to rebuild if the hospital device transfers badly |
| `engine-swap-architecture` | DATED | the `metrics.json` contract the website client (`../12_website_pacs_demo/`) consumes; S2 keeps the schema when the engine behind `code/service/` changes |
| `feasibility-claims-measured` | RECORD ONLY [LEAK] | the claim-by-claim reading of the external FOV feasibility report (`docs/external_reports/Feasibility_FOV_2026-09-17.docx`) stands; its numbers are RECORD ONLY [LEAK] |
| `level-id-2d-results-2026-09-13` | RECORD ONLY | the first real-film numbers and the trap that produced them (a cervical-dominated bank); RECORD ONLY, kept so the 96.7 % is never quoted again |
| `level-model-bank-coverage` | DATED | why the deployed bank held only cervical and lumbar films; the 14-class 99 % and why the service's older release (`code/service/`) cannot be quoted |
| `pacs-demo-and-ostk-params` | CURRENT | the website's PACS demo and `level-id.openspineconsortium.org`, the only public surface of the service; `MANIFEST_CODE.md` section 5 |
| `physics-three-defects-measured` | CURRENT | only the AEC extrapolation changed an image; closes the physics-linking line (`docs/PHYSICS_LINKING.md`, `results/physics/`) that `sweep-physics-no-bone` opened |
| `remedies-refuted-2026-09-17` | LEAKED numbers | pretrain-on-DRR, film-noise, anchored-only and CReST all lose: LEAKED numbers, not re-run on v9 (RD unknown 24); kept so none is rebuilt as if new |

## 4. The 22 standing-rule notes every folder carries

| note | status (INDEX.md) | one line |
|---|---|---|
| `bash-heredoc-backslashes` | CURRENT | heredocs collapse backslashes; write scripts with Write, run by path |
| `ct-volumes-are-pir-not-ras` | CURRENT | volumes are (P,I,R) on disk; decide by reading the affine |
| `data-directives-2026-09-23` | CURRENT | D1-D9: fix or justify every truncation; FluoroCap dropped; use all |
| `figure-captions-terse` | CURRENT | captions short, argument in text; float spacing |
| `fluorocap-repo-private` | CURRENT | spinesurg private since 2026-09-14; never push level-ID code public |
| `grid-access` | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) | login, project root, where CTs and labels lived, ITK-SNAP launch |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail |
| `grid-ceph-volume-oschome` | CURRENT | 20 TB Ceph volume, working tree, `df-ceph oschome` |
| `grid-local-singularity-is-broken` | CURRENT | use conda singularity + pre-unpacked sandbox + specific bind |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM → manifest → ann fields → filename last |
| `label-scheme-v4-vs-ostk` | CURRENT | two live maps; `labels_for(volume)`; what the mix-up cost |
| `morphology-deformation-feasibility` | CURRENT | literature first; no bespoke CT warp |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label |
| `no-jobs-on-login-node` | CURRENT | every computation via sbatch; compute nodes have internet; C&IT addendum |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a dataset; describe each in prose; fix leaks, don't disclose |
| `scratchpad-shadows-stdlib` | CURRENT | stdlib-named scratch scripts hijack Python |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate, record, stop |
| `user-affiliation-general-surgery` | CURRENT | General Surgery, not Neurosurgery |
| `windows-junction-worktree-trap` | CURRENT | worktree remove deletes junction targets |
| `writing-preferences` | CURRENT | the banned word; no fractional versions |
| `wsl-for-network` | CURRENT | network commands via WSL |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents 2026-06-30 |

## 5. The index of all 78 notes (from `docs/handoff/context/INDEX.md`, 2026-10-08)

| note | one line | project tag | status | what replaces it, or why |
|---|---|---|---|---|
| [`acquisition-space-saturation`](memory/acquisition-space-saturation.md) | fluoroscopy plateau follows where frames sit in acquisition space, not N (tested 2026-09-25, Figure 5 b-d); claim wording | SN | CURRENT |  |
| [`anomaly-rule-rc22-evaluated`](memory/anomaly-rule-rc22-evaluated.md) | R+C=22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | ANOM | CURRENT |  |
| [`bash-heredoc-backslashes`](memory/bash-heredoc-backslashes.md) | heredocs collapse backslashes; write scripts with Write, run by path | PREF | CURRENT |  |
| [`carm-plateau-is-the-denominator`](memory/carm-plateau-is-the-denominator.md) | same-device 82-85 % plateau is the truth denominator; clean subset 96.9 % | SN | CURRENT |  |
| [`carmlspine-level-experiment`](memory/carmlspine-level-experiment.md) | C-ArmLSpine (148 cases, AP+LAT+CBCT): reading traps, pose convention, pipeline | SN | CURRENT |  |
| [`chart-preferences`](memory/chart-preferences.md) | slides: no sideways bars, donuts/lines, published background figures, big type | PREF | CURRENT |  |
| [`ct-volumes-are-pir-not-ras`](memory/ct-volumes-are-pir-not-ras.md) | volumes are (P,I,R) on disk; decide by reading the affine | CTSP | CURRENT |  |
| [`data-audit-99-gaps`](memory/data-audit-99-gaps.md) | 99 gaps in `docs/DATA_COMPLETENESS_AUDIT.md`; the ones that change the science | DATA | DATED |  |
| [`data-directives-2026-09-23`](memory/data-directives-2026-09-23.md) | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | PREF / DATA | CURRENT |  |
| [`deepfluoro-convention`](memory/deepfluoro-convention.md) | DeepFluoro file layout and projection convention (0.00 px reprojection) | REF / SN | CURRENT |  |
| [`detection-is-the-binding-constraint`](memory/detection-is-the-binding-constraint.md) | counting fails on detection (60 points) not linking (11-28) | SN | CURRENT |  |
| [`device-sampling-audit`](memory/device-sampling-audit.md) | card clip saturates (95-98 % of the joint lost); typicality gate | SN | CURRENT |  |
| [`drr-row-spacing-defect`](memory/drr-row-spacing-defect.md) | A-P voxel size written as S-I row spacing; pre-sweep_v3 sweeps on the wrong field size | SN | CURRENT |  |
| [`drr-to-fluoro-levers`](memory/drr-to-fluoro-levers.md) | three measured levers for DRR→fluoro; CycleGAN/ADDA refuted; honest ceiling | REF / SN | CURRENT |  |
| [`engine-swap-architecture`](memory/engine-swap-architecture.md) | demo consumes a `metrics.json` contract so the engine can be swapped | WEB | DATED |  |
| [`feasibility-claims-measured`](memory/feasibility-claims-measured.md) | the FOV feasibility report tested claim by claim; head/encoder pairing trap | SN | RECORD ONLY [LEAK] | its accuracies are on v2 / v5 / v6 (C1.14, C1.16); its claim-by-claim reading of the external report still stands |
| [`figure-captions-terse`](memory/figure-captions-terse.md) | captions short, argument in text; float spacing | PREF | CURRENT |  |
| [`figure-preferences-schwingnet`](memory/figure-preferences-schwingnet.md) | Greg's figure verdicts for the SchwingNet manuscript (2026-09-22) | PREF / SN | PARTLY SUPERSEDED (five-figure paper 1, mem:paper-split-2026-09-24.md) |  |
| [`film-fluoro-boundary-not-transferable`](memory/film-fluoro-boundary-not-transferable.md) | devices separate pairwise; film vs fluoro does not transfer to an unseen corpus | SN | CURRENT |  |
| [`film-ncurve-ablation-result`](memory/film-ncurve-ablation-result.md) | CT renders raise ordinary-level film naming +6 to +22 points at 5-25 persons | SN | SUPERSEDED reading | all help is outdated: the tool's `sn:results/coverage/film_ncurve/ablation/READ.md` shows 7 of 9 cells separated, six help and one hurts (BUU at every person) (A10.6-A10.9); its "from 100 persons the arms overlap" holds at 100 and 200 persons, not at every person (A10.10) |
| [`flagship-paper-frame`](memory/flagship-paper-frame.md) | ships a network; claims ledger; `\PENDING` macros | SN | PARTLY SUPERSEDED (LevelCheck comparison moved to paper 2) |  |
| [`flagship-program`](memory/flagship-program.md) | gates G0-G7 in `docs/FLAGSHIP_PLAN.md` | SN | DATED |  |
| [`fluorocap-is-reproductions-not-fluoroscopy`](memory/fluorocap-is-reproductions-not-fluoroscopy.md) | 72.8 % of panels have zero pixel residual; test set only | FC | CURRENT (the reason FC is out of training) |  |
| [`fluorocap-pipeline-resume`](memory/fluorocap-pipeline-resume.md) | start at `docs/PIPELINE_RESUME.md` and `tools/pipeline_state.py`; add every stage there (not in MEMORY.md index) | SN | CURRENT |  |
| [`fluorocap-repo-private`](memory/fluorocap-repo-private.md) | spinesurg private since 2026-09-14; never push level-ID code public | PREF | CURRENT |  |
| [`grid-access`](memory/grid-access.md) | login, project root, where CTs and labels lived, ITK-SNAP launch | GRID | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) |  |
| [`grid-bash-4-2-quoting`](memory/grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail | GRID | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; write grid jobs for bash 4.2 |
| [`grid-ceph-volume-oschome`](memory/grid-ceph-volume-oschome.md) | 20 TB Ceph volume, working tree, `df-ceph oschome` | GRID | CURRENT |  |
| [`grid-local-singularity-is-broken`](memory/grid-local-singularity-is-broken.md) | use conda singularity + pre-unpacked sandbox + specific bind | GRID | CURRENT |  |
| [`grid-quota-and-deleted-banks`](memory/grid-quota-and-deleted-banks.md) | `pan_quota`; banks deleted 2026-09-20; `holdout.py` raises; refs → v7 | GRID | CURRENT |  |
| [`guided-acquisition-loop`](memory/guided-acquisition-loop.md) | commanded displacement + digital fiducial; what must not be quoted | SN | DATED |  |
| [`identity-audit-findings`](memory/identity-audit-findings.md) | prone/supine ruled out; TS renumber; three leaks; C-ArmLSpine case ≠ person | DATA | CURRENT |  |
| [`k-devices-one-network`](memory/k-devices-one-network.md) | per-device parameter sets, styled renders, LODO; where the pipeline lives | SN | CURRENT |  |
| [`key-patients-from-metadata-not-filenames`](memory/key-patients-from-metadata-not-filenames.md) | identity order: DICOM → manifest → ann fields → filename last | PREF / DATA | CURRENT |  |
| [`label-scheme-v4-vs-ostk`](memory/label-scheme-v4-vs-ostk.md) | two live maps; `labels_for(volume)`; what the mix-up cost | CTSP / OSTK | CURRENT |  |
| [`learned-formation-refuted-calibrate-instead`](memory/learned-formation-refuted-calibrate-instead.md) | CT→fluoro formation calibrated on DeepFluoro; first real-fluoro recall | SN | CURRENT; redacted copy | one staff contact withheld here (full note in `GREG_ONLY/context/`) |
| [`level-id-2d-results-2026-09-13`](memory/level-id-2d-results-2026-09-13.md) | 2-D level ID on real films, 13 Sep results | SN | RECORD ONLY | the 96.7 % single-crop number is on the cervical-dominated `films_ann` bank (C1.1) |
| [`level-model-bank-coverage`](memory/level-model-bank-coverage.md) | the deployed bank held only cervical and lumbar films | SN | DATED |  |
| [`level-service-serving`](memory/level-service-serving.md) | website never serves weights; service + private HF weights | PREF / WEB | CURRENT |  |
| [`local-level-identity-thesis`](memory/local-level-identity-thesis.md) | name a vertebra by local morphology instead of counting from C2 | SN / CTSP | CURRENT |  |
| [`lstv-tltv-detection-goal`](memory/lstv-tltv-detection-goal.md) | standing determination: detect LSTV/TLTV from C-arm exposures | SN | CURRENT |  |
| [`mixed-length-head-and-sota`](memory/mixed-length-head-and-sota.md) | mixed band lengths +3.8 points at 3 vertebrae; no metric-comparable published number | SN | LEAKED | its numbers (97.47 % at 3 vertebrae, the "shortcut-free" 99.02 %) are on allspine v2, which pooled NHANES II twice (`RESULTS_CATALOG.md` C1.6); do not follow its "quote 99.02 %". Held-out film naming today: the film N-curve at every person, CSXA 99.8 %, BUU 96.9 %, NHANES 92.7 % (A10.1-A10.3) |
| [`model-registry`](memory/model-registry.md) | content-addressed weights store, ledger, MLflow, HF mirror | GRID / SN | CURRENT |  |
| [`morphology-deformation-feasibility`](memory/morphology-deformation-feasibility.md) | literature first; no bespoke CT warp | PREF | CURRENT |  |
| [`never-reorient-when-writing-labels`](memory/never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label | CTSP | CURRENT |  |
| [`no-jobs-on-login-node`](memory/no-jobs-on-login-node.md) | every computation via sbatch; compute nodes have internet; C&IT addendum | GRID / PREF | CURRENT |  |
| [`no-unexplained-subsets-fix-not-disclose`](memory/no-unexplained-subsets-fix-not-disclose.md) | use all of a dataset; describe each in prose; fix leaks, don't disclose | PREF | CURRENT |  |
| [`oblique-angles-and-sweep-vision`](memory/oblique-angles-and-sweep-vision.md) | detector must work at any angle; synthetic AP→lateral arcs; AR vision is preview only | SN | CURRENT |  |
| [`pacs-demo-and-ostk-params`](memory/pacs-demo-and-ostk-params.md) | ostk parameters and CLI; NiiVue PACS demo; no blanket SVA/TPA claim | OSTK / WEB | CURRENT |  |
| [`paper-split-2026-09-24`](memory/paper-split-2026-09-24.md) | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | SN | CURRENT |  |
| [`physics-three-defects-measured`](memory/physics-three-defects-measured.md) | only the AEC defect changed an image; the display window hides the lateral spine | SN | CURRENT |  |
| [`pooled-vs-lodo-device-designs`](memory/pooled-vs-lodo-device-designs.md) | pooled and LODO both reported; list builder refuses split subjects | SN | CURRENT |  |
| [`recurrent-head-restored-2026-09-16`](memory/recurrent-head-restored-2026-09-16.md) | BiGRU head was unreachable; restored, +10 points on the 27-class bank | SN | DATED | the head's 99 % was on a cervical-dominated bank (`CONTEXT_EXPORT.md` §3) |
| [`registration-free-prior-art`](memory/registration-free-prior-art.md) | published C-arm detection recall 0.96-0.98; naming peaks at 73.3 % | REF | CURRENT |  |
| [`remedies-refuted-2026-09-17`](memory/remedies-refuted-2026-09-17.md) | pretrain-on-DRR, film-noise, anchored-only, CReST admission all lose | SN | LEAKED numbers | the scaling curve it quotes is the v2 sweep (C2.1, SUPERSEDED [LEAK] [SEL-SPLIT]); the refutations were not re-run on v9 |
| [`rigor-audit-findings`](memory/rigor-audit-findings.md) | selective reporting in two places, uninterval'd detector figure, one CI in 54 claims | SN | DATED |  |
| [`rsnai-author-instructions`](memory/rsnai-author-instructions.md) | Radiology AI limits | REF / SN | CURRENT |  |
| [`rsnai-paper-endpoint`](memory/rsnai-paper-endpoint.md) | one concise RSNA AI manuscript `paper/rsnai/main_v2.tex`; checklist `docs/RSNAI_PLAN.md` | SN | DATED (see schwingnet-manuscript, paper-split) |  |
| [`schwingnet-manuscript`](memory/schwingnet-manuscript.md) | `SchwingNet/` manuscript built only from rigor-passing numbers; CLAIM map, ATLAS cards | SN | CURRENT |  |
| [`scratchpad-shadows-stdlib`](memory/scratchpad-shadows-stdlib.md) | stdlib-named scratch scripts hijack Python | PREF | CURRENT |  |
| [`selective-prediction-the-honest-99`](memory/selective-prediction-the-honest-99.md) | 99 % as a coverage claim (35.7 % / 55.7 % coverage) | SN | LEAKED | the 99 % at 35.7 % / 55.7 % coverage is on the leaked v2 bank, computed on its own test half (C1.8; `LEAKAGE.md` §5.1); no clean re-run exists (`OPEN_QUESTIONS.md` C13). Its arithmetic (about 298 answered cases to certify 99 %) still holds (E.9) |
| [`six-figure-paper-plan`](memory/six-figure-paper-plan.md) | six figures; LevelCheck pre-specified, never tuned | SN | PARTLY SUPERSEDED (Figure 6 moved to paper 2) |  |
| [`spine-data-review-and-ts-bench`](memory/spine-data-review-and-ts-bench.md) | TS render bench, SPINEPS+VERIDAH over TS+VerSe, the scoping review | SN / DATA | DATED |  |
| [`split-leak-cross-naming`](memory/split-leak-cross-naming.md) | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | DATA | CURRENT |  |
| [`stc-does-not-transfer`](memory/stc-does-not-transfer.md) | Star Temporal Classification loses to cross-entropy on naming | SN | CURRENT |  |
| [`submit-and-sleep-orchestration`](memory/submit-and-sleep-orchestration.md) | submit, estimate, record, stop | PREF | CURRENT |  |
| [`sweep-map-replaces-registration`](memory/sweep-map-replaces-registration.md) | overlapping frames build a radiograph-only registration; sweep_v3 numbers | SN | CURRENT |  |
| [`sweep-physics-no-bone`](memory/sweep-physics-no-bone.md) | physics-perturbed sweeps rendered with no bone; fix `--paths2-only` | SN | CURRENT |  |
| [`synthetic-real-ratio-evidence`](memory/synthetic-real-ratio-evidence.md) | no DRR paper swept the ratio; adjacent sweeps flatten at 4:1-10:1 | REF | CURRENT |  |
| [`tables-black-not-colour`](memory/tables-black-not-colour.md) | matrix tables black + one outlined mark | PREF | CURRENT |  |
| [`ts-bench-inside-v9-bank`](memory/ts-bench-inside-v9-bank.md) | TS render bench is not held out from the v9 encoder | DATA / SN | CURRENT |  |
| [`two-mechanisms-thesis`](memory/two-mechanisms-thesis.md) | morphology for quick limited-FOV localisation; sweep/count as the safety net | SN | SUPERSEDED numbers | 98.2 % whole frame, 72.9 % one body and 44.9 % L6 are the v2-lineage run (C1.18, A3.11). Current: 601 / 617 = 97.4 % whole lateral frame (A3.1), 451 / 603 = 74.8 % one body in field (A3.3). The framing (morphology for limited fields, counting as the safety net) still governs paper 1 |
| [`user-affiliation-general-surgery`](memory/user-affiliation-general-surgery.md) | General Surgery, not Neurosurgery | PREF | CURRENT |  |
| [`windows-junction-worktree-trap`](memory/windows-junction-worktree-trap.md) | worktree remove deletes junction targets | PREF | CURRENT |  |
| [`writing-preferences`](memory/writing-preferences.md) | the banned word; no fractional versions | PREF | CURRENT |  |
| [`wsl-for-network`](memory/wsl-for-network.md) | network commands via WSL | GRID / PREF | CURRENT |  |
| [`wsu-library-access-cutoff`](memory/wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30 | REF | CURRENT |  |
| [`xray-corner-detector-status`](memory/xray-corner-detector-status.md) | spine-detector corpus 33,943 instances; detect_v2 AP50 0.970 | SN | DATED |  |

Project tags are `INDEX.md`'s: SN = SchwingNet and the C-arm line, FC = FluoroCap, DATA = the data platform, GRID = grid
operations, CTSP / OSTK = the dataset and the toolkit, ANOM = the transitional census, WEB = the website, PREF = Greg's
standing preferences, REF = reference material.

## 6. Where the statuses came from and how to refresh them

`docs/handoff/context/INDEX.md` was built by `code/handoff_builders/build_context_index.py` from the notes in the handoff
folder and the digest of `docs/handoff/CONTEXT_EXPORT.md` section 3, with the statuses corrected by the 2026-10-08
verification. A later session that changes a note's status edits the first line of the copy here and the row in
section 5; the builders expect the repository layout (`HANDOFF/` and the live memory folder) and are kept as a record of
how the index was made, not as a tool this folder runs.

