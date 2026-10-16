import pathlib
p = pathlib.Path('/home/user/spine-program/01_carm_level_detection/grants/aidas_2027/latex/main.tex')
s = p.read_text()
def rep(old, new):
    global s
    n = s.count(old); assert n == 1, (n, old[:90]); s = s.replace(old, new)
rep(r"""\vspace{2pt}
{\fontsize{5.8}{6.6}\selectfont
\begin{multicols}{5}""",
    r"""{\fontsize{5.8}{6.6}\selectfont\setlength{\multicolsep}{3pt}
\begin{multicols}{5}""")
rep(r""" End-to-end latency is
unmeasured; Aim 3 measures it first. \emph{The RAG-LLM.}""", r""" \emph{The RAG-LLM.}""")
rep(r"""and one US insurer's 68 wrong-site claims closed in 2013--2020 averaged \$136,453,
60.3\pct{} settled, spine the commonest procedure [25].""",
    r"""and one US insurer's 68 wrong-site claims closed in 2013--2020 averaged \$136,453, spine the
commonest procedure [25].""")
p.write_text(s); print("cuts 2 applied")
