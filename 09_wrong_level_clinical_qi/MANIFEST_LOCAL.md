# MANIFEST_LOCAL: every file copied into this folder, and every valuable file not copied

**The source paths below are history, not a dependency.** They record where each copy came from on 2026-10-08 so the
lineage is known; nothing in this folder reads them. The folder depends only on the grid paths in `MANIFEST_GRID.md`
and the repositories in `MANIFEST_CODE.md`. Prefixes: `ssn` = `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet`
(private repository, branch `L6_Class`, commit 097933a); `ctsp` = `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1`
(public repository, `master`, 7ddfe38, working tree modified); the laptop's WSL home = `/home/gschwing` (no
repository). Sizes are the source file's bytes on 2026-10-08.

## 1. How the copies were made

- Every row of `_plan/DISPOSITION.tsv` whose `project_folder` is `09_wrong_level_clinical_qi` (9 rows: 7 copy, 1
  reference, 1 exclude) is accounted for below. The HANDOFF rule (`_plan/PLAN.md` section 2 rule 3) adds the eight
  student-readable handoff files and, because this folder is Greg-only, the Greg-only handoff files whole; the memory
  rule (rule 2a and the per-project cut list) adds 22 standing-rule notes and `registration-free-prior-art`.
- **Two deviations from the row-level disposition, both recorded.** (a) `PLAN.md` section 3 folder 09 names
  `review_prisma.py`, `review_stats.py` and `prior_art_wrong_level.py` for `code/`, while DISPOSITION row ssn r144
  says "reference": both are honoured, the three are copied with their commit in the header and all twelve review
  tools are referenced in `MANIFEST_CODE.md`. (b) The review's result files on the laptop's WSL home
  (`~/review`, `~/FluoroCap_lstv/WRONG_LEVEL.*`) were in no inventory; the task says to leave nothing of value, the
  manuscript's open slots read from them, and they exist nowhere else, so the small result files and the two ledgers
  human charting needs were copied under `results/` (section 3) and the rest is referenced by path (section 4).
- **Redactions by kind, never by value**, applied to every text copy: (1) laptop paths replaced by tokens that name
  the repository and commit, the grid path, or "see MANIFEST_LOCAL.md" (`docs/handoff/PREFIX_KEY.md` resolves each
  token); (2) e-mail addresses replaced by `[e-mail withheld]`, keeping only the two institutional office addresses
  (`hpc@wayne.edu`, `IRBQuestions@wayne.edu`) and the grid login `go2432@grid.wayne.edu`; (3) student names, the
  eleven student Hugging Face usernames with their per-person annotation tally (`topic6`, lines 753-754), the one
  handle quoted beside a public co-author's name (`RECIPES.md` line 402, `topic2` line 801) and a second grid
  username replaced by a bracketed note, and the two Castellvi readers' initials removed from column names
  (`read_1_*`, `read_2_*`); (4) three telephone numbers removed from `memory/wsu-library-access-cutoff.md` (two
  library lines and the DMC Graduate Medical Education line). The tally, the two handles and the third telephone
  number were withheld on 2026-10-08 after the verifier's pass; a grep of every handle in the annotator roster over
  this folder then returned zero hits. Which files each touched is in the table.
- The banned word appears in no source file of this folder (checked by grep before copying) and in none of the
  written files.
- Three edits in copies that are not redactions: the QI manuscript's `\bibliography{../rsnai/refs}` points at
  `refs.bib` beside it; a PRIVATE banner is prepended to it; the uncited `@misc{ctsp1k}` entry of `refs.bib` has its
  14-author field trimmed to "Schwing, Gregory and Schehr, Ashley and others" (the full published list is on Zenodo
  10.5281/zenodo.22797014). The `.py` copies carry a four-line header. The memory notes carry a one-line status
  header.
- Nothing was copied from under a `.git` folder, no environment, cache, log over 2 MB, file over 25 MB, imaging data,
  weight, credential or personal file. No symlink or junction was followed.

## 2. Every file copied

