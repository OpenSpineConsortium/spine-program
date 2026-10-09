<!-- spine-program/08_render_devices: copy of spinesurg-ct-nnunet 097933a HANDOFF/LEAKAGE.md (copied 2026-10-08; redactions, if any, are listed in MANIFEST_LOCAL.md section 3). Laptop spellings of the path prefixes (`C:/` drive paths, the session scratchpad, the memory folder) are history, not dependencies: read them through this folder's CLAUDE.md "Prefixes in the copied documents". -->

# Leakage: how "held out" is enforced, how to run the checks, what they found

Written 2026-10-08 from `working_notes/topic3_dataset_usage_leakage_rsna.md` §7-13, `working_notes/topic1_schwingnet_carm_results.md`
§7, `working_notes/topic2_scaling_samples_anomaly_power.md` Part D and the files they cite. Path prefixes as in
`RESULTS_CATALOG.md`. The commands to run are also in `RECIPES.md` §10.

---

## 1. The rule

Greg, 2026-09-23 (`sn:results/eval_gate/EVAL_LEAKS.md` opening): an evaluation item is held out for a checkpoint only if
its **patient key** is in neither the training set nor the validation (selection) set of that checkpoint **or of any
ancestor** it was initialised from. A derived image (a DRR, a styled frame, a crop) inherits the person of its source CT.
Only public ImageNet / COCO weights are exempt as ancestors, and only when declared. **Unknown is not clean**: an
unkeyed item, an unresolved lineage link or a check that did not run counts as a failure.

The definitions behind it (`ssn:docs/DATA_ACCOUNTING.md` §1, §5):

- **An item is one acquisition** (one exposure or one CT series), not a file. Three keys: `store_key` (sha256 of the
  bytes), `pixel_key` (`pix_sha256` of a 0.5-99.5 percentile 8-bit reduction; `vol_sha256` of a 64^3 resample) and
  `item_key` (`canonical_id`, assigned by `tools/data_alias.py canon` after alias resolution). Compare rows only after
  reading `content_key_kind`.
- **Splits are enforced on the patient key, duplicates on the item key.**
- **Validation is seen.** A split that chose a checkpoint shaped it, so `tools/holdout.py`, the gate and every check count
  training AND validation as seen; `holdout.trained_on(..., train_only_because="<why>")` is the only exception.
- **Lineage is followed.** A checkpoint has seen everything its ancestors saw (`PUBLIC_ROOT_RX`, `PUBLIC_TORCHVISION` in
  `tools/checkpoint_lineage.py` declare the exempt roots).
- **Identity comes from metadata first, the file name last**: DICOM PatientID / StudyInstanceUID, then the release
  manifest, then annotation `patient_id` and other fields, then a crosswalk, then the file name
  (`context/key-patients-from-metadata-not-filenames.md`; `ssn:docs/PATIENT_IDENTITY_SPEC.md` §1-5, resolution order L0-L9).

---

## 2. The checks (CHK-1 to CHK-9)

From `ssn:docs/DATA_ACCOUNTING.md` §5 and §5.1.

