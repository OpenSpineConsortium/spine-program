# spine-program copy (2026-10-08): laptop path literals were replaced by the tokens [repo:<name>], [laptop:<what>] and "(session scratch path, not kept)"; see MANIFEST_LOCAL.md section 2. The repository copy is the one to run.
# RECORD ONLY (2026-10-08 verification pass): superseded by refresh_context.py. Do not rerun: its context half would put
# the moved notes back into HANDOFF/context/ and undo the three redactions, and its working-notes half reads a session
# scratchpad that may have been swept.
"""Copy the reader notes and the live spine-imaging memory notes into spinesurg-ct-nnunet/HANDOFF.

- working_notes/: the six topic notes written by the readers on 2026-10-08, verbatim, plus the Wilson check script.
- context/: every memory note except the U251 notes, the history-only entry points and the Beethoven product notes,
  copied byte for byte except for one substitution: the word Greg bans (see ctsp CLAUDE.md "Standing preferences")
  is replaced, and the one note whose file name carries it is renamed. A report of every change is printed.
"""
import os
import re
import shutil
import sys

SCR = ("(session scratch path, not kept)/"
       "0599380b-0d32-4e19-b5be-65bdd1017566/scratchpad/handoff/")
MEM = "[laptop:memory-notes]/"
OUT = "[repo:spinesurg-ct-nnunet]/HANDOFF/"

BANNED = "prove" + "nance"          # assembled so this file does not carry the word either
RULE_TEXT = "[the word named in CTSpinoPelvic1K-1/CLAUDE.md \"Standing preferences\"]"

NOTES = {
    "topic1_schwingnet_carm_results.md": "topic1_schwingnet_carm_results.md",
    "topic2_scaling_samples_anomaly_power.md": "topic2_scaling_samples_anomaly_power.md",
    "topic3_dataset_usage_leakage_rsna.md": "topic3_dataset_usage_leakage_rsna.md",
    "topic4_manuscripts.md": "topic4_manuscripts.md",
    "05_operating_here.md": "topic5_operating_here.md",
    "topic6_ctspinopelvic1k_and_toolkit.md": "topic6_ctspinopelvic1k_and_toolkit.md",
}

U251 = {"u251-cibersort-deconvolution.md", "u251-multiomics-sample-pairing.md", "u251-name-sweep-traps.md",
        "u251-project-containment.md", "u251-translation-fall-il68b.md", "litt-contralateral-two-readings.md",
        "cns-abstract-418-deck.md"}
HISTORY = {"resume-2026-09-21-pm.md", "resume-2026-09-22-pm.md", "resume-2026-09-22.md", "resume-2026-09-24.md",
           "overnight-2026-09-15-chains.md", "resume-2026-09-26-handoff.md"}
BEETHOVEN = {"ashley-bridge-project.md", "ashley-compliance-boundary.md", "ashley-extension-project.md",
             "beethoven-2026-10-02-field-failures.md", "beethoven-browser-ssh.md", "beethoven-first-run-ux.md"}

TOKEN_RX = re.compile(r"(hf_[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9]{16,}"
                      r"|AKIA[A-Z0-9]{12,}|https://[^\s/]+:[^\s@]+@)")


def scrub(text: str) -> str:
    # rule statements first, so the rule still reads as a rule
    text = text.replace('**"' + BANNED + '"**', "**" + RULE_TEXT + "**")
    text = text.replace('"' + BANNED + '"', RULE_TEXT)
    text = text.replace("splits-" + BANNED + "-", "splits-origin-")
    text = text.replace(BANNED.capitalize(), "Origin").replace(BANNED.upper(), "ORIGIN").replace(BANNED, "origin")
    return text


def main() -> int:
    wn = os.path.join(OUT, "working_notes")
    ctx = os.path.join(OUT, "context")
    os.makedirs(wn, exist_ok=True)
    os.makedirs(ctx, exist_ok=True)

    for src, dst in NOTES.items():
        text = open(os.path.join(SCR, "notes", src), encoding="utf-8").read()
        if BANNED in text.lower():
            print("REFUSE: banned word in", src)
            return 1
        if TOKEN_RX.search(text):
            print("REFUSE: credential-like value in", src)
            return 1
        shutil.copyfile(os.path.join(SCR, "notes", src), os.path.join(wn, dst))
    shutil.copyfile(os.path.join(SCR, "t2_wilson_check.py"), os.path.join(wn, "t2_wilson_check.py"))
    print("working_notes:", len(NOTES), "notes + t2_wilson_check.py")

    copied, changed, skipped = [], [], []
    for name in sorted(os.listdir(MEM)):
        if not name.endswith(".md"):
            continue
        if name in U251 or name in HISTORY or name in BEETHOVEN:
            skipped.append(name)
            continue
        raw = open(os.path.join(MEM, name), encoding="utf-8").read()
        if TOKEN_RX.search(raw):
            print("SKIP (credential-like value):", name)
            skipped.append(name)
            continue
        out_name = name.replace("splits-" + BANNED + "-", "splits-origin-")
        new = scrub(raw)
        if BANNED in new.lower():
            print("REFUSE: substitution incomplete in", name)
            return 1
        with open(os.path.join(ctx, out_name), "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
        copied.append(out_name)
        if new != raw or out_name != name:
            changed.append((name, out_name))
    print("context: copied", len(copied), "files; skipped", len(skipped))
    print("changed by the substitution:")
    for a, b in changed:
        print("  ", a if a == b else a.replace(BANNED, "<word>") + " -> " + b)
    print("skipped:")
    for s in skipped:
        print("  ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
