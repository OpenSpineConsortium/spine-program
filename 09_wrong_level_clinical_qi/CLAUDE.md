# 09_wrong_level_clinical_qi: working context

Wrong-level spine surgery, argued clinically and measured as a process. This folder holds the three instruments of
that argument: the iliac-crest clinical paper, the wrong-level-surgery scoping review (PRISMA-ScR) and the
quality-improvement protocol manuscript "The Universal Protocol with a level in it" (SQUIRE 2.0), together with the
verified evidence briefs behind them. Its one deliverable for the rest of the programme is the per-case process form of
the QI protocol (anchor used, exposures, minutes, dose, needles, disagreement and its resolution, surgeon confidence,
level reached, transitional anatomy; `manuscripts/qi_universal_protocol/main.tex`, Table 2), which is the scaffold the
hospital test in `01_carm_level_detection` needs at its steps S5 and S8. Nothing in this folder runs a model. Every piece
starts only with Greg's go-ahead (`docs/handoff/MANUSCRIPTS.md` section 21 item 8).

**Reader: Greg-only**, for claiming and hand-outs, not for reading: every Write holder may read this folder, and a
student takes an issue here only after Greg hands it out, with a comment naming the student's login or by removing the
label `greg-first` (Greg's answer of 2026-10-12, issue #68). The QI manuscript describes the sweep from the sacrum and the persistent digital fiducial, which
are invention aspects, and stays private until Greg confirms the provisional is filed (`docs/handoff/MANUSCRIPTS.md`
section 5). The review and the clinical paper may be split into a student-safe folder once Greg names the first author
(`_plan/PLAN.md` section 3, folder 09). Built 2026-10-08 from `spinesurg-ct-nnunet` 097933a and `CTSpinoPelvic1K`
7ddfe38; the folder is one project of the private `spine-program` repository and is self-contained: what it does not
hold is on the grid (`MANIFEST_GRID.md`) or in a repository (`MANIFEST_CODE.md`).

## Read first

1. `README.md` (what this is, its state on 2026-10-08, success criteria), then `STATUS.md` (every number in hand with
   its file and its rigor mark), then `TODO.md` (what remains, in order, with gates).
2. `docs/handoff/README.md` section 5 (the ten rules as the handoff wrote them) and `docs/handoff/RESULTS_CATALOG.md`
   "How to read a row" (the status words and rigor marks).
3. `MEMORY.md`, the index of `memory/` with each note's status. A note is a dated record, not an instruction; where a
   note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win.
4. The handoff copies use path prefixes (`ssn:`, `ctsp:`, `S/`, `C/`, `~`, `$RS`): `docs/handoff/PREFIX_KEY.md` maps each
   to a repository at a commit or a grid path.

## The standing rules, in this folder's words

1. **Words.** Never the banned word, the French-derived word for where data came from; write origin, lineage, source,
   where it came from (`memory/writing-preferences.md`). No fractional version numbers: a change folds into the next
   integer version. Figure captions at most 60 words, the argument in the text (`memory/figure-captions-terse.md`).
   Plain sentences. The affiliation is the Department of General Surgery, Wayne State University School of Medicine /
   Detroit Medical Center, never Neurosurgery (`memory/user-affiliation-general-surgery.md`): the QI manuscript's
   affiliation line is wrong as written and is corrected before anything leaves (`TODO.md` step 4). Ashley Schehr is a
   person, never a product name.
2. **Every number carries its file.** A count, date, path or claim names the file it comes from; what no file records
   is written "not recorded". Say plainly what is not known.
3. **Check outside the computation.** The recurring failure in this programme is a number that is wrong but
   plausible: estimators returned finite, reasonable values from the wrong bone, the wrong surface or the wrong label
   map, and the identity PI = SS + PT held throughout (`docs/handoff/README.md` section 5 rule 3). For this folder that
   means: the iliac-crest statistic is compared against published iliac-crest level distributions by its spread, not
   its median; the review's counts are compared against human charting before any is quoted; the QI protocol's derived
   annual figures are labelled derived. Test a tidy explanation before believing it; render the mask.
4. **Labels and orientation** (binding on the one computation this folder commissions, the v11 recompute of the crest
   statistic under `05_ct_morphometry_parity`). Two label schemes exist and mixing them does not raise ("femur_left"
   resolves to T4 against the wrong map): call `ostk.labels.labels_for(volume)`, never import a fixed map
   (`memory/label-scheme-v4-vs-ostk.md`). Identifier 29, the carved S1, is retired in release v11 and dissolved into 26;
   code that gates on 29 goes with it. Case ids are zero-padded with `zfill(4)` in the release and were not in the old
   CSVs. Canonicalise to RAS to analyse; never reorient when writing a label
   (`memory/never-reorient-when-writing-labels.md`, `memory/ct-volumes-are-pir-not-ras.md`).
5. **Held out means the person was never seen** by the checkpoint or any ancestor; every quoted score goes through
   `spinesurg-ct-nnunet` `tools/eval_gate.py`; never quote the leaked banks (allspine v2, v6, v7, v8 for VerSe,
   `anchor_drr`, `vindrps`) or any number marked LEAKED, SUPERSEDED or RECORD ONLY in `docs/handoff/RESULTS_CATALOG.md`.
   The fiducial-walk numbers the QI manuscript quotes (94.5 % of 950 walks, 92.2 % of 7,405) are not catalog rows and
   are owned by `01_carm_level_detection`; they are quoted here only as the manuscript's text until 01's gate passes
   them (`STATUS.md`).
6. **Pre-register, then score.** The review's protocol is post hoc and says so (`manuscripts/scoping_review/PROTOCOL_...md`
   "Declaration"); no outcome of the review may be called pre-specified. The iliac-crest hypothesis tests are stated
   before the v11 run (`TODO.md` step 1). Manuscript numbers enter through a manifest key, never typed.
