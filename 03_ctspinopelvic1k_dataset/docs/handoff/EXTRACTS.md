# EXTRACTS — the sections of the Greg-only HANDOFF files that bear on project 03

> **Written for this folder on 2026-10-08** as redacted extracts of the Greg-only HANDOFF files, quoting the handoff's own path spellings. Its prefixes and the laptop locations it names (`Desktop/NeurIPS/...`, the Temp scratchpad) resolve as `PREFIXES.md` says; nothing in this folder depends on them (`../../MANIFEST_LOCAL.md` section 3.6).

The handoff of 2026-10-08 (`spinesurg-ct-nnunet` `HANDOFF/`, commit 097933a) has four Greg-only files that
are not copied whole into a student-safe folder: `MANUSCRIPTS.md`, `RESEARCH_DIRECTIONS.md`,
`LITERATURE_STATE.md` and `CONTEXT_EXPORT.md` (`../../../_plan/PLAN.md` section 2 rule 3). This file carries
the sections of the first three that `STATUS.md` and `TODO.md` cite, verbatim except where marked
`[withheld]` (an author list, a student roster) and except for the banned word, which was rewritten.
Section ids: **M** = `MANUSCRIPTS.md`, **R** = `RESEARCH_DIRECTIONS.md`, **L** = `LITERATURE_STATE.md`.
Path prefixes are those of `README.md` section 0 in this folder (`ctsp:` = the public CTSpinoPelvic1K
repository at 7ddfe38; `Desktop/...` = a laptop file whose copy, if any, is named in `../../MANIFEST_LOCAL.md`).

---

## M6. CTSpinoPelvic1K dataset article (Medical Physics, Dataset and Software Article)

| item | record |
|---|---|
| title | "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral transitional anatomy" (`ctsp:paper/mpda/cover_letter.md`) |
| authors | 14 [names withheld here; they are on `ctsp:paper/mpda/title_page.tex`]; a sign-off sheet exists on the laptop and carries co-author e-mail addresses (not copied) |
| data | 802 records (ACRIN 6664); Zenodo concept 10.5281/zenodo.22139642; v11 = 10.5281/zenodo.22797014 ("published 18 Sep 2026"); build archive 10.5281/zenodo.22647933; CC BY-NC-SA 4.0 |
| preprint | arXiv 2609.22760 (`cover_letter.md`); form, categories and licence `paper/mpda/ARXIV_SUBMISSION.md`; upload built by `make_arxiv.sh` |
| history | MLHC 2026 version rejected; retargeted to Medical Physics 2026-07-24 (`context/publication-roadmap.md`); plan `paper/mpda/PLAN.md` (DOI before submission; no hypothesis testing; 10 published pages); returned unreviewed 2026-09-21 for carrying an abstract (commit 20ff26a); returned again for the supporting-information format; packet rebuilt 2026-09-25 10:34 (`ctsp:dist/submission/`) with the Castellvi wording fix (31e1b16, 70de829) and the F30 funding line (f14c9b9) |
| current packet | `ctsp:dist/submission/`: `Main_Document_CTSpinoPelvic1K.{tex,pdf}` (25 review pages), `Supporting_Information_CTSpinoPelvic1K.pdf` (3), `Title_Page_CTSpinoPelvic1K.pdf`, `Figure_1..3.pdf`, `Abstract.txt`, `Cover_Letter.md`; built by `paper/mpda/make_submission.py` (run from Windows) |
| page check | `bash paper/mpda/build.sh --reprint` -> 10 pages (rebuilt 2026-10-08 09:41) |
| floats | main: Table 1 prior art, Figure 1 pipeline, rib QC table, Figure four phenotypes, spinopelvic table, Figure morphometry by level (L5 withheld); supporting: Figures S1 hardware, S2 validation, S3 field of view; Tables pseudolabeller Dice, completeness, identifier census (`RECIPES.md` section 9) |
| where numbers come from | `paper/mpda/REPRODUCE.md`; text-vs-CSV check `audit_ms.py`; every figure / table regenerates `audit_artifacts.py`; PDF read-back `audit_pdfs.py`; citations read against sources `paper/mpda/CITATION_CHECK.md` (9 Sep 2026) |
| caption check | by a rough counter, three main-document table captions exceed 60 words (rib QC 66, spinopelvic 71, level atlas 62); the project's counter may differ by a few words |
| student review | the annotation lead's pass merged 2026-09-18 (7922c0c); comments `paper/mpda/CTSP_OTHERSTUDENTS.docx` (not copied); responses `paper/mpda/STUDENT_REVIEW_RESPONSE.md` |
| AI-text scans | `Desktop/MDPA_AI.pdf` (GPTZero 60 % on the 12 Sep copy), `ctsp:GPTZero AI Scan - CTSpinoPelvic1K_single_column.docx.pdf` (51 %); the manuscript discloses language-model assistance (`main.tex` line 652) |
| older copies | `Desktop/CTSpinoPelvic1K_coauthor_draft.{docx,pdf}`, `_overleaf(.zip)`, `_MDPA_overleaf(.zip)`, `_submission(.zip)`, `_arxiv.tar.gz`, `_arxiv_preview.pdf` (6-12 Sep, v10 era); `Desktop/MDPA.pdf` (12 Sep), `ctsp:MDPA.pdf` (16 Sep), `Desktop/MDPA_FINAL.pdf` (21 Sep), `Desktop/arxiv_prev.pdf`, `ctsp:arxiv_final_draft_9_19_2026.pdf` (19 Sep) |

