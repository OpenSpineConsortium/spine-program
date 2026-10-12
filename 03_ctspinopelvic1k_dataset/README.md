# 03_ctspinopelvic1k_dataset

**CTSpinoPelvic1K: release v11, the dataset article and the NeurIPS camera-ready.**
Project 03 of the spine programme (`../_plan/PLAN.md` section 1; rank 3 of 12). Reader: student-safe
after the redactions in `MANIFEST_LOCAL.md`; the whole repository is private and hand-outs wait on
Greg's confirmation of the reader split (`docs/handoff/OPEN_QUESTIONS.md` A29, A30). Written 2026-10-08.

## What this is

CTSpinoPelvic1K is a public CT dataset built from the TCIA CT COLONOGRAPHY collection (ACRIN 6664;
`results/nextpaper/ACRIN-6664_protocol.pdf`): 802 records, one per person, each with a CT and a label
volume carrying every vertebra in the field, the sacrum, both hips, both femora, thirteen ribs per side,
lumbar ribs and surgical hardware under one VerSe-native identifier scheme (`docs/release/dataset_labels.json`
for the v10 id table; the v11 scheme, with 29 retired, in `memory/scheme-bone-hardware-only.md`). It exists to ask
whether local morphology can name a vertebra at the lumbosacral junction without counting down from C2
(`memory/local-level-identity-thesis.md`), and it carries a two-reader Castellvi consensus on 34 records
for that purpose (`docs/ctsp/castellvi_consensus.csv`).

Release v11 (2026-09-18) differs from v10 in one step: the carved S1 (identifier 29), which was unreliable
(median craniocaudal extent 57.6 mm against a real segment near 30 mm; 221 of 801 carves took more than
half the sacrum; `docs/handoff/RESULTS_CATALOG.md` F.5), is dissolved back into the sacrum (26) and the id
retired (`memory/s1-carve-changed-spinopelvic.md`; `ctsp:scripts/merge_s1_into_sacrum.py`).

## Goal

Close out the public dataset so that it can be cited, used and built upon without the people who built
it:

1. the Medical Physics Dataset and Software Article corrected and resubmitted at ten published pages
   (`manuscripts/mpda/`; `TODO.md` steps 1, 3);
2. the accepted NeurIPS 2026 Evaluations and Datasets paper 3474 uploaded with zero `[pending]` slots and
   headline defects A and B fixed, not disclosed (`manuscripts/neurips_camera_ready/`; `TODO.md` step 2);
3. the release documents at v11 and the Hugging Face mirror either moved to v11 or dropped from the text
   (`docs/release/`; `TODO.md` step 4);
4. repository hygiene: no personal file at the public repository's root, no banned word in tracked
   files, every sacrum-adjacent CSV recomputed on v11 (`TODO.md` step 5).

## State on 2026-10-08

| item | state | file |
|---|---|---|
| release | v11 on Zenodo, 10.5281/zenodo.22797014, published 2026-09-18 (four documents agree; the live record was not re-checked, `OPEN_QUESTIONS.md` E7); concept DOI 10.5281/zenodo.22139642; build archive 10.5281/zenodo.22647933; CC BY-NC-SA 4.0 | `manuscripts/mpda/cover_letter.md`, `title_page.tex`; `docs/handoff/EXTRACTS.md` M6 |
| Hugging Face mirror `OpenSpineConsortium/CTSpinoPelvic1K` | still v10 with id 29 on 2026-09-27 (checked by API); its card says CC BY-NC 4.0 while Zenodo says CC BY-NC-SA 4.0 | `memory/hf-mirror-is-v10.md`; `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` item 22 |
| dataset article (Medical Physics) | returned unreviewed 2026-09-21 (abstract in the main document) and again for the supporting-information format; packet rebuilt 2026-09-25 10:34; whether that packet was uploaded, and under what number, is not recorded; arXiv v1 2609.22760 | `docs/handoff/EXTRACTS.md` M6; `manuscripts/mpda/ARXIV_SUBMISSION.md` |
| page check | `build.sh --reprint` gives 10 published pages; `CTSpinoPelvic1K_reprint_check.pdf` rebuilt 2026-10-08 09:41, by whom not recorded | `manuscripts/mpda/CTSpinoPelvic1K_reprint_check.pdf`; `OPEN_QUESTIONS.md` E6 |
| NeurIPS 3474 | accepted (poster; OpenReview D8yRWDAGQF, 2026-09-24); camera-ready working copy of 2026-09-27 has 31 pages, 134 `[pending]` slots in Appendices I and J, headline defects A and B still in the main text; the 2026-09-27 edits are uncommitted; the deadline is not recorded on disk | `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` items 16-26; `STATUS.md` F.46-F.49 |
| MLHC 2026 | rejected; never "under review" (`docs/ctsp/ROADMAP.md` still says in review: stale) | `manuscripts/mlhc_2026_rejected/`; `docs/handoff/EXTRACTS.md` M8 |
| CNS 2026 talk (2 November) | the public v12 deck is the only deck to show; whether the slides were submitted to the meeting is not recorded | `manuscripts/talks/cns2026/`; `memory/cns-deck-v2-2026-09-25.md` |
| measurements | v11 spinopelvic over 756 records: PI 52.1 +/- 11.1, SS 36.6 +/- 10.6, PT 15.5 +/- 7.9 against Veilleux 52.1 / 36.5 / 15.6 (`ctsp:morphometrics/surgical_morphometrics.csv`); four CSVs still on v10 labels | `STATUS.md` F.21, F.44 |
| grid | the only copy of the 802 CTs and v11 labels is on Ceph, batch B02 VERIFIED; the state of B02 and every other batch since is `../10_data_platform_grid/MANIFEST_GRID.md` section 2 | `MANIFEST_GRID.md` |

