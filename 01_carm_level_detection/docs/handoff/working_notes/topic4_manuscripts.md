# Topic 4: every manuscript, abstract, deck, disclosure and submission

Written 2026-10-08 from files on the laptop only (no network, no grid). Every entry names the file it comes from.
Repository prefixes used below:

- `sscn/` = `spinesurg-ct-nnunet:` (private, branch `L6_Class`)
- `ctsp/` = `CTSpinoPelvic1K:` (public; remotes `origin` and `osc`)
- `Desktop/` = `laptop:Desktop`
- `memory/` = `memory:`
- `u251/` = `Desktop/u251-xenograft-murine-RNASeq-study` (another project; one line only, by the containment rule in
  `memory/u251-project-containment.md`)

**When the state below was frozen.** The last manuscript commit in `sscn` is 2026-09-27 (`git log -- SchwingNet`, commit
4e3fe93); the last in `ctsp` touching a paper is 2026-09-25 (70de829), with uncommitted NeurIPS camera-ready edits
(git status at session start: `M CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`, `src/bib/references.bib`,
`src/checklist.tex`, `src/neurips_2026.pdf`, `src/neurips_2026.tex`; untracked `src/appendix/`,
`src/figs/fig_app_construction.pdf`). No commit touched a manuscript between 2026-09-28 and 2026-10-07 in either
repository (`git log --since=2026-09-28`). One artifact moved today: `ctsp/paper/mpda/CTSpinoPelvic1K_reprint_check.pdf`
was rebuilt 2026-10-08 09:41 (file timestamp; 10 pages); who rebuilt it is not recorded.

---

## 0. The rules that bind every item below

| rule | source |
|---|---|
| Never the word that means "origin of data" in its French-derived form; write origin, lineage, where it came from | `memory/writing-preferences.md`; `ctsp/CLAUDE.md` "Standing preferences" |
| No fractional version numbers; fold into the next integer version | same two files |
| Figure captions at most 60 words (target one or two sentences, about 25 words); the argument goes in the text; measure caption-to-text gaps with pymupdf | `memory/figure-captions-terse.md`; `ctsp/CLAUDE.md` |
| Capability/matrix tables in solid black plus at most one outlined mark, never colour, cells touching | `memory/tables-black-not-colour.md` |
| Medical Physics figure style: sans-serif (Arial/Helvetica), gray grid both axes, ticks out/in, degree symbol, numbers under ten spelled out, kV not kVp, 80 or 180 mm wide, 600 dpi; NO abstract in the main document of a Dataset and Software article | `memory/journal-figure-and-style-rules.md` |
| The MPDA limit is 10 PUBLISHED pages and only `build.sh --reprint` measures it; read the whole build output | `ctsp/CLAUDE.md` |
| Slides: no sideways bar charts; donuts and lines for results; background slides reproduce the cited paper's own figure ("permission pending"); 3-4 lines of 18-20 pt; a manuscript figure goes on a slide one panel at a time | `memory/chart-preferences.md` |
| SchwingNet figures: judged as a reader would; audit-style plots go to `docs/`, not the paper; at most four components per figure | `memory/figure-preferences-schwingnet.md`; `memory/rsnai-author-instructions.md` |
| Never state the commercial goal in anything that leaves (manuscripts, repos, READMEs, IRB text, student documents, commit messages); never name the product | `memory/commercialization-stance.md`; `ctsp/COMMERCIALIZATION.md` (gitignored) |
| Never re-add SchwingNet level-identification text or `paper/cns2026` to a public repository | `memory/schwingnet-disclosure-scrub.md`; `memory/fluorocap-repo-private.md` |
| Affiliation is NOT Neurosurgery; memory says "Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center" | `memory/user-affiliation-general-surgery.md` (see contradiction C5) |
| Ashley Schehr is a person (med-ed first author, annotation lead), never a product name | task brief; `ctsp/Student_Projects/BOARD.md` "People" |
| Read before writing under `sscn/paper/` (main.tex was overwritten once and restored from git) | `memory/rsnai-paper-endpoint.md`; `sscn/docs/RSNAI_PLAN.md` A3 "Incident 11:35" |
| LITT/U251 instrument statements stay conditional | `memory/litt-contralateral-two-readings.md` |

---

## 1. Overview: every work, its venue and its state

| # | work | venue / purpose | state as recorded | main files |
|---|---|---|---|---|
| 1 | SchwingNet, paper 1: "SchwingNet: a convolutional-recurrent network for level naming in spine surgery" | Radiology: Artificial Intelligence, Original Research | complete in two copies (review, camera-ready); ONE placeholder (the VinDr determination number, HPR 2026-330 of 29 September 2026, not yet printed) blocks it; HELD from submission pending the WSU technology transfer office; supplement now 13 pages against a 12-page cap; Word packet stale | `sscn/SchwingNet/` (section 2) |
| 2 | Paper 2: SchwingNet versus registration-assisted surgeons (LevelCheck) | not chosen | moved out of paper 1 on 2026-09-24; comparator frozen; blinded gate job cancelled 2026-09-27; needs human reads of transitional test persons | `sscn/SchwingNet/paper2_levelcheck/`, `LEVELCHECK_MODEL.md`, `LEVELCHECK_CLAIM.md` (section 3) |
| 3 | Older C-arm drafts: "Naming Vertebrae Without an Anchor", "Making the Intraoperative Count Exact", "Navigation from the C-arm alone", the k-devices skeleton | Radiology: AI (each, in turn) | superseded; sources to lift from; two disclose the undisclosed sweep | `sscn/paper/rsnai/`, `sscn/paper/focused/` (section 4) |
| 4 | QI paper: "The Universal Protocol with a level in it ..." | The Joint Commission Journal on Quality and Patient Safety | 8-9 page draft, builds; not submitted; discloses the sweep and the digital fiducial | `sscn/paper/qi_universal_protocol/main.tex` (section 5) |
| 5 | CTSpinoPelvic1K dataset article ("MPDA") | Medical Physics, Dataset and Software Article | submitted; returned by the editorial office twice (abstract in main document; supporting-information format); third packet built 2026-09-25; whether it was uploaded is not recorded; arXiv 2609.22760 public | `ctsp/paper/mpda/`, `ctsp/dist/submission/` (section 6) |
| 6 | "Not All Spines Are Created Equal: How CT Segmenters Fail on Lumbosacral Transitional Vertebrae" | NeurIPS 2026 Evaluations and Datasets Track, submission 3474 | ACCEPTED (poster) 24 Sep 2026; camera-ready 31 pages with 134 `[pending]` slots; the jobs that would fill them were cancelled 2026-09-27; not uploaded | `ctsp/CAMERA_READY_NEURIPS/` (section 7) |
| 7 | "CTSpinoPelvic1K: A Unified CT Benchmark for LSTV Segmentation" | MLHC 2026 research track | rejected (memory); ancestor of item 5 | `Desktop/MLHC_2026_Research_Track_Paper.pdf` (section 8) |
| 8 | CT one-shot / numbered-rib paper | Radiology: AI | draft with 22 `\todo`; results never landed | `Desktop/NextPaper/RadAI/main.tex` (section 9) |
| 9 | NeurIPS revision draft (AR) and VerSeFusion | NeurIPS D&B | AR frozen 2026-09-08 as a source; VerSeFusion submission not recorded | `Desktop/NextPaper/AR/`, `Desktop/NextPaper/VerSeFusion/` (section 9) |
| 10 | BIBM wrap-up "From Segmented CT to Spinopelvic Measurement" and XRSpinoPelvic1K | IEEE BIBM 2026 (deadline 5 Jul 2026) | draft with `\TODO`s; submission not recorded; XRSpinoPelvic1K repository made private 2026-09-26 | `Desktop/NextPaper/bibm-spinopelvic/`, `Desktop/XRaySpinoPelvic1K/`, `ctsp/BIBM/` (section 10) |
| 11 | "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy" | Spine Surgery and Related Research | "complete draft with real numbers", first author unassigned; computed before v11 | `ctsp/paper/clinical/main.tex` (section 11) |
| 12 | OpenSpineConsortium med-ed study | Cureus (PUBLISHED 14 Jul 2026, doi 10.7759/cureus.112661); JEEHP version on disk; CNS 2026 printed poster 66639 | published; JEEHP submission would duplicate it | `Desktop/cureus.pdf`, `ctsp/OSC MedEd Manuscript - JEEHP.docx`, `ctsp/Med_Ed_CNS*.pptx` (section 12) |
| 13 | CNS 2026: 12 OSC abstracts, Greg's mini-oral 66629 and its deck | CNS Annual Meeting, Washington DC, 31 Oct-4 Nov 2026; talk MP4SP1 Mon 2 Nov 5:21 PM | accepted; disclosure-safe deck v12_public (17 slides) | `Desktop/CNS2026_*.pptx`, `ctsp/paper/cns2026/` (section 13) |
| 14 | CNS 2026 Abstract 418 (LITT) deck | CNS 2026 SSTU02 | deck v6 on disk (memory says v5 current) | `u251/SLIDES/` (section 13) |
| 15 | AACA Tech Fair "Harnessing Algorithmic Disagreement for Automated LSTV Detection" | AACA 43rd meeting, Mayo Clinic, 13 Jun 2026 | presented | `Desktop/TechFair_LSTV_Schwing.pptx` (section 14) |
| 16 | Invention disclosure, provisional package, disclosure memo, TTO package | WSU Office for Technology Commercialization; patent counsel | disclosure submitted 2026-09-25 (signed form on disk); provisional filing not recorded | `sscn/docs/INVENTION_DISCLOSURE.md`, `sscn/docs/provisional/`, `Desktop/private_ip/` (section 15) |
| 17 | Fluoroscopy and C-arm data requests | 14 cine sources, SX-Stitch, Balgrist | drafted, all `requested_not_sent` | `sscn/docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md`, `sscn/docs/fluoro_requests_eml/`, `sscn/docs/data_requests/`, `sscn/docs/outreach/` (section 16) |
| 18 | Flagship / feasibility / guided-acquisition plans | internal programs | gate tables; superseded in part by the paper split | `sscn/docs/FLAGSHIP_PLAN.md`, `sscn/docs/FEASIBILITY_REPRODUCE.md`, `sscn/docs/RSNAI_PLAN.md` (section 17) |
| 19 | NIH F30 progress report (RPPR) | NIH, year 4 | written July 2026 | `ctsp/RPPR_Accomplishments.docx/.pdf`, `ctsp/Sponsor Progress Report Letter 2026.*` (section 18) |

---

## 2. SchwingNet, paper 1 (Radiology: Artificial Intelligence)

### 2.1 What it is, and how it got here

Title (current): **SchwingNet: a convolutional-recurrent network for level naming in spine surgery**; the review copy prints
**[AuthorLastName]-Net: ...** (`sscn/SchwingNet/TITLE.md`). The title lost "versus registration-assisted neurosurgeons" on
2026-09-24 evening (comparison moved to paper 2) and "robust to transitional anatomy" at ~22:15 the same night (Greg: "If
it's not robust to transitional anatomy, then it should be removed from the title"; `TITLE.md`, `CLAIMS_LEDGER.md` §9).

Lineage of the drafts (each later one supersedes the earlier):

1. `sscn/paper/rsnai/main.tex` "Naming Vertebrae Without an Anchor: Registration-Free Level Identification on
   Limited-Field Radiographs" (2026-09-17 to 09-19; 27-page PDF of 2026-09-19); cut material in `graveyard.tex`;
   pre-restructure copy `main.tex.pre-restructure` (`memory/feasibility-claims-measured.md`).
2. `sscn/paper/focused/main.tex` "Making the Intraoperative Count Exact: Vertebral Level Confirmation from Overlapping
   C-arm Exposures, With No Learned Component in the Count" (2026-09-19 to 09-22; 43-page PDF of 2026-09-21).
3. `sscn/paper/rsnai/main_kdevices_skeleton.tex` then `sscn/paper/rsnai/main_v2.tex` "Navigation from the C-arm alone:
   naming the vertebral level on any fluoroscope with a physics-parameterised synthetic corpus" (2026-09-22; 13-page PDF;
   every number a macro from `claims.tex` <- `tools/claims_fill.py` <- `docs/RSNAI_CLAIMS.json`; checklist
   `docs/RSNAI_PLAN.md`). Note: the task brief places `main_v2.tex` under `SchwingNet/paper/rsnai/`; it is at
   `sscn/paper/rsnai/main_v2.tex`.