Must be redone (each from the file named): confirm the submission state with Greg; title page calls the
corresponding author "a faculty surgeon" (`title_page.tex` line 85) while the TTO and HPR records say resident
(C6); "no relevant conflicts" while an invention disclosure in the same field was filed 2026-09-25 (C7); the
contribution statement says each Castellvi reader read "every case independently", while the NeurIPS audit found
the reads complete by 4 Sep, reader 2's grades for five cases are 23 Aug second reads, and the readers had seen the
May grading (`ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` S6, change 19) (C12); the cover letter says the
NeurIPS paper "shares no text, figure or table" while NeurIPS appendices G and H are captioned "Adapted from" the
dataset article (C10); mirror-image CTs (at least tokens 75 and 480) are disclosed in NeurIPS but not in the MPDA or
`zenodo/KNOWN_ISSUES.md`; `KNOWN_ISSUES.md` (last changed 2026-09-07, v10) lacks the mirrored CTs, the 0533
truncation and the misplaced L5 label in COLONOG_299; the Zenodo v11 README still carries the August Castellvi
paragraph; `REPRODUCE.md` section 0 still says "v10 ... S1=29" (C18); the Figure 3 caption still says "digitised
from Figure 4A" though Panjabi Table 3 was obtained (`RESULTS_CATALOG.md` F.38); `main.tex` Acknowledgements says
"This work received no funding" while the title page names NIH F30GM147909 (topic 6 C13); cite the NeurIPS paper
with key `neurips2026lstv`. Whether to post an arXiv replacement (v1 predates the ten-page cut, the Castellvi
five-of-six and the funding line) is not decided anywhere. Then rebuild with `build.sh --reprint` reading the whole
output, regenerate the packet from Windows, and run the three audits; a deposit with changed files is a new integer
Zenodo version.

---

## M7. NeurIPS 2026 Evaluations and Datasets Track, submission 3474 (accepted)

