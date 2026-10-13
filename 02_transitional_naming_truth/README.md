# 02_transitional_naming_truth

**Transitional-aware naming and the real-frame truth file (paper 2).** Rank 2 of 12 in `spine-program`
(`../_plan/PLAN.md` section 1). Reader: Greg only (SchwingNet and level-identification content). Built
2026-10-08 from the sources listed in `MANIFEST_LOCAL.md`; every number below names its file.

## What this project is

The programme's thesis is that a network can name a vertebra from its local morphology on a limited-field C-arm
exposure instead of counting down from C2 (`memory/lstv-tltv-detection-goal.md`). That thesis is only worth
testing where counting fails: on a transitional spine, where an L6, a T13, a sacralised L5 or a four-lumbar count
moves every name by one. Greg's standing determination of 2026-09-23 is the goal of this folder: name the level
correctly on a transitional spine from C-arm exposures **at parity with an ordinary spine, or write "not at
parity" with its number** (`docs/handoff/RESEARCH_DIRECTIONS.md` section 2.1). The parity target is stated
against count-changing anatomy (Castellvi II to IV, L6, T13, four-lumbar), not against "LSTV" as a whole:
Castellvi type I is unrecoverable from a lateral film by construction (RD section 2.1).

Paper 2 is the vehicle. It compares SchwingNet against registration-assisted surgeons (the LevelCheck series:
Otake 2012, Lo 2015, De Silva 2016, Manbachi 2018) under a comparator that was pre-specified from the literature
and frozen on 2026-09-23 before any test person was scored (`docs/LEVELCHECK_MODEL.md`; `docs/handoff/RESULTS_CATALOG.md`
B.2). Greg moved it out of paper 1 on 2026-09-24 because ordinary-only superiority over 97.6 % needs 152
zero-error persons and the transitional strata need human reads that do not exist
(`memory/paper-split-2026-09-24.md`; `docs/handoff/MANUSCRIPTS.md` section 3).

## What the folder owns

| item | where | state 2026-10-08 |
|---|---|---|
| the frozen LevelCheck comparator, endpoint, freeze, flag F1, automated reference, primary detector | `docs/LEVELCHECK_MODEL.md` sections 1-15 | FROZEN (ecae75f to d0403de); never edit |
| the earlier claim table (89-person inventory) | `docs/LEVELCHECK_CLAIM.md` | superseded by the model file; its literature reading (section 1-3) still stands (B.1, B.8) |
| paper 2's moved material, moved manifest keys, LevelCheck table, open gate 40438004 | `manuscripts/paper2_levelcheck/` | CURRENT; the open gate's reference score was never written (OPEN_QUESTIONS F3) |
| the G3 person split and the transitional subtypes (194 persons) | `results/paper2/rare_class/split_plan.md`, `transitional_subtypes.{csv,json,md}` | frozen 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS (A16.4) |
| the automated reference standard and its calibration | `results/paper2/auto_reference/CALIBRATION.md`, `calibration.json`, readers A/B/C lists and tables | CURRENT; certifies ordinary spines only (B.3) |
| the gate records (detector lineage, exclusions, G5 manifest, hold note, release record) | `results/paper2/fig6/` | CURRENT; the frozen reference and verification trees stay in the repository and on Ceph by path |
| the dual-loss arm D1 and the development learning curve | `results/paper2/dual_loss/RUN_d1.json`, `saturation.{json,csv}` | CURRENT, validation side only (A17) |
| what the level encoder learned about L6 and T13 (Figure 2 analyses) | `results/paper2/learning/` | CURRENT-SEL [SEL-SPLIT] except the never-seen L6 rows (A1) |
| the power inventory and the independent Wilson check | `docs/handoff/literature_state/power.md`, `power_calc.{py,json}`; `docs/handoff/working_notes/t2_wilson_check.py` | CURRENT (E.1-E.15) |
| the reader study Space (unaided then assisted naming; McNemar on rescued and harmed) | `code/reader_space/` | written 2026-09-18; no reader has used it (not recorded otherwise) |
| the rare-class, detector, reference-standard, verification and scoring tools | `code/` (copies with source headers); `MANIFEST_CODE.md` | tracked at 097933a |
| the whole 2026-10-08 handoff including the Greg-only files | `docs/handoff/` | copies; researcher e-mail addresses and student names withheld; laptop path prefixes rewritten to the tokens `[repo:<name>]`, `[laptop:<what>]` and `(session scratch path, not kept)` (`MANIFEST_LOCAL.md` section 2) |

