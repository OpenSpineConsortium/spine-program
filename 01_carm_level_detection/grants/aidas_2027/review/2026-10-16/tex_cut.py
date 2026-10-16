import pathlib
p = pathlib.Path('/home/user/spine-program/01_carm_level_detection/grants/aidas_2027/latex/main.tex')
s = p.read_text()
def rep(old, new):
    global s
    n = s.count(old); assert n == 1, (n, old[:90]); s = s.replace(old, new)
def rep_span(start, end, new, keep_end=False):
    global s
    i = s.find(start); assert i >= 0 and s.count(start) == 1, start[:60]
    j = s.find(end, i); assert j >= 0 and s.count(end) == 1, end[:60]
    s = s[:i] + new + s[(j if keep_end else j + len(end)):]

# Leading, paragraph skip and float separation.
rep(r"\begingroup\fontsize{8.8}{10}\selectfont\setlength{\parskip}{1pt}\setlength{\textfloatsep}{8pt}",
    r"\begingroup\fontsize{8.8}{9.9}\selectfont\setlength{\parskip}{0.5pt}\setlength{\textfloatsep}{6pt}")
# Figures a little smaller.
rep(r"\placefigure{0.58\linewidth}{figures/fig1_overview.pdf}", r"\placefigure{0.50\linewidth}{figures/fig1_overview.pdf}")
rep(r"\includegraphics[width=0.54\linewidth]{figures/fig2_beethoven.pdf}", r"\includegraphics[width=0.48\linewidth]{figures/fig2_beethoven.pdf}")
rep(r"\placefigure{0.58\linewidth}{figures/fig4_results.pdf}", r"\placefigure{0.50\linewidth}{figures/fig4_results.pdf}")
rep(r"\begin{minipage}[t]{2.80in}", r"\begin{minipage}[t]{2.55in}")
rep(r"\includegraphics[width=2.80in]{figures/network_architecture.pdf}", r"\includegraphics[width=2.55in]{figures/network_architecture.pdf}")
rep(r"\end{minipage}\hspace{0.45in}%", r"\end{minipage}\hspace{0.6in}%")
rep(r"\includegraphics[width=1.71in]{figures/fig3b_projection.pdf}", r"\includegraphics[width=1.56in]{figures/fig3b_projection.pdf}")

# Section 1, the rib check in fewer words.
rep(r"""with a thirteenth thoracic, under a stopping rule fixed before any download that turned 29,479 chest CTs away; when one
labeler called a thirteenth rib-bearing vertebra in 9.3\pct{} of 367 chest CTs, five to fifteen times the published
rate, requiring a rib on the named body brought it to 1.4\pct{}, the check outside the computation that this project's
gates make routine.""",
    r"""with a thirteenth thoracic, under a stopping rule fixed before any download that turned 29,479 chest CTs away; a
labeler's 9.3\pct{} rate of thirteenth rib-bearing vertebrae in 367 chest CTs fell to 1.4\pct{} once a rib on the named
body was required, the check outside the computation that this project's gates make routine.""")

# 1c without the three axes in parentheses.
rep(r"""on the twelve-axis taxonomy written
for the comparison (who pays, how a claim is kept, what decides acceptance).""",
    r"""on the twelve-axis taxonomy written for the comparison.""")

# 1d, tighter.
new_1d = r"""\emph{1d, the
control plane.} A web control panel driven by Claude's own browser (repositories, board, CI, tasks, workers, prompts)
showing each run's cost beside the same work on unsorry or Copilot's cloud agent; a wizard storing a lab's Claude
tokens as saved environment secrets; Beethoven bridging Actions to the grid, a worker in Actions submitting the Slurm
job and posting its results and logs back to the pull request; and the extension's one click brought from Claude Code
to the claude.ai Project each trainee works in. """
rep_span(r"\emph{1d, the", r"\emph{Preliminary work.}", new_1d, keep_end=True)

# Aim 2's preliminary work, tighter.
rep(r"""\emph{Preliminary work} [9]: in 2026, 16 students, seven with no
coding and eleven with no imaging experience, worked on ten sub-projects in that setup with mentors expert in Slurm;
all six domains improved on retrospective before-and-after ratings (Figure~2c), all ten went to a national meeting as
abstracts, and the report names what it lacked, a control group and objective measures, which Aim 2 adds.""",
    r"""\emph{Preliminary work} [9]: in 2026, 16 students, seven with no
coding and eleven with no imaging experience, worked on ten sub-projects in that setup; all six domains improved on
retrospective ratings (Figure~2c), all ten went to a national meeting as abstracts, and the report's own limits, no
control group and no objective measure, are what Aim 2 adds.""")

# Aim 3, the rebuilt-truth clause goes.
rep(r"""(90.6\pct{} and 83.9\pct{} at 0.25); on truth rebuilt after that scoring it finds 82.2\pct{} of the 287 and 93.9\pct{}
of the 214 whose truth is complete and at least 80\pct{} visible. \emph{What COBRA adds.}""",
    r"""(90.6\pct{} and 83.9\pct{} at 0.25). \emph{What COBRA adds.}""")

# COBRA, what it buys in fewer words.
rep(r"""are real-image corner labels for the new detector
at scale (Figure~3b), paired data to fit the simulator's spectrum, scatter and sensor terms by supervision, and, in
Varian, a second held-out vendor; the cost is export and storage, a Varian bank with a quality look, and GPU hours, an
Aim 1 task set.""",
    r"""are real-image corner labels for the new detector
at scale (Figure~3b), paired data to fit the simulator's spectrum, scatter and sensor terms, and a second held-out
vendor (Varian); the cost is export, storage, a quality look at the Varian bank and GPU hours, an Aim 1 task set.""")

# The RAG-LLM paragraph, tighter.
rep_span(r"\emph{The RAG-LLM.}", r"no patient record leaves the grid. \emph{H3:}",
    r"""\emph{The RAG-LLM.} The detector and level model become tools of a multimodal model hosted on the grid that
takes the image, the detectors' boxes and names and the retrieved passages, and answers a clinical question with the
level, the finding and verbatim quotations. Its first release is fine-tuned on the public corpus (CTSpinoPelvic1K, the
films and their reports, COBRA), its second on images paired with operative notes and radiology reports under
IRB-26-03-8648, whose stated purpose is a locally hosted multimodal spine LLM, amended as the work requires; a lab swaps
in its own corpus, detectors and records. On a held-out question set the mentors write, its answers and OpenEvidence's,
through OpenEvidence's plug-in for Claude [31], are graded side by side for correctness and for quotations that support
them; our detectors' reading of an image can be handed to OpenEvidence as a tool, while no indexed passage and no
patient record leaves the grid. \emph{H3:}""")

# Reference 31 that can break across the narrow column.
rep(r"[31] OpenEvidence. openevidence.com; its API set-up skill for Claude Code, mcpmarket.com/tools/skills/openevidence-api-setup-auth.",
    r"[31] OpenEvidence, openevidence.com; its Claude Code set-up skill, mcpmarket.com/\allowbreak tools/\allowbreak skills/\allowbreak openevidence-api-setup-auth.")
p.write_text(s); print("cuts applied")
