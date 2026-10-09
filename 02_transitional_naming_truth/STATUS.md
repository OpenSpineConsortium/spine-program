# STATUS: the results in hand on 2026-10-08

Every row is an extract of `docs/handoff/RESULTS_CATALOG.md` (RC) or a memory note, with its id, the file that
holds the number and the rigor mark. Status words and marks are the catalog's (`docs/handoff/RESULTS_CATALOG.md`
"How to read a row"): CURRENT, CURRENT-SEL [SEL-SPLIT], HELD OUT, SUPERSEDED, REFUTED, RECORD ONLY, OPEN, FROZEN;
marks [THR], [SEL-REP], [WRONG-BANK], [LEAK], [SEL-SPLIT], [ONE-SEED], [AUTO-TRUTH], [DERIVED], [WORDING], [E],
[X]. Paths: `sn:` = `SchwingNet/` and `ssn:` = the root of the private repository `spinesurg-ct-nnunet` at
097933a (`MANIFEST_CODE.md`); a file copied into this folder is named by its path here. HOME =
`/wsu/home/go/go24/go2432`; Ceph = `/rs/rs_grp_oschome/go2432`.

**The one-sentence state.** No held-out transitional measurement exists; every powered statement rests on
planning accuracies of 95-99 % that no transitional measurement supports; 0 verified real at-risk persons exist
against 22 carriers, 35 at-risk persons or paper 2's 19 (RC E.14; `docs/handoff/literature_state/power.md`
section 6).

## 1. Transitional persons, the split and the sample-size argument (RC A16)

| id | result | file | status |
|---|---|---|---|
| A16.1 | 194 transitional persons in the sources: L6 110 (CTSP 18 / VerSe 86 / TS 3 / C-ArmLSpine 3), T13 7 (VerSe 6 / TS 1), sacralised L5 28 (12 four-lumbar), Castellvi I/II 31, lumbar rib 14, unassigned 4; per source 52 / 135 / 4 / 3 | `results/paper2/rare_class/transitional_subtypes.csv` (2026-09-23 18:54; `ssn:tools/transitional_subtypes.py --ts-override`) | CURRENT (paper 1 Table 2) |
| A16.2 | no spine carries both L6 and T13, in any source | `results/paper2/rare_class/transitional_subtypes.md` | CURRENT |
| A16.3 | eight of twelve TotalSegmentator "L6" spines are normal by an independent rib count; four are transitional | `sn:results/spineps_ids/TS12_VERIFY.md` (repository) | CURRENT |
| A16.4 | the built G3 split, test side: L6 43 + 3 real, T13 3, sacralised 11 (5 four-lumbar + 6 five-lumbar), Castellvi 12, lumbar rib 6, unassigned 2 = 77 CT + 3 real; 92 of 97 val+test persons sit in v8/v9 training (L6: 49 of 54) | `results/paper2/rare_class/split_plan.md` (`ssn:tools/make_split.py` apply 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS) | CURRENT, FROZEN |
| A16.5 | pre-stated targets: exact-level Wilson lower bound >= 90 % needs 35 error-free at-risk persons; variant sensitivity >= 85 % needs 22 carriers | `sn:results/power/power.json#n_needed_zero_errors` (repository); independent check `sn:results/stats_review/recompute.json#R4_wilson` PASS; re-derived by `docs/handoff/working_notes/t2_wilson_check.py` (match) | CURRENT |
| A16.6 | COBRA2026 screen: 91 unread test-side calls (L6 38, T13 45, four-lumbar 8); persons with both junctions in field and an exported frame: 7 at-risk, 4 two-labeller and 3 single-labeller (L6 3 = 2 + 1; sacralised L5 or four-lumbar 4 = 2 + 2; T13 0); error-free Wilson bound 64.6 % | `sn:packet_src/persons_available_2026-09-24.json#rows/<row>/real_counted_with_frame` (repository; a verbatim copy of the persons-available block of `power.json` as `fig_power.py` wrote it 2026-09-24 10:33, git 8d6a4f4); `sn:results/transitional_registry/REGISTRY.md` table C | CURRENT [AUTO-TRUTH] [WORDING] (paper 1 `results.tex` L94-97 calls the seven "a two-labeller count"; 3 are single-labeller) |
| A16.7 | at-risk CT test persons: 51 (L6 43, four-lumbar 5, T13 3), 36 rendered, 93.0 % if error-free; most in the encoder's training lineage | same file `#rows/at_risk_pooled/ct_test`, `#.../ct_rendered` | CURRENT |
| A16.8 | labeller calibration: VERIDAH's L6 call matched the CTSP readers in 10 of 24; T13 in 0 of 52 | `sn:results/spineps_ids/IMPACT.md` line 230; `sn:results/stats_review2/recompute.json#S4_cobra_call_yield` | CURRENT |
| A16.9 | no released radiograph or C-arm frame carries a human-read T13 or Castellvi grade | `sn:figures/figure1.record.json#not_shown_and_why` | CURRENT |
| A16.10 | 57 "field-supported" COBRA calls / 93.7 % best case; the 89 / 37 / 90.6 % inventory projection; the 98.2 %-planning-accuracy power curve (69 / 4,276) | `sn:tables/tab4_transitional.md` still prints "91 (57) ... 93.7"; the printed `.tex` reads "91 (7) ... 93.0 (51 CT); 64.6 (7 real)" | SUPERSEDED |