7. **The grid's login node runs nothing.** Every computation is an `sbatch` job; `sbatch -D <dir>`; `afterany`, not
   `afterok`; IPC under `/dev/shm`; large outputs on Ceph `/rs/rs_grp_oschome/go2432`, not HOME; grid bash is bash 4.2
   (`memory/no-jobs-on-login-node.md`, `memory/grid-bash-4-2-quoting.md`). Submit, estimate the wall time, write the
   job ids and the ETA down, stop (`memory/submit-and-sleep-orchestration.md`).
8. **What stays private.** SchwingNet and all level-identification code, text, figures and weights; the QI manuscript
   until the provisional is confirmed; `spinesurg-ct-nnunet` and `XRSpinoPelvic1K`. Run `spinesurg-ct-nnunet`
   `tools/disclosure_audit.py` before any talk, upload or submission (`memory/fluorocap-repo-private.md`).
9. **Data directives.** Use all of a public dataset; fix or justify every truncation in writing before a rerun; identity
   from metadata first, file name last (`memory/data-directives-2026-09-23.md`,
   `memory/no-unexplained-subsets-fix-not-disclose.md`, `memory/key-patients-from-metadata-not-filenames.md`).
10. **Network, tokens, git.** On Greg's laptop, network through `wsl -e bash -lc '...'` (`memory/wsl-for-network.md`).
    Tokens are read from files, never echoed, never on a command line; the Semantic Scholar key the review tools use
    lives in a credentials file on the grid and the laptop and is never copied (`MANIFEST_GRID.md`). In the code
    repositories this folder names, commit only when Greg asks; Greg pushes. In spine-program itself the account doing
    the work pushes only its claim branch `claude/<issue>` and the pull request merges as root `CLAUDE.md` rule 10 says. Write scripts as files and run them by path (`memory/bash-heredoc-backslashes.md`); never name a scratch
    script `numbers.py`, `io.py` or `pdb.py` (`memory/scratchpad-shadows-stdlib.md`).
11. **Personal data.** No student name or username, no researcher or personal e-mail address enters any file here; the
    copies in this folder were redacted by kind and `MANIFEST_LOCAL.md` records each redaction.

## Traps that bind this project

- **The iliac-crest number is v5-era.** "24.7 % (195 / 789) with the crest 12 mm or more above the L4-5 disc" comes
  from the v5 release QC (`docs/handoff/RESULTS_CATALOG.md` F.41, status SUPERSEDED-PENDING) and the clinical paper's
  tables were computed before the v6 hip-laterality corrections and before v11 (`docs/handoff/MANUSCRIPTS.md`
  section 11). The crest is read from the hip labels and the disc from the L4 and L5 bodies
  (`CTSpinoPelvic1K` `scripts/extract_surgical_morphometrics.py` "the lateral corridor"), so the measure touches the
  pelvis: nothing from it is quoted until it is recomputed on v11 with `labels_for`.
- **Two included counts are in circulation for the review.** The first screening pass (title only) included 665
  records; the second pass (title and abstract) included 1,933 (`results/scoping_review/titleonly/PRISMA_FLOW.json`,
  `results/scoping_review/PRISMA_FLOW.json`). The manuscript draft and the checklist still say 665 in three places and
  1,933 in two (`STATUS.md`). No number of the review has passed human charting: the 200-row validation sample has
  zero human decisions (`results/scoping_review/validation_sample.csv`).
