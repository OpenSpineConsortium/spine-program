"""Parse the topic-1 bibliography tables (sections A to G) and print them newest first as compact markdown rows.

Columns kept: date (latest date in the cell, with its basis word), file, question, conclusion, verification (first
sentence). Sort key: latest YYYY-MM-DD in the date cell, then row number. Output: biblio_sorted.md beside this script.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
NOTE = HERE / "notes" / "topic1_bibliography.md"
OUT = HERE / "biblio_sorted.md"

ROOTS = {
    "S/": "spinesurg-ct-nnunet/",
    "C/": "CTSpinoPelvic1K-1/",
    "M/": "memory/",
}

rows = []
section = None
for line in NOTE.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^## ([A-J])\. ", line)
    if m:
        section = m.group(1)
        continue
    if section not in list("ABCDEFG"):
        continue
    if not line.startswith("| ") or line.startswith("| #") or line.startswith("|---"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
    if len(cells) != 7 or not cells[0].isdigit():
        continue
    num, date, file_, question, named, concl, verified = cells
    dates = re.findall(r"20\d\d-\d\d-\d\d", date)
    key = max(dates) if dates else "0000-00-00"
    basis = None
    for w in ("stated", "mtime", "git", "modified"):
        if w in date:
            basis = w
            break
    date_disp = key + (f" ({basis})" if basis else "")
    v = verified
    # first sentence of the verification cell
    vs = re.split(r"(?<=[.)])\s+(?=[A-Z])", v)
    v1 = v if len(v) <= 240 else " ".join(vs[:2])
    rows.append((key, int(num), section, date_disp, file_, question, concl, v1))

rows.sort(key=lambda r: (r[0], -r[1]), reverse=True)

out = ["| date | file | question it answered | conclusion, as recorded in the file | verification | T1 row |",
       "|---|---|---|---|---|---:|"]
for key, num, sec, dd, f, q, c, v in rows:
    out.append(f"| {dd} | {f} | {q} | {c} | {v} | {num} |")
OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(len(rows), "rows written to", OUT)
by_sec = {}
for r in rows:
    by_sec[r[2]] = by_sec.get(r[2], 0) + 1
print(by_sec)
