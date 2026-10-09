# MANIFEST_CODE: the repositories this project references

Nothing that lives in a repository needs copying; this table says which repository, at which commit, holds each file
that matters to this project. Commits and remotes were read with `git rev-parse` and `git remote -v` on 2026-10-08.
Three small scripts are also copied into `code/` with their commit in the header (`MANIFEST_LOCAL.md`); the
repository remains the source of truth.

## spinesurg-ct-nnunet (private)

`https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` , branch `L6_Class`, commit 097933a (2026-10-08,
"HANDOFF: the handoff for a new student or a fresh Claude project"). Private since 2026-09-14; level-identification
code, text and weights never go public (`memory/fluorocap-repo-private.md`). On the grid: `~/spinesurg-ct-nnunet`.

| file | what it is for here | last commit of the file |
|---|---|---|
| `tools/review_screen.py` | stage 1 of the scoping review: screens every record by the named patterns of `review_patterns.py` over title, abstract and full text; writes `screening.jsonl` with the matched strings | 2026-09-15 (mtime; commit not read) |
| `tools/review_patterns.py` | the named patterns and the machine-readable inclusion criteria (`CRITERIA`) written into every output | 2026-09-15 |
| `tools/review_abstracts.py` | fetches abstracts for every record from Europe PMC and Semantic Scholar (key from a credentials file, never copied); resumable via `abstracts_done.txt` | 2026-09-15 |
| `tools/review_compare.py` | compares two screening passes record by record (`screening_titleonly.jsonl` against `screening.jsonl`); writes `SCREEN_CHANGES.md`, `screen_changes.csv/.json` | 2026-09-15 |
| `tools/review_extract.py` | stage 3 pre-fill: charts the included records from the held text with explicit / inferred / absent flags; writes `extraction.jsonl`, `incidence.csv`, `incidence_reported.csv` | 2026-09-15 |
| `tools/review_prisma.py` | PRISMA 2020 / PRISMA-ScR flow counts and the SVG diagram from `screening.jsonl` (`--screening ~/review/screening.jsonl --out ~/review`); copied to `code/` | 3d91ecd 2026-09-15 |
| `tools/review_stats.py` | the six provisional statistics over `extraction.jsonl` and `incidence_reported.csv`, explicit subset primary, explicit-plus-inferred as sensitivity; writes `REVIEW_STATS.md/.json`; copied to `code/` | 3d91ecd 2026-09-15 |
| `tools/review_summary.py` | writes `REVIEW_DATA.md` (every count a count of rows in a named file) | 2026-09-15 |
| `tools/review_figures.py` | joins the included set to the figure corpus by PMCID; `review_figures.jsonl`, `REVIEW_FIGURES.md`, `figure_shortlist.csv` | 2026-09-15 |
| `tools/prior_art_wrong_level.py` | OpenAlex top-cited pulls for wrong-level surgery, transitional anatomy, AI detection of variants, rare classes; copied to `code/` | 8180a63 2026-09-14 |
| `tools/prior_art_weak.py` | OpenAlex pulls on weak supervision for vertebra labels on radiographs | 2026-09-14 |
| `tools/fluorocap_wrong_level_report.py` | counts mechanisms, countermeasures and regions over the mined passages (`--passages ~/FluoroCap_lstv/passages.jsonl --out WRONG_LEVEL.md`); its output is `results/wrong_level_passages/` | 729872a 2026-09-15 |
| `tools/fluorocap.py` line 58 | `QUERY_EXTRA`, the executed Europe PMC query the protocol reproduces verbatim (`PROTOCOL_...md` section 5) | not read |
| `tools/fluorocap_passages.py` | mines the full-text passages the report counts | not read |
| `tools/disclosure_audit.py` | the audit run before any talk, upload or submission (`docs/handoff/README.md` section 5 rule 8) | 345c187 2026-09-18 |
| `tools/fiducial_walk.py`, `slurm/fiducial_walk.sh` | the fiducial-walk experiment whose numbers the QI manuscript quotes; results under `~/model_night` (`MANIFEST_GRID.md`) | not read |
| `docs/WRONG_LEVEL_COST_EVIDENCE.md`, `docs/WRONG_SITE_BURDEN_EVIDENCE.md` | the two verified briefs; copied to `docs/` | 980eecc, e2eab64 (2026-09-19) |
| `docs/SWEEP_TIME_EVIDENCE.md` | the sweep's time budget, verified (the "one to three minutes" sentence of the QI abstract) | 098756a 2026-09-19 |
| `docs/PRIOR_ART_LEVEL_ID_HUMANS_AND_AI.md` | human naming 69.6 % unassisted, 97.6 % with LevelCheck (Manbachi 2018); 24 verified claims; in `01_carm_level_detection/docs/` | 90cf5d1 2026-09-17 |
| `docs/PRIOR_ART_WRONG_LEVEL_SCAN.md`, `docs/WRONG_LEVEL_AND_TRANSITIONAL.md` | the raw OpenAlex tables and the note on imaging causes behind `prior_art_wrong_level.py`; in `01_carm_level_detection/docs/` | 8180a63 2026-09-14 |
| `docs/research_localisation_cost_2026-09-22.json`, `docs/research_rsnai_intro_verified_2026-09-22.json`, `docs/research_rsnai_intro2_partial_2026-09-22.json`, `docs/research_rsnai_intro_nav_verified_2026-09-22.json` | the verified sweeps on localisation cost and wrong-level incidence (`docs/handoff/LITERATURE_STATE.md` section 6 rows 25 to 28) | 2026-09-22 |
| `docs/CONTINUANCE_2026-09-19.md` lines 87 to 101 | the fiducial-walk record (950 walks, 7,405 walks) and the Universal Protocol mapping; in `01_carm_level_detection/docs/` | 2026-09-19 |
| `docs/RSNAI_PLAN.md` line 260 | records that the QI draft's "about fifteen minutes of fluoroscopic counting" (mongardi2021 + upadhyaya2012) is unverified | not read |
| `paper/qi_universal_protocol/main.tex`, `build.sh` | the QI manuscript; copied to `manuscripts/qi_universal_protocol/` | d4b895e 2026-09-22; 8e4d845 2026-09-19 |
| `paper/rsnai/refs.bib` | the bibliography the QI manuscript cites (`\bibliography{../rsnai/refs}` in the original); copied beside the manuscript | 180fb0f 2026-09-23 |
| `SchwingNet/LEVELCHECK_CLAIM.md` section 2 | the prior-art rates of catalog row B.8 (Mody 2008, Jhawar 2007, Furuya 2026, Nakagawa 2017, Hanhivaara 2020); private; a copy is in `02_transitional_naming_truth/docs/` | not read |
| `docs/INVENTION_DISCLOSURE.md` section 3 E | names the sweep and the persistent digital fiducial as invention aspects; never copied into `spine-program`; referenced by path only | not read |
| `HANDOFF/` (all but `GREG_ONLY/`) | the handoff of 2026-10-08; copied whole to `docs/handoff/` | 097933a |
| `tools/eval_gate.py` | the evaluation gate every quoted score passes (`docs/handoff/README.md` section 5 rule 5) | not read |

