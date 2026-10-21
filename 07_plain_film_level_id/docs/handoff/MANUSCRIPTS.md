# Manuscripts, abstracts, decks, disclosures and data requests

**Reader: Greg and the Claude project only.** This file carries the disclosure, TTO and provisional record (§1 row 16,
§2.6 item 4, §2.7, §2.8 items 1-2, §5, §15, §20 C4 and C7, §21 items 1-2); a student copy needs those parts cut first
(`GREG_ONLY/PRIVATE_STATE.md` §5).

Every written work found on 2026-10-08: title, venue, paths, state, what is finished, what must be redone, the claims
map, the binding style rules, and a redo plan in order. Built from `working_notes/topic4_manuscripts.md` (which keeps
the full tables) and the files it cites. Path prefixes: `ssn:` spinesurg-ct-nnunet (private), `sn:` its `SchwingNet/`,
`ctsp:` CTSpinoPelvic1K-1 (public), `<laptop:Desktop>/` = `<laptop:Desktop>/`, `context/` = the memory copies here.

**When the state was frozen.** The last commits touching `sn:main.tex`, `sn:sections/` or `sn:supplement.tex` are 7e81dd7
(2026-09-27 13:17, the film N-curve ablation enters the text) and the rebuild of record 05e05dc (13:30); the last
SchwingNet commit is 4e3fe93 (17:12, adds only `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md`) (`git log`, 2026-10-08).
In `ctsp:` the last content commit to a paper is 38b0cb9 (2026-09-25 17:23, "NeurIPS camera-ready ... 21 pages"),
after 70de829 (10:34); 45df97d (2026-09-26) stopped tracking `paper/cns2026`; the NeurIPS camera-ready edits of
2026-09-27 are uncommitted (§7). No commit touched a manuscript between
2026-09-28 and 2026-10-07 in either repository. `ctsp:paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` was rebuilt
2026-10-08 09:41 (10 pages); who rebuilt it is not recorded.

---

## 0. The rules that bind every item

| rule | source |
|---|---|
| Never the word `ctsp:CLAUDE.md` "Standing preferences" bans for the origin of data; write origin, lineage, where it came from | `context/writing-preferences.md` |
| No fractional version numbers; fold into the next integer version | same |
| Figure captions at most 60 words (target one or two sentences, about 25 words); the argument goes in the text; measure caption-to-text gaps with pymupdf | `context/figure-captions-terse.md` |
| Capability / matrix tables in solid black plus at most one outlined mark, never colour, cells touching | `context/tables-black-not-colour.md` |
| Medical Physics: sans-serif figures (Arial / Helvetica), grey grid on both axes, ticks out / in, the degree symbol, numbers under ten spelled out, kV not kVp, 80 or 180 mm wide, 600 dpi; **no abstract in the main document of a Dataset and Software article**; 10 PUBLISHED pages measured only by `build.sh --reprint` | `context/journal-figure-and-style-rules.md`; `ctsp:CLAUDE.md` |
| Radiology: Artificial Intelligence: 3,000 words, a 250-word four-part abstract, 6 figures of at most four panels, 4 tables, 35 references, CLAIM 2024, double-anonymised, TIF / EPS figures; arXiv allowed with disclosure; supplement at most 12 pages | `context/rsnai-author-instructions.md`; `sn:RSNA_AI_REQUIREMENTS.md` |
| Slides: no sideways bar charts; donuts and lines; background slides reproduce the cited paper's own figure ("permission pending"); 3-4 lines of 18-20 pt; a manuscript figure goes on a slide one panel at a time | `context/chart-preferences.md` |
| SchwingNet figures judged as a reader would; audit-style plots go to `docs/`, not the paper | `context/figure-preferences-schwingnet.md` |
| Never state the commercial goal in anything that leaves; never name the product | `GREG_ONLY/context/commercialization-stance.md` |
| Never re-add SchwingNet level-identification text or `ctsp:paper/cns2026` to a public repository; only `<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v12.pptx` is safe to show | `GREG_ONLY/context/schwingnet-disclosure-scrub.md`; `context/fluorocap-repo-private.md`; `context/cns-deck-v2-2026-09-25.md` |
| Affiliation is NOT Neurosurgery: "Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center" | `context/user-affiliation-general-surgery.md` (contradiction C5) |
| Ashley Schehr is a person (med-ed first author, annotation lead), never a product name | task brief; `ctsp:Student_Projects/BOARD.md` |
| Read before writing under `ssn:paper/` (a `main.tex` was overwritten once and restored from git) | `ssn:docs/RSNAI_PLAN.md` A3 "Incident 11:35" |
| LITT / U251 instrument statements stay conditional (other project) | memory note `litt-contralateral-two-readings` (not copied; U251) |
| Every printed number comes from a results file through a manifest key (`\RESULT{}`); the build fails on a bare numeral | `sn:RESULTS_BUILD.md` |

---

## 1. Overview

