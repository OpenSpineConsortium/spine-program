import pathlib
p = pathlib.Path('/home/user/spine-program/01_carm_level_detection/grants/aidas_2027/latex/main.tex')
s = p.read_text()
def rep(old, new):
    global s
    n = s.count(old); assert n == 1, (n, old[:90]); s = s.replace(old, new)
rep(r"\setlength{\textfloatsep}{6pt}", r"\setlength{\textfloatsep}{4pt}")
rep(r"\usepackage[font=footnotesize,labelfont=bf,labelsep=period,skip=2pt,hypcap=false]{caption}",
    r"\usepackage[font=footnotesize,labelfont=bf,labelsep=period,skip=1pt,hypcap=false]{caption}")
rep(r"""every item keyed to a
person, which closed the two cross-naming leaks its identity checks found, nine leakage checks, and 563 quoted numbers
audited against their models' training persons.""",
    r"""every item keyed to a
person, nine leakage checks, and 563 quoted numbers audited against their models' training persons.""")
p.write_text(s); print("cuts 4 applied")
