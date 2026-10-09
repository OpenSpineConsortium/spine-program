# MEMORY.md: the notes that bind this project

`memory/` holds the memory notes assigned to this folder, copied on 2026-10-08 from the redacted handoff copies
(`HANDOFF/context/` of spinesurg-ct-nnunet at 097933a) with one exception stated below. Each copy carries, after its
frontmatter, the status that `HANDOFF/context/INDEX.md` gave it on 2026-10-08. A note is a dated record from the session
that did the work, not an instruction: where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the
file and the catalog win. LEAKED = its numbers were measured on a bank with a known leak; SUPERSEDED = replaced by the
number named; RECORD ONLY = history, not quotable; DATED = a state at its date; PARTLY SUPERSEDED = the part named.

`memory/CONTEXT_INDEX_2026-10-08.md` is the full handoff index of 141 notes with their statuses; only the notes listed
below are present in this folder, so most of its links do not resolve here (the others sit in the project folders that
own them). `memory/COPIED_AT_2026-10-08.txt` gives the copy time of every redacted note.

## Data platform, identity and leakage (the notes this folder owns)

| note | status on 2026-10-08 | one line | replaced by, or caveat |
|---|---|---|---|
| `data-platform-migration-2026-10` | CURRENT | manifest, layout, batches B00-B14, census, state on 2026-10-08, dedup verdicts, the TCIA contradiction | this copy is the live note of 20:43 UTC, newer than the handoff copy of 16:39 (one added paragraph records the handoff commit); per-batch truth is `plan/runs/<B>/STATUS` on the grid; its dedup totals (lines 70-71: 97.7 / 482.9 / 1,659) are the first plan's figures, superseded by `DEDUP_PLAN.md` "The totals" (`STATUS.md` section 9) |
| `grid-quota-and-deleted-banks` | CURRENT | `pan_quota` is the quota; allspine v2-v5c deleted 2026-09-20; `holdout.py` raises; 57 references repointed to v7 | |
| `grid-ceph-volume-oschome` | CURRENT | the 20 TB Ceph volume, `df-ceph oschome` | one username redacted here |
| `identity-audit-findings` | CURRENT | prone/supine ruled out; TS v2/v3 is a 24-id renumber; three leaks; a C-ArmLSpine case is not a person | |
| `key-patients-from-metadata-not-filenames` | CURRENT | identity order: DICOM, manifest, annotation fields, file name last | |
| `nhanes-double-inclusion` | CURRENT (fixed by patient keys) | NHANES II in the banks twice, split independently | |
| `split-leak-cross-naming` | CURRENT | per-source splits put one person on both sides (NHANES, CTSP); fixed by patient keys | |
| `splits-origin-and-v3-resplit` | DATED | the 5-fold splitter is patient-grouped and LSTV-stratified; v3 needs a resplit; the shipped v11 splits never read the lumbar count | the copy is renamed; the live note's file name carries the banned word |
| `spineps-ids-can-be-scrambled` | CURRENT | pre-147428d SPINEPS masks carry raw ids 1..N; guard `tools/spineps_ids.py`; VERIDAH is not truth | |
| `ts-sacrum-excludes-s1` | CURRENT | TotalSegmentator `sacrum` and `vertebrae_S1` are disjoint; whole sacrum = union | |
| `ts-bench-inside-v9-bank` | CURRENT | the TS render bench is not held out from the v9 encoder (70 TS + 1 CTSP + 0 VerSe renders unseen) | |
| `versefusion-t13-flag-wrong` | CURRENT | VerSeFusion `has_T13` says 18; the truth is 6 | |
| `vf813-drops-c1-t9-use-raw-verse-for-whole-spine` | CURRENT | `/wsu/home/go/go24/go2432/vf_813` maps C1-T9 to ignore; read raw VerSeFusion for whole-spine work | |
| `dataset813-image-links-are-container-paths` | CURRENT | Dataset813 `imagesTr` links resolve only inside the container; never repair on the host | |
| `ct-benchmark-covers-all-collections` | CURRENT | the CT axis is every collection (5,700+ subjects); `tools/ct_inventory.py` | |
| `data-audit-99-gaps` | DATED | the 99 gaps of `docs/DATA_COMPLETENESS_AUDIT.md`; the ones that change the science | |
| `data-directives-2026-09-23` | CURRENT | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | |
| `fluorocap-is-reproductions-not-fluoroscopy` | CURRENT | 72.8 % of FluoroCap panels have zero pixel residual; test set only | the reason FluoroCap is out of training |
| `flagship-program` | DATED | gates G0-G7 in the repository's `docs/FLAGSHIP_PLAN.md` | which gates are closed is not written in one place; `tools/pipeline_state.py` on the grid is the authority |
| `spine-data-review-and-ts-bench` | DATED | the TS render bench; SPINEPS + VERIDAH over TS and VerSe; where the scoping review lives | the SPINEPS stores it built carry raw ids |
| `model-registry` | CURRENT | content-addressed weights store, ledger, MLflow, HF mirror | whether `/wsu/home/go/go24/go2432/model_registry` survived the migration: it did on 2026-10-08 (`MANIFEST_GRID.md`) |
| `cloudflare-tls-fingerprint` | CURRENT | 403 everywhere = TLS fingerprint block; `curl_cffi impersonate="chrome"` | fetch recipe for the JHU archive and similar hosts |