| # | work | venue / purpose | state as recorded | main files |
|---|---|---|---|---|
| 1 | SchwingNet, paper 1: "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" | Radiology: AI, Original Research | complete in review and camera-ready copies; one placeholder (VinDr determination); supplement 13 pages > 12; Word packets stale; **held pending the WSU technology transfer office** | `sn:` |
| 2 | Paper 2: SchwingNet vs registration-assisted surgeons (LevelCheck) | not chosen | comparator frozen; blinded gate cancelled 2026-09-27; needs human reads | `sn:paper2_levelcheck/`, `sn:LEVELCHECK_MODEL.md`, `sn:LEVELCHECK_CLAIM.md` |
| 3 | Older C-arm drafts: "Naming Vertebrae Without an Anchor"; "Making the Intraoperative Count Exact"; "Navigation from the C-arm alone"; the k-devices skeleton | Radiology: AI, each in turn | superseded; sources to lift from; two disclose the undisclosed sweep | `ssn:paper/rsnai/`, `ssn:paper/focused/` |
| 4 | **QI paper**: "The Universal Protocol with a level in it ..." | The Joint Commission Journal on Quality and Patient Safety | 9-page draft, builds; not submitted; discloses invention aspects | `ssn:paper/qi_universal_protocol/` |
| 5 | CTSpinoPelvic1K dataset article ("MPDA") | Medical Physics, Dataset and Software Article | submitted; returned twice for format; third packet built 2026-09-25; upload not recorded; arXiv 2609.22760 public | `ctsp:paper/mpda/`, `ctsp:dist/submission/` |
| 6 | "Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae" | NeurIPS 2026 Evaluations and Datasets Track, submission 3474 | **accepted (poster) 24 Sep 2026**; camera-ready 31 pages with 134 `[pending]` slots; jobs cancelled; not uploaded | `ctsp:CAMERA_READY_NEURIPS/` |
| 7 | "CTSpinoPelvic1K: A Unified CT Benchmark for LSTV Segmentation" | MLHC 2026 research track | rejected | `<laptop:Desktop>/MLHC_2026_Research_Track_Paper.pdf` |
| 8 | CT one-shot / numbered-rib paper | Radiology: AI | draft with 22 `\todo`; results never landed | `<laptop:Desktop>/NextPaper/RadAI/main.tex` |
| 9 | NeurIPS revision draft (AR) and VerSeFusion | NeurIPS D&B | AR frozen 2026-09-08 as a source; VerSeFusion submission not recorded | `<laptop:Desktop>/NextPaper/AR/`, `NextPaper/VerSeFusion/` |
| 10 | BIBM wrap-up "From Segmented CT to Spinopelvic Measurement" and XRSpinoPelvic1K | IEEE BIBM 2026 (deadline 5 Jul 2026) | draft with `\TODO`s; submission not recorded; XRSpinoPelvic1K private since 2026-09-26 | `<laptop:Desktop>/NextPaper/bibm-spinopelvic/`, `<laptop:Desktop>/XRaySpinoPelvic1K/`, `ctsp:BIBM/` |
| 11 | "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy" | Spine Surgery and Related Research | complete draft with numbers; first author unassigned; computed before v11 | `ctsp:paper/clinical/main.tex` |
| 12 | OpenSpineConsortium medical-education study | **published in Cureus** 14 Jul 2026 (doi 10.7759/cureus.112661); JEEHP version on disk; CNS 2026 printed poster 66639 | published; a JEEHP submission would duplicate it | `<laptop:Desktop>/cureus.pdf`, `ctsp:OSC MedEd Manuscript - JEEHP.docx`, `ctsp:Med_Ed_CNS*.pptx` |
| 13 | CNS 2026: 12 OSC abstracts, Greg's mini-oral 66629 and its deck | CNS Annual Meeting, Washington DC, 31 Oct-4 Nov 2026; talk MP4SP1 Mon 2 Nov 5:21 PM | accepted; disclosure-safe deck v12_public | `<laptop:Desktop>/CNS2026_*.pptx`, `ctsp:paper/cns2026/` (untracked by design) |
| 14 | CNS 2026 Abstract 418 (LITT) deck | CNS 2026 | other project (U251); deck v6 on disk, memory describes v5 | `<laptop:Desktop>/u251-xenograft-murine-RNASeq-study/SLIDES/` |
| 15 | AACA Tech Fair "Harnessing Algorithmic Disagreement for Automated LSTV Detection" | 43rd AACA meeting, Mayo Clinic, 13 Jun 2026 | presented | `<laptop:Desktop>/TechFair_LSTV_Schwing.pptx` |
| 16 | Invention disclosure, provisional package, disclosure memo, TTO package | WSU Office for Technology Commercialization; counsel | disclosure submitted 2026-09-25 (signed form on disk); provisional filing not recorded | `ssn:docs/INVENTION_DISCLOSURE.md`, `ssn:docs/provisional/`, `<laptop:Desktop>/private_ip/` |
| 17 | Fluoroscopy and C-arm data requests | 14 cine sources, SX-Stitch, Balgrist | drafted, all `requested_not_sent` | `ssn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `ssn:docs/fluoro_requests_eml/`, `ssn:docs/data_requests/`, `ssn:docs/outreach/` |
| 18 | Flagship / feasibility / guided-acquisition plans | internal | gate tables; superseded in part by the paper split | `ssn:docs/FLAGSHIP_PLAN.md`, `FEASIBILITY_REPRODUCE.md`, `RSNAI_PLAN.md` |
| 19 | NIH F30 year-4 progress report (RPPR) and sponsor letter | NIH | written and sent July 2026 | `ctsp:RPPR_Accomplishments.{docx,pdf}`, `ctsp:Sponsor Progress Report Letter 2026.*` |

---

## 2. SchwingNet, paper 1 (Radiology: Artificial Intelligence)

### 2.1 What it is and how it got here

Title: **SchwingNet: a convolutional-recurrent network for level naming in spine surgery** (the review copy prints
"[AuthorLastName]-Net: ..."; `sn:TITLE.md`). It lost "versus registration-assisted neurosurgeons" on 2026-09-24 (the
comparison moved to paper 2) and "robust to transitional anatomy" at ~22:15 the same night (Greg: "If it's not robust to
transitional anatomy, then it should be removed from the title"; `sn:TITLE.md`, `sn:CLAIMS_LEDGER.md` §9).

Lineage of drafts (each supersedes the earlier): `ssn:paper/rsnai/main.tex` "Naming Vertebrae Without an Anchor"
(2026-09-17 to 09-19) -> `ssn:paper/focused/main.tex` "Making the Intraoperative Count Exact" (09-19 to 09-22) ->
`ssn:paper/rsnai/main_v2.tex` "Navigation from the C-arm alone" (09-22; numbers from `claims.tex` <- `tools/claims_fill.py`
<- `ssn:docs/RSNAI_CLAIMS.json`) -> `sn:main.tex` from 2026-09-22 evening, built only from rigor-passing numbers
(`context/schwingnet-manuscript.md`); six figures on 09-23, five figures and three tables since 09-24
(`context/paper-split-2026-09-24.md`; `sn:PAPER1_SCOPE.md`).

### 2.2 Where everything is (`sn:`)

| path | what |
|---|---|
| `main.tex`, `sections/{introduction,methods,results,discussion_motivation,discussion_limits}.tex` | the manuscript (cai4cai / RSNATemplate skeleton; `TEMPLATE_NOTES.md` records departures) |
| `supplement.tex` | Figures S1-S5, Tables S1-S4 |
| `rsnastyle.tex`, `rsnaresults.sty`, `nejm.bbx/.cbx`, `latexmkrc` | style; `\ifcameraready` selects `\netname{}`, `\withheldurl{}`, `\selfcite{}` |
| `numbers_manifest.json` -> `tools/results_macros.py` -> `generated/{numbers.tex,numbers_audit.md,pending.json}` | the results-driven build; `pending.json` (2026-09-27 17:15Z): 79 resolved, 0 pending |
| `NUMBERS.md` | every number in text, tables and figures with its source (older trace; section headings carry pre-09-24 numbering) |
| `CLAIMS_LEDGER.md` | **the claims map**: every superlative, "first" and comparison with its published comparator, our file, and a verdict (DEFENSIBLE NOW / AFTER Gx / REWRITE); "The Discussion is built from this file and nothing else" (line 5) |
| `CLAIM_CHECKLIST.md`, `claim_checklist.json`; `packet_src/claim2024/map.json` -> `packet_src/build/CLAIM_CHECKLIST_2024.md` | CLAIM 2020 (42 items) and the CLAIM 2024 map the packet submits (2026-09-27: READY 35, PENDING 3, NEEDS-EDIT 6) |
| `atlas/{model,dataset}.json`, `validate_cards.py`, `VALIDATION.md` | RSNA ATLAS 2025-11 cards (**stale numbers, see §2.6**) |
| `figures/figure1..5.*`, `figureN.caption.txt`, `figureN.record.json` | main figures; each record lists every drawn number with its `file#key` |
| `tables/tab_corpus.tex` (Table 1), `tab4_transitional.tex` (2), `tab3_naming.tex` (3); supplement `tabS1_device_terms.tex`, `tab2_detection.tex`, `tabS3_corpus.tex`, `tabS4_ablation.tex` | each main table has a `.md` twin and a `.sources.md` naming the file behind every cell; `tabS4_ablation.tex` has neither; the `.md` twins of Tables 2 and 3 are stale |
| `PAPER1_SCOPE.md` | no G3 test transitional person is scored in paper 1 |
| `REVISION_LOG.md`, `REVISION_LOG2.md`, `REVISION_LOG3.md` (§1-13, to 2026-09-26) | change logs |
| `REVIEW_RSNA.md`, `REVIEW2_RSNA.md`, `REVIEW_STATS.md` (F1-F22), `REVIEW2_STATS.md`, `DRIVE_CHECK.md`, `REFS_AUDIT.md`, `FINAL_CHECK.md` | internal adversarial reviews and checks (`FINAL_CHECK.md` is the 09-22/23 state, stale) |
| `RSNA_AI_REQUIREMENTS.md` | the journal limits verbatim (pasted by Greg 2026-09-22) |
| `lit/CITABLE_CLAIMS.md`, `lit/acquisition_space_review_2026-09-24.{pdf,txt}` | an external review's claims checked one by one (only VERIFIED rows enter the text; the review itself is not cited) |
| `sections/SOURCES.md`, `sections/methods_sources.md` | which earlier draft each paragraph came from |
| `packet_src/` (`build_packet_src.py`, `front_matter.json`, `statements.md`, `cover_letter.md`, `supplement_technical.tex`, `build/`) | front documents |
| `packet/`, `packet_cameraready/` | Word packets from `tools/make_packet.py` (2026-09-25 15:42: stale) |
| `packet_build/` | fetched grid PDFs; latest `SchwingNet_{review,cameraready}_main_and_supplement_2026-09-27.pdf` (36 pages each) |
| `paper2_levelcheck/` | everything moved to paper 2 |
| `slurm/compile.sh` | grid build (texlive/2020, xelatex + biber; flock since 05e05dc; `CAMERAREADY=1` for the camera-ready) |

Figures and tables with their builders and data are in `RESULTS_CATALOG.md` part A (header) and `RECIPES.md` §1;
in short: Figure 1 `tools/figure1.py`; Figure 2 `tools/figure2.py` + `figure2_analyse.py` (selection split, said in the
caption); Figure 3 `tools/figure3_network.py` (schematic); Figure 4 `tools/figure4_frame.py --models v9init_pre --pull`;
Figure 5 `tools/fig_power.py`; S1 `tools/fig2_flow.py`; S2-S5 `tools/figS_supplement.py`; Tables S1, S3, S4
`tools/make_supp_{device,census,ablation}_table.py`; Tables 1-3 and S2 hand-built with `.sources.md`.

Headline numbers as printed (Key Points): never trained on the C-arm, 595 of 617 detected lateral vertebrae (96.4 %;
92.3, 98.4) in 141 cases against 276 of 631 AP (43.7 %); count from the detected sacrum 979 of 1,009 (97.0 %); fine-tuned
1,079 of 1,159 lateral with three in view (93.1 %) and 608 of 631 AP (96.4 %); coupled 991 of 1,009 (98.2 %); L6-vs-L5
silhouette 0.35 vs L5-vs-L4 0.23 (selection split); 35 error-free at-risk persons needed to certify 90 %, seven real-frame
candidates exist. Every one with its file: `RESULTS_CATALOG.md` part A.

### 2.3 Limits and build state

| item | count | limit | source |
|---|---|---|---|
| body words | 2,998 (review copy, RESUME 2026-09-27 13:20); 2,988 (commit 044ca9a); 2,986 (camera-ready counter, `BUILD_REPORT.md`) | 3,000 | not settled without running `tools/check_limits.py` |
| abstract | 249 words | 250 | `sn:packet/PACKET_README.md` |
| summary statement | 244 characters | 255 | same |
| figures / tables | 5 (at most four components each) / 3 | 6 / 4 | `main.tex` |
| references | 32 review, 33 camera-ready | 35 | `PACKET_README.md`; `BUILD_REPORT.md` |
| **supplement** | **13 pages** | **12** | commit 05e05dc; `packet_build/review/supplement.pdf`; `RSNA_AI_REQUIREMENTS.md` line 21 |

Builds of record: grid jobs 40483839 (review) and 40483840 (camera-ready), 2026-09-27: latexmk rc 0, main 23 pages,
supplement 13 pages, zero warnings, RESULT_PENDING 0. The concurrent pair 40483834 / 40483835 raced on `main.aux` and was
discarded (hence the flock). `check_limits.py` fails on exactly one thing: the `\PENDING{G0}` token for the VinDr
determination number and date in the Ethics paragraph (`main.tex` line 137). There is no TeX on the Windows workstation.

### 2.4 The rigor audit, item by item (2026-09-22; `context/rigor-audit-findings.md`; `sn:results/RIGOR_FIXES.md`)

