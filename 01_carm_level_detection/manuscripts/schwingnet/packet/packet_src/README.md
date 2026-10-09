# packet_src: everything in the submission packet outside the manuscript body

Prepared 2026-09-23 (20:45-21:15 EDT) and brought to final form 2026-09-24 (05:30-06:05 EDT) while the six-figure
wrap owned `main.tex`, `sections/`, `tables/`, `supplement.tex`, `NUMBERS.md`, `CLAIMS_LEDGER.md` and `refs.bib`;
nothing here edits them. The sources are here, the built documents land in `build/`, and the Packet phase wires
`build/` into `packet/` (below).

    python SchwingNet/packet_src/build_packet_src.py            # draft: exit 0 unless a number, a commit or a float is wrong
    python SchwingNet/packet_src/build_packet_src.py --strict   # submission gate: every marker, anchor, decision and hit closed
    python SchwingNet/atlas/update_cards.py && python SchwingNet/atlas/validate_cards.py

## State at 2026-09-24 (evening): paper 1 restructured, the comparison is paper 2

Greg moved the LevelCheck / surgeon comparison into a second paper (`PAPER1_SCOPE.md`; `paper2_levelcheck/MOVED_FROM_PAPER1.md`;
`REVISION_LOG3.md` section 8). Paper 1 has five figures and three tables, the title *SchwingNet: a convolutional-recurrent
network for level naming in spine surgery*, and the Registration statement "Not a clinical
trial; not registered." This folder was brought to that state in the packet pass of the same evening:

- `cover_letter.md`: the paragraph "The comparator was fixed before the result", the G6 result sentence and the Figure 6
  pointer are out (their text is kept in `MOVED_FROM_PAPER1.md` section 9); "What it does not show" states what paper 1
  states (three cross-validation patients; 35 error-free at-risk persons to certify 90 %; seven real-frame candidates, none
  verified; the comparison is a separate study). The headline numbers are the v9-lineage cells the manuscript prints.
- `front_matter.json`: `trial_registration` = "Not a clinical trial; not registered."; `levelcheck_prespecification` is marked
  paper-2 material, lists all **six** commits that touched `LEVELCHECK_MODEL.md` (d0403de added; the builder had flagged it) and
  marks every one `in_letter=false`, so the builder still checks the frozen file's history against git but requires nothing
  of the letter; `author_decisions.comparator_public_deposit` moved out of paper 1's list (kept under
  `moved_to_paper2_2026-09-24`); `title_clauses` now concerns "robust to transitional anatomy" alone.
- `numbers.json`: 38 numbers, every one re-read from `results/eval_gate/leaks/zeroshot_v9.json`,
  `results/eval_gate/closure/cv_v9/cv_v9.json` (fold cells and the det74/kfull coupling row), `results/a1.json`,
  `results/figure2/figure2_metrics.json` and `results/power/power.json`; the LevelCheck entries (82.2, 97.6, 19) and the 157
  left with the comparison.
- `statements.md`: no statement names the comparator file; edit-phase notes 4, 8 and 9 closed or moved.
- `claim2024/map.json`: `fig:levelcheck` / `tab:levelcheck` left every placement; items 2, 6, 14, 16, 18, 20, 21, 24-26,
  28, 34, 36-38 and 42 re-pointed; items 8, 11, 31-33, 36 and 39 re-anchored to the revision-5 wording.