| item | record |
|---|---|
| title | submitted as "Not All Spines Are Created Equal: How TotalSegmentator Fails on Lumbosacral Transitional Vertebrae" (`Desktop/3474_Not_All_Spines_Are_Create.pdf` = `ctsp:3474_...pdf` = `CAMERA_READY_NEURIPS/NEURIPS_CURRENT_PDF.pdf`); camera-ready "... How CT Segmenters Fail ..." (`src/neurips_2026.tex` line 35) |
| decision | accept, poster, OpenReview 24 Sep 2026, id D8yRWDAGQF; authors Gregory John Schwing, Patrick Schwing, Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert (`CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt`) |
| change log | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`: three 2026-09-27 passes supersede the 25 Sep sections |
| build | `latexmk -pdf -interaction=nonstopmode neurips_2026.tex` in WSL (TeX Live; `cm-super` installed 2026-09-26; first rebuild needs `latexmk -g`); `src/neurips_2026.pdf` 31 pages, 134 `[pending]` slots (2026-09-27 02:15); content pages 1-10. **Why 21 and 31 pages both exist**: the committed copy (38b0cb9, 2026-09-25) is 21 pages with technical appendices A-D; the uncommitted 2026-09-27 working copy is 31 pages because its edits `\input{appendix/appendix}` from the untracked `src/appendix/` (eleven files, among them `spineps.tex`, `v11_results.tex` and `release_split.tex`) whose `[pending]` slots wait on the cancelled jobs below (page counts read from both PDFs with PyMuPDF on 2026-10-08; `git status`) |
| the pending slots | Appendix I (SPINEPS under the protocol: jobs 40481323 -> 40481314 -> 40481315; use only with 0 ground-truth-gate mismatches) and Appendix J (v11 summaries: 40480728/31/32, 40480730/33); TotalSegmentator total_v3 (40481824-26) |
| **those jobs were cancelled** | 2026-09-27 15:50 with everything outside `ruleclass/` (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; nv11_ts had 6 of 16 shards done and resumes per shard) |
| open for Greg | "What remains for Greg" items 3-26: upload the camera-ready and the Croissant file (v11 has no `croissant.json`, only v6); do not upload while any `[pending]` remains (fill or cut Appendices I-J); run or cut total_v3; headline defects A (TS sacrum 0.817 counts its S1 class as a miss) and B (junction comparisons subtract two window definitions) are still in the main text; publish the April release manifests and the evaluated 174-record split, or keep checklist item 5 at "No"; licence per host differs; the MPDA overlap sentence; the mirror images; competing interests vs the invention disclosure; readers' PGY level (not recorded); the Castellvi grades changed after review (Greg's judgement whether to tell the AC); post the OpenReview note |
| evidence | per-case `Desktop/NeurIPS/bm/benchmark_per_case.csv`, `bm/benchmark_per_case_record_level.csv`, `ens/per_case_dice.csv`; Castellvi `ctsp:docs/castellvi_consensus.csv`, `castellvi_readers_2026-09-04.csv`; recomputation scripts (`crverify.py`, `crverify2.py`, `crverify3.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py`) **only** in a laptop Temp scratchpad (Temp can be swept: copy them into the repository) |
| referenced but not found | `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` (named in the change log) are in no Temp scratchpad |
| commit state | the 2026-09-27 edits are uncommitted ("Nothing was pushed, committed, posted or published") |
| captions | by the rough counter two table captions exceed 60 words (per-class DSC 64, five-fold checkpoint 66); the log's `capcount.py` reported all at most 60 |
| released code | `OpenSpineConsortium/spinopelvic-seg` at c105981 (local `Desktop/NextPaper/spinopelvic-seg`, remote `origin` still `anonymous-neurips-ED/spinopelvic-seg`, remote `osc` the OSC repository); the camera-ready cites it as the public code repository (commit 70de829: "cites the public code repository (the development repository is private)"; "All are accessible"); its live visibility was not re-checked (no network); still carries an anonymised citation and author (item 14) |
| deadline | not recorded on disk |

Redo plan: commit the current state; rescue the scratch scripts; decide with Greg whether to resubmit the cancelled
chains (the grid record says how to resume each) or cut Appendices I-J and the four sentences that point at
total_v3 (their exact wording was in the missing `INTEGRATE.md` section 5, so it must be rewritten); fix defects A
and B; settle items 16-24; rebuild; check fonts and pages; upload. This has a deadline and goes first among the
CT-side items.

---

## M8. MLHC 2026 (rejected)

`Desktop/MLHC_2026_Research_Track_Paper.pdf` (20 pages, 8 Jun 2026; text `ctsp:_paper_text.txt`): "CTSpinoPelvic1K: A
Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation", 1,137 volumes, 804 patients, 10-class
labelmap. Source `ctsp:mlhc/full-paper-template.tex`; rebuttals `ctsp:_rebuttal_r2.txt`, `_rebuttal_r3.txt`,
`_rebuttal_f65r.txt`. Outcome rejected (`context/publication-roadmap.md`, 2026-07-24); `ctsp:docs/ROADMAP.md` still says
"in review, score 2.75/4" (stale, C8). Where the decision letter is: not recorded. Nothing to redo; never cite it as
under review.

## M9. Other CT-side manuscripts in `Desktop/NextPaper/`

| file | record | state |
|---|---|---|
| `NextPaper/RadAI/main.tex` "A CT Segmentation Network Trained on Labelled Transitional Anatomy Reports the Lumbar Count with a Posterior: Comparison with Public Systems on an LSTV-Stratified Cohort" | Radiology: AI target set 2026-09-08 for the one-shot / numbered-rib work (`README.md`, `claim_checklist.md`) | 22 `\todo`; results were to come from Dataset810 (retired 2026-09-08) and Dataset813 (numbered ribs); whether Dataset813 finished or was scored is not recorded |
| `NextPaper/AR/neurips_2026.tex` + `REVISION_PLAN.md` | the September revision toward v10 and the one-shot model | FROZEN 2026-09-08 as a source only (Greg: stop drafting it) |
| `NextPaper/VerSeFusion/` (README) | "accompanies the NeurIPS 2026 Datasets & Benchmarks Track submission" | submission not recorded; the CV lists no VerSeFusion paper |

---

## M13. CNS 2026 (Washington DC, 31 Oct-4 Nov 2026)

### M13.1 The twelve OSC abstracts (the OSC website's `contributions/manifest.json`, 2026-05-19)

| CNS id | title (short) | status |
|---|---|---|
| 66629 | Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model for Preoperative Detection of Lumbar and Thoracic End Anomalies | Mini Oral Poster (Greg; MP4SP1 Mon 2 Nov 5:21-6:00 PM); Greg sole author |
| 66639 | Beyond the Cadaver Lab (OSC med-ed) | Printed Poster; 16 students [names withheld] |
| 68300 | Automated CT-Derived Cobb Angle Measurement | Digital Only |
| 67525 | Opportunistic Screening for Vertebral Degeneration Using Vertebral Hounsfield Units | Digital Only |
| 68579 | Sagittal Lumbar Lordosis via a TRALL Angle Pipeline | Digital Only |
| 69734 | Automated Lumbar Intervertebral Disc Heights | Digital Only |
| 69093 | Automated CT-Based Pelvic Incidence and Sacral Slope | Digital Only |
| 68733 | Automated Vertebral Wedging Index | Digital Only |
| 68460 | Lordosis Distribution Index | "Submitted" (not updated) |
| 68858 | Lumbar Spinal Stenosis Screening, Normative Torg Ratio L1-L5 | Digital Only |
| 68779 | Lumbar Spondylolisthesis and Meyerding Classification | "Submitted" (not updated) |
| 67829 | Automated 3D Vertebral Centroid Trajectory | Digital Only |

(The student authors of each abstract are named in the website manifest, project 12; withheld here.) Three more
topics are "In preparation" (vertebral spacing, SVA, TPA). The submitted abstract texts are not on disk. **Before
the posters are shown**: the PI / SS abstract (69093) and the measurement abstracts were computed by May 2026; the
spinopelvic-estimator defects and the canal / end-plate defects were found in August-September; whether the May
numbers predate the fixes is not recorded; re-check each against v11 and the fixed estimators. The talk title
promises a single-shot model; no evaluated single-shot model is recorded on disk (C17).

### M13.2 Greg's spine deck for 66629

| file | what | disclosure status |
|---|---|---|
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` (copied: `manuscripts/talks/cns2026/`) | **current disclosure-safe deck**, 17 slides, CT side only (generator `ctsp:paper/cns2026/make_cns_deck_v12_public.py` + `prep_v16_public_figs.py`); every number asserted against the committed NeurIPS camera-ready; adds the MPDA pipeline, hardware figure and the spinopelvic table (PI 52.1 vs Veilleux 52.1 / Hasegawa 53.4; SS 36.6; PT 15.5) | safe |
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | 15-slide predecessor (not copied) | safe |
| the C-arm decks on the CNS template (v9, v10, v3, v2) | 21-slide C-arm decks | **disclose Part B and the sweep; never show publicly**; not copied (project 01 / 99) |
| `Desktop/CNS2026_Schwing_LSTV.pptx` (copied: `manuscripts/talks/cns2026/`) | 7 Sep draft "Naming a Lumbar Level Without Counting From C2" | draft, not presented |
| generators `ctsp:paper/cns2026/make_cns_deck*.py`, `prep_*`, `figs*` (copied: `manuscripts/talks/cns2026/`) | not tracked (45df97d; `.git/info/exclude`); must never be pushed | — |

