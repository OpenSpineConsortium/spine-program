# AIDaS SEED 2026-2027 proposal packet

The Wayne State AIDaS Seed Grant proposal: PI Zhizhong Han, Co-PI Loren Schwiebert, clinical collaborator Gregory
Schwing (General Surgery); $18,568 for January to December 2027; due October 16, 2026, 11:59 p.m. ET, as one PDF to
the AIDaS office (aidas@wayne.edu). Three aims across three of the call's four strategic areas: a self-repairing
agent that writes and repairs its own Slurm jobs on the WSU grid under gates written before each run (Foundational
AI), medical trainees driving that agent through Beethoven (Education and Workforce Training), and CT-labeled 3-D
structure carried into 2-D C-arm images at low latency (Health). The call is
`../../regulatory/carm_validation_plan_2026-09-21/AIDaS_Seed_Grant_Program.pdf`, read from git history at main 5597197
(`ARCHIVE.md`).

## Files

| file | holds |
|---|---|
| `latex/main.tex` | the packet: cover (1 page), narrative with four figures and the evaluation table (3), alignment (1), budget and justification (1), then the biosketches; compiles with pdflatex alone |
| `latex/figures/` | the figure PDFs the packet places, written by `make_figures.py`; Figure 3a, `network_architecture.pdf`, is the archived drawing copied unchanged |
| `latex/contacts.example.tex` | the cover's placeholder contact lines, with how to escape `%`, `_` and `&`; the filled `contacts.tex` and the two biosketch PDFs go beside `main.tex` in the Overleaf copy only, never into git (`latex/.gitignore` and `.gitignore`; root CLAUDE.md rule 12) |
| `AIDaS_SEED_2027_packet.pdf` | the committed draft build: 8 pages, the contacts as placeholders and one placeholder page for each biosketch |
| `build_pdf.sh` | builds the packet with pdflatex in a temporary directory and fails when a section spills onto an extra page; with `contacts.tex` and both biosketches in `latex/` it writes the 10-page `AIDaS_SEED_2027_submission.pdf` instead, which git ignores, and refuses while one of the three is missing, a biosketch is not two pages or a [DATA NEEDED] mark is left |
| `make_figures.py` | draws Figures 1, 2, 3b and 4 (matplotlib and Pillow) into `latex/figures/`, with a 300 dpi preview of each in `figures/` |
| `figures/sources/` | the images the figures are made from, each with its origin in `SOURCES.md`: a crop of the Beethoven browser extension's popup, three crops of the record's sixth-lumbar figure, the network drawing |
| `RECORD.md` | the file behind every number, the values found on the web with their links, the [DATA NEEDED] list, the open items and caveats; not submitted |
| `autonomous_spine_agent.py` | the execution skeleton of Aim 1: a grid simulator with the WSU grid's partitions and refusals, a mock model that drafts and repairs jobs, the agent loop with gates registered by hash, a placeholder evaluation. `python3 autonomous_spine_agent.py --selftest`; run it on a laptop or as an sbatch job, never on the grid's login node |
| `REVIEW_2026-10-14.md` | the five reviewers' findings on the packet merged in #91, applied in the pull request for issue #94, except where `RECORD.md` section 4 says a change was made another way by design |
| `HANDOFF_2026-10-14c.md` | the checkpoint that set that work |
| `HANDOFF_2026-10-14e.md` | where the work for #94 stopped when the owner's usage ran low: the next steps to Friday's deadline, how to build the submission and the Overleaf zip, and what waits on the owner |
| `review/` | the second review round's writing edits (`r6_line_edits.patch`, then `r6_hidden_check.patch` and `r6_figure_edits.patch`), applied to `main.tex` and `make_figures.py` on 2026-10-15 with the choices `RECORD.md` section 4 records; the reviewer's report `r6_panel_writing.md`; and `page_slack.py`, which prints the room left at the foot of each page |

## Building it

- **On Overleaf:** upload the zip of `latex/` with `contacts.tex`, `biosketch_han.pdf` and `biosketch_schwiebert.pdf`
  beside `main.tex` (`HANDOFF_2026-10-14e.md` says how to make it), set the compiler to pdfLaTeX and
  compile `main.tex`: 10 pages.
- **Here:** `bash build_pdf.sh` writes the 8-page draft; put the three files in `latex/` to get the 10-page
  submission, which it builds only once every [DATA NEEDED] mark is filled. After a figure changes, run
  `python3 make_figures.py` first.

## Before submission

1. Fill each red [DATA NEEDED] mark; `RECORD.md` section 3 lists them, and section 2 links every value taken from the
   web, most of them from search excerpts that need a click-through.
2. Ask the AIDaS office whether lines B (the cadaver set), D (the FDA Pre-Submission consultant) and F (the poster)
   are allowable and how line A may be hired; `RECORD.md` section 4 gives the totals without them.
3. Run the disclosure audit (root CLAUDE.md rule 8): the packet shows SchwingNet's architecture and quotes its
   held-out results.
4. Decide the MIT release of the agent and its benchmark, and the caveats in `RECORD.md` section 4.
5. Build with the contacts and biosketches, check the page count is 10, and send the one PDF.
