# STATUS.md — the results in hand on 2026-10-08

Every row names the file that holds the number. Rows D.x and A16.x are the rows of `docs/handoff/RESULTS_CATALOG.md`
Part D and section A16 that the plan assigns to this folder, with the catalog's status word and rigor mark carried
unchanged; where the file is copied into this folder the local path is given, otherwise the repository path
(`MANIFEST_CODE.md`) or the grid path (`MANIFEST_GRID.md`). Rows G.x were read off the grid on 2026-10-08 22:20 UTC
(`../10_data_platform_grid/`, the one read-only pass). Rows V.x, S.x and M.x are the feeder lines.

**Status words** (from the catalog): CURRENT = the standing value in its document; DATED = a state at its date;
DISPUTED = two files disagree, the trusted reading is given; REFUTED = tested and failed; OPEN = unfinished;
NOT RECORDED = known to have run, result in no file on the laptop; SUPERSEDED = replaced by a named later number.
**Rigor marks**: [AUTO-TRUTH] the truth is two labellers agreeing or one labeller's read, not a human read;
[WORDING] a printed sentence overstates the file; [E] an expectation (prior times probability), not an observation.

**2026-10-12, who reads what.** Greg answered OPEN_QUESTIONS A29 on issue #68, option (a): every Write holder may read all 13 folders; "Greg-only" and the label `greg-first` govern claiming and hand-outs, not reading. The `docs/handoff` copies keep their older wording.

## 1. The anomaly scan (catalog Part D)

