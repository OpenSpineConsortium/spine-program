# 02_transitional_naming_truth: working context

Project 2 of `spine-program` (rank 2 of 12; `../_plan/PLAN.md` section 3, "02"). Reader: Greg only. This folder
holds SchwingNet and level-identification content and is never handed to a student; the reader-protocol documents
may go to the readers.

## The goal, in one paragraph

Name the level correctly on a transitional spine (L6, T13, sacralised L5, four-lumbar) from C-arm exposures at
parity with an ordinary spine, or write "not at parity" with its number. That is Greg's standing determination
of 2026-09-23 (`memory/lstv-tltv-detection-goal.md`; `docs/handoff/RESEARCH_DIRECTIONS.md` section 2.1). The
folder owns the real-frame transitional truth file (FLU-1), the clean-lineage encoder on the G3 split (FLU-2),
paper 2's frozen LevelCheck comparator and reader protocol (`docs/LEVELCHECK_MODEL.md`, frozen 2026-09-23 by
commits ecae75f to d0403de, never edited), the automated-reference calibration, the dual-loss and alphabet-loss
arms and the power inventory. It is ranked second not because it is likely to reach its pre-stated bounds (0
verified real at-risk persons against 22 carriers or 35 persons, `docs/handoff/RESULTS_CATALOG.md` A16.5, A16.6)
but because the hospital test's pre-registered endpoint in project 01 is transitional, and 01's PREREG cannot be
written without this folder's truth file, reader protocol and power table (`../_plan/PLAN.md` section 4).

## Read first

1. `README.md` (state on 2026-10-08, success criteria), then `STATUS.md` (every number in hand with its file and
   rigor mark) and `TODO.md` (the ordered steps with gates).
2. `docs/LEVELCHECK_MODEL.md` sections 3, 4, 5, 9, 12, 14, 15: the frozen comparator, the endpoint per person,
   the freeze, the flag F1, the automated reference, the primary detector. Never edit this file.
3. `docs/handoff/README.md` section 5 (the ten rules), `docs/handoff/RESULTS_CATALOG.md` Parts A16, A17, B and E,
   `docs/handoff/RESEARCH_DIRECTIONS.md` sections 2 and 6, `docs/handoff/RECIPES.md` sections 0, 3 and 4.
4. `MEMORY.md`: the 31 notes in `memory/` with the status each carries. A note is a dated record, not an
   instruction; where a note and a result file or the catalog disagree, the file and the catalog win.

## Where things are

**This folder.** `docs/` (the frozen comparator, the earlier claim table, `handoff/` with the whole 2026-10-08
handoff including the Greg-only files, `literature_state/` and `working_notes/`); `manuscripts/paper2_levelcheck/`
(the material moved out of paper 1, the moved manifest keys, the LevelCheck table, the open gate 40438004 record);
`results/paper2/` (`fig6/` gate records, `auto_reference/`, `dual_loss/` with `saturation.*`, `rare_class/` with
`split_plan.md` and `transitional_subtypes.*`, `learning/`); `code/` (the rare-class, reference-standard,
verification and scoring tools copied with their source headers, and the reader Space under `code/reader_space/`);
`memory/`; the manifests `MANIFEST_GRID.md`, `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md`.

