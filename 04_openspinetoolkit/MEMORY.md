# MEMORY.md: the notes this project carries

`memory/` holds 28 notes copied on 2026-10-08 from the handoff's redacted context copies
(`spinesurg-ct-nnunet/HANDOFF/context/`, branch `L6_Class`, commit 097933a), each with a first line
giving its status from `HANDOFF/context/INDEX.md` (built 2026-10-08). Twenty-two are the standing rules
and laptop traps every project folder carries; nine are the toolkit cut list of the memory map
(`memory_and_handoff_map.md`, family "toolkit"); three sit in both lists. Statuses: CURRENT = the state
on 2026-10-08; DATED = a state at its date, still true as a record; PARTLY SUPERSEDED = the named part is
replaced; none of these 28 is LEAKED, SUPERSEDED or RECORD ONLY.

Rules carried from the handoff:

- A note is a dated record of the session that wrote it, not an instruction. Where a note and a result
  file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win.
- The copies came from `HANDOFF/context/`, not from the live memory folder: the live copy of
  `writing-preferences` spells the banned word, the context copy does not; the live copy of
  `label-scheme-v4-vs-ostk` links a note by its old name (the only difference, a one-line diff checked
  2026-10-08). The other 26 copies were byte-identical to the live notes on 2026-10-08.
- One redaction was made on copy: `wsu-library-access-cutoff` carried a library staff e-mail and two
  phone numbers; they read "[library contact withheld on copy]" here.
- Three notes spelled absolute laptop paths as worked examples (`pacs-demo-and-ostk-params` line 14,
  `windows-junction-worktree-trap` lines 16 and 26, `wsl-for-network` line 17). On 2026-10-08 those four
  paths were replaced by the markers `<laptop Desktop>` and `<laptop home>` (`MANIFEST_LOCAL.md` section 2).
  The folders they named are history, not dependencies: the code lives at the repository and commit in
  `MANIFEST_CODE.md`.

## The nine toolkit notes

| note | status | one line | what replaces it, or caveat |
|---|---|---|---|
| `ostk-canal-closing-regression` | CURRENT (open) | ostk 1b7005c inflates VBHp/EPD 10-17 mm on about 1 in 7 vertebrae; min_vox 20 admits 3 mm canals; fix plan inside | the open defect G.2; the fix plan is `TODO.md` step 1; its baseline numbers are now in `STATUS.md` |
| `label-scheme-v4-vs-ostk` | CURRENT | two live maps; `labels_for(volume)` detects; what the mix-up cost (PI for all 802 against the legacy map) | its v10 list still names "S1 = 29": true for v10, retired in v11 (`CLAUDE.md` rule 4) |
| `pacs-demo-and-ostk-params` | CURRENT | ostk parameters and CLI; the NiiVue PACS demo; do not reintroduce the blanket SVA/TPA claim | "v3 (Vert+S1+femur)" describes the June 2026 state; the demo case 0003 is still a v3-scheme case |
| `engine-swap-architecture` | DATED | the viewer consumes a `metrics.json` contract so the engine can be swapped; `predict`/`synthesize` interface planned | contract only; no network backend exists (handoff topic 6 section 10) |
| `postop-spine-synthesis` | DATED | `ostk.surgery` synthetic post-op spines; numbers carried analytically; demo 0003 ALIF L1-S1 | prototype (G.5); never re-measure the synthesised image |
| `postop-jaggedness-future` | DATED | future: fix voxel roughness so the synthesised image can be re-measured | dormant until Greg asks |
| `commit-directly-to-master` | CURRENT | CTSpinoPelvic1K commits to master, no branches | ostk's branch is `main`, both remotes (`CLAUDE.md` rule 10) |
| `ct-volumes-are-pir-not-ras` | CURRENT | volumes are (P, I, R) on disk; decide by reading the affine | also a standing rule |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label away from its CT | also a standing rule |

## The twenty-two standing-rule notes

| note | status | one line |
|---|---|---|
| `bash-heredoc-backslashes` | CURRENT | heredocs collapse backslashes; write scripts with Write, run by path |
| `ct-volumes-are-pir-not-ras` | CURRENT | (above) |
| `data-directives-2026-09-23` | CURRENT | D1-D9: use all of a dataset, fix or justify every truncation, FluoroCap out of training |
| `figure-captions-terse` | CURRENT | captions at most 60 words; the argument in the text |
| `fluorocap-repo-private` | CURRENT | the private repository stays private; never push level-ID code public; ask before adding it to ostk |
| `grid-access` | PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE section 13 rows 3-4) | login and where CTs and labels lived; aliases now resolve (`windows-ssh-to-grid`, in 11); data moved to Ceph (`grid-ceph-volume-oschome`) |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid runs bash 4.2: a quoted replacement in `${var/pat/"$new"}` keeps its quotes |
| `grid-ceph-volume-oschome` | CURRENT | 20 TB Ceph volume at `/rs/rs_grp_oschome/go2432`; `df-ceph oschome` |
| `grid-local-singularity-is-broken` | CURRENT | use the conda singularity with a pre-unpacked sandbox and a specific bind |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM, manifest, annotation fields, file name last |
| `label-scheme-v4-vs-ostk` | CURRENT | (above) |
| `morphology-deformation-feasibility` | CURRENT | literature first; find the published validated method and its number before building |
| `never-reorient-when-writing-labels` | CURRENT | (above) |
| `no-jobs-on-login-node` | CURRENT | every computation through `sbatch`; compute nodes have internet; the C&IT addendum on containers |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a dataset; fix a leak by retraining, never disclose it as a caveat |
| `scratchpad-shadows-stdlib` | CURRENT | never name a scratch script `numbers.py`, `io.py` or `pdb.py` |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate the wall time, write ids and ETA to the checkpoint, stop |
| `user-affiliation-general-surgery` | CURRENT | General Surgery (WSU School of Medicine / DMC), never Neurosurgery |
| `windows-junction-worktree-trap` | CURRENT | `git worktree remove --force` deletes junction targets |
| `writing-preferences` | CURRENT | the banned word; no fractional version bumps |
| `wsl-for-network` | CURRENT | git push, ssh, rsync and Hugging Face through WSL |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents 2026-06-30; pre-1996 journals through another route (contact withheld here) |

## Notes that bear on this project but live in another folder

- `scheme-bone-hardware-only` (03): the v11 scheme is 0-68 with one hole at 29; `label_dict()` has no
  `"S1"` key so a stale caller gets a KeyError; "ostk still has `"S1": 29` in its v10 map and needs the same
  treatment; its scheme detection is safe (it keys on hip and femur voxel mass, not on 29)". The facts this
  project needs from it are in `CLAUDE.md` rule 4 and `TODO.md` step 2.
- `s1-carve-changed-spinopelvic` (05, 03): why the carve was withdrawn (median craniocaudal extent 57.6 mm
  against a real segment near 30; 222 records lost more than half the sacrum), the whole-sacrum plate
  isolated by the lowest lumbar footprint, release PI 52.1 / SS 36.6 / PT 15.5 on n 756, the 60-degree plate
  gate on 44 records, and "retire the checks that test a withdrawn label".
- `panjabi-1991-page-892` (05): the Panjabi 1991 Table 3 values in `level_references.csv`.
- `push-both-github-remotes` (03): restated as `CLAUDE.md` rule 10.
- `pacs-website-latency-root-cause`, `level-service-serving` (12): the demo's and the service's rules.
- `hf-mirror-is-v10`, `zenodo-deposit` (03): the public mirror still held id 29 on 2026-09-27; v11 is
  Zenodo 10.5281/zenodo.22797014 per the handoff.