- Draft build after the pass: **0 hard problems, 0 unresolved CLAIM anchors, 0 placement mismatches**; CLAIM 2024
  35 READY / 3 PENDING / 6 NEEDS-EDIT; 20 open author markers; 7 open author decisions; 2 anonymization hits
  (the network's name, by the author's choice; the descriptor's self-citation, allowed). `--strict` still exits 1 until
  G5 lands and the author decides.

The sections below this one describe the folder as it stood on the morning of 2026-09-24, before the restructure; they are
the record of that pass and are not rewritten. Where they name Figure 6, Table 3 = `tab_levelcheck`, the comparator
paragraph or the comparator commits in the letter, read "paper 2".

## State at 2026-09-24 06:05 EDT (tree ac77d1a + the uncommitted wrap; before the restructure)

- Draft build: **0 hard problems**, 0 unresolved CLAIM anchors, 0 anchors outside their six-figure placement; 22 open
  markers in the letter and title page (2 G6, 20 author); CLAIM 2024 27 READY / 11 PENDING / 6 NEEDS-EDIT; 4
  anonymization hits (guarantor, conflict and "sole author" still in `main.tex`; SchwingNet by the author's choice);
  **8 open author decisions**. `--strict` exits 1, as it must until G5/G6 land and the author decides.
- Counts (check_limits.py counter): body 2,961 words, abstract 247, 6 figures, 4 tables, 30 references.
- ATLAS: 0 errors, 5 warnings (the recalled RadLex identifiers).
- `supplement_technical.tex` compiles alone in the manuscript style on the grid (`texcheck/`, job 40429710,
  2026-09-24 05:53): 3 pages, both passes rc 0, 0 overfull boxes. The one LaTeX warning ("There were undefined
  references") comes from biblatex, because Biber is not run for a file with no citations. The one `\ref` resolves:
  the PDF reads "Table S1 lists", with no "??". Pages 2-3 were rendered and read.

## Files

| file | what | status |
|---|---|---|
| `front_matter.json` | every fact that identifies the author, each with its source and a `confirmed` flag; the frozen comparator file's commit history (all six commits that touched `LEVELCHECK_MODEL.md`, kept as a guard for paper 2, none printed in paper 1); the subject-overlap candidates with their evidence; `author_decisions`, the list the strict build holds on | 13 fields and 7 decisions await the author |
| `cover_letter.md` | the letter: what the study shows and does not (the comparison is a separate study, paper 2), why this journal, the anonymization decision, subject overlap, conflicts, sole submission | author markers only |
| `title_page.md` | the full title page in the journal's order; word counts filled at build time with `check_limits.py`'s own counter; ethics from the signed IRB notice; registration line "Not a clinical trial; not registered." | author markers only |
| `statements.md` | data sharing (full title page); data availability, **two code-and-weights wordings** and ethics for the anonymized manuscript; Table 1 footnote (b); ten notes for the edit phase; an evidence table for every fact | 3 author decisions |
| `numbers.json` | the 38 numbers the letter prints, each re-read from its result file at every build (v9-lineage cells since 2026-09-24 evening), plus 4 checked against the manuscript text; every one must appear in `main.tex` | all verified 2026-09-24 evening |
| `claim2024/items.json` | the 44 CLAIM 2024 items verbatim, with the 2020 crosswalk | done |
| `claim2024/map.json` | Yes/No/NA per item, status, anchors, **six-figure placement (`expect`)**, what is still owed | 27 READY, 11 PENDING, 6 NEEDS-EDIT |
| `supplement_technical.tex` | proposed supplement section for CLAIM items 9, 13, 22-25, 27, every value with its source in a comment | the edit phase decides; 2 G5 markers |
| `overlap/arXiv_2609.22760v1_CTSpinoPelvic1K.pdf` | the posted descriptor preprint, to enclose with the subject-overlap statement | done |
| `build_packet_src.py` | the builder (checks listed in its docstring) | done |
| `texcheck/` | standalone grid compile of `supplement_technical.tex` | passes |
| `build/` | `cover_letter.docx/.md`, `full_title_page.docx/.md`, `claim_checklist_2024.docx`, `CLAIM_CHECKLIST_2024.md/.json`, `BUILD_REPORT.md` | regenerated every run |

## What changed on 2026-09-24, and why

1. **The letter misattributed two fine-tuned results.** It read "Trained on public rendered CT and radiographs and
   never shown the intraoperative C-arm, it named 594 of 617 ... and 1,079 of 1,162 (92.9%) with three vertebrae in
   view". The three-body figure (`results/a4.json` det/LAT/k3) and the coupled 995 of 1,009 (`results/COUPLING.md`
   det74/kfull, from `coupling_c74/cv_fold*`) are from the fine-tuned case-grouped folds, not the zero-shot model.
   The letter now separates the zero-shot result from the fine-tuned ones, and states the day-grouped 571 (92.5%)
   beside the case-grouped 606 (98.2%). The letter's source comment forbids one clause mixing the two again.
2. **The letter named one comparator amendment of three.** `LEVELCHECK_MODEL.md` was amended before unblinding at
   1897772 (+ efab8dd), 2993f40 (section 13, accepted-frame accuracy with coverage) and b511985 (section 14, the
   automated reference standard, 24 September 05:29 EDT). The letter, the title page's registration line, the
   statements and CLAIM 42 now give all of them. The builder now reads the file's history from git and fails if an
   amendment is missing from `front_matter.json`, if a recorded time differs from git's, if a commit is not an ancestor
   of HEAD, or if the letter does not name it. The letter's dates and times come from git; none is typed.
3. **Reference standard (CLAIM 14, 16, 18).** Figure 6 and the dual-loss scoring now use `LEVELCHECK_MODEL.md` s4
   + s14. Test persons whom no person has read enter only through the automated reference: readers A-D, a consensus
   rule chosen on human-read CTSpinoPelvic1K and VerSe persons outside the test side, per-subtype PPV Wilson lower
   bound at least 0.90, frozen with its SHA-256 before unblinding. The three items now ask for that.
4. **Checkpoint lineage (CLAIM 20, 24, 26, 32; cards; supplement draft).** The sacrum detector descends from COCO
   through the render-trained `anchor_none_v2_17-1882` (not from COCO directly, as `NUMBERS.md` still says), and it
   was selected on the COBRA2026 and DeepFluoro test splits. The body detector descends from detect_v3, itself from
   COCO-pose. The plain-film naming figures are the encoder's selection split: Table 4 already says so and the cards
   do not quote them. The Figure 6 arm is planned from ImageNet on the training side of the built split
   (`results/eval_gate/LINEAGE.md`, `EVALUATORS.md`; `docs/RESUME_2026-09-22_PM.md`).
5. **The release promise is withdrawn until the author decides.** The data sharing statement promised a public
   deposit of the weights at publication. The project's own documents disagree (evidence table in `statements.md`).
   The statement now commits only to "private, available to reviewers and editors on request", and offers two
   wordings for publication.
6. **Subject overlap.** Four more of the author's works use CTSpinoPelvic1K subjects and may have to be named:
   - "Not All Spines Are Created Equal" (a NeurIPS 2026 reviewer copy, submission 3474);
   - the MLHC 2026 benchmark paper;
   - the BIBM 2026 paper;
   - the CNS 2026 abstracts.

   Each is in `front_matter.json` with its evidence and a proposed sentence; none prints until confirmed.
7. **ATLAS cards.** The updater was not idempotent. Six identical CTSpinoPelvic1K references had accumulated in each
   card, and the dataset card copied them. It is now `update_cards.py` and idempotent, and the validator fails on a
   duplicate reference. `atlas/README.md` ("What changed on 2026-09-24") lists every field changed.
8. **The ImageNet start of the level encoders is a default, not a record.** `tools/train_level_classifier.py` loads
   the torchvision ResNet-18 file only when it is cached on the node, and otherwise starts from random weights with
   no error; `--require-pretrained` exists to stop that. Two read-only grid jobs (40429822, 40429828) found:
   - the file has been in the shared home cache since 2026-09-21 18:31;
   - v9 trained from 2026-09-22 21:57, but its log (`model_night/logs/v9train_40415669.out`) starts at epoch 25, so
     it does not record the load;
   - scoring and learning-curve jobs from the same days print `pretrained=True`.

   The supplement draft says "started by the script's default ... its log does not record the load". **For the
   Figure 6 trainer** (not this workflow's to change): `slurm/fig6_train.sh` should pass `--require-pretrained` when
   it trains from ImageNet, so that the arm the paper scores has a recorded start.
9. **`results/power/power.json` changed schema under this pass** (`tools/fig_power.py`, 06:00:33, uncommitted,
   presumably the Figure 5 workflow). The builder stopped on seven hard problems, as designed. The values stand and
   the paths were re-pointed:
   - 157 is now `panel_a.crossings_n.0` (Wilson bound above 97.6 %); the exact-test n is 152;
   - 35 is `G6_level_wilson_90`;
   - the three real C-ArmLSpine L6 are under `not_drawn`, excluded from the primary analysis;
   - the old 83 COBRA calls are checked as 38 L6 + 45 T13; the file now also counts 8 sacralised-L5 calls, 91 in all;
   - the CTSpinoPelvic1K 18 is checked against Table 2.

   The file no longer draws a best-case interval for the three real persons, so the model card dropped its 43.9 %.
   **For the wrap:** the abstract's "Three persons have a real transitional exposure (best-case lower bound 43.9 %)" and
   Results' "with all 83 unread COBRA2026 calls" rest on the old schema; reconcile them with the new file (0 real
   primary persons; 91 calls, 57 supported).
10. **New checks in the builder:**
   - no self-evaluation, priority claim or regulatory pathway in the letter or title page;
   - no cited self-reference other than `ctsp1k`: `refs.bib` `schwing2026mixed` names the author and the account URL,
     and is uncited today;
   - every CLAIM item carries a six-figure placement, and anchors that land outside it are listed;
   - figure and table numbers the letter names must exist in the tree.

   Each check was confirmed to fire on a planted defect (2026-09-24):
   - 9 planted defects, all caught: an unlisted amendment, an amendment the letter omits, a wrong commit time, an
     untraced number, a float the tree lacks, "novel", a priority claim, a regulatory pathway, and a cited
     self-reference;
   - 1 false-positive guard passed: "first author" is not flagged;
   - a broken anchor printed its six-figure placement with a red re-anchor marker.

## What waits on which gate

| gate | what in this folder waits on it |
|---|---|
| G6 | the letter's result sentence (the frozen comparison per stratum, with the reference behind it) and the unblinding record (UTC time and HEAD the G6 evaluator writes; the letter's "before any held-out transitional person was scored" holds only if ecae75f and every amendment are ancestors of that HEAD and older than that time); CLAIM items 2, 14, 16, 18, 37, 38; the frozen `results/fig6/frozen/auto_reference.json` (its calibration PPV answers CLAIM 18) |
| G5 | CLAIM 20, 25, 32 (the Figure 6 arm's bank, split, ImageNet initialisation and recipe; training-partition rows); the two markers in `supplement_technical.tex` (body-detector corpus; the Figure 6 arm's manifest) |
| G0 | CLAIM 8 wording (COBRA2026 is complete on disk), 17 (labeller versions), 36 (age and sex) |
| G7 | CLAIM 42, 43: a public deposit of the frozen comparator, result files and, as decided, code and weights |
| edit phase | CLAIM 9, 13, 22, 24 (text the wrap removed; `supplement_technical.tex` has it); the Other-information paragraphs; deleting "Guarantor" and "Conflicts of interest" from the anonymized file; the comparator's amendment history in Methods and Registration; `NUMBERS.md`'s COCO line (`statements.md` EDIT_PHASE_NOTES 1-10) |
| Packet phase | re-point any RE-ANCHOR item to text inside its placement (`build/CLAIM_CHECKLIST_2024.md`, column "Expected"); wire `build/` into `packet/` (below) |

## Decisions only Greg can make (`front_matter.json` author_decisions; the strict build fails until each is closed)

1. **vindr_irb**: VinDr-SpineXR is outside IRB determination 2026-269 (PhysioNet Restricted Health Data Use Agreement).
   Its films are in the intraoperative fold banks. Obtain a determination for it and cite both, or retrain the fold
   models without VinDr.
2. **hf_mirror_v11**: the CTSpinoPelvic1K Hugging Face mirror is still v10, re-checked 2026-09-24 05:45 EDT:
   - it keeps `"29": "S1"`, which v11 retired;
   - its card licence is cc-by-nc-4.0 and its LICENSE file Apache-2.0, against Zenodo's CC BY-NC-SA 4.0;
   - its KNOWN_ISSUES has no 0533 entry.

   The 0533 CT there is repaired. Bring the mirror to v11 under one licence, or delete the mirror sentence.
3. **release_code_weights**: what is released at publication. `docs/FLAGSHIP_PLAN.md` s5 releases the weights;
   `docs/MODEL_CARD.md` 1.4 says code private and weights not released; `docs/INVENTION_DISCLOSURE.md` s9-10 leaves
   weights and university ownership to counsel. Pick `WEIGHTS_OPTION_DEPOSIT` or `WEIGHTS_OPTION_AGREEMENT` in
   `statements.md`.
4. **filing_before_submission**: the counsel-only memorandum that accompanies the invention disclosure
   (`docs/DISCLOSURE_MEMO.md` s7-8) recommends filing the provisional before submission and having counsel see the
   conflict statement first. Nothing from it enters the packet.
5. **comparator_public_deposit**: whether to deposit `LEVELCHECK_MODEL.md` publicly now, with a timestamp outside
   git, before G6 unblinds (CLAIM 42).
6. **title_clauses**: "robust to transitional anatomy" and "versus registration-assisted neurosurgeons" are
   unsupported until G6 (`CLAIMS_LEDGER.md`), and the comparator is a model, not neurosurgeons. The letter says so
   plainly. Keep or reword the title after G6.
7. **subject_overlap_list**: whether each candidate is published, in press or under consideration today:
   - NeurIPS 2026 #3474;
   - MLHC 2026;
   - BIBM 2026;
   - the CNS 2026 abstracts.

   Name each one that is, enclose its PDF, and delete the others.
8. **claim_form**: CLAIM 2024 is required. The docx at the repository root is 2020. Use the journal's 2024 form if in
   hand, else upload `build/claim_checklist_2024.docx`.

Also on the title page, each with its source in `front_matter.json`:

- the street address (University Health Center 6C, 4201 St. Antoine, or the 540 E Canfield of the old packet);
- the telephone [phone withheld], from the IRB form);
- the ORCID iD (none recorded in any workspace);
- funding, CRediT roles and acknowledgments;
- no prior presentation, no preprint of this manuscript, and sole submission.