| id | tests | implemented by | run in the G3 split? |
|---|---|---|---|
| CHK-1 | item disjointness: no acquisition on two sides | `tools/leak_check.py` row `2_within_collection_merged_key` (in part); `tools/make_split.py` CHK-1, CHK-1b | yes |
| CHK-2 | alias closure: one item under two names counted once (the NHANES failure) | row `2_...` plus `alias_gaps`; `make_split.py` CHK-2 (62 alias edges) | yes |
| CHK-3 | patient closure, including derived items: a person and all their renders on one side | rows `1_within_collection_builder_key`, `2_...`; `make_split.py` CHK-3, CHK-3b | yes |
| CHK-4 | derivation closure: parent and child on one side | row `5_render_pose_duplicates`; `lineage.json` `leakage[]`; `make_split.py` CHK-4, CHK-4b (pose donors, WARN only: 8,082 training renders under the poses of val, test or held real subjects, of which 2,720 under test poses: DeepFluoro test 1,143 + COBRA test 992 + C-ArmLSpine test 585; `sn:results/rare_class/split_plan.md` CHK-4b) | yes (WARN) |
| CHK-5 | a held-out device or corpus is held out whole | rows `4_eval_vs_training`, `6_styled_vs_real_device`; `make_split.py` CHK-5 | yes |
| CHK-6 | near-duplicates across splits (pHash, then NCC64 >= 0.97) | `tools/data_alias.py canon --pixels`; `tools/or_audit_dupes.py` | **NOT RUN** |
| CHK-7 | undeclared aliases by store or pixel key | `alias_groups.json` groups spanning undeclared roots | **NOT RUN** |
| CHK-8 | orphans and coverage | `leak_report.json` `census` and `verdict`; `make_split.py` CHK-8 (WARN: 17 unkeyed AASCE `coronal` films), CHK-8b | yes (WARN) |
| CHK-9 | evaluation against selection and lineage, for every quoted number | `tools/leak_check.py chk9` over `sn:results/eval_gate/quoted_results.json`, `$RS/data/or_ready/eval_gate/touched.json`, `eval_sets.json` | yes, 563 rows (§5) |

## 3. The tools, by layer

| layer | tool | what it does | source |
|---|---|---|---|
| person keys | `ssn:tools/patient_keys.py` (`key_for`, `key_any`, `canon_key`, `resolve_key`) | one key per person across naming schemes (Dataset813 crosswalk, NHANES pairs, VerSe series -> subject via `--verse-manifest`, implant -> source CT, scoped Bournemouth and C-ArmLSpine sweep schemes); refuses names it cannot key | docstring; `PATIENT_IDENTITY_SPEC.md` |
| tests | `ssn:tools/test_patient_keys.py`, `ssn:tools/test_leak_check.py`, `ssn:tests/test_eval_gate.py` | the two cross-naming defects collapse; leak_check fixtures; the arc leak, two spellings, declarations, `holdout.py`, CHK-9 | `DATA_ACCOUNTING.md` §5.3 |
| bank builder | `ssn:tools/make_context_crops.py --patient-json` | one split over people across all `--drr` roots; refuses unkeyed cases (`--allow-unkeyed` overrides); fails if anyone is on both sides; records the key file in `meta.json` | `ssn:docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md` "The fix" |
| bank and split audit | `ssn:tools/leak_check.py check` | builder-key disjointness; cross-source merged-key disjointness; one source twice under two names; eval vs training; render pose duplicates; styled corpora vs the real device and pose donors; hash evidence corroborates, never merges two keys | docstring |
| content chain | `ssn:slurm/data_accounting.sh` -> `data_ledger.py build/summary` -> `data_alias.py canon` -> `data_lineage.py build` -> `leak_check.py check` -> `fig_data_flow.py` | item ledger, alias classes, lineage graph, leak report, three-panel figure; exits non-zero on FAIL or on a stage that produced nothing | `DATA_ACCOUNTING.md` §2, §6 |
| person split (G3) | `ssn:tools/make_split.py plan/apply` (`sn:slurm/g3_split.sh`) | person hash `sha256('g3|<seed>|<key>')`, 80 / 10 / 10; transitional 50 / 10 / 40 per subtype; real transitional subjects to test; COBRA hold rule; union-find alias folds; writes `~/split_final.json`, `split_leak_report.json` | docstring; `sn:results/rare_class/split_plan.md` |
| independent split check | `ssn:tools/g3_leak_intersect.py`, `ssn:tools/g3_split_verify.py` | a second, code-independent intersection of detector lists with the split's test, hold and excluded persons | docstrings |
| checkpoint lineage | `ssn:tools/checkpoint_lineage.py` | `touched.json`: train, val and touched keys per checkpoint and ancestor; closes gaps only from recorded evidence; unresolved links carried to descendants | `DATA_ACCOUNTING.md` §5.2; `sn:results/eval_gate/LINEAGE.md` (306 checkpoints, 133 with an unreadable link) |
| evaluation gate | `ssn:tools/eval_gate.py` (`assert_unseen`, `carry`, `stamp`, `gate_evaluation`) | every evaluator keys its items, walks the chain and refuses a seen or unresolved pair before scoring; writes the verdict and `weights_sha256` into the result; `--not-held-out "<reason>"` is the only way past and is printed; eval_gate/2 refuses a block whose sha set differs | `DATA_ACCOUNTING.md` §5.3; wired into about 40 evaluators |
| seen cases | `ssn:tools/holdout.py` | the cases a model has SEEN (train AND val since 2026-09-23); raises when a bank is missing (after the 2026-09-20 deletions left `--holdout-bank` empty) | docstring; `context/grid-quota-and-deleted-banks.md` |
| unseen lists | `ssn:tools/unseen_cases.py` | what a checkpoint's chain never saw (v9: 70 TotalSegmentator + 1 CTSP + 0 VerSe renders) | `context/ts-bench-inside-v9-bank.md` |
| SPINEPS ids | `ssn:tools/spineps_ids.py` | raises on raw SPINEPS instance ids (masks before 147428d) | `context/spineps-ids-can-be-scrambled.md` |
| excluded sources | `ssn:tools/excluded_sources.py` (`assert_clean`, REASONS) | refuses excluded corpora (Mendeley re-encodings of BUU; FluoroCap) at list-building time | `sn:supplement.tex` "Data integrity and quality controls" |
| real-frame admission | `ssn:tools/realxray_banks.json` + `ssn:tools/realxray_train.py check` | fail-closed admission list; device banks must not share a case id (checked on disk); derived banks never enter pooled or LODO arms | JSON `_README` |
| real-frame split audit | `ssn:tools/or_audit_splits.py`, `ssn:tools/or_audit_dupes.py` | split disjointness by case on the four real-frame sets and fold banks; NCC near-duplicates against films and FluoroCap | `sn:results/DATA_CONTRIBUTION.md` §6 (`AUDIT.md`, grid only) |
| pooled list builder | `ssn:tools/devcorpus_build.py lists --design P` | refuses if a CT subject or real specimen is on two sides; **designs A and B do not run this refusal** | `DATA_CONTRIBUTION.md` §6 finding 2 |
| leak size | `ssn:tools/leak_effect.py` | same-run comparison of in-train vs held-out spines on a sweep, cluster bootstrap | docstring |
| the holding index | `ssn:data_platform/db/` view `v_subjects_in_several_sources` | "the query that would have caught the NHANES double inclusion"; indexes only folders with a README.yaml | `ssn:data_platform/db/README.md` |