| copied to | copied from (history, not a dependency) | bytes | changes made in the copy |
|---|---|---:|---|
| `code/prior_art_wrong_level.py` | spinesurg-ct-nnunet 097933a tools/prior_art_wrong_level.py (last commit 8180a63 2026-09-14) | 3,566 | header added |
| `code/review_prisma.py` | spinesurg-ct-nnunet 097933a tools/review_prisma.py (last commit 3d91ecd 2026-09-15) | 24,667 | header added |
| `code/review_stats.py` | spinesurg-ct-nnunet 097933a tools/review_stats.py (last commit 3d91ecd 2026-09-15) | 44,506 | header added |
| `docs/WRONG_LEVEL_COST_EVIDENCE.md` | spinesurg-ct-nnunet 097933a docs/WRONG_LEVEL_COST_EVIDENCE.md (last commit 980eecc 2026-09-19) | 19,631 | none (verbatim) | also copied into 01_carm_level_detection/docs/ (deliberate duplicate, PLAN.md section 2 rule 2) |
| `docs/WRONG_SITE_BURDEN_EVIDENCE.md` | spinesurg-ct-nnunet 097933a docs/WRONG_SITE_BURDEN_EVIDENCE.md (last commit e2eab64 2026-09-19) | 18,122 | none (verbatim) | also copied into 01_carm_level_detection/docs/ (deliberate duplicate, PLAN.md section 2 rule 2) |
| `docs/handoff/CONTEXT_EXPORT.md` | spinesurg-ct-nnunet 097933a HANDOFF/CONTEXT_EXPORT.md (tracked at 097933a, 2026-10-08) | 34,696 | laptop paths | Greg-only handoff file (this folder is Greg-only) |
| `docs/handoff/DATASET_USAGE.md` | spinesurg-ct-nnunet 097933a HANDOFF/DATASET_USAGE.md (tracked at 097933a, 2026-10-08) | 37,254 | none (verbatim) | student-readable handoff file |
| `docs/handoff/GLOSSARY.md` | spinesurg-ct-nnunet 097933a HANDOFF/GLOSSARY.md (tracked at 097933a, 2026-10-08) | 25,368 | none (verbatim) | student-readable handoff file |
| `docs/handoff/INFRASTRUCTURE.md` | spinesurg-ct-nnunet 097933a HANDOFF/INFRASTRUCTURE.md (tracked at 097933a, 2026-10-08) | 48,550 | laptop paths; names / usernames | student-readable handoff file |
| `docs/handoff/LEAKAGE.md` | spinesurg-ct-nnunet 097933a HANDOFF/LEAKAGE.md (tracked at 097933a, 2026-10-08) | 25,299 | none (verbatim) | student-readable handoff file |
| `docs/handoff/LITERATURE_STATE.md` | spinesurg-ct-nnunet 097933a HANDOFF/LITERATURE_STATE.md (tracked at 097933a, 2026-10-08) | 170,864 | laptop paths; e-mail addresses | Greg-only handoff file (this folder is Greg-only) |
| `docs/handoff/MANUSCRIPTS.md` | spinesurg-ct-nnunet 097933a HANDOFF/MANUSCRIPTS.md (tracked at 097933a, 2026-10-08) | 67,604 | laptop paths; names / usernames | Greg-only handoff file (this folder is Greg-only) |
| `docs/handoff/OPEN_QUESTIONS.md` | spinesurg-ct-nnunet 097933a HANDOFF/OPEN_QUESTIONS.md (tracked at 097933a, 2026-10-08) | 28,532 | none (verbatim) | student-readable handoff file |
| `docs/handoff/README.md` | spinesurg-ct-nnunet 097933a HANDOFF/README.md (tracked at 097933a, 2026-10-08) | 42,567 | laptop paths; names / usernames | student-readable handoff file |
| `docs/handoff/RECIPES.md` | spinesurg-ct-nnunet 097933a HANDOFF/RECIPES.md (tracked at 097933a, 2026-10-08) | 73,585 | laptop paths; names / usernames (line 402: one Hugging Face handle replaced by `[handle withheld]`; the co-author's name stays) | student-readable handoff file |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | spinesurg-ct-nnunet 097933a HANDOFF/RESEARCH_DIRECTIONS.md (tracked at 097933a, 2026-10-08) | 133,695 | laptop paths; e-mail addresses | Greg-only handoff file (this folder is Greg-only) |
| `docs/handoff/RESULTS_CATALOG.md` | spinesurg-ct-nnunet 097933a HANDOFF/RESULTS_CATALOG.md (tracked at 097933a, 2026-10-08) | 110,438 | laptop paths | student-readable handoff file |
| `docs/handoff/context/COPIED_AT.txt` | spinesurg-ct-nnunet 097933a HANDOFF/context/COPIED_AT.txt (the status table of every memory note) | 7,282 | laptop paths |
| `docs/handoff/context/INDEX.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/INDEX.md (the status table of every memory note) | 25,948 | none (verbatim) |
| `docs/handoff/literature_state/assemble.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/assemble.py | 2,233 | laptop paths |
| `docs/handoff/literature_state/biblio_sorted.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/biblio_sorted.py | 2,213 | none (verbatim) |
| `docs/handoff/literature_state/calc_addendum.json` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/calc_addendum.json | 308 | none (verbatim) |
| `docs/handoff/literature_state/calc_addendum.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/calc_addendum.py | 1,589 | none (verbatim) |
| `docs/handoff/literature_state/calc_review.json` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/calc_review.json | 1,381 | none (verbatim) |
| `docs/handoff/literature_state/calc_review.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/calc_review.py | 3,098 | none (verbatim) |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/dataset_landscape_by_task.md | 61,579 | laptop paths; e-mail addresses |
| `docs/handoff/literature_state/join_ranking.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/join_ranking.py | 4,319 | laptop paths |
| `docs/handoff/literature_state/power.md` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/power.md | 36,598 | laptop paths |
| `docs/handoff/literature_state/power_calc.json` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/power_calc.json | 14,819 | none (verbatim) |
| `docs/handoff/literature_state/power_calc.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/power_calc.py | 8,151 | none (verbatim) |
| `docs/handoff/literature_state/ranking_joined.csv` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/ranking_joined.csv | 23,589 | none (verbatim) |
| `docs/handoff/literature_state/t3_ratios.py` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/t3_ratios.py | 3,918 | none (verbatim) |
| `docs/handoff/literature_state/topic1_bibliography.md` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/topic1_bibliography.md | 92,083 | laptop paths |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | spinesurg-ct-nnunet 097933a HANDOFF/literature_state/topic3_size_relative_to_studies.md | 41,506 | laptop paths |
| `docs/handoff/working_notes/builders/build_context_export.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/build_context_export.py | 12,480 | laptop paths |
| `docs/handoff/working_notes/builders/build_context_index.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/build_context_index.py | 7,545 | none (verbatim) |
| `docs/handoff/working_notes/builders/check_paths.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/check_paths.py | 9,628 | laptop paths |
| `docs/handoff/working_notes/builders/check_refs.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/check_refs.py | 1,974 | none (verbatim) |
| `docs/handoff/working_notes/builders/copy_context.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/copy_context.py | 5,168 | laptop paths |
| `docs/handoff/working_notes/builders/patch_helper.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/patch_helper.py | 1,613 | laptop paths |
| `docs/handoff/working_notes/builders/refresh_context.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/builders/refresh_context.py | 6,796 | laptop paths |
| `docs/handoff/working_notes/t2_wilson_check.py` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/t2_wilson_check.py | 905 | none (verbatim) | Greg-only reader note |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic1_schwingnet_carm_results.md | 87,350 | laptop paths | Greg-only reader note |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic2_scaling_samples_anomaly_power.md | 97,413 | laptop paths; names / usernames (line 801: one Hugging Face handle replaced by `[handle withheld]`) | Greg-only reader note |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic3_dataset_usage_leakage_rsna.md | 59,464 | laptop paths | Greg-only reader note |
| `docs/handoff/working_notes/topic4_manuscripts.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic4_manuscripts.md | 87,391 | laptop paths; names / usernames | Greg-only reader note |
| `docs/handoff/working_notes/topic5_operating_here.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic5_operating_here.md | 86,160 | laptop paths; names / usernames | Greg-only reader note |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | spinesurg-ct-nnunet 097933a HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md | 96,339 | laptop paths; names / usernames (lines 753-754: the eleven-handle annotation tally replaced by a bracketed note pointing at `ctsp:morphometrics/annotation_counts.csv`; Greg's own count kept) | Greg-only reader note |
| `manuscripts/iliac_crest/iliac_crest_landmark.pdf` | CTSpinoPelvic1K 7ddfe38 paper/clinical/iliac_crest_landmark.pdf (last commit 0ecbb82 2026-08-22) | 120,963 | none (verbatim) |
| `manuscripts/iliac_crest/main.tex` | CTSpinoPelvic1K 7ddfe38 paper/clinical/main.tex (last commit 0ecbb82 2026-08-22) | 14,606 | none (verbatim) | verbatim; numbers are v5-era (SUPERSEDED-PENDING, RESULTS_CATALOG F.41) |
| `manuscripts/qi_universal_protocol/build.sh` | spinesurg-ct-nnunet 097933a paper/qi_universal_protocol/build.sh (last commit 8e4d845 2026-09-19) | 1,126 | none (verbatim) |
| `manuscripts/qi_universal_protocol/main.pdf` | built here on 2026-10-08 21:18 from the redacted `main.tex` and the `refs.bib` beside it with `build.sh` (WSL latexmk; pdfTeX, TeX Live 2026). Not a copy: the ssn working-tree PDF of 2026-09-22 12:07 (84,103 B) printed the author e-mail and was not copied (section 4) | 83,889 | built from the redacted sources: prints `[e-mail withheld]`; still prints the Neurosurgery affiliation, left as written (`TODO.md` step 4) | `build.sh` printed "pages: 9 pages", "undefined references: 0", "overfull boxes: 3"; the intermediates it wrote (`main.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`) were deleted after reading; PRIVATE |
| `manuscripts/qi_universal_protocol/main.tex` | spinesurg-ct-nnunet 097933a paper/qi_universal_protocol/main.tex (tracked; last commit d4b895e 2026-09-22) | 19,656 | e-mail addresses; bibliography path -> refs.bib beside the file; header added | PRIVATE banner; affiliation line left as written (wrong: Neurosurgery) |
| `manuscripts/qi_universal_protocol/refs.bib` | spinesurg-ct-nnunet 097933a paper/rsnai/refs.bib (last commit 180fb0f 2026-09-23; 97 entries) | 57,214 | names / usernames (the uncited @misc{ctsp1k} author list trimmed to 'and others') | the QI manuscript's bibliography, copied beside it so the folder builds alone |
| `manuscripts/scoping_review/MANUSCRIPT_wrong_level_scoping_review.md` | CTSpinoPelvic1K working tree proposals/review/MANUSCRIPT_wrong_level_scoping_review.md (gitignored, untracked at 7ddfe38; mtime 2026-09-15/16) | 34,961 | none (verbatim) | verbatim; the only copy outside the laptop |
| `manuscripts/scoping_review/PROTOCOL_wrong_level_scoping_review.md` | CTSpinoPelvic1K working tree proposals/review/PROTOCOL_wrong_level_scoping_review.md (gitignored, untracked at 7ddfe38; mtime 2026-09-15/16) | 14,463 | none (verbatim) | verbatim; the only copy outside the laptop |
| `manuscripts/scoping_review/SUPPLEMENT_1_PRISMA_ScR_checklist.md` | CTSpinoPelvic1K working tree proposals/review/SUPPLEMENT_1_PRISMA_ScR_checklist.md (gitignored, untracked at 7ddfe38; mtime 2026-09-15/16) | 5,664 | none (verbatim) | verbatim; the only copy outside the laptop |
| `memory/bash-heredoc-backslashes.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/bash-heredoc-backslashes.md (redacted copy; INDEX status CURRENT) | 1,009 | header added |
| `memory/ct-volumes-are-pir-not-ras.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/ct-volumes-are-pir-not-ras.md (redacted copy; INDEX status CURRENT) | 2,001 | header added |
| `memory/data-directives-2026-09-23.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/data-directives-2026-09-23.md (redacted copy; INDEX status CURRENT) | 2,133 | header added |
| `memory/figure-captions-terse.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/figure-captions-terse.md (redacted copy; INDEX status CURRENT) | 1,277 | header added |
| `memory/fluorocap-repo-private.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/fluorocap-repo-private.md (redacted copy; INDEX status CURRENT) | 1,422 | header added |
| `memory/grid-access.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/grid-access.md (redacted copy; INDEX status PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE section 13 rows 3-4)) | 1,342 | header added |
| `memory/grid-bash-4-2-quoting.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/grid-bash-4-2-quoting.md (redacted copy; INDEX status CURRENT (new 2026-10-08)) | 1,380 | header added |
| `memory/grid-ceph-volume-oschome.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/grid-ceph-volume-oschome.md (redacted copy; INDEX status CURRENT) | 1,283 | names / usernames; header added |
| `memory/grid-local-singularity-is-broken.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/grid-local-singularity-is-broken.md (redacted copy; INDEX status CURRENT) | 2,368 | header added |
| `memory/key-patients-from-metadata-not-filenames.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/key-patients-from-metadata-not-filenames.md (redacted copy; INDEX status CURRENT) | 2,159 | header added |
| `memory/label-scheme-v4-vs-ostk.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/label-scheme-v4-vs-ostk.md (redacted copy; INDEX status CURRENT) | 2,423 | header added |
| `memory/morphology-deformation-feasibility.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/morphology-deformation-feasibility.md (redacted copy; INDEX status CURRENT) | 2,267 | header added |
| `memory/never-reorient-when-writing-labels.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/never-reorient-when-writing-labels.md (redacted copy; INDEX status CURRENT) | 1,892 | header added |
| `memory/no-jobs-on-login-node.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/no-jobs-on-login-node.md (redacted copy; INDEX status CURRENT) | 2,148 | header added |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md (redacted copy; INDEX status CURRENT) | 2,097 | header added |
| `memory/registration-free-prior-art.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/registration-free-prior-art.md (redacted copy; INDEX status CURRENT) | 2,098 | header added |
| `memory/scratchpad-shadows-stdlib.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/scratchpad-shadows-stdlib.md (redacted copy; INDEX status CURRENT) | 1,364 | header added |
| `memory/submit-and-sleep-orchestration.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/submit-and-sleep-orchestration.md (redacted copy; INDEX status CURRENT) | 1,888 | header added |
| `memory/user-affiliation-general-surgery.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/user-affiliation-general-surgery.md (redacted copy; INDEX status CURRENT) | 1,516 | header added |
| `memory/windows-junction-worktree-trap.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/windows-junction-worktree-trap.md (redacted copy; INDEX status CURRENT) | 1,490 | laptop paths; header added |
| `memory/writing-preferences.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/writing-preferences.md (redacted copy; INDEX status CURRENT) | 788 | header added |
| `memory/wsl-for-network.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/wsl-for-network.md (redacted copy; INDEX status CURRENT) | 1,439 | header added |
| `memory/wsu-library-access-cutoff.md` | spinesurg-ct-nnunet 097933a HANDOFF/context/wsu-library-access-cutoff.md (redacted copy; INDEX status CURRENT) | 1,478 | e-mail addresses; three phone numbers (each `[phone withheld]`; the DMC Graduate Medical Education line was withheld on 2026-10-08 after the verifier's pass, the two library lines before); header added |
| `results/scoping_review/PRISMA_FLOW.json` | laptop WSL home ~/review/PRISMA_FLOW.json (2026-09-15; not in any inventory; copied 2026-10-08) | 3,180 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/PRISMA_FLOW.md` | laptop WSL home ~/review/PRISMA_FLOW.md (2026-09-15; not in any inventory; copied 2026-10-08) | 3,688 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/REVIEW_DATA.md` | laptop WSL home ~/review/REVIEW_DATA.md (2026-09-15; not in any inventory; copied 2026-10-08) | 22,037 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/REVIEW_FIGURES.md` | laptop WSL home ~/review/REVIEW_FIGURES.md (2026-09-15; not in any inventory; copied 2026-10-08) | 978 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/REVIEW_STATS.json` | laptop WSL home ~/review/REVIEW_STATS.json (2026-09-15; not in any inventory; copied 2026-10-08) | 65,112 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/REVIEW_STATS.md` | laptop WSL home ~/review/REVIEW_STATS.md (2026-09-15; not in any inventory; copied 2026-10-08) | 18,177 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/SCREEN_CHANGES.md` | laptop WSL home ~/review/SCREEN_CHANGES.md (2026-09-15; not in any inventory; copied 2026-10-08) | 20,709 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/corpus_snapshot/MANIFEST.lines` | laptop WSL home ~/review/corpus_snapshot/MANIFEST.lines (2026-09-15; not in any inventory; copied 2026-10-08) | 164 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/corpus_snapshot/MANIFEST.sha256` | laptop WSL home ~/review/corpus_snapshot/MANIFEST.sha256 (2026-09-15; not in any inventory; copied 2026-10-08) | 434 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/corpus_snapshot/MANIFEST.taken_at` | laptop WSL home ~/review/corpus_snapshot/MANIFEST.taken_at (2026-09-15; not in any inventory; copied 2026-10-08) | 21 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/criteria.json` | laptop WSL home ~/review/criteria.json (2026-09-15; not in any inventory; copied 2026-10-08) | 3,379 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/dedup_report.json` | laptop WSL home ~/review/dedup_report.json (2026-09-15; not in any inventory; copied 2026-10-08) | 93,005 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/extraction.jsonl` | laptop WSL home ~/review/extraction.jsonl (2026-09-15; not in any inventory; copied 2026-10-08) | 5,657,062 | e-mail addresses (a corresponding-author address quoted inside an abstract, replaced by [e-mail withheld]) | otherwise verbatim result file of the scoping review; the byte count is the source file's |
| `results/scoping_review/extraction_stats.json` | laptop WSL home ~/review/extraction_stats.json (2026-09-15; not in any inventory; copied 2026-10-08) | 1,960 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/figure_shortlist.csv` | laptop WSL home ~/review/figure_shortlist.csv (2026-09-15; not in any inventory; copied 2026-10-08) | 63,598 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/incidence.csv` | laptop WSL home ~/review/incidence.csv (2026-09-15; not in any inventory; copied 2026-10-08) | 3,125 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/incidence_reported.csv` | laptop WSL home ~/review/incidence_reported.csv (2026-09-15; not in any inventory; copied 2026-10-08) | 249,268 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/log_abstracts.txt` | laptop WSL home ~/review/log_abstracts.txt (2026-09-15; not in any inventory; copied 2026-10-08) | 1,418 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/prisma_flow.svg` | laptop WSL home ~/review/prisma_flow.svg (2026-09-15; not in any inventory; copied 2026-10-08) | 9,708 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/prisma_flow_simple.svg` | laptop WSL home ~/review/prisma_flow_simple.svg (2026-09-15; not in any inventory; copied 2026-10-08) | 6,815 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/review_figures.jsonl` | laptop WSL home ~/review/review_figures.jsonl (2026-09-15; not in any inventory; copied 2026-10-08) | 566,131 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/screen_changes.json` | laptop WSL home ~/review/screen_changes.json (2026-09-15; not in any inventory; copied 2026-10-08) | 1,601 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/screening.jsonl` | laptop WSL home ~/review/screening.jsonl (2026-09-15; not in any inventory; copied 2026-10-08) | 15,979,944 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/titleonly/PRISMA_FLOW.json` | laptop WSL home ~/review/titleonly/PRISMA_FLOW.json (2026-09-15; not in any inventory; copied 2026-10-08) | 3,316 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/titleonly/PRISMA_FLOW.md` | laptop WSL home ~/review/titleonly/PRISMA_FLOW.md (2026-09-15; not in any inventory; copied 2026-10-08) | 3,835 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/titleonly/extraction_stats.json` | laptop WSL home ~/review/titleonly/extraction_stats.json (2026-09-15; not in any inventory; copied 2026-10-08) | 1,971 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/titleonly/incidence.csv` | laptop WSL home ~/review/titleonly/incidence.csv (2026-09-15; not in any inventory; copied 2026-10-08) | 2,187 | none (verbatim) | verbatim result file of the scoping review |
| `results/scoping_review/validation_sample.csv` | laptop WSL home ~/review/validation_sample.csv (2026-09-15; not in any inventory; copied 2026-10-08) | 323,081 | e-mail addresses (a corresponding-author address quoted inside an abstract, replaced by [e-mail withheld]) | otherwise verbatim result file of the scoping review; the byte count is the source file's |
| `results/wrong_level_passages/WRONG_LEVEL.json` | laptop WSL home ~/FluoroCap_lstv/WRONG_LEVEL.json (2026-09-15; not in any inventory; copied 2026-10-08) | 883 | none (verbatim) | verbatim result file of the scoping review |
| `results/wrong_level_passages/WRONG_LEVEL.md` | laptop WSL home ~/FluoroCap_lstv/WRONG_LEVEL.md (2026-09-15; not in any inventory; copied 2026-10-08) | 18,067 | none (verbatim) | verbatim result file of the scoping review |
| `results/wrong_level_passages/log_passages.txt` | laptop WSL home ~/FluoroCap_lstv/log_passages.txt (2026-09-15; not in any inventory; copied 2026-10-08) | 737 | none (verbatim) | verbatim result file of the scoping review |

## 3. Files copied from the laptop's WSL home (not in any inventory)

Included in the table above with source "laptop WSL home". `~/review` (directory mtime 2026-09-15 21:46 by `stat -c %y`; its newest files, `REVIEW_STATS.json` and
`REVIEW_STATS.md`, are 21:49 by `ls -lt`) is the working folder
the review tools write by default; `~/FluoroCap_lstv` (2026-09-15 22:13) is the Europe PMC arm. What was taken:
the PRISMA flow of both passes, the criteria, the dedup report, the screening ledger (`screening.jsonl`,
15,979,944 B, 11,981 lines including the criteria row), the extraction ledger (`extraction.jsonl`, 5,657,062 B,
1,933 rows), the validation sample (200 rows, unread), the reported rates (426 rows), the figure join and shortlist,
the provisional statistics, the screen-change summary, the corpus checksum manifest, and the mechanism count over the
passages. The review's own index of these files is `results/scoping_review/REVIEW_DATA.md`.

## 4. Valuable files NOT copied, with the reason

| file | where (history) | size | reason |
|---|---|---|---|
| `paper/qi_universal_protocol/main - Copy.pdf` | ssn | 72,702 B | DISPOSITION row ssn r183, exclude: an earlier copy of the PDF (2026-09-19); the 2026-09-22 build is copied |
| `paper/qi_universal_protocol/main.pdf` (2026-09-22 12:07) | ssn working tree | 84,103 B | the gitignored build output of the unredacted tex: prints the author e-mail. Replaced here by a build from the redacted tex (section 2 row `manuscripts/qi_universal_protocol/main.pdf`) |
| `paper/qi_universal_protocol/main.aux`, `.bbl`, `.blg`, `.log`, `.fls`, `.fdb_latexmk`, `.gitignore` | ssn | 3 to 13 KB each | build intermediates, gitignored; regenerated by `build.sh` (the 2026-10-08 build's own intermediates were deleted after its counts were read) |
| the NeurIPS camera-ready recomputation scripts `crverify*.py`, `kapfce.py`, `unmerged_ranges.py`, `capcount.py`, `pagecheck.py` (`neurips_fixes/cr_apply/`) | a laptop Claude-session scratchpad under the Windows temp directory; the token `<laptop scratchpad; see MANIFEST_LOCAL.md>/<uuid>/scratchpad/...` in the handoff copies names it, and the UUID tails are session ids a reader cannot use | not sized | named by `docs/handoff/CONTEXT_EXPORT.md` line 248 and `RESULTS_CATALOG.md` F.48 as living only in that scratchpad; they belong to the NeurIPS camera-ready of `03_ctspinopelvic1k_dataset` and are copied into no folder of `spine-program` on 2026-10-08. The other tails of the same token resolve inside this folder: `directions/notes` is `docs/handoff/working_notes/topic1_*.md` to `topic6_*.md`, and `handoff/t2_wilson_check.py` is copied beside them; the proposals A, B and C of `RESEARCH_DIRECTIONS.md` line 641 are not in this folder |
| `~/review/abstracts.jsonl` | WSL home | 17,913,689 B | the fetched abstracts (9,487 records): re-fetchable by `review_abstracts.py` from the identifiers in `screening.jsonl`; goes to Ceph in `TODO.md` step 0 |
| `~/review/abstracts_done.txt` | WSL home | 374,301 B | the resumable fetch log |
| `~/review/screening_titleonly.jsonl` | WSL home | 12,280,009 B | the first (title-only) screening pass, superseded; its flow is copied (`results/scoping_review/titleonly/PRISMA_FLOW.json`) |
| `~/review/screen_changes.csv` | WSL home | 3,525,612 B | regenerated by `review_compare.py` from the two ledgers; its summary `SCREEN_CHANGES.md` and `screen_changes.json` are copied |
| `~/review/validation_sample_titleonly.csv` | WSL home | 231,388 B | the first-pass validation sample, superseded |
| `~/review/titleonly/screening.jsonl`, `extraction.jsonl`, `incidence_reported.csv`, `prisma_flow*.svg` | WSL home | 12,280,009 B; 2,245,691 B; 135,473 B | the first-pass twins of files copied for the second pass |
| `~/review/corpus_snapshot/lstv/`, `s2/` | WSL home | 25 MB | the checksummed copy of the corpus the screen ran on (`MANIFEST.sha256` is copied so the Ceph copy can be checked against it) |
| `~/FluoroCap_lstv/` (all but `WRONG_LEVEL.*`, `log_passages.txt`) | WSL home | 1.6 GB | the Europe PMC corpus: `articles.jsonl` 1,889,024 B, `passages.jsonl` 15,955,486 B, `captions_*.jsonl`, `raw/` (822 entries of panel images), `raw_hires/` (540) (`ls | wc -l` on 2026-10-08; the 824 and 542 first written here came from `ls -a` and counted `.` and `..`), `pdf_cache/`: images and a corpus, not for this repository; `TODO.md` step 0 |
| `~/FluoroCap_s2/` | WSL home | 3.6 GB | the Semantic Scholar corpus: `s2_works.jsonl` 3,949,017 B, `passages.jsonl` 2,093,752 B, `pdf/`, `pdffig/` (452 entries of images; `ls | wc -l` on 2026-10-08, the 454 first written here counted `.` and `..`); same |
| `~/FluoroCap_lstv2/` | WSL home | not sized | a second harvest round (OpenAlex, Commons, MedPix, Open-i); whether it feeds the review is not recorded; same |
| `C:/Users/grego/OneDrive/Desktop/FluoroCap_reading/`, `FluoroCap_screening/` | laptop | not sized | reader HTML pages of the FluoroCap harvest; routed to `02_transitional_naming_truth` (reference) by DISPOSITION |
| `ssn:docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md`, `PRIOR_ART_WRONG_LEVEL_SCAN.md`, `WRONG_LEVEL_AND_TRANSITIONAL.md`, `SWEEP_TIME_EVIDENCE.md`, `CONTINUANCE_2026-09-19.md` | ssn | 22,102 B; 7,188 B; 7,055 B; not sized; not sized | copied into `01_carm_level_detection/docs/` by DISPOSITION; referenced from `MANIFEST_CODE.md` (nothing is copied twice beyond the named duplicates) |
| `ssn:SchwingNet/LEVELCHECK_CLAIM.md` | ssn | not sized | the prior-art rates of catalog B.8; copied into `02_transitional_naming_truth/docs/`; private SchwingNet text |
| `ssn:docs/INVENTION_DISCLOSURE.md`, `DISCLOSURE_MEMO.md`, `provisional/`, `disclosure_audit.json`, `disclosure_forensics.json`, `disclosure_evidence/` | ssn | not sized | the invention-disclosure package: excluded from `spine-program` (`_plan/EXCLUDED.md`); referenced by path from 01 |
| `ssn:HANDOFF/GREG_ONLY/` | ssn | not sized | never copied into `spine-program` (`_plan/PLAN.md` section 2 rule 3); credential locations, personal data, the commercial stance |
| `ssn:HANDOFF/context/*.md` other than the 23 notes in `memory/` | ssn | 141 notes | the notes of other projects live in their folders; the full status table is copied (`docs/handoff/context/INDEX.md`) |
| the live memory folder and its `MEMORY.md` | laptop | not sized | never copied (rule 5 of `_plan/PLAN.md` section 2); the redacted copies with statuses are the source |
| `ctsp:morphometrics/surgical_morphometrics.csv`, `transition_morphometrics.csv`, `pelvic_shape.csv` | ctsp | not sized | tracked in the public repository at 7ddfe38 (`MANIFEST_CODE.md`); the results of `03_ctspinopelvic1k_dataset` and `05_ct_morphometry_parity` |
| `ctsp:docs/castellvi_consensus.csv` | ctsp | not sized | tracked; reader initials in its column names; owned by 03 |
| `C:/Users/grego/OneDrive/Desktop/QI101.pdf`, `QI102.pdf` | laptop | not sized | course-completion certificates, not research (`_plan/EXCLUDED.md`; `MANUSCRIPTS.md` section 5 item 4) |
| the IRB determination letters (HPR 2026-269, HPR 2026-144, the OSC public-datasets determination, the VinDr request) | laptop | not sized | regulatory documents of the hospital test: copied into `01_carm_level_detection/regulatory/` by DISPOSITION; this folder cites them from there (`TODO.md` step 9) |
| `~/.fluorocap/credentials.env` (grid and laptop) | grid HOME; WSL | never read | the Semantic Scholar key `review_abstracts.py` reads; credentials are never copied |


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Ownership of files that were duplicated in 01

`docs/WRONG_LEVEL_COST_EVIDENCE.md` and `docs/WRONG_SITE_BURDEN_EVIDENCE.md` are owned here (PLAN.md section 3, 09); 01 held byte-identical copies and removed them in the final pass, citing this folder from its `STATUS.md`.
