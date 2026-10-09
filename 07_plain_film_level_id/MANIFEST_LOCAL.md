# MANIFEST_LOCAL.md: every file copied into this folder, and every valuable file that was not

**The source paths below are history, not a dependency.** They record where each copy came from on
the laptop that built this folder on 2026-10-08. Nothing in this folder depends on them; the living
copies are the repositories named in `MANIFEST_CODE.md` and the grid paths in `MANIFEST_GRID.md`. This
is the only file in the folder that names a laptop path.

Totals: **163 files copied, 17,280,151 bytes (17.3 MB)** (the builder's `copy_log.json` recorded
204 files and 80,732,741 bytes on 2026-10-08; the 2026-10-08 verification then removed the seven
`working_notes/builders/` scripts, 46,122 B, and 34 of the 37 detect_v1 renders, 63,406,545 B, recorded by
path in section 3); 3 of the 40 detect_v1 renders kept as figures; 0 files skipped for size (nothing over
25 MB was in scope); the items of section 3 recorded by path instead of copied. Every text file in the
folder was scanned for the banned word after the build and again after the verification fixes: 0 hits. Commits: `spinesurg-ct-nnunet` 097933a, `XRSpinoPelvic1K` 4f22935,
`CTSpinoPelvic1K` 7ddfe38 (working tree), `OpenSpineToolkit` cb43197; the spine-detector snapshot's
commit is not recorded.

## 1. Redactions made in the copies (by kind, never by value)

| copy | redaction | why |
|---|---|---|
| `docs/handoff/LITERATURE_STATE.md` | 23 researcher e-mail addresses replaced by `[e-mail withheld]` (the data-request contacts of section 2 and section 6) | researcher e-mail addresses are not copied; the papers' corresponding-author lines hold them |
| `docs/handoff/RESEARCH_DIRECTIONS.md`, `docs/handoff/literature_state/dataset_landscape_by_task.md` | 1 researcher e-mail each replaced by `[e-mail withheld]` | same |
| every `docs/handoff/*.md` | institutional service addresses (`hpc@wayne.edu`, `IRBQuestions@wayne.edu`) kept | help desks, not persons |
| `memory/xray-corner-detector-status.md` | a student's first name replaced by "a student" | student names are not copied; the HANDOFF copy was unredacted (`memory_and_handoff_map.md` rule) |
| `memory/wsu-library-access-cutoff.md` | the library help-desk address and phone kept | an institutional desk |
| `docs/xrspinopelvic1k/docs/dataset_card.md` | its second heading, which carried the banned word, rewritten "Origin and how it is made" | the banned word |
| every `docs/handoff/**/*.md` | literal laptop path spellings replaced by bracketed tokens: `<repo:spinesurg-ct-nnunet 097933a>`, `<repo:CTSpinoPelvic1K 7ddfe38>`, `<repo:OpenSpineToolkit cb43197>`, `<repo:XRSpinoPelvic1K 4f22935>`, `<repo:openspineconsortium.github.io>`, `<laptop:NextPaper (folders 03, 99)>`, `<laptop:ashley-bridge (Beethoven; folder 11)>`, `<laptop:Desktop>/`, `<laptop:.claude>`, `<laptop:Temp scratchpad>`, `<live memory folder; HANDOFF/context/ holds the copies>`, `<vendor folder, never read>`; the handoff's own `ssn:`, `sn:`, `ctsp:`, `ostk:`, `np:`, `mem:` prefixes are kept and resolved in `CLAUDE.md` "Prefixes in the copied documents" | no text in this folder may depend on a laptop path (the task's self-containment rule); the count of substitutions per file is in the builder's `rewrite_log.json` |
| `docs/handoff/working_notes/builders/*.py` | **removed on 2026-10-08** (verification): the seven scripts rebuild the handoff from the live memory folder on the laptop, name it by its full path, and have no bearing on plain-film work; recorded by path in section 3b | no text in this folder may depend on a laptop path; the repository copy (`HANDOFF/working_notes/builders/` at 097933a) is the one to run |
| `docs/handoff/literature_state/assemble.py` (`DOC`), `join_ranking.py` (`ROOT`) | the one laptop-path constant in each replaced by `<repo:spinesurg-ct-nnunet 097933a>` plus a three-line comment; the copies are records and do not run | same; the other `literature_state/*.py`, `*.json`, `*.csv` carry no laptop path and are byte-identical to 097933a |
| `results/spine_detector_report/assets.json` | the base64 thumbnails of `buu_0004-F-010Y0.png` and `buu_0004-F-010Y1.png` emptied; a `redacted` field added | BUU-LSPINE terms: "never redistribute its images or crops" (`DATA_MANIFEST.md` card `buu_lspine_3600`, 097933a) |
| `results/spine_detector_report/report.html` | regenerated from the redacted `assets.json` with the report's own `build_report.py` (97,343 B against the original 301,047 B); the two BUU image slots are empty, the Mendeley thumbnail stays | same |
| `regulatory/irb_amendment_47_eprotocol_checklist.md`, `regulatory/irb_amendment_47_fracture_and_level_proposal.md` | twelve student names, two radiology residents' names and two e-mail addresses withheld; the IRB coordinator's name replaced by her role; the PI of record and Greg kept; a banner states the redaction | student names, researcher e-mails and personal data are not copied; the route needs the PI |
| `results/spine_detector_report/manifest.parquet` | one column, whose name was the banned word, renamed `origin` (values untouched: `buu`, `buu_derived`, `nhanes`; 6,073 rows; rewritten with pandas 2.2.2 / pyarrow 25.0.1, so the file is 379,728 B against the source's 379,768 B); `make_assets.py` never reads that column | the banned word; the source file in the spine-detector repository keeps its column name, so a script that reads the original by that name must be told |
| `memory/wsl-for-network.md` and `docs/handoff/RECIPES.md` line 29 | the WSL mount spelling of a laptop checkout replaced by `/mnt/c/<laptop checkout of CTSpinoPelvic1K 7ddfe38>` and `/mnt/c/<laptop checkout of spinesurg-ct-nnunet 097933a>` | no text here depends on a laptop path |
| `docs/handoff/MANUSCRIPTS.md` (lines 303, 339, and the CNS 2026 abstract table at lines 415-423), `docs/handoff/README.md` (line 343), `docs/handoff/working_notes/topic4_manuscripts.md` (lines 326, 377, 464-472), `topic6_ctspinopelvic1k_and_toolkit.md` (lines 324-325, 627) | **not redacted and stated so; Greg decides** (the 2026-10-08 verification flagged it; `TODO.md` "Decisions reserved to Greg"): the author lists of the CTSpinoPelvic1K dataset article (14 authors on `ctsp:paper/mpda/title_page.tex`: Greg, Ashley Schehr and twelve students), of the accepted NeurIPS 2026 paper 3474 (two radiology residents among its five authors) and of the accepted CNS 2026 abstracts are bibliographic records of public works and stay in the copies; the same names in a regulatory personnel roster (an IRB amendment, not public) are withheld in `regulatory/`. If Greg rules the other way, the replacement text is "and twelve student co-authors (`ctsp:paper/mpda/title_page.tex`)" and "two resident co-authors (`REVIEWER_CRITIQUES.txt`)" | the task's rule admits no exception; the earlier builder kept citations as not personal data; the decision is recorded, not made here |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` line 753-754 | eleven student GitHub usernames in the annotation tally replaced by "eleven student usernames with 20 to 73 slots each [usernames withheld in this copy]"; `[handle]` and Greg kept | student usernames are not copied (the task's rule); the committed `morphometrics/annotation_counts.csv` of `CTSpinoPelvic1K` holds them |
| `memory/grid-ceph-volume-oschome.md` line 13, `docs/handoff/INFRASTRUCTURE.md` line 97, `docs/handoff/working_notes/topic5_operating_here.md` line 112 | a C&IT administrator's AccessID replaced by "the C&IT administrator" | a person's username in a repository bound for GitHub |
| `memory/windows-junction-worktree-trap.md` lines 16 and 26 | two laptop path spellings replaced by `<laptop:ashley (Beethoven; folder 11)>/extension` and `<laptop:ashley-wt (Beethoven worktrees; folder 11)>/` | the token convention of the row above; the only memory note that named a laptop path |
| `docs/xrspinopelvic1k/docs/RESULTS.md` line 93 | a bracketed "spine-program note" added after "1.15–1.20 px at L3/L4": `per_landmark_buu.csv` gives L3 1.141 px and L4 1.213 px (medians recomputed 2026-10-08) | a copied document is not silently changed; the note is marked as this folder's |
| `docs/journal.pone.0347290.pdf` | **not redacted and stated so**: the published article (PLoS One 2026, CC BY) carries its corresponding author's address as the journal printed it | a published paper copied whole as the baseline this folder compares against; altering it would alter a published document |
| `code/context_ladder.py`, `code/eval_shortcut_controls.py` | a three-line header with the source repository and commit prepended | the plan's `code/` rule |
| every `memory/*.md` | a one-line HTML comment header with the status from `HANDOFF/context/INDEX.md` prepended | the plan's memory rule |

