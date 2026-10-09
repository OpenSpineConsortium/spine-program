"""Refresh HANDOFF/context/ and HANDOFF/GREG_ONLY/context*/ from the live memory notes.

Written 2026-10-08 to replace the context half of copy_context.py (its working-notes half read a session scratchpad
that may be swept). Run it on Greg's laptop immediately before handing the folder over:

    python HANDOFF/working_notes/builders/refresh_context.py

What it does, note by note (the memory folder is read, never written):
- U251 / LITT notes and the history-only entry points: not copied (another project; superseded entry points).
- Beethoven product notes: copied to GREG_ONLY/context_beethoven/ (their facts are cited by INFRASTRUCTURE.md).
- GREG_ONLY notes (the commercial stance, the disclosure-scrub state, the credential-location notes) and MEMORY.md (as an
  archive of the original index): copied to GREG_ONLY/context/ only, and removed from context/ if a copy is there.
- REDACT notes (personal or contact data): the full copy goes to GREG_ONLY/context/; context/ gets a copy with those
  lines replaced by a pointer.
- every other note: copied to context/.
Every copy keeps the original bytes and line endings except one substitution: the word Greg bans (see
CTSpinoPelvic1K-1/CLAUDE.md "Standing preferences") is replaced, and the one note whose file name carries it is renamed.
The script refuses to write if the word survives or a token-shaped string appears. It stamps COPIED_AT.txt in each
target folder with the copy time and each source note's modification time.
"""
import datetime
import io
import os
import re
import sys

MEM = "<the memory folder; copies in memory/ of this project, statuses in docs/handoff/context/INDEX.md>/"
HANDOFF = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CTX = os.path.join(HANDOFF, "context")
GO_CTX = os.path.join(HANDOFF, "GREG_ONLY", "context")
GO_BTH = os.path.join(HANDOFF, "GREG_ONLY", "context_beethoven")

BANNED = "prove" + "nance"          # assembled so this file does not carry the word either
RULE_TEXT = "[the word named in CTSpinoPelvic1K-1/CLAUDE.md \"Standing preferences\"]"

U251 = {"u251-cibersort-deconvolution.md", "u251-multiomics-sample-pairing.md", "u251-name-sweep-traps.md",
        "u251-project-containment.md", "u251-translation-fall-il68b.md", "litt-contralateral-two-readings.md",
        "cns-abstract-418-deck.md"}
HISTORY = {"resume-2026-09-21-pm.md", "resume-2026-09-22-pm.md", "resume-2026-09-22.md", "resume-2026-09-24.md",
           "overnight-2026-09-15-chains.md", "resume-2026-09-26-handoff.md"}
BEETHOVEN = {"ashley-bridge-project.md", "ashley-compliance-boundary.md", "ashley-extension-project.md",
             "beethoven-2026-10-02-field-failures.md", "beethoven-browser-ssh.md", "beethoven-first-run-ux.md"}
GREG_ONLY = {"MEMORY.md", "commercialization-stance.md", "schwingnet-disclosure-scrub.md", "hf-org-token-location.md",
             "hf-osc-token-and-namespace.md", "fluorocap-credentials-and-resolution.md"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b")
POINTER = "[contact details withheld here; the full note is in HANDOFF/GREG_ONLY/context/{name}]"


def redact_contacts(name, text):
    text = EMAIL.sub(POINTER.format(name=name), text)
    return PHONE.sub("[phone withheld]", text)


def redact_roster(name, text):
    # the per-student tally block (indented lines of "username count, ...") becomes a pointer
    return re.sub(r"(\n {4}[^\n]+){1,6}\n",
                  "\n    [per-person usernames and counts withheld here; the full note is in "
                  "HANDOFF/GREG_ONLY/context/" + name + "]\n", text, count=1)


REDACT = {"annotator-roster.md": redact_roster,
          "learned-formation-refuted-calibrate-instead.md": redact_contacts,
          "lstv-data-landscape.md": redact_contacts}

TOKEN_RX = re.compile(r"(hf_[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9]{16,}"
                      r"|AKIA[A-Z0-9]{12,}|https://[^\s/]+:[^\s@]+@)")


def scrub(text):
    text = text.replace('**"' + BANNED + '"**', "**" + RULE_TEXT + "**")
    text = text.replace('"' + BANNED + '"', RULE_TEXT)
    text = text.replace("splits-" + BANNED + "-", "splits-origin-")
    return text.replace(BANNED.capitalize(), "Origin").replace(BANNED.upper(), "ORIGIN").replace(BANNED, "origin")


def write(folder, name, text):
    if BANNED in text.lower() or TOKEN_RX.search(text):
        sys.exit("REFUSE: banned word or token-shaped string would be written in %s/%s" % (folder, name))
    os.makedirs(folder, exist_ok=True)
    with io.open(os.path.join(folder, name), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stamps = {CTX: [], GO_CTX: [], GO_BTH: []}
    removed = []
    for name in sorted(os.listdir(MEM)):
        if not name.endswith(".md") or name in U251 or name in HISTORY:
            continue
        path = os.path.join(MEM, name)
        with io.open(path, "r", encoding="utf-8", newline="") as fh:
            raw = fh.read()
        if TOKEN_RX.search(raw):
            print("SKIP (token-shaped string in the original):", name)
            continue
        out = name.replace("splits-" + BANNED + "-", "splits-origin-")
        text = scrub(raw)
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
        if name in BEETHOVEN:
            write(GO_BTH, out, text)
            stamps[GO_BTH].append((out, mtime))
        elif name in GREG_ONLY:
            write(GO_CTX, out, text)
            stamps[GO_CTX].append((out, mtime))
            if os.path.exists(os.path.join(CTX, out)):
                os.remove(os.path.join(CTX, out))
                removed.append(out)
        elif name in REDACT:
            write(GO_CTX, out, text)
            stamps[GO_CTX].append((out, mtime))
            red = REDACT[name](out, text)
            if red == text:
                sys.exit("REFUSE: nothing was redacted in " + name)
            write(CTX, out, red)
            stamps[CTX].append((out + " (redacted)", mtime))
        else:
            write(CTX, out, text)
            stamps[CTX].append((out, mtime))
    for folder, rows in stamps.items():
        lines = ["copied %s by HANDOFF/working_notes/builders/refresh_context.py from %s" % (now, MEM),
                 "%d notes; each line: note, modification time of the memory original" % len(rows), ""]
        lines += ["%s\t%s" % r for r in rows]
        write(folder, "COPIED_AT.txt", "\n".join(lines) + "\n")
        print("%-60s %d notes" % (folder, len(rows)))
    if removed:
        print("removed from context/ (now GREG_ONLY):", ", ".join(removed))


if __name__ == "__main__":
    main()
