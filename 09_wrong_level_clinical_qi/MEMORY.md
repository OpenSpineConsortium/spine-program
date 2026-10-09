# MEMORY: the notes this project carries

`memory/` holds 23 notes copied on 2026-10-08 from `spinesurg-ct-nnunet` 097933a `HANDOFF/context/` (the redacted
copies with statuses), not from the live memory folder. Twenty-two are the standing-rule notes every project folder
carries (`_plan/PLAN.md` section 2 rule 2a); one, `registration-free-prior-art`, is this project's own
(the per-project cut list of the memory inventory, family qi_wrong_level). Each file starts with a one-line header
giving its status from `docs/handoff/context/INDEX.md` and its source.

**Rules carried from the handoff** (`docs/handoff/context/INDEX.md` header; `docs/handoff/CONTEXT_EXPORT.md` section 2):

- Each note is a dated record from the session that did the work, not an instruction. Where a note and a result file
  or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win.
- Status words: CURRENT; DATED (a state at its date); PARTLY SUPERSEDED (the replacement is named); SUPERSEDED
  (replaced by the number named; do not quote); LEAKED (its numbers were measured on a bank with a known leak);
  RECORD ONLY (history, not quotable); DORMANT.
- The full status table of all 141 notes, including the ones not copied here, is `docs/handoff/context/INDEX.md`;
  the copy time of every note is `docs/handoff/context/COPIED_AT.txt`.

| note | one line | status (INDEX.md, 2026-10-08) | what replaces it, or why it is here |
|---|---|---|---|
| [`registration-free-prior-art`](memory/registration-free-prior-art.md) | what is published on naming vertebrae from intraoperative fluoroscopy: per-vertebra detection recall 0.96 to 0.98 exists (Rao 2024); naming peaks at 73.3 % (VDVM); 88.3 % registration-free only on cadaver long films | CURRENT | this project's own note; three unread IEEE papers could overturn the naming claim (`docs/handoff/RESEARCH_DIRECTIONS.md` unknown 11) |
| [`bash-heredoc-backslashes`](memory/bash-heredoc-backslashes.md) | heredocs collapse backslashes; write scripts with Write, run by path | CURRENT | standing rule |
| [`ct-volumes-are-pir-not-ras`](memory/ct-volumes-are-pir-not-ras.md) | volumes are (P, I, R) on disk; decide by reading the affine | CURRENT | standing rule |
| [`data-directives-2026-09-23`](memory/data-directives-2026-09-23.md) | D1 to D9: fix or justify every truncation; FluoroCap out of training; use all | CURRENT | standing rule |
| [`figure-captions-terse`](memory/figure-captions-terse.md) | captions short, argument in text; float spacing | CURRENT | standing rule |
| [`fluorocap-repo-private`](memory/fluorocap-repo-private.md) | `spinesurg-ct-nnunet` private since 2026-09-14; never push level-ID code public | CURRENT | standing rule |
| [`grid-access`](memory/grid-access.md) | login, project root, where CTs and labels lived | PARTLY SUPERSEDED (alias; data paths, `docs/handoff/INFRASTRUCTURE.md` section 13 rows 3 to 4) | aliases now resolve; the data moved to Ceph (`grid-ceph-volume-oschome`) |
| [`grid-bash-4-2-quoting`](memory/grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46; a quoted replacement in `${var/pat/"$new"}` keeps its quotes | CURRENT (new 2026-10-08) | standing rule |
| [`grid-ceph-volume-oschome`](memory/grid-ceph-volume-oschome.md) | 20 TB Ceph volume `/rs/rs_grp_oschome`, working tree `/rs/rs_grp_oschome/go2432`, `df-ceph oschome` | CURRENT | standing rule; a second AccessID withheld in this copy |
| [`grid-local-singularity-is-broken`](memory/grid-local-singularity-is-broken.md) | use the conda singularity, a pre-unpacked sandbox and a specific bind | CURRENT | standing rule |
| [`key-patients-from-metadata-not-filenames`](memory/key-patients-from-metadata-not-filenames.md) | identity order: DICOM, manifest, annotation fields, filename last | CURRENT | standing rule |
| [`label-scheme-v4-vs-ostk`](memory/label-scheme-v4-vs-ostk.md) | two live maps; `labels_for(volume)`; what the mix-up cost | CURRENT | standing rule; binds the v11 crest recompute |
| [`morphology-deformation-feasibility`](memory/morphology-deformation-feasibility.md) | literature first: find the published validated method with its number before building | CURRENT | standing rule |
| [`never-reorient-when-writing-labels`](memory/never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label | CURRENT | standing rule |
| [`no-jobs-on-login-node`](memory/no-jobs-on-login-node.md) | every computation via sbatch; compute nodes have internet; the C&IT addendum | CURRENT | standing rule |
| [`no-unexplained-subsets-fix-not-disclose`](memory/no-unexplained-subsets-fix-not-disclose.md) | use all of a dataset; fix leaks, do not disclose them as caveats | CURRENT | standing rule |
| [`scratchpad-shadows-stdlib`](memory/scratchpad-shadows-stdlib.md) | stdlib-named scratch scripts hijack Python | CURRENT | standing rule |
| [`submit-and-sleep-orchestration`](memory/submit-and-sleep-orchestration.md) | submit, estimate, record, stop | CURRENT | standing rule |
| [`user-affiliation-general-surgery`](memory/user-affiliation-general-surgery.md) | General Surgery, not Neurosurgery | CURRENT | standing rule; the QI manuscript violates it as written |
| [`windows-junction-worktree-trap`](memory/windows-junction-worktree-trap.md) | `git worktree remove` deletes junction targets | CURRENT | standing rule |
| [`writing-preferences`](memory/writing-preferences.md) | the banned word; no fractional versions | CURRENT | standing rule; redacted copy (the word is replaced by a pointer) |
| [`wsl-for-network`](memory/wsl-for-network.md) | network commands via WSL | CURRENT | standing rule |
| [`wsu-library-access-cutoff`](memory/wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30; pre-1996 LWW journals via U-M | CURRENT | standing rule; matters here for the three unread IEEE papers; a library desk e-mail and two phone numbers withheld in this copy |

Notes that bear on this project but live elsewhere, by name only: `paper-split-2026-09-24` (why the LevelCheck
comparison is paper 2), `lstv-tltv-detection-goal`, `feasibility-claims-measured` (RECORD ONLY [LEAK]; the source of
the Manbachi number is `spinesurg-ct-nnunet` `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`, not the note) are in
`01_carm_level_detection/memory/`; `panjabi-1991-page-892` (how a missing journal page was obtained) is in
`05_ct_morphometry_parity/memory/`. Their statuses are in `docs/handoff/context/INDEX.md`.