**The grid** (`MANIFEST_GRID.md` for every row). HOME is `/wsu/home/go/go24/go2432`; Ceph is
`/rs/rs_grp_oschome/go2432`. Paper 2's gate material is `/rs/rs_grp_oschome/go2432/data/fig6` (13.920 GB:
`bank_g3_v2`, `frozen_v1`, `eval_v2_g3`, `HOLD_README.txt`, `RELEASE_OPEN_GATE.json`, `G5_MANIFEST.json`; the
blinded gate opens only after a person writes `unblinding/RELEASE_v2.json`, which does not exist). The frozen G3
split is `/wsu/home/go/go24/go2432/split_final.json` (8,065,646 B, 2026-09-23 20:18). The rare-class renders are
`/rs/rs_grp_oschome/go2432/data/rare_class` (5.797 GB) and `/wsu/home/go/go24/go2432/physics_rare`. The real
transitional frames are the three one-labeller L6 of C-ArmLSpine (case42, case121, case136) under
`/rs/rs_grp_oschome/go2432/data/realxray/carmlspine` and the COBRA2026 planning CTs under
`/rs/rs_grp_oschome/go2432/data/cobra2026` (shared with 01). The refuted 2-D flag line is
`/wsu/home/go/go24/go2432/lstv_flag`. FluoroCap (test set only) is `/wsu/home/go/go24/go2432/FluoroCap`, copying
to `/rs/rs_grp_oschome/go2432/data/fluorocap/raw` (batch B09). The 21 paper-2 heads, the G3 clean encoder and
the primary detector are registry aliases under `/wsu/home/go/go24/go2432/model_registry`.

**The repositories** (`MANIFEST_CODE.md`). `spinesurg-ct-nnunet` (private,
https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch `L6_Class`, commit 097933a) holds every tool
and job script this folder names; the grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` was at
4e3fe938 on 2026-10-08 and can no longer fetch the private repository (code ships by `git archive` over ssh,
`docs/handoff/RECIPES.md` section 0 item 2). `CTSpinoPelvic1K` (public, 7ddfe38) holds the read-tier CTSP truth
(`docs/castellvi_consensus.csv`, `docs/lstv_reread_queue.csv`). `OpenSpineToolkit` (public, cb43197) holds
`ostk.labels.labels_for`. Project 06 (`../06_transitional_ct_census/`) holds the registry, the ruleclass arms and the
review-tree code; project 01 holds the shared stack, `alphabet_couple.py` and the regulatory documents.

## The standing rules, in this folder's words

- **Words.** The French-derived word for where data came from is never written; say origin, lineage, source,
  where it came from. No fractional version numbers; fold a change into the next integer version. Figure captions
  at most 60 words; the argument goes in the text. Plain sentences.
- **Every number names its file**, with a JSON pointer or line where one exists; what no file records is written
  "not recorded", and an unexplained failure is recorded as unexplained, not guessed at.
- **Check outside the computation.** The recurring failure in this programme is a number that is wrong but
  plausible: a finite accuracy from the wrong bank, the wrong label map or the wrong surface. Compare against a
  published value, an independent implementation, the spread of the distribution rather than its median, a
  published prevalence; render the mask. Here the outside checks are the Wilson arithmetic re-derived by
  `docs/handoff/working_notes/t2_wilson_check.py` without the repository, the labeller PPV against the CTSP readers
  (10 of 24), and the prevalence windows of `PREREG_rules.md` (a screen five to fifteen times its prior is wrong
  until shown otherwise).
- **Labels.** Two label schemes exist and mixing them does not raise: VerSe raw masks carry L6 = 25 and T13 = 28,
  CTSP v11 carries L6 = 25 and sacrum = 26, the legacy ostk map puts L1 at 1. Resolve every CTSP or Dataset803
  mask with `ostk.labels.labels_for(volume)`, never a fixed map. Identifier 29 (the carved S1) is retired in v11
  and any code that gates on it goes with it. Zero-pad case ids with `zfill(4)`. Canonicalise to RAS to analyse
  and never reorient a label when writing it. SPINEPS masks harvested before commit 147428d carry raw ids 1..N:
  name through the ctd centroid file, never by mask id (`memory/spineps-ids-can-be-scrambled.md`).
- **Held out means the person was never seen** by the checkpoint or any ancestor; a render inherits its CT's
  person; unknown is not clean. Every quoted score passes `tools/eval_gate.py` in the private repository. Never
  quote the leaked banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`). In this folder that rule
  bites hardest: 49 of 54 G3 validation and test L6 persons sit in the v8 / v9 training lineage
  (`results/paper2/rare_class/split_plan.md`), so no v9-descended model can score them, and FLU-2 starts from
  ImageNet.