## CTSpinoPelvic1K (public)

`https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K` (origin) and
`https://github.com/OpenSpineConsortium/CTSpinoPelvic1K` (osc), branch `master`, commit 7ddfe38 (working tree
modified on 2026-10-08). Commit directly to master; push both remotes through WSL. On the grid: `~/CTSpinoPelvic1K`
at a0c5139 (`MANIFEST_GRID.md`).

| file | what it is for here | last commit |
|---|---|---|
| `paper/clinical/main.tex`, `paper/clinical/iliac_crest_landmark.pdf` | the iliac-crest clinical paper; copied to `manuscripts/iliac_crest/` | 0ecbb82 2026-08-22 |
| `scripts/extract_surgical_morphometrics.py` | `crest_above_l45_mm` and `crest_blocks_l45` (crest 12 mm or more above the L4-5 disc): the crest is the highest z of either hip label, the disc the midpoint between the L4 and L5 bodies ("the lateral corridor" block); exits non-zero when a median leaves its published range | 2232bde 2026-09-11 |
| `scripts/extract_transition_morphometrics.py` | the rib-free count and the vertebral level reached by the crest ("iliac crest height" block, line 423): the clinical paper's Tables 1 and 2 | not read |
| `morphometrics/surgical_morphometrics.csv` | per-case `crest_above_l45_mm`, `crest_blocks_l45`, `crest_z_mm`, `rib12_to_crest_mm` (columns 12 to 14, 57) | 2232bde 2026-09-11 |
| `morphometrics/transition_morphometrics.csv`, `morphometrics/pelvic_shape.csv` | written 2026-09-10 on v10 labels; recompute on v11 (`docs/handoff/RECIPES.md` section 9 item 3) | not read |
| `README.md` "Release QC - v5" (line 190) | the sentence "24.7 % of cases (195 / 789) have an iliac crest 12 mm or more above the L4-5 disc" (catalog F.41) | not read |
| `docs/SPINOPELVIC_ESTIMATOR.md` | how the spinopelvic numbers are computed, the four defects found and the three open ones; the pattern the crest recompute follows | not read |
| `CLAUDE.md` | the dataset repository's working context (the two label schemes, identifier 29, `zfill(4)`, RAS) | not read |
| `docs/castellvi_consensus.csv` | the 33 Castellvi grades (two readers) behind catalog D.18; reader initials in the column names | not read |
| `slurm/morphometrics.sh` and the other extractor wrappers | still point at `data/v5_final` and `-q primary`: edit before reuse (`RECIPES.md` section 9 item 3) | not read |
| `proposals/review/` | the scoping review protocol, manuscript and checklist: gitignored and untracked at 7ddfe38, so the repository does NOT hold them; this folder's `manuscripts/scoping_review/` is the copy | untracked |
| `Student_Projects/BOARD.md` | the lab board; names "Dr Tech" as the senior clinical PI who confirms clinical reads (`OPEN_QUESTIONS.md` A18) | not read |