### Device designs (LODO and pooled)

- **LODO (leave one device out)**: the held-out device is absent from training frames, from the poses of the training
  renders and from the calibration terms of the initialisation; real frames split by specimen or case; renders follow
  their CT subject (`ssn:docs/RSNAI_PLAN.md`; `MODEL_CARD.md` §3.1; `context/k-devices-one-network.md`).
- **Design P (pooled)**, Greg 2026-09-22: every device's training frames in one detector, scored on every device's test
  split; reported only beside the LODO number (`context/pooled-vs-lodo-device-designs.md`).
- **Known exposure of design A**: it renders every card under the Cios Fusion pose pool, which includes DeepFluoro test
  specimen 18-1109, so arms that "hold DeepFluoro out" trained on renders under that specimen's poses; design B does
  not and reads higher (`DATA_CONTRIBUTION.md` §6 finding 1).
- **C-ArmLSpine: a case is an acquisition, not a proven person** (149 cases on five acquisition dates); the
  cross-validation is reported both case-grouped and acquisition-day-grouped (`PATIENT_IDENTITY_SPEC.md` §4;
  `context/identity-audit-findings.md`). **What 149, 148 and 141 count.** 149 is the number of C-ArmLSpine case folders released (acquisition sessions on disk: 299 spot exposures over 149 cases, `sn:NUMBERS.md` L182, L295; `ssn:docs/PATIENT_IDENTITY_SPEC.md` L130, L239-244). 148 is the number of cases whose frames were scored (296 frames of 148 cases; case134's two exposures were missed by a folder walker, `sn:NUMBERS.md` L295; `sn:sections/methods.tex` L47 "148 of 149 cases"). 141 (lateral) and 142 (AP) are the cases that contribute at least one scored vertebra to the whole-frame cells (`sn:results/eval_gate/closure/cv_v9/CV_V9.md` L35, L45: the case count varies by cell, 131-143); which cases drop out of each cell and why is not recorded in the files read. Whether any of these cases are the same person cannot be established.

---

## 4. Patient keys per corpus

From `PATIENT_IDENTITY_SPEC.md` §2 and `DATA_ACCOUNTING.md` §4.

| corpus | key | trap |
|---|---|---|
| CTSpinoPelvic1K | `ctsp:<TCIA token>` via `manifest.json` (token is not the release id; 0145 = token 100; 34 tokens are `CTC-<10 digits>`, match `[A-Za-z0-9-]+`) | four name shapes; implant variants |
| TotalSegmentator | `ts:<sid>` after release fold (content override) | v201 / v300 renumber (s1406-s1429: 24 split + 15 merged); no patient id exists |
| VerSe | `verse:<subject>` (374 series -> 355 subjects) | `CTSP_VERSE_` prefix; `glgl` doubles |
| NHANES II | `nhanes:<5-digit sample person>` from `NHANES_nhanes_*`, `NH_*`, `NHANESPS_*` | three schemes |
| BUU-LSPINE | `buu:<NNNN>`, AP and lateral together | "(1)" copies; two byte-identical case pairs |
| CSXA | `csxa:<SSSS>` | one image = one person assumed |
| VinDr | `vindr:<study_id>` | image-level keys leaked 77.8 % of `vindrps` val |
| Mendeley | folds to `buu:` (500) or `vindr:` (13); 71 refused | redistribution |
| AASCE | `aasce:<index>`; `coronal` names refused | the index may not be a person |
| Spinal-AI | `spinalai:<similarity group>`, `person_key=false`, whole corpus train | no person exists |
| FluoroCap | source document or video; never a patient count | over-merges by design |
| C-ArmLSpine | `carmlspine:case<N>`; never `PatientID` | case = acquisition; case134/ori carries a real name (never print it) |
| DeepFluoro | `deepfluoro:<accession>` | the fluoro `PatientID` is wrong |
| COBRA2026 | `cobra:<case>` on the paper's authority | centres D / F / G stripped |
| Geneva, Ljubljana | one object each, test only | Geneva keyed per view until 2026-09-24 |
| devcorpus | `ts:<subject>` | 17 held subjects appear in five other banks |

---

## 5. What the checks found, in the order found

The two historical leaks first; they are why the rule exists.

### 5.1 Historical leak 1: NHANES II in the banks twice (found 2026-09-22)

`~/films_drr` and `~/nhanes_drr` both contain the 543 annotated NHANES II films, under different names; the banks split
each source separately, so **48 of 54 NHANES validation patients had their twin in training**: measured on allspine v6 and v7 (48 of 54
each); v2 was built the same way (both sources in its build log) but was not counted before it was deleted; v5 is
not recorded (`ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md` lines 17-19). The construction inflated every pooled
real-film number of that era (the mixed-length head's 97.47 %, the 2026-09-17 scaling sweep,
the selective-prediction 99 %) (`ssn:docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`; `context/nhanes-double-inclusion.md`).
**Fix**: v8 dropped `~/nhanes_drr` and keyed every root by person across sources (`tools/patient_keys.py`,
`make_context_crops --patient-json`); `tools/subset_bank.py --drop-val-twins` was written for the old banks. **Still
present in the C-ArmLSpine fold banks** (`nhanes` 303 + `nhanes_drr` 277 crops), though no quoted number scores NHANES
with them (`ssn:docs/MODEL_CARD.md` §3.2).

### 5.2 Historical leak 2: CTSpinoPelvic1K under two names (found 2026-09-22)

`ctsp_drr` names a case `CTSP_COLONOG_<token>`; the physics renders name it `ctsp_<release id>`. A per-source split
therefore put **371 people on both sides of the v6 / v7 split, 357 from naming alone** (the same rule applied to v2)
(`ssn:docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`; `context/split-leak-cross-naming.md`). **Fix**: the
`patient_keys.py` crosswalk (token map from `manifest.json`), one split over people across all roots, the builder refusing
unkeyed cases; closed in v8 / v9.

### 5.3 Everything found, chronologically

| date | finding | size | affected | fix | status |
|---|---|---|---|---|---|
| 2026-09-14 | the deployed level bank `films_all2` had no T2-T11, T13 or L6 crops | 0 crops for 11+ classes | that week's level model | all-spine banks | closed (`context/level-model-bank-coverage.md`) |
| 2026-09-15 | evaluations scored renders whose CT was in the bank's training split | the v1 "92.7 %" was on training cases | transitional evaluations | `--include-train` default off | closed (same) |
| 2026-09-20 | deleted banks left `--holdout-bank` empty, so evaluations ran on fitted cases | ~90 scripts | any holdout run after the deletion | `tools/holdout.py` raises; 57 references repointed to v7 | closed (`context/grid-quota-and-deleted-banks.md`) |
| 2026-09-22 | NHANES II twice | 48 of 54 val patients (counted on v6 and v7; v2 same construction, not counted) | v2, v6, v7; every pooled real-film number | §5.1 | closed in v8 / v9; **still in the fold banks** |
| 2026-09-22 | CTSpinoPelvic1K under two names | 371 people on both sides (357 from naming) | v6, v7 (v2 same rule) | §5.2 | closed in v8 / v9 |
| 2026-09-22 | VerSe series keyed as subjects | 5 people, 10.5 % of VerSe val | the "clean" v8 bank | `--verse-manifest`; v9 | closed in v9 (`context/identity-audit-findings.md`) |
| 2026-09-22 | `anchor_drr` split seeded on the implant-variant stem | 301 of 801 CTSP people | `anchor_det_v1` own-domain 93.48 % | not quoted | open (bank not rebuilt) |
| 2026-09-22 | VinDr keyed per image, not study | 77.8 % of `vindrps` val | `vindrps`, v7 | `export_vindr_identity.py`; study key in G3 | open for the old banks |
| 2026-09-22 | TotalSegmentator v201 s1406-s1429 renumbered in v300 | 24 split + 15 merged | any `ts:s####` key | G3 folds TS by md5 and shape + affine; `tools/identity/ts_alias.json` not built | partly |
| 2026-09-22 | a C-ArmLSpine case is not a person | 149 cases released, 5 dates (§3 says what 148 and 141 count) | the 98.22 % CV | day-grouped folds reported beside case-grouped | closed by reporting both |
| 2026-09-23 | COBRA derived banks globbed into one detector arm | 5,013 duplicate frames (one patient up to 4 times) | `rx_pooled_1024_init18` (quoted nowhere) | fail-closed `realxray_banks.json` + on-disk disjointness | closed (`sn:results/repairs/cobra-dup-leak_CHECK.md`, job 40416578) |
| 2026-09-23 | the recall-vs-angle curve was scored on the detectors' own selection subjects | 17 TS subjects | old Figure 4d | re-scored on 40 unseen subjects (job 40428072); the leak did not inflate it | closed (curve retired) |
| 2026-09-23 | plain-film naming numbers are on the encoder's selection split | CSXA 99.8, BUU 97.3, NHANES 99.1 % | the film rows | relabelled "selection split" | labelled (`EVALUATORS.md` item 1) |
| 2026-09-23 | `rx_lodo_*` `best.pt` selected on the other devices' test splits | COBRA test 27 / 27 patients | lcurve rows only | only the own held-out device is quoted | labelled (`EVALUATORS.md` item 2) |
| 2026-09-23 | first CHK-9 | 380 rows: the job log reads 35 SEEN, 40 UNRESOLVED, 236 HELD OUT, 69 N/A (`sn:results/eval_gate/chk9/job_40427457.log` L35); `ssn:docs/DATA_ACCOUNTING.md` L350 says 31 SEEN, 240 HELD OUT for jobs 40427275 and 40427457 (a discrepancy; the log is the computed reading; superseded either way) | quoted numbers | gate wired into ~40 evaluators | superseded |
| 2026-09-23 | G3 split: v8 / v9 trained on most transitional val + test persons | 49 / 54 L6, 4 / 4 T13, 14 / 14 sacralised | any v8 / v9 descendant on the G3 test | paper 1 scores no G3 test person; paper 2 trains from ImageNet | rule in place (`split_plan.md`) |
| 2026-09-24 | the EVAL_LEAKS sweep | 563 rows: 81 SEEN, 58 UNRESOLVED (57 trace to the deleted `allspine_v2_r1`) | quoted numbers | v9 re-run of the CV (cv_v9 closure) | **after closure: 380 held out, 81 seen (must stay labelled not held out), 1 unresolved, 101 not applicable** (`sn:results/eval_gate/closure/chk9_cv_v9/CHK9_DIFF.md`) |
| 2026-09-25 | the TotalSegmentator render bench sits inside the v9 bank | 483 of 523 sacrum-bearing spines in v9 train / val | any v9 number on `ts_drr` | `--holdout-bank` matched stems, not keys; use `unseen_cases.py` (71 cases) | rule in place (`context/ts-bench-inside-v9-bank.md`) |

### 5.4 Verdicts by family after the sweep (`EVAL_LEAKS.md` §1-3, §6)

- **LEAKED** families: `embedding_v9` (Figure 2, scored on v9's validation split: L5), `device_cards` (15; L6: two devices
  have one subject, re-read on 12 patient-held-out folds), `fig4a_pairs` (13), `film_naming_v8` (9; L4: no unseen film
  subset exists), `render_vs_film` (7; L2: re-run on 17 unseen spines, the gap holds), `count_only` (2), `lcurve` (2), `arc`
  (1; L1: re-scored on 40 unseen subjects). L3 (the COBRA learning-curve control) is not in the manuscript; L7 (Figure S2a
  pair R^2) was re-run under the held-out fold.
- **UNRESOLVED U1**: every v2-lineage C-ArmLSpine number (its bank was deleted); re-run on v9 (`RESULTS_CATALOG.md` A2-A5).
- **CLEAN** families include `lodo_detector_on_carm` (21), `fig3_scored` (58), `contribution` (99), `counting` (11),
  `pooled_vs_lodo_carm` (4), `case134`.
- **Not measured**: the selection effect of the v9 checkpoint on the alphabet-loss "10 held-out L6 spines" (recall
  56.1-72.4 %), because the encoder kept its best epoch on the split they belong to (`EVAL_LEAKS.md` item 6).
- **Pose dependency reported, not scored**: every `lc_*` list carries all 7,322 styled renders, including 598 under
  C-ArmLSpine test-case poses (`EVAL_LEAKS.md` item 3; `sn:results/eval_gate/EVALUATORS.md` §1.3).

### 5.5 Controls on each accuracy-against-samples curve (`working_notes/topic2_scaling_samples_anomaly_power.md` Part D)

| curve | control |
|---|---|
| 2026-09-17 scaling sweep | none adequate (v2 split per source, NHANES twins); superseded |
| lcurve | test split never in any list; the three real L6 patients removed from every list of every device; checkpoint on a fixed val split |
| det_fill / name_fill | `tools/eval_gate.py` on every model chain against every test image's patient; detection 45 cells and naming 245 cells held out, overlap 0, unresolved 0 |
| film N-curve and ablation | a new render-only encoder (v9 and the G3 encoder both trained on the film persons); test persons outside every cell and outside the encoder's bank; `eval_gate` inside `a5-rows`; every cell `HELD OUT` |
| coverage arms | the 40 unseen-sweep subjects excluded from training; real tests never trained on |
| a5 per-source film numbers | selection split; leak check by patient key: 0 of 549 BUU, 727 CSXA, 52 NHANES val patients in train |
| cv_v9 C-arm per level | v9-lineage re-run; the old lineage reads `held out: False`, 60 unresolved |
| G3 transitional split | leak audit PASS, but 49 of 54 L6 val + test people are in the v8 / v9 training lineage |

---

## 6. How to run the checks

See `RECIPES.md` §10 for the full block. In short: the content chain is two `sbatch` submissions of
`ssn:slurm/data_accounting.sh` (`STAGE=ledger` array 0-15, then `STAGE=rest` afterany; grep `DATA_ACCOUNTING_LEAK_CHECK`
in the stage-2 log); the self-test plants a leak with `tools/diagnostics/make_fake_corpus.py` (it must fail) and builds a
clean tree with `--clean` (it must pass); `python tools/leak_check.py check --out $RS/data/or_ready/leak` (in a job) audits banks and splits;
CHK-9 over every quoted number runs only as the recorded job `sbatch -D /rs/rs_grp_oschome/go2432/data/or_ready/eval_gate
-p reqp --qos=requeue --export=ALL,STAGE=chk9 ~/spinesurg-ct-nnunet/slurm/eval_gate.sh` (a bare `leak_check.py chk9`
has no `--quoted-results`, `--touched` or `--eval-sets`, prints `CHK9 COULD NOT RUN` and exits 3); the G3 person split
(`SchwingNet/slurm/g3_split.sh`) is **frozen** (applied 2026-09-23 20:18:48, job 40426793) and re-running it rewrites
`~/split_final.json` in place, so re-verify only on a copy (`RECIPES.md` §10); `python -m pytest tests/test_eval_gate.py -v`
tests the gate on the laptop (`tools/test_leak_check.py` fails today on one stale fixture, `RECIPES.md` §10);
`python tools/realxray_train.py check --root $RS/data/realxray` (in a job) checks real-frame admission.

---

## 7. What remains open

1. **The content-hash chain has not been run on the real corpus.** `$RS/data/or_ready/data_accounting/` did not exist on
   2026-09-22 (`DATA_CONTRIBUTION.md` §6); no later file records a run; the G3 split marks CHK-6 and CHK-7 NOT RUN. The
   repository copy of `DATA_ACCOUNTING.md` §7 is empty by design.
2. **Box E3 never ran**: the leakage audit over every device-corpus training list (`ssn:docs/RSNAI_PLAN.md`), and designs A
   and B lack the design-P refusal.
3. **The C-ArmLSpine fold banks still hold both NHANES copies, FluoroCap and VinDr** (`DATASET_USAGE.md` §3.2, §5).
4. **The metadata-first keyer of `PATIENT_IDENTITY_SPEC.md` is only partly built.** `ssn:tools/identity/` is empty in this
   checkout; the frozen tables (`ctsp_token_map.json`, `ts_alias.json`, `verse_series_to_patient.json`,
   `vindr_image_to_study.json`, `fluorocap_doc_keys.json`, `deepfluoro_h5_alias.json`) and the bank registry
   `tools/identity/banks.json` are not in the repository; the VinDr map was exported on the grid (job 40416449);
   `patient_keys.py` still reads `patient_id` first for `films_drr` (spec §5).
5. **Assumed identities**: CSXA one image = one person (untested); AASCE index = person (unknown); Mendeley `Screenshot-*`
   films (unknown); TotalSegmentator scans folded by content, persons unknown; COBRA centres D / F / G stripped; the 149
   C-ArmLSpine cases (148 scored; §3); the 768 numeric-id vs 34 `CTC-` CTSP records (settled only by a TCIA query) (spec §4).
6. **81 SEEN quoted rows** must stay labelled as not held out or be removed (the manuscript workflow owns it; whether all
   are labelled in `sn:main.tex` is not recorded).
7. **No weight file of the k-devices half has a SHA-256 in the registry** (`MODEL_CARD.md` §1.3); the gate binds verdicts
   to sha256 only for dumps written after 2026-09-24.
8. **`ssn:splits_5fold.json` at the repository root is an empty file** (0 bytes, 2026-09-12); the CTSpinoPelvic1K
   release's own patient-grouped split is used by nothing and is keyed by TCIA token, not release id
   (`DATA_COMPLETENESS_AUDIT.md` line 21). The release split itself has no held-out test set and never read the lumbar
   count (`RESULTS_CATALOG.md` F.17).
9. **The TotalSegmentator render bench is not held out from the v9 encoder** (483 of 523 sacrum-bearing spines); only 70
   TS + 1 CTSP + 0 VerSe renders are unseen.
