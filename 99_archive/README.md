# 99_archive: superseded, refuted and dormant work kept as a record

Rank 99 in `spine-program/_plan/PLAN.md` section 1: not a project to work, a record with the reason each item is here and
what replaced it. Reader: Greg only (it holds SchwingNet deck history and private draft history). State written
2026-10-08. Nothing in this folder is run.

## 1. Description

The spine programme produced, between 2026-03 and 2026-10, a line of work that was later replaced by a better bank, a
cleaner split or a different method, and a line of work that was tested and failed. Both lines matter: the first because
their numbers still sit in old documents and decks and get quoted by mistake, the second because an idea that failed once
gets rebuilt by someone who does not know. This folder holds the written record of both, with dates, the file that
carries each number, its status in the 2026-10-08 results catalog (`docs/handoff/RESULTS_CATALOG.md`) and what replaced it.

What is in it (the row ids are those of `spine-program/_plan/DISPOSITION.tsv`):

| part | what | where |
|---|---|---|
| FluoroCap | the literature harvest of published spine fluoroscopy figures: the protocol, the README, the QC of 2026-09-14, the overnight report of 2026-09-14, the pathology-source sweep (366 sources, 534 queries) and its JSON form (ssn r114, r110, carm r110) | `docs/fluorocap/`, `docs/checkpoints/FLUOROCAP_MORNING_2026-09-14.md`; the 92 harvester tools, 12 slurm chains, the frozen `benchmark/data/fluorocap_v0.1/` and the grid tree by path in `MANIFEST_CODE.md` and `MANIFEST_GRID.md` |
| dated checkpoints | the two `HANDOFF_2026-09-21_PM.md` (different files, both kept), `RESUME_2026-09-22_PM.md` (367 KB, the last session checkpoint, 2026-09-22 to 2026-09-27, banned word rewritten), `RESUME_2026-09-22.md`, `DAILY_REPORT_2026-09-22.md`, `MORNING_BRIEF_2026-09-16.md` (carm r30, r31, ctsp r13, ssn r109, r110) | `docs/checkpoints/` |
| the superseded numbers | one page listing every v2-lineage, leaked or wrong-bank number with its replacement | `SUPERSEDED_NUMBERS.md` |
| the refuted routes and rules | SDXL img2img, CUT, CycleGAN, ADDA; Star Temporal Classification; R + C = 22; the pelvic Castellvi cues; foramina counting | `STATUS.md` section 3; `memory/fluorogen-synthetic.md` |
| the talks | the AACA 2026 Tech Fair deck (one copy, ctsp r94); the CNS 2026 decks v2, v3, v9, v11 and the v10 twin by path (desk r18 to r22); the MANS teaching-talk outlines (ctsp r136); two clinical teaching decks by path (desk r31, r37) | `manuscripts/talks/`, `docs/mans_talk/`, `MANIFEST_LOCAL.md` |
| early scratch | the fifteen-step plan of 2026-05-15 (two first names struck), the May 2026 meeting agenda, one Castellvi IV example image, two plots (inv3 r6, r30); the 2026-02-14 DICOM viewer bug note and fixed JavaScript (inv3 r87, desk r30) | `docs/early_scratch_2026-05/`, `code/fuc/` |
| the handoff | the eight student-readable files of the 2026-10-08 handoff, whole; the extracts of the Greg-only sections assigned here (MANUSCRIPTS sections 4, 8, 13, 14, 18, 19; LITERATURE_STATE section 1.7); pointers to README section 11 and RESULTS_CATALOG Part C, which are inside the whole copies (mem r181, r205, r275, r333, r337, r342, r343, r347, r348) | `docs/handoff/` |
| memory | 28 notes with their status headers: the 22 standing-rule notes every folder carries and the six archive-family notes; six history-only notes by reference | `MEMORY.md`, `memory/` |
| literature | every third-party PDF kept by path with its identifier | `LITERATURE_BY_PATH.md` |
| the grid | the RSNA 2022 cervical archive (used by nothing), the annotator backup, the Multi-View-Vertebra clone, the ten documents of 2026-02-12, the loose audit scripts and the HOME job logs, the FluoroCap tree, the roots of every superseded number | `MANIFEST_GRID.md` |

## 2. Goal and success criteria

Goal: that no number from the superseded line is quoted again, and no refuted route is rebuilt without a new argument.
Success is checkable on the day it is read:

1. Every number that appears in a current manuscript, deck or page can be traced to a CURRENT row of
   `docs/handoff/RESULTS_CATALOG.md`; none traces to a row listed in `SUPERSEDED_NUMBERS.md`.
