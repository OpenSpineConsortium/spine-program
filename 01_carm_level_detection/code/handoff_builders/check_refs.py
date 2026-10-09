# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): HANDOFF/working_notes/builders/check_refs.py [tracked at 097933a]
"""Check that every `context/<note>.md`, `GREG_ONLY/context*/<note>.md` and `mem:<note>` reference in the handoff files
names a note that is actually there, and that every `working_notes/<file>` reference exists.
(Updated 2026-10-08 for the GREG_ONLY split; the first version knew only HANDOFF/context/.)"""
import os
import re

H = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")) + os.sep
FILES = ["README.md", "RESULTS_CATALOG.md", "RECIPES.md", "DATASET_USAGE.md", "LEAKAGE.md", "MANUSCRIPTS.md",
         "INFRASTRUCTURE.md", "CONTEXT_EXPORT.md", "GLOSSARY.md", "OPEN_QUESTIONS.md", "LITERATURE_STATE.md",
         "GREG_ONLY/PRIVATE_STATE.md", "literature_state/power.md"]
FOLDERS = {"context": set(os.listdir(H + "context")),
           "GREG_ONLY/context": set(os.listdir(H + "GREG_ONLY/context")),
           "GREG_ONLY/context_beethoven": set(os.listdir(H + "GREG_ONLY/context_beethoven"))}
everywhere = set().union(*FOLDERS.values())
wn = set(os.listdir(H + "working_notes"))
bad = []
for f in FILES:
    text = open(H + f, encoding="utf-8").read()
    for m in re.finditer(r"(GREG_ONLY/)?(context(?:_beethoven)?)/([A-Za-z0-9_.\-]+\.(?:md|txt))", text):
        folder = (m.group(1) or "") + m.group(2)
        if folder not in FOLDERS:
            continue
        if m.group(3) not in FOLDERS[folder]:
            bad.append((f, folder + "/" + m.group(3)))
    for m in re.finditer(r"mem:([A-Za-z0-9_\-]+)(\.md)?", text):
        if m.group(1) + ".md" not in everywhere:
            bad.append((f, "mem:" + m.group(1)))
    for m in re.finditer(r"working_notes/([A-Za-z0-9_.\-]+)", text):
        name = m.group(1).rstrip(".")
        if name.endswith("_...") or name.endswith("_"):
            continue
        if name not in wn and not any(w.startswith(name) for w in wn):
            bad.append((f, "working_notes/" + name))
for b in sorted(set(bad)):
    print("BAD", b)
print("done;", len(set(bad)), "bad references")