4. `sscn/SchwingNet/main.tex` from 2026-09-22 evening, built "ONLY from rigor-passing numbers"
   (`memory/schwingnet-manuscript.md`; `sscn/SchwingNet/README.md`). Six figures on 2026-09-23
   (`memory/six-figure-paper-plan.md`), five figures and three tables since 2026-09-24 evening
   (`memory/paper-split-2026-09-24.md`; `SchwingNet/PAPER1_SCOPE.md`).

### 2.2 Where everything is (`sscn/SchwingNet/`)

| path | what |
|---|---|
| `main.tex`, `sections/{introduction,methods,results,discussion_motivation,discussion_limits}.tex` | the manuscript in the cai4cai/RSNATemplate skeleton (`TEMPLATE_NOTES.md` records departures) |
| `supplement.tex` | Figures S1-S5, Tables S1-S4 (float map in `packet_src/build/BUILD_REPORT.md`: S1 flow `fig2_flow`, S2 corpus manifold `figS1`, S3 image formation `figS2`, S4 which source carries the detector `figS3`, S5 detection against angle `figS4`; Table S1 device terms, S2 detection per device/arm, S3 corpus by source with age/sex, S4 film N-curve ablation). The file names figS<n> are one less than the printed numbers (`NUMBERS.md` §"six-figure wrap") |
| `rsnastyle.tex`, `rsnaresults.sty`, `nejm.bbx/.cbx`, `latexmkrc` | style; `\ifcameraready` (FALSE = review copy) selects `\netname{}`, `\withheldurl{}`, `\selfcite{}` (`TITLE.md`) |
| `numbers_manifest.json` -> `tools/results_macros.py` -> `generated/{numbers.tex,numbers_audit.md,pending.json}` | the results-driven build: every result in the prose is `\RESULT{key}` pointing at `file#json-pointer`; `--check` fails on any pending key, unused key or bare numeral (`RESULTS_BUILD.md`). `generated/pending.json` (2026-09-27 17:15Z): 79 resolved, 0 pending |
| `NUMBERS.md` | every number in text, tables, figures and its source file (the older trace; section headings carry pre-2026-09-24 figure/table numbers, said in its own header) |
| `CLAIMS_LEDGER.md` | the claims map: every superlative/"first"/comparison with the published comparator, our file, and a verdict (DEFENSIBLE NOW / AFTER Gx / REWRITE); "The Discussion is built from this file and nothing else" |
| `CLAIM_CHECKLIST.md`, `claim_checklist.json` | CLAIM 2020 (42 items; 30 SATISFIED, 12 GAP on 2026-09-23/24) from the docx at `sscn/CLAIM+-+Checklist+for+AI+in+Medical+imaging.docx`; the CLAIM 2024 map the packet submits is `packet_src/claim2024/map.json` -> `packet_src/build/CLAIM_CHECKLIST_2024.md` (2026-09-27: Yes 39, No 3, NA 2; READY 35, PENDING 3, NEEDS-EDIT 6) |
| `atlas/{model,dataset}.json`, `atlas/validate_cards.py`, `atlas/VALIDATION.md` | RSNA ATLAS 2025-11 cards; last run 0 errors, 5 warnings (RadLex identifiers) |
| `figures/figure1..5.{pdf,png,tif}` + `figureN.caption.txt` + `figureN.record.json` | main figures; each record lists every drawn number with its `file#key` |
| `tables/tab_corpus.tex` (Table 1), `tab4_transitional.tex` (Table 2), `tab3_naming.tex` (Table 3); supplement `tabS1_device_terms.tex`, `tab2_detection.tex`, `tabS3_corpus.tex`, `tabS4_ablation.tex` | each main table has a `.md` twin and a `.sources.md` naming the file behind every cell; `tabS4_ablation.tex` has neither (file listing) |
| `PAPER1_SCOPE.md` | the scope rule: no G3 test transitional person is scored in paper 1 |
| `REVISION_LOG.md`, `REVISION_LOG2.md`, `REVISION_LOG3.md` | change logs; REVISION_LOG3 §1-§13 runs to 2026-09-26 |
| `REVIEW_RSNA.md`, `REVIEW2_RSNA.md`, `REVIEW_STATS.md`, `REVIEW2_STATS.md`, `DRIVE_CHECK.md`, `REFS_AUDIT.md`, `FINAL_CHECK.md` | internal adversarial reviews and checks (FINAL_CHECK is the 2026-09-22/23 state and stale) |
| `RSNA_AI_REQUIREMENTS.md` | the journal limits, verbatim (Greg pasted the live summary box 2026-09-22) |
| `lit/CITABLE_CLAIMS.md`, `lit/acquisition_space_review_2026-09-24.{pdf,txt}` | an external review's claims checked one by one (VERIFIED rows only enter the text) |
| `sections/SOURCES.md`, `sections/methods_sources.md` | which earlier draft each Introduction/Discussion paragraph was distilled from |
| `packet_src/` (`build_packet_src.py`, `front_matter.json`, `statements.md`, `cover_letter.md`, `supplement_technical.tex`, `build/`) | the front documents (full title page, cover letter, CLAIM 2024) |
| `packet/` (review) and `packet_cameraready/` | Word submission packets built by `tools/make_packet.py`, dated 2026-09-25 15:42 |
| `packet_build/` | fetched grid PDFs (`review/`, `cameraready/`, 2026-09-27 13:23) and merged PDFs by date; latest `SchwingNet_{review,cameraready}_main_and_supplement_2026-09-27.pdf` (36 pages each) |
| `results/` | rigor fixes (`RIGOR_FIXES.md`, `a1..a9.json`), contribution matrix, coverage, power, census, age/sex, eval gates, film N-curve and its ablation |
| `paper2_levelcheck/` | everything moved to paper 2 (section 3) |
| `slurm/compile.sh` | grid build (texlive/2020 module, xelatex + biber; writes `localfont.tex`; `CAMERAREADY=1` writes `cameraready.flag.tex`; flock since 05e05dc) |

### 2.3 Figures and tables, and where their numbers come from

| float | content | builder | numbers from |
|---|---|---|---|
| Figure 1 (fig:phenotypes) | transitional phenotypes: L6, T13 (VerSe verse547), sacralised L5 (Castellvi IV), four lumbar (Castellvi IIIb); rows CT / render / another patient's film | `SchwingNet/tools/figure1.py` (+ grid panels `tools/figure1_panels.py`) | `figures/figure1.record.json` |
| Figure 2 (fig:embedding) | level-encoder t-SNE on the checkpoint-selection split; L6 vs L5 silhouette; occlusion enrichment | `tools/figure2.py`, `figure2_analyse.py`; grid `tools/fig2_heldout_embed.py`, `fig2_occlusion_clean.py` | `figures/figure2.record.json`; NOT held out (stated in caption) |
| Figure 3 (fig:network) | schematic: two detectors, ResNet-18 + bidirectional GRU, count from the detected sacrum, alphabet coupling | `tools/figure3_network.py` | none (schematic) |
| Figure 4 (fig:exposure) | one C-arm exposure: detection, naming, ordinals, an L6 frame at confidence 0.74 | `tools/figure4_frame.py` | `figures/figure4.record.json`; `results/eval_gate/closure/cv_v9/cv_v9.json`, `coupling_pre/coupling.json` |
| Figure 5 (fig:power) | (a) Wilson 95 % lower bound vs transitional test persons with the 90 %/85 % targets; (b) naming vs training persons, three film corpora and the C-arm per view; (c) same-device detection vs real frames; (d) render-only detectors at matched N vs lateral angle | `tools/fig_power.py` | (a) `results/power/power.json`; (b) film N curve (`film_ncurve.json`) and `results/indomain/name_fill.json#figure5b`; (c) `results/indomain/det_fill.json`; (d) `experiment/runs/cov_surgio_b51_dr_*/unseen/recall_vs_angle.json` (all named in the comment above the Figure 5 block of `main.tex`) |
| Table 1 (tab:data) | image sources, licences, counts (4,093 CT renders, 9,108 radiographs, 4,276 real exposures per the abstract) | hand table | `tables/tab_corpus.sources.md` |
| Table 2 (tab:transitional) | transitional persons by subtype and source | hand table | `tables/tab4_transitional.sources.md` |
| Table 3 (tab:naming) | naming, counting, coupling on C-ArmLSpine | hand table | `tables/tab3_naming.sources.md` |
| S1 | flow of cases | `tools/fig2_flow.py` | figure record |
| S2-S5 | corpus manifold, image-formation parameters, which training source carries the detector, detection vs view angle | `tools/figS_supplement.py` | `figures/figS1..figS4.record.json` |
| Table S1 | per-device image-formation terms | `tools/make_supp_device_table.py` | `sscn/docs/devices/*.json` |
| Table S3 | corpus by source with age and sex | `tools/make_supp_census_tables.py --merged` | `results/age_sex_by_source.json`, `results/corpus_census.json` |
| Table S4 | film N-curve ablation (render-only vs ImageNet vs film-only) | `tools/make_supp_ablation_table.py` | the three arms' result files; reading in `results/coverage/film_ncurve/ablation/READ.md` and `ablation_read.json` (REVISION_LOG3 §13; commit 7e81dd7) |

Headline numbers as printed in the Key Points of `main.tex` (cited here only so a student can find them): never trained on the
C-arm, 595 of 617 detected lateral vertebrae (96.4 %; 92.3, 98.4) in 141 cases with cone-beam CT truth against 276 of 631
anteroposterior (43.7 %); count from the detected sacrum 979 of 1,009 (97.0 %); fine-tuned 1,079 of 1,159 lateral with three
in view (93.1 %) and 608 of 631 AP (96.4 %); coupled 991 of 1,009 (98.2 %); L6-vs-L5 silhouette 0.35 vs L5-vs-L4 0.23
(selection split); 35 error-free at-risk persons needed to certify 90 %, seven real-frame candidates exist.

### 2.4 Limits and build state

| item | count | limit (`RSNA_AI_REQUIREMENTS.md`) | source |
|---|---|---|---|
| body words | 2,998 (review copy) | 3,000 | `sscn/docs/RESUME_2026-09-22_PM.md` block "2026-09-27 13:20" |
| abstract | 249 words | 250 | `SchwingNet/packet/PACKET_README.md` |
| summary statement | 244 characters | 255 | same |
| figures | 5, at most four components each | 6 | `main.tex` |
| tables | 3 | 4 | `main.tex` |
| references | 32 (review), 33 (camera-ready, self-citations print) | 35 | PACKET_README; BUILD_REPORT |
| supplement | **13 pages** | **12 pages** | commit 05e05dc message ("supplement 13 pages"); `packet_build/review/supplement.pdf` (13 pages); cap at `RSNA_AI_REQUIREMENTS.md` line 21 |

Builds of record: grid jobs 40483839 (review) and 40483840 (camera-ready), 2026-09-27: latexmk rc 0, main 23 pages,
supplement 13 pages, zero LaTeX warnings, RESULT_PENDING 0 (commit 05e05dc). The concurrent pair 40483834/40483835 raced on
`main.aux` and was discarded. `check_limits.py` fails on exactly one thing: the `\PENDING{G0}` token for the VinDr-SpineXR
determination number and date in the Ethics paragraph (RESUME 13:20 block; the 2026-09-27 PDFs print
"[PENDING G0: VinDr determination number and date]", checked by text extraction for this note; the number is HPR 2026-330 of 29 September 2026).

There is no TeX on the Windows workstation; build on the grid (`SchwingNet/README.md` "How to build"); ship code by commit,
push, and `git pull --ff-only` on the grid checkout (`memory/resume-2026-09-24.md`), never run jobs on the login node
(`memory/no-jobs-on-login-node.md`).

### 2.5 The rigor audit, item by item

The adversarial audit of 2026-09-22 (`memory/rigor-audit-findings.md`; ranked list in `sscn/docs/RESUME_2026-09-22_PM.md`)
is answered by `SchwingNet/results/RIGOR_FIXES.md` (generated by `tools/rigor_fixes.py report` at code 6e1cf8d) and the
folder's rules (`SchwingNet/README.md` "Rules the folder was built under"):