## 2. The development learning curve of the paper-2 arm (RC A17)

ImageNet-initialised encoder plus head on G3 training persons, nested fractions, three seeds, read on the
validation side that chose the epoch; this head belongs to the paper-2 model (`docs/LEVELCHECK_MODEL.md` section
12). Files `results/paper2/dual_loss/saturation.json`, `saturation_curve.csv`, `saturation_epochs.csv`
(`sn:tools/d1_saturation.py`; d1lcurve array 40436887, d1cover 40436997; logs `results/paper2/dual_loss/*.out`).
Status CURRENT, validation side only ("development numbers; no test person").

| id | result |
|---|---|
| A17.1 | training persons 563 / 1,121 / 2,240 / 4,477 / 8,950; random windows overall 68.9 % -> 74.0 % (last doubling +0.6; seed spread 1.0 at full size) |
| A17.2 | real films 98.2 % (563) -> 98.7 % (8,950), last doubling +0.1; three bodies 97.2-97.5 % at every size |
| A17.3 | CT renders 59.6 -> 66.2 % (+0.8 last doubling); rendered L6 bodies 51.8 -> 64.2 % (+1.7; seed spread 3.4); rendered T13 named in none of three full-size runs |
| A17.4 | epochs: within 0.5 points of final by epoch 8-12 |

D1 itself (`results/paper2/dual_loss/RUN_d1.json`): the dual-loss arm of section 12, a pre-specified secondary
model; three heads `head_fig6_g3clean_dual_seed{0,1,2}` and twelve learning-curve heads on the bank
`/rs/rs_grp_oschome/go2432/data/fig6/bank_g3_v2` (134,975 crops: 116,706 train / 18,269 val; 8,950 / 1,079
persons) from the ImageNet-root encoder `model_rung_1_g3clean_aug2.pt` (registry 629f0e058649ca1d); nothing
touches a G3 test person. Self-tests and the module md5 checks are beside it.

## 3. Paper 2 against LevelCheck (RC Part B)

Nothing here is printed in paper 1 (`sn:PAPER1_SCOPE.md`; `memory/paper-split-2026-09-24.md`).

