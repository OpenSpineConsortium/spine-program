"""Replace the AIDaS packet's four figures with the one panel, and point the text's references at its panels."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
s = path.read_text()

CAPTION = ("Three aims. (a) The agent iterates until a sealed gate passes or its budget runs out. (b) Beethoven starts it "
           "on the grid. (c) Mean comfort [9]. (d) A sixth lumbar vertebra (arrow). (e) No indexed passage or patient "
           "record leaves the grid. (f) Zero-shot and detection rows never saw C-ArmLSpine; others hold out whole "
           "cases. Bars: 95\\pct{} case-clustered intervals.")
PANEL = ("\\begin{figure}[t]\\centering\n"
         "\\includegraphics[width=\\linewidth]{figures/fig1_panel.pdf}\n"
         "\\caption{" + CAPTION + "}\n"
         "\\end{figure}\n")

edits = [
    # The four figures go; the panel takes the first one's place.
    ("""\\placefigure{0.50\\linewidth}{figures/fig1_overview.pdf}{One loop, three aims. (a) Beethoven starts the trainee's agent. (b) The agent iterates hypotheses inside the
frameworks until a sealed gate passes or its budget runs out. (c) Why counting fails:
a sixth lumbar vertebra (arrow) in a labeled CT, its render and another person's radiograph.}
""", PANEL),
    ("""\\begin{figure}[t]\\centering
\\includegraphics[width=0.46\\linewidth]{figures/fig2_beethoven.pdf}
\\caption{Beethoven, the trainee's door to the grid. (a) The trainee asks
in claude.ai; the Claude Code worker runs as a Slurm job on the WSU grid, built to send GPU jobs to H200s. (b) One click opens the session. (c)
The 2026 cohort's mean comfort, before (recalled) and after (n = 16) [9].}
\\end{figure}

\\begin{figure}[t]\\centering
\\begin{minipage}[t]{2.55in}
  \\vspace{0pt}\\paneltitle{a}{The detector and the level model}\\par\\vspace{3pt}
  \\includegraphics[width=2.55in]{figures/network_architecture.pdf}
\\end{minipage}\\hspace{0.6in}%
\\begin{minipage}[t]{2.05in}
  \\vspace{0pt}\\paneltitle{b}{From the labeled CT to the image}\\par\\vspace{1pt}
  \\includegraphics[width=1.56in]{figures/fig3b_projection.pdf}
\\end{minipage}
\\par\\vspace{1pt}
\\caption{The level model, and how a CT labels the image. (a) The C-arm detector boxes the vertebral bodies and the sacrum,
and the level model names each body among 27 levels. (b) Each labeled body and its corners project to the image; a
transitional one in orange.}
\\end{figure}

""", ""),
    ("""\\placefigure{0.48\\linewidth}{figures/fig4_results.pdf}{Held-out results; bars are 95\\pct{} case-clustered intervals,
where recorded. (a) Level named exactly: zero-shot points never saw C-ArmLSpine, the others hold out whole cases.
(b) Vertebrae found, of 287, on a C-arm never trained on, at 0.74 (filled) and 0.25 (open).}

""", ""),
    # The macros only those figures used.
    ("""% A figure placed where it is written, so that no float drifts past the narrative's three pages.
\\newcommand{\\placefigure}[3]{%
  \\par\\smallskip\\noindent\\begin{minipage}{\\linewidth}\\centering
  \\includegraphics[width=#1]{#2}\\par
  \\captionof{figure}{#3}\\end{minipage}\\par\\smallskip}
% A panel title set like the ones drawn inside the figures: a 10 pt letter, an 8 pt title.
\\newcommand{\\paneltitle}[2]{{\\fontsize{10}{12}\\selectfont\\bfseries #1}\\hspace{0.45em}%
  {\\fontsize{8}{10}\\selectfont\\bfseries #2}}
""", ""),
    # The references, each to the panel that now shows it.
    ("a level model (Figure~3a) that names 96.4\\pct{} of the lateral vertebrae the\n"
     "film detector finds on a public C-arm it never saw (Figure~4a), while detection",
     "a level model that names 96.4\\pct{} of the lateral vertebrae the\n"
     "film detector finds on a public C-arm it never saw, while detection"),
    ("short of the 97\\pct{} set in advance (Figure~4b).", "short of the 97\\pct{} set in advance (Figure~1f)."),
    ("hands through Beethoven (Figure~2).", "hands through Beethoven (Figure~1b)."),
    ("retrospective ratings (Figure~2c)", "retrospective ratings (Figure~1c)"),
    ("\\emph{Model} (Figure~3a): a", "\\emph{Model}: a"),
    ("(Figure~3b), exact on renders. \\emph{Preliminary results} (Figure~4).",
     "(Figure~1d), exact on renders. \\emph{Preliminary results} (Figure~1f)."),
    ("at scale (Figure~3b), paired data", "at scale, paired data"),
    ("\\emph{The RAG-LLM.} The", "\\emph{The RAG-LLM} (Figure~1e). The"),
]
for old, new in edits:
    count = s.count(old)
    if count != 1:
        sys.exit(f"expected once, found {count}: {old[:80]!r}")
    s = s.replace(old, new)
for leftover in ("Figure~2", "Figure~3", "Figure~4", "placefigure", "paneltitle", "fig1_overview", "fig2_", "fig3b_",
                 "fig4_", "network_architecture"):
    if leftover in s:
        sys.exit(f"left over: {leftover}")
path.write_text(s)
words = CAPTION.replace("\\pct{}", "").split()
print(f"caption: {len(words)} words")