- **The review's corpus and ledgers are on the laptop, not the grid.** `tools/review_*.py` default to `~/review`,
  `~/FluoroCap_lstv` and `~/FluoroCap_s2` in the laptop's WSL home; the data manifest records that `FluoroCap_lstv`
  "does not exist on the grid" (`MANIFEST_GRID.md`). The small result files are copied under `results/`; the corpora
  are not. Putting them on Ceph is `TODO.md` step 0.
- **Two sentences of the QI manuscript have no file.** "The encoder takes 17 ms per frame" has no result file
  (`docs/handoff/MANUSCRIPTS.md` section 5); "about fifteen minutes for fluoroscopic localization" is an unverified
  citation (`spinesurg-ct-nnunet` `docs/RSNAI_PLAN.md` line 260). Both are struck or sourced before any use.
- **A wrong-level rate is not one number.** The widely quoted 0.09 to 4.5 per 10,000 band is wrong-site surgery across
  all specialties, not a spine rate (`docs/WRONG_LEVEL_COST_EVIDENCE.md` "Verified findings"); the review's 426 reported
  rates carry seven kinds of denominator and are not pooled (`results/scoping_review/extraction_stats.json`).
- **The QI study is powered to estimate, not to detect** a change in wrong-level events, which at 0.12 % would need
  tens of thousands of cases (`manuscripts/qi_universal_protocol/main.tex` "Analysis"; `RESULTS_CATALOG.md` E.10).
  The near-miss rate is the proxy and is reported as such.
- **The prior-art naming claim can still be overturned** by three unread IEEE papers (Li 2016, Li 2017,
  ABLSpineLevelCheck 2024; `memory/registration-free-prior-art.md`; `docs/handoff/RESEARCH_DIRECTIONS.md` unknown 11).
- **The scoping review and the dataset scoping review are two different reviews.** This folder's review is of the
  wrong-level literature (`manuscripts/scoping_review/`, tools `review_*.py`). The PRISMA-ScR review of public spine
  datasets (`spinesurg-ct-nnunet` `spine_data_review/`) belongs to `10_data_platform_grid`. `~/review_pack` on the grid
  is the level-review pack of the film programme, not this review.

## Where things are

- **This folder.** `manuscripts/` (the three manuscripts; the QI one with a PRIVATE banner), `docs/` (the two evidence
  briefs; `docs/handoff/` the whole handoff of 2026-10-08 with its working notes, literature state and the status
  index of every memory note), `code/` (`review_prisma.py`, `review_stats.py`, `prior_art_wrong_level.py`, copies
  with their source commit in the header), `results/scoping_review/` (the PRISMA flow, the screening and extraction
  ledgers, the validation sample, the provisional statistics), `results/wrong_level_passages/` (the mechanism count
  over 1,678 passages), `memory/` (23 notes), `figures/` (empty: the manuscript figures are not yet drawn).
- **The grid.** HOME `/wsu/home/go/go24/go2432`, Ceph `/rs/rs_grp_oschome/go2432`. This folder owns no grid path. It
  uses the v11 labels at `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels` (the
  recompute runs under 05) and reads the fiducial-walk record under `/wsu/home/go/go24/go2432/model_night` (owned by
  01). Everything with sizes and migration state: `MANIFEST_GRID.md`.
- **Repositories.** `spinesurg-ct-nnunet` (private, `L6_Class`, 097933a): the review tools, the evidence briefs, the
  QI manuscript, the handoff. `CTSpinoPelvic1K` (public, `master`, 7ddfe38): the clinical paper and the crest
  extractors. `OpenSpineToolkit` (public, `main`, cb43197): `labels_for`. URLs, branches, commits and the files that
  matter: `MANIFEST_CODE.md`.
- **Sibling folders.** `01_carm_level_detection` (the hospital test and its regulatory folder; consumes the per-case
  form), `05_ct_morphometry_parity` (runs the v11 crest recompute), `02_transitional_naming_truth`
  (`LEVELCHECK_CLAIM.md`, the prior-art rates of catalog row B.8), `10_data_platform_grid` (the Ceph migration the
  review corpora need), `03_ctspinopelvic1k_dataset` (the release the clinical paper measures).

## How to be useful here

Check against something outside the computation. When a tidy explanation presents itself, test it before believing
it. Say plainly what is not known. Render the mask.