Deck rules (`context/cns-deck-v2-2026-09-25.md`): CNS template traps (titles about 60 characters; zero-height text
boxes make PowerPoint refuse the file); ACCME rules (no disclosure slide, study design and dates on every data slide,
generic names, no ineligible-company logo, HIPAA statement); render with PowerPoint COM (no LibreOffice on this
machine) and look at every slide; no two consecutive results slides in the same visual form; the NeurIPS track is
"Evaluations and Datasets". Whether the slides were submitted to the meeting, and by what deadline, is not recorded.

---

## M20. Contradictions between documents (the rows that touch this project)

| id | readings | trusted, and why |
|---|---|---|
| C1 | Zenodo: `context/hf-mirror-is-v10.md` and `context/zenodo-deposit.md` say v10 is current; the student board says "v11 in preparation"; against: `ctsp:paper/mpda/cover_letter.md`, `title_page.tex`, `CAMERA_READY_NEURIPS/src/checklist.tex` and a disclosure timeline all give v11 = 10.5281/zenodo.22797014 published 18 Sep 2026 | v11 is on Zenodo (four documents give the DOI and date); the Hugging Face mirror is still v10 (checked by API 2026-09-27); not re-verified today: open https://doi.org/10.5281/zenodo.22797014 |
| C5 | affiliation: memory and the SchwingNet front matter General Surgery; MPDA, NeurIPS, arXiv, Cureus, JEEHP, TTO README "Department of Surgery"; the QI paper, main_v2, the TechFair slide "Neurosurgery" | never Neurosurgery (binding); "Surgery" vs "General Surgery" is Greg's choice |
| C6 | role: MPDA title page "a faculty surgeon"; TTO README and the HPR form "Resident physician" | resident; fix the MPDA title page |
| C7 | conflicts: MPDA "no relevant conflicts"; NeurIPS "No conflicts of interest"; the SchwingNet front matter "a commercial interest in a level-confirmation product under development" | unresolved; counsel sees the COI statement before filing; Greg decides one consistent statement |
| C8 | MLHC: memory "rejected"; `ctsp:docs/ROADMAP.md` "in review, score 2.75/4" | rejected |
| C10 | MPDA cover letter "shares no text, figure or table" vs NeurIPS appendices G / H "Adapted from" the article | unresolved |
| C11 | the NeurIPS senior author: the student board "senior author, dataset article"; the MPDA lists 14 authors without him; he is last author on NeurIPS | MPDA title page for the MPDA |
| C12 | Castellvi "each reading every case independently" vs reads dated by 4 Sep with prior exposure to the May sheet | the NeurIPS audit |
| C16 | "current" CNS deck v12_public vs the CNStemplate decks that disclose Part B | v12_public for anything public |
| C17 | the RPPR "developed and validated a single-shot CT segmentation model" and the CNS 66629 title vs no evaluated one-shot model on disk | no evaluated single-shot model is recorded |
| C18 | `ctsp:paper/mpda/REPRODUCE.md` section 0 "v10 ... S1=29" vs `ctsp:CLAUDE.md` v11, 29 retired | CLAUDE.md |

