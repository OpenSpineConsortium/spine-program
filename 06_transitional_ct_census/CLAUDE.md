# 06_transitional_ct_census — working context

Project 6 of 12 in `spine-program` (one private repository; rank 6 of the triage in `../_plan/PLAN.md` section 1).
Reader: student-safe after the redactions recorded in `MANIFEST_LOCAL.md`; Greg answered the reader split
(`docs/handoff/OPEN_QUESTIONS.md` A29) on 2026-10-12: every Write holder may read all 13 folders (issue #68). Built
2026-10-08.

## The goal in one paragraph

Find enough people with transitional spinal anatomy across every public CT we hold to test vertebra naming, and turn
each machine call into a human truth. Greg's directive of 2026-09-23 (`memory/anomaly-harvest-directive.md`): screen
every CT, two labellers that fail differently, both junctions in the field or the CT cannot count. The machine side is
nearly done: 18 collections acquired (18,873 listed, 16,898 on disk, 12,123 passing the field gate;
`docs/CENSUS_TABLE_2026-09-25.md`, whose counts run one too high in every collection but PANORAMA), one registry of
6,131 rows and 6,108 persons with L6 146 and T13 14 (`results/transitional_registry/REGISTRY.md`), a ruleclass census
over 21,622 CTs (`docs/ruleclass/TIERS.md`) with arm A complete but one tier-1 CT and 848 tier-2 CTs pending
(`MANIFEST_GRID.md`, the grid `arms/ts/STATUS.md` of 2026-09-29), four pre-registered rules still unsigned
(`docs/ruleclass/PREREG_rules.md`, DRAFT v1), and a two-stage review tree that has never run (`code/transitional_review/`,
untracked). What is missing is human: `greg_verdict` is filled on 0 of the 446 registry review cases (verse 71, ctsp 72,
totalsegmentator 137, cobra 79, other_ct 87; `REGISTRY.md` "Review queues"); with the 103 labeller-validation renders
that is 549 contact-sheet tiles (`contact_sheets/index.csv`, by path in `MANIFEST_LOCAL.md`). Until readers read, every positive outside the `read` tier is a candidate, not a result.

## Where things are

- **This folder.** `README.md` (state and success criteria), `STATUS.md` (every result with its file and rigor mark),
  `TODO.md` (what remains, ordered, with gates), `MANIFEST_GRID.md` (every grid path), `MANIFEST_CODE.md` (every
  repository, commit and file that matters), `MANIFEST_LOCAL.md` (what was copied, from where, what was left and why),
  `MEMORY.md` + `memory/` (the notes that bind this project, each with its status). `docs/handoff/` holds the eight
  student-readable handoff files of 2026-10-08 whole; `docs/handoff/README_PREFIXES.md` says what their path prefixes mean
  here. `docs/ruleclass/` is the rule design (R1-R33 in `CLASSIFIERS.md`, the stump rule, the pelvis arm, the tiers,
  the pre-registration). `results/transitional_registry/` is the one registry and its five streams.
  `results/versefusion_grid_derived/` and `results/nextpaper/` are the VerSeFusion line. `results/aaca_lstv_mri/` and
  `docs/aaca_lstv_mri/` are the MRI lstv-detector line. `code/` holds the review tree, the SPINEPS container recipe and
  the CTSpinoPelvic1K-Syn scaffold (its only copy).
- **The grid.** HOME `/wsu/home/go/go24/go2432`, Ceph `/rs/rs_grp_oschome/go2432`. The census lives at
  `/rs/rs_grp_oschome/go2432/ruleclass` (48.579 GB) and the screens and acquisitions under
  `/rs/rs_grp_oschome/go2432/data/anomaly_harvest` (325.817 GB) and `/rs/rs_grp_oschome/go2432/data/<collection>`;
  the full table with sizes, migration state and what was verified is `MANIFEST_GRID.md`.
- **The repositories.** `spinesurg-ct-nnunet` (private, branch `L6_Class`, commit 097933a) holds every tool and job of
  the scan; `CTSpinoPelvic1K` (public, `master`, 7ddfe38) the reads and the consensus; `OpenSpineToolkit` (public,
  `main`, cb43197) the label resolver; `VerSeFusion` (2b21cc4), `lstv-detector` (`no_angles`, 84636d6),
  `spine-level-ai` (5043793) and `lstv-annotation-tool` (1c51db7) the feeder lines. URLs and the files that matter:
  `MANIFEST_CODE.md`. Nothing in a repository is copied here.

## Standing rules, in this project's words

1. **The banned word.** The French-derived word for where data came from is never written. Say origin, lineage, source,
   where it came from. Copies that carried it were rewritten (`MANIFEST_LOCAL.md`).
2. **No fractional version bumps.** The next version is the next integer.
3. **Captions at most 60 words.** The argument goes in the text.
4. **Plain sentences. Every number carries the file it came from. What no file records is written "not recorded".**
5. **Check outside the computation.** The recurring failure in this programme is a number that is wrong but plausible.
   This folder holds the house example: the NLST pilot called T13 in 34 of 367 CTs, 9.3 %, five to fifteen times the
   prior, and the figure fell to 1.5 % once a rib had to sit on the named body
   (`results/transitional_registry/acquisition/collections/nlst_pilot/t13_check/T13_CHECK.md`). Every screen rate is
   read against its prevalence window (L6 2-5 %, thirteen rib-bearing 0.37-0.88 %, lumbar rib 1.6 %, Castellvi II-IV
   9-18 %; `docs/ruleclass/PREREG_rules.md`, `docs/handoff/RECIPES.md` section 3.4), against an outside read
   (`results/transitional_registry/acquisition/validation/VALIDATION.md`), and by rendering the mask.
6. **Two label schemes exist and mixing them does not raise.** CTSpinoPelvic1K v11 is VerSe-native (L1 20 ... L5 24,
   L6 25, sacrum 26, hips 30/31); the legacy map puts L1 at 1. Resolve names with `ostk.labels.labels_for(volume)`;
   never import a fixed map. Identifier 29 (the carved S1) is retired in v11; code that gates on 29 is retired with it.
   Case ids are zero-padded (`0001`): `zfill(4)` before any join. Canonicalise to RAS to analyse; never reorient a
   volume when writing it (`memory/label-scheme-v4-vs-ostk.md`, `memory/never-reorient-when-writing-labels.md`).
7. **Held out means never seen.** A person is held out only if neither the checkpoint nor any of its ancestors saw
   them. Every quoted score passes the evaluation gate (`tools/eval_gate.py` in `spinesurg-ct-nnunet`). The leaked
   banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`) are never quoted.
8. **Pre-register, then score.** The four rules are calibration until `PREREG_rules.md` section 9 carries a signer, a
   date and a sha256; after that every output row carries `prereg_sha256`, and a later change is a new dated version.
   Numbers enter text through a manifest key, never by hand.
9. **The grid.** Nothing runs on the login node (python, rsync and others are killed there by name): every census,
   count, render and plot is an `sbatch` job. `sbatch -D <dir>` because `--output` resolves against the submit
   directory; chain with `afterany` and read the output yourself; IPC sockets under `/dev/shm`, never `/tmp`; large
   outputs on Ceph; jobs are written for bash 4.2 (`memory/grid-bash-4-2-quoting.md`). Nothing container-related on the
   login node and nothing of ours under its `/tmp`.
10. **Private.** SchwingNet and every piece of level-identification code, text, figure and weight stays private; this
    whole repository is private and the student-safe label is about hand-outs only.
11. **Use all of a public dataset.** Every truncation is fixed or justified in writing before a rerun
    (`memory/data-directives-2026-09-23.md`, `memory/no-unexplained-subsets-fix-not-disclose.md`).
12. **Network through WSL on Greg's laptop** (`wsl -e bash -lc '...'` for git push, ssh, rsync). **Tokens are read
    from files only**, never echoed, never on a command line or in `sbatch --export`. **In the code repositories this
    folder names, commit only when Greg asks**; in spine-program itself the account doing the work pushes only its claim
    branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10).
13. **People.** Ashley Schehr is a person, never a product name; usernames are never written. The affiliation is
    General Surgery, Wayne State University School of Medicine / Detroit Medical Center, never Neurosurgery.

## Traps that bind this project

- **`has_T13` in the VerSeFusion manifest is wrong.** 18 flagged, 6 true; re-counted on the copy here
  (`results/versefusion_grid_derived/HAS_T13_IS_WRONG.md`). Read the raw VerSe masks (id 28 = T13, id 25 = L6) and
  the Loeffler table, never the flag, and never `vf_813`, which maps C1-T9 to ignore.
- **SPINEPS masks harvested before commit 147428d carry raw ids 1..N.** Never name by mask id; read through
  `tools/spineps_ids.relabel_by_ctd`; 431 masks in `tsv3_ctd` and 31 in `ctd_relabel/bench_ts_native` are symlinks back
  to the raw mask (`docs/ruleclass/TIERS.md` sections 3-4, `memory/spineps-ids-can-be-scrambled.md`). VERIDAH is a
  labeller, not truth: it matched the readers' L6 in 10 of 24 and T13 in 0 of 52 (`STATUS.md` A16.8).
- **A call needs a count, and a count needs both junction references in the field.** A CT that cannot count is
  `no_count`, never ordinary (`docs/handoff/RECIPES.md` section 3). Children: an unfused S1 reads as a free body.
- **Two labellers agreeing is a tier, not truth.** On CTSpinoPelvic1K the two-labeller L6 was right 5 of 7 after the
  2026-09-24 rules (`results/transitional_registry/cobra/labeller_validation_ctsp.md`). Only `read` is truth.
- **TotalSegmentator `sacrum` and `vertebrae_S1` are disjoint**; the whole sacrum is their union. Dataset803 was
  trained on CTSpine1K, CTPelvic1K and COLONOG, and 440 of the 802 CTSpinoPelvic1K pelvis labels are its own
  out-of-fold pseudolabels, so on that set its agreement with "GT" is model against model (`PREREG_rules.md` section 2).
- **Dated counts are never mixed.** 749 anomalous spines (2026-09-17), 81 (09-23 inventory), 194 persons (09-23
  subtypes), registry L6 146 / T13 14 (09-24), 196 rendered CTs (09-24), tier-1 flags L6 148 + 303 (09-27): six
  different things (`STATUS.md` D.27).
- **The census table is off by one** in every collection but PANORAMA, and the CNS 2026 table copied the high figures;
  fix it before anything copies it again (`docs/handoff/OPEN_QUESTIONS.md` F13).
- **`anomaly_manifest.py` defaults to a deleted bank** (`~/allspine_v5_fov96_ctx/rung_1.npz`, gone since 2026-09-20);
  pass `--bank` to v9 or the quality columns come back empty (OPEN_QUESTIONS F22).
- **The review tree writes to `/rs/rs_grp_oschome/go2432/review_tree`, which does not exist**, and its code is untracked. Commit after the
  self-tests; never score before the freeze.
- **The LCC post-processing deletes the loose lamina of a spondylolytic vertebra**, and a model counting from the rib
  anchor fails preferentially on LSTV cases because the anchor moves (`memory/spondylolysis-and-border-anomaly-findings.md`).
- **Append CTSpinoPelvic1K re-read discrepancies to `docs/lstv_reread_queue.csv` in the CTSpinoPelvic1K repository**,
  never a new file.

## How to be useful here

Read `STATUS.md` before quoting anything, `TODO.md` before starting anything, and `MANIFEST_GRID.md` before touching
the grid. Submit, estimate the wall time, write the job ids and the ETA into the step of `TODO.md` you are on, and stop
(`memory/submit-and-sleep-orchestration.md`). When a tidy explanation presents itself, test it before believing it. Say
plainly what is not known: `REGISTRY.md` "What is not known" and `STATUS.md` section 7 are the preferred form.