| id | result | file | status |
|---|---|---|---|
| B.1 | LevelCheck's published numbers are registration accuracy; the level name is imported from the preoperative CT: Otake 2012 99.998 % simulated; Lo 2015 100 % at 200 multistarts; Manbachi 2018 median error 30.4 % -> 2.4 %; five surgeons 69.6 % unassisted -> 97.6 % with LevelCheck; "LevelCheck fails on transitional anatomy" is not citable | `docs/LEVELCHECK_CLAIM.md` sections 1, 3 | CURRENT literature reading |
| B.2 | frozen comparator: H1 at-risk 82.2 % (Peh 1999) n_min 19; H2 97.6 % (Manbachi 2018) n_min 152; H6 ordinary non-inferiority 92.6 % (margin 5) n 48 | `docs/LEVELCHECK_MODEL.md` (frozen by ecae75f 2026-09-23 19:50:36; then 1897772, 2993f40, b511985 section 14, d0403de section 15) | FROZEN; never edit |
| B.3 | automated reference: only ordinary spines qualify (Dawid-Skene PPV 0.971 [0.957, 0.981], coverage 0.886); no rule reaches a PPV lower bound of 0.90 for L6, T13 or four-lumbar; every transitional test person needs a human read. Calibration set 945 persons (CTSP 707, VerSe 238; train 846, val 99; 0 test persons, asserted); per-reader and three-rule tables | `results/paper2/auto_reference/CALIBRATION.md`, `calibration.json`; frozen `sn:results/fig6/frozen/auto_reference.json` sha256 57782cad... (repository and Ceph `data/fig6/frozen_v1`) | CURRENT |
| B.4 | ordinary COBRA test persons on automated truth: 56 assigned ordinary (44 with frames); H6 short of n_min 48 by 4 | `ssn:docs/RESUME_2026-09-22_PM.md` 2026-09-24 15:47 block | CURRENT (superseded in detail by `power.md` row 14: 13 reference-ordinary COBRA persons in the open gate) |
| B.5 | open gate 40438004 (ordinary strata only) ran 2026-09-25 04:22-06:02 UTC; harvest-name scores only; the reference-standard score was never written because `sn:tools/fig6_score.py` read `T1/blinded/meta_ref/` instead of `T1/open/meta_ref/`. Harvest-name lines per head (persons): T3 ordinary network 6-8/10, count 9/10, coupled 9/10; T1 render ordinary 3/3, 1/3, 1/3; T2 ordinary 1/4, 2/4, 2/4 | `manuscripts/paper2_levelcheck/open_gate_40438004/README.md`, `fig6_score_open_harvest.json`, `truth_join_open.json`, `RUN_CONFIG_open.json`, `f6eval-40438004.out`; `code/fig6_score.py` (the copy carries the defect note) | OPEN BUG |
| B.6 | blinded gate: memory names f6eval 40438005; `sn:REVISION_LOG3.md` line 7 names 40431765 / 40431766; held for Greg's truth decision, then cancelled 2026-09-27 15:50; must not be released before `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` exists | `results/paper2/fig6/HOLD_README.txt`, `RELEASE_OPEN_GATE.json`; `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` | OPEN; which job carries the post-section-15 detector is not recorded |
| B.7 | why it left paper 1: ordinary-only superiority over 97.6 % needs 152 zero-error persons; the transitional strata need human reads that do not exist | `memory/paper-split-2026-09-24.md` | CURRENT |
| B.8 | prior-art rates: wrong-level 1 in 3,110 (Mody 2008), 12.8 / 10,000 (Jhawar 2007), 0.12 % of 34,544 (Furuya 2026); LSTV 12.9 % with 54 % miscounted at clinic (Nakagawa 2017); Castellvi II-IV about 9 % of CT (Hanhivaara 2020) | `docs/LEVELCHECK_CLAIM.md` section 2 | CURRENT (as recorded) |
| B.9 | the old Figure 6d Wilson table: all 30 cells equal scipy Wilson lower bounds | `sn:results/power_table.json` (`sn:tools/fig_claim.py`) | RECORD ONLY |
| B.10 | moved material, verbatim with file and line (8 items from dd8f4a5) | `manuscripts/paper2_levelcheck/MOVED_FROM_PAPER1.md`, `numbers_manifest_moved.json`, `tables/tab_levelcheck.*` | CURRENT |

Gate records in `results/paper2/fig6/`: `RELEASE_OPEN_GATE.json` (released 2026-09-24 21:56:12 UTC; grid HEAD
0e8536bc; prespec commit ecae75f is an ancestor; G5 manifest commit a6cc8a1, sha256 e21f96bf...; pre-check job
40438053, 108 of 108 pass; eval root `data/fig6/eval_v2_g3`); `DETECTOR_G3_VALIDATION.md`, `DETECTOR_G3_VERIFY.md`,
`DETECTOR_G3_SUBMITTED.json` (the section 15 primary detector `det_g3_primary_s0`); `detector_lineage.json`,
`detector_exclusions.json`, `detector_g3_lists_check.json`, `G5_MANIFEST.json` (and a `_v2.draft`), `RUN_v2.json`,
`EVAL_SUBMITTED.json`, `cobra_g3test_export_list.txt`, `ts12_name_remap.json`.

## 4. What the level encoder learned about L6 and T13 (RC A1; v9 encoder on v9 VAL)

