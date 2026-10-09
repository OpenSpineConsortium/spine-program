# 09 Wrong-level surgery: the iliac-crest paper, the scoping review and the QI protocol

Rank 9 of 12 projects in `spine-program` (`_plan/PLAN.md` section 1). Reader: Greg-only for the QI manuscript; the
review and the clinical paper may be split into a student-safe folder once Greg names the first author. Built
2026-10-08.

## What this is

The clinical argument of the programme and its three instruments:

1. **The iliac-crest clinical paper.** "The iliac crest is an unreliable level landmark in transitional lumbosacral
   anatomy: a morphometric study of 802 screening CT examinations", target Spine Surgery and Related Research,
   "complete draft with real numbers" (`manuscripts/iliac_crest/main.tex` header; last commit 0ecbb82, 2026-08-22).
   It exists because the Medical Physics dataset article may not test hypotheses (same header). First author
   unassigned.
2. **The wrong-level-surgery scoping review.** "Wrong-level and wrong-site spine surgery: mechanisms, the imaging step
   that fails, and decision support", reported to PRISMA-ScR: a protocol dated 15 September 2026 (written after the
   searches and declared post hoc), a manuscript draft of the same date, and the PRISMA-ScR checklist, written
   against an earlier draft of the manuscript (`manuscripts/scoping_review/`; the three documents carry their own
   fractional version labels, to be renumbered to integers at the next edit, `TODO.md` step 3f). Searches ran on
   2026-09-15 over Europe PMC and Semantic Scholar; screening and a first-pass extraction are machine-made; no number
   has passed human charting (`manuscripts/scoping_review/MANUSCRIPT_wrong_level_scoping_review.md` first paragraph).
3. **The QI protocol manuscript.** "The Universal Protocol with a level in it: site marking and time-out for spine
   surgery assisted by a fluoroscopic level map: evidence, and a quality-improvement protocol", target The Joint
   Commission Journal on Quality and Patient Safety, SQUIRE 2.0, 9 pages, built 2026-09-22, about 2,400 words, two
   tables, never submitted (`docs/handoff/MANUSCRIPTS.md` section 5). Private until the provisional is filed.

Behind them: the two adversarially verified evidence briefs on the cost and the annual burden of wrong-level and
wrong-site spine surgery (`docs/WRONG_LEVEL_COST_EVIDENCE.md`, `docs/WRONG_SITE_BURDEN_EVIDENCE.md`, both
2026-09-19, three verifiers per claim), the mechanism count over 1,678 wrong-level passages from 529 works
(`results/wrong_level_passages/WRONG_LEVEL.md`), and the handoff of 2026-10-08 whole (`docs/handoff/`).

## Goal

Three publishable pieces and one instrument for the hospital test:

- a clinical paper whose numbers are recomputed on release v11 and checked against the published iliac-crest level
  distributions by spread, not median;
- a scoping review whose every number has passed two human readers, with the screen's sensitivity and specificity
  measured on the 200-record validation sample and reported;
- a QI protocol manuscript with the affiliation corrected, no sentence without a file, submitted only after Greg
  confirms the provisional and only after the hospital test's step S8 can run it;
- the per-case process form registered as the reader-protocol scaffold of `01_carm_level_detection` (S5, S8).

## State on 2026-10-08

| piece | state | file |
|---|---|---|
| iliac-crest paper | complete draft; its statistic is v5-era and touches the pelvis: SUPERSEDED-PENDING until recomputed on v11 | `STATUS.md`; `docs/handoff/RESULTS_CATALOG.md` F.41 |
| scoping review | searches done (12,294 identified, 11,980 screened, 1,933 included in the second pass; 665 in the first); validation sample of 200 unread; human charting not started; the draft still carries both included counts | `results/scoping_review/PRISMA_FLOW.json`; `STATUS.md` |
| evidence briefs | verified (votes recorded per claim); feed the QI manuscript's Table 1 and paper 1's introduction | `docs/` |
| QI manuscript | 9-page draft builds; affiliation line wrong (Neurosurgery); two sentences without a file; invention aspects inside; not submitted | `docs/handoff/MANUSCRIPTS.md` section 5; `TODO.md` step 4 |
| per-case form | written (Table 2 of the QI manuscript); not yet registered in 01's PREREG draft | `TODO.md` step 5 |
| review corpora and ledgers | on the laptop's WSL home only, not on the grid | `MANIFEST_GRID.md`; `TODO.md` step 0 |

Why the plan ranks it medium-low near term: the one number is v5-era, the review needs two human readers, and the QI
protocol cannot run before 01 reaches S8 (`_plan/PLAN.md` section 3, folder 09).

## Success criteria (pre-stated)

- **Clinical paper.** The 24.7 % and the crest-by-rib-free-count table are replaced by v11 numbers with their CSV and
  the hypothesis tests written before the run, or the paper is withdrawn from the queue (`TODO.md` step 1). The spread
  of the crest height is compared with the widest published living-cohort spread before any sentence is kept.
- **Scoping review.** Two readers chart the included set; Cohen's kappa reported; the automated screen's sensitivity
  on the validation sample is at or above 0.90 or the screen is revised and the corpus re-screened with both passes
  reported (`manuscripts/scoping_review/PROTOCOL_wrong_level_scoping_review.md` section 6); no number in the manuscript
  that did not pass human charting.
- **QI manuscript.** `disclosure_audit.py` passes; no sentence without a file; affiliation reads General Surgery;
  Greg's written go before any submission.
- **Per-case form.** It appears in `01_carm_level_detection/regulatory/PREREG.md` (the file 01's step S5 gate names;
  not yet written on 2026-10-08) and 01's PREREG cites it.

## How it relates to the other projects

- **01_carm_level_detection** consumes the per-case form at S5 and S8, owns the fiducial-walk numbers the QI
  manuscript quotes, holds the IRB determinations in its `regulatory/` folder and the latency measurement (S1) that
  would source the "17 ms" sentence.
- **05_ct_morphometry_parity** runs the v11 recompute of the crest statistic (its step 3; `_plan/PLAN.md`).
- **02_transitional_naming_truth** holds `LEVELCHECK_CLAIM.md`, the file behind the prior-art rates of catalog row B.8.
- **10_data_platform_grid** owns the Ceph migration the review corpora need and the FluoroCap batch B09.
- **03_ctspinopelvic1k_dataset** owns release v11, which the clinical paper measures.
- **Greg** decides the venue, the first author, whether the paper waits for the whole-cohort Castellvi read, and when
  the QI manuscript may leave (`TODO.md`).