## M21. One order of work for whoever takes these over

1. **Ask Greg six questions** (none answerable from disk): was SchwingNet uploaded; was the MPDA's 2026-09-25 packet
   uploaded and under what number; has the TTO advised and is the provisional filed; what is the VinDr determination
   number; was BIBM 2026 submitted; is the NeurIPS camera-ready deadline past.
2. **Disclosure first.** Until the provisional is confirmed: no SchwingNet, QI, focused or main_v2 text, figure or deck
   anywhere public; only `CNS2026_Schwing_NotAllSpines_public_v12.pptx` for the talk; run `ssn:tools/disclosure_audit.py`
   before any talk or upload; Greg files the GitHub purge requests.
3. **NeurIPS camera-ready** (accepted, has a deadline): section M7 redo plan.
4. **MPDA**: section M6 corrections; reprint check; packet.
5. SchwingNet paper 1 (project 01).
6. **CNS posters** (2 Nov): re-check each student abstract's numbers against v11 and the fixed estimators.
7. Med-ed (project 11).
8. **The Radiology: AI CT paper** and the others: start only with Greg's go-ahead; each needs new data, human reads or
   a v11 recomputation first.

Every step follows the house pattern: results file -> manifest key -> `\RESULT{}` -> strict build -> render and look.

---

