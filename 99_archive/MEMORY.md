# Memory index for 99_archive

Each note in `memory/` is a dated record from the session that did the work, not an instruction. Where a note and a
result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win. Every copy was taken from the
redacted set `HANDOFF/context/` of spinesurg-ct-nnunet at 097933a (copied there 2026-10-08 16:39 by
`HANDOFF/working_notes/builders/refresh_context.py`), never from the live notes, and carries its status from
`HANDOFF/context/INDEX.md` as the first line. Status words: CURRENT; DATED (a state at its date); PARTLY SUPERSEDED;
SUPERSEDED (replaced by the number named); LEAKED (its numbers were measured on a bank with a known leak: allspine v2,
v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`); RECORD ONLY (history, not quotable); DORMANT (a line nobody works).

## The six archive-family notes

| note | status | one line | row home and why it is also here |
|---|---|---|---|
| `fluorocap-dataset` | DORMANT | FluoroCap test set on the grid under `/wsu/home/go/go24/go2432/FluoroCap`: stages, routes, manifest schema, the frozen release | DISPOSITION mem r40: home is this folder; 01 references it. 2,100 FluoroCap crops still sit in the C-ArmLSpine fold banks (`docs/handoff/DATASET_USAGE.md` section 3.2) |
| `publication-roadmap` | PARTLY SUPERSEDED (later frames in flagship, rsnai, paper-split notes) | the paper split plan and venues, with 2026-06, 07 and 09 updates | DISPOSITION mem r100: home is this folder; history of the venue plan |
| `cns-deck-v2-2026-09-25` | DATED | the CNS 2026 spine deck: v10 discloses Part B; the public CT-side cut; generator and template traps | row home `03_ctspinopelvic1k_dataset`; copied here too because the superseded deck lineage is recorded here (the archive cut list, `../_plan/inventories/memory_and_handoff_map.md` section "archive (history, superseded decks and plans)"; rule 2b of the plan) |
| `fluoro-panel-gap-diagnosed` | DORMANT | literature panels 19.7 % against 95.1 % on radiographs: domain plus contamination | row home `07_plain_film_level_id`; here because it is the FluoroCap diagnosis; never quote 19.7 % as an accuracy (catalog C1.11) |
| `fluorocap-prototype-and-lstv-arm` | DORMANT | the single-image prototype, the transitional harvest arm, the Semantic Scholar route, the LSTV flag results, the two verification benches | row home `02_transitional_naming_truth`; here as the FluoroCap record |
| `fluorogen-synthetic` | DATED | SDXL + ControlNet + LoRA synthetic C-arm frames; img2img dead at every strength; CUT v2 is not a lever | row home `08_render_devices`; here because it is a refuted generative route that stops a repeat |

## The 22 standing-rule notes (every project folder carries them; plan rule 2a)

| note | status | one line |
|---|---|---|
| `bash-heredoc-backslashes` | CURRENT | inline heredocs collapse backslashes; write scripts with the Write tool and run them by path |
| `ct-volumes-are-pir-not-ras` | CURRENT | CT volumes are (P, I, R) on disk; canonicalise to analyse, read the affine to check, never reorient to write |
| `data-directives-2026-09-23` | CURRENT | Greg's directives D1 to D9: fix or justify every truncation; FluoroCap out of training; use all |
| `figure-captions-terse` | CURRENT | captions at most 60 words; the argument goes in the text |
| `fluorocap-repo-private` | CURRENT | spinesurg-ct-nnunet private since 2026-09-14; never push level-identification code public |
| `grid-access` | PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE section 13 rows 3-4) | login, project root, where CTs and labels lived; aliases now resolve; data moved to Ceph |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46; a quoted replacement in `${var/pat/"$new"}` keeps its quotes |
| `grid-ceph-volume-oschome` | CURRENT | the 20 TB Ceph volume `/rs/rs_grp_oschome/go2432`; `df-ceph oschome` |
| `grid-local-singularity-is-broken` | CURRENT | use the conda singularity, a pre-unpacked sandbox and a specific bind |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM, manifest, annotation fields, file name last |
| `label-scheme-v4-vs-ostk` | CURRENT | two live label maps; call `labels_for(volume)`; what the mix-up cost |
| `morphology-deformation-feasibility` | CURRENT | literature first; no bespoke CT warp |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label away from its CT |
| `no-jobs-on-login-node` | CURRENT | every computation via sbatch; compute nodes have internet; the C&IT addendum |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a dataset; fix leaks, do not disclose them as caveats |
| `scratchpad-shadows-stdlib` | CURRENT | never name a scratch script after a standard-library module |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate the wall time, record the ids and ETA, stop |
| `user-affiliation-general-surgery` | CURRENT | General Surgery, never Neurosurgery |
| `windows-junction-worktree-trap` | CURRENT | `git worktree remove --force` deletes junction targets |
| `writing-preferences` | CURRENT | the banned word; no fractional version numbers (the copy is the redacted one, which does not spell the word) |
| `wsl-for-network` | CURRENT | network commands through WSL |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents on 2026-06-30 |

## By reference only (never copied; RECORD ONLY; history-only entry points)

These six live notes point at repository documents that hold the actual checkpoints; the documents are in
`docs/checkpoints/`. They are not in `HANDOFF/context/` and are not copied here (`MANIFEST_LOCAL.md` records why).

| note | what it was | the record it points at |
|---|---|---|
| `overnight-2026-09-15-chains` | where the 2026-09-15 overnight FluoroCap runs wrote their markers, logs and chain scripts | the markers are on the grid under `/wsu/home/go/go24/go2432/FluoroCap` |
| `resume-2026-09-21-pm` | START HERE for the CT-to-fluoroscopy formation work after 2026-09-21; names a researcher and an e-mail (Balgrist), so never copied unredacted | `docs/checkpoints/HANDOFF_2026-09-21_PM.md` |
| `resume-2026-09-22` | the 2026-09-22 checkpoint: the RSNAI plan, the k-devices queue | `docs/checkpoints/RESUME_2026-09-22.md` |
| `resume-2026-09-22-pm` | the 2026-09-23 02:15 checkpoint at the top of the resume file; the FLAGSHIP_PLAN gates | `docs/checkpoints/RESUME_2026-09-22_PM.md` |
| `resume-2026-09-24` | the 2026-09-24 checkpoint: Figure 6 open gate released (job 40438004), blinded gate 40438005 held | `docs/checkpoints/RESUME_2026-09-22_PM.md` |
| `resume-2026-09-26-handoff` | the 2026-09-26 handoff: half U251 (another study), the spine half points at the resume file | `docs/checkpoints/RESUME_2026-09-22_PM.md` |

The live `MEMORY.md` index of the Claude project is Greg-only and never copied: its one-liners carry leaked numbers and
link notes that were not copied.

## Notes that bear on this archive but live in other folders

`fluorocap-is-reproductions-not-fluoroscopy` (CURRENT; the reason FluoroCap is out of training; 01),
`stc-does-not-transfer` (CURRENT; 01, 07), `drr-to-fluoro-levers` (CURRENT; 01, 08), `anomaly-rule-rc22-evaluated`
(CURRENT; 06), `remedies-refuted-2026-09-17` (LEAKED numbers; 01, 07), `selective-prediction-the-honest-99` (LEAKED;
01, 07), `mixed-length-head-and-sota` (LEAKED; 01, 07), `two-mechanisms-thesis` (SUPERSEDED numbers; 01),
`level-id-2d-results-2026-09-13` (RECORD ONLY; 01, 07), `xr-benchmark-and-robustness-2026-09-13` (RECORD ONLY
[WRONG-BANK]; 07), `feasibility-claims-measured` (RECORD ONLY [LEAK]; 01, 07), `film-ncurve-ablation-result`
(SUPERSEDED reading; 01), `recurrent-head-restored-2026-09-16` (DATED; 01, 07), `fluorocap-pipeline-resume` (CURRENT,
but it runs python on the login node, against the rule; 01), `lstv-oneshot-training-run` (DATED; 03). The folder in
parentheses is the row home in `spine-program/_plan/DISPOSITION.tsv`; their replacements are in `SUPERSEDED_NUMBERS.md`.