| item | answer in paper 1 | still open |
|---|---|---|
| A1 detector number threshold-dependent, no interval | the cross-device threshold 0.74 is quoted with the full recall-against-confidence curve; 0.25 kept "as quoted" | call 0.74 "cross-device", never "pre-stated" |
| A2 selective reporting (`rescore_outline` 1,440 cells; manifold three feature spaces) | multiplicity stated in Methods; all three manifold spaces reported (`a2.json`) | none recorded |
| A3 no paired tests | paired comparisons with the interval of the difference, Holm-adjusted (`a3.json`) | none |
| A4 percentile interval at the ceiling | BCa beside the percentile interval | none |
| A5 film intervals clustered by vertebra; leaked v2 bank | patient-clustered on the clean-for-film v8 bank | the v9-bank re-score (chain 40415667 -> 40415670) "had not landed"; later state not recorded |
| A6 criterion C3 never evaluated per fold | evaluated as written (`a6.json`): not met | none |
| A7 selective prediction invisible; abstention untuned | an abstention operating point beside every naming headline; "at full coverage" everywhere; the leaked 99 %-at-35.7 % absent | a clean re-run of selective prediction is not recorded |
| A8 verse_drr millimetres | prohibited; none printed | none |
| A9 C-ArmLSpine groupings | case-grouped five-fold and day-grouped three-fold both reported (`a9.json`) | none |

### 2.5 Claims map

Three layers, in order of authority: `sn:CLAIMS_LEDGER.md` (every claim that compares or ranks, with its published
comparator and verdict; the Discussion is built from it alone); `sn:numbers_manifest.json` + `generated/numbers_audit.md`
(every printed number with its file, JSON pointer, job and the file's SHA-256); `sn:NUMBERS.md` (the human-readable trace
and the "Numbers deliberately absent" list). For the superseded `main_v2.tex`, `ssn:docs/RSNAI_CLAIMS.json` (54 claims)
checked by `python tools/claims_check.py` (exit 1 on drift). Citation traps recorded in `context/rsnai-paper-endpoint.md`:
no source gives "three or four bodies" or a 9-inch field; Siminski is Mayo Clinic Rochester; Macki's costs are fiducial
implantation; Furuya's 81 % is of lumbar events; the Universal Protocol cites `jcnpsg2025`; upadhyaya2012 has no cost
numbers.

### 2.6 What blocks submission

`sn:packet_src/build/BUILD_REPORT.md` (2026-09-27 13:26) lists seven author decisions; `build_packet_src.py --strict`
fails while any is open:

