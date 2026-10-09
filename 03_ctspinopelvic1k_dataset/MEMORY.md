# MEMORY — index of `memory/` for project 03

55 notes, every one copied from the redacted `HANDOFF/context/` copies of 2026-10-08 (never from the live memory
folder), each with its status from `HANDOFF/context/INDEX.md` written on its first line after the front matter.
A note is a dated record from the session that did the work, not an instruction: where a note and a result file
or `STATUS.md` disagree, the file wins. Statuses: **CURRENT** (holds today), **DATED** (a state at its date),
**PARTLY SUPERSEDED** (the replacement is named), **SUPERSEDED**, **LEAKED** (none here), **RECORD ONLY** (none here).
The 32 notes the disposition assigned to this folder, the 4 the memory inventory's per-project cut list adds, and
the 22 standing-rule notes tagged for every folder are all here; the notes that are Greg-only (credential
locations, the commercial stance, the disclosure scrub), the Beethoven notes, the U251 / LITT notes and the
history-only resume notes were never copied (`../_plan/PLAN.md` section 2 rule 5).

Wikilinks inside a note (`[[name]]`) point at other notes by name; a target not in this folder lives in another
project's `memory/` or is Greg-only.

## Standing rules and laptop traps (carried by every project folder)

| note | one line | status (INDEX.md) |
|---|---|---|
| [`bash-heredoc-backslashes`](memory/bash-heredoc-backslashes.md) | inline heredocs collapse backslashes; write scripts as files, run by path | CURRENT |
| [`ct-volumes-are-pir-not-ras`](memory/ct-volumes-are-pir-not-ras.md) | volumes are (P,I,R) on disk; canonicalise to analyse, read the affine to check, never reorient to write | CURRENT (standing rule) |
| [`data-directives-2026-09-23`](memory/data-directives-2026-09-23.md) | D1-D9: fix or justify every truncation; use all of a dataset; FluoroCap out of training | CURRENT |
| [`figure-captions-terse`](memory/figure-captions-terse.md) | captions at most 60 words; the argument in the text | CURRENT |
| [`fluorocap-repo-private`](memory/fluorocap-repo-private.md) | the private repositories stay private; never push level-identification code public | CURRENT |
| [`grid-access`](memory/grid-access.md) | login, project root, where CTs and labels lived | PARTLY SUPERSEDED (the ssh alias now resolves, see wsl-for-network; data moved to Ceph, see grid-ceph-volume-oschome; HANDOFF INFRASTRUCTURE.md section 13 rows 3-4) |
| [`grid-bash-4-2-quoting`](memory/grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46: a quoted replacement keeps its quotes; a WSL-tested script can still fail there | CURRENT (new 2026-10-08) |
| [`grid-ceph-volume-oschome`](memory/grid-ceph-volume-oschome.md) | the 20 TB Ceph volume; `df-ceph oschome` | CURRENT |
| [`grid-local-singularity-is-broken`](memory/grid-local-singularity-is-broken.md) | use the conda singularity + a pre-unpacked sandbox + the specific bind | CURRENT |
| [`key-patients-from-metadata-not-filenames`](memory/key-patients-from-metadata-not-filenames.md) | identity order: DICOM, manifest, annotation fields, file name last | CURRENT |
| [`label-scheme-v4-vs-ostk`](memory/label-scheme-v4-vs-ostk.md) | two live label maps; `labels_for(volume)`; what the mix-up cost | CURRENT (standing rule) |
| [`morphology-deformation-feasibility`](memory/morphology-deformation-feasibility.md) | literature first; no bespoke CT warp | CURRENT |
| [`never-reorient-when-writing-labels`](memory/never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label away from its CT | CURRENT (standing rule) |
| [`no-jobs-on-login-node`](memory/no-jobs-on-login-node.md) | every computation through sbatch; compute nodes have internet; the C&IT addendum | CURRENT |
| [`no-unexplained-subsets-fix-not-disclose`](memory/no-unexplained-subsets-fix-not-disclose.md) | use all of a public dataset; fix leaks, never disclose them as caveats | CURRENT |
| [`scratchpad-shadows-stdlib`](memory/scratchpad-shadows-stdlib.md) | never name a scratch script after a standard-library module | CURRENT |
| [`submit-and-sleep-orchestration`](memory/submit-and-sleep-orchestration.md) | submit, estimate the wall time, record the ids and ETA, stop | CURRENT |
| [`user-affiliation-general-surgery`](memory/user-affiliation-general-surgery.md) | General Surgery (WSU School of Medicine / DMC), never Neurosurgery | CURRENT |
| [`windows-junction-worktree-trap`](memory/windows-junction-worktree-trap.md) | `git worktree remove --force` deletes junction targets | CURRENT |
| [`writing-preferences`](memory/writing-preferences.md) | the banned word; no fractional version numbers | CURRENT |
| [`wsl-for-network`](memory/wsl-for-network.md) | network commands through WSL | CURRENT |
| [`wsu-library-access-cutoff`](memory/wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30; pre-1996 full text elsewhere | CURRENT |

## The label scheme, the S1 carve and orientation

| note | one line | status (INDEX.md) |
|---|---|---|
| [`scheme-bone-hardware-only`](memory/scheme-bone-hardware-only.md) | the scheme is 0-68 with one hole at 29 from v11; 13 ribs per side; hardware 62-68 | CURRENT |
| [`s1-carve-changed-spinopelvic`](memory/s1-carve-changed-spinopelvic.md) | the carved S1 (29) was unreliable; gone in v11; retire every check on 29 | CURRENT (standing rule: identifier 29 retired) |
| [`ts-sacrum-excludes-s1`](memory/ts-sacrum-excludes-s1.md) | TotalSegmentator `sacrum` excludes S1; the whole sacrum is the union | CURRENT (the trap behind NeurIPS defect A, RESULTS_CATALOG F.47) |
| [`thoracic-gt-fov-limited`](memory/thoracic-gt-fov-limited.md) | the v3 thoracic ground truth covers about T8 down | CURRENT |
| [`dataset813-image-links-are-container-paths`](memory/dataset813-image-links-are-container-paths.md) | Dataset813 `imagesTr` links resolve only in the container; never repair; `HF_EXPORT_DIR` | CURRENT |

## The release, the deposit and the mirror

| note | one line | status (INDEX.md) |
|---|---|---|
| [`zenodo-deposit`](memory/zenodo-deposit.md) | Zenodo DOIs, the version recipe, the build archive; the token file by name only | PARTLY SUPERSEDED: says v10 is current; four documents give v11 = 10.5281/zenodo.22797014 published 2026-09-18 (MANUSCRIPTS.md section 20 C1); live state not re-checked (OPEN_QUESTIONS E7); names a token file by name only, never a value |
| [`hf-mirror-is-v10`](memory/hf-mirror-is-v10.md) | the public HF mirror is v10 with id 29 (2026-09-27); v11 local only; the lines to change when it ships | PARTLY SUPERSEDED: the Hugging Face mirror was still v10 on 2026-09-27 (checked by API), but its statement that Zenodo is v10 is contradicted by four documents giving v11 = 10.5281/zenodo.22797014, published 2026-09-18 (HANDOFF MANUSCRIPTS.md section 20 C1); live state not re-checked (OPEN_QUESTIONS E7) |
| [`hf-identity`](memory/hf-identity.md) | Greg's Hugging Face handle (public, no secret) | CURRENT |
| [`grid-ct-0533-truncated`](memory/grid-ct-0533-truncated.md) | CT 0533 truncation repaired on the grid and HF 2026-09-23 | CURRENT (done) |
| [`splits-origin-and-v3-resplit`](memory/splits-origin-and-v3-resplit.md) | the 5-fold splitter is patient-grouped + LSTV-stratified; the shipped splits never read the lumbar count | DATED (copied from HANDOFF/context under its renamed file name) |
| [`ctspine1k-selection-code-deleted`](memory/ctspine1k-selection-code-deleted.md) | CTSpine1K's supine / prone selector did not select; recoverable at 7f44959 | CURRENT |
| [`prone-supine-flexibility-future`](memory/prone-supine-flexibility-future.md) | 351 separate-mode pelvic acquisitions held out; the flexibility idea (CT-11) | DATED |

## Ribs and the review process

| note | one line | status (INDEX.md) |
|---|---|---|
| [`canonical-rib-triage`](memory/canonical-rib-triage.md) | the rib review set is defined by `qc_v4_ribs_and_verts.py` (152 cases); the worklist is regenerated from it | DATED |
| [`rib-approach-ts-trust`](memory/rib-approach-ts-trust.md) | rib labelling: trust TS numbering, add Möller's bridge (implemented 2026-06-29) | DATED |
| [`rib-auto-engulf-post-correction-only`](memory/rib-auto-engulf-post-correction-only.md) | rib cleanup only after student correction | CURRENT |
| [`rib-qc-gates-never-block-lstv`](memory/rib-qc-gates-never-block-lstv.md) | only rib-purity checks gate rib reviews; vertebra checks are advisory because transitional anatomy shifts ribs | CURRENT; redacted by hand on copy (two student usernames withheld) |
| [`review-space-repos`](memory/review-space-repos.md) | the exact HF repository ids of the review Spaces; the decoy repository | CURRENT |
| [`annotator-roster`](memory/annotator-roster.md) | who annotated what, from `slots[].reviewer` in the private ledgers; 13 students by 2026-08-23 | DATED; redacted copy (per-person usernames and counts withheld; the full note is Greg-only, HANDOFF/GREG_ONLY/context/) |
| [`nninteractive-colab-versions`](memory/nninteractive-colab-versions.md) | ITK-SNAP DLS (nnInteractive) Colab pins for the student rib review | DATED |
| [`lstv-reread-queue`](memory/lstv-reread-queue.md) | log doubtful source LSTV labels in `docs/lstv_reread_queue.csv` | CURRENT |
| [`spondylolysis-and-border-anomaly-findings`](memory/spondylolysis-and-border-anomaly-findings.md) | LCC deletes the loose lamina; T-L and L-S variants co-occur | CURRENT |

## Segmentation, benchmark and the thesis

| note | one line | status (INDEX.md) |
|---|---|---|
| [`local-level-identity-thesis`](memory/local-level-identity-thesis.md) | name a vertebra by local morphology instead of counting from C2 | CURRENT |
| [`competitor-benchmark`](memory/competitor-benchmark.md) | TotalSegmentator, SPINEPS / VERIDAH + Möller ribs, VISTA3D, RibSeg in the one-shot space; grid layout; decoder rules | DATED |
| [`l6-sample-count-and-counting-decoder`](memory/l6-sample-count-and-counting-decoder.md) | L6 Dice 0.000 = too few distinct cases; the counting decoder; Dataset815 | DATED |
| [`lstv-oneshot-training-run`](memory/lstv-oneshot-training-run.md) | the Dataset810 one-shot run for the CNS slides; retired for Dataset813 | DATED (whether the Dataset813 folds finished or were scored is not recorded, RESULTS_CATALOG C5.3) |
| [`panjabi-1991-page-892`](memory/panjabi-1991-page-892.md) | the full Panjabi 1991 obtained; Table 3 in `level_references.csv` | CURRENT (the article scan it names is reference-by-path, never copied) |

## Manuscripts, talks and style

| note | one line | status (INDEX.md) |
|---|---|---|
| [`journal-figure-and-style-rules`](memory/journal-figure-and-style-rules.md) | Medical Physics figure and text rules; no abstract in the main document; the page estimate | CURRENT |
| [`tables-black-not-colour`](memory/tables-black-not-colour.md) | matrix tables in solid black with one outlined mark | CURRENT |
| [`chart-preferences`](memory/chart-preferences.md) | slides: no sideways bars, donuts and lines, published background figures, big type | CURRENT |
| [`cns-deck-v2-2026-09-25`](memory/cns-deck-v2-2026-09-25.md) | the CNS spine deck: v10 discloses Part B; v12_public (17 slides, CT side only) is the disclosure-safe cut; generators and template traps | DATED (the talk is on 2026-11-02; only the v12_public deck may be shown) |
| [`publication-roadmap`](memory/publication-roadmap.md) | the paper split plan and venues, with 2026-06/07/09 updates | PARTLY SUPERSEDED (later frames in the flagship, rsnai and paper-split notes; history of the venue plan) |
| [`commit-directly-to-master`](memory/commit-directly-to-master.md) | the CTSP repository: commit to master, no branches | CURRENT |
| [`push-both-github-remotes`](memory/push-both-github-remotes.md) | CTSP: push `origin` and `osc` every time | CURRENT |

## What a reader would lose without these notes

Nothing numeric that is quotable: every current number is in a result file and in `STATUS.md`. What the notes keep
is the reasoning record: why each defect was found (rendering, an outside reference), the traps that cost days
(two label maps, identifier 29, P-I-R volumes, the login-node bans, bash 4.2, the heredoc backslashes), Greg's
directives with their dates (D1-D9, the two-remote rule, submit-and-sleep), and what must not be repeated (the
carved S1, a fixed label map, a fractional version).
