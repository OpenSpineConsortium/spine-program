# AIDaS SEED 2026-2027 proposal packet

The Wayne State AIDaS Seed Grant proposal (PI Zhizhong Han, Co-PI Loren Schwiebert; $10,000 to $20,000 for one
year; deadline October 16, 2026, 11:59 p.m. ET, one PDF to the AIDaS office) written from this repository's record
on 2026-10-14. It addresses three of the call's four strategic areas with three aims: an autonomous code-generating
agent that writes and repairs grid jobs under pre-registered gates (Foundational AI), medical trainees driving that
agent on the WSU grid (Education and Workforce Training), and CT-trained 3-D structure carried into 2-D C-arm
fluoroscopy at low latency (Health). The call itself is `../../regulatory/carm_validation_plan_2026-09-21/AIDaS_Seed_Grant_Program.pdf`
in git history at main 5597197 (ARCHIVE.md), beside the earlier C-arm validation roadmap this packet draws on.

## Files

| file | holds |
|---|---|
| `AIDaS_SEED_2027_packet.md` | the whole packet in one markdown: cover page, the three-page narrative with the evaluation section and two figures, the alignment page, the budget page with its justification, the biosketch placeholder; then, after the marker `end of the submitted packet`, an appendix that the PDF leaves out: the execution skeleton, the file behind every number, and the open items |
| `AIDaS_SEED_2027_packet.pdf` | the export of the submitted part: 7 pages (cover 1, narrative 3, alignment 1, budget 1, biosketches 1) |
| `build_pdf.sh` | rebuilds the PDF: the markdown up to the marker, pandoc to .docx with the reference document, LibreOffice to PDF; prints the page count |
| `make_reference_docx.py` | writes the reference .docx for pandoc (Liberation Sans 10 pt, 0.7 inch margins, a page break before each top-level heading) and, with `--page`, gives the built .docx its page size and margins |
| `autonomous_spine_agent.py` | the execution skeleton of Aim 1: a grid simulator with the WSU grid's partitions, QoS rules and refusals; a mock language model that drafts and repairs job scripts; the agent loop with pre-registered gates; a placeholder evaluation loop with the C-arm projection matrix (Dice, IoU, corner error, exact level with a Wilson interval). `python3 autonomous_spine_agent.py --selftest`, then `--tasks 6 --seed 0 --root <repository> --out run.json` |
| `make_key_idea_figure.py` | draws `figures/fig_key_idea.svg` (Figure 1, the key idea) with the standard library; render it with `soffice --headless --convert-to pdf` then `pdftoppm -r 300 -png` |
| `make_preliminary_figure.py` | composes `figures/fig_preliminary_data.png` (Figure 2) from the three record figures with Pillow |
| `figures/fig_key_idea.svg`, `figures/fig_key_idea.png` | Figure 1, source and 300 dpi render |
| `figures/fig_preliminary_data.png` | Figure 2 |
| `figures/fig_spine_cartoon_typical_vs_t13.png` | `figures/schwingnet/fig1_row2_anatomy.png` at 5597197: the spine cartoon, a typical column against one with a thirteenth thoracic body |
| `figures/fig_corpus_tsne_manifold.png` | `figures/schwingnet/figS1.png` at 5597197: the corpus manifold, t-SNE of 11,638 frames from 18 sources |
| `figures/fig_problem_count_off_by_one.png` | `figures/schwingnet/fig1a_problem.png` at 5597197: the off-by-one count |

## Before submission

1. Fill every `[DATA NEEDED]` tag; the appendix of the packet lists them: ranks, department codes, contacts, AIDaS
   membership, New Investigator and NIH Early Stage Investigator status, the IRB number, the cohort size, the
   specimen count and imaging site, every placeholder fee and the fringe rate, the seat count, the solicitation numbers
   and dates, the OSTP citation, the F&A rule.
2. Ask the AIDaS office whether the cadaver lines (B1 to B5) and the FDA Pre-Submission line (D) are allowable; the
   call lists graduate student support, computing, invited collaborator travel and data management.
3. Append the two biosketches, two pages each.
4. Run the disclosure audit this repository requires before any submission (CLAUDE.md rule 8): the narrative quotes
   level-identification results from `docs/handoff/RESULTS_CATALOG.md`.
5. Rebuild with `bash build_pdf.sh` and check that the page count is still 7.

Every number in the packet names its file in the appendix; none is quoted from a LEAKED or SUPERSEDED row. The
mock run's numbers in the appendix are simulated and appear nowhere in the narrative as results.
