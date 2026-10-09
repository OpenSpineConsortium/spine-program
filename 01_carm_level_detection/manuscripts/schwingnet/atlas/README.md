# ATLAS cards for SchwingNet

Two JSON cards to the RSNA ATLAS 2025-11 schemas (https://github.com/RSNA/ATLAS), written 2026-09-22 and brought to
the six-figure manuscript on 2026-09-23:

- `model.json` — SchwingNet as the manuscript reports it: two detectors never trained on the test C-arm (a film-trained
  YOLO11m-pose body detector at confidence 0.35; the held-out-device YOLO11m vertebra/sacrum detector
  `rx_lodo_carmlspine_1024` at 0.74), the ResNet-18 level encoder, the bidirectional GRU head, the count from the
  detected sacrum and the alphabet coupling. The sweep linker of the earlier drafts is not part of it.
- `dataset.json` — the corpus behind it: Table 1's sources, the real C-arm frame sets, the level bank, the synthetic
  device corpus and, new on 2026-09-23, the transitional test side of the built person-disjoint split.
- `VALIDATION.md` — what `validate_cards.py` checks and every field whose vocabulary could not be confirmed.
- `validate_cards.py` — parses both files, checks required fields, enums and key sets, and (since 2026-09-24) fails
  on a duplicate reference; exits non-zero on any error. Last run 2026-09-24: 0 errors, 5 warnings (the recalled
  RadLex identifiers, as before).
- `update_cards.py` — the only writer of the two cards (was `update_cards_2026-09-23.py`).

## What changed on 2026-09-24 (evening), and why: the comparison is paper 2

Greg moved the LevelCheck / surgeon comparison into a second paper (`SchwingNet/PAPER1_SCOPE.md`,
`paper2_levelcheck/MOVED_FROM_PAPER1.md`). `update_cards.py` was brought to that state and rerun (0 errors, the same 5
RadLex warnings):

| field | before (morning) | now | source |
|---|---|---|---|
| Summary (model) | "the comparison with a LevelCheck model frozen before unblinding is pending (gate G6)" | the three real transitional persons are scored only in cross-validation as agreement with one labeller's read; no held-out transitional person is scored; the comparison is a separate study (paper 2) | `PAPER1_SCOPE.md` |
| Keywords (model) | included "LevelCheck comparison" | dropped | |
| Version, Limitations (5)-(6), Recommendation, Reproducibility, Model performance TRANSITIONAL | the Figure 6 arm; the frozen comparator, the automated reference, 157 / 152 persons against 97.6 % | the split-trained arm is paper 2's (paper 1 shows its development learning curve only); certifying 90 % needs 35 error-free at-risk persons, seven real-frame candidates, none verified; nothing from the comparison is quoted | `results/power/power.json` (`at_risk_pooled.real_counted_with_frame` = 7, `real_reference` = 0) |
| Dataset Summary, Test partition | "six figures"; "Scored in Figure 6 against the frozen LevelCheck model" | five figures, three tables; the test side is not scored in paper 1 and is paper 2's | `PAPER1_SCOPE.md` |
| pointer repair | `rows.pooled.real_verified_primary` (no such key since the 10:32 schema of `power.json`; the updater raised) | `rows.at_risk_pooled.real_reference` and `.real_counted_with_frame` | `results/power/power.json` |

**Still not brought to the manuscript (open):** the cards' naming, field and coupling numbers are read from `results/a4.json`,
`a7.json` and `a9.json` (first-run fold models: 594/617, 606/617, 571/617, 1,079/1,162, 995/1,009), while the manuscript
prints the v9-lineage cells since the G5 fill (595/617, 601/617, 568/617, 1,079/1,159, 991/1,009;
`results/eval_gate/leaks/zeroshot_v9.json`, `results/eval_gate/closure/cv_v9/cv_v9.json`). Re-pointing the updater is a
separate item (`REVISION_LOG3.md` section 8, packet pass).

## What changed on 2026-09-24 (morning), and why

| field | before (2026-09-23) | now | source |
|---|---|---|---|
| References (both cards) | six identical CTSpinoPelvic1K entries: the updater re-appended one per run, although this file called it idempotent; COBRA2026 under a descriptive title with no authors; Grupp 2020 without its issue | one entry each (the updater drops every entry it owns before adding it back; the validator now fails on a duplicate DOI or title); COBRA2026 as the Zenodo record names it (Thummerer A, Rit S, Kamp F, et al., version 1.0.0, 13 July 2026); Grupp 2020 15(5) with its PMID | `REFS_AUDIT.md` rows 25-26; `refs_corrections.bib` |
| Architecture | body detector "from an earlier pose checkpoint" | from detect_v3, itself from COCO-pretrained yolo11m-pose; the sacrum detector's best.pt was selected on the COBRA2026 and DeepFluoro test splits | `results/eval_gate/LINEAGE.md`, `EVALUATORS.md` item 2 |
| Limitations, Model performance | nothing on selection-split numbers | (12) the plain-film naming figures (CSXA, BUU-LSPINE, NHANES II) are the encoder's selection split and are not quoted; (13) only the sacrum detector's held-out-device results are clean, and its parent trained on renders of five of the 17 arc subjects | `results/eval_gate/EVALUATORS.md` items 1-2 |
| Transitional comparator | "a LevelCheck model frozen before unblinding" | frozen at ecae75f and amended before unblinding, by its own rule, at 1897772 (+ efab8dd), 2993f40 and b511985 (the automated reference standard); no comparator value, stratum, endpoint, test or primary hypothesis changed | `git log -- SchwingNet/LEVELCHECK_MODEL.md` |
| Test partition (dataset) | COBRA2026 calls join "only after a human verification" | test persons without a human read enter only through the section 14 automated reference, frozen with its calibrated PPV before unblinding; human-verified truth stays primary; the Figure 6 arm is planned from ImageNet on the training side of the built split | `LEVELCHECK_MODEL.md` s4, s14; `docs/RESUME_2026-09-22_PM.md` (checkpoints 2026-09-23 21:45 and 2026-09-24 05:40) |
| Validation partition (dataset) | "the 17 TotalSegmentator subjects held out of every styled synthetic corpus" | the 17 are the checkpoint-selection side of every styled-corpus arm, so no such arm is held out on them; the real-frame detector's parent trained on renders of five and validated on one | `results/eval_gate/EVALUATORS.md` (corrections table, `tables/tab_corpus.tex:43`) |
| License (model) | "at publication they are to be deposited publicly ... for research use" | the release decision is stated as open: `docs/FLAGSHIP_PLAN.md` s5 releases the weights, `docs/MODEL_CARD.md` 1.4 says not released, and the invention disclosure (s9-10) leaves weights and university ownership to counsel; `packet_src/statements.md` carries both wordings | those three files |
| Version (dataset) | state of 2026-09-23 | state of 2026-09-24; the overnight VerSe and TotalSegmentator v3 screens will change the transitional counts when Table 2 is regenerated, and the card follows the table | `docs/RESUME_2026-09-22_PM.md` |

Checked again on 2026-09-24 (05:45 EDT, through WSL): the Hugging Face mirror's newest commit is still 72cd777 (the 0533
repair); its `dataset_labels.json` still reads "CTSpinoPelvic1K v10" with `"29": "S1"`, its card licence is
`cc-by-nc-4.0` and its LICENSE file Apache-2.0; its KNOWN_ISSUES has no 0533 entry. Zenodo 22797014 (v11, CC BY-NC-SA
4.0, 18 September 2026) is the latest version of the concept record.

