import pathlib
p = pathlib.Path('/home/user/spine-program/01_carm_level_detection/grants/aidas_2027/latex/main.tex')
s = p.read_text()
def rep(old, new):
    global s
    n = s.count(old); assert n == 1, (n, old[:90]); s = s.replace(old, new)
rep(r"\setlength{\multicolsep}{3pt}", r"\setlength{\multicolsep}{1pt}")
rep(r"checks); each runs each copy once, in its own repository (80 runs).", r"checks); each runs each copy once (80 runs).")
rep(r"""The seed buys what does not exist yet:
the researcher's hours, subscriptions, the cadaver set and regulatory review; the trainee program, grid, Beethoven,
Symphony, pipelines and faculty time come in kind, and the Gaussian renderer is fitted only as a feasibility test, its
full build left to the R21.""",
    r"""The seed buys the researcher's hours,
subscriptions, the cadaver set and regulatory review; the trainee program, grid, Beethoven, Symphony, pipelines and
faculty time come in kind; the Gaussian renderer is fitted as a feasibility test, its full build left to the R21.""")
p.write_text(s); print("cuts 3 applied")