The affiliation: none of the copied documents carries "Neurosurgery" as this folder's affiliation;
the HANDOFF files record where other documents do (`MANUSCRIPTS.md` C5).

## 2. Files copied (163)

Grouped by destination. `bytes` is the copied file's size on disk after the redactions and rewrites of
section 1 (every row re-measured on 2026-10-08 after the verification fixes; where a source size differs,
section 1 says so); `source` is the laptop path of the original (history only).

### `code/` (2 files, 142,189 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `code/context_ladder.py` | 6,541 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/context_ladder.py` | tool copy with source header (097933a) |
| `code/eval_shortcut_controls.py` | 135,648 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/eval_shortcut_controls.py` | tool copy with source header (097933a) |

### `code/review_space/` (5 files, 67,510 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `code/review_space/Dockerfile` | 624 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/review_space/Dockerfile` | student film-review Space (097933a) |
| `code/review_space/README.md` | 3,884 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/review_space/README.md` | student film-review Space (097933a) |
| `code/review_space/SPACE_README.md` | 680 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/review_space/SPACE_README.md` | student film-review Space (097933a) |
| `code/review_space/app.py` | 61,552 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/review_space/app.py` | student film-review Space (097933a) |
| `code/review_space/requirements.txt` | 770 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/review_space/requirements.txt` | student film-review Space (097933a) |

### `docs/` (1 files, 1,784,881 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `docs/journal.pone.0347290.pdf` | 1,784,881 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/journal.pone.0347290.pdf` | Bansal et al. PLoS One 2026 e0347290, the published baseline docs/RESULTS.md compares against (CC BY) |

