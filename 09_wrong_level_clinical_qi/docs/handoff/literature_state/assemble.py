"""Insert the newest-first bibliography into LITERATURE_STATE.md, strip licence version numbers from it, then check the
whole document for forbidden words and fractional version numbers, and count table rows per section."""
import re
from pathlib import Path

HERE = Path(__file__).parent
DOC = Path("<spinesurg-ct-nnunet 097933a>/HANDOFF/LITERATURE_STATE.md")
BIB = HERE / "biblio_sorted.md"

doc = DOC.read_text(encoding="utf-8")
bib = BIB.read_text(encoding="utf-8").rstrip("\n")

# licence names without their version number
bib = re.sub(r"\b(CC BY(?:-[A-Z]{2})*(?:-[A-Z]{2})?) \d\.\d\b", r"\1", bib)
bib = bib.replace("Apache-2.0", "Apache")

if "<!-- BIBLIO -->" in doc:
    doc = doc.replace("<!-- BIBLIO -->", bib)
    DOC.write_text(doc, encoding="utf-8")
    print("bibliography inserted")
else:
    print("placeholder not found (already inserted?)")

doc = DOC.read_text(encoding="utf-8")
problems = []
for i, line in enumerate(doc.splitlines(), 1):
    if re.search("prov" "enance", line, re.I):  # the banned word, spelled in two pieces so this file never carries it
        problems.append((i, "banned word", line[:120]))
    for m in re.finditer(r"\b[vV]?\d+\.\d+\.\d+\b", line):
        problems.append((i, "semver " + m.group(0), line[:120]))
    for m in re.finditer(r"CC BY[A-Z-]* \d\.\d", line):
        problems.append((i, "licence version " + m.group(0), line[:120]))
    for m in re.finditer(r"\bv\d+\.\d+\b", line):
        problems.append((i, "version " + m.group(0), line[:120]))
    if re.search(r"[\U0001F300-\U0001FAFF]", line):
        problems.append((i, "emoji", line[:120]))
print("problems:", len(problems))
for p in problems:
    print(p)

# count table data rows per top-level section
sec = None
counts = {}
for line in doc.splitlines():
    m = re.match(r"^## (\d)\. ", line)
    if m:
        sec = m.group(1)
        continue
    if line.startswith("## "):
        sec = None
        continue
    if sec and line.startswith("| ") and not line.startswith("|---"):
        counts.setdefault(sec, []).append(line)
for s, rows in sorted(counts.items()):
    print("section", s, "table lines incl. headers:", len(rows))
print("chars", len(doc), "lines", len(doc.splitlines()))
