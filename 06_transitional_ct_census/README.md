# 06 The transitional census: harvest, registry, ruleclass arms and the review tree

**Rank 6 of 12** (`../_plan/PLAN.md` section 1). **Reader:** student-safe after the redactions in `MANIFEST_LOCAL.md` and
Greg's confirmation of the reader split (`docs/handoff/OPEN_QUESTIONS.md` A29, A30). **Built** 2026-10-08 from the
sources recorded in `MANIFEST_LOCAL.md`. Start with `CLAUDE.md`, then `STATUS.md`, then `TODO.md`.

## What this is

A programme to find people with transitional spinal anatomy (a sixth lumbar vertebra, a thirteenth rib-bearing
vertebra, a sacralised L5, Castellvi II-IV, a lumbar rib) in every public CT collection we can hold, so that vertebra
naming can be tested on the people it fails on. It has five parts, all machine work except the last:

1. **The acquisition.** Public CT collections fetched to the grid under a stopping rule written before any fetch
   (`results/transitional_registry/acquisition/ACQUISITION_PLAN.md` sections 1-3): 18 collections screened by
   2026-09-25, 18,873 CTs listed, 16,898 on disk, 12,123 passing the field gate, 843 GPU-hours spent
   (`docs/CENSUS_TABLE_2026-09-25.md`; its "on disk" and "field gate" counts are one too high in every collection but
   PANORAMA, cause not recorded, `STATUS.md` D.13).
2. **The two-labeller screen.** Labeller A is SPINEPS + VERIDAH names bound to instances through the centroid file;
   labeller B is TotalSegmentator geometry with a 38 mm stump rule; they fail differently, which is why their agreement
   is a tier (`docs/handoff/RECIPES.md` section 3). Validated against 70 outside-labelled CTs: A found 12 of 28 L6, B
   17 of 28, both 9 (`results/transitional_registry/acquisition/validation/VALIDATION.md`).
3. **The registry.** One table over five harvest streams (verse, ctsp, totalsegmentator, cobra, other_ct): 6,131 rows,
   6,108 persons; L6 146 (read 103, two-labeller 29, single 10, morphology-only 4), T13 14 (read 6, two-labeller 3,
   single 5), sacralised L5 27, Castellvi I-II 31, lumbar rib 26 (`results/transitional_registry/REGISTRY.md`, written
   2026-09-24 11:07).
4. **The ruleclass census ("SUPER DETECTOR RUN").** Every CT with a mask, 21,622 of them in two tiers
   (`docs/ruleclass/TIERS.md`), under arm A (TotalSegmentator) and arm B (SPINEPS + VERIDAH + the Moller rib network,
   with Dataset803 for the pelvis only), feeding four pre-registered rules (`docs/ruleclass/PREREG_rules.md`, DRAFT v1,
   unsigned) and a two-stage human review tree (`code/transitional_review/`, `docs/REVIEW_TRANSITIONAL.md`).
5. **The human verdicts.** 446 registry review cases (verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87;
   `REGISTRY.md` "Review queues") plus 103 labeller-validation renders, 549 contact-sheet tiles in
   `contact_sheets/index.csv` (by path, `MANIFEST_LOCAL.md`); `greg_verdict` filled on 0. Stage 1 screen and stage 2 confirm are designed and have never run.

Three feeder lines are kept here because their results exist nowhere else: the **VerSeFusion** refusion of VerSe'19 and
'20 with VERIDAH corrections (`results/nextpaper/`, `results/versefusion_grid_derived/`, `figures/veridah_renders/`), the
**CTSpinoPelvic1K-Syn** synthetic Castellvi generator scaffold (`code/ctspinopelvic1k_syn/`, the only copy), and the
**MRI lstv-detector** line of the AACA 2026 abstract (`results/aaca_lstv_mri/`, `docs/aaca_lstv_mri/`; no ground truth,
its own README estimates 65-90 % accuracy by task).

## The goal

Enough verified transitional people to power the naming tests of projects 01 and 02: 22 carriers for an 85 %
sensitivity bound, 35 error-free at-risk persons for a 90 % exact-level bound (`docs/handoff/RESULTS_CATALOG.md`
A16.5), and a Castellvi grade on all 802 CTSpinoPelvic1K records (33 graded today against 71-142 expected;
`HANDOFF/RESEARCH_DIRECTIONS.md` CT-3 in spinesurg-ct-nnunet 097933a, a Greg-only file not in this folder, extracted as
`TODO.md` step 5). The route is readers, not more segmentation.

## State on 2026-10-08