### `docs/handoff/` (12 files, 802,804 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `docs/handoff/CONTEXT_EXPORT.md` | 34,830 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/CONTEXT_EXPORT.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/DATASET_USAGE.md` | 37,548 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/DATASET_USAGE.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/GLOSSARY.md` | 25,544 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/GLOSSARY.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/INFRASTRUCTURE.md` | 48,976 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/INFRASTRUCTURE.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/LEAKAGE.md` | 25,532 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LEAKAGE.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/LITERATURE_STATE.md` | 170,667 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/LITERATURE_STATE.md` | HANDOFF file, whole copy (2026-10-08, 097933a); 23 e-mail address(es) replaced by [e-mail withheld] |
| `docs/handoff/MANUSCRIPTS.md` | 68,464 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/MANUSCRIPTS.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/OPEN_QUESTIONS.md` | 28,746 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/OPEN_QUESTIONS.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/README.md` | 42,970 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/README.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/RECIPES.md` | 74,325 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RECIPES.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | 134,264 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESEARCH_DIRECTIONS.md` | HANDOFF file, whole copy (2026-10-08, 097933a); 1 e-mail address(es) replaced by [e-mail withheld] |
| `docs/handoff/RESULTS_CATALOG.md` | 110,938 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/RESULTS_CATALOG.md` | HANDOFF file, whole copy (2026-10-08, 097933a) |

### `docs/handoff/literature_state/` (15 files, 299,063 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `docs/handoff/literature_state/assemble.py` | 2,584 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/assemble.py` | HANDOFF/literature_state; its `DOC` constant (a laptop path) replaced by `<repo:spinesurg-ct-nnunet 097933a>` with a comment (section 1); 2,289 B at the source |
| `docs/handoff/literature_state/biblio_sorted.py` | 2,213 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/biblio_sorted.py` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/calc_addendum.json` | 308 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.json` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/calc_addendum.py` | 1,629 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_addendum.py` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/calc_review.json` | 1,381 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.json` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/calc_review.py` | 3,155 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/calc_review.py` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | 61,934 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/dataset_landscape_by_task.md` | HANDOFF/literature_state, whole copy; 1 e-mail address(es) replaced by [e-mail withheld] |
| `docs/handoff/literature_state/join_ranking.py` | 4,712 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/join_ranking.py` | HANDOFF/literature_state; its `ROOT` constant (a laptop path) replaced by `<repo:spinesurg-ct-nnunet 097933a>` with a comment (section 1); 4,418 B at the source |
| `docs/handoff/literature_state/power.md` | 36,745 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power.md` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/power_calc.json` | 14,819 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power_calc.json` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/power_calc.py` | 8,342 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/power_calc.py` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/ranking_joined.csv` | 23,589 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/ranking_joined.csv` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/t3_ratios.py` | 3,966 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/t3_ratios.py` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/topic1_bibliography.md` | 92,014 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/topic1_bibliography.md` | HANDOFF/literature_state, whole copy |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | 41,672 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/literature_state/topic3_size_relative_to_studies.md` | HANDOFF/literature_state, whole copy |

### `docs/handoff/working_notes/` (7 files, 519,774 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `docs/handoff/working_notes/t2_wilson_check.py` | 933 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/t2_wilson_check.py` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | 88,060 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic1_schwingnet_carm_results.md` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | 98,267 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic2_scaling_samples_anomaly_power.md` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | 59,925 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic3_dataset_usage_leakage_rsna.md` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 88,639 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic4_manuscripts.md` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic5_operating_here.md` | 86,664 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic5_operating_here.md` | HANDOFF/working_notes, whole copy |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 97,286 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | HANDOFF/working_notes, whole copy |