## Facts checked for this folder (so they are not re-derived)

- **IRB.** "Notice of IRB Administrative Determination: Non-Human Participant Research":
  - WSU IRB HPR Number 2026 269, 2 September 2026, signed by the IRB Administration Office;
  - category "De-Identified Private Information";
  - project "Open Spine Consortium: Secondary Analysis of Publicly Available, De-Identified Imaging Datasets and the
    Derived Annotations, Software, and Models Produced From Them";
  - source: `CTSpinoPelvic1K-1/2026_269 ... 9.2.26.pdf`, 14 pages.
- **`LEVELCHECK_MODEL.md`.**
  - Frozen at ecae75f (2026-09-23 19:50:36 -04:00).
  - Amended before unblinding, each under its own section 9 rule: 1897772 (20:50:41, section 12), efab8dd (20:50:56,
    section 12 time wording), 2993f40 (20:58:29, section 13) and b511985 (2026-09-24 05:29:51, section 14).
  - H1-H6, the p0 values, the strata, the endpoint and the test are unchanged throughout.
  - All five commits are on origin/L6_Class and are ancestors of HEAD.
  - At b511985 no SchwingNet model had run on a G3 test person: the held f6eval 40427985 was cancelled, and its f6train
    jobs failed in 13 s (`docs/RESUME_2026-09-22_PM.md`, 05:40).