## What changed on 2026-09-23, and why

| field | before (2026-09-22) | now | source |
|---|---|---|---|
| headline naming | the five-fold CV lateral 98.22 % with a percentile interval at the 1.000 boundary | zero-shot 594/617 (96.3 %; Wilson on the design-effect-adjusted n 92.0-98.3) first, then case-grouped 606/617 (94.6-99.4) beside day-grouped 571/617 (87.7-96.4), the three-body field 1,079/1,162, the count 979/1,009 and the coupled call 995/1,009 | `results/a7.json`, `a4.json`, `a9.json`; `results/COUPLING.md` rows det74/kfull |
| headline detection | vertebral-body boxes from `or_ready/lodo/curves.json`: 5.23 % vertebrae, 76.79 % sacra at 0.75 | the manuscript's convention and operating point: whole-vertebra boxes at the cross-device 0.74, 231/287 (80.5 %; 74.1-86.8) and 43/56 (76.8 %; 64.3-89.3), with the 0.25 figures beside; body-box recompute named as pending (G5) | `results/a1.json` |
| network | detector, encoder, head, sweep linker | two detectors, encoder, head, count, alphabet coupling (Figure 3) | `sections/methods.tex` "The network"; `docs/MANIFEST_DATA_MODELS_RESULTS.md` (detector_v5z_final); `tools/alphabet_couple.py` |
| embedding | not in the card | allspine_v9 encoder with its SHA-256; nearest-person same level 74.9 %; L6-L5 silhouette 0.35 (10 persons) against L5-L4 0.23 | `results/figure2/figure2_metrics.json` |
| transitional | the claim marked pending | the frozen LevelCheck comparison (pending G6), the power arithmetic (3 real persons, best-case bound 43.9 %; 157 persons to beat 97.6 %) and the leak that forces a new arm (49 of 54) | `LEVELCHECK_MODEL.md`; `results/power/power.json`; `tables/tab4_transitional.md` |
| ethical review | rested on the unsigned self-determination tool; the signed 2026-269 notice was an image-only scan "not read" | the signed notice read page by page: WSU IRB HPR 2026-269, 2 September 2026, not human participant research; and its scope, which excludes sources behind a data use agreement, so VinDr-SpineXR (PhysioNet Restricted Health Data Use Agreement, in the fold banks) is flagged as outside it | `CTSpinoPelvic1K-1/2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf`; PhysioNet project page; `slurm/reproduce_all.sh` |
| contact | [e-mail withheld] (docs/DATASHEET.md section 7) | [e-mail withheld], the corresponding address of the manuscript; affiliation Department of General Surgery, WSU School of Medicine / DMC | `packet_src/front_matter.json` |
| licence | "not released" | the release plan of the availability statements: private now, public deposit at publication for research use, terms no less restrictive than non-commercial because of the NC, NC-SA, NC-ND and DUA sources; the licence itself is the author's open decision | `packet_src/statements.md` |
| CTSpinoPelvic1K | 0533 "a truncated download" | 0533 was truncated in the public mirror and replaced there on 2026-09-23 (the banks still hold 801); the Zenodo record is v11 CC BY-NC-SA 4.0, while the mirror still serves v10 labels with other licence metadata | Zenodo API record 22797014; Hugging Face paths-info and dataset_labels.json |
| dataset partitions | no transitional partition | a `Test` partition: the L6 and T13 test side of the built split (43 + 3 CT persons, 3 real) | `tables/tab4_transitional.md`; `results/rare_class/split_plan.md` |