## Grid operating notes

| note | status | one line |
|---|---|---|
| `no-jobs-on-login-node` | CURRENT | every computation via sbatch; compute nodes have internet; the C&IT addendum |
| `grid-bash-4-2-quoting` | CURRENT (new 2026-10-08) | the grid's bash 4.2.46 keeps the quotes of a quoted replacement; a WSL-tested suite can pass and the job still fail |
| `grid-access` | PARTLY SUPERSEDED (alias; data paths) | the old project-root layout; aliases now resolve (`windows-ssh-to-grid`); data moved to Ceph |
| `grid-access-list-gate` | CURRENT | approved students = named-user ACL entries on `/rs/rs_grp_oschome`; redacted by hand here (two usernames withheld) |
| `grid-apptainer-module-works` | CURRENT | `module load apptainer/1.2.2` builds sandboxes unprivileged; `secp` starts at once when `reqp` sits pending |
| `grid-local-singularity-is-broken` | CURRENT | use the conda singularity, a pre-unpacked sandbox, bind `/rs/rs_grp_oschome/go2432`, never `-B /rs` |
| `grid-slurm-inside-apptainer` | CURRENT | the binds that make sbatch work inside a container |
| `grid-ssh-second-factor` | CURRENT | ssh off-VPN with password + TOTP; keys skip it; warrior bans python, rsync and others by name |
| `grid-ct-0533-truncated` | CURRENT (done) | CT 0533 truncation repaired on the grid and the HF mirror 2026-09-23/24 |
| `windows-ssh-to-grid` | CURRENT | Windows ssh needs `MACs +hmac-sha1` and `AddressFamily inet`; the `wsu-grid`/`grid` alias |
| `wsl-for-network` | CURRENT | network commands through WSL |
| `submit-and-sleep-orchestration` | CURRENT | submit, estimate the wall time, record the id and ETA, stop |

## Standing rules copied into every project folder (`../_plan/PLAN.md` rule 2a)

| note | status | one line |
|---|---|---|
| `writing-preferences` | CURRENT | the banned word (named by a pointer, not spelled); no fractional versions |
| `figure-captions-terse` | CURRENT | captions at most 60 words; the argument in the text |
| `user-affiliation-general-surgery` | CURRENT | General Surgery, never Neurosurgery |
| `fluorocap-repo-private` | CURRENT | spinesurg-ct-nnunet private since 2026-09-14; never push level-identification code public |
| `no-unexplained-subsets-fix-not-disclose` | CURRENT | use all of a dataset; fix a leak, do not disclose it as a caveat |
| `label-scheme-v4-vs-ostk` | CURRENT | two live label maps; `labels_for(volume)`; what the mix-up cost |
| `never-reorient-when-writing-labels` | CURRENT | `as_closest_canonical` + `nib.save` transposes a label away from its CT |
| `ct-volumes-are-pir-not-ras` | CURRENT | volumes are (P,I,R) on disk; canonicalise to analyse, never to write |
| `morphology-deformation-feasibility` | CURRENT | literature first: find the published validated method with its number before building |
| `commit-directly-to-master` | CURRENT | CTSpinoPelvic1K: commit to master, no feature branches |
| `push-both-github-remotes` | CURRENT | push to `origin` and `osc` every time |
| `bash-heredoc-backslashes` | CURRENT | inline heredocs collapse backslashes; write scripts as files and run them by path |
| `scratchpad-shadows-stdlib` | CURRENT | never name a scratch script after a standard-library module |
| `windows-junction-worktree-trap` | CURRENT | `git worktree remove --force` deletes junction targets |
| `wsu-library-access-cutoff` | CURRENT | WSU Libraries dropped DMC residents 2026-06-30; the contact is withheld here |

## Not copied into this folder, and why

- The five Greg-only notes (`commercialization-stance`, `schwingnet-disclosure-scrub`, `hf-org-token-location`,
  `hf-osc-token-and-namespace`, `fluorocap-credentials-and-resolution`): commercial stance and credential locations.
- The six Beethoven product notes: they carry a personal e-mail, a tester's e-mail, licence key ids and token paths;
  `11_students_grid_access` holds them redacted.
- The seven U251 / LITT notes (another study) and the six history-only resume notes.
- The SchwingNet, render, transitional, CTSpinoPelvic1K and website notes: they sit in the folders that own them;
  their statuses are in `memory/CONTEXT_INDEX_2026-10-08.md`.
- The live `MEMORY.md` index: its one-line summaries carry leaked numbers and point at notes that were not copied
  (`docs/handoff/extracts/CONTEXT_EXPORT_sections_1_2_5.md`).
