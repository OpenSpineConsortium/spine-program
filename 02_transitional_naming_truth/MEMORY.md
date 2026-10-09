# MEMORY: the notes in `memory/` and the status each one carries

31 notes, copied on 2026-10-08 from the redacted handoff copies (`HANDOFF/context/` of the private repository at
097933a), not from the live memory folder. The status column is the verbatim status of `HANDOFF/context/INDEX.md`
as built on 2026-10-08; the same status is the first line of each copy. The 22 "standing rule, every folder" notes
are in every project of `spine-program`; the 9 "transitional_fluoro cut list" notes are this folder's own
(the cut list is the last column of `MEMORY.md`; the plan states it in `../_plan/PLAN.md` section 3 "02", Families absorbed, "the 9 memory notes of the transitional cut list", under rules 2(a) and 5 of its section 2; `../_plan/DISPOSITION.tsv` rows 845 and 878 carry two of them as rows).

## The rules that govern these notes

- Each note is a dated record from the session that did the work, not an instruction. Where a note and a result
  file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win.
- Status words: CURRENT = still the state; DATED = a state at its date; PARTLY SUPERSEDED = part replaced by the
  thing named; SUPERSEDED = replaced by the number named; LEAKED = its numbers were measured on a bank with a known
  leak (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`); RECORD ONLY = history, not quotable; DORMANT =
  a line not being pursued.
- Notes that are never in this folder: the five Greg-only notes (commercial stance, disclosure scrub, the three
  credential-location notes), the seven U251 / LITT notes (another study), the six history-only resume notes, the
  six Beethoven notes (project 11), and the live `MEMORY.md` index. Notes of the other families (the C-arm
  programme's 48, the data platform's 28, and so on) live in their own folders; this folder quotes their numbers
  only through `docs/handoff/RESULTS_CATALOG.md`.

## The nine notes of this folder's own cut, and what each is for

| note | why it is here | caveat |
|---|---|---|
| `lstv-tltv-detection-goal` | Greg's standing determination of 2026-09-23: the goal sentence of this folder | its numbers (72.9 / 97.0 / 44.9 %) are the v2-lineage table (RC C1.18): quote the goal, not the numbers |
| `paper-split-2026-09-24` | the scope rule: LevelCheck and the surgeon comparison are paper 2; paper 1 scores no G3 transitional test person | CURRENT |
| `anomaly-harvest-directive` | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in the field | the binding directive behind the registry and the truth tiers |
| `spineps-ids-can-be-scrambled` | raw SPINEPS ids before 147428d; name through the ctd file; VERIDAH is a labeller, not truth; v8/v9 saw most G3 test people | the standing trap for every SPINEPS consumer |
| `fluorocap-prototype-and-lstv-arm` | the LSTV flag results (REFUTED as a flag), the FluoroCap arm, the scoping-review statistics, the two verification benches | DORMANT line; the flag numbers are in RC C1.12 |
| `lstv-data-landscape` | where LSTV / TLTV labels exist in the world; Kwak 2025, the one published 2-D LSTV model (76.4 % accuracy, AUC 0.84, 62.3 % positive rate: never benchmark against it on a balanced set) | DATED; redacted copy (three researcher e-mail addresses withheld) |
| `polypose-decision` | Greg's decision on synthesis: morphology augmentation only within published ranges of motion; fused junctions zero motion | CURRENT |
| `two-mechanisms-thesis` | the framing that governs paper 1 and the coupling step of this folder (morphology for the limited field, counting as the safety net) | SUPERSEDED numbers: current 601 / 617 = 97.4 % whole lateral, 451 / 603 = 74.8 % one body (RC A3.1, A3.3) |
| `feasibility-claims-measured` | the FOV feasibility report tested claim by claim; the head/encoder pairing trap; the Cina benchmark mandate | RECORD ONLY [LEAK]: never quote its numbers (49.9 %, 66.0 %, 91.8 %); its reading of the external report stands |

## The index (generated from `HANDOFF/context/INDEX.md`)

| note | one line | project | status (INDEX.md verbatim) | what replaces it, or why | why it is here |
|---|---|---|---|---|---|
| [`bash-heredoc-backslashes`](memory/bash-heredoc-backslashes.md) | heredocs collapse backslashes; write scripts with Write, run by path | PREF | CURRENT |  | standing rule, every folder |
| [`ct-volumes-are-pir-not-ras`](memory/ct-volumes-are-pir-not-ras.md) | volumes are (P,I,R) on disk; decide by reading the affine | CTSP | CURRENT |  | standing rule, every folder |
| [`data-directives-2026-09-23`](memory/data-directives-2026-09-23.md) | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | PREF / DATA | CURRENT |  | standing rule, every folder |
| [`figure-captions-terse`](memory/figure-captions-terse.md) | captions short, argument in text; float spacing | PREF | CURRENT |  | standing rule, every folder |
| [`fluorocap-repo-private`](memory/fluorocap-repo-private.md) | spinesurg private since 2026-09-14; never push level-ID code public | PREF | CURRENT |  | standing rule, every folder |
| [`grid-access`](memory/grid-access.md) | login, project root, where CTs and labels lived, ITK-SNAP launch | GRID | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) |  | standing rule, every folder |
| [`grid-bash-4-2-quoting`](memory/grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail | GRID | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; write grid jobs for bash 4.2 | standing rule, every folder |
| [`grid-ceph-volume-oschome`](memory/grid-ceph-volume-oschome.md) | 20 TB Ceph volume, working tree, `df-ceph oschome` | GRID | CURRENT |  | standing rule, every folder |
| [`grid-local-singularity-is-broken`](memory/grid-local-singularity-is-broken.md) | use conda singularity + pre-unpacked sandbox + specific bind | GRID | CURRENT |  | standing rule, every folder |
| [`key-patients-from-metadata-not-filenames`](memory/key-patients-from-metadata-not-filenames.md) | identity order: DICOM → manifest → ann fields → filename last | PREF / DATA | CURRENT |  | standing rule, every folder |
| [`label-scheme-v4-vs-ostk`](memory/label-scheme-v4-vs-ostk.md) | two live maps; `labels_for(volume)`; what the mix-up cost | CTSP / OSTK | CURRENT |  | standing rule, every folder |
| [`morphology-deformation-feasibility`](memory/morphology-deformation-feasibility.md) | literature first; no bespoke CT warp | PREF | CURRENT |  | standing rule, every folder |
| [`never-reorient-when-writing-labels`](memory/never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label | CTSP | CURRENT |  | standing rule, every folder |
| [`no-jobs-on-login-node`](memory/no-jobs-on-login-node.md) | every computation via sbatch; compute nodes have internet; C&IT addendum | GRID / PREF | CURRENT |  | standing rule, every folder |
| [`no-unexplained-subsets-fix-not-disclose`](memory/no-unexplained-subsets-fix-not-disclose.md) | use all of a dataset; describe each in prose; fix leaks, don't disclose | PREF | CURRENT |  | standing rule, every folder |
| [`scratchpad-shadows-stdlib`](memory/scratchpad-shadows-stdlib.md) | stdlib-named scratch scripts hijack Python | PREF | CURRENT |  | standing rule, every folder |
| [`submit-and-sleep-orchestration`](memory/submit-and-sleep-orchestration.md) | submit, estimate, record, stop | PREF | CURRENT |  | standing rule, every folder |
| [`user-affiliation-general-surgery`](memory/user-affiliation-general-surgery.md) | General Surgery, not Neurosurgery | PREF | CURRENT |  | standing rule, every folder |
| [`windows-junction-worktree-trap`](memory/windows-junction-worktree-trap.md) | worktree remove deletes junction targets | PREF | CURRENT |  | standing rule, every folder |
| [`writing-preferences`](memory/writing-preferences.md) | the banned word; no fractional versions | PREF | CURRENT |  | standing rule, every folder |
| [`wsl-for-network`](memory/wsl-for-network.md) | network commands via WSL | GRID / PREF | CURRENT |  | standing rule, every folder |
| [`wsu-library-access-cutoff`](memory/wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30 | REF | CURRENT |  | standing rule, every folder |
| [`anomaly-harvest-directive`](memory/anomaly-harvest-directive.md) | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in FOV | ANOM | CURRENT |  | transitional_fluoro cut list |
| [`feasibility-claims-measured`](memory/feasibility-claims-measured.md) | the FOV feasibility report tested claim by claim; head/encoder pairing trap | SN | RECORD ONLY [LEAK] | its accuracies are on v2 / v5 / v6 (C1.14, C1.16); its claim-by-claim reading of the external report still stands | transitional_fluoro cut list |
| [`fluorocap-prototype-and-lstv-arm`](memory/fluorocap-prototype-and-lstv-arm.md) | single-image prototype, transitional harvest arm, Semantic Scholar route | FC | DORMANT |  | transitional_fluoro cut list |
| [`lstv-data-landscape`](memory/lstv-data-landscape.md) | where LSTV/TLTV labels exist; the one published 2-D LSTV model | REF | DATED; redacted copy | three researcher e-mail addresses withheld here (full note in `GREG_ONLY/context/`) | transitional_fluoro cut list |
| [`lstv-tltv-detection-goal`](memory/lstv-tltv-detection-goal.md) | standing determination: detect LSTV/TLTV from C-arm exposures | SN | CURRENT |  | transitional_fluoro cut list |
| [`paper-split-2026-09-24`](memory/paper-split-2026-09-24.md) | LevelCheck/surgeon comparison is paper 2; paper 1 = five figures, no G3 transitional test person | SN | CURRENT |  | transitional_fluoro cut list |
| [`polypose-decision`](memory/polypose-decision.md) | morphology augmentation = PolyPose within published ROM; fused junctions zero motion | SN | CURRENT |  | transitional_fluoro cut list |
| [`spineps-ids-can-be-scrambled`](memory/spineps-ids-can-be-scrambled.md) | pre-147428d SPINEPS masks carry raw ids; guard `tools/spineps_ids.py`; VERIDAH not truth | DATA | CURRENT |  | transitional_fluoro cut list |
| [`two-mechanisms-thesis`](memory/two-mechanisms-thesis.md) | morphology for quick limited-FOV localisation; sweep/count as the safety net | SN | SUPERSEDED numbers | 98.2 % whole frame, 72.9 % one body and 44.9 % L6 are the v2-lineage run (C1.18, A3.11). Current: 601 / 617 = 97.4 % whole lateral frame (A3.1), 451 / 603 = 74.8 % one body in field (A3.3). The framing (morphology for limited fields, counting as the safety net) still governs paper 1 | transitional_fluoro cut list |
