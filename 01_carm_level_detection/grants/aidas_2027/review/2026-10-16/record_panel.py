"""Point RECORD.md's rows at the one figure panel of issue #110 and record the change in section 4."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
s = path.read_text()

BULLET = """- **One figure panel (issue #110).** The owner, 2026-10-16: "ALSO THE PICTURES ARE NONVISIBLE, CAN YOU
  CONSOLIDATE THEM INTO ONE FIGURE PANEL TO SAVE SPACE?" The four figures were drawn 7.1 in wide and placed at 0.46
  to 0.50 of the line, so their labels printed near 3.4 pt. Figure 1 is now one panel of six, drawn 7.2 in wide and
  placed at that width at the top of page 3, so every label prints at 7 pt or more; `make_figures.py --check` fails
  on a label under 7 pt, outside the panel or its box, or over another label. Kept: the research loop (a, was 1b),
  the trainee's route (b, 1a and 2a in one), the cohort (c, was 2c), the sixth lumbar vertebra (d, was 1c) and the
  held-out results (f, was 4), now one dot plot with the values in a column and the counts left to the narrative
  and section 1. New: (e), the spine RAG-LLM as Aim 3's "The RAG-LLM" describes it, its two inputs, its two
  fine-tunes and its answer graded against OpenEvidence, with no number. Left out, since none could be read at a
  size that fits: the Beethoven popup's crop (2b), the archived network drawing (3a) and the projection drawing (3b),
  with the two rows above that only the drawings used; the text's references to 3a and 3b went with them, and its
  corners sentence now points at (d). The panel and its 60-word caption take about 1.4 in less of the narrative than
  the four figures did, left as room at the foot of page 4; 10 pages with the real and the example contact lines,
  no overfull line. The bullets above keep the figure numbers of their day.
"""

edits = [
    ("| YOLO11m detector; ResNet-18 encoder; two-layer bidirectional GRU over the run of 2 to 9 bodies; 27 levels | "
     "`01_carm_level_detection/docs/MODEL_CARD.md` (the model table); Figure 3a is `figures/schwingnet/fig1c_arch.pdf` "
     "at 5597197 |",
     "| (left the packet with Figure 3 on 2026-10-16, issue #110) YOLO11m detector; ResNet-18 encoder; two-layer "
     "bidirectional GRU over the run of 2 to 9 bodies; 27 levels | `01_carm_level_detection/docs/MODEL_CARD.md` (the "
     "model table); Figure 3a was `figures/schwingnet/fig1c_arch.pdf` at 5597197 |"),
    ("| SID 1,140 mm and SOD 745 mm, so 1.53 times larger on the detector (Figure 3b) |",
     "| (left the packet with Figure 3 on 2026-10-16, issue #110) SID 1,140 mm and SOD 745 mm, so 1.53 times larger on "
     "the detector (Figure 3b) |"),
    ("white on the CT and the render and black on the radiograph (Figure 1c) |",
     "white on the CT and the render and black on the radiograph (Figure 1d) |"),
    ("Figure 4a sets it beside A2.2's zero-shot 43.7 % on 631 agreed bodies",
     "Figure 1f sets it beside A2.2's zero-shot 43.7 % on 631 agreed bodies"),
    ("runs Claude Code workers as Slurm jobs (the significance, Aim 1, Figure 2) |",
     "runs Claude Code workers as Slurm jobs (the significance, Aim 1, Figure 1b) |"),
    ("which this session could not read, and Figure 2a, from the extension's own store diagram.",
     "which this session could not read, and Figure 1b, from the extension's own store diagram."),
    ("so Figure 2's caption says the worker is built to send GPU jobs to H200s |",
     "so Figure 1b labels its arrow to the H200s \"built to send GPU jobs\" |"),
    ("numbers drawn in Figures 2c and 4 are typed once in `make_figures.py` beside their rows;",
     "numbers drawn in Figure 1c and 1f are typed once in `make_figures.py` beside their rows;"),
    ("Rows A5.1 and A5.3 (Figure 4a's coupled point and the stop signal)",
     "Rows A5.1 and A5.3 (Figure 1f's point checked by the count, and the stop signal)"),
    ("The packet describes SchwingNet: Figure 3a is its architecture and the\n  narrative quotes its held-out results;",
     "The packet describes SchwingNet: the narrative names its parts and quotes\n  its held-out results, which Figure 1f "
     "draws, and since issue #110 no figure shows its architecture;"),
    ("- **The figures.** Figure 2a is redrawn as vector boxes from the labels of the extension's own store diagram, and\n"
     "  Figure 2b crops the popup's top half, which shows no grid login; the VS Code edition's diagrams have labels that\n"
     "  overlap at print size and are not used.",
     "- **The figures.** Figure 2a, now Figure 1b, is redrawn as vector boxes from the labels of the extension's own store\n"
     "  diagram; Figure 2b, which cropped the popup's top half and showed no grid login, left with issue #110; the VS Code\n"
     "  edition's diagrams have labels that overlap at print size and are not used."),
    ("servers (Figure 2a) and the correspondence told Elsevier",
     "servers (Figure 1b) and the correspondence told Elsevier"),
]
for old, new in edits:
    count = s.count(old)
    if count != 1:
        sys.exit(f"expected once, found {count}: {old[:90]!r}")
    s = s.replace(old, new)

anchor = "\n## 5. The execution skeleton"
if s.count(anchor) != 1:
    sys.exit("no section 5 heading")
before, after = s.split(anchor)
s = before.rstrip("\n") + "\n" + BULLET + "\n" + anchor.lstrip("\n").join(["", ""]) if False else \
    before.rstrip("\n") + "\n" + BULLET + anchor + after
path.write_text(s)