| id | claim | file | status |
|---|---|---|---|
| D.1 | anomaly manifest of 2026-09-17: 749 anomalous spines; tier A certain 355 (VerSe 163, BUU 144 real films, CTSP 48), tier B pseudolabel 211 (VinDr 209, LAT236 2), tier C FluoroCap captions 183; four-class over 1,113 CT spines 902 ordinary / 98 LS-only / 47 TL-only / 66 both | grid `/wsu/home/go/go24/go2432/model_night/anomaly_manifest/{anomaly_manifest.csv, spine_classes.json, summary.json}`; `memory/anomaly-manifest-sources.md` | DATED; the master flag table is grid `~/lstv_flag/lstv_flag_labels_v2.csv`; the count was once 34/16/2 because only the 802-row CTSP manifest was read |
| D.2 | co-occurrence of thoracolumbar and lumbosacral variants: OR VerSe 4.30 [2.59, 7.14], CTSP 4.00 [1.00, 16.03]; the pooled 12.8 is Simpson's paradox; VerSe 280 fully graded 3.61 [2.08, 6.27] | `memory/anomaly-manifest-sources.md`; tool `tools/anomaly_cooccurrence_from_labels.py` (spinesurg-ct-nnunet 097933a) | DISPUTED: trust 3.61; never quote 12.8; CTSP's 4.00 is underpowered (a both-cell of two) |
| D.3 | BUU anomaly labels in `KIOM2022_dataset_report.xlsx` sheet `L4L6` (129 L4, 15 L6); 9 of the 15 "L6" are children | `memory/anomaly-manifest-sources.md` | CURRENT caution |
| D.4 | anomalous inventory of 2026-09-23: VerSe 56 (L6 50, T13 6), CTSP 18 L6, TotalSegmentator 4 (3 L6, 1 T13), C-ArmLSpine real 3 L6 = 81 | `SchwingNet/results/anomalous_inventory.{json,md}` (spinesurg-ct-nnunet 097933a); job 40416205 | DATED |
| D.5 | transitional subtypes 194 persons; the G3 split | catalog A16.1, A16.4 (`docs/handoff/RESULTS_CATALOG.md`) | CURRENT |
| D.6 | 49 of 54 L6 val+test people of the G3 split are in the v8 / v9 training lineage | `SchwingNet/results/rare_class/split_plan.md` (spinesurg-ct-nnunet) | CURRENT; limits what any v8/v9 descendant can claim |
| D.7 | five harvest streams (workflow wf_babed05b-84a): verse 374 series / 355 persons (L6 85, T13 6, sacralised 13, Castellvi I/II 27, lumbar rib 12, unassigned 23); ctsp 64 positive rows (L6 29: 17 read, 11 two-labeller, 1 single; sacralised 12; Castellvi I/II 4; lumbar rib 14; unassigned 5); totalsegmentator 1,935 v300 keys (L6 22, T13 4, unassigned 26, unresolved 74); cobra 692 (L6 3, unassigned 6, unresolved 11, TEST only); other_ct 3,066 (CTSpine1K L6 3, sacralised 2; RibFrac T13 4, L6 1) | `results/transitional_registry/<stream>/SUMMARY.md`, `rows.csv` | DATED |
| D.8 | **the one registry** (2026-09-24 11:07): 6,131 rows -> 6,108 persons (5 phantoms as rows); 782 alias edges; **L6 146** (read 103, two-labeller 29, single 10, morphology-only 4; 6 real-frame TEST), **T13 14** (read 6, two-labeller 3, single 5), sacralised L5 27, Castellvi I-II 31, lumbar rib 26, unassigned 62, unresolved 129, none 1,686, no_count 3,987; against the subtype table L6 110 -> 146 (106 kept, 3 dropped, 40 new), T13 7 -> 14 | `results/transitional_registry/REGISTRY.md`, `registry.csv` (2,885,193 B), `registry.json` | CURRENT for persons |
| D.9 | review queues: verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87 (+103 labeller-validation), all rendered; **`greg_verdict` filled on 0** | `results/transitional_registry/REGISTRY.md` "Review queues"; the queue csv files under each stream's `review_queue/`; the 26 contact sheets are by path only (`MANIFEST_LOCAL.md`) | OPEN |
| D.10 | MAXIMIZE: rendered before 87; planned 165, rendered 109, held by the ID guard 54, stopped 2; waiting for adjudication 39; real-frame TEST 13; unavailable 2; rendered transitional CTs now 196 | `results/transitional_registry/maximize/MAXIMIZE.md` (2026-09-24 16:55), `after/` json | CURRENT |
| D.11 | acquisition plan tier 1: 45 routes + NLST pilot, 15,233 CTs, expected transitional people E_low / E_high 831 / 1,703, E_count 460; stopping rule stated before any fetch | `results/transitional_registry/acquisition/ACQUISITION_PLAN.md` sections 1-3; `fov_calibration.json` (job 40425064); priors `tools/acquisition_census.py` L17-26 | [E] expectation, not observation |
| D.12 | **NLST pilot T13 9.3 % (34 of 367, labeller A alone, 5-15x the prior) was wrong but plausible**; with a rib on the named body required: 21 had no rib on the body, 6 sat below the last disc, 2 had only a cut rib, **5 kept** as single-labeller T13 (1.4 % of 367; the catalog writes 1.5 %, the plan's rounding) | `results/transitional_registry/acquisition/collections/nlst_pilot/t13_check/T13_CHECK.md`, `t13_check.csv`; `ACQUISITION_PLAN.md` section 11; jobs 40436876/77 | CURRENT; the house example of checking outside the computation; `acquisition_screen.confirm_t13_by_rib` now runs at every call stage |
| D.13 | census of every collection (2026-09-25): 18 collections, 18,873 listed, 16,898 on disk, 12,123 passing the field gate; expected L6 322, four-lumbar 161, Castellvi II-IV 907-1,813, T13 38-119 [E]; called L6 two-labeller 21, single 18; T13 single 16; review 84; 843 GPU-hours; tier 2 (chest) 29,479 CTs, 2.9 TB refused by the stopping rule; gated Merlin alone about 447 L6 [E]; storage 4,482 GB of 20 TB | `docs/CENSUS_TABLE_2026-09-25.md` | DISPUTED: "on disk" and "field gate" are one high in every collection checked except PANORAMA (`data_platform/DATA_MANIFEST.md` L175, L3698-3703 in spinesurg-ct-nnunet); the CNS 2026 table copied the high figures; cause NOT RECORDED |
| D.14 | labellers on 70 externally labelled TotalSegmentator CTs: A found 12 of 28 L6 (6 no count), B 17 of 28 (9 no count), both 9; T13: A 5 of 7, B 0 of 7; false L6 A 2, B 1 | `results/transitional_registry/acquisition/validation/VALIDATION.md` (the "both 9" is read from its cross table) | CURRENT; B is scored on its own training images |
| D.15 | A and B on CTSP against reader truth, before / after the 2026-09-24 rules: two-labeller L6 12 calls, 6 right [25.4, 74.6] -> 7 calls, 5 right [35.9, 91.8]; L6 reaching the two-labeller tier 6 of 18 -> 5 of 18 | `results/transitional_registry/cobra/labeller_validation_ctsp.md` | CURRENT |
| D.16 | TotalSegmentator-stream two-labeller L6 on CTSP: right 6 of 10 | `results/transitional_registry/REGISTRY.md` "What is not known" | CURRENT |
| D.17 | Moller-mask stump flag against the VerSe read: 65.7 % sensitive; the foramina counter fails on normals | `docs/ruleclass/CLASSIFIERS.md` R27, R31 | CURRENT |
| D.18 | CTSP read prevalence against priors: L6 18 / 789 = 2.3 % (prior 3.2 %); four-lumbar 9 / 789 = 1.1 % (1.6 %); only 33 Castellvi-graded against 71-142 expected | `HANDOFF/literature_state/power.md` section 4 (spinesurg-ct-nnunet 097933a; Greg-only file, not copied here); the numbers are restated in `HANDOFF/LITERATURE_STATE.md` section 5.2 (same repository and commit; Greg-only, not in this folder; this row is the extract) | CURRENT |
| D.19 | ruleclass tier lists (2026-09-27 00:20-00:40): 21,622 CTs (21,603 persons); tier 1 5,094 (CTSP 802 + TS-benchmark natives 1,602 + COBRA 692 + 1,997 flagged + 1); tier 2 12,217; untiered 4,311 (PANORAMA pending 1,114, 210 TS scans where SPINEPS failed); tier-1 flags L6 148 (registry) + 303 (screens), T13 14 + 82, unresolved 129, review 1,168; children 114 / 442; both junctions in field 2,951 / 8,050; raw-id SPINEPS masks 108 / 422 | `docs/ruleclass/TIERS.md` | CURRENT lists. DISPUTED small counts: `RESUME_2026-09-22_PM.md` L134 says 5,095 / 12,218 / 4,312 (trust TIERS.md); grid `CORPUS.md` says 21,655, a 33-CT difference, unexplained |
| D.20 | ruleclass state on 2026-09-27 17:00: 228 jobs running, 315 pending; Moller fast pass 1,801 of 5,094 tier-1 CTs; pelvis 0; total_v3 0 | `docs/RESUME_2026-09-22_PM.md` L29, L55 and `docs/grid_records/JOBS_RECORD_2026-09-27_1544.md` (spinesurg-ct-nnunet 097933a) | what arm B finished after 2026-09-27: NOT RECORDED on the laptop; arms A and pelvis: rows G.1-G.2 below |
| D.21 | every earlier pelvic cue for Castellvi on CTSP was falsified or weak: ala rise AUC 0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599 | `docs/CASTELLVI_SCREEN_BLIND_SPOT.md` (CTSpinoPelvic1K 7ddfe38; copied into `../03_ctspinopelvic1k_dataset/`) | REFUTED cues; rule 2 gates nothing until a reference half is frozen |
| D.22 | rule 1's second step already ran on CTSP: 18 six-lumbar spines split A 11 / C 4 / B 1 / B-or-C 2 | `docs/ruleclass/CLASSIFIERS.md` R30 | CURRENT |
| D.23 | four-rule pre-registration DRAFT v1 (commit f15da62, 2026-09-27 16:47): freeze block blank; "every number this document produces is calibration, not a result" | `docs/ruleclass/PREREG_rules.md` section 9 | OPEN (unsigned) |
| D.24 | the R + C = 22 rule: one count (N != 23); computable on 14 of 1,175 spines (1.2 %; VerSe 14 / 374, CTSP 0 / 801); C1 is labelled on every VerSe case carrying C2, so a detector that boxes C1 flags every normal spine (specificity 0.000); holding false alarm at 5 % needs a per-body miss rate at or below 0.223 %; centre-to-centre spacing (p99 ratio 1.17, threshold 1.6) finds a missing body | `docs/ANOMALY_RULE_EVALUATION.md`, `docs/anomaly_rule_evaluation.json`; job 40414996 | REFUTED; removed from the manuscript on Greg's order |
| D.25 | grid `~/verse_drr` holds 13 exact duplicate renders (`glgl003` ... repeating `gl003` ...) | catalog D.25 | CURRENT fact |
| D.26 | VerSeFusion manifest `has_T13` claims 18 spines; truth 6 (six of the eighteen carry an L6 instead); `verse707` is a genuine table-vs-mask conflict | `memory/versefusion-t13-flag-wrong.md`; re-counted on this copy: 18 True of 374 rows (`results/versefusion_grid_derived/HAS_T13_IS_WRONG.md`) | CURRENT trap |
| D.27 | distinct transitional counts by date, never mixed: 749 anomalous spines (09-17); 81 (09-23 inventory); 89 (09-23, superseded: 12 TS raw-id selections); 194 persons (09-23 subtypes); registry L6 146 / T13 14 (09-24); 196 rendered CTs (09-24); tier-1 flags L6 148 + 303 (09-27) | the Greg-only working note topic 2 (`../01_carm_level_detection/docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md`; removed from this folder in the final pass) B.4 | reference |

## 2. Labeller calibration and the real-frame count (catalog A16.6-A16.8)

| id | claim | file | status |
|---|---|---|---|
| A16.6 | COBRA2026 screen: 91 unread test-side calls (L6 38, T13 45, four-lumbar 8); persons with both junctions in field and an exported frame: 7 at-risk, **4 two-labeller and 3 single-labeller** (L6 3 = 2 + 1; sacralised L5 or four-lumbar 4 = 2 + 2; T13 0) -> error-free Wilson bound 64.6 % | `results/transitional_registry/REGISTRY.md` table C; `results/transitional_registry/cobra/rows.csv`; `SchwingNet/packet_src/persons_available_2026-09-24.json` (spinesurg-ct-nnunet) | CURRENT [AUTO-TRUTH] [WORDING]: the manuscript prints "a two-labeller count ... found seven" |
| A16.7 | at-risk CT test persons: 51 (L6 43, four-lumbar 5, T13 3), 36 rendered -> 93.0 % if error-free; most are in the encoder's training lineage | same packet json | CURRENT |
| A16.8 | **labeller calibration: VERIDAH's L6 call matched the CTSP readers in 10 of 24; T13 in 0 of 52** | `SchwingNet/results/spineps_ids/IMPACT.md` L230; `SchwingNet/results/stats_review2/recompute.json#S4_cobra_call_yield` (spinesurg-ct-nnunet) | CURRENT |

## 3. The grid on 2026-10-08 (read-only pass 22:20 UTC; `MANIFEST_GRID.md`)

| id | fact | file |
|---|---|---|
| G.1 | arm A (TotalSegmentator) at 2026-09-29 04:23:52: tier 1 5,094 = done 3,166 + exists 1,927 + failed 1 (remaining 1); tier 2 12,217 = done 10,398 + exists 968 + failed 3 + pending 848 (remaining 851, 19.7 GPU-hours at the measured mean); the pending CTs by collection: kidney_thoraxabdomen 176, nlst_pilot 484, panorama 155, idc 22, aortaseg60 2, quadra_hc 4, abdomenatlas 3, fdg 2 | grid `/rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md` |
| G.2 | pelvis arm gate: `mode tta`, `n_timing 0`, `tier2_go false`, "tier 2 ready, NOT submitted: no projection"; written from zero timing CTs; the production array never ran | grid `/rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/_timing/DECISION.json` (621 B, 2026-09-29 08:21) |
| G.3 | `/rs/rs_grp_oschome/go2432/ruleclass` 48.579 GB, 163,587 files; `CORPUS.md` 30,381 B says 21,655 CTs against the tiers' 21,622 | census of job 40580051 (`../10_data_platform_grid/`) |
| G.4 | `/rs/rs_grp_oschome/go2432/data/anomaly_harvest` 325.817 GB, 1,063,032 files; PANORAMA's `calls/`, `rows.csv`, `registry_rows.csv` exist, row counts not read | the same pass |
| G.5 | `/rs/rs_grp_oschome/go2432/review_tree` does not exist; `~/lstv-detector` is ABSENT; `~/VerSeFusion/data` is a symlink into Ceph since 2026-10-08 10:39 with `data.pre-ceph` still beside it; B06 (VerSeFusion) VERIFIED 14/14 | the same pass; `plan/runs/B06/STATUS` |

## 4. The VerSeFusion line (2026-05)

| id | fact | file |
|---|---|---|
| V.1 | 374 scans refused from VerSe'19 + '20, all (P,I,R) on disk; patient-level 5-fold splits | `results/versefusion_grid_derived/manifest/manifest.csv` (374 rows), `splits_5fold.json`; `orientation/orientation_audit.csv` (374 rows) |
| V.2 | VERIDAH corrections: 25 rows in `configs/veridah_corrections.csv` of the VerSeFusion repository (26 lines with the header); the 2026-05-08 reader sheet flags T13 = 1 on 14 of its 25 rows and TLTV = 1 on 16 | `results/neurips_2026-05/verse_veridah_labelcorrection.csv` (counted on this copy); `results/versefusion_grid_derived/hf_staging_lstv/corrections/veridah_manifest.json` |
| V.3 | the 68-scan LSTV subset card: 18 t13_supernumerary, 44 lumbarization, 6 t12_absent by its headings; the 44 matches `has_L6` True on 44 manifest rows; the 18 is the wrong flag of D.26 | `results/versefusion_grid_derived/hf_staging_lstv/BROWSE_BY_CLASS.md`; `HAS_T13_IS_WRONG.md` |
| V.4 | 25 before/after renders with `renders_manifest.json`; 7 disputed cases (verse509, 512, 513, 557, 587, 593, 599) where the release and its audit disagree about the phenotype | `figures/veridah_renders/`; `figures/disputed_renders/` |
| V.5 | per-scan correction json: `corrected/` holds 375 json = 373 `scan-*_meta.json` (the source held 374 `scan-*` folders; `scan-verse606/scan-verse606_meta.json` was a cloud-only placeholder on the laptop on 2026-10-08 and is not in this copy) + `veridah_manifest.json` + `renders/renders_manifest.json`; `unified/` holds 375 json = 374 scan meta.json (none missing) + `unify_manifest.json`; counted on this copy 2026-10-08 | `results/versefusion_grid_derived/corrected/`, `unified/`; `MANIFEST_LOCAL.md` section 3 and Appendix B |
| V.6 | the `Lumbosac_Castelvii_Class.csv` worksheet of 2026-05-06 carries 19 IIIb entries and is stale against the 33-record CTSP consensus of 2026-09 | `results/neurips_2026-05/Lumbosac_Castelvii_Class.csv`; the consensus is `docs/castellvi_consensus.csv` in CTSpinoPelvic1K 7ddfe38 |
| V.7 | whether VerSeFusion was submitted to NeurIPS Datasets and Benchmarks: not recorded | `docs/handoff/OPEN_QUESTIONS.md` A8 |

## 5. CTSpinoPelvic1K-Syn (2026-06-11)

| id | fact | file |
|---|---|---|
| S.1 | a scaffold: `castellvi.py` (taxonomy, the Ia-IV matrix) and `manifest.py` (SYNTH tagging, origin records, split-leak audit) are real; `procedural.py`, `blend.py`, `refine.py`, `cli.py` are stubs; `fuse_split.py` is a deterministic L6-sacrum boundary splitter (commit 7098eb1); no synthetic case was ever generated | `code/ctspinopelvic1k_syn/README.md` "Status"; local git 7098eb1, no remote; this folder is the only copy |

## 6. The MRI lstv-detector line (AACA 2026)

| id | fact | file |
|---|---|---|
| M.1 | RSNA 2024 lumbar MRI: 282 studies; aligned 232, offset +1 19, offset -1 24, other 1, insufficient 6; VERIDAH L6 present 31 (confirmed 21, rejected 9); mean best Dice 0.857 +/- 0.028; L6 false-positive rate 29.0 % | `results/aaca_lstv_mri/lstv_cohort_summary.csv`; `lstv_per_study.csv` (283 rows), `lstv_alignment.csv`, `lstv_l6_subgroup.csv` |
| M.2 | no ground truth; thresholds literature-derived; accuracies estimated 65-90 % by task; "validation against even 20-30 CT-confirmed LSTV cases" needed | the `README.md` sections 15-17 of lstv-detector `no_angles` 84636d6 (`MANIFEST_CODE.md`) |
| M.3 | the AACA 2026 submission record and the labelling manual | `docs/aaca_lstv_mri/Submission_Summary.pdf`, `LSTV_Vertebrae_Labeling_Manual.pdf` |

## 7. Superseded and by what

| superseded | by |
|---|---|
| the pooled co-occurrence OR 12.8 (D.2) | 3.61 [2.08, 6.27] on VerSe 280 fully graded |
| the 2026-09-23 inventory 81 and the 89 with raw-id selections (D.27) | the registry L6 146 / T13 14 of 2026-09-24 (D.8) |
| the manuscript twin `tables/tab4_transitional.md` "91 (57) ... 93.7" (catalog A16.10) | "91 (7) ... 93.0 (51 CT); 64.6 (7 real)" (A16.6-A16.7) |
| the census table's "on disk" and "field gate" counts (D.13) | one lower in every collection but PANORAMA; corrected table not yet written (`TODO.md` step 1) |
| `RESUME_2026-09-22_PM.md` L134 tier counts 5,095 / 12,218 / 4,312 | `docs/ruleclass/TIERS.md` 5,094 / 12,217 / 4,311 |
| the NLST T13 9.3 % | 5 of 367 after the rib rule (D.12) |
| `memory/anomaly-manifest-sources.md` 34/16/2 | 749 (D.1) |
| the R + C = 22 rule | refuted (D.24) |
| the pelvic Castellvi cues (D.21) | refuted; rule 2 waits for a frozen reference half |
| VerSeFusion `has_T13` 18 | 6 (D.26) |
| "546 rendered review cases" (`docs/handoff/OPEN_QUESTIONS.md` A17, `../_plan/PLAN.md`, and the first build of this folder) | 446 registry review cases (verse 71 + ctsp 72 + totalsegmentator 137 + cobra 79 + other_ct 87; `REGISTRY.md` "Review queues", D.9) plus 103 labeller-validation renders = 549 tiles in `contact_sheets/index.csv` (spinesurg-ct-nnunet 097933a, counted 2026-10-08); no file records a 546 |

## 8. What is not known (recorded, not guessed)

- What arm B (Moller fast and full) finished after 2026-09-27 17:00; the contents of `arms/pelvis/<collection>` (OPEN_QUESTIONS B1).
- PANORAMA's screen results: the row counts of its `rows.csv` and `registry_rows.csv` (B2).
- The 33-CT difference between `CORPUS.md` and the tiers (B3); which of the 1,186 near-duplicate alias candidates are the same person (B4); the cause of the census table's one-high counts (B5).
- Whether `tools/transitional_review/` self-tests ever passed; the outcome of workflow wf_ded52e0e-cd1 (C21).
- The full name, department and HF user of the stage-2 reviewer "Dr Tech" (A18).
- Whether the Dataset813 folds finished or were scored (`memory/lstv-oneshot-training-run.md`; catalog C5.3).
- Where the grid tree of lstv-detector went (`~/lstv-detector` absent on 2026-10-08); whether the eleven 3-D HTML renders under the VerSeFusion line folder equal those under the AACA folder (same study ids, not hashed).
- Whether VerSeFusion, the BIBM paper or the SPIE abstract were submitted (A8).
