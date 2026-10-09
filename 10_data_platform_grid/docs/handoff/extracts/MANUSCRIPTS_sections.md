# Extract of HANDOFF/MANUSCRIPTS.md (spinesurg-ct-nnunet 097933a)

Sections 0, 1, 16, 20 and 21, per DISPOSITION rows 124-128.

The whole file is Greg-only and sits in the Greg-only project folders (`01_carm_level_detection/docs/handoff/` and the others `../_plan/PLAN.md` rule 3 names); this extract carries the sections that bear on the data platform, with their section ids. Path prefixes (`ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:`) read as the repositories of `MANIFEST_CODE.md` at the stated commits, never as a laptop path. Two researcher addresses are withheld.

---

<!-- section: 0 The rules that bind every item -->

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
| Never re-add SchwingNet level-identification text or `ctsp:paper/cns2026` to a public repository; only `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` is safe to show | `GREG_ONLY/context/schwingnet-disclosure-scrub.md`; `context/fluorocap-repo-private.md`; `context/cns-deck-v2-2026-09-25.md` |
| Affiliation is NOT Neurosurgery: "Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center" | `context/user-affiliation-general-surgery.md` (contradiction C5) |
| Ashley Schehr is a person (med-ed first author, annotation lead), never a product name | task brief; `ctsp:Student_Projects/BOARD.md` |
| Read before writing under `ssn:paper/` (a `main.tex` was overwritten once and restored from git) | `ssn:docs/RSNAI_PLAN.md` A3 "Incident 11:35" |
| LITT / U251 instrument statements stay conditional (other project) | memory note `litt-contralateral-two-readings` (not copied; U251) |
| Every printed number comes from a results file through a manifest key (`\RESULT{}`); the build fails on a bare numeral | `sn:RESULTS_BUILD.md` |

---


---

<!-- section: 1 Overview -->

## 1. Overview

| # | work | venue / purpose | state as recorded | main files |
|---|---|---|---|---|
| 1 | SchwingNet, paper 1: "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" | Radiology: AI, Original Research | complete in review and camera-ready copies; one placeholder (VinDr determination); supplement 13 pages > 12; Word packets stale; **held pending the WSU technology transfer office** | `sn:` |
| 2 | Paper 2: SchwingNet vs registration-assisted surgeons (LevelCheck) | not chosen | comparator frozen; blinded gate cancelled 2026-09-27; needs human reads | `sn:paper2_levelcheck/`, `sn:LEVELCHECK_MODEL.md`, `sn:LEVELCHECK_CLAIM.md` |
| 3 | Older C-arm drafts: "Naming Vertebrae Without an Anchor"; "Making the Intraoperative Count Exact"; "Navigation from the C-arm alone"; the k-devices skeleton | Radiology: AI, each in turn | superseded; sources to lift from; two disclose the undisclosed sweep | `ssn:paper/rsnai/`, `ssn:paper/focused/` |
| 4 | **QI paper**: "The Universal Protocol with a level in it ..." | The Joint Commission Journal on Quality and Patient Safety | 9-page draft, builds; not submitted; discloses invention aspects | `ssn:paper/qi_universal_protocol/` |
| 5 | CTSpinoPelvic1K dataset article ("MPDA") | Medical Physics, Dataset and Software Article | submitted; returned twice for format; third packet built 2026-09-25; upload not recorded; arXiv 2609.22760 public | `ctsp:paper/mpda/`, `ctsp:dist/submission/` |
| 6 | "Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae" | NeurIPS 2026 Evaluations and Datasets Track, submission 3474 | **accepted (poster) 24 Sep 2026**; camera-ready 31 pages with 134 `[pending]` slots; jobs cancelled; not uploaded | `ctsp:CAMERA_READY_NEURIPS/` |
| 7 | "CTSpinoPelvic1K: A Unified CT Benchmark for LSTV Segmentation" | MLHC 2026 research track | rejected | `Desktop/MLHC_2026_Research_Track_Paper.pdf` |
| 8 | CT one-shot / numbered-rib paper | Radiology: AI | draft with 22 `\todo`; results never landed | `Desktop/NextPaper/RadAI/main.tex` |
| 9 | NeurIPS revision draft (AR) and VerSeFusion | NeurIPS D&B | AR frozen 2026-09-08 as a source; VerSeFusion submission not recorded | `Desktop/NextPaper/AR/`, `NextPaper/VerSeFusion/` |
| 10 | BIBM wrap-up "From Segmented CT to Spinopelvic Measurement" and XRSpinoPelvic1K | IEEE BIBM 2026 (deadline 5 Jul 2026) | draft with `\TODO`s; submission not recorded; XRSpinoPelvic1K private since 2026-09-26 | `Desktop/NextPaper/bibm-spinopelvic/`, `Desktop/XRaySpinoPelvic1K/`, `ctsp:BIBM/` |
| 11 | "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy" | Spine Surgery and Related Research | complete draft with numbers; first author unassigned; computed before v11 | `ctsp:paper/clinical/main.tex` |
| 12 | OpenSpineConsortium medical-education study | **published in Cureus** 14 Jul 2026 (doi 10.7759/cureus.112661); JEEHP version on disk; CNS 2026 printed poster 66639 | published; a JEEHP submission would duplicate it | `Desktop/cureus.pdf`, `ctsp:OSC MedEd Manuscript - JEEHP.docx`, `ctsp:Med_Ed_CNS*.pptx` |
| 13 | CNS 2026: 12 OSC abstracts, Greg's mini-oral 66629 and its deck | CNS Annual Meeting, Washington DC, 31 Oct-4 Nov 2026; talk MP4SP1 Mon 2 Nov 5:21 PM | accepted; disclosure-safe deck v12_public | `Desktop/CNS2026_*.pptx`, `ctsp:paper/cns2026/` (untracked by design) |
| 14 | CNS 2026 Abstract 418 (LITT) deck | CNS 2026 | other project (U251); deck v6 on disk, memory describes v5 | `Desktop/u251-xenograft-murine-RNASeq-study/SLIDES/` |
| 15 | AACA Tech Fair "Harnessing Algorithmic Disagreement for Automated LSTV Detection" | 43rd AACA meeting, Mayo Clinic, 13 Jun 2026 | presented | `Desktop/TechFair_LSTV_Schwing.pptx` |
| 16 | Invention disclosure, provisional package, disclosure memo, TTO package | WSU Office for Technology Commercialization; counsel | disclosure submitted 2026-09-25 (signed form on disk); provisional filing not recorded | `ssn:docs/INVENTION_DISCLOSURE.md`, `ssn:docs/provisional/`, `Desktop/private_ip/` |
| 17 | Fluoroscopy and C-arm data requests | 14 cine sources, SX-Stitch, Balgrist | drafted, all `requested_not_sent` | `ssn:docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `ssn:docs/fluoro_requests_eml/`, `ssn:docs/data_requests/`, `ssn:docs/outreach/` |
| 18 | Flagship / feasibility / guided-acquisition plans | internal | gate tables; superseded in part by the paper split | `ssn:docs/FLAGSHIP_PLAN.md`, `FEASIBILITY_REPRODUCE.md`, `RSNAI_PLAN.md` |
| 19 | NIH F30 year-4 progress report (RPPR) and sponsor letter | NIH | written and sent July 2026 | `ctsp:RPPR_Accomplishments.{docx,pdf}`, `ctsp:Sponsor Progress Report Letter 2026.*` |

---


---

<!-- section: 16 Data requests (all drafted, none sent) -->

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


---

<!-- section: 20 Contradictions between documents -->

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


---

<!-- section: 21 One order of work -->

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