2. The stale twins that still print superseded rows (`SchwingNet/tables/tab3_naming.md` and the three `atlas/model.json`
   copies in spinesurg-ct-nnunet at 097933a; catalog A2.9, A3.11) are fixed in `01_carm_level_detection` and no new twin
   appears.
3. Every refuted route in section 4 below is either still absent from every plan, or re-opened with a written new
   argument and a pre-stated number.
4. This folder gained nothing after 2026-10-08 except further dated records and further rows in these lists.

## 3. State on 2026-10-08

- 79 files copied (7,224,703 bytes), nothing skipped, nothing over 25 MB; the copy record is `MANIFEST_LOCAL.md`.
- The FluoroCap grid tree `/wsu/home/go/go24/go2432/FluoroCap` (316 GB by `du` on 2026-09-19) was still copying to Ceph
  under migration batch B09 at 22:20 UTC on 2026-10-08, with no STATUS file (`MANIFEST_GRID.md`).
- The RSNA 2022 cervical archive is on Ceph and VERIFIED (B08; 4 files, 203,321,991,870 bytes); whether to keep or
  delete it is open (`docs/handoff/OPEN_QUESTIONS.md` A19; Greg decides).
- No human-verified FluoroCap test set exists (0 of the "about 200" panels; `docs/handoff/RESEARCH_DIRECTIONS` is not
  copied here, the row is restated in `TODO.md`).
- Four historical documents referenced from here say "Department of Neurosurgery": the Tech Fair deck title slide, the
  `paper/rsnai/main_v2.tex` title page, the QI protocol draft and the Balgrist request draft
  (`docs/handoff/MANUSCRIPTS` extract, contradiction C5). The standing affiliation is General Surgery.

## 4. The five do-not-carry-forward lists (verbatim in substance, each with its source)

1. From the C-arm hospital-path inventory of 2026-10-08 (`../_plan/inventories/carm_hospital_path.md` section 3,
   "What not to carry forward", line 214; cited by `../_plan/PLAN.md` section 3, project 01): the 98.22 % v2-lineage cross-validation; the 99 % at 35.7 % coverage; the "100 % sacrum on
   DeepFluoro" (a same-device number, `docs/checkpoints/HANDOFF_2026-09-21_PM_ctsp_audit_track.md`); any styled-corpus
   "design B beats A" sentence (seed spread of the same order; `MODEL_CARD.md` section 4.6 in spinesurg-ct-nnunet); the
   R + C = 22 rule; any guided-loop corpus number; the 734x linker speed-up as a shipped timing; CycleGAN, CUT, ADDA and
   SDXL translation (no gain in any arm).
