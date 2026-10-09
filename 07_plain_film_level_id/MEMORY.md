# MEMORY.md: the index of `memory/`

36 notes copied on 2026-10-08 from `HANDOFF/context/` of `spinesurg-ct-nnunet` (private, branch
`L6_Class`, commit 097933a), the redacted copies with statuses, never from the live memory folder.
Every copy carries a one-line header with its status from `HANDOFF/context/INDEX.md` and the
modification time of the memory original (`memory/COPIED_AT.txt`). A note is a dated record from
the session that did the work, not an instruction; where a note and a result file or
`docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win.

Status words (from `HANDOFF/context/INDEX.md`): CURRENT; DATED (a state at its date); PARTLY
SUPERSEDED; SUPERSEDED (replaced by the number named); LEAKED (its numbers were measured on a bank
with a known leak: allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`); RECORD ONLY (history,
not quotable); DORMANT.

## The 14 notes of this project (the `plain_film_level_id` cut list of `memory_and_handoff_map.md`)

| note | status | what replaces it, or the caveat |
|---|---|---|
| `context-ladder-2d-level-experiment` | DATED | design rules of the context ladder (masking, not cropping); BUU levels are counting-inferred |
| `feasibility-claims-measured` | RECORD ONLY [LEAK] | never quote its numbers: its accuracies are on v2 / v5 / v6 (RESULTS_CATALOG C1.14, C1.16); its claim-by-claim reading of the external report still stands |
| `film-ncurve-ablation-result` | SUPERSEDED reading | "all help" is outdated: the tool's `READ.md` shows 7 of 9 cells separated, six help and one hurts (BUU at every person) (A10.6-A10.9); "from 100 persons the arms overlap" holds at 100 and 200 persons, not at every person (A10.10) |
| `fluoro-panel-gap-diagnosed` | DORMANT | FluoroCap diagnosis; never quote 19.7 % as an accuracy (C1.11) |
| `level-id-2d-results-2026-09-13` | RECORD ONLY | the 96.7 % single-crop number is on the cervical-dominated `films_ann` bank (C1.1) |
| `level-model-bank-coverage` | DATED | why the 99 % was a 14-class number |
| `mixed-length-head-and-sota` | LEAKED | 97.47 % at 3 vertebrae and the "shortcut-free" 99.02 % are on allspine v2, which pooled NHANES II twice (C1.6); held-out film naming today is the film N-curve: CSXA 99.8 %, BUU 96.9 %, NHANES 92.7 % (A10.1-A10.3). The training rule (mixed band lengths) and the prior-art reading stand |
| `nhanes-double-inclusion` | CURRENT (fixed by patient keys) | the leak record behind the v2, v6 and v7 verdicts |
| `recurrent-head-restored-2026-09-16` | DATED | the head's 99 % was on a cervical-dominated bank (`CONTEXT_EXPORT.md` section 3); the head lineage stands |
| `remedies-refuted-2026-09-17` | LEAKED numbers | the scaling curve it quotes is the v2 sweep (C2.1, SUPERSEDED [LEAK] [SEL-SPLIT]); the refutations were not re-run on v9 (RESEARCH_DIRECTIONS unknown 24) |
| `selective-prediction-the-honest-99` | LEAKED | the 99 % at 35.7 % / 55.7 % coverage is on the leaked v2 bank, computed on its own test half (C1.8; LEAKAGE section 5.1); no clean re-run exists (OPEN_QUESTIONS C13). Its arithmetic (about 298 answered cases to certify 99 %) still holds (E.9) |
| `stc-does-not-transfer` | CURRENT | a refuted loss; do not revisit (C1.7) |
| `xr-benchmark-and-robustness-2026-09-13` | RECORD ONLY [WRONG-BANK] | the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; OPEN_QUESTIONS F5) |
| `xray-corner-detector-status` | DATED | detector lineage (detect_v2 on 2026-09-08; detector_v5z descends from it); **redacted by hand in this copy**: a student's first name replaced by "a student" |

## The 22 standing-rule notes (tagged `all`; every project folder carries them)

| note | status | one line |
|---|---|---|
| `bash-heredoc-backslashes` | CURRENT | heredocs collapse backslashes; write scripts as files and run them by path |
| `ct-volumes-are-pir-not-ras` | CURRENT | volumes are (P,I,R) on disk; canonicalise to analyse, never to write; read the affine to check |
| `data-directives-2026-09-23` | CURRENT | D1-D9: fix or justify every truncation; FluoroCap dropped; use all of a dataset |
| `figure-captions-terse` | CURRENT | captions at most 60 words; the argument in the text |
| `fluorocap-repo-private` | CURRENT | `spinesurg-ct-nnunet` private since 2026-09-14; never push level-identification code public |
| `grid-access` | PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE section 13 rows 3-4) | login and project root; aliases now resolve (`windows-ssh-to-grid`, not in this folder); data moved to Ceph (`grid-ceph-volume-oschome`) |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46; a WSL-tested suite can pass and the job still fail |
| `grid-ceph-volume-oschome` | CURRENT | the 20 TB Ceph volume at `/rs/rs_grp_oschome/go2432`; `df-ceph oschome` |
| `grid-local-singularity-is-broken` | CURRENT | use the conda singularity with a pre-unpacked sandbox; bind `/rs/rs_grp_oschome/go2432`, never `-B /rs` |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM, manifest, annotation fields, file name last |
| `label-scheme-v4-vs-ostk` | CURRENT | two live label maps; `labels_for(volume)` detects; never import a fixed map |
| `morphology-deformation-feasibility` | CURRENT | find the published validated method with its number before building anything bespoke |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label away from its CT |
| `no-jobs-on-login-node` | CURRENT | every computation via `sbatch`; compute nodes have internet; the C&IT addendum |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a public dataset; fix leaks, do not disclose them as caveats |
| `scratchpad-shadows-stdlib` | CURRENT | never name a scratch script `numbers.py`, `io.py` or `pdb.py` |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate the wall time, write ids and the ETA to the checkpoint, stop |
| `user-affiliation-general-surgery` | CURRENT | General Surgery, Wayne State University School of Medicine / Detroit Medical Center, never Neurosurgery |
| `windows-junction-worktree-trap` | CURRENT | `git worktree remove --force` deletes junction targets; remove junctions first |
| `writing-preferences` | CURRENT | the banned word; no fractional version bumps |
| `wsl-for-network` | CURRENT | git push, ssh, rsync and Hugging Face through WSL |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents on 2026-06-30; pre-1996 articles through another route |

## Not in this folder, and why

- The five Greg-only notes (`commercialization-stance`, `schwingnet-disclosure-scrub`,
  `hf-org-token-location`, `hf-osc-token-and-namespace`, `fluorocap-credentials-and-resolution`), the
  seven U251 / LITT notes, the six history-only resume notes and the live `MEMORY.md` index: never
  copied into any project folder (`_plan/PLAN.md` section 2 rule 5).
- `review-space-repos` (the exact Hugging Face repository ids of the review Spaces and the decoy
  repository): carried by `11_students_grid_access`; this folder's `code/review_space/README.md` names
  the ledger repository the maintainer recipe downloads.
- `lstv-data-landscape` (the one published 2-D LSTV model; BUU's "No License Provided" plus EULA):
  carried by `06_transitional_ct_census`; its BUU reading is quoted in `MANIFEST_LOCAL.md` from the
  `buu_lspine_3600` card.
- `anomaly-manifest-sources` (the BUU `L4L6` sheet: 129 four-lumbar, 15 six-lumbar): carried by 06;
  the count is restated in `docs/handoff/LITERATURE_STATE.md` section 1.3.