The update is `update_cards.py` in this folder: it reads every number from its result file (none is typed), is
idempotent (checked 2026-09-24 by running it twice and validating; before that date it was not, see above), and is
followed by `validate_cards.py`; the text of each card names those files.

## Rules the cards follow

- Only numbers with a clustered interval, a stated operating point and a result file are quoted as performance.
- No number from a bank with a known split leak (allspine v2, v6, v7, v8 for VerSe; anchor_drr; vindrps); those banks
  are named only to state the leak.
- The counting heuristic evaluated in docs/ANOMALY_RULE_EVALUATION.md does not appear.
- No commercial product and no regulatory pathway is named; the conflict statement is quoted as the title page words it.
- No wrong-level surgery rate is derived from any naming accuracy.
- The word the project bans does not appear (`grep -ri` over this folder is clean).

## Still open in the cards (waits on a gate or on the author)

- **G5**: the split-trained arm (bank, split, initialisation, recipe; scored in paper 2); the body detector's training corpus by source and
  split; the vertebral-body box recompute; training-partition performance.
- **G6** (paper 2 since 2026-09-24 evening): every transitional number against the frozen LevelCheck model, variant
  sensitivity and specificity, and the reference behind each test person (human-verified, or the section 14 automated
  reference, frozen in `results/fig6/frozen/auto_reference.json`); the cards quote none of it.
- **Author**: the release decision for code and weights (two wordings in `packet_src/statements.md`); the VinDr-SpineXR
  determination (or retraining without it); the CTSpinoPelvic1K mirror brought to v11 and one licence; an ORCID iD;
  the funding sentence.
- **Registry**: SHA-256 for the fold encoders, heads and the sacrum detector (docs/MODEL_CARD.md 1.3) before any
  deposit.