## Success criteria

- `build.sh --reprint` prints 10 pages with the whole build output read; `audit_ms.py`, `audit_artifacts.py`
  and `audit_pdfs.py` pass; the packet is regenerated from Windows; a manuscript number is recorded for
  the Medical Physics submission.
- The NeurIPS camera-ready has zero `[pending]` slots, defects A and B corrected in the main text, every
  table caption at most 60 words by the project counter, and is uploaded on Greg's word with the
  Croissant file and the OpenReview note.
- No release document names v10, id 29 or MLHC-in-review as current; the mirror serves v11 labels byte for
  byte against `SHA256SUMS.txt` of the v11 deposit, or the mirror sentence is gone.
- `git status` in the public repository shows no personal file; a grep for the banned word returns
  nothing; every CSV touching the sacrum carries a v11 commit.

## How this folder relates to the others

- **10_data_platform_grid** owns the Ceph migration that holds the v11 tree (B02) and the cancelled
  NeurIPS appendix chains (`neurips_v11`, `neurips_tsv3`, `neurips_spineps`); nothing here runs on the grid
  without it.
- **05_ct_morphometry_parity** owns the measurement estimators and the v11 recompute of the four v10-era
  CSVs (`STATUS.md` F.44); the four morphometry documents in `docs/ctsp/` are duplicated there by design.
- **04_openspinetoolkit** owns the ostk defects (whole-sacrum S1 fallback on v11, the canal-closing
  regression) that block any ostk-derived number in the article.
- **06_transitional_ct_census** owns the Castellvi reads, the seven disputed records and the whole-cohort
  read (CT-3); the Castellvi CSVs and `lstv_reread_queue.csv` are duplicated there by design.
- **01_carm_level_detection** and **02** are Greg-only and hold nothing this folder needs; the one C-arm
  note that lived in `ctsp:docs/` (`HANDOFF_2026-09-21_PM.md`) was not copied here (`MANIFEST_LOCAL.md`).

## Folder map

