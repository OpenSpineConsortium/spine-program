# MEMORY.md — the notes that bind this project

`memory/` holds 34 memory notes copied from the redacted handoff copies of 2026-10-08 (`docs/handoff/README_PREFIXES.md`
says where those came from), plus `memory/HANDOFF_CONTEXT_INDEX.md`, the status index of all 141 notes (only 34 are in
this folder; the rest sit in the sibling project folders). Every note carries a first line `> STATUS ...` with the
status of `HANDOFF/context/INDEX.md` carried verbatim.

**Rules carried from the handoff.** A note is a dated record from the session that did the work, not an instruction;
where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win. LEAKED means
its numbers were measured on a bank with a known leak (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`);
SUPERSEDED means replaced by the number named; RECORD ONLY means history, not quotable; DATED means a state at its
date. None of the 34 notes here is LEAKED or RECORD ONLY.

## The 12 notes of this project's cut list (`memory_and_handoff_map`, family anomaly_scan_census)

| note | status | one line | caveat |
|---|---|---|---|
| `anomaly-harvest-directive` | CURRENT | Greg 2026-09-23: screen every CT for transitional anatomy, two labellers, both junctions in the field | the binding directive |
| `anomaly-manifest-sources` | DATED | 749 anomalous spines in 3 tiers; master table `lstv_flag_labels_v2.csv` (grid `~/lstv_flag/`); why the count was once 34/16/2 | the dated series of counts is `STATUS.md` D.27; never mix dates |
| `anomaly-rule-rc22-evaluated` | CURRENT | the R + C = 22 rule is one count, applies to 1.2 % of spines, C1 premise false for VerSe, localises nothing | REFUTED; removed from the manuscript on Greg's order (`STATUS.md` D.24) |
| `competitor-benchmark` | DATED | TotalSegmentator, SPINEPS/VERIDAH + Moller ribs, VISTA3D, RibSeg in the one-shot space; grid layout | the SPINEPS stores it harvested carry raw ids |
| `l6-sample-count-and-counting-decoder` | DATED | L6 Dice 0.000 = too few distinct cases; counting decoder; Dataset815 | the premise of CT-6 (`TODO.md`) |
| `lstv-data-landscape` | DATED; redacted copy | where LSTV/TLTV labels exist; Kwak 2025 is the one published 2-D LSTV model | three researcher e-mail addresses withheld |
| `lstv-oneshot-training-run` | DATED | Dataset810 one-shot LSTV run for the CNS slides; retired for Dataset813 | whether the Dataset813 folds finished is not recorded (`RESULTS_CATALOG.md` C5.3) |
| `ruleclass-super-detector-run` | CURRENT | the ruleclass census over 21,622 CTs; two arms; the review tree | what the arms finished after 2026-09-27 is partly answered in `MANIFEST_GRID.md` (arm A, pelvis); arm B not recorded |
| `spine-data-review-and-ts-bench` | DATED | the TS render bench, SPINEPS+VERIDAH over TS+VerSe, the scoping review | its SPINEPS stores carry raw ids; the TS bench is inside the v9 bank |
| `spineps-ids-can-be-scrambled` | CURRENT | pre-147428d SPINEPS masks carry raw ids; guard `tools/spineps_ids.py`; VERIDAH is not truth | the standing trap for every SPINEPS consumer |
| `spondylolysis-and-border-anomaly-findings` | CURRENT | LCC deletes the loose lamina; T-L and L-S variants co-occur | two paper-worthy findings not in code |
| `versefusion-t13-flag-wrong` | CURRENT | VerSeFusion `has_T13` says 18; truth 6 | re-counted on the copy here: 18 (`results/versefusion_grid_derived/HAS_T13_IS_WRONG.md`) |

## The 22 standing-rule notes every project folder carries (tagged `all`)

| note | status | one line |
|---|---|---|
| `bash-heredoc-backslashes` | CURRENT | inline heredocs collapse backslashes; write scripts to a file, run by path |
| `ct-volumes-are-pir-not-ras` | CURRENT | volumes are (P,I,R) on disk; canonicalise to analyse, read the affine to check |
| `data-directives-2026-09-23` | CURRENT | D1-D9: fix or justify every truncation; FluoroCap dropped; use all |
| `figure-captions-terse` | CURRENT | captions at most 60 words; the argument in the text |
| `fluorocap-repo-private` | CURRENT | spinesurg-ct-nnunet private since 2026-09-14; never push level-ID code public |
| `grid-access` | PARTLY SUPERSEDED | login and old data paths; aliases now resolve, data moved to Ceph |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46; a WSL-tested script can still fail there |
| `grid-ceph-volume-oschome` | CURRENT | 20 TB Ceph volume; `df-ceph oschome` |
| `grid-local-singularity-is-broken` | CURRENT | use the conda singularity + pre-unpacked sandbox + a specific bind |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM, manifest, ann fields, filename last |
| `label-scheme-v4-vs-ostk` | CURRENT | two live label maps; `labels_for(volume)`; what the mix-up cost |
| `morphology-deformation-feasibility` | CURRENT | literature first; no bespoke CT warp |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label away from its CT |
| `no-jobs-on-login-node` | CURRENT | every computation via sbatch; compute nodes have internet; the C&IT addendum |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a dataset; fix leaks, do not disclose them |
| `scratchpad-shadows-stdlib` | CURRENT | never name a scratch script `numbers.py`, `io.py`, `pdb.py` |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate the wall time, write ids and ETA, stop |
| `user-affiliation-general-surgery` | CURRENT | General Surgery, never Neurosurgery |
| `windows-junction-worktree-trap` | CURRENT | `git worktree remove --force` deletes junction targets |
| `writing-preferences` | CURRENT | the banned word; no fractional versions |
| `wsl-for-network` | CURRENT | network commands through WSL |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents 2026-06-30; pre-1996 via U-M |

## Three traps this project relies on whose notes live in sibling folders (not copied twice, `../_plan/PLAN.md` section 2 rule 2)

| note | where | the trap in one line |
|---|---|---|
| `ts-sacrum-excludes-s1` | `../10_data_platform_grid/memory/` | TotalSegmentator `sacrum` and `vertebrae_S1` are disjoint; the whole sacrum is their union; TS rib masks often lack the rib head |
| `vf813-drops-c1-t9-use-raw-verse-for-whole-spine` | `../10_data_platform_grid/memory/` | the Dataset815 conversion `vf_813` maps C1-T9 to ignore; whole-spine work reads the raw VerSeFusion masks |
| `lstv-reread-queue` | `../03_ctspinopelvic1k_dataset/memory/` | doubtful CTSpinoPelvic1K LSTV labels go into `docs/lstv_reread_queue.csv` of that repository, never a new file |

`docs/handoff/RECIPES.md` section 3.5 restates all three.