### `docs/xrspinopelvic1k/` (13 files, 342,328 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `docs/xrspinopelvic1k/CITATION.cff` | 1,655 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/CITATION.cff` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/LICENSE` | 11,514 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/LICENSE` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/README.md` | 11,412 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/README.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/annot/README.md` | 6,604 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/annot/README.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/HPC.md` | 5,906 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/HPC.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/PIPELINE.md` | 7,524 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/PIPELINE.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/RESULTS.md` | 17,085 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/RESULTS.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/ROADMAP.md` | 3,194 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/ROADMAP.md` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/dataset_card.md` | 2,081 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/dataset_card.md` | XRSpinoPelvic1K main 4f22935; 1 text substitution(s) |
| `docs/xrspinopelvic1k/docs/figures/drr_0001.png` | 112,803 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/figures/drr_0001.png` | CTSpinoPelvic1K DRR figure (CC BY-NC 4.0 lineage) |
| `docs/xrspinopelvic1k/docs/figures/drr_0003.png` | 156,745 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/figures/drr_0003.png` | CTSpinoPelvic1K DRR figure (CC BY-NC 4.0 lineage) |
| `docs/xrspinopelvic1k/docs/reader_measurements_template.csv` | 74 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/reader_measurements_template.csv` | XRSpinoPelvic1K main 4f22935 |
| `docs/xrspinopelvic1k/docs/reader_study_protocol.md` | 5,731 | `C:/Users/grego/OneDrive/Desktop/XRaySpinoPelvic1K/docs/reader_study_protocol.md` | XRSpinoPelvic1K main 4f22935 |

### `figures/buu_vs_drr/` (33 files, 2,680,787 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `figures/buu_vs_drr/fig_agreement_buu.pdf` | 21,768 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_agreement_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_agreement_buu.png` | 175,289 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_agreement_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_agreement_drr.pdf` | 60,088 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_agreement_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_agreement_drr.png` | 495,829 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_agreement_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_bland_altman_buu.pdf` | 22,922 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_bland_altman_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_bland_altman_buu.png` | 160,237 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_bland_altman_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_bland_altman_drr.pdf` | 61,008 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_bland_altman_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_bland_altman_drr.png` | 474,797 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_bland_altman_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_ced_buu.pdf` | 11,531 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_ced_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_ced_buu.png` | 65,728 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_ced_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_ced_drr.pdf` | 12,411 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_ced_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_ced_drr.png` | 75,635 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_ced_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_corner_identity_buu.pdf` | 16,769 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_corner_identity_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_corner_identity_buu.png` | 119,241 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_corner_identity_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_corner_identity_drr.pdf` | 16,694 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_corner_identity_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_corner_identity_drr.png` | 130,099 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_corner_identity_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_error_by_level_buu.pdf` | 11,027 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_error_by_level_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_error_by_level_buu.png` | 39,147 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_error_by_level_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_error_by_level_drr.pdf` | 12,836 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_error_by_level_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_error_by_level_drr.png` | 74,274 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_error_by_level_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_pi_identity_buu.pdf` | 9,281 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_pi_identity_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_pi_identity_buu.png` | 30,347 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_pi_identity_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_pi_identity_drr.pdf` | 11,227 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_pi_identity_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_pi_identity_drr.png` | 40,465 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_pi_identity_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_roussouly_buu.pdf` | 17,540 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_roussouly_buu.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_roussouly_buu.png` | 87,707 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_roussouly_buu.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_roussouly_drr.pdf` | 17,795 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_roussouly_drr.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_roussouly_drr.png` | 88,363 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_roussouly_drr.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_training_curves.pdf` | 17,065 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_training_curves.pdf` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/fig_training_curves.png` | 212,158 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/fig_training_curves.png` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/per_item_buu.csv` | 15,889 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/per_item_buu.csv` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/per_item_drr.csv` | 65,730 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/per_item_drr.csv` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |
| `figures/buu_vs_drr/summary.json` | 9,890 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/results_unified/summary.json` | unified-model agreement figures and per-item tables, BUU vs DRR (2026-08-08) |

### `memory/` (37 files, 104,701 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `memory/COPIED_AT.txt` | 2,061 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/COPIED_AT.txt` | filtered to the 36 notes |
| `memory/bash-heredoc-backslashes.md` | 1,417 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/bash-heredoc-backslashes.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/context-ladder-2d-level-experiment.md` | 2,375 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/context-ladder-2d-level-experiment.md` | memory note from HANDOFF/context/ with status header: DATED |
| `memory/ct-volumes-are-pir-not-ras.md` | 2,429 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/ct-volumes-are-pir-not-ras.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/data-directives-2026-09-23.md` | 2,550 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/data-directives-2026-09-23.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/feasibility-claims-measured.md` | 15,433 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/feasibility-claims-measured.md` | memory note from HANDOFF/context/ with status header: RECORD ONLY [LEAK] |
| `memory/figure-captions-terse.md` | 1,687 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/figure-captions-terse.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/film-ncurve-ablation-result.md` | 2,455 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/film-ncurve-ablation-result.md` | memory note from HANDOFF/context/ with status header: SUPERSEDED reading |
| `memory/fluoro-panel-gap-diagnosed.md` | 4,326 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluoro-panel-gap-diagnosed.md` | memory note from HANDOFF/context/ with status header: DORMANT |
| `memory/fluorocap-repo-private.md` | 1,835 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/fluorocap-repo-private.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/grid-access.md` | 1,944 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-access.md` | memory note from HANDOFF/context/ with status header: PARTLY SUPERSEDED (alias; data paths, INFRASTRUCTURE.md section 13 rows 3-4) |
| `memory/grid-bash-4-2-quoting.md` | 1,807 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-bash-4-2-quoting.md` | memory note from HANDOFF/context/ with status header: CURRENT (new 2026-10-08) |
| `memory/grid-ceph-volume-oschome.md` | 1,703 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-ceph-volume-oschome.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/grid-local-singularity-is-broken.md` | 2,800 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/grid-local-singularity-is-broken.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/key-patients-from-metadata-not-filenames.md` | 2,581 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/key-patients-from-metadata-not-filenames.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/label-scheme-v4-vs-ostk.md` | 2,850 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/label-scheme-v4-vs-ostk.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/level-id-2d-results-2026-09-13.md` | 2,813 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-id-2d-results-2026-09-13.md` | memory note from HANDOFF/context/ with status header: RECORD ONLY |
| `memory/level-model-bank-coverage.md` | 3,453 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/level-model-bank-coverage.md` | memory note from HANDOFF/context/ with status header: DATED |
| `memory/mixed-length-head-and-sota.md` | 4,450 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/mixed-length-head-and-sota.md` | memory note from HANDOFF/context/ with status header: LEAKED |
| `memory/morphology-deformation-feasibility.md` | 2,684 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/morphology-deformation-feasibility.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/never-reorient-when-writing-labels.md` | 2,312 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/never-reorient-when-writing-labels.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/nhanes-double-inclusion.md` | 1,958 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/nhanes-double-inclusion.md` | memory note from HANDOFF/context/ with status header: CURRENT (fixed by patient keys) |
| `memory/no-jobs-on-login-node.md` | 2,570 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-jobs-on-login-node.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | 2,516 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/recurrent-head-restored-2026-09-16.md` | 3,752 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/recurrent-head-restored-2026-09-16.md` | memory note from HANDOFF/context/ with status header: DATED |
| `memory/remedies-refuted-2026-09-17.md` | 2,590 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/remedies-refuted-2026-09-17.md` | memory note from HANDOFF/context/ with status header: LEAKED numbers |
| `memory/scratchpad-shadows-stdlib.md` | 1,774 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/scratchpad-shadows-stdlib.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/selective-prediction-the-honest-99.md` | 3,221 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/selective-prediction-the-honest-99.md` | memory note from HANDOFF/context/ with status header: LEAKED |
| `memory/stc-does-not-transfer.md` | 3,556 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/stc-does-not-transfer.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/submit-and-sleep-orchestration.md` | 2,304 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/submit-and-sleep-orchestration.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/user-affiliation-general-surgery.md` | 1,927 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/user-affiliation-general-surgery.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/windows-junction-worktree-trap.md` | 1,929 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/windows-junction-worktree-trap.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/writing-preferences.md` | 1,195 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/writing-preferences.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/wsl-for-network.md` | 1,843 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsl-for-network.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/wsu-library-access-cutoff.md` | 1,894 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/wsu-library-access-cutoff.md` | memory note from HANDOFF/context/ with status header: CURRENT |
| `memory/xr-benchmark-and-robustness-2026-09-13.md` | 3,385 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/xr-benchmark-and-robustness-2026-09-13.md` | memory note from HANDOFF/context/ with status header: RECORD ONLY [WRONG-BANK] |
| `memory/xray-corner-detector-status.md` | 2,322 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/HANDOFF/context/xray-corner-detector-status.md` | memory note from HANDOFF/context/ with status header: DATED; redacted by hand (one student first name) |

### `regulatory/` (2 files, 19,933 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `regulatory/irb_amendment_47_eprotocol_checklist.md` | 9,052 | `C:/Users/grego/OneDrive/Desktop/CTSP1K_private/proposals_backup_20260911/irb_amendment_draft.md` | amendment-47 draft; 12 roster line(s) replaced by withheld placeholders; coordinator name replaced by role; e-mails withheld |
| `regulatory/irb_amendment_47_fracture_and_level_proposal.md` | 10,881 | `C:/Users/grego/OneDrive/Desktop/CTSP1K_private/proposals_backup_20260911/xr_fracture_detector.md` | amendment-47 draft; 15 roster line(s) replaced by withheld placeholders; coordinator name replaced by role; e-mails withheld |

### `results/corner_detector_buu/` (5 files, 1,827,834 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `results/corner_detector_buu/per_landmark_buu.csv` | 438,055 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/per_landmark_buu.csv` | per-corner errors on the 301 BUU test films (2026-08-08/09) |
| `results/corner_detector_buu/pl_v8l1024.csv` | 461,273 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/pl_v8l1024.csv` | per-corner errors on the 301 BUU test films (2026-08-08/09) |
| `results/corner_detector_buu/pl_v8l640.csv` | 464,131 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/pl_v8l640.csv` | per-corner errors on the 301 BUU test films (2026-08-08/09) |
| `results/corner_detector_buu/yolo/per_landmark.csv` | 461,635 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/yolo/per_landmark.csv` | YOLO11n-pose per-corner errors, 301 BUU test films (2026-08-08) |
| `results/corner_detector_buu/yolo/summary.json` | 2,740 | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/scratchpad/yolo/summary.json` | YOLO11n-pose summary, 301 BUU test films (2026-08-08) |

