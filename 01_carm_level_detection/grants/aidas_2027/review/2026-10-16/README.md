# The one-shot scripts of 2026-10-16

Kept for reference at the owner's word of 2026-10-16, 18:58 UTC (issue #114, `../../HANDOFF_2026-10-16.md`). The
thread "AIDaS grant" wrote each script in its session's scratch folder for one pull request, ran it once and merged the
result, so the pull request's diff is the record. The paths inside the scripts name that session's scratch folder and
its clone, so none runs as it stands. None holds a private file's contents: `build_both.sh` copies `contacts.tex` and
the biosketches into a scratch build and never into git.

| script | pull request | what it did |
|---|---|---|
| `tex_reframe.py` | #107 | rewrote `latex/main.tex` around the spine RAG-LLM as the goal and the spine program as its case |
| `tex_cut.py`, `tex_cut2.py`, `tex_cut3.py`, `tex_cut4.py` | #107 | trimmed the reframed text back to 10 pages |
| `record_reframe.py` | #107 | recorded the reframing in `RECORD.md`: amended and new rows, reference [31], section 4 and section 6 |
| `tex_plugin.py` | #107 | stopped attributing the Claude plug-in to OpenEvidence, and said what goes to it |
| `tex_review.py`, `record_review.py` | #107 | applied that day's adversarial review to `latex/main.tex` and `RECORD.md` |
| `tex_contacts_fit.py` | #109 | won back the two lines the real contact lines take on the cover |
| `tex_panel.py`, `record_panel.py` | #111 | replaced the four figures with the one panel, and recorded it in `RECORD.md` |
| `figs_review.py`, `probe_check.py` | #111 | applied the review's findings to `make_figures.py`, and showed that its label check catches what it should |
| `record_panel2.py` | #111 | rewrote `RECORD.md`'s bullet for issue #110 after the review |
| `tex_approx.py`, `record_approx.py` | #113 | replaced each red mark with an approximation, added line C3, and recorded both |
| `build_both.sh` | #111, #113 | built the packet with the example contact lines and with the real ones, and printed each build's pages and room |
| `note_send.py` | none | pointed the owner's note in the Project files at the PDF copy named for sending |
