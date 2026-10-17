"""Parse the ready-to-send request letters into data_mining/data/requests.json: one record per numbered source, with
the checklist row, the subject, the sending route, what to expect and the letter text. Addresses are withheld in the
source files except the sender's own signature. Run from anywhere: paths are relative to this file."""
import json
import os
import re
import sys

BUILD = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(BUILD))
REQ = os.path.join(REPO, "01_carm_level_detection", "docs", "data_requests")
src = os.path.join(REQ, "FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md")
extra = {
    "balgrist": os.path.join(REQ, "balgrist_data_request_2026-09-21.md"),
    "sxstitch": os.path.join(REQ, "SX-Stitch_request.md"),
}
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(BUILD), "data", "requests.json")
s = open(src, encoding="utf-8").read()

# checklist rows
rows = {}
for line in s.splitlines():
    m = re.match(r"^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
    if m:
        rows[int(m.group(1))] = dict(source=m.group(2), gets=m.group(3), route=m.group(4), effort=m.group(5), status=m.group(6))

# sections
secs = re.split(r"^## (\d+)\. (.+)$", s, flags=re.M)
items = []
for i in range(1, len(secs) - 2, 3):
    n = int(secs[i]); title = secs[i + 1].strip(); body = secs[i + 2]
    body = body.split("\n## ")[0]
    subj = re.search(r"^\*\*Subject:\*\* (.+)$", body, re.M)
    expect = re.search(r"^Expect: (.+)$", body, re.M)
    verified = re.search(r"^Verified: (.+)$", body, re.M)
    how = re.search(r"\*\*How to send:\*\* (.+?)(?:\n\n|\n(?=Expect))", body, re.S)
    letter = re.search(r"```text\n(.*?)```", body, re.S)
    # notes between Verified and the letter (bullets), stripped of markdown emphasis
    notes = []
    for ln in body.splitlines():
        if ln.startswith("- ") and "How to send" not in ln:
            notes.append(ln[2:].strip())
    rec = dict(n=n, title=title, **rows.get(n, {}))
    rec["subject"] = subj.group(1).strip() if subj else None
    rec["expect"] = expect.group(1).strip() if expect else None
    rec["verified"] = verified.group(1).strip() if verified else None
    rec["how"] = re.sub(r"\s+", " ", how.group(1)).strip() if how else None
    rec["notes"] = notes[:6]
    rec["letter"] = letter.group(1).rstrip() if letter else None
    items.append(rec)

def letter_from(path, start_marker=None):
    t = open(path, encoding="utf-8").read()
    if start_marker and start_marker in t:
        t = t.split(start_marker, 1)[1]
    return t.strip()

bal = open(extra["balgrist"], encoding="utf-8").read()
subj_b = re.search(r"^Subject: (.+)$", bal, re.M)
items.append(dict(n=15, title="Balgrist (Jecklin et al., Medical Image Analysis 2024): ex-vivo lumbar CT with real C-arm X-rays",
                  source="Balgrist University Hospital, Zurich", gets="13 + 6 ex-vivo lumbar specimens: CT volumes, every real X-ray, the fiducial projection matrix per image, and the C-arm that took it (three devices)",
                  route="Email (letter below)", effort="5 min; a data-transfer agreement through WSU", status="Ready. Set is restricted because of pending patents",
                  subject=subj_b.group(1).strip() if subj_b else None, expect="A data-use or transfer agreement on their terms; restricted set, so it may be refused or limited.",
                  verified=None, how="Email the corresponding author of the Medical Image Analysis 2024 paper (address on the paper).", notes=[],
                  letter=bal.split("\n\n", 1)[1].strip() if "\n\n" in bal else bal))
sx = open(extra["sxstitch"], encoding="utf-8").read()
subj_s = re.search(r"^Subject: (.+)$", sx, re.M)
items.append(dict(n=16, title="SX-Stitch (Li et al., arXiv 2409.05681): overlapping intraoperative C-arm series",
                  source="SUSTech / Peking Union Medical College Hospital", gets="1,032 intraoperative C-arm spine images in consecutive overlapping series (20 to 90 % overlap) with vertebra masks",
                  route="Email (SUSTech and PUMCH directory addresses; none printed in the arXiv paper)", effort="5 min", status="Ready",
                  subject=subj_s.group(1).strip() if subj_s else None, expect="An academic request; the only published set of real overlapping C-arm sweeps, the acquisition your sweep protocol simulates.",
                  verified=None, how="Find the corresponding authors' institutional addresses (Wei Liu, SUSTech; Jinqian Liang, PUMCH) and email the letter.", notes=[],
                  letter=sx.split("---", 1)[1].strip() if "---" in sx else sx))
# strip the To/Cc lines and any withheld markers from letters
for it in items:
    if it.get("letter"):
        L = [ln for ln in it["letter"].splitlines() if not re.match(r"^(To|Cc):", ln)]
        it["letter"] = "\n".join(L).strip()
for it in items:
    if it.get("letter"):
        it["letter"] = it["letter"].replace("info@daradia.com", "[the address on daradia.com]")
    it["notes"] = [n.replace("info@daradia.com", "[the address on daradia.com]") for n in it.get("notes", [])]
json.dump(items, open(out, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(len(items), "request records;", sum(1 for i in items if i.get("letter")), "with letters")