| audit item | answer in paper 1 | still open |
|---|---|---|
| A1 detector number threshold-dependent, no interval (90.6 % at conf 0.25 vs 76.8 % sacrum at best F1) | the pre-stated cross-device threshold 0.74 is quoted (vertebra 80.5 % [74.1, 86.8], sacrum 76.8 % [64.3, 89.3]) with the full recall-against-confidence curve; 0.25 kept as "as quoted" (`RIGOR_FIXES.md` A1) | none recorded |
| A2 selective reporting (rescore_outline 1,440 cells, manifold three feature spaces) | multiplicity stated in Methods; all three manifold spaces reported (`a2.json`) | none recorded |
| A3 no paired tests | paired comparisons with the interval of the difference, Holm-adjusted (`a3.json`) | none recorded |
| A4 percentile CI at the ceiling | BCa beside the percentile interval | none recorded |
| A5 film CIs clustered by vertebra; leaked v2 bank | patient-clustered on the clean-for-film v8 bank, seed 0 | the v9-bank re-score (chain 40415667 -> 40415670) "had not landed" (`SchwingNet/README.md`); whether it did later is not recorded |
| A6 criterion C3 never evaluated per fold | evaluated as written per fold (`a6.json`) | none recorded |
| A7 selective prediction invisible; abstention untuned | abstention operating point beside every naming headline; every headline says "at full coverage"; the 99 %-at-35.7 % figure on the leaked bank is deliberately absent (`FINAL_CHECK.md` row 4) | re-run of selective prediction on a clean bank is not recorded (`memory/selective-prediction-the-honest-99.md`) |
| A8 verse_drr millimetres | prohibited; none printed | none |
| A9 C-ArmLSpine groupings | case-grouped five-fold AND acquisition-day-grouped three-fold both reported (`a9.json`, `results/carmlspine_day_groups.json`) | none recorded |

Leak-free source rule: nothing is quoted from allspine v2, v6, v7, v8-for-VerSe, anchor_drr or vindrps
(`SchwingNet/NUMBERS.md` rule paragraph; `memory/split-leak-cross-naming.md`, `memory/nhanes-double-inclusion.md`).

### 2.6 The submission packet and what blocks it

`packet_src/build/BUILD_REPORT.md` (built 2026-09-27 13:26 at 1af5828 with 28 uncommitted SchwingNet paths) lists seven
decisions only the author can make; `build_packet_src.py --strict` fails while any is open:

