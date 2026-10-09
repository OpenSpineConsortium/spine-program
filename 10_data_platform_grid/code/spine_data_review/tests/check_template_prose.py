"""Bare digits in the template's Methods and Discussion prose (the 'numbers under ten spelled out'
style rule; PROTOCOL.md section 13 enforces only Abstract and Results), caption word counts
(limit 60) and the forbidden word. Read-only. Run: python tests/check_template_prose.py
"""
from __future__ import annotations

import re
from pathlib import Path
WORD = "prov" + "enance"  # the banned word, spelled in two halves so this file does not carry it

ROOT = Path(__file__).resolve().parent.parent
t = (ROOT / "manuscript" / "template.tex").read_text(encoding="utf-8")
STRIP = r"\\(cite[tp]?|ref|label|input|num[A-Za-z]*|pending|tabref|figref|yearRange|url)\*?(\[[^\]]*\])?(\{[^}]*\})*"
for name, pat in (("methods", r"\\section\{Methods\}(.*?)\\section\{Results\}"),
                  ("discussion", r"\\section\{Discussion\}(.*?)\\bibliographystyle")):
    m = re.search(pat, t, re.S)
    body = re.sub(r"(?m)%.*$", "", m.group(1)) if m else ""
    body = re.sub(STRIP, " ", body)
    print(name, "digit tokens:", sorted(set(re.findall(r"[^\s~]*\d[^\s~]*", body))))
caps = re.findall(r"\\caption\{(.*?)\}\\label", t)
print("caption word counts:", [len(re.sub(r"\\[a-zA-Z]+(\{[^}]*\})?", " ", c).split()) for c in caps])
print("'" + WORD + "' occurrences:", len(re.findall(WORD, t, re.I)))