## Field sources — model.json

| field | sourced from |
|---|---|
| Name, Summary, Architecture | `sections/methods.tex` ("The network", "The level encoder and what it learns"); `docs/MODEL_CARD.md` 1.1, 6.3 (parameter counts, GMAC); `docs/MANIFEST_DATA_MODELS_RESULTS.md` (detector_v5z_final); args.yaml / data.yaml of `rx_lodo_carmlspine_1024` read on the grid 2026-09-22; `slurm/carmlspine_cv.sh`; `tools/train_level_classifier.py`, `tools/head_mixed_length.py`, `tools/alphabet_couple.py` |
| Link, License URL | `git remote -v` (origin) |
| Authors, Contact, Organizations | `packet_src/front_matter.json` (name with middle initial, degrees, affiliation, institutional e-mail) |
| Date | the dates the card was written and updated |
| Ethical review | the signed WSU IRB notice 2026-269 (read 2026-09-23); PhysioNet's VinDr-SpineXR access policy (read 2026-09-23) |
| Funding | none declared; the author confirms on the full title page |
| License | `packet_src/statements.md` (availability statements) |
| References | `refs.bib` entries `grupp2020`, `totalsegmentator`, `verse2021`, `veridah2026`, `claim2024`, `ctsp1k`; DOIs of C-ArmLSpine, COBRA2026 and Geneva from `docs/RSNAI_DATA_MANIFEST.json` |
| Version | the result files named in the field; `results/figure2/figure2_metrics.json` (encoder and SHA-256) |
| Availability | `docs/MODEL_CARD.md` 1.1, 1.3; `docs/MANIFEST_DATA_MODELS_RESULTS.md` |
| Decision threshold | `results/a1.json` (0.74 and how it was chosen); `sections/methods.tex` (0.35, the abstain rule); `results/a7.json` cv5/det/LAT/kfull default_rule; `results/COUPLING.md` det74/kfull |
| Limitations | `results/a1.json`, `a4.json`, `a7.json`, `a9.json`, `a6.json`; `results/figure2/figure2_metrics.json`; `results/power/power.json`; `tables/tab4_transitional.md`; `sections/discussion_limits.tex` (the frozen comparator file is paper 2's since 2026-09-24 and is no longer a source here) |
| Model performance | as the Comments field names, file by file |
| Regulatory information | the conflict statement of `main.tex` / the full title page |
| Use / User, Imaging, EHR | unchanged from 2026-09-22 (schema enums; see VALIDATION.md) |

## Field sources — dataset.json

| field | sourced from |
|---|---|
| Name, Summary | `tables/tab_corpus.md` (Table 1 totals, cells traced in `tab_corpus.sources.md`); `tables/tab4_transitional.md` (transitional persons, the built split); `sections/results.tex` |
| Descriptors | as for the model card; `Version` adds `results/rare_class/transitional_subtypes.csv`, `split_plan.md`, `cobra2026/COBRA_COMPLETE.md` (692 of 692) |
| License | the source licences of Table 1; the Zenodo LICENSE of CTSpinoPelvic1K v11; PhysioNet's VinDr-SpineXR licence |
| Missing information, Noise (16, 17), Sampling | Hugging Face paths-info for `ct/0533_ct.nii.gz` (commit 72cd777, 2026-09-23); `tables/tab4_transitional.md` note (e); `docs/RESUME_2026-09-22_PM.md` (scrambled SPINEPS ids) |
| Partitions: External testing (C-ArmLSpine) | `results/a1.json` cross_device_0.74 |
| Partitions: Test (transitional) | `tables/tab4_transitional.md` rows L6, T13 and note (c)-(e) |
| Everything else | unchanged from 2026-09-22; its sources are the table in the git history of this file (commit before 2026-09-23) |

## What is deliberately not in the cards

- Any transitional accuracy: none exists on a held-out person until gate G6 runs the frozen comparison.
- The three real C-ArmLSpine L6 patients as evidence of correctness: they measure agreement with one automatic
  labeller (one of five anchored frames matched).
- Any pooled real-film naming number from a leaked bank; any selective-prediction figure from the v2 bank; the
  render-only detector's own-domain recall; any millimetre from `verse_drr`; a patient count for C-ArmLSpine,
  FluoroCap, TotalSegmentator or AASCE.