### `results/lumbar_diag_2026-09-16/` (10 files, 704,985 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `results/lumbar_diag_2026-09-16/decode_by_film_pattern.json` | 476 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/decode_by_film_pattern.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_combine_eval.json` | 30,503 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_combine_eval.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_decode_depth.json` | 4,503 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_decode_depth.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_error_anatomy.json` | 260,717 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_error_anatomy.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_film_effect.json` | 185,516 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_film_effect.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_hypotheses.json` | 2,845 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_hypotheses.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/lumbar_shift_films.json` | 217,574 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/lumbar_shift_films.json` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/per_level_before_after.csv` | 1,119 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/per_level_before_after.csv` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |
| `results/lumbar_diag_2026-09-16/render/crop_stats_summary.json` | 947 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/render/crop_stats_summary.json` | crop statistics of wrong vs right crops (097933a) |
| `results/lumbar_diag_2026-09-16/shifted_films.txt` | 785 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/lumbar_diag_2026-09-16/shifted_films.txt` | mid-lumbar error diagnosis on the real-film level model, RECORD ONLY (097933a) |

### `results/spine_detector_report/` (12 files, 7,951,562 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `results/spine_detector_report/assets.json` | 80,572 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/assets.json` | base64 thumbnails of 2 BUU renders removed: buu_0004-F-010Y0.png, buu_0004-F-010Y1.png |
| `results/spine_detector_report/build_report.py` | 18,955 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/build_report.py` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/make_assets.py` | 4,765 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/make_assets.py` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/manifest.parquet` | 379,728 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/manifest.parquet` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/metrics.json` | 867 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/metrics.json` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/predictions.json` | 25,209 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/predictions.json` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/renders/mendeley_2695-F-026Y1.png` | 1,785,969 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/renders/mendeley_2695-F-026Y1.png` | detect_v1 render, Mendeley 5jdfdgp762 (CC BY) |
| `results/spine_detector_report/renders/mendeley_N26-Olisthesis-L3-4-F-52-Yrs.png` | 1,616,135 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/renders/mendeley_N26-Olisthesis-L3-4-F-52-Yrs.png` | detect_v1 render, Mendeley 5jdfdgp762 (CC BY) |
| `results/spine_detector_report/renders/nhanes_cervical_00200.png` | 3,920,253 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/renders/nhanes_cervical_00200.png` | detect_v1 render, NHANES II (public domain) |
| `results/spine_detector_report/report.html` | 97,343 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/report.html` | regenerated by build_report.py from the redacted assets.json (two BUU thumbnails removed); wrote report.html (0.10 MB) |
| `results/spine_detector_report/report.txt` | 558 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/report.txt` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |
| `results/spine_detector_report/results.csv` | 21,208 | `C:/Users/grego/OneDrive/Desktop/spine-detector/report/results.csv` | detect_v1 field report of 2026-09-02 (local snapshot, commit not recorded) |

### `results/track5_results/` (9 files, 31,800 bytes)

| destination | bytes | source (history) | note |
|---|---:|---|---|
| `results/track5_results/CROSSCHECK.txt` | 1,656 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/CROSSCHECK.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/L5_DIP.txt` | 2,320 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/L5_DIP.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/REPORT.txt` | 9,198 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/REPORT.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/REPORT_all2.txt` | 3,463 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/REPORT_all2.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/bank_audit_allspine_v2.txt` | 5,421 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/bank_audit_allspine_v2.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/bank_audit_films_all2.txt` | 4,168 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/bank_audit_films_all2.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/bank_audit_films_ann.txt` | 3,333 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/bank_audit_films_ann.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/frozen_sha.txt` | 540 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/frozen_sha.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |
| `results/track5_results/transitional_class_sources.txt` | 1,701 | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/track5_results/transitional_class_sources.txt` | Track 5 band-transfer report, RECORD ONLY [WRONG-BANK] (097933a) |

### Documents written by the builder (not copies)

`CLAUDE.md`, `README.md`, `MEMORY.md`, `MANIFEST_GRID.md`, `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md`, `TODO.md`, `STATUS.md`, `regulatory/README.md`, `results/README.md`, `memory/COPIED_AT.txt (filtered)`.

## 3. Valuable files not copied, with the reason

### 3a. Left on their source paths: BUU-LSPINE film pixels, other non-copyable content, and the full-resolution renders the size rule excludes

BUU-LSPINE terms (`DATA_MANIFEST.md` card `buu_lspine_3600`): "No License Provided" plus an end-user
licence agreement; recorded as not open; "never redistribute its images or crops"; terms for derived
labels not addressed in any file read, so treated as non-redistributable. Greg's licence reading
(`TODO.md` step 3) may unlock these. Each regenerates from the grid: the detect_v1 renders from
`/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1` with `src/render_prediction.py`; the
best / worst overlays from the XRSpinoPelvic1K evaluators; the montages from
`spinesurg-ct-nnunet` `tools/lumbar_*.py` over the (deleted) allspine_v2 bank.

| item | bytes | reason |
|---|---|---|
| `phase0_buu_hip_fov.png` (in `docs/figures/`) | 533,183 | BUU-LSPINE film pixels (overlay figure); BUU terms forbid redistribution of its images; tracked in XRSpinoPelvic1K 4f22935 docs/figures/ |
| `phase0_buu_overlay20.png` (in `docs/figures/`) | 1,699,281 | BUU-LSPINE film pixels (overlay figure); BUU terms forbid redistribution of its images; tracked in XRSpinoPelvic1K 4f22935 docs/figures/ |
| `buu_0004-F-010Y0.png` (in `report/renders/`) | 3,293,905 | BUU-LSPINE film render (film pixels); BUU terms forbid redistribution; regenerate from ~/spine-detector/runs/detect_v1 with src/render_prediction.py |
| `buu_0004-F-010Y1.png` (in `report/renders/`) | 1,906,436 | BUU-LSPINE film render (film pixels); BUU terms forbid redistribution; regenerate from ~/spine-detector/runs/detect_v1 with src/render_prediction.py |
| `buu_0019-F-015Y0.png` (in `report/renders/`) | 2,832,343 | BUU-LSPINE film render (film pixels); BUU terms forbid redistribution; regenerate from ~/spine-detector/runs/detect_v1 with src/render_prediction.py |
| `mendeley_2742-M-073Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,147,027 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_2783-M-046Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,614,099 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_2786-F-053Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,507,092 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_2822-F-055Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,376,509 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_2834-M-019Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,393,691 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3070-F-088Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,287,773 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3100-F-056Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,560,749 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3129-M-041Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,720,964 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3142-M-079Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,956,801 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3143-F-053Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,089,788 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3149-F-044Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,740,698 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3189-F-073Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,574,145 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3203-F-046Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,677,827 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3209-F-073Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,047,901 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3210-M-067Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,494,966 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3232-F-059Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,685,945 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3246-M-051Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,628,312 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3278-F-054Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,455,270 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3290-F-046Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,667,171 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3293-M-026Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,352,100 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3296-F-070Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,448,389 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3310-F-053Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,522,333 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3311-M-044Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 2,003,579 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3332-M-026Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,650,172 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3360-F-073Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,567,452 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3370-F-024Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,496,648 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3411-F-074Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,613,800 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_3447-F-040Y1.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,856,690 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_N27-Olisthesis-L4-5-M-61-Yrs.png` (in `report/renders/`; was copied, removed 2026-10-08) | 1,738,902 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_N48-Olisthesis-L3-4-L4-5-L5-S1-F-55-Yrs.png` (in `report/renders/`; was copied, removed 2026-10-08) | 3,657,616 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_f4dd04fb042aa0f4f7249283bc3972d8.png` (in `report/renders/`; was copied, removed 2026-10-08) | 932,644 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `mendeley_fd71e4535c5fd16c32096670c8984022.png` (in `report/renders/`; was copied, removed 2026-10-08) | 974,679 | full-resolution (2048 px) detect_v1 render of a patient radiograph, Mendeley 5jdfdgp762 (CC BY): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `nhanes_cervical_00321.png` (in `report/renders/`; was copied, removed 2026-10-08) | 3,944,745 | full-resolution (2048 px) detect_v1 render of a patient radiograph, NHANES II (public domain): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `nhanes_cervical_00325.png` (in `report/renders/`; was copied, removed 2026-10-08) | 4,020,068 | full-resolution (2048 px) detect_v1 render of a patient radiograph, NHANES II (public domain): the task bars imaging data and large png sets, and the numbers behind it are in `metrics.json` / `results.csv` / `predictions.json`; grid `/wsu/home/go/go24/go2432/spine-detector/runs/detect_v1`; regenerate with `src/render_prediction.py` (the `spine-detector` repository; snapshot in `01_carm_level_detection/code/`) |
| `best_00_0888-F-058Y1.png` (in `scratchpad/yolo/`) | 222,263 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_01_1206-F-056Y1.png` (in `scratchpad/yolo/`) | 263,199 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_02_0314-M-015Y1.png` (in `scratchpad/yolo/`) | 256,253 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_03_0441-M-044Y1.png` (in `scratchpad/yolo/`) | 318,971 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_04_1511-F-061Y1.png` (in `scratchpad/yolo/`) | 213,107 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_00_2224-F-077Y1.png` (in `scratchpad/yolo/`) | 222,422 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_01_1490-F-054Y1.png` (in `scratchpad/yolo/`) | 252,131 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_02_0014-F-062Y1.png` (in `scratchpad/yolo/`) | 228,949 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_03_0766-F-061Y1.png` (in `scratchpad/yolo/`) | 266,415 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_04_1556-M-053Y1.png` (in `scratchpad/yolo/`) | 241,994 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_00_0277-F-050Y1.png` (in `scratchpad/failures/`) | 264,454 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_01_1424-F-075Y1.png` (in `scratchpad/failures/`) | 244,564 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `best_02_1592-M-049Y1.png` (in `scratchpad/failures/`) | 273,365 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_00_0913-F-048Y1.png` (in `scratchpad/failures/`) | 214,365 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_01_1024-F-074Y1.png` (in `scratchpad/failures/`) | 248,692 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_02_1068-F-071Y1.png` (in `scratchpad/failures/`) | 278,823 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_03_2330-M-064Y1.png` (in `scratchpad/failures/`) | 307,738 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_04_2504-F-087Y1.png` (in `scratchpad/failures/`) | 300,394 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `worst_05_2540-F-059Y1.png` (in `scratchpad/failures/`) | 279,281 | best/worst-case overlay on a BUU-LSPINE film (film pixels); BUU terms forbid redistribution |
| `clean_films.png` (in `lumbar_diag_2026-09-16/render/`) | 1,212,434 | montage of allspine_v2 bank films (BUU-LSPINE among them); BUU terms forbid redistribution; tracked in spinesurg-ct-nnunet 097933a lumbar_diag_2026-09-16/render/ |
| `l3_correct.png` (in `lumbar_diag_2026-09-16/render/`) | 937,765 | montage of allspine_v2 bank films (BUU-LSPINE among them); BUU terms forbid redistribution; tracked in spinesurg-ct-nnunet 097933a lumbar_diag_2026-09-16/render/ |
| `l3_errors.png` (in `lumbar_diag_2026-09-16/render/`) | 895,383 | montage of allspine_v2 bank films (BUU-LSPINE among them); BUU terms forbid redistribution; tracked in spinesurg-ct-nnunet 097933a lumbar_diag_2026-09-16/render/ |
| `worst_films.png` (in `lumbar_diag_2026-09-16/render/`) | 1,177,211 | montage of allspine_v2 bank films (BUU-LSPINE among them); BUU terms forbid redistribution; tracked in spinesurg-ct-nnunet 097933a lumbar_diag_2026-09-16/render/ |
| `IRB-21-10-4123_Amendment_Draft.docx` (in `CTSP1K_private/proposals_backup_20260911/`) | 15,807 | Word twin of the markdown draft (same text, verified 2026-10-08 by extracting word/document.xml); carries the unredacted student roster and two e-mail addresses, so the redacted markdown twin is copied instead |
| `XR_Fracture_Detector_Proposal.docx` (in `CTSP1K_private/proposals_backup_20260911/`) | 17,121 | Word twin of the markdown draft (same text, verified 2026-10-08 by extracting word/document.xml); carries the unredacted student roster and two e-mail addresses, so the redacted markdown twin is copied instead |

### 3b. Disposition rows of this project that are references by path (`_plan/DISPOSITION.tsv`, project 07, action `reference`)

| item | what | reason not copied |
|---|---|---|
| `CTSpinoPelvic1K-1/BUU-LSPINE_400/` (AP 800 jpg + csv, LA 800 jpg + csv, `BUU-LSPINE_400_report.xlsx`; 1,603 files) | the public BUU-LSPINE 400 subset | imaging data; BUU terms; on the grid as `~/spine-detector/data/raw/buu_v1` (B04) |
| `CTSpinoPelvic1K-1/BUULSPINE_3600/` (five zips, 9.96 GB, 2026-09-10) | the BUU-LSPINE release (3,600 patients, 7,200 films) | imaging data; BUU terms; on the grid as `~/spine-detector/data/raw/buu_full` (B04) |
| `CTSpinoPelvic1K-1/AASCE19/Archive.zip` (85 MB, 199 jpg dated 2019-06/07) | AASCE 2019 radiographs | imaging data; over 25 MB; on the grid as `~/spine-detector/data/raw/aasce` and `$RS/data/thoracic_xr` |
| `CTSpinoPelvic1K-1/CSPINE_ARCHIVE/` (`datasets-JSON.zip` 1.47 GB, `datasets-PNG.zip` 1.39 GB, `datasets.xlsx` 8.6 MB, `s41597-024-03383-0.pdf`) | the CSXA cervical radiograph dataset (Scientific Data 2024) | imaging data; the paper is public (its DOI is in the file name); on the grid as `~/spine-detector/data/raw/csxa` (B04) |
| `CTSpinoPelvic1K-1/LATERAL_ATLAS/lateral full-spine x-ray dataset.zip` (1.02 GB, 236 jpg) and `LATERAL_ATLAS/key.txt` | the IEEE DataPort lateral full-spine set; **`key.txt` is an AWS access key pair** (its first two lines were printed into a tool output on 2026-10-08: treat as exposed; rotate and delete; `_plan/PLAN.md` section 6) | imaging data (subscription set); a credential; on the grid as `~/spine-detector/data/raw/lateral_236` (B04) |
| `Desktop/TEST_XR.png` (2026-08-26) | a single lateral lumbar radiograph with pedicle screws used as a test image | imaging data of unrecorded origin; never into any repository until its source is known |
| `XRaySpinoPelvic1K/dataset2024.zip` (4,023,726,207 B, 2026-08-06, untracked) | a download whose identity is not recorded | data; over 25 MB; on the grid as `~/XRSpinoPelvic1K/data/dataset2024.zip` (B05 candidate) |
| `XRaySpinoPelvic1K/Spondylolisthesis Vertebral Landmark.zip` (43 MB) | Mendeley 5jdfdgp762 | data; over 25 MB; on Ceph `$RS/data/mendeley_5jdfdgp762/raw` (B14 VERIFIED) |
| `XRaySpinoPelvic1K/*.ica` (six files, one tracked at 4f22935) and `Unconfirmed 31234.crdownload` (tracked) | Cerner / Citrix session files from a hospital login; a partial download | credentials and junk; purge from history (`TODO.md` step 1) |
| `XRaySpinoPelvic1K/annot/.drr_yaw8_0.35.npz`, `examples/0003/{ap_drr, lateral_drr}.npy` | arrays | arrays never copied; the example PNGs and JSON are in the repository |
| `XRaySpinoPelvic1K/docs/figures/phase0_buu_hip_fov.png`, `phase0_buu_overlay20.png` | BUU overlay figures (tracked) | BUU film pixels (section 3a) |
| `XRaySpinoPelvic1K/.pytest_cache`, `xrsp/__pycache__` | caches | never copied |
| `spine-detector/dist/{detect_v3_640_fp32, detect_v4_1024_fp32, v11m_1024_v4_fp16, v11m_640_v4_fp16}.onnx` (84, 84, 42, 42 MB) | ONNX exports of 2026-09-12 | weights; over 25 MB; on the grid `~/spine-detector/dist` and `onnx_out`; removed from the public website on 2026-09-14 and never to return anywhere public |
| `spine-detector/dist/films`, `dist/labels` | 12 BUU / Mendeley films with YOLO labels | imaging data; BUU terms |
| `spine-detector/src/`, `tests/`, `.gitignore` | the detector code snapshot (21 `.py`) | copied into `01_carm_level_detection/code/` (one copy; `_plan/PLAN.md` section 4); the live tree is the grid checkout and the private repository |
| `spine-detector/configs`, `data`, `notebooks`, `.pytest_cache` | empty folders and a cache | nothing to copy |
| `spinesurg-ct-nnunet/logs/xray_gate/` (`corpus_xray_gate.json` 6,221 B, `modality_cheap.json` 323,639 B, `xray_gate_keep.txt` 31,284 B, `xray_gate_keep_readonly_modality.txt` 34,644 B, `xray_gate_rejected.jsonl` 814,037 B, three `xray_gate_eval_*.json` about 20 KB each, `pixmod/`, `strict/` (empty), `sheets/` 11 contact-sheet PNGs 20.9 MB; 22.7 MB in all, 2026-09-16, untracked) | the FluoroCap X-ray gate outputs | the disposition routes it by path; FluoroCap is out of training (directive D1) and is figures of published articles; the contact sheets are page images of articles; `TODO.md` step 19 decides archive or delete |
| `CTSP1K_private/proposals_backup_20260911/{IRB-21-10-4123_Amendment_Draft.docx, XR_Fracture_Detector_Proposal.docx}` | Word twins of the two redacted markdown drafts | same text (verified by extracting `word/document.xml` on 2026-10-08) with the unredacted roster and two e-mail addresses; the redacted markdown twins are in `regulatory/` |
| `CTSP1K_private/proposals_backup_20260911/{Annotator_Email.docx, annotator_email.md, andreea_email.md, cm_spine_request_email.md, lab_update_email_2026-09-07.md, student_primer_email.md, celebrate_life/, irb/}` | the other purged proposals (e-mails to students and staff; the IRB plan for two new protocols) | personal correspondence (names, addresses); `irb/IRB_PLAN.md` and `PROPOSAL_SHORT.md` are routed to folder 01 by the disposition; not this folder's |
| `CTSP1K_private/CTSpinoPelvic1K_prepurge_20260911.bundle` (97.8 MB) | the public repository's history before the 2026-09-11 purge of personal material | over 25 MB; personal material; reference by path, never push |
| `spinesurg-ct-nnunet/HANDOFF/working_notes/builders/` (`build_context_export.py` 12,652 B, `build_context_index.py` 7,661, `check_paths.py` 9,933, `check_refs.py` 2,010, `copy_context.py` 5,273, `patch_helper.py` 1,664, `refresh_context.py` 6,929; tracked at 097933a) | the scripts that rebuild `HANDOFF/` and `HANDOFF/context/` from the live memory folder | copied by the builder, removed on 2026-10-08: they name the laptop's memory folder and scratchpad by full path and have no bearing on plain-film work; run them only inside the repository |
| `spinesurg-ct-nnunet/HANDOFF/GREG_ONLY/` (`PRIVATE_STATE.md`, `README.md`, `context/`, `context_beethoven/`) | Greg's private state, the credential-location notes, the full copies of the three redacted notes, the six Beethoven notes | never copied into any project folder (`_plan/PLAN.md` section 2 rule 3); referenced by path from folder 01 |
| `spinesurg-ct-nnunet/HANDOFF/context/` (the 105 notes not in this folder's cut list) | the other families' memory notes | each note sits in the folder(s) its cut list names (`MEMORY.md` "Not in this folder") |
| `CTSpinoPelvic1K-1/scratchpad/` (everything but `results_unified/`, `yolo/`, `failures/`, the three `per_landmark` / `pl_*` csv files) | four review reports, about 120 one-off paper-edit scripts, measure diagrams, label volumes under `brk/`, `gapt/`, `one0631/`, `probecases/`, `case22/` | folder 03's or data; the paper-edit scripts' effects are already in the dataset article |
| `CTSpinoPelvic1K-1/Lumbosac.csv` (root) | reader initials | folder 03's, with the initials replaced by A / B / C there |

### 3c. Referenced but living only on the grid

Every item of `MANIFEST_GRID.md`: the film corpora, the detector tree, the banks, the model
registry, the result files behind the RECORD ONLY rows, the film N-curve outputs. None was copied;
none could be (imaging data, weights, or files only a job can read).

### 3d. Known to exist, in no file

The detect_v2 report folder beyond its numbers (grid only); the competitor ensemble result (grid
only, unread); any student read collected by the review Space (the ledger repository, not checked);
the XRSpinoPelvic1K `data/xrsp1k` DRRs (6,416 lateral DRRs of 822 pre-release cases) are **present** on HOME
(`/wsu/home/go/go24/go2432/XRSpinoPelvic1K/data/xrsp1k`, directory entry 114,688 B, a read-only `ls` at 01:25 UTC 2026-10-09; the 22:20
listing had cut that directory at `head -80` before the entry); unsized; B05 moves them (`MANIFEST_GRID.md` section 1).


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`
- `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md`

### Student names withheld (the same redaction 01 and 02 already carried)

The 14-author list of the dataset article (ten students), the two CNS abstract rows with student presenters, and (topic 6) the per-student username tally were still spelled out in the copies below; they now carry the placeholders used in 01 and 02. The two radiology residents and the published co-author stay (public co-authors of NeurIPS 3474 and the dataset article).

- `docs/handoff/MANUSCRIPTS.md`
- `docs/handoff/working_notes/topic4_manuscripts.md`

### E-mail address withheld

`memory/wsu-library-access-cutoff.md`: the library contact address replaced by `[library e-mail withheld]` (the library's public phone numbers kept), the same as 08's copy already read.

### Student presenters withheld in the CNS 2026 abstract table

The abstract table (section 12 of `MANUSCRIPTS.md` and its twin in topic 4) still named student presenters in four rows; each author cell now reads `[n student names withheld]` as 02's copy already did. Files: `docs/handoff/MANUSCRIPTS.md`, `docs/handoff/working_notes/topic4_manuscripts.md`.

### The one handle, withheld here as well

`docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` line 753 still spelled the co-PI's Hugging Face handle before her count; it now reads `[handle withheld] 142`. The redaction row of section 2 that quoted the handle by value now says `[handle]`.