1. **vindr_irb**: VinDr-SpineXR is covered by WSU IRB HPR 2026-330 of 29 September 2026, the supplement to 2026-269, and its films are in the C-arm fold banks behind the
   fine-tuned numbers. Print that number and date where the manuscript carries its token (the HPR tool was filled and sent to Greg 2026-09-25:
   `ctsp:IRB_VinDr_2026-09-25/`, gitignored; draft `ssn:docs/IRB/HPR_determination_VinDr-SpineXR_draft.md`; the notice of
   2026-09-29 stays on Greg's laptop, out of every repository), or retrain the fold models without VinDr (`DATASET_USAGE.md` §5); the measured version of option (b) already exists: the 250 Figure 5b `name_fill` cells are v9-base fold models with no VinDr or FluoroCap (N = all lateral 98.1 %, AP 97.0 %; `RESULTS_CATALOG.md` A9.4; `DATASET_USAGE.md` §3.2), scored on REP truth per protocol cell, so not identical to Table 3. Greg's instruction of
   2026-09-25: assume it granted, leave only the number token.
2. **hf_mirror_v11**: the Hugging Face mirror serves v10 labels, a cc-by-nc-4.0 card and an Apache-2.0 LICENSE against
   Zenodo's CC BY-NC-SA 4.0; bring it to v11 under one licence or delete the mirror sentence.
3. **release_code_weights**: `ssn:docs/FLAGSHIP_PLAN.md` says weights are released; `ssn:docs/MODEL_CARD.md` §1.4 says code
   private, weights not released; `ssn:docs/INVENTION_DISCLOSURE.md` §9 advises holding weights as a trade secret. Pick
   `statements.md` WEIGHTS_OPTION_DEPOSIT or WEIGHTS_OPTION_AGREEMENT.
4. **filing_before_submission**: file the provisional and let counsel see the conflict-of-interest statement first
   (`ssn:docs/DISCLOSURE_MEMO.md` §7-8; `ssn:docs/provisional/FILING_CHECKLIST.md`: "The manuscript is held until the
   provisional is on file").
5. **title_clauses**: `front_matter.json` still describes the title with "robust to transitional anatomy".
6. **subject_overlap_list**: which of NeurIPS 3474, MLHC 2026, BIBM 2026 and the CNS 2026 abstracts to name in the cover
   letter's overlap paragraph.
7. **claim_form**: the journal requires CLAIM 2024; the repository docx is CLAIM 2020; upload
   `packet_src/build/claim_checklist_2024.docx` or paste its Location column.

CLAIM 2024 items not READY: 9 preprocessing, 13 acquisition protocol, 17 versions of TotalSegmentator and SPINEPS /
VERIDAH run on the CBCTs, 22 the body detector's training corpus by source and split, 24 initialisation, 25 training
details (all NEEDS-EDIT); 32 and 37 training / validation-partition performance (PENDING G5); 43 code / weights
availability (PENDING G7). Proposed text for several is in `packet_src/supplement_technical.tex`. 19 open `[[CONFIRM]]`
markers remain in the cover letter and full title page.

Defects found by reading timestamps and page counts: **the supplement is 13 pages** since Table S4 (2026-09-27; it was
trimmed back to 12 twice before, `REVISION_LOG3.md` §8 and §11 show how); **the Word packets are stale** (dated
2026-09-25 15:42, before the PDFs with the ablation; the packet README still lists "Tables S1-S2");
`tabS4_ablation.tex` lacks its `.md` and `.sources.md`; **the ATLAS cards** (`sn:atlas/model.json`,
`sn:packet/atlas/model.json`, `sn:packet_cameraready/atlas/model.json`) **carry superseded v2-lineage numbers** (594 / 617,
239 / 631, 606 / 617) instead of the printed 595 / 617, 276 / 631, 601 / 617; the twins `tables/tab3_naming.md` and
`tables/tab4_transitional.md` are stale against their `.tex`; `sn:README.md`, `FINAL_CHECK.md` and `figures/FIGURES.md`
describe the retired 2026-09-22/23 state.

### 2.7 Disclosure hold

The Part B manuscript is "complete and HELD pending the office's advice"
(`<laptop:Desktop>/private_ip/TTO_package_2026-09-25/06_disclosure_timeline.md`, row 25 Sep; `00_README_for_TTO.md` item 02;
copies given to the TTO: `02_CONFIDENTIAL_Part_B_manuscript_Radiology_AI.pdf` and `followup/..._rev2..rev5.pdf`). Paper 1
must not appear in any public repository. Whether the TTO has advised and whether the provisional was filed are not
recorded. **Contradiction C4**: the ERAS CV (`<laptop:Desktop>/ERAS_2026/CV_2026-09-27.pdf`) lists the paper as "Submitted" with
the old long title; the repository says held. Greg must say which is true; if the CV is wrong, the ERAS entry needs
correcting.

### 2.8 Redo plan for paper 1, in order

1. Ask Greg whether it was uploaded (C4).
2. Get the TTO / counsel answer on Part B and the provisional; do nothing public before it.
3. Close the seven decisions in `packet_src/front_matter.json`, including the VinDr determination number (HPR 2026-330, 29 September 2026); if the
   determination is refused, the measured version of option (b) already exists: the 250 Figure 5b `name_fill` cells are v9-base fold models with no VinDr or FluoroCap (N = all lateral 98.1 %, AP 97.0 %; `RESULTS_CATALOG.md` A9.4; `DATASET_USAGE.md` §3.2), scored on REP truth per protocol cell, so not identical to Table 3.
4. Correct Table 1's TotalSegmentator rows (`DATASET_USAGE.md` §6) and decide the FluoroCap "refused by the guard"
   wording (`DATASET_USAGE.md` §5).
5. Trim the supplement to 12 pages; give `tabS4_ablation` its `.md` and `.sources.md`; regenerate the ATLAS cards
   (`sn:atlas/update_cards.py`, `validate_cards.py`) and the stale `.md` twins.
6. Rebuild both copies on the grid one after the other (compile.sh holds a flock); fetch to `packet_build/`; run
   `python SchwingNet/tools/check_limits.py` (and with `CAMERAREADY=1`), `python SchwingNet/tools/results_macros.py --check`,
   `python SchwingNet/packet_src/build_packet_src.py --strict`, `python SchwingNet/tools/make_packet.py` (and with
   `CAMERAREADY=1`); render and look at every page (`SchwingNet/tools/render_pdf.py`).
7. Convert the remaining hand-typed table cells to `\RESULT{}` keys (the board task in `ctsp:Student_Projects/BOARD.md`
   "schwingnet"; the mapping is row by row in `NUMBERS.md` and the `.sources.md` files).
8. Settle Greg's open analysis items before any new number enters (RESUME 2026-09-27 18:05 "FOR GREG"): supplement Table
   S5 per level; the synthetic:real ratio sweep (45 cells); seeds 1-2 above N = 25; the denominator-repair wording
   (`REVISION_LOG3.md` §11); the "7 of 9" Discussion scope (`RESULTS_CATALOG.md` A10.9).
9. Verify the journal limits in a browser (pubs.rsna.org returns 403 to scripts).

---

## 3. Paper 2: SchwingNet against registration-assisted surgeons (LevelCheck)

| item | record |
|---|---|
| why it exists | Greg moved it out of paper 1 on 2026-09-24 ("move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper"); ordinary-only superiority over 97.6 % needs 152 zero-error persons; the transitional strata (19 persons vs 82.2 %) need human reads that do not exist (`context/paper-split-2026-09-24.md`) |
| moved material | verbatim with file and line in `sn:paper2_levelcheck/MOVED_FROM_PAPER1.md` (8 items, from dd8f4a5); `numbers_manifest_moved.json`; `tables/tab_levelcheck.{tex,md,sources.md}` |
| frozen comparator | `sn:LEVELCHECK_MODEL.md` §1-§15 (frozen ecae75f, last d0403de); never edit. Literature reading `sn:LEVELCHECK_CLAIM.md`. The comparator was pre-specified and never tuned; Greg asked for LevelCheck to "fail enough" and that was declined (`context/six-figure-paper-plan.md`) |
| open gate | job 40438004, ran 2026-09-25 04:22-06:02Z, ordinary persons only; **defect**: the reference-standard score was never written because `sn:tools/fig6_score.py` read `T1/blinded/meta_ref/` instead of `T1/open/meta_ref/` (`sn:paper2_levelcheck/open_gate_40438004/README.md`) |
| blinded gate | f6eval 40438005 (memory) / 40431765-66 (`REVISION_LOG3.md` line 7), held for Greg's truth decision, then **cancelled** 2026-09-27 15:50 (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`, which holds the resume instructions per job) |
| needs | human reads of the ~90 transitional COBRA test candidates; the automated reference calibration (`LEVELCHECK_MODEL.md` §14); a person-disjoint transitional test set (G3) |
| ledger caution | if paper 1 ever prints an ordinary-person real-frame accuracy, paper 2's ledger must record "H6 seen" (`PAPER1_SCOPE.md` item 3) |
| reserved title | "SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy, versus registration-assisted neurosurgeons" (`TITLE.md`) |
| redo | nothing until human reads exist; then fix `fig6_score.py`, re-score the open gate from the dumps on disk, resubmit the blinded gate from `sn:slurm/fig6_eval.sh`, never touch `LEVELCHECK_MODEL.md` |

---

## 4. Older C-arm drafts (sources only, private)

| file | state | caution |
|---|---|---|
| `ssn:paper/rsnai/main.tex` "Naming Vertebrae Without an Anchor: Registration-Free Level Identification on Limited-Field Radiographs" | superseded (last commit 6506470, 2026-09-20); built with `paper/rsnai/build.sh`; numbers from `ssn:slurm/reproduce_feasibility.sh` -> `~/model_night/repro_feasibility/LEDGER.tsv` (`ssn:docs/FEASIBILITY_REPRODUCE.md`) | uses banks later found leaky; 14 partly supported citing sentences were not corrected (`ssn:docs/RSNAI_PLAN.md` 12:10); a web copy exists at https://claude.ai/artifact/3DFZMHt4oAnrDVHwxdZnyf (`context/feasibility-claims-measured.md`) |
| `ssn:paper/rsnai/graveyard.tex` | material cut from the above, kept for its negative results | — |
| `ssn:paper/focused/main.tex` "Making the Intraoperative Count Exact: Vertebral Level Confirmation from Overlapping C-arm Exposures, With No Learned Component in the Count" | superseded (f61cd72, 2026-09-22); every number transcribed from the evidence briefs `ssn:docs/COUNTING_EVIDENCE.md`, `WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `SWEEP_PROTOCOL.md`, `SIMULATION_FIDELITY.md`, `CARM_DEPLOYMENT_EVIDENCE.md`; its Figure 6 cartoon (TikZ lines 876-941) is the model for SchwingNet's numbered panorama | describes the overlapping-exposure sweep, which is in no filing: keep private; the only "latency unmeasured" sentences (`MODEL_CARD.md` §6) |
| `ssn:paper/rsnai/main_v2.tex` "Navigation from the C-arm alone: naming the vertebral level on any fluoroscope with a physics-parameterised synthetic corpus" + `claims.tex` | superseded the same evening by SchwingNet (c508f5b); 54 / 54 claims verified on the grid (job 40414708); C7 / C8 left as `\todo` | title page says Department of Neurosurgery (wrong); `context/rsnai-paper-endpoint.md` still calls it "THE CULMINATION" (C2) |
| `ssn:docs/RSNAI_PLAN.md` | the A-E checklist for main_v2 (last status 2026-09-22 15:00) | most boxes never ticked |
| `ssn:docs/research_rsnai_*.json`, `BIB_RESOLVE_2026-09-22.json`, `BIB_AUDIT_2026-09-22*` | verified introduction claims; bibliography resolution (49 entries, workflow wf_387e3e52-e7b) | — |

---

## 5. "QI": what exists under that name

A search of file names to depth 6 under the Desktop and of `ssn:docs/`, `sn:`, `ssn:tools/`, `ssn:paper/` found four things
(`working_notes/topic4_manuscripts.md` §5):

1. **The QI manuscript** `ssn:paper/qi_universal_protocol/main.tex` (+ `main.pdf`, 9 pages, built 2026-09-22; `build.sh`):
   "The Universal Protocol with a level in it: site marking and time-out for spine surgery assisted by a fluoroscopic level
   map---evidence, and a quality-improvement protocol". Target: The Joint Commission Journal on Quality and Patient Safety
   (SQUIRE 2.0 for the protocol). About 2,400 words, 2 tables, caterpillar and timing figures (commit 515c6da). Every
   figure traces to `ssn:docs/WRONG_LEVEL_COST_EVIDENCE.md` and `WRONG_SITE_BURDEN_EVIDENCE.md` (header comment). Its
   proposal rests on the sweep walk ("94.5 % of 950 walks", "92.2 % of 7,405 walks", from `tools/fiducial_walk.py` ->
   `~/model_night/fiducial/`; `ssn:docs/CONTINUANCE_2026-09-19.md`). Citing sentences corrected 2026-09-22 (d4b895e);
   "~15 minutes of fluoroscopic counting" (mongardi2021 + upadhyaya2012) is unverified. Power: "powered to estimate, not
   to detect a change in wrong-level events, which at 0.12 % would need tens of thousands of cases" (L229-231). State:
   draft, not submitted (no record). **Cautions**: the affiliation line reads "Department of Neurosurgery" (wrong); the
   protocol describes the sweep and a persistent digital fiducial, which are invention aspects
   (`ssn:docs/INVENTION_DISCLOSURE.md` §3 E): private until filing.
2. **The QI deep-research run** wf_93111768-3ea (106 agents): the only human exact-level naming number on intraoperative
   images is Manbachi 2018 (69.6 % -> 97.6 % with LevelCheck); written to `ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`
   (`context/feasibility-claims-measured.md`).
3. **"QI tools" in SchwingNet** = the quality-control and integrity tools gathered in the supplement section "Data
   integrity and quality controls" (`ssn:docs/RESUME_2026-09-22_PM.md` line 869; `sn:REVISION_LOG3.md` line 402).
4. **`<laptop:Desktop>/QI101.pdf`, `<laptop:Desktop>/QI102.pdf`**: one-page course-completion certificates ("QI 101: Introduction to
   Health Care Improvement", 10/15/2025; "QI 102: How to Improve with the Model for Improvement", 10/16/2025). Not
   research.

Redo plan for the QI paper: hold until the provisional is filed; then correct the affiliation, verify the "~15 minutes"
citation, and decide whether the sweep section can be published.

---

## 6. CTSpinoPelvic1K dataset article (Medical Physics, Dataset and Software Article)

| item | record |
|---|---|
| title | "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral transitional anatomy" (`ctsp:paper/mpda/cover_letter.md`) |
| authors | 14: Schwing; Schehr; [10 student co-author names withheld; `ctsp:paper/mpda/title_page.tex` at 7ddfe38]; Ismoilov; Alnabahneh (`ctsp:paper/mpda/title_page.tex`); sign-off sheet `<laptop:Desktop>/CTSpinoPelvic1K_coauthor_signoff.xlsx` |
| data | 802 records (ACRIN 6664); Zenodo concept 10.5281/zenodo.22139642; v11 = 10.5281/zenodo.22797014 ("published 18 Sep 2026"); build archive 10.5281/zenodo.22647933; CC BY-NC-SA 4.0 |
| preprint | arXiv 2609.22760 (`cover_letter.md`); form, categories and licence `paper/mpda/ARXIV_SUBMISSION.md`; upload built by `make_arxiv.sh` |
| history | MLHC 2026 version rejected; retargeted to Medical Physics 2026-07-24 (`context/publication-roadmap.md`); plan `paper/mpda/PLAN.md` (DOI before submission; no hypothesis testing; 10 published pages); returned unreviewed 2026-09-21 for carrying an abstract (commit 20ff26a); returned again for the supporting-information format; packet rebuilt 2026-09-25 10:34 (`ctsp:dist/submission/`) with the Castellvi wording fix (31e1b16, 70de829) and the F30 funding line (f14c9b9) |
| current packet | `ctsp:dist/submission/`: `Main_Document_CTSpinoPelvic1K.{tex,pdf}` (25 review pages), `Supporting_Information_CTSpinoPelvic1K.pdf` (3), `Title_Page_CTSpinoPelvic1K.pdf`, `Figure_1..3.pdf`, `Abstract.txt`, `Cover_Letter.md`; built by `paper/mpda/make_submission.py` (run from Windows) |
| page check | `bash paper/mpda/build.sh --reprint` -> 10 pages (rebuilt 2026-10-08 09:41) |
| floats | main: Table 1 prior art, Figure 1 pipeline, rib QC table, Figure four phenotypes, spinopelvic table, Figure morphometry by level (L5 withheld); supporting: Figures S1 hardware, S2 validation, S3 field of view; Tables pseudolabeller Dice, completeness, identifier census (`RECIPES.md` §9) |
| where numbers come from | `paper/mpda/REPRODUCE.md`; text-vs-CSV check `audit_ms.py`; every figure / table regenerates `audit_artifacts.py`; PDF read-back `audit_pdfs.py`; citations read against sources `paper/mpda/CITATION_CHECK.md` (9 Sep 2026) |
| caption check | by a rough counter (`scratchpad/handoff/t4/caption_words.py`), three main-document table captions exceed 60 words (rib QC 66, spinopelvic 71, level atlas 62); the project's counter may differ by a few words |
| student review | Ashley Schehr's pass merged 2026-09-18 (7922c0c); comments `paper/mpda/CTSP_OTHERSTUDENTS.docx`; responses `paper/mpda/STUDENT_REVIEW_RESPONSE.md` |
| AI-text scans | `<laptop:Desktop>/MDPA_AI.pdf` (GPTZero 60 % on the 12 Sep copy), `ctsp:GPTZero AI Scan - CTSpinoPelvic1K_single_column.docx.pdf` (51 %); the manuscript discloses language-model assistance (`main.tex` line 652) |
| older copies | `<laptop:Desktop>/CTSpinoPelvic1K_coauthor_draft.{docx,pdf}`, `_overleaf(.zip)`, `_MDPA_overleaf(.zip)`, `_submission(.zip)`, `_arxiv.tar.gz`, `_arxiv_preview.pdf` (6-12 Sep, v10 era); `<laptop:Desktop>/MDPA.pdf` (12 Sep), `ctsp:MDPA.pdf` (16 Sep), `<laptop:Desktop>/MDPA_FINAL.pdf` (21 Sep), `<laptop:Desktop>/arxiv_prev.pdf`, `ctsp:arxiv_final_draft_9_19_2026.pdf` (19 Sep) |

Must be redone (each from the file named): confirm the submission state with Greg; title page calls the corresponding
author "a faculty surgeon" (`title_page.tex` line 85) while the TTO and HPR records say resident (C6); "no relevant
conflicts" while an invention disclosure in the same field was filed 2026-09-25 (C7); the contribution statement says each
Castellvi reader read "every case independently", while the NeurIPS audit found the reads complete by 4 Sep, reader 2's
grades for five cases are 23 Aug second reads, and the readers had seen the May grading (`ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`
S6, change 19) (C12); the cover letter says the NeurIPS paper "shares no text, figure or table" while NeurIPS appendices G
and H are captioned "Adapted from" the dataset article (C10); mirror-image CTs (at least tokens 75 and 480) are disclosed in
NeurIPS but not in the MPDA or `zenodo/KNOWN_ISSUES.md`; `KNOWN_ISSUES.md` (last changed 2026-09-07, v10) lacks the
mirrored CTs, the 0533 truncation and the misplaced L5 label in COLONOG_299; the Zenodo v11 README still carries the
August Castellvi paragraph; `REPRODUCE.md` §0 still says "v10 ... S1=29" (C18); the Figure 3 caption still says
"digitised from Figure 4A" though Panjabi Table 3 was obtained (`RESULTS_CATALOG.md` F.38); `main.tex` Acknowledgements
says "This work received no funding" while the title page names NIH F30GM147909 (topic 6 C13); cite the NeurIPS paper with
key `neurips2026lstv`. Whether to post an arXiv replacement (v1 predates the ten-page cut, the Castellvi five-of-six and the
funding line) is not decided anywhere. Then rebuild with `build.sh --reprint` reading the whole output, regenerate the
packet from Windows, and run the three audits; a deposit with changed files is a new integer Zenodo version.

---

## 7. NeurIPS 2026 Evaluations and Datasets Track, submission 3474 (accepted)

| item | record |
|---|---|
| title | submitted as "Not All Spines Are Created Equal: How TotalSegmentator Fails on Lumbosacral Transitional Vertebrae" (`<laptop:Desktop>/3474_Not_All_Spines_Are_Create.pdf` = `ctsp:3474_...pdf` = `CAMERA_READY_NEURIPS/NEURIPS_CURRENT_PDF.pdf`); camera-ready "... How CT Segmenters Fail ..." (`src/neurips_2026.tex` line 35) |
| decision | accept, poster, OpenReview 24 Sep 2026, id D8yRWDAGQF; authors Gregory John Schwing, Patrick Schwing, Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert (`CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt`) |
| change log | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`: three 2026-09-27 passes supersede the 25 Sep sections |
| build | `latexmk -pdf -interaction=nonstopmode neurips_2026.tex` in WSL (TeX Live; `cm-super` installed 2026-09-26; first rebuild needs `latexmk -g`); `src/neurips_2026.pdf` 31 pages, 134 `[pending]` slots (2026-09-27 02:15); content pages 1-10. **Why 21 and 31 pages both exist**: the committed copy (38b0cb9, 2026-09-25) is 21 pages with technical appendices A-D; the uncommitted 2026-09-27 working copy is 31 pages because its edits `\input{appendix/appendix}` from the untracked `src/appendix/` (eleven files, among them `spineps.tex`, `v11_results.tex` and `release_split.tex`) whose `[pending]` slots wait on the cancelled jobs below (page counts read from both PDFs with PyMuPDF on 2026-10-08; `git status`) |
| the pending slots | Appendix I (SPINEPS under the protocol: jobs 40481323 -> 40481314 -> 40481315; use only with 0 ground-truth-gate mismatches) and Appendix J (v11 summaries: 40480728/31/32, 40480730/33); TotalSegmentator total_v3 (40481824-26) |
| **those jobs were cancelled** | 2026-09-27 15:50 with everything outside `ruleclass/` (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`; nv11_ts had 6 of 16 shards done and resumes per shard) |
| open for Greg | "What remains for Greg" items 3-26: upload the camera-ready and the Croissant file (v11 has no `croissant.json`, only v6); do not upload while any `[pending]` remains (fill or cut Appendices I-J); run or cut total_v3; headline defects A (TS sacrum 0.817 counts its S1 class as a miss) and B (junction comparisons subtract two window definitions) are still in the main text; publish the April release manifests and the evaluated 174-record split, or keep checklist item 5 at "No"; licence per host differs; the MPDA overlap sentence; the mirror images; competing interests vs the invention disclosure; readers' PGY level (not recorded); the Castellvi grades changed after review (Greg's judgement whether to tell the AC); post the OpenReview note |
| evidence | per-case `<laptop:Desktop>/NeurIPS/bm/benchmark_per_case.csv`, `bm/benchmark_per_case_record_level.csv`, `ens/per_case_dice.csv`; Castellvi `ctsp:docs/castellvi_consensus.csv`, `castellvi_readers_2026-09-04.csv`; recomputation scripts (`crverify.py`, `crverify2.py`, `crverify3.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py`) **only** in `<laptop:Temp scratchpad>` (Temp can be swept: copy them into the repository) |
| referenced but not found | `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` (named in the change log) are in no Temp scratchpad |
| commit state | the 2026-09-27 edits are uncommitted ("Nothing was pushed, committed, posted or published") |
| captions | by the rough counter two table captions exceed 60 words (per-class DSC 64, five-fold checkpoint 66); the log's `capcount.py` reported all at most 60 |
| released code | `OpenSpineConsortium/spinopelvic-seg` at c105981 (local `<laptop:Desktop>/NextPaper/spinopelvic-seg`, remote `origin` still `anonymous-neurips-ED/spinopelvic-seg`, remote `osc` the OSC repository); the camera-ready cites it as the public code repository (commit 70de829: "cites the public code repository (the development repository is private)"; "All are accessible"); its live visibility was not re-checked (no network); still carries an anonymised citation and author (item 14) |
| deadline | not recorded on disk |

Redo plan: commit the current state; rescue the scratch scripts; decide with Greg whether to resubmit the cancelled chains
(the grid record says how to resume each) or cut Appendices I-J and the four sentences that point at total_v3 (their exact
wording was in the missing `INTEGRATE.md` §5, so it must be rewritten); fix defects A and B; settle items 16-24; rebuild;
check fonts and pages; upload. This has a deadline and goes first among the CT-side items.

---

## 8. MLHC 2026 (rejected)

`<laptop:Desktop>/MLHC_2026_Research_Track_Paper.pdf` (20 pages, 8 Jun 2026; text `ctsp:_paper_text.txt`): "CTSpinoPelvic1K: A Unified
CT Benchmark for Lumbosacral Transitional Vertebra Segmentation", 1,137 volumes, 804 patients, 10-class labelmap. Source
`ctsp:mlhc/full-paper-template.tex`; rebuttals `ctsp:_rebuttal_r2.txt`, `_rebuttal_r3.txt`, `_rebuttal_f65r.txt`. Outcome
rejected (`context/publication-roadmap.md`, 2026-07-24); `ctsp:docs/ROADMAP.md` still says "in review, score 2.75/4" (stale,
C8). Where the decision letter is: not recorded. Nothing to redo; never cite it as under review.

## 9. Other CT-side manuscripts in `<laptop:Desktop>/NextPaper/`

| file | record | state |
|---|---|---|
| `NextPaper/RadAI/main.tex` "A CT Segmentation Network Trained on Labelled Transitional Anatomy Reports the Lumbar Count with a Posterior: Comparison with Public Systems on an LSTV-Stratified Cohort" | Radiology: AI target set 2026-09-08 for the one-shot / numbered-rib work (`README.md`, `claim_checklist.md`) | 22 `\todo`; results were to come from Dataset810 (retired 2026-09-08) and Dataset813 (numbered ribs); whether Dataset813 finished or was scored is not recorded |
| `NextPaper/AR/neurips_2026.tex` + `REVISION_PLAN.md` | the September revision toward v10 and the one-shot model | FROZEN 2026-09-08 as a source only (Greg: stop drafting it) |
| `NextPaper/VerSeFusion/` (README) | "accompanies the NeurIPS 2026 Datasets & Benchmarks Track submission" | submission not recorded; the CV lists no VerSeFusion paper |

## 10. BIBM and XRSpinoPelvic1K

P1 XRSpinoPelvic1K (limited-field level localisation on DRR / XR) to BIBM, deadline ~5 Jul 2026, collapsed on 2026-06-28
into one BIBM wrap-up of everything built on the dataset (ostk spinopelvic parameters, CT-to-radiograph bridge with
label-carrying DRRs, NiiVue viewer and the `metrics.json` contract, post-op synthesis) (`context/publication-roadmap.md`;
`ctsp:docs/ROADMAP.md`). Draft `<laptop:Desktop>/NextPaper/bibm-spinopelvic/main.tex` (IEEEtran; README lists the `\TODO`s: Table 1
from `python -m ostk all` + `tools/cohort_stats.py`, two figures, the 2-D / 3-D tolerance, citations). `ctsp:BIBM/` holds
only the IEEE template. `<laptop:Desktop>/XRaySpinoPelvic1K/` (README, `docs/RESULTS.md`, `docs/reader_study_protocol.md`) was made
PRIVATE 2026-09-26 because it held `localize.py` and a Cerner `.ica` credential file. Submission of either: not recorded
(the CV of 2026-09-27 lists no BIBM paper). A SPIE MI 2027 abstract (5 Aug 2026) was planned; not recorded. Redo: treat both
as unwritten; XR level-localisation content is SchwingNet-adjacent and private; recompute spinopelvic numbers on v11 with
`ostk.labels.labels_for(volume)` and after fixing ostk's S1 fallback (`RESULTS_CATALOG.md` G.3).

## 11. Iliac crest clinical paper

`ctsp:paper/clinical/main.tex` "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy: a
morphometric study of 802 screening CT examinations"; target Spine Surgery and Related Research; "complete draft with real
numbers. Needs the introduction expanded and someone to argue with the discussion" (header); first author "[First
author]"; last commit 2026-08-22 (0ecbb82). It exists because the MPDA may not test hypotheses. **Its numbers predate the v6
hip-laterality corrections and v11; the measure touches the pelvis and the lumbosacral junction, so recompute from v11
before use** (`ctsp:CLAUDE.md`).

## 12. OpenSpineConsortium medical-education study

| item | record |
|---|---|
| published | Schehr A, Kim J, Schwing G. "OpenSpineConsortium: An Open-Source Framework for Medical Student Engagement in Computational Spine Imaging Research." Cureus 2026;18(7):e112661, doi 10.7759/cureus.112661, published 14 Jul 2026 (`<laptop:Desktop>/cureus.pdf`; PMID 42598196 per the ERAS CV) |
| JEEHP version | `ctsp:OSC MedEd Manuscript - JEEHP.docx` (14-15 Jun 2026): same 16 respondents and the same six-domain table |
| CNS 2026 poster | CNS 66639 "Beyond the Cadaver Lab ..." selected as Printed Poster; one-slide poster `ctsp:Med_Ed_CNS.pptx` and `ctsp:Med_Ed_CNS_visual_abstract.pptx` (both last edited by Ashley Schehr, 2026-09-01); visual abstract source `ctsp:poster/make_visual_abstract.py` |
| board | `ctsp:Student_Projects/BOARD.md` card `meded`: lead Ashley Schehr, co-lead Greg; open task "journal submission"; survey protocol `ctsp:docs/survey_protocol.md`; the raw survey CSV was never committed (it holds names) |
| caution | submitting the JEEHP version would publish the same survey data twice (C9): drop it, or make it a follow-up with new data |

## 13. CNS 2026 (Washington DC, 31 Oct-4 Nov 2026)

### 13.1 The twelve OSC abstracts (`<laptop:Desktop>/openspineconsortium.github.io/contributions/manifest.json`, 2026-05-19)

| CNS id | title (short) | status | students |
|---|---|---|---|
| 66629 | Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model for Preoperative Detection of Lumbar and Thoracic End Anomalies | Mini Oral Poster (Greg; MP4SP1 Mon 2 Nov 5:21-6:00 PM) | Greg sole author |
| 66639 | Beyond the Cadaver Lab (OSC med-ed) | Printed Poster | [1 student name withheld] |
| 68300 | Automated CT-Derived Cobb Angle Measurement | Digital Only | [1 student name withheld], Schehr |
| 67525 | Opportunistic Screening for Vertebral Degeneration Using Vertebral Hounsfield Units | Digital Only | [student authors withheld] |
| 68579 | Sagittal Lumbar Lordosis via a TRALL Angle Pipeline | Digital Only | [3 student names withheld] |
| 69734 | Automated Lumbar Intervertebral Disc Heights | Digital Only | [3 student names withheld] |
| 69093 | Automated CT-Based Pelvic Incidence and Sacral Slope | Digital Only | [2 student names withheld] |
| 68733 | Automated Vertebral Wedging Index | Digital Only | [1 student name withheld] |
| 68460 | Lordosis Distribution Index | "Submitted" (not updated) | Kim, Schehr |
| 68858 | Lumbar Spinal Stenosis Screening, Normative Torg Ratio L1-L5 | Digital Only | [student author withheld] |
| 68779 | Lumbar Spondylolisthesis and Meyerding Classification | "Submitted" (not updated) | Fahmy, Saad, Schehr |
| 67829 | Automated 3D Vertebral Centroid Trajectory | Digital Only | [1 student name withheld] |
Three more topics are "In preparation" (vertebral spacing, SVA, TPA); topic list `<laptop:Desktop>/NextPaper/CNS 2026 ABSTRACT
PROJECTS.csv`. The submitted abstract texts are not on disk. **Before the posters are shown**: the PI / SS abstract (69093)
and the measurement abstracts were computed by May 2026; the spinopelvic-estimator defects and the canal / end-plate
defects were found in August-September; whether the May numbers predate the fixes is not recorded; re-check each against
v11 and the fixed estimators. The talk title promises a single-shot model; no evaluated single-shot model is recorded on
disk (C17).

### 13.2 Greg's spine deck for 66629

| file | what | disclosure status |
|---|---|---|
| `<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | **current disclosure-safe deck**, 17 slides, CT side only (generator `ctsp:paper/cns2026/make_cns_deck_v12_public.py` + `prep_v16_public_figs.py`); every number asserted against the committed NeurIPS camera-ready; adds the MPDA pipeline, hardware figure and the spinopelvic table (PI 52.1 vs Veilleux 52.1 / Hasegawa 53.4; SS 36.6; PT 15.5) | safe |
| `<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | 15-slide predecessor | safe |
| `<laptop:Desktop>/CNS2026_Schwing_SchwingNet_CNStemplate.pptx` (= `_v10`), `_v9.pptx` | 21-slide C-arm decks on the CNS template | **disclose Part B and the sweep; never show publicly** |
| `<laptop:Desktop>/CNS2026_Schwing_SchwingNet.pptx` (v3), `CNS2026_Schwing_Spine_v2.pptx` | earlier arcs | disclose Part B results |
| `<laptop:Desktop>/CNS2026_Schwing_LSTV.pptx` | 7 Sep draft "Naming a Lumbar Level Without Counting From C2" | draft, not presented |
| generators `ctsp:paper/cns2026/make_cns_deck*.py`, `prep_*`, `figs*` | not tracked (45df97d; `.git/info/exclude`); must never be pushed | — |

Deck rules (`context/cns-deck-v2-2026-09-25.md`): CNS template traps (titles about 60 characters; zero-height text boxes
make PowerPoint refuse the file); ACCME rules (no disclosure slide, study design and dates on every data slide, generic
names, no ineligible-company logo, HIPAA statement); render with PowerPoint COM (no LibreOffice on this machine) and look at
every slide; no two consecutive results slides in the same visual form; the NeurIPS track is "Evaluations and Datasets".
Whether the slides were submitted to the meeting, and by what deadline, is not recorded.

## 14. AACA Tech Fair (presented)

`<laptop:Desktop>/TechFair_LSTV_Schwing.pptx` (15 slides; copies in `ctsp:` and `NextPaper/`): "Harnessing Algorithmic Disagreement
for Automated Lumbosacral Transitional Vertebrae Detection", 43rd AACA meeting, Mayo Clinic, 13 Jun 2026; an earlier
pipeline built from third-party segmenters; listed in the TTO package as disclosing neither Part A nor Part B. The title
slide says "Department of Neurosurgery" (C5). Nothing to redo.

## 15. Invention disclosure, patent package and disclosure control (private)

| document | what | state |
|---|---|---|
| `ssn:docs/INVENTION_DISCLOSURE.md` | engineering disclosure: five aspects (A closed-loop acquisition control, B fewer exposures, C supernumerary segment without a rare class, D no imaging leaves the room, E persistent digital marker), claim scope, §101 strategy, freedom to operate, what a provisional must contain | written 2026-09-18 |
| `ssn:docs/DISCLOSURE_MEMO.md` | counsel-only memo on publication timing and prior public availability | 2026-09-18 |
| `ssn:docs/PATENT_PACKAGE.md` | superseded; records three corrections | — |
| `ssn:docs/provisional/` (`SPECIFICATION.md`, `CLAIMS.md`, `COVER_SHEET.md`, `FILING_CHECKLIST.md`, `README.md`) | provisional package; FIG. 1-13 not drawn; first item "export the GitHub audit log" | not filed (no record) |
| `ssn:docs/research_patent_2026-09-18.json`, `research_registration_free_2026-09-18.json`, `disclosure_audit.json`, `disclosure_forensics.json`, `disclosure_evidence/` | prior-art research and the public-surface audit (`tools/disclosure_audit.py`: "Run it before any submission, talk or release") | 2026-09-18 |
| `<laptop:Desktop>/private_ip/TTO_package_2026-09-25/` | 00 README for TTO; 01 WSU invention disclosure form (docx, pdf, signed pdf); 02 the confidential Part B manuscript (+ rev2-rev5); 03 NeurIPS camera-ready; 04 MPDA; 05 AACA slides; 06 disclosure timeline; 07 cover email draft; `SCRUB_PLAN.md`; `followup/` CNS decks v2-v10 | sent to Greg 2026-09-25; the TTO asked for the inventor signature on page 8 and Chair / Dean signatures; the MOU left unsigned pending clarification (`ssn:docs/RESUME_2026-09-22_PM.md` lines 347, 353) |
| disclosure title | "(A) a segmenter-agnostic classifier that flags transitional vertebrae on preoperative CT, and (B) a neural network that names vertebral levels from a single intraoperative C-arm exposure without registration to a preoperative scan"; sole inventor; NIH F30GM147909 (ended 31 May 2026) | `00_README_for_TTO.md` |
| `<laptop:Desktop>/private_ip/github_purge_requests/` | drafts and SHA lists for GitHub Support purges (orphaned `proposals/**`, 171 commits; 5 detector ONNX files on the OSC site, 106 SHAs) | **Greg must file**; until then those SHAs return HTTP 200 |
| evidence bundles | `$RS/private_ip/git_bundles_2026-09-26/` (grid) | done 2026-09-26 |

Part A has no manuscript; its plan is `ssn:docs/CT_LSTV_CLASSIFIER_PLAN.md` and the pre-registration draft
`ssn:docs/ruleclass/PREREG_rules.md`. Already public: the CNS abstracts, AACA, NeurIPS, Zenodo / arXiv; Part A's name-free
classifier and Part B are undisclosed (`06_disclosure_timeline.md`).

## 16. Data requests (all drafted, none sent)

| request | file | status |
|---|---|---|
| 14 fluoroscopy cine sources (Bournemouth QF, Maastricht, Bern, Pittsburgh swallow, Seattle Science Foundation, Mayfield, DMX, Radiopaedia, Procedure Guide, Konica Minolta, Jefferson, MTFI, Faubel, DARADIA) | `ssn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` (checklist, verified addresses, two UNVERIFIED) + Outlook drafts `ssn:docs/fluoro_requests_eml/NN_*.eml` (11 files); sources `FLUORO_VIDEO_SOURCES_2026-09-26.md`, `FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | `requested_not_sent` (`ssn:data_platform/DATA_MANIFEST.md` entry `fluoro_cine_requests_2026_09_26`) |
| SX-Stitch intraoperative C-arm series (1,032 frames, SUSTech / PUMCH) | `ssn:docs/data_requests/SX-Stitch_request.md` | `requested_not_sent` |
| Balgrist ex-vivo lumbar CT + C-arm (Jecklin 2024) | `ssn:docs/outreach/balgrist_data_request_2026-09-21.md` | `requested_not_sent`; its first sentence still reads "I am [a neurosurgery resident; confirm title]" |
| VinDr-SpineXR HPR determination | `ctsp:IRB_VinDr_2026-09-25/` (gitignored), draft `ssn:docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` | sent to Greg 2026-09-25 for IRBQuestions@wayne.edu; number not recorded |

The ready-to-send file's "Read once before sending" list binds: the commercial-scope sentence, the IRB question first,
delete "we would not train on it" if fine-tuning is possible, co-authorship offers, the YouTube-copies sentence,
Radiopaedia only by application. Already obtained items: `$RS/data/external/fluoro_video/` (grid).

## 17. Plans and external reports

| file | what | standing |
|---|---|---|
| `ssn:docs/FLAGSHIP_PLAN.md` | "one corpus, one super model, one claim": gates G0-G7 with evidence files, corpus roles, the 50 / 10 / 40 transitional split | written 2026-09-23; G6 moved to paper 2 on 09-24 |
| `ssn:docs/RSNAI_PLAN.md` | checklist for main_v2 | stopped 2026-09-22 |
| `ssn:docs/FEASIBILITY_REPRODUCE.md` | one-job reproduction of the feasibility manuscript | feeds §4 only |
| `ssn:docs/GUIDED_ACQUISITION.md`, `SWEEP_PROTOCOL.md`, `CARM_DEPLOYMENT_EVIDENCE.md` | the sweep and guided-acquisition loop | private (invention) |
| `ssn:docs/WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `COUNTING_EVIDENCE.md` | adversarially verified evidence briefs (three refutation votes per claim) | reuse for any introduction; derived totals labelled derived |
| `ctsp:Feasibility_FOV.docx` | external report (17 Sep 2026) arguing isolated-stack naming is ill-posed; tested claim by claim (three of five "disproofs" overturned) | reference only (`context/feasibility-claims-measured.md`) |
| `ctsp:MULTI_XR.docx` | external report (18 Sep 2026) "Real-Time Vertebral Level Localization and Limited Field-of-View Classification via Deep Serial Fluoroscopic Mapping"; carries "[cite: n]" markers and unverified competitor claims | reference only; cited by no file; claims of the same kind were refuted in `sn:lit/CITABLE_CLAIMS.md` |
| `ctsp:C-Arm Validation Research Plan.pdf` | "Translational Roadmap for Exact Intraoperative Vertebral Counting via Overlapping C-Arm Fluoroscopy" | reference only |

## 18. Reports to funders

`ctsp:RPPR_Accomplishments.{docx,pdf}` (24 Jul 2026), `RPPR_B4_Training.*`, `RPPR_RCR_Instruction.docx`, `<laptop:Desktop>/RCR.pdf`,
and `ctsp:Sponsor Progress Report Letter 2026.{docx,pdf}` (Loren Schwiebert, 24 Jul 2026): the NIH F30 year-4 report. It
reports one Cureus paper, five accepted abstracts, NeurIPS under review, and says a single-shot CT model was "developed and
validated" (C17: no evaluated single-shot model is recorded). Already sent; nothing to redo. Older: `<laptop:Desktop>/F30_initial.pdf`
and `<laptop:Desktop>/Sponsor Progress Report Letter 2024.docx` (classified by name; not opened).

---

## 19. Desktop classification

`<laptop:Desktop>/` top level holds 288 entries (listing 2026-10-08). **Several items Greg named are not on the Desktop but in
the root of the public `CTSpinoPelvic1K-1` repository, untracked** (`git status`, 2026-10-08): `MULTI_XR.docx`,
`Feasibility_FOV.docx` (external reports, §17), `OSC MedEd Manuscript - JEEHP.docx` (manuscript, §12),
`Med_Ed_CNS.pptx` and `Med_Ed_CNS_visual_abstract.pptx` (poster deck, §12), `BIBM/` (the IEEE template only, §10),
`AR/` (one Elsevier template, `elsarticle-template-harv.tex`: a template, not a manuscript; the AR draft is
`<laptop:Desktop>/NextPaper/AR`, §9), `BUU-LSPINE_400/` (an 800-image data sample, `DATASET_USAGE.md` §2.1). A careless
`git add -A` there would publish them (`OPEN_QUESTIONS.md` F11). `MLHC_2026_Research_Track_Paper.pdf` and
`3474_Not_All_Spines_Are_Create.pdf` exist in both places. Personal and administrative files (taxes, leases, licences,
benefits, insurance, background checks, residency application, letters of recommendation, personal statements, legal,
religious and video media, installers, shortcuts) are not listed one by one. Items classified by name only, without
opening, are marked "(name)".

| item | class | note |
|---|---|---|
| `3474_Not_All_Spines_Are_Create.pdf` | submission (NeurIPS, as reviewed) | §7 |
| `MLHC_2026_Research_Track_Paper.pdf` | submission (rejected) | §8 |
| `MDPA.pdf`, `MDPA_FINAL.pdf`, `arxiv_prev.pdf`, `CTSpinoPelvic1K_coauthor_draft.{docx,pdf}`, `CTSpinoPelvic1K_arxiv_preview.pdf`, `CTSpinoPelvic1K_arxiv.tar.gz`, `CTSpinoPelvic1K_overleaf(.zip)`, `CTSpinoPelvic1K_MDPA_overleaf(.zip)`, `CTSpinoPelvic1K_submission(.zip)`, `CTSpinoPelvic1K_coauthor_signoff.xlsx` | manuscript copies and packets (MPDA, v10 era) | §6 |
| `MDPA_AI.pdf` | AI-text scan of the MPDA | §6 |
| `cureus.pdf` | published article (med-ed) | §12 |
| `CNS2026_*.pptx` (8 files) | decks | §13.2; only `_public_v12` is safe to show |
| `TechFair_LSTV_Schwing.pptx` | deck (presented) | §14 |
| `SCHWING_PRESENTATION_NSURG.pptx`, `SPINAL_AVM.pptx`, `GREG_PRES.pptx`, `Schwing_Presentations.docx` | decks / presentation list (name) | not opened; not part of the spine-imaging record as far as any file shows |
| `CNS_SNO Abstract_tnn edits.docx`, `JNS24-1395_..._Annotated.pdf`, `arrillaga-romany-...pdf` | U251 / glioma work (an abstract, a reviewed manuscript, a reference) | other project |
| `F30_initial.pdf`, `Sponsor Progress Report Letter 2024.docx`, `RCR.pdf` | grant and funder documents (F30 by name) | §18 |
| `2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf`, `IRB Not HPR Determination 4.21.26.pdf`, `hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf` | ethics determinations (2026-144, April 2026) | the dataset work cites 2026-269 (`ctsp:2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf`) |
| `spine_study_protocol.pdf` | protocol "Development of a Publicly Accessible, Deep Learning-Ready Clinical and Radiographic Dataset for Spine Surgery Outcomes" (Mar 2026) | not a manuscript |
| `wsu_patent_policy.pdf` | reference for §15 | — |
| `2505.01595v2.pdf`, `2505.14338v3.pdf`, `2602.09959v1.pdf`, `2605.10395v1.pdf`, `Panjabi_1976_JBJS_thoracic.pdf`, `STUMP_RIBS.pdf`, `venetti.pdf`, `ACQUIFER.pdf`, `ACQUIFER_2.pdf` (name), `307c4738...pdf` (name) | published papers and references | — |
| `Spine Morphometrics_ Beyond Basic Measurements.pdf` | externally generated research report | verify before citing |
| `Manuscript_Template.docx`, `OUP_General_Template_ID.pdf`, `ama.bst` | templates | — |
| `AI_Imaging_Workshop.{docx,pdf}`, `student_evaluations.xlsx`, `student_evaluations_full_table.docx` (name) | teaching (a 20 Jun workshop agenda; evaluations) | evaluations may hold names: never commit |
| `QI101.pdf`, `QI102.pdf` | course certificates | §5 |
| `Lumbosac.csv` | Castellvi grades for 39 cases (older) | data |
| `Experimental_planning.docx`, `True_PHD.docx` (name) | not opened | not recorded |
| `AshleyBridge-6.0.0-tester-package.zip`, `Ashley Bridge for testers/`, `new_repo.zip`, `new_repo/` | Beethoven tester package; an unidentified repository archive (name) | Beethoven is another project |
| `authentication-log-2026-09-27.csv` (name) | not opened | not recorded |
| `x-ray_machine_registration_form.doc` (name) | administrative | — |
| `openapi_key.txt`, `client_secret_*.json`, two `*.ica` files | **credential-like files: not read; never commit, copy or upload** | `INFRASTRUCTURE.md` §9 |

Research folders on the Desktop (one line each, from earlier sections or by name): `CTSpinoPelvic1K-1/` (working copy),
`CTSpinoPelvic1K/` (old clone), `CTSpinoPelvic1K-Syn/` (role not recorded), `CTSP1K_private/` (name; not opened),
`spinesurg-ct-nnunet/`, `SpineSurg-CT/` (name; not opened), `spinesurg-ct-annotator/` (role not recorded), `OpenSpineToolkit/`,
`openspineconsortium.github.io/`, `Gregory-Schwing-MD-PhD.github.io/` (personal site), `NextPaper/`, `NeurIPS/` (camera-ready
evidence), `XRaySpinoPelvic1K/` (private), `spine-detector/`, `lstv-detector/` (older MRI project), `private_ip/`,
`FluoroCap_reading/`, `FluoroCap_screening/` (name: FluoroCap review work), `BUUSPINE/` (data), `morphometrics/`,
`fov_check/`, `itksnap_review/`, `rib_review/`, `v2_inspect/`, `v3_inspect/`, `outlier/` (name: QC working folders),
`onboarding/` (name), `MANUSCRIPT/` (BMJ Case Reports submission with consent forms: patient material, other project),
`u251/`, `u251-xenograft-murine-RNASeq-study/`, `MBR_CoAuthor_Review_2026-09-07/` (name; likely U251), `ashley/`,
`ashley-bridge/` (Beethoven), `ERAS_2026/` (residency application; cite only its CV's publication list).

---

## 20. Contradictions between documents

| id | readings | trusted, and why |
|---|---|---|
| C1 | Zenodo: `context/hf-mirror-is-v10.md` and `context/zenodo-deposit.md` say v10 is current; `ctsp:Student_Projects/BOARD.md` says "v11 in preparation"; against: `ctsp:paper/mpda/cover_letter.md`, `title_page.tex`, `CAMERA_READY_NEURIPS/src/checklist.tex` and `06_disclosure_timeline.md` all give v11 = 10.5281/zenodo.22797014 published 18 Sep 2026 | v11 is on Zenodo (four documents give the DOI and date); the Hugging Face mirror is still v10 (checked by API 2026-09-27); not re-verified today: open https://doi.org/10.5281/zenodo.22797014 |
| C2 | `context/rsnai-paper-endpoint.md` names `paper/rsnai/main_v2.tex` "THE CULMINATION"; every later record uses `SchwingNet/main.tex` | SchwingNet |
| C3 | title: the CV says "... robust to transitional anatomy, versus registration-assisted neurosurgeons"; `front_matter.json` still mentions "robust"; `TITLE.md` and the PDFs print the short title | `TITLE.md` + PDFs |
| C4 | submission: CV "Submitted"; the TTO files, `FILING_CHECKLIST.md`, RESUME and `PACKET_README.md` say held / not submittable | the repository (not submitted as of 2026-09-27); Greg must say |
| C5 | affiliation: memory and SchwingNet `front_matter.json` General Surgery; MPDA, NeurIPS, arXiv, Cureus, JEEHP, TTO README "Department of Surgery"; QI paper, main_v2, TechFair slide "Neurosurgery"; Balgrist draft "[a neurosurgery resident; confirm title]" | never Neurosurgery (binding); "Surgery" vs "General Surgery" is Greg's choice |
| C6 | role: MPDA title page "a faculty surgeon"; TTO README and the HPR form "Resident physician" | resident; fix the MPDA title page |
| C7 | conflicts: MPDA "no relevant conflicts"; NeurIPS "No conflicts of interest"; SchwingNet `front_matter.json` "a commercial interest in a level-confirmation product under development"; the commercial stance forbids stating the goal outward | unresolved; counsel sees the COI statement before filing; Greg decides one consistent statement |
| C8 | MLHC: memory "rejected"; `ctsp:docs/ROADMAP.md` "in review, score 2.75/4" | rejected |
| C9 | med-ed: published in Cureus vs the board task "journal submission" for the JEEHP version | published; JEEHP would be duplicate |
| C10 | MPDA cover letter "shares no text, figure or table" vs NeurIPS appendices G / H "Adapted from" the article | unresolved |
| C11 | Loren Schwiebert: `BOARD.md` "senior author, dataset article"; the MPDA lists 14 authors without him; he is last author on NeurIPS | MPDA title page for the MPDA |
| C12 | Castellvi "each reading every case independently" vs reads dated by 4 Sep with prior exposure to the May sheet | the NeurIPS audit |
| C13 | SchwingNet body words 3,000 / 2,986 / 2,998 | two copies and two dates; the review copy is the one under the limit |
| C14 | `sn:README.md` / `FINAL_CHECK.md` four figures, four tables; `main.tex` five and three | `main.tex` |
| C15 | LITT deck: memory v5 current; disk has v6 (2026-09-27) | disk (other project) |
| C16 | "current" CNS deck v12_public vs the CNStemplate decks on the Desktop that disclose Part B | v12_public for anything public |
| C17 | RPPR "developed and validated a single-shot CT segmentation model" and the CNS 66629 title vs no evaluated one-shot model on disk | no evaluated single-shot model is recorded |
| C18 | `ctsp:paper/mpda/REPRODUCE.md` §0 "v10 ... S1=29" vs `ctsp:CLAUDE.md` v11, 29 retired | CLAUDE.md |

---

## 21. One order of work for whoever takes these over

1. **Ask Greg six questions** (none answerable from disk): was SchwingNet uploaded; was the MPDA's 2026-09-25 packet
   uploaded and under what number; has the TTO advised and is the provisional filed; what is the VinDr determination
   number; was BIBM 2026 submitted; is the NeurIPS camera-ready deadline past.
2. **Disclosure first.** Until the provisional is confirmed: no SchwingNet, QI, focused or main_v2 text, figure or deck
   anywhere public; only `CNS2026_Schwing_NotAllSpines_public_v12.pptx` for the talk; run `ssn:tools/disclosure_audit.py`
   before any talk or upload; Greg files the GitHub purge requests.
3. **NeurIPS camera-ready** (accepted, has a deadline): §7 redo plan.
4. **MPDA**: §6 corrections; reprint check; packet.
5. **SchwingNet paper 1**: §2.8; submission only on the TTO's word.
6. **CNS posters** (2 Nov): re-check each student abstract's numbers against v11 and the fixed estimators.
7. **Med-ed**: drop the JEEHP plan or turn it into a follow-up with new data (Ashley Schehr leads).
8. **Paper 2, the iliac-crest paper, BIBM, the Radiology: AI CT paper, the QI paper**: start only with Greg's go-ahead;
   each needs new data, human reads or a v11 recomputation first.

Every step follows the house pattern the SchwingNet folder already implements: results file -> manifest key ->
`\RESULT{}` -> strict build -> render and look (`sn:RESULTS_BUILD.md`; `ctsp:Student_Projects/RECIPE.md`).