## R4. CT-based projects (`RESEARCH_DIRECTIONS.md` section 4, the rows this project owns or shares)

Ranked by how little stands between the holding and a result, and by what each unlocks. Every project names its
outside check. (CT-1, CT-2, CT-4, CT-5, CT-8, CT-9 belong to projects 04, 05 and 06.)

| rank | project | question | data | comparable published number | first experiment | gate | n or power | outside check |
|---|---|---|---|---|---|---|---|---|
| CT-3 | the whole-cohort Castellvi read, the seven re-reads and the VerSe raw-mask L6 count | how many Castellvi II to IV spines does CTSP hold, and does the rib anomaly co-segregate with the lumbosacral one | 802 CTs, 789 countable; 33 consensus grades, two residents, kappa 0.74, no senior read; the MPDA line 707 records only the six resolved disagreements; queues `castellvi_reread_queue.csv` 25, `castellvi_type1_queue.csv` 214, `lstv_reread_queue.csv`; VerSe raw masks on the grid under the VerSeFusion `data/unified/scan-*/`, never `vf_813` | Castellvi II to IV 9.0 % of 3,855 CTs, type I 68 % of calls; CT inter-reader kappa 0.63 to 0.71; Nagata 2025 co-segregation; VerSe OR 3.61 [2.08, 6.27] on 280 graded | one script counts ids 25 and 28 per raw mask against the Loeffler table with the 37 duplicate series collapsed; a third reader blind to the first two reads 0008, 0021, 0033, 0049, 0176, 0179, 0196, 0172 and 0068; then two readers grade all 802 in the review tree with a senior adjudicator | the II to IV rate inside 9 to 18 % and type I near 68 % of calls or the read is suspect; second-reader kappa at or above 0.63 or a third reader before anything trains; a VerSe subject enters the L6 pool only when table and mask agree | 802 cases at 3 to 5 minutes is 40 to 67 reader-hours per stage; expected positives 71 to 142 (9 to 18 % of the 789 countable records); the stump-rib against II to IV test has power 0.98 at OR 3.61 and 0.59 to 0.81 at OR 2.1 | the prevalence band; the readers' CTSP L6 rate 16 of 789, 2.0 % [1.3, 3.3], against the 3.2 % prior; the token join through the manifest field only |
| CT-6 | the L6 learnability curve on Dataset815 | at how many distinct six-lumbar cases does L6 Dice leave zero, and does the rib-free counting decoder beat it at every n | Dataset813 with stale flags, 23 against 34; Dataset815, 1,176 cases, 62 L6 by manifest, never preprocessed; VerSe masks with id 25 on 44 of 76 read L6 | VerSe'20: 85 L6 scans in the whole set, and 28 in its training split sufficed; VerTE-MT L6 Dice 81.03 % public, 75.96 % hidden | preprocess Dataset815 where singularity resolves, repair the flags from the deposit manifest, then one fold at 18, 36 and 62 distinct L6 with case-level oversampling and a lumbar-rib signature | the preflight refuses a validation fold with fewer than two variant cases; the endpoint is the rib-free count by status, not Dice | three points on a curve, 18, 36 and 62, read against the 28 training-split scans of VerSe'20, not the 85; qualitative, zero against not zero | the counting decoder on the same folds, 6 of 6 on truth input; the 25-presacral share 5.5 to 8.2 % |
| CT-7 | the anchor-ordinal design: detection by disagreement | do two dense ordinal fields, count from the sacrum and from the lowest rib-bearing body, plus a per-body type, flag the variant as a consistency violation | 802 CTSP; rib-free count against the source label, normal and transitional: count 4 in 21 and 8, count 5 in 736 and 7, count 6 in 9 and 18 (`ANCHOR_ORDINAL_DESIGN.md` lines 389 to 392); the table sums to 799 while its caption says all 802, a disagreement inside the file | Schinz 2026; MPDA 0.990 | arms 1 and 2 of the design as a matched pair on the same folds; the delta is the result | an ROC on the count disagreement separating the 26 transitional-labelled records at counts 4 and 6 (8 plus 18) from the 757 normal-labelled records at counts 4 and 5 (21 plus 736), at AUC above the rib-free count alone; the 7 transitional at count 5 and the 9 normal at count 6 are the cells a count alone cannot separate | 16 lumbar-rib cases stay 16 | patch geometry measured on the corpus, T11 to S1 about 265 mm, bi-iliac 278 mm median |
| CT-10 | the competitor benchmark, finished in one scoring space | on the same 802 records, what count and name does each public system give, and where does each fail on the 33 graded | `ssn:benchmark/cases.csv`; TotalSegmentator native outputs; SPINEPS plus VERIDAH relabelled stores; VISTA3D set up | VERIDAH 99.18 %; TotalSegmentator L6 0 of 1,152 here; HealthOST 91.49 % | run `ssn:benchmark/collect.py` and print the offset histogram and the whole-spine shift count per phenotype | every mask passes `assert_verse_monotonic`; truth scores Dice 1.000 through the same path | 802, 33 graded, 18 L6, 9 four-lumbar | a system's number on its private cohort and its number here are two numbers |
| CT-11 | segmental mobility from the 351 prone and supine pairs | per-segment lumbar angular change between prone and supine | 351 within-patient pairs; one acquisition per pair labelled | none on disk for paired-posture CT; Panjabi segmental ROM as the envelope | pseudolabel the second acquisition of 20 pairs out of fold; require PI to agree within its repeatability before any angle is read | PI invariance across the pair | 351 pairs | PI invariance |