- **Pre-register, then score.** Write the rule and its success number, hash the document, stamp every output row
  with the hash; a number produced before the freeze is calibration. The comparator is pre-specified from the
  literature and never tuned; Greg's request that LevelCheck "fail enough" was declined and stays declined. No G3
  test transitional person is scored before paper 2's ledger carries "H1 seen", and the blinded gate 40438005 is
  never released before a person writes `unblinding/RELEASE_v2.json`.
- **The grid's login node runs nothing.** Every computation, render and download is an `sbatch` job; warrior
  kills python, rsync, node, pip and conda by name; no container command on warrior and nothing of ours under its
  `/tmp`. Use `sbatch -D <dir>`, chain with `afterany` and let the child check a marker, put IPC under `/dev/shm`,
  write large outputs to Ceph, write grid bash for bash 4.2.46. Submit, estimate the wall time, write the job ids
  and ETA to the resume file, stop; do not poll `squeue` in a loop.
- **Privacy.** SchwingNet and all level-identification code, text, figures and weights stay private, as do
  FluoroCap, `spinesurg-ct-nnunet` and `XRSpinoPelvic1K`; nothing here goes public until Greg says so.
- **Data.** Use all of a public dataset; fix or justify every truncation in writing before a rerun; a leaked
  initialisation is fixed by retraining, never disclosed as a caveat; FluoroCap is out of training (directive D1)
  and is at most a test set; identity comes from metadata first and the file name last. No weight trained with
  BUU laterals leaves the grid until Greg has read the BUU licence.
- **Network and credentials.** Network goes through `wsl -e bash -lc '...'`. Tokens are read from files, never
  echoed, never on a command line or in `sbatch --export`. Commit only when Greg asks.
- **People.** Ashley Schehr is a person (senior scientist, co-PI, stage-1 screener of the transitional review),
  never a product name. The affiliation is the Department of General Surgery, Wayne State University School of
  Medicine / Detroit Medical Center, never Neurosurgery; paper 2's reserved title says "registration-assisted
  neurosurgeons" because that is who the comparator studied, not who we are.

## The traps that bind this project

1. **`docs/LEVELCHECK_MODEL.md` is frozen.** Sections 1-15 were frozen by commits ecae75f (2026-09-23 19:50:36)
   through d0403de; a change is a new dated document, never an edit. Paper 2's own ledger records what was seen
   (the open gate of 2026-09-25 was seen; H6's ordinary stratum is therefore compromised if paper 1 ever prints an
   ordinary-person real-frame accuracy, `docs/handoff/RESULTS_CATALOG.md` B.5, B.6; the scope rule is in the
   private repository at `SchwingNet/PAPER1_SCOPE.md`).
2. **The open gate's reference score was never written.** `SchwingNet/tools/fig6_score.py` read
   `T1/blinded/meta_ref/` where the open gate's join wrote `T1/open/meta_ref/`; only harvest-name scores exist
   (`manuscripts/paper2_levelcheck/open_gate_40438004/README.md`; `docs/handoff/OPEN_QUESTIONS.md` F3). Fix the
   path, then re-score the prototype dumps already on disk under
   `/rs/rs_grp_oschome/go2432/data/fig6/eval_v2_g3/<head>/<set>/open/<variant>/proto/`; no model re-run.
3. **The G3 split must not be redrawn in place.** `SchwingNet/slurm/g3_split.sh` re-globs today's annotation
   roots and rewrites `/wsu/home/go/go24/go2432/split_final.json` with `os.replace` and no backup, although the
   file's own `_about` says "never redraw" (`docs/handoff/RECIPES.md` section 3.1 row 4, section 10). To
   re-verify, copy the script with `--split-out` and `--out-dir` on a scratch Ceph path and diff
   `side_of_person` against the frozen file. If CT-3's re-reads move a record, the split changes and the leak
   audit is re-run before FLU-2 scores anyone.