## State on 2026-10-08, in numbers

- **Transitional persons in the sources: 194** (L6 110, T13 7, sacralised L5 28 of which 12 four-lumbar,
  Castellvi I/II 31, lumbar rib 14, unassigned 4; CTSP 52 / VerSe 135 / TotalSegmentator 4 / C-ArmLSpine 3)
  (`results/paper2/rare_class/transitional_subtypes.csv`, A16.1). G3 test side: L6 43 + 3 real, T13 3,
  sacralised 11, Castellvi 12, lumbar rib 6, unassigned 2 = 77 CT + 3 real; **92 of 97 val+test persons sit in
  v8/v9 training** (`split_plan.md`, A16.4); for L6, 49 of 54.
- **Real at-risk persons with a frame: 7, none verified** (4 two-labeller, 3 single-labeller: L6 3, sacralised
  L5 or four-lumbar 4, T13 0); error-free Wilson bound 64.6 % (`SchwingNet/packet_src/persons_available_2026-09-24.json`
  in the private repository, A16.6, E.3). COBRA screen: 91 unread test-side calls (L6 38, T13 45, four-lumbar 8);
  57 field-supported (11 L6, 38 T13, 8 four-lumbar) (A16.6, A16.10 note, RD section 2.7).
- **Pre-stated targets:** 35 error-free at-risk persons for the 90 % exact-level bound, 22 carriers for 85 %
  sensitivity (`SchwingNet/results/power/power.json#n_needed_zero_errors`, A16.5, E.2); paper 2 H1 n_min 19 (over
  82.2 %), H2 152 (over 97.6 %), H6 48 (non-inferiority at 92.6 %, margin 5) (`docs/LEVELCHECK_MODEL.md` sections 3,
  5; B.2, E.6). Power at today's n: 0 for every transitional hypothesis (E.14; `power.md` rows 8-13).
- **Labeller calibration:** VERIDAH's L6 call matched the CTSP readers in 10 of 24; T13 in 0 of 52
  (`SchwingNet/results/spineps_ids/IMPACT.md` line 230; A16.8). Automated reference: Dawid-Skene PPV 0.971
  [0.957, 0.981], coverage 0.886, ordinary only; no rule reaches 0.90 for L6, T13 or four-lumbar
  (`results/paper2/auto_reference/CALIBRATION.md`, B.3).
- **The open gate** (job 40438004, ordinary persons only, 2026-09-25 04:22-06:02 UTC) wrote harvest-name scores
  for six heads and no reference-standard score (`manuscripts/paper2_levelcheck/open_gate_40438004/README.md`,
  B.5). **The blinded gate** (40438005; `REVISION_LOG3.md` names 40431765 / 40431766) was held and then cancelled
  on 2026-09-27 15:50 with every non-ruleclass job; it may not be released before
  `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` exists, written by a person after a frozen human
  truth (`results/paper2/fig6/HOLD_README.txt`, B.6).
- **Development curve (paper 2 arm, validation side):** rendered L6 bodies 51.8 to 64.2 % across training
  fractions 563 to 8,950 persons; rendered T13 named in none of three full-size runs; real films 98.2 to 98.7 %
  (`results/paper2/dual_loss/saturation.json`, A17.1-A17.3).
- **Transitional numbers that are not held out:** render L6 recall 56.1-72.4 % [SEL-SPLIT]; the v2-lineage
  44.9 / 72.9 / 97.0 / 98.2 % (SUPERSEDED); anomalous-film 49.9 % and 66.0 % (RECORD ONLY [LEAK]); the three real
  L6 patients 0 of 5 classifier, 1 of 5 coupled against one labeller [AUTO-TRUTH] (A5.5, C1.14, C1.18, E.14).
  **No held-out transitional measurement exists.**
- **Human reads: 0.** `greg_verdict` is filled on 0 of 546 rendered registry review cases (D.9;
  OPEN_QUESTIONS A17). `PREREG_rules.md` is DRAFT v1 (f15da62), unsigned (D.23; A16). The review tree
  `/rs/rs_grp_oschome/go2432/review_tree` was never built (`MANIFEST_GRID.md`).