Two housekeeping items sit beside these and gate publication rather than research. The first is the dataset
article resubmission at Medical Physics: seven items needing Greg, and `REPRODUCE.md` section 0 and Known-open item 1
corrected to v11 and to the solved 128-record failure. The second is paper 1's eight rigor fixes (project 01).

## R6. The ranked project list (the rows this project owns or shares)

| rank | project | first step | gate | n today against n needed | the decision it returns | depends on |
|---|---|---|---|---|---|---|
| 4 | CT-3, the re-reads, the VerSe mask count and the whole-cohort Castellvi read | the VerSe raw-mask count script, under an hour; the nine CTSP re-reads with a third reader | II to IV rate inside 9 to 18 %; second-reader kappa at or above 0.63 | 33 graded against 71 to 142 expected | the lumbosacral truth pools and the rib co-occurrence test at power 0.98 | two readers and an adjudicator |
| 13 | CT-6, the L6 learnability curve on Dataset815 | preprocess 815 where singularity resolves; repair the flags | Dice leaves zero at 36 or stays zero at 62 | 62 distinct L6 with a read | whether L6 is learnable as a voxel class from this corpus | GPU time; CT-3's flags |
| 14 | CT-5, CT-7, CT-8, CT-9, CT-10 | as in section 4 | as in section 4 | as in section 4 | atlas revision; the anchor-ordinal premise; the rib phenotype; the census adjudication; the benchmark | CT-1; the PREREG freeze; readers |
| 15 | PUB-1, the dataset article resubmission and paper 1's rigor fixes | the seven items to Greg as a list; `build.sh --reprint`; the eight fixes on existing outputs | ten published pages; `eval_gate` held out on every quoted row | none by policy | a citable dataset article; a submittable paper 1 held for the TTO | Greg; the TTO answer |
| 16 | CT-11, prone and supine mobility | twenty pairs pseudolabelled out of fold | PI invariance | 351 pairs | a later paper | recorded as not a now-thing |

Week one has no model in it. The COBRA coverage render and the VerSe mask count run as single one-hour jobs on
`reqp`. The reader queues open: the seven CTSP re-reads plus 0172 and 0068 first, then the 63 field-supported
volumes, then the 802 for Castellvi grade. If CT-3's re-reads move a record, the G3 split changes and the leak audit
is re-run before anything scores anyone.

---

## L1.1. Vertebra-labelled CT (`LITERATURE_STATE.md` section 1.1)