## OpenSpineToolkit (public)

`https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit` (origin) and
`https://github.com/OpenSpineConsortium/OpenSpineToolkit` (osc), branch `main`, commit cb43197. `ostk.labels.labels_for(volume)` is the only way a label name is resolved
(`memory/label-scheme-v4-vs-ostk.md`). Known open defects that bear on any pelvis-adjacent recompute: the
whole-sacrum fallback for S1 on v11 and the canal-closing regression of 1b7005c (`docs/handoff/RESULTS_CATALOG.md`
G.2, G.3; `04_openspinetoolkit`).

## XRSpinoPelvic1K (private)

`https://github.com/Gregory-Schwing-MD-PhD/XRSpinoPelvic1K`, branch `main`, commit 4f22935. Not used by this project;
listed because every folder names the four source repositories.

## Other repositories named by the inventories

None is used by this project. Each is listed with URL, branch and commit as its owning folder's `MANIFEST_CODE.md`
records them (read 2026-10-08).

| repository | URL | branch, commit | owning folder |
|---|---|---|---|
| Beethoven (browser extension and `hpcworker` framework; the clone keeps the code name `ashley-bridge`; the students' route to the grid) | `https://github.com/OpenSpineConsortium/beethoven` | `main`, 2f90319 (2026-10-03) | `11_students_grid_access` |
| Beethoven for VS Code and the access service (the clone keeps the code name `ashley`) | `https://github.com/OpenSpineConsortium/beethoven-vscode` | `main`, 8d7fc65 (2026-10-02) | `11_students_grid_access` |
| the consortium site | `https://github.com/OpenSpineConsortium/openspineconsortium.github.io` | `master`; the clone read at c1800f8 (2026-10-02), origin head a17ea39 (2026-10-07) | `12_website_pacs_demo` |
| spine-detector (private) | `https://github.com/OpenSpineConsortium/spine-detector` | commit not recorded: the laptop snapshot has no `.git`; the live tree is the grid checkout `/wsu/home/go/go24/go2432/spine-detector` (2026-09-12) | `07_plain_film_level_id` |
| spinopelvic-seg | `https://github.com/OpenSpineConsortium/spinopelvic-seg` (osc) and `https://github.com/anonymous-neurips-ED/spinopelvic-seg` (origin, the review-time anonymous copy) | `main`, c105981 (2026-06-23) | `03_ctspinopelvic1k_dataset` |
