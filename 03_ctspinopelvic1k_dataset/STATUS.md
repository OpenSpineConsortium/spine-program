# STATUS — the results in hand on 2026-10-08

An extract of `docs/handoff/RESULTS_CATALOG.md` (Part F rows F.1-F.20 and F.46-F.50, Part C5), of the
Greg-only `HANDOFF/MANUSCRIPTS.md` sections 6-9, 13 and 20 (redacted extracts in `docs/handoff/EXTRACTS.md`),
and of the memory notes in `memory/`. Ids are the catalog's. Rigor marks: **CURRENT** (the file supports
it today), **DATED** (true at its date), **OPEN**, **DISPUTED**, **NOT RECORDED**, **SUPERSEDED** (replaced
by the row named), **RECORD** (history, not quotable). Where this folder's documents and a copied note
disagree, the result file wins. The measurement rows F.21-F.45 belong to project 05 and are listed in
section 6 only where this folder's documents depend on them.

## 1. The release

| id | claim | file | status |
|---|---|---|---|
| F.1 | 802 records from TCIA CT COLONOGRAPHY: 342 fused (spine and pelvis on one series), 351 separate, 89 spine only, 20 pelvis only; 422 supine, 377 prone, 3 decubitus; 562 at 1.0 mm, 232 at 1.25 mm, 8 other | `manuscripts/mpda/main.tex` Sources and Figure 1 (TikZ); `docs/release/manifest.json` (802 records) | CURRENT; feeds MPDA Figure 1 |
| F.2 | CTSpine1K's selector never selected (the retained series is whichever the directory walk reached last); `Path.csv` names no position for 217 of 782 annotated records; CTPelvic1K: 702 of 713 masks resolve to the series chosen by bone overlap | `manuscripts/mpda/main.tex` Sources; `ctsp:morphometrics/ctspine1k_pathcsv_agreement.csv` (`ctsp:scripts/compare_ctspine1k_pathcsv.py`); `memory/ctspine1k-selection-code-deleted.md`; `results/root_qc_tables/Path.csv` | CURRENT |
| F.3 | source ground-truth corrections: 112 spine corrections in 103 cases, 13 pelvic in 12 | `manuscripts/mpda/main.tex` Figure 1 | **DISPUTED**: every row of `docs/ctsp/CORRECTIONS.md` (last changed 2026-07-21) still reads "pending (in review)"; the final state per row is NOT RECORDED (`OPEN_QUESTIONS.md` E13) |
| F.4 | pelvic pseudolabeller (Dataset803, five-fold nnU-Net, out of fold on 440 records) held-out Dice against manual CTPelvic1K labels: sacrum 0.980 +/- 0.003 (no fold below 0.977), left hip 0.970 +/- 0.016, right hip 0.971 +/- 0.015 | `results/ctsp_results/pseudolabel_dice/README.md`, `dataset803_fold_validation_dice*.csv` (`ctsp:scripts/extract_pseudolabel_dice.py`) | CURRENT with the caveat recorded there: these are nnU-Net's patch-based online validation Dice read from the checkpoints; `scripts/eval_vs_manual.py` was written but never run; feeds MPDA Table S1 |
| F.5 | the S1 carve (v3-v10, id 29): median craniocaudal extent 57.6 mm (a real first sacral segment is near 30); 221 of 801 records with S1 over half the sacrum (CSV count; `ctsp:CLAUDE.md` and commit 2232bde say 222); 580 in 0.15-0.50; failures shaved the ventral cortex; found by rendering | `ctsp:morphometrics/s1_carve_audit.csv` (`ctsp:scripts/audit_s1_carve.py`); `docs/ctsp/qc/s1_carve_0428_vs_0704.png` | CURRENT (221 vs 222 not settled, `OPEN_QUESTIONS.md` D5); the reason for v11 |
| F.6 | effect of the carve on the angles: on the 580 sound carves PI 52.7 / PT 19.6 (Hasegawa 53.4 / 19.2); on the 221 degenerate PI 68.5 / PT 33.6; the plate gate fired on 96 % of the second group and 4 % of the first | commit 2232bde; `ctsp:scripts/compare_v10_v11_spinopelvic.py` | CURRENT |
| F.7 | the v11 merge returned 155,093,558 voxels to the sacrum on 801 of 802 records (record 1000 never had an S1) | `memory/s1-carve-changed-spinopelvic.md` line 19 and `docs/handoff/RESULTS_CATALOG.md` F.7 (the record). The step is `ctsp:scripts/merge_s1_into_sacrum.py` with `check_s1_merge.py`, but neither docstring nor any commit message at 7ddfe38 carries the count (checked 2026-10-08); the run output that produced it is not recorded (if it survives, it is under `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, `MANIFEST_GRID.md` section 1) | RECORD (a note's number; the run log was not located) |
| F.8 | rib checks, pseudolabel against release (same code): two numbers on one bone 151 / 584 -> 0 / 0; detached 37 / 40 -> 0 / 0; split inside the field 119 / 280 -> 6 / 7; offset 24 / 170 -> 0 / 2; no vertebra within reach 38 -> 11; rib on a lumbar body 14 / 21 -> 0 / 0 | `results/ctsp_results/rib_qc_v4_vs_release/README.md` (grid job 40220664) | CURRENT; MPDA Table II |
| F.9 | release rib incidence: 11,560 ribs, 5,796 skipped (own vertebra outside the field), 11 no contact, 5,753 evaluable, 5,751 match, 2 offset (0.035 %), 0 misnumbered cases | `results/ctsp_results/rib_qc_v4_vs_release/incidence_release.json` | CURRENT; MPDA Validation |
| F.10 | rib review: all 152 worklist cases corrected, 149 finalised by a second read; not finalised: token 46 (case 0068), 61 (0090), 518 (0730) | `results/ctsp_results/rib_qc_v4_vs_release/README.md` (checked against the ribs ledger 2026-09-14); `results/root_qc_tables/rib_worklist.json` (152 tokens; `memory/canonical-rib-triage.md`) | CURRENT (an earlier "148 of 152" was a stale worklist) |
| F.11 | lumbar ribs (60 / 61): 16 records (13 bilateral, 3 right only) | `manuscripts/mpda/main.tex` Label scheme; `ctsp:morphometrics/label_census_v11.csv`; `results/root_qc_tables/lumbar_ribs.csv` | CURRENT (case 0787 was the 15-vs-16 disagreement; how it was resolved is NOT RECORDED, E19) |
| F.12 | stump twelfth ribs (lowest-rib ratio < 0.33) in 98 of 789 records (12.4 %); lumbar ribs 2.0 %, against 12.6 % and 1.5 % in Nagata 2025 | `manuscripts/mpda/main.tex` Descriptive Analysis; `ctsp:morphometrics/transition_morphometrics.csv` column `rib12_11_ratio_min`; `results/root_qc_tables/stump_rib_candidates.csv` | CURRENT (the CSV was written on v10 labels; ribs are unaffected by v11) |
| F.13 | surgical hardware: 52 detections -> 11 kept (kept >= 2,586 mm^3, rejected <= 1,768 mm^3); eight arthroplasties, one osteosynthesis, one SI fixation, one cage pair (0068); 1,538,852 voxels reclaimed; the femoral head used for PI / PT is an implant in eight records | `docs/release/KNOWN_ISSUES.md` sections 3 and 8; `manuscripts/mpda/main.tex`; `results/hardware_review/` (README, `hardware_manifest.csv/json`, `applied.json`, `review_log.csv`, 70 per-case json) | CURRENT (`docs/ctsp/HARDWARE_CLASSES.md` says nine: stale); MPDA Figure S1 |
| F.14 | Castellvi: 34 records read by two radiology residents (reads dated 2026-09-04): 33 graded as an LSTV and 1 graded 0 (normal); six disagreements resolved by consensus; consensus IIIb 16, IIb 6, IV 4, IIa 4, Ib 2, IIIa 1, 0 1; kappa 0.737 (0.553-0.920) full, 0.696 type only; 768 of 802 unread (null means ungraded, not normal) | `docs/ctsp/castellvi_consensus.csv` (columns `read_1_A`, `read_2_B` here; distribution and kappa recomputed from it 2026-10-08: 33 double-read rows, 6 disagreements, 0.737 full, 0.696 type only; the 0.553-0.920 interval is the catalog's and was not recomputed), `docs/ctsp/castellvi_readers_2026-09-04.csv` (readers A / B here); `docs/handoff/RESULTS_CATALOG.md` F.14; `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` row 19 only for the camera-ready's own wording, kappa 0.70 (0.48-0.92) on type I-IV alone | CURRENT. **Stale distributions** (do not quote): `ctsp:morphometrics/castellvi_grades.csv`, `docs/release/README.md` (the Zenodo v11 README carries the August paragraph, IIIb 18), `results/root_qc_tables/Lumbosac.csv` (the three-column reader sheet: IIIb 16 by reader A and 17 by reader B, counted 2026-10-08; the IIIb 19 sheet is `Desktop/NeurIPS/Lumbosac_Castelvii_Class.csv`, not copied, `RESULTS_CATALOG.md` F.14) |
| F.15 | manifest `has_l6`, `n_lumbar_labels`, `has_lumbar_rib`, `lumbar_rib_side` recomputed from volumes 2026-08-23; current census 18 L6 records | `docs/ctsp/RELEASE_CHECKLIST.md`; `ctsp:morphometrics/label_census_v11.csv` | CURRENT |
| F.16 | `n_voxels_fg` is broken (0 in 340 of 802); `spine_bone_pct` is over vertebra ids only and nothing says so | `memory/grid-ct-0533-truncated.md` | OPEN |
| F.17 | splits: five disjoint folds, no held-out test set; the splitter never read the lumbar count (strata lumbarization 15 / sacralization 15 / semi 2 / ambiguous 2 / normal 768; record 0500 sits in lumbarization on a phantom L6) | `manuscripts/mpda/main.tex` Data Format; `memory/splits-origin-and-v3-resplit.md`; `docs/release/splits_5fold.json` (schema 6, 802 patients, 5 folds, seed 42, 6 subtypes); `code/spinesurg_scripts/generate_5fold_splits.py` | OPEN (why 0500 was flagged: NOT RECORDED, D3) |
| F.18 | identity: one release id = one person, 802 / 802; prone / supine duplication ruled out (zero shared signatures over 1,728 acquisitions) | `ssn:docs/PATIENT_IDENTITY_SPEC.md` line 119; `docs/handoff/LEAKAGE.md` | CURRENT; whether the 768 numeric-id and 34 `CTC-` records overlap as humans: NOT RECORDED (E2) |
| F.19 | known defects: 0533 truncated, repaired 2026-09-23 (job 40416624) and the HF file replaced (40419665); 16 records with no thoracic vertebra (2026-08-19 list); top labelled vertebra cut in 553 of 802; 27,738 detached label pieces in 741 records; six `pelvic_native` cases never reviewed; 0172 in the re-read queue; LCC post-processing deletes the loose lamina of a spondylolytic vertebra | `docs/release/KNOWN_ISSUES.md`; `docs/ctsp/LAB_JOURNAL.md`; `docs/ctsp/RELEASE_CHECKLIST.md`; `memory/grid-ct-0533-truncated.md`; `memory/spondylolysis-and-border-anomaly-findings.md` | mixed; **`KNOWN_ISSUES.md` (v10) lacks 0533, the mirrored CTs (tokens 75, 480) and COLONOG_299's misplaced L5** (`TODO.md` step 4) |
| F.20 | version progression with identical checks: fragmented labels 366 -> 1,146 (v3, ribs arrive) -> 377; rib offset 10.83 % -> 7.69 % (a version-comparison metric only) | `docs/ctsp/VERSION_PROGRESSION.md` (`ctsp:scripts/qc_version_progression.py`); `results/qc/qc_final/version_progression.csv` | RECORD |

## 2. The dataset article (Medical Physics Dataset and Software Article)

From the Greg-only `HANDOFF/MANUSCRIPTS.md` section 6 (`docs/handoff/EXTRACTS.md` M6), checked against the
files named.

| item | record | file |
|---|---|---|
| title | "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral transitional anatomy" | `manuscripts/mpda/cover_letter.md` |
| authors | 14 on the title page (the NeurIPS senior author is not among them, contradiction C11) | `manuscripts/mpda/title_page.tex` |
| data | 802 records; Zenodo concept 10.5281/zenodo.22139642; v11 10.5281/zenodo.22797014 (published 2026-09-18); build archive 10.5281/zenodo.22647933; CC BY-NC-SA 4.0 | `cover_letter.md`, `title_page.tex` |
| preprint | arXiv 2609.22760 (v1, 2026-09-19, named authors, "Department of Surgery, DMC and WSU") | `manuscripts/arxiv_final_draft_9_19_2026.pdf`; `manuscripts/mpda/ARXIV_SUBMISSION.md` |
| history | MLHC 2026 version rejected; retargeted 2026-07-24; plan: DOI before submission, no hypothesis testing, 10 published pages (`manuscripts/mpda/PLAN.md`); first submitted 2026-09-07 (`manuscripts/mpda_as_submitted_2026-09-07/`); returned unreviewed 2026-09-21 for carrying an abstract (commit 20ff26a); the 21 September build (`manuscripts/mpda_as_submitted_2026-09-21/MDPA_FINAL.pdf`); returned again for the supporting-information format; packet rebuilt 2026-09-25 10:34 with the Castellvi wording fix (31e1b16, 70de829) and the F30 funding line (f14c9b9) | `docs/handoff/EXTRACTS.md` M6 |
| current packet | `ctsp:dist/submission/` (regenerable by `manuscripts/mpda/make_submission.py` from Windows): main document 25 review pages, supporting information 3, title page, Figures 1-3, `Abstract.txt`, `Cover_Letter.md` | not copied (regenerable); `MANIFEST_LOCAL.md` |
| page check | `build.sh --reprint` -> 10 pages; `CTSpinoPelvic1K_reprint_check.pdf` rebuilt 2026-10-08 09:41 (by whom: NOT RECORDED, E6) | `manuscripts/mpda/CTSpinoPelvic1K_reprint_check.pdf` |
| floats | main: Table I prior art, Figure 1 pipeline, Table II rib QC, Figure 2 four phenotypes, Table III spinopelvic, Figure 3 morphometry by level (L5 end-plate and pedicle width withheld); supporting: Figures S1 hardware, S2 validation, S3 field of view; Tables S1 pseudolabeller Dice, S2 completeness, S3 identifier census | `docs/handoff/RECIPES.md` section 9 item 5 |
| number chain | `REPRODUCE.md`; `audit_ms.py` (text against CSV), `audit_artifacts.py` (every figure and table regenerates), `audit_pdfs.py` (packet read-back); `CITATION_CHECK.md` (9 Sep 2026) | `manuscripts/mpda/` |
| caption check | by a rough counter three main-document table captions exceed 60 words (rib QC 66, spinopelvic 71, level atlas 62); the project's counter may differ by a few words | EXTRACTS M6 |
| student review | the annotation lead's pass merged 2026-09-18 (7922c0c); responses in `manuscripts/mpda/STUDENT_REVIEW_RESPONSE.md` | same |
| AI-text scans | GPTZero 60 % on the 12 Sep copy (`manuscripts/mpda_ai_text_scans/MDPA_AI.pdf`); 51 % on the single-column docx (not copied); the manuscript discloses language-model assistance (`main.tex` line 652) | same |
| submission state | whether the 2026-09-25 packet was uploaded, under what number, and its editorial status: **NOT RECORDED** (`OPEN_QUESTIONS.md` A2) | — |

**Defects known in the article text** (must be fixed, not disclosed; `TODO.md` step 3): the title page calls the
corresponding author "a faculty surgeon" (line 85) while the HPR records say resident (C6); "no relevant conflicts"
against an invention disclosure filed 2026-09-25 in the same field (C7); the contribution statement says each
Castellvi reader read "every case independently" while the reads were complete by 4 Sep, reader B's grades for
five cases are 23 Aug second reads and both readers had seen the May grading (C12); the cover letter says the
NeurIPS paper "shares no text, figure or table" while NeurIPS Appendices G and H are captioned "Adapted from" the
article (C10); the mirror-image CTs (tokens 75 and 480) are disclosed in NeurIPS but not here; the Figure 3
caption and `REPRODUCE.md` section 2 still say "digitised from Figure 4A" though Panjabi 1991 Table 3 was obtained
(F.38); the Acknowledgements say "This work received no funding" while the title page names NIH F30GM147909
(`OPEN_QUESTIONS.md` F16); the NeurIPS paper should be cited with key `neurips2026lstv`; `REPRODUCE.md` section 0
still says "v10 ... S1=29" (C18).

## 3. NeurIPS 2026 Evaluations and Datasets paper 3474 (accepted)

| id | claim | file | status |
|---|---|---|---|
| — | submitted as "Not All Spines Are Created Equal: How TotalSegmentator Fails on Lumbosacral Transitional Vertebrae" (`manuscripts/3474_Not_All_Spines_Are_Create.pdf`, 19 pages, anonymous); camera-ready title "... How CT Segmenters Fail ..." (`src/neurips_2026.tex` line 35); accepted as a poster, OpenReview 2026-09-24, id D8yRWDAGQF; five authors (`REVIEWER_CRITIQUES.txt`) | `manuscripts/neurips_camera_ready/` | CURRENT |
| — | build: `latexmk -pdf -interaction=nonstopmode neurips_2026.tex` in WSL (TeX Live; `cm-super` installed 2026-09-26; first rebuild needs `latexmk -g`). The committed copy (38b0cb9, 2026-09-25) is 21 pages with appendices A-D; the uncommitted 2026-09-27 working copy is 31 pages because it `\input`s `src/appendix/` (eleven files: `spineps.tex`, `v11_results.tex`, `release_split.tex`, ...) whose `[pending]` slots wait on the cancelled jobs | `manuscripts/neurips_camera_ready/src/neurips_2026.pdf` (the 2026-09-27 copy); `CAMERA_READY_CHANGES.md` | CURRENT fact |
| F.46 | every segmentation number was computed on the April 2026 release (1,153 records, ten-class scheme merged to nine, record-level split 805 train / 174 validation / 174 test of a 979-record pool), not on v11; the Castellvi grades are the September two-reader reads | `CAMERA_READY_CHANGES.md` rows 14-23 and "Version note" | CURRENT fact |
| F.47 | **headline defect A**: TotalSegmentator sacrum Dice 0.817 (abstract "0.817 -> 0.969", section 8 "+15.2") counts TotalSegmentator's separate S1 class as a miss (TS `sacrum` excludes S1; the whole sacrum is the union, `memory/ts-sacrum-excludes-s1.md`); **defect B**: the junction comparisons subtract two window definitions | `CAMERA_READY_CHANGES.md` item 21 | **OPEN: still in the main text**; Appendix I says the first in one clause, Appendix J carries the corrected-row slot |
| F.48 | per-case evidence for the camera-ready numbers | `results/neurips_2026-05/bm/benchmark_per_case.csv`, `bm/benchmark_per_case_record_level.csv`, `ens/per_case_dice.csv`, `bm/benchmark_results.json`, `audit/`, `pred/`; which checkpoint made `ens/` and `pred/` is NOT RECORDED | OPEN: the recomputation scripts (`crverify.py`, `crverify2.py`, `crverify3.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py`) exist only in a Temp scratchpad on the laptop and were not found for this copy; rescue them into the repository (`OPEN_QUESTIONS.md` F2) |
| F.49 | 134 `[pending]` slots in Appendices I (SPINEPS) and J (v11 summaries); their jobs (40481323 -> 40481314 -> 40481315; 40480728/31/32, 40480730/33; total_v3 40481824-26) were cancelled 2026-09-27 15:50 | `CAMERA_READY_CHANGES.md` items 19-20; `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; `MANIFEST_GRID.md` section 2 | OPEN |
| — | `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` are named in the change log and found in no scratchpad (E10); the 2026-09-27 edits are uncommitted; the camera-ready deadline is NOT RECORDED on disk | `CAMERA_READY_CHANGES.md` | OPEN |
| — | captions: by the rough counter two table captions exceed 60 words (per-class DSC 64, five-fold checkpoint 66); the log's `capcount.py` reported all at most 60 | EXTRACTS M7 | OPEN (counter disagreement) |
| — | released code: `OpenSpineConsortium/spinopelvic-seg` at c105981, cited as the public code repository (commit 70de829); still carries an anonymised citation and author; live visibility not re-checked | `MANIFEST_CODE.md` section 4 | OPEN (item 14, E16) |
| F.50 | the twelve CNS 2026 student abstracts were computed by May 2026, before the spinopelvic-estimator and canal / end-plate fixes | the OSC website `contributions/manifest.json` (project 12); `docs/ctsp/SPINOPELVIC_ESTIMATOR.md`; `LEVEL_MORPHOMETRY.md` | NOT VERIFIED: whether the May numbers predate the fixes is not recorded; re-check before the posters are shown (2 November; `OPEN_QUESTIONS.md` C22) |

## 4. Earlier manuscripts and the talk (record)

| item | record | file | status |
|---|---|---|---|
| MLHC 2026 | "CTSpinoPelvic1K: A Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation" (20 pages, 2026-06-08; 1,137 volumes, 804 patients, 10-class labelmap); three rebuttals; **rejected** (2026-07-24); where the decision letter is: NOT RECORDED (E11) | `manuscripts/mlhc_2026_rejected/` | RECORD; `docs/ctsp/ROADMAP.md` "in review, score 2.75/4" is stale (C8): never cite as under review |
| March 2026 draft | `SpineSurgCT_arxiv.tex` and two PDFs; "Department of Neurosurgery" on its line 56 is a historical error (the affiliation is General Surgery) | `manuscripts/spinesurgct_arxiv_2026-03/`; `docs/labnotebook_2026-03/` (the clinical case: Ishida 54 % miscounting, Hanhivaara CT vs MRI sensitivity, Kwak 2025 76.4 %) | RECORD |
| NeurIPS draft of 2026-09-08 | `neurips_2026.tex` + `REVISION_PLAN.md`, frozen as a source only (Greg: stop drafting it) | `manuscripts/nextpaper_ar_2026-09-08/` | SUPERSEDED by the camera-ready |
| Radiology: AI CT paper | "A CT Segmentation Network Trained on Labelled Transitional Anatomy Reports the Lumbar Count with a Posterior ..." skeleton of 2026-09-08: 36 `\todo` markers (23 filled, 13 empty placeholders) counted 2026-10-08 in `manuscripts/nextpaper_radai/main.tex`; the handoff's 22 (`docs/handoff/EXTRACTS.md` M9) is not reproduced; results were to come from Dataset810 (retired) and Dataset813 (C5.3); `claim_checklist.md` (CLAIM 2024, 42 items) | `manuscripts/nextpaper_radai/` | OPEN, not started (EXTRACTS M9) |
| CNS 2026 talk 66629 (Mini Oral Poster, Monday 2 November, 5:21-6:00 PM) | the public v12 deck (17 slides, CT side only; every number asserted against the committed camera-ready; adds the MPDA pipeline, the hardware figure and the spinopelvic table PI 52.1 vs Veilleux 52.1 / Hasegawa 53.4, SS 36.6, PT 15.5); the 7 September draft deck (not presented); generators and figures. The talk title promises a single-shot model; no evaluated single-shot model is recorded on disk (C17). Whether the slides were submitted to the meeting: NOT RECORDED (A23) | `manuscripts/talks/cns2026/`; `memory/cns-deck-v2-2026-09-25.md`; `memory/chart-preferences.md` | CURRENT (talk pending) |

## 5. CT segmentation (Part C5)

| id | claim | file | status |
|---|---|---|---|
| C5.1 | six ablations of the segmentation model (fused_only 803, no_partial 804, no_lstv_oversample, short 100 epochs, ResEnc L, fused-only test 805) submitted by `ssn:slurm/spine_ablation.sh` (`make ablate`), aggregated by `ssn:tools/compare_ablations.py` into `tables/ablations.tex` | `docs/spinesurg_ct_nnunet/ablations.md` (first commit 2026-04-18); `docs/ctsp_root/STATUS.md` (2026-06-11: Dataset804 fold 0 in flight) | **NOT RECORDED**: no `tables/` directory on the laptop; the grid holds `/wsu/home/go/go24/go2432/ablate` (201.6 GB) whose outcome was never read (B16) |
| C5.2 | L6 pseudo-Dice 0.000 for 27+ epochs under 12x duplication (Dataset813); a counting decoder finds 6 / 6 L6 on four-class truth; Dataset815 raises L6 cases 18 -> 62 | `memory/l6-sample-count-and-counting-decoder.md` | DATED: a distinct-case count signal, not a trainer bug; premise of CT-6 |
| C5.3 | Dataset810 one-shot model launched 2026-09-07, retired 2026-09-08 for Dataset813 (numbered ribs); whether the Dataset813 folds finished or were scored | `memory/lstv-oneshot-training-run.md`; `ssn:docs/ruleclass/CLASSIFIERS.md` R36 | NOT RECORDED; no evaluated single-shot model exists on disk (contradicts the RPPR and the CNS 66629 title, C17) |
| — | the CT competitor benchmark (TotalSegmentator, SPINEPS + VERIDAH + Möller ribs, RibSeg v2, VISTA3D in the one-shot space): TotalSegmentator ready; SPINEPS container to pull; RibSeg has no released checkpoint; VISTA3D environment built, smoke pending; `collect.py` "to write"; Dataset810 retired | `code/benchmark/README.md`; `docs/spinesurg_ct_nnunet/COMPETITOR_BENCHMARK.md`; `memory/competitor-benchmark.md` | partial (CT-10); the re-implemented 2-D ensemble result is NOT RECORDED (B6) |

## 6. Measurement rows this folder's documents depend on (owned by project 05)

| id | claim | file | status |
|---|---|---|---|
| F.21 | v11 spinopelvic over 756 of 802 records: PI 52.1 +/- 11.1, SS 36.6 +/- 10.6, PT 15.5 +/- 7.9, LL 51.7 +/- 13.3, PI-LL 0.3 +/- 10.3; plate gate rejects 44; comparators Veilleux 2020 (n 200) 52.1 / 36.5 / 15.6, Hasegawa 2018 (n 24) 53.4 / 34.1 / 19.2 | `ctsp:morphometrics/surgical_morphometrics.csv` (commit 2232bde; recomputed from the CSV 2026-10-08 and matching) | CURRENT; MPDA Table III; the v12 deck (which two records besides the 44 lack PI: NOT RECORDED, D4) |
| F.22-F.26 | the four estimator defects found and fixed; the 128 low PI solved 2026-09-11 (028210a); the cohort-vs-convention reading of the SS gap; three items still open (eight prosthetic heads, the LSTV-dependent S1 call, the unmeasured anterior pelvic plane); ostk's bimodal S1 fit | `docs/ctsp/SPINOPELVIC_ESTIMATOR.md` | fixed / OPEN as the document says |
| F.32-F.34 | canal depth and L5 end-plate width: the defects caught by spread, the rewrite (below-11 mm 473 -> 12), L5 end-plate width and pedicle width **withheld** in `level_atlas.csv` and Figure 3 | `docs/ctsp/LEVEL_MORPHOMETRY.md` | CURRENT |
| F.35, F.38 | body height about 6 mm above Panjabi with every artefact excluded; Panjabi 1991 Table 3 in `make_reference_table.py` since 83f7f95 while the Figure 3 caption still says "digitised" | `docs/ctsp/BODY_HEIGHT_INVESTIGATION.md`; `memory/panjabi-1991-page-892.md` | CURRENT; caption stale |
| F.44 | four CSVs written before v11 that touch the sacrum or the lumbosacral disc must be recomputed: `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv`, plus `opportunistic.csv`, `proximal_femur.csv` | `ctsp:morphometrics/` (git log) | OPEN (`TODO.md` step 5) |
| F.45 | the student pelvic-width demo: the committed report used S1 width (v10); the current script measures femoral-head separation | `results/ctsp_results/pelvic_width/report.txt`; `ctsp:scripts/demo_pelvic_width_dimorphism.py` | OPEN (stale report) |

## 7. Superseded, and by what

| superseded | replaced by |
|---|---|
| the carved S1 (id 29) and every number computed through it (v3-v10 spinopelvic, `pelvic_shape.csv` of 2026-09-10, the committed pelvic-width report) | v11 (sacrum 26 whole; F.5-F.7); recompute on v11 (F.44, F.45) |
| `docs/release/KNOWN_ISSUES.md`, `docs/release/README.md`, `docs/release/dataset_labels.json` (all v10) | the v11 deposit on Zenodo and the v11 staging on the grid (`MANIFEST_GRID.md` section 1); `TODO.md` step 4 |
| `results/root_qc_tables/Lumbosac.csv` (2026-09-04 three-column reader sheet; IIIb 16 / 17 by reader) and `ctsp:morphometrics/castellvi_grades.csv` | `docs/ctsp/castellvi_consensus.csv` (F.14) |
| `results/nextpaper/manifest.csv` (1,153 rows, 2026-05-17, ids unpadded) | `docs/release/manifest.json` (802 records) and the v11 manifest on the grid |
| `results/nextpaper_viz/` (the 2026-05-31 refinement review page) | the v10 / v11 build (`docs/ctsp/BUILD_CHAIN.md`) |
| `manuscripts/nextpaper_ar_2026-09-08/`, `manuscripts/3474_Not_All_Spines_Are_Create.pdf` (as reviewed) | `manuscripts/neurips_camera_ready/` (working tree of 2026-09-27) |
| `manuscripts/mpda_as_submitted_2026-09-07/`, `manuscripts/mpda_as_submitted_2026-09-21/`, the arXiv v1 | `manuscripts/mpda/main.tex` at 70de829 (2026-09-25) |
| `manuscripts/mlhc_2026_rejected/`, `manuscripts/spinesurgct_arxiv_2026-03/` | the dataset article |
| `docs/ctsp/ROADMAP.md` (MLHC in review; v3 rebuild in progress) and `docs/ctsp_root/STATUS.md` (2026-06-11), `docs/ctsp_root/README.md` (v5 era) | this file; `TODO.md` step 4 updates them |
| `memory/hf-mirror-is-v10.md` and `memory/zenodo-deposit.md` on "Zenodo is v10" | four documents giving v11 (M20 C1); the HF-is-v10 part stands |
| `docs/ctsp/HARDWARE_CLASSES.md` "nine arthroplasties" | eight (F.13) |

## 8. What no file records (the preferred form: stated, not guessed)

Whether the MPDA packet of 2026-09-25 was uploaded (A2); the NeurIPS camera-ready deadline and whether the
camera-ready, Croissant file and OpenReview note were uploaded (A6); who rebuilt the reprint check on
2026-10-08 (E6); the live state of Zenodo v11 and the HF mirror today (E7); the final state of each of the
125 source corrections (E13); which script made the committed `fig_hardware.pdf` and the exact command
behind `label_census_v11.csv` (E14); the PGY year of the two Castellvi readers (E3); whether the 768
numeric-id and 34 `CTC-` records share a human (E2); why 0500 was flagged L6 (D3); which two records lack PI
beside the 44 rejections (D4); 221 vs 222 degenerate carves (D5); the state of the six unreviewed
`pelvic_native` cases and the 16 zero-thoracic cases, and how 0787 was resolved (E19); whether the
Dataset813 folds finished (C19); what the ablation array found (B16); whether the sacrum-adjacent CSVs were
recomputed on v11 on the grid (B27); which checkpoint produced `results/neurips_2026-05/ens/` and `pred/`.