| dataset | held n | labels | licence, access | card |
|---|---|---|---|---|
| CTSpinoPelvic1K (yours) | 802 records, one per patient, and 802 label volumes (MPDA lines 226, 435, 801); 1,153 distinct spine and pelvic series UIDs across those records. The NeurIPS paper used the April release of 1,153 records over 802 patients (NIPS lines 90 to 91, 194) and scored 1,152 records of 801 patients (NIPS lines 299 to 301) | vertebrae C1 to L6 from CTSpine1K radiologists; sacrum, hips, femora; ribs (TotalSegmentator plus the Möller network, student-corrected); Castellvi two-reader consensus on 33 | open; labels CC BY-NC-SA; Zenodo v11. HELD; the Hugging Face mirror still carries v10 labels | MAN#ctspinopelvic1k |
| TCIA CT COLONOGRAPHY | 825 patients, 3,451 series | none (the CT behind CTSpinoPelvic1K) | open | MAN#tcia_ct_colonography (HOME state unknown) |
| CTSpine1K | 1,005 volumes (COLONOG 784, MSD-T10 150, COVID-19 40, HNSCC-3DCT-RT 31) | expert VerSe-convention masks C1 to L6 and sacrum | open; CC BY-NC-SA. HELD on Ceph; HOME copy presumed deleted | MAN#ctspine1k |
| CTPelvic1K | 1,184 scans in 7 sub-datasets (MPDA) | radiologist-supervised pelvic masks; no vertebra numbering | open; CC BY or BY-NC, quoted both ways. PARTIAL: masks of datasets 1 to 5 plus clinical datasets 6 and 7 (178 listed, 173 on disk, 172 converted) | MAN#ctpelvic1k |
| VerSe'19 and '20 | 374 scans of 355 patients, 4,505 vertebrae | expert masks C1 to L6, T13 = 28; no sacrum | open; CC BY-SA or CC BY, quoted both ways. PARTIAL: 10 VerSe'20 series never downloaded, VerSe'19 copies substituted silently | MAN#verse19_20 |
| VerSeFusion (project) | 374 unified scans | release masks; VERIDAH renumbering of 14 scans; pseudo ribs | project. HELD | MAN#versefusion |
| TotalSegmentator v2 | 1,228 subjects | 117 masks each; no L6 or T13 class | open; CC BY. HELD | MAN#totalsegmentator_v201 |
| TotalSegmentator v3 | 1,939 folders, 1,935 distinct scans (286 under 18) | refined bone labels | open. HELD; 24 subjects alias v2 ids | MAN#totalsegmentator_v300 |
| RibFrac with RibSeg v2 | 660 chest CTs; 661 rib masks | fracture labels; ribs 1 to 24 | CC BY-NC. HELD | MAN#ribfrac |
| Möller 2025 stump-rib masks | VerSe 323 + RibFrac 420 public subjects (743); final analysis set 648, of whom 133 carry a stump rib (why 95 were left out is not recorded) | rib masks | CC BY; Zenodo concept 14850928, version 14864106. HELD; adds no new subjects | MAN#ribfrac |
| RSNA 2022 cervical fracture | 2,019 studies; 961 with a fracture | per-level C1 to C7 fracture labels; 87 segmentations | Kaggle rules, non-commercial. HELD | MAN#rsna_2022_cspine |
| CSI 2014 spine CT | 20 | vertebra masks | ODC-By. HELD | MAN#csi2014 |
| PENGWIN 2026 pelvic fracture CT | 340 (308 after folding onto CTPelvic1K) | fragment masks | CC BY-NC-SA. HELD | MAN#pengwin2026 |
| Pelvic-Reference-Data (IDC) | 58 | none for vertebrae | CC BY. HELD | MAN#idc_pelvic_reference_data |
| VertebralBodiesCT-Labels (HF) | 1,460 (ROAD) | numbered bodies T1 to T13, L1 to L6, S1 | CC BY-SA. PARTIAL: only its external L6 and T13 reads on 70 TotalSegmentator CTs are used; the masks have no card | MAN#totalsegmentator_v201; MAN#validation_ts |

`MAN#...` cards are in the data platform manifest (project 10, `ssn:data_platform/DATA_MANIFEST.md`).
