"""Count the span the title page declares, and print the declaration beside it so they cannot drift apart.

The label reads "Introduction through Conclusion", so the count runs from the Introduction heading to the
END of the Conclusion paragraph, not to its start. Those two spans differ by about 120 words here, and an
earlier declaration was made against the narrower one.

Figures, tables and TikZ are excluded; citations and LaTeX control sequences are stripped. Run from the
repository root or from paper/focused.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "main.tex")
s = io.open(P, encoding="utf-8").read()

i = s.index(r"\section*{Introduction}")
# the conclusion paragraph ends at the first block comment after it, which opens the figures
j = s.index("% ---", s.index(r"\textbf{Conclusion.}"))
t = s[i:j]

t = re.sub(r"%.*", "", t)
for env in ("tikzpicture", "figure", "table", "tabular"):
    t = re.sub(r"\\begin\{" + env + r"\}.*?\\end\{" + env + r"\}", " ", t, flags=re.S)
t = re.sub(r"\\cite[a-z]*\*?(\[[^\]]*\])*\{[^}]*\}", " ", t)
t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
t = re.sub(r"[{}$\\&~^_]", " ", t)
w = [x for x in t.split() if re.search("[A-Za-z0-9]", x)]

m = re.search(r"\(Introduction through Conclusion\):\}\s*([0-9,{}]+)", s)
declared = re.sub(r"[^0-9]", "", m.group(1)) if m else None
print("measured : %d" % len(w))
print("declared : %s" % (declared or "not found"))
if declared and int(declared) != len(w):
    print("MISMATCH  -- set the title page to %d" % len(w))
    sys.exit(1)
print("agree")