Files in this folder: `results/paper2/learning/figure2_metrics.json` (the Figure 2 metrics file,
`sn:results/figure2/figure2_metrics.json`, built 2026-09-23 20:10:19 on the person-cleaned validation set: 15,898
validation crops, 2,889 dropped because their person is in the encoder's training keys, 13,009 crops of 1,612 persons
kept, `#cleaning`); `figure2_transitional.json` (`sn:results/figure2/figure2_transitional.json`, `#fused_L5`);
`LEARNING.md`, `analysis.json`, `gradient_regression.json`, `zones.json`, `l6_confound.json`, `census.json`,
`bank_census.json`, `gradcam_summary.json`, `lateral/*.json` (grid jobs 40416675 GPU, 40416700 CPU). The arrays
(`embeddings.npz`, `heldout_l6.npz` and six more) are not in this folder (`MANIFEST_LOCAL.md` section 3).

**Two computations of the L6 silhouette exist and give different numbers; the rows below quote `figure2_metrics.json`.**
`analysis.json#silhouette/pairs/L6_vs_L5` and `LEARNING.md` line 88 are the earlier full-space computation on 150 L6
crops: 0.322 [0.289, 0.352]; L5 vs L4 0.192 [0.174, 0.208]; T12 vs L1 0.222. `figure2_metrics.json#silhouette/pairs` is
the person-cleaned recomputation that the catalog and paper 1 quote (98 L6 crops of 10 persons): L6|L5 0.349
[0.310, 0.386]; L5|L4 0.227 [0.205, 0.249]; L1|T12 0.324 [0.294, 0.352]; the earlier values are kept there under
`#silhouette/as_published`. A reader who opens `analysis.json` for row A1.2 finds 0.322, not 0.35; that is the earlier
file, not an error in either.