- **Descriptor.** arXiv 2609.22760 v1 is live. Zenodo record 22797014 is v11 (2026-09-18, labels only, CC BY-NC-SA 4.0)
  and was still the latest version on 2026-09-24. `paper/mpda/FROM_ARXIV.pdf` is an older 10-page build, not the posted
  version.
- **Zero-shot versus fine-tuned sources:**
  - zero-shot: `a7.json` zeroshot2 cells (594/617 lateral, 239/631 AP);
  - fine-tuned case-grouped: `a4.json` (606/617; k3 1,079/1,162; k5 647/667; k1 440/604), with the coupled call from
    `COUPLING.md` det74/kfull;
  - day-grouped: `a9.json` (0.9254 x 617 vertebrae = 571).
- **Selection.** `tools/train_level_classifier.py` keeps the epoch with the best exact accuracy on the bank's
  validation split, for every level encoder it trains.
- **Counts at build** (check_limits.py counter): body 2,961 words, abstract 247, 6 figures, 4 tables, 30 references.
  Float numbers from the tree:
  - fig:phenotypes 1, fig:embedding 2, fig:network 3, fig:exposure 4, fig:power 5, fig:levelcheck 6;
  - tab:data 1, tab:transitional 2, tab:levelcheck 3, tab:naming 4;
  - supplement: fig:flow S1, fig:contribution S2, fig:manifold S3, tab:deviceterms S1, tab:detection S2.

  First-citation order matches.

## Wiring for the Packet phase (tools/make_packet.py, not edited here)

- `build_title_page()` and `build_cover_letter()`: replace with a copy of `packet_src/build/full_title_page.docx` and
  `cover_letter.docx`. Run `build_packet_src.py --strict` first; it must exit 0.
- `build_claim_checklist()`: copy `packet_src/build/claim_checklist_2024.docx` instead of filling the 2020 form.
- `FIGS`: figure1..figure6 (`figures/figureN.png`) with labels fig:phenotypes, fig:embedding, fig:network,
  fig:exposure, fig:power, fig:levelcheck.
- `TABNUM`: tab:data 1, tab:transitional 2, tab:levelcheck 3, tab:naming 4, tab:detection "S2", tab:deviceterms "S1".
- `TABLES`: tab_corpus, tab4_transitional, tab_levelcheck, tab3_naming.
- Supplement figures: fig2_flow, fig5_contribution, fig_manifold.
- Enclose `packet_src/overlap/arXiv_2609.22760v1_CTSpinoPelvic1K.pdf` with the upload (the subject-overlap PDF), and
  the PDF of every other overlap the author confirms.
- `PACKET_README.md`: the counts and the file list from `build/BUILD_REPORT.md`.