- **The refuted line:** the 2-D LSTV / TLTV flag, CTSP AUC 0.577 [0.480, 0.669] (contains 0.5), VerSe 0.724
  (`/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`, C1.12). The R + C = 22 rule: one count, 1.2 % of
  spines, specificity 0.000 (D.24). Both withdrawn.

## Success criteria

1. **FLU-1, the truth file.** A table of real-frame transitional persons, each with its truth tier (read >
   two-labeller > single-labeller), its CT read through the frozen two-stage protocol, and whether an exported
   frame exists, in two columns (confirmed on CT; scorable on a real frame). The gate is 22 carriers with a frame
   for the 85 % sensitivity bound, 35 at-risk persons for the 90 % exact-level bound, 19 for paper 2 H1, **or the
   written sentence** that no fluoroscopy transitional sensitivity can be claimed from the holding and that DAT-1
   is the only route (RD section 2.8, section 6 rank 3).
2. **FLU-2, the clean encoder.** A ResNet-18 two-channel encoder from ImageNet on G3 training persons only,
   scored on the 7 render-scoreable of the 11 validation L6 persons: zero or one miss proceeds to three seeds, two
   heads and the count-against-morphology agreement with `alphabet_couple.py`; two or more misses stops the arm and
   the manuscript says "not at parity" with the number. The count must catch at least 80 % of run-shifted L6 films
   and the stop signal must fire on at least half of the erring L6 films for the design to be called anomaly-aware
   (RD sections 2.7, 2.8).
3. **Paper 2.** The reference-standard score of the open gate written (F3); power recomputed under the section 15
   detector once 19 or more verified at-risk persons exist; the blinded gate unblinded only under the frozen
   protocol, by a person, with the ledger carrying every "seen" entry. If fewer than 19, paper 2 is restated as
   awaiting verified cases (RD "After FLU-1's read").
4. **The hand-off to 01.** The truth file, the reader protocol (`PREREG_rules.md` section 9 freeze block signed
   and hashed; `REVIEW_TRANSITIONAL.md`) and the power table are what 01's PREREG for the hospital test is written
   from (`../_plan/PLAN.md` 01 S5, S6).

## How it relates to the other projects

- **01 C-arm level detection** (`../01_carm_level_detection/`): owns the shared stack, `alphabet_couple.py`, the
  COBRA2026 collection and the regulatory documents; depends on this folder for the pre-registered transitional
  endpoint. 01 S10 (the reader study and the comparison) is this folder's paper 2.
- **06 transitional CT census** (`../06_transitional_ct_census/`): owns the registry (`REGISTRY.md`, the review
  queues, contact sheets), the ruleclass arms, `PREREG_rules.md`, `REVIEW_TRANSITIONAL.md` and the untracked
  review-tree code. This folder's reader queue runs through 06's tree; 06's re-reads can move the G3 split.
- **08 render devices** (`../08_render_devices/`): the `physics_rare` renders and the device cards that render the
  rare-class banks.
- **10 data platform** (`../10_data_platform_grid/`): the identity tables, `patient_keys.py`, batches B09 (FluoroCap),
  B10 and B11 (banks, `split_final.json`); the one read-only grid listing of 2026-10-08 22:20 UTC lives there.
- **05 CT morphometry parity**: the 2-D side of parity (PAR-6) depends on FLU-2; CT-3's whole-cohort Castellvi
  read is the largest increase in read positives on data already held.
- **07 plain-film level identification**: the film N-curve shares `film_ncurve.py`; the refuted flag line's film
  side (BUU) sits there.
- **99 archive**: the FluoroCap documents and dormant lines.

## People

Greg Schwing (resident physician, Department of General Surgery, Wayne State University School of Medicine /
Detroit Medical Center; grid account `go2432`; signs every freeze). Ashley Schehr (senior scientist and co-PI;
stage-1 screener of the transitional review; a person, never a product name). "Dr Tech" (senior clinical PI;
stage-2 confirmer; full name and e-mail recorded nowhere on disk, `docs/handoff/OPEN_QUESTIONS.md` A18).

## On the grid

Since 2026-10-13 (issue #87) `results/` and `manuscripts/` of this folder are symlinks to the same path under `/rs/rs_grp_oschome/shared/spine-program/archive/` on the grid, where the files are read through the link; everywhere else they are read from git history at main 5597197. `../ARCHIVE.md` says how, and how a task that must change one of them brings it back into its branch. The counts and sizes in `MANIFEST_LOCAL.md` describe the folder as it was built on 2026-10-08.