| id | result | file | status |
|---|---|---|---|
| A1.2 | L6 separates from L5 more than any ordinary pair: silhouette L6/L5 0.35 [0.31, 0.39] (98 crops, 10 persons; leave-person-out 0.34 [0.30, 0.38]); L5/L4 0.23 [0.21, 0.25]; L1/T12 0.32 [0.29, 0.35] | `results/paper2/learning/figure2_metrics.json#silhouette/pairs/L6|L5`, `.../L5|L4`, `.../L1|T12`; leave-person-out `#heldout_l6/validation_reference_two_cluster/L6` | CURRENT-SEL [SEL-SPLIT] (`#gate_verdict_validation_split`: the best of 40 epochs was kept on this split) |
| A1.3 | classifier calls: 75 of 98 L6 crops named L6 (0.765 [0.595, 0.944]); 111 of 1,012 L5 crops named L6 (0.110) | same file `#validation_neighbours_and_calls/L6/called/L6`, `/L5/called/L6` | CURRENT-SEL |
| A1.5 | never-seen L6 (C-ArmLSpine case42, case121, case136; 180 crops under the whole-vertebra box, AP and lateral): two-cluster silhouette 0.12 / 0.16 / 0.10 against validation L6 0.34; 84 of 180 crops named L6 (0.467; per patient 0.40 / 0.55 / 0.45 of 60); under the body box -0.07 and 13 of 180 (5 / 4 / 4) | same file `#heldout_l6/cells/"whole/primary"/L6` (`sil_L6_vs_L5_clusters`, `called/L6`, `per_patient/*`), `#heldout_l6/cells/"body/primary"/L6` (`sil_L6_vs_L5_clusters`, `per_patient/*/called_L6`), `#heldout_l6/validation_reference_two_cluster`; `#heldout_gate_check` (none of the three patient keys in the v9 train or val keys); `sn:figures/figure2.record.json#never_seen` (repository) | CURRENT, HELD OUT (EVAL_LEAKS item 5 CLEAN for v9) [AUTO-TRUTH: one labeller's read] |
| A1.6 | fused L5 (four validation persons): last free vertebra nearer L5 in 2 of 4 | `results/paper2/learning/figure2_transitional.json#fused_L5` | CURRENT-SEL |
| A1.8 | no T13 crop in validation: 44 T13 crops in training (7 persons), 0 in validation | `results/paper2/learning/figure2_metrics.json#bank_transitional_census/by_subtype/T13` (no `val` key) | CURRENT (a census) |

The L6 source confound (`l6_confound.json`; RD section 1.2): single-crop L6 on held-out render crops 0.800
[0.653, 0.922] of 150, but 116 of the 150 are `physics_rare`, where ordinary L4 and L5 also fall to 33-36 %; real
test sacra called L6 0.417 of 24.

## 5. Coupling on the real L6 patients (RC A5, the rows that bear on this folder)

| id | result | file | status |
|---|---|---|---|
| A5.4 | L6 calls on 3 of 233 anchored C-ArmLSpine frames (case139 AP + LAT, case44 LAT), all stopped; coupled exact on their 12 bodies 12 / 12, count 0 / 12 | `sn:results/eval_gate/closure/cv_v9/coupling_pre/coupling.json` (repository) | CURRENT, HELD OUT |
| A5.5 | the three one-labeller L6 patients: 6 frames, 4 anchored, one L6 call (case42 LAT, flagged); classifier 0 / 5, coupled 1 / 5 on the five bodies one labeller reads L6 (agreement, not correctness) | same | CURRENT [AUTO-TRUTH] |

## 6. Power (RC Part E; `docs/handoff/literature_state/power.md`)

| id | result | file | status |
|---|---|---|---|
| E.1 | Wilson lower bound with 0 errors: 88.65 % at n 30, 92.13 at 45, 93.98 at 60, 96.30 at 100 | `sn:results/power_table.json` | CURRENT; its 89-person inventory block superseded |
| E.2 | smallest n meeting the targets: 90 % bound needs 35 / 53 / 69 / 113 persons at 0 / 1 / 2 / 5 errors; 85 % sensitivity needs 22 / 34 / 45 / 74 carriers | `sn:results/power/power.json#panel_a`, `#n_needed_zero_errors`; re-derived by `docs/handoff/working_notes/t2_wilson_check.py` | CURRENT |
| E.3 | error-free bounds: 64.57 % at n 7, 90.59 at 37, 93.00 at 51, 95.86 at 89 | same | CURRENT (arithmetic) |
| E.4 | n for 80 % power: 99 persons at a true 97 %, 69 at 98 % (planning values with no transitional measurement behind them) | `sn:results/stats_review/recompute.json` R4_wilson | CURRENT, conditional |
| E.5 | power at 51 persons with no error allowed: 0.07 / 0.21 / 0.36 / 0.60 at a true 95 / 97 / 98 / 99 % | `power.md` section 2 rows 8-10 | CURRENT |
| E.6 | LevelCheck: n_min 19 / 48 / 152 for p0 0.822 / 0.926 / 0.976; 97.6 % cannot be exceeded at any reachable n (152 error-free persons give 0.22 power at a true 99 %); power 0 at any true accuracy <= 0.822 | `docs/LEVELCHECK_MODEL.md` sections 5, 7, 13; `sn:results/stats_review2/recompute.json` S1-S4, S9, S12 | FROZEN |
| E.7 | earlier claim table: 89-person inventory, test n about 36; 3 real transitional subjects give 43.9 % | `docs/LEVELCHECK_CLAIM.md` section 4 | SUPERSEDED inventory |
| E.8 | older Figure 5 panel b: 80 % power for the 90 % bound at 69; exceeding 97.6 % first at 4,276 | `sn:NUMBERS.md` L52 | SUPERSEDED 2026-09-24 |
| E.9 | certifying 99 % selective accuracy with zero errors takes about 298 answered cases; class-conditional 99 % needs >= 99 real cases per class | memory note `selective-prediction-the-honest-99` (not in this folder; LEAKED numbers, arithmetic stands) | CURRENT arithmetic |
| E.11 | device-level claims cannot be tested with 4 devices (smallest two-sided sign-flip P 0.125) | `power.md` section 6 | CURRENT |
| E.12 | T13 is the scarce class: 44-138 T13 people expected in the whole holding [E] against about 55 needed for 22 test carriers under 50/10/40 | `power.md` section 4 | CURRENT |
| E.13 | no power calculation exists for the synthetic:real ratio, device-level differences or LODO across devices; the person-level intraclass correlation for transitional endpoints is unknown | `power.md` section 8 | OPEN |
| E.14 | every powered statement rests on planning accuracies of 95-99 % that no transitional measurement supports; the transitional figures on disk put every transitional test at or near zero power; no held-out transitional measurement exists | `power.md` section 6 | CURRENT as a planning statement; none of the three figures is quotable |
| E.15 | two-proportion power, n per arm, minimum detectable difference | `ssn:tools/stats_compare.py` (its top-level `--help` crashes, OPEN_QUESTIONS F20; subcommand help works) | tool, no saved output |

The frozen endpoint's effect on power (`power.md` after row 17): the paper-2 endpoint scores a person wrong for a
missed body, an unanchored frame or an abstention; on ordinary C-ArmLSpine development frames it held on 162 of
284 (57.0 %) and naming failed on 1; the COBRA sacrum detector fixed for the primary analysis found the sacrum on
21 of 609 frames (3.4 %); section 15 replaced those detectors before unblinding and no file recomputes the power
under the replacement (C10).

## 7. The refuted and superseded lines (do not quote as current)

| id | result | file | status |
|---|---|---|---|
| C1.12 | 2-D LSTV / TLTV flags: CTSP AUC 0.577 [0.480, 0.669] (contains 0.5); VerSe 0.724; sex as positive control 0.951 on renders / 0.829 on real BUU | `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`; `memory/fluorocap-prototype-and-lstv-arm.md` | REFUTED as a flag |
| C1.14 | anomalous film interior windows: v2 ordinary 91.8 %, anomalous 66.0 % (12 films); v6 anomalous 49.9 % [41.5, 58.9] (128 films) | `memory/feasibility-claims-measured.md` | RECORD ONLY [LEAK] |
| C1.18 | the two-mechanisms table: L6 44.9 % in State C; one body 72.9 %, five bodies 97.0 %, whole 98.2 % | `memory/two-mechanisms-thesis.md` | SUPERSEDED (the framing still governs paper 1; current 601 / 617 = 97.4 % whole lateral, 451 / 603 = 74.8 % one body, RC A3.1, A3.3) |
| RD 1.2 | render L6 recall, mixed head, three seeds: lambda 0 56.1-61.2 %; lambda 1.0 67.4-72.4 %; false-L6 rate 0.14-0.18 % rising to 0.38-0.41 %; 10 held-out L6 persons, 98 crops, 0 T13 | `sn:results/ALPHABET_LOSS.md` (repository) | [SEL-SPLIT]: the v9 encoder kept its best epoch on the split these spines belong to (`sn:results/eval_gate/EVAL_LEAKS.md` item 6); quote only with that mark |
| D.24 | the R + C = 22 rule: one count, computable on 14 of 1,175 spines (1.2 %), specificity 0.000 | `ssn:docs/ANOMALY_RULE_EVALUATION.md` | REFUTED; removed on Greg's order |
| D.21 | pelvic cues for Castellvi on CTSP: ala rise AUC 0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599 | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` (public repository) | REFUTED cues |
| RD 2.2 | pretrain on renders then fine-tune: lost 25.6 anomalous points; decoder-named pseudolabels -19 anomalous; Star Temporal Classification 22-24 % against 39.8 %; render-to-fluoro translation (SDXL, CUT, CycleGAN, ADDA) no gain; size in millimetres no gain three times | `docs/handoff/RESEARCH_DIRECTIONS.md` section 2.2 | refuted or leaked; not re-run on v9 |

## 8. What is on disk but not scored, and what does not exist

- `greg_verdict` on 546 rendered registry review cases: 0 filled (D.9). `PREREG_rules.md` DRAFT v1, unsigned
  (D.23). `/rs/rs_grp_oschome/go2432/review_tree`: never built. `truth_frozen.csv`: does not exist
  (`RELEASE_OPEN_GATE.json` `human_truth_file`). `unblinding/RELEASE_v2.json`: does not exist.
- What the ruleclass arms finished after 2026-09-27: not recorded on the laptop (D.20); arm A tier 1 complete but
  one CT, tier 2 848 pending at 2026-09-29 04:23 (`../_plan/` grid listing via project 10); the pelvis arm's
  production array never ran (`MANIFEST_GRID.md`).
- The reader study Space (`code/reader_space/`): the design and its one confound are written; no reader has used
  it as far as any file records.
- The LSTV flag learning curve (`/wsu/home/go/go24/go2432/lstv_flag/LEARNING_CURVE.md`): exists on the grid; its
  date, job id and full table are not on the laptop (OPEN_QUESTIONS B15).