| part | state | file |
|---|---|---|
| acquisition | tier 1 fetched and screened except PANORAMA (1,114 CTs pending); tier 2 (29,479 CTs, 2.9 TB) refused by the stopping rule; seven gated collections (Merlin, RATIC, CT-RATE, INSPECT, CADS, RSPECT, MAGIC-CT) have no agreement | `docs/CENSUS_TABLE_2026-09-25.md`; `HANDOFF/LITERATURE_STATE.md` section 2B (spinesurg-ct-nnunet 097933a; Greg-only, not in this folder; extract in `TODO.md` step 13) |
| registry | current for persons (2026-09-24); the acquisition stream has no `rows.csv` in it yet | `REGISTRY.md` "What is not known" |
| ruleclass arm A | tier 1: 5,094 CTs, done 3,166 + exists 1,927 + failed 1 (one remaining); tier 2: 12,217, done 10,398 + exists 968 + failed 3 + pending 848 (19.7 GPU-hours) | grid `ruleclass/arms/ts/STATUS.md` 2026-09-29 04:23:52, read 2026-10-08 (`MANIFEST_GRID.md`) |
| ruleclass arm B | fast pass 1,801 of 5,094 tier-1 CTs at 17:00 on 2026-09-27; later counts not recorded on the laptop | `STATUS.md` D.20 |
| ruleclass pelvis arm | `DECISION.json` written from 0 timing CTs (`n_timing 0`, `tier2_go false`); the production array never ran | grid `arms/pelvis/_timing/DECISION.json` 2026-09-29 08:21 |
| pre-registration | DRAFT v1 of 2026-09-27 (commit f15da62); the freeze block (signer, date, sha256) is blank | `docs/ruleclass/PREREG_rules.md` section 9 |
| review tree | code untracked, self-tests never recorded as run, `/rs/rs_grp_oschome/go2432/review_tree` does not exist, 0 of 446 registry review cases verdicted | `STATUS.md` D.9, D.23; `MANIFEST_GRID.md` |
| labeller calibration | VERIDAH L6 matched readers 10 of 24, T13 0 of 52; two-labeller L6 right 5 of 7 on CTSpinoPelvic1K | `STATUS.md` A16.8, D.15 |
| the house example | NLST T13 9.3 % (34 of 367) fell to 1.5 % once a rib on the named body was required | `STATUS.md` D.12 |

## Success criteria (pre-stated; `TODO.md` carries the gate of each step)

- The 33-CT discrepancy between `CORPUS.md` (21,655) and the tiers (21,622) is resolved and the census table's
  off-by-one is corrected, before any count is copied again.
- `PREREG_rules.md` is signed (section 9 filled); every rule output row carries `prereg_sha256`.
- Arm A tier 2 remaining = 0; the pelvis arm's `DECISION.json` rewritten from at least 20 timing CTs with a Dice.
- The review queues (verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87) carry a `greg_verdict` on every
  case; yield reported in two columns (confirmed on CT; with a frame); per-collection call rate inside the prevalence
  windows (L6 prior 3.2 %, T13 0.6-2.0 %, Castellvi II-IV 9-18 %).
- The whole-cohort CTSpinoPelvic1K Castellvi read: II-IV rate inside 9-18 %, type I near 68 % of calls, second-reader
  kappa at or above 0.63 (`HANDOFF/RESEARCH_DIRECTIONS.md` CT-3, spinesurg-ct-nnunet 097933a; Greg-only, not in this
  folder; extract in `TODO.md` step 5).

## How it relates to the other projects

- **10_data_platform_grid** owns the collections on Ceph, `spineps_ids.py` and the migration batches this folder
  depends on (B06 VerSeFusion VERIFIED; B07 TotalSegmentator copying on 2026-10-08).
- **03_ctspinopelvic1k_dataset** owns the seven disputed CTSpinoPelvic1K records, the Castellvi consensus and
  `lstv_reread_queue.csv`; the Castellvi csv files are deliberately in both folders (`../_plan/PLAN.md` section 2 rule 2).
- **02_transitional_naming_truth** consumes this folder's output: the real-frame truth file (FLU-1) needs the verdicts.
- **01_carm_level_detection** is the reason the count matters; it never reads this folder's data directly.
- **05_ct_morphometry_parity** shares the thoracolumbar shape score (rule 4) and the morphology API.
- Readers: Ashley Schehr (stage 1), the senior reviewer "Dr Tech" (stage 2; full name recorded nowhere on disk,
  OPEN_QUESTIONS A18), Greg adjudicates.


## Added in the final pass of 2026-10-08

- `code/aaca_lstv_mri/lstv_fusion/`: the SPINEPS + uncertainty-detection fusion pipeline behind the AACA 2026 LSTV result and the two tables in `results/aaca_lstv_mri/` (repository lstv-fusion 3c8f5c1; `MANIFEST_CODE.md` section 6b).
- Lineage note: the first synthesis of a transitional vertebra from a normal mask in this programme was the March-April 2026 sacralisation-synthesis line of SpineSurg-CT at 0051074; its scripts and its one QC result now sit in `../08_render_devices/code/spinesurg_ct_0051074/` and `../08_render_devices/results/superseded/sacralization_synthesis_2026-04/`. CTSpinoPelvic1K-Syn (this folder) replaced it; nothing from it is quotable.