```
CLAUDE.md  README.md  MEMORY.md  STATUS.md  TODO.md
MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md
manuscripts/
  mpda/                       the dataset article: main.tex, REPRODUCE.md, PLAN.md, build.sh, make_*.py,
                              audit_*.py, bib, figures/, arxiv/, overleaf/, tools/, the compiled article,
                              reprint and reprint-check PDFs, _schehr_crossref/ (37 verified bib entries)
  mpda_as_submitted_2026-09-07/   the package as first submitted (Cover_Letter.md, PDFs, LaTeX source zip)
  mpda_as_submitted_2026-09-21/   MDPA_FINAL.pdf, the 21 September double-anonymised build
  mpda_ai_text_scans/         MDPA_AI.pdf (GPTZero scan of 2026-09-12)
  arxiv_final_draft_9_19_2026.pdf   arXiv v1 (2609.22760)
  neurips_camera_ready/       the 2026-09-27 working tree: src/neurips_2026.tex, src/appendix/ (11 tex),
                              checklist.tex, bib, CAMERA_READY_CHANGES.md, REVIEWER_CRITIQUES.*
  3474_Not_All_Spines_Are_Create.pdf   NeurIPS 3474 as reviewed
  mlhc_2026_rejected/         the MLHC 2026 PDF, its text and three rebuttals
  spinesurgct_arxiv_2026-03/  the March 2026 first draft
  nextpaper_ar_2026-09-08/    the NeurIPS draft frozen 2026-09-08 (record only)
  nextpaper_radai/            the Radiology: AI skeleton (36 \todo markers, 23 filled and 13 empty, counted 2026-10-08; never filled)
  talks/cns2026/              the public v12 deck, the 7 September draft deck, the generators and figures
docs/
  ctsp/                       the repository's docs/ (SPINOPELVIC_ESTIMATOR, LEVEL_MORPHOMETRY, OSTK_VS_EXTRACTION,
                              BODY_HEIGHT_INVESTIGATION, LABELING_GUIDE, RIB_*, RELEASE_CHECKLIST, BUILD_CHAIN,
                              CORRECTIONS, LAB_JOURNAL, ROADMAP, the Castellvi and re-read CSVs, annotation/, qc/)
  ctsp_root/                  README.md (the HF card), CLAUDE.md, STATUS.md, REVIEWERS_*.md, CITATION.cff, LICENSE,
                              NOTICE, Makefile, pyproject.toml, requirements.txt, ci.yml
  release/                    zenodo README and KNOWN_ISSUES (v10), hf_dataset_card.md, the v10 deposit sidecars
                              (manifest.json 802 records, splits_5fold.json, dataset_labels.json, SHA256SUMS.txt),
                              ITK-SNAP descriptors v4/v5/v6
  handoff/                    README, GLOSSARY, RECIPES, RESULTS_CATALOG, DATASET_USAGE, LEAKAGE, OPEN_QUESTIONS,
                              INFRASTRUCTURE (2026-10-08, whole), EXTRACTS.md, PREFIXES.md (working_notes/topic6 was removed in the final pass: Greg-only, whole in `../01_carm_level_detection/docs/handoff/working_notes/`)
                              (written for this folder: every prefix resolved to a repository, this folder or the grid)
  spinesurg_ct_nnunet/        BENCHMARK_PROTOCOL, COMPETITOR_BENCHMARK, ablations, xrsp1k_seg, data_README (old scheme)
  review_reports/             the four review-round reports of the spine and class-fix pass
  itksnap_review_2026-08/     the seven-case ITK-SNAP notes (the 0008 reasoning; "anchor at S1, count up")
  labnotebook_2026-03/        the March 2026 progress memos
  LAB_JOURNAL_2026-08-19.pdf
results/
  ctsp_results/               pseudolabel_dice/, reading_sheets/, rib_qc_v4_vs_release/, six_lumbar_readings/, pelvic_width/
  hardware_review/            README, manifests, review_log, 70 per-case hardware and geometry json
  qc/                         qc_final/ and qc_hardware/ release QC tables
  root_qc_tables/             Lumbosac.csv (readers A/B/C), lumbar_ribs, stump_rib_candidates, worklists, Path.csv
  neurips_2026-05/            bm/, audit/, ens/, pred/: the per-case evidence behind the NeurIPS numbers
  nextpaper/                  manifest.csv (1,153 rows, 2026-05-17, ids unpadded), ACRIN protocol, TCIA polyp table
  flip18_review/              blank L6 and Castellvi forms of 2026-06-11 and seven QC renders
  nextpaper_viz/              the 2026-05-31 mask-refinement review page
code/
  case_fixes/                 _review_0816/, _verify_0816/, thoracic_fix_0068/ scripts and json (volumes excluded)
  lstv_review_tool/           LSTVReviewer.py, install guide, manifest, per-token review forms
  benchmark/                  the CT competitor benchmark (cases.csv 802 records, mappings, run scripts, figs, data)
  spinesurg_scripts/ containers/ docker/   download_dataset.py, generate_5fold_splits.py, the container build
memory/                       55 notes, each with its status line (see MEMORY.md)
figures/                      spinopelvic_rotation.mp4
```

## Conventions in the documents written for this folder

`ctsp:` means a path inside the public `CTSpinoPelvic1K` repository at commit 7ddfe38; `ssn:` a path inside
the private `spinesurg-ct-nnunet` repository at 097933a; `ostk:` the public `OpenSpineToolkit` at cb43197
(`MANIFEST_CODE.md`). `HOME` is `/wsu/home/go/go24/go2432` and `$RS` is `/rs/rs_grp_oschome/go2432`
(`MANIFEST_GRID.md`). The copied HANDOFF files use the same prefixes plus `sn:` and `mem:`, defined in
`docs/handoff/README.md` section 0 as laptop folders; `docs/handoff/PREFIXES.md` resolves each one to a repository
at a named commit, to a path in this folder, or to the grid. Of the eight documents written for this folder (this
file, `CLAUDE.md`, `MEMORY.md`, `STATUS.md`, `TODO.md` and the three manifests) only `MANIFEST_LOCAL.md` carries
laptop paths, as a record of where a copy came from; the copied notes, HANDOFF files and scripts that still quote
one are listed in `MANIFEST_LOCAL.md` section 3.6 with the line to change, and nothing here depends on them.


## Added in the final pass of 2026-10-08

- `manuscripts/neurips_as_submitted_2026-05/`: the anonymised LaTeX source (`main.tex`, `bib.tex`) and PDF of the paper as it was scored and accepted as NeurIPS 2026 Evaluations and Datasets 3474; the camera-ready in `manuscripts/neurips_camera_ready/` is the later working copy.
- `manuscripts/mpda/coauthor_review/`: the co-author's revision notes with the sources behind each change, and the reviewed draft they were made on (`.docx` metadata scrubbed; `MANIFEST_LOCAL.md`, final pass). `TODO.md` step 3 reads them before the rebuild.