1. **vindr_irb**: VinDr-SpineXR is covered by WSU IRB HPR 2026-330 of 29 September 2026, the supplement to 2026-269; its films are in the C-arm fold banks behind the
   fine-tuned naming numbers. Print that number and date where the manuscript carries its token (the HPR tool was filled and sent to Greg on 2026-09-25:
   `ctsp/IRB_VinDr_2026-09-25/` and `.zip`, gitignored; draft `sscn/docs/IRB/HPR_determination_VinDr-SpineXR_draft.md`; the
   notice of 2026-09-29 stays on Greg's laptop, out of every repository), or retrain the fold models without VinDr. Greg's instruction of 2026-09-25 was to assume
   it granted and leave only the number token (comment in `main.tex` Ethics paragraph).
2. **hf_mirror_v11**: the Hugging Face mirror serves v10 labels, a cc-by-nc-4.0 card and an Apache-2.0 LICENSE against
   Zenodo's CC BY-NC-SA 4.0 (re-checked 2026-09-24). Bring it to v11 under one licence or delete the mirror sentence.
3. **release_code_weights**: `docs/FLAGSHIP_PLAN.md` says weights are released; `docs/MODEL_CARD.md` 1.4 says code private and
   weights not released; `docs/INVENTION_DISCLOSURE.md` §9 advises holding weights as a trade secret. Pick
   `statements.md` WEIGHTS_OPTION_DEPOSIT or WEIGHTS_OPTION_AGREEMENT.
4. **filing_before_submission**: file the provisional and let counsel see the conflict-of-interest statement before
   submitting (`docs/DISCLOSURE_MEMO.md` §7-8; `docs/provisional/FILING_CHECKLIST.md`: "The manuscript is held until the
   provisional is on file").
5. **title_clauses**: stale in `front_matter.json` (it still describes the title with "robust to transitional anatomy");
   `TITLE.md` already removed the clause on 2026-09-24 22:15. Close it in `front_matter.json`.
6. **subject_overlap_list**: which of NeurIPS 3474, MLHC 2026, BIBM 2026 and the CNS 2026 abstracts to name in the cover
   letter's overlap paragraph (NeurIPS is accepted, MLHC rejected per memory, BIBM unknown, CNS accepted: sections 7, 8,
   10, 13 below).
7. **claim_form**: the journal requires CLAIM 2024; the docx in the repository is CLAIM 2020. Upload
   `packet_src/build/claim_checklist_2024.docx` or paste its Location column into the journal's 2024 form.

CLAIM 2024 items not READY (same report): 9 preprocessing (NEEDS-EDIT), 13 acquisition protocol (NEEDS-EDIT), 17 versions of
TotalSegmentator and SPINEPS/VERIDAH run on the CBCTs (NEEDS-EDIT), 22 body detector's training corpus by source and split
(NEEDS-EDIT), 24 initialisation (NEEDS-EDIT), 25 training details (NEEDS-EDIT), 32 and 37 training/validation-partition
performance (PENDING G5), 43 code/weights availability (PENDING G7). Proposed text for several is in
`packet_src/supplement_technical.tex`. The report also lists 19 open `[[CONFIRM]]` markers in the cover letter and full
title page (industry support, sole submission, prior presentation, preprint, street address, telephone, ORCID, CRediT roles,
acknowledgments, the HF-mirror sentence, the weights paragraph).

Defects this note found by reading timestamps and page counts (not recorded elsewhere):

- **The supplement is 13 pages against the 12-page cap** since the ablation pass (Table S4 added 2026-09-27). REVISION_LOG3
  §8 and §11 show it was trimmed back to 12 twice before; it was not trimmed this time.
- **The Word packets are stale**: `packet/*.docx` and `packet_cameraready/*.docx` are dated 2026-09-25 15:42; the PDFs with the
  ablation were fetched 2026-09-27 13:23 and `make_packet.py` was not re-run afterwards (file timestamps). The packet README
  still lists "Tables S1-S2".
- `tables/tabS4_ablation.tex` has no `.md` twin and no `.sources.md`, which every other table has.
- `SchwingNet/README.md` and `FINAL_CHECK.md` describe the 2026-09-22/23 state (four figures, four tables, 2,984 words);
  `figures/FIGURES.md` describes the six-row set of 2026-09-23. Treat all three as history.

### 2.7 Disclosure hold

The Part B manuscript is "complete and HELD pending the office's advice" (`Desktop/private_ip/TTO_package_2026-09-25/
06_disclosure_timeline.md`, row 25 Sep; `00_README_for_TTO.md` item 02). Copies given to the TTO are
`02_CONFIDENTIAL_Part_B_manuscript_Radiology_AI.pdf` and `followup/..._rev2..rev5.pdf`. Paper 1 must not appear in any
public repository (`memory/schwingnet-disclosure-scrub.md`). Whether the TTO has advised, and whether the provisional was
filed, is not recorded.

### 2.8 What a student must do to finish paper 1, in order

1. Ask Greg whether the manuscript was uploaded (the ERAS CV says "Submitted", the repository says held; contradiction C4).
2. Get the TTO/counsel answer on Part B and the provisional; do nothing public before it (section 15).
3. Close the seven author decisions in `packet_src/front_matter.json` (above), including the VinDr determination number (HPR 2026-330, 29 September 2026).
4. Trim the supplement to 12 pages (REVISION_LOG3 §8 "supplement length" and §11 "Supplement page cap" show what was cut
   before and how), give `tabS4_ablation` its `.md` and `.sources.md`.
5. Rebuild both copies on the grid one after the other (compile.sh holds a flock), fetch to `packet_build/{review,cameraready}/`,
   run `python SchwingNet/tools/check_limits.py` (and with `CAMERAREADY=1`), `python SchwingNet/tools/results_macros.py
   --check`, `python SchwingNet/packet_src/build_packet_src.py --strict`, then `python SchwingNet/tools/make_packet.py`
   (and with `CAMERAREADY=1`). Render and look at every page (`SchwingNet/tools/render_pdf.py`).
6. Convert the remaining hand-typed table cells to `\RESULT{}` keys (board task in `ctsp/Student_Projects/BOARD.md`
   "schwingnet"; the mapping is row by row in `NUMBERS.md` and the `.sources.md` files).
7. Decide Greg's open analysis items before any new number enters (RESUME "FOR GREG", 2026-09-27 18:05): per-level supplement
   table S5 from `results/coverage/PER_LEVEL_DOMAIN_ANGLE.md`; the synthetic:real ratio sweep (real_share 0.1-0.9, 45 cells);
   seeds 1-2 above N = 25 on the film N curve.
8. Verify the journal limits in a browser (pubs.rsna.org returns 403 to scripts; `memory/rsnai-author-instructions.md`).

---

## 3. Paper 2: SchwingNet against registration-assisted surgeons (LevelCheck)

| item | record |
|---|---|
| why it exists | Greg moved it out of paper 1 on 2026-09-24 ("move the comparison to neurosurgeons / all the LevelCheck stuff into a new paper"); ordinary-only superiority over 97.6 % is unreachable (n_min 152 zero-error persons; 13 reference-ordinary COBRA persons in the open gate; automated reference PPV 0.971); the cheap transitional strata (19 persons vs 82.2 %) need human reads that do not exist (`memory/paper-split-2026-09-24.md`) |
| moved material | verbatim with file and line in `SchwingNet/paper2_levelcheck/MOVED_FROM_PAPER1.md` (8 items, from commit dd8f4a5); manifest keys `numbers_manifest_moved.json`; Table `paper2_levelcheck/tables/tab_levelcheck.{tex,md,sources.md}` |
| frozen comparator | `SchwingNet/LEVELCHECK_MODEL.md` §1-§15, frozen by ecae75f, last d0403de; do not edit (`PAPER1_SCOPE.md`). Literature reading in `SchwingNet/LEVELCHECK_CLAIM.md` (LevelCheck numbers are registration accuracy, not naming; Manbachi 2018: five surgeons 69.6 % unassisted -> 97.6 % with LevelCheck; no study stratifies by transitional anatomy) |
| pre-specification rule | the comparator was pre-specified from the literature and never tuned; Greg asked for LevelCheck to "fail enough" and that was declined (`memory/six-figure-paper-plan.md`) |
| open gate | job 40438004 released 2026-09-24 21:56Z, ran 2026-09-25 04:22-06:02Z, ordinary persons only; outputs in `paper2_levelcheck/open_gate_40438004/`. **Defect:** the reference-standard score was never written because `SchwingNet/tools/fig6_score.py` read `T1/blinded/meta_ref/` instead of `T1/open/meta_ref/`; fix the path and re-score the dumps on disk (its README) |
| blinded gate | f6eval 40438005 was held for Greg's truth decision and then **cancelled** on 2026-09-27 15:50 with every non-ruleclass job (`sscn/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`, section added by c99bf91); resume instructions are in that file's per-job section |
| what it needs | human reads of the ~90 transitional COBRA test candidates (paper-split note); the automated reference calibration (`LEVELCHECK_MODEL.md` §14); a person-disjoint transitional test set (the G3 split, `docs/FLAGSHIP_PLAN.md`) |
| ledger caution | if paper 1 ever prints an ordinary-person real-frame accuracy, paper 2's ledger must record "H6 seen" (`PAPER1_SCOPE.md` item 3) |
| title reserved | "SchwingNet: a convolutional-recurrent network for level naming in spine surgery, robust to transitional anatomy, versus registration-assisted neurosurgeons" is "the natural title of paper 2's comparison" (`TITLE.md`) |

What a student would redo: nothing until human reads exist; then fix `fig6_score.py`, re-score the open gate, resubmit the
blinded gate from its recorded script (`SchwingNet/slurm/fig6_eval.sh`), and never touch `LEVELCHECK_MODEL.md`.

---

## 4. Older C-arm drafts (sources only)

| file | state | caution |
|---|---|---|
| `sscn/paper/rsnai/main.tex` "Naming Vertebrae Without an Anchor" | superseded; built with `paper/rsnai/build.sh`; numbers from `slurm/reproduce_feasibility.sh` -> `~/model_night/repro_feasibility/LEDGER.tsv` (`docs/FEASIBILITY_REPRODUCE.md`) | uses banks later found leaky (v2, v5; `memory/feasibility-claims-measured.md` LEAK paragraph); 14 partly supported citing sentences were NOT corrected (`docs/RSNAI_PLAN.md` 12:10 entry); web copy https://claude.ai/artifact/3DFZMHt4oAnrDVHwxdZnyf (`memory/feasibility-claims-measured.md`) |
| `sscn/paper/rsnai/graveyard.tex` | material cut from the above, kept for its negative results | none |
| `sscn/paper/focused/main.tex` "Making the Intraoperative Count Exact" | superseded; every number transcribed from evidence briefs `docs/COUNTING_EVIDENCE.md`, `WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `SWEEP_PROTOCOL.md`, `SIMULATION_FIDELITY.md`, `CARM_DEPLOYMENT_EVIDENCE.md` (its header); its Figure 6 left cartoon (`fig:mechanism`, TikZ lines 876-941) is the model for SchwingNet's numbered panorama (`memory/figure-preferences-schwingnet.md`) | describes the overlapping-exposure sweep, which is in no filing (`memory/cns-deck-v2-2026-09-25.md` v11_public); keep private |
| `sscn/paper/rsnai/main_v2.tex` "Navigation from the C-arm alone" + `claims.tex` | superseded the same evening by SchwingNet; Figure 1 six-row `paper/rsnai/figures/fig1_story.pdf`; ledger `docs/RSNAI_CLAIMS.json` (54 of 54 verified on the grid, job 40414708; `docs/RSNAI_PLAN.md` 15:00 entry) | affiliation line says Department of Neurosurgery (wrong); `memory/rsnai-paper-endpoint.md` still calls it "THE CULMINATION" (contradiction C2) |
| `sscn/docs/RSNAI_PLAN.md` | the A-E checklist for main_v2; last status 2026-09-22 15:00 | most boxes never ticked; stopped when SchwingNet started |
| `sscn/docs/research_rsnai_*.json`, `BIB_RESOLVE_2026-09-22.json`, `BIB_AUDIT_2026-09-22*.{md,json}` | verified introduction claims and the bibliography resolution (49 entries, workflow wf_387e3e52-e7b) | citation traps listed in `memory/rsnai-paper-endpoint.md` (no source gives "three or four bodies" or a 9-inch field; Siminski is Mayo Clinic Rochester; Macki's costs are fiducial implantation; Furuya's 81 % is of lumbar events; Universal Protocol cites `jcnpsg2025`; upadhyaya2012 has no cost numbers) |

---

## 5. "QI": what exists under that name

A search of file names to depth 6 under the Desktop (`find -iname 'qi*'` and variants) and of `docs/`, `SchwingNet/`,
`tools/`, `paper/` for the word found four different things:

1. **The QI manuscript** `sscn/paper/qi_universal_protocol/main.tex` (+ `main.pdf`, 9 pages, built 2026-09-22; `build.sh`):
   "The Universal Protocol with a level in it: site marking and time-out for spine surgery assisted by a fluoroscopic level
   map---evidence, and a quality-improvement protocol". Target: The Joint Commission Journal on Quality and Patient Safety
   (SQUIRE 2.0 for the protocol). About 2,400 words, 2 tables, caterpillar and timing figures (commit 515c6da). Every figure
   traces to `docs/WRONG_LEVEL_COST_EVIDENCE.md` and `docs/WRONG_SITE_BURDEN_EVIDENCE.md` (header comment). Its proposal
   rests on the sweep walk ("94.5 % of 950 walks", "92.2 % of 7,405 walks"; from `tools/fiducial_walk.py` ->
   `~/model_night/fiducial/`, `docs/CONTINUANCE_2026-09-19.md`). Citing sentences were corrected on 2026-09-22 (d4b895e);
   "~15 minutes of fluoroscopic counting" (mongardi2021 + upadhyaya2012) is unverified (`docs/RSNAI_PLAN.md`). State: draft,
   not submitted (no record). **Cautions:** the affiliation line reads "Department of Neurosurgery" (wrong); the protocol
   describes the sweep and a persistent digital fiducial, which are invention aspects (`docs/INVENTION_DISCLOSURE.md` §3 E)
   and undisclosed; it must stay private until filing.
2. **The QI deep-research run** wf_93111768-3ea (106 agents): the only human exact-level naming number on intraoperative
   images is Manbachi 2018 (69.6 % -> 97.6 % with LevelCheck); written to `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`
   (`memory/feasibility-claims-measured.md`).
3. **"QI tools" in SchwingNet** = quality-control and integrity tools, gathered in the supplement section "Data integrity and
   quality controls" (`sscn/docs/RESUME_2026-09-22_PM.md` line 869; `SchwingNet/REVISION_LOG3.md` line 402).
4. **`Desktop/QI101.pdf` and `Desktop/QI102.pdf`**: one-page course-completion certificates, "QI 101: Introduction to Health
   Care Improvement" (10/15/2025) and "QI 102: How to Improve with the Model for Improvement" (10/16/2025). Not research.

---

## 6. CTSpinoPelvic1K dataset article (Medical Physics, Dataset and Software Article)

| item | record |
|---|---|
| title | "CTSpinoPelvic1K: spine, pelvis, ribs and femora in one coordinate frame, annotated for lumbosacral transitional anatomy" (`ctsp/paper/mpda/cover_letter.md`) |
| authors | 14: Schwing; Schehr; [10 student co-author names withheld; `ctsp:paper/mpda/title_page.tex` at 7ddfe38]; Ismoilov; Alnabahneh (`ctsp/paper/mpda/title_page.tex`; `ARXIV_SUBMISSION.md`); sign-off sheet `Desktop/CTSpinoPelvic1K_coauthor_signoff.xlsx` |
| data | 802 records, ACRIN 6664 screening protocol; Zenodo concept 10.5281/zenodo.22139642; version described v11 = 10.5281/zenodo.22797014 (published 18 Sep 2026); build archive 10.5281/zenodo.22647933; CC BY-NC-SA 4.0 (`cover_letter.md`; `memory/zenodo-deposit.md`) |
| preprint | arXiv 2609.22760 (`cover_letter.md`; posted per commit a98a8ac 2026-09-22; TTO timeline says 19 Sep); arXiv form, categories and licence in `paper/mpda/ARXIV_SUBMISSION.md`; upload built by `make_arxiv.sh`; enclosed in SchwingNet's packet as `overlap/arXiv_2609.22760v1_CTSpinoPelvic1K.pdf` |
| history | MLHC 2026 version rejected; retargeted to Medical Physics 2026-07-24 (`memory/publication-roadmap.md`); planning document `paper/mpda/PLAN.md` (DOI before submission; no hypothesis testing; 10 published pages); returned unreviewed 2026-09-21 for carrying an abstract (`memory/journal-figure-and-style-rules.md`; commit 20ff26a); returned again for the supporting-information format (`cover_letter.md` "This resubmission answers the editorial office's check of the supporting information"); packet rebuilt 2026-09-25 10:34 (`ctsp/dist/submission/`) with the Castellvi wording fix (31e1b16, 70de829) and the F30 funding line (f14c9b9) |
| current packet | `ctsp/dist/submission/`: `Main_Document_CTSpinoPelvic1K.{tex,pdf}` (25 review pages), `Supporting_Information_CTSpinoPelvic1K.pdf` (3 pages), `Title_Page_CTSpinoPelvic1K.pdf`, `Figure_1..3.pdf`, `Abstract.txt` (form text from `make_abstract_text.py`), `Cover_Letter.md`; built by `paper/mpda/make_submission.py` (must run from Windows; it shells out to WSL, `ctsp/CLAUDE.md`) |
| page check | `bash paper/mpda/build.sh --reprint` -> `paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` = 10 pages (rebuilt 2026-10-08 09:41); journal estimate `page_estimate.py` (formula 4.3 + words/3000 + floats/1.9 disagrees with the reprint either way, `memory/journal-figure-and-style-rules.md`) |
| floats (main) | Table 1 prior art (`tab:priorart`, black/outlined matrix), Figure 1 pipeline (`fig:pipeline`, TikZ in `main.tex`; standalone `fig_pipeline_standalone.tex`), Table rib QC (`tab:ribqc`), Figure four phenotypes (`fig:anchors`, `figures/fig_anchors.pdf`), Table spinopelvic measures (`tab:spinopelvic`), Figure morphometry by level T11-L5 (`fig:levelatlas`, `make_levelatlas_fig.py`/`levelatlas.py`; L5 row withheld after the canal/end-plate defects, `ctsp/docs/LEVEL_MORPHOMETRY.md`, commits e7c8e91, a7b94ef) |
| floats (supporting) | Figure S1 hardware (`fig_hardware.pdf`), S2 spinopelvic validation (`fig_validation.pdf`), S3 field of view (`fig_fov.pdf`, `make_fov_fig.py`); Tables pseudolabeller Dice (`tab:pseudodice`), completeness (`tab:completeness`), identifier census (`census_table.tex`, generated by `scripts/make_census_table.py` from `morphometrics/label_census_v11.csv`) (`paper/mpda/supplement_body.tex`) |
| where numbers come from | `paper/mpda/REPRODUCE.md` (measurement scripts -> `morphometrics/*.csv`; reference values `morphometrics/make_reference_table.py`; Panjabi Fig 4A digitised by `paper/mpda/tools/digitize_panjabi_fig4a.py` because page 892 is missing from every scan); text-vs-CSV check `paper/mpda/audit_ms.py`; every figure/table regenerates check `audit_artifacts.py`; PDF read-back `audit_pdfs.py`; citations read against sources `paper/mpda/CITATION_CHECK.md` (checked 9 Sep 2026) |
| spinopelvic numbers | four estimator defects found, three still open (`ctsp/docs/SPINOPELVIC_ESTIMATOR.md`); the release reports the simple estimator and says why |
| caption check | by this note's rough counter (`scratchpad/handoff/t4/caption_words.py`), three main-document table captions exceed 60 words (rib QC 66, spinopelvic 71, level atlas 62); the counter may differ from the project's by a few words |
| student review | Ashley Schehr's pass merged 2026-09-18 (7922c0c; `paper/mpda/CTSpinoPelvic1K_schehr revisions + sources notes.docx`); student comments `paper/mpda/CTSP_OTHERSTUDENTS.docx`; responses `paper/mpda/STUDENT_REVIEW_RESPONSE.md` |
| AI-text scans on disk | `Desktop/MDPA_AI.pdf` (GPTZero 60 % on the 12 Sep review copy), `ctsp/GPTZero AI Scan - CTSpinoPelvic1K_single_column.docx.pdf` (51 %); the manuscript discloses language-model assistance (`paper/mpda/main.tex` line 652) |
| older copies on the Desktop | `Desktop/CTSpinoPelvic1K_coauthor_draft.{docx,pdf}`, `_overleaf(.zip)`, `_MDPA_overleaf(.zip)`, `_submission(.zip)`, `_arxiv.tar.gz`, `_arxiv_preview.pdf` (all 6-12 Sep, v10 era); `Desktop/MDPA.pdf` (12 Sep), `ctsp/MDPA.pdf` (16 Sep), `Desktop/MDPA_FINAL.pdf` (21 Sep), `Desktop/arxiv_prev.pdf` and `ctsp/arxiv_final_draft_9_19_2026.pdf` (19 Sep) |

Open items that touch this article (each from the file named):

- Whether the 2026-09-25 packet was uploaded, the manuscript number and the editorial status: not recorded.
- Title page says "The corresponding author, a faculty surgeon" (`title_page.tex` line 85); other records say resident
  physician (contradiction C6). Title page conflicts: "no relevant conflicts" while an invention disclosure in the same field
  was filed 2026-09-25 (C7).
- The contribution statement says each Castellvi reader read "every case independently"; the NeurIPS audit found the reads
  were complete by 4 Sep, reader 2's grades for five cases are 23 Aug second reads, and the readers had seen the May grading
  (`ctsp/CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` S6 and change 19). Align the wording.
- Cover letter says the NeurIPS paper "shares no text, figure or table"; the NeurIPS appendices G and H are captioned
  "Adapted from" the dataset article (CAMERA_READY_CHANGES item 23). Change one (C10).
- Mirror-image CTs (at least tokens 75 and 480, left-right flipped in the April and v11 CTs) are disclosed in the NeurIPS
  appendix but not in the MPDA or `zenodo/KNOWN_ISSUES.md` (CAMERA_READY_CHANGES item 24; grep of `main.tex`).
- `zenodo/KNOWN_ISSUES.md` was last changed 2026-09-07 (v10) and has no entry for the mirrored CTs, the 0533 CT truncation
  (repaired on the grid and HF 2026-09-23/24, `memory/grid-ct-0533-truncated.md`) or the misplaced L5 label in COLONOG_299
  (`sscn/docs/CONTINUANCE_2026-09-19.md`, "report to the dataset").
- The Zenodo v11 README still carries the August Castellvi paragraph (CAMERA_READY_CHANGES item 11); the HF mirror is v10
  with different licence metadata (C1).
- `paper/mpda/REPRODUCE.md` §0 still says "The scheme is v10 ... S1=29"; v11 retired 29 (`ctsp/CLAUDE.md`). Fix the line.
- The arXiv v1 predates the 21-25 Sep changes (ten-page cut, Castellvi five-of-six, funding line); whether to post a
  replacement is not decided anywhere on disk.
- Cite the NeurIPS paper with key `neurips2026lstv` from `CAMERA_READY_NEURIPS/neurips2026.bib` (item 7 there).

What a student would redo: confirm the submission state with Greg; correct the title page (role, conflicts, reader
wording), the cover letter overlap sentence and REPRODUCE.md §0; add the missing KNOWN_ISSUES entries in a new integer
version of the deposit if files change (no fractional versions); rebuild with `build.sh --reprint` and read the whole
output; regenerate the packet with `make_submission.py` from Windows; run `audit_ms.py`, `audit_artifacts.py`,
`audit_pdfs.py`.

---

## 7. NeurIPS 2026 Evaluations and Datasets Track, submission 3474 (accepted)

| item | record |
|---|---|
| title | submitted as "Not All Spines Are Created Equal: How TotalSegmentator Fails on Lumbosacral Transitional Vertebrae" (`Desktop/3474_Not_All_Spines_Are_Create.pdf` = `ctsp/3474_Not_All_Spines_Are_Create.pdf` = `CAMERA_READY_NEURIPS/NEURIPS_CURRENT_PDF.pdf`, byte-identical); OpenReview and camera-ready: "... How CT Segmenters Fail on Lumbosacral Transitional Vertebrae" (`src/neurips_2026.tex` line 35; `REVIEWER_CRITIQUES.txt`) |
| decision | accept, poster, published on OpenReview 24 Sep 2026, id D8yRWDAGQF; authors Gregory John Schwing, Patrick Schwing, Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert (`CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt`) |
| change log | `ctsp/CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md`: three 2026-09-27 passes (adversarial audit, residual issues S1-S19, appendices) supersede the 25 Sep sections, which are marked superseded |
| build | `latexmk -pdf -interaction=nonstopmode neurips_2026.tex` in WSL (TeX Live / TinyTeX; `cm-super` installed 2026-09-26 for Type 1 fonts; first rebuild after needs `latexmk -g`); current `src/neurips_2026.pdf` = 31 pages, 134 `[pending]` slots, modified 2026-09-27 02:15 (checked for this note); content pages 1-10 |
| what the pending slots wait for | Appendix I (SPINEPS under the protocol: jobs 40481323 -> 40481314 -> 40481315; use only if 0 ground-truth-gate mismatches) and Appendix J (v11 summaries: jobs 40480728/31/32, 40480730/33); TotalSegmentator total_v3 (40481824-26) (CAMERA_READY_CHANGES items 19-20) |
| **those jobs were cancelled** | 2026-09-27 15:50 with everything outside `ruleclass/` (`sscn/docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`, closing section; nv11_ts had 6 of 16 shards done and resumes per shard) |
| open decisions for Greg | CAMERA_READY_CHANGES "What remains for Greg" items 3-26, the main ones: upload the camera-ready and the Croissant file (item 3); do not upload while any `[pending]` remains (19) - fill or cut Appendices I-J; run or cut total_v3 (20); headline defects A and B (TotalSegmentator sacrum 0.817 counts its separate S1 class as a miss; junction comparisons subtract two window definitions) are still in the main text (21); publish the April release manifests and the evaluated 174-record split, or keep checklist item 5 at "No" (16, top item); licence per host differs (22); cover letter overlap with the MDPA (23); mirror images (24); competing interests vs the invention disclosure (17, S14); readers' PGY level (18); the Castellvi grades changed after review, Greg's judgement whether to tell the AC (13); post the OpenReview note (8) |
| evidence for the camera-ready numbers | per-case files `Desktop/NeurIPS/bm/benchmark_per_case.csv`, `bm/benchmark_per_case_record_level.csv`, `ens/per_case_dice.csv`; Castellvi `ctsp/docs/castellvi_consensus.csv`, `docs/castellvi_readers_2026-09-04.csv`; recomputation scripts `crverify.py`, `crverify2.py`, `crverify3.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py` live ONLY in a Temp scratchpad: `laptop-scratchpad:neurips_fixes/cr_apply/` (listing). Temp can be swept; copy them into the repository |
| referenced but not found | `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` (named in CAMERA_READY_CHANGES) are in no scratchpad under the Temp project folder (find, 2026-10-08) |
| commit state | the 2026-09-27 edits are uncommitted (git status at session start); CAMERA_READY_CHANGES says "Nothing was pushed, committed, posted or published" |
| caption check | by this note's rough counter two table captions exceed 60 words (per-class DSC table 64, five-fold checkpoint table 66); the log's own counter (`cr_apply/capcount.py`) reported all at most 60 in the second pass |
| released code | public trainer copy `OpenSpineConsortium/spinopelvic-seg` at c105981 (local clone `Desktop/NextPaper/spinopelvic-seg`, remote still `anonymous-neurips-ED/spinopelvic-seg`); it still carries an anonymised citation and author (item 14) |
| camera-ready deadline | not recorded on disk |

What a student would redo: commit the current state; copy the scratch recomputation scripts into the repo; decide with Greg
whether to resubmit the cancelled chains (resume per the grid record) or cut Appendices I-J and the four sentences that point
at total_v3 (exact wording was in the missing INTEGRATE.md §5, so it must be rewritten); fix defects A and B; rebuild; check
fonts and pages; upload.

---

## 8. MLHC 2026 research track (rejected)

`Desktop/MLHC_2026_Research_Track_Paper.pdf` (20 pages, "Preprint: Under Review", 8 Jun 2026; text copy
`ctsp/_paper_text.txt`): "CTSpinoPelvic1K: A Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation",
1,137 volumes, 804 patients, 10-class labelmap. Source `ctsp/mlhc/full-paper-template.tex`; visual abstract
`ctsp/mlhc/visual_abstract.tex`; rebuttals `ctsp/_rebuttal_r2.txt`, `_rebuttal_r3.txt`, `_rebuttal_f65r.txt`. Outcome:
rejected (`memory/publication-roadmap.md`, update 2026-07-24); `ctsp/docs/ROADMAP.md` still says "in review, score 2.75/4"
(stale, C8). Its successor is the MPDA (section 6). Nothing to redo; cite it nowhere as under review.

---

## 9. Other CT-side manuscripts in `Desktop/NextPaper/`

| file | record | state |
|---|---|---|
| `NextPaper/RadAI/main.tex` "A CT Segmentation Network Trained on Labelled Transitional Anatomy Reports the Lumbar Count with a Posterior: Comparison with Public Systems on an LSTV-Stratified Cohort" | Radiology: AI target set 2026-09-08 for the one-shot / numbered-rib CT work (`memory/publication-roadmap.md` redirect; `NextPaper/RadAI/README.md`; `claim_checklist.md`) | 22 `\todo`; its results were to come from Dataset810 (one-shot, retired 2026-09-08) and Dataset813 (numbered ribs, `memory/lstv-oneshot-training-run.md`); whether the Dataset813 folds finished or were scored is not recorded (`sscn/docs/ruleclass/CLASSIFIERS.md` R36: "catalogue only; no per-person output joined") |
| `NextPaper/AR/neurips_2026.tex` + `REVISION_PLAN.md` | the September revision of the NeurIPS paper toward v10 and the one-shot model | FROZEN 2026-09-08 as a source only; Greg said stop drafting it (`memory/publication-roadmap.md`) |
| `NextPaper/VerSeFusion/` (README) | "accompanies the NeurIPS 2026 Datasets & Benchmarks Track submission" | whether it was submitted is not recorded; the CV lists no VerSeFusion paper |

---

## 10. BIBM and XRSpinoPelvic1K

| item | record |
|---|---|
| plan | P1 XRSpinoPelvic1K (limited-field level localisation on DRR/XR) to BIBM, deadline ~5 Jul 2026; collapsed on 2026-06-28 into ONE BIBM wrap-up paper of everything built on the dataset (ostk spinopelvic parameters, CT-to-radiograph bridge with label-carrying DRRs, NiiVue viewer and metrics.json contract, post-op synthesis prototype), BIBM §6.d / §6.n (`memory/publication-roadmap.md`; `ctsp/docs/ROADMAP.md` venue matrix) |
| draft | `Desktop/NextPaper/bibm-spinopelvic/main.tex` "From Segmented CT to Spinopelvic Measurement" (IEEEtran; README lists the `\TODO`s: Table 1 from `python -m ostk all` + `tools/cohort_stats.py`, two figures, the 2-D/3-D tolerance, citations); honest-scope list in its README |
| template | `ctsp/BIBM/IEEE_Conference_Template__3_/` (+ `.zip`, 28 Jun) holds only the IEEE template |
| XRSpinoPelvic1K | `Desktop/XRaySpinoPelvic1K/` (README, `docs/RESULTS.md`, `docs/reader_study_protocol.md`); GitHub repository made PRIVATE 2026-09-26 because it held `localize.py` (level under the C-arm centre) and a Cerner `.ica` credential file (`memory/schwingnet-disclosure-scrub.md`) |
| submission | not recorded (no confirmation file; the CV of 2026-09-27 lists no BIBM paper; SchwingNet `BUILD_REPORT.md` calls it "unknown") |
| SPIE MI 2027 abstract (5 Aug 2026) | planned in `ctsp/docs/ROADMAP.md`; not recorded |

What a student would redo: treat both as unwritten; any XR level-localisation content is SchwingNet-adjacent and private.
The spinopelvic numbers must be recomputed from v11 with `ostk.labels.labels_for(volume)` (`ctsp/CLAUDE.md`).

---

## 11. Iliac crest clinical paper

`ctsp/paper/clinical/main.tex` "The iliac crest is an unreliable level landmark in transitional lumbosacral anatomy: a
morphometric study of 802 screening CT examinations"; target Spine Surgery and Related Research; "complete draft with real
numbers. Needs the introduction expanded and someone to argue with the discussion" (header); first author "[First
author]"; last commits 2026-08-22 (0ecbb82). It exists because the MPDA may not test hypotheses. **Caution:** the iliac-crest
measure touches the pelvis and the lumbosacral junction, so by `ctsp/CLAUDE.md` it must be recomputed from v11 before use.

---

## 12. OpenSpineConsortium medical-education study

| item | record |
|---|---|
| PUBLISHED | Schehr A, Kim J, Schwing G. "OpenSpineConsortium: An Open-Source Framework for Medical Student Engagement in Computational Spine Imaging Research." Cureus 2026;18(7):e112661, doi 10.7759/cureus.112661, review 28 Jun-9 Jul, published 14 Jul 2026 (`Desktop/cureus.pdf`; PMID 42598196 per `Desktop/ERAS_2026/CV_2026-09-27.pdf`) |
| JEEHP version | `ctsp/OSC MedEd Manuscript - JEEHP.docx` (14-15 Jun 2026): "OpenSpineConsortium: an asynchronous open-source framework ... a single-group pre-and post-test study", same 16 respondents and the same six-domain table (Wilcoxon) |
| CNS 2026 poster | CNS 66639 "Beyond the Cadaver Lab: The OpenSpineConsortium as an Asynchronous, Open-Source Framework ..." selected as Printed Poster (`Desktop/openspineconsortium.github.io/contributions/manifest.json`); one-slide poster `ctsp/Med_Ed_CNS.pptx` and `ctsp/Med_Ed_CNS_visual_abstract.pptx` (two different files, both last edited by Ashley Schehr, 2026-09-01); visual abstract source `ctsp/poster/make_visual_abstract.py` -> `poster/OSC_visual_abstract.{pdf,png}` |
| board | `ctsp/Student_Projects/BOARD.md` card `meded`: lead Ashley Schehr, co-lead Greg; open task "journal submission"; survey summary `meded/survey-summary.json` on the website; raw survey CSV never committed; survey protocol `ctsp/docs/survey_protocol.md` |
| caution | submitting the JEEHP version now would publish the same survey data twice (contradiction C9) |

---

## 13. CNS 2026 (Washington DC, 31 Oct-4 Nov 2026)

### 13.1 The twelve OSC abstracts (`Desktop/openspineconsortium.github.io/contributions/manifest.json`, generated 2026-05-19; titles verbatim from the CNS submission list)

| CNS id | title (short) | status in the manifest | students |
|---|---|---|---|
| 66629 | Not All Spines Are Created Equal: A Single-Shot CT Segmentation Model for Preoperative Detection of Lumbar and Thoracic End Anomalies | Mini Oral Poster (Greg's talk; MP4SP1 Mon 2 Nov 5:21-6:00 PM, `memory/cns-deck-v2-2026-09-25.md` v8) | Greg sole author |
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
Three more OSC topics are "In preparation" (vertebral spacing, SVA, TPA). Topic list with students:
`Desktop/NextPaper/CNS 2026 ABSTRACT PROJECTS.csv`. The submitted abstract texts are not on disk (only titles). The
COMMERCIALIZATION file counts "12 CNS 2026 abstracts" as public disclosures (`ctsp/COMMERCIALIZATION.md` line 92).
**Check before the posters are shown:** the PI/SS abstract (69093) and the measurement abstracts were computed by May 2026;
the spinopelvic estimator defects and the canal/end-plate defects were found in August-September
(`ctsp/docs/SPINOPELVIC_ESTIMATOR.md`, `docs/LEVEL_MORPHOMETRY.md`). Whether the May numbers predate the fixes is not
recorded.

Other CNS 2026 items in the CV, outside this topic: the LITT recurrence-signature oral (Abstract 418), the H3K27M
diffuse-midline-glioma shunt case report poster (`Desktop/MANUSCRIPT/2026 CNS Abstract Submission Portal ... .pdf`), and an
LLM-vs-EPIC craniotomy coding poster (`Desktop/ERAS_2026/CV_2026-09-27.pdf`).

### 13.2 Greg's spine deck for 66629

| file | what | disclosure status |
|---|---|---|
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | **current disclosure-safe deck**, 17 slides, CT side only; generator `ctsp/paper/cns2026/make_cns_deck_v12_public.py` (+ `prep_v16_public_figs.py`); every number asserted against the committed NeurIPS camera-ready; adds the MPDA pipeline, hardware figure and the spinopelvic table (PI 52.1 vs Veilleux 52.1 / Hasegawa 53.4; SS 36.6; PT 15.5) | safe (`memory/cns-deck-v2-2026-09-25.md` v11_public/v12_public) |
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | 15-slide predecessor | safe |
| `Desktop/CNS2026_Schwing_SchwingNet_CNStemplate.pptx` (= `_v10`, same byte size 13,608,401), `_v9.pptx` | 21-slide C-arm decks on the CNS template | **disclose Part B and the sweep; never show publicly** |
| `Desktop/CNS2026_Schwing_SchwingNet.pptx` (v3), `CNS2026_Schwing_Spine_v2.pptx` | earlier arcs | disclose Part B results |
| `Desktop/CNS2026_Schwing_LSTV.pptx` | 7 Sep draft "Naming a Lumbar Level Without Counting From C2: CTSpinoPelvic1K and a One-Shot Detector"; "not presented" (TTO followup copy name) | draft |
| generators | `ctsp/paper/cns2026/make_cns_deck*.py`, `prep_*`, `figs*` are NOT tracked (45df97d; `.git/info/exclude`) and must never be pushed (`memory/schwingnet-disclosure-scrub.md`) | - |

Rules learned on this deck (`memory/cns-deck-v2-2026-09-25.md`): CNS template traps (titles about 60 characters, zero-height
text boxes make PowerPoint refuse the file); ACCME rules (no disclosure slide, study design and dates on every data slide,
generic names, no ineligible-company logo, HIPAA statement); render with PowerPoint COM (no LibreOffice on this machine) and
look at every slide; no two consecutive results slides in the same visual form; NeurIPS track name is "Evaluations and
Datasets" (v10 wrongly said "Datasets and Benchmarks"). Still open per that note: abstract number, session and author list
to match the submitted abstract (the session is now known: MP4SP1). The talk title promises a single-shot model; no
evaluated single-shot model is recorded on disk (section 9; C17).

### 13.3 CNS Abstract 418 (LITT) deck, one line (U251 project)

`u251/SLIDES/CNS2026_Schwing_Abstract418_CNStemplate_v5.pptx` (46 slides; `memory/cns-abstract-418-deck.md`) and a later
`..._v6.pptx` (2026-09-27 06:56, not described in memory); binding rule: instrument-contamination statements stay
conditional (`memory/litt-contralateral-two-readings.md`).

---

## 14. AACA Tech Fair (presented)

`Desktop/TechFair_LSTV_Schwing.pptx` (15 slides; also `ctsp/TechFair_LSTV_Schwing.pptx`, `NextPaper/TechFair_LSTV_Schwing.pptx`):
"Harnessing Algorithmic Disagreement for Automated Lumbosacral Transitional Vertebrae Detection", 43rd AACA meeting, Mayo
Clinic, 13 Jun 2026. A separate earlier pipeline built from third-party segmenters (TotalSpineSeg, SPINEPS/VERIDAH); listed
in the TTO package for completeness as disclosing neither Part A nor Part B (`Desktop/private_ip/TTO_package_2026-09-25/
00_README_for_TTO.md` item 05). The title slide says "Department of Neurosurgery" (C5). Nothing to redo.

---

## 15. Invention disclosure, patent package and disclosure control

| document | what | state |
|---|---|---|
| `sscn/docs/INVENTION_DISCLOSURE.md` | engineering disclosure for TTO and counsel: the problem, five aspects (A closed-loop acquisition control, B fewer exposures, C supernumerary segment without a rare class, D no imaging leaves the room, E persistent digital marker), claim scope, §101 strategy, freedom to operate, novelty, what a provisional must contain, what not to patent | written 2026-09-18 |
| `sscn/docs/DISCLOSURE_MEMO.md` | counsel-only memo on publication timing and prior public availability | written 2026-09-18 |
| `sscn/docs/PATENT_PACKAGE.md` | superseded; records three corrections (US 8,718,346 is clear; the review Spaces were readable; the clock-started question) | - |
| `sscn/docs/provisional/` (`SPECIFICATION.md`, `CLAIMS.md`, `COVER_SHEET.md`, `FILING_CHECKLIST.md`, `README.md`) | provisional application package; FIG. 1-13 not drawn; first item "export the GitHub audit log"; "The manuscript is held until the provisional is on file" | not filed (no record of filing) |
| `sscn/docs/research_patent_2026-09-18.json`, `research_registration_free_2026-09-18.json`, `disclosure_audit.json`, `disclosure_forensics.json`, `disclosure_evidence/` | prior-art research and the public-surface audit (`tools/disclosure_audit.py`: "Run it before any submission, talk or release") | 2026-09-18 |
| `Desktop/private_ip/TTO_package_2026-09-25/` | 00 README for TTO; 01 WSU invention disclosure form (docx, pdf, **signed pdf**); 02 the confidential Part B manuscript (+ followup rev2-rev5); 03 NeurIPS camera-ready; 04 MDPA main + supporting information; 05 AACA slides; 06 disclosure timeline; 07 cover email draft; `SCRUB_PLAN.md`; `followup/` CNS decks v2-v10 | sent to Greg 2026-09-25; TTO (Laura) asked for the inventor signature on page 8 and Chair/Dean signatures (`sscn/docs/RESUME_2026-09-22_PM.md` line 347); MOU left unsigned pending clarification (line 353) |
| disclosure title | "(A) a segmenter-agnostic classifier that flags transitional vertebrae on preoperative CT, and (B) a neural network that names vertebral levels from a single intraoperative C-arm exposure without registration to a preoperative scan"; sole inventor; NIH F30GM147909 (ended 31 May 2026) | `00_README_for_TTO.md` |
| `Desktop/private_ip/idf_work/` | `fill_idf.py`, `fill_hpr_vindr.py`, patch scripts that filled the forms | - |
| `Desktop/private_ip/github_purge_requests/` | drafts and SHA lists for GitHub Support purges (orphaned `proposals/**`, 171 commits; 5 detector ONNX files on the OSC site, 106 SHAs) | **Greg must file**; until then those SHAs return HTTP 200 (`memory/schwingnet-disclosure-scrub.md`) |
| evidence bundles | `/rs/rs_grp_oschome/go2432/private_ip/git_bundles_2026-09-26/` (grid only) | done 2026-09-26 |
| commercial stance | `ctsp/COMMERCIALIZATION.md`, `ctsp/IRB_ADDENDUM.md` (both gitignored); `memory/commercialization-stance.md` | the CNS abstracts, AACA, NeurIPS and Zenodo/arXiv are already public; Part A's name-free classifier and Part B are undisclosed (`06_disclosure_timeline.md`) |

Part A has no manuscript; its plan is `sscn/docs/CT_LSTV_CLASSIFIER_PLAN.md` and the pre-registration draft
`sscn/docs/ruleclass/PREREG_rules.md` (awaiting Greg's sign-off; `RESUME` 2026-09-27 16:45).

What a student would do: nothing public until Greg confirms the filing; run `tools/disclosure_audit.py` before any talk or
submission.

---

## 16. Data requests (all drafted, none sent)

| request | file | status |
|---|---|---|
| 14 fluoroscopy cine sources (Bournemouth QF, Maastricht, Bern, Pittsburgh swallow, Seattle Science Foundation, Mayfield, DMX, Radiopaedia, Procedure Guide, Konica Minolta, Jefferson, MTFI, Faubel, DARADIA) | `sscn/docs/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md` (checklist, verified addresses, two UNVERIFIED) + Outlook drafts `sscn/docs/fluoro_requests_eml/NN_*.eml` (11 files); earlier draft `FLUORO_CINE_DATA_REQUESTS_DRAFT_2026-09-26.md`; sources `FLUORO_VIDEO_SOURCES_2026-09-26.md`, `FLUORO_VIDEO_YOUTUBE_SCAN_2026-09-26.md` | `requested_not_sent` (`sscn/data_platform/DATA_MANIFEST.md`, entry `fluoro_cine_requests_2026_09_26`) |
| SX-Stitch intraoperative C-arm series (1,032 frames, SUSTech/PUMCH) | `sscn/docs/data_requests/SX-Stitch_request.md` | `requested_not_sent` (entry `sx_stitch_request`) |
| Balgrist ex-vivo lumbar CT + C-arm (Jecklin 2024) | `sscn/docs/outreach/balgrist_data_request_2026-09-21.md` | `requested_not_sent` (entry `balgrist_exvivo_request`); its opening sentence still reads "I am [a neurosurgery resident; confirm title]" |
| VinDr-SpineXR HPR determination | `ctsp/IRB_VinDr_2026-09-25/` (gitignored), draft `sscn/docs/IRB/HPR_determination_VinDr-SpineXR_draft.md` | sent to Greg 2026-09-25 for IRBQuestions@wayne.edu; determination number not recorded |

The ready-to-send file's "Read once before sending" list binds: commercial scope sentence, IRB question first, delete "we
would not train on it" if fine-tuning is possible, co-authorship offers, the YouTube-copies sentence, Radiopaedia only by
application. Already obtained items are listed there (`/rs/rs_grp_oschome/go2432/data/external/fluoro_video/`, grid).

---

## 17. Flagship, feasibility and plan documents

| file | what | standing |
|---|---|---|
| `sscn/docs/FLAGSHIP_PLAN.md` | "one corpus, one super model, one claim": five contributions, payload (parity with surgeon + LevelCheck on transitional spines), gates G0-G7 with evidence files, corpus roles, the 50/10/40 transitional split | written 2026-09-23 (`memory/flagship-program.md`, `memory/flagship-paper-frame.md`); G6 moved to paper 2 on 2026-09-24 |
| `sscn/docs/RSNAI_PLAN.md` | checklist for main_v2 (A-E) | stopped 2026-09-22 |
| `sscn/docs/FEASIBILITY_REPRODUCE.md` | the one-job reproduction of the feasibility manuscript (`slurm/reproduce_feasibility.sh`) | feeds section 4 only |
| `ctsp/Feasibility_FOV.docx` | external report (17 Sep 2026, about 3,800 words) arguing isolated-stack naming is ill-posed; tested claim by claim on 2026-09-17 (three of five "disproofs" overturned by the adversarial audit) | reference only (`memory/feasibility-claims-measured.md`) |
| `ctsp/MULTI_XR.docx` | external report (18 Sep 2026, about 3,800 words) "Real-Time Vertebral Level Localization and Limited Field-of-View Classification via Deep Serial Fluoroscopic Mapping"; carries "[cite: n]" markers and unverified competitor claims (for example X23D, RadGS-Reg rows) | reference only; no file in either repository cites it; claims of the same kind were refuted in `SchwingNet/lit/CITABLE_CLAIMS.md` |
| `ctsp/C-Arm Validation Research Plan.pdf` | Google-Docs report "Translational Roadmap for Exact Intraoperative Vertebral Counting via Overlapping C-Arm Fluoroscopy" | reference only |
| `sscn/docs/GUIDED_ACQUISITION.md`, `SWEEP_PROTOCOL.md`, `CARM_DEPLOYMENT_EVIDENCE.md` | the sweep and guided-acquisition loop | private (invention) |
| `sscn/docs/WRONG_LEVEL_COST_EVIDENCE.md`, `WRONG_SITE_BURDEN_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `COUNTING_EVIDENCE.md` | adversarially verified evidence briefs (three refutation votes per claim) behind the introductions, the QI paper and the CNS cost board | reuse for any introduction; derived totals must be labelled derived |

---

## 18. Reports to funders

`ctsp/RPPR_Accomplishments.{docx,pdf}` (24 Jul 2026), `RPPR_B4_Training.*`, `RPPR_RCR_Instruction.docx`, `Desktop/RCR.pdf`, and
the sponsor letter `ctsp/Sponsor Progress Report Letter 2026.{docx,pdf}` (Loren Schwiebert, 24 Jul 2026): the NIH F30 year-4
progress report. It reports one Cureus paper, five accepted abstracts, NeurIPS under review, and says a single-shot CT model
was "developed and validated" (C17). Already sent (dated July); nothing to redo.

---

## 19. Desktop classification (research-relevant items)

Top level of `Desktop/` and the root of `ctsp/` (which holds many untracked files, per the session-start git status).
Personal and administrative files (taxes, leases, licences, benefits, insurance, residency application material, letters of
recommendation, personal statements, religious and video media, installers, `.ica` remote-session files, browser shortcuts)
are not listed one by one.

| item | class | note |
|---|---|---|
| `Desktop/3474_Not_All_Spines_Are_Create.pdf`, `ctsp/3474_...pdf` | submission (NeurIPS, as reviewed) | section 7 |
| `Desktop/MLHC_2026_Research_Track_Paper.pdf` | submission (rejected) | section 8 |
| `Desktop/MDPA.pdf`, `MDPA_FINAL.pdf`, `ctsp/MDPA.pdf`, `Desktop/arxiv_prev.pdf`, `ctsp/arxiv_final_draft_9_19_2026.pdf`, `Desktop/CTSpinoPelvic1K_*` | manuscript copies (MPDA) | section 6 |
| `Desktop/MDPA_AI.pdf`, `ctsp/GPTZero AI Scan - ...pdf` | AI-text scans of the MPDA | section 6 |
| `Desktop/CNS2026_*.pptx` (8 files) | decks | section 13.2 |
| `Desktop/TechFair_LSTV_Schwing.pptx` | deck (presented) | section 14 |
| `ctsp/Med_Ed_CNS.pptx`, `ctsp/Med_Ed_CNS_visual_abstract.pptx` | poster / visual abstract (CNS 66639) | section 12 |
| `Desktop/cureus.pdf` | published article | section 12 |
| `ctsp/OSC MedEd Manuscript - JEEHP.docx` | manuscript (duplicate of the published study) | section 12 |
| `ctsp/MULTI_XR.docx`, `ctsp/Feasibility_FOV.docx`, `ctsp/C-Arm Validation Research Plan.pdf`, `ctsp/Spine Fluoroscopy Image Datasets.pdf`, `ctsp/Fluoroscopic AI Dataset Author Contacts - Google Gemini.pdf`, `Desktop/Spine Morphometrics_ Beyond Basic Measurements.pdf` | externally generated research reports (references; verify before citing) | section 17 |
| `ctsp/Browser Extension HPC Orchestration Protocols.pdf`, `University-Agnostic HPC AI Architecture.pdf`, `Protocols for Reproducible Machine Learning Research.pdf`, `WayneStateVSCodeSetupExtension.pdf`, `Configuring Resend DNS in Spaceship.pdf`, `Remote Development FAQ.pdf`, `Publishing Extensions _ ...pdf` | Beethoven / grid-tool references (not this topic; see `Desktop/ashley-bridge/docs/guides/`) | - |
| `ctsp/2026 CNS AM Speaker Powerpoint Template.pptx`, `ctsp/ACCME Accreditation Guidelines ...pdf`, `ctsp/OUP_General_Template.zip`, `ctsp/med_phys_latex_template_v2021.zip`, `Desktop/Manuscript_Template.docx`, `Desktop/ama.bst` | templates and rules | - |
| `ctsp/2026_269 Schwing IRB Not HPR Determination 9.2.26.pdf` (and the duplicate with a space), `Desktop/2026 144 Schwing IRB Not HPR Determination 4.21.26.pdf`, `Desktop/IRB Not HPR Determination 4.21.26.pdf`, `ctsp/OSC_HPR_Determination_public_datasets.pdf`, `Desktop/hpr_determination_tool_revised_11_2021_SCHWING_FILLED.pdf`, `ctsp/IRB_VinDr_2026-09-25*` | ethics determinations cited by the manuscripts (2026-269 = public de-identified data, 2 Sep 2026; 2026-144 = April 2026) | - |
| `Desktop/spine_study_protocol.pdf` | protocol "Development of a Publicly Accessible, Deep Learning-Ready Clinical and Radiographic Dataset for Spine Surgery Outcomes" (Mar 2026) | not a manuscript |
| `ctsp/VAIDYAS_IRB.pdf` | another investigator's IRB protocol (IRB-21-10-4123), reference | - |
| `Desktop/wsu_patent_policy.pdf` | WSU patent policy, reference for section 15 | - |
| `Desktop/AI_Imaging_Workshop.{docx,pdf}`, `ctsp/AI_Imaging_Workshop.pdf` | teaching agenda (20 Jun workshop) | - |
| `Desktop/OUP_General_Template_ID.pdf`, `ctsp/MAN_PREP.pdf`, `Desktop/CNS_SNO Abstract_tnn edits.docx`, `ctsp/Ablation video_TNN_18Sept26.pptx`, `Desktop/JNS24-1395_..._Annotated.pdf` | U251/LITT and glioma work (Neuro-Oncology letter, Neuro-Oncology Advances instructions, SNO abstract, a collaborator's slide, a reviewed JNS manuscript) | other project, one line |
| `Desktop/MANUSCRIPT/` | BMJ Case Reports submission (H3K27M diffuse midline glioma, shunt) with consent forms | clinical case report; patient material; not this topic |
| `Desktop/STUMP_RIBS.pdf`, `ctsp/RIBSEG.pdf`, `ctsp/TS_DS.pdf`, `ctsp/COBRA.pdf`, `ctsp/2D-3D-GS_UG.pdf`, `ctsp/AITR-2002-001.pdf`, `ctsp/CaseReports_T12_hypoplastic_rib.pdf`, `ctsp/Sun_2021_...pdf`, `ctsp/PG-Net_...pdf`, `ctsp/Development_and_Evaluation_of_a_Robotic_System...pdf`, `ctsp/PANJABI_1991_FULL*.pdf`, `Desktop/Panjabi_1976_JBJS_thoracic.pdf`, `Desktop/2505.*.pdf`, `Desktop/2602.*.pdf`, `Desktop/2605.*.pdf`, `Desktop/venetti.pdf`, `Desktop/arrillaga-romany...pdf`, `ctsp/2017 Summer Research Program Abstract Book.pdf` | published papers and books (references) | - |
| `ctsp/BIBM/`, `ctsp/mlhc/` | template folder; MLHC source | sections 8, 10 |
| `Desktop/BUU-LSPINE_400/` (in `Desktop/NeurIPS/`), `ctsp/BUU-LSPINE_400`, `ctsp/BUULSPINE_3600`, `ctsp/AASCE19`, `ctsp/LATERAL_ATLAS`, `ctsp/PIG`, `ctsp/CSPINE_ARCHIVE` | data, not manuscripts (data topic) | - |
| `Desktop/NeurIPS/` | NeurIPS working files (per-case benchmark CSVs `bm/`, `ens/`, the May Castellvi sheet `Lumbosac_Castelvii_Class.csv`, drafts) | section 7 evidence |
| `Desktop/private_ip/` | invention disclosure work | section 15 |
| `Desktop/ERAS_2026/` | residency application; `CV_2026-09-27.pdf` lists publication statuses used above | personal; cite only the publication list |
| `Desktop/Lumbosac.csv`, `ctsp/Lumbosac.csv` | Castellvi grades for 39 cases (`memory/publication-roadmap.md`) | data |

---

## 20. Contradictions between documents

| id | readings | trusted, and why |
|---|---|---|
| C1 | Zenodo: `memory/hf-mirror-is-v10.md` (2026-09-27) says "Zenodo v10 2026-09-07"; `memory/zenodo-deposit.md` (2026-09-07) "current v10"; `ctsp/Student_Projects/BOARD.md` "v10 on Zenodo ... v11 in preparation" with task "publish v11 to Zenodo and Hugging Face". Against: `ctsp/paper/mpda/cover_letter.md`, `title_page.tex`, `CAMERA_READY_NEURIPS/src/checklist.tex`, `private_ip/.../06_disclosure_timeline.md` all give v11 = 10.5281/zenodo.22797014 published 18 Sep 2026, and CAMERA_READY item 11 describes the v11 README | v11 IS on Zenodo (four documents name the DOI and date; one describes its README). The Hugging Face mirror is still v10 (re-checked 2026-09-24 in `SchwingNet/packet_src/build/BUILD_REPORT.md`; 2026-09-27 in memory), so student identifier text stays v10 only for the HF route. Not re-verified today (no network): open https://doi.org/10.5281/zenodo.22797014 |
| C2 | `memory/rsnai-paper-endpoint.md` names `paper/rsnai/main_v2.tex` "THE CULMINATION"; `memory/schwingnet-manuscript.md` and every later record use `SchwingNet/main.tex` | SchwingNet (later, and every subsequent commit is there) |
| C3 | Title: CV `Desktop/ERAS_2026/CV_2026-09-27.pdf` "... robust to transitional anatomy, versus registration-assisted neurosurgeons"; `front_matter.json` decision still mentions "robust"; `TITLE.md` and the 09-27 PDFs print the short title | `TITLE.md` + compiled PDFs |
| C4 | Submission: CV says "Submitted" (Sept 2026) and `TITLE.md` carries an ERAS line "Submitted September 2026"; `06_disclosure_timeline.md` and `00_README_for_TTO.md` say held pending TTO advice; `docs/provisional/FILING_CHECKLIST.md` says held until the provisional is filed; RESUME 2026-09-27 13:20 says the G0 token "blocks submission"; `packet/PACKET_README.md` "not submittable" | the repository: not submitted as of 2026-09-27. If the CV is wrong, the ERAS entry needs correcting; Greg must say |
| C5 | Affiliation: memory "Department of General Surgery"; SchwingNet `front_matter.json` General Surgery; MPDA title page, NeurIPS, arXiv, Cureus, JEEHP, TTO README "Department of Surgery"; QI paper, main_v2, TechFair slide "Department of Neurosurgery"; Balgrist draft "[a neurosurgery resident; confirm title]"; CAMERA_READY item 15 left it untouched | never Neurosurgery (memory, binding). "Surgery" vs "General Surgery" is Greg's choice; both appear in submitted documents |
| C6 | Role: MPDA `title_page.tex` line 85 "a faculty surgeon"; `00_README_for_TTO.md` and the HPR form record (RESUME line 352) "Resident physician" | resident (form-level records); fix the MPDA title page |
| C7 | Conflicts: MPDA title page "no relevant conflicts"; NeurIPS acknowledgments "No conflicts of interest" (S14, Greg's judgement); SchwingNet `front_matter.json` "The author has a commercial interest in a level-confirmation product under development"; `memory/commercialization-stance.md` "never state the commercial goal in anything that leaves" | unresolved; counsel sees the COI statement before filing (`FILING_CHECKLIST.md`); Greg decides one consistent statement for all three |
| C8 | MLHC: `memory/publication-roadmap.md` rejected; `ctsp/docs/ROADMAP.md` "in review, score 2.75/4"; SchwingNet `BUILD_REPORT.md` "outcome not recorded on disk" | rejected (later record, Greg's) |
| C9 | Med-ed: published in Cureus 14 Jul 2026 (`Desktop/cureus.pdf`, CV, RPPR) vs board task "journal submission" for the JEEHP manuscript (`BOARD.md`, 2026-09-27) | published; a JEEHP submission of the same data would be duplicate publication unless it reports new data |
| C10 | MPDA cover letter "shares no text, figure or table" with NeurIPS vs NeurIPS Appendices G/H "Adapted from" the dataset article | unresolved (CAMERA_READY item 23) |
| C11 | Loren Schwiebert: `BOARD.md` "senior author, dataset article"; MPDA title page and arXiv list 14 authors without him; he is last author on NeurIPS | MPDA title page for the MPDA |
| C12 | Castellvi reads "each reading every case independently" (MPDA contribution statement) vs reads dated by 4 Sep with prior exposure to the May sheet (CAMERA_READY S6, change 19) | the NeurIPS audit (it cites the dated reader files) |
| C13 | SchwingNet body words: 3,000 (`PACKET_README.md`, 09-25), 2,986 (`BUILD_REPORT.md`, 09-27, camera-ready counter), 2,998 (RESUME 09-27, review copy) | not a conflict: two copies and two dates; the review copy is the one under the limit at 2,998 |
| C14 | SchwingNet `README.md`/`FINAL_CHECK.md` say four figures, four tables, 2,984 words; `main.tex` has five figures and three tables | `main.tex` (the README is a dated record) |
| C15 | LITT deck: memory says v5 current; disk has v6 (2026-09-27 06:56) | disk; v6's content is not described anywhere read |
| C16 | "Current" CNS deck: memory says v12_public; the Desktop also holds the CNStemplate decks (v9, v10, unversioned = v10) that disclose Part B | v12_public for anything public |
| C17 | RPPR (24 Jul) "developed and validated a single-shot CT segmentation model" and the CNS 66629 title; `memory/lstv-oneshot-training-run.md`: one-shot folds launched 7 Sep, retired 8 Sep for Dataset813, whose outcome is not recorded | no evaluated single-shot model is recorded; the talk presents the NeurIPS merge-based segmenter (memory v11/v12_public) |
| C18 | `paper/mpda/REPRODUCE.md` §0 "The scheme is v10 ... S1=29" vs `ctsp/CLAUDE.md` "The release is v11 ... 29 retired" | CLAUDE.md for the working tree |

---

## 21. One organised order of work for a student taking these over

1. **Ask Greg six questions** (none is answerable from disk): was SchwingNet uploaded; was the MPDA's 2026-09-25 packet
   uploaded and under what number; has the TTO advised and is the provisional filed; what is the VinDr determination
   number; was BIBM 2026 submitted; is the NeurIPS camera-ready deadline past.
2. **Disclosure first.** Until the provisional is confirmed: no SchwingNet, QI, focused or main_v2 text, figure or deck
   anywhere public; only `CNS2026_Schwing_NotAllSpines_public_v12.pptx` for the talk; run `sscn/tools/disclosure_audit.py`
   before any talk or upload; Greg files the GitHub purge requests.
3. **NeurIPS camera-ready** (an accepted paper with a deadline): commit; rescue the scratch recomputation scripts; resubmit or
   cut the cancelled appendix chains; fix defects A and B; settle items 16-24; upload.
4. **MPDA**: title page role/conflict/reader wording, cover-letter overlap sentence, REPRODUCE.md §0, KNOWN_ISSUES entries;
   reprint check; packet.
5. **SchwingNet paper 1**: the seven author decisions, supplement to 12 pages, Word packet rebuild, CLAIM 2024 NEEDS-EDIT
   items, then submission only on the TTO's word.
6. **CNS posters**: re-check each student abstract's numbers against v11 and the fixed estimators before the posters are
   shown (2 Nov).
7. **Med-ed**: drop the JEEHP plan or turn it into a follow-up with new data (Ashley Schehr leads).
8. **Paper 2, the iliac-crest paper, BIBM, the RadAI CT paper**: start only with Greg's go-ahead; each needs new data or a
   v11 recomputation first.

Every one of these steps follows the house pattern the SchwingNet folder already implements: results file -> manifest key
-> `\RESULT{}` -> strict build -> render and look (`SchwingNet/RESULTS_BUILD.md`; `ctsp/Student_Projects/RECIPE.md`, local
commit 3f1cf04, not pushed).

---

## 22. Memory notes that bind this topic (exportable context)

| note | one line |
|---|---|
| `rsnai-author-instructions.md` | Radiology: AI limits (3,000 words, 250-word abstract, 6 figures of at most four parts, 4 tables, 35 references; CLAIM 2024; double-anonymized; TIF/EPS figures; arXiv allowed with disclosure) |
| `rsnai-paper-endpoint.md` | main_v2 as the endpoint (superseded, C2) and the citation traps |
| `schwingnet-manuscript.md` | SchwingNet folder rules: rigor-passing numbers only, CLAIM map, ATLAS cards, no counting rule, no leaked banks |
| `rigor-audit-findings.md` | the eight audit items (section 2.5) |
| `six-figure-paper-plan.md`, `paper-split-2026-09-24.md`, `flagship-paper-frame.md`, `flagship-program.md` | how the paper's scope moved from six figures to five and to two papers |
| `figure-preferences-schwingnet.md`, `figure-captions-terse.md`, `tables-black-not-colour.md`, `chart-preferences.md`, `journal-figure-and-style-rules.md`, `writing-preferences.md` | style rules (section 0) |
| `publication-roadmap.md` | P1-P6 plan, MLHC rejection, BIBM collapse, Rad AI redirect |
| `hf-mirror-is-v10.md`, `zenodo-deposit.md` | release state (C1) and the new-version recipe |
| `cns-deck-v2-2026-09-25.md`, `cns-abstract-418-deck.md`, `litt-contralateral-two-readings.md` | deck history, disclosure-safe cut, LITT wording rule |
| `commercialization-stance.md`, `schwingnet-disclosure-scrub.md`, `fluorocap-repo-private.md`, `level-service-serving.md` | what may never be public |
| `user-affiliation-general-surgery.md` | affiliation (C5) |
| `feasibility-claims-measured.md` | the feasibility report tested; QI deep research; head/encoder pairing trap |
| `annotator-roster.md` | who annotated what (MPDA authorship evidence) |
| `lstv-oneshot-training-run.md`, `competitor-benchmark.md` | the one-shot / numbered-rib CT arm behind the RadAI draft |
| `lab-recipe-and-board.md` | the student board that lists these projects |
| U251 notes (`u251-*`) | another project; the LITT deck and manuscript live in `u251/` |

---

## 23. Unknowns

| fact | where looked |
|---|---|
| Whether SchwingNet paper 1 was uploaded to Radiology: AI | `SchwingNet/*.md`, `packet*/`, `docs/RESUME_2026-09-22_PM.md`, TTO package, git log; only the ERAS CV says "Submitted" |
| Whether the MPDA 2026-09-25 resubmission was uploaded; manuscript number; editorial status | `ctsp/paper/mpda/*.md`, `dist/submission/`, git log, memory |
| Whether the provisional patent application was filed; the TTO's advice on Part B | `sscn/docs/provisional/`, `Desktop/private_ip/`, RESUME, memory |
| Whether the GitHub Support purge requests were filed | `Desktop/private_ip/github_purge_requests/README.md` (drafts only), memory |
| VinDr-SpineXR determination number and date | `main.tex` Ethics paragraph, `ctsp/IRB_VinDr_2026-09-25/` (not opened: gitignored personal form), RESUME |
| NeurIPS camera-ready deadline, whether the camera-ready or the Croissant file was uploaded, whether the OpenReview note was posted | `CAMERA_READY_CHANGES.md`, RESUME, memory |
| Location of `OPENREVIEW_NOTE.md`, `INTEGRATE.md`, `FACTS_{split,numbers,build}.md` | find over `laptop-scratchpad:` (none found) |
| Whether BIBM 2026 (5 Jul) or SPIE MI 2027 (5 Aug abstract) submissions were made | `Desktop/NextPaper/bibm-spinopelvic/`, `ctsp/BIBM/`, `ctsp/docs/ROADMAP.md`, CV |
| Whether VerSeFusion was submitted to NeurIPS D&B | `Desktop/NextPaper/VerSeFusion/README.md`, CV |
| Where the MLHC decision letter and reviews are | `ctsp/mlhc/`, `ctsp/_rebuttal_*.txt`, memory (outcome only) |
| Whether the Dataset813 numbered-rib folds finished and were scored | memory `lstv-oneshot-training-run.md`, `competitor-benchmark.md`; `sscn/docs/ruleclass/CLASSIFIERS.md` |
| Whether the A5 film re-score on the v9 bank (chain 40415667 -> 40415670) landed | `SchwingNet/README.md`, NUMBERS.md, REVISION_LOGs |
| Training year (PGY) of the two Castellvi readers in September 2026 | `CAMERA_READY_CHANGES.md` S11 ("No record of the training year found"), MPDA title page |
| Full name of "Dr Tech", the confirming clinical reader on the board | `ctsp/Student_Projects/BOARD.md`, RESUME 2026-09-27 16:45 |
| The submitted text of the twelve CNS abstracts | contributions manifest (titles only), `Desktop/NextPaper/`, `ctsp/` |
| Whether the student CNS abstract numbers were computed before the spinopelvic-estimator and canal/end-plate fixes | `ctsp/docs/SPINOPELVIC_ESTIMATOR.md`, `docs/LEVEL_MORPHOMETRY.md`, contributions manifest |
| Whether the CNS slides were submitted to the meeting, and by what deadline | `memory/cns-deck-v2-2026-09-25.md`, TTO timeline ("slides not yet submitted" on 25 Sep) |
| Whether the JEEHP manuscript was ever submitted, and why the study went to Cureus | the docx, `BOARD.md`, CV |
| Whether an arXiv replacement of the MPDA is planned | `ARXIV_SUBMISSION.md`, cover letter |
| Who rebuilt `ctsp/paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` at 2026-10-08 09:41, and why | file timestamp only; no commit |
| Live state of Zenodo v11 and the Hugging Face mirror today | no network in this session |
| Whether the 14 fluoroscopy, SX-Stitch and Balgrist requests were ever sent after 2026-09-26 | `sscn/data_platform/DATA_MANIFEST.md` says `requested_not_sent`; nothing later |
| Content of the LITT deck v6 | `u251/SLIDES/` listing only; memory describes v5 |
