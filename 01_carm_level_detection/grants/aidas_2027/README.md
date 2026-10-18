# AIDaS SEED 2026-2027 proposal packet

The Wayne State AIDaS Seed Grant proposal: PI Zhizhong Han, Co-PI Loren Schwiebert, clinical collaborator Gregory
Schwing (General Surgery); $19,987 for January to December 2027; due October 16, 2026, 11:59 p.m. ET, as one PDF to
the AIDaS office (aidas@wayne.edu). Three aims across three of the call's four strategic areas: Claude Code
iterating the scientific method on the WSU grid inside the consortium's frameworks, Beethoven, beethoven-qa,
beethoven-research and Symphony, under tests sealed before each run (Foundational AI), medical trainees driving that
agent through Beethoven (Education and Workforce Training), and CT-labeled 3-D
structure carried into 2-D C-arm images and on to a spine RAG-LLM, the case example (Health). The call is
`../../regulatory/carm_validation_plan_2026-09-21/AIDaS_Seed_Grant_Program.pdf`, read from git history at main 5597197
(`ARCHIVE.md`).

## Files

| file | holds |
|---|---|
| `latex/main.tex` | the packet: cover (1 page), narrative with one figure panel (3), alignment (1), budget and justification (1), then the biosketches; compiles with pdflatex alone |
| `latex/figures/` | `fig1_panel.pdf`, the one figure the packet places, at its own size, written by `make_figures.py` |
| `latex/contacts.example.tex` | the cover's placeholder contact lines, with how to escape `%`, `_` and `&`; the filled `contacts.tex` and the two biosketch PDFs go beside `main.tex` in the Overleaf copy only, never into git (`latex/.gitignore` and `.gitignore`; root CLAUDE.md rule 12) |
| `AIDaS_SEED_2027_packet.pdf` | the committed draft build: 8 pages, the contacts as placeholders and one placeholder page for each biosketch |
| `build_pdf.sh` | builds the packet with pdflatex in a temporary directory and fails when a section spills onto an extra page; with `contacts.tex` and both biosketches in `latex/` it writes the 10-page `AIDaS_SEED_2027_submission.pdf` instead, which git ignores, and refuses while one of the three is missing, a biosketch is not two pages or a [DATA NEEDED] mark is left |
| `make_overleaf_zip.sh` | makes the Overleaf zip from the tracked files under `latex/` and the three local files beside `main.tex`, refuses while one is missing or a biosketch is not two pages, and writes the zip only once an unzipped copy compiles to 10 pages; the zip carries e-mail addresses, so it is written outside the tree by default and git ignores it |
| `make_figures.py` | draws Figure 1, one panel of six as wide as the text (matplotlib and Pillow), into `latex/figures/`, with a 300 dpi preview in `figures/`, and writes nothing when a label is under 7 pt, outside the panel or its box, or over another label, a box, an image or a data point; `--check` checks and writes nothing |
| `figures/sources/` | the images the panel is made from, three crops of the record's sixth-lumbar figure, with their origin and the file behind every number drawn in `SOURCES.md` |
| `APPROXIMATIONS.md` | since issue #112, every value that stands in for one the team has not confirmed, with its basis and who can confirm it |
| `RECORD.md` | the file behind every number, the values found on the web with their links, the [DATA NEEDED] list, the open items and caveats; not submitted |
| `autonomous_spine_agent.py` | a record of the earlier Aim 1, kept since issue #100 rewrote it (`RECORD.md` section 5): a grid simulator with the WSU grid's partitions and refusals, a mock model that drafts and repairs jobs, the agent loop with gates registered by hash, a placeholder evaluation. `python3 autonomous_spine_agent.py --selftest`; run it on a laptop or as an sbatch job, never on the grid's login node |
| `REVIEW_2026-10-14.md` | the five reviewers' findings on the packet merged in #91, applied in the pull request for issue #94, except where `RECORD.md` section 4 says a change was made another way by design |
| `HANDOFF_2026-10-14c.md` | the checkpoint that set that work |
| `HANDOFF_2026-10-14e.md` | where the work for #94 stopped when the owner's usage ran low: the next steps to Friday's deadline, how to build the submission and the Overleaf zip, and what waits on the owner; its 2026-10-15 updates record #95's merge and the build of the zip and the 10-page PDF with the biosketches |
| `HANDOFF_2026-10-16.md` | the owner's checkpoint of 2026-10-16 (issue #114): where the packet stands after #113, what was sent and what the PI and Co-PI answered, what remains before the deadline, and how a thread on another account carries on |
| `SUBMITTED_2026-10-16.md` | the packet as submitted to the AIDaS office on 2026-10-16: when, the PDF's checksum, that its narrative is `latex/main.tex` at 88871de, what Elsevier's message of 2026-10-16 changes, and the changes proposed for the next submissions, none made (issue #118) |
| `review/` | the second review round's writing edits (`r6_line_edits.patch`, then `r6_hidden_check.patch` and `r6_figure_edits.patch`), applied to `main.tex` and `make_figures.py` on 2026-10-15 with the choices `RECORD.md` section 4 records; the reviewer's report `r6_panel_writing.md`; and `page_slack.py`, which prints the room left at the foot of each page; `review/2026-10-16/` keeps the one-shot scripts of 2026-10-16 behind #107 to #113, for reference, with a README |

## Building it

- **On Overleaf:** upload the zip of `latex/` with `contacts.tex`, `biosketch_han.pdf` and `biosketch_schwiebert.pdf`
  beside `main.tex` (`bash make_overleaf_zip.sh` makes it), set the compiler to pdfLaTeX and
  compile `main.tex`: 10 pages.
- **Here:** `bash build_pdf.sh` writes the 8-page draft; put the three files in `latex/` to get the 10-page
  submission, which it builds only once every [DATA NEEDED] mark is filled. After a figure changes, run
  `python3 make_figures.py` first.

## Before submission

1. Replace each approximation with a confirmed value; `APPROXIMATIONS.md` lists them, `RECORD.md` section 3 the red
   marks they replaced, and section 2 links every value taken from the web, most of them from search excerpts that
   need a click-through.
2. Ask the AIDaS office whether lines B (the cadaver set), C3 (the reimbursement), D (the FDA Pre-Submission consultant)
   and F (the poster) are allowable and how line A may be hired; `RECORD.md` section 4 gives the totals without them.
3. Run the disclosure audit (root CLAUDE.md rule 8): the packet quotes SchwingNet's held-out results and draws
   them in Figure 1f.
4. Decide the MIT release of Aim 1's tasks, records and report, and the caveats in `RECORD.md` section 4.
5. Confirm that Elsevier has enabled the Scopus APIs on the key and ask the library for the text and data mining
   amendment to WSU's ScienceDirect agreement; the packet states both as they stood on 2026-10-15 (`RECORD.md`
   section 6), as it states the IRB protocol IRB-26-03-8648 as pending.
6. Build with the contacts and biosketches, check the page count is 10, and send the one PDF.