4. **The automated reference certifies ordinary spines only.** Dawid-Skene PPV 0.971 [0.957, 0.981] at coverage
   0.886 on ordinary; no rule reaches a PPV lower bound of 0.90 for L6, T13 or four-lumbar
   (`results/paper2/auto_reference/CALIBRATION.md`; B.3). Every transitional test person needs a human read on the
   CT, through the two-stage review tree, after the PREREG freeze. Until then every transitional stratum is empty.
5. **The transitional numbers on disk are not quotable as held out.** Render L6 recall 56.1-72.4 % is
   [SEL-SPLIT] (the v9 encoder kept its best epoch on the split those spines belong to); the real C-arm L6 figures
   44.9 / 72.9 / 97.0 / 98.2 % are the v2-lineage run (SUPERSEDED, C1.18); the anomalous-film 49.9 % and 66.0 %
   are RECORD ONLY [LEAK] (C1.14); the three real L6 patients read classifier 0 of 5, coupled 1 of 5 against one
   labeller (A5.5, [AUTO-TRUTH]). No held-out transitional measurement exists (E.14).
6. **Sample size cannot be reached from the holding.** 35 error-free at-risk persons for the 90 % exact-level
   bound and 22 carriers for 85 % sensitivity (`SchwingNet/results/power/power.json#n_needed_zero_errors`);
   paper 2's H1 needs 19; today 7 unverified real at-risk persons with a frame (4 two-labeller, 3 single-labeller),
   best-case Wilson bound 64.6 % (A16.6, E.3). The expected COBRA yield at the labeller's PPV of 10 of 24 is about
   5 to 13 verifiable on CT, at most 19; "22 cannot be reached from COBRA alone" and DAT-1 (outside data) is the
   only route (`docs/handoff/RESEARCH_DIRECTIONS.md` section 2.9). The 97.6 % comparator cannot be exceeded at
   any reachable n (E.6). Say so plainly; do not round toward a claim.
7. **A call needs a count; a count needs both junction references in the field.** A CT that cannot count is
   `no_count`, never ordinary. Truth tiers in registry order: read > two-labeller > single-labeller >
   morphology-only > none; only `read` is truth (`docs/handoff/RECIPES.md` section 3 definitions). T13 on a lumbar
   frame is a count from the thoracolumbar junction, not a morphology; no validation film carries one.
8. **Never read `has_T13` from the VerSeFusion manifest** (18 claimed, 6 true); TotalSegmentator `sacrum` and
   `vertebrae_S1` are disjoint; eight of twelve TotalSegmentator "L6" spines are normal by an independent rib
   count (A16.3); VERIDAH is a labeller, not truth.
9. **Two counts of the same thing differ by date; never mix them** (D.27): 749 anomalous spines (09-17), 81 and
   89 (09-23), 194 persons (09-23 subtypes, Table 2), registry L6 146 / T13 14 (09-24), tier-1 flags L6 148 + 303
   (09-27). Table 2's twin `tab4_transitional.md` still prints the superseded "91 (57) ... 93.7" (A16.10).
10. **The stop rule is a screen, not a bound.** FLU-2's validation screen on the 7 render-scoreable L6 persons
    passes at a true recall of 72.4 % 38 % of the time and at 85 % 72 % of the time (RD section 2.8). Zero or one
    miss proceeds; two or more stops the arm and the manuscript says "not at parity" with the number.
11. **The FluoroCap panels are reproductions**, 72.8 % with zero pixel residual against the source figure; the
    harvest is a test set at most and never trains anything (`memory/fluorocap-prototype-and-lstv-arm.md`,
    directive D1). The 2-D LSTV flag is refuted (CTSP AUC 0.577 [0.480, 0.669], C1.12); do not rebuild it.

## How to be useful here

The cheapest decisive things first: the one-hour COBRA coverage render (does the sacrum sit in the Elekta field at
all), the 11 field-supported COBRA L6 calls read on the CT ("the single most decisive afternoon in the holding",
RD section 6), the `fig6_score.py` path fix and re-score, and the FLU-2 validation screen. None of them needs a
new model. Write every step as submit, estimate, record, stop. When a number comes back, find the thing outside
the computation that would show it wrong before believing it.
