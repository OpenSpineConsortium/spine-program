"""Rewrite RECORD.md's bullet for issue #110 after the adversarial review, wrapped at 118 columns."""
import sys
import textwrap
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text()
start = text.index("- **One figure panel (issue #110).**")
end = text.index("\n\n## 5. The execution skeleton", start)

bullet = (
    '- **One figure panel (issue #110).** The owner, 2026-10-16: "ALSO THE PICTURES ARE NONVISIBLE, CAN YOU '
    'CONSOLIDATE THEM INTO ONE FIGURE PANEL TO SAVE SPACE?" The four figures were drawn 7.1 in wide and placed at 0.46 '
    "to 0.50 of the line, so their labels printed near 3.4 pt. Figure 1 is now one panel of six, drawn 7.2 in wide, "
    "the text's width, and placed at its own size at the top of page 3, so every label prints at 7 pt or more and a "
    "narrower text block would raise an overfull line rather than shrink them. `make_figures.py` checks before it "
    "writes and writes nothing when a label is under 7 pt, outside the panel, within 0.03 in of its own box's edge, or "
    "over another label, another box, an image or a data point; `--check` only checks. Kept: the research loop (a, was "
    "1b), the trainee's route (b, 1a and 2a in one), the cohort (c, was 2c), the sixth lumbar vertebra (d, was 1c) and "
    "the held-out results (f, was 4), now one dot plot with the values in a column, the 97 % goal named at the top of "
    "its line and the counts left to the narrative and section 1. New: (e), the spine RAG-LLM as Aim 3's \"The "
    "RAG-LLM\" describes it, with no number: inside a dashed line marking the grid, the image read by the detectors "
    "and the level model, the Scopus and ScienceDirect literature indexed, the model fine-tuned on public datasets' "
    "images and then on images with charts under the pending protocol, the retrieved passages and the answer; outside "
    "it, OpenEvidence, which gets only the question and the reading. Its boxes are white, since none of it is built. "
    "Left out, since none could be read at a size that fits: the Beethoven popup's crop (2b), the archived network "
    "drawing (3a) and the projection drawing (3b), with the two rows above that only the drawings used; the text's "
    "references to 3a and 3b went with them. The corners sentence cites no panel; the text cites (d) where section 1 "
    "first names a sixth lumbar vertebra and (a) where Aim 1 says the agent iterates. The caption, 59 words with its "
    "letters, says the dashed line is the grid, that answers are graded beside OpenEvidence's, and that the bars are "
    "intervals where recorded. The room at the foot of page 4 went from 0.35 in to 1.44 in, so the panel and its "
    "caption take about 1.1 in less than the four figures did; 10 pages with the real and the example contact lines, "
    "no overfull line. An adversarial review of the first draft found that (e) could be read as sending the answer, "
    "and the Elsevier text in it, to OpenEvidence, and that the corners sentence cited a panel with no corners in it; "
    "both were fixed as above, with its smaller findings: the goal label off the last row, the threshold key and the "
    "goal masked where they cross grid lines, the two thresholds' intervals set further apart, panel c's tick marks, "
    "(b)'s GPU label beside its arrow, a check blind to boxes, images and points, and figure files written before the "
    "check ran. Two were declined: the Symphony note in (a) stays in ink, since Symphony is one of the frameworks the "
    "loop runs in, not an aside, and the naming dots in (f) stay teal, the colour of every naming result there, the "
    "zero-shot AP row included, as the colour note in `make_figures.py` now says. The bullets above keep the figure "
    "numbers of their day."
)
wrapped = textwrap.fill(bullet, width=118, subsequent_indent="  ", break_on_hyphens=False, break_long_words=False)
path.write_text(text[:start] + wrapped + text[end:])
print(wrapped)