2. From the memory-and-handoff map of 2026-10-08 (`../_plan/inventories/memory_and_handoff_map.md`, section "What a
   reader would lose if the memory folder were dropped"): the dormant lines that must not be
   repeated are FluoroCap as training data, FluoroGen img2img, the STC loss, CycleGAN translation and bespoke CT warps
   (`memory/morphology-deformation-feasibility.md`: literature first, no bespoke warp).
3. From `RESEARCH_DIRECTIONS.md` section 3 of the handoff (spinesurg-ct-nnunet 097933a): "Excluded by the record and not
   revisited without a new argument: Star Temporal Classification; CycleGAN, ADDA, CUT and SDXL restyling; decoder-named
   pseudolabels; size in millimetres as a scalar. A learned refiner as the 2-D reference is excluded too, because it
   invents pixels, 68.1 % explained against 69.3 % calibrated."
4. From `SchwingNet/NUMBERS.md` "Numbers deliberately absent" (spinesurg-ct-nnunet 097933a): any accuracy from allspine
   v2 / v6 / v7 (the film naming 99.87 % / 98.04 % of the earlier draft, the v2 head seed spread, selective prediction at
   35.7 % coverage); any VerSe accuracy from v8 and the pooled v8 figure; the render-only detector's own-domain recall
   93.48 % (anchor_drr split leak); any VinDr number (vindrps keyed per image); any millimetre from `/wsu/home/go/go24/go2432/verse_drr`; the
   pooled all-device detector (job 40415009, unfinished); the Bhattacharyya overlaps and card typicality values; the
   one-specimen DeepFluoro test column except as one cluster.
5. From `docs/handoff/RESULTS_CATALOG.md` "How to read a row" and `docs/handoff/README.md` rule 5: nothing is quoted from
   allspine v2, v6, v7, v8-for-VerSe, `anchor_drr` or `vindrps`; held out means the person was never seen.

## 5. What is superseded by what (the chains of three inventory notes, all in `../_plan/inventories/`)

From `../_plan/inventories/ctsp_repo_root_and_sibling_folders.md` section 4, "What is superseded by what":

- Repositories: `SpineSurg-CT` (April 2026, 0051074) -> the older `CTSpinoPelvic1K` clone (4fb4a62, 2026-04-28) ->
  `CTSpinoPelvic1K` master 7ddfe38 (2026-09-28). The first two are ancestors in substance and in git.
- Dataset article: `SpineSurgCT_arxiv.tex` (March) -> the MLHC 2026 submission and rebuttals (April to June; rejected) ->
  the Medical Physics article: overleaf 2026-09-04 -> overleaf 2026-09-06 / 09-10 -> submitted 2026-09-07 -> arXiv v1
  2026-09-19 -> `paper/mpda/main.tex` at 70de829, 2026-09-25 (current; owned by `03_ctspinopelvic1k_dataset`).
- NeurIPS: `NeurIPS/main.tex` (2026-05-06) -> `3474_Not_All_Spines_Are_Create.pdf` (as reviewed) ->
  `CAMERA_READY_NEURIPS/src/neurips_2026.tex` (2026-09-25, corrected 2026-09-27; working tree modified after 7ddfe38).
- IRB: the March drafts and the IRB-26-03-8648 pre-approval receipt (2026-03-30) -> HPR 2026-144 (2026-04-21) -> HPR
  2026-269 (2026-09-02) -> the two-new-protocols decision (2026-09-11 backup) -> the Protocol 1 draft of 2026-09-15 and the
  VinDr follow-up of 2026-09-25 (owned by `01_carm_level_detection/regulatory/`).
- Morphometrics tables: the Desktop `morphometrics/` of 2026-08-17 and `transition_morphometrics_OLD.csv` -> `.pre0631`
  -> `.bak` -> the tracked `morphometrics/*.csv` at 7ddfe38.
- Annotator tooling: `spinesurg-ct-annotator` (April, 1083c4f) -> `review_service/` + `reviewtool/` in CTSpinoPelvic1K.

From `../_plan/inventories/desktop_root_loose_files.md`, section "Superseded chains":

- Medical Physics PDFs: `MDPA.pdf` of 2026-09-12 -> the repository `MDPA.pdf` of 2026-09-16 -> `MDPA_FINAL.pdf` of
  2026-09-21 (the submission; owned by 03). arXiv: `CTSpinoPelvic1K_arxiv_preview.pdf` (09-07) -> `arxiv_prev.pdf` =
  `arxiv_final_draft_9_19_2026.pdf` (09-19). The three source zips and the tar.gz at the Desktop root (09-06 to 09-10) are
  older and smaller than their `paper/mpda` and `dist/` counterparts.
- `Lumbosac.csv` at the root (06-08, one reviewer) -> the repository `Lumbosac.csv` (09-04, three reviewer columns).
- `spine_study_protocol.pdf` at the root (03-30) -> `IRB/spine_study_protocol.pdf` (retitled, sponsor named).
- `AshleyBridge-6.0.0-tester-package.zip` (09-29) -> the Beethoven releases (OpenSpineConsortium/beethoven); the product
  has been Beethoven since 2026-09-29 and Ashley Schehr is a person.
- `new_repo.zip` (04-18, a scaffold of spinesurg-ct-nnunet) -> the private repository at L6_Class 097933a.
- The CNS 2026 deck lineage: `manuscripts/talks/README.md`.

From `../_plan/inventories/memory_and_handoff_map.md`, section "What is superseded by what" (the notes a builder must
not quote as current; each note's home folder is in `../_plan/DISPOSITION.tsv`):

| note | status | what replaces it |
|---|---|---|
| feasibility-claims-measured | RECORD ONLY [LEAK] | never quote its numbers (C1.14, C1.16); its claim-by-claim reading of the external report stands |
| film-ncurve-ablation-result | SUPERSEDED reading | `SchwingNet/results/coverage/film_ncurve/ablation/READ.md`: 7 of 9 cells separated, six help and one hurts (A10.6 to A10.10) |
| level-id-2d-results-2026-09-13 | RECORD ONLY | the 96.7 % is on the cervical-dominated `films_ann` bank (C1.1) |
| mixed-length-head-and-sota | LEAKED | do not quote 97.47 or 99.02; held-out film naming today is the film N-curve (A10.1 to A10.3) |
| remedies-refuted-2026-09-17 | LEAKED numbers | the refutations were not re-run on v9; the scaling curve it quotes is C2.1 |
| selective-prediction-the-honest-99 | LEAKED | the arithmetic (about 298 answered cases to certify 99 %) stands (E.9); the numbers are on the leaked v2 bank and its own test half (C1.8); no clean re-run exists (OQ C13) |
| two-mechanisms-thesis | SUPERSEDED numbers | the framing governs paper 1; its numbers are the v2-lineage run (C1.18, A3.11); current 601 / 617 = 97.4 % whole lateral (A3.1), 451 / 603 = 74.8 % one body (A3.3) |
| xr-benchmark-and-robustness-2026-09-13 | RECORD ONLY [WRONG-BANK] | the 98.7 / 99.1 / 99.4 % recurrent head is attributed to the wrong bank (C1.2; OQ F5) |
| recurrent-head-restored-2026-09-16 | DATED | the head's 99 % was on a cervical-dominated bank |
| figure-preferences-schwingnet, flagship-paper-frame, six-figure-paper-plan | PARTLY SUPERSEDED | the five-figure paper 1; Figure 6 and the LevelCheck comparison moved to paper 2 |
| grid-access | PARTLY SUPERSEDED | aliases resolve (windows-ssh-to-grid); data moved to Ceph (grid-ceph-volume-oschome) |
| hf-mirror-is-v10, zenodo-deposit | PARTLY SUPERSEDED | four documents give v11 = 10.5281/zenodo.22797014 published 2026-09-18; the Hugging Face mirror was still v10 on 2026-09-27; live state unverified (OQ E7) |
| publication-roadmap | PARTLY SUPERSEDED | history of the venue plan (copied here) |
| overnight-2026-09-15-chains, resume-2026-09-21-pm, resume-2026-09-22, resume-2026-09-22-pm, resume-2026-09-24, resume-2026-09-26-handoff | RECORD ONLY, by reference | the repository documents they point at are in `docs/checkpoints/` |

## 6. How this folder relates to the others

- `01_carm_level_detection` owns every CURRENT C-arm number and fixes the stale twins (A2.9, A3.11); it cites the
  FluoroCap documents here by path and carries `RSNAI_PLAN.md`, `RSNAI_CLAIMS.json`, `FEASIBILITY_REPRODUCE.md`,
  `paper/rsnai/` and `paper/focused/` as superseded history of its own.
- `02_transitional_naming_truth` owns the FluoroCap grid tree as test material at most (`MANIFEST_GRID.md`) and the
  decision between a 200-panel human-read test set and a written write-off (`TODO.md`).
- `03_ctspinopelvic1k_dataset` owns the MLHC 2026 submission (rejected), the CNS 2026 generators and the public v12 deck,
  the Medical Physics and NeurIPS lineages whose superseded members are listed here by path.
- `06_transitional_ct_census` owns the refuted R + C = 22 evaluation and the pelvic-cue screen as design history.
- `07_plain_film_level_id` owns the LEAKED and RECORD ONLY film notes with their replacements.
- `08_render_devices` owns the refuted translation routes' memory notes and the physics record.
- `10_data_platform_grid` owns the migration batches that move or keep every grid path named here.
- `12_website_pacs_demo` is where the `code/fuc/` viewer prototype's successor, the NiiVue PACS demo, lives.

## 7. Layout

```
99_archive/
  CLAUDE.md  README.md  MEMORY.md  STATUS.md  TODO.md  SUPERSEDED_NUMBERS.md  LITERATURE_BY_PATH.md
  MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md
  memory/                      28 notes, each with a status header line
  docs/checkpoints/            the dated handoffs, resumes, reports (2026-09-14 to 2026-09-27)
  docs/fluorocap/              FluoroCap protocol, README, QC, pathology-source sweep (md + json)
  docs/handoff/                the eight student-readable HANDOFF files + GREG_ONLY_SECTION_EXTRACTS.md
  docs/mans_talk/              the August 2026 teaching-talk outlines (md, html, txt, css, one docx)
  docs/early_scratch_2026-05/  action items, agenda, one example image, two plots
  manuscripts/talks/           TechFair_LSTV_Schwing.pptx + the deck lineage README
  code/fuc/                    the 2026-02-14 viewer bug note and fixed JavaScript
```


## Added in the final pass of 2026-10-08

- `manuscripts/talks/PRESENTATIONS_RECORD_2026-08-17.md`: the redacted record of the programme's oral and poster presentations (venue, date, placing), extracted from a laptop Word file that the inventory had misclassified; `11_students_grid_access/STATUS.md` section E cites it for the student symposium placings.
