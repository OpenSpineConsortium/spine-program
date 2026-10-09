# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/diagnostics/ctsp_crosswalk_leak.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does one CTSpinoPelvic1K patient reach a level bank under TWO names, split independently?

`~/ctsp_drr` names a case CTSP_COLONOG_<n> (the Dataset813 stem); `~/physics_drr` and `~/physics_rare` name the
same patient ctsp_<release id>_<view>_p<k> (`source_case` in the ann). make_context_crops splits per SOURCE, so
if the two names are not tied together the same CT can be train under one and validation under the other -- the
NHANES defect at CT level. The tie is the Dataset813 imagesTr symlink: COLONOG_<n>_0000.nii.gz -> <id>_ct.nii.gz.
"""
import json
import re
import sys
from pathlib import Path

S = Path(r"<session scratchpad; not a dependency>")

# COLONOG_<n> -> release id, from the Dataset813 symlinks
x = {}
for line in (S / "d813_links.txt").read_text().splitlines():
    m = re.search(r"(COLONOG_[^_]+)_0000\.nii\.gz -> .*/(\d{4})_ct\.nii\.gz", line)
    if m:
        x[m.group(1)] = m.group(2)
print(f"crosswalk: {len(x)} COLONOG stems -> release ids")

# every case of every render bank, by section
sections, cur = {}, None
for line in (S / "ann_lists.txt").read_text().splitlines():
    line = line.strip()
    if line == "===":
        cur = None; continue
    if not line:
        continue
    if line.endswith(".json"):
        sections.setdefault(cur or "first", []).append(line[:-5])
order = ["ctsp_drr", "physics_drr", "physics_rare", "verse_drr", "ts_drr"]
keys = list(sections)
banks = {}
if len(keys) == 1:                      # sections separated by === lines that we consumed; re-split by name shape
    names = sections[keys[0]]
    banks["ctsp_drr"] = [n for n in names if n.startswith("CTSP_COLONOG_")]
    phys = [n for n in names if n.startswith("ctsp_") or n.startswith("verse_") or n.startswith("totalseg_") or n.startswith("implant_")]
    banks["physics"] = phys
    banks["verse_drr"] = [n for n in names if re.fullmatch(r"(gl|verse)\w*", n)]
    banks["ts_drr"] = [n for n in names if n.startswith("TS_")]
else:
    for k, v in zip(order, keys):
        banks[k] = sections[v]
for k, v in banks.items():
    print(f"  {k:<14} {len(v)} cases")


def patient_of(case):
    """The person, across naming schemes. CTSP_COLONOG_<n> -> release id; ctsp_<id>_... -> release id."""
    m = re.fullmatch(r"CTSP_(COLONOG_[^_]+)", case)
    if m:
        return ("ctsp", x.get(m.group(1), "UNMAPPED:" + m.group(1)))
    m = re.match(r"ctsp_(\d{4})_", case)
    if m:
        return ("ctsp", m.group(1))
    m = re.match(r"(?:verse|gl)(\w+?)(?:_(?:lat|ap)_p\d+)?$", case)
    if m:
        return ("verse", m.group(1))
    m = re.match(r"verse_(.+?)_(?:lat|ap)_p\d+$", case)
    if m:
        return ("verse", m.group(1))
    m = re.match(r"(?:TS_|totalseg_)(s\d+)", case)
    if m:
        return ("ts", m.group(1))
    m = re.match(r"implant_(.+?)_(?:lat|ap)_p\d+$", case)
    if m:
        return ("implant", m.group(1))
    return ("?", case)


for bank_name in ("allspine_v7_fov96_ctx", "allspine_v6_fov96_ctx"):
    meta = json.loads((S / "banks" / f"{bank_name}.meta.json").read_text())
    val = set(meta["val_cases"])
    print(f"\n=== {bank_name}: {len(val)} validation cases")
    val_pat, train_pat = {}, {}
    for src, cases in banks.items():
        for c in cases:
            p = patient_of(c)
            (val_pat if c in val else train_pat).setdefault(p, set()).add(src)
    both = {p: (val_pat[p], train_pat[p]) for p in val_pat if p in train_pat}
    print(f"  patients in validation: {len(val_pat)}; in training: {len(train_pat)}; in BOTH: {len(both)}")
    cross = {p: v for p, v in both.items() if not (v[0] & v[1])}
    print(f"  of those, patients whose two sides come from DIFFERENT render banks: {len(cross)}")
    for p, (a, b) in list(cross.items())[:8]:
        print(f"     {p}  val via {sorted(a)}  train via {sorted(b)}")
    unmapped = [p for p in list(val_pat) + list(train_pat) if isinstance(p[1], str) and p[1].startswith("UNMAPPED")]
    print(f"  unmapped stems: {len(set(unmapped))}")
